$ErrorActionPreference='Stop'
$env:Path = "$env:SystemRoot\System32;$env:SystemRoot;$env:Path"
$ws='<project>'
Set-Location $ws
$tmp = Join-Path $env:TEMP 'icis_coders'
$cb = Join-Path $tmp 'gpt11\codebook.md'; $tk = Join-Path $tmp 'gpt11\TASK_base.md'
"codebook sha256 gpt11   : " + (Get-FileHash $cb -Algorithm SHA256).Hash
"codebook sha256 gemini11: " + (Get-FileHash (Join-Path $tmp 'gemini11\codebook.md') -Algorithm SHA256).Hash
"TASK_base sha256 gpt11  : " + (Get-FileHash $tk -Algorithm SHA256).Hash
"TASK_base sha256 gemini11: " + (Get-FileHash (Join-Path $tmp 'gemini11\TASK_base.md') -Algorithm SHA256).Hash
$jobs = @(@('gpt12a','github-copilot/gpt-6.1-sol','research\coding\packet_ext_a.md'), @('gpt12b','github-copilot/gpt-6.1-sol','research\coding\packet_ext_b.md'),
          @('gemini12a','github-copilot/gemini-4-argon','research\coding\packet_ext_a.md'), @('gemini12b','github-copilot/gemini-4-argon','research\coding\packet_ext_b.md'))
foreach($j in $jobs){
  $d = Join-Path $tmp $j[0]; New-Item -ItemType Directory -Force -Path $d | Out-Null
  Copy-Item $cb (Join-Path $d 'codebook.md') -Force; Copy-Item $tk (Join-Path $d 'TASK_base.md') -Force
  Copy-Item (Join-Path $ws $j[2]) (Join-Path $d 'packet_full.md') -Force
  Remove-Item (Join-Path $d 'result_*.jsonl') -ErrorAction SilentlyContinue
  Start-Process -WindowStyle Hidden -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','research\tools\run_coder.ps1','-Model',$j[1],'-Label',$j[0],'-ChunkSize','20'
  "launched " + $j[0] + " " + $j[1] + " at " + (Get-Date -Format s)
}
