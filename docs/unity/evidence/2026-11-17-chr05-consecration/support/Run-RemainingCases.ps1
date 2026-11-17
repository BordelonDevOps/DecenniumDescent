param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$CaseList,
    [Parameter(Mandatory)][string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$CaseList = (Resolve-Path -LiteralPath $CaseList).Path
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new result directory; retain previous attempts.' }
$null = New-Item -ItemType Directory -Path $OutputDirectory
$assemblyFiles = @('Core','Persistence','LabModel','HeadlessTests') | ForEach-Object {
    Join-Path $AssemblyRoot ('Decennium.Foundation.' + $_ + '.dll')
}
foreach ($path in $assemblyFiles) { Add-Type -Path $path }
$names = @(Get-Content -LiteralPath $CaseList | Where-Object { $_.Trim().Length -gt 0 })
$registered = @([Decennium.Foundation.Tests.FoundationCases]::Names())
if ($names.Count -eq 0 -or @($names | Select-Object -Unique).Count -ne $names.Count) { throw 'Empty or duplicate case list.' }
foreach ($name in $names) { if ($name -cnotin $registered) { throw ('Unregistered case: ' + $name) } }
$report = [ordered]@{
    status = 'RUNNING'; startedUtc = [DateTime]::UtcNow.ToString('o'); pid = $PID
    powershell = $PSVersionTable.PSVersion.ToString()
    runtime = [System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    assemblyRoot = $AssemblyRoot; caseList = $CaseList
    caseListSha256 = (Get-FileHash -LiteralPath $CaseList -Algorithm SHA256).Hash.ToLowerInvariant()
    assemblies = @($assemblyFiles | ForEach-Object {
        @{name = [IO.Path]::GetFileName($_); sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()}
    })
    registered = $registered.Count; requested = $names.Count; completed = 0; passed = 0; failed = 0
    cases = @(); sourceCommit = '3c5135ae0d664d79528fff1f2676fae2198beb28'
    scope = 'Only unresolved Consecration regression cases on the original frozen assemblies; previous accepted TAC-10 qualification is not restarted.'
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'LAUNCH.json') -Encoding utf8
$journal = Join-Path $OutputDirectory 'journal.jsonl'
foreach ($name in $names) {
    @{phase='START'; name=$name; atUtc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json -Compress |
        Add-Content -LiteralPath $journal -Encoding utf8
    Write-Output ('START ' + $name)
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $result = [Decennium.Foundation.Tests.FoundationCases]::Run($name, (Join-Path $OutputDirectory ('saves/' + $name)))
    $timer.Stop()
    $resultPath = Join-Path $OutputDirectory ($name + '.json')
    $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resultPath -Encoding utf8
    $report.completed++
    if ($result.Passed) { $report.passed++ } else { $report.failed++ }
    $row = @{name=$name; passed=$result.Passed; elapsedMs=$timer.Elapsed.TotalMilliseconds;
        resultSha256=(Get-FileHash -LiteralPath $resultPath -Algorithm SHA256).Hash.ToLowerInvariant()}
    $report.cases += $row
    @{phase='RESULT'; name=$name; passed=$result.Passed; atUtc=[DateTime]::UtcNow.ToString('o');
        resultSha256=$row.resultSha256} | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding utf8
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'PROGRESS.json') -Encoding utf8
    Write-Output ('RESULT ' + $name + ' ' + $result.Passed)
}
$report.finishedUtc = [DateTime]::UtcNow.ToString('o')
$report.status = if ($report.completed -eq $report.requested -and $report.failed -eq 0) { 'PASS' } else { 'FAIL' }
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'TERMINAL.json') -Encoding utf8
if ($report.status -ne 'PASS') { exit 1 }
