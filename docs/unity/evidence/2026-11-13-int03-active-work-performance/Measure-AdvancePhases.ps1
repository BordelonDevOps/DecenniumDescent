param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Baseline,
    [Parameter(Mandatory)][string]$Output
)
$ErrorActionPreference='Stop'
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$store=[Decennium.Foundation.FileSaveStore]::new()
$results=[ordered]@{}
foreach ($profile in 'Default','FishingTrap') {
    $session=if ($profile -eq 'Default') { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start() }
        else { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap() }
    $pre="$Baseline/$profile/pre-submit.ddsave"
    $post="$Baseline/$profile/post-submit.ddsave"
    $reference=$store.Load($post)
    $command=[Decennium.Foundation.CommandHistory]::Read(($reference.Receipts | Where-Object Id -eq 'i-94'))
    $session.Restore($pre)
    [Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Reset()
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $public=$session.SubmitSessionCommand($command)
    $view=$session.View('Player')
    $publicMs=$watch.Elapsed.TotalMilliseconds
    $publicPhases=[Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Results()
    [Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Boundaries() |
        Set-Content (Join-Path (Split-Path $Output) "$profile-public-boundaries.txt") -Encoding utf8
    $save=Join-Path (Split-Path $Output) "$profile-diagnostic.ddsave"
    $session.Save($save)
    if ($public.Response -ne 'Committed' -or $view.Revision -ne 104 -or (Get-FileHash $save).Hash -cne (Get-FileHash $post).Hash) {
        throw "The instrumented $profile execution changed canonical output."
    }
    $policy=$session.GetType().GetField('policy',[Reflection.BindingFlags]'NonPublic,Instance').GetValue($session)
    $candidate=$store.Load($pre)
    [Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Reset()
    $watch.Restart()
    $failure=$policy.Resolve($candidate,$command)
    $directMs=$watch.Elapsed.TotalMilliseconds
    if ($null -ne $failure) { throw $failure }
    [Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Boundaries() |
        Set-Content (Join-Path (Split-Path $Output) "$profile-reference-boundaries.txt") -Encoding utf8
    $results[$profile]=[ordered]@{PublicMs=$publicMs; PublicPhases=$publicPhases; DirectResolverMs=$directMs
        DirectPhases=[Decennium.Foundation.Laboratory.AdvancePhaseProbe]::Results()
        FinalSha256=(Get-FileHash $save).Hash.ToLowerInvariant()}
}
[ordered]@{Status='PASS'; Instrumented=$true; Profiles=$results} | ConvertTo-Json -Depth 7 | Set-Content $Output -Encoding utf8
Get-Content $Output
