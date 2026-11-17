param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CompatibilityRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$CompatibilityRoot=(Resolve-Path -LiteralPath $CompatibilityRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh rejection-control directory'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$binding=Start-GeometryExecutionBinding $Run @($PSCommandPath)
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){$file=(Resolve-Path -LiteralPath (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")).Path;$a=[Reflection.Assembly]::LoadFrom($file);Require ($a.Location-ceq$file) 'Unexpected assembly';$loaded[$part]=@{sha256=(Digest $file);moduleId=$a.ManifestModule.ModuleVersionId.ToString()}}
$cases=[Collections.Generic.List[object]]::new()
$old=Get-Content -LiteralPath (Join-Path $CompatibilityRoot 'compatibility95-110/results.json') -Raw|ConvertFrom-Json
Require ($old.Status-eq'PASS'-and$old.Cases.Count-eq28) 'Authentic95-110 qualification must pass first'
foreach($case in $old.Cases){$cases.Add(@{wire=$case.Wire;path=(Join-Path (Join-Path $repository 'docs/unity/evidence') $case.Source);sha256=$case.SourceSha256})}
foreach($wire in 111,112){
    $folder=Join-Path $CompatibilityRoot ('wire'+$wire);$report=Get-Content -LiteralPath (Join-Path $folder 'results.json') -Raw|ConvertFrom-Json
    Require ($report.status-eq'PASS') "Authentic$wire qualification must pass first"
    foreach($mark in Get-Content -LiteralPath (Join-Path $folder 'sources/marks.json') -Raw|ConvertFrom-Json){$cases.Add(@{wire=$wire;path=(Join-Path (Join-Path $folder 'sources') $mark.name);sha256=$mark.sha256})}
}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
$codec=[Decennium.Foundation.SnapshotCodec]::new()
function Live-Digest{$sim=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($session);[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($sim.Capture()))).ToLowerInvariant()}
$session.Save((Join-Path $Run 'before.ddsave'));$stable=Live-Digest
$report=[ordered]@{status='FAIL';scope='Declared113 rejects every authenticated predecessor without migration, repair, file mutation or live adoption';assemblies=$loaded;cases=@()}
try {
    foreach($case in $cases){
        Require ((Digest $case.path)-ceq$case.sha256) 'Authentic input changed'
        $errorText=$null;try{$session.Restore($case.path)}catch{$errorText=$_.Exception.Message}
        Require ($null-ne$errorText) "Declared113 adopted wire$($case.wire)"
        $after=Live-Digest;Require ($after-ceq$stable-and(Digest $case.path)-ceq$case.sha256) 'Rejected predecessor changed files or state'
        $report.cases+=@{wire=$case.wire;source=$case.path;sourceSha256=$case.sha256;error=$errorText;unchangedSha256=$after}
    }
    $session.Save((Join-Path $Run 'after.ddsave'));Require ((Digest (Join-Path $Run 'before.ddsave'))-ceq(Digest (Join-Path $Run 'after.ddsave'))) 'Final canonical state changed'
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $binding;$report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output "PASS: declared113 rejected $($cases.Count) authenticated95-112 predecessor saves unchanged."
