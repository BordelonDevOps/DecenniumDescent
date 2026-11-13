#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedCarriedVial;

        public TestOnlySharedWorldPolicy EnableConnectedCarriedVial()
        {
            if (initializationStarted || !connectedRecipe4Batch || connectedCarriedVial
                || !ContentFingerprint.StartsWith(ConnectedRecipe4Batch.FingerprintPrefix, StringComparison.Ordinal))
                throw new InvalidOperationException("Select the carried vial before initializing the connected batch.");
            var manifest = TestOnlyContentManifest.CreateSelectedProfile();
            var recipe = manifest.ResolveSemantic("crafting", ConnectedRecipe4Batch.RecipeId);
            if (manifest.ValidateBindings() != null || !manifest.Supports(recipe, ContentOperation.Manufacture)
                || !manifest.Supports(recipe, ContentOperation.UseProducedItem))
                throw new InvalidOperationException("The selected carried dose has no supported recipe binding.");
            connectedCarriedVial = true;
            ContentFingerprint = ConnectedVialRules.FingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, recipe.Canonical, ConnectedVialRules.ProfileId, "first-dose|hero-held|pickup|self-use"));
            return this;
        }

        private static void RegisterConnectedVial(Snapshot s)
        {
            string id = ConnectedVialRules.SelectedId(s);
            var dose = s.AlchemyDoses.SingleOrDefault(x => x.Id == id);
            if (dose == null) return;
            var body = new PortableEquipmentRecord(id, ConnectedVialRules.ProfileId, dose.OwnerId, dose.CustodianId, "",
                PortablePlacement.Ground, PortableLinkKind.AlchemyDose, id, PortableMassBasis.AlchemyDose, null, null,
                groundX: ConnectedRecipe4Batch.BenchX, groundY: ConnectedRecipe4Batch.BenchY);
            s.PortableEquipment = s.PortableEquipment.Append(body).ToArray();
            SynchronizeConnectedVial(s, body);
        }

        internal static void SynchronizeConnectedVial(Snapshot s, PortableEquipmentRecord body)
        {
            s.AlchemyDoses = s.AlchemyDoses.Select(x => x.Id == body.LinkedId
                ? x.WithPlacement(body.CustodianId, ConnectedVialRules.Location(body)) : x).ToArray();
        }

        internal static void DropConnectedVial(Snapshot s, ActorState carrier)
        {
            if (!s.ConnectedCarriedVial) return;
            var vial = s.PortableEquipment.SingleOrDefault(x => x.LinkKind == PortableLinkKind.AlchemyDose
                && x.Placement == PortablePlacement.Carried && x.CustodianId == carrier.Id && x.HeldHands == 1);
            if (vial == null) return;
            var dropped = vial.With(placement: PortablePlacement.Ground, groundX: carrier.X, groundY: carrier.Y, heldHands: 0);
            SetPortable(s, dropped);
            SynchronizeConnectedVial(s, dropped);
        }

        private static bool ConnectedVialIsHeldBy(Snapshot s, string id, string actor)
            => actor == ConnectedVialRules.CarrierId && s.PortableEquipment.Any(x => x.Id == id
                && x.LinkKind == PortableLinkKind.AlchemyDose && x.ParentId == "" && x.CustodianId == actor
                && x.Placement == PortablePlacement.Carried && x.HeldHands == 1);
    }
}
#endif
