#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlyClubAttackPolicy
    {
        private readonly ConditionCombatFixture conditions;
        public static ConditionLedger ConditionsFor(Snapshot s, string actor)
            => ConditionHistory.Restore(s.Conditions.Single(x => x.Target == actor)).Ledger;
        private static bool WithConditions(Snapshot s) => s.SchemaVersion >= Snapshot.ConditionSchema;
        internal static bool Aware(Snapshot s, string actor) => ActorLifeRules.CanAct(s, actor)
            && (!WithConditions(s) || !ConditionsFor(s, actor).View().Unaware);
        private static ConditionClauses CombatConditions(Snapshot s, string actor)
        {
            var result = WithConditions(s) ? ConditionsFor(s, actor).View().Clauses.Active.ToList() : new System.Collections.Generic.List<ConditionClause>();
            if (!WithConditions(s) && s.Lives.Single(x => x.ActorId == actor).Prone) result.Add(ConditionClause.Prone);
            // The external-condition ledger cannot remove the independently owned zero-HP cause.
            if (ActorLifeRules.ZeroHpUnconscious(s, actor)) { result.Add(ConditionClause.Unconscious); result.Add(ConditionClause.Incapacitated); }
            return ConditionClauses.FromResolved(result);
        }
        private static ConditionPermissions CurrentPermissions(Snapshot s, string actor)
        {
            bool ownTurn = s.Encounter?.CurrentActor == actor;
            long spent = ownTurn ? s.ActorMovement.Single(x => x.ActorId == actor).Spent
                + s.TacticalMoves.Where(x => x.ActorId == actor && x.TurnOrdinal == s.Encounter.TurnOrdinal && EncounterHistory.InCurrent(s,x.Revision) && x.Kind == TacticalMoveKind.Press && x.Status == TacticalMoveStatus.Completed).Sum(x => x.CostPaid) : 0;
            if(ownTurn&&s.WorldSchedule!=null&&s.WorldIntervals.Single(x=>x.ActorId==actor).MovementSpent!=default)spent=Math.Max(1,spent);
            return PlaytestConditions.Permissions(CombatConditions(s, actor), ownTurn && ActionSpent(s) ? 1 : 0, spent);
        }
        private static bool EffectiveProne(Snapshot s, string actor) => WithConditions(s)
            ? ConditionsFor(s, actor).View().Has(ConditionKind.Prone) : s.Lives.Single(x => x.ActorId == actor).Prone;
        private static bool CanSee(Snapshot s, string observer, string target) => !WithConditions(s)
            || Aware(s, observer) && !ConditionsFor(s, observer).View().BlocksSight && !ConditionsFor(s, target).View().Has(ConditionKind.Invisible);
        internal static bool DamageConditionCapacity(Snapshot s, string target)
        {
            if (!WithConditions(s)) return true;
            var journal = s.Conditions.Single(x => x.Target == target);
            return journal.Operations.Count < ConditionJournal.MaxOperations && ConditionsFor(s, target).Applications.Count < ConditionLedger.MaxApplications;
        }
        private static void CommitCondition(Snapshot s, ConditionHistoryTransition result)
        {
            var ledger = result.State.Ledger; string actor = ledger.Target;
            s.Conditions = s.Conditions.Select(x => x.Target == actor ? result.State.Journal : x).ToArray();
            bool prone = ledger.Applications.Any(x => x.Application.Kind == ConditionKind.Prone && x.Present(ledger.Now));
            var before = s.Lives.Single(x => x.ActorId == actor);
            bool drop = result.Consequences.Any(x => x.Kind == ConditionConsequenceKind.DropHeldItems);
            s.Lives = s.Lives.Select(x => x.ActorId == actor ? ActorLifeRules.Record(actor, ActorLifeRules.Read(before), prone, drop ? Array.Empty<string>() : before.HeldItems) : x).ToArray();
            if (drop) DropConditionEquipment(s, actor);
            // This explicitly selected fixture admits no concentration. EndConcentration has
            // no world target; admitting concentration later requires its actual lifecycle.
        }
        private static void DropConditionEquipment(Snapshot s, string actor)
        {
            var body = s.Actors.Single(x => x.Id == actor);
            s.Clubs = s.Clubs.Select(x => x.HeldBy == actor ? new ClubInstance(x.Id, x.ProfileId, x.OwnerId, x.CustodianId, "", body.X, body.Y) : x).ToArray();
        }
        private static void AppendCondition(Snapshot s, string actor, ConditionOperation operation)
            => CommitCondition(s, ConditionHistory.Restore(s.Conditions.Single(x => x.Target == actor)).Append(operation));
        private static void AddPhysicalProne(Snapshot s, string actor, string cause)
        {
            var journal = s.Conditions.Single(x => x.Target == actor);
            string id = "host." + cause + "." + N(s.Revision + 1);
            AppendCondition(s, actor, ConditionOperation.Apply(id, journal.Now,
                new ConditionApplicationData(id, actor, "TEST_ONLY." + cause, "Prone", null, "stand-or-explicit-cure", true)));
        }
        private void InitializeConditions(Snapshot s)
        {
            s.SchemaVersion = Snapshot.ConditionSchema;
            if (conditions.Events.Any(x => !s.Actors.Any(a => a.Id == x.Target) || x.Operation.At.Time < s.RuleClock))
                throw new ArgumentException("Condition event target or timing is outside the fixture.");
            s.Conditions = s.Actors.Select(x => new ConditionJournal(ConditionHistory.PolicyId, x.Id, new ConditionStamp(s.RuleClock))).ToArray();
            foreach (var body in s.Lives.Where(x => x.Prone).ToArray()) AddPhysicalProne(s, body.ActorId, "initial-prone");
        }
        internal static void AdvanceConditions(Snapshot s, string subevent = "")
        {
            if (!WithConditions(s)) return;
            foreach (var journal in s.Conditions.ToArray())
                if (journal.Now.Time < s.RuleClock) AppendCondition(s, journal.Target, ConditionOperation.Advance("host.clock." + N(s.Revision + 1) + subevent, new ConditionStamp(s.RuleClock)));
        }
        private string DispatchCondition(Snapshot s, Command c)
        {
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null) return "InvalidConditionEvent";
            int actors = s.Actors.Length;
            if ((PendingMove(s) != null || CurrentPressOffer(s) != null)
                && s.Receipts.Length + 1 + 3 * (actors + 1) * (actors - 1) > 512)
                return "ContinuationCapacityReached";
            var fact = conditions.Events.SingleOrDefault(x => x.Operation.Id == c.Target && x.Target == c.Actor);
            if (fact == null) return "UnknownConditionEvent";
            var journal = s.Conditions.Single(x => x.Target == fact.Target);
            if (journal.Operations.Any(x => x.Id == fact.Operation.Id)) return "ConditionEventAlreadyResolved";
            if (!journal.Now.Equals(fact.Operation.At)) return "WrongConditionEventTime";
            AppendCondition(s, fact.Target, fact.Operation);
            if ((PendingMove(s) != null || CurrentPressOffer(s) != null) && s.Actors.Any(x => !DamageConditionCapacity(s, x.Id)))
                return "ConditionContinuationCapacityReached";
            AdvanceTacticalFlow(s); return null;
        }
        private static string ConditionActionFailure(Snapshot s, CommandKind kind, string actor)
        {
            if (!WithConditions(s)) return null;
            if (!Aware(s, actor)) return "ActorUnaware";
            var permissions = CurrentPermissions(s, actor);
            if (kind == CommandKind.SelectCombatStance) return null;
            if (kind == CommandKind.DropProne) {
                var ledger = ConditionsFor(s, actor);
                if (ledger.ImmuneTo(ConditionKind.Prone)) return "PronePrevented";
                return CombatConditions(s, actor).Immobile ? "BodyCannotMove" : null;
            }
            if (kind == CommandKind.StandFromProne || kind == CommandKind.TacticalStep)
                return permissions.VoluntarySpeed ? null : "ConditionPreventsMovement";
            if (kind == CommandKind.EncounterDash) return permissions.Dash ? null : "ConditionPreventsDash";
            return permissions.Action ? null : "ConditionPreventsAction";
        }
        private static string PhysicalAttackFailure(Snapshot s, string actor)
        {
            if (!WithConditions(s)) return null;
            if (!Aware(s, actor)) return "ActorUnaware";
            // Delegated prototype completion: residual Stunned/Paralyzed prevents the bodily
            // execution of an ordinary Club/unarmed attack even without its Incapacitated component.
            return CombatConditions(s, actor).Immobile ? "ConditionPreventsPhysicalAttack" : null;
        }
    }
}
#endif
