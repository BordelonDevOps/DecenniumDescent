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
$hero = 'TEST_ONLY.actor'
$branches = [ordered]@{}
foreach ($branch in 'early','late') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $early = $branch -eq 'early'
    $finalName = if ($early) { 'continued' } else { 'expired' }
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try {
            & $Launcher -ConsumeDecay -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" |
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
                    if ($request.id -eq 'decay.control.wrong-seat') { 'NotAuthorized' }
                    elseif ($request.id -like 'decay.control.*') { 'Unavailable' }
                    elseif ($request.id -and !$seen.Add($request.id)) {
                        if ($request.target -eq $hero) { 'CommandIdConflict' } else { 'Duplicate' }
                    } else { $revision++; 'Committed' }
                }
            }
            Require ($responses[$i].Response -ceq $expected) "$branch $runName input $i ($($request.id)) expected $expected."
            if ($request.op -notin 'save','load') {
                Require ($responses[$i].Revision -eq $revision) "$branch $runName unexpected revision at $i."
            }
        }
        $expectedFinal = if ($early) { 184 } else { 204 }
        Require ($revision -eq $expectedFinal) "$branch $runName missed its continuation."
        foreach ($name in @($hashes.Keys | Where-Object { $_ -like '*-after.ddsave' })) {
            $before = $name.Replace('-after.ddsave','-before.ddsave')
            Require ($hashes[$name] -ceq $hashes[$before]) "$branch $name changed complete state."
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
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConsumeDecay()
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

    $points = if ($early) { 'entry','ready','grant','depleted','normal-damage','healed','closed','continued' }
        else { 'entry','late-candidate','defeated','grant','healed','closed','continued','before-expiry','expired' }
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $life = $state.Lives | Where-Object ActorId -eq $hero
        $position = $state.Actors | Where-Object Id -eq $hero
        $dose = $state.AlchemyDoses | Where-Object Id -eq 'manufacture.order.104.dose0'
        $last = @($state.MeleeAttacks | Where-Object TargetId -eq $hero | Select-Object -Last 1)
        $data[$point] = [ordered]@{
            Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision; Clock=$state.RuleClock.ToString()
            Combat=$state.InventoryCombat; Turn=$state.Encounter.TurnOrdinal; Cell=@($position.X,$position.Y)
            Hp=$life.Hp; MaxHp=$life.MaximumHp; TempHp=$life.TemporaryHp; Prone=$life.Prone; Wounds=$life.LinkedInjuries
            RNG=$state.RandomState; Grant=$state.ConsumeDecay; Damage=$last; Dose=$dose
            ActionSpent=($state.WorldIntervals | Where-Object ActorId -eq $hero).ActionSpent; Interactions=$state.InventoryInteractions
        }
    }
    Require ($data.entry.Wire -eq 102 -and $data.entry.Base -eq 90 -and $data.entry.Revision -eq 118 -and
        $data.grant.TempHp -eq 3 -and $data.grant.MaxHp -eq 26 -and $data.grant.ActionSpent -and
        $data.grant.Grant.Active -and $data.grant.Grant.Offer -eq 3 -and !$data.closed.Combat -and
        ($data.continued.Cell -join ',') -eq '0,1') "$branch grant, encounter or continuation differed."
    if ($early) {
        Require ($data.ready.RNG -eq $data.grant.RNG -and $data.ready.Clock -eq $data.grant.Clock -and
            $data.ready.Interactions -eq $data.grant.Interactions -and $data.grant.Hp -eq 26 -and
            $data.depleted.Grant.End -eq 'Depleted' -and $data.depleted.TempHp -eq 0 -and $data.depleted.Hp -eq 26 -and
            $data.depleted.Damage[0].Damage.Total -eq 3 -and $data.'normal-damage'.Damage[0].Damage.Total -eq 2 -and
            $data.'normal-damage'.Hp -eq 24 -and $data.healed.Dose.ActualHealing -eq 2 -and
            $data.healed.Hp -eq 26 -and $data.healed.TempHp -eq 0) 'Early actual absorption or separate healing differed.'
    } else {
        $before = $data.'before-expiry'
        Require ($data.grant.Hp -eq 18 -and $data.grant.Clock -eq '113453/2' -and
            $data.healed.Dose.ActualHealing -eq 8 -and $data.healed.Hp -eq 26 -and $data.healed.TempHp -eq 3 -and
            $data.closed.TempHp -eq 3 -and $before.Clock -eq '120651/2' -and $before.TempHp -eq 3 -and
            $data.expired.Clock -eq '120653/2' -and $data.expired.TempHp -eq 0 -and
            $data.expired.Grant.End -eq 'Expired' -and $data.expired.Hp -eq $before.Hp -and
            $data.expired.MaxHp -eq $before.MaxHp -and $data.expired.RNG -eq $before.RNG -and
            $data.expired.Prone -eq $before.Prone -and ($data.expired.Wounds -join ',') -eq ($before.Wounds -join ',')) 'Late healing, closure or exact expiry differed.'
    }
    $branches[$branch] = [ordered]@{Runs=$checks; DirectCheckpoints=$digests; States=$data; Final=(Digest "$restored/$finalName.ddsave")}
}
[ordered]@{Status='PASS'; Branches=$branches} | ConvertTo-Json -Depth 15 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: Consume Decay depletion, independent healing, expiry and three-path replay in $Run"
