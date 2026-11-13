#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ExpeditionManufacturingQualityAlternative
    {
        public CraftQualityChoice Choice { get; }
        public int DoseCount { get; }
        public int VialStructuralHp { get; }
        public int VialMaximumStructuralHp => VialStructuralHp;
        public RuleQuantity SupplementaryVialsConsumed { get; }
        public RuleQuantity SupplementaryVialsReleased { get; }

        internal ExpeditionManufacturingQualityAlternative(CraftQualityChoice choice, int doseCount, int vialHp,
            RuleQuantity consumed, RuleQuantity released)
        {
            Choice = choice;
            DoseCount = doseCount;
            VialStructuralHp = vialHp;
            SupplementaryVialsConsumed = consumed;
            SupplementaryVialsReleased = released;
        }
    }

    public sealed class ExpeditionManufacturingQualityExplanation
    {
        public long Revision { get; }
        public string DecisionId { get; }
        public string WorkerId { get; }
        public string RecipeId { get; }
        public CraftQuality Quality { get; }
        public bool TestOnly => true;
        public string RecipeSourceRevision { get; }
        public string RecipeSourceBlobId { get; }
        public string RecipeSourcePointer { get; }
        public string ReviewedPublicRecipeReference => TestOnlyContentManifest.Recipe4PublicReference;
        public string HealingEffect => "Ordinary magical nonspell healing: 2d4+2, subject to the recipient's caps and blockers. Quality does not increase potency.";
        public IReadOnlyList<ExpeditionManufacturingQualityAlternative> Alternatives { get; }

        internal ExpeditionManufacturingQualityExplanation(long revision, ManufacturingOrderRecord order,
            ContentDefinitionBinding source, IEnumerable<ExpeditionManufacturingQualityAlternative> alternatives)
        {
            Revision = revision;
            DecisionId = order.Id;
            WorkerId = order.WorkerId;
            RecipeId = source.SemanticId;
            Quality = order.Quality;
            RecipeSourceRevision = source.SourceRevision;
            RecipeSourceBlobId = source.SourceBlobId;
            RecipeSourcePointer = source.JsonPointer;
            Alternatives = Array.AsReadOnly(alternatives.ToArray());
        }
    }

    public sealed partial class ConnectedExpeditionSession
    {
        private static readonly TestOnlyContentManifest QualitySource = TestOnlyContentManifest.CreateSelectedProfile();
        private static readonly CraftQualityChoice[] ExplainedChoices = { CraftQualityChoice.FullYield, CraftQualityChoice.Durability };

        /// <summary>Describes the authorized current Exceptional recipe-4 choice, or returns null.
        /// The explanation is advisory and does not reserve or authorize a command.</summary>
        public ExpeditionManufacturingQualityExplanation ExplainManufacturingQuality(
            ExpeditionSeat seat, long expectedRevision, string decisionId)
        {
            lock (gate) {
                if (seat != ExpeditionSeat.Player || !Validation.ValidId(decisionId)) return null;
                var grant = SeatGrant(seat);
                if (grant == null) return null;
                var state = simulation.Capture();
                var order = OwnedQualityOrder(state, grant, expectedRevision, decisionId);
                if (order == null) return null;
                var source = QualitySource.ResolveSemantic("crafting", order.RecipeId);
                if (source == null || source.Visibility != ContentVisibility.Public
                    || source.ViewerAccess != ContentViewerAccess.RequiresExistingKnowledge
                    || !QualitySource.Supports(source, ContentOperation.Manufacture)
                    || !QualitySource.Supports(source, ContentOperation.UseProducedItem)) return null;

                var alternatives = new List<ExpeditionManufacturingQualityAlternative>(ExplainedChoices.Length);
                // The ordinary query preflight requires an unused command ID. This temporary
                // identity is never committed or returned and cannot collide with a prior receipt.
                string probeId = "quality.explanation";
                for (int suffix = 0; state.Receipts.Any(x => x.Principal == grant.Principal && x.Id == probeId); suffix++)
                    probeId = "quality.explanation." + (suffix + 1).ToString(System.Globalization.CultureInfo.InvariantCulture);
                foreach (var choice in ExplainedChoices) {
                    var probe = new Command(probeId, order.WorkerId, state.Revision,
                        CommandKind.ResolveManufacturingQuality, order.Id, x: (int)choice);
                    if (simulation.QueryCommand(grant, probe).Admissible)
                        alternatives.Add(TestOnlySharedWorldPolicy.DescribeManufacturingOutput(state, order, choice));
                }
                return alternatives.Count == 0 ? null
                    : new ExpeditionManufacturingQualityExplanation(state.Revision, order, source, alternatives);
            }
        }

        private static ManufacturingOrderRecord OwnedQualityOrder(Snapshot state, Authority grant,
            long expectedRevision, string decisionId)
        {
            if (state.Revision != expectedRevision || state.ConnectedBatch?.OrderId != decisionId) return null;
            string worker = ActingActor(state, out var kind, out var currentDecisionId);
            if (kind != ExpeditionDecisionKind.ManufacturingQuality || currentDecisionId != decisionId
                || !grant.Controls(worker) || !grant.MayUseInventory(worker)) return null;
            var order = state.ManufacturingOrders.SingleOrDefault(x => x.Id == decisionId && x.WorkerId == worker);
            return order != null && order.RecipeId == Recipe && order.Quality == CraftQuality.Exceptional
                && FormulaResearchRules.Knows(state, worker, order.RecipeId) ? order : null;
        }
    }
}
#endif
