$ErrorActionPreference='Stop'
Set-Location '<project>'
$u = New-Object Text.UTF8Encoding($false)
$now = (Get-Date).ToString('yyyy-MM-ddTHH:mm')+'+08:00'
$t = @"
I014,$now,ses_ea32c9901ffe7o77BUt54LtH2Q,,human:<user>,design,unit_clarification,"Human corrects the AI's reading of 'round': a round is ONE model response, not human-message-to-human-message (that would be too long); a sub-agent dispatch counts as a round, possibly several. Human will use GPT and Gemini as the two coders; wants the whole paper written TODAY and the codebook fixed soon; agrees to a dry run","AI had defined round too coarsely (I013 reading); human fixes it. Also sets same-day deadline","AI to redefine unit in framework, run dry run on existing exports, then finalize codebook v1.0 draft",research/rounds_dryrun.csv
"@
[IO.File]::AppendAllText((Resolve-Path 'records\logs\interventions.csv'), $t.Trim()+"`r`n", $u)
$e = "E023,$now,ses_ea32c9901ffe7o77BUt54LtH2Q,,openwork/claude-sonnet-5.5,design,ai_misreading,""AI interpreted human 'one round' (I013) as human-message-to-human-message and warned of only ~6 rounds; human meant one model response. Misreading cost a wrong small-N warning in the previous turn"",""human feedback I014"",""Unit redefined; N estimate recomputed from data"",resolved"
[IO.File]::AppendAllText((Resolve-Path 'records\logs\events.csv'), $e+"`r`n", $u)

# dry run: one row per assistant message (response)
$ids = (Import-Csv records\session_registry.csv -Encoding UTF8)
$out = New-Object System.Collections.Generic.List[object]
foreach($s in $ids){
  $j = [IO.File]::ReadAllText((Join-Path 'records' $s.raw_file), $u) | ConvertFrom-Json
  $n=0
  foreach($m in $j.messages){
    if($m.info.role -ne 'assistant'){ continue }
    $n++
    $txt = @($m.parts | ?{$_.type -eq 'text'})
    $tools = @($m.parts | ?{$_.type -eq 'tool'})
    $chars = ($txt | %{ $_.text.Length } | Measure-Object -Sum).Sum
    $toolNames = (($tools | %{ $_.tool }) | Sort-Object -Unique) -join ';'
    $hasTask = [bool]($tools | ?{$_.tool -eq 'task'})
    $out.Add([pscustomobject]@{ session_id=$s.session_id; is_subagent=[bool]$s.parent_session_id; seq=$n; message_id=$m.info.id; text_parts=$txt.Count; text_chars=[int]$chars; tool_calls=$tools.Count; tools=$toolNames; spawns_subagent=$hasTask })
  }
}
$out | Export-Csv research\rounds_dryrun.csv -NoTypeInformation -Encoding UTF8
"total responses: " + $out.Count
$g = $out | Group-Object {$_.is_subagent}
foreach($x in $g){ "subagent=$($x.Name): $($x.Count) responses; with text: " + @($x.Group|?{$_.text_chars -gt 0}).Count + "; tool-only: " + @($x.Group|?{$_.text_chars -eq 0}).Count }
"main session: "; $out | ?{$_.session_id -eq 'ses_ea32c9901ffe7o77BUt54LtH2Q'} | %{ "{0,3} chars={1,5} tools={2,2} {3} {4}" -f $_.seq,$_.text_chars,$_.tool_calls,$_.tools,$_.spawns_subagent }
