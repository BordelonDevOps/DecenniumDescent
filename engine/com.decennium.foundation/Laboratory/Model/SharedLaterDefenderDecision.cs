#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : ICommandAdmissionPolicy
    {
        bool ICommandAdmissionPolicy.SupportsAdmission(CommandKind kind)
            => connectedRecipe4Batch && IsDefenderAdmissionCommand(kind);

        private static bool IsDefenderAdmissionCommand(CommandKind kind)
            => kind == CommandKind.SelectCombatStance || kind == CommandKind.AttackClub
                || kind == CommandKind.TacticalStep || kind == CommandKind.EndRegularTurn
                || kind == CommandKind.RespondOpportunityAttack;

        string ICommandAdmissionPolicy.AssessAdmission(Snapshot snapshot, Command command)
        {
            // ResolveCore shares the outer admission gates. These five commands stop before the
            // first tactical write, payment, clock advance or draw in their existing resolver.
            if (command == null || !IsDefenderAdmissionCommand(command.Kind)
                || !UsesLaterDefenderController(snapshot) || command.Actor != LaterDefenderId)
                return "DefenderAdmissionUnavailable";
            return ResolveCore(snapshot, command, assessTactical: true);
        }

        private bool UsesLaterDefenderController(Snapshot state)
            => connectedRecipe4Batch && state?.TestOnly == true && state.ContentFingerprint == ContentFingerprint
                && state.ConnectedBatch != null && state.InventoryCombat && WorldTiming.IsLaterActive(state)
                && state.Encounter.Order.Contains(LaterDefenderId);

        /// <summary>Trusted snapshot projection. The decision policy sees only the returned view.</summary>
        public DefenderDecisionView ObserveLaterDefender(Snapshot state, Authority grant)
        {
            if (!UsesLaterDefenderController(state) || !LaterDefenderController.HasGrant(grant))
                return new DefenderDecisionView();

            // A live ordinary movement offer precedes queued post-step records. The body's
            // pending knockout and the shared calendar's earlier responses still take priority.
            if (HasPendingRecoveryOffer(state) || ManufacturingChoicePending(state)
                || PendingDefensiveFormationShift(state) != null || PendingCommandStepOffer(state) != null
                || state.OverwatchRiderChoices.Any(x => x.Status == OverwatchRiderChoiceStatus.Pending)
                || state.MeleeAttacks.Any(x => x.Pending))
                return new DefenderDecisionView();

            var move = TestOnlyClubAttackPolicy.PendingMove(state);
            if (move != null) {
                if (move.ResponseIndex >= move.Reactors.Count || move.Reactors[move.ResponseIndex] != LaterDefenderId
                    || !TestOnlyClubAttackPolicy.EligibleOpportunity(state, LaterDefenderId, move))
                    return new DefenderDecisionView();
                return ObserveDefenderSlot(state, DefenderDecisionSlot.Opportunity, move.ActorId);
            }
            if (PendingCalendarChoice(state) || state.Encounter.CurrentActor != LaterDefenderId)
                return new DefenderDecisionView();
            return ObserveDefenderSlot(state, DefenderDecisionSlot.RegularTurn, "");
        }

        private static DefenderDecisionView ObserveDefenderSlot(Snapshot state, DefenderDecisionSlot slot, string provoker)
        {
            var own = state.Actors.Single(x => x.Id == LaterDefenderId);
            var ownCell = new CombatCell(own.X, own.Y);
            var life = state.Lives.Single(x => x.ActorId == LaterDefenderId);
            bool hasClub = life.HeldItems.Contains(LaterDefenderClubId) && state.Clubs.Any(club => club.Id == LaterDefenderClubId
                && club.OwnerId == LaterDefenderId && club.ProfileId == TestOnlyClubAttackPolicy.ClubProfile
                && club.HeldBy == LaterDefenderId && club.CustodianId == LaterDefenderId);
            var seen = state.Actors.Where(actor => actor.Id != LaterDefenderId
                && ObservationRules.CanSee(state, LaterDefenderId, actor.Id)).ToArray();
            var opponents = seen.Where(actor => state.Encounter.Order.Contains(actor.Id)
                && !SoldierTacticalFeatures.IsAlly(state, LaterDefenderId, actor.Id))
                .OrderBy(actor => actor.Id, StringComparer.Ordinal)
                .Select(actor => new DefenderVisibleOpponent(actor.Id, new CombatCell(actor.X, actor.Y),
                    ObservationGeometry.LineOfEffectClear(state, LaterDefenderId, actor.Id))).ToArray();
            if (slot == DefenderDecisionSlot.Opportunity)
                return new DefenderDecisionView(slot, ownCell, hasClub: hasClub, eligibleOpportunity: true,
                    visibleProvokerId: opponents.Any(actor => actor.ActorId == provoker) ? provoker : "",
                    visibleOpponents: opponents);

            bool aware = TestOnlyClubAttackPolicy.Aware(state, LaterDefenderId);
            var permissions = TestOnlyClubAttackPolicy.CurrentPermissions(state, LaterDefenderId);
            bool canAttack = aware && permissions.Action && !TestOnlyClubAttackPolicy.ActionSpent(state)
                && TestOnlyClubAttackPolicy.PhysicalAttackFailure(state, LaterDefenderId) == null;
            bool canMove = aware && permissions.VoluntarySpeed
                && TestOnlyClubAttackPolicy.RemainingMovement(state, LaterDefenderId) > default(RuleQuantity);
            return new DefenderDecisionView(slot, ownCell, aware, TestOnlyClubAttackPolicy.HasStance(state),
                canAttack, canMove, hasClub, visibleOpponents: opponents,
                approachCells: canMove ? KnownDefenderApproachCells(state, ownCell, seen) : null);
        }

        private static IEnumerable<CombatCell> KnownDefenderApproachCells(Snapshot state, CombatCell origin, ActorState[] seen)
        {
            // The selected arena's authored floor and side walls are known to this resident
            // defender. Dynamic occupancy and reservations are visible only through direct sight.
            bool Walkable(int x, int y) => TestOnlyPolicy.Walkable(x, y) && ObservationGeometry.SupportsAnchorAt(state, x, y);
            for (int x = origin.X - 1; x <= origin.X + 1; x++)
                for (int y = origin.Y - 1; y <= origin.Y + 1; y++) {
                    if (!WorldSpatialQueries.Neighbor(origin.X, origin.Y, x, y, diagonals: true)
                        || !Walkable(x, y) || seen.Any(actor => actor.X == x && actor.Y == y)) continue;
                    var cell = new CombatCell(x, y);
                    if (PlanarCombatGeometry.NeighborPassesCornerRule(origin, cell,
                        !Walkable(x, origin.Y), !Walkable(origin.X, y))) yield return cell;
                }
        }
    }
}
#endif
