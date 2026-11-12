#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedBloodSpecimen;

        public TestOnlySharedWorldPolicy EnableConnectedBloodSpecimen()
        {
            if (initializationStarted || connectedBloodSpecimen || !connectedFormulaResearch
                || !ContentFingerprint.StartsWith(ConnectedExplorationObservation.FingerprintPrefix, StringComparison.Ordinal))
                throw new InvalidOperationException("Select the blood specimen once before initializing the connected recipe-4 expedition.");

            var manifest = TestOnlyContentManifest.CreateManufacturingExpansionProfile();
            var recipe4 = manifest.ResolveSemantic("crafting", ManufacturingRules.Recipe4Id);
            var recipe14 = manifest.ResolveSemantic("crafting", ManufacturingRules.Recipe14Id);
            var recipe4Specimen = manifest.ResolveSemantic("crafting-component", ConnectedBloodSpecimen.MaterialId);
            var recipe14Specimen = manifest.ResolveSemantic("crafting-component", ManufacturingRules.Recipe14Id + "." + ConnectedBloodSpecimen.MaterialId);
            if (manifest.ValidateBindings() != null || !manifest.Supports(recipe4, ContentOperation.Manufacture)
                || !manifest.Supports(recipe14, ContentOperation.Manufacture)
                || !manifest.Supports(recipe4Specimen, ContentOperation.Manufacture)
                || !manifest.Supports(recipe14Specimen, ContentOperation.Manufacture)
                || recipe4Specimen.SourceRevision != ConnectedBloodSpecimen.SourceRevision
                || recipe14Specimen.SourceRevision != ConnectedBloodSpecimen.SourceRevision
                || recipe4Specimen.JsonPointer != ConnectedBloodSpecimen.RecipePointer
                || recipe14Specimen.JsonPointer != recipe14.JsonPointer + "/sourceRequirements/components/2")
                throw new InvalidOperationException("The exact recipe material occurrences are unavailable.");

            connectedBloodSpecimen = true;
            var specimen = ConnectedBloodSpecimen.Selected();
            ContentFingerprint = ConnectedBloodSpecimen.FingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, recipe4Specimen.Canonical, recipe14Specimen.Canonical, specimen.AuthorityId, specimen.LotId,
                specimen.SourceOccurrence, specimen.RecipeOccurrence, specimen.Origin, specimen.IntervalSeconds, specimen.UnitMass,
                specimen.VesselId, specimen.FitId, specimen.SupplyLotId, specimen.ToolId, specimen.CleanToolFactId,
                "staging-4,3|bench-3,3|one-counted-unit|vessel-1lb-10lb-1cuft|terminal-supply-to-retained-packing|clean-open-60s"));
            return this;
        }

        private static PortableStorageProfileRecord BloodStorageProfile()
            => new PortableStorageProfileRecord(ConnectedBloodSpecimen.MaterialProfile, ConnectedBloodSpecimen.MaterialId,
                packedVolumePerUnitCubicFeet: null, massPerUnitLb: ConnectedBloodSpecimen.Mass);

        private void InitializeConnectedBloodSpecimen(Snapshot s)
        {
            if (!connectedBloodSpecimen) return;
            var specimen = ConnectedBloodSpecimen.Selected();
            s.BloodSpecimen = specimen;
            const string worker = ConnectedBloodSpecimen.Worker;
            var supplyAmount = HarvestPreservationTreatmentValidation.SupplyAmount;
            s.Work = new WorkLedger(s.Work.Lots.Concat(new[] {
                new ResourceLot(specimen.LotId, ConnectedBloodSpecimen.MaterialId, 1, SharedCraftingFixture.StationId, worker),
                new ResourceLot(specimen.SupplyLotId, "mass-pound", supplyAmount, SharedCraftingFixture.StationId, worker)
            }), s.Work.WorkerIntervals, s.Work.Reservations);
            s.InventoryLots = s.InventoryLots.Concat(new[] {
                new InventoryLotRecord(specimen.LotId, "", worker, new RuleQuantity(1), specimen.Origin, NutritionKind.None, null, InventoryAccess.Ground),
                new InventoryLotRecord(specimen.SupplyLotId, "", worker, supplyAmount, s.RuleClock, NutritionKind.None, null, InventoryAccess.Ground)
            }).ToArray();
            s.PortableStorageProfiles = s.PortableStorageProfiles.Append(BloodStorageProfile()).ToArray();
            s.PortableEquipment = s.PortableEquipment.Concat(new[] {
                new PortableEquipmentRecord(specimen.VesselId, HarvestPreservationTreatmentFixture.ContainerProfileId, worker, worker, "",
                    PortablePlacement.Ground, PortableLinkKind.None, "", PortableMassBasis.Fixed, new RuleQuantity(1), new RuleQuantity(1),
                    capacityPounds: new RuleQuantity(10), capacityCubicFeet: new RuleQuantity(1), open: false,
                    fitRuleId: specimen.FitId, fitMemberIds: new[] { specimen.LotId, specimen.SupplyLotId, ConnectedBloodSpecimen.Packing },
                    groundX: 4, groundY: 3),
                new PortableEquipmentRecord(specimen.LotId, ConnectedBloodSpecimen.MaterialProfile, worker, worker, specimen.VesselId,
                    PortablePlacement.Contained, PortableLinkKind.InventoryLot, specimen.LotId, PortableMassBasis.CountedQuantity, null, null),
                new PortableEquipmentRecord(specimen.SupplyLotId, "TEST_ONLY.specimen-preservative.v1", worker, worker, specimen.VesselId,
                    PortablePlacement.Contained, PortableLinkKind.InventoryLot, specimen.SupplyLotId, PortableMassBasis.GenericPounds, null, null)
            }).ToArray();
            PortableEquipmentRules.SynchronizeLinks(s);
        }

        private static HarvestPreservationTreatmentAttemptRecord ActiveBloodTreatment(Snapshot s)
            => s.BloodSpecimen == null ? null : s.HarvestPreservationTreatmentAttempts
                .SingleOrDefault(x => x.Status == HarvestPreservationTreatmentStatus.Working);

        private string ValidateConnectedBloodProfile(Snapshot s)
        {
            if (connectedBloodSpecimen != (s.BloodSpecimen != null)) return "ConnectedBloodProfileMismatch";
            if (!connectedBloodSpecimen) return null;
            var storage = PortableStorageProfileValidation.Find(s, ConnectedBloodSpecimen.MaterialProfile);
            var vessel = s.PortableEquipment.Single(x => x.Id == s.BloodSpecimen.VesselId);
            if (vessel.ProfileId != HarvestPreservationTreatmentFixture.ContainerProfileId)
                return "ConnectedBloodVesselProfileMismatch";
            if (storage == null || storage.PackedVolumePerUnitCubicFeet.HasValue
                || storage.AllowedContainedProfileIds.Count != 0 || storage.RequiresInstalledTemporaryCamp)
                return "ConnectedBloodStorageProfileMismatch";
            if (s.InventoryCombat && BloodTacticalTransitionFailure(s) != null)
                return "ConnectedBloodTacticalHistoryMismatch";
            return null;
        }

        private string BloodTreatmentAccess(Snapshot s, string actor)
        {
            if (actor != ConnectedBloodSpecimen.Worker || !manufacturing.ToolTrained
                || !s.Trades.Any(x => x.WorkerId == actor && x.TradeId == SharedCraftingFixture.TradeId && x.Level >= 5))
                return "BloodTreatmentAlchemyTrainingRequired";
            if (!ConnectedResearchWorkshopAvailable(s) || TargetInActiveRepair(s, s.BloodSpecimen.ToolId))
                return "BloodTreatmentToolUnavailable";
            if (!ResearchCapable(s, actor)) return "BloodTreatmentWorkerUnavailable";

            var body = s.Actors.Single(x => x.Id == actor);
            if (s.WorldTraversals.Any(x => x.ActorId == actor) || Math.Max(Math.Abs(body.X - 3), Math.Abs(body.Y - 3)) > 1)
                return "BloodTreatmentEquipmentOutOfReach";
            var specimen = s.PortableEquipment.Single(x => x.Id == s.BloodSpecimen.LotId);
            var vessel = s.PortableEquipment.Single(x => x.Id == s.BloodSpecimen.VesselId);
            var supply = s.PortableEquipment.SingleOrDefault(x => x.Id == s.BloodSpecimen.SupplyLotId);
            if (!vessel.Open || supply == null || supply.ParentId != vessel.Id || specimen.ParentId != vessel.Id
                || !PortableEquipmentValidation.FitsAuthoredMember(s, vessel, specimen)
                || !PortableEquipmentValidation.FitsAuthoredMember(s, vessel, supply))
                return "BloodTreatmentContainerFitNotEstablished";
            return PortableEquipmentRules.Accessible(s, actor, specimen) && PortableEquipmentRules.Accessible(s, actor, supply)
                ? null : "BloodTreatmentEquipmentOutOfReach";
        }

        private string AssessBloodTreatment(Snapshot s, Command c)
        {
            if (c.Target != s.BloodSpecimen.LotId || c.Inventory.Amount != new RuleQuantity(1))
                return "BloodTreatmentRequiresBoundWholeSpecimen";
            if (!ConnectedExplorationObservation.StageOpen(s) || !IsOffCalendarActivity(s, c.Actor))
                return "BloodTreatmentStageClosed";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (!HarvestPreservationRules.TryProjectAt(s, c.Target,
                    s.RuleClock.AddSeconds(HarvestPreservationTreatmentValidation.WorkSeconds), out var atFinish)
                || atFinish.State == HarvestPreservationState.Spoiled)
                return "HarvestTreatmentCannotFinishBeforeSpoilage";
            string access = BloodTreatmentAccess(s, c.Actor);
            if (access != null) return access;
            if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
            if (s.Work.AvailableAmount(c.Target) != c.Inventory.Amount
                || s.Work.AvailableAmount(s.BloodSpecimen.SupplyLotId) != HarvestPreservationTreatmentValidation.SupplyAmount
                || s.PortableEquipment.Where(x => x.Id == s.BloodSpecimen.VesselId || x.Id == c.Target
                    || x.Id == s.BloodSpecimen.SupplyLotId).Any(x => PortableEquipmentRules.HasPendingClaim(s, x)))
                return "BloodTreatmentInputsUnavailable";
            return null;
        }

        private static void RetainBloodTreatmentPacking(Snapshot s)
        {
            var specimen = s.BloodSpecimen;
            const string worker = ConnectedBloodSpecimen.Worker;
            var mass = HarvestPreservationTreatmentValidation.SupplyAmount;
            var packing = new PortableEquipmentRecord(ConnectedBloodSpecimen.Packing, "TEST_ONLY.used-specimen-packing.v1",
                worker, worker, specimen.VesselId, PortablePlacement.Contained, PortableLinkKind.None, "",
                PortableMassBasis.Fixed, mass, mass);
            s.PortableEquipment = s.PortableEquipment.Where(x => x.Id != specimen.SupplyLotId).Append(packing).ToArray();
            PortableEquipmentRules.SynchronizeLinks(s);
        }

        private static bool BloodVesselAtWorkshop(PortableEquipmentRecord vessel)
            => vessel.Placement == PortablePlacement.Ground && vessel.GroundX == 3 && vessel.GroundY == 3;

        private static string BloodTacticalTransitionFailure(Snapshot s)
        {
            if (s.BloodSpecimen == null) return null;
            if (ActiveBloodTreatment(s) != null) return "HarvestTreatmentInterruptionUnsupported";
            return HasUnresolvedHarvestOpening(s)
                ? "HarvestPreservationOpenLifecycleTacticalUnsupported" : null;
        }

        private string BloodSpecimenHandlingFailure(Snapshot s, Command c)
        {
            var specimen = s.BloodSpecimen;
            if (specimen == null) return null;
            if (c.Target == specimen.LotId || c.Target == specimen.SupplyLotId || c.Target == ConnectedBloodSpecimen.Packing)
                return "BloodSpecimenRemainsInBoundVessel";
            if (c.Target != specimen.VesselId) return null;
            if (c.Actor != ConnectedBloodSpecimen.Worker || s.InventoryCombat)
                return "BloodSpecimenHandlingRequiresOrdinaryOwner";
            if (!ConnectedExplorationObservation.StageOpen(s) && s.LaterEncounter?.Entry == null)
                return "BloodSpecimenHandlingStageClosed";
            if (ActiveBloodTreatment(s) != null) return "HarvestTreatmentInputsInUse";

            var vessel = s.PortableEquipment.Single(x => x.Id == specimen.VesselId);
            if (c.Kind == CommandKind.OpenPortableContainer) {
                if (!HarvestPreservationRules.IsProtectedAt(s, specimen.LotId, s.RuleClock)) return null;
                return BloodVesselAtWorkshop(vessel) && ConnectedResearchWorkshopAvailable(s)
                    && !TargetInActiveRepair(s, specimen.ToolId) && ResearchCapable(s, c.Actor)
                    ? null : "CleanPreservationToolUnavailable";
            }
            if (c.Kind == CommandKind.ClosePortableContainer) return null;
            if (c.Kind == CommandKind.HandlePortableEquipment && !vessel.Open && c.Inventory != null
                && (c.Inventory.Handling == HandlingKind.Pickup || c.Inventory.Handling == HandlingKind.Drop)) return null;
            return "BloodSpecimenRequiresClosedVesselMovement";
        }

        /// <summary>Assess this exact accessible input without admitting manufacturing or booking its first phase.</summary>
        public (bool Eligible, string Code, RuleTime? CurrentAge, RuleTime? FirstPhaseAge) AssessRecipe4Specimen(
            Snapshot s, Authority authority, string actor, string lotId, int materialSet = 0, int extraVials = 0)
        {
            if (!connectedBloodSpecimen || s?.BloodSpecimen == null || s.ContentFingerprint != ContentFingerprint)
                return (false, "ConnectedBloodSpecimenNotSelected", null, null);
            if (authority == null || !authority.Controls(actor) || !authority.MayUseInventory(ConnectedBloodSpecimen.Worker))
                return (false, "InventoryNotAuthorized", null, null);
            if (string.IsNullOrEmpty(lotId) || !s.Work.Lots.Any(x => x.Id == lotId))
                return (false, "BloodSpecimenMissing", null, null);
            if (s.InventoryCombat) return (false, "BloodSpecimenWorkshopRequiresOrdinaryActivity", null, null);

            var command = new Command("assess.recipe4.specimen", actor, s.Revision, CommandKind.StartManufacturing,
                ManufacturingRules.Recipe4Id, materialSet, extraVials);
            string failure = AssessManufacturingStart(s, command, out var recipe, lotId);
            if (lotId != s.BloodSpecimen.LotId || recipe == null
                || !HarvestPreservationRules.TryProject(s, lotId, out var current)
                || !HarvestPreservationRules.TryProjectAt(s, lotId, s.RuleClock.AddSeconds(recipe.FirstPhase.Numerator), out var phase))
                return (false, failure ?? "BloodSpecimenBindingMismatch", null, null);
            return (failure == null, failure ?? "Eligible", current.UnprotectedAge, phase.UnprotectedAge);
        }

        private static string AssessBloodIngredient(Snapshot s, string actor, string lotId, ManufacturingRecipeDefinition recipe)
        {
            var specimen = s.BloodSpecimen;
            if (specimen == null || lotId != specimen.LotId || recipe.Id != ManufacturingRules.Recipe4Id
                || recipe.Components[3].Id != ConnectedBloodSpecimen.MaterialId)
                return "BloodSpecimenBindingMismatch";
            var lot = s.InventoryLots.SingleOrDefault(x => x.LotId == lotId);
            var item = s.PortableEquipment.SingleOrDefault(x => x.Id == lotId && x.LinkedId == lotId);
            var vessel = s.PortableEquipment.SingleOrDefault(x => x.Id == specimen.VesselId);
            if (lot == null || item == null || vessel == null || !HarvestPreservationRules.TryProject(s, lotId, out var current))
                return "BloodSpecimenMissing";
            if (current.State == HarvestPreservationState.Spoiled) return "ManufacturingIngredientSpoiled";
            if (s.Work.AvailableAmount(lotId) != new RuleQuantity(1) || PortableEquipmentRules.HasPendingClaim(s, item))
                return "ManufacturingIngredientsUnavailable";
            if (!vessel.Open || !BloodVesselAtWorkshop(vessel) || item.ParentId != vessel.Id
                || lot.OwnerId != actor || item.CustodianId != actor || !PortableEquipmentRules.Accessible(s, actor, item)
                || HarvestPreservationRules.IsProtectedAt(s, lotId, s.RuleClock))
                return "BloodSpecimenWorkshopAccessUnavailable";
            if (!s.HarvestPreservationTreatmentAttempts.Any(x => x.InventoryLotId == lotId
                    && x.Status == HarvestPreservationTreatmentStatus.Success))
                return "BloodSpecimenTreatmentRequired";
            return HarvestPreservationRules.TryProjectAt(s, lotId, s.RuleClock.AddSeconds(recipe.FirstPhase.Numerator), out var phase)
                && phase.State != HarvestPreservationState.Spoiled ? null : "BloodSpecimenSpoilsBeforeStabilization";
        }

        private IEnumerable<Command> DiscoverBloodTreatment(Snapshot s, Authority authority, string actor)
        {
            if (!connectedBloodSpecimen || actor != ConnectedBloodSpecimen.Worker || !authority.MayUseInventory(actor)) yield break;
            var command = new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".blood-treatment",
                actor, s.Revision, CommandKind.StartHarvestPreservationTreatment, s.BloodSpecimen.LotId,
                inventory: new InventoryRequest(new RuleQuantity(1)));
            if (ResolveCore(s, command, assessFormula: true) == null) yield return command;
        }
    }
}
#endif
