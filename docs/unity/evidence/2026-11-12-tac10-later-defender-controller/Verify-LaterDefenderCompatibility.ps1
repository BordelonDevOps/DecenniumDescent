param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
$prior = Join-Path $PSScriptRoot '../2026-11-12-mgt04-connected-recipe4-batch'
$binding = Get-Content -LiteralPath (Join-Path $prior 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
if ($binding.implementationCommit -cne '0f4d1139dd28a4c8d1051ca82fa81adc2b336dfb') {
    throw 'The wire95 predecessor implementation does not match the reviewed source.'
}
$saves = @($binding.artifacts.Keys | Where-Object { $_ -clike 'focused/saves/*.ddsave' } | Sort-Object)
if ($saves.Count -ne 22) { throw 'Unexpected authentic predecessor save inventory.' }
foreach ($save in $saves) {
    $file = Join-Path $prior $save
    if ((Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant() -cne $binding.artifacts[$save].sha256) {
        throw "Authentic predecessor bytes changed: $save"
    }
}
& (Join-Path $prior 'Measure-ConnectedRecipe4Batch.ps1') -AssemblyRoot $AssemblyRoot `
    -SaveRoot (Join-Path $prior 'focused/saves') -OutputPath $OutputPath
