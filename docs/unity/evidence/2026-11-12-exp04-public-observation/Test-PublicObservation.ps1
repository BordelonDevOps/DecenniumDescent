param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$base = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-12-int03-connected-session/correction')).Path
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$console = Join-Path $Run 'console'
New-Item -ItemType Directory -Path $console | Out-Null
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$hero = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$companion = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
$session = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$store = [Decennium.Foundation.FileSaveStore]::new()
$reference = $store.Load((Join-Path $base 'connected/saves/checkpoint-165.ddsave'))
$prefix = @($reference.Receipts | Select-Object -First 108)
$inputs = [Collections.Generic.List[string]]::new()
$trace = [Collections.Generic.List[object]]::new()
$timer = [Diagnostics.Stopwatch]::new()
$number = 0

function Require-Observation([bool]$condition,[string]$message) {
    if (-not $condition) { throw $message }
}
function Add-Input($row) {
    $inputs.Add((ConvertTo-Json -InputObject $row -Compress -Depth 6))
}
function Read-View([string]$seat = 'Player') {
    Add-Input @{op='view';seat=$seat}
    $session.View($seat)
}
function Invoke-Entry($targetSession,$entry) {
    switch ($entry.Op) {
        'clock' { $targetSession.SubmitSessionCommand($entry.Command) }
        'close' { $targetSession.SubmitSessionCommand($entry.Command) }
        'auto' { $targetSession.AdvanceAutomaticDefender() }
        default { $targetSession.Submit($entry.Seat,$entry.Command) }
    }
}
function Run-Prefix($targetSession) {
    foreach ($receipt in $prefix) {
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $result = switch ($receipt.Principal) {
            'TEST_ONLY.session-operator' { $targetSession.SubmitSessionCommand($command) }
            'TEST_ONLY.session-first-opponent' { $targetSession.Submit('FirstOpponent',$command) }
            default { $targetSession.Submit('Player',$command) }
        }
        Require-Observation ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) 'Accepted input prefix changed.'
    }
}
function New-Input([string]$kind,[string]$actor = $hero,[string]$target = '',[int]$x = 0,[int]$y = 0,
    $combat = $null,$inventory = $null) {
    $script:number++
    [Decennium.Foundation.Command]::new("exp04.public.$number",$actor,$session.View('Player').Revision,
        $kind,$target,$x,$y,$inventory,$combat)
}
function Send-Input($command,[string]$expected = 'Committed',[string]$seat = 'Player') {
    $op = if ($null -eq $command) { 'auto' } else {
        switch ($command.Kind) {
            'AdvanceClock' { 'clock' }
            'EndFixedEncounter' { 'close' }
            default { 'submit' }
        }
    }
    $entry = [pscustomobject]@{Op=$op;Seat=$seat;Command=$command;Expected=$expected}
    $row = [ordered]@{op=$op}
    if ($command) {
        $row.id=$command.Id; $row.revision=$command.ExpectedRevision; $row.x=$command.X; $row.y=$command.Y
        $row.target=$command.Target
        if ($op -eq 'submit') {
            $row.seat=$seat; $row.actor=$command.Actor; $row.kind=$command.Kind.ToString()
        }
        if ($command.Combat) {
            $row.combat=@{turn=$command.Combat.TurnId; weapon=$command.Combat.WeaponId; stance=$command.Combat.Stance;
                choice=$command.Combat.Choice; knockout=$command.Combat.Knockout.ToString(); press=$command.Combat.PressInstruction.ToString()}
        }
        if ($command.Inventory) {
            $row.inventory=@{numerator=$command.Inventory.Amount.Numerator; denominator=$command.Inventory.Amount.Denominator;
                destination=$command.Inventory.Destination; handling=$command.Inventory.Handling.ToString()}
        }
    }
    Add-Input $row
    $timer.Restart()
    $result = Invoke-Entry $session $entry
    $view = $session.View($seat)
    $ms = $timer.Elapsed.TotalMilliseconds
    Require-Observation ($result.Response -eq $expected) (
        "Revision $($view.Revision), $($command.Kind) $op expected $expected, got $($result.Response).")
    $entry | Add-Member -NotePropertyName Revision -NotePropertyValue $result.Revision
    $entry | Add-Member -NotePropertyName Clock -NotePropertyValue $result.Clock.ToString()
    $entry | Add-Member -NotePropertyName Milliseconds -NotePropertyValue ([math]::Round($ms,3))
    $trace.Add($entry)
}
function Advance-Ordinary([int]$seconds) { Send-Input (New-Input AdvanceClock -x $seconds -y 1) }
function Walk-Ordinary([int]$x,[int]$y,[string]$actor = $hero) {
    Send-Input (New-Input BeginWorldStep $actor walk $x $y)
    Advance-Ordinary 6
}
function Save-Observation([string]$name) {
    Add-Input @{op='save';path=$name}
    $session.Save((Join-Path $Run $name))
}
function Restore-Observation([string]$name) {
    Add-Input @{op='load';path=$name}
    $session.Restore((Join-Path $Run $name))
}
function Save-Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }

