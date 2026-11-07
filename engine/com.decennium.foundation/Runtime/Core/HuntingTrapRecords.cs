using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum HuntingTrapDeploymentStatus { Armed, Sprung }
    public enum HuntingTrapActionKind { Set, Reset, Free }
    public enum HuntingTrapActionStatus { Working, Succeeded, Failed, Interrupted }
    public enum HuntingTrapTriggerStatus { Pending, Resolved }
    public enum HuntingTrapEntryKind { ExplorationStep, TacticalStep, ForcedTacticalStep, RouteTravelCheckpoint }
    public enum HuntingTrapTetherStatus { Active, Released }

    /// <summary>One actual authored deployment of a physical hunting-trap item.</summary>
    public sealed class HuntingTrapDeploymentRecord
    {
        public string Id { get; }
        public string TrapItemId { get; }
        public string SetterId { get; }
        public int AnchorX { get; }
        public int AnchorY { get; }
        public long ArmedRevision { get; }
        public RuleTime ArmedAt { get; }
        public HuntingTrapDeploymentStatus Status { get; }
        public string TriggerId { get; }

        public HuntingTrapDeploymentRecord(string id,string item,string setter,int x,int y,long revision,RuleTime at,
            HuntingTrapDeploymentStatus status=HuntingTrapDeploymentStatus.Armed,string triggerId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(item)||!Validation.ValidId(setter)||x<0||y<0||revision<1
                ||!Enum.IsDefined(typeof(HuntingTrapDeploymentStatus),status)||triggerId==null
                ||(triggerId!=""&&!Validation.ValidId(triggerId))||(status==HuntingTrapDeploymentStatus.Armed)!=(triggerId==""))
                throw new ArgumentException("Invalid hunting-trap deployment.");
            Id=id;TrapItemId=item;SetterId=setter;AnchorX=x;AnchorY=y;ArmedRevision=revision;ArmedAt=at;Status=status;TriggerId=triggerId;
        }
        public HuntingTrapDeploymentRecord Sprung(string triggerId)
            =>new HuntingTrapDeploymentRecord(Id,TrapItemId,SetterId,AnchorX,AnchorY,ArmedRevision,ArmedAt,HuntingTrapDeploymentStatus.Sprung,triggerId);
    }

    /// <summary>Persistent set/reset/free action work and exact STR-check evidence.</summary>
    public sealed class HuntingTrapActionRecord
    {
        public string Id { get; }
        public HuntingTrapActionKind Kind { get; }
        public string ActorId { get; }
        public string TrapItemId { get; }
        public string TargetActorId { get; }
        public string DeploymentId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime? EndedAt { get; }
        public HuntingTrapActionStatus Status { get; }
        public bool Tactical { get; }
        public bool AutomaticFailure { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public int Dc { get; }
        public long Total { get; }
        public bool CheckSuccess { get; }
        public int Damage { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public HuntingTrapActionRecord(string id,HuntingTrapActionKind kind,string actor,string trap,string target,string deployment,
            RuleTime started,RuleTime? ended,HuntingTrapActionStatus status,bool tactical=false,bool automaticFailure=false,
            int natural=0,int modifier=0,int dc=0,long total=0,bool checkSuccess=false,int damage=0,
            uint randomBefore=1,uint randomAfter=1,long wordsConsumed=0)
        {
            if(!Validation.ValidId(id)||!Enum.IsDefined(typeof(HuntingTrapActionKind),kind)||!Validation.ValidId(actor)
                ||trap==null||(trap!=""&&!Validation.ValidId(trap))||target==null||(target!=""&&!Validation.ValidId(target))
                ||deployment==null||(deployment!=""&&!Validation.ValidId(deployment))||!Enum.IsDefined(typeof(HuntingTrapActionStatus),status)
                ||(status==HuntingTrapActionStatus.Working)==ended.HasValue||natural<0||natural>20||dc<0||modifier< -100||modifier>100
                ||damage<0||randomBefore==0||randomAfter==0||wordsConsumed<0
                ||kind==HuntingTrapActionKind.Free&&(trap==""||target==""||deployment=="")
                ||kind!=HuntingTrapActionKind.Free&&(trap==""||target!="")
                ||automaticFailure&&(kind!=HuntingTrapActionKind.Free||status!=HuntingTrapActionStatus.Failed||natural!=0)
                ||kind!=HuntingTrapActionKind.Free&&(natural!=0||modifier!=0||dc!=0||total!=0||checkSuccess||damage!=0||wordsConsumed!=0
                    ||randomBefore!=randomAfter)
                ||kind==HuntingTrapActionKind.Free&&status==HuntingTrapActionStatus.Working&&(natural!=0||damage!=0||automaticFailure||wordsConsumed!=0)
                ||kind==HuntingTrapActionKind.Free&&status==HuntingTrapActionStatus.Interrupted&&(natural!=0||damage!=0||automaticFailure||wordsConsumed!=0)
                ||kind==HuntingTrapActionKind.Free&&status==HuntingTrapActionStatus.Succeeded&&(automaticFailure||natural==0||!checkSuccess||damage!=0)
                ||kind==HuntingTrapActionKind.Free&&status==HuntingTrapActionStatus.Failed
                    &&(checkSuccess||!automaticFailure&&natural==0||damage<1||damage>1)
                ||tactical&&status!=HuntingTrapActionStatus.Working&&(!ended.HasValue||ended.Value!=started)
                ||!tactical&&status!=HuntingTrapActionStatus.Working&&ended.HasValue&&ended.Value==started
                    &&status!=HuntingTrapActionStatus.Interrupted)
                throw new ArgumentException("Invalid hunting-trap action.");
            Id=id;Kind=kind;ActorId=actor;TrapItemId=trap;TargetActorId=target;DeploymentId=deployment;StartedAt=started;EndedAt=ended;
            Status=status;Tactical=tactical;AutomaticFailure=automaticFailure;Natural=natural;Modifier=modifier;Dc=dc;Total=total;
            CheckSuccess=checkSuccess;Damage=damage;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
        }
        public HuntingTrapActionRecord Resolve(RuleTime at,HuntingTrapActionStatus status,string deployment="",bool automaticFailure=false,
            int natural=0,int modifier=0,int dc=0,long total=0,bool success=false,int damage=0,uint before=1,uint after=1,long words=0)
            =>new HuntingTrapActionRecord(Id,Kind,ActorId,TrapItemId,TargetActorId,deployment==""?DeploymentId:deployment,
                StartedAt,at,status,Tactical,automaticFailure,natural,modifier,dc,total,success,damage,before,after,words);
        public HuntingTrapActionRecord Interrupt(RuleTime at)
            =>new HuntingTrapActionRecord(Id,Kind,ActorId,TrapItemId,TargetActorId,DeploymentId,StartedAt,at,
                HuntingTrapActionStatus.Interrupted,Tactical);
    }

    /// <summary>Exactly-once first-entry result. A pending record owns the deployment before any save is rolled.</summary>
    public sealed class HuntingTrapTriggerRecord
    {
        public string Id { get; }
        public string DeploymentId { get; }
        public string EntryId { get; }
        public HuntingTrapEntryKind EntryKind { get; }
        public string RouteId { get; }
        public long RouteStartedRevision { get; }
        public RuleQuantity RouteProgress { get; }
        public string EntrantId { get; }
        public long CreatedRevision { get; }
        public long ResolvedRevision { get; }
        public long SourceAppliedRevision { get; }
        public RuleTime At { get; }
        public HuntingTrapTriggerStatus Status { get; }
        public bool AutomaticFailure { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public int Dc { get; }
        public long Total { get; }
        public bool SaveSuccess { get; }
        public int DamageRoll { get; }
        public long DamageApplied { get; }
        public string TetherId { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public HuntingTrapTriggerRecord(string id,string deployment,string entry,HuntingTrapEntryKind entryKind,string entrant,
            long created,long resolved,long sourceRevision,RuleTime at,HuntingTrapTriggerStatus status,bool automaticFailure=false,
            int natural=0,int modifier=0,int dc=13,long total=0,bool success=false,int damageRoll=0,long damageApplied=0,
            string tetherId="",uint randomBefore=1,uint randomAfter=1,long words=0,string routeId="",
            long routeStartedRevision=0,RuleQuantity routeProgress=default(RuleQuantity))
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(deployment)||!Validation.ValidId(entry)||!Enum.IsDefined(typeof(HuntingTrapEntryKind),entryKind)
                ||!Validation.ValidId(entrant)||created<1||resolved<0||resolved!=0&&resolved<created||sourceRevision<1||sourceRevision>created
                ||routeId==null||(routeId!=""&&!Validation.ValidId(routeId))||routeStartedRevision<0
                ||(entryKind==HuntingTrapEntryKind.RouteTravelCheckpoint
                    ?routeId==""||routeStartedRevision<1||routeStartedRevision>=created||routeProgress<default(RuleQuantity)
                    :routeId!=""||routeStartedRevision!=0||routeProgress!=default(RuleQuantity))
                ||!Enum.IsDefined(typeof(HuntingTrapTriggerStatus),status)||(status==HuntingTrapTriggerStatus.Pending)!=(resolved==0)
                ||natural<0||natural>20||modifier< -100||modifier>100||dc!=13||damageRoll<0||damageRoll>4||damageApplied<0
                ||tetherId==null||(tetherId!=""&&!Validation.ValidId(tetherId))||randomBefore==0||randomAfter==0||words<0
                ||status==HuntingTrapTriggerStatus.Pending&&(automaticFailure||natural!=0||modifier!=0||total!=0||success||damageRoll!=0
                    ||damageApplied!=0||tetherId!=""||randomBefore!=randomAfter||words!=0)
                ||status==HuntingTrapTriggerStatus.Resolved&&(automaticFailure?natural!=0:natural==0)
                ||status==HuntingTrapTriggerStatus.Resolved&&success&&(damageRoll!=0||damageApplied!=0||tetherId!="")
                ||status==HuntingTrapTriggerStatus.Resolved&&!success&&(damageRoll<1||tetherId==""))
                throw new ArgumentException("Invalid hunting-trap trigger.");
            Id=id;DeploymentId=deployment;EntryId=entry;EntryKind=entryKind;RouteId=routeId;
            RouteStartedRevision=routeStartedRevision;RouteProgress=routeProgress;EntrantId=entrant;CreatedRevision=created;
            ResolvedRevision=resolved;SourceAppliedRevision=sourceRevision;At=at;Status=status;AutomaticFailure=automaticFailure;
            Natural=natural;Modifier=modifier;Dc=dc;Total=total;SaveSuccess=success;DamageRoll=damageRoll;DamageApplied=damageApplied;
            TetherId=tetherId;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=words;
        }
        public HuntingTrapTriggerRecord Resolve(long revision,bool automaticFailure,int natural,int modifier,long total,bool success,
            int damageRoll,long damageApplied,string tether,uint before,uint after,long words)
            =>new HuntingTrapTriggerRecord(Id,DeploymentId,EntryId,EntryKind,EntrantId,CreatedRevision,revision,SourceAppliedRevision,At,
                HuntingTrapTriggerStatus.Resolved,automaticFailure,natural,modifier,13,total,success,damageRoll,damageApplied,tether,before,after,words,
                RouteId,RouteStartedRevision,RouteProgress);
    }

    /// <summary>The exact source tether; it is not the Restrained condition and does not change action access.</summary>
    public sealed class HuntingTrapTetherRecord
    {
        public string Id { get; }
        public string TriggerId { get; }
        public string DeploymentId { get; }
        public string TrapItemId { get; }
        public string ActorId { get; }
        public int AnchorX { get; }
        public int AnchorY { get; }
        public int MaximumDistanceFeet { get; }
        public HuntingTrapTetherStatus Status { get; }
        public long ReleasedRevision { get; }
        public string ReleaseActionId { get; }
        public HuntingTrapTetherRecord(string id,string trigger,string deployment,string trap,string actor,int x,int y,
            HuntingTrapTetherStatus status=HuntingTrapTetherStatus.Active,long released=0,string releaseAction="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(trigger)||!Validation.ValidId(deployment)||!Validation.ValidId(trap)
                ||!Validation.ValidId(actor)||x<0||y<0||!Enum.IsDefined(typeof(HuntingTrapTetherStatus),status)||released<0
                ||releaseAction==null||(releaseAction!=""&&!Validation.ValidId(releaseAction))
                ||(status==HuntingTrapTetherStatus.Active)!=(released==0)||(status==HuntingTrapTetherStatus.Active)!=(releaseAction==""))
                throw new ArgumentException("Invalid hunting-trap tether.");
            Id=id;TriggerId=trigger;DeploymentId=deployment;TrapItemId=trap;ActorId=actor;AnchorX=x;AnchorY=y;
            MaximumDistanceFeet=3;Status=status;ReleasedRevision=released;ReleaseActionId=releaseAction;
        }
        public HuntingTrapTetherRecord Release(long revision,string action)
            =>new HuntingTrapTetherRecord(Id,TriggerId,DeploymentId,TrapItemId,ActorId,AnchorX,AnchorY,
                HuntingTrapTetherStatus.Released,revision,action);
    }

    public static class HuntingTrapValidation
    {
        public const int MaxDeployments=128,MaxActions=256,MaxTriggers=256,MaxTethers=256;
        public static bool CanReserveEntries(Snapshot s,int additionalEntries=1)
        {
            if(s?.HuntingTrapTriggers==null||s.HuntingTrapTethers==null||additionalEntries<0)return false;
            int pending=s.HuntingTrapTriggers.Count(x=>x!=null&&x.Status==HuntingTrapTriggerStatus.Pending);
            return s.HuntingTrapTriggers.Length<=MaxTriggers-additionalEntries
                &&s.HuntingTrapTethers.Length<=MaxTethers-pending-additionalEntries;
        }
        public static bool HasActiveTether(Snapshot s,string actor)
            =>s?.HuntingTrapTethers?.Any(x=>x.ActorId==actor&&x.Status==HuntingTrapTetherStatus.Active)==true;
        public static bool BlocksGridMove(Snapshot s,string actor,int x,int y)
        {
            var tether=s?.HuntingTrapTethers?.SingleOrDefault(t=>t.ActorId==actor&&t.Status==HuntingTrapTetherStatus.Active);
            return tether!=null&&(x!=tether.AnchorX||y!=tether.AnchorY);
        }
        public static void Validate(Snapshot s)
        {
            if(s.HuntingTrapDeployments==null||s.HuntingTrapActions==null||s.HuntingTrapTriggers==null||s.HuntingTrapTethers==null
                ||s.HuntingTrapDeployments.Length>MaxDeployments||s.HuntingTrapActions.Length>MaxActions
                ||s.HuntingTrapTriggers.Length>MaxTriggers||s.HuntingTrapTethers.Length>MaxTethers
                ||s.HuntingTrapDeployments.Any(x=>x==null)||s.HuntingTrapActions.Any(x=>x==null)
                ||s.HuntingTrapTriggers.Any(x=>x==null)||s.HuntingTrapTethers.Any(x=>x==null))
                throw new ArgumentException("Invalid hunting-trap collections.");
            if(!CanReserveEntries(s,0)||s.HuntingTrapTethers.Length>s.HuntingTrapTriggers.Length)
                throw new ArgumentException("Hunting-trap trigger and tether capacity reservations are inconsistent.");
            if(s.SchemaVersion<Snapshot.HuntingTrapSchema) {
                if(s.HuntingTrapDeployments.Length+s.HuntingTrapActions.Length+s.HuntingTrapTriggers.Length+s.HuntingTrapTethers.Length!=0)
                    throw new ArgumentException("Hunting traps require schema55.");
                return;
            }
            var deployments=s.HuntingTrapDeployments;var actions=s.HuntingTrapActions;var triggers=s.HuntingTrapTriggers;var tethers=s.HuntingTrapTethers;
            if(deployments.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=deployments.Length
                ||actions.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=actions.Length
                ||triggers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=triggers.Length
                ||tethers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=tethers.Length
                ||deployments.Where(x=>x.Status==HuntingTrapDeploymentStatus.Armed).GroupBy(x=>x.TrapItemId,StringComparer.Ordinal).Any(x=>x.Count()>1)
                ||deployments.Where(x=>x.Status==HuntingTrapDeploymentStatus.Armed).GroupBy(x=>x.AnchorX.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    +","+x.AnchorY.ToString(System.Globalization.CultureInfo.InvariantCulture),StringComparer.Ordinal).Any(x=>x.Count()>1)
                ||deployments.Any(x=>s.Actors.All(a=>a.Id!=x.SetterId)||x.ArmedRevision>s.Revision||x.ArmedAt>s.RuleClock)
                ||actions.Any(x=>x.StartedAt>s.RuleClock||x.EndedAt.HasValue&&(x.EndedAt.Value<x.StartedAt||x.EndedAt.Value>s.RuleClock)
                    ||x.Status==HuntingTrapActionStatus.Working&&x.StartedAt.AddSeconds(6)<=s.RuleClock
                    ||x.Status!=HuntingTrapActionStatus.Working&&x.EndedAt.HasValue&&x.EndedAt.Value>x.StartedAt.AddSeconds(6)
                    ||x.Status!=HuntingTrapActionStatus.Working&&x.EndedAt.HasValue&&x.EndedAt.Value==x.StartedAt&&!x.Tactical&&x.Status!=HuntingTrapActionStatus.Interrupted
                ||x.Tactical&&x.Status!=HuntingTrapActionStatus.Working&&(!x.EndedAt.HasValue||x.EndedAt.Value!=x.StartedAt))
                ||triggers.Any(x=>x.CreatedRevision>s.Revision||x.ResolvedRevision>s.Revision||x.At>s.RuleClock
                    ||x.Status==HuntingTrapTriggerStatus.Pending&&s.InventoryCombat&&s.Encounter==null)
                ||tethers.Any(x=>x.ReleasedRevision>s.Revision||x.Status==HuntingTrapTetherStatus.Active&&x.MaximumDistanceFeet!=3))
                throw new ArgumentException("Invalid hunting-trap history or clock.");
            foreach(var deployment in deployments) {
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==deployment.TrapItemId);
                var trigger=deployment.TriggerId==""?null:triggers.SingleOrDefault(x=>x.Id==deployment.TriggerId);
                if(item==null||item.ProfileId!="adventuring-gear.hunting-trap"||item.OwnerId!=deployment.SetterId
                    ||deployment.Status==HuntingTrapDeploymentStatus.Armed&&(item.Placement!=PortablePlacement.Ground
                        ||item.GroundX!=deployment.AnchorX||item.GroundY!=deployment.AnchorY||trigger!=null)
                    ||deployment.Status==HuntingTrapDeploymentStatus.Sprung&&(trigger==null||trigger.DeploymentId!=deployment.Id
                        ||trigger.SourceAppliedRevision!=deployment.ArmedRevision))
                    throw new ArgumentException("Hunting-trap deployment does not match its physical item or trigger.");
            }
            foreach(var trigger in triggers) {
                var deployment=deployments.SingleOrDefault(x=>x.Id==trigger.DeploymentId);
                var route=trigger.RouteStartedRevision==0?null:s.RouteTravels.SingleOrDefault(x=>x.StartedRevision==trigger.RouteStartedRevision);
                bool validEntry=false;
                if(trigger.EntryKind==HuntingTrapEntryKind.TacticalStep)
                    validEntry=s.TacticalMoves.Any(x=>x.Id==trigger.EntryId&&x.Status==TacticalMoveStatus.Completed
                        &&x.ResolvedRevision==trigger.CreatedRevision&&x.ActorId==trigger.EntrantId
                        &&x.ToX==deployment?.AnchorX&&x.ToY==deployment?.AnchorY);
                else if(trigger.EntryKind==HuntingTrapEntryKind.ForcedTacticalStep)
                    validEntry=s.OverwatchRiderChoices.Any(x=>x.Id==trigger.EntryId&&x.Status==OverwatchRiderChoiceStatus.Resolved
                            &&x.Choice==OverwatchRider.Push&&x.MovedFeet>0&&x.ResolvedRevision==trigger.CreatedRevision
                            &&x.TargetId==trigger.EntrantId&&x.ToX==deployment?.AnchorX&&x.ToY==deployment?.AnchorY);
                else if(trigger.EntryKind==HuntingTrapEntryKind.ExplorationStep)
                    validEntry=trigger.EntryId.StartsWith("world.",StringComparison.Ordinal)
                        &&long.TryParse(trigger.EntryId.Substring(6),System.Globalization.NumberStyles.None,
                            System.Globalization.CultureInfo.InvariantCulture,out long moveRevision)
                        &&moveRevision<trigger.CreatedRevision&&s.Receipts.Any(receipt=>receipt.Revision==moveRevision
                            &&CommandHistory.Read(receipt).Actor==trigger.EntrantId
                            &&CommandHistory.Read(receipt).Kind==CommandKind.BeginWorldStep);
                else if(trigger.EntryKind==HuntingTrapEntryKind.RouteTravelCheckpoint)
                    validEntry=route!=null
                        &&route.RouteId==trigger.RouteId&&route.TravelerId==trigger.EntrantId
                        &&route.StartedRevision<trigger.CreatedRevision&&route.SegmentStartProgress<=trigger.RouteProgress
                        &&trigger.RouteProgress<=route.SegmentStartProgress+route.SegmentProgressAward
                        &&route.Progress>=trigger.RouteProgress;
                var tether=trigger.TetherId==""?null:tethers.SingleOrDefault(x=>x.Id==trigger.TetherId);
                if(deployment==null||deployment.Status!=HuntingTrapDeploymentStatus.Sprung||deployment.TriggerId!=trigger.Id
                    ||deployment.ArmedRevision!=trigger.SourceAppliedRevision||!s.Actors.Any(a=>a.Id==trigger.EntrantId)||!validEntry
                    ||trigger.Status==HuntingTrapTriggerStatus.Resolved&&!trigger.SaveSuccess
                        &&(tether==null||tether.TriggerId!=trigger.Id||tether.ActorId!=trigger.EntrantId)
                    ||trigger.Status==HuntingTrapTriggerStatus.Resolved&&trigger.SaveSuccess&&tether!=null
                    ||trigger.Status==HuntingTrapTriggerStatus.Pending&&tether!=null)
                    throw new ArgumentException("Invalid hunting-trap trigger relation.");
            }
            foreach(var tether in tethers) {
                var trigger=triggers.SingleOrDefault(x=>x.Id==tether.TriggerId);
                var deployment=deployments.SingleOrDefault(x=>x.Id==tether.DeploymentId);
                var action=tether.ReleaseActionId==""?null:actions.SingleOrDefault(x=>x.Id==tether.ReleaseActionId);
                if(trigger==null||trigger.Status!=HuntingTrapTriggerStatus.Resolved||trigger.SaveSuccess||deployment==null
                    ||trigger.DeploymentId!=deployment.Id||tether.TrapItemId!=deployment.TrapItemId||tether.ActorId!=trigger.EntrantId
                    ||tether.AnchorX!=deployment.AnchorX||tether.AnchorY!=deployment.AnchorY
                    ||tether.Status==HuntingTrapTetherStatus.Released&&(action==null||action.Kind!=HuntingTrapActionKind.Free
                        ||action.Status!=HuntingTrapActionStatus.Succeeded||action.TargetActorId!=tether.ActorId
                        ||action.DeploymentId!=deployment.Id||action.EndedAt==null||action.EndedAt.Value>s.RuleClock
                        ||action.Id!=tether.ReleaseActionId))
                    throw new ArgumentException("Invalid hunting-trap tether relation.");
            }
            if(tethers.Where(x=>x.Status==HuntingTrapTetherStatus.Active).Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()
                !=tethers.Count(x=>x.Status==HuntingTrapTetherStatus.Active))throw new ArgumentException("An actor has more than one active hunting-trap tether.");
            if(actions.GroupBy(x=>x.ActorId,StringComparer.Ordinal).Any(g=>g.Count(x=>x.Status==HuntingTrapActionStatus.Working)>1)
                ||actions.GroupBy(x=>x.TrapItemId,StringComparer.Ordinal).Any(g=>g.Key!=""&&g.Count(x=>x.Status==HuntingTrapActionStatus.Working)>1))
                throw new ArgumentException("Conflicting active hunting-trap work.");
            foreach(var action in actions) {
                if(!s.Actors.Any(a=>a.Id==action.ActorId)||action.TrapItemId!=""&&!s.PortableEquipment.Any(x=>x.Id==action.TrapItemId)
                    ||action.TargetActorId!=""&&!s.Actors.Any(x=>x.Id==action.TargetActorId)
                    ||action.DeploymentId!=""&&!deployments.Any(x=>x.Id==action.DeploymentId))
                    throw new ArgumentException("Invalid hunting-trap action reference.");
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==action.Id).ToArray();
                bool zeroTimeInterruption=action.Status==HuntingTrapActionStatus.Interrupted&&action.EndedAt==action.StartedAt;
                if(action.Tactical?intervals.Length!=0:zeroTimeInterruption?intervals.Length!=0:intervals.Length!=1
                    ||!action.Tactical&&!zeroTimeInterruption&&intervals[0].WorkerId!=action.ActorId
                    ||!action.Tactical&&!zeroTimeInterruption&&intervals[0].Start!=action.StartedAt
                    ||!action.Tactical&&!zeroTimeInterruption&&intervals[0].End!=action.StartedAt.AddSeconds(6)
                    ||!action.Tactical&&!zeroTimeInterruption&&action.Status==HuntingTrapActionStatus.Interrupted
                        &&intervals[0].End!=action.EndedAt.Value)
                    throw new ArgumentException("Hunting-trap labor interval mismatch.");
            }
            if(s.Work.WorkerIntervals.Any(w=>actions.All(x=>x.Id!=w.JobId)
                &&s.Crops.SelectMany(c=>c.Tasks).All(t=>t.Id!=w.JobId)&&s.Intakes.All(j=>j.Id!=w.JobId)
                &&s.Handling.All(j=>j.Id!=w.JobId)&&s.WaterFills.All(j=>j.Id!=w.JobId)&&s.VesselMoves.All(j=>j.Id!=w.JobId)
                &&s.SupplyCacheAttempts.All(j=>j.Id!=w.JobId)&&s.PortableHandling.All(j=>j.Id!=w.JobId)
                &&s.FormulaWork.All(j=>j.Id!=w.JobId)&&s.RepairWork.All(j=>j.Id!=w.JobId)&&s.ManufacturingOrders.All(j=>j.Id!=w.JobId)
                &&s.FishingTrapAttempts.All(j=>j.Id!=w.JobId)&&s.FishingTrapRetrievals.All(j=>j.Id!=w.JobId)
                &&s.HarvestAttempts.All(j=>j.Id!=w.JobId)&&s.MiningAttempts.All(j=>j.Id!=w.JobId)
                &&s.ProspectingAttempts.All(j=>j.Id!=w.JobId)&&s.MiningAssayAttempts.All(j=>j.Id!=w.JobId)
                &&s.DestructiveMiningAssayAttempts.All(j=>j.Id!=w.JobId)&&s.MineralPreparationAttempts.All(j=>j.Id!=w.JobId)
                &&s.OrdinaryReceptacleAttempts.All(j=>j.Id!=w.JobId)
                &&s.RouteMappingWorkAttempts.All(j=>j.Id!=w.JobId)
                &&s.CacheExcavations.All(j=>j.Id!=w.JobId)))
                throw new ArgumentException("Unattributed hunting-trap worker interval.");
        }
    }
}
