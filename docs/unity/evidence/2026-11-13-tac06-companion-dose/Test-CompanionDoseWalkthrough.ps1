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
foreach ($branch in 'walkthrough') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $expectedFinal = 183
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try {
            & $Launcher -CompanionDose -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" |
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
                    if ($request.id -in 'vial.out-of-reach','ally.pre-admission','ally.range-denied') { 'Unavailable' }
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
        $denials = [ordered]@{'rejected-pickup'='settled';'pre-admission-denied'='held';'range-denied'='out-of-reach';'retry-unchanged'='fed'}
        foreach ($key in $denials.Keys) {
            Require ($hashes["$key.ddsave"] -ceq $hashes["$($denials[$key]).ddsave"]) "$branch $key mutated the state."
        }
        $checks[$runName] = [ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
    }

    $restored = "$folder/Restored"
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCompanionDose()
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

    $points = @('staged','entry','held','admitted','damaged','out-of-reach','ready','fed','exited','continued')
    $states = @{}
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $states[$point] = $state
        $body = $state.PortableEquipment | Where-Object Id -eq $vial
        $h = $state.Actors | Where-Object Id -eq $hero
        $c = $state.Actors | Where-Object Id -eq 'TEST_ONLY.companion'
        $hLife = $state.Lives | Where-Object ActorId -eq $hero
        $cLife = $state.Lives | Where-Object ActorId -eq $c.Id
        $interval = $state.WorldIntervals | Where-Object ActorId -eq $hero
        $dose = $state.AlchemyDoses | Where-Object Id -eq $vial
        $burden = [Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($state,$hero)
        $data[$point] = [ordered]@{
            Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision
            Clock=$state.RuleClock.ToString(); Turn=$state.Encounter.CurrentTurnId; InEncounter=$state.InventoryCombat
            HeroX=$h.X; HeroY=$h.Y; CompanionX=$c.X; CompanionY=$c.Y; HeroHP=$hLife.Hp
            CompanionHP=$cLife.Hp; CompanionMaximum=$cLife.MaximumHp; CompanionWounds=$cLife.LinkedInjuries.Count
            Roster=@($state.Encounter.Order); ReinforcementAdmitted=($null -ne $state.Reinforcement.Admission)
            Parent=$body.ParentId; Hands=$body.HeldHands; Pounds=$burden.Pounds.ToString(); Load=$burden.Load.ToString()
            ActionSpent=$interval.ActionSpent; Interactions=$state.InventoryInteractions; Rng=$state.RandomState.ToString()
            Dose=$dose; Body=$body; Sibling=($state.AlchemyDoses | Where-Object Id -eq 'manufacture.order.104.dose1')
        }
    }
    Require ($data.entry.Wire -eq 99 -and $data.entry.Base -eq 90 -and $data.entry.InEncounter -and
        $data.entry.HeroX -eq 0 -and $data.entry.HeroY -eq 3 -and $data.entry.Parent -eq $pack -and
        $data.staged.CompanionX -eq 2 -and $data.entry.Roster -cnotcontains 'TEST_ONLY.companion' -and
        $data.admitted.ReinforcementAdmitted -and $data.admitted.Roster -ccontains 'TEST_ONLY.companion' -and
        $data.admitted.CompanionX -eq 1 -and $data.admitted.CompanionY -eq 3) 'Actual staging or roster admission differs.'
    Require ($data.admitted.CompanionHP -eq 26 -and $data.damaged.CompanionHP -eq 25 -and
        $data.damaged.CompanionWounds -eq 0 -and $data['out-of-reach'].HeroY -eq 1 -and
        $data.ready.HeroX -eq 0 -and $data.ready.HeroY -eq 2) 'Actual defender damage or five-foot positioning differs.'
    $before = $data.ready
    $after = $data.fed
    Require (!$before.ActionSpent -and $after.ActionSpent -and $before.Interactions -eq $after.Interactions -and
        $before.Clock -eq $after.Clock -and $before.Rng -ne $after.Rng -and $before.HeroHP -eq $after.HeroHP -and
        $after.CompanionHP -eq 26 -and $after.Dose.ActualHealing -eq 1 -and $after.Dose.PotentialHealing -eq 7 -and
        $after.Dose.FirstD4 -eq 3 -and $after.Dose.SecondD4 -eq 2 -and $after.Dose.UserId -eq $hero -and
        $after.Dose.RecipientId -eq 'TEST_ONLY.companion' -and $after.Body.Id -eq $before.Body.Id -and
        $after.Body.OwnerId -eq 'TEST_ONLY.companion' -and $after.Body.CustodianId -eq $hero -and $after.Hands -eq 1 -and
        !(Compare-Object @($before.Sibling | ConvertTo-Json -Compress) @($after.Sibling | ConvertTo-Json -Compress))) 'Healing, exact finite custody or sibling identity differs.'
    Require (!$data.exited.InEncounter -and !$data.continued.InEncounter -and $data.continued.Revision -eq 183 -and
        $data.continued.Clock -ne $data.exited.Clock) 'The encounter did not close and return to real ordinary travel.'
    $branches[$branch] = [ordered]@{Console=$checks; Direct=$digests; Observations=$data; FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()}
}
[ordered]@{Status='PASS'; Wire=99; Base=90; Branches=$branches} |
    ConvertTo-Json -Depth 12 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: companion administration, restored console and direct C# replay in $Run"
