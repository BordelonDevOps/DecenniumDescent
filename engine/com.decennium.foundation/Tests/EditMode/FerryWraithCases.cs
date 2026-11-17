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
        private static ConnectedExpeditionSession NewFerryExpedition()=>ConnectedExpeditionSession.StartWithFerryWraith(
            ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),
            ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
        private static void FerryMechanicalCondition(Snapshot s,string kind)
        {
            var journal=s.Conditions.Single(x=>x.Target==FerryWraithProfile.Actor);
            var history=ConditionHistory.Restore(journal).Append(ConditionOperation.Apply("ferry.mechanical.apply."+kind,
                journal.Now,new ConditionApplicationData("ferry.mechanical."+kind,"TEST_ONLY.owner","TEST_ONLY.supplied-event",
                    kind,null,"supplied-end",true))).State;
            s.Conditions=s.Conditions.Select(x=>x.Target==journal.Target?history.Journal:x).ToArray();
        }
        private static void AddFerryWraithCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("tac10_ferry_numeric_origin_and_source_payload_roundtrip",()=>{
                var session=NewFerryExpedition();var s=ShortRestCapture(session);var codec=new SnapshotCodec();
                var before=codec.Encode(s);var facts=ActorNumericFacts.ForActor(s,FerryWraithProfile.Actor);
                Require(facts.IsCreature&&facts.ProficiencyBonus==null&&facts.ProficiencyContribution(0)==0
                    &&facts.BaseArmorClass==10&&facts.AbilityModifier(CharacterAbility.Strength)==1
                    &&facts.AbilityModifier(CharacterAbility.Dexterity)==2&&facts.AbilityModifier(CharacterAbility.Constitution)==2,
                    "Printed creature facts acquired phantom levels/PB or character AC.");
                bool absent=false;try{facts.ProficiencyContribution(1);}catch(InvalidOperationException){absent=true;}
                Require(absent,"An unknown creature proficiency was supplied as zero or inferred from Claw.");
                var commands=new List<Command>();
                string Fingerprint(Command c)=>(string)typeof(Command).GetProperty("Fingerprint",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(c);
                foreach(var kind in new[]{CommandKind.AttackCreatureFeature,CommandKind.RespondOpportunityAttack})
                    foreach(var press in new[]{PressHitInstruction.ArmOrReplace,PressHitInstruction.KeepExisting}) {
                        var c=new Command("ferry.payload."+commands.Count,FerryWraithProfile.Actor,0,kind,"TEST_ONLY.target",
                            combat:new CombatRequest("TEST_ONLY.turn",knockout:AttackKnockoutMode.AskIfEligible,
                                choice:kind==CommandKind.RespondOpportunityAttack,pressInstruction:press,featureId:FerryWraithProfile.Feature));
                        var read=CommandHistory.Read(new CommandReceipt{Principal=c.Actor,Id=c.Id,Revision=1,Fingerprint=Fingerprint(c)});
                        Require(Fingerprint(read)==Fingerprint(c)&&read.Kind==kind&&read.Combat.FeatureId==FerryWraithProfile.Feature
                            &&read.Combat.WeaponId==""&&read.Combat.PressInstruction==press
                            &&read.Combat.Knockout==AttackKnockoutMode.AskIfEligible&&read.Combat.Choice==c.Combat.Choice,
                            "Source attack receipt lost its feature, knockout, Press or opportunity choice.");
                        commands.Add(c);
                    }
                bool mixed=false;try{new CombatRequest("TEST_ONLY.turn","TEST_ONLY.club",featureId:FerryWraithProfile.Feature);}
                catch(ArgumentException){mixed=true;}Require(mixed,"Natural source accepted a held-weapon payload.");
                BishopCheckpoint(session,directory,"ferry-genesis-source");
                Require(before.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Detached source probes changed the live session.");
                File.WriteAllText(Path.Combine(directory,"source-payloads.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Fresh actual genesis/restore plus detached command receipt controls; no creature encounter admission",commands}));
            });
            cases.Add("tac10_ferry_typed_defenses_settle_actual_life_mechanical",()=>{
                var session=NewFerryExpedition();var ready=ShortRestCapture(session);var beforeBytes=new SnapshotCodec().Encode(ready);
                var damage=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules")
                    .GetMethod("Damage",BindingFlags.Static|BindingFlags.NonPublic);
                var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                var results=new List<object>();
                var controls=new[]{("necrotic",false,false,5L,2L),("necrotic",true,false,5L,2L),
                    ("poison",false,false,5L,0L),("poison",true,false,5L,0L),("fire",false,false,4L,4L),
                    ("fire",true,false,5L,2L),("corruption",true,false,4L,4L),("necrotic",true,true,7L,1L)};
                foreach(var control in controls) {
                    var s=ready.Copy();if(control.Item2)FerryMechanicalCondition(s,"Petrified");
                    var life=s.Lives.Single(x=>x.ActorId==FerryWraithProfile.Actor);
                    if(control.Item1=="poison") {
                        // Explicit supplied temporary HP, confined to this mechanical control.
                        life=new ActorLifeRecord(life.ActorId,9,9,3,Array.Empty<int>(),false,false,false,0,0,null,0,false,Array.Empty<string>());
                        s.Lives=s.Lives.Select(x=>x.ActorId==life.ActorId?life:x).ToArray();
                    }
                    uint random=s.RandomState;
                    var defense=SharedTypedDamage.Resolve(s,"mechanical.damage",life.ActorId,control.Item1,control.Item4,control.Item3);
                    var rolled=(RolledDamage)damage.Invoke(null,new object[]{s,life,defense.EventId,defense.Effective,s.RuleClock,random,
                        2,false,false,false,KnockoutInstruction.OrdinaryOutcome,false});
                    apply.Invoke(null,new object[]{s,life,rolled.Outcome.State});s.RandomState=rolled.NextRandomState;
                    var after=s.Lives.Single(x=>x.ActorId==life.ActorId);
                    Require(defense.Effective==control.Item5&&after.Hp==9-control.Item5&&after.TemporaryHp==life.TemporaryHp,
                        "Shared typed defense/life settlement violated the independently derived source amount.");
                    Require(s.TypedDamage.Length==1&&s.TypedDamage[0]==defense,"Damage boundary evidence was omitted or duplicated.");
                    if(control.Item1=="poison")Require(after.Hp==9&&after.TemporaryHp==3&&s.RandomState==random
                        &&rolled.WordsConsumed==0&&after.LinkedInjuries.Count==0,"Immune damage consumed life, temporary HP or damage-triggered RNG.");
                    results.Add(new{defense,after,rolled.WordsConsumed,rolled.NextRandomState});
                }
                var unsupported=ready.Copy();bool rejected=false;
                try{SharedTypedDamage.Resolve(unsupported,"mechanical.unknown",FerryWraithProfile.Actor,"Poison",5);}
                catch(ArgumentException){rejected=true;}
                Require(rejected&&unsupported.TypedDamage.Length==0&&unsupported.RandomState==ready.RandomState,
                    "Unknown damage label bypassed a known defense or mutated state.");
                Require(beforeBytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Mechanical controls changed the genuine session.");
                File.WriteAllText(Path.Combine(directory,"typed-life-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached supplied damage/condition/tempHP events through shared typed, Aura/life and ApplyLife pipelines; not a connected attack or supported save",results}));
            });
        }
    }
}
#endif
