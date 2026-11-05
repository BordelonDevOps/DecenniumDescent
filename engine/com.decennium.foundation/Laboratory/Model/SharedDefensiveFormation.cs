#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private sealed class DefensiveFormationAssessment
        {
            public string[] Recipients;
        }

        internal static DefensiveFormationShiftRecord PendingDefensiveFormationShift(Snapshot s)
            =>s.DefensiveFormations.Where(x=>x.Active).OrderByDescending(x=>x.CreatedRevision)
                .SelectMany(x=>x.Shifts).SingleOrDefault(x=>x.Status==DefensiveFormationShiftStatus.AwaitingResponse);

        private DefensiveFormationActivationRecord ActivationForShift(Snapshot s,DefensiveFormationShiftRecord shift)
            =>shift==null?null:s.DefensiveFormations.SingleOrDefault(x=>x.Active&&x.Shifts.Any(y=>y.Id==shift.Id));

        private static bool FormationAlly(Snapshot s,string source,string target)
            =>source==target||s.TacticalAllies.Any(x=>x.Includes(source)&&x.Other(source)==target);

        private string AssessDefensiveFormation(Snapshot s,Command c,out DefensiveFormationAssessment facts)
        {
            facts=null;
            if(s.SchemaVersion<Snapshot.DefensiveFormationSchema)return "DefensiveFormationNotImplemented";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.SuppressionFire!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.Target!=""||c.X!=0||c.Y!=0)return "InvalidDefensiveFormationRequest";
            if(!s.InventoryCombat||s.Encounter==null)return "DefensiveFormationRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            var request=c.DefensiveFormation;
            if(request==null||request.TurnId!=s.Encounter.CurrentTurnId||c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterFeatureIds.DefensiveFormation
                &&x.ClassName=="Soldier"&&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))return "FeatureNotOwned";
            if(s.DefensiveFormations.Any(x=>x.SourceActorId==c.Actor&&x.EncounterId==s.Encounter.Id))return "DefensiveFormationAlreadyUsed";
            if(!CharacterAdvancementRules.BonusActionAvailable(s,c.Actor))return "BonusActionUnavailable";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).BonusAction)return "ConditionPreventsBonusAction";
            if(request.RecipientIds.Length<1||request.RecipientIds.Length>3)return "DefensiveFormationRecipientCountInvalid";
            var source=s.Actors.SingleOrDefault(x=>x.Id==c.Actor);
            if(source==null)return "UnknownWorldActor";
            foreach(string recipientId in request.RecipientIds) {
                var recipient=s.Actors.SingleOrDefault(x=>x.Id==recipientId);
                if(recipient==null||!s.WorldSchedule.Order.Contains(recipientId))return "RecipientOutsideEncounter";
                if(!FormationAlly(s,c.Actor,recipientId))return "RecipientMustBeAlly";
                if(PlanarCombatGeometry.DistanceFeet(new CombatCell(source.X,source.Y),new CombatCell(recipient.X,recipient.Y))>15)
                    return "RecipientOutOfRange";
            }
            if(s.DefensiveFormations.Length>=DefensiveFormationValidation.MaxActivations)return "DefensiveFormationHistoryCapacityReached";
            if(s.Receipts.Length>=512)return "CommandHistoryCapacityReached";
            facts=new DefensiveFormationAssessment{Recipients=request.RecipientIds.ToArray()};
            return null;
        }

        private string AssessDefensiveFormationResponse(Snapshot s,Command c,out DefensiveFormationActivationRecord activation,
            out DefensiveFormationShiftRecord shift)
        {
            activation=null;shift=null;
            if(s.SchemaVersion<Snapshot.DefensiveFormationSchema)return "DefensiveFormationNotImplemented";
            if(c.Inventory!=null||c.Advancement!=null||c.Ranged!=null||c.SuppressionFire!=null||c.DefensiveFormation!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.Combat==null||c.Combat.WeaponId!=""||c.Combat.Stance!=0
                ||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||c.Combat.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidDefensiveFormationResponse";
            var pending=PendingDefensiveFormationShift(s);activation=ActivationForShift(s,pending);
            if(activation==null||pending==null)return "NoPendingDefensiveFormationChoice";
            if(c.Actor!=pending.RecipientActorId||c.Target!=activation.Id||c.Combat.TurnId!=activation.TurnId)return "WrongDefensiveFormationController";
            shift=pending;
            if(!c.Combat.Choice) {
                if(c.X!=0||c.Y!=0||c.Combat.WeaponId!="")return "InvalidDefensiveFormationResponse";
                return null;
            }
            string failure=bodies.DefensiveFormationDestinationFailure(s,activation.Id,c.Actor,s.Actors.Single(x=>x.Id==c.Actor).X,
                s.Actors.Single(x=>x.Id==c.Actor).Y,c.X,c.Y);
            return failure;
        }

        private bool FormationCanMove(Snapshot s,string actor)
            =>bodies.DefensiveFormationCanMove(s,actor);

        private long FormationExpirySlot(Snapshot s,string actor)
        {
            int index=Array.IndexOf(s.WorldSchedule.Order.ToArray(),actor);long count=s.WorldSchedule.Order.Count;
            if(index<0||count<1)throw new InvalidOperationException("Defensive Formation owner has no world schedule slot.");
            long current=s.WorldSchedule.SlotAt(s.RuleClock),candidate=index;
            return candidate<=current?checked(candidate+checked(((current-candidate)/count+1)*count)):candidate;
        }

        private void UpdateFormation(Snapshot s,DefensiveFormationActivationRecord value)
            =>s.DefensiveFormations=s.DefensiveFormations.Select(x=>x.Id==value.Id?value:x).ToArray();

        private string ResolveDefensiveFormation(Snapshot s,Command c)
        {
            string failure=AssessDefensiveFormation(s,c,out var facts);if(failure!=null)return failure;
            if(!CharacterAdvancementRules.SpendBonusAction(s,c.Actor))return "BonusActionUnavailable";
            long revision=s.Revision+1,expiry=FormationExpirySlot(s,c.Actor);
            var shifts=facts.Recipients.Select((id,index)=>new DefensiveFormationShiftRecord(
                c.Id+".shift."+index.ToString(CultureInfo.InvariantCulture),index,id,DefensiveFormationShiftStatus.Queued,revision)).ToArray();
            var activation=new DefensiveFormationActivationRecord(c.Id,c.Actor,s.Encounter.Id,s.Encounter.CurrentTurnId,s.Encounter.TurnOrdinal,
                revision,revision,s.RuleClock,expiry,shifts);
            s.DefensiveFormations=s.DefensiveFormations.Concat(new[]{activation}).ToArray();
            AdvanceFormationSequence(s,activation.Id,c.Id);
            return null;
        }

        private void AdvanceFormationSequence(Snapshot s,string activationId,string resolutionCommandId)
        {
            var activation=s.DefensiveFormations.Single(x=>x.Id==activationId&&x.Active);
            foreach(var shift in activation.Shifts) {
                if(shift.Status!=DefensiveFormationShiftStatus.Queued)continue;
                if(!FormationCanMove(s,shift.RecipientActorId)) {
                    activation=activation.UpdateShift(shift.Skip(s.Revision+1,resolutionCommandId),s.Revision+1);
                    UpdateFormation(s,activation);continue;
                }
                activation=activation.UpdateShift(shift.Await(s.Revision+1),s.Revision+1);
                UpdateFormation(s,activation);return;
            }
        }

        private string ResolveDefensiveFormationResponse(Snapshot s,Command c)
        {
            string failure=AssessDefensiveFormationResponse(s,c,out var activation,out var shift);if(failure!=null)return failure;
            if(!c.Combat.Choice) {
                UpdateFormation(s,activation.UpdateShift(shift.Decline(s.Revision+1,c.Id),s.Revision+1));
                AdvanceFormationSequence(s,activation.Id,c.Id);return null;
            }
            string moveId="move."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            var moving=shift.BeginMove(s.Revision+1,c.Id,moveId);
            UpdateFormation(s,activation.UpdateShift(moving,s.Revision+1));
            failure=bodies.BeginDefensiveFormationShift(s,activation.Id,c.Actor,c.X,c.Y);
            if(failure!=null)return failure;
            return null;
        }

        private bool FormationContinuationBlocked(Snapshot s)
            =>TestOnlyClubAttackPolicy.PendingMove(s)!=null||s.MeleeAttacks.Any(x=>x.Pending)
                ||TestOnlyClubAttackPolicy.CurrentPressOffer(s)!=null||s.OverwatchOffers.Any(x=>x.Status==OverwatchOfferStatus.Pending)
                ||s.OverwatchRiderChoices.Any(x=>x.Status==OverwatchRiderChoiceStatus.Pending);

        private void FinishDefensiveFormationContinuation(Snapshot s,string commandId)
        {
            if(FormationContinuationBlocked(s))return;
            foreach(var activation in s.DefensiveFormations.Where(x=>x.Active).ToArray()) {
                var shift=activation.Shifts.SingleOrDefault(x=>x.Status==DefensiveFormationShiftStatus.Moving);
                if(shift==null)continue;
                var move=s.TacticalMoves.SingleOrDefault(x=>x.Id==shift.MoveId);
                if(move==null||move.Pending)return;
                var resolved=move.Status==TacticalMoveStatus.Completed?shift.CompleteMove(s.Revision+1,commandId):shift.Skip(s.Revision+1,commandId);
                var updated=activation.UpdateShift(resolved,s.Revision+1);UpdateFormation(s,updated);
                AdvanceFormationSequence(s,activation.Id,commandId);
            }
        }

        private bool HasMovingDefensiveFormation(Snapshot s)
            =>s.DefensiveFormations.Any(x=>x.Active&&x.Shifts.Any(y=>y.Status==DefensiveFormationShiftStatus.Moving));

        private DefensiveFormationActivationRecord CurrentActivationForPendingShift(Snapshot s)
            =>ActivationForShift(s,PendingDefensiveFormationShift(s));

        private System.Collections.Generic.IEnumerable<Command> DiscoverDefensiveFormationCommands(Snapshot s,string actor)
        {
            int index=0;string turn=s.Encounter.CurrentTurnId;
            var pending=PendingDefensiveFormationShift(s);
            if(pending!=null) {
                if(actor!=pending.RecipientActorId)yield break;
                var activation=CurrentActivationForPendingShift(s);var result=new System.Collections.Generic.List<Command>();
                var decline=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".formation.decline",actor,s.Revision,
                    CommandKind.RespondDefensiveFormation,activation.Id,combat:new CombatRequest(turn,choice:false));
                if(AssessDefensiveFormationResponse(s,decline,out _,out _) == null)result.Add(decline);
                var body=s.Actors.Single(x=>x.Id==actor);
                foreach(var delta in new[]{new[]{-1,-1},new[]{-1,0},new[]{-1,1},new[]{0,-1},new[]{0,1},new[]{1,-1},new[]{1,0},new[]{1,1}}) {
                    var move=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".formation.move."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.RespondDefensiveFormation,activation.Id,body.X+delta[0],body.Y+delta[1],
                        combat:new CombatRequest(turn,choice:true));
                    if(AssessDefensiveFormationResponse(s,move,out _,out _) == null)result.Add(move);
                }
                foreach(var command in result)yield return command;
                yield break;
            }
            if(actor!=s.Encounter.CurrentActor||s.DefensiveFormations.Any(x=>x.SourceActorId==actor&&x.EncounterId==s.Encounter.Id))
                yield break;
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==actor&&x.FeatureId==CharacterFeatureIds.DefensiveFormation
                &&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))yield break;
            var eligible=s.Actors.Where(x=>s.WorldSchedule.Order.Contains(x.Id)&&FormationAlly(s,actor,x.Id)
                &&PlanarCombatGeometry.DistanceFeet(new CombatCell(s.Actors.Single(a=>a.Id==actor).X,s.Actors.Single(a=>a.Id==actor).Y),
                    new CombatCell(x.X,x.Y))<=15).Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            var recipientLists=new System.Collections.Generic.List<string[]>();
            foreach(string recipient in eligible)recipientLists.Add(new[]{recipient});
            for(int i=0;i<eligible.Length;i++)for(int j=i+1;j<eligible.Length;j++) {
                recipientLists.Add(new[]{eligible[i],eligible[j]});recipientLists.Add(new[]{eligible[j],eligible[i]});
            }
            foreach(var ids in recipientLists) {
                var command=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".formation.activate."+(index++).ToString(CultureInfo.InvariantCulture),
                    actor,s.Revision,CommandKind.ActivateDefensiveFormation,
                    defensiveFormation:new DefensiveFormationRequest(turn,ids));
                if(AssessDefensiveFormation(s,command,out _) == null)yield return command;
            }
        }

        private CommandQueryResult QueryDefensiveFormation(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.ActivateDefensiveFormation) {
                string failure=AssessDefensiveFormation(s,c,out _);
                var costs=failure==null?new[]{new CommandCost("bonus-action","",1)}:Array.Empty<CommandCost>();
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            string responseFailure=AssessDefensiveFormationResponse(s,c,out _,out _);
            return new CommandQueryResult(true,responseFailure==null,responseFailure??"Available",s.Revision,Array.Empty<CommandCost>());
        }
    }
}
#endif
