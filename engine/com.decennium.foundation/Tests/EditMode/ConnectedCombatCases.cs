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
        private static TestOnlySharedWorldPolicy ConnectedPolicy(long hp=26,uint seed=1,ConditionCombatFixture conditions=null)
            =>new TestOnlySharedWorldPolicy(new SharedCombatFixture(hp,seed),conditions:conditions);
        private static Simulation ConnectedArena(TestOnlySharedWorldPolicy p=null)
        {
            var s=World(p??ConnectedPolicy());
            WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);
            Require(s.Capture().InventoryCombat&&s.Capture().Actors.Single(a=>a.Id==TestOnlyPolicy.ActorId).X==2,"Authored approach did not enter combat before departure.");
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(s,3,0);return s;
        }
        private static void ConnectedEnd(Simulation s)
        {
            if(ActorLifeRules.CanAct(s.Capture(),s.Capture().Encounter.CurrentActor)&&!TestOnlyClubAttackPolicy.ConditionsFor(s.Capture(),s.Capture().Encounter.CurrentActor).View().Unaware&&!s.Capture().Stances.Any(t=>t.TurnOrdinal==s.Capture().Encounter.TurnOrdinal))
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
        }
        private static void DefeatConnectedEnemy(Simulation s)
        {
            for(int count=0;!s.Capture().Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Dead;count++) {
                Require(count<20,"Combat fixture enemy did not resolve within bounded trace.");
                if(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId) {
                    if(!s.Capture().Stances.Any(t=>t.TurnOrdinal==s.Capture().Encounter.TurnOrdinal))WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                    WorldCommit(s,Tac(s,CommandKind.AttackClub,AdditionalTacticalActor.Id,weapon:TestOnlyClubAttackPolicy.ActorClub));
                    if(s.Capture().Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Dead)return;
                }
                ConnectedEnd(s);
            }
        }
        private static void AddConnectedCombatCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("connected_combat_day_seven_entry_preserves_sparse_calendar_and_paid_dash",()=>{
                var p=ConnectedPolicy();var s=World(p);WorldAdvance(s,612000);WorldStep(s,1,0,true);WorldAdvance(s,1,2);
                var before=WorldLedger(s);var calendar=s.Capture().WorldSchedule;BeginEncounter(s);var v=s.Capture();
                Require(v.SchemaVersion==14&&v.Encounter.TurnOrdinal==204000&&v.Encounter.StartRevisions.Count==1&&v.RuleClock==T(1224001,2)
                    &&v.WorldSchedule.Id==calendar.Id&&WorldLedger(s).LastStart==before.LastStart&&WorldLedger(s).MovementSpent==before.MovementSpent&&WorldLedger(s).ActionSpent,
                    "Entry rebased calendar, invented turns or refilled Dash.");
                RejectUnchanged(s,host,Tac(s,CommandKind.EncounterDash),"ActionAlreadySpent");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Guarded));ConnectedEnd(s);
                Require(s.Capture().RuleClock==T(612003)&&WorldLedger(s).ActionSpent,"Partial slot awarded a full round or refreshed outgoing actor.");
                var path=Path.Combine(directory,"connected-day-seven.bin");new FileSaveStore().Save(path,s.Capture());
                Require(Bytes(s).SequenceEqual(Bytes(new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory))),"Sparse day-seven entry failed restore.");
            });
            cases.Add("connected_combat_boundary_save_entry_processes_start_only_once",()=>{
                var p=ConnectedPolicy();var s=World(p);WorldAdvance(s,6);WorldStep(s,1,0,true);WorldAdvance(s,1,2);
                s=new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);BeginEncounter(s);
                Require(WorldLedger(s).LastStart==2&&WorldLedger(s).ActionSpent&&WorldLedger(s).MovementSpent==new RuleQuantity(5)
                    &&s.Capture().LifeEvents.Length==0&&s.Capture().Encounter.ObservedOrdinals.SequenceEqual(new[]{2}),"Saved Start repeated on entry.");
            });
            cases.Add("connected_combat_entry_interrupts_participant_intake_but_remote_crop_continues",()=>{
                var s=World(ConnectedPolicy());FarmWork(s,CommandKind.PlantCrop);Eat(s,new RuleQuantity(1));WorldAdvance(s,90);BeginEncounter(s);
                Require(s.Capture().Intakes.Single().Status==IntakeStatus.CombatInterrupted&&Eaten(s)==new RuleQuantity(1,10)
                    &&Crop(s).Tasks[0].Status==CropWorkStatus.Working&&Crop(s).Tasks[0].Progress==T(90),"Entry reset intake or stopped remote worker.");
                RejectUnchanged(s,host,IC(s,CommandKind.AdvanceClock,x:5,y:1),"TacticalDecisionClockPaused");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));ConnectedEnd(s);
                Require(Crop(s).Tasks[0].Progress==T(93)&&Eaten(s)==new RuleQuantity(1,10),"Tactical elapsed work or intake interruption wrong.");
            });
            cases.Add("connected_combat_exact_boundary_restore_entry_does_not_repeat_expiry",()=>{
                var p=ConnectedPolicy(conditions:new ConditionCombatFixture(CCApply("blind","Blinded",expires:new ConditionStamp(T(6)))));
                var s=World(p);CCDispatch(s,"blind");WorldAdvance(s,6);
                Require(!TestOnlyClubAttackPolicy.ConditionsFor(s.Capture(),TestOnlyPolicy.ActorId).View().Has(ConditionKind.Blinded),"Boundary expiry was not processed before entry.");
                s=new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);var before=s.Capture();BeginEncounter(s);var after=s.Capture();
                Require(after.RuleClock==T(6)&&after.WorldSchedule.ProcessedSlot==2&&after.Encounter.ObservedOrdinals.SequenceEqual(new[]{2})
                    &&after.LifeEvents.Length==before.LifeEvents.Length&&after.Conditions.Length==before.Conditions.Length&&after.Conditions.All(x=>before.Conditions.Any(y=>y.SameAs(x)))
                    &&after.WorldIntervals.All(x=>before.WorldIntervals.Any(y=>y.ActorId==x.ActorId&&y.LastStart==x.LastStart&&y.ActionSpent==x.ActionSpent&&y.MovementSpent==x.MovementSpent&&y.ReactionAvailable==x.ReactionAvailable)),
                    "Exact-boundary mode entry repeated a processed event or interval refresh.");
            });
            cases.Add("connected_combat_actual_attack_spends_shared_action_and_preserves_movement",()=>{
                var s=ConnectedArena(ConnectedPolicy(1));Require(WorldLedger(s).MovementSpent==new RuleQuantity(15),"Tactical step forgot10 exploration feet.");
                WorldCommit(s,Tac(s,CommandKind.AttackClub,AdditionalTacticalActor.Id,weapon:TestOnlyClubAttackPolicy.ActorClub));
                Require(WorldLedger(s).ActionSpent&&s.Capture().MeleeAttacks.Length==1,"Actual attack did not debit shared Action.");
                RejectUnchanged(s,host,Tac(s,CommandKind.AttackClub,AdditionalTacticalActor.Id,weapon:TestOnlyClubAttackPolicy.ActorClub),"ActionAlreadySpent");
                RejectUnchanged(s,host,Tac(s,CommandKind.EndFixedEncounter),"ConflictNotResolved");
            });
            cases.Add("dodge_uses_shared_action_persists_disadvantages_visible_attack_and_expires_at_next_start",()=>{
                var p=ConnectedPolicy(seed:SeedForDeath(16)).EnableDodgeAction();var s=ConnectedArena(p);
                var dodge=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.Dodge).Command;
                byte[] before=Bytes(s);uint random=s.Capture().RandomState;var preview=s.QueryCommand(host,dodge);
                Require(preview.Supported&&preview.Admissible&&preview.Costs.Any(x=>x.Kind=="action"&&x.Amount==1)
                    &&before.SequenceEqual(Bytes(s))&&s.Capture().RandomState==random,
                    "Dodge query changed the shared world or omitted its Action cost.");
                WorldCommit(s,dodge);
                Require(TestOnlyClubAttackPolicy.DodgeEffective(s.Capture(),TestOnlyPolicy.ActorId)
                    &&WorldLedger(s).ActionSpent,"Dodge did not use the shared Action interval or persist as active.");
                RejectUnchanged(s,host,Tac(s,CommandKind.AttackClub,AdditionalTacticalActor.Id,
                    weapon:TestOnlyClubAttackPolicy.ActorClub),"ActionAlreadySpent");
                byte[] saved=Bytes(s);s=new Simulation(p,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(s)),"Dodge changed through the shared-world save/restore.");
                ConnectedEnd(s);
                Require(s.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,"Dodge owner did not finish before the enemy turn.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                WorldCommit(s,Tac(s,CommandKind.AttackClub,TestOnlyPolicy.ActorId,actor:AdditionalTacticalActor.Id,weapon:AdditionalTacticalActor.ClubId));
                var incoming=s.Capture().MeleeAttacks.Single(x=>x.AttackerId==AdditionalTacticalActor.Id);
                Require(incoming.TargetId==TestOnlyPolicy.ActorId&&incoming.Attack.Second>0
                    &&incoming.Attack.Selected==Math.Min(incoming.Attack.First,incoming.Attack.Second),
                    "A visible enemy attack did not roll disadvantage against Dodge.");
                ConnectedEnd(s);var nextStart=s.Capture();
                Require(nextStart.Encounter.CurrentActor==TestOnlyPolicy.ActorId
                    &&nextStart.Dodges.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ExpiresAt==nextStart.RuleClock
                    &&!TestOnlyClubAttackPolicy.DodgeEffective(nextStart,TestOnlyPolicy.ActorId),
                    "Dodge did not expire at its owner's exact next regular start.");
            });
            cases.Add("connected_combat_remote_worker_cannot_be_attacked_or_act_in_encounter",()=>{
                var s=ConnectedArena();
                RejectUnchanged(s,host,Tac(s,CommandKind.AttackClub,TestOnlyPolicy.CompanionId,weapon:TestOnlyClubAttackPolicy.ActorClub),"TargetOutsideEncounter");
                RejectUnchanged(s,host,Tac(s,CommandKind.SelectCombatStance,actor:TestOnlyPolicy.CompanionId,stance:(int)CombatStance.Guarded),"ActorOutsideEncounter");
                RejectUnchanged(s,host,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Mobile),"SharedMobileDistanceNotImplemented");
            });
            cases.Add("connected_combat_inventory_handling_remains_gated_before_schema19",()=>{
                var p=ConnectedPolicy();var s=World(p);BeginEncounter(s);
                Require(s.Capture().SchemaVersion==Snapshot.CalendarCombatSchema,"Fixture did not select the legacy shared-combat schema.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Stow)),"ClubCommandNotImplemented");
                Require(s.Capture().WorldIntervals.All(x=>x.Interactions==0&&!x.ActionSpent)&&s.Capture().InventoryInteractions==0,
                    "Legacy combat handling changed the schema14 world interval.");
            });
            cases.Add("connected_combat_opportunity_choice_survives_disk_and_spends_only_reaction",()=>{
                var p=ConnectedPolicy();var s=ConnectedArena(p);TacStep(s,2,0);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())!=null,"Hostile departure skipped ordinary OA.");
                RejectUnchanged(s,host,Tac(s,CommandKind.EndRegularTurn),"TacticalChoicePending");
                var path=Path.Combine(directory,"connected-opportunity.bin");new FileSaveStore().Save(path,s.Capture());s=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                WorldCommit(s,Opportunity(s,true,AdditionalTacticalActor.ClubId,press:PressHitInstruction.KeepExisting));
                Require(!WorldLedger(s,AdditionalTacticalActor.Id).ReactionAvailable&&!WorldLedger(s,AdditionalTacticalActor.Id).ActionSpent&&WorldLedger(s).MovementSpent==new RuleQuantity(20),"OA spent Action or duplicated movement.");
                ConnectedEnd(s);Require(WorldLedger(s,AdditionalTacticalActor.Id).ReactionAvailable,"Actual incoming Start did not refresh Reaction.");
            });
            cases.Add("connected_combat_knockout_continuation_keeps_paid_action",()=>{
                var p=ConnectedPolicy(1,SeedForDeath(16));var s=ConnectedArena(p);
                WorldCommit(s,Tac(s,CommandKind.AttackUnarmed,AdditionalTacticalActor.Id,knockout:AttackKnockoutMode.AskIfEligible));
                Require(s.Capture().MeleeAttacks.Single().Pending&&WorldLedger(s).ActionSpent,"Pending knockout did not preserve paid Action.");
                s=new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
                WorldCommit(s,Tac(s,CommandKind.ResolveKnockout,s.Capture().MeleeAttacks.Single().Id,choice:true));
                Require(s.Capture().Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Stable&&WorldLedger(s).ActionSpent,"Knockout resolution charged again or lost result.");
            });
            cases.Add("connected_combat_resolved_exit_finishes_outgoing_slot_without_refill",()=>{
                var p=ConnectedPolicy(1);var s=ConnectedArena(p);DefeatConnectedEnemy(s);var old=s.Capture();long slot=old.WorldSchedule.ProcessedSlot;
                var outgoing=old.WorldIntervals.Single(x=>x.ActorId==old.Encounter.CurrentActor);
                WorldCommit(s,Tac(s,CommandKind.EndFixedEncounter));var v=s.Capture();
                var retained=v.WorldIntervals.Single(x=>x.ActorId==outgoing.ActorId);
                Require(!v.InventoryCombat&&v.Encounter.Id==old.Encounter.Id&&v.RuleClock==old.WorldSchedule.Start(slot+1)
                    &&v.ClosedEncounters.Length==0&&retained.LastStart==outgoing.LastStart&&retained.ActionSpent==outgoing.ActionSpent&&retained.MovementSpent==outgoing.MovementSpent,
                    "Exit restarted encounter, archived continuation, refilled outgoing actor or awarded round.");
                BeginEncounter(s);Require(s.Capture().InventoryCombat&&s.Capture().Encounter.Id==old.Encounter.Id
                    &&s.Capture().WorldIntervals.All(x=>v.WorldIntervals.Any(y=>y.ActorId==x.ActorId&&y.LastStart==x.LastStart&&y.ActionSpent==x.ActionSpent&&y.MovementSpent==x.MovementSpent&&y.ReactionAvailable==x.ReactionAvailable)),"Reentry refilled ordinary allowance.");
            });
            cases.Add("connected_combat_full_three_layer_loop_retains_crop_and_inventory",()=>{
                var p=ConnectedPolicy(1);var s=World(p);FarmWork(s,CommandKind.PlantCrop);
                WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(s,3,0);DefeatConnectedEnemy(s);WorldCommit(s,Tac(s,CommandKind.EndFixedEncounter));
                Require(Crop(s).Tasks[0].Progress==s.Capture().RuleClock&&Crop(s).Tasks[0].Status==CropWorkStatus.Working,"Combat discarded remote crop work.");
                WorldStep(s,0,1);WorldAdvance(s,1);WorldStep(s,0,1);WorldAdvance(s,1);
                FarmUntil(s,T(3600));for(int day=0;day<6;day++){FarmUntil(s,FarmDifference(Crop(s).CareUntil.Value,T(900)));FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,900);}
                FarmUntil(s,T(608400));FarmWork(s,CommandKind.HarvestCrop);WorldAdvance(s,3600);
                string food=HandleI(s,s.Capture().CropFood.Single().LotId,new RuleQuantity(2,3),HandlingKind.Pickup);Eat(s,new RuleQuantity(2,3),food);WorldAdvance(s,600);
                var path=Path.Combine(directory,"connected-three-layer-loop.bin");new FileSaveStore().Save(path,s.Capture());s=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                WorldStep(s,-1,0);WorldAdvance(s,1);
                Require(Eaten(s)==new RuleQuantity(2,3)&&s.Capture().Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Dead&&s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==2,
                    "Three-layer loop lost combat outcome, actual intake or further exploration.");
            });
            cases.Add("connected_exploration_combat_and_assigned_mining_share_one_saved_timeline",()=>{
                var fixture=new SharedMiningFixture(siteX:1,siteY:3);
                var p=TestOnlySharedWorldPolicy.WithMining(fixture,enemyHp:1).EnableExpeditionAssignments();
                var s=World(p);
                var selection=new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,
                    new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom);
                var request=new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.MiningExtraction,
                    SharedMiningFixture.DepositId,miningSelection:selection);
                var assign=ExpeditionCommand(s,CommandKind.AssignExpeditionWork,request:request);
                WorldCommit(s,assign);
                WorldStep(s,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                WorldStep(s,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                var assignment=s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status==ExpeditionAssignmentStatus.Ready&&assignment.SiteX==fixture.SiteX
                    &&assignment.SiteY==fixture.SiteY,"Companion did not reach the assignment's authored mining site.");
                WorldCommit(s,ExpeditionCommand(s,CommandKind.StartExpeditionWork,assignment.Id));
                var started=s.Capture().MiningAttempts.Single();
                Require(started.Status==MiningAttemptStatus.Working&&started.WorkerId==TestOnlyPolicy.CompanionId
                    &&s.Capture().ExpeditionAssignments.Single().Status==ExpeditionAssignmentStatus.Started
                    &&s.Capture().ExpeditionAssignments.Single().WorkId==started.Id,
                    "Assignment did not retain the existing mining attempt as authoritative work.");

                byte[] beforeApproach=Bytes(s);
                s=new Simulation(p,new SnapshotCodec().Decode(beforeApproach),ExecutionProfile.Laboratory);
                Require(beforeApproach.SequenceEqual(Bytes(s)),"Active assignment changed during save/restore before combat.");
                WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);
                Require(s.Capture().InventoryCombat&&s.Capture().Encounter!=null
                    &&!s.Capture().Encounter.Order.Contains(TestOnlyPolicy.CompanionId),
                    "Exploration did not enter tactical combat while keeping the assigned worker off-calendar.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                TacStep(s,3,0);
                RuleTime workAtEntry=s.Capture().MiningAttempts.Single().WorkDone;
                DefeatConnectedEnemy(s);WorldCommit(s,Tac(s,CommandKind.EndFixedEncounter));
                var afterCombat=s.Capture();var continuing=afterCombat.MiningAttempts.Single();
                Require(!afterCombat.InventoryCombat&&continuing.Status==MiningAttemptStatus.Working
                    &&continuing.WorkDone>workAtEntry&&afterCombat.ExpeditionAssignments.Single().WorkId==continuing.Id,
                    "Tactical time failed to continue the remote assignment or changed its linked procedure.");

                string path=Path.Combine(directory,"connected-assigned-mining-after-combat.bin");
                var store=new FileSaveStore();store.Save(path,afterCombat);
                byte[] saved=File.ReadAllBytes(path);
                s=new Simulation(p,store.Load(path),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(s)),"Post-combat save/restore changed work, encounter or assignment history.");
                WorldAdvance(s,continuing.DurationSeconds);
                var settled=s.Capture();var result=settled.MiningAttempts.Single();
                bool resolved=result.Status==MiningAttemptStatus.Success||result.Status==MiningAttemptStatus.CriticalSuccess
                    ||result.Status==MiningAttemptStatus.Failure||result.Status==MiningAttemptStatus.CriticalFailure;
                Require(resolved&&result.WorkDone==new RuleTime(result.DurationSeconds)
                    &&settled.MiningAttempts.Length==1&&settled.MiningUnits.Length==2
                    &&settled.ExpeditionAssignments.Single().WorkId==result.Id,
                    "Mining failed to settle exactly one valid source-selected attempt after the encounter.");
                byte[] settledBytes=Bytes(s);
                Require(s.Execute(host,assign).Outcome==Outcome.Duplicate&&settledBytes.SequenceEqual(Bytes(s))
                    &&s.Capture().MiningAttempts.Length==1,
                    "Replaying the original assignment duplicated work or changed the finite deposit.");
                var beforeContinue=s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId);
                var continuation=IC(s,CommandKind.BeginWorldStep,"walk",actor:TestOnlyPolicy.ActorId,x:-1,y:0);
                var continued=s.Execute(host,continuation);
                Require(continued.Outcome==Outcome.Committed,$"Post-settlement exploration from ({beforeContinue.X},{beforeContinue.Y}) west was rejected: {continued.Code}.");
                WorldAdvance(s,1);
                Require(s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1
                    &&s.Capture().MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA).Status==MiningUnitStatus.Extracted,
                    "Exploration did not continue after combat, mining settlement and save/restore.");
            });
            cases.Add("connected_combat_off_grid_entry_rejects_and_preserves_partial_position",()=>{
                var s=World(ConnectedPolicy());WorldStep(s,1,0);WorldAdvance(s,2,5);
                RejectUnchanged(s,host,IC(s,CommandKind.BeginFixedEncounter),"OffGridCombatEntryUnsupported");
                Require(s.Capture().WorldTraversals.Single().DistanceFeet==new RuleQuantity(2),"Entry snapped position.");
            });
            cases.Add("connected_combat_fractional_exploration_cost_survives_tactical_spending",()=>{
                var cure=new ConditionFixtureEvent(TestOnlyPolicy.ActorId,ConditionOperation.Cure("event.stand",new ConditionStamp(T(2,5)),"Prone"));
                var p=new TestOnlySharedWorldPolicy(new SharedCombatFixture(),30,new ConditionCombatFixture(CCApply("down","Prone"),cure),new TacticalTerrainCell(1,0,TerrainCost.Difficult));
                var s=World(p);CCDispatch(s,"down");WorldStep(s,1,0);WorldAdvance(s,2,5);CCDispatch(s,"stand");WorldAdvance(s,26,15);BeginEncounter(s);
                Require(WorldLedger(s).MovementSpent==new RuleQuantity(32,3),"Entry rounded earlier terrain/crawl expenditure.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(s,1,1);
                Require(WorldLedger(s).MovementSpent==new RuleQuantity(47,3),"Tactical step rounded the fractional shared ledger.");
            });
            cases.Add("connected_combat_entry_pauses_two_hand_fill_without_freeing_reserved_capacity",()=>{
                var wake=new ConditionFixtureEvent(TestOnlyPolicy.ActorId,ConditionOperation.Cure("event.wake",new ConditionStamp(T(6)),"Unconscious"));
                var p=ConnectedPolicy(conditions:new ConditionCombatFixture(CCApply("sleep","Unconscious",at:new ConditionStamp(T(6))),wake));
                var s=World(p);FarmWork(s,CommandKind.PlantCrop);
                foreach(var step in new[]{new[]{0,1},new[]{0,1},new[]{1,0},new[]{1,0},new[]{1,0}}){WorldStep(s,step[0],step[1]);WorldAdvance(s,1);}
                WorldAdvance(s,1);CCDispatch(s,"sleep");CCDispatch(s,"wake");
                WorldCommit(s,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(new RuleQuantity(1),TestOnlyFillingPolicy.FlaskId)));
                WorldAdvance(s,10);BeginEncounter(s);var v=s.Capture();
                Require(v.WaterFills.Single().Status==WaterFillStatus.Paused&&v.WaterFills.Single().Progress==T(10)
                    &&WaterFilling.FreeCapacity(v,TestOnlyFillingPolicy.FlaskId)==default&&Crop(s).Tasks[0].Status==CropWorkStatus.Working,"Entry lost fill progress/reservation or paused remote crop.");
            });
        }
    }
}
#endif
