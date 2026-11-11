param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = foreach ($name in 'Core', 'Persistence', 'LabModel', 'HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{ name = (Split-Path -Leaf $path); sha256 = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
}
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$method = $fixture.GetMethod('RetreatPolicy', $flags)
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Read-Save([string]$Name, $Seed = $null, [switch]$DecodeOnly) {
    $file = @(Get-ChildItem -LiteralPath $Saves -File -Recurse -Filter "$Name.ddsave")
    if ($file.Count -ne 1) { throw "Expected one retained $Name save" }
    $bytes = [IO.File]::ReadAllBytes($file[0].FullName)
    $state = $codec.Decode($bytes)
    if (-not $DecodeOnly) {
        $policy = $method.Invoke($null, @($Seed, $null, $null))
        $sim = [Decennium.Foundation.Simulation]::new($policy, $state, [Decennium.Foundation.ExecutionProfile]::Laboratory)
        $state = $sim.Capture()
    }
    $hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    if ($hash -ne [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($state))).ToLowerInvariant()) {
        throw "Retained $Name changed when re-encoded"
    }
    [pscustomobject]@{ state = $state; sha256 = $hash; name = $Name }
}
function Position($Actor) { @($Actor.X, $Actor.Y) }
function Describe($File) {
    $s = $File.state
    $d = $s.Retreat.Definition
    $archive = $s.ClosedEncounters | Where-Object { $_.Encounter.Id -ceq $d.EncounterId }
    $checkpoint = foreach ($c in $s.ExpeditionPressureCheckpoints) {
        [ordered]@{ watch = $c.WatchIndex; time = $c.At.ToString(); receipt = $c.CommandId; revision = $c.AppliedRevision
            before = $c.PressureBefore; stored = $c.StoredPressure; natural = $c.Natural; causes = @($c.CauseIds)
            consequence = $c.Consequence.ToString(); consequenceEnds = if ($null -ne $c.ConsequenceEndsAt) { $c.ConsequenceEndsAt.ToString() } }
    }
    $rounds = foreach ($r in $s.Retreat.Rounds) {
        $threat = $s.MeleeAttacks | Where-Object Id -CEQ $r.ThreatId
        $settled = $r.Settlement
        [ordered]@{ round = $r.Number; started = $r.StartedAt.ToString(); startRevision = $r.StartRevision
            task = if ($r.Task) { [ordered]@{ id = $r.Task.CommandId; revision = $r.Task.Revision; turn = $r.Task.Turn
                natural = $r.Task.Natural; dice = @($r.Task.First, $r.Task.Second); modifier = $r.Task.Modifier
                degree = $r.Task.Degree.ToString(); randomBefore = $r.Task.RandomBefore; randomAfter = $r.Task.RandomAfter } }
            threat = if ($threat) { [ordered]@{ id = $threat.Id; revision = $threat.Revision; turn = $threat.TurnOrdinal; hit = $threat.Attack.Hit } }
            end = if ($settled) { [ordered]@{ time = $settled.At.ToString(); receipt = $settled.CommandId; revision = $settled.Revision
                turn = $settled.EndTurn; outcome = $settled.Outcome.ToString(); lead = @(Position $settled.Lead)
                companion = @(Position $settled.Companion); defender = @(Position $settled.Defender)
                crossingIds = @($settled.LeadCrossingId, $settled.CompanionCrossingId) } }
        }
    }
    $exposure = $s.ExpeditionPressureExposures | Where-Object Id -CEQ $d.ExposureId
    $change = foreach ($c in $s.ExpeditionPressureChanges) {
        [ordered]@{ id = $c.Id; kind = $c.Kind.ToString(); watch = $c.WatchIndex; source = $c.SourceId
            revision = $c.SourceRevision; time = $c.At.ToString() }
    }
    [ordered]@{ name = $File.name; sha256 = $File.sha256; revision = $s.Revision; time = $s.RuleClock.ToString(); rng = $s.RandomState
        schema = $s.SchemaVersion; fingerprint = $s.ContentFingerprint; charter = if ($s.CharterAttempt) { $s.CharterAttempt.Outcome.ToString() }
        activeEncounter = if ($s.Encounter) { $s.Encounter.Id }; archive = if ($archive) { [ordered]@{ id = $archive.Encounter.Id
            end = $archive.ClosedAt.ToString(); revision = $archive.ClosedRevision; command = $archive.Reason
            oldOrder = @($archive.Encounter.InitialOrder); continuedOrder = @($archive.Encounter.RosterPhase.Epoch.Order)
            observedOrdinals = @($archive.Encounter.ObservedOrdinals) } }
        body = @($s.Actors | Where-Object { $_.Id -cin @($d.LeadId, $d.CompanionId, $d.DefenderId) } | ForEach-Object {
            [ordered]@{ id = $_.Id; coordinates = @(Position $_); hp = ($s.Lives | Where-Object ActorId -CEQ $_.Id).Hp } })
        work = @($s.WaterFills | ForEach-Object { [ordered]@{ id = $_.Id; status = $_.Status.ToString(); worker = $_.WorkerId; progress = $_.Progress.ToString() } })
        escape = $s.Retreat.Escape; pursuit = $s.Retreat.Pursuit; declaration = $s.Retreat.DeclarationId; rounds = @($rounds)
        pressure = if ($exposure) { [ordered]@{ route = $d.RouteId; cohort = $d.CohortId
            members = @($s.ExpeditionPressureCohorts[0].Members); quality = $d.Quality.ToString(); risk = $d.Risk
            activatedAt = $exposure.StartedAt.ToString(); activatedRevision = $exposure.StartedRevision
            initial = $d.InitialPressure; current = [Decennium.Foundation.ExpeditionPressureRules]::Current($s, $d.CohortId)
            changes = @($change); checkpoints = @($checkpoint) } }
    }
}
$witnesses = @(
    (Read-Save 'exp07-retreat-connected-before-declaration'),
    (Read-Save 'exp07-retreat-connected-final-round'),
    (Read-Save 'exp07-retreat-connected-exit'),
    (Read-Save 'exp07-retreat-connected-continued'),
    (Read-Save 'exp07-retreat-failed' ([uint32]2)),
    (Read-Save 'exp07-retreat-same-watch-exit' ([uint32]7)),
    (Read-Save 'exp07-retreat-following-watch' ([uint32]7)),
    (Read-Save 'exp07-retreat-same-watch-obstruction' ([uint32]42)),
    (Read-Save 'exp07-retreat-remote-work'),
    (Read-Save 'exp07-retreat-live-condition' -DecodeOnly)
)
[ordered]@{
    status = 'PASS'
    source = 'Retained schema 88 headless fixtures. The condition fixture uses its focused test for canonical replay.'
    assemblies = $assemblies
    witnesses = @($witnesses | ForEach-Object { Describe $_ })
} | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $OutputFile -Encoding utf8
