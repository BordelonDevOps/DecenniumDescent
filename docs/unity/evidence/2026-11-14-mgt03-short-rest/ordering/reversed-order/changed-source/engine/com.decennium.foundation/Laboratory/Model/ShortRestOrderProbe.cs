#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System.Linq;
namespace Decennium.Foundation.Laboratory
{
    // Evidence instrumentation only; never copied into the engine branch.
    public static class ShortRestOrderProbe
    {
        public static bool DeferExpiry { get; } = true;
        public static int Count { get; private set; }
        public static Observation Last { get; private set; }
        public static void Observe(Snapshot state, ShortRestRecord rest)
        {
            Count++;
            Last = new Observation(state, rest);
        }
        public sealed class Observation
        {
            public string Clock { get; }
            public string RestBeforeWrite { get; }
            public long TemporaryHp { get; }
            public string GrantId { get; }
            public long GrantRevision { get; }
            public string GrantEnd { get; }
            public string GrantEndedAt { get; }
            internal Observation(Snapshot state, ShortRestRecord rest)
            {
                Clock = state.RuleClock.ToString();
                RestBeforeWrite = state.ShortRests.Single(x => x.Id == rest.Id).Outcome.ToString();
                TemporaryHp = state.Lives.Single(x => x.ActorId == rest.ActorId).TemporaryHp;
                GrantId = state.ConsumeDecay.CommandId;
                GrantRevision = state.ConsumeDecay.Revision;
                GrantEnd = state.ConsumeDecay.End.ToString();
                GrantEndedAt = state.ConsumeDecay.EndedAt?.ToString();
            }
        }
    }
}
#endif
