#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum TerrainCost { Normal=1, Difficult=2, Severe=3 }
    public enum SpecialMovement { Ready, Withdraw, Interpose, Press }

    /// <summary>Spent cost follows a turn across movement modes; caller pays each legal Dash.</summary>
    public sealed class MovementLedger
    {
        public long Spent { get; }
        public int Dashes { get; }
        public MovementLedger(long spent=0, int dashes=0)
        {
            if (spent<0 || dashes<0) throw new ArgumentOutOfRangeException(nameof(spent));
            Spent=spent; Dashes=dashes;
        }
        public long Remaining(long currentSpeed)
        {
            if (currentSpeed<0) throw new ArgumentOutOfRangeException(nameof(currentSpeed));
            return Math.Max(0,checked((1L+Dashes)*currentSpeed)-Spent);
        }
        public MovementLedger Spend(long cost, long currentSpeed)
        {
            if (cost<0 || cost>Remaining(currentSpeed)) throw new ArgumentException("Insufficient movement for current mode.");
            return new MovementLedger(checked(Spent+cost),Dashes);
        }
        public MovementLedger Stand(long currentSpeed)
        {
            if (currentSpeed<=0) throw new ArgumentException("Cannot stand without positive Speed.");
            return Spend(currentSpeed/2,currentSpeed);
        }
        public MovementLedger AddPaidDash() => new MovementLedger(Spent,checked(Dashes+1));
    }

    /// <summary>Ordinary Reaction only; extra card-granted resources are separate records.</summary>
    public sealed class ReactionClock
    {
        public bool Available { get; }
        public bool SurprisePending { get; }
        public long LastRegularStart { get; }
        public ReactionClock(bool available=true, bool surprisePending=false, long lastRegularStart=-1)
        {
            if(lastRegularStart < -1) throw new ArgumentOutOfRangeException(nameof(lastRegularStart));
            Available=available; SurprisePending=surprisePending; LastRegularStart=lastRegularStart;
        }
        public ReactionClock RegularStart(long marker)
        {
            if(marker<0 || marker<=LastRegularStart) throw new ArgumentException("Regular start cannot repeat or go backward.");
            return new ReactionClock(true,SurprisePending,marker);
        }
        public ReactionClock EndFirstRegularTurn()
        {
            if(LastRegularStart<0) throw new ArgumentException("First regular turn has not begun.");
            return new ReactionClock(Available,false,LastRegularStart);
        }
        public ReactionClock Spend(bool prohibited=false)
        {
            if(!Available || SurprisePending || prohibited) throw new ArgumentException("Reaction unavailable.");
            return new ReactionClock(false,SurprisePending,LastRegularStart);
        }
        public ReactionClock ExtraTurn() => this;
        public ReactionClock RoundBoundary() => this;
    }

    /// <summary>Per-creature record. This enforces the shared cap; it never supplies an extra Action.</summary>
    public sealed class ExtraActionClock
    {
        public IReadOnlyList<long> SpentRounds { get; }
        public ExtraActionClock(IEnumerable<long> spentRounds=null)
        {
            long[] rounds=(spentRounds??Array.Empty<long>()).ToArray();
            if(rounds.Any(x=>x<1) || rounds.Distinct().Count()!=rounds.Length)
                throw new ArgumentException("Distinct positive numbered rounds required.");
            Array.Sort(rounds); SpentRounds=Array.AsReadOnly(rounds);
        }
        public ExtraActionClock Spend(long numberedRound, bool grantedByExtraAction=false)
        {
            if(numberedRound<1 || grantedByExtraAction || SpentRounds.Contains(numberedRound))
                throw new ArgumentException("Extra full Action cap or recursive grant.");
            return new ExtraActionClock(SpentRounds.Concat(new[]{numberedRound}));
        }
    }

    public static class PlaytestCombatBudgets
    {
        public static long MovementCost(long distanceFeet, TerrainCost terrain=TerrainCost.Normal,
            bool crawling=false, bool squeezing=false)
        {
            if(distanceFeet<0 || terrain<TerrainCost.Normal || terrain>TerrainCost.Severe)
                throw new ArgumentOutOfRangeException(nameof(distanceFeet));
            return checked(distanceFeet*((int)terrain+(crawling?1:0)+(squeezing?1:0)));
        }
        public static long SpecialBudget(SpecialMovement kind, long currentSpeed)
        {
            if(currentSpeed<0 || !Enum.IsDefined(typeof(SpecialMovement),kind)) throw new ArgumentException("Invalid movement grant.");
            if(currentSpeed==0) return 0;
            return kind==SpecialMovement.Ready ? currentSpeed : kind==SpecialMovement.Withdraw ? currentSpeed/2 : 5;
        }
        public static bool CanSpecialMove(SpecialMovement kind, long speed, long distanceFeet,
            TerrainCost terrain=TerrainCost.Normal, bool crawling=false, bool squeezing=false)
            => MovementCost(distanceFeet,terrain,crawling,squeezing)<=SpecialBudget(kind,speed);
        public static long ReinforcementFirstRound(long currentRound, bool slotStillUpcoming, bool endRoundEntry=false)
        {
            if(currentRound<1) throw new ArgumentOutOfRangeException(nameof(currentRound));
            return checked(currentRound+((endRoundEntry || !slotStillUpcoming)?1:0));
        }
    }
}
#endif
