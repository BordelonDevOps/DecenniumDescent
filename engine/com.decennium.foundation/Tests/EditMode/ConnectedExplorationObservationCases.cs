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
        private static TestOnlySharedWorldPolicy ConnectedObservationPolicy(params ConditionFixtureEvent[] events)
            => SurprisePolicy(SurpriseAwareness.Warned, events.Length == 0 ? null : new ConditionCombatFixture(events))
                .EnableConnectedExplorationObservation();

        private static void ReachConnectedObservationWindow(Simulation sim)
        {
            PlanWalk(sim, -1, 0, ExplorationSearcher);
            PlanWalk(sim, 0, -1, ExplorationSearcher);
            for (int i = 0; i < 3; i++) PlanWalk(sim, 0, -1);
            WorldAdvance(sim, 2);
            Require(sim.Capture().RuleClock == T(11610) && Body(sim).X == 1 && Body(sim).Y == 0
                && Body(sim, ExplorationSearcher).X == 3 && Body(sim, ExplorationSearcher).Y == 2,
                "Actual ordinary movement did not reach the authored observation window.");
        }

        private static Simulation ConnectedObservationReady(params ConditionFixtureEvent[] events)
        {
            var sim = LaterPrepared(ConnectedObservationPolicy(events));
            ReachConnectedObservationWindow(sim);
            return sim;
        }

        private static Simulation SaveConnectedObservation(Simulation sim, string directory, string name,
            params ConditionFixtureEvent[] events)
            => SaveBill(sim, ConnectedObservationPolicy(events), directory, "exp04-connected-observation-" + name);

        private static ObservationActionRecord PrepareConnectedConcealment(Simulation sim, string directory = null)
        {
            FinishPaidHide(sim);
            var first = OrdinaryHideRoll(sim);
            var firstAttempt = LastHideAttempt(sim);
            var prior = sim.Capture();
            Require(first.Natural == 9 && firstAttempt.PaidStart == 3870 && first.At == T(11616)
                && WorldLedger(sim).LastStart == 3872 && !WorldLedger(sim).ActionSpent
                && prior.ObservationHideResults.Single().ObserverId == ExplorationSearcher
                && !prior.ObservationHideResults.Single().HiddenEstablished
                && ObservationRules.CanSee(prior, SaleBuyer, PlanHero),
                "The initial genuine roll should fail against the companion while the independent buyer sees.");
            if (directory != null) SaveConnectedObservation(sim, directory, "primary-failure");

            PlanWalk(sim, 1, 0);
            var moved = sim.Capture();
            Require(moved.RuleClock == T(11622) && moved.ExplorationHide.LatestRelocation.At == T(23235, 2)
                && !ObservationRules.CanSee(moved, ExplorationSearcher, PlanHero) && !ObservationRules.CanSee(moved, SaleBuyer, PlanHero),
                "Actual movement did not supply the selected alternate position.");
            FinishPaidHide(sim);
            var alternate = OrdinaryHideRoll(sim);
            Require(alternate.Total == 12 && alternate.At == T(11628) && LastHideAttempt(sim).Relocation.At == T(23235, 2)
                && new[] { ExplorationSearcher, SaleBuyer }.All(x => ObservationRules.HiddenTo(sim.Capture(), x, PlanHero))
                && !ObservationRules.HiddenTo(sim.Capture(), LaterDefender, PlanHero),
                "The alternate Stealth result must apply to the two selected observers only.");
            if (directory != null) SaveConnectedObservation(sim, directory, "alternate-hidden");

            PlanWalk(sim, -1, 0);
            var returned = sim.Capture();
            Require(returned.RuleClock == T(11634) && SearchKnowledge(returned, ExplorationSearcher).HiddenAttemptId == alternate.Id
                && !ObservationRules.CanSee(returned, ExplorationSearcher, PlanHero)
                && !ObservationRules.HiddenTo(returned, SaleBuyer, PlanHero) && ObservationRules.CanSee(returned, SaleBuyer, PlanHero),
                "The unseen return must preserve the companion's Hide and allow the buyer's independent sight.");
            if (directory != null) SaveConnectedObservation(sim, directory, "returned-unseen-to-searcher");
            return alternate;
        }

        private static void ReturnToConnectedApproach(Simulation sim)
        {
            for (int i = 0; i < 3; i++) PlanWalk(sim, 0, 1);
            Require(Body(sim).X == 1 && Body(sim).Y == 3, "Actual movement did not reach the later engagement approach.");
        }

        private static void AddConnectedExplorationObservationCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp04_connected_observation_initialization_stage_and_real_geometry", () =>
            {
                var policy = ConnectedObservationPolicy();
                var initial = PortableWorld(policy);
                var start = initial.Capture();
                var predecessor = SurprisePolicy(SurpriseAwareness.Warned).Initial();
                Require(start.SchemaVersion == 90 && start.WireSchemaVersion == 93 && start.TestOnly
                    && start.Actors.Select(x => (x.Id, x.X, x.Y)).SequenceEqual(predecessor.Actors.Select(x => (x.Id, x.X, x.Y)))
                    && start.Lives.Select(x => (x.ActorId, x.Hp, x.Dead)).SequenceEqual(predecessor.Lives.Select(x => (x.ActorId, x.Hp, x.Dead)))
                    && start.Clubs.Select(x => (x.Id, x.HeldBy)).SequenceEqual(predecessor.Clubs.Select(x => (x.Id, x.HeldBy)))
                    && start.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                        .SequenceEqual(predecessor.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                    && start.RandomState == predecessor.RandomState && start.ExplorationHide.Attempts.Count == 0
                    && start.ExplorationSearch.Attempts.Count == 0 && start.ObservationMapWidth == 5
                    && start.ObservationCells.Single().BlocksSight && !start.ObservationCells.Single().BlocksEffect
                    && !start.ObservationCells.Single().BlocksMovement && !TestOnlyPolicy.Walkable(2, 1),
                    "The approved overlay changed an existing body, source object or movement/effect channel.");
                var earlyHide = ExplorationHideCommand(initial);
                var earlySearch = ExplorationSearchCommand(initial);
                foreach (var command in new[] { earlyHide, earlySearch }) {
                    Require(initial.QueryCommand(host, command).Code == "ConnectedObservationStageClosed",
                        "A premature ordinary declaration was advertised.");
                    RejectUnchanged(initial, host, command, "ConnectedObservationStageClosed");
                }
                SaveConnectedObservation(initial, directory, "initial-empty");

                var sim = LaterPrepared(policy);
                var prepared = sim.Capture();
                Require(prepared.LaterEncounter.FirstExit.ClosedAt == T(15)
                    && prepared.HavenSales.Single().Basis.GoodsLotId == "TEST_ONLY.mining.unit.iron"
                    && prepared.HavenSales.Single().UpdatedAt == T(5436) && prepared.HavenSales.Single().PaymentCopper == 2
                    && prepared.HavenMealPurchases.Single().PaymentCopper == 2
                    && prepared.ExpeditionBills.Single().Status == ExpeditionBillStatus.Reconciled
                    && prepared.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                    && prepared.ObservationActions.Length == 0, "The actual connected preparation changed authority or prior expenditure.");
                ReachConnectedObservationWindow(sim);
                var state = sim.Capture();
                var d = state.ExplorationSearch.Definition;
                Require(WorldTiming.ForActor(state, PlanHero).Id == state.WorldSchedule.Id
                    && WorldTiming.ForActor(state, ExplorationSearcher) == null && !WorldLedger(sim).ActionSpent
                    && SearchInterval(state).Action == WorldActionCommitment.None && SearchInterval(state).IntervalIndex == 1935
                    && !ObservationRules.CanSee(state, ExplorationSearcher, PlanHero) && ObservationRules.CanSee(state, SaleBuyer, PlanHero)
                    && !ObservationRules.HiddenTo(state, ExplorationSearcher, PlanHero)
                    && state.ExplorationHide.Definition.WitnessId == SaleBuyer && d.CueId == ConnectedExplorationObservation.VisibleFringe,
                    "The ordinary window lost the two existing owners or observer-specific physical facts.");
                var wrongActor = new Authority("TEST_ONLY.observer-only", new[] { ExplorationSearcher });
                var ownHide = ExplorationHideCommand(sim);
                RejectUnchanged(sim, wrongActor, ownHide, "NotAuthorized");
                Require(sim.QueryCommand(host, ownHide).Admissible && sim.QueryCommand(host, ExplorationSearchCommand(sim)).Admissible,
                    "Both admitted original-ledger procedures must be available after the actual return.");
                SaveConnectedObservation(sim, directory, "before-observation");
            });

            cases.Add("exp04_connected_observation_paid_hide_search_combat_and_byte_replay", () =>
            {
                var sim = ConnectedObservationReady();
                var concealment = PrepareConnectedConcealment(sim, directory);
                var search = ExplorationSearchCommand(sim, id: "test.connected-search");
                var before = sim.Capture();
                WorldCommit(sim, search);
                var pending = sim.Capture();
                var interval = SearchInterval(pending);
                Require(interval.Action == WorldActionCommitment.Search && interval.ActionReference == search.Id
                    && pending.RandomState == before.RandomState && pending.RuleClock == before.RuleClock
                    && !WorldLedger(sim).ActionSpent, "Paid Search did not use only the companion's real ordinary Action.");
                var replay = SaveConnectedObservation(sim, directory, "paid-search");
                foreach (var run in new[] { sim, replay }) {
                    SearchAdvance(run, 18);
                    var found = run.Capture();
                    var result = LastExplorationSearchResult(found);
                    var attempt = found.ExplorationSearch.Attempts.Single();
                    var buyer = SearchKnowledge(found, SaleBuyer);
                    Require(found.RuleClock == T(11640) && result.Natural == 15 && result.WordsConsumed == 1
                        && result.Outcome == ObservationActionOutcome.SearchFound && attempt.End.HideId == concealment.Id
                        && !ObservationRules.CanSee(found, ExplorationSearcher, PlanHero)
                        && ObservationRules.LocationKnown(found, ExplorationSearcher, PlanHero)
                        && !ObservationRules.HiddenTo(found, ExplorationSearcher, PlanHero)
                        && buyer.Evidence != ObservationEvidenceKind.Search && ObservationRules.CanSee(found, SaleBuyer, PlanHero)
                        && SearchInterval(found).Action == WorldActionCommitment.None
                        && run.ObserveExplorationSearch(host, attempt.Id).Status == ExplorationSearchViewStatus.Found,
                        "The actual paid Search failed to use the ordinary Stealth record without granting sight or other knowledge.");
                    Require(run.Execute(host, search).Outcome == Outcome.Duplicate, "A duplicate Search repeated actual payment or disclosure.");
                    RejectUnchanged(run, host, new Command(search.Id, search.Actor, search.ExpectedRevision, search.Kind,
                        search.Target, 0, 0), "CommandIdConflict");
                    ReturnToConnectedApproach(run);
                    var beforeEntry = run.Capture();
                    var entry = EnterLater(run);
                    Require(entry.Draws[0].RandomBefore == beforeEntry.RandomState && entry.Draws[1].RandomAfter == run.Capture().RandomState
                        && run.Capture().SurpriseEntry.Binding.Outcome == SurpriseAwareness.Warned
                        && run.Capture().SurpriseEntry.Decision.Revision == entry.ArrivalRevision
                        && WorldTiming.ForActor(run.Capture(), PlanHero).Id == entry.Epoch.Id
                        && WorldTiming.ForActor(run.Capture(), ExplorationSearcher) == null,
                        "Genuine later entry must use the actual post-observation RNG and independent Warned authority.");
                    var oldHide = new Command("test.connected-old-ordinary-marker", PlanHero, run.Capture().Revision,
                        CommandKind.Hide, beforeEntry.WorldSchedule.MarkerId(beforeEntry.ExplorationHide.Attempts[0].PaidStart));
                    Require(!run.QueryCommand(host, oldHide).Admissible && run.Execute(host, oldHide).Outcome == Outcome.Rejected,
                        "An old ordinary marker was admitted by the later tactical command path.");
                    if (run == sim) SaveConnectedObservation(run, directory, "actual-later-entry");
                    FinishLaterFight(run, false);
                    PlanWalk(run, 1, 0);
                    var continued = run.Capture();
                    Require(!continued.InventoryCombat && continued.ClosedEncounters.Length == 2 && Body(run).X == 1
                        && continued.HavenSales.Single().PaymentCopper == 2
                        && continued.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(before.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                        && continued.HavenMealPurchases.Single().Id == before.HavenMealPurchases.Single().Id
                        && continued.ExpeditionBills.Single().Id == before.ExpeditionBills.Single().Id
                        && continued.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                        && WorldTiming.ForActor(continued, PlanHero).Id == entry.Epoch.Id
                        && continued.ExplorationHide.Attempts[0].CalendarId == "world.fixed-calendar"
                        && continued.ExplorationHide.Attempts[0].PaidStart == 3870
                        && continued.ExplorationSearch.Attempts.Single().End.HideId == concealment.Id,
                        "Combat and ordinary continuation did not preserve the actual earlier resources and observation provenance.");
                    RejectUnchanged(run, host, ExplorationHideCommand(run), "ConnectedObservationStageClosed");
                    RejectUnchanged(run, host, ExplorationSearchCommand(run), "ConnectedObservationStageClosed");
                    Require(run.Execute(host, search).Outcome == Outcome.Duplicate,
                        "A historical observation duplicate must remain idempotent after later exit.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Identical cross-mode save/replay did not produce exact bytes.");
                SaveConnectedObservation(sim, directory, "continued-after-real-combat");
            });

            AddConnectedObservationBoundaryCases(cases, directory);
            AddConnectedObservationIntegrityCases(cases, directory);
            cases.Add("exp04_connected_observation_retired_search_ledger_survives_actual_reinforcement", () =>
            {
                var sim = ConnectedObservationReady();
                var hidden = PrepareConnectedConcealment(sim);
                WorldCommit(sim, ExplorationSearchCommand(sim));
                SearchAdvance(sim, 18);
                var paidSearch = sim.Capture().ExplorationSearch.Attempts.Single();
                var originalCalendar = sim.Capture().WorldSchedule;
                Require(paidSearch.End.HideId == hidden.Id && paidSearch.End.At == T(11640),
                    "The historical Search was not genuinely paid and resolved.");
                PlanWalk(sim, 0, 1, ExplorationSearcher);
                StageReinforcingCompanion(sim);
                ReturnToConnectedApproach(sim);
                var entry = EnterLater(sim);
                LaterCommit(sim, ReinforcementCommand(sim));
                EndReinforcementTurn(sim);
                var saved = SaveConnectedObservation(sim, directory, "reinforcement-before-admission");
                foreach (var run in new[] { sim, saved }) {
                    EndReinforcementTurn(run);
                    var admitted = run.Capture();
                    var phase = admitted.Reinforcement.Admission.Phase;
                    var recorded = admitted.ExplorationSearch.Attempts.Single();
                    Require(admitted.InventoryCombat && admitted.Encounter.Order.Contains(ExplorationSearcher)
                        && phase.Epoch.Order.Contains(ExplorationSearcher)
                        && WorldTiming.ForActor(admitted, ExplorationSearcher).Id == phase.Epoch.Id
                        && WorldTiming.FindEpoch(admitted, originalCalendar.Id).Id == originalCalendar.Id
                        && !admitted.WorldActivityIntervals.Any(x => x.ActorId == ExplorationSearcher)
                        && recorded.CommandId == paidSearch.CommandId && recorded.IntervalIndex == paidSearch.IntervalIndex
                        && recorded.End.ObservationId == paidSearch.End.ObservationId && recorded.End.HideId == hidden.Id
                        && admitted.ExplorationSearch.Pending == null && admitted.LaterEncounter.Entry.ArrivalRevision == entry.ArrivalRevision
                        && run.ObserveExplorationSearch(host, recorded.Id).Status == ExplorationSearchViewStatus.Found,
                        "Real admission must retire the old ledger while preserving actual historical Search and its projection.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(saved)), "Saving before actual admission changed replay across the roster change.");
                SaveConnectedObservation(sim, directory, "reinforcement-search-history-retained");
                File.WriteAllLines(Path.Combine(directory, "exp04-connected-observation-reinforcement.tsv"), new[] {
                    "historical Search " + paidSearch.CommandId + " paid in " + originalCalendar.Id + " interval " + paidSearch.IntervalIndex,
                    "actual admission " + sim.Capture().RuleClock + " current companion calendar " + WorldTiming.ForActor(sim.Capture(), ExplorationSearcher).Id,
                    "old activity row retired, exact history retained and replayed"
                });
            });
        }

        private static void AddConnectedObservationBoundaryCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp04_connected_observation_coincident_receipt_order_and_private_views", () =>
            {
                var forward = ConnectedObservationReady();
                var concealment = PrepareConnectedConcealment(forward);
                var reverse = SaveConnectedObservation(forward, directory, "before-coincident");
                var absent = new Simulation(ConnectedObservationPolicy(), forward.Capture(), ExecutionProfile.Laboratory);

                WorldCommit(forward, ExplorationHideCommand(forward));
                WorldCommit(forward, ExplorationSearchCommand(forward));
                WorldCommit(reverse, ExplorationSearchCommand(reverse));
                WorldCommit(reverse, ExplorationHideCommand(reverse));
                WorldCommit(absent, ExplorationHideCommand(absent));
                WorldCommit(absent, ExplorationSearchCommand(absent, x: 0, y: 0));
                foreach (var sim in new[] { forward, reverse, absent })
                    Require(SearchAdvance(sim, 18).ReachedClock == T(11640), "A private result changed the shared clock yield.");
                var a = forward.Capture();
                var b = reverse.Capture();
                var hide = OrdinaryHideRoll(forward);
                var reversedHide = OrdinaryHideRoll(reverse);
                var sa = LastExplorationSearchResult(a);
                var sb = LastExplorationSearchResult(b);
                Require(hide.Natural == 15 && sa.Natural == 4 && sa.RandomBefore == hide.RandomAfter
                    && a.ExplorationSearch.Attempts.Single().End.HideId == hide.Id
                    && sa.Outcome == ObservationActionOutcome.SearchNoFinding && sa.Revision == hide.Revision
                    && sb.Natural == 15 && reversedHide.Natural == 4 && reversedHide.RandomBefore == sb.RandomAfter
                    && b.ExplorationSearch.Attempts.Single().End.HideId == concealment.Id
                    && sb.Outcome == ObservationActionOutcome.SearchFound && sb.Revision == reversedHide.Revision
                    && !ObservationRules.HiddenTo(b, ExplorationSearcher, PlanHero),
                    "Receipt order did not preserve the actual active Hide and RNG at each same-boundary comparison.");
                var aSearch = a.ExplorationSearch.Attempts.Single();
                var cSearch = absent.Capture().ExplorationSearch.Attempts.Single();
                var noFinding = forward.ObserveExplorationSearch(host, aSearch.Id);
                var noCheck = absent.ObserveExplorationSearch(host, cSearch.Id);
                Require(noFinding.Status == ExplorationSearchViewStatus.NoFinding && noFinding.AttemptId == noCheck.AttemptId
                    && noFinding.Status == noCheck.Status && noFinding.StartedAt == noCheck.StartedAt
                    && noFinding.DueAt == noCheck.DueAt && noFinding.EndedAt == noCheck.EndedAt
                    && noFinding.FoundLocation == null && noCheck.FoundLocation == null
                    && LastExplorationSearchResult(absent.Capture()).WordsConsumed == 0
                    && HidePublic(forward.ObserveExplorationHide(host, LastHideAttempt(forward).Id))
                        == HidePublic(absent.ObserveExplorationHide(host, LastHideAttempt(absent).Id)),
                    "Public views distinguished a failed comparison from the equal no-finding control.");
                var observer = new Authority("TEST_ONLY.connected-buyer-observer", new[] { SaleBuyer });
                Require(forward.ObserveExplorationSearch(observer, aSearch.Id) == null
                    && forward.ObserveExplorationHide(observer, LastHideAttempt(forward).Id) == null,
                    "An independent buyer received the hider or searcher's private procedure view.");
                SaveConnectedObservation(forward, directory, "hide-first");
                SaveConnectedObservation(reverse, directory, "search-first");
                SaveConnectedObservation(absent, directory, "no-finding-control");
                var codec = new SnapshotCodec();
                var reordered = forward.Capture();
                Array.Reverse(reordered.ObservationActions, reordered.ObservationActions.Length - 2, 2);
                Throws<ArgumentException>(() => codec.Encode(reordered));
                var wrongHideLink = forward.Capture();
                var falseLink = new ExplorationSearchEnd(aSearch.End.Status, aSearch.End.Interruption, aSearch.End.Revision,
                    aSearch.End.CommandId, aSearch.End.At, aSearch.End.ObservationId, aSearch.End.CueId, "forged.hide-link");
                wrongHideLink.ExplorationSearch = new ExplorationSearchRecord(a.ExplorationSearch.Definition, new[] { aSearch.Finish(falseLink) });
                Throws<ArgumentException>(() => codec.Encode(wrongHideLink));
                File.WriteAllLines(Path.Combine(directory, "exp04-connected-observation-coincident.tsv"), new[] {
                    "Hide first " + hide.Natural + " then Search " + sa.Natural + " against " + aSearch.End.HideId,
                    "Search first " + sb.Natural + " against " + concealment.Id + " then Hide " + reversedHide.Natural,
                    "both exact endpoints " + a.RuleClock
                });
            });

            cases.Add("exp04_connected_observation_real_early_entry_and_failed_entry_control", () =>
            {
                var blindness = CCApply("connected-defender-blind-at-arrival", "Blinded", LaterDefender,
                    at: new ConditionStamp(T(23281, 2)));
                var events = new[] { blindness };
                var sim = ConnectedObservationReady(events);
                ReturnToConnectedApproach(sim);
                SearchAdvance(sim, 12);
                Require(sim.Capture().RuleClock == T(11640) && SearchInterval(sim.Capture()).Action == WorldActionCommitment.None,
                    "The actual early-entry branch lost its unspent companion window.");
                var declaration = ExplorationSearchCommand(sim, id: "test.connected-search-before-entry");
                WorldCommit(sim, declaration);
                var saved = SaveConnectedObservation(sim, directory, "early-entry-search-paid", events);
                foreach (var run in new[] { sim, saved }) {
                    LaterCommit(run, LaterApproach(run));
                    LaterCommit(run, LaterAdvance(run, 1, 2));
                }
                var rngBeforeEntry = sim.Capture().RandomState;
                var advancing = LaterAdvance(sim);
                var accepted = LaterCommit(sim, advancing);
                var actual = sim.Capture();
                var entry = actual.LaterEncounter.Entry;
                var paid = SearchInterval(actual);
                var end = actual.ExplorationSearch.Attempts.Single().End;
                Require(accepted.TacticalDecisionAt == T(23283, 2) && actual.InventoryCombat && end.At == T(23283, 2)
                    && end.Status == ExplorationSearchStatus.Interrupted && end.Interruption == ExplorationSearchInterruption.TacticalControlEntered
                    && end.CommandId == entry.ArrivalCommandId && end.Revision == entry.ArrivalRevision && end.ObservationId == ""
                    && paid.ActionReference == declaration.Id && paid.Action == WorldActionCommitment.Search
                    && actual.ObservationActions.Length == 0 && entry.Draws[0].RandomBefore == rngBeforeEntry
                    && entry.Draws[1].RandomAfter == actual.RandomState,
                    "Early genuine entry must interrupt off-roster Search in the entry transaction with only actual initiative draws.");
                Require(sim.Execute(host, advancing).Outcome == Outcome.Duplicate
                    && sim.Execute(host, declaration).Outcome == Outcome.Duplicate, "Duplicate entry or Search replayed resources.");
                SaveConnectedObservation(sim, directory, "search-interrupted-by-actual-entry", events);
                var wrongTerminal = sim.Capture();
                var receipt = wrongTerminal.Receipts.Single(x => x.Revision == end.Revision - 1);
                var forgedEnd = new ExplorationSearchEnd(end.Status, end.Interruption, receipt.Revision, receipt.Id, end.At);
                wrongTerminal.ExplorationSearch = new ExplorationSearchRecord(actual.ExplorationSearch.Definition,
                    new[] { actual.ExplorationSearch.Attempts.Single().Finish(forgedEnd) });
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(wrongTerminal));
                FinishLaterFight(sim, false);
                Require(sim.Capture().ExplorationSearch.Pending == null && sim.Capture().ObservationActions.Length == 0
                    && !sim.Capture().InventoryCombat, "Returning to ordinary mode revived interrupted Search.");
                SaveConnectedObservation(sim, directory, "ordinary-after-interruption", events);

                LaterCommit(saved, CCCommand(saved, "connected-defender-blind-at-arrival", LaterDefender));
                var failed = LaterCommit(saved, LaterAdvance(saved));
                var stillOrdinary = saved.Capture();
                Require(failed.Code == "LaterEncounterAwarenessUnavailable" && !stillOrdinary.InventoryCombat
                    && stillOrdinary.LaterEncounter.Entry == null && stillOrdinary.ExplorationSearch.Pending != null
                    && SearchInterval(stillOrdinary).Action == WorldActionCommitment.Search
                    && stillOrdinary.RandomState == rngBeforeEntry,
                    "A genuine failed contact must leave ordinary Search pending without initiative or a Search draw.");
                var ended = SearchAdvance(saved, 18);
                Require(ended.ReachedClock == T(11646) && saved.Capture().ExplorationSearch.Attempts.Single().End.Status == ExplorationSearchStatus.Completed
                    && LastExplorationSearchResult(saved.Capture()).WordsConsumed == 0
                    && saved.Capture().RandomState == rngBeforeEntry,
                    "The prior failed contact prevented the pending ordinary Search from resolving normally.");
                SaveConnectedObservation(saved, directory, "failed-contact-search-completed", events);
            });

            cases.Add("exp04_connected_observation_due_effects_and_compatible_remote_work", () =>
            {
                var poisoned = CCApply("connected-hider-poison", "Poisoned", PlanHero, new ConditionStamp(T(11616)),
                    new ConditionStamp(T(11610)));
                var stunned = CCApply("connected-hider-stun", "Stunned", PlanHero, new ConditionStamp(T(11615)),
                    new ConditionStamp(T(11613)));
                var events = new[] { poisoned, stunned };
                var sim = ConnectedObservationReady(events);
                WorldCommit(sim, CCCommand(sim, "connected-hider-poison", PlanHero));
                WorldCommit(sim, ExplorationHideCommand(sim));
                var interrupted = SaveConnectedObservation(sim, directory, "hide-paid-before-effect", events);
                WorldStep(sim, 0, 1, actor: ExplorationSearcher);
                SearchAdvance(sim, 1);
                FarmWork(sim, CommandKind.PlantCrop);
                var yielded = SearchAdvance(sim, 18);
                var ended = sim.Capture();
                var work = ReinforcementPlanting(ended);
                Require(yielded.ReachedClock == T(11616) && OrdinaryHideRoll(sim).Selection == ObservationDieSelection.Normal
                    && work.Progress == T(5) && work.Status == CropWorkStatus.Working
                    && WorldLedger(sim).LastStart == 3872 && !WorldLedger(sim).ActionSpent
                    && SearchInterval(ended).Action != WorldActionCommitment.Search,
                    "The due Poisoned expiry, genuine Start and independent crop labor did not preserve their order and shared time.");
                SaveConnectedObservation(sim, directory, "expiry-and-real-remote-work", events);
                FarmWork(sim, CommandKind.PauseCrop);
                WorldStep(sim, 0, -1, actor: ExplorationSearcher);
                SearchAdvance(sim, 6);
                Require(Body(sim, ExplorationSearcher).X == 3 && Body(sim, ExplorationSearcher).Y == 2
                    && ReinforcementPlanting(sim.Capture()).Status == CropWorkStatus.Paused
                    && ReinforcementPlanting(sim.Capture()).Progress == T(5), "Remote labor was not paused before the actual walk to Search.");
                WorldCommit(sim, ExplorationSearchCommand(sim));
                SearchAdvance(sim, 18);
                Require(LastExplorationSearchResult(sim.Capture()).WordsConsumed == 0,
                    "The worker's later paid Search manufactured a prior concealment check.");
                SaveConnectedObservation(sim, directory, "remote-job-paused-before-search", events);

                SearchAdvance(interrupted, 3);
                WorldCommit(interrupted, CCCommand(interrupted, "connected-hider-stun", PlanHero));
                Require(LastHideAttempt(interrupted).End.Interruption == ExplorationHideInterruption.ActionCapabilityLost
                    && LastHideAttempt(interrupted).End.At == T(11613) && WorldLedger(interrupted).ActionSpent
                    && interrupted.Capture().ObservationActions.Length == 0,
                    "An actual condition did not interrupt the pending Hide without refunding payment.");
                SaveConnectedObservation(interrupted, directory, "hide-condition-interruption", events);
                SearchAdvance(interrupted, 9);
                Require(interrupted.Capture().ObservationActions.Length == 0 && interrupted.Capture().ExplorationHide.Pending == null,
                    "Recovery resumed an already-interrupted Hide.");
            });
        }

        private static void AddConnectedObservationIntegrityCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp04_connected_observation_wire93_profile_and_historical_integrity", () =>
            {
                var codec = new SnapshotCodec();
                var sim = ConnectedObservationReady();
                var hide = ExplorationHideCommand(sim, "test.connected-hide-integrity");
                WorldCommit(sim, hide);
                var replay = SaveConnectedObservation(sim, directory, "pending-hide");
                SearchAdvance(sim, 5, 2);
                SearchAdvance(replay, 5, 2);
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Identical pending Hide histories changed save bytes.");
                var partial = SaveConnectedObservation(sim, directory, "partial-hide");
                SearchAdvance(sim, 18);
                SearchAdvance(partial, 3, 2);
                SearchAdvance(partial, 2);
                var actual = OrdinaryHideRoll(sim);
                var divided = OrdinaryHideRoll(partial);
                Require(sim.Capture().RuleClock == partial.Capture().RuleClock && actual.Natural == divided.Natural
                    && actual.RandomAfter == divided.RandomAfter && WorldLedger(sim).LastStart == WorldLedger(partial).LastStart
                    && !WorldLedger(partial).ActionSpent, "Equivalent ordinary advances changed mechanical outcomes.");
                Require(sim.Execute(host, hide).Outcome == Outcome.Duplicate, "A historical Hide duplicate repeated the Action.");
                RejectUnchanged(sim, host, new Command(hide.Id, hide.Actor, hide.ExpectedRevision, hide.Kind,
                    "forged.marker"), "CommandIdConflict");

                var completed = sim.Capture();
                var attempt = completed.ExplorationHide.Attempts.Single();
                var component = completed.ExplorationHide;
                void Reject(Snapshot value) => Throws<ArgumentException>(() => codec.Encode(value));
                void ReplaceAttempt(Snapshot value, ExplorationHideAttempt replacement)
                    => value.ExplorationHide = new ExplorationHideRecord(component.Definition, component.LatestRelocation, new[] { replacement });

                var forgedStage = sim.Capture();
                forgedStage.CharterAttempt = null;
                Reject(forgedStage);
                var forgedOwner = sim.Capture();
                ReplaceAttempt(forgedOwner, new ExplorationHideAttempt(attempt.Revision, attempt.CommandId, "TEST_ONLY.later-calendar",
                    attempt.PaidStart, attempt.StartedAt, attempt.DueAt, attempt.Anchor, attempt.Relocation, attempt.End));
                Reject(forgedOwner);
                var forgedMarker = sim.Capture();
                ReplaceAttempt(forgedMarker, new ExplorationHideAttempt(attempt.Revision, attempt.CommandId, attempt.CalendarId,
                    3868, T(11604), T(11610), attempt.Anchor));
                Reject(forgedMarker);
                var forgedObserver = sim.Capture();
                var result = forgedObserver.ObservationHideResults.Single();
                forgedObserver.ObservationHideResults = new[] {
                    new ObservationHideResultRecord(result.AttemptId, LaterDefender, result.ObserverX, result.ObserverY,
                        result.Dc, result.Degree, result.HiddenEstablished) };
                Reject(forgedObserver);
                var missingSearch = sim.Capture();
                missingSearch.ExplorationSearch = null;
                Reject(missingSearch);
                var missingHide = sim.Capture();
                missingHide.ExplorationHide = null;
                Reject(missingHide);
                var movementBlock = sim.Capture();
                movementBlock.ObservationCells = new[] { new ObservationMapCellRecord(2, 1, true, false, true, false) };
                Reject(movementBlock);
                var effectBlock = sim.Capture();
                effectBlock.ObservationCells = new[] { new ObservationMapCellRecord(2, 1, true, true, false, false) };
                Reject(effectBlock);
                var unrelated = SurprisePolicy(SurpriseAwareness.Warned);
                var raw = Bytes(sim);
                Require(BitConverter.ToInt32(raw, 4) == 93 && codec.Decode(raw).SchemaVersion == 90
                    && codec.Encode(codec.Decode(raw)).SequenceEqual(raw), "Wire93 did not retain exact base90 bytes.");
                Throws<ArgumentException>(() => new Simulation(unrelated, completed, ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(ConnectedObservationPolicy(), unrelated.Initial(), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(ConnectedObservationPolicy(), completed, ExecutionProfile.Release));
                Throws<InvalidOperationException>(() => SurprisePolicy().EnableConnectedExplorationObservation());
                Throws<InvalidOperationException>(() => ConnectedObservationPolicy().EnableExplorationSearch());
                foreach (int oldWire in new[] { 51, 86, 90, 91, 92 }) {
                    byte[] altered = raw.ToArray();
                    Buffer.BlockCopy(BitConverter.GetBytes(oldWire), 0, altered, 4, 4);
                    int length = altered.Length - 32;
                    using (var checksum = System.Security.Cryptography.SHA256.Create())
                        Buffer.BlockCopy(checksum.ComputeHash(altered, 0, length), 0, altered, length, 32);
                    Throws<InvalidDataException>(() => codec.Decode(altered));
                }
                SaveConnectedObservation(sim, directory, "wire93-completed");
            });
        }
    }
}
#endif
