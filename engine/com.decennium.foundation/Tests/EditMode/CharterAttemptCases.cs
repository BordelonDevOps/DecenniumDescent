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
        private static TestOnlySharedWorldPolicy AttemptPolicy(TestOnlyCharterAttemptProfile profile = null,
            TestOnlyNextCharterAgreementProfile agreement = null, ConditionCombatFixture conditions = null)
            => PlanPolicy(new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true), conditions)
                .EnableNextCharterAgreement(agreement ?? new TestOnlyNextCharterAgreementProfile())
                .EnableCharterAttempt(profile ?? new TestOnlyCharterAttemptProfile());

        private static Simulation AttemptReady(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = AgreementReady(policy ?? AttemptPolicy());
            SaleCommit(sim, AgreementCommand(sim));
            Require(sim.Capture().RuleClock == T(11557) && sim.Capture().CharterAttempt == null,
                "The actual prepared agreement baseline changed or inferred execution.");
            return sim;
        }

        private static CharterAttemptRecord Attempt(Simulation sim) => sim.Capture().CharterAttempt;

        private static Command AttemptCommand(Simulation sim, CommandKind kind = CommandKind.StartCharterAttempt,
            string target = null, string actor = PlanHero)
            => MiningCommand(sim, kind, target ?? (kind == CommandKind.StartCharterAttempt ? AcceptedCharter : Attempt(sim).Id), actor: actor);

        private static void StartAttempt(Simulation sim) => SaleCommit(sim, AttemptCommand(sim));

        private static void ObserveAttempt(Simulation sim) => SaleCommit(sim, AttemptCommand(sim, CommandKind.ObserveCharterApproach));

        private static CharterAttemptAssessment InspectAttempt(Simulation sim, Authority authority)
        {
            byte[] before = Bytes(sim);
            var query = sim.QueryCommand(authority, AttemptCommand(sim, CommandKind.InspectCharterAttempt));
            Require(query.Admissible && query.CharterAttemptAssessment != null && before.SequenceEqual(Bytes(sim)),
                "Attempt inspection changed state or failed: " + query.Code);
            return query.CharterAttemptAssessment;
        }

        private static WorldTraversalRecord HeroEdge(Simulation sim) => sim.Capture().WorldTraversals.Single(x => x.ActorId == PlanHero);

        private static void AddCharterAttemptCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            var actor = new Authority(host.Principal, new[] { PlanHero });
            var codec = new SnapshotCodec();

            cases.Add("mgt10_charter_execution_connected_actual_steps_and_fractional_replay", () =>
            {
                var sim = AttemptReady();
                PlanWalk(sim, 1, 0);
                PlanWalk(sim, -1, 0);
                var before = sim.Capture();
                Require(before.SchemaVersion == Snapshot.CharterAttemptSchema && before.CharterAttempt == null,
                    "Ordinary pre-admission passage earned objective credit.");
                var start = AttemptCommand(sim);
                Require(sim.QueryCommand(actor, start).Admissible
                    && sim.DiscoverCommands(actor, PlanHero).Any(x => x.Command.Kind == start.Kind && x.Query.Admissible),
                    "The authorized attempt could not be discovered.");
                Require(sim.Execute(actor, start).Outcome == Outcome.Committed, "Explicit admission failed.");
                var admitted = Attempt(sim);
                Require(admitted.OutboundStarted == null && admitted.Admitted.At == before.RuleClock
                    && admitted.Admission.Strain == 0 && !admitted.Admission.RestDebtOwed && !admitted.Admission.RoutePressureApplicable
                    && admitted.Admission.Physical.Pressure == null && !admitted.Admission.Physical.WiderObligationsResolved
                    && admitted.Admission.Physical.Supplies[0].ReadyAvailable == new RuleQuantity(20),
                    "Admission invented movement, a Pressure value or an unsupported resource fact.");
                var stripped = sim.Capture();
                stripped.CharterAttempt = null;
                stripped.Revision = before.Revision;
                stripped.Receipts = before.Receipts;
                Require(codec.Encode(stripped).SequenceEqual(codec.Encode(before)), "Admission changed state beyond its record and receipt.");
                SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-admitted");
                RejectUnchanged(sim, actor, AttemptCommand(sim, CommandKind.ObserveCharterApproach), "CharterObservationRequiresStationaryArrival");
                WorldStep(sim, 1, 0);
                Require(Attempt(sim).OutboundStarted.Revision == HeroEdge(sim).StartedRevision
                    && Attempt(sim).Departure.Physical.ScoutAtStage && Attempt(sim).OutboundArrived == null,
                    "Departure did not bind the actual ordinary step and its pre-step readiness.");
                WorldAdvance(sim, 1, 2);
                var inspection = InspectAttempt(sim, actor);
                Require(inspection.X == new RuleQuantity(7, 3) && inspection.Y == new RuleQuantity(3)
                    && inspection.Traversal.DistanceFeet == new RuleQuantity(5, 3) && Attempt(sim).OutboundMovingTime == T(1, 2),
                    "The partial position or actual movement time was rounded or fabricated.");
                RejectUnchanged(sim, actor, AttemptCommand(sim, CommandKind.ObserveCharterApproach), "CharterObservationRequiresStationaryArrival");
                var replay = SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-partial-outbound");
                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 1);
                    var arrival = Attempt(run).OutboundArrived;
                    var beforeObservation = run.Capture();
                    var observe = AttemptCommand(run, CommandKind.ObserveCharterApproach);
                    Require(arrival != null && beforeObservation.WorldTraversals.Length == 0
                        && run.Execute(actor, observe).Outcome == Outcome.Committed,
                        "The actual stationary approach did not permit its limited observation.");
                    var checkedAttempt = Attempt(run);
                    Require(checkedAttempt.Observed.At == arrival.At && checkedAttempt.Observation.X == 3
                        && checkedAttempt.Observation.Y == 3 && checkedAttempt.Observation.StageSurfaceWalkable
                        && checkedAttempt.Observation.ApproachSurfaceWalkable && !checkedAttempt.Observation.HiddenConditionsEstablished
                        && !checkedAttempt.Observation.FuturePassageEstablished && run.Capture().RandomState == beforeObservation.RandomState,
                        "Observation changed the clock, RNG or unsupported knowledge.");
                    RejectUnchanged(run, actor, AttemptCommand(run, CommandKind.ObserveCharterApproach), "CharterApproachAlreadyObserved");
                    WorldStep(run, -1, 0);
                    WorldAdvance(run, 1, 2);
                    Require(HeroEdge(run).DistanceFeet == new RuleQuantity(5, 3) && Attempt(run).ReturnMovingTime == T(1, 2),
                        "The actual return did not preserve fractional movement.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Partial outbound replay diverged.");
                var returnReplay = SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-partial-return");
                foreach (var run in new[] { sim, returnReplay }) {
                    var agreementBefore = run.Capture().NextCharterAgreement;
                    WorldAdvance(run, 1);
                    var result = Attempt(run);
                    var after = run.Capture();
                    Require(result.Outcome == CharterAttemptOutcome.ReturnedComplete && result.Returned.At == before.RuleClock.AddSeconds(3)
                        && result.OutboundMovingTime == T(3, 2) && result.ReturnMovingTime == T(3, 2)
                        && after.Actors.Single(x => x.Id == PlanHero).X == 2 && after.RuleClock == result.Returned.At
                        && after.RandomState == before.RandomState && after.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(before.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                        && ReferenceEquals(after.NextCharterAgreement, agreementBefore)
                        && after.ExpeditionEpisodeClose.CloseRevision == result.CloseRevision,
                        "The factual out-and-back did not preserve stock, exact time, or prior records.");
                    RejectUnchanged(run, actor, AttemptCommand(run), "CharterAttemptAlreadyAdmitted");
                    RejectUnchanged(run, actor, new Command(start.Id, start.Actor, start.ExpectedRevision, start.Kind, "wrong-charter"),
                        "CommandIdConflict");
                    Require(run.Execute(actor, start).Outcome == Outcome.Duplicate, "Identical admission replay lost idempotence.");
                    RejectUnchanged(run, actor, AttemptCommand(run, CommandKind.InspectCharterAttempt), "CharterAttemptReadOnly");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(returnReplay)), "Partial return replay diverged.");
                var continued = SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-complete");
                foreach (var run in new[] { sim, continued }) {
                    var history = Attempt(run);
                    PlanWalk(run, -1, 0);
                    Require(ReferenceEquals(history, Attempt(run)), "Later ordinary movement rewrote the completed attempt.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(continued)), "Ordinary continuation diverged.");
                SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-continued");
                File.WriteAllLines(Path.Combine(directory, "mgt10-charter-attempt.tsv"), AttemptAudit(sim.Capture()));
                Throws<ArgumentException>(() => new Simulation(AgreementPolicy(), sim.Capture(), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(AttemptPolicy(), sim.Capture(), ExecutionProfile.Release));
            });

            cases.Add("mgt10_charter_execution_scoped_authority_and_fresh_ready_support", () =>
            {
                var fresh = PortableWorld(AttemptPolicy());
                RejectUnchanged(fresh, actor, AttemptCommand(fresh), "CharterAcceptedAgreementRequired");
                var sim = AttemptReady();
                RejectUnchanged(sim, new Authority("no-hero", new[] { SaleSeller }), AttemptCommand(sim), "NotAuthorized");
                RejectUnchanged(sim, host, AttemptCommand(sim, actor: SaleSeller), "CharterAttemptActorUnauthorized");
                RejectUnchanged(sim, actor, AttemptCommand(sim, target: "wrong-charter"), "CharterAttemptAgreementUnknown");
                foreach (var entry in new[] {
                    (new TestOnlyCharterAttemptProfile(departureAuthorized: false), "CharterDepartureMandateMissing"),
                    (new TestOnlyCharterAttemptProfile(controlledLocalSite: false), "CharterLocalSiteScopeMissing"),
                    (new TestOnlyCharterAttemptProfile(currentFatigueHistoryEstablished: false), "CharterCurrentFatigueBasisUnavailable"),
                    (new TestOnlyCharterAttemptProfile(egressIssued: false), "CharterEgressAuthorityMissing"),
                    (new TestOnlyCharterAttemptProfile(conflictingLocalRestriction: true), "CharterLocalSiteScopeContradicted"),
                    (new TestOnlyCharterAttemptProfile(directViewEstablished: false), "CharterDirectObservationUnavailable")
                }) {
                    var run = AttemptReady(AttemptPolicy(entry.Item1));
                    Require(run.QueryCommand(actor, AttemptCommand(run)).Code == entry.Item2, "A prerequisite was ignored by query.");
                    RejectUnchanged(run, actor, AttemptCommand(run), entry.Item2);
                }
                var expired = AttemptReady(AttemptPolicy(agreement: new TestOnlyNextCharterAgreementProfile(validUntil: 11558)));
                WorldAdvance(expired, 1);
                RejectUnchanged(expired, actor, AttemptCommand(expired), "CharterAgreementOutOfForce");
                var withdrawn = AttemptReady();
                SaleCommit(withdrawn, AgreementCommand(withdrawn, CommandKind.WithdrawNextCharter, AcceptedCharter));
                RejectUnchanged(withdrawn, actor, AttemptCommand(withdrawn), "CharterAgreementOutOfForce");

                // A detached negative projection exercises the actual burden predicate. Ordinary handling cannot create it.
                var overweight = sim.Capture();
                overweight.PortableEquipment = overweight.PortableEquipment.Append(new PortableEquipmentRecord("TEST_ONLY.attempt-capacity-control",
                    "adventuring-gear.pouch", PlanHero, PlanHero, "", PortablePlacement.Carried, PortableLinkKind.None, "",
                    PortableMassBasis.Fixed, new RuleQuantity(1000), new RuleQuantity(1000))).ToArray();
                Require(AttemptPolicy().QueryCommand(overweight, actor, AttemptCommand(sim)).Code == "CharterHardCarryingLimit",
                    "The actual hard carrying limit was omitted.");
                StartAttempt(sim);
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Drop));
                var step = new Command("charter-fresh-outward", PlanHero, sim.Capture().Revision, CommandKind.BeginWorldStep, "walk", 1, 0);
                Require(sim.QueryCommand(actor, step).Code == "CharterReadySupportInsufficient", "Departure reused stale admission supplies.");
                RejectUnchanged(sim, actor, step, "CharterReadySupportInsufficient");
                Require(Attempt(sim).OutboundStarted == null && sim.Capture().WorldTraversals.Length == 0,
                    "A rejected outbound step became actual departure.");
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Pickup));
                WorldAdvance(sim, 6);
                WorldStep(sim, 1, 0);
                Require(Attempt(sim).OutboundStarted != null, "Fresh lawful preparation could not use the same admitted attempt.");
            });

            cases.Add("mgt10_charter_execution_actual_condition_interruption_and_direct_observation", () =>
            {
                var conditions = new ConditionCombatFixture(
                    CCApply("charter-stun", "Stunned", PlanHero, at: new ConditionStamp(T(23115, 2))),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Cure("event.charter-stun-cure", new ConditionStamp(T(23117, 2)), "Stunned")),
                    CCApply("charter-blind", "Blinded", PlanHero, at: new ConditionStamp(T(23119, 2))),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Cure("event.charter-blind-cure", new ConditionStamp(T(23119, 2)), "Blinded")));
                var sim = AttemptReady(AttemptPolicy(conditions: conditions));
                StartAttempt(sim);
                WorldStep(sim, 1, 0);
                WorldAdvance(sim, 1, 2);
                SaleCommit(sim, CCCommand(sim, "charter-stun"));
                Require(Attempt(sim).Interrupted && HeroEdge(sim).Status == WorldTraversalStatus.Suspended
                    && HeroEdge(sim).DistanceFeet == new RuleQuantity(5, 3), "Incapacity discarded or advanced spent movement.");
                RejectUnchanged(sim, actor, IC(sim, CommandKind.ResumeWorldStep), "ConditionPreventsMovement");
                var replay = SaveBill(sim, AttemptPolicy(conditions: conditions), directory, "mgt10-charter-attempt-interrupted");
                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 1);
                    SaleCommit(run, CCCommand(run, "charter-stun-cure"));
                    Require(Attempt(run).Interrupted && HeroEdge(run).Status == WorldTraversalStatus.Suspended,
                        "Cure automatically resumed the attempt.");
                    WorldCommit(run, IC(run, CommandKind.ResumeWorldStep));
                    WorldAdvance(run, 1);
                    Require(Attempt(run).OutboundArrived.At == T(23119, 2) && Attempt(run).OutboundMovingTime == T(3, 2),
                        "Actual elapsed interruption was counted as active movement.");
                    SaleCommit(run, CCCommand(run, "charter-blind"));
                    RejectUnchanged(run, actor, AttemptCommand(run, CommandKind.ObserveCharterApproach), "CharterDirectObservationUnavailable");
                    SaleCommit(run, CCCommand(run, "charter-blind-cure"));
                    Require(Attempt(run).Interrupted && Attempt(run).Observation == null, "Cure fabricated an observation.");
                    ObserveAttempt(run);
                    WorldStep(run, -1, 0);
                    WorldAdvance(run, 3, 2);
                    Require(Attempt(run).Outcome == CharterAttemptOutcome.ReturnedComplete
                        && Attempt(run).Returned.At == T(11561) && Attempt(run).ReturnMovingTime == T(3, 2),
                        "Explicit continuation did not complete the same objective.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Actual interruption and observation replay diverged.");
                File.WriteAllLines(Path.Combine(directory, "mgt10-charter-interruption.tsv"), AttemptAudit(sim.Capture()));
            });

            cases.Add("mgt10_charter_execution_abort_and_withdrawal_preserve_egress", () =>
            {
                var atStage = AttemptReady();
                StartAttempt(atStage);
                SaleCommit(atStage, AttemptCommand(atStage, CommandKind.AbortCharterAttempt));
                Require(Attempt(atStage).Outcome == CharterAttemptOutcome.EndedAtStaging && Attempt(atStage).OutboundStarted == null,
                    "Abort before departure fabricated an excursion.");
                RejectUnchanged(atStage, actor, AttemptCommand(atStage), "CharterAttemptAlreadyAdmitted");

                var partial = AttemptReady();
                StartAttempt(partial);
                WorldStep(partial, 1, 0);
                WorldAdvance(partial, 1, 2);
                var abort = AttemptCommand(partial, CommandKind.AbortCharterAttempt);
                SaleCommit(partial, abort);
                Require(Attempt(partial).Outcome == CharterAttemptOutcome.AwaitingLawfulReturn
                    && HeroEdge(partial).Status == WorldTraversalStatus.Suspended && HeroEdge(partial).DistanceFeet == new RuleQuantity(5, 3),
                    "Partial abort snapped or erased the traversal.");
                WorldAdvance(partial, 2);
                Require(HeroEdge(partial).DistanceFeet == new RuleQuantity(5, 3), "Abort automatically began egress.");
                var replay = SaveBill(partial, AttemptPolicy(), directory, "mgt10-charter-attempt-return-only");
                foreach (var run in new[] { partial, replay }) {
                    WorldCommit(run, IC(run, CommandKind.ResumeWorldStep));
                    WorldAdvance(run, 1);
                    RejectUnchanged(run, actor, AttemptCommand(run, CommandKind.ObserveCharterApproach), "CharterObjectiveEnded");
                    WorldStep(run, -1, 0);
                    WorldAdvance(run, 3, 2);
                    Require(Attempt(run).Outcome == CharterAttemptOutcome.ReturnedIncomplete
                        && Attempt(run).OutboundMovingTime == T(3, 2) && Attempt(run).ReturnMovingTime == T(3, 2),
                        "Independent egress fabricated success or lost prior spent movement.");
                }
                Require(Bytes(partial).SequenceEqual(Bytes(replay)), "Return-only replay diverged.");
                SaveBill(partial, AttemptPolicy(), directory, "mgt10-charter-attempt-returned-incomplete");

                var egressConditions = new ConditionCombatFixture(
                    CCApply("charter-egress-stun", "Stunned", PlanHero, at: new ConditionStamp(T(23119, 2))),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Cure("event.charter-egress-cure", new ConditionStamp(T(23119, 2)), "Stunned")));
                var withdrawn = AttemptReady(AttemptPolicy(conditions: egressConditions));
                StartAttempt(withdrawn);
                WorldStep(withdrawn, 1, 0);
                WorldAdvance(withdrawn, 3, 2);
                PortableCommit(withdrawn, Portable(withdrawn, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Drop));
                SaleCommit(withdrawn, AgreementCommand(withdrawn, CommandKind.WithdrawNextCharter, AcceptedCharter));
                var stop = Attempt(withdrawn).Stop;
                Require(stop.Kind == CharterAttemptEventKind.Withdrawn
                    && stop.Revision == withdrawn.Capture().NextCharterAgreement.Withdrawal.Revision, "Actual withdrawal did not stop the linked objective.");
                SaleCommit(withdrawn, CCCommand(withdrawn, "charter-egress-stun"));
                var blocked = InspectAttempt(withdrawn, actor);
                Require(blocked.Attempt.Outcome == CharterAttemptOutcome.AwaitingLawfulReturn
                    && blocked.EgressBlocker == "CharterEgressActorIncapable" && blocked.X == new RuleQuantity(3)
                    && blocked.Traversal == null, "Actual incapacity during egress lost the unresolved physical position.");
                RejectUnchanged(withdrawn, actor,
                    new Command("charter-blocked-egress", PlanHero, withdrawn.Capture().Revision, CommandKind.BeginWorldStep, "walk", -1, 0),
                    "ConditionPreventsMovement");
                SaveBill(withdrawn, AttemptPolicy(conditions: egressConditions), directory, "mgt10-charter-attempt-egress-incapable");
                SaleCommit(withdrawn, CCCommand(withdrawn, "charter-egress-cure"));
                RejectUnchanged(withdrawn, actor,
                    new Command("charter-unscoped-running-egress", PlanHero, withdrawn.Capture().Revision, CommandKind.BeginWorldStep, "run", -1, 0),
                    "CharterReturnRequiresOrdinaryWalk");
                WorldStep(withdrawn, -1, 0);
                WorldAdvance(withdrawn, 3, 2);
                Require(Attempt(withdrawn).Outcome == CharterAttemptOutcome.ReturnedIncomplete
                    && withdrawn.Capture().PortableEquipment.Single(x => x.Id == PortableKitFixture.Rations).Placement == PortablePlacement.Ground,
                    "Egress required the original reserve or restored lost supplies.");
            });

            cases.Add("mgt10_charter_execution_expiry_during_each_leg_and_exact_arrival_ties", () =>
            {
                foreach (var item in new[] {
                    (11558, false, false, new RuleQuantity(10, 3)),
                    (11559, false, true, default(RuleQuantity)),
                    (11559, true, false, new RuleQuantity(5, 3)),
                    (11560, true, true, default(RuleQuantity))
                }) {
                    var terms = new TestOnlyNextCharterAgreementProfile(validUntil: item.Item1);
                    var sim = AttemptReady(AttemptPolicy(agreement: terms));
                    if (!item.Item2 && item.Item3) WorldAdvance(sim, 1, 2);
                    StartAttempt(sim);
                    WorldStep(sim, 1, 0);
                    if (item.Item2) {
                        WorldAdvance(sim, 3, 2);
                        ObserveAttempt(sim);
                        WorldStep(sim, -1, 0);
                    }
                    WorldAdvance(sim, 3);
                    var expired = Attempt(sim);
                    Require(expired.Stop.Kind == CharterAttemptEventKind.Expired && expired.Stop.At == T(item.Item1),
                        "Expiry failed to preserve the actual half-open boundary.");
                    RejectUnchanged(sim, actor, AgreementCommand(sim, CommandKind.WithdrawNextCharter, AcceptedCharter), "NextCharterAgreementExpired");
                    if (item.Item3) {
                        var arrival = item.Item2 ? expired.Returned : expired.OutboundArrived;
                        Require(arrival.At == expired.Stop.At && sim.Capture().WorldTraversals.Length == 0
                            && expired.Outcome != CharterAttemptOutcome.ReturnedComplete, "Exact expiry incorrectly discarded arrival or awarded success.");
                    } else {
                        Require(HeroEdge(sim).Status == WorldTraversalStatus.Suspended && HeroEdge(sim).DistanceFeet == item.Item4,
                            "An expiry inside a leg did not preserve its exact partial distance.");
                        WorldCommit(sim, IC(sim, CommandKind.ResumeWorldStep));
                        WorldAdvance(sim, 3, 2);
                    }
                    if (!item.Item2) {
                        RejectUnchanged(sim, actor, AttemptCommand(sim, CommandKind.ObserveCharterApproach), "CharterObjectiveEnded");
                        WorldStep(sim, -1, 0);
                        WorldAdvance(sim, 3, 2);
                    }
                    Require(Attempt(sim).Outcome == CharterAttemptOutcome.ReturnedIncomplete && Attempt(sim).ReturnMovingTime == T(3, 2),
                        "Lawful physical egress acquired successful objective credit.");
                }
                var shortTerms = new TestOnlyNextCharterAgreementProfile(validUntil: 11558);
                var limited = new TestOnlyCharterAttemptProfile(egressUntil: 11562);
                var stranded = AttemptReady(AttemptPolicy(limited, shortTerms));
                StartAttempt(stranded);
                WorldStep(stranded, 1, 0);
                WorldAdvance(stranded, 5);
                var status = InspectAttempt(stranded, actor);
                Require(status.Attempt.Outcome == CharterAttemptOutcome.AwaitingLawfulReturn
                    && status.EgressBlocker == "CharterEgressPermissionUnavailable" && status.Traversal.DistanceFeet == new RuleQuantity(10, 3),
                    "Finite egress expiration changed the actual stranded position.");
                RejectUnchanged(stranded, actor, IC(stranded, CommandKind.ResumeWorldStep), "CharterEgressPermissionUnavailable");
                SaveBill(stranded, AttemptPolicy(limited, shortTerms), directory, "mgt10-charter-attempt-egress-expired");
            });

            cases.Add("mgt10_charter_execution_forged_authority_movement_observation_and_outcome", () =>
            {
                var sim = AttemptReady();
                StartAttempt(sim);
                WorldStep(sim, 1, 0);
                WorldAdvance(sim, 3, 2);
                ObserveAttempt(sim);
                SaveBill(sim, AttemptPolicy(), directory, "mgt10-charter-attempt-observed");
                WorldStep(sim, -1, 0);
                WorldAdvance(sim, 3, 2);
                WorldAdvance(sim, 1);
                var actual = Attempt(sim);
                var authority = actual.Authority;
                CharterAttemptRecord Copy(CharterAttemptAuthority terms = null, CharterAttemptReadiness readiness = null,
                    IEnumerable<CharterAttemptEvent> events = null, CharterApproachObservation observation = null)
                    => new CharterAttemptRecord(actual.Id, actual.CharterId, actual.AgreementRevision, actual.PlanId, actual.CloseRevision,
                        terms ?? authority, readiness ?? actual.Admission, events ?? actual.Events, actual.Departure,
                        observation ?? actual.Observation, actual.OutboundMovingTime, actual.ReturnMovingTime);
                var forged = sim.Capture();
                forged.CharterAttempt = Copy(readiness: new CharterAttemptReadiness(actual.Admission.Physical, 1, false));
                RejectAttemptReplay(codec, forged);
                var substitute = new CharterAttemptAuthority(authority.VersionId, authority.DepartureMandateId, authority.SiteId,
                    authority.SiteScopeEvidenceId, authority.ControllerId, authority.ControllerAuthorityId, authority.HeroId,
                    authority.StageX, authority.StageY, authority.ApproachX, authority.ApproachY, authority.VisibilityEvidenceId,
                    authority.FatigueEvidenceId, authority.RestScheduleId, authority.Epoch, authority.OpeningStrain, authority.OpeningRestDebt,
                    authority.FatigueUntil, authority.EgressPermissionId, "forged-egress-evidence", authority.EgressFrom, authority.EgressUntil);
                forged.CharterAttempt = Copy(terms: substitute);
                RejectAttemptReplay(codec, forged);
                forged.CharterAttempt = Copy(observation: new CharterApproachObservation(3, 3, false, true, actual.Observation.PermissionVersionId));
                RejectAttemptReplay(codec, forged);
                forged.CharterAttempt = Copy(events: actual.Events.Select(x => x == actual.OutboundArrived
                    ? new CharterAttemptEvent(x.Kind, "forged-arrival", x.Revision, x.At, x.Reason) : x));
                Throws<ArgumentException>(() => codec.Encode(forged));
                forged.CharterAttempt = Copy(events: actual.Events.Select(x => x == actual.Returned
                    ? new CharterAttemptEvent(x.Kind, x.CommandId, x.Revision, x.At.AddSeconds(1), x.Reason) : x));
                RejectAttemptReplay(codec, forged);
            });
        }

        private static void RejectAttemptReplay(SnapshotCodec codec, Snapshot forged)
        {
            var decoded = codec.Decode(codec.Encode(forged));
            bool rejected = false;
            try { new Simulation(AttemptPolicy(), decoded, ExecutionProfile.Laboratory); }
            catch (ArgumentException ex) { rejected = ex.Message.Contains("InvalidSharedWorldReplay"); }
            Require(rejected, "A coherent forged charter-attempt fact bypassed canonical replay.");
        }

        private static string[] AttemptAudit(Snapshot state)
        {
            var attempt = state.CharterAttempt;
            string events = string.Join("|", attempt.Events.Select(x => string.Join(",", x.Kind, x.At, x.Revision, x.CommandId, x.Reason)));
            var journey = new RuleQuantity(attempt.Returned.At.Numerator, attempt.Returned.At.Denominator)
                - new RuleQuantity(attempt.OutboundStarted.At.Numerator, attempt.OutboundStarted.At.Denominator);
            var moving = new RuleQuantity(attempt.OutboundMovingTime.Numerator, attempt.OutboundMovingTime.Denominator)
                + new RuleQuantity(attempt.ReturnMovingTime.Numerator, attempt.ReturnMovingTime.Denominator);
            return new[] { string.Join("\t", attempt.Id, "assent=" + state.NextCharterAgreement.AcceptedAt,
                "assent-rev=" + attempt.AgreementRevision, "close-rev=" + attempt.CloseRevision, "outcome=" + attempt.Outcome,
                "outbound-moving=" + attempt.OutboundMovingTime, "return-moving=" + attempt.ReturnMovingTime,
                "non-moving=" + (journey - moving), "strain=" + attempt.Admission.Strain, "debt=" + attempt.Admission.RestDebtOwed,
                "route-pressure-applies=" + attempt.Admission.RoutePressureApplicable, "site=" + attempt.Authority.SiteScopeEvidenceId,
                "egress=" + attempt.Authority.EgressPermissionId, "scope=" + attempt.Observation.MethodId, events) };
        }
    }
}
#endif
