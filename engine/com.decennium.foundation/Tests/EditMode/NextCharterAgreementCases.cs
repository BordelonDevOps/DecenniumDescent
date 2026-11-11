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
        private const string AssentOffer = TestOnlyNextCharterAgreementProfile.OfferId;
        private const string AcceptedCharter = TestOnlyNextCharterAgreementProfile.CharterId;

        private static TestOnlySharedWorldPolicy AgreementPolicy(TestOnlyNextCharterAgreementProfile profile = null,
            TestOnlyNextCharterPlanProfile planning = null, CraftingMishapFact incident = null)
            => PlanPolicy(planning ?? new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true), incident: incident)
                .EnableNextCharterAgreement(profile ?? new TestOnlyNextCharterAgreementProfile());

        private static Command AgreementCommand(Simulation sim, CommandKind kind = CommandKind.AcceptNextCharter,
            string target = AssentOffer, string actor = PlanHero) => MiningCommand(sim, kind, target, actor: actor);

        private static Simulation AgreementReady(TestOnlySharedWorldPolicy policy = null, bool clearApproach = true, bool readySupplies = true)
        {
            var sim = PlanReady(policy ?? AgreementPolicy());
            SaleCommit(sim, PlanCommand(sim));
            WorldAdvance(sim, 3600);
            Require(PlanJob(sim).Report != null && sim.Capture().NextCharterAgreement == null,
                "Completing planning supplied an agreement or failed to produce its actual report.");
            if (clearApproach) ClearAgreementApproach(sim);
            if (readySupplies) {
                foreach (string item in new[] { PortableKitFixture.Rations, PortableKitFixture.Skin }) {
                    PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, item, handling: HandlingKind.Retrieve));
                    WorldAdvance(sim, 6);
                }
            }
            return sim;
        }

        private static void ClearAgreementApproach(Simulation sim)
        {
            PlanWalk(sim, -1, 0);
            PlanWalk(sim, 1, 0, SaleSeller);
            PlanWalk(sim, 1, 0);
        }

        private static NextCharterAgreementAssessment InspectAgreement(Simulation sim, Authority authority)
        {
            byte[] before = Bytes(sim);
            var result = sim.QueryCommand(authority, AgreementCommand(sim, CommandKind.InspectNextCharterAgreement, AcceptedCharter));
            Require(result.Admissible && result.NextCharterAgreementAssessment != null && before.SequenceEqual(Bytes(sim)),
                "Current agreement inspection failed or changed state: " + result.Code);
            return result.NextCharterAgreementAssessment;
        }

        private static void AddNextCharterAgreementCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            var assent = new Authority(host.Principal, new[] { PlanHero });
            var codec = new SnapshotCodec();

            cases.Add("mgt10_charter_assent_connected_zero_time_explicit_solo_agreement_and_replay", () =>
            {
                var planning = new TestOnlyNextCharterPlanProfile(authorizationUntil: 12000, reserveWaterStartsCarried: true);
                var sim = AgreementReady(AgreementPolicy(planning: planning));
                var prepared = sim.Capture();
                Require(prepared.SchemaVersion == Snapshot.NextCharterAgreementSchema && prepared.ExpeditionEpisodeClose != null
                    && prepared.NextCharterAgreement == null && prepared.RuleClock < T(12000), "Connected preparation inferred assent.");
                var planningReport = PlanJob(sim).Report;
                WorldAdvance(sim, checked(12000 - (int)prepared.RuleClock.Numerator));
                WorldStep(sim, 0, 1, actor: SaleSeller);
                var before = sim.Capture();
                Require(before.RuleClock == T(12000) && !PlanJob(sim).Terms.AuthorizedAt(before.RuleClock)
                    && before.WorldTraversals.Single().ActorId == SaleSeller, "The old appointment or remote traversal control was absent.");
                byte[] beforeBytes = Bytes(sim);
                var command = AgreementCommand(sim);
                var query = sim.QueryCommand(assent, command);
                var preview = query.NextCharterAgreementAssessment;
                Require(query.Admissible && preview.Status == NextCharterAgreementStatus.Offered
                    && preview.CurrentObservation.Revision == before.Revision && !preview.AgreementRecorded
                    && sim.DiscoverCommands(assent, PlanHero).Any(x => x.Command.Kind == command.Kind && x.Query.Admissible)
                    && beforeBytes.SequenceEqual(Bytes(sim)), "Free query or discovery inferred assent or lost eligibility: " + query.Code);
                var replay = SaveBill(sim, AgreementPolicy(planning: planning), directory, "mgt10-charter-before-assent");
                foreach (var branch in new[] { sim, replay }) {
                    Require(branch.Execute(assent, command).Outcome == Outcome.Committed, "The explicit controlled hero could not assent.");
                    var after = branch.Capture();
                    var record = after.NextCharterAgreement;
                    var terms = record.Terms;
                    Require(record.AcceptedAt == before.RuleClock && record.SourceRevision == before.Revision
                        && record.AcceptedRevision == before.Revision + 1 && record.CommandId == command.Id && record.ActorId == PlanHero
                        && record.PlanId == before.NextCharterPlans.Single().Id && record.PlanReportRevision == planningReport.Revision
                        && record.PriorCloseRevision == before.ExpeditionEpisodeClose.CloseRevision
                        && terms.ParticipantId == PlanHero && terms.SoloOffices == NextCharterOffice.All
                        && terms.CharterVersionId != before.ExpeditionEpisodeClose.CharterVersionId
                        && terms.AccessPermission.IssuerAuthorityId == TestOnlyNextCharterAgreementProfile.SiteControlAuthorityId
                        && terms.AccessPermission.BeneficiaryId == PlanHero && terms.AccessPermission.Covers(terms.PlanTerms)
                        && terms.NewCashLimitCopper == 0 && terms.ReservesDesignated && !terms.ReservesExclusivelyCommitted,
                        "The actual assent lost its prospective authority, offices, terms, or causal evidence.");
                    var current = InspectAgreement(branch, assent);
                    Require(current.AgreementRecorded && current.InForce && current.Status == NextCharterAgreementStatus.AcceptedConditional
                        && !current.DeparturePermitted && !record.Observation.DeparturePermitted
                        && record.Observation.Pressure == null && record.Observation.Strain == null && record.Observation.RestDebt == null
                        && !record.Observation.HazardSafetyEstablished && !record.Observation.WiderObligationsResolved
                        && record.Observation.Supplies[0].ReadyAvailable == new RuleQuantity(20)
                        && record.Observation.Supplies.Skip(1).All(x => x.ReadyAvailable == new RuleQuantity(4))
                        && record.Observation.ActualPounds == new RuleQuantity(68) && planningReport.Occupied,
                        "Assent misrepresented a risk, proposed quantities, or the earlier plan.");
                    after.NextCharterAgreement = null;
                    after.Revision = before.Revision;
                    after.Receipts = before.Receipts;
                    Require(codec.Encode(after).SequenceEqual(beforeBytes), "Assent changed facts besides the agreement and command receipt.");
                    Require(branch.Execute(assent, command).Outcome == Outcome.Duplicate, "Identical assent was not a duplicate.");
                    RejectUnchanged(branch, assent, new Command(command.Id, command.Actor, command.ExpectedRevision, command.Kind, "other-offer"),
                        "CommandIdConflict");
                    RejectUnchanged(branch, assent, AgreementCommand(branch), "NextCharterOfferAlreadyAccepted");
                    RejectUnchanged(branch, assent, AgreementCommand(branch, CommandKind.InspectNextCharterAgreement, AcceptedCharter),
                        "NextCharterAgreementReadOnly");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Agreement replay after save/restore diverged.");
                var afterRestore = SaveBill(sim, AgreementPolicy(planning: planning), directory, "mgt10-charter-accepted");
                foreach (var branch in new[] { sim, afterRestore }) {
                    WorldAdvance(branch, 6);
                    PlanWalk(branch, -1, 0);
                    Require(InspectAgreement(branch, assent).CurrentPrerequisiteFailure == "NextCharterAssentStationaryStagingRequired",
                        "Ordinary continuation did not update the current staging evidence.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(afterRestore)), "Ordinary continuation diverged after agreement restore.");
                var completed = sim.Capture();
                File.WriteAllLines(Path.Combine(directory, "mgt10-charter-assent.tsv"), new[] {
                    AgreementAudit("accepted", before, completed.NextCharterAgreement, completed.NextCharterAgreement.Observation),
                    AgreementAudit("continued", completed, completed.NextCharterAgreement, InspectAgreement(sim, assent).CurrentObservation) });
                SaveBill(sim, AgreementPolicy(planning: planning), directory, "mgt10-charter-continued");
                Throws<ArgumentException>(() => new Simulation(PlanPolicy(planning), completed, ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(AgreementPolicy(planning: planning), completed, ExecutionProfile.Release));
            });

            cases.Add("mgt10_charter_assent_independent_authority_and_scoped_access", () =>
            {
                var open = new TestOnlyNextCharterAgreementProfile(validFrom: 0);
                var initial = PortableWorld(AgreementPolicy(open));
                RejectUnchanged(initial, assent, AgreementCommand(initial), "NextCharterAssentPriorCloseRequired");
                RejectUnchanged(initial, new Authority("no-hero", new[] { SaleSeller }), AgreementCommand(initial), "NotAuthorized");
                RejectUnchanged(initial, host, AgreementCommand(initial, actor: SaleSeller), "NextCharterAssentActorUnauthorized");
                RejectUnchanged(initial, assent, AgreementCommand(initial, target: "different-offer"), "NextCharterOfferUnknown");
                var wrongPayload = new Command("bad-assent-payload", PlanHero, initial.Capture().Revision,
                    CommandKind.AcceptNextCharter, AssentOffer, 1);
                RejectUnchanged(initial, assent, wrongPayload, "InvalidNextCharterAssentPayload");
                var closed = PlanReady(AgreementPolicy(open));
                RejectUnchanged(closed, assent, AgreementCommand(closed), "NextCharterAssentCompletedPlanRequired");

                foreach (var entry in new[] {
                    (new TestOnlyNextCharterAgreementProfile(assentAuthorized: false), "NextCharterAssentMandateMissing"),
                    (new TestOnlyNextCharterAgreementProfile(recordsAccessible: false), "NextCharterAssentRecordsUnavailable"),
                    (new TestOnlyNextCharterAgreementProfile(resourceUseAuthorized: false), "NextCharterAssentResourceUseUnauthorized"),
                    (new TestOnlyNextCharterAgreementProfile(resourceOwnerId: SaleSeller), "NextCharterAssentResourceUseUnauthorized"),
                    (new TestOnlyNextCharterAgreementProfile(accessIssued: false), "NextCharterAssentPermissionMissing"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        issuerId: SaleBuyer)), "NextCharterAssentPermissionIssuerUnestablished"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        authorityId: "name-without-site-control")), "NextCharterAssentPermissionIssuerUnestablished"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        beneficiaryId: SaleSeller)), "NextCharterAssentPermissionScopeOrValidity"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        approachX: 1)), "NextCharterAssentPermissionScopeOrValidity"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        directions: NextCharterPassageDirections.Outbound)), "NextCharterAssentPermissionScopeOrValidity"),
                    (new TestOnlyNextCharterAgreementProfile(accessPermission: TestOnlyNextCharterAgreementProfile.IssueAccess(
                        validUntil: 11500)), "NextCharterAssentPermissionScopeOrValidity"),
                    (new TestOnlyNextCharterAgreementProfile(conflictingRestriction: true), "NextCharterAssentApplicableRestriction")
                }) {
                    var run = PortableWorld(AgreementPolicy(entry.Item1));
                    var query = run.QueryCommand(assent, AgreementCommand(run));
                    Require(query.Supported && !query.Admissible && query.Code == entry.Item2,
                        "Agreement query admitted a wrong authority or scoped permission: " + query.Code);
                    RejectUnchanged(run, assent, AgreementCommand(run), entry.Item2);
                }

                var withoutPermission = AgreementReady(AgreementPolicy(new TestOnlyNextCharterAgreementProfile(accessIssued: false)));
                Require(InspectPlan(withoutPermission, assent).ApproachAccess == true,
                    "The bare planning Boolean was absent in the independent permission control.");
                RejectUnchanged(withoutPermission, assent, AgreementCommand(withoutPermission), "NextCharterAssentPermissionMissing");
                var denied = AgreementReady(AgreementPolicy(planning: new TestOnlyNextCharterPlanProfile(approachAccess: false,
                    reserveWaterStartsCarried: true)));
                RejectUnchanged(denied, assent, AgreementCommand(denied), "NextCharterAssentPermissionContradicted");
            });

            cases.Add("mgt10_charter_assent_ready_resources_exact_grouped_claims_and_actual_capacity", () =>
            {
                var cached = AgreementReady(AgreementPolicy(planning: new TestOnlyNextCharterPlanProfile()));
                var cachedQuery = cached.QueryCommand(assent, AgreementCommand(cached));
                Require(cachedQuery.Code == "NextCharterAssentReadyReservesInsufficient"
                    && cachedQuery.NextCharterAgreementAssessment.CurrentObservation.Supplies[2].Lots.Single().PhysicalAmount == new RuleQuantity(4)
                    && cachedQuery.NextCharterAgreementAssessment.CurrentObservation.Supplies[2].ReadyAvailable == default,
                    "The cached physical reserve was counted as ready.");
                RejectUnchanged(cached, assent, AgreementCommand(cached), cachedQuery.Code);

                var closedPack = AgreementReady(readySupplies: false);
                PortableCommit(closedPack, Portable(closedPack, CommandKind.ClosePortableContainer, PortableKitFixture.Pack));
                RejectUnchanged(closedPack, assent, AgreementCommand(closedPack), "NextCharterAssentReadyReservesInsufficient");
                var inaccessible = closedPack.QueryCommand(assent, AgreementCommand(closedPack)).NextCharterAgreementAssessment.CurrentObservation;
                Require(inaccessible.Supplies[1].EligibleAvailable == new RuleQuantity(4) && inaccessible.Supplies[1].AccessibleAvailable == default,
                    "A closed pack changed physical water or supplied false access.");

                var nearCompanion = AgreementReady(clearApproach: false);
                var exact = SaveBill(nearCompanion, AgreementPolicy(), directory, "mgt10-charter-before-ration-custody");
                foreach (var input in new[] { (nearCompanion, 17), (exact, 16) }) {
                    var run = input.Item1;
                    WorldCommit(run, IC(run, CommandKind.PortionInventory, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(input.Item2))));
                    string portion = run.Capture().InventoryLots.Single(x => x.ParentId == PortableKitFixture.Rations).LotId;
                    PortableCommit(run, Portable(run, CommandKind.HandlePortableEquipment, portion, SaleSeller, HandlingKind.Handover));
                    WorldAdvance(run, 6);
                    ClearAgreementApproach(run);
                    var query = run.QueryCommand(assent, AgreementCommand(run));
                    var food = query.NextCharterAgreementAssessment.CurrentObservation.Supplies[0];
                    Require(food.ReadyAvailable == new RuleQuantity(20 - input.Item2) && food.Required == new RuleQuantity(4)
                        && food.Lots.Single(x => x.LotId == portion).CustodianId == SaleSeller,
                        "The actual handover failed the cumulative stock check.");
                    if (input.Item2 == 17)
                        RejectUnchanged(run, assent, AgreementCommand(run), "NextCharterAssentReadyReservesInsufficient");
                    else {
                        Require(query.Admissible, "Exactly four ready unreserved pounds failed admission: " + query.Code);
                        SaleCommit(run, AgreementCommand(run));
                        Require(run.Capture().NextCharterAgreement.Observation.Supplies[0].ReadyAvailable == new RuleQuantity(4),
                            "The exact four-pound boundary was not preserved.");
                    }
                }

                var busy = AgreementReady();
                WorldCommit(busy, IC(busy, CommandKind.StartIntake, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(17))));
                var busyQuery = busy.QueryCommand(assent, AgreementCommand(busy));
                Require(busyQuery.Code == "NextCharterAssentWorkerBusy"
                    && busyQuery.NextCharterAgreementAssessment.CurrentObservation.Supplies[0].ReadyAvailable == new RuleQuantity(3),
                    "A live claim failed to reduce unreserved availability or to block the worker independently.");
                RejectUnchanged(busy, assent, AgreementCommand(busy), busyQuery.Code);
                WorldCommit(busy, IC(busy, CommandKind.InterruptIntake, busy.Capture().Intakes.Single(x => x.ActorId == PlanHero && x.Status == IntakeStatus.Working).Id));
                Require(busy.QueryCommand(assent, AgreementCommand(busy)).Admissible, "A released historical claim still blocked assent.");

                // These are detached negative query projections. Ordinary handling cannot create an over-capacity save.
                var authorityPolicy = AgreementPolicy();
                var overweight = busy.Capture();
                overweight.PortableEquipment = overweight.PortableEquipment.Append(new PortableEquipmentRecord("TEST_ONLY.capacity-control",
                    "adventuring-gear.pouch", PlanHero, PlanHero, "", PortablePlacement.Carried, PortableLinkKind.None, "",
                    PortableMassBasis.Fixed, new RuleQuantity(1000), new RuleQuantity(1000))).ToArray();
                var projected = authorityPolicy.QueryCommand(overweight, assent, AgreementCommand(busy));
                Require(projected.Code == "NextCharterAssentCarryingCapacity"
                    && projected.NextCharterAgreementAssessment.CurrentObservation.CanCarry == false,
                    "The hard capacity limit did not block the actual burden projection.");
                var foreign = busy.Capture();
                var ration = foreign.InventoryLots.Single(x => x.LotId == PortableKitFixture.Rations);
                foreign.InventoryLots = foreign.InventoryLots.Select(x => x == ration
                    ? new InventoryLotRecord(x.LotId, x.ParentId, SaleSeller, x.CreatedAmount, x.CreatedAt, x.Nutrition, x.FreshUntil, x.Access)
                    : x).ToArray();
                projected = authorityPolicy.QueryCommand(foreign, assent, AgreementCommand(busy));
                Require(projected.Code == "NextCharterAssentReadyReservesInsufficient"
                    && !projected.NextCharterAgreementAssessment.CurrentObservation.Supplies[0].Lots.Single().UseAuthorized,
                    "An inventory grant or current custody conferred another owner's title.");
                SaleCommit(busy, AgreementCommand(busy));
            });

            cases.Add("mgt10_charter_assent_current_stable_boundary_and_no_second_desk_task", () =>
            {
                var occupied = AgreementReady(clearApproach: false);
                RejectUnchanged(occupied, assent, AgreementCommand(occupied), "NextCharterAssentPassageUnavailable");
                ClearAgreementApproach(occupied);
                WorldStep(occupied, -1, 0);
                RejectUnchanged(occupied, assent, AgreementCommand(occupied), "NextCharterAssentStationaryStagingRequired");
                WorldAdvance(occupied, 6);
                PlanWalk(occupied, 1, 0);
                WorldCommit(occupied, IC(occupied, CommandKind.BeginFixedEncounter));
                RejectUnchanged(occupied, assent, AgreementCommand(occupied), "NextCharterAssentStableBoundaryRequired");

                var preparedAt = AgreementReady().Capture().RuleClock;
                var incident = new CraftingMishapFact("assent-desk-incident", 1, at: preparedAt,
                    stationId: TestOnlyExpeditionBillProfile.DeskId);
                var run = AgreementReady(AgreementPolicy(incident: incident));
                CraftEvent(run, incident.Id);
                Require(CraftingRestrictions.StationUseBlocked(run.Capture(), TestOnlyExpeditionBillProfile.DeskId),
                    "The actual writing station restriction did not apply.");
                var before = run.Capture();
                SaleCommit(run, AgreementCommand(run));
                Require(run.Capture().NextCharterAgreement != null && run.Capture().RuleClock == before.RuleClock
                    && run.Capture().RandomState == before.RandomState && CraftingRestrictions.StationUseBlocked(run.Capture(), TestOnlyExpeditionBillProfile.DeskId),
                    "Explicit assent repeated writing work or cleared the actual station restriction.");
            });

            cases.Add("mgt10_charter_assent_half_open_expiry_and_withdrawal_without_resource_lock", () =>
            {
                var profile = new TestOnlyNextCharterAgreementProfile(validFrom: 11558, validUntil: 11585);
                var sim = AgreementReady(AgreementPolicy(profile));
                Require(sim.Capture().RuleClock == T(11557), "The authored validity control moved off its exact baseline.");
                RejectUnchanged(sim, assent, AgreementCommand(sim), "NextCharterAssentOfferOutsideWindow");
                var unaccepted = SaveBill(sim, AgreementPolicy(profile), directory, "mgt10-charter-before-validity");
                WorldAdvance(unaccepted, 28);
                RejectUnchanged(unaccepted, assent, AgreementCommand(unaccepted), "NextCharterAssentOfferOutsideWindow");
                WorldAdvance(unaccepted, 1);
                RejectUnchanged(unaccepted, assent, AgreementCommand(unaccepted), "NextCharterAssentOfferOutsideWindow");

                WorldAdvance(sim, 1);
                var accept = AgreementCommand(sim);
                SaleCommit(sim, accept);
                var record = sim.Capture().NextCharterAgreement;
                var expiring = SaveBill(sim, AgreementPolicy(profile), directory, "mgt10-charter-expiry-start");
                WorldAdvance(expiring, 26);
                Require(InspectAgreement(expiring, assent).InForce, "The agreement expired before its exact endpoint.");
                WorldAdvance(expiring, 1);
                Require(InspectAgreement(expiring, assent).Status == NextCharterAgreementStatus.Expired
                    && expiring.Capture().NextCharterAgreement.Withdrawal == null,
                    "Exact expiry rewrote the accepted history.");
                RejectUnchanged(expiring, assent, AgreementCommand(expiring, CommandKind.WithdrawNextCharter, AcceptedCharter), "NextCharterAgreementExpired");
                Require(expiring.Execute(assent, accept).Outcome == Outcome.Duplicate, "Identical assent lost idempotence after expiry.");
                SaveBill(expiring, AgreementPolicy(profile), directory, "mgt10-charter-expired");

                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Drop));
                PlanWalk(sim, -1, 0);
                var now = InspectAgreement(sim, assent);
                Require(now.InForce && now.CurrentObservation.Supplies[0].ReadyAvailable == default
                    && now.Agreement.Observation.Supplies[0].ReadyAvailable == new RuleQuantity(20),
                    "Ordinary stock loss could not update the current assessment independently.");
                var before = sim.Capture();
                var replay = SaveBill(sim, AgreementPolicy(profile), directory, "mgt10-charter-before-withdrawal");
                var command = AgreementCommand(sim, CommandKind.WithdrawNextCharter, AcceptedCharter);
                foreach (var branch in new[] { sim, replay }) {
                    Require(branch.Execute(assent, command).Outcome == Outcome.Committed, "Authorized withdrawal required the desk or sufficient stock.");
                    var withdrawn = branch.Capture();
                    var stored = withdrawn.NextCharterAgreement;
                    var status = InspectAgreement(branch, assent);
                    Require(stored.Withdrawal.CommandId == command.Id && stored.Withdrawal.Revision == before.Revision + 1
                        && stored.Withdrawal.At == before.RuleClock && status.Status == NextCharterAgreementStatus.Withdrawn && !status.InForce,
                        "Withdrawal lost its actual boundary or retained force.");
                    withdrawn.NextCharterAgreement = before.NextCharterAgreement;
                    withdrawn.Revision = before.Revision;
                    withdrawn.Receipts = before.Receipts;
                    Require(codec.Encode(withdrawn).SequenceEqual(codec.Encode(before)), "Withdrawal mutated stock, clock, RNG, or another procedure.");
                    Require(branch.Execute(assent, command).Outcome == Outcome.Duplicate
                        && branch.Execute(assent, accept).Outcome == Outcome.Duplicate, "Withdrawal broke command replay.");
                    RejectUnchanged(branch, assent, AgreementCommand(branch, CommandKind.WithdrawNextCharter, AcceptedCharter),
                        "NextCharterAlreadyWithdrawn");
                    RejectUnchanged(branch, assent, AgreementCommand(branch), "NextCharterOfferAlreadyAccepted");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)) && record.AcceptedAt == T(11558), "Withdrawal replay diverged.");
                SaveBill(sim, AgreementPolicy(profile), directory, "mgt10-charter-withdrawn");
            });

            cases.Add("mgt10_charter_assent_replay_rejects_forged_history", () =>
            {
                var sim = AgreementReady();
                SaleCommit(sim, AgreementCommand(sim));
                var record = sim.Capture().NextCharterAgreement;
                var terms = record.Terms;
                var report = record.Observation;
                var forged = sim.Capture();
                NextCharterAgreementRecord Copy(NextCharterAgreementTerms replacementTerms = null,
                    NextCharterPlanObservation replacementObservation = null, long? priorClose = null)
                    => new NextCharterAgreementRecord(replacementTerms ?? terms, record.PlanId, record.PlanReportRevision,
                        priorClose ?? record.PriorCloseRevision, record.CommandId, record.AcceptedRevision, replacementObservation ?? report);
                forged.NextCharterAgreement = Copy(priorClose: record.PriorCloseRevision - 1);
                Throws<ArgumentException>(() => codec.Encode(forged));

                NextCharterAgreementTerms TermsWith(string mandate, NextCharterAccessPermission permission)
                    => new NextCharterAgreementTerms(terms.OfferId, terms.CharterId, terms.CharterVersionId, mandate,
                        terms.RecordsAccessId, terms.ResourceUseAuthorityId, terms.ResourceOwnerId, terms.SoloOffices,
                        terms.PlanTerms, permission, terms.ValidFrom, terms.ValidUntil);
                forged.NextCharterAgreement = Copy(TermsWith("forged-mandate", terms.AccessPermission));
                RejectAgreementReplay(codec, forged);
                forged.NextCharterAgreement = Copy(TermsWith(terms.AssentAuthorityId, TestOnlyNextCharterAgreementProfile.IssueAccess(issuerId: SaleBuyer)));
                RejectAgreementReplay(codec, forged);

                var food = report.Supplies[0];
                var lot = food.Lots.Single();
                var falseLot = new NextCharterStockObservation(lot.LotId, lot.OwnerId, lot.CustodianId, lot.LocationId, lot.PhysicalAmount,
                    new RuleQuantity(19), lot.UseAuthorized, lot.CorrectCustody, lot.Carried, lot.Suitable, lot.Accessible, lot.Ready);
                var falseFood = new NextCharterSupplyObservation(food.RootId, "", null, "", "", "", food.Required, new[] { falseLot });
                forged.NextCharterAgreement = Copy(replacementObservation: CopyPlanObservation(report, report.At,
                    new[] { falseFood, report.Supplies[1], report.Supplies[2] }));
                RejectAgreementReplay(codec, forged);
                var unsupportedRisk = new NextCharterPlanObservation(report.At, report.Revision, report.Walkable, report.Occupied,
                    report.PathReserved, report.TacticalTransition, report.ApproachAccess, report.ScoutCapable, report.ScoutAtStage,
                    report.ActualPounds, report.ActualLoad, report.CanCarry, report.Burdened, 0, report.Strain, report.RestDebt, report.Supplies);
                forged.NextCharterAgreement = Copy(replacementObservation: unsupportedRisk);
                RejectAgreementReplay(codec, forged);

                SaleCommit(sim, AgreementCommand(sim, CommandKind.WithdrawNextCharter, AcceptedCharter));
                forged = sim.Capture();
                var withdrawal = forged.NextCharterAgreement.Withdrawal;
                forged.NextCharterAgreement = record.WithWithdrawal(new NextCharterWithdrawal("forged-withdrawal", withdrawal.Revision, withdrawal.At));
                Throws<ArgumentException>(() => codec.Encode(forged));
                Throws<ArgumentException>(() => new Simulation(AgreementPolicy(new TestOnlyNextCharterAgreementProfile(validUntil: 23000)),
                    sim.Capture(), ExecutionProfile.Laboratory));
            });
        }

        private static void RejectAgreementReplay(SnapshotCodec codec, Snapshot forged)
        {
            var decoded = codec.Decode(codec.Encode(forged));
            bool rejectedByReplay = false;
            try { new Simulation(AgreementPolicy(), decoded, ExecutionProfile.Laboratory); }
            catch (ArgumentException ex) { rejectedByReplay = ex.Message.Contains("InvalidSharedWorldReplay"); }
            Require(rejectedByReplay, "A structurally coherent forged charter bypassed historical replay.");
        }

        private static string AgreementAudit(string label, Snapshot state, NextCharterAgreementRecord agreement, NextCharterPlanObservation view)
            => string.Join("\t", label, agreement.Terms.CharterId, "close=" + state.ExpeditionEpisodeClose.ClosedAt,
                "close-rev=" + agreement.PriorCloseRevision, "plan=" + state.NextCharterPlans.Single().Report.At,
                "plan-rev=" + agreement.PlanReportRevision, "assent=" + agreement.AcceptedAt, "assent-rev=" + agreement.AcceptedRevision,
                "source-rev=" + agreement.SourceRevision, "view-at=" + view.At, "view-rev=" + view.Revision,
                "food-designated=" + agreement.Terms.PlanTerms.IntendedFood + "+" + agreement.Terms.PlanTerms.ReserveFood,
                "water-designated-per-vessel=" + agreement.Terms.PlanTerms.WaterPerVessel,
                "exclusive-commitment=" + agreement.Terms.ReservesExclusivelyCommitted, "cash-limit=" + agreement.Terms.NewCashLimitCopper,
                "permission=" + agreement.Terms.AccessPermission.VersionId, "permission-basis=" + agreement.Terms.AccessPermission.IssuerAuthorityId,
                "pounds=" + view.ActualPounds, "departure=" + view.DeparturePermitted,
                string.Join(";", view.Supplies.Select(x => string.Join(",", x.RootId, x.VesselId, x.Required, x.EligibleAvailable, x.ReadyAvailable))));
    }
}
#endif
