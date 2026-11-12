param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$EvidenceRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference = 'Stop'
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$EvidenceRoot = (Resolve-Path -LiteralPath $EvidenceRoot).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$inputs = Join-Path $Run 'inputs.jsonl'
$raw = Join-Path $Run 'responses.jsonl'
$walkthrough = Join-Path $EvidenceRoot 'walkthrough.jsonl'
Get-Content -LiteralPath $walkthrough | Set-Content -LiteralPath $inputs -Encoding utf8
'{"op":"view"}','{"op":"save","path":"continued.ddsave"}' | Add-Content -LiteralPath $inputs -Encoding utf8
Push-Location -LiteralPath $Run
try {
    $timer = [Diagnostics.Stopwatch]::StartNew()
    & $launcher -AssemblyRoot $AssemblyRoot -InputPath $inputs | Set-Content -LiteralPath $raw -Encoding utf8
    $elapsed = $timer.Elapsed.TotalMilliseconds
} finally {
    Pop-Location
}
$rows = @(Get-Content -LiteralPath $raw | ForEach-Object { ConvertFrom-Json $_ })
$commits = @($rows | Where-Object Response -eq 'Committed')
$views = @($rows | Where-Object TestOnly)
$digest = (Get-FileHash -LiteralPath "$Run/continued.ddsave").Hash.ToLowerInvariant()
$expected = (Get-FileHash -LiteralPath (Join-Path $EvidenceRoot 'checkpoint-165.ddsave')).Hash.ToLowerInvariant()
$pending = (Get-FileHash -LiteralPath "$Run/pending.ddsave").Hash.ToLowerInvariant()
$expectedPending = (Get-FileHash -LiteralPath (Join-Path $EvidenceRoot 'checkpoint-113.ddsave')).Hash.ToLowerInvariant()
if ($commits.Count -ne 165 -or $commits[-1].Revision -ne 165 -or $rows.Count -ne 172 -or
    $views.Count -ne 4 -or $views[0].NextSeat -ne 'Player' -or $views[0].PendingDecision -ne 'ManufacturingQuality' -or
    $views[0].ActingActorId -ne 'TEST_ONLY.companion' -or $views[0].DecisionId -eq '' -or
    $views[1].NextSeat -ne 'AutomaticDefender' -or -not $views[1].OpportunityPending -or
    $views[1].OpportunityId -ne '' -or $views[2].OpportunityPending -or $views[2].Work.Count -ne 0 -or
    $views[-1].InEncounter -or $views[-1].HistoricalSaleCopper -ne 2 -or
    @($rows | Where-Object Response -eq 'Saved').Count -ne 2 -or @($rows | Where-Object Response -eq 'Restored').Count -ne 1 -or
    $digest -cne $expected -or $pending -cne $expectedPending) {
    throw 'Console inputs, filtered responses or canonical continuation differ from the C# session witness.'
}
[ordered]@{
    Status='PASS'; Inputs=$rows.Count; Commits=$commits.Count; FinalRevision=$commits[-1].Revision
    TotalWallMs=$elapsed; Includes='PowerShell JSON input and response, allowed projections, startup and full pending restore.'
    PendingSha256=$pending; FinalSha256=$digest
} | ConvertTo-Json | Set-Content -LiteralPath "$Run/results.json" -Encoding utf8
Get-Content -LiteralPath "$Run/results.json"
