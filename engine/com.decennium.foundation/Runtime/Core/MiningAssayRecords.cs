using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum MiningAssayFindingKind { SupportedCategory, Suitability, HandlingRequirement }
    public enum MiningAssayStatus { Working, Paused, AwaitingCheck, Success, CriticalSuccess, Failure, CriticalFailure, Cancelled }

    /// <summary>One authored fact about an already-authored mineral category. It does not create
    /// an item, property, reserve, price, or quantity.</summary>
    public sealed class MiningAssayFindingRecord
    {
        public string Id { get; }
        public string CategoryId { get; }
        public MiningAssayFindingKind Kind { get; }
        public string Fact { get; }

        public MiningAssayFindingRecord(string id, string categoryId, MiningAssayFindingKind kind, string fact)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(categoryId)
                || !Enum.IsDefined(typeof(MiningAssayFindingKind), kind) || fact == null || fact.Length > 512
                || kind == MiningAssayFindingKind.SupportedCategory && fact != ""
                || kind != MiningAssayFindingKind.SupportedCategory && string.IsNullOrWhiteSpace(fact))
                throw new ArgumentException("Invalid authored mineral assay finding.");
            Id = id; CategoryId = categoryId; Kind = kind; Fact = fact;
        }

        internal string Key => Id + "|" + CategoryId + "|" + (int)Kind + "|" + Fact;
    }

    /// <summary>One nondestructive assay profile bound to an existing exposed mineral manifest.
    /// Findings, implements and assessed categories are authored; this profile does not infer them.</summary>
    public sealed class MiningAssayProfileRecord
    {
        private readonly string[] assessedCategoryIds, requiredImplementIds;
        private readonly MiningAssayFindingRecord[] findings;
        public string Id { get; }
        public string DepositId { get; }
        public string DepositVersionId { get; }
        public int? ExactSourceDc { get; }
        public int RequiredHands { get; }
        public string[] AssessedCategoryIds => assessedCategoryIds.ToArray();
        public string[] RequiredImplementIds => requiredImplementIds.ToArray();
        public MiningAssayFindingRecord[] Findings => findings.Select(x => x).ToArray();

        public MiningAssayProfileRecord(string id, string depositId, string depositVersionId, int? exactSourceDc,
            int requiredHands, string[] assessedCategoryIds, string[] requiredImplementIds, MiningAssayFindingRecord[] findings)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(depositId) || !Validation.ValidId(depositVersionId)
                || exactSourceDc.HasValue && (exactSourceDc.Value < 1 || exactSourceDc.Value > 100)
                || requiredHands < 0 || requiredHands > 2 || assessedCategoryIds == null || assessedCategoryIds.Length < 1
                || assessedCategoryIds.Length > MiningValidation.MaxRecords || assessedCategoryIds.Any(x => !Validation.ValidId(x))
                || assessedCategoryIds.Distinct(StringComparer.Ordinal).Count() != assessedCategoryIds.Length
                || requiredImplementIds == null || requiredImplementIds.Length > MiningValidation.MaxRecords
                || requiredImplementIds.Any(x => !Validation.ValidId(x))
                || requiredImplementIds.Distinct(StringComparer.Ordinal).Count() != requiredImplementIds.Length
                || findings == null || findings.Length < assessedCategoryIds.Length || findings.Length > MiningValidation.MaxRecords
                || findings.Any(x => x == null) || findings.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != findings.Length
                || !assessedCategoryIds.All(id => findings.Count(x => x.Kind == MiningAssayFindingKind.SupportedCategory && x.CategoryId == id) == 1)
                || findings.Any(x => !assessedCategoryIds.Contains(x.CategoryId, StringComparer.Ordinal)))
                throw new ArgumentException("Invalid authored mineral assay profile.");
            Id = id; DepositId = depositId; DepositVersionId = depositVersionId; ExactSourceDc = exactSourceDc;
            RequiredHands = requiredHands;
            this.assessedCategoryIds = assessedCategoryIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.requiredImplementIds = requiredImplementIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.findings = findings.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
        }

        internal string Key => string.Join("|", new[] { Id, DepositId, DepositVersionId,
            ExactSourceDc?.ToString(System.Globalization.CultureInfo.InvariantCulture) ?? "-",
            RequiredHands.ToString(System.Globalization.CultureInfo.InvariantCulture),
            string.Join(",", assessedCategoryIds), string.Join(",", requiredImplementIds),
            string.Join("||", findings.Select(x => x.Key)) });

        // The stable authored assay procedure, excluding its content identifier. A renamed copy
        // is not a new evidence-bearing method.
        internal string MethodKey => string.Join("|", new[] {
            ExactSourceDc?.ToString(System.Globalization.CultureInfo.InvariantCulture) ?? "-",
            RequiredHands.ToString(System.Globalization.CultureInfo.InvariantCulture),
            string.Join(",", assessedCategoryIds), string.Join(",", requiredImplementIds),
            string.Join("||", findings.Select(x => string.Join("|", new[] { x.CategoryId,
                ((int)x.Kind).ToString(System.Globalization.CultureInfo.InvariantCulture), x.Fact }))) });

        public bool HasSameContent(MiningAssayProfileRecord other) => other != null && Key == other.Key;
    }

    /// <summary>One one-minute, nondestructive manifest-assay job with a deterministic check audit.</summary>
    public sealed class MiningAssayAttemptRecord
    {
        private readonly string[] findingIds;
        public string Id { get; }
        public string WorkerId { get; }
        public string ProfileId { get; }
        public string DepositId { get; }
        public string DepositVersionId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public MiningAssayStatus Status { get; }
        public int WisdomModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int CheckDc { get; }
        public RuleTime? ResolvedAt { get; }
        public MiningCheckDegree Degree { get; }
        public MiningDiceSelection DiceSelection { get; }
        public int FirstDie { get; }
        public int SecondDie { get; }
        public int Natural { get; }
        public int CheckModifier { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public string[] FindingIds => findingIds.ToArray();

        public MiningAssayAttemptRecord(string id, string workerId, string profileId, string depositId, string depositVersionId,
            RuleTime startedAt, RuleTime updatedAt, RuleTime workDone, MiningAssayStatus status, int wisdomModifier,
            int proficiencyRank, int proficiencyBonus, int checkDc, RuleTime? resolvedAt, MiningCheckDegree degree,
            MiningDiceSelection diceSelection, int firstDie, int secondDie, int natural, int checkModifier,
            uint randomBefore, uint randomAfter, long wordsConsumed, string[] findingIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(workerId) || !Validation.ValidId(profileId)
                || !Validation.ValidId(depositId) || !Validation.ValidId(depositVersionId) || startedAt > updatedAt
                || workDone < default(RuleTime) || workDone > new RuleTime(MiningAssayValidation.WorkSeconds)
                || !Enum.IsDefined(typeof(MiningAssayStatus), status) || proficiencyRank < 0 || proficiencyRank > 2
                || proficiencyBonus < 0 || proficiencyBonus > 20 || checkDc < 1 || checkDc > 100
                || !Enum.IsDefined(typeof(MiningCheckDegree), degree) || !Enum.IsDefined(typeof(MiningDiceSelection), diceSelection)
                || firstDie < 0 || firstDie > 20 || secondDie < 0 || secondDie > 20 || natural < 0 || natural > 20
                || wordsConsumed < 0 || findingIds == null || findingIds.Length > MiningValidation.MaxRecords
                || findingIds.Any(x => !Validation.ValidId(x)) || findingIds.Distinct(StringComparer.Ordinal).Count() != findingIds.Length)
                throw new ArgumentException("Invalid mineral assay attempt.");

            bool resolved = status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess
                || status == MiningAssayStatus.Failure || status == MiningAssayStatus.CriticalFailure;
            bool hasRoll = resolvedAt.HasValue && degree != MiningCheckDegree.None && diceSelection != MiningDiceSelection.None
                && firstDie >= 1 && natural >= 1 && randomBefore != 0 && randomAfter != 0 && wordsConsumed > 0;
            bool validDice = diceSelection == MiningDiceSelection.Normal ? secondDie == 0 && natural == firstDie
                : diceSelection == MiningDiceSelection.Advantage ? secondDie >= 1 && natural == Math.Max(firstDie, secondDie)
                : diceSelection == MiningDiceSelection.Disadvantage && secondDie >= 1 && natural == Math.Min(firstDie, secondDie);
            if (resolved != hasRoll || resolved && (!validDice || workDone != new RuleTime(MiningAssayValidation.WorkSeconds))
                || resolved != resolvedAt.HasValue || resolvedAt.HasValue && resolvedAt.Value != updatedAt
                || (status == MiningAssayStatus.Working || status == MiningAssayStatus.Paused) && workDone >= new RuleTime(MiningAssayValidation.WorkSeconds)
                || status == MiningAssayStatus.AwaitingCheck && workDone != new RuleTime(MiningAssayValidation.WorkSeconds)
                || !resolved && (resolvedAt.HasValue || degree != MiningCheckDegree.None || diceSelection != MiningDiceSelection.None
                    || firstDie != 0 || secondDie != 0 || natural != 0 || checkModifier != 0 || randomBefore != 0 || randomAfter != 0 || wordsConsumed != 0)
                || resolved && ((status == MiningAssayStatus.Success) != (degree == MiningCheckDegree.Success)
                    || (status == MiningAssayStatus.CriticalSuccess) != (degree == MiningCheckDegree.CriticalSuccess)
                    || (status == MiningAssayStatus.Failure) != (degree == MiningCheckDegree.Failure)
                    || (status == MiningAssayStatus.CriticalFailure) != (degree == MiningCheckDegree.CriticalFailure))
                || (status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess) != (findingIds.Length > 0)
                || (status == MiningAssayStatus.Failure || status == MiningAssayStatus.CriticalFailure) && findingIds.Length != 0)
                throw new ArgumentException("Mineral assay outcome does not match its persisted check.");

            Id = id; WorkerId = workerId; ProfileId = profileId; DepositId = depositId; DepositVersionId = depositVersionId;
            StartedAt = startedAt; UpdatedAt = updatedAt; WorkDone = workDone; Status = status; WisdomModifier = wisdomModifier;
            ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus; CheckDc = checkDc; ResolvedAt = resolvedAt;
            Degree = degree; DiceSelection = diceSelection; FirstDie = firstDie; SecondDie = secondDie; Natural = natural;
            CheckModifier = checkModifier; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
            this.findingIds = findingIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        public MiningAssayAttemptRecord WithWork(RuleTime at, RuleTime work, MiningAssayStatus status)
            => Copy(at, work, status, null, MiningCheckDegree.None, MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, Array.Empty<string>());

        public MiningAssayAttemptRecord WithResult(RuleTime at, MiningAssayStatus status, MiningCheckDegree degree,
            MiningDiceSelection selection, int firstDie, int secondDie, int natural, int modifier, uint randomBefore,
            uint randomAfter, long wordsConsumed, string[] learnedFindingIds)
            => Copy(at, new RuleTime(MiningAssayValidation.WorkSeconds), status, at, degree, selection, firstDie,
                secondDie, natural, modifier, randomBefore, randomAfter, wordsConsumed, learnedFindingIds);

        private MiningAssayAttemptRecord Copy(RuleTime at, RuleTime work, MiningAssayStatus status, RuleTime? resolvedAt,
            MiningCheckDegree degree, MiningDiceSelection selection, int firstDie, int secondDie, int natural, int modifier,
            uint randomBefore, uint randomAfter, long wordsConsumed, string[] learnedFindingIds)
            => new MiningAssayAttemptRecord(Id, WorkerId, ProfileId, DepositId, DepositVersionId, StartedAt, at, work,
                status, WisdomModifier, ProficiencyRank, ProficiencyBonus, CheckDc, resolvedAt, degree, selection,
                firstDie, secondDie, natural, modifier, randomBefore, randomAfter, wordsConsumed, learnedFindingIds);
    }

    public static class MiningAssayValidation
    {
        public const int WorkSeconds = 60;
        public const int MaxRecords = MiningValidation.MaxRecords;
        private static RuleTime Add(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                + (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);
        private static RuleTime Subtract(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                - (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);

        public static int Difficulty(Snapshot s, MiningAssayProfileRecord profile)
        {
            if (s == null || profile == null) throw new ArgumentNullException();
            if (profile.ExactSourceDc.HasValue) return profile.ExactSourceDc.Value;
            var categories = s.MiningCategories.Where(x => profile.AssessedCategoryIds.Contains(x.Id, StringComparer.Ordinal)).ToArray();
            if (categories.Length != profile.AssessedCategoryIds.Length || categories.Any(x => x.Tier < 1))
                throw new InvalidOperationException("An exact assay DC is required when an assessed category has no tier.");
            return MiningExtractionRules.TierDc(categories.Max(x => x.Tier));
        }

        public static MiningAssayFindingRecord[] FindingsFor(Snapshot s, string actorId)
        {
            if (s == null || !Validation.ValidId(actorId)) throw new ArgumentException("Invalid assay query.");
            var nondestructive = s.MiningAssayAttempts.Where(x => x.WorkerId == actorId
                    && (x.Status == MiningAssayStatus.Success || x.Status == MiningAssayStatus.CriticalSuccess))
                .SelectMany(attempt => s.MiningAssayProfiles.Where(profile => profile.Id == attempt.ProfileId)
                    .SelectMany(profile => profile.Findings.Where(finding => attempt.FindingIds.Contains(finding.Id, StringComparer.Ordinal))));
            var destructive = (s.DestructiveMiningAssayAttempts ?? Array.Empty<DestructiveMiningAssayAttemptRecord>())
                .Where(x => x.WorkerId == actorId
                    && (x.Status == MiningAssayStatus.Success || x.Status == MiningAssayStatus.CriticalSuccess))
                .SelectMany(attempt => s.DestructiveMiningAssayProfiles.Where(profile => profile.Id == attempt.ProfileId)
                    .SelectMany(profile => s.MiningAssayProfiles.Where(method => method.Id == profile.MethodProfileId)
                        .SelectMany(method => method.Findings.Where(finding => attempt.FindingIds.Contains(finding.Id, StringComparer.Ordinal)))));
            return nondestructive.Concat(destructive)
                .OrderBy(x => x.Id, StringComparer.Ordinal).ThenBy(x => x.CategoryId, StringComparer.Ordinal)
                .ThenBy(x => x.Kind).ThenBy(x => x.Fact, StringComparer.Ordinal).ToArray();
        }

        public static void Validate(Snapshot s)
        {
            if (s.MiningAssayProfiles == null || s.MiningAssayAttempts == null
                || new[] { s.MiningAssayProfiles.Length, s.MiningAssayAttempts.Length }.Any(x => x > MaxRecords)
                || s.MiningAssayProfiles.Any(x => x == null) || s.MiningAssayAttempts.Any(x => x == null))
                throw new ArgumentException("Invalid mining assay records.");
            if (s.SchemaVersion < Snapshot.MiningAssaySchema) {
                if (s.MiningAssayProfiles.Length + s.MiningAssayAttempts.Length != 0)
                    throw new ArgumentException("Mining assay requires schema45.");
                return;
            }
            if (s.MiningAssayProfiles.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.MiningAssayProfiles.Length
                || s.SchemaVersion < Snapshot.DestructiveMiningAssaySchema
                    && s.MiningAssayProfiles.Select(x => x.DepositId).Distinct(StringComparer.Ordinal).Count() != s.MiningAssayProfiles.Length
                || s.MiningAssayAttempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.MiningAssayAttempts.Length
                || s.MiningAssayAttempts.Select(x => x.ProfileId).Distinct(StringComparer.Ordinal).Count() != s.MiningAssayAttempts.Length)
                throw new ArgumentException("Duplicate mining assay identity or repeated evidence basis.");

            foreach (var profile in s.MiningAssayProfiles) {
                var deposit = s.MiningDeposits.SingleOrDefault(x => x.Id == profile.DepositId && x.VersionId == profile.DepositVersionId)
                    ?? throw new ArgumentException("Assay profile references an unknown exposed manifest.");
                var categories = s.MiningCategories.Where(x => x.DepositId == deposit.Id).ToArray();
                if (profile.AssessedCategoryIds.Any(id => !categories.Any(x => x.Id == id && x.Accessible))
                    || profile.Findings.Any(f => !profile.AssessedCategoryIds.Contains(f.CategoryId, StringComparer.Ordinal))
                    || profile.RequiredImplementIds.Any(id => !s.PortableEquipment.Any(x => x.Id == id && x.OwnerId == deposit.OwnerId)))
                    throw new ArgumentException("Assay profile exceeds its authored exposed manifest.");
                int dc = Difficulty(s, profile);
                if (dc < 1 || dc > 100) throw new ArgumentException("Assay DC is outside supported bounds.");
            }
            if (s.SchemaVersion >= Snapshot.DestructiveMiningAssaySchema
                && (s.MiningAssayProfiles.GroupBy(x => x.DepositId + "|" + x.DepositVersionId + "|" + x.MethodKey, StringComparer.Ordinal)
                        .Any(x => x.Count() > 1)
                    || s.MiningAssayProfiles.Select(x => x.Id)
                        .Intersect(s.DestructiveMiningAssayProfiles.Select(x => x.Id), StringComparer.Ordinal).Any()))
                throw new ArgumentException("Assay method identity is ambiguous or renaming does not create different evidence.");

            foreach (var attempt in s.MiningAssayAttempts) {
                if (attempt.Status == MiningAssayStatus.Cancelled)
                    throw new ArgumentException("Cancellation state belongs only to schema46 destructive attempts.");
                var profile = s.MiningAssayProfiles.SingleOrDefault(x => x.Id == attempt.ProfileId)
                    ?? throw new ArgumentException("Assay attempt references an unknown profile.");
                if (attempt.DepositId != profile.DepositId || attempt.DepositVersionId != profile.DepositVersionId
                    || attempt.CheckDc != Difficulty(s, profile) || !s.Actors.Any(x => x.Id == attempt.WorkerId)
                    || attempt.UpdatedAt > s.RuleClock || attempt.ResolvedAt > s.RuleClock)
                    throw new ArgumentException("Assay attempt does not match its authored manifest.");
                bool open = attempt.Status == MiningAssayStatus.Working || attempt.Status == MiningAssayStatus.Paused
                    || attempt.Status == MiningAssayStatus.AwaitingCheck;
                if (attempt.Status == MiningAssayStatus.Working
                    && !s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == attempt.WorkerId
                        && w.Start <= s.RuleClock && w.End > s.RuleClock))
                    throw new ArgumentException("Working assay has no active shared interval.");
                var intervals = s.Work.WorkerIntervals.Where(w => w.JobId == attempt.Id)
                    .OrderBy(w => w.Start).ThenBy(w => w.Id, StringComparer.Ordinal).ToArray();
                if (intervals.Length == 0 || intervals.Any(w => w.WorkerId != attempt.WorkerId || w.Start < attempt.StartedAt)
                    || s.Work.Reservations.Any(r => r.JobId == attempt.Id))
                    throw new ArgumentException("Assay work provenance is invalid or reserves unsupported resources.");
                var active = intervals.Where(w => w.Start <= s.RuleClock && w.End > s.RuleClock).ToArray();
                if (attempt.Status == MiningAssayStatus.Working) {
                    RuleTime booked = active.Length == 1 ? Subtract(active[0].End, s.RuleClock) : default;
                    RuleTime remaining = Subtract(new RuleTime(WorkSeconds), attempt.WorkDone);
                    if (active.Length != 1 || booked != remaining) throw new ArgumentException("Assay interval does not match remaining work.");
                } else if (active.Length != 0) throw new ArgumentException("Inactive assay retains active labor.");
                RuleTime credited = default;
                for (int i = 0; i < intervals.Length; i++) {
                    if (i > 0 && intervals[i - 1].End > intervals[i].Start) throw new ArgumentException("Assay labor intervals overlap.");
                    if (intervals[i].Start >= s.RuleClock) continue;
                    RuleTime end = intervals[i].End < s.RuleClock ? intervals[i].End : s.RuleClock;
                    if (end > intervals[i].Start) credited = Add(credited, Subtract(end, intervals[i].Start));
                }
                if (credited != attempt.WorkDone) throw new ArgumentException("Assay recorded work differs from shared labor.");
                var expectedFindings = profile.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray();
                if ((attempt.Status == MiningAssayStatus.Success || attempt.Status == MiningAssayStatus.CriticalSuccess)
                    && !attempt.FindingIds.SequenceEqual(expectedFindings))
                    throw new ArgumentException("Successful assay must reveal exactly the authored findings.");
                if (attempt.FindingIds.Any(id => !profile.Findings.Any(x => x.Id == id)))
                    throw new ArgumentException("Assay attempt references an unauthored finding.");
                _ = open;
            }
        }
    }

    /// <summary>An actual, already-prepared physical mineral sample. Its quantity and compatible
    /// assay procedures are authored; the record does not create or subdivide inventory.</summary>
    public sealed class MiningAssaySampleRecord
    {
        private readonly string[] compatibleMethodProfileIds;
        public string Id { get; }
        public string DepositId { get; }
        public string DepositVersionId { get; }
        public string CategoryId { get; }
        public string InventoryLotId { get; }
        public RuleQuantity Amount { get; }
        public string[] CompatibleMethodProfileIds => compatibleMethodProfileIds.ToArray();

        public MiningAssaySampleRecord(string id, string depositId, string depositVersionId, string categoryId,
            string inventoryLotId, RuleQuantity amount, string[] compatibleMethodProfileIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(depositId) || !Validation.ValidId(depositVersionId)
                || !Validation.ValidId(categoryId) || !Validation.ValidId(inventoryLotId) || amount <= default(RuleQuantity)
                || compatibleMethodProfileIds == null || compatibleMethodProfileIds.Length == 0
                || compatibleMethodProfileIds.Length > MiningValidation.MaxRecords
                || compatibleMethodProfileIds.Any(x => !Validation.ValidId(x))
                || compatibleMethodProfileIds.Distinct(StringComparer.Ordinal).Count() != compatibleMethodProfileIds.Length)
                throw new ArgumentException("Invalid authored physical assay sample.");
            Id = id; DepositId = depositId; DepositVersionId = depositVersionId; CategoryId = categoryId;
            InventoryLotId = inventoryLotId; Amount = amount;
            this.compatibleMethodProfileIds = compatibleMethodProfileIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        internal string Key => string.Join("|", new[] { Id, DepositId, DepositVersionId, CategoryId, InventoryLotId,
            Amount.ToString(), string.Join(",", compatibleMethodProfileIds) });
        public bool HasSameContent(MiningAssaySampleRecord other) => other != null && Key == other.Key;
    }

    /// <summary>A destructive one-minute assay admission. It binds one actual prepared sample portion
    /// to one authored assay procedure and consumes the whole portion at first credited work.</summary>
    public sealed class DestructiveMiningAssayProfileRecord
    {
        public string Id { get; }
        public string SampleId { get; }
        public string MethodProfileId { get; }
        public RuleQuantity SampleAmount { get; }

        public DestructiveMiningAssayProfileRecord(string id, string sampleId, string methodProfileId, RuleQuantity sampleAmount)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(sampleId) || !Validation.ValidId(methodProfileId)
                || sampleAmount <= default(RuleQuantity)) throw new ArgumentException("Invalid destructive assay profile.");
            Id = id; SampleId = sampleId; MethodProfileId = methodProfileId; SampleAmount = sampleAmount;
        }
    }

    /// <summary>Durable destructive assay attempt. Inventory, reservation settlement and labor intervals
    /// remain authoritative in the shared inventory and WorkLedger records.</summary>
    public sealed class DestructiveMiningAssayAttemptRecord
    {
        private readonly string[] findingIds;
        public string Id { get; }
        public string WorkerId { get; }
        public string ProfileId { get; }
        public string SampleId { get; }
        public string InventoryLotId { get; }
        public RuleQuantity SampleAmount { get; }
        public string EvidenceBasisId { get; }
        public string MethodProfileId { get; }
        public string ReservationId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public MiningAssayStatus Status { get; }
        public int WisdomModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int CheckDc { get; }
        public RuleTime? ResolvedAt { get; }
        public MiningCheckDegree Degree { get; }
        public MiningDiceSelection DiceSelection { get; }
        public int FirstDie { get; }
        public int SecondDie { get; }
        public int Natural { get; }
        public int CheckModifier { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public string[] FindingIds => findingIds.ToArray();

        public DestructiveMiningAssayAttemptRecord(string id, string workerId, string profileId, string sampleId,
            string inventoryLotId, RuleQuantity sampleAmount, string evidenceBasisId, string methodProfileId,
            string reservationId, RuleTime startedAt, RuleTime updatedAt, RuleTime workDone, MiningAssayStatus status,
            int wisdomModifier, int proficiencyRank, int proficiencyBonus, int checkDc, RuleTime? resolvedAt,
            MiningCheckDegree degree, MiningDiceSelection diceSelection, int firstDie, int secondDie, int natural,
            int checkModifier, uint randomBefore, uint randomAfter, long wordsConsumed, string[] findingIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(workerId) || !Validation.ValidId(profileId)
                || !Validation.ValidId(sampleId) || !Validation.ValidId(inventoryLotId) || sampleAmount <= default(RuleQuantity)
                || !Validation.ValidId(evidenceBasisId) || !Validation.ValidId(methodProfileId) || !Validation.ValidId(reservationId)
                || startedAt > updatedAt || workDone < default(RuleTime) || workDone > new RuleTime(MiningAssayValidation.WorkSeconds)
                || !Enum.IsDefined(typeof(MiningAssayStatus), status) || proficiencyRank < 0 || proficiencyRank > 2
                || proficiencyBonus < 0 || proficiencyBonus > 20 || checkDc < 1 || checkDc > 100
                || !Enum.IsDefined(typeof(MiningCheckDegree), degree) || !Enum.IsDefined(typeof(MiningDiceSelection), diceSelection)
                || firstDie < 0 || firstDie > 20 || secondDie < 0 || secondDie > 20 || natural < 0 || natural > 20
                || wordsConsumed < 0 || findingIds == null || findingIds.Length > MiningValidation.MaxRecords
                || findingIds.Any(x => !Validation.ValidId(x))
                || findingIds.Distinct(StringComparer.Ordinal).Count() != findingIds.Length)
                throw new ArgumentException("Invalid destructive mining assay attempt.");
            bool resolved = status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess
                || status == MiningAssayStatus.Failure || status == MiningAssayStatus.CriticalFailure;
            bool hasRoll = resolvedAt.HasValue && degree != MiningCheckDegree.None && diceSelection != MiningDiceSelection.None
                && firstDie >= 1 && natural >= 1 && randomBefore != 0 && randomAfter != 0 && wordsConsumed > 0;
            bool validDice = diceSelection == MiningDiceSelection.Normal ? secondDie == 0 && natural == firstDie
                : diceSelection == MiningDiceSelection.Advantage ? secondDie >= 1 && natural == Math.Max(firstDie, secondDie)
                : diceSelection == MiningDiceSelection.Disadvantage && secondDie >= 1 && natural == Math.Min(firstDie, secondDie);
            if (resolved != hasRoll || resolved && (!validDice || workDone != new RuleTime(MiningAssayValidation.WorkSeconds))
                || resolved != resolvedAt.HasValue || resolvedAt.HasValue && resolvedAt.Value != updatedAt
                || (status == MiningAssayStatus.Working || status == MiningAssayStatus.Paused)
                    && workDone >= new RuleTime(MiningAssayValidation.WorkSeconds)
                || status == MiningAssayStatus.AwaitingCheck && workDone != new RuleTime(MiningAssayValidation.WorkSeconds)
                || !resolved && (resolvedAt.HasValue || degree != MiningCheckDegree.None || diceSelection != MiningDiceSelection.None
                    || firstDie != 0 || secondDie != 0 || natural != 0 || checkModifier != 0 || randomBefore != 0
                    || randomAfter != 0 || wordsConsumed != 0)
                || resolved && ((status == MiningAssayStatus.Success) != (degree == MiningCheckDegree.Success)
                    || (status == MiningAssayStatus.CriticalSuccess) != (degree == MiningCheckDegree.CriticalSuccess)
                    || (status == MiningAssayStatus.Failure) != (degree == MiningCheckDegree.Failure)
                    || (status == MiningAssayStatus.CriticalFailure) != (degree == MiningCheckDegree.CriticalFailure))
                || (status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess) != (findingIds.Length > 0)
                || (status == MiningAssayStatus.Failure || status == MiningAssayStatus.CriticalFailure) && findingIds.Length != 0)
                throw new ArgumentException("Destructive assay outcome does not match its persisted check.");
            Id = id; WorkerId = workerId; ProfileId = profileId; SampleId = sampleId; InventoryLotId = inventoryLotId;
            SampleAmount = sampleAmount; EvidenceBasisId = evidenceBasisId; MethodProfileId = methodProfileId;
            ReservationId = reservationId; StartedAt = startedAt; UpdatedAt = updatedAt; WorkDone = workDone; Status = status;
            WisdomModifier = wisdomModifier; ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus;
            CheckDc = checkDc; ResolvedAt = resolvedAt; Degree = degree; DiceSelection = diceSelection; FirstDie = firstDie;
            SecondDie = secondDie; Natural = natural; CheckModifier = checkModifier; RandomBefore = randomBefore;
            RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
            this.findingIds = findingIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        public DestructiveMiningAssayAttemptRecord WithWork(RuleTime at, RuleTime work, MiningAssayStatus status)
            => Copy(at, work, status, null, MiningCheckDegree.None, MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, Array.Empty<string>());

        public DestructiveMiningAssayAttemptRecord WithResult(RuleTime at, MiningAssayStatus status, MiningCheckDegree degree,
            MiningDiceSelection selection, int firstDie, int secondDie, int natural, int modifier, uint randomBefore,
            uint randomAfter, long wordsConsumed, string[] learnedFindingIds)
            => Copy(at, new RuleTime(MiningAssayValidation.WorkSeconds), status, at, degree, selection, firstDie,
                secondDie, natural, modifier, randomBefore, randomAfter, wordsConsumed, learnedFindingIds);

        private DestructiveMiningAssayAttemptRecord Copy(RuleTime at, RuleTime work, MiningAssayStatus status,
            RuleTime? resolvedAt, MiningCheckDegree degree, MiningDiceSelection selection, int firstDie, int secondDie,
            int natural, int modifier, uint randomBefore, uint randomAfter, long wordsConsumed, string[] learnedFindingIds)
            => new DestructiveMiningAssayAttemptRecord(Id, WorkerId, ProfileId, SampleId, InventoryLotId, SampleAmount,
                EvidenceBasisId, MethodProfileId, ReservationId, StartedAt, at, work, status, WisdomModifier,
                ProficiencyRank, ProficiencyBonus, CheckDc, resolvedAt, degree, selection, firstDie, secondDie, natural,
                modifier, randomBefore, randomAfter, wordsConsumed, learnedFindingIds);
    }

    public static class DestructiveMiningAssayValidation
    {
        private static RuleTime Add(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                + (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);
        private static RuleTime Subtract(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                - (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);

        public static string EvidenceBasis(Snapshot s, string inventoryLotId)
        {
            var current = s.InventoryLots.Single(x => x.LotId == inventoryLotId);
            var seen = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal) { current.LotId };
            while (current.ParentId != "") {
                if (!seen.Add(current.ParentId)) throw new ArgumentException("Assay sample inventory lineage is cyclic.");
                current = s.InventoryLots.Single(x => x.LotId == current.ParentId);
            }
            return current.LotId;
        }

        public static void Validate(Snapshot s)
        {
            if (s.MiningAssaySamples == null || s.DestructiveMiningAssayProfiles == null || s.DestructiveMiningAssayAttempts == null
                || s.MiningAssaySamples.Length > MiningAssayValidation.MaxRecords
                || s.DestructiveMiningAssayProfiles.Length > MiningAssayValidation.MaxRecords
                || s.DestructiveMiningAssayAttempts.Length > MiningAssayValidation.MaxRecords
                || s.MiningAssaySamples.Any(x => x == null) || s.DestructiveMiningAssayProfiles.Any(x => x == null)
                || s.DestructiveMiningAssayAttempts.Any(x => x == null)) throw new ArgumentException("Invalid destructive assay collections.");
            if (s.SchemaVersion < Snapshot.DestructiveMiningAssaySchema) {
                if (s.MiningAssaySamples.Length + s.DestructiveMiningAssayProfiles.Length + s.DestructiveMiningAssayAttempts.Length != 0)
                    throw new ArgumentException("Destructive assay requires schema46.");
                return;
            }
            if (s.MiningAssaySamples.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.MiningAssaySamples.Length
                || s.MiningAssaySamples.Select(x => x.InventoryLotId).Distinct(StringComparer.Ordinal).Count() != s.MiningAssaySamples.Length
                || s.DestructiveMiningAssayProfiles.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.DestructiveMiningAssayProfiles.Length
                || s.DestructiveMiningAssayAttempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.DestructiveMiningAssayAttempts.Length)
                throw new ArgumentException("Duplicate destructive assay identity.");
            foreach (var sample in s.MiningAssaySamples) {
                var deposit = s.MiningDeposits.SingleOrDefault(x => x.Id == sample.DepositId && x.VersionId == sample.DepositVersionId)
                    ?? throw new ArgumentException("Assay sample references an unknown source exposure.");
                if (!s.MiningCategories.Any(x => x.Id == sample.CategoryId && x.DepositId == deposit.Id && x.Accessible)
                    || !s.Actors.Any(x => x.Id == deposit.OwnerId)) throw new ArgumentException("Assay sample category or owner is unavailable.");
                var item = s.PortableEquipment.SingleOrDefault(x => x.Id == sample.Id);
                var provenance = s.InventoryLots.SingleOrDefault(x => x.LotId == sample.InventoryLotId);
                var lot = s.Work.Lots.SingleOrDefault(x => x.Id == sample.InventoryLotId);
                if (item == null || item.LinkKind != PortableLinkKind.InventoryLot || item.LinkedId != sample.InventoryLotId
                    || item.OwnerId != deposit.OwnerId || provenance == null || provenance.OwnerId != deposit.OwnerId
                    || provenance.Nutrition != NutritionKind.None || provenance.CreatedAmount != sample.Amount
                    || lot == null || lot.UnitId != "mass-pound" || lot.CustodianId != deposit.OwnerId
                    || lot.Amount > sample.Amount || s.PortableEquipment.Count(x => x.LinkKind == PortableLinkKind.InventoryLot
                        && x.LinkedId == sample.InventoryLotId) != 1)
                    throw new ArgumentException("Assay sample is not a real compatible inventory portion.");
                var methods = sample.CompatibleMethodProfileIds.Select(id => s.MiningAssayProfiles.SingleOrDefault(x => x.Id == id)
                    ?? throw new ArgumentException("Assay sample names an unknown compatible method.")).ToArray();
                if (methods.Any(x => x.DepositId != deposit.Id || x.DepositVersionId != deposit.VersionId
                    || !x.AssessedCategoryIds.Contains(sample.CategoryId, StringComparer.Ordinal)))
                    throw new ArgumentException("Assay sample is incompatible with its authored method.");
                _ = EvidenceBasis(s, sample.InventoryLotId);
            }
            foreach (var profile in s.DestructiveMiningAssayProfiles) {
                var sample = s.MiningAssaySamples.SingleOrDefault(x => x.Id == profile.SampleId)
                    ?? throw new ArgumentException("Destructive assay profile references an unknown sample.");
                var method = s.MiningAssayProfiles.SingleOrDefault(x => x.Id == profile.MethodProfileId)
                    ?? throw new ArgumentException("Destructive assay profile references an unknown method.");
                if (profile.SampleAmount != sample.Amount || !sample.CompatibleMethodProfileIds.Contains(method.Id, StringComparer.Ordinal)
                    || method.DepositId != sample.DepositId || method.DepositVersionId != sample.DepositVersionId)
                    throw new ArgumentException("Destructive assay profile does not bind an explicitly sufficient sample portion to a compatible method.");
            }
            foreach (var attempt in s.DestructiveMiningAssayAttempts) {
                var profile = s.DestructiveMiningAssayProfiles.SingleOrDefault(x => x.Id == attempt.ProfileId)
                    ?? throw new ArgumentException("Destructive attempt references an unknown profile.");
                var sample = s.MiningAssaySamples.Single(x => x.Id == profile.SampleId);
                var method = s.MiningAssayProfiles.Single(x => x.Id == profile.MethodProfileId);
                if (attempt.SampleId != sample.Id || attempt.InventoryLotId != sample.InventoryLotId
                    || attempt.SampleAmount != profile.SampleAmount || attempt.EvidenceBasisId != EvidenceBasis(s, sample.InventoryLotId)
                    || attempt.MethodProfileId != method.Id || attempt.CheckDc != MiningAssayValidation.Difficulty(s, method)
                    || !s.Actors.Any(x => x.Id == attempt.WorkerId) || attempt.UpdatedAt > s.RuleClock
                    || attempt.ResolvedAt > s.RuleClock)
                    throw new ArgumentException("Destructive attempt no longer matches its authored sample and method.");
                var claims = s.Work.Reservations.Where(x => x.JobId == attempt.Id).ToArray();
                var claim = claims.SingleOrDefault(x => x.Id == attempt.ReservationId);
                if (claims.Length != 1 || claim == null || claim.LotId != sample.InventoryLotId || claim.Amount != sample.Amount
                    || claim.ConsumedAmount > sample.Amount || claim.ReleasedAmount > sample.Amount)
                    throw new ArgumentException("Destructive attempt lost its exact sample reservation.");
                bool hasWork = attempt.WorkDone > default(RuleTime);
                bool badSettlement = hasWork
                    ? claim.ConsumedAmount != sample.Amount || claim.ReleasedAmount != default(RuleQuantity)
                    : claim.ConsumedAmount != default(RuleQuantity)
                        || (attempt.Status == MiningAssayStatus.Cancelled
                            ? claim.ReleasedAmount != sample.Amount
                            : claim.ReleasedAmount != default(RuleQuantity));
                if (badSettlement)
                    throw new ArgumentException("Destructive sample settlement does not match credited work and cancellation.");
                bool open = attempt.Status == MiningAssayStatus.Working || attempt.Status == MiningAssayStatus.Paused
                    || attempt.Status == MiningAssayStatus.AwaitingCheck;
                var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == attempt.Id)
                    .OrderBy(x => x.Start).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
                if (intervals.Any(x => x.WorkerId != attempt.WorkerId || x.Start < attempt.StartedAt))
                    throw new ArgumentException("Destructive assay labor provenance is invalid.");
                if ((attempt.Status != MiningAssayStatus.Cancelled || hasWork) && intervals.Length == 0)
                    throw new ArgumentException("Destructive assay attempt has no credited labor provenance.");
                var active = intervals.Where(x => x.Start <= s.RuleClock && x.End > s.RuleClock).ToArray();
                if (attempt.Status == MiningAssayStatus.Working) {
                    RuleTime remaining = Subtract(new RuleTime(MiningAssayValidation.WorkSeconds), attempt.WorkDone);
                    if (active.Length != 1 || Subtract(active[0].End, s.RuleClock) != remaining)
                        throw new ArgumentException("Working destructive assay interval does not match remaining work.");
                } else if (active.Length != 0) throw new ArgumentException("Inactive destructive assay retains active labor.");
                RuleTime credited = default;
                for (int i = 0; i < intervals.Length; i++) {
                    if (i > 0 && intervals[i - 1].End > intervals[i].Start)
                        throw new ArgumentException("Destructive assay labor intervals overlap.");
                    if (intervals[i].Start >= s.RuleClock) continue;
                    RuleTime end = intervals[i].End < s.RuleClock ? intervals[i].End : s.RuleClock;
                    if (end > intervals[i].Start) credited = Add(credited, Subtract(end, intervals[i].Start));
                }
                if (credited != attempt.WorkDone || open && (attempt.Status == MiningAssayStatus.AwaitingCheck
                    ? attempt.WorkDone != new RuleTime(MiningAssayValidation.WorkSeconds)
                    : attempt.WorkDone >= new RuleTime(MiningAssayValidation.WorkSeconds)))
                    throw new ArgumentException("Destructive assay recorded work differs from its shared labor.");
                var expectedFindings = method.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray();
                if ((attempt.Status == MiningAssayStatus.Success || attempt.Status == MiningAssayStatus.CriticalSuccess)
                    && !attempt.FindingIds.SequenceEqual(expectedFindings)
                    || attempt.FindingIds.Any(id => !method.Findings.Any(x => x.Id == id)))
                    throw new ArgumentException("Destructive assay findings exceed its authored method.");
            }
            var resolved = s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Success
                    || x.Status == MiningAssayStatus.CriticalSuccess || x.Status == MiningAssayStatus.Failure
                    || x.Status == MiningAssayStatus.CriticalFailure).ToArray();
            if (resolved.GroupBy(x => x.EvidenceBasisId + "|" + x.MethodProfileId, StringComparer.Ordinal).Any(x => x.Count() > 1)
                || s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working
                    || x.Status == MiningAssayStatus.Paused || x.Status == MiningAssayStatus.AwaitingCheck)
                    .GroupBy(x => x.EvidenceBasisId + "|" + x.MethodProfileId, StringComparer.Ordinal).Any(x => x.Count() > 1))
                throw new ArgumentException("The same evidence and assay method cannot resolve or run concurrently more than once.");
        }
    }
}
