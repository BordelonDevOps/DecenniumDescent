#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedCompanionStabilization;

        internal TestOnlySharedWorldPolicy EnableConnectedCompanionStabilization()
        {
            EnableConnectedCompanionDose();
            connectedCompanionStabilization = true;
            ContentFingerprint = ConnectedVialRules.StabilizationFingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, "ordinary-medicine|dc10|five-foot-clear|action|stable-recovery"));
            return this;
        }

        private string ResolveCompanionStabilization(Snapshot state, Command command)
        {
            if (!state.ConnectedCompanionStabilization || !state.InventoryCombat
                || state.Reinforcement?.Admission == null
                || state.Encounter?.Id != state.Reinforcement.Definition.EncounterId
                || command.Actor != ConnectedVialRules.CarrierId || command.Target != ConnectedVialRules.CompanionRecipientId
                || !state.Encounter.Order.Contains(command.Target))
                return "CompanionStabilizationUnavailable";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return "InvalidCompanionStabilizationRequest";
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "TacticalChoicePending";
            if (state.Encounter.CurrentActor != command.Actor || state.InventoryTurnActor != command.Actor)
                return "WrongRegularTurn";
            var interval = Interval(state, command.Actor);
            if (interval.ActionSpent) return "ActionAlreadySpent";
            if (!CapableWorker(state, command.Actor) || !Permissions(state, command.Actor).Action)
                return "ConditionPreventsAction";
            if (OrdinaryInventory.Busy(state, command.Actor) || state.WorldTraversals.Any(x => x.ActorId == command.Actor || x.ActorId == command.Target))
                return "StabilizationRequiresStationaryAccess";
            if (AvailableHands(state, command.Actor) < 1) return "UsableHandRequired";
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            var patient = state.Actors.Single(x => x.Id == command.Target);
            if (PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X, actor.Y), new CombatCell(patient.X, patient.Y)) > 5
                || !ObservationGeometry.LineOfEffectClear(state, actor.Id, patient.Id))
                return "StabilizationTargetOutOfReach";
            var before = state.Lives.Single(x => x.ActorId == patient.Id);
            if (!Dying(before)) return "StabilizationTargetNotDying";

            var facts = CharacterStateFacts.ForActor(state, actor.Id, "medicine");
            int modifier = facts.TotalWithInjury(CharacterAbility.Wisdom);
            bool disadvantage = View(state, actor.Id).Has(ConditionKind.Poisoned)
                || ExpeditionStrainRules.Current(state, actor.Id).ExpeditionCheckDisadvantage;
            uint randomBefore = state.RandomState;
            var roll = PlaytestDice.RollD20(randomBefore, disadvantageSources: disadvantage ? 1 : 0);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, CompanionStabilizationAttempt.DC);
            uint randomAfter = roll.NextRandomState;
            long words = roll.WordsConsumed;
            int recoveryDie = 0;
            SetInterval(state, interval.PayAction());
            if (check.Success) {
                var recovery = DiceStream.Draw(randomAfter, 4);
                recoveryDie = recovery.Value + 1;
                randomAfter = recovery.NextState;
                words = checked(words + recovery.WordsConsumed);
                var stabilized = PlaytestLife.StabilizeAt(ActorLifeRules.ReadForResolution(state, before), recoveryDie, state.RuleClock);
                TestOnlyClubAttackPolicy.ApplyLife(state, before, stabilized);
                ReconcileDyingCadences(state);
            }
            state.RandomState = randomAfter;
            state.CompanionStabilizations = state.CompanionStabilizations.Append(new CompanionStabilizationAttempt(
                command.Id, state.Revision + 1, actor.Id, patient.Id, state.Encounter.TurnOrdinal, state.RuleClock,
                roll.First, roll.Second ?? 0, roll.Natural, modifier, recoveryDie, randomBefore, randomAfter, words)).ToArray();
            return null;
        }
    }
}
#endif
