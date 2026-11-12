#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        /// <summary>Selects ordinary Hide and Search for the finite Warned connected expedition.</summary>
        public TestOnlySharedWorldPolicy EnableConnectedExplorationObservation()
        {
            if (initializationStarted || SelectedSchema != Snapshot.SurpriseEntrySchema
                || surpriseEntryBinding?.Outcome != SurpriseAwareness.Warned || observationFixture != null
                || explorationSearchDefinition != null || explorationHideDefinition != null
                || nextCharterPlanProfile?.Key != new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true).Key
                || havenSaleProfile?.Key != new TestOnlyHavenSaleProfile().Key
                || charterAttemptProfile?.Key != new TestOnlyCharterAttemptProfile().Key || TestOnlyPolicy.Walkable(2, 1))
                throw new InvalidOperationException("Select connected ordinary observation on the Warned carried-reserve expedition before initialization.");

            var participants = new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id,
                TestOnlyHavenSaleProfile.BuyerId, LaterDefenderId };
            EnableObservation(new ObservationFixture(5, 5,
                new[] { new ObservationGridCell(2, 1, blocksSight: true, blocksEffect: false, blocksMovement: false) },
                participants.Select(x => new ObservationSightProfile(x, 30, 30))));

            var search = new ExplorationSearchDefinition(ExplorationSearchDefinition.Source, ConnectedExplorationObservation.SearchDirector,
                ConnectedExplorationObservation.VisibleFringe, TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId,
                new ExplorationSearchCell(3, 2), new ExplorationSearchCell(1, 0), new ExplorationSearchCell(3, 1),
                new ExplorationSearchCell(2, 1));
            var hide = new ExplorationHideDefinition(search.SourceRevision, ConnectedExplorationObservation.HideDirector,
                TestOnlyPolicy.ActorId, TestOnlyHavenSaleProfile.BuyerId, search.CueCandidate, new ExplorationSearchCell(2, 0));
            explorationSearchDefinition = search;
            explorationHideDefinition = hide;
            ContentFingerprint = ConnectedExplorationObservation.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                search.SourceRevision, search.DirectorId, search.CueId, search.SearcherId, search.ConcealedActorId, search.Anchor,
                search.CueCandidate, search.Sign, search.Occlusion, hide.DirectorId, hide.WitnessId, hide.Alternate,
                "returned-charter-before-later-entry|existing-personal-and-off-calendar-actions|receipt-ordered-boundary"));
            return this;
        }

        private static bool ConnectedObservationStageClosed(Snapshot state)
            => ConnectedExplorationObservation.IsSelected(state) && !ConnectedExplorationObservation.StageOpen(state);
    }
}
#endif
