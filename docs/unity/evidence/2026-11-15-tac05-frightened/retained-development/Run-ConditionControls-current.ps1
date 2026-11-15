$ErrorActionPreference = 'Stop'
$runRoot = Join-Path $PSScriptRoot 'run-20261115T081942630Z-1533a130'
$assemblies = @('Decennium.Foundation.Core','Decennium.Foundation.Persistence','Decennium.Foundation.LabModel','Decennium.Foundation.HeadlessTests')
foreach ($name in $assemblies) { Add-Type -Path (Join-Path $runRoot ($name + '.dll')) }
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names() | Where-Object { $_.StartsWith('condition_') -or $_.StartsWith('tac05_frightened_') })
if ($names.Count -eq 0) { throw 'No condition cases selected.' }
[Decennium.Foundation.Tests.FoundationCases]::Names() | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'development-inventory.txt') -Encoding utf8
$started = [DateTime]::UtcNow.ToString('o')
$cases = @($names | ForEach-Object { [Decennium.Foundation.Tests.FoundationCases]::Run($_,(Join-Path $PSScriptRoot ('condition-controls-current/' + $_))) })
$failed = @($cases | Where-Object { -not $_.Passed })
$report = [ordered]@{status=$(if ($failed.Count -eq 0) {'PASS'} else {'FAIL'});scope='focused shared condition regression, not full TAC05 acceptance';startedUtc=$started;finishedUtc=[DateTime]::UtcNow.ToString('o');compiledSourceReport=(Join-Path $runRoot 'results.json');assemblies=@($assemblies | ForEach-Object { $p=Join-Path $runRoot ($_+'.dll'); @{name=$_;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()} });passed=$cases.Count-$failed.Count;failed=$failed.Count;cases=$cases}
$report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'condition-controls-current.json') -Encoding utf8
Write-Output ($report.status+': '+$report.passed+'/'+$cases.Count)
$failed | Format-List
if ($failed.Count -ne 0) { exit 1 }
