using System;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation
{
    public enum TemporaryCampConstructionStatus { Working, Paused, AwaitingCheck, Resolved }
    public enum TemporaryCampConstructionResult { CriticalFailure = 0, Failure = 1, Success = 2, CriticalSuccess = 3 }
    public enum TemporaryCampFixtureKind { TwoPersonTent, FittingPack }

    /// <summary>TEST_ONLY work attempt over one existing expedition camp site.</summary>
    public sealed class TemporaryCampConstructionAttemptRecord
    {
        private readonly string[] assistants;
        public string Id { get; }
        public string SiteId { get; }
        public string RouteId { get; }
        public int RouteTier { get; }
        public string ProfileFingerprint { get; }
        public string LeadId { get; }
        public string SkillId { get; }
        public CharacterAbility Ability { get; }
        public string TentLotId { get; }
        public string PackLotId { get; }
        public ReadOnlyCollection<string> AssistantIds { get; }
        public long StartedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkRequired { get; }
        public RuleTime WorkDone { get; }
        public TemporaryCampConstructionStatus Status { get; }
        public TemporaryCampConstructionCheckRecord Check { get; }

        public TemporaryCampConstructionAttemptRecord(string id, string siteId, string routeId, int routeTier,
            string profileFingerprint, string leadId, string skillId, CharacterAbility ability,
            string tentLotId, string packLotId, string[] assistantIds, long startedRevision,
            RuleTime startedAt, RuleTime updatedAt, RuleTime workRequired, RuleTime workDone,
            TemporaryCampConstructionStatus status, TemporaryCampConstructionCheckRecord check = null)
        {
            var crew = assistantIds ?? Array.Empty<string>();
            if (!Validation.ValidId(id) || !Validation.ValidId(siteId) || !Validation.ValidId(routeId)
                || routeTier < 1 || routeTier > 6 || !Validation.ValidId(profileFingerprint)
                || !Validation.ValidId(leadId) || !Validation.ValidId(skillId)
                || !Enum.IsDefined(typeof(CharacterAbility), ability)
                || !Validation.ValidId(tentLotId) || !Validation.ValidId(packLotId) || tentLotId == packLotId
                || crew.Length > 3 || crew.Any(x => !Validation.ValidId(x))
                || crew.Distinct(StringComparer.Ordinal).Count() != crew.Length || crew.Contains(leadId, StringComparer.Ordinal)
                || startedRevision < 1 || updatedAt < startedAt || workRequired <= default(RuleTime)
                || workDone < default(RuleTime) || workDone > workRequired
                || !Enum.IsDefined(typeof(TemporaryCampConstructionStatus), status)
                || status == TemporaryCampConstructionStatus.AwaitingCheck && (workDone != workRequired || check != null)
                || status == TemporaryCampConstructionStatus.Resolved && (workDone != workRequired || check == null)
                || status != TemporaryCampConstructionStatus.Resolved && check != null)
                throw new ArgumentException("Invalid temporary-camp construction attempt.");
            Id = id; SiteId = siteId; RouteId = routeId; RouteTier = routeTier; ProfileFingerprint = profileFingerprint;
            LeadId = leadId; SkillId = skillId; Ability = ability; TentLotId = tentLotId; PackLotId = packLotId;
            assistants = (string[])crew.Clone(); AssistantIds = Array.AsReadOnly(assistants);
            StartedRevision = startedRevision; StartedAt = startedAt; UpdatedAt = updatedAt;
            WorkRequired = workRequired; WorkDone = workDone; Status = status; Check = check;
        }

        public TemporaryCampConstructionAttemptRecord WithProgress(RuleTime at, RuleTime workDone,
            TemporaryCampConstructionStatus status)
            => new TemporaryCampConstructionAttemptRecord(Id, SiteId, RouteId, RouteTier, ProfileFingerprint,
                LeadId, SkillId, Ability, TentLotId, PackLotId, assistants, StartedRevision, StartedAt,
                at, WorkRequired, workDone, status);

        public TemporaryCampConstructionAttemptRecord WithCheck(TemporaryCampConstructionCheckRecord check)
            => new TemporaryCampConstructionAttemptRecord(Id, SiteId, RouteId, RouteTier, ProfileFingerprint,
                LeadId, SkillId, Ability, TentLotId, PackLotId, assistants, StartedRevision, StartedAt,
                check.At, WorkRequired, WorkRequired, TemporaryCampConstructionStatus.Resolved, check);
    }

    /// <summary>Character, condition, and deterministic dice evidence for one completion check.</summary>
    public sealed class TemporaryCampConstructionCheckRecord
    {
        private readonly int[] linkedInjuries;
        public string CommandId { get; }
        public long AppliedRevision { get; }
        public RuleTime At { get; }
        public int LeadModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int InjuryPenalty { get; }
        public int StrainModifier { get; }
        public int AssistantBonus { get; }
        public int Dc { get; }
        public int ConditionOperationCount { get; }
        public bool Disadvantage { get; }
        public ReadOnlyCollection<int> LinkedInjuriesAtCheck { get; }
        public int FirstRoll { get; }
        public int SecondRoll { get; }
        public int Natural { get; }
        public int Total { get; }
        public TemporaryCampConstructionResult Result { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public int WordsConsumed { get; }

        public TemporaryCampConstructionCheckRecord(string commandId, long appliedRevision, RuleTime at,
            int leadModifier, int proficiencyRank, int proficiencyBonus, int injuryPenalty, int strainModifier,
            int assistantBonus, int dc, int conditionOperationCount, bool disadvantage, int[] linkedInjuriesAtCheck,
            int firstRoll, int secondRoll, int natural, int total, TemporaryCampConstructionResult result,
            uint randomBefore, uint randomAfter, int wordsConsumed)
        {
            var injuries = linkedInjuriesAtCheck ?? Array.Empty<int>();
            if (!Validation.ValidId(commandId) || appliedRevision < 1 || proficiencyRank < 0 || proficiencyRank > 2
                || proficiencyBonus < 0 || assistantBonus < 0 || assistantBonus > 3 || dc < 1
                || conditionOperationCount < 0 || injuries.Length > 3 || injuries.Any(x => x < 0)
                || firstRoll < 1 || firstRoll > 20 || secondRoll < 0 || secondRoll > 20
                || natural < 1 || natural > 20 || (disadvantage ? secondRoll < 1 : secondRoll != 0)
                || total != natural + leadModifier + assistantBonus
                || !Enum.IsDefined(typeof(TemporaryCampConstructionResult), result)
                || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 1 || wordsConsumed > 4)
                throw new ArgumentException("Invalid temporary-camp construction check.");
            CommandId = commandId; AppliedRevision = appliedRevision; At = at; LeadModifier = leadModifier;
            ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus; InjuryPenalty = injuryPenalty;
            StrainModifier = strainModifier; AssistantBonus = assistantBonus; Dc = dc;
            ConditionOperationCount = conditionOperationCount; Disadvantage = disadvantage;
            linkedInjuries = (int[])injuries.Clone(); LinkedInjuriesAtCheck = Array.AsReadOnly(linkedInjuries);
            FirstRoll = firstRoll; SecondRoll = secondRoll; Natural = natural; Total = total; Result = result;
            RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    /// <summary>Links a successful attempt to an installed physical fixture without consuming its lot.</summary>
    public sealed class TemporaryCampInstallationRecord
    {
        public string Id { get; }
        public string AttemptId { get; }
        public string SiteId { get; }
        public string LotId { get; }
        public TemporaryCampFixtureKind Kind { get; }
        public RuleTime InstalledAt { get; }
        public long AppliedRevision { get; }
        public TemporaryCampInstallationRecord(string id, string attemptId, string siteId, string lotId,
            TemporaryCampFixtureKind kind, RuleTime installedAt, long appliedRevision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(attemptId) || !Validation.ValidId(siteId)
                || !Validation.ValidId(lotId) || !Enum.IsDefined(typeof(TemporaryCampFixtureKind), kind)
                || appliedRevision < 1)
                throw new ArgumentException("Invalid temporary-camp installation record.");
            Id = id; AttemptId = attemptId; SiteId = siteId; LotId = lotId; Kind = kind;
            InstalledAt = installedAt; AppliedRevision = appliedRevision;
        }
    }

    /// <summary>Structural checks shared by in-memory snapshots and save decoding. Rule replay stays in LabModel.</summary>
    public static class TemporaryCampConstructionValidation
    {
        public const int MaxAttempts = 64;
        public const int MaxInstallations = 128;
        public static void Validate(Snapshot s)
        {
            if (s.TemporaryCampConstructionAttempts == null || s.TemporaryCampInstallations == null
                || s.TemporaryCampConstructionAttempts.Length > MaxAttempts
                || s.TemporaryCampInstallations.Length > MaxInstallations
                || s.TemporaryCampConstructionAttempts.Any(x => x == null)
                || s.TemporaryCampInstallations.Any(x => x == null))
                throw new ArgumentException("Invalid temporary-camp construction collections.");
            var attempts = s.TemporaryCampConstructionAttempts; var installs = s.TemporaryCampInstallations;
            if (s.SchemaVersion < Snapshot.TemporaryCampConstructionSchema)
            {
                if (attempts.Length != 0 || installs.Length != 0)
                    throw new ArgumentException("Temporary-camp construction requires schema70.");
                return;
            }
            if (attempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != attempts.Length
                || installs.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != installs.Length
                || installs.Select(x => x.LotId).Distinct(StringComparer.Ordinal).Count() != installs.Length
                || attempts.Any(x => x.StartedRevision > s.Revision || x.UpdatedAt > s.RuleClock
                    || !s.ExpeditionCampSites.Any(site => site.Id == x.SiteId && site.RouteId == x.RouteId)
                    || x.Check != null && (x.Check.AppliedRevision > s.Revision || x.Check.At > s.RuleClock)))
                throw new ArgumentException("Duplicate, future, or unbound temporary-camp construction history.");
            foreach (var attempt in attempts)
            {
                var crew = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
                if (s.Work.WorkerIntervals.Where(x => x.JobId == attempt.Id).Any(x => !crew.Contains(x.WorkerId, StringComparer.Ordinal)))
                    throw new ArgumentException("Temporary-camp work has an unbound worker.");
                if (attempt.Status == TemporaryCampConstructionStatus.AwaitingCheck
                    && (attempt.WorkDone != attempt.WorkRequired || attempt.Check != null))
                    throw new ArgumentException("Awaiting temporary-camp check has incomplete work.");
                var claims = s.Work.Reservations.Where(x => x.JobId == attempt.Id).ToArray();
                if (claims.Length != 2
                    || claims.Count(x => x.LotId == attempt.TentLotId && x.Amount == new RuleQuantity(20)) != 1
                    || claims.Count(x => x.LotId == attempt.PackLotId && x.Amount == new RuleQuantity(20)) != 1)
                    throw new ArgumentException("Temporary-camp attempt must retain its exact tent and pack claims.");
                if (attempt.Status == TemporaryCampConstructionStatus.Resolved
                    && attempt.Check.Result >= TemporaryCampConstructionResult.Success)
                {
                    if (claims.Any(x => x.RemainingAmount == default || x.ReleasedAmount != default)
                        || installs.Count(x => x.AttemptId == attempt.Id) != 2)
                        throw new ArgumentException("Successful temporary-camp attempt lost fixture claims or installations.");
                }
                else if (attempt.Status == TemporaryCampConstructionStatus.Resolved
                    && (claims.Any(x => x.RemainingAmount != default || x.ReleasedAmount != x.Amount)
                        || installs.Any(x => x.AttemptId == attempt.Id)))
                    throw new ArgumentException("Failed temporary-camp attempt did not release unused fixtures.");
                else if (attempt.Status != TemporaryCampConstructionStatus.Resolved
                    && claims.Any(x => x.RemainingAmount == default))
                    throw new ArgumentException("Open temporary-camp attempt lost reserved fixtures.");
            }
            foreach (var installation in installs)
            {
                var attempt = attempts.SingleOrDefault(x => x.Id == installation.AttemptId);
                string expectedLot = installation.Kind == TemporaryCampFixtureKind.TwoPersonTent
                    ? attempt?.TentLotId : attempt?.PackLotId;
                if (attempt == null || attempt.Status != TemporaryCampConstructionStatus.Resolved
                    || attempt.Check.Result < TemporaryCampConstructionResult.Success
                    || installation.SiteId != attempt.SiteId || installation.LotId != expectedLot
                    || installation.InstalledAt != attempt.Check.At || installation.AppliedRevision != attempt.Check.AppliedRevision
                    || !s.Work.Lots.Any(x => x.Id == installation.LotId))
                    throw new ArgumentException("Temporary-camp installation is not backed by a successful physical fixture.");
            }
            if (installs.GroupBy(x => x.AttemptId, StringComparer.Ordinal).Any(g => g.Count(x => x.Kind == TemporaryCampFixtureKind.TwoPersonTent) != 1
                || g.Count(x => x.Kind == TemporaryCampFixtureKind.FittingPack) != 1))
                throw new ArgumentException("Temporary-camp install set is incomplete or duplicated.");
            foreach (var attempt in attempts.Where(x => x.Check != null))
            {
                var receipt = s.Receipts.SingleOrDefault(x => x.Id == attempt.Check.CommandId);
                if (receipt == null || receipt.Revision != attempt.Check.AppliedRevision)
                    throw new ArgumentException("Temporary-camp check is not bound to a command receipt.");
            }
        }

        /// <summary>Support marks are derived from completed checks; no parallel mutable mark total is stored.</summary>
        public static int SupportMarks(Snapshot s, string siteId)
        {
            if (s == null || !Validation.ValidId(siteId) || s.TemporaryCampConstructionAttempts == null) return 0;
            return s.TemporaryCampConstructionAttempts
                .Where(x => x.SiteId == siteId && x.Status == TemporaryCampConstructionStatus.Resolved && x.Check != null)
                .Sum(x => x.Check.Result == TemporaryCampConstructionResult.Success ? 1
                    : x.Check.Result == TemporaryCampConstructionResult.CriticalSuccess ? 2 : 0);
        }

        public static bool HasTemporaryCamp(Snapshot s, string siteId)
            => s != null && Validation.ValidId(siteId) && SupportMarks(s, siteId) > 0
                && s.TemporaryCampInstallations.Count(x => x.SiteId == siteId && x.Kind == TemporaryCampFixtureKind.TwoPersonTent) == 1
                && s.TemporaryCampInstallations.Count(x => x.SiteId == siteId && x.Kind == TemporaryCampFixtureKind.FittingPack) == 1;

        public static TemporaryCampStorageCapacity StorageCapacity(Snapshot s, string siteId)
        {
            if (!HasTemporaryCamp(s, siteId)) throw new InvalidOperationException("Temporary Camp is not installed at this site.");
            return new TemporaryCampStorageCapacity(20, new RuleQuantity(200), new RuleQuantity(20));
        }

        public static int TierDc(int tier)
        {
            switch (tier) { case 1: return 12; case 2: return 13; case 3: return 15; case 4: return 16; case 5: return 18; case 6: return 19;
                default: throw new ArgumentOutOfRangeException(nameof(tier)); }
        }
    }

    public readonly struct TemporaryCampStorageCapacity
    {
        public int Load { get; }
        public RuleQuantity Pounds { get; }
        public RuleQuantity CubicFeet { get; }
        public TemporaryCampStorageCapacity(int load, RuleQuantity pounds, RuleQuantity cubicFeet)
        {
            if (load < 1 || pounds <= default(RuleQuantity) || cubicFeet <= default(RuleQuantity))
                throw new ArgumentException("Invalid Temporary Camp storage capacity.");
            Load = load; Pounds = pounds; CubicFeet = cubicFeet;
        }
    }
}
