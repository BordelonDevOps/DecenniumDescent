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
foreach ($branch in 'completion','whole','interruption') {
    $folder = (New-Item -ItemType Directory "$Run/$branch").FullName
    $inputs = @(Get-Content "$PSScriptRoot/$branch.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $checks = [ordered]@{}
    foreach ($runName in 'Restored','Uninterrupted') {
        $target = (New-Item -ItemType Directory "$folder/$runName").FullName
        $trace = @($inputs | Where-Object { $runName -eq 'Restored' -or $_.op -ne 'load' })
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$target/inputs.jsonl" -Encoding utf8
        Push-Location $target
        try { & $Launcher -ShortRest -AssemblyRoot $AssemblyRoot -InputPath "$target/inputs.jsonl" | Set-Content "$target/responses.jsonl" -Encoding utf8 }
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
    $direct = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
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
    $points = @('continued','rest-pending','rest-completed','rest-continued')
    if ($branch -eq 'completion') { $points += 'rest-partial','rest-before-expiry','rest-expired','rest-before-completion' }
    if ($branch -eq 'interruption') { $points += 'rest-interrupted','rest-restarted','rest-first','rest-second','rest-third' }
    $data = [ordered]@{}
    foreach ($point in $points) {
        $state = $store.Load("$restored/$point.ddsave")
        $life = $state.Lives | Where-Object ActorId -eq $hero
        $position = $state.Actors | Where-Object Id -eq $hero
        $data[$point] = [ordered]@{Wire=$state.WireSchemaVersion; Base=$state.SchemaVersion; Revision=$state.Revision
            Clock=$state.RuleClock.ToString(); Combat=$state.InventoryCombat; Cell=@($position.X,$position.Y)
            Hp=$life.Hp; MaxHp=$life.MaximumHp; TempHp=$life.TemporaryHp; Wounds=$life.LinkedInjuries; Prone=$life.Prone
            RNG=$state.RandomState; Grant=$state.ConsumeDecay; Rests=$state.ShortRests
            BenefitsUsed=[Decennium.Foundation.ShortRestBerth]::BenefitsUsed($state)}
    }
    Require ($data.continued.Wire -eq 103 -and $data.continued.Base -eq 90 -and $data.continued.Revision -eq 202 -and
        $data.continued.Clock -eq '113481/2' -and ($data.continued.Cell -join ',') -eq '0,1' -and $data.continued.Hp -eq 26 -and
        $data.continued.TempHp -eq 3 -and !$data.continued.Combat) "$branch missed actual predecessor arrival."
    $end = $data.'rest-completed'
    Require ($end.Rests[-1].Outcome -eq 'Completed' -and $end.Rests[-1].HitDiceSpent -eq 0 -and
        $end.Rests[-1].Healing -eq 0 -and $end.Rests[-1].RewardRandomWords -eq 0 -and $end.Hp -eq 26 -and
        $end.TempHp -eq 0 -and ($data.'rest-continued'.Cell -join ',') -eq '0,0') "$branch rest reward or paid continuation differs."
    if ($branch -ne 'interruption') {
        Require ($end.Clock -eq '120681/2' -and $end.BenefitsUsed -eq 1 -and $end.Rests[0].Benefit -eq 'Eligible' -and
            $end.Rests[0].WarriorStrainReduction -eq 'Eligible' -and $end.Rests[0].WarriorStrainAfter -eq 0) 'First completion timing/cadence differs.'
    }
    if ($branch -eq 'completion') {
        Require ($data.'rest-before-expiry'.TempHp -eq 3 -and $data.'rest-expired'.Clock -eq '120653/2' -and
            $data.'rest-expired'.TempHp -eq 0 -and $data.'rest-expired'.Rests[0].Outcome -eq 'Active' -and
            $data.'rest-before-completion'.Rests[0].Outcome -eq 'Active') 'Expiry/rest ordering differs.'
    }
    if ($branch -eq 'interruption') {
        Require ($data.'rest-interrupted'.Rests[0].Interruption -eq 'Explicit' -and $data.'rest-interrupted'.BenefitsUsed -eq 0 -and
            $data.'rest-first'.BenefitsUsed -eq 1 -and $data.'rest-second'.BenefitsUsed -eq 2 -and $data.'rest-third'.BenefitsUsed -eq 2 -and
            $data.'rest-third'.Rests[-1].Benefit -eq 'Ineligible' -and $data.'rest-third'.Rests[-1].WarriorStrainReduction -eq 'Ineligible') 'Interruption/restart or third-rest control differs.'
        $restart = $data.'rest-restarted'.Rests[-1]
        Require ($restart.DueAt.Equals($restart.StartedAt.AddSeconds(3600))) 'Restart retained interrupted progress.'
    }
    $branches[$branch] = [ordered]@{Runs=$checks; DirectCheckpoints=$digests; States=$data; Final=(Digest "$restored/rest-continued.ddsave")}
}
$split = $branches.completion.States.'rest-completed'
$whole = $branches.whole.States.'rest-completed'
foreach ($property in 'Clock','Hp','MaxHp','TempHp','Prone','RNG','BenefitsUsed') {
    Require ($split[$property] -eq $whole[$property]) "Clock partition changed $property."
}
Require ($split.Grant.EndedAt.Equals($whole.Grant.EndedAt) -and $split.Rests[0].DueAt.Equals($whole.Rests[0].DueAt)) 'Clock partition changed causal deadlines.'
[ordered]@{Status='PASS'; Branches=$branches; ClockPartitions='PASS; different input receipts retain their distinct history'} |
    ConvertTo-Json -Depth 18 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: public Short Rest, interruption, cadence, paid continuation and three-path replay in $Run"
