#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlyClubAttackPolicy
    {
        private static ActorTacticalRecord TacticalActor(Snapshot s,string actor)=>s.TacticalActors.Single(x=>x.ActorId==actor);
        private static void SetTactical(Snapshot s,ActorTacticalRecord record) {
            s.TacticalActors=s.TacticalActors.Select(x=>x.ActorId==record.ActorId?record:x).ToArray();
            if(s.WorldSchedule!=null)s.WorldIntervals=s.WorldIntervals.Select(x=>x.ActorId==record.ActorId?x.WithReaction(record.ReactionAvailable):x).ToArray();
        }
        private static void StartTactical(Snapshot s)
        {
            var e=s.Encounter;var before=TacticalActor(s,e.CurrentActor);
            var reaction=new ReactionClock(before.ReactionAvailable,lastRegularStart:before.LastRegularStart).RegularStart(e.TurnOrdinal);
            SetTactical(s,new ActorTacticalRecord(e.CurrentActor,e.TurnOrdinal,reaction.Available));
        }
        public static TacticalMoveRecord PendingMove(Snapshot s)=>s.TacticalMoves.SingleOrDefault(m=>m.Pending);
        public static PressOfferRecord CurrentPressOffer(Snapshot s)=>s.PressOffers.Where(p=>p.Status==PressOfferStatus.Pending)
            .OrderByDescending(p=>p.CreatedRevision).ThenBy(p=>p.ArmedRevision).ThenBy(p=>p.Id,StringComparer.Ordinal).FirstOrDefault();
        private static void SetMove(Snapshot s,TacticalMoveRecord move)=>s.TacticalMoves=s.TacticalMoves.Select(m=>m.Id==move.Id?move:m).ToArray();
        private static void SetOffer(Snapshot s,PressOfferRecord offer)=>s.PressOffers=s.PressOffers.Select(p=>p.Id==offer.Id?offer:p).ToArray();
        private static bool Adjacent(int ax,int ay,int bx,int by)=>WorldSpatialQueries.DistanceInCells(ax,ay,bx,by)==1;
        private long StepCost(Snapshot s,string actor,int x,int y)=>PlaytestCombatBudgets.MovementCost(5,tactical.At(x,y),EffectiveProne(s,actor));
        internal bool DefensiveFormationCanMove(Snapshot s,string actor)
            =>ActorLifeRules.CanAct(s,actor)&&WalkingSpeed(s,actor)>0
                &&(!WithConditions(s)||Aware(s,actor)&&CurrentPermissions(s,actor).VoluntarySpeed);
        private string StepFailure(Snapshot s,string actor,int fromX,int fromY,int x,int y,TacticalMoveKind kind,string commandStepOffer="",string defensiveFormationId="")
        {
            if(!ActorLifeRules.CanAct(s,actor))return "MoverCannotAct";
            if(WithConditions(s)&&(!Aware(s,actor)||!CurrentPermissions(s,actor).VoluntarySpeed))return "ConditionPreventsMovement";
            var body=s.Actors.Single(a=>a.Id==actor);
            if(body.X!=fromX||body.Y!=fromY)return "MovementOriginChanged";
            if(HuntingTrapValidation.BlocksGridMove(s,actor,x,y))return "HuntingTrapTetherPreventsMovement";
            var spatial=WorldSpatialQueries.Step(s,actor,fromX,fromY,x,y,true,true,
                (px,py)=>TestOnlyPolicy.Walkable(px,py)&&(!ObservationRules.Enabled(s)||ObservationGeometry.SupportsAnchorAt(s,px,py)));
            if(spatial==SpatialStepFailure.NotNeighbor)return "InvalidTacticalStep";
            if(spatial==SpatialStepFailure.Blocked)return "BlockedTacticalStep";
            if(spatial==SpatialStepFailure.Occupied)return "OccupiedTacticalStep";
            long speed=WalkingSpeed(s,actor);if(speed==0)return "ZeroSpeedCannotMove";
            long cost=StepCost(s,actor,x,y);
            if(kind==TacticalMoveKind.Press)return cost>PlaytestCombatBudgets.SpecialBudget(SpecialMovement.Press,speed)?"InsufficientPressMovement":null;
            if(kind==TacticalMoveKind.CommandStep) {
                var offer=s.CommandStepOffers.SingleOrDefault(x=>x.Id==commandStepOffer
                    &&(x.Status==CommandStepOfferStatus.Accepted||x.Status==CommandStepOfferStatus.Pending)&&x.AllyActorId==actor);
                if(offer==null)return "CommandStepOfferUnavailable";
                return cost>5?"InsufficientCommandStepMovement":null;
            }
            if(kind==TacticalMoveKind.DefensiveFormationShift) {
                var activation=s.DefensiveFormations.SingleOrDefault(f=>f.Id==defensiveFormationId&&f.Active);
                if(activation==null||!activation.Shifts.Any(x=>x.RecipientActorId==actor
                    &&(x.Status==DefensiveFormationShiftStatus.AwaitingResponse||x.Status==DefensiveFormationShiftStatus.Moving)))
                    return "DefensiveFormationShiftUnavailable";
                return cost>5?"InsufficientDefensiveFormationMovement":null;
            }
            if(s.Encounter.CurrentActor!=actor)return "WrongRegularTurn";
            if(kind==TacticalMoveKind.TacticalReposition)return cost>CharacterAdvancementRules.RepositionBudget(s,actor,s.Encounter.TurnOrdinal)?"InsufficientRepositionMovement":null;
            return new RuleQuantity(cost)>RemainingMovement(s,actor)?"InsufficientMovement":null;
        }
        private static bool EligibleOpportunity(Snapshot s,string reactor,TacticalMoveRecord move)
        {
            if(move.Kind==TacticalMoveKind.TacticalReposition||move.Kind==TacticalMoveKind.CommandStep
                ||move.Kind==TacticalMoveKind.DefensiveFormationShift)return false;
            if(reactor==move.ActorId||SoldierTacticalFeatures.IsAlly(s,reactor,move.ActorId)
                ||!ActorLifeRules.CanAct(s,reactor)||!TacticalActor(s,reactor).ReactionAvailable
                ||ActiveStance(s,reactor)?.Kind==CombatStance.Focused)return false;
            if(WithConditions(s)&&(!CurrentPermissions(s,reactor).Reaction||PhysicalAttackFailure(s,reactor)!=null||!CanSee(s,reactor,move.ActorId)))return false;
            var moving=TacticalActor(s,move.ActorId);
            if(moving.DisengageTurn==s.Encounter.TurnOrdinal||ActiveStance(s,move.ActorId)?.Kind==CombatStance.Mobile&&moving.MobileFeet<5)return false;
            var body=s.Actors.Single(a=>a.Id==reactor);
            // This admitted fixture supplies hostility and sight for legal adjacent melee attacks.
            // Every reactor has a usable ordinary unarmed attack, even after dropping a Club.
            return Adjacent(body.X,body.Y,move.FromX,move.FromY)&&!Adjacent(body.X,body.Y,move.ToX,move.ToY);
        }
        private string BeginOrdinaryStep(Snapshot s,Command c)
        {
            var body=s.Actors.Single(a=>a.Id==c.Actor);string error=StepFailure(s,c.Actor,body.X,body.Y,c.X,c.Y,TacticalMoveKind.Ordinary);if(error!=null)return error;
            error=OrdinaryStepCapacityFailure(s);if(error!=null)return error;
            BeginStep(s,c.Actor,c.X,c.Y,TacticalMoveKind.Ordinary);AdvanceTacticalFlow(s);return null;
        }
        private string OrdinaryStepCapacityFailure(Snapshot s)
        {
            // Reserve room for the entire bounded chain before any reaction can be paid. Every
            // accepted follow consumes one interval entitlement, with no clock/start inside it.
            if(s.Actors.Any(a=>!DamageConditionCapacity(s,a.Id)))return "ConditionContinuationCapacityReached";
            int n=s.Actors.Length,steps=n+1,offers=steps*(n-1),commands=1+3*offers;
            if(s.TacticalMoves.Length+steps>64||s.PressOffers.Length+offers>128||s.MeleeAttacks.Length+offers>128||s.Receipts.Length+commands>512)return "ContinuationCapacityReached";
            return null;
        }
        private string BeginTacticalRepositionStep(Snapshot s,Command c)
        {
            var body=s.Actors.Single(a=>a.Id==c.Actor);string error=StepFailure(s,c.Actor,body.X,body.Y,c.X,c.Y,TacticalMoveKind.TacticalReposition);if(error!=null)return error;
            error=TacticalRepositionCapacityFailure(s,c.Actor);if(error!=null)return error;
            BeginStep(s,c.Actor,c.X,c.Y,TacticalMoveKind.TacticalReposition);AdvanceTacticalFlow(s);return null;
        }
        private string TacticalRepositionCapacityFailure(Snapshot s,string actor)
        {
            int pendingPress=s.Presses.Count(x=>x.TargetId==actor&&s.RuleClock<x.ExpiresAt);
            if(s.TacticalMoves.Length>=64||s.PressOffers.Length+pendingPress>128||s.MeleeAttacks.Length+pendingPress>128
                ||s.Receipts.Length+pendingPress*3+1>512)return "ContinuationCapacityReached";
            return null;
        }
        internal string AssessTacticalMovementCommand(Snapshot s,Command c,out long movementCost)
        {
            movementCost=0;
            if(tactical==null)return "TacticalMovementNotSelected";
            if(s==null||c==null||c.Inventory!=null||c.Combat!=null||c.Target==""||c.Kind!=CommandKind.TacticalStep&&c.Kind!=CommandKind.TacticalRepositionStep)
                return "InvalidTacticalStep";
            if(s.MeleeAttacks.Any(x=>x.Pending))return "KnockoutChoicePending";
            if(PendingMove(s)!=null||CurrentPressOffer(s)!=null)return "TacticalMovementChoicePending";
            var encounter=s.Encounter;
            if(encounter==null||c.Actor!=encounter.CurrentActor||c.Target!=encounter.CurrentTurnId)return "WrongRegularTurn";
            if(c.Kind==CommandKind.TacticalStep&&!HasStance(s))return "StanceRequired";
            var body=s.Actors.Single(x=>x.Id==c.Actor);
            var kind=c.Kind==CommandKind.TacticalStep?TacticalMoveKind.Ordinary:TacticalMoveKind.TacticalReposition;
            string error=StepFailure(s,c.Actor,body.X,body.Y,c.X,c.Y,kind);
            if(error!=null)return error;
            error=c.Kind==CommandKind.TacticalStep?OrdinaryStepCapacityFailure(s):TacticalRepositionCapacityFailure(s,c.Actor);
            if(error!=null)return error;
            movementCost=StepCost(s,c.Actor,c.X,c.Y);
            return null;
        }
        internal string BeginCommandStep(Snapshot s,CommandStepOfferRecord offer,int x,int y)
        {
            if(offer==null||offer.Status!=CommandStepOfferStatus.Accepted)return "CommandStepOfferUnavailable";
            var body=s.Actors.Single(a=>a.Id==offer.AllyActorId);
            string error=StepFailure(s,offer.AllyActorId,body.X,body.Y,x,y,TacticalMoveKind.CommandStep,offer.Id);if(error!=null)return error;
            int pressCount=s.Presses.Count(p=>p.TargetId==offer.AllyActorId&&s.RuleClock<p.ExpiresAt);
            int movementOverwatchCount=s.OverwatchDesignations.Count(z=>z.Status==OverwatchDesignationStatus.Active&&z.OwnerId!=offer.AllyActorId);
            if(s.TacticalMoves.Length+1+pressCount>64||s.PressOffers.Length+pressCount>128||s.MeleeAttacks.Length+pressCount>128
                ||s.Receipts.Length+pressCount*3+1>512||s.OverwatchOffers.Length+movementOverwatchCount>OverwatchExecutionValidation.MaxOffers)
                return "ContinuationCapacityReached";
            BeginStep(s,offer.AllyActorId,x,y,TacticalMoveKind.CommandStep,parentCommandStep:offer.Id);AdvanceTacticalFlow(s);return null;
        }
        internal string CommandStepDestinationFailure(Snapshot s,CommandStepOfferRecord offer,int fromX,int fromY,int x,int y)
        {
            if(offer==null||offer.Status!=CommandStepOfferStatus.Pending)return "CommandStepOfferUnavailable";
            return StepFailure(s,offer.AllyActorId,fromX,fromY,x,y,TacticalMoveKind.CommandStep,offer.Id);
        }
        internal string BeginDefensiveFormationShift(Snapshot s,string activationId,string actor,int x,int y)
        {
            var activation=s.DefensiveFormations.SingleOrDefault(f=>f.Id==activationId&&f.Active);
            var shift=activation?.Shifts.SingleOrDefault(x=>x.RecipientActorId==actor&&x.Status==DefensiveFormationShiftStatus.Moving);
            if(shift==null)return "DefensiveFormationShiftUnavailable";
            var body=s.Actors.Single(a=>a.Id==actor);
            string error=StepFailure(s,actor,body.X,body.Y,x,y,TacticalMoveKind.DefensiveFormationShift,
                defensiveFormationId:activationId);if(error!=null)return error;
            int pressCount=s.Presses.Count(p=>p.TargetId==actor&&s.RuleClock<p.ExpiresAt);
            int movementOverwatchCount=s.OverwatchDesignations.Count(z=>z.Status==OverwatchDesignationStatus.Active&&z.OwnerId!=actor);
            if(s.TacticalMoves.Length+1+pressCount>64||s.PressOffers.Length+pressCount>128||s.MeleeAttacks.Length+pressCount>128
                ||s.Receipts.Length+pressCount*3+1>512||s.OverwatchOffers.Length+movementOverwatchCount>OverwatchExecutionValidation.MaxOffers)
                return "ContinuationCapacityReached";
            BeginStep(s,actor,x,y,TacticalMoveKind.DefensiveFormationShift,parentDefensiveFormation:activationId);
            AdvanceTacticalFlow(s);return null;
        }
        internal string DefensiveFormationDestinationFailure(Snapshot s,string activationId,string actor,int fromX,int fromY,int x,int y)
        {
            return StepFailure(s,actor,fromX,fromY,x,y,TacticalMoveKind.DefensiveFormationShift,defensiveFormationId:activationId);
        }
        private static TacticalMoveRecord NewStep(Snapshot s,string actor,int x,int y,TacticalMoveKind kind,string parent="",string parentCommandStep="",string parentDefensiveFormation="")
        {
            var body=s.Actors.Single(a=>a.Id==actor);return new TacticalMoveRecord("move."+N(s.Revision+1),s.Revision+1,0,s.Encounter.TurnOrdinal,
                actor,body.X,body.Y,x,y,kind,TacticalMoveStatus.AwaitingReactions,Array.Empty<string>(),parentPressOffer:parent,
                parentCommandStepOffer:parentCommandStep,parentDefensiveFormationId:parentDefensiveFormation);
        }
        private static void BeginStep(Snapshot s,string actor,int x,int y,TacticalMoveKind kind,string parent="",string parentCommandStep="",string parentDefensiveFormation="")
        {
            var step=NewStep(s,actor,x,y,kind,parent,parentCommandStep,parentDefensiveFormation);
            var reactors=s.Encounter.Order.Where(id=>EligibleOpportunity(s,id,step)).ToArray();
            step=new TacticalMoveRecord(step.Id,step.Revision,0,step.TurnOrdinal,actor,step.FromX,step.FromY,x,y,kind,step.Status,reactors,
                parentPressOffer:parent,parentCommandStepOffer:parentCommandStep,parentDefensiveFormationId:parentDefensiveFormation);
            s.TacticalMoves=s.TacticalMoves.Concat(new[]{step}).ToArray();
        }
        private bool PressLegal(Snapshot s,PressOfferRecord offer)
        {
            var source=ActivePress(s,offer.ActorId);if(source==null||source.ArmedRevision!=offer.ArmedRevision||source.TargetId!=offer.TargetId||TacticalActor(s,offer.ActorId).PressConsumed)return false;
            var moved=s.TacticalMoves.Single(m=>m.Id==offer.MoveId);var holder=s.Actors.Single(a=>a.Id==offer.ActorId);
            return moved.Status==TacticalMoveStatus.Completed&&moved.ActorId==offer.TargetId
                &&Adjacent(holder.X,holder.Y,moved.FromX,moved.FromY)&&!Adjacent(holder.X,holder.Y,moved.ToX,moved.ToY)
                &&StepFailure(s,offer.ActorId,holder.X,holder.Y,moved.FromX,moved.FromY,TacticalMoveKind.Press)==null;
        }
        private void QueuePress(Snapshot s,TacticalMoveRecord move)
        {
            foreach(var press in s.Presses.Where(p=>p.TargetId==move.ActorId&&s.RuleClock<p.ExpiresAt).OrderBy(p=>p.ArmedRevision).ThenBy(p=>p.ActorId,StringComparer.Ordinal)) {
                var offer=new PressOfferRecord("press."+N(s.Revision+1)+"."+press.ActorId,move.Id,press.ActorId,move.ActorId,s.Revision+1,press.ArmedRevision);
                if(PressLegal(s,offer))s.PressOffers=s.PressOffers.Concat(new[]{offer}).ToArray();
            }
        }
        private void AdvanceTacticalFlow(Snapshot s)
        {
            while(!s.MeleeAttacks.Any(a=>a.Pending)) {
                if(s.SchemaVersion>=Snapshot.OverwatchExecutionSchema&&TestOnlySharedWorldPolicy.EarlierPostStepChoiceThanPress(s))return;
                var move=PendingMove(s);
                if(move!=null) {
                    if(StepFailure(s,move.ActorId,move.FromX,move.FromY,move.ToX,move.ToY,move.Kind,move.ParentCommandStepOffer,move.ParentDefensiveFormationId)!=null) {
                        SetMove(s,move.Progress(move.ResponseIndex,TacticalMoveStatus.Interrupted,s.Revision+1));continue;
                    }
                    int index=move.ResponseIndex;
                    while(index<move.Reactors.Count&&!EligibleOpportunity(s,move.Reactors[index],move))index++;
                    if(index!=move.ResponseIndex){move=move.Progress(index,move.Status);SetMove(s,move);}
                    if(index<move.Reactors.Count)return;
                    long cost=StepCost(s,move.ActorId,move.ToX,move.ToY);
                    if(move.Kind==TacticalMoveKind.Ordinary) {
                        SpendMovement(s,move.ActorId,cost);
                    }
                    else if(move.Kind==TacticalMoveKind.TacticalReposition)CharacterAdvancementRules.SpendReposition(s,move.ActorId,cost);
                    var actor=s.Actors.Single(a=>a.Id==move.ActorId);actor.X=move.ToX;actor.Y=move.ToY;
                    if(ObservationRules.Enabled(s))ObservationRules.Refresh(s,s.RuleClock,s.Revision+1);
                    if(cost>0)CharacterAdvancementRules.MarkMoved(s,move.ActorId);
                    s.Clubs=s.Clubs.Select(w=>w.HeldBy==actor.Id?new ClubInstance(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,w.HeldBy,actor.X,actor.Y):w).ToArray();
                    if(s.SchemaVersion>=Snapshot.OverwatchExecutionSchema)
                        s.RepeatingCrossbows=s.RepeatingCrossbows.Select(w=>w.HeldBy==actor.Id
                            ?new RepeatingCrossbowRecord(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,w.HeldBy,w.GripHands,actor.X,actor.Y,w.LoadedBoltLots.ToArray()):w).ToArray();
                    var resources=TacticalActor(s,actor.Id);
                    if(ActiveStance(s,actor.Id)?.Kind==CombatStance.Mobile)SetTactical(s,new ActorTacticalRecord(actor.Id,resources.LastRegularStart,resources.ReactionAvailable,5,resources.PressConsumed,resources.DisengageTurn));
                    move=move.Progress(index,TacticalMoveStatus.Completed,s.Revision+1,cost);SetMove(s,move);QueuePress(s,move);continue;
                }
                var offer=CurrentPressOffer(s);
                if(offer!=null) {
                    if(PressLegal(s,offer))return;
                    SetOffer(s,offer.Resolve(PressOfferStatus.Invalidated,s.Revision+1));continue;
                }
                var accepted=s.PressOffers.Where(x=>x.Status==PressOfferStatus.Accepted
                    &&!s.TacticalMoves.Any(m=>m.ParentPressOffer==x.Id)).OrderByDescending(x=>x.CreatedRevision)
                    .ThenBy(x=>x.ArmedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).FirstOrDefault();
                if(accepted!=null) {
                    var departed=s.TacticalMoves.Single(m=>m.Id==accepted.MoveId);
                    BeginStep(s,accepted.ActorId,departed.FromX,departed.FromY,TacticalMoveKind.Press,accepted.Id);continue;
                }
                return;
            }
        }
        internal void ContinueTacticalFlow(Snapshot s)=>AdvanceTacticalFlow(s);
        private string ResolveTacticalChoice(Snapshot s,Command c)
        {
            var move=PendingMove(s);var r=c.Combat;
            if(move!=null) {
                if(c.Kind!=CommandKind.RespondOpportunityAttack)return "OpportunityChoicePending";
                if(r==null||r.TurnId!=s.Encounter.CurrentTurnId||c.Target!=move.Id||c.X!=0||c.Y!=0||r.Stance!=0)return "InvalidOpportunityResponse";
                if(move.ResponseIndex>=move.Reactors.Count||c.Actor!=move.Reactors[move.ResponseIndex])return "WrongReactionController";
                if(!EligibleOpportunity(s,c.Actor,move))return "OpportunityNoLongerEligible";
                if(!r.Choice&&(r.WeaponId!=""||r.Knockout!=AttackKnockoutMode.OrdinaryOutcome||r.PressInstruction!=PressHitInstruction.ArmOrReplace))return "InvalidOpportunityResponse";
                SetMove(s,move.Progress(move.ResponseIndex+1,move.Status));
                if(r.Choice) {
                    var actor=TacticalActor(s,c.Actor);var reaction=new ReactionClock(actor.ReactionAvailable,lastRegularStart:actor.LastRegularStart).Spend();
                    SetTactical(s,new ActorTacticalRecord(actor.ActorId,actor.LastRegularStart,reaction.Available,actor.MobileFeet,actor.PressConsumed,actor.DisengageTurn));
                    bool unarmed=r.WeaponId==CombatProfileIds.OrdinaryUnarmed;
                    var attack=new Command(c.Id,c.Actor,c.ExpectedRevision,unarmed?CommandKind.AttackUnarmed:CommandKind.AttackClub,move.ActorId,
                        combat:new CombatRequest(r.TurnId,unarmed?"":r.WeaponId,knockout:r.Knockout,pressInstruction:r.PressInstruction));
                    string error=Attack(s,attack,true);if(error!=null)return error;
                }
                AdvanceTacticalFlow(s);return null;
            }
            var offer=CurrentPressOffer(s);
            if(c.Kind!=CommandKind.RespondPress)return "PressChoicePending";
            if(offer==null||r==null||c.Actor!=offer.ActorId||c.Target!=offer.Id||r.TurnId!=s.Encounter.CurrentTurnId||r.WeaponId!=""||r.Stance!=0
                ||r.Knockout!=AttackKnockoutMode.OrdinaryOutcome||r.PressInstruction!=PressHitInstruction.ArmOrReplace||c.X!=0||c.Y!=0)return "InvalidPressResponse";
            if(!PressLegal(s,offer))return "PressNoLongerEligible";
            SetOffer(s,offer.Resolve(r.Choice?PressOfferStatus.Accepted:PressOfferStatus.Declined,s.Revision+1));
            if(r.Choice) {
                var actor=TacticalActor(s,c.Actor);SetTactical(s,new ActorTacticalRecord(actor.ActorId,actor.LastRegularStart,actor.ReactionAvailable,actor.MobileFeet,true,actor.DisengageTurn));
                if(s.SchemaVersion<Snapshot.OverwatchExecutionSchema||TestOnlySharedWorldPolicy.NextPostStepAllowsPressFollow(s)) {
                    var departed=s.TacticalMoves.Single(m=>m.Id==offer.MoveId);BeginStep(s,c.Actor,departed.FromX,departed.FromY,TacticalMoveKind.Press,offer.Id);
                }
            }
            AdvanceTacticalFlow(s);return null;
        }
    }
}
#endif
