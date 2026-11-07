#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class AdditionalTacticalActor
    {
        public const string Id="TEST_ONLY.third-combatant",ClubId="TEST_ONLY.third-club";
        public int X { get; } public int Y { get; } public int WalkingSpeed { get; } public long Hp { get; } public long MaximumHp { get; }
        public AdditionalTacticalActor(int x,int y,int walkingSpeed,long hp=26,long maximumHp=26)
        {if(!TestOnlyPolicy.Walkable(x,y)||walkingSpeed<0||hp<1||maximumHp<hp||maximumHp>26)throw new ArgumentException("Invalid third actor fixture facts.");X=x;Y=y;WalkingSpeed=walkingSpeed;Hp=hp;MaximumHp=maximumHp;}
    }
    public sealed class TacticalTerrainCell
    {
        public int X { get; } public int Y { get; } public TerrainCost Terrain { get; }
        public TacticalTerrainCell(int x,int y,TerrainCost terrain)
        {if(!TestOnlyPolicy.Walkable(x,y)||!Enum.IsDefined(typeof(TerrainCost),terrain))throw new ArgumentException("Invalid supplied terrain.");X=x;Y=y;Terrain=terrain;}
    }
    /// <summary>Explicit five-foot conversion of the fixture map, mutually hostile ordinary humanoids,
    /// usable striking bodies, no surprise, and unobstructed sight/line of effect for legal adjacent
    /// attacks. No off-roster creatures, body restrictions, independent conditions, spells or effects.</summary>
    public sealed class TacticalCombatFixture
    {
        public AdditionalTacticalActor Third { get; }
        public IReadOnlyList<TacticalTerrainCell> Terrain { get; }
        public TacticalCombatFixture(AdditionalTacticalActor third=null,IEnumerable<TacticalTerrainCell> terrain=null)
        {
            Third=third;var rows=(terrain??Array.Empty<TacticalTerrainCell>()).ToArray();
            if(rows.Any(x=>x==null)||rows.Select(x=>x.X+","+x.Y).Distinct(StringComparer.Ordinal).Count()!=rows.Length)throw new ArgumentException("Duplicate/null supplied terrain.");
            Terrain=Array.AsReadOnly(rows.OrderBy(x=>x.X).ThenBy(x=>x.Y).ToArray());
        }
        internal string Fingerprint
        {
            get
            {
                string third=Third==null?"none":string.Join(",",new long[]{Third.X,Third.Y,Third.WalkingSpeed,Third.Hp}
                    .Select(x=>x.ToString(CultureInfo.InvariantCulture)));
                if(Third!=null&&Third.MaximumHp!=26)third+=",maxhp="+Third.MaximumHp.ToString(CultureInfo.InvariantCulture);
                return "tactical-v1|"+third+"|"+string.Join(";",Terrain.Select(x=>x.X.ToString(CultureInfo.InvariantCulture)
                    +","+x.Y.ToString(CultureInfo.InvariantCulture)+","+((int)x.Terrain).ToString(CultureInfo.InvariantCulture)));
            }
        }
        internal TerrainCost At(int x,int y)=>Terrain.FirstOrDefault(t=>t.X==x&&t.Y==y)?.Terrain??TerrainCost.Normal;
        public static Authority Host()=>new Authority("TEST_ONLY.host",new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id},true,true,
            new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id});
    }
}
#endif
