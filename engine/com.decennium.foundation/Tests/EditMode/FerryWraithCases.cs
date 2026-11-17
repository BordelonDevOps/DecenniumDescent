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
        private static ConnectedExpeditionSession RunFerryAdmission(string directory)
        {
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
            return session;
        }
        private static void AddFerryWraithCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("tac10_ferry_public_dash_paid_movement_and_authorized_retry",()=>{
                var ordinary=NewFerryExpedition();var ordinaryCodec=new SnapshotCodec();var ordinaryBefore=ordinaryCodec.Encode(ShortRestCapture(ordinary));
                var outside=new Command("ferry.public.outside",FerryWraithProfile.Hero,ShortRestCapture(ordinary).Revision,CommandKind.EncounterDash,"TEST_ONLY.turn");
                Require(!ordinary.View(ExpeditionSeat.Player).Commands.Contains(CommandKind.EncounterDash)
                    &&!ordinary.QueryCastingCommand(ExpeditionSeat.Player,outside).Admissible
                    &&ordinary.Submit(ExpeditionSeat.Player,outside).Response==ExpeditionResponse.Unavailable
                    &&ordinaryBefore.SequenceEqual(ordinaryCodec.Encode(ShortRestCapture(ordinary))),"Selected profile alone admitted Dash outside actual Ferry combat.");
                var session=RunFerryAdmission(directory);var codec=new SnapshotCodec();var checks=new List<string>();
                const string hero=FerryWraithProfile.Hero,companion=FerryWraithProfile.Companion;
                Snapshot State()=>ShortRestCapture(session);
                byte[] Bytes()=>codec.Encode(State());
                Command Dash(string id,string actor=null,string turn=null,long? revision=null,int x=0,int y=0,
                    CombatRequest combat=null,SpellCastRequest spell=null)
                    =>new Command("ferry.public.dash."+id,actor??State().Encounter.CurrentActor,revision??State().Revision,
                        CommandKind.EncounterDash,turn??State().Encounter.CurrentTurnId,x,y,combat:combat,spellCast:spell);
                void PureDenied(string label,Command command,ExpeditionSeat seat=ExpeditionSeat.Player,
                    ExpeditionResponse expected=ExpeditionResponse.Unavailable) {
                    var before=Bytes();var query=session.QueryCastingCommand(seat,command);
                    Require(!query.Admissible&&session.Submit(seat,command).Response==expected&&before.SequenceEqual(Bytes()),
                        "Public Dash denial changed state or admitted "+label);checks.Add(label);
                }
                void Guard(bool focused=false) {
                    var s=State();BishopCommit(session,new Command("ferry.public.stance."+s.Revision,s.Encounter.CurrentActor,s.Revision,
                        CommandKind.SelectCombatStance,combat:new CombatRequest(s.Encounter.CurrentTurnId,stance:(int)(focused?CombatStance.Focused:CombatStance.Guarded))));
                }
                void End() {var s=State();BishopCommit(session,new Command("ferry.public.end."+s.Revision,s.Encounter.CurrentActor,s.Revision,CommandKind.EndRegularTurn,s.Encounter.CurrentTurnId));}
                void Auto() {Require(session.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Actual Ferry controller failed during public Dash route.");}
                void Step(string actor,int x,int y) {var s=State();BishopCommit(session,new Command("ferry.public.step."+s.Revision,actor,s.Revision,CommandKind.TacticalStep,s.Encounter.CurrentTurnId,x,y));}
                Require(State().Encounter.CurrentActor==hero&&State().Encounter.TurnOrdinal==0,"Expected actual hero admission Start0.");
                Guard();End();
                for(int i=0;i<16&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.FerryOpponent;i++)Auto();
                Require(State().Encounter.CurrentActor==companion,"Public Dash route missed the actual companion Start.");
                Guard();
                Require(session.View(ExpeditionSeat.Player).Commands.Contains(CommandKind.EncounterDash)
                    &&!session.View(ExpeditionSeat.FerryOpponent).Commands.Contains(CommandKind.EncounterDash),"Public command views expose the wrong Dash seats.");
                var companionOptions=session.DiscoverCastingCommands(ExpeditionSeat.Player,companion).Where(x=>x.Command.Kind==CommandKind.EncounterDash).ToArray();
                Require(companionOptions.Length==1&&companionOptions[0].Query.Admissible,"Party companion has no actual Dash discovery.");
                BishopCheckpoint(session,directory,"dash-companion-before");
                BishopCommit(session,companionOptions[0].Command);BishopCheckpoint(session,directory,"dash-companion-paid");
                session.Restore(Path.Combine(directory,"dash-companion-before.ddsave"));
                // Alternate genuine branch: retain both saves, then continue the original unspent Action.
                Step(companion,9,3);Step(companion,10,2);
                var guidance=session.DiscoverCastingCommands(ExpeditionSeat.Player,companion)
                    .Single(x=>x.Command.Kind==CommandKind.CastKnownSpell&&x.Command.SpellCast.SpellId=="guidance"&&x.Command.Target==hero);
                Require(guidance.Query.Admissible,"Actual Guidance setup unavailable.");BishopCommit(session,guidance.Command);
                PureDenied("spent Action",Dash("spent"));End();Guard(true);
                Step(hero,7,2);
                Require(State().TacticalMoves.Any(x=>x.Pending),"Expected genuine source opportunity before paying Dash.");
                PureDenied("pending opportunity",Dash("pending"));BishopCheckpoint(session,directory,"dash-pending-opportunity");Auto();
                Require(!State().TacticalMoves.Any(x=>x.Pending),"Actual source opportunity did not finish.");
                var beforeDash=State();var beforeInterval=beforeDash.WorldIntervals.Single(x=>x.ActorId==hero);
                Require(beforeInterval.MovementSpent==new RuleQuantity(5),"The first actual edge did not spend5ft.");
                PureDenied("wrong turn",Dash("wrong-turn",turn:"TEST_ONLY.wrong-turn"));
                PureDenied("old epoch",Dash("wrong-epoch",turn:"TEST_ONLY.recovery-turn"));
                PureDenied("wrong current party actor",Dash("wrong-actor",actor:companion));
                PureDenied("nonzero x",Dash("x",x:1));PureDenied("nonzero y",Dash("y",y:1));
                PureDenied("unrelated combat",Dash("combat",combat:new CombatRequest(beforeDash.Encounter.CurrentTurnId)));
                PureDenied("unrelated spell",Dash("spell",spell:new SpellCastRequest("guidance")));
                PureDenied("unauthorized opponent seat",Dash("opponent"),ExpeditionSeat.FerryOpponent,ExpeditionResponse.NotAuthorized);
                PureDenied("creature cannot acquire party Dash",Dash("creature",actor:FerryWraithProfile.Actor),ExpeditionSeat.FerryOpponent);
                PureDenied("stale revision",Dash("stale",revision:beforeDash.Revision-1),expected:ExpeditionResponse.StaleRevision);
                var beforeQuery=Bytes();var options=session.DiscoverCastingCommands(ExpeditionSeat.Player,hero).Where(x=>x.Command.Kind==CommandKind.EncounterDash).ToArray();
                Require(options.Length==1&&beforeQuery.SequenceEqual(Bytes()),"Dash discovery is absent, duplicated or impure.");
                var dash=options[0].Command;var query=session.QueryCastingCommand(ExpeditionSeat.Player,dash);
                Require(query.Supported&&query.Admissible&&query.Costs.Count==1&&query.Costs[0].Kind=="action"
                    &&query.Costs[0].Amount==1&&beforeQuery.SequenceEqual(Bytes()),"Dash query did not expose the pure shared one-Action payment.");
                session.SetSeatEnabled(ExpeditionSeat.Player,false);
                PureDenied("revoked fresh request",dash,expected:ExpeditionResponse.NotAuthorized);
                session.SetSeatEnabled(ExpeditionSeat.Player,true);BishopCommit(session,dash);
                var paid=State();var interval=paid.WorldIntervals.Single(x=>x.ActorId==hero);
                Require(interval.ActionSpent&&interval.DashPaid&&interval.MovementSpent==beforeInterval.MovementSpent
                    &&paid.RuleClock==beforeDash.RuleClock&&paid.RandomState==beforeDash.RandomState,"Dash changed movement already spent, time or RNG, or omitted its Action.");
                var stable=Bytes();Require(session.Submit(ExpeditionSeat.Player,dash).Response==ExpeditionResponse.Duplicate&&stable.SequenceEqual(Bytes()),"Immediate Dash retry repaid.");
                var conflict=new Command(dash.Id,dash.Actor,dash.ExpectedRevision,CommandKind.EncounterDash,"TEST_ONLY.conflicting-turn");
                PureDenied("conflicting receipt ID",conflict,expected:ExpeditionResponse.CommandIdConflict);
                BishopCheckpoint(session,directory,"dash-hero-paid");
                foreach(var cell in new[]{new CombatCell(6,3),new CombatCell(5,2),new CombatCell(4,2),new CombatCell(3,1),new CombatCell(2,0)})Step(hero,cell.X,cell.Y);
                var routed=State();var spent=routed.WorldIntervals.Single(x=>x.ActorId==hero).MovementSpent;
                Require(spent==new RuleQuantity(35)&&spent>new RuleQuantity(TestOnlyClubAttackPolicy.WalkingSpeed(routed,hero)),"Actual route did not use movement beyond the undashed allowance.");
                End();stable=Bytes();
                Require(session.Submit(ExpeditionSeat.Player,dash).Response==ExpeditionResponse.Duplicate
                    &&session.QueryCastingCommand(ExpeditionSeat.Player,dash).Code=="AlreadyCommitted"&&stable.SequenceEqual(Bytes()),"Exact Dash retry failed after the turn changed.");
                session.SetSeatEnabled(ExpeditionSeat.Player,false);
                PureDenied("revoked exact retry",dash,expected:ExpeditionResponse.NotAuthorized);
                session.SetSeatEnabled(ExpeditionSeat.Player,true);
                for(int i=0;i<16&&session.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.FerryOpponent;i++)Auto();
                Require(State().Encounter.CurrentActor==companion,"Dash route did not reach companion Start5.");Guard();End();Guard(true);
                var hide=session.DiscoverCastingCommands(ExpeditionSeat.Player,hero).Single(x=>x.Command.Kind==CommandKind.Hide&&x.Command.Guidance!=null);
                Require(hide.Query.Admissible,"The public Dash route did not reach an eligible guided Hide.");BishopCommit(session,hide.Command);
                Require(State().GuidanceUses.Any(x=>x.CheckKind==GuidanceCheckKind.Hide),"Public route did not consume Guidance on the actual check.");
                End();BishopCheckpoint(session,directory,"dash-guidance-continued");
                var legacy=NewDeclaredGeometryExpedition();var legacyBefore=codec.Encode(ShortRestCapture(legacy));
                var unsupported=new Command("ferry.public.legacy",hero,ShortRestCapture(legacy).Revision,CommandKind.EncounterDash,"TEST_ONLY.turn");
                Require(!legacy.View(ExpeditionSeat.Player).Commands.Contains(CommandKind.EncounterDash)
                    &&!legacy.QueryCastingCommand(ExpeditionSeat.Player,unsupported).Supported
                    &&legacy.Submit(ExpeditionSeat.Player,unsupported).Response==ExpeditionResponse.Unavailable
                    &&legacyBefore.SequenceEqual(codec.Encode(ShortRestCapture(legacy))),"Historical geometry host acquired new Dash behavior.");
                File.WriteAllText(Path.Combine(directory,"public-dash-checks.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Genuine public party Dash and Guided Hide continuation; alternate paid companion branch retained separately; not five paths or whole-module acceptance",
                    checks,beforeInterval,paidInterval=interval,spent,query,finalRevision=State().Revision,finalClock=State().RuleClock}));
            });
            cases.Add("tac10_seal_uses_owned_action_and_original_deadline",()=>{
                // Detached, explicitly mechanical arrangements. Genuine gameplay and verified saves
                // are retained by Probe-FerrySeal; these do not manufacture a playable campaign.
                var session=NewFerryExpedition();var initial=ShortRestCapture(session);var policy=ClericPolicy(session);
                var codec=new SnapshotCodec();var unchanged=codec.Encode(initial);var rows=new List<object>();
                var resolve=typeof(TestOnlySharedWorldPolicy).GetMethod("ResolveFerrySeal",BindingFlags.Instance|BindingFlags.NonPublic);
                var expire=typeof(TestOnlySharedWorldPolicy).GetMethod("ExpireFerrySealSuppression",BindingFlags.Static|BindingFlags.NonPublic);
                string Resolve(Snapshot s,Command c,bool assess=false)=>(string)resolve.Invoke(policy,new object[]{s,c,assess});
                Snapshot Arrange(string actor,long slot=0) {
                    var s=initial.Copy();s.InventoryCombat=false;s.InventoryTurnActor="";
                    s.WorldSchedule=s.WorldSchedule.At(slot);s.RuleClock=s.WorldSchedule.Start(slot);
                    var body=s.Actors.Single(x=>x.Id==actor);body.X=8;body.Y=3;
                    s.WorldIntervals=s.WorldIntervals.Select(x=>x.ActorId==actor?new WorldIntervalRecord(actor,x.LastStart):x).ToArray();
                    return s;
                }
                Command Tear(Snapshot s,string actor,string suffix="")=>new Command("seal.mechanical"+suffix,actor,s.Revision,
                    CommandKind.TearExposedSeal,FerryWraithProfile.Seal);
                const string hero=FerryWraithProfile.Hero;
                int own=initial.WorldSchedule.Order.ToList().IndexOf(hero);
                Require(own>=0,"Mechanical scheduled control has no actual hero calendar.");
                string off=initial.WorldActivityIntervals.Select(x=>x.ActorId).First(x=>initial.Characters.Any(y=>y.ActorId==x)
                    &&WorldTiming.ForActor(initial,x)==null);
                foreach(var spec in new[]{(Actor:hero,Slot:(long)own,Initiative:false),
                    (Actor:hero,Slot:(long)((own+1)%initial.WorldSchedule.Order.Count),Initiative:false),
                    (Actor:off,Slot:0L,Initiative:false),(Actor:hero,Slot:(long)own+initial.WorldSchedule.Order.Count,Initiative:true)}) {
                    var s=Arrange(spec.Actor,spec.Slot);
                    if(spec.Initiative) {
                        s.InventoryCombat=true;s.InventoryTurnActor=spec.Actor;
                        s.Encounter=new FixedEncounterRecord("TEST_ONLY.mechanical-seal",s.WorldSchedule.Origin,s.WorldSchedule.Order,
                            new[]{s.Revision+1},new[]{checked((int)spec.Slot)});
                    }
                    var command=Tear(s,spec.Actor);var beforeClock=s.RuleClock;uint beforeRng=s.RandomState;
                    Require(Resolve(s,command,true)==null&&s.FerryWraith.Rupture==null,"Seal assessment mutated or rejected a valid arrangement.");
                    Require(Resolve(s,command)==null,"Owned Action seal control rejected.");
                    var rupture=s.FerryWraith.Rupture;
                    bool scheduled=WorldTiming.ForActor(s,spec.Actor)!=null;
                    Require(rupture!=null&&s.RuleClock==beforeClock&&s.RandomState==beforeRng
                        &&rupture.ActionLedger==(scheduled?SealActionLedger.Scheduled:SealActionLedger.OffCalendar),"Seal changed time/RNG or chose a new Action ledger.");
                    Require(scheduled?s.WorldIntervals.Single(x=>x.ActorId==spec.Actor).ActionSpent
                        :s.WorldActivityIntervals.Single(x=>x.ActorId==spec.Actor).Action==WorldActionCommitment.SealTear,"Seal did not debit its owned Action.");
                    Require(rupture.ExpiresAt==(spec.Initiative?s.WorldSchedule.Origin.AddSeconds(18):beforeClock.AddSeconds(6)),
                        "Seal used the wrong original cycle/world deadline.");
                    Require(Resolve(s,Tear(s,spec.Actor,".again"))=="ExposedSealAlreadyTorn"&&ReferenceEquals(rupture,s.FerryWraith.Rupture),
                        "Second rupture renewed or replaced the original timer.");
                    s.Revision++;
                    s.RuleClock=new RuleTime(checked(rupture.ExpiresAt.Numerator*2-rupture.ExpiresAt.Denominator),
                        checked(rupture.ExpiresAt.Denominator*2));expire.Invoke(null,new object[]{s});
                    Require(s.FerryWraith.ClawSuppressed,"Claw suppression expired before its endpoint.");
                    s.InventoryCombat=false;s.InventoryTurnActor=""; // Mode closure does not replace the saved basis.
                    s.RuleClock=rupture.ExpiresAt;expire.Invoke(null,new object[]{s});
                    Require(!s.FerryWraith.ClawSuppressed&&s.FerryWraith.SealDestroyed&&ReferenceEquals(rupture,s.FerryWraith.Rupture),
                        "Original endpoint did not expire suppression while retaining destruction.");
                    long expired=s.FerryWraith.SuppressionExpiredRevision;s.RuleClock=s.RuleClock.AddSeconds(1);expire.Invoke(null,new object[]{s});
                    Require(s.FerryWraith.SuppressionExpiredRevision==expired,"Already expired suppression was renewed or expired twice.");
                    if(!scheduled)Throws<InvalidOperationException>(()=>s.WorldActivityIntervals.Single(x=>x.ActorId==spec.Actor).CommitActiveLabor("probe.work"));
                    rows.Add(new{spec.Actor,spec.Slot,spec.Initiative,rupture,beforeRng,afterRng=s.RandomState,expired});
                }
                var spent=Arrange(hero,own);spent.WorldIntervals=spent.WorldIntervals.Select(x=>x.ActorId==hero?x.PayAction():x).ToArray();
                Require(Resolve(spent,Tear(spent,hero))=="ActionAlreadySpent"&&spent.FerryWraith.Rupture==null,"Spent scheduled Action was reset.");
                var noHand=Arrange(FerryWraithProfile.Actor);Require(Resolve(noHand,Tear(noHand,FerryWraithProfile.Actor))=="UsableHandRequired",
                    "Printed natural Claw invented a free grasping hand.");
                var far=Arrange(hero);far.Actors.Single(x=>x.Id==hero).X=7;
                Require(Resolve(far,Tear(far,hero))=="SealOutOfReach","Out-of-reach seal was torn.");
                var unseen=Arrange(hero);unseen.Actors.Single(x=>x.Id==hero).X=0;
                Require(Resolve(unseen,Tear(unseen,hero))=="ExposedSealUnavailable","Unseen physical object leaked or was torn.");
                var blind=Arrange(hero);FerryMechanicalCondition(blind,"Blinded",hero);
                Require(Resolve(blind,Tear(blind,hero))=="ExposedSealUnavailable","Blind actor used remembered physical position as direct perception.");
                var malformed=Arrange(hero);
                Require(Resolve(malformed,new Command("seal.bad-payload",hero,malformed.Revision,CommandKind.TearExposedSeal,
                    FerryWraithProfile.Seal,x:1))=="InvalidSealRequest","Extraneous seal payload accepted.");
                Require(unchanged.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Mechanical seal controls mutated the genuine session.");
                File.WriteAllText(Path.Combine(directory,"seal-mechanical-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="Four labeled detached Action/basis arrangements with before/at/after expiry, closure, no time/RNG and repeat controls; six negative access/payload controls; no manufactured gameplay",rows}));
            });
            cases.Add("tac10_petrified_poison_immunity_retains_event_condition_provenance",()=>{
                // Supplied poison packets, temporary HP and condition events on detached states.
                // No new connected poison/Petrified producer or supported mechanical save is claimed.
                var session=NewFerryExpedition();var initial=ShortRestCapture(session);var codec=new SnapshotCodec();
                var unchanged=codec.Encode(initial);var rows=new List<object>();
                var damage=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules")
                    .GetMethod("Damage",BindingFlags.Static|BindingFlags.NonPublic);
                var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.Static|BindingFlags.NonPublic);
                var wire=typeof(SnapshotCodec).Assembly.GetType("Decennium.Foundation.FerryWraithCodec");
                var write=wire.GetMethod("Write",BindingFlags.Static|BindingFlags.NonPublic);
                var read=wire.GetMethod("Read",BindingFlags.Static|BindingFlags.NonPublic);int wireRoundtrips=0;
                void Roundtrip(Snapshot s) {
                    // Actual selected codec payload on an explicitly mechanical state, not a supported save.
                    using(var bytes=new MemoryStream()) {
                        using(var writer=new BinaryWriter(bytes,System.Text.Encoding.UTF8,true))write.Invoke(null,new object[]{writer,s});
                        bytes.Position=0;var restored=s.Copy();
                        using(var reader=new BinaryReader(bytes,System.Text.Encoding.UTF8,true))read.Invoke(null,new object[]{reader,restored});
                        Require(bytes.Position==bytes.Length,"Selected condition-provenance codec left unread bytes.");
                        Require(System.Text.Json.JsonSerializer.Serialize(s.TypedDamage)==System.Text.Json.JsonSerializer.Serialize(restored.TypedDamage),
                            "Selected codec lost condition policy, origin, prefix, applications or evaluation marker.");
                        SharedTypedDamage.ValidateConditionHistory(restored);wireRoundtrips++;
                    }
                }
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
                                    actor,"poison",raw,raw,false,"",innate?FerryWraithProfile.SourceId:"",false,resolved.ConditionOperationCount,
                                    conditionPolicyId:resolved.ConditionPolicyId,conditionOrigin:resolved.ConditionOrigin,conditionEvaluation:resolved.ConditionEvaluation)};
                                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(forged));
                            } else {
                                var forged=s.Copy();forged.TypedDamage=new[]{new TypedDamageRecord(resolved.EventId,resolved.Revision,resolved.At,
                                    actor,"poison",raw,raw,false,"",TypedDamageRecord.PetrifiedPoisonSource,true,resolved.ConditionOperationCount,
                                    new[]{"ferry.mechanical.Petrified"},resolved.ConditionPolicyId,resolved.ConditionOrigin,resolved.ConditionEvaluation)};
                                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(forged));
                            }
                            Roundtrip(s);
                            rows.Add(new{actor,mode,rolledPacket,raw,sourceWords,before,afterRoll,resolved,after,settled.WordsConsumed});
                        }
                var phased=initial.Copy();const string phaseActor=FerryWraithProfile.Hero;
                Operation(phased,phaseActor,j=>ConditionOperation.Advance("probe.phase",new ConditionStamp(phased.RuleClock,3)));
                FerryMechanicalCondition(phased,"Petrified",phaseActor);
                var protectedAtPhase=SharedTypedDamage.Resolve(phased,"probe.phase.protected",phaseActor,"poison",4);
                Operation(phased,phaseActor,j=>ConditionOperation.End("probe.phase.end",j.Now,"ferry.mechanical.Petrified","supplied-end"));
                var unprotectedAtPhase=SharedTypedDamage.Resolve(phased,"probe.phase.unprotected",phaseActor,"poison",4);
                Require(protectedAtPhase.At==unprotectedAtPhase.At&&protectedAtPhase.ConditionEvaluation.Equals(unprotectedAtPhase.ConditionEvaluation)
                    &&protectedAtPhase.ConditionEvaluation.Phase==3&&protectedAtPhase.ConditionOperationCount+1==unprotectedAtPhase.ConditionOperationCount
                    &&protectedAtPhase.Effective==0&&unprotectedAtPhase.Effective==4,
                    "Same-time same-phase ordered prefixes did not distinguish operative and ended protection.");
                SharedTypedDamage.ValidateConditionHistory(phased);Roundtrip(phased);
                var badMarker=phased.Copy();badMarker.TypedDamage=new[]{new TypedDamageRecord(protectedAtPhase.EventId,protectedAtPhase.Revision,
                    protectedAtPhase.At,phaseActor,"poison",4,4,false,"",TypedDamageRecord.PetrifiedPoisonSource,true,
                    protectedAtPhase.ConditionOperationCount,protectedAtPhase.PetrifiedApplicationIds,protectedAtPhase.ConditionPolicyId,
                    protectedAtPhase.ConditionOrigin,new ConditionStamp(protectedAtPhase.At,2))};
                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(badMarker));
                var badPolicy=phased.Copy();badPolicy.TypedDamage=new[]{new TypedDamageRecord(protectedAtPhase.EventId,protectedAtPhase.Revision,
                    protectedAtPhase.At,phaseActor,"poison",4,4,false,"",TypedDamageRecord.PetrifiedPoisonSource,true,
                    protectedAtPhase.ConditionOperationCount,protectedAtPhase.PetrifiedApplicationIds,"TEST_ONLY.wrong-policy",
                    protectedAtPhase.ConditionOrigin,protectedAtPhase.ConditionEvaluation)};
                Throws<ArgumentException>(()=>SharedTypedDamage.ValidateConditionHistory(badPolicy));
                var legacy=ShortRestCapture(NewDeclaredGeometryExpedition());FerryMechanicalCondition(legacy,"Petrified",FerryWraithProfile.Hero);
                var oldResult=SharedTypedDamage.Resolve(legacy,"probe.legacy",FerryWraithProfile.Hero,"poison",4);
                Require(oldResult.Effective==2&&legacy.TypedDamage.Length==0,"Supported predecessor behavior was changed by the selected correction.");
                Require(unchanged.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Detached condition controls changed the genuine session.");
                File.WriteAllText(Path.Combine(directory,"petrified-poison-controls.json"),System.Text.Json.JsonSerializer.Serialize(new{
                    scope="24 labeled shared-pipeline controls; actual condition ledger, event-prefix validation, life/tempHP and RNG; no new connected producer",rows,
                    legacyEffective=oldResult.Effective,wireRoundtrips,protectedAtPhase,unprotectedAtPhase}));
            });
            cases.Add("tac10_ferry_paid_current_epoch_admission_from_fresh_campaign",()=>{
                var session=RunFerryAdmission(directory);var admitted=ShortRestCapture(session);
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
