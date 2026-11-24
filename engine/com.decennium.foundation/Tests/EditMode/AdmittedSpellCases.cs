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
        private static void AddAdmittedSpellCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("int05_genuine_cast_assessment_denials_payment_and_retry",()=> {
                const string actor=ClericRpProfile.Actor;
                var session=CastingFirstOwnTurn(); var before=ShortRestCapture(session);
                var sim=CastingSimulation(session); var bytes=Bytes(sim); int index=0;
                var denials=new List<object>();
                void Deny(string expected,string spell,string focus="",bool willing=false,bool focused=false) {
                    var command=new Command("int05.cast.deny."+(++index),actor,before.Revision,CommandKind.CastKnownSpell,actor,
                        spellCast:new SpellCastRequest(spell,focus,willing,focused));
                    AssertPureUtility(session,command,expected);
                    var read=sim.AssessCommandFactsV1(CastingAuthority(),command,before.Revision);
                    var actual=sim.Execute(CastingAuthority(),command);
                    Require(actual.Outcome==Outcome.Rejected && actual.Code==expected && bytes.SequenceEqual(Bytes(sim)),
                        "A pure casting denial disagreed with execution or changed state: "+expected);
                    denials.Add(new { expected, read.Constraint.SourcePath, read.Constraint.SourceLine });
                }
                Deny("SpellNotKnown","detect-magic",SpellCastingProfile.FocusId);
                Deny("SpellClassAccessDenied","flare-spark");
                Deny("SpellClassLevelDenied",BishopProfile.Dispel);
                Deny("SpellSourceAdmissionUnsupported","light");
                Deny("SpellFocusUnavailable","arcane-ward","focus.missing",true);
                Deny("UnexpectedSpellFocusSelection","guidance",SpellCastingProfile.FocusId,true);
                Deny("SpellWillingTargetSelectionRequired","guidance");
                Deny("FocusedSpellBenefitUnavailable","sanctuary",SpellCastingProfile.FocusId,true,true);
                Deny("StabilizationTargetNotDying","spare-the-dying");
                var cast=new Command("int05.cast.sanctuary",actor,before.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true));
                AssertPureUtility(session,cast);
                string save=Path.Combine(directory,"int05-cast-before.ddsave");session.Save(save);session.Restore(save);
                AssertPureUtility(session,cast);CommitVialRoute(session,cast);
                var after=ShortRestCapture(session);sim=CastingSimulation(session);var paid=Bytes(sim);
                Require(after.Revision==before.Revision+1 && after.RuleClock==before.RuleClock && after.RandomState==before.RandomState
                    && after.ResonancePools.Single().Current==before.ResonancePools.Single().Current-2
                    && after.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent
                    && after.SpellCasts.Single().CommandId==cast.Id && after.SpellEffects.Single().Present,
                    "The actual Sanctuary cast did not make exactly its native payment and effect.");
                var retry=sim.AssessCommandFactsV1(CastingAuthority(),cast,after.Revision);
                Require(retry.Status==NativeAssessmentStatusV1.AlreadyCommitted && retry.InitialEligibility==null
                    && retry.ProhibitedCallAttempts.All(x=>x==0)
                    && session.Submit(ExpeditionSeat.Player,cast).Response==ExpeditionResponse.Duplicate
                    && paid.SequenceEqual(Bytes(sim)),"A cast retry reevaluated spent Action eligibility or paid again.");
                var fresh=new Command("int05.cast.spent",actor,after.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true));
                AssertPureUtility(session,fresh,"ActionAlreadySpent");
                string complete=Path.Combine(directory,"int05-cast-after.ddsave");session.Save(complete);session.Restore(complete);
                Require(paid.SequenceEqual(Bytes(CastingSimulation(session))),"The assessed actual cast failed authenticated restore.");
                File.WriteAllText(Path.Combine(directory,"int05-cast-assessment-facts.json"),System.Text.Json.JsonSerializer.Serialize(new {
                    scope="Genuine paid reinforcement, repeated pure native casting reads, actual denials, payment, retry and strict restore",
                    beforeRevision=before.Revision,afterRevision=after.Revision,before.RandomState,before.RuleClock,
                    rpBefore=before.ResonancePools.Single().Current,rpAfter=after.ResonancePools.Single().Current,denials,
                    commitFeasibility="NOT CERTIFIED",moduleAcceptance="OPEN" }));
            });
        }
    }
}
#endif
