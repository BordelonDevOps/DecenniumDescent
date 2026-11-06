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
        private const string OrdinaryLockA="TEST_ONLY.lock-a",OrdinaryLockB="TEST_ONLY.lock-b";
        private const string OrdinaryContainerA="TEST_ONLY.receptacle-a",OrdinaryContainerB="TEST_ONLY.receptacle-b";
        private const string OrdinaryKeyA="TEST_ONLY.key-a",OrdinaryKeyB="TEST_ONLY.key-b";
        private const string OrdinaryRationA="TEST_ONLY.ration-a",OrdinaryRationB="TEST_ONLY.ration-b";

        private static OrdinaryReceptacleFixture OrdinaryFixture(uint seed=1)
            =>new OrdinaryReceptacleFixture(new[]{
                new OrdinaryReceptacleDefinition(OrdinaryLockA,OrdinaryContainerA,OrdinaryKeyA,OrdinaryRationA,1,0),
                new OrdinaryReceptacleDefinition(OrdinaryLockB,OrdinaryContainerB,OrdinaryKeyB,OrdinaryRationB,0,1)
            },new[]{OrdinaryKeyB},toolsProficient:true,seed:seed);

        private static TestOnlySharedWorldPolicy OrdinaryPolicy(uint seed=1)=>new TestOnlySharedWorldPolicy(OrdinaryFixture(seed));
        private static Command OrdinaryLockCommand(Simulation s,string target,OrdinaryReceptacleInteraction operation,string id=null)
            =>IC(s,CommandKind.Interact,target,actor:TestOnlyPolicy.ActorId,x:(int)operation,id:id);
        private static void OrdinaryCommit(Simulation s,Command c)
        {var result=s.Execute(TestOnlySharedWorldPolicy.Host(),c);Require(result.Outcome==Outcome.Committed,"Ordinary receptacle command rejected: "+c.Target+" "+c.X+" "+result.Code);}
        private static void AddOrdinaryReceptacleCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("contextual_lock_commands_discover_and_query_without_mutation",()=>{
                var cachePolicy=SupplyPolicy(toolsProficient:true,hasKey:true,hasTools:true);
                var cache=SupplyWorld(cachePolicy);SupplyApproach(cache);byte[] cacheBefore=Bytes(cache);
                var cachePick=SupplyCommand(cache,SupplyCacheInteraction.PickWithTools,id:"context-cache-preview");
                var cacheQuery=cache.QueryCommand(host,cachePick);
                Require(cacheQuery.Supported&&cacheQuery.Admissible&&cacheQuery.Costs.Any(x=>x.Kind=="action"&&x.Amount==1)
                    &&cacheQuery.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==6)&&Bytes(cache).SequenceEqual(cacheBefore),
                    "The existing cache pick query was incorrect: supported="+cacheQuery.Supported+" admissible="+cacheQuery.Admissible
                    +" code="+cacheQuery.Code+" costs="+string.Join(",",cacheQuery.Costs.Select(x=>x.Kind+":"+x.Amount))
                    +" pure="+Bytes(cache).SequenceEqual(cacheBefore)+".");
                var cacheOptions=cache.DiscoverCommands(host,TestOnlyPolicy.ActorId).Where(x=>x.Command.Kind==CommandKind.Interact
                    &&x.Command.Target==SupplyCacheFixture.CacheId).ToArray();
                Require(cacheOptions.Any(x=>x.Command.X==(int)SupplyCacheInteraction.UnlockWithKey&&x.Query.Admissible)
                    &&cacheOptions.Any(x=>x.Command.X==(int)SupplyCacheInteraction.PickWithTools&&x.Query.Admissible)
                    &&!cacheOptions.Any(x=>x.Command.X==(int)SupplyCacheInteraction.Open),
                    "The reachable locked cache did not expose its available credentials as contextual commands.");
                SupplyCommit(cache,cacheOptions.Single(x=>x.Command.X==(int)SupplyCacheInteraction.PickWithTools).Command);
                WorldAdvance(cache,2);
                var cacheInterrupt=cache.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.Interact
                    &&x.Command.Target==SupplyCacheFixture.CacheId&&x.Command.X==(int)SupplyCacheInteraction.Interrupt);
                byte[] cachePending=Bytes(cache);
                Require(cacheInterrupt.Query.Admissible&&cacheInterrupt.Query.Costs.Count==0
                    &&cache.QueryCommand(host,cacheInterrupt.Command).Admissible&&Bytes(cache).SequenceEqual(cachePending),
                    "Cache interruption was not discoverable and queryable without changing active work.");
                SupplyCommit(cache,cacheInterrupt.Command);
                Require(cache.Capture().SupplyCacheAttempts.Single().Status==SupplyCacheAttemptStatus.Interrupted,
                    "The discovered cache interruption did not use the existing attempt path.");

                var receptaclePolicy=OrdinaryPolicy();var receptacle=World(receptaclePolicy);byte[] receptacleBefore=Bytes(receptacle);
                var lockOptions=receptacle.DiscoverCommands(host,TestOnlyPolicy.ActorId).Where(x=>x.Command.Kind==CommandKind.Interact
                    &&x.Command.Target==OrdinaryLockA).ToArray();
                var receptaclePick=lockOptions.SingleOrDefault(x=>x.Command.X==(int)OrdinaryReceptacleInteraction.PickWithTools);
                Require(receptaclePick!=null&&receptaclePick.Query.Admissible
                    &&receptaclePick.Query.Costs.Any(x=>x.Kind=="action"&&x.Amount==1)
                    &&receptaclePick.Query.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==6)
                    &&Bytes(receptacle).SequenceEqual(receptacleBefore),
                    "The reachable receptacle did not expose a pure existing thieves-tools option with staged costs.");
                OrdinaryCommit(receptacle,receptaclePick.Command);WorldAdvance(receptacle,2);
                var receptacleInterrupt=receptacle.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.Interact
                    &&x.Command.Target==OrdinaryLockA&&x.Command.X==(int)OrdinaryReceptacleInteraction.Interrupt);
                byte[] receptaclePending=Bytes(receptacle);
                Require(receptacleInterrupt.Query.Admissible&&receptacleInterrupt.Query.Costs.Count==0
                    &&receptacle.QueryCommand(host,receptacleInterrupt.Command).Admissible
                    &&Bytes(receptacle).SequenceEqual(receptaclePending),
                    "Receptacle interruption was not discoverable and queryable without changing active work.");
                OrdinaryCommit(receptacle,receptacleInterrupt.Command);
                Require(receptacle.Capture().OrdinaryReceptacleAttempts.Single().Status==OrdinaryReceptacleAttemptStatus.Interrupted,
                    "The discovered receptacle interruption did not use the existing attempt path.");
            });
            cases.Add("ordinary_receptacle_schema50_authored_physical_locks_and_closed_stock",()=>{
                var p=OrdinaryPolicy();var s=World(p);var v=s.Capture();
                Require(v.SchemaVersion==Snapshot.OrdinaryReceptacleSchema&&v.OrdinaryReceptacleLocks.Length==2
                    &&v.OrdinaryReceptacleLocks.All(x=>x.Locked)&&v.PortableEquipment.Single(x=>x.Id==OrdinaryContainerA).Placement==PortablePlacement.Ground
                    &&!v.PortableEquipment.Single(x=>x.Id==OrdinaryContainerA).Open
                    &&v.Work.Lots.Single(x=>x.Id==OrdinaryRationA).LocationId==OrdinaryContainerA
                    &&v.Work.Lots.Single(x=>x.Id==OrdinaryRationB).LocationId==OrdinaryContainerB
                    &&v.PortableEquipment.Single(x=>x.Id==OrdinaryKeyB).MassBasis==PortableMassBasis.Unmodeled
                    &&!v.PortableEquipment.Any(x=>x.Id==OrdinaryKeyA),"Authored physical lock, unknown key mass or finite closed stock was not preserved.");
                byte[] before=Bytes(s);var missingKey=OrdinaryLockCommand(s,OrdinaryLockA,OrdinaryReceptacleInteraction.UnlockWithKey,"ordinary-missing-key");
                var query=p.QueryCommand(s.Capture(),host,missingKey);
                bool queryPure=Bytes(s).SequenceEqual(before);
                Require(query.Supported&&!query.Admissible&&query.Code=="PhysicalKeyUnavailable"&&queryPure,
                    "Unexpected key query: supported="+query.Supported+" admissible="+query.Admissible+" code="+query.Code+" pure="+queryPure+".");
                RejectUnchanged(s,host,missingKey,"PhysicalKeyUnavailable");
                RejectUnchanged(s,host,Portable(s,CommandKind.OpenPortableContainer,OrdinaryContainerA),"PortableContainerLocked");
                RejectUnchanged(s,host,Portable(s,CommandKind.HandlePortableEquipment,OrdinaryRationA,handling:HandlingKind.Retrieve),"PortableItemOutOfReach");
                byte[] encoded=codec.Encode(s.Capture());Require(encoded.SequenceEqual(codec.Encode(codec.Decode(encoded))),"Schema50 receptacle state did not round-trip canonically.");
            });
            cases.Add("ordinary_receptacle_pick_shared_clock_restore_open_retrieve_and_independent_key",()=>{
                var p=OrdinaryPolicy(SuccessfulPickSeed(true));var s=World(p);
                FarmWork(s,CommandKind.PlantCrop);
                var pick=OrdinaryLockCommand(s,OrdinaryLockA,OrdinaryReceptacleInteraction.PickWithTools,"ordinary-pick-a");
                var query=p.QueryCommand(s.Capture(),host,pick);byte[] beforeQuery=Bytes(s);
                Require(query.Supported&&query.Admissible&&query.Costs.Any(x=>x.Kind=="action"&&x.Amount==1)
                    &&query.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==6)&&Bytes(s).SequenceEqual(beforeQuery),
                    "Pick preview omitted the staged Action/time cost or mutated the simulation.");
                OrdinaryCommit(s,pick);byte[] paid=Bytes(s);
                Require(s.Execute(host,pick).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(paid),"Duplicate pick repeated its cost.");
                WorldAdvance(s,3);var atThree=s;var pending=atThree.Capture();
                Require(pending.OrdinaryReceptacleAttempts.Single(x=>x.LockId==OrdinaryLockA).Status==OrdinaryReceptacleAttemptStatus.Working
                    &&pending.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent
                    &&Crop(atThree).Tasks.Single().Progress>default(RuleTime),"Pick did not retain paid staged labor while the companion's crop advanced.");
                string path=Path.Combine(directory,"ordinary-receptacle-pending.bin");new FileSaveStore().Save(path,pending);
                var restored=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                WorldAdvance(restored,3);var afterPick=restored.Capture();
                Require(!afterPick.OrdinaryReceptacleLocks.Single(x=>x.Id==OrdinaryLockA).Locked
                    &&afterPick.OrdinaryReceptacleLocks.Single(x=>x.Id==OrdinaryLockB).Locked
                    &&afterPick.OrdinaryReceptacleAttempts.Single(x=>x.LockId==OrdinaryLockA).Status==OrdinaryReceptacleAttemptStatus.Succeeded
                    &&afterPick.OrdinaryReceptacleAttempts.Single(x=>x.LockId==OrdinaryLockA).Natural>0
                    &&Crop(restored).Tasks.Single().Progress>Crop(atThree).Tasks.Single().Progress,
                    "Restored pick did not resolve once on its deadline while remote work continued; another lock changed.");
                byte[] afterCompletion=Bytes(restored);Require(restored.Execute(host,pick).Outcome==Outcome.Duplicate
                    &&Bytes(restored).SequenceEqual(afterCompletion),"Restored pick replay repeated its check or unlock.");
                OrdinaryCommit(restored,Portable(restored,CommandKind.OpenPortableContainer,OrdinaryContainerA));
                OrdinaryCommit(restored,Portable(restored,CommandKind.HandlePortableEquipment,OrdinaryRationA,handling:HandlingKind.Retrieve));
                var ration=restored.Capture();
                Require(ration.PortableEquipment.Single(x=>x.Id==OrdinaryRationA).ParentId==""
                    &&ration.PortableEquipment.Single(x=>x.Id==OrdinaryRationA).Placement==PortablePlacement.Carried
                    &&ration.Work.Lots.Single(x=>x.Id==OrdinaryRationA).LocationId==TestOnlyPolicy.ActorId
                    &&ration.InventoryLots.Single(x=>x.LotId==OrdinaryRationA).Access==InventoryAccess.Ready
                    &&ration.Work.Lots.Single(x=>x.Id==OrdinaryRationA).Amount==new RuleQuantity(2),
                    "Existing portable retrieval did not move the finite ration and its inventory access together.");
                var key=OrdinaryLockCommand(restored,OrdinaryLockB,OrdinaryReceptacleInteraction.UnlockWithKey,"ordinary-key-b");
                OrdinaryCommit(restored,key);WorldAdvance(restored,6);
                var afterKey=restored.Capture();
                Require(!afterKey.OrdinaryReceptacleLocks.Single(x=>x.Id==OrdinaryLockB).Locked
                    &&afterKey.OrdinaryReceptacleAttempts.Single(x=>x.LockId==OrdinaryLockB).Method==OrdinaryReceptacleMethod.Key
                    &&afterKey.OrdinaryReceptacleAttempts.Single(x=>x.LockId==OrdinaryLockB).Status==OrdinaryReceptacleAttemptStatus.Succeeded,
                    "The other lock did not use its distinct physical key through the same resolver.");
                OrdinaryCommit(restored,Portable(restored,CommandKind.OpenPortableContainer,OrdinaryContainerB));
                OrdinaryCommit(restored,Portable(restored,CommandKind.HandlePortableEquipment,OrdinaryRationB,handling:HandlingKind.Retrieve));
                Require(restored.Capture().Work.Lots.Single(x=>x.Id==OrdinaryRationB).LocationId==TestOnlyPolicy.ActorId,
                    "Second receptacle contents did not remain independently retrievable.");
            });
            cases.Add("ordinary_receptacle_interruption_retains_paid_time_and_claims_credential",()=>{
                var p=OrdinaryPolicy(SuccessfulPickSeed(true));var s=World(p);
                var pick=OrdinaryLockCommand(s,OrdinaryLockA,OrdinaryReceptacleInteraction.PickWithTools,"ordinary-interrupt-pick");
                OrdinaryCommit(s,pick);WorldAdvance(s,2);
                var tool=s.Capture().PortableEquipment.Single(x=>x.Id==OrdinaryReceptacleFixture.ToolsId);
                RejectUnchanged(s,host,Portable(s,CommandKind.HandlePortableEquipment,tool.Id,handling:HandlingKind.Drop),"WorkerBusy");
                OrdinaryCommit(s,OrdinaryLockCommand(s,OrdinaryLockA,OrdinaryReceptacleInteraction.Interrupt,"ordinary-interrupt"));
                var ended=s.Capture();var attempt=ended.OrdinaryReceptacleAttempts.Single();var labor=ended.Work.WorkerIntervals.Single(x=>x.JobId==attempt.Id);
                Require(attempt.Status==OrdinaryReceptacleAttemptStatus.Interrupted&&attempt.EndedAt==new RuleTime(2)
                    &&labor.End==new RuleTime(2)&&ended.OrdinaryReceptacleLocks.Single(x=>x.Id==OrdinaryLockA).Locked
                    &&ended.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Interrupted lock work kept progress, refunded the Action, or released the credential early.");
            });
        }
    }
}
#endif
