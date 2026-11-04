#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Bounded combined crop/inventory host. Supplies capable Medium STR10 actors, usable hands,
    /// an open pouch verified to fit the entire initial two-pound ration bundle, prepared plot
    /// and a fixed four-pint waterskin (one-pound tare). Harvested greens have no authored volume/shape here.
    /// Food is ready ordinary bulk; the waterskin can be drunk from but vessel transfer/filling is unsupported.
    /// No hazards, scheduled combat entries or other timed systems exist in this fixture.</summary>
    public sealed class TestOnlyInventoryPolicy : ICommandPolicy
    {
        public const string FoodId="TEST_ONLY.ready-rations",WaterId="TEST_ONLY.ready-water";
        public const string FoodUnit="TEST_ONLY.ration-pound",WaterUnit="prototype.potable-water.pint";
        private readonly long freshSeconds;
        private readonly TestOnlyCropPolicy crops=new TestOnlyCropPolicy();
        public TestOnlyInventoryPolicy(long remainingFoodFreshness=2592000)
        {if(remainingFoodFreshness<0)throw new ArgumentOutOfRangeException(nameof(remainingFoodFreshness));freshSeconds=remainingFoodFreshness;}
        public bool TestOnly=>true;
        public string ContentFingerprint=>"TEST_ONLY.inventory-v1-f"+freshSeconds.ToString(CultureInfo.InvariantCulture);
        public static Authority Host()=>new Authority("TEST_ONLY.host",new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},true,true,
            new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId});
        public Snapshot Initial()
        {
            var s=crops.Initial();s.SchemaVersion=Snapshot.InventorySchema;s.ContentFingerprint=ContentFingerprint;
            s.Work=new WorkLedger(s.Work.Lots.Concat(new[]{new ResourceLot(FoodId,FoodUnit,2,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId),
                new ResourceLot(WaterId,WaterUnit,4,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId)}));
            s.InventoryLots=s.Work.Lots.Select(x=>new InventoryLotRecord(x.Id,"",x.CustodianId,x.Amount,default,
                x.Id==FoodId?NutritionKind.FoodPounds:x.Id==WaterId?NutritionKind.WaterPints:NutritionKind.None,
                x.Id==FoodId?new RuleTime(freshSeconds):(RuleTime?)null,x.Id==FoodId||x.Id==WaterId?InventoryAccess.Ready:InventoryAccess.Ground)).ToArray();
            return s;
        }
        private static bool Near(ActorState a,ActorState b)=>Math.Abs((long)a.X-b.X)+Math.Abs((long)a.Y-b.Y)<=1;
        private static bool AtPlot(ActorState a)=>Math.Abs((long)a.X-3)+Math.Abs((long)a.Y-3)<=1;
        private static bool Accessible(Snapshot s,string actor,InventoryLotRecord item,ResourceLot lot)=>item.Access==InventoryAccess.Ground
            ?lot.LocationId==TestOnlyCropPolicy.PlotId&&AtPlot(s.Actors.Single(a=>a.Id==actor))
            :lot.LocationId==actor&&lot.CustodianId==actor;
        private static bool FitsSuppliedPouch(Snapshot s,InventoryLotRecord item)
        {
            // The fixture verifies the complete initial ration bundle fits its pouch. Descendants are
            // portions of that same finite bundle, not extra contents. It supplies no greens volume or
            // universal food density; do not infer fit from carrying pounds alone.
            while(item.ParentId!="")item=s.InventoryLots.Single(x=>x.LotId==item.ParentId);
            return item.LotId==FoodId;
        }
        public static BurdenTotals CarriedBurden(Snapshot s,string actor)
        {
            if(!s.Actors.Any(x=>x.Id==actor))throw new ArgumentException("Unknown fixture carrier.");
            // Each actor's fixed pouch weighs one pound. The actor's fixed skin also retains its
            // one-pound tare when empty. These host fixtures are not transferable equipment records.
            var pounds=RuleQuantity.Sum(s.Work.Lots.Where(x=>x.LocationId==actor||s.Vessels.Any(v=>v.Id==x.LocationId&&v.LocationId==actor)).Select(x=>x.Amount))
                +new RuleQuantity(1)+(s.SchemaVersion>=Snapshot.VesselSchema
                    ?RuleQuantity.Sum(s.Vessels.Where(v=>v.LocationId==actor).Select(v=>WaterFilling.Tare(v.Profile)))
                    :actor==TestOnlyPolicy.ActorId?new RuleQuantity(1):default);
            pounds+=new RuleQuantity(2L*s.Clubs.Count(w=>w.HeldBy==actor));
            return new BurdenTotals(pounds,pounds.Scale(1,10),true);
        }
        private static bool Capacity(Snapshot s,string actor,RuleQuantity additional)
        {
            var burden=CarriedBurden(s,actor);var pounds=burden.Pounds.Value+additional;
            return PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium,10),new BurdenTotals(pounds,pounds.Scale(1,10),true))==true;
        }
        public string Resolve(Snapshot s,Command c)
        {
            bool request=c.Kind==CommandKind.PortionInventory||c.Kind==CommandKind.HandleInventory||c.Kind==CommandKind.StartIntake;
            if(request!=(c.Inventory!=null))return "UnexpectedInventoryPayload";
            if(c.Kind==CommandKind.AdvanceClock) {
                if(s.InventoryCombat)return "EncounterClockNotImplemented";
                if(c.Target!=""||c.X<1||c.Y<1)return "InvalidInventoryAdvance";
                OrdinaryInventory.AdvanceTo(s,CampGreens.Add(s.RuleClock,new RuleTime(c.X,c.Y)));return null;
            }
            if(c.Kind==CommandKind.EnterInventoryCombat) {
                if(s.InventoryCombat||c.Target!=""||c.X!=0||c.Y!=0)return "InvalidCombatEntry";
                foreach(var job in s.Intakes.Where(x=>x.Status==IntakeStatus.Working).ToArray())OrdinaryInventory.Interrupt(s,job,IntakeStatus.CombatInterrupted);
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                s.InventoryCombat=true;s.InventoryTurnActor=c.Actor;s.InventoryInteractions=0;return null;
            }
            if(c.Kind==CommandKind.InterruptIntake) {
                if(c.X!=0||c.Y!=0)return "InvalidIntakeRequest";
                var job=s.Intakes.SingleOrDefault(x=>x.Id==c.Target&&x.ActorId==c.Actor&&x.Status==IntakeStatus.Working);
                if(job==null)return "NoActiveIntake";
                OrdinaryInventory.Interrupt(s,job,IntakeStatus.Interrupted);return null;
            }
            if(!request) {
                if(s.InventoryCombat)return "EncounterCommandNotImplemented";
                if((c.Kind==CommandKind.Move||c.Kind==CommandKind.Interact)&&OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                // Synthetic token chest is not a physical inventory closure or a free ready-storage operation.
                return crops.Resolve(s,c);
            }
            if(c.X!=0||c.Y!=0||c.Inventory.Amount==default)return "InvalidInventoryRequest";
            var item=s.InventoryLots.SingleOrDefault(x=>x.LotId==c.Target);
            if(item==null)return "UnknownInventoryLot";
            var lot=s.Work.Lots.Single(x=>x.Id==item.LotId);
            if(item.Nutrition==NutritionKind.None)return "UnsupportedInventoryProfile";
            if(!Accessible(s,c.Actor,item,lot))return "InventoryOutOfReach";
            if(c.Inventory.Amount>s.Work.AvailableAmount(lot.Id))return "InventoryQuantityUnavailable";
            if(c.Kind==CommandKind.PortionInventory) {
                if(c.Inventory.Destination!=""||c.Inventory.Handling!=HandlingKind.Pickup)return "InvalidPortionRequest";
                OrdinaryInventory.Descendant(s,lot.Id,OrdinaryInventory.Identity(s,"lot"),c.Inventory.Amount,lot.LocationId,lot.CustodianId,item.Access);return null;
            }
            if(c.Kind==CommandKind.StartIntake) {
                if(c.Inventory.Destination!=""||c.Inventory.Handling!=HandlingKind.Pickup)return "InvalidIntakeRequest";
                if(s.InventoryCombat)return "TacticalIntakeNotAdopted";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(item.Access!=InventoryAccess.Ready||lot.CustodianId!=c.Actor||lot.LocationId!=c.Actor)return "IntakeRequiresReadyCustody";
                if(!OrdinaryInventory.Fresh(s,item))return "IntakeExpired";
                OrdinaryInventory.StartIntake(s,c.Actor,lot.Id,c.Inventory.Amount);return null;
            }
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(item.Nutrition!=NutritionKind.FoodPounds)return "VesselProcedureNotImplemented";
            string location=c.Actor,custodian=c.Actor;InventoryAccess access=InventoryAccess.Ready;
            switch(c.Inventory.Handling) {
                case HandlingKind.Pickup:
                    if(c.Inventory.Destination!=""||item.Access!=InventoryAccess.Ground)return "InvalidPickup";break;
                case HandlingKind.Drop:
                    if(c.Inventory.Destination!=""||item.Access!=InventoryAccess.Ready||!AtPlot(s.Actors.Single(x=>x.Id==c.Actor)))return "InvalidDrop";
                    location=TestOnlyCropPolicy.PlotId;access=InventoryAccess.Ground;break;
                case HandlingKind.Stow:
                    if(c.Inventory.Destination!=""||item.Access!=InventoryAccess.Ready)return "InvalidStow";
                    if(!FitsSuppliedPouch(s,item))return "ContainerFitNotEstablished";
                    access=InventoryAccess.Stowed;break;
                case HandlingKind.Retrieve:
                    if(c.Inventory.Destination!=""||item.Access!=InventoryAccess.Stowed)return "InvalidRetrieval";break;
                case HandlingKind.Handover:
                    var receiver=s.Actors.SingleOrDefault(x=>x.Id==c.Inventory.Destination);
                    if(item.Access!=InventoryAccess.Ready||receiver==null||receiver.Id==c.Actor
                        ||!Near(s.Actors.Single(x=>x.Id==c.Actor),receiver))return "InvalidHandover";
                    if(s.WaterFills.Any(j=>j.WorkerId==receiver.Id&&j.Status==WaterFillStatus.Working))return "RecipientHandsReserved";
                    location=receiver.Id;custodian=receiver.Id;break;
                default:return "InvalidHandling";
            }
            if(access!=InventoryAccess.Ground&&!Capacity(s,custodian,lot.LocationId==location?default:c.Inventory.Amount))return "CarryingCapacityExceeded";
            if(s.InventoryCombat&&(s.InventoryTurnActor!=c.Actor||s.InventoryInteractions>=2))return "InteractionBudgetUnavailable";
            OrdinaryInventory.Handle(s,c,location,custodian,access);return null;
        }
        public string ValidateState(Snapshot s)=>ValidateInventoryState(s,false);
        internal string ValidateInventoryState(Snapshot s,bool filling,bool movable=false,bool encounter=false,bool actorLife=false,bool ordinaryAttack=false,bool posture=false,bool tactical=false)
        {
            try {
                if(s.SchemaVersion!=(tactical?Snapshot.TacticalMovementSchema:posture?Snapshot.PostureSchema:ordinaryAttack?Snapshot.ClubAttackSchema:actorLife?Snapshot.ActorLifeSchema:encounter?Snapshot.EncounterSchema:movable?Snapshot.MovableVesselSchema:filling?Snapshot.VesselSchema:Snapshot.InventorySchema))return "WrongInventorySchema";
                string error=crops.ValidateCropState(s,true);if(error!=null)return error;
                error=OrdinaryInventory.Validate(s);if(error!=null)return error;
                var roots=s.InventoryLots.Where(x=>x.ParentId=="").ToArray();
                if(roots.Length!=(filling?5:4)+s.CropFood.Length)return "InvalidInventoryRoots";
                foreach(var root in roots) {
                    var lot=s.Work.Lots.Single(x=>x.Id==root.LotId);long amount;string unit,owner,location;NutritionKind kind;RuleTime? fresh=null;RuleTime created=default;InventoryAccess access=InventoryAccess.Ground;
                    if(root.LotId==TestOnlyCropPolicy.SeedLotId){amount=8;unit=CampGreens.SeedUnit;kind=NutritionKind.None;owner=TestOnlyPolicy.CompanionId;location=TestOnlyCropPolicy.PlotId;}
                    else if(root.LotId==TestOnlyCropPolicy.WaterLotId){amount=512;unit=CampGreens.WaterUnit;kind=NutritionKind.None;owner=TestOnlyPolicy.CompanionId;location=TestOnlyCropPolicy.PlotId;}
                    else if(root.LotId==FoodId){amount=2;unit=FoodUnit;kind=NutritionKind.FoodPounds;fresh=new RuleTime(freshSeconds);owner=TestOnlyPolicy.ActorId;location=owner;access=InventoryAccess.Ready;}
                    else if(root.LotId==WaterId){amount=4;unit=WaterUnit;kind=NutritionKind.WaterPints;owner=TestOnlyPolicy.ActorId;location=filling?TestOnlyFillingPolicy.ActorSkinId:owner;access=InventoryAccess.Ready;}
                    else if(filling&&root.LotId==TestOnlyFillingPolicy.SupplyId){amount=32;unit=WaterUnit;kind=NutritionKind.WaterPints;owner=TestOnlyPolicy.CompanionId;location=TestOnlyCropPolicy.PlotId;}
                    else {
                        var food=s.CropFood.Single(f=>f.LotId==root.LotId);var crop=s.Crops.Single(c=>c.Id==food.BatchId);
                        amount=8;unit=CampGreens.FoodUnit;kind=NutritionKind.FoodPounds;fresh=food.FreshUntil;created=crop.ClosedAt.Value;owner=crop.OwnerId;location=crop.PlotId;
                    }
                    string expectedCustodian=owner;
                    if(movable&&root.LotId==WaterId) {
                        var container=s.Vessels.Single(v=>v.Id==location);expectedCustodian=container.CustodianId;
                        access=container.LocationId==TestOnlyCropPolicy.PlotId?InventoryAccess.Ground:InventoryAccess.Ready;
                    }
                    if(root.CreatedAmount!=new RuleQuantity(amount)||lot.UnitId!=unit||root.OwnerId!=owner||root.Nutrition!=kind
                        ||root.FreshUntil!=fresh||root.CreatedAt!=created||root.Access!=access||lot.LocationId!=location||lot.CustodianId!=expectedCustodian)return "InvalidInventoryRoot";
                }
                foreach(var item in s.InventoryLots) {
                    var lot=s.Work.Lots.Single(x=>x.Id==item.LotId);
                    if(item.Access==InventoryAccess.Stowed&&!FitsSuppliedPouch(s,item))return "ContainerFitNotEstablished";
                    var containing=s.Vessels.SingleOrDefault(v=>v.Id==lot.LocationId);
                    if(containing!=null) {
                        if(item.Nutrition!=NutritionKind.WaterPints||lot.CustodianId!=containing.CustodianId
                            ||item.Access!=(containing.LocationId==TestOnlyCropPolicy.PlotId?InventoryAccess.Ground:InventoryAccess.Ready))return "InvalidContainedAccess";
                    } else if(item.Access==InventoryAccess.Ground?lot.LocationId!=TestOnlyCropPolicy.PlotId
                        :!s.Actors.Any(a=>a.Id==lot.LocationId&&a.Id==lot.CustodianId))return "InvalidInventoryLocation";
                    if(item.ParentId!="") {
                        var parent=s.InventoryLots.Single(x=>x.LotId==item.ParentId);var parentLot=s.Work.Lots.Single(x=>x.Id==parent.LotId);
                        var moves=s.Handling.Where(x=>x.ChildId==item.LotId).ToArray();
                        if(moves.Length>1)return "DuplicatePhysicalHandling";
                        if(moves.Length==0&&!s.WaterFills.Any(j=>j.Status==WaterFillStatus.Complete&&j.OutputLotId==item.LotId)&&(item.Access!=parent.Access||lot.LocationId!=parentLot.LocationId||lot.CustodianId!=parentLot.CustodianId))return "UnrecordedInventoryMovement";
                        if(moves.Length!=0) {
                            var move=moves[0];bool sourceHeld=parentLot.LocationId==move.ActorId&&parentLot.CustodianId==move.ActorId;
                            bool heldHere=lot.LocationId==move.ActorId&&lot.CustodianId==move.ActorId;
                            bool valid=move.Kind==HandlingKind.Pickup?parent.Access==InventoryAccess.Ground&&item.Access==InventoryAccess.Ready&&heldHere
                                :move.Kind==HandlingKind.Drop?parent.Access==InventoryAccess.Ready&&sourceHeld&&item.Access==InventoryAccess.Ground&&lot.CustodianId==move.ActorId
                                :move.Kind==HandlingKind.Stow?parent.Access==InventoryAccess.Ready&&sourceHeld&&item.Access==InventoryAccess.Stowed&&heldHere
                                :move.Kind==HandlingKind.Retrieve?parent.Access==InventoryAccess.Stowed&&sourceHeld&&item.Access==InventoryAccess.Ready&&heldHere
                                :parent.Access==InventoryAccess.Ready&&sourceHeld&&item.Access==InventoryAccess.Ready&&lot.CustodianId!=move.ActorId;
                            if(item.Nutrition!=NutritionKind.FoodPounds||!valid)return "InvalidHandlingTransition";
                        }
                    }
                }
                if(s.Actors.Any(a=>!Capacity(s,a.Id,default)))return "InvalidCarriedCapacity";
                return null;
            } catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException) {return "InvalidInventoryState";}
        }
    }
}
#endif
