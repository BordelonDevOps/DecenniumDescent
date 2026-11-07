using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Persistent application facts for a source-registered periodic rider. Core records
    /// structure and preserve these facts; the selected content policy owns their meaning.</summary>
    public sealed class PeriodicRiderRecord
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string FamilyId { get; }
        public string OwnerId { get; }
        public string SourceId { get; }
        public string TargetId { get; }
        public string OriginEventId { get; }
        public string DamageType { get; }
        public int ApplyingDc { get; }
        public long ApplicationOrder { get; }
        public RuleTime AppliedAt { get; }
        public long NextStartSlot { get; }
        public int RemainingTicks { get; }
        public bool Suppressed { get; }
        public RuleTime? EndedAt { get; }
        public string EndingMethod { get; }

        public PeriodicRiderRecord(string id,string profileId,string familyId,string ownerId,string sourceId,string targetId,
            string originEventId,string damageType,int applyingDc,long applicationOrder,RuleTime appliedAt,long nextStartSlot,
            int remainingTicks,bool suppressed=false,RuleTime? endedAt=null,string endingMethod="")
        {
            foreach(string value in new[]{id,profileId,familyId,ownerId,sourceId,targetId,originEventId,damageType})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid periodic rider identity.");
            if(applyingDc<0||applyingDc>100||applicationOrder<0||nextStartSlot<0||remainingTicks<0||remainingTicks>64
                ||endingMethod==null||endingMethod!=""&&!Validation.ValidId(endingMethod)
                ||remainingTicks==0&&(!endedAt.HasValue||endingMethod=="")
                ||remainingTicks>0&&(endedAt.HasValue||endingMethod!=""))
                throw new ArgumentException("Invalid periodic rider state.");
            Id=id;ProfileId=profileId;FamilyId=familyId;OwnerId=ownerId;SourceId=sourceId;TargetId=targetId;OriginEventId=originEventId;
            DamageType=damageType;ApplyingDc=applyingDc;ApplicationOrder=applicationOrder;AppliedAt=appliedAt;NextStartSlot=nextStartSlot;
            RemainingTicks=remainingTicks;Suppressed=suppressed;EndedAt=endedAt;EndingMethod=endingMethod;
        }
        public bool Present=>RemainingTicks>0&&!EndedAt.HasValue;
        public PeriodicRiderRecord Refresh(long nextStartSlot)
        {
            if(!Present)throw new InvalidOperationException("Only a present rider can refresh.");
            return new PeriodicRiderRecord(Id,ProfileId,FamilyId,OwnerId,SourceId,TargetId,OriginEventId,DamageType,
                ApplyingDc,ApplicationOrder,AppliedAt,Math.Max(NextStartSlot,nextStartSlot),RemainingTicks,Suppressed);
        }
        public PeriodicRiderRecord WithSuppressed(bool value)
        {
            if(!Present)throw new InvalidOperationException("Only a present rider can change suppression.");
            return new PeriodicRiderRecord(Id,ProfileId,FamilyId,OwnerId,SourceId,TargetId,OriginEventId,DamageType,
                ApplyingDc,ApplicationOrder,AppliedAt,NextStartSlot,RemainingTicks,value);
        }
        public PeriodicRiderRecord End(RuleTime at,string method)
        {
            if(!Present||at<AppliedAt)throw new InvalidOperationException("Only a present rider can end.");
            return new PeriodicRiderRecord(Id,ProfileId,FamilyId,OwnerId,SourceId,TargetId,OriginEventId,DamageType,
                ApplyingDc,ApplicationOrder,AppliedAt,NextStartSlot,0,Suppressed,at,method);
        }
        public bool SameAs(PeriodicRiderRecord x)=>x!=null&&Id==x.Id&&ProfileId==x.ProfileId&&FamilyId==x.FamilyId&&OwnerId==x.OwnerId
            &&SourceId==x.SourceId&&TargetId==x.TargetId&&OriginEventId==x.OriginEventId&&DamageType==x.DamageType&&ApplyingDc==x.ApplyingDc
            &&ApplicationOrder==x.ApplicationOrder&&AppliedAt==x.AppliedAt&&NextStartSlot==x.NextStartSlot&&RemainingTicks==x.RemainingTicks
            &&Suppressed==x.Suppressed&&EndedAt==x.EndedAt&&EndingMethod==x.EndingMethod;
    }

    public sealed class PeriodicFamilyImmunityRecord
    {
        public string Id { get; }
        public string TargetId { get; }
        public string FamilyId { get; }
        public string SourceId { get; }
        public RuleTime GrantedAt { get; }
        public RuleTime? EndedAt { get; }
        public PeriodicFamilyImmunityRecord(string id,string targetId,string familyId,string sourceId,RuleTime grantedAt,RuleTime? endedAt=null)
        {
            foreach(string value in new[]{id,targetId,familyId,sourceId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid periodic immunity identity.");
            if(endedAt.HasValue&&endedAt.Value<grantedAt)throw new ArgumentException("Invalid periodic immunity interval.");
            Id=id;TargetId=targetId;FamilyId=familyId;SourceId=sourceId;GrantedAt=grantedAt;EndedAt=endedAt;
        }
        public bool Present=>!EndedAt.HasValue;
        public PeriodicFamilyImmunityRecord End(RuleTime at)
        {if(!Present||at<GrantedAt)throw new InvalidOperationException("Only a present immunity can end.");return new PeriodicFamilyImmunityRecord(Id,TargetId,FamilyId,SourceId,GrantedAt,at);}
        public bool SameAs(PeriodicFamilyImmunityRecord x)=>x!=null&&Id==x.Id&&TargetId==x.TargetId&&FamilyId==x.FamilyId
            &&SourceId==x.SourceId&&GrantedAt==x.GrantedAt&&EndedAt==x.EndedAt;
    }

    /// <summary>Explicit skill-training fact. Ability and proficiency modifiers are interpreted by LabModel.</summary>
    public sealed class SkillTrainingRecord
    {
        public string ActorId { get; }
        public string SkillId { get; }
        public int ProficiencyRank { get; }
        public SkillTrainingRecord(string actorId,string skillId,int proficiencyRank)
        {
            if(!Validation.ValidId(actorId)||!Validation.ValidId(skillId)||proficiencyRank<0||proficiencyRank>2)
                throw new ArgumentException("Invalid skill training.");
            ActorId=actorId;SkillId=skillId;ProficiencyRank=proficiencyRank;
        }
        public bool SameAs(SkillTrainingRecord x)=>x!=null&&ActorId==x.ActorId&&SkillId==x.SkillId&&ProficiencyRank==x.ProficiencyRank;
    }

    public enum PeriodicRiderEventKind { Applied, Refreshed, Prevented, Tick, Medicine, Suppression, FamilyImmunity, MagicalHealing }
    public enum PeriodicRiderOutcome { None, Damage, Suppressed, Immune, FamilyLost, TargetDead, MedicineSuccess, MedicineFailure, HealingCure, NoPositiveHealing }
    public enum PeriodicRiderCheckDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    /// <summary>Auditable domain outcome. A command receipt binds it to an admitted event; replay
    /// recomputes it and the shared RNG/life state before accepting a save.</summary>
    public sealed class PeriodicRiderEventRecord
    {
        public string EventId { get; }
        public PeriodicRiderEventKind Kind { get; }
        public PeriodicRiderOutcome Outcome { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public long WorldSlot { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public string RiderId { get; }
        public string SourceId { get; }
        public bool Flag { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public int Dc { get; }
        public int Die { get; }
        public long Amount { get; }
        public long HitPointGain { get; }
        public PeriodicRiderCheckDegree CheckDegree { get; }
        public long CheckTotal { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public PeriodicRiderEventRecord(string eventId,PeriodicRiderEventKind kind,PeriodicRiderOutcome outcome,long revision,RuleTime at,
            long worldSlot,string actorId,string targetId,string riderId,string sourceId,bool flag,int natural,int modifier,int dc,int die,
            long amount,long hitPointGain,uint randomBefore,uint randomAfter,long wordsConsumed,
            PeriodicRiderCheckDegree checkDegree=PeriodicRiderCheckDegree.None,long checkTotal=0)
        {
            if(!Validation.ValidId(eventId)||!Enum.IsDefined(typeof(PeriodicRiderEventKind),kind)||!Enum.IsDefined(typeof(PeriodicRiderOutcome),outcome)
                ||!Enum.IsDefined(typeof(PeriodicRiderCheckDegree),checkDegree)
                ||revision<1||worldSlot< -1||!Validation.ValidId(actorId)||!Validation.ValidId(targetId)
                ||riderId==null||riderId!=""&&!Validation.ValidId(riderId)||sourceId==null||sourceId!=""&&!Validation.ValidId(sourceId)
                ||natural<0||natural>20||modifier< -100||modifier>100||dc<0||dc>100||die<0||die>20||amount<0||hitPointGain<0
                ||randomBefore==0||randomAfter==0||wordsConsumed<0
                ||kind==PeriodicRiderEventKind.Medicine&&(checkDegree==PeriodicRiderCheckDegree.None||amount!=0||checkTotal!=(long)natural+modifier
                    ||flag!=(checkDegree>=PeriodicRiderCheckDegree.Success)
                    ||outcome!=(flag?PeriodicRiderOutcome.MedicineSuccess:PeriodicRiderOutcome.MedicineFailure)
                    ||checkDegree!=ResolveCheckDegree(checkTotal,natural,dc))
                ||kind!=PeriodicRiderEventKind.Medicine&&(checkDegree!=PeriodicRiderCheckDegree.None||checkTotal!=0))
                throw new ArgumentException("Invalid periodic rider event.");
            EventId=eventId;Kind=kind;Outcome=outcome;Revision=revision;At=at;WorldSlot=worldSlot;ActorId=actorId;TargetId=targetId;
            RiderId=riderId;SourceId=sourceId;Flag=flag;Natural=natural;Modifier=modifier;Dc=dc;Die=die;Amount=amount;
            HitPointGain=hitPointGain;CheckDegree=checkDegree;CheckTotal=checkTotal;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
        }
        private static PeriodicRiderCheckDegree ResolveCheckDegree(long total,int natural,int dc)
        {
            var degree=total>=(long)dc+10?PeriodicRiderCheckDegree.CriticalSuccess:total>=dc?PeriodicRiderCheckDegree.Success
                :total<=(long)dc-10?PeriodicRiderCheckDegree.CriticalFailure:PeriodicRiderCheckDegree.Failure;
            if(natural==20&&degree<PeriodicRiderCheckDegree.CriticalSuccess)degree++;
            else if(natural==1&&degree>PeriodicRiderCheckDegree.CriticalFailure)degree--;
            return degree;
        }
        public bool SameAs(PeriodicRiderEventRecord x)=>x!=null&&EventId==x.EventId&&Kind==x.Kind&&Outcome==x.Outcome&&Revision==x.Revision
            &&At==x.At&&WorldSlot==x.WorldSlot&&ActorId==x.ActorId&&TargetId==x.TargetId&&RiderId==x.RiderId&&SourceId==x.SourceId
            &&Flag==x.Flag&&Natural==x.Natural&&Modifier==x.Modifier&&Dc==x.Dc&&Die==x.Die&&Amount==x.Amount&&HitPointGain==x.HitPointGain
            &&CheckDegree==x.CheckDegree&&CheckTotal==x.CheckTotal&&RandomBefore==x.RandomBefore&&RandomAfter==x.RandomAfter&&WordsConsumed==x.WordsConsumed;
    }

    public static class PeriodicRiderValidation
    {
        public const int MaxRiders=128,MaxEvents=512,MaxImmunities=64,MaxSkillRecords=64;
        public static void Validate(Snapshot s)
        {
            if(s.PeriodicRiders==null||s.PeriodicRiderEvents==null||s.PeriodicImmunities==null||s.SkillTraining==null
                ||s.PeriodicRiders.Length>MaxRiders||s.PeriodicRiderEvents.Length>MaxEvents||s.PeriodicImmunities.Length>MaxImmunities
                ||s.SkillTraining.Length>MaxSkillRecords||s.PeriodicRiders.Any(x=>x==null)||s.PeriodicRiderEvents.Any(x=>x==null)
                ||s.PeriodicImmunities.Any(x=>x==null)||s.SkillTraining.Any(x=>x==null))throw new ArgumentException("Invalid periodic rider collections.");
            if(s.SchemaVersion<Snapshot.PeriodicRiderSchema) {
                if(s.PeriodicRiders.Length+s.PeriodicRiderEvents.Length+s.PeriodicImmunities.Length+s.SkillTraining.Length!=0)
                    throw new ArgumentException("Periodic rider records require schema23.");
                return;
            }
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            if(s.WorldSchedule==null||s.PeriodicRiders.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.PeriodicRiders.Length
                ||s.PeriodicRiderEvents.Select(x=>x.EventId).Distinct(StringComparer.Ordinal).Count()!=s.PeriodicRiderEvents.Length
                ||s.PeriodicImmunities.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.PeriodicImmunities.Length
                ||s.SkillTraining.Select(x=>x.ActorId+"|"+x.SkillId).Distinct(StringComparer.Ordinal).Count()!=s.SkillTraining.Length
                ||s.PeriodicRiders.Any(x=>!Actor(x.OwnerId)||!Actor(x.TargetId)||x.AppliedAt>s.RuleClock
                    ||x.ApplicationOrder>s.Revision||x.NextStartSlot<0||x.EndedAt>s.RuleClock)
                ||s.PeriodicRiderEvents.Any(x=>!Actor(x.ActorId)||!Actor(x.TargetId)||x.Revision>s.Revision||x.At>s.RuleClock
                    ||x.WorldSlot>=0&&(x.WorldSlot>s.WorldSchedule.ProcessedSlot||s.WorldSchedule.Start(x.WorldSlot)!=x.At)
                    ||x.RiderId!=""&&!s.PeriodicRiders.Any(r=>r.Id==x.RiderId))
                ||s.PeriodicImmunities.Any(x=>!Actor(x.TargetId)||x.GrantedAt>s.RuleClock||x.EndedAt>s.RuleClock)
                ||s.SkillTraining.Any(x=>!Actor(x.ActorId)||x.SkillId!="medicine"
                    &&!(s.SchemaVersion>=Snapshot.FishingTrapLegacySchema&&x.SkillId=="fishing-tackle")
                    &&!(s.SchemaVersion>=Snapshot.MiningSchema&&x.SkillId=="mining-tools")
                    &&!(s.SchemaVersion>=Snapshot.RouteMappingWorkSchema&&x.SkillId=="survival")
                    &&!(s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema&&s.InitialCharacterLoadouts.Any(b=>b.ActorId==x.ActorId&&b.SelectedSkillIds.Contains(x.SkillId)))))
                throw new ArgumentException("Invalid periodic rider references.");
            foreach(var rider in s.PeriodicRiders.Where(x=>x.Present))
                if(rider.NextStartSlot<=s.WorldSchedule.ProcessedSlot||rider.EndedAt.HasValue||rider.RemainingTicks<1)
                    throw new ArgumentException("Active periodic rider has no future marker.");
        }
    }
}
