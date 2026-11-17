param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh combat development probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Development shared damage and selected existing combat regressions only; not TAC-10 connected qualification';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();cases=@();executedScript=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}}
try {
    foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
        Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $selected=@('tac10_ferry_typed_defenses_settle_actual_life_mechanical',
        'condition_combat_petrified_damage_halves_before_life_resolution',
        'condition_combat_stone_pending_knockout_preserves_resolved_damage',
        'condition_combat_event_invalidates_oa_without_spending_reaction',
        'club_knockout_deadline_keeps_fractional_attack_instant',
        'club_late_knockout_equals_conditional_early_instruction',
        'club_declining_knockout_consumes_no_additional_randomness',
        'tac08_genuine_sanctuary_pending_retarget_forgo_and_restore')
    $available=[Decennium.Foundation.Tests.FoundationCases]::Names()
    foreach($name in $selected){if($available -cnotcontains $name){throw "Missing case: $name"}}
    $report.selected=$selected
    foreach($name in $selected){
        $result=[Decennium.Foundation.Tests.FoundationCases]::Run($name,(Join-Path $Run $name))
        $report.cases+=@($result)
        $result|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run ($name+'.result.json')) -Encoding utf8
        Write-Output (($result.Passed.ToString())+': '+$name)
        if(!$result.Passed){throw $result.Error}
    }
    $report.status='PASS_DEVELOPMENT_COMBAT_ONLY'
} catch {$report.error=$_.ToString();throw}
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
    Write-Output ($report.status+': '+$Run)
}
