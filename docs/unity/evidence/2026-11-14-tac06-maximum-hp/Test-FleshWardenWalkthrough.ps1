param([string]$AssemblyRoot,[string]$Launcher,[string]$Run)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$Launcher = (Resolve-Path -LiteralPath $Launcher).Path
$Run = (New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
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
foreach ($branch in 'split','whole') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try { & $Launcher -FleshWarden -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" | Set-Content "$target/responses.jsonl" -Encoding utf8 }
        finally { Pop-Location }
        $responses = @(Get-Content "$target/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
        Require ($responses.Count -eq $trace.Count) "$branch $runName response count differs."
        $revision = 0
        $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        $hashes = [ordered]@{}
        for ($i=0; $i -lt $trace.Count; $i++) {
            $request = $trace[$i]
            if ($request.op -eq 'view') {
                Require ($responses[$i].Revision -eq $revision) "$branch view has stale revision."
                if ($request.seat -eq 'FirstOpponent') { Require ($null -eq $responses[$i].ShortRest) 'Foreign seat disclosed rest history.' }
                else { Require ($responses[$i].ShortRest.SiteId -eq 'TEST_ONLY.short-rest-berth') 'Owner rest view missing.' }
                continue
            }
            $expected = switch ($request.op) {
                'save' { $hashes[$request.path] = Digest "$target/$($request.path)"; 'Saved' }
                'load' { 'Restored' }
                default {
                    if ($request.expect) { $request.expect }
                    elseif ($request.id -eq 'decay.control.wrong-seat') { 'NotAuthorized' }
                    elseif ($request.id -like 'decay.control.*') { 'Unavailable' }
                    elseif ($request.id -and !$seen.Add($request.id)) {
                        if ($request.target -eq $hero) { 'CommandIdConflict' } else { 'Duplicate' }
                    } else { $revision++; 'Committed' }
                }
            }
            Require ($responses[$i].Response -ceq $expected) "$branch $runName input $i ($($request.id)) expected $expected; got $($responses[$i].Response)."
            if ($request.op -notin 'save','load' -and $null -ne $responses[$i].Revision) {
                Require ($responses[$i].Revision -eq $revision) "$branch $runName revision differs at $i."
            }
        }
        foreach ($name in @($hashes.Keys | Where-Object { $_ -like '*-after.ddsave' })) {
            $before = $name.Replace('-after.ddsave','-before.ddsave')
            Require ($hashes[$name] -ceq $hashes[$before]) "$branch $name changed denied state."
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
    $final = $store.Load("$restored/rest-continued.ddsave")
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFleshWarden()
    $digests = [ordered]@{}
    foreach ($receipt in $final.Receipts) {
        $result = Dispatch $direct $receipt
        Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "$branch direct replay failed at $($receipt.Revision)."
        if (!$marks.ContainsKey($receipt.Revision)) { continue }
        foreach ($key in $marks[$receipt.Revision]) {
            $path = "$folder/direct-$key"
            $direct.Save($path)
            $digests[$key] = Digest $path
            Require ($digests[$key] -ceq $checks.Restored.Checkpoints[$key]) "$branch direct replay differs at $key."
        }
    }
    Require ($digests.Count -eq $checks.Restored.Checkpoints.Count) "$branch direct replay missed checkpoints."
    $points = @('before-first-rest','first-rest-pending','first-rest-completed','entry','defeated','healed','continued','rest-completed','rest-continued')
    if ($branch -eq 'split') { $points += 'first-rest-partial','first-rest-before-end','first-rest-end' }
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $life = $state.Lives | Where-Object ActorId -eq $hero
        $position = $state.Actors | Where-Object Id -eq $hero
        $data[$point] = [ordered]@{Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision
            Clock=$state.RuleClock.ToString(); Combat=$state.InventoryCombat; Cell=@($position.X,$position.Y)
            Hp=$life.Hp; MaxHp=$life.MaximumHp; TempHp=$life.TemporaryHp; RNG=$state.RandomState
            Calendar=$state.WorldSchedule; Encounter=$state.Encounter; Intervals=$state.WorldIntervals
            Grant=$state.ConsumeDecay; Rests=$state.ShortRests; Mutation=$state.FleshWarden; Vial=($state.AlchemyDoses | Where-Object Id -eq 'manufacture.order.104.dose0')
            BenefitsUsed=[Decennium.Foundation.ShortRestBerth]::BenefitsUsed($state)}
    }
    $arrival=$data.'before-first-rest'; $pending=$data.'first-rest-pending'; $first=$data.'first-rest-completed'
    Require ($arrival.Wire -eq 104 -and $arrival.Base -eq 90 -and $arrival.Revision -eq 120 -and
        $arrival.Clock -eq '56681/1' -and ($arrival.Cell -join ',') -eq '0,1' -and !$arrival.Combat -and
        $arrival.Encounter.Id -eq 'world.fixed-conflict' -and $arrival.Encounter.Sparse) "$branch missed actual historical-calendar arrival."
    Require ($pending.Rests[0].Outcome -eq 'Active' -and $first.Rests[0].Outcome -eq 'Completed' -and $first.BenefitsUsed -eq 1 -and
        $first.Rests[0].Benefit -eq 'Eligible' -and $first.Clock -eq '60281/1' -and $first.Hp -eq 26 -and $first.MaxHp -eq 32 -and
        $first.RNG -eq $arrival.RNG -and $first.Rests[0].Healing -eq 0 -and $first.Rests[0].HitDiceSpent -eq 0 -and
        $first.Rests[0].RewardRandomWords -eq 0 -and $first.Calendar.ProcessedSlot -eq $arrival.Calendar.ProcessedSlot+1200 -and
        $first.Encounter.Id -eq $arrival.Encounter.Id -and $first.Encounter.Origin.Equals($arrival.Encounter.Origin) -and
        ($first.Encounter.InitialOrder -join ',') -ceq ($arrival.Encounter.InitialOrder -join ',')) "$branch rest altered calendar identity, progression, life or reward."
    if ($branch -eq 'split') {
        Require ($data.'first-rest-partial'.Rests[0].Outcome -eq 'Active' -and
            $data.'first-rest-before-end'.Rests[0].Outcome -eq 'Active' -and $data.'first-rest-end'.Rests[0].Outcome -eq 'Completed') 'Split hour completed early.'
    }
    Require ($data.entry.Combat -and $data.entry.Encounter.Id -ne $arrival.Encounter.Id -and $data.defeated.Hp -lt 26 -and
        $data.healed.Hp -gt 26 -and $data.healed.MaxHp -eq 32 -and $data.healed.Vial.Spent -and $data.healed.Vial.ActualHealing -gt 0) "$branch did not enter genuine later combat and use a finite tactical vial."
    $end=$data.'rest-completed'
    Require ($end.Rests.Count -eq 2 -and $end.Rests[-1].Outcome -eq 'Completed' -and $end.BenefitsUsed -eq 2 -and
        $end.Hp -eq 26 -and $end.MaxHp -eq 26 -and $end.TempHp -eq 0 -and $end.Grant.End -eq 'Expired' -and
        ($data.'rest-continued'.Cell -join ',') -eq '0,0') "$branch did not finish the second actual rest and paid continuation."
    Require ($pending.MaxHp -eq 26 -and $pending.Hp -eq 26 -and $pending.Mutation.Applications.Count -eq 0 -and
        $pending.Mutation.EquippedMutationId -eq 'warrior.supplement.spinal-buffer') 'A pending choice changed the loadout or life.'
    Require ($first.Mutation.EquippedMutationId -eq 'warrior.supplement.flesh-warden' -and
        $first.Mutation.Applications.Count -eq 1 -and $first.Mutation.Applications[0].Amount -eq 6 -and
        $first.Mutation.Applications[0].Present -and $first.Mutation.Choices[0].Change.Healing -eq 0 -and
        $first.Mutation.Choices[0].Change.CapacityClamp -eq 0) 'First completed rest did not apply actual capacity only.'
    Require ($end.Mutation.EquippedMutationId -eq 'warrior.supplement.spinal-buffer' -and
        $end.Mutation.ApplicationId -eq '' -and $end.Mutation.Applications.Count -eq 1 -and
        !$end.Mutation.Applications[0].Present -and $end.Mutation.Applications[0].Id -eq $first.Mutation.Applications[0].Id -and
        $end.Mutation.Applications[0].EndedAt.Equals($end.Rests[1].EndedAt) -and
        $end.Mutation.Choices[1].Change.HpBefore -eq $data.healed.Hp -and
        $end.Mutation.Choices[1].Change.CapacityClamp -eq ($data.healed.Hp-26) -and
        $end.Mutation.Choices[1].Change.Damage -eq 0 -and $end.Mutation.Choices[1].Change.Healing -eq 0) 'Replacement lost application identity or misclassified the actual clamp.'
    $branches[$branch]=[ordered]@{Runs=$checks; DirectCheckpoints=$digests; States=$data; Final=(Digest "$restored/rest-continued.ddsave")}
}
$split=$branches.split.States.'first-rest-completed'; $whole=$branches.whole.States.'first-rest-completed'
foreach ($property in 'Clock','Hp','MaxHp','TempHp','RNG','BenefitsUsed') { Require ($split[$property] -eq $whole[$property]) "Clock partition changed $property." }
Require ($split.Calendar.ProcessedSlot -eq $whole.Calendar.ProcessedSlot -and $split.Encounter.TurnOrdinal -eq $whole.Encounter.TurnOrdinal -and
    $split.Rests[0].DueAt.Equals($whole.Rests[0].DueAt)) 'Clock partition changed calendar progression or causal deadline.'
$left=$store.Load("$Run/split/Restored/first-rest-completed.ddsave"); $right=$store.Load("$Run/whole/Restored/first-rest-completed.ddsave")
Require (($left.WorldIntervals | ConvertTo-Json -Depth 8 -Compress) -ceq ($right.WorldIntervals | ConvertTo-Json -Depth 8 -Compress)) 'Clock partition changed interval budgets.'
Require ($left.Conditions.Count -eq $right.Conditions.Count) 'Clock partition changed condition count.'
for ($i=0; $i -lt $left.Conditions.Count; $i++) { Require ($left.Conditions[$i].SameAs($right.Conditions[$i])) 'Clock partition changed condition history.' }
[ordered]@{Status='PASS'; Branches=$branches; ClockPartitions='PASS; distinct observation/receipt histories retained'} |
    ConvertTo-Json -Depth 22 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: real Flesh Warden application, injury/healing, capacity clamp and three-path replay in $Run"
