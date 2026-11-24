param([Parameter(Mandatory)][string]$AssemblyRoot, [Parameter(Mandatory)][string]$ResultsDirectory, [switch]$LegacyChecks, [switch]$UtilityChecks, [switch]$SpellChecks, [switch]$BishopChecks, [switch]$RecoveryChecks, [switch]$ConsecrationChecks, [switch]$CareChecks, [switch]$FearRepertoireChecks, [switch]$StabilizationChecks, [switch]$AdvancementChecks, [switch]$ObservationChecks, [string]$NamedCasesFile = '')
$ErrorActionPreference = 'Stop'
if (([int][bool]$LegacyChecks+[int][bool]$UtilityChecks+[int][bool]$SpellChecks+[int][bool]$BishopChecks+[int][bool]$RecoveryChecks+[int][bool]$ConsecrationChecks+[int][bool]$CareChecks+[int][bool]$FearRepertoireChecks+[int][bool]$StabilizationChecks+[int][bool]$AdvancementChecks+[int][bool]$ObservationChecks+[int][bool]$NamedCasesFile) -gt 1) { throw 'Choose one checkpoint case group.' }
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$ResultsDirectory = [IO.Path]::GetFullPath($ResultsDirectory)
if (Test-Path -LiteralPath $ResultsDirectory) { throw 'Use a new results directory.' }
$null = New-Item -ItemType Directory -Path $ResultsDirectory
$compiled = Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw | ConvertFrom-Json
if ($compiled.coreCompilation -ne 'PASS') { throw 'A successful compiled candidate is required.' }
foreach ($part in 'Core','Persistence','LabModel','HeadlessTests') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll") }
$names = @('int05_read_guard_detects_caught_execution_attempts',
    'int05_genuine_concentration_assessment_execution_restore',
    'int05_read_context_owner_generation_and_failure_isolation',
    'int05_materialized_conditions_strict_lookup_and_scope_cleanup',
    'int05_private_canonical_comparison_preserves_validated_codec')
