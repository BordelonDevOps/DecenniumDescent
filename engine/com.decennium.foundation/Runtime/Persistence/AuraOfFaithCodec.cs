using System;
using System.IO;

namespace Decennium.Foundation
{
    internal static class AuraOfFaithCodec
    {
        internal static void Write(BinaryWriter w,BishopEntryRecord entry)
        {
            w.Write(entry.AuraSaves.Count);
            foreach(var x in entry.AuraSaves) {
                Text(w,x.Id);Text(w,x.CauseId);w.Write(x.Revision);Time(w,x.At);w.Write((int)x.Consumer);Qualification(w,x.Qualification);
                w.Write(x.BaseModifier);w.Write(x.OtherTemporaryBonus);w.Write(x.Dc);w.Write(x.Natural);w.Write(x.AutomaticFailure);w.Write(x.Success);
                w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
            }
            w.Write(entry.AuraHealing.Count);
            foreach(var x in entry.AuraHealing) {
                Text(w,x.RiteCommandId);w.Write(x.Revision);Time(w,x.At);Qualification(w,x.Qualification);
                w.Write(x.BaseGain);w.Write(x.HpBefore);w.Write(x.Potential);w.Write(x.HpAfter);
            }
        }
        internal static void Read(BinaryReader r,out AuraOfFaithSaveRecord[] saves,out AuraOfFaithHealingRecord[] healing)
        {
            saves=new AuraOfFaithSaveRecord[SnapshotCodec.ReadCount(r,2048)];
            for(int i=0;i<saves.Length;i++)saves[i]=new AuraOfFaithSaveRecord(Text(r),Text(r),r.ReadInt64(),Time(r),
                (AuraSaveConsumer)r.ReadInt32(),Qualification(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt64(),r.ReadInt32(),
                SnapshotCodec.ReadBool(r),SnapshotCodec.ReadBool(r),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
            healing=new AuraOfFaithHealingRecord[SnapshotCodec.ReadCount(r,128)];
            for(int i=0;i<healing.Length;i++)healing[i]=new AuraOfFaithHealingRecord(Text(r),r.ReadInt64(),Time(r),Qualification(r),
                r.ReadInt64(),r.ReadInt64(),r.ReadInt64(),r.ReadInt64());
        }
        private static void Qualification(BinaryWriter w,AuraOfFaithQualification q)
        {
            w.Write(q.AcquiredRevision);Text(w,q.TargetId);w.Write(q.OwnerConscious);w.Write(q.Allied);w.Write(q.RecipientConscious);w.Write(q.Perceived);
            Quantity(w,q.OwnerX);Quantity(w,q.OwnerY);Quantity(w,q.TargetX);Quantity(w,q.TargetY);
        }
        private static AuraOfFaithQualification Qualification(BinaryReader r)=>new AuraOfFaithQualification(r.ReadInt64(),Text(r),
            SnapshotCodec.ReadBool(r),SnapshotCodec.ReadBool(r),SnapshotCodec.ReadBool(r),SnapshotCodec.ReadBool(r),Quantity(r),Quantity(r),Quantity(r),Quantity(r));
        private static void Quantity(BinaryWriter w,RuleQuantity q){w.Write(q.Numerator);w.Write(q.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        private static void Time(BinaryWriter w,RuleTime at){w.Write(at.Numerator);w.Write(at.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Text(BinaryWriter w,string text)=>SnapshotCodec.WriteText(w,text);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
    }
}
