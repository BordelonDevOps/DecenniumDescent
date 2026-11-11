#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyLivingOpponentRetreatProfile
    {
        public bool LeadAuthorized { get; }
        public bool CompanionConsents { get; }
        public bool RouteAuthorized { get; }

        public TestOnlyLivingOpponentRetreatProfile(bool leadAuthorized = true, bool companionConsents = true,
            bool routeAuthorized = true, ExpeditionRouteQuality quality = ExpeditionRouteQuality.Known, int risk = 1)
        {
            if (quality != ExpeditionRouteQuality.Known || risk != 1)
                throw new ArgumentException("This opening has Known route authority and Risk 1.");
            LeadAuthorized = leadAuthorized;
            CompanionConsents = companionConsents;
            RouteAuthorized = routeAuthorized;
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private RetreatDefinition retreatDefinition;

        public TestOnlySharedWorldPolicy EnableLivingOpponentRetreat(TestOnlyLivingOpponentRetreatProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || retreatDefinition != null || SelectedSchema != Snapshot.ReinforcementSchema
                || routeTravelFixture != null || expeditionPressureProfile != null)
                throw new InvalidOperationException("Select the local retreat on the reinforced host before initialization.");
            const string routeFacts = "FL-08|FL-15|46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|north-lanes-x0-x1-y3-y0|"
                + "cross-y1|two-walking-members|tier1-dc12|known-risk1-pressure1|watch-closure-900-3600|no-haven";
            var reinforcement = reinforcementDefinition;
            retreatDefinition = new RetreatDefinition("TEST_ONLY.fl15.north-withdrawal.v1", laterEncounterDefinition.EncounterId,
                laterEncounterDefinition.HeroId, reinforcement.CompanionId, laterEncounterDefinition.DefenderId,
                laterEncounterDefinition.DefenderClubId, reinforcement.ControllerId,
                profile.LeadAuthorized ? "TEST_ONLY.fl15.hero-lead.v1" : "",
                profile.CompanionConsents ? "TEST_ONLY.fl15.companion-consent.v1" : "",
                "TEST_ONLY.fl15.local-operation.v1", "TEST_ONLY.fl15.north-opening",
                profile.RouteAuthorized ? "TEST_ONLY.fl15.north-access.v1" : "",
                "TEST_ONLY.fl15.route-" + RetreatHash(routeFacts),
                "TEST_ONLY.fl15.party-pressure", "TEST_ONLY.fl15.north-exposure");
            var d = retreatDefinition;
            string binding = string.Join("|", ContentFingerprint, routeFacts, d.Id, d.EncounterId, d.LeadId, d.CompanionId,
                d.DefenderId, d.ClubId, d.ControllerId, d.LeadMandateId, d.CompanionConsentId, d.OperationId, d.RouteId,
                d.RouteAccessId, d.RouteFingerprint, d.CohortId, d.ExposureId);
            ContentFingerprint = "TEST_ONLY.fl15-v1-" + RetreatHash(binding);
            bodies.ConfigurePressureMovement(AssessLocalRetreatMovement, (_, __, ___, ____, _____, ______) => false,
                (_, __, ___, ____) => { });
            return this;
        }

        private static string RetreatHash(string text)
        {
            using (var sha = SHA256.Create())
                return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(text)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private void InitializeRetreat(Snapshot state)
        {
            if (retreatDefinition != null) state.Retreat = new RetreatRecord(retreatDefinition);
        }

        private static bool AtRetreatRoundStart(FixedEncounterRecord encounter)
            => encounter?.RosterPhase != null && (encounter.TurnOrdinal - encounter.RosterPhase.FirstTurn) % 3 == 0;

        private static RetreatPosition RetreatBody(Snapshot s, string actor)
        {
            var body = s.Actors.Single(x => x.Id == actor);
            return new RetreatPosition(body.X, body.Y);
        }

        private bool RetreatLaneAvailable(Snapshot s, RetreatDefinition d, string actor)
        {
            var at = RetreatBody(s, actor);
            if (!d.IsLanePoint(actor, at.X, at.Y) || !CapableWorker(s, actor) || !Permissions(s, actor).VoluntarySpeed
                || Speed(s, actor) == 0 || s.WorldTraversals.Any(x => x.ActorId == actor)) return false;
            for (int y = at.Y - 1; y >= d.CrossingY; y--) {
                if (!WorldWalkable(s, at.X, y) || WorldSpatialQueries.Occupied(s, actor, at.X, y)) return false;
            }
            return !LocalRetreatOpeningBlocked(s);
        }

        private string AssessRetreatInstruction(Snapshot s, Command c)
        {
            var retreat = s.Retreat;
            if (retreat == null || retreatDefinition == null) return "RetreatNotSelected";
            var d = retreat.Definition;
            if (c.Actor != d.LeadId) return "RetreatLeadUnauthorized";
            if (c.Target != d.Id) return "UnknownRetreatDefinition";
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Ranged != null || c.Advancement != null)
                return "InvalidRetreatPayload";
            if (PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s))
                return "TacticalChoicePending";
            if (d.LeadMandateId == "") return "RetreatLeadMandateMissing";
            if (d.CompanionConsentId == "") return "RetreatCompanionConsentMissing";
            if (d.RouteAccessId == "") return "RetreatRouteAuthorityMissing";
            if (s.Encounter?.Id != d.EncounterId || !s.InventoryCombat || s.Encounter.RosterPhase == null || ResolvedConflict(s))
                return "RetreatEncounterUnavailable";
            if (c.Kind == CommandKind.DeclareRetreat) {
                if (retreat.Round != null) return "RetreatAlreadyAttempted";
                if (!AtRetreatRoundStart(s.Encounter) || s.Encounter.StartRevisions.Last() != s.Revision
                    || s.Encounter.StartAt(s.Encounter.TurnOrdinal) != s.RuleClock) return "RetreatRequiresUnconsumedRoundStart";
                if (LocalRetreatExposure(s) == null) return "RetreatPressureAuthorityMissing";
                return RetreatLaneAvailable(s, d, d.LeadId) && RetreatLaneAvailable(s, d, d.CompanionId)
                    ? null : "RetreatOpeningUnavailable";
            }
            if (!retreat.Active) return "RetreatNotActive";
            if (c.Kind == CommandKind.AbandonRetreat) return null;
            if (s.Encounter.CurrentActor != d.LeadId || retreat.Round.Number != s.Encounter.Round)
                return "RetreatRequiresLeadTurn";
            if (retreat.Round.Task != null) return "RetreatTaskAlreadyPaid";
            if (Interval(s, d.LeadId).ActionSpent) return "ActionAlreadySpent";
            if (!Permissions(s, d.LeadId).Action || !CapableWorker(s, d.LeadId)) return "RetreatLeadIncapable";
            return RetreatLaneAvailable(s, d, d.LeadId) ? null : "RetreatOpeningUnavailable";
        }

        private IEnumerable<Command> DiscoverRetreatCommands(Snapshot s, Authority authority, string actor)
        {
            var d = s.Retreat?.Definition;
            if (d == null || actor != d.LeadId || authority.Principal != d.ControllerId || !authority.Controls(d.CompanionId)) yield break;
            foreach (var kind in new[] { CommandKind.DeclareRetreat, CommandKind.AttemptRetreatEscape, CommandKind.AbandonRetreat }) {
                var option = new Command("option.retreat." + Number(s.Revision) + "." + kind, actor, s.Revision, kind, d.Id);
                if (AssessRetreatInstruction(s, option) == null) yield return option;
            }
        }

        private string ResolveRetreatInstruction(Snapshot s, Command c)
        {
            string error = AssessRetreatInstruction(s, c);
            if (error != null) return error;
            var retreat = s.Retreat;
            var d = retreat.Definition;
            var e = s.Encounter;
            if (c.Kind == CommandKind.DeclareRetreat) {
                s.Retreat = new RetreatRecord(d, s.Revision + 1, c.Id, new[] {
                    new RetreatRound(e.Round, e.TurnOrdinal, e.StartRevisions.Last(), s.RuleClock)
                });
            } else if (c.Kind == CommandKind.AbandonRetreat) {
                RecordRetreatSettlement(s, c, RetreatOutcome.Abandoned);
            } else {
                var facts = CharacterStateFacts.ForActor(s, d.LeadId);
                int modifier = facts.TotalWithInjury(CharacterAbility.Dexterity);
                bool disadvantage = View(s, d.LeadId).Has(ConditionKind.Poisoned)
                    || ExpeditionStrainRules.Current(s, d.LeadId).ExpeditionCheckDisadvantage;
                uint before = s.RandomState;
                var roll = RuleDice.RollD20(before, disadvantageSources: disadvantage ? 1 : 0);
                var result = RuleResolution.TaskCheck(roll.Natural, modifier, d.TaskDc);
                s.RandomState = roll.NextRandomState;
                SetInterval(s, Interval(s, d.LeadId).PayAction());
                s.Retreat = retreat.WithRound(retreat.Round.WithTask(new RetreatTaskRecord(s.Revision + 1, c.Id,
                    s.RuleClock, e.TurnOrdinal, modifier, roll.First, roll.Second ?? 0, before, roll.NextRandomState,
                    roll.WordsConsumed, (RetreatTaskDegree)result.Degree)));
            }
            return null;
        }

        private static string RetreatHostileAttackFailure(Snapshot s, Command c)
        {
            var retreat = s.Retreat;
            if (retreat?.Active != true || c.Actor != retreat.Definition.DefenderId) return null;
            var d = retreat.Definition;
            if (c.Kind == CommandKind.RespondOpportunityAttack && c.Combat?.Choice == true)
                return "RetreatAdditionalHostileAttackUnsupported";
            if (c.Kind != CommandKind.AttackClub && c.Kind != CommandKind.AttackUnarmed
                && c.Kind != CommandKind.AttackRepeatingCrossbow && c.Kind != CommandKind.RespondOverwatch
                && c.Kind != CommandKind.RespondReady) return null;
            if (PendingCalendarChoice(s)) return null;
            return c.Kind == CommandKind.AttackClub && c.Target == d.LeadId && c.Combat?.WeaponId == d.ClubId
                && retreat.Round.ThreatId == "" ? null : "RetreatAdditionalHostileAttackUnsupported";
        }

        private static void ReconcileRetreat(Snapshot s, Command cause)
        {
            var retreat = s.Retreat;
            if (retreat?.Active != true) return;
            if (s.Encounter?.Id == retreat.Definition.EncounterId && ResolvedConflict(s)) {
                RecordRetreatSettlement(s, cause, RetreatOutcome.OpponentResolved);
                return;
            }
            var d = retreat.Definition;
            var attack = s.MeleeAttacks.SingleOrDefault(x => x.Revision == s.Revision + 1 && x.AttackerId == d.DefenderId
                && x.TargetId == d.LeadId && x.WeaponId == d.ClubId && !x.Opportunity);
            if (attack != null) s.Retreat = retreat.WithRound(retreat.Round.WithThreat(attack.Id));
        }

        private static string RetreatCrossing(Snapshot s, RetreatRecord retreat, string actor, RetreatPosition position)
        {
            var d = retreat.Definition;
            if (!d.IsLanePoint(actor, position.X, position.Y) || position.Y > d.CrossingY) return "";
            return s.TacticalMoves.LastOrDefault(x => x.ActorId == actor && d.IsCrossing(x)
                && x.ResolvedRevision > retreat.DeclaredRevision && EncounterHistory.InCurrent(s, x.Revision))?.Id ?? "";
        }

        private static void RecordRetreatSettlement(Snapshot s, Command cause, RetreatOutcome outcome)
        {
            var retreat = s.Retreat;
            var d = retreat.Definition;
            var lead = RetreatBody(s, d.LeadId);
            var companion = RetreatBody(s, d.CompanionId);
            var end = new RetreatSettlement(outcome, s.Revision + 1, cause.Id, s.RuleClock, s.Encounter.TurnOrdinal,
                lead, companion, RetreatBody(s, d.DefenderId), RetreatCrossing(s, retreat, d.LeadId, lead),
                RetreatCrossing(s, retreat, d.CompanionId, companion));
            s.Retreat = retreat.WithRound(retreat.Round.Settle(end));
        }

        private static bool AtRetreatSettlement(Snapshot s, Command cause, RuleTime next, RuleTime target)
            => s.Retreat?.Active == true && s.Encounter?.Id == s.Retreat.Definition.EncounterId
                && cause?.Kind == CommandKind.EndRegularTurn && next == target
                && s.Encounter.TurnOrdinal == s.Retreat.Round.FirstTurn + 2;

        private void SettleRetreatRound(Snapshot s, Command cause)
        {
            var retreat = s.Retreat;
            var round = retreat.Round;
            var d = retreat.Definition;
            var encounter = s.Encounter;
            var threat = s.MeleeAttacks.SingleOrDefault(x => x.Id == round.ThreatId);
            RetreatOutcome result;
            if (ResolvedConflict(s)) result = RetreatOutcome.OpponentResolved;
            else if (round.Task == null || threat == null || threat.Pending) result = RetreatOutcome.Incomplete;
            else {
                result = RetreatRules.ResolveCounters(retreat.Escape + RetreatRules.Escape(round.Task.Degree),
                    retreat.Pursuit + RetreatRules.Pursuit(round.Task.Degree));
                if (result == RetreatOutcome.Successful && (!RetreatLaneAvailable(s, d, d.LeadId)
                    || !RetreatLaneAvailable(s, d, d.CompanionId)
                    || RetreatCrossing(s, retreat, d.LeadId, RetreatBody(s, d.LeadId)) == ""
                    || RetreatCrossing(s, retreat, d.CompanionId, RetreatBody(s, d.CompanionId)) == ""))
                    result = RetreatOutcome.PhysicallyBlocked;
            }
            RecordRetreatSettlement(s, cause, result);
            if (result == RetreatOutcome.Successful) {
                var phase = s.Reinforcement.Admission.Phase;
                s.Reinforcement = s.Reinforcement.At(phase.Epoch.SlotAt(s.RuleClock));
                RecordSuccessfulRetreatPressure(s, cause);
                s.InventoryCombat = false;
                s.InventoryTurnActor = "";
                s.InventoryInteractions = 0;
                CharacterAdvancementRules.TacticalExit(s);
                RecordActualCombatExit(s, encounter, cause);
                return;
            }

            RefreshReinforcementEpoch(s);
            if (result == RetreatOutcome.Continue)
                s.Retreat = s.Retreat.Continue(new RetreatRound(round.Number + 1, encounter.TurnOrdinal + 1,
                    s.Revision + 1, s.RuleClock));
        }
    }
}
#endif
