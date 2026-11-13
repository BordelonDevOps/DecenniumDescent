param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)

$ErrorActionPreference = 'Stop'
$runner = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-11-exp07-living-opponent-retreat/Run-ExactRetreatRegressionShard.ps1')).Path
$prior = Join-Path $PSScriptRoot '../2026-11-12-exp05-local-mining/regression/inventory.txt'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$priorNames = @(Get-Content -LiteralPath $prior)
$focus = 'mgt06_session_trap_profile_restore_and_remote_resume'
$predecessors = @($names | Where-Object { $_ -cne $focus })
if ($names.Count -ne 1486 -or $focus -cnotin $names -or
    [string]::Join("`n", $predecessors) -cne [string]::Join("`n", $priorNames)) {
    throw 'Unexpected trap case or accepted predecessor inventory.'
}
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$groups = @('shardA','shardB','shardC','shardD','shardE','shardF')
$pwsh = (Get-Command pwsh).Source
# Preserve the prior distribution of its long-running witnesses and put the new control first.
$processes = for ($i=0; $i -lt $groups.Count; $i++) {
    $group = $groups[$i]
    $assigned = @(Get-Content -LiteralPath (Join-Path (Split-Path $prior) "$group-names.txt"))
    if ($i -eq 0) { $assigned = @($focus) + $assigned }
    $assigned | Set-Content -LiteralPath "$Run/$group-names.txt" -Encoding utf8
    $arguments = @('-NoLogo','-NoProfile','-File',('"' + $runner + '"'),'-Run',('"' + $Run + '"'),
        '-AssemblyRoot',('"' + $AssemblyRoot + '"'),'-Group',$group)
    $process = Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru `
        -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=$assigned.Count;assemblyRoot=$AssemblyRoot}
}
$processes | ConvertTo-Json | Set-Content -LiteralPath "$Run/processes.json" -Encoding utf8
$processes | Select-Object group,pid,cases | Format-Table
