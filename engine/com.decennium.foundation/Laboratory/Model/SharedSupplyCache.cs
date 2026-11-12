#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One authored TEST_ONLY chest with finite existing ration and waterskin records.</summary>
    public sealed class SupplyCacheFixture
    {
        public const string CacheId="TEST_ONLY.supply-cache",KeyId="TEST_ONLY.cache-key",ToolsId="TEST_ONLY.thieves-tools";
        public const int CacheX=1,CacheY=2;
        public bool ToolsProficient { get; }
        public bool HasKey { get; }
        public bool HasTools { get; }
        public bool PickRequiresSight { get; }
        public SupplyCacheFixture(bool toolsProficient=true,bool hasKey=false,bool hasTools=true,bool pickRequiresSight=true)
        {ToolsProficient=toolsProficient;HasKey=hasKey;HasTools=hasTools;PickRequiresSight=pickRequiresSight;}
        internal string Key=>"ordinary-lock-dc15-six-active-seconds-open-one-second|key-mass-unrecorded|"+ToolsProficient+"|"+HasKey+"|"+HasTools+"|pick-requires-sight="+PickRequiresSight;
    }
    public enum SupplyCacheInteraction { UnlockWithKey=1,PickWithTools=2,Open=3,Interrupt=4 }
    public static class SupplyCacheRules
    {
        internal static bool Buried(Snapshot s,string cacheId)
            =>s.SchemaVersion>=Snapshot.BuriedCacheSchema&&s.BuriedCacheSites.Any(x=>x.CacheId==cacheId&&x.Buried);
        internal static bool IsCacheLocation(Snapshot s,string location)=>!Buried(s,location)&&s.SupplyCaches.Any(x=>x.Id==location&&x.Open);
        internal static bool Accessible(Snapshot s,string actor,string location)
        {
            var cache=s.SupplyCaches.SingleOrDefault(x=>x.Id==location);
            if(cache==null||Buried(s,location)||!cache.Open)return false;
            var body=s.Actors.SingleOrDefault(x=>x.Id==actor);
            return cache.OwnerId==actor&&body!=null&&Math.Abs((long)body.X-cache.X)+Math.Abs((long)body.Y-cache.Y)<=1;
        }
        public static int PickCheckModifier(CharacterStateFacts character,bool proficient)
        {
            var check=AbilityCheckRules.Derive(character.Character,CharacterAbility.Dexterity,proficient?1:0);
            return check.TotalWithInjury(character,toolCheck:true,manipulatesObject:true);
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static string SupplyCacheFingerprint(string prior,SupplyCacheFixture fixture)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.supply-cache-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+fixture.Key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private void InitializeSupplyCache(Snapshot s)
        {
            if(supplyCache==null)return;
            string id=SupplyCacheFixture.CacheId,actor=TestOnlyPolicy.ActorId;
            bool reserveStartsCarried = nextCharterPlanProfile?.ReserveWaterStartsCarried == true;
            s.SupplyCaches=new[]{new SupplyCacheRecord(id,actor,SupplyCacheFixture.CacheX,SupplyCacheFixture.CacheY,true,false,
                supplyCache.ToolsProficient,TestOnlyInventoryPolicy.FoodId,TestOnlyFillingPolicy.ActorSkinId)};
            s.SupplyCacheEquipment=(supplyCache.HasKey?new[]{new SupplyCacheEquipmentRecord(SupplyCacheFixture.KeyId,SupplyCacheEquipmentKind.Key,actor,actor,actor)}:Array.Empty<SupplyCacheEquipmentRecord>())
                .Concat(supplyCache.HasTools?new[]{new SupplyCacheEquipmentRecord(SupplyCacheFixture.ToolsId,SupplyCacheEquipmentKind.ThievesTools,actor,actor,actor)}:Array.Empty<SupplyCacheEquipmentRecord>()).ToArray();
            s.Work=new WorkLedger(s.Work.Lots.Select(l=>l.Id==TestOnlyInventoryPolicy.FoodId
                ?new ResourceLot(l.Id,l.UnitId,l.Amount,id,l.CustodianId)
                :l.Id==TestOnlyInventoryPolicy.WaterId
                    ?new ResourceLot(l.Id,l.UnitId,l.Amount,TestOnlyFillingPolicy.ActorSkinId,l.CustodianId):l),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Select(l=>l.LotId==TestOnlyInventoryPolicy.FoodId
                ?new InventoryLotRecord(l.LotId,l.ParentId,l.OwnerId,l.CreatedAmount,l.CreatedAt,l.Nutrition,l.FreshUntil,InventoryAccess.Ground)
                :l.LotId==TestOnlyInventoryPolicy.WaterId && !reserveStartsCarried
                    ?new InventoryLotRecord(l.LotId,l.ParentId,l.OwnerId,l.CreatedAmount,l.CreatedAt,l.Nutrition,l.FreshUntil,InventoryAccess.Ground):l).ToArray();
            if (!reserveStartsCarried) s.Vessels=s.Vessels.Select(v=>v.Id==TestOnlyFillingPolicy.ActorSkinId
                ?new WaterVesselRecord(v.Id,v.Profile,v.OwnerId,id,actor):v).ToArray();
        }
        private bool IsSupplyCacheCommand(Command c)=>supplyCache!=null&&c.Kind==CommandKind.Interact&&c.Target==SupplyCacheFixture.CacheId;
        private static SupplyCacheRecord Cache(Snapshot s,string id)=>s.SupplyCaches.SingleOrDefault(x=>x.Id==id);
        private static void SetCache(Snapshot s,SupplyCacheRecord value)=>s.SupplyCaches=s.SupplyCaches.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetAttempt(Snapshot s,SupplyCacheAttemptRecord value)=>s.SupplyCacheAttempts=s.SupplyCacheAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
        internal static bool NearCache(Snapshot s,string actor,SupplyCacheRecord cache)
        {var a=s.Actors.Single(x=>x.Id==actor);return Math.Abs((long)a.X-cache.X)+Math.Abs((long)a.Y-cache.Y)<=1;}
        private bool CredentialAvailable(Snapshot s,string actor,SupplyCacheUnlockMethod method,out SupplyCacheEquipmentRecord item)
        {
            var kind=method==SupplyCacheUnlockMethod.Key?SupplyCacheEquipmentKind.Key:SupplyCacheEquipmentKind.ThievesTools;
            item=s.SupplyCacheEquipment.SingleOrDefault(x=>x.Kind==kind&&x.OwnerId==actor&&x.LocationId==actor&&x.CustodianId==actor);
            return item!=null;
        }
        private bool CanContinueCacheAttempt(Snapshot s,SupplyCacheAttemptRecord attempt)
        {
            var cache=Cache(s,attempt.CacheId);
            return cache!=null&&cache.Locked&&!cache.Open&&attempt.ActorId==cache.OwnerId&&NearCache(s,attempt.ActorId,cache)
                &&CapableWorker(s,attempt.ActorId)&&AvailableHands(s,attempt.ActorId)>0
                &&s.SupplyCacheEquipment.Any(x=>x.Id==attempt.EquipmentId&&x.OwnerId==attempt.ActorId&&x.LocationId==attempt.ActorId&&x.CustodianId==attempt.ActorId);
        }
        private static void RecordAttempt(Snapshot s,SupplyCacheAttemptRecord prior,SupplyCacheAttemptStatus status,int natural,int modifier,bool automaticFailure=false)
        {
            var ended=new SupplyCacheAttemptRecord(prior.Id,prior.CacheId,prior.ActorId,prior.EquipmentId,prior.Method,prior.StartedAt,s.RuleClock,status,natural,modifier,prior.Tactical,automaticFailure);
            if(prior.Status==SupplyCacheAttemptStatus.Working)SetAttempt(s,ended);else s.SupplyCacheAttempts=s.SupplyCacheAttempts.Concat(new[]{ended}).ToArray();
        }
        private void ResolveCacheAttempt(Snapshot s,SupplyCacheAttemptRecord attempt)
        {
            if(!CanContinueCacheAttempt(s,attempt)){RecordAttempt(s,attempt,SupplyCacheAttemptStatus.Interrupted,0,0);return;}
            if(attempt.Method==SupplyCacheUnlockMethod.Key) {
                RecordAttempt(s,attempt,SupplyCacheAttemptStatus.Succeeded,0,0);SetCache(s,Cache(s,attempt.CacheId).With(locked:false));return;
            }
            if(supplyCache.PickRequiresSight&&View(s,attempt.ActorId).BlocksSight) {
                RecordAttempt(s,attempt,SupplyCacheAttemptStatus.Failed,0,0,automaticFailure:true);return;
            }
            var character=CharacterStateFacts.ForActor(s,attempt.ActorId);
            int modifier=SupplyCacheRules.PickCheckModifier(character,Cache(s,attempt.CacheId).ToolsProficient);
            var conditions=View(s,attempt.ActorId);
            var roll=PlaytestDice.RollD20(s.RandomState,disadvantageSources:conditions.Has(ConditionKind.Poisoned)?1:0);
            int natural=roll.Natural;s.RandomState=roll.NextRandomState;
            bool success=PlaytestRolls.TaskCheck(natural,modifier,15).Success;
            RecordAttempt(s,attempt,success?SupplyCacheAttemptStatus.Succeeded:SupplyCacheAttemptStatus.Failed,natural,modifier);
            if(success)SetCache(s,Cache(s,attempt.CacheId).With(locked:false));
        }
        private string AssessSupplyCacheCommand(Snapshot s,Command c,out SupplyCacheRecord cache,
            out SupplyCacheUnlockMethod method,out SupplyCacheEquipmentRecord equipment)
        {
            cache=null;method=default(SupplyCacheUnlockMethod);equipment=null;
            if(c.Inventory!=null||c.Combat!=null||c.Target!=SupplyCacheFixture.CacheId||c.Y!=0)return "InvalidSupplyCacheInteraction";
            cache=Cache(s,c.Target);if(cache==null)return "UnknownSupplyCache";
            if(SupplyCacheRules.Buried(s,cache.Id))return "SupplyCacheBuried";
            string cacheId=cache.Id;
            if(c.Actor!=cache.OwnerId)return "NoSupplyCachePermission";
            if(!NearCache(s,c.Actor,cache))return "SupplyCacheOutOfReach";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            var operation=(SupplyCacheInteraction)c.X;
            if(!Enum.IsDefined(typeof(SupplyCacheInteraction),operation))return "InvalidSupplyCacheInteraction";
            if(operation==SupplyCacheInteraction.Interrupt) {
                var pending=s.SupplyCacheAttempts.SingleOrDefault(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.CacheId==cacheId&&x.ActorId==c.Actor);
                return pending==null?"NoActiveSupplyCacheAttempt":null;
            }
            if(s.SupplyCacheAttempts.Any(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.CacheId==cacheId))return "SupplyCacheBusy";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
            if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
            if(operation==SupplyCacheInteraction.Open) {
                if(cache.Locked)return "SupplyCacheLocked";
                if(cache.Open)return "SupplyCacheAlreadyOpen";
                if(s.InventoryCombat) {
                    if(s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s))return "TacticalChoicePending";
                    var interval=Interval(s,c.Actor);
                    if(s.InventoryInteractions!=interval.Interactions)return "TacticalInteractionLedgerMismatch";
                    if(interval.Interactions>=2)return "InteractionBudgetUnavailable";
                    if(interval.Interactions==1&&interval.ActionSpent)return "ActionAlreadySpent";
                    if(interval.Interactions==1&&!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
                    return null;
                }
                RuleTime end=s.RuleClock.AddSeconds(1);
                var condition=NextConditionDeadline(s);if(condition.HasValue&&condition.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var formula=NextFormulaBoundary(s);if(formula.HasValue&&formula.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var dying=NextDyingMarker(s);if(dying.HasValue&&dying.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var remedy=NextRemedyBoundary(s);if(remedy.HasValue&&remedy.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var repairBoundary=NextRepairBoundary(s);if(repairBoundary.HasValue&&repairBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                return null;
            }
            if(operation!=SupplyCacheInteraction.UnlockWithKey&&operation!=SupplyCacheInteraction.PickWithTools)return "InvalidSupplyCacheInteraction";
            if(!cache.Locked)return "SupplyCacheAlreadyUnlocked";
            method=operation==SupplyCacheInteraction.UnlockWithKey?SupplyCacheUnlockMethod.Key:SupplyCacheUnlockMethod.ThievesTools;
            if(!CredentialAvailable(s,c.Actor,method,out equipment))return method==SupplyCacheUnlockMethod.Key?"PhysicalKeyUnavailable":"ActualThievesToolsRequired";
            var actionInterval=Interval(s,c.Actor);
            if(actionInterval.ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.InventoryCombat) {
                if(s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s))return "TacticalChoicePending";
                return null;
            }
            return OrdinaryInventory.Busy(s,c.Actor)?"WorkerBusy":null;
        }
        private CommandQueryResult QuerySupplyCacheCommand(Snapshot s,Command c)
        {
            if(!IsSupplyCacheCommand(c))return new CommandQueryResult(false,false,"UnsupportedOperation",s.Revision);
            string failure=AssessSupplyCacheCommand(s,c,out _,out _,out _);
            var costs=new System.Collections.Generic.List<CommandCost>();
            if(failure==null) {
                var operation=(SupplyCacheInteraction)c.X;
                if(operation==SupplyCacheInteraction.Open) {
                    if(s.InventoryCombat) {
                        var interval=Interval(s,c.Actor);
                        costs.Add(new CommandCost(interval.Interactions==0?"ordinary-interaction":"action","",1));
                    } else costs.Add(new CommandCost("work-seconds","",1));
                } else if(operation!=SupplyCacheInteraction.Interrupt) {
                    costs.Add(new CommandCost("action","",1));
                    if(!s.InventoryCombat)costs.Add(new CommandCost("work-seconds","",6));
                }
            }
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
        }
        private IEnumerable<Command> DiscoverSupplyCacheCommands(Snapshot s,string actor)
        {
            int index=0;
            if(supplyCache==null)yield break;
            foreach(var cache in s.SupplyCaches.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                if(SupplyCacheRules.Buried(s,cache.Id))continue;
                if(cache.OwnerId!=actor||!NearCache(s,actor,cache))continue;
                var working=s.SupplyCacheAttempts.SingleOrDefault(x=>x.Status==SupplyCacheAttemptStatus.Working
                    &&x.CacheId==cache.Id&&x.ActorId==actor);
                if(working!=null) {
                    yield return SupplyCacheOption(s,actor,cache.Id,SupplyCacheInteraction.Interrupt,index++);
                    continue;
                }
                if(cache.Locked) {
                    if(CredentialAvailable(s,actor,SupplyCacheUnlockMethod.Key,out _))
                        yield return SupplyCacheOption(s,actor,cache.Id,SupplyCacheInteraction.UnlockWithKey,index++);
                    if(CredentialAvailable(s,actor,SupplyCacheUnlockMethod.ThievesTools,out _))
                        yield return SupplyCacheOption(s,actor,cache.Id,SupplyCacheInteraction.PickWithTools,index++);
                } else if(!cache.Open)
                    yield return SupplyCacheOption(s,actor,cache.Id,SupplyCacheInteraction.Open,index++);
            }
        }
        private static Command SupplyCacheOption(Snapshot s,string actor,string cacheId,SupplyCacheInteraction operation,int index)
            =>new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".supply-cache."+index.ToString(CultureInfo.InvariantCulture),
                actor,s.Revision,CommandKind.Interact,cacheId,(int)operation);
        private string ResolveSupplyCache(Snapshot s,Command c)
        {
            string failure=AssessSupplyCacheCommand(s,c,out var cache,out var method,out var equipment);
            if(failure!=null)return failure;
            var operation=(SupplyCacheInteraction)c.X;
            if(operation==SupplyCacheInteraction.Interrupt) {
                var pending=s.SupplyCacheAttempts.Single(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.CacheId==cache.Id&&x.ActorId==c.Actor);
                InterruptSupplyCacheAttempt(s,pending);return null;
            }
            if(operation==SupplyCacheInteraction.Open) {
                if(s.InventoryCombat) {
                    var interval=Interval(s,c.Actor);var spent=interval.SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
                    SetCache(s,cache.With(open:true));return null;
                }
                string timeFailure=AdvanceTo(s,s.RuleClock.AddSeconds(1),initiating:c);if(timeFailure!=null)return timeFailure;
                SetCache(s,cache.With(open:true));return null;
            }
            var actionInterval=Interval(s,c.Actor);
            if(s.InventoryCombat) {
                SetInterval(s,actionInterval.PayAction());
                var immediate=new SupplyCacheAttemptRecord(OrdinaryInventory.Identity(s,"cache-attempt"),cache.Id,c.Actor,equipment.Id,method,
                    s.RuleClock,s.RuleClock,SupplyCacheAttemptStatus.Interrupted,tactical:true);
                ResolveCacheAttempt(s,immediate);return null;
            }
            string id=OrdinaryInventory.Identity(s,"cache-attempt");RuleTime start=s.RuleClock,endAttempt=start.AddSeconds(6);
            SetInterval(s,actionInterval.PayAction());
            s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,start,endAttempt)},Array.Empty<ResourceReservation>());
            s.SupplyCacheAttempts=s.SupplyCacheAttempts.Concat(new[]{new SupplyCacheAttemptRecord(id,cache.Id,c.Actor,equipment.Id,method,start,null,SupplyCacheAttemptStatus.Working)}).ToArray();
            return null;
        }
        private static RuleTime? NextSupplyCacheBoundary(Snapshot s)
        {var due=s.SupplyCacheAttempts.Where(x=>x.Status==SupplyCacheAttemptStatus.Working).Select(x=>x.StartedAt.AddSeconds(6)).ToArray();return due.Length==0?(RuleTime?)null:due.Min();}
        private void CompleteSupplyCacheAttempts(Snapshot s)
        {foreach(var attempt in s.SupplyCacheAttempts.Where(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.StartedAt.AddSeconds(6)==s.RuleClock).ToArray())ResolveCacheAttempt(s,attempt);}
        private void InterruptSupplyCacheAttempts(Snapshot s)
        {foreach(var attempt in s.SupplyCacheAttempts.Where(x=>x.Status==SupplyCacheAttemptStatus.Working&&!CanContinueCacheAttempt(s,x)).ToArray())InterruptSupplyCacheAttempt(s,attempt);}
        private static void InterruptSupplyCacheAttempt(Snapshot s,SupplyCacheAttemptRecord attempt)
        {
            if(attempt.Status!=SupplyCacheAttemptStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            SetAttempt(s,new SupplyCacheAttemptRecord(attempt.Id,attempt.CacheId,attempt.ActorId,attempt.EquipmentId,attempt.Method,
                attempt.StartedAt,s.RuleClock,SupplyCacheAttemptStatus.Interrupted));
        }
    }
}
#endif
