param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$AcceptedSave,
    [Parameter(Mandatory)][string]$ReturnedSave,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference='Stop'
$assemblies=@('Core','Persistence','LabModel','HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$type=[Decennium.Foundation.Tests.FoundationCases]
$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Invoke-CaseHelper([string]$Name,[object[]]$Arguments) {
    $type.GetMethod($Name,$flags).Invoke($null,$Arguments)
}
function New-AgreementPolicy {
    $planning=[Decennium.Foundation.Laboratory.TestOnlyNextCharterPlanProfile]::new($true,$true,$true,$true,$true,$false,0,12000,$true)
    Invoke-CaseHelper 'AgreementPolicy' @($null,$planning,$null)
}
function Get-Digest([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Waypoint($Snapshot,[string]$Actor) {
    $position=$Snapshot.Actors | Where-Object Id -EQ $Actor
    $edge=$Snapshot.WorldTraversals | Where-Object ActorId -EQ $Actor
    [ordered]@{
        at=$Snapshot.RuleClock.ToString()
        revision=$Snapshot.Revision
        x=$position.X
        y=$position.Y
        traversalRevision=$edge.StartedRevision
        partialFeet=if($edge){$edge.DistanceFeet.ToString()}else{$null}
    }
}
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$saves=[Decennium.Foundation.FileSaveStore]::new()
$path=(Resolve-Path -LiteralPath $AcceptedSave).Path
$inputDigest=Get-Digest ([IO.File]::ReadAllBytes($path))
$hero=[Decennium.Foundation.Laboratory.TestOnlyNextCharterPlanProfile]::PlannerId
$report=$null
for($iteration=1;$iteration -le 2;$iteration++){
    $sim=[Decennium.Foundation.Simulation]::new((New-AgreementPolicy),$saves.Load($path),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $before=$sim.Capture()
    if($before.SchemaVersion -ne 84 -or (Get-Digest ($codec.Encode($before))) -ne $inputDigest){throw 'The authentic accepted charter did not roundtrip.'}
    $agreement=$before.NextCharterAgreement
    if(!$agreement -or $agreement.AcceptedAt.ToString() -ne '12000/1'){throw 'The actual accepted charter was absent.'}
    Invoke-CaseHelper 'WorldAdvance' @($sim,6,1)
    $staging=$sim.Capture()
    if($staging.WorldTraversals.Length -ne 0){throw 'The companion still occupied the shared traversal path.'}
    $speed=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::WalkingSpeed($staging,$hero)
    if($speed -ne 20){throw 'The actual burden-adjusted walking speed changed.'}
    Invoke-CaseHelper 'WorldStep' @($sim,1,0,$false,$hero)
    Invoke-CaseHelper 'WorldAdvance' @($sim,1,2)
    $partial=Waypoint ($sim.Capture()) $hero
    if($partial.partialFeet -ne '5/3'){throw 'Partial ordinary traversal did not retain its exact distance.'}
    Invoke-CaseHelper 'WorldAdvance' @($sim,1,1)
    $arrived=$sim.Capture()
    $arrival=Waypoint $arrived $hero
    if($arrival.x -ne 3 -or $arrival.y -ne 3 -or $arrival.partialFeet){throw 'The ordinary outbound traversal did not complete at its actual destination.'}
    Invoke-CaseHelper 'WorldStep' @($sim,-1,0,$false,$hero)
    Invoke-CaseHelper 'WorldAdvance' @($sim,3,2)
    $after=$sim.Capture()
    $returned=Waypoint $after $hero
    if($returned.x -ne 2 -or $returned.y -ne 3 -or $returned.partialFeet -or $after.RuleClock -ne $staging.RuleClock.AddSeconds(3)){
        throw 'The ordinary return or exact aggregate movement time diverged.'
    }
    if(![object]::ReferenceEquals($agreement,$after.NextCharterAgreement) -or $after.RandomState -ne $before.RandomState){
        throw 'Ordinary movement rewrote the agreement or consumed RNG.'
    }
    $digest=Get-Digest ($codec.Encode($after))
    if($iteration -eq 1){
        $returnedPath=[IO.Path]::GetFullPath($ReturnedSave)
        $saves.Save($returnedPath,$after)
        $restored=[Decennium.Foundation.Simulation]::new((New-AgreementPolicy),$saves.Load($returnedPath),[Decennium.Foundation.ExecutionProfile]::Laboratory)
        $report=[ordered]@{
            status='PASS'
            authority='Accepted schema84 TEST_ONLY ordinary movement baseline'
            schema=84
            acceptedSha256=$inputDigest
            returnedSha256=$digest
            roundtripSha256=(Get-Digest ($codec.Encode($restored.Capture())))
            identicalReplay=$true
            charterBoundExecutionRecorded=$false
            ordinaryWalkingSpeedFeet=$speed
            staging=(Waypoint $staging $hero)
            partialOutbound=$partial
            outboundArrival=$arrival
            returned=$returned
            assemblyHashes=@($assemblies | ForEach-Object { @{name=(Split-Path -Leaf $_);sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()} })
        }
    } elseif($digest -ne $report.returnedSha256 -or $digest -ne $report.roundtripSha256){
        throw 'Ordinary movement or restored continuation diverged.'
    }
}
$report | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath $ReportPath -Encoding utf8
'PASS: actual ordinary movement traversed both directions and reproduced the returned schema84 bytes.'
