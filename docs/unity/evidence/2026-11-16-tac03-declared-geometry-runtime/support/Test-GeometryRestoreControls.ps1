param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ValidSource,
    [Parameter(Mandatory)][string]$ForgedSource,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ValidSource=(Resolve-Path -LiteralPath $ValidSource).Path;$ForgedSource=(Resolve-Path -LiteralPath $ForgedSource).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh restore-control directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $Run @($PSCommandPath)
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";$assembly=[Reflection.Assembly]::LoadFrom($file)
    Require ($assembly.Location-ceq$file) 'Unexpected loaded assembly.'
    $loaded[$part]=@{sha256=(Digest $file);moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
function Rejected([scriptblock]$operation){$failed=$false;try{& $operation}catch{$failed=$true};Require $failed 'Expected explicit rejection.'}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
$store=[Decennium.Foundation.FileSaveStore]::new();$report=[ordered]@{status='FAIL';scope='Actual wire113 public restore and explicit backup recovery; disposable test files only';pid=$PID;assemblies=$loaded}
try{
    Require ($store.Load($ValidSource).WireSchemaVersion-eq113) 'Current valid source must be wire113.'
    Require ($store.Load($ForgedSource).WireSchemaVersion-eq113) 'Causal forgery must pass structural/checksum decoding.'
    $session.Restore($ValidSource);$original=Join-Path $Run 'live-before.ddsave';$session.Save($original)
    $target=Join-Path $Run 'recovery.ddsave';$session.Save($target);$session.Save($target)
    Copy-Item -LiteralPath ($target+'.bak') -Destination (Join-Path $Run 'preserved-valid-backup.ddsave')
    $valid=Digest ($target+'.bak');$bytes=[IO.File]::ReadAllBytes($target);$bytes[11]=$bytes[11]-bxor 128;[IO.File]::WriteAllBytes($target,$bytes)
    $corrupt=Digest $target
    Rejected {$session.Restore($target)};Rejected {$session.Save($target)}
    $session.Save((Join-Path $Run 'after-corrupt-rejections.ddsave'))
    Require ((Digest $target)-ceq$corrupt-and(Digest ($target+'.bak'))-ceq$valid-and(Digest $original)-ceq(Digest (Join-Path $Run 'after-corrupt-rejections.ddsave'))) 'Corrupt primary rejection changed live state or good backup.'
    $displaced=$session.RecoverBackup($target)
    Require ((Digest $displaced)-ceq$corrupt-and(Digest $target)-ceq$valid-and(Digest ($target+'.bak'))-ceq$valid) 'Explicit recovery did not preserve both input files.'
    $session.Save((Join-Path $Run 'after-explicit-recovery.ddsave'))
    Require ((Digest $original)-ceq(Digest (Join-Path $Run 'after-explicit-recovery.ddsave'))) 'Explicit good backup recovery changed canonical state.'
    [IO.File]::WriteAllBytes($target,$bytes);[IO.File]::WriteAllBytes(($target+'.bak'),[IO.File]::ReadAllBytes($ForgedSource))
    $forged=Digest ($target+'.bak');Rejected {$session.RecoverBackup($target)}
    $session.Save((Join-Path $Run 'after-forged-backup-rejection.ddsave'))
    Require ((Digest $target)-ceq$corrupt-and(Digest ($target+'.bak'))-ceq$forged-and(Digest $original)-ceq(Digest (Join-Path $Run 'after-forged-backup-rejection.ddsave'))) 'Rejected causal backup mutated files or live state.'
    $report.status='PASS';$report.validSourceSha256=Digest $ValidSource;$report.forgedSourceSha256=Digest $ForgedSource
    $report.corruptPrimarySha256=$corrupt;$report.displacedPrimary=[IO.Path]::GetFileName($displaced);$report.canonicalLiveSha256=Digest $original
    $report.checks=@('Structurally valid causal forgery independently decodes','Corrupt primary rejects without fallback','Saving over corrupt primary preserves good backup',
        'Explicit good backup recovery preserves displaced primary and backup','Causal forged backup rejects before file replacement or live adoption')
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $executionSourceBinding;$report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output 'PASS: wire113 corrupt-primary and explicit validated backup recovery controls.'
