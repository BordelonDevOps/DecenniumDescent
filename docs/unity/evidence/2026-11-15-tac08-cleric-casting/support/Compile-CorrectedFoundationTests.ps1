param([Parameter(Mandatory)][string]$OriginalBuild,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$engine=Join-Path $repository 'engine'
$OriginalBuild=(Resolve-Path -LiteralPath $OriginalBuild).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$original=Get-Content -LiteralPath (Join-Path $OriginalBuild 'results.json') -Raw|ConvertFrom-Json
if($original.status-ne'PASS'){throw 'Original engine compilation must pass.'}
$report=[ordered]@{status='FAIL';runner='C#9 complete test recompile linked to unchanged, previously compiled Core/Persistence/LabModel';
    originalBuild=$OriginalBuild;originalReportSha256=(Digest (Join-Path $OriginalBuild 'results.json'));
    startedUtc=[DateTime]::UtcNow.ToString('o');language='C# 9';sourceHashes=@();reusedRuntimeAssemblies=@();testsDiscovered=0;passed=0;failed=0}
try{
    foreach($source in $original.sourceHashes){
        $path=Join-Path $engine $source.path
        $isTest=$source.path.Replace('\','/').Contains('/Tests/')
        $digest=Digest $path
        if(!$isTest-and$digest-cne$source.sha256){throw "Runtime source changed: $($source.path)"}
        $report.sourceHashes+=@{path=$source.path;sha256=$digest}
    }
    $references=@(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll'|ForEach-Object FullName)
    foreach($name in 'Core','Persistence','LabModel'){
        $dll="Decennium.Foundation.$name.dll"
        $source=Join-Path $OriginalBuild $dll
        $destination=Join-Path $Run $dll
        Copy-Item -LiteralPath $source -Destination $destination
        if((Digest $source)-cne(Digest $destination)){throw 'Runtime binary changed during copy.'}
        Add-Type -Path $destination
        $references+=$destination
        $report.reusedRuntimeAssemblies+=@{name=$dll;sha256=(Digest $destination)}
    }
    $files=@(Get-ChildItem -Path (Join-Path $engine 'com.decennium.foundation/Tests/EditMode/*Cases.cs') -File|ForEach-Object FullName)
    $compiled=(Join-Path $Run 'Decennium.Foundation.HeadlessTests.dll')
    Add-Type -Path $files -OutputAssembly $compiled -ReferencedAssemblies $references -CompilerOptions '/langversion:9.0','/warnaserror','/define:DECENNIUM_TEST_ONLY,HEADLESS_TESTS'
    Add-Type -Path $compiled
    $report.testsDiscovered=@([Decennium.Foundation.Tests.FoundationCases]::Names()).Count
    if($report.testsDiscovered-ne1551){throw 'Changed full test inventory.'}
    $case='tac06_connected_companion_stabilization_paid_failure_and_absolute_recovery'
    $result=[Decennium.Foundation.Tests.FoundationCases]::Run($case,(Join-Path $Run 'corrected-case'))
    $report.results=@($result)
    if(!$result.Passed){$report.failed=1;throw $result.Error}
    $report.passed=1
    $report.status='PASS'
}catch{$report.error=$_.Exception.ToString();throw}
finally{
    $report.completedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
}
Write-Output 'PASS: compiled all test sources against the exact frozen engine DLLs; corrected predecessor case passed.'
