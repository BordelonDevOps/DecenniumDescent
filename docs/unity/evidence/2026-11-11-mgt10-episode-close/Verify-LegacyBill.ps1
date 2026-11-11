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

public static class LegacyBillWitness
{
    private static void Apply(Simulation sim, CommandKind kind, string actor, string target = "", int x = 0, int y = 0)
    {
        long revision = sim.Capture().Revision;
        var result = sim.Execute(TestOnlySharedWorldPolicy.Host(),
            new Command("legacy-bill." + revision, actor, revision, kind, target, x, y));
        if (result.Outcome != Outcome.Committed) throw new InvalidOperationException(kind + " rejected: " + result.Code);
    }

    public static string Run(string beforePath, string afterPath, bool capture)
    {
        uint seed = 1;
        while (PlaytestDice.RollD20(seed).Natural != 12) seed++;
        var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture()).EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile())
            .EnableHavenSale(new TestOnlyHavenSaleProfile()).EnableHavenMeal(new TestOnlyHavenMealProfile())
            .EnableExpeditionBill(new TestOnlyExpeditionBillProfile());
        var store = new FileSaveStore();
        var codec = new SnapshotCodec();
        var before = store.Load(beforePath);
        var sim = new Simulation(policy, before, ExecutionProfile.Laboratory);
        var bill = before.ExpeditionBills.Single();
        var worker = before.Actors.Single(x => x.Id == bill.WorkerId);
        if (before.SchemaVersion != 81 || bill.Status != ExpeditionBillStatus.Reconciled || bill.Basis.NetExpeditionCopper != 2
            || bill.Report.OwnerId != TestOnlyHavenMealProfile.VendorId || bill.Report.PhysicalCount != new RuleQuantity(2)
            || worker.X != 3 || worker.Y != 3 || !codec.Encode(sim.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Accepted schema 81 bill did not roundtrip with its actual movement and tender.");
        Apply(sim, CommandKind.BeginWorldStep, worker.Id, "walk", x: -1);
        Apply(sim, CommandKind.AdvanceClock, TestOnlyPolicy.ActorId, x: 6, y: 1);
        var after = sim.Capture();
        var retained = after.ExpeditionBills.Single();
        if (after.Actors.Single(x => x.Id == worker.Id).X != 2 || after.RuleClock != before.RuleClock.AddSeconds(6)
            || retained.UpdatedRevision != bill.UpdatedRevision || retained.UpdatedAt != bill.UpdatedAt
            || retained.Report.OwnerId != bill.Report.OwnerId || retained.Report.PhysicalCount != bill.Report.PhysicalCount
            || after.HavenSales.Single().PaymentCopper != 2 || after.HavenMealPurchases.Single().PaymentCopper != 2)
            throw new InvalidOperationException("Ordinary continuation changed completed bill or receipt history.");
        if (capture) store.Save(afterPath, after);
        if (!codec.Encode(after).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Accepted schema 81 continuation changed.");
        return before.ContentFingerprint;
    }
}
'@
$saves = Join-Path $PSScriptRoot 'legacy-saves'
$before = Join-Path $saves 'reconciled-bill-before.ddsave'
$after = Join-Path $saves 'reconciled-bill-after.ddsave'
if ($CaptureFrom) {
    if ((Test-Path -LiteralPath $before) -or (Test-Path -LiteralPath $after)) {
        throw 'Authentic pre-change witnesses already exist.'
    }
    New-Item -ItemType Directory -Path $saves -Force | Out-Null
    Copy-Item -LiteralPath $CaptureFrom -Destination $before
}
$fingerprint = [LegacyBillWitness]::Run($before, $after, [bool]$CaptureFrom)
$report = [ordered]@{
    status = 'PASS'
    schema = 81
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
Write-Output 'PASS: schema 81 reconciled bill roundtrip and ordinary movement continuation are byte-identical.'
