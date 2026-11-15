#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.IO;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewCastingExpedition()=>ConnectedExpeditionSession.StartWithClericCasting(
            ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());
        private static Simulation CastingSimulation(ConnectedExpeditionSession session)=>(Simulation)typeof(ConnectedExpeditionSession)
            .GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
        private static Authority CastingAuthority()=>new Authority("TEST_ONLY.host",new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor},
            inventoryOwners:new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor},willingRecipients:new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor});
        private static ConnectedExpeditionSession CastingFirstOwnTurn(bool selectStance=true)
        {
            var session=StartVialScenario(NewCastingExpedition()); const string hero=ConnectedExpeditionSession.Hero,ally=ClericRpProfile.Actor;
            ClericCommit(session,ally,CommandKind.BeginWorldStep,"walk",-1);
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
            ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",-1);
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:12,y:1);
            ClericCommit(session,ally,CommandKind.BeginReinforcementApproach,"TEST_ONLY.companion-reinforcement.v1");
            ClericGuard(session,hero); ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:2);
            ClericDefender(session); ClericEnd(session,hero); ClericDefender(session);
            Require(ShortRestCapture(session).Reinforcement.Admission!=null,"The caster must enter by genuine paid reinforcement.");
            if(selectStance)ClericGuard(session,ally);return session;
        }
        private static void AddSpellCastingCases(Dictionary<string, Action> cases,string directory)
        {
            cases.Add("tac08_detached_purify_batches_contamination_and_enclosure", () => {
                var session=CastingFirstOwnTurn();var before=ShortRestCapture(session);var policy=ClericPolicy(session);
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero,water=SpellCastingProfile.ContaminatedWaterId;
                Command Cast(string id,string target)=>new Command(id,actor,before.Revision,CommandKind.CastKnownSpell,target,
                    spellCast:new SpellCastRequest("purify-food-and-drink",SpellCastingProfile.FocusId));
                var command=Cast("detached.purify.mixed",water);var mixed=before.Copy();
                mixed.ConsumableContamination=Enum.GetValues(typeof(ConsumableContaminationKind)).Cast<ConsumableContaminationKind>()
                    .Select(k=>new ConsumableContaminationRecord("detached.taint."+(int)k,water,"detached.initial",0,k)).ToArray();
                string lots=System.Text.Json.JsonSerializer.Serialize(mixed.Work.Lots),meta=System.Text.Json.JsonSerializer.Serialize(mixed.InventoryLots);
                Require(policy.Resolve(mixed,command)==null&&mixed.ConsumableContamination.All(x=>x.Purifiable?!x.Present:x.Present)
                    &&mixed.ConsumableContamination.Count(x=>!x.Present)==3&&SpellCastingProfile.HasUnsafeContamination(mixed,water)
                    &&mixed.ResonancePools.Single().Current==1&&mixed.RandomState==before.RandomState
                    &&lots==System.Text.Json.JsonSerializer.Serialize(mixed.Work.Lots)&&meta==System.Text.Json.JsonSerializer.Serialize(mixed.InventoryLots),
                    "Actual Purify must remove only the three eligible categories, preserve residual hazard, stock, custody and freshness, and yield no reagent.");
                var clean=before.Copy();clean.ConsumableContamination=Array.Empty<ConsumableContaminationRecord>();
                Require(policy.Resolve(clean,Cast("detached.purify.clean",water))==null&&clean.ResonancePools.Single().Current==1
                    &&clean.ConsumableContamination.Length==0&&clean.RandomState==before.RandomState,
                    "A valid clean batch must still admit a paid no-removal cast.");
                var split=before.Copy();split.ConsumableContamination=Array.Empty<ConsumableContaminationRecord>();
                OrdinaryInventory.Descendant(split,water,"detached.purify.water-child",new RuleQuantity(1,2),TestOnlyFillingPolicy.FlaskId,actor,InventoryAccess.Ready);
                string Stocks(Snapshot s)=>string.Join("|",s.Work.Lots.Select(x=>x.Id+":"+x.Amount+":"+x.LocationId+":"+x.CustodianId));
                string splitBefore=Stocks(split);
                Require(policy.Resolve(split,Cast("detached.purify.unseparated",water))=="PurifyBatchNotSeparated"
                    &&splitBefore==Stocks(split)&&split.RandomState==before.RandomState
                    &&split.SpellCasts.Length==0&&split.ResonancePools.Single().Current==3,
                    "Two physical content lots in one continuous vessel are not separately selectable batches.");
                var food=before.Copy();const string foodId="detached.purify.food-five-pounds";
                OrdinaryInventory.Descendant(food,PortableKitFixture.Rations,foodId,new RuleQuantity(5),hero,hero,InventoryAccess.Ready);
                var separated=food.Copy();var foodMeta=food.InventoryLots.Single(x=>x.LotId==foodId);
                Require(policy.Resolve(food,Cast("detached.purify.food",foodId))==null&&food.ResonancePools.Single().Current==1
                    &&food.Work.Lots.Single(x=>x.Id==foodId).Amount==new RuleQuantity(5)
                    &&food.InventoryLots.Single(x=>x.LotId==foodId).FreshUntil==foodMeta.FreshUntil,
                    "A physically separated five-pound food batch must be eligible without a freshness reset.");
                var enclosed=separated.Copy();enclosed.PortableEquipment=enclosed.PortableEquipment.Select(x=>x.LinkedId==foodId
                    ?x.With(parentId:PortableKitFixture.Pack,placement:PortablePlacement.Contained)
                    :x.Id==PortableKitFixture.Pack?x.With(open:false):x).ToArray();
                Require(policy.Resolve(enclosed,Cast("detached.purify.enclosed",foodId))=="PurifyBatchEnclosed"
                    &&enclosed.SpellCasts.Length==0&&enclosed.ResonancePools.Single().Current==3,
                    "A closed enclosing pack must block targeting its contained food before payment.");
                Require(policy.Resolve(before.Copy(),Cast("detached.purify.oversized",PortableKitFixture.Rations))=="PurifyBatchUnsupported",
                    "A twenty-pound lot must not be implicitly portioned by casting.");
                File.WriteAllText(Path.Combine(directory,"tac08-detached-purify-batches.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached category/placement setup and actual portion/cast producers; no campaign contamination acquisition or supported-save claim",
                    contamination=mixed.ConsumableContamination,food=food.Work.Lots.Single(x=>x.Id==foodId),freshUntil=foodMeta.FreshUntil?.ToString(),
                    cleanPaid=clean.ResonancePools.Single().Current,splitRejected="PurifyBatchNotSeparated",enclosedRejected="PurifyBatchEnclosed"}));
            });
            cases.Add("tac08_detached_damage_zero_temporary_hp_and_save_capacity", () => {
                var session=CastingFirstOwnTurn();const string actor=ClericRpProfile.Actor;
                CommitVialRoute(session,new Command("tac08.packet.actual-concentration",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                var paid=ShortRestCapture(session);var settle=typeof(TestOnlySharedWorldPolicy).GetMethod("SettleSpellDamage",BindingFlags.Static|BindingFlags.NonPublic);
                var zero=paid.Copy();var codec=new SnapshotCodec();byte[] zeroBefore=codec.Encode(zero);
                settle.Invoke(null,new object[]{zero,actor,FrightenedProfile.Actor,"detached.damage.zero",0L,true});
                Require(zeroBefore.SequenceEqual(codec.Encode(zero)),"Zero resolved damage must draw no CON die or end any effect.");
                var candidate=paid.Copy();var life=candidate.Lives.Single(x=>x.ActorId==actor);
                var tempLife=new LifeState(life.MaximumHp,life.Hp,temporaryHp:4);
                var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                apply.Invoke(null,new object[]{candidate,life,tempLife});life=candidate.Lives.Single(x=>x.ActorId==actor);
                var packet=PlaytestDamageDice.Resolve(ActorLifeRules.ReadForResolution(candidate,life),2,candidate.RuleClock,candidate.RandomState);
                candidate.RandomState=packet.NextRandomState;apply.Invoke(null,new object[]{candidate,life,packet.Outcome.State});
                settle.Invoke(null,new object[]{candidate,actor,FrightenedProfile.Actor,"detached.damage.temp",2L,true});
                Require(candidate.Lives.Single(x=>x.ActorId==actor).Hp==life.Hp&&candidate.Lives.Single(x=>x.ActorId==actor).TemporaryHp==2
                    &&candidate.SpellSaves.Length==1&&candidate.SpellSaves.Single().Damage==2&&candidate.SpellSaves.Single().Dc==10
                    &&candidate.SpellSaves.Single().RandomBefore==packet.NextRandomState,
                    "A positive packet absorbed entirely by temporary HP must still produce one CON save after life settlement.");
                var capacity=typeof(TestOnlySharedWorldPolicy).GetMethod("SpellDamageCapacityFailure",BindingFlags.Static|BindingFlags.NonPublic);
                var bounded=paid.Copy();bounded.SpellSaves=Enumerable.Repeat(candidate.SpellSaves.Single(),SpellCastingProfile.MaxSaves-1).ToArray();
                Require(capacity.Invoke(null,new object[]{bounded,actor,0})==null
                    &&(string)capacity.Invoke(null,new object[]{bounded,actor,1})=="CastingHistoryFull",
                    "The pure bound check must reserve both an admission WIS and a possible CON before rolling either.");
                ClericEnd(session,actor);ClericGuard(session,ConnectedExpeditionSession.Hero);
                var attackBefore=ShortRestCapture(session);Snapshot knockout=null;uint knockoutSeed=0;
                // Explicit detached low-HP/seed setup. Use the actual full attack resolver,
                // including Sanctuary admission, payment, retained pending choice and completion.
                for(uint seed=1;seed<=128&&knockout==null;seed++) {
                    var trial=attackBefore.Copy();var target=trial.Lives.Single(x=>x.ActorId==actor);
                    apply.Invoke(null,new object[]{trial,target,new LifeState(target.MaximumHp,1)});trial.RandomState=seed;
                    var attack=new Command("detached.damage.knockout-attack",ConnectedExpeditionSession.Hero,trial.Revision,CommandKind.AttackClub,actor,
                        combat:new CombatRequest(trial.Encounter.CurrentTurnId,TestOnlyClubAttackPolicy.ActorClub,knockout:AttackKnockoutMode.AskIfEligible));
                    string result=ClericPolicy(session).Resolve(trial,attack);
                    if(result==null&&trial.MeleeAttacks.Any(x=>x.Pending)){knockout=trial;knockoutSeed=seed;}
                }
                Require(knockout!=null,"The detached full attack producer did not reach a lawful pending knockout.");
                var pending=knockout.MeleeAttacks.Single(x=>x.Pending);
                Require(knockout.SpellEffects.Single().Present&&knockout.SpellSaves.All(x=>x.Kind!=SpellSaveKind.ConcentrationConstitution)
                    &&knockout.Lives.Single(x=>x.ActorId==actor).Hp==1,
                    "Pending knockout must defer life/concentration settlement and its CON die.");
                knockout.Revision++; // Simulate only the transaction boundary; no receipt or supported save is fabricated.
                var finish=new Command("detached.damage.knockout-finish",ConnectedExpeditionSession.Hero,knockout.Revision,CommandKind.ResolveKnockout,pending.Id,
                    combat:new CombatRequest(knockout.Encounter.CurrentTurnId,choice:true));
                Require(ClericPolicy(session).Resolve(knockout,finish)==null&&knockout.Lives.Single(x=>x.ActorId==actor).Stable
                    &&knockout.Lives.Single(x=>x.ActorId==actor).Hp==0&&knockout.SpellEffects.Single().EndReason==SpellEffectEndReason.Incapacitated
                    &&knockout.SpellSaves.All(x=>x.Kind!=SpellSaveKind.ConcentrationConstitution),
                    "Actual knockout completion must settle zero HP and end concentration without an unnecessary CON save.");
                uint completedRandom=knockout.RandomState;
                Require(ClericPolicy(session).Resolve(knockout,finish)=="NoPendingKnockout"&&knockout.RandomState==completedRandom,
                    "A completed knockout cannot settle the same damage or consume dice twice.");
                File.WriteAllText(Path.Combine(directory,"tac08-detached-damage-packets.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached temporary-HP, low-HP/seed and history-capacity setup; real damage/life/attack/knockout producers; no campaign grant, fabricated receipt or supported-save claim",
                    zeroUnchanged=true,packet=packet.Outcome.State,save=candidate.SpellSaves.Single(),capacityRejected=true,
                    knockoutSeed,pending,completed=knockout.MeleeAttacks.Single(x=>x.Id==pending.Id),concentration=knockout.SpellEffects.Single()}));
            });
            cases.Add("tac08_detached_component_range_sight_and_focus_preflight", () => {
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var session=CastingFirstOwnTurn();var baseline=ShortRestCapture(session);var policy=ClericPolicy(session);
                var witnesses=new List<object>();
                void Check(string label,Action<Snapshot> setup,string expected,string target=hero) {
                    var candidate=baseline.Copy();setup(candidate);var pools=candidate.ResonancePools;var intervals=candidate.WorldIntervals;
                    var effects=candidate.SpellEffects;var casts=candidate.SpellCasts;uint random=candidate.RandomState;
                    var command=new Command("detached.components."+label,actor,candidate.Revision,CommandKind.CastKnownSpell,target,
                        spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true));
                    string actual=policy.Resolve(candidate,command);
                    Require(actual==expected,"Actual casting preflight differed for detached "+label+": "+actual);
                    if(expected!=null)Require(ReferenceEquals(pools,candidate.ResonancePools)&&ReferenceEquals(intervals,candidate.WorldIntervals)
                        &&ReferenceEquals(effects,candidate.SpellEffects)&&ReferenceEquals(casts,candidate.SpellCasts)&&random==candidate.RandomState,
                        "A component/range/sight denial paid, rolled, or changed effects.");
                    witnesses.Add(new{label,expected,actual,cast=expected==null?candidate.SpellCasts.Last():null});
                }
                Check("range",s=>{s.Actors.Single(x=>x.Id==hero).X=20;s.Actors.Single(x=>x.Id==hero).Y=20;},"SpellTargetUnavailable");
                Check("sight",s=>{
                    var journal=s.Conditions.Single(x=>x.Target==actor);
                    var changed=CJApply(ConditionHistory.Restore(journal),"detached.blind","Blinded").State.Journal;
                    s.Conditions=s.Conditions.Select(x=>x.Target==actor?changed:x).ToArray();
                },"SpellTargetNotPerceived",actor);
                Check("dropped",s=>s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==SpellCastingProfile.FocusId
                    ?x.With(placement:PortablePlacement.Ground,groundX:1,groundY:3,heldHands:0):x).ToArray(),"SpellFocusUnavailable");
                Check("other-custodian",s=>s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==SpellCastingProfile.FocusId
                    ?x.With(custodianId:hero):x).ToArray(),"SpellFocusUnavailable");
                Check("worn-no-s-hand",s=>s.Clubs=s.Clubs.Concat(new[]{
                    new ClubInstance("detached.grip.one",TestOnlyClubAttackPolicy.ClubProfile,actor,actor,actor,0,0),
                    new ClubInstance("detached.grip.two",TestOnlyClubAttackPolicy.ClubProfile,actor,actor,actor,0,0)}).ToArray(),"SpellSomaticHandUnavailable");
                Check("held-s-f-same-hand",s=>{
                    s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==SpellCastingProfile.FocusId
                        ?x.With(placement:PortablePlacement.Carried,heldHands:1):x).ToArray();
                    s.Clubs=s.Clubs.Append(new ClubInstance("detached.other-hand",TestOnlyClubAttackPolicy.ClubProfile,actor,actor,actor,0,0)).ToArray();
                },null);
                File.WriteAllText(Path.Combine(directory,"tac08-detached-component-preflight.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached positions, condition and hand/custody facts through real cast preflight; no acquisition or supported-save claim",witnesses}));
            });
            cases.Add("tac08_genuine_sanctuary_success_cache_reaction_and_next_owner_start", () => {
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var session=CastingFirstOwnTurn();var authority=LaterDefenderController.DefenderAuthority();var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.cache.ward",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                SpellSaveRecord success=null;
                for(int round=0;round<8&&success==null;round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);ClericEnd(session,hero);
                    for(int step=0;step<12&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.AutomaticDefender;step++) {
                        var before=ShortRestCapture(session);var simulation=CastingSimulation(session);
                        var pending=before.SanctuaryAdmissions.SingleOrDefault(x=>x.Pending);
                        if(pending!=null) {
                            Require(simulation.Execute(authority,new Command("tac08.cache.forgo."+round,pending.ActorId,before.Revision,
                                CommandKind.RespondSanctuary,pending.Id,sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo)))
                                .Outcome==Outcome.Committed,"The genuine blocked attack could not be forgone.");
                            var forgone=ShortRestCapture(session);
                            Require(simulation.Execute(authority,new Command("tac08.cache.end."+round,pending.ActorId,forgone.Revision,
                                CommandKind.EndRegularTurn,forgone.Encounter.CurrentTurnId)).Outcome==Outcome.Committed,"The genuine defender could not end after forgo.");
                        } else Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"The real ward gate did not resolve.");
                    }
                    success=ShortRestCapture(session).SpellSaves.LastOrDefault(x=>x.Kind==SpellSaveKind.SanctuaryWisdom&&x.Success);
                }
                Require(success!=null&&ShortRestCapture(session).SpellEffects.Single().Present,
                    "A successful real ward save must occur while its generating Sanctuary remains active.");
                session.Save(Path.Combine(directory,"tac08-sanctuary-success-interval.ddsave"));
                ClericGuard(session,actor);ClericEnd(session,actor);ClericGuard(session,hero);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:1);
                var reactionBefore=ShortRestCapture(session);int saves=reactionBefore.SpellSaves.Length;
                Require(reactionBefore.TacticalMoves.Any(x=>x.Status==TacticalMoveStatus.AwaitingReactions),"The genuine departure must offer an actual opportunity attack.");
                session.Save(Path.Combine(directory,"tac08-sanctuary-success-before-reaction.ddsave"));
                ClericDefender(session);var reacted=ShortRestCapture(session);var attack=reacted.MeleeAttacks.Last();
                Require(reacted.SpellSaves.Length==saves&&attack.Opportunity&&attack.TargetId==hero
                    &&attack.Attack.RandomBefore==reactionBefore.RandomState,
                    "A real Reaction in the same successful attacker interval must reuse its gate and draw only its actual attack.");
                // Re-enter reach through actual movement so the next defender Action again
                // targets the warded hero, rather than its nearer unwarded companion.
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:2);
                ClericEnd(session,hero);
                for(int step=0;step<12&&ShortRestCapture(session).SpellSaves.Length==saves;step++)
                    Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"The next real defender Start did not reach its attack gate.");
                var refreshed=ShortRestCapture(session);var next=refreshed.SpellSaves.Last();
                Require(refreshed.SpellSaves.Length==saves+1&&next.Kind==SpellSaveKind.SanctuaryWisdom
                    &&next.EffectId==success.EffectId&&!next.AttackerTurn.SameAs(success.AttackerTurn)
                    &&next.AttackerTurn.LocalStart>success.AttackerTurn.LocalStart,
                    "Only the next actual attacker Start must refresh the same ward's admission save.");
                string path=Path.Combine(directory,"tac08-sanctuary-success-refreshed.ddsave");session.Save(path);
                var bytes=codec.Encode(refreshed);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Successful cache, Reaction reuse and actual refresh failed replay.");
            });
            cases.Add("tac08_genuine_sanctuary_offensive_damage_and_detached_hostile_save_producer", () => {
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var session=CastingFirstOwnTurn();var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.offense.sanctuary",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                var authority=LaterDefenderController.DefenderAuthority();bool missed=false,hostileControl=false,damaged=false;
                for(int round=0;round<10&&!damaged;round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);
                    Require(ShortRestCapture(session).SpellEffects.Single().Present,"The ward must still be active before the real offensive attempt.");
                    ClericCommit(session,hero,CommandKind.AttackClub,FrightenedProfile.Actor,
                        combat:new CombatRequest(session.View(ExpeditionSeat.Player).TurnId,"TEST_ONLY.actor-club"));
                    var attacked=ShortRestCapture(session);var attack=attacked.MeleeAttacks.Last();
                    damaged=attack.Attack.Hit&&attack.Damage.Total>0;
                    if(damaged) {
                        Require(attacked.SpellEffects.Single().EndReason==SpellEffectEndReason.SanctuaryDamage,
                            "Actual intentional positive damage must break the attacker's Sanctuary.");
                        break;
                    }
                    missed=true;Require(attacked.SpellEffects.Single().Present,"A real missed or zero-damage attack must preserve Sanctuary.");
                    ClericEnd(session,hero);
                    for(int step=0;step<12&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.AutomaticDefender;step++) {
                        var before=ShortRestCapture(session);var simulation=CastingSimulation(session);
                        var pending=before.SanctuaryAdmissions.SingleOrDefault(x=>x.Pending);
                        if(pending!=null) {
                            Require(simulation.Execute(authority,new Command("tac08.offense.forgo."+round,pending.ActorId,before.Revision,
                                CommandKind.RespondSanctuary,pending.Id,sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo)))
                                .Outcome==Outcome.Committed,"The actual defender must forgo its failed ward target before ending.");
                            var forgone=ShortRestCapture(session);
                            Require(simulation.Execute(authority,new Command("tac08.offense.defender-end."+round,pending.ActorId,forgone.Revision,
                                CommandKind.EndRegularTurn,forgone.Encounter.CurrentTurnId)).Outcome==Outcome.Committed,
                                "A trusted defender may end its own unspent regular turn after forgoing the blocked attack.");
                            continue;
                        }
                        var decision=new LaterDefenderController(simulation,ClericPolicy(session)).Plan(authority);
                        if(!hostileControl&&decision.Primary?.Kind==CommandKind.UseIntimidatingPresence) {
                            // The campaign cannot willingly ward this nonparty actor. Only the
                            // detached control substitutes the recipient, then invokes the real
                            // paid Presence producer and its real forced-saving-throw procedure.
                            var detached=before.Copy();var ward=detached.SpellEffects.Single();
                            detached.SpellEffects=new[]{new SpellEffectRecord(ward.Id,ward.CastId,ward.CastRevision,ward.SpellId,
                                ward.CasterId,FrightenedProfile.Actor,ward.StartedAt,ward.ExpiresAt,ward.ExpiryKind,ward.ExpiryTurn,true)};
                            var original=codec.Encode(before);
                            Require(ClericPolicy(session).Resolve(detached,decision.Primary)==null
                                &&detached.SpellEffects.Single().EndReason==SpellEffectEndReason.SanctuaryHostileSave
                                &&detached.FrightenedSaves.Length>before.FrightenedSaves.Length
                                &&original.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                                "The actual hostile-save producer must break the ward, without mutating the genuine campaign control.");
                            File.WriteAllText(Path.Combine(directory,"tac08-detached-sanctuary-hostile-save.json"),System.Text.Json.JsonSerializer.Serialize(new{
                                scope="DETACHED recipient substitution; no nonparty casting authority or campaign acquisition",effect=detached.SpellEffects.Single(),saves=detached.FrightenedSaves}));
                            hostileControl=true;
                        }
                        Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Actual defender continuation failed.");
                    }
                }
                File.WriteAllText(Path.Combine(directory,"tac08-sanctuary-offense-attempt.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    missed,damaged,hostileControl,attacks=ShortRestCapture(session).MeleeAttacks,effects=ShortRestCapture(session).SpellEffects}));
                Require(missed&&damaged&&hostileControl,"The genuine miss/positive-damage sequence and distinct hostile-save producer control must all execute: "
                    +"missed="+missed+", damaged="+damaged+", hostileControl="+hostileControl);
                var final=ShortRestCapture(session);string path=Path.Combine(directory,"tac08-sanctuary-offensive-break.ddsave");session.Save(path);
                var bytes=codec.Encode(final);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"The genuine offensive break failed independent replay.");
            });
            cases.Add("tac08_genuine_focused_sanctuary_retains_cast_dc_and_reaction_prohibition", () => {
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var session=CastingFirstOwnTurn(false);var before=ShortRestCapture(session);
                RetainClericDenial(CastingSimulation(session),CastingAuthority(),new Command("tac08.focused.no-stance",actor,before.Revision,
                    CommandKind.CastKnownSpell,hero,spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true,true)),
                    "StanceRequired",directory);
                ClericCommit(session,actor,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(session.View(ExpeditionSeat.Player).TurnId,stance:(int)CombatStance.Focused));
                before=ShortRestCapture(session);
                CommitVialRoute(session,new Command("tac08.focused.cast",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true,true)));
                var paid=ShortRestCapture(session);var cast=paid.SpellCasts.Single();
                Require(cast.FocusedDcElected&&cast.SpellDc==13&&paid.ResonancePools.Single().Current==1,
                    "Focused must apply its elected +1 exactly once at the real paid generating cast.");
                var reaction=typeof(TestOnlyClubAttackPolicy).GetMethod("CanReactToOrdinaryDeparture",BindingFlags.Static|BindingFlags.NonPublic);
                Require(!(bool)reaction.Invoke(null,new object[]{before,actor,FrightenedProfile.Actor})
                    &&!(bool)reaction.Invoke(null,new object[]{paid,actor,FrightenedProfile.Actor}),
                    "Spending Focused's DC benefit must not remove the stance's Reaction prohibition.");
                var detached=paid.Copy();detached.WorldIntervals=before.WorldIntervals;detached.ResonancePools=before.ResonancePools;
                Require(ClericPolicy(session).Resolve(detached,new Command("detached.focused.reelection",actor,detached.Revision,
                    CommandKind.CastKnownSpell,hero,spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true,true)))
                    =="FocusedSpellBenefitUnavailable","The same actual stance election cannot be consumed twice even in a detached unspent-budget control.");
                for(int round=0;round<5&&!ShortRestCapture(session).SanctuaryAdmissions.Any(x=>x.Pending);round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);ClericEnd(session,hero);
                    for(int step=0;step<12&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.AutomaticDefender;step++) {
                        Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Focused ward defender continuation failed.");
                        if(ShortRestCapture(session).SanctuaryAdmissions.Any(x=>x.Pending))break;
                    }
                }
                var pending=ShortRestCapture(session);
                Require(pending.SpellSaves.Any(x=>x.Kind==SpellSaveKind.SanctuaryWisdom)
                    &&pending.SpellSaves.Where(x=>x.Kind==SpellSaveKind.SanctuaryWisdom).All(x=>x.Dc==cast.SpellDc)
                    &&pending.SpellEffects.Single().Present,"Later automatic gates must retain the generating DC without breaking Sanctuary for its own save.");
                string path=Path.Combine(directory,"tac08-focused-sanctuary-pending.ddsave");session.Save(path);
                var codec=new SnapshotCodec();var bytes=codec.Encode(pending);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Focused DC and pending ward gate failed strict replay.");
            });
            cases.Add("tac08_detached_real_producer_concentration_replacement_incapacity_and_death", () => {
                const string actor=ClericRpProfile.Actor;
                var session=CastingFirstOwnTurn();var before=ShortRestCapture(session);var policy=ClericPolicy(session);
                CommitVialRoute(session,new Command("tac08.lifecycle.actual-concentration",actor,before.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                var paid=ShortRestCapture(session);var witnesses=new List<object>();
                // Explicitly detached setup restores the unspent budget solely to exercise
                // the normal paid replacement producer. It is never a supported save or a
                // claim that this finite campaign can afford two ranked casts.
                var replacement=paid.Copy();replacement.ResonancePools=before.ResonancePools;replacement.WorldIntervals=before.WorldIntervals;
                var replace=new Command("detached.lifecycle.replace",actor,replacement.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true));
                Require(policy.Resolve(replacement,replace)==null&&replacement.SpellEffects.Length==2
                    &&replacement.SpellEffects[0].EndReason==SpellEffectEndReason.Replaced&&replacement.SpellEffects[1].Present
                    &&replacement.ResonancePools.Single().Current==1&&replacement.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent,
                    "The actual paid cast producer must replace the prior concentration before creating its new effect.");
                witnesses.Add(new{control="DETACHED replacement with disclosed restored RP/Action",effects=replacement.SpellEffects});
                var appendCondition=typeof(TestOnlyClubAttackPolicy).GetMethod("AppendCondition",BindingFlags.Static|BindingFlags.NonPublic);
                foreach(bool held in new[]{false,true})foreach(string condition in new[]{"Incapacitated","Unconscious"}) {
                    var candidate=paid.Copy();
                    if(held)candidate.PortableEquipment=candidate.PortableEquipment.Select(x=>x.Id==SpellCastingProfile.FocusId
                        ?x.With(placement:PortablePlacement.Carried,heldHands:1):x).ToArray();
                    string application="detached.casting."+condition;
                    var operation=ConditionOperation.Apply(application,new ConditionStamp(candidate.RuleClock),
                        CJApp(application,condition),condition=="Unconscious"?application+".prone":"");
                    appendCondition.Invoke(null,new object[]{candidate,actor,operation});
                    var focus=candidate.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId);
                    bool drop=condition=="Unconscious"&&held;
                    Require(candidate.SpellEffects.Single().EndReason==SpellEffectEndReason.Incapacitated
                        &&candidate.Lives.Single(x=>x.ActorId==actor).Hp==paid.Lives.Single(x=>x.ActorId==actor).Hp
                        &&focus.HeldHands==(held&&!drop?1:0)&&focus.Placement==(drop?PortablePlacement.Ground:held?PortablePlacement.Carried:PortablePlacement.Worn)
                        &&candidate.RandomState==paid.RandomState&&candidate.SpellSaves.Length==0,
                        "The actual source-qualified condition consequences must distinguish concentration loss from held-equipment onset.");
                    witnesses.Add(new{control="DETACHED "+condition+" producer; held focus setup="+held,effect=candidate.SpellEffects.Single(),focus});
                    if(condition=="Unconscious"&&held) {
                        // A disclosed replacement held-item setup makes an accidental replay
                        // of the old onset observable. No such handling/acquisition is claimed.
                        candidate.PortableEquipment=candidate.PortableEquipment.Select(x=>x.Id==SpellCastingProfile.FocusId
                            ?x.With(placement:PortablePlacement.Carried,groundX:0,groundY:0,heldHands:1):x).ToArray();
                        appendCondition.Invoke(null,new object[]{candidate,actor,ConditionOperation.Suppress("detached.suppress",new ConditionStamp(candidate.RuleClock),application,true)});
                        appendCondition.Invoke(null,new object[]{candidate,actor,ConditionOperation.Suppress("detached.resume",new ConditionStamp(candidate.RuleClock),application,false)});
                        Require(candidate.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId).HeldHands==1
                            &&!candidate.SpellEffects.Single().Present,"Resumption must not replay the prior drop onset or restore concentration.");
                        string independent="detached.unconscious.independent";
                        appendCondition.Invoke(null,new object[]{candidate,actor,ConditionOperation.Apply(independent,new ConditionStamp(candidate.RuleClock),
                            CJApp(independent,"Unconscious"),independent+".prone")});
                        Require(candidate.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId).HeldHands==0,
                            "A new independent Unconscious application must still resolve its own actual drop onset once.");
                    }
                }
                var dead=paid.Copy();var life=dead.Lives.Single(x=>x.ActorId==actor);
                var damage=PlaytestDamageDice.Resolve(ActorLifeRules.ReadForResolution(dead,life),life.Hp+life.MaximumHp,dead.RuleClock,dead.RandomState);
                dead.RandomState=damage.NextRandomState;
                typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic)
                    .Invoke(null,new object[]{dead,life,damage.Outcome.State});
                typeof(TestOnlySharedWorldPolicy).GetMethod("SettleSpellDamage",BindingFlags.Static|BindingFlags.NonPublic)
                    .Invoke(null,new object[]{dead,actor,FrightenedProfile.Actor,"detached.lifecycle.damage",life.Hp+life.MaximumHp,true});
                Require(dead.Lives.Single(x=>x.ActorId==actor).Dead&&dead.SpellEffects.Single().EndReason==SpellEffectEndReason.Dead
                    &&dead.SpellSaves.Length==0&&dead.RandomState==damage.NextRandomState,
                    "Actual fatal damage settlement must end concentration before any unnecessary CON save.");
                witnesses.Add(new{control="DETACHED declared fatal packet through actual damage/life producers",effect=dead.SpellEffects.Single(),rng=dead.RandomState});
                File.WriteAllText(Path.Combine(directory,"tac08-detached-concentration-producers.json"),
                    System.Text.Json.JsonSerializer.Serialize(new{scope="Mechanical producer controls only; no campaign acquisition, funding, or supported-save claim",witnesses}));
            });
            cases.Add("tac08_actual_cast_authority_payload_and_source_denials", () => {
                var session=CastingFirstOwnTurn();var before=ShortRestCapture(session);var simulation=CastingSimulation(session);
                const string actor=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
                var host=CastingAuthority();int index=0;
                void Deny(string code,string spell="guidance",string target=actor,string focus="",bool willing=true,bool focused=false,
                    string caster=actor,Authority grant=null,int x=0,CombatRequest combat=null) {
                    var command=new Command("tac08.negative."+(++index),caster,before.Revision,CommandKind.CastKnownSpell,target,x,
                        combat:combat,spellCast:new SpellCastRequest(spell,focus,willing,focused));
                    RetainClericDenial(simulation,grant??host,command,code,directory);
                }
                Deny("NotAuthorized",target:hero,grant:new Authority("TEST_ONLY.caster-only",new[]{actor}));
                Deny("OrdinarySpellcastingUnsupported",caster:hero,target:hero);
                Deny("SpellNotKnown",spell:"detect-magic",focus:SpellCastingProfile.FocusId,willing:false);
                Deny("SpellClassAccessDenied",spell:"flare-spark");
                Deny("SpellClassLevelDenied",spell:"dispel-magic-lesser");
                Deny("SpellSourceAdmissionUnsupported",spell:"light");
                Deny("SpellFocusUnavailable",spell:"arcane-ward",focus:"TEST_ONLY.forged-focus");
                Deny("SpellWillingTargetSelectionRequired",willing:false);
                Deny("UnexpectedSpellFocusSelection",focus:SpellCastingProfile.FocusId);
                Deny("FocusedSpellBenefitUnavailable",spell:"sanctuary",focus:SpellCastingProfile.FocusId,focused:true);
                Deny("StabilizationTargetNotDying",spell:"spare-the-dying",willing:false);
                Deny("UnexpectedSpellCastPayload",x:1);
                Deny("UnexpectedCombatPayload",combat:new CombatRequest(session.View(ExpeditionSeat.Player).TurnId));
                var cast=new Command("tac08.negative.recipient-cast",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true));
                CommitVialRoute(session,cast);var after=ShortRestCapture(session);var codec=new SnapshotCodec();var bytes=codec.Encode(after);
                var casterOnly=new Authority("TEST_ONLY.host",new[]{actor});
                Require(!simulation.QueryCommand(casterOnly,cast).Admissible&&simulation.Execute(casterOnly,cast).Code=="NotAuthorized"
                    &&bytes.SequenceEqual(Bytes(simulation)),"A retained duplicate must still require its recipient authority.");
                var opponent=session.View(ExpeditionSeat.FirstOpponent);
                Require(opponent.Actors.Where(x=>x.Position.Id==hero||x.Position.Id==actor).All(x=>x.Casting==null),
                    "A noncontrolling seat received another actor's casting state or Guidance choice.");
                byte[] approval=System.Text.Encoding.UTF8.GetBytes(SpellCastingProfile.ApprovalResponse);
                var corrupted=(byte[])bytes.Clone();int offset=-1;
                for(int i=0;i<=corrupted.Length-approval.Length;i++)if(corrupted.Skip(i).Take(approval.Length).SequenceEqual(approval)){offset=i;break;}
                Require(offset>=0,"The wire must retain its exact actual approval binding.");corrupted[offset]=corrupted[offset]==(byte)'a'?(byte)'b':(byte)'a';
                Resign(corrupted);
                Throws<InvalidDataException>(()=>codec.Decode(corrupted));
                File.WriteAllBytes(Path.Combine(directory,"tac08-tampered-approval-rejected.ddsave"),corrupted);
            });
            cases.Add("tac08_genuine_strain_survives_actual_encounter_closure", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                Snapshot before=null;
                var session=EarnClericObjective(false,selected:NewCastingExpedition(),beforeClosure:campaign=>{
                    for(int repeat=0;repeat<2;repeat++) {
                        ClericEnd(campaign,hero);ClericDefender(campaign);ClericGuard(campaign,actor);
                        CommitVialRoute(campaign,new Command("tac08.closure.ward."+repeat,actor,ShortRestCapture(campaign).Revision,
                            CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)));
                        ClericEnd(campaign,actor);ClericGuard(campaign,hero);
                    }
                    before=ShortRestCapture(campaign);campaign.Save(Path.Combine(directory,"tac08-cadence-before-closure.ddsave"));
                    Require(before.CastingStrain.Single().Dissonance==1&&before.InventoryCombat,
                        "The closure witness must contain real positive strain before ending the encounter.");
                });
                var after=ShortRestCapture(session);
                Require(!after.InventoryCombat&&after.ClericObjective!=null&&after.CastingStrain.Single().Dissonance==1
                    &&after.CastingStrain.Single().LastCastRevision==before.CastingStrain.Single().LastCastRevision
                    &&after.ResonancePools.Single().Current==3,"Actual closure must preserve cadence and finite RP.");
                string path=Path.Combine(directory,"tac08-cadence-after-closure.ddsave");session.Save(path);
                var codec=new SnapshotCodec();var bytes=codec.Encode(after);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Closure cadence failed independent replay.");
            });
            cases.Add("tac08_genuine_cadence_grounding_advancement_and_passive_concentration", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=EarnClericObjective(false,selected:NewCastingExpedition());ReachClericOwnSlot(session);
                var codec=new SnapshotCodec();int expected=0;
                for(int repeat=0;repeat<6;repeat++) {
                    var before=ShortRestCapture(session);
                    CommitVialRoute(session,new Command("tac08.cadence.guidance."+repeat,actor,before.Revision,CommandKind.CastKnownSpell,actor,
                        spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                    expected+=Math.Min(3,repeat);var cast=ShortRestCapture(session).SpellCasts.Last();
                    Require(cast.DissonanceAfter==expected&&cast.AppliedRefrain==Math.Min(3,repeat)&&cast.RpAfter==3,
                        "Actual repeated cantrips must accumulate the source refrain without RP payment.");
                    var effects=ShortRestCapture(session).SpellEffects;
                    Require(effects.Count(x=>x.Present&&x.SpellId=="guidance")==1
                        &&effects.Where(x=>x.SpellId=="guidance"&&x.Id!=effects.Last().Id).All(x=>x.EndReason==SpellEffectEndReason.Replaced)
                        &&effects.Last().ExpiresAt==before.RuleClock.AddSeconds(60),
                        "Actual repeated Guidance must retain replaced predecessors and only one later-expiring usable benefit.");
                    ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                    Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==expected,
                        "A magical interval must not also receive idle decay.");
                    if(repeat==3) {
                        // Two separately restored lawful branches share only their actual prefix.
                        // Each starts with the same finite, unspent RP3; their payments never combine.
                        string prefix=Path.Combine(directory,"tac08-cadence-surcharge-prefix.ddsave");session.Save(prefix);
                        var paid=NewCastingExpedition();paid.Restore(prefix);var paidBefore=ShortRestCapture(paid);
                        CommitVialRoute(paid,new Command("tac08.cadence.paid-surcharge",actor,paidBefore.Revision,CommandKind.CastKnownSpell,actor,
                            spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                        var surcharge=ShortRestCapture(paid).SpellCasts.Last();
                        Require(surcharge.Surcharge==1&&surcharge.RpBefore==3&&surcharge.RpAfter==0,
                            "The real threshold surcharge must spend exactly the finite initial RP3.");
                        ClericCommit(paid,hero,CommandKind.AdvanceClock,x:6,y:1);
                        RetainClericDenial(CastingSimulation(paid),CastingAuthority(),new Command("tac08.cadence.unfunded-ranked",actor,
                            ShortRestCapture(paid).Revision,CommandKind.CastKnownSpell,actor,
                            spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)),"InsufficientResonance",directory);
                        paid.Save(Path.Combine(directory,"tac08-cadence-surcharge-paid.ddsave"));
                        var rite=NewCastingExpedition();rite.Restore(prefix);
                        CommitVialRoute(rite,new Command("tac08.cadence.rite-award",actor,ShortRestCapture(rite).Revision,
                            CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
                        CommitVialRoute(rite,new Command("tac08.cadence.rite-advance",actor,ShortRestCapture(rite).Revision,
                            CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
                        ClericCommit(rite,actor,CommandKind.UseHealingRite,actor);
                        ClericCommit(rite,hero,CommandKind.AdvanceClock,x:6,y:1);var riteAfter=ShortRestCapture(rite);
                        Require(riteAfter.ResonancePools.Single().Current==1&&riteAfter.CastingStrain.Single().Dissonance==expected
                            &&riteAfter.CastingTurnEnds.Last().MagicalActivity&&riteAfter.HealingRites.Last().ActualGain>0,
                            "A real paid post-advancement Rite must heal and prevent that interval's idle decay without ordinary cast strain.");
                        string ritePath=Path.Combine(directory,"tac08-cadence-rite-activity.ddsave");rite.Save(ritePath);rite.Restore(ritePath);
                    }
                }
                var high=ShortRestCapture(session);var facts=CharacterRuleFacts.ForActor(high,actor);
                Require(high.CastingStrain.Single().RankedBlocked(facts.ProficiencyBonus,facts.AbilityModifier(CharacterAbility.Wisdom)),
                    "This genuine sequence must reach the actual ranked blocking threshold.");
                RetainClericDenial(CastingSimulation(session),CastingAuthority(),new Command("tac08.cadence.blocked-ranked",actor,high.Revision,
                    CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)),
                    "RankedCastingBlockedByDissonance",directory);
                CommitVialRoute(session,new Command("tac08.cadence.different-cantrip",actor,high.Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)));
                var changed=ShortRestCapture(session);
                Require(changed.CastingStrain.Single().Dissonance==expected&&changed.CastingStrain.Single().Refrain==0,
                    "A different spell resets refrain, not accumulated dissonance.");
                string path=Path.Combine(directory,"tac08-cadence-before-advancement.ddsave");session.Save(path);session.Restore(path);
                CommitVialRoute(session,new Command("tac08.cadence.award",actor,changed.Revision,CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
                CommitVialRoute(session,new Command("tac08.cadence.advance",actor,ShortRestCapture(session).Revision,CommandKind.AdvanceCharacterLevel,
                    ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==expected&&ShortRestCapture(session).ResonancePools.Single().Current==3,
                    "Real earned advancement or restore must not reset strain or fund current RP.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                CommitVialRoute(session,new Command("tac08.cadence.ground",actor,ShortRestCapture(session).Revision,CommandKind.GroundCastingStrain));
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==expected,"Grounding must wait for the actual owning End.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);expected-=facts.ProficiencyBonus;
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==expected
                    &&ShortRestCapture(session).CastingTurnEnds.Last().Grounding,"Grounding must reduce PB exactly once, without additional idle decay.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);expected--;
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==expected,"An actual nonmagical idle End must reduce one.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6*expected,y:1);
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==0,"Actual idle intervals must settle chronological decay to zero.");
                CommitVialRoute(session,new Command("tac08.cadence.passive-concentration",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                Require(ShortRestCapture(session).CastingStrain.Single().Dissonance==1,"The ranked casting interval must retain its base dissonance.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);var passive=ShortRestCapture(session);
                var concentration=passive.SpellEffects.Single(x=>x.Present&&x.RequiresConcentration);
                Require(passive.CastingStrain.Single().Dissonance==0&&passive.ResonancePools.Single().Current==1,
                    "Passive concentration must allow idle decay without recovering RP.");
                CommitVialRoute(session,new Command("tac08.cadence.voluntary-end",actor,passive.Revision,CommandKind.EndSpellConcentration,concentration.Id));
                var ended=ShortRestCapture(session);
                Require(!ended.SpellEffects.Any(x=>x.Present&&x.RequiresConcentration)&&!ended.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent
                    &&ended.RandomState==passive.RandomState&&ended.ResonancePools.Single().Current==1,
                    "Voluntary ending must preserve the unspent Action, RNG and paid RP.");
                path=Path.Combine(directory,"tac08-cadence-complete.ddsave");session.Save(path);var bytes=codec.Encode(ended);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"The complete actual cadence did not restore/replay exactly.");
            });
            cases.Add("tac08_detached_verbal_condition_preflight", () => {
                var session=CastingFirstOwnTurn();var baseline=ShortRestCapture(session);var policy=ClericPolicy(session);
                const string actor=ClericRpProfile.Actor;
                foreach(string condition in new[]{"Silenced","Deafened"}) {
                    // No admitted producer applies either condition in this campaign. These
                    // detached controls exercise the actual casting preflight, not acquisition.
                    var candidate=baseline.Copy();var journal=candidate.Conditions.Single(x=>x.Target==actor);
                    var changed=CJApply(ConditionHistory.Restore(journal),"detached.casting."+condition,condition).State.Journal;
                    candidate.Conditions=candidate.Conditions.Select(x=>x.Target==actor?changed:x).ToArray();
                    var casts=candidate.SpellCasts;var pools=candidate.ResonancePools;var intervals=candidate.WorldIntervals;
                    var command=new Command("detached.casting.verbal",actor,candidate.Revision,CommandKind.CastKnownSpell,actor,
                        spellCast:new SpellCastRequest("guidance",willingTarget:true));
                    string result=policy.Resolve(candidate,command);
                    Require(result==(condition=="Silenced"?"SpellVerbalComponentUnavailable":null),
                        "Casting must distinguish inability to speak from hearing loss.");
                    if(condition=="Silenced")Require(ReferenceEquals(casts,candidate.SpellCasts)&&ReferenceEquals(pools,candidate.ResonancePools)
                        &&ReferenceEquals(intervals,candidate.WorldIntervals)&&candidate.RandomState==baseline.RandomState,
                        "Failed verbal preflight paid or rolled before denial.");
                }
            });
            cases.Add("tac08_genuine_guidance_search_actual_hidden_target", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=CastingFirstOwnTurn();var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.search.hide-benefit",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                string hideBenefit=ShortRestCapture(session).SpellEffects.Last().Id;
                ClericEnd(session,actor);ClericGuard(session,hero);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,1,1);ClericDefender(session);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,2,0);ClericDefender(session);
                CommitVialRoute(session,new Command("tac08.search.actual-hide",hero,ShortRestCapture(session).Revision,CommandKind.Hide,
                    session.View(ExpeditionSeat.Player).TurnId,guidance:new GuidanceChoice(hideBenefit)));
                ClericEnd(session,hero);ClericDefender(session);ClericGuard(session,actor);
                CommitVialRoute(session,new Command("tac08.search.check-benefit",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                string benefit=ShortRestCapture(session).SpellEffects.Last().Id;
                ClericEnd(session,actor);ClericGuard(session,hero);ClericEnd(session,hero);ClericDefender(session);ClericGuard(session,actor);
                var before=ShortRestCapture(session);string path=Path.Combine(directory,"tac08-guidance-before-actual-search.ddsave");session.Save(path);
                var search=new Command("tac08.search.guided",actor,before.Revision,CommandKind.Search,session.View(ExpeditionSeat.Player).TurnId,2,0,
                    guidance:new GuidanceChoice(benefit));
                CommitVialRoute(session,search);var after=ShortRestCapture(session);var check=after.ObservationActions.Last();var use=after.GuidanceUses.Last();
                Require(use.CheckKind==GuidanceCheckKind.Search&&use.EffectId==benefit&&use.RandomBefore==before.RandomState
                    &&use.RandomAfter==check.RandomBefore&&check.WordsConsumed>0
                    &&check.Modifier==CharacterStateFacts.ForActor(before,actor,"perception").TotalWithInjury(CharacterAbility.Wisdom,perception:true)+use.D4,
                    "Search must consume one chosen Guidance d4 before the actual hidden-target check.");
                path=Path.Combine(directory,"tac08-guidance-actual-search.ddsave");session.Save(path);var bytes=codec.Encode(after);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Guided Search did not restore/replay exactly.");
            });
            cases.Add("tac08_genuine_guidance_medicine_stabilization", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=CastingFirstOwnTurn();var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.medicine.guidance",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                string benefit=ShortRestCapture(session).SpellEffects.Single().Id;
                for(int round=0;round<10&&ShortRestCapture(session).Lives.Single(x=>x.ActorId==actor).Hp>0;round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);
                    if(round==0){
                        ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,1,1);ClericDefender(session);
                        ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,2,0);ClericDefender(session);
                    }
                    ClericEnd(session,hero);ClericDefender(session);
                }
                var dying=ShortRestCapture(session);var life=dying.Lives.Single(x=>x.ActorId==actor);
                Require(life.Hp==0&&!life.Dead&&!life.Stable&&dying.SpellEffects.Single().Present,
                    "The real combat patient must become dying while the previously cast Guidance remains present.");
                ClericEnd(session,actor);ClericGuard(session,hero);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,1,1);ClericDefender(session);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,1,2);ClericDefender(session);
                var before=ShortRestCapture(session);string path=Path.Combine(directory,"tac08-guidance-before-medicine.ddsave");session.Save(path);
                var command=new Command("tac08.medicine.actual-check",hero,before.Revision,CommandKind.StabilizeCompanion,actor,guidance:new GuidanceChoice(benefit));
                var query=CastingSimulation(session).QueryCommand(CastingAuthority(),command);
                Require(query.Admissible,"Real guided Medicine must be in reach with an available Action: "+query.Code);
                CommitVialRoute(session,command);var after=ShortRestCapture(session);var use=after.GuidanceUses.Single();var check=after.CompanionStabilizations.Single();
                Require(use.CheckKind==GuidanceCheckKind.MedicineStabilization&&use.CheckId==command.Id+".medicine"
                    &&use.RandomBefore==before.RandomState&&use.RandomAfter==check.RandomBefore
                    &&check.Modifier==CharacterStateFacts.ForActor(before,hero,"medicine").TotalWithInjury(CharacterAbility.Wisdom)+use.D4
                    &&!after.SpellEffects.Single().Present&&after.ResonancePools.Single().Current==3,
                    "Medicine must consume the real Guidance d4 before its d20, without replacing its existing stabilization procedure.");
                path=Path.Combine(directory,"tac08-guidance-medicine.ddsave");session.Save(path);var bytes=codec.Encode(after);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Guided Medicine history did not restore/replay exactly.");
            });
            cases.Add("tac08_genuine_earned_detect_guidance_aura_and_paid_focus", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=EarnClericObjective(false,selected:NewCastingExpedition());var codec=new SnapshotCodec();
                var objective=ShortRestCapture(session);
                Require(objective.ResonancePools.Single().Current==3&&objective.SpellCasts.Length==0&&objective.HealingRites.Length==0,
                    "The earned Detect branch must preserve its actual initial finite RP through real combat and manufacturing.");
                CommitVialRoute(session,new Command("tac08.detect.award",actor,objective.Revision,CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
                CommitVialRoute(session,new Command("tac08.detect.advance",actor,ShortRestCapture(session).Revision,CommandKind.AdvanceCharacterLevel,
                    ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
                var advanced=ShortRestCapture(session);
                Require(advanced.ResonancePools.Single().Current==3&&advanced.KnownSpells.Any(x=>x.SpellId=="detect-magic"&&x.AcquiredRevision==advanced.Revision),
                    "Actual Cleric2 must acquire Detect while preserving current RP3.");
                session.Save(Path.Combine(directory,"tac08-detect-earned.ddsave"));ReachClericOwnSlot(session);
                CommitVialRoute(session,new Command("tac08.detect.aura-producer",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                CommitVialRoute(session,new Command("tac08.detect.paid-cast",actor,ShortRestCapture(session).Revision,CommandKind.CastKnownSpell,actor,
                    spellCast:new SpellCastRequest("detect-magic",SpellCastingProfile.FocusId)));
                var detected=ShortRestCapture(session);var view=session.View(ExpeditionSeat.Player);
                var own=view.Actors.Single(x=>x.Position.Id==actor);var recipient=view.Actors.Single(x=>x.Position.Id==hero);
                var aura=own.Casting.Auras.Single(x=>x.X==recipient.Position.X&&x.Y==recipient.Position.Y);
                Require(detected.ResonancePools.Single().Current==1&&!aura.Focused&&aura.SchoolCategory==""
                    &&own.Repertoire.KnownSpells.Single(x=>x.Id=="detect-magic").CastingSupported&&!own.Casting.ProductionAuthority
                    &&recipient.Casting.GuidanceBenefits.Count==1,"Actual Detect must pay3-to1 and reveal only an opaque outline for actual Guidance.");
                var publicAura=System.Text.Json.JsonSerializer.Serialize(aura);
                Require(!publicAura.Contains("guidance")&&!publicAura.Contains("Source")&&!publicAura.Contains("Owner")&&!publicAura.Contains("Rank"),
                    "An aura observation leaked internal spell provenance.");
                string detectedPath=Path.Combine(directory,"tac08-detect-active.ddsave");session.Save(detectedPath);
                byte[] bytes=codec.Encode(detected);session.Restore(detectedPath);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Paid Detect failed independent restore.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);var before=ShortRestCapture(session);
                var focus=new Command("tac08.detect.later-focus",actor,before.Revision,CommandKind.FocusDetectedAura,aura.ObservationId);
                bytes=codec.Encode(before);
                Require(CastingSimulation(session).QueryCommand(CastingAuthority(),focus).Admissible
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Aura focus preflight must be pure and target the retained public observation.");
                // Explicitly detached protection control: the cohort owns no protection producer.
                // This altered policy input is never submitted, saved, or claimed as campaign acquisition.
                var protectedCandidate=before.Copy();var method=typeof(TestOnlySharedWorldPolicy).GetMethod("ResolveCastingUtility",BindingFlags.Instance|BindingFlags.NonPublic);
                Require(method.Invoke(ClericPolicy(session),new object[]{protectedCandidate,focus,true})==null
                    &&protectedCandidate.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent
                    &&protectedCandidate.DetectMagicFocuses.Single().SchoolWithheld&&protectedCandidate.DetectMagicFocuses.Single().BroadSchool==""
                    &&protectedCandidate.RandomState==before.RandomState&&protectedCandidate.ResonancePools.Single().Current==1,
                    "A legal protected focus must still pay the Action and withhold its school.");
                Require(!SpellCastingProfile.AuraOutlinePermitted(true,true,true,true,true)
                    &&!SpellCastingProfile.AuraOutlinePermitted(false,true,true,true,false)
                    &&!SpellCastingProfile.AuraOutlinePermitted(true,true,true,false,false),
                    "Unregistered, blocked, or total-cover auras must expose no observation.");
                var covered=before.Copy();covered.Actors.Single(x=>x.Id==actor).X=0;covered.Actors.Single(x=>x.Id==actor).Y=0;
                covered.Actors.Single(x=>x.Id==hero).X=2;covered.Actors.Single(x=>x.Id==hero).Y=0;
                covered.ObservationCells=covered.ObservationCells.Where(x=>x.X!=1||x.Y!=0)
                    .Append(new ObservationMapCellRecord(1,0,true,true,true,true)).ToArray();
                var observe=typeof(TestOnlySharedWorldPolicy).GetMethod("ObserveCasting",BindingFlags.Static|BindingFlags.NonPublic);
                var coveredView=(ExpeditionCastingView)observe.Invoke(null,new object[]{covered,actor});
                Require(!ObservationGeometry.LineOfEffectClear(covered,actor,hero)
                    &&coveredView.Auras.All(x=>x.ObservationId!=aura.ObservationId)
                    &&ClericPolicy(session).Resolve(covered,focus)=="AuraObservationUnavailable"
                    &&!covered.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent&&covered.RandomState==before.RandomState,
                    "The actual geometry, aura filter and focus preflight must reject a covered aura before paying or rolling.");
                RetainClericDenial(CastingSimulation(session),new Authority("TEST_ONLY.other-seat",new[]{hero}),
                    focus,"NotAuthorized",directory);
                CommitVialRoute(session,focus);var focused=ShortRestCapture(session);
                var focusedAura=session.View(ExpeditionSeat.Player).Actors.Single(x=>x.Position.Id==actor).Casting.Auras.Single(x=>x.ObservationId==aura.ObservationId);
                Require(focusedAura.Focused&&focusedAura.SchoolCategory==SpellSourceCatalog.Get("guidance").AccessFor("Cleric").School
                    &&focused.ResonancePools.Single().Current==1&&focused.RandomState==before.RandomState&&focused.SpellCasts.Length==2
                    &&focused.CastingStrain.Single().Dissonance==before.CastingStrain.Single().Dissonance
                    &&focused.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent,
                    "Later focus must disclose only the broad school and pay Action without another cast, RP payment or strain.");
                session.Save(Path.Combine(directory,"tac08-detect-guidance-focused.ddsave"));
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:48,y:1);var expiredGuidance=ShortRestCapture(session);
                Require(expiredGuidance.SpellEffects.Single(x=>x.SpellId=="guidance").EndReason==SpellEffectEndReason.Expired
                    &&session.View(ExpeditionSeat.Player).Actors.Single(x=>x.Position.Id==actor).Casting.Auras.All(x=>x.ObservationId!=aura.ObservationId),
                    "The real Guidance endpoint must remove its aura without ending Detect.");
                // The accepted consumers are tactical only. This detached flag supplies that
                // context to the actual eligibility gate; expiry itself came from real shared time.
                var expiredConsumer=expiredGuidance.Copy();expiredConsumer.InventoryCombat=true;
                var expiredChoice=new Command("detached.guidance.expired-choice",hero,expiredConsumer.Revision,CommandKind.Hide,
                    guidance:new GuidanceChoice(expiredConsumer.SpellEffects.Single(x=>x.SpellId=="guidance").Id));
                var benefitGate=typeof(TestOnlySharedWorldPolicy).GetMethod("GuidanceChoiceFailure",BindingFlags.Static|BindingFlags.NonPublic);
                Require((string)benefitGate.Invoke(null,new object[]{expiredConsumer,expiredChoice})=="GuidanceBenefitUnavailable"
                    &&expiredConsumer.GuidanceUses.Length==0&&expiredConsumer.RandomState==expiredGuidance.RandomState,
                    "An effect actually expired by the shared clock cannot fund a later Guidance choice.");
                File.WriteAllText(Path.Combine(directory,"tac08-detached-aura-and-expiry-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached cover geometry, school-protection input and tactical consumer context; real paid focus and actual shared-clock expiry records",
                    coveredAuraUnavailable=true,protectedFocus=protectedCandidate.DetectMagicFocuses.Single(),expiredChoice="GuidanceBenefitUnavailable"}));
                RetainClericDenial(CastingSimulation(session),CastingAuthority(),new Command("tac08.detect.stale-aura",actor,expiredGuidance.Revision,
                    CommandKind.FocusDetectedAura,aura.ObservationId),"AuraObservationUnavailable",directory);
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:546,y:1);var final=ShortRestCapture(session);
                Require(final.SpellEffects.Single(x=>x.SpellId=="detect-magic").EndReason==SpellEffectEndReason.Expired
                    &&session.View(ExpeditionSeat.Player).Actors.Single(x=>x.Position.Id==actor).Casting.Auras.Count==0
                    &&final.ResonancePools.Single().Current==1,"The real600-second Detect deadline must end its view without refund.");
                string path=Path.Combine(directory,"tac08-detect-expired-continuation.ddsave");session.Save(path);bytes=codec.Encode(final);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Earned Detect/focus/expiry failed independent replay.");
            });
            cases.Add("tac08_genuine_spare_stabilizes_actual_combat_patient", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var session=CastingFirstOwnTurn();var codec=new SnapshotCodec();
                for(int round=0;round<20&&ShortRestCapture(session).Lives.Single(x=>x.ActorId==hero).Hp>0;round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);ClericEnd(session,hero);ClericDefender(session);
                }
                var dying=ShortRestCapture(session);var patient=dying.Lives.Single(x=>x.ActorId==hero);
                Require(patient.Hp==0&&!patient.Dead&&!patient.Stable
                    &&dying.MeleeAttacks.Any(x=>x.TargetId==hero&&x.Attack.Hit&&x.Damage.Total>0),
                    "Spare's patient must be made genuinely dying by the existing defender's actual attacks.");
                ClericGuard(session,actor);dying=ShortRestCapture(session);
                string path=Path.Combine(directory,"tac08-spare-before-cast.ddsave");session.Save(path);session.Restore(path);
                var cast=new Command("tac08.spare.actual-patient",actor,dying.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("spare-the-dying"));
                byte[] bytes=codec.Encode(dying);
                Require(CastingSimulation(session).QueryCommand(CastingAuthority(),cast).Admissible
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Spare preflight must neither heal nor roll the Stable deadline.");
                CommitVialRoute(session,cast);var after=ShortRestCapture(session);var stable=after.Lives.Single(x=>x.ActorId==hero);
                var draw=DiceStream.Draw(dying.RandomState,4);var record=after.SpellCasts.Single();
                Require(stable.Stable&&!stable.Dead&&stable.Hp==0&&stable.DeathSuccesses==0&&stable.DeathFailures==0
                    &&stable.StableUntil==dying.RuleClock.AddSeconds((draw.Value+1)*3600L)
                    &&stable.LinkedInjuries.SequenceEqual(patient.LinkedInjuries)
                    &&record.StableRecoveryD4==draw.Value+1&&after.RandomState==draw.NextState
                    &&after.ResonancePools.Single().Current==3&&after.CompanionStabilizations.Length==0
                    &&after.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent,
                    "Automatic stabilization must use one existing recovery d4, preserve HP/injury/RP, and pay only the real Action.");
                path=Path.Combine(directory,"tac08-spare-stable-patient.ddsave");session.Save(path);bytes=codec.Encode(after);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Spare's real Stable deadline failed save/replay.");
            });
            cases.Add("tac08_genuine_purify_finite_water_and_measured_intake", () => {
                const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var codec=new SnapshotCodec();Snapshot beforeCast=null,purified=null;
                var session=EarnClericObjective(false,selected:NewCastingExpedition(),firstClericAction:campaign=>{
                    beforeCast=ShortRestCapture(campaign);campaign.Save(Path.Combine(directory,"tac08-before-purify.ddsave"));
                    var command=new Command("tac08.purify.water",actor,beforeCast.Revision,CommandKind.CastKnownSpell,
                        SpellCastingProfile.ContaminatedWaterId,spellCast:new SpellCastRequest("purify-food-and-drink",SpellCastingProfile.FocusId));
                    var query=CastingSimulation(campaign).QueryCommand(CastingAuthority(),command);
                    Require(query.Admissible,"The actual finite flask must be perceived and in range: "+query.Code);
                    CommitVialRoute(campaign,command);purified=ShortRestCapture(campaign);
                    Require(!purified.ConsumableContamination.Single().Present&&purified.ResonancePools.Single().Current==1
                        &&purified.RandomState==beforeCast.RandomState&&purified.RuleClock==beforeCast.RuleClock
                        &&purified.Work.Lots.Single(x=>x.Id==SpellCastingProfile.ContaminatedWaterId).Amount==new RuleQuantity(1)
                        &&purified.Vessels.Single(x=>x.Id==TestOnlyFillingPolicy.FlaskId).LocationId==TestOnlyCropPolicy.PlotId
                        &&purified.InventoryLots.Single(x=>x.LotId==SpellCastingProfile.ContaminatedWaterId).CreatedAmount==new RuleQuantity(1),
                        "Purify must remove the qualified occurrence without moving, manufacturing, or consuming its actual water.");
                    campaign.Save(Path.Combine(directory,"tac08-purified-water.ddsave"));
                });
                Require(!ShortRestCapture(session).InventoryCombat&&ShortRestCapture(session).ClericObjective!=null,
                    "The paid Purify branch must continue through actual combat and earned objective closure.");
                ClericCommit(session,actor,CommandKind.BeginWorldStep,"walk",x:1);
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
                var handling=ShortRestCapture(session);
                CommitVialRoute(session,new Command("tac08.purified-flask-pickup",actor,handling.Revision,CommandKind.HandleVessel,
                    TestOnlyFillingPolicy.FlaskId,inventory:new InventoryRequest(new RuleQuantity(1))));
                var ready=ShortRestCapture(session);
                Require(ready.Vessels.Single(x=>x.Id==TestOnlyFillingPolicy.FlaskId).CustodianId==actor
                    &&ready.RuleClock==handling.RuleClock.AddSeconds(1),"The same flask must be reached and picked up through paid handling.");
                CommitVialRoute(session,new Command("tac08.purified-water-intake",actor,ready.Revision,CommandKind.StartIntake,
                    SpellCastingProfile.ContaminatedWaterId,inventory:new InventoryRequest(new RuleQuantity(1))));
                var started=ShortRestCapture(session);session.Save(Path.Combine(directory,"tac08-purified-water-intake-started.ddsave"));
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:60,y:1);var after=ShortRestCapture(session);
                Require(after.RuleClock==started.RuleClock.AddSeconds(60)
                    &&after.Work.Lots.Single(x=>x.Id==SpellCastingProfile.ContaminatedWaterId).Amount==default(RuleQuantity)
                    &&after.Intakes.Any(x=>x.ActorId==actor&&x.LotId==SpellCastingProfile.ContaminatedWaterId&&x.Status==IntakeStatus.Complete)
                    &&after.ResonancePools.Single().Current==1&&!after.ConsumableContamination.Single().Present
                    &&after.Work.Lots.Where(x=>x.Id!=SpellCastingProfile.ContaminatedWaterId).All(x=>ready.Work.Lots.Any(y=>y.Id==x.Id&&y.Amount==x.Amount)),
                    "Measured consumption must use exactly the same one pint in one minute without stock or RP gains.");
                string path=Path.Combine(directory,"tac08-purified-water-consumed.ddsave");session.Save(path);
                var bytes=codec.Encode(after);string viewBefore=System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player));session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Purify, carrying, and measured intake failed independent restore.");
                Require(viewBefore==System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player)),
                    "Purified intake work changed its public order after restore.");
            });
            cases.Add("tac08_genuine_sanctuary_carried_opportunity_forgo", () => {
                var session=CastingFirstOwnTurn();const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var before=ShortRestCapture(session);var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.sanctuary.carried-ward",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                ClericEnd(session,actor);ClericGuard(session,hero);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:1);
                before=ShortRestCapture(session);var movement=before.TacticalMoves.Single(x=>x.Status==TacticalMoveStatus.AwaitingReactions);
                var authority=LaterDefenderController.DefenderAuthority();var simulation=CastingSimulation(session);
                var controller=new LaterDefenderController(simulation,ClericPolicy(session));var decision=controller.Plan(authority);
                byte[] bytes=codec.Encode(before);
                var admission=simulation.AssessCommandAdmission(authority,decision.Primary);
                var query=simulation.QueryCommand(authority,decision.Primary);
                Require(decision.Intent.Kind==DefenderIntentKind.AcceptOpportunity
                    &&admission.Status==CommandAdmissionStatus.Admitted&&query.Admissible
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                    "A reaction eligibility probe must not predict or consume its future ward save: "+decision.Intent.Kind+"/"+admission.Code+"/"+query.Code);
                Require(controller.Dispatch(authority,decision)==DefenderDispatchStatus.Committed,"The actual opportunity ward gate did not commit.");
                var pendingState=ShortRestCapture(session);var pending=pendingState.SanctuaryAdmissions.Single(x=>x.Pending);
                var save=pendingState.SpellSaves.Single();var entry=pendingState.Reinforcement.Events.Single(x=>x.Kind==ReinforcementEventKind.Admitted);
                Require(pending.Source==SanctuaryAttackSource.Opportunity&&pending.OpportunityId==movement.Id&&!save.Success
                    &&save.AttackerTurn.IsCarried&&save.AttackerTurn.LocalStart==-1&&save.AttackerTurn.CarriedAdmissionRevision==entry.Revision
                    &&save.AttackerTurn.GlobalStart==pendingState.Reinforcement.Admission.Carried.Single(x=>x.Interval.ActorId==pending.ActorId).Interval.LastStart
                    &&pendingState.Actors.Single(x=>x.Id==hero).Y==2
                    &&pendingState.MeleeAttacks.Length==before.MeleeAttacks.Length
                    &&pendingState.TacticalActors.Single(x=>x.ActorId==pending.ActorId).ReactionAvailable,
                    "The failed ward gate must retain the actual carried interval and suspend the exact unpaid reaction/movement.");
                string path=Path.Combine(directory,"tac08-sanctuary-carried-opportunity.ddsave");session.Save(path);
                RetainClericDenial(simulation,authority,new Command("tac08.sanctuary.reaction-conversion",pending.ActorId,pendingState.Revision,
                    CommandKind.RespondSanctuary,pending.Id,sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Retarget,actor)),
                    "SanctuaryRetargetOutsideOriginalSource",directory);
                Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"The actual reaction controller could not forgo.");
                var after=ShortRestCapture(session);
                Require(after.RandomState==pendingState.RandomState&&after.SpellSaves.Length==1
                    &&after.SanctuaryAdmissions.Single().Status==SanctuaryAdmissionStatus.Forgone
                    &&after.TacticalMoves.Single(x=>x.Id==movement.Id).Status==TacticalMoveStatus.Completed
                    &&after.Actors.Single(x=>x.Id==hero).Y==1&&after.TacticalActors.Single(x=>x.ActorId==pending.ActorId).ReactionAvailable
                    &&!after.WorldIntervals.Single(x=>x.ActorId==hero).ActionSpent,
                    "Forgo must finish only the original occurrence, resume its parent step, and preserve unspent budgets.");
                bytes=codec.Encode(after);session.Save(Path.Combine(directory,"tac08-sanctuary-carried-parent-resumed.ddsave"));
                var restored=NewCastingExpedition();restored.Restore(path);
                Require(restored.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(restored))),"Restoring a pending carried reaction changed its exact continuation.");
            });
            cases.Add("tac08_genuine_concentration_damage_uses_actual_packet", () => {
                var session=CastingFirstOwnTurn();const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var before=ShortRestCapture(session);var codec=new SnapshotCodec();
                CommitVialRoute(session,new Command("tac08.concentration.hero-ward",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                for(int round=0;round<10&&ShortRestCapture(session).SpellEffects.Single().Present;round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);
                    if(round==0){ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:1);ClericDefender(session);}
                    ClericEnd(session,hero);ClericDefender(session);
                    session.Save(Path.Combine(directory,"tac08-concentration-round-"+round+".ddsave"));
                }
                var after=ShortRestCapture(session);var saves=after.SpellSaves.Where(x=>x.Kind==SpellSaveKind.ConcentrationConstitution).ToArray();
                File.WriteAllText(Path.Combine(directory,"tac08-concentration-damage-witness.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    saves,effect=after.SpellEffects.Single(),attacks=after.MeleeAttacks.Where(x=>x.Revision>before.Revision),life=after.Lives.Single(x=>x.ActorId==actor)}));
                Require(saves.Length>0,"Real incoming damage did not reach an eligible concentration save.");
                foreach(var save in saves) {
                    var packet=after.MeleeAttacks.Single(x=>x.ResolvedRevision==save.Revision&&x.TargetId==actor);
                    var draw=DiceStream.Draw(packet.Damage.FinalRandom,20);
                    Require(packet.Attack.Hit&&packet.Damage.Total>0&&save.Damage==packet.Damage.Total
                        &&save.RandomBefore==packet.Damage.FinalRandom&&save.RandomAfter==draw.NextState&&save.First==draw.Value+1
                        &&save.Dc==Math.Max(10,packet.Damage.Total/2),"Concentration must follow the complete actual positive damage packet exactly once.");
                }
                Require(!after.SpellEffects.Single().Present&&after.SpellEffects.Single().EndReason==SpellEffectEndReason.DamageSaveFailed
                    &&saves.Last().Success==false&&after.Lives.Single(x=>x.ActorId==actor).Hp>0&&after.ResonancePools.Single().Current==1,
                    "A genuine failed CON save must end concentration without refunding the paid cast or requiring incapacity.");
                string path=Path.Combine(directory,"tac08-concentration-damage-ended.ddsave");session.Save(path);
                byte[] bytes=codec.Encode(after);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Concentration damage failed independent save/replay.");
            });
            cases.Add("tac08_genuine_sanctuary_pending_retarget_forgo_and_restore", () => {
                var session=CastingFirstOwnTurn();const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var codec=new SnapshotCodec();var before=ShortRestCapture(session);
                CommitVialRoute(session,new Command("tac08.sanctuary.hero",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                Require(ShortRestCapture(session).ResonancePools.Single().Current==1,"Sanctuary must spend the real finite 2RP.");
                session.Save(Path.Combine(directory,"tac08-active-sanctuary.ddsave"));
                Snapshot gateBefore=null;
                for(int round=0;round<5&&ShortRestCapture(session).SanctuaryAdmissions.All(x=>!x.Pending);round++) {
                    if(round>0)ClericGuard(session,actor);
                    ClericEnd(session,actor);ClericGuard(session,hero);
                    ClericEnd(session,hero);
                    for(int step=0;step<12&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.AutomaticDefender;step++) {
                        gateBefore=ShortRestCapture(session);
                        Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Sanctuary defender step failed.");
                        if(ShortRestCapture(session).SanctuaryAdmissions.Any(x=>x.Pending))break;
                    }
                }
                var pendingState=ShortRestCapture(session);var pending=pendingState.SanctuaryAdmissions.Single(x=>x.Pending);
                var save=pendingState.SpellSaves.Single(x=>x.Id==pending.SaveId);
                File.WriteAllText(Path.Combine(directory,"tac08-sanctuary-pending-witness.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    pending,save,positions=pendingState.Actors.Select(x=>new{x.Id,x.X,x.Y}),intervals=pendingState.WorldIntervals}));
                Require(!save.Success&&save.RandomBefore==gateBefore.RandomState&&save.RandomAfter==pendingState.RandomState
                    &&pendingState.MeleeAttacks.Length==gateBefore.MeleeAttacks.Length
                    &&!pendingState.WorldIntervals.Single(x=>x.ActorId==pending.ActorId).ActionSpent
                    &&pendingState.ResonancePools.Single().Current==1,
                    "A failed real ward gate must persist only its save without drawing an attack or spending the Action.");
                string path=Path.Combine(directory,"tac08-sanctuary-pending.ddsave");session.Save(path);
                byte[] bytes=codec.Encode(pendingState);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Pending Sanctuary did not independently restore/replay.");
                var authority=LaterDefenderController.DefenderAuthority();var simulation=CastingSimulation(session);
                var retarget=new Command("tac08.sanctuary.retarget",pending.ActorId,pendingState.Revision,CommandKind.RespondSanctuary,pending.Id,
                    sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Retarget,actor));
                var retargetQuery=simulation.QueryCommand(authority,retarget);
                Require(retargetQuery.Admissible
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Legal retarget query must not reroll or pay: "+retargetQuery.Code);
                Require(simulation.Execute(CastingAuthority(),retarget).Outcome==Outcome.Rejected
                    &&bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"A player grant cannot answer for the defender.");
                Require(simulation.Execute(authority,retarget).Outcome==Outcome.Committed,"The original controller could not retarget its real attack.");
                var resolved=ShortRestCapture(session);
                Require(resolved.SanctuaryAdmissions.Single().Status==SanctuaryAdmissionStatus.Retargeted
                    &&resolved.MeleeAttacks.Last().TargetId==actor&&resolved.MeleeAttacks.Last().Attack.RandomBefore==save.RandomAfter
                    &&resolved.SpellSaves.Count(x=>x.Kind==SpellSaveKind.SanctuaryWisdom)==1
                    &&resolved.WorldIntervals.Single(x=>x.ActorId==pending.ActorId).ActionSpent,
                    "Retarget must use the same remaining attack budget after the retained WIS save.");
                byte[] result=codec.Encode(resolved);
                Require(simulation.Execute(authority,retarget).Outcome==Outcome.Duplicate&&result.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                    "Duplicate retarget must not repeat the attack or save.");
                session.Save(Path.Combine(directory,"tac08-sanctuary-retargeted.ddsave"));
                var forgone=NewCastingExpedition();forgone.Restore(path);simulation=CastingSimulation(forgone);
                var forgo=new Command("tac08.sanctuary.forgo",pending.ActorId,pendingState.Revision,CommandKind.RespondSanctuary,pending.Id,
                    sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo));
                Require(simulation.Execute(authority,forgo).Outcome==Outcome.Committed,"The original controller could not forgo its attack.");
                var after=ShortRestCapture(forgone);
                Require(after.RandomState==pendingState.RandomState&&after.MeleeAttacks.Length==pendingState.MeleeAttacks.Length
                    &&!after.WorldIntervals.Single(x=>x.ActorId==pending.ActorId).ActionSpent,
                    "Forgoing an unresolved regular attack must preserve the unused Action and RNG.");
                var original=CommandHistory.Read(pendingState.Receipts.Single(x=>x.Id==pending.SourceCommandId));
                var retry=new Command("tac08.sanctuary.failed-target-retry",pending.ActorId,after.Revision,original.Kind,original.Target,combat:original.Combat);
                RetainClericDenial(simulation,authority,retry,"SanctuaryTargetProhibitedThisInterval",directory);
                Require(forgone.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,
                    "After forgo the controller must choose a legal different Action or End from known cache facts.");
                forgone.Save(Path.Combine(directory,"tac08-sanctuary-forgone-continued.ddsave"));
            });
            cases.Add("tac08_genuine_guidance_hide_choice_and_no_check_search", () => {
                var session=CastingFirstOwnTurn(); const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var codec=new SnapshotCodec();var before=ShortRestCapture(session);
                CommitVialRoute(session,new Command("tac08.guidance.hero",actor,before.Revision,CommandKind.CastKnownSpell,hero,
                    spellCast:new SpellCastRequest("guidance",willingTarget:true)));
                string effectId=ShortRestCapture(session).SpellEffects.Last().Id;
                string castPath=Path.Combine(directory,"tac08-guidance-before-choice.ddsave");session.Save(castPath);
                ClericEnd(session,actor);ClericGuard(session,hero);
                before=ShortRestCapture(session);var position=before.Actors.Single(x=>x.Id==hero);
                var emptySearch=new Command("tac08.guidance.empty-search",hero,before.Revision,CommandKind.Search,
                    session.View(ExpeditionSeat.Player).TurnId,position.X,position.Y,guidance:new GuidanceChoice(effectId));
                var bytes=codec.Encode(before);
                Require(CastingSimulation(session).QueryCommand(CastingAuthority(),emptySearch).Admissible
                    && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Guidance Search query must be pure.");
                CommitVialRoute(session,emptySearch);var searched=ShortRestCapture(session);
                Require(searched.RandomState==before.RandomState && searched.GuidanceUses.Length==0
                    && searched.SpellEffects.Single(x=>x.Id==effectId).Present
                    && searched.ObservationActions.Last().WordsConsumed==0
                    && searched.WorldIntervals.Single(x=>x.ActorId==hero).ActionSpent,
                    "An empty Search must pay its Action but preserve Guidance and RNG.");
                session.Save(Path.Combine(directory,"tac08-guidance-empty-search.ddsave"));
                session=NewCastingExpedition();session.Restore(castPath);
                ClericEnd(session,actor);ClericGuard(session,hero);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,1,1);ClericDefender(session);
                ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,2,0);ClericDefender(session);
                string choicePath=Path.Combine(directory,"tac08-guidance-hide-choice.ddsave");session.Save(choicePath);
                before=ShortRestCapture(session);bytes=codec.Encode(before);
                var hide=new Command("tac08.guidance.actual-hide",hero,before.Revision,CommandKind.Hide,
                    session.View(ExpeditionSeat.Player).TurnId,guidance:new GuidanceChoice(effectId));
                var query=CastingSimulation(session).QueryCommand(CastingAuthority(),hide);
                Require(query.Admissible && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),
                    "The actual Guidance Hide query must be legal and leave RNG/effects unchanged: "+query.Code);
                // No-observer Hide is a separate detached consumer control: remove observers
                // with the actual fatal life producer, never alter the genuine campaign.
                var noObservers=before.Copy();var applyLife=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                foreach(var observer in noObservers.Lives.Where(x=>x.ActorId!=hero&&!x.Dead).ToArray()) {
                    var fatal=PlaytestDamageDice.Resolve(ActorLifeRules.ReadForResolution(noObservers,observer),observer.Hp+observer.MaximumHp,
                        noObservers.RuleClock,noObservers.RandomState);
                    noObservers.RandomState=fatal.NextRandomState;
                    applyLife.Invoke(null,new object[]{noObservers,observer,fatal.Outcome.State});
                }
                uint noCheckRandom=noObservers.RandomState;
                Require(ClericPolicy(session).Resolve(noObservers,hide)==null&&noObservers.GuidanceUses.Length==0
                    &&noObservers.SpellEffects.Single(x=>x.Id==effectId).Present&&noObservers.RandomState==noCheckRandom
                    &&noObservers.ObservationActions.Last().Outcome==ObservationActionOutcome.NoEligibleObservers,
                    "An actual no-check Hide consumer must preserve the selected Guidance and draw no die.");
                CommitVialRoute(session,hide);var hidden=ShortRestCapture(session);
                var use=hidden.GuidanceUses.Single();var check=hidden.ObservationActions.Last();var d4=DiceStream.Draw(before.RandomState,4);
                Require(use.D4==d4.Value+1 && use.RandomBefore==before.RandomState && use.RandomAfter==check.RandomBefore
                    && use.CheckId==check.Id && use.CheckKind==GuidanceCheckKind.Hide && check.WordsConsumed>0
                    && check.Modifier==CharacterStateFacts.ForActor(before,hero,"stealth").TotalWithInjury(CharacterAbility.Dexterity)+use.D4
                    && !hidden.SpellEffects.Single(x=>x.Id==effectId).Present
                    && hidden.SpellEffects.Single(x=>x.Id==effectId).EndReason==SpellEffectEndReason.GuidanceConsumed,
                    "The real Hide must consume exactly one d4 before its d20 and add the result once.");
                string finalPath=Path.Combine(directory,"tac08-guidance-hidden.ddsave");session.Save(finalPath);
                var finalBytes=codec.Encode(hidden);session.Restore(finalPath);
                Require(finalBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Guidance consumption did not restore/replay exactly.");
                RetainClericDenial(CastingSimulation(session),CastingAuthority(),new Command("tac08.guidance.reused",hero,hidden.Revision,
                    CommandKind.Search,session.View(ExpeditionSeat.Player).TurnId,2,0,guidance:new GuidanceChoice(effectId)),
                    "GuidanceBenefitUnavailable",directory);
                var declined=NewCastingExpedition();declined.Restore(choicePath);before=ShortRestCapture(declined);
                ClericCommit(declined,hero,CommandKind.Hide,declined.View(ExpeditionSeat.Player).TurnId);
                var ordinary=ShortRestCapture(declined);
                Require(ordinary.GuidanceUses.Length==0 && ordinary.SpellEffects.Single(x=>x.Id==effectId).Present
                    && ordinary.ObservationActions.Last().RandomBefore==before.RandomState,
                    "An actual check without the recipient's election must preserve Guidance.");
                // The genuine declined roll may succeed. A failed-retry rule needs a failed
                // check: disclose this separate deterministic RNG setup, then use the real
                // Hide producer and its retained observer results on the detached copy.
                var failedHide=before.Copy();uint failedSeed=1;
                while(PlaytestDice.RollD20(failedSeed).Natural!=1)failedSeed++;
                failedHide.RandomState=failedSeed;
                var failedCommand=new Command("detached.guidance.failed-hide",hero,failedHide.Revision,CommandKind.Hide,
                    failedHide.Encounter.CurrentTurnId);
                Require(ClericPolicy(declined).Resolve(failedHide,failedCommand)==null
                    &&failedHide.ObservationHideResults.Where(x=>x.AttemptId==failedHide.ObservationActions.Last().Id).Any(x=>!x.HiddenEstablished),
                    "The detached actual Hide producer must establish a failed result before the retry control.");
                var retry=new Command("detached.guidance.unchanged-hide",hero,failedHide.Revision,CommandKind.Hide,
                    failedHide.Encounter.CurrentTurnId,guidance:new GuidanceChoice(effectId));
                var assessHide=typeof(TestOnlySharedWorldPolicy).GetMethod("ResolveHide",BindingFlags.Instance|BindingFlags.NonPublic);
                Require((string)assessHide.Invoke(ClericPolicy(declined),new object[]{failedHide.Copy(),retry,true})=="HideAttemptUnchanged",
                    "Adding a Guidance choice alone must not authorize an unchanged failed Hide retry.");
                declined.Save(Path.Combine(directory,"tac08-guidance-declined.ddsave"));
                File.WriteAllText(Path.Combine(directory,"tac08-guidance-detached-consumer-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Detached no-observer life setup and seeded failed Hide through actual producer/pure retry assessment; no injected campaign state",noCheckRandom,
                    noCheck=noObservers.ObservationActions.Last(),failedSeed,failedCheck=failedHide.ObservationActions.Last(),unchangedRetry="HideAttemptUnchanged"}));
            });
            cases.Add("tac08_genuine_arcane_ward_attack_and_next_start_expiry", () => {
                var session=CastingFirstOwnTurn(); const string hero=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                var before=ShortRestCapture(session); var codec=new SnapshotCodec(); Snapshot cast=null,after=null;
                SpellEffectRecord effect=null; MeleeAttackRecord[] incoming=Array.Empty<MeleeAttackRecord>();
                for(int attempt=0;attempt<6&&incoming.Length==0;attempt++) {
                    if(attempt!=0)ClericGuard(session,actor);
                    before=ShortRestCapture(session);
                    var command=new Command("tac08.actual-ward."+attempt,actor,before.Revision,CommandKind.CastKnownSpell,actor,
                        spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true));
                    Require(CastingSimulation(session).QueryCommand(CastingAuthority(),command).Admissible,"Actual worn focus failed legal Ward preflight.");
                    CommitVialRoute(session,command);cast=ShortRestCapture(session);effect=cast.SpellEffects.Last();
                    session.Save(Path.Combine(directory,"tac08-active-ward-"+attempt+".ddsave"));
                    ClericEnd(session,actor);ClericGuard(session,hero);
                    if(attempt==0){ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:1);ClericDefender(session);}
                    ClericEnd(session,hero);ClericDefender(session);
                    after=ShortRestCapture(session);incoming=after.MeleeAttacks.Where(x=>x.Revision>before.Revision&&x.TargetId==actor).ToArray();
                }
                File.WriteAllText(Path.Combine(directory,"tac08-ward-attack-witness.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    cast=cast.SpellCasts.Last(),effect=after.SpellEffects.Last(),attacks=after.MeleeAttacks.Where(x=>x.Revision>before.Revision).ToArray(),
                    clock=after.RuleClock.ToString(),phase=after.Reinforcement.Admission.Phase.Epoch.Id}));
                Require(incoming.Length>0 && incoming.All(x=>x.Attack.ArmorClass==9&&x.At<effect.ExpiresAt),
                    "A real attack did not use base10, Aggressive-2 and Ward+1 before expiry.");
                Require(after.RuleClock==effect.ExpiresAt && !after.SpellEffects.Last().Present
                    && after.SpellEffects.Last().EndReason==SpellEffectEndReason.Expired
                    && after.SpellEffects.Last().ExpiryTurn.LocalStart==WorldTiming.ForActor(after,actor).ProcessedSlot
                    && after.ResonancePools.Single().Current==3,"Ward did not end at the actual next caster Start.");
                var bytes=codec.Encode(after);string path=Path.Combine(directory,"tac08-expired-ward.ddsave");session.Save(path);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Ward attack/expiry failed independent restore replay.");
                Require(SpellCastingProfile.CombineFlatArmorBonuses(1,1,2,1)==3
                    && SpellCastingProfile.CombineFlatArmorBonuses(1,1,0,1)==1
                    && SpellCastingProfile.CombineFlatArmorBonuses(1,0,0,2)==2,"Strongest-flat composition lost the explicit Guard exception.");
            });
            cases.Add("tac08_focus_handling_and_unsafe_consumable_denials", () => {
                var session=NewCastingExpedition(); var codec=new SnapshotCodec(); const string actor=ClericRpProfile.Actor;
                var initial=ShortRestCapture(session); var simulation=CastingSimulation(session); var authority=CastingAuthority();
                RetainClericDenial(simulation,authority,new Command("tac08.unclean-intake",actor,0,CommandKind.StartIntake,
                    SpellCastingProfile.ContaminatedWaterId,inventory:new InventoryRequest(new RuleQuantity(1))),"UnsafeConsumableIntakeUnsupported",directory);
                RetainClericDenial(simulation,authority,new Command("tac08.unclean-split",actor,0,CommandKind.PortionInventory,
                    SpellCastingProfile.ContaminatedWaterId,inventory:new InventoryRequest(new RuleQuantity(1,2))),"ContaminationPropagationUnsupported",directory);
                RetainClericDenial(simulation,authority,new Command("tac08.unclean-mix",actor,0,CommandKind.StartWaterFill,
                    TestOnlyFillingPolicy.SupplyId,inventory:new InventoryRequest(new RuleQuantity(1),TestOnlyFillingPolicy.FlaskId)),
                    "ContaminationPropagationUnsupported",directory);
                var initialBurden=PortableEquipmentRules.CarriedBurden(initial,actor);
                CommitVialRoute(session,new Command("tac08.focus-remove",actor,0,CommandKind.RemovePortableItem,SpellCastingProfile.FocusId));
                var removed=ShortRestCapture(session);
                Require(removed.RuleClock==initial.RuleClock.AddSeconds(1) && removed.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId).HeldHands==1
                    && PortableEquipmentRules.CarriedBurden(removed,actor).Pounds==initialBurden.Pounds,"Remove did not pay work or preserve focus mass.");
                RetainClericDenial(CastingSimulation(session),authority,new Command("tac08.focus-store",actor,removed.Revision,
                    CommandKind.HandlePortableEquipment,SpellCastingProfile.FocusId,
                    inventory:new InventoryRequest(new RuleQuantity(1),PortableKitFixture.Pack,HandlingKind.Stow)),"SpellFocusStorageUnsupported",directory);
                CommitVialRoute(session,new Command("tac08.focus-drop",actor,removed.Revision,CommandKind.HandlePortableEquipment,SpellCastingProfile.FocusId,
                    inventory:new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Drop)));
                var dropped=ShortRestCapture(session);var item=dropped.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId);
                Require(item.Placement==PortablePlacement.Ground && item.HeldHands==0
                    && PortableEquipmentRules.CarriedBurden(dropped,actor).Pounds==initialBurden.Pounds-new RuleQuantity(1),"Drop did not remove actual carried focus mass.");
                CommitVialRoute(session,new Command("tac08.focus-pickup",actor,dropped.Revision,CommandKind.HandlePortableEquipment,SpellCastingProfile.FocusId,
                    inventory:new InventoryRequest(new RuleQuantity(1))));
                var picked=ShortRestCapture(session);
                foreach(var step in new[]{(-1,0),(-1,0),(0,-1),(-1,0),(0,-1)}) {
                    ClericCommit(session,actor,CommandKind.BeginWorldStep,"walk",step.Item1,step.Item2);
                    ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                }
                var handover=new Command("tac08.focus-handover",actor,ShortRestCapture(session).Revision,CommandKind.HandlePortableEquipment,SpellCastingProfile.FocusId,
                    inventory:new InventoryRequest(new RuleQuantity(1),ConnectedExpeditionSession.Hero,HandlingKind.Handover));
                var handoverQuery=CastingSimulation(session).QueryCommand(authority,handover);
                Require(handoverQuery.Admissible,"Focus handover preflight: "+handoverQuery.Code+"; positions="
                    +string.Join(";",ShortRestCapture(session).Actors.Select(x=>x.Id+":"+x.X+","+x.Y)));
                session.Save(Path.Combine(directory,"tac08-focus-handover-ready.ddsave"));
                RetainClericDenial(CastingSimulation(session),new Authority("TEST_ONLY.no-consent",new[]{actor,ConnectedExpeditionSession.Hero},
                    inventoryOwners:new[]{actor,ConnectedExpeditionSession.Hero}),handover,"RecipientNotWilling",directory);
                CommitVialRoute(session,handover);
                var handed=ShortRestCapture(session);var held=handed.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId);
                Require(held.OwnerId==actor&&held.CustodianId==ConnectedExpeditionSession.Hero&&held.HeldHands==1,
                    "A paid handover must move the same held focus without changing ownership.");
                CommitVialRoute(session,new Command("tac08.focus-return",ConnectedExpeditionSession.Hero,handed.Revision,CommandKind.HandlePortableEquipment,SpellCastingProfile.FocusId,
                    inventory:new InventoryRequest(new RuleQuantity(1),actor,HandlingKind.Handover)));
                RetainClericDenial(CastingSimulation(session),authority,new Command("tac08.focus-wear-spent",actor,ShortRestCapture(session).Revision,
                    CommandKind.EquipPortableItem,SpellCastingProfile.FocusId),"OffCalendarActionAlreadySpent",directory);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                var wear=new Command("tac08.focus-wear",actor,ShortRestCapture(session).Revision,CommandKind.EquipPortableItem,SpellCastingProfile.FocusId);
                var wearQuery=CastingSimulation(session).QueryCommand(authority,wear);
                Require(wearQuery.Admissible,"Focus wearing preflight: "+wearQuery.Code);
                CommitVialRoute(session,wear);
                var final=ShortRestCapture(session); var bytes=codec.Encode(final); string path=Path.Combine(directory,"tac08-focus-handling.ddsave");
                session.Save(path);session.Restore(path);
                Require(final.RuleClock==initial.RuleClock.AddSeconds(42) && final.PortableHandling.Length==6
                    && final.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId).Placement==PortablePlacement.Worn
                    && final.ResonancePools.Single().Current==3 && final.ConsumableContamination.Single().Present
                    && final.Work.Lots.Single(x=>x.Id==SpellCastingProfile.ContaminatedWaterId).Amount==new RuleQuantity(1)
                    && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Paid focus history or untouched finite water failed strict replay.");
            });
            cases.Add("tac08_genuine_first_cast_spends_real_action_and_replays", () => {
                var initial=NewCastingExpedition(); var initialSimulation=CastingSimulation(initial);
                RetainClericDenial(initialSimulation,CastingAuthority(),new Command("tac08.before-calendar",ClericRpProfile.Actor,0,
                    CommandKind.CastKnownSpell,ClericRpProfile.Actor,spellCast:new SpellCastRequest("guidance",willingTarget:true)),
                    "SpellcastingCalendarUnsupported",directory);
                var session=CastingFirstOwnTurn(); var before=ShortRestCapture(session); var codec=new SnapshotCodec();
                var command=new Command("tac08.first-guidance",ClericRpProfile.Actor,before.Revision,CommandKind.CastKnownSpell,
                    ClericRpProfile.Actor,spellCast:new SpellCastRequest("guidance",willingTarget:true));
                var simulation=CastingSimulation(session); var authority=CastingAuthority(); var bytes=codec.Encode(before);
                var query=simulation.QueryCommand(authority,command);
                Require(query.Admissible && bytes.SequenceEqual(Bytes(simulation)),"Legal cast query denied or changed actual state: "+query.Code);
                session.Save(Path.Combine(directory,"tac08-before-first-cast.ddsave"));
                CommitVialRoute(session,command); var after=ShortRestCapture(session); var cast=after.SpellCasts.Single();
                var effect=after.SpellEffects.Single();
                Require(after.Revision==before.Revision+1 && after.RuleClock==before.RuleClock && after.RandomState==before.RandomState
                    && after.ResonancePools.Single().Current==3 && cast.BaseRp==0 && cast.Surcharge==0 && cast.SpellDc==12
                    && cast.Turn.LocalStart==WorldTiming.ForActor(before,ClericRpProfile.Actor).ProcessedSlot
                    && after.WorldIntervals.Single(x=>x.ActorId==ClericRpProfile.Actor).ActionSpent
                    && effect.SpellId=="guidance" && effect.Present && effect.ExpiresAt==before.RuleClock.AddSeconds(60),
                    "First actual cast did not preserve finite RP and shared clock/RNG or spend its owning Action.");
                var saved=codec.Encode(after); string path=Path.Combine(directory,"tac08-after-first-cast.ddsave");session.Save(path);session.Restore(path);
                Require(saved.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Actual cast failed strict command replay.");
                simulation=CastingSimulation(session);
                Require(simulation.Execute(authority,command).Outcome==Outcome.Duplicate && saved.SequenceEqual(Bytes(simulation)),"Cast retry duplicated its payment or effect.");
                RetainClericDenial(simulation,authority,new Command("tac08.spent-action",ClericRpProfile.Actor,after.Revision,
                    CommandKind.CastKnownSpell,ClericRpProfile.Actor,spellCast:new SpellCastRequest("guidance",willingTarget:true)),
                    "ActionAlreadySpent",directory);
                ClericEnd(session,ClericRpProfile.Actor); var ended=ShortRestCapture(session);
                Require(ended.CastingTurnEnds.Length==1 && ended.CastingTurnEnds[0].MagicalActivity
                    && ended.CastingTurnEnds[0].After==0 && ended.SpellEffects.Single().Present,"Cast activity was not settled at the actual regular End.");
                session.Save(Path.Combine(directory,"tac08-after-caster-end.ddsave"));
            });
            cases.Add("tac08_initial_physical_state_and_wire_isolation", () => {
                var session=ConnectedExpeditionSession.StartWithClericCasting(ClericInitialSelection.AuthoredExample(),
                    ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());
                var state=ShortRestCapture(session); var codec=new SnapshotCodec();
                var focus=state.PortableEquipment.Single(x=>x.Id==SpellCastingProfile.FocusId);
                var lot=state.Work.Lots.Single(x=>x.Id==SpellCastingProfile.ContaminatedWaterId);
                Require(state.WireSchemaVersion==109 && state.SchemaVersion==90 && state.ConnectedClericSettlement
                    && state.ResonancePools.Single().Current==3 && state.KnownSpells.Length==5 && state.SpellCasts.Length==0
                    && state.CastingStrain.Single().Dissonance==0 && state.ClericInvocationPath==null,
                    "Casting selection manufactured a cast, earned knowledge or funding.");
                Require(focus.OwnerId==ClericRpProfile.Actor && focus.CustodianId==ClericRpProfile.Actor && focus.Placement==PortablePlacement.Worn
                    && focus.SourceWeightLb==new RuleQuantity(1) && focus.HeldHands==0 && lot.Amount==new RuleQuantity(1)
                    && lot.LocationId==TestOnlyFillingPolicy.FlaskId && state.ConsumableContamination.Single().Present,
                    "Declared focus and contaminated pint do not use their real physical records.");
                byte[] bytes=codec.Encode(state);
                Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Wire109 initial state does not round-trip.");
                string viewBefore=System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player));
                string path=Path.Combine(directory,"tac08-initial.ddsave"); session.Save(path); session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Strict initial replay changed casting authority.");
                Require(viewBefore==System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player)),
                    "The public inventory or mining view changed order across initial restore.");
                var old=ShortRestCapture(NewClericSettlement()); var oldBytes=codec.Encode(old);
                Require(old.WireSchemaVersion==108 && old.CastingStrain.Length==0 && old.ConsumableContamination.Length==0
                    && !old.PortableEquipment.Any(x=>x.Id==SpellCastingProfile.FocusId)
                    && oldBytes.SequenceEqual(codec.Encode(codec.Decode(oldBytes))),"The old profile acquired casting or new physical stock.");
                old.CastingStrain=state.CastingStrain; Throws<ArgumentException>(()=>codec.Encode(old));
                var corrupt=state.Copy(); corrupt.ConsumableContamination=Array.Empty<ConsumableContaminationRecord>();
                Throws<ArgumentException>(()=>codec.Encode(corrupt));
            });
            cases.Add("tac08_casting_receipts_preserve_choices_and_reject_aliases", () => {
                const string actor = TestOnlyPolicy.CompanionId, target = TestOnlyPolicy.ActorId;
                CommandReceipt Receipt(CommandKind kind, string subject, string tail, int x = 0, int y = 0)
                    => new CommandReceipt { Principal = "TEST_ONLY.host", Id = "casting.receipt", Revision = 4,
                        Fingerprint = ((int)kind).ToString(CultureInfo.InvariantCulture) + "|" + actor + "|" + subject
                            + "|3|" + x.ToString(CultureInfo.InvariantCulture) + "|" + y.ToString(CultureInfo.InvariantCulture) + tail };
                var cast = Receipt(CommandKind.CastKnownSpell, target,
                    "|spell-cast-v1|sanctuary|TEST_ONLY.cleric-casting.holy-symbol|1|1");
                var command = CommandHistory.Read(cast);
                Require(command.MatchesReceipt(cast) && command.SpellCast.SpellId == "sanctuary"
                    && command.SpellCast.WillingTarget && command.SpellCast.ElectFocusedDc
                    && command.SpellCast.FocusItemId == SpellCastingProfile.FocusId && command.Target == target,
                    "Casting replay lost source, target, focus, consent or elected stance benefit.");
                foreach (var kind in new[] { CommandKind.Hide, CommandKind.Search, CommandKind.StabilizeCompanion }) {
                    var receipt = Receipt(kind, target, "|guidance-v1|spell.effect.2", kind == CommandKind.Search ? 1 : 0);
                    var check = CommandHistory.Read(receipt);
                    Require(check.MatchesReceipt(receipt) && check.Guidance.EffectId == "spell.effect.2"
                        && check.SpellCast == null, "Guidance choice did not survive its actual check command.");
                }
                foreach (var choice in new[] { SanctuaryResponseKind.Forgo, SanctuaryResponseKind.Retarget }) {
                    var receipt = Receipt(CommandKind.RespondSanctuary, "sanctuary.pending.3",
                        "|sanctuary-response-v1|" + ((int)choice).ToString(CultureInfo.InvariantCulture) + "|"
                            + (choice == SanctuaryResponseKind.Retarget ? target : ""));
                    Require(CommandHistory.Read(receipt).MatchesReceipt(receipt), "Sanctuary continuation choice changed in replay.");
                }
                var legacy = Receipt(CommandKind.CastKnownSpell, "sanctuary", "");
                Require(CommandHistory.Read(legacy).MatchesReceipt(legacy) && CommandHistory.Read(legacy).SpellCast == null,
                    "The pre-casting historical command shape was rewritten.");
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(CommandKind.CastKnownSpell, target,
                    "|spell-cast-v1|sanctuary||true|0")));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(CommandKind.CastKnownSpell, target,
                    "|spell-cast-v1|sanctuary||0|0|guidance-v1|spell.effect.2")));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(CommandKind.RespondSanctuary, "pending",
                    "|sanctuary-response-v1|1|" + target)));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(CommandKind.RespondSanctuary, "pending", "")));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(CommandKind.UseHealingRite, target,
                    "|guidance-v1|spell.effect.2")));
            });

            cases.Add("tac08_old_profile_rejects_new_casting_payloads_without_mutation", () => {
                var simulation = New(); var host = TestOnlyPolicy.Host(); const string actor = TestOnlyPolicy.ActorId;
                var commands = new[] {
                    new Command("casting.old.cast", actor, 0, CommandKind.CastKnownSpell, actor,
                        spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,true)),
                    new Command("casting.old.guidance", actor, 0, CommandKind.Search, "turn.0", guidance:new GuidanceChoice("spell.effect.1")),
                    new Command("casting.old.response", actor, 0, CommandKind.RespondSanctuary, "pending.1",
                        sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo)),
                    new Command("casting.old.ground", actor, 0, CommandKind.GroundCastingStrain),
                    new Command("casting.old.end", actor, 0, CommandKind.EndSpellConcentration,"spell.effect.1"),
                    new Command("casting.old.focus", actor, 0, CommandKind.FocusDetectedAura,"aura.1")
                };
                foreach (var command in commands) {
                    var before = Bytes(simulation);
                    Require(!simulation.QueryCommand(host,command).Admissible && before.SequenceEqual(Bytes(simulation)),
                        "An old-profile query consumed state or advertised new casting.");
                    RejectUnchanged(simulation,host,command,"OrdinarySpellcastingUnsupported");
                    RejectUnchanged(simulation,host,command,"OrdinarySpellcastingUnsupported");
                }
                Require(simulation.Capture().Revision == 0 && simulation.Capture().Receipts.Length == 0,
                    "Rejected new choices created history in an old profile.");
            });

            cases.Add("tac08_cadence_and_effect_history_preserve_source_boundaries", () => {
                const string actor = TestOnlyPolicy.CompanionId;
                var strain = new CastingStrainRecord(actor);
                int[] totals = { 0, 1, 3, 6, 9 };
                for (int i = 0; i < totals.Length; i++) {
                    strain = strain.BeginAdmittedCast("arcane-ward",0,i+1);
                    Require(strain.Dissonance == totals[i],"Same-name cantrip cadence differed from the source progression.");
                }
                strain = strain.ReduceAtSettledEnd(2).BeginAdmittedCast("arcane-ward",0,6);
                Require(strain.Dissonance == 10 && strain.Refrain == 3, "Reduction incorrectly reset the repeated spell identity.");
                strain = strain.BeginAdmittedCast("guidance",0,7);
                Require(strain.Dissonance == 10 && strain.Refrain == 0 && strain.RankedSurcharge(2,2) == 2
                    && !strain.RankedBlocked(2,2),"Different spell reset accumulated strain or changed pre-cast thresholds.");
                strain = strain.BeginAdmittedCast("guidance",0,8).BeginAdmittedCast("guidance",0,9);
                Require(strain.RankedBlocked(2,2) && strain.LastCastRevision == 9,
                    "Ordinary ranked blocking did not preserve chronological repeat buildup.");
                var normal = new SpellTurnIdentity(actor,"epoch.1",3,5);
                var carried = new SpellTurnIdentity(actor,"epoch.1",-1,0,2);
                Require(!normal.SameAs(carried) && carried.IsCarried && carried.GlobalStart == 0,
                    "A carried interval was mistaken for a new regular Start.");
                Throws<ArgumentException>(() => new SpellTurnIdentity(actor,"epoch.1",-1,0));
                _ = new CastingTurnEndRecord(normal,"end.1",10,new RuleTime(12),13,13,true,true,2);
                _ = new CastingTurnEndRecord(normal,"end.1",10,new RuleTime(12),13,11,false,true,2);
                Throws<ArgumentException>(() => new CastingTurnEndRecord(normal,"end.1",10,new RuleTime(12),13,10,false,true,2));
                var effect = new SpellEffectRecord("effect.1","cast.1",1,"guidance",actor,actor,
                    default,new RuleTime(60),SpellExpiryKind.Absolute,null,false);
                var ended = effect.End("check.1",2,new RuleTime(5),SpellEffectEndReason.GuidanceConsumed);
                Require(effect.Present && !ended.Present && ended.CastId == effect.CastId && ended.ExpiresAt == effect.ExpiresAt,
                    "Ending an immutable effect rewrote its origin or duration.");
                Throws<InvalidOperationException>(() => ended.End("check.2",3,new RuleTime(6),SpellEffectEndReason.GuidanceConsumed));
                var ordinary = new ConsumableContaminationRecord("taint.1","lot.1","initial.1",0,ConsumableContaminationKind.OrdinaryPathogen);
                var removed = ordinary.Destroy("purify.1",1);
                Require(ordinary.Present && !removed.Present && removed.LotId == ordinary.LotId && removed.OriginId == ordinary.OriginId,
                    "Purification replaced physical lineage instead of recording destruction.");
                var magical = new ConsumableContaminationRecord("taint.2","lot.1","initial.1",0,ConsumableContaminationKind.MagicalPoison);
                Throws<InvalidOperationException>(() => magical.Destroy("purify.1",1));
            });
        }
    }
}
#endif
