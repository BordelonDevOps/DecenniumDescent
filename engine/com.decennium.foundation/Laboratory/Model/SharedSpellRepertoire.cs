#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ClericRepertoireSelection
    {
        public ReadOnlyCollection<string> SpellIds { get; }
        public ClericRepertoireSelection(IEnumerable<string> spellIds)
        {
            var ids = spellIds?.ToArray();
            string failure = ClericRepertoireProfile.ValidateInitialChoices(ids);
            if (failure != null) throw new ArgumentException(failure);
            SpellIds = Array.AsReadOnly(ids.OrderBy(x => x, StringComparer.Ordinal).ToArray());
        }
        public static ClericRepertoireSelection AuthoredExample() => new ClericRepertoireSelection(ClericRepertoireProfile.InitialSpells);
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ClericRepertoireSelection clericRepertoireSelection;
        internal TestOnlySharedWorldPolicy EnableConnectedClericRepertoire(ClericInitialSelection initial, ClericRepertoireSelection repertoire)
        {
            if (initial == null || repertoire == null) throw new ArgumentNullException("Complete initial class and repertoire choices are required.");
            // Both typed bundles are already immutable and validated before any Initial(), simulation or funding exists.
            EnableConnectedCleric(initial);
            clericRepertoireSelection = repertoire;
            ContentFingerprint = ClericRepertoireProfile.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                SpellSourceCatalog.SourceRevision, SpellSourceCatalog.CatalogSha256, SpellSourceCatalog.ClassProgressionSha256,
                string.Join(",", repertoire.SpellIds), "review-f17c9e06-7464-56da-8184-a5723befea81|known-only|no-earned-or-casting"));
            return this;
        }
        private void InitializeClericRepertoire(Snapshot state)
        {
            if (clericRepertoireSelection == null) return;
            state.ConnectedClericRepertoire = true;
            state.KnownSpells = clericRepertoireSelection.SpellIds.Select(id => KnownSpellRecord.FromSource(ClericRpProfile.Actor,
                id, SpellAcquisitionOrigin.InitialClassRepertoire, 1, 1, ClericRepertoireProfile.InitialEntitlement)).ToArray();
        }

        /// <summary>Shared earned-repertoire transaction component. The CHR-03 caller stages mandatory grants
        /// and consumes the real milestone before invoking this component in the same atomic command.</summary>
        internal static void SettleClericEarnedRepertoire(Snapshot staged, string actor, string spell, CharacterAdvancementRecord advancement)
        {
            if (staged == null || advancement == null) throw new ArgumentException("Earned advancement required.");
            var character = staged.Characters.SingleOrDefault(x => x.ActorId == actor);
            var milestone = staged.CharacterMilestones.SingleOrDefault(x => x.ActorId == actor && x.MilestoneId == advancement.MilestoneId);
            if (character == null || character.Levels.Count != 2 || character.Levels.Any(x => x.ClassName != "Cleric")
                || advancement.ActorId != actor || advancement.ClassName != "Cleric" || advancement.ClassLevel != 2
                || advancement.PreviousTotalLevel != 1 || advancement.NewTotalLevel != 2 || advancement.Revision != staged.Revision + 1
                || milestone == null || milestone.ConsumedRevision != advancement.Revision
                || !staged.CharacterAdvancements.Contains(advancement)
                || staged.InitialClassSelections.Count(x => x.ActorId == actor && x.ClassName == "Cleric" && x.ClassLevel == 1
                    && x.SourceRevision == SpellSourceCatalog.SourceRevision) != 1)
                throw new ArgumentException("ClericEarnedAdvancementUnavailable");
            var owned = staged.KnownSpells.Where(x => x.ActorId == actor && x.ClassName == "Cleric").ToArray();
            if (owned.Length != 5 || ClericRepertoireProfile.ValidateInitialChoices(owned.Select(x => x.SpellId)) != null
                || owned.Any(x => !x.MatchesSource() || x.Origin != SpellAcquisitionOrigin.InitialClassRepertoire
                    || x.EntitlementId != ClericRepertoireProfile.InitialEntitlement || x.ClassLevel != 1 || x.LevelOrdinal != 1)
                || spell != ClericRepertoireProfile.FutureChoice || ClericRepertoireProfile.AssessChoice(spell, 2) != null)
                throw new ArgumentException("ClericEarnedRepertoireChoiceUnavailable");
            var earned = KnownSpellRecord.FromSource(actor, spell, SpellAcquisitionOrigin.EarnedClassLevel, 2, 2,
                ClericRepertoireProfile.EarnedEntitlement, milestone.MilestoneId, advancement.Revision);
            // All validation precedes this one ledger replacement; no time, RNG, RP, HP or other grants change here.
            staged.KnownSpells = staged.KnownSpells.Append(earned).ToArray();
        }
    }
}
#endif
