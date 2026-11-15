param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ContinuedSave,[Parameter(Mandatory)][string]$UnseenHideSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($value,[string]$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
$store=[Decennium.Foundation.FileSaveStore]::new();$rows=[Collections.Generic.List[object]]::new()
function Reject-Forgery($original,$candidate,[string]$name){
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
    $session.Restore($original)
    $valid=Join-Path $Run ($name+'-valid.ddsave');$session.Save($valid)
    Require ((Digest $valid)-ceq(Digest $original)) 'Valid historical consumer did not restore exactly'
    $forged=Join-Path $Run ($name+'-forged.ddsave');$store.Save($forged,$candidate)
    $rejected=$false;$message=''
    try{$session.Restore($forged)}catch{if($_.Exception.GetBaseException()-isnot[ArgumentException]){throw};$rejected=$true;$message=$_.Exception.GetBaseException().Message}
    Require $rejected ('Historical consumer forgery accepted: '+$name)
    $after=Join-Path $Run ($name+'-unchanged.ddsave');$session.Save($after)
    Require ((Digest $after)-ceq(Digest $original)) 'Rejected restore changed live state'
    $rows.Add(@{name=$name;original=$original;originalSha256=(Digest $original);forgedSha256=(Digest $forged);unchangedSha256=(Digest $after);stage='structural encode passes; strict restore rejects';message=$message})
}
$ContinuedSave=(Resolve-Path -LiteralPath $ContinuedSave).Path
$source=$store.Load($ContinuedSave);$candidate=$source.Copy();$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
Require (!$source.InventoryCombat-and![Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($source,$hero).View().Has([Decennium.Foundation.Laboratory.ConditionKind]::Frightened)) 'Main historical attack requires actual closure and ended fear'
$index=-1
for($i=0;$i-lt$candidate.MeleeAttacks.Count;$i++){
    $a=$candidate.MeleeAttacks[$i];if($a.AttackerId-eq$hero-and$a.Attack.First-eq11-and$a.Attack.Second-eq16-and$a.Attack.Selected-eq11){$index=$i;break}
}
Require ($index-ge0) 'Actual frightened attack not found'
$a=$candidate.MeleeAttacks[$index];$r=$a.Attack
$forgedRoll=[Decennium.Foundation.CombatAttackRoll]::new($r.First,$r.Second,$r.Selected,($r.Modifier+1),$r.ArmorClass,$r.Hit,$r.Critical,$r.RandomBefore,$r.RandomAfter,$r.Words)
$candidate.MeleeAttacks[$index]=[Decennium.Foundation.MeleeAttackRecord]::new($a.Id,$a.Revision,$a.ResolvedRevision,$a.TurnOrdinal,$a.AttackerId,$a.TargetId,$a.WeaponId,$a.At,$a.Instruction,$forgedRoll,$a.Damage,$a.Opportunity,$a.PressInstruction)
Reject-Forgery $ContinuedSave $candidate 'ended-fear-old-attack-modifier'
$UnseenHideSave=(Resolve-Path -LiteralPath $UnseenHideSave).Path
$source=$store.Load($UnseenHideSave);$candidate=$source.Copy();$a=$candidate.ObservationActions[-1]
Require ($a.Kind-eq'Hide'-and$a.Second-eq0-and$a.WordsConsumed-eq1) 'Actual unseen source Hide not found'
$candidate.ObservationActions[-1]=[Decennium.Foundation.ObservationActionRecord]::new($a.Id,$a.ActorId,$a.TargetId,$a.Kind,$a.Outcome,$a.At,$a.Revision,$a.X,$a.Y,$a.First,$a.Second,$a.Natural,($a.Modifier+1),($a.Total+1),$a.Selection,$a.RandomBefore,$a.RandomAfter,$a.WordsConsumed)
Reject-Forgery $UnseenHideSave $candidate 'unseen-fear-old-hide-modifier'
[ordered]@{status='PASS';assemblyRoot=$AssemblyRoot;controls=@($rows);scope='Historical causal consumer controls; no altered state is represented as gameplay.'}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count) additional historical consumer forgeries rejected unchanged."
