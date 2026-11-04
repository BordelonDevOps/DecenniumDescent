using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class RangedCombatCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.RepeatingCrossbows.Length);
            foreach(var x in s.RepeatingCrossbows.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ProfileId);Text(w,x.OwnerId);Text(w,x.CustodianId);Text(w,x.HeldBy);w.Write(x.GripHands);w.Write(x.CellX);w.Write(x.CellY);
                w.Write(x.LoadedBoltLots.Count);foreach(string lot in x.LoadedBoltLots)Text(w,lot);
            }
            w.Write(s.AmmunitionLots.Length);
            foreach(var x in s.AmmunitionLots.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ProfileId);Text(w,x.OwnerId);Text(w,x.CustodianId);w.Write(x.OriginalQuantity);w.Write(x.AvailableQuantity);w.Write(x.Accessible);
            }
            w.Write(s.RangedCombatants.Length);
            foreach(var x in s.RangedCombatants.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,x.ActorId);w.Write(x.DexterityScore);w.Write(x.ProficiencyBonus);w.Write(x.CrossbowProficient);Text(w,x.TrainingId);
            }
            w.Write(s.RangedAttacks.Length);
            foreach(var x in s.RangedAttacks.OrderBy(x=>x.Revision)) {
                Text(w,x.Id);w.Write(x.Revision);w.Write(x.TurnOrdinal);Text(w,x.AttackerId);Text(w,x.TargetId);Text(w,x.WeaponId);Text(w,x.AmmunitionLotId);Time(w,x.At);
                var a=x.Attack;w.Write(a.First);w.Write(a.Second);w.Write(a.Selected);w.Write(a.Modifier);w.Write(a.ArmorClass);w.Write(a.Hit);w.Write(a.Critical);
                w.Write(a.RandomBefore);w.Write(a.RandomAfter);w.Write(a.Words);
                var d=x.Damage;w.Write(d.Dice.Count);foreach(int die in d.Dice)w.Write(die);w.Write(d.FlatModifier);w.Write(d.Total);w.Write(d.AfterDefense);w.Write(d.DiceWords);
                w.Write(d.EffectsSeed);w.Write(d.FinalRandom);w.Write(d.EffectsWords);w.Write(d.WoundNatural);w.Write(d.InjuryD6);w.Write(d.StableD4);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.RepeatingCrossbows=new RepeatingCrossbowRecord[Count(r,64)];
            for(int i=0;i<s.RepeatingCrossbows.Length;i++) {
                string id=Text(r),profile=Text(r),owner=Text(r),custodian=Text(r),held=Text(r);int hands=r.ReadInt32(),x=r.ReadInt32(),y=r.ReadInt32();
                var lots=new string[Count(r,5)];for(int j=0;j<lots.Length;j++)lots[j]=Text(r);
                s.RepeatingCrossbows[i]=new RepeatingCrossbowRecord(id,profile,owner,custodian,held,hands,x,y,lots);
            }
            s.AmmunitionLots=new AmmunitionLotRecord[Count(r,128)];
            for(int i=0;i<s.AmmunitionLots.Length;i++)s.AmmunitionLots[i]=new AmmunitionLotRecord(Text(r),Text(r),Text(r),Text(r),r.ReadInt32(),r.ReadInt32(),Bool(r));
            s.RangedCombatants=new RangedCombatantRecord[Count(r,64)];
            for(int i=0;i<s.RangedCombatants.Length;i++)s.RangedCombatants[i]=new RangedCombatantRecord(Text(r),r.ReadInt32(),r.ReadInt32(),Bool(r),Text(r));
            s.RangedAttacks=new RangedAttackRecord[Count(r,128)];
            for(int i=0;i<s.RangedAttacks.Length;i++) {
                string id=Text(r);long revision=r.ReadInt64();int ordinal=r.ReadInt32();string attacker=Text(r),target=Text(r),weapon=Text(r),lot=Text(r);var at=Time(r);
                var attack=new CombatAttackRoll(r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),Bool(r),Bool(r),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
                var dice=new int[Count(r,2)];for(int j=0;j<dice.Length;j++)dice[j]=r.ReadInt32();
                var damage=new RangedDamageRoll(dice,r.ReadInt32(),r.ReadInt64(),r.ReadInt64(),r.ReadInt64(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32());
                s.RangedAttacks[i]=new RangedAttackRecord(id,revision,ordinal,attacker,target,weapon,lot,at,attack,damage);
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid ranged combat count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid ranged combat flag.");return b==1;}
        private static void Text(BinaryWriter w,string t){byte[] b=Utf8.GetBytes(t);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
