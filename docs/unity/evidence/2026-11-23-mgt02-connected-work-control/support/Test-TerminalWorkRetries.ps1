param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Artifacts,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop';$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path;$Artifacts=(Resolve-Path $Artifacts).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path $Run){throw 'Fresh output required.'};$null=New-Item -ItemType Directory -Path $Run;Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$report=[ordered]@{status='RUNNING';checks=@();sourceRun=$AssemblyRoot;startedUtc=[DateTime]::UtcNow.ToString('o')}
function Require([bool]$ok,[string]$why){if(!$ok){throw $why}}
function Digest($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
try{
 foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
 $store=[Decennium.Foundation.FileSaveStore]::new()
 $inputs=@(@{file='branches-01/ResearchCancelPositive/cancelled.ddsave';kind='CancelFormulaWork'},@{file='branches-01/ManufacturingCancelPositive/final.ddsave';kind='CancelManufacturing'},@{file='principal-prefix-02/r107.ddsave';kind='ResolveManufacturingQuality'})
 foreach($caseSpec in $inputs){
  $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
  $parent=Join-Path $Artifacts $caseSpec.file;$session.Restore($parent);$state=$store.Load($parent)
  $receipt=@($state.Receipts|Where-Object{[Decennium.Foundation.CommandHistory]::Read($_).Kind.ToString()-eq$caseSpec.kind})[-1]
  $command=[Decennium.Foundation.CommandHistory]::Read($receipt);$q=$session.QueryCommand('Player',$command);$r=$session.Submit('Player',$command)
  $output=Join-Path $Run ($caseSpec.kind+'.ddsave');$session.Save($output)
  Require ($q.Code-eq'AlreadyCommitted'-and$r.Response.ToString()-eq'Duplicate'-and(Digest $parent)-eq(Digest $output)) "Terminal retry diverged: $($caseSpec.kind) / $($q.Code) / $($r.Response)"
  $session.SetSeatEnabled('Player',$false);$revokedQuery=$session.QueryCommand('Player',$command);$revoked=$session.Submit('Player',$command);$session.Save($output+'.revoked')
  Require ($revokedQuery.Code-eq'NotAuthorized'-and$revoked.Response.ToString()-eq'NotAuthorized'-and(Digest $output)-eq(Digest ($output+'.revoked'))) 'Revoked terminal retry bypassed authority or mutated state.'
  $report.checks+=@{kind=$caseSpec.kind;parent=$parent;parentSha256=Digest $parent;query=$q;result=$r;revokedQuery=$revokedQuery;revokedResult=$revoked;canonicalRngClaimsUnchanged=$true}
 }
 $report.status='PASS'
}catch{$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 14|Set-Content -LiteralPath (Join-Path $Run 'result.json');Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS'){throw $report.error}
