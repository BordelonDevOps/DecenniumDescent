#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedConsumeDecay;

        internal TestOnlySharedWorldPolicy EnableConnectedConsumeDecay()
        {
            EnableConnectedWoundTreatment();
            connectedConsumeDecay = true;
            ContentFingerprint = ConsumeDecaySite.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                ConsumeDecaySite.Source, "hero-only|bed-1,3|clear-exposed-edge|one-beneficial-long-rest-use|elapsed-3600"));
            return this;
        }

        private string ResolveConsumeDecay(Snapshot state, Command command)
        {
            if (!state.ConnectedConsumeDecay || command.Actor != ConsumeDecaySite.Actor || command.Target != ConsumeDecaySite.Id
                || !state.InventoryCombat || !WorldTiming.IsLaterActive(state))
                return "ConsumeDecayUnavailable";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return "InvalidConsumeDecayRequest";
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "TacticalChoicePending";
            if (state.Encounter.CurrentActor != command.Actor || state.InventoryTurnActor != command.Actor)
                return "WrongRegularTurn";
            if (state.ConsumeDecay != null) return "ConsumeDecayUseSpent";
            var interval = Interval(state, command.Actor);
            if (interval.ActionSpent) return "ActionAlreadySpent";
            if (!CapableWorker(state, command.Actor) || !Permissions(state, command.Actor).Action)
                return "ConsumeDecayActorIncapable";
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            var bed = new CombatCell(ConsumeDecaySite.X, ConsumeDecaySite.Y);
            if (actor.X != 0 || (actor.Y != 2 && actor.Y != 3)
                || PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X, actor.Y), bed) != 5
                || state.WorldTraversals.Any(x => x.ActorId == actor.Id)
                || !ObservationGeometry.LineOfEffectClearToCell(state, actor.Id, bed.X, bed.Y))
                return "ConsumeDecaySubstrateOutOfReach";

            var life = state.Lives.Single(x => x.ActorId == actor.Id);
            int offer = state.Characters.Single(x => x.ActorId == actor.Id).Levels.Count;
            SetInterval(state, interval.PayAction());
            var offered = new ConsumeDecayRecord(command.Id, state.Revision + 1, state.RuleClock, offer, true);
            var winner = TemporaryHpRules.Select(null, life.TemporaryHp, offered);
            bool accepted = ReferenceEquals(winner.Grant, offered);
            state.ConsumeDecay = accepted ? offered
                : new ConsumeDecayRecord(command.Id, state.Revision + 1, state.RuleClock, offer, false);
            if (accepted) ReplaceTemporaryHp(state, life, winner.Remaining);
            return null;
        }

        private static RuleTime? NextConsumeDecayDeadline(Snapshot state)
            => state.ConsumeDecay?.Active == true ? state.ConsumeDecay.Deadline : (RuleTime?)null;

        internal static void ExpireConsumeDecay(Snapshot state, ConsumeDecayRecord scheduled)
        {
            var grant = state.ConsumeDecay;
            var life = state.Lives.Single(x => x.ActorId == ConsumeDecaySite.Actor);
            var remaining = TemporaryHpRules.Expire(grant, life.TemporaryHp, scheduled, state.RuleClock);
            if (remaining.Grant != null) return;
            ReplaceTemporaryHp(state, life, 0);
            EndConsumeDecay(state, grant, TemporaryHpEnd.Expired);
        }

        internal static void ReconcileTemporaryHpLoss(Snapshot state, ActorLifeRecord before, LifeState after)
        {
            var grant = state.ConsumeDecay;
            if (grant?.Active == true && before.ActorId == ConsumeDecaySite.Actor && before.TemporaryHp > 0 && after.TemporaryHp == 0)
                EndConsumeDecay(state, grant, TemporaryHpEnd.Depleted);
        }

        private static void EndConsumeDecay(Snapshot state, ConsumeDecayRecord grant, TemporaryHpEnd cause)
            => state.ConsumeDecay = new ConsumeDecayRecord(grant.CommandId, grant.Revision, grant.StartedAt,
                grant.Offer, grant.Accepted, cause, state.RuleClock, state.Revision + 1);

        private static void ReplaceTemporaryHp(Snapshot state, ActorLifeRecord before, long amount)
        {
            var updated = new ActorLifeRecord(before.ActorId, before.MaximumHp, before.Hp, amount, before.LinkedInjuries,
                before.Stable, before.Dead, before.UsesDeathSaves, before.DeathSuccesses, before.DeathFailures,
                before.StableUntil, before.LastDeathTurn, before.Prone, before.HeldItems);
            state.Lives = state.Lives.Select(x => x.ActorId == before.ActorId ? updated : x).ToArray();
        }
    }

    public static class TemporaryHpRules
    {
        public static (ConsumeDecayRecord Grant, long Remaining) Select(ConsumeDecayRecord current, long remaining, ConsumeDecayRecord offered)
        {
            if (remaining < 0) throw new ArgumentOutOfRangeException(nameof(remaining));
            if (offered?.Active != true) throw new ArgumentException("An active offer is required.", nameof(offered));
            return offered.Offer > remaining ? (offered, offered.Offer) : (current, remaining);
        }

        public static (ConsumeDecayRecord Grant, long Remaining) Expire(ConsumeDecayRecord current, long remaining,
            ConsumeDecayRecord scheduled, RuleTime at)
        {
            bool due = current?.Active == true && scheduled?.Active == true && current.Revision == scheduled.Revision
                && current.CommandId == scheduled.CommandId && current.Deadline == at && scheduled.Deadline == at;
            return due ? (null, 0) : (current, remaining);
        }
    }
}
#endif
