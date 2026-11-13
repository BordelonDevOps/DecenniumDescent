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
foreach ($branch in 'closed','open') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $closed = $branch -eq 'closed'
    $expectedFinal = if ($closed) { 167 } else { 166 }
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try {
            & $Launcher -TacticalVial -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" |
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
                    if ($request.id -in 'vial.out-of-reach','tac.closed-retrieve','tac.contained-use','tac.pending-retrieve','tac.action-spent') { 'Unavailable' }
                    elseif ($request.id -and !$seen.Add($request.id)) { 'Duplicate' }
                    else { $revision++; 'Committed' }
                }
            }
            $result = $responses[$i]
            Require ($result.Response -ceq $expected) "$branch $runName unexpected response for input $i ($($request.id))."
            if ($request.op -notin 'save','load') {
                Require ($result.Revision -eq $revision) "$branch $runName wrong revision at input $i."
            }
            if ($request.id -eq 'tac.pending-retrieve') {
                Require ($result.PendingDecision -eq 'Opportunity') 'The pending denial requires a live opportunity decision.'
            }
        }
        Require ($revision -eq $expectedFinal) "$branch $runName did not reach its real continuation."
        $denials = [ordered]@{'rejected-pickup'='settled';'contained-denied'=$(if ($closed) {'opened'} else {'entry'})}
        if ($closed) {
            $denials['closed-denied'] = 'entry'
            $denials['pending-denied'] = 'pending'
            $denials['spent-denied'] = 'retrieved'
        }
        foreach ($key in $denials.Keys) {
            Require ($hashes["$key.ddsave"] -ceq $hashes["$($denials[$key]).ddsave"]) "$branch $key mutated the state."
        }
        $checks[$runName] = [ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
    }

    $restored = "$folder/Restored"
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithTacticalVial()
    $marks = @{}
    foreach ($key in $checks.Restored.Checkpoints.Keys) {
        Require ($checks.Restored.Checkpoints[$key] -ceq $checks.Uninterrupted.Checkpoints[$key]) "$branch differs on restored replay at $key."
        $state = $store.Load("$restored/$key")
        if (!$marks.ContainsKey($state.Revision)) { $marks[$state.Revision] = [Collections.Generic.List[string]]::new() }
        $marks[$state.Revision].Add($key)
    }
    $final = $store.Load("$restored/continued.ddsave")
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

    $points = @('entry','before-retrieve','retrieved','used','exited','continued')
    if ($closed) { $points += 'opened','ready','pending' }
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $body = $state.PortableEquipment | Where-Object Id -eq $vial
        $container = $state.PortableEquipment | Where-Object Id -eq $pack
        $interval = $state.WorldIntervals | Where-Object ActorId -eq $hero
        $life = $state.Lives | Where-Object ActorId -eq $hero
        $dose = $state.AlchemyDoses | Where-Object Id -eq $vial
        $burden = [Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($state,$hero)
        $data[$point] = [ordered]@{
            Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision
            Clock=$state.RuleClock.ToString(); Turn=$state.Encounter.CurrentTurnId; InEncounter=$state.InventoryCombat
            PackOpen=$container.Open; Parent=$body.ParentId; Hands=$body.HeldHands; Pounds=$burden.Pounds.ToString(); Load=$burden.Load.ToString()
            ActionSpent=$interval.ActionSpent; Interactions=$state.InventoryInteractions; Rng=$state.RandomState.ToString()
            WorkIntervals=$state.Work.WorkerIntervals.Count; FirstD4=$dose.FirstD4; SecondD4=$dose.SecondD4
            PotentialHealing=$dose.PotentialHealing; ActualHealing=$dose.ActualHealing; Spent=$dose.Spent
            HP=$life.Hp; MaximumHP=$life.MaximumHp; X=($state.Actors | Where-Object Id -eq $hero).X
            Y=($state.Actors | Where-Object Id -eq $hero).Y
        }
    }
    Require ($data.entry.Wire -eq 98 -and $data.entry.Base -eq 90 -and $data.entry.InEncounter -and
        $data.entry.X -eq 0 -and $data.entry.Y -eq 3 -and $data.entry.Parent -eq $pack -and
        $data.entry.PackOpen -eq (!$closed)) "$branch did not genuinely enter packed."
    if ($closed) {
        Require ($data.opened.Interactions -eq 1 -and !$data.opened.ActionSpent -and $data.opened.PackOpen -and
            $data.opened.Parent -eq $pack -and $data.opened.Clock -eq $data.entry.Clock -and
            $data.opened.Rng -eq $data.entry.Rng -and $data.opened.WorkIntervals -eq $data.entry.WorkIntervals) 'Tactical open costs or access differ.'
    }
    $prior = $data['before-retrieve']
    Require ($data.retrieved.Interactions -eq $(if ($closed) {2} else {1}) -and $data.retrieved.ActionSpent -eq $closed -and
        $data.retrieved.Hands -eq 1 -and $data.retrieved.Parent -eq '' -and
        $data.retrieved.Pounds -eq $prior.Pounds -and $data.retrieved.Load -eq $prior.Load -and
        $data.retrieved.Rng -eq $prior.Rng -and $data.retrieved.Clock -eq $prior.Clock -and
        $data.retrieved.WorkIntervals -eq $prior.WorkIntervals) "$branch tactical retrieve costs differ."
    Require ($data.used.ActionSpent -and $data.used.Spent -and $data.used.Hands -eq 1 -and
        ($data.used.Turn -eq $data.retrieved.Turn) -eq (!$closed) -and
        $data.used.PotentialHealing -eq ($data.used.FirstD4 + $data.used.SecondD4 + 2) -and
        !$data.exited.InEncounter -and !$data.continued.InEncounter -and $data.continued.Revision -eq $expectedFinal -and
        $data.continued.Clock -ne $data.exited.Clock) "$branch use or continuation differs."
    $branches[$branch] = [ordered]@{Console=$checks; Direct=$digests; Observations=$data; FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()}
}
[ordered]@{Status='PASS'; Wire=98; Base=90; Branches=$branches} |
    ConvertTo-Json -Depth 12 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: both connected paths, exact restores and direct replay in $Run"
