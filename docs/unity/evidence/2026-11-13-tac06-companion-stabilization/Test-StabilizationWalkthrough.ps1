param([string]$AssemblyRoot,[string]$Launcher,[string]$Run)
$ErrorActionPreference = 'Stop'
$Run = (New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require($condition,$message) { if (!$condition) { throw $message } }
function Dispatch($session,$receipt) {
    $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
    if ($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { return $session.AdvanceAutomaticDefender() }
    if ($command.Kind -in 'AdvanceClock','EndFixedEncounter') { return $session.SubmitSessionCommand($command) }
    $seat = if ($command.Actor -eq 'TEST_ONLY.third-combatant') { 'FirstOpponent' } else { 'Player' }
    $session.Submit($seat,$command)
}
$store = [Decennium.Foundation.FileSaveStore]::new()
$branches = [ordered]@{}
$hero = 'TEST_ONLY.actor'
$vial = 'manufacture.order.104.dose0'
$pack = 'TEST_ONLY.explorer-pack'
foreach ($branch in 'failure','success') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $succeeds = $branch -eq 'success'
    $expectedFinal = if ($succeeds) { 320 } else { 350 }
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try {
            & $Launcher -CompanionStabilization -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" |
                Set-Content "$target/responses.jsonl" -Encoding utf8
        } finally { Pop-Location }
        $responses = @(Get-Content "$target/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
        Require ($responses.Count -eq $trace.Count) "$branch $runName response count differs."
        $revision = 0
        $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        $hashes = [ordered]@{}
        for ($i=0; $i -lt $trace.Count; $i++) {
            $request = $trace[$i]
            $expected = switch ($request.op) {
                'save' { $hashes[$request.path] = Digest "$target/$($request.path)"; 'Saved' }
                'load' { 'Restored' }
                default {
                    if ($request.id -in 'vial.out-of-reach','ally.pre-admission','ally.range-denied','stab.range-denied','stab.same-turn-denied','stab.already-stable') { 'Unavailable' }
                    elseif ($request.id -and !$seen.Add($request.id)) { 'Duplicate' }
                    else { $revision++; 'Committed' }
                }
            }
            $result = $responses[$i]
            Require ($result.Response -ceq $expected) "$branch $runName unexpected response for input $i ($($request.id))."
            if ($request.op -notin 'save','load') {
                Require ($result.Revision -eq $revision) "$branch $runName wrong revision at input $i."
            }
        }
        Require ($revision -eq $expectedFinal) "$branch $runName did not reach its real continuation."
        $denials = [ordered]@{'rejected-pickup'='settled';'pre-admission-denied'='held';'range-denied'='out-of-reach';
            'range-unchanged'='dying-out-of-reach';'retry'='attempt';'action-denied'='attempt'}
        if ($succeeds) { $denials['already-stable-denied']='still-stable' }
        foreach ($key in $denials.Keys) {
            Require ($hashes["$key.ddsave"] -ceq $hashes["$($denials[$key]).ddsave"]) "$branch $key mutated the state."
        }
        $checks[$runName] = [ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
    }

    $restored = "$folder/Restored"
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCompanionStabilization()
    $marks = @{}
    foreach ($key in $checks.Restored.Checkpoints.Keys) {
        Require ($checks.Restored.Checkpoints[$key] -ceq $checks.Uninterrupted.Checkpoints[$key]) "$branch differs on restored replay at $key."
        $state = $store.Load("$restored/$key")
        if (!$marks.ContainsKey($state.Revision)) { $marks[$state.Revision] = [Collections.Generic.List[string]]::new() }
        $marks[$state.Revision].Add($key)
    }
    $finalName = if ($succeeds) { "recovered" } else { "continued" }
    $final = $store.Load("$restored/$finalName.ddsave")
    $digests = [ordered]@{}
    foreach ($receipt in $final.Receipts) {
        $result = Dispatch $direct $receipt
        Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "$branch direct replay diverged at $($receipt.Revision)."
        if (!$marks.ContainsKey($receipt.Revision)) { continue }
        foreach ($key in $marks[$receipt.Revision]) {
            $path = "$folder/direct-$key"
            $direct.Save($path)
            $digests[$key] = Digest $path
            Require ($digests[$key] -ceq $checks.Restored.Checkpoints[$key]) "$branch direct replay differs at $key."
        }
    }
    Require ($digests.Count -eq $checks.Restored.Checkpoints.Count) "$branch direct replay missed checkpoints."

    $points = @('entry','admitted','damaged','dying-out-of-reach','ready','attempt','exited','continued')
    if ($succeeds) { $points += 'recovered' }
    $data = [ordered]@{}
    $states = @{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $states[$point] = $state
        $patient = $state.Lives | Where-Object ActorId -eq 'TEST_ONLY.companion'
        $interval = $state.WorldIntervals | Where-Object ActorId -eq $hero
        $data[$point] = [ordered]@{
            Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision; Clock=$state.RuleClock.ToString()
            Turn=$state.Encounter.CurrentTurnId; InEncounter=$state.InventoryCombat; ActionSpent=$interval.ActionSpent
            Interactions=$state.InventoryInteractions; PatientHP=$patient.Hp; Stable=$patient.Stable; Dead=$patient.Dead
            DeathSuccesses=$patient.DeathSuccesses; DeathFailures=$patient.DeathFailures; Injuries=$patient.LinkedInjuries
            Prone=$patient.Prone; Deadline=$patient.StableUntil; Rng=$state.RandomState
            Attempts=$state.CompanionStabilizations; RecoveryEvents=@($state.LifeEvents | Where-Object Kind -eq 'StableRecovery')
        }
    }
    $before = $data.ready
    $after = $data.attempt
    $check = $after.Attempts[0]
    Require ($before.Wire -eq 100 -and $before.Base -eq 90 -and $before.PatientHP -eq 0 -and !$before.Stable -and !$before.Dead -and
        !$before.ActionSpent -and $after.ActionSpent -and $after.PatientHP -eq 0 -and $before.Interactions -eq $after.Interactions -and
        $before.Clock -eq $after.Clock -and $before.Rng -eq $check.RandomBefore -and $after.Rng -eq $check.RandomAfter -and
        $check.Succeeded -eq $succeeds -and $check.Modifier -eq 0 -and [Decennium.Foundation.CompanionStabilizationAttempt]::DC -eq 10 -and
        !(Compare-Object @($before.Injuries) @($after.Injuries)) -and $before.Prone -eq $after.Prone) "$branch changed cost or independent life state."
    if ($succeeds) {
        Require ($check.Natural -eq 12 -and $check.RecoveryDie -eq 2 -and $check.WordsConsumed -eq 2 -and
            $after.Stable -and $after.DeathSuccesses -eq 0 -and $after.DeathFailures -eq 0 -and
            $after.Deadline.ToString() -eq '128033/2' -and $data.continued.Stable -and
            $data.recovered.Clock -eq '128033/2' -and $data.recovered.PatientHP -eq 1 -and !$data.recovered.Stable -and
            $data.recovered.RecoveryEvents.Count -eq 1 -and $data.recovered.RecoveryEvents[0].WordsConsumed -eq 0 -and
            $data.recovered.RecoveryEvents[0].RandomBefore -eq $data.recovered.RecoveryEvents[0].RandomAfter) 'Absolute recovery differed.'
    } else {
        $first = $states.ready.Lives | Where-Object ActorId -eq 'TEST_ONLY.companion'
        $second = $states.attempt.Lives | Where-Object ActorId -eq 'TEST_ONLY.companion'
        Require ($check.Natural -eq 6 -and $check.RecoveryDie -eq 0 -and $check.WordsConsumed -eq 1 -and $first.SameAs($second)) 'Failed Medicine altered life.'
    }
    Require (!$data.exited.InEncounter -and !$data.continued.InEncounter -and
        $data.continued.Clock -ne $data.exited.Clock -and $final.Revision -eq $expectedFinal) 'The actual route did not return to ordinary travel.'
    $branches[$branch] = [ordered]@{Console=$checks; Direct=$digests; Observations=$data; FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()}
}
[ordered]@{Status='PASS'; Wire=100; Base=90; Branches=$branches} |
    ConvertTo-Json -Depth 12 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: actual stabilization failure and recovery, restored console and direct C# replay in $Run"
