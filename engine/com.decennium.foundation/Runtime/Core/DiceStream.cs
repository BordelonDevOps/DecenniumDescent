using System;

namespace Decennium.Foundation
{
    public readonly struct BoundedDraw
    {
        public int Value { get; }
        public uint NextState { get; }
        public long WordsConsumed { get; }
        internal BoundedDraw(int value,uint state,long consumed) {Value=value;NextState=state;WordsConsumed=consumed;}
    }
    /// <summary>Unbiased mapping of RandomV1's nonzero uint output domain. No global random source.</summary>
    public static class DiceStream
    {
        public const string MappingVersion="xorshift32-nonzero-reject-v1";
        public static BoundedDraw Draw(uint initialState,int exclusiveMaximum)
        {
            if(initialState==0) throw new ArgumentException("RNG state cannot be zero.",nameof(initialState));
            if(exclusiveMaximum<1) throw new ArgumentOutOfRangeException(nameof(exclusiveMaximum));
            // RandomV1 produces 1..UInt32.MaxValue, not 0..UInt32.MaxValue.
            // Subtract one and retain an exact multiple of the requested outcome count.
            uint outcomes=(uint)exclusiveMaximum;
            uint limit=uint.MaxValue-uint.MaxValue%outcomes;
            uint state=initialState;long words=0;
            while(true) {
                uint value=RandomV1.Next(ref state)-1;words++;
                if(value<limit) return new BoundedDraw((int)(value%outcomes),state,words);
            }
        }
    }
}
