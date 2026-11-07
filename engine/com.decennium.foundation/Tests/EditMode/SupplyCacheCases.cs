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
        private static TestOnlySharedWorldPolicy SupplyPolicy(bool toolsProficient=true,bool hasKey=false,bool hasTools=true,uint seed=1,ConditionCombatFixture conditions=null,bool connected=false)
        {
            var combat=connected?new SharedCombatFixture(seed:seed):null;
            return new TestOnlySharedWorldPolicy(combat,null,null,null,null,new SupplyCacheFixture(toolsProficient,hasKey,hasTools),conditions:conditions);
        }
        private static Simulation SupplyWorld(TestOnlySharedWorldPolicy p)=>World(p);
        private static Command SupplyCommand(Simulation s,SupplyCacheInteraction action,string actor=TestOnlyPolicy.ActorId,string id=null)
            =>IC(s,CommandKind.Interact,SupplyCacheFixture.CacheId,actor:actor,x:(int)action,id:id);
        private static void SupplyApproach(Simulation s)
        {
            WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,0,1);WorldAdvance(s,1);
            var actor=s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId);
            Require(actor.X==1&&actor.Y==1,"The authored cache approach did not reach its adjacent interaction point.");
        }
        private static void SupplyCommit(Simulation s,Command c)
        {var result=s.Execute(TestOnlySharedWorldPolicy.Host(),c);Require(result.Outcome==Outcome.Committed,c.Kind+" x="+c.X+" y="+c.Y+" target="+c.Target+" rev="+c.ExpectedRevision+": "+result.Code);}
        private static uint FailedThenSuccessSeed()
        {
            for(uint seed=1;seed<100000;seed++) {
                var first=DiceStream.Draw(seed,20);var second=DiceStream.Draw(first.NextState,20);
                if(first.Value+1<15&&second.Value+1>=15)return seed;
            }
            throw new InvalidOperationException("No deterministic binary lock seed found.");
        }
        private static uint PoisonedDisadvantageSeed()
        {
            for(uint seed=1;seed<100000;seed++) {
                var first=DiceStream.Draw(seed,20);var second=DiceStream.Draw(first.NextState,20);
                if(first.Value+1>=15&&second.Value+1<15)return seed;
            }
            throw new InvalidOperationException("No deterministic poisoned-check contrast seed found.");
        }
        private static uint SuccessfulPickSeed(bool proficient)
        {
            int modifier=proficient?PlaytestCharacters.ProficiencyBonus(3):0;
            for(uint seed=1;seed<100000;seed++) {
                var roll=DiceStream.Draw(seed,20);
                if(PlaytestRolls.TaskCheck(roll.Value+1,modifier,15).Success)return seed;
            }
            throw new InvalidOperationException("No deterministic successful lockpick seed found.");
        }
        private static void AddSupplyCacheCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("supply_cache_schema19_closed_access_and_authored_stock",()=>{
                var p=SupplyPolicy();var s=SupplyWorld(p);var v=s.Capture();
                Require(v.SchemaVersion==Snapshot.SupplyCacheSchema&&v.SupplyCaches.Single().Locked&&!v.SupplyCaches.Single().Open,
                    "The explicitly selected cache state was not locked in schema19.");
                Require(v.Work.Lots.Single(x=>x.Id==TestOnlyInventoryPolicy.FoodId).LocationId==SupplyCacheFixture.CacheId
                    &&v.Vessels.Single(x=>x.Id==TestOnlyFillingPolicy.ActorSkinId).LocationId==SupplyCacheFixture.CacheId
                    &&v.Work.Lots.Single(x=>x.Id==TestOnlyInventoryPolicy.WaterId).Amount==new RuleQuantity(4),
                    "Finite ration or filled waterskin stock was not placed in the cache.");
                var burden=TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.ActorId);
                Require(burden.Pounds.HasValue&&burden.Pounds.Value==new RuleQuantity(4),
                    "Carried thieves' tools did not add their sourced one-pound mass to pouch and held club weight: "+burden.Pounds+".");
                var path=Path.Combine(directory,"schema19-initial.bin");new FileSaveStore().Save(path,v);
                var restored=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)),"Initial supply cache did not round-trip.");
                SupplyApproach(s);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(2))),"InventoryOutOfReach");
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.Open),"SupplyCacheLocked");
                Require(!s.Capture().SupplyCaches.Single().Open,"Rejected closed-container access changed the cache.");
            });
            cases.Add("supply_cache_tools_unlock_open_retrieve_and_consume_across_reload",()=>{
                var p=SupplyPolicy(seed:SuccessfulPickSeed(true),connected:true);var s=SupplyWorld(p);FarmWork(s,CommandKind.PlantCrop);SupplyApproach(s);
                var start=SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-tools-start");SupplyCommit(s,start);
                var pending=s.Capture();Require(pending.SupplyCacheAttempts.Single().Status==SupplyCacheAttemptStatus.Working
                    &&pending.SupplyCacheAttempts.Single().StartedAt==new RuleTime(2)&&pending.SupplyCacheAttempts.Single().StartedAt.AddSeconds(6)>pending.RuleClock
                    &&pending.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,"Tool unlock did not reserve a real staged Action and six-second interval.");
                byte[] paid=Bytes(s);Require(s.Execute(host,start).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(paid),"Duplicate unlock repeated cost.");
                var path=Path.Combine(directory,"pending-tools.bin");new FileSaveStore().Save(path,s.Capture());
                var restored=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)),"Pending unlock changed over reload.");
                WorldAdvance(restored,2);Require(restored.Capture().SupplyCacheAttempts.Single().Status==SupplyCacheAttemptStatus.Working,"Unlock completed before its six active seconds.");
                WorldAdvance(restored,4);var complete=restored.Capture();
                Require(complete.RuleClock==new RuleTime(8)&&!complete.SupplyCaches.Single().Locked&&!complete.SupplyCaches.Single().Open
                    &&complete.RandomState!=pending.RandomState&&complete.SupplyCacheAttempts.Single().Natural>0&&complete.Crops.Single().Tasks.Single().Progress==new RuleTime(8),
                    "The tools path did not check after shared time while the companion continued working.");
                byte[] beforeDuplicate=Bytes(restored);Require(restored.Execute(host,start).Outcome==Outcome.Duplicate&&Bytes(restored).SequenceEqual(beforeDuplicate),"Restored command receipt repeated the unlock.");
                SupplyCommit(restored,SupplyCommand(restored,SupplyCacheInteraction.Open));
                Require(restored.Capture().SupplyCaches.Single().Open&&restored.Capture().RuleClock==new RuleTime(9),"Opening was not a separate one-second interaction.");
                var opened=new Simulation(p,codec.Decode(Bytes(restored)),ExecutionProfile.Laboratory);
                string rationChild="inventory."+(opened.Capture().Revision+1)+".lot";
                SupplyCommit(opened,IC(opened,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(2))));
                var ration=opened.Capture().InventoryLots.Single(x=>x.LotId==rationChild);
                Require(ration.OwnerId==TestOnlyPolicy.ActorId&&ration.ParentId==TestOnlyInventoryPolicy.FoodId&&ration.CreatedAmount==new RuleQuantity(2)
                    &&opened.Capture().Work.Lots.Single(x=>x.Id==TestOnlyInventoryPolicy.FoodId).Amount==default,
                    "Ration retrieval lost ownership/provenance or regenerated the finite source lot.");
                var rationHandle=opened.Capture().Handling.Single(x=>x.ChildId==rationChild);
                Require(rationHandle.Kind==HandlingKind.Pickup,"Ration retrieval was not recorded as physical pickup.");
                SupplyCommit(opened,IC(opened,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,
                    new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Pickup)));
                var carried=opened.Capture();var vessel=carried.Vessels.Single(x=>x.Id==TestOnlyFillingPolicy.ActorSkinId);
                Require(vessel.LocationId==TestOnlyPolicy.ActorId&&vessel.CustodianId==TestOnlyPolicy.ActorId
                    &&carried.VesselContents.Single(x=>x.VesselId==vessel.Id).LotId==TestOnlyInventoryPolicy.WaterId
                    &&carried.Work.Lots.Single(x=>x.Id==TestOnlyInventoryPolicy.WaterId).Amount==new RuleQuantity(4),
                    "Waterskin retrieval changed physical liquid identity or amount.");
                SupplyCommit(opened,IC(opened,CommandKind.StartIntake,rationChild,new InventoryRequest(new RuleQuantity(2,3))));
                var foodPath=Path.Combine(directory,"rations-intake.bin");new FileSaveStore().Save(foodPath,opened.Capture());
                opened=new Simulation(p,new FileSaveStore().Load(foodPath),ExecutionProfile.Laboratory);WorldAdvance(opened,900);
                Require(opened.Capture().Intakes.Single().Status==IntakeStatus.Complete
                    &&opened.Capture().Work.Reservations.Single(x=>x.Id==opened.Capture().Intakes.Single().ReservationId).ConsumedAmount==new RuleQuantity(2,3),
                    "Reloaded ration intake did not consume exactly its declared portion.");
                SupplyCommit(opened,IC(opened,CommandKind.StartIntake,TestOnlyInventoryPolicy.WaterId,new InventoryRequest(new RuleQuantity(1))));WorldAdvance(opened,60);
                Require(opened.Capture().Work.Lots.Single(x=>x.Id==TestOnlyInventoryPolicy.WaterId).Amount==new RuleQuantity(3)
                    &&opened.Capture().InventoryLots.Single(x=>x.LotId==TestOnlyInventoryPolicy.WaterId).OwnerId==TestOnlyPolicy.ActorId,
                    "Water intake failed to preserve source ownership or exact remaining quantity.");
                var finalPath=Path.Combine(directory,"consumed-cache.bin");new FileSaveStore().Save(finalPath,opened.Capture());
                var final=new Simulation(p,new FileSaveStore().Load(finalPath),ExecutionProfile.Laboratory);
                Require(Bytes(opened).SequenceEqual(Bytes(final))&&final.Capture().SupplyCaches.Single().Open,
                    "Consumed cache history did not round-trip without restoring stock.");
                RejectUnchanged(final,host,IC(final,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1))),"InventoryQuantityUnavailable");
            });
            cases.Add("supply_cache_failed_pick_retries_full_duration_with_source_task_degrees",()=>{
                uint seed=FailedThenSuccessSeed();var p=SupplyPolicy(toolsProficient:false,hasKey:false,seed:seed,connected:true);var s=SupplyWorld(p);SupplyApproach(s);
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.UnlockWithKey),"PhysicalKeyUnavailable");
                var start=SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-pick-first");SupplyCommit(s,start);
                Require(s.Capture().RandomState==seed&&s.Capture().SupplyCaches.Single().Locked,"Lockpick rolled or unlocked before completion.");
                WorldAdvance(s,6);var fail=s.Capture().SupplyCacheAttempts.Single();
                Require(fail.Status==SupplyCacheAttemptStatus.Failed&&!fail.Tactical&&!PlaytestRolls.TaskCheck(fail.Natural,fail.Modifier,15).Success&&fail.Modifier==0
                    &&s.Capture().SupplyCaches.Single().Locked,"A failed binary pick gained a critical outcome or changed the lock.");
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-pick-retry"));WorldAdvance(s,6);
                var attempts=s.Capture().SupplyCacheAttempts.OrderBy(x=>x.StartedAt).ToArray();
                Require(attempts.Length==2&&attempts.All(x=>x.StartedAt.AddSeconds(6)==x.EndedAt.Value)
                    &&attempts[1].Status==SupplyCacheAttemptStatus.Succeeded&&PlaytestRolls.TaskCheck(attempts[1].Natural,attempts[1].Modifier,15).Success
                    &&!s.Capture().SupplyCaches.Single().Locked,"Retry skipped the full attempt or did not use ordinary binary success.");
            });
            cases.Add("supply_cache_key_path_and_unknown_key_burden_are_explicit",()=>{
                var p=SupplyPolicy(hasKey:true,hasTools:false);var s=SupplyWorld(p);SupplyApproach(s);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.UnlockWithKey,id:"cache-key-only"));WorldAdvance(s,6);
                Require(!s.Capture().SupplyCaches.Single().Locked&&s.Capture().SupplyCacheAttempts.Single().Status==SupplyCacheAttemptStatus.Succeeded
                    &&s.Capture().SupplyCacheAttempts.Single().Natural==0,"Physical key did not unlock without a check.");
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.Open,id:"cache-key-open"));
                var burden=TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.ActorId);
                Require(!burden.Pounds.HasValue&&!burden.Load.HasValue,
                    "Unspecified key mass was silently treated as zero in the carrying ledger.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,
                    new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Pickup)),"CarryingCapacityNotEstablished");
            });
            cases.Add("supply_cache_action_permission_authority_and_check_modifiers_are_revalidated",()=>{
                var events=new ConditionCombatFixture(CCApply("cache-dazed","Dazed",at:CJAt(2)));
                var p=SupplyPolicy(hasKey:true,hasTools:false,conditions:events);var s=SupplyWorld(p);SupplyApproach(s);CCDispatch(s,"cache-dazed");
                var before=Bytes(s);var denied=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},true,true);
                Require(s.Execute(denied,SupplyCommand(s,SupplyCacheInteraction.UnlockWithKey,id:"cache-no-grant")).Code=="InventoryNotAuthorized"
                    &&Bytes(s).SequenceEqual(before),"Cache credential use bypassed host inventory authority.");
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.UnlockWithKey),"ConditionPreventsAction");
                var duplicateWorld=SupplyWorld(SupplyPolicy(hasKey:true,hasTools:false));SupplyApproach(duplicateWorld);
                var keyCommand=SupplyCommand(duplicateWorld,SupplyCacheInteraction.UnlockWithKey,id:"cache-key-authority-duplicate");SupplyCommit(duplicateWorld,keyCommand);
                byte[] committed=Bytes(duplicateWorld);
                Require(duplicateWorld.Execute(denied,keyCommand).Code=="InventoryNotAuthorized"&&Bytes(duplicateWorld).SequenceEqual(committed),
                    "Duplicate key use bypassed the current inventory grant.");
                uint seed=PoisonedDisadvantageSeed();var plain=SupplyWorld(SupplyPolicy(hasKey:false,hasTools:true,toolsProficient:false,seed:seed,connected:true));SupplyApproach(plain);
                SupplyCommit(plain,SupplyCommand(plain,SupplyCacheInteraction.PickWithTools,id:"cache-pick-plain"));WorldAdvance(plain,6);
                var ordinary=plain.Capture().SupplyCacheAttempts.Single();
                var poisonedFixture=new ConditionCombatFixture(CCApply("cache-poison","Poisoned",at:CJAt(2)));
                var poisoned=SupplyWorld(SupplyPolicy(hasKey:false,hasTools:true,toolsProficient:false,seed:seed,conditions:poisonedFixture,connected:true));
                SupplyApproach(poisoned);CCDispatch(poisoned,"cache-poison");
                SupplyCommit(poisoned,SupplyCommand(poisoned,SupplyCacheInteraction.PickWithTools,id:"cache-pick-poisoned"));WorldAdvance(poisoned,6);
                var impaired=poisoned.Capture().SupplyCacheAttempts.Single();
                Require(ordinary.Natural>=15&&ordinary.Status==SupplyCacheAttemptStatus.Succeeded&&impaired.Natural<ordinary.Natural&&impaired.Status==SupplyCacheAttemptStatus.Failed,
                    "Poisoned did not apply disadvantage to the actual Dexterity tool check.");
                var injuredState=plain.Capture();
                var existingLife=injuredState.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                var injuredLife=new ActorLifeRecord(existingLife.ActorId,existingLife.MaximumHp,existingLife.Hp,existingLife.TemporaryHp,
                    new[]{(int)Injury.FineMotorTrauma},existingLife.Stable,existingLife.Dead,existingLife.UsesDeathSaves,
                    existingLife.DeathSuccesses,existingLife.DeathFailures,existingLife.StableUntil,existingLife.LastDeathTurn,
                    existingLife.Prone,existingLife.HeldItems);
                injuredState.Lives=injuredState.Lives.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?injuredLife:x).ToArray();
                var hero=CharacterStateFacts.ForActor(injuredState,TestOnlyPolicy.ActorId);
                Require(SupplyCacheRules.PickCheckModifier(hero,false)==PlaytestCharacters.AbilityModifier(hero.Character.Abilities[1])-1,
                    "Fine-Motor Injury was omitted from a Dexterity lock-manipulation check.");
            });
            cases.Add("supply_cache_blinded_task_requirement_is_an_authored_fixture_fact",()=>{
                var events=new ConditionCombatFixture(CCApply("cache-blind","Blinded",at:CJAt(2)));
                var p=SupplyPolicy(hasKey:false,hasTools:true,conditions:events);var s=SupplyWorld(p);SupplyApproach(s);CCDispatch(s,"cache-blind");
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-pick-blind"));WorldAdvance(s,6);
                var attempt=s.Capture().SupplyCacheAttempts.Single();
                Require(attempt.Status==SupplyCacheAttemptStatus.Failed&&attempt.AutomaticFailure&&attempt.Natural==0&&s.Capture().RandomState==SupplyWorld(SupplyPolicy(hasKey:false,hasTools:true)).Capture().RandomState,
                    "The sight-dependent pick task rolled dice while the authored lock was not visible.");
            });
            cases.Add("supply_cache_tactical_open_inventory_and_vessel_share_action_ledger",()=>{
                var p=SupplyPolicy(hasKey:false,hasTools:true,seed:SuccessfulPickSeed(true),connected:true);var s=SupplyWorld(p);SupplyApproach(s);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-tactical-tools"));WorldAdvance(s,6);
                BeginEncounter(s);
                for(int i=0;i<3&&s.Capture().Encounter.CurrentActor!=TestOnlyPolicy.ActorId;i++)ConnectedEnd(s);
                Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId,"Hero did not receive the tactical interval.");
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.Open,id:"cache-tactical-open"));
                Require(s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Interactions==1
                    &&s.Capture().InventoryInteractions==1,"Tactical opening was not recorded as the first ordinary interaction.");
                var child="inventory."+(s.Capture().Revision+1)+".lot";
                SupplyCommit(s,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(new RuleQuantity(1))));
                Require(s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Interactions==2
                    &&s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent
                    &&s.Capture().InventoryInteractions==2&&s.Capture().InventoryLots.Any(x=>x.LotId==child),
                    "The second tactical interaction failed to spend and record its Action.");
                RejectUnchanged(s,host,Tac(s,CommandKind.EncounterDash),"ActionAlreadySpent");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,
                    new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Pickup)),"InteractionBudgetUnavailable");
            });
            cases.Add("supply_cache_tactical_handling_rejects_unconscious_actor",()=>{
                var events=new ConditionCombatFixture(CCApply("cache-tactical-sleep","Unconscious",at:CJAt(9)));
                var p=SupplyPolicy(hasKey:false,hasTools:true,seed:SuccessfulPickSeed(true),connected:true,conditions:events);var s=SupplyWorld(p);SupplyApproach(s);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-sleep-tools"));WorldAdvance(s,6);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.Open,id:"cache-sleep-open"));
                CCDispatch(s,"cache-tactical-sleep");BeginEncounter(s);
                for(int i=0;i<3&&s.Capture().Encounter.CurrentActor!=TestOnlyPolicy.ActorId;i++)ConnectedEnd(s);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(2))),"WorkerCannotPerformTask");
            });
            cases.Add("supply_cache_interruption_retains_elapsed_time_and_cancels_check",()=>{
                var p=SupplyPolicy();var s=SupplyWorld(p);SupplyApproach(s);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-pick-interrupt"));uint seed=s.Capture().RandomState;
                WorldAdvance(s,2);SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.Interrupt));var state=s.Capture();var attempt=state.SupplyCacheAttempts.Single();
                Require(attempt.Status==SupplyCacheAttemptStatus.Interrupted&&attempt.EndedAt==new RuleTime(4)
                    &&attempt.Natural==0&&state.RuleClock==new RuleTime(4)&&state.RandomState==seed&&state.SupplyCaches.Single().Locked
                    &&state.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Interrupted attempt checked the lock, refunded Action, or rewound elapsed shared time.");
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.Interrupt),"NoActiveSupplyCacheAttempt");
            });
            cases.Add("supply_cache_unconscious_event_interrupts_staged_pick",()=>{
                var events=new ConditionCombatFixture(CCApply("cache-sleep","Unconscious",at:CJAt(4)));
                var p=SupplyPolicy(conditions:events);var s=SupplyWorld(p);SupplyApproach(s);
                SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,id:"cache-pick-sleep"));uint seed=s.Capture().RandomState;
                WorldAdvance(s,2);WorldCommit(s,new Command("cache-sleep-event",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DispatchConditionEvent,"event.cache-sleep"));
                var state=s.Capture();var attempt=state.SupplyCacheAttempts.Single();
                Require(attempt.Status==SupplyCacheAttemptStatus.Interrupted&&attempt.EndedAt==new RuleTime(4)&&attempt.Natural==0
                    &&state.RandomState==seed&&state.SupplyCaches.Single().Locked,
                    "A same-time incapacity failed to interrupt the unfinished check before resolution.");
            });
            cases.Add("supply_cache_requires_actual_unlocking_item_and_owner_access",()=>{
                var p=SupplyPolicy(toolsProficient:false,hasKey:false,hasTools:false);var s=SupplyWorld(p);SupplyApproach(s);
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.PickWithTools),"ActualThievesToolsRequired");
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.UnlockWithKey),"PhysicalKeyUnavailable");
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.PickWithTools,TestOnlyPolicy.CompanionId),"NoSupplyCachePermission");
                var noInventory=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},true,true);
                RejectUnchanged(s,noInventory,SupplyCommand(s,SupplyCacheInteraction.Open),"InventoryNotAuthorized");
            });
        }
    }
}
#endif
