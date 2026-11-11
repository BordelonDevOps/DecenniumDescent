#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ReengagementDefinition reengagementDefinition;

        public TestOnlySharedWorldPolicy EnablePhysicalReengagement(bool companionConsents = true, bool directorAuthorizes = true)
        {
            if (initializationStarted || reengagementDefinition != null || SelectedSchema != Snapshot.RetreatSchema)
                throw new InvalidOperationException("Select the bounded physical re-engagement before initializing the retreat host.");
            var retreat = retreatDefinition;
            reengagementDefinition = new ReengagementDefinition(retreat.EncounterId, retreat.EncounterId + ".segment.2",
                retreat.LeadId, retreat.CompanionId, retreat.DefenderId, retreat.ControllerId,
                companionConsents ? "TEST_ONLY.reengagement.companion-consent.v1" : "",
                directorAuthorizes ? "TEST_ONLY.reengagement.defender-hold.v1" : "");
            var d = reengagementDefinition;
            const string rule = "EXP-07|FL-15|46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"
                + "hero-0,0-to-0,1|companion-1,2|same-alert-defender-0,2|paid-walk|original-hero-marker|watch-before-start";
            ContentFingerprint = "TEST_ONLY.reengagement-v1-" + RetreatHash(string.Join("|", ContentFingerprint, rule,
                d.RootId, d.SegmentId, d.LeadId, d.CompanionId, d.DefenderId, d.ControllerId, d.ConsentId, d.DirectorMandateId));
            return this;
        }

        private void InitializeReengagement(Snapshot s)
        {
            if (reengagementDefinition != null) s.Reengagement = new ReengagementRecord(reengagementDefinition);
        }

        private static bool ReengagementAvailable(Snapshot s) => s.Reengagement != null && s.Retreat.SuccessfulExit != null
            && !s.InventoryCombat && s.Reengagement.Entry == null;

        private static bool IsReengagementEdge(Snapshot s, WorldTraversalRecord edge)
        {
            if (!ReengagementAvailable(s) || !s.Reengagement.Definition.IsApproach(edge)) return false;
            var d = s.Reengagement.Definition;
            var receipt = s.Receipts.SingleOrDefault(x => x.Revision == edge.StartedRevision);
            return receipt?.Principal == d.ControllerId && edge.StartedRevision > s.Retreat.SuccessfulExit.Revision
                && d.IsWalk(CommandHistory.Read(receipt));
        }

        private static string ReengagementTraversalObstruction(Snapshot s, WorldTraversalRecord edge)
            => IsReengagementEdge(s, edge) && LocalRetreatOpeningBlocked(s) ? "ReengagementOpeningObstructedByPressure" : null;

        private static void SuspendObstructedReengagementApproach(Snapshot s)
        {
            if (!ReengagementAvailable(s) || !LocalRetreatOpeningBlocked(s)) return;
            var edge = s.WorldTraversals.SingleOrDefault(x => x.Status != WorldTraversalStatus.Suspended && IsReengagementEdge(s, x));
            if (edge != null) SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
        }

        private string AssessReengagementDeparture(Snapshot s, Command command)
        {
            if (ReengagementAvailable(s) && command.Actor == s.Reengagement.Definition.DefenderId
                && s.Reengagement.Definition.DirectorMandateId != "")
                return "ReengagementDefenderHoldsActualPosition";
            if (s.Reengagement?.Definition.IsApproachCommand(s, command) != true) return null;
            if (s.Reengagement.Contacts.Count == ReengagementRecord.MaxContacts) return "ReengagementContactCapacityReached";
            return AssessReengagement(s, atContact: false);
        }

        private string AssessReengagement(Snapshot s, bool atContact)
        {
            var d = s.Reengagement.Definition;
            if (d.ConsentId == "") return "ReengagementCompanionConsentMissing";
            if (d.DirectorMandateId == "") return "ReengagementDirectorAuthorityMissing";
            if (LocalRetreatExposure(s) == null) return "ReengagementRouteUnavailable";
            if (LocalRetreatOpeningBlocked(s)) return "ReengagementOpeningObstructedByPressure";
            if (PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s))
                return "ReengagementChoicePending";
            if (s.RestIntervals.Any(x => x.Status == RestIntervalStatus.Active && d.IsParticipant(x.ActorId))
                || s.ExpeditionHavenCareIntervals.Any(x => x.Status == HavenCareIntervalStatus.Active
                    && (d.IsParticipant(x.ActorId) || d.IsParticipant(x.ProviderId)))
                || s.ExpeditionMoraleRestIntervals.Any(x => x.Status == MoraleRestIntervalStatus.Active && d.IsParticipant(x.ActorId)))
                return "ReengagementParticipantInterruptionUnsupported";
            var hero = s.Actors.SingleOrDefault(x => x.Id == d.LeadId);
            var companion = s.Actors.SingleOrDefault(x => x.Id == d.CompanionId);
            var defender = s.Actors.SingleOrDefault(x => x.Id == d.DefenderId);
            if (hero == null || hero.X != 0 || hero.Y != (atContact ? 1 : 0)
                || companion == null || companion.X != 1 || companion.Y != 2
                || defender == null || defender.X != 0 || defender.Y != 2
                || s.WorldTraversals.Any(x => d.IsParticipant(x.ActorId)))
                return "ReengagementParticipantsAbsent";
            if (!new[] { d.LeadId, d.CompanionId, d.DefenderId }.All(x => CapableWorker(s, x) && TestOnlyClubAttackPolicy.Aware(s, x)))
                return "ReengagementParticipantsIneligible";
            if (!WorldWalkable(s, 0, 1) || !WorldWalkable(s, 1, 2) || !WorldWalkable(s, 0, 2)
                || WorldSpatialQueries.Occupied(s, d.LeadId, 0, 1))
                return "ReengagementContactBlocked";
            if (atContact && (!ReengagementMutuallyAware(s, d.LeadId, d.DefenderId)
                || !ReengagementMutuallyAware(s, d.CompanionId, d.DefenderId)))
                return "ReengagementAwarenessUnavailable";
            return null;
        }

        private static bool ReengagementMutuallyAware(Snapshot s, string participant, string defender)
            => TestOnlyClubAttackPolicy.CanSee(s, participant, defender) && TestOnlyClubAttackPolicy.CanSee(s, defender, participant)
                && (!ObservationRules.Enabled(s) || ObservationGeometry.LineOfEffectClear(s, participant, defender));

        private static int ReengagementHeroMarker(Snapshot s, RuleTime at)
        {
            var phase = s.Reinforcement.Admission.Phase;
            long slot = phase.Epoch.SlotAt(at);
            int ordinal = phase.GlobalTurn(slot);
            return phase.Epoch.Start(slot) == at && phase.Actor(ordinal) == s.Reengagement.Definition.LeadId ? ordinal : -1;
        }

        private void ResolveReengagementArrival(Snapshot s, WorldTraversalRecord edge, Command cause, int marker, RuleQuantity distance)
        {
            var r = s.Reengagement;
            var d = r.Definition;
            string error = marker < 0 ? "ReengagementArrivalOutsideHeroStart" : AssessReengagement(s, atContact: true);
            s.Reengagement = r.Append(new ReengagementContact(edge.StartedRevision, s.Revision + 1, cause.Id, s.RuleClock, marker, distance, error ?? ""));
            if (error != null) return;

            var phase = s.Reinforcement.Admission.Phase;
            s.Encounter = new FixedEncounterRecord(d.SegmentId, s.RuleClock, phase.Epoch.Order,
                new[] { s.Revision + 1 }, new[] { marker }, rosterPhase: null, inheritedPhase: phase);
            foreach (var actor in phase.Epoch.Order) PauseParticipantWork(s, actor);
            s.InventoryCombat = true;
            s.InventoryTurnActor = d.LeadId;
            s.InventoryInteractions = Interval(s, d.LeadId).Interactions;
            PauseIncompatibleWork(s);
        }
    }
}
#endif
