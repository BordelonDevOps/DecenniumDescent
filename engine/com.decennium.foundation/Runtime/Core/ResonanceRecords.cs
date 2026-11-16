using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>One-time funding provenance, separate from a source-derived capacity.</summary>
    public sealed class ResonanceFundingRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string PolicyId { get; }
        public int Amount { get; }
        public long Revision { get; }
        public ResonanceFundingRecord(string id, string actor, string policy, int amount, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actor) || !Validation.ValidId(policy) || amount < 0 || revision < 0)
                throw new ArgumentException("Invalid RP funding record.");
            Id = id; ActorId = actor; PolicyId = policy; Amount = amount; Revision = revision;
        }
    }

    /// <summary>Character-wide RP balance. Capacity reconciliation never funds a pool.</summary>
    public sealed class ResonancePoolRecord
    {
        public string ActorId { get; }
        public int Maximum { get; }
        public int Current { get; }
        public ResonanceFundingRecord InitialFunding { get; }
        public ResonancePoolRecord(string actor, int maximum, int current, ResonanceFundingRecord initialFunding)
        {
            if (!Validation.ValidId(actor) || maximum < 0 || current < 0 || current > maximum
                || initialFunding == null || initialFunding.ActorId != actor)
                throw new ArgumentException("Invalid shared RP pool.");
            ActorId = actor; Maximum = maximum; Current = current; InitialFunding = initialFunding;
        }
        public ResonancePoolRecord ReconcileCapacity(int maximum)
            => new ResonancePoolRecord(ActorId, maximum, Math.Min(Current, maximum), InitialFunding);
        public ResonancePoolRecord Pay(int amount)
        {
            if (amount <= 0 || amount > Current) throw new ArgumentException("RP payment is not funded.");
            return new ResonancePoolRecord(ActorId, Maximum, Current - amount, InitialFunding);
        }
    }

    /// <summary>Initial class provenance. Levels, abilities, HP, training and grants remain in their shared ledgers.</summary>
    public sealed class ClericClassEntryRecord
    {
        public string ActorId { get; }
        public string SourceRevision { get; }
        public int PointBuyCost { get; }
        public string FavoredWeaponProfile { get; }
        public string EngineSelector { get; }
        public ReadOnlyCollection<string> SelectedSkills { get; }
        public ReadOnlyCollection<string> SavingThrows { get; }
        // These fixed class facts are derived from the persisted, validated source binding.
        // They record training; they do not award equipment or enable an equipment procedure.
        public IReadOnlyList<string> ArmorTraining { get; } = Array.AsReadOnly(new[] { "Light", "Medium", "Shields" });
        public IReadOnlyList<string> WeaponTraining { get; } = Array.AsReadOnly(new[] { "Simple weapons" });
        public IReadOnlyList<string> ToolTraining { get; } = Array.AsReadOnly(new[] { "Religious implements" });
        public string AutomaticEngineName => "Divine Favor";
        public bool ConvictionSupported => false;
        public ClericClassEntryRecord(string actor, string sourceRevision, int pointBuyCost, string favoredWeapon,
            string engineSelector, IEnumerable<string> skills, IEnumerable<string> savingThrows)
        {
            if (!Validation.ValidId(actor) || sourceRevision == null || sourceRevision.Length != 40 || pointBuyCost < 0
                || pointBuyCost > 27 || !Validation.ValidId(favoredWeapon) || engineSelector == null || skills == null || savingThrows == null)
                throw new ArgumentException("Invalid Cleric initial class provenance.");
            var selected = skills.ToArray(); var saves = savingThrows.ToArray();
            if (selected.Length != 2 || saves.Length != 2 || selected.Any(x => !Validation.ValidId(x))
                || saves.Any(x => !Validation.ValidId(x)) || selected.Distinct(StringComparer.Ordinal).Count() != 2
                || saves.Distinct(StringComparer.Ordinal).Count() != 2)
                throw new ArgumentException("Invalid initial Cleric training.");
            ActorId = actor; SourceRevision = sourceRevision; PointBuyCost = pointBuyCost; FavoredWeaponProfile = favoredWeapon;
            EngineSelector = engineSelector; SelectedSkills = Array.AsReadOnly(selected); SavingThrows = Array.AsReadOnly(saves);
        }
    }

    /// <summary>Causal payment and ordinary-healing evidence; ActorLife owns the resulting HP.</summary>
    public sealed class HealingRiteRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public string SourceId { get; }
        public string SourceRevision { get; }
        public int TurnOrdinal { get; }
        public RuleTime At { get; }
        public int RpBefore { get; }
        public int RpPaid { get; }
        public int RpAfter { get; }
        public int Die { get; }
        public int Modifier { get; }
        public long RolledPotential => checked((long)Die + Modifier);
        public long Potential { get; }
        public long HpBefore { get; }
        public long HpAfter { get; }
        public long ActualGain => HpAfter - HpBefore;
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public HealingRiteRecord(string command, long revision, string actor, string target, string source, string sourceRevision,
            int turn, RuleTime at, int rpBefore, int rpPaid, int rpAfter, int die, int modifier,
            long potential, long hpBefore, long hpAfter, uint randomBefore, uint randomAfter, long words)
        {
            if (!Validation.ValidId(command) || revision <= 0 || !Validation.ValidId(actor) || !Validation.ValidId(target)
                || !Validation.ValidId(source) || sourceRevision == null || sourceRevision.Length != 40 || turn < 0
                || at < default(RuleTime) || rpPaid <= 0 || rpBefore < rpPaid || rpAfter != rpBefore - rpPaid
                || die < 1 || die > 8 || modifier < 1 || potential < 0 || potential > checked((long)die + modifier)
                || hpBefore < 0 || hpAfter < hpBefore || hpAfter - hpBefore > potential || randomBefore == 0 || randomAfter == 0 || words < 1)
                throw new ArgumentException("Invalid Healing Rite payment/result.");
            CommandId = command; Revision = revision; ActorId = actor; TargetId = target; SourceId = source; SourceRevision = sourceRevision;
            TurnOrdinal = turn; At = at; RpBefore = rpBefore; RpPaid = rpPaid; RpAfter = rpAfter; Die = die; Modifier = modifier;
            Potential = potential; HpBefore = hpBefore; HpAfter = hpAfter; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = words;
        }
    }

    public static class ClericRpProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.cleric-rp-v1-";
        public const string CharacterProfile = "TEST_ONLY.initial-cleric1";
        public const string Actor = ConnectedVialRules.CompanionRecipientId;
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string HealingRite = "cleric.base.healing-rite";
        public const string FundingPolicy = "TEST_ONLY.cleric-initial-rp3";
        public const string FundingId = "TEST_ONLY.cleric-rp-genesis";
        public const string FavoredWeapon = "simple-melee-weapons.club";
        public const string EngineSelector = "data/public/class_playtests/cleric.json#/engine/9";
        public const byte Marker = 10;
        public static IReadOnlyList<string> SelectedCards { get; } = Array.AsReadOnly(new[] {
            "cleric.base.consecrate", "cleric.base.consecrated-ground", "cleric.base.fervent-ritualist", HealingRite });
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            || ClericRepertoireProfile.SelectedFingerprint(value));
        public static bool ValidInitialGrant(Snapshot s, CharacterFeatureGrantRecord grant)
            => s.ConnectedClericRp && grant.ActorId == Actor && grant.ClassName == "Cleric" && grant.ClassLevel == 1
                && grant.Origin == CharacterFeatureGrantOrigin.InitialClassSelection && grant.MilestoneId == ""
                && grant.GrantedRevision == 0 && SelectedCards.Contains(grant.FeatureId, StringComparer.Ordinal);
        public static bool ValidInitialSelection(Snapshot s, CharacterInitialClassSelectionRecord selection)
            => s.ConnectedClericRp && selection.ActorId == Actor && selection.ClassName == "Cleric" && selection.ClassLevel == 1
                && selection.SourceRevision == SourceRevision && selection.SelectedFeatureIds.SequenceEqual(SelectedCards, StringComparer.Ordinal);

        internal static void Validate(Snapshot state)
        {
            bool selected = SelectedFingerprint(state.ContentFingerprint);
            if (state.ResonancePools == null || state.HealingRites == null || state.ResonancePools.Any(x => x == null)
                || state.HealingRites.Any(x => x == null) || state.HealingRites.Length > 128
                || selected != state.ConnectedClericRp
                || !selected && (state.ClericEntry != null || state.ResonancePools.Length != 0 || state.HealingRites.Length != 0))
                throw new ArgumentException("Invalid Cleric RP envelope.");
            if (!selected) return;
            if (!state.TestOnly || state.SchemaVersion != Snapshot.SurpriseEntrySchema || state.ConnectedBatch == null
                || state.ConnectedCarriedVial || state.ConnectedShortRest || state.ResonancePools.Length != 1)
                throw new ArgumentException("Cleric RP requires its exact connected profile.");
            var entry = state.ClericEntry;
            var character = state.Characters.Single(x => x.ActorId == Actor);
            var life = state.Lives.Single(x => x.ActorId == Actor);
            var pool = state.ResonancePools[0]; var funding = pool.InitialFunding;
            bool earned = state.ConnectedClericSettlement && state.ClericInvocationPath != null;
            if (entry == null || entry.ActorId != Actor || entry.SourceRevision != SourceRevision || entry.PointBuyCost != 17
                || entry.FavoredWeaponProfile != FavoredWeapon || entry.EngineSelector != EngineSelector
                || !entry.SelectedSkills.SequenceEqual(new[] { "medicine", "religion" }, StringComparer.Ordinal)
                || !entry.SavingThrows.SequenceEqual(new[] { "CHA", "WIS" }, StringComparer.Ordinal)
                || character.ProfileId != CharacterProfile || !character.Abilities.SequenceEqual(new[] { 10, 10, 10, 10, 14, 10 })
                || character.Levels.Count != (BishopProfile.Earned(state) ? 3 : earned ? 2 : 1) || character.Levels[0].ClassName != "Cleric" || character.Levels[0].BaseHp != 8
                || life.MaximumHp != (BishopProfile.Earned(state) ? 18 : earned ? 13 : 8) || pool.ActorId != Actor
                || pool.Maximum != (BishopProfile.Earned(state) ? 7 : earned ? 4 : 3)
                || funding.Id != FundingId || funding.ActorId != Actor || funding.PolicyId != FundingPolicy || funding.Amount != 3 || funding.Revision != 0
                || state.CharacterHitDice.Count(x => x.ActorId == Actor && x.LevelOrdinal == 1 && x.ClassName == "Cleric" && x.DieSize == 8 && (state.ConnectedClericSettlement || !x.Spent)) != 1
                || entry.SelectedSkills.Any(skill => state.SkillTraining.Count(x => x.ActorId == Actor && x.SkillId == skill && x.ProficiencyRank == 1) != 1)
                || state.InitialClassSelections.Count(x => ValidInitialSelection(state, x)) != 1
                || state.CharacterFeatureGrants.Count(x => ValidInitialGrant(state, x)) != 4)
                throw new ArgumentException("Invalid shared Cleric class, training, grant or RP facts.");
            int balance = funding.Amount;
            foreach (var result in state.HealingRites) {
                if (state.ConnectedClericLongRest) balance = ClericLongRestProfile.RpBefore(state,result.Revision);
                else if (state.ConnectedClericCasting) balance = funding.Amount
                    - state.HealingRites.Where(x => x.Revision < result.Revision).Sum(x => x.RpPaid)
                    - state.SpellCasts.Where(x => x.Revision < result.Revision).Sum(x => x.BaseRp + x.Surcharge);
                if (result.ActorId != Actor || result.TargetId != Actor && result.TargetId != ConnectedVialRules.CarrierId
                    || result.SourceId != HealingRite || result.SourceRevision != SourceRevision || result.RpBefore != balance
                    || result.RpPaid != 2 || result.Modifier != 2 || result.Revision > state.Revision || result.At > state.RuleClock
                    || result.RandomBefore == result.RandomAfter)
                    throw new ArgumentException("Invalid shared Healing Rite history.");
                var receipt = state.Receipts.SingleOrDefault(x => x.Id == result.CommandId && x.Revision == result.Revision);
                var command = state.ConnectedClericSettlement && receipt != null ? CommandHistory.Read(receipt)
                    : new Command(result.CommandId, result.ActorId, result.Revision - 1, CommandKind.UseHealingRite, result.TargetId);
                if (command.Kind != CommandKind.UseHealingRite || command.Actor != result.ActorId || command.Target != result.TargetId)
                    throw new ArgumentException("Healing Rite receipt differs from its payment.");
                if (!state.Receipts.Any(x => command.MatchesReceipt(x) && x.Principal == "TEST_ONLY.host"))
                    throw new ArgumentException("Unattributed Healing Rite payment.");
                balance = result.RpAfter;
            }
            if (state.ConnectedClericCasting) {
                foreach (var cast in state.SpellCasts) {
                    int before = state.ConnectedClericLongRest ? ClericLongRestProfile.RpBefore(state,cast.Revision)
                        : funding.Amount - state.HealingRites.Where(x => x.Revision < cast.Revision).Sum(x => x.RpPaid)
                        - state.SpellCasts.Where(x => x.Revision < cast.Revision).Sum(x => x.BaseRp + x.Surcharge);
                    if (cast.ActorId != Actor || cast.RpBefore != before || cast.RpAfter != before - cast.BaseRp - cast.Surcharge)
                        throw new ArgumentException("Casting payment differs from the shared RP chronology.");
                }
                balance = state.ConnectedClericLongRest ? ClericLongRestProfile.RpBefore(state,long.MaxValue)
                    : funding.Amount - state.HealingRites.Sum(x => x.RpPaid) - state.SpellCasts.Sum(x => x.BaseRp + x.Surcharge);
            }
            string kind = ((int)CommandKind.UseHealingRite).ToString(CultureInfo.InvariantCulture) + "|";
            if (pool.Current != balance || state.HealingRites.Select(x => x.CommandId).Distinct(StringComparer.Ordinal).Count() != state.HealingRites.Length
                || state.Receipts.Count(x => x.Fingerprint.StartsWith(kind, StringComparison.Ordinal)) != state.HealingRites.Length)
                throw new ArgumentException("RP balance or payment history mismatch.");
        }
    }
}
