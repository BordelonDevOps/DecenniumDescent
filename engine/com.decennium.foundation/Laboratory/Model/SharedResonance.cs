#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Typed, validated initial class choices. This is not an in-play class replacement.</summary>
    public sealed class ClericInitialSelection
    {
        public ReadOnlyCollection<int> Abilities { get; }
        public ReadOnlyCollection<string> Skills { get; }
        public ReadOnlyCollection<string> Cards { get; }
        public string FavoredWeapon { get; }
        public int PointBuyCost { get; }
        public ClericInitialSelection(IEnumerable<int> abilities, IEnumerable<string> skills,
            IEnumerable<string> cards, string favoredWeapon)
        {
            if (abilities == null || skills == null || cards == null) throw new ArgumentNullException("Initial class choices are required.");
            var scores = abilities.ToArray(); var selectedSkills = skills.ToArray(); var selectedCards = cards.ToArray();
            PointBuyCost = PlaytestCharacters.PointBuyCost(scores);
            if (selectedSkills.Length != 2 || selectedSkills.Distinct(StringComparer.Ordinal).Count() != 2
                || selectedCards.Length != 4 || selectedCards.Distinct(StringComparer.Ordinal).Count() != 4)
                throw new ArgumentException("Invalid initial class selection counts.");
            var options = selectedCards.Select(id => ClassAdvancementOptionCatalog.Get("Cleric", id)).ToArray();
            if (options.Any(x => x == null || x.Acquisition != "selection" || x.Band != "Base" || x.MinimumClassLevel > 1
                    || x.HasPathConstraint || x.HasDeclaredPrerequisite) || options.Count(x => x.Kind == "active") < 2)
                throw new ArgumentException("Ineligible initial Cleric card selection.");
            selectedSkills = selectedSkills.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            selectedCards = selectedCards.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (!scores.SequenceEqual(new[] { 10, 10, 10, 10, 14, 10 })
                || !selectedSkills.SequenceEqual(new[] { "medicine", "religion" }, StringComparer.Ordinal)
                || !selectedCards.SequenceEqual(ClericRpProfile.SelectedCards, StringComparer.Ordinal)
                || favoredWeapon != ClericRpProfile.FavoredWeapon)
                throw new ArgumentException("InitialClericSelectionUnsupported");
            Abilities = Array.AsReadOnly(scores); Skills = Array.AsReadOnly(selectedSkills); Cards = Array.AsReadOnly(selectedCards);
            FavoredWeapon = favoredWeapon;
        }
        public static ClericInitialSelection AuthoredExample() => new ClericInitialSelection(new[] { 10, 10, 10, 10, 14, 10 },
            new[] { "medicine", "religion" }, ClericRpProfile.SelectedCards, ClericRpProfile.FavoredWeapon);
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ClericInitialSelection clericInitialSelection;
        internal TestOnlySharedWorldPolicy EnableConnectedCleric(ClericInitialSelection selection)
        {
            if (selection == null) throw new ArgumentNullException(nameof(selection));
            if (initializationStarted || clericInitialSelection != null || !connectedRecipe4Batch || connectedCarriedVial
                || characterAdvancement != null)
                throw new InvalidOperationException("Select first-class Cleric construction on a fresh connected expedition.");
            clericInitialSelection = selection;
            ContentFingerprint = ClericRpProfile.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                ClericRpProfile.SourceRevision, "class-entry1|point-buy17|10,10,10,10,14,10|medicine,religion|hp8|d8-unspent",
                string.Join(",", selection.Cards), selection.FavoredWeapon, ClericRpProfile.EngineSelector,
                ClericRpProfile.FundingPolicy, "review-009cd55a-2184-5e31-b093-b4b40b05e2d0|fund-once3|healing-rite2|no-recovery"));
            return this;
        }

        private void InitializeClericRp(Snapshot state)
        {
            if (clericInitialSelection == null) return;
            const string actor = ClericRpProfile.Actor;
            var selection = clericInitialSelection;
            var before = state.Lives.Single(x => x.ActorId == actor);
            state.ConnectedClericRp = true;
            state.Characters = state.Characters.Select(x => x.ActorId != actor ? x : new ActorCharacterRecord(actor,
                ClericRpProfile.CharacterProfile, selection.Abilities, new[] { new CharacterLevelFact("Cleric", 8) })).ToArray();
            state.Lives = state.Lives.Select(x => x.ActorId != actor ? x : new ActorLifeRecord(actor, 8, 8, 0,
                Array.Empty<int>(), false, false, true, 0, 0, null, 0, false, before.HeldItems)).ToArray();
            state.CharacterHitDice = state.CharacterHitDice.Append(new CharacterHitDieRecord(actor, 1, "Cleric", 8, false)).ToArray();
            state.InitialClassSelections = state.InitialClassSelections.Append(new CharacterInitialClassSelectionRecord(actor, "Cleric", 1,
                ClericRpProfile.SourceRevision, selection.Cards.ToArray())).ToArray();
            state.CharacterFeatureGrants = state.CharacterFeatureGrants.Concat(selection.Cards.Select(card =>
                new CharacterFeatureGrantRecord(actor, card, "Cleric", 1, "", 0, CharacterFeatureGrantOrigin.InitialClassSelection))).ToArray();
            state.SkillTraining = state.SkillTraining.Where(x => x.ActorId != actor || !selection.Skills.Contains(x.SkillId))
                .Concat(selection.Skills.Select(skill => new SkillTrainingRecord(actor, skill, 1))).ToArray();
            state.ClericEntry = new ClericClassEntryRecord(actor, ClericRpProfile.SourceRevision, selection.PointBuyCost,
                selection.FavoredWeapon, ClericRpProfile.EngineSelector, selection.Skills, new[] { "CHA", "WIS" });
            var character = state.Characters.Single(x => x.ActorId == actor);
            int maximum = DeriveResonanceMaximum(character);
            state.ResonancePools = new[] { new ResonancePoolRecord(actor, maximum, 3,
                new ResonanceFundingRecord(ClericRpProfile.FundingId, actor, ClericRpProfile.FundingPolicy, 3, 0)) };
        }

        internal static int DeriveResonanceMaximum(ActorCharacterRecord character)
        {
            var levels = character.Levels.GroupBy(x => x.ClassName, StringComparer.Ordinal)
                .ToDictionary(x => x.Key, x => x.Count(), StringComparer.Ordinal);
            var order = character.Levels.Select(x => x.ClassName).Distinct(StringComparer.Ordinal).ToArray();
            return PlaytestCharacters.MergedRp(levels, order).Maximum;
        }

        private string AssessHealingRite(Snapshot state, Command command)
        {
            if (!state.ConnectedClericRp || command.Actor != ClericRpProfile.Actor) return "HealingRiteUnavailable";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null || command.Advancement != null
                || command.Ranged != null || command.OverwatchRider != OverwatchRider.None || command.SuppressionFire != null
                || command.DefensiveFormation != null || command.ExpeditionAssignment != null || command.HarvestSelection != null
                || command.MiningSelection != null || command.ProspectingExposure != null || command.RouteMappingWork != null)
                return "InvalidHealingRiteRequest";
            bool postClosure = state.ConnectedClericSettlement && !state.InventoryCombat;
            if (postClosure || PostRecoveryProfile.Active(state)) {
                string context = RadianceRules.OwnTurnFailure(state,command.Actor); if (context != null) return context;
            } else if (!state.InventoryCombat || state.Reinforcement?.Admission == null
                || state.Encounter?.Id != state.Reinforcement.Definition.EncounterId) return "HealingRiteContextUnsupported";
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state)) return "TacticalChoicePending";
            if (!postClosure && (state.Encounter.CurrentActor != command.Actor || state.InventoryTurnActor != command.Actor)) return "WrongRegularTurn";
            if (!state.CharacterFeatureGrants.Any(x => x.FeatureId == ClericRpProfile.HealingRite && ClericRpProfile.ValidInitialGrant(state, x)))
                return "HealingRiteNotOwned";
            var character = state.Characters.Single(x => x.ActorId == command.Actor);
            if (character.Levels.Count(x => x.ClassName == "Cleric") != (BishopProfile.Earned(state)?3:postClosure || PostRecoveryProfile.Active(state) ? 2 : 1)) return "HealingRiteClassUnsupported";
            if (!CapableWorker(state, command.Actor) || !Permissions(state, command.Actor).Action) return "ConditionPreventsAction";
            if (Interval(state, command.Actor).ActionSpent) return "ActionAlreadySpent";
            if (OrdinaryInventory.Busy(state, command.Actor) || state.WorldTraversals.Any(x => x.ActorId == command.Actor || x.ActorId == command.Target))
                return "HealingRiteRequiresStationaryAccess";
            if (command.Target != TestOnlyPolicy.ActorId && command.Target != TestOnlyPolicy.CompanionId
                || !postClosure && !state.Encounter.Order.Contains(command.Target)) return "HealingRiteTargetUnavailable";
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            var target = state.Actors.Single(x => x.Id == command.Target);
            if (state.Lives.Single(x => x.ActorId == command.Target).Dead) return "HealingRiteTargetUnavailable";
            if (PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X, actor.Y), new CombatCell(target.X, target.Y)) > 30
                || !ObservationGeometry.LineOfEffectClear(state, actor.Id, target.Id)
                || actor.Id != target.Id && !ObservationRules.CanSee(state, actor.Id, target.Id)) return "HealingRiteTargetUnavailable";
            if (state.PeriodicRiders.Any(x => x.TargetId == target.Id && x.Present)) return "HealingRiteSourceInteractionUnsupported";
            var pool = state.ResonancePools.SingleOrDefault(x => x.ActorId == command.Actor);
            if (pool == null || pool.Maximum != DeriveResonanceMaximum(character)) return "ResonancePoolUnavailable";
            if (pool.Current < 2) return "InsufficientResonance";
            if (state.HealingRites.Length >= 128) return "HealingRiteHistoryFull";
            if (state.ConnectedClericCasting && state.CastingActivities.Length >= SpellCastingProfile.MaxActivities) return "CastingHistoryFull";
            return state.ConnectedClericSettlement ? RadiancePreflight(state,command) : null;
        }

        private string ResolveHealingRite(Snapshot state, Command command)
        {
            string failure = AssessHealingRite(state, command);
            if (failure != null) return failure;
            var pool = state.ResonancePools.Single(x => x.ActorId == command.Actor);
            var before = state.Lives.Single(x => x.ActorId == command.Target);
            uint random = state.RandomState;
            var draw = DiceStream.Draw(random, 8);
            int modifier = Math.Max(1, CharacterRuleFacts.ForActor(state, command.Actor).AbilityModifier(CharacterAbility.Wisdom));
            long potential = View(state, command.Target).HealingPotential(draw.Value + 1L + modifier);
            var healed = PlaytestLife.Heal(ActorLifeRules.ReadForResolution(state, before), potential);
            var paid = pool.Pay(2);
            SetInterval(state, Interval(state, command.Actor).PayAction());
            state.ResonancePools = state.ResonancePools.Select(x => x.ActorId == command.Actor ? paid : x).ToArray();
            TestOnlyClubAttackPolicy.ApplyLife(state, before, healed);
            state.RandomState = draw.NextState;
            var rite = new HealingRiteRecord(command.Id, state.Revision + 1,
                command.Actor, command.Target, ClericRpProfile.HealingRite, ClericRpProfile.SourceRevision, state.InventoryCombat ? state.Encounter.TurnOrdinal : checked((int)Interval(state,command.Actor).LastStart),
                state.RuleClock, pool.Current, 2, paid.Current, draw.Value + 1, modifier, potential, before.Hp, healed.Hp,
                random, draw.NextState, draw.WordsConsumed);
            state.HealingRites = state.HealingRites.Append(rite).ToArray();
            RecordCastingActivity(state,command,CastingActivityKind.MagicalClassAbility);
            if (state.ConnectedClericSettlement) SettleRadiance(state,command,rite);
            AuraOfFaithRules.HealAfterRite(state,command,rite);
            ReconcileDyingCadences(state); PauseIncompatibleWork(state);
            return null;
        }

        private CommandQueryResult QueryHealingRite(Snapshot state, Command command)
        {
            string failure = AssessHealingRite(state, command);
            return new CommandQueryResult(true, failure == null, failure ?? "Available", state.Revision,
                failure == null ? new[] { new CommandCost("action", "", 1), new CommandCost("rp", command.Actor, 2) } : null);
        }
    }
}
#endif
