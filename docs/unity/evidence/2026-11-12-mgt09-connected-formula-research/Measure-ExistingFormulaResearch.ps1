$ErrorActionPreference='Stop'
$d=Join-Path $PSScriptRoot '../2026-11-11-exp04-connected-observation'
foreach ($n in 'Core','Persistence','LabModel','HeadlessTests') { Add-Type -Path "$d/focused/assemblies/Decennium.Foundation.$n.dll" }
$t=[Decennium.Foundation.Tests.FoundationCases]
$f=[Reflection.BindingFlags]'NonPublic,Static'
function Call([string]$Name,[object[]]$ArgsIn) {
 try { $t.GetMethod($Name,$f).Invoke($null,$ArgsIn) } catch { throw $_.Exception.GetBaseException() }
}
$companion=[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$kind=[Decennium.Foundation.CommandKind]
$researcher=[Decennium.Foundation.Laboratory.SharedResearchFixture]

$codec=[Decennium.Foundation.SnapshotCodec]::new()
$auth=Call 'LaterHost' @()
$arguments=[object[]]::new(1)
$arguments[0]=[Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$oldPolicy=Call 'ConnectedObservationPolicy' $arguments
$connected=Call 'LaterPrepared' @($oldPolicy)
$null=Call 'PlanWalk' @($connected,-1,0,$companion)
$atSite=$connected.Capture()
$actor=$atSite.Actors | Where-Object Id -EQ $companion
$command=Call 'ResearchCommand' @($connected,$kind::StartFormulaResearch,$researcher::Evidence,0,$companion,$researcher::Recipe)
$oldQuery=$connected.QueryCommand($auth,$command).Code
$oldStart=$connected.Execute($auth,$command).Code
$manifest=[Decennium.Foundation.Laboratory.TestOnlyContentManifest]::CreateSelectedProfile()
$unknown=@($atSite.PortableEquipment | Where-Object {$null -eq $manifest.ResolveRuntime($_.ProfileId)} | Select-Object Id,ProfileId)
if ($atSite.RuleClock.ToString() -ne '11584/1' -or $actor.X -ne 3 -or $actor.Y -ne 3 -or
    $oldQuery -ne 'UnsupportedOperation' -or $oldStart -ne 'FormulaWorkNotSelected' -or $unknown.Count -lt 1) {
    throw 'Accepted expedition baseline changed.'
}
$seed=[uint32]1
while ([Decennium.Foundation.Laboratory.PlaytestDice]::RollD20($seed).Natural -ne 12) { $seed++ }
$kit=[Decennium.Foundation.Laboratory.PortableKitFixture]::new()
$combat=[Decennium.Foundation.Laboratory.SharedCombatFixture]::new(1,$seed,26)
$research=[Decennium.Foundation.Laboratory.SharedResearchFixture]::new()
$crafting=[Decennium.Foundation.Laboratory.SharedCraftingFixture]::new(26,26,5,$false,[Decennium.Foundation.Laboratory.CraftingMishapFact[]]@())
$repair=[Decennium.Foundation.Laboratory.SharedRepairFixture]::new()
$manufacture=[Decennium.Foundation.Laboratory.SharedManufacturingFixture]::new()
$cache=[Decennium.Foundation.Laboratory.SupplyCacheFixture]::new()
$terrain=[Decennium.Foundation.Laboratory.TacticalTerrainCell[]]@()
$p=[Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::new($manifest,$kit,$combat,$research,$crafting,$repair,$manufacture,$cache,30,$null,$terrain)
$null=$p.EnableMining([Decennium.Foundation.Laboratory.SharedMiningFixture]::new())
$null=$p.EnableHavenAppraisal([Decennium.Foundation.Laboratory.TestOnlyHavenAppraisalProfile]::new())
$null=$p.EnableHavenSale([Decennium.Foundation.Laboratory.TestOnlyHavenSaleProfile]::new())
$null=$p.EnableHavenMeal([Decennium.Foundation.Laboratory.TestOnlyHavenMealProfile]::new())
$null=$p.EnableExpeditionBill([Decennium.Foundation.Laboratory.TestOnlyExpeditionBillProfile]::new())
$null=$p.EnableExpeditionClose([Decennium.Foundation.Laboratory.TestOnlyExpeditionCloseProfile]::new())
$null=$p.EnableNextCharterPlan([Decennium.Foundation.Laboratory.TestOnlyNextCharterPlanProfile]::new($true,$true,$true,$true,$true,$false,0,48000,$true))
$null=$p.EnableNextCharterAgreement([Decennium.Foundation.Laboratory.TestOnlyNextCharterAgreementProfile]::new())
$null=$p.EnableCharterAttempt([Decennium.Foundation.Laboratory.TestOnlyCharterAttemptProfile]::new())
$null=$p.EnableLaterEncounter()
$null=$p.EnableCompanionReinforcement([Decennium.Foundation.Laboratory.TestOnlyReinforcementProfile]::new())
$null=$p.EnableLivingOpponentRetreat([Decennium.Foundation.Laboratory.TestOnlyLivingOpponentRetreatProfile]::new())
$null=$p.EnablePhysicalReengagement($true,$true)
$null=$p.EnableSurpriseAwareEntry([Decennium.Foundation.SurpriseAwareness]::Warned)
$null=$p.EnableConnectedExplorationObservation()

$combinedFailure=$null
try { $null=Call 'LaterPrepared' @($p) } catch { $combinedFailure=$_.Exception.Message }
if ($combinedFailure -notlike '*ContentRequiredReferenceUnresolved*') { throw "Combined-manifest baseline changed: $combinedFailure" }

$standalonePolicy=Call 'ManufacturePolicy' @([uint32]8,$null,$null,$null)
$sim=Call 'World' @($standalonePolicy)
$null=Call 'WorldAdvance' @($sim,11584,1)
$manufacture=Call 'ManufactureCommand' @($sim,$kind::StartManufacturing,$researcher::Recipe,0,0)
$beforeStock=$sim.Execute($auth,$manufacture).Code
$start=Call 'ResearchCommand' @($sim,$kind::StartFormulaResearch,$researcher::Evidence,0,$companion,$researcher::Recipe)
$began=$sim.Execute($auth,$start).Code
$null=Call 'WorldAdvance' @($sim,17216,1)
$paused=$sim.Capture()
$bytes=$codec.Encode($paused)
$restored=[Decennium.Foundation.Simulation]::new($standalonePolicy,$codec.Decode($bytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$pauseRoundtrip=[Convert]::ToHexString($bytes) -eq [Convert]::ToHexString($codec.Encode($restored.Capture()))
foreach ($run in @($sim,$restored)) {
    $resume=Call 'ResearchCommand' @($run,$kind::ResumeFormulaWork,$paused.FormulaWork[-1].Id,0,$companion,$researcher::Recipe)
    $resumed=$run.Execute($auth,$resume).Code
    if ($resumed -ne 'Committed') { throw "Resume failed: $resumed" }
    $null=Call 'WorldAdvance' @($run,11584,1)
}
$completed=$sim.Capture()
$project=$completed.FormulaWork[-1]
$replay=[Convert]::ToHexString($codec.Encode($completed)) -eq [Convert]::ToHexString($codec.Encode($restored.Capture()))
$manufacture=Call 'ManufactureCommand' @($sim,$kind::StartManufacturing,$researcher::Recipe,0,0)
$afterStock=$sim.Execute($auth,$manufacture).Code
if ($beforeStock -ne 'ManufacturingCredentialMissing' -or $began -ne 'Committed' -or
    $paused.FormulaWork[-1].Status.ToString() -ne 'Paused' -or $paused.FormulaWork[-1].Work.Labor.ToString() -ne '17216/1' -or
    $project.Status.ToString() -ne 'Success' -or $project.Natural -ne 12 -or
    $project.Work.Labor.ToString() -ne '28800/1' -or $afterStock -ne 'ManufacturingIngredientSpoiled' -or
    !$pauseRoundtrip -or !$replay) { throw 'Standalone research baseline changed.' }

[pscustomobject]@{
    connectedExisting=[ordered]@{
        clock=$atSite.RuleClock.ToString()
        revision=$atSite.Revision
        wire=$atSite.WireSchemaVersion
        charterOutcome=$atSite.CharterAttempt.Outcome.ToString()
        site=@($actor.X,$actor.Y)
        randomState=$atSite.RandomState
        nextNaturalIfUnchanged=[Decennium.Foundation.Laboratory.PlaytestDice]::RollD20($atSite.RandomState).Natural
        query=$oldQuery
        execute=$oldStart
        combinedFailure=$combinedFailure
        portableProfilesUnresolvedByCombinedManifest=$unknown
    }
    standaloneExisting=[ordered]@{
        wire=$completed.WireSchemaVersion
        beforeKnowledgeManufacturing=$beforeStock
        start=$began
        pausedAt=$paused.RuleClock.ToString()
        pausedLabor=$paused.FormulaWork[-1].Work.Labor.ToString()
        resume=$resumed
        pauseRoundtripByteIdentical=$pauseRoundtrip
        resumedFinalByteIdentical=$replay
        completedAt=$completed.RuleClock.ToString()
        labor=$project.Work.Labor.ToString()
        result=$project.Status.ToString()
        natural=$project.Natural
        afterKnowledgeManufacturing=$afterStock
    }
} | ConvertTo-Json -Depth 8
