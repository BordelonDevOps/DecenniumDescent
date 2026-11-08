using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ExpeditionProvisioningCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.DailyProvisioningSettlements.Length);
            foreach (var x in s.DailyProvisioningSettlements.OrderBy(x => x.DayOrdinal).ThenBy(x => x.ActorId, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); w.Write(x.DayOrdinal); Time(w, x.Start); Time(w, x.End);
                Quantity(w, x.FoodRequired); Quantity(w, x.WaterRequired); Quantity(w, x.FoodConsumed);
                Quantity(w, x.WaterConsumed); w.Write(x.RecipientLivingBeforeGain); Text(w, x.StrainGainId); w.Write(x.Revision);
            }
            w.Write(s.DailyProvisioningConsumption.Length);
            foreach (var x in s.DailyProvisioningConsumption.OrderBy(x => x.SettlementId, StringComparer.Ordinal)
                .ThenBy(x => x.IntakeId, StringComparer.Ordinal))
            {
                Text(w, x.SettlementId); Text(w, x.IntakeId); Text(w, x.ActorId); Text(w, x.LotId);
                Text(w, x.ReservationId); w.Write((int)x.Nutrition); Quantity(w, x.Amount);
            }
            w.Write(s.ExpeditionStrainGains.Length);
            foreach (var x in s.ExpeditionStrainGains.OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.PointId); Text(w, x.SettlementId); Text(w, x.ActorId);
                Text(w, x.SourceId); Text(w, x.TrackId); Time(w, x.At); w.Write(x.Revision);
                w.Write(x.LevelBefore); w.Write(x.AttemptedAmount); w.Write(x.AddedAmount);
                OptionalBool(w, x.OrdinaryRemovable); OptionalBool(w, x.RemovalGateMet); w.Write((int)x.Endpoint);
            }
            w.Write(s.ExpeditionDashLocks.Length);
            foreach (var x in s.ExpeditionDashLocks.OrderBy(x => x.ActorId, StringComparer.Ordinal))
            {
                Text(w, x.ActorId); w.Write(x.AppliedRevision); Time(w, x.AppliedAt); Time(w, x.Deadline);
                Text(w, x.EncounterId); Time(w, x.MarkerPhase);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.DailyProvisioningSettlements = new DailyProvisioningSettlementRecord[Count(r, ExpeditionProvisioningValidation.MaxSettlements)];
            for (int i = 0; i < s.DailyProvisioningSettlements.Length; i++)
                s.DailyProvisioningSettlements[i] = new DailyProvisioningSettlementRecord(Text(r), Text(r), r.ReadInt64(),
                    Time(r), Time(r), Quantity(r), Quantity(r), Quantity(r), Quantity(r), Bool(r), Text(r), r.ReadInt64());
            s.DailyProvisioningConsumption = new DailyProvisioningConsumptionRecord[Count(r, ExpeditionProvisioningValidation.MaxConsumptionEvidence)];
            for (int i = 0; i < s.DailyProvisioningConsumption.Length; i++)
                s.DailyProvisioningConsumption[i] = new DailyProvisioningConsumptionRecord(Text(r), Text(r), Text(r),
                    Text(r), Text(r), (NutritionKind)r.ReadInt32(), Quantity(r));
            s.ExpeditionStrainGains = new ExpeditionStrainGainRecord[Count(r, ExpeditionProvisioningValidation.MaxStrainGains)];
            for (int i = 0; i < s.ExpeditionStrainGains.Length; i++)
                s.ExpeditionStrainGains[i] = new ExpeditionStrainGainRecord(Text(r), Text(r), Text(r), Text(r), Text(r),
                    Text(r), Time(r), r.ReadInt64(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), OptionalBool(r),
                    OptionalBool(r), (ExpeditionStrainEndpoint)r.ReadInt32());
            s.ExpeditionDashLocks = new ExpeditionDashLockRecord[Count(r, ExpeditionProvisioningValidation.MaxDashLocks)];
            for (int i = 0; i < s.ExpeditionDashLocks.Length; i++)
                s.ExpeditionDashLocks[i] = new ExpeditionDashLockRecord(Text(r), r.ReadInt64(), Time(r), Time(r), Text(r), Time(r));
        }

        private static int Count(BinaryReader r, int maximum)
        { int n = r.ReadInt32(); if (n < 0 || n > maximum) throw new InvalidDataException("Invalid provisioning collection length."); return n; }
        private static bool Bool(BinaryReader r) => SnapshotCodec.ReadBool(r);
        private static void Text(BinaryWriter w, string text) => SnapshotCodec.WriteText(w, text);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime t) { w.Write(t.Numerator); w.Write(t.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void Quantity(BinaryWriter w, RuleQuantity q) { w.Write(q.Numerator); w.Write(q.Denominator); }
        private static RuleQuantity Quantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
        private static void OptionalBool(BinaryWriter w, bool? value)
        { w.Write(value.HasValue); if (value.HasValue) w.Write(value.Value); }
        private static bool? OptionalBool(BinaryReader r) => Bool(r) ? (bool?)Bool(r) : null;
    }
}
