param([string]$Docx,[string]$Pdf)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
  $d = $w.Documents.Open($Docx, $false, $true)
  $d.ExportAsFixedFormat($Pdf, 17)
  $d.Close($false)
} finally { $w.Quit() }
"exported"
