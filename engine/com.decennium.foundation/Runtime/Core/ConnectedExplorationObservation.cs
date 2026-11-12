using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>The selected TEST_ONLY composition over the existing Warned connected world.</summary>
    public static class ConnectedExplorationObservation
    {
        public const string FingerprintPrefix = "TEST_ONLY.connected-observe-v1-";
        public const string SearchDirector = "TEST_ONLY.director.connected-visual-search.v1";
        public const string HideDirector = "TEST_ONLY.director.connected-hide.v1";
        public const string VisibleFringe = "TEST_ONLY.connected-faint-fringe.v1";
        public const string Hero = "TEST_ONLY.actor";
        public const string Searcher = "TEST_ONLY.companion";
        public const string Buyer = "TEST_ONLY.haven-copper-buyer";
        private static readonly string[] Actors = { Hero, Searcher, Buyer, "TEST_ONLY.third-combatant", "TEST_ONLY.later-defender" };

        public static bool IsSelected(Snapshot state)
            => state.ContentFingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
                || ConnectedBloodSpecimen.HasFingerprint(state);

        public static bool MatchesSearch(ExplorationSearchDefinition d)
            => d.DirectorId == SearchDirector && d.CueId == VisibleFringe && d.SearcherId == Searcher
                && d.ConcealedActorId == Hero && d.Anchor.Equals(new ExplorationSearchCell(3, 2))
                && d.CueCandidate.Equals(new ExplorationSearchCell(1, 0)) && d.Sign.Equals(new ExplorationSearchCell(3, 1))
                && d.Occlusion.Equals(new ExplorationSearchCell(2, 1));

        public static bool StageOpen(Snapshot state)
            => state.LaterEncounter?.FirstExit != null && state.LaterEncounter.Entry == null
                && state.CharterAttempt?.Outcome == CharterAttemptOutcome.ReturnedComplete;

        internal static void ValidateLayout(Snapshot state, ExplorationSearchDefinition search)
        {
            var binding = state.SurpriseEntry?.Binding;
            var later = state.LaterEncounter?.Definition;
            var cells = state.ObservationCells;
            if (!state.TestOnly || state.SchemaVersion != Snapshot.SurpriseEntrySchema || state.ExplorationHide == null
                || binding?.Outcome != SurpriseAwareness.Warned || binding.ParticipantId != Hero
                || later?.HeroId != Hero || state.Reinforcement == null || state.Retreat == null || state.Reengagement == null
                || state.WorldSchedule?.Id != "world.fixed-calendar" || state.ObservationMapWidth != 5
                || state.ObservationMapHeight != 5 || cells.Length != 1 || cells[0].X != 2 || cells[0].Y != 1
                || !cells[0].BlocksSight || cells[0].BlocksEffect || cells[0].BlocksMovement || cells[0].Solid
                || !MatchesSearch(search) || state.ObservationProfiles.Length != Actors.Length
                || !Actors.All(id => state.ObservationProfiles.Any(x => x.ActorId == id && x.SightRangeFeet == 30 && x.SearchRangeFeet == 30)))
                throw new ArgumentException("Invalid selected wire93 connected observation layout.");
        }

        internal static void ValidateDeclaration(Snapshot state, long revision, RuleTime at)
        {
            var returned = state.CharterAttempt?.Returned;
            var later = state.LaterEncounter;
            var first = later.FirstExit;
            var entry = later.Entry;
            if (state.CharterAttempt?.Outcome != CharterAttemptOutcome.ReturnedComplete || returned == null || first == null
                || revision <= returned.Revision || revision <= first.ClosedRevision || at < returned.At
                || entry != null && (revision >= entry.ArrivalRevision || at > entry.Epoch.Origin))
                throw new ArgumentException("Connected observation declaration falls outside its historical ordinary stage.");
        }

        internal static void ValidateTerminal(Snapshot state, long revision, string command, RuleTime at, bool enteredTactical)
        {
            var entry = state.LaterEncounter.Entry;
            if (enteredTactical) {
                if (entry == null || revision != entry.ArrivalRevision || command != entry.ArrivalCommandId || at != entry.Epoch.Origin)
                    throw new ArgumentException("Connected observation interruption lacks its actual later entry receipt.");
            } else if (entry != null && (revision >= entry.ArrivalRevision || at > entry.Epoch.Origin)) {
                throw new ArgumentException("Connected ordinary observation cannot finish after later entry.");
            }
        }
    }
}
