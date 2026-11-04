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
    public sealed partial class TestOnlySharedWorldPolicy : ICommandPolicy
    {
        private readonly TestOnlyClubAttackPolicy bodies;
        private readonly TestOnlyFillingPolicy inventory = new TestOnlyFillingPolicy(movableVessels: true);
        private readonly TacticalCombatFixture terrain;
        private readonly ConditionCombatFixture conditions;
        private readonly SharedCombatFixture connectedCombat;
        public bool TestOnly => true;
        public string ContentFingerprint { get; }
        public TestOnlySharedWorldPolicy(int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            :this(combat,null,walkingSpeed,conditions,terrain) { }
        public TestOnlySharedWorldPolicy(SharedCombatFixture combat,SharedResearchFixture research,int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
        {
            connectedCombat=combat;
            this.research=research;
            if(research!=null&&combat==null)throw new ArgumentException("Research requires the explicit connected calendar host.");
            this.conditions = conditions ?? new ConditionCombatFixture();
            this.terrain = new TacticalCombatFixture(new AdditionalTacticalActor(4, combat==null?4:0, walkingSpeed,combat?.EnemyHp??26), terrain);
            bodies = new TestOnlyClubAttackPolicy(actorBaseWalkingSpeed: walkingSpeed, companionBaseWalkingSpeed: walkingSpeed,
                tactical: this.terrain, conditions: this.conditions,seed:combat?.Seed??1);
            ContentFingerprint = (combat==null?"TEST_ONLY.shared-v1-":"TEST_ONLY.connected-v1-") + bodies.ContentFingerprint.Substring("TEST_ONLY.club-v1-".Length);
            if(research!=null)ContentFingerprint=ResearchFingerprint(ContentFingerprint,research);
        }
        public static Authority Host() => new Authority("TEST_ONLY.host", new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }, true, true,
            new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }, new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId });
        public Snapshot Initial()
        {
            var s = bodies.Initial(); s.SchemaVersion = research!=null?Snapshot.FormulaWorkSchema:connectedCombat==null?Snapshot.SharedWorldSchema:Snapshot.CalendarCombatSchema; s.ContentFingerprint = ContentFingerprint;
            var companion = s.Actors.Single(a => a.Id == TestOnlyPolicy.CompanionId); companion.X = 3; companion.Y = 3;
            // The remote worker starts with both hands available. Its supplied Club is on the
            // ground at the plot; the two calendar actors begin holding their one-handed Clubs.
            s.Clubs = s.Clubs.Select(c => c.HeldBy == companion.Id ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, "", 3, 3) : c).ToArray();
            s.Lives = s.Lives.Select(l => l.ActorId == companion.Id ? ActorLifeRules.Record(l.ActorId, ActorLifeRules.Read(l), l.Prone) : l).ToArray();
            s.WorldSchedule = new WorldScheduleRecord("world.fixed-calendar", default, new[] { TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id });
            s.WorldIntervals = s.WorldSchedule.Order.Select(a => new WorldIntervalRecord(a, s.WorldSchedule.LatestStart(a, 0))).ToArray();
            if(connectedCombat!=null)SyncCalendarBodies(s);
            InitializeResearch(s);
            return s;
        }
        private static WorldIntervalRecord Interval(Snapshot s, string actor) => s.WorldIntervals.Single(x => x.ActorId == actor);
        private static void SetInterval(Snapshot s, WorldIntervalRecord value) => s.WorldIntervals = s.WorldIntervals.Select(x => x.ActorId == value.ActorId ? value : x).ToArray();
        private static void SetEdge(Snapshot s, WorldTraversalRecord edge) => s.WorldTraversals = s.WorldTraversals.Select(x => x.ActorId == edge.ActorId ? edge : x).ToArray();
        private static ConditionView View(Snapshot s, string actor) => TestOnlyClubAttackPolicy.ConditionsFor(s, actor).View();
        private static ConditionPermissions Permissions(Snapshot s, string actor)
        {
            var a = Interval(s, actor);
            // Permission projection asks whether any movement occurred, not its rounded foot count.
            return View(s, actor).PermissionsForLife(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == actor)), a.ActionSpent ? 1 : 0, a.MovementSpent == default ? 0 : 1);
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
        private static int AvailableHands(Snapshot s, string actor) => 2 - s.Clubs.Count(c => c.HeldBy == actor);
        private void PauseIncompatibleWork(Snapshot s,bool includeFormula=true)
        {
            foreach (var actor in s.Actors.Where(a => !CapableWorker(s, a.Id))) {
                foreach (var crop in s.Crops.Where(c => c.Tasks.Any(t => t.WorkerId == actor.Id && t.Status == CropWorkStatus.Working)).ToArray()) CampGreens.Pause(s, crop.Id, actor.Id);
                foreach (var fill in s.WaterFills.Where(f => f.WorkerId == actor.Id && f.Status == WaterFillStatus.Working).ToArray()) WaterFilling.Pause(s, fill);
                foreach (var intake in s.Intakes.Where(i => i.ActorId == actor.Id && i.Status == IntakeStatus.Working).ToArray()) OrdinaryInventory.Interrupt(s, intake, IntakeStatus.Interrupted);
            }
            if(includeFormula)PauseIncompatibleFormulaWork(s);
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
        private void ReconcileTraversal(Snapshot s)
        {
            foreach (var edge in s.WorldTraversals.Where(x => x.Status != WorldTraversalStatus.Suspended).ToArray()) {
                if (!Permissions(s, edge.ActorId).VoluntarySpeed || Speed(s, edge.ActorId) == 0 || edge.Running && PayRun(s, edge.ActorId) != null)
                    SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
                else SetEdge(s, edge.With(edge.DistanceFeet, Remaining(s, edge.ActorId) == default ? WorldTraversalStatus.WaitingForRefresh : WorldTraversalStatus.Moving));
            }
        }
        private static RuleTime? NextConditionDeadline(Snapshot s)
        {
            var values = s.Conditions.Select(j => ConditionHistory.Restore(j).Ledger).SelectMany(l => l.Applications.Where(x => !x.EndedAt.HasValue).Select(x => x.Application.Expires)
                .Concat(l.Immunities.Where(x => !x.EndedAt.HasValue).Select(x => x.Grant.Expires))).Where(x => x.HasValue && x.Value.Time > s.RuleClock).Select(x => x.Value.Time).ToArray();
            return values.Length == 0 ? (RuleTime?)null : values.Min();
        }
        private void AdvanceTo(Snapshot s, RuleTime target)
        {
            if (target <= s.RuleClock) throw new ArgumentException("Positive shared advance required.");
            int subevent = 0;
            while (s.RuleClock < target) {
                ReconcileTraversal(s); RuleTime next = target;
                var condition = NextConditionDeadline(s); if (condition.HasValue && condition.Value < next) next = condition.Value;
                var formula = NextFormulaBoundary(s); if (formula.HasValue && formula.Value < next) next = formula.Value;
                var active = s.WorldTraversals.Where(x => x.Status != WorldTraversalStatus.Suspended).ToArray();
                // Stationary, living actors have no per-Start event here. The arithmetic cursor
                // skips empty intervals; active movement must visit its real budget boundaries.
                if (active.Length != 0 || s.InventoryCombat || s.Encounter!=null&&s.Lives.Any(x=>x.Hp==0&&!x.Stable&&!x.Dead&&x.UsesDeathSaves)) {
                    var boundary = s.WorldSchedule.Start(checked(s.WorldSchedule.ProcessedSlot + 1)); if (boundary < next) next = boundary;
                }
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    long multiplier = CostPerFoot(s, edge); var distance = new RuleQuantity(5) - edge.DistanceFeet;
                    var remaining = Remaining(s, edge.ActorId).Scale(1, multiplier); if (remaining < distance) distance = remaining;
                    var duration = distance.Scale(6 * multiplier, checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)));
                    var end = CampGreens.Add(s.RuleClock, new RuleTime(duration.Numerator, duration.Denominator)); if (end < next) next = end;
                }
                var elapsed = CampGreens.Subtract(next, s.RuleClock);
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    long multiplier = CostPerFoot(s, edge);
                    var distance = new RuleQuantity(elapsed.Numerator, elapsed.Denominator).Scale(checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)), 6 * multiplier);
                    SetInterval(s, Interval(s, edge.ActorId).Spend(distance.Scale(multiplier)));
                    var progress = edge.DistanceFeet + distance;
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
                if(connectedCombat==null) {
                    OrdinaryInventory.AdvanceTo(s, next);
                    TestOnlyClubAttackPolicy.AdvanceConditions(s, "." + (++subevent).ToString(CultureInfo.InvariantCulture));
                } else {
                    OrdinaryInventory.AdvanceTo(s,next,world=> {
                        TestOnlyClubAttackPolicy.AdvanceConditions(world,"."+(++subevent).ToString(CultureInfo.InvariantCulture));
                        PauseIncompatibleWork(world,false);
                    }, (world,elapsedWork)=>CreditFormulaWork(world,elapsedWork,ready));
                }
                RefreshIntervals(s);
                if(connectedCombat!=null&&s.Encounter!=null&&s.WorldSchedule.ProcessedSlot!=previousSlot) {
                    // Any dying actor forces real boundary visits above; no random save is skipped.
                    ActorLifeRules.RegularStart(s,checked((int)s.WorldSchedule.ProcessedSlot));
                }
                foreach(string id in ready) {
                    var job=s.FormulaWork.Single(x=>x.Id==id);
                    if(ResearchAccess(s,job.WorkerId,false)==null)FinishFormulaCheck(s,job);
                }
                PauseIncompatibleWork(s); ReconcileTraversal(s);
            }
            if(connectedCombat!=null)ObserveCalendar(s);
        }
        public string Resolve(Snapshot s, Command c)
        {
            if (!s.Actors.Any(a => a.Id == c.Actor)) return "UnknownWorldActor";
            if(FormulaCommand(c.Kind))return connectedCombat!=null&&PendingCalendarChoice(s)?"TacticalChoicePending":ResolveFormulaWork(s,c);
            if(connectedCombat!=null) {
                if(c.Kind==CommandKind.BeginFixedEncounter)return EnterCalendarCombat(s,c);
                if(s.InventoryCombat)return ResolveCalendarCombat(s,c);
            }
            if (c.Combat != null) return "SharedCombatHandoffNotImplemented";
            if (c.Kind == CommandKind.AdvanceClock) {
                if (c.Inventory != null || c.Target != "" || c.X < 1 || c.Y < 1) return "InvalidWorldAdvance";
                AdvanceTo(s, CampGreens.Add(s.RuleClock, new RuleTime(c.X, c.Y))); return null;
            }
            if (c.Kind == CommandKind.BeginWorldStep) {
                if (c.Inventory != null || (c.Target != "walk" && c.Target != "run") || Math.Abs((long)c.X) + Math.Abs((long)c.Y) != 1) return "InvalidWorldStep";
                if (!s.WorldSchedule.Order.Contains(c.Actor)) return "NoActivityCalendar";
                if (s.WorldTraversals.Any(x => x.ActorId == c.Actor)) return "TraversalAlreadyPending";
                if (s.WorldTraversals.Any(x => s.WorldSchedule.Order.Contains(x.ActorId))) return "ConcurrentHostileTraversalUnsupported";
                if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
                if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";
                var actor = s.Actors.Single(x => x.Id == c.Actor); int x = checked(actor.X + c.X), y = checked(actor.Y + c.Y);
                if (!TestOnlyPolicy.Walkable(x, y)) return "Blocked";
                if (s.Actors.Any(a => a.Id != actor.Id && a.X == x && a.Y == y) || s.WorldTraversals.Any(e => e.ToX == x && e.ToY == y)) return "Occupied";
                // No implicit combat is fabricated. Entering/leaving a hostile engagement requires
                // the upcoming tactical continuation host before the departure can be admitted.
                if (s.WorldSchedule.Order.Where(a => a != actor.Id&&(connectedCombat==null||!s.Lives.Single(l=>l.ActorId==a).Dead)).Any(id => {
                    var enemy = s.Actors.Single(a => a.Id == id);
                    return Math.Max(Math.Abs(actor.X - enemy.X), Math.Abs(actor.Y - enemy.Y)) <= 1 || Math.Max(Math.Abs(x - enemy.X), Math.Abs(y - enemy.Y)) <= 1;
                })) return connectedCombat==null?"TacticalTransitionRequired":EnterCalendarCombat(s,new Command(c.Id,c.Actor,c.ExpectedRevision,CommandKind.BeginFixedEncounter));
                if (c.Target == "run") { string error = PayRun(s, c.Actor); if (error != null) return error; }
                if (Remaining(s, c.Actor) == default) return "InsufficientMovement";
                s.WorldTraversals = s.WorldTraversals.Concat(new[] { new WorldTraversalRecord(c.Actor, s.Revision + 1, actor.X, actor.Y, x, y, running: c.Target == "run") }).ToArray(); return null;
            }
            if (c.Kind == CommandKind.SuspendWorldStep || c.Kind == CommandKind.ResumeWorldStep) {
                if (c.Inventory != null || c.Target != "" || c.X != 0 || c.Y != 0) return "InvalidTraversalControl";
                var edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == c.Actor); if (edge == null) return "NoPendingTraversal";
                if (c.Kind == CommandKind.SuspendWorldStep) {
                    if (edge.Status == WorldTraversalStatus.Suspended) return "TraversalAlreadySuspended";
                    SetEdge(s, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended)); return null;
                }
                if (edge.Status != WorldTraversalStatus.Suspended) return "TraversalNotSuspended";
                if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";
                if (edge.Running) { string error = PayRun(s, c.Actor); if (error != null) return error; }
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
                var formula = NextFormulaBoundary(s);
                if(formula.HasValue&&formula.Value<=s.RuleClock.AddSeconds(1))return "TimedHandlingBoundaryUnsupported";
            }
            var before = s.RuleClock; string failure = inventory.Resolve(s, c);
            if (failure != null) return failure;
            if (s.RuleClock > before) {
                CreditFormulaWork(s,CampGreens.Subtract(s.RuleClock,before),new System.Collections.Generic.List<string>());
                // No traversal or condition deadline can occur inside the admitted interval.
                TestOnlyClubAttackPolicy.AdvanceConditions(s, ".handling"); RefreshIntervals(s); PauseIncompatibleWork(s);
                if(connectedCombat!=null)ObserveCalendar(s);
            }
            return null;
        }
        public string ValidateState(Snapshot s)
        {
            try {
                if (s.SchemaVersion != (research!=null?Snapshot.FormulaWorkSchema:connectedCombat==null?Snapshot.SharedWorldSchema:Snapshot.CalendarCombatSchema) || s.Receipts.Length != s.Revision) return "InvalidSharedWorldHeader";
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
