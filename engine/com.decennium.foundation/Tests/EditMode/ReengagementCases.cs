#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy ReengagementPolicy(uint? seed = null, ConditionCombatFixture conditions = null,
            bool companionConsents = true, bool directorAuthorizes = true)
            => RetreatPolicy(seed, conditions).EnablePhysicalReengagement(companionConsents, directorAuthorizes);

        private static Simulation ReengagementContinued(TestOnlySharedWorldPolicy policy = null, bool early = false,
            int upstreamDelay = 0, int denominator = 1, Action<Simulation> afterAdmission = null)
            => ReengagementRetreatAndContinue(RetreatReady(policy ?? ReengagementPolicy(), early, upstreamDelay, denominator), early, afterAdmission);

        private static Simulation ReengagementRetreatAndContinue(Simulation sim, bool early, Action<Simulation> afterAdmission = null)
        {
            afterAdmission?.Invoke(sim);
            if (!early) {
                for (int turn = 0; turn < 6; turn++) {
                    if (sim.Capture().Encounter.CurrentActor == LaterDefender) {
                        LaterStance(sim, CombatStance.Guarded);
                        RetreatThreat(sim);
                    }
                    EndReinforcementTurn(sim);
                }
            }
            LaterCommit(sim, RetreatInstruction(sim));
            PlayRetreatToOutcome(sim);
            Require(sim.Capture().Retreat.SuccessfulExit != null && Body(sim, LaterDefender).X == 0 && Body(sim, LaterDefender).Y == 2,
                "Expected the actual surviving defender at the selected contact.");
            PlanWalk(sim, 0, -1);
            return sim;
        }

        private static void StageReengagement(Simulation sim, bool run = false)
        {
            WorldStep(sim, 0, 1, run: run, actor: ReinforcingCompanion);
            WorldAdvance(sim, 1);
            Require(Body(sim, ReinforcingCompanion).X == 1 && Body(sim, ReinforcingCompanion).Y == 2,
                "The companion did not actually reach staging.");
        }

        private static Command ReengagementWalk(Simulation sim, string id = null)
            => new Command(id ?? "reengagement.walk." + sim.Capture().Revision, PlanHero, sim.Capture().Revision,
                CommandKind.BeginWorldStep, "walk", 0, 1);

        private static RuleTime ShiftReengagementTime(RuleTime first, RuleTime second, int sign)
            => T(checked(first.Numerator * second.Denominator + sign * second.Numerator * first.Denominator),
                checked(first.Denominator * second.Denominator));

        private static void ReengagementWaitTo(Simulation sim, RuleTime time)
        {
            var wait = ShiftReengagementTime(time, sim.Capture().RuleClock, -1);
            if (wait > default(RuleTime)) WorldAdvance(sim, checked((int)wait.Numerator), checked((int)wait.Denominator));
        }

        private static RuleTime ReengagementDepartureAt(Simulation sim, RuleTime? contact = null)
        {
            var s = sim.Capture();
            var phase = s.Reinforcement.Admission.Phase;
            var duration = T(30, TestOnlyClubAttackPolicy.WalkingSpeed(s, PlanHero));
            if (!contact.HasValue) {
                long slot = phase.Epoch.LatestStart(PlanHero, phase.Epoch.SlotAt(s.RuleClock));
                var earliest = ShiftReengagementTime(s.RuleClock, duration, 1);
                do { slot += phase.Epoch.Order.Count; } while (phase.Epoch.Start(slot) < earliest);
                contact = phase.Epoch.Start(slot);
            }
            return ShiftReengagementTime(contact.Value, duration, -1);
        }

        private static CommandResult CompleteReengagement(Simulation sim)
        {
            LaterCommit(sim, ReengagementWalk(sim));
            return LaterCommit(sim, LaterAdvance(sim, 12));
        }

        private static void RejectReengagementForgery(Simulation run, Action<Snapshot> alter, string expected)
        {
            var forged = run.Capture();
            alter(forged);
            var codec = new SnapshotCodec();
            string rejection = null;
            try { new Simulation(ReengagementPolicy(), codec.Decode(codec.Encode(forged)), ExecutionProfile.Laboratory); }
            catch (ArgumentException ex) { rejection = ex.Message; }
            Require(rejection?.Contains(expected) == true,
                "The isolated re-engagement forgery expected " + expected + ", received " + (rejection ?? "accepted"));
        }

        private static void AddReengagementCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp07_reengagement_authenticated_paid_contact_and_partial_save", () =>
            {
                var sim = ReengagementContinued();
                var before = sim.Capture();
                Require(before.SchemaVersion == Snapshot.ReengagementSchema && before.RuleClock == T(23295, 2)
                    && before.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete,
                    "The real earlier expedition did not continue into the new profile.");
                RejectUnchanged(sim, host, ReengagementWalk(sim), "ReengagementParticipantsAbsent");
                RejectUnchanged(sim, host, new Command("reengagement.defender-leaves", LaterDefender, before.Revision,
                    CommandKind.BeginWorldStep, "walk", 0, 1), "ReengagementDefenderHoldsActualPosition");
                WorldStep(sim, 0, 1, actor: ReinforcingCompanion);
                WorldAdvance(sim, 1, 2);
                RejectUnchanged(sim, host, ReengagementWalk(sim), "ConcurrentHostileTraversalUnsupported");
                WorldAdvance(sim, 1, 2);
                var stale = ReengagementWalk(sim, "reengagement.stale");
                WorldAdvance(sim, 3, 2);
                RejectUnchanged(sim, host, stale, "StaleRevision");
                var walk = ReengagementWalk(sim);
                var wrong = new Authority("TEST_ONLY.other", new[] { PlanHero, ReinforcingCompanion }, true, true);
                var noCompanion = new Authority("TEST_ONLY.host", new[] { PlanHero }, true, true);
                RejectUnchanged(sim, wrong, walk, "ReengagementControllerUnauthorized");
                RejectUnchanged(sim, noCompanion, walk, "ReengagementControllerUnauthorized");
                var query = sim.QueryCommand(host, walk);
                Require(query.Admissible && query.Code == "ReengagementApproachAvailable"
                    && sim.DiscoverCommands(host, PlanHero).Any(x => x.Command.Kind == CommandKind.BeginWorldStep
                        && x.Command.X == 0 && x.Command.Y == 1 && x.Command.Target == "walk"),
                    "The named physical contact was not discoverable through the ordinary walk.");
                SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-before-approach");
                LaterCommit(sim, walk);
                WorldAdvance(sim, 1, 2);
                var partial = sim.Capture();
                Require(partial.WorldTraversals.Single().DistanceFeet == Q(5, 3) && !partial.InventoryCombat
                    && partial.Reengagement.Contacts.Count == 0, "Partial approach did not preserve actual distance.");
                LaterCommit(sim, new Command("reengagement.suspend", PlanHero, partial.Revision, CommandKind.SuspendWorldStep));
                var resume = new Command("reengagement.resume", PlanHero, sim.Capture().Revision, CommandKind.ResumeWorldStep);
                RejectUnchanged(sim, wrong, resume, "ReengagementControllerUnauthorized");
                LaterCommit(sim, resume);
                Require(sim.Capture().WorldTraversals.Single().StartedRevision == partial.WorldTraversals.Single().StartedRevision
                    && sim.Capture().WorldTraversals.Single().DistanceFeet == partial.WorldTraversals.Single().DistanceFeet,
                    "Resume replaced the authenticated receipt or previously paid progress.");
                var replay = SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-partial");
                foreach (var run in new[] { sim, replay }) {
                    var arrival = new Command("reengagement.trusted-clock", SaleBuyer, run.Capture().Revision,
                        CommandKind.AdvanceClock, x: 12, y: 1);
                    var clockAuthority = new Authority("TEST_ONLY.clock", new[] { SaleBuyer }, true, false);
                    var result = run.Execute(clockAuthority, arrival);
                    var contacted = run.Capture();
                    var entry = contacted.Reengagement.Entry;
                    Require(entry != null && entry.At == T(23303, 2) && entry.MarkerOrdinal == 28
                        && entry.ApproachRevision == walk.ExpectedRevision + 1 && entry.DistanceFeet == Q(5) && contacted.RuleClock == entry.At
                        && result.Outcome == Outcome.Committed && result.TacticalDecisionAt == entry.At
                        && contacted.Receipts.Last().Principal == "TEST_ONLY.clock" && contacted.Encounter.CurrentActor == PlanHero
                        && contacted.Encounter.Round == 10 && contacted.Encounter.TurnOrdinal == 28
                        && contacted.RandomState == before.RandomState
                        && ExpeditionPressureRules.Current(contacted, before.Retreat.Definition.CohortId) == 2,
                        "Actual contact did not yield once at the original hero Start.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Partial approach restore changed the tactical decision.");
                SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-contact");

                foreach (var (consents, director, expected) in new[] {
                    (false, true, "ReengagementCompanionConsentMissing"),
                    (true, false, "ReengagementDirectorAuthorityMissing")
                }) {
                    var limited = ReengagementContinued(ReengagementPolicy(20, companionConsents: consents,
                        directorAuthorizes: director), early: true);
                    StageReengagement(limited);
                    RejectUnchanged(limited, host, ReengagementWalk(limited), expected);
                }
                var absent = RetreatReady(ReengagementPolicy(7), early: true);
                LaterCommit(absent, RetreatInstruction(absent));
                PlayRetreatToOutcome(absent);
                Require(absent.Capture().Retreat.SuccessfulExit != null && Body(absent, LaterDefender).Y == 3,
                    "The actual short retreat must leave the defender outside this contact.");
                PlanWalk(absent, 0, -1);
                StageReengagement(absent);
                RejectUnchanged(absent, host, ReengagementWalk(absent), "ReengagementParticipantsAbsent");

            });

            cases.Add("exp07_reengagement_watch_at_contact_and_honest_failure", () =>
            {
                foreach (var (seed, delay, natural, admitted) in new[] {
                    (20u, 57405, 5, true), (15u, 57409, 1, false)
                }) {
                    var sim = ReengagementContinued(ReengagementPolicy(seed), early: true, upstreamDelay: delay, denominator: 2);
                    StageReengagement(sim);
                    var target = T(28800);
                    ReengagementWaitTo(sim, ReengagementDepartureAt(sim, target));
                    var before = sim.Capture();
                    var phase = before.Reinforcement.Admission.Phase;
                    int ordinal = phase.GlobalTurn(phase.Epoch.SlotAt(target));
                    Require(phase.Start(ordinal) == target && phase.Actor(ordinal) == PlanHero
                        && before.ExpeditionPressureCheckpoints.Length == 0, "The real upstream timeline failed to align.");
                    if (!admitted) {
                        var earlyClosure = SaveBill(sim, ReengagementPolicy(seed), directory, "exp07-reengagement-before-watch-closure");
                        WorldAdvance(earlyClosure, 1, 2);
                        LaterCommit(earlyClosure, ReengagementWalk(earlyClosure));
                        ReengagementWaitTo(earlyClosure, target);
                        var partial = earlyClosure.Capture();
                        var edge = partial.WorldTraversals.Single();
                        Require(partial.Reengagement.Contacts.Count == 0 && edge.Status == WorldTraversalStatus.Suspended
                            && edge.DistanceFeet > default(RuleQuantity) && edge.DistanceFeet < Q(5)
                            && partial.ExpeditionPressureCheckpoints.Single().Consequence == ExpeditionPressureConsequenceKind.RouteClosure,
                            "A genuine obstruction before physical arrival did not suspend the existing edge.");
                        RejectUnchanged(earlyClosure, host, new Command("reengagement.resume-closed", PlanHero, partial.Revision,
                            CommandKind.ResumeWorldStep), "ReengagementOpeningObstructedByPressure");
                        SaveBill(earlyClosure, ReengagementPolicy(seed), directory, "exp07-reengagement-partial-watch-closure");
                    }
                    var result = CompleteReengagement(sim);
                    var after = sim.Capture();
                    var contact = after.Reengagement.Contacts.Single();
                    var checkpoint = after.ExpeditionPressureCheckpoints.Single();
                    Require(contact.Entered == admitted && contact.MarkerOrdinal == ordinal
                        && after.RuleClock == target && checkpoint.At == target
                        && checkpoint.AppliedRevision == contact.ArrivalRevision && checkpoint.CommandId == contact.ArrivalCommandId
                        && checkpoint.Natural == natural && checkpoint.PressureBefore == 2 && checkpoint.StoredPressure == 3
                        && Body(sim).Y == 1 && ReinforcementInterval(after, PlanHero).LastStart == ordinal
                        && after.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat) == 1
                        && after.ExpeditionPressureExposures.Single().Id == before.ExpeditionPressureExposures.Single().Id
                        && after.RandomState == checkpoint.RandomAfter && checkpoint.RandomBefore == before.RandomState,
                        "Watch and inherited Start did not settle once through the actual contact.");
                    if (admitted)
                        Require(after.InventoryCombat && result.TacticalDecisionAt == target
                            && checkpoint.Consequence == ExpeditionPressureConsequenceKind.None,
                            "The unblocked real Watch did not allow tactical entry.");
                    else
                        Require(!after.InventoryCombat && result.ReachedClock == target
                            && result.Code == "ReengagementOpeningObstructedByPressure"
                            && checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure,
                            "The actual route closure did not preserve the paid arrival and reject the transition.");
                    SaveBill(sim, ReengagementPolicy(seed), directory, admitted
                        ? "exp07-reengagement-watch-admitted" : "exp07-reengagement-watch-closed");
                }

                var mistimed = ReengagementContinued(ReengagementPolicy(20), early: true);
                StageReengagement(mistimed);
                var off = ReengagementDepartureAt(mistimed).AddSeconds(1);
                ReengagementWaitTo(mistimed, off);
                var failure = CompleteReengagement(mistimed);
                var interrupted = mistimed.Capture();
                Require(failure.Code == "ReengagementArrivalOutsideHeroStart" && failure.ReachedClock == interrupted.RuleClock
                    && interrupted.Reengagement.Contacts.Single().MarkerOrdinal == -1 && Body(mistimed).Y == 1
                    && !interrupted.InventoryCombat && !interrupted.WorldTraversals.Any(),
                    "An off-phase arrival discarded movement, ran past the decision or fabricated a Start.");
                RejectUnchanged(mistimed, host, ReengagementWalk(mistimed, "reengagement.occupied"), "Occupied");
                WorldAdvance(mistimed, 6);
                Require(mistimed.Capture().Reengagement.Contacts.Count == 1 && !mistimed.Capture().InventoryCombat,
                    "Standing in the contact cell replayed a missed arrival.");
                PlanWalk(mistimed, 0, -1);
                ReengagementWaitTo(mistimed, ReengagementDepartureAt(mistimed));
                CompleteReengagement(mistimed);
                Require(mistimed.Capture().Reengagement.Entry != null && mistimed.Capture().Reengagement.Contacts.Count == 2,
                    "A fresh lawful physical approach could not follow an honest failed arrival.");
                SaveBill(mistimed, ReengagementPolicy(20), directory, "exp07-reengagement-off-phase-and-retry");

                var condition = new ConditionCombatFixture(new[] {
                    CCApply("reengagement-defender-blind", "Blinded", LaterDefender, at: new ConditionStamp(T(191, 2)))
                });
                var unaware = ReengagementContinued(ReengagementPolicy(20, condition), early: true, upstreamDelay: 9, denominator: 2);
                StageReengagement(unaware);
                ReengagementWaitTo(unaware, ReengagementDepartureAt(unaware, T(96)));
                LaterCommit(unaware, ReengagementWalk(unaware));
                ReengagementWaitTo(unaware, T(191, 2));
                Require(unaware.Capture().WorldTraversals.Single().DistanceFeet > default(RuleQuantity),
                    "The contact condition must occur after actual progress.");
                LaterCommit(unaware, CCCommand(unaware, "reengagement-defender-blind", LaterDefender));
                var changed = LaterCommit(unaware, LaterAdvance(unaware, 12));
                Require(changed.Code == "ReengagementAwarenessUnavailable" && changed.ReachedClock == T(96)
                    && Body(unaware).Y == 1 && !unaware.Capture().InventoryCombat
                    && unaware.Capture().Reengagement.Contacts.Single().MarkerOrdinal >= 0,
                    "A live condition change did not preserve the lawful arrival and suppress contact.");
                SaveBill(unaware, ReengagementPolicy(20, condition), directory, "exp07-reengagement-condition-at-arrival");

            });

            cases.Add("exp07_reengagement_original_schedule_and_distinct_active_segment", () =>
            {
                var sim = ReengagementContinued();
                var before = sim.Capture();
                StageReengagement(sim);
                ReengagementWaitTo(sim, ReengagementDepartureAt(sim));
                long gap = sim.Capture().Revision;
                CompleteReengagement(sim);
                var opened = sim.Capture();
                var entry = opened.Reengagement.Entry;
                var segment = opened.Encounter;
                var phase = before.Reinforcement.Admission.Phase;
                Require(opened.Reengagement.Definition.RootId == before.ClosedEncounters.Last().Encounter.Id
                    && segment.Id != opened.Reengagement.Definition.RootId && segment.Origin == T(23303, 2)
                    && segment.InheritedPhase.Epoch.Id == phase.Epoch.Id && segment.InheritedPhase.Epoch.Origin == T(23199, 2)
                    && segment.ObservedOrdinals.SequenceEqual(new[] { 28 }) && segment.StartRevisions.SequenceEqual(new[] { entry.ArrivalRevision })
                    && segment.NextOwnStart(28) == T(23315, 2) && segment.ActorAt(29) == ReinforcingCompanion
                    && segment.RoundAt(29) == 11 && segment.StartAt(29) == T(23307, 2)
                    && EncounterHistory.AtRevision(opened, gap) == null && EncounterHistory.AtRevision(opened, entry.ArrivalRevision).Id == segment.Id
                    && opened.ClosedEncounters.Zip(before.ClosedEncounters, (a, b) => a.Reason == b.Reason
                        && a.ClosedRevision == b.ClosedRevision && a.Encounter.ObservedOrdinals.SequenceEqual(b.Encounter.ObservedOrdinals)).All(x => x)
                    && opened.LaterEncounter.Entry.Draws.SequenceEqual(before.LaterEncounter.Entry.Draws)
                    && opened.Reinforcement.Admission.Draw == before.Reinforcement.Admission.Draw,
                    "The old archive, inherited order, gap or original initiative evidence changed.");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.EndFixedEncounter), "ConflictNotResolved");
                foreach (var (actor, ordinal, at) in new[] {
                    (ReinforcingCompanion, 29, T(23307, 2)), (LaterDefender, 30, T(23311, 2)), (PlanHero, 31, T(23315, 2))
                }) {
                    EndReinforcementTurn(sim);
                    var next = sim.Capture();
                    Require(next.Encounter.CurrentActor == actor && next.Encounter.TurnOrdinal == ordinal
                        && next.Encounter.Round == 11 && next.Encounter.CurrentTurnId == segment.Id + ".turn." + ordinal
                        && next.RuleClock == at && ReinforcementInterval(next, actor).LastStart == ordinal,
                        "The resumed segment did not use the next actual incumbent Start.");
                }
                Require(sim.Capture().Encounter.ObservedOrdinals.SequenceEqual(new[] { 28, 29, 30, 31 }),
                    "The active segment synthesized gap observations or reused the retired turn key.");
                SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-inherited-starts");
            });

            cases.Add("exp07_reengagement_real_fight_resolution_and_continuation", () =>
            {
                var sim = ReengagementContinued();
                StageReengagement(sim);
                ReengagementWaitTo(sim, ReengagementDepartureAt(sim));
                var approach = ReengagementWalk(sim);
                LaterCommit(sim, approach);
                var arrival = LaterAdvance(sim, 12);
                var opening = LaterCommit(sim, arrival);
                var start = sim.Capture();
                var ready = Bytes(sim);
                var repeated = sim.Execute(host, arrival);
                Require(repeated.Outcome == Outcome.Duplicate && repeated.TacticalDecisionAt == opening.TacticalDecisionAt
                    && ready.SequenceEqual(Bytes(sim)), "The arrival retry replayed contact or the own Start.");
                RejectUnchanged(sim, host, new Command(arrival.Id, arrival.Actor, arrival.ExpectedRevision,
                    CommandKind.AdvanceClock, x: arrival.X + 1, y: arrival.Y), "CommandIdConflict");

                LaterStance(sim, CombatStance.Aggressive);
                var attack = Tac(sim, CommandKind.AttackClub, LaterDefender, weapon: TestOnlyClubAttackPolicy.ActorClub,
                    press: PressHitInstruction.KeepExisting);
                LaterCommit(sim, attack);
                var paid = sim.Capture();
                var actual = paid.MeleeAttacks.Last();
                Require(actual.AttackerId == PlanHero && actual.TargetId == LaterDefender && actual.TurnOrdinal == start.Encounter.TurnOrdinal
                    && attack.Combat.TurnId == start.Encounter.CurrentTurnId && paid.RandomState != start.RandomState
                    && ReinforcementInterval(paid, PlanHero).ActionSpent && paid.RuleClock == start.RuleClock
                    && paid.ExpeditionPressureChanges.Any(x => x.SourceId == actual.Id && x.Kind == ExpeditionPressureChangeKind.OpenCombat),
                    "The resumed action did not use the same actor, physical attack, action, RNG and Pressure history.");
                var replay = SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-paid-attack");
                foreach (var run in new[] { sim, replay }) {
                    if (Life(run, LaterDefender).Dead) LaterCommit(run, Tac(run, CommandKind.EndFixedEncounter));
                    else {
                        EndReinforcementTurn(run);
                        FinishLaterFight(run, defenderAttacked: true);
                    }
                    var closed = run.Capture();
                    var archive = closed.ClosedEncounters.Last();
                    Require(closed.ClosedEncounters.Length == 3 && closed.Encounter == null && !closed.InventoryCombat
                        && Life(run, LaterDefender).Dead && archive.Encounter.Id == start.Encounter.Id
                        && archive.Encounter.ObservedOrdinals[0] == 28 && archive.Encounter.Origin == T(23303, 2)
                        && archive.ClosedAt == archive.Encounter.StartAt(archive.Encounter.TurnOrdinal + 1)
                        && CommandHistory.Read(closed.Receipts.Last()).Kind == CommandKind.EndFixedEncounter
                        && closed.ClosedEncounters[1].Reason == start.ClosedEncounters[1].Reason
                        && closed.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat) == 1,
                        "Real defender defeat did not use ordinary distinct segment closure and existing Pressure.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Resumed combat did not replay byte-identically.");
                RejectReengagementForgery(sim, altered => {
                    var archive = altered.ClosedEncounters.Last();
                    altered.ClosedEncounters = altered.ClosedEncounters.Take(altered.ClosedEncounters.Length - 1)
                        .Append(new ClosedEncounterRecord(archive.Encounter, archive.ClosedRevision, archive.ClosedAt, "test.forged-exit"))
                        .ToArray();
                }, "Invalid resolved re-engagement exit provenance.");
                var ordinary = SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-closed");
                foreach (var run in new[] { sim, ordinary }) {
                    PlanWalk(run, 0, -1);
                    LaterCommit(run, ReengagementWalk(run, "reengagement.fresh-id-after-resolution"));
                    WorldAdvance(run, 3);
                    Require(!run.Capture().InventoryCombat && run.Capture().Reengagement.Contacts.Count == 1
                        && run.Capture().ClosedEncounters.Length == 3,
                        "Ordinary movement or a new command identity created a second re-engagement.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(ordinary)), "Ordinary movement after re-engagement closure diverged.");
                SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-continued");
            });

            cases.Add("exp07_reengagement_carries_intervals_conditions_and_remote_work", () =>
            {
                var contactAt = T(23303, 2);
                var marker = "TEST_ONLY.reinforced-calendar.start.26";
                var conditions = new ConditionCombatFixture(
                    new ConditionFixtureEvent(ReinforcingCompanion, ConditionOperation.Apply("event.reengagement-virtual",
                        new ConditionStamp(T(23199, 2)), new ConditionApplicationData("reengagement-virtual", PlanHero,
                            marker, "Poisoned", new ConditionStamp(contactAt), "original-regular-start", false))),
                    CCApply("reengagement-absolute", "Deafened", PlanHero,
                        expires: new ConditionStamp(contactAt.AddSeconds(1)), at: new ConditionStamp(T(23199, 2))));
                var sim = ReengagementContinued(ReengagementPolicy(conditions: conditions), afterAdmission: run => {
                    LaterCommit(run, CCCommand(run, "reengagement-virtual", ReinforcingCompanion));
                    LaterCommit(run, CCCommand(run, "reengagement-absolute", PlanHero));
                });
                StageReengagement(sim, run: true);
                ReengagementWaitTo(sim, ReengagementDepartureAt(sim));
                var before = sim.Capture();
                Require(CCState(sim, ReinforcingCompanion).View().Has(ConditionKind.Poisoned)
                    && CCState(sim, PlanHero).View().Has(ConditionKind.Deafened), "Both bound effects must still be live before contact.");
                CompleteReengagement(sim);
                var after = sim.Capture();
                var companion = ReinforcementInterval(after, ReinforcingCompanion);
                Require(after.Reengagement.Entry?.At == contactAt
                    && companion.ActionSpent && companion.DashPaid && companion.MovementSpent == Q(5)
                    && companion.LastStart == 26 && companion.ReactionAvailable == ReinforcementInterval(before, ReinforcingCompanion).ReactionAvailable
                    && companion.Interactions == ReinforcementInterval(before, ReinforcingCompanion).Interactions
                    && ReinforcementInterval(after, LaterDefender).LastStart == 27 && ReinforcementInterval(after, PlanHero).LastStart == 28
                    && WorldTiming.FindEpoch(after, after.Encounter.InheritedPhase.Epoch.Id).MarkerId(26) == marker
                    && ConditionHistory.Restore(after.Conditions.Single(x => x.Target == ReinforcingCompanion)).Ledger.Applications
                        .Single(x => x.Application.Id == "reengagement-virtual").EndedAt?.Time == contactAt
                    && CCState(sim, PlanHero).View().Has(ConditionKind.Deafened) && ReinforcementPlanting(after).Progress == T(2)
                    && after.Clubs.Single(x => x.Id == LaterClub).HeldBy == LaterDefender,
                    "The resumed segment replaced a real interval, existing condition deadline, work or gear.");
                EndReinforcementTurn(sim);
                Require(ViewCondition(sim, "reengagement-absolute").EndedAt?.Time == contactAt.AddSeconds(1)
                    && !ReinforcementInterval(sim.Capture(), ReinforcingCompanion).DashPaid,
                    "An existing absolute expiry or the companion's later actual own Start was lost.");
                SaveBill(sim, ReengagementPolicy(conditions: conditions), directory, "exp07-reengagement-dash-and-markers");

                var work = ReinforcementStaged(ReengagementPolicy());
                const string filledSkin = "TEST_ONLY.pack-skin";
                const string emptySkin = TestOnlyFillingPolicy.CompanionSkinId;
                PlanWalk(work, 0, 1);
                LaterCommit(work, Portable(work, CommandKind.HandlePortableEquipment, filledSkin, SaleBuyer, HandlingKind.Handover));
                LaterCommit(work, Portable(work, CommandKind.HandlePortableEquipment, emptySkin, SaleBuyer,
                    HandlingKind.Handover, ReinforcingCompanion));
                PlanWalk(work, 0, -1);
                EnterLater(work);
                LaterCommit(work, ReinforcementCommand(work));
                EndReinforcementTurn(work);
                EndReinforcementTurn(work);
                ReengagementRetreatAndContinue(work, early: false);
                StageReengagement(work);
                ReengagementWaitTo(work, ReengagementDepartureAt(work));
                LaterCommit(work, IC(work, CommandKind.StartWaterFill, "TEST_ONLY.pack-water", new InventoryRequest(Q(1), emptySkin), SaleBuyer));
                var previous = work.Capture();
                CompleteReengagement(work);
                var now = work.Capture();
                var filling = now.WaterFills.Single();
                var elapsed = ShiftReengagementTime(now.RuleClock, previous.RuleClock, -1);
                Require(now.Reengagement.Entry != null && filling.Status == WaterFillStatus.Working && filling.WorkerId == SaleBuyer
                    && filling.Progress == elapsed && now.Work.WorkerIntervals.Count(x => x.JobId == filling.Id) == 1
                    && !now.Encounter.Order.Contains(SaleBuyer) && ReinforcementPlanting(now).Progress == T(2),
                    "Independent real remote labor did not advance once through contact.");
                SaveBill(work, ReengagementPolicy(), directory, "exp07-reengagement-remote-work");
            });

            cases.Add("exp07_reengagement_compatible_saves_and_isolated_provenance", () =>
            {
                var sim = ReengagementContinued();
                var before = sim.Capture();
                Throws<InvalidOperationException>(() => new Simulation(ReengagementPolicy(), before, ExecutionProfile.Release));
                Throws<ArgumentException>(() => new Simulation(RetreatPolicy(), before, ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(ReengagementPolicy(companionConsents: false), before, ExecutionProfile.Laboratory));

                StageReengagement(sim, run: true);
                ReengagementWaitTo(sim, ReengagementDepartureAt(sim));
                CompleteReengagement(sim);
                RejectReengagementForgery(sim, altered => {
                    var r = altered.Reengagement;
                    var d = r.Definition;
                    altered.Reengagement = new ReengagementRecord(new ReengagementDefinition("test.forged-conflict", d.SegmentId,
                        d.LeadId, d.CompanionId, d.DefenderId, d.ControllerId, d.ConsentId, d.DirectorMandateId), r.Contacts);
                }, "does not bind the original opposition");
                RejectReengagementForgery(sim, altered => {
                    var r = altered.Reengagement;
                    var d = r.Definition;
                    altered.Reengagement = new ReengagementRecord(new ReengagementDefinition(d.RootId, "test.forged-segment",
                        d.LeadId, d.CompanionId, d.DefenderId, d.ControllerId, d.ConsentId, d.DirectorMandateId), r.Contacts);
                }, "Invalid later encounter history");
                RejectReengagementForgery(sim, altered => {
                    var r = altered.Reengagement;
                    var x = r.Entry;
                    altered.Reengagement = new ReengagementRecord(r.Definition, new[] {
                        new ReengagementContact(x.ApproachRevision - 1, x.ArrivalRevision, x.ArrivalCommandId, x.At, x.MarkerOrdinal, x.DistanceFeet, "")
                    });
                }, "Invalid re-engagement approach, arrival or inherited marker");
                RejectReengagementForgery(sim, altered => {
                    var r = altered.Reengagement;
                    var x = r.Entry;
                    altered.Reengagement = new ReengagementRecord(r.Definition, new[] {
                        new ReengagementContact(x.ApproachRevision, x.ArrivalRevision, "test.forged-arrival", x.At, x.MarkerOrdinal, x.DistanceFeet, "")
                    });
                }, "Invalid re-engagement approach, arrival or inherited marker");
                RejectReengagementForgery(sim, altered => {
                    var r = altered.Reengagement;
                    var x = r.Entry;
                    altered.Reengagement = new ReengagementRecord(r.Definition, new[] {
                        new ReengagementContact(x.ApproachRevision, x.ArrivalRevision, x.ArrivalCommandId, x.At, x.MarkerOrdinal + 3, x.DistanceFeet, "")
                    });
                }, "Invalid re-engagement approach, arrival or inherited marker");
                RejectReengagementForgery(sim, altered => {
                    altered.WorldIntervals = altered.WorldIntervals.Select(x => x.ActorId == ReinforcingCompanion
                        ? new WorldIntervalRecord(x.ActorId, x.LastStart, x.MovementSpent, false, false, x.ReactionAvailable, x.Interactions) : x).ToArray();
                }, "InvalidSharedWorldReplay");
                RejectReengagementForgery(sim, altered => {
                    altered.ExpeditionPressureChanges = altered.ExpeditionPressureChanges.Where(x =>
                        x.Kind != ExpeditionPressureChangeKind.SuccessfulRetreat).ToArray();
                }, "Invalid local retreat Pressure history");
                SaveBill(sim, ReengagementPolicy(), directory, "exp07-reengagement-unmodified-integrity");

                var old = ReengagementContinued(RetreatPolicy());
                Require(old.Capture().SchemaVersion == Snapshot.RetreatSchema && old.Capture().Reengagement == null,
                    "The original profile selected re-engagement.");
                StageReengagement(old);
                ReengagementWaitTo(old, ReengagementDepartureAt(old));
                var previous = CompleteReengagement(old);
                Require(previous.TacticalDecisionAt == null && old.Capture().Encounter == null
                    && old.Capture().Reengagement == null && Body(old).Y == 1,
                    "The older selected profile changed ordinary contact behavior.");
                SaveBill(old, RetreatPolicy(), directory, "exp07-reengagement-original-schema88");
            });
        }
    }
}
#endif
