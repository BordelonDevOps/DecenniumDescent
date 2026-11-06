using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ProspectingSignSeverity { Clear, Obscured, SevereFeasible }
    public enum ProspectingMethodKind { VisualInspection, PhysicalSampling, Measurement }
    public enum ProspectingObservationKind { MineralSign, PossibleAccess }
    public enum ProspectingAttemptStatus { Working, Paused, AwaitingCheck, Success, CriticalSuccess, Failure, CriticalFailure, InvalidatedWithoutCheck }

    /// <summary>One immutable authored set of prospecting evidence and method requirements.
    /// This contains observable facts only; it has no deposit or hidden-reserve fields.</summary>
    public sealed class ProspectingExposureProfile
    {
        private readonly string[] requiredImplementIds, findingIds;
        public string Id { get; }
        public string PatchId { get; }
        public int AreaSquareFeet { get; }
        public bool Exposed { get; }
        public bool Accessible { get; }
        public ProspectingSignSeverity Signs { get; }
        public ProspectingMethodKind Method { get; }
        public int RequiredHands { get; }
        public string HazardDeclarationId { get; }
        public string[] RequiredImplementIds => requiredImplementIds.ToArray();
        public string[] FindingIds => findingIds.ToArray();

        public ProspectingExposureProfile(string id, string patchId, int areaSquareFeet, bool exposed, bool accessible,
            ProspectingSignSeverity signs, ProspectingMethodKind method, int requiredHands, string hazardDeclarationId,
            string[] requiredImplementIds, string[] findingIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(patchId) || areaSquareFeet < 1 || areaSquareFeet > 100
                || !Enum.IsDefined(typeof(ProspectingSignSeverity), signs) || !Enum.IsDefined(typeof(ProspectingMethodKind), method)
                || requiredHands < 0 || requiredHands > 2 || !Validation.ValidId(hazardDeclarationId)
                || requiredImplementIds == null || requiredImplementIds.Length > ProspectingValidation.MaxRecords
                || requiredImplementIds.Any(x => !Validation.ValidId(x))
                || requiredImplementIds.Distinct(StringComparer.Ordinal).Count() != requiredImplementIds.Length
                || findingIds == null || findingIds.Length > ProspectingValidation.MaxRecords || findingIds.Any(x => !Validation.ValidId(x))
                || findingIds.Distinct(StringComparer.Ordinal).Count() != findingIds.Length)
                throw new ArgumentException("Invalid authored prospecting exposure.");
            Id = id; PatchId = patchId; AreaSquareFeet = areaSquareFeet; Exposed = exposed; Accessible = accessible;
            Signs = signs; Method = method; RequiredHands = requiredHands; HazardDeclarationId = hazardDeclarationId;
            this.requiredImplementIds = requiredImplementIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.findingIds = findingIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        internal string Key => Id + "|" + PatchId + "|" + AreaSquareFeet + "|" + Exposed + "|" + Accessible + "|"
            + (int)Signs + "|" + (int)Method + "|" + RequiredHands + "|" + HazardDeclarationId + "|"
            + string.Join(",", requiredImplementIds) + "|" + string.Join(",", findingIds);
    }

    /// <summary>One authored, player-observable statement. Interpretations and concealed geology
    /// are deliberately not represented by this record.</summary>
    public sealed class ProspectingObservationProfile
    {
        public string Id { get; }
        public ProspectingObservationKind Kind { get; }
        public string ObservableFact { get; }
        public ProspectingObservationProfile(string id, ProspectingObservationKind kind, string observableFact)
        {
            if (!Validation.ValidId(id) || !Enum.IsDefined(typeof(ProspectingObservationKind), kind)
                || string.IsNullOrWhiteSpace(observableFact) || observableFact.Length > 512)
                throw new ArgumentException("Invalid prospecting observation.");
            Id = id; Kind = kind; ObservableFact = observableFact;
        }
        internal string Key => Id + "|" + (int)Kind + "|" + ObservableFact;
    }

    /// <summary>Canonical patch identity and the currently active exposure version.</summary>
    public sealed class ProspectingPatchRecord
    {
        public string Id { get; }
        public string OwnerId { get; }
        public string SiteId { get; }
        public int X { get; }
        public int Y { get; }
        public string CurrentExposureId { get; }
        public ProspectingPatchRecord(string id, string ownerId, string siteId, int x, int y, string currentExposureId)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(ownerId) || !Validation.ValidId(siteId)
                || !Validation.ValidId(currentExposureId) || x < 0 || y < 0)
                throw new ArgumentException("Invalid prospecting patch.");
            Id = id; OwnerId = ownerId; SiteId = siteId; X = x; Y = y; CurrentExposureId = currentExposureId;
        }
        public ProspectingPatchRecord WithCurrentExposure(string exposureId)
            => new ProspectingPatchRecord(Id, OwnerId, SiteId, X, Y, exposureId);
    }

    /// <summary>Persisted exposure history. ChangeCauseId records the trusted host's asserted
    /// world event; engine validation requires an actual evidence change and a linked version.</summary>
    public sealed class ProspectingExposureRecord
    {
        private readonly string[] requiredImplementIds, findingIds;
        public string Id { get; }
        public string PatchId { get; }
        public string ParentExposureId { get; }
        public string ChangeCauseId { get; }
        public RuleTime ChangedAt { get; }
        public int AreaSquareFeet { get; }
        public bool Exposed { get; }
        public bool Accessible { get; }
        public ProspectingSignSeverity Signs { get; }
        public ProspectingMethodKind Method { get; }
        public int RequiredHands { get; }
        public string HazardDeclarationId { get; }
        public string[] RequiredImplementIds => requiredImplementIds.ToArray();
        public string[] FindingIds => findingIds.ToArray();

        public ProspectingExposureRecord(string id, string patchId, string parentExposureId, string changeCauseId, RuleTime changedAt,
            int areaSquareFeet, bool exposed, bool accessible, ProspectingSignSeverity signs, ProspectingMethodKind method,
            int requiredHands, string hazardDeclarationId, string[] requiredImplementIds, string[] findingIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(patchId) || parentExposureId == null
                || parentExposureId != "" && !Validation.ValidId(parentExposureId) || !Validation.ValidId(changeCauseId)
                || changedAt < default(RuleTime) || areaSquareFeet < 1 || areaSquareFeet > 100
                || !Enum.IsDefined(typeof(ProspectingSignSeverity), signs) || !Enum.IsDefined(typeof(ProspectingMethodKind), method)
                || requiredHands < 0 || requiredHands > 2 || !Validation.ValidId(hazardDeclarationId)
                || requiredImplementIds == null || requiredImplementIds.Length > ProspectingValidation.MaxRecords
                || requiredImplementIds.Any(x => !Validation.ValidId(x))
                || requiredImplementIds.Distinct(StringComparer.Ordinal).Count() != requiredImplementIds.Length
                || findingIds == null || findingIds.Length > ProspectingValidation.MaxRecords || findingIds.Any(x => !Validation.ValidId(x))
                || findingIds.Distinct(StringComparer.Ordinal).Count() != findingIds.Length)
                throw new ArgumentException("Invalid prospecting exposure history.");
            Id = id; PatchId = patchId; ParentExposureId = parentExposureId; ChangeCauseId = changeCauseId; ChangedAt = changedAt;
            AreaSquareFeet = areaSquareFeet; Exposed = exposed; Accessible = accessible; Signs = signs; Method = method;
            RequiredHands = requiredHands; HazardDeclarationId = hazardDeclarationId;
            this.requiredImplementIds = requiredImplementIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.findingIds = findingIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        public static ProspectingExposureRecord FromProfile(ProspectingExposureProfile profile, string parentId, string causeId, RuleTime at)
            => new ProspectingExposureRecord(profile.Id, profile.PatchId, parentId, causeId, at, profile.AreaSquareFeet,
                profile.Exposed, profile.Accessible, profile.Signs, profile.Method, profile.RequiredHands,
                profile.HazardDeclarationId, profile.RequiredImplementIds, profile.FindingIds);
    }

    /// <summary>One 10-active-minute observation job and its deterministic task-check audit.</summary>
    public sealed class ProspectingAttemptRecord
    {
        private readonly string[] findingIds;
        public string Id { get; }
        public string ActorId { get; }
        public string PatchId { get; }
        public string ExposureId { get; }
        public string MethodId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public ProspectingAttemptStatus Status { get; }
        public int WisdomModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int CheckDc { get; }
        public RuleTime? ResolvedAt { get; }
        public RuleTime? ClosedAt { get; }
        public MiningCheckDegree Degree { get; }
        public MiningDiceSelection DiceSelection { get; }
        public int FirstDie { get; }
        public int SecondDie { get; }
        public int Natural { get; }
        public int CheckModifier { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public string InvalidationCauseId { get; }
        public string[] FindingIds => findingIds.ToArray();

        public ProspectingAttemptRecord(string id, string actorId, string patchId, string exposureId, string methodId,
            RuleTime startedAt, RuleTime updatedAt, RuleTime workDone, ProspectingAttemptStatus status, int wisdomModifier,
            int proficiencyRank, int proficiencyBonus, int checkDc, RuleTime? resolvedAt, RuleTime? closedAt,
            MiningCheckDegree degree, MiningDiceSelection diceSelection, int firstDie, int secondDie, int natural,
            int checkModifier, uint randomBefore, uint randomAfter, long wordsConsumed, string invalidationCauseId,
            string[] findingIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(patchId)
                || !Validation.ValidId(exposureId) || !Validation.ValidId(methodId) || startedAt > updatedAt
                || workDone < default(RuleTime) || workDone > new RuleTime(600) || !Enum.IsDefined(typeof(ProspectingAttemptStatus), status)
                || proficiencyRank < 0 || proficiencyRank > 2 || proficiencyBonus < 0 || proficiencyBonus > 20
                || checkDc < 1 || checkDc > 100 || !Enum.IsDefined(typeof(MiningCheckDegree), degree)
                || !Enum.IsDefined(typeof(MiningDiceSelection), diceSelection) || firstDie < 0 || firstDie > 20
                || secondDie < 0 || secondDie > 20 || natural < 0 || natural > 20 || wordsConsumed < 0
                || invalidationCauseId == null || invalidationCauseId != "" && !Validation.ValidId(invalidationCauseId)
                || findingIds == null || findingIds.Length > ProspectingValidation.MaxRecords
                || findingIds.Any(x => !Validation.ValidId(x)) || findingIds.Distinct(StringComparer.Ordinal).Count() != findingIds.Length)
                throw new ArgumentException("Invalid prospecting attempt.");
            bool resolved = status == ProspectingAttemptStatus.Success || status == ProspectingAttemptStatus.CriticalSuccess
                || status == ProspectingAttemptStatus.Failure || status == ProspectingAttemptStatus.CriticalFailure;
            bool invalidated = status == ProspectingAttemptStatus.InvalidatedWithoutCheck;
            bool dieValid = diceSelection == MiningDiceSelection.Normal ? secondDie == 0 && natural == firstDie
                : diceSelection == MiningDiceSelection.Advantage ? secondDie >= 1 && natural == Math.Max(firstDie, secondDie)
                : diceSelection == MiningDiceSelection.Disadvantage && secondDie >= 1 && natural == Math.Min(firstDie, secondDie);
            if (resolved != (resolvedAt.HasValue && degree != MiningCheckDegree.None && diceSelection != MiningDiceSelection.None
                    && firstDie >= 1 && natural >= 1 && randomBefore != 0 && randomAfter != 0 && wordsConsumed > 0)
                || resolved && (!dieValid || workDone != new RuleTime(600)) || resolved != resolvedAt.HasValue
                || (resolved || invalidated) != closedAt.HasValue || closedAt.HasValue && closedAt.Value != updatedAt
                || resolvedAt.HasValue && resolvedAt.Value != updatedAt
                || (status == ProspectingAttemptStatus.Working || status == ProspectingAttemptStatus.Paused) && workDone >= new RuleTime(600)
                || status == ProspectingAttemptStatus.AwaitingCheck && workDone != new RuleTime(600)
                || invalidated != (invalidationCauseId != "")
                || !resolved && !invalidated && (resolvedAt.HasValue || closedAt.HasValue || degree != MiningCheckDegree.None
                    || diceSelection != MiningDiceSelection.None || firstDie != 0 || secondDie != 0 || natural != 0
                    || randomBefore != 0 || randomAfter != 0 || wordsConsumed != 0 || invalidationCauseId != "")
                || resolved && ((status == ProspectingAttemptStatus.Success) != (degree == MiningCheckDegree.Success)
                    || (status == ProspectingAttemptStatus.CriticalSuccess) != (degree == MiningCheckDegree.CriticalSuccess)
                    || (status == ProspectingAttemptStatus.Failure) != (degree == MiningCheckDegree.Failure)
                    || (status == ProspectingAttemptStatus.CriticalFailure) != (degree == MiningCheckDegree.CriticalFailure))
                || invalidated && (degree != MiningCheckDegree.None || diceSelection != MiningDiceSelection.None || firstDie != 0
                    || secondDie != 0 || natural != 0 || randomBefore != 0 || randomAfter != 0 || wordsConsumed != 0 || findingIds.Length != 0)
                || (status != ProspectingAttemptStatus.Success && status != ProspectingAttemptStatus.CriticalSuccess) && findingIds.Length != 0)
                throw new ArgumentException("Prospecting outcome does not match its persisted check.");
            Id = id; ActorId = actorId; PatchId = patchId; ExposureId = exposureId; MethodId = methodId;
            StartedAt = startedAt; UpdatedAt = updatedAt; WorkDone = workDone; Status = status; WisdomModifier = wisdomModifier;
            ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus; CheckDc = checkDc;
            ResolvedAt = resolvedAt; ClosedAt = closedAt; Degree = degree; DiceSelection = diceSelection;
            FirstDie = firstDie; SecondDie = secondDie; Natural = natural; CheckModifier = checkModifier;
            RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
            InvalidationCauseId = invalidationCauseId; this.findingIds = findingIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        public ProspectingAttemptRecord WithWork(RuleTime updatedAt, RuleTime workDone, ProspectingAttemptStatus status)
            => Copy(updatedAt, workDone, status, null, null, MiningCheckDegree.None, MiningDiceSelection.None,
                0, 0, 0, 0, 0, 0, 0, "", Array.Empty<string>());

        public ProspectingAttemptRecord WithResult(RuleTime at, ProspectingAttemptStatus status, MiningCheckDegree degree,
            MiningDiceSelection diceSelection, int firstDie, int secondDie, int natural, int checkModifier,
            uint randomBefore, uint randomAfter, long wordsConsumed, string[] learnedFindingIds)
            => Copy(at, new RuleTime(600), status, at, at, degree, diceSelection, firstDie, secondDie, natural,
                checkModifier, randomBefore, randomAfter, wordsConsumed, "", learnedFindingIds);

        public ProspectingAttemptRecord Invalidate(RuleTime at, string causeId)
            => Copy(at, WorkDone, ProspectingAttemptStatus.InvalidatedWithoutCheck, null, at, MiningCheckDegree.None,
                MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, causeId, Array.Empty<string>());

        private ProspectingAttemptRecord Copy(RuleTime at, RuleTime work, ProspectingAttemptStatus status,
            RuleTime? resolvedAt, RuleTime? closedAt, MiningCheckDegree degree, MiningDiceSelection diceSelection,
            int firstDie, int secondDie, int natural, int checkModifier, uint randomBefore, uint randomAfter,
            long wordsConsumed, string invalidationCauseId, string[] learnedFindingIds)
            => new ProspectingAttemptRecord(Id, ActorId, PatchId, ExposureId, MethodId, StartedAt, at, work, status,
                WisdomModifier, ProficiencyRank, ProficiencyBonus, CheckDc, resolvedAt, closedAt, degree, diceSelection,
                firstDie, secondDie, natural, checkModifier, randomBefore, randomAfter, wordsConsumed, invalidationCauseId, learnedFindingIds);
    }

    public static class ProspectingValidation
    {
        public const int MaxRecords = 64;
        public const int WorkSeconds = 600;
        public static int Difficulty(ProspectingSignSeverity signs)
        {
            switch (signs) {
                case ProspectingSignSeverity.Clear: return 12;
                case ProspectingSignSeverity.Obscured: return 15;
                case ProspectingSignSeverity.SevereFeasible: return 18;
                default: throw new ArgumentOutOfRangeException(nameof(signs));
            }
        }

        private static RuleTime Add(RuleTime first, RuleTime second)
            => RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator * second.Denominator
                + (System.Numerics.BigInteger)second.Numerator * first.Denominator,
                (System.Numerics.BigInteger)first.Denominator * second.Denominator);
        private static RuleTime Subtract(RuleTime first, RuleTime second)
            => RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator * second.Denominator
                - (System.Numerics.BigInteger)second.Numerator * first.Denominator,
                (System.Numerics.BigInteger)first.Denominator * second.Denominator);

        public static void Validate(Snapshot s)
        {
            if (s.ProspectingPatches == null || s.ProspectingExposures == null || s.ProspectingAttempts == null
                || new[] { s.ProspectingPatches.Length, s.ProspectingExposures.Length, s.ProspectingAttempts.Length }.Any(x => x > MaxRecords)
                || s.ProspectingPatches.Any(x => x == null) || s.ProspectingExposures.Any(x => x == null) || s.ProspectingAttempts.Any(x => x == null))
                throw new ArgumentException("Invalid prospecting collections.");
            if (s.SchemaVersion < Snapshot.ProspectingSchema) {
                if (s.ProspectingPatches.Length + s.ProspectingExposures.Length + s.ProspectingAttempts.Length != 0)
                    throw new ArgumentException("Prospecting requires schema44.");
                return;
            }
            if (s.ProspectingPatches.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ProspectingPatches.Length
                || s.ProspectingExposures.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ProspectingExposures.Length
                || s.ProspectingAttempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ProspectingAttempts.Length
                || s.ProspectingAttempts.Select(x => x.ExposureId).Distinct(StringComparer.Ordinal).Count() != s.ProspectingAttempts.Length)
                throw new ArgumentException("Duplicate prospecting identity or opportunity claim.");
            foreach (var patch in s.ProspectingPatches) {
                if (!s.Actors.Any(x => x.Id == patch.OwnerId) || !s.ProspectingExposures.Any(x => x.Id == patch.CurrentExposureId && x.PatchId == patch.Id))
                    throw new ArgumentException("Prospecting patch references an unknown owner or exposure.");
                var exposures = s.ProspectingExposures.Where(x => x.PatchId == patch.Id).ToArray();
                if (exposures.Length == 0 || exposures.Any(x => x.ChangedAt > s.RuleClock)
                    || exposures.Count(x => x.ParentExposureId == "") != 1
                    || exposures.Where(x => x.ParentExposureId != "").Any(x => !exposures.Any(p => p.Id == x.ParentExposureId && p.ChangedAt < x.ChangedAt)))
                    throw new ArgumentException("Prospecting exposure history is incomplete or out of order.");
                var current = exposures.SingleOrDefault(x => x.Id == patch.CurrentExposureId);
                var reachable = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
                var cursor = current;
                while (cursor != null && reachable.Add(cursor.Id))
                    cursor = cursor.ParentExposureId == "" ? null : exposures.SingleOrDefault(x => x.Id == cursor.ParentExposureId);
                if (current == null || reachable.Count != exposures.Length)
                    throw new ArgumentException("Prospecting current exposure is not the latest recorded version.");
            }
            foreach (var exposure in s.ProspectingExposures) {
                if (!s.ProspectingPatches.Any(x => x.Id == exposure.PatchId)
                    || exposure.HazardDeclarationId != "TEST_ONLY.prospecting.hazard.none")
                    throw new ArgumentException("Prospecting exposure is outside the admitted observable, accessible, no-hazard profile.");
                if (exposure.FindingIds.Distinct(StringComparer.Ordinal).Count() != exposure.FindingIds.Length)
                    throw new ArgumentException("Duplicate prospecting finding reference.");
            }
            foreach (var attempt in s.ProspectingAttempts) {
                var exposure = s.ProspectingExposures.SingleOrDefault(x => x.Id == attempt.ExposureId && x.PatchId == attempt.PatchId)
                    ?? throw new ArgumentException("Prospecting attempt references an unknown exposure.");
                var patch = s.ProspectingPatches.Single(x => x.Id == attempt.PatchId);
                if (attempt.MethodId != exposure.Id + ".method" || attempt.CheckDc != Difficulty(exposure.Signs)
                    || !s.Actors.Any(x => x.Id == attempt.ActorId) || attempt.UpdatedAt > s.RuleClock
                    || attempt.ResolvedAt > s.RuleClock || attempt.ClosedAt > s.RuleClock)
                    throw new ArgumentException("Prospecting attempt does not match its authored exposure.");
                bool open = attempt.Status == ProspectingAttemptStatus.Working || attempt.Status == ProspectingAttemptStatus.Paused
                    || attempt.Status == ProspectingAttemptStatus.AwaitingCheck;
                if (open && patch.CurrentExposureId != attempt.ExposureId)
                    throw new ArgumentException("An open prospecting attempt cannot target a superseded exposure.");
                if (attempt.Status == ProspectingAttemptStatus.Working
                    && !s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == attempt.ActorId && w.Start <= s.RuleClock && w.End > s.RuleClock))
                    throw new ArgumentException("Working prospecting attempt has no active shared work interval.");
                var intervals = s.Work.WorkerIntervals.Where(w => w.JobId == attempt.Id)
                    .OrderBy(w => w.Start).ThenBy(w => w.Id, StringComparer.Ordinal).ToArray();
                if (intervals.Length == 0 || intervals.Any(w => w.WorkerId != attempt.ActorId || w.Start < attempt.StartedAt)
                    || s.Work.Reservations.Any(r => r.JobId == attempt.Id))
                    throw new ArgumentException("Prospecting job has invalid work provenance or unexpected resource reservations.");
                var active = intervals.Where(w => w.Start <= s.RuleClock && w.End > s.RuleClock).ToArray();
                if (attempt.Status == ProspectingAttemptStatus.Working) {
                    RuleTime bookedRemaining = active.Length == 1 ? Subtract(active[0].End, s.RuleClock) : default;
                    RuleTime workRemaining = Subtract(new RuleTime(WorkSeconds), attempt.WorkDone);
                    if (active.Length != 1 || bookedRemaining != workRemaining)
                        throw new ArgumentException("Working prospecting attempt has no exact remaining interval.");
                } else if (active.Length != 0) throw new ArgumentException("Inactive prospecting attempt retains an active worker interval.");
                RuleTime credited = default;
                for (int i = 0; i < intervals.Length; i++) {
                    if (i > 0 && intervals[i - 1].End > intervals[i].Start)
                        throw new ArgumentException("Prospecting labor intervals overlap.");
                    if (intervals[i].Start >= s.RuleClock) continue;
                    RuleTime end = intervals[i].End < s.RuleClock ? intervals[i].End : s.RuleClock;
                    if (end > intervals[i].Start) credited = Add(credited, Subtract(end, intervals[i].Start));
                }
                if (credited != attempt.WorkDone)
                    throw new ArgumentException("Prospecting recorded work differs from its shared intervals.");
                if ((attempt.Status == ProspectingAttemptStatus.Success || attempt.Status == ProspectingAttemptStatus.CriticalSuccess)
                    && !attempt.FindingIds.SequenceEqual(exposure.FindingIds.OrderBy(x => x, StringComparer.Ordinal)))
                    throw new ArgumentException("Successful prospecting must reveal exactly the authored observations.");
                if (attempt.FindingIds.Any(id => !exposure.FindingIds.Contains(id, StringComparer.Ordinal)))
                    throw new ArgumentException("Prospecting attempt references a finding outside its exposure.");
            }
            if (s.ProspectingAttempts.Where(x => x.Status == ProspectingAttemptStatus.Working || x.Status == ProspectingAttemptStatus.Paused
                || x.Status == ProspectingAttemptStatus.AwaitingCheck).GroupBy(x => x.PatchId, StringComparer.Ordinal).Any(g => g.Count() > 1))
                throw new ArgumentException("A prospecting patch cannot have concurrent workers.");
        }
    }
}
