param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Artifacts,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop';$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path;$Artifacts=(Resolve-Path $Artifacts).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path $Run){throw 'Use a fresh output folder.'};$null=New-Item -ItemType Directory -Path $Run
Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$report=[ordered]@{status='RUNNING';checks=@();startedUtc=[DateTime]::UtcNow.ToString('o');sourceRun=$AssemblyRoot}
function Require([bool]$ok,[string]$why){if(!$ok){throw $why}}
function Digest($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function Json($v){ConvertTo-Json -InputObject $v -Depth 16 -Compress -EnumsAsStrings}
try {
 foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
 function New-Session {[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())}
 $store=[Decennium.Foundation.FileSaveStore]::new();$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero;$companion=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
 function State {$session.Save((Join-Path $Run 'live.ddsave'));$store.Load((Join-Path $Run 'live.ddsave'))}
 function Deny([string]$name,$command) {
  $null=State;$before=Digest (Join-Path $Run 'live.ddsave');$q=$session.QueryCommand('Player',$command);$r=$session.Submit('Player',$command);$null=State
  Require (!$q.Admissible-and$r.Response.ToString()-notin@('Committed','Duplicate')-and$before-eq(Digest (Join-Path $Run 'live.ddsave'))) "Negative changed state or was accepted: $name / $($q.Code) / $($r.Response)"
  $report.checks+=@{name=$name;query=$q;result=$r;unchanged=$true}
 }
 $parents=@(
  @{file='principal-prefix-01/r016.ddsave';kind='PauseMining';family='mining'},
  @{file='principal-prefix-02/r094.ddsave';kind='PauseFormulaWork';family='research'},
  @{file='principal-prefix-02/r106.ddsave';kind='PauseManufacturing';family='manufacturing'},
  @{file='principal-work-01/paused-fill.ddsave';kind='ResumeWaterFill';family='filling'})
 foreach($parent in $parents){
  $session=New-Session;$path=Join-Path $Artifacts $parent.file;$session.Restore($path);$s=State
  $job=switch($parent.family){mining{$s.MiningAttempts[0]}research{$s.FormulaWork[0]}manufacturing{$s.ManufacturingOrders[0]}filling{$s.WaterFills[-1]}}
  $actor=$job.WorkerId
  Deny ($parent.family+'-wrong-worker') ([Decennium.Foundation.Command]::new('negative.wrong-worker',$hero,$s.Revision,$parent.kind,$job.Id))
  Deny ($parent.family+'-unknown-job') ([Decennium.Foundation.Command]::new('negative.unknown-job',$actor,$s.Revision,$parent.kind,'TEST_ONLY.unknown-work'))
  Deny ($parent.family+'-stale') ([Decennium.Foundation.Command]::new('negative.stale',$actor,$s.Revision-1,$parent.kind,$job.Id))
  if($parent.family-eq'manufacturing'){
   Require ($job.Status.ToString()-eq'AwaitingChoice') 'Manufacturing negative parent is not actual AwaitingChoice.'
   foreach($kind in 'PauseManufacturing','ResumeManufacturing','CancelManufacturing'){Deny ('pending-choice-'+$kind) ([Decennium.Foundation.Command]::new(('negative.'+$kind),$actor,$s.Revision,$kind,$job.Id))}
  }
 }
 $session=New-Session;$session.Restore((Join-Path $Artifacts 'principal-work-01/final.ddsave'));$s=State
 $soldMining=@($s.Receipts|Where-Object{[Decennium.Foundation.CommandHistory]::Read($_).Kind.ToString()-eq'StartMining'})[0]
 Deny 'mining-retry-after-actual-sale-lost-inventory-authority' ([Decennium.Foundation.CommandHistory]::Read($soldMining))
 Require ($report.checks[-1].query.Code-eq'InventoryNotAuthorized') 'Sold mining retry bypassed current inventory ownership.'
 foreach($kind in 'StartMining','StartFormulaResearch','StartManufacturing'){
  $session=New-Session;$retryParent=if($kind-eq'StartMining'){'branches-01/MiningBoundary/final.ddsave'}else{'principal-work-01/final.ddsave'}
  $session.Restore((Join-Path $Artifacts $retryParent));$s=State
  $receipt=@($s.Receipts|Where-Object{[Decennium.Foundation.CommandHistory]::Read($_).Kind.ToString()-eq$kind})[0]
  $command=[Decennium.Foundation.CommandHistory]::Read($receipt);$null=State;$before=Digest (Join-Path $Run 'live.ddsave')
  $q=$session.QueryCommand('Player',$command);$r=$session.Submit('Player',$command);$null=State
  $report.checks+=@{name=$kind+'-retry-diagnostic';receiptPrincipal=$receipt.Principal;command=$command;query=$q;result=$r;before=$before;after=Digest (Join-Path $Run 'live.ddsave')}
  Require ($q.Code-eq'AlreadyCommitted'-and$r.Response.ToString()-eq'Duplicate'-and$before-eq(Digest (Join-Path $Run 'live.ddsave'))) "Persisted exact $kind retry failed: $($q.Code) / $($r.Response) / $($receipt.Principal)"
  $report.checks+=@{name=$kind+'-persisted-exact-retry';query=$q;result=$r;unchanged=$true}
  Deny ($kind+'-conflicting-id') ([Decennium.Foundation.Command]::new($command.Id,$command.Actor,$command.ExpectedRevision,'PauseMining','TEST_ONLY.conflicting-work'))
  $session.SetSeatEnabled('Player',$false);Deny ($kind+'-revoked-retry') $command
  Require (!$session.ObserveWork('Player',$companion).Enabled-and@($session.DiscoverCommands('Player',$companion)).Count-eq0) 'Revoked seat retained work observation/discovery.'
  $session.SetSeatEnabled('Player',$true)
 }
 # Actual displaced-primary preservation and normal receipt continuation after backup recovery.
 $session=New-Session;$parent=Join-Path $Artifacts 'principal-work-01/paused-fill.ddsave';$session.Restore($parent);$beforeState=State
 $primary=Join-Path $Run 'primary.ddsave';$session.Save($primary);$backupBytes=[IO.File]::ReadAllBytes($primary)
 $session.Restore((Join-Path $Artifacts 'principal-work-01/final.ddsave'));$finalState=State;$session.Save($primary)
 $corrupt=[IO.File]::ReadAllBytes($primary);$corrupt[$corrupt.Length-1]=$corrupt[$corrupt.Length-1]-bxor1;[IO.File]::WriteAllBytes($primary,$corrupt)
 $before=Digest (Join-Path $Run 'live.ddsave');$rejected=$false;try{$session.Restore($primary)}catch{$rejected=$true};$null=State
 Require ($rejected-and$before-eq(Digest (Join-Path $Run 'live.ddsave'))) 'Corrupt primary restore changed live state.'
 $displaced=$session.RecoverBackup($primary);$session.Save((Join-Path $Run 'recovered.ddsave'))
 Require ((Digest $parent)-eq(Digest (Join-Path $Run 'recovered.ddsave'))-and[Convert]::ToBase64String($corrupt)-eq[Convert]::ToBase64String([IO.File]::ReadAllBytes($displaced))) 'Backup recovery lost backup or displaced bytes.'
 foreach($receipt in @($finalState.Receipts|Where-Object Revision -gt $beforeState.Revision)){
  $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
  $r=if($receipt.Principal-eq'TEST_ONLY.session-operator'){$session.SubmitSessionCommand($command)}else{$session.Submit('Player',$command)}
  Require ($r.Response.ToString()-eq'Committed') 'Recovered actual continuation was rejected.'
 }
 $session.Save((Join-Path $Run 'continued.ddsave'));Require ((Digest (Join-Path $Artifacts 'principal-work-01/final.ddsave'))-eq(Digest (Join-Path $Run 'continued.ddsave'))) 'Recovered final canonical state differs.'
 $report.backup=@{from=$beforeState.Revision;to=$finalState.Revision;recoveredExact=$true;displacedPreserved=$true;continuedExact=$true};$report.status='PASS'
}catch{$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 18|Set-Content -LiteralPath (Join-Path $Run 'result.json');Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS'){throw $report.error}
