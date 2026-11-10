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
            out string treatedLotId,out string untreatedSiblingId)
        {
            policy=TestOnlySharedWorldPolicy.WithHarvestPreservationTreatment(new SharedHarvestFixture(),seed);
            var simulation=World(policy);
            Require(simulation.Capture().SchemaVersion==Snapshot.HarvestPreservationTreatmentSchema
                &&simulation.Capture().HarvestRequirementWorks.Length==0,
                "MGT-05B did not select the treatment-only schema75 profile.");
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
        }
    }
}
#endif
