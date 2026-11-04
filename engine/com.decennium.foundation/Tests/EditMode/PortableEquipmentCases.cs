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
        private static TestOnlySharedWorldPolicy PortablePolicy(uint seed=1)
            =>new TestOnlySharedWorldPolicy(new PortableKitFixture(),new SharedCombatFixture(seed:seed),new SupplyCacheFixture());
        private static Simulation PortableWorld(TestOnlySharedWorldPolicy policy=null)
        {policy=policy??PortablePolicy();return new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);}
        private static Command Portable(Simulation s,CommandKind kind,string target,string destination="",HandlingKind handling=HandlingKind.Pickup,
            string actor=TestOnlyPolicy.ActorId)
        {
            var v=s.Capture();bool transfer=kind==CommandKind.HandlePortableEquipment;
            return new Command("portable.command."+(v.Revision+1),actor,v.Revision,kind,target,
                inventory:transfer?new InventoryRequest(new RuleQuantity(1),destination,handling):null);
        }
        private static void PortableCommit(Simulation s,Command c)
        {var r=s.Execute(TestOnlySharedWorldPolicy.Host(),c);Require(r.Outcome==Outcome.Committed,c.Kind+" expected commit: "+r.Code);}
        private static void PortableMoveToCache(Simulation s)
        {WorldStep(s,1,0);WorldAdvance(s,3,2);WorldStep(s,0,1);WorldAdvance(s,3,2);}
        private static void AddPortableEquipmentCases(Dictionary<string,Action> cases,string directory)
        {
            var codec=new SnapshotCodec();var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("portable_equipment_schema20_exact_pack_mass_burden_and_roundtrip",()=>{
                var p=PortablePolicy();var s=PortableWorld(p);var v=s.Capture();var pack=v.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Pack);
                var load=PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.ActorId);
                Require(v.SchemaVersion==Snapshot.PortableEquipmentSchema&&PortableEquipmentRules.FixtureFitValid(v,pack)
                    &&pack.Open&&pack.Placement==PortablePlacement.Worn&&pack.CapacityPounds==new RuleQuantity(30)
                    &&load.Pounds==new RuleQuantity(63)&&load.Load==new RuleQuantity(63,10)&&PortableEquipmentRules.IsBurdened(v,TestOnlyPolicy.ActorId)
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(v,TestOnlyPolicy.ActorId)==20,
                    "The exact 28-pound internal fit, externally attached source gear, pouch and held club did not produce the authored 63-pound burden.");
                Require(v.Work.Lots.Single(x=>x.Id==PortableKitFixture.Rations).Amount==new RuleQuantity(20)
                    &&v.Work.Lots.Single(x=>x.Id==PortableKitFixture.Water).Amount==new RuleQuantity(4)
                    &&v.Vessels.Single(x=>x.Id==PortableKitFixture.Skin).LocationId==PortableKitFixture.Pack
                    &&v.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Rope).Placement==PortablePlacement.Attached,
                    "Physical contents, source water or the external rope attachment were duplicated or misplaced.");
                var encoded=codec.Encode(v);Require(encoded.SequenceEqual(codec.Encode(codec.Decode(encoded))),"Schema20 portable equipment did not round-trip canonically.");
                Throws<InvalidOperationException>(()=>new Simulation(p,v,ExecutionProfile.Release));
            });
            cases.Add("portable_equipment_fit_records_and_fixture_are_detached_readonly",()=>{
                var s=PortableWorld();var v=s.Capture();byte[] before=Bytes(s);
                var item=v.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Pack);
                var recordSet=(IList<string>)item.FitMemberIds;
                var fixtureSet=(IList<string>)PortableKitFixture.FitMembers;
                Throws<NotSupportedException>(()=>recordSet[0]="TEST_ONLY.forged-fit-member");
                Throws<NotSupportedException>(()=>fixtureSet[0]="TEST_ONLY.forged-fixture-member");
                Require(before.SequenceEqual(Bytes(s))&&PortableEquipmentRules.FixtureFitValid(s.Capture(),s.Capture().PortableEquipment.Single(x=>x.Id==PortableKitFixture.Pack)),
                    "A detached snapshot or public fixture profile changed the authoritative fit rule.");
            });
            cases.Add("portable_equipment_does_not_relabel_unrelated_food_as_pack_rations",()=>{
                var p=PortablePolicy();var s=p.Initial();
                OrdinaryInventory.Descendant(s,TestOnlyInventoryPolicy.FoodId,"TEST_ONLY.generic-food-lot",new RuleQuantity(1),
                    TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId,InventoryAccess.Ready);
                var food=s.PortableEquipment.Single(x=>x.Id=="TEST_ONLY.generic-food-lot");
                Require(food.ProfileId=="prototype.food-lot"&&s.Work.Lots.Single(x=>x.Id==food.LinkedId).Amount==new RuleQuantity(1),
                    "Nutrition kind was treated as proof that unrelated food came from the Explorer's Pack rations profile.");
            });
            cases.Add("portable_equipment_splitting_a_stowed_lot_preserves_exact_fit_and_mass",()=>{
                var p=PortablePolicy();var s=PortableWorld(p);var before=PortableEquipmentRules.CarriedBurden(s.Capture(),TestOnlyPolicy.ActorId);
                var v=s.Capture();var split=new Command("portable.portion.rations",TestOnlyPolicy.ActorId,v.Revision,CommandKind.PortionInventory,
                    PortableKitFixture.Rations,inventory:new InventoryRequest(new RuleQuantity(5),"",HandlingKind.Pickup));
                PortableCommit(s,split);v=s.Capture();var child=v.InventoryLots.Single(x=>x.ParentId==PortableKitFixture.Rations);
                var physical=v.PortableEquipment.Single(x=>x.Id==child.LotId);
                var after=PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.ActorId);
                Require(child.CreatedAmount==new RuleQuantity(5)&&child.Access==InventoryAccess.Stowed
                    &&v.Work.Lots.Single(x=>x.Id==child.LotId).LocationId==PortableKitFixture.Pack&&physical.ParentId==PortableKitFixture.Pack
                    &&before.Pounds==after.Pounds&&before.Load==after.Load&&v.Work.Lots.Single(x=>x.Id==PortableKitFixture.Rations).Amount==new RuleQuantity(15),
                    "A no-movement portion changed containment, source mass or known fit.");
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,child.LotId,handling:HandlingKind.Retrieve));
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,child.LotId,PortableKitFixture.Pack,HandlingKind.Stow));
                v=s.Capture();Require(v.PortableEquipment.Single(x=>x.Id==child.LotId).ParentId==PortableKitFixture.Pack
                    &&v.InventoryLots.Single(x=>x.LotId==child.LotId).Access==InventoryAccess.Stowed
                    &&PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==before.Pounds,
                    "A retrieved portion could not return to its authored pack fit set without changing mass.");
                byte[] bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,codec.Decode(bytes),ExecutionProfile.Laboratory))),
                    "A portioned pack did not survive canonical save/load.");
                var rootPack=PortableWorld(p);
                var rootView=rootPack.Capture();
                WorldCommit(rootPack,new Command("portable.portion.root",TestOnlyPolicy.ActorId,rootView.Revision,CommandKind.PortionInventory,
                    PortableKitFixture.Rations,inventory:new InventoryRequest(new RuleQuantity(5),"",HandlingKind.Pickup)));
                PortableCommit(rootPack,Portable(rootPack,CommandKind.HandlePortableEquipment,PortableKitFixture.Rations,handling:HandlingKind.Retrieve));
                var splitView=rootPack.Capture();var splitChild=splitView.InventoryLots.Single(x=>x.ParentId==PortableKitFixture.Rations);
                Require(splitView.PortableEquipment.Single(x=>x.Id==splitChild.LotId).ParentId==PortableKitFixture.Pack
                    &&splitView.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Rations).ParentId==""
                    &&PortableEquipmentRules.CarriedBurden(splitView,TestOnlyPolicy.ActorId).Pounds==new RuleQuantity(63),
                    "Retrieving a source remainder invalidated the authored fit of its in-pack portion.");
                bytes=Bytes(rootPack);Require(bytes.SequenceEqual(Bytes(new Simulation(p,codec.Decode(bytes),ExecutionProfile.Laboratory))),
                    "Fit provenance for a remaining portion did not survive save/load.");
            });
            cases.Add("portable_equipment_rejects_unknown_key_mass_and_untracked_vessel_move",()=>{
                Throws<ArgumentException>(()=>new TestOnlySharedWorldPolicy(new PortableKitFixture(),new SharedCombatFixture(),new SupplyCacheFixture(hasKey:true)));
                var s=PortableWorld();PortableMoveToCache(s);
                var move=new Command("portable.untracked-vessel",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.HandleVessel,
                    TestOnlyFillingPolicy.ActorSkinId,inventory:new InventoryRequest(new RuleQuantity(1),"",HandlingKind.Pickup));
                RejectUnchanged(s,host,move,"PortableEquipmentRequired");
            });
            cases.Add("portable_equipment_tracks_companion_skin_and_filled_water_mass",()=>{
                var s=PortableWorld();var initial=PortableEquipmentRules.CarriedBurden(s.Capture(),TestOnlyPolicy.CompanionId);
                Require(initial.Pounds==new RuleQuantity(2),"The companion's carried empty waterskin tare was omitted.");
                WorldCommit(s,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(4),TestOnlyFillingPolicy.CompanionSkinId),TestOnlyPolicy.CompanionId));
                WorldAdvance(s,60);var v=s.Capture();var fill=v.WaterFills.Single(x=>x.DestinationId==TestOnlyFillingPolicy.CompanionSkinId);
                var output=v.InventoryLots.Single(x=>x.LotId==fill.OutputLotId);var full=PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.CompanionId);
                Require(full.Pounds==new RuleQuantity(6)&&v.PortableEquipment.Single(x=>x.Id==output.LotId).ParentId==TestOnlyFillingPolicy.CompanionSkinId,
                    "Completed water did not add to the companion's one-pound skin tare exactly once.");
                WorldCommit(s,IC(s,CommandKind.StartIntake,output.LotId,new InventoryRequest(new RuleQuantity(1)),TestOnlyPolicy.CompanionId));
                WorldAdvance(s,60);v=s.Capture();var after=PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.CompanionId);
                Require(after.Pounds==new RuleQuantity(5)&&v.Work.Lots.Single(x=>x.Id==output.LotId).Amount==new RuleQuantity(3),
                    "Consuming one pint did not reduce the physically carried liquid mass.");
            });
            cases.Add("portable_equipment_handover_rejects_recipient_with_active_traversal",()=>{
                var s=PortableWorld();PortableMoveToCache(s);
                foreach(var step in new[]{(0,1),(1,0),(1,0)}){WorldStep(s,step.Item1,step.Item2);WorldAdvance(s,3,2);}
                PortableCommit(s,Portable(s,CommandKind.RemovePortableItem,PortableKitFixture.Pack));
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,TestOnlyPolicy.CompanionId,
                    HandlingKind.Handover,TestOnlyPolicy.ActorId));
                WorldStep(s,-1,0);
                var handover=Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,TestOnlyPolicy.ActorId,
                    HandlingKind.Handover,TestOnlyPolicy.CompanionId);
                RejectUnchanged(s,host,handover,"RecipientTraversalInProgress");
            });
            cases.Add("portable_equipment_retrieve_tools_then_use_cache_and_save",()=>{
                var p=PortablePolicy(PortableToolSeed());var s=PortableWorld(p);PortableMoveToCache(s);
                RejectUnchanged(s,host,SupplyCommand(s,SupplyCacheInteraction.PickWithTools),"ActualThievesToolsRequired");
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Tools,handling:HandlingKind.Retrieve));
                var retrieved=s.Capture();Require(retrieved.SupplyCacheEquipment.Single(x=>x.Id==PortableKitFixture.Tools).LocationId==TestOnlyPolicy.ActorId
                    &&retrieved.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Tools).ParentId==""
                    &&retrieved.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Tools).OwnerId==TestOnlyPolicy.ActorId,
                    "Tool retrieval did not change actual access while preserving ownership.");
                string path=Path.Combine(directory,"portable-tools-retrieved.ddsave");new FileSaveStore().Save(path,retrieved);
                s=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                var start=SupplyCommand(s,SupplyCacheInteraction.PickWithTools);SupplyCommit(s,start);WorldAdvance(s,6);
                Require(!s.Capture().SupplyCaches.Single().Locked&&s.Capture().SupplyCacheAttempts.Single().Status==SupplyCacheAttemptStatus.Succeeded,
                    "A retrieved physical tool could not complete its actual cache operation.");
                byte[] paid=Bytes(s);Require(s.Execute(host,start).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(paid),"Restored duplicate repeated tool work or dice.");
            });
            cases.Add("portable_equipment_drop_recover_and_handover_preserve_lots_and_ownership",()=>{
                var p=PortablePolicy();var s=PortableWorld(p);PortableMoveToCache(s);
                PortableCommit(s,Portable(s,CommandKind.RemovePortableItem,PortableKitFixture.Pack));
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,handling:HandlingKind.Drop));
                var dropped=s.Capture();var burden=PortableEquipmentRules.CarriedBurden(dropped,TestOnlyPolicy.ActorId);
                Require(dropped.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Pack).Placement==PortablePlacement.Ground
                    &&burden.Pounds==new RuleQuantity(3)&&!PortableEquipmentRules.IsBurdened(dropped,TestOnlyPolicy.ActorId)
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(dropped,TestOnlyPolicy.ActorId)==30
                    &&dropped.Work.Lots.Single(x=>x.Id==PortableKitFixture.Rations).LocationId==PortableKitFixture.Pack,
                    "Dropping a worn pack did not remove its full carried burden or preserve its contents on the ground.");
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,handling:HandlingKind.Pickup));
                foreach(var step in new[]{(0,1),(1,0),(1,0)}){WorldStep(s,step.Item1,step.Item2);WorldAdvance(s,3,2);}
                PortableCommit(s,Portable(s,CommandKind.EquipPortableItem,PortableKitFixture.Pack));
                PortableCommit(s,Portable(s,CommandKind.RemovePortableItem,PortableKitFixture.Pack));
                var rationsBefore=s.Capture().InventoryLots.Single(x=>x.LotId==PortableKitFixture.Rations);
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,TestOnlyPolicy.CompanionId,HandlingKind.Handover));
                var v=s.Capture();var pack=v.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Pack);var contents=v.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Rations);
                Require(pack.CustodianId==TestOnlyPolicy.CompanionId&&contents.CustodianId==TestOnlyPolicy.CompanionId&&contents.OwnerId==TestOnlyPolicy.ActorId
                    &&v.InventoryLots.Single(x=>x.LotId==PortableKitFixture.Rations).CreatedAt==rationsBefore.CreatedAt
                    &&v.Work.Lots.Single(x=>x.Id==PortableKitFixture.Rations).LocationId==PortableKitFixture.Pack
                    &&v.SupplyCacheEquipment.Single(x=>x.Id==PortableKitFixture.Tools).OwnerId==TestOnlyPolicy.ActorId
                    &&v.SupplyCacheEquipment.Single(x=>x.Id==PortableKitFixture.Tools).CustodianId==TestOnlyPolicy.CompanionId,
                    "Handing over the full pack changed content ownership, freshness history, custody or containment.");
                var bytes=Bytes(s);var restored=new Simulation(p,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),"Handover did not survive a schema20 save/load.");
            });
            cases.Add("portable_equipment_tactical_unload_preserves_spent_movement",()=>{
                var s=PortableWorld();WorldCommit(s,IC(s,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(s,0,1);
                var before=s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(before.MovementSpent==new RuleQuantity(5)&&TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId)==20,
                    "Burdened tactical movement did not use the reduced Speed.");
                PortableCommit(s,Portable(s,CommandKind.RemovePortableItem,PortableKitFixture.Pack));
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Pack,handling:HandlingKind.Drop));
                var unloaded=s.Capture();var interval=unloaded.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(interval.MovementSpent==before.MovementSpent&&interval.Interactions==2&&interval.ActionSpent
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(unloaded,TestOnlyPolicy.ActorId)==30,
                    "Unloading refunded tactical movement or failed to restore current Speed.");
                TacStep(s,0,2);var after=s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(after.MovementSpent==new RuleQuantity(10)&&s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==2,
                    "The actor could not spend newly available movement while retaining its prior five feet.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(PortablePolicy(),codec.Decode(bytes),ExecutionProfile.Laboratory))),
                    "Tactical portable interactions failed authoritative replay after reload.");
            });
        }
        private static uint PortableToolSeed()
        {
            for(uint seed=1;seed<10000;seed++)if(DiceStream.Draw(seed,20).Value+1+PlaytestCharacters.AbilityModifier(14)+PlaytestCharacters.ProficiencyBonus(3)>=15)return seed;
            throw new InvalidOperationException("No deterministic cache-success seed found.");
        }
    }
}
#endif