Run-Prefix $session
foreach ($line in (Get-Content -LiteralPath (Join-Path $base 'walkthrough.jsonl') -TotalCount 109)) { $inputs.Add($line) }
Walk-Ordinary 0 -1 $companion
for ($step=0; $step -lt 3; $step++) { Walk-Ordinary 0 -1 }
$view = Read-View
for ($wait=0; $wait -lt 6 -and -not $view.Observation.HideStartId; $wait++) {
    Advance-Ordinary 1
    $view = Read-View
}
Require-Observation ($view.Observation.OrdinaryStageOpen -and $view.Observation.HideStartId -and $view.Observation.SearchStartId) (
    'Public inputs must reach the actual legal observation window.')
Save-Observation 'observation-start.ddsave'
$hide = New-Input Hide $hero $view.Observation.HideStartId
Send-Input (New-Input Hide $companion $view.Observation.HideStartId) Unavailable
Send-Input $hide NotAuthorized FirstOpponent
Send-Input $hide
$view = Read-View
$pending = $view.Observation.HideAttempts[-1]
Require-Observation ($pending.Status -eq 'Pending' -and -not $view.Observation.HideStartId -and $view.Observation.SearchStartId) (
    'The paid Hide uses only the hero action.')
$cancelHide = New-Input CancelExplorationHide $hero $pending.AttemptId
Send-Input (New-Input CancelExplorationHide $companion $pending.AttemptId) Unavailable
Send-Input $cancelHide
Send-Input $cancelHide Duplicate
$view = Read-View
Require-Observation ($view.Observation.HideAttempts[-1].Status -eq 'Cancelled' -and -not $view.Observation.HideStartId) (
    'Cancellation preserves the paid hero interval.')
$cancelledSearch = New-Input Search $companion $view.Observation.SearchStartId 0 0
Send-Input $cancelledSearch
Advance-Ordinary 2
$view = Read-View
$pending = $view.Observation.SearchAttempts[-1]
Send-Input (New-Input CancelExplorationSearch $companion $pending.AttemptId)
Save-Observation 'paid-cancellations.ddsave'
Advance-Ordinary 4
$view = Read-View
Send-Input (New-Input Hide $hero $view.Observation.HideStartId)
Advance-Ordinary 6
Walk-Ordinary 1 0
$view = Read-View
Send-Input (New-Input Hide $hero $view.Observation.HideStartId)
Advance-Ordinary 6
Walk-Ordinary -1 0
$view = Read-View
$search = New-Input Search $companion $view.Observation.SearchStartId 1 0
Send-Input $search
Advance-Ordinary 2
$working = Read-View
Require-Observation ($working.Observation.SearchAttempts[-1].Status -eq 'Pending' -and
    $working.Observation.SearchAttempts[-1].DueAt -eq $working.Clock.AddSeconds(4)) 'Search must retain its actual remaining interval.'
Require-Observation ($null -eq (Read-View FirstOpponent).Observation) 'The opponent must have no party investigation projection.'
Save-Observation 'pending-search.ddsave'
Restore-Observation 'pending-search.ddsave'
$restored = Read-View
Require-Observation ($restored.Observation.SearchAttempts[-1].AttemptId -eq $working.Observation.SearchAttempts[-1].AttemptId) (
    'Validated restore must preserve the actual pending Search.')
Send-Input $search Duplicate
Advance-Ordinary 4
$settled = Read-View
Require-Observation ($settled.Observation.SearchAttempts[-1].Status -eq 'NoFinding' -and
    $null -eq $settled.Observation.SearchAttempts[-1].FoundLocation -and
    -not ($settled.Observation.HiderKnowledge | Where-Object Evidence -eq 'Search')) (
    'Public Search reports the actual generic no-finding without sharing knowledge.')
