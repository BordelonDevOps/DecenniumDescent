using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class NextCharterPlanCodec
    {
        public static void Write(BinaryWriter writer, Snapshot state)
        {
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }
            writer.Write(state.NextCharterPlans.Length);
            foreach (var job in state.NextCharterPlans.OrderBy(x => x.StartRevision)) {
                var terms = job.Terms;
                foreach (string value in new[] { job.Id, terms.VersionId, terms.EpisodeId, terms.CharterVersionId, terms.PlannerId,
                    terms.MandateId, terms.EvidenceAuthorityId, terms.DeskId, terms.ObjectiveId, terms.PassageWitnessId, terms.RationRoot,
                    terms.WaterRoot, terms.WaterVessel, terms.ReserveWaterRoot, terms.ReserveWaterVessel }) Text(value);
                writer.Write(terms.StageX);
                writer.Write(terms.StageY);
                writer.Write(terms.ApproachX);
                writer.Write(terms.ApproachY);
                Time(terms.ValidFrom);
                Time(terms.AuthorizationUntil);
                writer.Write(job.PriorCloseRevision);
                writer.Write(job.PassageRevision);
                writer.Write(job.StartRevision);
                writer.Write(job.UpdatedRevision);
                Time(job.StartedAt);
                Time(job.UpdatedAt);
                Time(job.Work.Labor);
                writer.Write((int)job.Status);
                Text(job.Reason);
                var report = job.Report;
                if (report == null) continue;
                WriteObservation(writer, report);
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            var jobs = new NextCharterPlanRecord[SnapshotCodec.ReadCount(reader, NextCharterPlanValidation.MaxAttempts)];
            for (int i = 0; i < jobs.Length; i++) {
                string id = Text(), version = Text(), episode = Text(), charter = Text(), planner = Text(), mandate = Text(),
                    evidence = Text(), desk = Text(), objective = Text(), witness = Text(), ration = Text(), water = Text(),
                    vessel = Text(), reserve = Text(), reserveVessel = Text();
                var terms = new NextCharterPlanTerms(version, episode, charter, planner, mandate, evidence, desk, objective, witness,
                    reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), ration, water, vessel, reserve,
                    reserveVessel, Time(), Time());
                long prior = reader.ReadInt64(), passage = reader.ReadInt64(), start = reader.ReadInt64(), update = reader.ReadInt64();
                var startedAt = Time();
                var updatedAt = Time();
                var labor = Time();
                var status = (NextCharterPlanStatus)reader.ReadInt32();
                string reason = Text();
                NextCharterPlanObservation report = null;
                if (status == NextCharterPlanStatus.CompletedConditional)
                    report = ReadObservation(reader);
                jobs[i] = new NextCharterPlanRecord(id, terms, prior, passage, start, update, startedAt, updatedAt, labor, status, reason, report);
            }
            state.NextCharterPlans = jobs;
        }

        internal static void WriteObservation(BinaryWriter writer, NextCharterPlanObservation report)
        {
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }
            void Quantity(RuleQuantity value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }
            void OptionalQuantity(RuleQuantity? value)
            {
                writer.Write(value.HasValue);
                if (value.HasValue) Quantity(value.Value);
            }
            void OptionalFlag(bool? value)
            {
                writer.Write(value.HasValue);
                if (value.HasValue) writer.Write(value.Value);
            }
            void OptionalInt(int? value)
            {
                writer.Write(value.HasValue);
                if (value.HasValue) writer.Write(value.Value);
            }
            Time(report.At);
            writer.Write(report.Revision);
            writer.Write(report.Walkable);
            writer.Write(report.Occupied);
            writer.Write(report.PathReserved);
            writer.Write(report.TacticalTransition);
            OptionalFlag(report.ApproachAccess);
            writer.Write(report.ScoutCapable);
            writer.Write(report.ScoutAtStage);
            OptionalQuantity(report.ActualPounds);
            OptionalQuantity(report.ActualLoad);
            OptionalFlag(report.CanCarry);
            OptionalFlag(report.Burdened);
            OptionalInt(report.Pressure);
            OptionalInt(report.Strain);
            OptionalFlag(report.RestDebt);
            foreach (var supply in report.Supplies) {
                Text(supply.RootId);
                Text(supply.VesselId);
                OptionalQuantity(supply.VesselCapacity);
                Text(supply.VesselOwnerId);
                Text(supply.VesselCustodianId);
                Text(supply.VesselLocationId);
                Quantity(supply.Required);
                writer.Write(supply.Lots.Count);
                foreach (var lot in supply.Lots) {
                    Text(lot.LotId);
                    Text(lot.OwnerId);
                    Text(lot.CustodianId);
                    Text(lot.LocationId);
                    Quantity(lot.PhysicalAmount);
                    Quantity(lot.UnreservedAmount);
                    writer.Write(lot.UseAuthorized);
                    writer.Write(lot.CorrectCustody);
                    writer.Write(lot.Carried);
                    writer.Write(lot.Suitable);
                    writer.Write(lot.Accessible);
                    writer.Write(lot.Ready);
                }
            }
        }

        internal static NextCharterPlanObservation ReadObservation(BinaryReader reader)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            bool Flag() => SnapshotCodec.ReadBool(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            RuleQuantity Quantity() => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
            RuleQuantity? OptionalQuantity() => Flag() ? Quantity() : (RuleQuantity?)null;
            bool? OptionalFlag() => Flag() ? Flag() : (bool?)null;
            int? OptionalInt() => Flag() ? reader.ReadInt32() : (int?)null;
            NextCharterSupplyObservation Supply()
            {
                string root = Text(), vessel = Text();
                var capacity = OptionalQuantity();
                string owner = Text(), custodian = Text(), location = Text();
                var required = Quantity();
                var lots = new NextCharterStockObservation[SnapshotCodec.ReadCount(reader, 128)];
                for (int j = 0; j < lots.Length; j++)
                    lots[j] = new NextCharterStockObservation(Text(), Text(), Text(), Text(), Quantity(), Quantity(),
                        Flag(), Flag(), Flag(), Flag(), Flag(), Flag());
                return new NextCharterSupplyObservation(root, vessel, capacity, owner, custodian, location, required, lots);
            }

            return new NextCharterPlanObservation(Time(), reader.ReadInt64(), Flag(), Flag(), Flag(), Flag(), OptionalFlag(),
                Flag(), Flag(), OptionalQuantity(), OptionalQuantity(), OptionalFlag(), OptionalFlag(), OptionalInt(),
                OptionalInt(), OptionalFlag(), new[] { Supply(), Supply(), Supply() });
        }
    }
}
