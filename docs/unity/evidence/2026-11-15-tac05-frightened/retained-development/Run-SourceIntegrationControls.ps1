param([Parameter(Mandatory)][string]$AssemblyRoot)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$assemblies = @('Core','Persistence','LabModel','HeadlessTests')
foreach ($name in $assemblies) { Add-Type -Path (Join-Path $AssemblyRoot ("Decennium.Foundation.$name.dll")) }
$all = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$names = @($all | Where-Object {
    ($_.StartsWith('condition_') -or $_.StartsWith('tac05_frightened_')) -and
    -not $_.StartsWith('tac05_frightened_connected_')
})
if ($names.Count -eq 0) { throw 'No controls selected.' }
$all | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'source-integration-inventory.txt') -Encoding utf8
$started = [DateTime]::UtcNow.ToString('o')
$results = @($names | ForEach-Object { [Decennium.Foundation.Tests.FoundationCases]::Run($_,
    (Join-Path $PSScriptRoot ('source-integration-controls/' + $_))) })
$failed = @($results | Where-Object { -not $_.Passed })
[ordered]@{
    status=$(if ($failed.Count -eq 0) {'PASS'} else {'FAIL'})
    scope='Focused component controls; both connected cases are retained separately. Not full regression or TAC05 acceptance.'
    startedUtc=$started;finishedUtc=[DateTime]::UtcNow.ToString('o')
    compiledSourceReport=(Join-Path $AssemblyRoot 'results.json')
    assemblies=@($assemblies | ForEach-Object {
        $file=Join-Path $AssemblyRoot ("Decennium.Foundation.$_.dll")
        @{name=$_;sha256=(Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant()}
    })
    passed=$results.Count-$failed.Count;failed=$failed.Count;cases=$results
} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'source-integration-controls.json') -Encoding utf8
Write-Output ("Focused controls: " + ($results.Count-$failed.Count) + '/' + $results.Count)
$failed | Format-List
if ($failed.Count -ne 0) { exit 1 }
