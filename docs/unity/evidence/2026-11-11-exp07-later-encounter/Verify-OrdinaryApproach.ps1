param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ContinuedSave,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core','Persistence','LabModel','HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$caseType = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Invoke-Fixture([string]$Name,[object[]]$Arguments) {
    $caseType.GetMethod($Name,$flags).Invoke($null,$Arguments)
}
function New-Policy { Invoke-Fixture 'AttemptPolicy' @($null,$null,$null) }
function Assert-True([bool]$Condition,[string]$Message) {
    if(-not $Condition){ throw $Message }
}
function Digest([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Read-Position($State,[string]$Actor) {
    $position = [Decennium.Foundation.WorldPositionResolver]::Position($State,$Actor)
    $edge = $State.WorldTraversals | Where-Object ActorId -EQ $Actor
    $ledger = $State.WorldIntervals | Where-Object ActorId -EQ $Actor
    [ordered]@{
        clock = $State.RuleClock.ToString()
        revision = $State.Revision
        x = $position.Item1.ToString()
        y = $position.Item2.ToString()
        slot = $State.WorldSchedule.ProcessedSlot
        movementSpent = $ledger.MovementSpent.ToString()
        actionSpent = $ledger.ActionSpent
        reactionAvailable = $ledger.ReactionAvailable
        partialFeet = if($edge){$edge.DistanceFeet.ToString()}else{$null}
        tactical = $State.InventoryCombat
    }
}
function Compare-Scope($State) {
    @($State.Actors | Where-Object { ($_.X -eq 0 -and $_.Y -eq 4) -or ($_.X -eq 0 -and $_.Y -eq 3) })
}
$store = [Decennium.Foundation.FileSaveStore]::new()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$savePath = (Resolve-Path -LiteralPath $ContinuedSave).Path
$baseline = $store.Load($savePath)
$hero = $baseline.CharterAttempt.Authority.HeroId
$deadId = $baseline.Encounter.Order | Where-Object { $_ -ne $hero }
$baselineDigest = Digest ($codec.Encode($baseline))
Assert-True ($baseline.SchemaVersion -eq 85 -and -not $baseline.InventoryCombat -and
    $baseline.CharterAttempt.Outcome.ToString() -eq 'ReturnedComplete' -and
    ($baseline.Lives | Where-Object ActorId -EQ $deadId).Dead) 'Expected the authentic continued schema 85 state.'

$replayPolicy = New-Policy
$replay = [Decennium.Foundation.Simulation]::new($replayPolicy,$replayPolicy.Initial(),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$hostAuthority = Invoke-Fixture 'HavenSaleHost' @()
$earlierScopeVisits = [Collections.Generic.List[object]]::new()
$previousExit = $null
foreach($receipt in ($baseline.Receipts | Sort-Object Revision)){
    $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
    Assert-True ($receipt.Principal -eq $hostAuthority.Principal) 'Unexpected principal in the authentic history.'
    $before = $replay.Capture()
    $result = $replay.Execute($hostAuthority,$command)
    Assert-True ($result.Outcome.ToString() -eq 'Committed') "$($receipt.Id) failed: $($result.Code)"
    $after = $replay.Capture()
    foreach($actor in (Compare-Scope $after)){
        $earlierScopeVisits.Add([ordered]@{revision=$after.Revision;actor=$actor.Id;x=$actor.X;y=$actor.Y})
    }
    if($command.Kind.ToString() -eq 'EndFixedEncounter'){
        Assert-True ($null -eq $previousExit -and $before.InventoryCombat -and -not $after.InventoryCombat) 'Unexpected encounter exit history.'
        $previousExit = [ordered]@{
            encounter = $before.Encounter.Id
            revision = $after.Revision
            clock = $after.RuleClock.ToString()
            outgoingOrdinal = $before.Encounter.TurnOrdinal
            retainedOrdinalAtExit = $after.Encounter.TurnOrdinal
            retainedLastStartRevisionAtExit = $after.Encounter.StartRevisions[$after.Encounter.StartRevisions.Count - 1]
            receipt = $receipt.Id
        }
    }
}
Assert-True ((Digest ($codec.Encode($replay.Capture()))) -eq $baselineDigest) 'Actual receipt replay did not reproduce the accepted save.'
Assert-True ($null -ne $previousExit) 'The baseline did not prove the earlier exit.'

$waypoints = @()
$finalDigest = ''
for($i=0;$i -lt 2;$i++){
    $sim = [Decennium.Foundation.Simulation]::new((New-Policy),$store.Load($savePath),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $start = Read-Position ($sim.Capture()) $hero
    Invoke-Fixture 'WorldStep' @($sim,-1,0,$false,$hero)
    $entered = Read-Position ($sim.Capture()) $hero
    Invoke-Fixture 'WorldAdvance' @($sim,1,2)
    $partial = Read-Position ($sim.Capture()) $hero
    Invoke-Fixture 'WorldAdvance' @($sim,1,1)
    $final = $sim.Capture()
    $arrived = Read-Position $final $hero
    Assert-True ($start.x -eq '1/1' -and $start.y -eq '3/1' -and $partial.x -eq '2/3' -and
        $partial.partialFeet -eq '5/3' -and $arrived.x -eq '0/1' -and $arrived.y -eq '3/1' -and -not $arrived.tactical) 'Ordinary approach geometry or expenditure changed.'
    Assert-True ($final.Encounter.Id -eq $baseline.Encounter.Id -and $final.ClosedEncounters.Count -eq 0 -and
        $final.CharterAttempt.Returned.Revision -eq $baseline.CharterAttempt.Returned.Revision -and
        $final.RandomState -eq $baseline.RandomState) 'The ordinary baseline manufactured a later encounter or rewrote history.'
    $digest = Digest ($codec.Encode($final))
    if($i -eq 0){ $finalDigest = $digest; $waypoints = @($start,$entered,$partial,$arrived) }
    else { Assert-True ($digest -eq $finalDigest) 'Exact continuation replay diverged.' }
}
[ordered]@{
    status = 'PASS'
    authority = 'Accepted TEST_ONLY schema85 ordinary continuation baseline'
    schema = $baseline.SchemaVersion
    originalSaveSha256 = Digest ([IO.File]::ReadAllBytes($savePath))
    authenticReceiptReplaySha256 = $baselineDigest
    repeatedOrdinaryApproachSha256 = $finalDigest
    priorActualExit = $previousExit
    priorOpponent = $deadId
    laterOpponentExists = $false
    earlierAnchorVisitsToProposedCells = $earlierScopeVisits.ToArray()
    proposedThreshold = @(0,3)
    proposedOpponentCell = @(0,4)
    waypoints = $waypoints
    assemblies = @($assemblies | ForEach-Object {
        [ordered]@{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
