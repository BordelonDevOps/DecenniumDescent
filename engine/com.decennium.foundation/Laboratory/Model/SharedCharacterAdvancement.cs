#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicit Soldier 1 fixture for the source-scoped level-2 advancement path.</summary>
    public sealed class CharacterAdvancementFixture
    {
        public const string DefensivePositioning=CharacterFeatureIds.DefensivePositioning;
        public const string TacticalReposition=CharacterFeatureIds.TacticalReposition;
        public const string SoldierSourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public ActorLifeRecord HeroLife { get; }
        public bool StartingHitDieSpent { get; }
        public System.Collections.Generic.IReadOnlyList<TacticalCoverRecord> Covers { get; }
        public CharacterAdvancementFixture(ActorLifeRecord heroLife=null,params TacticalCoverRecord[] covers)
            :this(heroLife,false,covers)
        { }
        public CharacterAdvancementFixture(ActorLifeRecord heroLife,bool startingHitDieSpent,params TacticalCoverRecord[] covers)
        {
            HeroLife=heroLife??new ActorLifeRecord(TestOnlyPolicy.ActorId,10,4,0,Array.Empty<int>(),false,false,true,0,0,null,0,false,new[]{TestOnlyClubAttackPolicy.ActorClub});
            StartingHitDieSpent=startingHitDieSpent;
            var rows=covers??Array.Empty<TacticalCoverRecord>();
            if(HeroLife.ActorId!=TestOnlyPolicy.ActorId||HeroLife.MaximumHp!=10||!HeroLife.HeldItems.SequenceEqual(new[]{TestOnlyClubAttackPolicy.ActorClub},StringComparer.Ordinal)
                ||rows.Length>64||rows.Any(x=>x==null)
                ||rows.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=rows.Length||rows.Select(x=>x.X+","+x.Y).Distinct(StringComparer.Ordinal).Count()!=rows.Length)
                throw new ArgumentException("The advancement fixture requires the named Soldier's ten-point level-1 capacity, held Club custody, and unique cover markers.");
            Covers=Array.AsReadOnly(rows.ToArray());
        }
        internal string Key=>"soldier-1-to-2-v1|milestone-only|fixed-average-d10-base-6|prior-hit-die-spent="+(StartingHitDieSpent?"1":"0")+"|"+string.Join("|",new[]{HeroLife.ActorId,
            HeroLife.MaximumHp.ToString(CultureInfo.InvariantCulture),HeroLife.Hp.ToString(CultureInfo.InvariantCulture),HeroLife.TemporaryHp.ToString(CultureInfo.InvariantCulture),
            string.Join(",",HeroLife.LinkedInjuries),HeroLife.Stable?"1":"0",HeroLife.Dead?"1":"0",HeroLife.UsesDeathSaves?"1":"0",
            HeroLife.DeathSuccesses.ToString(CultureInfo.InvariantCulture),HeroLife.DeathFailures.ToString(CultureInfo.InvariantCulture),HeroLife.StableUntil?.ToString()??"none",
            HeroLife.LastDeathTurn.ToString(CultureInfo.InvariantCulture),HeroLife.Prone?"1":"0",string.Join(",",HeroLife.HeldItems),
            string.Join(";",Covers.OrderBy(x=>x.Id,StringComparer.Ordinal).Select(x=>x.Id+":"+x.X.ToString(CultureInfo.InvariantCulture)+","+x.Y.ToString(CultureInfo.InvariantCulture)))});
        internal const string SourceReferences="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md@04c77b3ddff460219600df2f28bac27d854647af#sha256=5c9f9ab4c9b485546a249637a335f56193dd3d58e58c451f9561c4e330c09a84;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md@5a446dd0dabae096e51f419b5e71756e0169bb3b#sha256=adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/public/class_playtests/manifest.json@c7f68a17b5b38cfc6ab7ce6022eae80ae635b890#sha256=41c044ad787394f0b52a0bf8ec7bb7f4a923c7cbec9a553423fa78c64947c20d;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json@c414a1d9ba2ce37cde89d0ef73265821bb74ac2d#sha256=ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json@88fad6737419c7053d262bdf747fad80fd20f1c4#sha256=21e12af81f191abe52d1e3272ed1f57c6446ed3d4487cafbd5609dff08e56a77;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/XP_ADVANCEMENT_CANON.md@f16bbdf4f352aaccf8e8548e2b993ef338e9c05d#sha256=f9c92adc2444f37bf0cabc0baabce4e37ab58781f0959bdce178c2266c8ebf01;"
            +"Engine:docs/unity/CHARACTER_ADVANCEMENT_RULE_DECISIONS.md@3a8cdfcf83072f02a9b08fa457d354e42f4ac12b#sha256=6a53f8cfb9ac6e197c38b4b73c082f36bfbc8f4791893e8ca0abd97b8f3d41e9";
        internal string BindFingerprint(string prior)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.soldier-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+Key
                +"|sources="+SourceReferences))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
    }

    public static class CharacterAdvancementRules
    {
        private static bool EmptyCommand(Command c)=>c.Inventory==null&&c.Combat==null&&c.X==0&&c.Y==0;
        private static string FeatureOne(string a,string b)=>string.CompareOrdinal(a,b)<0?a:b;
        private static string FeatureTwo(string a,string b)=>string.CompareOrdinal(a,b)<0?b:a;
        private static bool Busy(Snapshot s,string actor)
            =>s.WorldTraversals.Any(x=>x.ActorId==actor)
                ||s.Crops.SelectMany(x=>x.Tasks).Any(x=>x.WorkerId==actor&&x.Status==CropWorkStatus.Working)
                ||s.FormulaWork.Any(x=>x.WorkerId==actor&&x.Status==FormulaWorkStatus.Working)
                ||s.WaterFills.Any(x=>x.WorkerId==actor&&x.Status==WaterFillStatus.Working)
                ||s.Intakes.Any(x=>x.ActorId==actor&&x.Status==IntakeStatus.Working)
                ||s.RepairWork.Any(x=>x.WorkerId==actor&&x.Status==RepairWorkStatus.Working)
                ||s.ManufacturingOrders.Any(x=>x.WorkerId==actor&&x.Status==ManufacturingStatus.Working)
                ||s.SupplyCacheAttempts.Any(x=>x.ActorId==actor&&x.Status==SupplyCacheAttemptStatus.Working);
        private static void SetRuntime(Snapshot s,CharacterFeatureRuntimeRecord value)
            =>s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Select(x=>x.ActorId==value.ActorId?value:x).ToArray();
        private static CharacterFeatureRuntimeRecord Runtime(Snapshot s,string actor)
            =>s.CharacterFeatureRuntime.SingleOrDefault(x=>x.ActorId==actor);
        internal static void RegularStart(Snapshot s,string actor,int ordinal)
        {
            var before=Runtime(s,actor);if(before==null||ordinal<=before.LastRegularStart)return;
            SetRuntime(s,before.RegularStart(ordinal));
        }
        internal static void TacticalExit(Snapshot s)
            =>s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Select(x=>x.RepositionTurnOrdinal>=0?x.EndTacticalUse():x).ToArray();
        internal static void EndRegularTurn(Snapshot s,string actor,int ordinal)
        {
            var state=Runtime(s,actor);if(state!=null&&state.RepositionTurnOrdinal==ordinal)SetRuntime(s,state.EndTacticalUse());
        }
        internal static string ActivateTacticalReposition(Snapshot s,Command c)
        {
            if(!s.InventoryCombat||s.Encounter==null)return "TacticalRepositionRequiresCombat";
            if(c.Target!=s.Encounter.CurrentTurnId||c.X!=0||c.Y!=0||c.Inventory!=null||c.Combat!=null||c.Advancement!=null)return "InvalidTacticalReposition";
            if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
            if(!ActorLifeRules.CanAct(s,c.Actor))return "ActorCannotAct";
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterAdvancementFixture.TacticalReposition))return "FeatureNotOwned";
            var runtime=Runtime(s,c.Actor);if(runtime==null)return "FeatureRuntimeUnavailable";
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);long speed=TestOnlyClubAttackPolicy.WalkingSpeed(s,c.Actor);
            if(speed==0)return "ZeroSpeedCannotMove";
            if(s.SchemaVersion>=Snapshot.ConditionSchema) {
                var view=TestOnlyClubAttackPolicy.ConditionsFor(s,c.Actor).View();
                if(view.Unaware||!view.PermissionsForLife(ActorLifeRules.Read(life)).VoluntarySpeed)return "ConditionPreventsMovement";
            }
            if(!runtime.BonusActionAvailable)return "BonusActionUnavailable";
            if(runtime.RepositionRechargeRemaining>0)return "TacticalRepositionRecharging";
            if(s.TacticalMoves.Length>=64)return "ContinuationCapacityReached";
            try {SetRuntime(s,runtime.Activate(s.Encounter.TurnOrdinal,speed/2));return null;}
            catch(ArgumentException){return "TacticalRepositionUnavailable";}
        }
        internal static long RepositionBudget(Snapshot s,string actor,int turnOrdinal)
        {
            var state=Runtime(s,actor);return state!=null&&state.RepositionTurnOrdinal==turnOrdinal?state.RepositionBudgetRemaining:0;
        }
        internal static void SpendReposition(Snapshot s,string actor,long cost)
        {
            var state=Runtime(s,actor)??throw new ArgumentException("FeatureRuntimeUnavailable");SetRuntime(s,state.SpendReposition(cost));
        }
        public static int DefensivePositioningBonus(Snapshot s,string actor)
        {
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==actor&&x.FeatureId==CharacterAdvancementFixture.DefensivePositioning))return 0;
            var body=s.Actors.Single(x=>x.Id==actor);
            return s.TacticalCovers.Any(x=>PlanarCombatGeometry.DistanceFeet(new CombatCell(body.X,body.Y),new CombatCell(x.X,x.Y))==5)?1:0;
        }
        public static string Resolve(Snapshot s,Command c)
        {
            if(s.SchemaVersion!=Snapshot.CharacterAdvancementSchema)return "CharacterAdvancementUnsupported";
            if(!EmptyCommand(c))return "InvalidAdvancementCommand";
            var character=s.Characters.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(character==null)return "CharacterNotFound";
            if(c.Kind==CommandKind.AwardCharacterMilestone) {
                if(c.Advancement!=null||c.Target=="")return "InvalidMilestoneAward";
                if(character.Levels.Count!=1||character.Levels[0].ClassName!="Soldier")return "UnsupportedAdvancementPath";
                if(s.CharacterMilestones.Any(x=>x.ActorId==c.Actor&&x.MilestoneId==c.Target))return "MilestoneAlreadyAwarded";
                if(s.CharacterMilestones.Length>=256)return "MilestoneCapacityReached";
                s.CharacterMilestones=s.CharacterMilestones.Concat(new[]{new CharacterMilestoneRecord(c.Target,c.Actor,s.Revision+1)}).ToArray();
                return null;
            }
            if(c.Kind!=CommandKind.AdvanceCharacterLevel||c.Advancement==null||c.Target=="")return "CharacterAdvancementCommandNotImplemented";
            if(character.Levels.Count!=1||character.Levels[0].ClassName!="Soldier")return "UnsupportedAdvancementPath";
            var entitlement=s.CharacterMilestones.SingleOrDefault(x=>x.ActorId==c.Actor&&x.MilestoneId==c.Target);
            if(entitlement==null)return "MilestoneNotAvailable";
            if(entitlement.ConsumedRevision!=0)return "MilestoneAlreadyConsumed";
            if(s.InventoryCombat)return "TacticalControlActive";
            if(TestOnlySharedWorldPolicy.PendingCalendarChoice(s))return "TacticalChoicePending";
            if(s.ManufacturingAdvance!=null)return "ManufacturingChoicePending";
            if(Busy(s,c.Actor))return "CharacterBusy";
            var request=c.Advancement;string first=FeatureOne(request.FeatureOne,request.FeatureTwo),second=FeatureTwo(request.FeatureOne,request.FeatureTwo);
            if(request.FeatureOne==""||request.FeatureTwo==""||request.FeatureOne==request.FeatureTwo)return "IncompleteFeatureSelection";
            if(first!=CharacterAdvancementFixture.DefensivePositioning||second!=CharacterAdvancementFixture.TacticalReposition)return "UnsupportedFeatureSelection";
            if(s.CharacterAdvancements.Length>=128||s.CharacterFeatureGrants.Length>254||s.CharacterHitDice.Length>=1280)return "AdvancementCapacityReached";
            var dice=s.CharacterHitDice.Where(x=>x.ActorId==c.Actor).OrderBy(x=>x.LevelOrdinal).ToArray();
            if(dice.Length!=1||dice[0].LevelOrdinal!=1||dice[0].ClassName!="Soldier"||dice[0].DieSize!=10)return "HitDieLedgerMismatch";
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
            if(life.MaximumHp!=10)return "AdvancementHealthBasisMismatch";
            var levels=character.Levels.Concat(new[]{new CharacterLevelFact("Soldier",6)}).ToArray();
            var hp=PlaytestCharacters.BaseMaximumHp(levels.Select(x=>new CharacterLevelRecord(x.ClassName,x.BaseHp)).ToArray(),character.Abilities[2]);
            long newHp=PlaytestCharacters.ClampAfterCapacityChange(life.Hp,hp.BaseMaximum);
            // No resource or life transition is attached to a capacity increase.
            s.Characters=s.Characters.Select(x=>x.ActorId==c.Actor?new ActorCharacterRecord(x.ActorId,x.ProfileId,x.Abilities,levels):x).ToArray();
            s.Lives=s.Lives.Select(x=>x.ActorId==c.Actor?new ActorLifeRecord(x.ActorId,hp.BaseMaximum,newHp,x.TemporaryHp,x.LinkedInjuries,
                x.Stable,x.Dead,x.UsesDeathSaves,x.DeathSuccesses,x.DeathFailures,x.StableUntil,x.LastDeathTurn,x.Prone,x.HeldItems):x).ToArray();
            s.CharacterMilestones=s.CharacterMilestones.Select(x=>x.ActorId==c.Actor&&x.MilestoneId==c.Target?x.Consume(s.Revision+1):x).ToArray();
            s.CharacterHitDice=s.CharacterHitDice.Concat(new[]{new CharacterHitDieRecord(c.Actor,2,"Soldier",10,false)}).ToArray();
            s.CharacterFeatureGrants=s.CharacterFeatureGrants.Concat(new[]{
                new CharacterFeatureGrantRecord(c.Actor,first,"Soldier",2,c.Target,s.Revision+1),
                new CharacterFeatureGrantRecord(c.Actor,second,"Soldier",2,c.Target,s.Revision+1)
            }).ToArray();
            int lastStart=checked((int)s.WorldIntervals.Single(x=>x.ActorId==c.Actor).LastStart);
            s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Concat(new[]{new CharacterFeatureRuntimeRecord(c.Actor,lastStart)}).ToArray();
            s.CharacterAdvancements=s.CharacterAdvancements.Concat(new[]{new CharacterAdvancementRecord(c.Actor,c.Target,s.Revision+1,1,2,"Soldier",2,6,
                HitPointGainMethod.FixedAverage,life.MaximumHp,hp.BaseMaximum,life.Hp,newHp,first,second)}).ToArray();
            return null;
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly CharacterAdvancementFixture characterAdvancement;
        public TestOnlySharedWorldPolicy(CharacterAdvancementFixture advancement,SharedCombatFixture combat,int walkingSpeed=30,
            ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,(SharedResearchFixture)null,(SharedCraftingFixture)null,(SharedRepairFixture)null,(SharedManufacturingFixture)null,
                (SupplyCacheFixture)null,walkingSpeed,conditions,terrain)
        {
            characterAdvancement=advancement??throw new ArgumentNullException(nameof(advancement));
            if(combat==null)throw new ArgumentNullException(nameof(combat));
            ContentFingerprint=characterAdvancement.BindFingerprint(ContentFingerprint);
        }
        private void InitializeCharacterAdvancement(Snapshot s)
        {
            if(characterAdvancement==null)return;
            s.Characters=s.Characters.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                ?new ActorCharacterRecord(x.ActorId,CharacterAdvancementProfileIds.TestOnlySoldierLevel1,new[]{10,10,10,10,10,10},new[]{new CharacterLevelFact("Soldier",10)}):x).ToArray();
            s.Lives=s.Lives.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?characterAdvancement.HeroLife:x).ToArray();
            s.CharacterHitDice=new[]{new CharacterHitDieRecord(TestOnlyPolicy.ActorId,1,"Soldier",10,characterAdvancement.StartingHitDieSpent)};
            s.TacticalCovers=characterAdvancement.Covers.ToArray();
        }
        private string ResolveCharacterAdvancement(Snapshot s,Command c)=>CharacterAdvancementRules.Resolve(s,c);
    }
}
#endif
