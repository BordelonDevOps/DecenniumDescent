#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private PostRecoveryEncounterDefinition postRecoveryDefinition;

        internal TestOnlySharedWorldPolicy EnablePostRecoveryEncounter(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration,
            bool companionConsents = true, bool directorAuthorizes = true)
        {
            EnableConnectedClericLongRest(initial,repertoire,declaration);
            postRecoveryDefinition = new PostRecoveryEncounterDefinition(companionConsents,directorAuthorizes);
            bodies.RegisterDeferredConditionTarget(PostRecoveryEncounterDefinition.Actor);
            observationFixture = new ObservationFixture(observationFixture.Width,observationFixture.Height,
                observationFixture.Cells,observationFixture.Profiles.Append(new ObservationSightProfile(PostRecoveryEncounterDefinition.Actor,30,30)));
            ContentFingerprint = PostRecoveryProfile.FingerprintPrefix + RetreatHash(string.Join("|",ContentFingerprint,
                PostRecoveryProfile.Approval,postRecoveryDefinition.Binding,observationFixture.Key,
                FrightenedProfile.SourceRevision,FrightenedProfile.CardSha256,FrightenedProfile.WarriorEngineSha256,
                "initial-off-calendar-npc|exact-old-defender-start|old-ends-settled|no-partial-credit-transfer|"
                + "new-three-person-epoch|source-initial-reaction|actor-specific-fear|earned2-existing-rite-radiance-six-spells|dead-closes-no-reward"));
            return this;
        }

        private void InitializePostRecoveryActor(Snapshot s)
        {
            if (postRecoveryDefinition == null) return;
            const string actor=PostRecoveryEncounterDefinition.Actor, club=PostRecoveryEncounterDefinition.Club;
            var body=s.Characters.Single(x=>x.ActorId==AdditionalTacticalActor.Id);
            s.PostRecoveryEncounter=new PostRecoveryEncounterRecord(postRecoveryDefinition);
            s.Actors=s.Actors.Append(new ActorState { Id=actor,X=4,Y=4 }).ToArray();
            s.Characters=s.Characters.Append(new ActorCharacterRecord(actor,"TEST_ONLY.numeric-warrior3",body.Abilities,body.Levels)).ToArray();
            s.Lives=s.Lives.Append(ActorLifeRules.Record(actor,new LifeState(26,26),false,new[]{club})).ToArray();
            s.Clubs=s.Clubs.Append(new ClubInstance(club,TestOnlyClubAttackPolicy.ClubProfile,actor,actor,actor,4,4)).ToArray();
            s.ActorMovement=s.ActorMovement.Append(new ActorMovementRecord(actor,30)).ToArray();
            s.TacticalActors=s.TacticalActors.Append(new ActorTacticalRecord(actor)).ToArray();
            s.Conditions=s.Conditions.Append(new ConditionJournal(ConditionHistory.PolicyId,actor,new ConditionStamp(s.RuleClock))).ToArray();
        }

        private void InitializePostRecoverySource(Snapshot s)
        {
            if (postRecoveryDefinition == null) return;
            s.CharacterFeatureGrants=s.CharacterFeatureGrants.Append(new CharacterFeatureGrantRecord(PostRecoveryEncounterDefinition.Actor,
                FrightenedProfile.SourceId,"Warrior",2,"",0,CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement)).ToArray();
            s.WarriorAbilityChoices=s.WarriorAbilityChoices.Append(new WarriorAbilityChoiceRecord(PostRecoveryEncounterDefinition.Actor,
                CharacterAbility.Strength,FrightenedProfile.SourceRevision,PostRecoveryEncounterDefinition.Entitlement,0)).ToArray();
        }

        private static bool IsPostRecoveryApproach(Snapshot s,WorldTraversalRecord edge)
            => s.PostRecoveryEncounter != null && s.PostRecoveryEncounter.Admission == null && s.PostRecoveryEncounter.Definition.Matches(edge);

        private static long PostRecoveryContactMarker(Snapshot s)
        {
            var epoch=s.Reinforcement?.Admission?.Phase.Epoch;
            if(epoch==null)return -1;
            long slot=epoch.SlotAt(s.RuleClock);
            return epoch.Start(slot)==s.RuleClock && epoch.LatestStart(PostRecoveryEncounterDefinition.PriorDefender,slot)==slot ? slot : -1;
        }

        private static bool PostRecoveryOldEndsSettled(Snapshot s)
        {
            var epoch=s.Reinforcement.Admission.Phase.Epoch;
            foreach(string actor in new[]{PostRecoveryEncounterDefinition.Hero,PostRecoveryEncounterDefinition.Companion}) {
                long local=epoch.LatestStart(actor,epoch.SlotAt(s.RuleClock));
                if(local<0 || epoch.Start(local+1)>s.RuleClock)return false;
                if(actor!=ClericRpProfile.Actor)continue;
                if(s.OrdinaryMagic!=null) { if(!OrdinaryMagicOldDisposition(s,epoch.Id))return false; continue; }
                bool required=s.CastingStrain.Single(x=>x.ActorId==actor).Dissonance>0
                    || s.CastingActivities.Any(x=>x.Turn.ActorId==actor && x.Turn.EpochId==epoch.Id && x.Turn.LocalStart==local);
                if(required && !s.CastingTurnEnds.Any(x=>x.Turn.ActorId==actor && x.Turn.EpochId==epoch.Id && x.Turn.LocalStart==local))return false;
            }
            return true;
        }

        private string AssessPostRecoveryContact(Snapshot s,bool arrival)
        {
            var record=s.PostRecoveryEncounter; var d=record.Definition;
            if(record.Admission!=null)return "PostRecoveryEncounterAlreadyEntered";
            if(!d.CompanionConsents)return "PostRecoveryCompanionConsentMissing";
            if(!d.DirectorAuthorizes)return "PostRecoveryDirectorMandateMissing";
            if(s.InventoryCombat || s.Encounter!=null || s.ClericObjective==null || s.ClericInvocationPath==null
                || s.ConvictionCapacity==null || s.ConvictionCapacity.PoolAcquiredRevision==0 || s.Reinforcement?.Admission==null
                || !s.ClosedEncounters.Any(x=>x.Encounter.Id==s.ClericMilestone.LaterEncounterId)
                || !s.Lives.Single(x=>x.ActorId==PostRecoveryEncounterDefinition.PriorDefender).Dead
                || !s.ClericLongRestSettlements.Any(x=>x.Benefit==ClericLongRestBenefit.Eligible))
                return "PostRecoveryPriorRecoveryRequired";
            if(PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s))return "PostRecoveryChoicePending";
            if(record.Contacts.Count>=PostRecoveryEncounterRecord.MaxContacts)return "PostRecoveryContactHistoryFull";
            var hero=s.Actors.Single(x=>x.Id==PostRecoveryEncounterDefinition.Hero);
            var companion=s.Actors.Single(x=>x.Id==PostRecoveryEncounterDefinition.Companion);
            var defender=s.Actors.Single(x=>x.Id==PostRecoveryEncounterDefinition.Actor);
            if(hero.X!=3 || hero.Y!=(arrival?3:2) || companion.X!=3 || companion.Y!=4 || defender.X!=4 || defender.Y!=4
                || s.WorldTraversals.Any(x=>PostRecoveryEncounterDefinition.IsParticipant(x.ActorId)))return "PostRecoveryParticipantsAbsent";
            if(new[]{hero.Id,companion.Id,defender.Id}.Any(x=>!CapableWorker(s,x) || !TestOnlyClubAttackPolicy.Aware(s,x)))
                return "PostRecoveryParticipantsIneligible";
            if(s.RestIntervals.Any(x=>x.Status==RestIntervalStatus.Active && PostRecoveryEncounterDefinition.IsParticipant(x.ActorId))
                || s.ExpeditionHavenCareIntervals.Any(x=>x.Status==HavenCareIntervalStatus.Active
                    && (PostRecoveryEncounterDefinition.IsParticipant(x.ActorId)||PostRecoveryEncounterDefinition.IsParticipant(x.ProviderId)))
                || s.ExpeditionMoraleRestIntervals.Any(x=>x.Status==MoraleRestIntervalStatus.Active && PostRecoveryEncounterDefinition.IsParticipant(x.ActorId)))
                return "PostRecoveryParticipantInterruptionUnsupported";
            if(!WorldWalkable(s,3,3)||!WorldWalkable(s,3,4)||!WorldWalkable(s,4,4))return "PostRecoveryContactUnsupported";
            var participants=new[]{hero.Id,companion.Id,defender.Id};
            foreach(string observer in participants)
                foreach(string target in participants.Where(x=>x!=observer))
                    if(!ObservationRules.CanSee(s,observer,target) || !ObservationGeometry.LineOfEffectClear(s,observer,target))
                        return "PostRecoveryAwarenessUnavailable";
            if(arrival && (PostRecoveryContactMarker(s)<0 || !PostRecoveryOldEndsSettled(s)))return "PostRecoveryArrivalOutsideSettledDefenderStart";
            return null;
        }

        private string AssessPostRecoveryWorldStep(Snapshot s,WorldTraversalRecord edge)
        {
            if(s.PostRecoveryEncounter==null || s.PostRecoveryEncounter.Admission!=null)return null;
            if(edge.ActorId==PostRecoveryEncounterDefinition.Actor)return "PostRecoveryDefenderHoldsAuthoredPosition";
            return IsPostRecoveryApproach(s,edge)?AssessPostRecoveryContact(s,false):null;
        }

        private void ResolvePostRecoveryArrival(Snapshot s,WorldTraversalRecord edge,Command cause,RuleTime requested)
        {
            var record=s.PostRecoveryEncounter;
            string failure=AssessPostRecoveryContact(s,true);
            var contact=new PostRecoveryContact(edge.StartedRevision,s.Revision+1,cause.Id,s.RuleClock,requested,failure??"");
            if(failure!=null) {
                s.PostRecoveryEncounter=record.Append(contact); RefreshActivityIntervals(s); ObserveCalendar(s); return;
            }
            var prior=s.Reinforcement.Admission.Phase.Epoch;
            var actors=new[]{PostRecoveryEncounterDefinition.Hero,PostRecoveryEncounterDefinition.Companion,PostRecoveryEncounterDefinition.Actor};
            var draws=actors.OrderBy(x=>x,StringComparer.Ordinal).Select(x=>RollWorldInitiative(s,x)).ToArray();
            var order=draws.OrderByDescending(x=>x.Total).ThenBy(x=>PostRecoveryEncounterDefinition.TieOrder(x.ActorId)).Select(x=>x.ActorId).ToArray();
            var party=actors.Where(PostRecoveryEncounterDefinition.IsParty).Select(x=>new ReinforcementCarry(Interval(s,x),
                s.BonusActions.Single(xb=>xb.ActorId==x).Available)).ToArray();
            var activity=s.WorldActivityIntervals.Single(x=>x.ActorId==PostRecoveryEncounterDefinition.Actor);
            var reactions=actors.Where(x=>Permissions(s,x).Reaction).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            var epoch=new WorldScheduleRecord(PostRecoveryEncounterDefinition.Calendar,s.RuleClock,order);
            var admission=new PostRecoveryAdmission(epoch,prior.Id,PostRecoveryContactMarker(s),draws,party,activity,reactions);
            s.PostRecoveryEncounter=record.Append(contact,admission);
            s.Encounter=new FixedEncounterRecord(PostRecoveryEncounterDefinition.Encounter,s.RuleClock,order,new[]{s.Revision+1});
            s.WorldActivityIntervals=s.WorldActivityIntervals.Where(x=>x.ActorId!=PostRecoveryEncounterDefinition.Actor).ToArray();
            ChangeMagicalContext(s,epoch,true,cause);
            foreach(string actor in actors) {
                var carried=admission.CarriedInterval(actor);
                var interval=new WorldIntervalRecord(actor,-1,carried.MovementSpent,carried.ActionSpent,carried.DashPaid,
                    reactions.Contains(actor),carried.Interactions);
                if(s.WorldIntervals.Any(x=>x.ActorId==actor))SetInterval(s,interval);
                else s.WorldIntervals=s.WorldIntervals.Append(interval).ToArray();
                bool bonus=party.SingleOrDefault(x=>x.Interval.ActorId==actor)?.BonusActionAvailable??false;
                s.BonusActions=s.BonusActions.Where(x=>x.ActorId!=actor).Append(new ActorBonusActionRecord(actor,-1,bonus)).ToArray();
                BindLaterIntervalBodies(s,actor,interval,true);
            }
            ProcessLaterRegularStart(s,epoch,0,cause: cause,magicalInitiative: true);
            s.InventoryCombat=true;s.InventoryTurnActor=s.Encounter.CurrentActor;
            s.InventoryInteractions=Interval(s,s.InventoryTurnActor).Interactions;
            foreach(string actor in actors)PauseParticipantWork(s,actor);
            PauseIncompatibleWork(s);
        }

        private IEnumerable<Command> DiscoverPostRecoveryCommands(Snapshot s,string actor)
        {
            if(!PostRecoveryProfile.Active(s) || actor!=PostRecoveryEncounterDefinition.Actor)return Array.Empty<Command>();
            var targets=new[]{new[]{PostRecoveryEncounterDefinition.Hero},new[]{PostRecoveryEncounterDefinition.Companion},
                new[]{PostRecoveryEncounterDefinition.Hero,PostRecoveryEncounterDefinition.Companion}};
            return targets.Select((ids,index)=>new Command("option."+s.Revision+".post-recovery.fear."+index,
                actor,s.Revision,CommandKind.UseIntimidatingPresence,intimidatingPresence:new IntimidatingPresenceRequest(ids)))
                .Where(command=>AssessIntimidatingPresence(s,command)==null).ToArray();
        }

        private static void RefreshPostRecoveryEpoch(Snapshot s, Command cause = null)
        {
            var record=s.PostRecoveryEncounter;var epoch=record?.Admission?.Epoch;if(epoch==null)return;
            long slot=epoch.SlotAt(s.RuleClock);if(slot==epoch.ProcessedSlot)return;
            s.PostRecoveryEncounter=record.At(slot);
            foreach(string actor in epoch.Order.OrderBy(x=>epoch.LatestStart(x,slot))) {
                if(WorldTiming.ForActor(s,actor)?.Id!=epoch.Id)continue;
                long start=epoch.LatestStart(actor,slot);
                if(start>=0 && start!=Interval(s,actor).LastStart)ProcessLaterRegularStart(s,epoch,start,cause: cause);
            }
        }
    }
}
#endif
