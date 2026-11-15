using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class CastingAdditionalNegatives {
    static void Need(bool ok,string message){if(!ok)throw new Exception(message);}
    static ConnectedExpeditionSession Session(string path){
        var s=ConnectedExpeditionSession.StartWithClericCasting(ClericInitialSelection.AuthoredExample(),
            ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());s.Restore(path);return s;
    }
    static Simulation Simulation(ConnectedExpeditionSession s)=>(Simulation)typeof(ConnectedExpeditionSession)
        .GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(s);
    static SpellCastRecord Alter(SpellCastRecord c,SpellTurnIdentity turn,long origin,int level)=>new SpellCastRecord(
        c.CommandId,c.Revision,c.ActorId,c.TargetId,c.SpellId,origin,level,c.Rank,c.Proficiency,c.CastingModifier,c.SpellDc,
        c.StanceRevision,c.FocusedDcElected,c.FocusItemId,c.FocusHeld,c.AvailableHands,c.WillingTarget,turn,c.At,
        c.RpBefore,c.BaseRp,c.Surcharge,c.RpAfter,c.DissonanceBefore,c.DissonanceAfter,c.AppliedRefrain,c.EffectId,
        c.StableRecoveryD4,c.RandomBefore,c.RandomAfter,c.WordsConsumed);
    public static string Run(string caseRoot,string output){
        const string actor=ClericRpProfile.Actor;var codec=new SnapshotCodec();var rows=new List<object>();
        var authority=new Authority("TEST_ONLY.supplement",new[]{ConnectedExpeditionSession.Hero,actor},
            inventoryOwners:new[]{ConnectedExpeditionSession.Hero,actor});
        string beforePath=Path.Combine(caseRoot,"tac08-before-first-cast.ddsave");
        void Deny(string name,string path,Func<Snapshot,Command> request,string code){
            var session=Session(path);var simulation=Simulation(session);var before=simulation.Capture();
            var bytes=codec.Encode(before);var command=request(before);var query=simulation.QueryCommand(authority,command);
            Need(bytes.SequenceEqual(codec.Encode(simulation.Capture())),"Query mutated "+name);
            var result=simulation.Execute(authority,command);
            Need(!query.Admissible&&query.Code==code&&result.Outcome==Outcome.Rejected&&result.Code==code,
                "Wrong denial for "+name+": query="+query.Code+", execute="+result.Code);
            var after=codec.Encode(simulation.Capture());Need(bytes.SequenceEqual(after),"Denial mutated "+name);
            File.WriteAllBytes(Path.Combine(output,name+"-before.ddsave"),bytes);File.WriteAllBytes(Path.Combine(output,name+"-after.ddsave"),after);
            rows.Add(new{name,code,queryPure=true,executionUnchanged=true});
        }
        Deny("stale-revision",beforePath,s=>new Command("supp.stale",actor,s.Revision-1,CommandKind.CastKnownSpell,actor,
            spellCast:new SpellCastRequest("guidance",willingTarget:true)),"StaleRevision");
        Deny("wrong-owned-slot",Path.Combine(caseRoot,"tac08-after-caster-end.ddsave"),s=>new Command("supp.slot",actor,s.Revision,
            CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("guidance",willingTarget:true)),"WrongRegularTurn");
        Deny("unsupported-guidance-attack",beforePath,s=>new Command("supp.guidance-attack",actor,s.Revision,CommandKind.AttackClub,
            ConnectedExpeditionSession.Hero,combat:new CombatRequest(s.Encounter.CurrentTurnId,TestOnlyClubAttackPolicy.CompanionClub),
            guidance:new GuidanceChoice("supp.unbound-benefit")),"UnexpectedSpellPayload");
        Deny("unsupported-readied-spell",beforePath,s=>new Command("supp.ready",actor,s.Revision,CommandKind.Ready,
            actor,combat:new CombatRequest(s.Encounter.CurrentTurnId),spellCast:new SpellCastRequest("guidance",willingTarget:true)),"UnexpectedSpellPayload");
        Deny("unowned-counterspell",beforePath,s=>new Command("supp.counterspell",actor,s.Revision,CommandKind.CastKnownSpell,actor,
            spellCast:new SpellCastRequest("counterspell")),"SpellNotKnown");
        var original=new FileSaveStore().Load(Path.Combine(caseRoot,"tac08-after-first-cast.ddsave"));var cast=original.SpellCasts.Single();
        foreach(string mode in new[]{"stale-epoch","forged-known-origin","forged-class-level"}){
            var altered=original.Copy();var turn=mode=="stale-epoch"
                ?new SpellTurnIdentity(actor,"TEST_ONLY.stale-casting-epoch",cast.Turn.LocalStart,cast.Turn.GlobalStart):cast.Turn;
            altered.SpellCasts=new[]{Alter(cast,turn,mode=="forged-known-origin"?1:cast.KnownAcquiredRevision,
                mode=="forged-class-level"?2:cast.ClassLevel)};
            string error=null;try{codec.Encode(altered);}catch(ArgumentException ex){error=ex.Message;}
            Need(error!=null,"Retained history accepted "+mode);
            rows.Add(new{name=mode,code=error,scope="Detached structural counterexample to an actual cast record; no invalid save admitted"});
        }
        return System.Text.Json.JsonSerializer.Serialize(rows);
    }
}