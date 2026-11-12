param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ResultsRoot
)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
New-Item -ItemType Directory -Path $ResultsRoot | Out-Null
$ResultsRoot = (Resolve-Path -LiteralPath $ResultsRoot).Path
$csharp = Join-Path $ResultsRoot 'csharp'
$console = Join-Path $ResultsRoot 'console'
New-Item -ItemType Directory -Path $csharp,$console | Out-Null
$accepted = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-12-int03-connected-session/correction')).Path
$acceptedFinal = Join-Path $accepted 'connected/saves/checkpoint-165.ddsave'
$acceptedInitial = Join-Path $accepted 'connected/saves/initial.ddsave'
$store = [Decennium.Foundation.FileSaveStore]::new()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$hero = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$director = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::FirstOpponent
$cacheId = 'TEST_ONLY.supply-cache'
$rootId = 'TEST_ONLY.ready-rations'
$toolId = 'TEST_ONLY.thieves-tools'
$timer = [Diagnostics.Stopwatch]::new()
$commands = [Collections.Generic.List[object]]::new()
$events = [Collections.Generic.List[object]]::new()
$consoleInput = [Collections.Generic.List[string]]::new()
$fileTimings = [Collections.Generic.List[object]]::new()
$session = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()

function Assert-Cache([bool]$condition, [string]$message) {
    if (-not $condition) { throw $message }
}
function Hash-CacheFile([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Add-ConsoleInput($row) {
    $consoleInput.Add((ConvertTo-Json -InputObject $row -Depth 6 -Compress))
}
function Run-AcceptedInputs($run) {
    foreach ($receipt in $store.Load($acceptedFinal).Receipts) {
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $result = switch ($receipt.Principal) {
            'TEST_ONLY.tac10-later-defender.v1' { $run.AdvanceAutomaticDefender() }
            'TEST_ONLY.session-operator' { $run.SubmitSessionCommand($command) }
            'TEST_ONLY.session-first-opponent' { $run.Submit('FirstOpponent', $command) }
            default { $run.Submit('Player', $command) }
        }
        Assert-Cache ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) (
            "Accepted route input $($receipt.Revision) $($command.Kind) did not commit.")
        if ($receipt.Revision -eq 5) {
            $view = $run.View('Player')
            $try = [Decennium.Foundation.Command]::new('cache.tactical.denied', $hero, $view.Revision, 'Interact', $cacheId, 2)
            Assert-Cache ($view.InEncounter -and $null -eq $view.Cache -and $run.Submit('Player', $try).Response -eq 'Unavailable') (
                'Cache commands and projection must remain outside tactical play.')
        }
    }
}
function Show-Cache {
    Add-ConsoleInput @{op='view'; seat='Player'}
    $session.View('Player')
}
function Invoke-Recorded($run, $entry) {
    if ($entry.Op -eq 'clock') { $run.SubmitSessionCommand($entry.Command) }
    else { $run.Submit('Player', $entry.Command) }
}
function Send-CacheInput([string]$label, $command, [string]$expected = 'Committed') {
    $op = if ($command.Kind -eq 'AdvanceClock') {'clock'} else {'submit'}
    $entry = [pscustomobject]@{Command=$command; Op=$op; Expected=$expected}
    $commands.Add($entry)
    $row = [ordered]@{op=$op; id=$command.Id; revision=$command.ExpectedRevision; x=$command.X; y=$command.Y}
    if ($op -eq 'submit') {
        $row.actor=$command.Actor
        $row.kind=$command.Kind.ToString()
        $row.target=$command.Target
    }
    if ($command.Inventory) {
        $row.inventory=@{numerator=$command.Inventory.Amount.Numerator; denominator=$command.Inventory.Amount.Denominator;
            handling=$command.Inventory.Handling.ToString()}
    }
    Add-ConsoleInput $row
    $timer.Restart()
    $result = Invoke-Recorded $session $entry
    $view = $session.View('Player')
    $elapsed = $timer.Elapsed.TotalMilliseconds
    Assert-Cache ($result.Response -eq $expected -and $result.Revision -eq $view.Revision -and $result.Clock -eq $view.Clock) (
        "$label at revision $($view.Revision) expected $expected, got $($result.Response).")
    $events.Add([pscustomobject]@{Label=$label; Revision=$view.Revision; Clock=$view.Clock.ToString();
        Response=$result.Response.ToString(); Ms=[math]::Round($elapsed,3); CacheVisible=$null -ne $view.Cache;
        Locked=$view.Cache.Locked; Open=$view.Cache.Open; PickAttempt=$view.Cache.PickAttemptId; Stock=$view.Cache.StockId;
        Available=$view.Cache.AvailablePounds})
}
function Request-Cache([string]$id, $kind, [string]$target = '', [int]$x = 0, [int]$y = 0, $inventory = $null) {
    [Decennium.Foundation.Command]::new("exp03.$id", $hero, $session.View('Player').Revision, $kind, $target, $x, $y, $inventory)
}
function Walk-Cache([string]$name,[int]$direction) {
    Send-CacheInput "$name starts" (Request-Cache "$name.step" BeginWorldStep walk $direction 0)
    $travelling = Show-Cache
    Assert-Cache ($null -eq $travelling.Cache) 'Cache view must stay hidden while traversing.'
    Send-CacheInput "$name paid" (Request-Cache "$name.time" AdvanceClock '' 2 1)
}
function Save-CacheFile([string]$name) {
    Add-ConsoleInput @{op='save'; path=$name}
    $timer.Restart()
    $session.Save((Join-Path $csharp $name))
    $fileTimings.Add([pscustomobject]@{Operation='Save'; File=$name; Ms=$timer.Elapsed.TotalMilliseconds})
}
function Restore-CacheFile([string]$name) {
    Add-ConsoleInput @{op='load'; path=$name}
    $timer.Restart()
    $session.Restore((Join-Path $csharp $name))
    $fileTimings.Add([pscustomobject]@{Operation='Full restore'; File=$name; Ms=$timer.Elapsed.TotalMilliseconds})
}

$session.Save((Join-Path $csharp 'initial.ddsave'))
Assert-Cache ((Hash-CacheFile (Join-Path $csharp 'initial.ddsave')) -ceq (Hash-CacheFile $acceptedInitial)) (
    'The profile must preserve the exact accepted starting save.')
$initial = $session.View('Player')
Assert-Cache ($null -eq $initial.Cache -and $rootId -notin $initial.Items.Id) 'Locked stock must not appear remotely.'
Run-AcceptedInputs $session
$session.Save((Join-Path $csharp 'baseline-165.ddsave'))
Assert-Cache ((Hash-CacheFile (Join-Path $csharp 'baseline-165.ddsave')) -ceq (Hash-CacheFile $acceptedFinal)) (
    'The unchanged public route must reach the accepted canonical revision 165.')
$prior = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$prior.Restore($acceptedFinal)
$priorFile = Join-Path $csharp 'authentic-165.ddsave'
$prior.Save($priorFile)
Assert-Cache ((Hash-CacheFile $priorFile) -ceq (Hash-CacheFile $acceptedFinal) -and
    $prior.View('Player').Cache.Locked -and $prior.View('Player').Cache.StockId -eq '') (
    'An authentic wire95 predecessor must restore byte-identically with the corrected projection.')
foreach ($line in [IO.File]::ReadLines((Join-Path $accepted 'walkthrough.jsonl'))) { $consoleInput.Add($line) }

Walk-Cache before-approach 1
Assert-Cache ($null -eq (Show-Cache).Cache) 'Remote chest is unavailable.'
Walk-Cache approach -1
$closed = Show-Cache
Assert-Cache ($closed.Cache.Id -eq $cacheId -and $closed.Cache.Locked -and -not $closed.Cache.Open -and
    $closed.Cache.StockId -eq '' -and $rootId -notin $closed.Items.Id) 'Closed chest discloses its shell and hides its stock.'
$take = [Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(2))
Send-CacheInput 'closed stock guess' (Request-Cache closed-pickup HandleInventory $rootId -inventory $take) 'Unavailable'
Send-CacheInput 'unknown stock guess' (Request-Cache unknown-pickup HandleInventory 'unknown' -inventory $take) 'Unavailable'
$tools = $closed.Items | Where-Object Id -eq $toolId
$retrieve = [Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'','Retrieve')
Send-CacheInput 'retrieve actual tools' (Request-Cache tools HandlePortableEquipment $tools.Id -inventory $retrieve)
Save-CacheFile 'before-pick.ddsave'
Send-CacheInput 'start first pick' (Request-Cache pick-a Interact $closed.Cache.Id 2)
Send-CacheInput 'pay first two seconds' (Request-Cache pick-a-part AdvanceClock '' 2 1)
$working = Show-Cache
Assert-Cache ($working.Cache.Locked -and $working.Cache.PickAttemptId -ne '' -and
    $working.Cache.PickDueAt -eq $working.Clock.AddSeconds(4)) 'First pick must have four active seconds remaining.'
Save-CacheFile 'pick-pending.ddsave'
Restore-CacheFile 'pick-pending.ddsave'
$restored = Show-Cache
Assert-Cache ($restored.Cache.PickAttemptId -eq $working.Cache.PickAttemptId -and
    $restored.Cache.PickDueAt -eq $working.Cache.PickDueAt) 'Restore must preserve the same real pending attempt.'
Send-CacheInput 'finish first pick' (Request-Cache pick-a-finish AdvanceClock '' 4 1)
$failed = Show-Cache
Assert-Cache ($failed.Cache.Locked -and $failed.Cache.PickAttemptId -eq '') 'The first paid attempt must genuinely fail.'
Send-CacheInput 'start second pick' (Request-Cache pick-b Interact $failed.Cache.Id 2)
Send-CacheInput 'finish second pick' (Request-Cache pick-b-time AdvanceClock '' 6 1)
$unlocked = Show-Cache
Assert-Cache (-not $unlocked.Cache.Locked -and -not $unlocked.Cache.Open -and $unlocked.Cache.StockId -eq '') (
    'Successful unlocking must keep the separate opening and stock boundary.')
Send-CacheInput 'open separately' (Request-Cache open Interact $unlocked.Cache.Id 3)
$open = Show-Cache
Assert-Cache ($open.Cache.Open -and $open.Cache.StockId -eq $rootId -and $open.Cache.AvailablePounds.Numerator -eq 2 -and
    $open.Cache.AvailablePounds.Denominator -eq 1 -and $rootId -notin $open.Items.Id) 'Only the open cache view publishes its finite stock.'
Send-CacheInput 'deny portion in chest' (Request-Cache portion PortionInventory $open.Cache.StockId -inventory $take) 'Unavailable'
$pickup = Request-Cache pickup HandleInventory $open.Cache.StockId -inventory $take
Send-CacheInput 'pick up complete stock' $pickup
Walk-Cache departure 1
Save-CacheFile 'depleted-away.ddsave'
Restore-CacheFile 'depleted-away.ddsave'
Send-CacheInput 'retry completed pickup out of reach' $pickup 'Duplicate'
Walk-Cache revisit -1
$empty = Show-Cache
Assert-Cache ($empty.Cache.Id -eq $closed.Cache.Id -and $empty.Cache.Open -and -not $empty.Cache.Locked -and
    $empty.Cache.StockId -eq '' -and $null -eq $empty.Cache.AvailablePounds -and $rootId -notin $empty.Items.Id) (
    'Revisit must retain the same open chest with no stock token or amount.')
Send-CacheInput 'fresh reopening' (Request-Cache reopen Interact $empty.Cache.Id 3) 'Unavailable'
Send-CacheInput 'fresh repeat pickup' (Request-Cache retake HandleInventory $open.Cache.StockId -inventory $take) 'Unavailable'
Walk-Cache continue 1
Save-CacheFile 'continued.ddsave'

$replayed = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
Run-AcceptedInputs $replayed
foreach ($entry in $commands) {
    $result = Invoke-Recorded $replayed $entry
    Assert-Cache ($result.Response -eq $entry.Expected) 'The uninterrupted exact inputs must preserve all outcomes.'
}
$replayFile = Join-Path $csharp 'uninterrupted.ddsave'
$replayed.Save($replayFile)
$finalFile = Join-Path $csharp 'continued.ddsave'
$finalSha = Hash-CacheFile $finalFile
Assert-Cache ((Hash-CacheFile $replayFile) -ceq $finalSha) 'The restored and uninterrupted continuations must match exactly.'

$before = $store.Load((Join-Path $csharp 'before-pick.ddsave'))
$pending = $store.Load((Join-Path $csharp 'pick-pending.ddsave'))
$final = $store.Load($finalFile)
$child = $final.InventoryLots | Where-Object ParentId -eq $rootId
$lot = $final.Work.Lots | Where-Object Id -eq $child.LotId
$root = $final.Work.Lots | Where-Object Id -eq $rootId
$reserve = $final.Vessels | Where-Object Id -eq 'TEST_ONLY.actor-skin'
Assert-Cache ($before.RandomState -eq $pending.RandomState -and $pending.SupplyCacheAttempts[0].Natural -eq 0 -and
    $pending.SupplyCacheAttempts[0].Status -eq 'Working' -and $final.SupplyCacheAttempts.Count -eq 2 -and
    $final.SupplyCacheAttempts[0].Status -eq 'Failed' -and $final.SupplyCacheAttempts[1].Status -eq 'Succeeded' -and
    @($child).Count -eq 1 -and $child.OwnerId -eq $hero -and $child.CreatedAmount.ToString() -eq '2/1' -and
    $lot.LocationId -eq $hero -and $lot.CustodianId -eq $hero -and $lot.Amount.ToString() -eq '2/1' -and
    $root.LocationId -eq $cacheId -and $root.Amount.ToString() -eq '0/1' -and $reserve.LocationId -eq $hero -and
    $final.WireSchemaVersion -eq 95 -and $final.ContentFingerprint -eq $before.ContentFingerprint) (
    'Paid attempts, finite carried provenance, carried reserve and the selected wire95 profile must agree.')
foreach ($attempt in $final.SupplyCacheAttempts) {
    Assert-Cache ($attempt.EndedAt -eq $attempt.StartedAt.AddSeconds(6)) 'Both complete attempts must pay six actual seconds.'
}
$forged = $store.Load($finalFile)
$forged.SupplyCaches[0] = $forged.SupplyCaches[0].With($null,$false)
$forgedFile = Join-Path $csharp 'forged-cache.ddsave'
[IO.File]::WriteAllBytes($forgedFile,$codec.Encode($forged))
Assert-Cache (-not $store.Load($forgedFile).SupplyCaches[0].Open) 'The false chest state must decode before strict replay rejects it.'
$rejected = $false
try { $session.Restore($forgedFile) } catch { $rejected = $true }
$afterRejection = Join-Path $csharp 'after-forgery-rejection.ddsave'
$session.Save($afterRejection)
Assert-Cache ($rejected -and (Hash-CacheFile $afterRejection) -ceq $finalSha) 'Forged cache history must not replace the live session.'

$walkthrough = Join-Path $ResultsRoot 'walkthrough.jsonl'
$consoleInput | Set-Content -LiteralPath $walkthrough -Encoding utf8
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
Push-Location -LiteralPath $console
try {
    & $launcher -AssemblyRoot $AssemblyRoot -InputPath $walkthrough |
        Set-Content -LiteralPath (Join-Path $console 'responses.jsonl') -Encoding utf8
} finally { Pop-Location }
$rows = @(Get-Content -LiteralPath (Join-Path $console 'responses.jsonl') | ForEach-Object { ConvertFrom-Json $_ })
$newResponses = @($rows | Select-Object -Skip 170 | Where-Object { $_.Response -in 'Committed','Unavailable','Duplicate' })
Assert-Cache ($rows.Count -eq $consoleInput.Count -and $newResponses.Count -eq $commands.Count) 'The console must answer every exact input.'
for ($i=0; $i -lt $commands.Count; $i++) {
    Assert-Cache ($newResponses[$i].Response -eq $commands[$i].Expected) "Console response mismatch at cache input $i."
}
$cacheViews = @($rows | Where-Object Cache)
Assert-Cache (@($cacheViews | Where-Object {$_.Cache.StockId -eq $rootId}).Count -eq 1 -and
    @($cacheViews | Where-Object {$_.Cache.PickAttemptId -eq $working.Cache.PickAttemptId}).Count -eq 2 -and
    @($cacheViews | Where-Object {$_.Cache.Open -and $_.Cache.StockId -eq ''}).Count -ge 1 -and
    (Hash-CacheFile (Join-Path $console 'continued.ddsave')) -ceq $finalSha -and
    (Hash-CacheFile (Join-Path $console 'pick-pending.ddsave')) -ceq (Hash-CacheFile (Join-Path $csharp 'pick-pending.ddsave'))) (
    'Console projections and pending/final canonical saves must agree.')

$events | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $ResultsRoot 'timeline.json') -Encoding utf8
[ordered]@{
    Status='PASS'; BaselineRevision=165; BaselineSha256=(Hash-CacheFile $acceptedFinal)
    FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString(); FinalSha256=$finalSha
    PendingSha256=(Hash-CacheFile (Join-Path $csharp 'pick-pending.ddsave')); ConsoleInputs=$rows.Count
    FileTimings=$fileTimings; EncodableFalseCacheRejected=$rejected; PickAttempts=$final.SupplyCacheAttempts
    RootPounds=$root.Amount.ToString(); CarriedLot=$child.LotId; CarriedPounds=$lot.Amount.ToString()
    ReserveLocation=$reserve.LocationId
} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $ResultsRoot 'results.json') -Encoding utf8
Get-Content -LiteralPath (Join-Path $ResultsRoot 'results.json')
