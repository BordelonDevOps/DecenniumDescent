#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
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
        private const string SurprisePack = "TEST_ONLY.pack-skin";
        private static TestOnlySharedWorldPolicy SurprisePolicy(SurpriseAwareness outcome = SurpriseAwareness.Surprised,
            ConditionCombatFixture conditions = null)
            => ReengagementPolicy(conditions: conditions).EnableSurpriseAwareEntry(outcome);

        private static void SurpriseDefenderLeavesReach(Simulation sim)
        {
            LaterStance(sim, CombatStance.Guarded);
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 4));
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 2, y: 3));
        }

        private static void SurpriseDefenderFinishesFirstTurn(Simulation sim)
        {
            if (TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null)
                LaterCommit(sim, Opportunity(sim, false));
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 4));
            LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
        }

        private static Simulation SurpriseFirstTurn(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = LaterPrepared(policy ?? SurprisePolicy());
            EnterLater(sim);
            SurpriseDefenderLeavesReach(sim);
            SurpriseDefenderFinishesFirstTurn(sim);
            return sim;
        }

        private static Command SurpriseClub(Simulation sim) => Tac(sim, CommandKind.AttackClub, LaterDefender,
            weapon: TestOnlyClubAttackPolicy.ActorClub, press: PressHitInstruction.KeepExisting);

        private static void SurpriseQuery(Simulation sim, Command command, string code)
        {
            var before = Bytes(sim);
            var query = sim.QueryCommand(LaterHost(), command);
            Require(query.Supported && query.Admissible == (code == "Available") && query.Code == code
                && (query.Admissible || query.Costs.Count == 0) && before.SequenceEqual(Bytes(sim)),
                command.Kind + " query expected " + code + ", got " + query.Code);
        }

        private static ConditionPermissions ProjectSurprisePermissions(Type policy, string method, Snapshot state)
            => (ConditionPermissions)policy.GetMethod(method, BindingFlags.Static | BindingFlags.NonPublic)
                .Invoke(null, new object[] { state, PlanHero });

        private static void RejectSurpriseForgery(Simulation sim, Action<Snapshot> change, string reason)
        {
            var state = sim.Capture();
            change(state);
            var codec = new SnapshotCodec();
            string rejection = null;
            try { new Simulation(SurprisePolicy(), codec.Decode(codec.Encode(state)), ExecutionProfile.Laboratory); }
            catch (ArgumentException error) { rejection = error.Message; }
            Require(rejection?.Contains(reason) == true, "Expected " + reason + ", got " + (rejection ?? "accepted"));
        }

        private static void AddSurpriseEntryCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp07_surprise_entry_connected_director_and_physical_contact", () =>
            {
                var surprised = LaterPrepared(SurprisePolicy());
                var warned = LaterPrepared(SurprisePolicy(SurpriseAwareness.Warned));
                var before = surprised.Capture();
                Require(before.SchemaVersion == Snapshot.SurpriseEntrySchema && before.SurpriseEntry.Decision == null
                    && before.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                    && before.ContentFingerprint != warned.Capture().ContentFingerprint,
                    "The opt-in decisions must be bound before genuine contact and differ by awareness.");
                SaveBill(surprised, SurprisePolicy(), directory, "exp07-surprise-before-approach");
                foreach (var sim in new[] { surprised, warned }) {
                    LaterCommit(sim, LaterApproach(sim));
                    LaterCommit(sim, LaterAdvance(sim, 1, 2));
                    var partial = sim.Capture();
                    Require(partial.RuleClock == T(23157, 2) && partial.SurpriseEntry.Decision == null
                        && partial.LaterEncounter.Entry == null && partial.RandomState == before.RandomState
                        && partial.WorldTraversals.Single().DistanceFeet == Q(5, 3),
                        "A partial physical approach applied surprise or consumed initiative.");
                    LaterCommit(sim, LaterAdvance(sim));
                }

                var s = surprised.Capture();
                var w = warned.Capture();
                Require(s.SurpriseEntry.SurprisePending && !w.SurpriseEntry.SurprisePending
                    && s.SurpriseEntry.Binding.ThreatId == LaterDefender && s.SurpriseEntry.Binding.ParticipantId == PlanHero
                    && s.SurpriseEntry.Decision.At == T(23159, 2) && w.RuleClock == s.RuleClock
                    && s.SurpriseEntry.Decision.Revision == s.LaterEncounter.Entry.ArrivalRevision
                    && s.SurpriseEntry.Decision.CommandId == s.LaterEncounter.Entry.ArrivalCommandId
                    && s.Encounter.CurrentActor == LaterDefender && s.Encounter.ObservedOrdinals.SequenceEqual(new[] { 0 })
                    && s.LaterEncounter.Entry.Draws.Select(x => x.Total).SequenceEqual(new[] { 9, 12 })
                    && s.LaterEncounter.Entry.Draws.Zip(w.LaterEncounter.Entry.Draws, (a, b) =>
                        a.ActorId == b.ActorId && a.RandomBefore == b.RandomBefore && a.RandomAfter == b.RandomAfter).All(x => x)
                    && s.RandomState == w.RandomState && Body(surprised).X == 0 && Body(surprised).Y == 3
                    && Body(surprised, LaterDefender).Y == 4,
                    "Actual contact, selected Director authority, or existing initiative diverged.");
                SaveBill(surprised, SurprisePolicy(), directory, "exp07-surprise-entered");
                SaveBill(warned, SurprisePolicy(SurpriseAwareness.Warned), directory, "exp07-warned-entered");

                var fixture = new ConditionCombatFixture(
                    CCApply("surprise-blinded-defender", "Blinded", LaterDefender, at: new ConditionStamp(T(23157, 2))));
                var invalid = LaterPrepared(SurprisePolicy(conditions: fixture));
                Require(invalid.Capture().SurpriseEntry.Decision == null && invalid.Capture().LaterEncounter.FirstExit != null,
                    "The actual unrelated earlier conflict must not apply surprise.");
                LaterCommit(invalid, LaterApproach(invalid));
                LaterCommit(invalid, LaterAdvance(invalid, 1, 2));
                var failedBefore = invalid.Capture();
                LaterCommit(invalid, CCCommand(invalid, "surprise-blinded-defender", LaterDefender));
                var failed = LaterCommit(invalid, LaterAdvance(invalid));
                var failedAfter = invalid.Capture();
                Require(failed.Code == "LaterEncounterAwarenessUnavailable" && failed.TacticalDecisionAt == null
                    && failedAfter.SurpriseEntry.Decision == null && failedAfter.LaterEncounter.Entry == null
                    && failedAfter.RandomState == failedBefore.RandomState && failedAfter.RuleClock == s.RuleClock
                    && WorldLedger(invalid).MovementSpent == Q(5) && Body(invalid).X == 0,
                    "A genuine failed arrival must preserve paid movement without applying surprise or drawing initiative.");
                SaveBill(invalid, SurprisePolicy(conditions: fixture), directory, "exp07-surprise-failed-actual-arrival");
                var authority = s.SurpriseEntry.Binding;
                Throws<ArgumentException>(() => new SurpriseAwarenessBinding(authority.SourceRevision, "", authority.EncounterId,
                    authority.ParticipantId, authority.ThreatId, authority.EvidenceId, authority.Outcome));
                Throws<ArgumentException>(() => new SurpriseAwarenessBinding(authority.SourceRevision, authority.DirectorId,
                    authority.EncounterId, authority.ParticipantId, authority.ThreatId,
                    SurpriseAwarenessBinding.EvidenceFor(SurpriseAwareness.Warned), authority.Outcome));
                var priorThreat = before.Copy();
                priorThreat.ObserverKnowledge = new[] { new ObserverKnowledgeRecord(PlanHero, LaterDefender, true, true,
                    Q(0), Q(4), ObservationEvidenceKind.AttackEvidence, before.RuleClock, before.Revision) };
                var approach = new Command("test.surprise-prior-threat", PlanHero, before.Revision, CommandKind.BeginWorldStep, "walk", -1, 0);
                Require(SurprisePolicy().QueryCommand(priorThreat, host, approach).Code == "LaterEncounterAwarenessContradicted"
                    && !SurpriseEntryValidation.ConflictingAwareness(priorThreat, w.SurpriseEntry.Binding, before.Revision + 1),
                    "Explicit previously represented hostile evidence must contradict the surprise basis only.");
                priorThreat.ObserverKnowledge = new[] { new ObserverKnowledgeRecord(PlanHero, LaterDefender, true, true,
                    Q(0), Q(4), ObservationEvidenceKind.DirectSight, before.RuleClock, before.Revision) };
                Require(SurprisePolicy().QueryCommand(priorThreat, host, approach).Admissible,
                    "Ordinary location knowledge alone must not establish advance warning of a threat.");
                File.WriteAllLines(Path.Combine(directory, "exp07-surprise-entry.tsv"), new[] {
                    "profile\tarrival\tapproachRevision\tarrivalRevision\tinitiative\trandom\tawareness",
                    "surprised\t" + s.RuleClock + "\t" + s.LaterEncounter.Entry.ApproachRevision + "\t" + s.Revision
                        + "\t9,12\t" + s.RandomState + "\t" + authority.EvidenceId,
                    "warned\t" + w.RuleClock + "\t" + w.LaterEncounter.Entry.ApproachRevision + "\t" + w.Revision
                        + "\t9,12\t" + w.RandomState + "\t" + w.SurpriseEntry.Binding.EvidenceId,
                    "failed arrival\t" + failedAfter.RuleClock + "\t" + failedAfter.LaterEncounter.Interruptions.Single().ApproachRevision
                        + "\t" + failedAfter.Revision + "\t\t" + failedAfter.RandomState + "\t" + failed.Code
                });
            });

            cases.Add("exp07_surprise_entry_reaction_actual_start_end_and_new_trigger", () =>
            {
                var surprised = LaterPrepared(SurprisePolicy());
                var warned = LaterPrepared(SurprisePolicy(SurpriseAwareness.Warned));
                EnterLater(surprised);
                EnterLater(warned);
                Require(!Resources(surprised).ReactionAvailable && Resources(warned).ReactionAvailable,
                    "Genuine entry must suppress only the surprised hero's initial ordinary Reaction.");
                SurpriseDefenderLeavesReach(surprised);
                SurpriseDefenderLeavesReach(warned);
                var offer = TestOnlyClubAttackPolicy.PendingMove(warned.Capture());
                var s = surprised.Capture();
                Require(offer?.Reactors.SequenceEqual(new[] { PlanHero }) == true
                    && TestOnlyClubAttackPolicy.PendingMove(s) == null && s.TacticalMoves.Last().Status == TacticalMoveStatus.Completed
                    && s.TacticalMoves.Last().ActorId == LaterDefender && s.TacticalMoves.Last().CostPaid == 5
                    && s.SurpriseEntry.FirstStart == null && !s.MeleeAttacks.Any(x => x.Opportunity
                        && x.Revision > s.SurpriseEntry.Decision.Revision),
                    "Actual leave-reach must complete without banking or fabricating the suppressed opportunity.");
                SurpriseDefenderFinishesFirstTurn(surprised);
                SurpriseDefenderFinishesFirstTurn(warned);
                var first = surprised.Capture();
                Require(first.RuleClock == T(23165, 2) && first.SurpriseEntry.FirstStart.Ordinal == 1
                    && first.SurpriseEntry.SurprisePending && Resources(surprised).ReactionAvailable
                    && !ProjectSurprisePermissions(typeof(TestOnlyClubAttackPolicy), "CurrentPermissions", first).Reaction,
                    "Normal first Start must refresh the existing ordinary resource while keeping it unusable.");
                var premature = Tac(surprised, CommandKind.EndRegularTurn);
                SurpriseQuery(surprised, premature, "StanceRequired");
                RejectUnchanged(surprised, host, premature, "StanceRequired");
                var end = EndReinforcementTurn(surprised);
                var completed = surprised.Capture();
                Require(completed.RuleClock == T(23171, 2) && completed.SurpriseEntry.FirstEnd.EndCommandId == end.Id
                    && completed.SurpriseEntry.FirstEnd.CompletedRevision == completed.Revision
                    && !completed.SurpriseEntry.SurprisePending && Resources(surprised).ReactionAvailable,
                    "Only actual first End may unlock the already-refreshed ordinary Reaction.");
                var bytes = Bytes(surprised);
                Require(surprised.Execute(host, end).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(surprised)),
                    "A duplicate End changed the lifecycle or Reaction.");
                RejectUnchanged(surprised, host, new Command(end.Id, end.Actor, completed.Revision,
                    CommandKind.EndRegularTurn, end.Target), "CommandIdConflict");
                LaterStance(surprised, CombatStance.Guarded);
                LaterCommit(surprised, Tac(surprised, CommandKind.TacticalStep, x: 2, y: 3));
                var newOffer = TestOnlyClubAttackPolicy.PendingMove(surprised.Capture());
                Require(newOffer?.Reactors.SequenceEqual(new[] { PlanHero }) == true && newOffer.Id != offer.Id,
                    "The actual new leave-reach event after End must offer the ordinary Reaction.");
                LaterCommit(surprised, Opportunity(surprised, true, TestOnlyClubAttackPolicy.ActorClub));
                var attack = surprised.Capture().MeleeAttacks.Last();
                Require(attack.Opportunity && attack.AttackerId == PlanHero && !Resources(surprised).ReactionAvailable,
                    "A genuine after-End attack must spend the existing Reaction.");
                SaveBill(surprised, SurprisePolicy(), directory, "exp07-surprise-after-reactive-attack");
                File.WriteAllLines(Path.Combine(directory, "exp07-surprise-reaction.tsv"), new[] {
                    "warned offer " + offer.Id, "surprised before-Start paid step without offer " + s.TacticalMoves.Last().Id,
                    "hero first Start " + first.RuleClock + " ordinal " + first.SurpriseEntry.FirstStart.Ordinal,
                    "hero first End " + completed.RuleClock + " " + end.Id,
                    "new trigger " + newOffer.Id + " paid attack " + attack.Id
                });
            });

            cases.Add("exp07_surprise_entry_first_turn_permissions_and_costs", () =>
            {
                var sim = SurpriseFirstTurn();
                var warned = SurpriseFirstTurn(SurprisePolicy(SurpriseAwareness.Warned));
                LaterStance(sim, CombatStance.Guarded);
                LaterStance(warned, CombatStance.Guarded);
                var start = sim.Capture();
                var shared = ProjectSurprisePermissions(typeof(TestOnlySharedWorldPolicy), "Permissions", start);
                var tactical = ProjectSurprisePermissions(typeof(TestOnlyClubAttackPolicy), "CurrentPermissions", start);
                var aware = ProjectSurprisePermissions(typeof(TestOnlySharedWorldPolicy), "Permissions", warned.Capture());
                Require(!shared.Action && !shared.BonusAction && !shared.VoluntarySpeed && !shared.Dash
                    && !tactical.BonusAction && !tactical.Reaction && tactical.ConcentrationMayContinue && aware.BonusAction
                    && !start.CharacterFeatureGrants.Any(x => x.ActorId == PlanHero)
                    && start.BonusActions.Single(x => x.ActorId == PlanHero).Available
                    && TestOnlyClubAttackPolicy.ActiveStance(start, PlanHero)?.Kind == CombatStance.Guarded,
                    "Restriction must preserve ordinary stance and raw resources while denying shared permissions.");
                foreach (var kind in new[] { CommandKind.TacticalStep, CommandKind.AttackClub }) {
                    var restricted = kind == CommandKind.TacticalStep ? Tac(sim, kind, x: 0, y: 2) : SurpriseClub(sim);
                    var legal = kind == CommandKind.TacticalStep ? Tac(warned, kind, x: 0, y: 2) : SurpriseClub(warned);
                    string code = kind == CommandKind.TacticalStep ? "ConditionPreventsMovement" : "ConditionPreventsAction";
                    SurpriseQuery(warned, legal, "Available");
                    SurpriseQuery(sim, restricted, code);
                    RejectUnchanged(sim, host, restricted, code);
                }

                foreach (var run in new[] { sim, warned }) {
                    var free = Portable(run, CommandKind.HandlePortableEquipment, SurprisePack, handling: HandlingKind.Drop);
                    SurpriseQuery(run, free, "Available");
                    LaterCommit(run, free);
                }
                var dropped = sim.Capture();
                Require(dropped.RuleClock == start.RuleClock && dropped.RandomState == start.RandomState
                    && WorldLedger(sim).Interactions == 1 && !WorldLedger(sim).ActionSpent
                    && dropped.PortableEquipment.Single(x => x.Id == SurprisePack).Placement == PortablePlacement.Ground,
                    "A lawful free drop must spend only its real interaction.");
                var second = Portable(sim, CommandKind.HandlePortableEquipment, SurprisePack, handling: HandlingKind.Pickup);
                var awareSecond = Portable(warned, CommandKind.HandlePortableEquipment, SurprisePack, handling: HandlingKind.Pickup);
                SurpriseQuery(sim, second, "ConditionPreventsAction");
                RejectUnchanged(sim, host, second, "ConditionPreventsAction");
                SurpriseQuery(warned, awareSecond, "Available");
                LaterCommit(warned, awareSecond);
                Require(WorldLedger(warned).Interactions == 2 && WorldLedger(warned).ActionSpent,
                    "The comparable second handling must actually spend an Action.");
                LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
                EndReinforcementTurn(sim);
                LaterStance(sim, CombatStance.Guarded);
                SurpriseQuery(sim, SurpriseClub(sim), "Available");
                LaterCommit(sim, SurpriseClub(sim));
                Require(WorldLedger(sim).ActionSpent && sim.Capture().MeleeAttacks.Last().AttackerId == PlanHero,
                    "The next genuine hero turn must admit a real voluntary Club Action.");
                SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-later-paid-action");
            });

            cases.Add("exp07_surprise_entry_passive_expiry_and_concurrent_work", () =>
            {
                var expiry = new ConditionStamp(T(23179, 2));
                var fixture = new ConditionCombatFixture(new ConditionFixtureEvent(PlanHero,
                    ConditionOperation.Apply("event.surprise-passive", new ConditionStamp(T(11584)),
                        new ConditionApplicationData("surprise-passive", PlanHero, "TEST_ONLY.existing-condition-event",
                            "Poisoned", expiry, "absolute-time", true))));
                var sim = LaterPrepared(SurprisePolicy(conditions: fixture));
                PlanWalk(sim, -1, 0, ReinforcingCompanion);
                FarmWork(sim, CommandKind.PlantCrop);
                LaterCommit(sim, CCCommand(sim, "surprise-passive"));
                EnterLater(sim);
                SurpriseDefenderLeavesReach(sim);
                SurpriseDefenderFinishesFirstTurn(sim);
                var start = sim.Capture();
                var progress = ReinforcementPlanting(start).Progress;
                Require(start.RuleClock == T(23177, 2) && progress == T(9, 2)
                    && start.SurpriseEntry.SurprisePending && ViewCondition(sim, "surprise-passive").EndedAt == null,
                    "The real first slot must begin with its independently scheduled effect and working companion.");
                var replay = SaveBill(sim, SurprisePolicy(conditions: fixture), directory, "exp07-surprise-passive-at-start");
                foreach (var run in new[] { sim, replay }) {
                    EndReinforcementTurn(run, CombatStance.Focused);
                    var end = run.Capture();
                    Require(end.RuleClock == T(23183, 2) && !end.SurpriseEntry.SurprisePending
                        && ViewCondition(run, "surprise-passive").EndedAt?.Time == expiry.Time
                        && ReinforcementPlanting(end).Progress == T(15, 2) && ReinforcementPlanting(end).Status == CropWorkStatus.Working,
                        "The actual slot must expire the existing effect and credit the concurrent work exactly once.");
                    LaterStance(run, CombatStance.Guarded);
                    LaterCommit(run, Tac(run, CommandKind.TacticalStep, x: 2, y: 3));
                    Require(TestOnlyClubAttackPolicy.PendingMove(run.Capture()) == null
                        && Resources(run).ReactionAvailable && TestOnlyClubAttackPolicy.ActiveStance(run.Capture(), PlanHero)?.Kind == CombatStance.Focused,
                        "Clearing surprise must preserve the independent Focused Reaction prohibition.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Passive first-End continuation replay diverged.");
                SaveBill(sim, SurprisePolicy(conditions: fixture), directory, "exp07-surprise-passive-completed");
                File.WriteAllLines(Path.Combine(directory, "exp07-surprise-passive.tsv"), new[] {
                    "first Start " + start.RuleClock + " remote labor " + progress,
                    "existing passive expiry " + expiry.Time, "actual first End " + sim.Capture().SurpriseEntry.FirstEnd.At
                        + " remote labor " + ReinforcementPlanting(sim.Capture()).Progress,
                    "after-End Focused prohibited the real new leave-reach Reaction"
                });
            });

            cases.Add("exp07_surprise_entry_exact_saves_integrity_and_continuation", () =>
            {
                var sim = LaterPrepared(SurprisePolicy());
                LaterCommit(sim, LaterApproach(sim));
                LaterCommit(sim, LaterAdvance(sim, 1, 2));
                var replay = SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-partial");
                foreach (var run in new[] { sim, replay }) LaterCommit(run, LaterAdvance(run));
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Entry from a real partial approach must replay exactly.");
                replay = SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-before-hero-start");
                foreach (var run in new[] { sim, replay }) {
                    SurpriseDefenderLeavesReach(run);
                    SurpriseDefenderFinishesFirstTurn(run);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "First regular Start replay diverged.");
                RejectSurpriseForgery(sim, forged => {
                    var r = forged.SurpriseEntry;
                    var d = r.Binding;
                    forged.SurpriseEntry = new SurpriseEntryRecord(new SurpriseAwarenessBinding(d.SourceRevision, d.DirectorId,
                        d.EncounterId, d.ThreatId, d.ParticipantId, d.EvidenceId, d.Outcome), r.Decision, r.FirstStart);
                }, "does not identify this genuine encounter");
                RejectSurpriseForgery(sim, forged => {
                    var r = forged.SurpriseEntry;
                    forged.SurpriseEntry = new SurpriseEntryRecord(r.Binding,
                        new SurpriseEntryDecision(r.Decision.Revision, "test.false-arrival", r.Decision.At), r.FirstStart);
                }, "Invalid surprise entry");
                RejectSurpriseForgery(sim, forged => {
                    var r = forged.SurpriseEntry;
                    forged.SurpriseEntry = new SurpriseEntryRecord(r.Binding, r.Decision,
                        new SurpriseFirstStart(r.FirstStart.Revision, 0, r.FirstStart.At));
                }, "Invalid surprise first regular Start");
                RejectSurpriseForgery(sim, forged => {
                    var r = forged.SurpriseEntry;
                    var receipt = forged.Receipts.Last();
                    forged.SurpriseEntry = r.Complete(new SurpriseFirstEnd(receipt.Revision + 1, "test.early-end",
                        receipt.Revision + 1, r.FirstStart.At.AddSeconds(1)));
                }, "Invalid surprise first-End");
                RejectSurpriseForgery(sim, forged => forged.WorldIntervals = forged.WorldIntervals.Select(x => x.ActorId == PlanHero
                    ? x.PayAction() : x).ToArray(), "InvalidSharedWorldReplay");

                replay = SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-restricted-slot");
                foreach (var run in new[] { sim, replay }) EndReinforcementTurn(run);
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Actual first End did not replay byte-for-byte.");
                replay = SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-after-first-end");
                foreach (var run in new[] { sim, replay }) {
                    FinishLaterFight(run, defenderAttacked: true);
                    var closed = run.Capture();
                    Require(closed.ClosedEncounters.Length == 2 && closed.SurpriseEntry.FirstEnd.At == T(23171, 2)
                        && !closed.SurpriseEntry.SurprisePending && closed.Lives.Single(x => x.ActorId == LaterDefender).Dead,
                        "The actual later encounter must close without reapplying its entry decision.");
                    PlanWalk(run, 1, 0);
                    Require(!run.Capture().InventoryCombat && Body(run).X == 1 && Body(run).Y == 3
                        && run.Capture().RandomState == closed.RandomState, "Ordinary continuation must preserve shared world state.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Combat closure and ordinary continuation replay diverged.");
                SaveBill(sim, SurprisePolicy(), directory, "exp07-surprise-ordinary-continued");
            });

            cases.Add("exp07_surprise_entry_schema89_and_profile_authority_controls", () =>
            {
                var sim = LaterPrepared(ReengagementPolicy());
                EnterLater(sim);
                SurpriseDefenderLeavesReach(sim);
                var old = sim.Capture();
                Require(old.SchemaVersion == Snapshot.ReengagementSchema && old.SurpriseEntry == null
                    && TestOnlyClubAttackPolicy.PendingMove(old)?.Reactors.SequenceEqual(new[] { PlanHero }) == true,
                    "The selected schema 89 aware profile lost its original real opportunity or layout.");
                var prior = SaveBill(sim, ReengagementPolicy(), directory, "exp07-surprise-schema89-control");
                Throws<ArgumentException>(() => new Simulation(SurprisePolicy(), old, ExecutionProfile.Laboratory));
                var modern = SurprisePolicy().Initial();
                Throws<ArgumentException>(() => new Simulation(ReengagementPolicy(), modern, ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(SurprisePolicy(SurpriseAwareness.Warned), modern, ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(SurprisePolicy(), modern, ExecutionProfile.Release));
                var mutablePolicy = SurprisePolicy();
                mutablePolicy.Initial();
                Throws<InvalidOperationException>(() => mutablePolicy.EnableSurpriseAwareEntry(SurpriseAwareness.Warned));
                Throws<InvalidOperationException>(() => RetreatPolicy().EnableSurpriseAwareEntry(SurpriseAwareness.Surprised));
                SurpriseDefenderFinishesFirstTurn(sim);
                SurpriseDefenderFinishesFirstTurn(prior);
                Require(Bytes(sim).SequenceEqual(Bytes(prior)) && prior.Capture().SurpriseEntry == null,
                    "The schema 89 restore must continue with its original first Start.");
            });
        }
    }
}
#endif
