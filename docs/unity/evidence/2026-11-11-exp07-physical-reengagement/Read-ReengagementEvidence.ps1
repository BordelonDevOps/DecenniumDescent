param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = foreach ($name in 'Core', 'Persistence', 'LabModel', 'HeadlessTests') {
    $dll = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $dll
    [ordered]@{ name = (Split-Path -Leaf $dll); sha256 = (Get-FileHash -LiteralPath $dll).Hash.ToLowerInvariant() }
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Read-State([string]$Name, $Seed = $null, [switch]$DecodeOnly) {
    $files = @(Get-ChildItem -LiteralPath $Saves -Recurse -File -Filter "$Name.ddsave")
    if ($files.Count -ne 1) { throw "Expected one save for $Name" }
    $bytes = [IO.File]::ReadAllBytes($files[0].FullName)
    $s = $codec.Decode($bytes)
    if (-not $DecodeOnly) {
        $method = $fixture.GetMethod('ReengagementPolicy', $flags)
        $policy = $method.Invoke($null, @($Seed, $null, $true, $true))
        $s = ([Decennium.Foundation.Simulation]::new($policy, $s, [Decennium.Foundation.ExecutionProfile]::Laboratory)).Capture()
    }
    $hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    $actual = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($s))).ToLowerInvariant()
    if ($hash -cne $actual) { throw "Save $Name re-encoded differently" }
    $d = $s.Reengagement.Definition
    $phase = $s.Reinforcement.Admission.Phase
    $pressure = [Decennium.Foundation.ExpeditionPressureRules]::Current($s, $s.Retreat.Definition.CohortId)
    $contacts = foreach ($c in $s.Reengagement.Contacts) {
        $walk = $s.Receipts | Where-Object Revision -EQ $c.ApproachRevision
        $advance = $s.Receipts | Where-Object Revision -EQ $c.ArrivalRevision
        [ordered]@{ at = $c.At.ToString(); originalMarker = $c.MarkerOrdinal; entered = $c.Entered; reason = $c.Failure
            paidFeet = $c.DistanceFeet.ToString(); approach = $walk.Id; controller = $walk.Principal
            approachRevision = $c.ApproachRevision; arrival = $advance.Id; arrivalRevision = $c.ArrivalRevision }
    }
    $archives = foreach ($a in $s.ClosedEncounters) {
        [ordered]@{ id = $a.Encounter.Id; actualOrigin = $a.Encounter.Origin.ToString(); exit = $a.Reason
            at = $a.ClosedAt.ToString(); revision = $a.ClosedRevision; ordinals = @($a.Encounter.ObservedOrdinals) }
    }
    [ordered]@{ name = $Name; sha256 = $hash; schema = $s.SchemaVersion; fingerprint = $s.ContentFingerprint
        clock = $s.RuleClock.ToString(); revision = $s.Revision; rng = $s.RandomState; root = $d.RootId; segment = $d.SegmentId
        epoch = $phase.Epoch.Id; inheritedOrigin = $phase.Epoch.Origin.ToString(); inheritedOrder = @($phase.Epoch.Order)
        originalRetreat = $s.Retreat.SuccessfulExit.CommandId; originalRetreatAt = $s.Retreat.SuccessfulExit.At.ToString()
        contact = @($contacts); archives = @($archives)
        active = if ($s.Encounter) { [ordered]@{ id = $s.Encounter.Id; origin = $s.Encounter.Origin.ToString()
            currentActor = $s.Encounter.CurrentActor; currentTurnId = $s.Encounter.CurrentTurnId; round = $s.Encounter.Round
            starts = @(for ($i = 0; $i -lt $s.Encounter.ObservedOrdinals.Count; $i++) {
                $ordinal = $s.Encounter.ObservedOrdinals[$i]
                [ordered]@{ ordinal = $ordinal; time = $s.Encounter.StartAt($ordinal).ToString()
                    revision = $s.Encounter.StartRevisions[$i]; actor = $s.Encounter.ActorAt($ordinal) }
            }) } }
        participants = @(foreach ($id in $d.LeadId, $d.CompanionId, $d.DefenderId) {
            $life = $s.Lives | Where-Object ActorId -CEQ $id
            $interval = $s.WorldIntervals | Where-Object ActorId -CEQ $id
            $position = [Decennium.Foundation.WorldPositionResolver]::Position($s, $id)
            [ordered]@{ id = $id; physicalPosition = @($position.Item1.ToString(), $position.Item2.ToString()); hp = $life.Hp
                dead = $life.Dead; held = @($life.HeldItems); interval = $interval.LastStart; actionSpent = $interval.ActionSpent
                dashPaid = $interval.DashPaid; movementSpent = $interval.MovementSpent.ToString()
                reaction = $interval.ReactionAvailable; interactions = $interval.Interactions }
        })
        pendingWalk = @($s.WorldTraversals | ForEach-Object { [ordered]@{ actor = $_.ActorId; paid = $_.DistanceFeet.ToString()
            startedRevision = $_.StartedRevision; status = $_.Status.ToString() } })
        timedConditions = @(foreach ($journal in $s.Conditions) {
            $ledger = [Decennium.Foundation.Laboratory.ConditionHistory]::Restore($journal).Ledger
            foreach ($effect in $ledger.Applications | Where-Object { $_.Application.Id -clike 'reengagement-*' }) {
                [ordered]@{ actor = $journal.Target; id = $effect.Application.Id
                    expires = if ($effect.Application.Expires) { $effect.Application.Expires.Time.ToString() }
                    ended = if ($effect.EndedAt) { $effect.EndedAt.Time.ToString() } }
            }
        })
        waterWork = @($s.WaterFills | ForEach-Object { [ordered]@{ worker = $_.WorkerId; job = $_.Id
            progress = $_.Progress.ToString(); status = $_.Status.ToString() } })
        pressure = [ordered]@{ value = $pressure; exposure = $s.ExpeditionPressureExposures[0].Id
            retreatCauses = @($s.ExpeditionPressureChanges | Where-Object Kind -EQ SuccessfulRetreat | ForEach-Object SourceId)
            watches = @($s.ExpeditionPressureCheckpoints | ForEach-Object { [ordered]@{ watch = $_.WatchIndex
                at = $_.At.ToString(); receipt = $_.CommandId; revision = $_.AppliedRevision
                prior = $_.PressureBefore; stored = $_.StoredPressure; natural = $_.Natural; consequence = $_.Consequence.ToString() } }) }
        attacksAfterContact = @(if ($s.Reengagement.Entry) {
            $s.MeleeAttacks | Where-Object Revision -GT $s.Reengagement.Entry.ArrivalRevision | ForEach-Object {
                [ordered]@{ id = $_.Id; at = $_.At.ToString(); turn = $_.TurnOrdinal; attacker = $_.AttackerId
                    target = $_.TargetId; hit = $_.Attack.Hit }
            }
        })
    }
}
$witnesses = @(
    (Read-State 'exp07-reengagement-before-approach'),
    (Read-State 'exp07-reengagement-partial'),
    (Read-State 'exp07-reengagement-contact'),
    (Read-State 'exp07-reengagement-inherited-starts'),
    (Read-State 'exp07-reengagement-unmodified-integrity'),
    (Read-State 'exp07-reengagement-dash-and-markers' -DecodeOnly),
    (Read-State 'exp07-reengagement-remote-work'),
    (Read-State 'exp07-reengagement-watch-admitted' ([uint32]20)),
    (Read-State 'exp07-reengagement-watch-closed' ([uint32]15)),
    (Read-State 'exp07-reengagement-partial-watch-closure' ([uint32]15)),
    (Read-State 'exp07-reengagement-condition-at-arrival' -DecodeOnly),
    (Read-State 'exp07-reengagement-paid-attack'),
    (Read-State 'exp07-reengagement-closed'),
    (Read-State 'exp07-reengagement-continued')
)
[ordered]@{ status = 'PASS'; assemblies = $assemblies; witnesses = $witnesses
    scope = 'The two condition-specific saves are replayed by their exact focused test and decoded here.' } |
    ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $OutputFile -Encoding utf8
