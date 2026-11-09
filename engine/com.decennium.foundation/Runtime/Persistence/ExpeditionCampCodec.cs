using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema69 encoding for immutable TEST_ONLY camp facts and activity history.</summary>
    internal static class ExpeditionCampCodec
    {
        public static void Write(BinaryWriter w, Snapshot s)
        {
            var sites = s.ExpeditionCampSites.OrderBy(x => x.Id, System.StringComparer.Ordinal).ToArray();
            w.Write(sites.Length);
            foreach (var x in sites)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.CohortId);
                SnapshotCodec.WriteText(w, x.RouteId); WriteQuantity(w, x.RouteProgress);
                SnapshotCodec.WriteText(w, x.RouteFingerprint); SnapshotCodec.WriteText(w, x.ProfileFingerprint);
                w.Write(x.RouteX); w.Write(x.RouteY);
                w.Write(x.FootprintWidthFeet); w.Write(x.FootprintHeightFeet);
                w.Write(x.LegalAccess); w.Write(x.Stable); w.Write(x.Drainage); w.Write(x.WeatherProtection);
                w.Write(x.InhabitantSpace); w.Write(x.GearSpace); w.Write(x.Exposed);
                w.Write(x.KnownToEnemies); w.Write(x.Concealed);
            }

            var activities = s.ExpeditionCampActivities.OrderBy(x => x.StartedRevision)
                .ThenBy(x => x.Id, System.StringComparer.Ordinal).ToArray();
            w.Write(activities.Length);
            foreach (var x in activities)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.CohortId);
                SnapshotCodec.WriteText(w, x.ExposureId); SnapshotCodec.WriteText(w, x.CampId);
                w.Write((int)x.Kind); SnapshotCodec.WriteText(w, x.ParentUseId);
                WriteTime(w, x.StartedAt); w.Write(x.StartedRevision); SnapshotCodec.WriteText(w, x.StartCommandId);
                w.Write(x.EndedAt.HasValue); if (x.EndedAt.HasValue) WriteTime(w, x.EndedAt.Value);
                w.Write(x.EndRevision); SnapshotCodec.WriteText(w, x.EndCommandId); w.Write((int)x.EndReason);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            int count = SnapshotCodec.ReadCount(r, ExpeditionCampValidation.MaxSites);
            var sites = new ExpeditionCampSiteRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), cohort = SnapshotCodec.ReadText(r), route = SnapshotCodec.ReadText(r);
                RuleQuantity progress = ReadQuantity(r); string routeFingerprint = SnapshotCodec.ReadText(r);
                string profileFingerprint = SnapshotCodec.ReadText(r); int routeX = r.ReadInt32(), routeY = r.ReadInt32();
                int width = r.ReadInt32(), height = r.ReadInt32();
                bool legal = SnapshotCodec.ReadBool(r), stable = SnapshotCodec.ReadBool(r), drainage = SnapshotCodec.ReadBool(r);
                bool weather = SnapshotCodec.ReadBool(r), inhabitants = SnapshotCodec.ReadBool(r), gear = SnapshotCodec.ReadBool(r);
                bool exposed = SnapshotCodec.ReadBool(r), known = SnapshotCodec.ReadBool(r), concealed = SnapshotCodec.ReadBool(r);
                sites[i] = new ExpeditionCampSiteRecord(id, cohort, route, progress, routeFingerprint, profileFingerprint,
                    routeX, routeY, width, height, legal, stable, drainage, weather, inhabitants, gear, exposed, known, concealed);
            }

            count = SnapshotCodec.ReadCount(r, ExpeditionCampValidation.MaxActivities);
            var activities = new ExpeditionCampActivityRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), cohort = SnapshotCodec.ReadText(r);
                string exposure = SnapshotCodec.ReadText(r), camp = SnapshotCodec.ReadText(r);
                var kind = (ExpeditionCampActivityKind)r.ReadInt32(); string parent = SnapshotCodec.ReadText(r);
                RuleTime started = ReadTime(r); long startedRevision = r.ReadInt64(); string startCommand = SnapshotCodec.ReadText(r);
                RuleTime? ended = SnapshotCodec.ReadBool(r) ? ReadTime(r) : (RuleTime?)null;
                long endRevision = r.ReadInt64(); string endCommand = SnapshotCodec.ReadText(r);
                var endReason = (ExpeditionCampActivityEndReason)r.ReadInt32();
                activities[i] = new ExpeditionCampActivityRecord(id, cohort, exposure, camp, kind, parent,
                    started, startedRevision, startCommand, ended, endRevision, endCommand, endReason);
            }
            s.ExpeditionCampSites = sites; s.ExpeditionCampActivities = activities;
        }

        private static void WriteTime(BinaryWriter w, RuleTime x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleTime ReadTime(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void WriteQuantity(BinaryWriter w, RuleQuantity x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
    }
}
