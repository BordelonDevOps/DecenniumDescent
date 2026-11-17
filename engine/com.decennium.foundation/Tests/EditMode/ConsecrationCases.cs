#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewConsecrationExpedition() => ConnectedExpeditionSession.StartWithConsecration(
            ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),
            ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
        private static void AddConsecrationCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("chr05_consecration_mechanical_geometry_lifetime_and_source_controls",() => {
                // Detached component controls only. No edited state is saved or adopted as a campaign.
                var session=NewConsecrationExpedition();var initial=ShortRestCapture(session);var codec=new SnapshotCodec();
                var bytes=codec.Encode(initial);
                var rules=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.ConsecrationRules");
                var attack=rules.GetMethod("AttackModifier",BindingFlags.Static|BindingFlags.NonPublic);
                int Modifier(Snapshot s,string actor)=>(int)attack.Invoke(null,new object[]{s,actor});
                Snapshot Arrange(int cx,int cy,int ax,int ay) {
                    var s=initial.Copy();s.Revision=2;s.RuleClock=initial.RuleClock.AddSeconds(1);
                    var zone=new ConsecrationZone("ground.control",1,ClericRpProfile.Actor,cx,cy,initial.RuleClock,false,
                        "TEST_ONLY.component-calendar",0,initial.RuleClock.AddSeconds(18),4);
                    s.Consecration=s.Consecration.WithZones(new[]{zone});
                    var actor=s.Actors.Single(x=>x.Id==FerryWraithProfile.Actor);actor.X=ax;actor.Y=ay;
                    return s;
                }
                var inclusive=Arrange(8,2,11,2);
                Require(Modifier(inclusive,FerryWraithProfile.Actor)==-1,"Inclusive15ft edge lost its one penalty.");
                inclusive.Actors.Single(x=>x.Id==FerryWraithProfile.Actor).X=12;
                Require(Modifier(inclusive,FerryWraithProfile.Actor)==0,"Leaving terrain retained its attack penalty.");
                var sightOnly=Arrange(6,0,8,0);
                Require(Modifier(sightOnly,FerryWraithProfile.Actor)==-1,"Sight-only blocker incorrectly blocked terrain propagation.");
                var effectOnly=Arrange(8,0,10,0);
                Require(Modifier(effectOnly,FerryWraithProfile.Actor)==0,"Effect-only blocker failed to block terrain propagation.");
                var prone=Arrange(8,2,8,2);FerryMechanicalCondition(prone,"Prone");
                Require(Modifier(prone,FerryWraithProfile.Actor)==-1,"Grounded Prone creature lost terrain contact.");
                var owner=prone.Actors.Single(x=>x.Id==ClericRpProfile.Actor);owner.X=0;owner.Y=0;
                Require(Modifier(prone,FerryWraithProfile.Actor)==-1,"Fixed terrain followed its creator.");
                var human=prone.Actors.Single(x=>x.Id==FerryWraithProfile.Hero);human.X=8;human.Y=2;
                Require(Modifier(prone,FerryWraithProfile.Hero)==0,"Known non-Undead fixture acquired a penalty.");
                var zone0=prone.Consecration.Zones.Single();prone.RuleClock=zone0.ExpiresAt;
                Require(Modifier(prone,FerryWraithProfile.Actor)==0,"Tied expiry retained its penalty.");
                var replacement=zone0.Finish(ConsecrationEnd.Replacement,5,zone0.At.AddSeconds(10));
                Require(replacement.PresentAtRevision(replacement.EndAt,4) && !replacement.PresentAtRevision(replacement.EndAt,5)
                    && !replacement.PresentAtRevision(zone0.ExpiresAt,4),"Same-time replacement corrupted prior attack provenance.");
                Throws<ArgumentException>(()=>new ConsecrationRecord(initial.Consecration.PredecessorFingerprint,
                    ConsecrationProfile.HumanoidActors.Skip(1)));
                Throws<ArgumentException>(()=>new ConsecrationAttackContribution("bad",3,initial.RuleClock,
                    FerryWraithProfile.Hero,new RuleQuantity(1),new RuleQuantity(1),true,"ground.control",2));
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Detached controls mutated the genuine genesis.");
                File.WriteAllText(Path.Combine(directory,"scope.txt"),"Detached implementation controls; no source-acquisition, paid command, full-save, gameplay completion or module acceptance claim.");
            });
            cases.Add("chr05_consecration_opt_in_genesis_authority_and_legacy_boundary",() => {
                var session=NewConsecrationExpedition(); var codec=new SnapshotCodec();
                var state=ShortRestCapture(session); var bytes=codec.Encode(state);
                Require(state.WireSchemaVersion==115 && state.Consecration.Zones.Count==0
                    && state.Consecration.HumanoidActors.SequenceEqual(ConsecrationProfile.HumanoidActors),"New genesis lost its explicit source/type envelope.");
                Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"New genesis component roundtrip changed bytes.");
                var command=new Command("consecration.no-calendar",ClericRpProfile.Actor,state.Revision,CommandKind.UseConsecrate,
                    consecrate:new ConsecrateRequest(3,3));
                Require(!session.QueryCastingCommand(ExpeditionSeat.Player,command).Admissible
                    && session.Submit(ExpeditionSeat.Player,command).Response!=ExpeditionResponse.Committed
                    && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Absent source calendar admitted or mutated Consecrate.");
                session.SetSeatEnabled(ExpeditionSeat.Player,false);
                Require(session.Submit(ExpeditionSeat.Player,command).Response==ExpeditionResponse.NotAuthorized
                    && session.ObserveConsecration(ExpeditionSeat.Player,ClericRpProfile.Actor).Count==0,"Revoked authority exposed or executed terrain.");
                var old=NewFerryExpedition(); var oldBefore=codec.Encode(ShortRestCapture(old));
                Require(ShortRestCapture(old).WireSchemaVersion==114
                    && old.Submit(ExpeditionSeat.Player,command).Response!=ExpeditionResponse.Committed
                    && oldBefore.SequenceEqual(codec.Encode(ShortRestCapture(old))),"Old Ferry profile acquired terrain behavior.");
                BishopCheckpoint(session,directory,"consecration-genesis");
            });
            cases.Add("chr05_consecration_genuine_paid_zone_rite_and_expiry",() => {
                var session=RunFerryAdmission(directory,NewConsecrationExpedition());
                const string hero=FerryWraithProfile.Hero, companion=ClericRpProfile.Actor;
                Snapshot State()=>ShortRestCapture(session);
                void End() { var s=State();
                    if(!TestOnlyClubAttackPolicy.ConditionsFor(s,s.Encounter.CurrentActor).View().Unaware
                        && !s.Stances.Any(x=>x.TurnOrdinal==s.Encounter.TurnOrdinal&&EncounterHistory.InCurrent(s,x.Revision))) {
                        Guard(); s=State();
                    }
                    BishopCommit(session,new Command("consecrate.end."+s.Revision,s.Encounter.CurrentActor,s.Revision,
                    CommandKind.EndRegularTurn,s.Encounter.CurrentTurnId)); }
                void Guard() { var s=State(); BishopCommit(session,new Command("consecrate.guard."+s.Revision,s.Encounter.CurrentActor,s.Revision,
                    CommandKind.SelectCombatStance,combat:new CombatRequest(s.Encounter.CurrentTurnId,stance:(int)CombatStance.Guarded))); }
                void Auto() {
                    for(int i=0;i<16&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.FerryOpponent;i++)
                        Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Actual Ferry controller failed.");
                    Require(session.View(ExpeditionSeat.Player).NextSeat!=ExpeditionTurnSeat.FerryOpponent,"Controller exceeded the declared finite drain.");
                }
                Guard(); End(); Auto();
                Require(State().Encounter.CurrentActor==companion,"Missing first genuine companion Start.");
                var before=State(); var request=new Command("consecrate.first",companion,before.Revision,CommandKind.UseConsecrate,
                    consecrate:new ConsecrateRequest(8,2));
                Require(session.QueryCastingCommand(ExpeditionSeat.Player,request).Admissible,"Genuine funded Consecrate unavailable.");
                BishopCommit(session,request); var created=State(); var zone=created.Consecration.Zones.Single();
                Require(before.ResonancePools.Single().Current==7 && created.ResonancePools.Single().Current==5
                    && before.RandomState==created.RandomState && before.RuleClock==created.RuleClock
                    && created.WorldIntervals.Single(x=>x.ActorId==companion).ActionSpent
                    && created.AbilityRecharges.Single(x=>x.AbilityId==ConsecrationProfile.Consecrate).Remaining==3,
                    "Consecrate payment, activity or RNG was not exact.");
                var codec=new SnapshotCodec(); var paid=codec.Encode(created);
                Require(session.Submit(ExpeditionSeat.Player,request).Response==ExpeditionResponse.Duplicate
                    && paid.SequenceEqual(codec.Encode(State())),"Paid terrain retry changed state.");
                BishopCheckpoint(session,directory,"consecration-paid");
                End(); Guard(); End(); Auto();
                Require(State().Encounter.CurrentActor==companion && State().RuleClock<zone.ExpiresAt,"Rite missed the live terrain interval.");
                var riteState=State(); var riteCommand=new Command("consecrate.rite",companion,riteState.Revision,CommandKind.UseHealingRite,hero);
                BishopCommit(session,riteCommand); var after=State();
                var rite=after.HealingRites.Single(x=>x.CommandId==riteCommand.Id);
                var ground=after.Consecration.Healing.Single(x=>x.RiteCommandId==riteCommand.Id);
                var radiance=after.RadianceUses.Single(x=>x.RiteCommandId==riteCommand.Id);
                var aura=after.BishopEntry.AuraHealing.Single(x=>x.RiteCommandId==riteCommand.Id);
                Require(rite.ActualGain>0 && ground.ActualGain==1 && ground.HpBefore==rite.HpAfter && radiance.BaseHpAfter==rite.HpAfter
                    && radiance.PreRadianceHp()==ground.HpAfter && aura.HpBefore==radiance.HpAfter
                    && after.ResonancePools.Single().Current==3,"Genuine base/Ground/Radiance/Aura chain lost provenance or payment.");
                BishopCheckpoint(session,directory,"consecration-rite");
                int rounds=0;
                while(State().RuleClock<zone.ExpiresAt && rounds++<12) { End(); Auto(); }
                var expired=State();
                Require(expired.Consecration.Zones.Single().End==ConsecrationEnd.Expiry
                    && expired.Consecration.Zones.Single().EndAt==zone.ExpiresAt
                    && expired.AbilityRecharges.Single(x=>x.AbilityId==ConsecrationProfile.Consecrate).Remaining==0,
                    "Original third owner Start did not expire terrain and independently settle recharge.");
                Require(expired.Consecration.Attacks.Any(x=>x.Undead&&x.ZoneCommandId==zone.CommandId
                    &&x.Contribution==-1&&x.TotalModifier==2),"No genuine source Claw received the zone's one-point penalty.");
                BishopCheckpoint(session,directory,"consecration-expired");
            });
        }
    }
}
#endif
