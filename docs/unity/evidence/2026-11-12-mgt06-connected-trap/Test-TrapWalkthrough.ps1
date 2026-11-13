param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)

$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path $AssemblyRoot).Path
$Run = (New-Item -ItemType Directory -Force $Run).FullName
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
$authentic = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-12-exp05-local-mining/connected/travel-continued.ddsave')).Path
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require([bool]$ok, [string]$message) { if (-not $ok) { throw $message } }
function Digest([string]$path) { (Get-FileHash $path).Hash.ToLowerInvariant() }
$inputPath = Join-Path $Run 'walkthrough.jsonl'
python (Join-Path $PSScriptRoot 'New-TrapWalkthrough.py') $inputPath
if ($LASTEXITCODE -ne 0) { throw 'Unable to generate the selected input history.' }
$raw = Get-Content $inputPath
$inputs = @($raw | ForEach-Object { ConvertFrom-Json $_ })
function Run-Console([string]$folder, [string]$trace) {
    Push-Location $folder
    try { & $launcher -FishingTrap -AssemblyRoot $AssemblyRoot -InputPath $trace | Set-Content responses.jsonl -Encoding utf8 }
    finally { Pop-Location }
}
Run-Console $Run $inputPath
$rows = @(Get-Content "$Run/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
$store = [Decennium.Foundation.FileSaveStore]::new()
function Read-Save([string]$name) { $store.Load("$Run/$name.ddsave") }
$prefix = Read-Save 'travel-continued'
$reserved = Read-Save 'before-cancel'
$cancelled = Read-Save 'cancelled'
$pendingSetup = Read-Save 'pending-setup'
$exposed = Read-Save 'committed-setup'
$away = Read-Save 'away-pending'
$resolved = Read-Save 'away-resolved'
$overshoot = Read-Save 'away-overshoot'
$pending = Read-Save 'pending-retrieval'
$final = Read-Save 'trap-continued'
$companion = 'TEST_ONLY.companion'
$bait = 'TEST_ONLY.trap-ordinary-bait'
$trap = 'TEST_ONLY.fishing-trap'
$receiver = 'TEST_ONLY.riverbank.receiving-location'
$attempt = $resolved.FishingTrapAttempts | Where-Object OpportunityCommitted
$retrieval = $final.FishingTrapRetrievals[0]
Require ($rows.Count -eq $inputs.Count -and @($rows | Where-Object Response -eq 'Committed').Count -eq 242 -and
    @($rows | Where-Object {$_.Response -in 'StaleRevision','CommandIdConflict'}).Count -eq 0 -and $final.Revision -eq 242) 'The public trace did not complete at the expected revision.'
Require ($prefix.Revision -eq 223 -and $prefix.FishingTrapAttempts.Count -eq 0 -and
    ($prefix.Actors | Where-Object Id -eq $companion).X -eq 3 -and
    ($prefix.Actors | Where-Object Id -eq $companion).Y -eq 3 -and
    ($prefix.WorldActivityIntervals | Where-Object ActorId -eq $companion).Action -eq 'None') 'The real expedition prefix must leave the companion ready at the site.'
Require ($reserved.FishingOpportunities[0].Status -eq 'Reserved' -and $reserved.FishingTraps[0].Status -eq 'Reserved' -and
    $reserved.Work.AvailableAmount($bait).Numerator -eq 0 -and
    $cancelled.FishingTrapAttempts[0].SetupLabor.ToString() -eq '1/1' -and
    $cancelled.FishingOpportunities[0].Status -eq 'Available' -and $cancelled.FishingTraps[0].Status -eq 'Staged' -and
    $cancelled.Work.AvailableAmount($bait).Numerator -eq 1 -and $cancelled.RuleClock -eq $reserved.RuleClock) 'Cancellation must preserve paid time and release only reservations.'
Require ($pendingSetup.FishingTrapAttempts[1].SetupLabor.ToString() -eq '599/2' -and
    $exposed.FishingTrapAttempts[1].SetupLabor.ToString() -eq '300/1' -and $exposed.FishingTraps[0].Status -eq 'Deployed' -and
    $exposed.FishingOpportunities[0].Status -eq 'Spent' -and ($exposed.Work.Lots | Where-Object Id -eq $bait).Amount.Numerator -eq 0 -and
    $attempt.CheckDueAt -eq $attempt.StartedAt.AddSeconds(3300) -and $attempt.CheckResolvedAt -eq $attempt.CheckDueAt -and
    $away.FishingTrapAttempts[1].Status -eq 'Soaking' -and $attempt.WordsConsumed -gt 0 -and
    $attempt.RandomBefore -eq $away.RandomState -and $attempt.RandomAfter -eq $resolved.RandomState -and
    $resolved.RandomState -eq $overshoot.RandomState) 'Commit and due check must use real shared time and RNG exactly once.'
Require ($pending.FishingTrapRetrievals[0].WorkDone.ToString() -eq '599/2' -and
    $pending.FishingReceiveLocations[0].ReservedByRetrievalId -eq $retrieval.Id -and
    $retrieval.WorkDone.ToString() -eq '300/1' -and $retrieval.Status -eq 'Complete' -and
    $final.FishingReceiveLocations[0].ReservedByRetrievalId -eq '' -and
    $final.FishingTraps[0].Status -eq 'Retrieved' -and $final.FishingTraps[0].ReceivingLocationId -eq $receiver -and
    ($final.PortableEquipment | Where-Object Id -eq $trap).Placement -eq 'Ground' -and
    ($final.PortableEquipment | Where-Object Id -eq $trap).CustodianId -eq $companion -and
    $final.FishingOpportunities[0].Status -eq 'Spent') 'The receiver reservation must settle once after paid physical retrieval.'
if ($attempt.CheckOutcome -eq 'CapturedInTrap') {
    $creature = $final.FishingCreatures[0]
    Require ($creature.Id -eq $attempt.CapturedCreatureId -and $creature.LocationId -eq $receiver -and
        $creature.CustodianId -eq $companion -and $creature.ContainerId -eq '' -and
        @($final.InventoryLots | Where-Object LotId -eq $creature.Id).Count -eq 0) 'The existing captured body must move to the receiver without minting a lot.'
}
$direct = New-Item -ItemType Directory -Force "$Run/csharp"
$session = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()
$receipts = @{}
foreach ($receipt in $final.Receipts) { $receipts[$receipt.Revision] = $receipt }
$timings = @()
$checkpoints = @('pending-setup.ddsave','away-pending.ddsave','pending-retrieval.ddsave','trap-continued.ddsave')
for ($i=0; $i -lt $rows.Count; $i++) {
    $inputRow = $inputs[$i]
    $output = $rows[$i]
    if ($inputRow.op -eq 'view' -and $i -ge 277) {
        $view = $output.FishingTrap
        if ($inputRow.seat -eq 'FirstOpponent') { Require ($null -eq $view) 'Opposing seat leaked trap information.' }
        elseif (-not $view.ObservedLocally) {
            Require ($null -eq $view.CheckOutcome -and $null -eq $view.PhysicalStatus -and $null -eq $view.CapturedCreatureId -and
                @($output.Items | Where-Object {$_.Id -in $trap,$bait}).Count -eq 0) 'Remote projection leaked physical outcome.'
        }
    }
    if ($inputRow.id -in 'mgt06.repeat-set','mgt06.repeat-retrieval') {
        Require ($output.Response -eq 'Unavailable' -and $output.Revision -eq $inputRow.revision) 'The spent claim was accepted again.'
    }
    if ($output.Response -eq 'Committed') {
        $receipt = $receipts[$output.Revision]
        Require ($inputRow.op -eq 'auto' -or $receipt.Id -ceq $inputRow.id) 'The public trace does not match the canonical command.'
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $watch = [Diagnostics.Stopwatch]::StartNew()
        $result = switch ($inputRow.op) {
            'auto' { $session.AdvanceAutomaticDefender() }
            'submit' { $session.Submit(($inputRow.seat ?? 'Player'), $command) }
            'clock' { $session.SubmitSessionCommand($command) }
            'close' { $session.SubmitSessionCommand($command) }
            default { throw "Unrecognized committed input $($inputRow.op)." }
        }
        Require ($result.Response -eq 'Committed' -and $result.Revision -eq $output.Revision) "Public C# replay diverged at revision $($output.Revision)."
        if ($inputRow.id -like 'mgt06.*') {
            $null = $session.View('Player')
            $timings += [ordered]@{Id=$inputRow.id; Revision=$result.Revision; SubmitAndViewMs=$watch.Elapsed.TotalMilliseconds}
        }
    }
    if ($inputRow.op -eq 'save' -and $inputRow.path -in $checkpoints) { $session.Save((Join-Path $direct $inputRow.path)) }
}
$replay = New-Item -ItemType Directory -Force "$Run/replay"
$raw | Where-Object { (ConvertFrom-Json $_).op -ne 'load' } | Set-Content "$replay/walkthrough.jsonl" -Encoding utf8
Run-Console $replay "$replay/walkthrough.jsonl"
$hashes = [ordered]@{}
foreach ($name in $checkpoints) {
    $hashes[$name] = Digest "$Run/$name"
    Require ($hashes[$name] -ceq (Digest "$direct/$name") -and $hashes[$name] -ceq (Digest "$replay/$name")) "Canonical bytes differ for $name."
}
$default = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$default.Restore($authentic)
$default.Save("$Run/authentic-exp05.ddsave")
Require ((Digest $authentic) -ceq (Digest "$Run/authentic-exp05.ddsave")) 'The authentic default save changed.'
$rejections = [ordered]@{}
foreach ($case in @(
    @{Name='default-in-trap'; Session=$session; Path=$authentic; Revision=242},
    @{Name='trap-in-default'; Session=$default; Path="$Run/trap-continued.ddsave"; Revision=223})) {
    $failed = $false
    try { $case.Session.Restore($case.Path) } catch [ArgumentException] { $failed = $true }
    Require ($failed -and $case.Session.View('Player').Revision -eq $case.Revision) "Wrong-profile restore replaced live state: $($case.Name)"
    $rejections[$case.Name] = $true
}
$forged = $final.Copy()
$forged.RandomState = [uint32]($final.RandomState -bxor 1)
$store.Save("$Run/forged-history.ddsave",$forged)
$failed = $false
try { $session.Restore("$Run/forged-history.ddsave") } catch [ArgumentException] { $failed = $true }
Require ($failed -and $session.View('Player').Revision -eq 242) 'A structurally valid altered history replaced the live session.'
$rejections['forged-history'] = $true
$restoreTimes = [ordered]@{}
foreach ($name in $checkpoints) {
    $watch = [Diagnostics.Stopwatch]::StartNew()
    $session.Restore("$Run/$name")
    $restoreTimes[$name] = $watch.Elapsed.TotalMilliseconds
}
[ordered]@{
    Status='PASS'; Inputs=$inputs.Count; CSharpCommittedActions=$receipts.Count
    Fingerprint=$final.ContentFingerprint; BaseSchema=$final.SchemaVersion; Wire=$final.WireSchemaVersion
    FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()
    SetupStarted=$attempt.StartedAt.ToString(); Deployed=$attempt.SetupCompletedAt.ToString()
    CheckResolved=$attempt.CheckResolvedAt.ToString(); Outcome=$attempt.CheckOutcome.ToString()
    Natural=$attempt.Natural; Modifier=$attempt.CheckModifier; Words=$attempt.WordsConsumed
    CapturedCreature=$attempt.CapturedCreatureId; Receiver=$receiver; Retrieved=$retrieval.CompletedAt.ToString()
    PublicTimings=$timings; StrictRestoreMs=$restoreTimes; Checkpoints=$hashes; AuthenticDefaultSha256=(Digest $authentic)
    RestoreRejections=$rejections
} | ConvertTo-Json -Depth 8 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
