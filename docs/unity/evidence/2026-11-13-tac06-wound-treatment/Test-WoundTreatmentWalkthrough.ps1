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
function Stock($state,$basket) {
    $type = [Decennium.Foundation.WoundTreatmentStation]
    $lots = @($type::Stock($basket) | ForEach-Object {
        $origin = $_
        $lot = $state.Work.Lots | Where-Object Id -ceq $origin.Id
        [ordered]@{Id=$lot.Id; Location=$lot.LocationId; Custodian=$lot.CustodianId; Unit=$lot.UnitId;
            Initial=$origin.Amount.ToString(); Current=$lot.Amount.ToString()}
    })
    $vessels = @($type::Vessels($basket) | ForEach-Object {
        [ordered]@{Id=$_.Id; LotId=$_.LotId; Capacity=$_.CapacityPints; Tare=$_.TarePounds.ToString();
            Gross=$_.GrossPounds($state.Work).ToString()}
    })
    [ordered]@{Lots=$lots; Vessels=$vessels}
}
$store = [Decennium.Foundation.FileSaveStore]::new()
$patient = 'TEST_ONLY.companion'
$hero = 'TEST_ONLY.actor'
$kit = [Decennium.Foundation.WoundTreatmentStation]::KitLot
$denied = @('vial.out-of-reach','ally.pre-admission','ally.range-denied','stab.range-denied',
    'stab.same-turn-denied','stab.already-stable','treatment.wrong-actor','treatment.wrong-target',
    'treatment.no-active','treatment.parallel','treatment.occupied-move','treatment.no-wound',
    'treatment.pressure-block','treatment.no-third-basket')
