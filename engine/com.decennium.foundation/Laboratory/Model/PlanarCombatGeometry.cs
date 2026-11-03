#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit aligned five-foot combat cells, not synthetic world coordinates or arbitrary 3D positions.</summary>
    public readonly struct CombatCell
    {
        public int X { get; }
        public int Y { get; }
        public CombatCell(int x,int y){X=x;Y=y;}
    }
    public enum CombatCover { None, Half, ThreeQuarters, Total }
    public readonly struct CoverResult
    {
        public CombatCover Cover { get; }
        public bool DirectTargetLegal=>Cover!=CombatCover.Total;
        public int? DefenseBonus=>Cover==CombatCover.Total?(int?)null:Cover==CombatCover.ThreeQuarters?5:Cover==CombatCover.Half?2:0;
        internal CoverResult(CombatCover cover){Cover=cover;}
    }
    public readonly struct RangeResult
    {
        public bool WithinMaximum { get; }
        public bool RangeDisadvantage { get; }
        internal RangeResult(bool legal,bool disadvantage){WithinMaximum=legal;RangeDisadvantage=disadvantage;}
    }
    /// <summary>Source-bound planar distance and individual targeting constraints only. Does not infer
    /// visibility, line of effect, occupied body volumes, pathfinding, weapon/hands or complete attack legality.</summary>
    public static class PlanarCombatGeometry
    {
        public static long DistanceFeet(CombatCell from,CombatCell to)
            =>5*Math.Max(Math.Abs((long)to.X-from.X),Math.Abs((long)to.Y-from.Y));

        // This is the corner constraint for a single neighboring step, not a traversability decision.
        public static bool NeighborPassesCornerRule(CombatCell from,CombatCell to,bool horizontalSideCompletelyBlocked,bool verticalSideCompletelyBlocked)
        {
            long x=Math.Abs((long)to.X-from.X),y=Math.Abs((long)to.Y-from.Y);
            if(x>1||y>1||x+y==0)throw new ArgumentException("Supply one neighboring combat step.");
            return x==0||y==0||!horizontalSideCompletelyBlocked||!verticalSideCompletelyBlocked;
        }
        public static CoverResult BestCover(IEnumerable<CombatCover> covers)
        {
            if(covers==null)throw new ArgumentNullException(nameof(covers));
            CombatCover best=CombatCover.None;
            foreach(var cover in covers) {
                if(cover<CombatCover.None||cover>CombatCover.Total)throw new ArgumentException("Unknown cover.");
                if(cover>best)best=cover;
            }
            return new CoverResult(best);
        }
        public static RangeResult RangedRange(long distanceFeet,long normalFeet,long maximumFeet)
        {
            if(distanceFeet<0||normalFeet<0||maximumFeet<normalFeet)throw new ArgumentException("Invalid ranged distance or profile.");
            return new RangeResult(distanceFeet<=maximumFeet,distanceFeet>normalFeet&&distanceFeet<=maximumFeet);
        }
        public static bool CloseHostileDisadvantage(long distanceFeet,bool hostile,bool incapacitated,bool hostileSeesAttacker)
        {
            if(distanceFeet<0)throw new ArgumentOutOfRangeException(nameof(distanceFeet));
            return distanceFeet<=5&&hostile&&!incapacitated&&hostileSeesAttacker;
        }
    }
}
#endif
