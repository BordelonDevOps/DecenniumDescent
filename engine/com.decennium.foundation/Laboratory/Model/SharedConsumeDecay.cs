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
            bool accepted = TemporaryHpRules.Replaces(life.TemporaryHp, offer);
            SetInterval(state, interval.PayAction());
            state.ConsumeDecay = new ConsumeDecayRecord(command.Id, state.Revision + 1, state.RuleClock, offer, accepted);
            if (accepted) ReplaceTemporaryHp(state, life, offer);
            return null;
        }

        private static RuleTime? NextConsumeDecayDeadline(Snapshot state)
            => state.ConsumeDecay?.Active == true ? state.ConsumeDecay.Deadline : (RuleTime?)null;

        internal static void ExpireConsumeDecay(Snapshot state)
        {
            var grant = state.ConsumeDecay;
            if (grant?.Active != true || grant.Deadline != state.RuleClock) return;
            var life = state.Lives.Single(x => x.ActorId == ConsumeDecaySite.Actor);
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
        public static bool Replaces(long remaining, long offer)
        {
            if (remaining < 0 || offer < 0) throw new ArgumentOutOfRangeException(remaining < 0 ? nameof(remaining) : nameof(offer));
            return offer > remaining;
        }
    }
}
#endif
