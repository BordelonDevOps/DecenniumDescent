#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy ExplorationHidePolicy(uint seed = 2, bool clearWitness = false,
            int toolHp = 5, params ConditionFixtureEvent[] events)
            => ExplorationObservationPolicy(true, true, toolHp, seed, clearWitness ? 2 : 1, clearWitness ? 0 : 4,
                30, 30, events);

        private static Simulation ExplorationHideReady(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = ExplorationSearchReady(policy ?? ExplorationHidePolicy(), tacticalHide: false);
            // Different authored seeds may take additional complete combat rounds before a lawful exit.
            Require(!sim.Capture().InventoryCombat && sim.Capture().ObservationActions.Length == 0,
                "Ordinary Hide must start after real combat without earlier concealment.");
            return sim;
        }

        private static Command ExplorationHideCommand(Simulation sim, string id = null, string marker = null)
        {
            var state = sim.Capture();
            return IC(sim, CommandKind.Hide, marker ?? state.WorldSchedule.MarkerId(WorldLedger(sim).LastStart), id: id);
        }

        private static Command CancelHideCommand(Simulation sim)
            => IC(sim, CommandKind.CancelExplorationHide, sim.Capture().ExplorationHide.Pending.Id);

        private static ExplorationHideAttempt LastHideAttempt(Simulation sim)
            => sim.Capture().ExplorationHide.Attempts.Last();

        private static ObservationActionRecord OrdinaryHideRoll(Simulation sim)
            => sim.Capture().ObservationActions.Single(x => x.Id == LastHideAttempt(sim).End.ObservationId);

        private static Simulation SaveHide(Simulation sim, TestOnlySharedWorldPolicy policy, string directory, string name)
            => SaveBill(sim, policy, directory, "exp04-hide-" + name);

        private static string HidePublic(ExplorationHideView view)
            => string.Join("|", view.AttemptId, view.Status, view.StartedAt, view.DueAt, view.EndedAt);

        private static string HideQueryPublic(CommandQueryResult query)
            => string.Join("|", query.Supported, query.Admissible, query.Code,
                string.Join(",", query.Costs.Select(x => x.Kind + "=" + x.Amount + ":" + x.ResourceId)),
                string.Join(",", query.RequiredChoices));

        private static CommandResult FinishPaidHide(Simulation sim)
        {
            WorldCommit(sim, ExplorationHideCommand(sim));
            return SearchAdvance(sim, 18);
        }

        private static void AddExplorationHideCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            var hero = TestOnlyPolicy.ActorId;
            cases.Add("exp04_exploration_hide_genuine_roll_and_scheduled_payment", () =>
            {
                var sim = ExplorationHideReady();
                var before = sim.Capture();
                var declaration = ExplorationHideCommand(sim, "test.ordinary-hide");
                var original = WorldLedger(sim);
                Require(before.SchemaVersion == Snapshot.ObservationSchema && before.WireSchemaVersion == Snapshot.ExplorationHideSchema
                    && before.RuleClock == T(30) && original.LastStart == 10 && !original.ActionSpent
                    && before.RandomState == 3157281828u
                    && new[] { ExplorationSearcher, SearchWitness }.All(x => ActorLifeRules.CanAct(before, x)
                        && !ObservationRules.CanSee(before, x, hero) && !ObservationRules.HiddenTo(before, x, hero)),
                    "The baseline failed to establish the actual two-observer post-encounter state.");
                SaveHide(sim, ExplorationHidePolicy(), directory, "real-combat-exit");
                var bytes = Bytes(sim);
                var query = sim.QueryCommand(host, declaration);
                var option = sim.DiscoverCommands(host, hero).Single(x => x.Command.Kind == CommandKind.Hide);
                Require(query.Admissible && HideQueryPublic(query) == HideQueryPublic(option.Query)
                    && query.Costs.Select(x => (x.Kind, x.Amount)).SequenceEqual(new[] { ("action", 1L), ("elapsed-seconds", 6L) })
                    && Bytes(sim).SequenceEqual(bytes), "Query and discovery must expose the existing Action and time without mutation.");
                WorldCommit(sim, declaration);
                var paid = sim.Capture();
                var attempt = paid.ExplorationHide.Pending;
                Require(paid.RuleClock == before.RuleClock && paid.RandomState == before.RandomState && paid.ObservationActions.Length == 0
                    && attempt.PaidStart == 10 && attempt.StartedAt == T(30) && attempt.DueAt == T(36)
                    && attempt.CalendarId == before.WorldSchedule.Id && attempt.CommandId == declaration.Id
                    && WorldLedger(sim).ActionSpent && SearchInterval(paid).Action == WorldActionCommitment.None,
                    "Hide payment must use the scheduled hider Action once with no immediate time or RNG.");
                SaveHide(sim, ExplorationHidePolicy(), directory, "paid-declared");
                var reached = SearchAdvance(sim, 12);
                var after = sim.Capture();
                var roll = OrdinaryHideRoll(sim);
                Require(reached.ReachedClock == T(36) && after.RuleClock == T(36) && WorldLedger(sim).LastStart == 12
                    && !WorldLedger(sim).ActionSpent && LastHideAttempt(sim).PaidStart == 10
                    && roll.Natural == 6 && roll.WordsConsumed == 1 && roll.At == T(36)
                    && after.ObservationHideResults.Length == 2 && after.ObservationHideResults.All(x => x.Dc == 10 && !x.HiddenEstablished)
                    && LastHideAttempt(sim).End.EligibleObservers == (ExplorationHideObservers.Searcher | ExplorationHideObservers.Witness),
                    "The scheduled Start must refresh independently of the actual shared Stealth roll and its two outcomes.");
                SaveHide(sim, ExplorationHidePolicy(), directory, "rolled-two-observers");
                File.WriteAllLines(Path.Combine(directory, "exp04-hide-scheduled-payment.tsv"), new[] {
                    "paid " + before.WorldSchedule.MarkerId(attempt.PaidStart) + " via " + attempt.CommandId + " at " + attempt.StartedAt,
                    "next " + after.WorldSchedule.MarkerId(WorldLedger(sim).LastStart) + " action spent " + WorldLedger(sim).ActionSpent,
                    "roll " + roll.Id + " natural " + roll.Natural + " modifier " + roll.Modifier + " total " + roll.Total,
                    string.Join(" | ", after.ObservationHideResults.Select(x => x.ObserverId + " DC " + x.Dc + " " + x.Degree))
                });
            });

            AddExplorationHidePrivacyCases(cases, directory);
            AddExplorationHideContinuationCases(cases, directory);
            AddExplorationHidePersistenceCases(cases, directory);
        }

        private static void AddExplorationHidePrivacyCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            string hero = TestOnlyPolicy.ActorId;
            cases.Add("exp04_exploration_hide_public_lifecycle_and_cancellation", () =>
            {
                var sim = ExplorationHideReady();
                var declaration = ExplorationHideCommand(sim, "test.hide.cancelled");
                var guest = new Authority("TEST_ONLY.hide-guest", new[] { ExplorationSearcher });
                RejectUnchanged(sim, guest, declaration, "NotAuthorized");
                RejectUnchanged(sim, host, new Command("test.hide.stale", hero, declaration.ExpectedRevision - 1,
                    CommandKind.Hide, declaration.Target), "StaleRevision");
                RejectUnchanged(sim, host, ExplorationHideCommand(sim, marker: "wrong.start"), "WrongOrdinaryHideStart");
                WorldCommit(sim, declaration);
                var pending = LastHideAttempt(sim);
                Require(sim.ObserveExplorationHide(guest, pending.Id) == null && sim.ObserveExplorationHide(null, pending.Id) == null
                    && sim.ObserveExplorationHide(host, pending.Id).Status == ExplorationHideStatus.Pending,
                    "The pending lifecycle belongs to the hider.");
                Require(sim.Execute(host, declaration).Outcome == Outcome.Duplicate, "Duplicate Hide charged again.");
                RejectUnchanged(sim, host, new Command(declaration.Id, hero, declaration.ExpectedRevision,
                    CommandKind.Hide, "different.start"), "CommandIdConflict");
                foreach (var incompatible in new[] {
                    IC(sim, CommandKind.BeginWorldStep, "walk", x: 1), IC(sim, CommandKind.BeginWorldStep, "run", x: 1),
                    IC(sim, CommandKind.StartToolRepair, SharedCraftingFixture.ToolId), IC(sim, CommandKind.BeginRest),
                    IC(sim, CommandKind.HandleInventory)
                }) {
                    RejectUnchanged(sim, host, incompatible, "OrdinaryHideInProgress");
                }
                SearchAdvance(sim, 3);
                var cancel = CancelHideCommand(sim);
                var option = sim.DiscoverCommands(host, hero).Single(x => x.Command.Kind == CommandKind.CancelExplorationHide);
                Require(option.Query.Admissible && option.Query.Costs.Count == 0 && option.Command.Target == pending.Id,
                    "Pure discovery should show the pending hider's zero-cost cancellation.");
                var rng = sim.Capture().RandomState;
                WorldCommit(sim, cancel);
                Require(sim.Execute(host, cancel).Outcome == Outcome.Duplicate && WorldLedger(sim).ActionSpent
                    && sim.Capture().RuleClock == T(33) && sim.Capture().RandomState == rng
                    && sim.ObserveExplorationHide(host, pending.Id).Status == ExplorationHideStatus.Cancelled,
                    "Cancellation changed time, RNG or the paid ledger.");
                SaveHide(sim, ExplorationHidePolicy(), directory, "cancelled");
                WorldStep(sim, 1, 0);
                SearchAdvance(sim, 3);
                Require(WorldLedger(sim).LastStart == 12 && !WorldLedger(sim).ActionSpent
                    && sim.Capture().ObservationActions.Length == 0, "Cancellation did not release the claim or refreshed naturally into a roll.");
            });

            cases.Add("exp04_exploration_hide_independent_observers_and_equal_public_shape", () =>
            {
                var silent = CCApply("hide-hider-silent", "Silenced", hero, null, new ConditionStamp(T(30)));
                var blindHider = CCApply("hide-hider-blind", "Blinded", hero, null, new ConditionStamp(T(30)));
                var publicControls = new[] { silent, blindHider };
                var clearPolicy = ExplorationHidePolicy(seed: 1, clearWitness: true, events: publicControls);
                var successPolicy = ExplorationHidePolicy(seed: 1, events: publicControls);
                var ordinaryPolicy = ExplorationHidePolicy(events: publicControls);
                var clear = ExplorationHideReady(clearPolicy);
                var ordinary = ExplorationHideReady(ordinaryPolicy);
                var success = ExplorationHideReady(successPolicy);
                var blindSearcher = CCApply("hide-searcher-blind", "Blinded", ExplorationSearcher, null, new ConditionStamp(T(30)));
                var blindWitness = CCApply("hide-witness-blind", "Blinded", SearchWitness, null, new ConditionStamp(T(30)));
                var emptyPolicy = ExplorationHidePolicy(events: new[] { blindSearcher, blindWitness });
                var empty = ExplorationHideReady(emptyPolicy);
                var everyone = emptyPolicy.HostAuthority();
                WorldCommit(empty, CCCommand(empty, "hide-searcher-blind", ExplorationSearcher));
                ArchitectureCommit(empty, everyone, CCCommand(empty, "hide-witness-blind", SearchWitness));
                // Match declaration revisions without changing the other two worlds' clocks or observer state.
                foreach (var sim in new[] { clear, ordinary, success }) {
                    WorldCommit(sim, CCCommand(sim, "hide-hider-silent", hero));
                    WorldCommit(sim, CCCommand(sim, "hide-hider-blind", hero));
                }
                Require(ObservationRules.CanSee(clear.Capture(), SearchWitness, hero)
                    && !ObservationRules.CanSee(clear.Capture(), ExplorationSearcher, hero), "The independent clear-sight control is not real.");
                var shapes = new List<string>();
                var lifecycles = new List<string>();
                foreach (var sim in new[] { ordinary, clear, empty, success }) {
                    var command = ExplorationHideCommand(sim);
                    shapes.Add(HideQueryPublic(sim.QueryCommand(host, command)));
                    WorldCommit(sim, command);
                    string pending = HidePublic(sim.ObserveExplorationHide(host, LastHideAttempt(sim).Id));
                    var advance = SearchAdvance(sim, 18);
                    lifecycles.Add(pending + " -> " + HidePublic(sim.ObserveExplorationHide(host, LastHideAttempt(sim).Id))
                        + " -> " + advance.ReachedClock);
                }
                Require(shapes.Distinct().Count() == 1 && lifecycles.Distinct().Count() == 1,
                    "Public eligibility or lifecycle disclosed private observer qualification.");
                Require(clear.Capture().ObservationHideResults.Select(x => x.ObserverId).SequenceEqual(new[] { ExplorationSearcher })
                    && ObservationRules.CanSee(clear.Capture(), SearchWitness, hero)
                    && ObservationRules.LocationKnown(clear.Capture(), SearchWitness, hero)
                    && !ObservationRules.HiddenTo(clear.Capture(), SearchWitness, hero)
                    && ObservationRules.HiddenTo(clear.Capture(), ExplorationSearcher, hero)
                    && success.Capture().ObservationHideResults.All(x => x.HiddenEstablished)
                    && LastHideAttempt(empty).End.NoRoll == ExplorationHideNoRoll.NoEligibleObservers
                    && empty.Capture().ObservationActions.Length == 0 && empty.Capture().RandomState == 3157281828u,
                    "Private eligibility fabricated a result or used one clear-sighted observer as a veto.");
                SaveHide(clear, clearPolicy, directory, "independent-clear-sight");
                SaveHide(empty, ExplorationHidePolicy(events: new[] { blindSearcher, blindWitness }), directory, "empty-completed");
                foreach (var sim in new[] { ordinary, success }) {
                    var command = ExplorationHideCommand(sim);
                    shapes.Add(HideQueryPublic(sim.QueryCommand(host, command)));
                    WorldCommit(sim, command);
                    SearchAdvance(sim, 18);
                    lifecycles.Add(HidePublic(sim.ObserveExplorationHide(host, LastHideAttempt(sim).Id)));
                }
                Require(shapes[4] == shapes[5] && lifecycles[4] == lifecycles[5]
                    && LastHideAttempt(ordinary).End.NoRoll == ExplorationHideNoRoll.UnchangedFailure
                    && LastHideAttempt(success).End.ObservationId != "",
                    "A paid suppressed retry disclosed its private failure history.");
                File.WriteAllLines(Path.Combine(directory, "exp04-hide-public-lifecycle.tsv"), shapes.Concat(lifecycles));
            });
        }

        private static void AddExplorationHideContinuationCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            string hero = TestOnlyPolicy.ActorId;
            cases.Add("exp04_exploration_hide_failed_retry_relocation_and_real_search", () =>
            {
                var companionAway = CCApply("hide-companion-away", "Blinded", ExplorationSearcher,
                    new ConditionStamp(T(43)), new ConditionStamp(T(36)));
                var witnessAway = CCApply("hide-witness-away", "Blinded", SearchWitness,
                    new ConditionStamp(T(55)), new ConditionStamp(T(36)));
                var events = new[] { companionAway, witnessAway };
                var policy = ExplorationHidePolicy(events: events);
                var sim = ExplorationHideReady(policy);
                FinishPaidHide(sim);
                var failed = OrdinaryHideRoll(sim);
                uint afterFailure = sim.Capture().RandomState;
                WorldCommit(sim, CCCommand(sim, "hide-companion-away", ExplorationSearcher));
                ArchitectureCommit(sim, policy.HostAuthority(), CCCommand(sim, "hide-witness-away", SearchWitness));
                FinishPaidHide(sim);
                Require(LastHideAttempt(sim).End.NoRoll == ExplorationHideNoRoll.NoEligibleObservers,
                    "An empty qualification should remain unrolled after a real failed attempt.");
                SearchAdvance(sim, 6);
                var retry = FinishPaidHide(sim);
                var suppressed = LastHideAttempt(sim);
                Require(retry.ReachedClock == T(54) && suppressed.End.NoRoll == ExplorationHideNoRoll.UnchangedFailure
                    && suppressed.End.PriorFailureId == failed.Id && suppressed.End.PriorFailureObserverId == ExplorationSearcher
                    && suppressed.End.EligibleObservers == ExplorationHideObservers.Searcher
                    && sim.Capture().RandomState == afterFailure && sim.Capture().ObservationActions.Length == 1
                    && sim.ObserveExplorationHide(host, suppressed.Id).Status == ExplorationHideStatus.Completed,
                    "Intervening no-roll or observer-count changes must not reset the actual failed comparison.");
                SaveHide(sim, ExplorationHidePolicy(events: events), directory, "unchanged-paid-no-roll");

                FinishPaidHide(sim);
                Require(LastHideAttempt(sim).End.EligibleObservers == (ExplorationHideObservers.Searcher | ExplorationHideObservers.Witness)
                    && LastHideAttempt(sim).End.PriorFailureId == failed.Id && sim.Capture().RuleClock == T(60),
                    "A returning observer cleared failed-result history.");
                WorldStep(sim, 1, 0);
                SearchAdvance(sim, 1, 2);
                Require(sim.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(5, 2),
                    "The alternate-position witness did not traverse an actual edge.");
                RejectUnchanged(sim, host, ExplorationHideCommand(sim), "OrdinaryHideRequiresStationaryAnchor");
                SearchAdvance(sim, 1, 2);
                WorldStep(sim, -1, 0);
                SearchAdvance(sim, 5);
                FinishPaidHide(sim);
                Require(sim.Capture().RuleClock == T(72) && LastHideAttempt(sim).End.NoRoll == ExplorationHideNoRoll.UnchangedFailure
                    && sim.Capture().RandomState == afterFailure, "An excursion back to the failed position authorized an unchanged retry.");

                WorldStep(sim, 1, 0);
                SearchAdvance(sim, 6);
                var arrived = sim.Capture();
                Require(arrived.RuleClock == T(78) && arrived.ExplorationHide.LatestRelocation.At == T(73)
                    && arrived.ExplorationHide.LatestRelocation.To.Equals(new ExplorationSearchCell(2, 0)),
                    "The second authored anchor was not established by actual movement.");
                FinishPaidHide(sim);
                var concealed = LastHideAttempt(sim);
                var actualHide = OrdinaryHideRoll(sim);
                Require(concealed.Anchor.Equals(new ExplorationSearchCell(2, 0)) && concealed.Relocation.At == T(73)
                    && actualHide.At == T(84) && actualHide.Total == 14 && actualHide.WordsConsumed == 1
                    && new[] { ExplorationSearcher, SearchWitness }.All(x => ObservationRules.HiddenTo(sim.Capture(), x, hero)),
                    "A paid Hide after genuine relocation did not establish separate Hidden results.");
                SaveHide(sim, ExplorationHidePolicy(events: events), directory, "alternate-real-hidden");
                WorldStep(sim, -1, 0);
                SearchAdvance(sim, 6);
                Require(sim.Capture().RuleClock == T(90)
                    && SearchKnowledge(sim.Capture(), ExplorationSearcher).HiddenAttemptId == actualHide.Id
                    && SearchKnowledge(sim.Capture(), SearchWitness).HiddenAttemptId == actualHide.Id,
                    "Actual unseen return lost or replaced the genuine ordinary Hide record.");
                int[] expectedDraws = { 7, 11, 13, 19 };
                for (int i = 0; i < expectedDraws.Length; i++) {
                    WorldCommit(sim, ExplorationSearchCommand(sim));
                    SearchAdvance(sim, 18);
                    var search = sim.Capture().ExplorationSearch.Attempts.Last();
                    var result = LastExplorationSearchResult(sim.Capture());
                    Require(search.End.HideId == actualHide.Id && result.Natural == expectedDraws[i]
                        && result.WordsConsumed == 1 && (result.Outcome == ObservationActionOutcome.SearchFound) == (i == 3),
                        "Paid Search did not resolve against the recorded ordinary Stealth total.");
                }
                var found = sim.Capture();
                Require(found.RuleClock == T(114) && !ObservationRules.HiddenTo(found, ExplorationSearcher, hero)
                    && ObservationRules.LocationKnown(found, ExplorationSearcher, hero)
                    && !ObservationRules.CanSee(found, ExplorationSearcher, hero)
                    && ObservationRules.HiddenTo(found, SearchWitness, hero),
                    "Ordinary Search leaked its actual finding to the second observer.");
                SaveHide(sim, ExplorationHidePolicy(events: events), directory, "continued-and-found");
                File.WriteAllLines(Path.Combine(directory, "exp04-hide-retry-and-search.tsv"), new[] {
                    "failure " + failed.Id + " at " + failed.At + " total " + failed.Total,
                    "paid suppressed " + suppressed.Id + " at " + suppressed.End.At + " with no RNG",
                    "completed move " + concealed.Relocation.ArrivalCommandId + " at " + concealed.Relocation.At,
                    "ordinary concealment " + actualHide.Id + " at " + actualHide.At + " total " + actualHide.Total,
                    "unseen return followed by paid Search draws " + string.Join(",", expectedDraws),
                    "actual private find at " + found.RuleClock + "; second observer remains Hidden"
                });
            });

            cases.Add("exp04_exploration_hide_and_search_same_boundary_receipt_orders", () =>
            {
                const uint seed = 1;
                var original = ExplorationHideReady(ExplorationHidePolicy(seed));
                var before = original.Capture();
                var reverse = new Simulation(ExplorationHidePolicy(seed), before, ExecutionProfile.Laboratory);
                var clock = before.RuleClock;
                Require(PlaytestDice.RollD20(before.RandomState).Natural >= 10,
                    "Selected authored seed does not establish Hide before the first Search. Actual time " + clock
                    + " RNG " + before.RandomState + " die " + PlaytestDice.RollD20(before.RandomState).Natural);
                WorldCommit(original, ExplorationHideCommand(original));
                WorldCommit(original, ExplorationSearchCommand(original));
                WorldCommit(reverse, ExplorationSearchCommand(reverse));
                WorldCommit(reverse, ExplorationHideCommand(reverse));
                var forwardAdvance = SearchAdvance(original, 24);
                var reverseAdvance = SearchAdvance(reverse, 24);
                var a = original.Capture();
                var b = reverse.Capture();
                var hide = OrdinaryHideRoll(original);
                var reversedHide = OrdinaryHideRoll(reverse);
                var sa = LastExplorationSearchResult(a);
                var sb = LastExplorationSearchResult(b);
                var due = LastHideAttempt(original).DueAt;
                Require(due == clock.AddSeconds(6) && a.RuleClock == due && b.RuleClock == due
                    && forwardAdvance.ReachedClock == due && reverseAdvance.ReachedClock == due
                    && a.ExplorationHide.Pending == null && a.ExplorationSearch.Pending == null
                    && b.ExplorationHide.Pending == null && b.ExplorationSearch.Pending == null,
                    "The same-boundary batch failed to resolve both procedures at one shared yield.");
                Require(sa.At == sb.At && sa.Revision == hide.Revision && sb.Revision == reversedHide.Revision
                    && a.ExplorationSearch.Attempts.Single().End.HideId == hide.Id && sa.WordsConsumed == 1
                    && sa.RandomBefore == hide.RandomAfter && a.RandomState == sa.RandomAfter
                    && b.ExplorationSearch.Attempts.Single().End.HideId == "" && sb.WordsConsumed == 0
                    && reversedHide.RandomBefore == sb.RandomAfter && b.RandomState == reversedHide.RandomAfter
                    && reversedHide.Natural == hide.Natural && ObservationRules.HiddenTo(b, ExplorationSearcher, hero),
                    "Search did not use the actual Hide/RNG/knowledge state at its position in receipt order.");
                SaveHide(original, ExplorationHidePolicy(seed), directory, "coincident-hide-before-search");
                SaveHide(reverse, ExplorationHidePolicy(seed), directory, "coincident-search-before-hide");
                var codec = new SnapshotCodec();
                var reversedRecords = original.Capture();
                Array.Reverse(reversedRecords.ObservationActions);
                Throws<ArgumentException>(() => codec.Encode(reversedRecords));

                var forgedOrder = reverse.Capture();
                var actualReverseSearch = b.ExplorationSearch.Attempts.Single();
                var invalidEarlierSearch = actualReverseSearch.Finish(a.ExplorationSearch.Attempts.Single().End);
                forgedOrder.ExplorationSearch = new ExplorationSearchRecord(b.ExplorationSearch.Definition, new[] { invalidEarlierSearch });
                forgedOrder.ObservationActions = new[] { sa, reversedHide };
                Throws<ArgumentException>(() => codec.Encode(forgedOrder));
                File.WriteAllLines(Path.Combine(directory, "exp04-hide-coincident-order.tsv"), new[] {
                    "shared clock " + due + " shared completion revision " + sa.Revision,
                    "Hide first " + hide.Natural + " then Search " + sa.Natural + " (" + sa.Outcome + ")",
                    "Search first draws " + sb.WordsConsumed + " then Hide " + reversedHide.Natural
                });
            });
        }

        private static void AddExplorationHidePersistenceCases(Dictionary<string, Action> cases, string directory)
        {
            var hero = TestOnlyPolicy.ActorId;
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("exp04_exploration_hide_due_effects_interruptions_and_remote_work", () =>
            {
                var stunned = CCApply("hide-hider-stunned", "Stunned", hero, new ConditionStamp(T(35)), new ConditionStamp(T(33)));
                var stunnedPolicy = ExplorationHidePolicy(events: new[] { stunned });
                var interrupted = ExplorationHideReady(stunnedPolicy);
                WorldCommit(interrupted, ExplorationHideCommand(interrupted));
                SearchAdvance(interrupted, 3);
                WorldCommit(interrupted, CCCommand(interrupted, "hide-hider-stunned", hero));
                var stopped = LastHideAttempt(interrupted);
                Require(stopped.End.At == T(33) && stopped.End.Interruption == ExplorationHideInterruption.ActionCapabilityLost
                    && WorldLedger(interrupted).ActionSpent && interrupted.Capture().ObservationActions.Length == 0,
                    "Actual incapacity must interrupt while retaining the paid Action.");
                interrupted = SaveHide(interrupted, ExplorationHidePolicy(events: new[] { stunned }), directory, "condition-interrupted");
                SearchAdvance(interrupted, 9);
                Require(interrupted.Capture().ExplorationHide.Pending == null && interrupted.Capture().ObservationActions.Length == 0,
                    "Recovery automatically resumed an interrupted Hide.");

                var mode = ExplorationHideReady();
                WorldCommit(mode, ExplorationHideCommand(mode));
                SearchAdvance(mode, 3);
                RejectUnchanged(mode, host, IC(mode, CommandKind.BeginFixedEncounter, "unlawful"), "InvalidSharedCombatEntry");
                WorldCommit(mode, IC(mode, CommandKind.BeginFixedEncounter, id: "test.hide-lawful-mode-entry"));
                Require(mode.Capture().InventoryCombat && LastHideAttempt(mode).End.At == T(33)
                    && LastHideAttempt(mode).End.Interruption == ExplorationHideInterruption.TacticalControlEntered
                    && WorldLedger(mode).ActionSpent && mode.Capture().ObservationActions.Length == 0,
                    "Actual tactical re-entry must interrupt, retaining original payment and RNG.");
                SaveHide(mode, ExplorationHidePolicy(), directory, "mode-interrupted");
                WorldCommit(mode, Tac(mode, CommandKind.EndFixedEncounter));
                Require(!mode.Capture().InventoryCombat && mode.Capture().ExplorationHide.Pending == null
                    && mode.Capture().ObservationActions.Length == 0, "Returning to exploration revived an interrupted Hide.");

                var poison = CCApply("hide-hider-poison", "Poisoned", hero, new ConditionStamp(T(36)), new ConditionStamp(T(30)));
                var events = new[] { poison };
                var workPolicy = ExplorationHidePolicy(toolHp: 4, events: events);
                var work = ExplorationHideReady(workPolicy);
                var everyone = workPolicy.HostAuthority();
                WorldCommit(work, CCCommand(work, "hide-hider-poison", hero));
                WorldCommit(work, ExplorationHideCommand(work));
                ArchitectureCommit(work, everyone, IC(work, CommandKind.BeginWorldStep, "walk", actor: SearchWitness, x: 1));
                SearchAdvance(work, 1);
                ArchitectureCommit(work, everyone, IC(work, CommandKind.BeginWorldStep, "walk", actor: SearchWitness, x: 1));
                SearchAdvance(work, 1);
                ArchitectureCommit(work, everyone, IC(work, CommandKind.StartToolRepair, SharedCraftingFixture.ToolId, actor: SearchWitness));
                var reached = SearchAdvance(work, 20);
                var state = work.Capture();
                var repair = state.RepairWork.Single(x => x.WorkerId == SearchWitness);
                Require(reached.ReachedClock == T(36) && OrdinaryHideRoll(work).Selection == ObservationDieSelection.Normal
                    && WorldLedger(work).LastStart == 12 && !WorldLedger(work).ActionSpent
                    && repair.Work.Labor == T(4) && repair.Status == RepairWorkStatus.Working,
                    "Exact due effects and the new Start must settle before Hide while compatible remote repair receives actual time.");
                SaveHide(work, ExplorationHidePolicy(toolHp: 4, events: events), directory, "expiry-start-and-remote-work");
                File.WriteAllLines(Path.Combine(directory, "exp04-hide-interruptions-and-work.tsv"), new[] {
                    "actual interruption " + stopped.End.Interruption + " at " + stopped.End.At,
                    "lawful tactical interruption " + LastHideAttempt(mode).End.At,
                    "due Poisoned expiry and normal selection " + state.RuleClock + "; compatible remote repair " + repair.Work.Labor
                });
            });

            cases.Add("exp04_exploration_hide_exact_restore_partition_and_integrity", () =>
            {
                var codec = new SnapshotCodec();
                var sim = ExplorationHideReady();
                var restored = SaveHide(sim, ExplorationHidePolicy(), directory, "restore-before");
                var declaration = ExplorationHideCommand(sim);
                foreach (var run in new[] { sim, restored }) {
                    WorldCommit(run, declaration);
                    SearchAdvance(run, 5, 2);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Identical traces diverged before the pending save.");
                var pending = SaveHide(sim, ExplorationHidePolicy(), directory, "restore-partial");
                var partitioned = new Simulation(ExplorationHidePolicy(), pending.Capture(), ExecutionProfile.Laboratory);
                var terminal = IC(sim, CommandKind.AdvanceClock, x: 9, y: 1, id: "test.hide-restored-terminal");
                WorldCommit(sim, terminal);
                WorldCommit(pending, terminal);
                Require(Bytes(sim).SequenceEqual(Bytes(pending)), "Identical pending restores and traces changed exact terminal bytes.");
                SearchAdvance(partitioned, 3, 2);
                SearchAdvance(partitioned, 2);
                var a = sim.Capture();
                var b = partitioned.Capture();
                var actual = OrdinaryHideRoll(sim);
                var divided = OrdinaryHideRoll(partitioned);
                Require(a.RuleClock == b.RuleClock && a.RandomState == b.RandomState
                    && a.WorldSchedule.ProcessedSlot == b.WorldSchedule.ProcessedSlot
                    && WorldLedger(sim).LastStart == WorldLedger(partitioned).LastStart
                    && WorldLedger(sim).ActionSpent == WorldLedger(partitioned).ActionSpent
                    && actual.Natural == divided.Natural && actual.Selection == divided.Selection && actual.Total == divided.Total
                    && a.ObservationHideResults.Select(x => (x.ObserverId, x.Dc, x.Degree))
                        .SequenceEqual(b.ObservationHideResults.Select(x => (x.ObserverId, x.Dc, x.Degree))),
                    "Partitioning the shared clock changed mechanical outcomes.");
                SaveHide(sim, ExplorationHidePolicy(), directory, "restore-completed");

                void RejectAltered(Snapshot altered)
                    => Throws<ArgumentException>(() => new Simulation(ExplorationHidePolicy(), codec.Decode(codec.Encode(altered)),
                        ExecutionProfile.Laboratory));
                var paid = SaveHide(ExplorationHideReady(), ExplorationHidePolicy(), directory, "wire92-control");
                WorldCommit(paid, ExplorationHideCommand(paid));
                var noPayment = paid.Capture();
                noPayment.WorldIntervals = noPayment.WorldIntervals.Select(x => x.ActorId == hero
                    ? new WorldIntervalRecord(x.ActorId, x.LastStart) : x).ToArray();
                RejectAltered(noPayment);

                var forgedMarker = sim.Capture();
                var hide = forgedMarker.ExplorationHide;
                var attempt = hide.Attempts.Single();
                forgedMarker.ExplorationHide = new ExplorationHideRecord(hide.Definition, null, new[] {
                    new ExplorationHideAttempt(attempt.Revision, attempt.CommandId, "forged.calendar", attempt.PaidStart,
                        attempt.StartedAt, attempt.DueAt, attempt.Anchor, end: attempt.End) });
                RejectAltered(forgedMarker);

                var forgedMove = sim.Capture();
                var move = new ExplorationHideRelocation(new ExplorationSearchCell(2, 0), attempt.Anchor,
                    attempt.Revision - 2, attempt.Revision - 1, "forged.arrival", attempt.StartedAt);
                forgedMove.ExplorationHide = new ExplorationHideRecord(hide.Definition, move, new[] {
                    new ExplorationHideAttempt(attempt.Revision, attempt.CommandId, attempt.CalendarId, attempt.PaidStart,
                        attempt.StartedAt, attempt.DueAt, attempt.Anchor, move, attempt.End) });
                RejectAltered(forgedMove);

                var forgedObserver = sim.Capture();
                var old = forgedObserver.ObservationHideResults.Single(x => x.ObserverId == SearchWitness);
                forgedObserver.ObservationHideResults = forgedObserver.ObservationHideResults.Where(x => x != old)
                    .Append(new ObservationHideResultRecord(old.AttemptId, AdditionalTacticalActor.Id, old.ObserverX,
                        old.ObserverY, old.Dc, old.Degree, old.HiddenEstablished)).ToArray();
                RejectAltered(forgedObserver);

                var forgedResult = sim.Capture();
                var end = attempt.End;
                forgedResult.ExplorationHide = new ExplorationHideRecord(hide.Definition, null, new[] {
                    attempt.Finish(new ExplorationHideEnd(end.Status, end.Interruption, end.Revision, end.CommandId,
                        end.At, "forged.observation", eligibleObservers: end.EligibleObservers)) });
                RejectAltered(forgedResult);

                var forgedAuthority = sim.Capture();
                forgedAuthority.ContentFingerprint = ExplorationSearchPolicy().ContentFingerprint;
                RejectAltered(forgedAuthority);
            });

            cases.Add("exp04_exploration_hide_independent_wire_and_legacy_profiles", () =>
            {
                var codec = new SnapshotCodec();
                var wire92 = ExplorationHideReady();
                var wire91 = ExplorationSearchReady();
                var wire51 = ExplorationSearchReady(ExplorationSearchPolicy(false));
                var current = wire92.Capture();
                foreach (var pair in new[] { (Run: wire51, Wire: 51), (Run: wire91, Wire: 91), (Run: wire92, Wire: 92) }) {
                    byte[] bytes = Bytes(pair.Run);
                    var decoded = codec.Decode(bytes);
                    Require(BitConverter.ToInt32(bytes, 4) == pair.Wire && decoded.SchemaVersion == 51
                        && decoded.WireSchemaVersion == pair.Wire && codec.Encode(decoded).SequenceEqual(bytes),
                        "An ordinary observation wire profile lost its exact base or encoding.");
                }
                Require(!wire51.QueryCommand(host, ExplorationHideCommand(wire51)).Supported
                    && !wire91.QueryCommand(host, ExplorationHideCommand(wire91)).Supported
                    && wire91.Capture().ObservationActions.Single().Kind == ObservationActionKind.Hide
                    && wire92.QueryCommand(host, ExplorationHideCommand(wire92)).Admissible,
                    "The selected ordinary action altered the old tactical profile boundary.");
                RejectUnchanged(wire91, host, ExplorationHideCommand(wire91), "ObservationActionRequiresTacticalCombat");
                Throws<ArgumentException>(() => new Simulation(ExplorationHidePolicy(), wire91.Capture(), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(ExplorationSearchPolicy(), current, ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(ExplorationHidePolicy(), current, ExecutionProfile.Release));
                var omitted = wire92.Capture();
                omitted.ExplorationHide = null;
                Throws<ArgumentException>(() => codec.Encode(omitted));
                var moved = wire51.Capture();
                moved.ExplorationHide = current.ExplorationHide;
                Throws<ArgumentException>(() => codec.Encode(moved));
                foreach (var oldWire in new[] { 51, 90, 91 }) {
                    byte[] bytes = Bytes(wire92);
                    Buffer.BlockCopy(BitConverter.GetBytes(oldWire), 0, bytes, 4, 4);
                    int payloadLength = bytes.Length - 32;
                    using (var hash = System.Security.Cryptography.SHA256.Create())
                        Buffer.BlockCopy(hash.ComputeHash(bytes, 0, payloadLength), 0, bytes, payloadLength, 32);
                    Throws<InvalidDataException>(() => codec.Decode(bytes));
                }
                SaveHide(wire91, ExplorationSearchPolicy(), directory, "wire91-control");
                SaveHide(wire51, ExplorationSearchPolicy(false), directory, "wire51-control");
            });
        }
    }
}
#endif
