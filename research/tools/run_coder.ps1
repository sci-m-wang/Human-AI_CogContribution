param([string]$Model,[string]$Label,[int]$ChunkSize=18)
$ErrorActionPreference='Continue'
$env:Path = "$env:SystemRoot\System32;$env:SystemRoot;$env:Path"
$u = New-Object Text.UTF8Encoding($false)
$ws = '<project>'
$d = Join-Path $env:TEMP "icis_coders\$Label"
$pk = [IO.File]::ReadAllText((Join-Path $d 'packet_full.md'),$u)
$parts = [regex]::Split($pk,'(?m)^(?=### UNIT )') | ?{$_.Trim()}
$chunks = @(); for($i=0;$i -lt $parts.Count;$i+=$ChunkSize){ $chunks += ,($parts[$i..([Math]::Min($i+$ChunkSize,$parts.Count)-1)] -join '') }
$log = Join-Path $d 'driver.log'
"start $(Get-Date -Format s) units=$($parts.Count) chunks=$($chunks.Count)" | Out-File $log -Encoding utf8
for($c=0;$c -lt $chunks.Count;$c++){
  $n=$c+1; $res = Join-Path $d ("result_{0:D2}.jsonl" -f $n)
  if(Test-Path $res){ continue }
  [IO.File]::WriteAllText((Join-Path $d 'packet.md'),$chunks[$c],$u)
  $task = [IO.File]::ReadAllText((Join-Path $d 'TASK_base.md'),$u).Replace('result.jsonl',("result_{0:D2}.jsonl" -f $n))
  [IO.File]::WriteAllText((Join-Path $d 'TASK.md'),$task,$u)
  for($try=1;$try -le 3;$try++){
    $out = Join-Path $d ("run_{0:D2}_{1}.json" -f $n,$try)
    & opencode run -m $Model --dir $d --auto --format json --title ("coder-$Label-chunk$n") "Read TASK.md and follow it exactly." > $out 2>&1
    $sid = (Select-String -Path $out -Pattern '"sessionID":"(ses_[A-Za-z0-9]+)"' -List | %{ $_.Matches[0].Groups[1].Value })
    if($sid){ Add-Content (Join-Path $ws 'research\coding\coder_sessions.txt') "$Label chunk$n try$try $sid" }
    "chunk $n try $try exists=$(Test-Path $res) sid=$sid $(Get-Date -Format s)" | Out-File $log -Append -Encoding utf8
    if(Test-Path $res){ break }
  }
}
"done $(Get-Date -Format s)" | Out-File $log -Append -Encoding utf8
