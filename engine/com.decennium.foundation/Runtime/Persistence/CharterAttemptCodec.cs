using System.IO;

namespace Decennium.Foundation
{
    internal static class CharterAttemptCodec
    {
        public static void Write(BinaryWriter writer, CharterAttemptRecord attempt)
        {
            writer.Write(attempt != null);
            if (attempt == null) return;
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }
            void Readiness(CharterAttemptReadiness value)
            {
                NextCharterPlanCodec.WriteObservation(writer, value.Physical);
                writer.Write(value.Strain);
                writer.Write(value.RestDebtOwed);
            }

            Text(attempt.Id);
            Text(attempt.CharterId);
            writer.Write(attempt.AgreementRevision);
            Text(attempt.PlanId);
            writer.Write(attempt.CloseRevision);
            var authority = attempt.Authority;
            foreach (string id in new[] { authority.VersionId, authority.DepartureMandateId, authority.SiteId,
                authority.SiteScopeEvidenceId, authority.ControllerId, authority.ControllerAuthorityId, authority.HeroId,
                authority.VisibilityEvidenceId, authority.FatigueEvidenceId, authority.RestScheduleId,
                authority.EgressPermissionId, authority.EgressEvidenceId })
                Text(id);
            writer.Write(authority.StageX);
            writer.Write(authority.StageY);
            writer.Write(authority.ApproachX);
            writer.Write(authority.ApproachY);
            Time(authority.Epoch);
            writer.Write(authority.OpeningStrain);
            writer.Write(authority.OpeningRestDebt);
            Time(authority.FatigueUntil);
            Time(authority.EgressFrom);
            Time(authority.EgressUntil);
            Readiness(attempt.Admission);
            writer.Write(attempt.Departure != null);
            if (attempt.Departure != null) Readiness(attempt.Departure);
            writer.Write(attempt.Observation != null);
            if (attempt.Observation != null) {
                var observation = attempt.Observation;
                writer.Write(observation.X);
                writer.Write(observation.Y);
                writer.Write(observation.StageSurfaceWalkable);
                writer.Write(observation.ApproachSurfaceWalkable);
                Text(observation.PermissionVersionId);
            }
            Time(attempt.OutboundMovingTime);
            Time(attempt.ReturnMovingTime);
            writer.Write(attempt.Events.Count);
            foreach (var entry in attempt.Events) {
                writer.Write((int)entry.Kind);
                Text(entry.CommandId);
                writer.Write(entry.Revision);
                Time(entry.At);
                Text(entry.Reason);
            }
        }

        public static CharterAttemptRecord Read(BinaryReader reader)
        {
            bool Flag() => SnapshotCodec.ReadBool(reader);
            if (!Flag()) return null;
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            CharterAttemptReadiness Readiness() => new CharterAttemptReadiness(NextCharterPlanCodec.ReadObservation(reader),
                reader.ReadInt32(), Flag());

            string id = Text(), charter = Text();
            long agreementRevision = reader.ReadInt64();
            string plan = Text();
            long closeRevision = reader.ReadInt64();
            string version = Text(), mandate = Text(), site = Text(), scope = Text(), controller = Text(), issuer = Text(),
                hero = Text(), visibility = Text(), fatigue = Text(), rest = Text(), egress = Text(), egressEvidence = Text();
            int stageX = reader.ReadInt32(), stageY = reader.ReadInt32(), approachX = reader.ReadInt32(), approachY = reader.ReadInt32();
            var authority = new CharterAttemptAuthority(version, mandate, site, scope, controller, issuer, hero,
                stageX, stageY, approachX, approachY, visibility, fatigue, rest, Time(), reader.ReadInt32(), Flag(), Time(),
                egress, egressEvidence, Time(), Time());
            var admission = Readiness();
            var departure = Flag() ? Readiness() : null;
            var observation = Flag()
                ? new CharterApproachObservation(reader.ReadInt32(), reader.ReadInt32(), Flag(), Flag(), Text()) : null;
            var outboundMovingTime = Time();
            var returnMovingTime = Time();
            var history = new CharterAttemptEvent[SnapshotCodec.ReadCount(reader, CharterAttemptRecord.MaxEvents)];
            for (int i = 0; i < history.Length; i++)
                history[i] = new CharterAttemptEvent((CharterAttemptEventKind)reader.ReadInt32(), Text(), reader.ReadInt64(), Time(), Text());
            return new CharterAttemptRecord(id, charter, agreementRevision, plan, closeRevision, authority,
                admission, history, departure, observation, outboundMovingTime, returnMovingTime);
        }
    }
}
