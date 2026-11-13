#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedCarriedVial;
        private bool connectedStowedVial;
        private bool connectedTacticalVial;
        private bool connectedCompanionDose;

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

        internal TestOnlySharedWorldPolicy EnableConnectedStowedVial()
        {
            EnableConnectedCarriedVial();
            var manifest = TestOnlyContentManifest.CreateSelectedProfile();
            var pack = manifest.ResolveSemantic("equipment", "adventuring-gear.backpack");
            if (manifest.ValidateBindings() != null || !manifest.Supports(pack, ContentOperation.PortableEquipment)
                || !manifest.Supports(pack, ContentOperation.PortableInteraction))
                throw new InvalidOperationException("The selected vial pack has no supported equipment binding.");
            connectedStowedVial = true;
            ContentFingerprint = ConnectedVialRules.StowFingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, pack.Canonical, ConnectedVialRules.PackId, "exact-dose-zero-fit|direct-contained|one-second"));
            return this;
        }

        internal TestOnlySharedWorldPolicy EnableConnectedTacticalVial()
        {
            EnableConnectedStowedVial();
            connectedTacticalVial = true;
            ContentFingerprint = ConnectedVialRules.TacticalFingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, "later-encounter|open-pack|retrieve|shared-interaction"));
            return this;
        }

        internal TestOnlySharedWorldPolicy EnableConnectedCompanionDose()
        {
            EnableConnectedTacticalVial();
            connectedCompanionDose = true;
            ContentFingerprint = ConnectedVialRules.CompanionFingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, ConnectedVialRules.CompanionRecipientId,
                "willing-for-hero-recipe4|can-swallow-while-conscious|reinforced-companion"));
            return this;
        }

        private static string CompanionDoseDeliveryFailure(Snapshot state, ActorState user, ActorState recipient)
        {
            var reinforcement = state.Reinforcement;
            if (!state.ConnectedCompanionDose || user.Id != ConnectedVialRules.CarrierId
                || recipient?.Id != ConnectedVialRules.CompanionRecipientId
                || reinforcement?.Admission == null || reinforcement.Definition.CompanionId != recipient.Id
                || state.Encounter.Id != reinforcement.Definition.EncounterId
                || !state.Encounter.Order.Contains(recipient.Id)
                || !SoldierTacticalFeatures.IsAlly(state, user.Id, recipient.Id))
                return "CompanionDoseRecipientUnavailable";
            if (PlanarCombatGeometry.DistanceFeet(new CombatCell(user.X, user.Y), new CombatCell(recipient.X, recipient.Y)) > 5)
                return "AlchemyRecipientOutOfReach";
            if (!ObservationGeometry.LineOfEffectClear(state, user.Id, recipient.Id))
                return "CompanionDoseDeliveryBlocked";
            var life = state.Lives.Single(x => x.ActorId == recipient.Id);
            var conditions = View(state, recipient.Id);
            if (life.Dead || life.Hp == 0 || conditions.Unaware || conditions.Has(ConditionKind.Paralyzed))
                return "AlchemyRecipientCannotIngest";
            if (state.PeriodicRiders.Any(x => x.TargetId == recipient.Id && x.Present))
                return "CompanionDoseEndpointUnsupported";
            return null;
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
