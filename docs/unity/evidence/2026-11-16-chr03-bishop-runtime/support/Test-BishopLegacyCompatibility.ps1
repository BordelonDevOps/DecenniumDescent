param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$evidence=Join-Path $repository 'docs/unity/evidence'
if(Test-Path -LiteralPath $Run){throw 'Use a fresh compatibility directory.'}
& pwsh -NoProfile -File (Join-Path $evidence '2026-11-16-exp07-post-recovery/support/Test-Compatibility.ps1') -AssemblyRoot $AssemblyRoot -Run $Run
if($LASTEXITCODE-ne0){throw 'Authentic predecessor continuation failed.'}
$Run=(Resolve-Path -LiteralPath $Run).Path
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";$assembly=[Reflection.Assembly]::LoadFrom($file)
    Require ($assembly.Location-ceq$file) 'Unexpected loaded assembly.'
    $loaded[$part]=@{sha256=(Digest $file);moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
$compat=Get-Content -LiteralPath (Join-Path $Run 'results.json') -Raw|ConvertFrom-Json
Require ($compat.Status-eq'PASS'-and$compat.Cases.Count-eq28) 'All authentic predecessors must pass.'
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithBishopEntry(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
$before=Join-Path $Run 'bishop-before.ddsave';$session.Save($before);$rows=[Collections.Generic.List[object]]::new()
foreach($case in $compat.Cases){
    $source=Join-Path $evidence $case.Source;Require ((Digest $source)-ceq$case.SourceSha256) 'Authentic source changed.'
    $rejected=$false;try{$session.Restore($source)}catch{$rejected=$true}
    Require $rejected "Bishop accepted incompatible wire$($case.Wire)."
    $after=Join-Path $Run ('bishop-after-'+$rows.Count+'.ddsave');$session.Save($after)
    Require ((Digest $after)-ceq(Digest $before)-and(Digest $source)-ceq$case.SourceSha256) 'Rejected restore mutated live state or input.'
    $rows.Add(@{source=$case.Source;wire=$case.Wire;sourceSha256=$case.SourceSha256;after=[IO.Path]::GetFileName($after);unchangedSha256=(Digest $after)})
}
[ordered]@{status='PASS';scope='Wire112 rejects each authentic wire95-110 checkpoint without adopting or altering it';pid=$PID;
    assemblies=$loaded;compatibilityReportSha256=(Digest (Join-Path $Run 'results.json'));rejections=$rows;beforeSha256=(Digest $before)}
    |ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'bishop-profile-results.json') -Encoding utf8
Write-Output 'PASS: Bishop profile rejected all 28 authentic wire95-110 saves unchanged.'
