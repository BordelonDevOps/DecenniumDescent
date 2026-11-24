param([Parameter(Mandatory)][string]$AssemblyRoot, [Parameter(Mandatory)][string]$ResultsDirectory)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$ResultsDirectory = [IO.Path]::GetFullPath($ResultsDirectory)
if (Test-Path -LiteralPath $ResultsDirectory) { throw 'Use a new results directory.' }
$null = New-Item -ItemType Directory -Path $ResultsDirectory
$compiled = Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw | ConvertFrom-Json
if ($compiled.coreCompilation -ne 'PASS') { throw 'A successful compiled candidate is required.' }
foreach ($part in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")
}
$names = @('int05_materialized_conditions_strict_lookup_and_scope_cleanup', 'int05_private_canonical_comparison_preserves_validated_codec')
$report = [ordered]@{status='RUNNING'; sourceRun=$AssemblyRoot; startedUtc=[DateTime]::UtcNow.ToString('o');
    sourceHashes=$compiled.sourceHashes; assemblyHashes=@(Get-ChildItem -LiteralPath $AssemblyRoot -Filter '*.dll' | ForEach-Object {
        @{name=$_.Name;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}
    }); cases=@(); unityCompilation='NOT RUN'; moduleAcceptance='OPEN'}
try {
    foreach ($name in $names) {
        $path = Join-Path $ResultsDirectory $name
        $null = New-Item -ItemType Directory -Path $path
        $report.cases += [Decennium.Foundation.Tests.FoundationCases]::Run($name, $path)
    }
    $report.status = if ($report.cases.Count -eq $names.Count -and @($report.cases | Where-Object { -not $_.Passed }).Count -eq 0) { 'PASS' } else { 'FAIL' }
} catch { $report.status='FAIL'; $report.error=$_.Exception.ToString() }
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ResultsDirectory 'results.json') -Encoding utf8
    Write-Output ($report.status+': '+$ResultsDirectory)
    foreach($case in $report.cases) { if(-not $case.Passed) { Write-Output ($case.Name+': '+$case.Error) } }
}
if($report.status -ne 'PASS') { exit 1 }
