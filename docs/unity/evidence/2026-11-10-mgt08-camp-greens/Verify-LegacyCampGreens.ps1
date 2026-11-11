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

public static class CampGreensLegacyWitness
{
    public static string Verify(string directory, bool assigned)
    {
        ICommandPolicy legacy = assigned
            ? (ICommandPolicy)new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableCampGreensAssignments()
            : new TestOnlyCropPolicy();
        ICommandPolicy firstWork = assigned
            ? (ICommandPolicy)new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableCampGreensAssignments()
                .EnableCampGreensFirstWorkTending()
            : new TestOnlyCropPolicy(firstWorkTending: true);
        var authority = assigned ? TestOnlySharedWorldPolicy.Host() : TestOnlyCropPolicy.Host();
        string prefix = assigned ? "schema39-assigned" : "schema3-direct";
        var beforePath = Path.Combine(directory, prefix + "-before.ddsave");
        var afterPath = Path.Combine(directory, prefix + "-after.ddsave");
        var before = new FileSaveStore().Load(beforePath);
        var simulation = new Simulation(legacy, before, ExecutionProfile.Laboratory);
        var codec = new SnapshotCodec();
        if (!codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Legacy roundtrip changed: " + prefix);
        bool rejected = false;
        try { new Simulation(firstWork, before, ExecutionProfile.Laboratory); }
        catch (ArgumentException) { rejected = true; }
        if (!rejected) throw new InvalidOperationException("Wrong profile loaded: " + prefix);
        var command = new Command("golden." + before.Revision, TestOnlyPolicy.ActorId,
            before.Revision, CommandKind.AdvanceClock, x: 900, y: 1);
        if (simulation.Execute(authority, command).Outcome != Outcome.Committed
            || !codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Legacy continuation changed: " + prefix);
        return before.ContentFingerprint;
    }
}
'@

$saves = Join-Path $PSScriptRoot 'legacy-saves'
$report = [ordered]@{
    status = 'PASS'
    cases = @(
        @{ schema = 3; fingerprint = [CampGreensLegacyWitness]::Verify($saves, $false) },
        @{ schema = 39; fingerprint = [CampGreensLegacyWitness]::Verify($saves, $true) }
    )
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    saveHashes = @(Get-ChildItem -LiteralPath $saves -Filter '*.ddsave' | Sort-Object Name | ForEach-Object {
        @{ name = $_.Name; sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output "PASS: legacy schema 3 and 39 roundtrip, continuation, and wrong-profile rejection."
