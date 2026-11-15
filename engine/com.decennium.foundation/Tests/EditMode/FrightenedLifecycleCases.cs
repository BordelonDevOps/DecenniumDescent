#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewFrightenedExpedition() => ConnectedExpeditionSession.StartWithFrightened(
            ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample());

        private static ConnectedExpeditionSession FrightenedArrival()
        {
            var session = StartVialScenario(NewFrightenedExpedition());
            const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
            ClericCommit(session, ally, CommandKind.BeginWorldStep, "walk", -1);
            ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6, y: 1);
            ClericCommit(session, hero, CommandKind.BeginWorldStep, "walk", -1);
            ClericCommit(session, hero, CommandKind.AdvanceClock, x: 12, y: 1);
            ClericCommit(session, ally, CommandKind.BeginReinforcementApproach, "TEST_ONLY.companion-reinforcement.v1");
            ClericGuard(session, hero);
            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 2);
            ClericDefender(session); ClericEnd(session, hero); ClericDefender(session);
            Require(ShortRestCapture(session).Reinforcement.Admission != null, "Fear route requires actual companion admission.");
            ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 1);
            ClericDefender(session); ClericEnd(session, hero); ClericDefender(session);
            return session;
        }

        // These altered candidates exercise the same source preflight/producer components.
        // They are deliberately detached controls, never claimed as reachable gameplay saves.
        private static void FrightenedDetachedSourceControls(TestOnlySharedWorldPolicy policy, Snapshot ready)
        {
            const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
            var command = new Command("fear.detached.preflight", FrightenedProfile.Actor, ready.Revision,
                CommandKind.UseIntimidatingPresence, intimidatingPresence: new IntimidatingPresenceRequest(new[] { hero, ally }));
            object Fields(object value, int depth = 0) {
                if (value == null) return null;
                Require(depth < 80, "Detached candidate field capture encountered a cycle.");
                var type = value.GetType();
                if (type.IsPrimitive || type.IsEnum || value is string || value is decimal) return value;
                if (value is System.Collections.IEnumerable sequence)
                    return sequence.Cast<object>().Select(x => Fields(x, depth + 1)).ToArray();
                var fields = new SortedDictionary<string, object>(StringComparer.Ordinal) { { "$type", type.FullName } };
                foreach (var field in type.GetFields(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
                    fields.Add(field.Name, Fields(field.GetValue(value), depth + 1));
                return fields;
            }
            // Capture every stored field without calling legacy integer projections that
            // intentionally throw on fractional quantities. Invalid detached candidates
            // cannot be passed through SnapshotCodec's authoritative validation gate.
            string Raw(Snapshot value) => System.Text.Json.JsonSerializer.Serialize(Fields(value));
            void Reject(Snapshot candidate, string code, Command selected = null) {
                string before = Raw(candidate);
                Require(policy.Resolve(candidate, selected ?? command) == code && before == Raw(candidate),
                    "Detached preflight changed full candidate state or returned the wrong diagnostic: " + code);
            }
            Snapshot WithCondition(string actor, string kind) {
                var candidate = ready.Copy();
                var journal = candidate.Conditions.Single(x => x.Target == actor);
                var history = ConditionHistory.Restore(journal).Append(ConditionOperation.Advance("detached.sync",
                    new ConditionStamp(candidate.RuleClock))).State.Append(ConditionOperation.Apply("detached.blind",
                    new ConditionStamp(candidate.RuleClock), new ConditionApplicationData("detached.blind", "TEST_ONLY.detached",
                        "TEST_ONLY.detached-preflight", kind, new ConditionStamp(candidate.RuleClock.AddSeconds(6)), "expiry", true))).State;
                candidate.Conditions = candidate.Conditions.Select(x => x.Target == actor ? history.Journal : x).ToArray();
                return candidate;
            }
            Reject(WithCondition(hero, "Blinded"), "IntimidatingPresenceHearingTargetingUnsupported");
            Reject(WithCondition(FrightenedProfile.Actor, "Blinded"), "IntimidatingPresenceAlternativePerceptionUnsupported");
            Reject(ready.Copy(), "IntimidatingPresenceTargetUnavailable", new Command("fear.detached.bad-target",
                FrightenedProfile.Actor, ready.Revision, CommandKind.UseIntimidatingPresence,
                intimidatingPresence: new IntimidatingPresenceRequest(new[] { hero, "zz.unsupported-target" })));
            var absent = ready.Copy(); absent.CharacterFeatureGrants = absent.CharacterFeatureGrants
                .Where(x => x.FeatureId != FrightenedProfile.SourceId).ToArray();
            Reject(absent, "IntimidatingPresenceNotOwned");
            absent = ready.Copy(); absent.WarriorAbilityChoices = Array.Empty<WarriorAbilityChoiceRecord>();
            Reject(absent, "IntimidatingPresenceClassUnavailable");
            var spent = ready.Copy(); spent.WorldIntervals = spent.WorldIntervals.Select(x => x.ActorId == FrightenedProfile.Actor
                ? x.PayAction() : x).ToArray();
            Reject(spent, "ActionAlreadySpent");
            var recharging = ready.Copy(); var cursor = recharging.AbilityRecharges.Single();
            recharging.AbilityRecharges = new[] { new CharacterAbilityRechargeRecord(cursor.ActorId, cursor.AbilityId,
                cursor.EpochId, cursor.LastLocalStart, cursor.LastStartAt, 1) };
            Reject(recharging, "IntimidatingPresenceRecharging");

            var immune = ready.Copy(); var originalJournal = immune.Conditions.Single(x => x.Target == hero);
            var ward = ConditionHistory.Restore(originalJournal).Append(ConditionOperation.Advance("detached.sync",
                new ConditionStamp(immune.RuleClock))).State.Append(ConditionOperation.Grant("detached.ward",
                new ConditionStamp(immune.RuleClock), new ConditionImmunityData("detached.ward", "TEST_ONLY.detached",
                    "TEST_ONLY.detached-immunity", new[] { "Frightened" }, null, "source-end", allowRelationships: true))).State;
            immune.Conditions = immune.Conditions.Select(x => x.Target == hero ? ward.Journal : x).ToArray();
            int priorSaves = immune.FrightenedSaves.Length;
            var first = PlaytestDice.RollD20(immune.RandomState);
            var second = PlaytestDice.RollD20(first.NextRandomState);
            Require(policy.Resolve(immune, command) == null, "Detached source invocation with an immune target must still be legal.");
            var saves = immune.FrightenedSaves.Skip(priorSaves).ToArray();
            Require(saves.Length == 2 && saves[0].TargetId == hero && !saves[0].Success && saves[0].AdmissionPrevented
                && saves[0].ApplicationId == "" && saves[0].Natural == first.Natural && saves[1].Natural == second.Natural
                && immune.RandomState == second.NextRandomState && immune.AbilityRecharges.Single().Remaining == 3
                && immune.WorldIntervals.Single(x => x.ActorId == FrightenedProfile.Actor).ActionSpent
                && !immune.FrightenedTimings.Any(x => x.TargetId == hero),
                "Named immunity must follow the canonical initial saves, prevent admission, and retain payment and recharge.");
        }

        private static void FrightenedDetachedSuppressedRepeat(Snapshot applied)
        {
            var timing = applied.FrightenedTimings.OrderBy(x => x.RepeatAt.Time).First();
            var ordinary = applied.Copy(); ordinary.RuleClock = timing.RepeatAt.Time;
            var suppressed = ordinary.Copy();
            var journal = suppressed.Conditions.Single(x => x.Target == timing.TargetId);
            var history = ConditionHistory.Restore(journal).Append(ConditionOperation.Suppress("detached.suppress-repeat",
                journal.Now, timing.ApplicationId, true)).State;
            suppressed.Conditions = suppressed.Conditions.Select(x => x.Target == timing.TargetId ? history.Journal : x).ToArray();
            var process = typeof(TestOnlySharedWorldPolicy).GetMethod("ProcessFrightenedRepeatMarkers", BindingFlags.Static | BindingFlags.NonPublic);
            process.Invoke(null, new object[] { ordinary }); process.Invoke(null, new object[] { suppressed });
            var a = ordinary.FrightenedSaves.Last(); var b = suppressed.FrightenedSaves.Last();
            Require(a.Repeat && b.Repeat && a.ApplicationId == timing.ApplicationId && b.ApplicationId == a.ApplicationId
                && a.Natural == b.Natural && a.Success == b.Success && a.RandomBefore == b.RandomBefore
                && a.RandomAfter == b.RandomAfter && a.Second == 0 && b.Second == 0 && ordinary.RandomState == suppressed.RandomState,
                "Explicit suppression must neither skip the due source save nor impose fear disadvantage on it.");
        }

        private static void AddFrightenedLifecycleCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac05_frightened_connected_paid_ability_check", () => {
                var session = FrightenedArrival(); var codec = new SnapshotCodec();
                const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
                for (int reuse = 0; reuse < 2; reuse++) {
                    for (int round = 0; round < 3; round++) {
                        ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
                        if (reuse == 1 && round == 2) {
                            var toolsState = ShortRestCapture(session);
                            if (!toolsState.PortableEquipment.Single(x => x.Id == PortableKitFixture.Pack).Open)
                                ClericCommit(session, hero, CommandKind.OpenPortableContainer, PortableKitFixture.Pack);
                            long revision = session.View(ExpeditionSeat.Player).Revision;
                            CommitVialRoute(session, new Command("fear.tools." + revision, hero, revision,
                                CommandKind.HandlePortableEquipment, PortableKitFixture.Tools,
                                inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Retrieve)));
                            Require(ShortRestCapture(session).SupplyCacheEquipment.Single(x => x.Id == PortableKitFixture.Tools).LocationId == hero,
                                "The affected check requires actual paid physical tool retrieval.");
                            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 2);
                        }
                        ClericEnd(session, hero);
                        if (round < 2) ClericDefender(session);
                    }
                    var ready = ShortRestCapture(session);
                    if (reuse == 1) FrightenedDetachedSourceControls(ClericPolicy(session), ready);
                    Require(session.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(),
                        new Command("fear.check.reuse." + reuse, FrightenedProfile.Actor, ready.Revision, CommandKind.UseIntimidatingPresence,
                            intimidatingPresence: new IntimidatingPresenceRequest(new[] { hero, ally }))).Response == ExpeditionResponse.Committed,
                        "Real recharged source use did not commit.");
                    ClericDefender(session);
                }
                ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
                var before = ShortRestCapture(session);
                Require(TestOnlyClubAttackPolicy.ConditionsFor(before, hero).View().Has(ConditionKind.Frightened)
                    && ObservationRules.CanSee(before, hero, FrightenedProfile.Actor) && before.SupplyCaches.Single().Locked,
                    "Real check requires visible active fear and the untouched locked cache.");
                string path = Path.Combine(directory, "frightened-before-ability-check.ddsave"); session.Save(path);
                session = NewFrightenedExpedition(); session.Restore(path);
                Require(codec.Encode(before).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Check checkpoint changed on restore.");
                var expected = PlaytestDice.RollD20(before.RandomState, disadvantageSources: 1);
                ClericCommit(session, hero, CommandKind.Interact, SupplyCacheFixture.CacheId, (int)SupplyCacheInteraction.PickWithTools);
                var after = ShortRestCapture(session); var attempt = after.SupplyCacheAttempts.Single();
                Require(expected.Second.HasValue && expected.Natural == Math.Min(expected.First, expected.Second.Value)
                    && attempt.Tactical && !attempt.AutomaticFailure && attempt.Natural == expected.Natural
                    && after.RandomState == expected.NextRandomState && after.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent,
                    "Real frightened ability check must consume both shared dice, select disadvantage and pay its Action.");
                session.Save(Path.Combine(directory, "frightened-affected-ability-check.ddsave"));
                ClericEnd(session, hero);
                var repeated = ShortRestCapture(session);
                var repeat = repeated.FrightenedSaves.Single(x => x.TargetId == hero && x.Repeat);
                var timing = repeated.FrightenedTimings.Single(x => x.TargetId == hero);
                Require(!repeat.Success && repeat.Second == 0 && repeat.At == timing.RepeatAt.Time
                    && TestOnlyClubAttackPolicy.ConditionsFor(repeated, hero).View().Has(ConditionKind.Frightened),
                    "Actual second failure must continue the same fear with an ordinary single-die save.");
                session.Save(Path.Combine(directory, "frightened-ability-check-repeat.ddsave"));
                ClericDefender(session); ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
                var lastTurn = ShortRestCapture(session);
                Require(lastTurn.RuleClock < timing.FinalAt.Time
                    && TestOnlyClubAttackPolicy.ConditionsFor(lastTurn, hero).View().Has(ConditionKind.Frightened),
                    "The continued application ended before its final source endpoint.");
                session.Save(Path.Combine(directory, "frightened-before-final-expiry.ddsave"));
                ClericEnd(session, hero);
                var expired = ShortRestCapture(session);
                Require(expired.RuleClock == timing.FinalAt.Time && expired.RandomState == lastTurn.RandomState
                    && expired.FrightenedSaves.Length == repeated.FrightenedSaves.Length
                    && !TestOnlyClubAttackPolicy.ConditionsFor(expired, hero).View().Has(ConditionKind.Frightened),
                    "Final expiry must happen exactly six seconds later without a third save or RNG draw.");
                session.Save(Path.Combine(directory, "frightened-final-expiry.ddsave"));

                // A genuine alternate branch reaches the authored sight blocker using paid
                // tactical movement and the actual defender's opportunity decision.
                var unseen = NewFrightenedExpedition(); unseen.Restore(path);
                ClericCommit(unseen, hero, CommandKind.TacticalStep, unseen.View(ExpeditionSeat.Player).TurnId, 1, 1);
                ClericDefender(unseen);
                ClericCommit(unseen, hero, CommandKind.TacticalStep, unseen.View(ExpeditionSeat.Player).TurnId, 2, 0);
                ClericDefender(unseen);
                var obscured = ShortRestCapture(unseen);
                Require(!ObservationRules.CanSee(obscured, hero, FrightenedProfile.Actor)
                    && TestOnlyClubAttackPolicy.ConditionsFor(obscured, hero).View().Has(ConditionKind.Frightened),
                    "Sight loss must use the real blocker without ending the relationship.");
                unseen.Save(Path.Combine(directory, "frightened-sight-lost.ddsave"));
                var step = new Command("fear.unseen.approach", hero, obscured.Revision, CommandKind.TacticalStep,
                    unseen.View(ExpeditionSeat.Player).TurnId, 1, 1);
                Require(ClericPolicy(unseen).Resolve(obscured.Copy(), step) == "FrightenedPreventsWillingApproach"
                    && unseen.Submit(ExpeditionSeat.Player, step).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(obscured).SequenceEqual(codec.Encode(ShortRestCapture(unseen))),
                    "Unseen fear must still prohibit an otherwise walkable closer step without payment or RNG.");
                unseen.Save(Path.Combine(directory, "frightened-unseen-approach-denied.ddsave"));
                ClericCommit(unseen, hero, CommandKind.Hide, unseen.View(ExpeditionSeat.Player).TurnId);
                var hidden = ShortRestCapture(unseen); var hide = hidden.ObservationActions.Last();
                Require(hide.WordsConsumed == 1 && hide.Second == 0 && hide.Natural != 0
                    && hidden.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent,
                    "An actual check with the source unseen must use one die and pay its Action.");
                string hiddenPath = Path.Combine(directory, "frightened-unseen-hide-check.ddsave"); unseen.Save(hiddenPath);
                var unseenRestored = NewFrightenedExpedition(); unseenRestored.Restore(hiddenPath);
                Require(codec.Encode(hidden).SequenceEqual(codec.Encode(ShortRestCapture(unseenRestored))),
                    "Historical unseen-source check did not restore exactly.");
            });
            cases.Add("tac05_frightened_qualified_named_cure_component_authority", () => {
                var assembly = typeof(TestOnlySharedWorldPolicy).Assembly;
                var contextType = assembly.GetType("Decennium.Foundation.Laboratory.ConditionCureInvocation", true);
                var settleType = assembly.GetType("Decennium.Foundation.Laboratory.SourceQualifiedConditionCure", true);
                var factory = contextType.GetMethod("ForDetachedTest", BindingFlags.Static | BindingFlags.NonPublic);
                var settle = settleType.GetMethod("Settle", BindingFlags.Static | BindingFlags.NonPublic);
                Require(!contextType.IsPublic && !settleType.IsPublic
                    && !Enum.GetNames(typeof(CommandKind)).Contains("CureFrightened"), "Generic cure must not become a public gameplay command.");
                object Context(string target = "target", string authority = "TEST_ONLY.detached-condition-cure.v1",
                    string source = "TEST_ONLY.cure-source", ConditionStamp at = default) => factory.Invoke(null, new object[] {
                        authority, "TEST_ONLY.cure-invocation", source, "TEST_ONLY.source-revision", "healer", target, at,
                        new[] { ConditionKind.Frightened, ConditionKind.Poisoned } });
                var history = new ConditionHistory("target", relationships: true);
                foreach (string id in new[] { "eligible", "suppressed", "protected" }) {
                    history = history.Append(ConditionOperation.Apply("apply." + id, default,
                        new ConditionApplicationData(id, "owner", "TEST_ONLY.fear", "Frightened", new ConditionStamp(new RuleTime(12)),
                            "expiry", id != "protected", fear: new FrightenedRelationshipData("source-actor", "use." + id, "TEST_ONLY.source")))).State;
                }
                history = history.Append(ConditionOperation.Suppress("suppress", default, "suppressed", true)).State;
                history = history.Append(ConditionOperation.Apply("apply.poison", default,
                    new ConditionApplicationData("poison", "owner", "TEST_ONLY.poison", "Poisoned", null, "qualified-cure", true))).State;
                var codec = new ConditionJournalCodec(); var before = codec.Encode(history.Journal);
                object Invoke(ConditionHistory state, object context, string target = "target", ConditionKind kind = ConditionKind.Frightened)
                    => settle.Invoke(null, new[] { (object)state, context, target, kind });
                Throws<TargetInvocationException>(() => Context(authority: "unqualified"));
                Throws<TargetInvocationException>(() => Context(source: "cleric.base.radiance.radiance"));
                Throws<TargetInvocationException>(() => Invoke(history, Context("wrong")));
                Throws<TargetInvocationException>(() => Invoke(history, Context(), "wrong"));
                Throws<TargetInvocationException>(() => Invoke(history, Context(at: new ConditionStamp(new RuleTime(1)))));
                Throws<TargetInvocationException>(() => Invoke(history, Context(), kind: ConditionKind.Blinded));
                Require(before.SequenceEqual(codec.Encode(history.Journal)), "Invalid invocation changed the target history.");
                object result = Invoke(history, Context());
                var type = result.GetType();
                var transition = (ConditionHistoryTransition)type.GetProperty("Transition", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(result);
                var ended = (IEnumerable<string>)type.GetProperty("EndedApplications", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(result);
                Require(ended.SequenceEqual(new[] { "eligible", "suppressed" })
                    && transition.State.Ledger.View().Sources(ConditionKind.Frightened).SequenceEqual(new[] { "protected" })
                    && transition.State.Ledger.View().Has(ConditionKind.Poisoned),
                    "Qualified named cure missed suppressed eligible effects or removed protected/unrelated effects.");
                var restored = ConditionHistory.Restore(codec.Decode(codec.Encode(transition.State.Journal)));
                Throws<TargetInvocationException>(() => Invoke(restored, Context()));
                Require(before.SequenceEqual(codec.Encode(history.Journal)) && restored.Journal.SameAs(transition.State.Journal),
                    "Pure settlement mutated its input or replay lost the complete eligible set.");
            });
            cases.Add("tac05_frightened_connected_activation_restore_and_recharge", () => {
                var session = FrightenedArrival(); var state = ShortRestCapture(session); var codec = new SnapshotCodec();
                var use = state.FrightenedUses.Single();
                Require(use.Dc == 10 && use.TargetIds.Count > 0 && state.FrightenedSaves.Count(x => !x.Repeat) == use.TargetIds.Count
                    && state.FrightenedTimings.Length == 0 && state.FrightenedSaves.All(x => x.Success) && state.AlchemyDoses.Length == 6
                    && state.ResonancePools.Single().Current == 3, "Actual first use must preserve its successful saves and real prepared resources.");
                string path = Path.Combine(directory, "frightened-after-use.ddsave");
                session.Save(path); session = NewFrightenedExpedition(); session.Restore(path);
                Require(codec.Encode(state).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Fear save did not restore byte-identically.");
                const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
                for (int reuse = 0; reuse < 2; reuse++) {
                    for (int round = 0; round < 3; round++) {
                        ClericGuard(session, ally); ClericEnd(session, ally);
                        ClericGuard(session, hero);
                        if (reuse == 1 && round == 2) {
                            session.Save(Path.Combine(directory, "frightened-before-last-approach.ddsave"));
                            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 2);
                        }
                        ClericEnd(session, hero);
                        var start = ShortRestCapture(session);
                        Require(start.AbilityRecharges.Single().Remaining == 2 - round, "Recharge did not count each actual owner Start once.");
                        if (round < 2) ClericDefender(session);
                    }
                    var ready = ShortRestCapture(session);
                    var command = new Command("fear.reuse." + reuse, FrightenedProfile.Actor, ready.Revision, CommandKind.UseIntimidatingPresence,
                        intimidatingPresence: new IntimidatingPresenceRequest(new[] { hero, ally }));
                    Require(session.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(), command).Response
                        == ExpeditionResponse.Committed, "Actual recharged use failed.");
                    var paidBytes = codec.Encode(ShortRestCapture(session));
                    Require(session.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(), command).Response
                        == ExpeditionResponse.Duplicate && paidBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                        "Repeated source delivery consumed more Action or RNG.");
                    if (reuse == 0) ClericDefender(session);
                }
                var applied = ShortRestCapture(session);
                FrightenedDetachedSuppressedRepeat(applied);
                Require(applied.FrightenedUses.Length == 3 && applied.FrightenedTimings.Length == 2
                    && applied.FrightenedSaves.Skip(4).All(x => !x.Success && x.ApplicationId != ""),
                    "Third actual use must produce two independent fear applications after earlier per-use successes.");
                var forgery = applied.Copy(); forgery.FrightenedTimings = Array.Empty<FrightenedTimingRecord>();
                Throws<ArgumentException>(() => codec.Encode(forgery));
                forgery = applied.Copy(); forgery.AbilityRecharges = Array.Empty<CharacterAbilityRechargeRecord>();
                Throws<ArgumentException>(() => codec.Encode(forgery));
                forgery = applied.Copy(); var cursor = forgery.AbilityRecharges.Single();
                forgery.AbilityRecharges = new[] { new CharacterAbilityRechargeRecord(cursor.ActorId, cursor.AbilityId,
                    cursor.EpochId, cursor.LastLocalStart, cursor.LastStartAt, 0) };
                Throws<ArgumentException>(() => codec.Encode(forgery));
                forgery = applied.Copy(); var save = forgery.FrightenedSaves.Last();
                forgery.FrightenedSaves[forgery.FrightenedSaves.Length - 1] = new FrightenedSaveRecord(save.Id, save.UseId,
                    save.TargetId, save.ApplicationId, save.Revision, save.At, save.Repeat, save.Dc, save.Modifier,
                    save.First, save.Second, save.Natural, save.Success, save.AdmissionPrevented,
                    save.RandomBefore == 1 ? 2u : 1u, save.RandomAfter, save.WordsConsumed);
                Throws<ArgumentException>(() => codec.Encode(forgery));
                path = Path.Combine(directory, "frightened-active.ddsave"); session.Save(path);
                session = NewFrightenedExpedition(); session.Restore(path);
                Require(codec.Encode(applied).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Active relationships changed on restore.");
                ClericDefender(session);
                for (int round = 0; round < 3; round++) {
                    ClericGuard(session, ally); ClericEnd(session, ally);
                    ClericGuard(session, hero);
                    if (round == 0) {
                        var beforeAttack = ShortRestCapture(session);
                        Require(TestOnlyClubAttackPolicy.ConditionsFor(beforeAttack, hero).View().Has(ConditionKind.Frightened)
                            && ObservationRules.CanSee(beforeAttack, hero, FrightenedProfile.Actor), "Attack witness requires actual visible fear.");
                        ClericCommit(session, hero, CommandKind.AttackClub, FrightenedProfile.Actor,
                            combat: new CombatRequest(session.View(ExpeditionSeat.Player).TurnId, "TEST_ONLY.actor-club"));
                        var attacked = ShortRestCapture(session); var roll = attacked.MeleeAttacks.Last().Attack;
                        Require(roll.Second != 0 && roll.Selected == Math.Min(roll.First, roll.Second)
                            && attacked.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent,
                            "Affected actual attack must pay Action and select the lower of two shared dice.");
                        session.Save(Path.Combine(directory, "frightened-affected-attack.ddsave"));
                    }
                    ClericEnd(session, hero); ClericDefender(session);
                }
                var ended = ShortRestCapture(session);
                Require(ended.AbilityRecharges.Single().Remaining == 0 && ended.FrightenedUses.Length == 3
                    && ended.FrightenedSaves.Count(x => x.Repeat) == applied.FrightenedTimings.Length
                    && ended.Conditions.Where(x => use.TargetIds.Contains(x.Target)).All(x => !ConditionHistory.Restore(x).Ledger.View().Has(ConditionKind.Frightened)),
                    "Actual own starts must recharge once and the source must resolve one repeat and final ending.");
                session.Save(Path.Combine(directory, "frightened-after-recharge.ddsave"));
                for (int round = 0; ; round++) {
                    Require(round < 24, "Fear route's real later fight did not conclude.");
                    ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
                    if (!ShortRestCapture(session).Lives.Single(x => x.ActorId == FrightenedProfile.Actor).Dead)
                        ClericCommit(session, hero, CommandKind.AttackClub, FrightenedProfile.Actor,
                            combat: new CombatRequest(session.View(ExpeditionSeat.Player).TurnId, "TEST_ONLY.actor-club"));
                    if (ShortRestCapture(session).Lives.Single(x => x.ActorId == FrightenedProfile.Actor).Dead) break;
                    ClericEnd(session, hero); ClericDefender(session);
                }
                ClericCommit(session, hero, CommandKind.EndFixedEncounter, session.View(ExpeditionSeat.Player).TurnId);
                var closed = ShortRestCapture(session);
                Require(!closed.InventoryCombat && closed.Encounter == null && closed.ClosedEncounters.Length == 2
                    && closed.Lives.Single(x => x.ActorId == FrightenedProfile.Actor).Dead && closed.AlchemyDoses.Length == 6,
                    "Source encounter must close through actual combat while retaining earlier acquisition and preparation.");
                session.Save(Path.Combine(directory, "frightened-closed.ddsave"));
                ClericCommit(session, hero, CommandKind.BeginWorldStep, "walk", y: -1);
                ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6, y: 1);
                var continued = ShortRestCapture(session);
                Require(continued.RuleClock == closed.RuleClock.AddSeconds(6)
                    && continued.Actors.Single(x => x.Id == hero).Y == closed.Actors.Single(x => x.Id == hero).Y - 1
                    && continued.FrightenedUses.Length == 3 && continued.AlchemyDoses.Length == 6
                    && continued.ResonancePools.Single().Current == 3,
                    "Normal closure must retain source, class, resource and acquisition history into paid exploration.");
                session.Save(Path.Combine(directory, "frightened-continued.ddsave"));

                // Genuine alternate continuation: retain the earlier farther position instead of taking the legal pre-fear step.
                var farther = NewFrightenedExpedition(); farther.Restore(Path.Combine(directory, "frightened-before-last-approach.ddsave"));
                ClericEnd(farther, hero);
                var beforeUse = ShortRestCapture(farther);
                var apply = new Command("fear.farther.use", FrightenedProfile.Actor, beforeUse.Revision, CommandKind.UseIntimidatingPresence,
                    intimidatingPresence: new IntimidatingPresenceRequest(new[] { hero, ally }));
                Require(farther.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(), apply).Response
                    == ExpeditionResponse.Committed, "Farther branch use failed.");
                ClericDefender(farther); ClericGuard(farther, ally); ClericEnd(farther, ally); ClericGuard(farther, hero);
                var beforeStep = ShortRestCapture(farther); var unchanged = codec.Encode(beforeStep);
                var step = new Command("fear.denied-approach", hero, beforeStep.Revision, CommandKind.TacticalStep,
                    beforeStep.Encounter.CurrentTurnId, y: 2);
                Require(ClericPolicy(farther).Resolve(beforeStep.Copy(), step) == "FrightenedPreventsWillingApproach"
                    && farther.Submit(ExpeditionSeat.Player, step).Response == ExpeditionResponse.Unavailable
                    && unchanged.SequenceEqual(codec.Encode(ShortRestCapture(farther))),
                    "Fear must reject the previously legal closer step without payment, movement or RNG.");
                farther.Save(Path.Combine(directory, "frightened-denied-approach.ddsave"));
            });
            cases.Add("tac05_frightened_initial_source_profile_and_legacy_isolation", () => {
                var session = ConnectedExpeditionSession.StartWithFrightened(ClericInitialSelection.AuthoredExample(),
                    ClericRepertoireSelection.AuthoredExample());
                var state = ShortRestCapture(session); var codec = new SnapshotCodec();
                Require(state.WireSchemaVersion == 107 && state.SchemaVersion == 90 && state.ConnectedFrightened
                    && state.ConnectedClericRepertoire && state.KnownSpells.Length == 5 && state.ResonancePools.Single().Current == 3
                    && state.CharacterFeatureGrants.Count(x => FrightenedProfile.ValidFixtureGrant(state, x)) == 1
                    && state.WarriorAbilityChoices.Single().Ability == CharacterAbility.Strength
                    && state.FrightenedUses.Length == 0 && state.AbilityRecharges.Length == 0,
                    "Initial fear profile must preserve Cleric ownership and add only its source-qualified defender entitlement.");
                var bytes = codec.Encode(state);
                Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))), "Initial wire107 bytes changed on decode.");
                var old = ShortRestCapture(NewRepertoireExpedition()); var oldBytes = codec.Encode(old);
                Require(old.WireSchemaVersion == 106 && old.Conditions.All(x => x.PolicyId == ConditionHistory.PolicyId)
                    && oldBytes.SequenceEqual(codec.Encode(codec.Decode(oldBytes))), "Legacy repertoire profile changed.");
                var command = new Command("fear.early", FrightenedProfile.Actor, state.Revision, CommandKind.UseIntimidatingPresence,
                    intimidatingPresence: new IntimidatingPresenceRequest(new[] { ConnectedExpeditionSession.Hero }));
                Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.NotAuthorized
                    && session.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(), command).Response == ExpeditionResponse.Unavailable
                    && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Early use or player control must reject unchanged.");
            });
            cases.Add("tac05_frightened_typed_request_and_receipt_identity", () => {
                var targets = new[] { "target.b", "target.a" };
                var request = new IntimidatingPresenceRequest(targets);
                targets[0] = "changed";
                Require(request.TargetIds.SequenceEqual(new[] { "target.a", "target.b" }),
                    "Target selection retained caller order or mutable storage.");
                Throws<NotSupportedException>(() => ((IList<string>)request.TargetIds)[0] = "changed");
                Throws<ArgumentException>(() => new IntimidatingPresenceRequest(Array.Empty<string>()));
                Throws<ArgumentException>(() => new IntimidatingPresenceRequest(new[] { "a", "a" }));
                Throws<ArgumentException>(() => new IntimidatingPresenceRequest(new[] { "a", "b", "c", "d" }));
                Throws<ArgumentException>(() => new IntimidatingPresenceRequest(new[] { "bad target" }));
                string prefix = ((int)CommandKind.UseIntimidatingPresence).ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + "|actor||0|0|0";
                var receipt = new CommandReceipt { Principal = "TEST_ONLY.host", Id = "use", Revision = 1,
                    Fingerprint = prefix + "|intimidating-presence-v1|target.a,target.b" };
                var command = CommandHistory.Read(receipt);
                Require(command.Kind == CommandKind.UseIntimidatingPresence && command.MatchesReceipt(receipt)
                    && command.IntimidatingPresence.TargetIds.SequenceEqual(request.TargetIds), "Typed fear receipt did not reconstruct exactly.");
                var reordered = receipt.Copy(); reordered.Fingerprint = prefix + "|intimidating-presence-v1|target.b,target.a";
                Throws<ArgumentException>(() => CommandHistory.Read(reordered));
                var missing = receipt.Copy(); missing.Fingerprint = prefix;
                Throws<ArgumentException>(() => CommandHistory.Read(missing));
                var wrongKind = receipt.Copy(); wrongKind.Fingerprint = "0|actor||0|0|0|intimidating-presence-v1|target.a,target.b";
                Throws<ArgumentException>(() => CommandHistory.Read(wrongKind));
                var malformed = receipt.Copy(); malformed.Fingerprint = prefix + "|intimidating-presence-v1|target.a,target.a";
                Throws<ArgumentException>(() => CommandHistory.Read(malformed));
            });
            cases.Add("tac05_frightened_exact_willing_displacement_attribution", () => {
                (RuleQuantity X, RuleQuantity Y) P(long x, long y) => (new RuleQuantity(x), new RuleQuantity(y));
                RuleQuantity? First((RuleQuantity X, RuleQuantity Y) a, (RuleQuantity X, RuleQuantity Y) b,
                    (RuleQuantity X, RuleQuantity Y) s, (RuleQuantity X, RuleQuantity Y) t)
                    => FrightenedMovementRules.FirstProhibitedFraction(a, b, s, t);
                Require(First(P(7,5), P(6,5), P(5,5), P(5,5)) == default(RuleQuantity), "Ordinary approach admitted.");
                Require(First(P(7,5), P(8,5), P(5,5), P(5,5)) == null, "Retreat rejected.");
                Require(First(P(6,6), P(5,6), P(5,5), P(5,5)) == null, "Equal Chebyshev distance rejected.");
                Require(First(P(4,5), P(8,5), P(5,5), P(5,5)) == default(RuleQuantity),
                    "Farther endpoint concealed an initially approaching path.");
                Require(First(P(7,5), P(7,5), P(5,5), P(9,5)) == null,
                    "Source crossing attributed displacement to stationary target.");
                Require(First(P(7,5), P(8,5), P(5,5), P(7,5)) == null,
                    "Approaching source turned target retreat into prohibited motion.");
                Require(First(P(7,5), P(6,5), P(5,5), P(3,5)) == default(RuleQuantity),
                    "Source retreat concealed target approach.");
                Require(First(P(7,5), P(8,5), P(5,5), P(9,5)) == new RuleQuantity(2,3),
                    "Exact later source-relative direction change was lost.");
                Require(First((new RuleQuantity(1,3),new RuleQuantity(2)), (new RuleQuantity(1,2),new RuleQuantity(2)),
                    (new RuleQuantity(2,3),new RuleQuantity(2)), (new RuleQuantity(2,3),new RuleQuantity(2))) == default(RuleQuantity),
                    "Partial-position approach used integer anchors.");
            });
            cases.Add("tac05_frightened_versioned_relationship_lifecycle_and_cure", () => {
                var codec = new ConditionJournalCodec();
                var history = new ConditionHistory("target", relationships: true);
                ConditionHistory Restore(ConditionHistory value) {
                    var bytes = codec.Encode(value.Journal);
                    var restored = ConditionHistory.Restore(codec.Decode(bytes));
                    Require(bytes.SequenceEqual(codec.Encode(restored.Journal)), "Relationship bytes changed on restore.");
                    return restored;
                }
                ConditionApplicationData Fear(string id, string feared, bool cure = true) =>
                    new ConditionApplicationData(id, "applying-owner", "TEST_ONLY.detached-fear", "Frightened",
                        new ConditionStamp(new RuleTime(12)), "source-expiry", cure, 10,
                        fear: new FrightenedRelationshipData(feared, "use." + id, "TEST_ONLY.pinned-source"));
                history = history.Append(ConditionOperation.Apply("apply.a", default, Fear("a", "feared.a"))).State;
                history = history.Append(ConditionOperation.Apply("apply.b", default, Fear("b", "feared.b"))).State;
                history = history.Append(ConditionOperation.Apply("apply.protected", default, Fear("protected", "feared.a", false))).State;
                history = history.Append(ConditionOperation.Apply("apply.poison", default,
                    new ConditionApplicationData("poison", "owner", "TEST_ONLY.poison", "Poisoned", null, "source-cure", true))).State;
                history = Restore(history);
                Require(history.Ledger.View().Sources(ConditionKind.Frightened).Count == 3
                    && history.Ledger.Applications.Single(x => x.Id == "a").Application.Owner == "applying-owner"
                    && history.Ledger.Applications.Single(x => x.Id == "a").Application.Fear.FearedEntityId == "feared.a",
                    "Independent relationships or applying-owner distinction lost.");
                history = history.Append(ConditionOperation.Suppress("suppress.b", default, "b", true)).State;
                history = history.Append(ConditionOperation.Grant("grant", default,
                    new ConditionImmunityData("ward", "ward-owner", "TEST_ONLY.ward", new[] { "Frightened" },
                        new ConditionStamp(new RuleTime(6)), "expiry", allowRelationships: true))).State;
                Require(!history.Ledger.View().Has(ConditionKind.Frightened), "Named immunity did not suppress existing fear.");
                var prevented = history.Append(ConditionOperation.Apply("prevented", default, Fear("blocked", "feared.c")));
                Require(prevented.ApplicationPrevented && prevented.State.Ledger.Applications.Count == 4,
                    "Fear immunity created a dormant blocked application.");
                history = Restore(prevented.State);
                history = history.Append(ConditionOperation.Cure("qualified-component-test", default, "Frightened")).State;
                Require(history.Ledger.Applications.Where(x => x.Id == "a" || x.Id == "b").All(x => x.EndedAt.HasValue)
                    && !history.Ledger.Applications.Single(x => x.Id == "protected").EndedAt.HasValue
                    && history.Ledger.View().Has(ConditionKind.Poisoned),
                    "Named cure missed suppressed eligible fear or removed protected/unrelated effects.");
                history = Restore(history).Append(ConditionOperation.Advance("ward-end", new ConditionStamp(new RuleTime(6)))).State;
                Require(history.Ledger.View().Sources(ConditionKind.Frightened).SequenceEqual(new[] { "protected" })
                    && history.Ledger.Applications.Count == 4, "Immunity ending resurrected cured or prevented fear.");
                history = Restore(history).Append(ConditionOperation.Advance("final", new ConditionStamp(new RuleTime(12)))).State;
                Require(!Restore(history).Ledger.View().Has(ConditionKind.Frightened)
                    && history.Ledger.View().Has(ConditionKind.Poisoned), "Suppression paused duration or expiry removed unrelated state.");
            });
            cases.Add("tac05_frightened_policy_codec_and_relationship_rejection", () => {
                var codec = new ConditionJournalCodec();
                var fear = new FrightenedRelationshipData("feared", "source-use", "TEST_ONLY.source-revision");
                var application = new ConditionApplicationData("fear", "owner", "TEST_ONLY.effect", "Frightened",
                    new ConditionStamp(new RuleTime(12)), "source-end", true, 10, fear: fear);
                var operation = ConditionOperation.Apply("apply", default, application);
                var old = new ConditionHistory("target");
                var before = codec.Encode(old.Journal);
                Throws<ArgumentException>(() => old.Append(operation));
                Throws<ArgumentException>(() => old.Append(ConditionOperation.Cure("cure", default, "Frightened")));
                Require(before.SequenceEqual(codec.Encode(old.Journal)), "Rejected relationship changed legacy history.");
                var legacyWithRelationship = new ConditionJournal(ConditionHistory.PolicyId, "target", operations: new[] { operation });
                Throws<InvalidDataException>(() => codec.Encode(legacyWithRelationship));
                Throws<ArgumentException>(() => ConditionHistory.Restore(legacyWithRelationship));
                var plainFear = new ConditionApplicationData("fear", "owner", "source", "Frightened", null, "end", true);
                var noRelationship = new ConditionJournal(ConditionJournal.RelationshipPolicyId, "target",
                    operations: new[] { ConditionOperation.Apply("apply", default, plainFear) });
                Throws<ArgumentException>(() => ConditionHistory.Restore(codec.Decode(codec.Encode(noRelationship))));
                Throws<ArgumentException>(() => new ConditionApplicationData("p", "o", "s", "Poisoned", null, "end", true, fear: fear));
                Throws<ArgumentException>(() => new FrightenedRelationshipData("", "use", "revision"));
                var modern = new ConditionHistory("target", relationships: true).Append(operation).State;
                byte[] bytes = codec.Encode(modern.Journal);
                var decoded = ConditionHistory.Restore(codec.Decode(bytes));
                Require(decoded.Ledger.View().Has(ConditionKind.Frightened)
                    && bytes.SequenceEqual(codec.Encode(decoded.Journal))
                    && BitConverter.ToInt32(before, 4) == 1 && BitConverter.ToInt32(bytes, 4) == 2,
                    "Explicit condition codec version or replay changed.");
                var falseVersion = (byte[])before.Clone(); falseVersion[4] = 2; Resign(falseVersion);
                Throws<InvalidDataException>(() => codec.Decode(falseVersion));
                var oldImmunity = new ConditionImmunityData("ward", "owner", "source",
                    new[] { "Frightened" }, null, "end", allowRelationships: true);
                Throws<ArgumentException>(() => old.Append(ConditionOperation.Grant("grant", default, oldImmunity)));
                var all = Enum.GetValues(typeof(ConditionKind)).Cast<ConditionKind>().Select(x => x.ToString()).ToArray();
                Throws<ArgumentException>(() => new ConditionImmunityData("ward", "owner", "source", all, null, "end"));
                modern = modern.Append(ConditionOperation.Grant("full-ward", default,
                    new ConditionImmunityData("full", "owner", "source", all, null, "end", allowRelationships: true))).State;
                Require(ConditionHistory.Restore(codec.Decode(codec.Encode(modern.Journal))).Ledger.Immunities[0].Grant.Kinds.Count == 15,
                    "Explicit v2 immunity set did not persist all named kinds.");
            });
        }
    }
}
#endif
