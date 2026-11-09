using System.IO;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema70 encoding for bounded TEST_ONLY Temporary Camp construction.</summary>
    internal static class TemporaryCampConstructionCodec
    {
        public static void Write(BinaryWriter w, Snapshot s)
        {
            var attempts = s.TemporaryCampConstructionAttempts;
            w.Write(attempts.Length);
            foreach (var x in attempts)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.SiteId); SnapshotCodec.WriteText(w, x.RouteId);
                w.Write(x.RouteTier); SnapshotCodec.WriteText(w, x.ProfileFingerprint); SnapshotCodec.WriteText(w, x.LeadId);
                SnapshotCodec.WriteText(w, x.SkillId); w.Write((int)x.Ability); SnapshotCodec.WriteText(w, x.TentLotId);
                SnapshotCodec.WriteText(w, x.PackLotId); w.Write(x.AssistantIds.Count);
                foreach (string id in x.AssistantIds) SnapshotCodec.WriteText(w, id);
                w.Write(x.StartedRevision); WriteTime(w, x.StartedAt); WriteTime(w, x.UpdatedAt);
                WriteTime(w, x.WorkRequired); WriteTime(w, x.WorkDone); w.Write((int)x.Status);
                w.Write(x.Check != null); if (x.Check != null) WriteCheck(w, x.Check);
            }
            var installs = s.TemporaryCampInstallations;
            w.Write(installs.Length);
            foreach (var x in installs)
            {
                SnapshotCodec.WriteText(w, x.Id); SnapshotCodec.WriteText(w, x.AttemptId);
                SnapshotCodec.WriteText(w, x.SiteId); SnapshotCodec.WriteText(w, x.LotId);
                w.Write((int)x.Kind); WriteTime(w, x.InstalledAt); w.Write(x.AppliedRevision);
            }
        }

        private static void WriteCheck(BinaryWriter w, TemporaryCampConstructionCheckRecord x)
        {
            SnapshotCodec.WriteText(w, x.CommandId); w.Write(x.AppliedRevision); WriteTime(w, x.At);
            w.Write(x.LeadModifier); w.Write(x.ProficiencyRank); w.Write(x.ProficiencyBonus);
            w.Write(x.InjuryPenalty); w.Write(x.StrainModifier); w.Write(x.AssistantBonus); w.Write(x.Dc);
            w.Write(x.ConditionOperationCount); w.Write(x.Disadvantage); w.Write(x.LinkedInjuriesAtCheck.Count);
            foreach (int id in x.LinkedInjuriesAtCheck) w.Write(id);
            w.Write(x.FirstRoll); w.Write(x.SecondRoll); w.Write(x.Natural); w.Write(x.Total); w.Write((int)x.Result);
            w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            int count = SnapshotCodec.ReadCount(r, TemporaryCampConstructionValidation.MaxAttempts);
            var attempts = new TemporaryCampConstructionAttemptRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(r), site = SnapshotCodec.ReadText(r), route = SnapshotCodec.ReadText(r);
                int tier = r.ReadInt32(); string fingerprint = SnapshotCodec.ReadText(r), lead = SnapshotCodec.ReadText(r);
                string skill = SnapshotCodec.ReadText(r); var ability = (CharacterAbility)r.ReadInt32();
                string tent = SnapshotCodec.ReadText(r), pack = SnapshotCodec.ReadText(r);
                int crewCount = SnapshotCodec.ReadCount(r, 3); var crew = new string[crewCount];
                for (int j = 0; j < crewCount; j++) crew[j] = SnapshotCodec.ReadText(r);
                long revision = r.ReadInt64(); RuleTime started = ReadTime(r), updated = ReadTime(r);
                RuleTime required = ReadTime(r), done = ReadTime(r);
                var status = (TemporaryCampConstructionStatus)r.ReadInt32();
                var check = SnapshotCodec.ReadBool(r) ? ReadCheck(r) : null;
                attempts[i] = new TemporaryCampConstructionAttemptRecord(id, site, route, tier, fingerprint, lead,
                    skill, ability, tent, pack, crew, revision, started, updated, required, done, status, check);
            }
            count = SnapshotCodec.ReadCount(r, TemporaryCampConstructionValidation.MaxInstallations);
            var installs = new TemporaryCampInstallationRecord[count];
            for (int i = 0; i < count; i++)
                installs[i] = new TemporaryCampInstallationRecord(SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r),
                    SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r), (TemporaryCampFixtureKind)r.ReadInt32(),
                    ReadTime(r), r.ReadInt64());
            s.TemporaryCampConstructionAttempts = attempts; s.TemporaryCampInstallations = installs;
        }

        private static TemporaryCampConstructionCheckRecord ReadCheck(BinaryReader r)
        {
            string command = SnapshotCodec.ReadText(r); long revision = r.ReadInt64(); RuleTime at = ReadTime(r);
            int modifier = r.ReadInt32(), rank = r.ReadInt32(), proficiency = r.ReadInt32();
            int injury = r.ReadInt32(), strain = r.ReadInt32(), assistant = r.ReadInt32(), dc = r.ReadInt32();
            int operations = r.ReadInt32(); bool disadvantage = SnapshotCodec.ReadBool(r);
            int injuryCount = SnapshotCodec.ReadCount(r, 3); var injuries = new int[injuryCount];
            for (int i = 0; i < injuryCount; i++) injuries[i] = r.ReadInt32();
            int first = r.ReadInt32(), second = r.ReadInt32(), natural = r.ReadInt32(), total = r.ReadInt32();
            var result = (TemporaryCampConstructionResult)r.ReadInt32(); uint before = r.ReadUInt32(), after = r.ReadUInt32();
            int words = r.ReadInt32();
            return new TemporaryCampConstructionCheckRecord(command, revision, at, modifier, rank, proficiency,
                injury, strain, assistant, dc, operations, disadvantage, injuries, first, second, natural, total,
                result, before, after, words);
        }

        private static void WriteTime(BinaryWriter w, RuleTime x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleTime ReadTime(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
    }
}
