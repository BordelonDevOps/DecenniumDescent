param(
    [Parameter(Mandatory = $true)][string]$SavePath,
    [Parameter(Mandatory = $true)][string]$AssemblyDirectory,
    [string]$ResultsPath = (Join-Path $PSScriptRoot 'final/historical-save-roundtrip/results.json')
)
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$save = [IO.Path]::GetFullPath($SavePath)
$assemblies = [IO.Path]::GetFullPath($AssemblyDirectory)
$result = [ordered]@{ status = 'FAIL'; schema = 0; source = ''; bytes = 0; originalSha256 = ''; roundtripSha256 = ''; byteIdentical = $false; testedWith = 'Current schema66 Core/Persistence Roslyn build' }
try {
    Add-Type -Path (Join-Path $assemblies 'Decennium.Foundation.Core.dll')
    Add-Type -Path (Join-Path $assemblies 'Decennium.Foundation.Persistence.dll')
    $bytes = [IO.File]::ReadAllBytes($save)
    $codec = [Decennium.Foundation.SnapshotCodec]::new()
    $snapshot = $codec.Decode($bytes)
    $roundtrip = $codec.Encode($snapshot)
    $originalHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    $roundtripHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($roundtrip)).ToLowerInvariant()
    $identical = $bytes.Length -eq $roundtrip.Length -and $originalHash -ceq $roundtripHash
    $result.schema = $snapshot.SchemaVersion
    $result.source = [IO.Path]::GetRelativePath($repoRoot, $save)
    $result.bytes = $bytes.Length
    $result.originalSha256 = $originalHash
    $result.roundtripSha256 = $roundtripHash
    $result.byteIdentical = $identical
    if ($snapshot.SchemaVersion -ne 65 -or -not $identical) { throw 'Historical schema65 save was not byte-identical after codec roundtrip.' }
    $result.status = 'PASS'
} catch {
    $result.error = $_.ToString()
} finally {
    $output = [IO.Path]::GetFullPath($ResultsPath)
    New-Item -ItemType Directory -Force -Path (Split-Path $output) | Out-Null
    $result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $output -Encoding utf8
    Write-Output ($result.status + ': schema65 byte-identical roundtrip; ' + $output)
}
if ($result.status -ne 'PASS') { Write-Error $result.error; exit 1 }
