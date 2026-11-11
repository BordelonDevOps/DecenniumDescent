#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyReinforcementProfile
    {
        public bool ParticipationAuthorized { get; }
        public bool AlliedSideBound { get; }
        public bool PlayerTieBound { get; }
        public bool DirectorTieBound { get; }

        public TestOnlyReinforcementProfile(bool participationAuthorized = true, bool alliedSideBound = true,
            bool playerTieBound = true, bool directorTieBound = true)
        {
            ParticipationAuthorized = participationAuthorized;
            AlliedSideBound = alliedSideBound;
            PlayerTieBound = playerTieBound;
            DirectorTieBound = directorTieBound;
        }

        internal ReinforcementDefinition Bind(LaterEncounterDefinition encounter)
            => new ReinforcementDefinition("TEST_ONLY.companion-reinforcement.v1", encounter.EncounterId,
                "TEST_ONLY.reinforced-calendar", TestOnlyPolicy.CompanionId, encounter.HeroId, "TEST_ONLY.host",
                ParticipationAuthorized ? "TEST_ONLY.companion-voluntary-participation.v1" : "",
                AlliedSideBound ? "TEST_ONLY.hero-companion-player-side.v1" : "",
                PlayerTieBound ? "TEST_ONLY.player-hero-before-companion-on-tie.v1" : "",
                DirectorTieBound ? "TEST_ONLY.director-defender-before-companion-on-tie.v1" : "");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ReinforcementDefinition reinforcementDefinition;

        public TestOnlySharedWorldPolicy EnableCompanionReinforcement(TestOnlyReinforcementProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || reinforcementDefinition != null || SelectedSchema != Snapshot.LaterEncounterSchema)
                throw new InvalidOperationException("Select the named reinforcement on the later encounter host before initialization.");
            var definition = profile.Bind(laterEncounterDefinition);
            reinforcementDefinition = definition;
            string binding = string.Join("|", ContentFingerprint, "EXP-07.46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
                definition.Id, definition.EncounterId, definition.EpochId, definition.CompanionId, definition.AllyId,
                definition.ControllerId, definition.ParticipationMandateId, definition.AlliedSideId, definition.PlayerTieChoiceId,
                definition.DirectorTieChoiceId, definition.AwarenessPolicyId,
                "2,3-to-1,3-walk|arrival-then-end-round|next-round-three-slots");
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.reinforcement-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(binding))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeReinforcement(Snapshot state)
        {
            var definition = reinforcementDefinition;
            if (definition == null) return;
            if (definition.AlliedSideId != "")
                state.TacticalAllies = state.TacticalAllies.Append(new TacticalAllyRecord(definition.AllyId, definition.CompanionId)).ToArray();
            state.Reinforcement = new ReinforcementRecord(definition);
        }

        private IEnumerable<Command> DiscoverReinforcementCommands(Snapshot state, Authority authority, string actor)
        {
            var record = state.Reinforcement;
            if (record == null || actor != record.Definition.CompanionId || authority.Principal != record.Definition.ControllerId) yield break;
            string prefix = "option." + state.Revision.ToString(CultureInfo.InvariantCulture) + ".reinforcement.";
            Command Instruction(CommandKind kind) => new Command(prefix + kind, actor, state.Revision, kind, record.Definition.Id);
            if (record.Began == null) {
                var begin = Instruction(CommandKind.BeginReinforcementApproach);
                if (AssessReinforcementInstruction(state, begin, out _) == null) yield return begin;
                yield break;
            }
            if (!record.Pending) yield break;
            var cancel = Instruction(CommandKind.CancelReinforcementApproach);
            if (AssessReinforcementInstruction(state, cancel, out _) == null) yield return cancel;
            var edge = ReinforcementEdge(state);
            if (edge == null) yield break;
            var control = edge.Status == WorldTraversalStatus.Suspended ? CommandKind.ResumeWorldStep : CommandKind.SuspendWorldStep;
            var command = new Command(prefix + control, actor, state.Revision, control);
            if (AssessReinforcementControl(state, command, out _) == null) yield return command;
        }

        private static bool IsReinforcementControl(Snapshot state, Command command)
            => state.InventoryCombat && state.Reinforcement?.Definition.CompanionId == command.Actor
                && (command.Kind == CommandKind.SuspendWorldStep || command.Kind == CommandKind.ResumeWorldStep)
                && state.WorldTraversals.Any(edge => state.Reinforcement.OwnsApproach(edge));

        private static bool ReinforcementIsActiveFight(Snapshot state, ReinforcementDefinition definition)
            => state.InventoryCombat && state.Encounter?.Id == definition.EncounterId && state.Encounter.RosterPhase == null;

        private static string ReinforcementMandateFailure(Snapshot state, ReinforcementDefinition definition)
        {
            if (definition.ParticipationMandateId == "") return "ReinforcementParticipationMandateMissing";
            if (definition.AlliedSideId == "" || !SoldierTacticalFeatures.IsAlly(state, definition.AllyId, definition.CompanionId))
                return "ReinforcementAlliedSideMissing";
            if (definition.PlayerTieChoiceId == "" || definition.DirectorTieChoiceId == "") return "ReinforcementTieAuthorityMissing";
            return null;
        }

        private static string ReinforcementAwarenessFailure(Snapshot state, ReinforcementDefinition definition)
            => !TestOnlyClubAttackPolicy.CanSee(state, definition.CompanionId, definition.AllyId)
                || !TestOnlyClubAttackPolicy.CanSee(state, definition.AllyId, definition.CompanionId)
                || !TestOnlyClubAttackPolicy.CanSee(state, definition.CompanionId, state.LaterEncounter.Definition.DefenderId)
                    ? "ReinforcementAwarenessUnavailable" : null;

        private string AssessReinforcementInstruction(Snapshot state, Command command, out WorldStepFacts facts)
        {
            facts = null;
            var reinforcement = state.Reinforcement;
            if (reinforcement == null || reinforcementDefinition == null) return "ReinforcementNotSelected";
            var definition = reinforcement.Definition;
            if (command.Actor != definition.CompanionId) return "ReinforcementActorUnauthorized";
            if (command.Target != definition.Id) return "UnknownReinforcementDefinition";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Ranged != null || command.Advancement != null)
                return "InvalidReinforcementPayload";
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "TacticalChoicePending";
            if (command.Kind == CommandKind.CancelReinforcementApproach)
                return reinforcement.Pending ? null : "ReinforcementApproachNotPending";
            if (reinforcement.Began != null) return "ReinforcementAlreadyAttempted";
            if (!ReinforcementIsActiveFight(state, definition) || ResolvedConflict(state)) return "ReinforcementEncounterUnavailable";
            string mandate = ReinforcementMandateFailure(state, definition);
            if (mandate != null) return mandate;
            if (state.ReadyActions.Any(x => x.Armed) || state.OverwatchOffers.Any(x => x.Status == OverwatchOfferStatus.Pending))
                return "ReinforcementApproachTriggerUnsupported";
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            if (actor.X != definition.FromX || actor.Y != definition.FromY || state.WorldTraversals.Any(x => x.ActorId == command.Actor))
                return "ReinforcementRequiresStationaryStaging";
            if (!CapableWorker(state, command.Actor)) return "ReinforcementActorIncapable";
            var burden = PortableEquipmentRules.CarriedBurden(state, command.Actor);
            if (PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium, 10), burden) != true)
                return "ReinforcementHardCarryingLimit";
            string failure = ReinforcementAwarenessFailure(state, definition) ?? AssessWorldStep(state, command, out facts, reinforcementApproach: true);
            if (failure != null) return failure;
            if (facts.DetachesRoute) return "ReinforcementRouteAttachmentUnsupported";
            var edge = new WorldTraversalRecord(command.Actor, state.Revision + 1, actor.X, actor.Y, facts.ToX, facts.ToY);
            return TestOnlyClubAttackPolicy.ReinforcementWouldTriggerOpportunity(state, edge)
                ? "ReinforcementApproachTriggerUnsupported" : null;
        }

        private static void AppendReinforcementEvent(Snapshot state, Command cause, ReinforcementEventKind kind,
            string reason, RuleQuantity distance = default, ReinforcementAdmission admission = null)
        {
            var entry = new ReinforcementEvent(kind, state.Revision + 1, cause.Id, state.RuleClock, reason, distance);
            state.Reinforcement = state.Reinforcement.Append(entry, admission);
        }

        private static WorldTraversalRecord ReinforcementEdge(Snapshot state)
            => state.WorldTraversals.SingleOrDefault(edge => state.Reinforcement?.OwnsApproach(edge) == true);

        private static void SuspendReinforcementEdge(Snapshot state, WorldTraversalRecord edge)
        {
            if (edge != null && edge.Status != WorldTraversalStatus.Suspended)
                SetEdge(state, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
        }

        private string ResolveReinforcementInstruction(Snapshot state, Command command)
        {
            string failure = AssessReinforcementInstruction(state, command, out var facts);
            if (failure != null) return failure;
            if (command.Kind == CommandKind.CancelReinforcementApproach) {
                var pending = ReinforcementEdge(state);
                SuspendReinforcementEdge(state, pending);
                AppendReinforcementEvent(state, command, ReinforcementEventKind.Cancelled, "ReinforcementExplicitCancellation",
                    pending?.DistanceFeet ?? state.Reinforcement.Arrival?.Distance ?? default);
                return null;
            }
            AddOrdinaryWorldTraversal(state, command, facts, running: false);
            AppendReinforcementEvent(state, command, ReinforcementEventKind.Began, "ReinforcementVoluntaryDeparture");
            SyncExpeditionAssignments(state, command.Actor);
            return null;
        }

        private string AssessReinforcementControl(Snapshot state, Command command, out WorldTraversalRecord edge)
        {
            edge = null;
            if (PendingCalendarChoice(state)) return "TacticalChoicePending";
            if (!state.Reinforcement.Pending) return "ReinforcementApproachNotPending";
            string failure = AssessTraversalControl(state, command, out edge);
            if (failure != null || command.Kind == CommandKind.SuspendWorldStep) return failure;
            return ReinforcementPassageFailure(state, edge);
        }

        private string ResolveReinforcementControl(Snapshot state, Command command)
        {
            string failure = AssessReinforcementControl(state, command, out var edge);
            if (failure != null) return failure;
            bool suspend = command.Kind == CommandKind.SuspendWorldStep;
            SetEdge(state, edge.With(edge.DistanceFeet, suspend ? WorldTraversalStatus.Suspended : WorldTraversalStatus.Moving));
            AppendReinforcementEvent(state, command, suspend ? ReinforcementEventKind.Suspended : ReinforcementEventKind.Resumed,
                suspend ? "ReinforcementExplicitSuspension" : "ReinforcementExplicitResume", edge.DistanceFeet);
            if (!suspend) ReconcileTraversal(state);
            return null;
        }

        private string ReinforcementPassageFailure(Snapshot state, WorldTraversalRecord edge)
        {
            if (!CapableWorker(state, edge.ActorId) || !Permissions(state, edge.ActorId).VoluntarySpeed || Speed(state, edge.ActorId) == 0)
                return "ReinforcementActorIncapable";
            if (OrdinaryInventory.Busy(state, edge.ActorId)) return "ReinforcementWorkerBusy";
            if (WorldSpatialQueries.Step(state, edge.ActorId, edge.FromX, edge.FromY, edge.ToX, edge.ToY, false, false,
                (x, y) => WorldWalkable(state, x, y)) != SpatialStepFailure.None) return "ReinforcementPassageObstructed";
            return TestOnlyClubAttackPolicy.ReinforcementWouldTriggerOpportunity(state, edge)
                ? "ReinforcementApproachTriggerUnsupported" : null;
        }

        private void ReconcileReinforcement(Snapshot state, Command cause)
        {
            var reinforcement = state.Reinforcement;
            if (reinforcement?.Pending != true || cause == null) return;
            var edge = ReinforcementEdge(state);
            if (!ReinforcementIsActiveFight(state, reinforcement.Definition) || ResolvedConflict(state)) {
                SuspendReinforcementEdge(state, edge);
                AppendReinforcementEvent(state, cause, ReinforcementEventKind.NoLongerNeeded, "ReinforcementConflictResolved",
                    edge?.DistanceFeet ?? reinforcement.Arrival?.Distance ?? default);
                return;
            }
            if (edge == null) return;
            string blocker = ReinforcementPassageFailure(state, edge);
            if (blocker == null && edge.Status != WorldTraversalStatus.Suspended) return;
            SuspendReinforcementEdge(state, edge);
            var last = reinforcement.Events.LastOrDefault(x => x.Kind == ReinforcementEventKind.Suspended || x.Kind == ReinforcementEventKind.Resumed);
            if (last?.Kind != ReinforcementEventKind.Suspended)
                AppendReinforcementEvent(state, cause, ReinforcementEventKind.Suspended,
                    blocker ?? "ReinforcementTraversalSuspended", edge.DistanceFeet);
        }

        private static bool AtReinforcementEndRound(Snapshot state, Command cause, RuleTime next, RuleTime target)
        {
            var reinforcement = state.Reinforcement;
            var encounter = state.Encounter;
            return reinforcement?.Pending == true && ReinforcementIsActiveFight(state, reinforcement.Definition)
                && next == target && (cause?.Kind == CommandKind.EndRegularTurn || cause?.Kind == CommandKind.EndFixedEncounter)
                && (encounter.TurnOrdinal + 1) % encounter.Order.Count == 0;
        }

        private static void RecordReinforcementArrival(Snapshot state, Command cause, WorldTraversalRecord edge)
        {
            var record = state.Reinforcement;
            if (record?.Pending != true || record.Arrival != null || !record.OwnsApproach(edge)) return;
            var actor = state.Actors.Single(x => x.Id == edge.ActorId);
            if (actor.X == edge.ToX && actor.Y == edge.ToY)
                AppendReinforcementEvent(state, cause, ReinforcementEventKind.Arrived, "ReinforcementPhysicalArrival",
                    new RuleQuantity(5));
        }

        private string ReinforcementAdmissionFailure(Snapshot state, ReinforcementDefinition definition)
        {
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "ReinforcementTacticalChoicePending";
            var actor = state.Actors.Single(x => x.Id == definition.CompanionId);
            if (actor.X != definition.EntryX || actor.Y != definition.EntryY || ReinforcementEdge(state) != null)
                return "ReinforcementEntryPositionUnavailable";
            if (!CapableWorker(state, actor.Id)) return "ReinforcementActorIncapable";
            if (OrdinaryInventory.Busy(state, actor.Id)) return "ReinforcementWorkerBusy";
            if (WorldSpatialQueries.Occupied(state, actor.Id, actor.X, actor.Y) || !WorldWalkable(state, actor.X, actor.Y))
                return "ReinforcementPassageObstructed";
            var burden = PortableEquipmentRules.CarriedBurden(state, actor.Id);
            if (PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium, 10), burden) != true)
                return "ReinforcementHardCarryingLimit";
            return ReinforcementMandateFailure(state, definition) ?? ReinforcementAwarenessFailure(state, definition);
        }

        private void ResolveReinforcementEndRound(Snapshot state, Command cause)
        {
            var record = state.Reinforcement;
            if (record.Pending && ResolvedConflict(state)) {
                ReconcileReinforcement(state, cause);
                record = state.Reinforcement;
            }
            if (record.Pending && record.Arrival != null && cause.Kind == CommandKind.EndRegularTurn) {
                string failure = ReinforcementAdmissionFailure(state, record.Definition);
                if (failure == null) {
                    AdmitReinforcement(state, cause);
                    RefreshLaterEpoch(state);
                    return;
                }
                AppendReinforcementEvent(state, cause, ReinforcementEventKind.Deferred, failure, new RuleQuantity(5));
            }
            RefreshActivityIntervals(state);
            RefreshLaterEpoch(state);
        }

        private void AdmitReinforcement(Snapshot state, Command cause)
        {
            var record = state.Reinforcement;
            var definition = record.Definition;
            var outgoing = state.Encounter;
            var draw = RollWorldInitiative(state, definition.CompanionId);
            var previous = state.LaterEncounter.Entry;
            var draws = outgoing.Order.Select(id => previous.Draws.Single(x => x.ActorId == id));
            var order = ReinforcementValidation.Order(draws, draw).ToArray();
            var epoch = new WorldScheduleRecord(definition.EpochId, state.RuleClock, order);
            var phase = new EncounterRosterPhase(epoch, checked(outgoing.TurnOrdinal + 1), checked(outgoing.Round + 1));

            var activity = ActivityInterval(state, definition.CompanionId);
            var entrant = new WorldIntervalRecord(definition.CompanionId, -1, activity.MovementSpent,
                activity.Action != WorldActionCommitment.None, activity.DashPaid, Permissions(state, definition.CompanionId).Reaction);
            var carried = outgoing.Order.Select(id => new ReinforcementCarry(Interval(state, id),
                    state.BonusActions.Single(x => x.ActorId == id).Available))
                .Append(new ReinforcementCarry(entrant, true)).ToArray();
            var admission = new ReinforcementAdmission(phase, draw, carried);
            AppendReinforcementEvent(state, cause, ReinforcementEventKind.Admitted, "ReinforcementEndRoundAdmission",
                new RuleQuantity(5), admission);
            state.Encounter = outgoing.Observe(state.Revision + 1, phase.FirstTurn, phase);
            state.WorldActivityIntervals = state.WorldActivityIntervals.Where(x => x.ActorId != definition.CompanionId).ToArray();
            state.WorldIntervals = state.WorldIntervals.Append(entrant).ToArray();
            state.BonusActions = state.BonusActions.Append(new ActorBonusActionRecord(entrant.ActorId, -1)).ToArray();
            BindLaterIntervalBodies(state, entrant.ActorId, entrant, preserveTurnState: true);
            ProcessLaterRegularStart(state, epoch, 0, phase.FirstTurn);
            state.InventoryTurnActor = state.Encounter.CurrentActor;
            state.InventoryInteractions = Interval(state, state.Encounter.CurrentActor).Interactions;
        }

        private static void RefreshReinforcementEpoch(Snapshot state)
        {
            var record = state.Reinforcement;
            var phase = record?.Admission?.Phase;
            if (phase == null) return;
            var epoch = phase.Epoch;
            long slot = epoch.SlotAt(state.RuleClock);
            if (slot == epoch.ProcessedSlot) return;
            state.Reinforcement = record.At(slot);
            foreach (string actor in epoch.Order.OrderBy(x => epoch.LatestStart(x, slot))) {
                long local = epoch.LatestStart(actor, slot);
                if (local >= 0 && phase.GlobalTurn(local) != Interval(state, actor).LastStart)
                    ProcessLaterRegularStart(state, epoch, local, phase.GlobalTurn(local));
            }
        }
    }
}
#endif
