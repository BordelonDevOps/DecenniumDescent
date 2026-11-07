using System;
using System.Linq;
using System.Globalization;

namespace Decennium.Foundation
{
    public enum ReadyActionStatus { Armed = 1, Released = 2, Expired = 3, Replaced = 4 }
    public enum ReadyOccurrenceStatus { Pending = 1, Accepted = 2, Declined = 3, Invalidated = 4 }

    /// <summary>Persisted declaration for the bounded TEST_ONLY Ready Action. The action and
    /// next-own-start expiry are anchored at preparation; movement occurrences are separate.</summary>
    public sealed class ReadyActionRecord
    {
        public string Id { get; }
        public string PreparationCommandId { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public string WeaponId { get; }
        public int TriggerDistanceFeet { get; }
        public AttackKnockoutMode Knockout { get; }
        public int PreparedTurnOrdinal { get; }
        public int ExpiresAfterTurnOrdinal { get; }
        public RuleTime ExpiresAt { get; }
        public long PreparedRevision { get; }
        public ReadyActionStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }
        public bool Armed => Status == ReadyActionStatus.Armed;

        public ReadyActionRecord(string id,string preparationCommandId,string actorId,string targetId,string weaponId,
            int triggerDistanceFeet,AttackKnockoutMode knockout,int preparedTurnOrdinal,int expiresAfterTurnOrdinal,
            RuleTime expiresAt,long preparedRevision,ReadyActionStatus status=ReadyActionStatus.Armed,long resolvedRevision=0,string resolutionId="")
        {
            if(new[]{id,preparationCommandId,actorId,targetId}.Any(x=>!Validation.ValidId(x))||actorId==targetId
                ||weaponId==null||weaponId!=""&&!Validation.ValidId(weaponId)||triggerDistanceFeet!=5
                ||!Enum.IsDefined(typeof(AttackKnockoutMode),knockout)||preparedTurnOrdinal<0
                ||expiresAfterTurnOrdinal<=preparedTurnOrdinal||expiresAt<default(RuleTime)||preparedRevision<1||resolvedRevision<0
                ||!Enum.IsDefined(typeof(ReadyActionStatus),status)
                ||status==ReadyActionStatus.Armed&&(resolvedRevision!=0||resolutionId!="")
                ||status!=ReadyActionStatus.Armed&&(resolvedRevision<preparedRevision||!Validation.ValidId(resolutionId)))
                throw new ArgumentException("Invalid Ready Action declaration.");
            Id=id;PreparationCommandId=preparationCommandId;ActorId=actorId;TargetId=targetId;WeaponId=weaponId;
            TriggerDistanceFeet=triggerDistanceFeet;Knockout=knockout;PreparedTurnOrdinal=preparedTurnOrdinal;
            ExpiresAfterTurnOrdinal=expiresAfterTurnOrdinal;ExpiresAt=expiresAt;PreparedRevision=preparedRevision;Status=status;
            ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }

        public ReadyActionRecord Resolve(ReadyActionStatus status,long revision,string resolutionId)
        {
            if(Status!=ReadyActionStatus.Armed||status==ReadyActionStatus.Armed)
                throw new InvalidOperationException("Only an armed Ready Action can resolve.");
            return new ReadyActionRecord(Id,PreparationCommandId,ActorId,TargetId,WeaponId,TriggerDistanceFeet,Knockout,
                PreparedTurnOrdinal,ExpiresAfterTurnOrdinal,ExpiresAt,PreparedRevision,status,revision,resolutionId);
        }

        public bool SameAs(ReadyActionRecord x)=>x!=null&&Id==x.Id&&PreparationCommandId==x.PreparationCommandId
            &&ActorId==x.ActorId&&TargetId==x.TargetId&&WeaponId==x.WeaponId&&TriggerDistanceFeet==x.TriggerDistanceFeet
            &&Knockout==x.Knockout&&PreparedTurnOrdinal==x.PreparedTurnOrdinal&&ExpiresAfterTurnOrdinal==x.ExpiresAfterTurnOrdinal
            &&ExpiresAt==x.ExpiresAt&&PreparedRevision==x.PreparedRevision&&Status==x.Status&&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId;
    }

