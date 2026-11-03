param([string]$ResultsRoot = (Join-Path $PSScriptRoot '../artifacts'))
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Core') { throw 'Run with PowerShell 7 (pwsh), not Windows PowerShell 5.' }
$engineRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$packageRoot = Join-Path $engineRoot 'com.decennium.foundation'
$runDirectory = Join-Path ([IO.Path]::GetFullPath($ResultsRoot)) ('run-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $runDirectory | Out-Null
$resultFile = Join-Path $runDirectory 'results.json'
$sources = @()
$report = [ordered]@{ status='FAIL'; runner='PowerShell Roslyn shared-source regression'; language='C# 9';
    powershell=$PSVersionTable.PSVersion.ToString(); runtime=[System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription;
    startedUtc=[DateTime]::UtcNow.ToString('o'); testsDiscovered=0; passed=0; failed=0;
    unityCompilation='NOT RUN'; editMode='NOT RUN'; playMode='NOT RUN'; standaloneBuild='NOT RUN'; gameplay='NOT RUN' }
try {
    $referenceAssemblies = @(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
    if ($referenceAssemblies.Count -eq 0) { throw 'PowerShell reference assemblies unavailable.' }
    $options = @('/langversion:9.0','/warnaserror','/define:DECENNIUM_TEST_ONLY,HEADLESS_TESTS')
    $groups = @(
        @{Name='Decennium.Foundation.Core'; Pattern='Runtime/Core/*.cs'},
        @{Name='Decennium.Foundation.Persistence'; Pattern='Runtime/Persistence/*.cs'},
        @{Name='Decennium.Foundation.LabModel'; Pattern='Laboratory/Model/*.cs'},
        @{Name='Decennium.Foundation.HeadlessTests'; Pattern='Tests/EditMode/*Cases.cs'}
    )
    foreach ($group in $groups) {
        $files = @(Get-ChildItem -Path (Join-Path $packageRoot $group.Pattern) -File | ForEach-Object FullName)
        if ($files.Count -eq 0) { throw ('No sources for ' + $group.Name) }
        $sources += $files
        $assembly = Join-Path $runDirectory ($group.Name + '.dll')
        Add-Type -Path $files -OutputAssembly $assembly -ReferencedAssemblies $referenceAssemblies -CompilerOptions $options
        Add-Type -Path $assembly
        $referenceAssemblies += $assembly
    }
    $results = @([Decennium.Foundation.Tests.FoundationCases]::RunAll((Join-Path $runDirectory 'saves')))
    $report.testsDiscovered = $results.Count
    $report.passed = @($results | Where-Object Passed).Count
    $report.failed = @($results | Where-Object { -not $_.Passed }).Count
    $report.cases = $results
    $report.coreCompilation = 'PASS'
    $report.sourceHashes = @($sources | ForEach-Object { @{path=[IO.Path]::GetRelativePath($engineRoot,$_);sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()} })
    if ($results.Count -eq 0 -or $report.failed -ne 0) { throw 'Regression suite failed or discovered zero tests.' }
    $report.status = 'PASS'
} catch { $report.error = $_.ToString() }
finally {
    $report.finishedUtc = [DateTime]::UtcNow.ToString('o')
    $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $resultFile -Encoding utf8
    Write-Output ($report.status + ': ' + $report.passed + '/' + $report.testsDiscovered + ' cases; ' + $resultFile)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
