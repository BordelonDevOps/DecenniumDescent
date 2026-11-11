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

public static class LegacySaleWitness
{
    private const string Seller = TestOnlyHavenSaleProfile.SellerId;
    private const string Buyer = TestOnlyHavenSaleProfile.BuyerId;
    private const string Hero = TestOnlyPolicy.ActorId;
    private const string Tender = TestOnlyHavenSaleProfile.TenderLotId;

    private static void Apply(Simulation s, CommandKind kind, string actor, string target = "", int x = 0, int y = 0,
        InventoryRequest inventory = null)
    {
        long revision = s.Capture().Revision;
        var command = new Command("legacy-sale." + revision, actor, revision, kind, target, x, y, inventory);
        var result = s.Execute(TestOnlySharedWorldPolicy.Host(), command);
        if (result.Outcome != Outcome.Committed) throw new InvalidOperationException(kind + " rejected: " + result.Code);
    }

    public static string Run(string beforePath, string afterPath, bool capture)
    {
        uint seed = 1;
        while (PlaytestDice.RollD20(seed).Natural != 12) seed++;
        var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture()).EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile())
            .EnableHavenSale(new TestOnlyHavenSaleProfile());
        var store = new FileSaveStore();
        var codec = new SnapshotCodec();
        var before = store.Load(beforePath);
        var s = new Simulation(policy, before, ExecutionProfile.Laboratory);
        if (before.SchemaVersion != 79 || before.HavenSales.Single().PaymentCopper != 2
            || !codec.Encode(s.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Accepted schema 79 paid sale did not roundtrip.");
        Apply(s, CommandKind.AdvanceClock, Hero, x: 6, y: 1);
        Apply(s, CommandKind.HandlePortableEquipment, Seller, Tender,
            inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Drop));
        Apply(s, CommandKind.BeginWorldStep, Seller, "walk", x: 1);
        Apply(s, CommandKind.AdvanceClock, Hero, x: 2, y: 1);
        var after = s.Capture();
        if (after.HavenSales.Single().PaymentCopper != 2 || after.HavenAppraisals.Single().ResultCopper != new RuleQuantity(15, 2)
            || after.PortableEquipment.Single(x => x.Id == Tender).Placement != PortablePlacement.Ground
            || after.InventoryLots.Single(x => x.LotId == Tender).OwnerId != Seller
            || after.InventoryLots.Single(x => x.LotId == SharedMiningFixture.UnitA).OwnerId != Buyer)
            throw new InvalidOperationException("Paid history or normal tender handling changed.");
        if (capture) store.Save(afterPath, after);
        if (!codec.Encode(after).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Accepted schema 79 continuation changed.");
        return before.ContentFingerprint;
    }
}
'@
$saves = Join-Path $PSScriptRoot 'legacy-saves'
$before = Join-Path $saves 'paid-sale-before.ddsave'
$after = Join-Path $saves 'paid-sale-after.ddsave'
if ($CaptureFrom) {
    if ((Test-Path -LiteralPath $before) -or (Test-Path -LiteralPath $after)) {
        throw 'Authentic pre-change witnesses already exist.'
    }
    New-Item -ItemType Directory -Path $saves -Force | Out-Null
    Copy-Item -LiteralPath $CaptureFrom -Destination $before
}
$fingerprint = [LegacySaleWitness]::Run($before, $after, [bool]$CaptureFrom)
$report = [ordered]@{
    status = 'PASS'
    schema = 79
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
Write-Output 'PASS: schema 79 paid sale roundtrip and normal continuation are byte-identical.'
