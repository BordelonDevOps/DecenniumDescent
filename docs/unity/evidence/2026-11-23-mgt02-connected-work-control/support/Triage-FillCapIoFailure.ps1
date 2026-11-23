param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Artifacts,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop';$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path;$Artifacts=(Resolve-Path $Artifacts).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path $Run){throw 'Fresh result folder required.'};$null=New-Item -ItemType Directory -Path $Run;Copy-Item -LiteralPath $PSCommandPath -Destination $Run
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Digest($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function Require([bool]$ok,[string]$why){if(!$ok){throw $why}}
$caseRoot=Join-Path $Artifacts 'full-01/worker2/cases/mgt02_work_control_native_fill_record_and_booking_caps'
$failed=Get-Content -LiteralPath (Join-Path $caseRoot 'result.json') -Raw|ConvertFrom-Json
$retry=Get-Content -LiteralPath (Join-Path $Artifacts 'fill-cap-io-recheck-01/results.json') -Raw|ConvertFrom-Json
$rows=@();$report=[ordered]@{status='FAIL';failedCase=$failed;failedCaseSha256=Digest (Join-Path $caseRoot 'result.json');rerunResultSha256=Digest (Join-Path $Artifacts 'fill-cap-io-recheck-01/results.json');sourceRun=$AssemblyRoot}
try{
 Require (!$failed.Passed-and$failed.Error.StartsWith('System.IO.IOException: Unable to remove the file to be replaced.')) 'Unexpected original failure.'
 Require ($retry.status-eq'PASS'-and$retry.assigned-eq1-and$retry.passed-eq1-and$retry.cases[0].Name-eq$failed.Name) 'Exact isolated case did not pass.'
 foreach($binding in $retry.assemblyHashes){Require ($binding.sha256-eq(Digest (Join-Path $AssemblyRoot $binding.name))) 'Rerun changed a frozen DLL.'}
 $store=[Decennium.Foundation.FileSaveStore]::new()
 foreach($name in 'fill-record-cap.ddsave','fill-record-cap.ddsave.bak'){
  $path=Join-Path $caseRoot $name;$original=Digest $path;$s=$store.Load($path)
  $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
  $session.Restore($path);$out=Join-Path $Run ($name+'.restored');$session.Save($out)
  Require ((Digest $out)-eq$original-and(Digest $path)-eq$original) 'Retained original failed-run save changed or did not strictly restore.'
  $rows+=@{file=$name;sha256=$original;revision=$s.Revision;fillCount=$s.WaterFills.Length;reservations=$s.Work.Reservations.Count;strictRestoreExact=$true}
 }
 $report.status='PASS_BOUNDED_TRIAGE';$report.originalFiles=$rows;$report.sameFrozenAssemblies=$true;$report.isolatedObservedExitCode=0
 $report.disposition='Original raw case and eventual worker failure remain failures. Exact same-DLL case passed once in a fresh directory. Both retained primary/backup strictly restore. No evidence identifies the OS handle/process cause; no runtime retry or persistence-policy change. GPT agreement on finite reconciliation remains pending.'
}catch{$report.error=$_.Exception.ToString()}
finally{$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'result.json');Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS_BOUNDED_TRIAGE'){throw $report.error}
