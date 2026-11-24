param([Parameter(Mandatory)][string]$AssemblyRoot, [Parameter(Mandatory)][string]$ResultsDirectory, [switch]$LegacyChecks, [switch]$UtilityChecks)
$ErrorActionPreference = 'Stop'
if ($LegacyChecks -and $UtilityChecks) { throw 'Choose one checkpoint case group.' }
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
$report = [ordered]@{status='RUNNING'; sourceRun=$AssemblyRoot; startedUtc=[DateTime]::UtcNow.ToString('o');
    legacyChecks=[bool]$LegacyChecks;
    utilityChecks=[bool]$UtilityChecks;
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
