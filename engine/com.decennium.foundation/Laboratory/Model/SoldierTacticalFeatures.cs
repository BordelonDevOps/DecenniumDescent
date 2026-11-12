#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal sealed class TacticalAttackEffects
    {
        public string[] EffectIds { get; }
        public bool WarningShot { get; }
        public int CoveringFirePenalty { get; }
        public int TacticalAssessmentBonus { get; }
        public TacticalAttackEffects(string[] effectIds,bool warningShot,int coveringFirePenalty,int tacticalAssessmentBonus=0)
        {EffectIds=effectIds;WarningShot=warningShot;CoveringFirePenalty=coveringFirePenalty;TacticalAssessmentBonus=tacticalAssessmentBonus;}
    }

    /// <summary>Finite Soldier card effects only; this deliberately does not generalize into a
    /// condition, buff, or interrupt framework.</summary>
    internal static class SoldierTacticalFeatures
    {
        public static bool IsAlly(Snapshot s,string first,string second)
            =>first==second||s.TacticalAllies.Any(x=>x.Includes(first)&&x.Other(first)==second);

        public static TacticalAttackEffects ForAttack(Snapshot s,string attacker,string target)
        {
            var active=s.SoldierTacticalEffects.Where(x=>x.Status==SoldierTacticalEffectStatus.Active&&x.TargetActorId==attacker).ToArray();
            var warnings=active.Where(x=>x.Kind==SoldierTacticalEffectKind.WarningShot).ToArray();
            var covering=active.Where(x=>x.Kind==SoldierTacticalEffectKind.CoveringFire&&target!=x.SourceActorId&&IsAlly(s,x.SourceActorId,target)).ToArray();
            var assessments=s.TacticalAssessments.Where(x=>x.Status==TacticalAssessmentStatus.Active&&x.AllyActorId==attacker&&x.EnemyActorId==target).ToArray();
            return new TacticalAttackEffects(warnings.Concat(covering).Select(x=>x.Id).Concat(assessments.Select(x=>x.Id))
                .OrderBy(x=>x,StringComparer.Ordinal).ToArray(),warnings.Length!=0,covering.Length!=0?2:0,assessments.Length==0?0:1);
        }

        public static string Technique(CommandKind kind)=>kind==CommandKind.WarningShot?CharacterFeatureIds.WarningShot
            :kind==CommandKind.CoveringFire?CharacterFeatureIds.CoveringFire:"";

        public static long NextFutureStartSlot(Snapshot s,string actor)
        {
            int index=Array.IndexOf(s.WorldSchedule.Order.ToArray(),actor);if(index<0)throw new ArgumentException("Actor has no regular start marker.");
            long count=s.WorldSchedule.Order.Count,candidate=index,current=s.WorldSchedule.ProcessedSlot;
            if(candidate<=current)candidate=checked(candidate+checked(((current-candidate)/count+1)*count));
            return candidate;
        }

        internal static string AttackAuditCapacityFailure(Snapshot s)
            => s.SchemaVersion >= Snapshot.SoldierTacticalTechniquesSchema
                && s.TacticalAttackAudits.Length >= SoldierTacticalFeatureValidation.MaxAttackAudits
                ? "TacticalAttackAuditCapacityReached" : null;

        public static string CaptureAndConsume(Snapshot s,string attackId,string attacker,string target,string technique,out TacticalAttackEffects effects)
        {
            effects=ForAttack(s,attacker,target);
            if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema)return null;
            string failure = AttackAuditCapacityFailure(s);
            if (failure != null) return failure;
            if(effects.EffectIds.Length>0) {
                var selected=new System.Collections.Generic.HashSet<string>(effects.EffectIds,StringComparer.Ordinal);
                s.SoldierTacticalEffects=s.SoldierTacticalEffects.Select(x=>selected.Contains(x.Id)
                    ?x.Resolve(SoldierTacticalEffectStatus.Consumed,s.Revision+1,attackId):x).ToArray();
                s.TacticalAssessments=s.TacticalAssessments.Select(x=>selected.Contains(x.Id)
                    ?x.Resolve(TacticalAssessmentStatus.Consumed,s.Revision+1,attackId):x).ToArray();
            }
            s.TacticalAttackAudits=s.TacticalAttackAudits.Concat(new[]{new TacticalAttackAuditRecord(attackId,attacker,target,technique,effects.EffectIds)}).ToArray();
            return null;
        }

        public static void ApplyHit(Snapshot s,string attackId,string source,string target,CommandKind technique)
        {
            if(technique!=CommandKind.WarningShot&&technique!=CommandKind.CoveringFire)return;
            var kind=technique==CommandKind.WarningShot?SoldierTacticalEffectKind.WarningShot:SoldierTacticalEffectKind.CoveringFire;
            string id="soldier-effect."+N(s.Revision+1)+"."+(kind==SoldierTacticalEffectKind.WarningShot?"warning":"covering");
            if(kind==SoldierTacticalEffectKind.CoveringFire) {
                s.SoldierTacticalEffects=s.SoldierTacticalEffects.Select(x=>x.Status==SoldierTacticalEffectStatus.Active
                    &&x.Kind==SoldierTacticalEffectKind.CoveringFire&&x.TargetActorId==target
                    ?x.Resolve(SoldierTacticalEffectStatus.Replaced,s.Revision+1,id):x).ToArray();
            }
            long expiry=NextFutureStartSlot(s,kind==SoldierTacticalEffectKind.WarningShot?target:source);
            string expiryActor=kind==SoldierTacticalEffectKind.WarningShot?target:source;
            var phase=kind==SoldierTacticalEffectKind.WarningShot?SoldierTacticalEffectPhase.End:SoldierTacticalEffectPhase.Start;
            long order=s.SoldierTacticalEffects.Length==0?0:checked(s.SoldierTacticalEffects.Max(x=>x.ApplicationOrder)+1);
            var effect=new SoldierTacticalEffectRecord(id,kind,source,target,attackId,order,s.Revision+1,s.RuleClock,expiryActor,expiry,phase);
            s.SoldierTacticalEffects=s.SoldierTacticalEffects.Concat(new[]{effect}).ToArray();
        }

        public static void StartRecharge(Snapshot s,string actor,CommandKind technique)
        {
            if(technique!=CommandKind.WarningShot&&technique!=CommandKind.CoveringFire)return;
            var runtime=s.CharacterFeatureRuntime.Single(x=>x.ActorId==actor);
            var changed=technique==CommandKind.WarningShot?runtime.UseWarningShot():runtime.UseCoveringFire();
            s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Select(x=>x.ActorId==actor?changed:x).ToArray();
        }

        public static void ExpireEndMarkers(Snapshot s,long previousSlot,long nextSlot,long revision)
        {
            if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema||nextSlot<=previousSlot)return;
            var due=s.SoldierTacticalEffects.Where(x=>x.Status==SoldierTacticalEffectStatus.Active&&x.ExpiryPhase==SoldierTacticalEffectPhase.End
                &&x.ExpirySlot>=previousSlot&&x.ExpirySlot<nextSlot).Select(x=>x.Id).ToArray();
            if(due.Length!=0) {
                var ids=new System.Collections.Generic.HashSet<string>(due,StringComparer.Ordinal);
                s.SoldierTacticalEffects=s.SoldierTacticalEffects.Select(x=>ids.Contains(x.Id)
                    ?x.Resolve(SoldierTacticalEffectStatus.Expired,revision,s.WorldSchedule.MarkerId(x.ExpirySlot+1)+".end"):x).ToArray();
            }
            if(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema) {
                var assessments=s.TacticalAssessments.Where(x=>x.Status==TacticalAssessmentStatus.Active
                    &&x.ExpirySlot>=previousSlot&&x.ExpirySlot<nextSlot).Select(x=>x.Id).ToArray();
                if(assessments.Length!=0) {
                    var assessmentIds=new System.Collections.Generic.HashSet<string>(assessments,StringComparer.Ordinal);
                    s.TacticalAssessments=s.TacticalAssessments.Select(x=>assessmentIds.Contains(x.Id)
                        ?x.Resolve(TacticalAssessmentStatus.Expired,revision,s.WorldSchedule.MarkerId(x.ExpirySlot+1)+".end"):x).ToArray();
                }
            }
            if(s.SchemaVersion>=Snapshot.SuppressionFireSchema) {
                var slowIds=s.SuppressionSlows.Where(x=>x.Status==SuppressionSlowStatus.Active&&x.ExpirySlot>=previousSlot&&x.ExpirySlot<nextSlot)
                    .Select(x=>x.Id).ToArray();
                if(slowIds.Length!=0) {
                    var ids=new System.Collections.Generic.HashSet<string>(slowIds,StringComparer.Ordinal);
                    s.SuppressionSlows=s.SuppressionSlows.Select(x=>ids.Contains(x.Id)
                        ?x.Expire(revision,s.WorldSchedule.MarkerId(x.ExpirySlot+1)+".end"):x).ToArray();
                }
            }
        }

        public static void ExpireStartMarker(Snapshot s,string actor,long slot,long revision)
        {
            if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema)return;
            var due=s.SoldierTacticalEffects.Where(x=>x.Status==SoldierTacticalEffectStatus.Active&&x.ExpiryPhase==SoldierTacticalEffectPhase.Start
                &&x.ExpiryActorId==actor&&x.ExpirySlot==slot).Select(x=>x.Id).ToArray();
            if(due.Length>0) {
                var ids=new System.Collections.Generic.HashSet<string>(due,StringComparer.Ordinal);
                s.SoldierTacticalEffects=s.SoldierTacticalEffects.Select(x=>ids.Contains(x.Id)
                    ?x.Resolve(SoldierTacticalEffectStatus.Expired,revision,s.WorldSchedule.MarkerId(slot)+".start"):x).ToArray();
            }
            if(s.SchemaVersion>=Snapshot.DefensiveFormationSchema) {
                string marker=s.WorldSchedule.MarkerId(slot)+".start";
                s.DefensiveFormations=s.DefensiveFormations.Select(x=>x.Active&&x.SourceActorId==actor&&x.ExpirySlot==slot
                    ?x.Expire(revision,marker):x).ToArray();
            }
        }

        public static RuleTime? NextDeadline(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema||s.WorldSchedule==null)return null;
            RuleTime[] deadlines=s.SoldierTacticalEffects.Where(x=>x.Status==SoldierTacticalEffectStatus.Active).Select(x=>
                s.WorldSchedule.Start(x.ExpiryPhase==SoldierTacticalEffectPhase.End?checked(x.ExpirySlot+1):x.ExpirySlot))
                .Concat(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema?s.TacticalAssessments.Where(x=>x.Status==TacticalAssessmentStatus.Active)
                    .Select(x=>s.WorldSchedule.Start(checked(x.ExpirySlot+1))):Array.Empty<RuleTime>())
                .Concat(s.SchemaVersion>=Snapshot.SuppressionFireSchema?s.SuppressionSlows.Where(x=>x.Status==SuppressionSlowStatus.Active)
                    .Select(x=>s.WorldSchedule.Start(checked(x.ExpirySlot+1))):Array.Empty<RuleTime>())
                .Concat(s.SchemaVersion>=Snapshot.DefensiveFormationSchema?s.DefensiveFormations.Where(x=>x.Active)
                    .Select(x=>s.WorldSchedule.Start(x.ExpirySlot)):Array.Empty<RuleTime>())
                .Where(x=>x>s.RuleClock).ToArray();
            return deadlines.Length==0?(RuleTime?)null:deadlines.Min();
        }
        private static string N(long value)=>value.ToString(CultureInfo.InvariantCulture);
    }
}
#endif
