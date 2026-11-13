using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Physical identity for the single selected recipe-4 vial. The portable record
    /// owns placement and custody. The dose owns manufacture, contents, use and structural HP.</summary>
    public static class ConnectedVialRules
    {
        public const byte Marker = 1;
        public const byte StowMarker = 2;
        public const byte TacticalMarker = 3;
        public const byte CompanionMarker = 4;
        public const byte StabilizationMarker = 5;
        public const string FingerprintPrefix = "TEST_ONLY.carried-vial-v1-";
        public const string StowFingerprintPrefix = "TEST_ONLY.stowed-vial-v1-";
        public const string TacticalFingerprintPrefix = "TEST_ONLY.tactical-vial-v1-";
        public const string CompanionFingerprintPrefix = "TEST_ONLY.companion-dose-v1-";
        public const string StabilizationFingerprintPrefix = "TEST_ONLY.companion-stable-v1-";
        public const string ProfileId = "TEST_ONLY.recipe4.finished-vial.v1";
        public const string CarrierId = "TEST_ONLY.actor";
        public const string CompanionRecipientId = "TEST_ONLY.companion";
        public const string PackId = "TEST_ONLY.explorer-pack";

        public static string SelectedId(Snapshot state)
            => state.ConnectedCarriedVial && state.ConnectedBatch?.OrderId is string id && id.Length != 0
                ? id + ".dose0" : null;

        public static string Location(PortableEquipmentRecord item)
            => item.ParentId != "" ? item.ParentId : item.Placement == PortablePlacement.Carried
                ? item.CustodianId : PortableEquipmentValidation.GroundLocation(item);

        private static bool SelectedPack(PortableEquipmentRecord pack)
            => pack != null && pack.Id == PackId && pack.ProfileId == "adventuring-gear.backpack"
                && pack.OwnerId == CarrierId && pack.CustodianId == CarrierId && pack.ParentId == ""
                && pack.Placement == PortablePlacement.Worn && pack.CapacityPounds == new RuleQuantity(30)
                && pack.CapacityCubicFeet == new RuleQuantity(1) && pack.FitRuleId == "TEST_ONLY.explorer-pack-fit-v1";

        internal static bool FitsPack(Snapshot state, PortableEquipmentRecord pack, PortableEquipmentRecord item)
            => state.ConnectedStowedVial && SelectedPack(pack) && item.LinkKind == PortableLinkKind.AlchemyDose
                && item.Id == SelectedId(state) && item.LinkedId == item.Id && item.ProfileId == ProfileId;

        public static void Validate(Snapshot state)
        {
            var linked = state.PortableEquipment.Where(x => x.LinkKind == PortableLinkKind.AlchemyDose || x.ProfileId == ProfileId).ToArray();
            bool stowFingerprint = state.ContentFingerprint.StartsWith(StowFingerprintPrefix, StringComparison.Ordinal);
            bool tacticalFingerprint = state.ContentFingerprint.StartsWith(TacticalFingerprintPrefix, StringComparison.Ordinal);
            bool stabilizationFingerprint = state.ContentFingerprint.StartsWith(StabilizationFingerprintPrefix, StringComparison.Ordinal)
                || WoundTreatmentStation.SelectedFingerprint(state.ContentFingerprint);
            bool companionFingerprint = stabilizationFingerprint || state.ContentFingerprint.StartsWith(CompanionFingerprintPrefix, StringComparison.Ordinal);
            bool selectedFingerprint = state.ContentFingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
                || stowFingerprint || tacticalFingerprint || companionFingerprint;
            if (stabilizationFingerprint != state.ConnectedCompanionStabilization || companionFingerprint != state.ConnectedCompanionDose
                || (tacticalFingerprint || companionFingerprint) != state.ConnectedTacticalVial
                || (stowFingerprint || tacticalFingerprint || companionFingerprint) != state.ConnectedStowedVial
                || state.ConnectedStowedVial && !state.ConnectedCarriedVial)
                throw new ArgumentException("Stowed vial requires its selected envelope.");
            if (!state.ConnectedCarriedVial) {
                if (linked.Length != 0 || selectedFingerprint) throw new ArgumentException("Carried vial requires its selected envelope.");
                return;
            }
            if (!state.TestOnly || state.SchemaVersion != Snapshot.SurpriseEntrySchema || !selectedFingerprint
                || state.ConnectedBatch == null || state.FishingTraps.Length != 0)
                throw new ArgumentException("Invalid carried vial composition.");
            string id = SelectedId(state);
            var dose = state.AlchemyDoses.SingleOrDefault(x => x.Id == id);
            if (dose == null ? linked.Length != 0 : linked.Length != 1 || linked[0].Id != id)
                throw new ArgumentException("Carried vial must have one physical body for the produced dose.");
        }

        public static void ValidateLink(Snapshot state, PortableEquipmentRecord item)
        {
            string id = SelectedId(state);
            var dose = state.AlchemyDoses.SingleOrDefault(x => x.Id == id);
            bool carried = item.Placement == PortablePlacement.Carried;
            bool contained = item.Placement == PortablePlacement.Contained
                && FitsPack(state, state.PortableEquipment.SingleOrDefault(x => x.Id == item.ParentId), item);
            if (id == null || dose == null || item.Id != id || item.LinkedId != id || item.ProfileId != ProfileId
                || item.MassBasis != PortableMassBasis.AlchemyDose || (!contained && item.ParentId != "") || item.Wearable || item.Open
                || item.CapacityPounds.HasValue || item.FitRuleId != "" || item.SourceWeightLb.HasValue || item.PrintedLoad.HasValue
                || (!carried && !contained && item.Placement != PortablePlacement.Ground) || item.HeldHands != (carried ? 1 : 0)
                || dose.RecipeId != ConnectedRecipe4Batch.RecipeId || dose.OrderId != state.ConnectedBatch.OrderId
                || ((carried || contained) && item.CustodianId != CarrierId)
                || (dose.Spent && (dose.UserId != CarrierId
                    || (dose.RecipientId != CarrierId
                        && (!state.ConnectedCompanionDose || dose.RecipientId != CompanionRecipientId))
                    || dose.FirstD4 < 1 || dose.SecondD4 < 1))
                || item.OwnerId != dose.OwnerId || item.CustodianId != dose.CustodianId || dose.LocationId != Location(item)
                || state.Work.Lots.Any(x => x.Id == id) || state.InventoryLots.Any(x => x.LotId == id))
                throw new ArgumentException("Invalid carried vial link or physical state.");
        }
    }
}
