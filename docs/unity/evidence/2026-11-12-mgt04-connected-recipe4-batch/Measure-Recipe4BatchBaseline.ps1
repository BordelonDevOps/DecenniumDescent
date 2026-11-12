param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
$accepted = Join-Path $PSScriptRoot '../2026-11-12-mgt05-black-blood-handoff'
$bindings = Get-Content (Join-Path $accepted 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
if ($bindings.implementationCommit -cne '246ca4e4899469241402899ba6750d4379d035a9' -or $bindings.unfilteredCases -ne 1470) {
    throw 'The accepted corrected wire 94 checkpoint is required.'
}
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $relative = "focused/assemblies/Decennium.Foundation.$name.dll"
    $path = Join-Path $accepted $relative
    if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $bindings.artifacts[$relative].sha256) {
        throw "Wrong accepted assembly $name"
    }
    Add-Type -Path $path
}
$save = 'focused/saves/mgt05-connected-blood-cutoff.ddsave'
$path = Join-Path $accepted $save
$bytes = [IO.File]::ReadAllBytes($path)
if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $bindings.artifacts[$save].sha256) {
    throw 'Wrong accepted cutoff save.'
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$argsIn = [object[]]::new(1)
$argsIn[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$policy = $tests.GetMethod('ConnectedObservationPolicy',$flags).Invoke($null,$argsIn).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
$hostAuthority = $tests.GetMethod('LaterHost',$flags).Invoke($null,@())
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$sim = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$state = $sim.Capture()
$worker = [Decennium.Foundation.ConnectedBloodSpecimen]::Worker
$specimen = $state.BloodSpecimen
$recipe = [Decennium.Foundation.Laboratory.ManufacturingRules]::Recipe('recipe-4')
$assay = $policy.AssessRecipe4Specimen($state,$hostAuthority,$worker,$specimen.LotId,0,2)
$old = [Decennium.Foundation.Command]::new('baseline.recipe4.batch',$worker,$state.Revision,
    [Decennium.Foundation.CommandKind]::StartManufacturing,$recipe.Id,0,2)
$denial = $sim.QueryCommand($hostAuthority,$old)
if ($state.WireSchemaVersion -ne 94 -or !$assay.Item1 -or $denial.Admissible -or $denial.Code -cne 'ManufacturingIngredientSpoiled' -or
    $state.ManufacturingOrders.Length -ne 0 -or $state.AlchemyDoses.Length -ne 0) { throw 'Unexpected accepted assessment or fixed-stock behavior.' }
$facts = [Decennium.Foundation.Laboratory.CharacterStateFacts]::ForActor($state,$worker)
$intelligence = [Decennium.Foundation.CharacterAbility]::Intelligence
$modifier = $facts.Rules.AbilityModifier($intelligence) + $facts.Rules.ProficiencyBonus + $facts.InjuryPenalty($intelligence,$true)
$next = [Decennium.Foundation.DiceStream]::Draw($state.RandomState,20)
$total = $recipe.FirstPhase.Numerator + $recipe.RemainingPhase.Numerator
$expected = [Decennium.Foundation.Laboratory.ManufacturingRules]::Quality($next.Value+1,$modifier,$recipe.Difficulty,$false)
@{
    status='PASS'; sourceSaveSha256=$bindings.artifacts[$save].sha256; sourceWire=$state.WireSchemaVersion
    cutoff=$state.RuleClock.ToString(); actor=$worker; lot=$specimen.LotId; selectedOriginalSet=0; requestedSupplementaryVials=2
    specimenAssessment=$assay.Item2; unprotectedAge=$assay.Item3.ToString(); conditionalFirstPhaseAge=$assay.Item4.ToString()
    fixedStockRejection=$denial.Code; actualManufacturingOrders=0; actualDoses=0
    conditional=@{phaseAt=$state.RuleClock.AddSeconds($recipe.FirstPhase.Numerator).ToString()
        fullLaborAt=$state.RuleClock.AddSeconds($total).ToString(); currentRng=$state.RandomState
        nextNaturalWithoutInterveningDraw=$next.Value+1; currentIntelligenceToolModifier=$modifier
        qualityIfFactsAndRngAreUnchanged=$expected.ToString()}
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
