param([Parameter(Mandatory)][string]$OutputRoot)
$ErrorActionPreference = 'Stop'
$old = Join-Path $PSScriptRoot '../2026-11-12-mgt05-black-blood-handoff'
$bindings = Get-Content -LiteralPath (Join-Path $old 'BINDINGS.json') -Raw | ConvertFrom-Json
if ($bindings.implementationCommit -cne '246ca4e4899469241402899ba6750d4379d035a9') { throw 'Wrong accepted source.' }
foreach ($input in $bindings.exactExecutedAssemblies) {
    $path = Join-Path $old "focused/assemblies/$($input.name)"
    if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $input.sha256) { throw "Changed assembly $($input.name)" }
    Add-Type -Path $path
}
$null = New-Item -ItemType Directory -Force -Path $OutputRoot
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
function Call-Test([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$seed = Call-Test 'ManufacturingNaturalSeed' @(12)
$origins = @(foreach ($wire in 18,20) {
    $policy = if ($wire -eq 18) { Call-Test 'ManufacturePolicy' @([uint32]$seed,$null,$null,$null) }
        else { Call-Test 'ResolvedPolicy' @([uint32]$seed) }
    $sim = Call-Test 'World' @($policy)
    $null = Call-Test 'LearnManufacturing' @($sim,'recipe-4')
    $null = Call-Test 'ManufactureStart' @($sim,0,0,'recipe-4')
    $null = Call-Test 'WorldAdvance' @($sim,1200,1)
    $state = $sim.Capture()
    if ($state.WireSchemaVersion -ne $wire -or $state.ManufacturingOrders[0].StabilizedAt.ToString() -cne '4500/1') {
        throw "Missing authentic stabilized wire $wire order."
    }
    $file = "wire$wire-recipe4-working.ddsave"
    $path = Join-Path $OutputRoot $file
    [IO.File]::WriteAllBytes($path,$codec.Encode($state))
    [ordered]@{wire=$wire;file=$file;seed=$seed;at=$state.RuleClock.ToString();revision=$state.Revision
        sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
})
[ordered]@{sourceCommit=$bindings.implementationCommit;executedAssemblies=$bindings.exactExecutedAssemblies;saves=$origins} |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputRoot 'origin.json') -Encoding utf8
