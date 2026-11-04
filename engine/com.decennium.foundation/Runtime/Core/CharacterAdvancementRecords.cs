using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class CharacterAdvancementProfileIds
    {
        public const string TestOnlySoldierLevel1="TEST_ONLY.soldier-level1";
    }

    public static class CharacterFeatureIds
    {
        public const string DefensivePositioning="soldier.base.defensive-positioning";
        public const string TacticalReposition="soldier.base.tactical-reposition";
    }
    public enum HitPointGainMethod { FixedAverage }

    /// <summary>Explicit map marker for a solid feature or cover that qualifies for this one passive.</summary>
    public sealed class TacticalCoverRecord
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }
        public TacticalCoverRecord(string id,int x,int y)
        {if(!Validation.ValidId(id))throw new ArgumentException("Invalid tactical cover identity.");Id=id;X=x;Y=y;}
    }

    /// <summary>Level-gated feature resource state, kept separate from the ordinary Action/Reaction ledgers.</summary>
    public sealed class CharacterFeatureRuntimeRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public bool BonusActionAvailable { get; }
        public int RepositionRechargeRemaining { get; }
        public int RepositionTurnOrdinal { get; }
        public long RepositionBudgetRemaining { get; }
        public CharacterFeatureRuntimeRecord(string actorId,int lastRegularStart,bool bonusActionAvailable=true,int rechargeRemaining=0,
            int repositionTurnOrdinal=-1,long repositionBudgetRemaining=0)
        {
            if(!Validation.ValidId(actorId)||lastRegularStart< -1||rechargeRemaining<0||rechargeRemaining>2||repositionTurnOrdinal< -1
                ||repositionBudgetRemaining<0||repositionTurnOrdinal<0&&repositionBudgetRemaining!=0)
                throw new ArgumentException("Invalid character feature runtime.");
            ActorId=actorId;LastRegularStart=lastRegularStart;BonusActionAvailable=bonusActionAvailable;RepositionRechargeRemaining=rechargeRemaining;
            RepositionTurnOrdinal=repositionTurnOrdinal;RepositionBudgetRemaining=repositionBudgetRemaining;
        }
        public CharacterFeatureRuntimeRecord RegularStart(int ordinal)
        {
            if(ordinal<=LastRegularStart)throw new ArgumentException("Feature regular start cannot repeat or go backward.");
            return new CharacterFeatureRuntimeRecord(ActorId,ordinal,true,Math.Max(0,RepositionRechargeRemaining-1));
        }
        public CharacterFeatureRuntimeRecord Activate(int ordinal,long budget)
        {
            if(ordinal<0||budget<1||!BonusActionAvailable||RepositionRechargeRemaining!=0)throw new ArgumentException("Tactical Reposition is unavailable.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,false,2,ordinal,budget);
        }
        public CharacterFeatureRuntimeRecord SpendReposition(long cost)
        {
            if(cost<0||cost>RepositionBudgetRemaining||RepositionTurnOrdinal<0)throw new ArgumentException("Invalid special movement expenditure.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,RepositionBudgetRemaining-cost);
        }
        public CharacterFeatureRuntimeRecord EndTacticalUse()=>new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining);
    }

    /// <summary>A host-authored entitlement tied to one actor. Consuming it is a separate command.</summary>
    public sealed class CharacterMilestoneRecord
    {
        public string MilestoneId { get; }
        public string ActorId { get; }
        public long AwardedRevision { get; }
        public long ConsumedRevision { get; }
        public CharacterMilestoneRecord(string milestoneId,string actorId,long awardedRevision,long consumedRevision=0)
        {
            if(!Validation.ValidId(milestoneId)||!Validation.ValidId(actorId)||awardedRevision<1||consumedRevision<0
                ||consumedRevision!=0&&consumedRevision<=awardedRevision)throw new ArgumentException("Invalid milestone entitlement.");
            MilestoneId=milestoneId;ActorId=actorId;AwardedRevision=awardedRevision;ConsumedRevision=consumedRevision;
        }
        public CharacterMilestoneRecord Consume(long revision)=>new CharacterMilestoneRecord(MilestoneId,ActorId,AwardedRevision,revision);
    }

    /// <summary>Per-level Hit Die availability, separate from the immutable attained-level count.</summary>
    public sealed class CharacterHitDieRecord
    {
        public string ActorId { get; }
        public int LevelOrdinal { get; }
        public string ClassName { get; }
        public int DieSize { get; }
        public bool Spent { get; }
        public CharacterHitDieRecord(string actorId,int levelOrdinal,string className,int dieSize,bool spent)
        {
            if(!Validation.ValidId(actorId)||levelOrdinal<1||levelOrdinal>20||string.IsNullOrEmpty(className)||className.Length>96
                ||className.Any(c=>c<32||c>126)||(dieSize!=6&&dieSize!=8&&dieSize!=10&&dieSize!=12))throw new ArgumentException("Invalid Hit Die record.");
            ActorId=actorId;LevelOrdinal=levelOrdinal;ClassName=className;DieSize=dieSize;Spent=spent;
        }
    }

    /// <summary>Explicit class-card grant; owned features are never inferred from class level alone.</summary>
    public sealed class CharacterFeatureGrantRecord
    {
        public string ActorId { get; }
        public string FeatureId { get; }
        public string ClassName { get; }
        public int ClassLevel { get; }
        public string MilestoneId { get; }
        public long GrantedRevision { get; }
        public CharacterFeatureGrantRecord(string actorId,string featureId,string className,int classLevel,string milestoneId,long grantedRevision)
        {
            if(!Validation.ValidId(actorId)||!Validation.ValidId(featureId)||string.IsNullOrEmpty(className)||className.Length>96
                ||className.Any(c=>c<32||c>126)||classLevel<1||classLevel>20||!Validation.ValidId(milestoneId)||grantedRevision<1)
                throw new ArgumentException("Invalid feature grant.");
            ActorId=actorId;FeatureId=featureId;ClassName=className;ClassLevel=classLevel;MilestoneId=milestoneId;GrantedRevision=grantedRevision;
        }
    }

    /// <summary>Auditable, replay-derived result for a single earned level.</summary>
    public sealed class CharacterAdvancementRecord
    {
        public string ActorId { get; }
        public string MilestoneId { get; }
        public long Revision { get; }
        public int PreviousTotalLevel { get; }
        public int NewTotalLevel { get; }
        public string ClassName { get; }
        public int ClassLevel { get; }
        public int BaseHpGain { get; }
        public HitPointGainMethod HitPointMethod { get; }
        public long MaximumHpBefore { get; }
        public long MaximumHpAfter { get; }
        public long CurrentHpBefore { get; }
        public long CurrentHpAfter { get; }
        public string FeatureOne { get; }
        public string FeatureTwo { get; }
        public CharacterAdvancementRecord(string actorId,string milestoneId,long revision,int previousTotalLevel,int newTotalLevel,
            string className,int classLevel,int baseHpGain,HitPointGainMethod method,long maximumBefore,long maximumAfter,
            long currentBefore,long currentAfter,string featureOne,string featureTwo)
        {
            if(!Validation.ValidId(actorId)||!Validation.ValidId(milestoneId)||revision<1||previousTotalLevel<1||newTotalLevel!=previousTotalLevel+1
                ||string.IsNullOrEmpty(className)||className.Length>96||className.Any(c=>c<32||c>126)||classLevel<1||classLevel>20
                ||baseHpGain<1||!Enum.IsDefined(typeof(HitPointGainMethod),method)||maximumBefore<1||maximumAfter<maximumBefore
                ||currentBefore<0||currentBefore>maximumBefore||currentAfter<0||currentAfter>maximumAfter
                ||!Validation.ValidId(featureOne)||!Validation.ValidId(featureTwo)||featureOne==featureTwo)
                throw new ArgumentException("Invalid advancement result.");
            ActorId=actorId;MilestoneId=milestoneId;Revision=revision;PreviousTotalLevel=previousTotalLevel;NewTotalLevel=newTotalLevel;
            ClassName=className;ClassLevel=classLevel;BaseHpGain=baseHpGain;HitPointMethod=method;MaximumHpBefore=maximumBefore;
            MaximumHpAfter=maximumAfter;CurrentHpBefore=currentBefore;CurrentHpAfter=currentAfter;FeatureOne=featureOne;FeatureTwo=featureTwo;
        }
    }

    /// <summary>Optional command payload. Empty fields are representable so the policy can reject an incomplete selection atomically.</summary>
    public sealed class CharacterAdvancementRequest
    {
        public string FeatureOne { get; }
        public string FeatureTwo { get; }
        public CharacterAdvancementRequest(string featureOne="",string featureTwo="")
        {
            if(featureOne==null||featureTwo==null||featureOne!=""&&!Validation.ValidId(featureOne)||featureTwo!=""&&!Validation.ValidId(featureTwo))
                throw new ArgumentException("Invalid feature selection payload.");
            FeatureOne=featureOne;FeatureTwo=featureTwo;
        }
    }

    public static class CharacterAdvancementValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.CharacterMilestones==null||s.CharacterHitDice==null||s.CharacterFeatureGrants==null||s.CharacterAdvancements==null
                ||s.CharacterFeatureRuntime==null||s.TacticalCovers==null
                ||s.CharacterMilestones.Length>256||s.CharacterHitDice.Length>1280||s.CharacterFeatureGrants.Length>256||s.CharacterAdvancements.Length>128
                ||s.CharacterFeatureRuntime.Length>64||s.TacticalCovers.Length>64
                ||s.CharacterMilestones.Any(x=>x==null)||s.CharacterHitDice.Any(x=>x==null)||s.CharacterFeatureGrants.Any(x=>x==null)||s.CharacterAdvancements.Any(x=>x==null)
                ||s.CharacterFeatureRuntime.Any(x=>x==null)||s.TacticalCovers.Any(x=>x==null))
                throw new ArgumentException("Invalid advancement collections.");
            if(s.SchemaVersion<Snapshot.CharacterAdvancementSchema) {
                if(s.CharacterMilestones.Length+s.CharacterHitDice.Length+s.CharacterFeatureGrants.Length+s.CharacterAdvancements.Length+s.CharacterFeatureRuntime.Length+s.TacticalCovers.Length!=0)
                    throw new ArgumentException("Character progression requires schema21.");
                return;
            }
            bool Actor(string id)=>s.Characters.Any(c=>c.ActorId==id);
            if(s.TacticalCovers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.TacticalCovers.Length
                ||s.TacticalCovers.Select(x=>x.X+","+x.Y).Distinct(StringComparer.Ordinal).Count()!=s.TacticalCovers.Length
                ||s.Characters.Where(c=>c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                    ||s.CharacterHitDice.Any(d=>d.ActorId==c.ActorId)||s.CharacterMilestones.Any(m=>m.ActorId==c.ActorId)
                    ||s.CharacterFeatureGrants.Any(g=>g.ActorId==c.ActorId)||s.CharacterAdvancements.Any(a=>a.ActorId==c.ActorId)
                    ||s.CharacterFeatureRuntime.Any(r=>r.ActorId==c.ActorId))
                    .Any(c=>s.CharacterHitDice.Count(d=>d.ActorId==c.ActorId)!=c.Levels.Count)
                ||s.CharacterFeatureRuntime.Any(x=>!Actor(x.ActorId)||!s.CharacterFeatureGrants.Any(g=>g.ActorId==x.ActorId&&g.FeatureId==CharacterFeatureIds.TacticalReposition)
                    ||x.LastRegularStart>=0&&s.WorldSchedule!=null&&x.LastRegularStart!=s.WorldSchedule.LatestStart(x.ActorId,s.WorldSchedule.ProcessedSlot)
                    ||x.RepositionTurnOrdinal>=0&&(!s.InventoryCombat||s.Encounter==null||x.RepositionTurnOrdinal!=s.Encounter.TurnOrdinal))
                ||s.CharacterFeatureRuntime.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterFeatureRuntime.Length
                ||s.CharacterMilestones.Any(m=>!Actor(m.ActorId)||m.AwardedRevision>s.Revision||m.ConsumedRevision>s.Revision)
                ||s.CharacterMilestones.Select(m=>m.ActorId+"|"+m.MilestoneId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterMilestones.Length
                ||s.CharacterHitDice.Any(d=>!Actor(d.ActorId)||d.LevelOrdinal>s.Characters.Single(c=>c.ActorId==d.ActorId).Levels.Count
                    ||d.ClassName!=s.Characters.Single(c=>c.ActorId==d.ActorId).Levels[d.LevelOrdinal-1].ClassName)
                ||s.CharacterHitDice.Select(d=>d.ActorId+"|"+d.LevelOrdinal).Distinct(StringComparer.Ordinal).Count()!=s.CharacterHitDice.Length
                ||s.CharacterFeatureGrants.Any(g=>!Actor(g.ActorId)||g.GrantedRevision>s.Revision||!s.CharacterMilestones.Any(m=>m.ActorId==g.ActorId&&m.MilestoneId==g.MilestoneId&&m.ConsumedRevision==g.GrantedRevision)
                    ||(g.FeatureId!=CharacterFeatureIds.DefensivePositioning&&g.FeatureId!=CharacterFeatureIds.TacticalReposition)
                    ||g.ClassName!="Soldier"||g.ClassLevel!=2||g.ClassLevel>s.Characters.Single(c=>c.ActorId==g.ActorId).Levels.Count(x=>x.ClassName==g.ClassName))
                ||s.CharacterFeatureGrants.Select(g=>g.ActorId+"|"+g.FeatureId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterFeatureGrants.Length
                ||s.CharacterAdvancements.Any(a=>!Actor(a.ActorId)||a.Revision>s.Revision||!s.CharacterMilestones.Any(m=>m.ActorId==a.ActorId&&m.MilestoneId==a.MilestoneId&&m.ConsumedRevision==a.Revision)
                    ||a.PreviousTotalLevel!=1||a.NewTotalLevel!=2||a.ClassName!="Soldier"||a.ClassLevel!=2||a.BaseHpGain!=6||a.HitPointMethod!=HitPointGainMethod.FixedAverage
                    ||a.MaximumHpBefore!=10||a.MaximumHpAfter!=16||a.FeatureOne!=CharacterFeatureIds.DefensivePositioning||a.FeatureTwo!=CharacterFeatureIds.TacticalReposition
                    ||a.NewTotalLevel!=s.Characters.Single(c=>c.ActorId==a.ActorId).Levels.Count
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==a.ActorId&&g.FeatureId==a.FeatureOne&&g.GrantedRevision==a.Revision)
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==a.ActorId&&g.FeatureId==a.FeatureTwo&&g.GrantedRevision==a.Revision))
                ||s.CharacterAdvancements.Select(a=>a.ActorId+"|"+a.MilestoneId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterAdvancements.Length
                ||s.CharacterMilestones.Any(m=>(m.ConsumedRevision!=0)!=s.CharacterAdvancements.Any(a=>a.ActorId==m.ActorId&&a.MilestoneId==m.MilestoneId)))
                throw new ArgumentException("Invalid advancement references or ledgers.");
            foreach(var actor in s.CharacterHitDice.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal)) {
                var dice=s.CharacterHitDice.Where(x=>x.ActorId==actor).OrderBy(x=>x.LevelOrdinal).ToArray();
                if(dice.Length!=s.Characters.Single(x=>x.ActorId==actor).Levels.Count
                    ||!dice.Select(x=>x.LevelOrdinal).SequenceEqual(Enumerable.Range(1,dice.Length)))throw new ArgumentException("Hit Dice must cover attained levels in order.");
            }
        }
    }
}
