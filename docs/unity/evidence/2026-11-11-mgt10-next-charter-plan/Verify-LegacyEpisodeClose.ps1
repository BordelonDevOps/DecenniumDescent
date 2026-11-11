param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ReportPath,
    [string]$CaptureFrom
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

public static class LegacyEpisodeCloseWitness
{
    private static void Apply(Simulation sim, CommandKind kind, string actor, string target = "", int x = 0, int y = 0)
    {
        long revision = sim.Capture().Revision;
        var result = sim.Execute(TestOnlySharedWorldPolicy.Host(),
            new Command("legacy-close." + revision, actor, revision, kind, target, x, y));
        if (result.Outcome != Outcome.Committed) throw new InvalidOperationException(kind + " rejected: " + result.Code);
    }

    public static string Run(string beforePath, string afterPath, bool capture)
    {
        uint seed = 1;
        while (PlaytestDice.RollD20(seed).Natural != 12) seed++;
        var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture()).EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile())
            .EnableHavenSale(new TestOnlyHavenSaleProfile()).EnableHavenMeal(new TestOnlyHavenMealProfile())
            .EnableExpeditionBill(new TestOnlyExpeditionBillProfile()).EnableExpeditionClose(new TestOnlyExpeditionCloseProfile());
        var store = new FileSaveStore();
        var codec = new SnapshotCodec();
        var before = store.Load(beforePath);
        var sim = new Simulation(policy, before, ExecutionProfile.Laboratory);
        var close = before.ExpeditionEpisodeClose;
        var companion = before.Actors.Single(x => x.Id == TestOnlyHavenMealProfile.CustomerId);
        if (before.SchemaVersion != 82 || close == null || close.MealIntakeIds.Count != 3
            || close.Outcome.PrimaryTargetMet || !close.Outcome.GrossTargetMet || close.Outcome.ProfitTargetMet != null
            || companion.X != 3 || companion.Y != 3 || !codec.Encode(sim.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Accepted schema 82 descendant-meal close did not roundtrip.");
        Apply(sim, CommandKind.BeginWorldStep, companion.Id, "walk", x: -1);
        Apply(sim, CommandKind.AdvanceClock, TestOnlyPolicy.ActorId, x: 6, y: 1);
        var after = sim.Capture();
        var retained = after.ExpeditionEpisodeClose;
        if (after.Actors.Single(x => x.Id == companion.Id).X != 2 || after.RuleClock != before.RuleClock.AddSeconds(6)
            || retained.CloseRevision != close.CloseRevision || retained.ClosedAt != close.ClosedAt
            || !retained.MealIntakeIds.SequenceEqual(close.MealIntakeIds) || after.HavenMealPurchases.Single().PaymentCopper != 2
            || after.ExpeditionBills.Single().Basis.NetExpeditionCopper != 2)
            throw new InvalidOperationException("Ordinary continuation changed the accepted historical close or its payment history.");
        if (capture) store.Save(afterPath, after);
        if (!codec.Encode(after).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Accepted schema 82 continuation changed.");
        return before.ContentFingerprint;
    }
}
'@
$saves = Join-Path $PSScriptRoot 'legacy-saves'
$before = Join-Path $saves 'episode-closed-before.ddsave'
$after = Join-Path $saves 'episode-closed-after.ddsave'
if ($CaptureFrom) {
    if ((Test-Path -LiteralPath $before) -or (Test-Path -LiteralPath $after)) {
        throw 'Authentic pre-change witnesses already exist.'
    }
    New-Item -ItemType Directory -Path $saves -Force | Out-Null
    Copy-Item -LiteralPath $CaptureFrom -Destination $before
}
$fingerprint = [LegacyEpisodeCloseWitness]::Run($before, $after, [bool]$CaptureFrom)
$report = [ordered]@{
    status = 'PASS'
    schema = 82
    fingerprint = $fingerprint
    roundtrip = 'byte-identical'
    continuation = 'byte-identical'
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    saveHashes = @($before, $after | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output 'PASS: schema 82 closed episode roundtrip and ordinary movement continuation are byte-identical.'
