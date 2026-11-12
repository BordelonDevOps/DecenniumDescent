#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public enum DefenderDecisionSlot { Waiting, RegularTurn, Opportunity }
    public enum DefenderIntentKind { Wait, Guard, Attack, Step, End, AcceptOpportunity, DeclineOpportunity }

    public readonly struct DefenderIntent
    {
        public DefenderIntentKind Kind { get; }
        public string TargetId { get; }
        public CombatCell Destination { get; }

        internal DefenderIntent(DefenderIntentKind kind, string targetId = "", CombatCell destination = default)
        { Kind = kind; TargetId = targetId; Destination = destination; }
    }

    public sealed class DefenderVisibleOpponent
    {
        public string ActorId { get; }
        public CombatCell Cell { get; }
        public bool ClearLineOfEffect { get; }

        internal DefenderVisibleOpponent(string actorId, CombatCell cell, bool clearLineOfEffect)
        { ActorId = actorId; Cell = cell; ClearLineOfEffect = clearLineOfEffect; }
    }

    public sealed class DefenderDecisionView
    {
        public DefenderDecisionSlot Slot { get; }
        public CombatCell OwnCell { get; }
        public bool CanSelectStance { get; }
        public bool StanceSelected { get; }
        public bool CanAttack { get; }
        public bool CanMove { get; }
        public bool HasClub { get; }
        public bool EligibleOpportunity { get; }
        public string VisibleProvokerId { get; }
        public IReadOnlyList<DefenderVisibleOpponent> VisibleOpponents { get; }
        public IReadOnlyList<CombatCell> ApproachCells { get; }

        internal DefenderDecisionView(DefenderDecisionSlot slot = DefenderDecisionSlot.Waiting, CombatCell ownCell = default,
            bool canSelectStance = false, bool stanceSelected = false, bool canAttack = false, bool canMove = false,
            bool hasClub = false, bool eligibleOpportunity = false, string visibleProvokerId = "",
            IEnumerable<DefenderVisibleOpponent> visibleOpponents = null, IEnumerable<CombatCell> approachCells = null)
        {
            Slot = slot; OwnCell = ownCell; CanSelectStance = canSelectStance; StanceSelected = stanceSelected;
            CanAttack = canAttack; CanMove = canMove; HasClub = hasClub;
            EligibleOpportunity = eligibleOpportunity; VisibleProvokerId = visibleProvokerId;
            VisibleOpponents = Array.AsReadOnly(visibleOpponents?.ToArray() ?? Array.Empty<DefenderVisibleOpponent>());
            ApproachCells = Array.AsReadOnly(approachCells?.ToArray() ?? Array.Empty<CombatCell>());
        }
    }

    /// <summary>Pure TEST_ONLY tactics for the existing later defender.</summary>
    public static class LaterDefenderDecisionPolicy
    {
        public static DefenderIntent Select(DefenderDecisionView view)
        {
            if (view == null) throw new ArgumentNullException(nameof(view));
            if (view.Slot == DefenderDecisionSlot.Waiting) return new DefenderIntent(DefenderIntentKind.Wait);
            if (view.Slot == DefenderDecisionSlot.Opportunity) {
                bool accept = view.EligibleOpportunity && view.HasClub && view.VisibleOpponents.Any(x =>
                    x.ActorId == view.VisibleProvokerId && x.ClearLineOfEffect);
                return new DefenderIntent(accept ? DefenderIntentKind.AcceptOpportunity : DefenderIntentKind.DeclineOpportunity);
            }
            if (!view.StanceSelected && view.CanSelectStance) return new DefenderIntent(DefenderIntentKind.Guard);
            if (!view.CanAttack || !view.HasClub) return new DefenderIntent(DefenderIntentKind.End);

            var ranked = view.VisibleOpponents.OrderBy(x => PlanarCombatGeometry.DistanceFeet(view.OwnCell, x.Cell))
                .ThenBy(x => x.ActorId, StringComparer.Ordinal).ToArray();
            var attack = ranked.FirstOrDefault(x => x.ClearLineOfEffect && PlanarCombatGeometry.DistanceFeet(view.OwnCell, x.Cell) <= 5);
            if (attack != null) return new DefenderIntent(DefenderIntentKind.Attack, attack.ActorId);

            var target = ranked.FirstOrDefault();
            if (view.CanMove && target != null) {
                long distance = PlanarCombatGeometry.DistanceFeet(view.OwnCell, target.Cell);
                var steps = view.ApproachCells.Select(cell => (Cell: cell, Distance: PlanarCombatGeometry.DistanceFeet(cell, target.Cell)))
                    .Where(step => step.Distance < distance).OrderBy(step => step.Distance)
                    .ThenBy(step => step.Cell.X).ThenBy(step => step.Cell.Y).Take(1).ToArray();
                if (steps.Length != 0) return new DefenderIntent(DefenderIntentKind.Step, destination: steps[0].Cell);
            }
            return new DefenderIntent(DefenderIntentKind.End);
        }
    }

    public sealed class LaterDefenderDecision
    {
        internal LaterDefenderController Owner { get; }
        internal Command Fallback { get; }
        public DefenderDecisionView View { get; }
        public DefenderIntent Intent { get; }
        public Command Primary { get; }

        internal LaterDefenderDecision(LaterDefenderController owner, DefenderDecisionView view, DefenderIntent intent,
            Command primary, Command fallback)
        { Owner = owner; View = view; Intent = intent; Primary = primary; Fallback = fallback; }
    }

    public enum DefenderDispatchStatus { Waiting, Committed, Duplicate, Stale, Rejected }

    /// <summary>Trusted caller adapter. One plan may commit at most one ordinary command.</summary>
    public sealed class LaterDefenderController
    {
        public const string Principal = "TEST_ONLY.tac10-later-defender.v1";
        private readonly Simulation simulation;
        private readonly TestOnlySharedWorldPolicy policy;
        private readonly object deliveryLock = new object();

        public LaterDefenderController(Simulation simulation, TestOnlySharedWorldPolicy policy)
        {
            this.simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            this.policy = policy ?? throw new ArgumentNullException(nameof(policy));
        }

        public static Authority DefenderAuthority()
            => new Authority(Principal, new[] { TestOnlySharedWorldPolicy.LaterDefenderId },
                inventoryOwners: new[] { TestOnlySharedWorldPolicy.LaterDefenderId });

        internal static bool HasGrant(Authority grant)
            => grant?.Principal == Principal && grant.Controls(TestOnlySharedWorldPolicy.LaterDefenderId)
                && grant.MayUseInventory(TestOnlySharedWorldPolicy.LaterDefenderId);

        public LaterDefenderDecision Plan(Authority grant)
        {
            var snapshot = simulation.Capture();
            var view = policy.ObserveLaterDefender(snapshot, grant);
            var intent = LaterDefenderDecisionPolicy.Select(view);
            Command primary = Materialize(snapshot, intent);
            Command fallback = null;
            if (intent.Kind == DefenderIntentKind.Attack || intent.Kind == DefenderIntentKind.Step)
                fallback = Materialize(snapshot, new DefenderIntent(DefenderIntentKind.End));
            if (intent.Kind == DefenderIntentKind.AcceptOpportunity)
                fallback = Materialize(snapshot, new DefenderIntent(DefenderIntentKind.DeclineOpportunity));
            return new LaterDefenderDecision(this, view, intent, primary, fallback);
        }

        public DefenderDispatchStatus Dispatch(Authority grant, LaterDefenderDecision decision)
        {
            if (decision == null || decision.Owner != this || !HasGrant(grant)) return DefenderDispatchStatus.Rejected;
            if (decision.Primary == null) return DefenderDispatchStatus.Waiting;

            // A repeated delivery checks the same two command identities. It never creates an additional action.
            lock (deliveryLock) {
                var authority = DefenderAuthority();
                var primary = simulation.AssessCommandAdmission(authority, decision.Primary);
                if (primary.Status == CommandAdmissionStatus.AlreadyCommitted || primary.Status == CommandAdmissionStatus.Admitted)
                    return Execute(authority, decision.Primary);
                if (decision.Fallback != null && primary.Code == "StaleRevision") {
                    var previousFallback = simulation.AssessCommandAdmission(authority, decision.Fallback);
                    if (previousFallback.Status == CommandAdmissionStatus.AlreadyCommitted)
                        return Execute(authority, decision.Fallback);
                }
                if (primary.Status != CommandAdmissionStatus.RuleDenied) return RejectedAdmission(primary.Code);
                if (!MayFallback(primary.Code) || decision.Fallback == null) return RuleDenial(primary.Code);
                var fallback = simulation.AssessCommandAdmission(authority, decision.Fallback);
                if (fallback.Status == CommandAdmissionStatus.Admitted || fallback.Status == CommandAdmissionStatus.AlreadyCommitted)
                    return Execute(authority, decision.Fallback);
                return fallback.Status == CommandAdmissionStatus.RuleDenied
                    ? RuleDenial(fallback.Code) : RejectedAdmission(fallback.Code);
            }
        }

        private DefenderDispatchStatus Execute(Authority authority, Command command)
        {
            var result = simulation.Execute(authority, command);
            if (result.Outcome == Outcome.Committed) return DefenderDispatchStatus.Committed;
            if (result.Outcome == Outcome.Duplicate) return DefenderDispatchStatus.Duplicate;
            return RejectedAdmission(result.Code);
        }

        private static DefenderDispatchStatus RejectedAdmission(string code)
            => code == "StaleRevision" ? DefenderDispatchStatus.Stale : DefenderDispatchStatus.Rejected;

        private static DefenderDispatchStatus RuleDenial(string code)
        {
            if (MayFallback(code) || code == "OpportunityNoLongerEligible" || code == "TacticalChoicePending"
                || code == "ManufacturingChoicePending" || code == "ExpeditionStrainRecoveryChoicePending")
                return DefenderDispatchStatus.Waiting;
            return DefenderDispatchStatus.Rejected;
        }

        private static bool MayFallback(string code)
        {
            switch (code) {
                case "BlockedTacticalStep":
                case "OccupiedTacticalStep":
                case "InsufficientMovement":
                case "ZeroSpeedCannotMove":
                case "MoverCannotAct":
                case "ConditionPreventsMovement":
                case "HuntingTrapTetherPreventsMovement":
                case "InvalidLivingTarget":
                case "TargetOutsideEncounter":
                case "TargetLocationUnknown":
                case "BlockedLineOfEffect":
                case "TargetOutOfReach":
                case "ClubNotHeld":
                case "OverwatchAttackTriggerNotImplemented":
                    return true;
                default:
                    return false;
            }
        }

        private static Command Materialize(Snapshot state, DefenderIntent intent)
        {
            if (intent.Kind == DefenderIntentKind.Wait) return null;
            const string actor = TestOnlySharedWorldPolicy.LaterDefenderId;
            string turn = state.Encounter.CurrentTurnId;
            string target = turn;
            CombatRequest combat = null;
            CombatCell cell = default;
            CommandKind kind;
            switch (intent.Kind) {
                case DefenderIntentKind.Guard:
                    kind = CommandKind.SelectCombatStance;
                    target = "";
                    combat = new CombatRequest(turn, stance: (int)CombatStance.Guarded);
                    break;
                case DefenderIntentKind.Attack:
                    kind = CommandKind.AttackClub;
                    target = intent.TargetId;
                    combat = new CombatRequest(turn, TestOnlySharedWorldPolicy.LaterDefenderClubId, pressInstruction: PressHitInstruction.KeepExisting);
                    break;
                case DefenderIntentKind.Step:
                    kind = CommandKind.TacticalStep;
                    cell = intent.Destination;
                    break;
                case DefenderIntentKind.End:
                    kind = CommandKind.EndRegularTurn;
                    break;
                default:
                    kind = CommandKind.RespondOpportunityAttack;
                    target = TestOnlyClubAttackPolicy.PendingMove(state).Id;
                    combat = intent.Kind == DefenderIntentKind.AcceptOpportunity
                        ? new CombatRequest(turn, TestOnlySharedWorldPolicy.LaterDefenderClubId, choice: true,
                            pressInstruction: PressHitInstruction.KeepExisting)
                        : new CombatRequest(turn);
                    break;
            }
            var key = FormattableString.Invariant($"{Principal}|{actor}|{state.Encounter.Id}|{turn}|{state.Revision}|{intent.Kind}|{target}|{cell.X}|{cell.Y}");
            using (var sha = SHA256.Create()) {
                string id = "tac10." + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key))
                    .Select(value => value.ToString("x2", CultureInfo.InvariantCulture)));
                return new Command(id, actor, state.Revision, kind, target, cell.X, cell.Y, combat: combat);
            }
        }
    }
}
#endif
