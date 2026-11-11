param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ClosedSave,
    [Parameter(Mandatory)][string]$EnteredSave,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core','Persistence','LabModel','HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$cases = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Invoke-Fixture([string]$Name,[object[]]$Arguments) {
    $cases.GetMethod($Name,$flags).Invoke($null,$Arguments)
}
function Assert-True([bool]$Condition,[string]$Message) {
    if(-not $Condition){throw $Message}
}
function Hash-Bytes([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Waypoint($State,[string]$Actor) {
    $point=[Decennium.Foundation.WorldPositionResolver]::Position($State,$Actor)
    $edge=$State.WorldTraversals | Where-Object ActorId -EQ $Actor
    $crop=$State.Crops | ForEach-Object Tasks | Where-Object WorkerId -EQ $Actor
    [ordered]@{
        at=$State.RuleClock.ToString()
        revision=$State.Revision
        x=$point.Item1.ToString()
        y=$point.Item2.ToString()
        partialFeet=if($edge){$edge.DistanceFeet.ToString()}else{$null}
        cropStatus=if($crop){$crop.Status.ToString()}else{$null}
        cropProgress=if($crop){$crop.Progress.ToString()}else{$null}
    }
}
function End-ActualTurn($Simulation) {
    Invoke-Fixture 'LaterStance' @($Simulation,[Decennium.Foundation.CombatStance]::Guarded)
    $state=$Simulation.Capture()
    $command=[Decennium.Foundation.Command]::new("reinforcement.baseline.end.$($state.Revision)",
        $state.Encounter.CurrentActor,$state.Revision,[Decennium.Foundation.CommandKind]::EndRegularTurn,
        $state.Encounter.CurrentTurnId)
    $result=$Simulation.Execute($hostAuthority,$command)
    Assert-True ($result.Outcome.ToString() -eq 'Committed') "Turn failed: $($result.Code)"
}

$hostAuthority = Invoke-Fixture 'LaterHost' @()
$store=[Decennium.Foundation.FileSaveStore]::new()
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$companion=[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId

$prepared=Invoke-Fixture 'LaterPrepared' @($null)
$before=Waypoint ($prepared.Capture()) $companion
Invoke-Fixture 'PlanWalk' @($prepared,-1,0,$companion)
Invoke-Fixture 'FarmWork' @($prepared,[Decennium.Foundation.CommandKind]::PlantCrop,'TEST_ONLY.crop')
Invoke-Fixture 'WorldAdvance' @($prepared,2,1)
Invoke-Fixture 'FarmWork' @($prepared,[Decennium.Foundation.CommandKind]::PauseCrop,'TEST_ONLY.crop')
$paused=Waypoint ($prepared.Capture()) $companion
Invoke-Fixture 'PlanWalk' @($prepared,-1,0,$companion)
$staged=Waypoint ($prepared.Capture()) $companion
Assert-True ($staged.x -eq '2/1' -and $staged.y -eq '3/1' -and $staged.cropStatus -eq 'Paused' -and
    $staged.cropProgress -eq '2/1') 'Expected real companion staging and paused work.'
$entry=Invoke-Fixture 'EnterLater' @($prepared)
$state=$prepared.Capture()
$club=$state.Clubs | Where-Object OwnerId -EQ $companion
$burden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($state,$companion)
$speed=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::WalkingSpeed($state,$companion)
$command=[Decennium.Foundation.Command]::new("reinforcement.baseline.approach",$companion,$state.Revision,
    [Decennium.Foundation.CommandKind]::BeginWorldStep,"walk",-1,0)
$beforeDigest=Hash-Bytes ($codec.Encode($state))
$query=$prepared.QueryCommand($hostAuthority,$command)
$refused=$prepared.Execute($hostAuthority,$command)
Assert-True ($refused.Outcome.ToString() -eq 'Rejected' -and
    (Hash-Bytes ($codec.Encode($prepared.Capture()))) -eq $beforeDigest) 'The accepted profile unexpectedly changed state during off-roster tactical travel.'
$fullEntered=[IO.Path]::GetFullPath($EnteredSave)
$store.Save($fullEntered,$state)
$restorePolicy=Invoke-Fixture 'LaterPolicy' @($null,$null)
$restored=[Decennium.Foundation.Simulation]::new($restorePolicy,$store.Load($fullEntered),[Decennium.Foundation.ExecutionProfile]::Laboratory)
Assert-True ((Hash-Bytes ($codec.Encode($restored.Capture()))) -eq $beforeDigest) 'Entered staging save changed on restore.'

End-ActualTurn $prepared
$next=Waypoint ($prepared.Capture()) $companion
End-ActualTurn $prepared
$round=Waypoint ($prepared.Capture()) $companion
Assert-True ($prepared.Capture().Encounter.Round -eq 2 -and $prepared.Capture().Encounter.Id -eq $state.Encounter.Id -and
    $next.cropProgress -eq '2/1' -and $round.cropProgress -eq '2/1') 'Accepted end-round or paused work changed.'

$closedPath=(Resolve-Path -LiteralPath $ClosedSave).Path
$closedPolicy=Invoke-Fixture 'LaterPolicy' @($null,$null)
$ordinary=[Decennium.Foundation.Simulation]::new($closedPolicy,$store.Load($closedPath),[Decennium.Foundation.ExecutionProfile]::Laboratory)
Invoke-Fixture 'PlanWalk' @($ordinary,-1,0,$companion)
Invoke-Fixture 'PlanWalk' @($ordinary,-1,0,$companion)
$ordinaryStart=Waypoint ($ordinary.Capture()) $companion
Invoke-Fixture 'WorldStep' @($ordinary,-1,0,$false,$companion)
Invoke-Fixture 'WorldAdvance' @($ordinary,1,2)
$ordinaryPartial=Waypoint ($ordinary.Capture()) $companion
Invoke-Fixture 'WorldAdvance' @($ordinary,1,2)
$ordinaryArrival=Waypoint ($ordinary.Capture()) $companion
Assert-True ($ordinaryStart.x -eq '2/1' -and $ordinaryPartial.x -eq '3/2' -and
    $ordinaryPartial.partialFeet -eq '5/2' -and $ordinaryArrival.x -eq '1/1' -and
    -not $ordinary.Capture().InventoryCombat) 'The existing ordinary edge or fractional arrival changed.'

[ordered]@{
    status='PASS'
    authority='Accepted TEST_ONLY schema86 reinforcement gap and exact approach baseline'
    schema=$state.SchemaVersion
    actualCompanion=$companion
    actualSpeed=$speed
    actualLoadPounds=if($burden.Pounds){$burden.Pounds.ToString()}else{$null}
    actualClub=[ordered]@{id=$club.Id;heldBy=$club.HeldBy;owner=$club.OwnerId;custodian=$club.CustodianId;x=$club.CellX;y=$club.CellY}
    beforePlanting=$before
    pausedAtPlot=$paused
    staged=$staged
    activeEncounter=$state.Encounter.Id
    entry=$entry.Epoch.Origin.ToString()
    order=@($entry.Epoch.Order)
    retainedRoundWaypoints=@($next,$round)
    commandRejection=$refused.Code
    queryResult=$query.Code
    rejectedCommandPreservedBytes=$true
    enteredSaveSha256=Hash-Bytes ([IO.File]::ReadAllBytes($fullEntered))
    enteredRoundtripSha256=$beforeDigest
    acceptedClosedSaveSha256=Hash-Bytes ([IO.File]::ReadAllBytes($closedPath))
    ordinaryApproach=@($ordinaryStart,$ordinaryPartial,$ordinaryArrival)
    assemblies=@($assemblies | ForEach-Object {
        [ordered]@{ name=Split-Path $_ -Leaf; sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
