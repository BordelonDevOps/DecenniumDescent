#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit fixed two-participant encounter in the supplied arena. The third expedition
    /// member is the independent plot worker. This supplies test facts, not enemy content or AI.</summary>
    public sealed class SharedCombatFixture
    {
        public long EnemyHp { get; }
        public uint Seed { get; }
        public SharedCombatFixture(long enemyHp=26,uint seed=1)
        {if(enemyHp<1||enemyHp>26||seed==0)throw new ArgumentException("Invalid connected combat fixture.");EnemyHp=enemyHp;Seed=seed;}
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        public TestOnlySharedWorldPolicy(RepeatingCrossbowFixture rangedCombat,SharedCombatFixture combat,int walkingSpeed=30,
            ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,walkingSpeed,conditions,terrain)
        {
            if(combat==null||rangedCombat==null)throw new ArgumentException("Repeating crossbow combat requires its connected encounter and explicit shooter fixture.");
            this.rangedCombat=rangedCombat;ContentFingerprint=RepeatingCrossbowFixture.BindFingerprint(ContentFingerprint,rangedCombat);
        }
        private static void SyncCalendarBodies(Snapshot s)
        {
            foreach(var interval in s.WorldIntervals) {
                int start=checked((int)interval.LastStart);var before=s.TacticalActors.Single(x=>x.ActorId==interval.ActorId);
                if(before.LastRegularStart!=start){s.TacticalActors=s.TacticalActors.Select(x=>x.ActorId==interval.ActorId?new ActorTacticalRecord(x.ActorId,start,interval.ReactionAvailable):x).ToArray();CharacterAdvancementRules.RegularStart(s,interval.ActorId,start);TestOnlySharedWorldPolicy.OverwatchRegularStart(s,interval.ActorId,start,s.Revision+1);}
                s.ActorMovement=s.ActorMovement.Select(x=>x.ActorId==interval.ActorId?new ActorMovementRecord(x.ActorId,x.BaseWalkingSpeed,start):x).ToArray();
            }
        }
        private static void ObserveCalendar(Snapshot s)
        {
            var e=s.Encounter;if(e==null)return;int slot=checked((int)s.WorldSchedule.ProcessedSlot);
            if(slot!=e.TurnOrdinal)s.Encounter=new FixedEncounterRecord(e.Id,e.Origin,e.Order,e.StartRevisions.Concat(new[]{s.Revision+1}),e.ObservedOrdinals.Concat(new[]{slot}));
            if(s.InventoryCombat)s.InventoryTurnActor=s.Encounter.CurrentActor;
        }
        private static void PauseParticipantWork(Snapshot s,string actor)
        {
            foreach(var job in s.FormulaWork.Where(x=>x.WorkerId==actor&&x.Status==FormulaWorkStatus.Working).ToArray())PauseFormula(s,job);
            foreach(var crop in s.Crops.Where(x=>x.Tasks.Any(t=>t.WorkerId==actor&&t.Status==CropWorkStatus.Working)).ToArray())CampGreens.Pause(s,crop.Id,actor);
            foreach(var fill in s.WaterFills.Where(x=>x.WorkerId==actor&&x.Status==WaterFillStatus.Working).ToArray())WaterFilling.Pause(s,fill);
            foreach(var intake in s.Intakes.Where(x=>x.ActorId==actor&&x.Status==IntakeStatus.Working).ToArray())OrdinaryInventory.Interrupt(s,intake,IntakeStatus.CombatInterrupted);
            foreach(var attempt in s.SupplyCacheAttempts.Where(x=>x.ActorId==actor&&x.Status==SupplyCacheAttemptStatus.Working).ToArray())InterruptSupplyCacheAttempt(s,attempt);
        }
        private string EnterCalendarCombat(Snapshot s,Command c)
        {
            if(c.Inventory!=null||c.Combat!=null||c.Target!=""||c.X!=0||c.Y!=0||!s.WorldSchedule.Order.Contains(c.Actor))return "InvalidSharedCombatEntry";
            if(s.InventoryCombat)return "AlreadyInTacticalControl";
            if(s.WorldTraversals.Length!=0)return "OffGridCombatEntryUnsupported";
            if(s.WorldSchedule.ProcessedSlot>=int.MaxValue)return "CombatCalendarCapacityReached";
            if(s.Encounter==null)s.Encounter=new FixedEncounterRecord("world.fixed-conflict",s.WorldSchedule.Origin,s.WorldSchedule.Order,new[]{s.Revision+1},new[]{(int)s.WorldSchedule.ProcessedSlot});
            foreach(string actor in s.WorldSchedule.Order)PauseParticipantWork(s,actor);
            // Starts have already been processed by shared advancement. Do not replay one here.
            s.InventoryCombat=true;s.InventoryTurnActor=s.Encounter.CurrentActor;s.InventoryInteractions=Interval(s,s.Encounter.CurrentActor).Interactions;
            PauseIncompatibleRemedies(s);PauseIncompatibleRepairs(s);PauseIncompatibleManufacturing(s);return null;
        }
        internal static bool PendingCalendarChoice(Snapshot s)=>s.MeleeAttacks.Any(x=>x.Pending)||TestOnlyClubAttackPolicy.PendingMove(s)!=null||TestOnlyClubAttackPolicy.CurrentPressOffer(s)!=null;
        private static bool ResolvedConflict(Snapshot s)=>s.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Dead;
        private string ResolveCalendarCombat(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.AdvanceClock)return "TacticalDecisionClockPaused";
            if(c.Kind==CommandKind.AttackRepeatingCrossbow||c.Kind==CommandKind.ReloadRepeatingCrossbow)return ResolveRepeatingCrossbow(s,c);
            if(c.Kind==CommandKind.DispatchConditionEvent) {
                string error=bodies.Resolve(s,c);if(error==null)PauseIncompatibleWork(s);return error;
            }
            if(c.Kind==CommandKind.EndRegularTurn||c.Kind==CommandKind.EndFixedEncounter) {
                if(c.Inventory!=null||c.Combat!=null||c.X!=0||c.Y!=0||c.Actor!=s.Encounter.CurrentActor||c.Target!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                bool exit=c.Kind==CommandKind.EndFixedEncounter;
                if(exit&&!ResolvedConflict(s))return "ConflictNotResolved";
                if(TestOnlyClubAttackPolicy.Aware(s,c.Actor)&&!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
                if(s.WorldSchedule.ProcessedSlot>=int.MaxValue-1)return "CombatCalendarCapacityReached";
                CharacterAdvancementRules.EndRegularTurn(s,c.Actor,s.Encounter.TurnOrdinal);
                AdvanceTo(s,s.WorldSchedule.Start(s.WorldSchedule.ProcessedSlot+1),exit,c);
                if(s.ManufacturingAdvance!=null)return null;
                s.InventoryInteractions=Interval(s,s.Encounter.CurrentActor).Interactions;
                // Time and consequences are committed even if the exit predicate no longer holds.
                if(exit&&ResolvedConflict(s)&&!PendingCalendarChoice(s)){s.InventoryCombat=false;s.InventoryTurnActor="";s.InventoryInteractions=0;CharacterAdvancementRules.TacticalExit(s);}
                return null;
            }
            if(!s.WorldSchedule.Order.Contains(c.Actor))return "ActorOutsideEncounter";
            if(c.Kind==CommandKind.SelectCombatStance&&c.Combat?.Stance==(int)CombatStance.Mobile)return "SharedMobileDistanceNotImplemented";
            if((c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.AttackUnarmed)&&!s.WorldSchedule.Order.Contains(c.Target))return "TargetOutsideEncounter";
            if(c.Kind==CommandKind.EncounterDash) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                if(c.Inventory!=null||c.Combat!=null||c.X!=0||c.Y!=0||c.Actor!=s.Encounter.CurrentActor||c.Target!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
                if(Interval(s,c.Actor).ActionSpent)return "ActionAlreadySpent";
                return PayRun(s,c.Actor);
            }
            if(c.Kind==CommandKind.ActivateTacticalReposition) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                return CharacterAdvancementRules.ActivateTacticalReposition(s,c);
            }
            if(c.Kind==CommandKind.DesignateOverwatch) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                return ResolveOverwatchDesignation(s,c);
            }
            if(c.Kind==CommandKind.CurePeriodicRider)return ResolvePeriodicMedicine(s,c);
            if((c.Kind==CommandKind.HandleInventory||c.Kind==CommandKind.HandleVessel)&&s.SchemaVersion>=Snapshot.SupplyCacheSchema) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
                if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
                if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
                var interval=Interval(s,c.Actor);
                if(s.InventoryInteractions!=interval.Interactions)return "TacticalInteractionLedgerMismatch";
                if(interval.Interactions>=2)return "InteractionBudgetUnavailable";
                if(interval.Interactions==1&&interval.ActionSpent)return "ActionAlreadySpent";
                if(interval.Interactions==1&&!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
                string handling=inventory.Resolve(s,c);if(handling!=null)return handling;
                var spent=Interval(s,c.Actor).SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
                PauseIncompatibleWork(s);return null;
            }
            bool action=c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.AttackUnarmed||c.Kind==CommandKind.Disengage;
            string failure=bodies.Resolve(s,c);if(failure!=null)return failure;
            if(action)SetInterval(s,Interval(s,c.Actor).PayAction());
            PauseIncompatibleWork(s);return null;
        }
    }
}
#endif
