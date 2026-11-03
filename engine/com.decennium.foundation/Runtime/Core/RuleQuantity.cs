using System;
using System.Collections.Generic;
using System.Globalization;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>Exact nonnegative quantity. The consuming record supplies its unit; never implicitly convert units.</summary>
    public readonly struct RuleQuantity : IComparable<RuleQuantity>,IEquatable<RuleQuantity>
    {
        private readonly long numerator,denominator;
        public long Numerator=>numerator;
        public long Denominator=>denominator==0?1:denominator;
        public RuleQuantity(long numerator,long denominator=1)
        {
            if(numerator<0||denominator<=0)throw new ArgumentOutOfRangeException(nameof(numerator));
            long divisor=(long)BigInteger.GreatestCommonDivisor(numerator,denominator);
            this.numerator=numerator/divisor;this.denominator=denominator/divisor;
        }
        public static RuleQuantity FromFraction(BigInteger numerator,BigInteger denominator)
        {
            if(numerator<0||denominator<=0)throw new ArgumentOutOfRangeException(nameof(numerator));
            var gcd=BigInteger.GreatestCommonDivisor(numerator,denominator);
            return new RuleQuantity(checked((long)(numerator/gcd)),checked((long)(denominator/gcd)));
        }
        public RuleQuantity Scale(long numerator,long denominator=1)
        {
            if(numerator<0||denominator<=0)throw new ArgumentOutOfRangeException(nameof(numerator));
            return FromFraction((BigInteger)Numerator*numerator,(BigInteger)Denominator*denominator);
        }
        public static RuleQuantity Sum(IEnumerable<RuleQuantity> values)
        {
            if(values==null)throw new ArgumentNullException(nameof(values));
            BigInteger n=0,d=1;
            foreach(var value in values){n=n*value.Denominator+(BigInteger)value.Numerator*d;d*=value.Denominator;
                var gcd=BigInteger.GreatestCommonDivisor(n,d);n/=gcd;d/=gcd;}
            return FromFraction(n,d);
        }
        public int CompareTo(RuleQuantity other)=>((BigInteger)Numerator*other.Denominator).CompareTo((BigInteger)other.Numerator*Denominator);
        public bool Equals(RuleQuantity other)=>Numerator==other.Numerator&&Denominator==other.Denominator;
        public override bool Equals(object obj)=>obj is RuleQuantity other&&Equals(other);
        public override int GetHashCode()=>unchecked(Numerator.GetHashCode()*397^Denominator.GetHashCode());
        public override string ToString()=>Numerator.ToString(CultureInfo.InvariantCulture)+"/"+Denominator.ToString(CultureInfo.InvariantCulture);
        public static RuleQuantity operator +(RuleQuantity a,RuleQuantity b)=>FromFraction((BigInteger)a.Numerator*b.Denominator+(BigInteger)b.Numerator*a.Denominator,(BigInteger)a.Denominator*b.Denominator);
        public static RuleQuantity operator -(RuleQuantity a,RuleQuantity b)=>FromFraction((BigInteger)a.Numerator*b.Denominator-(BigInteger)b.Numerator*a.Denominator,(BigInteger)a.Denominator*b.Denominator);
        public static bool operator ==(RuleQuantity a,RuleQuantity b)=>a.Equals(b);
        public static bool operator !=(RuleQuantity a,RuleQuantity b)=>!a.Equals(b);
        public static bool operator <(RuleQuantity a,RuleQuantity b)=>a.CompareTo(b)<0;
        public static bool operator >(RuleQuantity a,RuleQuantity b)=>a.CompareTo(b)>0;
        public static bool operator <=(RuleQuantity a,RuleQuantity b)=>a.CompareTo(b)<=0;
        public static bool operator >=(RuleQuantity a,RuleQuantity b)=>a.CompareTo(b)>=0;
    }
}