    /// <summary>One target-entry occurrence captured by a completed tactical step. Its stable
    /// timestamps place it in the same queue as Press, trap, and Overwatch occurrences.</summary>
    public sealed class ReadyOccurrenceRecord
    {
        public string Id { get; }
        public string ReadyActionId { get; }
        public string MoveId { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public int OwnerXAtTrigger { get; }
        public int OwnerYAtTrigger { get; }
        public long CreatedRevision { get; }
        public long SourceAppliedRevision { get; }
        public ReadyOccurrenceStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionCommandId { get; }
        public string AttackId { get; }
        public bool Pending => Status == ReadyOccurrenceStatus.Pending;

        public ReadyOccurrenceRecord(string id,string readyActionId,string moveId,string ownerId,string targetId,
            int ownerXAtTrigger,int ownerYAtTrigger,long createdRevision,long sourceAppliedRevision,
            ReadyOccurrenceStatus status=ReadyOccurrenceStatus.Pending,long resolvedRevision=0,
            string resolutionCommandId="",string attackId="")
        {
            if(new[]{id,readyActionId,moveId,ownerId,targetId}.Any(x=>!Validation.ValidId(x))||ownerId==targetId
                ||createdRevision<1||sourceAppliedRevision<1||resolvedRevision<0
                ||!Enum.IsDefined(typeof(ReadyOccurrenceStatus),status)
                ||(status==ReadyOccurrenceStatus.Pending)!=(resolvedRevision==0)
                ||status==ReadyOccurrenceStatus.Pending&&(resolutionCommandId!=""||attackId!="")
                ||status==ReadyOccurrenceStatus.Accepted&&(!Validation.ValidId(resolutionCommandId)||!Validation.ValidId(attackId))
                ||status==ReadyOccurrenceStatus.Declined&&(!Validation.ValidId(resolutionCommandId)||attackId!="")
                ||status==ReadyOccurrenceStatus.Invalidated&&(resolutionCommandId==null||resolutionCommandId!=""&&!Validation.ValidId(resolutionCommandId)||attackId!=""))
                throw new ArgumentException("Invalid Ready Action occurrence.");
            Id=id;ReadyActionId=readyActionId;MoveId=moveId;OwnerId=ownerId;TargetId=targetId;
            OwnerXAtTrigger=ownerXAtTrigger;OwnerYAtTrigger=ownerYAtTrigger;CreatedRevision=createdRevision;
            SourceAppliedRevision=sourceAppliedRevision;Status=status;ResolvedRevision=resolvedRevision;
            ResolutionCommandId=resolutionCommandId;AttackId=attackId;
        }

        public ReadyOccurrenceRecord Resolve(ReadyOccurrenceStatus status,long revision,string commandId="",string attackId="")
        {
            if(Status!=ReadyOccurrenceStatus.Pending||status==ReadyOccurrenceStatus.Pending)
                throw new InvalidOperationException("Ready Action occurrence is already resolved.");
            return new ReadyOccurrenceRecord(Id,ReadyActionId,MoveId,OwnerId,TargetId,OwnerXAtTrigger,OwnerYAtTrigger,
                CreatedRevision,SourceAppliedRevision,status,revision,commandId,attackId);
        }

        public bool SameAs(ReadyOccurrenceRecord x)=>x!=null&&Id==x.Id&&ReadyActionId==x.ReadyActionId&&MoveId==x.MoveId
            &&OwnerId==x.OwnerId&&TargetId==x.TargetId&&OwnerXAtTrigger==x.OwnerXAtTrigger&&OwnerYAtTrigger==x.OwnerYAtTrigger
            &&CreatedRevision==x.CreatedRevision&&SourceAppliedRevision==x.SourceAppliedRevision&&Status==x.Status
            &&ResolvedRevision==x.ResolvedRevision&&ResolutionCommandId==x.ResolutionCommandId&&AttackId==x.AttackId;
    }

    public static class ReadyActionValidation
    {
        public const int MaxActions=128,MaxOccurrences=256;

