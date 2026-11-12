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
        private const string ExplorationSearcher = TestOnlyPolicy.CompanionId;
        private const string SearchWitness = "TEST_ONLY.search-witness";

        private static TestOnlySharedWorldPolicy ExplorationSearchPolicy(bool enabled = true, int toolHp = 5,
            params ConditionFixtureEvent[] events)
            => ExplorationObservationPolicy(enabled, false, toolHp, 2, 1, 4, 30, 30, events);

        private static TestOnlySharedWorldPolicy ExplorationObservationPolicy(bool search, bool hide, int toolHp, uint seed,
            int witnessX, int witnessY, int companionRange, int witnessRange, ConditionFixtureEvent[] events)
        {
            var original = ObservationObserverIsolatedGapFixture();
            var map = new ObservationFixture(8, 8,
                original.Cells.Append(new ObservationGridCell(2, 1, true, false, true)),
                original.Profiles.Select(x => x.ActorId == ExplorationSearcher
                    ? new ObservationSightProfile(x.ActorId, companionRange, 30) : x)
                    .Append(new ObservationSightProfile(SearchWitness, witnessRange, 30)));
            var config = new SharedWorldConfiguration("TEST_ONLY.search-source-baseline",
                new[] { new SharedActorDefinition("profile.numeric-warrior3", "TEST_ONLY.numeric-warrior3", 30) },
                new[] { new SharedActorInstanceDefinition(SearchWitness, "profile.numeric-warrior3", witnessX, witnessY) },
                new[] { new SharedSiteDefinition("profile.tool-repair", SharedSiteDefinition.ToolRepairProfile) },
                new SharedSiteInstanceDefinition("TEST_ONLY.search-unused-site", "profile.tool-repair", 4, 4),
                "TEST_ONLY.search-unused-lot");
            var conditions = new ConditionCombatFixture(new[] { CCApply("observation-exit-blind", "Blinded", AdditionalTacticalActor.Id) }
                .Concat(events).ToArray());
            var policy = new TestOnlySharedWorldPolicy(config, new SharedCombatFixture(1, seed), null,
                new SharedCraftingFixture(toolHp: toolHp), new SharedRepairFixture(siteX: 4, siteY: 4),
                conditions: conditions).EnableObservation(map);
            if (search) policy.EnableExplorationSearch();
            return hide ? policy.EnableExplorationHide() : policy;
        }

        private static Simulation ExplorationSearchReady(TestOnlySharedWorldPolicy policy = null, bool tacticalHide = true)
        {
            policy = policy ?? ExplorationSearchPolicy();
            var sim = World(policy);
            CCDispatch(sim, "observation-exit-blind", AdditionalTacticalActor.Id);
            WorldStep(sim, 1, 0);
            WorldAdvance(sim, 1);
            WorldCommit(sim, IC(sim, CommandKind.BeginFixedEncounter, id: "search.baseline.begin"));
            return RunObservationHideThroughExit(policy, Bytes(sim), 3, tacticalHide);
        }

        private static WorldActivityIntervalRecord SearchInterval(Snapshot state)
            => state.WorldActivityIntervals.Single(x => x.ActorId == ExplorationSearcher);

        private static Command ExplorationSearchCommand(Simulation sim, int x = 1, int y = 0, string id = null)
        {
            var s = sim.Capture();
            var interval = SearchInterval(s);
            return new Command(id ?? "test.search." + (s.Revision + 1), ExplorationSearcher, s.Revision, CommandKind.Search,
                ExplorationSearchRecord.Marker(interval.CalendarId, interval.IntervalIndex), x, y);
        }

        private static Command SearchCancellation(Simulation sim)
        {
            var s = sim.Capture();
            return new Command("test.cancel-search." + (s.Revision + 1), ExplorationSearcher,
                s.Revision, CommandKind.CancelExplorationSearch, s.ExplorationSearch.Pending.Id);
        }

        private static ObservationActionRecord LastExplorationSearchResult(Snapshot state)
            => state.ObservationActions.Single(x => x.Id == state.ExplorationSearch.Attempts.Last().End.ObservationId);

        private static CommandResult SearchAdvance(Simulation sim, int seconds, int denominator = 1)
        {
            var command = IC(sim, CommandKind.AdvanceClock, x: seconds, y: denominator);
            var result = sim.Execute(TestOnlySharedWorldPolicy.Host(), command);
            Require(result.Outcome == Outcome.Committed, "Clock advance failed: " + result.Code);
            return result;
        }

        private static ObserverKnowledgeRecord SearchKnowledge(Snapshot state, string actor)
            => state.ObserverKnowledge.Single(x => x.ObserverId == actor && x.TargetId == TestOnlyPolicy.ActorId);

        private static Simulation SaveExplorationSearch(Simulation sim, TestOnlySharedWorldPolicy policy, string directory, string name)
            => SaveBill(sim, policy, directory, "exp04-search-" + name);

        private static void AddExplorationSearchCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("exp04_exploration_search_genuine_hide_and_paid_interval", () =>
            {
                var sim = ExplorationSearchReady();
                var before = sim.Capture();
                var d = before.ExplorationSearch.Definition;
                var hide = before.ObservationActions.Single(x => x.Kind == ObservationActionKind.Hide);
                Require(before.SchemaVersion == Snapshot.ObservationSchema && before.WireSchemaVersion == Snapshot.ExplorationSearchSchema
                    && before.LaterEncounter == null && before.CharterAttempt == null && before.SurpriseEntry == null && !before.InventoryCombat
                    && before.RuleClock == T(30) && hide.At == T(1) && hide.Total == 18 && before.RandomState == 3157281828u
                    && d.DirectorId == ExplorationSearchDefinition.Director && d.CueId == ExplorationSearchDefinition.VisibleFringe
                    && d.Anchor.Equals(new ExplorationSearchCell(3, 3)) && d.CueCandidate.Equals(new ExplorationSearchCell(1, 0))
                    && d.Sign.Equals(new ExplorationSearchCell(2, 2)) && d.Occlusion.Equals(new ExplorationSearchCell(2, 1))
                    && new[] { ExplorationSearcher, SearchWitness }.All(x => ActorLifeRules.CanAct(before, x)
                        && ObservationRules.HiddenTo(before, x, TestOnlyPolicy.ActorId)
                        && !ObservationRules.CanSee(before, x, TestOnlyPolicy.ActorId)),
                    "The selected independent profile lost its genuine two-observer concealment and authored sight geometry.");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "before-declaration");

                var declaration = ExplorationSearchCommand(sim);
                WorldCommit(sim, declaration);
                var pending = sim.Capture();
                var attempt = pending.ExplorationSearch.Pending;
                var activity = SearchInterval(pending);
                Require(attempt.StartedAt == T(30) && attempt.DueAt == T(36) && attempt.IntervalIndex == 5
                    && activity.Action == WorldActionCommitment.Search && activity.ActionReference == declaration.Id
                    && activity.ActionReferenceRevision == pending.Revision && pending.ObservationActions.Length == before.ObservationActions.Length
                    && pending.RandomState == before.RandomState && pending.RuleClock == before.RuleClock
                    && sim.ObserveExplorationSearch(host, attempt.Id).Status == ExplorationSearchViewStatus.Pending,
                    "Declaration must pay the existing Action and leave the clock and RNG untouched.");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "paid-pending");
                File.WriteAllLines(Path.Combine(directory, "exp04-search-authority.tsv"), new[] {
                    "genuine Hide " + hide.Id + " at " + hide.At + " total " + hide.Total,
                    "actual exit and declaration " + before.RuleClock + " interval " + activity.IntervalIndex
                        + " paid by " + declaration.Id + " revision " + activity.ActionReferenceRevision,
                    "source " + d.SourceRevision + " Director " + d.DirectorId + " private cue " + d.CueId
                });
            });

            cases.Add("exp04_exploration_search_query_payment_cancel_and_conflicts", () =>
            {
                var sim = ExplorationSearchReady();
                var before = Bytes(sim);
                var discovery = sim.DiscoverCommands(host, ExplorationSearcher);
                var cells = new[] { (X: 1, Y: 0), (X: 0, Y: 1), (X: 2, Y: 0) };
                foreach (var cell in cells) {
                    var command = ExplorationSearchCommand(sim, cell.X, cell.Y);
                    var query = sim.QueryCommand(host, command);
                    var option = discovery.Single(x => x.Command.Kind == CommandKind.Search && x.Command.X == cell.X && x.Command.Y == cell.Y);
                    Require(query.Admissible && query.Code == "Available" && option.Query.Admissible
                        && query.Costs.Select(x => (x.Kind, x.Amount)).SequenceEqual(new[] { ("action", 1L), ("elapsed-seconds", 6L) }),
                        "Public query and discovery must have identical legal cost independent of hidden content.");
                }
                Require(before.SequenceEqual(Bytes(sim)), "Search query or discovery changed hidden state, clock, receipts or RNG.");
                var unauthorized = new Authority("TEST_ONLY.other-observer", new[] { SearchWitness });
                RejectUnchanged(sim, unauthorized, ExplorationSearchCommand(sim), "NotAuthorized");
                var real = ExplorationSearchCommand(sim);
                RejectUnchanged(sim, host, new Command("test.stale-search", real.Actor, real.ExpectedRevision - 1,
                    real.Kind, real.Target, real.X, real.Y), "StaleRevision");
                WorldCommit(sim, real);
                var paid = Bytes(sim);
                Require(sim.Execute(host, real).Outcome == Outcome.Duplicate && paid.SequenceEqual(Bytes(sim)),
                    "A duplicate declaration paid or initiated a second attempt.");
                RejectUnchanged(sim, host, new Command(real.Id, real.Actor, sim.Capture().Revision,
                    real.Kind, real.Target, 0, 1), "CommandIdConflict");
                var active = sim.Capture().ExplorationSearch.Pending;
                Require(sim.ObserveExplorationSearch(unauthorized, active.Id) == null,
                    "A non-controller obtained another observer's Search projection.");
                var moving = IC(sim, CommandKind.BeginWorldStep, "walk", actor: ExplorationSearcher, x: 0, y: 1);
                Require(sim.QueryCommand(host, moving).Code == "OrdinarySearchInProgress", "Movement query ignored the active Search.");
                RejectUnchanged(sim, host, moving, "OrdinarySearchInProgress");
                RejectUnchanged(sim, host, IC(sim, CommandKind.BeginWorldStep, "run", actor: ExplorationSearcher, x: 0, y: 1),
                    "OrdinarySearchInProgress");
                RejectUnchanged(sim, host, FarmCommand(sim, CommandKind.PlantCrop), "OrdinarySearchInProgress");

                var cancel = SearchCancellation(sim);
                WorldCommit(sim, cancel);
                var stopped = sim.Capture();
                Require(stopped.ExplorationSearch.Attempts.Single().End.At == T(30) && stopped.RandomState == 3157281828u
                    && SearchInterval(stopped).Action == WorldActionCommitment.Search
                    && sim.ObserveExplorationSearch(host, active.Id).Status == ExplorationSearchViewStatus.Cancelled,
                    "Cancellation must release only the stationary claim while retaining the actual paid Action.");
                RejectUnchanged(sim, host, FarmCommand(sim, CommandKind.PlantCrop), "OffCalendarActionAlreadySpent");
                RejectUnchanged(sim, host, ExplorationSearchCommand(sim), "OffCalendarActionAlreadySpent");
                Throws<InvalidOperationException>(() => SearchInterval(stopped).CommitActiveLabor("test.forged-labor"));
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "cancelled-payment");
                var released = new Simulation(ExplorationSearchPolicy(), stopped, ExecutionProfile.Laboratory);
                WorldCommit(released, IC(released, CommandKind.BeginWorldStep, "walk", actor: ExplorationSearcher, y: 1));
                Require(SearchInterval(released.Capture()).Action == WorldActionCommitment.Search,
                    "Ordinary movement after cancellation must use the released claim without refunding the Action.");
                WorldAdvance(sim, 6);
                Require(SearchInterval(sim.Capture()).Action == WorldActionCommitment.None
                    && sim.QueryCommand(host, ExplorationSearchCommand(sim)).Admissible,
                    "Only the ordinary interval refresh can permit a separately paid Search.");
            });

            cases.Add("exp04_exploration_search_private_no_finding_and_real_success", () =>
            {
                var sim = ExplorationSearchReady();
                var ready = sim.Capture();
                var empty = new Simulation(ExplorationSearchPolicy(), ready, ExecutionProfile.Laboratory);
                var absent = new Simulation(ExplorationSearchPolicy(), ready, ExecutionProfile.Laboratory);
                var unqualified = new Simulation(ExplorationSearchPolicy(), ready, ExecutionProfile.Laboratory);
                var partial = new Simulation(ExplorationSearchPolicy(), ready, ExecutionProfile.Laboratory);
                var witness = SearchKnowledge(ready, SearchWitness);
                WorldCommit(sim, ExplorationSearchCommand(sim));
                WorldCommit(empty, ExplorationSearchCommand(empty, 0, 1));
                WorldCommit(absent, ExplorationSearchCommand(absent));
                WorldStep(absent, 1, 0);
                WorldAdvance(absent, 1);
                WorldCommit(unqualified, ExplorationSearchCommand(unqualified, 2, 0));
                WorldStep(unqualified, 1, 0);
                WorldAdvance(unqualified, 1);
                WorldCommit(partial, ExplorationSearchCommand(partial));
                SearchAdvance(partial, 11, 2);
                WorldStep(partial, 1, 0);
                var paid = ready.ExplorationSearch.Definition;
                var first = SearchAdvance(sim, 12);
                var second = SearchAdvance(empty, 12);
                var vacated = SearchAdvance(absent, 12);
                var noCue = SearchAdvance(unqualified, 12);
                var betweenCells = SearchAdvance(partial, 12);
                var failure = LastExplorationSearchResult(sim.Capture());
                var noRoll = LastExplorationSearchResult(empty.Capture());
                var noTarget = LastExplorationSearchResult(absent.Capture());
                Require(new[] { first, second, vacated, noCue, betweenCells }.All(x => x.ReachedClock == T(36) && x.Code == "Committed"
                    && x.TacticalDecisionAt == null) && failure.Natural == 6 && failure.WordsConsumed == 1
                    && noRoll.WordsConsumed == 0 && noTarget.WordsConsumed == 0
                    && LastExplorationSearchResult(unqualified.Capture()).WordsConsumed == 0 && Body(unqualified).X == 2
                    && LastExplorationSearchResult(partial.Capture()).WordsConsumed == 0
                    && partial.Capture().WorldTraversals.Single().DistanceFeet == Q(5, 2),
                    "A long advance must yield at the same endpoint for qualified failure, empty and actual vacancy.");
                var view = sim.ObserveExplorationSearch(host, sim.Capture().ExplorationSearch.Attempts.Single().Id);
                foreach (var run in new[] { empty, absent, unqualified, partial }) {
                    var projection = run.ObserveExplorationSearch(host, view.AttemptId);
                    Require(view.Status == ExplorationSearchViewStatus.NoFinding
                        && projection.GetType().GetProperties().All(p => Equals(p.GetValue(view), p.GetValue(projection))),
                        "A public no-finding projection exposed private occupancy, qualification or a failed roll.");
                }
                Require(sim.Capture().ExplorationSearch.Attempts.Single().End.CueId == paid.CueId
                    && sim.Capture().ExplorationSearch.Attempts.Single().End.HideId == "observation.6.hide"
                    && empty.Capture().RandomState == ready.RandomState && absent.Capture().RandomState == ready.RandomState,
                    "Private failed-check evidence or no-roll RNG continuity was lost.");
                SaveExplorationSearch(empty, ExplorationSearchPolicy(), directory, "empty-completed");
                SaveExplorationSearch(absent, ExplorationSearchPolicy(), directory, "unseen-vacated-candidate");
                SaveExplorationSearch(unqualified, ExplorationSearchPolicy(), directory, "occupied-without-sensory-cue");
                SaveExplorationSearch(partial, ExplorationSearchPolicy(), directory, "target-partial-at-completion");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "qualified-failure");

                var attempts = new List<string> { failure.Natural.ToString() };
                foreach (int natural in new[] { 14, 7, 11, 13, 19 }) {
                    WorldCommit(sim, ExplorationSearchCommand(sim));
                    SearchAdvance(sim, 12);
                    var result = LastExplorationSearchResult(sim.Capture());
                    Require(result.Natural == natural, "The separately paid repeat changed the actual shared RNG sequence.");
                    attempts.Add(result.Natural.ToString());
                }
                var found = sim.Capture();
                var last = found.ExplorationSearch.Attempts.Last();
                var disclosed = SearchKnowledge(found, ExplorationSearcher);
                var projectionFound = sim.ObserveExplorationSearch(host, last.Id);
                Require(found.RuleClock == T(66) && found.ExplorationSearch.Attempts.Select(x => x.IntervalIndex)
                    .SequenceEqual(new long[] { 5, 6, 7, 8, 9, 10 })
                    && projectionFound.Status == ExplorationSearchViewStatus.Found && projectionFound.FoundLocation.Value.Equals(last.Candidate)
                    && disclosed.Evidence == ObservationEvidenceKind.Search && disclosed.CurrentLocationKnown && disclosed.HiddenAttemptId == ""
                    && witness.SameAs(SearchKnowledge(found, SearchWitness))
                    && !ObservationRules.CanSee(found, ExplorationSearcher, TestOnlyPolicy.ActorId)
                    && ObservationGeometry.LineOfEffectClear(ready, ExplorationSearcher, TestOnlyPolicy.ActorId)
                        == ObservationGeometry.LineOfEffectClear(found, ExplorationSearcher, TestOnlyPolicy.ActorId),
                    "Only the searcher must learn the actual position from the real sixth separately paid Search.");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "actual-find");

                WorldStep(sim, 1, 0);
                WorldAdvance(sim, 1);
                var moved = sim.Capture();
                var stale = SearchKnowledge(moved, ExplorationSearcher);
                Require(Body(sim).X == 2 && Body(sim).Y == 0 && stale.HasLastKnownLocation && !stale.CurrentLocationKnown
                    && stale.Evidence == ObservationEvidenceKind.Search && stale.LastKnownX == Q(1) && stale.LastKnownY == default
                    && stale.EvidenceAt == T(66) && stale.HiddenAttemptId == "" && witness.SameAs(SearchKnowledge(moved, SearchWitness)),
                    "Unseen movement must stale the Search evidence without tracking or restoring the old Hidden latch.");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "continued-unseen-movement");
                File.WriteAllLines(Path.Combine(directory, "exp04-search-disclosure.tsv"), new[] {
                    "first boundary 36 for qualified failure, empty and actual vacancy",
                    "paid shared RNG " + string.Join(",", attempts) + " actual find at " + found.RuleClock,
                    "unseen move to 2,0 at " + moved.RuleClock + " retains stale 1,0 only"
                });
            });

            cases.Add("exp04_exploration_search_due_effects_mode_change_and_remote_labor", () =>
            {
                var blind = CCApply("searcher-blind", "Blinded", ExplorationSearcher, new ConditionStamp(T(35)),
                    new ConditionStamp(T(33)));
                var blindedPolicy = ExplorationSearchPolicy(events: new[] { blind });
                var interrupted = ExplorationSearchReady(blindedPolicy);
                WorldCommit(interrupted, ExplorationSearchCommand(interrupted));
                SearchAdvance(interrupted, 3);
                WorldCommit(interrupted, CCCommand(interrupted, "searcher-blind", ExplorationSearcher));
                var blindState = interrupted.Capture();
                var lost = blindState.ExplorationSearch.Attempts.Single().End;
                Require(lost.At == T(33) && lost.Interruption == ExplorationSearchInterruption.VisualCapabilityLost
                    && SearchInterval(blindState).Action == WorldActionCommitment.Search
                    && blindState.ObservationActions.Count(x => x.Kind == ObservationActionKind.Search) == 0,
                    "Actual visual incapacity must interrupt without a roll or Action refund.");
                SaveExplorationSearch(interrupted, ExplorationSearchPolicy(events: new[] { blind }), directory, "blind-interrupted");
                SearchAdvance(interrupted, 9);
                Require(interrupted.Capture().ExplorationSearch.Pending == null
                    && interrupted.Capture().ObservationActions.Count(x => x.Kind == ObservationActionKind.Search) == 0,
                    "Recovery must not restart the interrupted Search.");

                var mode = ExplorationSearchReady();
                WorldCommit(mode, ExplorationSearchCommand(mode));
                SearchAdvance(mode, 3);
                RejectUnchanged(mode, host, IC(mode, CommandKind.BeginFixedEncounter, "unlawful"), "InvalidSharedCombatEntry");
                var before = mode.Capture();
                WorldCommit(mode, IC(mode, CommandKind.BeginFixedEncounter, id: "test.search-existing-tactical-reentry"));
                var entered = mode.Capture();
                var modeEnd = entered.ExplorationSearch.Attempts.Single().End;
                Require(modeEnd.At == T(33) && modeEnd.Interruption == ExplorationSearchInterruption.TacticalControlEntered
                    && entered.InventoryCombat && entered.Encounter.Id == before.Encounter.Id && entered.RandomState == before.RandomState
                    && !entered.Encounter.Order.Contains(ExplorationSearcher) && SearchInterval(entered).Action == WorldActionCommitment.Search
                    && entered.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead,
                    "Existing tactical re-entry must interrupt the off-roster search without restarting a conflict.");
                SaveExplorationSearch(mode, ExplorationSearchPolicy(), directory, "mode-interrupted");
                WorldCommit(mode, Tac(mode, CommandKind.EndFixedEncounter));
                Require(!mode.Capture().InventoryCombat && mode.Capture().ExplorationSearch.Pending == null
                    && mode.Capture().ObservationActions.Count(x => x.Kind == ObservationActionKind.Search) == 0,
                    "Tactical exit must not restart the old paid Search.");

                var poison = CCApply("searcher-poison", "Poisoned", ExplorationSearcher, new ConditionStamp(T(36)),
                    new ConditionStamp(T(30)));
                var workPolicy = ExplorationSearchPolicy(toolHp: 4, events: new[] { poison });
                var work = ExplorationSearchReady(workPolicy);
                var everyone = workPolicy.HostAuthority();
                WorldCommit(work, CCCommand(work, "searcher-poison", ExplorationSearcher));
                WorldCommit(work, ExplorationSearchCommand(work));
                ArchitectureCommit(work, everyone, IC(work, CommandKind.BeginWorldStep, "walk", actor: SearchWitness, x: 1));
                SearchAdvance(work, 1);
                ArchitectureCommit(work, everyone, IC(work, CommandKind.BeginWorldStep, "walk", actor: SearchWitness, x: 1));
                SearchAdvance(work, 1);
                ArchitectureCommit(work, everyone, IC(work, CommandKind.StartToolRepair, SharedCraftingFixture.ToolId, actor: SearchWitness));
                var advancing = SearchAdvance(work, 20);
                var complete = work.Capture();
                var actualWork = complete.RepairWork.Single(x => x.WorkerId == SearchWitness);
                Require(advancing.ReachedClock == T(36) && complete.RuleClock == T(36)
                    && LastExplorationSearchResult(complete).Selection == ObservationDieSelection.Normal
                    && actualWork.Work.Labor == T(4) && actualWork.Status == RepairWorkStatus.Working,
                    "Due Poisoned expiry must settle before the roll and unrelated real work must advance once to the yield.");
                SaveExplorationSearch(work, ExplorationSearchPolicy(toolHp: 4, events: new[] { poison }), directory,
                    "exact-expiry-and-remote-work");
                File.WriteAllLines(Path.Combine(directory, "exp04-search-boundaries.tsv"), new[] {
                    "loss of visual capability at " + lost.At, "lawful fixed-calendar mode change at " + modeEnd.At,
                    "due Poisoned expiry before ordinary Search at " + complete.RuleClock + " remote work " + actualWork.Work.Labor
                });
            });

            cases.Add("exp04_exploration_search_exact_restore_partition_and_integrity", () =>
            {
                var sim = ExplorationSearchReady();
                var initial = SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "restore-before");
                var declaration = ExplorationSearchCommand(sim);
                foreach (var run in new[] { sim, initial }) WorldCommit(run, declaration);
                Require(Bytes(sim).SequenceEqual(Bytes(initial)), "Declaration from the exact earlier save diverged.");
                SearchAdvance(sim, 2);
                var pending = SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "restore-partial");
                var partitioned = new Simulation(ExplorationSearchPolicy(), pending.Capture(), ExecutionProfile.Laboratory);
                var advance = IC(sim, CommandKind.AdvanceClock, x: 12, y: 1);
                foreach (var run in new[] { sim, pending }) WorldCommit(run, advance);
                SearchAdvance(partitioned, 1, 2);
                SearchAdvance(partitioned, 12);
                var a = LastExplorationSearchResult(sim.Capture());
                var b = LastExplorationSearchResult(partitioned.Capture());
                Require(Bytes(sim).SequenceEqual(Bytes(pending)) && a.At == b.At && a.Natural == b.Natural && a.Outcome == b.Outcome
                    && a.RandomAfter == b.RandomAfter && SameKnowledgeContent(sim.Capture(), partitioned.Capture()),
                    "Exact replay or mechanically equivalent clock partitions diverged.");
                var bytes = Bytes(sim);
                Require(sim.Execute(host, advance).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(sim)),
                    "A duplicate finishing advance repeated the roll or disclosure.");
                SaveExplorationSearch(sim, ExplorationSearchPolicy(), directory, "restore-completed");

                void RejectForgery(Simulation run, Action<Snapshot> alter, string expected)
                {
                    var altered = run.Capture();
                    alter(altered);
                    var codec = new SnapshotCodec();
                    string failure = null;
                    try { new Simulation(ExplorationSearchPolicy(), codec.Decode(codec.Encode(altered)), ExecutionProfile.Laboratory); }
                    catch (ArgumentException error) { failure = error.Message; }
                    Require(failure?.Contains(expected) == true, "Expected " + expected + ", got " + (failure ?? "accepted"));
                }

                var paying = ExplorationSearchReady();
                WorldCommit(paying, ExplorationSearchCommand(paying));
                RejectForgery(paying, state => state.WorldActivityIntervals = state.WorldActivityIntervals.Select(x =>
                    x.ActorId == ExplorationSearcher ? new WorldActivityIntervalRecord(x.CalendarId, x.ActorId, x.IntervalIndex) : x).ToArray(),
                    "lost its paid Action");
                RejectForgery(paying, state => {
                    var search = state.ExplorationSearch;
                    var paid = search.Pending;
                    state.ExplorationSearch = new ExplorationSearchRecord(search.Definition, new[] {
                        new ExplorationSearchAttempt(paid.Revision, paid.CommandId, paid.IntervalIndex, paid.StartedAt,
                            paid.DueAt.AddSeconds(1), paid.Candidate)
                    });
                }, "declaration or interval");
                RejectForgery(sim, state => {
                    var search = state.ExplorationSearch;
                    var done = search.Attempts.Single();
                    var end = done.End;
                    state.ExplorationSearch = new ExplorationSearchRecord(search.Definition, new[] {
                        done.Finish(new ExplorationSearchEnd(end.Status, end.Interruption, end.Revision, end.CommandId, end.At,
                            "test.forged-observation", end.CueId, end.HideId))
                    });
                }, "does not bind its actual completion");
                RejectForgery(sim, state => {
                    var search = state.ExplorationSearch;
                    var done = search.Attempts.Single();
                    var end = done.End;
                    state.ExplorationSearch = new ExplorationSearchRecord(search.Definition, new[] {
                        done.Finish(new ExplorationSearchEnd(end.Status, end.Interruption, end.Revision, end.CommandId, end.At,
                            end.ObservationId, end.CueId, "test.forged-hide"))
                    });
                }, "no genuine cue and observer-specific Hide");
                RejectForgery(sim, state => {
                    state.ObserverKnowledge = state.ObserverKnowledge.Select(k => k.ObserverId == ExplorationSearcher
                        && k.TargetId == TestOnlyPolicy.ActorId
                        ? new ObserverKnowledgeRecord(k.ObserverId, k.TargetId, true, true, Q(1), Q(0),
                            ObservationEvidenceKind.Search, state.RuleClock, state.Revision)
                        : k).ToArray();
                }, "InvalidSharedWorldReplay");
                var d = sim.Capture().ExplorationSearch.Definition;
                Throws<ArgumentException>(() => new ExplorationSearchDefinition(d.SourceRevision, "test.false-director", d.CueId,
                    d.SearcherId, d.ConcealedActorId, d.Anchor, d.CueCandidate, d.Sign, d.Occlusion));
            });

            cases.Add("exp04_exploration_search_independent_wire_legacy_and_profile_controls", () =>
            {
                var legacy = ExplorationSearchReady(ExplorationSearchPolicy(false));
                var modern = ExplorationSearchReady();
                var original = legacy.Capture();
                var newState = modern.Capture();
                var codec = new SnapshotCodec();
                byte[] oldBytes = codec.Encode(original);
                byte[] newBytes = codec.Encode(newState);
                Require(BitConverter.ToInt32(oldBytes, 4) == 51 && BitConverter.ToInt32(newBytes, 4) == 91
                    && codec.Decode(newBytes).SchemaVersion == 51 && codec.Decode(newBytes).WireSchemaVersion == 91
                    && codec.Decode(oldBytes).ExplorationSearch == null && codec.Decode(oldBytes).WireSchemaVersion == 51,
                    "The codec must preserve distinct envelope identity and the actual base feature selection.");
                Throws<ArgumentException>(() => new Simulation(ExplorationSearchPolicy(false), newState, ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(ExplorationSearchPolicy(), original, ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(ExplorationSearchPolicy(), newState, ExecutionProfile.Release));
                RejectUnchanged(legacy, host, ExplorationSearchCommand(legacy), "ObservationActionRequiresTacticalCombat");
                Require(oldBytes.SequenceEqual(codec.Encode(codec.Decode(oldBytes))), "The original profile changed canonical bytes.");

                var forged = original.Copy();
                forged.WorldActivityIntervals = forged.WorldActivityIntervals.Select(x => x.ActorId == ExplorationSearcher
                    ? x.PaySearch("test.unrepresentable-new-commitment", forged.Revision) : x).ToArray();
                Throws<ArgumentException>(() => codec.Encode(forged));
                var unsupported = ExplorationSearchPolicy(false);
                unsupported.Initial();
                Throws<InvalidOperationException>(() => unsupported.EnableExplorationSearch());

                SaveExplorationSearch(legacy, ExplorationSearchPolicy(false), directory, "legacy-schema51-control");
                SaveExplorationSearch(modern, ExplorationSearchPolicy(), directory, "wire91-control");
            });
        }
    }
}
#endif
