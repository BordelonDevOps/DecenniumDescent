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
            var gains = s.SchemaVersion >= Snapshot.RestDebtSchema
                ? s.ExpeditionStrainGains.OrderBy(x => x.At).ThenBy(x => x.Revision)
                    .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.GainSequence).ThenBy(x => x.Id, StringComparer.Ordinal)
                : s.ExpeditionStrainGains.OrderBy(x => x.At).ThenBy(x => x.Revision)
                    .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal);
            foreach (var x in gains)
            {
                Text(w, x.Id); Text(w, x.PointId);
                if (s.SchemaVersion >= Snapshot.RestDebtSchema)
                { w.Write((int)x.CauseKind); Text(w, x.CauseId); w.Write(x.GainSequence); }
                else Text(w, x.SettlementId);
                Text(w, x.ActorId);
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
            if (s.SchemaVersion >= Snapshot.RestDebtSchema) RestDebtStateCodec.Write(w, s);
            if (s.SchemaVersion >= Snapshot.ExpeditionStrainRecoverySchema) StrainRecoveryStateCodec.Write(w, s);
            if (s.SchemaVersion >= Snapshot.MoraleRestSchema) MoraleRestStateCodec.Write(w, s);
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
            {
                string id = Text(r), pointId = Text(r);
                if (s.SchemaVersion >= Snapshot.RestDebtSchema)
                    s.ExpeditionStrainGains[i] = new ExpeditionStrainGainRecord(id, pointId,
                        (ExpeditionStrainCauseKind)r.ReadInt32(), Text(r), r.ReadInt32(), Text(r), Text(r),
                        Text(r), Time(r), r.ReadInt64(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(),
                        OptionalBool(r), OptionalBool(r), (ExpeditionStrainEndpoint)r.ReadInt32());
                else
                    s.ExpeditionStrainGains[i] = new ExpeditionStrainGainRecord(id, pointId, Text(r), Text(r), Text(r),
                        Text(r), Time(r), r.ReadInt64(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), OptionalBool(r),
                        OptionalBool(r), (ExpeditionStrainEndpoint)r.ReadInt32());
            }
            s.ExpeditionDashLocks = new ExpeditionDashLockRecord[Count(r, ExpeditionProvisioningValidation.MaxDashLocks)];
            for (int i = 0; i < s.ExpeditionDashLocks.Length; i++)
                s.ExpeditionDashLocks[i] = new ExpeditionDashLockRecord(Text(r), r.ReadInt64(), Time(r), Time(r), Text(r), Time(r));
            if (s.SchemaVersion >= Snapshot.RestDebtSchema) RestDebtStateCodec.Read(r, s);
            if (s.SchemaVersion >= Snapshot.ExpeditionStrainRecoverySchema) StrainRecoveryStateCodec.Read(r, s);
            if (s.SchemaVersion >= Snapshot.MoraleRestSchema) MoraleRestStateCodec.Read(r, s);
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

    internal static class RestDebtStateCodec
    {
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static int Count(BinaryReader r, int maximum) => SnapshotCodec.ReadCount(r, maximum);

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.RestWatchSchedules.Length);
            foreach (var x in s.RestWatchSchedules.OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.DayOrdinal).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); w.Write(x.DayOrdinal); w.Write((int)x.Slot);
                Time(w, x.At); w.Write(x.Revision);
            }
            w.Write(s.RestIntervals.Length);
            foreach (var x in s.RestIntervals.OrderBy(x => x.StartedAt).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.SiteId); Time(w, x.StartedAt); Time(w, x.ScheduledEnd);
                w.Write(x.EndedAt.HasValue); if (x.EndedAt.HasValue) Time(w, x.EndedAt.Value);
                w.Write((int)x.Status); w.Write(x.Revision);
            }
            w.Write(s.RestWatchOutcomes.Length);
            foreach (var x in s.RestWatchOutcomes.OrderBy(x => x.End).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.DayOrdinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); w.Write(x.DayOrdinal); w.Write((int)x.Slot);
                Time(w, x.Start); Time(w, x.End); w.Write((int)x.Outcome); Text(w, x.RestIntervalId); w.Write(x.Revision);
            }
            w.Write(s.RestDebtEvents.Length);
            foreach (var x in s.RestDebtEvents.OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.EventSequence)
                .ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); w.Write((int)x.Kind); Time(w, x.At); w.Write(x.Revision);
                w.Write(x.EventSequence);
                Text(w, x.EpisodeId); Text(w, x.EvidenceId); Time(w, x.DeadlineBefore); Time(w, x.DeadlineAfter);
                Text(w, x.StrainGainId);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.RestWatchSchedules = new RestWatchScheduleRecord[Count(r, ExpeditionProvisioningValidation.MaxRestWatchSchedules)];
            for (int i = 0; i < s.RestWatchSchedules.Length; i++)
                s.RestWatchSchedules[i] = new RestWatchScheduleRecord(Text(r), Text(r), r.ReadInt64(),
                    (RestWatchSlot)r.ReadInt32(), Time(r), r.ReadInt64());
            s.RestIntervals = new RestIntervalRecord[Count(r, ExpeditionProvisioningValidation.MaxRestIntervals)];
            for (int i = 0; i < s.RestIntervals.Length; i++)
            {
                string id = Text(r), actorId = Text(r), siteId = Text(r);
                RuleTime start = Time(r), end = Time(r);
                RuleTime? endedAt = SnapshotCodec.ReadBool(r) ? (RuleTime?)Time(r) : null;
                s.RestIntervals[i] = new RestIntervalRecord(id, actorId, siteId, start, end, endedAt,
                    (RestIntervalStatus)r.ReadInt32(), r.ReadInt64());
            }
            s.RestWatchOutcomes = new RestWatchOutcomeRecord[Count(r, ExpeditionProvisioningValidation.MaxRestWatchOutcomes)];
            for (int i = 0; i < s.RestWatchOutcomes.Length; i++)
                s.RestWatchOutcomes[i] = new RestWatchOutcomeRecord(Text(r), Text(r), r.ReadInt64(),
                    (RestWatchSlot)r.ReadInt32(), Time(r), Time(r), (RestWatchOutcomeKind)r.ReadInt32(), Text(r), r.ReadInt64());
            s.RestDebtEvents = new RestDebtEventRecord[Count(r, ExpeditionProvisioningValidation.MaxRestDebtEvents)];
            for (int i = 0; i < s.RestDebtEvents.Length; i++)
                s.RestDebtEvents[i] = new RestDebtEventRecord(Text(r), Text(r), (RestDebtEventKind)r.ReadInt32(),
                    Time(r), r.ReadInt64(), r.ReadInt32(), Text(r), Text(r), Time(r), Time(r), Text(r));
        }
    }

    internal static class StrainRecoveryStateCodec
    {
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static int Count(BinaryReader r, int maximum) => SnapshotCodec.ReadCount(r, maximum);

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.ExpeditionStrainRecoveryGateUpdates.Length);
            foreach (var x in s.ExpeditionStrainRecoveryGateUpdates.OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.PointId, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.PointId); Text(w, x.SettlementId);
                Time(w, x.At); w.Write(x.Revision);
            }
            w.Write(s.ExpeditionBeneficialRests.Length);
            foreach (var x in s.ExpeditionBeneficialRests.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.RecoveryOfferId); Text(w, x.RestIntervalId);
                Time(w, x.CompletedAt); w.Write(x.Revision);
            }
            w.Write(s.ExpeditionStrainRecoveryOffers.Length);
            foreach (var x in s.ExpeditionStrainRecoveryOffers.OrderBy(x => x.CompletedAt).ThenBy(x => x.ActorId, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId);
                if (s.SchemaVersion >= Snapshot.MoraleRestSchema)
                {
                    w.Write((int)x.RecoveryKind); Text(w, x.RecoveryCompletionId); Text(w, x.ActivityIntervalId);
                }
                else Text(w, x.RestIntervalId);
                Text(w, x.InitiatingCommandId);
                Time(w, x.CompletedAt); w.Write(x.Revision); w.Write(x.PointIds.Length);
                foreach (string pointId in x.PointIds) Text(w, pointId);
                Text(w, x.ChosenPointId); w.Write(x.ResolvedRevision);
            }
            w.Write(s.ExpeditionStrainRemovals.Length);
            foreach (var x in s.ExpeditionStrainRemovals.OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.MutationSequence))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.PointId); Text(w, x.GainId);
                if (s.SchemaVersion >= Snapshot.MoraleRestSchema)
                { w.Write((int)x.RecoveryKind); Text(w, x.RecoveryCompletionId); }
                else Text(w, x.BeneficialRestId);
                Time(w, x.At); w.Write(x.Revision); w.Write(x.MutationSequence);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.ExpeditionStrainRecoveryGateUpdates = new ExpeditionStrainRecoveryGateUpdateRecord[
                Count(r, ExpeditionProvisioningValidation.MaxStrainRecoveryGateUpdates)];
            for (int i = 0; i < s.ExpeditionStrainRecoveryGateUpdates.Length; i++)
                s.ExpeditionStrainRecoveryGateUpdates[i] = new ExpeditionStrainRecoveryGateUpdateRecord(
                    Text(r), Text(r), Text(r), Text(r), Time(r), r.ReadInt64());
            s.ExpeditionBeneficialRests = new ExpeditionBeneficialRestRecord[
                Count(r, ExpeditionProvisioningValidation.MaxBeneficialRests)];
            for (int i = 0; i < s.ExpeditionBeneficialRests.Length; i++)
                s.ExpeditionBeneficialRests[i] = new ExpeditionBeneficialRestRecord(
                    Text(r), Text(r), Text(r), Text(r), Time(r), r.ReadInt64());
            s.ExpeditionStrainRecoveryOffers = new ExpeditionStrainRecoveryOfferRecord[
                Count(r, ExpeditionProvisioningValidation.MaxStrainRecoveryOffers)];
            for (int i = 0; i < s.ExpeditionStrainRecoveryOffers.Length; i++)
            {
                string id = Text(r), actor = Text(r);
                ExpeditionRecoveryKind kind = ExpeditionRecoveryKind.SecureLongRest;
                string completionId = "";
                string activityIntervalId;
                if (s.SchemaVersion >= Snapshot.MoraleRestSchema)
                {
                    kind = (ExpeditionRecoveryKind)r.ReadInt32(); completionId = Text(r); activityIntervalId = Text(r);
                }
                else activityIntervalId = Text(r);
                string initiating = Text(r);
                RuleTime completedAt = Time(r); long revision = r.ReadInt64();
                int pointCount = Count(r, 6); if (pointCount == 0) throw new InvalidDataException("Empty Strain recovery offer.");
                var points = new string[pointCount];
                for (int point = 0; point < pointCount; point++) points[point] = Text(r);
                string chosenPointId = Text(r); long resolvedRevision = r.ReadInt64();
                s.ExpeditionStrainRecoveryOffers[i] = s.SchemaVersion >= Snapshot.MoraleRestSchema
                    ? new ExpeditionStrainRecoveryOfferRecord(id, actor, kind, completionId, activityIntervalId,
                        initiating, completedAt, revision, points, chosenPointId, resolvedRevision)
                    : new ExpeditionStrainRecoveryOfferRecord(id, actor, activityIntervalId, initiating,
                        completedAt, revision, points, chosenPointId, resolvedRevision);
            }
            s.ExpeditionStrainRemovals = new ExpeditionStrainRemovalRecord[
                Count(r, ExpeditionProvisioningValidation.MaxStrainRemovals)];
            for (int i = 0; i < s.ExpeditionStrainRemovals.Length; i++)
            {
                string id = Text(r), actor = Text(r), point = Text(r), gain = Text(r);
                if (s.SchemaVersion >= Snapshot.MoraleRestSchema)
                    s.ExpeditionStrainRemovals[i] = new ExpeditionStrainRemovalRecord(id, actor, point, gain,
                        (ExpeditionRecoveryKind)r.ReadInt32(), Text(r), Time(r), r.ReadInt64(), r.ReadInt32());
                else s.ExpeditionStrainRemovals[i] = new ExpeditionStrainRemovalRecord(id, actor, point, gain,
                    Text(r), Time(r), r.ReadInt64(), r.ReadInt32());
            }
        }
    }

    internal static class MoraleRestStateCodec
    {
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static int Count(BinaryReader r, int maximum) => SnapshotCodec.ReadCount(r, maximum);

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.ExpeditionMoraleRestIntervals.Length);
            foreach (var x in s.ExpeditionMoraleRestIntervals.OrderBy(x => x.StartedAt).ThenBy(x => x.StartRevision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.SiteId); Text(w, x.ActivityId);
                Time(w, x.StartedAt); Time(w, x.ScheduledEnd); w.Write(x.EndedAt.HasValue);
                if (x.EndedAt.HasValue) Time(w, x.EndedAt.Value);
                w.Write((int)x.Status); Text(w, x.StartCommandId); w.Write(x.StartRevision);
                Text(w, x.EndCommandId); w.Write(x.EndRevision);
            }
            w.Write(s.ExpeditionMoraleRestBenefits.Length);
            foreach (var x in s.ExpeditionMoraleRestBenefits.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision)
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.ActorId); Text(w, x.IntervalId); Text(w, x.RecoveryOfferId);
                Time(w, x.CompletedAt); w.Write(x.Revision);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.ExpeditionMoraleRestIntervals = new ExpeditionMoraleRestIntervalRecord[
                Count(r, ExpeditionProvisioningValidation.MaxMoraleRestIntervals)];
            for (int i = 0; i < s.ExpeditionMoraleRestIntervals.Length; i++)
            {
                string id = Text(r), actor = Text(r), site = Text(r), activity = Text(r);
                RuleTime started = Time(r), end = Time(r);
                RuleTime? ended = SnapshotCodec.ReadBool(r) ? (RuleTime?)Time(r) : null;
                s.ExpeditionMoraleRestIntervals[i] = new ExpeditionMoraleRestIntervalRecord(id, actor, site, activity,
                    started, end, ended, (MoraleRestIntervalStatus)r.ReadInt32(), Text(r), r.ReadInt64(),
                    Text(r), r.ReadInt64());
            }
            s.ExpeditionMoraleRestBenefits = new ExpeditionMoraleRestBenefitRecord[
                Count(r, ExpeditionProvisioningValidation.MaxMoraleRestBenefits)];
            for (int i = 0; i < s.ExpeditionMoraleRestBenefits.Length; i++)
                s.ExpeditionMoraleRestBenefits[i] = new ExpeditionMoraleRestBenefitRecord(
                    Text(r), Text(r), Text(r), Text(r), Time(r), r.ReadInt64());
        }
    }
}
