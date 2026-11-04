using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public static class CombatProfileIds { public const string OrdinaryUnarmed="TEST_ONLY.ordinary-unarmed"; }
    public enum TacticalMoveKind { Ordinary, Press }
    public enum TacticalMoveStatus { AwaitingReactions, Completed, Interrupted }
    public enum PressOfferStatus { Pending, Accepted, Declined, Invalidated }
    public sealed class ActorTacticalRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public bool ReactionAvailable { get; }
        public int MobileFeet { get; }
        public bool PressConsumed { get; }
        public int DisengageTurn { get; }
        public ActorTacticalRecord(string actor,int lastStart=-1,bool reaction=true,int mobileFeet=0,bool pressConsumed=false,int disengageTurn=-1)
        {
            if(!Validation.ValidId(actor)||lastStart< -1||mobileFeet<0||mobileFeet>5||disengageTurn< -1||disengageTurn>lastStart)throw new ArgumentException("Invalid tactical resource record.");
            ActorId=actor;LastRegularStart=lastStart;ReactionAvailable=reaction;MobileFeet=mobileFeet;PressConsumed=pressConsumed;DisengageTurn=disengageTurn;
        }
        public bool SameAs(ActorTacticalRecord x)=>x!=null&&ActorId==x.ActorId&&LastRegularStart==x.LastRegularStart&&ReactionAvailable==x.ReactionAvailable
            &&MobileFeet==x.MobileFeet&&PressConsumed==x.PressConsumed&&DisengageTurn==x.DisengageTurn;
    }
    /// <summary>One fixed voluntary step and its captured ordinary OA offer list. The response cursor
    /// advances on acceptance/decline; pending damage choices resolve before remaining offers.</summary>
    public sealed class TacticalMoveRecord
    {
        public string Id { get; }
        public long Revision { get; }
        public long ResolvedRevision { get; }
        public int TurnOrdinal { get; }
        public string ActorId { get; }
        public int FromX { get; }
        public int FromY { get; }
        public int ToX { get; }
        public int ToY { get; }
        public TacticalMoveKind Kind { get; }
        public TacticalMoveStatus Status { get; }
        public IReadOnlyList<string> Reactors { get; }
        public int ResponseIndex { get; }
        public long CostPaid { get; }
        public string ParentPressOffer { get; }
        public bool Pending=>Status==TacticalMoveStatus.AwaitingReactions;
        public TacticalMoveRecord(string id,long revision,long resolvedRevision,int ordinal,string actor,int fromX,int fromY,int toX,int toY,
            TacticalMoveKind kind,TacticalMoveStatus status,IEnumerable<string> reactors,int responseIndex=0,long costPaid=0,string parentPressOffer="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(actor)||revision<1||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<revision||ordinal<0
                ||!Enum.IsDefined(typeof(TacticalMoveKind),kind)||!Enum.IsDefined(typeof(TacticalMoveStatus),status)||reactors==null||costPaid<0
                ||parentPressOffer==null||parentPressOffer!=""&&!Validation.ValidId(parentPressOffer))throw new ArgumentException("Invalid movement record.");
            var ids=reactors.ToArray();if(ids.Length>64||ids.Any(x=>!Validation.ValidId(x)||x==actor)||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length
                ||responseIndex<0||responseIndex>ids.Length||(status==TacticalMoveStatus.AwaitingReactions)!=(resolvedRevision==0)
                ||status!=TacticalMoveStatus.Completed&&costPaid!=0||(kind==TacticalMoveKind.Press)!=(parentPressOffer!=""))throw new ArgumentException("Invalid movement continuation.");
            Id=id;Revision=revision;ResolvedRevision=resolvedRevision;TurnOrdinal=ordinal;ActorId=actor;FromX=fromX;FromY=fromY;ToX=toX;ToY=toY;
            Kind=kind;Status=status;Reactors=Array.AsReadOnly(ids);ResponseIndex=responseIndex;CostPaid=costPaid;ParentPressOffer=parentPressOffer;
        }
        public TacticalMoveRecord Progress(int index,TacticalMoveStatus status,long resolved=0,long cost=0)=>new TacticalMoveRecord(Id,Revision,resolved,TurnOrdinal,ActorId,
            FromX,FromY,ToX,ToY,Kind,status,Reactors,index,cost,ParentPressOffer);
        public bool SameAs(TacticalMoveRecord x)=>x!=null&&Id==x.Id&&Revision==x.Revision&&ResolvedRevision==x.ResolvedRevision&&TurnOrdinal==x.TurnOrdinal&&ActorId==x.ActorId
            &&FromX==x.FromX&&FromY==x.FromY&&ToX==x.ToX&&ToY==x.ToY&&Kind==x.Kind&&Status==x.Status&&Reactors.SequenceEqual(x.Reactors)
            &&ResponseIndex==x.ResponseIndex&&CostPaid==x.CostPaid&&ParentPressOffer==x.ParentPressOffer;
    }
    public sealed class PressOfferRecord
    {
        public string Id { get; }
        public string MoveId { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public long CreatedRevision { get; }
        public long ArmedRevision { get; }
        public long ResolvedRevision { get; }
        public PressOfferStatus Status { get; }
        public PressOfferRecord(string id,string moveId,string actor,string target,long created,long armed,PressOfferStatus status=PressOfferStatus.Pending,long resolved=0)
        {
            if(new[]{id,moveId,actor,target}.Any(x=>!Validation.ValidId(x))||actor==target||created<1||armed<1||armed>created||resolved<0||resolved!=0&&resolved<created
                ||!Enum.IsDefined(typeof(PressOfferStatus),status)||(status==PressOfferStatus.Pending)!=(resolved==0))throw new ArgumentException("Invalid Press offer.");
            Id=id;MoveId=moveId;ActorId=actor;TargetId=target;CreatedRevision=created;ArmedRevision=armed;Status=status;ResolvedRevision=resolved;
        }
        public PressOfferRecord Resolve(PressOfferStatus status,long revision)=>new PressOfferRecord(Id,MoveId,ActorId,TargetId,CreatedRevision,ArmedRevision,status,revision);
        public bool SameAs(PressOfferRecord x)=>x!=null&&Id==x.Id&&MoveId==x.MoveId&&ActorId==x.ActorId&&TargetId==x.TargetId&&CreatedRevision==x.CreatedRevision
            &&ArmedRevision==x.ArmedRevision&&ResolvedRevision==x.ResolvedRevision&&Status==x.Status;
    }
    public static class TacticalMovementValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.TacticalActors==null||s.TacticalMoves==null||s.PressOffers==null||s.TacticalActors.Length>64||s.TacticalMoves.Length>64||s.PressOffers.Length>128
                ||s.TacticalActors.Any(x=>x==null)||s.TacticalMoves.Any(x=>x==null)||s.PressOffers.Any(x=>x==null))throw new ArgumentException("Invalid tactical collections.");
            if(s.SchemaVersion<Snapshot.TacticalMovementSchema){if(s.TacticalActors.Length+s.TacticalMoves.Length+s.PressOffers.Length!=0||s.MeleeAttacks.Any(a=>a.Opportunity||a.PressInstruction!=PressHitInstruction.ArmOrReplace))throw new ArgumentException("Tactical continuations require schema11.");return;}
            bool Actor(string id)=>s.Actors.Any(a=>a.Id==id);
            if(!s.Actors.Select(a=>a.Id).OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(s.TacticalActors.Select(a=>a.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||s.TacticalMoves.Select(m=>m.Id).Distinct(StringComparer.Ordinal).Count()!=s.TacticalMoves.Length||s.TacticalMoves.Count(m=>m.Pending)>1
                ||s.PressOffers.Select(p=>p.Id).Distinct(StringComparer.Ordinal).Count()!=s.PressOffers.Length
                ||s.TacticalActors.Any(a=>a.LastRegularStart>=0&&(s.Encounter==null||a.LastRegularStart>s.Encounter.TurnOrdinal||s.Encounter.Order[a.LastRegularStart%s.Encounter.Order.Count]!=a.ActorId))
                ||s.TacticalMoves.Any(m=>!Actor(m.ActorId)||m.Reactors.Any(id=>!Actor(id))||m.Revision>s.Revision||m.ResolvedRevision>s.Revision
                    ||s.Encounter==null||m.TurnOrdinal>s.Encounter.TurnOrdinal||m.ParentPressOffer!=""&&!s.PressOffers.Any(p=>p.Id==m.ParentPressOffer&&p.Status==PressOfferStatus.Accepted))
                ||s.PressOffers.Any(p=>!Actor(p.ActorId)||!Actor(p.TargetId)||p.CreatedRevision>s.Revision||p.ResolvedRevision>s.Revision||!s.TacticalMoves.Any(m=>m.Id==p.MoveId&&m.Status==TacticalMoveStatus.Completed)))
                throw new ArgumentException("Invalid tactical references.");
        }
    }
}
