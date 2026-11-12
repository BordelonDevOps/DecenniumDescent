param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
$awarePath = Join-Path $OutputRoot 'schema89-aware-replayed.json'
$original = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'baseline.json') -Raw | ConvertFrom-Json -AsHashtable
& (Join-Path $PSScriptRoot 'Verify-SurpriseEntryBaseline.ps1') -AssemblyRoot $AssemblyRoot -OutputFile $awarePath
$replay = Get-Content -LiteralPath $awarePath -Raw | ConvertFrom-Json -AsHashtable
$assemblies = $replay.assemblies
$original.Remove('assemblies')
$replay.Remove('assemblies')
if (($original | ConvertTo-Json -Depth 20 -Compress) -cne ($replay | ConvertTo-Json -Depth 20 -Compress)) {
    throw 'The entire original schema 89 aware baseline changed under the new assemblies.'
}

$predecessor = 'docs/unity/evidence/2026-11-11-exp07-physical-reengagement'
$manifest = Get-Content -LiteralPath "$predecessor/BINDINGS.json" -Raw | ConvertFrom-Json -AsHashtable
if ($manifest.sourceCommit -cne '344c33f11fbd4c2d3919c2f3f68cb0ec4db072b1') { throw 'Unexpected predecessor binding.' }
$method = [Decennium.Foundation.Tests.FoundationCases].GetMethod('ReengagementPolicy', [Reflection.BindingFlags]'Static,NonPublic')
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Hash([byte[]]$Bytes) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant() }
$saves = @(foreach ($name in 'exp07-reengagement-contact.ddsave','exp07-reengagement-closed.ddsave','exp07-reengagement-continued.ddsave') {
    $path = "$predecessor/focused/saves/$name"
    $raw = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $path).Path)
    $sha = Hash $raw
    if ($sha -cne $manifest.artifacts["save:$name"].sha256) { throw "Authentic schema 89 save changed: $name" }
    $state = $codec.Decode($raw)
    $policy = $method.Invoke($null, @($null,$null,$true,$true))
    $restore = [Decennium.Foundation.Simulation]::new($policy, $state, [Decennium.Foundation.ExecutionProfile]::Laboratory)
    $actual = $restore.Capture()
    if ($actual.SchemaVersion -ne 89 -or $actual.SurpriseEntry -or $sha -cne (Hash ($codec.Encode($actual)))) {
        throw "Schema 89 roundtrip failed: $name"
    }
    [ordered]@{ path=$path; sha256=$sha; bytes=$raw.Length; schema=$actual.SchemaVersion; clock=$actual.RuleClock.ToString()
        revision=$actual.Revision; phase=if($actual.Encounter){$actual.Encounter.Id}; archives=@($actual.ClosedEncounters.Encounter.Id) }
})
[ordered]@{status='PASS'; awareBaseline='All observed values and final save bytes matched'; awareFinalSaveSha256=$replay.finalSaveSha256
    predecessorSource=$manifest.sourceCommit; assemblies=$assemblies; authenticSaves=$saves} |
    ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $OutputRoot 'results.json') -Encoding utf8
