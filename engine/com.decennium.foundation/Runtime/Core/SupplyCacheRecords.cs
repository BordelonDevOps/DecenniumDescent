using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum SupplyCacheEquipmentKind { Key, ThievesTools }
    public enum SupplyCacheUnlockMethod { Key, ThievesTools }
    public enum SupplyCacheAttemptStatus { Working, Succeeded, Failed, Interrupted }

    /// <summary>Mutable state for one explicit test-only ordinary locked supply cache.</summary>
    public sealed class SupplyCacheRecord
    {
        public string Id { get; }
        public string OwnerId { get; }
        public int X { get; }
        public int Y { get; }
        public bool Locked { get; }
        public bool Open { get; }
        public bool ToolsProficient { get; }
        public string RationLotId { get; }
        public string WaterskinId { get; }
        public SupplyCacheRecord(string id,string ownerId,int x,int y,bool locked,bool open,bool toolsProficient,string rationLotId,string waterskinId)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(ownerId)||!Validation.ValidId(rationLotId)||!Validation.ValidId(waterskinId)
                ||x<0||y<0||locked&&open)throw new ArgumentException("Invalid supply cache state.");
            Id=id;OwnerId=ownerId;X=x;Y=y;Locked=locked;Open=open;ToolsProficient=toolsProficient;RationLotId=rationLotId;WaterskinId=waterskinId;
        }
        public SupplyCacheRecord With(bool? locked=null,bool? open=null)=>new SupplyCacheRecord(Id,OwnerId,X,Y,locked??Locked,open??Open,ToolsProficient,RationLotId,WaterskinId);
    }

    /// <summary>Actual fixture-held physical key or thieves' tools; no ownership or training is inferred.</summary>
    public sealed class SupplyCacheEquipmentRecord
    {
        public string Id { get; }
        public SupplyCacheEquipmentKind Kind { get; }
        public string OwnerId { get; }
        public string LocationId { get; }
        public string CustodianId { get; }
        public SupplyCacheEquipmentRecord(string id,SupplyCacheEquipmentKind kind,string ownerId,string locationId,string custodianId)
        {
            if(!Validation.ValidId(id)||!Enum.IsDefined(typeof(SupplyCacheEquipmentKind),kind)||!Validation.ValidId(ownerId)
                ||!Validation.ValidId(locationId)||!Validation.ValidId(custodianId))throw new ArgumentException("Invalid cache equipment.");
            Id=id;Kind=kind;OwnerId=ownerId;LocationId=locationId;CustodianId=custodianId;
        }
    }

    /// <summary>One staged unlock operation. A working attempt owns its full six-second labor interval.</summary>
    public sealed class SupplyCacheAttemptRecord
    {
        public string Id { get; }
        public string CacheId { get; }
        public string ActorId { get; }
        public string EquipmentId { get; }
        public SupplyCacheUnlockMethod Method { get; }
        public RuleTime StartedAt { get; }
        public RuleTime? EndedAt { get; }
        public SupplyCacheAttemptStatus Status { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public bool Tactical { get; }
        public bool AutomaticFailure { get; }
        public SupplyCacheAttemptRecord(string id,string cacheId,string actorId,string equipmentId,SupplyCacheUnlockMethod method,
            RuleTime startedAt,RuleTime? endedAt,SupplyCacheAttemptStatus status,int natural=0,int modifier=0,bool tactical=false,bool automaticFailure=false)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(cacheId)||!Validation.ValidId(actorId)||!Validation.ValidId(equipmentId)
                ||!Enum.IsDefined(typeof(SupplyCacheUnlockMethod),method)||!Enum.IsDefined(typeof(SupplyCacheAttemptStatus),status)
                ||(status==SupplyCacheAttemptStatus.Working)==endedAt.HasValue
                ||natural<0||natural>20||status==SupplyCacheAttemptStatus.Working&&natural!=0
                ||status==SupplyCacheAttemptStatus.Interrupted&&natural!=0
                ||automaticFailure&&(method!=SupplyCacheUnlockMethod.ThievesTools||status!=SupplyCacheAttemptStatus.Failed||natural!=0)
                ||method==SupplyCacheUnlockMethod.Key&&(natural!=0||automaticFailure)
                ||method==SupplyCacheUnlockMethod.ThievesTools&&(status==SupplyCacheAttemptStatus.Succeeded||status==SupplyCacheAttemptStatus.Failed)&&natural==0&&!automaticFailure)
                throw new ArgumentException("Invalid supply cache attempt.");
            Id=id;CacheId=cacheId;ActorId=actorId;EquipmentId=equipmentId;Method=method;StartedAt=startedAt;EndedAt=endedAt;
            Status=status;Natural=natural;Modifier=modifier;Tactical=tactical;AutomaticFailure=automaticFailure;
        }
    }

    public static class SupplyCacheValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.SupplyCaches==null||s.SupplyCacheAttempts==null||s.SupplyCacheEquipment==null
                ||s.SupplyCaches.Length>1||s.SupplyCacheAttempts.Length>128||s.SupplyCacheEquipment.Length>8
                ||s.SupplyCaches.Any(x=>x==null)||s.SupplyCacheAttempts.Any(x=>x==null)||s.SupplyCacheEquipment.Any(x=>x==null))
                throw new ArgumentException("Invalid supply cache collections.");
            if(s.SchemaVersion<Snapshot.SupplyCacheSchema) {
                if(s.SupplyCaches.Length!=0||s.SupplyCacheAttempts.Length!=0||s.SupplyCacheEquipment.Length!=0)
                    throw new ArgumentException("Supply cache state requires schema19.");
                return;
            }
            if(s.SupplyCaches.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SupplyCaches.Length
                ||s.SupplyCacheAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SupplyCacheAttempts.Length
                ||s.SupplyCacheEquipment.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SupplyCacheEquipment.Length)
                throw new ArgumentException("Duplicate supply cache identity.");
            if(s.SupplyCaches.Length==0&&(s.SupplyCacheAttempts.Length!=0||s.SupplyCacheEquipment.Length!=0))
                throw new ArgumentException("Cache events require an authored cache.");
            foreach(var cache in s.SupplyCaches) {
                var owner=s.Actors.SingleOrDefault(x=>x.Id==cache.OwnerId);
                var rations=s.InventoryLots.SingleOrDefault(x=>x.LotId==cache.RationLotId);
                var rationLot=s.Work.Lots.SingleOrDefault(x=>x.Id==cache.RationLotId);
                var vessel=s.Vessels.SingleOrDefault(x=>x.Id==cache.WaterskinId);
                if(owner==null||rations==null||rationLot==null||rations.ParentId!=""||rations.OwnerId!=cache.OwnerId
                    ||rations.Nutrition!=NutritionKind.FoodPounds||rationLot.UnitId!=TestOnlyCacheIds.RationUnit
                    ||vessel==null||vessel.Profile!=WaterVesselProfile.Waterskin||vessel.OwnerId!=cache.OwnerId
                    ||!s.VesselContents.Any(x=>x.VesselId==vessel.Id&&s.InventoryLots.Single(i=>i.LotId==x.LotId).Nutrition==NutritionKind.WaterPints))
                    throw new ArgumentException("Invalid cache stock references.");
                if(cache.Open&&cache.Locked)throw new ArgumentException("A locked cache cannot be open.");
            }
            foreach(var item in s.SupplyCacheEquipment) {
                var held=s.Actors.SingleOrDefault(x=>x.Id==item.LocationId);
                if(held==null||item.LocationId!=item.CustodianId||item.OwnerId!=item.CustodianId)
                    throw new ArgumentException("Cache credentials must remain with their recorded owner.");
            }
            if(s.SupplyCacheEquipment.Select(x=>x.Kind).Distinct().Count()!=s.SupplyCacheEquipment.Length)
                throw new ArgumentException("Duplicate cache credential profile.");
            foreach(var attempt in s.SupplyCacheAttempts) {
                var cache=s.SupplyCaches.SingleOrDefault(x=>x.Id==attempt.CacheId);
                var item=s.SupplyCacheEquipment.SingleOrDefault(x=>x.Id==attempt.EquipmentId);
                if(cache==null||item==null||!s.Actors.Any(x=>x.Id==attempt.ActorId)||attempt.StartedAt>s.RuleClock
                    ||attempt.EndedAt.HasValue&&(attempt.EndedAt.Value<attempt.StartedAt||attempt.EndedAt.Value>s.RuleClock)
                    ||attempt.Method==SupplyCacheUnlockMethod.Key&&item.Kind!=SupplyCacheEquipmentKind.Key
                    ||attempt.Method==SupplyCacheUnlockMethod.ThievesTools&&item.Kind!=SupplyCacheEquipmentKind.ThievesTools)
                    throw new ArgumentException("Invalid cache attempt references.");
                if(!attempt.Tactical) {
                    var interval=s.Work.WorkerIntervals.SingleOrDefault(x=>x.JobId==attempt.Id);
                    if(attempt.Status==SupplyCacheAttemptStatus.Working
                        ?interval==null||interval.WorkerId!=attempt.ActorId||interval.Start!=attempt.StartedAt||interval.End!=attempt.StartedAt.AddSeconds(6)
                        :attempt.EndedAt==attempt.StartedAt&&attempt.Status==SupplyCacheAttemptStatus.Interrupted
                            ?interval!=null
                            :interval==null||interval.WorkerId!=attempt.ActorId||interval.Start!=attempt.StartedAt
                                ||attempt.Status!=SupplyCacheAttemptStatus.Interrupted&&interval.End!=attempt.StartedAt.AddSeconds(6)
                                ||attempt.Status==SupplyCacheAttemptStatus.Interrupted&&interval.End!=attempt.EndedAt.Value)
                        throw new ArgumentException("Cache attempt labor does not match its outcome.");
                } else if(attempt.StartedAt!=attempt.EndedAt||attempt.Status==SupplyCacheAttemptStatus.Working)
                    throw new ArgumentException("Tactical lock operations resolve immediately.");
                if(attempt.Method==SupplyCacheUnlockMethod.Key&&attempt.Status!=SupplyCacheAttemptStatus.Working&&attempt.Status!=SupplyCacheAttemptStatus.Interrupted
                    &&attempt.Status!=SupplyCacheAttemptStatus.Succeeded)throw new ArgumentException("A key cannot fail an ordinary lock.");
            }
            if(s.SupplyCacheAttempts.Count(x=>x.Status==SupplyCacheAttemptStatus.Working)>1)
                throw new ArgumentException("Only one ordinary cache attempt may be active.");
        }
    }

    internal static class TestOnlyCacheIds
    {
        internal const string RationUnit="TEST_ONLY.ration-pound";
    }
}
