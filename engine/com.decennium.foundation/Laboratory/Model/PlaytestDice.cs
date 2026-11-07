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
            return (D20Selection)RuleDice.SelectD20(advantageSources, disadvantageSources);
        }
        public static D20Roll RollD20(uint initialState,int advantageSources=0,int disadvantageSources=0)
        {
            RuleD20Roll roll = RuleDice.RollD20(initialState, advantageSources, disadvantageSources);
            return new D20Roll((D20Selection)roll.Selection, roll.First, roll.Second, roll.Natural,
                roll.NextRandomState, roll.WordsConsumed);
        }
    }
}
#endif
