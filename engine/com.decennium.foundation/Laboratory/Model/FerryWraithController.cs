#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public enum FerryDecisionSlot { Waiting, RegularTurn, Opportunity, Sanctuary, Press }
    public enum FerryIntentKind { Wait, Guard, Attack, Step, End, AcceptOpportunity, DeclineOpportunity, Retarget, Forgo, DeclinePress }
    public readonly struct FerryIntent
    {
        public FerryIntentKind Kind { get; }
        public string TargetId { get; }
        public CombatCell Destination { get; }
        internal FerryIntent(FerryIntentKind kind,string targetId="",CombatCell destination=default)
        { Kind=kind;TargetId=targetId;Destination=destination; }
    }
    /// <summary>Own source/allowances, directly seen opponents, and known terrain only.</summary>
    public sealed class FerryDecisionView
    {
        public FerryDecisionSlot Slot { get; }
        public CombatCell OwnCell { get; }
        public string FeatureId => Slot==FerryDecisionSlot.Waiting?"":FerryWraithProfile.Feature;
        public bool SourceAvailable { get; }
        public bool CanGuard { get; }
        public bool StanceSelected { get; }
        public bool CanAttack { get; }
        public bool CanMove { get; }
        public bool OpportunityEligible { get; }
        public string ProvokerId { get; }
        public IReadOnlyList<DefenderVisibleOpponent> VisibleOpponents { get; }
        public IReadOnlyList<CombatCell> ApproachCells { get; }
        internal FerryDecisionView(FerryDecisionSlot slot=FerryDecisionSlot.Waiting,CombatCell ownCell=default,
            bool sourceAvailable=false,bool canGuard=false,bool stanceSelected=false,bool canAttack=false,bool canMove=false,
            bool opportunityEligible=false,string provokerId="",IEnumerable<DefenderVisibleOpponent> visibleOpponents=null,
            IEnumerable<CombatCell> approachCells=null)
        {
            Slot=slot;OwnCell=ownCell;SourceAvailable=sourceAvailable;CanGuard=canGuard;StanceSelected=stanceSelected;
            CanAttack=canAttack;CanMove=canMove;OpportunityEligible=opportunityEligible;ProvokerId=provokerId;
            VisibleOpponents=Array.AsReadOnly((visibleOpponents??Array.Empty<DefenderVisibleOpponent>()).ToArray());
            ApproachCells=Array.AsReadOnly((approachCells??Array.Empty<CombatCell>()).ToArray());
        }
    }
    public static class FerryDecisionPolicy
    {
        public static FerryIntent Select(FerryDecisionView view)
        {
            if(view==null)throw new ArgumentNullException(nameof(view));
            if(view.Slot==FerryDecisionSlot.Waiting)return new FerryIntent(FerryIntentKind.Wait);
            if(view.Slot==FerryDecisionSlot.Press)return new FerryIntent(FerryIntentKind.DeclinePress);
            var ranked=view.VisibleOpponents.OrderBy(x=>PlanarCombatGeometry.DistanceFeet(view.OwnCell,x.Cell))
                .ThenBy(x=>x.ActorId,StringComparer.Ordinal).ToArray();
            bool InReach(DefenderVisibleOpponent x)=>x.DirectAttackAllowed&&x.ClearLineOfEffect
                &&PlanarCombatGeometry.DistanceFeet(view.OwnCell,x.Cell)<=5;
            if(view.Slot==FerryDecisionSlot.Opportunity)
                return new FerryIntent(view.SourceAvailable&&view.OpportunityEligible&&ranked.Any(x=>x.ActorId==view.ProvokerId&&InReach(x))
                    ?FerryIntentKind.AcceptOpportunity:FerryIntentKind.DeclineOpportunity);
            if(view.Slot==FerryDecisionSlot.Sanctuary) {
                var target=view.SourceAvailable?ranked.FirstOrDefault(InReach):null;
                return target==null?new FerryIntent(FerryIntentKind.Forgo):new FerryIntent(FerryIntentKind.Retarget,target.ActorId);
            }
            if(!view.StanceSelected&&view.CanGuard)return new FerryIntent(FerryIntentKind.Guard);
            if(!view.SourceAvailable||!view.CanAttack)return new FerryIntent(FerryIntentKind.End);
            var attack=ranked.FirstOrDefault(InReach);
            if(attack!=null)return new FerryIntent(FerryIntentKind.Attack,attack.ActorId);
            if(view.CanMove&&ranked.Length>0) {
                var target=ranked[0];long distance=PlanarCombatGeometry.DistanceFeet(view.OwnCell,target.Cell);
                var steps=view.ApproachCells.Select(x=>(Cell:x,Distance:PlanarCombatGeometry.DistanceFeet(x,target.Cell)))
                    .Where(x=>x.Distance<distance).OrderBy(x=>x.Distance).ThenBy(x=>x.Cell.X).ThenBy(x=>x.Cell.Y).Take(1).ToArray();
                if(steps.Length!=0)return new FerryIntent(FerryIntentKind.Step,destination:steps[0].Cell);
            }
            return new FerryIntent(FerryIntentKind.End);
        }
    }
    public sealed class FerryDecision
    {
        internal FerryWraithController Owner { get; }
        internal Command Fallback { get; }
        public FerryDecisionView View { get; }
        public FerryIntent Intent { get; }
        public Command Primary { get; }
        internal FerryDecision(FerryWraithController owner,FerryDecisionView view,FerryIntent intent,Command primary,Command fallback)
        { Owner=owner;View=view;Intent=intent;Primary=primary;Fallback=fallback; }
    }
    public sealed class FerryWraithController
    {
        public const string Principal="TEST_ONLY.ferry-controller";
        private readonly Simulation simulation;
        private readonly TestOnlySharedWorldPolicy policy;
        private readonly object gate=new object();
        public FerryWraithController(Simulation simulation,TestOnlySharedWorldPolicy policy)
        { this.simulation=simulation??throw new ArgumentNullException(nameof(simulation));this.policy=policy??throw new ArgumentNullException(nameof(policy)); }
        public static Authority CreatureAuthority()=>new Authority(Principal,new[]{FerryWraithProfile.Actor},inventoryOwners:new[]{FerryWraithProfile.Actor});
        internal static bool HasGrant(Authority grant)=>grant?.Principal==Principal&&grant.Controls(FerryWraithProfile.Actor)
            &&grant.MayUseInventory(FerryWraithProfile.Actor);
        public FerryDecision Plan(Authority grant)
        {
            var state=simulation.Capture();var view=policy.ObserveFerryController(state,grant);var intent=FerryDecisionPolicy.Select(view);
            var primary=Materialize(state,intent);Command fallback=null;
            if(intent.Kind==FerryIntentKind.Attack||intent.Kind==FerryIntentKind.Step)fallback=Materialize(state,new FerryIntent(FerryIntentKind.End));
            if(intent.Kind==FerryIntentKind.AcceptOpportunity)fallback=Materialize(state,new FerryIntent(FerryIntentKind.DeclineOpportunity));
            if(intent.Kind==FerryIntentKind.Retarget)fallback=Materialize(state,new FerryIntent(FerryIntentKind.Forgo));
            return new FerryDecision(this,view,intent,primary,fallback);
        }
        public DefenderDispatchStatus Dispatch(Authority grant,FerryDecision decision)
        {
            if(!HasGrant(grant)||decision?.Owner!=this)return DefenderDispatchStatus.Rejected;
            if(decision.Primary==null)return DefenderDispatchStatus.Waiting;
            lock(gate) {
                var first=simulation.AssessCommandAdmission(grant,decision.Primary);
                if(first.Status==CommandAdmissionStatus.Admitted||first.Status==CommandAdmissionStatus.AlreadyCommitted)return Execute(grant,decision.Primary);
                if(decision.Fallback!=null&&(first.Code=="StaleRevision"||first.Status==CommandAdmissionStatus.RuleDenied&&MayFallback(first.Code))) {
                    var second=simulation.AssessCommandAdmission(grant,decision.Fallback);
                    if(second.Status==CommandAdmissionStatus.AlreadyCommitted||first.Status==CommandAdmissionStatus.RuleDenied&&second.Status==CommandAdmissionStatus.Admitted)
                        return Execute(grant,decision.Fallback);
                }
                return first.Code=="StaleRevision"?DefenderDispatchStatus.Stale:DefenderDispatchStatus.Rejected;
            }
        }
        private DefenderDispatchStatus Execute(Authority grant,Command command)
        {
            var result=simulation.Execute(grant,command);
            return result.Outcome==Outcome.Committed?DefenderDispatchStatus.Committed:result.Outcome==Outcome.Duplicate
                ?DefenderDispatchStatus.Duplicate:result.Code=="StaleRevision"?DefenderDispatchStatus.Stale:DefenderDispatchStatus.Rejected;
        }
        private static bool MayFallback(string code)=>code=="BlockedTacticalStep"||code=="OccupiedTacticalStep"||code=="InsufficientMovement"
            ||code=="ZeroSpeedCannotMove"||code=="MoverCannotAct"||code=="ConditionPreventsMovement"||code=="HuntingTrapTetherPreventsMovement"
            ||code=="InvalidLivingTarget"||code=="TargetOutsideEncounter"||code=="TargetLocationUnknown"||code=="BlockedLineOfEffect"
            ||code=="TargetOutOfReach"||code=="CreatureAttackSourceSuppressed"||code=="SanctuaryTargetProhibitedThisInterval";
        private static Command Materialize(Snapshot state,FerryIntent intent)
        {
            if(intent.Kind==FerryIntentKind.Wait)return null;
            string turn=state.Encounter.CurrentTurnId,target=turn;CombatRequest combat=null;SanctuaryResponseRequest response=null;
            var cell=intent.Destination;CommandKind kind;
            switch(intent.Kind) {
                case FerryIntentKind.Guard:kind=CommandKind.SelectCombatStance;target="";combat=new CombatRequest(turn,stance:(int)CombatStance.Guarded);break;
                case FerryIntentKind.Attack:kind=CommandKind.AttackCreatureFeature;target=intent.TargetId;
                    combat=new CombatRequest(turn,pressInstruction:PressHitInstruction.KeepExisting,featureId:FerryWraithProfile.Feature);break;
                case FerryIntentKind.Step:kind=CommandKind.TacticalStep;break;
                case FerryIntentKind.End:kind=CommandKind.EndRegularTurn;break;
                case FerryIntentKind.DeclinePress:kind=CommandKind.RespondPress;target=TestOnlyClubAttackPolicy.CurrentPressOffer(state).Id;combat=new CombatRequest(turn);break;
                case FerryIntentKind.Retarget:case FerryIntentKind.Forgo:
                    kind=CommandKind.RespondSanctuary;target=TestOnlySharedWorldPolicy.PendingSanctuary(state).Id;
                    response=new SanctuaryResponseRequest(intent.Kind==FerryIntentKind.Retarget?SanctuaryResponseKind.Retarget:SanctuaryResponseKind.Forgo,intent.TargetId);break;
                default:kind=CommandKind.RespondOpportunityAttack;target=TestOnlyClubAttackPolicy.PendingMove(state).Id;
                    combat=intent.Kind==FerryIntentKind.AcceptOpportunity?new CombatRequest(turn,choice:true,
                        pressInstruction:PressHitInstruction.KeepExisting,featureId:FerryWraithProfile.Feature):new CombatRequest(turn);break;
            }
            string key=FormattableString.Invariant($"{Principal}|{state.Encounter.Id}|{turn}|{state.Revision}|{intent.Kind}|{target}|{cell.X}|{cell.Y}|{intent.TargetId}");
            using(var sha=SHA256.Create())return new Command("ferry."+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture))),
                FerryWraithProfile.Actor,state.Revision,kind,target,cell.X,cell.Y,combat:combat,sanctuaryResponse:response);
        }
    }
}
#endif
