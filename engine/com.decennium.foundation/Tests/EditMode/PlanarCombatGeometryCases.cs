#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddPlanarGeometryCases(Dictionary<string,Action> cases)
        {
            cases.Add("geometry_neighbors_are_five_feet_in_all_eight_directions",()=>{
                var center=new CombatCell(-7,12);
                for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++)if(x!=0||y!=0)
                    Require(PlanarCombatGeometry.DistanceFeet(center,new CombatCell(-7+x,12+y))==5,"Neighbor used Euclidean or alternating diagonals."); });
            cases.Add("geometry_long_diagonal_and_orthogonal_use_same_metric",()=>{
                var zero=new CombatCell(0,0);
                Require(PlanarCombatGeometry.DistanceFeet(zero,new CombatCell(6,6))==30&&PlanarCombatGeometry.DistanceFeet(zero,new CombatCell(6,0))==30
                    &&PlanarCombatGeometry.DistanceFeet(zero,new CombatCell(4,-6))==30&&PlanarCombatGeometry.DistanceFeet(zero,zero)==0,"Ordinary range metric changed."); });
            cases.Add("geometry_distance_is_symmetric_translation_invariant_and_widened",()=>{
                foreach(int x in new[]{int.MinValue,-1,0,1,int.MaxValue})foreach(int y in new[]{int.MinValue,-1,0,1,int.MaxValue}) {
                    var a=new CombatCell(x,y);var b=new CombatCell(y,x);Require(PlanarCombatGeometry.DistanceFeet(a,b)==PlanarCombatGeometry.DistanceFeet(b,a),"Distance is asymmetric.");}
                Require(PlanarCombatGeometry.DistanceFeet(new CombatCell(int.MinValue,int.MaxValue),new CombatCell(int.MaxValue,int.MinValue))==21474836475L,"Coordinate subtraction overflowed.");
                Require(PlanarCombatGeometry.DistanceFeet(new CombatCell(10,8),new CombatCell(12,9))==PlanarCombatGeometry.DistanceFeet(new CombatCell(-2,-3),new CombatCell(0,-2)),"Translation changed metric."); });
            cases.Add("geometry_diagonal_corner_requires_both_completely_blocked_sides",()=>{
                foreach(bool a in new[]{false,true})foreach(bool b in new[]{false,true})
                    Require(PlanarCombatGeometry.NeighborPassesCornerRule(new CombatCell(0,0),new CombatCell(-1,1),a,b)==!(a&&b),"Corner restriction changed."); });
            cases.Add("geometry_orthogonal_steps_do_not_use_diagonal_corner_rule",()=>{
                Require(PlanarCombatGeometry.NeighborPassesCornerRule(new CombatCell(0,0),new CombatCell(1,0),true,true)
                    &&PlanarCombatGeometry.NeighborPassesCornerRule(new CombatCell(0,0),new CombatCell(0,-1),true,true),"Side blockers became destination collision checks."); });
            cases.Add("geometry_corner_constraint_rejects_zero_and_nonneighbor_steps",()=>{
                foreach(var end in new[]{new CombatCell(0,0),new CombatCell(2,0),new CombatCell(1,-2),new CombatCell(int.MaxValue,int.MinValue)})
                    Throws<ArgumentException>(()=>PlanarCombatGeometry.NeighborPassesCornerRule(new CombatCell(0,0),end,false,false)); });
            cases.Add("geometry_cover_uses_only_best_bonus",()=>{
                var c=PlanarCombatGeometry.BestCover(new[]{CombatCover.Half,CombatCover.None,CombatCover.ThreeQuarters,CombatCover.Half});
                Require(c.DirectTargetLegal&&c.DefenseBonus==5&&PlanarCombatGeometry.BestCover(Array.Empty<CombatCover>()).DefenseBonus==0
                    &&PlanarCombatGeometry.BestCover(new[]{CombatCover.Half,CombatCover.Half}).DefenseBonus==2,"Cover stacked or empty cover gained a bonus."); });
            cases.Add("geometry_total_cover_blocks_direct_target_with_no_finite_bonus",()=>{
                var c=PlanarCombatGeometry.BestCover(new[]{CombatCover.Total,CombatCover.Half,CombatCover.ThreeQuarters});
                Require(!c.DirectTargetLegal&&c.DefenseBonus==null,"Total cover became a hittable AC bonus."); });
            cases.Add("geometry_cover_rejects_unknown_values_even_after_total",()=>{
                Throws<ArgumentNullException>(()=>PlanarCombatGeometry.BestCover(null));
                foreach(int invalid in new[]{-1,4,int.MaxValue})Throws<ArgumentException>(()=>PlanarCombatGeometry.BestCover(new[]{CombatCover.Total,(CombatCover)invalid})); });
            cases.Add("geometry_range_endpoints_are_inclusive",()=>{
                foreach(long d in new[]{0L,79,80}) {var r=PlanarCombatGeometry.RangedRange(d,80,320);Require(r.WithinMaximum&&!r.RangeDisadvantage,"Normal range endpoint penalized.");}
                foreach(long d in new[]{81L,319,320}) {var r=PlanarCombatGeometry.RangedRange(d,80,320);Require(r.WithinMaximum&&r.RangeDisadvantage,"Long range endpoint rejected.");}
                var beyond=PlanarCombatGeometry.RangedRange(321,80,320);Require(!beyond.WithinMaximum&&!beyond.RangeDisadvantage,"Illegal range offered a disadvantaged attack."); });
            cases.Add("geometry_range_handles_equal_zero_and_maximum_limits",()=>{
                Require(PlanarCombatGeometry.RangedRange(0,0,0).WithinMaximum&&!PlanarCombatGeometry.RangedRange(0,0,0).RangeDisadvantage,"Zero range numeric boundary changed.");
                Require(PlanarCombatGeometry.RangedRange(long.MaxValue,0,long.MaxValue).RangeDisadvantage
                    &&!PlanarCombatGeometry.RangedRange(long.MaxValue,long.MaxValue,long.MaxValue).RangeDisadvantage,"Long range arithmetic overflowed."); });
            cases.Add("geometry_range_rejects_negative_and_reversed_profiles",()=>{
                Throws<ArgumentException>(()=>PlanarCombatGeometry.RangedRange(-1,1,2));Throws<ArgumentException>(()=>PlanarCombatGeometry.RangedRange(0,-1,2));
                Throws<ArgumentException>(()=>PlanarCombatGeometry.RangedRange(0,2,1)); });
            cases.Add("geometry_close_hostile_uses_hostiles_sight_and_capacity",()=>{
                foreach(long distance in new[]{0L,5,6,long.MaxValue})foreach(bool hostile in new[]{false,true})foreach(bool incapable in new[]{false,true})foreach(bool sees in new[]{false,true})
                    Require(PlanarCombatGeometry.CloseHostileDisadvantage(distance,hostile,incapable,sees)==(distance<=5&&hostile&&!incapable&&sees),"Close hostile criterion changed.");
                Throws<ArgumentOutOfRangeException>(()=>PlanarCombatGeometry.CloseHostileDisadvantage(-1,true,false,true)); });
        }
    }
}
#endif
