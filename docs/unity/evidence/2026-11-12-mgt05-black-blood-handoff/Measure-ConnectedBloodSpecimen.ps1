param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SaveRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$argsIn = [object[]]::new(1)
$argsIn[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$policy = $tests.GetMethod('ConnectedObservationPolicy',$flags).Invoke($null,$argsIn).
    EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
$hostAuthority = $tests.GetMethod('LaterHost',$flags).Invoke($null,@())
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
$rows = @(foreach ($file in Get-ChildItem -LiteralPath $SaveRoot -Recurse -Filter 'mgt05-connected-blood-*.ddsave') {
    $bytes = [IO.File]::ReadAllBytes($file.FullName)
    $simulation = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),$profile)
    $state = $simulation.Capture()
    $digest = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    $reencoded = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($state))).ToLowerInvariant()
    if ($digest -cne $reencoded) { throw "Re-encoding changed $($file.Name)" }
    $binding = $state.BloodSpecimen
    $view = $null
    if (![Decennium.Foundation.HarvestPreservationRules]::TryProject($state,$binding.LotId,[ref]$view)) {
        throw "Missing specimen age for $($file.Name)"
    }
    $treated = $state.HarvestPreservationTreatmentAttempts[0]
    $supply = $state.Work.Reservations | Where-Object Id -ceq $treated.SupplyReservationId
    $vessel = $state.PortableEquipment | Where-Object Id -ceq $binding.VesselId
    $open = $state.HarvestPreservationEvidence | Select-Object -Last 1
    $research = $state.FormulaWork | Select-Object -Last 1
    $assay = $policy.AssessRecipe4Specimen($state,$hostAuthority,[Decennium.Foundation.ConnectedBloodSpecimen]::Worker,$binding.LotId,0,0)
    [ordered]@{
        save=$file.Name; sha256=$digest; wire=$state.WireSchemaVersion; base=$state.SchemaVersion
        revision=$state.Revision; time=$state.RuleClock.ToString(); rng=$state.RandomState
        lot=$binding.LotId; origin=$binding.Origin.ToString(); amount=($state.Work.Lots | Where-Object Id -ceq $binding.LotId).Amount.ToString()
        attempt=$treated.Status.ToString(); labor=$treated.Work.Labor.ToString(); natural=$treated.Natural
        ability=$treated.AbilityModifier; proficiency=$treated.ProficiencyBonus; sealedAt=$treated.SealedAt?.ToString()
        supplyConsumed=$supply.ConsumedAmount.ToString()
        vesselPlacement=$vessel.Placement.ToString(); groundX=$vessel.GroundX; groundY=$vessel.GroundY; vesselOpen=$vessel.Open
        opening=if ($open) {$open.At.ToString()}; openingLimit=if ($open) {$open.At.AddSeconds(60).ToString()}
        protected=[Decennium.Foundation.HarvestPreservationRules]::IsProtectedAt($state,$binding.LotId,$state.RuleClock)
        unprotectedAge=$view.UnprotectedAge.ToString(); preservationState=$view.State.ToString()
        research=if ($research) {$research.Status.ToString()}; eligibility=$assay.Item2; eligible=$assay.Item1
        eligibilityCurrentAge=$assay.Item3?.ToString(); firstPhaseAge=$assay.Item4?.ToString()
        manufacturingOrders=$state.ManufacturingOrders.Length
        tactical=$state.InventoryCombat; laterEntry=if ($state.LaterEncounter.Entry) {$state.LaterEncounter.Entry.Epoch.Origin.ToString()}
    }
})
if ($rows.Count -ne 10 -or @($rows.save | Sort-Object -Unique).Count -ne 10) {
    throw 'Expected ten distinct connected wire 94 saves.'
}
@{status='PASS'; savedStates=$rows} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
