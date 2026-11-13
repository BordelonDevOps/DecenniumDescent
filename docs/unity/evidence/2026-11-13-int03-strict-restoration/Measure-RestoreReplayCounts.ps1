param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Output
)
$ErrorActionPreference='Stop'
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$source=(Resolve-Path (Join-Path $PSScriptRoot '../2026-11-13-int03-active-work-performance/performance')).Path
$probe=[Decennium.Foundation.Laboratory.RestoreReplayProbe]
$results=[ordered]@{}
foreach($profile in 'Default','FishingTrap') {
    $session=if($profile -eq 'Default'){[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()}
        else{[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()}
    $file="$source/$profile/post-submit.ddsave"
    $probe::Reset()
    $session.Restore($file)
    $null=$session.View('Player')
    $copy=Join-Path (Split-Path $Output) "$profile.ddsave"
    $session.Save($copy)
    if((Get-FileHash $copy).Hash -cne (Get-FileHash $file).Hash){throw 'The diagnostic restore changed canonical bytes.'}
    $results[$profile]=[ordered]@{Outer=$probe::Outer; Nested=$probe::Nested; DedicatedSeal=$probe::Seal
        Sha256=(Get-FileHash $copy).Hash.ToLowerInvariant()}
}
[ordered]@{Status='PASS'; Profiles=$results} | ConvertTo-Json -Depth 6 | Set-Content $Output -Encoding utf8
Get-Content $Output
