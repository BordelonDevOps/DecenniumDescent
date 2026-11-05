param([string]$ResultsRoot = (Join-Path $PSScriptRoot '../artifacts'))
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Core') { throw 'Run with PowerShell 7 (pwsh), not Windows PowerShell 5.' }
$engineRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$packageRoot = Join-Path $engineRoot 'com.decennium.foundation'
$runDirectory = Join-Path ([IO.Path]::GetFullPath($ResultsRoot)) ('compile-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $runDirectory | Out-Null
$resultFile = Join-Path $runDirectory 'results.json'
$sources = @()
$report = [ordered]@{
    status = 'FAIL'
    runner = 'PowerShell Roslyn shared-source compilation'
    language = 'C# 9'
    powershell = $PSVersionTable.PSVersion.ToString()
    runtime = [System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    startedUtc = [DateTime]::UtcNow.ToString('o')
    compilation = [ordered]@{ core = 'NOT RUN'; persistence = 'NOT RUN'; labModel = 'NOT RUN' }
    tests = 'NOT RUN'
    unityCompilation = 'NOT RUN'
}
try {
    $referenceAssemblies = @(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
    if ($referenceAssemblies.Count -eq 0) { throw 'PowerShell reference assemblies unavailable.' }
    $options = @('/langversion:9.0','/warnaserror','/define:DECENNIUM_TEST_ONLY,HEADLESS_TESTS')
    $groups = @(
        @{ Name = 'Decennium.Foundation.Core'; Key = 'core'; Pattern = 'Runtime/Core/*.cs' },
        @{ Name = 'Decennium.Foundation.Persistence'; Key = 'persistence'; Pattern = 'Runtime/Persistence/*.cs' },
        @{ Name = 'Decennium.Foundation.LabModel'; Key = 'labModel'; Pattern = 'Laboratory/Model/*.cs' }
    )
    foreach ($group in $groups) {
        $files = @(Get-ChildItem -Path (Join-Path $packageRoot $group.Pattern) -File | ForEach-Object FullName)
        if ($files.Count -eq 0) { throw ('No sources for ' + $group.Name) }
        $sources += $files
        $assembly = Join-Path $runDirectory ($group.Name + '.dll')
        Add-Type -Path $files -OutputAssembly $assembly -ReferencedAssemblies $referenceAssemblies -CompilerOptions $options
        Add-Type -Path $assembly
        $referenceAssemblies += $assembly
        $report.compilation[$group.Key] = 'PASS'
    }
    $report.sourceHashes = @($sources | ForEach-Object {
        @{ path = [IO.Path]::GetRelativePath($engineRoot, $_); sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    $report.status = 'PASS'
} catch {
    $report.error = $_.ToString()
} finally {
    $report.finishedUtc = [DateTime]::UtcNow.ToString('o')
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resultFile -Encoding utf8
    Write-Output ($report.status + ': Core, Persistence and LabModel compilation; ' + $resultFile)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
