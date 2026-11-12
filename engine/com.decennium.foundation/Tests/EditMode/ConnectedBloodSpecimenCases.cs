#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy BloodHandoffPolicy()
            => ConnectedObservationPolicy().EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen();

        private static Command BloodVesselCommand(Simulation sim, CommandKind kind, HandlingKind? handling = null)
            => IC(sim, kind, ConnectedBloodSpecimen.Vessel,
                handling.HasValue ? new InventoryRequest(new RuleQuantity(1), handling: handling.Value) : null,
                ConnectedBloodSpecimen.Worker);

        private static Command BloodTreatmentCommand(Simulation sim)
            => IC(sim, CommandKind.StartHarvestPreservationTreatment, ConnectedBloodSpecimen.SpecimenId,
                new InventoryRequest(new RuleQuantity(1)), ConnectedBloodSpecimen.Worker);

        private static HarvestPreservationTreatmentAttemptRecord BloodTreatment(Simulation sim)
            => sim.Capture().HarvestPreservationTreatmentAttempts.Single();

        private static HarvestPreservationView BloodAge(Simulation sim)
        {
            Require(HarvestPreservationRules.TryProject(sim.Capture(), ConnectedBloodSpecimen.SpecimenId, out var view),
                "The supplied physical specimen lost its distinct preservation projection.");
            return view;
        }

        private static Simulation SaveBlood(Simulation sim, TestOnlySharedWorldPolicy policy, string directory, string stage)
            => SaveBill(sim, policy, directory, "mgt05-connected-blood-" + stage);

        private static void AdvanceBloodTo(Simulation sim, RuleTime endpoint)
        {
            var now = sim.Capture().RuleClock;
            Require(now.Denominator == 1 && endpoint.Denominator == 1 && endpoint > now,
                "The selected ordinary-clock test requires a later whole-second boundary.");
            WorldAdvance(sim, checked((int)(endpoint.Numerator - now.Numerator)));
        }

        private static void AddConnectedBloodSpecimenCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("mgt05_connected_blood_treatment_delivery_timeout_and_real_recipe_eligibility", () =>
            {
                var policy = BloodHandoffPolicy();
                var sim = LaterPrepared(policy);
                var ready = sim.Capture();
                var definition = ready.BloodSpecimen;
                Require(ready.WireSchemaVersion == 94 && ready.SchemaVersion == 90
                    && ready.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                    && ready.LaterEncounter.FirstExit.ClosedAt == T(15) && ready.HavenSales.Single().PaymentCopper == 2
                    && definition.Origin == default && definition.IntervalSeconds == 14400
                    && definition.SourceOccurrence == "/recipes/13/components/2"
                    && definition.RecipeOccurrence == "/recipes/3/components/3"
                    && !FormulaResearchRules.Knows(ready, ConnectedBloodSpecimen.Worker, ManufacturingRules.Recipe4Id)
                    && ready.HarvestUnits.Length == 0, "The genuine returned expedition did not retain exact independent starting stock.");
                var specimen = ready.PortableEquipment.Single(x => x.Id == definition.LotId);
                var vessel = ready.PortableEquipment.Single(x => x.Id == definition.VesselId);
                Require(specimen.ParentId == vessel.Id && vessel.GroundX == 4 && vessel.GroundY == 3
                    && PortableEquipmentValidation.Mass(ready, specimen) == new RuleQuantity(19, 50)
                    && ready.Work.AvailableAmount(definition.LotId) == new RuleQuantity(1)
                    && ready.Work.AvailableAmount(definition.SupplyLotId) == new RuleQuantity(1, 2)
                    && !vessel.Open, "The one counted specimen, its physical fit, and its actual preservative must exist before play.");
                FormulaDenial(sim, host, BloodTreatmentCommand(sim), "BloodTreatmentContainerFitNotEstablished");
                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.OpenPortableContainer));
                byte[] beforeQuery = Bytes(sim);
                var start = sim.DiscoverCommands(host, ConnectedBloodSpecimen.Worker)
                    .Single(x => x.Command.Kind == CommandKind.StartHarvestPreservationTreatment);
                Require(start.Query.Admissible && Bytes(sim).SequenceEqual(beforeQuery), "Treatment discovery changed the live state.");
                LaterCommit(sim, start.Command);
                Require(sim.Execute(host, start.Command).Outcome == Outcome.Duplicate, "Treatment start repeated its claims.");
                FormulaDenial(sim, host, BloodVesselCommand(sim, CommandKind.ClosePortableContainer), "HarvestTreatmentInputsInUse");
                WorldAdvance(sim, 600);
                var mid = sim.Capture();
                var attempt = BloodTreatment(sim);
                Require(attempt.Work.Labor == T(600) && mid.RandomState == ready.RandomState
                    && mid.Work.AvailableAmount(definition.LotId) == default && mid.Work.AvailableAmount(definition.SupplyLotId) == default
                    && mid.Work.Lots.Single(x => x.Id == definition.SupplyLotId).Amount == new RuleQuantity(1, 2)
                    && !HarvestPreservationRules.IsProtectedAt(mid, definition.LotId, mid.RuleClock),
                    "The active treatment must reserve supplies without spending them or granting protection early.");
                FormulaDenial(sim, host, BloodVesselCommand(sim, CommandKind.ClosePortableContainer), "OffCalendarActionAlreadySpent");
                var restored = SaveBlood(sim, policy, directory, "mid-treatment");
                foreach (var run in new[] { sim, restored }) {
                    WorldAdvance(run, 1200);
                    var treated = run.Capture();
                    var completed = BloodTreatment(run);
                    var draw = PlaytestDice.RollD20(mid.RandomState);
                    Require(completed.Status == HarvestPreservationTreatmentStatus.Success && completed.Work.Labor == T(1800)
                        && completed.Natural == draw.Natural && completed.SealedAt == treated.RuleClock
                        && treated.RandomState == draw.NextRandomState && treated.Work.AvailableAmount(definition.LotId) == new RuleQuantity(1)
                        && treated.Work.Reservations.Single(x => x.Id == completed.SupplyReservationId).ConsumedAmount == new RuleQuantity(1, 2)
                        && PortableEquipmentValidation.Mass(treated, treated.PortableEquipment.Single(x => x.Id == ConnectedBloodSpecimen.Packing)) == new RuleQuantity(1, 2)
                        && !treated.PortableEquipment.Any(x => x.Id == definition.SupplyLotId)
                        && BloodAge(run).UnprotectedAge == treated.RuleClock
                        && HarvestPreservationRules.IsProtectedAt(treated, definition.LotId, treated.RuleClock),
                        "The actual endpoint must roll once, settle supply, retain packing mass, and preserve origin.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Restored treatment diverged at settlement.");
                var sealedBranch = SaveBlood(sim, policy, directory, "protected");
                var settledAt = sim.Capture().RuleClock;

                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                AdvanceBloodTo(sim, T(28800));
                Require(ResearchJob(sim).Status == FormulaWorkStatus.Paused, "The actual research window did not pause.");
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.ResumeFormulaWork));
                WorldAdvance(sim, checked((int)settledAt.Numerator));
                var learned = sim.Capture();
                Require(ResearchJob(sim).Work.Labor == T(28800)
                    && FormulaResearchRules.Knows(learned, ConnectedBloodSpecimen.Worker, ManufacturingRules.Recipe4Id)
                    && BloodAge(sim).UnprotectedAge == settledAt, "Genuine knowledge did not preserve the earlier treatment and original age.");

                var priorBurden = PortableEquipmentRules.CarriedBurden(learned, ConnectedBloodSpecimen.Worker);
                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.HandlePortableEquipment, HandlingKind.Pickup));
                var carried = sim.Capture();
                var burden = PortableEquipmentRules.CarriedBurden(carried, ConnectedBloodSpecimen.Worker);
                Require(priorBurden.Pounds.HasValue && burden.Pounds == priorBurden.Pounds.Value + new RuleQuantity(47, 25), "Sealed cargo must count the vessel, specimen and retained packing.");
                PlanWalk(sim, -1, 0, ConnectedBloodSpecimen.Worker);
                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.HandlePortableEquipment, HandlingKind.Drop));
                var delivered = sim.Capture();
                vessel = delivered.PortableEquipment.Single(x => x.Id == definition.VesselId);
                Require(!vessel.Open && vessel.GroundX == 3 && vessel.GroundY == 3
                    && delivered.PortableEquipment.Single(x => x.Id == definition.LotId).ParentId == vessel.Id,
                    "The exact sealed specimen did not reach the workshop through physical movement.");
                SaveBlood(sim, policy, directory, "delivered-closed");
                Require(policy.AssessRecipe4Specimen(delivered, host, ConnectedBloodSpecimen.Worker, definition.LotId).Code
                    == "BloodSpecimenWorkshopAccessUnavailable", "A sealed inaccessible specimen was admitted.");
                FormulaDenial(sim, host, ManufactureCommand(sim), "ManufacturingIngredientSpoiled");
                FormulaDenial(sim, host, ManufactureCommand(sim, x: 1), "ManufacturingIngredientSpoiled");

                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.OpenPortableContainer));
                var opened = sim.Capture();
                var opening = opened.HarvestPreservationEvidence.Single();
                Require(opening.At == opened.PortableHandling.Last().EndedAt && opening.At == opened.RuleClock
                    && opening.CleanToolFactId == definition.CleanToolFactId
                    && HarvestPreservationRules.IsProtectedAt(opened, definition.LotId, opened.RuleClock),
                    "Protection ended at opening instead of the real clean-opening cutoff.");
                FormulaDenial(sim, host, LaterApproach(sim), "HarvestPreservationOpenLifecycleTacticalUnsupported");
                var missingOpening = opened.Copy();
                missingOpening.HarvestPreservationEvidence = Array.Empty<HarvestPreservationEvidenceRecord>();
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(missingOpening));
                var unclean = opened.Copy();
                unclean.HarvestPreservationEvidence = new[] {
                    new HarvestPreservationEvidenceRecord(opening.Id, opening.Kind, opening.TreatmentAttemptId,
                        opening.VesselId, opening.CommandId, opening.AppliedRevision, opening.At,
                        portableHandlingId: opening.PortableHandlingId, toolId: opening.ToolId,
                        cleanToolFactId: "TEST_ONLY.unbound-clean-tool")
                };
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(unclean));
                var replay = SaveBlood(sim, policy, directory, "delivered-open");
                var closeEarly = new Simulation(policy, opened, ExecutionProfile.Laboratory);
                WorldAdvance(closeEarly, 58);
                LaterCommit(closeEarly, BloodVesselCommand(closeEarly, CommandKind.ClosePortableContainer));
                Require(closeEarly.Capture().RuleClock == opening.At.AddSeconds(59)
                    && HarvestPreservationRules.IsProtectedAt(closeEarly.Capture(), definition.LotId, closeEarly.Capture().RuleClock),
                    "Closing strictly before the limit lost earned protection.");

                var closeAtLimit = new Simulation(policy, opened, ExecutionProfile.Laboratory);
                WorldAdvance(closeAtLimit, 59);
                LaterCommit(closeAtLimit, BloodVesselCommand(closeAtLimit, CommandKind.ClosePortableContainer));
                Require(closeAtLimit.Capture().RuleClock == opening.At.AddSeconds(60)
                    && !HarvestPreservationRules.IsProtectedAt(closeAtLimit.Capture(), definition.LotId, closeAtLimit.Capture().RuleClock),
                    "Closing at the exclusive limit restored protection.");

                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 59);
                    Require(HarvestPreservationRules.IsProtectedAt(run.Capture(), definition.LotId, run.Capture().RuleClock),
                        "The clean interval cut off too early.");
                    WorldAdvance(run, 1);
                    var atCutoff = run.Capture();
                    var bytes = Bytes(run);
                    var assay = policy.AssessRecipe4Specimen(atCutoff, host, ConnectedBloodSpecimen.Worker, definition.LotId);
                    Require(atCutoff.RuleClock == opening.At.AddSeconds(60)
                        && !HarvestPreservationRules.IsProtectedAt(atCutoff, definition.LotId, atCutoff.RuleClock)
                        && assay.Eligible && assay.CurrentAge == settledAt && assay.FirstPhaseAge == settledAt.AddSeconds(900)
                        && Bytes(run).SequenceEqual(bytes) && atCutoff.ManufacturingOrders.Length == 0,
                        "The same physically accessible specimen must pass the pure real assessment at the actual cutoff.");
                    FormulaDenial(run, host, LaterApproach(run), "HarvestPreservationOpenLifecycleTacticalUnsupported");
                    if (run == sim) {
                        var closedBranch = SaveBlood(sim, policy, directory, "cutoff");
                        FormulaDenial(closedBranch, host, LaterApproach(closedBranch),
                            "HarvestPreservationOpenLifecycleTacticalUnsupported");
                        LaterCommit(closedBranch, BloodVesselCommand(closedBranch, CommandKind.ClosePortableContainer));
                        Require(!HarvestPreservationRules.IsProtectedAt(closedBranch.Capture(), definition.LotId,
                                closedBranch.Capture().RuleClock)
                            && BloodAge(closedBranch).UnprotectedAge == settledAt.AddSeconds(1),
                            "Closing after timeout restored treatment or changed age beyond its elapsed second.");
                        EnterLater(closedBranch);
                        Require(closedBranch.Capture().InventoryCombat,
                            "The real later encounter stayed gated after the physical close.");
                        SaveBlood(closedBranch, policy, directory, "tactical-entry-after-close");
                    }
                    WorldAdvance(run, 900);
                    Require(BloodAge(run).UnprotectedAge == settledAt.AddSeconds(900)
                        && run.Capture().ManufacturingOrders.Length == 0 && run.Capture().AlchemyDoses.Length == 0,
                        "Ordinary elapsed observation cannot book a manufacturing phase or stabilize the input.");
                    FormulaDenial(run, host, LaterApproach(run), "HarvestPreservationOpenLifecycleTacticalUnsupported");
                    PlanWalk(run, 0, -1);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Restored opening cutoff and ordinary continuation diverged.");
                SaveBlood(sim, policy, directory, "continued");

                var readyAgain = sim.Capture();
                var age = BloodAge(sim).UnprotectedAge;
                Require(policy.AssessRecipe4Specimen(readyAgain, host, ConnectedBloodSpecimen.Worker, "missing.specimen").Code
                        == "BloodSpecimenMissing"
                    && policy.AssessRecipe4Specimen(readyAgain, host, ConnectedBloodSpecimen.Worker,
                        SharedManufacturingFixture.Lot(0, 3)).Code == "BloodSpecimenBindingMismatch",
                    "The real assessor must distinguish missing and wrong material identities.");
                var reserved = readyAgain.Copy();
                reserved.Work = reserved.Work.Reserve("specimen.reserve-control", Array.Empty<WorkerInterval>(),
                    new[] { new ResourceReservation("specimen.reserve-control.claim", "specimen.reserve-control", definition.LotId, 1) });
                Require(policy.AssessRecipe4Specimen(reserved, host, ConnectedBloodSpecimen.Worker, definition.LotId).Code
                    == "ManufacturingIngredientsUnavailable", "The detached reserved-lot control must not double-allocate stock.");

                AdvanceBloodTo(sim, readyAgain.RuleClock.AddSeconds(14400 - age.Numerator));
                Require(BloodAge(sim).State == HarvestPreservationState.Degraded
                    && policy.AssessRecipe4Specimen(sim.Capture(), host, ConnectedBloodSpecimen.Worker, definition.LotId).Eligible,
                    "The actual Degraded threshold incorrectly became a Fresh-only recipe gate.");
                WorldAdvance(sim, 13500);
                Require(BloodAge(sim).UnprotectedAge == T(27900)
                    && policy.AssessRecipe4Specimen(sim.Capture(), host, ConnectedBloodSpecimen.Worker, definition.LotId).Code
                        == "BloodSpecimenSpoilsBeforeStabilization",
                    "The projected 900-second endpoint must reject exact simultaneous spoilage.");
                WorldAdvance(sim, 900);
                Require(BloodAge(sim).State == HarvestPreservationState.Spoiled
                    && !policy.AssessRecipe4Specimen(sim.Capture(), host, ConnectedBloodSpecimen.Worker, definition.LotId).Eligible,
                    "Actual elapsed spoilage remained eligible.");
                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.ClosePortableContainer));
                Require(!HarvestPreservationRules.IsProtectedAt(sim.Capture(), definition.LotId, sim.Capture().RuleClock),
                    "Late closing restored expired protection.");
                SaveBlood(sim, policy, directory, "late-close-spoiled");

                AdvanceBloodTo(sealedBranch, settledAt.AddSeconds(86399));
                Require(HarvestPreservationRules.IsProtectedAt(sealedBranch.Capture(), definition.LotId, sealedBranch.Capture().RuleClock),
                    "The sealed specimen lost protection before natural expiry.");
                WorldAdvance(sealedBranch, 1);
                Require(!HarvestPreservationRules.IsProtectedAt(sealedBranch.Capture(), definition.LotId, sealedBranch.Capture().RuleClock)
                    && BloodAge(sealedBranch).UnprotectedAge == settledAt, "Natural expiry failed at the exclusive elapsed-time boundary.");
                SaveBlood(sealedBranch, policy, directory, "sealed-natural-expiry");
            });

            cases.Add("mgt05_connected_blood_failed_treatment_and_spoiled_admission", () =>
            {
                var policy = BloodHandoffPolicy();
                var sim = LaterPrepared(policy);
                ReachConnectedObservationWindow(sim);
                PrepareConnectedConcealment(sim);
                LaterCommit(sim, ExplorationSearchCommand(sim));
                SearchAdvance(sim, 18);
                PlanWalk(sim, 0, 1, ConnectedBloodSpecimen.Worker);
                LaterCommit(sim, BloodVesselCommand(sim, CommandKind.OpenPortableContainer));
                var spoiled = new Simulation(policy, sim.Capture(), ExecutionProfile.Laboratory);
                AdvanceBloodTo(spoiled, T(28800));
                FormulaDenial(spoiled, host, BloodTreatmentCommand(spoiled), "HarvestTreatmentCannotFinishBeforeSpoilage");
                Require(BloodAge(spoiled).State == HarvestPreservationState.Spoiled, "The test did not reach real specimen spoilage.");
                uint rng = sim.Capture().RandomState;
                LaterCommit(sim, BloodTreatmentCommand(sim));
                WorldAdvance(sim, 1800);
                var state = sim.Capture();
                var failed = BloodTreatment(sim);
                var draw = PlaytestDice.RollD20(rng);
                Require(failed.Status == HarvestPreservationTreatmentStatus.Failure && failed.Natural == draw.Natural
                    && failed.Work.Labor == T(1800) && !failed.SealedAt.HasValue && state.RandomState == draw.NextRandomState
                    && !HarvestPreservationRules.IsProtectedAt(state, failed.InventoryLotId, state.RuleClock)
                    && state.Work.Reservations.Single(x => x.Id == failed.SupplyReservationId).ConsumedAmount == new RuleQuantity(1, 2)
                    && state.Work.AvailableAmount(failed.InventoryLotId) == new RuleQuantity(1),
                    "The actual failed check must settle supply and retain the whole unprotected specimen.");
                FormulaDenial(sim, host, BloodTreatmentCommand(sim), "HarvestTreatmentAlreadyAttempted");
                SaveBlood(sim, policy, directory, "failed-treatment");
            });

            cases.Add("mgt05_connected_blood_wire94_exact_profile_and_malformed_origin", () =>
            {
                var codec = new SnapshotCodec();
                var original = ConnectedObservationPolicy().EnableConnectedFormulaResearch();
                var selected = BloodHandoffPolicy();
                var old = original.Initial();
                var initial = selected.Initial();
                var encoded = codec.Encode(initial);
                Require(old.WireSchemaVersion == 93 && BitConverter.ToInt32(encoded, 4) == 94
                    && codec.Decode(encoded).SchemaVersion == 90 && codec.Encode(codec.Decode(encoded)).SequenceEqual(encoded)
                    && initial.ContentFingerprint != old.ContentFingerprint && ConnectedExplorationObservation.IsSelected(initial),
                    "The distinct wire must preserve recognition and encode its exact base once.");
                Throws<ArgumentException>(() => new Simulation(original, codec.Decode(encoded), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(selected, codec.Decode(codec.Encode(old)), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(selected, codec.Decode(encoded), ExecutionProfile.Release));
                Throws<InvalidOperationException>(() => selected.EnableConnectedBloodSpecimen());
                Throws<InvalidOperationException>(() => ConnectedObservationPolicy().EnableConnectedBloodSpecimen());

                byte[] Retag(int wire)
                {
                    var body = encoded.Take(encoded.Length - 32).ToArray();
                    Array.Copy(BitConverter.GetBytes(wire), 0, body, 4, 4);
                    using (var sha = SHA256.Create()) return body.Concat(sha.ComputeHash(body)).ToArray();
                }
                Throws<InvalidDataException>(() => codec.Decode(Retag(93)));
                var absent = initial.Copy();
                absent.BloodSpecimen = null;
                Throws<ArgumentException>(() => codec.Encode(absent));
                var inflated = initial.Copy();
                inflated.Work = new WorkLedger(inflated.Work.Lots.Select(x => x.Id == ConnectedBloodSpecimen.SpecimenId
                    ? new ResourceLot(x.Id, x.UnitId, 2, x.LocationId, x.CustodianId) : x),
                    inflated.Work.WorkerIntervals, inflated.Work.Reservations);
                Throws<ArgumentException>(() => codec.Encode(inflated));

                var specimen = initial.BloodSpecimen;
                ConnectedBloodSpecimen Rebind(RuleTime origin, int interval, string mapping)
                    => new ConnectedBloodSpecimen(specimen.AuthorityId, specimen.LotId, specimen.SourceOccurrence, mapping,
                        origin, interval, specimen.UnitMass, specimen.VesselId, specimen.FitId, specimen.SupplyLotId,
                        specimen.ToolId, specimen.CleanToolFactId);
                Throws<ArgumentException>(() => Rebind(T(1), specimen.IntervalSeconds, specimen.RecipeOccurrence));
                Throws<ArgumentException>(() => Rebind(default, 3600, specimen.RecipeOccurrence));
                Throws<ArgumentException>(() => Rebind(default, specimen.IntervalSeconds, "/recipes/3/components/2"));
            });
        }
    }
}
#endif
