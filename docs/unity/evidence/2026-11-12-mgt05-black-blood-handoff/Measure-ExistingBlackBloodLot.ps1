$ErrorActionPreference = 'Stop'
$accepted = Join-Path $PSScriptRoot '../2026-11-12-mgt09-connected-formula-research/focused/assemblies'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $accepted "Decennium.Foundation.$name.dll")
}
$t = [Decennium.Foundation.Tests.FoundationCases]
$f = [Reflection.BindingFlags]'NonPublic,Static'
$recipe = [Decennium.Foundation.Laboratory.ManufacturingRules]::Recipe14Id
$lotId = [Decennium.Foundation.Laboratory.SharedManufacturingFixture]::Lot($recipe,0,2)
$policy = $t.GetMethod('Recipe14ManufacturePolicy',$f).Invoke($null,@([uint32]1,$null,$null))
$sim = $t.GetMethod('World',$f).Invoke($null,@($policy))
$start = $sim.Capture()
$lot = $start.Work.Lots | Where-Object Id -CEQ $lotId
$inventory = $start.InventoryLots | Where-Object LotId -CEQ $lotId
$startAge = $policy.BloodUnprotectedAge($start,$recipe,0)
$null = $t.GetMethod('WorldAdvance',$f).Invoke($null,@($sim,11584,1))
$elapsed = $sim.Capture()
$elapsedAge = $policy.BloodUnprotectedAge($elapsed,$recipe,0)
if ($lotId -cne 'manufacture.recipe14.set0.component2' -or $lot.UnitId -cne 'drop-black_blood_sample' -or
    $lot.Amount.ToString() -cne '1/1' -or $inventory.OwnerId -cne $lot.CustodianId -or
    $startAge.ToString() -cne '0/1' -or $elapsedAge.ToString() -cne '11584/1') {
    throw 'The prior finite recipe-14 profile differs from the source/API baseline.'
}
[ordered]@{
    scope = 'Existing standalone TEST_ONLY stock baseline. It supplies no connected preservation or portability.'
    policyFingerprint = $start.ContentFingerprint
    wire = $start.WireSchemaVersion
    recipe = $recipe
    resource = [ordered]@{id=$lot.Id;unit=$lot.UnitId;amount=$lot.Amount.ToString();location=$lot.LocationId;custodian=$lot.CustodianId}
    inventory = [ordered]@{owner=$inventory.OwnerId;access=$inventory.Access.ToString();created=$inventory.CreatedAt.ToString()
        portableLinkCount=@($start.PortableEquipment | Where-Object LinkedId -CEQ $lotId).Count}
    age = [ordered]@{atOrigin=$startAge.ToString();atElapsed=$elapsed.RuleClock.ToString();unprotected=$elapsedAge.ToString()}
    completedProtection = $elapsed.HarvestPreservationTreatmentAttempts.Count
} | ConvertTo-Json -Depth 8
