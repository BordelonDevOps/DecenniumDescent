using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class MiningAssayCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { byte[] bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r)
        {
            int length = r.ReadInt32();
            if (length < 0 || length > 512) throw new InvalidDataException("Invalid mineral assay text length.");
            byte[] bytes = r.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        private static bool Bool(BinaryReader r) { byte value = r.ReadByte(); if (value > 1) throw new InvalidDataException("Invalid mineral assay boolean."); return value == 1; }
        private static int Count(BinaryReader r) { int count = r.ReadInt32(); if (count < 0 || count > MiningAssayValidation.MaxRecords) throw new InvalidDataException("Invalid mineral assay record count."); return count; }
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void NullableTime(BinaryWriter w, RuleTime? value) { w.Write(value.HasValue); if (value.HasValue) Time(w, value.Value); }
        private static RuleTime? NullableTime(BinaryReader r) => Bool(r) ? Time(r) : (RuleTime?)null;
        private static void Ids(BinaryWriter w, string[] values) { w.Write(values.Length); foreach (string value in values) Text(w, value); }
        private static string[] Ids(BinaryReader r) { var values = new string[Count(r)]; for (int i = 0; i < values.Length; i++) values[i] = Text(r); return values; }

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.MiningAssayProfiles.Length);
            foreach (var profile in s.MiningAssayProfiles.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, profile.Id); Text(w, profile.DepositId); Text(w, profile.DepositVersionId);
                w.Write(profile.ExactSourceDc.HasValue); if (profile.ExactSourceDc.HasValue) w.Write(profile.ExactSourceDc.Value);
                w.Write(profile.RequiredHands); Ids(w, profile.AssessedCategoryIds); Ids(w, profile.RequiredImplementIds);
                w.Write(profile.Findings.Length);
                foreach (var finding in profile.Findings.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                    Text(w, finding.Id); Text(w, finding.CategoryId); w.Write((int)finding.Kind); Text(w, finding.Fact);
                }
            }
            w.Write(s.MiningAssayAttempts.Length);
            foreach (var attempt in s.MiningAssayAttempts.OrderBy(x => x.StartedAt).ThenBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, attempt.Id); Text(w, attempt.WorkerId); Text(w, attempt.ProfileId);
                Text(w, attempt.DepositId); Text(w, attempt.DepositVersionId);
                Time(w, attempt.StartedAt); Time(w, attempt.UpdatedAt); Time(w, attempt.WorkDone); w.Write((int)attempt.Status);
                w.Write(attempt.WisdomModifier); w.Write(attempt.ProficiencyRank); w.Write(attempt.ProficiencyBonus); w.Write(attempt.CheckDc);
                NullableTime(w, attempt.ResolvedAt); w.Write((int)attempt.Degree); w.Write((int)attempt.DiceSelection);
                w.Write(attempt.FirstDie); w.Write(attempt.SecondDie); w.Write(attempt.Natural); w.Write(attempt.CheckModifier);
                w.Write(attempt.RandomBefore); w.Write(attempt.RandomAfter); w.Write(attempt.WordsConsumed); Ids(w, attempt.FindingIds);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.MiningAssayProfiles = new MiningAssayProfileRecord[Count(r)];
            for (int i = 0; i < s.MiningAssayProfiles.Length; i++) {
                string id = Text(r), deposit = Text(r), version = Text(r);
                int? dc = Bool(r) ? r.ReadInt32() : (int?)null;
                int hands = r.ReadInt32(); string[] categories = Ids(r), implements = Ids(r);
                var findings = new MiningAssayFindingRecord[Count(r)];
                for (int j = 0; j < findings.Length; j++)
                    findings[j] = new MiningAssayFindingRecord(Text(r), Text(r), (MiningAssayFindingKind)r.ReadInt32(), Text(r));
                s.MiningAssayProfiles[i] = new MiningAssayProfileRecord(id, deposit, version, dc, hands, categories, implements, findings);
            }
            s.MiningAssayAttempts = new MiningAssayAttemptRecord[Count(r)];
            for (int i = 0; i < s.MiningAssayAttempts.Length; i++) {
                string id = Text(r), worker = Text(r), profile = Text(r), deposit = Text(r), version = Text(r);
                RuleTime started = Time(r), updated = Time(r), work = Time(r); var status = (MiningAssayStatus)r.ReadInt32();
                int wisdom = r.ReadInt32(), rank = r.ReadInt32(), bonus = r.ReadInt32(), dc = r.ReadInt32();
                RuleTime? resolved = NullableTime(r); var degree = (MiningCheckDegree)r.ReadInt32();
                var dice = (MiningDiceSelection)r.ReadInt32(); int first = r.ReadInt32(), second = r.ReadInt32();
                int natural = r.ReadInt32(), modifier = r.ReadInt32(); uint before = r.ReadUInt32(), after = r.ReadUInt32();
                long words = r.ReadInt64(); string[] findings = Ids(r);
                s.MiningAssayAttempts[i] = new MiningAssayAttemptRecord(id, worker, profile, deposit, version, started,
                    updated, work, status, wisdom, rank, bonus, dc, resolved, degree, dice, first, second, natural,
                    modifier, before, after, words, findings);
            }
        }
    }

    /// <summary>Schema46 destructive-sample records appended after the schema45 assay payload.</summary>
    internal static class DestructiveMiningAssayCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { byte[] bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r)
        {
            int length = r.ReadInt32();
            if (length < 0 || length > 512) throw new InvalidDataException("Invalid destructive assay text length.");
            byte[] bytes = r.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        private static int Count(BinaryReader r)
        {
            int count = r.ReadInt32();
            if (count < 0 || count > MiningAssayValidation.MaxRecords) throw new InvalidDataException("Invalid destructive assay record count.");
            return count;
        }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime? NullableTime(BinaryReader r)
        {
            byte value = r.ReadByte();
            if (value > 1) throw new InvalidDataException("Invalid destructive assay time flag.");
            return value == 1 ? Time(r) : (RuleTime?)null;
        }
        private static void NullableTime(BinaryWriter w, RuleTime? value) { w.Write(value.HasValue); if (value.HasValue) Time(w, value.Value); }
        private static RuleQuantity Quantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
        private static void Quantity(BinaryWriter w, RuleQuantity value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static string[] Ids(BinaryReader r)
        {
            var values = new string[Count(r)];
            for (int i = 0; i < values.Length; i++) values[i] = Text(r);
            return values;
        }
        private static void Ids(BinaryWriter w, string[] values) { w.Write(values.Length); foreach (string value in values) Text(w, value); }

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.MiningAssaySamples.Length);
            foreach (var sample in s.MiningAssaySamples.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, sample.Id); Text(w, sample.DepositId); Text(w, sample.DepositVersionId); Text(w, sample.CategoryId);
                Text(w, sample.InventoryLotId); Quantity(w, sample.Amount); Ids(w, sample.CompatibleMethodProfileIds);
            }
            w.Write(s.DestructiveMiningAssayProfiles.Length);
            foreach (var profile in s.DestructiveMiningAssayProfiles.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, profile.Id); Text(w, profile.SampleId); Text(w, profile.MethodProfileId); Quantity(w, profile.SampleAmount);
            }
            w.Write(s.DestructiveMiningAssayAttempts.Length);
            foreach (var attempt in s.DestructiveMiningAssayAttempts.OrderBy(x => x.StartedAt).ThenBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, attempt.Id); Text(w, attempt.WorkerId); Text(w, attempt.ProfileId); Text(w, attempt.SampleId);
                Text(w, attempt.InventoryLotId); Quantity(w, attempt.SampleAmount); Text(w, attempt.EvidenceBasisId);
                Text(w, attempt.MethodProfileId); Text(w, attempt.ReservationId);
                Time(w, attempt.StartedAt); Time(w, attempt.UpdatedAt); Time(w, attempt.WorkDone); w.Write((int)attempt.Status);
                w.Write(attempt.WisdomModifier); w.Write(attempt.ProficiencyRank); w.Write(attempt.ProficiencyBonus); w.Write(attempt.CheckDc);
                NullableTime(w, attempt.ResolvedAt); w.Write((int)attempt.Degree); w.Write((int)attempt.DiceSelection);
                w.Write(attempt.FirstDie); w.Write(attempt.SecondDie); w.Write(attempt.Natural); w.Write(attempt.CheckModifier);
                w.Write(attempt.RandomBefore); w.Write(attempt.RandomAfter); w.Write(attempt.WordsConsumed); Ids(w, attempt.FindingIds);
            }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.MiningAssaySamples = new MiningAssaySampleRecord[Count(r)];
            for (int i = 0; i < s.MiningAssaySamples.Length; i++) {
                string id = Text(r), deposit = Text(r), version = Text(r), category = Text(r), lot = Text(r);
                RuleQuantity amount = Quantity(r); string[] methods = Ids(r);
                s.MiningAssaySamples[i] = new MiningAssaySampleRecord(id, deposit, version, category, lot, amount, methods);
            }
            s.DestructiveMiningAssayProfiles = new DestructiveMiningAssayProfileRecord[Count(r)];
            for (int i = 0; i < s.DestructiveMiningAssayProfiles.Length; i++)
                s.DestructiveMiningAssayProfiles[i] = new DestructiveMiningAssayProfileRecord(Text(r), Text(r), Text(r), Quantity(r));
            s.DestructiveMiningAssayAttempts = new DestructiveMiningAssayAttemptRecord[Count(r)];
            for (int i = 0; i < s.DestructiveMiningAssayAttempts.Length; i++) {
                string id = Text(r), worker = Text(r), profile = Text(r), sample = Text(r), lot = Text(r);
                RuleQuantity amount = Quantity(r); string basis = Text(r), method = Text(r), reservation = Text(r);
                RuleTime started = Time(r), updated = Time(r), work = Time(r); var status = (MiningAssayStatus)r.ReadInt32();
                int wisdom = r.ReadInt32(), rank = r.ReadInt32(), bonus = r.ReadInt32(), dc = r.ReadInt32();
                RuleTime? resolved = NullableTime(r); var degree = (MiningCheckDegree)r.ReadInt32();
                var dice = (MiningDiceSelection)r.ReadInt32(); int first = r.ReadInt32(), second = r.ReadInt32();
                int natural = r.ReadInt32(), modifier = r.ReadInt32(); uint before = r.ReadUInt32(), after = r.ReadUInt32();
                long words = r.ReadInt64(); string[] findings = Ids(r);
                s.DestructiveMiningAssayAttempts[i] = new DestructiveMiningAssayAttemptRecord(id, worker, profile, sample,
                    lot, amount, basis, method, reservation, started, updated, work, status, wisdom, rank, bonus, dc,
                    resolved, degree, dice, first, second, natural, modifier, before, after, words, findings);
            }
        }
    }
}
