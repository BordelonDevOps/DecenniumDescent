using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class SoldierTacticalFeatureCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.TacticalAllies.Length);
            foreach(var x in s.TacticalAllies.OrderBy(x=>x.FirstActorId,StringComparer.Ordinal).ThenBy(x=>x.SecondActorId,StringComparer.Ordinal)) {
                Text(w,x.FirstActorId);Text(w,x.SecondActorId);
            }
            w.Write(s.SoldierTacticalEffects.Length);
            foreach(var x in s.SoldierTacticalEffects.OrderBy(x=>x.ApplicationOrder)) {
                Text(w,x.Id);w.Write((int)x.Kind);Text(w,x.SourceActorId);Text(w,x.TargetActorId);Text(w,x.OriginAttackId);
                w.Write(x.ApplicationOrder);w.Write(x.AppliedRevision);w.Write(x.AppliedAt.Numerator);w.Write(x.AppliedAt.Denominator);
                Text(w,x.ExpiryActorId);w.Write(x.ExpirySlot);w.Write((int)x.ExpiryPhase);w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.ResolutionId);
            }
            w.Write(s.TacticalAttackAudits.Length);
            foreach(var x in s.TacticalAttackAudits.OrderBy(x=>x.AttackId,StringComparer.Ordinal)) {
                Text(w,x.AttackId);Text(w,x.AttackerId);Text(w,x.TargetId);Text(w,x.TechniqueFeatureId);var ids=x.ConsumedEffectIds;
                w.Write(ids.Length);foreach(string id in ids)Text(w,id);
            }
            if(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema) {
                w.Write(s.TacticalAssessments.Length);
                foreach(var x in s.TacticalAssessments.OrderBy(x=>x.AppliedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    Text(w,x.Id);Text(w,x.SourceActorId);Text(w,x.AllyActorId);Text(w,x.EnemyActorId);w.Write(x.AppliedRevision);
                    w.Write(x.AppliedAt.Numerator);w.Write(x.AppliedAt.Denominator);w.Write(x.ExpirySlot);Text(w,x.ArmorCategory);
                    w.Write(x.HasCover);w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.ResolutionId);
                }
            }
            if(s.SchemaVersion>=Snapshot.CommandStepSchema) {
                w.Write(s.CommandStepOffers.Length);
                foreach(var x in s.CommandStepOffers.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    Text(w,x.Id);Text(w,x.ActionId);Text(w,x.TurnId);Text(w,x.SoldierActorId);Text(w,x.AllyActorId);w.Write(x.TurnOrdinal);
                    w.Write(x.RoundOrdinal);w.Write(x.CreatedRevision);w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.ResolutionId);Text(w,x.MoveId);
                }
            }
            if(s.SchemaVersion>=Snapshot.SuppressionFireSchema) {
                w.Write(s.SuppressionFireVolleys.Length);
                foreach(var x in s.SuppressionFireVolleys.OrderBy(x=>x.Revision)) {
                    Text(w,x.Id);w.Write(x.Revision);w.Write(x.TurnOrdinal);Text(w,x.SourceActorId);Text(w,x.WeaponId);
                    var lots=x.AmmunitionLotIds;w.Write(lots.Length);foreach(string id in lots)Text(w,id);
                    w.Write(x.At.Numerator);w.Write(x.At.Denominator);w.Write(x.CenterX);w.Write(x.CenterY);w.Write(x.ClassLevel);w.Write(x.SaveDc);
                    var dice=x.DamageDice;w.Write(dice.Length);foreach(int die in dice)w.Write(die);w.Write(x.DamageTotal);
                    w.Write(x.DamageRandomBefore);w.Write(x.DamageRandomAfter);w.Write(x.DamageWords);
                    var targets=x.Targets;w.Write(targets.Length);foreach(var t in targets) {
                        Text(w,t.TargetActorId);w.Write(t.TargetX);w.Write(t.TargetY);w.Write(t.SaveNatural);w.Write(t.SaveModifier);w.Write(t.SaveTotal);w.Write(t.SaveSucceeded);
                        w.Write(t.Damage);w.Write(t.AfterDefense);w.Write(t.SaveRandomBefore);w.Write(t.SaveRandomAfter);w.Write(t.SaveWords);
                        w.Write(t.LifeRandomBefore);w.Write(t.LifeRandomAfter);w.Write(t.LifeWords);
                    }
                }
                w.Write(s.SuppressionSlows.Length);
                foreach(var x in s.SuppressionSlows.OrderBy(x=>x.AppliedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    Text(w,x.Id);Text(w,x.VolleyId);Text(w,x.SourceActorId);Text(w,x.TargetActorId);w.Write(x.AppliedRevision);w.Write(x.ExpirySlot);
                    w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.ResolutionId);
                }
            }
            if(s.SchemaVersion>=Snapshot.DefensiveFormationSchema) {
                w.Write(s.DefensiveFormations.Length);
                foreach(var x in s.DefensiveFormations.OrderBy(x=>x.CreatedRevision)) {
                    Text(w,x.Id);Text(w,x.SourceActorId);Text(w,x.EncounterId);Text(w,x.TurnId);w.Write(x.TurnOrdinal);
                    w.Write(x.CreatedRevision);w.Write(x.UpdatedRevision);w.Write(x.At.Numerator);w.Write(x.At.Denominator);w.Write(x.ExpirySlot);
                    w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.ResolutionId);var shifts=x.Shifts;w.Write(shifts.Length);
                    foreach(var shift in shifts) {
                        Text(w,shift.Id);w.Write(shift.OrderIndex);Text(w,shift.RecipientActorId);w.Write((int)shift.Status);w.Write(shift.UpdatedRevision);
                        w.Write(shift.DecisionRevision);Text(w,shift.DecisionId);Text(w,shift.MoveId);w.Write(shift.ResolvedRevision);Text(w,shift.ResolutionId);
                    }
                }
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.TacticalAllies=new TacticalAllyRecord[Count(r,SoldierTacticalFeatureValidation.MaxAllies)];
            for(int i=0;i<s.TacticalAllies.Length;i++)s.TacticalAllies[i]=new TacticalAllyRecord(Text(r),Text(r));
            s.SoldierTacticalEffects=new SoldierTacticalEffectRecord[Count(r,SoldierTacticalFeatureValidation.MaxEffects)];
            for(int i=0;i<s.SoldierTacticalEffects.Length;i++) {
                string id=Text(r);var kind=(SoldierTacticalEffectKind)r.ReadInt32();string source=Text(r),target=Text(r),attack=Text(r);
                long order=r.ReadInt64(),revision=r.ReadInt64();var applied=new RuleTime(r.ReadInt64(),r.ReadInt64());string expiryActor=Text(r);
                long expirySlot=r.ReadInt64();var phase=(SoldierTacticalEffectPhase)r.ReadInt32();var status=(SoldierTacticalEffectStatus)r.ReadInt32();
                long resolved=r.ReadInt64();string resolution=Text(r);
                s.SoldierTacticalEffects[i]=new SoldierTacticalEffectRecord(id,kind,source,target,attack,order,revision,applied,
                    expiryActor,expirySlot,phase,status,resolved,resolution);
            }
            s.TacticalAttackAudits=new TacticalAttackAuditRecord[Count(r,SoldierTacticalFeatureValidation.MaxAttackAudits)];
            for(int i=0;i<s.TacticalAttackAudits.Length;i++) {
                string attack=Text(r),attacker=Text(r),target=Text(r),feature=Text(r);var used=new string[Count(r,64)];
                for(int j=0;j<used.Length;j++)used[j]=Text(r);
                s.TacticalAttackAudits[i]=new TacticalAttackAuditRecord(attack,attacker,target,feature,used);
            }
            if(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema) {
                s.TacticalAssessments=new TacticalAssessmentRecord[Count(r,SoldierTacticalFeatureValidation.MaxAssessments)];
                for(int i=0;i<s.TacticalAssessments.Length;i++) {
                    string id=Text(r),source=Text(r),ally=Text(r),enemy=Text(r);long appliedRevision=r.ReadInt64();
                    var applied=new RuleTime(r.ReadInt64(),r.ReadInt64());long expiry=r.ReadInt64();string armor=Text(r);
                    bool cover=Bool(r);var status=(TacticalAssessmentStatus)r.ReadInt32();long resolved=r.ReadInt64();string resolution=Text(r);
                    s.TacticalAssessments[i]=new TacticalAssessmentRecord(id,source,ally,enemy,appliedRevision,applied,expiry,armor,cover,status,resolved,resolution);
                }
            }
            if(s.SchemaVersion>=Snapshot.CommandStepSchema) {
                s.CommandStepOffers=new CommandStepOfferRecord[Count(r,128)];
                for(int i=0;i<s.CommandStepOffers.Length;i++) {
                    string id=Text(r),action=Text(r),turn=Text(r),soldier=Text(r),ally=Text(r);int ordinal=r.ReadInt32(),round=r.ReadInt32();
                    long created=r.ReadInt64();var status=(CommandStepOfferStatus)r.ReadInt32();long resolved=r.ReadInt64();string resolution=Text(r),move=Text(r);
                    s.CommandStepOffers[i]=new CommandStepOfferRecord(id,action,turn,soldier,ally,ordinal,round,created,status,resolved,resolution,move);
                }
            }
            if(s.SchemaVersion>=Snapshot.SuppressionFireSchema) {
                s.SuppressionFireVolleys=new SuppressionFireVolleyRecord[Count(r,128)];
                for(int i=0;i<s.SuppressionFireVolleys.Length;i++) {
                    string id=Text(r);long revision=r.ReadInt64();int ordinal=r.ReadInt32();string source=Text(r),weapon=Text(r);
                    var lots=new string[Count(r,3)];for(int j=0;j<lots.Length;j++)lots[j]=Text(r);
                    var at=new RuleTime(r.ReadInt64(),r.ReadInt64());int x=r.ReadInt32(),y=r.ReadInt32(),level=r.ReadInt32(),dc=r.ReadInt32();
                    var dice=new int[Count(r,20)];for(int j=0;j<dice.Length;j++)dice[j]=r.ReadInt32();long total=r.ReadInt64();
                    uint damageBefore=r.ReadUInt32(),damageAfter=r.ReadUInt32();long damageWords=r.ReadInt64();
                    var targets=new SuppressionFireTargetResult[Count(r,3)];for(int j=0;j<targets.Length;j++) {
                        string target=Text(r);int targetX=r.ReadInt32(),targetY=r.ReadInt32();int natural=r.ReadInt32(),modifier=r.ReadInt32();long saveTotal=r.ReadInt64();bool success=Bool(r);
                        long damage=r.ReadInt64(),afterDefense=r.ReadInt64();uint saveBefore=r.ReadUInt32(),saveAfter=r.ReadUInt32();long saveWords=r.ReadInt64();
                        uint lifeBefore=r.ReadUInt32(),lifeAfter=r.ReadUInt32();long lifeWords=r.ReadInt64();
                        targets[j]=new SuppressionFireTargetResult(target,targetX,targetY,natural,modifier,saveTotal,success,damage,afterDefense,
                            saveBefore,saveAfter,saveWords,lifeBefore,lifeAfter,lifeWords);
                    }
                    s.SuppressionFireVolleys[i]=new SuppressionFireVolleyRecord(id,revision,ordinal,source,weapon,lots,at,x,y,level,dc,dice,total,
                        damageBefore,damageAfter,damageWords,targets);
                }
                s.SuppressionSlows=new SuppressionSlowRecord[Count(r,384)];
                for(int i=0;i<s.SuppressionSlows.Length;i++) {
                    string id=Text(r),volley=Text(r),source=Text(r),target=Text(r);long applied=r.ReadInt64(),expiry=r.ReadInt64();
                    var status=(SuppressionSlowStatus)r.ReadInt32();long resolved=r.ReadInt64();string resolution=Text(r);
                    s.SuppressionSlows[i]=new SuppressionSlowRecord(id,volley,source,target,applied,expiry,status,resolved,resolution);
                }
            }
            if(s.SchemaVersion>=Snapshot.DefensiveFormationSchema) {
                s.DefensiveFormations=new DefensiveFormationActivationRecord[Count(r,DefensiveFormationValidation.MaxActivations)];
                for(int i=0;i<s.DefensiveFormations.Length;i++) {
                    string id=Text(r),source=Text(r),encounter=Text(r),turn=Text(r);int ordinal=r.ReadInt32();
                    long created=r.ReadInt64(),updated=r.ReadInt64();var at=new RuleTime(r.ReadInt64(),r.ReadInt64());long expiry=r.ReadInt64();
                    var status=(DefensiveFormationStatus)r.ReadInt32();long resolved=r.ReadInt64();string resolution=Text(r);
                    var shifts=new DefensiveFormationShiftRecord[Count(r,3)];
                    for(int j=0;j<shifts.Length;j++) {
                        string shiftId=Text(r);int order=r.ReadInt32();string recipient=Text(r);var shiftStatus=(DefensiveFormationShiftStatus)r.ReadInt32();
                        long shiftUpdated=r.ReadInt64(),decisionRevision=r.ReadInt64();string decision=Text(r),move=Text(r);
                        long shiftResolved=r.ReadInt64();string shiftResolution=Text(r);
                        shifts[j]=new DefensiveFormationShiftRecord(shiftId,order,recipient,shiftStatus,shiftUpdated,decisionRevision,decision,move,shiftResolved,shiftResolution);
                    }
                    s.DefensiveFormations[i]=new DefensiveFormationActivationRecord(id,source,encounter,turn,ordinal,created,updated,at,expiry,shifts,status,resolved,resolution);
                }
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid Soldier tactical feature count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid Soldier tactical feature flag.");return b==1;}
        private static void Text(BinaryWriter w,string x){byte[] b=Utf8.GetBytes(x);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
