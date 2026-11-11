using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ExpeditionEpisodeCloseCodec
    {
        public static void Write(BinaryWriter writer, ExpeditionEpisodeCloseRecord record)
        {
            writer.Write(record != null);
            if (record == null) return;
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) => WritePair(writer, value.Numerator, value.Denominator);
            void Quantity(RuleQuantity value) => WritePair(writer, value.Numerator, value.Denominator);
            foreach (string value in new[] { record.EpisodeId, record.CharterVersionId, record.CloserId, record.MandateId,
                record.EvidenceAuthorityId, record.CommandId, record.BillId, record.EncounterId, record.HostileId,
                record.MiningAttemptId }) Text(value);
            writer.Write(record.SourceRevision);
            Time(record.ClosedAt);
            writer.Write(record.BillReportRevision);
            writer.Write(record.EncounterExitRevision);
            Quantity(record.HostileX);
            Quantity(record.HostileY);
            var outcome = record.Outcome;
            writer.Write((int)outcome.PrimaryMetric);
            writer.Write(outcome.RealizedNetCopper);
            Quantity(outcome.NetTargetCopper);
            writer.Write(outcome.RealizedGrossCopper);
            Quantity(outcome.GrossTargetCopper);
            Quantity(outcome.ProfitTargetCopper);

            writer.Write(record.MealIntakeIds.Count);
            foreach (string intakeId in record.MealIntakeIds) Text(intakeId);
            writer.Write(record.Members.Count);
            foreach (var member in record.Members) {
                ActorLifeCodec.WriteLife(writer, member.Life);
                Quantity(member.X);
                Quantity(member.Y);
                writer.Write(member.LastMovementRevision);
                writer.Write(member.AttainedLevels);
                writer.Write(member.Conditions.Count);
                foreach (var condition in member.Conditions) {
                    Text(condition.ApplicationId);
                    Text(condition.Kind);
                    writer.Write(condition.Effective);
                    writer.Write(condition.Inherited);
                    writer.Write(condition.Expires.HasValue);
                    if (condition.Expires.HasValue) {
                        Time(condition.Expires.Value.Time);
                        writer.Write(condition.Expires.Value.Phase);
                    }
                }
            }
            writer.Write(record.MiningDispositions.Count);
            foreach (var disposition in record.MiningDispositions) {
                Text(disposition.UnitId);
                writer.Write((int)disposition.Status);
                Text(disposition.ReceivedLotId);
            }
            writer.Write(record.Stock.Count);
            foreach (var row in record.Stock) {
                var provenance = row.Provenance;
                var stock = row.Stock;
                foreach (string value in new[] { stock.Id, stock.UnitId, stock.LocationId, stock.CustodianId,
                    provenance.ParentId, provenance.OwnerId }) Text(value);
                Quantity(stock.Amount);
                Quantity(provenance.CreatedAmount);
                Time(provenance.CreatedAt);
                writer.Write((int)provenance.Nutrition);
                writer.Write((int)provenance.Access);
                writer.Write(provenance.FreshUntil.HasValue);
                if (provenance.FreshUntil.HasValue) Time(provenance.FreshUntil.Value);
            }
            writer.Write(record.Equipment.Count);
            foreach (var item in record.Equipment) PortableEquipmentCodec.WriteItem(writer, item, Snapshot.ExpeditionEpisodeCloseSchema);
            writer.Write(record.Vessels.Count);
            foreach (var vessel in record.Vessels) {
                Text(vessel.Id);
                writer.Write((int)vessel.Profile);
                Text(vessel.OwnerId);
                Text(vessel.LocationId);
                Text(vessel.CustodianId);
            }
            writer.Write(record.Coverage.Count);
            foreach (var fact in record.Coverage) {
                writer.Write((int)fact.Field);
                writer.Write((int)fact.Knowledge);
                Text(fact.BasisId);
            }
        }

        public static ExpeditionEpisodeCloseRecord Read(BinaryReader reader)
        {
            if (!SnapshotCodec.ReadBool(reader)) return null;
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            RuleQuantity Quantity() => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
            T[] Rows<T>(int limit, Func<T> read) => Enumerable.Range(0, SnapshotCodec.ReadCount(reader, limit)).Select(_ => read()).ToArray();
            string episode = Text(), charter = Text(), closer = Text(), mandate = Text(), access = Text(), command = Text(),
                bill = Text(), encounter = Text(), hostile = Text(), mining = Text();
            long sourceRevision = reader.ReadInt64();
            var at = Time();
            long billRevision = reader.ReadInt64(), exitRevision = reader.ReadInt64();
            var hostileX = Quantity();
            var hostileY = Quantity();
            var outcome = new ExpeditionCloseOutcome((ExpeditionCloseMetric)reader.ReadInt32(), reader.ReadInt64(),
                Quantity(), reader.ReadInt64(), Quantity(), Quantity());

            var intakes = Rows(32, Text);
            ExpeditionCloseCondition ReadCondition()
            {
                string id = Text(), kind = Text();
                bool effective = SnapshotCodec.ReadBool(reader), inherited = SnapshotCodec.ReadBool(reader);
                ConditionStamp? expires = SnapshotCodec.ReadBool(reader) ? new ConditionStamp(Time(), reader.ReadInt32()) : (ConditionStamp?)null;
                return new ExpeditionCloseCondition(id, kind, effective, inherited, expires);
            }
            var members = Rows(12, () => new ExpeditionCloseMember(ActorLifeCodec.ReadLife(reader), Quantity(), Quantity(),
                reader.ReadInt64(), reader.ReadInt32(), Rows(256, ReadCondition)));
            var dispositions = Rows(32, () => new ExpeditionCloseMiningDisposition(Text(), (MiningUnitStatus)reader.ReadInt32(), Text()));
            ExpeditionCloseStock ReadStock()
            {
                string id = Text(), unit = Text(), location = Text(), custodian = Text(), parent = Text(), owner = Text();
                var stock = new ResourceLot(id, unit, Quantity(), location, custodian);
                var originalAmount = Quantity();
                var created = Time();
                var nutrition = (NutritionKind)reader.ReadInt32();
                var inventoryAccess = (InventoryAccess)reader.ReadInt32();
                RuleTime? freshUntil = SnapshotCodec.ReadBool(reader) ? Time() : (RuleTime?)null;
                return new ExpeditionCloseStock(new InventoryLotRecord(id, parent, owner, originalAmount, created,
                    nutrition, freshUntil, inventoryAccess), stock);
            }
            var stockRows = Rows(WorkLedger.MaxRecords, ReadStock);
            var equipment = Rows(128, () => PortableEquipmentCodec.ReadItem(reader, Snapshot.ExpeditionEpisodeCloseSchema));
            var vessels = Rows(128, () => new WaterVesselRecord(Text(), (WaterVesselProfile)reader.ReadInt32(), Text(), Text(), Text()));
            var coverage = Rows(Enum.GetValues(typeof(ExpeditionCloseField)).Length, () => new ExpeditionCloseCoverage(
                (ExpeditionCloseField)reader.ReadInt32(), (ExpeditionCloseKnowledge)reader.ReadInt32(), Text()));
            return new ExpeditionEpisodeCloseRecord(episode, charter, closer, mandate, access, command, sourceRevision, at,
                bill, billRevision, encounter, exitRevision, hostile, hostileX, hostileY, mining, intakes, outcome,
                members, dispositions, stockRows, equipment, vessels, coverage);
        }

        private static void WritePair(BinaryWriter writer, long numerator, long denominator)
        { writer.Write(numerator); writer.Write(denominator); }
    }
}
