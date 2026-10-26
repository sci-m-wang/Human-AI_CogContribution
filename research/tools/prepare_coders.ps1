$ErrorActionPreference='Stop'
Set-Location '<project>'
$u = New-Object Text.UTF8Encoding($false)
$cb = [IO.File]::ReadAllText((Resolve-Path 'research\codebook_v1.0_FROZEN.md'),$u)
$a = $cb.IndexOf('## 0. Construct'); $b = $cb.IndexOf('## 6. Coders')
$coderCb = "# Coding manual (v1.0)`r`n`r`n" + $cb.Substring($a,$b-$a)
$task = @"
# TASK (read carefully)
You are an independent coder. Apply the coding manual in codebook.md to EVERY unit in packet.md (units are headed '### UNIT <id>'). Do not skip units.
Rules: code only what is observable in the unit text; the actor_hint tells who authored the unit (use it as the actor of the tags unless the unit text clearly quotes or attributes content to the other actor, in which case tag the content by who originates it only if the unit itself originates it; do NOT re-tag a quoted instruction on the quoting unit). A unit may have several tags (multi-label), at most one primary per actor. Use residual codes X, C, Z when no cognitive type applies.
Output: write a file named result.jsonl in the current directory with ONE JSON object per line, one line per unit, exactly in the schema of section 5 of codebook.md (unit_id, tags[], uncertain, note). Keep each evidence quote <=25 words. Cover all units, in order. Do not read any files other than codebook.md and packet.md. When done, reply only with the number of units coded and the number of lines written.
"@
foreach($m in 'gpt','gemini'){
  $d = Join-Path $env:TEMP "icis_coders\$m"
  New-Item -ItemType Directory -Force -Path $d | Out-Null
  [IO.File]::WriteAllText((Join-Path $d 'codebook.md'),$coderCb,$u)
  Copy-Item research\coding\packet_all.md (Join-Path $d 'packet.md') -Force
  [IO.File]::WriteAllText((Join-Path $d 'TASK.md'),$task,$u)
  Remove-Item (Join-Path $d 'result.jsonl') -ErrorAction SilentlyContinue
}
Get-ChildItem "$env:TEMP\icis_coders" -Recurse | %{ $_.FullName + ' ' + $_.Length }
