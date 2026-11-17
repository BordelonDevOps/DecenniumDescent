param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FinalSource,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
. (Join-Path $PSScriptRoot 'Ferry-TypedCommand.ps1')
. (Join-Path $PSScriptRoot 'Ferry-TraceCommand.ps1')
if(Test-Path -LiteralPath $Output){throw 'Use a fresh export directory.'}
$Output=(New-Item -ItemType Directory -Path $Output).FullName
$FinalSource=(Resolve-Path -LiteralPath $FinalSource).Path
$final=[Decennium.Foundation.FileSaveStore]::new().Load($FinalSource)
if($final.WireSchemaVersion-ne114-or$final.Revision-ne463-or$final.InventoryCombat-or!($final.Lives|Where-Object ActorId -eq 'TEST_ONLY.ferry-wraith').Dead){throw 'Expected the genuine completed Dash/Ferry lineage.'}
$revisions=[Collections.Generic.SortedSet[long]]::new()
foreach($value in 0,345,346,351,354,357,359,366,437,438,463){$null=$revisions.Add($value)}
$all=@($final.Receipts|ForEach-Object {[ordered]@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
foreach($row in $all){if($row.command.Kind-in'EndFixedEncounter','CastKnownSpell','StartMining','StartManufacturing','CloseExpeditionEpisode','AcceptNextCharter','AdvanceCharacterLevel'){$null=$revisions.Add($row.receipt.Revision)}}
$requests=[Collections.Generic.List[object]]::new()
function Add-Mark([long]$revision){if($revisions.Contains($revision)){$requests.Add(@{op='save';path=('ferry-r'+$revision.ToString('D3')+'.ddsave')})}}
Add-Mark 0
foreach($receipt in $final.Receipts){$requests.Add((ConvertTo-FerryRequest $receipt));Add-Mark $receipt.Revision}
$requests|ForEach-Object {ConvertTo-Json -InputObject $_ -Depth 12 -Compress}|Set-Content -LiteralPath (Join-Path $Output 'inputs.jsonl') -Encoding utf8
$all|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Output 'all-command-receipts.json') -Encoding utf8
[ordered]@{scope='Exact requests exported from genuine completed receipts; no new gameplay execution or causal restore claimed';source=$FinalSource;sourceSha256=(Get-FileHash -LiteralPath $FinalSource).Hash.ToLowerInvariant();revision=$final.Revision;selectedRevisions=@($revisions)}|
    ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Output 'source.json') -Encoding utf8
foreach($path in $PSCommandPath,(Join-Path $PSScriptRoot 'Ferry-TypedCommand.ps1'),(Join-Path $PSScriptRoot 'Ferry-TraceCommand.ps1')){Copy-Item -LiteralPath $path -Destination (Join-Path $Output ([IO.Path]::GetFileName($path)))}
Write-Output "Exported $($final.Revision) requests and $($revisions.Count) selected checkpoint revisions."
