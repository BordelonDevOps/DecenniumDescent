param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path
$launcher=(Resolve-Path "$PSScriptRoot/../../../../engine/tools/Open-ConnectedExpedition.ps1").Path
foreach($name in 'Core','Persistence','LabModel') {
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    $a=[Reflection.Assembly]::LoadFrom($file)
    if ($a.Location -cne $file) { throw "Unexpected assembly location for $name" }
}
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require($value,$message) { if (!$value) { throw $message } }
$inputs=@(Get-Content "$PSScriptRoot/walkthrough.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
$checks='settled','picked','stowed','closed','away','reopened','retrieved','remote','remote-used','stow-continued'
$records=@{}
foreach($name in 'Restored','Uninterrupted') {
    $folder=(New-Item -ItemType Directory -Path "$Run/$name").FullName
    $trace=@($inputs | Where-Object { $name -eq 'Restored' -or $_.op -ne 'load' })
    $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$folder/inputs.jsonl" -Encoding utf8
    Push-Location $folder
    try { & $launcher -StowedVial -AssemblyRoot $AssemblyRoot -InputPath "$folder/inputs.jsonl" | Set-Content "$folder/responses.jsonl" -Encoding utf8 }
    finally { Pop-Location }
    $responses=@(Get-Content "$folder/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
    Require ($responses.Count -eq $trace.Count) "$name response count differs."
    $seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    $revision=0
    for($i=0;$i -lt $trace.Count;$i++) {
        $request=$trace[$i]; $result=$responses[$i]
        $expected=switch($request.op) {
            'save' {'Saved'}
            'load' {'Restored'}
            'view' {''}
            default {
                if($request.id -in 'vial.out-of-reach','vial.closed-retrieve') {'Unavailable'}
                elseif($request.id -and !$seen.Add($request.id)) {'Duplicate'}
                else {'Committed'; $revision++}
            }
        }
        Require ([string]$result.Response -ceq [string]$expected) "$name unexpected response at $i."
        if($request.op -notin 'save','load') { Require ($result.Revision -eq $revision) "$name wrong revision at $i." }
    }
    Require ($revision -eq 168) "$name route did not reach r168."
    $hashes=[ordered]@{}
    foreach($point in $checks) { $hashes[$point]=Digest "$folder/$point.ddsave" }
    Require ((Digest "$folder/rejected-pickup.ddsave") -ceq $hashes.settled -and
        (Digest "$folder/closed-reject.ddsave") -ceq $hashes.away) "$name rejected input changed full bytes."
    $records[$name]=[ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
}
foreach($point in $checks) {
    Require ($records.Restored.Checkpoints[$point] -ceq $records.Uninterrupted.Checkpoints[$point]) "Console replay differs at $point."
}
$store=[Decennium.Foundation.FileSaveStore]::new()
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithStowedVial()
$final=$store.Load("$Run/Restored/stow-continued.ddsave")
$points=@{108='settled';111='picked';112='stowed';113='closed';115='away';116='reopened';117='retrieved';119='remote';120='remote-used';168='stow-continued'}
$direct=[ordered]@{}
foreach($receipt in $final.Receipts) {
    $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
    $result=if($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { $session.AdvanceAutomaticDefender() }
        elseif($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $session.SubmitSessionCommand($command) }
        else { $session.Submit($(if($command.Actor -eq 'TEST_ONLY.third-combatant'){'FirstOpponent'}else{'Player'}),$command) }
    Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "Direct C# diverged at $($receipt.Revision)."
    if($points.ContainsKey([int]$receipt.Revision)) {
        $point=$points[[int]$receipt.Revision]
        $file="$Run/direct-$point.ddsave"
        $session.Save($file)
        $direct[$point]=Digest $file
        Require ($direct[$point] -ceq $records.Restored.Checkpoints[$point]) "Direct C# bytes differ at $point."
    }
}
$hands=[ordered]@{}
foreach($point in 'picked','stowed','closed','away','reopened','retrieved') {
    $state=$store.Load("$Run/Restored/$point.ddsave")
    $v=$state.PortableEquipment | Where-Object Id -eq 'manufacture.order.104.dose0'
    $pack=$state.PortableEquipment | Where-Object Id -eq 'TEST_ONLY.explorer-pack'
    $b=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($state,'TEST_ONLY.actor')
    $hands[$point]=[ordered]@{Revision=$state.Revision;Clock=$state.RuleClock.ToString();Placement=$v.Placement.ToString()
        Parent=$v.ParentId;HeldHands=$v.HeldHands;PackOpen=$pack.Open;Burden=$b}
}
Require ($hands.picked.HeldHands -eq 1 -and $hands.stowed.HeldHands -eq 0 -and !$hands.away.PackOpen -and
    $hands.reopened.PackOpen -and $hands.retrieved.HeldHands -eq 1 -and
    $hands.picked.Burden.Pounds -eq $hands.stowed.Burden.Pounds -and $hands.picked.Burden.Load -eq $hands.stowed.Burden.Load -and
    $hands.reopened.Burden.Pounds -eq $hands.retrieved.Burden.Pounds -and $hands.reopened.Burden.Load -eq $hands.retrieved.Burden.Load) 'Containment changed burden or hands incorrectly.'
$prior=$store.Load("$Run/Restored/remote.ddsave")
$after=$store.Load("$Run/Restored/remote-used.ddsave")
$hero=$prior.Actors | Where-Object Id -eq 'TEST_ONLY.actor'
$life=$prior.Lives | Where-Object ActorId -eq $hero.Id
$vial=$after.AlchemyDoses | Where-Object Id -eq 'manufacture.order.104.dose0'
$body=$after.PortableEquipment | Where-Object Id -eq $vial.Id
$interval=$after.WorldIntervals | Where-Object ActorId -eq $hero.Id
$beforeBurden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($prior,$hero.Id)
$afterBurden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($after,$hero.Id)
Require ($prior.WireSchemaVersion -eq 97 -and $prior.SchemaVersion -eq 90 -and $hero.X -eq 0 -and $hero.Y -eq 3 -and
    $life.Hp -eq $life.MaximumHp -and $interval.ActionSpent -and $vial.ActualHealing -eq 0 -and
    $vial.PotentialHealing -eq ($vial.FirstD4 + $vial.SecondD4 + 2) -and $vial.Spent -and $body.HeldHands -eq 1 -and
    $vial.CustodianId -eq $hero.Id -and !$final.InventoryCombat) 'Remote full-HP tactical use or ordinary continuation differs.'
[ordered]@{Status='PASS'; Wire=$prior.WireSchemaVersion; Base=$prior.SchemaVersion; Profile=$prior.ContentFingerprint
    Console=$records; Direct=$direct; Handling=$hands; Remote=[ordered]@{X=$hero.X;Y=$hero.Y;Hp=$life.Hp;MaximumHp=$life.MaximumHp;
        PaidAction=$interval.ActionSpent; Vial=$vial; Body=$body; BeforeBurden=$beforeBurden; AfterBurden=$afterBurden}
    FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()} |
    ConvertTo-Json -Depth 10 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json" -TotalCount 9
