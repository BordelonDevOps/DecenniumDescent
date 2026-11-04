using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum OverwatchOfferStatus { Pending, Accepted, Declined, Invalidated }
    public enum OverwatchRiderChoiceStatus { Pending, Resolved, Expired }

    /// <summary>One post-step Base Overwatch occurrence. Source application time remains fixed
    /// to the designation; the movement revision is the occurrence time used with Press ordering.</summary>
    public sealed class OverwatchOfferRecord
    {
        public string Id { get; }
        public string MoveId { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public string DesignationId { get; }
        public long CreatedRevision { get; }
        public long SourceAppliedRevision { get; }
        public OverwatchOfferStatus Status { get; }
        public long ResolvedRevision { get; }
        public string AttackId { get; }
        public OverwatchOfferRecord(string id,string moveId,string ownerId,string targetId,string designationId,long createdRevision,
            long sourceAppliedRevision,OverwatchOfferStatus status=OverwatchOfferStatus.Pending,long resolvedRevision=0,string attackId="")
        {
            if(new[]{id,moveId,ownerId,targetId,designationId}.Any(x=>!Validation.ValidId(x))||ownerId==targetId||createdRevision<1
                ||sourceAppliedRevision<1||sourceAppliedRevision>createdRevision||!Enum.IsDefined(typeof(OverwatchOfferStatus),status)
                ||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<createdRevision||attackId==null||attackId!=""&&!Validation.ValidId(attackId)
                ||(status==OverwatchOfferStatus.Pending)!=(resolvedRevision==0)
                ||status==OverwatchOfferStatus.Accepted!=(attackId!=""))throw new ArgumentException("Invalid Overwatch offer.");
            Id=id;MoveId=moveId;OwnerId=ownerId;TargetId=targetId;DesignationId=designationId;CreatedRevision=createdRevision;
            SourceAppliedRevision=sourceAppliedRevision;Status=status;ResolvedRevision=resolvedRevision;AttackId=attackId;
        }
        public OverwatchOfferRecord Resolve(OverwatchOfferStatus status,long revision,string attackId="")
            =>new OverwatchOfferRecord(Id,MoveId,OwnerId,TargetId,DesignationId,CreatedRevision,SourceAppliedRevision,status,revision,attackId);
        public bool SameAs(OverwatchOfferRecord x)=>x!=null&&Id==x.Id&&MoveId==x.MoveId&&OwnerId==x.OwnerId&&TargetId==x.TargetId
            &&DesignationId==x.DesignationId&&CreatedRevision==x.CreatedRevision&&SourceAppliedRevision==x.SourceAppliedRevision
            &&Status==x.Status&&ResolvedRevision==x.ResolvedRevision&&AttackId==x.AttackId;
    }

    /// <summary>Persisted controller choice and resulting rider application. Push save data and
    /// forced-movement endpoints are retained so replay can verify the full consequence.</summary>
    public sealed class OverwatchRiderChoiceRecord
    {
        public string Id { get; }
        public string OfferId { get; }
        public string AttackId { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public long CreatedRevision { get; }
        public OverwatchRiderChoiceStatus Status { get; }
        public OverwatchRider Choice { get; }
        public long ResolvedRevision { get; }
        public int ExpiresAfterTurnOrdinal { get; }
        public int SaveNatural { get; }
        public int SaveModifier { get; }
        public int SaveDc { get; }
        public long SaveTotal { get; }
        public bool SaveSucceeded { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long RandomWordsConsumed { get; }
        public int FromX { get; }
        public int FromY { get; }
        public int ToX { get; }
        public int ToY { get; }
        public int MovedFeet { get; }

        public OverwatchRiderChoiceRecord(string id,string offerId,string attackId,string ownerId,string targetId,long createdRevision,
            OverwatchRiderChoiceStatus status=OverwatchRiderChoiceStatus.Pending,OverwatchRider choice=OverwatchRider.None,
            long resolvedRevision=0,int expiresAfterTurnOrdinal=-1,int saveNatural=0,int saveModifier=0,int saveDc=0,long saveTotal=0,
            bool saveSucceeded=false,uint randomBefore=1,uint randomAfter=1,long randomWordsConsumed=0,
            int fromX=0,int fromY=0,int toX=0,int toY=0,int movedFeet=0)
        {
            if(new[]{id,offerId,attackId,ownerId,targetId}.Any(x=>!Validation.ValidId(x))||createdRevision<1
                ||!Enum.IsDefined(typeof(OverwatchRiderChoiceStatus),status)||!Enum.IsDefined(typeof(OverwatchRider),choice)
                ||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<createdRevision||expiresAfterTurnOrdinal< -1
                ||saveNatural<0||saveNatural>20||saveModifier< -100||saveModifier>100||saveDc<0||saveDc>100||saveTotal< -200||saveTotal>200
                ||randomBefore==0||randomAfter==0||randomWordsConsumed<0||(movedFeet!=0&&movedFeet!=5)
                ||(status==OverwatchRiderChoiceStatus.Pending)!=(choice==OverwatchRider.None)
                ||(status==OverwatchRiderChoiceStatus.Pending)!=(resolvedRevision==0)
                ||status==OverwatchRiderChoiceStatus.Expired&&(choice!=OverwatchRider.Snare||expiresAfterTurnOrdinal<0)
                ||choice==OverwatchRider.Snare&&status!=OverwatchRiderChoiceStatus.Pending&&expiresAfterTurnOrdinal<0
                ||choice!=OverwatchRider.Snare&&expiresAfterTurnOrdinal!=-1
                ||choice==OverwatchRider.Push&&status!=OverwatchRiderChoiceStatus.Pending
                    &&(saveNatural==0?(saveSucceeded||saveTotal!=0||randomWordsConsumed!=0||randomBefore!=randomAfter)
                        :(saveTotal!=(long)saveNatural+saveModifier||saveSucceeded!=(saveTotal>=saveDc)||randomWordsConsumed<1))
                ||choice!=OverwatchRider.Push&&(saveNatural!=0||saveModifier!=0||saveDc!=0||saveTotal!=0||saveSucceeded
                    ||randomWordsConsumed!=0||fromX!=0||fromY!=0||toX!=0||toY!=0||movedFeet!=0))
                throw new ArgumentException("Invalid Overwatch rider choice.");
            Id=id;OfferId=offerId;AttackId=attackId;OwnerId=ownerId;TargetId=targetId;CreatedRevision=createdRevision;
            Status=status;Choice=choice;ResolvedRevision=resolvedRevision;ExpiresAfterTurnOrdinal=expiresAfterTurnOrdinal;
            SaveNatural=saveNatural;SaveModifier=saveModifier;SaveDc=saveDc;SaveTotal=saveTotal;SaveSucceeded=saveSucceeded;
            RandomBefore=randomBefore;RandomAfter=randomAfter;RandomWordsConsumed=randomWordsConsumed;
            FromX=fromX;FromY=fromY;ToX=toX;ToY=toY;MovedFeet=movedFeet;
        }
        public OverwatchRiderChoiceRecord Resolve(OverwatchRider choice,long revision,int expiresAfterTurnOrdinal=-1,
            int saveNatural=0,int saveModifier=0,int saveDc=0,long saveTotal=0,bool saveSucceeded=false,uint randomBefore=1,uint randomAfter=1,
            long randomWordsConsumed=0,int fromX=0,int fromY=0,int toX=0,int toY=0,int movedFeet=0)
            =>new OverwatchRiderChoiceRecord(Id,OfferId,AttackId,OwnerId,TargetId,CreatedRevision,OverwatchRiderChoiceStatus.Resolved,
                choice,revision,expiresAfterTurnOrdinal,saveNatural,saveModifier,saveDc,saveTotal,saveSucceeded,randomBefore,randomAfter,
                randomWordsConsumed,fromX,fromY,toX,toY,movedFeet);
        public OverwatchRiderChoiceRecord Expire(long revision)
        {
            if(Status!=OverwatchRiderChoiceStatus.Resolved||Choice!=OverwatchRider.Snare||revision<ResolvedRevision)
                throw new InvalidOperationException("Only an active Snare can expire.");
            return new OverwatchRiderChoiceRecord(Id,OfferId,AttackId,OwnerId,TargetId,CreatedRevision,OverwatchRiderChoiceStatus.Expired,
                Choice,revision,ExpiresAfterTurnOrdinal,randomBefore:RandomBefore,randomAfter:RandomAfter);
        }
        public bool SameAs(OverwatchRiderChoiceRecord x)=>x!=null&&Id==x.Id&&OfferId==x.OfferId&&AttackId==x.AttackId&&OwnerId==x.OwnerId
            &&TargetId==x.TargetId&&CreatedRevision==x.CreatedRevision&&Status==x.Status&&Choice==x.Choice&&ResolvedRevision==x.ResolvedRevision
            &&ExpiresAfterTurnOrdinal==x.ExpiresAfterTurnOrdinal&&SaveNatural==x.SaveNatural&&SaveModifier==x.SaveModifier&&SaveDc==x.SaveDc
            &&SaveTotal==x.SaveTotal&&SaveSucceeded==x.SaveSucceeded&&RandomBefore==x.RandomBefore&&RandomAfter==x.RandomAfter
            &&RandomWordsConsumed==x.RandomWordsConsumed&&FromX==x.FromX&&FromY==x.FromY&&ToX==x.ToX&&ToY==x.ToY&&MovedFeet==x.MovedFeet;
    }

    public static class OverwatchExecutionValidation
    {
        public const int MaxOffers=128,MaxRiderChoices=128;
        public static void Validate(Snapshot s)
        {
            if(s.OverwatchOffers==null||s.OverwatchRiderChoices==null||s.OverwatchOffers.Length>MaxOffers
                ||s.OverwatchRiderChoices.Length>MaxRiderChoices||s.OverwatchOffers.Any(x=>x==null)||s.OverwatchRiderChoices.Any(x=>x==null))
                throw new ArgumentException("Invalid Overwatch execution collections.");
            if(s.SchemaVersion<Snapshot.OverwatchExecutionSchema) {
                if(s.OverwatchOffers.Length+s.OverwatchRiderChoices.Length!=0)throw new ArgumentException("Overwatch execution requires schema26.");
                return;
            }
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            bool Attack(string id)=>s.RangedAttacks.Any(x=>x.Id==id);
            if((s.OverwatchOffers.Length>0||s.OverwatchRiderChoices.Length>0)&&(s.WorldSchedule==null||s.Encounter==null))
                throw new ArgumentException("Overwatch execution requires the shared tactical calendar.");
            if(s.OverwatchOffers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.OverwatchOffers.Length
                ||s.OverwatchOffers.Count(x=>x.Status==OverwatchOfferStatus.Pending)>1
                ||s.OverwatchOffers.Any(x=>!Actor(x.OwnerId)||!Actor(x.TargetId)||x.CreatedRevision>s.Revision||x.ResolvedRevision>s.Revision
                    ||x.Status==OverwatchOfferStatus.Pending&&!EncounterHistory.InCurrent(s,x.CreatedRevision)
                    ||x.ResolvedRevision!=0&&EncounterHistory.AtRevision(s,x.CreatedRevision)?.Id!=EncounterHistory.AtRevision(s,x.ResolvedRevision)?.Id
                    ||!s.TacticalMoves.Any(m=>m.Id==x.MoveId&&m.Status==TacticalMoveStatus.Completed&&m.ActorId==x.TargetId
                        &&m.ResolvedRevision==x.CreatedRevision)
                    ||!s.OverwatchDesignations.Any(z=>z.Id==x.DesignationId&&z.OwnerId==x.OwnerId&&z.CreatedRevision==x.SourceAppliedRevision)
                    ||x.AttackId!=""&&!Attack(x.AttackId))
                ||s.OverwatchRiderChoices.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.OverwatchRiderChoices.Length
                ||s.OverwatchRiderChoices.Count(x=>x.Status==OverwatchRiderChoiceStatus.Pending)>1
                ||s.OverwatchRiderChoices.Any(x=>!Actor(x.OwnerId)||!Actor(x.TargetId)||x.CreatedRevision>s.Revision||x.ResolvedRevision>s.Revision
                    ||x.Status==OverwatchRiderChoiceStatus.Pending&&!EncounterHistory.InCurrent(s,x.CreatedRevision)
                    ||!s.OverwatchOffers.Any(o=>o.Id==x.OfferId&&o.Status==OverwatchOfferStatus.Accepted&&o.AttackId==x.AttackId
                        &&o.OwnerId==x.OwnerId&&o.TargetId==x.TargetId)
                    ||!Attack(x.AttackId)
                    ||x.Choice==OverwatchRider.Snare&&x.Status==OverwatchRiderChoiceStatus.Resolved
                        &&(s.Encounter==null||x.ExpiresAfterTurnOrdinal<s.Encounter.TurnOrdinal)))
                throw new ArgumentException("Invalid Overwatch execution references.");
        }
    }
}
