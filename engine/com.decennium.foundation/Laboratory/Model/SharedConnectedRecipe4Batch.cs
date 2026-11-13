#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedRecipe4Batch;
        private bool connectedRecipe4InjuryWitness;
        public const string Recipe4InjuryWitnessId = "TEST_ONLY.recipe4.injury-witness.acid";
        public static RuleTime Recipe4InjuryWitnessAt => new RuleTime(42248);

        public TestOnlySharedWorldPolicy EnableConnectedRecipe4InjuryWitness()
        {
            if (crafting?.CompanionHp != 1 || crafting.HeroHp != 26 || crafting.ToolHp != 5
                || crafting.HeroProficient || crafting.Events.Count != 1)
                throw new InvalidOperationException("Select the exact authored companion injury witness before initialization.");
            var occurrence = crafting.Events[0];
            if (occurrence.Id != Recipe4InjuryWitnessId || occurrence.At != Recipe4InjuryWitnessAt
                || occurrence.Result != 4 || occurrence.LeadId != ConnectedBloodSpecimen.Worker
                || occurrence.Participants.Count != 1 || occurrence.ToolId != SharedCraftingFixture.ToolId
                || occurrence.StationId != SharedCraftingFixture.StationId || occurrence.TradeId != SharedCraftingFixture.TradeId)
                throw new InvalidOperationException("The recipe-4 injury witness requires its exact authored acid occurrence.");
            SelectConnectedFormulaResearch(allowCraftingWitness: true).EnableConnectedBloodSpecimen().EnableConnectedRecipe4Batch();
            connectedRecipe4InjuryWitness = true;
            return this;
        }

        public TestOnlySharedWorldPolicy EnableConnectedRecipe4Batch()
        {
            if (initializationStarted || connectedRecipe4Batch || !connectedBloodSpecimen
                || !ContentFingerprint.StartsWith(ConnectedBloodSpecimen.FingerprintPrefix, StringComparison.Ordinal))
                throw new InvalidOperationException("Select the connected recipe-4 batch before initializing the specimen expedition.");
            connectedRecipe4Batch = true;
            ContentFingerprint = ConnectedRecipe4Batch.FingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, ConnectedRecipe4Batch.RecipeId, ConnectedRecipe4Batch.Apparatus,
                ConnectedRecipe4Batch.ApparatusProfile, ConnectedRecipe4Batch.Fit, ConnectedBloodSpecimen.SpecimenId,
                ConnectedBloodSpecimen.Vessel, "bench-3,3|set0|two-optional-vials|one-order|actual-closed-charge|native-settlement|native-dose"));
            return this;
        }

        private void InitializeConnectedRecipe4Batch(Snapshot s)
        {
            if (!connectedRecipe4Batch) return;
            s.ConnectedCarriedVial = connectedCarriedVial;
            s.ConnectedStowedVial = connectedStowedVial;
            s.ConnectedTacticalVial = connectedTacticalVial;
            s.ConnectedBatch = ConnectedRecipe4Batch.Selected();
            s.PortableEquipment = s.PortableEquipment.Append(new PortableEquipmentRecord(
                s.ConnectedBatch.ApparatusId, ConnectedRecipe4Batch.ApparatusProfile,
                ConnectedBloodSpecimen.Worker, ConnectedBloodSpecimen.Worker, "", PortablePlacement.Ground,
                PortableLinkKind.None, "", PortableMassBasis.Unmodeled, null, null, fitRuleId: s.ConnectedBatch.FitId,
                fitMemberIds: new[] { s.BloodSpecimen.LotId }, groundX: ConnectedRecipe4Batch.BenchX,
                groundY: ConnectedRecipe4Batch.BenchY)).ToArray();
        }

        private string AssessConnectedRecipe4Start(Snapshot s, Command c, out ManufacturingRecipeDefinition recipe)
        {
            recipe = null;
            if (c.Target != ConnectedRecipe4Batch.RecipeId || c.X != 0 || c.Y < 0 || c.Y > 2)
                return "ConnectedRecipe4RequestNotSelected";
            if (s.ConnectedBatch.Disposition != ConnectedSpecimenDisposition.Uncharged)
                return "ConnectedRecipe4BatchAlreadyDeclared";
            var apparatus = s.PortableEquipment.Single(x => x.Id == s.ConnectedBatch.ApparatusId);
            if (!ConnectedRecipe4Batch.OnBench(apparatus) || apparatus.Open || !PortableEquipmentRules.Accessible(s, c.Actor, apparatus))
                return "ConnectedRecipe4ApparatusUnavailable";
            return AssessManufacturingStart(s, c, out recipe, s.BloodSpecimen.LotId);
        }

        private bool IsConnectedRecipe4InjuryDispatch(Snapshot s, Command c)
            => connectedRecipe4InjuryWitness && c.Kind == CommandKind.DispatchCraftingMishap
                && c.Target == Recipe4InjuryWitnessId && c.Actor == ConnectedBloodSpecimen.Worker
                && s.ConnectedBatch?.Disposition == ConnectedSpecimenDisposition.Uncharged
                && !s.InventoryCombat && ConnectedExplorationObservation.StageOpen(s);

        private static bool IsConnectedRecipe4Check(Snapshot s, Command c)
            => s.ConnectedBatch != null && c.Kind == CommandKind.ResumeManufacturing
                && s.ManufacturingOrders.Any(x => x.Id == c.Target && x.WorkerId == c.Actor
                    && x.Status == ManufacturingStatus.AwaitingCheck);

        private static string ManufacturingLot(Snapshot s, string recipe, int set, int component)
            => s.ConnectedBatch != null && recipe == ConnectedRecipe4Batch.RecipeId && set == 0 && component == 3
                ? s.BloodSpecimen.LotId : SharedManufacturingFixture.Lot(recipe, set, component);

        private static void MoveBatchSpecimen(Snapshot s, string destination)
        {
            s.Work = new WorkLedger(s.Work.Lots.Select(x => x.Id == s.BloodSpecimen.LotId
                ? new ResourceLot(x.Id, x.UnitId, x.Amount, destination, x.CustodianId) : x),
                s.Work.WorkerIntervals, s.Work.Reservations);
        }

        private static void ChargeConnectedRecipe4(Snapshot s, ManufacturingOrderRecord order)
        {
            if (s.ConnectedBatch == null) return;
            MoveBatchSpecimen(s, s.ConnectedBatch.ApparatusId);
            s.PortableEquipment = s.PortableEquipment.Where(x => x.Id != s.BloodSpecimen.LotId).ToArray();
            s.ConnectedBatch = s.ConnectedBatch.Charge(order.Id, s.Revision + 1);
        }

        private static void SettleConnectedRecipe4(Snapshot s, ManufacturingOrderRecord order)
        {
            if (s.ConnectedBatch == null) return;
            var specimen = s.BloodSpecimen;
            var claim = s.Work.Reservations.Single(x => x.JobId == order.Id && x.Id == ComponentClaim(order, 3));
            bool returned = claim.ReleasedAmount == new RuleQuantity(1);
            if (returned) {
                MoveBatchSpecimen(s, s.ConnectedBatch.ReturnVesselId);
                s.PortableEquipment = s.PortableEquipment.Append(new PortableEquipmentRecord(specimen.LotId,
                    ConnectedBloodSpecimen.MaterialProfile, ConnectedBloodSpecimen.Worker, ConnectedBloodSpecimen.Worker,
                    s.ConnectedBatch.ReturnVesselId, PortablePlacement.Contained, PortableLinkKind.InventoryLot,
                    specimen.LotId, PortableMassBasis.CountedQuantity, null, null)).ToArray();
            }
            s.ConnectedBatch = s.ConnectedBatch.Settle(s.Revision + 1, returned);
        }

        private static string ConnectedRecipe4HandlingFailure(Snapshot s, Command c)
        {
            var batch = s.ConnectedBatch;
            if (batch == null) return null;
            if (c.Target == batch.ApparatusId || c.Inventory?.Destination == batch.ApparatusId)
                return "ConnectedRecipe4ApparatusIsFixed";
            return batch.Disposition == ConnectedSpecimenDisposition.Charged
                && (c.Target == batch.ReturnVesselId || c.Inventory?.Destination == batch.ReturnVesselId)
                ? "ConnectedRecipe4ReturnVesselClaimed" : null;
        }

        private IEnumerable<Command> DiscoverConnectedRecipe4(Snapshot s, string actor)
        {
            if (s.ConnectedBatch == null) yield break;
            string id = "option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".recipe4.";
            if (actor == ConnectedBloodSpecimen.Worker && s.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Uncharged) {
                for (int vials = 0; vials <= 2; vials++) {
                    var command = new Command(id + "start." + vials.ToString(CultureInfo.InvariantCulture), actor, s.Revision,
                        CommandKind.StartManufacturing, ConnectedRecipe4Batch.RecipeId, y: vials);
                    if (ResolveCore(s, command, assessFormula: true) == null) yield return command;
                }
            }
            if (!s.InventoryCombat || s.Encounter.CurrentActor != actor) yield break;
            foreach (var dose in s.AlchemyDoses.Where(x => !x.Spent))
                foreach (var recipient in s.Actors) {
                    var command = new Command(id + dose.Id + "." + recipient.Id, actor, s.Revision,
                        CommandKind.UseAlchemyDose, dose.Id, inventory: new InventoryRequest(new RuleQuantity(1), recipient.Id));
                    if (ResolveCore(s, command, assessFormula: true) == null) yield return command;
                }
        }

        private IReadOnlyList<CommandCost> ConnectedRecipe4Costs(Snapshot s, Command c)
        {
            if (c.Kind == CommandKind.UseAlchemyDose)
                return new[] { new CommandCost("action", "", 1), new CommandCost("inventory", c.Target, 1) };
            if (c.Kind != CommandKind.StartManufacturing) return Array.Empty<CommandCost>();
            var recipe = ManufacturingRules.Recipe(ConnectedRecipe4Batch.RecipeId);
            var costs = recipe.Components.Select((component, i) => new CommandCost("reserve-lot",
                ManufacturingLot(s, recipe.Id, 0, i), component.Quantity)).ToList();
            if (c.Y > 0) costs.Add(new CommandCost("reserve-lot", SharedManufacturingFixture.Packaging, c.Y));
            costs.Add(new CommandCost("work-seconds", "", recipe.FirstPhase.Numerator + recipe.RemainingPhase.Numerator));
            return costs;
        }

        private static string ValidateConnectedRecipe4Settlement(Snapshot s)
        {
            var batch = s.ConnectedBatch;
            if (batch == null) return null;
            var order = s.ManufacturingOrders.SingleOrDefault();
            if (s.ManufacturingAdvance != null && order?.Status != ManufacturingStatus.AwaitingChoice)
                return "ConnectedRecipe4ContinuationMismatch";
            if (order == null) return null;
            var returned = s.CharterAttempt?.Returned;
            var encounter = s.LaterEncounter?.Entry;
            if (returned == null || batch.ChargeRevision <= returned.Revision || order.StartedAt < returned.At
                || encounter != null && (batch.ChargeRevision >= encounter.ArrivalRevision
                    || batch.SettlementRevision >= encounter.ArrivalRevision))
                return "ConnectedRecipe4WorkStageMismatch";

            bool complete = order.Status == ManufacturingStatus.Complete;
            bool choice = order.Status == ManufacturingStatus.AwaitingChoice;
            bool check = complete || choice;
            if (check && !order.Work.Complete || !check && order.Quality != CraftQuality.None
                || choice && order.Quality < CraftQuality.Exceptional
                || complete && (order.Quality == CraftQuality.None
                    || (order.Quality == CraftQuality.Mishap) != (order.Mishap > 0)))
                return "ConnectedRecipe4CheckMismatch";
            if (order.Mishap > 0 && !s.CraftingIncidents.Any(x => x.Id == order.MishapIncidentId
                && x.Result == order.Mishap && x.LeadId == order.WorkerId))
                return "ConnectedRecipe4MishapMismatch";

            var recipe = ManufacturingRules.Recipe(order.RecipeId);
            if (complete && (order.Quality >= CraftQuality.Exceptional
                    ? order.Choice == CraftQualityChoice.StandardQuantity
                    : order.Choice != CraftQualityChoice.StandardQuantity)
                || complete && (order.Quality == CraftQuality.Masterwork
                    ? !recipe.CatalystIndexes.Contains(order.RetainedCatalyst)
                    : order.RetainedCatalyst != -1))
                return "ConnectedRecipe4QualityMismatch";
            var (doseCount, hp, extra) = complete ? ManufacturingOutput(recipe, order.Quality, order.Choice) : (0, 1, 0);
            bool abandoned = order.Status == ManufacturingStatus.Cancelled && order.Work.Labor != default;
            bool CheckSettlement(ResourceReservation claim, RuleQuantity consumed)
                => claim.ConsumedAmount == consumed && claim.ReleasedAmount == (order.Open ? default : claim.Amount - consumed);
            for (int i = 0; i < recipe.Components.Count; i++) {
                var claim = s.Work.Reservations.Single(x => x.JobId == order.Id && x.Id == ComponentClaim(order, i));
                var expected = complete ? ManufacturingComponentConsumption(recipe, order.Quality, order.RetainedCatalyst, i)
                    : abandoned ? claim.Amount : default;
                if (!CheckSettlement(claim, expected)) return "ConnectedRecipe4InputSettlementMismatch";
            }
            if (order.ExtraVials > 0) {
                var packaging = s.Work.Reservations.Single(x => x.JobId == order.Id && x.Id == order.Id + ".packaging");
                if (!CheckSettlement(packaging, new RuleQuantity(extra))) return "ConnectedRecipe4PackagingSettlementMismatch";
            }
            if (extra > order.ExtraVials || s.AlchemyDoses.Length != doseCount) return "ConnectedRecipe4OutputCountMismatch";
            for (int i = 0; i < doseCount; i++) {
                string id = order.Id + ".dose" + i.ToString(CultureInfo.InvariantCulture);
                var dose = s.AlchemyDoses.SingleOrDefault(x => x.Id == id);
                if (dose == null || id != ConnectedVialRules.SelectedId(s) && dose.LocationId != SharedCraftingFixture.StationId
                    || dose.MaximumHp != hp || dose.Hp != hp)
                    return "ConnectedRecipe4OutputCustodyMismatch";
            }
            return null;
        }
    }
}
#endif
