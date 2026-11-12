param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run,
    [switch]$Correction
)

$ErrorActionPreference = 'Stop'
$runner = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-11-exp07-living-opponent-retreat/Run-ExactRetreatRegressionShard.ps1')).Path
$prior = Join-Path $PSScriptRoot '../2026-11-12-int03-playability/regression/inventory.txt'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$priorNames = @(Get-Content -LiteralPath $prior)
$focus = @('int03_session_scoped_views_delivery_and_validated_file_recovery')
if ($Correction) { $focus += 'int03_session_off_turn_knockout_and_press_restore' }
$predecessors = @($names | Where-Object { $_ -cnotin $focus })
if ($names.Count -ne (1480 + $focus.Count) -or @($focus | Where-Object { $_ -cnotin $names }).Count -ne 0 -or
    [string]::Join("`n", $predecessors) -cne [string]::Join("`n", $priorNames)) {
    throw 'Unexpected session case or accepted predecessor inventory.'
}
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$groups = @('shardA','shardB','shardC','shardD','shardE','shardF')
$direct = @($names | Where-Object { $_ -cmatch 'int03|tac10|mgt04|replay|authority|restore|duplicate|stale|corrupt' })
$remaining = @($names | Where-Object { $_ -cnotin $direct })
$blocks = @($direct, $remaining)
$pwsh = (Get-Command pwsh).Source
$processes = for ($i=0; $i -lt $groups.Count; $i++) {
    $group = $groups[$i]
    $assigned = @(foreach ($block in $blocks) {
        for ($j=$i; $j -lt $block.Count; $j+=$groups.Count) { $block[$j] }
    })
    $assigned | Set-Content -LiteralPath "$Run/$group-names.txt" -Encoding utf8
    $arguments = @('-NoLogo','-NoProfile','-File',('"' + $runner + '"'),'-Run',('"' + $Run + '"'),
        '-AssemblyRoot',('"' + $AssemblyRoot + '"'),'-Group',$group)
    $process = Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru `
        -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=$assigned.Count;assemblyRoot=$AssemblyRoot}
}
$processes | ConvertTo-Json | Set-Content -LiteralPath "$Run/processes.json" -Encoding utf8
$processes | Select-Object group,pid,cases | Format-Table
