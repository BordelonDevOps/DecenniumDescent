using System;
using System.IO;

namespace Decennium.Foundation
{
    internal static class ClericLongRestCodec
    {
        internal static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.ClericLongRests.Length);
            foreach (var x in s.ClericLongRests) {
                w.Write(x.Sequence); Text(w,x.StartCommandId); w.Write(x.StartRevision); Time(w,x.StartedAt);
                w.Write((int)x.Outcome); w.Write((int)x.Interruption); w.Write((int)x.Benefit);
                Text(w,x.EndCommandId); w.Write(x.EndRevision); w.Write(x.EndedAt.HasValue);
                if (x.EndedAt.HasValue) Time(w,x.EndedAt.Value);
                Text(w,x.CauseId);
            }
            w.Write(s.ClericLongRestSettlements.Length);
            foreach (var x in s.ClericLongRestSettlements) {
                Text(w,x.RestId); Text(w,x.CommandId); w.Write(x.Revision); Time(w,x.At); w.Write((int)x.Benefit);
                Text(w,x.BeneficialRestId); Text(w,x.PreviousBeneficialRestId); w.Write(x.CapacityAcquiredRevision);
                w.Write(x.HpBefore); w.Write(x.EffectiveMaximumHp); w.Write(x.HealingRequested); w.Write(x.HealingPotential); w.Write(x.HpAfter);
                w.Write(x.TemporaryHpBefore); w.Write(x.TemporaryHpAfter); w.Write(x.Wounds);
                w.Write(x.ExpendedHitDice); w.Write(x.HitDiceAllowance); w.Write(x.HitDiceRecovered);
                w.Write(x.RpBefore); w.Write(x.RpMaximum); w.Write(x.RpAfter);
                OptionalInt(w,x.ConvictionBefore); OptionalInt(w,x.ConvictionAfter);
                w.Write(x.DissonanceBefore); w.Write(x.DissonanceAfter); Text(w,x.LastSpellId); w.Write(x.Refrain); w.Write(x.LastCastRevision);
            }
            w.Write(s.ConvictionBalance != null);
            if (s.ConvictionBalance != null) {
                Text(w,s.ConvictionBalance.FundingRestId); w.Write(s.ConvictionBalance.FundingRevision); w.Write(s.ConvictionBalance.Current);
            }
        }

        internal static void Read(BinaryReader r, Snapshot s)
        {
            s.ClericLongRests = new ClericLongRestRecord[SnapshotCodec.ReadCount(r,ClericLongRestProfile.MaxAttempts)];
            for (int i=0;i<s.ClericLongRests.Length;i++) {
                int sequence=r.ReadInt32(); string start=Text(r); long startRevision=r.ReadInt64(); var startedAt=Time(r);
                var outcome=(ClericLongRestOutcome)r.ReadInt32(); var interruption=(ClericLongRestInterruption)r.ReadInt32();
                var benefit=(ClericLongRestBenefit)r.ReadInt32(); string end=Text(r); long endRevision=r.ReadInt64();
                RuleTime? endedAt=SnapshotCodec.ReadBool(r)?Time(r):(RuleTime?)null; string cause=Text(r);
                s.ClericLongRests[i]=new ClericLongRestRecord(sequence,start,startRevision,startedAt,outcome,interruption,benefit,
                    end,endRevision,endedAt,cause);
            }
            s.ClericLongRestSettlements=new ClericLongRestSettlementRecord[SnapshotCodec.ReadCount(r,ClericLongRestProfile.MaxAttempts)];
            for (int i=0;i<s.ClericLongRestSettlements.Length;i++) {
                string rest=Text(r),command=Text(r); long revision=r.ReadInt64(); var at=Time(r);
                var benefit=(ClericLongRestBenefit)r.ReadInt32(); string beneficial=Text(r),previous=Text(r);
                long capacityRevision=r.ReadInt64(),hpBefore=r.ReadInt64(),maximum=r.ReadInt64(),requested=r.ReadInt64(),potential=r.ReadInt64(),hpAfter=r.ReadInt64();
                long temporaryBefore=r.ReadInt64(),temporaryAfter=r.ReadInt64(); int wounds=r.ReadInt32();
                int expended=r.ReadInt32(),allowance=r.ReadInt32(),recovered=r.ReadInt32(),rpBefore=r.ReadInt32(),rpMaximum=r.ReadInt32(),rpAfter=r.ReadInt32();
                int? convictionBefore=OptionalInt(r),convictionAfter=OptionalInt(r); int dissonanceBefore=r.ReadInt32(),dissonanceAfter=r.ReadInt32();
                string lastSpell=Text(r); int refrain=r.ReadInt32(); long lastCast=r.ReadInt64();
                s.ClericLongRestSettlements[i]=new ClericLongRestSettlementRecord(rest,command,revision,at,benefit,beneficial,previous,
                    capacityRevision,hpBefore,maximum,requested,potential,hpAfter,temporaryBefore,temporaryAfter,wounds,
                    expended,allowance,recovered,rpBefore,rpMaximum,rpAfter,convictionBefore,convictionAfter,
                    dissonanceBefore,dissonanceAfter,lastSpell,refrain,lastCast);
            }
            if (SnapshotCodec.ReadBool(r)) s.ConvictionBalance=new ConvictionBalanceRecord(Text(r),r.ReadInt64(),r.ReadInt32());
        }

        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void OptionalInt(BinaryWriter w,int? value){w.Write(value.HasValue);if(value.HasValue)w.Write(value.Value);}
        private static int? OptionalInt(BinaryReader r)=>SnapshotCodec.ReadBool(r)?r.ReadInt32():(int?)null;
    }
}
