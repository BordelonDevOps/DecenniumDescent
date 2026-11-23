using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Reflection;
using System.Text.Json;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
using Decennium.Foundation.Tests;

// OMA-CARRY-ALLOCATION-01: hypothetical closure only. Never adopt this copy as a campaign.
public static class CarriedOutsideProbe
{
    const string A = ClericRpProfile.Actor, H = ConnectedExpeditionSession.Hero;
    static readonly SnapshotCodec Codec = new SnapshotCodec();
    static readonly JsonSerializerOptions J = Options();
    static JsonSerializerOptions Options() {
        var resolver = new System.Text.Json.Serialization.Metadata.DefaultJsonTypeInfoResolver();
        resolver.Modifiers.Add(info => { if (info.Type == typeof(ResourceLot) || info.Type == typeof(ResourceReservation)) {
            var legacy = info.Properties.SingleOrDefault(x => x.Name == "Quantity"); if (legacy != null) info.Properties.Remove(legacy);
        }});
        return new JsonSerializerOptions { IncludeFields = true, WriteIndented = true, TypeInfoResolver = resolver };
    }
    static string Json(object value) => JsonSerializer.Serialize(value,J);
    static void Check(bool value,string why) { if (!value) throw new Exception(why); }
    static Snapshot S(ConnectedExpeditionSession s) => (Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});
    static ConnectedExpeditionSession New() => ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
    static object Call(object policy,string method,params object[] args) {
        var m = typeof(TestOnlySharedWorldPolicy).GetMethod(method,BindingFlags.NonPublic|BindingFlags.Static|BindingFlags.Instance);
        Check(m != null,"Missing actual method " + method); return m.Invoke(m.IsStatic ? null : policy,args);
    }
    static void Paid(ConnectedExpeditionSession s,Command c) {
        var r = c.Kind == CommandKind.AdvanceClock ? s.SubmitSessionCommand(c) : s.Submit(ExpeditionSeat.Player,c);
        Check(r.Response == ExpeditionResponse.Committed,c.Id + ": " + r.Response);
    }
    static void Advance(ConnectedExpeditionSession s,RuleTime at,string id) {
        var before = S(s); var delta = new RuleTime(checked(at.Numerator*before.RuleClock.Denominator-before.RuleClock.Numerator*at.Denominator),checked(at.Denominator*before.RuleClock.Denominator));
        Paid(s,new Command(id,H,before.Revision,CommandKind.AdvanceClock,x:checked((int)delta.Numerator),y:checked((int)delta.Denominator)));
    }
    static void Late(ConnectedExpeditionSession s,string id) {
        var state=S(s);var e=WorldTiming.ForActor(state,A);
        Advance(s,e.Start(e.LatestStart(A,e.ProcessedSlot)+e.Order.Count).AddSeconds(3),id);
    }
    static string NormalRejection(Snapshot s) {
        try { Codec.Encode(s); } catch (Exception e) when (e is ArgumentException || e is InvalidDataException || e is InvalidOperationException) { return e.GetType().Name + ": " + e.Message; }
        throw new Exception("Hypothetical state passed normal validation");
    }
    static string[] ChangedTop(string before,string after) {
        using var a=JsonDocument.Parse(before);using var b=JsonDocument.Parse(after);
        return a.RootElement.EnumerateObject().Where(x=>x.Value.GetRawText()!=b.RootElement.GetProperty(x.Name).GetRawText()).Select(x=>x.Name).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
    }
    public static void Run(string dir,string[] args) {
        var session=New();session.Restore(args[0]);
        Late(session,"oma.carry2.guidance-time");
        Paid(session,new Command("oma.carry2.guidance",A,S(session).Revision,CommandKind.CastKnownSpell,H,spellCast:new SpellCastRequest("guidance",willingTarget:true)));
        Late(session,"oma.carry2.detect-time");
        Paid(session,new Command("oma.carry2.detect",A,S(session).Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("detect-magic",SpellCastingProfile.FocusId)));
        var before=S(session);var epoch=WorldTiming.ForActor(before,A);int speed=(int)TestOnlyClubAttackPolicy.WalkingSpeed(before,H);long slot=epoch.SlotAt(before.RuleClock);
        RuleTime Departure(long k) { var at=epoch.Start(k);return new RuleTime(checked(at.Numerator*speed-30L*at.Denominator),checked(at.Denominator*speed)); }
        while(epoch.Order[(int)(slot%epoch.Order.Count)]!=PostRecoveryEncounterDefinition.Actor || Departure(slot)<=before.RuleClock)slot++;
        Advance(session,Departure(slot),"oma.carry2.depart-time");
        Paid(session,new Command("oma.carry2.contact",H,S(session).Revision,CommandKind.BeginWorldStep,"walk",0,1));
        Advance(session,epoch.Start(slot),"oma.carry2.arrival");
        var parent=S(session);session.Save(Path.Combine(dir,"genuine-parent.ddsave"));session.Restore(Path.Combine(dir,"genuine-parent.ddsave"));
        Check(Codec.Encode(parent).SequenceEqual(Codec.Encode(S(session))),"Genuine strict restore changed bytes");
        File.WriteAllText(Path.Combine(dir,"genuine-parent.json"),Json(parent));
        Check(parent.InventoryCombat && parent.Encounter.Id==FerryWraithProfile.Encounter && parent.FerryWraith.Admission.Epoch.LatestStart(A,parent.FerryWraith.Admission.Epoch.ProcessedSlot)<0,"Parent already has first new Cleric Start");
        Check(!parent.WorldIntervals.Single(x=>x.ActorId==A).ActionSpent && !parent.OrdinaryMagic.Current.Consumed && parent.OrdinaryMagic.Current.Origin.EpochId!=WorldTiming.ForActor(parent,A).Id,"Parent lacks genuine open carried allowance");
        var policy=typeof(ConnectedExpeditionSession).GetField("policy",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
        var views=session.View(ExpeditionSeat.Player);var hero=views.Actors.Single(x=>x.Position.Id==H).Position;
        string aura=views.Actors.Single(x=>x.Position.Id==A).Casting.Auras.Single(x=>x.X==hero.X&&x.Y==hero.Y).ObservationId;
        var body=parent.Actors.Single(x=>x.Id==A);
        var commands=new[]{
            new Command("oma.detached.consecrate",A,parent.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(body.X,body.Y)),
            new Command("oma.detached.rite",A,parent.Revision,CommandKind.UseHealingRite,H,healingRite:new HealingRiteRequest(RadianceCurePreference.Frightened)),
            new Command("oma.detached.invocation",A,parent.Revision,CommandKind.UseDivineInvocation,divineInvocation:new DivineInvocationRequest(new[]{H,A},H,RadianceCurePreference.Frightened)),
            new Command("oma.detached.guidance",A,parent.Revision,CommandKind.CastKnownSpell,H,spellCast:new SpellCastRequest("guidance",willingTarget:true)),
            new Command("oma.detached.focus",A,parent.Revision,CommandKind.FocusDetectedAura,aura),
            new Command("oma.detached.ground",A,parent.Revision,CommandKind.GroundCastingStrain)
        };
        var methods=new[]{"ResolveConsecrate","ResolveHealingRite","ResolveDivineInvocation","ResolveSpellCast","ResolveCastingUtility","ResolveCastingUtility"};
        var rows=new List<object>();
        for(int i=0;i<commands.Length;i++) {
            var c=commands[i];var genuine=Codec.Decode(Codec.Encode(parent));string original=Json(genuine);
            object[] ProducerArgs(Snapshot s) => i>=4 ? new object[]{s,c,false} : new object[]{s,c};
            string originalFailure=(string)Call(policy,methods[i],ProducerArgs(genuine));
            Check(originalFailure=="WrongRegularTurn" && original==Json(genuine),"Original tactical parent must reject unchanged: "+c.Kind+" "+originalFailure);
            var s=Codec.Decode(Codec.Encode(parent));
            // These five top-level fields are the complete fixture assumptions, not an occurred closure.
            var assumedCause=new Command("oma.assumed.close",H,s.Revision,CommandKind.EndFixedEncounter,s.Encounter.CurrentTurnId);
            s.ClosedEncounters=s.ClosedEncounters.Append(new ClosedEncounterRecord(s.Encounter,s.Revision+1,s.RuleClock,"TEST_ONLY.assumed-closure")).ToArray();
            s.Encounter=null;s.InventoryCombat=false;s.InventoryTurnActor="";
            Call(policy,"ChangeMagicalContext",s,WorldTiming.ForActor(s,A),false,assumedCause);
            string assumed=Json(s);string[] changed=ChangedTop(original,assumed);
            Check(changed.SequenceEqual(new[]{"ClosedEncounters","Encounter","InventoryCombat","InventoryTurnActor","OrdinaryMagic"}),"Unexpected assumed field set: "+string.Join(",",changed));
            Check(s.OrdinaryMagic.Current.Origin.SameAs(parent.OrdinaryMagic.Current.Origin)&&s.OrdinaryMagic.Current.Deadline==parent.OrdinaryMagic.Current.Deadline&&s.OrdinaryMagic.Current.Consumed==parent.OrdinaryMagic.Current.Consumed,"Context change refreshed origin/accounting");
            string invalidBefore=NormalRejection(s);
            File.WriteAllText(Path.Combine(dir,c.Kind+"-hypothetical-before.json"),assumed);
            string failure=(string)Call(policy,methods[i],ProducerArgs(s));Check(failure==null,"Actual producer blocked "+c.Kind+": "+failure);
            Check(s.RuleClock==parent.RuleClock&&s.Revision==parent.Revision&&Json(s.Receipts)==Json(parent.Receipts),"Detached producer invented clock/revision/receipt");
            Check(s.WorldIntervals.Single(x=>x.ActorId==A).ActionSpent,"Real producer did not pay carried Action");
            var activity=s.OrdinaryMagic.Activities.Single(x=>x.CommandId==c.Id);
            Check(activity.Origin.SameAs(parent.OrdinaryMagic.Current.Origin)&&activity.ContextEpoch==WorldTiming.ForActor(parent,A).Id&&!activity.InInitiative,"Paid activity lost old origin/current context");
            Check(s.OrdinaryMagic.Current.Deadline==parent.OrdinaryMagic.Current.Deadline&&s.OrdinaryMagic.Current.Consumed==parent.OrdinaryMagic.Current.Consumed,"Producer reset accounting deadline/consumption");
            int paidRp=parent.ResonancePools.Single().Current-s.ResonancePools.Single().Current;
            Check(paidRp==(i==0||i==1?2:i==2?3:0),"Wrong actual RP payment");
            if(i==0||i==2) {
                string ability=i==0?ConsecrationProfile.Consecrate:BishopProfile.Invocation;
                var recharge=s.AbilityRecharges.Single(x=>x.AbilityId==ability);
                Check(recharge.EpochId==parent.OrdinaryMagic.Current.Origin.EpochId&&recharge.LastLocalStart==parent.OrdinaryMagic.Current.Origin.LocalStart&&recharge.Remaining==3,"Recharge not bound to old actual origin");
            }
            if(i==0) { var zone=s.Consecration.Zones.Last();Check(zone.EpochId==parent.OrdinaryMagic.Current.Origin.EpochId&&zone.LocalStart==parent.OrdinaryMagic.Current.Origin.LocalStart&&!zone.InInitiative&&zone.ExpiresAt==parent.RuleClock.AddSeconds(18),"Consecrate application identity/deadline changed"); }
            if(i==2)Check(s.ConvictionBalance.Current==parent.ConvictionBalance.Current-2&&s.CastingStrain.Single().Dissonance==Math.Max(0,parent.CastingStrain.Single().Dissonance-1),"Invocation payment/vent changed");
            Check(Json(s.SpellEffects.Where(x=>x.CastId!=c.Id).Select(x=>new{x.Id,x.ExpiresAt}))==Json(parent.SpellEffects.Select(x=>new{x.Id,x.ExpiresAt})),"Existing spell expiry moved");
            string after=Json(s);string repeat=(string)Call(policy,methods[i],ProducerArgs(s));Check(repeat!=null&&after==Json(s),"Direct repeat paid or applied again");
            string invalidAfter=NormalRejection(s);
            File.WriteAllText(Path.Combine(dir,c.Kind+"-hypothetical-after.json"),after);
            rows.Add(new{kind=c.Kind.ToString(),method=methods[i],originalFailure,changedAssumptionFields=changed,paidRp,activity,repeat,invalidBefore,invalidAfter,normalCampaignRejected=true});
            File.WriteAllText(Path.Combine(dir,"progress.json"),Json(rows));
        }
        Check(Codec.Encode(parent).SequenceEqual(Codec.Encode(S(session))),"Detached control mutated genuine campaign");
        File.WriteAllText(Path.Combine(dir,"result.json"),Json(new{status="PASS",allocation="OMA-CARRY-ALLOCATION-01",scope="Genuine unspent admitted parent; only assumed closure/context on detached copies. Six unchanged actual producer paths and direct-repeat denials. Optional cure choices execute, but no claim of ending an absent condition. No hypothetical save, receipt, life, RNG, resource, origin or deadline fabrication; no detached continuation claimed. A fully genuine joint before-first-new-Start outside-use remains UNPROVED_REQUIRED_FOR_BROADER_ENGINE_COMPLETION.",cases=rows}));
    }
}
