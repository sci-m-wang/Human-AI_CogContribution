<#
.SYNOPSIS
  Snapshot ALL raw agent sessions of this project into records/raw_sessions and
  rebuild records/session_registry.csv (idempotent, safe to run repeatedly).

.DESCRIPTION
  Sources captured:
   1. every OpenCode/OpenWork session whose working directory is this project
      (this includes sub-agent / child sessions, which live in the same DB);
   2. extra OpenCode session ids listed in records/extra_sessions.txt
      (e.g. sessions started in another folder but belonging to this project);
   3. any transcript dropped by hand into records/raw_sessions/external/
      (other agents/frameworks: Claude Code, Codex, web chat exports, ...).

  Raw files are never edited. Each run overwrites the OpenCode snapshot with the
  latest full export and appends one line per snapshot to records/snapshot_log.csv
  (so growth of a session over time is itself evidence).
  Manual columns (role_in_project, notes) in the registry are preserved.

.USAGE
  powershell -NoProfile -ExecutionPolicy Bypass -File records\scripts\sync_sessions.ps1
#>
$ErrorActionPreference = 'Stop'
$env:Path = "$env:SystemRoot\System32;$env:SystemRoot;$env:Path"
$root    = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$rec     = Join-Path $root 'records'
$rawDir  = Join-Path $rec 'raw_sessions'
$extDir  = Join-Path $rawDir 'external'
$regPath = Join-Path $rec 'session_registry.csv'
$logPath = Join-Path $rec 'snapshot_log.csv'
$extra   = Join-Path $rec 'extra_sessions.txt'
New-Item -ItemType Directory -Force -Path $rawDir, $extDir | Out-Null
$now = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Convert-Ms($ms) { if ($ms) { [DateTimeOffset]::FromUnixTimeMilliseconds([int64]$ms).ToLocalTime().ToString('yyyy-MM-ddTHH:mm:sszzz') } else { '' } }

# ---- preserve manual columns from the existing registry
$manual = @{}
if (Test-Path $regPath) {
  Import-Csv $regPath -Encoding UTF8 | ForEach-Object { $manual[$_.session_id] = @{ role = $_.role_in_project; notes = $_.notes; fw = $_.agent_framework; ver = $_.framework_version; mdl = $_.models; ag = $_.agent_names; cr = $_.created } }
}

