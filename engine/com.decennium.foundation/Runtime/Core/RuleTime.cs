using System;
using System.Globalization;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>
    /// Exact nonnegative rational seconds. No simulation cadence or slot phases are implied.
    /// Normalized components fit Int64; overflowing results reject rather than round.
    /// Default is zero seconds. Intermediate products use BigInteger to avoid overflow.
    /// </summary>
    public readonly struct RuleTime : IComparable<RuleTime>, IEquatable<RuleTime>
    {
        private readonly long numerator, denominator;
        public long Numerator => numerator;
        public long Denominator => denominator == 0 ? 1 : denominator;
        public RuleTime(long numerator, long denominator=1)
        {
            if(numerator<0 || denominator<=0) throw new ArgumentOutOfRangeException(nameof(numerator));
            long divisor=(long)BigInteger.GreatestCommonDivisor(numerator,denominator);
            this.numerator=numerator/divisor; this.denominator=denominator/divisor;
        }
        public static RuleTime FromFraction(BigInteger numerator, BigInteger denominator)
        {
            if(numerator<0 || denominator<=0) throw new ArgumentOutOfRangeException(nameof(numerator));
            BigInteger divisor=BigInteger.GreatestCommonDivisor(numerator,denominator);
            return new RuleTime(checked((long)(numerator/divisor)),checked((long)(denominator/divisor)));
        }
        public RuleTime AddSeconds(long seconds)
        {
            if(seconds<0) throw new ArgumentOutOfRangeException(nameof(seconds));
            return FromFraction((BigInteger)Numerator+(BigInteger)seconds*Denominator,Denominator);
        }
        public int CompareTo(RuleTime other) => ((BigInteger)Numerator*other.Denominator).CompareTo((BigInteger)other.Numerator*Denominator);
        public bool Equals(RuleTime other) => Numerator==other.Numerator && Denominator==other.Denominator;
        public override bool Equals(object obj) => obj is RuleTime other && Equals(other);
        public override int GetHashCode() => unchecked(Numerator.GetHashCode()*397 ^ Denominator.GetHashCode());
        public override string ToString() => Numerator.ToString(CultureInfo.InvariantCulture)+"/"+Denominator.ToString(CultureInfo.InvariantCulture);
        public static bool operator ==(RuleTime a, RuleTime b) => a.Equals(b);
        public static bool operator !=(RuleTime a, RuleTime b) => !a.Equals(b);
        public static bool operator <(RuleTime a, RuleTime b) => a.CompareTo(b)<0;
        public static bool operator >(RuleTime a, RuleTime b) => a.CompareTo(b)>0;
        public static bool operator <=(RuleTime a, RuleTime b) => a.CompareTo(b)<=0;
        public static bool operator >=(RuleTime a, RuleTime b) => a.CompareTo(b)>=0;
    }
}
