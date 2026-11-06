using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ProspectingCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { var bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r)
        { int n=r.ReadInt32(); if(n<0||n>512)throw new InvalidDataException("Invalid prospecting text length.");var b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b); }
        private static bool Bool(BinaryReader r) { byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid prospecting boolean.");return b==1; }
        private static int Count(BinaryReader r) { int n=r.ReadInt32();if(n<0||n>ProspectingValidation.MaxRecords)throw new InvalidDataException("Invalid prospecting record count.");return n; }
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void NullableTime(BinaryWriter w,RuleTime? value){w.Write(value.HasValue);if(value.HasValue)Time(w,value.Value);}
        private static RuleTime? NullableTime(BinaryReader r)=>Bool(r)?Time(r):(RuleTime?)null;
        private static void Ids(BinaryWriter w,string[] values){w.Write(values.Length);foreach(string id in values)Text(w,id);}
        private static string[] Ids(BinaryReader r){var values=new string[Count(r)];for(int i=0;i<values.Length;i++)values[i]=Text(r);return values;}

        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.ProspectingPatches.Length);
            foreach(var x in s.ProspectingPatches.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.OwnerId);Text(w,x.SiteId);w.Write(x.X);w.Write(x.Y);Text(w,x.CurrentExposureId);
            }
            w.Write(s.ProspectingExposures.Length);
            foreach(var x in s.ProspectingExposures.OrderBy(x=>x.ChangedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.PatchId);Text(w,x.ParentExposureId);Text(w,x.ChangeCauseId);Time(w,x.ChangedAt);
                w.Write(x.AreaSquareFeet);w.Write(x.Exposed);w.Write(x.Accessible);w.Write((int)x.Signs);w.Write((int)x.Method);
                w.Write(x.RequiredHands);Text(w,x.HazardDeclarationId);Ids(w,x.RequiredImplementIds);Ids(w,x.FindingIds);
            }
            w.Write(s.ProspectingAttempts.Length);
            foreach(var x in s.ProspectingAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ActorId);Text(w,x.PatchId);Text(w,x.ExposureId);Text(w,x.MethodId);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);Time(w,x.WorkDone);w.Write((int)x.Status);
                w.Write(x.WisdomModifier);w.Write(x.ProficiencyRank);w.Write(x.ProficiencyBonus);w.Write(x.CheckDc);
                NullableTime(w,x.ResolvedAt);NullableTime(w,x.ClosedAt);w.Write((int)x.Degree);w.Write((int)x.DiceSelection);
                w.Write(x.FirstDie);w.Write(x.SecondDie);w.Write(x.Natural);w.Write(x.CheckModifier);
                w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);Text(w,x.InvalidationCauseId);Ids(w,x.FindingIds);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.ProspectingPatches=new ProspectingPatchRecord[Count(r)];
            for(int i=0;i<s.ProspectingPatches.Length;i++)s.ProspectingPatches[i]=new ProspectingPatchRecord(
                Text(r),Text(r),Text(r),r.ReadInt32(),r.ReadInt32(),Text(r));
            s.ProspectingExposures=new ProspectingExposureRecord[Count(r)];
            for(int i=0;i<s.ProspectingExposures.Length;i++) {
                string id=Text(r),patch=Text(r),parent=Text(r),cause=Text(r);RuleTime at=Time(r);int area=r.ReadInt32();
                bool exposed=Bool(r),accessible=Bool(r);var signs=(ProspectingSignSeverity)r.ReadInt32();
                var method=(ProspectingMethodKind)r.ReadInt32();int hands=r.ReadInt32();string hazard=Text(r);
                s.ProspectingExposures[i]=new ProspectingExposureRecord(id,patch,parent,cause,at,area,exposed,accessible,
                    signs,method,hands,hazard,Ids(r),Ids(r));
            }
            s.ProspectingAttempts=new ProspectingAttemptRecord[Count(r)];
            for(int i=0;i<s.ProspectingAttempts.Length;i++) {
                string id=Text(r),actor=Text(r),patch=Text(r),exposure=Text(r),method=Text(r);
                RuleTime started=Time(r),updated=Time(r),work=Time(r);var status=(ProspectingAttemptStatus)r.ReadInt32();
                int wisdom=r.ReadInt32(),rank=r.ReadInt32(),pb=r.ReadInt32(),dc=r.ReadInt32();
                RuleTime? resolved=NullableTime(r),closed=NullableTime(r);var degree=(MiningCheckDegree)r.ReadInt32();
                var selection=(MiningDiceSelection)r.ReadInt32();int first=r.ReadInt32(),second=r.ReadInt32(),natural=r.ReadInt32();
                int modifier=r.ReadInt32();uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();string cause=Text(r);
                s.ProspectingAttempts[i]=new ProspectingAttemptRecord(id,actor,patch,exposure,method,started,updated,work,status,
                    wisdom,rank,pb,dc,resolved,closed,degree,selection,first,second,natural,modifier,before,after,words,cause,Ids(r));
            }
        }
    }
}
