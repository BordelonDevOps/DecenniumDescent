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
$checks='settled','picked','remote','remote-used','vial-continued'
$records=@{}
foreach($name in 'Restored','Uninterrupted') {
    $folder=(New-Item -ItemType Directory -Path "$Run/$name").FullName
    $trace=@($inputs | Where-Object { $name -eq 'Restored' -or $_.op -ne 'load' })
    $trace | ForEach-Object { ConvertTo-Json $_ -Depth 8 -Compress } | Set-Content "$folder/inputs.jsonl" -Encoding utf8
    Push-Location $folder
    try { & $launcher -CarriedVial -AssemblyRoot $AssemblyRoot -InputPath "$folder/inputs.jsonl" | Set-Content "$folder/responses.jsonl" -Encoding utf8 }
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
                if($request.id -in 'vial.out-of-reach','vial.remote-sibling','vial.spent-again') {'Unavailable'}
                elseif($request.id -and !$seen.Add($request.id)) {'Duplicate'}
                else {'Committed'; $revision++}
            }
        }
        Require ([string]$result.Response -ceq [string]$expected) "$name unexpected response at $i."
        if($request.op -notin 'save','load') { Require ($result.Revision -eq $revision) "$name wrong revision at $i." }
    }
    Require ($revision -eq 164) "$name route did not reach r164."
    $hashes=[ordered]@{}
    foreach($point in $checks) { $hashes[$point]=Digest "$folder/$point.ddsave" }
    Require ((Digest "$folder/rejected-pickup.ddsave") -ceq $hashes.settled -and
        (Digest "$folder/rejected-sibling.ddsave") -ceq $hashes.remote) "$name rejected input changed full bytes."
    $records[$name]=[ordered]@{Inputs=$trace.Count; Committed=$revision; Checkpoints=$hashes}
}
foreach($point in $checks) {
    Require ($records.Restored.Checkpoints[$point] -ceq $records.Uninterrupted.Checkpoints[$point]) "Console replay differs at $point."
}
$store=[Decennium.Foundation.FileSaveStore]::new()
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCarriedVial()
$final=$store.Load("$Run/Restored/vial-continued.ddsave")
$points=@{108='settled';111='picked';115='remote';116='remote-used';164='vial-continued'}
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
$prior=$store.Load("$Run/Restored/remote.ddsave")
$after=$store.Load("$Run/Restored/remote-used.ddsave")
$hero=$prior.Actors | Where-Object Id -eq 'TEST_ONLY.actor'
$life=$prior.Lives | Where-Object ActorId -eq $hero.Id
$vial=$after.AlchemyDoses | Where-Object Id -eq 'manufacture.order.104.dose0'
$body=$after.PortableEquipment | Where-Object Id -eq $vial.Id
$interval=$after.WorldIntervals | Where-Object ActorId -eq $hero.Id
$beforeBurden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($prior,$hero.Id)
$afterBurden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($after,$hero.Id)
Require ($prior.WireSchemaVersion -eq 96 -and $prior.SchemaVersion -eq 90 -and $hero.X -eq 0 -and $hero.Y -eq 3 -and
    $life.Hp -eq $life.MaximumHp -and $interval.ActionSpent -and $vial.ActualHealing -eq 0 -and
    $vial.PotentialHealing -eq ($vial.FirstD4 + $vial.SecondD4 + 2) -and $vial.Spent -and $body.HeldHands -eq 1 -and
    $vial.CustodianId -eq $hero.Id -and !$final.InventoryCombat) 'Remote full-HP tactical use or ordinary continuation differs.'
[ordered]@{Status='PASS'; Wire=$prior.WireSchemaVersion; Base=$prior.SchemaVersion; Profile=$prior.ContentFingerprint
    Console=$records; Direct=$direct; Remote=[ordered]@{X=$hero.X;Y=$hero.Y;Hp=$life.Hp;MaximumHp=$life.MaximumHp;
        PaidAction=$interval.ActionSpent; Vial=$vial; Body=$body; BeforeBurden=$beforeBurden; AfterBurden=$afterBurden}
    FinalRevision=$final.Revision; FinalClock=$final.RuleClock.ToString()} |
    ConvertTo-Json -Depth 10 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json" -TotalCount 9
