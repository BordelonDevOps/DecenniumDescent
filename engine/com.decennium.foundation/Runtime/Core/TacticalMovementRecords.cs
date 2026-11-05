using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public static class CombatProfileIds { public const string OrdinaryUnarmed="TEST_ONLY.ordinary-unarmed"; }
    public enum TacticalMoveKind { Ordinary, Press, TacticalReposition, CommandStep, DefensiveFormationShift }
    public enum TacticalMoveStatus { AwaitingReactions, Completed, Interrupted }
    public enum PressOfferStatus { Pending, Accepted, Declined, Invalidated }
    public enum CommandStepOfferStatus { Pending, Accepted, Declined }
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
        public string ParentCommandStepOffer { get; }
        public string ParentDefensiveFormationId { get; }
        public bool Pending=>Status==TacticalMoveStatus.AwaitingReactions;
        public TacticalMoveRecord(string id,long revision,long resolvedRevision,int ordinal,string actor,int fromX,int fromY,int toX,int toY,
            TacticalMoveKind kind,TacticalMoveStatus status,IEnumerable<string> reactors,int responseIndex=0,long costPaid=0,string parentPressOffer="",
            string parentCommandStepOffer="",string parentDefensiveFormationId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(actor)||revision<1||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<revision||ordinal<0
                ||!Enum.IsDefined(typeof(TacticalMoveKind),kind)||!Enum.IsDefined(typeof(TacticalMoveStatus),status)||reactors==null||costPaid<0
                ||parentPressOffer==null||parentPressOffer!=""&&!Validation.ValidId(parentPressOffer)
                ||parentCommandStepOffer==null||parentCommandStepOffer!=""&&!Validation.ValidId(parentCommandStepOffer)
                ||parentDefensiveFormationId==null||parentDefensiveFormationId!=""&&!Validation.ValidId(parentDefensiveFormationId))throw new ArgumentException("Invalid movement record.");
            var ids=reactors.ToArray();if(ids.Length>64||ids.Any(x=>!Validation.ValidId(x)||x==actor)||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length
                ||responseIndex<0||responseIndex>ids.Length||(status==TacticalMoveStatus.AwaitingReactions)!=(resolvedRevision==0)
                ||status!=TacticalMoveStatus.Completed&&costPaid!=0||(kind==TacticalMoveKind.Press)!=(parentPressOffer!="")
                ||(kind==TacticalMoveKind.CommandStep)!=(parentCommandStepOffer!="")||kind==TacticalMoveKind.Press&&parentCommandStepOffer!=""
                ||kind==TacticalMoveKind.CommandStep&&parentPressOffer!=""
                ||(kind==TacticalMoveKind.DefensiveFormationShift)!=(parentDefensiveFormationId!="")
                ||kind==TacticalMoveKind.DefensiveFormationShift&&(parentPressOffer!=""||parentCommandStepOffer!=""))throw new ArgumentException("Invalid movement continuation.");
            Id=id;Revision=revision;ResolvedRevision=resolvedRevision;TurnOrdinal=ordinal;ActorId=actor;FromX=fromX;FromY=fromY;ToX=toX;ToY=toY;
            Kind=kind;Status=status;Reactors=Array.AsReadOnly(ids);ResponseIndex=responseIndex;CostPaid=costPaid;ParentPressOffer=parentPressOffer;
            ParentCommandStepOffer=parentCommandStepOffer;ParentDefensiveFormationId=parentDefensiveFormationId;
        }
        public TacticalMoveRecord Progress(int index,TacticalMoveStatus status,long resolved=0,long cost=0)=>new TacticalMoveRecord(Id,Revision,resolved,TurnOrdinal,ActorId,
            FromX,FromY,ToX,ToY,Kind,status,Reactors,index,cost,ParentPressOffer,ParentCommandStepOffer,ParentDefensiveFormationId);
        public bool SameAs(TacticalMoveRecord x)=>x!=null&&Id==x.Id&&Revision==x.Revision&&ResolvedRevision==x.ResolvedRevision&&TurnOrdinal==x.TurnOrdinal&&ActorId==x.ActorId
            &&FromX==x.FromX&&FromY==x.FromY&&ToX==x.ToX&&ToY==x.ToY&&Kind==x.Kind&&Status==x.Status&&Reactors.SequenceEqual(x.Reactors)
            &&ResponseIndex==x.ResponseIndex&&CostPaid==x.CostPaid&&ParentPressOffer==x.ParentPressOffer&&ParentCommandStepOffer==x.ParentCommandStepOffer
            &&ParentDefensiveFormationId==x.ParentDefensiveFormationId;
    }
    /// <summary>One source-action-linked Command Step offer and the ally's persisted response.</summary>
    public sealed class CommandStepOfferRecord
    {
        public string Id { get; }
        public string ActionId { get; }
        public string TurnId { get; }
        public string SoldierActorId { get; }
        public string AllyActorId { get; }
        public int TurnOrdinal { get; }
        public int RoundOrdinal { get; }
        public long CreatedRevision { get; }
        public long ResolvedRevision { get; }
        public CommandStepOfferStatus Status { get; }
        public string ResolutionId { get; }
        public string MoveId { get; }
        public bool Pending=>Status==CommandStepOfferStatus.Pending;
        public CommandStepOfferRecord(string id,string actionId,string turnId,string soldierActorId,string allyActorId,int turnOrdinal,int roundOrdinal,
            long createdRevision,CommandStepOfferStatus status=CommandStepOfferStatus.Pending,long resolvedRevision=0,string resolutionId="",string moveId="")
        {
            if(new[]{id,actionId,turnId,soldierActorId,allyActorId}.Any(x=>!Validation.ValidId(x))||soldierActorId==allyActorId
                ||turnOrdinal<0||roundOrdinal<0||createdRevision<1||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<createdRevision
                ||!Enum.IsDefined(typeof(CommandStepOfferStatus),status)||(status==CommandStepOfferStatus.Pending)!=(resolvedRevision==0)
                ||status==CommandStepOfferStatus.Pending&&(resolutionId!=""||moveId!="")
                ||status==CommandStepOfferStatus.Accepted&&(!Validation.ValidId(resolutionId)||!Validation.ValidId(moveId))
                ||status==CommandStepOfferStatus.Declined&&(!Validation.ValidId(resolutionId)||moveId!=""))
                throw new ArgumentException("Invalid Command Step offer record.");
            Id=id;ActionId=actionId;TurnId=turnId;SoldierActorId=soldierActorId;AllyActorId=allyActorId;TurnOrdinal=turnOrdinal;
            RoundOrdinal=roundOrdinal;CreatedRevision=createdRevision;Status=status;ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;MoveId=moveId;
        }
        public CommandStepOfferRecord Resolve(CommandStepOfferStatus status,long revision,string resolutionId,string moveId="")
        {
            if(Status!=CommandStepOfferStatus.Pending||status==CommandStepOfferStatus.Pending)throw new ArgumentException("Command Step offer is already resolved.");
            return new CommandStepOfferRecord(Id,ActionId,TurnId,SoldierActorId,AllyActorId,TurnOrdinal,RoundOrdinal,CreatedRevision,status,revision,resolutionId,moveId);
        }
        public bool SameAs(CommandStepOfferRecord x)=>x!=null&&Id==x.Id&&ActionId==x.ActionId&&TurnId==x.TurnId&&SoldierActorId==x.SoldierActorId
            &&AllyActorId==x.AllyActorId&&TurnOrdinal==x.TurnOrdinal&&RoundOrdinal==x.RoundOrdinal&&CreatedRevision==x.CreatedRevision
            &&ResolvedRevision==x.ResolvedRevision&&Status==x.Status&&ResolutionId==x.ResolutionId&&MoveId==x.MoveId;
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
        private static bool CommandStepAction(CommandKind kind)
            =>kind==CommandKind.AttackClub||kind==CommandKind.AttackUnarmed||kind==CommandKind.AttackRepeatingCrossbow||kind==CommandKind.ReloadRepeatingCrossbow
                ||kind==CommandKind.WarningShot||kind==CommandKind.CoveringFire||kind==CommandKind.DoffPortableShield
                ||kind==CommandKind.Disengage||kind==CommandKind.EncounterDash||kind==CommandKind.HandleInventory
                ||kind==CommandKind.HandleVessel||kind==CommandKind.HandlePortableEquipment||kind==CommandKind.EquipPortableItem
                ||kind==CommandKind.RemovePortableItem||kind==CommandKind.OpenPortableContainer||kind==CommandKind.ClosePortableContainer
                ||kind==CommandKind.CurePeriodicRider;
        private static bool ValidCommandStepOffer(Snapshot s,CommandStepOfferRecord offer)
        {
            if(s.SchemaVersion<Snapshot.CommandStepSchema||!s.CharacterFeatureGrants.Any(x=>x.ActorId==offer.SoldierActorId
                &&x.FeatureId==CharacterFeatureIds.CommandStep&&x.ClassName=="Soldier"&&x.ClassLevel==3
                &&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))return false;
            var created=EncounterHistory.AtRevision(s,offer.CreatedRevision);
            if(created==null||!EncounterHistory.MatchesTurn(created,offer.TurnOrdinal,offer.SoldierActorId)
                ||offer.RoundOrdinal!=offer.TurnOrdinal/created.Order.Count
                ||offer.TurnId!=created.Id+".turn."+offer.TurnOrdinal.ToString(CultureInfo.InvariantCulture))return false;
            long ownStart=0,nextOwnStart=long.MaxValue;
            for(int i=0;i<created.StartRevisions.Count;i++) {
                int ordinal=created.ObservedOrdinals[i];if(created.Order[ordinal%created.Order.Count]!=offer.SoldierActorId)continue;
                if(ordinal==offer.TurnOrdinal)ownStart=Math.Max(ownStart,created.StartRevisions[i]);
                else if(ordinal>offer.TurnOrdinal)nextOwnStart=Math.Min(nextOwnStart,created.StartRevisions[i]);
            }
            if(ownStart==0||offer.CreatedRevision<ownStart||offer.CreatedRevision>=nextOwnStart)return false;
            var offerReceipt=s.Receipts.SingleOrDefault(x=>x.Id==offer.Id&&x.Revision==offer.CreatedRevision);
            var actionReceipt=s.Receipts.SingleOrDefault(x=>x.Id==offer.ActionId&&x.Revision<offer.CreatedRevision);
            if(offerReceipt==null||actionReceipt==null)return false;
            Command offered,action;
            try{offered=CommandHistory.Read(offerReceipt);action=CommandHistory.Read(actionReceipt);}
            catch(ArgumentException){return false;}
            if(offered.Kind!=CommandKind.OfferCommandStep||offered.Actor!=offer.SoldierActorId||offered.Target!=offer.AllyActorId
                ||offered.Combat?.TurnId!=offer.TurnId||offered.Combat.WeaponId!=offer.ActionId||action.Actor!=offer.SoldierActorId
                ||!CommandStepAction(action.Kind))return false;
            var actionEncounter=EncounterHistory.AtRevision(s,actionReceipt.Revision);
            if(actionEncounter==null||actionEncounter.Id!=created.Id||!EncounterHistory.MatchesTurn(actionEncounter,offer.TurnOrdinal,offer.SoldierActorId)
                ||actionReceipt.Revision<ownStart||actionReceipt.Revision>=nextOwnStart)return false;
            string actionTurn=action.Combat?.TurnId??action.Ranged?.TurnId;
            if(!string.IsNullOrEmpty(actionTurn)&&actionTurn!=offer.TurnId)return false;
            if(offer.Status==CommandStepOfferStatus.Pending)return true;
            var responseReceipt=s.Receipts.SingleOrDefault(x=>x.Id==offer.ResolutionId&&x.Revision==offer.ResolvedRevision);
            if(responseReceipt==null)return false;
            Command response;
            try{response=CommandHistory.Read(responseReceipt);}catch(ArgumentException){return false;}
            if(response.Kind!=CommandKind.RespondCommandStep||response.Actor!=offer.AllyActorId||response.Target!=offer.Id
                ||response.Combat?.TurnId!=offer.TurnId||response.Combat.Choice!=(offer.Status==CommandStepOfferStatus.Accepted))return false;
            if(offer.Status==CommandStepOfferStatus.Declined)return response.X==0&&response.Y==0&&offer.MoveId=="";
            var moved=s.TacticalMoves.SingleOrDefault(x=>x.Id==offer.MoveId);
            return moved!=null&&moved.Kind==TacticalMoveKind.CommandStep&&moved.ActorId==offer.AllyActorId
                &&moved.TurnOrdinal==offer.TurnOrdinal&&moved.Revision==offer.ResolvedRevision
                &&moved.ToX==response.X&&moved.ToY==response.Y;
        }
        public static void Validate(Snapshot s)
        {
            if(s.TacticalActors==null||s.TacticalMoves==null||s.PressOffers==null||s.CommandStepOffers==null||s.TacticalActors.Length>64||s.TacticalMoves.Length>64
                ||s.PressOffers.Length>128||s.CommandStepOffers.Length>128||s.TacticalActors.Any(x=>x==null)||s.TacticalMoves.Any(x=>x==null)
                ||s.PressOffers.Any(x=>x==null)||s.CommandStepOffers.Any(x=>x==null))throw new ArgumentException("Invalid tactical collections.");
            if(s.SchemaVersion<Snapshot.TacticalMovementSchema){if(s.TacticalActors.Length+s.TacticalMoves.Length+s.PressOffers.Length+s.CommandStepOffers.Length!=0||s.MeleeAttacks.Any(a=>a.Opportunity||a.PressInstruction!=PressHitInstruction.ArmOrReplace))throw new ArgumentException("Tactical continuations require schema11.");return;}
            if(s.SchemaVersion<Snapshot.CommandStepSchema&&s.CommandStepOffers.Length!=0)throw new ArgumentException("Command Step requires schema32.");
            if(s.SchemaVersion<Snapshot.CommandStepSchema&&s.TacticalMoves.Any(x=>x.Kind==TacticalMoveKind.CommandStep))
                throw new ArgumentException("Command Step movement requires schema32.");
            if(s.SchemaVersion<Snapshot.DefensiveFormationSchema&&s.TacticalMoves.Any(x=>x.Kind==TacticalMoveKind.DefensiveFormationShift))
                throw new ArgumentException("Defensive Formation movement requires schema34.");
            bool Actor(string id)=>s.Actors.Any(a=>a.Id==id);
            if(!s.Actors.Select(a=>a.Id).OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(s.TacticalActors.Select(a=>a.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||s.TacticalMoves.Select(m=>m.Id).Distinct(StringComparer.Ordinal).Count()!=s.TacticalMoves.Length||s.TacticalMoves.Count(m=>m.Pending)>1
                ||s.PressOffers.Select(p=>p.Id).Distinct(StringComparer.Ordinal).Count()!=s.PressOffers.Length
                ||s.TacticalActors.Any(a=>a.LastRegularStart>=0&&(s.SchemaVersion>=Snapshot.SharedWorldSchema?a.LastRegularStart!=EncounterHistory.LatestStartOrdinal(s,a.ActorId)
                    :!EncounterHistory.MatchesTurn(s.Encounter,a.LastRegularStart,a.ActorId)))
                ||s.TacticalMoves.Any(m=>!Actor(m.ActorId)||m.Reactors.Any(id=>!Actor(id))||m.Revision>s.Revision||m.ResolvedRevision>s.Revision
                    ||EncounterHistory.AtRevision(s,m.Revision)==null||m.TurnOrdinal>EncounterHistory.AtRevision(s,m.Revision).TurnOrdinal
                    ||m.Pending&&!EncounterHistory.InCurrent(s,m.Revision)||m.ResolvedRevision!=0&&EncounterHistory.AtRevision(s,m.Revision)?.Id!=EncounterHistory.AtRevision(s,m.ResolvedRevision)?.Id
                    ||m.ParentPressOffer!=""&&!s.PressOffers.Any(p=>p.Id==m.ParentPressOffer&&p.Status==PressOfferStatus.Accepted
                        &&EncounterHistory.AtRevision(s,p.CreatedRevision)?.Id==EncounterHistory.AtRevision(s,m.Revision)?.Id)
                    ||m.ParentCommandStepOffer!=""&&!s.CommandStepOffers.Any(p=>p.Id==m.ParentCommandStepOffer&&p.Status==CommandStepOfferStatus.Accepted&&p.MoveId==m.Id
                        &&EncounterHistory.AtRevision(s,p.CreatedRevision)?.Id==EncounterHistory.AtRevision(s,m.Revision)?.Id)
                    ||m.ParentDefensiveFormationId!=""&&!s.DefensiveFormations.Any(f=>f.Id==m.ParentDefensiveFormationId
                        &&f.Shifts.Any(x=>x.MoveId==m.Id&&x.RecipientActorId==m.ActorId
                            &&(x.Status==DefensiveFormationShiftStatus.Moving||x.Status==DefensiveFormationShiftStatus.Moved
                                ||x.Status==DefensiveFormationShiftStatus.Skipped))))
                ||s.PressOffers.Any(p=>!Actor(p.ActorId)||!Actor(p.TargetId)||p.CreatedRevision>s.Revision||p.ResolvedRevision>s.Revision
                    ||p.Status==PressOfferStatus.Pending&&!EncounterHistory.InCurrent(s,p.CreatedRevision)
                    ||p.ResolvedRevision!=0&&EncounterHistory.AtRevision(s,p.CreatedRevision)?.Id!=EncounterHistory.AtRevision(s,p.ResolvedRevision)?.Id
                    ||!s.TacticalMoves.Any(m=>m.Id==p.MoveId&&m.Status==TacticalMoveStatus.Completed
                        &&EncounterHistory.AtRevision(s,m.Revision)?.Id==EncounterHistory.AtRevision(s,p.CreatedRevision)?.Id))
                ||s.CommandStepOffers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.CommandStepOffers.Length
                ||s.CommandStepOffers.Count(x=>x.Pending)>1
                ||s.CommandStepOffers.Any(p=>!Actor(p.SoldierActorId)||!Actor(p.AllyActorId)||p.CreatedRevision>s.Revision||p.ResolvedRevision>s.Revision
                    ||!s.TacticalAllies.Any(a=>a.Includes(p.SoldierActorId)&&a.Includes(p.AllyActorId))
                    ||p.CreatedRevision>0&&EncounterHistory.AtRevision(s,p.CreatedRevision)==null
                    ||p.Pending&&!EncounterHistory.InCurrent(s,p.CreatedRevision)
                    ||p.ResolvedRevision!=0&&EncounterHistory.AtRevision(s,p.CreatedRevision)?.Id!=EncounterHistory.AtRevision(s,p.ResolvedRevision)?.Id
                    ||!ValidCommandStepOffer(s,p)
                    ||p.Status==CommandStepOfferStatus.Accepted&&s.CommandStepOffers.Any(other=>other.Id!=p.Id
                        &&other.Status==CommandStepOfferStatus.Accepted&&other.SoldierActorId==p.SoldierActorId&&other.RoundOrdinal==p.RoundOrdinal)
                    ||p.Status==CommandStepOfferStatus.Accepted&&!s.TacticalMoves.Any(m=>m.Id==p.MoveId&&m.ParentCommandStepOffer==p.Id
                        &&EncounterHistory.AtRevision(s,m.Revision)?.Id==EncounterHistory.AtRevision(s,p.ResolvedRevision)?.Id)))
                throw new ArgumentException("Invalid tactical references.");
        }
    }
}
