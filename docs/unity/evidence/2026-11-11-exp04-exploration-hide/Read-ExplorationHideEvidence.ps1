param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{name=Split-Path -Leaf $path;sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
})
$test = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$hero = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId
$searcher = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$witness = [Decennium.Foundation.ExplorationHideDefinition]::Witness
$hostAuthority = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::Host()
function Hash([byte[]]$Data) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant() }
function Stamp([int]$Seconds) {
    [Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new($Seconds,1),0)
}
function Read-Save([string]$Name,[uint32]$Seed=2,[Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]$Events=@()) {
    $path = Join-Path $Saves "exp04-hide-$Name.ddsave"
    $policy = $test.GetMethod('ExplorationHidePolicy',$flags).Invoke($null,@($Seed,$false,5,$Events))
    $raw = [IO.File]::ReadAllBytes($path)
    $sim = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $s = $sim.Capture()
    if ((Hash ($codec.Encode($s))) -cne (Hash $raw)) { throw "Roundtrip changed $Name" }
    $ledger = $s.WorldIntervals | Where-Object ActorId -CEQ $hero
    $hide = @($s.ExplorationHide.Attempts | ForEach-Object {
        $attempt = $_
        $projection = $sim.ObserveExplorationHide($hostAuthority,$attempt.Id)
        $row = [ordered]@{attempt=$attempt.Id;declarationRevision=$attempt.Revision;declaration=$attempt.CommandId
            paidMarker=$s.WorldSchedule.MarkerId($attempt.PaidStart);anchor=@($attempt.Anchor.X,$attempt.Anchor.Y)
            started=$projection.StartedAt.ToString();due=$projection.DueAt.ToString();status=$projection.Status.ToString()}
        if ($attempt.End) {
            $row.ended = $projection.EndedAt.ToString()
            $row.terminalRevision = $attempt.End.Revision
            $row.terminal = $attempt.End.CommandId
            $row.privateNoRoll = $attempt.End.NoRoll.ToString()
            $row.privateObserverSet = $attempt.End.EligibleObservers.ToString()
            $row.priorFailure = $attempt.End.PriorFailureId
            $row.observation = $attempt.End.ObservationId
        }
        if ($attempt.Relocation) {
            $row.actualRelocation = [ordered]@{startedRevision=$attempt.Relocation.StartedRevision
                at=$attempt.Relocation.At.ToString();arrivedRevision=$attempt.Relocation.ArrivedRevision
                arrival=$attempt.Relocation.ArrivalCommandId;from=@($attempt.Relocation.From.X,$attempt.Relocation.From.Y)
                to=@($attempt.Relocation.To.X,$attempt.Relocation.To.Y)}
        }
        $row
    })
    $search = @($s.ExplorationSearch.Attempts | ForEach-Object {
        [ordered]@{attempt=$_.Id;declarationRevision=$_.Revision;terminalRevision=$_.End.Revision;terminal=$_.End.CommandId
            at=$_.End.At.ToString();hide=$_.End.HideId;observation=$_.End.ObservationId}
    })
    $observations = @($s.ObservationActions | ForEach-Object {
        $action = $_
        [ordered]@{id=$action.Id;kind=$action.Kind.ToString();at=$action.At.ToString();revision=$action.Revision
            outcome=$action.Outcome.ToString();natural=$action.Natural;modifier=$action.Modifier;total=$action.Total
            before=$action.RandomBefore;after=$action.RandomAfter;words=$action.WordsConsumed
            comparisons=@($s.ObservationHideResults | Where-Object AttemptId -CEQ $action.Id | ForEach-Object {
                [ordered]@{observer=$_.ObserverId;dc=$_.Dc;degree=$_.Degree.ToString();hidden=$_.HiddenEstablished}
            })}
    })
    $knowledge = @(foreach ($observer in $searcher,$witness) {
        $row = $s.ObserverKnowledge | Where-Object {$_.ObserverId -ceq $observer -and $_.TargetId -ceq $hero}
        [ordered]@{observer=$observer;hidden=[Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($s,$observer,$hero)
            directSight=[Decennium.Foundation.Laboratory.ObservationRules]::CanSee($s,$observer,$hero)
            currentLocationKnown=[Decennium.Foundation.Laboratory.ObservationRules]::LocationKnown($s,$observer,$hero)
            activeHide=$row.HiddenAttemptId}
    })
    [ordered]@{name=$Name;sha256=Hash $raw;wire=$s.WireSchemaVersion;base=$s.SchemaVersion;at=$s.RuleClock.ToString()
        revision=$s.Revision;clockRng=$s.RandomState;currentMarker=$s.WorldSchedule.MarkerId($ledger.LastStart)
        actionSpent=$ledger.ActionSpent;hide=$hide;search=$search;observations=$observations;knowledge=$knowledge}
}
$apply = $test.GetMethod('CCApply',$flags)
$events = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@(
    $apply.Invoke($null,@('hide-companion-away','Blinded',$searcher,(Stamp 43),(Stamp 36),$null))
    $apply.Invoke($null,@('hide-witness-away','Blinded',$witness,(Stamp 55),(Stamp 36),$null))
)
$ready = Read-Save 'real-combat-exit'
$paid = Read-Save 'paid-declared'
$roll = Read-Save 'rolled-two-observers'
$forward = Read-Save 'coincident-hide-before-search' 1
$reverse = Read-Save 'coincident-search-before-hide' 1
$suppressed = Read-Save 'unchanged-paid-no-roll' 2 $events
$alternate = Read-Save 'alternate-real-hidden' 2 $events
$continued = Read-Save 'continued-and-found' 2 $events
if ($ready.observations.Count -ne 0 -or $ready.actionSpent -or -not $paid.actionSpent -or $roll.actionSpent -or
    $paid.currentMarker -cne 'world.fixed-calendar.start.10' -or $roll.currentMarker -cne 'world.fixed-calendar.start.12' -or
    $roll.hide[0].paidMarker -cne $paid.currentMarker -or $roll.observations[0].comparisons.Count -ne 2) {
    throw 'The real exit, original Hide payment and independently refreshed Start were not recovered.'
}
if ($forward.at -cne '36/1' -or $reverse.at -cne $forward.at -or $forward.observations[0].kind -cne 'Hide' -or
    $reverse.observations[0].kind -cne 'Search' -or $forward.search[0].hide -cne $forward.observations[0].id -or
    $reverse.observations[0].words -ne 0 -or $forward.observations[1].before -ne $forward.observations[0].after -or
    $reverse.observations[1].before -ne $reverse.observations[0].after) {
    throw 'The retained coincident saves do not prove both receipt orders.'
}
if ($suppressed.hide[-1].privateNoRoll -cne 'UnchangedFailure' -or $alternate.hide[-1].actualRelocation.at -cne '73/1' -or
    $continued.at -cne '114/1' -or @($continued.search | Where-Object hide -CNE $alternate.hide[-1].observation).Count -ne 0 -or
    -not $continued.knowledge[0].currentLocationKnown -or $continued.knowledge[0].hidden -or -not $continued.knowledge[1].hidden) {
    throw 'The retained retry, relocation or Search continuation does not bind the genuine Hide result.'
}
[ordered]@{status='PASS';assemblies=$assemblies;restored=@($ready,$paid,$roll,$forward,$reverse,$suppressed,$alternate,$continued)} |
    ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $OutputFile -Encoding utf8