# ---- 1+2: discover OpenCode sessions and write the raw snapshots straight from the OpenCode database (read-only).
# Changed 2026-10-22: the `opencode` CLI was upgraded, `opencode export <id>` now prints its help text (which the old script
# wrote over 29 raw snapshots) and `opencode session export` omits messages removed by context compaction. The database is
# the source of truth: records/scripts/export_session_legacy.py rebuilds the legacy export (info + parts) from the
# `session/message/part` tables and dumps the v2 tables (`session_v2/session_message`), which hold every message written
# since the cut-over. Both files are kept: raw_sessions/<id>.json (legacy) and raw_sessions_v2/<id>.json (v2).
# A file is never replaced by a version with fewer messages. See records/incidents/20261022_sync_overwrite.
$v2Dir = Join-Path $rec 'raw_sessions_v2'
$py = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python311\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
$extraIds = @()
if (Test-Path $extra) {
  $extraIds = @(Get-Content $extra -Encoding UTF8 | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') })
}
$regIds = @()
if (Test-Path $regPath) { $regIds = @(Import-Csv $regPath -Encoding UTF8 | Where-Object { $_.source -eq 'opencode' } | ForEach-Object { $_.session_id }) }
$argList = @((Join-Path $PSScriptRoot 'export_session_legacy.py'), 'sync', $rawDir, $v2Dir, $root) + $extraIds + $regIds
$syncOut = & $py @argList
if ($LASTEXITCODE -ne 0 -or -not $syncOut) { throw "database export failed; raw snapshots were left untouched" }
$report = $syncOut | ConvertFrom-Json
$ids = New-Object System.Collections.Generic.List[string]
$v2n = @{}
foreach ($r in $report) { $ids.Add($r.session_id); $v2n[$r.session_id] = [string]$r.v2 }

$rows = New-Object System.Collections.Generic.List[object]
for ($qi = 0; $qi -lt $ids.Count; $qi++) {
  $id = $ids[$qi]
  $out = Join-Path $rawDir "$id.json"
  if (-not (Test-Path $out) -or (Get-Item $out).Length -lt 10) { Write-Warning "no snapshot for $id"; continue }
  $sha = (Get-FileHash $out -Algorithm SHA256).Hash.ToLower()
  $row = [ordered]@{
    session_id=$id; source='opencode'; title=''; directory=''; parent_session_id=''
    agent_framework='OpenCode (via OpenWork)'; framework_version=''; agent_names=''; models=''
    created=''; updated=''; user_msgs=0; assistant_msgs=0; raw_file=("raw_sessions/$id.json")
    sha256=$sha; bytes=(Get-Item $out).Length; exported_at=$now; role_in_project=''; notes=''
    v2_file=("raw_sessions_v2/$id.json"); v2_messages=$v2n[$id]
  }
  try {
    $j = [IO.File]::ReadAllText($out, $utf8) | ConvertFrom-Json
    $row.title = $j.info.title; $row.directory = $j.info.directory
    $row.parent_session_id = [string]$j.info.parentID
    $row.framework_version = [string]$j.info.version
    $row.created = Convert-Ms $j.info.time.created; $row.updated = Convert-Ms $j.info.time.updated
    $row.user_msgs = @($j.messages | Where-Object { $_.info.role -eq 'user' }).Count
    $row.assistant_msgs = @($j.messages | Where-Object { $_.info.role -eq 'assistant' }).Count
    $row.agent_names = (($j.messages | ForEach-Object { $_.info.agent } | Where-Object { $_ } | Sort-Object -Unique) -join ';')
    $ms = $j.messages | ForEach-Object {
      $i = $_.info
      if ($i.role -eq 'assistant' -and $i.modelID) { "$($i.providerID)/$($i.modelID)" }
      elseif ($i.model) { "$($i.model.providerID)/$($i.model.modelID)" }
    } | Where-Object { $_ } | Sort-Object -Unique
    $row.models = ($ms -join ';')
  } catch { $row.notes = "metadata parse failed: $($_.Exception.Message)" }
  if ($manual.ContainsKey($id)) { $row.role_in_project = $manual[$id].role; if ($manual[$id].notes) { $row.notes = $manual[$id].notes } }
  $rows.Add([pscustomobject]$row)
  [pscustomobject]@{ exported_at=$now; session_id=$id; sha256=$sha; bytes=$row.bytes; messages=($row.user_msgs+$row.assistant_msgs) } |
    Export-Csv $logPath -Append -NoTypeInformation -Encoding UTF8
}

# ---- 3: external transcripts
Get-ChildItem $extDir -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne 'README.txt' } | ForEach-Object {
  $sid = 'ext_' + [IO.Path]::GetFileNameWithoutExtension($_.Name)
  $sha = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
  $row = [ordered]@{
    session_id=$sid; source='external'; title=$_.Name; directory=''; parent_session_id=''
    agent_framework='(fill in)'; framework_version='(fill in)'; agent_names=''; models='(fill in)'
    created=''; updated=(Convert-Ms ([DateTimeOffset]$_.LastWriteTime).ToUnixTimeMilliseconds()); user_msgs=''; assistant_msgs=''
    raw_file=("raw_sessions/external/" + $_.Name); sha256=$sha; bytes=$_.Length; exported_at=$now; role_in_project=''; notes=''
  }
  if ($manual.ContainsKey($sid)) {
    $m = $manual[$sid]
    $row.role_in_project = $m.role; $row.notes = $m.notes; $row.agent_framework = $m.fw; $row.framework_version = $m.ver
    $row.models = $m.mdl; $row.agent_names = $m.ag; $row.created = $m.cr
  }
  $rows.Add([pscustomobject]$row)
}

$rows | Export-Csv $regPath -NoTypeInformation -Encoding UTF8
Write-Host "Synced $($rows.Count) session(s) at $now -> records/session_registry.csv"
$rows | ForEach-Object { Write-Host (" - {0}  msgs={1}/{2}  {3}" -f $_.session_id, $_.user_msgs, $_.assistant_msgs, $_.title) }
