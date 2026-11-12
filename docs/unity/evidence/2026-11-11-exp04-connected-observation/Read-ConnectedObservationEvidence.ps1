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
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$hero = [Decennium.Foundation.ConnectedExplorationObservation]::Hero
$companion = [Decennium.Foundation.ConnectedExplorationObservation]::Searcher
$buyer = [Decennium.Foundation.ConnectedExplorationObservation]::Buyer
$defender = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
function Hash([byte[]]$Data) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant() }
function Stage([string]$Name,[Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]$Events=@()) {
    $arguments = [object[]]::new(1)
    $arguments[0] = $Events
    $policy = $tests.GetMethod('ConnectedObservationPolicy',$flags).Invoke($null,$arguments)
    $raw = [IO.File]::ReadAllBytes((Join-Path $Saves "exp04-connected-observation-$Name.ddsave"))
    $sim = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $s = $sim.Capture()
    if ($s.WireSchemaVersion -ne 93 -or $s.SchemaVersion -ne 90 -or (Hash ($codec.Encode($s))) -cne (Hash $raw)) {
        throw "The selected save failed an exact wire93 restore: $Name"
    }
    $current = [Decennium.Foundation.WorldTiming]::ForActor($s,$hero)
    $allowance = $s.WorldIntervals | Where-Object ActorId -CEQ $hero
    $searcher = $s.WorldActivityIntervals | Where-Object ActorId -CEQ $companion
    $position = $s.Actors | Where-Object Id -CEQ $hero
    $entry = $s.LaterEncounter.Entry
    $hide = @($s.ExplorationHide.Attempts | ForEach-Object {
        $a = $_
        $row = [ordered]@{id=$a.Id;declaration=$a.CommandId;revision=$a.Revision;paidCalendar=$a.CalendarId
            paidStart=$a.PaidStart;started=$a.StartedAt.ToString();due=$a.DueAt.ToString();anchor=@($a.Anchor.X,$a.Anchor.Y)
            status=$a.Status.ToString()}
        if ($a.End) { $row.end = [ordered]@{at=$a.End.At.ToString();command=$a.End.CommandId;revision=$a.End.Revision
            observation=$a.End.ObservationId;reason=$a.End.Interruption.ToString();observers=$a.End.EligibleObservers.ToString()} }
        if ($a.Relocation) { $row.arrived = $a.Relocation.At.ToString() }
        $row
    })
    $search = @($s.ExplorationSearch.Attempts | ForEach-Object {
        $a = $_
        $row = [ordered]@{id=$a.Id;declaration=$a.CommandId;revision=$a.Revision;interval=$a.IntervalIndex
            started=$a.StartedAt.ToString();due=$a.DueAt.ToString();status=$a.Status.ToString()}
        if ($a.End) { $row.end = [ordered]@{at=$a.End.At.ToString();command=$a.End.CommandId;revision=$a.End.Revision
            observation=$a.End.ObservationId;reason=$a.End.Interruption.ToString();hide=$a.End.HideId} }
        $row
    })
    $checks = @($s.ObservationActions | ForEach-Object {
        $a = $_
        [ordered]@{id=$a.Id;kind=$a.Kind.ToString();at=$a.At.ToString();revision=$a.Revision
            outcome=$a.Outcome.ToString();natural=$a.Natural;total=$a.Total;words=$a.WordsConsumed
            before=$a.RandomBefore;after=$a.RandomAfter;comparisons=@($s.ObservationHideResults |
                Where-Object AttemptId -CEQ $a.Id | ForEach-Object {
                    [ordered]@{observer=$_.ObserverId;dc=$_.Dc;degree=$_.Degree.ToString();hidden=$_.HiddenEstablished}
                })}
    })
    $knowledge = @(foreach ($observer in $companion,$buyer,$defender) {
        $k = $s.ObserverKnowledge | Where-Object {$_.ObserverId -ceq $observer -and $_.TargetId -ceq $hero}
        [ordered]@{observer=$observer;hidden=[Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($s,$observer,$hero)
            sees=[Decennium.Foundation.Laboratory.ObservationRules]::CanSee($s,$observer,$hero);evidence=$k.Evidence.ToString()
            known=[Decennium.Foundation.Laboratory.ObservationRules]::LocationKnown($s,$observer,$hero)}
    })
    $result = [ordered]@{name=$Name;sha256=Hash $raw;wire=$s.WireSchemaVersion;base=$s.SchemaVersion
        at=$s.RuleClock.ToString();revision=$s.Revision;rng=$s.RandomState;tactical=$s.InventoryCombat;hero=@($position.X,$position.Y)
        currentHeroCalendar=$current.Id;currentHeroOrdinal=$allowance.LastStart;currentHeroActionSpent=$allowance.ActionSpent
        searcherCalendar=$searcher.CalendarId;searcherInterval=$searcher.IntervalIndex
        searcherAction=$searcher.Action.ToString();searcherPayment=$searcher.ActionReference
        hide=$hide;search=$search;checks=$checks;knowledge=$knowledge}
    if ($entry) {
        $result.entry = [ordered]@{at=$entry.Epoch.Origin.ToString();receipt=$entry.ArrivalCommandId;revision=$entry.ArrivalRevision
            director=$s.SurpriseEntry.Binding.DirectorId;decision=$s.SurpriseEntry.Binding.Outcome.ToString();order=@($entry.Epoch.Order)
            draws=@($entry.Draws | Select-Object ActorId,Natural,RandomBefore,RandomAfter,WordsConsumed)}
    }
    if ($s.ClosedEncounters.Count -eq 2) {
        $sale = $s.HavenSales[0]
        $result.continued = [ordered]@{earlierCombat=$s.ClosedEncounters[0].ClosedAt.ToString()
            acquiredLot=$sale.Basis.GoodsLotId;paidAt=$sale.UpdatedAt.ToString();paidCopper=$sale.PaymentCopper
            mealAt=$s.HavenMealPurchases[0].EndedAt.ToString();billAt=$s.ExpeditionBills[0].UpdatedAt.ToString()
            charterReturned=$s.CharterAttempt.Returned.At.ToString();laterCombatClosed=$s.ClosedEncounters[1].ClosedAt.ToString()
            realLaterAttacks=@($s.MeleeAttacks | Where-Object {$_.Revision -gt $entry.ArrivalRevision} |
                Select-Object Id,Revision,AttackerId,TargetId)}
    }
    $result
}

$ready = Stage 'before-observation'
$first = Stage 'primary-failure'
$alternate = Stage 'alternate-hidden'
$return = Stage 'returned-unseen-to-searcher'
$pending = Stage 'paid-search'
$entry = Stage 'actual-later-entry'
$continued = Stage 'continued-after-real-combat'
$hideFirst = Stage 'hide-first'
$searchFirst = Stage 'search-first'
$event = $tests.GetMethod('CCApply',$flags).Invoke($null,@('connected-defender-blind-at-arrival','Blinded',$defender,$null,
    [Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(23281,2),0),$null))
$events = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@($event)
$interrupted = Stage 'search-interrupted-by-actual-entry' $events
$failed = Stage 'failed-contact-search-completed' $events

if ($ready.at -cne '11610/1' -or $first.checks[0].natural -ne 9 -or $alternate.checks[-1].total -ne 12 -or
    -not $return.knowledge[0].hidden -or -not $return.knowledge[1].sees -or $pending.searcherAction -cne 'Search' -or
    $entry.search[0].end.hide -cne $alternate.checks[-1].id -or $entry.checks[-1].outcome -cne 'SearchFound' -or
    $entry.entry.draws[0].RandomBefore -ne $entry.checks[-1].after -or $entry.entry.decision -cne 'Warned' -or
    $continued.tactical -or -not $continued.continued -or $continued.currentHeroCalendar -cne 'TEST_ONLY.later-calendar' -or
    $continued.hide[0].paidCalendar -cne 'world.fixed-calendar') {
    throw 'The actual saved connected chain lost an observation, payment, RNG or mode relationship.'
}
if ($hideFirst.at -cne $searchFirst.at -or $hideFirst.checks[-1].natural -ne 4 -or $searchFirst.checks[-2].natural -ne 15 -or
    $hideFirst.search[0].end.hide -cne $hideFirst.checks[-2].id -or $searchFirst.search[0].end.hide -cne $alternate.checks[-1].id) {
    throw 'The two exact receipt-order witnesses do not retain their respective observation and RNG evidence.'
}
if ($interrupted.search[0].end.command -cne $interrupted.entry.receipt -or
    $interrupted.search[0].end.at -cne '23283/2' -or $interrupted.search[0].end.observation -cne '' -or
    $interrupted.searcherAction -cne 'Search' -or $failed.entry -or $failed.search[0].end.at -cne '11646/1' -or
    $failed.checks[0].words -ne 0) {
    throw 'The successful and failed later-contact saves do not retain the different ordinary Search consequences.'
}
[ordered]@{status='PASS';assemblies=$assemblies
    restored=@($ready,$first,$alternate,$return,$pending,$entry,$continued,$hideFirst,$searchFirst,$interrupted,$failed)} |
    ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $OutputFile -Encoding utf8
