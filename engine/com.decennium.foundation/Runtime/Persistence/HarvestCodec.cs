using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class HarvestCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value)
        {var bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r)
        {int length=r.ReadInt32();if(length<0||length>512)throw new InvalidDataException("Invalid harvest text length.");
            var bytes=r.ReadBytes(length);if(bytes.Length!=length)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static int Count(BinaryReader r)
        {int count=r.ReadInt32();if(count<0||count>HarvestValidation.MaxRecords)throw new InvalidDataException("Invalid harvest record count.");return count;}
        public static void Write(BinaryWriter w,Snapshot s,int schemaVersion)
        {
            w.Write(s.HarvestDonors.Length);
            foreach(var x in s.HarvestDonors.OrderBy(x=>x.CreatureId,StringComparer.Ordinal)) {
                Text(w,x.CreatureId);Text(w,x.LifecycleEventId);Time(w,x.DeathAt);w.Write((int)x.OriginRestriction);
                Text(w,x.AnatomyProfileId);Text(w,x.OwnerId);w.Write(x.OriginalMassPounds.Numerator);w.Write(x.OriginalMassPounds.Denominator);
            }
            w.Write(s.HarvestManifests.Length);
            foreach(var x in s.HarvestManifests.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.CreatureId);Text(w,x.AnatomyVersionId);w.Write((int)x.Size);Time(w,x.CreatedAt);
                w.Write(x.RequiredDc);w.Write(x.FullTimeSeconds);w.Write(x.BaseYieldUnits);Text(w,x.SiteId);Text(w,x.ToolkitId);
                Text(w,x.KnifeId);Text(w,x.ContainerId);Text(w,x.WorkSurfaceId);
                if(schemaVersion>=Snapshot.HarvestManifestSchema) {
                    int[] dice=x.BaseYieldDice;w.Write(dice.Length);foreach(int face in dice)w.Write(face);
                    w.Write(x.YieldRandomBefore);w.Write(x.YieldRandomAfter);w.Write(x.YieldWordsConsumed);
                }
            }
            w.Write(s.HarvestCategories.Length);
            foreach(var x in s.HarvestCategories.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ManifestId);Text(w,x.CategoryId);w.Write(x.AllocationUnits);
                var ids=x.UnitIds.OrderBy(y=>y,StringComparer.Ordinal).ToArray();w.Write(ids.Length);foreach(string id in ids)Text(w,id);
            }
            w.Write(s.HarvestUnits.Length);
            foreach(var x in s.HarvestUnits.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ManifestId);Text(w,x.CategoryId);Text(w,x.MaterialId);w.Write(x.Tier);
                w.Write(x.MassPounds.Numerator);w.Write(x.MassPounds.Denominator);w.Write(x.ValueCopper.HasValue);
                if(x.ValueCopper.HasValue)w.Write(x.ValueCopper.Value);w.Write((int)x.Condition);w.Write((int)x.Status);
                w.Write(x.PreservationIntervalSeconds);Time(w,x.OriginAt);
            }
            w.Write(s.HarvestAttempts.Length);
            foreach(var x in s.HarvestAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.WorkerId);Text(w,x.ManifestId);Text(w,x.CategoryId);Text(w,x.UnitId);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);Time(w,x.Duration);Time(w,x.WorkDone);w.Write((int)x.Status);
                w.Write(x.AbilityModifier);w.Write(x.ProficiencyRank);w.Write(x.ProficiencyBonus);w.Write(x.CheckDc);
                w.Write(x.CompletedAt.HasValue);if(x.CompletedAt.HasValue)Time(w,x.CompletedAt.Value);
                w.Write((int)x.Degree);w.Write((int)x.DiceSelection);w.Write(x.FirstDie);w.Write(x.SecondDie);w.Write(x.Natural);
                w.Write(x.CheckModifier);w.Write(x.D4Rolled);w.Write(x.DamageApplied);Text(w,x.AccidentDamageType);w.Write(x.WoundRoll);w.Write(x.InjuryRoll);
                w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
                if(schemaVersion>=Snapshot.HarvestManifestSchema) {
                    string[] categories=x.SelectedCategoryIds;w.Write(categories.Length);foreach(string category in categories)Text(w,category);
                    string[] units=x.SelectedUnitIds;w.Write(units.Length);foreach(string unit in units)Text(w,unit);
                    Text(w,x.FailureVictimPreference);Text(w,x.CriticalRecoveryPreference);
                }
            }
        }
        public static void Read(BinaryReader r,Snapshot s,int schemaVersion)
        {
            s.HarvestDonors=new HarvestDonorRecord[Count(r)];
            for(int i=0;i<s.HarvestDonors.Length;i++)s.HarvestDonors[i]=new HarvestDonorRecord(Text(r),Text(r),Time(r),
                (HarvestOriginRestriction)r.ReadInt32(),Text(r),Text(r),new RuleQuantity(r.ReadInt64(),r.ReadInt64()));
            s.HarvestManifests=new HarvestManifestRecord[Count(r)];
            for(int i=0;i<s.HarvestManifests.Length;i++) {
                string id=Text(r),creature=Text(r),anatomy=Text(r);var size=(HarvestSize)r.ReadInt32();RuleTime created=Time(r);
                int dc=r.ReadInt32(),seconds=r.ReadInt32(),yieldUnits=r.ReadInt32();string site=Text(r),toolkit=Text(r),knife=Text(r),container=Text(r),surface=Text(r);
                HarvestYieldResolution yield=null;
                if(schemaVersion>=Snapshot.HarvestManifestSchema) {
                    int count=Count(r);if(count>8)throw new InvalidDataException("Invalid harvest yield die count.");
                    var faces=new int[count];for(int j=0;j<count;j++)faces[j]=r.ReadInt32();
                    uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                    yield=new HarvestYieldResolution(size,yieldUnits,faces,before,after,words);
                }
                s.HarvestManifests[i]=new HarvestManifestRecord(id,creature,anatomy,size,created,dc,seconds,yieldUnits,
                    site,toolkit,knife,container,surface,yield);
            }
            s.HarvestCategories=new HarvestCategoryRecord[Count(r)];
            for(int i=0;i<s.HarvestCategories.Length;i++) {
                string id=Text(r),manifest=Text(r),category=Text(r);int allocation=r.ReadInt32(),count=Count(r);
                var units=new string[count];for(int j=0;j<count;j++)units[j]=Text(r);
                s.HarvestCategories[i]=new HarvestCategoryRecord(id,manifest,category,allocation,units);
            }
            s.HarvestUnits=new HarvestMaterialUnitRecord[Count(r)];
            for(int i=0;i<s.HarvestUnits.Length;i++) {
                string id=Text(r),manifest=Text(r),category=Text(r),material=Text(r);int tier=r.ReadInt32();
                var mass=new RuleQuantity(r.ReadInt64(),r.ReadInt64());long? value=r.ReadBoolean()?r.ReadInt64():(long?)null;
                s.HarvestUnits[i]=new HarvestMaterialUnitRecord(id,manifest,category,material,tier,mass,value,
                    (HarvestUnitCondition)r.ReadInt32(),(HarvestUnitStatus)r.ReadInt32(),r.ReadInt32(),Time(r));
            }
            s.HarvestAttempts=new HarvestAttemptRecord[Count(r)];
            for(int i=0;i<s.HarvestAttempts.Length;i++) {
                string id=Text(r),worker=Text(r),manifest=Text(r),category=Text(r),unit=Text(r);
                RuleTime start=Time(r),updated=Time(r),duration=Time(r),done=Time(r);var status=(HarvestAttemptStatus)r.ReadInt32();
                int ability=r.ReadInt32(),rank=r.ReadInt32(),proficiency=r.ReadInt32(),dc=r.ReadInt32();
                RuleTime? completed=r.ReadBoolean()?Time(r):(RuleTime?)null;var degree=(HarvestCheckDegree)r.ReadInt32();
                var selection=(HarvestDiceSelection)r.ReadInt32();int first=r.ReadInt32(),second=r.ReadInt32(),natural=r.ReadInt32();
                int modifier=r.ReadInt32(),d4=r.ReadInt32();long damage=r.ReadInt64();string damageType=Text(r);int wound=r.ReadInt32(),injury=r.ReadInt32();
                uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                string[] categories=null,units=null;string failurePreference="",criticalPreference="";
                if(schemaVersion>=Snapshot.HarvestManifestSchema) {
                    int categoryCount=Count(r);if(categoryCount<1)throw new InvalidDataException("Invalid selected harvest category count.");
                    categories=new string[categoryCount];for(int j=0;j<categoryCount;j++)categories[j]=Text(r);
                    int unitCount=Count(r);if(unitCount<1)throw new InvalidDataException("Invalid selected harvest unit count.");
                    units=new string[unitCount];for(int j=0;j<unitCount;j++)units[j]=Text(r);
                    failurePreference=Text(r);criticalPreference=Text(r);
                }
                s.HarvestAttempts[i]=new HarvestAttemptRecord(id,worker,manifest,category,unit,start,updated,duration,done,status,
                    ability,rank,proficiency,dc,completed,degree,selection,first,second,natural,modifier,d4,damage,damageType,wound,injury,before,after,words,
                    categories,units,failurePreference,criticalPreference);
            }
        }
    }
}
