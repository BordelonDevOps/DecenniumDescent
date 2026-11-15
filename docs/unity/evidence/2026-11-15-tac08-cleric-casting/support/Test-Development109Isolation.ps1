param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$packet=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCasting(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
    [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$cases=@(
    'implementation/focused/tac08_initial_physical_state_and_wire_isolation/tac08-initial.ddsave',
    'implementation/focused/tac08_genuine_first_cast_spends_real_action_and_replays/tac08-after-first-cast.ddsave',
    'review-correction/weapon-boundary/tac08-refrain-after-idle.ddsave'
)
$rows=@();$index=0
foreach($relative in $cases){
    $source=(Resolve-Path -LiteralPath (Join-Path $packet $relative)).Path
    $copy=Join-Path $Run "case-$index-original109.ddsave"
    Copy-Item -LiteralPath $source -Destination $copy
    $before=Join-Path $Run "case-$index-before.ddsave";$after=Join-Path $Run "case-$index-after.ddsave"
    $session.Save($before);$rejected=$false;$reason=''
    try{$session.Restore($copy)}catch [System.ArgumentException]{$rejected=$true;$reason=$_.Exception.Message}
    catch [System.IO.InvalidDataException]{$rejected=$true;$reason=$_.Exception.Message}
    $session.Save($after)
    if(!$rejected-or(Digest $before)-cne(Digest $after)-or(Digest $source)-cne(Digest $copy)){
        throw "Earlier developmental109 was not rejected unchanged: $relative"
    }
    $rows+=@{source=$relative;sourceSha256=(Digest $source);copy=[IO.Path]::GetFileName($copy);
        rejection=$reason;before=[IO.Path]::GetFileName($before);after=[IO.Path]::GetFileName($after);unchangedSha256=(Digest $before)}
    $index++
}
@{status='PASS';profile=[Decennium.Foundation.SpellCastingProfile]::FingerprintPrefix;rejectedUnchanged=$rows.Count;
    cases=$rows;assemblies=@(foreach($part in 'Core','Persistence','LabModel'){@{name=$part;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll"))}})
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count) authentic developmental109 saves rejected unchanged."
