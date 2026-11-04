#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
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
        internal static bool IsCacheLocation(Snapshot s,string location)=>s.SupplyCaches.Any(x=>x.Id==location&&x.Open);
        internal static bool Accessible(Snapshot s,string actor,string location)
        {
            var cache=s.SupplyCaches.SingleOrDefault(x=>x.Id==location);
            if(cache==null||!cache.Open)return false;
            var body=s.Actors.SingleOrDefault(x=>x.Id==actor);
            return cache.OwnerId==actor&&body!=null&&Math.Abs((long)body.X-cache.X)+Math.Abs((long)body.Y-cache.Y)<=1;
        }
        public static int PickCheckModifier(ActorCharacterRecord character,bool proficient,LifeState life)
        {
            if(character==null||life==null)throw new ArgumentNullException(character==null?nameof(character):nameof(life));
            int modifier=PlaytestCharacters.AbilityModifier(character.Abilities[1]);
            if(proficient)modifier=checked(modifier+PlaytestCharacters.ProficiencyBonus(character.Levels.Count));
            return checked(modifier+PlaytestLife.AbilityCheckInjuryPenalty(life,1,toolCheck:true,manipulatesObject:true));
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
                :l.LotId==TestOnlyInventoryPolicy.WaterId
                    ?new InventoryLotRecord(l.LotId,l.ParentId,l.OwnerId,l.CreatedAmount,l.CreatedAt,l.Nutrition,l.FreshUntil,InventoryAccess.Ground):l).ToArray();
            s.Vessels=s.Vessels.Select(v=>v.Id==TestOnlyFillingPolicy.ActorSkinId
                ?new WaterVesselRecord(v.Id,v.Profile,v.OwnerId,id,actor):v).ToArray();
        }
        private bool IsSupplyCacheCommand(Command c)=>supplyCache!=null&&c.Kind==CommandKind.Interact&&c.Target==SupplyCacheFixture.CacheId;
        private static SupplyCacheRecord Cache(Snapshot s,string id)=>s.SupplyCaches.SingleOrDefault(x=>x.Id==id);
        private static void SetCache(Snapshot s,SupplyCacheRecord value)=>s.SupplyCaches=s.SupplyCaches.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetAttempt(Snapshot s,SupplyCacheAttemptRecord value)=>s.SupplyCacheAttempts=s.SupplyCacheAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static bool NearCache(Snapshot s,string actor,SupplyCacheRecord cache)
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
            var character=s.Characters.Single(x=>x.ActorId==attempt.ActorId);
            int modifier=SupplyCacheRules.PickCheckModifier(character,Cache(s,attempt.CacheId).ToolsProficient,
                ActorLifeRules.Read(s.Lives.Single(x=>x.ActorId==attempt.ActorId)));
            var conditions=View(s,attempt.ActorId);
            var roll=PlaytestDice.RollD20(s.RandomState,disadvantageSources:conditions.Has(ConditionKind.Poisoned)?1:0);
            int natural=roll.Natural;s.RandomState=roll.NextRandomState;
            bool success=PlaytestRolls.TaskCheck(natural,modifier,15).Success;
            RecordAttempt(s,attempt,success?SupplyCacheAttemptStatus.Succeeded:SupplyCacheAttemptStatus.Failed,natural,modifier);
            if(success)SetCache(s,Cache(s,attempt.CacheId).With(locked:false));
        }
        private string ResolveSupplyCache(Snapshot s,Command c)
        {
            if(c.Inventory!=null||c.Combat!=null||c.Target!=SupplyCacheFixture.CacheId||c.Y!=0)return "InvalidSupplyCacheInteraction";
            var cache=Cache(s,c.Target);if(cache==null)return "UnknownSupplyCache";
            if(c.Actor!=cache.OwnerId)return "NoSupplyCachePermission";
            if(!NearCache(s,c.Actor,cache))return "SupplyCacheOutOfReach";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            var operation=(SupplyCacheInteraction)c.X;
            if(!Enum.IsDefined(typeof(SupplyCacheInteraction),operation))return "InvalidSupplyCacheInteraction";
            if(operation==SupplyCacheInteraction.Interrupt) {
                var pending=s.SupplyCacheAttempts.SingleOrDefault(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.CacheId==cache.Id&&x.ActorId==c.Actor);
                if(pending==null)return "NoActiveSupplyCacheAttempt";
                InterruptSupplyCacheAttempt(s,pending);return null;
            }
            if(s.SupplyCacheAttempts.Any(x=>x.Status==SupplyCacheAttemptStatus.Working&&x.CacheId==cache.Id))return "SupplyCacheBusy";
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
                    var spent=interval.SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
                    SetCache(s,cache.With(open:true));return null;
                }
                RuleTime end=s.RuleClock.AddSeconds(1);
                var condition=NextConditionDeadline(s);if(condition.HasValue&&condition.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var formula=NextFormulaBoundary(s);if(formula.HasValue&&formula.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var dying=NextDyingMarker(s);if(dying.HasValue&&dying.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var remedy=NextRemedyBoundary(s);if(remedy.HasValue&&remedy.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var repairBoundary=NextRepairBoundary(s);if(repairBoundary.HasValue&&repairBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                AdvanceTo(s,end,initiating:c);SetCache(s,cache.With(open:true));return null;
            }
            if(operation!=SupplyCacheInteraction.UnlockWithKey&&operation!=SupplyCacheInteraction.PickWithTools)return "InvalidSupplyCacheInteraction";
            if(!cache.Locked)return "SupplyCacheAlreadyUnlocked";
            var method=operation==SupplyCacheInteraction.UnlockWithKey?SupplyCacheUnlockMethod.Key:SupplyCacheUnlockMethod.ThievesTools;
            if(!CredentialAvailable(s,c.Actor,method,out var equipment))return method==SupplyCacheUnlockMethod.Key?"PhysicalKeyUnavailable":"ActualThievesToolsRequired";
            var actionInterval=Interval(s,c.Actor);
            if(actionInterval.ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.InventoryCombat) {
                if(s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s))return "TacticalChoicePending";
                SetInterval(s,actionInterval.PayAction());
                var immediate=new SupplyCacheAttemptRecord(OrdinaryInventory.Identity(s,"cache-attempt"),cache.Id,c.Actor,equipment.Id,method,
                    s.RuleClock,s.RuleClock,SupplyCacheAttemptStatus.Interrupted,tactical:true);
                ResolveCacheAttempt(s,immediate);return null;
            }
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
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
