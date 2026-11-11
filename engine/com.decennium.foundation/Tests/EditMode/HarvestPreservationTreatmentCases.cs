#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string Mgt05bVessel="TEST_ONLY.preservation.sealable-vessel";
        private const string Mgt05bSupply="TEST_ONLY.preservation.supply-half-pound";

        private static uint HarvestTreatmentSeed(bool success)
        {
            var baseline=TestOnlySharedWorldPolicy.WithHarvestPreservationTreatment(new SharedHarvestFixture()).Initial();
            int harvestModifier=HarvestModifier(baseline);
            int cookingModifier=AbilityCheckRules.Derive(baseline,TestOnlyPolicy.ActorId,"cooking",CharacterAbility.Wisdom).Total;
            for(uint seed=1;seed<uint.MaxValue;seed++) {
                var harvest=RuleDice.RollD20(seed);
                if(!RuleResolution.TaskCheck(harvest.Natural,harvestModifier,12).Success)continue;
                var treatment=RuleDice.RollD20(harvest.NextRandomState);
                bool treatmentSuccess=RuleResolution.TaskCheck(treatment.Natural,cookingModifier,10).Success;
                if(treatmentSuccess==success)return seed;
            }
            throw new Exception("No deterministic source-harvest/treatment check seed found.");
        }

        private static Simulation PreparedHarvestTreatment(uint seed,bool portionFirst,out TestOnlySharedWorldPolicy policy,
            out string treatedLotId,out string untreatedSiblingId,bool splitTreatedLotBeforeTreatment=false,bool exposure=false)
        {
            policy=exposure
                ?TestOnlySharedWorldPolicy.WithHarvestPreservationExposure(new SharedHarvestFixture(),seed)
                :TestOnlySharedWorldPolicy.WithHarvestPreservationTreatment(new SharedHarvestFixture(),seed);
            var simulation=World(policy);
            Require(simulation.Capture().SchemaVersion==(exposure?Snapshot.HarvestPreservationExposureSchema:Snapshot.HarvestPreservationTreatmentSchema)
                &&simulation.Capture().HarvestRequirementWorks.Length==0,
                exposure?"MGT-05C did not select the exposure schema76 profile."
                    :"MGT-05B did not select the treatment-only schema75 profile.");
            WorldStep(simulation,1,0);WorldAdvance(simulation,1);
            WorldStep(simulation,0,1);WorldAdvance(simulation,1);
            WorldStep(simulation,0,1);WorldAdvance(simulation,1);
            WorldStep(simulation,0,1);WorldAdvance(simulation,1);
            WorldStep(simulation,1,0);WorldAdvance(simulation,1);

            HarvestCommit(simulation,HarvestPreservationSourceCommand(simulation));
            WorldAdvance(simulation,600);
            var harvested=simulation.Capture();
            treatedLotId=harvested.HarvestUnits.Single(x=>x.Status==HarvestUnitStatus.Extracted).Id;
            untreatedSiblingId="";
            if(portionFirst) {
                string sourceLotId=treatedLotId;
                untreatedSiblingId=sourceLotId;
                HarvestCommit(simulation,IC(simulation,CommandKind.PortionInventory,sourceLotId,
                    new InventoryRequest(RuleQuantity.FromFraction(1,8),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                treatedLotId=simulation.Capture().InventoryLots.Single(x=>x.ParentId==sourceLotId).LotId;
                if(splitTreatedLotBeforeTreatment)
                    WorldCommit(simulation,IC(simulation,CommandKind.PortionInventory,treatedLotId,
                        new InventoryRequest(RuleQuantity.FromFraction(1,16),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
            }

            PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,treatedLotId,
                handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
            PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,treatedLotId,
                Mgt05bVessel,HandlingKind.Stow,TestOnlyPolicy.ActorId));
            PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,Mgt05bSupply,
                Mgt05bVessel,HandlingKind.Stow,TestOnlyPolicy.ActorId));
            return simulation;
        }

        private static Command StartHarvestTreatment(Simulation simulation,string lotId)
        {
            var state=simulation.Capture();
            return new Command("mgt05b.treatment."+(state.Revision+1),TestOnlyPolicy.ActorId,state.Revision,
                CommandKind.StartHarvestPreservationTreatment,lotId,
                inventory:new InventoryRequest(state.Work.AvailableAmount(lotId),"",HandlingKind.Pickup));
        }

        private static void AddHarvestPreservationTreatmentCases(Dictionary<string,Action> cases,string directory)
        {
            var codec=new SnapshotCodec();var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("mgt05b_closed_vessel_treatment_lineage_save_restore_and_replay",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var a=PreparedHarvestTreatment(seed,true,out var policyA,out string treated,out string sibling);
                var b=PreparedHarvestTreatment(seed,true,out var policyB,out string replayTreated,out string replaySibling);
                var onePiece=PreparedHarvestTreatment(seed,true,out _,out string wholePieceLot,out _);
                Require(treated==replayTreated&&sibling==replaySibling&&Bytes(a).SequenceEqual(Bytes(b)),
                    "Identically commanded harvesting, subdivision, custody and vessel preparation did not replay exactly.");
                var prepared=a.Capture();
                Require(wholePieceLot==treated&&Bytes(a).SequenceEqual(Bytes(onePiece)),
                    "The whole-advance run did not begin from the same authoritative treatment state.");
                Require(prepared.InventoryLots.Single(x=>x.LotId==treated).ParentId==sibling
                    &&prepared.PortableEquipment.Single(x=>x.Id==treated).ParentId==Mgt05bVessel
                    &&prepared.PortableEquipment.Single(x=>x.Id==Mgt05bSupply).ParentId==Mgt05bVessel
                    &&HarvestPreservationRules.TryProject(prepared,treated,out var beforeTreatment)
                    &&beforeTreatment.State==HarvestPreservationState.Fresh,
                    "The treatment target is not an actual fresh descendant of the extracted generic-fish-meat source in the open vessel.");

                var unsupportedOldAdapter=new Command("mgt05b.old-adapter",TestOnlyPolicy.ActorId,prepared.Revision,
                    CommandKind.StartHarvestRequirementWork,treated,
                    inventory:new InventoryRequest(prepared.Work.AvailableAmount(treated),"",HandlingKind.Pickup));
                var oldAdapterQuery=a.QueryCommand(host,unsupportedOldAdapter);
                Require(!oldAdapterQuery.Supported,"Schema75 exposed the superseded schema74 Fresh-work adapter.");
                var start=StartHarvestTreatment(a,treated);byte[] beforeQuery=Bytes(a);var query=a.QueryCommand(host,start);
                Require(query.Supported&&query.Admissible&&query.Costs.Any(x=>x.Kind=="work-seconds"
                    &&x.Amount==HarvestPreservationTreatmentValidation.WorkSeconds)
                    &&beforeQuery.SequenceEqual(Bytes(a)),"Schema75 did not expose a pure, bounded 1,800-second treatment command query.");
                var startResult=a.Execute(host,start);
                if(startResult.Outcome!=Outcome.Committed) {
                    var candidate=prepared.Copy();string resolver=policyA.Resolve(candidate,start);string validation="";
                    try { Validation.Snapshot(candidate); } catch(Exception error) { validation=error.Message; }
                    string fixture=policyA.ValidateState(candidate);
                    throw new Exception("Treatment start rejected by simulation: "+startResult.Code+"; resolver="+resolver
                        +"; snapshot="+validation+"; policy="+fixture);
                }
                WorldCommit(b,StartHarvestTreatment(b,replayTreated));
                WorldCommit(onePiece,StartHarvestTreatment(onePiece,wholePieceLot));
                WorldAdvance(onePiece,1800);
                WorldAdvance(a,900);WorldAdvance(b,900);
                var half=Bytes(a);Require(half.SequenceEqual(Bytes(b)),"Treatment work diverged before the save checkpoint.");
                var partial=a.Capture();var job=partial.HarvestPreservationTreatmentAttempts.Single();
                Require(job.Status==HarvestPreservationTreatmentStatus.Working&&job.Work.Labor==new RuleTime(900)
                    &&partial.Work.Reservations.Single(x=>x.Id==job.TargetReservationId).RemainingAmount==job.TreatedAmount
                    &&partial.Work.Reservations.Single(x=>x.Id==job.SupplyReservationId).RemainingAmount
                        ==HarvestPreservationTreatmentValidation.SupplyAmount
                    &&partial.PortableEquipment.Single(x=>x.Id==Mgt05bVessel).Open
                    &&!HarvestPreservationRules.IsProtectedAt(partial,treated,partial.RuleClock),
                    "Mid-work state failed to preserve exact worker credit, both reservations, and the required open vessel.");
                RejectUnchanged(a,host,Portable(a,CommandKind.ClosePortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId),"HarvestTreatmentInputsInUse");
                RejectUnchanged(a,host,IC(a,CommandKind.BeginFixedEncounter,actor:TestOnlyPolicy.ActorId),
                    "HarvestTreatmentInterruptionUnsupported");
                var decodedHalf=codec.Decode(half);
                string decodedPolicyError=policyA.ValidateState(decodedHalf);
                if(decodedPolicyError!=null)throw new Exception("Decoded mid-work policy state rejected: "+decodedPolicyError
                    +"; profiles="+decodedHalf.PortableStorageProfiles.Length+":"
                    +string.Join(",",decodedHalf.PortableStorageProfiles.Select(x=>x.ProfileId)));
                var restoredA=new Simulation(policyA,decodedHalf,ExecutionProfile.Laboratory);
                var restoredB=new Simulation(policyB,codec.Decode(half),ExecutionProfile.Laboratory);
                Require(half.SequenceEqual(Bytes(restoredA))&&half.SequenceEqual(Bytes(restoredB)),
                    "Schema75 active treatment failed canonical save/restore.");
                WorldAdvance(restoredA,900);WorldAdvance(restoredB,900);WorldAdvance(b,900);
                var completed=restoredA.Capture();job=completed.HarvestPreservationTreatmentAttempts.Single();
                Require(Bytes(restoredA).SequenceEqual(Bytes(restoredB))&&Bytes(restoredA).SequenceEqual(Bytes(b)),
                    "Save/restore or independent replay diverged at treatment completion.");
                var wholeCompleted=onePiece.Capture();var wholeAttempt=wholeCompleted.HarvestPreservationTreatmentAttempts.Single();
                var target=completed.Work.Lots.Single(x=>x.Id==treated);
                var targetReservation=completed.Work.Reservations.Single(x=>x.Id==job.TargetReservationId);
                var supplyReservation=completed.Work.Reservations.Single(x=>x.Id==job.SupplyReservationId);
                var supply=completed.Work.Lots.Single(x=>x.Id==Mgt05bSupply);
                var vessel=completed.PortableEquipment.Single(x=>x.Id==Mgt05bVessel);
                bool hasCompletionProjection=HarvestPreservationRules.TryProjectAt(completed,treated,
                    job.CompletedAt.Value,out var atCompletion);
                Require(job.Status==HarvestPreservationTreatmentStatus.Success&&job.Work.Labor==new RuleTime(1800)
                    &&job.CompletedAt==completed.RuleClock&&job.SealedAt==job.CompletedAt&&!vessel.Open
                    &&target.Amount==job.TreatedAmount&&completed.Work.AvailableAmount(treated)==job.TreatedAmount
                    &&targetReservation.ConsumedAmount==default(RuleQuantity)&&targetReservation.ReleasedAmount==job.TreatedAmount
                    &&supply.Amount==default(RuleQuantity)&&supplyReservation.ConsumedAmount==HarvestPreservationTreatmentValidation.SupplyAmount
                    &&supplyReservation.ReleasedAmount==default(RuleQuantity)&&job.RandomWordsConsumed==1
                    &&job.RandomBefore!=job.RandomAfter&&HarvestPreservationRules.IsProtectedAt(completed,treated,job.CompletedAt.Value)
                    &&hasCompletionProjection
                    &&atCompletion.State==HarvestPreservationState.Fresh
                    &&wholeCompleted.RuleClock==completed.RuleClock&&wholeAttempt.Status==job.Status
                    &&wholeAttempt.Work.Labor==job.Work.Labor&&wholeAttempt.Natural==job.Natural
                    &&wholeAttempt.Degree==job.Degree&&wholeAttempt.RandomBefore==job.RandomBefore
                    &&wholeAttempt.RandomAfter==job.RandomAfter&&wholeCompleted.Work.Lots.Single(x=>x.Id==treated).Amount==target.Amount
                    &&wholeCompleted.Work.Lots.Single(x=>x.Id==Mgt05bSupply).Amount==supply.Amount,
                    "Successful treatment did not spend one actual half-pound supply, release unconsumed fish, and seal/protect at completion.");
                var exactSave=Bytes(restoredA);var completionRestore=new Simulation(policyA,codec.Decode(exactSave),ExecutionProfile.Laboratory);
                Require(exactSave.SequenceEqual(Bytes(completionRestore)),"Completed sealed treatment changed through save/restore.");

                RejectUnchanged(restoredA,host,Portable(restoredA,CommandKind.OpenPortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId),"HarvestTreatmentProtectionActive");
                RejectUnchanged(restoredA,host,Portable(restoredA,CommandKind.HandlePortableEquipment,treated,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId),"HarvestTreatmentProtectionActive");
                RejectUnchanged(restoredA,host,IC(restoredA,CommandKind.PortionInventory,treated,
                    new InventoryRequest(RuleQuantity.FromFraction(1,32),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId),
                    "HarvestTreatmentProtectionActive");
                PortableCommit(restoredA,Portable(restoredA,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId));
                PortableCommit(restoredA,Portable(restoredA,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.ActorId));
                foreach(var replay in new[]{restoredB,b}) {
                    PortableCommit(replay,Portable(replay,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                        handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId));
                    PortableCommit(replay,Portable(replay,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                        handling:HandlingKind.Drop,actor:TestOnlyPolicy.ActorId));
                }
                Require(HarvestPreservationRules.IsProtectedAt(restoredA.Capture(),treated,restoredA.Capture().RuleClock),
                    "Moving the intact, closed whole vessel cancelled its treatment protection.");
                RuleTime expires=job.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds);
                int toExpiry=checked((int)(expires.Numerator/expires.Denominator-restoredA.Capture().RuleClock.Numerator
                    /restoredA.Capture().RuleClock.Denominator));
                WorldAdvance(restoredA,toExpiry);WorldAdvance(restoredB,toExpiry);WorldAdvance(b,toExpiry);
                var atExpiry=restoredA.Capture();
                Require(Bytes(restoredA).SequenceEqual(Bytes(restoredB))&&Bytes(restoredA).SequenceEqual(Bytes(b))
                    &&atExpiry.RuleClock==expires&&!HarvestPreservationRules.IsProtectedAt(atExpiry,treated,expires)
                    &&HarvestPreservationRules.TryProjectAt(atExpiry,treated,expires,out var exactEnd)
                    &&exactEnd.UnprotectedAge==atCompletion.UnprotectedAge
                    &&exactEnd.State==HarvestPreservationState.Fresh
                    &&HarvestPreservationRules.TryProject(atExpiry,sibling,out var unprotected)
                    &&unprotected.State==HarvestPreservationState.Spoiled,
                    "Protection did not end exclusively at 24 hours, preserve the treated descendant's age, or leave its sibling aging normally.");
                var expiryRestore=new Simulation(policyA,codec.Decode(Bytes(restoredA)),ExecutionProfile.Laboratory);
                Require(Bytes(restoredA).SequenceEqual(Bytes(expiryRestore)),"Exact expiry projection changed through save/restore.");
                WorldAdvance(restoredA,1);WorldAdvance(restoredB,1);WorldAdvance(b,1);
                var afterExpiry=restoredA.Capture();
                Require(Bytes(restoredA).SequenceEqual(Bytes(restoredB))&&Bytes(restoredA).SequenceEqual(Bytes(b))
                    &&HarvestPreservationRules.TryProject(afterExpiry,treated,out var afterProtection)
                    &&afterProtection.UnprotectedAge==atCompletion.UnprotectedAge.AddSeconds(1),
                    "After-expiry age did not resume or deterministic replay diverged.");

                PortableCommit(restoredA,Portable(restoredA,CommandKind.OpenPortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                PortableCommit(restoredA,Portable(restoredA,CommandKind.HandlePortableEquipment,treated,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
                RuleQuantity beforeSplit=restoredA.Capture().Work.Lots.Single(x=>x.Id==treated).Amount;
                WorldCommit(restoredA,IC(restoredA,CommandKind.PortionInventory,treated,
                    new InventoryRequest(RuleQuantity.FromFraction(1,16),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                var split=restoredA.Capture();var descendants=split.InventoryLots.Where(x=>x.ParentId==treated).ToArray();
                Require(descendants.Length==1
                    &&split.Work.Lots.Where(x=>x.Id==treated||x.Id==descendants[0].LotId)
                        .Aggregate(default(RuleQuantity),(sum,x)=>sum+x.Amount)==beforeSplit
                    &&HarvestPreservationRules.TryProject(split,treated,out var parentProjection)
                    &&HarvestPreservationRules.TryProject(split,descendants[0].LotId,out var inheritedProjection)
                    &&parentProjection.UnprotectedAge==inheritedProjection.UnprotectedAge
                    &&inheritedProjection.State==HarvestPreservationState.Fresh,
                    "A post-expiry portion failed to conserve mass and inherit the treated ancestor's origin and elapsed protection history.");
                var finalSave=Bytes(restoredA);var finalRestore=new Simulation(policyA,codec.Decode(finalSave),ExecutionProfile.Laboratory);
                Require(finalSave.SequenceEqual(Bytes(finalRestore)),"The post-expiry lineage save did not round-trip canonically.");
            });

            cases.Add("mgt05b_failed_treatment_spends_supply_once_without_protection",()=>{
                uint seed=HarvestTreatmentSeed(false);
                var simulation=PreparedHarvestTreatment(seed,false,out var policy,out string target,out _);
                var start=StartHarvestTreatment(simulation,target);WorldCommit(simulation,start);WorldAdvance(simulation,1800);
                var state=simulation.Capture();var attempt=state.HarvestPreservationTreatmentAttempts.Single();
                Require(attempt.Status==HarvestPreservationTreatmentStatus.Failure
                    &&(attempt.Degree==HarvestPreservationTreatmentDegree.Failure
                        ||attempt.Degree==HarvestPreservationTreatmentDegree.CriticalFailure),
                    "A seeded unsuccessful task check did not settle as a treatment failure.");
                Require(!attempt.SealedAt.HasValue&&state.PortableEquipment.Single(x=>x.Id==Mgt05bVessel).Open
                    &&state.Work.Lots.Single(x=>x.Id==target).Amount==attempt.TreatedAmount
                    &&state.Work.Reservations.Single(x=>x.Id==attempt.TargetReservationId).ReleasedAmount==attempt.TreatedAmount
                    &&state.Work.Lots.Single(x=>x.Id==Mgt05bSupply).Amount==default(RuleQuantity)
                    &&state.Work.Reservations.Single(x=>x.Id==attempt.SupplyReservationId).ConsumedAmount
                        ==HarvestPreservationTreatmentValidation.SupplyAmount
                    &&!HarvestPreservationRules.IsProtectedAt(state,target,state.RuleClock)
                    &&HarvestPreservationRules.TryProject(state,target,out var unpreserved)
                    &&unpreserved.State==HarvestPreservationState.Fresh,
                    "Failure did not spend only the consumed supply, release unconsumed target mass, and leave it unprotected in the open vessel.");
                var encoded=Bytes(simulation);var restored=new Simulation(policy,new SnapshotCodec().Decode(encoded),ExecutionProfile.Laboratory);
                Require(encoded.SequenceEqual(Bytes(restored)),"Failed treatment evidence or resource settlement changed through save/restore.");
            });

            cases.Add("mgt05b_degraded_treatment_retains_half_value_and_spoilage_deadlines_reject",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var degraded=PreparedHarvestTreatment(seed,false,out var policy,out string target,out _);
                var initial=degraded.Capture();var unit=initial.HarvestUnits.Single(x=>x.Status==HarvestUnitStatus.Extracted);
                RuleTime degradedAt=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds);
                var toDegraded=new RuleQuantity(degradedAt.Numerator,degradedAt.Denominator)
                    -new RuleQuantity(initial.RuleClock.Numerator,initial.RuleClock.Denominator);
                Require(toDegraded.Denominator==1&&toDegraded.Numerator>0,"Fixture cannot reach the exact Fresh-to-Degraded boundary.");
                WorldAdvance(degraded,checked((int)toDegraded.Numerator));
                var atBoundary=degraded.Capture();
                Require(HarvestPreservationRules.TryProject(atBoundary,target,out var degradedBefore)
                    &&degradedBefore.State==HarvestPreservationState.Degraded,
                    "Natural aging did not derive Degraded at the first sourced interval.");
                WorldCommit(degraded,StartHarvestTreatment(degraded,target));WorldAdvance(degraded,1800);
                var completed=degraded.Capture();var attempt=completed.HarvestPreservationTreatmentAttempts.Single();
                bool hasDegradedProjection=HarvestPreservationRules.TryProject(completed,target,out var degradedAfter);
                Require(attempt.Status==HarvestPreservationTreatmentStatus.Success
                    &&hasDegradedProjection
                    &&degradedAfter.State==HarvestPreservationState.Degraded
                    &&degradedAfter.ValueMultiplier==RuleQuantity.FromFraction(1,2),
                    "Successful preservation restored freshness or lost Degraded's half-value state.");
                WorldAdvance(degraded,HarvestPreservationTreatmentValidation.ProtectionSeconds);
                var expiry=degraded.Capture();
                Require(!HarvestPreservationRules.IsProtectedAt(expiry,target,expiry.RuleClock)
                    &&HarvestPreservationRules.TryProject(expiry,target,out var degradedAtExpiry)
                    &&degradedAtExpiry.State==HarvestPreservationState.Degraded
                    &&degradedAtExpiry.ValueMultiplier==RuleQuantity.FromFraction(1,2)
                    &&degradedAtExpiry.UnprotectedAge==degradedAfter.UnprotectedAge,
                    "The 24-hour protection interval failed to retain Degraded state and half value at exact expiry.");
                var restored=new Simulation(policy,new SnapshotCodec().Decode(Bytes(degraded)),ExecutionProfile.Laboratory);
                Require(Bytes(degraded).SequenceEqual(Bytes(restored)),"Degraded preservation changed through save/restore.");

                var deadline=PreparedHarvestTreatment(seed,false,out var deadlinePolicy,out string deadlineLot,out _);
                var deadlineState=deadline.Capture();var source=deadlineState.HarvestUnits.Single(x=>x.Status==HarvestUnitStatus.Extracted);
                RuleTime spoilAt=source.OriginAt.AddSeconds(checked(source.PreservationIntervalSeconds*2L));
                RuleQuantity finishQuantity=new RuleQuantity(spoilAt.Numerator,spoilAt.Denominator)
                    -new RuleQuantity(HarvestPreservationTreatmentValidation.WorkSeconds);
                RuleTime finishesAt=new RuleTime(finishQuantity.Numerator,finishQuantity.Denominator);
                var remaining=new RuleQuantity(finishesAt.Numerator,finishesAt.Denominator)
                    -new RuleQuantity(deadlineState.RuleClock.Numerator,deadlineState.RuleClock.Denominator);
                Require(remaining.Denominator==1&&remaining.Numerator>0,"Fixture cannot reach exactly 1,800 seconds before Spoiled.");
                WorldAdvance(deadline,checked((int)remaining.Numerator));
                Require(HarvestPreservationRules.TryProject(deadline.Capture(),deadlineLot,out var beforeDeadline)
                    &&beforeDeadline.State==HarvestPreservationState.Degraded,
                    "Target was not Degraded immediately before the exact Spoiled completion deadline.");
                RejectUnchanged(deadline,host,StartHarvestTreatment(deadline,deadlineLot),
                    "HarvestTreatmentCannotFinishBeforeSpoilage");
                WorldAdvance(deadline,HarvestPreservationTreatmentValidation.WorkSeconds);
                var spoiled=deadline.Capture();
                Require(spoiled.RuleClock==spoilAt&&HarvestPreservationRules.TryProject(spoiled,deadlineLot,out var spoiledView)
                    &&spoiledView.State==HarvestPreservationState.Spoiled,
                    "Exact two-interval age did not derive Spoiled.");
                RejectUnchanged(deadline,host,StartHarvestTreatment(deadline,deadlineLot),
                    "HarvestTreatmentCannotRescueSpoiledMaterial");
                Require(spoiled.HarvestPreservationTreatmentAttempts.Length==0
                    &&spoiled.Work.Lots.Single(x=>x.Id==Mgt05bSupply).Amount==HarvestPreservationTreatmentValidation.SupplyAmount,
                    "An exact-deadline or already-Spoiled rejection reserved work or spent preservation stock.");
            });

            cases.Add("mgt05b_lineage_cutoff_save_restore_and_replay",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var a=PreparedHarvestTreatment(seed,true,out var policyA,out string treated,out _,true);
                var b=PreparedHarvestTreatment(seed,true,out var policyB,out string replayTreated,out _,true);
                var preTreatmentChild=a.Capture().InventoryLots.Single(x=>x.ParentId==treated).LotId;
                Require(treated==replayTreated&&Bytes(a).SequenceEqual(Bytes(b)),
                    "The two actual harvest and pre-treatment subdivision runs did not begin identically.");
                WorldCommit(a,StartHarvestTreatment(a,treated));WorldCommit(b,StartHarvestTreatment(b,replayTreated));
                WorldAdvance(a,900);WorldAdvance(b,900);
                byte[] midWork=Bytes(a);
                var restored=new Simulation(policyA,new SnapshotCodec().Decode(midWork),ExecutionProfile.Laboratory);
                Require(midWork.SequenceEqual(Bytes(restored))&&midWork.SequenceEqual(Bytes(b)),
                    "The active treatment and pre-existing child did not round-trip or replay identically.");
                WorldAdvance(restored,900);WorldAdvance(b,900);
                var completed=restored.Capture();var attempt=completed.HarvestPreservationTreatmentAttempts.Single();
                var originLot=completed.InventoryLots.Single(x=>x.LotId==treated);
                while(originLot.ParentId!="")originLot=completed.InventoryLots.Single(x=>x.LotId==originLot.ParentId);
                var harvest=completed.HarvestUnits.Single(x=>x.Id==originLot.LotId);
                RuleQuantity expectedAge=new RuleQuantity(attempt.CompletedAt.Value.Numerator,attempt.CompletedAt.Value.Denominator)
                    -new RuleQuantity(harvest.OriginAt.Numerator,harvest.OriginAt.Denominator);
                Require(attempt.Status==HarvestPreservationTreatmentStatus.Success
                    &&HarvestPreservationRules.TryProjectAt(completed,preTreatmentChild,attempt.CompletedAt.Value,out var childAtCompletion)
                    &&childAtCompletion.UnprotectedAge==new RuleTime(expectedAge.Numerator,expectedAge.Denominator),
                    "A child separated before treatment did not retain its full unprotected age at successful completion.");
                Require(Bytes(restored).SequenceEqual(Bytes(b)),"Treatment completion diverged after restoring the active-work save.");
                var completionSave=Bytes(restored);
                var completedRestore=new Simulation(policyA,new SnapshotCodec().Decode(completionSave),ExecutionProfile.Laboratory);
                Require(completionSave.SequenceEqual(Bytes(completedRestore)),"The terminal treatment and lineage did not round-trip canonically.");

                WorldAdvance(completedRestore,HarvestPreservationTreatmentValidation.ProtectionSeconds);
                WorldAdvance(b,HarvestPreservationTreatmentValidation.ProtectionSeconds);
                Require(Bytes(completedRestore).SequenceEqual(Bytes(b)),"Protection expiry diverged across restored and uninterrupted runs.");
                var expired=completedRestore.Capture();
                Require(expired.RuleClock==attempt.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds)
                    &&HarvestPreservationRules.TryProject(expired,preTreatmentChild,out var oldBranch)
                    &&oldBranch.State==HarvestPreservationState.Spoiled,
                    "A pre-treatment branch did not age continuously while the remaining target was protected.");
                WorldCommit(completedRestore,IC(completedRestore,CommandKind.PortionInventory,preTreatmentChild,
                    new InventoryRequest(RuleQuantity.FromFraction(1,32),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                WorldCommit(b,IC(b,CommandKind.PortionInventory,preTreatmentChild,
                    new InventoryRequest(RuleQuantity.FromFraction(1,32),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                var afterBranchSplit=completedRestore.Capture();
                string laterChild=afterBranchSplit.InventoryLots.Single(x=>x.ParentId==preTreatmentChild).LotId;
                Require(Bytes(completedRestore).SequenceEqual(Bytes(b))
                    &&HarvestPreservationRules.TryProject(afterBranchSplit,preTreatmentChild,out var oldAfterSplit)
                    &&HarvestPreservationRules.TryProject(afterBranchSplit,laterChild,out var laterBranch)
                    &&oldAfterSplit.UnprotectedAge==laterBranch.UnprotectedAge
                    &&oldAfterSplit.State==laterBranch.State&&laterBranch.State==HarvestPreservationState.Spoiled,
                    "A descendant created after protection expired incorrectly inherited the treated ancestor's earlier protection.");

                foreach(var run in new[]{completedRestore,b}) {
                    PortableCommit(run,Portable(run,CommandKind.OpenPortableContainer,Mgt05bVessel,actor:TestOnlyPolicy.ActorId));
                    PortableCommit(run,Portable(run,CommandKind.HandlePortableEquipment,treated,
                        handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
                    WorldCommit(run,IC(run,CommandKind.PortionInventory,treated,
                        new InventoryRequest(RuleQuantity.FromFraction(1,32),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                }
                var completeLineage=completedRestore.Capture();
                string postTreatmentChild=completeLineage.InventoryLots.Single(x=>x.ParentId==treated
                    &&x.CreatedAt>=attempt.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds)).LotId;
                Require(Bytes(completedRestore).SequenceEqual(Bytes(b))
                    &&HarvestPreservationRules.TryProject(completeLineage,treated,out var preservedParent)
                    &&HarvestPreservationRules.TryProject(completeLineage,postTreatmentChild,out var postTreatmentBranch)
                    &&preservedParent.UnprotectedAge==postTreatmentBranch.UnprotectedAge
                    &&postTreatmentBranch.State==HarvestPreservationState.Fresh,
                    "A descendant separated from the treated target after expiry did not inherit the protection actually experienced by that target.");
                byte[] finalSave=Bytes(completedRestore);
                var finalRestore=new Simulation(policyA,new SnapshotCodec().Decode(finalSave),ExecutionProfile.Laboratory);
                Require(finalSave.SequenceEqual(Bytes(finalRestore)),"The split-before-treatment and split-after-expiry lineage did not round-trip.");
            });

            cases.Add("mgt05b_closed_vessel_handover_preserves_treatment_and_ownership",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var a=PreparedHarvestTreatment(seed,false,out var policyA,out string target,out _);
                var b=PreparedHarvestTreatment(seed,false,out var policyB,out string replayTarget,out _);
                WorldCommit(a,StartHarvestTreatment(a,target));WorldCommit(b,StartHarvestTreatment(b,replayTarget));
                WorldAdvance(a,HarvestPreservationTreatmentValidation.WorkSeconds);
                WorldAdvance(b,HarvestPreservationTreatmentValidation.WorkSeconds);
                var before=a.Capture();var prior=before.HarvestPreservationTreatmentAttempts.Single();
                string targetOwner=before.PortableEquipment.Single(x=>x.Id==target).OwnerId;
                Require(Bytes(a).SequenceEqual(Bytes(b))&&prior.Status==HarvestPreservationTreatmentStatus.Success
                    &&!before.PortableEquipment.Single(x=>x.Id==Mgt05bVessel).Open,
                    "The replay pair did not reach the same successfully sealed vessel state.");
                foreach(var run in new[]{a,b}) {
                    PortableCommit(run,Portable(run,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                        handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId));
                    PortableCommit(run,Portable(run,CommandKind.HandlePortableEquipment,Mgt05bVessel,
                        destination:TestOnlyPolicy.CompanionId,handling:HandlingKind.Handover,actor:TestOnlyPolicy.ActorId));
                }
                var state=a.Capture();var attempt=state.HarvestPreservationTreatmentAttempts.Single();
                var vessel=state.PortableEquipment.Single(x=>x.Id==Mgt05bVessel);
                var targetItem=state.PortableEquipment.Single(x=>x.Id==target);
                var supplyItem=state.PortableEquipment.Single(x=>x.Id==Mgt05bSupply);
                var supplyLot=state.InventoryLots.Single(x=>x.LotId==Mgt05bSupply);
                var supplyLedger=state.Work.Lots.Single(x=>x.Id==Mgt05bSupply);
                Require(Bytes(a).SequenceEqual(Bytes(b))&&vessel.CustodianId==TestOnlyPolicy.CompanionId
                    &&targetItem.CustodianId==TestOnlyPolicy.CompanionId&&supplyItem.CustodianId==TestOnlyPolicy.CompanionId
                    &&vessel.OwnerId==TestOnlyPolicy.ActorId&&targetItem.OwnerId==targetOwner
                    &&supplyItem.OwnerId==TestOnlyPolicy.ActorId&&supplyLot.OwnerId==TestOnlyPolicy.ActorId
                    &&supplyLedger.CustodianId==TestOnlyPolicy.CompanionId&&supplyLedger.Amount==default(RuleQuantity)
                    &&attempt.WorkerId==prior.WorkerId&&attempt.InventoryLotId==prior.InventoryLotId
                    &&attempt.TreatedAmount==prior.TreatedAmount&&attempt.CompletedAt==prior.CompletedAt
                    &&attempt.SealedAt==prior.SealedAt&&attempt.Status==prior.Status
                    &&HarvestPreservationRules.IsProtectedAt(state,target,state.RuleClock)
                    &&HarvestPreservationRules.TryProject(state,target,out var afterHandover)
                    &&HarvestPreservationRules.TryProject(before,target,out var beforeHandover)
                    &&afterHandover.UnprotectedAge==beforeHandover.UnprotectedAge,
                    "Legal closed-vessel custody transfer changed ownership, treatment history, resources, protection or elapsed protected age. "
                    +"custody="+vessel.CustodianId+"/"+targetItem.CustodianId+"/"+supplyItem.CustodianId+"/"+supplyLedger.CustodianId
                    +" owners="+vessel.OwnerId+"/"+targetItem.OwnerId+"/"+supplyItem.OwnerId+"/"+supplyLot.OwnerId
                    +" supply="+supplyLedger.Amount+" worker="+attempt.WorkerId+" target="+attempt.InventoryLotId
                    +" duration="+attempt.CompletedAt+"/"+attempt.SealedAt+" status="+attempt.Status+"/"+prior.Status
                    +" protected="+HarvestPreservationRules.IsProtectedAt(state,target,state.RuleClock)
                    +" age="+(HarvestPreservationRules.TryProject(state,target,out var afterView)?afterView.UnprotectedAge.ToString():"missing")
                    +"/"+(HarvestPreservationRules.TryProject(before,target,out var beforeView)?beforeView.UnprotectedAge.ToString():"missing")
                    +" bytes="+Bytes(a).SequenceEqual(Bytes(b)));
                byte[] handedOverSave=Bytes(a);
                var restored=new Simulation(policyA,new SnapshotCodec().Decode(handedOverSave),ExecutionProfile.Laboratory);
                Require(handedOverSave.SequenceEqual(Bytes(restored))&&handedOverSave.SequenceEqual(Bytes(b)),
                    "Closed-vessel handover custody did not survive canonical save/restore and deterministic replay.");
                RejectUnchanged(restored,TestOnlySharedWorldPolicy.Host(),Portable(restored,CommandKind.OpenPortableContainer,
                    Mgt05bVessel,actor:TestOnlyPolicy.CompanionId),"HarvestTreatmentProtectionActive");
                RejectUnchanged(restored,TestOnlySharedWorldPolicy.Host(),Portable(restored,CommandKind.HandlePortableEquipment,
                    target,handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.CompanionId),"HarvestTreatmentProtectionActive");
            });

            cases.Add("mgt05c_controlled_open_portion_retrieval_save_restore_and_replay",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var first=PreparedHarvestTreatment(seed,false,out var policyA,out string treated,out _,exposure:true);
                var replay=PreparedHarvestTreatment(seed,false,out var policyB,out string replayTreated,out _,exposure:true);
                WorldCommit(first,StartHarvestTreatment(first,treated));WorldCommit(replay,StartHarvestTreatment(replay,replayTreated));
                WorldAdvance(first,HarvestPreservationTreatmentValidation.WorkSeconds);
                WorldAdvance(replay,HarvestPreservationTreatmentValidation.WorkSeconds);
                Require(Bytes(first).SequenceEqual(Bytes(replay)),"Schema76 treatment setup did not replay identically.");

                uint randomBeforeOpening=first.Capture().RandomState;
                foreach(var run in new[]{first,replay})
                    PortableCommit(run,Portable(run,CommandKind.OpenPortableContainer,Mgt05bVessel,actor:TestOnlyPolicy.ActorId));
                var opened=first.Capture();var opening=opened.HarvestPreservationEvidence.Single();
                Require(Bytes(first).SequenceEqual(Bytes(replay))&&opening.Kind==HarvestPreservationEvidenceKind.ControlledOpening
                    &&opened.RandomState==randomBeforeOpening
                    &&opening.At==opened.PortableHandling.Single(x=>x.Id==opening.PortableHandlingId).EndedAt
                    &&HarvestPreservationRules.IsProtectedAt(opened,treated,opened.RuleClock),
                    "The qualifying open did not bind the physical handling completion or preserve current coverage.");

                byte[] openSave=Bytes(first);
                var restored=new Simulation(policyA,codec.Decode(openSave),ExecutionProfile.Laboratory);
                Require(openSave.SequenceEqual(Bytes(restored))&&openSave.SequenceEqual(Bytes(replay)),
                    "The active controlled-opening state failed save/restore or deterministic replay.");
                RejectUnchanged(restored,host,IC(restored,CommandKind.BeginFixedEncounter,actor:TestOnlyPolicy.ActorId),
                    "HarvestPreservationOpenLifecycleTacticalUnsupported");
                var parentBefore=restored.Capture().InventoryLots.Single(x=>x.LotId==treated);
                var stateBeforeSplit=restored.Capture();
                RuleQuantity availableBeforeSplit=stateBeforeSplit.Work.AvailableAmount(treated);
                string custodianBeforeSplit=stateBeforeSplit.PortableEquipment.Single(x=>x.Id==treated).CustodianId;
                uint randomBeforePortion=restored.Capture().RandomState;
                RuleQuantity amount=RuleQuantity.FromFraction(1,16);
                foreach(var run in new[]{restored,replay})
                    WorldCommit(run,IC(run,CommandKind.PortionInventory,treated,
                        new InventoryRequest(amount,"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                var split=restored.Capture();string child=split.InventoryLots.Single(x=>x.ParentId==treated).LotId;
                var childRecord=split.InventoryLots.Single(x=>x.LotId==child);
                Require(Bytes(restored).SequenceEqual(Bytes(replay))&&split.HarvestPreservationEvidence.Count(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion)==1
                    &&split.Work.AvailableAmount(treated)+split.Work.AvailableAmount(child)==availableBeforeSplit
                    &&childRecord.CreatedAmount==amount&&childRecord.CreatedAt==opening.At
                    &&childRecord.FreshUntil==parentBefore.FreshUntil&&childRecord.Nutrition==NutritionKind.None
                    &&childRecord.OwnerId==parentBefore.OwnerId
                    &&split.Work.Lots.Single(x=>x.Id==child).CustodianId==custodianBeforeSplit
                    &&split.RandomState==randomBeforePortion
                    &&split.PortableEquipment.Single(x=>x.Id==child).ParentId==Mgt05bVessel
                    &&split.PortableEquipment.Single(x=>x.Id==child).CustodianId==custodianBeforeSplit
                    &&HarvestPreservationRules.IsProtectedAt(split,treated,split.RuleClock)
                    &&HarvestPreservationRules.IsProtectedAt(split,child,split.RuleClock),
                    "The evidenced split was not conserved, in-vessel, origin-preserving, and covered for both child and remainder.");
                RejectUnchanged(restored,host,IC(restored,CommandKind.PortionInventory,treated,
                    new InventoryRequest(amount,"",HandlingKind.Pickup),TestOnlyPolicy.ActorId),"HarvestTreatmentProtectionActive");
                RejectUnchanged(restored,host,IC(restored,CommandKind.PortionInventory,child,
                    new InventoryRequest(RuleQuantity.FromFraction(1,32),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId),
                    "HarvestTreatmentProtectionActive");
                var downgraded=split.Copy();downgraded.SchemaVersion=Snapshot.HarvestPreservationTreatmentSchema;
                bool evidenceDowngradeRejected=false;
                try { codec.Encode(downgraded); }
                catch(ArgumentException) { evidenceDowngradeRejected=true; }
                catch(InvalidOperationException) { evidenceDowngradeRejected=true; }
                Require(evidenceDowngradeRejected,"Schema76 evidence was silently dropped by a schema75 downgrade.");

                byte[] splitSave=Bytes(restored);
                var splitRestored=new Simulation(policyA,codec.Decode(splitSave),ExecutionProfile.Laboratory);
                Require(splitSave.SequenceEqual(Bytes(splitRestored))&&splitSave.SequenceEqual(Bytes(replay)),
                    "The split-before-retrieval state failed canonical save/restore or replay.");
                WorldAdvance(splitRestored,20);WorldAdvance(replay,20);
                Require(Bytes(splitRestored).SequenceEqual(Bytes(replay)),
                    "The in-vessel protection interval diverged before physical retrieval.");
                foreach(var run in new[]{splitRestored,replay})
                    PortableCommit(run,Portable(run,CommandKind.HandlePortableEquipment,child,
                        handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
                var removed=splitRestored.Capture();var retrieval=removed.PortableHandling.Single(x=>x.ItemId==child
                    &&x.Operation==PortableOperation.Retrieve);
                Require(Bytes(splitRestored).SequenceEqual(Bytes(replay))&&retrieval.EndedAt==removed.RuleClock
                    &&!HarvestPreservationRules.IsProtectedAt(removed,child,retrieval.EndedAt)
                    &&HarvestPreservationRules.IsProtectedAt(removed,treated,retrieval.EndedAt),
                    "Physical retrieval did not cut off only the child at its handling completion.");

                byte[] removedSave=Bytes(splitRestored);
                var removedRestored=new Simulation(policyA,codec.Decode(removedSave),ExecutionProfile.Laboratory);
                Require(removedSave.SequenceEqual(Bytes(removedRestored))&&removedSave.SequenceEqual(Bytes(replay)),
                    "The post-retrieval cutoff failed save/restore or deterministic replay.");
                var beforeLaterSplit=removedRestored.Capture();
                Require(HarvestPreservationRules.TryProjectAt(beforeLaterSplit,child,beforeLaterSplit.RuleClock,
                    out var childAgeBeforeLaterSplit),"The removed child has no preservation projection before later subdivision.");
                RuleQuantity childMassBeforeLaterSplit=beforeLaterSplit.Work.AvailableAmount(child);
                RuleQuantity laterPortion=RuleQuantity.FromFraction(1,32);
                foreach(var run in new[]{removedRestored,replay})
                    WorldCommit(run,IC(run,CommandKind.PortionInventory,child,
                        new InventoryRequest(laterPortion,"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                var afterLaterSplit=removedRestored.Capture();
                string grandchild=afterLaterSplit.InventoryLots.Single(x=>x.ParentId==child).LotId;
                var laterChild=afterLaterSplit.InventoryLots.Single(x=>x.LotId==child);
                var grandchildRecord=afterLaterSplit.InventoryLots.Single(x=>x.LotId==grandchild);
                Require(Bytes(removedRestored).SequenceEqual(Bytes(replay))
                    &&afterLaterSplit.Work.AvailableAmount(child)+afterLaterSplit.Work.AvailableAmount(grandchild)==childMassBeforeLaterSplit
                    &&grandchildRecord.CreatedAmount==laterPortion&&grandchildRecord.ParentId==child
                    &&grandchildRecord.FreshUntil==laterChild.FreshUntil&&grandchildRecord.Nutrition==NutritionKind.None
                    &&grandchildRecord.OwnerId==laterChild.OwnerId
                    &&afterLaterSplit.RandomState==beforeLaterSplit.RandomState,
                    "A legal post-removal subdivision did not conserve the child amount and original material identity.");
                Require(HarvestPreservationRules.TryProjectAt(afterLaterSplit,child,afterLaterSplit.RuleClock,out var childAgeAfterLaterSplit)
                    &&HarvestPreservationRules.TryProjectAt(afterLaterSplit,grandchild,afterLaterSplit.RuleClock,out var grandchildAge)
                    &&childAgeBeforeLaterSplit.UnprotectedAge==childAgeAfterLaterSplit.UnprotectedAge
                    &&childAgeAfterLaterSplit.UnprotectedAge==grandchildAge.UnprotectedAge
                    &&!HarvestPreservationRules.IsProtectedAt(afterLaterSplit,child,afterLaterSplit.RuleClock)
                    &&!HarvestPreservationRules.IsProtectedAt(afterLaterSplit,grandchild,afterLaterSplit.RuleClock),
                    "A descendant of a removed portion lost earned protected time or regained active protection.");
                byte[] laterSplitSave=Bytes(removedRestored);
                var laterSplitRestored=new Simulation(policyA,codec.Decode(laterSplitSave),ExecutionProfile.Laboratory);
                Require(laterSplitSave.SequenceEqual(Bytes(laterSplitRestored))&&laterSplitSave.SequenceEqual(Bytes(replay)),
                    "The post-removal descendant lineage failed save/restore or deterministic replay.");
                removedRestored=laterSplitRestored;
                foreach(var run in new[]{removedRestored,replay}) {
                    PortableCommit(run,Portable(run,CommandKind.HandlePortableEquipment,child,Mgt05bVessel,
                        HandlingKind.Stow,TestOnlyPolicy.ActorId));
                    PortableCommit(run,Portable(run,CommandKind.ClosePortableContainer,Mgt05bVessel,actor:TestOnlyPolicy.ActorId));
                }
                var reinserted=removedRestored.Capture();var expiry=reinserted.HarvestPreservationTreatmentAttempts.Single()
                    .CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds);
                Require(Bytes(removedRestored).SequenceEqual(Bytes(replay))
                    &&reinserted.PortableEquipment.Single(x=>x.Id==child).ParentId==Mgt05bVessel
                    &&!HarvestPreservationRules.IsProtectedAt(reinserted,child,reinserted.RuleClock)
                    &&HarvestPreservationRules.IsProtectedAt(reinserted,treated,reinserted.RuleClock),
                    "Returning the retrieved child to the vessel incorrectly reactivated its protection.");
                var remaining=new RuleQuantity(expiry.Numerator,expiry.Denominator)
                    -new RuleQuantity(reinserted.RuleClock.Numerator,reinserted.RuleClock.Denominator);
                int secondsToExpiry=checked((int)(remaining.Numerator/remaining.Denominator));
                WorldAdvance(removedRestored,secondsToExpiry);
                WorldAdvance(replay,secondsToExpiry/2);
                WorldAdvance(replay,secondsToExpiry-secondsToExpiry/2);
                var wholeFinal=removedRestored.Capture();var partitionedFinal=replay.Capture();
                Require(wholeFinal.RuleClock==expiry&&partitionedFinal.RuleClock==expiry,
                    "Clock advancement did not settle at natural expiry: whole="+wholeFinal.RuleClock+" partitioned="
                    +partitionedFinal.RuleClock+" expected="+expiry);
                Require(!HarvestPreservationRules.IsProtectedAt(wholeFinal,treated,expiry)
                    &&!HarvestPreservationRules.IsProtectedAt(partitionedFinal,treated,expiry)
                    &&!HarvestPreservationRules.IsProtectedAt(wholeFinal,child,expiry)
                    &&!HarvestPreservationRules.IsProtectedAt(partitionedFinal,child,expiry),
                    "Natural expiry did not remove coverage consistently from root and permanently removed child.");
                Require(wholeFinal.RandomState==partitionedFinal.RandomState
                    &&HarvestPreservationRules.TryProjectAt(wholeFinal,treated,expiry,out var wholeProjection)
                    &&HarvestPreservationRules.TryProjectAt(partitionedFinal,treated,expiry,out var partitionedProjection)
                    &&wholeProjection.UnprotectedAge==partitionedProjection.UnprotectedAge
                    &&wholeProjection.State==partitionedProjection.State,
                    "Whole and partitioned advances produced different derived age, spoilage, or RNG results.");
            });

            cases.Add("mgt05c_deadline_and_trusted_exposure_boundaries",()=>{
                uint seed=HarvestTreatmentSeed(true);
                var prepared=PreparedHarvestTreatment(seed,false,out var policy,out string treated,out _,exposure:true);
                WorldCommit(prepared,StartHarvestTreatment(prepared,treated));
                WorldAdvance(prepared,HarvestPreservationTreatmentValidation.WorkSeconds);
                PortableCommit(prepared,Portable(prepared,CommandKind.OpenPortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                byte[] opened=Bytes(prepared);var codecLocal=new SnapshotCodec();

                var closes59=new Simulation(policy,codecLocal.Decode(opened),ExecutionProfile.Laboratory);
                WorldAdvance(closes59,58);
                PortableCommit(closes59,Portable(closes59,CommandKind.ClosePortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                var at59=closes59.Capture();
                Require(at59.PortableHandling.Single(x=>x.ItemId==Mgt05bVessel&&x.Operation==PortableOperation.Close).EndedAt
                        ==at59.HarvestPreservationEvidence.Single().At.AddSeconds(59)
                    &&HarvestPreservationRules.IsProtectedAt(at59,treated,at59.RuleClock),
                    "A close completing at O+59 did not preserve the remaining treatment coverage.");

                var closes60=new Simulation(policy,codecLocal.Decode(opened),ExecutionProfile.Laboratory);
                WorldAdvance(closes60,59);
                PortableCommit(closes60,Portable(closes60,CommandKind.ClosePortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                var at60=closes60.Capture();
                Require(at60.PortableHandling.Single(x=>x.ItemId==Mgt05bVessel&&x.Operation==PortableOperation.Close).EndedAt
                        ==at60.HarvestPreservationEvidence.Single().At.AddSeconds(HarvestPreservationEvidenceValidation.OpeningLimitSeconds)
                    &&!HarvestPreservationRules.IsProtectedAt(at60,treated,at60.RuleClock),
                    "A close completing exactly at D incorrectly preserved protection.");

                var crossingA=new Simulation(policy,codecLocal.Decode(opened),ExecutionProfile.Laboratory);
                var crossingB=new Simulation(policy,codecLocal.Decode(opened),ExecutionProfile.Laboratory);
                WorldAdvance(crossingA,120);
                WorldAdvance(crossingB,30);WorldAdvance(crossingB,90);
                var crossedA=crossingA.Capture();var crossedB=crossingB.Capture();
                Require(crossedA.RuleClock==crossedB.RuleClock
                    &&crossedA.RandomState==crossedB.RandomState
                    &&!HarvestPreservationRules.IsProtectedAt(crossedA,treated,crossedA.RuleClock)
                    &&!HarvestPreservationRules.IsProtectedAt(crossedB,treated,crossedB.RuleClock)
                    &&HarvestPreservationRules.TryProjectAt(crossedA,treated,crossedA.RuleClock,out var crossingViewA)
                    &&HarvestPreservationRules.TryProjectAt(crossedB,treated,crossedB.RuleClock,out var crossingViewB)
                    &&crossingViewA.UnprotectedAge==crossingViewB.UnprotectedAge&&crossingViewA.State==crossingViewB.State,
                    "Whole and partitioned advances across the unresolved-opening cutoff produced different clock, RNG, age, or state.");

                var fresh=PreparedHarvestTreatment(seed,true,out var exposurePolicy,out string exposureRoot,out _,exposure:true);
                WorldCommit(fresh,StartHarvestTreatment(fresh,exposureRoot));
                WorldAdvance(fresh,HarvestPreservationTreatmentValidation.WorkSeconds);
                PortableCommit(fresh,Portable(fresh,CommandKind.OpenPortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                WorldCommit(fresh,IC(fresh,CommandKind.PortionInventory,exposureRoot,
                    new InventoryRequest(RuleQuantity.FromFraction(1,16),"",HandlingKind.Pickup),TestOnlyPolicy.ActorId));
                byte[] exposedFrom=Bytes(fresh);string exposedChild=fresh.Capture().InventoryLots.Single(x=>x.ParentId==exposureRoot).LotId;
                string[] occurrences={
                    "TEST_ONLY.preservation.exposure.breach",
                    "TEST_ONLY.preservation.exposure.contamination",
                    "TEST_ONLY.preservation.exposure.incompatible-heat"
                };
                foreach(string occurrence in occurrences) {
                    var a=new Simulation(exposurePolicy,codecLocal.Decode(exposedFrom),ExecutionProfile.Laboratory);
                    var b=new Simulation(exposurePolicy,codecLocal.Decode(exposedFrom),ExecutionProfile.Laboratory);
                    var eventCommand=new Command("mgt05c.exposure."+occurrence,TestOnlyPolicy.ActorId,a.Capture().Revision,
                        CommandKind.RecordHarvestPreservationExposure,occurrence);
                    RejectUnchanged(new Simulation(exposurePolicy,codecLocal.Decode(exposedFrom),ExecutionProfile.Laboratory),
                        new Authority("TEST_ONLY.exposure-actor-only",new[]{TestOnlyPolicy.ActorId}),eventCommand,"NotAuthorized");
                    uint randomBeforeExposure=a.Capture().RandomState;
                    WorldCommit(a,eventCommand);
                    WorldCommit(b,new Command("mgt05c.exposure."+occurrence,TestOnlyPolicy.ActorId,b.Capture().Revision,
                        CommandKind.RecordHarvestPreservationExposure,occurrence));
                    var exposed=a.Capture();var record=exposed.HarvestPreservationEvidence.Single(x=>x.Kind==HarvestPreservationEvidenceKind.Exposure);
                    Require(Bytes(a).SequenceEqual(Bytes(b))&&record.OccurrenceId==occurrence
                        &&exposed.RandomState==randomBeforeExposure
                        &&record.At==exposed.RuleClock&&record.AppliedRevision==exposed.Revision
                        &&!HarvestPreservationRules.IsProtectedAt(exposed,exposureRoot,record.At)
                        &&!HarvestPreservationRules.IsProtectedAt(exposed,exposedChild,record.At),
                        "A trusted exposure did not end current root and in-vessel child coverage immediately: "+occurrence);
                    byte[] exposureSave=Bytes(a);
                    var exposureRestore=new Simulation(exposurePolicy,codecLocal.Decode(exposureSave),ExecutionProfile.Laboratory);
                    Require(exposureSave.SequenceEqual(Bytes(exposureRestore)),
                        "Typed exposure evidence failed canonical save/restore: "+occurrence);
                    var beforeExactRetry=exposureRestore.Capture();byte[] exactRetrySave=Bytes(exposureRestore);
                    var exactRetry=exposureRestore.Execute(host,eventCommand);var afterExactRetry=exposureRestore.Capture();
                    Require(exactRetry.Outcome==Outcome.Duplicate&&exactRetry.Code=="AlreadyCommitted"
                        &&exactRetrySave.SequenceEqual(Bytes(exposureRestore))
                        &&afterExactRetry.HarvestPreservationEvidence.Length==beforeExactRetry.HarvestPreservationEvidence.Length
                        &&afterExactRetry.RuleClock==beforeExactRetry.RuleClock&&afterExactRetry.RandomState==beforeExactRetry.RandomState,
                        "Exact exposure retry after restore was not idempotent: "+occurrence);
                    string conflictingOccurrence=occurrences[(Array.IndexOf(occurrences,occurrence)+1)%occurrences.Length];
                    RejectUnchanged(exposureRestore,host,new Command(eventCommand.Id,eventCommand.Actor,eventCommand.ExpectedRevision,
                        eventCommand.Kind,conflictingOccurrence),"CommandIdConflict");
                    RejectUnchanged(a,TestOnlySharedWorldPolicy.Host(),new Command("mgt05c.exposure.duplicate."+occurrence,
                        TestOnlyPolicy.ActorId,a.Capture().Revision,CommandKind.RecordHarvestPreservationExposure,occurrence),
                        "HarvestPreservationOccurrenceAlreadyRecorded");
                }
                var unknown=new Simulation(exposurePolicy,codecLocal.Decode(exposedFrom),ExecutionProfile.Laboratory);
                RejectUnchanged(unknown,TestOnlySharedWorldPolicy.Host(),new Command("mgt05c.exposure.unknown",
                    TestOnlyPolicy.ActorId,unknown.Capture().Revision,CommandKind.RecordHarvestPreservationExposure,
                    "TEST_ONLY.preservation.exposure.unknown"),"UnknownHarvestPreservationOccurrence");

                var removedBeforeExposure=new Simulation(exposurePolicy,codecLocal.Decode(exposedFrom),ExecutionProfile.Laboratory);
                PortableCommit(removedBeforeExposure,Portable(removedBeforeExposure,CommandKind.HandlePortableEquipment,exposedChild,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
                RuleTime retrievalAt=removedBeforeExposure.Capture().PortableHandling.Single(x=>x.ItemId==exposedChild
                    &&x.Operation==PortableOperation.Retrieve).EndedAt;
                Require(HarvestPreservationRules.TryProjectAt(removedBeforeExposure.Capture(),exposedChild,retrievalAt,
                    out var childAtRetrieval),"The removed child has no projection at retrieval completion.");
                WorldAdvance(removedBeforeExposure,1);
                var beforePostRemovalEvent=removedBeforeExposure.Capture();
                Require(HarvestPreservationRules.TryProjectAt(beforePostRemovalEvent,exposedChild,beforePostRemovalEvent.RuleClock,
                    out var childBeforeExposure),"The removed child has no projection before a later vessel event.");
                WorldCommit(removedBeforeExposure,new Command("mgt05c.exposure.after-retrieval",TestOnlyPolicy.ActorId,
                    beforePostRemovalEvent.Revision,CommandKind.RecordHarvestPreservationExposure,occurrences[0]));
                var afterPostRemovalEvent=removedBeforeExposure.Capture();
                Require(HarvestPreservationRules.TryProjectAt(afterPostRemovalEvent,exposedChild,afterPostRemovalEvent.RuleClock,
                        out var childAfterExposure)
                    &&childAtRetrieval.UnprotectedAge<childBeforeExposure.UnprotectedAge
                    &&childBeforeExposure.UnprotectedAge==childAfterExposure.UnprotectedAge
                    &&afterPostRemovalEvent.HarvestPreservationEvidence.Single(x=>x.Kind==HarvestPreservationEvidenceKind.Exposure).At
                        >retrievalAt
                    &&!HarvestPreservationRules.IsProtectedAt(afterPostRemovalEvent,exposureRoot,afterPostRemovalEvent.RuleClock),
                    "An exposure to the vessel rewrote a child’s already-removed protection history.");

                var beforeExpiry=PreparedHarvestTreatment(seed,false,out var expiryPolicy,out string expiryLot,out _,exposure:true);
                WorldCommit(beforeExpiry,StartHarvestTreatment(beforeExpiry,expiryLot));
                WorldAdvance(beforeExpiry,HarvestPreservationTreatmentValidation.WorkSeconds);
                RuleTime naturalExpiry=beforeExpiry.Capture().HarvestPreservationTreatmentAttempts.Single().CompletedAt.Value
                    .AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds);
                WorldAdvance(beforeExpiry,HarvestPreservationTreatmentValidation.ProtectionSeconds-1);
                PortableCommit(beforeExpiry,Portable(beforeExpiry,CommandKind.OpenPortableContainer,Mgt05bVessel,
                    actor:TestOnlyPolicy.ActorId));
                Require(beforeExpiry.Capture().RuleClock==naturalExpiry
                    &&!HarvestPreservationRules.IsProtectedAt(beforeExpiry.Capture(),expiryLot,naturalExpiry)
                    &&beforeExpiry.Capture().HarvestPreservationEvidence.Length==0,
                    "An opening completing at E created an invalid protected-opening exception.");
            });
        }
    }
}
#endif
