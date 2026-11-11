#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static ExpeditionPressureExposureRecord LocalRetreatExposure(Snapshot s)
        {
            var definition = s.Retreat?.Definition;
            return definition == null ? null : s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == definition.ExposureId);
        }

        private static void ActivateLocalRetreatPressure(Snapshot s)
        {
            var d = s.Retreat?.Definition;
            if (d == null || d.RouteAccessId == "" || LocalRetreatExposure(s) != null) return;
            var lead = RetreatBody(s, d.LeadId);
            var companion = RetreatBody(s, d.CompanionId);
            if (!d.IsLanePoint(d.LeadId, lead.X, lead.Y) || !d.IsLanePoint(d.CompanionId, companion.X, companion.Y)) return;
            var joined = s.Reinforcement.Joined;
            s.ExpeditionPressureCohorts = new[] {
                ExpeditionPressureCohortRecord.ForLocalRetreat(d.CohortId, s.ContentFingerprint, d.RouteFingerprint,
                    d.InitialPressure, new[] { d.LeadId, d.CompanionId })
            };
            s.ExpeditionPressureExposures = new[] {
                new ExpeditionPressureExposureRecord(d.ExposureId, d.CohortId, d.RouteId, joined.Revision, joined.At)
            };
        }

        private static bool LocalRetreatOpeningBlocked(Snapshot s)
        {
            var d = s.Retreat?.Definition;
            if (d == null) return false;
            return s.ExpeditionPressureCheckpoints.Any(x => x.RouteId == d.RouteId
                && (x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    || x.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction && x.ConsequenceEndsAt > s.RuleClock));
        }

        private static string AssessLocalRetreatMovement(Snapshot s, string actor, int fromX, int fromY, int toX, int toY, bool tactical)
        {
            var d = s.Retreat?.Definition;
            if (d == null || LocalRetreatExposure(s) == null || !LocalRetreatOpeningBlocked(s)) return null;
            bool openingEdge = (fromX == 0 || fromX == 1) && (toX == 0 || toX == 1)
                && Math.Min(fromY, toY) == d.CrossingY && Math.Max(fromY, toY) == d.CrossingY + 1;
            return openingEdge ? "RetreatOpeningObstructedByPressure" : null;
        }

        private static RuleTime? NextLocalRetreatPressureBoundary(Snapshot s)
        {
            if (LocalRetreatExposure(s) == null) return null;
            long watch = EventWatchIndex(s.RuleClock);
            return new RuleTime(checked((watch + 1) * ExpeditionPressureRules.WatchSeconds));
        }

        private static void RecordLocalRetreatCombatSources(Snapshot s)
        {
            var exposure = LocalRetreatExposure(s);
            if (exposure == null || s.Revision + 1 <= exposure.StartedRevision) return;
            var d = s.Retreat.Definition;
            foreach (var attack in s.MeleeAttacks.Where(x => x.Revision == s.Revision + 1
                && (d.IsWithdrawing(x.AttackerId) || d.IsWithdrawing(x.TargetId)))) {
                AddPressureChange(s, exposure, ExpeditionPressureChangeKind.OpenCombat,
                    attack.Id, attack.Revision, attack.At, EventWatchIndex(attack.At));
            }
        }

        private static void RecordSuccessfulRetreatPressure(Snapshot s, Command cause)
        {
            var exposure = LocalRetreatExposure(s);
            AddPressureChange(s, exposure, ExpeditionPressureChangeKind.SuccessfulRetreat,
                cause.Id, s.Revision + 1, s.RuleClock, EventWatchIndex(s.RuleClock));
        }

        private static string ProcessLocalRetreatPressureBoundary(Snapshot s, Command cause)
        {
            var exposure = LocalRetreatExposure(s);
            if (exposure == null || s.RuleClock <= exposure.StartedAt || !IsPressureWatchEnd(s.RuleClock)) return null;
            long watch = EventWatchIndex(s.RuleClock) - 1;
            if (s.ExpeditionPressureCheckpoints.Any(x => x.CohortId == exposure.CohortId && x.WatchIndex == watch)) return null;
            if (cause == null) return "RetreatPressureCheckpointRequiresCommand";
            if (s.ExpeditionPressureCheckpoints.Length >= ExpeditionPressureValidation.MaxCheckpoints)
                return "ExpeditionPressureCheckpointCapacityReached";
            var d = s.Retreat.Definition;
            long revision = s.Revision + 1;
            var at = s.RuleClock;
            int before = ExpeditionPressureRules.CurrentAt(s, exposure.CohortId, revision, at);
            var causes = s.ExpeditionPressureChanges.Where(x => x.CohortId == exposure.CohortId && x.WatchIndex == watch
                && x.Kind == ExpeditionPressureChangeKind.OpenCombat && x.At <= at && x.SourceRevision <= revision)
                .OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            int stored = ExpeditionPressureRules.Settle(before, ExpeditionPressureRules.IncreaseCategoryCount(causes), 0, d.Risk);
            int effective = ExpeditionPressureRules.EffectiveForRouteCheck(stored, d.Quality);
            uint randomBefore = s.RandomState;
            uint randomAfter = randomBefore;
            int natural = 0;
            long words = 0;
            if (effective > 0 && effective < 6) {
                var die = DiceStream.Draw(randomBefore, 6);
                natural = die.Value + 1;
                randomAfter = die.NextState;
                words = die.WordsConsumed;
                s.RandomState = randomAfter;
            }
            var outcome = ExpeditionPressureRules.Classify(effective, natural, natural, false);
            var consequence = outcome == ExpeditionPressureOutcome.None ? ExpeditionPressureConsequenceKind.None
                : outcome == ExpeditionPressureOutcome.Severe ? ExpeditionPressureConsequenceKind.RouteClosure
                : ExpeditionPressureConsequenceKind.TimedRouteObstruction;
            RuleTime? until = outcome == ExpeditionPressureOutcome.Minor ? at.AddSeconds(900)
                : outcome == ExpeditionPressureOutcome.Standard ? at.AddSeconds(3600) : (RuleTime?)null;
            var checkpoint = new ExpeditionPressureCheckpointRecord("pressure-check-" + Number(watch), d.CohortId, watch, at,
                ExpeditionPressureSettlementReason.WatchEnd, d.RouteId, d.RouteFingerprint, s.ContentFingerprint, d.Quality,
                d.Risk, before, stored, effective, causes.Select(x => x.Id), Array.Empty<string>(), natural, natural, false,
                randomBefore, randomAfter, words, outcome, consequence,
                consequence == ExpeditionPressureConsequenceKind.None ? "" : d.RouteId,
                consequence == ExpeditionPressureConsequenceKind.RouteClosure ? d.RouteId : "",
                default, until, cause.Id, revision);
            s.ExpeditionPressureCheckpoints = s.ExpeditionPressureCheckpoints.Append(checkpoint).ToArray();
            return null;
        }
    }
}
#endif
