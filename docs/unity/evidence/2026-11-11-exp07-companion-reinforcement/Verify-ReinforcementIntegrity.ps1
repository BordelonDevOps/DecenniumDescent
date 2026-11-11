param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$AdmittedSave,
    [Parameter(Mandatory)][string]$ClosedSave,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core','Persistence','LabModel','HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$laboratory = [Decennium.Foundation.ExecutionProfile]::Laboratory
$admittedBytes = [IO.File]::ReadAllBytes((Resolve-Path $AdmittedSave).Path)
$closedBytes = [IO.File]::ReadAllBytes((Resolve-Path $ClosedSave).Path)
$controls = [Collections.Generic.List[object]]::new()

function New-Policy {
    $fixture.GetMethod('ReinforcementPolicy',$flags).Invoke($null,
        @($null,$null,[Decennium.Foundation.Laboratory.TerrainCost]::Normal,$null))
}
function Hash-Bytes([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Assert-True([bool]$Condition,[string]$Message) {
    if (-not $Condition) { throw $Message }
}
function Assert-Rejected([string]$Name,[string]$Stage,[string]$Expected,[scriptblock]$Action) {
    $failure = $null
    try { $null = & $Action }
    catch { $failure = $_.Exception.GetBaseException() }
    Assert-True ($failure -is [ArgumentException] -and $failure.Message.Contains($Expected)) (
        "$Name at $Stage expected $Expected, observed $($failure.Message)")
    $controls.Add([ordered]@{name=$Name;stage=$Stage;error=$failure.Message})
}
function Assert-ReplayRejected([string]$Name,[Decennium.Foundation.Snapshot]$Snapshot) {
    $encoded = $codec.Encode($Snapshot)
    $decoded = $codec.Decode($encoded)
    Assert-True ((Hash-Bytes ($codec.Encode($decoded))) -eq (Hash-Bytes $encoded)) "$Name did not preserve structure"
    Assert-Rejected $Name 'canonical replay after successful codec roundtrip' 'InvalidSharedWorldReplay' {
        [Decennium.Foundation.Simulation]::new((New-Policy),$decoded,$laboratory)
    }
}
foreach ($original in @($admittedBytes,$closedBytes)) {
    $decoded = $codec.Decode($original)
    $replayed = [Decennium.Foundation.Simulation]::new((New-Policy),$decoded,$laboratory)
    Assert-True ($decoded.SchemaVersion -eq 87 -and $decoded.TestOnly -and
        (Hash-Bytes ($codec.Encode($replayed.Capture()))) -eq (Hash-Bytes $original)) 'Authentic replay changed'
}

$state = $codec.Decode($admittedBytes)
$record = $state.Reinforcement
$d = $record.Definition
$wrongController = [Decennium.Foundation.ReinforcementDefinition]::new($d.Id,$d.EncounterId,$d.EpochId,
    $d.CompanionId,$d.AllyId,'TEST_ONLY.forged-controller',$d.ParticipationMandateId,$d.AlliedSideId,
    $d.PlayerTieChoiceId,$d.DirectorTieChoiceId)
$state.Reinforcement = [Decennium.Foundation.ReinforcementRecord]::new($wrongController,$record.Events,$record.Admission)
Assert-Rejected 'forged controller against the original consent receipt' 'structural codec' 'Invalid reinforcement consent or cancellation receipt' {
    $codec.Encode($state)
}

$state = $codec.Decode($admittedBytes)
$record = $state.Reinforcement
$a = $record.Admission
$draw = $a.Draw
$wrongDraw = [Decennium.Foundation.LaterInitiativeDraw]::new($draw.ActorId,$draw.Natural,
    $draw.DexterityModifier,$draw.Bonus,[uint32]($draw.RandomBefore -bxor 1),$draw.RandomAfter,$draw.WordsConsumed)
Assert-True ($wrongDraw.Total -eq $draw.Total -and $wrongDraw.RandomBefore -ne $draw.RandomBefore) 'Draw mutation changed the total'
$state.Reinforcement = [Decennium.Foundation.ReinforcementRecord]::new($record.Definition,$record.Events,
    [Decennium.Foundation.ReinforcementAdmission]::new($a.Phase,$wrongDraw,$a.Carried))
Assert-ReplayRejected 'forged entrant RNG input with unchanged draw total and order' $state

$state = $codec.Decode($admittedBytes)
$phase = $state.Reinforcement.Admission.Phase
$wrongBoundary = [Decennium.Foundation.EncounterRosterPhase]::new($phase.Epoch,($phase.FirstTurn+1),$phase.FirstRound)
Assert-Rejected 'phase begins one global turn late' 'encounter roster phase binding' 'Invalid end-round roster transition' {
    $state.Encounter.BindRosterPhase($wrongBoundary)
}
$wrongRound = [Decennium.Foundation.EncounterRosterPhase]::new($phase.Epoch,$phase.FirstTurn,($phase.FirstRound+1))
Assert-Rejected 'phase skips one continuous round' 'encounter roster phase binding' 'Invalid end-round roster transition' {
    $state.Encounter.BindRosterPhase($wrongRound)
}

$state = $codec.Decode($admittedBytes)
$record = $state.Reinforcement
$a = $record.Admission
$carried = [Decennium.Foundation.ReinforcementCarry[]]@($a.Carried | ForEach-Object {
    $i = $_.Interval
    if ($i.ActorId -eq $record.Definition.CompanionId) {
        $changed = [Decennium.Foundation.WorldIntervalRecord]::new($i.ActorId,$i.LastStart,
            ($i.MovementSpent + [Decennium.Foundation.RuleQuantity]::new(1,1)),$i.ActionSpent,$i.DashPaid,
            $i.ReactionAvailable,$i.Interactions)
        [Decennium.Foundation.ReinforcementCarry]::new($changed,$_.BonusActionAvailable)
    } else { $_ }
})
$state.Reinforcement = [Decennium.Foundation.ReinforcementRecord]::new($record.Definition,$record.Events,
    [Decennium.Foundation.ReinforcementAdmission]::new($a.Phase,$a.Draw,$carried))
Assert-ReplayRejected 'forged companion movement spent in the transfer record' $state

$state = $codec.Decode($closedBytes)
$archive = $state.ClosedEncounters
Assert-True ($archive.Length -eq 2 -and $archive[0].Encounter.RosterPhase -eq $null -and
    $archive[1].Encounter.RosterPhase -ne $null) 'Expected first and phased later archives'
$later = $archive[1]
$archive[1] = [Decennium.Foundation.ClosedEncounterRecord]::new(
    $later.Encounter,$later.ClosedRevision,$later.ClosedAt,'review.forged-exit-receipt')
Assert-Rejected 'forged later exit receipt with the first archive intact' 'structural codec' 'Invalid later encounter exit provenance' {
    $codec.Encode($state)
}

$state = $codec.Decode($admittedBytes)
$sim = [Decennium.Foundation.Simulation]::new((New-Policy),$state,$laboratory)
$hostAuthority = $fixture.GetMethod('LaterHost',$flags).Invoke($null,@())
$beginReceipt = $state.Receipts | Where-Object Revision -EQ $state.Reinforcement.Began.Revision
$joinReceipt = $state.Receipts | Where-Object Revision -EQ $state.Reinforcement.Joined.Revision
$begin = [Decennium.Foundation.CommandHistory]::Read($beginReceipt)
$join = [Decennium.Foundation.CommandHistory]::Read($joinReceipt)
$conflict = [Decennium.Foundation.Command]::new($begin.Id,$begin.Actor,$begin.ExpectedRevision,$begin.Kind,'review.conflicting-definition')
$fresh = [Decennium.Foundation.Command]::new('review.fresh-approach-after-admission',$begin.Actor,$state.Revision,$begin.Kind,$begin.Target)
foreach ($trial in @(
    @{name='exact duplicate originating consent';command=$begin;outcome='Duplicate';code='AlreadyCommitted'},
    @{name='exact duplicate of the admitting incumbent End';command=$join;outcome='Duplicate';code='AlreadyCommitted'},
    @{name='same command ID with conflicting payload';command=$conflict;outcome='Rejected';code='CommandIdConflict'},
    @{name='fresh-ID approach after admission';command=$fresh;outcome='Rejected';code='ReinforcementAlreadyAttempted'}
)) {
    $r = $sim.Execute($hostAuthority,$trial.command)
    $after = $sim.Capture()
    $digest = Hash-Bytes ($codec.Encode($after))
    Assert-True ($r.Outcome.ToString() -eq $trial.outcome -and $r.Code -eq $trial.code -and
        $digest -eq (Hash-Bytes $admittedBytes) -and $after.RandomState -eq $state.RandomState -and
        @($after.Reinforcement.Events | Where-Object Kind -EQ 'Admitted').Count -eq 1 -and
        $after.Reinforcement.Admission.Draw.RandomAfter -eq $state.Reinforcement.Admission.Draw.RandomAfter) (
        "$($trial.name) returned $($r.Outcome)/$($r.Code) or changed canonical bytes, RNG, or the single admission")
    $controls.Add([ordered]@{name=$trial.name;stage='actual command dispatch';outcome=$r.Outcome.ToString();
        code=$r.Code;canonicalSha256=$digest;randomState=$after.RandomState;admissionCount=1;
        drawRandomAfter=$after.Reinforcement.Admission.Draw.RandomAfter})
}

[ordered]@{
    status='PASS';schema=87;authority='TEST_ONLY';controls=$controls;
    admittedSaveSha256=Hash-Bytes $admittedBytes;closedSaveSha256=Hash-Bytes $closedBytes;
    assemblies=@($assemblies | ForEach-Object { [ordered]@{name=Split-Path $_ -Leaf;
        sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()} })
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
"PASS: $($controls.Count) isolated schema 87 provenance and command-id controls."
