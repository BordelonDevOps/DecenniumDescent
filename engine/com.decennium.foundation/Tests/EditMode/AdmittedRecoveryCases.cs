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
        private static void AddAdmittedRecoveryCases(Dictionary<string,Action> cases,string directory)
        {
            AddAdmittedObservationCases(cases,directory);
            AddAdmittedPlanningCases(cases,directory);
            cases.Add("int05_genuine_provisioning_strain_offer_recovery_and_continuation",()=> {
                var session=EarnClericObjective(true,directory,NewWorkControlExpedition());
                AwardAndAdvanceCleric(session,directory);
                string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                Snapshot State()=>ShortRestCapture(session);
                void Save(string name)=>session.Save(Path.Combine(directory,"int05-strain-"+name+".ddsave"));
                void Wait(int seconds)=>ClericCommit(session,hero,CommandKind.AdvanceClock,x:seconds,y:1);
                void Inventory(string owner,CommandKind kind,string target,RuleQuantity amount,
                    string destination="",HandlingKind handling=HandlingKind.Pickup) {
                    var state=State();var command=new Command("int05.provision."+state.Revision,owner,state.Revision,
                        kind,target,inventory:new InventoryRequest(amount,destination,handling));
                    var query=session.QueryCommand(ExpeditionSeat.Player,command);
                    Require(query.Admissible,"Provisioning source guard: "+kind+"/"+query.Code);
                    CommitVialRoute(session,command);
                }
                LongRestAdvanceTo(session,57600);
                ClericCommit(session,actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                LongRestAdvanceTo(session,86400);Save("first-rest");
                var first=State();
                Require(first.ExpeditionStrainGains.Any(x=>x.ActorId==actor&&x.AddedAmount==1)
                    &&!first.ExpeditionStrainRecoveryOffers.Any(x=>x.ActorId==actor&&x.Pending),
                    "The first genuine underprovisioned day must earn Strain without inventing recovery.");
                ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",x:1);Wait(6);
                Inventory(hero,CommandKind.PortionInventory,"TEST_ONLY.pack-rations",new RuleQuantity(2));
                var portion=State().InventoryLots.Single(x=>x.ParentId=="TEST_ONLY.pack-rations").LotId;
                Inventory(hero,CommandKind.HandlePortableEquipment,portion,new RuleQuantity(1),handling:HandlingKind.Drop);
                Wait(6);
                Inventory(actor,CommandKind.HandlePortableEquipment,portion,new RuleQuantity(1));Wait(6);
                Inventory(actor,CommandKind.StartIntake,portion,new RuleQuantity(2));Wait(1800);Save("food-consumed");
                ClericCommit(session,actor,CommandKind.BeginWorldStep,"walk",x:1);Wait(6);
                for(int i=0;i<2;i++) {
                    Inventory(actor,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new RuleQuantity(4),
                        TestOnlyFillingPolicy.CompanionSkinId);
                    Wait(60);
                    var current=State();
                    var water=current.VesselContents.Where(x=>x.VesselId==TestOnlyFillingPolicy.CompanionSkinId)
                        .Select(x=>x.LotId).Single(x=>current.Work.AvailableAmount(x)>new RuleQuantity(0));
                    Inventory(actor,CommandKind.StartIntake,water,new RuleQuantity(4));Wait(240);
                }
                Save("water-consumed");
                ClericCommit(session,actor,CommandKind.BeginWorldStep,"walk",x:-1);Wait(6);
                LongRestAdvanceTo(session,144000);
                ClericCommit(session,actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                LongRestAdvanceTo(session,172806);
                var offered=State();Save("pending-offer");
                Require(offered.RuleClock==new RuleTime(172800),"Recovery offer did not suspend the actual requested clock.");
                var offer=offered.ExpeditionStrainRecoveryOffers.Single(x=>x.ActorId==actor&&x.Pending);
                var forged=offered.Copy();
                forged.ExpeditionStrainRecoveryOffers=offered.ExpeditionStrainRecoveryOffers.Select(x=>x.Id==offer.Id
                    ?new ExpeditionStrainRecoveryOfferRecord(x.Id,x.ActorId,x.ActivityIntervalId,x.InitiatingCommandId,
                        x.CompletedAt,x.Revision,x.PointIds):x).ToArray();
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(forged));
                var unbacked=first.Copy();
                unbacked.ManufacturingAdvance=new ManufacturingAdvanceRecord(first.RuleClock.AddSeconds(6),false,
                    first.Receipts.Last().Id,first.Revision,string.Empty);
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(unbacked));
                var selected=offer.PointIds.First();
                var command=new Command("int05.strain.resolve",actor,offered.Revision,
                    CommandKind.ResolveExpeditionStrainRecovery,selected);
                AssertPureUtility(session,command);
                string path=Path.Combine(directory,"int05-strain-pending-offer.ddsave");session.Restore(path);
                AssertPureUtility(session,command);CommitVialRoute(session,command);
                var after=State();Save("resolved-continued");
                Require(after.RuleClock==new RuleTime(172806)
                    &&after.ExpeditionStrainRemovals.Count(x=>x.ActorId==actor&&x.PointId==selected)==1
                    &&!after.ExpeditionStrainRecoveryOffers.Single(x=>x.Id==offer.Id).Pending,
                    "Actual recovery did not remove one offered point and resume the suspended clock.");
                var bytes=Bytes(CastingSimulation(session));
                Require(session.Submit(ExpeditionSeat.Player,command).Response==ExpeditionResponse.Duplicate
                    &&bytes.SequenceEqual(Bytes(CastingSimulation(session))),"Recovery retry removed a second point.");
            });
            cases.Add("int05_advancement_denials_and_native_fallback_are_pure",()=> {
                var authority=new Authority("TEST_ONLY.host",new[]{ClericRpProfile.Actor},canModifyWorld:true,
                    inventoryOwners:new[]{ClericRpProfile.Actor});
                var rows=new[] {
                    (NewClericSettlement(),CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId,"MilestoneObjectiveIncomplete"),
                    (NewClericSettlement(),CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,"MilestoneObjectiveIncomplete"),
                    (NewClericSettlement(),CommandKind.AwardCharacterMilestone,BishopProfile.Milestone,"UndeclaredMilestone"),
                    (NewClericExpedition(),CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId,"UnsupportedAdvancementPath")
                };
                int n=0;
                foreach(var row in rows) {
                    var command=new Command("int05.advancement.denial."+(++n),ClericRpProfile.Actor,0,row.Item2,row.Item3,
                        advancement:row.Item2==CommandKind.AdvanceCharacterLevel?ClericEarnedChoices():null);
                    var sim=CastingSimulation(row.Item1);var before=Bytes(sim);
                    AssertPureUtility(row.Item1,command,row.Item4,authority);
                    Require(sim.Execute(authority,command).Code==row.Item4&&before.SequenceEqual(Bytes(sim)),
                        "Advancement source denial disagreed with execution or changed state.");
                }
                // Existing native Soldier fixture: compatibility evidence, not an admitted connected profile.
                var policy=AdvancementPolicy();var native=World(policy);var host=TestOnlySharedWorldPolicy.Host();
                foreach(bool award in new[]{true,false}) {
                    var command=award?AwardMilestone(native):AdvanceLevel(native);var before=Bytes(native);
                    for(int i=0;i<3;i++) {
                        var read=native.AssessCommandFactsV1(host,command,native.Capture().Revision);
                        Require(read.Supported&&read.Admissible&&read.InitialEligibility==true&&read.CommitFeasibility==null
                            &&read.ProhibitedCallAttempts.All(x=>x==0)&&before.SequenceEqual(Bytes(native)),
                            "Native fallback assessment mutated or constructed progression instead of checking it.");
                    }
                    WorldCommit(native,command);
                }
                var advanced=native.Capture();
                Require(advanced.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Count==2
                    &&advanced.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==4,
                    "The existing native fallback did not advance exactly or manufactured healing.");
                var bytes=Bytes(native);File.WriteAllBytes(Path.Combine(directory,"int05-native-soldier-advanced.ddsave"),bytes);
                Require(bytes.SequenceEqual(Bytes(new Simulation(policy,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),
                    "Native fallback advancement failed strict restoration.");
            });

            cases.Add("int05_stabilization_profile_and_sealed_stock_order_are_pure",()=> {
                var rows=new[] {
                    (ConnectedExpeditionSession.StartWithCompanionDose(),ConnectedExpeditionSession.Companion,"CompanionStabilizationUnavailable"),
                    (ConnectedExpeditionSession.StartWithCompanionStabilization(),ConnectedExpeditionSession.Companion,"CompanionStabilizationUnavailable"),
                    (ConnectedExpeditionSession.StartWithWoundTreatment(),WoundTreatmentStation.Kit.Id,"WoundTreatmentStockSealed")
                };
                var facts=new List<object>();int i=0;
                foreach(var row in rows) {
                    var sim=CastingSimulation(row.Item1);var state=sim.Capture();var before=Bytes(sim);
                    var command=new Command("int05.stabilize.profile."+(++i),ConnectedExpeditionSession.Hero,state.Revision,
                        CommandKind.StabilizeCompanion,row.Item2);
                    AssertPureUtility(row.Item1,command,row.Item3);
                    var read=sim.AssessCommandFactsV1(CastingAuthority(),command,state.Revision);
                    var actual=sim.Execute(CastingAuthority(),command);
                    Require(actual.Outcome==Outcome.Rejected&&actual.Code==row.Item3&&before.SequenceEqual(Bytes(sim)),
                        "Stabilization assessment changed state or moved the sealed-stock guard after family admission.");
                    facts.Add(new {state.WireSchemaVersion,code=actual.Code,read.Constraint.SourcePath,read.Constraint.SourceLine});
                }
                File.WriteAllText(Path.Combine(directory,"int05-stabilization-denials.json"),
                    System.Text.Json.JsonSerializer.Serialize(new {scope="Three authentic native profile/outer-order denials",facts}));
            });

            cases.Add("int05_care_profile_denials_share_native_order",()=> {
                const string hero=ConnectedExpeditionSession.Hero,patient=ConnectedExpeditionSession.Companion;
                var rows=new[] {
                    (NewClericExpedition(),CommandKind.BeginShortRest,ShortRestBerth.Id,"ClassRecoveryUnsupported"),
                    (ConnectedExpeditionSession.StartWithConsumeDecay(),CommandKind.BeginShortRest,ShortRestBerth.Id,"ShortRestUnavailable"),
                    (ConnectedExpeditionSession.StartWithWoundTreatment(),CommandKind.ConsumeDecay,ConsumeDecaySite.Id,"ConsumeDecayUnavailable"),
                    (ConnectedExpeditionSession.StartWithShortRest(),CommandKind.BeginMutationShortRest,FleshWardenProfile.FleshWarden,"MutationRestUnavailable"),
                    (ConnectedExpeditionSession.StartWithFleshWarden(),CommandKind.BeginMutationShortRest,"mutation.unknown","UnsupportedMutationRestSelection"),
                    (ConnectedExpeditionSession.StartWithWoundTreatment(),CommandKind.InterruptWoundTreatment,patient,"NoActiveWoundTreatment"),
                    (ConnectedExpeditionSession.StartWithShortRest(),CommandKind.InterruptShortRest,"rest.missing","NoMatchingActiveShortRest")
                };
                var facts=new List<object>();int index=0;
                foreach(var row in rows) {
                    var session=row.Item1;var sim=CastingSimulation(session);var state=sim.Capture();var bytes=Bytes(sim);
                    var command=new Command("int05.care.profile."+(++index),hero,state.Revision,row.Item2,row.Item3);
                    AssertPureUtility(session,command,row.Item4);
                    var read=sim.AssessCommandFactsV1(CastingAuthority(),command,state.Revision);
                    var actual=sim.Execute(CastingAuthority(),command);
                    Require(actual.Outcome==Outcome.Rejected&&actual.Code==row.Item4&&bytes.SequenceEqual(Bytes(sim)),
                        "Native profile/cancellation denial differed from actual execution.");
                    facts.Add(new {state.WireSchemaVersion,kind=command.Kind.ToString(),code=actual.Code,
                        read.Constraint.SourcePath,read.Constraint.SourceLine});
                }
                File.WriteAllText(Path.Combine(directory,"int05-care-profile-denials.json"),System.Text.Json.JsonSerializer.Serialize(new {
                    scope="Seven authentic factory-genesis native denials; current profile selection and early branch ordering, not public V1 admission",facts }));
            });

            cases.Add("int05_genuine_rest_assessment_occupancy_interrupt_and_retry",()=> {
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var session=NewClericLongRestExpedition();
                var unearned=new Command("int05.rest.unearned",actor,0,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                AssertPureUtility(session,unearned,"LongRestRequiresEarnedCleric2");
                var sim=CastingSimulation(session);var bytes=Bytes(sim);
                Require(sim.Execute(CastingAuthority(),unearned).Code=="LongRestRequiresEarnedCleric2"
                    && bytes.SequenceEqual(Bytes(sim)),"Unearned rest read disagreed with execution.");
                session=EarnClericObjective(true,directory,session);AwardAndAdvanceCleric(session,directory);
                var before=ShortRestCapture(session);
                var begin=new Command("int05.rest.begin",actor,before.Revision,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                AssertPureUtility(session,begin);
                string save=Path.Combine(directory,"int05-rest-before.ddsave");session.Save(save);session.Restore(save);
                AssertPureUtility(session,begin);CommitVialRoute(session,begin);
                var started=ShortRestCapture(session);var active=ClericLongRestProfile.Active(started);
                Require(active!=null && active.StartedAt==before.RuleClock
                    && active.DueAt==before.RuleClock.AddSeconds(ClericLongRestProfile.DurationSeconds)
                    && started.Work.WorkerIntervals.Count(x=>x.JobId==active.Id&&x.WorkerId==actor
                        &&x.Start==active.StartedAt&&x.End==active.DueAt)==1
                    && started.ClericLongRestSettlements.Length==0 && started.ConvictionBalance==null
                    && started.ResonancePools.Single().Current==before.ResonancePools.Single().Current
                    && started.RuleClock==before.RuleClock && started.RandomState==before.RandomState,
                    "Starting the actual rest must reserve one full interval without completing recovery.");
                var again=new Command("int05.rest.again",actor,started.Revision,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                AssertPureUtility(session,again,"LongRestAlreadyActive");
                var cast=new Command("int05.rest.cast",actor,started.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true));
                AssertPureUtility(session,cast,"LongRestRequiresInterruption");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:100,y:1);
                var partial=ShortRestCapture(session);
                var wrong=new Command("int05.rest.wrong",actor,partial.Revision,CommandKind.InterruptLongRest,"rest.wrong");
                AssertPureUtility(session,wrong,"NoMatchingActiveLongRest");
                var stop=new Command("int05.rest.stop",actor,partial.Revision,CommandKind.InterruptLongRest,active.Id);
                AssertPureUtility(session,stop);
                save=Path.Combine(directory,"int05-rest-pending.ddsave");session.Save(save);session.Restore(save);
                AssertPureUtility(session,stop);CommitVialRoute(session,stop);
                var ended=ShortRestCapture(session);sim=CastingSimulation(session);bytes=Bytes(sim);
                Require(ClericLongRestProfile.Active(ended)==null
                    && ended.ClericLongRests.Single().Outcome==ClericLongRestOutcome.Interrupted
                    && ended.ClericLongRestSettlements.Length==0 && ended.ConvictionBalance==null
                    && ended.RuleClock==partial.RuleClock && ended.RandomState==partial.RandomState
                    && ended.ResonancePools.Single().Current==partial.ResonancePools.Single().Current
                    && !ended.Work.WorkerIntervals.Any(x=>x.JobId==active.Id&&x.End>ended.RuleClock),
                    "Interrupt must release future occupancy without recovering resources or changing time/RNG.");
                foreach(var original in new[]{begin,stop}) {
                    var read=sim.AssessCommandFactsV1(CastingAuthority(),original,ended.Revision);
                    Require(read.Status==NativeAssessmentStatusV1.AlreadyCommitted && read.InitialEligibility==null
                        && read.ProhibitedCallAttempts.All(x=>x==0)
                        &&session.Submit(ExpeditionSeat.Player,original).Response==ExpeditionResponse.Duplicate
                        &&bytes.SequenceEqual(Bytes(sim)),"An old rest receipt was replaced by current rest eligibility.");
                }
                var fresh=new Command("int05.rest.finished",actor,ended.Revision,CommandKind.InterruptLongRest,active.Id);
                AssertPureUtility(session,fresh,"NoMatchingActiveLongRest");
                save=Path.Combine(directory,"int05-rest-interrupted.ddsave");session.Save(save);session.Restore(save);
                Require(bytes.SequenceEqual(Bytes(CastingSimulation(session))),"Rest interruption failed authenticated replay.");
                File.WriteAllText(Path.Combine(directory,"int05-rest-assessment-facts.json"),System.Text.Json.JsonSerializer.Serialize(new {
                    scope="Genuine earned Cleric long-rest start, reserved occupancy,100 seconds elapsed, explicit interruption, retries and strict restore",
                    beforeRevision=before.Revision,startRevision=started.Revision,interruptRevision=ended.Revision,
                    active.StartedAt,active.DueAt,interruptedAt=ended.RuleClock,
                    rpBefore=before.ResonancePools.Single().Current,rpAfter=ended.ResonancePools.Single().Current,
                    commitFeasibility="NOT CERTIFIED",moduleAcceptance="OPEN" }));
            });
        }
    }
}
#endif
