param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ReportPath,
    [Parameter(Mandatory)][string]$SavePath,
    [switch]$ExpectClose
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core', 'Persistence', 'LabModel', 'HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$references = @(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
$assemblies | ForEach-Object { Add-Type -Path $_ }
Add-Type -Language CSharp -ReferencedAssemblies ($references + $assemblies) -TypeDefinition @'
using System;
using System.Linq;
using System.Reflection;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
using Decennium.Foundation.Tests;

public static class InterruptedMealCloseWitness
{
    private const string Customer = TestOnlyHavenMealProfile.CustomerId;
    private const string Meal = TestOnlyHavenMealProfile.MealLotId;
    private const string Hero = TestOnlyPolicy.ActorId;

    private static T Prepare<T>(string method, params object[] arguments)
        => (T)typeof(FoundationCases).GetMethod(method, BindingFlags.NonPublic | BindingFlags.Static).Invoke(null, arguments);

    private static void Apply(Simulation sim, Authority host, CommandKind kind, string actor, string target = "", int x = 0, int y = 0,
        InventoryRequest inventory = null)
    {
        var revision = sim.Capture().Revision;
        var result = sim.Execute(host, new Command("meal-close-baseline." + revision, actor, revision, kind, target, x, y, inventory));
        if (result.Outcome != Outcome.Committed) throw new InvalidOperationException(kind + " rejected: " + result.Code);
    }

    public static string[] Run(string savePath, bool expectClose)
    {
        var policy = Prepare<TestOnlySharedWorldPolicy>("ClosePolicy", new object[] { null, null });
        var host = Prepare<Authority>("HavenSaleHost");
        var sim = Prepare<Simulation>("MealAtCounter", policy, true);
        Apply(sim, host, CommandKind.PurchaseHavenMeal, Customer, TestOnlyHavenMealProfile.OfferVersionId);
        Apply(sim, host, CommandKind.StartIntake, Customer, Meal, inventory: new InventoryRequest(new RuleQuantity(2, 3)));
        Apply(sim, host, CommandKind.AdvanceClock, Hero, x: 150, y: 1);
        string first = sim.Capture().Intakes.Single().Id;
        Apply(sim, host, CommandKind.InterruptIntake, Customer, first);
        Apply(sim, host, CommandKind.AdvanceClock, Hero, x: 6, y: 1);
        Apply(sim, host, CommandKind.StartIntake, Customer, Meal, inventory: new InventoryRequest(new RuleQuantity(1, 2)));
        Apply(sim, host, CommandKind.AdvanceClock, Hero, x: 450, y: 1);
        Apply(sim, host, CommandKind.AdvanceClock, Hero, x: 6, y: 1);
        Apply(sim, host, CommandKind.StartExpeditionBill, Customer, TestOnlyExpeditionBillProfile.BillVersionId);
        Apply(sim, host, CommandKind.AdvanceClock, Hero, x: 1800, y: 1);

        var state = sim.Capture();
        var intakes = state.Intakes.OrderBy(x => x.StartedAt).ToArray();
        var amounts = intakes.Select(x => state.Work.Reservations.Single(r => r.Id == x.ReservationId)).ToArray();
        if (state.SchemaVersion != 82 || state.ExpeditionBills.Single().Status != ExpeditionBillStatus.Reconciled
            || intakes.Length != 2 || intakes[0].Status != IntakeStatus.Interrupted || intakes[1].Status != IntakeStatus.Complete
            || amounts[0].ConsumedAmount != new RuleQuantity(1, 6) || amounts[1].ConsumedAmount != new RuleQuantity(1, 2)
            || amounts.Any(x => x.RemainingAmount != default) || state.Work.Lots.Single(x => x.Id == Meal).Amount != default)
            throw new InvalidOperationException("The exact fully consumed, terminal meal history was not reproduced.");
        var command = new Command("meal-close-baseline.final", Hero, state.Revision,
            CommandKind.CloseExpeditionEpisode, TestOnlyExpeditionBillProfile.EpisodeId);
        var query = sim.QueryCommand(host, command);
        var outcome = sim.Execute(host, command);
        if (expectClose) {
            if (!query.Admissible || outcome.Outcome != Outcome.Committed || sim.Capture().ExpeditionEpisodeClose == null)
                throw new InvalidOperationException("Corrected close did not admit the intact consumed meal history.");
        } else if (query.Admissible || query.Code != "ExpeditionCloseMealIntakeRequired" || outcome.Outcome != Outcome.Rejected
            || outcome.Code != query.Code || sim.Capture().Revision != state.Revision)
            throw new InvalidOperationException("The specific pre-fix close rejection was not reproduced.");
        new FileSaveStore().Save(savePath, sim.Capture());
        return new[] { state.RuleClock.ToString(), state.Revision.ToString(), first, intakes[1].Id,
            amounts[0].ConsumedAmount.ToString(), amounts[1].ConsumedAmount.ToString(), query.Code, outcome.Outcome.ToString(), outcome.Code };
    }
}
'@
$facts = [InterruptedMealCloseWitness]::Run($SavePath, [bool]$ExpectClose)
[ordered]@{
    status = 'PASS'
    witness = $(if ($ExpectClose) { 'corrected-closure' } else { 'pre-fix-failure-reproduced' })
    beforeCloseTime = $facts[0]
    beforeCloseRevision = [long]$facts[1]
    interruptedIntake = $facts[2]
    completedIntake = $facts[3]
    firstConsumedLb = $facts[4]
    secondConsumedLb = $facts[5]
    query = $facts[6]
    outcome = $facts[7]
    code = $facts[8]
    saveSha256 = (Get-FileHash -LiteralPath $SavePath).Hash.ToLowerInvariant()
    assemblyHashes = @($assemblies | ForEach-Object {
        @{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant() }
    })
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $ReportPath -Encoding utf8
Write-Output ("PASS: terminal portions " + $facts[4] + " + " + $facts[5] + "; query " + $facts[6] + "; command " + $facts[7] + " " + $facts[8])
