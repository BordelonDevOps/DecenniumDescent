using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum OverwatchShotStatus { Available, Spent, Forfeited }
    public enum OverwatchDesignationStatus { Active, Replaced, Expired }
    public enum OverwatchRider { None, Snare, Bleed, Push }

    /// <summary>One actor's Base Overwatch shot entitlement for a regular-start interval.
    /// The interval owns use; replacing a zone never creates another shot.</summary>
    public sealed class OverwatchIntervalRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public OverwatchShotStatus ShotStatus { get; }
        public OverwatchIntervalRecord(string actorId,int lastRegularStart,OverwatchShotStatus shotStatus=OverwatchShotStatus.Available)
        {
            if(!Validation.ValidId(actorId)||lastRegularStart<0||!Enum.IsDefined(typeof(OverwatchShotStatus),shotStatus))
                throw new ArgumentException("Invalid Overwatch interval entitlement.");
            ActorId=actorId;LastRegularStart=lastRegularStart;ShotStatus=shotStatus;
        }
        public OverwatchIntervalRecord WithStatus(OverwatchShotStatus status)=>new OverwatchIntervalRecord(ActorId,LastRegularStart,status);
        public bool SameAs(OverwatchIntervalRecord x)=>x!=null&&ActorId==x.ActorId&&LastRegularStart==x.LastRegularStart&&ShotStatus==x.ShotStatus;
    }

    /// <summary>A fixed, axis-aligned 3-by-3-cell Overwatch zone. The interval and shot
    /// entitlement are stored separately so a replacement cannot refresh either one.</summary>
    public sealed class OverwatchDesignationRecord
    {
        public string Id { get; }
        public string OwnerId { get; }
        public int LastRegularStart { get; }
        public int X0 { get; }
        public int Y0 { get; }
        public long CreatedRevision { get; }
        public OverwatchDesignationStatus Status { get; }
        public long EndedRevision { get; }
        public OverwatchDesignationRecord(string id,string ownerId,int lastRegularStart,int x0,int y0,long createdRevision,
            OverwatchDesignationStatus status=OverwatchDesignationStatus.Active,long endedRevision=0)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(ownerId)||lastRegularStart<0||createdRevision<0
                ||!Enum.IsDefined(typeof(OverwatchDesignationStatus),status)||endedRevision<0
                ||status==OverwatchDesignationStatus.Active&&endedRevision!=0
                ||status!=OverwatchDesignationStatus.Active&&endedRevision<Math.Max(1,createdRevision))
                throw new ArgumentException("Invalid Overwatch designation.");
            Id=id;OwnerId=ownerId;LastRegularStart=lastRegularStart;X0=x0;Y0=y0;CreatedRevision=createdRevision;Status=status;EndedRevision=endedRevision;
        }
        public bool Contains(int x,int y)=>x>=(long)X0&&x<=(long)X0+2&&y>=(long)Y0&&y<=(long)Y0+2;
        public OverwatchDesignationRecord End(OverwatchDesignationStatus status,long revision)
        {
            if(Status!=OverwatchDesignationStatus.Active||status==OverwatchDesignationStatus.Active)throw new InvalidOperationException("Only an active zone may end.");
            return new OverwatchDesignationRecord(Id,OwnerId,LastRegularStart,X0,Y0,CreatedRevision,status,revision);
        }
        public bool SameAs(OverwatchDesignationRecord x)=>x!=null&&Id==x.Id&&OwnerId==x.OwnerId&&LastRegularStart==x.LastRegularStart
            &&X0==x.X0&&Y0==x.Y0&&CreatedRevision==x.CreatedRevision&&Status==x.Status&&EndedRevision==x.EndedRevision;
    }

    public static class OverwatchValidation
    {
        // Regular-start history is compacted as it advances; retain the current and immediately
        // previous interval per actor so old zones remain inspectable without campaign growth.
        public const int MaxIntervals=128,MaxDesignations=128;
        public static void Validate(Snapshot s)
        {
            if(s.OverwatchIntervals==null||s.OverwatchDesignations==null||s.OverwatchIntervals.Length>MaxIntervals
                ||s.OverwatchDesignations.Length>MaxDesignations||s.OverwatchIntervals.Any(x=>x==null)||s.OverwatchDesignations.Any(x=>x==null))
                throw new ArgumentException("Invalid Overwatch collections.");
            OverwatchExecutionValidation.Validate(s);
            if(s.SchemaVersion<Snapshot.OverwatchSchema)
            {
                if(s.OverwatchIntervals.Length+s.OverwatchDesignations.Length!=0)throw new ArgumentException("Overwatch state requires schema25.");
                return;
            }
            if(s.OverwatchIntervals.Length+s.OverwatchDesignations.Length==0)return;
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            bool Current(string actor,int interval)=>s.OverwatchIntervals.Where(x=>x.ActorId==actor).Max(x=>x.LastRegularStart)==interval;
            if(s.WorldSchedule==null||s.OverwatchIntervals.Select(x=>x.ActorId+"|"+x.LastRegularStart).Distinct(StringComparer.Ordinal).Count()!=s.OverwatchIntervals.Length
                ||s.OverwatchIntervals.Any(x=>!Actor(x.ActorId)||!s.WorldSchedule.Order.Contains(x.ActorId)
                    ||x.LastRegularStart>s.WorldSchedule.LatestStart(x.ActorId,s.WorldSchedule.ProcessedSlot)
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==x.ActorId&&g.FeatureId==CharacterFeatureIds.Overwatch))
                ||s.OverwatchIntervals.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Any(actor=>!s.OverwatchIntervals.Any(x=>x.ActorId==actor
                    &&x.LastRegularStart==s.WorldSchedule.LatestStart(actor,s.WorldSchedule.ProcessedSlot)))
                ||s.OverwatchDesignations.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.OverwatchDesignations.Length
                ||s.OverwatchDesignations.Any(x=>!Actor(x.OwnerId)||x.CreatedRevision>s.Revision||x.EndedRevision>s.Revision
                    ||!s.OverwatchIntervals.Any(i=>i.ActorId==x.OwnerId&&i.LastRegularStart==x.LastRegularStart)
                    ||x.Status==OverwatchDesignationStatus.Active&&!Current(x.OwnerId,x.LastRegularStart))
                ||s.OverwatchDesignations.Where(x=>x.Status==OverwatchDesignationStatus.Active).Select(x=>x.OwnerId).Distinct(StringComparer.Ordinal).Count()
                    !=s.OverwatchDesignations.Count(x=>x.Status==OverwatchDesignationStatus.Active))
                throw new ArgumentException("Invalid Overwatch references or active zones.");
        }
    }
}