        public static void Validate(Snapshot s)
        {
            if(s.ReadyActions==null||s.ReadyOccurrences==null||s.ReadyActions.Length>MaxActions
                ||s.ReadyOccurrences.Length>MaxOccurrences||s.ReadyActions.Any(x=>x==null)||s.ReadyOccurrences.Any(x=>x==null))
                throw new ArgumentException("Invalid Ready Action collections.");
            if(s.SchemaVersion<Snapshot.ReadyActionSchema) {
                if(s.ReadyActions.Length+s.ReadyOccurrences.Length!=0)throw new ArgumentException("Ready Action requires schema58.");
                return;
            }
            if(s.ReadyActions.Length+s.ReadyOccurrences.Length>0&&(s.WorldSchedule==null||s.Encounter==null))
                throw new ArgumentException("Ready Action requires an active tactical calendar.");
            if(s.ReadyActions.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.ReadyActions.Length
                ||s.ReadyActions.Where(x=>x.Armed).GroupBy(x=>x.ActorId,StringComparer.Ordinal).Any(x=>x.Count()>1)
                ||s.ReadyOccurrences.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.ReadyOccurrences.Length
                ||s.ReadyOccurrences.Count(x=>x.Pending)>MaxActions)
                throw new ArgumentException("Duplicate or excess Ready Action history.");

            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            Command ReceiptCommand(long revision,string id)
            {
                var receipt=s.Receipts.SingleOrDefault(x=>x.Revision==revision&&x.Id==id);
                if(receipt==null)return null;
                try{return CommandHistory.Read(receipt);}catch(ArgumentException){return null;}
            }

            foreach(var action in s.ReadyActions) {
                if(!Actor(action.ActorId)||!Actor(action.TargetId)||!s.WorldSchedule.Order.Contains(action.ActorId)
                    ||!s.WorldSchedule.Order.Contains(action.TargetId)||action.PreparedRevision>s.Revision
                    ||action.ResolvedRevision>s.Revision||action.Status==ReadyActionStatus.Armed
                        &&(action.ExpiresAfterTurnOrdinal<=s.Encounter.TurnOrdinal||action.ExpiresAt<=s.RuleClock))
                    throw new ArgumentException("Invalid Ready Action actor, timing, or target.");
                var encounter=EncounterHistory.AtRevision(s,action.PreparedRevision);
                if(encounter==null||!EncounterHistory.MatchesTurn(encounter,action.PreparedTurnOrdinal,action.ActorId)
                    ||!encounter.Order.SequenceEqual(s.WorldSchedule.Order)||encounter.Origin!=s.WorldSchedule.Origin
                    ||action.ExpiresAfterTurnOrdinal!=checked(action.PreparedTurnOrdinal+encounter.Order.Count)
                    ||action.ExpiresAt!=s.WorldSchedule.Start(action.ExpiresAfterTurnOrdinal))
                    throw new ArgumentException("Ready Action preparation is not anchored to the next own turn.");
                var preparation=ReceiptCommand(action.PreparedRevision,action.PreparationCommandId);
                if(preparation==null||preparation.Kind!=CommandKind.Ready||preparation.Actor!=action.ActorId||preparation.Target!=action.TargetId
                    ||preparation.X!=action.TriggerDistanceFeet||preparation.Y!=0||preparation.Combat==null
                    ||preparation.Combat.WeaponId!=action.WeaponId||preparation.Combat.Knockout!=action.Knockout
                    ||preparation.Combat.Stance!=0||preparation.Combat.Choice
                    ||preparation.Combat.PressInstruction!=PressHitInstruction.KeepExisting
                    ||preparation.Combat.TurnId!=encounter.Id+".turn."+action.PreparedTurnOrdinal.ToString(CultureInfo.InvariantCulture))
                    throw new ArgumentException("Ready Action preparation command does not match its record.");
                if(action.Status==ReadyActionStatus.Released) {
                    if(!s.ReadyOccurrences.Any(x=>x.Id==action.ResolutionId&&x.ReadyActionId==action.Id
                        &&x.Status==ReadyOccurrenceStatus.Accepted&&x.ResolvedRevision==action.ResolvedRevision))
                        throw new ArgumentException("Released Ready Action is missing its accepted occurrence.");
                } else if(action.Status==ReadyActionStatus.Expired) {
                    var command=ReceiptCommand(action.ResolvedRevision,action.ResolutionId);
                    if(command==null||action.ExpiresAt>s.RuleClock||s.WorldSchedule.ProcessedSlot<action.ExpiresAfterTurnOrdinal
                        ||s.ReadyOccurrences.Any(x=>x.ReadyActionId==action.Id&&x.Pending))
                        throw new ArgumentException("Ready Action expiry is not anchored to its shared-clock deadline.");
                } else if(action.Status==ReadyActionStatus.Replaced) {
                    var replacement=s.ReadyActions.SingleOrDefault(x=>x.Id==action.ResolutionId&&x.ActorId==action.ActorId
                        &&x.PreparedRevision==action.ResolvedRevision);
                    if(replacement==null)throw new ArgumentException("Replaced Ready Action has no replacement declaration.");
                }
            }

            foreach(var occurrence in s.ReadyOccurrences) {
                var action=s.ReadyActions.SingleOrDefault(x=>x.Id==occurrence.ReadyActionId);
                var move=s.TacticalMoves.SingleOrDefault(x=>x.Id==occurrence.MoveId);
                if(action==null||move==null||!Actor(occurrence.OwnerId)||!Actor(occurrence.TargetId)
                    ||occurrence.OwnerId!=action.ActorId||occurrence.TargetId!=action.TargetId
                    ||occurrence.SourceAppliedRevision!=action.PreparedRevision||occurrence.CreatedRevision>s.Revision
                    ||occurrence.ResolvedRevision>s.Revision||move.ActorId!=occurrence.TargetId||move.Status!=TacticalMoveStatus.Completed
                    ||move.ResolvedRevision!=occurrence.CreatedRevision||EncounterHistory.AtRevision(s,move.Revision)?.Id
                        !=EncounterHistory.AtRevision(s,occurrence.CreatedRevision)?.Id
                    ||DistanceCells(move.FromX,move.FromY,occurrence.OwnerXAtTrigger,occurrence.OwnerYAtTrigger)<=1
                    ||DistanceCells(move.ToX,move.ToY,occurrence.OwnerXAtTrigger,occurrence.OwnerYAtTrigger)>1)
                    throw new ArgumentException("Ready Action occurrence does not match a completed entry step.");
                if(occurrence.Status==ReadyOccurrenceStatus.Pending) {
                    if(!action.Armed||s.ReadyOccurrences.Count(x=>x.Pending&&x.ReadyActionId==action.Id)>1)
                        throw new ArgumentException("Pending Ready occurrence has no armed declaration or is duplicated.");
                } else if(occurrence.Status==ReadyOccurrenceStatus.Accepted) {
                    var command=ReceiptCommand(occurrence.ResolvedRevision,occurrence.ResolutionCommandId);
                    var attack=s.MeleeAttacks.SingleOrDefault(x=>x.Id==occurrence.AttackId);
                    if(action.Status!=ReadyActionStatus.Released||action.ResolutionId!=occurrence.Id||action.ResolvedRevision!=occurrence.ResolvedRevision
                        ||command?.Kind!=CommandKind.RespondReady||command.Actor!=occurrence.OwnerId||command.Target!=occurrence.Id
                        ||command.Combat?.Choice!=true||attack==null||attack.Revision!=occurrence.ResolvedRevision
                        ||attack.AttackerId!=occurrence.OwnerId||attack.TargetId!=occurrence.TargetId||attack.Opportunity
                        ||attack.WeaponId!=(action.WeaponId==""?CombatProfileIds.OrdinaryUnarmed:action.WeaponId))
                        throw new ArgumentException("Accepted Ready occurrence does not match its attack and response.");
                } else if(occurrence.Status==ReadyOccurrenceStatus.Declined) {
                    var command=ReceiptCommand(occurrence.ResolvedRevision,occurrence.ResolutionCommandId);
                    bool wasDeclinedWhileArmed=action.Armed||occurrence.ResolvedRevision<action.ResolvedRevision;
                    if(!wasDeclinedWhileArmed||command?.Kind!=CommandKind.RespondReady||command.Actor!=occurrence.OwnerId
                        ||command.Target!=occurrence.Id||command.Combat?.Choice!=false)
                        throw new ArgumentException("Declined Ready occurrence has no matching response.");
                } else if(occurrence.ResolutionCommandId=="") {
                    if(occurrence.AttackId!="")throw new ArgumentException("Automatic Ready invalidation cannot claim an attack.");
                } else {
                    var command=ReceiptCommand(occurrence.ResolvedRevision,occurrence.ResolutionCommandId);
                    if(command?.Kind!=CommandKind.RespondReady||command.Actor!=occurrence.OwnerId||command.Target!=occurrence.Id)
                        throw new ArgumentException("Invalidated Ready occurrence has no matching response.");
                }
            }

            foreach(var action in s.ReadyActions.Where(x=>x.Status==ReadyActionStatus.Released))
                if(s.ReadyOccurrences.Count(x=>x.ReadyActionId==action.Id&&x.Status==ReadyOccurrenceStatus.Accepted)!=1)
                    throw new ArgumentException("Released Ready Action has more than one accepted occurrence.");
        }

        private static long DistanceCells(int ax,int ay,int bx,int by)
            =>Math.Max(Math.Abs((long)ax-bx),Math.Abs((long)ay-by));
    }
}
