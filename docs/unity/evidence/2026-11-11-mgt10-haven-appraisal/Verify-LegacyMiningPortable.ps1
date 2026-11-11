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
public static class AppraisalLegacyFixture
{
    public static uint Seed()
    {
        for(uint seed=1;seed<100000;seed++)
            if(PlaytestDice.RollD20(seed).Natural==12)return seed;
        throw new InvalidOperationException("No mining seed.");
    }
    private static void Apply(Simulation s,CommandKind kind,string actor,string target="",int x=0,int y=0,
        InventoryRequest inventory=null, MiningSelectionRequest mining=null)
    {
        var revision=s.Capture().Revision;
        var result=s.Execute(TestOnlySharedWorldPolicy.Host(),new Command("appraisal-legacy."+revision,actor,revision,kind,
            target,x,y,inventory,miningSelection:mining));
        if(result.Outcome!=Outcome.Committed)throw new InvalidOperationException(kind+" "+result.Code);
    }
    public static string Verify(string directory)
    {
        string worker=TestOnlyPolicy.CompanionId;
        var policy=new TestOnlySharedWorldPolicy(new PortableKitFixture(),new SharedCombatFixture(enemyHp:1,seed:Seed()),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture());
        string beforePath=Path.Combine(directory,"mining-portable-before.ddsave");
        string afterPath=Path.Combine(directory,"mining-portable-after.ddsave");
        var before=new FileSaveStore().Load(beforePath);
        var simulation=new Simulation(policy,before,ExecutionProfile.Laboratory);
        var codec=new SnapshotCodec();
        if(before.SchemaVersion!=43||before.HavenAppraisals.Length!=0
            ||!codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(beforePath)))
            throw new InvalidOperationException("Legacy mining/portable roundtrip changed.");
        Apply(simulation,CommandKind.AdvanceClock,TestOnlyPolicy.ActorId,x:900,y:1);
        var after=simulation.Capture();
        if(!codec.Encode(after).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Legacy mining/portable continuation changed.");
        var retrieval=new Command("legacy.portable-retrieval",worker,after.Revision,CommandKind.HandlePortableEquipment,
            SharedMiningFixture.UnitA,inventory:new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Retrieve));
        if(simulation.Execute(TestOnlySharedWorldPolicy.Host(),retrieval).Code!="InvalidResult"
            ||!codec.Encode(simulation.Capture()).SequenceEqual(File.ReadAllBytes(afterPath)))
            throw new InvalidOperationException("Schema43 inherited the new transport behavior.");
        var appraisal=new TestOnlySharedWorldPolicy(new PortableKitFixture(),new SharedCombatFixture(enemyHp:1,seed:Seed()),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture()).EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile());
        try { new Simulation(appraisal,before,ExecutionProfile.Laboratory); }
        catch (ArgumentException) { return before.ContentFingerprint; }
        throw new InvalidOperationException("The appraisal host admitted the old profile's save.");
    }
}
'@
$saves = Join-Path $PSScriptRoot 'legacy-saves'
$report = [ordered]@{
    status = 'PASS'
    schema = 43
    fingerprint = [AppraisalLegacyFixture]::Verify($saves)
    roundtrip = 'byte-identical'
    continuation = 'byte-identical'
    legacyRetrieval = 'InvalidResult; state byte-identical'
    wrongProfileRejected = $true
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    saveHashes = @(Get-ChildItem -LiteralPath $saves -Filter '*.ddsave' | Sort-Object Name | ForEach-Object {
        @{ name = $_.Name; sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output 'PASS: schema43 byte-identical legacy roundtrip and continuation, retained legacy retrieval behavior, and wrong-profile rejection.'
