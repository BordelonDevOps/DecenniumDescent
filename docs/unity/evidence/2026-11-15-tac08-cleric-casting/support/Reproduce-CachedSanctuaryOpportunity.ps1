param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$SourceSave,[Parameter(Mandatory)][string]$Run,[switch]$ExpectFixed)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$SourceSave=(Resolve-Path -LiteralPath $SourceSave).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$references=@(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll'|ForEach-Object FullName)
$assemblies=@()
foreach($part in 'Core','Persistence','LabModel'){
    $path=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $path;$references+=$path
    $assemblies+=@{name=$part;sha256=(Digest $path)}
}
$source=@'
using System;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class CachedSanctuaryReproduction {
    static void Need(bool value,string message){if(!value)throw new Exception(message);}
    public static string Run(string input,string output,bool fixedExpected){
        var session=ConnectedExpeditionSession.StartWithClericCasting(ClericInitialSelection.AuthoredExample(),
            ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());
        session.Restore(input);
        var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
        var policy=(TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession).GetField("policy",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
        var initial=simulation.Capture();var codec=new SnapshotCodec();
        Need(initial.Revision==128&&initial.Actors.Single(x=>x.Id==ConnectedExpeditionSession.Hero).Y==1,"Unexpected authentic starting point");
        foreach(int y in new[]{2,1}){
            var state=simulation.Capture();
            var result=session.Submit(ExpeditionSeat.Player,new Command("tac08.review.revisit."+y,ConnectedExpeditionSession.Hero,
                state.Revision,CommandKind.TacticalStep,state.Encounter.CurrentTurnId,0,y));
            Need(result.Response==ExpeditionResponse.Committed,"Actual movement failed: "+result.Response);
        }
        var pending=simulation.Capture();
        Need(pending.TacticalMoves.Any(x=>x.Status==TacticalMoveStatus.AwaitingReactions),"Second occurrence did not open");
        session.Save(Path.Combine(output,"second-opportunity-pending.ddsave"));
        var controller=new LaterDefenderController(simulation,policy);var grant=LaterDefenderController.DefenderAuthority();
        var plan=controller.Plan(grant);var admission=simulation.AssessCommandAdmission(grant,plan.Primary);
        var response=session.AdvanceAutomaticDefender();var after=simulation.Capture();
        session.Save(Path.Combine(output,"after-automatic-controller.ddsave"));
        if(fixedExpected){
            Need(plan.Intent.Kind==DefenderIntentKind.DeclineOpportunity&&response.Response==ExpeditionResponse.Committed,
                "Controller failed to decline a known prohibited opportunity");
            Need(!after.TacticalMoves.Any(x=>x.Status==TacticalMoveStatus.AwaitingReactions)
                &&after.Actors.Single(x=>x.Id==ConnectedExpeditionSession.Hero).Y==1,"Parent movement remains pending");
            Need(after.RandomState==pending.RandomState&&after.SpellSaves.Length==pending.SpellSaves.Length
                &&after.TacticalActors.Single(x=>x.ActorId==TestOnlySharedWorldPolicy.LaterDefenderId).ReactionAvailable,
                "Cached prohibition spent RNG, another save, or the unspent Reaction");
        }else{
            Need(plan.Intent.Kind==DefenderIntentKind.AcceptOpportunity&&admission.Code=="SanctuaryTargetProhibitedThisInterval"
                &&response.Response!=ExpeditionResponse.Committed&&codec.Encode(after).SequenceEqual(codec.Encode(pending)),
                "Expected controller stall was not reproduced");
        }
        return System.Text.Json.JsonSerializer.Serialize(new{status=fixedExpected?"PASS":"REPRODUCED_STALL",initialRevision=initial.Revision,
            pendingRevision=pending.Revision,finalRevision=after.Revision,intent=plan.Intent.Kind.ToString(),admission=admission.Code,
            response=response.Response.ToString(),pendingRandom=pending.RandomState,finalRandom=after.RandomState,
            pendingSaves=pending.SpellSaves.Length,finalSaves=after.SpellSaves.Length,
            reactionAvailable=after.TacticalActors.Single(x=>x.ActorId==TestOnlySharedWorldPolicy.LaterDefenderId).ReactionAvailable,
            parentPending=after.TacticalMoves.Any(x=>x.Status==TacticalMoveStatus.AwaitingReactions)});
    }
}
'@
$sourcePath=Join-Path $Run 'CachedSanctuaryReproduction.cs'
[IO.File]::WriteAllText($sourcePath,$source,[Text.UTF8Encoding]::new($false))
Add-Type -Path $sourcePath -ReferencedAssemblies $references -CompilerOptions '/langversion:9.0','/warnaserror'
$result=[CachedSanctuaryReproduction]::Run($SourceSave,$Run,[bool]$ExpectFixed)|ConvertFrom-Json -AsHashtable
$result.assemblies=$assemblies;$result.sourceSave=$SourceSave;$result.sourceSaveSha256=Digest $SourceSave
$result.harnessSourceSha256=Digest $sourcePath
$result|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output ($result|ConvertTo-Json -Depth 4 -Compress)
