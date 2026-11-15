param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$BeforeApproachSave,[Parameter(Mandatory)][string]$ActiveSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
Add-Type -TypeDefinition @'
using System;
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Globalization;
public static class DetachedStoredFields {
  public static object Replace(object source, string property, object replacement) {
    var clone=typeof(object).GetMethod("MemberwiseClone",BindingFlags.Instance|BindingFlags.NonPublic).Invoke(source,null);
    source.GetType().GetField("<"+property+">k__BackingField",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(clone,replacement);
    return clone;
  }
  public static string Hash(object source) {
    using var stream=new MemoryStream(); using var writer=new BinaryWriter(stream);
    Write(writer,source,0); writer.Flush();
    return Convert.ToHexString(SHA256.HashData(stream.ToArray())).ToLowerInvariant();
  }
  private static void Write(BinaryWriter writer, object value, int depth) {
    if(depth>80)throw new InvalidOperationException("Unexpected stored-field cycle");
    writer.Write(value!=null); if(value==null)return;
    var type=value.GetType();writer.Write(type.FullName);
    if(type.IsPrimitive||type.IsEnum||value is string||value is decimal){writer.Write(Convert.ToString(value,CultureInfo.InvariantCulture));return;}
    if(value is IEnumerable sequence){foreach(var item in sequence){writer.Write(true);Write(writer,item,depth+1);}writer.Write(false);return;}
    foreach(var field in type.GetFields(BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic).OrderBy(x=>x.Name,StringComparer.Ordinal)){
      writer.Write(field.Name);Write(writer,field.GetValue(value),depth+1);
    }
  }
}
'@
$type=[Decennium.Foundation.Tests.FoundationCases];$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$Name,[object[]]$Arguments){try{$type.GetMethod($Name,$flags).Invoke($null,$Arguments)}catch{throw $_.Exception.GetBaseException()}}
function Require($value,[string]$message){if(!$value){throw $message}}
$session=Call 'NewFrightenedExpedition' @()
$session.Restore((Resolve-Path -LiteralPath $BeforeApproachSave).Path)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$ally=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
$npc=[Decennium.Foundation.FrightenedProfile]::Actor
$turn=$session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player).TurnId
Call 'ClericCommit' @($session,$hero,[Decennium.Foundation.CommandKind]::TacticalStep,$turn,0,2,$null)
Call 'ClericEnd' @($session,$hero)
$ready=Call 'ShortRestCapture' @($session);$policy=Call 'ClericPolicy' @($session)
$session.Save((Join-Path $Run 'genuine-ready.ddsave'))
function Presence([string]$Id,[long]$Revision,[string[]]$Targets){
    [Decennium.Foundation.Command]::new($Id,$npc,$Revision,[Decennium.Foundation.CommandKind]::UseIntimidatingPresence,'',0,0,$null,$null,$null,$null,[Decennium.Foundation.OverwatchRider]::None,$null,$null,$null,$null,$null,$null,$null,[Decennium.Foundation.IntimidatingPresenceRequest]::new($Targets))
}
$command=Presence 'detached.boundary' $ready.Revision @($hero,$ally)
$rows=[Collections.Generic.List[object]]::new()
function Deny($candidate,[string]$name,[string]$expected){
    $before=[DetachedStoredFields]::Hash($candidate);$rng=$candidate.RandomState
    $actual=$policy.Resolve($candidate,$command)
    Require ($actual-ceq$expected) "$name returned $actual instead of $expected"
    Require ($before-ceq[DetachedStoredFields]::Hash($candidate)) "$name changed stored fields"
    Require ($candidate.RandomState-eq$rng) "$name changed RNG"
    $rows.Add(@{name=$name;scope='DETACHED_PREFLIGHT';diagnostic=$actual;fullStoredFieldsSha256=$before;randomState=$rng;unchanged=$true})
}
$candidate=$ready.Copy();$candidate.InventoryCombat=$false
Deny $candidate 'wrong-context' 'IntimidatingPresenceContextUnsupported'
$candidate=$ready.Copy();$c=@($candidate.Characters|Where-Object ActorId -eq $npc)[0]
$replacement=[Decennium.Foundation.ActorCharacterRecord]::new($c.ActorId,$c.ProfileId,$c.Abilities,[Decennium.Foundation.CharacterLevelFact[]]@($c.Levels[0]))
$candidate.Characters=[Decennium.Foundation.ActorCharacterRecord[]]@($candidate.Characters|ForEach-Object{if($_.ActorId-eq$npc){$replacement}else{$_}})
Deny $candidate 'pre-level-warrior-one' 'IntimidatingPresenceClassUnavailable'
foreach($field in 'FrightenedUses','FrightenedSaves','FrightenedTimings'){
    $candidate=$ready.Copy();$count=switch($field){'FrightenedUses'{128};'FrightenedSaves'{763};'FrightenedTimings'{382}}
    $sample=if($field-eq'FrightenedTimings'){[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path -LiteralPath $ActiveSave).Path).FrightenedTimings[0]}else{$candidate.$field[0]}
    $array=[Array]::CreateInstance($sample.GetType(),$count);for($i=0;$i-lt$count;$i++){$array.SetValue($sample,$i)}
    $candidate.$field=$array
    Deny $candidate ('capacity-'+$field) 'IntimidatingPresenceHistoryFull'
}
$candidate=$ready.Copy();$journal=@($candidate.Conditions|Where-Object Target -eq $ally)[0]
$operations=[Collections.Generic.List[Decennium.Foundation.ConditionOperation]]::new()
$operations.AddRange([Decennium.Foundation.ConditionOperation[]]$journal.Operations)
while($operations.Count-lt[Decennium.Foundation.ConditionJournal]::MaxOperations-5){
    $operations.Add([Decennium.Foundation.ConditionOperation]::Advance(('detached.capacity.'+$operations.Count),[Decennium.Foundation.ConditionStamp]::new($candidate.RuleClock,0)))
}
$replacement=[Decennium.Foundation.ConditionJournal]::new($journal.PolicyId,$journal.Target,$journal.Origin,$operations)
$candidate.Conditions=[Decennium.Foundation.ConditionJournal[]]@($candidate.Conditions|ForEach-Object{if($_.Target-eq$ally){$replacement}else{$_}})
Deny $candidate 'second-target-condition-history-full' 'IntimidatingPresenceConditionHistoryFull'
$grant=[Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority()
$before=[DetachedStoredFields]::Hash((Call 'ShortRestCapture' @($session)))
$stale=$session.SubmitDefenderIntimidatingPresence($grant,(Presence 'fear.boundary.stale' ($ready.Revision-1) @($hero,$ally)))
Require ($stale.Response-eq'StaleRevision') 'Stale source request must reject at shared revision gate'
Require ($before-ceq[DetachedStoredFields]::Hash((Call 'ShortRestCapture' @($session)))) 'Stale request changed live state'
$session.Save((Join-Path $Run 'stale-unchanged.ddsave'))
$rows.Add(@{name='stale-public-source-request';scope='GENUINE_PUBLIC_SESSION';response=$stale.Response.ToString();unchanged=$true;fullStoredFieldsSha256=$before})
$active=[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path -LiteralPath $ActiveSave).Path)
$codec=[Decennium.Foundation.SnapshotCodec]::new()
function StructuralDeny($candidate,[string]$name){
    $before=[DetachedStoredFields]::Hash($candidate);$rejected=$false;$message=''
    try{$null=$codec.Encode($candidate)}catch{if($_.Exception.GetBaseException()-isnot[ArgumentException]){throw};$rejected=$true;$message=$_.Exception.GetBaseException().Message}
    Require $rejected "Structural forgery accepted: $name"
    Require ($before-ceq[DetachedStoredFields]::Hash($candidate)) "Structural rejection changed candidate: $name"
    $rows.Add(@{name=$name;scope='STRUCTURAL_FORGERY';rejected=$true;unchanged=$true;message=$message;fullStoredFieldsSha256=$before})
}
foreach($spec in @(@{field='Dc';value=11},@{field='SourceId';value='TEST_ONLY.other-source'},@{field='SourceRevision';value='TEST_ONLY.other-revision'})){
    $candidate=$active.Copy();$candidate.FrightenedUses[-1]=[DetachedStoredFields]::Replace($candidate.FrightenedUses[-1],$spec.field,$spec.value)
    StructuralDeny $candidate ('forged-use-'+$spec.field)
}
$candidate=$active.Copy();$jIndex=[Array]::FindIndex($candidate.Conditions,[Predicate[Decennium.Foundation.ConditionJournal]]{param($x)$x.Target-eq$hero})
$journal=$candidate.Conditions[$jIndex];$ops=[Decennium.Foundation.ConditionOperation[]]@($journal.Operations)
$opIndex=[Array]::FindIndex($ops,[Predicate[Decennium.Foundation.ConditionOperation]]{param($x)$null-ne$x.Application-and$x.Application.Kind-eq'Frightened'})
$op=$ops[$opIndex];$fear=[DetachedStoredFields]::Replace($op.Application.Fear,'FearedEntityId',$ally)
$app=[DetachedStoredFields]::Replace($op.Application,'Fear',$fear)
$ops[$opIndex]=[Decennium.Foundation.ConditionOperation]::Apply($op.Id,$op.At,$app)
$candidate.Conditions[$jIndex]=[Decennium.Foundation.ConditionJournal]::new($journal.PolicyId,$journal.Target,$journal.Origin,$ops)
StructuralDeny $candidate 'forged-feared-entity'
[ordered]@{status='PASS';assemblyRoot=$AssemblyRoot;sourceCommit='f5800818bfadb7c51865c96a6058f9af2deb75a3';controls=@($rows);scope='Detached capacity/class candidates are not reachable gameplay saves; public stale control uses genuine ready state.'}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count) source boundary and forgery controls."
