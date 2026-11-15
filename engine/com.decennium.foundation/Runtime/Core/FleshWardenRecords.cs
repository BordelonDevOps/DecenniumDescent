using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum MutationTier { Basic }
    public enum MutationTree { Vital }

    /// <summary>Explicit fixture qualification, distinct from the shared mutation ownership grants.</summary>
    public sealed class MutationQualificationRecord
    {
        public string ActorId { get; }
        public string SourceRevision { get; }
        public MutationTier Tier { get; }
        public MutationTree Tree { get; }
        public MutationQualificationRecord(string actor, string sourceRevision, MutationTier tier, MutationTree tree)
        {
            if (!Validation.ValidId(actor) || !Validation.ValidId(sourceRevision)
                || !Enum.IsDefined(typeof(MutationTier), tier) || !Enum.IsDefined(typeof(MutationTree), tree))
                throw new ArgumentException("Invalid mutation qualification.");
            ActorId = actor; SourceRevision = sourceRevision; Tier = tier; Tree = tree;
        }
    }

    /// <summary>Capacity-only settlement at a real completed rest. HP clamp is not damage or healing.</summary>
    public sealed class MutationCapacityChangeRecord
    {
        public string PreviousMutationId { get; }
        public string PreviousApplicationId { get; }
        public string ApplicationId { get; }
        public long BaseMaximum { get; }
        public long MaximumBefore { get; }
        public long MaximumAfter { get; }
        public long EffectiveBefore { get; }
        public long EffectiveAfter { get; }
        public long HpBefore { get; }
        public long HpAfter { get; }
        public long CapacityClamp => HpBefore - HpAfter;
        public string EventKind => "CapacityChange";
        public int Damage => 0;
        public int Healing => 0;
        public MutationCapacityChangeRecord(string previousMutationId, string previousApplicationId, string applicationId,
            long baseMaximum, long maximumBefore, long maximumAfter, long effectiveBefore, long effectiveAfter, long hpBefore, long hpAfter)
        {
            if (!FleshWardenProfile.IsMutation(previousMutationId)
                || previousApplicationId != "" && !Validation.ValidId(previousApplicationId)
                || applicationId != "" && !Validation.ValidId(applicationId)
                || baseMaximum < 1 || maximumBefore < 1 || maximumAfter < 1
                || effectiveBefore < 1 || effectiveBefore > maximumBefore || effectiveAfter < 1 || effectiveAfter > maximumAfter
                || hpBefore < 0 || hpBefore > effectiveBefore || hpAfter != Math.Min(hpBefore, effectiveAfter))
                throw new ArgumentException("Invalid mutation capacity settlement.");
            PreviousMutationId = previousMutationId; PreviousApplicationId = previousApplicationId; ApplicationId = applicationId;
            BaseMaximum = baseMaximum; MaximumBefore = maximumBefore; MaximumAfter = maximumAfter;
            EffectiveBefore = effectiveBefore; EffectiveAfter = effectiveAfter; HpBefore = hpBefore; HpAfter = hpAfter;
        }
    }

    public sealed class MutationRestChoiceRecord
    {
        public string RestId { get; }
        public string MutationId { get; }
        public MutationCapacityChangeRecord Change { get; }
        public MutationRestChoiceRecord(string restId, string mutationId, MutationCapacityChangeRecord change = null)
        {
            if (!Validation.ValidId(restId) || !FleshWardenProfile.IsMutation(mutationId))
                throw new ArgumentException("Invalid immutable mutation rest choice.");
            RestId = restId; MutationId = mutationId; Change = change;
        }
    }

    /// <summary>One application with actual rest endpoints; same-card rests do not refresh it.</summary>
    public sealed class MutationCapacityApplicationRecord
    {
        public string Id { get; }
        public string SourceId { get; }
        public string SourceRevision { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public int WarriorLevel { get; }
        public long Amount => checked(2L * WarriorLevel);
        public string StartRestId { get; }
        public RuleTime StartedAt { get; }
        public string EndRestId { get; }
        public RuleTime? EndedAt { get; }
        public bool Present => EndRestId == "";
        public MutationCapacityApplicationRecord(string id, string sourceId, string sourceRevision, string ownerId, string targetId,
            int warriorLevel, string startRestId, RuleTime startedAt, string endRestId = "", RuleTime? endedAt = null)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(sourceId) || !Validation.ValidId(sourceRevision)
                || !Validation.ValidId(ownerId) || !Validation.ValidId(targetId) || !Validation.ValidId(startRestId)
                || warriorLevel < 1 || warriorLevel > 20 || startedAt < default(RuleTime)
                || (endRestId == "" ? endedAt.HasValue : !Validation.ValidId(endRestId) || !endedAt.HasValue || endedAt < startedAt))
                throw new ArgumentException("Invalid mutation capacity application.");
            Id = id; SourceId = sourceId; SourceRevision = sourceRevision; OwnerId = ownerId; TargetId = targetId;
            WarriorLevel = warriorLevel; StartRestId = startRestId; StartedAt = startedAt; EndRestId = endRestId; EndedAt = endedAt;
        }
        public MutationCapacityApplicationRecord End(ShortRestRecord rest)
            => new MutationCapacityApplicationRecord(Id, SourceId, SourceRevision, OwnerId, TargetId, WarriorLevel,
                StartRestId, StartedAt, rest.Id, rest.EndedAt);
    }

    public sealed class FleshWardenRecord
    {
        public MutationQualificationRecord Qualification { get; }
        public int SlotOrdinal { get; }
        public string EquippedMutationId { get; }
        public string ApplicationId { get; }
        public IReadOnlyList<MutationRestChoiceRecord> Choices { get; }
        public IReadOnlyList<MutationCapacityApplicationRecord> Applications { get; }
        public FleshWardenRecord(MutationQualificationRecord qualification, int slotOrdinal, string equippedMutationId,
            string applicationId, IEnumerable<MutationRestChoiceRecord> choices, IEnumerable<MutationCapacityApplicationRecord> applications)
        {
            if (qualification == null || slotOrdinal != 1 || !FleshWardenProfile.IsMutation(equippedMutationId)
                || applicationId != "" && !Validation.ValidId(applicationId) || choices == null || applications == null)
                throw new ArgumentException("Invalid mutation loadout.");
            var plans = choices.ToArray(); var effects = applications.ToArray();
            if (plans.Length > ShortRestBerth.MaxAttempts || effects.Length > ShortRestBerth.MaxAttempts
                || plans.Any(x => x == null) || effects.Any(x => x == null)) throw new ArgumentException("Invalid mutation history.");
            Qualification = qualification; SlotOrdinal = slotOrdinal; EquippedMutationId = equippedMutationId; ApplicationId = applicationId;
            Choices = Array.AsReadOnly(plans); Applications = Array.AsReadOnly(effects);
        }
    }

    public static class FleshWardenProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.flesh-warden-v1-";
        public const string FleshWarden = "warrior.supplement.flesh-warden";
        public const string SpinalBuffer = "warrior.supplement.spinal-buffer";
        public const string SlotI = "warrior.supplement.mutation-slot-i";
        public const string Actor = ShortRestBerth.Actor;
        public const string SourceRevision = ShortRestBerth.SourceRevision;
        public const byte Marker = 9;
        public static bool IsMutation(string id) => id == FleshWarden || id == SpinalBuffer;
        public static bool SelectedFingerprint(string value) => value.StartsWith(FingerprintPrefix, StringComparison.Ordinal);
        public static string ApplicationIdentity(string restId) => restId + ".flesh-warden";
        public static bool Qualified(Snapshot s)
        {
            var q = s.FleshWarden?.Qualification;
            var c = s.Characters.SingleOrDefault(x => x.ActorId == Actor);
            return s.ConnectedFleshWarden && s.TestOnly && s.SchemaVersion == Snapshot.SurpriseEntrySchema
                && SelectedFingerprint(s.ContentFingerprint) && q?.ActorId == Actor && q.SourceRevision == SourceRevision
                && q.Tier == MutationTier.Basic && q.Tree == MutationTree.Vital && c != null
                && c.ProfileId == "TEST_ONLY.numeric-warrior3" && c.Levels.Count == 3 && c.Levels.All(x => x.ClassName == "Warrior")
                && c.Levels.Select(x => x.BaseHp).SequenceEqual(new[] { 12, 7, 7 })
                && c.Abilities[(int)CharacterAbility.Constitution] == 10;
        }
        private static bool GrantShape(CharacterFeatureGrantRecord g)
            => g.ActorId == Actor && IsMutation(g.FeatureId) && g.Origin == CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement
                && g.ClassName == "Warrior" && g.ClassLevel == 1 && g.MilestoneId == "" && g.GrantedRevision == 0;
        public static bool ValidFixtureGrant(Snapshot s, CharacterFeatureGrantRecord g)
            => Qualified(s) && GrantShape(g) && s.CharacterFeatureGrants.Count(x => x.ActorId == Actor) == 2
                && s.CharacterFeatureGrants.Count(x => GrantShape(x) && x.FeatureId == FleshWarden) == 1
                && s.CharacterFeatureGrants.Count(x => GrantShape(x) && x.FeatureId == SpinalBuffer) == 1;
        public static bool HasEntitlements(Snapshot s)
            => Qualified(s) && s.CharacterFeatureGrants.Count(x => ValidFixtureGrant(s, x)) == 2;
        public static MutationRestChoiceRecord Choice(Snapshot s, string restId)
            => s.FleshWarden?.Choices.SingleOrDefault(x => x.RestId == restId);

        internal static void Validate(Snapshot s)
        {
            if (s.ConnectedFleshWarden != SelectedFingerprint(s.ContentFingerprint)
                || s.ConnectedFleshWarden != (s.FleshWarden != null)) throw new ArgumentException("Invalid Flesh Warden envelope.");
            if (!s.ConnectedFleshWarden) return;
            if (!s.ConnectedShortRest || !HasEntitlements(s)) throw new ArgumentException("Invalid source-qualified mutation access.");
            var record = s.FleshWarden;
            if (record.Choices.Select(x => x.RestId).Distinct(StringComparer.Ordinal).Count() != record.Choices.Count
                || record.Applications.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != record.Applications.Count)
                throw new ArgumentException("Duplicate mutation provenance.");
            string equipped = SpinalBuffer, application = "";
            int benefits = 0, choiceIndex = 0;
            var expectedEffects = new Dictionary<string, MutationCapacityApplicationRecord>(StringComparer.Ordinal);
            foreach (var rest in s.ShortRests) {
                var choice = Choice(s, rest.Id);
                if (choice != null) {
                    if (record.Choices[choiceIndex++] != choice || benefits >= ShortRestBerth.InitialBenefits)
                        throw new ArgumentException("Mutation plan cadence or chronology is unsupported.");
                    bool complete = rest.Outcome == ShortRestOutcome.Completed;
                    if (complete != (choice.Change != null) || complete && rest.Benefit != ShortRestBenefit.Eligible)
                        throw new ArgumentException("Mutation settlement requires a completed eligible rest.");
                    if (complete) {
                        string next = application;
                        if (equipped != choice.MutationId) {
                            if (equipped == FleshWarden) expectedEffects[application] = expectedEffects[application].End(rest);
                            next = choice.MutationId == FleshWarden ? ApplicationIdentity(rest.Id) : "";
                            if (next != "") expectedEffects.Add(next, new MutationCapacityApplicationRecord(next, FleshWarden,
                                SourceRevision, Actor, Actor, 3, rest.Id, rest.EndedAt.Value));
                        }
                        var change = choice.Change;
                        if (change.PreviousMutationId != equipped || change.PreviousApplicationId != application || change.ApplicationId != next
                            || change.BaseMaximum != 26 || change.MaximumBefore != (equipped == FleshWarden ? 32 : 26)
                            || change.MaximumAfter != (choice.MutationId == FleshWarden ? 32 : 26))
                            throw new ArgumentException("Invalid mutation capacity transition attribution.");
                        equipped = choice.MutationId; application = next;
                    }
                }
                if (rest.Benefit == ShortRestBenefit.Eligible) benefits++;
            }
            if (choiceIndex != record.Choices.Count || record.EquippedMutationId != equipped || record.ApplicationId != application
                || record.Applications.Count != expectedEffects.Count || s.Lives.Single(x => x.ActorId == Actor).MaximumHp != (equipped == FleshWarden ? 32 : 26))
                throw new ArgumentException("Invalid mutation loadout or shared capacity.");
            foreach (var actual in record.Applications) {
                if (!expectedEffects.TryGetValue(actual.Id, out var expected) || actual.SourceId != expected.SourceId
                    || actual.SourceRevision != expected.SourceRevision || actual.OwnerId != expected.OwnerId || actual.TargetId != expected.TargetId
                    || actual.WarriorLevel != expected.WarriorLevel || actual.StartRestId != expected.StartRestId
                    || actual.StartedAt != expected.StartedAt || actual.EndRestId != expected.EndRestId || actual.EndedAt != expected.EndedAt)
                    throw new ArgumentException("Invalid actual Flesh Warden application.");
            }
            string kind = ((int)CommandKind.BeginMutationShortRest).ToString(CultureInfo.InvariantCulture) + "|";
            if (s.Receipts.Count(x => x.Fingerprint.StartsWith(kind, StringComparison.Ordinal)) != record.Choices.Count)
                throw new ArgumentException("Unattributed mutation rest choice.");
        }
    }
}