if ($LegacyChecks) {
    $names = @('command_id_reuse_with_new_payload_rejected','stale_command_has_no_effect',
        'unauthorized_actor_has_no_effect','revocation_applies_to_retries','malformed_commands_are_bounded',
        'clock_requires_host_permission','rng_has_known_versioned_sequence',
        'tac08_old_profile_rejects_new_casting_payloads_without_mutation',
        'chr03_bishop_request_cardinality_and_old_profile_denial',
        'tac08_actual_cast_authority_payload_and_source_denials')
}
if ($UtilityChecks) {
    $names = @('int05_genuine_aura_focus_assessment_ordinary_context',
        'int05_genuine_concentration_assessment_execution_restore',
        'tac01_ordinary_magic_consumed_strain_sparse_partition_regression',
        'tac08_genuine_earned_detect_guidance_aura_and_paid_focus')
}
if ($SpellChecks) {
    $names = @('int05_genuine_aura_focus_assessment_ordinary_context',
        'tac08_genuine_spare_stabilizes_actual_combat_patient',
        'tac08_genuine_purify_finite_water_and_measured_intake',
        'tac08_actual_cast_authority_payload_and_source_denials',
        'tac08_genuine_first_cast_spends_real_action_and_replays')
}
if ($BishopChecks) {
    $names = @('chr03_bishop_connected_earned_funded_cure_aura_dispel_continue')
}
if ($RecoveryChecks) {
    $names = @('chr02_cleric_connected_injury_payment_restore_and_continuation',
        'chr03_alternate_genuine_paid_radiance_and_continuation',
        'mgt03_long_rest_genuine_first_funding_and_paid_continuation',
        'int05_genuine_cast_assessment_denials_payment_and_retry')
}
if ($ConsecrationChecks) {
    $names = @('chr05_consecration_genuine_paid_zone_rite_and_expiry')
}
if ($CareChecks) {
    $names = @('mgt03_connected_short_rest_deadlines_cadence_interruption_and_restore',
        'tac06_flesh_warden_connected_real_healing_and_rest_replacement',
        'tac06_flesh_warden_choice_interruption_identity_authority_and_forgery',
        'tac06_connected_consume_decay_depletion_healing_and_expiry',
        'tac06_connected_wound_treatment_ordinary_supply_and_strain')
}
if ($FearRepertoireChecks) {
    $names = @('tac05_frightened_connected_activation_restore_and_recharge',
        'tac07_cleric_repertoire_connected_payment_restore_and_denials',
        'tac08_actual_cast_authority_payload_and_source_denials')
}
if ($StabilizationChecks) {
    $names = @('tac06_connected_companion_stabilization_paid_failure_and_absolute_recovery',
        'tac08_genuine_guidance_medicine_stabilization',
        'int05_care_profile_denials_share_native_order')
}
if ($AdvancementChecks) {
    $names = @('chr03_primary_genuine_earned_settlement',
        'character_advancement_fixed_average_grants_cards_and_hit_die_without_healing',
        'soldier_level_four_constitution_asi_recomputes_all_level_hp_without_healing_or_spending_dice',
        'int05_stabilization_profile_and_sealed_stock_order_are_pure')
}
if ($ObservationChecks) {
    $names = @('observation_shared_hide_search_save_replay_and_observer_isolation',
        'exp04_exploration_search_query_payment_cancel_and_conflicts',
        'exp04_exploration_hide_genuine_roll_and_scheduled_payment',
        'exp04_connected_observation_paid_hide_search_combat_and_byte_replay')
}
if ($NamedCasesFile) {
    $names = @(Get-Content -LiteralPath $NamedCasesFile -Raw | ConvertFrom-Json)
    if ($names.Count -eq 0 -or @($names | Where-Object { $_ -isnot [string] -or $_ -notmatch '^[a-z0-9_]+$' }).Count -ne 0) {
        throw 'Named cases must be a nonempty JSON array of exact case names.'
    }
    if (@($names | Select-Object -Unique).Count -ne $names.Count) { throw 'Named cases must be unique.' }
}
$report = [ordered]@{status='RUNNING'; sourceRun=$AssemblyRoot; startedUtc=[DateTime]::UtcNow.ToString('o');
    legacyChecks=[bool]$LegacyChecks;
    utilityChecks=[bool]$UtilityChecks;
    spellChecks=[bool]$SpellChecks;
    bishopChecks=[bool]$BishopChecks;
    recoveryChecks=[bool]$RecoveryChecks;
    consecrationChecks=[bool]$ConsecrationChecks;
    careChecks=[bool]$CareChecks;
    fearRepertoireChecks=[bool]$FearRepertoireChecks;
    stabilizationChecks=[bool]$StabilizationChecks;
    advancementChecks=[bool]$AdvancementChecks;
    observationChecks=[bool]$ObservationChecks;
    requestedCaseNames=@($names);
    sourceHashes=$compiled.sourceHashes; assemblyHashes=@(Get-ChildItem -LiteralPath $AssemblyRoot -Filter '*.dll' | ForEach-Object {
        @{name=$_.Name;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}
    }); cases=@(); unityCompilation='NOT RUN'; moduleAcceptance='OPEN'}
try {
    foreach ($name in $names) {
        $path = Join-Path $ResultsDirectory $name
        $null = New-Item -ItemType Directory -Path $path
        $report.cases += [Decennium.Foundation.Tests.FoundationCases]::Run($name, $path)
        $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ResultsDirectory 'results.json') -Encoding utf8
        Write-Output ($name+': '+$report.cases[-1].Passed)
    }
    $report.status = if ($report.cases.Count -eq $names.Count -and @($report.cases | Where-Object { -not $_.Passed }).Count -eq 0) { 'PASS' } else { 'FAIL' }
} catch { $report.status='FAIL'; $report.error=$_.Exception.ToString() }
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ResultsDirectory 'results.json') -Encoding utf8
    Write-Output ($report.status+': '+$ResultsDirectory)
    foreach($case in $report.cases) { if(-not $case.Passed) { Write-Output ($case.Name+': '+$case.Error) } }
}
if($report.status -ne 'PASS') { exit 1 }
