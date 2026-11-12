param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $file = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $file
    [ordered]@{name=Split-Path -Leaf $file;sha256=(Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant()}
})
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$authority = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::Host()
function Read-State([string]$Name) {
    $path = Join-Path $Saves "exp04-search-$Name.ddsave"
    $bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $path).Path)
    [pscustomobject]@{file=Split-Path -Leaf $path;sha256=[Convert]::ToHexString(
        [Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant();state=$codec.Decode($bytes)}
}
function Restore($State) {
    $events = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
    $policy = $fixture.GetMethod('ExplorationSearchPolicy',$flags).Invoke($null,@($true,5,$events))
    [Decennium.Foundation.Simulation]::new($policy,$State,[Decennium.Foundation.ExecutionProfile]::Laboratory)
}
function Public-View($Simulation,[string]$Id) {
    $view = $Simulation.ObserveExplorationSearch($authority,$Id)
    [ordered]@{id=$view.AttemptId;status=$view.Status.ToString();start=$view.StartedAt.ToString();due=$view.DueAt.ToString()
        ended=if($view.EndedAt){$view.EndedAt.ToString()};location=if($view.FoundLocation){$view.FoundLocation.ToString()}}
}
$groups = @('qualified-failure','empty-completed','unseen-vacated-candidate','occupied-without-sensory-cue','target-partial-at-completion')
$controls = @(foreach ($group in $groups) {
    $save = Read-State $group
    $s = $save.state
    $attempt = $s.ExplorationSearch.Attempts[0]
    $result = $s.ObservationActions | Where-Object Id -CEQ $attempt.End.ObservationId
    $actual = [Decennium.Foundation.WorldPositionResolver]::Position($s,$s.ExplorationSearch.Definition.ConcealedActorId)
    [ordered]@{branch=$group;file=$save.file;sha256=$save.sha256;wire=$s.WireSchemaVersion;base=$s.SchemaVersion
        public=Public-View (Restore $s) $attempt.Id
        privateAudit=[ordered]@{candidate=$attempt.Candidate.ToString();cue=$attempt.End.CueId;hide=$attempt.End.HideId
            actualTargetPosition=@($actual.Item1.ToString(),$actual.Item2.ToString());diceWords=$result.WordsConsumed
            rngAfter=$result.RandomAfter;actualCompletionReceipt=$attempt.End.CommandId}}
})
$public = $controls[0].public | ConvertTo-Json -Compress
if (@($controls | Where-Object {($_.public | ConvertTo-Json -Compress) -cne $public}).Count -ne 0) {
    throw 'The observed authorized no-finding projections differ.'
}

$closed = Read-State 'qualified-failure'
$reentry = Restore $closed.state
$before = $closed.state.ExplorationSearch.Attempts[0].End
$command = $fixture.GetMethod('IC',$flags).Invoke($null,@($reentry,[Decennium.Foundation.CommandKind]::BeginFixedEncounter,
    '',$null,$closed.state.ExplorationSearch.Definition.ConcealedActorId,0,0,'search.evidence.same-time-reentry'))
$transition = $reentry.Execute($authority,$command)
$entered = $reentry.Capture()
$end = $entered.ExplorationSearch.Attempts[0].End
if ($transition.Outcome.ToString() -cne 'Committed' -or -not $entered.InventoryCombat -or $entered.RuleClock -ne $before.At -or
    $end.ObservationId -cne $before.ObservationId -or $end.Revision -ne $before.Revision -or $entered.RandomState -ne $closed.state.RandomState) {
    throw 'A later command at the same timestamp altered the committed Search.'
}

$found = Read-State 'actual-find'
$continued = Read-State 'continued-unseen-movement'
$d = $found.state.ExplorationSearch.Definition
$known = $continued.state.ObserverKnowledge | Where-Object {$_.ObserverId -ceq $d.SearcherId -and $_.TargetId -ceq $d.ConcealedActorId}
[ordered]@{status='PASS';assemblies=$assemblies;equalNoFinding=$controls
    laterSameTimeMode=[ordered]@{at=$entered.RuleClock.ToString();searchRevision=$end.Revision;modeRevision=$entered.Revision
        mode=$command.Id;existingEncounter=$entered.Encounter.Id;searchObservation=$end.ObservationId}
    actualFind=Public-View (Restore $found.state) $found.state.ExplorationSearch.Attempts[-1].Id
    unseenContinuation=[ordered]@{at=$continued.state.RuleClock.ToString();currentlyKnown=$known.CurrentLocationKnown
        lastKnown=@($known.LastKnownX.ToString(),$known.LastKnownY.ToString());evidenceAt=$known.EvidenceAt.ToString()
        previousHiddenLatch=$known.HiddenAttemptId}} |
    ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $OutputFile -Encoding utf8
