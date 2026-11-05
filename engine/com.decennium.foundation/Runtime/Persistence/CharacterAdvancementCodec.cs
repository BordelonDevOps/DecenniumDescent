using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class CharacterAdvancementCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.CharacterMilestones.Length);
            foreach(var m in s.CharacterMilestones.OrderBy(x=>x.AwardedRevision).ThenBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.MilestoneId,StringComparer.Ordinal)) {
                Text(w,m.MilestoneId);Text(w,m.ActorId);w.Write(m.AwardedRevision);w.Write(m.ConsumedRevision);
            }
            w.Write(s.CharacterHitDice.Length);
            foreach(var d in s.CharacterHitDice.OrderBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.LevelOrdinal)) {
                Text(w,d.ActorId);w.Write(d.LevelOrdinal);Text(w,d.ClassName);w.Write(d.DieSize);w.Write(d.Spent);
            }
            w.Write(s.CharacterFeatureGrants.Length);
            foreach(var g in s.CharacterFeatureGrants.OrderBy(x=>x.GrantedRevision).ThenBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.FeatureId,StringComparer.Ordinal).ThenBy(x=>x.Origin)) {
                Text(w,g.ActorId);Text(w,g.FeatureId);Text(w,g.ClassName);w.Write(g.ClassLevel);Text(w,g.MilestoneId);w.Write(g.GrantedRevision);
                if(s.SchemaVersion>=Snapshot.SharedBonusActionSchema)w.Write((int)g.Origin);
            }
            w.Write(s.CharacterAdvancements.Length);
            foreach(var a in s.CharacterAdvancements.OrderBy(x=>x.Revision)) {
                Text(w,a.ActorId);Text(w,a.MilestoneId);w.Write(a.Revision);w.Write(a.PreviousTotalLevel);w.Write(a.NewTotalLevel);
                Text(w,a.ClassName);w.Write(a.ClassLevel);w.Write(a.BaseHpGain);w.Write((int)a.HitPointMethod);
                w.Write(a.MaximumHpBefore);w.Write(a.MaximumHpAfter);w.Write(a.CurrentHpBefore);w.Write(a.CurrentHpAfter);
                if(s.SchemaVersion>=Snapshot.CharacterAdvancementHistorySchema) {
                    w.Write(a.SelectedFeatureIds.Count);foreach(var feature in a.SelectedFeatureIds)Text(w,feature);
                } else { Text(w,a.FeatureOne);Text(w,a.FeatureTwo); }
            }
            w.Write(s.CharacterFeatureRuntime.Length);
            foreach(var f in s.CharacterFeatureRuntime.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,f.ActorId);w.Write(f.LastRegularStart);w.Write(f.BonusActionAvailable);w.Write(f.RepositionRechargeRemaining);
                w.Write(f.RepositionTurnOrdinal);w.Write(f.RepositionBudgetRemaining);
                if(s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema){w.Write(f.WarningShotRechargeRemaining);w.Write(f.CoveringFireRechargeRemaining);}
                if(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema)w.Write(f.TacticalAssessmentRechargeRemaining);
                if(s.SchemaVersion>=Snapshot.SuppressionFireSchema)w.Write(f.SuppressionFireRechargeRemaining);
            }
            w.Write(s.TacticalCovers.Length);
            foreach(var c in s.TacticalCovers.OrderBy(x=>x.Id,StringComparer.Ordinal)){Text(w,c.Id);w.Write(c.X);w.Write(c.Y);}
            if(s.SchemaVersion>=Snapshot.SharedBonusActionSchema) {
                w.Write(s.BonusActions.Length);
                foreach(var b in s.BonusActions.OrderBy(x=>x.ActorId,StringComparer.Ordinal)){Text(w,b.ActorId);w.Write(b.LastRegularStart);w.Write(b.Available);}
            }
            if(s.SchemaVersion>=Snapshot.SoldierInitialLoadoutSchema) {
                w.Write(s.InitialClassSelections.Length);
                foreach(var selection in s.InitialClassSelections.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                    Text(w,selection.ActorId);Text(w,selection.ClassName);w.Write(selection.ClassLevel);Text(w,selection.SourceRevision);
                    w.Write(selection.SelectedFeatureIds.Count);
                    foreach(var feature in selection.SelectedFeatureIds)Text(w,feature);
                }
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.CharacterMilestones=new CharacterMilestoneRecord[Count(r,256)];
            for(int i=0;i<s.CharacterMilestones.Length;i++)s.CharacterMilestones[i]=new CharacterMilestoneRecord(Text(r),Text(r),r.ReadInt64(),r.ReadInt64());
            s.CharacterHitDice=new CharacterHitDieRecord[Count(r,1280)];
            for(int i=0;i<s.CharacterHitDice.Length;i++)s.CharacterHitDice[i]=new CharacterHitDieRecord(Text(r),r.ReadInt32(),Text(r),r.ReadInt32(),Bool(r));
            s.CharacterFeatureGrants=new CharacterFeatureGrantRecord[Count(r,256)];
            for(int i=0;i<s.CharacterFeatureGrants.Length;i++) {
                string actor=Text(r),feature=Text(r),className=Text(r);int level=r.ReadInt32();string milestone=Text(r);long revision=r.ReadInt64();
                var origin=s.SchemaVersion>=Snapshot.SharedBonusActionSchema?(CharacterFeatureGrantOrigin)r.ReadInt32():CharacterFeatureGrantOrigin.SelectedCard;
                s.CharacterFeatureGrants[i]=new CharacterFeatureGrantRecord(actor,feature,className,level,milestone,revision,origin);
            }
            s.CharacterAdvancements=new CharacterAdvancementRecord[Count(r,128)];
            for(int i=0;i<s.CharacterAdvancements.Length;i++) {
                string actor=Text(r),milestone=Text(r);long revision=r.ReadInt64();int previous=r.ReadInt32(),next=r.ReadInt32();
                string className=Text(r);int classLevel=r.ReadInt32(),gain=r.ReadInt32();var method=(HitPointGainMethod)r.ReadInt32();
                long maximumBefore=r.ReadInt64(),maximumAfter=r.ReadInt64(),currentBefore=r.ReadInt64(),currentAfter=r.ReadInt64();
                if(s.SchemaVersion>=Snapshot.CharacterAdvancementHistorySchema) {
                    var selected=new string[Count(r,4)];for(int j=0;j<selected.Length;j++)selected[j]=Text(r);
                    s.CharacterAdvancements[i]=new CharacterAdvancementRecord(actor,milestone,revision,previous,next,className,classLevel,gain,method,
                        maximumBefore,maximumAfter,currentBefore,currentAfter,selected);
                } else s.CharacterAdvancements[i]=new CharacterAdvancementRecord(actor,milestone,revision,previous,next,className,classLevel,gain,method,
                    maximumBefore,maximumAfter,currentBefore,currentAfter,Text(r),Text(r));
            }
            s.CharacterFeatureRuntime=new CharacterFeatureRuntimeRecord[Count(r,64)];
            for(int i=0;i<s.CharacterFeatureRuntime.Length;i++) {
                string actor=Text(r);int start=r.ReadInt32();bool bonus=Bool(r);int repositionRecharge=r.ReadInt32(),turn=r.ReadInt32();long budget=r.ReadInt64();
                int warning=s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema?r.ReadInt32():0;
                int covering=s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema?r.ReadInt32():0;
                int assessment=s.SchemaVersion>=Snapshot.TacticalAssessmentSchema?r.ReadInt32():0;
                int suppression=s.SchemaVersion>=Snapshot.SuppressionFireSchema?r.ReadInt32():0;
                s.CharacterFeatureRuntime[i]=new CharacterFeatureRuntimeRecord(actor,start,bonus,repositionRecharge,turn,budget,warning,covering,assessment,suppression);
            }
            s.TacticalCovers=new TacticalCoverRecord[Count(r,64)];
            for(int i=0;i<s.TacticalCovers.Length;i++)s.TacticalCovers[i]=new TacticalCoverRecord(Text(r),r.ReadInt32(),r.ReadInt32());
            if(s.SchemaVersion>=Snapshot.SharedBonusActionSchema) {
                s.BonusActions=new ActorBonusActionRecord[Count(r,64)];
                for(int i=0;i<s.BonusActions.Length;i++)s.BonusActions[i]=new ActorBonusActionRecord(Text(r),r.ReadInt32(),Bool(r));
            }
            if(s.SchemaVersion>=Snapshot.SoldierInitialLoadoutSchema) {
                s.InitialClassSelections=new CharacterInitialClassSelectionRecord[Count(r,64)];
                for(int i=0;i<s.InitialClassSelections.Length;i++) {
                    string actor=Text(r),className=Text(r);int level=r.ReadInt32();string sourceRevision=Text(r);
                    var features=new string[Count(r,16)];for(int j=0;j<features.Length;j++)features[j]=Text(r);
                    s.InitialClassSelections[i]=new CharacterInitialClassSelectionRecord(actor,className,level,sourceRevision,features);
                }
            }
        }
        public static void WriteInitialBuild(BinaryWriter w,Snapshot s)
        {
            w.Write(s.InitialCharacterLoadouts.Length);
            foreach(var x in s.InitialCharacterLoadouts.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,x.ActorId);Text(w,x.SourceRevision);w.Write(x.OptionalPointBuySpent);Text(w,x.SelectionProfileId);
                w.Write(x.SelectedSkillIds.Count);foreach(var skill in x.SelectedSkillIds)Text(w,skill);
                w.Write(x.SavingThrowProficiencyIds.Count);foreach(var ability in x.SavingThrowProficiencyIds)Text(w,ability);
                Text(w,x.ChainMailId);Text(w,x.ShieldId);Text(w,x.DaggerId);Text(w,x.PackId);Text(w,x.CrossbowId);Text(w,x.AmmunitionLotId);
                Text(w,x.RationsId);Text(w,x.WaterskinId);Text(w,x.WaterId);w.Write(x.InitialPackGroundX);w.Write(x.InitialPackGroundY);
            }
            w.Write(s.ShieldStationarity.Length);
            foreach(var x in s.ShieldStationarity.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,x.ActorId);w.Write(x.LastRegularStart);w.Write(x.MovedSinceRegularStart);
            }
        }
        public static void ReadInitialBuild(BinaryReader r,Snapshot s)
        {
            s.InitialCharacterLoadouts=new CharacterInitialLoadoutRecord[Count(r,64)];
            for(int i=0;i<s.InitialCharacterLoadouts.Length;i++) {
                string actor=Text(r),source=Text(r);int pointBuy=r.ReadInt32();string profile=Text(r);
                var skills=new string[Count(r,16)];for(int j=0;j<skills.Length;j++)skills[j]=Text(r);
                var saves=new string[Count(r,6)];for(int j=0;j<saves.Length;j++)saves[j]=Text(r);
                string chainMail=Text(r),shield=Text(r),dagger=Text(r),pack=Text(r),crossbow=Text(r),ammunition=Text(r);
                string rations=Text(r),skin=Text(r),water=Text(r);int x=r.ReadInt32(),y=r.ReadInt32();
                s.InitialCharacterLoadouts[i]=new CharacterInitialLoadoutRecord(actor,source,pointBuy,profile,skills,saves,
                    chainMail,shield,dagger,pack,crossbow,ammunition,rations,skin,water,x,y);
            }
            s.ShieldStationarity=new ShieldStationarityRecord[Count(r,64)];
            for(int i=0;i<s.ShieldStationarity.Length;i++)s.ShieldStationarity[i]=new ShieldStationarityRecord(Text(r),r.ReadInt32(),Bool(r));
        }
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid advancement flag.");return b==1;}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid advancement count.");return n;}
        private static void Text(BinaryWriter w,string text){byte[] b=Utf8.GetBytes(text);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
