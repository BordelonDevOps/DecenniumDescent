param([string]$AssemblyRoot,[string]$Launcher,[string]$Run,[switch]$ReuseConsole)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Launcher=(Resolve-Path -LiteralPath $Launcher).Path
$Run=(New-Item -ItemType Directory -Force -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require($condition,$message) { if (!$condition) { throw $message } }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Start-Cleric { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample()) }
$inputs=@(Get-Content "$PSScriptRoot/walkthrough.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
$checks=[ordered]@{}
foreach ($mode in 'Restored','Uninterrupted') {
    $folder=(New-Item -ItemType Directory -Force "$Run/$mode").FullName
    $trace=@($inputs | Where-Object { $mode -eq 'Restored' -or $_.op -ne 'load' })
    if (!$ReuseConsole) {
        $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$folder/inputs.jsonl" -Encoding utf8
        Push-Location $folder
        try { & $Launcher -ClericCompanion -AssemblyRoot $AssemblyRoot -InputPath "$folder/inputs.jsonl" | Set-Content "$folder/responses.jsonl" -Encoding utf8 }
        finally { Pop-Location }
    }
    $responses=@(Get-Content "$folder/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
    Require ($responses.Count -eq $trace.Count) "$mode response count differs."
    $revision=0; $hashes=[ordered]@{}
    for ($i=0; $i -lt $trace.Count; $i++) {
        $request=$trace[$i]; $response=$responses[$i]
        if ($request.op -eq 'view') {
            Require ($response.Revision -eq $revision) "$mode view has stale revision."
            $clerics=@($response.Actors | Where-Object { $null -ne $_.Cleric })
            if ($request.seat -eq 'FirstOpponent') { Require ($clerics.Count -eq 0) 'Foreign seat disclosed class/resource ownership.' }
            else {
                Require ($clerics.Count -eq 1 -and $clerics[0].Position.Id -eq 'TEST_ONLY.companion') 'Owned Cleric projection missing.'
                $cleric=$clerics[0].Cleric
                Require ($cleric.ClassLevel -eq 1 -and $cleric.MaximumRp -eq 3 -and $cleric.OwnedCards.Count -eq 4 -and
                    $cleric.CurrentRp -eq $(if ($revision -lt 132) {3} else {1}) -and $cleric.UnsupportedCapabilities -contains 'Conviction') 'Class/RP view differs.'
            }
            continue
        }
        $expected=switch ($request.op) {
            'save' { $hashes[$request.path]=Digest "$folder/$($request.path)"; 'Saved' }
            'load' { 'Restored' }
            default { if ($request.expect) { $request.expect } else { $revision++; 'Committed' } }
        }
        Require ($response.Response -ceq $expected) "$mode input $i ($($request.id)) expected $expected; got $($response.Response)."
        if ($request.op -notin 'save','load' -and $null -ne $response.Revision) {
            Require ($response.Revision -eq $revision) "$mode revision differs at input $i."
        }
    }
    foreach ($name in @($hashes.Keys | Where-Object { $_ -like '*-after.ddsave' })) {
        Require ($hashes[$name] -ceq $hashes[$name.Replace('-after.ddsave','-before.ddsave')]) "$mode denial/retry changed $name."
    }
    $checks[$mode]=[ordered]@{Inputs=$trace.Count;Committed=$revision;Checkpoints=$hashes}
}
$store=[Decennium.Foundation.FileSaveStore]::new(); $marks=@{}
foreach ($name in $checks.Restored.Checkpoints.Keys) {
    Require ($checks.Restored.Checkpoints[$name] -ceq $checks.Uninterrupted.Checkpoints[$name]) "Restore changed $name."
    $s=$store.Load("$Run/Restored/$name")
    if (!$marks.ContainsKey($s.Revision)) { $marks[$s.Revision]=[Collections.Generic.List[string]]::new() }
    $marks[$s.Revision].Add($name)
}
$session=Start-Cleric; $digests=[ordered]@{}
function Save-Marks([long]$revision) {
    if (!$marks.ContainsKey($revision)) { return }
    foreach ($name in $marks[$revision]) {
        $path="$Run/receipt-$name"; $session.Save($path); $digests[$name]=Digest $path
        Require ($digests[$name] -ceq $checks.Restored.Checkpoints[$name]) "Receipt replay differs at $name."
    }
}
Save-Marks 0
$final=$store.Load("$Run/Restored/continued.ddsave")
foreach ($receipt in $final.Receipts) {
    $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
    if ($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { $result=$session.AdvanceAutomaticDefender() }
    elseif ($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $result=$session.SubmitSessionCommand($command) }
    else { $seat=if ($command.Actor -eq 'TEST_ONLY.third-combatant') {'FirstOpponent'} else {'Player'}; $result=$session.Submit($seat,$command) }
    Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "Receipt replay failed at $($receipt.Revision)."
    Save-Marks $receipt.Revision
}
Require ($digests.Count -eq $checks.Restored.Checkpoints.Count) 'Receipt replay missed a checkpoint.'
$data=[ordered]@{}
foreach ($point in 'initial','first-encounter-ended','prepared','entry','approach','opportunity-pending','admitted','injured','before-payment','paid','later-action','defeated','exited','continued') {
    $s=$store.Load("$Run/Restored/$point.ddsave")
    $data[$point]=[ordered]@{Wire=$s.WireSchemaVersion;Base=$s.SchemaVersion;Revision=$s.Revision;Clock=$s.RuleClock.ToString();Combat=$s.InventoryCombat
        RNG=$s.RandomState;Lives=$s.Lives;Characters=$s.Characters;Class=$s.ClericEntry;Pools=$s.ResonancePools;Healing=$s.HealingRites
        HitDice=$s.CharacterHitDice;Intervals=$s.WorldIntervals;Reinforcement=$s.Reinforcement;Batch=$s.ConnectedBatch;Doses=$s.AlchemyDoses
        Positions=$s.Actors;Grants=$s.CharacterFeatureGrants;SelectedCards=$s.InitialClassSelections;Conditions=$s.Conditions}
}
$initial=$data.initial; $prepared=$data.prepared; $injured=$data.injured; $paid=$data.paid; $later=$data.'later-action'; $continued=$data.continued
Require ($initial.Wire -eq 105 -and $initial.Base -eq 90 -and $initial.Class.PointBuyCost -eq 17 -and
    $initial.Pools[0].Current -eq 3 -and $initial.Pools[0].InitialFunding.PolicyId -eq 'TEST_ONLY.cleric-initial-rp3' -and
    !$initial.Class.ConvictionSupported -and $initial.HitDice[0].DieSize -eq 8) 'Initial class/funding facts differ.'
Require ($prepared.Doses.Count -eq 6 -and $prepared.Healing.Count -eq 0 -and $prepared.Pools[0].Current -eq 3 -and
    $data.entry.Combat -and $data.admitted.Reinforcement.Admission -and ($injured.Lives | Where-Object ActorId -eq 'TEST_ONLY.companion').Hp -eq 7) 'Connected acquisition/preparation/reinforcement/injury witness missing.'
$heal=$paid.Healing[0]
Require ($paid.Healing.Count -eq 1 -and $heal.RpBefore -eq 3 -and $heal.RpPaid -eq 2 -and $heal.RpAfter -eq 1 -and
    $heal.HpBefore -eq 7 -and $heal.HpAfter -eq 8 -and $heal.Die -eq 3 -and $heal.Modifier -eq 2 -and
    $heal.RolledPotential -eq 5 -and $heal.ActualGain -eq 1 -and $heal.WordsConsumed -eq 1 -and
    $paid.RNG -ne $data.'before-payment'.RNG -and ($paid.Intervals | Where-Object ActorId -eq 'TEST_ONLY.companion').ActionSpent) 'Real paid heal differs.'
Require ($later.Pools[0].Current -eq 1 -and !($later.Intervals | Where-Object ActorId -eq 'TEST_ONLY.companion').ActionSpent -and
    !$continued.Combat -and $continued.Pools[0].Current -eq 1 -and $continued.Healing.Count -eq 1 -and
    ($continued.Positions | Where-Object Id -eq 'TEST_ONLY.actor').Y -eq 1 -and $continued.Revision -eq 181) 'Finite denial or paid continuation missing.'
[ordered]@{Status='PASS';ReusedObservedConsole=[bool]$ReuseConsole;Runs=$checks;ReceiptCheckpoints=$digests;States=$data;Final=(Digest "$Run/Restored/continued.ddsave")} |
    ConvertTo-Json -Depth 24 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: connected Cleric class/RP/payment, denial and three-path evidence in $Run"
