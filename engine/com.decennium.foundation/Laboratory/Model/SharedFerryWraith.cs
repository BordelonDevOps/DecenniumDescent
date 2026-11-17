#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private FerryWraithRecord ferryDeclaration;
        internal static string CreatureAttackFailure(Snapshot s,string actor,string feature)
        {
            if(s.FerryWraith==null||actor!=FerryWraithProfile.Actor||feature!=FerryWraithProfile.Feature
                ||!s.Creatures.Any(x=>x.ActorId==actor))return "CreatureAttackSourceUnavailable";
            if(s.FerryWraith.Admission==null)return "FerryWraithHoldsAuthoredPosition";
            if(s.FerryWraith.ClawSuppressed)return "CreatureAttackSourceSuppressed";
            return null;
        }
        internal static bool HasOrdinaryMeleeSource(Snapshot s,string actor)
            =>s.Creatures.Any(x=>x.ActorId==actor)
                ?CreatureAttackFailure(s,actor,FerryWraithProfile.Feature)==null:s.Characters.Any(x=>x.ActorId==actor);
        internal TestOnlySharedWorldPolicy EnableFerryWraith(bool companionConsents=true,bool directorAuthorizes=true)
        {
            if(initializationStarted||ferryDeclaration!=null||declaredGeometry==null||bishopDeclaration==null||observationFixture==null)
                throw new InvalidOperationException("Select the Ferry source once on a fresh qualified-geometry expedition.");
            ferryDeclaration=new FerryWraithRecord(ContentFingerprint,companionConsents,directorAuthorizes);
            bodies.RegisterDeferredConditionTarget(FerryWraithProfile.Actor);
            observationFixture=new ObservationFixture(observationFixture.Width,observationFixture.Height,observationFixture.Cells,
                observationFixture.Profiles.Append(new ObservationSightProfile(FerryWraithProfile.Actor,30,30)));
            ContentFingerprint=FerryWraithProfile.BindFingerprint(ferryDeclaration.PredecessorFingerprint,companionConsents,directorAuthorizes);
            return this;
        }
        private void InitializeFerryActor(Snapshot s)
        {
            if(ferryDeclaration==null)return;
            const string actor=FerryWraithProfile.Actor;
            s.FerryWraith=ferryDeclaration;
            s.Creatures=s.Creatures.Append(FerryWraithProfile.CreateCreature()).ToArray();
            s.Actors=s.Actors.Append(new ActorState{Id=actor,X=10,Y=2}).ToArray();
            s.Lives=s.Lives.Append(ActorLifeRules.Record(actor,new LifeState(9,9,usesDeathSaves:false),false)).ToArray();
            s.ActorMovement=s.ActorMovement.Append(new ActorMovementRecord(actor,40)).ToArray();
            s.TacticalActors=s.TacticalActors.Append(new ActorTacticalRecord(actor)).ToArray();
            s.Conditions=s.Conditions.Append(new ConditionJournal(ConditionHistory.PolicyId,actor,new ConditionStamp(s.RuleClock))).ToArray();
        }
        private void InitializeFerrySource(Snapshot s)
        {
            if(ferryDeclaration==null)return;
            var before=s.Conditions.Single(x=>x.Target==FerryWraithProfile.Actor);
            var immunity=new ConditionImmunityData(FerryWraithProfile.PoisonedImmunity,FerryWraithProfile.Actor,FerryWraithProfile.SourceId,
                new[]{"Poisoned"},null,"source-profile-only");
            var after=ConditionHistory.Restore(before).Append(ConditionOperation.Grant(FerryWraithProfile.PoisonedImmunityGrant,
                new ConditionStamp(s.RuleClock),immunity)).State.Journal;
            s.Conditions=s.Conditions.Select(x=>x.Target==after.Target?after:x).ToArray();
        }
        private static bool IsFerryApproach(Snapshot s,WorldTraversalRecord edge)
            =>s.FerryWraith!=null&&s.FerryWraith.Admission==null&&FerryWraithProfile.MatchesApproach(edge);
        private static long FerryContactMarker(Snapshot s)
        {
            var prior=s.PostRecoveryEncounter?.Admission?.Epoch;if(prior==null)return -1;
            long slot=prior.SlotAt(s.RuleClock);
            return prior.Start(slot)==s.RuleClock&&prior.LatestStart(PostRecoveryEncounterDefinition.Actor,slot)==slot?slot:-1;
        }
        private static bool FerryOldEndsSettled(Snapshot s)
        {
            var prior=s.PostRecoveryEncounter.Admission.Epoch;
            foreach(string actor in FerryWraithProfile.Party) {
                long start=prior.LatestStart(actor,prior.SlotAt(s.RuleClock));
                if(start<0||prior.Start(start+1)>s.RuleClock)return false;
                if(actor!=ClericRpProfile.Actor)continue;
                bool required=s.CastingStrain.Single(x=>x.ActorId==actor).Dissonance>0
                    ||s.CastingActivities.Any(x=>x.Turn.ActorId==actor&&x.Turn.EpochId==prior.Id&&x.Turn.LocalStart==start);
                if(required&&!s.CastingTurnEnds.Any(x=>x.Turn.ActorId==actor&&x.Turn.EpochId==prior.Id
                    &&x.Turn.LocalStart==start&&x.At==prior.Start(start+1)))return false;
            }
            return true;
        }
        private string AssessFerryContact(Snapshot s,bool arrival)
        {
            var record=s.FerryWraith;
            if(record.Admission!=null)return "FerryEncounterAlreadyEntered";
            if(!record.CompanionConsents)return "FerryCompanionConsentMissing";
            if(!record.DirectorAuthorizes)return "FerryDirectorMandateMissing";
            if(s.InventoryCombat||s.Encounter!=null||s.PostRecoveryEncounter?.Admission==null
                ||!s.ClosedEncounters.Any(x=>x.Encounter.Id==PostRecoveryEncounterDefinition.Encounter)
                ||!s.Lives.Single(x=>x.ActorId==PostRecoveryEncounterDefinition.Actor).Dead)
                return "FerryPriorEncounterClosureRequired";
            if(PendingCalendarChoice(s)||ManufacturingChoicePending(s)||HasPendingRecoveryOffer(s))return "FerryChoicePending";
            if(record.Contacts.Count>=FerryWraithRecord.MaxContacts)return "FerryContactHistoryFull";
            var hero=s.Actors.Single(x=>x.Id==FerryWraithProfile.Hero);
            var companion=s.Actors.Single(x=>x.Id==FerryWraithProfile.Companion);
            var creature=s.Actors.Single(x=>x.Id==FerryWraithProfile.Actor);
            if(hero.X!=8||hero.Y!=(arrival?2:1)||companion.X!=8||companion.Y!=3||creature.X!=10||creature.Y!=2
                ||s.WorldTraversals.Any(x=>FerryWraithProfile.IsParticipant(x.ActorId)))return "FerryParticipantsAbsent";
            if(FerryWraithProfile.Participants.Any(x=>!CapableWorker(s,x)||!TestOnlyClubAttackPolicy.Aware(s,x)))
                return "FerryParticipantsIneligible";
            if(s.RestIntervals.Any(x=>x.Status==RestIntervalStatus.Active&&FerryWraithProfile.IsParticipant(x.ActorId))
                ||s.ExpeditionHavenCareIntervals.Any(x=>x.Status==HavenCareIntervalStatus.Active
                    &&(FerryWraithProfile.IsParticipant(x.ActorId)||FerryWraithProfile.IsParticipant(x.ProviderId)))
                ||s.ExpeditionMoraleRestIntervals.Any(x=>x.Status==MoraleRestIntervalStatus.Active&&FerryWraithProfile.IsParticipant(x.ActorId)))
                return "FerryParticipantInterruptionUnsupported";
            if(!WorldWalkable(s,8,2)||!WorldWalkable(s,8,3)||!WorldWalkable(s,10,2))return "FerryContactUnsupported";
            foreach(string observer in FerryWraithProfile.Participants)
                foreach(string target in FerryWraithProfile.Participants.Where(x=>x!=observer))
                    if(!ObservationRules.CanSee(s,observer,target)||!ObservationGeometry.LineOfEffectClear(s,observer,target))
                        return "FerryAwarenessUnavailable";
            if(arrival&&(FerryContactMarker(s)<0||!FerryOldEndsSettled(s)))return "FerryArrivalOutsideSettledRecoveryStart";
            return null;
        }
        private string AssessFerryWorldStep(Snapshot s,WorldTraversalRecord edge)
        {
            if(s.FerryWraith==null||s.FerryWraith.Admission!=null)return null;
            if(edge.ActorId==FerryWraithProfile.Actor)return "FerryWraithHoldsAuthoredPosition";
            return IsFerryApproach(s,edge)?AssessFerryContact(s,false):null;
        }
        private void ResolveFerryArrival(Snapshot s,WorldTraversalRecord edge,Command cause,RuleTime requested)
        {
            var record=s.FerryWraith;string failure=AssessFerryContact(s,true);
            var contact=new FerryWraithContact(edge.StartedRevision,s.Revision+1,cause.Id,s.RuleClock,requested,failure??"");
            if(failure!=null) {s.FerryWraith=record.Append(contact);RefreshActivityIntervals(s);ObserveCalendar(s);return;}
            var prior=s.PostRecoveryEncounter.Admission.Epoch;
            var actors=FerryWraithProfile.Participants;
            var draws=actors.OrderBy(x=>x,StringComparer.Ordinal).Select(x=>RollWorldInitiative(s,x)).ToArray();
            var order=draws.OrderByDescending(x=>x.Total).ThenBy(x=>FerryWraithProfile.TieOrder(x.ActorId)).Select(x=>x.ActorId).ToArray();
            var party=FerryWraithProfile.Party.Select(x=>new ReinforcementCarry(Interval(s,x),s.BonusActions.Single(b=>b.ActorId==x).Available)).ToArray();
            var activity=s.WorldActivityIntervals.Single(x=>x.ActorId==FerryWraithProfile.Actor);
            // Body permission is not an unspent Reaction. Carry the actual owning ledger too.
            var reactions=actors.Where(x=>Permissions(s,x).Reaction&&(FerryWraithProfile.IsParty(x)
                ?Interval(s,x).ReactionAvailable:s.TacticalActors.Single(t=>t.ActorId==x).ReactionAvailable))
                .OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            var epoch=new WorldScheduleRecord(FerryWraithProfile.Calendar,s.RuleClock,order);
            var admission=new FerryWraithAdmission(epoch,prior.Id,FerryContactMarker(s),draws,party,activity,reactions);
            s.FerryWraith=record.Append(contact,admission);
            s.Encounter=new FixedEncounterRecord(FerryWraithProfile.Encounter,s.RuleClock,order,new[]{s.Revision+1});
            s.WorldActivityIntervals=s.WorldActivityIntervals.Where(x=>x.ActorId!=FerryWraithProfile.Actor).ToArray();
            foreach(string actor in actors) {
                var carried=admission.CarriedInterval(actor);
                var interval=new WorldIntervalRecord(actor,-1,carried.MovementSpent,carried.ActionSpent,carried.DashPaid,
                    reactions.Contains(actor),carried.Interactions);
                if(s.WorldIntervals.Any(x=>x.ActorId==actor))SetInterval(s,interval);else s.WorldIntervals=s.WorldIntervals.Append(interval).ToArray();
                bool bonus=party.SingleOrDefault(x=>x.Interval.ActorId==actor)?.BonusActionAvailable??false;
                s.BonusActions=s.BonusActions.Where(x=>x.ActorId!=actor).Append(new ActorBonusActionRecord(actor,-1,bonus)).ToArray();
                BindLaterIntervalBodies(s,actor,interval,true);
            }
            ProcessLaterRegularStart(s,epoch,0);
            s.InventoryCombat=true;s.InventoryTurnActor=s.Encounter.CurrentActor;s.InventoryInteractions=Interval(s,s.InventoryTurnActor).Interactions;
            foreach(string actor in actors)PauseParticipantWork(s,actor);
            PauseIncompatibleWork(s);
        }
        private static void RefreshFerryEpoch(Snapshot s)
        {
            var record=s.FerryWraith;var epoch=record?.Admission?.Epoch;if(epoch==null)return;
            long slot=epoch.SlotAt(s.RuleClock);if(slot==epoch.ProcessedSlot)return;
            s.FerryWraith=record.At(slot);
            foreach(string actor in epoch.Order.OrderBy(x=>epoch.LatestStart(x,slot))) {
                long start=epoch.LatestStart(actor,slot);
                if(start>=0&&start!=Interval(s,actor).LastStart)ProcessLaterRegularStart(s,epoch,start);
            }
        }
    }
}
#endif
