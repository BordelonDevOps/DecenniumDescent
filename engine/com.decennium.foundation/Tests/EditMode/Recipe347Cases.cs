#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.IO;
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


        private static TestOnlySharedWorldPolicy Recipe347RestDebtPolicy(uint seed=1)
        {
            var policy=Recipe347Policy(seed);
            policy.EnableDailyProvisioning().EnableRestDebt();
            return policy;
        }

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

        private static void Recipe347PortableCommit(Simulation simulation,Command command)
        {
            Recipe347WaitForActivityWindow(simulation,command.Actor);
            if(command.ExpectedRevision!=simulation.Capture().Revision)
                command=new Command(command.Id,command.Actor,simulation.Capture().Revision,command.Kind,command.Target,
                    inventory:command.Inventory==null?null:new InventoryRequest(command.Inventory.Amount,
                        command.Inventory.Destination,command.Inventory.Handling));
            PortableCommit(simulation,command);
        }

        private static void Recipe347MoveCompanionTo(Simulation simulation,int x,int y)
        {
            for(int step=0;step<128;step++) {
                var actor=simulation.Capture().Actors.Single(a=>a.Id==TestOnlyPolicy.CompanionId);
                if(actor.X==x&&actor.Y==y)return;
                int dx=actor.X==x?0:Math.Sign(x-actor.X);
                int dy=dx==0&&actor.Y!=y?Math.Sign(y-actor.Y):0;
                try { WorldStep(simulation,dx,dy,actor:TestOnlyPolicy.CompanionId); }
                catch(Exception ex) {
                    var state=simulation.Capture();
                    throw new Exception("Companion movement to "+x.ToString()+","+y.ToString()+" failed from "+actor.X.ToString()
                        +","+actor.Y.ToString()+" via "+(actor.X+dx).ToString()+","+(actor.Y+dy).ToString()+"; actors="
                        +string.Join(";",state.Actors.Select(a=>a.Id+"@"+a.X.ToString()+","+a.Y.ToString())),ex);
                }
                WorldAdvance(simulation,5);
            }
            throw new Exception("Recipe-347 worker did not reach the requested physical location.");
        }

        private static void Recipe347MovePrimaryActorTo(Simulation simulation,int x,int y)
        {
            for(int step=0;step<128;step++) {
                var actor=simulation.Capture().Actors.Single(a=>a.Id==TestOnlyPolicy.ActorId);
                if(actor.X==x&&actor.Y==y)return;
                int dx=actor.X==x?0:Math.Sign(x-actor.X);
                int dy=dx==0&&actor.Y!=y?Math.Sign(y-actor.Y):0;
                WorldStep(simulation,dx,dy,actor:TestOnlyPolicy.ActorId);
                WorldAdvance(simulation,5);
            }
            throw new Exception("Recipe-347 second worker did not reach the requested physical location.");
        }

        private static void PrepareRecipe347Workshop(Simulation simulation)
        {
            var initial=simulation.Capture();
            var crate=initial.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
            var workshop=initial.Recipe347Workshops.Single(x=>x.Id==TestOnlyRecipe347Fixture.WorkshopId);
            var workshopDeposit=initial.MiningDeposits.Single(x=>x.SiteId==workshop.SiteId);
            string worker=TestOnlyPolicy.CompanionId;
            if(crate.Placement==PortablePlacement.Ground&&(crate.GroundX!=workshop.SiteX||crate.GroundY!=workshop.SiteY)) {
                var workerLocation=initial.Actors.Single(x=>x.Id==worker);
                if(Math.Abs((long)workerLocation.X-crate.GroundX)+Math.Abs((long)workerLocation.Y-crate.GroundY)>1) {
                    int[][] approaches={new[]{crate.GroundX-1,crate.GroundY},new[]{crate.GroundX+1,crate.GroundY},
                        new[]{crate.GroundX,crate.GroundY-1},new[]{crate.GroundX,crate.GroundY+1}};
                    var approach=approaches.Where(x=>TestOnlyPolicy.Walkable(x[0],x[1])
                            &&!WorldSpatialQueries.Occupied(initial,worker,x[0],x[1]))
                        .OrderBy(x=>Math.Abs((long)workerLocation.X-x[0])+Math.Abs((long)workerLocation.Y-x[1]))
                        .FirstOrDefault();
                    if(approach==null)throw new Exception("No physically accessible cardinal handling position exists beside the recipe storage crate.");
                    Recipe347MoveCompanionTo(simulation,approach[0],approach[1]);
                }
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,crate.Id,
                    handling:HandlingKind.Pickup,actor:worker));
                Recipe347MoveCompanionTo(simulation,workshop.SiteX,workshop.SiteY);
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,crate.Id,
                    handling:HandlingKind.Drop,actor:worker));
            }
            foreach(string id in new[]{TestOnlyRecipe347Fixture.BodyItemId,TestOnlyRecipe347Fixture.MiningToolsItemId,
                TestOnlyRecipe347Fixture.AssayKitId,workshopDeposit.PickId}) {
                var item=simulation.Capture().PortableEquipment.Single(x=>x.Id==id);
                if(item.Placement==PortablePlacement.Ground&&item.GroundX==workshop.SiteX&&item.GroundY==workshop.SiteY)continue;
                if(item.ParentId=="")throw new Exception("Recipe-347 required implement is not stored in the physical workshop crate: "+id);
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,id,
                    handling:HandlingKind.Retrieve,actor:worker));
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,id,
                    handling:HandlingKind.Drop,actor:worker));
            }
            var ready=simulation.Capture();
            if(ready.Actors.Single(x=>x.Id==worker).X!=workshop.SiteX||ready.Actors.Single(x=>x.Id==worker).Y!=workshop.SiteY
                ||ready.PortableEquipment.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyItemId).Placement!=PortablePlacement.Ground
                ||ready.PortableEquipment.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyItemId).GroundX!=workshop.SiteX
                ||ready.PortableEquipment.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyItemId).GroundY!=workshop.SiteY)
                throw new Exception("Physical recipe stock and required implements were not staged at the mining worksite.");
        }

        private static void PrepareRecipe347WorkshopBesideCampStorage(Simulation simulation)
        {
            var initial=simulation.Capture();var workshop=initial.Recipe347Workshops.Single();
            var workshopDeposit=initial.MiningDeposits.Single(x=>x.SiteId==workshop.SiteId);
            string worker=TestOnlyPolicy.CompanionId;
            Recipe347MoveCompanionTo(simulation,workshop.SiteX,workshop.SiteY);
            foreach(string id in new[]{TestOnlyRecipe347Fixture.BodyItemId,TestOnlyRecipe347Fixture.MiningToolsItemId,
                TestOnlyRecipe347Fixture.AssayKitId,workshopDeposit.PickId}) {
                var item=simulation.Capture().PortableEquipment.Single(x=>x.Id==id);
                if(item.Placement==PortablePlacement.Ground&&item.GroundX==workshop.SiteX&&item.GroundY==workshop.SiteY)continue;
                if(item.ParentId!=""&&item.ParentId!=TestOnlyPortableStorageFixture.CrateId)
                    throw new Exception("Recipe-347 camp stock is not in the authored physical crate: "+id);
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,id,
                    handling:HandlingKind.Retrieve,actor:worker));
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,id,
                    handling:HandlingKind.Drop,actor:worker));
            }
            var staged=simulation.Capture();var crate=staged.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
            if(crate.Placement!=PortablePlacement.Ground||Math.Abs((long)crate.GroundX-workshop.SiteX)
                +Math.Abs((long)crate.GroundY-workshop.SiteY)>1)
                throw new Exception("The open source crate must remain physically accessible beside the workshop.");
        }

        private static void Recipe347WaitForNextWorkWatch(Simulation simulation)
        {
            var state=simulation.Capture();var now=state.RuleClock;
            BigInteger wholeSeconds=(BigInteger)now.Numerator/now.Denominator;
            long slotOrdinal=checked((long)(wholeSeconds/28800)+1);
            long target=0;
            for(int offset=0;offset<12;offset++,slotOrdinal++) {
                long day=slotOrdinal/3;var slot=(RestWatchSlot)(slotOrdinal%3);
                var scheduled=state.RestWatchSchedules.Where(x=>x.ActorId==TestOnlyPolicy.CompanionId&&x.DayOrdinal==day)
                    .OrderBy(x=>x.Revision).LastOrDefault();
                RestWatchSlot rest=scheduled?.Slot??RestWatchSlot.Evening;
                if(slot==rest)continue;
                target=checked(slotOrdinal*28800);break;
            }
            if(target==0)throw new InvalidOperationException("Recipe-347 fixture could not find a future non-rest work Watch.");
            BigInteger delta=(BigInteger)target*now.Denominator-now.Numerator;
            if(delta<=0||delta>int.MaxValue||now.Denominator>int.MaxValue)
                throw new InvalidOperationException("Recipe-347 fixture Watch boundary is not a positive representable clock interval.");
            WorldAdvance(simulation,checked((int)delta),checked((int)now.Denominator));
            Require(simulation.Capture().RuleClock==new RuleTime(target),"Recipe-347 fixture did not reach its exact work-Watch start.");
        }

        private static void Recipe347AdvanceTo(Simulation simulation,long targetSeconds)
        {
            var now=simulation.Capture().RuleClock;
            BigInteger delta=(BigInteger)targetSeconds*now.Denominator-now.Numerator;
            if(delta<0||delta%now.Denominator!=0)throw new InvalidOperationException("Recipe-347 test clock target is not a future whole second.");
            if(delta>0)WorldAdvance(simulation,checked((int)(delta/now.Denominator)));
            Require(simulation.Capture().RuleClock==new RuleTime(targetSeconds),"Recipe-347 test clock did not reach the requested Watch boundary.");
        }

        private static void Recipe347PolicyForQuality(CraftQuality target,int requiredMishapResult,
            out TestOnlySharedWorldPolicy policy,out Snapshot initial,out int modifier,out int natural)
        {
            for(int wisdom=1;wisdom<=30;wisdom++) {
                var mining=new SharedMiningFixture(wisdom:wisdom);
                var probe=Recipe347Policy(1,mining);var probeState=probe.Initial();
                int candidateModifier=checked(AbilityCheckRules.Derive(probeState,TestOnlyPolicy.CompanionId,
                    "mining-tools",CharacterAbility.Wisdom).Total
                    +CharacterStateFacts.ForActor(probeState,TestOnlyPolicy.CompanionId,"mining-tools")
                        .InjuryPenalty(CharacterAbility.Wisdom,toolCheck:true)+1);
                for(uint seed=1;seed<100000;seed++) {
                    var roll=PlaytestDice.RollD20(seed);
                    if(ManufacturingRules.Quality(roll.Natural,candidateModifier,20)!=target)continue;
                    if(target==CraftQuality.Mishap&&requiredMishapResult!=0
                        &&DiceStream.Draw(roll.NextRandomState,6).Value+1!=requiredMishapResult)continue;
                    policy=seed==1?probe:Recipe347Policy(seed,mining);initial=seed==1?probeState:policy.Initial();
                    if(initial.RandomState!=seed)throw new Exception("Recipe-347 test fixture did not preserve its selected deterministic RNG seed.");
                    modifier=candidateModifier;natural=roll.Natural;return;
                }
            }
            throw new Exception("Could not find a deterministic recipe-347 seed for quality "+target.ToString()+".");
        }

        private static Recipe347WorkOrderRecord CompleteRecipe347Order(Simulation simulation,TestOnlySharedWorldPolicy policy=null,
            bool allowNonComplete=false)
        {
            if(simulation.Capture().Recipe347WorkOrders.Length==0) {
                PrepareRecipe347Workshop(simulation);
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
            }
            for(int step=0;step<20;step++) {
                var state=simulation.Capture();var order=state.Recipe347WorkOrders.Single();
                if(order.Status==Recipe347OrderStatus.Complete)return order;
                if(order.Status==Recipe347OrderStatus.Failed||order.Status==Recipe347OrderStatus.Mishap)
                    if(allowNonComplete)return order;
                    else
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
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id),policy);
                } else if(order.Status==Recipe347OrderStatus.AwaitingCheck) {
                    Recipe347Commit(simulation,new Command("recipe347.check."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id),policy);
                } else if(order.Status==Recipe347OrderStatus.AwaitingChoice) {
                    Recipe347Commit(simulation,new Command("recipe347.quality."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResolveRecipe347Quality,order.Id,
                        x:(int)CraftQualityChoice.Durability),policy);
                } else throw new Exception("Unexpected recipe-347 order status: "+order.Status);
            }
            throw new Exception("Recipe-347 order did not finish within five authored work Watches.");
        }

        private static Recipe347WorkOrderRecord Recipe347ReachQualityChoice(Simulation simulation,
            TestOnlySharedWorldPolicy policy,int secondsPastCompletion=0)
        {
            if(simulation.Capture().Recipe347WorkOrders.Length==0) {
                PrepareRecipe347Workshop(simulation);
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
            }
            for(int step=0;step<20;step++) {
                var state=simulation.Capture();var order=state.Recipe347WorkOrders.Single();
                if(order.Status==Recipe347OrderStatus.AwaitingChoice)return order;
                if(order.Status==Recipe347OrderStatus.Complete||order.Status==Recipe347OrderStatus.Failed
                    ||order.Status==Recipe347OrderStatus.Mishap)
                    throw new Exception("Recipe-347 selected seed did not reach a pending quality choice.");
                if(order.Status==Recipe347OrderStatus.Working) {
                    var interval=state.Work.WorkerIntervals.Single(x=>x.JobId==order.Id
                        &&x.Start<=state.RuleClock&&x.End>state.RuleClock);
                    long now=checked((long)(state.RuleClock.Numerator/state.RuleClock.Denominator));
                    long end=checked((long)(interval.End.Numerator/interval.End.Denominator));
                    int seconds=checked((int)(end-now));
                    if(secondsPastCompletion>0&&order.Work.CompletedPhases==order.Work.Phases.Count-1)
                        seconds=checked(seconds+secondsPastCompletion);
                    WorldAdvance(simulation,seconds);
                } else if(order.Status==Recipe347OrderStatus.Paused) {
                    long now=checked((long)(state.RuleClock.Numerator/state.RuleClock.Denominator));
                    if(now%86400/28800==2)WorldAdvance(simulation,28800);
                    else Recipe347Commit(simulation,new Command("recipe347.resume."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id),policy);
                } else if(order.Status==Recipe347OrderStatus.AwaitingCheck) {
                    Recipe347Commit(simulation,new Command("recipe347.check."+state.Revision,
                        TestOnlyPolicy.CompanionId,state.Revision,CommandKind.ResumeRecipe347,order.Id),policy);
                } else throw new Exception("Unexpected recipe-347 order status: "+order.Status);
            }
            throw new Exception("Recipe-347 quality choice did not become available.");
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
            cases.Add("recipe347_work_watch_applies_shared_default_and_alternate_rest_to_mining_start_and_resume",()=>{
                var policy=Recipe347RestDebtPolicy(41);var defaultSchedule=World(policy);PrepareRecipe347Workshop(defaultSchedule);
                var setupClock=defaultSchedule.Capture().RuleClock;
                if(setupClock.Denominator==1&&setupClock.Numerator%28800==0)WorldAdvance(defaultSchedule,1);
                var midWatchStart=Recipe347Start(defaultSchedule,"recipe347.watch.midwatch.query");
                byte[] beforeMidWatch=Bytes(defaultSchedule);var midWatchQuery=defaultSchedule.QueryCommand(
                    TestOnlySharedWorldPolicy.Host(),midWatchStart);
                var midWatchResult=defaultSchedule.Execute(TestOnlySharedWorldPolicy.Host(),midWatchStart);
                Require(midWatchQuery.Supported&&!midWatchQuery.Admissible
                    &&midWatchQuery.Code=="Recipe347WorkMustStartAtWatchBoundary"
                    &&midWatchResult.Outcome==Outcome.Rejected&&midWatchResult.Code==midWatchQuery.Code
                    &&Bytes(defaultSchedule).SequenceEqual(beforeMidWatch),
                    "Recipe query and commit must both reject a mid-Watch start without changing state.");
                byte[] preparedDefault=Bytes(defaultSchedule);
                var defaultRest=new Simulation(policy,new SnapshotCodec().Decode(preparedDefault),ExecutionProfile.Laboratory);
                Recipe347AdvanceTo(defaultRest,16*3600);
                var defaultStart=MiningCommand(defaultRest,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                    commandId:"recipe347.rest.default.start");
                byte[] beforeDefault=Bytes(defaultRest);var defaultQuery=defaultRest.QueryCommand(TestOnlySharedWorldPolicy.Host(),defaultStart);
                Require(defaultQuery.Supported&&!defaultQuery.Admissible&&defaultQuery.Code=="Recipe347ScheduledRestWatch"
                    &&defaultQuery.Costs.Count==0&&Bytes(defaultRest).SequenceEqual(beforeDefault),
                    "Mining start must query the effective default Evening Rest Watch without mutation.");
                var defaultRejected=defaultRest.Execute(TestOnlySharedWorldPolicy.Host(),defaultStart);
                Require(defaultRejected.Outcome==Outcome.Rejected&&defaultRejected.Code==defaultQuery.Code
                    &&Bytes(defaultRest).SequenceEqual(beforeDefault),
                    "Mining start query and commit disagree at the default Rest Watch or rejection changed state.");

                var alternatePolicy=Recipe347RestDebtPolicy(43);var alternate=World(alternatePolicy);
                var schedule=new Command("recipe347.rest.alternate.schedule",TestOnlyPolicy.CompanionId,
                    alternate.Capture().Revision,CommandKind.ScheduleRestWatch,"day.0",(int)RestWatchSlot.Morning);
                var scheduleQuery=alternate.QueryCommand(TestOnlySharedWorldPolicy.Host(),schedule);
                Require(scheduleQuery.Supported&&scheduleQuery.Admissible&&scheduleQuery.Costs.Count==0,
                    "The existing RestWatch command must prospectively schedule the alternate source slot.");
                var scheduleResult=alternate.Execute(TestOnlySharedWorldPolicy.Host(),schedule);
                Require(scheduleResult.Outcome==Outcome.Committed,"The source RestWatch schedule command was not committed.");
                PrepareRecipe347Workshop(alternate);byte[] preparedAlternate=Bytes(alternate);
                var morning=new Simulation(alternatePolicy,new SnapshotCodec().Decode(preparedAlternate),ExecutionProfile.Laboratory);
                var morningStart=MiningCommand(morning,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                    commandId:"recipe347.rest.morning.start");
                byte[] beforeMorning=Bytes(morning);var morningQuery=morning.QueryCommand(TestOnlySharedWorldPolicy.Host(),morningStart);
                var morningResult=morning.Execute(TestOnlySharedWorldPolicy.Host(),morningStart);
                Require(morningQuery.Supported&&!morningQuery.Admissible&&morningQuery.Code=="Recipe347ScheduledRestWatch"
                    &&morningResult.Outcome==Outcome.Rejected&&morningResult.Code==morningQuery.Code
                    &&Bytes(morning).SequenceEqual(beforeMorning),
                    "The prospectively selected Morning Rest Watch must reject Mining start with query/commit parity.");

                foreach(long watchStart in new[]{8L*3600,16L*3600}) {
                    var active=new Simulation(alternatePolicy,new SnapshotCodec().Decode(preparedAlternate),ExecutionProfile.Laboratory);
                    Recipe347AdvanceTo(active,watchStart);
                    var start=MiningCommand(active,CommandKind.StartMining,SharedMiningFixture.DepositId,
                        new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                        commandId:"recipe347.rest.active."+watchStart.ToString(System.Globalization.CultureInfo.InvariantCulture));
                    var query=active.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                    Require(query.Supported&&query.Admissible,"The non-rest Watch at "+watchStart.ToString()+" seconds was not admitted.");
                    MiningCommit(active,start);
                    Require(active.Capture().MiningAttempts.Any(x=>x.WorkerId==TestOnlyPolicy.CompanionId
                        &&x.StartedAt==new RuleTime(watchStart)),"An admitted non-rest Watch did not book Mining through the shared attempt and WorkLedger.");
                }

                var resume=new Simulation(policy,new SnapshotCodec().Decode(preparedDefault),ExecutionProfile.Laboratory);
                Recipe347AdvanceTo(resume,8*3600);
                var resumeStart=MiningCommand(resume,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                    commandId:"recipe347.rest.resume.source.start");MiningCommit(resume,resumeStart);
                WorldAdvance(resume,1);var attempt=resume.Capture().MiningAttempts.Single();
                MiningCommit(resume,MiningCommand(resume,CommandKind.PauseMining,attempt.Id));
                Recipe347AdvanceTo(resume,16*3600);
                var resumeCommand=MiningCommand(resume,CommandKind.ResumeMining,attempt.Id,commandId:"recipe347.rest.resume.rejected");
                byte[] beforeResume=Bytes(resume);var resumeQuery=resume.QueryCommand(TestOnlySharedWorldPolicy.Host(),resumeCommand);
                var resumeResult=resume.Execute(TestOnlySharedWorldPolicy.Host(),resumeCommand);
                Require(resumeQuery.Supported&&!resumeQuery.Admissible&&resumeQuery.Code=="Recipe347ScheduledRestWatch"
                    &&resumeResult.Outcome==Outcome.Rejected&&resumeResult.Code==resumeQuery.Code
                    &&Bytes(resume).SequenceEqual(beforeResume),
                    "Mining resume must use the same default Rest Watch admission and preserve query/commit parity.");
            });
            cases.Add("recipe347_work_watch_counts_mining_and_crafting_in_either_booking_order",()=>{
                var policy=Recipe347Policy(47);var prepared=World(policy);PrepareRecipe347Workshop(prepared);
                Recipe347AdvanceTo(prepared,24*3600);byte[] ready=Bytes(prepared);
                foreach(bool recipeFirst in new[]{true,false}) {
                    var simulation=new Simulation(policy,new SnapshotCodec().Decode(ready),ExecutionProfile.Laboratory);
                    if(recipeFirst) {
                        var start=Recipe347Start(simulation,"recipe347.watch.order.recipe-first");
                        var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                        Require(query.Supported&&query.Admissible,"Recipe-first Watch booking failed admission at its exact boundary.");
                        Recipe347Commit(simulation,start,policy);WorldAdvance(simulation,1);
                        var order=simulation.Capture().Recipe347WorkOrders.Single();
                        Recipe347Commit(simulation,new Command("recipe347.watch.order.pause-recipe",TestOnlyPolicy.CompanionId,
                            simulation.Capture().Revision,CommandKind.PauseRecipe347,order.Id),policy);
                    } else {
                        var start=MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                            new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                            commandId:"recipe347.watch.order.mining-first");
                        var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                        Require(query.Supported&&query.Admissible,"Mining-first Watch booking failed admission at its exact boundary.");
                        MiningCommit(simulation,start);WorldAdvance(simulation,1);
                        var attempt=simulation.Capture().MiningAttempts.Single();
                        MiningCommit(simulation,MiningCommand(simulation,CommandKind.PauseMining,attempt.Id,
                            commandId:"recipe347.watch.order.pause-mining"));
                    }
                    Recipe347AdvanceTo(simulation,32*3600);
                    if(recipeFirst) {
                        var start=MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                            new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom),
                            commandId:"recipe347.watch.order.mining-second");
                        var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                        Require(query.Supported&&query.Admissible,"Mining was not admitted after a recipe-first booking in the prior Watch.");
                        MiningCommit(simulation,start);
                    } else {
                        var start=Recipe347Start(simulation,"recipe347.watch.order.recipe-second");
                        var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                        Require(query.Supported&&query.Admissible,"Recipe was not admitted after a mining-first booking in the prior Watch.");
                        Recipe347Commit(simulation,start,policy);
                    }
                    var state=simulation.Capture();
                    Require(state.Recipe347WorkOrders.Length==1&&state.MiningAttempts.Length==1
                        &&state.Work.WorkerIntervals.Any(x=>x.WorkerId==TestOnlyPolicy.CompanionId
                            &&x.Start>=new RuleTime(24*3600)&&x.Start<new RuleTime(32*3600))
                        &&state.Work.WorkerIntervals.Any(x=>x.WorkerId==TestOnlyPolicy.CompanionId&&x.Start==new RuleTime(32*3600)),
                        "The two source-qualified jobs did not book distinct Morning/Afternoon Watches in the tested order.");
                }
            });
            cases.Add("recipe347_source_access_gates_and_workshop_claim_have_query_commit_parity",()=>{
                var policy=Recipe347Policy(29);var simulation=World(policy);PrepareRecipe347Workshop(simulation);
                Recipe347WaitForNextWorkWatch(simulation);var state=simulation.Capture();var command=Recipe347Start(simulation,
                    "recipe347.gates.access");
                void RejectGate(string name,Action<Snapshot> remove,string expected)
                {
                    var candidate=state.Copy();remove(candidate);long revision=candidate.Revision;RuleTime clock=candidate.RuleClock;
                    uint random=candidate.RandomState;var work=candidate.Work;var orders=candidate.Recipe347WorkOrders;
                    var receipts=candidate.Receipts;
                    string actual=policy.Resolve(candidate,command);
                    Require(actual==expected&&candidate.Revision==revision&&candidate.RuleClock==clock
                        &&candidate.RandomState==random&&ReferenceEquals(candidate.Work,work)
                        &&ReferenceEquals(candidate.Recipe347WorkOrders,orders)&&ReferenceEquals(candidate.Receipts,receipts),
                        name+" gate returned "+(actual??"success")+" rather than "+expected+" or mutated its query candidate.");
                }
                RejectGate("workshop",candidate=>candidate.Recipe347Workshops=Array.Empty<TestOnlyRecipe347WorkshopRecord>(),
                    "Recipe347WorkshopUnavailable");
                RejectGate("formula",candidate=>candidate.Recipe347FormulaAccess=Array.Empty<TestOnlyRecipe347FormulaAccessRecord>(),
                    "Recipe347FormulaUnavailable");
                RejectGate("trade level",candidate=>candidate.Trades=new[]{new TradeProgressRecord(TestOnlyPolicy.CompanionId,"Mining",9,0)},
                    "Recipe347MiningSpecialtyRequired");
                RejectGate("matching specialty",candidate=>candidate.Recipe347TradeSpecialties=Array.Empty<TestOnlyTradeSpecialtyRecord>(),
                    "Recipe347MiningSpecialtyRequired");
                RejectGate("Miner's-tools training",candidate=>candidate.SkillTraining=Array.Empty<SkillTrainingRecord>(),
                    "Recipe347MiningToolsTrainingRequired");
                RejectGate("required implements",candidate=>{
                    var workshop=candidate.Recipe347Workshops.Single();var itemId=workshop.ImplementIds[0];
                    candidate.PortableEquipment=candidate.PortableEquipment.Select(x=>x.Id==itemId
                        ?x.With(groundX:workshop.SiteX+1):x).ToArray();
                },"Recipe347RequiredImplementsUnavailable");
                var startQuery=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),command);
                Require(startQuery.Supported&&startQuery.Admissible&&startQuery.Code=="Available",
                    "A fully sourced recipe at an authorized Watch start was not query-admissible.");
                Recipe347Commit(simulation,command,policy);var order=simulation.Capture().Recipe347WorkOrders.Single();
                Recipe347Commit(simulation,new Command("recipe347.gates.pause",TestOnlyPolicy.CompanionId,
                    simulation.Capture().Revision,CommandKind.PauseRecipe347,order.Id),policy);
                byte[] claimed=Bytes(simulation);
                var conflict=Recipe347Start(simulation,"recipe347.gates.claim-conflict");
                var conflictQuery=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),conflict);
                var conflictResult=simulation.Execute(TestOnlySharedWorldPolicy.Host(),conflict);
                Require(conflictQuery.Supported&&!conflictQuery.Admissible&&conflictQuery.Code=="Recipe347WorkshopClaimed"
                    &&conflictResult.Outcome==Outcome.Rejected&&conflictResult.Code==conflictQuery.Code&&Bytes(simulation).SequenceEqual(claimed),
                    "A second order did not receive the same workshop-claim rejection from query and commit without mutation. query="
                    +conflictQuery.Code+" result="+conflictResult.Outcome.ToString()+"/"+conflictResult.Code
                    +" unchanged="+Bytes(simulation).SequenceEqual(claimed).ToString());
            });
            cases.Add("recipe347_crafting_and_camp_construction_run_for_distinct_workers",()=>{
                var assistants=Array.Empty<string>();var mining=new SharedMiningFixture();
                var policy=CampConstructionPolicy(61,assistants:assistants,storage:true,mining:mining,
                    crafting:new SharedCraftingFixture(toolHp:0),recipe347:true);
                var simulation=CampConstructionAtCheckpoint(policy,assistants,storage:true);
                Require(simulation.Capture().SchemaVersion==Snapshot.PortableCountedLotSchema,
                    "The composed camp/mining/recipe scenario did not select the counted-stock recipe schema.");
                WorldStep(simulation,0,-1,actor:TestOnlyPolicy.CompanionId);WorldAdvance(simulation,5);
                PrepareRecipe347Workshop(simulation);Recipe347WaitForNextWorkWatch(simulation);
                var authority=policy.HostAuthority();var startCraft=Recipe347Start(simulation,"recipe347.concurrent.craft");
                var craftQuery=simulation.QueryCommand(authority,startCraft);
                Require(craftQuery.Supported&&craftQuery.Admissible,"The crafting worker could not start at the shared Watch boundary: "
                    +craftQuery.Code+" time="+simulation.Capture().RuleClock.ToString()+" companion="
                    +simulation.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).X.ToString()+","+
                    simulation.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).Y.ToString()+" workshop="
                    +simulation.Capture().Recipe347Workshops.Single().SiteX.ToString()+","+
                    simulation.Capture().Recipe347Workshops.Single().SiteY.ToString());
                var craftResult=simulation.Execute(authority,startCraft);
                Require(craftResult.Outcome==Outcome.Committed,"The crafting worker's shared work order was rejected: "+craftResult.Code);
                var campStart=CampConstructionCommand(simulation,CommandKind.StartTemporaryCampConstruction,
                    PressureCampId,"recipe347.concurrent.camp");
                var campQuery=simulation.QueryCommand(authority,campStart);
                Require(campQuery.Supported&&campQuery.Admissible,"The second actor could not start the existing camp-construction job beside active crafting: "+campQuery.Code);
                var campResult=simulation.Execute(authority,campStart);
                Require(campResult.Outcome==Outcome.Committed,"The second actor's camp-construction job was rejected: "+campResult.Code);
                var working=simulation.Capture();var order=working.Recipe347WorkOrders.Single();var camp=working.TemporaryCampConstructionAttempts.Single();
                var craftInterval=working.Work.WorkerIntervals.Single(x=>x.JobId==order.Id&&x.Start==working.RuleClock);
                var campInterval=working.Work.WorkerIntervals.Single(x=>x.JobId==camp.Id&&x.Start==working.RuleClock);
                Require(order.Status==Recipe347OrderStatus.Working&&camp.Status==TemporaryCampConstructionStatus.Working
                    &&craftInterval.WorkerId==TestOnlyPolicy.CompanionId&&campInterval.WorkerId==TestOnlyPolicy.ActorId
                    &&craftInterval.End>campInterval.Start&&campInterval.End>craftInterval.Start,
                    "The recipe and existing camp job did not book overlapping positive-duration intervals for distinct actors.");
                byte[] saved=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                WorldAdvance(left,900);WorldAdvance(right,900);
                var resumed=left.Capture();order=resumed.Recipe347WorkOrders.Single();camp=resumed.TemporaryCampConstructionAttempts.Single();
                Require(order.Work.CompletedPhases==1&&order.Work.Partial==default(RuleTime)
                    &&camp.Status==TemporaryCampConstructionStatus.Working&&camp.WorkDone==new RuleTime(900)
                    &&Bytes(left).SequenceEqual(Bytes(right)),
                    "Concurrent recipe-phase and camp-construction progress did not save, restore, and replay byte-identically.");
            });
            cases.Add("recipe347_interrupted_phase_resume_stops_without_booking_unfinishable_next_phase",()=>{
                var policy=Recipe347Policy(37);var simulation=World(policy);PrepareRecipe347Workshop(simulation);
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
                var started=simulation.Capture();var order=started.Recipe347WorkOrders.Single();
                WorldAdvance(simulation,900);
                Require(simulation.Capture().Recipe347WorkOrders.Single().Work.CompletedPhases==1,
                    "The source-defined initial fifteen-minute phase did not complete before interruption.");
                WorldAdvance(simulation,3600);
                order=simulation.Capture().Recipe347WorkOrders.Single();
                Require(order.Work.CompletedPhases==1&&order.Work.Partial==new RuleTime(3600)
                    &&order.Work.Labor==new RuleTime(4500),
                    "The interruption fixture did not accrue exactly one hour of the unfinished second phase.");
                var pause=new Command("recipe347.phase.pause."+simulation.Capture().Revision,TestOnlyPolicy.CompanionId,
                    simulation.Capture().Revision,CommandKind.PauseRecipe347,order.Id);
                Recipe347Commit(simulation,pause,policy);
                byte[] pausedBytes=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(pausedBytes),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(pausedBytes),ExecutionProfile.Laboratory);
                Require(left.Capture().Recipe347WorkOrders.Single().Work.CompletedPhases==1
                    &&left.Capture().Recipe347WorkOrders.Single().Work.Partial==default(RuleTime)
                    &&left.Capture().Recipe347WorkOrders.Single().Work.Labor==new RuleTime(4500)
                    &&pausedBytes.SequenceEqual(Bytes(left)),
                    "Interruption must discard only incomplete phase progress, retain the completed phase and actual labor, and restore byte-identically.");

                Command resume=null;
                for(int i=0;i<4;i++) {
                    var state=left.Capture();long now=checked((long)(state.RuleClock.Numerator/state.RuleClock.Denominator));
                    long remainder=now%28800;long toBoundary=remainder==0?0:28800-remainder;
                    if(toBoundary>0) {WorldAdvance(left,checked((int)toBoundary));WorldAdvance(right,checked((int)toBoundary));}
                    state=left.Capture();var current=state.Recipe347WorkOrders.Single();
                    resume=new Command("recipe347.phase.resume."+state.Revision,TestOnlyPolicy.CompanionId,state.Revision,
                        CommandKind.ResumeRecipe347,current.Id);
                    var query=left.QueryCommand(TestOnlySharedWorldPolicy.Host(),resume);
                    if(query.Supported&&query.Admissible)break;
                    Require(query.Supported&&!query.Admissible&&query.Code=="Recipe347ScheduledRestWatch",
                        "A non-rest canonical Watch must admit the interrupted order; only its scheduled Rest Watch may reject it.");
                    WorldAdvance(left,28800);WorldAdvance(right,28800);
                    resume=null;
                }
                Require(resume!=null,"No legal work Watch was found for the interrupted phase.");
                var leftQuery=left.QueryCommand(TestOnlySharedWorldPolicy.Host(),resume);
                Require(leftQuery.Supported&&leftQuery.Admissible&&leftQuery.Costs.Single().Amount==27900,
                    "The restored second phase must book only its exact seven-hour-forty-five-minute remainder.");
                Recipe347Commit(left,resume,policy);Recipe347Commit(right,resume,policy);
                WorldAdvance(left,27900);WorldAdvance(right,27900);
                var settledPhase=left.Capture();var resumed=settledPhase.Recipe347WorkOrders.Single();
                Require(resumed.Status==Recipe347OrderStatus.Paused&&resumed.Work.CompletedPhases==2
                    &&resumed.Work.Partial==default(RuleTime)&&resumed.Work.Labor==new RuleTime(32400)
                    &&!settledPhase.Work.WorkerIntervals.Any(x=>x.JobId==resumed.Id&&x.Start<=settledPhase.RuleClock&&x.End>settledPhase.RuleClock)
                    &&Bytes(left).SequenceEqual(Bytes(right)),
                    "After the 7h45m remainder, the order must pause at the completed phase without spending the leftover 15 minutes or diverging after restore.");
                Directory.CreateDirectory(directory);File.WriteAllBytes(Path.Combine(directory,"recipe347_interrupted_phase_restore.sav"),pausedBytes);
                File.WriteAllBytes(Path.Combine(directory,"recipe347_completed_phase_pause.sav"),Bytes(left));
            });
            cases.Add("recipe347_six_quality_bands_settle_singleton_inputs_and_mishap_remedy",()=>{
                var expected=new[]{
                    new{Quality=CraftQuality.Mishap,Hp=0,Mishap=2},
                    new{Quality=CraftQuality.Failed,Hp=0,Mishap=0},
                    new{Quality=CraftQuality.Flawed,Hp=2,Mishap=0},
                    new{Quality=CraftQuality.Standard,Hp=5,Mishap=0},
                    new{Quality=CraftQuality.Exceptional,Hp=6,Mishap=0},
                    new{Quality=CraftQuality.Masterwork,Hp=7,Mishap=0}};
                foreach(var result in expected) {
                    Recipe347PolicyForQuality(result.Quality,result.Mishap,out var policy,out var initial,
                        out int modifier,out int natural);
                    var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                    var order=CompleteRecipe347Order(simulation,policy,allowNonComplete:true);
                    var state=simulation.Capture();
                    Require(order.Quality==result.Quality&&order.CheckModifier==modifier&&order.Natural==natural
                        &&order.Work.Labor==new RuleTime(144000),
                        "Recipe-347 did not preserve its selected sourced check or exactly forty active work hours for "+result.Quality.ToString()+".");
                    var expectedWood=result.Quality==CraftQuality.Failed?new RuleQuantity(1):default;
                    var expectedMetal=default(RuleQuantity);var expectedGrip=default(RuleQuantity);var expectedRib=default(RuleQuantity);
                    if(result.Quality!=CraftQuality.Failed&&result.Quality!=CraftQuality.Mishap) {
                        expectedWood=default;expectedMetal=default;expectedGrip=default;expectedRib=default;
                    }
                    if(result.Quality==CraftQuality.Mishap) {
                        expectedWood=default;expectedMetal=default;expectedGrip=default;expectedRib=default;
                    }
                    Require(state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.ComponentLotIds[0]).Amount==expectedWood
                        &&state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.ComponentLotIds[1]).Amount==expectedMetal
                        &&state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.ComponentLotIds[2]).Amount==new RuleQuantity(1)
                        &&state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.ComponentLotIds[3]).Amount==expectedGrip
                        &&state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.ComponentLotIds[4]).Amount==expectedRib
                        &&state.Work.Lots.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyLotId).Amount==new RuleQuantity(3),
                        "Recipe-347 consumed the retained kit/body or returned an incorrect Failed/Mishap/success quantity for "+result.Quality.ToString()+".");
                    var woodItem=state.PortableEquipment.Single(x=>x.LinkKind==PortableLinkKind.InventoryLot
                        &&x.LinkedId==TestOnlyRecipe347Fixture.ComponentLotIds[0]);
                    RuleQuantity expectedWoodMass=result.Quality==CraftQuality.Failed?new RuleQuantity(1,10):default;
                    RuleQuantity expectedWoodVolume=result.Quality==CraftQuality.Failed?new RuleQuantity(1,50):default;
                    Require(PortableEquipmentValidation.Mass(state,woodItem)==expectedWoodMass
                        &&PortableStorageProfileValidation.PackedVolume(state,woodItem)==expectedWoodVolume
                        &&state.PortableEquipment.Count(x=>x.LinkKind==PortableLinkKind.InventoryLot
                            &&x.LinkedId==TestOnlyRecipe347Fixture.ComponentLotIds[0])==1,
                        "Settled wood count must remain one authoritative physical link with the exact returned mass and packed volume.");
                    if(result.Quality==CraftQuality.Mishap||result.Quality==CraftQuality.Failed) {
                        Require(order.Status==(result.Quality==CraftQuality.Mishap?Recipe347OrderStatus.Mishap:Recipe347OrderStatus.Failed)
                            &&state.Recipe347Outputs.Length==0&&state.Recipe347MiningToolProfiles.Length==0
                            &&state.Structures.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyStructureId).MaximumHp==5,
                            "Failed or Mishap crafting created a tool output or changed the separately reserved body.");
                    } else {
                        var output=state.Recipe347Outputs.Single(x=>x.OrderId==order.Id);
                        var profile=state.Recipe347MiningToolProfiles.Single(x=>x.ProvenanceId==output.Id);
                        var structure=state.Structures.Single(x=>x.Id==TestOnlyRecipe347Fixture.BodyStructureId);
                        var expectedChoice=result.Quality==CraftQuality.Exceptional||result.Quality==CraftQuality.Masterwork
                            ?CraftQualityChoice.Durability:CraftQualityChoice.StandardQuantity;
                        Require(order.Status==Recipe347OrderStatus.Complete&&order.Choice==expectedChoice
                            &&output.ItemId==TestOnlyRecipe347Fixture.BodyItemId&&profile.ItemId==output.ItemId
                            &&output.Quality==result.Quality&&structure.MaximumHp==result.Hp&&structure.Hp==result.Hp
                            &&state.Recipe347Outputs.Length==1,
                            "A successful band failed to transform exactly one existing body with its reviewed structural maximum. quality="
                            +result.Quality.ToString()+" status="+order.Status.ToString()+" choice="+order.Choice.ToString()
                            +" outputs="+state.Recipe347Outputs.Length.ToString()+" outputItem="+output.ItemId
                            +" profileItem="+profile.ItemId+" outputQuality="+output.Quality.ToString()
                            +" expectedHp="+result.Hp.ToString()+" structureHp="+structure.Hp.ToString()
                            +" structureMax="+structure.MaximumHp.ToString());
                    }
                    if(result.Quality==CraftQuality.Mishap) {
                        var incident=state.CraftingIncidents.Single(x=>x.Id==order.IncidentId);
                        Require(order.MishapResult==result.Mishap&&incident.Result==result.Mishap
                            &&incident.ToolId==TestOnlyRecipe347Fixture.MiningToolsStructureId&&incident.TradeId=="Mining"
                            &&incident.RequiredLabor==new RuleTime(7200)&&incident.At>new RuleTime(57600)
                            &&CraftingRestrictions.CraftingCheckBlocked(state,TestOnlyRecipe347Fixture.MiningToolsStructureId),
                            "The late recipe Mishap did not bind Mining's primary Miner’s-tools target and its two-hour recalibration remedy.");
                        var remedy=new Command("recipe347.mishap.remedy."+state.Revision,TestOnlyPolicy.CompanionId,
                            state.Revision,CommandKind.StartCraftRemedy,incident.Id);
                        var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),remedy);
                        if(query.Supported&&!query.Admissible&&query.Code=="Recipe347ScheduledRestWatch") {
                            WorldAdvance(simulation,28800);state=simulation.Capture();incident=state.CraftingIncidents.Single(x=>x.Id==order.IncidentId);
                            remedy=new Command("recipe347.mishap.remedy."+state.Revision,TestOnlyPolicy.CompanionId,
                                state.Revision,CommandKind.StartCraftRemedy,incident.Id);
                            query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),remedy);
                        }
                        byte[] beforeRemedy=Bytes(simulation);
                        Require(query.Supported&&query.Admissible&&query.Costs.Count==0&&Bytes(simulation).SequenceEqual(beforeRemedy),
                            "The source-qualified Mining remedy was unavailable after the legacy sixteen-hour window or its query mutated state. supported="
                            +query.Supported.ToString()+" admissible="+query.Admissible.ToString()+" code="+query.Code
                            +" costs="+query.Costs.Count.ToString()+" unchanged="+Bytes(simulation).SequenceEqual(beforeRemedy).ToString()
                            +" incidentAt="+incident.At.ToString()+" now="+state.RuleClock.ToString());
                        Recipe347Commit(simulation,remedy,policy);WorldAdvance(simulation,7200);
                        var remedied=simulation.Capture();incident=remedied.CraftingIncidents.Single(x=>x.Id==order.IncidentId);
                        Require(incident.Remedied&&incident.Labor==incident.RequiredLabor
                            &&!CraftingRestrictions.CraftingCheckBlocked(remedied,TestOnlyRecipe347Fixture.MiningToolsStructureId),
                            "The post-recipe Mining remedy did not settle against the actual Miner’s-tools target.");
                    }
                }
            });
            cases.Add("recipe347_pending_quality_choice_queries_for_free_and_restores_clock_continuation",()=>{
                Recipe347PolicyForQuality(CraftQuality.Masterwork,0,out var policy,out var initial,
                    out _,out _);
                var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                var pending=Recipe347ReachQualityChoice(simulation,policy,3600);
                var before=simulation.Capture();byte[] pendingBytes=Bytes(simulation);
                Require(pending.Status==Recipe347OrderStatus.AwaitingChoice&&pending.Quality==CraftQuality.Masterwork
                    &&before.ManufacturingAdvance!=null&&before.ManufacturingAdvance.Target>before.RuleClock,
                    "The earned Masterwork choice did not pause at the result while retaining the original clock target.");
                var command=new Command("recipe347.masterwork.choice."+before.Revision,TestOnlyPolicy.CompanionId,
                    before.Revision,CommandKind.ResolveRecipe347Quality,pending.Id,(int)CraftQualityChoice.Durability);
                var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),command);
                Require(query.Supported&&query.Admissible&&query.Costs.Count==0&&Bytes(simulation).SequenceEqual(pendingBytes),
                    "The pending recipe quality choice was not queryable without cost or state mutation. supported="
                    +query.Supported.ToString()+" admissible="+query.Admissible.ToString()+" code="+query.Code
                    +" costs="+query.Costs.Count.ToString()+" unchanged="+Bytes(simulation).SequenceEqual(pendingBytes).ToString()
                    +" advance="+(before.ManufacturingAdvance==null?"null":before.ManufacturingAdvance.Target.ToString())
                    +" status="+pending.Status.ToString());
                var restored=new Simulation(policy,new SnapshotCodec().Decode(pendingBytes),ExecutionProfile.Laboratory);
                Require(pendingBytes.SequenceEqual(Bytes(restored)),"The pending-choice save did not restore byte-identically.");
                Recipe347Commit(restored,command,policy);byte[] settled=Bytes(restored);
                Require(restored.Capture().Recipe347WorkOrders.Single().Status==Recipe347OrderStatus.Complete
                    &&restored.Capture().Recipe347WorkOrders.Single().Choice==CraftQualityChoice.Durability
                    &&restored.Capture().RuleClock==before.ManufacturingAdvance.Target
                    &&restored.Execute(TestOnlySharedWorldPolicy.Host(),command).Outcome==Outcome.Duplicate
                    &&Bytes(restored).SequenceEqual(settled),
                    "Resolving the restored pending choice lost its clock continuation, repeated settlement, or failed duplicate receipt handling.");
            });
            cases.Add("recipe347_portable_handling_cannot_cross_a_phase_boundary_and_next_phase_continues",()=>{
                var policy=Recipe347Policy(1,new SharedMiningFixture(siteX:1,siteY:0));
                var simulation=World(policy);PrepareRecipe347Workshop(simulation);
                var workshop=simulation.Capture().Recipe347Workshops.Single();
                var primaryForHandling=simulation.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId);
                Require(Math.Abs((long)primaryForHandling.X-workshop.SiteX)
                    +Math.Abs((long)primaryForHandling.Y-workshop.SiteY)<=1,
                    "The primary actor is not physically adjacent to the unclaimed workshop kit used for synchronous handling: actor="
                    +primaryForHandling.X.ToString()+","+primaryForHandling.Y.ToString()+" workshop="
                    +workshop.SiteX.ToString()+","+workshop.SiteY.ToString()+".");
                Recipe347WaitForNextWorkWatch(simulation);
                var start=Recipe347Start(simulation,"recipe347.portable-boundary.start");
                var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),start);
                Require(query.Supported&&query.Admissible,"The recipe work order was not queryable at an authorized Watch start.");
                Recipe347Commit(simulation,start,policy);var workStart=simulation.Capture().RuleClock;
                WorldAdvance(simulation,899);var beforeBoundary=Bytes(simulation);
                var order=simulation.Capture().Recipe347WorkOrders.Single();
                Require(order.Work.CompletedPhases==0&&order.Work.Partial==new RuleTime(899)
                    &&order.Work.Labor==new RuleTime(899),"The first recipe phase did not retain exactly 899 active seconds before its boundary.");
                var handling=Portable(simulation,CommandKind.HandlePortableEquipment,TestOnlyRecipe347Fixture.AssayKitId,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId);
                var handlingQuery=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),handling);
                var handlingResult=simulation.Execute(TestOnlySharedWorldPolicy.Host(),handling);
                Require(handlingQuery.Supported&&!handlingQuery.Admissible&&handlingQuery.Code=="TimedHandlingBoundaryUnsupported"
                    &&handlingResult.Outcome==Outcome.Rejected&&handlingResult.Code==handlingQuery.Code
                    &&Bytes(simulation).SequenceEqual(beforeBoundary),
                    "One-second portable handling crossed the recipe phase boundary or query and commit disagreed.");
                WorldAdvance(simulation,1);var boundary=simulation.Capture();order=boundary.Recipe347WorkOrders.Single();
                var nextInterval=boundary.Work.WorkerIntervals.Single(x=>x.JobId==order.Id&&x.Start==workStart.AddSeconds(900));
                Require(boundary.RuleClock==workStart.AddSeconds(900)&&order.Status==Recipe347OrderStatus.Working
                    &&order.Work.CompletedPhases==1&&order.Work.Partial==default(RuleTime)&&order.Work.Labor==new RuleTime(900)
                    &&nextInterval.End==workStart.AddSeconds(28800),
                    "Clock progression lost or overbooked the next source phase at the exact endpoint.");
                byte[] saved=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                WorldAdvance(left,120);WorldAdvance(right,120);
                Require(Bytes(left).SequenceEqual(Bytes(right))
                    &&left.Capture().Recipe347WorkOrders.Single().Work.Labor==new RuleTime(1020),
                    "Post-boundary active labor did not continue deterministically after save/restore.");
            });
            cases.Add("recipe347_completed_output_is_the_same_physically_usable_mining_tool",()=>{
                Recipe347StandardPolicy(out var policy,out var initial,out int craftModifier);
                var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                var order=CompleteRecipe347Order(simulation,policy);var crafted=simulation.Capture();
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
                Recipe347WaitForNextWorkWatch(resumed);
                var start=MiningCommand(resumed,CommandKind.StartMining,SharedMiningFixture.DepositId,selection,
                    commandId:"recipe347.mine.first.start");
                MiningCommit(resumed,start);
                var deployed=resumed.Capture();var attempt=deployed.MiningAttempts.Single();
                var candidate=deployed.MiningToolCandidateProfiles.Single(x=>x.DepositId==SharedMiningFixture.DepositId
                    &&x.ToolItemId==tool.ItemId);
                var use=deployed.MiningToolUses.Single(x=>x.MiningAttemptId==attempt.Id);
                Require(candidate.StructureId==tool.StructureId&&use.ProfileId==candidate.Id
                    &&use.PreparedUnitId==SharedMiningFixture.UnitA&&use.ReservedUnitId==SharedMiningFixture.UnitB
                    &&deployed.Work.Reservations.Single(x=>x.Id==MiningIds.ToolReserveReservation(attempt.Id)).Status==ReservationStatus.Reserved,
                    "Mining must bind the same recipe output to the shared candidate, preparation, and distinct reserved stock authorities.");
                WorldAdvance(resumed,attempt.DurationSeconds);
                var mined=resumed.Capture();attempt=mined.MiningAttempts.Single();
                use=mined.MiningToolUses.Single(x=>x.MiningAttemptId==attempt.Id);
                Require(attempt.CheckModifier==baseMiningModifier+2&&use.CheckBonusApplied
                    &&use.ToolWorkDone>=new RuleTime(60)&&use.PreparationCompletedAt.HasValue
                    &&use.DressedBenefitAwarded&&use.CriticalReserveAwardedUnitId==SharedMiningFixture.UnitB,
                    "Shared mining records must settle the +2, measured dressing, and critical reserve from the physical recipe output.");
                byte[] savedMining=Bytes(resumed);var restored=new Simulation(policy,new SnapshotCodec().Decode(savedMining),ExecutionProfile.Laboratory);
                Require(savedMining.SequenceEqual(Bytes(restored)),"Completed mining candidate use, preparation, or reserve changed across schema72 restore.");
                Require(restored.Execute(TestOnlySharedWorldPolicy.Host(),start).Outcome==Outcome.Duplicate
                    &&savedMining.SequenceEqual(Bytes(restored)),"Replaying the recorded Mining start repeated extraction or tool effects.");

                var movedBeforeCheck=new Simulation(policy,new SnapshotCodec().Decode(preMining),ExecutionProfile.Laboratory);
                Recipe347WaitForNextWorkWatch(movedBeforeCheck);
                var pendingStart=MiningCommand(movedBeforeCheck,CommandKind.StartMining,SharedMiningFixture.DepositId,selection,
                    commandId:"recipe347.mine.pending.start");MiningCommit(movedBeforeCheck,pendingStart);
                WorldAdvance(movedBeforeCheck,movedBeforeCheck.Capture().MiningAttempts.Single().DurationSeconds-1);
                var pendingAttempt=movedBeforeCheck.Capture().MiningAttempts.Single();
                MiningCommit(movedBeforeCheck,MiningCommand(movedBeforeCheck,CommandKind.PauseMining,pendingAttempt.Id));
                Recipe347WaitForActivityWindow(movedBeforeCheck);
                PortableCommit(movedBeforeCheck,Portable(movedBeforeCheck,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.CompanionId));
                WorldStep(movedBeforeCheck,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(movedBeforeCheck,1);
                Recipe347WaitForActivityWindow(movedBeforeCheck);
                PortableCommit(movedBeforeCheck,Portable(movedBeforeCheck,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId));
                MiningCommit(movedBeforeCheck,MiningCommand(movedBeforeCheck,CommandKind.ResumeMining,pendingAttempt.Id));
                WorldAdvance(movedBeforeCheck,1);
                var excluded=movedBeforeCheck.Capture();var excludedUse=excluded.MiningToolUses.Single(x=>x.MiningAttemptId==pendingAttempt.Id);
                Require(excluded.MiningAttempts.Single(x=>x.Id==pendingAttempt.Id).CheckModifier==baseMiningModifier
                    &&!excludedUse.CheckBonusApplied&&excludedUse.CriticalReserveAwardedUnitId=="",
                    "Moving the body after measured work but before the unresolved check must remove all recipe-tool effects.");
            });
            cases.Add("recipe347_same_tool_works_at_two_deposits_and_only_when_physically_deployed",()=>{
                Recipe347StandardPolicy(out var policy,out var initial,out _,TwoDepositRecipe347Mining());
                var simulation=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                var order=CompleteRecipe347Order(simulation,policy);var crafted=simulation.Capture();
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
                Recipe347WaitForNextWorkWatch(absent);
                MiningCommit(absent,MiningCommand(absent,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    firstSelection,commandId:"recipe347.mine.first.absent"));
                WorldAdvance(absent,absent.Capture().MiningAttempts.Single().DurationSeconds);
                Require(absent.Capture().MiningAttempts.Single().CheckModifier==baseModifier
                    &&absent.Capture().MiningToolUses.Length==0&&absent.Capture().Recipe347MiningToolUseEvidence.Length==0,
                    "The same profile must supply no check bonus when its physical item is elsewhere.");

                var deployed=new Simulation(policy,new SnapshotCodec().Decode(craftedSave),ExecutionProfile.Laboratory);
                baseModifier=MiningModifier(deployed.Capture());
                Recipe347WaitForNextWorkWatch(deployed);
                MiningCommit(deployed,MiningCommand(deployed,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    firstSelection,commandId:"recipe347.mine.first.deployed"));
                WorldAdvance(deployed,deployed.Capture().MiningAttempts.Single().DurationSeconds);
                var firstAttempt=deployed.Capture().MiningAttempts.Single();
                var firstUse=deployed.Capture().MiningToolUses.Single(x=>x.MiningAttemptId==firstAttempt.Id);
                Require(firstAttempt.CheckModifier==baseModifier+2
                    &&firstUse.CheckBonusApplied&&firstUse.ToolWorkDone>=new RuleTime(60),
                    "The crafted item must use the shared candidate work record for its +2 check bonus at the first deposit.");
                Recipe347WaitForActivityWindow(deployed);
                PortableCommit(deployed,Portable(deployed,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.CompanionId));
                WorldStep(deployed,1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(deployed,1);
                Recipe347WaitForActivityWindow(deployed);
                PortableCommit(deployed,Portable(deployed,CommandKind.HandlePortableEquipment,tool.ItemId,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId));
                var secondDeposit=deployed.Capture().MiningDeposits.Single(x=>x.Id=="TEST_ONLY.mining.deposit.second");
                var relocated=deployed.Capture().PortableEquipment.Single(x=>x.Id==tool.ItemId);
                var relocatedStructure=deployed.Capture().Structures.Single(x=>x.Id==tool.StructureId);
                Require(relocated.Placement==PortablePlacement.Ground&&relocated.GroundX==secondDeposit.SiteX
                    &&relocated.GroundY==secondDeposit.SiteY&&relocatedStructure.LocationId==secondDeposit.SiteId,
                    "The same output item and its authoritative structure location must move between deposit sites through physical pickup, traversal and drop.");
                byte[] afterMove=Bytes(deployed);
                var restoredAfterMove=new Simulation(policy,new SnapshotCodec().Decode(afterMove),ExecutionProfile.Laboratory);
                var historicalUse=restoredAfterMove.Capture().MiningToolUses.Single(x=>x.MiningAttemptId==firstAttempt.Id);
                Require(afterMove.SequenceEqual(Bytes(restoredAfterMove))&&historicalUse.CheckBonusApplied
                    &&restoredAfterMove.Capture().MiningAttempts.Single(x=>x.Id==firstAttempt.Id).CheckModifier==firstAttempt.CheckModifier,
                    "Moving the output after the completed extraction must preserve its historical +2 result through save and restore.");
                deployed=restoredAfterMove;
                int secondBase=MiningModifier(deployed.Capture());
                var secondStockIds=deployed.Capture().MiningUnits.Where(x=>x.DepositId==secondDeposit.Id)
                    .Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                var secondSelection=new MiningSelectionRequest(secondDeposit.VersionId,
                    new[]{"TEST_ONLY.mining.category.second"},MiningAbilityChoice.Wisdom);
                Recipe347WaitForActivityWindow(deployed);
                Recipe347WaitForNextWorkWatch(deployed);
                MiningCommit(deployed,MiningCommand(deployed,CommandKind.StartMining,secondDeposit.Id,secondSelection,
                    commandId:"recipe347.mine.second.deployed"));
                var secondAttempt=deployed.Capture().MiningAttempts.Single(x=>x.DepositId==secondDeposit.Id);
                byte[] partial=Bytes(deployed);var left=new Simulation(policy,new SnapshotCodec().Decode(partial),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(partial),ExecutionProfile.Laboratory);
                WorldAdvance(left,secondAttempt.DurationSeconds);WorldAdvance(right,secondAttempt.DurationSeconds);
                var final=left.Capture();secondAttempt=final.MiningAttempts.Single(x=>x.DepositId==secondDeposit.Id);
                int sharedUses=final.MiningToolUses.Count(x=>final.MiningToolCandidateProfiles.Any(p=>p.ToolItemId==tool.ItemId&&p.Id==x.ProfileId));
                var finalSecondStockIds=final.MiningUnits.Where(x=>x.DepositId==secondDeposit.Id)
                    .Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                bool replayMatches=Bytes(left).SequenceEqual(Bytes(right));
                Require(secondAttempt.CheckModifier==secondBase+2&&sharedUses==2&&replayMatches
                    &&secondStockIds.SequenceEqual(finalSecondStockIds),
                    "The unchanged physical tool must earn +2 at a distinct deposit, with save/restore replay producing identical state."
                    +" check="+secondAttempt.CheckModifier.ToString()+" base="+secondBase.ToString()
                    +" sharedUses="+sharedUses.ToString()+" replay="+replayMatches.ToString()
                    +" finiteStockIdsPreserved="+secondStockIds.SequenceEqual(finalSecondStockIds).ToString());
            });
            cases.Add("recipe347_counted_lot_split_transfer_store_conserves_mass_volume_and_replays",()=>{
                var policy=Recipe347Policy(23);var simulation=World(policy);PrepareRecipe347Workshop(simulation);
                var before=simulation.Capture();string lotId=TestOnlyRecipe347Fixture.ComponentLotIds[0];
                var original=before.PortableEquipment.Single(x=>x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==lotId);
                var crate=before.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
                RuleQuantity originalMass=PortableEquipmentValidation.Mass(before,original);
                RuleQuantity originalVolume=PortableStorageProfileValidation.PackedVolume(before,original);
                RuleQuantity originalContents=PortableStorageProfileValidation.ContentsVolume(before,crate);
                Require(original.MassBasis==PortableMassBasis.CountedQuantity&&originalMass==new RuleQuantity(1,2)
                    &&originalVolume==new RuleQuantity(1,10)&&originalContents<=crate.CapacityCubicFeet.Value,
                    "The five source handles must have exactly 0.5 lb and 0.1 ft3 and fit once inside the actual storage crate.");
                string childId="inventory."+(before.Revision+1).ToString(System.Globalization.CultureInfo.InvariantCulture)+".lot";
                var split=new Command("recipe347.counted.split."+before.Revision,TestOnlyPolicy.CompanionId,before.Revision,
                    CommandKind.PortionInventory,lotId,inventory:new InventoryRequest(new RuleQuantity(2)));
                var query=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),split);byte[] beforeSplit=Bytes(simulation);
                Require(query.Supported&&query.Admissible&&query.Costs.Count==0&&Bytes(simulation).SequenceEqual(beforeSplit),
                    "Two unreserved handles must be available through a free, nonmutating inventory split query. supported="
                    +query.Supported.ToString()+" admissible="+query.Admissible.ToString()+" code="+query.Code
                    +" costs="+query.Costs.Count.ToString()+" unchanged="+Bytes(simulation).SequenceEqual(beforeSplit).ToString());
                var result=simulation.Execute(TestOnlySharedWorldPolicy.Host(),split);
                Require(result.Outcome==Outcome.Committed,"Counted recipe stock split was rejected: "+result.Code);
                var splitState=simulation.Capture();var sourceItem=splitState.PortableEquipment.Single(x=>x.LinkedId==lotId);
                var childItem=splitState.PortableEquipment.Single(x=>x.LinkedId==childId);
                var sourceLot=splitState.Work.Lots.Single(x=>x.Id==lotId);var childLot=splitState.Work.Lots.Single(x=>x.Id==childId);
                var sourceMeta=splitState.InventoryLots.Single(x=>x.LotId==lotId);var childMeta=splitState.InventoryLots.Single(x=>x.LotId==childId);
                Require(sourceLot.Amount==new RuleQuantity(3)&&childLot.Amount==new RuleQuantity(2)
                    &&sourceLot.Amount+childLot.Amount==new RuleQuantity(5)&&childMeta.ParentId==lotId
                    &&childMeta.OwnerId==sourceMeta.OwnerId&&childMeta.FreshUntil==sourceMeta.FreshUntil
                    &&sourceItem.ProfileId==childItem.ProfileId&&childItem.MassBasis==PortableMassBasis.CountedQuantity
                    &&childItem.ParentId==TestOnlyPortableStorageFixture.CrateId
                    &&PortableEquipmentValidation.Mass(splitState,sourceItem)+PortableEquipmentValidation.Mass(splitState,childItem)==originalMass
                    &&PortableStorageProfileValidation.PackedVolume(splitState,sourceItem)
                        +PortableStorageProfileValidation.PackedVolume(splitState,childItem)==originalVolume
                    &&PortableStorageProfileValidation.ContentsVolume(splitState,splitState.PortableEquipment.Single(x=>x.Id==crate.Id))==originalContents,
                    "Splitting must preserve count, one shared profile, ancestry, owner, freshness, crate placement, mass and volume.");
                byte[] splitBytes=Bytes(simulation);var splitRestored=new Simulation(policy,new SnapshotCodec().Decode(splitBytes),ExecutionProfile.Laboratory);
                Require(splitBytes.SequenceEqual(Bytes(splitRestored)),"The counted child and its profile link changed across schema73 save/restore.");
                simulation=splitRestored;
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,childId,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.CompanionId));
                childItem=simulation.Capture().PortableEquipment.Single(x=>x.LinkedId==childId);
                Require(childItem.ParentId==""&&childItem.Placement==PortablePlacement.Carried
                    &&PortableEquipmentValidation.Mass(simulation.Capture(),childItem)==new RuleQuantity(1,5)
                    &&PortableStorageProfileValidation.PackedVolume(simulation.Capture(),childItem)==new RuleQuantity(1,25),
                    "Retrieval must move the same two-count child without altering its physical profile.");
                Recipe347PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,childId,
                    TestOnlyPortableStorageFixture.CrateId,HandlingKind.Stow,TestOnlyPolicy.CompanionId));
                var stored=simulation.Capture();childItem=stored.PortableEquipment.Single(x=>x.LinkedId==childId);
                Require(childItem.ParentId==TestOnlyPortableStorageFixture.CrateId
                    &&PortableEquipmentValidation.Mass(stored,childItem)==new RuleQuantity(1,5)
                    &&PortableStorageProfileValidation.PackedVolume(stored,childItem)==new RuleQuantity(1,25)
                    &&PortableStorageProfileValidation.ContentsVolume(stored,stored.PortableEquipment.Single(x=>x.Id==crate.Id))==originalContents,
                    "Stowing the moved child must conserve the original crate capacity, count, mass and volume.");
                byte[] storedBytes=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(storedBytes),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(storedBytes),ExecutionProfile.Laboratory);
                WorldAdvance(left,6);WorldAdvance(right,6);
                Require(Bytes(left).SequenceEqual(Bytes(right)),"Restored counted-lot handling continuations did not replay deterministically.");
                var wrongProfile=left.Capture().Copy();var target=wrongProfile.PortableEquipment.Single(x=>x.LinkedId==childId);
                wrongProfile.PortableEquipment=wrongProfile.PortableEquipment.Select(x=>x.Id==target.Id
                    ?new PortableEquipmentRecord(x.Id,"prototype.food-lot",x.OwnerId,x.CustodianId,x.ParentId,x.Placement,
                        x.LinkKind,x.LinkedId,x.MassBasis,null,null):x).ToArray();
                Throws<ArgumentException>(()=>Validation.Snapshot(wrongProfile));
                var duplicate=left.Capture().Copy();target=duplicate.PortableEquipment.Single(x=>x.LinkedId==childId);
                duplicate.PortableEquipment=duplicate.PortableEquipment.Concat(new[]{new PortableEquipmentRecord(
                    target.Id+".duplicate",target.ProfileId,target.OwnerId,target.CustodianId,target.ParentId,target.Placement,
                    target.LinkKind,target.LinkedId,target.MassBasis,null,null)}).ToArray();
                Throws<ArgumentException>(()=>Validation.Snapshot(duplicate));
            });
            cases.Add("recipe347_counted_lot_reservations_preserve_physical_capacity_and_block_moves",()=>{
                var policy=Recipe347Policy(29,new SharedMiningFixture(siteX:2,siteY:3));var simulation=World(policy);
                Recipe347MovePrimaryActorTo(simulation,1,2);
                PrepareRecipe347WorkshopBesideCampStorage(simulation);
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
                var claimed=simulation.Capture();string lotId=TestOnlyRecipe347Fixture.ComponentLotIds[0];
                var physical=claimed.PortableEquipment.Single(x=>x.LinkedId==lotId);
                var crate=claimed.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
                RuleQuantity mass=PortableEquipmentValidation.Mass(claimed,physical);
                RuleQuantity volume=PortableStorageProfileValidation.PackedVolume(claimed,physical);
                RuleQuantity contents=PortableStorageProfileValidation.ContentsVolume(claimed,crate);
                Require(claimed.Work.AvailableAmount(lotId)==default&&claimed.Work.Lots.Single(x=>x.Id==lotId).Amount==new RuleQuantity(5)
                    &&PortableEquipmentValidation.Mass(claimed,physical)==mass
                    &&PortableStorageProfileValidation.PackedVolume(claimed,physical)==volume
                    &&PortableStorageProfileValidation.ContentsVolume(claimed,crate)==contents
                    &&contents<=crate.CapacityCubicFeet.Value,
                    "Reservation must reduce available handles while leaving physical mass and packed-volume capacity unchanged.");
                var move=Portable(simulation,CommandKind.HandlePortableEquipment,crate.Id,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId);
                byte[] beforeMoveQuery=Bytes(simulation);
                var moveQuery=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),move);
                Require(moveQuery.Supported&&!moveQuery.Admissible&&moveQuery.Code=="PortableItemHasPendingWork"
                    &&beforeMoveQuery.SequenceEqual(Bytes(simulation)),
                    "A physical parent with a live component claim must not be moved out of storage.");
                var split=new Command("recipe347.counted.reserved-split."+claimed.Revision,TestOnlyPolicy.ActorId,claimed.Revision,
                    CommandKind.PortionInventory,lotId,inventory:new InventoryRequest(new RuleQuantity(1)));
                var splitQuery=simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(),split);
                Require(splitQuery.Supported&&!splitQuery.Admissible&&splitQuery.Code=="InventoryQuantityUnavailable",
                    "The existing split command must not divide quantity already reserved by the shared work order.");
                byte[] save=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(save),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(save),ExecutionProfile.Laboratory);
                WorldAdvance(left,900);WorldAdvance(right,900);
                Require(Bytes(left).SequenceEqual(Bytes(right))
                    &&PortableEquipmentValidation.Mass(left.Capture(),left.Capture().PortableEquipment.Single(x=>x.LinkedId==lotId))==mass,
                    "A save during counted-stock reservation must continue the work and preserve physical mass deterministically.");
            });
            cases.Add("recipe347_existing_storage_acquisition_transfers_same_lot_to_qualified_worker",()=>{
                var policy=Recipe347Policy(31,new SharedMiningFixture(siteX:2,siteY:3));var simulation=World(policy);
                Recipe347MovePrimaryActorTo(simulation,1,2);
                var initial=simulation.Capture();var workshop=initial.Recipe347Workshops.Single();
                Recipe347MoveCompanionTo(simulation,workshop.SiteX,workshop.SiteY);
                string lotId=TestOnlyRecipe347Fixture.ComponentLotIds[0];
                var source=initial.PortableEquipment.Single(x=>x.LinkedId==lotId);
                PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,source.Id,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
                Recipe347MovePrimaryActorTo(simulation,1,3);
                PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,source.Id,
                    TestOnlyPolicy.CompanionId,HandlingKind.Handover,TestOnlyPolicy.ActorId));
                var transferred=simulation.Capture();var moved=transferred.PortableEquipment.Single(x=>x.LinkedId==lotId);
                Require(moved.OwnerId==source.OwnerId&&moved.CustodianId==TestOnlyPolicy.CompanionId
                    &&moved.ParentId==""&&moved.Placement==PortablePlacement.Carried
                    &&transferred.Work.Lots.Single(x=>x.Id==lotId).Amount==new RuleQuantity(5)
                    &&transferred.Work.Lots.Single(x=>x.Id==lotId).LocationId==TestOnlyPolicy.CompanionId
                    &&PortableEquipmentValidation.Mass(transferred,moved)==new RuleQuantity(1,2)
                    &&PortableStorageProfileValidation.PackedVolume(transferred,moved)==new RuleQuantity(1,10),
                    "The primary actor must retrieve the same five-count physical lot and willingly transfer custody to the trained companion. owner="
                    +moved.OwnerId+" custodian="+moved.CustodianId+" parent="+moved.ParentId+" placement="+moved.Placement.ToString()
                    +" amount="+transferred.Work.Lots.Single(x=>x.Id==lotId).Amount.ToString()+" location="
                    +transferred.Work.Lots.Single(x=>x.Id==lotId).LocationId+" mass="+PortableEquipmentValidation.Mass(transferred,moved).ToString()
                    +" volume="+PortableStorageProfileValidation.PackedVolume(transferred,moved).ToString());
                PrepareRecipe347WorkshopBesideCampStorage(simulation);
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
                var working=simulation.Capture();var order=working.Recipe347WorkOrders.Single();
                Require(order.Status==Recipe347OrderStatus.Working&&order.ComponentLotIds.Contains(lotId)
                    &&working.Work.Reservations.Single(x=>x.JobId==order.Id&&x.LotId==lotId).Amount==new RuleQuantity(5)
                    &&working.Work.AvailableAmount(lotId)==default
                    &&working.PortableEquipment.Single(x=>x.LinkedId==lotId).CustodianId==TestOnlyPolicy.CompanionId,
                    "The qualified worker must reserve the exact acquired lot through the shared WorkLedger.");
                byte[] save=Bytes(simulation);var left=new Simulation(policy,new SnapshotCodec().Decode(save),ExecutionProfile.Laboratory);
                var right=new Simulation(policy,new SnapshotCodec().Decode(save),ExecutionProfile.Laboratory);
                WorldAdvance(left,900);WorldAdvance(right,900);
                Require(Bytes(left).SequenceEqual(Bytes(right)),"Transferred, reserved recipe stock did not continue identically after save/restore.");
            });
            cases.Add("recipe347_work_order_shares_mining_inventory_and_roundtrips",()=>{
                var policy=Recipe347Policy(17);var simulation=World(policy);var initial=simulation.Capture();
                Require(initial.SchemaVersion==Snapshot.PortableCountedLotSchema&&initial.MiningDeposits.Length==1
                    &&initial.PortableStorageProfiles.Length>0&&initial.Recipe347FormulaAccess.Length==1,
                    "The composed world did not select the expected schema73 counted-stock, Mining and recipe profile.");
                PrepareRecipe347Workshop(simulation);
                var staged=simulation.Capture();
                Require(staged.PortableHandling.Count(x=>x.ActorId==TestOnlyPolicy.CompanionId)>=6
                    &&staged.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId).Placement==PortablePlacement.Ground
                    &&staged.PortableEquipment.Where(x=>TestOnlyRecipe347Fixture.ComponentLotIds.Contains(x.LinkedId))
                        .All(x=>x.ParentId==TestOnlyPortableStorageFixture.CrateId&&x.CustodianId==TestOnlyPolicy.CompanionId)
                    &&staged.PortableEquipment.Single(x=>x.Id==TestOnlyRecipe347Fixture.MiningToolsItemId).GroundX==staged.Recipe347Workshops.Single().SiteX,
                    "Actual movement and handling commands did not transfer counted stock and stage the implements at the worksite.");
                Recipe347WaitForNextWorkWatch(simulation);
                Recipe347Commit(simulation,Recipe347Start(simulation),policy);
                var working=simulation.Capture();var order=working.Recipe347WorkOrders.Single();
                var workStart=working.RuleClock;
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
                Require(left.Capture().RuleClock==workStart.AddSeconds(28800)
                    &&left.Capture().Recipe347WorkOrders.Single().Status==Recipe347OrderStatus.Paused
                    &&Bytes(left).SequenceEqual(Bytes(restored)),
                    "The first full work Watch must stop 8 hours after the accepted start and roundtrip byte-identically.");
            });
        }
    }
}
#endif
