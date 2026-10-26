param([string]$Docx, [string]$Pdf)
$progs = 'KWPS.Application','WPS.Application','Wps.Application'
$app = $null
foreach ($p in $progs) { try { $app = New-Object -ComObject $p; "using $p"; break } catch { "no $p : $($_.Exception.Message.Substring(0,[Math]::Min(80,$_.Exception.Message.Length)))" } }
if (-not $app) { 'WPS COM not available'; exit 2 }
try {
  $app.Visible = $false
  $d = $app.Documents.Open($Docx, $false, $true)
  "pages (WPS) = " + $d.ComputeStatistics(2)
  try { $d.ExportAsFixedFormat($Pdf, 17); "exported" } catch { "export failed: " + $_.Exception.Message; try { $d.SaveAs2($Pdf, 17); "saved as pdf via SaveAs2" } catch { "SaveAs2 failed: " + $_.Exception.Message } }
  $d.Close($false)
} finally { $app.Quit() }
