param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CaseRoot,
    [Parameter(Mandatory)][string]$Run,[ValidateSet(0,1)][int]$Group=0)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$CaseRoot=(Resolve-Path -LiteralPath $CaseRoot).Path
$Run=[IO.Path]::GetFullPath($Run)
$campaigns=@(
    @('sanctuary','tac08_genuine_sanctuary_pending_retarget_forgo_and_restore','tac08-sanctuary-retargeted.ddsave'),
    @('purify','tac08_genuine_purify_finite_water_and_measured_intake','tac08-purified-water-consumed.ddsave'),
    @('detect','tac08_genuine_earned_detect_guidance_aura_and_paid_focus','tac08-detect-expired-continuation.ddsave'),
    @('guidance','tac08_genuine_guidance_hide_choice_and_no_check_search','tac08-guidance-hidden.ddsave'),
    @('concentration','tac08_genuine_concentration_damage_uses_actual_packet','tac08-concentration-damage-ended.ddsave'),
    @('focus','tac08_focus_handling_and_unsafe_consumable_denials','tac08-focus-handling.ddsave'),
    @('refrain','tac08_genuine_cadence_grounding_advancement_and_passive_concentration','tac08-refrain-after-continuing-cast.ddsave'),
    @('sanctuary-forgo','tac08_genuine_sanctuary_carried_opportunity_forgo','tac08-sanctuary-second-parent-resumed.ddsave')
)
for($index=$Group;$index-lt$campaigns.Count;$index+=2){
    $route,$case,$final=$campaigns[$index]
    $directory=Join-Path $CaseRoot $case;$trace=Join-Path (Join-Path $Run 'traces') $route
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'Export-CastingTrace.ps1') -AssemblyRoot $AssemblyRoot `
        -FinalSave (Join-Path $directory $final) -CheckpointDirectory $directory -Run $trace
    if($LASTEXITCODE-ne0){throw "Trace export failed for $route"}
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'Test-CastingPaths.ps1') -AssemblyRoot $AssemblyRoot `
        -TraceRoot $trace -Run (Join-Path (Join-Path $Run 'paths') $route)
    if($LASTEXITCODE-ne0){throw "Five-path execution failed for $route"}
}
Write-Output "PASS: amended connected campaign group $Group."
