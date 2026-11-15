param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ActiveSave,[Parameter(Mandatory)][string]$UnseenSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ActiveSave=(Resolve-Path -LiteralPath $ActiveSave).Path;$UnseenSave=(Resolve-Path -LiteralPath $UnseenSave).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$store=[Decennium.Foundation.FileSaveStore]::new();$active=$store.Load($ActiveSave);$use=$active.FrightenedUses[-1]
$trace=[Collections.Generic.List[object]]::new();$checks=[Collections.Generic.List[object]]::new()
$trace.Add(@{op='load';path=$ActiveSave})
function Add-Denial([string]$name,$request,[string]$scope,[string]$expected='Unavailable'){
    $index=$trace.Count;$trace.Add($request);$trace.Add(@{op='save';path=(Join-Path $Run ($name+'.ddsave'))})
    $checks.Add(@{name=$name;scope=$scope;index=$index;expected=$expected;reference=$ActiveSave})
}
foreach($spec in @(
    @{name='supplied-dc';details=@{targets=@($use.TargetIds);dc=1}},
    @{name='supplied-source';details=@{targets=@($use.TargetIds);source='fake'}},
    @{name='supplied-perception';details=@{targets=@($use.TargetIds);canHear=$true}},
    @{name='supplied-duration';details=@{targets=@($use.TargetIds);rounds=99}},
    @{name='supplied-forced';details=@{targets=@($use.TargetIds);forced=$true}},
    @{name='duplicate-target';details=@{targets=@($use.TargetIds[0],$use.TargetIds[0])}},
    @{name='empty-targets';details=@{targets=@()}},
    @{name='string-targets';details=@{targets=$use.TargetIds[0]}}
)){
    Add-Denial $spec.name @{op='defender-presence';actor=$use.ActorId;id=('fear.parser.'+$spec.name);revision=$active.Revision;intimidatingPresence=$spec.details} 'PARSER_OR_REQUEST_CONSTRUCTOR'
}
Add-Denial 'conflicting-id' @{op='defender-presence';actor=$use.ActorId;id=$use.CommandId;revision=($use.Revision-1);intimidatingPresence=@{targets=@($use.TargetIds[0])}} 'SHARED_IDEMPOTENCY' 'CommandIdConflict'
$trace.Add(@{op='load';path=$UnseenSave})
$s=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
$s.Restore($UnseenSave);$v=$s.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player)
Add-Denial 'client-forced-step' @{op='submit';seat='Player';actor=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero;id='fear.client.forced';revision=$v.Revision;kind='TacticalStep';target=$v.TurnId;x=1;y=1;forced=$true} 'PUBLIC_WILLING_MOVEMENT'
$checks[-1].reference=$UnseenSave
$trace|ForEach-Object{ConvertTo-Json $_ -Depth 6 -Compress}|Set-Content -LiteralPath (Join-Path $Run 'inputs.jsonl') -Encoding utf8
& (Join-Path $PSScriptRoot '../../../tools/Open-ConnectedExpedition.ps1') -Frightened -AssemblyRoot $AssemblyRoot -InputPath (Join-Path $Run 'inputs.jsonl')|Set-Content -LiteralPath (Join-Path $Run 'responses.jsonl') -Encoding utf8
$responses=@(Get-Content -LiteralPath (Join-Path $Run 'responses.jsonl')|ConvertFrom-Json)
if($responses.Count-ne$trace.Count){throw 'Response count mismatch'}
foreach($check in $checks){
    $actual=$responses[$check.index].Response;if($actual-cne$check.expected){throw "$($check.name): expected $($check.expected), got $actual"}
    $before=(Get-FileHash -LiteralPath $check.reference).Hash.ToLowerInvariant()
    $after=(Get-FileHash -LiteralPath (Join-Path $Run ($check.name+'.ddsave'))).Hash.ToLowerInvariant()
    if($before-cne$after){throw "Rejected console input changed state: $($check.name)"}
    $check.response=$actual;$check.sha256=$after;$check.unchanged=$true
}
[ordered]@{status='PASS';assemblyRoot=$AssemblyRoot;checks=@($checks);scope='Parser/constructor controls are distinct from shared-boundary controls. Unknown root forced field cannot grant forced movement.'}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($checks.Count) console parser/idempotency/movement controls."
