param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run,
    [switch]$Full
)
$ErrorActionPreference = 'Stop'
$runner = (Resolve-Path 'docs/unity/evidence/2026-11-11-exp07-living-opponent-retreat/Run-ExactRetreatRegressionShard.ps1').Path
$prior = Join-Path $PSScriptRoot '../2026-11-11-exp04-exploration-hide/regression/historical/inventory.txt'
if ((Get-FileHash -LiteralPath $prior).Hash -cne '8FA5EF6EFBCA0FCB2B619FC22BF94A6F4A5FD37530AE9B352C78F1937C228381') {
    throw 'The accepted Hide historical inventory changed.'
}
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$previous = @(Get-Content -LiteralPath $prior)
$focus = @($names | Where-Object { $_ -clike 'exp04_connected_observation_*' })
$historical = @($names | Where-Object { $_ -cin $previous -or $_ -clike 'exp04_exploration_hide_*' })
$remainder = @($names | Where-Object { $_ -cnotin $focus -and $_ -cnotin $historical })
if ($previous.Count -ne 552 -or $focus.Count -ne 7 -or $historical.Count -ne 560 -or $names.Count -ne 1463 -or
    ($focus.Count + $historical.Count + $remainder.Count) -ne $names.Count) { throw 'Unexpected exact case inventory.' }
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$focus | Set-Content -LiteralPath "$Run/focus-original-inventory.txt" -Encoding utf8
$historical | Set-Content -LiteralPath "$Run/historical-original-inventory.txt" -Encoding utf8
$groups = @('shardA','shardB','shardC','shardD','shardE','shardF')
$pwsh = (Get-Command pwsh).Source
$blocks = @($focus, $historical)
if ($Full) { $blocks += ,$remainder }
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
