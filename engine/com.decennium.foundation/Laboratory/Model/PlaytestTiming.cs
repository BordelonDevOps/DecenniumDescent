#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public sealed class EffectOrderRecord
    {
        public string ApplicationId { get; }
        public string MechanicalId { get; }
        public RuleTime AppliedAt { get; }
        public long ApplicationSequence { get; }
        public EffectOrderRecord(string applicationId, string mechanicalId, RuleTime appliedAt, long applicationSequence)
        {
            if(!Validation.ValidId(applicationId) || !Validation.ValidId(mechanicalId) || applicationSequence<0)
                throw new ArgumentException("Invalid effect ordering record.");
            ApplicationId=applicationId; MechanicalId=mechanicalId; AppliedAt=appliedAt; ApplicationSequence=applicationSequence;
        }
    }

    /// <summary>Exact reviewed virtual-marker arithmetic. The scheduler supplies original slot phases.</summary>
    public static class PlaytestTiming
    {
        public static RuleTime MarkerDeadline(RuleTime appliedAt, RuleTime originalMarkerPhase, int count=1,
            RuleTime? excludedCurrentMarker=null)
        {
            if(count<1) throw new ArgumentOutOfRangeException(nameof(count));
            BigInteger difference=(BigInteger)appliedAt.Numerator*originalMarkerPhase.Denominator
                -(BigInteger)originalMarkerPhase.Numerator*appliedAt.Denominator;
            BigInteger divisor=(BigInteger)appliedAt.Denominator*originalMarkerPhase.Denominator*6;
            BigInteger cycle=BigInteger.DivRem(difference,divisor,out BigInteger remainder);
            if(remainder<0) cycle--; // Floor, including when the original phase is later than application.
            cycle++;
            RuleTime first=RuleTime.FromFraction((BigInteger)originalMarkerPhase.Numerator
                +cycle*6*originalMarkerPhase.Denominator,originalMarkerPhase.Denominator);
            if(excludedCurrentMarker.HasValue && first==excludedCurrentMarker.Value) first=first.AddSeconds(6);
            return first.AddSeconds((count-1L)*6);
        }
        public static RuleTime AbsoluteDuration(RuleTime appliedAt, int rounds)
        {
            if(rounds<1) throw new ArgumentOutOfRangeException(nameof(rounds));
            return appliedAt.AddSeconds(rounds*6L);
        }
        public static RuleTime ReadyEffectDeadline(RuleTime preparedAt, RuleTime releasedAt, int rounds,
            RuleTime? markerPhase=null, RuleTime? excludedCurrentMarker=null)
        {
            if(releasedAt<preparedAt) throw new ArgumentException("Ready cannot release before preparation.");
            return markerPhase.HasValue ? MarkerDeadline(releasedAt,markerPhase.Value,rounds,excludedCurrentMarker)
                : AbsoluteDuration(releasedAt,rounds);
        }
        public static IReadOnlyList<EffectOrderRecord> OrderedEffects(IEnumerable<EffectOrderRecord> records)
        {
            if(records==null) throw new ArgumentNullException(nameof(records));
            var copy=records.ToArray();
            if(copy.Any(x=>x==null) || copy.Select(x=>x.ApplicationId).Distinct(StringComparer.Ordinal).Count()!=copy.Length)
                throw new ArgumentException("Effect application IDs must be unique.",nameof(records));
            // The producer records printed within-source component order in ApplicationSequence.
            return Array.AsReadOnly(copy.OrderBy(x=>x.AppliedAt).ThenBy(x=>x.ApplicationSequence)
                .ThenBy(x=>x.MechanicalId,StringComparer.Ordinal).ThenBy(x=>x.ApplicationId,StringComparer.Ordinal).ToArray());
        }
    }
}
#endif
