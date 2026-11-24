#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedFrightened;

        internal TestOnlySharedWorldPolicy EnableConnectedFrightened(ClericInitialSelection initial, ClericRepertoireSelection repertoire)
        {
            EnableConnectedClericRepertoire(initial, repertoire);
            connectedFrightened = true;
            ContentFingerprint = FrightenedProfile.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                FrightenedProfile.SourceRevision, FrightenedProfile.CardSha256, FrightenedProfile.WarriorEngineSha256,
                FrightenedProfile.ConditionSha256, FrightenedProfile.Entitlement,
                "initial-defender-STR|visual-both-directions-and-effect|target-owned-end|recharge3|review-226d668a-fd32-51b3-b64c-bbd74b67e64c"));
            return this;
        }

        private void InitializeFrightened(Snapshot state)
        {
            if (!connectedFrightened) return;
            state.ConnectedFrightened = true;
            state.Conditions = state.Conditions.Select(x => new ConditionJournal(ConditionJournal.RelationshipPolicyId,
                x.Target, x.Origin, x.Operations)).ToArray();
            state.CharacterFeatureGrants = state.CharacterFeatureGrants.Append(new CharacterFeatureGrantRecord(
                FrightenedProfile.Actor, FrightenedProfile.SourceId, "Warrior", 2, "", 0,
                CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement)).ToArray();
            state.WarriorAbilityChoices = new[] { new WarriorAbilityChoiceRecord(FrightenedProfile.Actor,
                CharacterAbility.Strength, FrightenedProfile.SourceRevision, FrightenedProfile.Entitlement, 0) };
        }

        private string AssessIntimidatingPresence(Snapshot state, Command command)
            => IntimidatingPresenceConstraintV1(state, command)?.NativeCode;

        private NativeCommandConstraintV1 IntimidatingPresenceConstraintV1(Snapshot state, Command command)
        {
            if (!state.ConnectedFrightened || command.Actor != FrightenedProfile.Actor && !(state.PostRecoveryEncounter != null && command.Actor == PostRecoveryEncounterDefinition.Actor)) return new NativeCommandConstraintV1("IntimidatingPresenceUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 40);
            if (command.IntimidatingPresence == null) return new NativeCommandConstraintV1("InvalidIntimidatingPresenceRequest", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 41);
            bool recovery=command.Actor==PostRecoveryEncounterDefinition.Actor && PostRecoveryProfile.Active(state);
            if (!state.InventoryCombat || (!recovery && (command.Actor!=FrightenedProfile.Actor
                || state.Reinforcement?.Admission == null || state.Encounter?.Id != state.Reinforcement.Definition.EncounterId))) return new NativeCommandConstraintV1("IntimidatingPresenceContextUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 44);
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state)) return new NativeCommandConstraintV1("TacticalChoicePending", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 45);
            if (state.Encounter.CurrentActor != command.Actor || state.InventoryTurnActor != command.Actor) return new NativeCommandConstraintV1("WrongRegularTurn", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 46);
            if (!state.CharacterFeatureGrants.Any(x => x.ActorId==command.Actor && FrightenedProfile.ValidFixtureGrant(state, x))) return new NativeCommandConstraintV1("IntimidatingPresenceNotOwned", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 47);
            var choice = state.WarriorAbilityChoices.SingleOrDefault(x => x.ActorId == command.Actor);
            if (choice == null || state.Characters.Single(x => x.ActorId == command.Actor).Levels.Count(x => x.ClassName == "Warrior") < 2)
                return new NativeCommandConstraintV1("IntimidatingPresenceClassUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 50);
            if (!CapableWorker(state, command.Actor) || !Permissions(state, command.Actor).Action) return new NativeCommandConstraintV1("ConditionPreventsAction", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 51);
            if (Interval(state, command.Actor).ActionSpent) return new NativeCommandConstraintV1("ActionAlreadySpent", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 52);
            if (OrdinaryInventory.Busy(state, command.Actor) || state.WorldTraversals.Any(x => x.ActorId == command.Actor))
                return new NativeCommandConstraintV1("IntimidatingPresenceRequiresStationaryAccess", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 54);
            if (state.AbilityRecharges.Any(x => x.ActorId == command.Actor && x.AbilityId == FrightenedProfile.SourceId && x.Remaining > 0))
                return new NativeCommandConstraintV1("IntimidatingPresenceRecharging", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 56);
            if (state.FrightenedUses.Length >= 128 || state.FrightenedSaves.Length + 6 > 768 || state.FrightenedTimings.Length + 3 > 384)
                return new NativeCommandConstraintV1("IntimidatingPresenceHistoryFull", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 58);
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            foreach (string id in command.IntimidatingPresence.TargetIds) {
                if (id != TestOnlyPolicy.ActorId && id != TestOnlyPolicy.CompanionId || !state.Encounter.Order.Contains(id)
                    || state.Lives.Single(x => x.ActorId == id).Dead) return new NativeCommandConstraintV1("IntimidatingPresenceTargetUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 62);
                if (state.WorldTraversals.Any(x => x.ActorId == id)) return new NativeCommandConstraintV1("IntimidatingPresenceRequiresStationaryAccess", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 63);
                var target = state.Actors.Single(x => x.Id == id);
                if (PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X, actor.Y), new CombatCell(target.X, target.Y)) > 15
                    || !ObservationGeometry.LineOfEffectClear(state, actor.Id, target.Id)) return new NativeCommandConstraintV1("IntimidatingPresenceTargetUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 66);
                if (!ObservationRules.CanSee(state, target.Id, actor.Id))
                    return new NativeCommandConstraintV1("IntimidatingPresenceHearingTargetingUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 68);
                if (!ObservationRules.CanSee(state, actor.Id, target.Id))
                    return new NativeCommandConstraintV1("IntimidatingPresenceAlternativePerceptionUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 70);
                var journal = state.Conditions.Single(x => x.Target == id);
                var ledger = TestOnlyClubAttackPolicy.ConditionsFor(state, id);
                // Reserve application, synchronization, repeat and final-expiry operations before any payment or draw.
                if (journal.Operations.Count + 6 > ConditionJournal.MaxOperations || ledger.Applications.Count >= ConditionLedger.MaxApplications)
                    return new NativeCommandConstraintV1("IntimidatingPresenceConditionHistoryFull", "engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs", 75);
            }
            return null;
        }

        private CommandQueryResult QueryIntimidatingPresence(Snapshot state, Command command)
        {
            string failure = AssessIntimidatingPresence(state, command);
            return new CommandQueryResult(true, failure == null, failure ?? "Available", state.Revision,
                failure == null ? new[] { new CommandCost("action", "", 1) } : null);
        }

        private string ResolveIntimidatingPresence(Snapshot state, Command command)
        {
            string failure = AssessIntimidatingPresence(state, command);
            if (failure != null) return failure;
            var facts = CharacterRuleFacts.ForActor(state, command.Actor);
            var choice = state.WarriorAbilityChoices.Single(x => x.ActorId == command.Actor);
            int dc = checked(8 + facts.ProficiencyBonus + facts.AbilityModifier(choice.Ability));
            var epoch = WorldTiming.ForActor(state, command.Actor);
            long local = epoch.LatestStart(command.Actor, epoch.SlotAt(state.RuleClock));
            string useId = "fear.use." + (state.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var use = new FrightenedUseRecord(useId, command.Id, state.Revision + 1, command.Actor, FrightenedProfile.SourceId,
                FrightenedProfile.SourceRevision, epoch.Id, local, state.RuleClock, dc, command.IntimidatingPresence.TargetIds);
            SetInterval(state, Interval(state, command.Actor).PayAction());
            state.FrightenedUses = state.FrightenedUses.Append(use).ToArray();
            BreakSanctuaryForHostileSave(state,command.Actor,command.Id);
            state.AbilityRecharges = state.AbilityRecharges.Where(x=>x.ActorId!=command.Actor || x.AbilityId!=FrightenedProfile.SourceId)
                .Append(new CharacterAbilityRechargeRecord(command.Actor, FrightenedProfile.SourceId,
                    epoch.Id, local, epoch.Start(local), 3)).ToArray();
            foreach (string target in use.TargetIds) {
                var save = RollFrightenedSave(state, use, target, false, "");
                state.FrightenedSaves = state.FrightenedSaves.Append(save).ToArray();
                if (save.ApplicationId == "") continue;
                var targetEpoch = WorldTiming.ForActor(state, target);
                long end = FrightenedProfile.NextTargetEnd(targetEpoch, target, state.RuleClock);
                var repeat = new ConditionStamp(targetEpoch.Start(end + 1));
                var final = new ConditionStamp(repeat.Time.AddSeconds(6));
                state.FrightenedTimings = state.FrightenedTimings.Append(new FrightenedTimingRecord(save.ApplicationId,
                    use.Id, target, targetEpoch.Id, end, repeat, final)).ToArray();
                TestOnlyClubAttackPolicy.AppendCondition(state, target, ConditionOperation.Apply(save.ApplicationId,
                    new ConditionStamp(state.RuleClock), new ConditionApplicationData(save.ApplicationId, use.ActorId,
                        FrightenedProfile.SourceId, "Frightened", final, "source-repeat-or-final-end-or-qualified-cure", true, dc,
                        fear: new FrightenedRelationshipData(use.ActorId, use.Id, FrightenedProfile.SourceRevision))));
            }
            ReconcileTraversal(state); PauseIncompatibleWork(state);
            return null;
        }

        private static FrightenedSaveRecord RollFrightenedSave(Snapshot state, FrightenedUseRecord use, string target,
            bool repeat, string application)
        {
            int modifier = checked(ActorNumericFacts.ForActor(state, target).AbilityModifier(CharacterAbility.Wisdom)
                + CharacterAdvancementRules.SaveProficiencyBonus(state, target, "WIS")
                + ExpeditionStrainRules.Current(state, target).SavingThrowModifier);
            int basis=modifier;var aura=AuraOfFaithRules.Qualify(state,target);modifier=AuraOfFaithRules.Modifier(aura,basis);
            // The admitted WIS save has no automatic failure or advantage/disadvantage source.
            // Fear affects attacks and checks only; the ordinary shared RNG/save rules own this roll.
            uint before = state.RandomState;
            var roll = PlaytestDice.RollD20(before);
            bool success = roll.Natural + modifier >= use.Dc;
            bool prevented = !repeat && !success && TestOnlyClubAttackPolicy.ConditionsFor(state, target).ImmuneTo(ConditionKind.Frightened);
            if (!repeat) application = success || prevented ? "" : use.Id + "." + target;
            state.RandomState = roll.NextRandomState;
            string saveId=use.Id+".save."+target+(repeat?".repeat":".initial");
            AuraOfFaithRules.RecordSave(state,aura,AuraSaveConsumer.Frightened,saveId,basis,use.Dc,roll.Natural,false,success,before,roll.NextRandomState,roll.WordsConsumed);
            return new FrightenedSaveRecord(saveId, use.Id,
                target, application, state.Revision + 1, state.RuleClock, repeat, use.Dc, modifier, roll.First,
                roll.Second ?? 0, roll.Natural, success, prevented, before, roll.NextRandomState, roll.WordsConsumed);
        }

        private static RuleTime? NextFrightenedRepeatDeadline(Snapshot state)
        {
            if (!state.ConnectedFrightened) return null;
            var due = state.FrightenedTimings.Where(x => x.RepeatAt.Time > state.RuleClock
                && !state.FrightenedSaves.Any(y => y.Repeat && y.ApplicationId == x.ApplicationId)
                && TestOnlyClubAttackPolicy.ConditionsFor(state, x.TargetId).Applications.Any(y => y.Id == x.ApplicationId
                    && y.Present(new EffectClockMarker(state.RuleClock)))).Select(x => (RuleTime?)x.RepeatAt.Time);
            return due.OrderBy(x => x).FirstOrDefault();
        }

        internal static void ProcessFrightenedRepeatMarkers(Snapshot state)
        {
            if (!state.ConnectedFrightened) return;
            foreach (var timing in state.FrightenedTimings.Where(x => x.RepeatAt.Time == state.RuleClock)
                .OrderBy(x => x.ApplicationId, StringComparer.Ordinal)) {
                if (state.FrightenedSaves.Any(x => x.Repeat && x.ApplicationId == timing.ApplicationId)) continue;
                var ledger = TestOnlyClubAttackPolicy.ConditionsFor(state, timing.TargetId);
                if (!ledger.Applications.Any(x => x.Id == timing.ApplicationId && x.Present(ledger.Now))) continue;
                var use = state.FrightenedUses.Single(x => x.Id == timing.UseId);
                var save = RollFrightenedSave(state, use, timing.TargetId, true, timing.ApplicationId);
                state.FrightenedSaves = state.FrightenedSaves.Append(save).ToArray();
                if (save.Success) TestOnlyClubAttackPolicy.AppendCondition(state, timing.TargetId,
                    ConditionOperation.End(save.Id + ".end", new ConditionStamp(state.RuleClock), timing.ApplicationId, "source-repeat-success"));
            }
        }

        // Called only after ordinary duration/budget limits have bounded every active edge.
        // The result is a shared-clock boundary, never a snap, refund or forced-move label.
        private RuleTime BoundFrightenedTraversal(Snapshot state, RuleTime next, out string[] suspended)
        {
            suspended = Array.Empty<string>();
            if (!state.ConnectedFrightened || next <= state.RuleClock) return next;
            var elapsed = CampGreens.Subtract(next, state.RuleClock);
            var ends = new Dictionary<string, (RuleQuantity X, RuleQuantity Y)>(StringComparer.Ordinal);
            foreach (var edge in state.WorldTraversals.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                long multiplier = CostPerFoot(state, edge);
                var distance = edge.DistanceFeet + new RuleQuantity(elapsed.Numerator, elapsed.Denominator)
                    .Scale(checked(Speed(state, edge.ActorId) * (edge.Running ? 2 : 1)), 6 * multiplier);
                RuleQuantity Coordinate(int from, int to) => RuleQuantity.FromFraction(
                    (BigInteger)from * 5 * distance.Denominator + (BigInteger)Math.Sign(to - from) * distance.Numerator,
                    (BigInteger)5 * distance.Denominator);
                ends.Add(edge.ActorId, (Coordinate(edge.FromX, edge.ToX), Coordinate(edge.FromY, edge.ToY)));
            }
            var hits = new List<(string Actor, RuleQuantity Fraction)>();
            foreach (var pair in ends) {
                var start = WorldPositionResolver.Position(state, pair.Key);
                foreach (var fear in FrightenedRules.Operative(state, pair.Key)) {
                    string source = fear.Fear.FearedEntityId;
                    var sourceStart = WorldPositionResolver.Position(state, source);
                    var sourceEnd = ends.TryGetValue(source, out var moving) ? moving : sourceStart;
                    var fraction = FrightenedMovementRules.FirstProhibitedFraction(start, pair.Value, sourceStart, sourceEnd);
                    if (fraction.HasValue) hits.Add((pair.Key, fraction.Value));
                }
            }
            if (hits.Count == 0) return next;
            var first = hits.Min(x => x.Fraction);
            suspended = hits.Where(x => x.Fraction == first).Select(x => x.Actor).Distinct(StringComparer.Ordinal).ToArray();
            var duration = new RuleQuantity(elapsed.Numerator, elapsed.Denominator).Scale(first.Numerator, first.Denominator);
            return CampGreens.Add(state.RuleClock, new RuleTime(duration.Numerator, duration.Denominator));
        }

        private void ReconcileFrightenedTraversal(Snapshot state)
        {
            if (!state.ConnectedFrightened) return;
            while (true) {
                var moving = state.WorldTraversals.Where(x => x.Status == WorldTraversalStatus.Moving).ToArray();
                if (moving.Length == 0) return;
                RuleTime horizon = state.RuleClock.AddSeconds(1);
                foreach (var edge in moving) {
                    var duration = (new RuleQuantity(5) - edge.DistanceFeet).Scale(6 * CostPerFoot(state, edge),
                        checked(Speed(state, edge.ActorId) * (edge.Running ? 2 : 1)));
                    var end = CampGreens.Add(state.RuleClock, new RuleTime(duration.Numerator, duration.Denominator));
                    if (end < horizon) horizon = end;
                }
                if (BoundFrightenedTraversal(state, horizon, out var actors) != state.RuleClock) return;
                foreach (string actor in actors) {
                    var edge = state.WorldTraversals.Single(x => x.ActorId == actor);
                    SetEdge(state, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
                }
            }
        }
    }
}
#endif
