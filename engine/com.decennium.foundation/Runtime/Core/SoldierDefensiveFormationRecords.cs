using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum DefensiveFormationStatus { Active, Expired }
    public enum DefensiveFormationShiftStatus { Queued, AwaitingResponse, Moving, Declined, Skipped, Moved }

    /// <summary>Persisted disposition of one recipient's optional shift.</summary>
    public sealed class DefensiveFormationShiftRecord
    {
        public string Id { get; }
        public int OrderIndex { get; }
        public string RecipientActorId { get; }
        public DefensiveFormationShiftStatus Status { get; }
        public long UpdatedRevision { get; }
        public long DecisionRevision { get; }
        public string DecisionId { get; }
        public string MoveId { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }

        public DefensiveFormationShiftRecord(string id,int orderIndex,string recipientActorId,DefensiveFormationShiftStatus status,
            long updatedRevision,long decisionRevision=0,string decisionId="",string moveId="",long resolvedRevision=0,string resolutionId="")
        {
            bool noDecision=status==DefensiveFormationShiftStatus.Queued||status==DefensiveFormationShiftStatus.AwaitingResponse;
            bool skipped=status==DefensiveFormationShiftStatus.Skipped;
            bool invalidDecision= noDecision&&(decisionRevision!=0||decisionId!=""||moveId!=""||resolvedRevision!=0||resolutionId!="")
                ||status==DefensiveFormationShiftStatus.Moving&&(decisionRevision<1||!Validation.ValidId(decisionId)||!Validation.ValidId(moveId)
                    ||resolvedRevision!=0||resolutionId!="")
                ||status==DefensiveFormationShiftStatus.Declined&&(decisionRevision<1||!Validation.ValidId(decisionId)||moveId!=""
                    ||resolvedRevision!=decisionRevision||resolutionId!=decisionId)
                ||skipped&&(decisionRevision==0
                    ?decisionId!=""||moveId!=""||resolvedRevision<updatedRevision||!Validation.ValidId(resolutionId)
                    :!Validation.ValidId(decisionId)||resolvedRevision<decisionRevision||!Validation.ValidId(resolutionId)
                        ||(moveId!=""&&!Validation.ValidId(moveId)))
                ||status==DefensiveFormationShiftStatus.Moved&&(decisionRevision<1||!Validation.ValidId(decisionId)||!Validation.ValidId(moveId)
                    ||resolvedRevision<decisionRevision||!Validation.ValidId(resolutionId));
            if(!Validation.ValidId(id)||orderIndex<0||!Validation.ValidId(recipientActorId)||!Enum.IsDefined(typeof(DefensiveFormationShiftStatus),status)
                ||updatedRevision<1||decisionRevision<0||resolvedRevision<0||updatedRevision<decisionRevision||updatedRevision<resolvedRevision||invalidDecision)
                throw new ArgumentException("Invalid Defensive Formation shift disposition.");
            Id=id;OrderIndex=orderIndex;RecipientActorId=recipientActorId;Status=status;UpdatedRevision=updatedRevision;
            DecisionRevision=decisionRevision;DecisionId=decisionId;MoveId=moveId;ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }

        public DefensiveFormationShiftRecord Await(long revision)
        {
            if(Status!=DefensiveFormationShiftStatus.Queued)throw new InvalidOperationException("Only a queued shift can be offered.");
            return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.AwaitingResponse,
                revision);
        }
        public DefensiveFormationShiftRecord Decline(long revision,string commandId)
        {
            if(Status!=DefensiveFormationShiftStatus.AwaitingResponse)throw new InvalidOperationException("Defensive Formation shift is not awaiting a response.");
            return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.Declined,
                revision,revision,commandId,"",revision,commandId);
        }
        public DefensiveFormationShiftRecord Skip(long revision,string commandId)
        {
            if(Status==DefensiveFormationShiftStatus.Queued||Status==DefensiveFormationShiftStatus.AwaitingResponse)
                return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.Skipped,
                    revision,resolvedRevision:revision,resolutionId:commandId);
            if(Status==DefensiveFormationShiftStatus.Moving)
                return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.Skipped,
                    revision,DecisionRevision,DecisionId,MoveId,revision,commandId);
            throw new InvalidOperationException("Defensive Formation shift is already resolved.");
        }
        public DefensiveFormationShiftRecord BeginMove(long revision,string commandId,string moveId)
        {
            if(Status!=DefensiveFormationShiftStatus.AwaitingResponse)throw new InvalidOperationException("No Defensive Formation shift is awaiting movement.");
            return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.Moving,revision,revision,commandId,moveId);
        }
        public DefensiveFormationShiftRecord CompleteMove(long revision,string commandId)
        {
            if(Status!=DefensiveFormationShiftStatus.Moving)throw new InvalidOperationException("Defensive Formation movement is not pending.");
            return new DefensiveFormationShiftRecord(Id,OrderIndex,RecipientActorId,DefensiveFormationShiftStatus.Moved,revision,
                DecisionRevision,DecisionId,MoveId,revision,commandId);
        }
        public bool SameAs(DefensiveFormationShiftRecord x)=>x!=null&&Id==x.Id&&OrderIndex==x.OrderIndex&&RecipientActorId==x.RecipientActorId
            &&Status==x.Status&&UpdatedRevision==x.UpdatedRevision&&DecisionRevision==x.DecisionRevision&&DecisionId==x.DecisionId
            &&MoveId==x.MoveId&&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId;
    }

    /// <summary>One paid Defensive Formation use, its fixed encounter identity, ordered recipients,
    /// per-recipient shift decisions and the captured source-turn expiry.</summary>
    public sealed class DefensiveFormationActivationRecord
    {
        private readonly DefensiveFormationShiftRecord[] shifts;
        public string Id { get; }
        public string SourceActorId { get; }
        public string EncounterId { get; }
        public string TurnId { get; }
        public int TurnOrdinal { get; }
        public long CreatedRevision { get; }
        public long UpdatedRevision { get; }
        public RuleTime At { get; }
        public long ExpirySlot { get; }
        public DefensiveFormationStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }
        public DefensiveFormationShiftRecord[] Shifts=>shifts.ToArray();
        public bool Active=>Status==DefensiveFormationStatus.Active;
        public DefensiveFormationActivationRecord(string id,string sourceActorId,string encounterId,string turnId,int turnOrdinal,
            long createdRevision,long updatedRevision,RuleTime at,long expirySlot,DefensiveFormationShiftRecord[] shifts,
            DefensiveFormationStatus status=DefensiveFormationStatus.Active,long resolvedRevision=0,string resolutionId="")
        {
            var rows=shifts??Array.Empty<DefensiveFormationShiftRecord>();
            if(!Validation.ValidId(id)||!Validation.ValidId(sourceActorId)||!Validation.ValidId(encounterId)||!Validation.ValidId(turnId)
                ||turnOrdinal<0||createdRevision<1||updatedRevision<createdRevision||expirySlot<0||rows.Length<1||rows.Length>3||rows.Any(x=>x==null)
                ||rows.Select(x=>x.OrderIndex).Where((x,i)=>x!=i).Any()||rows.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=rows.Length
                ||rows.Any(x=>x.UpdatedRevision>updatedRevision)||!Enum.IsDefined(typeof(DefensiveFormationStatus),status)
                ||status==DefensiveFormationStatus.Active&&(resolvedRevision!=0||resolutionId!="")
                ||status==DefensiveFormationStatus.Expired&&(resolvedRevision<updatedRevision||!Validation.ValidId(resolutionId)
                    ||rows.Any(x=>x.Status==DefensiveFormationShiftStatus.Queued||x.Status==DefensiveFormationShiftStatus.AwaitingResponse
                        ||x.Status==DefensiveFormationShiftStatus.Moving)))
                throw new ArgumentException("Invalid Defensive Formation activation.");
            Id=id;SourceActorId=sourceActorId;EncounterId=encounterId;TurnId=turnId;TurnOrdinal=turnOrdinal;CreatedRevision=createdRevision;
            UpdatedRevision=updatedRevision;At=at;ExpirySlot=expirySlot;this.shifts=rows.ToArray();Status=status;ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }
        public DefensiveFormationActivationRecord UpdateShift(DefensiveFormationShiftRecord shift,long revision)
        {
            if(!Active||shift==null||shift.OrderIndex<0||shift.OrderIndex>=shifts.Length||revision<UpdatedRevision
                ||shifts[shift.OrderIndex].Id!=shift.Id)throw new ArgumentException("Invalid Defensive Formation shift update.");
            var next=shifts.ToArray();next[shift.OrderIndex]=shift;
            return new DefensiveFormationActivationRecord(Id,SourceActorId,EncounterId,TurnId,TurnOrdinal,CreatedRevision,revision,At,ExpirySlot,next,Status);
        }
        public DefensiveFormationActivationRecord Expire(long revision,string marker)
        {
            if(!Active)throw new InvalidOperationException("Defensive Formation already expired.");
            return new DefensiveFormationActivationRecord(Id,SourceActorId,EncounterId,TurnId,TurnOrdinal,CreatedRevision,revision,At,ExpirySlot,
                shifts,DefensiveFormationStatus.Expired,revision,marker);
        }
        public bool SameAs(DefensiveFormationActivationRecord x)=>x!=null&&Id==x.Id&&SourceActorId==x.SourceActorId&&EncounterId==x.EncounterId
            &&TurnId==x.TurnId&&TurnOrdinal==x.TurnOrdinal&&CreatedRevision==x.CreatedRevision&&UpdatedRevision==x.UpdatedRevision&&At==x.At
            &&ExpirySlot==x.ExpirySlot&&Status==x.Status&&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId
            &&shifts.Length==x.shifts.Length&&shifts.Zip(x.shifts,(a,b)=>a.SameAs(b)).All(v=>v);
    }

    public static class DefensiveFormationValidation
    {
        public const int MaxActivations=128;
        private static long FutureStartSlot(Snapshot s,string actor,long atSlot)
        {
            int index=Array.IndexOf(s.WorldSchedule.Order.ToArray(),actor);if(index<0)return -1;
            long count=s.WorldSchedule.Order.Count,candidate=index;
            return candidate<=atSlot?checked(candidate+checked(((atSlot-candidate)/count+1)*count)):candidate;
        }
        public static void Validate(Snapshot s)
        {
            if(s.DefensiveFormations==null||s.DefensiveFormations.Length>MaxActivations||s.DefensiveFormations.Any(x=>x==null))
                throw new ArgumentException("Invalid Defensive Formation history.");
            if(s.SchemaVersion<Snapshot.DefensiveFormationSchema) {
                if(s.DefensiveFormations.Length!=0||s.TacticalMoves.Any(x=>x.Kind==TacticalMoveKind.DefensiveFormationShift))
                    throw new ArgumentException("Defensive Formation requires schema34.");
                return;
            }
            if(s.DefensiveFormations.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.DefensiveFormations.Length
                ||s.DefensiveFormations.Select(x=>x.CreatedRevision).Distinct().Count()!=s.DefensiveFormations.Length
                ||s.DefensiveFormations.GroupBy(x=>x.SourceActorId+"|"+x.EncounterId,StringComparer.Ordinal).Any(g=>g.Count()>1))
                throw new ArgumentException("Defensive Formation encounter use was duplicated.");
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            foreach(var activation in s.DefensiveFormations) {
                var grant=s.CharacterFeatureGrants.SingleOrDefault(x=>x.ActorId==activation.SourceActorId&&x.FeatureId==CharacterFeatureIds.DefensiveFormation
                    &&x.ClassName=="Soldier"&&(x.ClassLevel==3||x.ClassLevel==4&&s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema)
                    &&x.Origin==CharacterFeatureGrantOrigin.SelectedCard);
                if(!Actor(activation.SourceActorId)||grant==null||!s.WorldSchedule.Order.Contains(activation.SourceActorId)
                    ||activation.CreatedRevision>s.Revision||activation.UpdatedRevision>s.Revision||activation.ExpirySlot>long.MaxValue-1
                    ||activation.At>s.RuleClock
                    ||activation.Status==DefensiveFormationStatus.Active&&s.WorldSchedule.ProcessedSlot>=activation.ExpirySlot
                    ||activation.Status==DefensiveFormationStatus.Expired&&(s.WorldSchedule.ProcessedSlot<activation.ExpirySlot
                        ||activation.ResolutionId!=s.WorldSchedule.MarkerId(activation.ExpirySlot)+".start"))
                    throw new ArgumentException("Defensive Formation activation is not source-bound to a valid encounter interval.");
                var encounter=EncounterHistory.AtRevision(s,activation.CreatedRevision);
                if(encounter==null||encounter.Id!=activation.EncounterId||!EncounterHistory.MatchesTurn(encounter,activation.TurnOrdinal,activation.SourceActorId)
                    ||activation.TurnId!=encounter.Id+".turn."+activation.TurnOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    ||activation.ExpirySlot!=FutureStartSlot(s,activation.SourceActorId,s.WorldSchedule.SlotAt(activation.At)))
                    throw new ArgumentException("Defensive Formation encounter identity or expiry is invalid.");
                var receipt=s.Receipts.SingleOrDefault(x=>x.Id==activation.Id&&x.Revision==activation.CreatedRevision);
                if(receipt==null)throw new ArgumentException("Defensive Formation activation receipt is missing.");
                Command command;try{command=CommandHistory.Read(receipt);}catch(ArgumentException){throw new ArgumentException("Defensive Formation activation receipt is malformed.");}
                var activationShifts=activation.Shifts;
                if(command.Kind!=CommandKind.ActivateDefensiveFormation||command.Actor!=activation.SourceActorId||command.DefensiveFormation==null
                    ||!command.DefensiveFormation.RecipientIds.SequenceEqual(activationShifts.Select(x=>x.RecipientActorId),StringComparer.Ordinal))
                    throw new ArgumentException("Defensive Formation selected recipients do not match its activation receipt.");
                for(int i=0;i<activationShifts.Length;i++) {
                    var shift=activationShifts[i];
                    if(shift.Id!=activation.Id+".shift."+i.ToString(System.Globalization.CultureInfo.InvariantCulture)||!Actor(shift.RecipientActorId)
                        ||!s.WorldSchedule.Order.Contains(shift.RecipientActorId)||shift.UpdatedRevision>activation.UpdatedRevision
                        ||i>0&&shift.Status!=DefensiveFormationShiftStatus.Queued&&activationShifts.Take(i).Any(x=>x.Status==DefensiveFormationShiftStatus.Queued
                            ||x.Status==DefensiveFormationShiftStatus.AwaitingResponse||x.Status==DefensiveFormationShiftStatus.Moving))
                        throw new ArgumentException("Defensive Formation recipient order or progress is invalid.");
                    if(shift.DecisionRevision>0) {
                        var decision=s.Receipts.SingleOrDefault(x=>x.Id==shift.DecisionId&&x.Revision==shift.DecisionRevision);
                        if(decision==null)throw new ArgumentException("Defensive Formation shift decision receipt is missing.");
                        if(shift.Status==DefensiveFormationShiftStatus.Declined||shift.Status==DefensiveFormationShiftStatus.Moving
                            ||shift.Status==DefensiveFormationShiftStatus.Moved||shift.Status==DefensiveFormationShiftStatus.Skipped&&shift.MoveId!="") {
                            Command response;try{response=CommandHistory.Read(decision);}catch(ArgumentException){throw new ArgumentException("Defensive Formation shift receipt is malformed.");}
                            if(response.Kind!=CommandKind.RespondDefensiveFormation||response.Actor!=shift.RecipientActorId||response.Target!=activation.Id
                                ||response.Combat==null||response.Combat.TurnId!=activation.TurnId
                                ||(shift.Status==DefensiveFormationShiftStatus.Declined&&response.Combat.Choice)
                                ||(shift.Status==DefensiveFormationShiftStatus.Moving||shift.Status==DefensiveFormationShiftStatus.Moved)&&!response.Combat.Choice)
                                throw new ArgumentException("Defensive Formation shift decision does not match its receipt.");
                        }
                        if(shift.Status==DefensiveFormationShiftStatus.Moved) {
                            var completed= s.TacticalMoves.SingleOrDefault(x=>x.Id==shift.MoveId&&x.Kind==TacticalMoveKind.DefensiveFormationShift
                                &&x.ActorId==shift.RecipientActorId&&x.ParentDefensiveFormationId==activation.Id&&x.Status==TacticalMoveStatus.Completed);
                            var resolved=s.Receipts.SingleOrDefault(x=>x.Id==shift.ResolutionId&&x.Revision==shift.ResolvedRevision);
                            if(completed==null||resolved==null)throw new ArgumentException("Defensive Formation completed movement is not linked to its history.");
                        } else if(shift.Status==DefensiveFormationShiftStatus.Moving) {
                            var pending=s.TacticalMoves.SingleOrDefault(x=>x.Id==shift.MoveId&&x.Kind==TacticalMoveKind.DefensiveFormationShift
                                &&x.ActorId==shift.RecipientActorId&&x.ParentDefensiveFormationId==activation.Id
                                &&(x.Status!=TacticalMoveStatus.Completed&&x.Status!=TacticalMoveStatus.Interrupted
                                    ||x.Status==TacticalMoveStatus.Completed&&(s.OverwatchOffers.Any(o=>o.MoveId==x.Id&&o.Status==OverwatchOfferStatus.Pending)
                                        ||s.PressOffers.Any(o=>o.MoveId==x.Id&&o.Status==PressOfferStatus.Pending)
                                        ||s.OverwatchRiderChoices.Any(o=>o.Status==OverwatchRiderChoiceStatus.Pending)
                                        ||s.TacticalMoves.Any(m=>m.Pending))));
                            if(pending==null)throw new ArgumentException("Defensive Formation pending movement is not linked to its history.");
                        }
                    }
                    if(shift.Status==DefensiveFormationShiftStatus.Skipped) {
                        if(!s.Receipts.Any(x=>x.Id==shift.ResolutionId&&x.Revision==shift.ResolvedRevision))
                            throw new ArgumentException("Defensive Formation skipped shift lacks its triggering receipt.");
                        if(shift.MoveId!=""&&!s.TacticalMoves.Any(x=>x.Id==shift.MoveId&&x.Kind==TacticalMoveKind.DefensiveFormationShift
                            &&x.ActorId==shift.RecipientActorId&&x.ParentDefensiveFormationId==activation.Id&&x.Status==TacticalMoveStatus.Interrupted))
                            throw new ArgumentException("Defensive Formation skipped movement is not linked to its interrupted step.");
                    }
                }
            }
            if(s.DefensiveFormations.SelectMany(x=>x.Shifts).Count(x=>x.Status==DefensiveFormationShiftStatus.AwaitingResponse
                    ||x.Status==DefensiveFormationShiftStatus.Moving)>1)
                throw new ArgumentException("Only one Defensive Formation continuation can be pending.");
        }
    }
}
