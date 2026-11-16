using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class ClericLongRestProfile
    {
        public static bool IsCommand(CommandKind kind)
            => kind == CommandKind.BeginLongRest || kind == CommandKind.InterruptLongRest;
        public static ClericLongRestRecord Active(Snapshot s)
            => s.ConnectedClericLongRest ? s.ClericLongRests.SingleOrDefault(x => x.Outcome == ClericLongRestOutcome.Active) : null;
        public static bool RestOccupancy(Snapshot s, WorkerInterval interval)
            => s.ConnectedClericLongRest && interval.WorkerId == ClericRpProfile.Actor
                && interval.Id == OccupancyId(interval.JobId) && s.ClericLongRests.Any(x => x.Id == interval.JobId);

        // Reconstruct ordered events; terminal recovery amounts must never be added to all earlier balances.
        public static int RpBefore(Snapshot s, long revision)
        {
            int balance = s.ResonancePools.Single(x => x.ActorId == ClericRpProfile.Actor).InitialFunding.Amount;
            var events = s.HealingRites.Select(x => (revision:x.Revision, before:x.RpBefore, after:x.RpAfter, recovery:false))
                .Concat(s.SpellCasts.Select(x => (revision:x.Revision, before:x.RpBefore, after:x.RpAfter, recovery:false)))
                .Concat(s.ClericLongRestSettlements.Select(x => (revision:x.Revision, before:x.RpBefore, after:x.RpAfter, recovery:true)))
                .Where(x => x.revision < revision).OrderBy(x => x.revision).ToArray();
            if (events.Select(x => x.revision).Distinct().Count() != events.Length)
                throw new ArgumentException("Multiple RP settlement events share one command revision.");
            foreach (var e in events) {
                if (e.before != balance || !e.recovery && e.after > e.before)
                    throw new ArgumentException("Invalid ordered RP payment/recovery history.");
                balance = e.after;
            }
            return balance;
        }

        internal static void Validate(Snapshot s)
        {
            bool selected = SelectedFingerprint(s.ContentFingerprint);
            if (s.ConnectedClericLongRest != selected || s.ClericLongRests == null || s.ClericLongRestSettlements == null
                || s.ClericLongRests.Length > MaxAttempts || s.ClericLongRestSettlements.Length > MaxAttempts
                || s.ClericLongRests.Any(x => x == null) || s.ClericLongRestSettlements.Any(x => x == null))
                throw new ArgumentException("Invalid connected Long Rest envelope.");
            if (!selected) {
                if (s.ClericLongRests.Length != 0 || s.ClericLongRestSettlements.Length != 0 || s.ConvictionBalance != null)
                    throw new ArgumentException("Long Rest history requires its explicit profile.");
                return;
            }
            if (!s.TestOnly || !s.ConnectedClericCasting || s.SchemaVersion != Snapshot.SurpriseEntrySchema)
                throw new ArgumentException("Long Rest requires its exact connected profile.");
            if (s.RestIntervals.Length != s.ClericLongRests.Length
                || s.ClericLongRestSettlements.Length != s.ClericLongRests.Count(x => x.Outcome == ClericLongRestOutcome.Completed)
                || s.ClericLongRestSettlements.Select(x => x.RestId).Distinct(StringComparer.Ordinal).Count() != s.ClericLongRestSettlements.Length
                || s.ExpeditionBeneficialRests.Any(x => x.ActorId != ClericRpProfile.Actor))
                throw new ArgumentException("Unsupported Long Rest participant or history coverage.");
            long previousRevision = 0;
            RuleTime previousEnd = default;
            foreach (var rest in s.ClericLongRests) {
                bool active = rest.Outcome == ClericLongRestOutcome.Active;
                if (rest.Sequence != Array.IndexOf(s.ClericLongRests, rest) || rest.StartRevision <= previousRevision
                    || rest.StartRevision > s.Revision || rest.StartedAt < previousEnd || rest.StartedAt > s.RuleClock
                    || active && (rest.Sequence != s.ClericLongRests.Length - 1 || rest.DueAt <= s.RuleClock)
                    || rest.EndRevision > s.Revision || rest.EndedAt > s.RuleClock
                    || s.ConvictionCapacity.PoolAcquiredRevision == 0 || rest.StartRevision <= s.ConvictionCapacity.PoolAcquiredRevision)
                    throw new ArgumentException("Invalid Long Rest chronology or earned access.");
                var start = new Command(rest.StartCommandId,rest.ActorId,rest.StartRevision-1,CommandKind.BeginLongRest,rest.SiteId);
                if (!s.Receipts.Any(x => x.Revision == rest.StartRevision && x.Principal == "TEST_ONLY.host" && start.MatchesReceipt(x)))
                    throw new ArgumentException("Long Rest has no exact start receipt.");
                var interval = s.RestIntervals.SingleOrDefault(x => x.Id == rest.Id);
                var status = active ? RestIntervalStatus.Active : rest.Outcome == ClericLongRestOutcome.Completed
                    ? RestIntervalStatus.Completed : RestIntervalStatus.Interrupted;
                if (interval == null || interval.ActorId != rest.ActorId || interval.SiteId != rest.SiteId
                    || interval.StartedAt != rest.StartedAt || interval.ScheduledEnd != rest.DueAt
                    || interval.Status != status || interval.EndedAt != rest.EndedAt
                    || interval.Revision != (active ? rest.StartRevision : rest.EndRevision))
                    throw new ArgumentException("Long Rest differs from its shared interval.");
                var occupancy = s.Work.WorkerIntervals.SingleOrDefault(x => x.Id == OccupancyId(rest.Id));
                var workEnd = rest.Outcome == ClericLongRestOutcome.Interrupted ? rest.EndedAt.Value : rest.DueAt;
                if (workEnd == rest.StartedAt ? occupancy != null : occupancy == null || occupancy.JobId != rest.Id
                    || occupancy.WorkerId != rest.ActorId || occupancy.Start != rest.StartedAt || occupancy.End != workEnd)
                    throw new ArgumentException("Long Rest differs from actual exclusive labor.");
                if (!active) {
                    var terminal = s.Receipts.SingleOrDefault(x => x.Revision == rest.EndRevision);
                    if (terminal == null || terminal.Id != rest.EndCommandId)
                        throw new ArgumentException("Long Rest has no terminal receipt.");
                    if (rest.Interruption == ClericLongRestInterruption.Explicit) {
                        var interrupt = new Command(rest.EndCommandId,rest.ActorId,rest.EndRevision-1,CommandKind.InterruptLongRest,rest.Id);
                        if (terminal.Principal != "TEST_ONLY.host" || !interrupt.MatchesReceipt(terminal))
                            throw new ArgumentException("Long Rest has no exact interruption receipt.");
                    }
                }
                previousRevision = active ? rest.StartRevision : rest.EndRevision;
                previousEnd = active ? rest.DueAt : rest.EndedAt.Value;
            }
            int? conviction = null;
            ClericLongRestSettlementRecord previousBenefit = null;
            long lastSettlementRevision = 0;
            foreach (var x in s.ClericLongRestSettlements) {
                var rest = s.ClericLongRests.SingleOrDefault(r => r.Id == x.RestId);
                bool eligible = x.Benefit == ClericLongRestBenefit.Eligible;
                if (rest == null || rest.Outcome != ClericLongRestOutcome.Completed || rest.Benefit != x.Benefit
                    || rest.EndRevision != x.Revision || rest.EndCommandId != x.CommandId || rest.EndedAt != x.At
                    || x.Revision <= lastSettlementRevision || x.Revision > s.Revision || x.At > s.RuleClock
                    || x.CapacityAcquiredRevision != s.ConvictionCapacity.PoolAcquiredRevision
                    || x.PreviousBeneficialRestId != (previousBenefit?.BeneficialRestId ?? "")
                    || x.ConvictionBefore != conviction || x.RpBefore != RpBefore(s,x.Revision)
                    || x.ExpendedHitDice != 0 || x.HitDiceRecovered != 0)
                    throw new ArgumentException("Unattributed Long Rest resource settlement.");
                var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(b => b.RestIntervalId == x.RestId);
                bool cadence = previousBenefit == null || x.At >= previousBenefit.At.AddSeconds(BenefitCadenceSeconds);
                if (eligible ? !cadence || benefit == null || benefit.Id != x.BeneficialRestId || benefit.Revision != x.Revision
                        || benefit.CompletedAt != x.At
                    : benefit != null || x.Benefit == ClericLongRestBenefit.CadenceLimited && cadence)
                    throw new ArgumentException("Invalid Long Rest benefit cadence or source link.");
                conviction = x.ConvictionAfter;
                if (eligible) previousBenefit = x;
                lastSettlementRevision = x.Revision;
            }
            if (s.ExpeditionBeneficialRests.Length != s.ClericLongRestSettlements.Count(x => x.Benefit == ClericLongRestBenefit.Eligible))
                throw new ArgumentException("Long Rest benefit and class settlement histories differ.");
            var firstFunding = s.ClericLongRestSettlements.FirstOrDefault(x => x.Benefit == ClericLongRestBenefit.Eligible);
            if (firstFunding == null ? s.ConvictionBalance != null : s.ConvictionBalance == null
                || s.ConvictionBalance.FundingRestId != firstFunding.RestId || s.ConvictionBalance.FundingRevision != firstFunding.Revision
                || s.ConvictionBalance.Current != conviction || conviction != 5)
                throw new ArgumentException("Current Conviction has no actual first eligible rest funding.");
        }
    }
}
