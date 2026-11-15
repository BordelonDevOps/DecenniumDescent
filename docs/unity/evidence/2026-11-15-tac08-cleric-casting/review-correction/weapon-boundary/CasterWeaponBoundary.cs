using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Reflection;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class CasterWeaponBoundary {
    public static string Run(string input,string output){
        var rows=new List<object>();var codec=new SnapshotCodec();
        foreach(string probe in new[]{"actual-weapon-attack","initial-grounded-club-pickup","initial-grounded-club-equip"}){
            var session=ConnectedExpeditionSession.StartWithClericCasting(ClericInitialSelection.AuthoredExample(),
                ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());
            if(probe=="actual-weapon-attack")session.Restore(input);
            var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
            var before=simulation.Capture();const string actor=ClericRpProfile.Actor;
            var authority=new Authority("TEST_ONLY.host",new[]{ConnectedExpeditionSession.Hero,actor},
                inventoryOwners:new[]{ConnectedExpeditionSession.Hero,actor},willingRecipients:new[]{ConnectedExpeditionSession.Hero,actor});
            var command=probe=="actual-weapon-attack"
                ?new Command("tac08.weapon-boundary.attack",actor,before.Revision,CommandKind.AttackClub,FrightenedProfile.Actor,
                    combat:new CombatRequest(before.Encounter.CurrentTurnId,TestOnlyClubAttackPolicy.CompanionClub))
                :new Command("tac08.weapon-boundary."+probe,actor,before.Revision,
                    probe.EndsWith("pickup")?CommandKind.HandlePortableEquipment:CommandKind.EquipPortableItem,
                    TestOnlyClubAttackPolicy.CompanionClub,inventory:probe.EndsWith("pickup")?new InventoryRequest(new RuleQuantity(1)):null);
            var bytes=codec.Encode(before);var query=simulation.QueryCommand(authority,command);
            var result=simulation.Execute(authority,command);var after=codec.Encode(simulation.Capture());
            if(query.Admissible||result.Outcome!=Outcome.Rejected||!bytes.SequenceEqual(after))throw new Exception("Boundary changed state: "+probe);
            File.WriteAllBytes(Path.Combine(output,probe+"-before.ddsave"),bytes);
            File.WriteAllBytes(Path.Combine(output,probe+"-after.ddsave"),after);
            var club=before.Clubs.Single(x=>x.Id==TestOnlyClubAttackPolicy.CompanionClub);
            var body=before.Actors.Single(x=>x.Id==actor);var life=before.Lives.Single(x=>x.ActorId==actor);
            rows.Add(new{probe,revision=before.Revision,queryCode=query.Code,resultCode=result.Code,
                unchanged=true,actorX=body.X,actorY=body.Y,heldItems=life.HeldItems,club,
                strain=before.CastingStrain.SingleOrDefault(),portableRecordExists=before.PortableEquipment.Any(x=>x.Id==club.Id)});
        }
        return System.Text.Json.JsonSerializer.Serialize(rows);
    }
}