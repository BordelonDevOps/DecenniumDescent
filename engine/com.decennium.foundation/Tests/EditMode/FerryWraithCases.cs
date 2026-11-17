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
        private static void FerryMechanicalCondition(Snapshot s,string kind,string actor=FerryWraithProfile.Actor)
        {
            var journal=s.Conditions.Single(x=>x.Target==actor);
            var history=ConditionHistory.Restore(journal).Append(ConditionOperation.Apply("ferry.mechanical.apply."+kind,
                journal.Now,new ConditionApplicationData("ferry.mechanical."+kind,"TEST_ONLY.owner","TEST_ONLY.supplied-event",
                    kind,null,"supplied-end",true))).State;
            s.Conditions=s.Conditions.Select(x=>x.Target==journal.Target?history.Journal:x).ToArray();
        }
        private static void AddFerryWraithCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("tac10_petrified_poison_immunity_retains_event_condition_provenance",()=>{
                // Supplied poison packets, temporary HP and condition events on detached states.
                // No new connected poison/Petrified producer or supported mechanical save is claimed.
                var session=NewFerryExpedition();var initial=ShortRestCapture(session);var codec=new SnapshotCodec();
                var unchanged=codec.Encode(initial);var rows=new List<object>();
                var damage=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules")
                    .GetMethod("Damage",BindingFlags.Static|BindingFlags.NonPublic);
                var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                void Operation(Snapshot s,string actor,Func<ConditionJournal,ConditionOperation> operation) {
                    var journal=s.Conditions.Single(x=>x.Target==actor);
                    var next=ConditionHistory.Restore(journal).Append(operation(journal)).State.Journal;
                    s.Conditions=s.Conditions.Select(x=>x.Target==actor?next:x).ToArray();
                }
                foreach(string actor in new[]{FerryWraithProfile.Hero,FerryWraithProfile.Actor})
                    foreach(string mode in new[]{"absent","active","suppressed","parent-immune","ended","incapacitated-immune"})
                        foreach(bool rolledPacket in new[]{false,true}) {
                            var s=initial.Copy();bool innate=actor==FerryWraithProfile.Actor;
                            if(mode!="absent")FerryMechanicalCondition(s,"Petrified",actor);
                            if(mode=="suppressed")Operation(s,actor,j=>ConditionOperation.Suppress("probe.suppress",j.Now,"ferry.mechanical.Petrified",true));
                            if(mode=="ended")Operation(s,actor,j=>ConditionOperation.End("probe.end",j.Now,"ferry.mechanical.Petrified","supplied-end"));
                            if(mode=="parent-immune"||mode=="incapacitated-immune")Operation(s,actor,j=>ConditionOperation.Grant("probe.grant",j.Now,
                                new ConditionImmunityData("probe.immunity","TEST_ONLY.owner","TEST_ONLY.supplied-event",
                                    new[]{mode=="parent-immune"?"Petrified":"Incapacitated"},null,"supplied-end")));
                            var view=TestOnlyClubAttackPolicy.ConditionsFor(s,actor).View();
                            bool operative=mode=="active"||mode=="incapacitated-immune";
                            Require(view.Has(ConditionKind.Petrified)==operative,"Unexpected actual Petrified component state.");
                            if(mode=="incapacitated-immune")Require(!view.Has(ConditionKind.Incapacitated),"Inherited component was not independently suppressed.");
                            var old=s.Lives.Single(x=>x.ActorId==actor);
                            var life=new ActorLifeRecord(actor,old.MaximumHp,8,3,Array.Empty<int>(),false,false,old.UsesDeathSaves,0,0,null,0,false,old.HeldItems);
                            s.Lives=s.Lives.Select(x=>x.ActorId==actor?life:x).ToArray();
                            uint before=s.RandomState,afterRoll=before;long raw=4,sourceWords=0;
                            if(rolledPacket){var die=DiceStream.Draw(before,4);raw=die.Value+1;afterRoll=die.NextState;sourceWords=die.WordsConsumed;s.RandomState=afterRoll;}
                            var resolved=SharedTypedDamage.Resolve(s,"probe.poison",actor,"poison",raw);
                            long expected=innate||operative?0:raw;
                            Require(resolved.Effective==expected&&resolved.Petrified==operative
                                &&resolved.ImmunitySource==(innate?FerryWraithProfile.SourceId:operative?TypedDamageRecord.PetrifiedPoisonSource:""),
                                "Poison immunity was conflated with resistance, innate immunity or the Poisoned condition.");
                            var settled=(RolledDamage)damage.Invoke(null,new object[]{s,life,resolved.EventId,resolved.Effective,s.RuleClock,afterRoll,
                                0,false,false,false,KnockoutInstruction.OrdinaryOutcome,false});
                            apply.Invoke(null,new object[]{s,life,settled.Outcome.State});s.RandomState=settled.NextRandomState;
                            var after=s.Lives.Single(x=>x.ActorId==actor);
                            Require(after.Hp==8-Math.Max(0,expected-3)&&after.TemporaryHp==Math.Max(0,3-expected)
                                &&s.RandomState==afterRoll&&settled.WordsConsumed==0&&s.TypedDamage.Length==1,
                                "Poison protection changed the actual HP/tempHP or consumed damage-triggered RNG.");
                            SharedTypedDamage.ValidateConditionHistory(s);
                            if(operative) {
                                Operation(s,actor,j=>ConditionOperation.End("probe.later.end",j.Now,"ferry.mechanical.Petrified","supplied-end"));
                                Require(!TestOnlyClubAttackPolicy.ConditionsFor(s,actor).View().Has(ConditionKind.Petrified),"Later ending failed.");
                                SharedTypedDamage.ValidateConditionHistory(s);
                                var forged=s.Copy();forged.TypedDamage=new[]{new TypedDamageRecord(resolved.EventId,resolved.Revision,resolved.At,
                                    actor,"poison",raw,raw,false,"",innate?FerryWraithProfile.SourceId:"",false,resolved.ConditionOperationCount)};
                                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(forged));
                            } else {
                                var forged=s.Copy();forged.TypedDamage=new[]{new TypedDamageRecord(resolved.EventId,resolved.Revision,resolved.At,
                                    actor,"poison",raw,raw,false,"",TypedDamageRecord.PetrifiedPoisonSource,true,resolved.ConditionOperationCount,
                                    new[]{"ferry.mechanical.Petrified"})};
                                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(forged));
                            }
                            rows.Add(new{actor,mode,rolledPacket,raw,sourceWords,before,afterRoll,resolved,after,settled.WordsConsumed});
                        }
                var legacy=ShortRestCapture(NewDeclaredGeometryExpedition());FerryMechanicalCondition(legacy,"Petrified",FerryWraithProfile.Hero);
                var oldResult=SharedTypedDamage.Resolve(legacy,"probe.legacy",FerryWraithProfile.Hero,"poison",4);
                Require(oldResult.Effective==2&&legacy.TypedDamage.Length==0,"Supported predecessor behavior was changed by the selected correction.");
                Require(unchanged.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Detached condition controls changed the genuine session.");
                File.WriteAllText(Path.Combine(directory,"petrified-poison-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="24 labeled shared-pipeline controls; actual condition ledger, event-prefix validation, life/tempHP and RNG; no new connected producer",rows,
                    legacyEffective=oldResult.Effective}));
            });
            cases.Add("tac10_ferry_paid_current_epoch_admission_from_fresh_campaign",()=>{
                // Re-execute the genuine acquire/manage/prepare/recovery prefix in the new
                // selected profile. Never adopt an old save or replace its life/RNG state.
                var session=RunDeclaredGeometryCampaign(directory,NewFerryExpedition());
                const string hero=FerryWraithProfile.Hero,companion=FerryWraithProfile.Companion;
                int sequence=0;
                void Walk(string actor,int dx,int dy) {
                    var before=ShortRestCapture(session);var body=before.Actors.Single(x=>x.Id==actor);
                    int speed=checked((int)TestOnlyClubAttackPolicy.WalkingSpeed(before,actor));
                    BishopCommit(session,new Command("ferry.approach."+(++sequence),actor,before.Revision,CommandKind.BeginWorldStep,"walk",dx,dy));
                    ClericCommit(session,hero,CommandKind.AdvanceClock,x:30,y:speed);
                    var after=ShortRestCapture(session);var moved=after.Actors.Single(x=>x.Id==actor);
                    Require(moved.X==body.X+dx&&moved.Y==body.Y+dy&&!after.WorldTraversals.Any(x=>x.ActorId==actor),
                        "Ferry approach did not complete its actual paid edge.");
                }
                for(int step=0;step<5;step++)Walk(companion,1,0);
                Walk(companion,0,-1);Walk(hero,1,0);Walk(hero,0,-1);
                var staged=ShortRestCapture(session);var prior=staged.PostRecoveryEncounter.Admission.Epoch;
                int actualSpeed=checked((int)TestOnlyClubAttackPolicy.WalkingSpeed(staged,hero));
                long slot=prior.SlotAt(staged.RuleClock);
                RuleTime Departure(long local) {
                    var arrival=prior.Start(local);
                    return new RuleTime(checked(arrival.Numerator*actualSpeed-30L*arrival.Denominator),checked(arrival.Denominator*actualSpeed));
                }
                while(prior.Order[(int)(slot%prior.Order.Count)]!=PostRecoveryEncounterDefinition.Actor||Departure(slot)<staged.RuleClock)slot++;
                PostRecoveryAdvanceTo(session,Departure(slot));
                BishopCheckpoint(session,directory,"ferry-before-paid-contact");
                var beforeContact=ShortRestCapture(session);Walk(hero,0,1);
                var admitted=ShortRestCapture(session);var admission=admitted.FerryWraith.Admission;
                Require(admission!=null&&admitted.Encounter.Id==FerryWraithProfile.Encounter
                    &&admission.PreviousPartyEpochId==prior.Id&&admission.PriorDefenderLocalStart==slot
                    &&admission.Epoch.Origin==prior.Start(slot)&&admitted.FerryWraith.Contacts.Count==1,
                    "Paid Ferry contact did not enter at the actual post-recovery nonparty Start.");
                Require(admitted.Creatures.Single().ActorId==FerryWraithProfile.Actor
                    &&admitted.Lives.Single(x=>x.ActorId==FerryWraithProfile.Actor).Hp==9
                    &&admitted.ResonancePools.Select(x=>(x.ActorId,x.Current,x.Maximum))
                        .SequenceEqual(beforeContact.ResonancePools.Select(x=>(x.ActorId,x.Current,x.Maximum)))
                    &&admitted.ConvictionBalance.Current==beforeContact.ConvictionBalance.Current,
                    "Ferry entry replaced the creature or granted party resources.");
                BishopCheckpoint(session,directory,"ferry-admitted");
                var restored=ShortRestCapture(session);
                Require(new SnapshotCodec().Encode(admitted).SequenceEqual(new SnapshotCodec().Encode(restored)),
                    "Ferry admission changed across verified restore and deterministic replay.");
                File.WriteAllText(Path.Combine(directory,"ferry-paid-admission.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Genuine new-profile prefix and nine paid approach edges; creature combat and seal qualification remain pending",
                    admitted.Revision,admitted.RuleClock,admitted.FerryWraith,admitted.WorldIntervals,admitted.BonusActions,
                    admitted.ResonancePools,admitted.ConvictionBalance,admitted.RandomState}));
            });
            cases.Add("tac10_damage_order_preserves_source_save_flat_resistance_and_life",()=>{
                // Earn the existing shield source through real predecessor commands. The following
                // damage packets/Petrified applications are explicitly supplied mechanical controls.
                var simulation=World(DefensiveFormationPolicy());AdvanceSoldierToDefensiveFormation(simulation);BeginEncounter(simulation);
                var ready=simulation.Capture();const string actor=TestOnlyPolicy.ActorId;
                Require(CharacterAdvancementRules.ReduceIncomingDamage(ready,actor,10)==9,"Actual Shield Trained reduction was not established.");
                var damage=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules")
                    .GetMethod("Damage",BindingFlags.Static|BindingFlags.NonPublic);
                var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                long[] noSave={0,0,1,2,3,4,5,6},saved={0,0,0,0,1,1,2,2};var rows=new List<object>();
                foreach(bool half in new[]{false,true})foreach(bool stone in new[]{false,true})for(int raw=0;raw<=7;raw++) {
                    var s=ready.Copy();if(stone)FerryMechanicalCondition(s,"Petrified",actor);
                    var life=s.Lives.Single(x=>x.ActorId==actor);long afterFlat=(half?saved:noSave)[raw];
                    long effective=stone?afterFlat/2:afterFlat;
                    var resolved=SharedTypedDamage.Resolve(s,"mechanical.ordered",actor,"fire",raw,half);
                    var rolled=(RolledDamage)damage.Invoke(null,new object[]{s,life,resolved.EventId,resolved.Effective,s.RuleClock,s.RandomState,
                        0,false,false,false,KnockoutInstruction.OrdinaryOutcome,false});
                    apply.Invoke(null,new object[]{s,life,rolled.Outcome.State});
                    Require(resolved.Raw==raw&&resolved.AfterSave==(half?raw/2:raw)&&resolved.AfterFlatReduction==afterFlat
                        &&resolved.Effective==effective&&s.Lives.Single(x=>x.ActorId==actor).Hp==life.Hp-effective,
                        "Source save/flat/resistance order or zero-floor life settlement changed.");
                    rows.Add(new{half,stone,resolved,afterHp=s.Lives.Single(x=>x.ActorId==actor).Hp});
                }
                bool malformed=false;try{new TypedDamageRecord("mechanical.wrong-order",1,ready.RuleClock,actor,"fire",5,4,true,"","",false);}
                catch(ArgumentException){malformed=true;}Require(malformed,"Typed damage accepted a flat-stage amount larger than the already halved packet.");
                File.WriteAllText(Path.Combine(directory,"ordered-damage-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Real earned Shield Trained source plus detached supplied packets through actual typed, flat-reduction and life pipelines; not a new connected producer",rows}));
            });
            cases.Add("tac10_ferry_shared_untrained_checks_and_actual_initiative",()=>{
                var session=NewFerryExpedition();var state=ShortRestCapture(session);var original=new SnapshotCodec().Encode(state);
                const string actor=FerryWraithProfile.Actor;
                var perception=CharacterStateFacts.ForActor(state,actor,"perception");
                var stealth=AbilityCheckRules.Derive(state,actor,"stealth",CharacterAbility.Dexterity);
                Require(perception.Training==null&&perception.ProficiencyRank==0&&perception.Numeric.ProficiencyBonus==null
                    &&perception.TotalWithInjury(CharacterAbility.Wisdom,perception:true)==0
                    &&stealth.AbilityModifier==2&&stealth.ProficiencyBonus==0&&stealth.Total==2,
                    "Generic creature checks inferred training/PB or lost source ability modifiers.");
                bool strict=false;try{var unused=perception.Rules.TotalLevel;}catch(InvalidOperationException){strict=true;}
                Require(strict,"Character-only level accessor fabricated a class for the creature.");
                var supplied=state.Copy();var before=supplied.Lives.Single(x=>x.ActorId==actor);
                supplied.Lives=supplied.Lives.Select(x=>x.ActorId==actor?new ActorLifeRecord(actor,9,9,0,
                    new[]{(int)Injury.Concussion,(int)Injury.CognitiveTrauma},false,false,false,0,0,null,0,false,Array.Empty<string>()):x).ToArray();
                var injured=CharacterStateFacts.ForActor(supplied,actor,"perception");
                Require(injured.TotalWithInjury(CharacterAbility.Wisdom,perception:true)==-1,
                    "Overlapping source injuries stacked or were ignored on creature perception.");
                var rollMethod=typeof(TestOnlySharedWorldPolicy).GetMethod("RollWorldInitiative",BindingFlags.NonPublic|BindingFlags.Static);
                uint random=supplied.RandomState;var expected=PlaytestDice.RollD20(random);
                var rolled=(LaterInitiativeDraw)rollMethod.Invoke(null,new object[]{supplied,actor});
                Require(rolled.DexterityModifier==2&&rolled.Bonus==-1&&rolled.Natural==expected.Natural
                    &&supplied.RandomState==expected.NextRandomState&&rolled.WordsConsumed==expected.WordsConsumed,
                    "Actual shared initiative did not use source DEX, one injury penalty and the owned RNG draw.");
                Require(original.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Detached numeric control changed live gameplay.");
                File.WriteAllText(Path.Combine(directory,"creature-checks.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Actual fresh source facts and detached supplied-injury execution of the shared initiative producer; not encounter admission",stealth,rolled}));
            });
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
