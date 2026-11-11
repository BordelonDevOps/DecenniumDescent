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
        private const string AppraisalWorker = TestOnlyHavenAppraisalProfile.WorkerId;
        private const string AppraisalDesk = TestOnlyHavenAppraisalProfile.DeskId;
        private const string AppraisalIron = SharedMiningFixture.UnitA;

        private static TestOnlySharedWorldPolicy AppraisalPolicy(TestOnlyHavenAppraisalProfile profile = null,
            ConditionCombatFixture conditions = null, bool legacy = false)
        {
            uint seed = 1;
            while (PlaytestDice.RollD20(seed).Natural != 12) seed++;
            var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
                new SupplyCacheFixture(), conditions: conditions).EnableMining(new SharedMiningFixture());
            return legacy ? policy : policy.EnableHavenAppraisal(profile ?? new TestOnlyHavenAppraisalProfile());
        }

        private static Command AppraisalCommand(Simulation s, CommandKind kind, string target = AppraisalDesk,
            string actor = AppraisalWorker)
            => MiningCommand(s, kind, target, actor: actor);

        private static Command AppraisalHandling(Simulation s, HandlingKind handling)
            => Portable(s, CommandKind.HandlePortableEquipment, AppraisalIron, handling: handling, actor: AppraisalWorker);

        private static void ExtractAppraisalIron(Simulation s)
        {
            MiningCommit(s, MiningCommand(s, CommandKind.StartMining, SharedMiningFixture.DepositId,
                MiningSelection(SharedMiningFixture.CategoryA)));
            WorldAdvance(s, 1800);
            Require(s.Capture().MiningUnits.Single(x => x.Id == AppraisalIron).Status == MiningUnitStatus.Extracted,
                "Extraction did not produce the exact iron subject.");
        }

        private static void PlaceIronAtAppraisalDesk(Simulation s)
        {
            PortableCommit(s, AppraisalHandling(s, HandlingKind.Retrieve));
            WorldStep(s, -1, 0, actor: AppraisalWorker);
            WorldAdvance(s, 6);
            PortableCommit(s, AppraisalHandling(s, HandlingKind.Drop));
            WorldAdvance(s, 6);
        }

        private static void ResolveAppraisalExpeditionEncounter(Simulation s)
        {
            WorldStep(s, 1, 0);
            WorldAdvance(s, 2);
            WorldStep(s, 1, 0);
            WorldAdvance(s, 2);
            WorldStep(s, 1, 0);
            Require(s.Capture().InventoryCombat, "Exploration did not enter the connected encounter.");
            WorldCommit(s, Tac(s, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
            TacStep(s, 3, 0);
            DefeatConnectedEnemy(s);
            WorldCommit(s, Tac(s, CommandKind.EndFixedEncounter));
        }

        private static void AddHavenAppraisalCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("mgt10_haven_appraisal_connected_whole_iron_fractional_pause_restore_replay", () =>
            {
                var policy = AppraisalPolicy();
                var s = PortableWorld(policy);
                ResolveAppraisalExpeditionEncounter(s);
                ExtractAppraisalIron(s);
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.StartHavenAppraisal), "AppraisalWholeSubjectNotAtDesk");
                PlaceIronAtAppraisalDesk(s);
                var subject = s.Capture().MiningUnits.Single(x => x.Id == AppraisalIron);
                var physical = s.Capture().PortableEquipment.Single(x => x.Id == AppraisalIron);
                Require(subject.ReceivedContainerId != "" && physical.ParentId == "" && physical.GroundX == 2 && physical.GroundY == 3,
                    "The original receipt and actual desk placement must both be retained.");
                MiningCommit(s, AppraisalCommand(s, CommandKind.StartHavenAppraisal));
                var job = s.Capture().HavenAppraisals.Single();
                WorldAdvance(s, 1, 2);
                MiningCommit(s, AppraisalCommand(s, CommandKind.PauseHavenAppraisal, job.Id));
                WorldAdvance(s, 6);
                Require(s.Capture().HavenAppraisals.Single().Work.Labor == T(1, 2)
                    && s.Capture().Work.AvailableAmount(AppraisalIron) == default, "Pause lost labor or the whole subject claim.");
                var path = Path.Combine(directory, "mgt10-haven-appraisal-paused.ddsave");
                new FileSaveStore().Save(path, s.Capture());
                var replay = new Simulation(AppraisalPolicy(), new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(replay).SequenceEqual(Bytes(s)), "Paused appraisal save changed on restore.");
                var audit = new List<string> { "event\tclock\trevision\twork\tlabor\tunit\tdepositVersion\towner\tcustodian\tquantity\tbaseCopper\tprovenance\tdemand\tcondition\turgency\tassessmentContext\tclearance\tevidence\tterms\tresultCopper" };
                audit.Add(AppraisalAuditRow("paused", s.Capture()));
                foreach (var run in new[] { s, replay })
                {
                    var old = run.Capture();
                    MiningCommit(run, AppraisalCommand(run, CommandKind.ResumeHavenAppraisal, job.Id));
                    WorldAdvance(run, 1799);
                    var almost = run.Capture().HavenAppraisals.Single();
                    Require(almost.Status == HavenAppraisalStatus.Working && almost.Work.Labor == T(3599, 2)
                        && !almost.ResultCopper.HasValue, "Appraisal produced a result before completing 1800 active seconds.");
                    WorldAdvance(run, 1, 2);
                    var end = run.Capture();
                    var report = end.HavenAppraisals.Single();
                    Require(report.Status == HavenAppraisalStatus.Completed && report.Work.Labor == T(1800)
                        && report.ResultCopper == new RuleQuantity(15, 2) && end.RandomState == old.RandomState,
                        "The exact report changed value, labor, or RNG.");
                    Require(end.Work.AvailableAmount(AppraisalIron) == subject.MassPounds
                        && end.PortableEquipment.Single(x => x.Id == AppraisalIron).CustodianId == AppraisalWorker
                        && end.InventoryLots.Single(x => x.LotId == AppraisalIron).OwnerId == AppraisalWorker
                        && end.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(old.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                        && end.CharacterAdvancements.Length == old.CharacterAdvancements.Length,
                        "Appraisal changed stock, ownership, custody, or advancement.");
                    if (run == s)
                    {
                        audit.Add(AppraisalAuditRow("completed", end));
                        string completePath = Path.Combine(directory, "mgt10-haven-appraisal-completed.ddsave");
                        new FileSaveStore().Save(completePath, end);
                        Require(Bytes(new Simulation(AppraisalPolicy(), new FileSaveStore().Load(completePath), ExecutionProfile.Laboratory))
                            .SequenceEqual(Bytes(run)), "Completed appraisal save changed on restore.");
                        Throws<ArgumentException>(() => new Simulation(AppraisalPolicy(legacy: true), end, ExecutionProfile.Laboratory));
                    }
                    RejectUnchanged(run, host, AppraisalCommand(run, CommandKind.StartHavenAppraisal), "AppraisalBasisAlreadyReported");
                    PortableCommit(run, AppraisalHandling(run, HandlingKind.Pickup));
                    WorldStep(run, 1, 0, actor: AppraisalWorker);
                    WorldAdvance(run, 1);
                    Require(run.Capture().HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2),
                        "Lawful continuation changed the historical report.");
                }
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "The connected appraisal continuation differed after replay.");
                audit.Add(AppraisalAuditRow("continued", s.Capture()));
                File.WriteAllLines(Path.Combine(directory, "appraisal-audit.tsv"), audit);
            });
            cases.Add("mgt10_haven_appraisal_pause_cancels_labor_and_retains_claim_until_cancel", () =>
            {
                var s = PortableWorld(AppraisalPolicy());
                ExtractAppraisalIron(s);
                PlaceIronAtAppraisalDesk(s);
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.StartHavenAppraisal, actor: TestOnlyPolicy.ActorId),
                    "AppraisalWorkerUnauthorized");
                var start = AppraisalCommand(s, CommandKind.StartHavenAppraisal);
                var before = Bytes(s);
                var query = s.QueryCommand(host, start);
                Require(query.Supported && query.Admissible && before.SequenceEqual(Bytes(s)), "Admission query wrote state or differed from execution.");
                MiningCommit(s, start);
                var opened = Bytes(s);
                Require(s.Execute(host, start).Outcome == Outcome.Duplicate && opened.SequenceEqual(Bytes(s)), "Duplicate opened a second booking.");
                var conflict = new Command(start.Id, start.Actor, start.ExpectedRevision, start.Kind, "different-desk");
                RejectUnchanged(s, host, conflict, "CommandIdConflict");
                var job = s.Capture().HavenAppraisals.Single();
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.StartHavenAppraisal), "AppraisalServiceSlotOccupied");
                RejectUnchanged(s, host, AppraisalHandling(s, HandlingKind.Pickup), "OffCalendarActionAlreadySpent");
                PortableCommit(s, Portable(s, CommandKind.HandlePortableEquipment, PortableKitFixture.Tools,
                    handling: HandlingKind.Retrieve));
                Require(s.Capture().HavenAppraisals.Single().Work.Labor == T(1),
                    "Another worker's ordinary handling failed to advance appraisal on the shared clock.");
                WorldAdvance(s, 1, 2);
                MiningCommit(s, AppraisalCommand(s, CommandKind.PauseHavenAppraisal, job.Id));
                WorldAdvance(s, 6);
                RejectUnchanged(s, host, AppraisalHandling(s, HandlingKind.Pickup), "PortableItemHasPendingWork");
                WorldStep(s, -1, 0, actor: AppraisalWorker);
                WorldAdvance(s, 6);
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.ResumeHavenAppraisal, job.Id), "AppraisalWorkerNotAtDesk");
                WorldStep(s, 1, 0, actor: AppraisalWorker);
                WorldAdvance(s, 6);
                MiningCommit(s, AppraisalCommand(s, CommandKind.CancelHavenAppraisal, job.Id));
                var cancelled = s.Capture().HavenAppraisals.Single();
                Require(cancelled.Status == HavenAppraisalStatus.Cancelled && cancelled.Work.Labor == T(3, 2)
                    && !cancelled.ResultCopper.HasValue && s.Capture().Work.AvailableAmount(AppraisalIron) == cancelled.Basis.Quantity,
                    "Cancellation paid, consumed the subject, or lost audit labor.");
                PortableCommit(s, AppraisalHandling(s, HandlingKind.Pickup));
            });
            cases.Add("mgt10_haven_appraisal_terms_and_finite_window_reject_unchanged", () =>
            {
                foreach (var pair in new[] {
                    (new TestOnlyHavenAppraisalProfile(cleared: false), "AppraisalClearanceMissing"),
                    (new TestOnlyHavenAppraisalProfile(evidenceAccessible: false), "AppraisalEvidenceUnavailable"),
                    (new TestOnlyHavenAppraisalProfile(termsAuthorized: false), "AppraisalTermsUnauthorized"),
                    (new TestOnlyHavenAppraisalProfile(instrumentsAvailable: false), "AppraisalDeskUnavailable"),
                    (new TestOnlyHavenAppraisalProfile(deskIntact: false), "AppraisalDeskUnavailable"),
                    (new TestOnlyHavenAppraisalProfile(availableFrom: 3000), "AppraisalAppointmentClosed") })
                {
                    var s = PortableWorld(AppraisalPolicy(pair.Item1));
                    ExtractAppraisalIron(s);
                    PlaceIronAtAppraisalDesk(s);
                    RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.StartHavenAppraisal), pair.Item2);
                    var query = s.QueryCommand(host, AppraisalCommand(s, CommandKind.StartHavenAppraisal));
                    Require(query.Supported && !query.Admissible && query.Code == pair.Item2, "Query admitted missing authority or service terms.");
                }
                var legacy = PortableWorld(AppraisalPolicy(legacy: true));
                Require(!legacy.QueryCommand(host, AppraisalCommand(legacy, CommandKind.StartHavenAppraisal)).Supported,
                    "The prior profile gained appraisal authority.");
                var policy = AppraisalPolicy();
                Throws<InvalidOperationException>(() => new Simulation(policy, policy.Initial(), ExecutionProfile.Release));
            });
            cases.Add("mgt10_haven_appraisal_appointment_expiry_preserves_partial_labor", () =>
            {
                const int expiry = 1815;
                var s = PortableWorld(AppraisalPolicy(new TestOnlyHavenAppraisalProfile(availableUntil: expiry)));
                ExtractAppraisalIron(s);
                PlaceIronAtAppraisalDesk(s);
                var start = s.Capture().RuleClock;
                MiningCommit(s, AppraisalCommand(s, CommandKind.StartHavenAppraisal));
                WorldAdvance(s, 10);
                var job = s.Capture().HavenAppraisals.Single();
                Require(job.Status == HavenAppraisalStatus.Paused && job.UpdatedAt == T(expiry)
                    && job.Work.Labor == T(expiry * start.Denominator - start.Numerator, start.Denominator)
                    && !job.ResultCopper.HasValue,
                    "Appointment expiry credited time outside the supplied slot or created a result.");
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.ResumeHavenAppraisal, job.Id), "AppraisalAppointmentClosed");
                MiningCommit(s, AppraisalCommand(s, CommandKind.CancelHavenAppraisal, job.Id));
            });
            cases.Add("mgt10_haven_appraisal_endpoint_incapacity_requires_explicit_finish", () =>
            {
                var timing = PortableWorld(AppraisalPolicy());
                ExtractAppraisalIron(timing);
                PlaceIronAtAppraisalDesk(timing);
                var endpoint = timing.Capture().RuleClock.AddSeconds(HavenAppraisalRecord.RequiredSeconds);
                var cure = new ConditionFixtureEvent(AppraisalWorker, ConditionOperation.Cure("event.cure",
                    new ConditionStamp(endpoint), "Stunned"));
                var conditions = new ConditionCombatFixture(CCApply("stun", "Stunned", AppraisalWorker),
                    CCGrant("ward", AppraisalWorker, new ConditionStamp(endpoint), "Stunned"), cure);
                var s = PortableWorld(AppraisalPolicy(conditions: conditions));
                CCDispatch(s, "stun", AppraisalWorker);
                CCDispatch(s, "ward", AppraisalWorker);
                ExtractAppraisalIron(s);
                PlaceIronAtAppraisalDesk(s);
                MiningCommit(s, AppraisalCommand(s, CommandKind.StartHavenAppraisal));
                WorldAdvance(s, HavenAppraisalRecord.RequiredSeconds);
                var job = s.Capture().HavenAppraisals.Single();
                Require(job.Status == HavenAppraisalStatus.PendingCompletion && job.Work.Complete && !job.ResultCopper.HasValue
                    && job.UpdatedAt == endpoint && s.Capture().Work.AvailableAmount(AppraisalIron) == default,
                    "The condition boundary released the claim or resolved the pending report.");
                var path = Path.Combine(directory, "mgt10-haven-appraisal-pending.ddsave");
                new FileSaveStore().Save(path, s.Capture());
                s = new Simulation(AppraisalPolicy(conditions: conditions), new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                RejectUnchanged(s, host, AppraisalCommand(s, CommandKind.ResumeHavenAppraisal, job.Id), "AppraisalWorkerIncapable");
                CCDispatch(s, "cure", AppraisalWorker);
                Require(s.Capture().HavenAppraisals.Single().Status == HavenAppraisalStatus.PendingCompletion,
                    "Restoring eligibility finished the report without an explicit command.");
                var before = s.Capture();
                var finish = AppraisalCommand(s, CommandKind.ResumeHavenAppraisal, job.Id);
                MiningCommit(s, finish);
                var after = s.Capture();
                var report = after.HavenAppraisals.Single();
                Require(after.RuleClock == before.RuleClock && after.RandomState == before.RandomState
                    && report.ResultCopper == new RuleQuantity(15, 2), "Explicit finish charged extra work or changed the exact value.");
                var encoded = Bytes(s);
                Require(s.Execute(host, finish).Outcome == Outcome.Duplicate && encoded.SequenceEqual(Bytes(s)), "Duplicate finish changed the report.");
                var basis = report.Basis;
                var forged = new HavenAppraisalBasis(basis.DeskId, basis.ProviderId, basis.UnitId, basis.DepositVersionId,
                    basis.OwnerId, basis.CustodianId, basis.EvidenceId, basis.ClearanceId, basis.ServiceTermsId, basis.AssessmentContextId, basis.Quantity,
                    20, basis.Provenance, basis.Demand, basis.Condition, basis.Urgency);
                after.HavenAppraisals[0] = new HavenAppraisalRecord(report.Id, report.WorkerId, forged, report.StartRevision,
                    report.UpdatedRevision, report.StartedAt, report.UpdatedAt, report.Work.Labor, report.Status, report.Reason, forged.ExactCopper());
                var codec = new SnapshotCodec();
                Throws<ArgumentException>(() => new Simulation(AppraisalPolicy(conditions: conditions), codec.Decode(codec.Encode(after)),
                    ExecutionProfile.Laboratory));
            });
            cases.Add("mgt10_haven_appraisal_exact_valuation_requires_complete_facts", () =>
            {
                Require(OrdinaryMaterialValuation.ExactCopper(10, MaterialProvenance.Documented, MaterialDemand.Glut,
                    MaterialCondition.Sound, MaterialUrgency.Normal) == new RuleQuantity(15, 2), "The copper result was rounded.");
                Require(OrdinaryMaterialValuation.ExactCopper(10, MaterialProvenance.GateSealed, MaterialDemand.Strategic,
                    MaterialCondition.Exceptional, MaterialUrgency.PatientAuction) == new RuleQuantity(825, 32), "Multipliers were not applied exactly.");
                Throws<ArgumentException>(() => OrdinaryMaterialValuation.ExactCopper(null, MaterialProvenance.Documented,
                    MaterialDemand.Normal, MaterialCondition.Sound, MaterialUrgency.Normal));
                Throws<ArgumentException>(() => OrdinaryMaterialValuation.ExactCopper(10, default,
                    MaterialDemand.Normal, MaterialCondition.Sound, MaterialUrgency.Normal));
            });
        }

        private static string AppraisalAuditRow(string label, Snapshot state)
        {
            var job = state.HavenAppraisals.Single();
            var basis = job.Basis;
            return string.Join("\t", label, state.RuleClock, state.Revision, job.Status, job.Work.Labor, basis.UnitId,
                basis.DepositVersionId, basis.OwnerId, basis.CustodianId, basis.Quantity, basis.BaseCopper, basis.Provenance,
                basis.Demand, basis.Condition, basis.Urgency, basis.AssessmentContextId, basis.ClearanceId, basis.EvidenceId,
                basis.ServiceTermsId, job.ResultCopper?.ToString() ?? "");
        }
    }
}
#endif
