param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ValidSource,[Parameter(Mandatory)][string]$HostileRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
if(Test-Path -LiteralPath $Run){throw 'Use a fresh trust-control directory'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $Run @($PSCommandPath)
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){$file=(Resolve-Path -LiteralPath (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")).Path;$a=[Reflection.Assembly]::LoadFrom($file);Require ($a.Location-ceq$file) 'Unexpected loaded binary';$loaded[$part]=@{sha256=(Digest $file);moduleId=$a.ManifestModule.ModuleVersionId.ToString()}}
function Start-Session{[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())}
function Reject([scriptblock]$op){$errorText=$null;try{& $op}catch{$errorText=$_.Exception.Message};Require ($null-ne$errorText) 'Expected rejection';return $errorText}
$session=Start-Session;$session.Restore((Resolve-Path -LiteralPath $ValidSource).Path);$codec=[Decennium.Foundation.SnapshotCodec]::new()
$before=Join-Path $Run 'before.ddsave';$session.Save($before);$stable=Digest $before
$report=[ordered]@{status='FAIL';scope='Actual113 geometry distrust and causal history rejection, with live/file nonmutation';assemblies=$loaded;sourceSha256=(Digest $ValidSource);cases=@()}
try {
    $manifest=Get-Content -LiteralPath (Join-Path $HostileRoot 'manifest.json') -Raw|ConvertFrom-Json
    foreach($case in $manifest.cases){
        $path=(Resolve-Path -LiteralPath (Join-Path $HostileRoot $case.name)).Path
        Require ((Digest $path)-ceq$case.sha256) 'Hostile source changed'
        $decode=Reject {$null=$codec.Decode([IO.File]::ReadAllBytes($path))}
        $restore=Reject {$session.Restore($path)}
        $after=Join-Path $Run ($case.name+'.after.ddsave');$session.Save($after)
        Require ((Digest $after)-ceq$stable-and(Digest $path)-ceq$case.sha256) 'Rejected geometry changed files or live state'
        $report.cases+=@{name=$case.name;sha256=$case.sha256;decodeError=$decode;restoreError=$restore;unchangedSha256=(Digest $after)}
    }
    # Change actual elapsed-time history without changing its structurally valid result.
    $state=$codec.Decode([IO.File]::ReadAllBytes($before));$forged=$state.Copy()
    $receipt=$forged.Receipts|Where-Object {([Decennium.Foundation.CommandHistory]::Read($_)).Kind-eq'AdvanceClock'}|Select-Object -Last 1
    Require ($null-ne$receipt) 'No actual clock receipt to forge'
    $fields=$receipt.Fingerprint.Split('|');$fields[4]=([int]$fields[4]+1).ToString([Globalization.CultureInfo]::InvariantCulture);$receipt.Fingerprint=[string]::Join('|',$fields)
    $history=Join-Path $Run 'forged-history.ddsave';[IO.File]::WriteAllBytes($history,$codec.Encode($forged))
    $decoded=$codec.Decode([IO.File]::ReadAllBytes($history));Require ($decoded.Revision-eq$state.Revision-and$decoded.WireSchemaVersion-eq113) 'Causal forgery must independently pass structural decoding'
    $historyHash=Digest $history;$errorText=Reject {$session.Restore($history)}
    $after=Join-Path $Run 'after-history-rejection.ddsave';$session.Save($after)
    Require ((Digest $after)-ceq$stable-and(Digest $history)-ceq$historyHash) 'Causal forgery rejection changed state or input'
    $report.cases+=@{name='forged-history.ddsave';sha256=$historyHash;structuralDecode='PASS';restoreError=$errorText;unchangedSha256=(Digest $after)}
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $executionSourceBinding;$report|ConvertTo-Json -Depth 9|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output "PASS: $($report.cases.Count) hostile geometry/history inputs rejected without mutation."
