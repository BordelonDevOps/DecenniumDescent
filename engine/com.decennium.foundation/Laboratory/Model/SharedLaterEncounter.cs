#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        public const string LaterDefenderId = "TEST_ONLY.later-defender";
        public const string LaterDefenderClubId = "TEST_ONLY.later-defender-club";
        private LaterEncounterDefinition laterEncounterDefinition;

        public TestOnlySharedWorldPolicy EnableLaterEncounter()
        {
            if (initializationStarted || laterEncounterDefinition != null || SelectedSchema != Snapshot.CharterAttemptSchema)
                throw new InvalidOperationException("Select the bounded later encounter on the charter execution host before initialization.");
            laterEncounterDefinition = new LaterEncounterDefinition("TEST_ONLY.later-conflict", "TEST_ONLY.later-calendar",
                TestOnlyPolicy.ActorId, LaterDefenderId, LaterDefenderClubId, "TEST_ONLY.numeric-warrior3",
                "TEST_ONLY.lower-left-completed-approach.v1", "TEST_ONLY.director-defender-first-on-tie.v1");
            bodies.RegisterDeferredConditionTarget(LaterDefenderId);
            const string rules = "EXP-07.46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"
                + "ordinary-warrior3-ability10|26hp-8current-0temporary-standing-30speed-standard-club|"
                + "1,3-to-0,3|defender-0,4|hold-position-mutually-aware|"
                + "ordinal-actor-draws|defender-first-tie|first-start-at-arrival|old-calendar-retained|dead-resolves";
            var binding = string.Join("|", ContentFingerprint, rules, laterEncounterDefinition.EncounterId,
                laterEncounterDefinition.EpochId, laterEncounterDefinition.HeroId, laterEncounterDefinition.DefenderId,
                laterEncounterDefinition.DefenderClubId, laterEncounterDefinition.CharacterProfileId,
                laterEncounterDefinition.EngagementId, laterEncounterDefinition.TieDecisionId);
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.later-encounter-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(binding))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeLaterEncounter(Snapshot state)
        {
            var definition = laterEncounterDefinition;
            if (definition == null) return;
            string defender = definition.DefenderId;
            int x = definition.DefenderX, y = definition.DefenderY;
            var body = state.Characters.Single(a => a.ActorId == AdditionalTacticalActor.Id);
            state.Actors = state.Actors.Append(new ActorState { Id = defender, X = x, Y = y }).ToArray();
            state.Characters = state.Characters.Append(new ActorCharacterRecord(defender, definition.CharacterProfileId,
                body.Abilities, body.Levels)).ToArray();
            state.Lives = state.Lives.Append(ActorLifeRules.Record(defender,
                new LifeState(definition.DefenderMaximumHp, definition.DefenderOpeningHp), false,
                new[] { definition.DefenderClubId })).ToArray();
            state.Clubs = state.Clubs.Append(new ClubInstance(definition.DefenderClubId, TestOnlyClubAttackPolicy.ClubProfile,
                defender, defender, defender, x, y)).ToArray();
            state.ActorMovement = state.ActorMovement.Append(new ActorMovementRecord(defender, definition.DefenderWalkingSpeed)).ToArray();
            state.TacticalActors = state.TacticalActors.Append(new ActorTacticalRecord(defender)).ToArray();
            state.Conditions = state.Conditions.Append(new ConditionJournal(ConditionHistory.PolicyId, defender,
                new ConditionStamp(state.RuleClock))).ToArray();
            state.LaterEncounter = new LaterEncounterRecord(definition);
        }

        private static string WorldAdvancePayloadFailure(Command command)
            => command.Inventory != null || command.Target != "" || command.X < 1 || command.Y < 1
                ? "InvalidWorldAdvance" : null;

        private string AssessLaterClockQuery(Snapshot state, Command command)
        {
            string choice = PendingRecoveryChoiceFailure(state, command);
            if (choice != null) return choice;
            if (state.InventoryCombat) return "TacticalDecisionClockPaused";
            if (command.Combat != null) return "SharedCombatHandoffNotImplemented";
            return WorldAdvancePayloadFailure(command);
        }

        private static bool IsLaterApproach(Snapshot state, WorldTraversalRecord edge)
            => state.LaterEncounter?.Entry == null && state.LaterEncounter?.Definition.IsApproach(edge) == true;

        private string AssessLaterEngagement(Snapshot state, LaterEncounterDefinition definition)
        {
            var first = state.LaterEncounter.FirstExit;
            if (first == null || state.Encounter?.Id != first.Encounter.Id
                || !state.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead)
                return "LaterEncounterPriorConflictUnresolved";
            if (state.InventoryCombat || PendingCalendarChoice(state) || ManufacturingChoicePending(state)
                || HasPendingRecoveryOffer(state))
                return "LaterEncounterChoicePending";
            var defender = state.Actors.SingleOrDefault(x => x.Id == definition.DefenderId);
            if (defender == null || defender.X != definition.DefenderX || defender.Y != definition.DefenderY
                || state.WorldTraversals.Any(x => x.ActorId == definition.DefenderId)
                || !CapableWorker(state, definition.DefenderId) || !CapableWorker(state, definition.HeroId))
                return "LaterEncounterParticipantsIneligible";
            if (!TestOnlyClubAttackPolicy.CanSee(state, definition.HeroId, definition.DefenderId)
                || !TestOnlyClubAttackPolicy.CanSee(state, definition.DefenderId, definition.HeroId)
                || !WorldWalkable(state, definition.DefenderX, definition.DefenderY)
                || !WorldWalkable(state, definition.ArrivalX, definition.ArrivalY)
                || ObservationRules.Enabled(state) && !ObservationGeometry.LineOfEffectClear(state, definition.HeroId, definition.DefenderId))
                return "LaterEncounterAwarenessUnavailable";
            if (state.RestIntervals.Any(x => x.Status == RestIntervalStatus.Active
                && (x.ActorId == definition.HeroId || x.ActorId == definition.DefenderId))
                || HasActiveHavenCare(state))
                return "LaterEncounterParticipantInterruptionUnsupported";
            return null;
        }

        private string AssessLaterWorldStep(Snapshot state, WorldTraversalRecord proposed)
        {
            var later = state.LaterEncounter;
            if (later == null || later.Entry != null) return null;
            if (proposed.ActorId == later.Definition.DefenderId) return "LaterDefenderHoldsAuthoredPosition";
            return IsLaterApproach(state, proposed) ? AssessLaterEngagement(state, later.Definition) : null;
        }

        private static LaterInitiativeDraw[] RollLaterInitiative(Snapshot state, LaterEncounterDefinition definition)
        {
            return new[] { definition.HeroId, definition.DefenderId }.OrderBy(x => x, StringComparer.Ordinal)
                .Select(actor => RollWorldInitiative(state, actor)).ToArray();
        }

        private static LaterInitiativeDraw RollWorldInitiative(Snapshot state, string actor)
        {
            var character = CharacterStateFacts.ForActor(state, actor);
            int dexterity = character.Rules.AbilityModifier(CharacterAbility.Dexterity);
            int legalModifier = character.InjuryPenalty(CharacterAbility.Dexterity, initiative: true);
            uint before = state.RandomState;
            var roll = PlaytestDice.RollD20(before);
            state.RandomState = roll.NextRandomState;
            return new LaterInitiativeDraw(actor, roll.Natural, dexterity, legalModifier, before,
                roll.NextRandomState, checked((int)roll.WordsConsumed));
        }

        private static void RecordActualCombatExit(Snapshot state, FixedEncounterRecord outgoing, Command command)
        {
            var later = state.LaterEncounter;
            if (later == null) return;
            var closed = new ClosedEncounterRecord(outgoing, state.Revision + 1, state.RuleClock, command.Id);
            if (later.Entry == null) {
                if (later.FirstExit == null) state.LaterEncounter = later.WithFirstExit(closed);
                return;
            }
            if (outgoing.Id == later.Definition.EncounterId) {
                state.ClosedEncounters = state.ClosedEncounters.Append(closed).ToArray();
                state.Encounter = null;
            }
        }

        private void ResolveLaterApproachArrival(Snapshot state, WorldTraversalRecord edge, Command cause, RuleTime target,
            WorldIntervalRecord carried, long previousOldSlot)
        {
            TestOnlyClubAttackPolicy.AdvanceConditions(state, ".clock-final", onlyAtExpiry: true);
            var later = state.LaterEncounter;
            var definition = later.Definition;
            var hero = state.Actors.Single(a => a.Id == definition.HeroId);
            string failure = hero.X == definition.ArrivalX && hero.Y == definition.ArrivalY
                ? AssessLaterEngagement(state, definition) : "LaterEncounterArrivalUnavailable";
            if (failure == null) {
                BeginLaterEncounter(state, edge, cause, target, carried);
                return;
            }
            RefreshIntervals(state);
            ProcessDeferredOldLifeMarker(state, previousOldSlot, definition.HeroId);
            ObserveCalendar(state);
            state.LaterEncounter = later.Interrupted(new LaterEncounterInterruption(edge.StartedRevision,
                state.Revision + 1, cause.Id, state.RuleClock, failure));
        }

        private void BeginLaterEncounter(Snapshot state, WorldTraversalRecord edge, Command cause, RuleTime target,
            WorldIntervalRecord carried)
        {
            var later = state.LaterEncounter;
            var definition = later.Definition;
            var draws = RollLaterInitiative(state, definition);
            var order = draws.OrderByDescending(x => x.Total).ThenBy(x => x.ActorId != definition.DefenderId)
                .Select(x => x.ActorId).ToArray();
            var epoch = new WorldScheduleRecord(definition.EpochId, state.RuleClock, order);
            var entry = new LaterEncounterEntry(epoch, edge.StartedRevision, state.Revision + 1, cause.Id, target, draws, carried);
            state.LaterEncounter = later.WithEntry(entry);
            state.ClosedEncounters = state.ClosedEncounters.Append(later.FirstExit).ToArray();
            state.Encounter = new FixedEncounterRecord(definition.EncounterId, state.RuleClock, order, new[] { state.Revision + 1 });

            var defendersActivity = state.WorldActivityIntervals.Single(x => x.ActorId == definition.DefenderId);
            state.WorldActivityIntervals = state.WorldActivityIntervals.Where(x => x.ActorId != definition.DefenderId).ToArray();
            bool heroReaction = Permissions(state, definition.HeroId).Reaction;
            bool defenderReaction = Permissions(state, definition.DefenderId).Reaction;
            SetInterval(state, new WorldIntervalRecord(definition.HeroId, -1, carried.MovementSpent,
                carried.ActionSpent, carried.DashPaid, heroReaction, carried.Interactions));
            state.WorldIntervals = state.WorldIntervals.Append(new WorldIntervalRecord(definition.DefenderId, -1,
                defendersActivity.MovementSpent, defendersActivity.Action != WorldActionCommitment.None,
                defendersActivity.DashPaid, defenderReaction)).ToArray();
            state.BonusActions = state.BonusActions.Select(x => x.ActorId == definition.HeroId
                ? new ActorBonusActionRecord(x.ActorId, -1, x.Available) : x)
                .Append(new ActorBonusActionRecord(definition.DefenderId, -1)).ToArray();
            BindLaterIntervalBodies(state, definition.HeroId, Interval(state, definition.HeroId), preserveTurnState: true);
            BindLaterIntervalBodies(state, definition.DefenderId, Interval(state, definition.DefenderId), preserveTurnState: true);
            ProcessLaterRegularStart(state, epoch, 0);

            state.InventoryCombat = true;
            state.InventoryTurnActor = state.Encounter.CurrentActor;
            state.InventoryInteractions = Interval(state, state.Encounter.CurrentActor).Interactions;
            foreach (string participant in order) PauseParticipantWork(state, participant);
            PauseIncompatibleWork(state);
        }

        private static void BindLaterIntervalBodies(Snapshot state, string actor, WorldIntervalRecord interval, bool preserveTurnState)
        {
            int start = checked((int)interval.LastStart);
            state.TacticalActors = state.TacticalActors.Select(x => x.ActorId != actor ? x
                : new ActorTacticalRecord(actor, start, interval.ReactionAvailable,
                    preserveTurnState ? x.MobileFeet : 0, preserveTurnState && x.PressConsumed,
                    preserveTurnState ? x.DisengageTurn : -1)).ToArray();
            state.ActorMovement = state.ActorMovement.Select(x => x.ActorId == actor
                ? new ActorMovementRecord(actor, x.BaseWalkingSpeed, start) : x).ToArray();
        }

        private static void ProcessLaterRegularStart(Snapshot state, WorldScheduleRecord epoch, long ordinal, int? globalTurn = null)
        {
            string actor = epoch.Order[(int)(ordinal % epoch.Order.Count)];
            int turn = globalTurn ?? checked((int)ordinal);
            var interval = new WorldIntervalRecord(actor, turn);
            SetInterval(state, interval);
            BindLaterIntervalBodies(state, actor, interval, preserveTurnState: false);
            CharacterAdvancementRules.RegularStart(state, actor, turn);
            if (epoch.Start(ordinal) == state.RuleClock)
                SaveWorldLifeMarker(state, actor, epoch.Id, epoch.Origin, ordinal, turn);
        }

        private static void RefreshLaterEpoch(Snapshot state)
        {
            var later = state.LaterEncounter;
            var entry = later?.Entry;
            if (entry == null) return;
            var epoch = entry.Epoch;
            long slot = epoch.SlotAt(state.RuleClock);
            if (slot == epoch.ProcessedSlot) return;
            state.LaterEncounter = later.WithEntry(entry.At(slot));
            foreach (string actor in epoch.Order.OrderBy(x => epoch.LatestStart(x, slot))) {
                if (WorldTiming.ForActor(state, actor).Id != epoch.Id) continue;
                long start = epoch.LatestStart(actor, slot);
                if (start >= 0 && start != Interval(state, actor).LastStart) ProcessLaterRegularStart(state, epoch, start);
            }
        }
    }
}
#endif
