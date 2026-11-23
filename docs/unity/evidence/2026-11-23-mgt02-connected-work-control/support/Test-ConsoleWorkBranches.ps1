param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Artifacts,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop';$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path;$Artifacts=(Resolve-Path $Artifacts).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path $Run){throw 'Use a fresh result folder.'};$null=New-Item -ItemType Directory -Path $Run
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
. (Join-Path $PSScriptRoot 'TypedCommand.ps1');. (Join-Path $PSScriptRoot 'TraceCommand.ps1')
$launcher=(Resolve-Path (Join-Path $PSScriptRoot '../../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
foreach($file in 'Test-ConsoleWorkBranches.ps1','TypedCommand.ps1','TraceCommand.ps1'){Copy-Item -LiteralPath (Join-Path $PSScriptRoot $file) -Destination $Run}
function Require([bool]$ok,[string]$why){if(!$ok){throw $why}}
function Json($v){ConvertTo-Json -InputObject $v -Depth 12 -Compress -EnumsAsStrings}
function Digest($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function New-Session {[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())}
$store=[Decennium.Foundation.FileSaveStore]::new();$workKinds=@('StartWaterFill','PauseWaterFill','ResumeWaterFill','CancelWaterFill','StartMining','PauseMining','ResumeMining','StartFormulaResearch','PauseFormulaWork','ResumeFormulaWork','CancelFormulaWork','StartManufacturing','PauseManufacturing','ResumeManufacturing','CancelManufacturing','ResolveManufacturingQuality')
$report=[ordered]@{status='RUNNING';sourceRun=$AssemblyRoot;consoleSha256=Digest $launcher;branches=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try{
 $inputs=@(Get-ChildItem -LiteralPath (Join-Path $Artifacts 'branches-01') -Directory|ForEach-Object{
  $r=Get-Content -LiteralPath (Join-Path $_.FullName 'results.json') -Raw|ConvertFrom-Json
  Require ($r.status-eq'PASS') 'Unqualified typed branch parent.'
  @{name=$_.Name;parent=$r.parentSave;final=(Join-Path $_.FullName 'final.ddsave')}
 })
 # Genuine two-command public-host zero-labor filling cancellation, then identical console replay.
 $session=New-Session;$parent=Join-Path $Run 'fill-cancel-parent.ddsave';$session.Save($parent)
 $actor=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
 $start=[Decennium.Foundation.Command]::new('console.cancel-fill.start',$actor,0,'StartWaterFill',[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::SupplyId,0,0,[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1,2),[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::CompanionSkinId))
 Require ($session.QueryCommand('Player',$start).Admissible-and$session.Submit('Player',$start).Response.ToString()-eq'Committed') 'Typed fill start failed.'
 $active=Join-Path $Run 'fill-cancel-active.ddsave';$session.Save($active);$job=$store.Load($active).WaterFills[0]
 $cancel=[Decennium.Foundation.Command]::new('console.cancel-fill.cancel',$actor,1,'CancelWaterFill',$job.Id)
 Require ($session.QueryCommand('Player',$cancel).Admissible-and$session.Submit('Player',$cancel).Response.ToString()-eq'Committed') 'Typed fill cancel failed.'
 $final=Join-Path $Run 'fill-cancel-final.ddsave';$session.Save($final);$cancelled=$store.Load($final);$genesis=$store.Load($parent)
 Require ($cancelled.WaterFills[0].Status.ToString()-eq'Cancelled'-and$cancelled.RandomState-eq$genesis.RandomState-and$cancelled.Work.Lots.Count-eq$genesis.Work.Lots.Count) 'Fill cancellation created output or drew RNG.'
 $inputs+=@{name='FillingCancel';parent=$parent;final=$final}
 foreach($spec in $inputs){
  $folder=Join-Path $Run $spec.name;$null=New-Item -ItemType Directory -Path $folder
  $before=$store.Load($spec.parent);$after=$store.Load($spec.final);$trace=[Collections.Generic.List[object]]::new();$trace.Add(@{op='load';path=$spec.parent})
  $commands=@($after.Receipts|Where-Object Revision -gt $before.Revision);$controls=@();$pairs=@()
  foreach($receipt in $commands){
   $request=ConvertTo-ConsecrationRequest $receipt
   if($request.kind-in$workKinds){
    $prefix=Join-Path $folder ('before-'+$receipt.Revision);$trace.Add(@{op='save';path=($prefix+'.ddsave')})
    $query=$request.Clone();$query.op='query';$trace.Add($query)
    $trace.Add(@{op='discover';seat='Player';actor=$request.actor;expectedKind=$request.kind;expectedTarget=$request.target})
    $trace.Add(@{op='work';seat='Player';actor=$request.actor})
    $trace.Add(@{op='save';path=($prefix+'.after-read.ddsave')});$pairs+=$prefix;$controls+=$request.kind
   }
   $trace.Add($request)
  }
  $save=Join-Path $folder 'final.ddsave';$trace.Add(@{op='save';path=$save});$trace.Add(@{op='load';path=$save});$trace.Add(@{op='work';seat='Player';actor=$actor});$trace.Add(@{op='save';path=($save+'.restored')})
  $inputFile=Join-Path $folder 'inputs.jsonl';$trace|ForEach-Object{Json $_}|Set-Content -LiteralPath $inputFile
  & $launcher -ConnectedWorkControl -AssemblyRoot $AssemblyRoot -InputPath $inputFile|Set-Content -LiteralPath (Join-Path $folder 'responses.jsonl')
  $answers=@(Get-Content -LiteralPath (Join-Path $folder 'responses.jsonl'));Require ($answers.Count-eq$trace.Count) 'Console branch response count differs.'
  $committed=0
  for($i=0;$i-lt$trace.Count;$i++){
   $request=$trace[$i];$answer=ConvertFrom-Json $answers[$i] -NoEnumerate
   switch($request.op){
    'query'{Require ($answer.Supported-and$answer.Admissible) "Console native query denied $($request.kind)."}
    'discover'{Require (@($answer|Where-Object{$_.Command.Kind-eq$request.expectedKind-and$_.Command.Target-eq$request.expectedTarget-and$_.Query.Admissible}).Count-gt0) "Console discovery omitted $($request.expectedKind)."}
    'work'{Require ($answer.Enabled) 'Console work observation disabled for controlled worker.'}
    'save'{Require ($answer.Response-eq'Saved') 'Console save failed.'}
    'load'{Require ($answer.Response-eq'Restored') 'Console strict restore failed.'}
    default{$committed++;Require ($answer.Response-eq'Committed'-and$answer.Revision-eq$before.Revision+$committed) 'Console branch command diverged.'}
   }
  }
  Require ((Digest $spec.final)-eq(Digest $save)-and(Digest $save)-eq(Digest ($save+'.restored'))) 'Console/typed branch final canonical state or restore differs.'
  foreach($pair in $pairs){Require ((Digest ($pair+'.ddsave'))-eq(Digest ($pair+'.after-read.ddsave'))) 'Console branch reads mutated state.'}
  $report.branches+=@{name=$spec.name;parent=$spec.parent;parentSha256=Digest $spec.parent;typedFinal=$spec.final;finalSha256=Digest $save;commands=$committed;positiveWorkKinds=$controls;pureReadPairs=$pairs.Count;typedConsoleCanonicalEqual=$true;strictRestoreEqual=$true}
  $report|ConvertTo-Json -Depth 14|Set-Content -LiteralPath (Join-Path $Run 'progress.json');Write-Output ('PASS console branch '+$spec.name)
 }
 $report.status='PASS'
}catch{$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 14|Set-Content -LiteralPath (Join-Path $Run 'result.json');Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS'){throw $report.error}
