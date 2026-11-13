param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run = (Resolve-Path -LiteralPath $Run).Path
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
function Require-Travel([bool]$test,[string]$message) {
    if (-not $test) { throw $message }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$inputs = @(Get-Content "$Run/walkthrough.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
$rows = @(Get-Content "$Run/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
$companion = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
$store = [Decennium.Foundation.FileSaveStore]::new()
$s = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$pending = "$Run/partial-edge.ddsave"
$timer = [Diagnostics.Stopwatch]::StartNew()
$s.Restore($pending)
$restoreMs = $timer.Elapsed.TotalMilliseconds
$v = $s.View('Player')
$edge = ($v.Actors | Where-Object {$_.Position.Id -eq $companion}).Traversal
$partial = $store.Load($pending)
$ordinary = $partial.WorldActivityIntervals | Where-Object ActorId -eq $companion
$savedEdge = $partial.WorldTraversals | Where-Object ActorId -eq $companion
Require-Travel ($edge.ExactX.Numerator -gt 0 -and $edge.ExactX.Denominator -gt 1 -and
    $edge.DistanceFeet -eq $savedEdge.DistanceFeet -and $edge.MovementSpent -eq $ordinary.MovementSpent -and
    $edge.IntervalIndex -eq $ordinary.IntervalIndex -and -not $edge.PersonalStart -and
    $v.MiningSite.ClaimClosed -eq $null -and $v.MiningSite.Units.Count -eq 0) 'Restored edge and allowance must come from existing state.'
$arrived = $store.Load("$Run/arrived.ddsave")
$final = $store.Load("$Run/travel-continued.ddsave")
$attempt = $final.MiningAttempts | Where-Object DepositId -eq 'TEST_ONLY.mining.deposit'
$iron = $final.MiningUnits | Where-Object Id -eq 'TEST_ONLY.mining.unit.iron'
$copper = $final.MiningUnits | Where-Object Id -eq 'TEST_ONLY.mining.unit.copper'
$sales = @($final.HavenSales | Where-Object {$_.Basis.GoodsLotId -eq $iron.ReceivedLotId})
Require-Travel ($arrived.WorldTraversals.Count -eq 0 -and
    ($arrived.Actors | Where-Object Id -eq $companion).X -eq 3 -and $arrived.MiningAttempts.Count -eq 0 -and
    @($attempt).Count -eq 1 -and $attempt.Status -eq 'Success' -and $attempt.WorkDone.Numerator -gt 0 -and
    $iron.Status -eq 'Extracted' -and $copper.Status -eq 'Forfeited' -and
    $iron.ReceivedLotId -eq 'TEST_ONLY.mining.unit.iron' -and $sales.Count -eq 1 -and $sales[0].PaymentCopper -eq 2) (
    'Actual arrival, work, recovery and later disposition must all survive.')
Require-Travel ($rows.Count -eq $inputs.Count -and @($rows | Where-Object Response -eq 'Committed').Count -eq $final.Revision -and
    @($rows | Where-Object {$_.Response -in 'StaleRevision','CommandIdConflict'}).Count -eq 0) 'Every planned command must reach the expected revision.'
$direct = Join-Path $Run 'csharp'
New-Item -ItemType Directory -Force -Path $direct | Out-Null
$directSession = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$receipts = @{}
foreach ($receipt in $final.Receipts) { $receipts[$receipt.Revision] = $receipt }
$times = @()
for ($i=0; $i -lt $inputs.Count; $i++) {
    $inputRow = $inputs[$i]
    $outputRow = $rows[$i]
    if ($inputRow.id -eq 'exp05.repeat-mining') {
        $revisit = $rows[$i - 1].MiningSite
        Require-Travel ($outputRow.Response -eq 'Unavailable' -and $outputRow.Revision -eq $inputRow.revision -and
            $revisit.ObservedLocally -and $revisit.ClaimClosed -and
            ($revisit.Units | Where-Object Id -eq $iron.Id).Status -eq 'Extracted' -and
            ($revisit.Units | Where-Object Id -eq $copper.Id).Status -eq 'Forfeited') 'The physical revisit and repeat denial differ.'
    }
    if ($outputRow.Response -eq 'Committed') {
        $receipt = $receipts[$outputRow.Revision]
        Require-Travel ($null -ne $receipt -and ($inputRow.op -eq 'auto' -or $receipt.Id -ceq $inputRow.id)) 'Console action and canonical receipt differ.'
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $watch = [Diagnostics.Stopwatch]::StartNew()
        $result = switch ($inputRow.op) {
            'auto' { $directSession.AdvanceAutomaticDefender() }
            'submit' { $directSession.Submit(($inputRow.seat ?? 'Player'), $command) }
            'clock' { $directSession.SubmitSessionCommand($command) }
            'close' { $directSession.SubmitSessionCommand($command) }
            default { throw "Unknown committed input $($inputRow.op)." }
        }
        Require-Travel ($result.Response -eq 'Committed' -and $result.Revision -eq $outputRow.Revision) "Public C# replay diverged at $($outputRow.Revision)."
        if ($inputRow.id -like 'exp05.*') {
            $null = $directSession.View('Player')
            $times += [ordered]@{Id=$inputRow.id; Revision=$result.Revision; SubmitAndViewMs=$watch.Elapsed.TotalMilliseconds}
        }
    }
    if ($inputRow.op -eq 'save' -and $inputRow.path -in 'partial-edge.ddsave','travel-continued.ddsave') {
        $directSession.Save((Join-Path $direct $inputRow.path))
    }
}
$replay = Join-Path $Run 'replay'
New-Item -ItemType Directory -Force -Path $replay | Out-Null
$replayInputs = Join-Path $replay 'walkthrough.jsonl'
Get-Content "$Run/walkthrough.jsonl" | Where-Object { ($_ | ConvertFrom-Json).op -ne 'load' } |
    Set-Content -LiteralPath $replayInputs -Encoding utf8
Push-Location -LiteralPath $replay
try {
    & $launcher -AssemblyRoot $AssemblyRoot -InputPath $replayInputs | Set-Content 'responses.jsonl' -Encoding utf8
} finally { Pop-Location }
$finalSha = Digest "$Run/travel-continued.ddsave"
Require-Travel ($finalSha -ceq (Digest "$replay/travel-continued.ddsave") -and
    (Digest $pending) -ceq (Digest "$replay/partial-edge.ddsave") -and
    $finalSha -ceq (Digest "$direct/travel-continued.ddsave") -and
    (Digest $pending) -ceq (Digest "$direct/partial-edge.ddsave")) 'Console and public C# replay must match canonical saves.'
$previous = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-12-exp04-public-observation/connected/continued.ddsave')).Path
$s.Restore($previous)
$s.Save("$Run/authentic-observation.ddsave")
Require-Travel ((Digest $previous) -ceq (Digest "$Run/authentic-observation.ddsave")) 'Authentic observation save changed.'
[ordered]@{
    Status='PASS'; FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()
    FinalSha256=$finalSha; PendingSha256=(Digest $pending)
    AuthenticSha256=(Digest $previous); FullPartialRestoreMs=$restoreMs
    Partial=[ordered]@{Revision=$partial.Revision; ExactX=$edge.ExactX.ToString(); ExactY=$edge.ExactY.ToString()
        DistanceFeet=$edge.DistanceFeet.ToString(); EdgeFeetRemaining=$edge.EdgeFeetRemaining.ToString()
        SpentFeet=$edge.MovementSpent.ToString(); RemainingFeet=$edge.MovementRemaining.ToString()
        Calendar=$edge.CalendarId; Interval=$edge.IntervalIndex; PersonalStart=$edge.PersonalStart}
    Mining=[ordered]@{Worker=$attempt.WorkerId; Attempt=$attempt.Id; Status=$attempt.Status.ToString()
        Labor=$attempt.WorkDone.ToString(); Natural=$attempt.Natural; Modifier=$attempt.CheckModifier
        IronStatus=$iron.Status.ToString(); ReceivedLot=$iron.ReceivedLotId; CopperStatus=$copper.Status.ToString()
        SaleCopper=$sales[0].PaymentCopper}
    Inputs=$rows.Count; CSharpCommittedActions=$receipts.Count; PublicTimings=$times
} | ConvertTo-Json -Depth 8 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
