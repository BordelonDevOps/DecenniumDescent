#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const string ConnectedResearchMethod = "method.sequence-analysis";
        private bool connectedFormulaResearch;

        /// <summary>Selects the existing recipe-4 research and finite stock assessment on the connected expedition.</summary>
        public TestOnlySharedWorldPolicy EnableConnectedFormulaResearch()
            => SelectConnectedFormulaResearch(allowCraftingWitness: false);

        private TestOnlySharedWorldPolicy SelectConnectedFormulaResearch(bool allowCraftingWitness)
        {
            if (initializationStarted || connectedFormulaResearch || SelectedSchema != Snapshot.SurpriseEntrySchema
                || explorationSearchDefinition?.DirectorId != ConnectedExplorationObservation.SearchDirector
                || !ContentFingerprint.StartsWith(ConnectedExplorationObservation.FingerprintPrefix, StringComparison.Ordinal)
                || contentManifest != null || research != null || crafting != null && !allowCraftingWitness
                || repair != null || manufacturing != null)
                throw new InvalidOperationException("Select connected recipe-4 research once on the connected observation expedition before initialization.");

            // The manifest supplies the two local recipe bindings. It is not installed as world content.
            var authority = TestOnlyContentManifest.CreateSelectedProfile();
            var recipe = authority.ResolveSemantic("crafting", SharedResearchFixture.Recipe);
            if (authority.ValidateBindings() != null || !authority.Supports(recipe, ContentOperation.FormulaResearch)
                || !authority.Supports(recipe, ContentOperation.Manufacture))
                throw new InvalidOperationException("The existing recipe-4 authority is unavailable.");

            research = new SharedResearchFixture();
            crafting ??= new SharedCraftingFixture();
            manufacturing = new SharedManufacturingFixture();
            connectedFormulaResearch = true;
            ContentFingerprint = ConnectedExplorationObservation.FingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, "connected-formula-research-v1", recipe.Canonical, research.Key, crafting.Key, manufacturing.Key,
                SharedResearchFixture.Evidence, ConnectedResearchMethod, SharedCraftingFixture.StationId, SharedCraftingFixture.ToolId,
                "ordinary-workshop-3,3-radius1|returned-charter|finite-stock-assessment-only"));
            return this;
        }

        private string ConnectedResearchAdmission(Snapshot state, Command command)
        {
            if (command.Kind == CommandKind.StartFormulaCopy
                || command.Kind == CommandKind.StartFormulaResearch
                    && (command.X != 0 || command.Y != 0 || command.Target != SharedResearchFixture.Evidence))
                return "ConnectedFormulaOperationNotSelected";
            if (command.Kind != CommandKind.StartFormulaResearch && command.Kind != CommandKind.ResumeFormulaWork)
                return null;
            if (command.Actor != research.WorkerId) return "ResearchCredentialMissing";
            if (ResearchParticipantInCombat(state, command.Actor)) return "ResearchParticipantInCombat";
            return !state.InventoryCombat && IsOffCalendarActivity(state, command.Actor)
                && ConnectedExplorationObservation.StageOpen(state) ? null : "ConnectedResearchStageClosed";
        }

        private bool ConnectedResearchWorkshopAvailable(Snapshot state)
        {
            var tool = state.Structures.SingleOrDefault(x => x.Id == SharedCraftingFixture.ToolId);
            return tool != null && tool.ProfileId == "tools.alchemist-s-supplies" && !tool.Broken
                && tool.OwnerId == research.WorkerId && tool.CustodianId == research.WorkerId
                && tool.LocationId == SharedCraftingFixture.StationId
                && state.CropPlots.Any(x => x.Id == tool.LocationId && x.OwnerId == research.WorkerId)
                && !CraftingRestrictions.StationUseBlocked(state, SharedCraftingFixture.StationId);
        }

        private string AssessConnectedManufacturing(Snapshot state, Command command)
        {
            if (command.Kind != CommandKind.StartManufacturing) return "ConnectedManufacturingNotSelected";
            return AssessManufacturingStart(state, command, out _) ?? "ConnectedManufacturingNotSelected";
        }

        private IEnumerable<Command> DiscoverConnectedFormulaWork(Snapshot state, string actor)
        {
            if (!connectedFormulaResearch || actor != research.WorkerId) yield break;
            var job = state.FormulaWork.SingleOrDefault(x => FormulaOpen(x));
            string id = "option." + state.Revision.ToString(CultureInfo.InvariantCulture) + ".connected-research.";
            if (job == null) {
                var start = new Command(id + "start", actor, state.Revision, CommandKind.StartFormulaResearch, SharedResearchFixture.Evidence);
                if (ResolveCore(state, start, assessFormula: true) == null) yield return start;
                yield break;
            }
            var control = job.Status == FormulaWorkStatus.Working ? CommandKind.PauseFormulaWork : CommandKind.ResumeFormulaWork;
            var change = new Command(id + "control", actor, state.Revision, control, job.Id);
            if (ResolveCore(state, change, assessFormula: true) == null) yield return change;
            var cancel = new Command(id + "cancel", actor, state.Revision, CommandKind.CancelFormulaWork, job.Id);
            if (ResolveCore(state, cancel, assessFormula: true) == null) yield return cancel;
        }

        private string ValidateConnectedFormulaResearch(Snapshot state)
        {
            if (!connectedFormulaResearch) return null;
            if (connectedRecipe4Batch != (state.ConnectedBatch != null) || connectedCarriedVial != state.ConnectedCarriedVial
                || connectedStowedVial != state.ConnectedStowedVial
                || !connectedRecipe4Batch && (state.ManufacturingOrders.Length != 0 || state.AlchemyDoses.Length != 0
                    || state.ManufacturingAdvance != null) || state.FormulaWork.Count(FormulaOpen) > 1)
                return "ConnectedFormulaProfileMismatch";

            var returned = state.CharterAttempt?.Returned;
            var entered = state.LaterEncounter?.Entry;
            foreach (var job in state.FormulaWork) {
                if (job.WorkerId != research.WorkerId || job.Kind != FormulaWorkKind.Research || job.RecipeId != research.RecipeId
                    || job.EvidenceId != SharedResearchFixture.Evidence || job.MethodId != ConnectedResearchMethod
                    || job.Work.Required != FormulaResearchRules.RequiredTime(SharedResearchFixture.MinimumResearchHours(job.RecipeId))
                    || returned == null || job.StartedAt < returned.At || entered != null && job.StartedAt >= entered.Epoch.Origin
                    || job.Status == FormulaWorkStatus.Working && ResearchParticipantInCombat(state, job.WorkerId))
                    return "ConnectedFormulaProfileMismatch";

                var receipt = state.Receipts.SingleOrDefault(x => job.Id == "formula." + x.Revision.ToString(CultureInfo.InvariantCulture));
                if (receipt == null || receipt.Revision <= returned.Revision || entered != null && receipt.Revision >= entered.ArrivalRevision)
                    return "ConnectedFormulaStartMissing";
                var command = CommandHistory.Read(receipt);
                if (command.Kind != CommandKind.StartFormulaResearch || command.Actor != job.WorkerId || command.Target != job.EvidenceId
                    || command.X != 0 || command.Y != 0)
                    return "ConnectedFormulaStartMissing";

                var bookings = state.Work.WorkerIntervals.Where(x => x.JobId == job.Id).ToArray();
                if (bookings.Count(x => x.End > state.RuleClock) != (job.Status == FormulaWorkStatus.Working ? 1 : 0)
                    || bookings.Any(x => x.WorkerId != job.WorkerId || x.Start < job.StartedAt || x.Start > state.RuleClock
                        || !ResearchWindowEnd(x.Start).HasValue || x.End > ResearchWindowEnd(x.Start).Value))
                    return "ConnectedFormulaLaborMismatch";
                RuleTime labor = default;
                foreach (var booking in bookings) {
                    RuleTime end = booking.End < state.RuleClock ? booking.End : state.RuleClock;
                    labor = CampGreens.Add(labor, CampGreens.Subtract(end, booking.Start));
                }
                if (job.Work.Labor != labor || job.Work.Retained != labor)
                    return "ConnectedFormulaLaborMismatch";
            }
            return null;
        }
    }
}
#endif
