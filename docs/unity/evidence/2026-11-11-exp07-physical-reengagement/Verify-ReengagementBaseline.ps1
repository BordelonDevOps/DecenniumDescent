param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ContinuedSave,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core', 'Persistence', 'LabModel', 'HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{ name = (Split-Path -Leaf $path); sha256 = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
})
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Invoke-Fixture([string]$Name, [object[]]$Arguments) {
    try { $fixture.GetMethod($Name, $flags).Invoke($null, $Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Assert-True([bool]$Condition, [string]$Failure) {
    if (-not $Condition) { throw $Failure }
}
function Hash-Bytes([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $ContinuedSave).Path)
$policy = Invoke-Fixture 'RetreatPolicy' @($null, $null, $null)
$sim = [Decennium.Foundation.Simulation]::new($policy, $codec.Decode($bytes), [Decennium.Foundation.ExecutionProfile]::Laboratory)
$hostAuthority = Invoke-Fixture 'LaterHost' @()
$kinds = [Decennium.Foundation.CommandKind]
$before = $sim.Capture()
$d = $before.Retreat.Definition
function Read-Body($State, [string]$Actor) {
    $body = $State.Actors | Where-Object Id -CEQ $Actor
    $position = [Decennium.Foundation.WorldPositionResolver]::Position($State, $Actor)
    $life = $State.Lives | Where-Object ActorId -CEQ $Actor
    $interval = $State.WorldIntervals | Where-Object ActorId -CEQ $Actor
    [ordered]@{ actor = $Actor; cell = @($body.X, $body.Y); position = @($position.Item1.ToString(), $position.Item2.ToString());
        hp = $life.Hp; held = @($life.HeldItems); lastStart = $interval.LastStart; actionSpent = $interval.ActionSpent;
        dashPaid = $interval.DashPaid; movementSpent = $interval.MovementSpent.ToString();
        reactionAvailable = $interval.ReactionAvailable; interactions = $interval.Interactions }
}
function Read-State($State) {
    $phase = $State.Reinforcement.Admission.Phase
    [ordered]@{ clock = $State.RuleClock.ToString(); revision = $State.Revision; rng = $State.RandomState
        inventoryCombat = $State.InventoryCombat; body = @($d.LeadId, $d.CompanionId, $d.DefenderId | ForEach-Object { Read-Body $State $_ })
        phase = [ordered]@{ id = $phase.Epoch.Id; origin = $phase.Epoch.Origin.ToString(); order = @($phase.Epoch.Order)
            slot = $phase.Epoch.ProcessedSlot; originalOrdinal = $phase.GlobalTurn($phase.Epoch.ProcessedSlot)
            round = $phase.Round($phase.GlobalTurn($phase.Epoch.ProcessedSlot))
            nextMarker = $phase.Epoch.Start($phase.Epoch.ProcessedSlot + 1).ToString() }
        archive = @($State.ClosedEncounters | ForEach-Object {
            [ordered]@{ id = $_.Encounter.Id; revision = $_.ClosedRevision; at = $_.ClosedAt.ToString(); ordinal = $_.Encounter.TurnOrdinal } })
        pressure = [Decennium.Foundation.ExpeditionPressureRules]::Current($State, $d.CohortId)
        exposure = $State.ExpeditionPressureExposures[0].Id
        changes = @($State.ExpeditionPressureChanges | Where-Object Kind -EQ ([Decennium.Foundation.ExpeditionPressureChangeKind]::SuccessfulRetreat) | ForEach-Object SourceId)
    }
}
function Commit-Command($Command) {
    $result = $sim.Execute($hostAuthority, $Command)
    Assert-True ($result.Outcome.ToString() -eq 'Committed') "$($Command.Kind) failed with $($result.Code)"
    $result
}
function New-Step([string]$Id, [string]$Actor, [int]$Y, [string]$Mode = 'walk') {
    [Decennium.Foundation.Command]::new($Id, $Actor, $sim.Capture().Revision, $kinds::BeginWorldStep, $Mode, 0, $Y)
}
function Advance-Exact([int]$Numerator, [int]$Denominator) {
    $c = Invoke-Fixture 'LaterAdvance' @($sim, $Numerator, $Denominator)
    Commit-Command $c
}
Assert-True ($before.SchemaVersion -eq 88 -and $before.Retreat.SuccessfulExit -and -not $before.InventoryCombat -and
    (Hash-Bytes $codec.Encode($before)) -eq (Hash-Bytes $bytes)) 'Expected the exact accepted schema88 continuation'
$stagedStep = New-Step 'reengagement.baseline.companion.step' $d.CompanionId 1
$null = Commit-Command $stagedStep
$null = Advance-Exact 1 2
$overlap = $sim.Capture()
$beforeOverlap = Hash-Bytes $codec.Encode($overlap)
$unsupportedOverlap = $sim.Execute($hostAuthority, (New-Step 'reengagement.baseline.concurrent' $d.LeadId 1))
Assert-True ($unsupportedOverlap.Outcome.ToString() -eq 'Rejected' -and $unsupportedOverlap.Code -eq 'ConcurrentHostileTraversalUnsupported' -and
    $beforeOverlap -eq (Hash-Bytes $codec.Encode($sim.Capture()))) 'Expected unchanged concurrent approach rejection'
$null = Advance-Exact 1 2
$staged = $sim.Capture()
Assert-True (((Read-Body $staged $d.CompanionId).cell -join ',') -eq '1,2' -and $staged.WorldTraversals.Count -eq 0) 'Expected the companion at the actual staging cell'
$null = Advance-Exact 3 2
$approach = New-Step 'reengagement.baseline.hero.step' $d.LeadId 1
$null = Commit-Command $approach
$null = Advance-Exact 1 2
$halfway = $sim.Capture()
Assert-True ($halfway.WorldTraversals.Count -eq 1 -and -not $halfway.InventoryCombat) 'Expected the lead to remain on the physical approach'
$arrival = Advance-Exact 1 1
$reached = $sim.Capture()
$point = Read-Body $reached $d.LeadId
Assert-True ($point.cell -join ',' -eq '0,1') 'Lead did not physically reach the declared contact cell'
Assert-True (-not $reached.InventoryCombat -and -not $reached.Encounter -and -not $arrival.TacticalDecisionAt -and
    $reached.RandomState -eq $before.RandomState -and $reached.ExpeditionPressureChanges.Length -eq $before.ExpeditionPressureChanges.Length) 'Physical approach unexpectedly entered combat or changed RNG/Pressure'
$manual = [Decennium.Foundation.Command]::new('reengagement.baseline.old-entry', $d.LeadId, $reached.Revision, $kinds::BeginFixedEncounter)
$preHash = Hash-Bytes $codec.Encode($reached)
$denied = $sim.Execute($hostAuthority, $manual)
Assert-True ($denied.Outcome.ToString() -eq 'Rejected' -and $denied.Code -eq 'FixedConflictAlreadyResolved' -and
    $preHash -eq (Hash-Bytes $codec.Encode($sim.Capture()))) 'Existing entry did not reject byte-identically'
$occupied = $sim.Execute($hostAuthority, (New-Step 'reengagement.baseline.occupied' $d.LeadId 1))
Assert-True ($occupied.Outcome.ToString() -eq 'Rejected' -and $occupied.Code -eq 'Occupied' -and
    $preHash -eq (Hash-Bytes $codec.Encode($sim.Capture()))) 'The defender did not retain the occupied cell'
$spent = Invoke-Fixture 'RetreatPolicy' @($null, $null, $null)
$sim = [Decennium.Foundation.Simulation]::new($spent, $codec.Decode($bytes), [Decennium.Foundation.ExecutionProfile]::Laboratory)
$null = Commit-Command (New-Step 'reengagement.baseline.companion.dash' $d.CompanionId 1 'run')
$null = Advance-Exact 5 2
$null = Commit-Command (New-Step 'reengagement.baseline.hero.step.after-dash' $d.LeadId 1)
$null = Advance-Exact 3 2
$spentReached = $sim.Capture()
$companionSpent = Read-Body $spentReached $d.CompanionId
Assert-True ($companionSpent.actionSpent -and $companionSpent.dashPaid -and $companionSpent.lastStart -eq 26 -and
    $spentReached.RuleClock -eq $reached.RuleClock -and -not $spentReached.InventoryCombat) 'The real companion Dash did not carry to contact'
$visibility = [Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy].GetMethod('CanSee', $flags)
$mutual = $visibility.Invoke($null, @($reached, $d.LeadId, $d.DefenderId)) -and
    $visibility.Invoke($null, @($reached, $d.DefenderId, $d.LeadId))
Assert-True $mutual 'The current physical/condition visibility gate rejected mutual lead-defender sight'
[ordered]@{
    status = 'PASS'; scope = 'Accepted schema88 positive paid approach and unimplemented re-engagement'
    continuedSaveSha256 = (Hash-Bytes $bytes); approach = $approach.Id; staging = $stagedStep.Id
    start = (Read-State $before); overlap = (Read-State $overlap); staged = (Read-State $staged); halfway = (Read-State $halfway); reached = (Read-State $reached)
    arrivalCommand = $reached.Receipts[-1].Id; arrivalRevision = $reached.Revision; mutualVisibility = $mutual
    manualEntry = $denied.Code; occupiedDefenderCell = $occupied.Code; concurrentApproach = $unsupportedOverlap.Code
    unchangedAfterRejectionSha256 = $preHash; spentResourceBranch = (Read-State $spentReached); assemblies = $assemblies
} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8
