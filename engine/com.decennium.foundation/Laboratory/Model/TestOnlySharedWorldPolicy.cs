#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>First connected exploration/management dispatcher. One persistent world, exact
    /// partial positions and ordinary interval spending; calendar creation is not combat entry.
    /// The fixed two-actor calendar excludes the remote companion at the prepared plot.
    /// Optional explicit combat and research fixtures extend the same dispatcher.</summary>
    public sealed partial class TestOnlySharedWorldPolicy : ICommandPolicy, ICommandInventoryClaims
    {
        private readonly TestOnlyClubAttackPolicy bodies;
        private readonly TestOnlyFillingPolicy inventory = new TestOnlyFillingPolicy(movableVessels: true);
        private readonly TacticalCombatFixture terrain;
        private readonly ConditionCombatFixture conditions;
        private readonly SharedCombatFixture connectedCombat;
        private readonly SupplyCacheFixture supplyCache;
        private SharedFishingTrapFixture fishingTrap;
        private SharedFishingTrapFixture[] fishingTrapProfiles = Array.Empty<SharedFishingTrapFixture>();
        private bool fishingTrapLegacy;
        private bool fishingTrapBaitOnly;
        private bool expeditionAssignmentsEnabled;
        private bool offCalendarActivityEnabled;
        private TestOnlyContentManifest contentManifest;
        public bool TestOnly => true;
        public string ContentFingerprint { get; private set; }
        public TestOnlySharedWorldPolicy(int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,(SharedResearchFixture)null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,research,null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,SharedCraftingFixture crafting,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,SharedCraftingFixture crafting,SharedRepairFixture repair,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,repair,null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,SharedCraftingFixture crafting,SharedRepairFixture repair,SharedManufacturingFixture manufacturing,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,repair,manufacturing,null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,SharedCraftingFixture crafting,SharedRepairFixture repair,SharedManufacturingFixture manufacturing,SupplyCacheFixture supplyCache,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,repair,manufacturing,supplyCache,walkingSpeed,conditions,terrain,null) { }
        private TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,SharedCraftingFixture crafting,
            SharedRepairFixture repair,SharedManufacturingFixture manufacturing,SupplyCacheFixture supplyCache,int walkingSpeed,
            ConditionCombatFixture conditions,TacticalTerrainCell[] terrain,SharedWorldConfiguration scenario)
        {
            worldConfiguration=scenario;
            connectedCombat=combat;
            this.supplyCache=supplyCache;
            this.research=research;
            this.crafting=crafting;
            this.repair=repair;
            this.manufacturing=manufacturing;
            if(manufacturing!=null&&(repair==null||research==null||research.WorkerId!=TestOnlyPolicy.CompanionId||research.RecipeId!=manufacturing.RecipeId))throw new ArgumentException("Manufacturing requires matching selected repair and formula fixtures.");
            if(repair!=null&&crafting==null)throw new ArgumentException("Repair requires the explicit physical crafting fixture.");
            if(crafting!=null&&combat==null)throw new ArgumentException("Crafting consequences require the explicit calendar host.");
            if(research!=null&&combat==null)throw new ArgumentException("Research requires the explicit connected calendar host.");
            this.conditions = conditions ?? new ConditionCombatFixture();
            this.terrain = new TacticalCombatFixture(new AdditionalTacticalActor(4, combat==null?4:0, walkingSpeed,combat?.EnemyHp??26), terrain);
            bodies = new TestOnlyClubAttackPolicy(actorHp:crafting?.HeroHp??26,companionHp:crafting?.CompanionHp??26,actorBaseWalkingSpeed: walkingSpeed, companionBaseWalkingSpeed: walkingSpeed,
                tactical: this.terrain, conditions: this.conditions,seed:combat?.Seed??1,
                deferredConditionTargets:scenario?.Actors.Select(x=>x.Id).ToArray());
            ContentFingerprint = (combat==null?"TEST_ONLY.shared-v1-":"TEST_ONLY.connected-v1-") + bodies.ContentFingerprint.Substring("TEST_ONLY.club-v1-".Length);
            if(research!=null)ContentFingerprint=ResearchFingerprint(ContentFingerprint,research);
            if(crafting!=null)ContentFingerprint=CraftingFingerprint(ContentFingerprint,crafting);
            if(repair!=null)ContentFingerprint=RepairFingerprint(ContentFingerprint,repair);
            if(manufacturing!=null)ContentFingerprint=ManufacturingFingerprint(ContentFingerprint,manufacturing);
            if(supplyCache!=null)ContentFingerprint=SupplyCacheFingerprint(ContentFingerprint,supplyCache);
        }
        public TestOnlySharedWorldPolicy(PortableKitFixture portableKit,SharedCombatFixture combat,SupplyCacheFixture supplyCache,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,null,null,null,null,supplyCache,walkingSpeed,conditions,terrain)
        {
            this.portableKit=portableKit??throw new ArgumentNullException(nameof(portableKit));
            if(combat==null||supplyCache==null||!supplyCache.HasTools||supplyCache.HasKey)
                throw new ArgumentException("Portable kit requires the selected cache and tools, and rejects an unsourced-mass key fixture.");
            ContentFingerprint=PortableEquipmentRules.Fingerprint(ContentFingerprint,portableKit);
        }
        /// <summary>Source-resolved opt-in profile. The legacy schema20 constructor above retains
        /// its original content fingerprint and saved-profile compatibility.</summary>
        public TestOnlySharedWorldPolicy(TestOnlyContentManifest manifest,PortableKitFixture portableKit,SharedCombatFixture combat,SupplyCacheFixture supplyCache,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(portableKit,combat,supplyCache,walkingSpeed,conditions,terrain)
        {
            BindContentManifest(manifest);
        }
        /// <summary>Extended connected fixture profile binds the same finite manifest while
        /// retaining the exact schema20 simulation path for research, manufacturing and combat.</summary>
        public TestOnlySharedWorldPolicy(TestOnlyContentManifest manifest,PortableKitFixture portableKit,SharedCombatFixture combat,
            SharedResearchFixture research,SharedCraftingFixture crafting,SharedRepairFixture repair,SharedManufacturingFixture manufacturing,
            SupplyCacheFixture supplyCache,int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,repair,manufacturing,supplyCache,walkingSpeed,conditions,terrain)
        {
            if(portableKit==null)throw new ArgumentNullException(nameof(portableKit));
            this.portableKit=portableKit;
            if(combat==null||supplyCache==null||!supplyCache.HasTools||supplyCache.HasKey)
                throw new ArgumentException("Portable kit requires the selected cache and tools, and rejects an unsourced-mass key fixture.");
            ContentFingerprint=PortableEquipmentRules.Fingerprint(ContentFingerprint,portableKit);
            BindContentManifest(manifest);
        }
        /// <summary>Source-resolved manufacturing profile without unrelated portable-equipment state.</summary>
        public TestOnlySharedWorldPolicy(TestOnlyContentManifest manifest,SharedCombatFixture combat,SharedResearchFixture research,
            SharedCraftingFixture crafting,SharedRepairFixture repair,SharedManufacturingFixture manufacturing,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,research,crafting,repair,manufacturing,null,walkingSpeed,conditions,terrain)
        {
            BindContentManifest(manifest);
        }
        private void BindContentManifest(TestOnlyContentManifest manifest)
        {
            contentManifest=manifest??throw new ArgumentNullException(nameof(manifest));
            string error=contentManifest.ValidateBindings();
            if(error!=null)throw new ArgumentException(error,nameof(manifest));
            ContentFingerprint=contentManifest.BindFingerprint(ContentFingerprint);
        }
        public static Authority Host() => new Authority("TEST_ONLY.host", new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }, true, true,
            new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }, new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId });
        public Snapshot Initial()
        {
            if(contentManifest!=null&&contentManifest.ValidateBindings()!=null)throw new InvalidOperationException("ContentManifestBuildMismatch");
            var s = bodies.Initial(); s.SchemaVersion = SelectedSchema; s.ContentFingerprint = ContentFingerprint;
            var companion = s.Actors.Single(a => a.Id == TestOnlyPolicy.CompanionId); companion.X = 3; companion.Y = 3;
            // The remote worker starts with both hands available. Its supplied Club is on the
            // ground at the plot; the two calendar actors begin holding their one-handed Clubs.
            s.Clubs = s.Clubs.Select(c => c.HeldBy == companion.Id ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, "", 3, 3) : c).ToArray();
            s.Lives = s.Lives.Select(l => l.ActorId == companion.Id ? ActorLifeRules.Record(l.ActorId, ActorLifeRules.Read(l), l.Prone) : l).ToArray();
            AddConfiguredActors(s);
            s.WorldSchedule = new WorldScheduleRecord("world.fixed-calendar", default, new[] { TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id });
            s.WorldIntervals = s.WorldSchedule.Order.Select(a => new WorldIntervalRecord(a, s.WorldSchedule.LatestStart(a, 0))).ToArray();
            if (offCalendarActivityEnabled||s.SchemaVersion>=Snapshot.OffCalendarActivitySchema)
                s.WorldActivityIntervals = s.Actors.Where(a => !s.WorldSchedule.Order.Contains(a.Id)).OrderBy(a => a.Id, StringComparer.Ordinal)
                    .Select(a => new WorldActivityIntervalRecord(s.WorldSchedule.Id, a.Id,
                        WorldActivityIntervalRecord.IndexAt(s.WorldSchedule, s.RuleClock))).ToArray();
            if(connectedCombat!=null)SyncCalendarBodies(s);
            InitializeResearch(s);
            InitializeCrafting(s);
            InitializeRepair(s);
            InitializeManufacturing(s);
            InitializeSupplyCache(s);
            InitializeFishingTrap(s);
            InitializePortableEquipment(s);
            InitializeHarvest(s);
            if(s.SchemaVersion>=Snapshot.SharedBonusActionSchema&&s.BonusActions.Length==0)
                s.BonusActions=s.WorldIntervals.Select(x=>new ActorBonusActionRecord(x.ActorId,checked((int)x.LastStart))).ToArray();
            InitializeCharacterAdvancement(s);
            InitializeRepeatingCrossbow(s);
            InitializePeriodicRider(s);
            InitializeOverwatchFoundation(s);
            InitializeSoldierInitialLoadout(s);
            InitializeSoldierCharacterBuild(s);
            InitializeOverwatchRuntime(s);
            if(contentManifest!=null) {
                string bindingError=contentManifest.ValidatePortableSnapshot(s);
                if(bindingError!=null)throw new InvalidOperationException(bindingError);
            }
            return s;
        }
        private static WorldIntervalRecord Interval(Snapshot s, string actor) => s.WorldIntervals.Single(x => x.ActorId == actor);
        private static void SetInterval(Snapshot s, WorldIntervalRecord value) => s.WorldIntervals = s.WorldIntervals.Select(x => x.ActorId == value.ActorId ? value : x).ToArray();
        private static WorldActivityIntervalRecord ActivityInterval(Snapshot s, string actor)
            => s.WorldActivityIntervals.Single(x => x.ActorId == actor);
        private static void SetActivityInterval(Snapshot s, WorldActivityIntervalRecord value)
            => s.WorldActivityIntervals = s.WorldActivityIntervals.Select(x => x.ActorId == value.ActorId ? value : x).ToArray();
        private static void RefreshActivityIntervals(Snapshot s)
        {
            if (s.SchemaVersion < Snapshot.OffCalendarActivitySchema) return;
            foreach (var activity in s.WorldActivityIntervals.ToArray()) {
                long current = WorldActivityIntervalRecord.IndexAt(s.WorldSchedule, s.RuleClock);
                if (activity.IntervalIndex != current)
                    SetActivityInterval(s, new WorldActivityIntervalRecord(s.WorldSchedule.Id, activity.ActorId, current));
            }
        }
        private static RuleQuantity ActivityRemaining(Snapshot s, string actor)
        {
            var activity = ActivityInterval(s, actor);
            var allowance = new RuleQuantity(Speed(s, actor)).Scale(activity.DashPaid ? 2 : 1);
            return allowance > activity.MovementSpent ? allowance - activity.MovementSpent : default;
        }
        private static bool ActivityHasLabor(Snapshot s, string actor)
        {
            var activity = ActivityInterval(s, actor);
            RuleTime start = WorldActivityIntervalRecord.StartAt(s.WorldSchedule, activity.IntervalIndex);
            RuleTime end = WorldActivityIntervalRecord.EndAt(s.WorldSchedule, activity.IntervalIndex);
            return WorldActivityValidation.HasActiveLabor(s, actor, start, end);
        }
        private static bool CanContinueActivityLabor(Snapshot s, string actor)
        {
            var activity = ActivityInterval(s, actor);
            if (activity.Action == WorldActionCommitment.None) return true;
            if (activity.Action == WorldActionCommitment.Dash) return false;
            var prior = s.Work.WorkerIntervals.SingleOrDefault(x => x.Id == activity.ActionReference
                && x.WorkerId == actor && x.End == s.RuleClock);
            return prior != null;
        }
        private static void CommitActivityLabor(Snapshot s, string actor, string workReference)
        {
            if (workReference == "" || !IsOffCalendarActivity(s, actor)) return;
            var activity = ActivityInterval(s, actor);
            SetActivityInterval(s, activity.CommitActiveLabor(workReference));
        }
        private static bool StartsOrResumesActivityWork(Command c)
        {
            switch (c.Kind) {
                case CommandKind.PlantCrop: case CommandKind.TendCrop: case CommandKind.HarvestCrop:
                case CommandKind.HandleInventory: case CommandKind.StartIntake: case CommandKind.StartWaterFill:
                case CommandKind.ResumeWaterFill: case CommandKind.HandleVessel:
                case CommandKind.StartFormulaResearch: case CommandKind.StartFormulaCopy: case CommandKind.ResumeFormulaWork:
                case CommandKind.StartCraftRemedy: case CommandKind.StartToolRepair: case CommandKind.ResumeToolRepair:
                case CommandKind.StartManufacturing: case CommandKind.ResumeManufacturing: case CommandKind.UseAlchemyDose:
                case CommandKind.StartExpeditionWork: case CommandKind.HandlePortableEquipment: case CommandKind.EquipPortableItem:
                case CommandKind.RemovePortableItem: case CommandKind.OpenPortableContainer: case CommandKind.ClosePortableContainer:
                case CommandKind.StartHarvest: case CommandKind.ResumeHarvest:
                    return true;
                case CommandKind.Interact:
                    return c.X == (int)FishingTrapInteraction.Set || c.X == (int)FishingTrapInteraction.Resume
                        || c.X == (int)FishingTrapInteraction.Retrieve || c.X == (int)FishingTrapInteraction.ResumeRetrieval;
                default: return false;
            }
        }
        private static bool IsOffCalendarActivity(Snapshot s, string actor)
            => s.SchemaVersion >= Snapshot.OffCalendarActivitySchema
                && s.WorldActivityIntervals.Any(x => x.ActorId == actor)
                && !s.WorldSchedule.Order.Contains(actor);
        private static void SetEdge(Snapshot s, WorldTraversalRecord edge) => s.WorldTraversals = s.WorldTraversals.Select(x => x.ActorId == edge.ActorId ? edge : x).ToArray();
        private static ConditionView View(Snapshot s, string actor) => TestOnlyClubAttackPolicy.ConditionsFor(s, actor).View();
        private static ConditionPermissions Permissions(Snapshot s, string actor)
        {
            var a = s.WorldIntervals.SingleOrDefault(x => x.ActorId == actor);
            // Permission projection asks whether any movement occurred, not its rounded foot count.
            return View(s, actor).PermissionsForLife(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == actor)),
                a != null && a.ActionSpent ? 1 : 0, a == null || a.MovementSpent == default ? 0 : 1);
        }
        private static long Speed(Snapshot s, string actor) => TestOnlyClubAttackPolicy.WalkingSpeed(s, actor);
        private static RuleQuantity Remaining(Snapshot s, string actor)
        {
            var a = Interval(s, actor); var available = new RuleQuantity(Speed(s, actor)).Scale(a.DashPaid ? 2 : 1);
            return available > a.MovementSpent ? available - a.MovementSpent : default;
        }
        private long CostPerFoot(Snapshot s, WorldTraversalRecord edge) => PrototypeTraversal.MovementCost(1, OrdinaryTraversal.Walk,
            terrain: terrain.At(edge.ToX, edge.ToY), crawling: View(s, edge.ActorId).Has(ConditionKind.Prone));
        private static bool CapableWorker(Snapshot s, string actor)
        {
            var view = View(s, actor);
            // Supplied ordinary labor requires deliberate bodily activity. No blanket test for
            // "has a condition": poison, invisibility and unrelated sensory clauses do not stop it.
            return ActorLifeRules.CanAct(s, actor) && !view.Unaware && !view.Clauses.Incapacitated && !view.Clauses.Immobile;
        }
        private static int AvailableHands(Snapshot s, string actor) => 2 - s.Clubs.Where(c => c.HeldBy == actor).Count()
            - s.RepeatingCrossbows.Where(c => c.HeldBy == actor).Sum(c => c.GripHands)
            - s.PortableEquipment.Where(x=>x.CustodianId==actor&&x.ParentId==""&&x.Placement==PortablePlacement.Carried).Sum(x=>x.HeldHands)
            - (CharacterAdvancementRules.ShieldOccupiesHand(s,actor)?1:0);
        private static int RepeatingCrossbowAttackHands(Snapshot s,string actor,RepeatingCrossbowRecord weapon)
            =>AvailableHands(s,actor)+weapon.GripHands+(CharacterAdvancementRules.ShieldTrainedCrossbowException(s,actor)?1:0);
        private void PauseIncompatibleWork(Snapshot s,bool includeFormula=true)
        {
            foreach (var actor in s.Actors.Where(a => !CapableWorker(s, a.Id))) {
                foreach (var crop in s.Crops.Where(c => c.Tasks.Any(t => t.WorkerId == actor.Id && t.Status == CropWorkStatus.Working)).ToArray()) CampGreens.Pause(s, crop.Id, actor.Id);
                foreach (var fill in s.WaterFills.Where(f => f.WorkerId == actor.Id && f.Status == WaterFillStatus.Working).ToArray()) WaterFilling.Pause(s, fill);
                foreach (var intake in s.Intakes.Where(i => i.ActorId == actor.Id && i.Status == IntakeStatus.Working).ToArray()) OrdinaryInventory.Interrupt(s, intake, IntakeStatus.Interrupted);
            }
            if(includeFormula)PauseIncompatibleFormulaWork(s);
            PauseIncompatibleRemedies(s);
            PauseIncompatibleRepairs(s);
            PauseIncompatibleManufacturing(s);
            InterruptSupplyCacheAttempts(s);
            PauseFishingTrapSetupIfIncompatible(s);
            PauseIncompatibleHarvesting(s);
        }
        private static void RefreshIntervals(Snapshot s)
        {
            var schedule = s.WorldSchedule; long slot = schedule.SlotAt(s.RuleClock);
            s.WorldIntervals = s.WorldIntervals.Select(a => {
                long start = schedule.LatestStart(a.ActorId, slot);
                return start == a.LastStart ? a : new WorldIntervalRecord(a.ActorId, start);
            }).ToArray();
            s.WorldSchedule = schedule.At(slot);
            if(s.SchemaVersion>=Snapshot.CalendarCombatSchema)SyncCalendarBodies(s);
        }
        private static string PayRun(Snapshot s, string actor)
        {
            if (Interval(s, actor).DashPaid) return null;
            if (Interval(s, actor).ActionSpent) return "ActionAlreadySpent";
            if (!Permissions(s, actor).Dash) return "ConditionPreventsDash";
            SetInterval(s, Interval(s, actor).PayDash()); return null;
        }
        private static string PayActivityDash(Snapshot s, string actor, string commandId, long commandRevision)
        {
            var activity = ActivityInterval(s, actor);
            if (activity.DashPaid) return null;
            if (ActivityHasLabor(s, actor)) return "OffCalendarLaborOverlapsActivity";
            if (activity.Action != WorldActionCommitment.None) return "ActionAlreadySpent";
            if (!Permissions(s, actor).Dash) return "ConditionPreventsDash";
            SetActivityInterval(s, activity.PayDash(commandId, commandRevision));
            return null;
        }
        private static CommandReceipt TraversalInstructionReceipt(Snapshot s, WorldTraversalRecord edge)
        {
            var receipt = s.Receipts.SingleOrDefault(x => x.Revision == edge.StartedRevision);
            if (receipt == null) return null;
            Command command;
            try { command = CommandHistory.Read(receipt); }
            catch (ArgumentException) { return null; }
            return command.Actor == edge.ActorId && command.Kind == CommandKind.BeginWorldStep && command.Target == "run"
                ? receipt : null;
        }
        private void ReconcileTraversal(Snapshot s)
        {
            foreach (var edge in s.WorldTraversals.Where(x => x.Status != WorldTraversalStatus.Suspended).ToArray()) {
                bool scheduled=s.WorldSchedule.Order.Contains(edge.ActorId);
                bool offCalendar=IsOffCalendarActivity(s,edge.ActorId);
                var activity = offCalendar ? ActivityInterval(s, edge.ActorId) : null;
                bool needsFreshDash=edge.Running&&offCalendar&&!activity.DashPaid;
                if (needsFreshDash && s.RuleClock == WorldActivityIntervalRecord.StartAt(s.WorldSchedule, activity.IntervalIndex)) {
                    bool blocked = WorldSpatialQueries.Step(s, edge.ActorId, edge.FromX, edge.FromY, edge.ToX, edge.ToY,
                        false, false, TestOnlyPolicy.Walkable) != SpatialStepFailure.None;
                    if (blocked || !Permissions(s, edge.ActorId).VoluntarySpeed || Speed(s, edge.ActorId) == 0) {
                        SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
                        continue;
                    }
                    var instruction = TraversalInstructionReceipt(s, edge);
                    string paymentError = instruction == null ? "TraversalInstructionMissing"
                        : PayActivityDash(s, edge.ActorId, instruction.Id, instruction.Revision);
                    if (paymentError != null || ActivityRemaining(s, edge.ActorId) == default) {
                        SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
                        continue;
                    }
                    needsFreshDash = false;
                }
                bool cannotDash=edge.Running&&(!Permissions(s,edge.ActorId).Dash
                    ||scheduled&&PayRun(s,edge.ActorId)!=null||!scheduled&&!offCalendar);
                bool noMovement=scheduled?Remaining(s,edge.ActorId)==default
                    :offCalendar?ActivityRemaining(s,edge.ActorId)==default:false;
                if (!Permissions(s, edge.ActorId).VoluntarySpeed || Speed(s, edge.ActorId) == 0 || cannotDash)
                    SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
                else SetEdge(s, edge.With(edge.DistanceFeet, needsFreshDash||noMovement
                    ? WorldTraversalStatus.WaitingForRefresh : WorldTraversalStatus.Moving));
            }
        }
        private static RuleTime? NextConditionDeadline(Snapshot s)
        {
            var values = s.Conditions.Select(j => ConditionHistory.Restore(j).Ledger).SelectMany(l => l.Applications.Where(x => !x.EndedAt.HasValue).Select(x => x.Application.Expires)
                .Concat(l.Immunities.Where(x => !x.EndedAt.HasValue).Select(x => x.Grant.Expires))).Where(x => x.HasValue && x.Value.Time > s.RuleClock).Select(x => x.Value.Time).ToArray();
            return values.Length == 0 ? (RuleTime?)null : values.Min();
        }
        private void AdvanceTo(Snapshot s, RuleTime target, bool exitAfterSlot=false, Command initiating=null, ManufacturingAdvanceRecord continuation=null)
        {
            if (target <= s.RuleClock) throw new ArgumentException("Positive shared advance required.");
            int subevent = 0;
            while (s.RuleClock < target) {
                ReconcileTraversal(s); RuleTime segmentStart = s.RuleClock; RuleTime next = target;
                var condition = NextConditionDeadline(s); if (condition.HasValue && condition.Value < next) next = condition.Value;
                var periodic = NextPeriodicMarker(s); if(periodic.HasValue&&periodic.Value<next)next=periodic.Value;
                var formula = NextFormulaBoundary(s); if (formula.HasValue && formula.Value < next) next = formula.Value;
                var dying = NextDyingMarker(s); if(dying.HasValue&&dying.Value<next)next=dying.Value;
                var remedy = NextRemedyBoundary(s); if(remedy.HasValue&&remedy.Value<next)next=remedy.Value;
                var repairBoundary = NextRepairBoundary(s); if(repairBoundary.HasValue&&repairBoundary.Value<next)next=repairBoundary.Value;
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<next)next=manufacturingBoundary.Value;
                var cacheBoundary=NextSupplyCacheBoundary(s);if(cacheBoundary.HasValue&&cacheBoundary.Value<next)next=cacheBoundary.Value;
                var trapBoundary=NextFishingTrapBoundary(s);if(trapBoundary.HasValue&&trapBoundary.Value<next)next=trapBoundary.Value;
                var harvestBoundary=NextHarvestBoundary(s);if(harvestBoundary.HasValue&&harvestBoundary.Value<next)next=harvestBoundary.Value;
                var tacticalFeatureBoundary=SoldierTacticalFeatures.NextDeadline(s);if(tacticalFeatureBoundary.HasValue&&tacticalFeatureBoundary.Value<next)next=tacticalFeatureBoundary.Value;
                var active = s.WorldTraversals.Where(x => x.Status != WorldTraversalStatus.Suspended).ToArray();
                // Stationary, living actors have no per-Start event here. The arithmetic cursor
                // skips empty intervals; active movement must visit its real budget boundaries.
                if (active.Length != 0 || s.InventoryCombat || s.Encounter!=null&&s.Lives.Any(x=>x.Hp==0&&!x.Stable&&!x.Dead&&x.UsesDeathSaves)) {
                    var boundary = s.WorldSchedule.Start(checked(s.WorldSchedule.ProcessedSlot + 1)); if (boundary < next) next = boundary;
                }
                foreach (var activity in s.WorldActivityIntervals) {
                    var boundary = WorldActivityIntervalRecord.EndAt(s.WorldSchedule, activity.IntervalIndex);
                    var horizon = target < boundary ? target : boundary;
                    bool activeOffCalendarWork = horizon > s.RuleClock
                        && (s.Work.WorkerIntervals.Any(w => w.WorkerId == activity.ActorId && w.Start < horizon && w.End > s.RuleClock)
                            || WorldActivityValidation.ActiveLaborReference(s, activity.ActorId, s.RuleClock, horizon) != "");
                    if ((active.Any(e => e.ActorId == activity.ActorId && e.Status == WorldTraversalStatus.Moving)
                        || activeOffCalendarWork) && boundary > s.RuleClock && boundary < next) next = boundary;
                    var nextWorkStart = s.Work.WorkerIntervals.Where(w => w.WorkerId == activity.ActorId
                        && w.Start > s.RuleClock && w.Start < next).Select(w => w.Start).DefaultIfEmpty(next).Min();
                    if (nextWorkStart < next) next = nextWorkStart;
                }
                foreach (var activity in s.WorldActivityIntervals.Where(x => x.DashPaid
                    && WorldActivityValidation.HasActiveLabor(s, x.ActorId, segmentStart, next)))
                    throw new InvalidOperationException("OffCalendarActionAlreadySpent");
                var activityLabor = s.WorldActivityIntervals.ToDictionary(x => x.ActorId,
                    x => WorldActivityValidation.ActiveLaborReference(s, x.ActorId, segmentStart, next), StringComparer.Ordinal);
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    long multiplier = CostPerFoot(s, edge); var distance = new RuleQuantity(5) - edge.DistanceFeet;
                    bool scheduled=s.WorldSchedule.Order.Contains(edge.ActorId);
                    if(scheduled||IsOffCalendarActivity(s,edge.ActorId)) {
                        var available=scheduled?Remaining(s,edge.ActorId):ActivityRemaining(s,edge.ActorId);
                        var remaining = available.Scale(1, multiplier); if (remaining < distance) distance = remaining;
                    }
                    var duration = distance.Scale(6 * multiplier, checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)));
                    var end = CampGreens.Add(s.RuleClock, new RuleTime(duration.Numerator, duration.Denominator)); if (end < next) next = end;
                }
                var elapsed = CampGreens.Subtract(next, s.RuleClock);
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    long multiplier = CostPerFoot(s, edge);
                    var distance = new RuleQuantity(elapsed.Numerator, elapsed.Denominator).Scale(checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)), 6 * multiplier);
                    bool scheduled=s.WorldSchedule.Order.Contains(edge.ActorId);
                    if(scheduled)SetInterval(s, Interval(s, edge.ActorId).Spend(distance.Scale(multiplier)));
                    else if(IsOffCalendarActivity(s,edge.ActorId))SetActivityInterval(s,ActivityInterval(s,edge.ActorId).Spend(distance.Scale(multiplier)));
                    var progress = edge.DistanceFeet + distance;
                    if(distance>default(RuleQuantity))CharacterAdvancementRules.MarkMoved(s,edge.ActorId);
                    if (progress == new RuleQuantity(5)) {
                        var actor = s.Actors.Single(a => a.Id == edge.ActorId); actor.X = edge.ToX; actor.Y = edge.ToY;
                        s.Clubs = s.Clubs.Select(c => c.HeldBy == actor.Id ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, c.HeldBy, actor.X, actor.Y) : c).ToArray();
                        s.WorldTraversals = s.WorldTraversals.Where(x => x.ActorId != actor.Id).ToArray();
                    } else SetEdge(s, edge.With(progress, edge.Status));
                }
                // Existing procedures own crop/food/water completion and their local ordering.
                // Movement duration was bounded before their advance, so they cannot over-credit it.
                long previousSlot=s.WorldSchedule.ProcessedSlot;
                var ready = new System.Collections.Generic.List<string>();
                var repairsReady = new System.Collections.Generic.List<string>();
                var manufacturingReady = new System.Collections.Generic.List<string>();
                if(connectedCombat==null) {
                    if(harvestFixture!=null)OrdinaryInventory.AdvanceTo(s,next,world=>{
                        TestOnlyClubAttackPolicy.AdvanceConditions(world,"."+(++subevent).ToString(CultureInfo.InvariantCulture));
                        PauseIncompatibleHarvesting(world);
                    },(world,elapsedWork)=>CreditHarvestWork(world,elapsedWork));
                    else {
                        OrdinaryInventory.AdvanceTo(s, next);
                        TestOnlyClubAttackPolicy.AdvanceConditions(s, "." + (++subevent).ToString(CultureInfo.InvariantCulture));
                    }
                } else {
                    OrdinaryInventory.AdvanceTo(s,next,world=> {
                        TestOnlyClubAttackPolicy.AdvanceConditions(world,"."+(++subevent).ToString(CultureInfo.InvariantCulture));
                        PauseIncompatibleWork(world,false);
                    }, (world,elapsedWork)=>{CreditFormulaWork(world,elapsedWork,ready);CreditRemedyWork(world,elapsedWork);CreditRepairWork(world,elapsedWork,repairsReady);CreditManufacturing(world,elapsedWork,manufacturingReady);CreditFishingTrapWork(world,elapsedWork);CreditHarvestWork(world,elapsedWork);});
                }
                RefreshActivityIntervals(s);
                foreach (var activity in s.WorldActivityIntervals.ToArray()) {
                    string reference = activityLabor[activity.ActorId];
                    if (reference == "") continue;
                    RuleTime intervalStart = WorldActivityIntervalRecord.StartAt(s.WorldSchedule, activity.IntervalIndex);
                    RuleTime intervalEnd = WorldActivityIntervalRecord.EndAt(s.WorldSchedule, activity.IntervalIndex);
                    if (segmentStart < intervalEnd && next > intervalStart)
                        CommitActivityLabor(s, activity.ActorId, reference);
                }
                SyncExpeditionAssignments(s);
                ResolveDueFishingTrapChecks(s);
                CompleteFishingTrapRetrievals(s);
                SoldierTacticalFeatures.ExpireEndMarkers(s,previousSlot,s.WorldSchedule.SlotAt(s.RuleClock),s.Revision+1);
                RefreshIntervals(s);
                if(s.SchemaVersion>=Snapshot.CraftingConsequenceSchema)ProcessSharedLifeMarkers(s,previousSlot);
                else if(connectedCombat!=null&&s.Encounter!=null&&s.WorldSchedule.ProcessedSlot!=previousSlot) {
                    // Any dying actor forces real boundary visits above; no random save is skipped.
                    ActorLifeRules.RegularStart(s,checked((int)s.WorldSchedule.ProcessedSlot));
                }
                else if(periodicRider!=null&&s.WorldSchedule.ProcessedSlot!=previousSlot) {
                    long slot=s.WorldSchedule.ProcessedSlot;string actor=s.WorldSchedule.Order[(int)(slot%s.WorldSchedule.Order.Count)];
                    SaveWorldLifeMarker(s,actor,s.WorldSchedule.Id,s.WorldSchedule.Origin,slot,checked((int)slot));
                }
                ProcessPeriodicRiderMarker(s,previousSlot);
                foreach(string id in ready) {
                    var job=s.FormulaWork.Single(x=>x.Id==id);
                    if(ResearchAccess(s,job.WorkerId,false)==null)FinishFormulaCheck(s,job);
                }
                foreach(string id in repairsReady) {
                    var job=s.RepairWork.Single(x=>x.Id==id);
                    if(RepairAccess(s,job.WorkerId,job.TargetId,false)==null)FinishRepair(s,job);
                }
                foreach(string id in manufacturingReady){
                    var job=s.ManufacturingOrders.Single(x=>x.Id==id);
                    if(ManufacturingAccess(s,job.WorkerId,false,true,job.RecipeId)==null)FinishManufacturingCheck(s,job);
                }
                PauseIncompatibleWork(s); CompleteSupplyCacheAttempts(s); ReconcileTraversal(s);
                if(ManufacturingChoicePending(s)){
                    s.ManufacturingAdvance=continuation??new ManufacturingAdvanceRecord(target,exitAfterSlot,initiating.Id,s.Revision+1,
                        initiating.Kind==CommandKind.EndRegularTurn||initiating.Kind==CommandKind.EndFixedEncounter?initiating.Target:"");
                    if(connectedCombat!=null)ObserveCalendar(s);return;
                }
            }
            if(connectedCombat!=null)ObserveCalendar(s);
        }
        public string Resolve(Snapshot s, Command c)
        {
            if (!s.Actors.Any(a => a.Id == c.Actor)) return "UnknownWorldActor";
            if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)) {
                var activity = ActivityInterval(s, c.Actor);
                if (activity.Action == WorldActionCommitment.Dash
                    || activity.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(s, c.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            if((c.Kind==CommandKind.RespondOverwatch||c.Kind==CommandKind.ResolveOverwatchRider)&&(connectedCombat==null||!s.InventoryCombat))
                return "OverwatchRequiresTacticalCombat";
            if(c.Kind==CommandKind.AwardCharacterMilestone||c.Kind==CommandKind.AdvanceCharacterLevel)return ResolveCharacterAdvancement(s,c);
            if(PeriodicEventCommand(c.Kind))return ResolvePeriodicEvent(s,c);
            if(c.Kind==CommandKind.CurePeriodicRider&&(connectedCombat==null||!s.InventoryCombat))return "MedicineRequiresTacticalAction";
            if(contentManifest!=null) {
                string contentError=contentManifest.ValidateCommand(s,c);
                if(contentError!=null)return contentError;
            }
            if(ManufacturingChoicePending(s)&&c.Kind!=CommandKind.ResolveManufacturingQuality)return "ManufacturingChoicePending";
            if(c.Kind==CommandKind.AssignExpeditionWork||c.Kind==CommandKind.CancelExpeditionWork||c.Kind==CommandKind.StartExpeditionWork)
                return ResolveExpeditionAssignment(s,c);
            if(PortableCommand(c.Kind))return ResolvePortableEquipment(s,c);
            if(IsHarvestCommand(c))return ResolveHarvest(s,c);
            if(ManufacturingCommand(c.Kind))return ResolveManufacturing(s,c);
            if(IsFishingTrapCommand(c))return ResolveFishingTrap(s,c);
            if(IsSupplyCacheCommand(c))return ResolveSupplyCache(s,c);
            if(RepairCommand(c.Kind))return ResolveRepair(s,c);
            if(CraftingCommand(c.Kind))return ResolveCraftingConsequence(s,c);
            if(FormulaCommand(c.Kind))return connectedCombat!=null&&PendingCalendarChoice(s)?"TacticalChoicePending":ResolveFormulaWork(s,c);
            if(connectedCombat!=null) {
                if(c.Kind==CommandKind.BeginFixedEncounter)return EnterCalendarCombat(s,c);
                if(s.InventoryCombat)return ResolveCalendarCombat(s,c);
            }
            if(c.Kind==CommandKind.TacticalAssessment)return "TacticalAssessmentRequiresEncounter";
            if(c.Kind==CommandKind.OfferCommandStep||c.Kind==CommandKind.RespondCommandStep)return "CommandStepRequiresEncounter";
            if(c.Kind==CommandKind.ActivateDefensiveFormation||c.Kind==CommandKind.RespondDefensiveFormation)
                return "DefensiveFormationRequiresEncounter";
            if(c.Kind==CommandKind.SuppressionFire)return rangedCombat==null?"RangedCommandNotImplemented":"RangedCombatRequiresEncounter";
            if(c.Kind==CommandKind.AttackRepeatingCrossbow||c.Kind==CommandKind.ReloadRepeatingCrossbow
                ||c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire)
                return rangedCombat==null?"RangedCommandNotImplemented":"RangedCombatRequiresEncounter";
            if (c.Combat != null) return "SharedCombatHandoffNotImplemented";
            if (c.Kind == CommandKind.AdvanceClock) {
                if (c.Inventory != null || c.Target != "" || c.X < 1 || c.Y < 1) return "InvalidWorldAdvance";
                AdvanceTo(s, CampGreens.Add(s.RuleClock, new RuleTime(c.X, c.Y)),initiating:c); return null;
            }
            if (c.Kind == CommandKind.BeginWorldStep) {
                string assessment = AssessWorldStep(s, c, out var facts); if (assessment != null) return assessment;
                bool scheduled=facts.Scheduled;
                bool offCalendarActivity=facts.OffCalendar&&IsOffCalendarActivity(s,c.Actor);
                // No implicit combat is fabricated. Entering/leaving a hostile engagement requires
                // the upcoming tactical continuation host before the departure can be admitted.
                if (facts.StartsEncounter) return EnterCalendarCombat(s,new Command(c.Id,c.Actor,c.ExpectedRevision,CommandKind.BeginFixedEncounter));
                if (c.Target == "run") {
                    if(scheduled) { string error = PayRun(s, c.Actor); if (error != null) return error; }
                    else { string error=PayActivityDash(s,c.Actor,c.Id,s.Revision+1);if(error!=null)return error; }
                }
                var actor = s.Actors.Single(x => x.Id == c.Actor);
                s.WorldTraversals = s.WorldTraversals.Concat(new[] { new WorldTraversalRecord(c.Actor, s.Revision + 1, actor.X, actor.Y, facts.ToX, facts.ToY, running: c.Target == "run") }).ToArray();
                SyncExpeditionAssignments(s,c.Actor); return null;
            }
            if (c.Kind == CommandKind.SuspendWorldStep || c.Kind == CommandKind.ResumeWorldStep) {
                string assessment=AssessTraversalControl(s,c,out var edge);if(assessment!=null)return assessment;
                if (c.Kind == CommandKind.SuspendWorldStep) {
                    SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended)); return null;
                }
                bool offCalendarActivity=IsOffCalendarActivity(s,c.Actor);
                bool waitingForFreshActivityDash=offCalendarActivity&&edge.Running&&edge.Status==WorldTraversalStatus.WaitingForRefresh;
                if(edge.Running) {
                    if(s.WorldSchedule.Order.Contains(c.Actor)) { string error = PayRun(s, c.Actor); if (error != null) return error; }
                    else { string error=PayActivityDash(s,c.Actor,c.Id,s.Revision+1);if(error!=null)return error; }
                }
                SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Moving)); ReconcileTraversal(s); return null;
            }
            if (c.Kind == CommandKind.DispatchConditionEvent) {
                var fact = conditions.Events.SingleOrDefault(x => x.Operation.Id == c.Target && x.Target == c.Actor);
                if (s.WorldTraversals.Any(x => x.ActorId == c.Actor && x.DistanceFeet != default)
                    && (fact?.Operation.Application?.Kind == "Unconscious" || fact?.Operation.Application?.Kind == "Prone")) return "OffGridPhysicalConsequenceUnsupported";
                string error = bodies.Resolve(s, c); if (error != null) return error;
                PauseIncompatibleWork(s); ReconcileTraversal(s); return null;
            }
            if (c.Kind == CommandKind.Move || c.Kind == CommandKind.Interact) return "UseWorldTraversal";
            bool management = c.Kind == CommandKind.PlantCrop || c.Kind == CommandKind.TendCrop || c.Kind == CommandKind.HarvestCrop || c.Kind == CommandKind.PauseCrop || c.Kind == CommandKind.SetCropConditions
                || c.Kind == CommandKind.PortionInventory || c.Kind == CommandKind.HandleInventory || c.Kind == CommandKind.StartIntake || c.Kind == CommandKind.InterruptIntake
                || c.Kind == CommandKind.StartWaterFill || c.Kind == CommandKind.PauseWaterFill || c.Kind == CommandKind.ResumeWaterFill || c.Kind == CommandKind.CancelWaterFill || c.Kind == CommandKind.HandleVessel;
            if (!management) return "SharedCommandNotImplemented";
            // None of these procedures may authorize access using a stale integer grid anchor.
            if (s.WorldTraversals.Any(x => x.ActorId == c.Actor || c.Inventory?.Destination == x.ActorId)) return "TraversalRequiresStationaryInteraction";
            bool release = c.Kind == CommandKind.PauseCrop || c.Kind == CommandKind.PauseWaterFill || c.Kind == CommandKind.CancelWaterFill || c.Kind == CommandKind.InterruptIntake || c.Kind == CommandKind.SetCropConditions;
            if (!release && !CapableWorker(s, c.Actor)) return "WorkerCannotPerformTask";
            if ((c.Kind == CommandKind.StartWaterFill || c.Kind == CommandKind.ResumeWaterFill) && AvailableHands(s, c.Actor) < 2) return "TwoHandsRequired";
            // Handling has its own one-second synchronous cost. Its existing stationary procedure
            // cannot observe an intervening capability change or another body's exact partial
            // position. Keep those combinations explicitly gated until that procedure is resumable.
            if ((c.Kind == CommandKind.HandleInventory || c.Kind == CommandKind.HandleVessel) && s.WorldTraversals.Length != 0) return "ConcurrentTraversalHandlingUnsupported";
            if (c.Kind == CommandKind.HandleInventory || c.Kind == CommandKind.HandleVessel) {
                var deadline = NextConditionDeadline(s);
                if (deadline.HasValue && deadline.Value <= s.RuleClock.AddSeconds(1)) return "TimedHandlingBoundaryUnsupported";
                var periodic = NextPeriodicMarker(s);
                if(periodic.HasValue&&periodic.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var formula = NextFormulaBoundary(s);
                if(formula.HasValue&&formula.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var dying=NextDyingMarker(s);if(dying.HasValue&&dying.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var remedy=NextRemedyBoundary(s);if(remedy.HasValue&&remedy.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var repairBoundary=NextRepairBoundary(s);if(repairBoundary.HasValue&&repairBoundary.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
                var tacticalFeatureBoundary=SoldierTacticalFeatures.NextDeadline(s);
                if(tacticalFeatureBoundary.HasValue&&tacticalFeatureBoundary.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
            }
            var before = s.RuleClock; string failure = inventory.Resolve(s, c);
            if (failure != null) return failure;
            if (s.RuleClock > before) {
                CreditFormulaWork(s,CampGreens.Subtract(s.RuleClock,before),new System.Collections.Generic.List<string>());
                CreditRemedyWork(s,CampGreens.Subtract(s.RuleClock,before));
                CreditRepairWork(s,CampGreens.Subtract(s.RuleClock,before),new System.Collections.Generic.List<string>());
                CreditManufacturing(s,CampGreens.Subtract(s.RuleClock,before),new System.Collections.Generic.List<string>());
                // No traversal or condition deadline can occur inside the admitted interval.
                TestOnlyClubAttackPolicy.AdvanceConditions(s, ".handling"); RefreshActivityIntervals(s);
                CommitActivityLabor(s, c.Actor, WorldActivityValidation.ActiveLaborReference(s, c.Actor, before, s.RuleClock));
                RefreshIntervals(s); PauseIncompatibleWork(s);
                if(connectedCombat!=null)ObserveCalendar(s);
            }
            return null;
        }
        public string ValidateState(Snapshot s)
        {
            try {
                if (s.SchemaVersion != SelectedSchema || s.Receipts.Length != s.Revision) return "InvalidSharedWorldHeader";
                // This laboratory has exactly one expedition member outside the tactical
                // calendar. The calendar remains the initiative roster; the companion can use
                // the shared exploration clock without gaining combat turns.
                if(s.WorldSchedule!=null&&s.WorldTraversals.Any(x=>!s.WorldSchedule.Order.Contains(x.ActorId)
                    &&(x.ActorId!=TestOnlyPolicy.CompanionId&&!IsOffCalendarActivity(s,x.ActorId)
                        ||x.Running&&s.SchemaVersion<Snapshot.OffCalendarActivitySchema)))return "InvalidExplorationTraveler";
                string manufacturingError=ValidateManufacturingProfile(s);if(manufacturingError!=null)return manufacturingError;
                if(contentManifest!=null) {
                    string bindingError=contentManifest.ValidateBindings();if(bindingError!=null)return bindingError;
                    bindingError=contentManifest.ValidatePortableSnapshot(s);if(bindingError!=null)return bindingError;
                    if(s.ContentFingerprint!=ContentFingerprint)return "ContentFingerprintMismatch";
                }
                if(portableKit!=null) {
                    PortableEquipmentRules.ValidateFixture(s);
                    var pack=s.PortableEquipment.SingleOrDefault(x=>x.Id==PortableKitFixture.Pack);
                    if(pack==null||!PortableEquipmentRules.FixtureFitValid(s,pack))return "InvalidPortableKitFixture";
                }
                if(overwatchFoundation!=null&&(s.SchemaVersion!=Snapshot.SharedBonusActionSchema
                    &&s.SchemaVersion!=Snapshot.OverwatchSchema&&s.SchemaVersion!=Snapshot.OverwatchExecutionSchema
                    &&s.SchemaVersion!=Snapshot.SoldierInitialLoadoutSchema&&s.SchemaVersion!=Snapshot.SoldierInitialBuildSchema
                    &&s.SchemaVersion!=Snapshot.SoldierTacticalTechniquesSchema&&s.SchemaVersion!=Snapshot.CharacterAdvancementHistorySchema
                    &&s.SchemaVersion!=Snapshot.TacticalAssessmentSchema
                    &&s.SchemaVersion!=Snapshot.CommandStepSchema&&s.SchemaVersion!=Snapshot.SuppressionFireSchema
                    &&s.SchemaVersion!=Snapshot.DefensiveFormationSchema
                    ||s.CharacterFeatureGrants.Count(g=>g.ActorId==TestOnlyPolicy.ActorId&&g.FeatureId==CharacterFeatureIds.Overwatch
                        &&g.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature)!=1
                    ||s.CharacterFeatureGrants.Any(g=>g.ActorId==TestOnlyPolicy.ActorId&&g.FeatureId==CharacterFeatureIds.Overwatch
                        &&g.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&(g.MilestoneId!=""||g.GrantedRevision!=0))))return "InvalidOverwatchFoundationFixture";
                if(overwatchRuntime!=null&&((s.SchemaVersion!=Snapshot.OverwatchSchema&&s.SchemaVersion!=Snapshot.OverwatchExecutionSchema)||s.OverwatchIntervals.Length<1
                    ||s.OverwatchIntervals.Any(x=>x.ActorId!=TestOnlyPolicy.ActorId)))return "InvalidOverwatchDesignationFixture";
                if(periodicRider!=null) {
                    if(s.SchemaVersion<Snapshot.PeriodicRiderSchema||s.PeriodicRiders.Any(x=>x.ProfileId!=PeriodicRiderFixture.ProfileId
                        ||x.FamilyId!=PeriodicRiderFixture.FamilyId||x.SourceId!=PeriodicRiderFixture.SourceId||x.DamageType!="piercing"||x.RemainingTicks>1)
                        ||s.PeriodicRiders.Where(x=>x.Present).GroupBy(x=>x.TargetId+"|"+x.OwnerId+"|"+x.SourceId,StringComparer.Ordinal).Any(g=>g.Count()>1)
                        ||s.SkillTraining.Any(x=>x.SkillId!="medicine"))return "InvalidPeriodicRiderFixture";
                }
                var fishingSkills=s.SkillTraining.Where(x=>x.SkillId=="fishing-tackle").ToArray();
                if(fishingTrapProfiles.Length==0) {
                    bool harvestSelected=harvestFixture!=null;
                    if(s.FishingTrapAttempts.Length!=0||!harvestSelected&&fishingSkills.Length!=0||s.FishingOpportunities.Length!=0
                        ||!harvestSelected&&s.FishingCreatures.Length!=0||s.FishingTraps.Length!=0||s.FishingReceiveLocations.Length!=0
                        ||s.FishingTrapRetrievals.Length!=0||s.FishingStockManifests.Length!=0||s.FishingStockAllocations.Length!=0)
                        return "FishingTrapFixtureNotSelected";
                    if(harvestSelected) {
                        var expectedHarvestWorkers=HarvestWorkerIds;
                        int expectedSkills=harvestFixture.Trained?expectedHarvestWorkers.Length:0;
                        if(s.SchemaVersion!=harvestFixture.SchemaVersion||fishingSkills.Length!=expectedSkills
                            ||fishingSkills.Any(x=>!expectedHarvestWorkers.Contains(x.ActorId,StringComparer.Ordinal)||x.ProficiencyRank!=1)
                            ||s.FishingCreatures.Length!=1||s.FishingCreatures[0].Id!=SharedHarvestFixture.CreatureId
                            ||s.FishingCreatures[0].OriginId!=HarvestSiteId||s.FishingCreatures[0].SiteId!=HarvestSiteId
                            ||s.FishingCreatures[0].LocationId!=HarvestSiteId||s.FishingCreatures[0].CustodianId!=OffCalendarWorkerId
                            ||s.FishingCreatures[0].LifeState!=FishingCreatureLifeState.Dead
                            ||s.HarvestDonors.Length!=1||s.HarvestManifests.Length!=1
                            ||s.HarvestDonors[0].OwnerId!=OffCalendarWorkerId||s.HarvestManifests[0].SiteId!=HarvestSiteId
                            ||s.HarvestCategories.Length!=(harvestFixture.SmallFinitePool?(harvestFixture.SingleCategoryMultipleUnits?1:2):1)
                            ||s.HarvestUnits.Length!=(harvestFixture.SmallFinitePool?3:1)
                            ||!s.HarvestUnits.Any(x=>x.Id==HarvestFiniteLotId)
                            ||s.PortableEquipment.Count(x=>x.Id==SharedHarvestFixture.ToolkitId)!= (harvestFixture.HasToolkit?1:0)
                            ||s.PortableEquipment.Count(x=>x.Id==SharedHarvestFixture.KnifeId)!= (harvestFixture.HasKnife?1:0)
                            ||s.PortableEquipment.Count(x=>x.Id==SharedHarvestFixture.ContainerId)!= (harvestFixture.HasContainer?1:0)
                            ||s.PortableEquipment.Where(x=>x.Id==SharedHarvestFixture.ToolkitId||x.Id==SharedHarvestFixture.KnifeId
                                ||x.Id==SharedHarvestFixture.ContainerId).Any(x=>x.GroundX!=HarvestSiteX||x.GroundY!=HarvestSiteY)
                            ||s.Structures.Count(x=>x.Id==SharedHarvestFixture.WorkSurfaceId)!=(harvestFixture.HasWorkSurface?1:0)
                            ||s.Structures.Any(x=>x.Id==SharedHarvestFixture.WorkSurfaceId&&x.LocationId!=HarvestSiteId))
                            return "InvalidHarvestFixture";
                    } else if(s.HarvestDonors.Length+s.HarvestManifests.Length+s.HarvestCategories.Length+s.HarvestUnits.Length+s.HarvestAttempts.Length!=0)
                        return "HarvestFixtureNotSelected";
                } else if(s.SchemaVersion!=SelectedSchema
                    ||fishingSkills.Length!=fishingTrapProfiles.Select(x=>x.SetterId).Distinct(StringComparer.Ordinal).Count()
                    ||fishingTrapProfiles.GroupBy(x=>x.SetterId,StringComparer.Ordinal).Any(g=>
                        !fishingSkills.Any(skill=>skill.ActorId==g.Key&&skill.ProficiencyRank==g.First().ProficiencyRank))
                    ||s.FishingTrapAttempts.Any(x=>{
                        var profile=fishingTrapProfiles.SingleOrDefault(p=>p.TrapIdentity==x.TrapId);
                        return profile==null||x.SetterId!=profile.SetterId||x.ResponsibleHolderId!=profile.SetterId
                            ||x.OpportunityId!=(PhysicalFishingEnabled?profile.OpportunityIdentity:SharedFishingTrapFixture.OpportunityId)
                            ||x.CreatureId!=(PhysicalFishingEnabled?profile.CreatureIdentity:SharedFishingTrapFixture.CreatureId)
                            ||x.SiteId!=(PhysicalFishingEnabled?profile.SiteIdentity:SharedFishingTrapFixture.SiteId)
                            ||(fishingTrapLegacy
                                ?(x.BaitLotId!=""||x.BaitReservationId!=""||x.BaitExposedAt.HasValue)
                                :(x.BaitLotId!=profile.BaitLotIdentity||x.BaitReservationId!=x.Id+".bait"))
                            ||x.CapturedCreatureId!=""&&x.CapturedCreatureId!=(PhysicalFishingEnabled?profile.CreatureIdentity:SharedFishingTrapFixture.CreatureId)
                            ||x.CheckDc!=0&&x.CheckDc!=profile.CatchDc;
                    })
                    ||PhysicalFishingEnabled&&(s.FishingOpportunities.Length!=fishingTrapProfiles.Length
                        ||s.FishingCreatures.Length!=fishingTrapProfiles.Select(x=>x.CreatureIdentity).Distinct(StringComparer.Ordinal).Count()
                        ||s.SchemaVersion>=Snapshot.FishingStockSchema&&(s.FishingStockManifests.Length!=fishingTrapProfiles
                            .Select(x=>x.SharedStockIdentity+"|"+x.StockVersionIdentity).Distinct(StringComparer.Ordinal).Count()
                            ||s.FishingStockAllocations.Length!=fishingTrapProfiles.Length)
                        ||s.SchemaVersion<Snapshot.FishingStockSchema&&(s.FishingStockManifests.Length!=0||s.FishingStockAllocations.Length!=0)
                        ||s.FishingTraps.Length!=fishingTrapProfiles.Length
                        ||s.FishingReceiveLocations.Length!=fishingTrapProfiles.Length
                        ||s.FishingTrapRetrievals.Any(x=>!fishingTrapProfiles.Any(p=>p.TrapIdentity==x.TrapId))
                        ||fishingTrapProfiles.Any(profile=>{
                            var opportunity=s.FishingOpportunities.SingleOrDefault(x=>x.Id==profile.OpportunityIdentity);
                            var creature=s.FishingCreatures.SingleOrDefault(x=>x.Id==profile.CreatureIdentity);
                            var trap=s.FishingTraps.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity);
                            var receiver=s.FishingReceiveLocations.SingleOrDefault(x=>x.Id==profile.ReceiverIdentity);
                            var bait=s.Work.Lots.SingleOrDefault(x=>x.Id==profile.BaitLotIdentity);
                            return opportunity==null||creature==null||trap==null||receiver==null
                                ||opportunity.SiteId!=profile.SiteIdentity||opportunity.StockVersionId!=profile.StockVersionIdentity
                                ||opportunity.CandidateCreatureId!=profile.CreatureIdentity
                                ||creature.OriginId!=profile.SiteIdentity||creature.SiteId!=profile.SiteIdentity
                                ||creature.ProfileId!="TEST_ONLY.ordinary-river-fish.1lb"
                                ||bait==null||bait.UnitId!=SharedFishingTrapFixture.BaitUnit
                                ||trap.SiteId!=profile.SiteIdentity||trap.SupportId!=profile.SupportIdentity
                                ||trap.StructuralAc!=15||trap.CatchCapacityPounds!=10
                                ||trap.CatchCapacityCubicFeet!=new RuleQuantity(1)||trap.BodyVolumeCubicFeet!=new RuleQuantity(2)
                                ||trap.RecoveryCordFeet!=20
                                ||trap.X!=(trap.Status==FishingTrapPhysicalStatus.Retrieved?profile.ReceiverX:profile.TrapX)
                                ||trap.Y!=(trap.Status==FishingTrapPhysicalStatus.Retrieved?profile.ReceiverY:profile.TrapY)
                                ||receiver.SiteId!=profile.SiteIdentity||receiver.SupportId!=profile.ReceiverSupportIdentity
                                ||receiver.X!=profile.ReceiverX||receiver.Y!=profile.ReceiverY
                                ||receiver.CapacityPounds!=new RuleQuantity(20)||receiver.CapacityCubicFeet!=new RuleQuantity(3)
                                ||receiver.RecoveryPathFeet!=profile.RecoveryPathFeet;
                        }))
                    ||!PhysicalFishingEnabled&&(s.FishingOpportunities.Length!=0||s.FishingCreatures.Length!=0
                        ||s.FishingTraps.Length!=0||s.FishingReceiveLocations.Length!=0||s.FishingTrapRetrievals.Length!=0
                        ||s.FishingStockManifests.Length!=0||s.FishingStockAllocations.Length!=0))
                    return "InvalidFishingTrapFixture";
                var replay = Initial();
                foreach (var receipt in s.Receipts.OrderBy(x => x.Revision)) {
                    var command = CommandHistory.Read(receipt);
                    if (command.ExpectedRevision != replay.Revision || Resolve(replay, command) != null) return "InvalidSharedWorldHistory";
                    replay.Revision = receipt.Revision; replay.Receipts = replay.Receipts.Concat(new[] { receipt }).ToArray();
                }
                // The laboratory dispatcher uses the existing canonical persistence projection
                // to compare EVERY subsystem, including nested crop tasks and consumed reservations.
                // Core stays independent of Persistence and the gameplay procedures stay in LabModel.
                var codec = new SnapshotCodec(); return codec.Encode(s).SequenceEqual(codec.Encode(replay)) ? null : "InvalidSharedWorldReplay";
            } catch (Exception ex) when (ex is ArgumentException || ex is InvalidOperationException || ex is OverflowException || ex is System.IO.InvalidDataException) { return "InvalidSharedWorldState"; }
        }
    }
}
#endif
