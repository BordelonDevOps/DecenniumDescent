param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
$baselinePath = Join-Path $OutputRoot 'schema51-baseline-replayed.json'
& (Join-Path $PSScriptRoot 'Verify-ExplorationSearchBaseline.ps1') -AssemblyRoot $AssemblyRoot -OutputFile $baselinePath
$replay = Get-Content -LiteralPath $baselinePath -Raw | ConvertFrom-Json -AsHashtable
$original = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'baseline.json') -Raw | ConvertFrom-Json -AsHashtable
$assemblies = $replay.assemblies
$replay.Remove('assemblies')
$original.Remove('assemblies')
if (($replay | ConvertTo-Json -Depth 20 -Compress) -cne ($original | ConvertTo-Json -Depth 20 -Compress)) {
    throw 'The exact old schema51 connected witness changed under the new runtime.'
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Hash([byte[]]$Data) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant()
}
function Restore-Old([string]$Path,[string]$ExpectedSha,[int]$Version,$Policy) {
    $raw = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Path).Path)
    if ((Hash $raw) -cne $ExpectedSha -or [BitConverter]::ToInt32($raw,4) -ne $Version) {
        throw "Published predecessor bytes changed: $Path"
    }
    $restored = [Decennium.Foundation.Simulation]::new($Policy,$codec.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $state = $restored.Capture()
    if ($state.WireSchemaVersion -ne $Version -or $state.ExplorationSearch -or (Hash ($codec.Encode($state))) -cne $ExpectedSha) {
        throw "Authentic save did not restore byte-identically: $Path"
    }
    [ordered]@{path=$Path;wire=$Version;base=$state.SchemaVersion;sha256=$ExpectedSha;bytes=$raw.Length
        time=$state.RuleClock.ToString();revision=$state.Revision}
}

$legacyFixture = $tests.GetMethod('ObservationTraversalGapFixture',$flags).Invoke($null,@())
$terrain = [Decennium.Foundation.Laboratory.TacticalTerrainCell[]]@()
$oldCombat = [Decennium.Foundation.Laboratory.SharedCombatFixture]::new(26,1,26)
$old51 = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::new($oldCombat,30,$null,$terrain)
$null = $old51.EnableObservation($legacyFixture,[Decennium.Foundation.Laboratory.ObservationAlgorithmVersion]::LegacySampledV1)
$legacyPath = 'docs/unity/evidence/2026-11-06-observation/exact-partition-20261106/LEGACY_SCHEMA51_SAVE.bin'
$legacy = Restore-Old $legacyPath '648b91683a742bf03807b0d945a29563eba88a112e41ce0c75f2dbdbb4354a35' 51 $old51

$prior = 'docs/unity/evidence/2026-11-11-exp07-surprise-aware-entry'
$manifest = Get-Content -LiteralPath "$prior/BINDINGS.json" -Raw | ConvertFrom-Json -AsHashtable
$priorPath = 'focused/saves/exp07-surprise-restricted-slot.ddsave'
$old90 = $tests.GetMethod('SurprisePolicy',$flags).Invoke($null,@([Decennium.Foundation.SurpriseAwareness]::Surprised,$null))
$surprise = Restore-Old "$prior/$priorPath" $manifest.artifacts[$priorPath].sha256 90 $old90

[ordered]@{status='PASS';originalSchema51ConnectedTrace='All observed state and save bytes matched';assemblies=$assemblies
    authenticSaves=@($legacy,$surprise)} | ConvertTo-Json -Depth 10 |
    Set-Content -LiteralPath (Join-Path $OutputRoot 'results.json') -Encoding utf8
