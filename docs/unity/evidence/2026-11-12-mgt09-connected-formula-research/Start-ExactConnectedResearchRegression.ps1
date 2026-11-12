param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference = 'Stop'
$runner = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-11-exp07-living-opponent-retreat/Run-ExactRetreatRegressionShard.ps1')).Path
$prior = Join-Path $PSScriptRoot '../2026-11-11-exp04-connected-observation/regression/full/inventory.txt'
if ((Get-FileHash -LiteralPath $prior).Hash -cne 'CEC63789BBC5FF6DA993FBC73B93CBF83AE1AED06C7F9D70C36878FA85F9668F') {
    throw 'The accepted connected observation inventory changed.'
}
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$priorNames = @(Get-Content -LiteralPath $prior)
$focus = @($names | Where-Object { $_ -clike 'mgt09_connected_formula_research_*' })
$predecessors = @($names | Where-Object { $_ -cnotin $focus })
if ($focus.Count -ne 4 -or $names.Count -ne 1467 -or
    [string]::Join("`n", $predecessors) -cne [string]::Join("`n", $priorNames)) {
    throw 'Unexpected exact research or predecessor case inventory.'
}
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$focus | Set-Content -LiteralPath "$Run/focus-inventory.txt" -Encoding utf8
$groups = @('shardA','shardB','shardC','shardD','shardE','shardF')
$pwsh = (Get-Command pwsh).Source
$direct = @($predecessors | Where-Object { $_ -cmatch 'formula|research|manufactur|connected_observation' })
$remaining = @($predecessors | Where-Object { $_ -cnotin $direct })
$blocks = @($focus, $direct, $remaining)
$processes = for ($i = 0; $i -lt $groups.Count; $i++) {
    $group = $groups[$i]
    $assigned = @(foreach ($block in $blocks) {
        for ($j = $i; $j -lt $block.Count; $j += $groups.Count) { $block[$j] }
    })
    $assigned | Set-Content -LiteralPath "$Run/$group-names.txt" -Encoding utf8
    $arguments = @('-NoLogo','-NoProfile','-File',('"' + $runner + '"'),'-Run',('"' + $Run + '"'),
        '-AssemblyRoot',('"' + $AssemblyRoot + '"'),'-Group',$group)
    $process = Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=$assigned.Count;assemblyRoot=$AssemblyRoot}
}
$processes | ConvertTo-Json | Set-Content -LiteralPath "$Run/processes.json" -Encoding utf8
$processes | Select-Object group,pid,cases | Format-Table
