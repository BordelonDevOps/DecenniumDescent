param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh genesis probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Development genesis/typed-console save-restore and labeled source mechanics only; no connected creature encounter qualification';checks=@();assemblies=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
        Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.executedSources=@($PSCommandPath,(Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1')|ForEach-Object{@{path=[IO.Path]::GetRelativePath($repository,$_);sha256=(Digest $_)}})
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $typed=Join-Path $Run 'typed-genesis.ddsave';$typedRestored=Join-Path $Run 'typed-restored.ddsave'
    $session.Save($typed);$session.Restore($typed);$session.Save($typedRestored)
    Require ((Digest $typed)-ceq(Digest $typedRestored)) 'Typed restore changed bytes.'
    $store=[Decennium.Foundation.FileSaveStore]::new();$state=$store.Load($typed)
    $creature='TEST_ONLY.ferry-wraith';$facts=[Decennium.Foundation.Laboratory.ActorNumericFacts]::ForActor($state,$creature)
    Require ($state.WireSchemaVersion-eq114-and$state.Revision-eq0-and$state.Creatures.Length-eq1-and$state.Characters.Length-eq6-and$state.Actors.Length-eq7) 'Wrong source-origin/genesis envelope.'
    Require (@($state.Characters|Where-Object ActorId -eq $creature).Count-eq0-and$null-eq$facts.ProficiencyBonus-and$facts.BaseArmorClass-eq10) 'Fabricated character/PB/AC.'
    $mods=@(0..5|ForEach-Object{$facts.AbilityModifier([Decennium.Foundation.CharacterAbility]$_)})
    Require (($mods-join',')-eq'1,2,2,-1,0,3') 'Wrong printed ability modifiers.'
    $life=$state.Lives|Where-Object ActorId -eq $creature
    Require ($life.Hp-eq9-and$life.MaximumHp-eq9-and!$life.UsesDeathSaves-and$life.HeldItems.Count-eq0) 'Wrong ordinary-monster source life.'
    $speed=$state.ActorMovement|Where-Object ActorId -eq $creature
    Require ($speed.BaseWalkingSpeed-eq40) 'Wrong source walking speed.'
    $report.checks+=@('Fresh trusted114 genesis has seven actors, six real characters and one source creature','Printed modifiers/AC10/HP9/Speed40; no creature PB/class/held item','Typed verified restore is byte-identical')
    $journal=$state.Conditions|Where-Object Target -eq $creature
    $history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($journal)
    foreach($kind in 'Poisoned','Blinded'){
        $application=[Decennium.Foundation.ConditionApplicationData]::new('mechanical.'+$kind,'mechanical.owner','mechanical.explicit-application',$kind,$null,'mechanical.end',$true)
        $operation=[Decennium.Foundation.ConditionOperation]::Apply('mechanical.apply.'+$kind,$journal.Now,$application)
        $result=$history.Append($operation)
        Require ($result.ApplicationPrevented-eq($kind-eq'Poisoned')) ('Wrong named immunity result for '+$kind)
    }
    $report.checks+='Labeled mechanical applications through actual source journal prevent Poisoned but admit unrelated Blinded; no new player producer claimed'
    $bad=$state.Copy()
    $bad.Characters=@($bad.Characters)+@([Decennium.Foundation.ActorCharacterRecord]::new($creature,'TEST_ONLY.forged-class',[int[]]@(12,14,14,9,11,16),[Decennium.Foundation.CharacterLevelFact[]]@([Decennium.Foundation.CharacterLevelFact]::new('Warrior',9))))
    $rejected=$false
    try{$null=[Decennium.Foundation.SnapshotCodec]::new().Encode($bad)}catch{$rejected=$true;$report.mixedOriginRejection=$_.Exception.GetBaseException().Message}
    Require $rejected 'Mixed character/creature origin encoded.'
    $report.checks+='Mixed character/creature origin is rejected by actual snapshot validation'
    $console=Join-Path $Run 'console-genesis.ddsave';$consoleRestored=Join-Path $Run 'console-restored.ddsave'
    $inputs=Join-Path $Run 'inputs.jsonl'
    @(@{op='save';path=$console},@{op='load';path=$console},@{op='save';path=$consoleRestored})|ForEach-Object{ConvertTo-Json -InputObject $_ -Compress}|Set-Content -LiteralPath $inputs -Encoding utf8
    & pwsh -NoProfile -File (Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1') -FerryWraith -AssemblyRoot $AssemblyRoot -InputPath $inputs > (Join-Path $Run 'responses.jsonl') 2> (Join-Path $Run 'stderr.txt')
    Require ($LASTEXITCODE-eq0-and(Get-Item -LiteralPath (Join-Path $Run 'stderr.txt')).Length-eq0) 'Console genesis failed.'
    $responses=@(Get-Content -LiteralPath (Join-Path $Run 'responses.jsonl')|ForEach-Object{ConvertFrom-Json $_})
    Require (($responses.Response-join',')-ceq'Saved,Restored,Saved') 'Console did not save/restore/save.'
    Require ((Digest $typed)-ceq(Digest $console)-and(Digest $typed)-ceq(Digest $consoleRestored)) 'Independent console/typed genesis differs.'
    $session.Save((Join-Path $Run 'typed-after-probes.ddsave'))
    Require ((Digest $typed)-ceq(Digest (Join-Path $Run 'typed-after-probes.ddsave'))) 'Read/mechanical/forgery probes changed the live session.'
    $report.checks+=@('Independent public console fresh genesis and restore match typed bytes','Source-mechanical/read/forgery probes leave actual session bytes unchanged')
    $report.genesisSha256=Digest $typed
    $report.status='PASS_DEVELOPMENT_GENESIS_ONLY'
} catch {$report.error=$_.ToString();throw}
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
    Write-Output ($report.status+': '+$Run)
}
