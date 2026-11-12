using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Wire94's one approved pre-owned specimen and its exact handoff authority.</summary>
    public sealed class ConnectedBloodSpecimen
    {
        public const string FingerprintPrefix = "TEST_ONLY.connected-blood-v1-";
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string StockAuthority = "TEST_ONLY.preowned-recipe14.set0.v1";
        public const string SpecimenId = "manufacture.recipe14.set0.component2";
        public const string MaterialId = "drop-black_blood_sample";
        public const string SourcePointer = "/recipes/13/components/2";
        public const string RecipePointer = "/recipes/3/components/3";
        public const string Worker = "TEST_ONLY.companion";
        public const string Vessel = "TEST_ONLY.preservation.sealable-vessel";
        public const string Fit = "TEST_ONLY.specimen-vessel-fit.v1";
        public const string Supply = "TEST_ONLY.preservation.supplies";
        public const string Packing = "TEST_ONLY.specimen.retained-packing";
        public const string Tool = "craft.alchemist-kit";
        public const string CleanTool = "TEST_ONLY.specimen.clean-alchemist-kit.v1";
        public const string MaterialProfile = "TEST_ONLY.black-blood-counted.v1";
        public const int Interval = 14400;
        public static readonly RuleQuantity Mass = new RuleQuantity(19, 50);

        public string AuthorityId { get; }
        public string LotId { get; }
        public string SourceOccurrence { get; }
        public string RecipeOccurrence { get; }
        public RuleTime Origin { get; }
        public int IntervalSeconds { get; }
        public RuleQuantity UnitMass { get; }
        public string VesselId { get; }
        public string FitId { get; }
        public string SupplyLotId { get; }
        public string ToolId { get; }
        public string CleanToolFactId { get; }

        public ConnectedBloodSpecimen(string authorityId, string lotId, string sourceOccurrence, string recipeOccurrence,
            RuleTime origin, int intervalSeconds, RuleQuantity unitMass, string vesselId, string fitId,
            string supplyLotId, string toolId, string cleanToolFactId)
        {
            if (authorityId != StockAuthority || lotId != SpecimenId || sourceOccurrence != SourcePointer
                || recipeOccurrence != RecipePointer || origin != default || intervalSeconds != Interval || unitMass != Mass
                || vesselId != Vessel || fitId != Fit || supplyLotId != Supply || toolId != Tool || cleanToolFactId != CleanTool)
                throw new ArgumentException("Invalid wire94 specimen origin or authority.");
            AuthorityId = authorityId;
            LotId = lotId;
            SourceOccurrence = sourceOccurrence;
            RecipeOccurrence = recipeOccurrence;
            Origin = origin;
            IntervalSeconds = intervalSeconds;
            UnitMass = unitMass;
            VesselId = vesselId;
            FitId = fitId;
            SupplyLotId = supplyLotId;
            ToolId = toolId;
            CleanToolFactId = cleanToolFactId;
        }

        public static ConnectedBloodSpecimen Selected()
            => new ConnectedBloodSpecimen(StockAuthority, SpecimenId, SourcePointer, RecipePointer, default, Interval, Mass,
                Vessel, Fit, Supply, Tool, CleanTool);

        internal static bool HasFingerprint(Snapshot s)
            => s.ContentFingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || ConnectedRecipe4Batch.IsSelected(s);

        internal static bool UsesAuthoredFit(Snapshot s, PortableEquipmentRecord item)
            => s.BloodSpecimen != null && item.Id == s.BloodSpecimen.LotId
                && item.ProfileId == MaterialProfile && item.ParentId == s.BloodSpecimen.VesselId
                && item.Placement == PortablePlacement.Contained;

        internal static void Validate(Snapshot s)
        {
            var specimen = s.BloodSpecimen;
            if ((specimen != null) != HasFingerprint(s))
                throw new ArgumentException("Wire94 requires its exact specimen composition.");
            if (specimen == null) return;
            if (s.SchemaVersion != Snapshot.SurpriseEntrySchema || !s.TestOnly || s.ExplorationSearch == null || s.ExplorationHide == null)
                throw new ArgumentException("Wire94 requires the connected observation base and both sections.");

            var resource = s.Work.Lots.SingleOrDefault(x => x.Id == specimen.LotId);
            var lot = s.InventoryLots.SingleOrDefault(x => x.LotId == specimen.LotId);
            var item = s.PortableEquipment.SingleOrDefault(x => x.Id == specimen.LotId);
            var vessel = s.PortableEquipment.SingleOrDefault(x => x.Id == specimen.VesselId);
            var storage = PortableStorageProfileValidation.Find(s, MaterialProfile);
            var batch = s.ConnectedBatch;
            bool inApparatus = batch?.UsesApparatus == true;
            var whole = new RuleQuantity(1);
            if (resource == null || resource.UnitId != MaterialId
                || resource.Amount != (batch?.Disposition == ConnectedSpecimenDisposition.Consumed ? default : whole)
                || resource.LocationId != (inApparatus ? batch.ApparatusId : specimen.VesselId)
                || resource.CustodianId != Worker || lot == null || lot.OwnerId != Worker || lot.ParentId != ""
                || lot.CreatedAt != specimen.Origin || lot.CreatedAmount != whole || lot.Nutrition != NutritionKind.None
                || lot.FreshUntil.HasValue || s.InventoryLots.Any(x => x.ParentId == specimen.LotId)
                || (inApparatus ? item != null || lot.Access != InventoryAccess.Stowed
                    : item == null || item.LinkKind != PortableLinkKind.InventoryLot || item.LinkedId != lot.LotId
                        || item.MassBasis != PortableMassBasis.CountedQuantity || item.ProfileId != MaterialProfile
                        || item.OwnerId != Worker || item.CustodianId != Worker || item.ParentId != specimen.VesselId
                        || item.Placement != PortablePlacement.Contained)
                || storage?.MassPerUnitLb != specimen.UnitMass
                || storage.QuantityUnitId != MaterialId || vessel == null || vessel.OwnerId != Worker || vessel.CustodianId != Worker
                || vessel.FitRuleId != specimen.FitId || vessel.FitMemberIds.Count != 3 || !vessel.FitMemberIds.Contains(specimen.LotId)
                || !vessel.FitMemberIds.Contains(specimen.SupplyLotId) || !vessel.FitMemberIds.Contains(Packing)
                || vessel.OperationalWeightLb != new RuleQuantity(1) || vessel.CapacityPounds != new RuleQuantity(10)
                || vessel.CapacityCubicFeet != new RuleQuantity(1) || s.HarvestUnits.Any(x => x.Id == lot.LotId))
                throw new ArgumentException("Invalid wire94 counted specimen, vessel, or origin linkage.");

            var supply = s.Work.Lots.SingleOrDefault(x => x.Id == specimen.SupplyLotId);
            var supplyItem = s.PortableEquipment.SingleOrDefault(x => x.Id == specimen.SupplyLotId);
            var packing = s.PortableEquipment.SingleOrDefault(x => x.Id == Packing);
            bool settled = s.HarvestPreservationTreatmentAttempts.Any(x => x.Status != HarvestPreservationTreatmentStatus.Working);
            var allotment = HarvestPreservationTreatmentValidation.SupplyAmount;
            if (supply == null || supply.UnitId != "mass-pound" || supply.CustodianId != Worker
                || supply.Amount != (settled ? default : allotment)
                || (settled ? supplyItem != null || packing == null || packing.ParentId != vessel.Id
                        || packing.Placement != PortablePlacement.Contained || packing.OperationalWeightLb != allotment
                    : packing != null || supplyItem == null || supplyItem.ParentId != vessel.Id
                        || supplyItem.LinkKind != PortableLinkKind.InventoryLot || supplyItem.LinkedId != specimen.SupplyLotId))
                throw new ArgumentException("Invalid wire94 preservation supplies or retained packing.");

            var treatment = s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x => x.Status == HarvestPreservationTreatmentStatus.Success);
            if (treatment == null) return;
            foreach (var opening in s.PortableHandling.Where(x => x.ItemId == specimen.VesselId && x.Operation == PortableOperation.Open
                && x.EndedAt >= treatment.CompletedAt.Value)) {
                if (HarvestPreservationRules.IsProtectedAtRevision(s, specimen.LotId, opening.EndedAt, opening.Revision - 1)
                    && !s.HarvestPreservationEvidence.Any(x => x.PortableHandlingId == opening.Id))
                    throw new ArgumentException("Wire94 protected opening lacks its actual clean-tool evidence.");
            }
        }
    }
}
