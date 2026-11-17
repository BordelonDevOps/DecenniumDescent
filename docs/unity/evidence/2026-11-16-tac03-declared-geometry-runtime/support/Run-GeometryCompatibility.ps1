param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh compatibility suite'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$bishop=Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support'
$recovery=Join-Path $PSScriptRoot '../../2026-11-16-exp07-post-recovery/support'
$steps=@(
    @{name='compatibility95-110';script=(Join-Path $bishop 'Test-BishopLegacyCompatibility.ps1')},
    @{name='legacy95-110-views';script=(Join-Path $recovery 'Test-LegacyConsoleProjection.ps1')},
    @{name='wire111';script=(Join-Path $bishop 'Test-Wire111Continuations.ps1')},
    @{name='wire112';script=(Join-Path $PSScriptRoot 'Test-Wire112Continuations.ps1')}
)
$binding=Start-GeometryExecutionBinding $Run @($PSCommandPath,(Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'),
    (Join-Path $recovery 'Test-Compatibility.ps1'),(Join-Path $bishop 'Bishop-ViewProjection.ps1'),$steps[0].script,$steps[1].script,$steps[2].script,$steps[3].script)
$report=[ordered]@{status='FAIL';startedUtc=[DateTime]::UtcNow.ToString('o');steps=@()}
try {
    foreach($step in $steps){
        $arguments=@('-NoProfile','-File',$step.script,'-AssemblyRoot',$AssemblyRoot,'-Run',(Join-Path $Run $step.name))
        if($step.name-eq'legacy95-110-views'){$arguments+=@('-CompatibilityRoot',(Join-Path $Run 'compatibility95-110'))}
        & pwsh @arguments
        if($LASTEXITCODE-ne0){throw "Compatibility step failed: $($step.name)"}
        $report.steps+=@{name=$step.name;exitCode=0;completedUtc=[DateTime]::UtcNow.ToString('o')}
        $report|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
    }
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $binding;$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
