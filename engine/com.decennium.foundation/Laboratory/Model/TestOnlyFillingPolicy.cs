#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Stable water arrangements only: a finite clean pool at the prepared plot, a skin carried
    /// by each actor and one supported ordinary flask at the plot. Individual openings admit one active
    /// worker at a time. Source pool access supports both workers. Explicit schema6 adds safe intact
    /// movement using supplied access/hand capabilities, not a general equipment/hand-slot model.
    /// Hazards, contamination and tactical filling remain unsupported.</summary>
    public sealed class TestOnlyFillingPolicy : ICommandPolicy
    {
        public const string ActorSkinId="TEST_ONLY.actor-skin",CompanionSkinId="TEST_ONLY.companion-skin",FlaskId="TEST_ONLY.plot-flask",SupplyId="TEST_ONLY.clean-pool";
        private readonly TestOnlyInventoryPolicy inventory;
        private readonly int actorHands,companionHands;
        private readonly bool movable;
        public TestOnlyFillingPolicy(int actorUsableHands=2,int companionUsableHands=2,long remainingFoodFreshness=2592000,
            bool movableVessels=false,TestOnlyCropPolicy cropPolicy=null)
        {
            if(actorUsableHands<0||actorUsableHands>2||companionUsableHands<0||companionUsableHands>2)throw new ArgumentOutOfRangeException(nameof(actorUsableHands));
            movable=movableVessels;actorHands=actorUsableHands;companionHands=companionUsableHands;inventory=new TestOnlyInventoryPolicy(remainingFoodFreshness,cropPolicy);
        }
        public bool TestOnly=>true;
        public string ContentFingerprint {
            get {
                string prefix=(movable?"TEST_ONLY.movable-v1-":"TEST_ONLY.filling-v1-")
                    +actorHands.ToString(CultureInfo.InvariantCulture)+"-"+companionHands.ToString(CultureInfo.InvariantCulture)+"-";
                // Keep every historical filling fingerprint whose inventory child used the
                // original food-freshness identity. Hash only newly parameterized crop profiles.
                if(inventory.ContentFingerprint.StartsWith("TEST_ONLY.inventory-v1-f",StringComparison.Ordinal))
                    return prefix+inventory.ContentFingerprint;
                string key=(movable?"movable":"filling")+"|actorHands="+actorHands.ToString(CultureInfo.InvariantCulture)
                    +"|companionHands="+companionHands.ToString(CultureInfo.InvariantCulture)+"|inventory="+inventory.ContentFingerprint;
                using(var sha=SHA256.Create())
                    return (movable?"TEST_ONLY.movable-v1-c":"TEST_ONLY.filling-v1-c")
                        +string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
            }
        }
        public static Authority Host()=>TestOnlyInventoryPolicy.Host();
        private int Hands(string actor)=>actor==TestOnlyPolicy.ActorId?actorHands:companionHands;
        private static WaterVesselRecord[] InitialVessels()=>new[]{
            new WaterVesselRecord(ActorSkinId,WaterVesselProfile.Waterskin,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId),
            new WaterVesselRecord(CompanionSkinId,WaterVesselProfile.Waterskin,TestOnlyPolicy.CompanionId,TestOnlyPolicy.CompanionId,TestOnlyPolicy.CompanionId),
            new WaterVesselRecord(FlaskId,WaterVesselProfile.OrdinaryFlask,TestOnlyPolicy.CompanionId,TestOnlyCropPolicy.PlotId,TestOnlyPolicy.CompanionId)};
        public Snapshot Initial()
        {
            var s=inventory.Initial();s.SchemaVersion=movable?Snapshot.MovableVesselSchema:Snapshot.VesselSchema;s.ContentFingerprint=ContentFingerprint;s.Vessels=InitialVessels();
            s.Work=new WorkLedger(s.Work.Lots.Select(x=>x.Id==TestOnlyInventoryPolicy.WaterId?new ResourceLot(x.Id,x.UnitId,x.Amount,ActorSkinId,x.CustodianId):x)
                .Concat(new[]{new ResourceLot(SupplyId,TestOnlyInventoryPolicy.WaterUnit,32,TestOnlyCropPolicy.PlotId,TestOnlyPolicy.CompanionId)}));
            s.InventoryLots=s.InventoryLots.Concat(new[]{new InventoryLotRecord(SupplyId,"",TestOnlyPolicy.CompanionId,new RuleQuantity(32),default,NutritionKind.WaterPints,null,InventoryAccess.Ground)}).ToArray();
            s.VesselContents=new[]{new VesselContentRecord(TestOnlyInventoryPolicy.WaterId,ActorSkinId)};return s;
        }
        public string Resolve(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.HandleVessel)return movable?VesselHandling.Resolve(s,c,Hands):"VesselMovementNotSupported";
            if(c.Kind==CommandKind.EnterInventoryCombat&&s.WaterFills.Any(j=>j.Pending))return "PendingFillEncounterTransitionUnsupported";
            if(c.Kind==CommandKind.StartWaterFill) {
                if(s.InventoryCombat)return "TacticalFillingUnsupported";
                if(c.Inventory==null||c.Inventory.Amount==default||c.Inventory.Destination==""||c.Inventory.Handling!=HandlingKind.Pickup||c.X!=0||c.Y!=0)return "InvalidFillRequest";
                if(Hands(c.Actor)<2)return "TwoHandsRequired";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                string error=WaterFilling.Prerequisite(s,c.Actor,c.Target,c.Inventory.Destination,c.Inventory.Amount);if(error!=null)return error;
                if(c.Inventory.Amount>s.Work.AvailableAmount(c.Target))return "FillSourceReservedOrInsufficient";
                if(c.Inventory.Amount>WaterFilling.FreeCapacity(s,c.Inventory.Destination))return "FillCapacityUnavailable";
                WaterFilling.Start(s,c.Actor,c.Target,c.Inventory.Destination,c.Inventory.Amount);return null;
            }
            if(c.Kind==CommandKind.PauseWaterFill||c.Kind==CommandKind.ResumeWaterFill||c.Kind==CommandKind.CancelWaterFill) {
                if(c.Inventory!=null||c.X!=0||c.Y!=0)return "InvalidFillRequest";
                var job=s.WaterFills.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);if(job==null)return "UnknownWorkerFill";
                if(c.Kind==CommandKind.PauseWaterFill) {
                    if(job.Status!=WaterFillStatus.Working)return "FillNotWorking";WaterFilling.Pause(s,job);return null;
                }
                if(c.Kind==CommandKind.CancelWaterFill) {
                    if(!job.Pending)return "FillAlreadyTerminal";WaterFilling.Cancel(s,job);return null;
                }
                if(s.InventoryCombat)return "TacticalFillingUnsupported";
                if(job.Status!=WaterFillStatus.Paused)return "FillNotPaused";
                if(Hands(c.Actor)<2)return "TwoHandsRequired";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                string error=WaterFilling.Prerequisite(s,c.Actor,job.SourceLotId,job.DestinationId,job.Amount,job.Id);if(error!=null)return error;
                WaterFilling.Resume(s,job);return null;
            }
            if(c.Kind==CommandKind.PortionInventory||c.Kind==CommandKind.StartIntake) {
                var item=s.InventoryLots.SingleOrDefault(x=>x.LotId==c.Target);
                if(item!=null&&item.Nutrition==NutritionKind.WaterPints) {
                    if(c.Inventory==null||c.Inventory.Amount==default||c.Inventory.Destination!=""||c.Inventory.Handling!=HandlingKind.Pickup||c.X!=0||c.Y!=0)return "InvalidInventoryRequest";
                    var lot=s.Work.Lots.Single(x=>x.Id==c.Target);
                    if(!WaterFilling.Accessible(s,c.Actor,lot))return "InventoryOutOfReach";
                    if(c.Inventory.Amount>s.Work.AvailableAmount(lot.Id))return "InventoryQuantityUnavailable";
                    if(c.Kind==CommandKind.PortionInventory) {
                        OrdinaryInventory.Descendant(s,lot.Id,OrdinaryInventory.Identity(s,"lot"),c.Inventory.Amount,lot.LocationId,lot.CustodianId,item.Access);return null;
                    }
                    if(s.InventoryCombat)return "TacticalIntakeNotAdopted";
                    if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                    if(!WaterFilling.ReadyForIntake(s,c.Actor,item,lot))return "IntakeRequiresReadyCustody";
                    OrdinaryInventory.StartIntake(s,c.Actor,lot.Id,c.Inventory.Amount);return null;
                }
            }
            return inventory.Resolve(s,c);
        }
        public string ValidateState(Snapshot s)=>ValidateFillingState(s,false);
        internal string ValidateFillingState(Snapshot s,bool encounter,bool actorLife=false,bool ordinaryAttack=false,bool posture=false,bool tactical=false,bool conditions=false)
        {
            try {
                var expected=InitialVessels();
                if(!movable&&(s.Vessels.Length!=expected.Length||expected.Any(e=>!s.Vessels.Any(v=>v.Id==e.Id&&v.Profile==e.Profile&&v.OwnerId==e.OwnerId
                    &&v.LocationId==e.LocationId&&v.CustodianId==e.CustodianId))))return "InvalidFixtureVessels";
                if(s.WaterFills.Any(j=>Hands(j.WorkerId)<2))return "InvalidFillingHands";
                string error=movable?VesselHandling.Validate(s,expected,Hands):null;
                return error??inventory.ValidateInventoryState(s,true,movable,encounter,actorLife,ordinaryAttack,posture,tactical,conditions)??WaterFilling.Validate(s);
            } catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException){return "InvalidFillingState";}
        }
    }
}
#endif
