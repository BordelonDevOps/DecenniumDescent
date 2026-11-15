param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CaseRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$CaseRoot=(Resolve-Path -LiteralPath $CaseRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$source=Join-Path $CaseRoot 'tac08-club-after-pickup.ddsave'
$codec=[Decennium.Foundation.SnapshotCodec]::new();$store=[Decennium.Foundation.FileSaveStore]::new()
$snapshot=$store.Load($source);$actor=[Decennium.Foundation.ClericRpProfile]::Actor;$id=[Decennium.Foundation.SpellCastingProfile]::CompanionClubId
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCasting(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
    [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$session.Restore($source)
$before=Join-Path $Run 'forged-drop-before.ddsave';$after=Join-Path $Run 'forged-drop-after.ddsave'
$session.Save($before)
$forged=$snapshot.Copy()
$forged.Clubs=@($forged.Clubs|ForEach-Object{if($_.Id-eq$id){
    [Decennium.Foundation.ClubInstance]::new($_.Id,$_.ProfileId,$_.OwnerId,$_.CustodianId,'',$_.CellX,$_.CellY)
}else{$_}})
$forged.Lives=@($forged.Lives|ForEach-Object{if($_.ActorId-eq$actor){
    [Decennium.Foundation.ActorLifeRecord]::new($_.ActorId,$_.MaximumHp,$_.Hp,$_.TemporaryHp,$_.LinkedInjuries,
        $_.Stable,$_.Dead,$_.UsesDeathSaves,$_.DeathSuccesses,$_.DeathFailures,$_.StableUntil,$_.LastDeathTurn,
        $_.Prone,[string[]]@($_.HeldItems|Where-Object {$_-cne$id}))
}else{$_}})
# This envelope is intentionally structurally consistent: holding and life records agree,
# while no real command or involuntary consequence caused the forged physical drop.
$bytes=$codec.Encode($forged)
$path=Join-Path $Run 'structurally-valid-forged-drop.ddsave';[IO.File]::WriteAllBytes($path,$bytes)
$rejected=$false;$reason=''
try{$session.Restore($path)}catch [System.ArgumentException]{$rejected=$true;$reason=$_.Exception.Message}
catch [System.IO.InvalidDataException]{$rejected=$true;$reason=$_.Exception.Message}
$session.Save($after)
if(!$rejected-or(Digest $before)-cne(Digest $after)){throw 'Strict replay accepted an uncommanded Club possession change or changed the selected session.'}
@{status='PASS';scope='Structurally valid physical forgery rejected by actual supported-save reconstruction; independent of Foundation case count';
    source=$source;sourceSha256=(Digest $source);forgedSha256=(Digest $path);rejectedUnchanged=$true;reason=$reason;
    unchangedSha256=(Digest $before);assemblies=@(foreach($part in 'Core','Persistence','LabModel'){@{name=$part;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll"))}})
}|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output 'PASS: structurally valid uncommanded Club drop rejected unchanged by strict replay.'
