using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema67 pressure, exposure, causal-change and checkpoint encoding.</summary>
    internal static class ExpeditionPressureCodec
    {
        public static void Write(BinaryWriter w, Snapshot s)
        {
            var cohorts = s.ExpeditionPressureCohorts.OrderBy(x => x.Id, System.StringComparer.Ordinal).ToArray();
            w.Write(cohorts.Length);
            foreach (var x in cohorts)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.ProfileFingerprint);
                SnapshotCodec.WriteText(w, x.RouteFingerprint); w.Write(x.InitialPressure);
                w.Write(x.Members.Count); foreach (var id in x.Members) SnapshotCodec.WriteText(w, id);
            }

            var exposures = s.ExpeditionPressureExposures.OrderBy(x => x.StartedRevision).ToArray();
            w.Write(exposures.Length);
            foreach (var x in exposures)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.CohortId); SnapshotCodec.WriteText(w, x.RouteId);
                w.Write(x.StartedRevision); WriteTime(w, x.StartedAt); w.Write(x.EndedAt.HasValue);
                if (x.EndedAt.HasValue) WriteTime(w, x.EndedAt.Value);
                w.Write(x.EndRevision); w.Write((int)x.EndKind);
            }

            var changes = s.ExpeditionPressureChanges.OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, System.StringComparer.Ordinal).ToArray();
            w.Write(changes.Length);
            foreach (var x in changes)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.CohortId);
                SnapshotCodec.WriteText(w, x.ExposureId); SnapshotCodec.WriteText(w, x.RouteId);
                w.Write(x.WatchIndex); w.Write((int)x.Kind); SnapshotCodec.WriteText(w, x.SourceId);
                w.Write(x.SourceRevision); WriteTime(w, x.At);
            }

            var checkpoints = s.ExpeditionPressureCheckpoints.OrderBy(x => x.WatchIndex).ToArray();
            w.Write(checkpoints.Length);
            foreach (var x in checkpoints)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.CohortId); w.Write(x.WatchIndex);
                WriteTime(w, x.At); w.Write((int)x.Reason); SnapshotCodec.WriteText(w, x.RouteId);
                SnapshotCodec.WriteText(w, x.RouteFingerprint); SnapshotCodec.WriteText(w, x.ProfileFingerprint);
                w.Write((int)x.RouteQuality); w.Write(x.RiskFloor); w.Write(x.PressureBefore);
                w.Write(x.StoredPressure); w.Write(x.EffectivePressure);
                WriteIds(w, x.CauseIds); WriteIds(w, x.ReductionIds);
                w.Write(x.Natural); w.Write(x.ModifiedTotal); w.Write(x.RollWasModifiedOrRerolled);
                w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
                w.Write((int)x.Outcome); w.Write((int)x.Consequence);
                SnapshotCodec.WriteText(w, x.AffectedRouteId); SnapshotCodec.WriteText(w, x.RetreatRouteId);
                WriteQuantity(w, x.RouteProgress);
                w.Write(x.ConsequenceEndsAt.HasValue); if (x.ConsequenceEndsAt.HasValue) WriteTime(w, x.ConsequenceEndsAt.Value);
                SnapshotCodec.WriteText(w, x.CommandId); w.Write(x.AppliedRevision);
                if (s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema) w.Write((int)x.Context);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            int count = SnapshotCodec.ReadCount(r, ExpeditionPressureValidation.MaxCohorts);
            var cohorts = new ExpeditionPressureCohortRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), profile = SnapshotCodec.ReadText(r), routes = SnapshotCodec.ReadText(r);
                int pressure = r.ReadInt32(); int membersCount = SnapshotCodec.ReadCount(r, Snapshot.MaxActors);
                var members = new string[membersCount]; for (int j = 0; j < membersCount; j++) members[j] = SnapshotCodec.ReadText(r);
                cohorts[i] = s.SchemaVersion >= Snapshot.RetreatSchema && members.Length == 2
                    ? ExpeditionPressureCohortRecord.ForLocalRetreat(id, profile, routes, pressure, members)
                    : new ExpeditionPressureCohortRecord(id, profile, routes, pressure, members);
            }

            count = SnapshotCodec.ReadCount(r, ExpeditionPressureValidation.MaxExposures);
            var exposures = new ExpeditionPressureExposureRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), cohort = SnapshotCodec.ReadText(r), route = SnapshotCodec.ReadText(r);
                long revision = r.ReadInt64(); RuleTime start = ReadTime(r);
                RuleTime? end = SnapshotCodec.ReadBool(r) ? ReadTime(r) : (RuleTime?)null;
                long endRevision = r.ReadInt64(); var endKind = (ExpeditionPressureExposureEndKind)r.ReadInt32();
                exposures[i] = new ExpeditionPressureExposureRecord(id, cohort, route, revision, start, end, endRevision, endKind);
            }

            count = SnapshotCodec.ReadCount(r, ExpeditionPressureValidation.MaxChanges);
            var changes = new ExpeditionPressureChangeRecord[count];
            for (int i = 0; i < count; i++)
                changes[i] = new ExpeditionPressureChangeRecord(SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r),
                    SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r), r.ReadInt64(),
                    (ExpeditionPressureChangeKind)r.ReadInt32(), SnapshotCodec.ReadText(r), r.ReadInt64(), ReadTime(r));

            count = SnapshotCodec.ReadCount(r, ExpeditionPressureValidation.MaxCheckpoints);
            var checkpoints = new ExpeditionPressureCheckpointRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), cohort = SnapshotCodec.ReadText(r); long watch = r.ReadInt64();
                RuleTime at = ReadTime(r); var reason = (ExpeditionPressureSettlementReason)r.ReadInt32();
                string route = SnapshotCodec.ReadText(r), routeFingerprint = SnapshotCodec.ReadText(r);
                string profileFingerprint = SnapshotCodec.ReadText(r); var quality = (ExpeditionRouteQuality)r.ReadInt32();
                int floor = r.ReadInt32(), before = r.ReadInt32(), stored = r.ReadInt32(), effective = r.ReadInt32();
                string[] causes = ReadIds(r), reductions = ReadIds(r);
                int natural = r.ReadInt32(), total = r.ReadInt32(); bool modified = SnapshotCodec.ReadBool(r);
                uint randomBefore = r.ReadUInt32(), randomAfter = r.ReadUInt32(); long words = r.ReadInt64();
                var outcome = (ExpeditionPressureOutcome)r.ReadInt32(); var consequence = (ExpeditionPressureConsequenceKind)r.ReadInt32();
                string affected = SnapshotCodec.ReadText(r), retreat = SnapshotCodec.ReadText(r);
                RuleQuantity routeProgress = ReadQuantity(r);
                RuleTime? ends = SnapshotCodec.ReadBool(r) ? ReadTime(r) : (RuleTime?)null;
                string command = SnapshotCodec.ReadText(r); long revision = r.ReadInt64();
                var context = s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                    ? (ExpeditionPressureCheckpointContext)r.ReadInt32()
                    : ExpeditionPressureCheckpointContext.Route;
                checkpoints[i] = new ExpeditionPressureCheckpointRecord(id, cohort, watch, at, reason, route,
                    routeFingerprint, profileFingerprint, quality, floor, before, stored, effective, causes, reductions,
                    natural, total, modified, randomBefore, randomAfter, words, outcome, consequence, affected, retreat,
                    routeProgress, ends, command, revision, context);
            }

            s.ExpeditionPressureCohorts = cohorts; s.ExpeditionPressureExposures = exposures;
            s.ExpeditionPressureChanges = changes; s.ExpeditionPressureCheckpoints = checkpoints;
        }

        private static void WriteIds(BinaryWriter w, System.Collections.Generic.IReadOnlyList<string> values)
        { w.Write(values.Count); foreach (var value in values) SnapshotCodec.WriteText(w, value); }
        private static string[] ReadIds(BinaryReader r)
        {
            int count = SnapshotCodec.ReadCount(r, 128); var values = new string[count];
            for (int i = 0; i < count; i++) values[i] = SnapshotCodec.ReadText(r);
            return values;
        }
        private static void WriteTime(BinaryWriter w, RuleTime x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleTime ReadTime(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void WriteQuantity(BinaryWriter w, RuleQuantity x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
    }
}
