param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$MainCheckpoints,[Parameter(Mandatory)][string]$BranchRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$MainCheckpoints=(Resolve-Path -LiteralPath $MainCheckpoints).Path
$BranchRoot=(Resolve-Path -LiteralPath $BranchRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$exporter=Join-Path $PSScriptRoot 'Export-LongRestTrace.ps1'
$driver=Join-Path $PSScriptRoot 'Test-LongRestPaths.ps1'
$campaigns=@(
    @{name='before';checkpoints=$MainCheckpoints;final='long-rest-cadence-172799.ddsave'},
    @{name='after';checkpoints=$MainCheckpoints;final='long-rest-cadence-172801.ddsave'},
    @{name='whole';checkpoints=(Join-Path $BranchRoot 'whole');final='long-rest-whole-funded.ddsave'},
    @{name='capped-debt';checkpoints=(Join-Path $BranchRoot 'capped-debt');final='long-rest-debt-capped.ddsave'}
)
$report=[ordered]@{status='RUNNING';startedUtc=[DateTime]::UtcNow.ToString('o');assemblyRoot=$AssemblyRoot;
    exporterSha256=(Get-FileHash -LiteralPath $exporter).Hash.ToLowerInvariant();driverSha256=(Get-FileHash -LiteralPath $driver).Hash.ToLowerInvariant();campaigns=@()}
$report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'started.json') -Encoding utf8
try {
    foreach($campaign in $campaigns){
        $trace=Join-Path $Run ('trace-'+$campaign.name);$paths=Join-Path $Run ('paths-'+$campaign.name)
        & pwsh -NoProfile -File $exporter -AssemblyRoot $AssemblyRoot -FinalSave (Join-Path $campaign.checkpoints $campaign.final) -CheckpointDirectory $campaign.checkpoints -Run $trace
        if($LASTEXITCODE-ne0){throw "Export failed: $($campaign.name)"}
        & pwsh -NoProfile -File $driver -AssemblyRoot $AssemblyRoot -TraceRoot $trace -Run $paths
        if($LASTEXITCODE-ne0){throw "Execution paths failed: $($campaign.name)"}
        $result=Get-Content -LiteralPath (Join-Path $paths 'results.json') -Raw|ConvertFrom-Json
        if($result.status-ne'PASS'){throw "Execution paths did not pass: $($campaign.name)"}
        $report.campaigns+=@{name=$campaign.name;trace=$trace;paths=$paths;resultSha256=(Get-FileHash -LiteralPath (Join-Path $paths 'results.json')).Hash.ToLowerInvariant()}
        $report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
    }
    $report.status='PASS'
} catch {$report.status='FAIL';$report.error=$_.ToString()}
finally {$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
