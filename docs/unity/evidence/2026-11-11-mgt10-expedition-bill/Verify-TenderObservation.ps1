param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SavePath,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core', 'Persistence' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$store = [Decennium.Foundation.FileSaveStore]::new()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$original = $store.Load((Resolve-Path $SavePath).Path)
$job = $original.ExpeditionBills[0]
if ($original.SchemaVersion -ne 81 -or $original.ExpeditionBills.Length -ne 1 -or $null -eq $job.Report) {
    throw 'Select the retained reconciled schema 81 state.'
}
$expected = 'Expedition bill traced tender observation contradicts paid title history.'
$control = $codec.Encode($original)
if ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($control)) -ne (Get-FileHash -LiteralPath $SavePath).Hash) {
    throw 'The original state is not a byte-identical control.'
}
$results = foreach ($case in @('wrong-owner', 'wrong-count')) {
    $changed = $original.Copy()
    $observedOwner = if ($case -eq 'wrong-owner') { $job.WorkerId } else { $job.Report.OwnerId }
    $observedCount = if ($case -eq 'wrong-count') { [Decennium.Foundation.RuleQuantity]::new(3) } else { $job.Report.PhysicalCount }
    $observation = [Decennium.Foundation.ExpeditionBillTenderObservation]::new($observedOwner, $observedCount)
    $changed.ExpeditionBills[0] = [Decennium.Foundation.ExpeditionBillRecord]::new($job.Id, $job.WorkerId, $job.Basis,
        $job.StartRevision, $job.UpdatedRevision, $job.UpdatedAt, $job.Work.Labor, $job.Status, $job.Reason, $observation)
    try {
        $null = $codec.Encode($changed)
        throw "Altered observation accepted: $case"
    } catch {
        if ($_.Exception.InnerException.Message -ne $expected) { throw }
        [ordered]@{ case = $case; status = 'PASS'; rejectedBy = $expected }
    }
}
[ordered]@{
    status = 'PASS'
    schema = $original.SchemaVersion
    observedAt = $job.UpdatedAt.ToString()
    originalStartRevision = $job.StartRevision
    originalUpdatedRevision = $job.UpdatedRevision
    originalSaveSha256 = (Get-FileHash -LiteralPath $SavePath).Hash.ToLowerInvariant()
    assemblies = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant() }
    })
    cases = @($results)
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output 'PASS: wrong owner and wrong count each reach the tender guard with original command provenance.'
