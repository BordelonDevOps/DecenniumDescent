#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum D20Selection { Normal, Advantage, Disadvantage }
    public sealed class D20Roll
    {
        public D20Selection Selection { get; }
        public int First { get; }
        public int? Second { get; }
        public int Natural { get; }
        public uint NextRandomState { get; }
        public long WordsConsumed { get; }
        internal D20Roll(D20Selection selection,int first,int? second,int natural,uint state,long words)
        {Selection=selection;First=first;Second=second;Natural=natural;NextRandomState=state;WordsConsumed=words;}
    }
    /// <summary>Caller supplies eligible advantage/disadvantage sources. Any presence on both sides cancels.</summary>
    public static class PlaytestDice
    {
        public static D20Selection Selection(int advantageSources,int disadvantageSources)
        {
            if(advantageSources<0 || disadvantageSources<0) throw new ArgumentOutOfRangeException(nameof(advantageSources));
            if((advantageSources==0)==(disadvantageSources==0)) return D20Selection.Normal;
            return advantageSources>0 ? D20Selection.Advantage : D20Selection.Disadvantage;
        }
        public static D20Roll RollD20(uint initialState,int advantageSources=0,int disadvantageSources=0)
        {
            D20Selection selection=Selection(advantageSources,disadvantageSources);
            BoundedDraw first=DiceStream.Draw(initialState,20);
            if(selection==D20Selection.Normal) return new D20Roll(selection,first.Value+1,null,first.Value+1,first.NextState,first.WordsConsumed);
            BoundedDraw second=DiceStream.Draw(first.NextState,20);
            int a=first.Value+1,b=second.Value+1;
            return new D20Roll(selection,a,b,selection==D20Selection.Advantage?Math.Max(a,b):Math.Min(a,b),
                second.NextState,checked(first.WordsConsumed+second.WordsConsumed));
        }
    }
}
#endif
