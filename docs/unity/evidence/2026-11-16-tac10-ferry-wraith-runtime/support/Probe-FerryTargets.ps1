param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh target integration probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Development target/check integration and existing consumer regressions; not full TAC-10 qualification';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();cases=@();executedScript=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}}
try {
    foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $available=[Decennium.Foundation.Tests.FoundationCases]::Names()
    $selected=@($available|Where-Object{$_ -cmatch '^(tac10_|ability_check_|character_rule_facts_|character_state_facts_|character_skill_training_queries_)'})
    $selected+=@('repeating_crossbow_attack_uses_shared_action_critical_d10_damage_and_one_bolt',
        'repeating_crossbow_attack_uses_character_facts_after_stale_cache_save_restore_and_replay',
        'periodic_rider_tick_uses_next_target_start_and_survives_save_replay',
        'periodic_rider_family_arbitration_rolls_winner_then_consumes_loser',
        'overwatch_registered_bleed_choice_uses_shared_periodic_record_and_calendar',
        'overwatch_push_uses_recorded_strength_save_and_forced_move',
        'hunting_trap_pending_overwatch_push_is_gated_before_save_and_then_resolves',
        'soldier_suppression_fire_records_one_shared_damage_roll_and_saves_then_expires_slow_at_soldier_end',
        'soldier_suppression_fire_success_halves_shared_damage_without_slow_or_attack_roll')
    foreach($name in $selected){if($available -cnotcontains $name){throw "Missing case: $name"}}
    if($selected.Count -ne 22){throw ('Unexpected selected case count: '+$selected.Count)}
    $report.selected=$selected
    foreach($name in $selected){
        $result=[Decennium.Foundation.Tests.FoundationCases]::Run($name,(Join-Path $Run $name));$report.cases+=@($result)
        $result|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run ($name+'.result.json')) -Encoding utf8
        Write-Output (($result.Passed.ToString())+': '+$name)
        if(!$result.Passed){throw $result.Error}
    }
    $report.status='PASS_DEVELOPMENT_TARGET_INTEGRATION_ONLY'
} catch {$report.error=$_.ToString();throw}
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
    Write-Output ($report.status+': '+$Run)
}
