#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Schema32 execution of the source-approved Soldier Command Step passive. The offer
    /// points to the paid action receipt; the ally's response and separate five-foot movement are
    /// persisted in the existing command and tactical-movement ledgers.</summary>
    public sealed partial class TestOnlySharedWorldPolicy
    {
        internal static CommandStepOfferRecord PendingCommandStepOffer(Snapshot s)
            =>s.CommandStepOffers.SingleOrDefault(x=>x.Status==CommandStepOfferStatus.Pending);

        private static bool CommandStepAction(CommandKind kind)
            =>kind==CommandKind.AttackClub||kind==CommandKind.AttackUnarmed||kind==CommandKind.AttackRepeatingCrossbow||kind==CommandKind.ReloadRepeatingCrossbow
                ||kind==CommandKind.WarningShot||kind==CommandKind.CoveringFire||kind==CommandKind.DoffPortableShield
                ||kind==CommandKind.Disengage||kind==CommandKind.EncounterDash||kind==CommandKind.HandleInventory
                ||kind==CommandKind.HandleVessel||kind==CommandKind.HandlePortableEquipment||kind==CommandKind.EquipPortableItem
                ||kind==CommandKind.RemovePortableItem||kind==CommandKind.OpenPortableContainer||kind==CommandKind.ClosePortableContainer
                ||kind==CommandKind.CurePeriodicRider;

        private static Command CommandStepActionReceipt(Snapshot s,string actionId,string actor,int turnOrdinal,string turnId)
        {
            var receipt=s.Receipts.SingleOrDefault(x=>x.Id==actionId);
            if(receipt==null||receipt.Revision>s.Revision)return null;
            Command action;
            try{action=CommandHistory.Read(receipt);}catch(ArgumentException){return null;}
            if(action.Actor!=actor||!CommandStepAction(action.Kind))return null;
            var encounter=EncounterHistory.AtRevision(s,receipt.Revision);
            if(encounter==null||!EncounterHistory.MatchesTurn(encounter,turnOrdinal,actor)
                ||encounter.Id+".turn."+turnOrdinal.ToString(CultureInfo.InvariantCulture)!=turnId)return null;
            long start=0,nextStart=long.MaxValue;
            for(int i=0;i<encounter.StartRevisions.Count;i++) {
                int ordinal=encounter.ObservedOrdinals[i];
                if(encounter.Order[ordinal%encounter.Order.Count]!=actor)continue;
                if(ordinal==turnOrdinal)start=Math.Max(start,encounter.StartRevisions[i]);
                else if(ordinal>turnOrdinal)nextStart=Math.Min(nextStart,encounter.StartRevisions[i]);
            }
            if(start==0||receipt.Revision<start||receipt.Revision>=nextStart)return null;
            string recordedTurn=action.Combat?.TurnId??action.Ranged?.TurnId;
            if(!string.IsNullOrEmpty(recordedTurn)&&recordedTurn!=turnId)return null;
            return action;
        }

        private string AssessCommandStepOffer(Snapshot s,Command c,out string actionId)
        {
            actionId="";
            if(s.SchemaVersion<Snapshot.CommandStepSchema)return "CommandStepNotImplemented";
            if(c.Kind!=CommandKind.OfferCommandStep||c.Inventory!=null||c.Advancement!=null||c.Ranged!=null||c.Combat==null
                ||c.X!=0||c.Y!=0||c.Combat.Stance!=0||c.Combat.Choice||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||c.Combat.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidCommandStepOffer";
            if(!s.InventoryCombat||s.Encounter==null)return "CommandStepRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Combat.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterFeatureIds.CommandStep
                &&x.ClassName=="Soldier"&&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))return "FeatureNotOwned";
            if(!TestOnlyClubAttackPolicy.ActionSpent(s))return "CommandStepRequiresCompletedAction";
            if(CommandStepActionReceipt(s,c.Combat.WeaponId,c.Actor,s.Encounter.TurnOrdinal,s.Encounter.CurrentTurnId)==null)
                return "CommandStepActionReceiptUnavailable";
            if(!s.TacticalAllies.Any(x=>x.Includes(c.Actor)&&x.Includes(c.Target))||c.Target==c.Actor
                ||!s.WorldSchedule.Order.Contains(c.Target))return "CommandStepTargetMustBeAlly";
            var source=s.Actors.Single(a=>a.Id==c.Actor);var ally=s.Actors.Single(a=>a.Id==c.Target);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(source.X,source.Y),new CombatCell(ally.X,ally.Y))!=5)
                return "CommandStepAllyMustBeAdjacent";
            int round=s.Encounter.TurnOrdinal/s.Encounter.Order.Count;
            if(s.CommandStepOffers.Any(x=>x.SoldierActorId==c.Actor&&x.RoundOrdinal==round&&x.Status==CommandStepOfferStatus.Accepted))
                return "CommandStepAlreadyUsedThisRound";
            if(s.CommandStepOffers.Length>=128)return "CommandStepHistoryCapacityReached";
            if(PendingCommandStepOffer(s)!=null)return "CommandStepChoicePending";
            actionId=c.Combat.WeaponId;return null;
        }

        private string AssessCommandStepResponse(Snapshot s,Command c,out CommandStepOfferRecord offer)
        {
            offer=PendingCommandStepOffer(s);
            if(s.SchemaVersion<Snapshot.CommandStepSchema)return "CommandStepNotImplemented";
            if(c.Kind!=CommandKind.RespondCommandStep||c.Inventory!=null||c.Advancement!=null||c.Ranged!=null||c.Combat==null
                ||c.Combat.WeaponId!=""||c.Combat.Stance!=0||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||c.Combat.PressInstruction!=PressHitInstruction.ArmOrReplace)
                return "InvalidCommandStepResponse";
            if(!s.InventoryCombat||s.Encounter==null)return "CommandStepRequiresEncounter";
            if(offer==null)return "NoPendingCommandStepChoice";
            if(c.Target!=offer.Id||c.Actor!=offer.AllyActorId||c.Combat.TurnId!=s.Encounter.CurrentTurnId
                ||offer.TurnId!=s.Encounter.CurrentTurnId||offer.TurnOrdinal!=s.Encounter.TurnOrdinal)return "WrongCommandStepResponder";
            if(!c.Combat.Choice&&(c.X!=0||c.Y!=0))return "InvalidCommandStepDecline";
            if(c.Combat.Choice) {
                string allyId=offer.AllyActorId,soldierId=offer.SoldierActorId;int round=offer.RoundOrdinal;
                var body=s.Actors.Single(x=>x.Id==allyId);
                string failure=bodies.CommandStepDestinationFailure(s,offer,body.X,body.Y,c.X,c.Y);
                if(failure!=null)return failure;
                if(s.CommandStepOffers.Any(x=>x.SoldierActorId==soldierId&&x.RoundOrdinal==round
                    &&x.Status==CommandStepOfferStatus.Accepted))return "CommandStepAlreadyUsedThisRound";
            }
            return null;
        }

        internal string ResolveCommandStepOffer(Snapshot s,Command c)
        {
            string failure=AssessCommandStepOffer(s,c,out string actionId);if(failure!=null)return failure;
            int ordinal=s.Encounter.TurnOrdinal,round=ordinal/s.Encounter.Order.Count;
            var offer=new CommandStepOfferRecord(c.Id,actionId,s.Encounter.CurrentTurnId,c.Actor,c.Target,ordinal,round,s.Revision+1);
            s.CommandStepOffers=s.CommandStepOffers.Concat(new[]{offer}).ToArray();return null;
        }

        internal string ResolveCommandStepResponse(Snapshot s,Command c)
        {
            string failure=AssessCommandStepResponse(s,c,out var offer);if(failure!=null)return failure;
            if(!c.Combat.Choice) {
                s.CommandStepOffers=s.CommandStepOffers.Select(x=>x.Id==offer.Id
                    ?x.Resolve(CommandStepOfferStatus.Declined,s.Revision+1,c.Id):x).ToArray();return null;
            }
            string moveId="move."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            var accepted=offer.Resolve(CommandStepOfferStatus.Accepted,s.Revision+1,c.Id,moveId);
            s.CommandStepOffers=s.CommandStepOffers.Select(x=>x.Id==offer.Id?accepted:x).ToArray();
            string movement=bodies.BeginCommandStep(s,accepted,c.X,c.Y);if(movement!=null)return movement;
            string overwatch=QueueCompletedMovementOverwatch(s);if(overwatch!=null)return overwatch;
            NormalizePendingOverwatchOffers(s);return null;
        }
    }
}
#endif
