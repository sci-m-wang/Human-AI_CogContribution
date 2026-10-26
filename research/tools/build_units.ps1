$ErrorActionPreference='Stop'
$env:Path = "$env:SystemRoot\System32;$env:SystemRoot;$env:Path"
Set-Location '<project>'
$u = New-Object Text.UTF8Encoding($false)
$maxChars = 2500
$reg = Import-Csv records\session_registry.csv -Encoding UTF8
# fixed session labels (stable across syncs). Coder sessions are excluded from the coded corpus.
$fixed = [ordered]@{
 'ses_ea32c9901ffe7o77BUt54LtH2Q'='S01'; 'ses_ea385f0bbffeXU99hpIMQgJxgX'='S02'; 'ses_ea307c02bffeHFBzAFG8xzW7wK'='S03'
 'ses_ea3079637ffegcYEhVlpvXOQLD'='S04'; 'ses_ea3075e9dffepzhhWfOy15F93b'='S05'; 'ses_ea2fdf10affejkfzAd0fMZsLJI'='S06'
 'ses_ea2fdcef5ffeXKndXENbHHYRxK'='S07'; 'ses_ea2fda8d8ffeZDcicyKTJC6TRa'='S08'; 'ses_ea2fd860cffeg2KP3aSGwTejfk'='S09'
 'ses_ea2e936ffffeS9S8yrARqHuQsx'='S10'; 'ses_ea2e91aa9ffeDU95gks8Fcqxu0'='S11'; 'ses_ea2e8f9caffe5i41TQ760735pH'='S12' }
$reg = @($reg | Where-Object { $_.title -notlike 'coder-*' })
$label=@{}; foreach($k in $fixed.Keys){ $label[$k]=$fixed[$k] }
$nextN=13
foreach($s in $reg){ if(-not $label.ContainsKey($s.session_id)){ $label[$s.session_id]=('S{0:D2}' -f $nextN); $nextN++ } }
$units = New-Object System.Collections.Generic.List[object]
foreach($s in $reg){
  $j = [IO.File]::ReadAllText((Join-Path 'records' $s.raw_file), $u) | ConvertFrom-Json
  $isChild = [bool]$s.parent_session_id
  $pending = New-Object System.Collections.Generic.List[string]   # tool-only steps
  $files = New-Object System.Collections.Generic.List[string]
  $n=0
  foreach($m in $j.messages){
    $t = $m.info.time.created
    if($m.info.role -eq 'user'){
      $txt = (($m.parts | ?{$_.type -eq 'text'} | %{$_.text}) -join "`n")
      $actor = if($isChild){'AI-primary (prompt to a sub-agent)'}else{'human'}
      $n++
      $units.Add([pscustomobject]@{ unit_id=("{0}-U{1:D3}" -f $label[$s.session_id],$n); session=$label[$s.session_id]; message_id=$m.info.id; time=$t; actor_hint=$actor; kind='user_message'; text=$txt; tools=''; files=''; spawned='' })
      $pending.Clear(); $files.Clear()
      continue
    }
    if($m.info.role -ne 'assistant'){ continue }
    $txt = (($m.parts | ?{$_.type -eq 'text'} | %{$_.text}) -join "`n").Trim()
    $tools = @($m.parts | ?{$_.type -eq 'tool'})
    foreach($tp in $tools){
      $st=$tp.state; $inp=$st.input
      $desc = $tp.tool
      if($inp){
        if($inp.filePath){ $desc += ':'+$inp.filePath; if($tp.tool -in 'write','edit'){ $files.Add([string]$inp.filePath) } }
        elseif($inp.command){ $c=[string]$inp.command; $desc += ':'+($c.Substring(0,[Math]::Min(90,$c.Length))) }
        elseif($inp.url){ $desc += ':'+$inp.url }
        elseif($inp.description){ $desc += ':'+$inp.description }
      }
      $pending.Add($desc)
    }
    $spawn = @($tools | ?{$_.tool -eq 'task'})
    if($txt.Length -gt 0 -or $spawn.Count -gt 0){
      $n++
      $sp = ''
      if($spawn.Count){ $sp = (($spawn | %{ $_.state.input.description }) -join ' | ') }
      $units.Add([pscustomobject]@{ unit_id=("{0}-U{1:D3}" -f $label[$s.session_id],$n); session=$label[$s.session_id]; message_id=$m.info.id; time=$t; actor_hint=$(if($isChild){'AI-subagent'}else{'AI-primary'}); kind='ai_response'; text=$txt; tools=($pending -join ' ; '); files=(($files|Select-Object -Unique) -join ' ; '); spawned=$sp })
      $pending.Clear(); $files.Clear()
    }
  }
}
$units | Export-Csv research\coding\units_all.csv -NoTypeInformation -Encoding UTF8
# packet file (markdown) for coders, truncated and blind
$sb = New-Object System.Text.StringBuilder
foreach($x in $units){
  $tx = [string]$x.text
  $trunc=''
  if($tx.Length -gt $maxChars){ $tx=$tx.Substring(0,$maxChars); $trunc=' [TRUNCATED]' }
  [void]$sb.AppendLine("### UNIT $($x.unit_id)")
  [void]$sb.AppendLine("session: $($x.session) | message_id: $($x.message_id) | actor_hint: $($x.actor_hint) | kind: $($x.kind)")
  if($x.spawned){ [void]$sb.AppendLine("spawned_subagents: $($x.spawned)") }
  if($x.tools){ $tl=[string]$x.tools; if($tl.Length -gt 700){$tl=$tl.Substring(0,700)+' ...'}; [void]$sb.AppendLine("work_context_tools: $tl") }
  if($x.files){ [void]$sb.AppendLine("files_written: $($x.files)") }
  [void]$sb.AppendLine("text:$trunc"); [void]$sb.AppendLine($tx); [void]$sb.AppendLine('')
}
$all = $sb.ToString()
[IO.File]::WriteAllText((Join-Path (Get-Location) 'research\coding\packet_all.md'), $all, $u)
"units: " + $units.Count + "; packet chars: " + $all.Length
$units | Group-Object session | %{ $_.Name + ': ' + $_.Count }