Save-Observation 'completed-search.ddsave'

for ($step=0; $step -lt 3; $step++) { Walk-Ordinary 0 1 }
Send-Input (New-Input BeginWorldStep $hero walk -1)
Advance-Ordinary 12
$entry = Read-View
Require-Observation ($entry.InEncounter -and -not $entry.Observation.OrdinaryStageOpen -and
    $null -eq $entry.Observation.SearchStartId -and $null -eq $entry.Observation.HideStartId) (
    'Genuine later entry closes ordinary observation.')
Send-Input (New-Input Search $companion $settled.Observation.SearchStartId 1 0) Unavailable
Save-Observation 'later-entry.ddsave'

$club = 'TEST_ONLY.actor-club'
for ($turn=0; $turn -lt 25; $turn++) {
    $view = $session.View('Player')
    if (-not $view.InEncounter) { break }
    while ($view.NextSeat -eq 'AutomaticDefender') {
        Send-Input $null
        $view = $session.View('Player')
    }
    Require-Observation ($view.ActingActorId -eq $hero -and $view.PendingDecision -eq 'None') 'Expected the hero regular turn.'
    Send-Input (New-Input SelectCombatStance $hero -combat ([Decennium.Foundation.CombatRequest]::new($view.TurnId,'',1)))
    $opponent = ($view.Actors | Where-Object {$_.Position.Id -eq $hero}).VisibleOpponents | Select-Object -First 1
    Require-Observation ($null -ne $opponent) 'Use the actually visible opponent.'
    Send-Input (New-Input AttackClub $hero $opponent.Id -combat (
        [Decennium.Foundation.CombatRequest]::new($view.TurnId,$club,0,'OrdinaryOutcome',$false,'KeepExisting')))
    $result = $session.SubmitSessionCommand((New-Input EndFixedEncounter $hero $view.TurnId))
    if ($result.Response -eq 'Committed') {
        # Record the actual closure for identical replay, without resubmitting it.
        $close = [Decennium.Foundation.Command]::new("exp04.public.$number",$hero,$result.Revision-1,'EndFixedEncounter',$view.TurnId)
        Add-Input @{op='close';id=$close.Id;revision=$close.ExpectedRevision;target=$close.Target}
        $trace.Add([pscustomobject]@{Op='close'; Seat='Player'; Command=$close; Expected='Committed';
            Revision=$result.Revision; Clock=$result.Clock.ToString(); Milliseconds=$null})
        break
    }
    Send-Input (New-Input EndRegularTurn $hero $view.TurnId)
}
$after = Read-View
Require-Observation (-not $after.InEncounter -and -not $after.Observation.OrdinaryStageOpen) 'Later combat must really close.'
Send-Input (New-Input Search $companion $settled.Observation.SearchStartId 1 0) Unavailable
Walk-Ordinary 1 0
Walk-Ordinary 0 -1
$closed = Read-View
Require-Observation ($closed.Cache.Locked -and -not $closed.Cache.Open) 'The original finite cache remains present after the observation route.'
$retrieve = [Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'','Retrieve')
$tools = $closed.Items | Where-Object Id -eq 'TEST_ONLY.thieves-tools'
Send-Input (New-Input HandlePortableEquipment $hero $tools.Id -inventory $retrieve)
for ($pick=0; $pick -lt 8 -and $session.View('Player').Cache.Locked; $pick++) {
    $cache = (Read-View).Cache
    # Each new declaration uses an actual interval. A rejected declaration spends nothing.
    $pickCommand = New-Input Interact $hero $cache.Id 2
    $attempt = $session.Submit('Player',$pickCommand)
    $pickRow = @{op='submit';seat='Player';kind='Interact';actor=$hero;id=$pickCommand.Id;
        revision=$pickCommand.ExpectedRevision;target=$cache.Id;x=2}
    Add-Input $pickRow
    $trace.Add([pscustomobject]@{Op='submit';Seat='Player';Command=$pickCommand;Expected=$attempt.Response.ToString();
        Revision=$attempt.Revision;Clock=$attempt.Clock.ToString();Milliseconds=$null})
    if ($attempt.Response -eq 'Unavailable') { Advance-Ordinary 6; continue }
    Require-Observation ($attempt.Response -eq 'Committed') 'Unexpected pick response.'
    Advance-Ordinary 6
}
$cache = (Read-View).Cache
Require-Observation ($cache -and -not $cache.Locked) 'Real pick attempts must unlock the selected cache.'
Send-Input (New-Input Interact $hero $cache.Id 3)
$stock = (Read-View).Cache
$take = [Decennium.Foundation.InventoryRequest]::new($stock.AvailablePounds)
Save-Observation 'before-cache-pickup.ddsave'
Advance-Ordinary 2
Send-Input (New-Input HandleInventory $hero $stock.StockId -inventory $take)
Walk-Ordinary 0 1
Save-Observation 'depleted-away.ddsave'
Restore-Observation 'depleted-away.ddsave'
Walk-Ordinary 0 -1
$empty = (Read-View).Cache
Require-Observation ($empty.Open -and $empty.StockId -eq '' -and $null -eq $empty.AvailablePounds) (
    'The continued session must revisit the same depleted cache.')
