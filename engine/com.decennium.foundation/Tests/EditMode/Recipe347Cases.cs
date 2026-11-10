#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy Recipe347Policy(uint seed=1,SharedMiningFixture mining=null)
            =>CampConstructionPolicy(seed,storage:true,mining:mining??new SharedMiningFixture(),
                crafting:new SharedCraftingFixture(toolHp:0),recipe347:true);

        private static void Recipe347StandardPolicy(out TestOnlySharedWorldPolicy policy,out Snapshot initial,
            out int checkModifier,SharedMiningFixture mining=null)
        {
            mining=mining??new SharedMiningFixture(wisdom:30);
            // Actor-life initialization pins RandomState directly to the supplied seed, so
            // enumerate the deterministic die stream before constructing the full composed world.
            var probe=Recipe347Policy(1,mining);var probeState=probe.Initial();
            int modifier=AbilityCheckRules.Derive(probeState,TestOnlyPolicy.CompanionId,"mining-tools",CharacterAbility.Wisdom).Total+1;
            for(uint seed=1;seed<4096;seed++) {
                if(ManufacturingRules.Quality(PlaytestDice.RollD20(seed).Natural,modifier,20)!=CraftQuality.Standard)continue;
                policy=seed==1?probe:Recipe347Policy(seed,mining);
                initial=seed==1?probeState:policy.Initial();checkModifier=modifier;return;
            }
            throw new Exception("Could not find a deterministic TEST_ONLY seed for the standard recipe-347 quality band.");
        }

        private static MiningDepositFixtureContent SecondRecipe347MiningDeposit()
        {
            const string depositId="TEST_ONLY.mining.deposit.second",version="TEST_ONLY.mining.deposit.second-v1";
            const string site="TEST_ONLY.mining.site.second",category="TEST_ONLY.mining.category.second";
            const string unit="TEST_ONLY.mining.unit.second",tools="TEST_ONLY.mining.tools.second";
            const string pick="TEST_ONLY.mining.pick.second",receiver="TEST_ONLY.mining.receiver.second";
            const string surface="TEST_ONLY.mining.surface.second",fit="TEST_ONLY.mining.receiver-fit.second";
            const int x=4,y=3;
            string owner=TestOnlyPolicy.CompanionId;
            var deposit=new MiningDepositRecord(depositId,version,site,owner,x,y,tools,pick,receiver,surface);
            var categoryRecord=new MiningCategoryRecord(category,depositId,"TEST_ONLY.mineral.second-ore",1,true,
                new[]{unit});
            var unitRecord=new MiningMaterialUnitRecord(unit,depositId,category,new RuleQuantity(1),
                RuleQuantity.FromFraction(1,50),10,MiningUnitCondition.Intact,MiningUnitStatus.Available);
            var raw=new PortableEquipmentRecord(unit,"TEST_ONLY.mining.raw-unit",owner,owner,"",
                PortablePlacement.Ground,PortableLinkKind.InventoryLot,unit,PortableMassBasis.GenericPounds,
                new RuleQuantity(1),null,groundX:x,groundY:y);
            var miningTools=new PortableEquipmentRecord(tools,"TEST_ONLY.mining.screen-and-tray",owner,owner,"",
                PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(3),
                new RuleQuantity(3),groundX:x,groundY:y);
            var miningPick=new PortableEquipmentRecord(pick,"TEST_ONLY.mining-pick",owner,owner,"",
                PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(10),
                new RuleQuantity(10),groundX:x,groundY:y);
            var miningReceiver=new PortableEquipmentRecord(receiver,"TEST_ONLY.mining-receiver",owner,owner,"",
                PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(2),
                new RuleQuantity(2),capacityPounds:new RuleQuantity(50),capacityCubicFeet:new RuleQuantity(1),
                open:true,fitRuleId:fit,fitMemberIds:new[]{unit},groundX:x,groundY:y);
            var workSurface=new ObjectStructureRecord(surface,"TEST_ONLY.stable-mining-work-surface",owner,owner,site,
                ObjectMaterial.Stone,100,100,0,new RuleQuantity(20));
            return new MiningDepositFixtureContent(deposit,new[]{categoryRecord},new[]{unitRecord},
                new[]{raw,miningTools,miningPick,miningReceiver},new[]{workSurface});
        }

        private static SharedMiningFixture TwoDepositRecipe347Mining()
            =>new SharedMiningFixture(new[]{new SharedMiningFixture().Deposits.Single(),SecondRecipe347MiningDeposit()},wisdom:30);

        private static void Recipe347WaitForActivityWindow(Simulation simulation,string actor=TestOnlyPolicy.CompanionId)
        {
            var state=simulation.Capture();var activity=state.WorldActivityIntervals.Single(x=>x.ActorId==actor);
            if(activity.Action==WorldActionCommitment.None)return;
            var end=WorldActivityIntervalRecord.EndAt(state.WorldSchedule,activity.IntervalIndex);
            BigInteger remaining=(BigInteger)end.Numerator*state.RuleClock.Denominator
                -(BigInteger)state.RuleClock.Numerator*end.Denominator;
            if(remaining<=0)return;
            BigInteger denominator=(BigInteger)end.Denominator*state.RuleClock.Denominator;
            int seconds=checked((int)((remaining+denominator-1)/denominator));
            WorldAdvance(simulation,seconds);
        }

        private static Recipe347WorkOrderRecord CompleteRecipe347Order(Simulation simulation)
        {
            if(simulation.Capture().Recipe347WorkOrders.Length==0)
                Recipe347Commit(simulation,Recipe347Start(simulation));
            for(int step=0;step<20;step++) {
                var state=simulation.Capture();var order=state.Recipe347WorkOrders.Single();
                if(order.Status==Recipe347OrderStatus.Complete)return order;
                if(order.Status==Recipe347OrderStatus.Failed||order.Status==Recipe347OrderStatus.Mishap)
                    throw new Exception("Deterministic crafting seed did not produce the required reusable item.");
                if(order.Status==Recipe347OrderStatus.Working) {
                    var interval=state.Work.WorkerIntervals.Single(x=>x.JobId==order.Id
                        &&x.Start<=state.RuleClock&&x.End>state.RuleClock);
                    long now=checked((long)(state.RuleClock.Numerator/state.RuleClock.Denominator));
                    long end=checked((long)(interval.End.Numerator/interval.End.Denominator));
                    WorldAdvance(simulation,checked((int)(end-now)));
                } else if(order.Status==Recipe347OrderStatus.Paused) {
                    long now=checked((long)(state.RuleClock.Numerator/state.RuleClock.Denominator));
                    if(now%86400/28800==2)WorldAdvance(simulation,28800);
                    else Recipe347Commit(simulation,new Command("recipe347.resume."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id));
                } else if(order.Status==Recipe347OrderStatus.AwaitingCheck) {
                    Recipe347Commit(simulation,new Command("recipe347.check."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id));
                } else if(order.Status==Recipe347OrderStatus.AwaitingChoice) {
                    Recipe347Commit(simulation,new Command("recipe347.quality."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResolveRecipe347Quality,order.Id,
                        x:(int)CraftQualityChoice.Durability));
                } else throw new Exception("Unexpected recipe-347 order status: "+order.Status);
            }
            throw new Exception("Recipe-347 order did not finish within five authored work Watches.");
        }

        private static Command Recipe347Start(Simulation simulation,string id="recipe347.start")
        {
            var state=simulation.Capture();
            return new Command(id,TestOnlyPolicy.CompanionId,state.Revision,CommandKind.StartRecipe347,
                TestOnlyRecipe347Fixture.WorkshopId,x:(int)CharacterAbility.Wisdom);
        }

        private static void Recipe347Commit(Simulation simulation,Command command,TestOnlySharedWorldPolicy policy=null)
        {
            var result=simulation.Execute(TestOnlySharedWorldPolicy.Host(),command);
            if(result.Outcome==Outcome.Rejected&&result.Code=="InvalidResult"&&policy!=null) {
                var candidate=simulation.Capture().Copy();
                string policyFailure=policy.Resolve(candidate,command);
                string stateFailure=policyFailure??policy.ValidateState(candidate);
                string snapshotFailure="";
                try { Validation.Snapshot(candidate); }
                catch(Exception ex) { snapshotFailure=ex.GetType().Name+":"+ex.Message; }
                Require(false,command.Kind+" produced an invalid candidate: "+stateFailure
                    +"; core snapshot="+snapshotFailure);
            }
            Require(result.Outcome==Outcome.Committed,command.Kind+" rejected: "+result.Code);
        }

        private static void AddRecipe347Cases(System.Collections.Generic.Dictionary<string,Action> cases,string directory)
        {
            cases.Add("recipe347_completed_output_is_the_same_physically_usable_mining_tool",()=>{
                Recipe347StandardPolicy(out var policy,out var initial,out int craftModifier);
                var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                var order=CompleteRecipe347Order(simulation);var crafted=simulation.Capture();
                var output=crafted.Recipe347Outputs.Single(x=>x.Id==order.OutputProvenanceId);
                var tool=crafted.Recipe347MiningToolProfiles.Single(x=>x.ItemId==output.ItemId);
                Require(order.Status==Recipe347OrderStatus.Complete&&order.Quality==CraftQuality.Standard
                    &&order.CheckModifier==craftModifier&&output.ItemId==TestOnlyRecipe347Fixture.BodyItemId
                    &&tool.ProvenanceId==output.Id&&crafted.PortableEquipment.Single(x=>x.Id==tool.ItemId).Placement==PortablePlacement.Ground,
                    "Successful source-bound work must transform the reserved body and publish its physical reusable-tool profile.");
                byte[] preMining=new SnapshotCodec().Encode(crafted);
                var resumed=new Simulation(policy,new SnapshotCodec().Decode(preMining),ExecutionProfile.Laboratory);
                Require(preMining.SequenceEqual(Bytes(resumed)),"Completed recipe output changed across its schema72 save/restore.");
                int baseMiningModifier=MiningModifier(crafted);
                var selection=new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,
                    new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom);
                var start=MiningCommand(resumed,CommandKind.StartMining,SharedMiningFixture.DepositId,selection,
                    commandId:"recipe347.mine.first.start");
                MiningCommit(resumed,start);
                var deployed=resumed.Capture();var attempt=deployed.MiningAttempts.Single();
                var evidence=deployed.Recipe347MiningToolUseEvidence.Single(x=>x.AttemptId==attempt.Id);
                Require(evidence.ItemId==tool.ItemId&&evidence.DepositId==SharedMiningFixture.DepositId
                    &&deployed.Recipe347MiningToolWorkSegments.Length==0,
                    "Mining must bind the same output item and selected deposit before any extraction work is credited.");
                WorldAdvance(resumed,attempt.DurationSeconds);
                var mined=resumed.Capture();attempt=mined.MiningAttempts.Single();
                Require(attempt.CheckModifier==baseMiningModifier+2
                    &&mined.Recipe347MiningToolWorkSegments.Any(x=>x.AttemptId==attempt.Id),
                    "At least sixty physically deployed removal seconds must supply exactly the recipe tool's +2 Mining bonus.");
                byte[] savedMining=Bytes(resumed);var restored=new Simulation(policy,new SnapshotCodec().Decode(savedMining),ExecutionProfile.Laboratory);
                Require(savedMining.SequenceEqual(Bytes(restored)),"Completed mining evidence or tool work changed across schema72 restore.");
                Require(restored.Execute(TestOnlySharedWorldPolicy.Host(),start).Outcome==Outcome.Duplicate
                    &&savedMining.SequenceEqual(Bytes(restored)),"Replaying the recorded Mining start repeated extraction or tool effects.");
            });
            cases.Add("recipe347_same_tool_works_at_two_deposits_and_only_when_physically_deployed",()=>{
                Recipe347StandardPolicy(out var policy,out var initial,out _,TwoDepositRecipe347Mining());
                var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                var order=CompleteRecipe347Order(simulation);var crafted=simulation.Capture();
                var tool=crafted.Recipe347MiningToolProfiles.Single(x=>x.ItemId==order.BodyItemId);
                byte[] craftedSave=Bytes(simulation);
                var absent=new Simulation(policy,new SnapshotCodec().Decode(craftedSave),ExecutionProfile.Laboratory);
                Recipe347WaitForActivityWindow(absent);
                PortableCommit(absent,Portable(absent,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.CompanionId));
                WorldStep(absent,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(absent,1);
                Recipe347WaitForActivityWindow(absent);
                PortableCommit(absent,Portable(absent,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId));
                var absentState=absent.Capture();
                Require(absentState.PortableEquipment.Single(x=>x.Id==tool.ItemId).GroundX==2
                    &&absentState.PortableEquipment.Single(x=>x.Id==tool.ItemId).GroundY==3,
                    "The no-tool branch must move the actual output body away from the first deposit through ordinary handling.");
                int baseModifier=MiningModifier(absentState);
                var firstSelection=new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,
                    new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom);
                Recipe347WaitForActivityWindow(absent);
                MiningCommit(absent,MiningCommand(absent,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    firstSelection,commandId:"recipe347.mine.first.absent"));
                WorldAdvance(absent,absent.Capture().MiningAttempts.Single().DurationSeconds);
                Require(absent.Capture().MiningAttempts.Single().CheckModifier==baseModifier
                    &&absent.Capture().Recipe347MiningToolUseEvidence.Length==0,
                    "The same profile must supply no check bonus when its physical item is elsewhere.");

                var deployed=new Simulation(policy,new SnapshotCodec().Decode(craftedSave),ExecutionProfile.Laboratory);
                baseModifier=MiningModifier(deployed.Capture());
                MiningCommit(deployed,MiningCommand(deployed,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    firstSelection,commandId:"recipe347.mine.first.deployed"));
                WorldAdvance(deployed,deployed.Capture().MiningAttempts.Single().DurationSeconds);
                var firstAttempt=deployed.Capture().MiningAttempts.Single();
                Require(firstAttempt.CheckModifier==baseModifier+2
                    &&deployed.Capture().Recipe347MiningToolUseEvidence.Single().ItemId==tool.ItemId,
                    "The crafted item must receive its +2 check bonus at the first deposit.");
                Recipe347WaitForActivityWindow(deployed);
                PortableCommit(deployed,Portable(deployed,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.CompanionId));
                WorldStep(deployed,1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(deployed,1);
                Recipe347WaitForActivityWindow(deployed);
                PortableCommit(deployed,Portable(deployed,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId));
                var secondDeposit=deployed.Capture().MiningDeposits.Single(x=>x.Id=="TEST_ONLY.mining.deposit.second");
                var relocated=deployed.Capture().PortableEquipment.Single(x=>x.Id==tool.ItemId);
                Require(relocated.Placement==PortablePlacement.Ground&&relocated.GroundX==secondDeposit.SiteX
                    &&relocated.GroundY==secondDeposit.SiteY,
                    "The same output item must move between deposit sites through physical pickup, traversal and drop.");
                int secondBase=MiningModifier(deployed.Capture());
                var secondSelection=new MiningSelectionRequest(secondDeposit.VersionId,
                    new[]{"TEST_ONLY.mining.category.second"},MiningAbilityChoice.Wisdom);
                Recipe347WaitForActivityWindow(deployed);
                MiningCommit(deployed,MiningCommand(deployed,CommandKind.StartMining,secondDeposit.Id,secondSelection,
                    commandId:"recipe347.mine.second.deployed"));
                var secondAttempt=deployed.Capture().MiningAttempts.Single(x=>x.DepositId==secondDeposit.Id);
                byte[] partial=Bytes(deployed);var left=new Simulation(policy,new SnapshotCodec().Decode(partial),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(partial),ExecutionProfile.Laboratory);
                WorldAdvance(left,secondAttempt.DurationSeconds);WorldAdvance(right,secondAttempt.DurationSeconds);
                var final=left.Capture();secondAttempt=final.MiningAttempts.Single(x=>x.DepositId==secondDeposit.Id);
                Require(secondAttempt.CheckModifier==secondBase+2
                    &&final.Recipe347MiningToolUseEvidence.Count(x=>x.ItemId==tool.ItemId)==2
                    &&Bytes(left).SequenceEqual(Bytes(right)),
                    "The unchanged physical tool must earn +2 at a distinct deposit, with save/restore replay producing identical state.");
            });
            cases.Add("recipe347_work_order_shares_mining_inventory_and_roundtrips",()=>{
                var policy=Recipe347Policy(17);var simulation=World(policy);var initial=simulation.Capture();
                Require(initial.SchemaVersion==Snapshot.Recipe347Schema&&initial.MiningDeposits.Length==1
                    &&initial.PortableStorageProfiles.Length>0&&initial.Recipe347FormulaAccess.Length==1,
                    "The composed world did not select the expected schema72 Mining, storage and recipe profile.");
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
                var working=simulation.Capture();var order=working.Recipe347WorkOrders.Single();
                Require(order.Status==Recipe347OrderStatus.Working&&working.Work.WorkerIntervals.Any(x=>x.JobId==order.Id)
                    &&working.Work.Reservations.Count(x=>x.JobId==order.Id)==6
                    &&working.Work.Reservations.Where(x=>x.JobId==order.Id).Sum(x=>x.Amount.Numerator)==14,
                    "Recipe-347 must reserve five exact component lots and the same three-pound body through shared WorkLedger.");
                var codec=new SnapshotCodec();byte[] partial=codec.Encode(working);
                var left=new Simulation(policy,codec.Decode(partial),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,codec.Decode(partial),ExecutionProfile.Laboratory);
                WorldAdvance(left,900);WorldAdvance(right,900);
                Require(left.Capture().Recipe347WorkOrders.Single().Work.CompletedPhases==1
                    &&Bytes(left).SequenceEqual(Bytes(right)),
                    "The first source phase and identical restored continuations must remain deterministic.");
                byte[] phase=Bytes(left);var restored=new Simulation(policy,codec.Decode(phase),ExecutionProfile.Laboratory);
                WorldAdvance(left,27900);WorldAdvance(restored,27900);
                Require(left.Capture().RuleClock==new RuleTime(28800)
                    &&left.Capture().Recipe347WorkOrders.Single().Status==Recipe347OrderStatus.Paused
                    &&Bytes(left).SequenceEqual(Bytes(restored)),
                    "The first full Watch must stop at its canonical boundary and roundtrip byte-identically.");
            });
        }
    }
}
#endif
