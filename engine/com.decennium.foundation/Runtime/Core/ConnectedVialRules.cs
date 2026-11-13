using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Physical identity for the single selected recipe-4 vial. The portable root
    /// owns placement and custody. The dose owns manufacture, contents, use and structural HP.</summary>
    public static class ConnectedVialRules
    {
        public const byte Marker = 1;
        public const string FingerprintPrefix = "TEST_ONLY.carried-vial-v1-";
        public const string ProfileId = "TEST_ONLY.recipe4.finished-vial.v1";
        public const string CarrierId = "TEST_ONLY.actor";

        public static string SelectedId(Snapshot state)
            => state.ConnectedCarriedVial && state.ConnectedBatch?.OrderId is string id && id.Length != 0
                ? id + ".dose0" : null;

        public static string Location(PortableEquipmentRecord item)
            => item.Placement == PortablePlacement.Carried
                ? item.CustodianId : PortableEquipmentValidation.GroundLocation(item);

        public static void Validate(Snapshot state)
        {
            var linked = state.PortableEquipment.Where(x => x.LinkKind == PortableLinkKind.AlchemyDose || x.ProfileId == ProfileId).ToArray();
            bool selectedFingerprint = state.ContentFingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal);
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
            if (id == null || dose == null || item.Id != id || item.LinkedId != id || item.ProfileId != ProfileId
                || item.MassBasis != PortableMassBasis.AlchemyDose || item.ParentId != "" || item.Wearable || item.Open
                || item.CapacityPounds.HasValue || item.FitRuleId != "" || item.SourceWeightLb.HasValue || item.PrintedLoad.HasValue
                || (!carried && item.Placement != PortablePlacement.Ground) || item.HeldHands != (carried ? 1 : 0)
                || dose.RecipeId != ConnectedRecipe4Batch.RecipeId || dose.OrderId != state.ConnectedBatch.OrderId
                || (carried && item.CustodianId != CarrierId)
                || (dose.Spent && (dose.UserId != CarrierId || dose.RecipientId != CarrierId
                    || dose.FirstD4 < 1 || dose.SecondD4 < 1))
                || item.OwnerId != dose.OwnerId || item.CustodianId != dose.CustodianId || dose.LocationId != Location(item)
                || state.Work.Lots.Any(x => x.Id == id) || state.InventoryLots.Any(x => x.LotId == id))
                throw new ArgumentException("Invalid carried vial link or physical state.");
        }
    }
}
