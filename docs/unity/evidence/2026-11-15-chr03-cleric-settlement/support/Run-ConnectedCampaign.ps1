param([Parameter(Mandatory)][string]$RegressionRoot,[Parameter(Mandatory)][ValidateSet('primary','alternate')][string]$Campaign,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$RegressionRoot=(Resolve-Path -LiteralPath $RegressionRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$case=if($Campaign-eq'primary'){'chr03_primary_genuine_earned_settlement'}else{'chr03_alternate_genuine_paid_radiance_and_continuation'}
$group=if($Campaign-eq'primary'){'shardF'}else{'shardA'}
$journal=Join-Path $RegressionRoot ($group+'.jsonl')
$worker=@(Get-Content -LiteralPath (Join-Path $RegressionRoot 'processes.json') -Raw|ConvertFrom-Json)|Where-Object group -eq $group
while($true){
    $result=if(Test-Path -LiteralPath $journal){Get-Content -LiteralPath $journal|ConvertFrom-Json|Where-Object Name -eq $case}else{$null}
    if($null-ne$result){if(!$result.Passed){throw "Campaign prerequisite failed: $($result.Error)"};break}
    if($null-eq(Get-Process -Id $worker.pid -ErrorAction SilentlyContinue)){throw 'Original regression worker exited before campaign result'}
    Start-Sleep -Seconds 10
}
$assemblies=Join-Path $RegressionRoot 'execution-assemblies'
$checkpoints=Join-Path (Join-Path $RegressionRoot 'saves') $case
$final=Join-Path $checkpoints ('cleric-'+$Campaign+'-continued.ddsave')
& (Join-Path $PSScriptRoot 'Export-ClericTrace.ps1') -AssemblyRoot $assemblies -FinalSave $final -CheckpointDirectory $checkpoints -Run (Join-Path $Run 'trace')
& (Join-Path $PSScriptRoot 'Test-ClericPaths.ps1') -AssemblyRoot $assemblies -TraceRoot (Join-Path $Run 'trace') -Run (Join-Path $Run 'paths')
