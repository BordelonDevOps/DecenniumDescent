param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core', 'Persistence', 'LabModel' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$references = @(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
$assemblies | ForEach-Object { Add-Type -Path $_ }
Add-Type -Language CSharp -ReferencedAssemblies ($references + $assemblies) -TypeDefinition @'
using System;
using System.IO;
using System.Linq;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;

public static class LegacyResearchWitness
{
    public static string Verify(string directory, bool structureHost)
    {
        var combat = new SharedCombatFixture(seed: 1);
        var research = new SharedResearchFixture();
        var legacy = structureHost
            ? new TestOnlySharedWorldPolicy(combat, research, new SharedCraftingFixture(), new SharedRepairFixture())
            : new TestOnlySharedWorldPolicy(combat, research);
        string key = structureHost ? "schema17-research" : "schema15-research";
        string beforePath = Path.Combine(directory, key + "-before.ddsave");
        string afterPath = Path.Combine(directory, key + "-after.ddsave");
        var before = new FileSaveStore().Load(beforePath);
        var simulation = new Simulation(legacy, before, ExecutionProfile.Laboratory);
        var codec = new SnapshotCodec();
        if (!codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Legacy roundtrip changed: " + key);
        if (structureHost) {
            var station = new TestOnlySharedWorldPolicy(combat, research, new SharedCraftingFixture(), new SharedRepairFixture())
                .EnableResearchStation(new TestOnlyResearchStationProfile());
            bool rejected = false;
            try { new Simulation(station, before, ExecutionProfile.Laboratory); }
            catch (ArgumentException) { rejected = true; }
            if (!rejected) throw new InvalidOperationException("Station profile loaded the ordinary save.");
        }
        var command = new Command("research-golden." + before.Revision, TestOnlyPolicy.ActorId,
            before.Revision, CommandKind.AdvanceClock, x: 14400, y: 1);
        if (simulation.Execute(TestOnlySharedWorldPolicy.Host(), command).Outcome != Outcome.Committed
            || !codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Legacy continuation changed: " + key);
        return before.ContentFingerprint;
    }
}
'@

$saves = Join-Path $PSScriptRoot 'legacy-saves'
$report = [ordered]@{
    status = 'PASS'
    cases = @(
        @{ schema = 15; fingerprint = [LegacyResearchWitness]::Verify($saves, $false) },
        @{ schema = 17; fingerprint = [LegacyResearchWitness]::Verify($saves, $true); wrongProfileRejected = $true }
    )
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    saveHashes = @(Get-ChildItem -LiteralPath $saves -Filter '*.ddsave' | Sort-Object Name | ForEach-Object {
        @{ name = $_.Name; sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output 'PASS: legacy schema 15 and 17 roundtrip and continuation, and schema 17 wrong-profile rejection.'
