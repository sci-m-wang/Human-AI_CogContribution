$ErrorActionPreference='Stop'
Set-Location '<project>'
$u = New-Object Text.UTF8Encoding($false)
$old=Import-Csv research\coding\units_v1_106.csv -Encoding UTF8
$oldIds=@{}; foreach($x in $old){$oldIds[$x.unit_id]=1}
$new=Import-Csv research\coding\units_all.csv -Encoding UTF8
$newUnits=@($new | ?{ -not $oldIds.ContainsKey($_.unit_id) })
$ev = Import-Csv records\logs\events.csv -Encoding UTF8 | ?{ $_.event_id -eq 'E030' }
"v1.1 freeze logged at: " + $ev.timestamp
$fz=[DateTimeOffset]::Parse($ev.timestamp)
$after=@($newUnits | ?{ [DateTimeOffset]::FromUnixTimeMilliseconds([int64]$_.time) -gt $fz })
"new units: "+$newUnits.Count+"; after v1.1 freeze: "+$after.Count
# packet of new units only, same format as packet_all
$all=[IO.File]::ReadAllText((Resolve-Path 'research\coding\packet_all.md'),$u)
$parts=[regex]::Split($all,'(?m)^(?=### UNIT )') | ?{$_.Trim()}
$ids=@{}; foreach($n in $newUnits){$ids[$n.unit_id]=1}
$sel=@($parts | ?{ $_ -match '^### UNIT (\S+)' -and $ids.ContainsKey($Matches[1]) })
"packet parts selected: "+$sel.Count
foreach($m in 'gpt11n','gemini11n'){
  $d=Join-Path $env:TEMP "icis_coders\$m"; New-Item -ItemType Directory -Force -Path $d | Out-Null
  Copy-Item (Join-Path $env:TEMP 'icis_coders\gpt11\codebook.md') (Join-Path $d 'codebook.md') -Force
  Copy-Item (Join-Path $env:TEMP 'icis_coders\gpt11\TASK_base.md') (Join-Path $d 'TASK_base.md') -Force
  [IO.File]::WriteAllText((Join-Path $d 'packet_full.md'),($sel -join ''),$u)
  Remove-Item (Join-Path $d 'result_*.jsonl') -ErrorAction SilentlyContinue
}
$newUnits | Export-Csv research\coding\units_new_40.csv -NoTypeInformation -Encoding UTF8
Start-Process -WindowStyle Hidden -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','research\tools\run_coder.ps1','-Model','github-copilot/gpt-6.1-sol','-Label','gpt11n','-ChunkSize','20'
Start-Process -WindowStyle Hidden -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','research\tools\run_coder.ps1','-Model','github-copilot/gemini-4-argon','-Label','gemini11n','-ChunkSize','20'
'launched'
