param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh connected probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Fresh current Ferry profile through genuine prefix, paid admission, actual first fire and verified restore; full creature/seal module qualification pending';assemblies=@();cases=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.executedScript=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryFreshFire.executed.ps1')
    $controller=Join-Path $Run 'Probe-FerryController.executed.ps1'
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Probe-FerryController.ps1') -Destination $controller
    $report.controllerScript=@{path=$controller;sha256=(Digest $controller)}
    $report.cases=@([Decennium.Foundation.Tests.FoundationCases]::Run('tac10_ferry_paid_current_epoch_admission_from_fresh_campaign',(Join-Path $Run 'saves')))
    if($report.cases.Count-ne1-or!$report.cases[0].Passed){throw ('Fresh paid campaign failed: '+($report.cases|ConvertTo-Json -Compress))}
    Write-Output 'PASS: fresh current-profile paid admission'
    & pwsh -NoProfile -File $controller -AssemblyRoot $AssemblyRoot -AdmissionSave (Join-Path $Run 'saves/ferry-admitted.ddsave') -Run (Join-Path $Run 'controller') > (Join-Path $Run 'controller.stdout.txt') 2> (Join-Path $Run 'controller.stderr.txt')
    if($LASTEXITCODE-ne0){throw ('Controller continuation failed: '+(Get-Content -LiteralPath (Join-Path $Run 'controller.stderr.txt') -Raw))}
    $report.controllerResult=Get-Content -LiteralPath (Join-Path $Run 'controller/RESULT.json') -Raw|ConvertFrom-Json
    if($report.controllerResult.status-ne'PASS_FIRST_GENUINE_CREATURE_FIRE_NOT_MODULE_ACCEPTANCE'){throw 'Controller result did not pass.'}
    $report.status='PASS_GENUINE_CURRENT_PREFIX_ADMISSION_FIRST_FIRE_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 60|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
