param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh focused output directory'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$binding=Start-GeometryExecutionBinding $Run @($PSCommandPath,(Join-Path $repository 'engine/tools/Test-Foundation.ps1'))
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
$build=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
if($build.status-ne'PASS'){throw 'Compiled build must pass its selected case'}
function Check-Sources{foreach($row in $build.sourceHashes){if((Digest (Join-Path (Join-Path $repository 'engine') $row.path))-cne$row.sha256){throw "Compiled source differs: $($row.path)"}}}
Check-Sources
$assemblies=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";$assembly=[Reflection.Assembly]::LoadFrom($file)
    if($assembly.Location-cne$file){throw 'Unexpected loaded assembly'}
    $assemblies[$part]=@{path=$file;sha256=(Digest $file);moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
$names=@([Decennium.Foundation.Tests.FoundationCases]::Names()|Where-Object {$_.StartsWith('tac03_declared_geometry_')})
if($names.Count-ne6){throw 'Expected all six geometry cases'}
$report=[ordered]@{status='FAIL';scope='All six geometry cases on one unchanged build; not full regression';startedUtc=[DateTime]::UtcNow.ToString('o');compiledReportSha256=(Digest (Join-Path $AssemblyRoot 'results.json'));assemblies=$assemblies;cases=@();sourceHashes=$build.sourceHashes}
try {
    foreach($name in $names){
        $report.cases+= [Decennium.Foundation.Tests.FoundationCases]::Run($name,(Join-Path (Join-Path $Run 'saves') $name))
        $report.cases|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
    }
    Check-Sources
    foreach($row in $assemblies.Values){if((Digest $row.path)-cne$row.sha256){throw 'Loaded assembly changed'}}
    if(@($report.cases|Where-Object {!$_.Passed-or$_.Error}).Count){throw 'Focused case failure'}
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $binding;$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 9|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
$report.cases|ConvertTo-Json -Depth 5
if($report.status-ne'PASS'){throw $report.error}
