using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ClubAttackCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.Clubs.Length);
            foreach(var c in s.Clubs.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,c.Id);Text(w,c.ProfileId);Text(w,c.OwnerId);Text(w,c.CustodianId);Text(w,c.HeldBy);w.Write(c.CellX);w.Write(c.CellY);
            }
            w.Write(s.Stances.Length);
            foreach(var t in s.Stances.OrderBy(x=>x.Revision)) {
                Text(w,t.ActorId);w.Write(t.Revision);w.Write(t.TurnOrdinal);w.Write((int)t.Kind);Time(w,t.ExpiresAt);
            }
            w.Write(s.MeleeAttacks.Length);
            foreach(var a in s.MeleeAttacks.OrderBy(x=>x.Revision)) {
                Text(w,a.Id);w.Write(a.Revision);w.Write(a.ResolvedRevision);w.Write(a.TurnOrdinal);Text(w,a.AttackerId);Text(w,a.TargetId);Text(w,a.WeaponId);
                Time(w,a.At);w.Write((int)a.Instruction);var r=a.Attack;
                w.Write(r.First);w.Write(r.Second);w.Write(r.Selected);w.Write(r.Modifier);w.Write(r.ArmorClass);w.Write(r.Hit);w.Write(r.Critical);
                w.Write(r.RandomBefore);w.Write(r.RandomAfter);w.Write(r.Words);var d=a.Damage;
                w.Write(d.Dice.Count);foreach(int n in d.Dice)w.Write(n);w.Write(d.Total);w.Write(d.DiceWords);w.Write(d.EffectsSeed);w.Write(d.FinalRandom);
                w.Write(d.EffectsWords);w.Write(d.WoundNatural);w.Write(d.InjuryD6);w.Write(d.StableD4);
                if(s.SchemaVersion>=Snapshot.TacticalMovementSchema){w.Write(a.Opportunity);w.Write((int)a.PressInstruction);}
            }
            w.Write(s.Presses.Length);
            foreach(var p in s.Presses.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,p.ActorId);Text(w,p.TargetId);w.Write(p.ArmedRevision);Time(w,p.ExpiresAt);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.Clubs=new ClubInstance[Count(r,64)];
            for(int i=0;i<s.Clubs.Length;i++)s.Clubs[i]=new ClubInstance(Text(r),Text(r),Text(r),Text(r),Text(r),r.ReadInt32(),r.ReadInt32());
            s.Stances=new StanceSelectionRecord[Count(r,128)];
            for(int i=0;i<s.Stances.Length;i++)s.Stances[i]=new StanceSelectionRecord(Text(r),r.ReadInt64(),r.ReadInt32(),(CombatStance)r.ReadInt32(),Time(r));
            s.MeleeAttacks=new MeleeAttackRecord[Count(r,128)];
            for(int i=0;i<s.MeleeAttacks.Length;i++) {
                string id=Text(r);long revision=r.ReadInt64(),resolved=r.ReadInt64();int ordinal=r.ReadInt32();string actor=Text(r),target=Text(r),weapon=Text(r);
                var at=Time(r);var instruction=(AttackKnockoutMode)r.ReadInt32();
                var attack=new CombatAttackRoll(r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),Bool(r),Bool(r),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
                var dice=new int[Count(r,2)];for(int j=0;j<dice.Length;j++)dice[j]=r.ReadInt32();
                var damage=new CombatDamageRoll(dice,r.ReadInt64(),r.ReadInt64(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32());
                bool opportunity=s.SchemaVersion>=Snapshot.TacticalMovementSchema&&Bool(r);
                var press=s.SchemaVersion>=Snapshot.TacticalMovementSchema?(PressHitInstruction)r.ReadInt32():PressHitInstruction.ArmOrReplace;
                s.MeleeAttacks[i]=new MeleeAttackRecord(id,revision,resolved,ordinal,actor,target,weapon,at,instruction,attack,damage,opportunity,press);
            }
            s.Presses=new PressRecord[Count(r,64)];
            for(int i=0;i<s.Presses.Length;i++)s.Presses[i]=new PressRecord(Text(r),Text(r),r.ReadInt64(),Time(r));
        }
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid combat flag.");return b==1;}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid combat count.");return n;}
        private static void Text(BinaryWriter w,string t){var b=Utf8.GetBytes(t);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);var b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
