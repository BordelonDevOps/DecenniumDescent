using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class PostRecoveryProfile
    {
        // Event ownership is revision-sensitive. Retained effect endpoints use their original
        // epoch separately; a superseded epoch can never produce a new current-turn payment.
        public static bool OwnsEvent(Snapshot s,string actor,string epoch,long revision)
        {
            var ferry=s.FerryWraith?.Entered;
            if(FerryWraithProfile.IsParticipant(actor)&&ferry!=null&&revision>ferry.Revision)
                return epoch==FerryWraithProfile.Calendar;
            if(epoch==FerryWraithProfile.Calendar)return false;
            var entry=s.PostRecoveryEncounter?.Entered;
            if(entry==null)return epoch!=PostRecoveryEncounterDefinition.Calendar;
            if(!PostRecoveryEncounterDefinition.IsParticipant(actor))return true;
            return revision>entry.Revision ? epoch==PostRecoveryEncounterDefinition.Calendar
                :epoch!=PostRecoveryEncounterDefinition.Calendar;
        }

        internal static void Validate(Snapshot s)
        {
            var record=s.PostRecoveryEncounter;
            if((record!=null)!=SelectedFingerprint(s.ContentFingerprint))throw new ArgumentException("Invalid post-recovery envelope selection.");
            if(record==null)return;
            const string npc=PostRecoveryEncounterDefinition.Actor, clubId=PostRecoveryEncounterDefinition.Club;
            var actor=s.Actors.SingleOrDefault(x=>x.Id==npc);
            var character=s.Characters.SingleOrDefault(x=>x.ActorId==npc);
            var life=s.Lives.SingleOrDefault(x=>x.ActorId==npc);
            var club=s.Clubs.SingleOrDefault(x=>x.Id==clubId);
            if(!s.TestOnly || s.SchemaVersion!=Snapshot.SurpriseEntrySchema || !s.ConnectedClericLongRest
                || actor==null || character==null || character.ProfileId!="TEST_ONLY.numeric-warrior3"
                || character.Abilities.Any(x=>x!=10) || character.Levels.Any(x=>x.ClassName!="Warrior")
                || !character.Levels.Select(x=>x.BaseHp).SequenceEqual(new[]{12,7,7})
                || life==null || life.MaximumHp!=26 || club==null || club.ProfileId!="TEST_ONLY.standard-club" || club.OwnerId!=npc || club.CustodianId!=npc
                || s.WorldSchedule.Order.Contains(npc) || s.LaterEncounter==null
                || s.LaterEncounter.Definition.DefenderId==npc || s.CharacterAdvancements.Any(x=>x.ActorId==npc)
                || s.ActorMovement.Single(x=>x.ActorId==npc).BaseWalkingSpeed!=30)
                throw new ArgumentException("Invalid post-recovery initial actor or source scope.");
            foreach(var contact in record.Contacts) {
                var approach=Receipt(s,contact.ApproachRevision);
                var arrival=Receipt(s,contact.Revision);
                if(approach.Kind!=CommandKind.BeginWorldStep || approach.Actor!=PostRecoveryEncounterDefinition.Hero
                    || approach.Target!="walk" || approach.X!=0 || approach.Y!=1
                    || arrival.Kind!=CommandKind.AdvanceClock || arrival.Id!=contact.CommandId
                    || contact.At>s.RuleClock || contact.Revision>s.Revision)
                    throw new ArgumentException("Invalid post-recovery completed-contact provenance.");
            }
            var admission=record.Admission;
            var closed=s.ClosedEncounters.SingleOrDefault(x=>x.Encounter.Id==PostRecoveryEncounterDefinition.Encounter);
            if(admission==null) {
                if(actor.X!=4 || actor.Y!=4 || life.Hp!=26 || life.Dead || life.Prone || life.TemporaryHp!=0
                    || club.HeldBy!=npc || closed!=null || s.Encounter?.Id==PostRecoveryEncounterDefinition.Encounter
                    || s.WorldIntervals.Any(x=>x.ActorId==npc) || s.WorldActivityIntervals.Count(x=>x.ActorId==npc)!=1)
                    throw new ArgumentException("Premature post-recovery actor or encounter mutation.");
                return;
            }
            var epoch=admission.Epoch;var prior=s.Reinforcement?.Admission?.Phase.Epoch;var entry=record.Entered;
            if(prior==null || admission.PreviousPartyEpochId!=prior.Id || epoch.Origin!=entry.At
                || prior.Start(admission.PriorDefenderLocalStart)!=entry.At
                || prior.LatestStart(PostRecoveryEncounterDefinition.PriorDefender,admission.PriorDefenderLocalStart)!=admission.PriorDefenderLocalStart
                || epoch.ProcessedSlot!=epoch.SlotAt(s.RuleClock) || s.WorldActivityIntervals.Any(x=>x.ActorId==npc)
                || s.ClericInvocationPath==null || s.ClericInvocationPath.AcquiredRevision>=entry.Revision
                || !s.ClericLongRestSettlements.Any(x=>x.Benefit==ClericLongRestBenefit.Eligible && x.Revision<entry.Revision)
                || !s.ClosedEncounters.Any(x=>x.Encounter.Id==s.ClericMilestone.LaterEncounterId && x.ClosedRevision<entry.Revision)
                || !s.Lives.Single(x=>x.ActorId==PostRecoveryEncounterDefinition.PriorDefender).Dead)
                throw new ArgumentException("Post-recovery admission lacks settled earned recovery and exact old Start.");
            var activity=admission.DefenderActivity;
            long index=WorldActivityIntervalRecord.IndexAt(s.WorldSchedule,entry.At);
            if(activity.CalendarId!=s.WorldSchedule.Id || activity.IntervalIndex!=index
                && (activity.IntervalIndex!=index-1 || WorldActivityIntervalRecord.EndAt(s.WorldSchedule,activity.IntervalIndex)!=entry.At))
                throw new ArgumentException("Post-recovery defender has no actual admission-time activity interval.");
            foreach(var carry in admission.PartyCarried) {
                long local=prior.LatestStart(carry.Interval.ActorId,admission.PriorDefenderLocalStart);
                if(local<0 || prior.Start(local+1)>entry.At
                    || carry.Interval.LastStart!=WorldTiming.TurnOrdinal(s,prior.Id,local))
                    throw new ArgumentException("Post-recovery party allowance came from an unfinished or invented old interval.");
                if(carry.Interval.ActorId==ClericRpProfile.Actor
                    && s.CastingActivities.Any(x=>x.Turn.EpochId==prior.Id && x.Turn.LocalStart==local)
                    && !s.CastingTurnEnds.Any(x=>x.Turn.EpochId==prior.Id && x.Turn.LocalStart==local
                        && x.At==prior.Start(local+1) && x.Revision<=entry.Revision))
                    throw new ArgumentException("Post-recovery admission bypassed an eligible old casting End.");
            }
            foreach(var draw in admission.Draws) {
                var die=DiceStream.Draw(draw.RandomBefore,20);
                if(draw.Natural!=die.Value+1 || draw.RandomAfter!=die.NextState || draw.WordsConsumed!=die.WordsConsumed)
                    throw new ArgumentException("Post-recovery initiative differs from its actual RNG words.");
            }
            var encounter=Active(s)?s.Encounter:closed?.Encounter;
            if(encounter==null || encounter.Id!=PostRecoveryEncounterDefinition.Encounter || encounter.Origin!=epoch.Origin
                || encounter.RosterPhase!=null || encounter.InheritedPhase!=null || !encounter.InitialOrder.SequenceEqual(epoch.Order)
                || encounter.StartRevisions[0]!=entry.Revision || encounter.ObservedOrdinals[0]!=0
                || Active(s) && (closed!=null || !s.InventoryCombat || encounter.TurnOrdinal!=epoch.ProcessedSlot)
                || !Active(s) && (closed==null || !FerryWraithProfile.Active(s) && (s.InventoryCombat || s.Encounter!=null)))
                throw new ArgumentException("Invalid independent post-recovery encounter history.");
            if(closed!=null) {
                var cause=Receipt(s,closed.ClosedRevision);
                if(!life.Dead || cause.Kind!=CommandKind.EndFixedEncounter || cause.Id!=closed.Reason
                    || cause.Actor!=encounter.CurrentActor || cause.Target!=encounter.CurrentTurnId
                    || closed.ClosedAt!=epoch.Start(encounter.TurnOrdinal+1) || closed.ClosedAt>s.RuleClock)
                    throw new ArgumentException("Invalid post-recovery death and outgoing-End closure.");
            }
            if(s.CastingActivities.Any(x=>!OwnsEvent(s,x.Turn.ActorId,x.Turn.EpochId,x.Revision))
                || s.CastingTurnEnds.Any(x=>x.At>entry.At && !OwnsEvent(s,x.Turn.ActorId,x.Turn.EpochId,x.Revision))
                || s.RadianceUses.Any(x=>!OwnsEvent(s,x.ActorId,x.EpochId,x.Revision)))
                throw new ArgumentException("Superseded party epoch produced current casting or Radiance activity.");
        }

        private static Command Receipt(Snapshot s,long revision)
        {
            var row=s.Receipts.SingleOrDefault(x=>x.Revision==revision);
            return row==null?throw new ArgumentException("Missing post-recovery command receipt."):CommandHistory.Read(row);
        }
    }
}
