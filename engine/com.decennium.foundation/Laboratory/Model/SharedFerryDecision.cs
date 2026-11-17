#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private IEnumerable<Command> DiscoverFerryCommands(Snapshot state,Authority grant)
        {
            const string actor=FerryWraithProfile.Actor;
            var view=ObserveFerryController(state,grant);if(view.Slot==FerryDecisionSlot.Waiting)yield break;
            int index=0;string Id()=>"option."+state.Revision.ToString(CultureInfo.InvariantCulture)+".ferry."+(++index).ToString(CultureInfo.InvariantCulture);
            string turn=state.Encounter.CurrentTurnId;
            if(view.Slot==FerryDecisionSlot.Sanctuary) {
                foreach(var option in DiscoverCastingCommands(state,grant,actor))yield return option;
                yield break;
            }
            if(view.Slot==FerryDecisionSlot.Opportunity) {
                string target=TestOnlyClubAttackPolicy.PendingMove(state).Id;
                yield return new Command(Id(),actor,state.Revision,CommandKind.RespondOpportunityAttack,target,combat:new CombatRequest(turn));
                if(view.SourceAvailable)yield return new Command(Id(),actor,state.Revision,CommandKind.RespondOpportunityAttack,target,
                    combat:new CombatRequest(turn,choice:true,featureId:FerryWraithProfile.Feature));
                yield break;
            }
            if(view.Slot==FerryDecisionSlot.Press) {
                string target=TestOnlyClubAttackPolicy.CurrentPressOffer(state).Id;
                foreach(bool accept in new[]{false,true})yield return new Command(Id(),actor,state.Revision,CommandKind.RespondPress,target,
                    combat:new CombatRequest(turn,choice:accept));
                yield break;
            }
            yield return new Command(Id(),actor,state.Revision,CommandKind.SelectCombatStance,combat:new CombatRequest(turn,stance:(int)CombatStance.Guarded));
            yield return new Command(Id(),actor,state.Revision,CommandKind.EndRegularTurn,turn);
            if(view.SourceAvailable)foreach(var target in view.VisibleOpponents)
                yield return new Command(Id(),actor,state.Revision,CommandKind.AttackCreatureFeature,target.ActorId,
                    combat:new CombatRequest(turn,featureId:FerryWraithProfile.Feature));
            foreach(var step in DiscoverTacticalMovementCommands(state,actor))yield return step;
        }
        public FerryDecisionView ObserveFerryController(Snapshot state,Authority grant)
        {
            const string actor=FerryWraithProfile.Actor;
            if(state?.ContentFingerprint!=ContentFingerprint||!FerryWraithProfile.Active(state)||!FerryWraithController.HasGrant(grant))
                return new FerryDecisionView();
            var pending=PendingSanctuary(state);var move=TestOnlyClubAttackPolicy.PendingMove(state);
            var press=TestOnlyClubAttackPolicy.CurrentPressOffer(state);FerryDecisionSlot slot;
            if(pending!=null) {
                if(pending.ActorId!=actor)return new FerryDecisionView();
                slot=FerryDecisionSlot.Sanctuary;
            } else {
                if(HasPendingRecoveryOffer(state)||ManufacturingChoicePending(state)||PendingDefensiveFormationShift(state)!=null
                    ||PendingCommandStepOffer(state)!=null||state.OverwatchRiderChoices.Any(x=>x.Status==OverwatchRiderChoiceStatus.Pending)
                    ||state.MeleeAttacks.Any(x=>x.Pending))return new FerryDecisionView();
                if(move!=null) {
                    if(move.ResponseIndex>=move.Reactors.Count||move.Reactors[move.ResponseIndex]!=actor)return new FerryDecisionView();
                    slot=FerryDecisionSlot.Opportunity;
                } else if(press!=null) {
                    if(press.ActorId!=actor)return new FerryDecisionView();
                    slot=FerryDecisionSlot.Press;
                } else {
                    if(PendingCalendarChoice(state)||state.Encounter.CurrentActor!=actor)return new FerryDecisionView();
                    slot=FerryDecisionSlot.RegularTurn;
                }
            }
            var own=state.Actors.Single(x=>x.Id==actor);var cell=new CombatCell(own.X,own.Y);
            var seen=state.Actors.Where(x=>x.Id!=actor&&ObservationRules.CanSee(state,actor,x.Id)).ToArray();
            var opponents=seen.Where(x=>state.Encounter.Order.Contains(x.Id)&&!SoldierTacticalFeatures.IsAlly(state,actor,x.Id))
                .Where(x=>pending==null||pending.Source!=SanctuaryAttackSource.Opportunity&&x.Id!=pending.OriginalTargetId)
                .OrderBy(x=>x.Id,StringComparer.Ordinal).Select(x=>new DefenderVisibleOpponent(x.Id,new CombatCell(x.X,x.Y),
                    ObservationGeometry.LineOfEffectClear(state,actor,x.Id),!SanctuaryTargetProhibited(state,actor,x.Id))).ToArray();
            var permissions=TestOnlyClubAttackPolicy.CurrentPermissions(state,actor);
            bool aware=TestOnlyClubAttackPolicy.Aware(state,actor);
            bool canMove=aware&&permissions.VoluntarySpeed&&TestOnlyClubAttackPolicy.RemainingMovement(state,actor)>default(RuleQuantity);
            bool canAttack=aware&&permissions.Action&&!TestOnlyClubAttackPolicy.ActionSpent(state)
                &&TestOnlyClubAttackPolicy.PhysicalAttackFailure(state,actor)==null;
            return new FerryDecisionView(slot,cell,CreatureAttackFailure(state,actor,FerryWraithProfile.Feature)==null,
                aware,TestOnlyClubAttackPolicy.HasStance(state),canAttack,canMove,
                slot==FerryDecisionSlot.Opportunity&&TestOnlyClubAttackPolicy.EligibleOpportunity(state,actor,move),
                move!=null&&opponents.Any(x=>x.ActorId==move.ActorId)?move.ActorId:"",opponents,
                canMove?KnownDefenderApproachCells(state,cell,seen):null);
        }
    }
}
#endif