$branches = [ordered]@{}
foreach ($branch in 'success','interrupted-critical-failure') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $success = $branch -eq 'success'
    $finalName = if ($success) { 'continued' } else { 'critical-failure' }
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try {
            & $Launcher -WoundTreatment -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" |
                Set-Content "$target/responses.jsonl" -Encoding utf8
        } finally { Pop-Location }
        $responses = @(Get-Content "$target/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
        Require ($responses.Count -eq $trace.Count) "$branch $runName response count differs."
        $revision = 0
        $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        $hashes = [ordered]@{}
        for ($i = 0; $i -lt $trace.Count; $i++) {
            $request = $trace[$i]
            $expected = switch ($request.op) {
                'save' { $hashes[$request.path] = Digest "$target/$($request.path)"; 'Saved' }
                'load' { 'Restored' }
                default {
                    if ($request.id -in $denied) { 'Unavailable' }
                    elseif ($request.id -and !$seen.Add($request.id)) { 'Duplicate' }
                    else { $revision++; 'Committed' }
                }
            }
            Require ($responses[$i].Response -ceq $expected) "$branch $runName input $i ($($request.id)) expected $expected."
            if ($request.op -notin 'save','load') {
                Require ($responses[$i].Revision -eq $revision) "$branch $runName unexpected revision at $i."
            }
        }
        $expectedFinal = if ($success) { 323 } else { 324 }
        Require ($revision -eq $expectedFinal) "$branch $runName missed its continuation."
        $same = [ordered]@{'admission-denied'='exited'; 'retry'='active'; 'busy-denied'='active'}
        if ($success) { $same['completion-denied']='completed' }
        else { $same['interrupt-retry']='interrupted'; $same['stock-denied']='critical-failure' }
        foreach ($name in $same.Keys) {
            Require ($hashes["$name.ddsave"] -ceq $hashes["$($same[$name]).ddsave"]) "$branch $name changed complete state."
        }
        $checks[$runName] = [ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
    }

    $restored = "$folder/Restored"
    $marks = @{}
    foreach ($key in $checks.Restored.Checkpoints.Keys) {
        Require ($checks.Restored.Checkpoints[$key] -ceq $checks.Uninterrupted.Checkpoints[$key]) "$branch restore differs at $key."
        $state = $store.Load("$restored/$key")
        if (!$marks.ContainsKey($state.Revision)) { $marks[$state.Revision] = [Collections.Generic.List[string]]::new() }
        $marks[$state.Revision].Add($key)
    }
    $final = $store.Load("$restored/$finalName.ddsave")
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithWoundTreatment()
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

    $points = @('exited','active','before-recovery','recovered')
    if ($success) { $points += 'completed','continued' }
    else { $points += 'interrupted','intermission','restarted','critical-failure' }
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $life = $state.Lives | Where-Object ActorId -eq $patient
        $healer = $state.Actors | Where-Object Id -eq $hero
        $recipient = $state.Actors | Where-Object Id -eq $patient
        $strain = [Decennium.Foundation.Laboratory.ExpeditionStrainRules]::Current($state,$patient)
        $data[$point] = [ordered]@{
            Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision; Clock=$state.RuleClock.ToString()
            HealerCell=@($healer.X,$healer.Y); PatientCell=@($recipient.X,$recipient.Y)
            Hp=$life.Hp; MaxHp=$life.MaximumHp; Stable=$life.Stable; Prone=$life.Prone; Wounds=$life.LinkedInjuries
            RecoveryAt=$life.StableUntil; RNG=$state.RandomState; Jobs=$state.WoundTreatments
            KitAvailable=$state.Work.Available($kit); Baskets=@((Stock $state 0),(Stock $state 1))
            Occupancy=@($state.Work.WorkerIntervals | Where-Object JobId -like 'TEST_ONLY.wound-treatment.*')
            Claims=@($state.Work.Reservations | Where-Object JobId -like 'TEST_ONLY.wound-treatment.*')
            Recovery=@($state.LifeEvents | Where-Object { $_.ActorId -eq $patient -and $_.Kind -eq 'StableRecovery' })
            Pressure=@($state.ExpeditionPressureCheckpoints); Gains=$state.ExpeditionStrainGains; Strain=$strain
        }
    }
    Require ($data.exited.Wire -eq 101 -and $data.exited.Base -eq 90 -and $data.exited.Revision -eq 317 -and
        $data.exited.Clock -eq '113673/2' -and $data.exited.Stable -and $data.exited.Hp -eq 0 -and
        ($data.exited.HealerCell -join ',') -eq '1,2' -and ($data.exited.PatientCell -join ',') -eq '1,3' -and
        $data.active.Hp -eq 0 -and $data.active.KitAvailable -eq 0 -and $data.active.Occupancy.Count -eq 2 -and
        $data.active.RNG -eq $data.exited.RNG -and $data.active.Clock -eq $data.exited.Clock -and
        $data.'before-recovery'.Hp -eq 0 -and $data.recovered.Hp -eq 1 -and $data.recovered.Prone -and
        $data.recovered.Clock -eq '128033/2' -and $data.recovered.Wounds.Count -eq 1 -and
        $data.recovered.Recovery.Count -eq 1 -and $data.recovered.Recovery[0].WordsConsumed -eq 0 -and
        $data.recovered.Jobs[0].Outcome -eq 'Active') "$branch did not retain independent Stable recovery."
    Require ((@($data.active.Baskets[0].Lots | Where-Object Current -eq '0/1')).Count -eq 5 -and
        (@($data.active.Baskets[1].Lots | Where-Object { $_.Initial -eq $_.Current })).Count -eq 5 -and
        ($data.active.Baskets[0].Vessels.Gross -join ',') -eq '1/1,1/1,1/4' -and
        ($data.exited.Baskets[0].Vessels.Gross -join ',') -eq '5/1,5/1,1/1' -and
        ($data.active.Baskets[0].Vessels.Id -join ',') -eq ($data.exited.Baskets[0].Vessels.Id -join ',')) "$branch stock or vessels differ."
    if ($success) {
        $check = $data.completed.Jobs[0]
        Require ($data.completed.Clock -eq '171273/2' -and $check.Outcome -eq 'Success' -and $check.Natural -eq 17 -and
            $check.Modifier -eq 0 -and $check.WordsConsumed -eq 1 -and $data.completed.Hp -eq 1 -and
            $data.completed.Prone -and $data.completed.Wounds.Count -eq 0 -and $data.completed.KitAvailable -eq 1 -and
            $data.completed.Gains.Count -eq 0 -and ($data.continued.HealerCell -join ',') -eq '2,2') 'Success or continued movement differed.'
    } else {
        $end = $data.'critical-failure'
        $check = $end.Jobs[1]
        Require ($data.interrupted.Jobs[0].Outcome -eq 'Interrupted' -and $data.interrupted.Jobs[0].WordsConsumed -eq 0 -and
            $data.interrupted.KitAvailable -eq 1 -and $data.interrupted.RNG -eq $data.recovered.RNG -and
            $data.restarted.Clock -eq '166400/1' -and $end.Clock -eq '195200/1' -and $check.Outcome -eq 'CriticalFailure' -and
            $check.Natural -eq 2 -and $check.WordsConsumed -eq 1 -and $end.Wounds.Count -eq 1 -and $end.Hp -eq 1 -and
            $end.Gains.Count -eq 1 -and $end.Gains[0].ActorId -eq $patient -and $end.Gains[0].CauseId -eq $check.Id -and
            $end.Strain.Level -eq 1 -and $end.Strain.InitiativeModifier -eq -1 -and $end.Strain.ExpeditionCheckModifier -eq -1 -and
            $end.Strain.AttackModifier -eq 0 -and $end.Strain.SavingThrowModifier -eq 0) 'Interruption or first-point Strain differed.'
    }
    $branches[$branch] = [ordered]@{Runs=$checks; DirectCheckpoints=$digests; States=$data; Final=(Digest "$restored/$finalName.ddsave")}
}
[ordered]@{Status='PASS'; Branches=$branches} | ConvertTo-Json -Depth 15 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: treatment, recovery, interruption, critical failure and three-path replay in $Run"
