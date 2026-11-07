#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Schema58 TEST_ONLY nonspell Ready Action slice. It persists one named target and
    /// one ordinary club/unarmed attack, then resolves completed movement triggers in the shared
    /// post-step queue. It deliberately does not implement Ready spells, movement, or class actions.</summary>
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static string ReadyIdentity(string input)
        {
            using(var sha=SHA256.Create())return "ready."+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(input)).Take(16)
                .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }

        private static ReadyOccurrenceRecord PendingReadyOccurrence(Snapshot s)
            =>s.ReadyOccurrences.Where(x=>x.Status==ReadyOccurrenceStatus.Pending)
                .OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.SourceAppliedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).FirstOrDefault();

        private static RuleTime? NextReadyActionExpiry(Snapshot s)
        {
            var deadlines=s.ReadyActions.Where(x=>x.Armed&&x.ExpiresAt>s.RuleClock).Select(x=>x.ExpiresAt).ToArray();
            return deadlines.Length==0?(RuleTime?)null:deadlines.Min();
        }

        private string AssessReadyDeclaration(Snapshot s,Command c)
        {
            if(!readyActionEnabled||s.SchemaVersion!=Snapshot.ReadyActionSchema)return "ReadyActionNotEnabled";
            if(c.Inventory!=null||c.Combat==null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null||c.HarvestSelection!=null
                ||c.MiningSelection!=null||c.ProspectingExposure!=null||c.X!=5||c.Y!=0)return "InvalidReadyActionRequest";
            if(!s.InventoryCombat||s.Encounter==null||s.WorldSchedule==null)return "ReadyActionRequiresTacticalCombat";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Combat.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            if(!s.WorldSchedule.Order.Contains(c.Target)||c.Target==c.Actor)return "TargetOutsideEncounter";
            if(SoldierTacticalFeatures.IsAlly(s,c.Actor,c.Target))return "TargetMustBeEnemy";
            if(s.Lives.Single(x=>x.ActorId==c.Target).Dead)return "InvalidLivingTarget";
            if(!TestOnlyClubAttackPolicy.CanSee(s,c.Actor,c.Target))return "ReadyTriggerNotPerceived";
            if(c.Combat.Stance!=0||c.Combat.Choice||c.Combat.PressInstruction!=PressHitInstruction.KeepExisting
                ||!Enum.IsDefined(typeof(AttackKnockoutMode),c.Combat.Knockout))return "InvalidReadyActionRequest";
            if(Interval(s,c.Actor).ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action||!ActorLifeRules.CanAct(s,c.Actor))return "ConditionPreventsAction";
            if(TestOnlyClubAttackPolicy.Aware(s,c.Actor)&&!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
            if(TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,c.Actor)!=null)return "PhysicalAttackUnavailable";
            if(c.Combat.WeaponId!="") {
                var club=s.Clubs.SingleOrDefault(x=>x.Id==c.Combat.WeaponId);
                if(club==null||club.ProfileId!=TestOnlyClubAttackPolicy.ClubProfile||club.HeldBy!=c.Actor
                    ||club.CustodianId!=c.Actor||!s.Lives.Single(x=>x.ActorId==c.Actor).HeldItems.Contains(club.Id))return "ClubNotHeld";
            }
            if(s.ReadyActions.Length>=ReadyActionValidation.MaxActions||s.ReadyOccurrences.Length>=ReadyActionValidation.MaxOccurrences)
                return "ReadyActionHistoryCapacityReached";
            return null;
        }

        private bool TryReadyAttack(Snapshot s,ReadyOccurrenceRecord occurrence,out string attackFailure)
        {
            attackFailure="ReadyActionUnavailable";
            var action=occurrence==null?null:s.ReadyActions.SingleOrDefault(x=>x.Id==occurrence.ReadyActionId&&x.Armed);
            if(action==null||!s.InventoryCombat||s.Encounter==null||!s.WorldSchedule.Order.Contains(action.ActorId)
                ||!s.WorldSchedule.Order.Contains(action.TargetId)||!ActorLifeRules.CanAct(s,action.ActorId)
                ||!Interval(s,action.ActorId).ReactionAvailable||!s.TacticalActors.Any(x=>x.ActorId==action.ActorId&&x.ReactionAvailable)
                ||!Permissions(s,action.ActorId).Reaction||TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,action.ActorId)!=null
                ||TestOnlyClubAttackPolicy.ActiveStance(s,action.ActorId)?.Kind==CombatStance.Focused
                ||!TestOnlyClubAttackPolicy.CanSee(s,action.ActorId,action.TargetId))return false;
            var owner=s.Actors.Single(x=>x.Id==action.ActorId);var target=s.Actors.Single(x=>x.Id==action.TargetId);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(owner.X,owner.Y),new CombatCell(target.X,target.Y))>action.TriggerDistanceFeet
                ||s.MeleeAttacks.Length>=128||!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,action.TargetId))return false;
            var probe=s.Copy();
            attackFailure=TestOnlyClubAttackPolicy.ResolveReadyAttack(probe,"ready-probe",action.ActorId,action.TargetId,
                action.WeaponId,action.Knockout);
            return attackFailure==null;
        }

        private string ResolveReadyDeclaration(Snapshot s,Command c)
        {
            string failure=AssessReadyDeclaration(s,c);if(failure!=null)return failure;
            string actionId=ReadyIdentity("action|"+c.Id);
            var current= s.ReadyActions.SingleOrDefault(x=>x.ActorId==c.Actor&&x.Armed);
            if(current!=null)s.ReadyActions=s.ReadyActions.Select(x=>x.Id==current.Id
                ?x.Resolve(ReadyActionStatus.Replaced,s.Revision+1,actionId):x).ToArray();
            int expires=checked(s.Encounter.TurnOrdinal+s.Encounter.Order.Count);
            var action=new ReadyActionRecord(actionId,c.Id,c.Actor,c.Target,c.Combat.WeaponId,5,c.Combat.Knockout,
                s.Encounter.TurnOrdinal,expires,s.WorldSchedule.Start(expires),s.Revision+1);
            s.ReadyActions=s.ReadyActions.Concat(new[]{action}).ToArray();
            SetInterval(s,Interval(s,c.Actor).PayAction());PauseIncompatibleWork(s);return null;
        }

        private string QueueCompletedReadyOccurrences(Snapshot s)
        {
            if(!readyActionEnabled||s.SchemaVersion<Snapshot.ReadyActionSchema)return null;
            var completed=s.TacticalMoves.Where(x=>x.Status==TacticalMoveStatus.Completed&&x.ResolvedRevision==s.Revision+1)
                .OrderBy(x=>x.ResolvedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            foreach(var move in completed) {
                foreach(var action in s.ReadyActions.Where(x=>x.Armed&&x.TargetId==move.ActorId)
                    .OrderBy(x=>x.PreparedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    var owner=s.Actors.Single(x=>x.Id==action.ActorId);
                    long before=PlanarCombatGeometry.DistanceFeet(new CombatCell(move.FromX,move.FromY),new CombatCell(owner.X,owner.Y));
                    long after=PlanarCombatGeometry.DistanceFeet(new CombatCell(move.ToX,move.ToY),new CombatCell(owner.X,owner.Y));
                    if(before<=action.TriggerDistanceFeet||after>action.TriggerDistanceFeet
                        ||!TestOnlyClubAttackPolicy.CanSee(s,action.ActorId,action.TargetId))continue;
                    if(s.ReadyOccurrences.Length>=ReadyActionValidation.MaxOccurrences)return "ReadyActionHistoryCapacityReached";
                    string id=ReadyIdentity("occurrence|"+action.Id+"|"+move.Id);
                    if(s.ReadyOccurrences.Any(x=>x.Id==id))continue;
                    s.ReadyOccurrences=s.ReadyOccurrences.Concat(new[]{new ReadyOccurrenceRecord(id,action.Id,move.Id,
                        action.ActorId,move.ActorId,owner.X,owner.Y,s.Revision+1,action.PreparedRevision)}).ToArray();
                }
            }
            return null;
        }

        private void NormalizePendingReadyOccurrences(Snapshot s)
        {
            while(NextPostStepChoice(s)==PostStepChoiceKind.Ready) {
                var occurrence=PendingReadyOccurrence(s);
                if(occurrence==null||TryReadyAttack(s,occurrence,out _))return;
                s.ReadyOccurrences=s.ReadyOccurrences.Select(x=>x.Id==occurrence.Id
                    ?x.Resolve(ReadyOccurrenceStatus.Invalidated,s.Revision+1):x).ToArray();
            }
        }

        private string AssessReadyResponse(Snapshot s,Command c,out ReadyOccurrenceRecord occurrence,out ReadyActionRecord action)
        {
            occurrence=null;action=null;
            if(!readyActionEnabled||s.SchemaVersion!=Snapshot.ReadyActionSchema)return "ReadyActionNotEnabled";
            if(c.Inventory!=null||c.Combat==null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null||c.HarvestSelection!=null
                ||c.MiningSelection!=null||c.ProspectingExposure!=null||c.X!=0||c.Y!=0||c.Combat.Stance!=0
                ||c.Combat.WeaponId!=""||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||c.Combat.PressInstruction!=PressHitInstruction.KeepExisting)return "InvalidReadyResponse";
            if(!s.InventoryCombat||s.Encounter==null)return "ReadyActionRequiresTacticalCombat";
            occurrence=s.ReadyOccurrences.SingleOrDefault(x=>x.Id==c.Target&&x.Pending);
            string readyActionId=occurrence?.ReadyActionId;
            action=readyActionId==null?null:s.ReadyActions.SingleOrDefault(x=>x.Id==readyActionId&&x.Armed);
            if(occurrence==null||action==null)return "NoPendingReadyChoice";
            if(NextPostStepChoice(s)!=PostStepChoiceKind.Ready)return "EarlierPostStepChoicePending";
            if(c.Actor!=action.ActorId||c.Combat.TurnId!=s.Encounter.CurrentTurnId)return "WrongReactionController";
            if(c.Combat.Choice&&!TryReadyAttack(s,occurrence,out _))return "ReadyResponseNoLongerLegal";
            return null;
        }

        private string ResolveReadyResponse(Snapshot s,Command c)
        {
            string failure=AssessReadyResponse(s,c,out var occurrence,out var action);if(failure!=null)return failure;
            if(!TryReadyAttack(s,occurrence,out _)) {
                s.ReadyOccurrences=s.ReadyOccurrences.Select(x=>x.Id==occurrence.Id
                    ?x.Resolve(ReadyOccurrenceStatus.Invalidated,s.Revision+1):x).ToArray();return null;
            }
            if(!c.Combat.Choice) {
                s.ReadyOccurrences=s.ReadyOccurrences.Select(x=>x.Id==occurrence.Id
                    ?x.Resolve(ReadyOccurrenceStatus.Declined,s.Revision+1,c.Id):x).ToArray();return null;
            }
            var tactical=s.TacticalActors.Single(x=>x.ActorId==action.ActorId);
            s.TacticalActors=s.TacticalActors.Select(x=>x.ActorId==action.ActorId
                ?new ActorTacticalRecord(x.ActorId,x.LastRegularStart,false,x.MobileFeet,x.PressConsumed,x.DisengageTurn):x).ToArray();
            SetInterval(s,Interval(s,action.ActorId).WithReaction(false));
            string attackId="attack."+checked(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            s.ReadyOccurrences=s.ReadyOccurrences.Select(x=>x.Id==occurrence.Id
                ?x.Resolve(ReadyOccurrenceStatus.Accepted,s.Revision+1,c.Id,attackId):x).ToArray();
            s.ReadyActions=s.ReadyActions.Select(x=>x.Id==action.Id
                ?x.Resolve(ReadyActionStatus.Released,s.Revision+1,occurrence.Id):x).ToArray();
            string attackFailure=TestOnlyClubAttackPolicy.ResolveReadyAttack(s,c.Id,action.ActorId,action.TargetId,action.WeaponId,action.Knockout);
            return attackFailure;
        }

        private void ExpireReadyActionsAtStart(Snapshot s,Command initiating)
        {
            if(!readyActionEnabled||s.WorldSchedule==null||initiating==null)return;
            var due=s.ReadyActions.Where(x=>x.Armed&&x.ExpiresAt<=s.RuleClock
                &&x.ExpiresAfterTurnOrdinal<=s.WorldSchedule.ProcessedSlot)
                .OrderBy(x=>x.ExpiresAt).ThenBy(x=>x.PreparedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            foreach(var action in due) {
                s.ReadyOccurrences=s.ReadyOccurrences.Select(x=>x.ReadyActionId==action.Id&&x.Pending
                    ?x.Resolve(ReadyOccurrenceStatus.Invalidated,s.Revision+1):x).ToArray();
                s.ReadyActions=s.ReadyActions.Select(x=>x.Id==action.Id
                    ?x.Resolve(ReadyActionStatus.Expired,s.Revision+1,initiating.Id):x).ToArray();
            }
        }
    }
}
#endif
