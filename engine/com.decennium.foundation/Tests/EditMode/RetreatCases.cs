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
        private static TestOnlySharedWorldPolicy RetreatPolicy(uint? seed = null, ConditionCombatFixture conditions = null,
            TestOnlyLivingOpponentRetreatProfile profile = null)
            => ReinforcementPolicy(seed, conditions).EnableLivingOpponentRetreat(profile ?? new TestOnlyLivingOpponentRetreatProfile());

        private static Simulation RetreatReady(TestOnlySharedWorldPolicy policy = null, bool early = false,
            int delay = 0, int denominator = 1)
        {
            var sim = ReinforcementStaged(policy ?? RetreatPolicy(), early);
            if (delay > 0) WorldAdvance(sim, delay, denominator);
            EnterLater(sim);
            LaterCommit(sim, ReinforcementCommand(sim));
            EndReinforcementTurn(sim);
            EndReinforcementTurn(sim);
            Require(sim.Capture().Reinforcement.Admission != null && sim.Capture().Encounter.Round == 2,
                "Expected the first actual reinforced round.");
            return sim;
        }

        private static Command RetreatInstruction(Simulation sim, CommandKind kind = CommandKind.DeclareRetreat,
            string id = null, string actor = PlanHero)
        {
            var state = sim.Capture();
            return new Command(id ?? "retreat." + state.Revision + "." + kind, actor, state.Revision, kind, state.Retreat.Definition.Id);
        }

        private static void RetreatStep(Simulation sim, int x, int y)
        {
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: x, y: y));
            while (TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null) LaterCommit(sim, Opportunity(sim, false));
        }

        private static void RetreatPartyAdvance(Simulation sim, string actor)
        {
            var body = Body(sim, actor);
            if (body.Y > 1) RetreatStep(sim, body.X, body.Y - 1);
        }

        private static Command RetreatThreat(Simulation sim, bool fork = false)
        {
            int heroY = Body(sim).Y;
            while (Math.Abs(Body(sim, LaterDefender).Y - heroY) > 1) {
                var enemy = Body(sim, LaterDefender);
                RetreatStep(sim, enemy.X, enemy.Y + Math.Sign(heroY - enemy.Y));
            }
            if (fork && Body(sim, ReinforcingCompanion).Y == 1 && Body(sim, LaterDefender).X == 0 && heroY == 2)
                RetreatStep(sim, 1, 2);
            var attack = Tac(sim, CommandKind.AttackClub, PlanHero, weapon: LaterClub, press: PressHitInstruction.KeepExisting);
            LaterCommit(sim, attack);
            return attack;
        }

        private static Command RetreatPlayRound(Simulation sim, bool moveCompanion = true, bool fork = false, bool skipThreat = false)
        {
            long round = sim.Capture().Encounter.Round;
            Command finalEnd = null;
            do {
                var state = sim.Capture();
                var actor = state.Encounter.CurrentActor;
                LaterStance(sim, CombatStance.Guarded);
                if (actor == ReinforcingCompanion && moveCompanion) RetreatPartyAdvance(sim, actor);
                if (actor == LaterDefender && !skipThreat) RetreatThreat(sim, fork);
                if (actor == PlanHero) {
                    LaterCommit(sim, RetreatInstruction(sim, CommandKind.AttemptRetreatEscape));
                    RetreatPartyAdvance(sim, actor);
                }
                finalEnd = EndReinforcementTurn(sim);
            } while (sim.Capture().Encounter?.Round == round);
            return finalEnd;
        }

        private static Command PlayRetreatToOutcome(Simulation sim, bool moveCompanion = true, bool fork = false)
        {
            Command last = null;
            while (sim.Capture().Retreat.Active)
                last = RetreatPlayRound(sim, moveCompanion, fork);
            return last;
        }

        private static void RejectRetreatSave(Simulation run, uint seed, Action<Snapshot> alter, string expected)
        {
            var state = run.Capture();
            alter(state);
            var codec = new SnapshotCodec();
            bool rejected = false;
            try { new Simulation(RetreatPolicy(seed), codec.Decode(codec.Encode(state)), ExecutionProfile.Laboratory); }
            catch (ArgumentException error) { rejected = error.Message.Contains(expected); }
            Require(rejected, "The isolated forgery did not fail as expected: " + expected);
        }

        private static void AddRetreatCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp07_living_retreat_connected_authority_and_actual_round_start", () =>
            {
                var sim = RetreatReady();
                var before = sim.Capture();
                var d = before.Retreat.Definition;
                var exposure = before.ExpeditionPressureExposures.Single();
                Require(before.SchemaVersion == Snapshot.RetreatSchema && before.RuleClock == T(23199, 2)
                    && before.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                    && ReinforcementPlanting(before).Progress == T(2)
                    && before.ExpeditionPressureCohorts.Single().Members.SequenceEqual(new[] { PlanHero, ReinforcingCompanion })
                    && exposure.StartedRevision == before.Reinforcement.Joined.Revision && exposure.StartedAt == before.Reinforcement.Joined.At
                    && ExpeditionPressureRules.Current(before, d.CohortId) == 1,
                    "The exact connected predecessor, two-member activation or starting Pressure changed.");
                var command = RetreatInstruction(sim);
                var wrong = new Authority("TEST_ONLY.other", new[] { PlanHero, ReinforcingCompanion }, true, true);
                RejectUnchanged(sim, wrong, command, "RetreatControllerUnauthorized");
                RejectUnchanged(sim, host, RetreatInstruction(sim, actor: ReinforcingCompanion), "RetreatLeadUnauthorized");
                Require(sim.QueryCommand(host, command).Admissible && sim.DiscoverCommands(host, PlanHero).Count(x => x.Command.Kind == command.Kind) == 1,
                    "The declaration was not discoverable at the actual unconsumed Start.");
                var late = SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-admitted");
                LaterStance(late, CombatStance.Guarded);
                RejectUnchanged(late, host, RetreatInstruction(late), "RetreatRequiresUnconsumedRoundStart");
                LaterCommit(sim, command);
                var after = sim.Capture();
                Require(after.Retreat.Active && after.Retreat.Escape == 0 && after.Retreat.Pursuit == 0
                    && after.RuleClock == before.RuleClock && after.RandomState == before.RandomState
                    && after.Encounter.CurrentTurnId == before.Encounter.CurrentTurnId && after.Encounter.CurrentActor == ReinforcingCompanion,
                    "Off-turn group declaration created time, resource or initiative.");
                SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-declared");
                var scopes = new[] {
                    (new TestOnlyLivingOpponentRetreatProfile(leadAuthorized: false), "RetreatLeadMandateMissing"),
                    (new TestOnlyLivingOpponentRetreatProfile(companionConsents: false), "RetreatCompanionConsentMissing"),
                    (new TestOnlyLivingOpponentRetreatProfile(routeAuthorized: false), "RetreatRouteAuthorityMissing")
                };
                foreach (var (profile, error) in scopes) {
                    var unauthorized = RetreatReady(RetreatPolicy(2, profile: profile), early: true);
                    RejectUnchanged(unauthorized, host, RetreatInstruction(unauthorized), error);
                    if (!profile.RouteAuthorized)
                        Require(unauthorized.Capture().ExpeditionPressureCohorts.Length == 0,
                            "Missing route access seeded a Pressure cohort.");
                }
                Throws<ArgumentException>(() => new TestOnlyLivingOpponentRetreatProfile(risk: 0));
                Throws<InvalidOperationException>(() => RetreatPolicy().EnableExpeditionRouteTravel(RouteTravelCheckpointFixture()));
            });

            cases.Add("exp07_living_retreat_paid_task_threat_priority_and_incomplete_round", () =>
            {
                var sim = RetreatReady(RetreatPolicy(2), early: true);
                LaterCommit(sim, RetreatInstruction(sim));
                LaterStance(sim, CombatStance.Guarded);
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 2));
                Require(TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null,
                    "The ordinary step must retain the actual defender opportunity offer.");
                RejectUnchanged(sim, host, Opportunity(sim, true, weapon: LaterClub), "RetreatAdditionalHostileAttackUnsupported");
                RejectUnchanged(sim, host, RetreatInstruction(sim, CommandKind.AbandonRetreat), "TacticalChoicePending");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.EndRegularTurn), "TacticalChoicePending");
                LaterCommit(sim, Opportunity(sim, false));
                EndReinforcementTurn(sim);
                LaterStance(sim, CombatStance.Guarded);
                RejectUnchanged(sim, host, Tac(sim, CommandKind.AttackUnarmed, PlanHero), "RetreatAdditionalHostileAttackUnsupported");
                var threat = RetreatThreat(sim);
                var afterThreat = sim.Capture();
                Require(afterThreat.Retreat.Round.ThreatId != "" && afterThreat.MeleeAttacks.Last().Revision == threat.ExpectedRevision + 1,
                    "The declared threat must be an actual resolved attack.");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.AttackClub, PlanHero, weapon: LaterClub),
                    "RetreatAdditionalHostileAttackUnsupported");
                EndReinforcementTurn(sim);
                LaterStance(sim, CombatStance.Guarded);
                var beforeTask = sim.Capture();
                var task = RetreatInstruction(sim, CommandKind.AttemptRetreatEscape);
                LaterCommit(sim, task);
                var paid = sim.Capture();
                Require(paid.Retreat.Round.Task.Degree == RetreatTaskDegree.Failure
                    && paid.Retreat.Round.Task.Natural == 9 && paid.Retreat.Round.Task.Modifier == 0
                    && paid.Retreat.Round.Task.RandomBefore == beforeTask.RandomState && paid.RandomState != beforeTask.RandomState
                    && ReinforcementInterval(paid, PlanHero).ActionSpent && paid.RuleClock == beforeTask.RuleClock
                    && Body(sim).Y == 3 && paid.Retreat.Pursuit == 0,
                    "The real failed task must spend one Action without moving or settling early.");
                RejectUnchanged(sim, host, RetreatInstruction(sim, CommandKind.AttemptRetreatEscape), "RetreatTaskAlreadyPaid");
                var replay = SaveBill(sim, RetreatPolicy(2), directory, "exp07-retreat-mid-round");
                foreach (var run in new[] { sim, replay }) {
                    RetreatPartyAdvance(run, PlanHero);
                    EndReinforcementTurn(run);
                    Require(run.Capture().Retreat.Pursuit == 1 && run.Capture().Retreat.Round.Number == 3
                        && run.Capture().Retreat.Rounds[0].Settlement.Outcome == RetreatOutcome.Continue,
                        "The completed exchange was not settled once at the final End.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Mid-round deterministic replay changed.");
                var incomplete = RetreatReady(RetreatPolicy(2), early: true);
                LaterCommit(incomplete, RetreatInstruction(incomplete));
                RetreatPlayRound(incomplete, skipThreat: true);
                var stopped = incomplete.Capture();
                Require(stopped.Retreat.Round.Settlement.Outcome == RetreatOutcome.Incomplete
                    && stopped.Retreat.Round.Task != null && stopped.Retreat.Round.ThreatId == ""
                    && stopped.Retreat.Escape == 0 && stopped.Retreat.Pursuit == 0 && stopped.Encounter.Round == 3
                    && stopped.ExpeditionPressureChanges.Length == 0,
                    "A missing threat invented an attack, a point, or an exit.");
                RejectUnchanged(incomplete, host, RetreatInstruction(incomplete), "RetreatAlreadyAttempted");
                SaveBill(incomplete, RetreatPolicy(2), directory, "exp07-retreat-incomplete");

                var liveConditions = new ConditionCombatFixture(new[] {
                    CCApply("retreat-lead-disabled", "Incapacitated", PlanHero, at: new ConditionStamp(T(117, 2)))
                });
                var disabled = RetreatReady(RetreatPolicy(2, liveConditions), early: true);
                LaterCommit(disabled, RetreatInstruction(disabled));
                EndReinforcementTurn(disabled);
                LaterStance(disabled, CombatStance.Guarded);
                RetreatThreat(disabled);
                EndReinforcementTurn(disabled);
                LaterStance(disabled, CombatStance.Guarded);
                LaterCommit(disabled, CCCommand(disabled, "retreat-lead-disabled", PlanHero));
                RejectUnchanged(disabled, host, RetreatInstruction(disabled, CommandKind.AttemptRetreatEscape), "RetreatLeadIncapable");
                LaterCommit(disabled, Tac(disabled, CommandKind.EndRegularTurn));
                var unable = disabled.Capture().Retreat;
                Require(unable.Round.Settlement.Outcome == RetreatOutcome.Incomplete && unable.Round.Task == null
                    && unable.Round.ThreatId != "" && unable.Pursuit == 0 && unable.Escape == 0,
                    "Incapacity produced a synthetic check or a contribution.");

                var poisonedProfile = new ConditionCombatFixture(new[] {
                    CCApply("retreat-lead-poisoned", "Poisoned", PlanHero,
                        expires: new ConditionStamp(T(121, 2)), at: new ConditionStamp(T(117, 2)))
                });
                var poisoned = RetreatReady(RetreatPolicy(2, poisonedProfile), early: true);
                LaterCommit(poisoned, RetreatInstruction(poisoned));
                EndReinforcementTurn(poisoned);
                LaterStance(poisoned, CombatStance.Guarded);
                RetreatThreat(poisoned);
                EndReinforcementTurn(poisoned);
                LaterStance(poisoned, CombatStance.Guarded);
                LaterCommit(poisoned, CCCommand(poisoned, "retreat-lead-poisoned", PlanHero));
                LaterCommit(poisoned, RetreatInstruction(poisoned, CommandKind.AttemptRetreatEscape));
                var impaired = poisoned.Capture().Retreat.Round.Task;
                Require(impaired.First == 9 && impaired.Second > 0 && impaired.Natural == Math.Min(impaired.First, impaired.Second)
                    && impaired.WordsConsumed >= 2 && CCState(poisoned, PlanHero).View().Has(ConditionKind.Poisoned),
                    "The paid task ignored the live condition or its shared disadvantage dice.");
                EndReinforcementTurn(poisoned);
                Require(poisoned.Capture().RuleClock == T(121, 2) && !CCState(poisoned, PlanHero).View().Has(ConditionKind.Poisoned),
                    "The shared due effect did not settle at the actual closing End.");
                SaveBill(poisoned, RetreatPolicy(2, poisonedProfile), directory, "exp07-retreat-live-condition");

                var reverse = RetreatReady(RetreatPolicy(8), early: true);
                LaterCommit(reverse, RetreatInstruction(reverse));
                EndReinforcementTurn(reverse);
                LaterStance(reverse, CombatStance.Guarded);
                LaterCommit(reverse, RetreatInstruction(reverse, CommandKind.AttemptRetreatEscape));
                EndReinforcementTurn(reverse);
                LaterStance(reverse, CombatStance.Guarded);
                RetreatThreat(reverse);
                EndReinforcementTurn(reverse);
                Require(reverse.Capture().Retreat.Rounds[0].Settlement.Outcome == RetreatOutcome.Continue,
                    "A real lead task before the actual opposing attack did not qualify.");
                var beforeAbandon = reverse.Capture();
                LaterCommit(reverse, RetreatInstruction(reverse, CommandKind.AbandonRetreat));
                var abandoned = reverse.Capture();
                Require(abandoned.Retreat.Round.Settlement.Outcome == RetreatOutcome.Abandoned
                    && abandoned.RuleClock == beforeAbandon.RuleClock && abandoned.RandomState == beforeAbandon.RandomState
                    && abandoned.Retreat.Escape == beforeAbandon.Retreat.Escape && abandoned.Retreat.Pursuit == beforeAbandon.Retreat.Pursuit,
                    "Abandonment changed the clock, RNG or previously earned totals.");
                RejectUnchanged(reverse, host, RetreatInstruction(reverse), "RetreatAlreadyAttempted");
                SaveBill(reverse, RetreatPolicy(8), directory, "exp07-retreat-abandoned");
            });

            cases.Add("exp07_living_retreat_seeded_thresholds_crossing_and_adverse_fork", () =>
            {
                var success = RetreatReady(RetreatPolicy(7), early: true);
                LaterCommit(success, RetreatInstruction(success));
                PlayRetreatToOutcome(success);
                var settled = success.Capture();
                Require(settled.Retreat.SuccessfulExit != null && settled.Retreat.Escape == 3 && settled.Retreat.Pursuit == 0
                    && settled.Retreat.Rounds.Select(x => x.Task.Natural).SequenceEqual(new[] { 20, 16 })
                    && settled.Retreat.Rounds[0].Task.Degree == RetreatTaskDegree.CriticalSuccess
                    && settled.Retreat.SuccessfulExit.LeadCrossingId != "" && settled.Retreat.SuccessfulExit.CompanionCrossingId != ""
                    && Body(success).Y == 1 && Body(success, ReinforcingCompanion).Y == 1
                    && Life(success, LaterDefender).Hp == 8 && !settled.InventoryCombat,
                    "The actual critical task and paid route did not produce a genuine living-opponent exit.");
                SaveBill(success, RetreatPolicy(7), directory, "exp07-retreat-seeded-success");

                var failure = RetreatReady(RetreatPolicy(2), early: true);
                LaterCommit(failure, RetreatInstruction(failure));
                PlayRetreatToOutcome(failure, fork: true);
                var failed = failure.Capture();
                var last = failed.Retreat.Round.Settlement;
                Require(last.Outcome == RetreatOutcome.Failed && failed.Retreat.Pursuit == 3 && failed.Retreat.Escape == 0
                    && failed.InventoryCombat && failed.Encounter.Round == 5 && failed.ClosedEncounters.Length == 1
                    && last.Defender.X == 1 && last.Defender.Y == 2 && Body(failure, LaterDefender).X == 1
                    && failed.ExpeditionPressureChanges.All(x => x.Kind != ExpeditionPressureChangeKind.SuccessfulRetreat)
                    && failed.MeleeAttacks.Any(x => x.AttackerId == LaterDefender && x.Attack.Hit)
                    && failed.MeleeAttacks.Any(x => x.AttackerId == LaterDefender && !x.Attack.Hit),
                    "Actual failed tasks or the physically attained adverse fork were replaced.");
                SaveBill(failure, RetreatPolicy(2), directory, "exp07-retreat-failed");
                var ordinary = RetreatReady(RetreatPolicy(7), early: true);
                LaterCommit(ordinary, RetreatInstruction(ordinary));
                FinishLaterFight(ordinary, defenderAttacked: true);
                var resolved = ordinary.Capture();
                Require(Life(ordinary, LaterDefender).Dead && resolved.Encounter == null
                    && resolved.Retreat.Rounds[0].Settlement.Outcome != RetreatOutcome.Successful
                    && resolved.ExpeditionPressureChanges.All(x => x.Kind != ExpeditionPressureChangeKind.SuccessfulRetreat)
                    && CommandHistory.Read(resolved.Receipts.Last()).Kind == CommandKind.EndFixedEncounter,
                    "Defeating the defender did not use ordinary conflict closure.");
                SaveBill(ordinary, RetreatPolicy(7), directory, "exp07-retreat-ordinary-conflict-close");

                Require(RetreatRules.ResolveCounters(3, 3) == RetreatOutcome.Failed
                    && RetreatRules.ResolveCounters(3, 2) == RetreatOutcome.Successful
                    && RetreatRules.ResolveCounters(2, 2) == RetreatOutcome.Continue,
                    "The rule-level precedence must make simultaneous 3/3 a failure.");

                var blocked = RetreatReady(RetreatPolicy(7), early: true);
                LaterCommit(blocked, RetreatInstruction(blocked));
                PlayRetreatToOutcome(blocked, moveCompanion: false);
                var physicallyBlocked = blocked.Capture();
                Require(physicallyBlocked.Retreat.Escape == 3
                    && physicallyBlocked.Retreat.Round.Settlement.Outcome == RetreatOutcome.PhysicallyBlocked
                    && physicallyBlocked.InventoryCombat && Body(blocked, ReinforcingCompanion).Y == 3
                    && physicallyBlocked.Retreat.Round.Settlement.CompanionCrossingId == ""
                    && ExpeditionPressureRules.Current(physicallyBlocked, physicallyBlocked.Retreat.Definition.CohortId) == 1,
                    "The threshold with an uncrossed member produced success, movement, or Pressure.");
                SaveBill(blocked, RetreatPolicy(7), directory, "exp07-retreat-uncrossed");
            });

            cases.Add("exp07_living_retreat_causal_pressure_watch_order_and_shared_work", () =>
            {
                var aligned = RetreatReady(RetreatPolicy(7), early: true, delay: 57431, denominator: 2);
                LaterCommit(aligned, RetreatInstruction(aligned));
                var outgoing = PlayRetreatToOutcome(aligned, fork: true);
                var state = aligned.Capture();
                var exit = state.Retreat.SuccessfulExit;
                var check = state.ExpeditionPressureCheckpoints.Single();
                var rise = state.ExpeditionPressureChanges.Single(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat);
                string cohort = state.Retreat.Definition.CohortId;
                Require(exit != null && exit.At == T(28800) && check.At == exit.At && check.AppliedRevision == exit.Revision
                    && check.CommandId == outgoing.Id && check.Natural == 3 && check.PressureBefore == 1 && check.StoredPressure == 2
                    && check.CauseIds.Count == 2 && check.CauseIds.All(id => state.ExpeditionPressureChanges.Any(x => x.Id == id
                        && x.Kind == ExpeditionPressureChangeKind.OpenCombat))
                    && rise.SourceId == outgoing.Id && rise.SourceRevision == exit.Revision && rise.At == exit.At
                    && rise.WatchIndex == check.WatchIndex + 1 && check.Consequence == ExpeditionPressureConsequenceKind.None
                    && ExpeditionPressureRules.CurrentAt(state, cohort, exit.Revision - 1, exit.At) == 1
                    && ExpeditionPressureRules.Current(state, cohort) == 3,
                    "The real closing Watch and the later same-receipt retreat cause were double counted or reversed.");
                var alignedReplay = SaveBill(aligned, RetreatPolicy(7), directory, "exp07-retreat-same-watch-exit");
                foreach (var run in new[] { aligned, alignedReplay }) {
                    WorldAdvance(run, 28800);
                    var next = run.Capture();
                    Require(next.ExpeditionPressureCheckpoints.Length == 2
                        && next.ExpeditionPressureCheckpoints.Last().PressureBefore == 3
                        && next.ExpeditionPressureCheckpoints.Last().StoredPressure == 3
                        && next.ExpeditionPressureCheckpoints.Last().CauseIds.Count == 0
                        && next.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat) == 1,
                        "The next actual Watch charged the same retreat or invented pursuit.");
                }
                Require(Bytes(aligned).SequenceEqual(Bytes(alignedReplay)), "The next Watch replay diverged.");
                SaveBill(aligned, RetreatPolicy(7), directory, "exp07-retreat-following-watch");

                var obstruction = RetreatReady(RetreatPolicy(42), early: true, delay: 57455, denominator: 2);
                LaterCommit(obstruction, RetreatInstruction(obstruction));
                PlayRetreatToOutcome(obstruction, fork: true);
                var obstructed = obstruction.Capture();
                var closure = obstructed.ExpeditionPressureCheckpoints.Single();
                var attempt = obstructed.Retreat.Round.Settlement;
                Require(attempt.Outcome == RetreatOutcome.PhysicallyBlocked && obstructed.Retreat.Escape >= 3
                    && attempt.LeadCrossingId != "" && attempt.CompanionCrossingId != "" && obstructed.InventoryCombat
                    && closure.At == attempt.At && closure.AppliedRevision == attempt.Revision && closure.Natural == 2
                    && closure.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && closure.ConsequenceEndsAt > closure.At
                    && obstructed.ExpeditionPressureChanges.All(x => x.Kind != ExpeditionPressureChangeKind.SuccessfulRetreat),
                    "An actual Watch obstruction did not defeat the already paid physical route at the boundary.");
                SaveBill(obstruction, RetreatPolicy(42), directory, "exp07-retreat-same-watch-obstruction");

                var work = ReinforcementStaged(RetreatPolicy());
                const string filledSkin = "TEST_ONLY.pack-skin";
                const string emptySkin = TestOnlyFillingPolicy.CompanionSkinId;
                PlanWalk(work, 0, 1);
                LaterCommit(work, Portable(work, CommandKind.HandlePortableEquipment, filledSkin, SaleBuyer, HandlingKind.Handover));
                LaterCommit(work, Portable(work, CommandKind.HandlePortableEquipment, emptySkin, SaleBuyer,
                    HandlingKind.Handover, ReinforcingCompanion));
                LaterCommit(work, IC(work, CommandKind.StartWaterFill, "TEST_ONLY.pack-water", new InventoryRequest(Q(1), emptySkin), SaleBuyer));
                PlanWalk(work, 0, -1);
                EnterLater(work);
                LaterCommit(work, ReinforcementCommand(work));
                EndReinforcementTurn(work);
                EndReinforcementTurn(work);
                var priorWork = work.Capture().WaterFills.Single();
                LaterCommit(work, RetreatInstruction(work));
                RetreatPlayRound(work);
                var later = work.Capture();
                var filling = later.WaterFills.Single();
                Require(filling.WorkerId == SaleBuyer && filling.Status == WaterFillStatus.Working
                    && filling.Progress == priorWork.Progress.AddSeconds(6)
                    && later.Work.WorkerIntervals.Count(x => x.JobId == filling.Id) == 1
                    && ReinforcementPlanting(later).Progress == T(2),
                    "The paid retreat round did not advance independent remote labor on the shared clock.");
                SaveBill(work, RetreatPolicy(), directory, "exp07-retreat-remote-work");
                Require(ExpeditionPressureRules.Settle(0, false, 0, 1) == 1
                    && ExpeditionPressureRules.Settle(6, true, 0, 1) == 6,
                    "The shared Pressure rules lost the Known Risk floor or cap.");
            });

            cases.Add("exp07_living_retreat_connected_living_archive_and_canonical_replay", () =>
            {
                var sim = RetreatReady();
                var admitted = sim.Capture();
                for (int turn = 0; turn < 6; turn++) {
                    if (sim.Capture().Encounter.CurrentActor == LaterDefender) {
                        LaterStance(sim, CombatStance.Guarded);
                        RetreatThreat(sim);
                    }
                    EndReinforcementTurn(sim);
                }
                var before = sim.Capture();
                Require(before.Encounter.Round == 4 && before.ExpeditionPressureChanges.Count(x =>
                    x.Kind == ExpeditionPressureChangeKind.OpenCombat) == 2 && Life(sim, LaterDefender).Hp == 8,
                    "The ordinary pre-declaration combat or its live Pressure causes were lost.");
                SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-connected-before-declaration");
                var declare = RetreatInstruction(sim);
                LaterCommit(sim, declare);
                for (int i = 0; i < 4; i++) RetreatPlayRound(sim);
                var beforeExit = sim.Capture();
                Require(beforeExit.Retreat.Active && beforeExit.Retreat.Escape == 2 && beforeExit.Retreat.Pursuit == 2,
                    "The connected attempt did not reach its real final paid round.");
                var replay = SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-connected-final-round");
                Command outgoing = null;
                foreach (var run in new[] { sim, replay }) {
                    outgoing = RetreatPlayRound(run);
                    var closed = run.Capture();
                    var exit = closed.Retreat.SuccessfulExit;
                    var archive = closed.ClosedEncounters.Last();
                    Require(exit != null && exit.At == T(23283, 2) && closed.Retreat.Escape == 3 && closed.Retreat.Pursuit == 2
                        && closed.Retreat.Rounds.Select(x => x.Task.Natural).SequenceEqual(new[] { 15, 7, 15, 10, 14 })
                        && closed.ClosedEncounters.Length == 2 && closed.ClosedEncounters[0].Reason == admitted.ClosedEncounters[0].Reason
                        && closed.CharterAttempt.Returned.Revision == admitted.CharterAttempt.Returned.Revision
                        && archive.Encounter.Id == before.Encounter.Id && archive.Encounter.RosterPhase.Epoch.Order.Contains(ReinforcingCompanion)
                        && archive.ClosedRevision == exit.Revision && archive.ClosedAt == exit.At && archive.Reason == outgoing.Id
                        && archive.Encounter.ObservedOrdinals.Last() == exit.EndTurn && archive.Encounter.ActorAt(exit.EndTurn) == outgoing.Actor
                        && closed.Encounter == null && !closed.InventoryCombat && Life(run, LaterDefender).Hp == 8
                        && ReinforcementPlanting(closed).Progress == T(2) && closed.RouteTravels.Length == admitted.RouteTravels.Length
                        && closed.ExpeditionPressureCheckpoints.Length == 0
                        && ExpeditionPressureRules.Current(closed, closed.Retreat.Definition.CohortId) == 2
                        && closed.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat) == 1,
                        "Connected exit changed the real archive, earlier charter, work, or ordinary resource state.");
                    Require(EncounterHistory.LatestStartOrdinal(closed, archive.Encounter.ActorAt(exit.EndTurn + 1)) < exit.EndTurn + 1,
                        "The archived round manufactured the next combat Start.");
                    var bytes = Bytes(run);
                    Require(run.Execute(host, declare).Outcome == Outcome.Duplicate && run.Execute(host, outgoing).Outcome == Outcome.Duplicate
                        && Bytes(run).SequenceEqual(bytes), "A duplicate issued time, RNG, or Pressure.");
                    RejectUnchanged(run, host, new Command(declare.Id, declare.Actor, declare.ExpectedRevision, declare.Kind, "changed"),
                        "CommandIdConflict");
                    RejectUnchanged(run, host, RetreatInstruction(run), "RetreatEncounterUnavailable");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "The same actual terminal round did not replay byte-identically.");
                var continued = SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-connected-exit");
                foreach (var run in new[] { sim, continued }) {
                    var prior = run.Capture();
                    PlanWalk(run, 0, -1);
                    var next = run.Capture();
                    Require(Body(run).Y == 0 && Body(run, ReinforcingCompanion).Y == 1 && next.RuleClock > prior.RuleClock
                        && next.RandomState == prior.RandomState && next.Encounter == null
                        && next.ClosedEncounters.Last().ClosedRevision == prior.ClosedEncounters.Last().ClosedRevision
                        && next.ExpeditionPressureExposures.Single().Id == prior.ExpeditionPressureExposures.Single().Id
                        && ExpeditionPressureRules.Current(next, next.Retreat.Definition.CohortId) == 2,
                        "Ordinary physical continuation changed the phased exit or its Pressure history.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(continued)), "Ordinary continuation failed deterministic replay.");
                SaveBill(sim, RetreatPolicy(), directory, "exp07-retreat-connected-continued");
            });

            cases.Add("exp07_living_retreat_save_authority_and_isolated_provenance", () =>
            {
                var legacyPressure = PressurePolicy(initialPressure: 2).Initial();
                var cohort = legacyPressure.ExpeditionPressureCohorts.Single();
                var codec = new SnapshotCodec();
                var original = codec.Encode(legacyPressure);
                Require(codec.Encode(codec.Decode(original)).SequenceEqual(original),
                    "The original one-member Pressure envelope did not roundtrip.");
                legacyPressure.ExpeditionPressureCohorts = new[] {
                    ExpeditionPressureCohortRecord.ForLocalRetreat(cohort.Id, cohort.ProfileFingerprint, cohort.RouteFingerprint,
                        cohort.InitialPressure, new[] { cohort.Members[0], TestOnlyPolicy.CompanionId })
                };
                Throws<ArgumentException>(() => codec.Encode(legacyPressure));

                var old = ReinforcementStaged(ReinforcementPolicy(7), early: true);
                EnterLater(old);
                LaterCommit(old, ReinforcementCommand(old));
                EndReinforcementTurn(old);
                EndReinforcementTurn(old);
                Require(old.Capture().SchemaVersion == Snapshot.ReinforcementSchema && old.Capture().Retreat == null
                    && old.Capture().ExpeditionPressureCohorts.Length == 0, "The older profile selected local retreat authority.");
                var oldReplay = SaveBill(old, ReinforcementPolicy(7), directory, "exp07-retreat-control-schema87");
                var oldExit = Tac(oldReplay, CommandKind.EndFixedEncounter);
                RejectUnchanged(oldReplay, host, oldExit, "ConflictNotResolved");
                RejectUnchanged(oldReplay, host, new Command("test.old-retreat", PlanHero, oldReplay.Capture().Revision,
                    CommandKind.DeclareRetreat, "TEST_ONLY.fl15.north-withdrawal.v1"), "ClubCommandNotImplemented");

                var run = RetreatReady(RetreatPolicy(7), early: true, delay: 57431, denominator: 2);
                var before = run.Capture();
                Throws<InvalidOperationException>(() => new Simulation(RetreatPolicy(7), before, ExecutionProfile.Release));
                Throws<ArgumentException>(() => new Simulation(ReinforcementPolicy(7), before, ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(RetreatPolicy(7, profile:
                    new TestOnlyLivingOpponentRetreatProfile(companionConsents: false)), before, ExecutionProfile.Laboratory));
                LaterCommit(run, RetreatInstruction(run));
                PlayRetreatToOutcome(run, fork: true);
                var exit = run.Capture().Retreat.SuccessfulExit;
                Require(exit != null && exit.At == T(28800), "The provenance witness did not produce the real Watch tie.");
                RejectRetreatSave(run, 7, s => {
                    var r = s.Retreat.Round;
                    var t = r.Task;
                    var task = new RetreatTaskRecord(t.Revision, t.CommandId, t.At, t.Turn, t.Modifier + 1, t.First, t.Second,
                        t.RandomBefore, t.RandomAfter, t.WordsConsumed, t.Degree);
                    s.Retreat = s.Retreat.WithRound(r.WithTask(task).Settle(r.Settlement));
                }, "InvalidSharedWorldReplay");
                RejectRetreatSave(run, 7, s => {
                    var r = s.Retreat.Round;
                    s.Retreat = s.Retreat.WithRound(r.WithThreat(s.Retreat.Rounds[0].ThreatId).Settle(r.Settlement));
                }, "Invalid actual retreat threat");
                RejectRetreatSave(run, 7, s => {
                    var r = s.Retreat.Round;
                    var t = r.Task;
                    var task = new RetreatTaskRecord(t.Revision, t.CommandId, t.At, t.Turn, t.Modifier, t.First, t.Second,
                        t.RandomBefore, t.RandomAfter, t.WordsConsumed, RetreatTaskDegree.Failure);
                    s.Retreat = s.Retreat.WithRound(r.WithTask(task).Settle(r.Settlement));
                }, "does not follow its earned counters");
                RejectRetreatSave(run, 7, s => {
                    var x = s.Retreat.SuccessfulExit;
                    s.Retreat = s.Retreat.WithRound(s.Retreat.Round.Settle(new RetreatSettlement(x.Outcome, x.Revision, x.CommandId,
                        x.At, x.EndTurn, x.Lead, x.Companion, x.Defender, x.CompanionCrossingId, x.LeadCrossingId)));
                }, "Invalid paid retreat crossing");
                RejectRetreatSave(run, 7, s => {
                    var x = s.Retreat.SuccessfulExit;
                    s.Retreat = s.Retreat.WithRound(s.Retreat.Round.Settle(new RetreatSettlement(x.Outcome, x.Revision, x.CommandId,
                        x.At, x.EndTurn, new RetreatPosition(x.Lead.X, 0), x.Companion, x.Defender, x.LeadCrossingId, x.CompanionCrossingId)));
                }, "InvalidSharedWorldReplay");
                RejectRetreatSave(run, 7, s => {
                    s.ExpeditionPressureChanges = s.ExpeditionPressureChanges.Select(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat
                        ? new ExpeditionPressureChangeRecord(x.Id, x.CohortId, x.ExposureId, x.RouteId, x.WatchIndex, x.Kind,
                            "test.forged-retreat-cause", x.SourceRevision, x.At) : x).ToArray();
                }, "Invalid expedition-pressure references or checkpoints");
                RejectRetreatSave(run, 7, s => {
                    s.ExpeditionPressureChanges = s.ExpeditionPressureChanges.Select(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat
                        ? new ExpeditionPressureChangeRecord(x.Id, x.CohortId, x.ExposureId, x.RouteId, x.WatchIndex - 1, x.Kind,
                            x.SourceId, x.SourceRevision, x.At) : x).ToArray();
                }, "Invalid expedition-pressure references or checkpoints");
                RejectRetreatSave(run, 7, s => {
                    var a = s.ClosedEncounters.Last();
                    s.ClosedEncounters = s.ClosedEncounters.Take(s.ClosedEncounters.Length - 1)
                        .Append(new ClosedEncounterRecord(a.Encounter, a.ClosedRevision, a.ClosedAt, "test.forged-exit")).ToArray();
                }, "Invalid later encounter exit provenance");
                SaveBill(run, RetreatPolicy(7), directory, "exp07-retreat-unaltered-provenance");
            });
        }
    }
}
#endif
