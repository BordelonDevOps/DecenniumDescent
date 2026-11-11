param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$PlanSave,
    [Parameter(Mandatory)][string]$PreparedSave,
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
function New-PositivePolicy {
    $profile=[Decennium.Foundation.Laboratory.TestOnlyNextCharterPlanProfile]::new($true,$true,$true,$true,$true,$false,0,48000,$true)
    Invoke-CaseHelper 'PlanPolicy' @($profile,$null,$null)
}
function Get-Digest([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function ObservationRow($Observation) {
    [ordered]@{
        time=$Observation.At.ToString()
        revision=$Observation.Revision
        walkable=$Observation.Walkable
        occupied=$Observation.Occupied
        pathReserved=$Observation.PathReserved
        tacticalTransition=$Observation.TacticalTransition
        approachAccess=$Observation.ApproachAccess
        scoutCapable=$Observation.ScoutCapable
        scoutAtStage=$Observation.ScoutAtStage
        carriedPounds=$Observation.ActualPounds.ToString()
        canCarry=$Observation.CanCarry
        pressure=$Observation.Pressure
        strain=$Observation.Strain
        restDebt=$Observation.RestDebt
        widerObligationsResolved=$Observation.WiderObligationsResolved
        hazardSafetyEstablished=$Observation.HazardSafetyEstablished
        charterAccepted=$Observation.CharterAccepted
        departurePermitted=$Observation.DeparturePermitted
        supplies=@($Observation.Supplies | ForEach-Object {
            [ordered]@{
                root=$_.RootId
                vessel=$_.VesselId
                required=$_.Required.ToString()
                eligible=$_.EligibleAvailable.ToString()
                accessible=$_.AccessibleAvailable.ToString()
                ready=$_.ReadyAvailable.ToString()
            }
        })
    }
}
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$saves=[Decennium.Foundation.FileSaveStore]::new()
$planPath=(Resolve-Path -LiteralPath $PlanSave).Path
$planBytes=[IO.File]::ReadAllBytes($planPath)
$hero=[Decennium.Foundation.Laboratory.TestOnlyNextCharterPlanProfile]::PlannerId
$companion=[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$hostAuthority=Invoke-CaseHelper 'HavenSaleHost' @()
$planner=[Decennium.Foundation.Authority]::new($hostAuthority.Principal,[string[]]@($hero))
$starting=$null
$ending=$null
$firstAfterHash=$null
$roundtripHash=$null
for($runNumber=1;$runNumber -le 2;$runNumber++){
    $simulation=[Decennium.Foundation.Simulation]::new((New-PositivePolicy),$saves.Load($planPath),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $initial=$simulation.Capture()
    if($initial.SchemaVersion -ne 83 -or (Get-Digest ($codec.Encode($initial))) -ne (Get-Digest $planBytes)){throw 'The authentic accepted plan did not roundtrip.'}
    $startReport=$initial.NextCharterPlans[0].Report
    $startObservation=Invoke-CaseHelper 'InspectPlan' @($simulation,$planner)
    if(!$startObservation.Occupied -or $startObservation.ActualPounds.ToString() -ne '68/1'){throw 'The accepted carried plan lacked its actual occupied approach or mass.'}

    Invoke-CaseHelper 'PlanWalk' @($simulation,-1,0,$hero)
    Invoke-CaseHelper 'PlanWalk' @($simulation,1,0,$companion)
    Invoke-CaseHelper 'PlanWalk' @($simulation,1,0,$hero)
    foreach($item in @([Decennium.Foundation.Laboratory.PortableKitFixture]::Rations,[Decennium.Foundation.Laboratory.PortableKitFixture]::Skin)){
        $retrieve=Invoke-CaseHelper 'Portable' @($simulation,[Decennium.Foundation.CommandKind]::HandlePortableEquipment,$item,'',[Decennium.Foundation.HandlingKind]::Retrieve,$hero)
        Invoke-CaseHelper 'PortableCommit' @($simulation,$retrieve)
        Invoke-CaseHelper 'WorldAdvance' @($simulation,6,1)
    }
    $current=Invoke-CaseHelper 'InspectPlan' @($simulation,$planner)
    $state=$simulation.Capture()
    if(!$current.Walkable -or $current.Occupied -or $current.PathReserved -or $current.TacticalTransition -or $current.ApproachAccess -ne $true -or !$current.ScoutAtStage -or !$current.ScoutCapable -or $current.CanCarry -ne $true -or $current.ActualPounds.ToString() -ne '68/1'){throw 'The ordinary preparation did not produce the expected current represented access and burden facts.'}
    if(($current.Supplies | Where-Object { $_.ReadyAvailable -lt $_.Required }).Count -ne 0){throw 'The actual physical allocations still require preparation.'}
    if($current.CharterAccepted -or $current.DeparturePermitted -or $null -ne $current.Pressure -or $null -ne $current.Strain -or $null -ne $current.RestDebt -or $current.WiderObligationsResolved -or $current.HazardSafetyEstablished -or ![object]::ReferenceEquals($startReport,$state.NextCharterPlans[0].Report)){throw 'Preparation changed historical or unresolved authority.'}
    $afterHash=Get-Digest ($codec.Encode($state))
    if($runNumber -eq 1){
        $starting=ObservationRow $startObservation
        $ending=ObservationRow $current
        $firstAfterHash=$afterHash
        $savePath=[IO.Path]::GetFullPath($PreparedSave)
        $saves.Save($savePath,$state)
        $restored=[Decennium.Foundation.Simulation]::new((New-PositivePolicy),$saves.Load($savePath),[Decennium.Foundation.ExecutionProfile]::Laboratory)
        $roundtripHash=Get-Digest ($codec.Encode($restored.Capture()))
    } elseif($afterHash -ne $firstAfterHash -or $roundtripHash -ne $firstAfterHash){
        throw 'Ordinary preparation or roundtrip diverged.'
    }
}
[ordered]@{
    status='PASS'
    authority='Accepted schema83 TEST_ONLY ordinary preparation baseline'
    schema=83
    baselineSha256=(Get-Digest $planBytes)
    preparedSha256=$firstAfterHash
    roundtripSha256=$roundtripHash
    identicalPreparationReplay=$true
    starting=$starting
    prepared=$ending
    assemblyHashes=@($assemblies | ForEach-Object { @{name=(Split-Path -Leaf $_);sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()} })
} | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath $ReportPath -Encoding utf8
'PASS: actual ordinary preparation and roundtrip reproduce the existing schema83 plan baseline.'
