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
using System.Linq;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;

public static class AppraisalDeskRestrictionWitness
{
    private const string Worker = TestOnlyHavenAppraisalProfile.WorkerId;
    private const string Desk = TestOnlyHavenAppraisalProfile.DeskId;
    private const string Hero = TestOnlyPolicy.ActorId;
    private const string Unit = SharedMiningFixture.UnitA;

    private static Simulation New(CraftingMishapFact incident = null)
    {
        uint seed = 1;
        while (PlaytestDice.RollD20(seed).Natural != 12) seed++;
        var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
            new SupplyCacheFixture()).EnableMining(new SharedMiningFixture());
        if (incident != null) policy.EnableCraftingConsequences(new SharedCraftingFixture(events: new[] { incident }));
        policy.EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile(availableUntil: 12000));
        return new Simulation(policy, policy.Initial(), ExecutionProfile.Laboratory);
    }

    private static void Apply(Simulation s, CommandKind kind, string actor, string target = "", int x = 0, int y = 0,
        InventoryRequest inventory = null, MiningSelectionRequest mining = null)
    {
        long revision = s.Capture().Revision;
        var command = new Command("desk-restriction." + revision, actor, revision, kind, target, x, y, inventory, miningSelection: mining);
        var result = s.Execute(TestOnlySharedWorldPolicy.Host(), command);
        if (result.Outcome != Outcome.Committed) throw new InvalidOperationException(kind + " rejected: " + result.Code);
    }

    private static void Advance(Simulation s, int seconds) => Apply(s, CommandKind.AdvanceClock, Hero, x: seconds, y: 1);

    private static void Transport(Simulation s)
    {
        Apply(s, CommandKind.StartMining, Worker, SharedMiningFixture.DepositId,
            mining: new MiningSelectionRequest(SharedMiningFixture.DepositVersionId, new[] { SharedMiningFixture.CategoryA }));
        Advance(s, 1800);
        Apply(s, CommandKind.HandlePortableEquipment, Worker, Unit,
            inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Retrieve));
        Apply(s, CommandKind.BeginWorldStep, Worker, "walk", x: -1);
        Advance(s, 6);
        Apply(s, CommandKind.HandlePortableEquipment, Worker, Unit,
            inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Drop));
        Advance(s, 6);
    }

    public static string[] Trace()
    {
        var setup = New();
        Transport(setup);
        var eventAt = setup.Capture().RuleClock.AddSeconds(300);
        var incident = new CraftingMishapFact("desk-spill", 1, at: eventAt, stationId: Desk);
        var s = New(incident);
        Transport(s);
        Apply(s, CommandKind.StartHavenAppraisal, Worker, Desk);
        Advance(s, 300);
        Apply(s, CommandKind.DispatchCraftingMishap, Worker, incident.Id);
        var blocked = s.Capture();
        var afterEvent = blocked.HavenAppraisals.Single();
        if (!CraftingRestrictions.StationUseBlocked(blocked, Desk)) throw new InvalidOperationException("The authored desk restriction did not occur.");
        Advance(s, 1500);
        var after = s.Capture().HavenAppraisals.Single();
        return new[] { blocked.RuleClock.ToString(), afterEvent.Status.ToString(), afterEvent.Work.Labor.ToString(),
            after.Status.ToString(), after.Work.Labor.ToString(), after.ResultCopper?.ToString() ?? "" };
    }
}
'@
$trace = [AppraisalDeskRestrictionWitness]::Trace()
$report = [ordered]@{
    eventClock = $trace[0]
    stationUseBlocked = $true
    statusAfterEvent = $trace[1]
    laborAfterEvent = $trace[2]
    statusAfter1500MoreSeconds = $trace[3]
    laborAfter1500MoreSeconds = $trace[4]
    resultCopper = $trace[5]
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReportPath -Encoding utf8
$report | ConvertTo-Json -Depth 5