Walk-Ordinary 1 0
Save-Observation 'continued.ddsave'

$replayed = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
Run-Prefix $replayed
foreach ($row in $trace) {
    $result = Invoke-Entry $replayed $row
    Require-Observation ($result.Response -eq $row.Expected -and $result.Revision -eq $row.Revision) 'Same public inputs must replay.'
}
$replayed.Save((Join-Path $Run 'uninterrupted.ddsave'))
$sha = Save-Digest (Join-Path $Run 'continued.ddsave')
Require-Observation ($sha -ceq (Save-Digest (Join-Path $Run 'uninterrupted.ddsave'))) 'C# restored and uninterrupted saves diverged.'

$start = $store.Load((Join-Path $Run 'observation-start.ddsave'))
$cancelled = $store.Load((Join-Path $Run 'paid-cancellations.ddsave'))
$found = $store.Load((Join-Path $Run 'completed-search.ddsave'))
$later = $store.Load((Join-Path $Run 'later-entry.ddsave'))
Require-Observation ($cancelled.RandomState -eq $start.RandomState -and $cancelled.ObservationActions.Length -eq 0 -and
    $cancelled.WorldIntervals[0].ActionSpent -and ($cancelled.WorldActivityIntervals | Where-Object ActorId -eq $companion).Action -eq 'Search') (
    'Both cancellations preserve their payments and consume no draw.')
Require-Observation ($found.ExplorationSearch.Attempts[-1].End.ObservationId -and
    -not ($found.ObserverKnowledge | Where-Object {$_.Evidence -eq 'Search' -and $_.ObserverId -ne $companion}) -and
    $later.LaterEncounter.Entry.Draws[0].RandomBefore -eq $found.RandomState -and $later.SurpriseEntry.Binding.Outcome -eq 'Warned') (
    'Observer-specific knowledge and later initiative must come from actual state and RNG.')

$walk = Join-Path $Run 'walkthrough.jsonl'
$inputs | Set-Content -LiteralPath $walk -Encoding utf8
Push-Location -LiteralPath $console
try {
    & $launcher -AssemblyRoot $AssemblyRoot -InputPath $walk | Set-Content -LiteralPath 'responses.jsonl' -Encoding utf8
} finally { Pop-Location }
$rows = @(Get-Content -LiteralPath (Join-Path $console 'responses.jsonl') | ForEach-Object { ConvertFrom-Json $_ })
Require-Observation ($rows.Count -eq $inputs.Count -and
    $sha -ceq (Save-Digest (Join-Path $console 'continued.ddsave')) -and
    (Save-Digest (Join-Path $Run 'pending-search.ddsave')) -ceq (Save-Digest (Join-Path $console 'pending-search.ddsave'))) (
    'Console inputs must reproduce the exact pending and final saves.')
$trace | Select-Object Op,Seat,@{n='Kind';e={if ($_.Command) {$_.Command.Kind.ToString()} else {'AutomaticDefender'}}},Expected,Revision,Clock,Milliseconds |
    ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Run 'timeline.json') -Encoding utf8
[ordered]@{Status='PASS'; Inputs=$inputs.Count; FinalSha256=$sha; FinalRevision=$session.View('Player').Revision;
    PendingSha256=(Save-Digest (Join-Path $Run 'pending-search.ddsave')); Search='NoFinding';
    HideRolls=@($found.ObservationActions | Where-Object Outcome -eq 'HideAttempted' | ForEach-Object Natural);
    LaterInitiative=$later.LaterEncounter.Entry.Epoch.Order} |
    ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Get-Content -LiteralPath (Join-Path $Run 'results.json')
