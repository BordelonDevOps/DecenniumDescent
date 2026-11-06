using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum OrdinaryReceptacleMethod { Key, ThievesTools }
    public enum OrdinaryReceptacleAttemptStatus { Working, Succeeded, Failed, Interrupted }

    /// <summary>Persistent lock state for one authored stationary portable receptacle.</summary>
    public sealed class OrdinaryReceptacleLockRecord
    {
        public string Id { get; }
        public string ContainerId { get; }
        public string OwnerId { get; }
        public string KeyItemId { get; }
        public string ToolsItemId { get; }
        public bool Locked { get; }

        public OrdinaryReceptacleLockRecord(string id,string containerId,string ownerId,string keyItemId,string toolsItemId,bool locked)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(containerId)||!Validation.ValidId(ownerId)
                ||keyItemId==null||(keyItemId!=""&&!Validation.ValidId(keyItemId))
                ||toolsItemId==null||(toolsItemId!=""&&!Validation.ValidId(toolsItemId))
                ||keyItemId==""&&toolsItemId=="")throw new ArgumentException("Invalid ordinary receptacle lock.");
            Id=id;ContainerId=containerId;OwnerId=ownerId;KeyItemId=keyItemId;ToolsItemId=toolsItemId;Locked=locked;
        }
        public OrdinaryReceptacleLockRecord With(bool? locked=null)
            =>new OrdinaryReceptacleLockRecord(Id,ContainerId,OwnerId,KeyItemId,ToolsItemId,locked??Locked);
    }

    /// <summary>Saved attempt history; the linked portable item remains the authoritative credential.</summary>
    public sealed class OrdinaryReceptacleAttemptRecord
    {
        public string Id { get; }
        public string LockId { get; }
        public string ActorId { get; }
        public string CredentialItemId { get; }
        public OrdinaryReceptacleMethod Method { get; }
        public RuleTime StartedAt { get; }
        public RuleTime? EndedAt { get; }
        public OrdinaryReceptacleAttemptStatus Status { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public bool Tactical { get; }
        public bool AutomaticFailure { get; }

        public OrdinaryReceptacleAttemptRecord(string id,string lockId,string actorId,string credentialItemId,
            OrdinaryReceptacleMethod method,RuleTime startedAt,RuleTime? endedAt,OrdinaryReceptacleAttemptStatus status,
            int natural=0,int modifier=0,bool tactical=false,bool automaticFailure=false)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(lockId)||!Validation.ValidId(actorId)||!Validation.ValidId(credentialItemId)
                ||!Enum.IsDefined(typeof(OrdinaryReceptacleMethod),method)||!Enum.IsDefined(typeof(OrdinaryReceptacleAttemptStatus),status)
                ||(status==OrdinaryReceptacleAttemptStatus.Working)==endedAt.HasValue||natural<0||natural>20
                ||status==OrdinaryReceptacleAttemptStatus.Working&&natural!=0
                ||status==OrdinaryReceptacleAttemptStatus.Interrupted&&natural!=0
                ||automaticFailure&&(method!=OrdinaryReceptacleMethod.ThievesTools||status!=OrdinaryReceptacleAttemptStatus.Failed||natural!=0)
                ||method==OrdinaryReceptacleMethod.Key&&(natural!=0||automaticFailure)
                ||method==OrdinaryReceptacleMethod.ThievesTools&&(status==OrdinaryReceptacleAttemptStatus.Succeeded
                    ||status==OrdinaryReceptacleAttemptStatus.Failed)&&natural==0&&!automaticFailure
                ||tactical&&(status==OrdinaryReceptacleAttemptStatus.Working||!endedAt.HasValue||startedAt!=endedAt.Value)
                ||!tactical&&status!=OrdinaryReceptacleAttemptStatus.Working&&endedAt.HasValue&&endedAt.Value==startedAt
                    &&status!=OrdinaryReceptacleAttemptStatus.Interrupted)
                throw new ArgumentException("Invalid ordinary receptacle attempt.");
            Id=id;LockId=lockId;ActorId=actorId;CredentialItemId=credentialItemId;Method=method;StartedAt=startedAt;EndedAt=endedAt;
            Status=status;Natural=natural;Modifier=modifier;Tactical=tactical;AutomaticFailure=automaticFailure;
        }
    }

    public static class OrdinaryReceptacleValidation
    {
        public const int MaxLocks=32,MaxAttempts=128;
        public static void Validate(Snapshot s)
        {
            if(s.OrdinaryReceptacleLocks==null||s.OrdinaryReceptacleAttempts==null
                ||s.OrdinaryReceptacleLocks.Length>MaxLocks||s.OrdinaryReceptacleAttempts.Length>MaxAttempts
                ||s.OrdinaryReceptacleLocks.Any(x=>x==null)||s.OrdinaryReceptacleAttempts.Any(x=>x==null))
                throw new ArgumentException("Invalid ordinary receptacle collections.");
            if(s.SchemaVersion<Snapshot.OrdinaryReceptacleSchema) {
                if(s.OrdinaryReceptacleLocks.Length!=0||s.OrdinaryReceptacleAttempts.Length!=0)
                    throw new ArgumentException("Ordinary receptacle state requires schema50.");
                return;
            }
            var locks=s.OrdinaryReceptacleLocks;var attempts=s.OrdinaryReceptacleAttempts;
            if(locks.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=locks.Length
                ||attempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=attempts.Length
                ||locks.Any(x=>s.Actors.Any(a=>a.Id==x.Id)||s.Objects.Any(o=>o.Id==x.Id)||s.PortableEquipment.Any(p=>p.Id==x.Id)))
                throw new ArgumentException("Duplicate ordinary receptacle identity.");
            foreach(var item in locks) {
                var container=s.PortableEquipment.SingleOrDefault(x=>x.Id==item.ContainerId);
                if(!s.Actors.Any(x=>x.Id==item.OwnerId)||container==null||container.OwnerId!=item.OwnerId
                    ||container.CustodianId!=item.OwnerId||container.Placement!=PortablePlacement.Ground||container.ParentId!=""
                    ||!container.CapacityPounds.HasValue||item.Locked&&container.Open)
                    throw new ArgumentException("Invalid stationary receptacle binding.");
                var key=s.PortableEquipment.SingleOrDefault(x=>x.Id==item.KeyItemId);
                if(item.KeyItemId!=""&&key!=null&&key.OwnerId!=item.OwnerId)
                    throw new ArgumentException("Ordinary receptacle key owner mismatch.");
                var tools=s.PortableEquipment.SingleOrDefault(x=>x.Id==item.ToolsItemId);
                if(item.ToolsItemId!=""&&(tools==null||tools.OwnerId!=item.OwnerId||tools.ProfileId!="tools.thieves-tools"))
                    throw new ArgumentException("Ordinary receptacle tools must be an authored physical item.");
            }
            if(attempts.GroupBy(x=>x.LockId,StringComparer.Ordinal).Any(g=>g.Count(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working)>1))
                throw new ArgumentException("A receptacle has multiple active unlock attempts.");
            foreach(var attempt in attempts) {
                var lockState=locks.SingleOrDefault(x=>x.Id==attempt.LockId);
                if(lockState==null||attempt.ActorId!=lockState.OwnerId||attempt.StartedAt>s.RuleClock
                    ||attempt.EndedAt.HasValue&&(attempt.EndedAt.Value<attempt.StartedAt||attempt.EndedAt.Value>s.RuleClock)
                    ||attempt.Method==OrdinaryReceptacleMethod.Key&&attempt.CredentialItemId!=lockState.KeyItemId
                    ||attempt.Method==OrdinaryReceptacleMethod.ThievesTools&&attempt.CredentialItemId!=lockState.ToolsItemId
                    ||attempt.Status==OrdinaryReceptacleAttemptStatus.Succeeded&&lockState.Locked
                    ||attempt.Status==OrdinaryReceptacleAttemptStatus.Working&&(!lockState.Locked
                        ||!s.PortableEquipment.Any(x=>x.Id==attempt.CredentialItemId)))
                    throw new ArgumentException("Invalid ordinary receptacle attempt references.");
                var interval=s.Work.WorkerIntervals.SingleOrDefault(x=>x.JobId==attempt.Id);
                if(attempt.Tactical) {
                    if(interval!=null)throw new ArgumentException("Tactical unlock cannot reserve exploration labor.");
                } else if(attempt.Status==OrdinaryReceptacleAttemptStatus.Working) {
                    if(interval==null||interval.WorkerId!=attempt.ActorId||interval.Start!=attempt.StartedAt
                        ||interval.End!=attempt.StartedAt.AddSeconds(6))throw new ArgumentException("Unlock labor interval mismatch.");
                } else if(attempt.Status==OrdinaryReceptacleAttemptStatus.Interrupted&&attempt.EndedAt.Value==attempt.StartedAt) {
                    if(interval!=null)throw new ArgumentException("Zero-time unlock interruption retained labor.");
                } else if(interval==null||interval.WorkerId!=attempt.ActorId||interval.Start!=attempt.StartedAt
                    ||attempt.Status!=OrdinaryReceptacleAttemptStatus.Interrupted&&interval.End!=attempt.StartedAt.AddSeconds(6)
                    ||attempt.Status==OrdinaryReceptacleAttemptStatus.Interrupted&&interval.End!=attempt.EndedAt.Value)
                    throw new ArgumentException("Unlock attempt labor does not match its outcome.");
            }
            if(attempts.Any(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                &&attempts.Any(y=>y.Id!=x.Id&&y.Status==OrdinaryReceptacleAttemptStatus.Working
                    &&(y.ActorId==x.ActorId||y.CredentialItemId==x.CredentialItemId))))
                throw new ArgumentException("Actor or physical credential has overlapping unlock attempts.");
        }
    }
}
