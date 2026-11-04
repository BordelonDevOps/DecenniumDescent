#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit dynamic shot-lane and Strength-save facts for the first complete
    /// Overwatch execution fixture. The authored lane is cardinal and the target remains fixed.</summary>
    public sealed class OverwatchExecutionFixture
    {
        public bool TargetLocationKnown { get; }
        public bool TargetVisible { get; }
        public bool LineOfFireClear { get; }
        public CombatCover TargetCover { get; }
        public int AdditionalStrengthSaveModifier { get; }
        public OverwatchExecutionFixture(bool targetLocationKnown=true,bool targetVisible=true,bool lineOfFireClear=true,
            CombatCover targetCover=CombatCover.None,int additionalStrengthSaveModifier=0)
        {
            if(!Enum.IsDefined(typeof(CombatCover),targetCover)||additionalStrengthSaveModifier< -100||additionalStrengthSaveModifier>100)
                throw new ArgumentException("Invalid authored Overwatch shot/save facts.");
            TargetLocationKnown=targetLocationKnown;TargetVisible=targetVisible;LineOfFireClear=lineOfFireClear;
            TargetCover=targetCover;AdditionalStrengthSaveModifier=additionalStrengthSaveModifier;
        }
        internal string Key=>"overwatch-execution-schema26-v1|known="+(TargetLocationKnown?"1":"0")+"|visible="+(TargetVisible?"1":"0")
            +"|line="+(LineOfFireClear?"1":"0")+"|cover="+(int)TargetCover+"|str-save="+AdditionalStrengthSaveModifier.ToString(CultureInfo.InvariantCulture)
            +"|supported-cells=designation-center-row-or-column-only|triggers=post-completed-enter-or-inside-move|source="+OverwatchFoundationFixture.SoldierSourceRevision
            +"|decision=Engine:docs/unity/OVERWATCH_RULE_DECISIONS.md@1e8cf03e0dde25978aba83d251cfe74266b2687a#sha256=972a722c1fd68f0ad4a7fcef894d06b1d940e75cd9bf2d4293f9b734512b2a43";
        internal string BindFingerprint(string prior)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.ow-execution-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+Key))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
    }

    /// <summary>Explicit visibility fact and first authored fixed footprint for the bounded
    /// Overwatch designation fixture. It is not a general visibility or placement provider.</summary>
    public sealed class OverwatchDesignationFixture
    {
        public int X0 { get; }
        public int Y0 { get; }
        public bool EntireZoneVisible { get; }
        public OverwatchDesignationFixture(int x0=1,int y0=-1,bool entireZoneVisible=true)
        {if(x0>int.MaxValue-2||y0>int.MaxValue-2)throw new ArgumentOutOfRangeException(nameof(x0));X0=x0;Y0=y0;EntireZoneVisible=entireZoneVisible;}
        internal string Key=>"overwatch-designation-schema25-v1|zone="+X0.ToString(CultureInfo.InvariantCulture)+","+Y0.ToString(CultureInfo.InvariantCulture)
            +"|visible="+(EntireZoneVisible?"1":"0")+"|footprint=3x3-five-foot|placement=explicit-full-visible-and-normal-range|source="+OverwatchFoundationFixture.SoldierSourceRevision
            +"|decision=Engine:docs/unity/OVERWATCH_RULE_DECISIONS.md@1e8cf03e0dde25978aba83d251cfe74266b2687a#sha256=972a722c1fd68f0ad4a7fcef894d06b1d940e75cd9bf2d4293f9b734512b2a43";
        internal string BindFingerprint(string prior)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.ow-zone-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+Key))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private OverwatchDesignationFixture overwatchRuntime;
        private OverwatchExecutionFixture overwatchExecution;

        public TestOnlySharedWorldPolicy(OverwatchDesignationFixture runtime,OverwatchFoundationFixture foundation,PeriodicRiderFixture periodic,
            RepeatingCrossbowFixture crossbow,CharacterAdvancementFixture advancement,SharedCombatFixture combat,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(foundation,periodic,advancement,combat,walkingSpeed,conditions,terrain)
        {
            overwatchRuntime=runtime??throw new ArgumentNullException(nameof(runtime));
            if(crossbow==null)throw new ArgumentNullException(nameof(crossbow));
            rangedCombat=crossbow;
            ContentFingerprint=RepeatingCrossbowFixture.BindFingerprint(ContentFingerprint,crossbow);
            ContentFingerprint=overwatchRuntime.BindFingerprint(ContentFingerprint);
        }

        public TestOnlySharedWorldPolicy(OverwatchExecutionFixture execution,OverwatchDesignationFixture runtime,OverwatchFoundationFixture foundation,
            PeriodicRiderFixture periodic,RepeatingCrossbowFixture crossbow,CharacterAdvancementFixture advancement,SharedCombatFixture combat,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(runtime,foundation,periodic,crossbow,advancement,combat,walkingSpeed,conditions,terrain)
        {
            overwatchExecution=execution??throw new ArgumentNullException(nameof(execution));
            ContentFingerprint=overwatchExecution.BindFingerprint(ContentFingerprint);
        }

        private void InitializeOverwatchRuntime(Snapshot s)
        {
            if(overwatchRuntime==null)return;
            if((s.SchemaVersion!=Snapshot.OverwatchSchema&&s.SchemaVersion!=Snapshot.OverwatchExecutionSchema)
                ||(s.SchemaVersion==Snapshot.OverwatchExecutionSchema)!=(overwatchExecution!=null)
                ||overwatchFoundation==null||periodicRider==null||rangedCombat==null
                ||rangedCombat.ShooterId!=TestOnlyPolicy.ActorId)
                throw new ArgumentException("The TEST_ONLY Overwatch designation fixture is incomplete or out of scope.");
            int start=checked((int)s.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).LastStart);
            s.OverwatchIntervals=new[]{new OverwatchIntervalRecord(TestOnlyPolicy.ActorId,start)};
        }

        private static bool ZoneWithinWeaponRange(Snapshot s,string actor,int x0,int y0)
        {
            var body=s.Actors.Single(x=>x.Id==actor);
            for(int x=0;x<3;x++)for(int y=0;y<3;y++)
                if(PlanarCombatGeometry.DistanceFeet(new CombatCell(body.X,body.Y),new CombatCell(checked(x0+x),checked(y0+y)))
                    >RepeatingCrossbowShotRules.NormalRangeFeet)return false;
            return true;
        }

        private static OverwatchIntervalRecord CurrentOverwatchInterval(Snapshot s,string actor)
            =>s.OverwatchIntervals.Where(x=>x.ActorId==actor).OrderByDescending(x=>x.LastRegularStart).FirstOrDefault();

        internal static void OverwatchRegularStart(Snapshot s,string actor,int ordinal,long revision)
        {
            if(s.SchemaVersion<Snapshot.OverwatchSchema)return;
            var before=CurrentOverwatchInterval(s,actor);
            if(before==null||ordinal<=before.LastRegularStart)return;
            s.OverwatchDesignations=s.OverwatchDesignations.Select(x=>x.OwnerId==actor&&x.Status==OverwatchDesignationStatus.Active
                ?x.End(OverwatchDesignationStatus.Expired,revision):x).ToArray();
            s.OverwatchIntervals=s.OverwatchIntervals.Concat(new[]{new OverwatchIntervalRecord(actor,ordinal)}).ToArray();
            int oldestRetained=before.LastRegularStart;
            s.OverwatchDesignations=s.OverwatchDesignations.Where(x=>x.OwnerId!=actor||x.LastRegularStart>=oldestRetained).ToArray();
            s.OverwatchIntervals=s.OverwatchIntervals.Where(x=>x.ActorId!=actor||x.LastRegularStart>=oldestRetained).ToArray();
            if(s.SchemaVersion>=Snapshot.OverwatchExecutionSchema) {
                var retained=s.OverwatchDesignations.Where(x=>x.OwnerId==actor).Select(x=>x.Id).ToHashSet(StringComparer.Ordinal);
                var removed=s.OverwatchOffers.Where(x=>x.OwnerId==actor&&!retained.Contains(x.DesignationId)).Select(x=>x.Id).ToHashSet(StringComparer.Ordinal);
                s.OverwatchOffers=s.OverwatchOffers.Where(x=>!removed.Contains(x.Id)).ToArray();
                s.OverwatchRiderChoices=s.OverwatchRiderChoices.Where(x=>!removed.Contains(x.OfferId)).ToArray();
            }
        }

        private static OverwatchDesignationRecord ActiveOverwatchZone(Snapshot s,string actor,int interval)
            =>s.OverwatchDesignations.SingleOrDefault(x=>x.OwnerId==actor&&x.LastRegularStart==interval&&x.Status==OverwatchDesignationStatus.Active);

        private string ResolveOverwatchDesignation(Snapshot s,Command c)
        {
            if(overwatchRuntime==null||s.SchemaVersion<Snapshot.OverwatchSchema)return "OverwatchDesignationNotImplemented";
            if(!s.InventoryCombat||s.Encounter==null)return "OverwatchRequiresTacticalCombat";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.Target!=s.Encounter.CurrentTurnId)return "InvalidOverwatchDesignation";
            if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
            if(TestOnlySharedWorldPolicy.PendingCalendarChoice(s))return "TacticalChoicePending";
            if(s.ManufacturingAdvance!=null)return "ManufacturingChoicePending";
            if(!ActorLifeRules.CanAct(s,c.Actor))return "ActorCannotAct";
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterFeatureIds.Overwatch))return "FeatureNotOwned";
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
            if(!View(s,c.Actor).PermissionsForLife(ActorLifeRules.Read(life)).BonusAction)return "ConditionPreventsBonusAction";
            var interval=CurrentOverwatchInterval(s,c.Actor);
            if(interval==null||interval.LastRegularStart!=s.Encounter.TurnOrdinal)return "OverwatchIntervalUnavailable";
            if(c.X!=overwatchRuntime.X0||c.Y!=overwatchRuntime.Y0)return "UnsupportedOverwatchPlacement";
            if(!ZoneWithinWeaponRange(s,c.Actor,c.X,c.Y))return "OverwatchZoneOutOfRange";
            if(!overwatchRuntime.EntireZoneVisible)return "OverwatchZoneNotVisible";
            var weapon=s.RepeatingCrossbows.SingleOrDefault(x=>x.Id==RepeatingCrossbowFixture.WeaponId);
            if(weapon==null||weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor)return "OverwatchWeaponUnavailable";
            if(s.OverwatchDesignations.Length>=OverwatchValidation.MaxDesignations)return "OverwatchHistoryCapacityReached";
            if(!CharacterAdvancementRules.BonusActionAvailable(s,c.Actor))return "BonusActionUnavailable";

            // All source, resource and fixture checks precede spending. A second zone replaces
            // the first while the interval-owned shot status remains untouched.
            if(!CharacterAdvancementRules.SpendBonusAction(s,c.Actor))return "BonusActionUnavailable";
            var current=ActiveOverwatchZone(s,c.Actor,interval.LastRegularStart);
            if(current!=null)s.OverwatchDesignations=s.OverwatchDesignations.Select(x=>x.Id==current.Id
                ?x.End(OverwatchDesignationStatus.Replaced,s.Revision+1):x).ToArray();
            string id="overwatch.zone."+s.Revision.ToString(CultureInfo.InvariantCulture);
            s.OverwatchDesignations=s.OverwatchDesignations.Concat(new[]{new OverwatchDesignationRecord(id,c.Actor,interval.LastRegularStart,c.X,c.Y,s.Revision+1)}).ToArray();
            return null;
        }
    }
}
#endif
