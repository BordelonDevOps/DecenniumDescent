#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string HuntingTrapItem="TEST_ONLY.hunting-trap";

        private static TestOnlyExpeditionRouteFixture HuntingTrapRoute()
            =>new TestOnlyExpeditionRouteFixture(new TestOnlyExpeditionRoute(RouteTravelId,
                TestOnlyPolicy.ContainerId,TestOnlyCropPolicy.PlotId,1,2,3,3,new RuleQuantity(4),
                ExpeditionRouteQuality.Secured,0,ExpeditionRouteMapping.Mapped,new RuleQuantity(100),new[]{
                    new TestOnlyRoutePositionBinding(default,1,2),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(1),1,3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(2),2,3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(3),2,4),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(4),3,4)}));

        private static TestOnlySharedWorldPolicy HuntingTrapRoutePolicy(TestOnlyExpeditionRouteFixture route,
            HuntingTrapFixture traps,uint seed)
            =>new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed))
                .EnableExpeditionRouteTravel(route).EnableHuntingTraps(traps);

        private static void AddHuntingTrapCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("hunting_trap_shares_exploration_clock_mining_save_and_tethered_recovery",()=>{
                var fixture=new HuntingTrapFixture(new HuntingTrapDefinition(HuntingTrapItem,TestOnlyPolicy.ActorId,1,0,
                    new[]{TestOnlyPolicy.ActorId}));
                var mining=new SharedMiningFixture();
                var policy=TestOnlySharedWorldPolicy.WithMiningAndHuntingTraps(mining,fixture,seed:5);
                var simulation=World(policy);
                Require(simulation.Capture().SchemaVersion==Snapshot.HuntingTrapSchema,"The explicit trap profile did not select schema55.");
                var item=simulation.Capture().PortableEquipment.Single(x=>x.Id==HuntingTrapItem);
                Require(item.ProfileId=="adventuring-gear.hunting-trap"&&item.SourceWeightLb==new RuleQuantity(25)
                    &&item.OperationalWeightLb==new RuleQuantity(25)&&item.Placement==PortablePlacement.Carried,
                    "The physical trap did not retain its authored 25 lb item identity.");

                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA,SharedMiningFixture.CategoryB)));
                var beforeSet=Bytes(simulation);
                var set=IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Set,id:"hunting-trap.set");
                var preview=simulation.QueryCommand(host,set);
                Require(preview.Admissible&&preview.Costs.Any(x=>x.Kind=="action"&&x.Amount==1)
                    &&preview.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==6)&&beforeSet.SequenceEqual(Bytes(simulation)),
                    "Set query changed state or omitted its one Action/six-second costs.");
                WorldCommit(simulation,set);
                Require(simulation.Capture().HuntingTrapActions.Single().Status==HuntingTrapActionStatus.Working
                    &&simulation.Capture().HuntingTrapDeployments.Length==0,
                    "Set did not pay at start while deferring deployment until completion.");
                WorldAdvance(simulation,6);
                var armed=simulation.Capture();
                var deployment=armed.HuntingTrapDeployments.Single();
                Require(deployment.Status==HuntingTrapDeploymentStatus.Armed&&deployment.AnchorX==1&&deployment.AnchorY==0
                    &&armed.PortableEquipment.Single(x=>x.Id==HuntingTrapItem).Placement==PortablePlacement.Ground
                    &&armed.MiningAttempts.Single().WorkDone==new RuleTime(6),
                    "Trap set completion did not share time and physical placement with companion mining.");

                byte[] armedSave=Bytes(simulation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(armedSave),ExecutionProfile.Laboratory);
                Require(armedSave.SequenceEqual(Bytes(simulation)),"Armed trap or concurrent mining changed through save/restore.");
                WorldStep(simulation,1,0);
                WorldAdvance(simulation,1);
                var triggered=simulation.Capture();
                var trigger=triggered.HuntingTrapTriggers.Single();
                var tether=triggered.HuntingTrapTethers.Single();
                Require(trigger.Status==HuntingTrapTriggerStatus.Resolved&&trigger.EntryKind==HuntingTrapEntryKind.ExplorationStep
                    &&trigger.Natural==5&&!trigger.SaveSuccess&&trigger.DamageRoll==1&&trigger.DamageApplied==1
                    &&deployment.Id==trigger.DeploymentId&&tether.Status==HuntingTrapTetherStatus.Active
                    &&tether.AnchorX==1&&tether.AnchorY==0&&tether.MaximumDistanceFeet==3
                    &&triggered.MiningAttempts.Single().WorkDone==new RuleTime(7),
                    "The first exploration entrant did not resolve the seeded DC13 save/damage/tether while mining advanced.");
                Require(!TestOnlyClubAttackPolicy.ConditionsFor(triggered,TestOnlyPolicy.ActorId).View().Has(ConditionKind.Restrained),
                    "The hunting-trap tether was incorrectly represented as Restrained.");
                byte[] triggeredSave=Bytes(simulation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(triggeredSave),ExecutionProfile.Laboratory);
                Require(triggeredSave.SequenceEqual(Bytes(simulation)),"Resolved trigger, tether or shared mining state changed through save/restore.");
                RejectUnchanged(simulation,host,IC(simulation,CommandKind.BeginWorldStep,"walk",actor:TestOnlyPolicy.ActorId,x:1),
                    "HuntingTrapTetherPreventsMovement");

                var free=IC(simulation,CommandKind.Interact,TestOnlyPolicy.ActorId,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Free,id:"hunting-trap.free-self");
                WorldCommit(simulation,free);
                WorldAdvance(simulation,6);
                var freed=simulation.Capture();
                Require(freed.HuntingTrapTethers.Single().Status==HuntingTrapTetherStatus.Released
                    &&freed.HuntingTrapActions.Single(x=>x.Id!=freed.HuntingTrapActions.Single(a=>a.Kind==HuntingTrapActionKind.Set).Id
                        &&x.Kind==HuntingTrapActionKind.Free).Status==HuntingTrapActionStatus.Succeeded,
                    "A successful STR check did not release the persisted tether.");

                var reset=IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Reset,id:"hunting-trap.reset");
                WorldCommit(simulation,reset);
                WorldAdvance(simulation,6);
                var rearmed=simulation.Capture();
                var resetAction=rearmed.HuntingTrapActions.Single(x=>x.Id!=free.Id&&x.Kind==HuntingTrapActionKind.Reset);
                var resetItem=rearmed.PortableEquipment.Single(x=>x.Id==HuntingTrapItem);
                Require(rearmed.HuntingTrapDeployments.Length==2
                    &&rearmed.HuntingTrapDeployments.Count(x=>x.TrapItemId==HuntingTrapItem&&x.Status==HuntingTrapDeploymentStatus.Armed)==1
                    &&rearmed.HuntingTrapDeployments.Any(x=>x.Id==deployment.Id&&x.Status==HuntingTrapDeploymentStatus.Sprung)
                    &&resetItem.OperationalWeightLb==new RuleQuantity(25),
                    "Reset state mismatch: deployments="+rearmed.HuntingTrapDeployments.Length+"; statuses="
                    +string.Join(",",rearmed.HuntingTrapDeployments.Select(x=>x.Id+"="+x.Status))+"; reset="+resetAction.Status
                    +"; item="+resetItem.Placement+"@"+resetItem.GroundX+","+resetItem.GroundY+"; weight="+resetItem.OperationalWeightLb);
                WorldStep(simulation,-1,0);
                WorldAdvance(simulation,1);
                var entry=IC(simulation,CommandKind.BeginWorldStep,"walk",actor:TestOnlyPolicy.ActorId,x:1,id:"hunting-trap.second-entry");
                WorldCommit(simulation,entry);
                var duplicateBytes=Bytes(simulation);
                Require(simulation.Execute(host,entry).Outcome==Outcome.Duplicate&&duplicateBytes.SequenceEqual(Bytes(simulation)),
                    "Duplicate movement delivery repeated the approach step.");
                var advance=IC(simulation,CommandKind.AdvanceClock,x:1,y:1,id:"hunting-trap.second-entry-arrival");
                WorldCommit(simulation,advance);
                var replayBytes=Bytes(simulation);
                Require(simulation.Execute(host,advance).Outcome==Outcome.Duplicate&&replayBytes.SequenceEqual(Bytes(simulation))
                    &&simulation.Capture().HuntingTrapTriggers.Length==2
                    &&simulation.Capture().HuntingTrapDeployments.Single(x=>x.Status==HuntingTrapDeploymentStatus.Sprung
                        &&x.Id!=deployment.Id).TriggerId==simulation.Capture().HuntingTrapTriggers.Single(x=>x.Id!=trigger.Id).Id,
                    "The reused trap did not trigger once for its next entrant or replay remained non-idempotent.");
            });
            cases.Add("hunting_trap_route_checkpoint_pauses_releases_and_resumes_with_saved_effort",()=>{
                var route=HuntingTrapRoute();
                var fixture=new HuntingTrapFixture(new HuntingTrapDefinition(HuntingTrapItem,TestOnlyPolicy.ActorId,1,3,
                    new[]{TestOnlyPolicy.ActorId}));
                var policy=HuntingTrapRoutePolicy(route,fixture,seed:5);var simulation=World(policy);
                RouteTravelReachSource(simulation);
                var set=IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Set,id:"hunting-trap.route.set");
                WorldCommit(simulation,set);WorldAdvance(simulation,6);
                WorldCommit(simulation,RouteTravelCommand(simulation,CommandKind.StartRouteTravel,"hunting-trap.route.start"));
                byte[] beforeArrival=Bytes(simulation);
                var partialAdvance=IC(simulation,CommandKind.AdvanceClock,x:5400,y:1,id:"hunting-trap.route.partial");
                WorldCommit(simulation,partialAdvance);
                var partial=simulation.Capture();
                Require(partial.HuntingTrapTriggers.Length==0&&partial.RouteTravels.Single().Progress==new RuleQuantity(1,2)
                    &&partial.RouteTravels.Single().Status==ExpeditionRouteTravelStatus.Moving
                    &&partial.RouteTravelSpatial.Single().X==new RuleQuantity(1)&&partial.RouteTravelSpatial.Single().Y==new RuleQuantity(2),
                    "Split route effort created an early checkpoint entry or lost its exact saved starting anchor.");
                byte[] partialBytes=Bytes(simulation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(partialBytes),ExecutionProfile.Laboratory);
                Require(partialBytes.SequenceEqual(Bytes(simulation)),"Partial route effort changed through save/restore.");
                var duplicatePartial=simulation.Execute(host,partialAdvance);
                Require(duplicatePartial.Outcome==Outcome.Duplicate&&partialBytes.SequenceEqual(Bytes(simulation)),
                    "Replayed partial route effort changed progress or trap-entry state.");
                var checkpointAdvance=IC(simulation,CommandKind.AdvanceClock,x:5400,y:1,id:"hunting-trap.route.checkpoint");
                WorldCommit(simulation,checkpointAdvance);
                var trapped=simulation.Capture();var arrival=trapped.HuntingTrapTriggers.Single();var travel=trapped.RouteTravels.Single();
                Require(arrival.EntryKind==HuntingTrapEntryKind.RouteTravelCheckpoint&&arrival.RouteId==RouteTravelId
                    &&arrival.RouteStartedRevision==travel.StartedRevision&&arrival.RouteProgress==new RuleQuantity(1)
                    &&arrival.Status==HuntingTrapTriggerStatus.Resolved&&!arrival.SaveSuccess&&arrival.At==trapped.RuleClock
                    &&travel.Status==ExpeditionRouteTravelStatus.Paused&&travel.Progress==new RuleQuantity(1)
                    &&travel.NominalEffort==new RuleTime(14400)
                    &&trapped.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1
                    &&trapped.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==3,
                    "Authored route arrival skipped the armed trap or failed to pause at the exact earned checkpoint.");
                byte[] trappedBytes=Bytes(simulation);
                var duplicateCheckpoint=simulation.Execute(host,checkpointAdvance);
                Require(duplicateCheckpoint.Outcome==Outcome.Duplicate&&trappedBytes.SequenceEqual(Bytes(simulation))
                    &&simulation.Capture().HuntingTrapTriggers.Length==1,
                    "Replayed route checkpoint processing created another trap entry.");
                simulation=new Simulation(policy,new SnapshotCodec().Decode(trappedBytes),ExecutionProfile.Laboratory);
                Require(trappedBytes.SequenceEqual(Bytes(simulation)),"Route entry, pause, and trap result changed through save/restore.");
                RejectUnchanged(simulation,host,RouteTravelCommand(simulation,CommandKind.ResumeRouteTravel,
                    "hunting-trap.route.resume-tethered"),"HuntingTrapTetherPreventsRouteTravel");
                WorldCommit(simulation,IC(simulation,CommandKind.Interact,TestOnlyPolicy.ActorId,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Free,id:"hunting-trap.route.free"));
                WorldAdvance(simulation,6);
                WorldCommit(simulation,RouteTravelCommand(simulation,CommandKind.ResumeRouteTravel,"hunting-trap.route.resume"));
                WorldAdvance(simulation,10800);
                var completed=simulation.Capture();
                Require(completed.RouteTravels.Single().Status==ExpeditionRouteTravelStatus.SegmentComplete
                    &&completed.RouteTravels.Single().Progress==new RuleQuantity(2)
                    &&completed.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==2
                    &&completed.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==3
                    &&completed.HuntingTrapTethers.Single().Status==HuntingTrapTetherStatus.Released
                    &&Bytes(simulation).SequenceEqual(Bytes(new Simulation(policy,
                        new SnapshotCodec().Decode(Bytes(simulation)),ExecutionProfile.Laboratory))),
                    "Release plus explicit route resumption did not preserve progress or canonical replay.");
                Require(beforeArrival.SequenceEqual(Bytes(new Simulation(policy,
                    new SnapshotCodec().Decode(beforeArrival),ExecutionProfile.Laboratory))),
                    "Moving route pre-arrival state did not round-trip canonically.");
            });
            cases.Add("hunting_trap_route_segment_completion_preserves_completed_status",()=>{
                var route=HuntingTrapRoute();
                var fixture=new HuntingTrapFixture(new HuntingTrapDefinition(HuntingTrapItem,TestOnlyPolicy.ActorId,2,3,
                    new[]{TestOnlyPolicy.ActorId}));
                var policy=HuntingTrapRoutePolicy(route,fixture,seed:5);var simulation=World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation,IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Set,id:"hunting-trap.terminal.set"));WorldAdvance(simulation,6);
                WorldCommit(simulation,RouteTravelCommand(simulation,CommandKind.StartRouteTravel,"hunting-trap.terminal.start"));
                WorldAdvance(simulation,21600);
                var terminal=simulation.Capture();var travel=terminal.RouteTravels.Single();
                Require(terminal.HuntingTrapTriggers.Single().RouteProgress==new RuleQuantity(2)
                    &&terminal.HuntingTrapTriggers.Single().Status==HuntingTrapTriggerStatus.Resolved
                    &&terminal.HuntingTrapTethers.Single().Status==HuntingTrapTetherStatus.Active
                    &&travel.Status==ExpeditionRouteTravelStatus.SegmentComplete&&travel.Progress==new RuleQuantity(2),
                    "A trap at the segment endpoint rewrote the completed route segment as paused or lost its trigger.");
                RejectUnchanged(simulation,host,RouteTravelCommand(simulation,CommandKind.StartRouteTravel,
                    "hunting-trap.terminal.next-segment"),"HuntingTrapTetherPreventsRouteTravel");
            });
            cases.Add("hunting_trap_composes_with_route_mapping_schema",()=>{
                var route=HuntingTrapRoute();
                var traps=new HuntingTrapFixture(new HuntingTrapDefinition(HuntingTrapItem,TestOnlyPolicy.ActorId,1,3,
                    new[]{TestOnlyPolicy.ActorId}));
                var mapping=new TestOnlyExpeditionRouteMappingResultFixture(route,
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId,"hunting-trap.route-map.result",
                        TestOnlyPolicy.ActorId,"hunting-trap.route-map.evidence",default,
                        ExpeditionRouteMappingResultDegree.Success));
                var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:5))
                    .EnableExpeditionRouteTravel(route).EnableTestOnlyRouteMappingResults(mapping).EnableHuntingTraps(traps);
                var simulation=World(policy);
                Require(simulation.Capture().SchemaVersion==Snapshot.HuntingTrapSchema,
                    "The trap + route mapping composition did not select schema55.");
                RouteTravelReachSource(simulation);
                WorldCommit(simulation,RouteMappingCommand(simulation,"hunting-trap.route-map.result",
                    "hunting-trap.route-map.consume"));
                WorldCommit(simulation,IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Set,id:"hunting-trap.route-map.set"));
                WorldAdvance(simulation,6);
                WorldCommit(simulation,RouteTravelCommand(simulation,CommandKind.StartRouteTravel,
                    "hunting-trap.route-map.start"));
                WorldAdvance(simulation,10800);
                var result=simulation.Capture();
                Require(result.RouteMappingResults.Length==1&&result.HuntingTrapTriggers.Length==1
                    &&result.HuntingTrapTriggers[0].Status==HuntingTrapTriggerStatus.Resolved
                    &&result.RouteTravels.Single().Status==ExpeditionRouteTravelStatus.Paused
                    &&result.RouteTravelSpatial.Single().X==new RuleQuantity(1)
                    &&result.RouteTravelSpatial.Single().Y==new RuleQuantity(3),
                    "Schema55 failed to preserve the earlier mapping extension alongside route-trigger state.");
                byte[] saved=Bytes(simulation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(simulation)),
                    "Composed route mapping, travel, trap and spatial records changed through save/restore.");
            });
            cases.Add("hunting_trap_pending_overwatch_push_is_gated_before_save_and_then_resolves",()=>{
                var traps=new HuntingTrapFixture(new HuntingTrapDefinition(HuntingTrapItem,TestOnlyPolicy.ActorId,3,0,
                    new[]{AdditionalTacticalActor.Id}));
                var policy=OverwatchExecutionPolicy(SeedForNatural(10)).EnableHuntingTraps(traps);
                var simulation=World(policy);
                WorldCommit(simulation,new Command("hunting-trap.ow.begin",TestOnlyPolicy.ActorId,
                    simulation.Capture().Revision,CommandKind.BeginFixedEncounter));
                RangedCommit(simulation,RangedCommand(simulation,CommandKind.ReloadRepeatingCrossbow,amount:1));
                WorldCommit(simulation,Tac(simulation,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(simulation,Tac(simulation,CommandKind.EndRegularTurn));
                for(int i=0;i<4&&simulation.Capture().Encounter.CurrentActor!=AdditionalTacticalActor.Id;i++)ConnectedEnd(simulation);
                Require(simulation.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,
                    "The fixed calendar did not reach the authored enemy between setup and the second shooter turn.");
                ConnectedEnd(simulation);
                Require(simulation.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId,
                    "The fixed calendar did not return to the shooter for trap deployment.");
                WorldCommit(simulation,Tac(simulation,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(simulation,new Command("hunting-trap.ow.designate",TestOnlyPolicy.ActorId,
                    simulation.Capture().Revision,CommandKind.DesignateOverwatch,simulation.Capture().Encounter.CurrentTurnId,
                    x:1,y:-1));
                TacStep(simulation,1,0);TacStep(simulation,2,0);
                WorldCommit(simulation,IC(simulation,CommandKind.Interact,HuntingTrapItem,actor:TestOnlyPolicy.ActorId,
                    x:(int)HuntingTrapInteraction.Set,id:"hunting-trap.ow.set"));
                WorldCommit(simulation,Tac(simulation,CommandKind.EndRegularTurn));
                for(int i=0;i<4&&simulation.Capture().Encounter.CurrentActor!=AdditionalTacticalActor.Id;i++)ConnectedEnd(simulation);
                Require(simulation.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,
                    "The fixed calendar did not return to the movement target after trap deployment.");
                if(!simulation.Capture().Stances.Any(x=>x.TurnOrdinal==simulation.Capture().Encounter.TurnOrdinal))
                    WorldCommit(simulation,Tac(simulation,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,
                        stance:(int)CombatStance.Guarded));
                TacStep(simulation,3,0);
                var entered=simulation.Capture();var pendingTrap=entered.HuntingTrapTriggers.Single();
                Require(entered.OverwatchOffers.Single().Status==OverwatchOfferStatus.Pending
                    &&pendingTrap.Status==HuntingTrapTriggerStatus.Pending
                    &&pendingTrap.EntryKind==HuntingTrapEntryKind.TacticalStep
                    &&pendingTrap.EntrantId==AdditionalTacticalActor.Id,
                    "Tactical entry did not retain both ordered Overwatch and trap decisions.");
                WorldCommit(simulation,OverwatchResponse(simulation,true));
                var shot=simulation.Capture();
                Require(shot.RangedAttacks.Single().Attack.Hit
                    &&shot.OverwatchRiderChoices.Single().Status==OverwatchRiderChoiceStatus.Pending
                    &&shot.HuntingTrapTriggers.Single().Status==HuntingTrapTriggerStatus.Pending
                    &&shot.HuntingTrapTethers.Length==0,
                    "The accepted Overwatch shot did not resolve before the pending trap's rider decision.");
                byte[] afterShot=Bytes(simulation);uint randomAfterShot=shot.RandomState;
                RejectUnchanged(simulation,host,OverwatchRiderCommand(simulation,OverwatchRider.Push),
                    "UnsupportedPendingTrapDisplacement");
                Require(afterShot.SequenceEqual(Bytes(simulation))&&simulation.Capture().RandomState==randomAfterShot
                    &&simulation.Capture().RangedAttacks.Single().Attack.Hit,
                    "A blocked pending-trap Push rewound the committed shot or consumed another random value.");
                WorldCommit(simulation,OverwatchRiderCommand(simulation,OverwatchRider.Snare));
                var resolved=simulation.Capture();
                Require(resolved.HuntingTrapTriggers.Single().Status==HuntingTrapTriggerStatus.Resolved
                    &&resolved.HuntingTrapTriggers.Single().CreatedRevision==resolved.TacticalMoves.Single(x=>x.Status==TacticalMoveStatus.Completed
                        &&x.ToX==3&&x.ToY==0).ResolvedRevision
                    &&resolved.OverwatchRiderChoices.Single().Choice==OverwatchRider.Snare
                    &&resolved.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).X==3
                    &&resolved.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).Y==0,
                    "Resolving a non-displacing rider did not proceed to the already-earned trap entry.");
                byte[] saved=Bytes(simulation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(simulation)),"Overwatch, selected rider and trap outcome changed through save/restore.");
            });
            cases.Add("hunting_trap_pending_entry_blocks_only_overlength_push_geometry",()=>{
                var deployment=new HuntingTrapDeploymentRecord("pending-deployment",HuntingTrapItem,TestOnlyPolicy.ActorId,
                    3,0,1,default,HuntingTrapDeploymentStatus.Sprung,"pending-trigger");
                var trigger=new HuntingTrapTriggerRecord("pending-trigger","pending-deployment","tactical-entry",
                    HuntingTrapEntryKind.TacticalStep,AdditionalTacticalActor.Id,2,0,1,default,HuntingTrapTriggerStatus.Pending);
                var snapshot=new Snapshot {HuntingTrapDeployments=new[]{deployment},HuntingTrapTriggers=new[]{trigger}};
                Require(TestOnlySharedWorldPolicy.PendingHuntingTrapEntryBlocksMove(snapshot,AdditionalTacticalActor.Id,4,0)
                    &&!TestOnlySharedWorldPolicy.PendingHuntingTrapEntryBlocksMove(snapshot,AdditionalTacticalActor.Id,3,0),
                    "Pending trap geometry either allowed a Push beyond three feet or blocked the trap anchor itself.");
            });
        }
    }
}
#endif
