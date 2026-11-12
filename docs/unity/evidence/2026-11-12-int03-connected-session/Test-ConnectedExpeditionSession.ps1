param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ResultsRoot,
    [ValidateRange(0,120)][int]$Samples = 30
)

$ErrorActionPreference = 'Stop'
$timer = [Diagnostics.Stopwatch]::StartNew()
foreach ($name in 'Core', 'Persistence', 'LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$assemblyLoadMs = $timer.Elapsed.TotalMilliseconds
$timer.Restart()
$first = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$firstView = $first.View('Player')
$coldStartMs = $timer.Elapsed.TotalMilliseconds

New-Item -ItemType Directory -Path $ResultsRoot -Force | Out-Null
$ResultsRoot = (Resolve-Path -LiteralPath $ResultsRoot).Path
$store = [Decennium.Foundation.FileSaveStore]::new()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$referencePath = Join-Path $PSScriptRoot '../2026-11-12-tac10-later-defender-controller/focused/saves/tac10-continued.ddsave'
$profilePath = Join-Path $PSScriptRoot '../2026-11-12-mgt04-connected-recipe4-batch/focused/saves/mgt04-connected-batch-continued.ddsave'

function Assert-Session([bool]$test, [string]$message) {
    if (-not $test) { throw $message }
}

function Get-Sha256([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$inputs = @(foreach ($receipt in $store.Load($referencePath).Receipts) {
    $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
    $seat = if ($command.Actor -eq 'TEST_ONLY.third-combatant') { 'FirstOpponent' } else { 'Player' }
    $operation = if ($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { 'auto' } else {
        switch ($command.Kind) {
            'AdvanceClock' { 'clock' }
            'EndFixedEncounter' { 'close' }
            default { 'submit' }
        }
    }
    [pscustomobject]@{Command=$command; Seat=$seat; Operation=$operation; Revision=$receipt.Revision}
})

function ConvertTo-ConsoleInput($inputRow) {
    if ($inputRow.Operation -eq 'auto') { return @{op='auto'} }
    $command = $inputRow.Command
    $row = [ordered]@{op=$inputRow.Operation; id=$command.Id; revision=$command.ExpectedRevision}
    if ($inputRow.Operation -eq 'submit') {
        $row.seat = $inputRow.Seat
        $row.actor = $command.Actor
        $row.kind = $command.Kind.ToString()
    }
    if ($command.Target -ne '') { $row.target = $command.Target }
    if ($command.X -ne 0) { $row.x = $command.X }
    if ($command.Y -ne 0) { $row.y = $command.Y }
    if ($null -ne $command.Inventory) {
        $row.inventory = @{numerator=$command.Inventory.Amount.Numerator; denominator=$command.Inventory.Amount.Denominator;
            destination=$command.Inventory.Destination; handling=$command.Inventory.Handling.ToString()}
    }
    if ($null -ne $command.Combat) {
        $row.combat = @{turn=$command.Combat.TurnId; weapon=$command.Combat.WeaponId; stance=$command.Combat.Stance;
            choice=$command.Combat.Choice; knockout=$command.Combat.Knockout.ToString(); press=$command.Combat.PressInstruction.ToString()}
    }
    if ($null -ne $command.MiningSelection) {
        $selection = $command.MiningSelection
        $row.mining = @{version=$selection.DepositVersionId; categories=$selection.CategoryIds;
            ability=$selection.Ability.ToString(); hurried=$selection.Hurried; failureVictim=$selection.FailureVictimPreference;
            criticalRecovery=$selection.CriticalRecoveryPreference; assistant=$selection.AssistantId}
    }
    $row
}

function Invoke-PublicInput($session, $row) {
    switch ($row.Operation) {
        'auto' { $session.AdvanceAutomaticDefender() }
        'submit' { $session.Submit($row.Seat, $row.Command) }
        default { $session.SubmitSessionCommand($row.Command) }
    }
}

$consolePath = Join-Path $ResultsRoot 'walkthrough.jsonl'
$consoleRows = foreach ($row in $inputs) {
    ConvertTo-ConsoleInput $row | ConvertTo-Json -Depth 5 -Compress
    if ($row.Revision -eq 106) { '{"op":"view","seat":"Player"}' }
    if ($row.Revision -eq 113) {
        '{"op":"view","seat":"Player"}'
        '{"op":"view","seat":"FirstOpponent"}'
        '{"op":"save","path":"pending.ddsave"}'
        '{"op":"load","path":"pending.ddsave"}'
    }
}
$consoleRows | Set-Content -LiteralPath $consolePath -Encoding utf8
Assert-Session ($firstView.Revision -eq 0 -and $firstView.TestOnly -and -not $firstView.InEncounter) 'Startup is not the fresh TEST_ONLY scenario.'
$startPath = Join-Path $ResultsRoot 'initial.ddsave'
$first.Save($startPath)
$fingerprint = $store.Load($startPath).ContentFingerprint
Assert-Session ($fingerprint -ceq $store.Load($profilePath).ContentFingerprint) 'Selected profile differs from the accepted ordinary recipe-4 profile.'

$checkpoints = @(5, 15, 16, 28, 30, 66, 84, 91, 93, 97, 104, 105, 106, 107, 110, 113, 114, 115, 163, 165)
$named = @{
    1='Opening step'; 10='First encounter attack'; 50='Mid-expedition clock advance'; 105='Stabilization milestone'
    114='Off-turn opportunity'; 117='Defender stance'; 118='Defender tactical step'; 165='Ordinary continuation'
}
$timings = [Collections.Generic.List[object]]::new()
$timeline = [Collections.Generic.List[object]]::new()
$paths = @{}
$warmStarts = [Collections.Generic.List[double]]::new()
for ($iteration = 0; $iteration -le $Samples; $iteration++) {
    if ($iteration -eq 0) {
        $session = $first
    } else {
        $timer.Restart()
        $session = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
        $null = $session.View('Player')
        $warmStarts.Add($timer.Elapsed.TotalMilliseconds)
    }
    foreach ($row in $inputs) {
        $timer.Restart()
        $response = Invoke-PublicInput $session $row
        $view = $session.View($row.Seat)
        $elapsed = $timer.Elapsed.TotalMilliseconds
        Assert-Session ($response.Response -eq 'Committed' -and $response.Revision -eq $row.Revision -and
            $view.Revision -eq $response.Revision -and $view.Clock -eq $response.Clock) (
            "Public input $($row.Revision) $($row.Command.Kind) failed with $($response.Response).")
        if ($iteration -eq 0 -and $row.Revision -eq 106) {
            Assert-Session ($view.NextSeat -eq 'Player' -and $view.PendingDecision -eq 'ManufacturingQuality' -and
                $view.ActingActorId -eq 'TEST_ONLY.companion' -and $view.DecisionId -eq $inputs[106].Command.Target -and
                $session.View('FirstOpponent').DecisionId -eq '') 'Manufacturing quality choice belongs to the companion.'
        }
        if ($iteration -gt 0) {
            $timings.Add([pscustomobject]@{Sample=$iteration; Revision=$row.Revision; Operation=$row.Operation;
                Kind=$row.Command.Kind.ToString(); ElapsedMs=[math]::Round($elapsed, 4)})
        } else {
            $timeline.Add([pscustomobject]@{Revision=$row.Revision; Operation=$row.Operation; Seat=$row.Seat;
                Kind=$row.Command.Kind.ToString(); Clock=$response.Clock.ToString(); Response=$response.Response.ToString();
                NextSeat=$view.NextSeat.ToString(); PendingDecision=$view.PendingDecision.ToString(); OpportunityPending=$view.OpportunityPending;
                HistoricalSaleCopper=$view.HistoricalSaleCopper;
                HeroHp=($view.Actors | Where-Object {$_.Position.Id -eq 'TEST_ONLY.actor'}).Hp})
            if ($row.Revision -in $checkpoints) {
                $path = Join-Path $ResultsRoot "checkpoint-$($row.Revision).ddsave"
                $session.Save($path)
                $paths[[int]$row.Revision] = $path
            }
        }
    }
    if ($iteration -eq 0) {
        $expectedFinalHash = Get-Sha256 $paths[165]
    } else {
        $warmFinal = Join-Path $ResultsRoot 'warm-final.ddsave'
        $session.Save($warmFinal)
        Assert-Session ((Get-Sha256 $warmFinal) -ceq $expectedFinalHash) "Warm run $iteration changed canonical bytes."
    }
}
$timings | Export-Csv -LiteralPath (Join-Path $ResultsRoot 'samples.csv') -NoTypeInformation -Encoding utf8
$timeline | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $ResultsRoot 'timeline.json') -Encoding utf8

$timer.Restart()
$pending = $store.Load($paths[113])
$decodeMs = $timer.Elapsed.TotalMilliseconds
$move = $pending.TacticalMoves | Where-Object Pending
Assert-Session ($move.Reactors[$move.ResponseIndex] -eq 'TEST_ONLY.later-defender' -and $pending.Revision -eq 113) 'Expected a real off-turn interrupt.'
$restored = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$timer.Restart()
$restored.Restore($paths[113])
$restoreMs = $timer.Elapsed.TotalMilliseconds
$playerPending = $restored.View('Player')
$firstPending = $restored.View('FirstOpponent')
Assert-Session ($playerPending.OpportunityPending -and $playerPending.NextSeat -eq 'AutomaticDefender' -and
    $playerPending.OpportunityId -eq '' -and -not $firstPending.OpportunityPending -and
    $firstPending.Work.Count -eq 0) 'The pending response leaked its token or appeared under the wrong seat.'
Assert-Session ($restored.Submit('Player', $inputs[113].Command).Response -eq 'NotAuthorized' -and
    $restored.Submit('FirstOpponent', $inputs[113].Command).Response -eq 'NotAuthorized' -and
    $restored.View('Player').Revision -eq 113) 'A human seat was able to respond as the automatic defender.'
$timer.Restart()
$restoredPath = Join-Path $ResultsRoot 'restored-pending.ddsave'
$restored.Save($restoredPath)
$saveMs = $timer.Elapsed.TotalMilliseconds
Assert-Session ((Get-Sha256 $restoredPath) -ceq (Get-Sha256 $paths[113])) 'Restored interrupt bytes changed.'

$pending.RandomState = $pending.RandomState -bxor 1
$forgedPath = Join-Path $ResultsRoot 'forged-history.ddsave'
[IO.File]::WriteAllBytes($forgedPath, $codec.Encode($pending))
Assert-Session ($store.Load($forgedPath).Revision -eq 113) 'The crafted control must pass file decoding.'
$rejected = $false
try { $restored.Restore($forgedPath) } catch { $rejected = $true }
Assert-Session ($rejected -and $restored.View('Player').Revision -eq 113 -and $restored.View('Player').OpportunityPending) (
    'Full restore failed to reject an encodable false RNG history or replaced the live predecessor.')

$oldSale = $inputs | Where-Object {$_.Command.Kind -eq 'StartHavenSale'} | Select-Object -First 1
Assert-Session ($restored.Submit('Player', $oldSale.Command).Response -eq 'Duplicate' -and
    $restored.View('Player').HistoricalSaleCopper -eq 2) 'Retry after restoration changed the completed payment.'
foreach ($row in $inputs | Where-Object Revision -gt 113) {
    $response = Invoke-PublicInput $restored $row
    Assert-Session ($response.Response -eq 'Committed' -and $response.Revision -eq $row.Revision) 'Restored public continuation failed.'
    if ($paths.ContainsKey([int]$row.Revision)) {
        $path = Join-Path $ResultsRoot "restored-$($row.Revision).ddsave"
        $restored.Save($path)
        Assert-Session ((Get-Sha256 $path) -ceq (Get-Sha256 $paths[[int]$row.Revision])) (
            "Restored continuation diverged at revision $($row.Revision).")
    }
}

$authentic = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$timer.Restart()
$authentic.Restore($profilePath)
$authenticRestoreMs = $timer.Elapsed.TotalMilliseconds
$authenticPath = Join-Path $ResultsRoot 'authentic-predecessor.ddsave'
$authentic.Save($authenticPath)
Assert-Session ((Get-Sha256 $authenticPath) -ceq (Get-Sha256 $profilePath)) 'An authentic ordinary wire95 predecessor changed on restore.'

$final = $store.Load($paths[165])
$work = $final.ManufacturingOrders | Select-Object -Last 1
$atReaction = $store.Load($paths[114])
$atDose = $store.Load($paths[115])
$preHeal = ($atReaction.Lives | Where-Object ActorId -eq 'TEST_ONLY.actor').Hp
$postHeal = ($atDose.Lives | Where-Object ActorId -eq 'TEST_ONLY.actor').Hp
$receipts = @($final.Receipts | Group-Object Principal | Select-Object Name,Count)
Assert-Session ($final.Revision -eq 165 -and $final.WireSchemaVersion -eq 95 -and $final.TestOnly -and -not $final.InventoryCombat -and
    $final.ClosedEncounters.Count -eq 2 -and $final.MiningAttempts.Count -eq 1 -and
    $final.HavenSales.Count -eq 1 -and $final.HavenSales[0].PaymentCopper -eq 2 -and
    $final.HavenMealPurchases.Count -eq 1 -and $null -ne $final.ExpeditionEpisodeClose -and
    $final.CharterAttempt.Outcome -eq 'ReturnedComplete' -and $final.FormulaWork[0].Status -eq 'Success' -and
    $work.Status -eq 'Complete' -and $work.Natural -eq 15 -and $work.Quality -eq 'Exceptional' -and
    $final.AlchemyDoses.Count -eq 6 -and @($final.AlchemyDoses | Where-Object Spent).Count -eq 1 -and
    $postHeal - $preHeal -eq 3 -and
    @($final.Receipts | Where-Object Principal -eq 'TEST_ONLY.session-first-opponent').Count -eq 4 -and
    @($final.Receipts | Where-Object Principal -eq 'TEST_ONLY.tac10-later-defender.v1').Count -eq 24) (
    'Selected gameplay or scoped receipt checkpoints changed.')

function Summarize-Timing($values) {
    $ordered = @($values | Sort-Object)
    if ($ordered.Count -eq 0) { return }
    $middle = [int][math]::Floor($ordered.Count / 2)
    $median = if ($ordered.Count % 2) { $ordered[$middle] } else { ($ordered[$middle - 1] + $ordered[$middle]) / 2 }
    [ordered]@{Count=$ordered.Count; MedianMs=[math]::Round($median, 3);
        P95Ms=[math]::Round($ordered[[int][math]::Ceiling($ordered.Count * 0.95) - 1], 3);
        MaxMs=[math]::Round($ordered[-1], 3)}
}

$distribution = @(foreach ($group in $timings | Group-Object Revision | Sort-Object {[int]$_.Name}) {
    $revision = [int]$group.Name
    $summary = Summarize-Timing $group.Group.ElapsedMs
    $budget = if ($revision -eq 105) { 350 } elseif ($named.ContainsKey($revision)) { 150 } else { $null }
    [ordered]@{Revision=$revision; Workload=$named[$revision]; Kind=$group.Group[0].Kind; BudgetMs=$budget;
        Timing=$summary; MetBudget=if ($null -ne $budget) { $summary.P95Ms -le $budget } else { $null }}
})
$report = [ordered]@{
    Status='PASS'; Measurement='Actual C# session input through scoped response and scoped View, excluding script input construction and JSON presentation.'
    Hardware=(Get-CimInstance Win32_Processor | Select-Object -First 1).Name; Runtime=[Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    PowerShell=$PSVersionTable.PSVersion.ToString()
    Percentile='Nearest rank ceil(0.95*n); one full trace before measurements.'
    WarmSamplesPerInput=$Samples; ProfileFingerprint=$fingerprint; RepeatedFinalSha256=$expectedFinalHash
    RestoredFinalSha256=(Get-Sha256 (Join-Path $ResultsRoot 'restored-165.ddsave')); PendingSha256=(Get-Sha256 $paths[113])
    ReferenceInputsSha256=(Get-Sha256 $referencePath); ConsoleInputsSha256=(Get-Sha256 $consolePath)
    Startup=[ordered]@{AssemblyLoadMs=$assemblyLoadMs; ColdStartWithViewMs=$coldStartMs; WarmStartWithView=(Summarize-Timing $warmStarts)}
    FileOperations=[ordered]@{DecodePendingMs=$decodeMs; FullRestorePendingMs=$restoreMs; SavePendingMs=$saveMs;
        EncodableFalseHistoryRejected=$rejected; AuthenticPredecessorFullRestoreMs=$authenticRestoreMs;
        AuthenticPredecessorSha256=(Get-Sha256 $authenticPath)}
    Gameplay=[ordered]@{FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString(); ClosedEncounters=$final.ClosedEncounters.Count
        MiningStatus=$final.MiningAttempts[0].Status.ToString(); HistoricalSaleCopper=$final.HavenSales[0].PaymentCopper
        CharterOutcome=$final.CharterAttempt.Outcome.ToString(); FormulaStatus=$final.FormulaWork[0].Status.ToString()
        BatchNatural=$work.Natural; BatchQuality=$work.Quality.ToString(); BatchDisposition=$final.ConnectedBatch.Disposition.ToString()
        Doses=$final.AlchemyDoses.Count; HeroHpBefore=$preHeal; HeroHpAfter=$postHeal; Receipts=$receipts}
    Timings=$distribution
}
if (@($distribution | Where-Object { $_.MetBudget -eq $false }).Count -gt 0) { $report.Status = 'TIMING BUDGET MISSED' }
$report | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath (Join-Path $ResultsRoot 'results.json') -Encoding utf8
$report.Gameplay | ConvertTo-Json -Depth 5
$report.Status
