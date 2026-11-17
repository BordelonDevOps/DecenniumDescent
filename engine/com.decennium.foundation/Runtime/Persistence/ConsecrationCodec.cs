using System;
using System.IO;

namespace Decennium.Foundation
{
    internal static class ConsecrationCodec
    {
        internal static void Write(BinaryWriter w, ConsecrationRecord record)
        {
            Text(w,record.PredecessorFingerprint); Text(w,record.RosterSource);
            w.Write(record.HumanoidActors.Count);
            foreach(string actor in record.HumanoidActors) { Text(w,actor); Text(w,"Humanoid"); Text(w,"Living"); }
            w.Write(record.Zones.Count);
            foreach(var x in record.Zones) {
                Text(w,x.CommandId); w.Write(x.Revision); Text(w,x.OwnerId); Text(w,x.SourceId); Text(w,x.SourceRevision); Text(w,x.AreaId);
                w.Write(x.X); w.Write(x.Y); Time(w,x.At); w.Write(x.InInitiative); Text(w,x.EpochId); w.Write(x.LocalStart);
                Time(w,x.ExpiresAt); w.Write(x.RpBefore); w.Write((int)x.End); w.Write(x.EndRevision); Time(w,x.EndAt);
            }
            w.Write(record.Healing.Count);
            foreach(var x in record.Healing) {
                Text(w,x.RiteCommandId); Text(w,x.ZoneCommandId); w.Write(x.Revision); Time(w,x.At);
                Text(w,x.OwnerId); Text(w,x.TargetId); Quantity(w,x.TargetX); Quantity(w,x.TargetY);
                w.Write(x.HpBefore); w.Write(x.Potential); w.Write(x.HpAfter);
            }
            w.Write(record.Attacks.Count);
            foreach(var x in record.Attacks) {
                Text(w,x.AttackId); w.Write(x.Revision); Time(w,x.At); Text(w,x.AttackerId);
                Quantity(w,x.X); Quantity(w,x.Y); w.Write(x.Undead); Text(w,x.TypeSource);
                Text(w,x.ZoneCommandId); Text(w,x.Disposition); w.Write(x.Contribution); w.Write(x.TotalModifier);
            }
        }
        internal static ConsecrationRecord Read(BinaryReader r)
        {
            string predecessor=Text(r);
            if(Text(r)!=ConsecrationProfile.RosterSource)throw new InvalidDataException("Unknown Consecration roster authority.");
            var actors=new string[SnapshotCodec.ReadCount(r,6)];
            for(int i=0;i<actors.Length;i++) {
                actors[i]=Text(r);
                if(Text(r)!="Humanoid"||Text(r)!="Living")throw new InvalidDataException("Altered Consecration fixture classification.");
            }
            var zones=new ConsecrationZone[SnapshotCodec.ReadCount(r,ConsecrationRecord.MaxZones)];
            for(int i=0;i<zones.Length;i++) {
                string command=Text(r); long revision=r.ReadInt64(); string owner=Text(r);
                if(Text(r)!=ConsecrationProfile.Consecrate||Text(r)!=ClericRpProfile.SourceRevision||Text(r)!=ConsecrationProfile.Area)
                    throw new InvalidDataException("Unknown Consecration source or area.");
                zones[i]=new ConsecrationZone(command,revision,owner,r.ReadInt32(),r.ReadInt32(),Time(r),SnapshotCodec.ReadBool(r),
                    Text(r),r.ReadInt64(),Time(r),r.ReadInt32(),(ConsecrationEnd)r.ReadInt32(),r.ReadInt64(),Time(r));
            }
            var healing=new ConsecratedGroundHealing[SnapshotCodec.ReadCount(r,ConsecrationRecord.MaxHealing)];
            for(int i=0;i<healing.Length;i++)healing[i]=new ConsecratedGroundHealing(Text(r),Text(r),r.ReadInt64(),Time(r),
                Text(r),Text(r),Quantity(r),Quantity(r),r.ReadInt64(),r.ReadInt64(),r.ReadInt64());
            var attacks=new ConsecrationAttackContribution[SnapshotCodec.ReadCount(r,ConsecrationRecord.MaxAttacks)];
            for(int i=0;i<attacks.Length;i++) {
                string attack=Text(r);long revision=r.ReadInt64();var at=Time(r);string actor=Text(r);
                var x=Quantity(r);var y=Quantity(r);bool undead=SnapshotCodec.ReadBool(r);string source=Text(r);
                string zone=Text(r),disposition=Text(r);int contribution=r.ReadInt32(),modifier=r.ReadInt32();
                attacks[i]=new ConsecrationAttackContribution(attack,revision,at,actor,x,y,undead,zone,modifier);
                if(source!=attacks[i].TypeSource || disposition!=attacks[i].Disposition || contribution!=attacks[i].Contribution)
                    throw new InvalidDataException("Altered Consecration attack source or contribution.");
            }
            return new ConsecrationRecord(predecessor,actors,zones,healing,attacks);
        }
        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w,RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
    }
}
