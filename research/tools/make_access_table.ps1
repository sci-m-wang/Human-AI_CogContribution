$ErrorActionPreference='Stop'
Set-Location '<project>'
$rows = foreach($f in Get-ChildItem research\fulltext\*.md | Sort-Object Name){
  $txt = [IO.File]::ReadAllText($f.FullName,[Text.Encoding]::UTF8)
  $m = [regex]::Match($txt,'ACCESS:\s*([A-Z_]+)')
  [pscustomobject]@{ src_id=$f.BaseName; access=$(if($m.Success){$m.Groups[1].Value}else{'UNPARSED'}); note_file=("research/fulltext/"+$f.Name); bytes=$f.Length }
}
$rows | Export-Csv research\source_access_status.csv -NoTypeInformation -Encoding UTF8
$rows | Group-Object access | %{ $_.Name + ' : ' + $_.Count + '  (' + (($_.Group|%{$_.src_id}) -join ',') + ')' }
