#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewPostRecoveryExpedition()
            => ConnectedExpeditionSession.StartWithPostRecoveryEncounter(ClericInitialSelection.AuthoredExample(),
                ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());

        private static ConnectedExpeditionSession PreparePostRecoveryExpedition(string directory,bool initialRite=true,int guardedRounds=0,int guardedMask=-1,bool preRestCare=false)
        {
            var session=EarnClericObjective(initialRite,directory,NewPostRecoveryExpedition(),
                heroStance:guardedRounds==0 && guardedMask<0?(Func<int,int>)null:
                    round=>(guardedMask>=0 ? (guardedMask & (1<<round))!=0 : round<guardedRounds)?(int)CombatStance.Guarded:(int)CombatStance.Aggressive);
            var before=ShortRestCapture(session);
            CommitVialRoute(session,new Command("chr03.award",ClericRpProfile.Actor,before.Revision,
                CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
            CommitVialRoute(session,new Command("chr03.advance",ClericRpProfile.Actor,ShortRestCapture(session).Revision,
                CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
            var advanced=ShortRestCapture(session);
            Require(advanced.KnownSpells.Length==6 && advanced.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).MaximumHp==13
                && advanced.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Hp==before.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Hp
                && advanced.ResonancePools.Single().Current==(initialRite?1:3) && advanced.ResonancePools.Single().Maximum==4,
                "Genuine earned2 advancement must preserve prior current life and RP while adding the sourced capacity and sixth spell.");
            if(preRestCare) {
                ReachClericOwnSlot(session);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.UseHealingRite,ClericRpProfile.Actor);
                var care=ShortRestCapture(session).HealingRites.Last();
                Require(care.RpPaid==2 && care.ActualGain>0,"Additional pre-rest care must spend real RP on an actual injury.");
                session.Save(Path.Combine(directory,"post-recovery-pre-rest-care.ddsave"));
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
            }
            LongRestGuidance(session,"long-rest.guidance.first");
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
            LongRestGuidance(session,"long-rest.guidance.repeat");
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:60,y:1);
            ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:100,y:1);
            ClericCommit(session,ClericRpProfile.Actor,CommandKind.InterruptLongRest,
                ClericLongRestProfile.Active(ShortRestCapture(session)).Id);
            LongRestAdvanceTo(session,57600);
            ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:28800,y:1);
            LongRestGuidance(session,"long-rest.guidance.after-rest");
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
            ReachClericOwnSlot(session);
            ClericCommit(session,ClericRpProfile.Actor,CommandKind.UseHealingRite,ConnectedExpeditionSession.Hero);
            var state=ShortRestCapture(session);
            session.Save(Path.Combine(directory,"post-recovery-paid-care.ddsave"));
            Require(state.RuleClock==new RuleTime(86406) && state.ResonancePools.Single().Current==2
                && state.ConvictionBalance.Current==5 && state.CastingStrain.Single().Dissonance==2
                && (initialRite && guardedRounds==0 && guardedMask<0 ? state.Lives.Single(x=>x.ActorId==ConnectedExpeditionSession.Hero).Hp==26
                    :state.Lives.Single(x=>x.ActorId==ConnectedExpeditionSession.Hero).Hp>0),
                "Persistent new occupant must preserve genuine recovery: "+state.RuleClock+" / RP"+state.ResonancePools.Single().Current
                    +" / Conviction"+state.ConvictionBalance.Current+" / Dissonance"+state.CastingStrain.Single().Dissonance
                    +" / hero HP"+state.Lives.Single(x=>x.ActorId==ConnectedExpeditionSession.Hero).Hp);
            return session;
        }

        private static void PostRecoveryStep(ConnectedExpeditionSession session,string actor,int x,int y)
        {
            long speed=TestOnlyClubAttackPolicy.WalkingSpeed(ShortRestCapture(session),actor);
            Require(speed>0,"The actual route requires a positive current walking speed.");
            var duration=new RuleTime(30,speed);
            ClericCommit(session,actor,CommandKind.BeginWorldStep,"walk",x,y);
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,
                x:checked((int)duration.Numerator),y:checked((int)duration.Denominator));
            Require(!ShortRestCapture(session).WorldTraversals.Any(t=>t.ActorId==actor),
                "The authored step did not finish through actual movement; do not substitute a position.");
        }

        private static void PostRecoveryAdvanceTo(ConnectedExpeditionSession session,RuleTime target)
        {
            var now=ShortRestCapture(session).RuleClock;
            Require(target>=now,"A genuine approach cannot reverse the shared clock.");
            if(target==now)return;
            var duration=new RuleTime(checked(target.Numerator*now.Denominator-now.Numerator*target.Denominator),
                checked(target.Denominator*now.Denominator));
            ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,
                x:checked((int)duration.Numerator),y:checked((int)duration.Denominator));
        }

        private static ConnectedExpeditionSession EnterPostRecoveryExpedition(string directory,bool ground=false,bool mistimed=false,bool ward=false,bool initialRite=true,int guardedRounds=0,int guardedMask=-1,bool preRestCare=false,bool finishCare=false)
        {
            var session=PreparePostRecoveryExpedition(directory,initialRite,guardedRounds,guardedMask,preRestCare);
            if(finishCare) {
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                ReachClericOwnSlot(session);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.UseHealingRite,ConnectedExpeditionSession.Hero);
                var care=ShortRestCapture(session).HealingRites.Last();
                Require(care.RpBefore==2 && care.RpAfter==0 && care.ActualGain>0,
                    "Finishing care must consume the remaining RP on genuine residual injury.");
                session.Save(Path.Combine(directory,"post-recovery-finished-care.ddsave"));
            }
            const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor;
            PostRecoveryStep(session,companion,1,0);
            PostRecoveryStep(session,companion,1,0);
            PostRecoveryStep(session,companion,0,1);
            if(ground) {
                var staged=ShortRestCapture(session);var epoch=WorldTiming.ForActor(staged,companion);
                long local=epoch.SlotAt(staged.RuleClock);
                while(epoch.LatestStart(companion,local)!=local || epoch.Start(local)<staged.RuleClock)local++;
                PostRecoveryAdvanceTo(session,epoch.Start(local));
                int dissonance=ShortRestCapture(session).CastingStrain.Single().Dissonance;
                Require(dissonance>0,"The Grounding witness requires genuine positive prior Dissonance.");
                ClericCommit(session,companion,CommandKind.GroundCastingStrain);
                var paid=ShortRestCapture(session);
                Require(paid.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent
                    && paid.CastingStrain.Single().Dissonance==dissonance,
                    "Paid Grounding must wait for its actual old End.");
                session.Save(Path.Combine(directory,"post-recovery-grounding-paid.ddsave"));
                PostRecoveryAdvanceTo(session,epoch.Start(local+1));
                var settled=ShortRestCapture(session);var end=settled.CastingTurnEnds.Last();
                Require(end.Grounding && end.Turn.EpochId==epoch.Id && end.Turn.LocalStart==local
                    && end.At==epoch.Start(local+1) && settled.CastingStrain.Single().Dissonance<dissonance,
                    "Grounding must reduce actual Dissonance once at the original own End before entry.");
                session.Save(Path.Combine(directory,"post-recovery-grounding-settled.ddsave"));
            }
            PostRecoveryStep(session,hero,1,0);
            PostRecoveryStep(session,hero,1,0);
            PostRecoveryStep(session,hero,1,0);
            if(mistimed) {
                var staged=ShortRestCapture(session);var epoch=WorldTiming.ForActor(staged,companion);
                var step=new RuleTime(30,TestOnlyClubAttackPolicy.WalkingSpeed(staged,hero));
                long local=epoch.SlotAt(staged.RuleClock);
                while(epoch.LatestStart(companion,local)!=local || epoch.Start(local)<staged.RuleClock.AddSeconds(2))local++;
                var arrival=epoch.Start(local).AddSeconds(1);
                var depart=new RuleTime(checked(arrival.Numerator*step.Denominator-step.Numerator*arrival.Denominator),
                    checked(arrival.Denominator*step.Denominator));
                PostRecoveryAdvanceTo(session,depart);
                ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",0,1);
                var advance=new Command("exp07.mistimed.long-advance",hero,ShortRestCapture(session).Revision,CommandKind.AdvanceClock,"",10,1);
                PostRecoveryCommit(session,advance);
                var failed=ShortRestCapture(session);var contactFailure=failed.PostRecoveryEncounter.Contacts.Single();
                Require(failed.RuleClock==arrival && failed.RuleClock<epoch.Start(local+1)
                    && failed.Actors.Single(x=>x.Id==hero).Y==3 && !failed.WorldTraversals.Any(x=>x.ActorId==hero)
                    && failed.WorldIntervals.Single(x=>x.ActorId==hero).MovementSpent>=new RuleQuantity(5)
                    && contactFailure.Failure=="PostRecoveryArrivalOutsideSettledDefenderStart"
                    && failed.PostRecoveryEncounter.Admission==null && !failed.InventoryCombat,
                    "Unfinished old interval must commit actual contact cost/failure and yield without auto-wait or entry.");
                string failedPath=Path.Combine(directory,"post-recovery-mistimed-arrival.ddsave");session.Save(failedPath);session.Restore(failedPath);
                var bytes=new SnapshotCodec().Encode(ShortRestCapture(session));
                Require(session.SubmitSessionCommand(advance).Response==ExpeditionResponse.Duplicate
                    && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                    "A mistimed contact retry must be an unchanged duplicate, never a new admission.");
                long defender=local+1;
                while(epoch.LatestStart(PostRecoveryEncounterDefinition.PriorDefender,defender)!=defender)defender++;
                PostRecoveryAdvanceTo(session,epoch.Start(defender));
                Require(ShortRestCapture(session).PostRecoveryEncounter.Admission==null
                    && ShortRestCapture(session).PostRecoveryEncounter.Contacts.Count==1,
                    "Standing at a later valid timestamp must not turn failed contact into combat.");
                session.Save(Path.Combine(directory,"post-recovery-standing-after-failure.ddsave"));
                PostRecoveryStep(session,hero,0,-1);
            }
            if(ward) {
                var staged=ShortRestCapture(session);var epoch=WorldTiming.ForActor(staged,companion);
                long local=epoch.SlotAt(staged.RuleClock);
                while(epoch.LatestStart(companion,local)!=local || epoch.Start(local)<staged.RuleClock)local++;
                PostRecoveryAdvanceTo(session,epoch.Start(local));
                PostRecoveryCommit(session,new Command("exp07.old-ward",companion,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,hero,spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)));
                session.Save(Path.Combine(directory,"post-recovery-old-ward.ddsave"));
            }
            var before=ShortRestCapture(session);var old=before.Reinforcement.Admission.Phase.Epoch;
            var duration=new RuleTime(30,TestOnlyClubAttackPolicy.WalkingSpeed(before,hero));
            var earliest=new RuleTime(checked(before.RuleClock.Numerator*duration.Denominator+duration.Numerator*before.RuleClock.Denominator),
                checked(before.RuleClock.Denominator*duration.Denominator));
            long contact=old.SlotAt(before.RuleClock);
            while(old.Order[(int)(contact%old.Order.Count)]!=PostRecoveryEncounterDefinition.PriorDefender
                || old.Start(contact)<earliest)contact++;
            var contactAt=old.Start(contact);
            var departure=new RuleTime(checked(contactAt.Numerator*duration.Denominator-duration.Numerator*contactAt.Denominator),
                checked(contactAt.Denominator*duration.Denominator));
            var wait=new RuleTime(checked(departure.Numerator*before.RuleClock.Denominator-before.RuleClock.Numerator*departure.Denominator),
                checked(departure.Denominator*before.RuleClock.Denominator));
            if(wait>default(RuleTime))ClericCommit(session,hero,CommandKind.AdvanceClock,x:checked((int)wait.Numerator),y:checked((int)wait.Denominator));
            session.Save(Path.Combine(directory,"post-recovery-before-contact.ddsave"));
            ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",0,1);
            var half=new RuleTime(duration.Numerator,checked(duration.Denominator*2));
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:checked((int)half.Numerator),y:checked((int)half.Denominator));
            var partial=ShortRestCapture(session);
            Require(partial.WorldTraversals.Single().DistanceFeet==new RuleQuantity(5,2)
                && partial.PostRecoveryEncounter.Admission==null,"Fractional contact must remain genuine incomplete travel.");
            string midway=Path.Combine(directory,"post-recovery-partway.ddsave");session.Save(midway);session.Restore(midway);
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:checked((int)half.Numerator),y:checked((int)half.Denominator));
            var entered=ShortRestCapture(session);var admission=entered.PostRecoveryEncounter.Admission;
            Require(admission!=null && entered.InventoryCombat && entered.RuleClock==old.Start(contact)
                && entered.Encounter.Id==PostRecoveryEncounterDefinition.Encounter && entered.Encounter.Order.Count==3
                && admission.PartyCarried.Count==2 && admission.DefenderActivity.ActorId==PostRecoveryEncounterDefinition.Actor
                && entered.ClosedEncounters.Count(x=>x.Encounter.Id==entered.ClericMilestone.LaterEncounterId)==1,
                "The paid, recovered party did not enter the fresh encounter at the exact settled old defender Start.");
            string path=Path.Combine(directory,"post-recovery-entered.ddsave");session.Save(path);session.Restore(path);
            Require(new SnapshotCodec().Encode(entered).SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                "New admission failed exact strict save/restore.");
            return session;
        }

        private static void PostRecoveryCommit(ConnectedExpeditionSession session,Command command)
        {
            var seat=command.Actor==PostRecoveryEncounterDefinition.Actor?ExpeditionSeat.RecoveryOpponent:ExpeditionSeat.Player;
            var query=session.QueryCastingCommand(seat,command);
            var result=command.Kind==CommandKind.AdvanceClock || command.Kind==CommandKind.EndFixedEncounter
                ?session.SubmitSessionCommand(command):session.Submit(seat,command);
            Require(result.Response==ExpeditionResponse.Committed && result.Revision==command.ExpectedRevision+1,
                "Post-recovery command failed: "+command.Kind+" / "+command.Actor+" / r"+command.ExpectedRevision+" / "+query.Code+" / "+result.Response);
        }

        private static void PostRecoveryChooseStance(ConnectedExpeditionSession session)
        {
            var state=ShortRestCapture(session);string actor=state.Encounter.CurrentActor;
            if(state.Lives.Single(x=>x.ActorId==actor).Hp>0)
                PostRecoveryCommit(session,new Command("exp07.guard."+state.Revision,actor,state.Revision,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(state.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)));
        }

        private static void PostRecoveryEnd(ConnectedExpeditionSession session)
        {
            var state=ShortRestCapture(session);
            PostRecoveryCommit(session,new Command("exp07.end."+state.Revision,state.Encounter.CurrentActor,state.Revision,
                CommandKind.EndRegularTurn,state.Encounter.CurrentTurnId));
        }

        private static bool PostRecoveryFear(Snapshot state,string actor)
        {
            var history=ConditionHistory.Restore(state.Conditions.Single(x=>x.Target==actor));
            return state.FrightenedSaves.Where(x=>x.TargetId==actor && !x.Repeat && x.ApplicationId!="")
                .Any(x=>history.Ledger.Applications.Any(a=>a.Id==x.ApplicationId && a.Present(history.Ledger.Now)));
        }

        private static void AddPostRecoveryEncounterCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("exp07_post_recovery_genesis_and_authority",()=> {
                var session=NewPostRecoveryExpedition();var state=ShortRestCapture(session);var codec=new SnapshotCodec();
                const string npc=PostRecoveryEncounterDefinition.Actor;
                Require(state.WireSchemaVersion==111 && state.SchemaVersion==90 && state.PostRecoveryEncounter!=null
                    && state.PostRecoveryEncounter.Admission==null && state.PostRecoveryEncounter.Contacts.Count==0
                    && WorldTiming.ForActor(state,npc)==null && !state.WorldIntervals.Any(x=>x.ActorId==npc)
                    && state.WorldActivityIntervals.Count(x=>x.ActorId==npc)==1
                    && state.Lives.Single(x=>x.ActorId==npc).Hp==26
                    && state.WarriorAbilityChoices.Length==2 && state.AbilityRecharges.Length==0,
                    "The new actor must exist at genesis with actual off-calendar activity and its own source, without an invented regular Start.");
                var own=session.View(ExpeditionSeat.RecoveryOpponent);
                Require(own.Actors.Count==1 && own.Actors.Single().Position.Id==npc && own.LongRest==null
                    && !session.View(ExpeditionSeat.Player).Actors.Any(x=>x.Position.Id==npc),
                    "Recovery-opponent seat must expose only its own resources.");
                var denied=new Command("exp07.unauthorized",npc,0,CommandKind.UseIntimidatingPresence,
                    intimidatingPresence:new IntimidatingPresenceRequest(new[]{ConnectedExpeditionSession.Hero}));
                var before=codec.Encode(state);
                Require(session.Submit(ExpeditionSeat.FirstOpponent,denied).Response==ExpeditionResponse.NotAuthorized
                    && session.Submit(ExpeditionSeat.Player,denied).Response==ExpeditionResponse.NotAuthorized
                    && !session.QueryCastingCommand(ExpeditionSeat.FirstOpponent,denied).Admissible,
                    "Old and party seats must not inherit the new opponent's authority.");
                string save=Path.Combine(directory,"post-recovery-genesis.ddsave");session.Save(save);session.Restore(save);
                Require(before.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Genesis save/restore or rejection changed state.");
            });

            cases.Add("exp07_post_recovery_genuine_approach_and_calendar",()=> {
                EnterPostRecoveryExpedition(directory);
            });
            cases.Add("exp07_post_recovery_genuine_player_and_director_ties",()=> {
                foreach(bool playerTie in new[]{false,true}) {
                    string branch=Path.Combine(directory,playerTie?"player-tie":"director-tie");Directory.CreateDirectory(branch);
                    var session=EnterPostRecoveryExpedition(branch,initialRite:!playerTie,
                        guardedRounds:playerTie?0:6,guardedMask:playerTie?5:-1,preRestCare:playerTie,finishCare:true);
                    var state=ShortRestCapture(session);var entry=state.PostRecoveryEncounter.Admission;
                    const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                    var expected=playerTie?new[]{npc,hero,companion}:new[]{companion,npc,hero};
                    Require(entry.Draws.Select(x=>x.Natural).SequenceEqual(playerTie?new[]{5,5,17}:new[]{6,12,6})
                        && state.Encounter.Order.SequenceEqual(expected) && state.ResonancePools.Single().Current==0,
                        "Actual paid injury care and prior combat must reach the genuine tied rolls and declared authority order.");
                    Require(entry.Draws.All(x=>x.Bonus==0 && x.DexterityModifier==0)
                        && state.HealingRites.Last().ActualGain>0 && state.HealingRites.Last().RpPaid==2,
                        "Tie evidence must not inject bonuses, draws or recovery; actual care and shared RNG remain causal.");
                    foreach(string actor in expected) {
                        Require(ShortRestCapture(session).Encounter.CurrentActor==actor,"Actual first Starts must follow the declared tie authority.");
                        PostRecoveryChooseStance(session);PostRecoveryEnd(session);
                    }
                    session.Save(Path.Combine(branch,"post-recovery-tied-first-round.ddsave"));
                }
            });
            cases.Add("exp07_post_recovery_grounding_old_end_then_contact",()=> {
                string branch=Path.Combine(directory,"grounding");Directory.CreateDirectory(branch);
                EnterPostRecoveryExpedition(branch,ground:true);
            });
            cases.Add("exp07_post_recovery_mistimed_contact_requires_fresh_approach",()=> {
                string branch=Path.Combine(directory,"mistimed");Directory.CreateDirectory(branch);
                var session=EnterPostRecoveryExpedition(branch,mistimed:true);
                var contacts=ShortRestCapture(session).PostRecoveryEncounter.Contacts;
                Require(contacts.Count==2 && contacts[0].Failure!="" && contacts[1].Failure==""
                    && contacts[1].ApproachRevision>contacts[0].Revision,
                    "A genuine fresh paid approach must follow the retained failed contact.");
            });
            cases.Add("exp07_post_recovery_initial_reaction_and_carried_spending",()=> {
                var session=EnterPostRecoveryExpedition(directory);
                const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                var state=ShortRestCapture(session);var admission=state.PostRecoveryEncounter.Admission;
                Require(state.Encounter.CurrentActor==companion && admission.CarriedInterval(hero).MovementSpent==new RuleQuantity(5)
                    && state.WorldIntervals.Single(x=>x.ActorId==hero).LastStart==-1
                    && state.WorldIntervals.Single(x=>x.ActorId==hero).MovementSpent==new RuleQuantity(5)
                    && state.WorldIntervals.Single(x=>x.ActorId==npc).LastStart==-1
                    && state.WorldIntervals.Single(x=>x.ActorId==npc).ReactionAvailable,
                    "Nonfirst actors must retain actual expenditure and source initial Reaction without a regular Start.");
                PostRecoveryCommit(session,new Command("exp07.initial.stance",companion,state.Revision,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(state.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)));
                state=ShortRestCapture(session);
                PostRecoveryCommit(session,new Command("exp07.initial.leave-reach",companion,state.Revision,CommandKind.TacticalStep,
                    state.Encounter.CurrentTurnId,2,3));
                state=ShortRestCapture(session);var pending=state.TacticalMoves.Single(x=>x.Pending);
                Require(pending.Reactors[pending.ResponseIndex]==npc && state.WorldIntervals.Single(x=>x.ActorId==npc).LastStart==-1,
                    "A genuine pre-first-Start departure must offer the new defender's ordinary Reaction.");
                string pendingPath=Path.Combine(directory,"post-recovery-initial-reaction-pending.ddsave");session.Save(pendingPath);session.Restore(pendingPath);
                PostRecoveryCommit(session,new Command("exp07.initial.react",npc,state.Revision,CommandKind.RespondOpportunityAttack,pending.Id,
                    combat:new CombatRequest(state.Encounter.CurrentTurnId,PostRecoveryEncounterDefinition.Club,choice:true,
                        pressInstruction:PressHitInstruction.KeepExisting)));
                state=ShortRestCapture(session);
                Require(!state.WorldIntervals.Single(x=>x.ActorId==npc).ReactionAvailable
                    && state.WorldIntervals.Single(x=>x.ActorId==npc).LastStart==-1,
                    "The actual initial Reaction must be spent before the first own regular Start.");
                session.Save(Path.Combine(directory,"post-recovery-initial-reaction-spent.ddsave"));
                PostRecoveryCommit(session,new Command("exp07.initial.end-companion",companion,state.Revision,CommandKind.EndRegularTurn,state.Encounter.CurrentTurnId));
                state=ShortRestCapture(session);
                Require(state.Encounter.CurrentActor==hero && state.WorldIntervals.Single(x=>x.ActorId==hero).MovementSpent==default
                    && !state.WorldIntervals.Single(x=>x.ActorId==npc).ReactionAvailable,
                    "Only the actual hero Start may refresh its carried movement; it must not refresh the NPC Reaction.");
                PostRecoveryCommit(session,new Command("exp07.initial.hero-stance",hero,state.Revision,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(state.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)));
                state=ShortRestCapture(session);
                PostRecoveryCommit(session,new Command("exp07.initial.end-hero",hero,state.Revision,CommandKind.EndRegularTurn,state.Encounter.CurrentTurnId));
                state=ShortRestCapture(session);
                Require(state.Encounter.CurrentActor==npc && state.WorldIntervals.Single(x=>x.ActorId==npc).LastStart==2
                    && state.WorldIntervals.Single(x=>x.ActorId==npc).ReactionAvailable,
                    "The NPC's first actual regular Start must supply the ordinary refresh exactly once.");
                session.Save(Path.Combine(directory,"post-recovery-npc-first-start.ddsave"));
            });
            cases.Add("exp07_post_recovery_original_spell_endpoints_and_current_decay",()=> {
                var session=EnterPostRecoveryExpedition(directory,ward:true);
                const string companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                var state=ShortRestCapture(session);var old=state.Reinforcement.Admission.Phase.Epoch;
                var wardEffect=state.SpellEffects.Single(x=>x.CastId=="exp07.old-ward");
                var guidance=state.SpellEffects.Single(x=>x.CastId=="long-rest.guidance.after-rest");
                Require(wardEffect.Present && guidance.Present && wardEffect.ExpiryTurn.EpochId==old.Id
                    && wardEffect.ExpiresAt>state.RuleClock && guidance.ExpiresAt==new RuleTime(86460),
                    "Genuine old Ward and Guidance must cross entry with their original virtual and absolute endpoints.");
                void StanceAndEnd() {
                    var s=ShortRestCapture(session);string actor=s.Encounter.CurrentActor;
                    PostRecoveryCommit(session,new Command("exp07.effects.stance."+s.Revision,actor,s.Revision,CommandKind.SelectCombatStance,
                        combat:new CombatRequest(s.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)));
                    s=ShortRestCapture(session);
                    PostRecoveryCommit(session,new Command("exp07.effects.end."+s.Revision,actor,s.Revision,CommandKind.EndRegularTurn,s.Encounter.CurrentTurnId));
                }
                StanceAndEnd();state=ShortRestCapture(session);
                var expired=state.SpellEffects.Single(x=>x.Id==wardEffect.Id);
                Require(!expired.Present && expired.EndedAt==wardEffect.ExpiresAt
                    && state.WorldIntervals.Single(x=>x.ActorId==companion).LastStart==0,
                    "Old virtual Ward expiry must not refresh the companion's current new-epoch interval.");
                StanceAndEnd();StanceAndEnd();state=ShortRestCapture(session);
                Require(state.Encounter.CurrentActor==companion,"Actual new companion Start is required.");
                PostRecoveryCommit(session,new Command("exp07.effects.cast-stance",companion,state.Revision,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(state.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)));
                state=ShortRestCapture(session);
                PostRecoveryCommit(session,new Command("exp07.effects.new-ward",companion,state.Revision,CommandKind.CastKnownSpell,companion,
                    spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)));
                state=ShortRestCapture(session);int strain=state.CastingStrain.Single().Dissonance;
                PostRecoveryCommit(session,new Command("exp07.effects.cast-end",companion,state.Revision,CommandKind.EndRegularTurn,state.Encounter.CurrentTurnId));
                StanceAndEnd();state=ShortRestCapture(session);
                Require(state.Encounter.CurrentActor==npc && state.CastingStrain.Single().Dissonance==strain,
                    "The superseded old companion End must not grant idle decay during a new magical interval.");
                while(ShortRestCapture(session).RuleClock<guidance.ExpiresAt)StanceAndEnd();
                state=ShortRestCapture(session);var absolute=state.SpellEffects.Single(x=>x.Id==guidance.Id);
                Require(!absolute.Present && absolute.EndedAt==guidance.ExpiresAt,
                    "The old absolute Guidance deadline must settle once at its original timestamp.");
                string path=Path.Combine(directory,"post-recovery-original-effects-ended.ddsave");session.Save(path);session.Restore(path);
            });
            cases.Add("exp07_post_recovery_ranked_spell_contexts_and_concentration",()=> {
                var session=EnterPostRecoveryExpedition(directory);
                const string companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                string anchor=Path.Combine(directory,"post-recovery-entered.ddsave");
                foreach(string spell in new[]{"sanctuary","purify-food-and-drink","detect-magic"}) {
                    session.Restore(anchor);PostRecoveryChooseStance(session);
                    var state=ShortRestCapture(session);
                    string target=spell=="purify-food-and-drink"?SpellCastingProfile.ContaminatedWaterId:companion;
                    PostRecoveryCommit(session,new Command("exp07.ranked."+spell,companion,state.Revision,CommandKind.CastKnownSpell,target,
                        spellCast:new SpellCastRequest(spell,SpellCastingProfile.FocusId,spell=="sanctuary")));
                    state=ShortRestCapture(session);
                    Require(state.SpellCasts.Last().Turn.EpochId==PostRecoveryEncounterDefinition.Calendar
                        && state.SpellCasts.Last().ClassLevel==2 && state.SpellCasts.Last().BaseRp==2
                        && state.ResonancePools.Single().Current==0 && state.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent,
                        "The genuinely acquired ranked spell must spend its Action and finite RP on the current new calendar.");
                    if(spell=="purify-food-and-drink") {
                        Require(!state.ConsumableContamination.Single(x=>x.LotId==target).Present,
                            "Purify must destroy the actual bound consumable contamination.");
                    } else {
                        PostRecoveryEnd(session);PostRecoveryChooseStance(session);PostRecoveryEnd(session);
                        if(spell=="sanctuary") {
                            PostRecoveryChooseStance(session);state=ShortRestCapture(session);
                            var attack=new Command("exp07.sanctuary.attack",npc,state.Revision,CommandKind.AttackClub,companion,
                                combat:new CombatRequest(state.Encounter.CurrentTurnId,PostRecoveryEncounterDefinition.Club));
                            PostRecoveryCommit(session,attack);state=ShortRestCapture(session);
                            Require(state.SpellSaves.Last().Kind==SpellSaveKind.SanctuaryWisdom
                                && state.SpellSaves.Last().SubjectId==npc
                                && state.SpellSaves.Last().AttackerTurn.EpochId==PostRecoveryEncounterDefinition.Calendar,
                                "Sanctuary must use the new attacker's actual calendar and WIS save.");
                            var pending=state.SanctuaryAdmissions.SingleOrDefault(x=>x.Pending);
                            if(pending!=null) {
                                string pendingPath=Path.Combine(directory,"post-recovery-sanctuary-pending.ddsave");session.Save(pendingPath);session.Restore(pendingPath);
                                var response=new Command("exp07.sanctuary.forgo",npc,state.Revision,CommandKind.RespondSanctuary,pending.Id,
                                    sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo));
                                var bytes=new SnapshotCodec().Encode(state);
                                Require(session.Submit(ExpeditionSeat.FirstOpponent,response).Response==ExpeditionResponse.NotAuthorized
                                    && session.Submit(ExpeditionSeat.Player,response).Response==ExpeditionResponse.NotAuthorized
                                    && !session.QueryCastingCommand(ExpeditionSeat.FirstOpponent,response).Admissible
                                    && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                                    "Old and party principals must not control or disclose the new attacker's Sanctuary choice.");
                                PostRecoveryCommit(session,response);
                                Require(!ShortRestCapture(session).SanctuaryAdmissions.Any(x=>x.Pending),
                                    "The new opponent must be able to resolve its own actual Sanctuary choice.");
                            }
                        } else {
                            PostRecoveryChooseStance(session);PostRecoveryEnd(session);PostRecoveryChooseStance(session);
                            var focus=session.DiscoverCastingCommands(ExpeditionSeat.Player,companion)
                                .First(x=>x.Command.Kind==CommandKind.FocusDetectedAura && x.Query.Admissible).Command;
                            PostRecoveryCommit(session,focus);state=ShortRestCapture(session);
                            Require(state.DetectMagicFocuses.Last().Turn.EpochId==PostRecoveryEncounterDefinition.Calendar,
                                "Detect Magic focus must use the actual new own Action and perceived effect.");
                            PostRecoveryEnd(session);
                            for(int attempt=0;attempt<40 && !ShortRestCapture(session).SpellSaves.Any(x=>x.Kind==SpellSaveKind.ConcentrationConstitution);attempt++) {
                                PostRecoveryChooseStance(session);state=ShortRestCapture(session);
                                if(state.Encounter.CurrentActor==npc)
                                    PostRecoveryCommit(session,new Command("exp07.concentration.attack."+state.Revision,npc,state.Revision,
                                        CommandKind.AttackClub,companion,combat:new CombatRequest(state.Encounter.CurrentTurnId,PostRecoveryEncounterDefinition.Club)));
                                PostRecoveryEnd(session);
                            }
                            state=ShortRestCapture(session);
                            Require(state.SpellSaves.Any(x=>x.Kind==SpellSaveKind.ConcentrationConstitution && x.SubjectId==companion)
                                && state.Lives.Single(x=>x.ActorId==companion).Hp<13,
                                "Genuine new-encounter damage must drive the actual concentration pipeline.");
                        }
                    }
                    string path=Path.Combine(directory,"post-recovery-"+spell+".ddsave");session.Save(path);session.Restore(path);
                }
            });
            cases.Add("exp07_post_recovery_spare_the_dying_on_actual_casualty",()=> {
                var session=EnterPostRecoveryExpedition(directory);
                const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                bool stabilized=false;
                for(int turns=0;turns<240;turns++) {
                    PostRecoveryChooseStance(session);var state=ShortRestCapture(session);string actor=state.Encounter.CurrentActor;
                    var patient=state.Lives.Single(x=>x.ActorId==hero);
                    Require(!patient.Dead,"The stabilization witness must reach a genuine living casualty without repairing death.");
                    if(actor==companion && patient.Hp==0 && !patient.Stable) {
                        session.Save(Path.Combine(directory,"post-recovery-genuine-dying.ddsave"));
                        PostRecoveryCommit(session,new Command("exp07.stabilize",companion,state.Revision,CommandKind.CastKnownSpell,hero,
                            spellCast:new SpellCastRequest("spare-the-dying")));
                        state=ShortRestCapture(session);
                        Require(state.Lives.Single(x=>x.ActorId==hero).Stable && state.Lives.Single(x=>x.ActorId==hero).Hp==0
                            && state.SpellCasts.Last().Turn.EpochId==PostRecoveryEncounterDefinition.Calendar
                            && state.SpellCasts.Last().WordsConsumed>0 && state.ResonancePools.Single().Current==2,
                            "Spare the Dying must stabilize the actual casualty with its real roll and current Action, without healing or RP recovery.");
                        stabilized=true;break;
                    }
                    if(actor==npc && patient.Hp>0)
                        PostRecoveryCommit(session,new Command("exp07.casualty.attack."+state.Revision,npc,state.Revision,CommandKind.AttackClub,hero,
                            combat:new CombatRequest(state.Encounter.CurrentTurnId,PostRecoveryEncounterDefinition.Club)));
                    PostRecoveryEnd(session);
                }
                Require(stabilized,"Actual hostile attacks did not supply the required dying target.");
                string path=Path.Combine(directory,"post-recovery-spare-the-dying.ddsave");session.Save(path);session.Restore(path);
            });
            cases.Add("exp07_post_recovery_fear_blocks_approach_and_penalizes_attack",()=> {
                var session=EnterPostRecoveryExpedition(directory);
                const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                bool denied=false,repeatSurvived=false,attacked=false;
                for(int turns=0;turns<180;turns++) {
                    PostRecoveryChooseStance(session);var state=ShortRestCapture(session);string actor=state.Encounter.CurrentActor;
                    var position=state.Actors.Single(x=>x.Id==actor);var source=state.Actors.Single(x=>x.Id==npc);
                    if(actor==hero && position.X==3) {
                        PostRecoveryCommit(session,new Command("exp07.fear.make-distance",hero,state.Revision,CommandKind.TacticalStep,
                            state.Encounter.CurrentTurnId,2,3));
                        state=ShortRestCapture(session);var pending=state.TacticalMoves.SingleOrDefault(x=>x.Pending);
                        if(pending!=null)PostRecoveryCommit(session,new Command("exp07.fear.decline-opportunity",npc,state.Revision,
                            CommandKind.RespondOpportunityAttack,pending.Id,combat:new CombatRequest(state.Encounter.CurrentTurnId)));
                    } else if(actor==companion && position.Y==4 && state.Actors.Single(x=>x.Id==hero).X==2) {
                        PostRecoveryCommit(session,new Command("exp07.fear.clear-cell",companion,state.Revision,CommandKind.TacticalStep,
                            state.Encounter.CurrentTurnId,3,3));
                    } else if(actor==npc && repeatSurvived && source.X==4) {
                        PostRecoveryCommit(session,new Command("exp07.fear.source-approaches",npc,state.Revision,CommandKind.TacticalStep,
                            state.Encounter.CurrentTurnId,3,4));
                    } else if(actor==npc && source.X==4 && !state.AbilityRecharges.Any(x=>x.ActorId==npc && x.Remaining>0)) {
                        var use=new Command("exp07.fear.use."+state.Revision,npc,state.Revision,CommandKind.UseIntimidatingPresence,
                            intimidatingPresence:new IntimidatingPresenceRequest(new[]{hero}));
                        var beforeUse=new SnapshotCodec().Encode(state);
                        Require(session.DiscoverCastingCommands(ExpeditionSeat.RecoveryOpponent,npc).Any(x=>x.Query.Admissible
                                && x.Command.Kind==CommandKind.UseIntimidatingPresence)
                            && session.DiscoverCastingCommands(ExpeditionSeat.FirstOpponent,npc).Count==0
                            && beforeUse.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                            "Read-only discovery must expose actual owned fear only to its new controller.");
                        PostRecoveryCommit(session,use);state=ShortRestCapture(session);var bytes=new SnapshotCodec().Encode(state);
                        Require(session.Submit(ExpeditionSeat.FirstOpponent,use).Response==ExpeditionResponse.NotAuthorized
                            && session.Submit(ExpeditionSeat.Player,use).Response==ExpeditionResponse.NotAuthorized
                            && session.QueryCastingCommand(ExpeditionSeat.FirstOpponent,use).Code=="NotAuthorized"
                            && session.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(),use).Response==ExpeditionResponse.NotAuthorized
                            && session.Submit(ExpeditionSeat.RecoveryOpponent,use).Response==ExpeditionResponse.Duplicate
                            && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                            "Only the current source owner may receive duplicate disclosure; historical opponent authority must be denied first.");
                    } else if(actor==hero && PostRecoveryFear(state,hero)) {
                        if(source.X==4) {
                            var move=new Command("exp07.fear.denied."+state.Revision,hero,state.Revision,CommandKind.TacticalStep,
                                state.Encounter.CurrentTurnId,3,4);
                            var bytes=new SnapshotCodec().Encode(state);
                            Require(session.QueryCastingCommand(ExpeditionSeat.Player,move).Code=="FrightenedPreventsWillingApproach"
                                && session.Submit(ExpeditionSeat.Player,move).Response==ExpeditionResponse.Unavailable
                                && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                                "A free reachable cell toward the feared source must be denied without payment or RNG change.");
                            denied=true;session.Save(Path.Combine(directory,"post-recovery-fear-approach-denied.ddsave"));
                        } else {
                            PostRecoveryCommit(session,new Command("exp07.fear.paid-attack",hero,state.Revision,CommandKind.AttackClub,npc,
                                combat:new CombatRequest(state.Encounter.CurrentTurnId,"TEST_ONLY.actor-club")));
                            state=ShortRestCapture(session);var roll=state.MeleeAttacks.Last().Attack;
                            Require(denied && roll.Second>0 && roll.Selected==Math.Min(roll.First,roll.Second)
                                && state.WorldIntervals.Single(x=>x.ActorId==hero).ActionSpent,
                                "Actual visible fear must penalize the paid attack with the normal shared dice pipeline.");
                            attacked=true;break;
                        }
                    }
                    PostRecoveryEnd(session);
                    if(actor==hero && denied)repeatSurvived=PostRecoveryFear(ShortRestCapture(session),hero);
                }
                Require(denied && repeatSurvived && attacked,"Actual source uses did not produce the required movement and attack consumers.");
                string path=Path.Combine(directory,"post-recovery-fear-paid-attack.ddsave");session.Save(path);session.Restore(path);
            });
            cases.Add("exp07_post_recovery_carried_action_survives_superseded_start",()=> {
                var session=EnterPostRecoveryExpedition(directory,ward:true,guardedRounds:3);
                const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                var state=ShortRestCapture(session);var a=state.PostRecoveryEncounter.Admission;
                Require(state.Encounter.Order.SequenceEqual(new[]{npc,hero,companion})
                    && a.CarriedInterval(companion).ActionSpent
                    && state.WorldIntervals.Single(x=>x.ActorId==companion).LastStart==-1
                    && state.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent,
                    "Genuine prior Guarded choices and paid old Ward must carry the nonfirst companion's actual spent Action.");
                PostRecoveryChooseStance(session);PostRecoveryEnd(session);state=ShortRestCapture(session);
                var old=state.Reinforcement.Admission.Phase.Epoch;
                Require(old.LatestStart(companion,old.SlotAt(state.RuleClock))==old.SlotAt(state.RuleClock)
                    && state.Encounter.CurrentActor==hero && state.WorldIntervals.Single(x=>x.ActorId==companion).LastStart==-1
                    && state.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent
                    && !state.SpellEffects.Single(x=>x.CastId=="exp07.old-ward").Present,
                    "The old companion Start may expire its old Ward but cannot refresh its current carried Action.");
                string carried=Path.Combine(directory,"post-recovery-spent-action-old-start.ddsave");session.Save(carried);session.Restore(carried);
                PostRecoveryChooseStance(session);PostRecoveryEnd(session);state=ShortRestCapture(session);
                Require(state.Encounter.CurrentActor==companion && state.WorldIntervals.Single(x=>x.ActorId==companion).LastStart==2
                    && !state.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent,
                    "Only the companion's actual new own Start may refresh the carried Action.");
                session.Save(Path.Combine(directory,"post-recovery-spent-action-new-start.ddsave"));
            });
            cases.Add("exp07_post_recovery_authority_rollback_and_forged_restoration",()=> {
                var session=EnterPostRecoveryExpedition(directory);var codec=new SnapshotCodec();
                const string hero=ConnectedExpeditionSession.Hero,companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                var actual=ShortRestCapture(session);var original=codec.Encode(actual);var controls=new List<object>();int strict=0;
                void Forge(string name,Action<Snapshot> alter) {
                    var candidate=actual.Copy();alter(candidate);byte[] bytes;
                    try {bytes=codec.Encode(candidate);} catch(ArgumentException) {
                        controls.Add(new{name,boundary="structural serialization",rejected=true});return;
                    }
                    string path=Path.Combine(directory,"post-recovery-forged-"+name+".ddsave");File.WriteAllBytes(path,bytes);
                    Throws<ArgumentException>(()=>session.Restore(path));strict++;
                    Require(original.SequenceEqual(codec.Encode(ShortRestCapture(session))) && bytes.SequenceEqual(File.ReadAllBytes(path)),
                        "Strict restore accepted or repaired a plausible post-recovery forgery: "+name);
                    controls.Add(new{name,boundary="strict public restore",rejected=true});
                }
                Forge("rng",s=>s.RandomState=DiceStream.Draw(s.RandomState,20).NextState);
                Forge("actor-position",s=>s.Actors.Single(x=>x.Id==npc).X=3);
                Forge("requested-arrival",s=> {
                    var record=s.PostRecoveryEncounter;var contact=record.Entered;
                    s.PostRecoveryEncounter=new PostRecoveryEncounterRecord(record.Definition,
                        new[]{new PostRecoveryContact(contact.ApproachRevision,contact.Revision,contact.CommandId,
                            contact.At,contact.RequestedUntil.AddSeconds(1),contact.Failure)},record.Admission);
                });
                Forge("carried-movement",s=> {
                    var record=s.PostRecoveryEncounter;var a=record.Admission;
                    var carry=a.PartyCarried.Select(x=>x.Interval.ActorId!=hero?x:new ReinforcementCarry(
                        new WorldIntervalRecord(hero,x.Interval.LastStart,default,x.Interval.ActionSpent,x.Interval.DashPaid,
                            x.Interval.ReactionAvailable,x.Interval.Interactions),x.BonusActionAvailable));
                    s.PostRecoveryEncounter=new PostRecoveryEncounterRecord(record.Definition,record.Contacts,
                        new PostRecoveryAdmission(a.Epoch,a.PreviousPartyEpochId,a.PriorDefenderLocalStart,a.Draws,carry,a.DefenderActivity,a.InitialReactionActors));
                });
                Forge("missing-source-grant",s=>s.CharacterFeatureGrants=s.CharacterFeatureGrants.Where(x=>x.ActorId!=npc).ToArray());
                Forge("borrowed-source-choice",s=>s.WarriorAbilityChoices=s.WarriorAbilityChoices.Select(x=>x.ActorId!=npc?x:
                    new WarriorAbilityChoiceRecord(npc,CharacterAbility.Strength,FrightenedProfile.SourceRevision,FrightenedProfile.Entitlement,0)).ToArray());
                Forge("changed-initial-body",s=>s.Characters=s.Characters.Select(x=>x.ActorId!=npc?x:
                    new ActorCharacterRecord(npc,x.ProfileId,new[]{12,10,10,10,10,10},x.Levels)).ToArray());
                Forge("lost-old-archive",s=>s.ClosedEncounters=s.ClosedEncounters.Skip(1).ToArray());
                Require(strict>=2,"At least two plausible checksummed forgeries must reach actual strict public restoration.");
                File.WriteAllBytes(Path.Combine(directory,"post-recovery-forged-restore-before.ddsave"),original);
                File.WriteAllBytes(Path.Combine(directory,"post-recovery-forged-restore-after.ddsave"),codec.Encode(ShortRestCapture(session)));
                string older=Path.Combine(directory,"post-recovery-wrong-profile.ddsave");NewClericLongRestExpedition().Save(older);
                Throws<ArgumentException>(()=>session.Restore(older));
                Require(original.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Cross-profile restore changed or migrated the active simulation.");
                void Deny(Command command,ExpeditionResponse expected) {
                    var before=codec.Encode(ShortRestCapture(session));var result=session.Submit(ExpeditionSeat.Player,command);
                    Require(result.Response==expected && before.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                        "A denied new-encounter command changed canonical state: "+command.Kind);
                    controls.Add(new{command=command.Id,response=result.Response.ToString(),unchanged=true});
                }
                Deny(new Command("exp07.stale",companion,actual.Revision-1,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(actual.Encounter.CurrentTurnId,stance:(int)CombatStance.Aggressive)),ExpeditionResponse.StaleRevision);
                Deny(new Command("exp07.invalid-target",companion,actual.Revision,CommandKind.UseHealingRite,"TEST_ONLY.unknown-recipient"),ExpeditionResponse.Unavailable);
                Deny(new Command("exp07.reenter",hero,actual.Revision,CommandKind.BeginFixedEncounter),ExpeditionResponse.Unavailable);
                PostRecoveryChooseStance(session);PostRecoveryEnd(session);PostRecoveryChooseStance(session);
                var heroTurn=ShortRestCapture(session);var prior=codec.Encode(heroTurn);
                Require(session.SubmitSessionCommand(new Command("exp07.premature-closure",hero,heroTurn.Revision,
                        CommandKind.EndFixedEncounter,heroTurn.Encounter.CurrentTurnId)).Response==ExpeditionResponse.Unavailable
                    && prior.SequenceEqual(codec.Encode(ShortRestCapture(session))),"An unresolved live conflict must not close or consume its outgoing slot.");
                PostRecoveryEnd(session);PostRecoveryChooseStance(session);var current=ShortRestCapture(session);
                var fear=new Command("exp07.revoke.fear",npc,current.Revision,CommandKind.UseIntimidatingPresence,
                    intimidatingPresence:new IntimidatingPresenceRequest(new[]{hero}));
                PostRecoveryCommit(session,fear);var committed=codec.Encode(ShortRestCapture(session));
                session.SetSeatEnabled(ExpeditionSeat.RecoveryOpponent,false);
                Require(session.Submit(ExpeditionSeat.RecoveryOpponent,fear).Response==ExpeditionResponse.NotAuthorized
                    && session.QueryCastingCommand(ExpeditionSeat.RecoveryOpponent,fear).Code=="NotAuthorized"
                    && session.DiscoverCastingCommands(ExpeditionSeat.RecoveryOpponent,npc).Count==0
                    && !session.View(ExpeditionSeat.RecoveryOpponent).Enabled
                    && committed.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                    "Revoked authority must precede query, discovery and duplicate receipt disclosure.");
                session.SetSeatEnabled(ExpeditionSeat.RecoveryOpponent,true);
                Require(session.Submit(ExpeditionSeat.RecoveryOpponent,fear).Response==ExpeditionResponse.Duplicate
                    && committed.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Restoring the controller must preserve persisted idempotency.");
                File.WriteAllText(Path.Combine(directory,"post-recovery-negative-controls.json"),System.Text.Json.JsonSerializer.Serialize(new {
                    scope="Genuine campaign controls; explicit forged candidate states are rejection-only and never accepted gameplay",strictRestoreRejections=strict,
                    controls,wrongProfileRejected=true,revokedBeforeDuplicate=true}));
                string final=Path.Combine(directory,"post-recovery-authority-controls.ddsave");session.Save(final);session.Restore(final);
            });
            cases.Add("exp07_post_recovery_genuine_damage_fear_cure_and_closure",()=> {
                var session=EnterPostRecoveryExpedition(directory);
                const string hero=ConnectedExpeditionSession.Hero, companion=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
                var entry=ShortRestCapture(session);var codec=new SnapshotCodec();
                string oldFear=System.Text.Json.JsonSerializer.Serialize(entry.FrightenedUses);
                int oldArchives=entry.ClosedEncounters.Length;long milestone=entry.ClericObjective.Revision;
                bool cured=false,cast=false;
                try {
                for(int turnCount=0;turnCount<150;turnCount++) {
                    var current=ShortRestCapture(session);string actor=current.Encounter.CurrentActor;
                    string turn=current.Encounter.CurrentTurnId;
                    string Id(string part)=>"exp07."+current.Revision+"."+part;
                    if(current.Lives.Single(x=>x.ActorId==actor).Hp>0)
                        PostRecoveryCommit(session,new Command(Id("stance"),actor,current.Revision,CommandKind.SelectCombatStance,
                            combat:new CombatRequest(turn,stance:(int)CombatStance.Aggressive)));
                    current=ShortRestCapture(session);
                    int uses=current.FrightenedUses.Count(x=>x.ActorId==npc);
                    if(actor==companion && !cured && current.Lives.Single(x=>x.ActorId==hero).Hp<26 && PostRecoveryFear(current,hero)) {
                        session.Save(Path.Combine(directory,"post-recovery-genuine-injury-and-fear.ddsave"));
                        long hp=current.Lives.Single(x=>x.ActorId==hero).Hp;int rp=current.ResonancePools.Single().Current;
                        PostRecoveryCommit(session,new Command(Id("rite"),actor,current.Revision,CommandKind.UseHealingRite,hero,
                            healingRite:new HealingRiteRequest(RadianceCurePreference.Frightened)));
                        current=ShortRestCapture(session);
                        Require(current.HealingRites.Last().ActualGain>0 && current.Lives.Single(x=>x.ActorId==hero).Hp>hp
                            && current.ResonancePools.Single().Current==rp-2 && !PostRecoveryFear(current,hero)
                            && current.RadianceUses.Last().EndedApplicationIds.Count>0
                            && current.RadianceUses.Last().EpochId==PostRecoveryEncounterDefinition.Calendar
                            && current.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent
                            && current.CastingActivities.Last().Kind==CastingActivityKind.MagicalClassAbility,
                            "Actual new-encounter Rite/Radiance must pay, heal genuine injury, cure the real fear and record magical activity.");
                        cured=true;session.Save(Path.Combine(directory,"post-recovery-paid-cure.ddsave"));
                    } else if(actor==companion && cured && !cast) {
                        PostRecoveryCommit(session,new Command(Id("guidance"),actor,current.Revision,CommandKind.CastKnownSpell,hero,
                            spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                        current=ShortRestCapture(session);cast=true;
                        Require(current.SpellCasts.Last().Turn.EpochId==PostRecoveryEncounterDefinition.Calendar
                            && current.SpellCasts.Last().ClassLevel==2 && current.ResonancePools.Single().Current==0,
                            "Actual owned cantrip must use the new own calendar and retain the spent RP balance.");
                    } else if(actor==npc && current.Lives.Single(x=>x.ActorId==npc).Hp>0) {
                        bool ready=!current.AbilityRecharges.Any(x=>x.ActorId==npc && x.Remaining>0);
                        if(current.Lives.Single(x=>x.ActorId==hero).Hp==26 && !cured) {
                            PostRecoveryCommit(session,new Command(Id("injure"),actor,current.Revision,CommandKind.AttackClub,hero,
                                combat:new CombatRequest(turn,PostRecoveryEncounterDefinition.Club)));
                        } else if(ready && (!cured || uses<2)) {
                            PostRecoveryCommit(session,new Command(Id("fear"),actor,current.Revision,CommandKind.UseIntimidatingPresence,
                                intimidatingPresence:new IntimidatingPresenceRequest(new[]{hero})));
                        }
                    } else if(actor==hero && cured && uses>=2) {
                        if(current.Lives.Single(x=>x.ActorId==npc).Dead) {
                            PostRecoveryCommit(session,new Command(Id("close"),actor,current.Revision,CommandKind.EndFixedEncounter,turn));
                            break;
                        }
                        PostRecoveryCommit(session,new Command(Id("attack"),actor,current.Revision,CommandKind.AttackClub,npc,
                            combat:new CombatRequest(turn,"TEST_ONLY.actor-club")));
                    }
                    current=ShortRestCapture(session);
                    PostRecoveryCommit(session,new Command("exp07."+current.Revision+".end",actor,current.Revision,CommandKind.EndRegularTurn,turn));
                }
                } catch { session.Save(Path.Combine(directory,"post-recovery-failed-command-predecessor.ddsave"));throw; }
                var closed=ShortRestCapture(session);
                Require(cured && cast && !closed.InventoryCombat && closed.Encounter==null
                    && closed.Lives.Single(x=>x.ActorId==npc).Dead && closed.ClosedEncounters.Length==oldArchives+1
                    && closed.ClericObjective.Revision==milestone && closed.CharacterAdvancements.Length==1
                    && closed.FrightenedUses.Count(x=>x.ActorId==npc)>=2
                    && oldFear==System.Text.Json.JsonSerializer.Serialize(closed.FrightenedUses.Where(x=>x.ActorId!=npc).ToArray()),
                    "Genuine death/outgoing closure must retain old source history and advancement without a new reward.");
                string path=Path.Combine(directory,"post-recovery-closed.ddsave");session.Save(path);session.Restore(path);
                Require(codec.Encode(closed).SequenceEqual(codec.Encode(ShortRestCapture(session))),"Closed new encounter failed strict replay restore.");
                var oldClock=closed.RuleClock;var position=closed.Actors.Single(x=>x.Id==hero);
                int oldX=position.X;
                PostRecoveryStep(session,hero,-1,0);
                var continued=ShortRestCapture(session);
                Require(continued.RuleClock>oldClock && continued.Actors.Single(x=>x.Id==hero).X==oldX-1
                    && WorldTiming.ForActor(continued,hero).Id==PostRecoveryEncounterDefinition.Calendar
                    && continued.ResonancePools.Single().Current==0,
                    "Ordinary paid continuation must retain the new calendar and finite resource history.");
                session.Save(Path.Combine(directory,"post-recovery-continued.ddsave"));
                var epoch=WorldTiming.ForActor(continued,companion);long local=epoch.SlotAt(continued.RuleClock);
                while(epoch.LatestStart(companion,local)!=local || epoch.Start(local)<=continued.RuleClock)local++;
                PostRecoveryAdvanceTo(session,epoch.Start(local));
                PostRecoveryCommit(session,new Command("exp07.after-closure.ward",companion,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,hero,spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)));
                var castAfter=ShortRestCapture(session);var effect=castAfter.SpellEffects.Last();
                Require(!castAfter.InventoryCombat && castAfter.SpellCasts.Last().Turn.EpochId==epoch.Id
                    && castAfter.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent
                    && castAfter.ResonancePools.Single().Current==0 && effect.Present,
                    "Ordinary post-closure casting must use the retained new epoch and actual current resources.");
                PostRecoveryAdvanceTo(session,effect.ExpiresAt);
                Require(!ShortRestCapture(session).SpellEffects.Single(x=>x.Id==effect.Id).Present,
                    "Ordinary continuation must settle the new caster's original Ward endpoint.");
                string afterPath=Path.Combine(directory,"post-recovery-continued-casting.ddsave");session.Save(afterPath);session.Restore(afterPath);
            });

        }
    }
}
#endif
