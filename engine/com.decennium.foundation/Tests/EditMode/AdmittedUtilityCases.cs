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
        private static void AssertPureUtility(ConnectedExpeditionSession session, Command command, string expected = null,
            Authority authority = null)
        {
            var sim=CastingSimulation(session); var before=Bytes(sim); var state=sim.Capture();
            for(int i=0;i<3;i++) {
                var result=sim.AssessCommandFactsV1(authority ?? CastingAuthority(),command,state.Revision);
                Require(result.Supported && result.Admissible==(expected==null) && result.Constraint?.NativeCode==expected
                    && result.InitialEligibility==(expected==null) && result.CommitFeasibility==null
                    && result.ProhibitedCallAttempts.All(x=>x==0) && before.SequenceEqual(Bytes(sim)),
                    "Native assessment changed state or disagreed with expected admission: "+command.Kind+" / "+result.Status+" / "+result.Constraint?.NativeCode);
            }
        }

        private static void AddAdmittedUtilityCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("int05_repertoire_and_fear_profile_denials_are_pure",()=> {
                var rows=new[] {
                    (NewClericExpedition(),CommandKind.AcquireEarnedSpell,"SpellRepertoireUnavailable"),
                    (NewRepertoireExpedition(),CommandKind.AcquireEarnedSpell,"ClericEarnedAdvancementUnavailable"),
                    (NewClericSettlement(),CommandKind.AcquireEarnedSpell,"EarnedSpellAcquisitionRequiresAdvancementTransaction"),
                    (NewClericExpedition(),CommandKind.CastKnownSpell,"SpellRepertoireUnavailable"),
                    (NewRepertoireExpedition(),CommandKind.CastKnownSpell,"OrdinarySpellcastingUnsupported")
                };
                var facts=new List<object>();int n=0;
                void Check(ConnectedExpeditionSession session,Command command,string code,Authority authority) {
                    var sim=CastingSimulation(session);var before=Bytes(sim);var state=sim.Capture();
                    AssertPureUtility(session,command,code,authority);
                    var read=sim.AssessCommandFactsV1(authority,command,state.Revision);
                    var actual=sim.Execute(authority,command);
                    Require(actual.Outcome==Outcome.Rejected&&actual.Code==code&&before.SequenceEqual(Bytes(sim)),
                        "Source/profile denial changed state or differed from native execution.");
                    facts.Add(new {state.WireSchemaVersion,kind=command.Kind.ToString(),code,
                        read.Constraint.SourcePath,read.Constraint.SourceLine});
                }
                foreach(var row in rows) Check(row.Item1,new Command("int05.source.profile."+(++n),ClericRpProfile.Actor,
                    0,row.Item2,ClericRepertoireProfile.FutureChoice),row.Item3,CastingAuthority());
                var fear=NewFrightenedExpedition();
                Check(fear,new Command("int05.fear.context",FrightenedProfile.Actor,0,CommandKind.UseIntimidatingPresence,
                    intimidatingPresence:new IntimidatingPresenceRequest(new[]{ConnectedExpeditionSession.Hero})),
                    "IntimidatingPresenceContextUnsupported",LaterDefenderController.DefenderAuthority());
                var old=NewRepertoireExpedition();
                Check(old,new Command("int05.fear.unselected",FrightenedProfile.Actor,0,CommandKind.UseIntimidatingPresence,
                    intimidatingPresence:new IntimidatingPresenceRequest(new[]{ConnectedExpeditionSession.Hero})),
                    "IntimidatingPresenceUnavailable",LaterDefenderController.DefenderAuthority());
                File.WriteAllText(Path.Combine(directory,"int05-fear-repertoire-denials.json"),
                    System.Text.Json.JsonSerializer.Serialize(new {scope="Seven authentic factory native denials; no public V1 or acquired entitlement claim",facts}));
            });

            cases.Add("int05_genuine_grounding_assessment_pays_action_once",()=> {
                const string actor=ClericRpProfile.Actor, hero=ConnectedExpeditionSession.Hero;
                var session=CastingFirstOwnTurn();
                CommitVialRoute(session,new Command("int05.ground.source",actor,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                ClericEnd(session,actor);ClericGuard(session,hero);ClericEnd(session,hero);ClericDefender(session);ClericGuard(session,actor);
                var before=ShortRestCapture(session); var strain=before.CastingStrain.Single();
                Require(strain.Dissonance>0 && !before.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent,
                    "The genuine producer must supply positive strain and an available Action.");
                var ground=new Command("int05.ground.pay",actor,before.Revision,CommandKind.GroundCastingStrain);
                AssertPureUtility(session,ground);
                string save=Path.Combine(directory,"int05-ground-before.ddsave");session.Save(save);session.Restore(save);
                AssertPureUtility(session,ground);CommitVialRoute(session,ground);
                var paid=ShortRestCapture(session);
                Require(paid.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent
                    && paid.CastingStrain.Single().Dissonance==strain.Dissonance && paid.RandomState==before.RandomState
                    && paid.RuleClock==before.RuleClock && paid.ResonancePools.Single().Current==before.ResonancePools.Single().Current,
                    "Grounding did not pay only its native Action or reduced strain before settlement.");
                var sim=CastingSimulation(session);var bytes=Bytes(sim);
                Require(sim.AssessCommandFactsV1(CastingAuthority(),ground,paid.Revision).Status==NativeAssessmentStatusV1.AlreadyCommitted
                    &&session.Submit(ExpeditionSeat.Player,ground).Response==ExpeditionResponse.Duplicate &&bytes.SequenceEqual(Bytes(sim)),
                    "Grounding retry paid or settled again.");
                var again=new Command("int05.ground.again",actor,paid.Revision,CommandKind.GroundCastingStrain);
                AssertPureUtility(session,again,"ActionAlreadySpent");
                Require(sim.Execute(CastingAuthority(),again).Code=="ActionAlreadySpent" && bytes.SequenceEqual(Bytes(sim)),
                    "Grounding fresh denial differs from execution.");
                ClericEnd(session,actor);var settled=ShortRestCapture(session);var end=settled.CastingTurnEnds.Last(x=>x.Turn.ActorId==actor);
                int pb=CharacterRuleFacts.ForActor(before,actor).ProficiencyBonus;
                Require(end.Grounding && !end.MagicalActivity && settled.CastingStrain.Single().Dissonance==Math.Max(0,strain.Dissonance-pb),
                    "The actual native interval did not settle Grounding exactly once.");
                string after=Path.Combine(directory,"int05-ground-settled.ddsave");session.Save(after);var settledBytes=Bytes(CastingSimulation(session));
                session.Restore(after);Require(settledBytes.SequenceEqual(Bytes(CastingSimulation(session))),"Grounding did not restore and replay.");
            });

            cases.Add("int05_genuine_aura_focus_assessment_ordinary_context",()=> {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=EarnClericObjective(false,selected:NewOrdinaryMagicExpedition());
                var objective=ShortRestCapture(session);
                CommitVialRoute(session,new Command("int05.focus.award",actor,objective.Revision,
                    CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
                CommitVialRoute(session,new Command("int05.focus.advance",actor,ShortRestCapture(session).Revision,
                    CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
                ReachClericOwnSlot(session);
                var guidance=new Command("int05.focus.aura",actor,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,hero,spellCast:new SpellCastRequest("guidance",willingTarget:true));
                AssertPureUtility(session,guidance);CommitVialRoute(session,guidance);
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                var detect=new Command("int05.focus.detect",actor,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("detect-magic",SpellCastingProfile.FocusId));
                AssertPureUtility(session,detect);CommitVialRoute(session,detect);
                var view=session.View(ExpeditionSeat.Player);var recipient=view.Actors.Single(x=>x.Position.Id==hero);
                var aura=view.Actors.Single(x=>x.Position.Id==actor).Casting.Auras.Single(x=>x.X==recipient.Position.X&&x.Y==recipient.Position.Y);
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);var before=ShortRestCapture(session);
                Require(before.OrdinaryMagic!=null && !before.InventoryCombat && !aura.Focused,
                    "The genuine aura branch did not reach the admitted ordinary magical context.");
                var unknown=new Command("int05.focus.unknown",actor,before.Revision,CommandKind.FocusDetectedAura,"aura.unseen");
                AssertPureUtility(session,unknown,"AuraObservationUnavailable");
                var sim=CastingSimulation(session);var bytes=Bytes(sim);
                Require(sim.Execute(CastingAuthority(),unknown).Code=="AuraObservationUnavailable" && bytes.SequenceEqual(Bytes(sim)),
                    "An unknown aura changed state or native denial.");
                var focus=new Command("int05.focus.pay",actor,before.Revision,CommandKind.FocusDetectedAura,aura.ObservationId);
                AssertPureUtility(session,focus);
                string save=Path.Combine(directory,"int05-focus-before.ddsave");session.Save(save);session.Restore(save);
                AssertPureUtility(session,focus);CommitVialRoute(session,focus);var after=ShortRestCapture(session);
                var observed=session.View(ExpeditionSeat.Player).Actors.Single(x=>x.Position.Id==actor).Casting.Auras.Single(x=>x.ObservationId==aura.ObservationId);
                Require(observed.Focused && observed.SchoolCategory==SpellSourceCatalog.Get("guidance").AccessFor("Cleric").School
                    && after.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent && after.RandomState==before.RandomState
                    && after.RuleClock==before.RuleClock && after.ResonancePools.Single().Current==before.ResonancePools.Single().Current
                    && after.CastingStrain.Single().Dissonance==before.CastingStrain.Single().Dissonance,
                    "Focus changed its native disclosure, Action payment, RP, time or strain.");
                Require(CastingSimulation(session).AssessCommandFactsV1(CastingAuthority(),focus,after.Revision).Status
                    ==NativeAssessmentStatusV1.AlreadyCommitted,"Focus retry reran current action eligibility.");
                string complete=Path.Combine(directory,"int05-focus-after.ddsave");session.Save(complete);bytes=Bytes(CastingSimulation(session));
                session.Restore(complete);Require(bytes.SequenceEqual(Bytes(CastingSimulation(session))),"Paid aura focus failed authenticated restore.");
            });
        }
    }
}
#endif
