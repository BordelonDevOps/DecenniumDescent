param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ValidSource,
    [Parameter(Mandatory)][string]$ForgedSource,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ValidSource=(Resolve-Path -LiteralPath $ValidSource).Path;$ForgedSource=(Resolve-Path -LiteralPath $ForgedSource).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh restore-control directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
function Rejected([scriptblock]$operation){$failed=$false;try{& $operation}catch{$failed=$true};Require $failed 'Expected explicit rejection.'}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithBishopEntry(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
$store=[Decennium.Foundation.FileSaveStore]::new();$report=[ordered]@{status='FAIL';scope='Actual wire112 public restore and explicit backup recovery; disposable test files only';pid=$PID}
try{
    Require ($store.Load($ValidSource).WireSchemaVersion-eq112) 'Current valid source must be wire112.'
    Require ($store.Load($ForgedSource).WireSchemaVersion-eq112) 'Causal forgery must pass structural/checksum decoding.'
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
finally{$report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output 'PASS: wire112 corrupt-primary and explicit validated backup recovery controls.'
