param([string]$BindingPath = (Join-Path $PSScriptRoot 'SOURCE_BINDINGS.json'))
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$bindingPath = [IO.Path]::GetFullPath($BindingPath)
$bindingRoot = Split-Path $bindingPath
$report = [ordered]@{
    status = 'FAIL'
    sourceRevision = ''
    sourcesChecked = 0
    sources = @()
}
try {
    $binding = Get-Content -Raw -LiteralPath $bindingPath | ConvertFrom-Json
    $report.sourceRevision = $binding.sourceRevision
    foreach ($source in $binding.sources) {
        $revisionPath = $binding.sourceRevision + ':' + $source.path
        $pinnedBlob = (& git -C $repoRoot rev-parse --verify $revisionPath 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -ne 0 -or $pinnedBlob -cne $source.blob) {
            throw ('Pinned Git blob mismatch for ' + $source.path + ': ' + $pinnedBlob)
        }
        $snapshotPath = [IO.Path]::GetFullPath((Join-Path $bindingRoot $source.snapshot))
        $snapshotHash = (Get-FileHash -LiteralPath $snapshotPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($snapshotHash -cne $source.sha256) {
            throw ('Pinned snapshot hash mismatch for ' + $source.snapshot)
        }
        $workingPath = [IO.Path]::GetFullPath((Join-Path $repoRoot $source.path))
        $workingHash = (Get-FileHash -LiteralPath $workingPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($workingHash -cne $source.sha256) {
            throw ('Working source hash mismatch for ' + $source.path)
        }
        $report.sources += [ordered]@{
            path = $source.path
            blob = $pinnedBlob
            snapshotSha256 = $snapshotHash
            workingSha256 = $workingHash
            status = 'PASS'
        }
        $report.sourcesChecked++
    }
    $report.status = 'PASS'
} catch {
    $report.error = $_.ToString()
} finally {
    $report.finishedUtc = [DateTime]::UtcNow.ToString('o')
    $outputPath = Join-Path $bindingRoot 'SOURCE_BINDINGS_VALIDATION.json'
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $outputPath -Encoding utf8
    Write-Output ($report.status + ': ' + $report.sourcesChecked + ' pinned source snapshots; ' + $outputPath)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
