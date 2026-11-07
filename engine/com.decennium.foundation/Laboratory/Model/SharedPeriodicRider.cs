#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const string PeriodicImmunitySource="TEST_ONLY.periodic-family-immunity";
        private static bool PeriodicEventCommand(CommandKind kind)=>kind==CommandKind.DispatchFixturePeriodicRider
            ||kind==CommandKind.SetPeriodicRiderSuppression||kind==CommandKind.SetPeriodicFamilyImmunity
            ||kind==CommandKind.ApplyFixtureMagicalHealing;
        private static string EventIdentity(string kind,string value)
        {
            using(var sha=SHA256.Create())return "periodic."+kind+"."+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value)).Take(12).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static void AppendPeriodicEvent(Snapshot s,PeriodicRiderEventRecord value)
        {
            if(s.PeriodicRiderEvents.Length==PeriodicRiderValidation.MaxEvents)throw new ArgumentException("Periodic event history full.");
            if(s.PeriodicRiderEvents.Any(x=>x.EventId==value.EventId))throw new InvalidOperationException("Periodic event identity already exists.");
            s.PeriodicRiderEvents=s.PeriodicRiderEvents.Concat(new[]{value}).ToArray();
        }
        private static bool ImmuneToPeriodicFamily(Snapshot s,string target,string family)
            =>s.PeriodicImmunities.Any(x=>x.TargetId==target&&x.FamilyId==family&&x.Present);
        private static long NextStartSlot(Snapshot s,string actor)
        {
            var schedule=s.WorldSchedule;int index=schedule.Order.ToList().IndexOf(actor);
            if(index<0)throw new ArgumentException("Periodic target is outside the shared calendar.");
            long first=checked(schedule.ProcessedSlot+1);long offset=(index-first%schedule.Order.Count+schedule.Order.Count)%schedule.Order.Count;
            return checked(first+offset);
        }
        private string ResolvePeriodicEvent(Snapshot s,Command c)
        {
            if(periodicRider==null||s.SchemaVersion<Snapshot.PeriodicRiderSchema)return "PeriodicRiderNotImplemented";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null)return "InvalidPeriodicRiderPayload";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.DispatchFixturePeriodicRider) {
                if(c.X!=0||c.Y!=0)return "InvalidPeriodicRiderEvent";
                var fact=periodicRider.Applications.SingleOrDefault(x=>x.EventId==c.Target&&x.OwnerId==c.Actor);
                if(fact==null)return "UnknownPeriodicRiderEvent";
                if(!s.InventoryCombat||s.Encounter==null)return "PeriodicRiderRequiresTacticalEvent";
                if(fact.At!=s.RuleClock)return "WrongPeriodicRiderEventTime";
                if(s.PeriodicRiderEvents.Any(x=>x.EventId==fact.EventId))return "PeriodicRiderEventAlreadyResolved";
                if(s.Lives.Single(x=>x.ActorId==fact.OwnerId).Dead||s.Lives.Single(x=>x.ActorId==fact.OwnerId).Hp==0)return "PeriodicSourceCannotAct";
                if(s.Lives.Single(x=>x.ActorId==fact.TargetId).Dead)return "PeriodicTargetNotLiving";
                uint random=s.RandomState;var immune=ImmuneToPeriodicFamily(s,fact.TargetId,PeriodicRiderFixture.FamilyId);
                if(immune) {
                    AppendPeriodicEvent(s,new PeriodicRiderEventRecord(fact.EventId,PeriodicRiderEventKind.Prevented,PeriodicRiderOutcome.Immune,
                        s.Revision+1,s.RuleClock,-1,c.Actor,fact.TargetId,"",PeriodicRiderFixture.SourceId,true,0,0,0,0,0,0,random,random,0));
                    return null;
                }
                long marker=NextStartSlot(s,fact.TargetId);
                var prior=s.PeriodicRiders.SingleOrDefault(x=>x.Present&&x.OwnerId==fact.OwnerId&&x.TargetId==fact.TargetId
                    &&x.SourceId==PeriodicRiderFixture.SourceId&&x.ProfileId==PeriodicRiderFixture.ProfileId);
                if(prior!=null) {
                    var refreshed=prior.Refresh(marker);
                    s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==prior.Id?refreshed:x).ToArray();
                    AppendPeriodicEvent(s,new PeriodicRiderEventRecord(fact.EventId,PeriodicRiderEventKind.Refreshed,PeriodicRiderOutcome.None,
                        s.Revision+1,s.RuleClock,-1,c.Actor,fact.TargetId,prior.Id,PeriodicRiderFixture.SourceId,false,0,0,fact.ApplyingDc,0,0,0,random,random,0));
                } else {
                    if(s.PeriodicRiders.Length==PeriodicRiderValidation.MaxRiders)return "PeriodicRiderCapacityReached";
                    var rider=new PeriodicRiderRecord(fact.RiderId,PeriodicRiderFixture.ProfileId,PeriodicRiderFixture.FamilyId,fact.OwnerId,
                        PeriodicRiderFixture.SourceId,fact.TargetId,fact.EventId,"piercing",fact.ApplyingDc,s.Revision+1,s.RuleClock,marker,1);
                    s.PeriodicRiders=s.PeriodicRiders.Concat(new[]{rider}).ToArray();
                    AppendPeriodicEvent(s,new PeriodicRiderEventRecord(fact.EventId,PeriodicRiderEventKind.Applied,PeriodicRiderOutcome.None,
                        s.Revision+1,s.RuleClock,-1,c.Actor,fact.TargetId,rider.Id,PeriodicRiderFixture.SourceId,false,0,0,fact.ApplyingDc,0,0,0,random,random,0));
                }
                return null;
            }
            if(c.Kind==CommandKind.SetPeriodicRiderSuppression) {
                if((c.X!=0&&c.X!=1)||c.Y!=0)return "InvalidPeriodicSuppression";
                var rider=s.PeriodicRiders.SingleOrDefault(x=>x.Id==c.Target&&x.Present);
                if(rider==null||rider.OwnerId!=c.Actor||rider.ProfileId!=PeriodicRiderFixture.ProfileId)return "PeriodicRiderUnavailable";
                bool value=c.X==1;if(rider.Suppressed==value)return "PeriodicSuppressionUnchanged";
                s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==rider.Id?x.WithSuppressed(value):x).ToArray();
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(EventIdentity("suppression",N(s.Revision+1)),PeriodicRiderEventKind.Suppression,
                    PeriodicRiderOutcome.None,s.Revision+1,s.RuleClock,-1,c.Actor,rider.TargetId,rider.Id,rider.SourceId,value,0,0,0,0,0,0,s.RandomState,s.RandomState,0));
                return null;
            }
            if(c.Kind==CommandKind.SetPeriodicFamilyImmunity) {
                if(c.Target!=c.Actor||(c.X!=0&&c.X!=1)||c.Y!=0)return "InvalidPeriodicImmunity";
                var active=s.PeriodicImmunities.SingleOrDefault(x=>x.TargetId==c.Actor&&x.FamilyId==PeriodicRiderFixture.FamilyId&&x.Present);
                if(c.X==1) {
                    if(active!=null)return "PeriodicImmunityAlreadyPresent";
                    if(s.PeriodicImmunities.Length==PeriodicRiderValidation.MaxImmunities)return "PeriodicImmunityCapacityReached";
                    var grant=new PeriodicFamilyImmunityRecord("periodic.immunity."+N(s.Revision+1),c.Actor,PeriodicRiderFixture.FamilyId,PeriodicImmunitySource,s.RuleClock);
                    s.PeriodicImmunities=s.PeriodicImmunities.Concat(new[]{grant}).ToArray();
                } else {
                    if(active==null)return "PeriodicImmunityUnavailable";
                    s.PeriodicImmunities=s.PeriodicImmunities.Select(x=>x.Id==active.Id?x.End(s.RuleClock):x).ToArray();
                }
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(EventIdentity("immunity",N(s.Revision+1)),PeriodicRiderEventKind.FamilyImmunity,
                    PeriodicRiderOutcome.None,s.Revision+1,s.RuleClock,-1,c.Actor,c.Actor,"",PeriodicImmunitySource,c.X==1,0,0,0,0,0,0,s.RandomState,s.RandomState,0));
                return null;
            }
            if(c.Kind==CommandKind.ApplyFixtureMagicalHealing) {
                var fact=periodicRider.Healing;
                if(fact==null||fact.CasterId!=c.Actor||fact.TargetId!=c.Target||c.X!=0||c.Y!=0)return "UnknownFixtureHealingEvent";
                if(s.PeriodicRiderEvents.Any(x=>x.EventId==fact.EventId))return "FixtureHealingAlreadyApplied";
                var before=s.Lives.Single(x=>x.ActorId==fact.TargetId);var view=View(s,fact.TargetId);
                long potential=view.HealingPotential(fact.Potential),gain=0;bool healingOccurred=potential>0&&!before.Dead;
                if(healingOccurred) {
                    var after=PlaytestLife.Heal(ActorLifeRules.Read(before),potential);gain=Math.Max(0,after.Hp-before.Hp);
                    TestOnlyClubAttackPolicy.ApplyLife(s,before,after);
                    foreach(var rider in s.PeriodicRiders.Where(x=>x.TargetId==fact.TargetId&&x.ProfileId==PeriodicRiderFixture.ProfileId&&x.Present).ToArray())
                        s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==rider.Id?x.End(s.RuleClock,"healing"):x).ToArray();
                    PauseIncompatibleWork(s);ReconcileTraversal(s);
                }
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(fact.EventId,PeriodicRiderEventKind.MagicalHealing,
                    healingOccurred?PeriodicRiderOutcome.HealingCure:PeriodicRiderOutcome.NoPositiveHealing,s.Revision+1,s.RuleClock,-1,c.Actor,fact.TargetId,"",
                    "TEST_ONLY.fixture-positive-potential-healing",healingOccurred,0,0,0,0,potential,gain,s.RandomState,s.RandomState,0));
                return null;
            }
            return "PeriodicRiderCommandNotImplemented";
        }
        private static RuleTime? NextPeriodicMarker(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.PeriodicRiderSchema||s.PeriodicRiders.Length==0)return null;
            var starts=s.PeriodicRiders.Where(x=>x.Present).Select(x=>s.WorldSchedule.Start(x.NextStartSlot)).Where(x=>x>s.RuleClock).ToArray();
            return starts.Length==0?(RuleTime?)null:starts.Min();
        }
        private void ProcessPeriodicRiderMarker(Snapshot s,long previousSlot)
        {
            if(periodicRider==null||s.WorldSchedule.ProcessedSlot==previousSlot||s.WorldSchedule.Start(s.WorldSchedule.ProcessedSlot)!=s.RuleClock)return;
            long slot=s.WorldSchedule.ProcessedSlot;
            var due=s.PeriodicRiders.Where(x=>x.Present&&x.NextStartSlot==slot).OrderBy(x=>x.TargetId,StringComparer.Ordinal)
                .ThenBy(x=>x.ApplicationOrder).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            if(due.Length==0)return;
            foreach(var group in due.GroupBy(x=>x.TargetId,StringComparer.Ordinal)) {
                var targetId=group.Key;var target=s.Lives.Single(x=>x.ActorId==targetId);bool dead=target.Dead;
                var eligible=group.Where(x=>!dead&&!x.Suppressed&&!ImmuneToPeriodicFamily(s,x.TargetId,x.FamilyId))
                    .OrderBy(x=>x.ApplicationOrder).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
                string winner=eligible.FirstOrDefault()?.Id??"";
                foreach(var rider in group.OrderBy(x=>x.ApplicationOrder).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    uint beforeRandom=s.RandomState;int die=0;long damage=0,words=0;uint afterRandom=beforeRandom;
                    bool immune=ImmuneToPeriodicFamily(s,rider.TargetId,rider.FamilyId);
                    PeriodicRiderOutcome outcome;
                    if(dead)outcome=PeriodicRiderOutcome.TargetDead;
                    else if(immune)outcome=PeriodicRiderOutcome.Immune;
                    else if(rider.Suppressed)outcome=PeriodicRiderOutcome.Suppressed;
                    else if(rider.Id!=winner)outcome=PeriodicRiderOutcome.FamilyLost;
                    else {
                        var draw=DiceStream.Draw(s.RandomState,4);die=draw.Value+1;afterRandom=draw.NextState;words=draw.WordsConsumed;
                        damage=CharacterAdvancementRules.ReduceIncomingDamage(s,rider.TargetId,die);
                        if(View(s,rider.TargetId).Has(ConditionKind.Petrified))damage=PlaytestConditions.PetrifiedDamage(damage);
                        var character=CharacterRuleFacts.ForActor(s,rider.TargetId);
                        int constitutionSave=checked(character.AbilityModifier(CharacterAbility.Constitution)
                            +CharacterAdvancementRules.SaveProficiencyBonus(s,rider.TargetId,"CON"));
                        var result=PlaytestDamageDice.Resolve(ActorLifeRules.Read(target),damage,s.RuleClock,afterRandom,
                            constitutionSaveModifier:constitutionSave,melee:false);
                        s.RandomState=result.NextRandomState;afterRandom=s.RandomState;words=checked(words+result.WordsConsumed);
                        TestOnlyClubAttackPolicy.ApplyLife(s,target,result.Outcome.State);
                        target=s.Lives.Single(x=>x.ActorId==rider.TargetId);outcome=PeriodicRiderOutcome.Damage;
                        PauseIncompatibleWork(s);ReconcileTraversal(s);
                    }
                    s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==rider.Id?x.End(s.RuleClock,"tick"):x).ToArray();
                    AppendPeriodicEvent(s,new PeriodicRiderEventRecord(EventIdentity("tick",rider.Id+"|"+slot.ToString(CultureInfo.InvariantCulture)),
                        PeriodicRiderEventKind.Tick,outcome,s.Revision+1,s.RuleClock,slot,rider.OwnerId,rider.TargetId,rider.Id,rider.SourceId,
                        rider.Id==winner,0,0,0,die,damage,0,beforeRandom,afterRandom,words));
                }
            }
        }
        private string ResolvePeriodicMedicine(Snapshot s,Command c)
        {
            if(periodicRider==null||s.SchemaVersion<Snapshot.PeriodicRiderSchema)return "PeriodicRiderNotImplemented";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.X!=0||c.Y!=0)return "InvalidMedicineRequest";
            if(!s.InventoryCombat||s.Encounter==null)return "MedicineRequiresTacticalAction";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Target=="")return "WrongRegularTurn";
            var rider=s.PeriodicRiders.SingleOrDefault(x=>x.Id==c.Target&&x.Present);
            if(rider==null)return "PeriodicRiderUnavailable";
            var medic=s.Actors.Single(x=>x.Id==c.Actor);var patient=s.Actors.Single(x=>x.Id==rider.TargetId);
            if(medic.Id!=patient.Id&&Math.Max(Math.Abs((long)medic.X-patient.X),Math.Abs((long)medic.Y-patient.Y))>1)return "MedicineTargetOutOfReach";
            if(AvailableHands(s,c.Actor)<1)return "UsableHandRequired";
            var interval=Interval(s,c.Actor);if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
            int modifier=AbilityCheckRules.Derive(s,c.Actor,"medicine",CharacterAbility.Wisdom).Total;
            var view=View(s,c.Actor);bool disadvantage=view.Clauses.Has(ConditionClause.Poisoned);
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before,disadvantage?0:0,disadvantage?1:0);
            var check=PlaytestRolls.TaskCheck(roll.Natural,modifier,rider.ApplyingDc);bool success=check.Success;
            var degree=check.Degree==TaskDegree.CriticalFailure?PeriodicRiderCheckDegree.CriticalFailure
                :check.Degree==TaskDegree.Failure?PeriodicRiderCheckDegree.Failure
                :check.Degree==TaskDegree.Success?PeriodicRiderCheckDegree.Success:PeriodicRiderCheckDegree.CriticalSuccess;
            SetInterval(s,interval.PayAction());s.RandomState=roll.NextRandomState;
            if(success)s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==rider.Id?x.End(s.RuleClock,"medicine"):x).ToArray();
            AppendPeriodicEvent(s,new PeriodicRiderEventRecord(EventIdentity("medicine",N(s.Revision+1)),PeriodicRiderEventKind.Medicine,
                success?PeriodicRiderOutcome.MedicineSuccess:PeriodicRiderOutcome.MedicineFailure,s.Revision+1,s.RuleClock,-1,c.Actor,rider.TargetId,rider.Id,
                "medicine",success,roll.Natural,modifier,rider.ApplyingDc,0,0,0,before,s.RandomState,roll.WordsConsumed,degree,check.Total));
            return null;
        }
    }
}
#endif
