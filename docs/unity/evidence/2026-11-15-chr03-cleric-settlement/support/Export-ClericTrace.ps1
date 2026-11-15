param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FinalSave,[Parameter(Mandatory)][string]$CheckpointDirectory,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FinalSave=(Resolve-Path -LiteralPath $FinalSave).Path
$CheckpointDirectory=(Resolve-Path -LiteralPath $CheckpointDirectory).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$store=[Decennium.Foundation.FileSaveStore]::new()
$final=$store.Load($FinalSave)
Require ($final.ConnectedClericSettlement-and$final.WireSchemaVersion-eq108) 'The trace requires a genuine earned Cleric settlement snapshot.'
$references=New-Item -ItemType Directory -Path (Join-Path $Run 'reference')
$initial=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericSettlement(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$initial.Save((Join-Path $references.FullName 'initial.ddsave'))
$marks=[Collections.Generic.List[object]]::new()
$marks.Add(@{revision=0;name='initial.ddsave';sha256=(Digest (Join-Path $references.FullName 'initial.ddsave'))})
foreach($file in Get-ChildItem -LiteralPath $CheckpointDirectory -File -Filter 'cleric-*.ddsave'){
    $s=$store.Load($file.FullName)
    if(!$s.ConnectedClericSettlement-or$s.Revision-gt$final.Revision){continue}
    $prefix=$true
    for($i=0;$i-lt$s.Receipts.Count;$i++){
        $a=$s.Receipts[$i];$b=$final.Receipts[$i]
        if($a.Principal-cne$b.Principal-or$a.Id-cne$b.Id-or$a.Fingerprint-cne$b.Fingerprint){$prefix=$false;break}
    }
    if(!$prefix){continue}
    Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $references.FullName $file.Name)
    $marks.Add(@{revision=$s.Revision;name=$file.Name;sha256=(Digest $file.FullName)})
}
Require (@($marks|Where-Object revision -eq $final.Revision).Count-gt0) 'Final checkpoint is absent from the source directory.'
$trace=[Collections.Generic.List[object]]::new()
function Add-Marks([long]$revision){
    foreach($mark in $marks|Where-Object revision -eq $revision|Sort-Object name){
        $trace.Add(@{op='save';path=$mark.name})
        $trace.Add(@{op='load';path=$mark.name})
    }
}
Add-Marks 0
foreach($receipt in $final.Receipts){
    # Export is performed once, outside all execution drivers. The independent typed
    # driver consumes only this retained JSON, never CommandHistory.Read or a save.
    $c=[Decennium.Foundation.CommandHistory]::Read($receipt)
    Require (($null-eq$c.Advancement-or$c.Advancement.UsesClericSettlementReceipt)-and$null-eq$c.Ranged-and$null-eq$c.SuppressionFire-and$null-eq$c.DefensiveFormation-and
        $null-eq$c.ExpeditionAssignment-and$null-eq$c.HarvestSelection-and$null-eq$c.ProspectingExposure-and$null-eq$c.RouteMappingWork-and
        $c.OverwatchRider-eq'None') 'A newly encountered payload requires an explicit typed exporter.'
    if($receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'-and$c.Id.StartsWith('tac10.')){
        $request=@{op='auto';expectedReceiptId=$receipt.Id;expectedRevision=$receipt.Revision}
    }else{
        $operation=if($c.Kind-eq'AdvanceClock'){'clock'}elseif($c.Kind-eq'EndFixedEncounter'){'close'}
            elseif($c.Kind-eq'UseIntimidatingPresence'){'defender-presence'}else{'submit'}
        $request=@{op=$operation;id=$c.Id;actor=$c.Actor;revision=$c.ExpectedRevision;kind=$c.Kind.ToString();target=$c.Target;x=$c.X;y=$c.Y}
        if($operation-eq'submit'){$request.seat=if($c.Actor-eq'TEST_ONLY.third-combatant'){'FirstOpponent'}else{'Player'}}
        if($c.Inventory){$i=$c.Inventory;$request.inventory=@{numerator=$i.Amount.Numerator;denominator=$i.Amount.Denominator;destination=$i.Destination;handling=$i.Handling.ToString()}}
        if($c.Combat){$a=$c.Combat;$request.combat=@{turn=$a.TurnId;weapon=$a.WeaponId;stance=$a.Stance;knockout=$a.Knockout.ToString();choice=$a.Choice;press=$a.PressInstruction.ToString()}}
        if($c.MiningSelection){$m=$c.MiningSelection;$request.mining=@{version=$m.DepositVersionId;categories=@($m.CategoryIds);ability=$m.Ability.ToString();hurried=$m.Hurried;failureVictim=$m.FailureVictimPreference;criticalRecovery=$m.CriticalRecoveryPreference;assistant=$m.AssistantId}}
        if($c.IntimidatingPresence){$request.intimidatingPresence=@{targets=@($c.IntimidatingPresence.TargetIds)}}
        if($c.Advancement){$request.advancement=@{features=@($c.Advancement.FeatureIds);invocationPath=$c.Advancement.InvocationPath;earnedSpell=$c.Advancement.EarnedSpell}}
        if($c.HealingRite){$request.healingRite=@{curePreference=$c.HealingRite.CurePreference.ToString()}}
    }
    $trace.Add($request);Add-Marks $receipt.Revision
}
$trace|ForEach-Object{ConvertTo-Json $_ -Depth 8 -Compress}|Set-Content -LiteralPath (Join-Path $Run 'inputs.jsonl') -Encoding utf8
[ordered]@{status='EXPORTED_NOT_EXECUTED';origin='Actual connected C# command receipts; exporter separate from typed execution.';
    finalSource=$FinalSave;finalSha256=(Digest $FinalSave);revision=$final.Revision;profile='TEST_ONLY.cleric-settlement-v1';seed=8;
    marks=@($marks);inputs=$trace.Count;sourceAssemblyRoot=$AssemblyRoot
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'manifest.json') -Encoding utf8
Write-Output "Exported $($final.Revision) actual commands and $($marks.Count) checkpoints to $Run"
