param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ExpiredCheckSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ExpiredCheckSave=(Resolve-Path -LiteralPath $ExpiredCheckSave).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
$store=[Decennium.Foundation.FileSaveStore]::new();$source=$store.Load($ExpiredCheckSave)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
Require (![Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($source,$hero).View().Has([Decennium.Foundation.Laboratory.ConditionKind]::Frightened)) 'Historical control requires fear actually expired.'
Require ($source.SupplyCacheAttempts.Count-eq1-and$source.SupplyCacheAttempts[0].Natural-eq11) 'Actual affected historical cache check missing.'
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
$session.Restore($ExpiredCheckSave);$session.Save((Join-Path $Run 'valid-restored.ddsave'))
Require ((Digest (Join-Path $Run 'valid-restored.ddsave'))-ceq(Digest $ExpiredCheckSave)) 'Historical valid state failed exact restore.'
$controls=[Collections.Generic.List[object]]::new()
function Reject-Historical($candidate,[string]$name){
    $path=Join-Path $Run ($name+'.ddsave')
    $store.Save($path,$candidate) # Must be structurally admissible; causal restore is the tested gate.
    $rejected=$false;$message=''
    try{$session.Restore($path)}catch{
        if($_.Exception.InnerException-isnot[ArgumentException]-and$_.Exception-isnot[ArgumentException]){throw}
        $rejected=$true;$message=$_.ToString()
    }
    Require $rejected "Historical forgery was accepted: $name"
    $after=Join-Path $Run ($name+'-unchanged.ddsave');$session.Save($after)
    Require ((Digest $after)-ceq(Digest $ExpiredCheckSave)) "Rejected restore changed the live session: $name"
    $controls.Add(@{name=$name;stage='strict causal restore';rejected=$true;message=$message;forgedSha256=(Digest $path);unchangedSha256=(Digest $after)})
}
$candidate=$source.Copy();$a=$candidate.SupplyCacheAttempts[0]
$candidate.SupplyCacheAttempts[0]=[Decennium.Foundation.SupplyCacheAttemptRecord]::new(
    $a.Id,$a.CacheId,$a.ActorId,$a.EquipmentId,$a.Method,$a.StartedAt,$a.EndedAt,$a.Status,12,$a.Modifier,$a.Tactical,$a.AutomaticFailure)
Reject-Historical $candidate 'forged-old-ability-natural'
$candidate=$source.Copy();$index=0;$a=$candidate.FrightenedSaves[$index]
$candidate.FrightenedSaves[$index]=[Decennium.Foundation.FrightenedSaveRecord]::new(
    $a.Id,$a.UseId,$a.TargetId,$a.ApplicationId,$a.Revision,$a.At,$a.Repeat,$a.Dc,($a.Modifier+1),
    $a.First,$a.Second,$a.Natural,$a.Success,$a.AdmissionPrevented,$a.RandomBefore,$a.RandomAfter,$a.WordsConsumed)
Reject-Historical $candidate 'forged-old-save-modifier'
[ordered]@{status='PASS';source=$ExpiredCheckSave;sourceSha256=(Digest $ExpiredCheckSave);assemblyRoot=$AssemblyRoot;
    currentFear='expired';validRestore='byte-identical';controls=@($controls)
}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: valid historical restore and $($controls.Count) causal forgeries rejected unchanged."
