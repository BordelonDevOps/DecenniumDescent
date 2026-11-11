param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference = 'Stop'
$runner=(Resolve-Path 'docs/unity/evidence/2026-11-11-exp07-living-opponent-retreat/Run-ExactRetreatRegressionShard.ps1').Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run=(Resolve-Path -LiteralPath $Run).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$old = @(Get-Content 'docs/unity/evidence/2026-11-11-exp07-living-opponent-retreat/final/regression/historical-original-inventory.txt')
$focus = @($names | Where-Object { $_ -clike 'exp07_reengagement_*' })
$history = @($names | Where-Object { $_ -cin $old -or $_ -clike 'exp07_living_retreat_*' })
$rest = @($names | Where-Object { $_ -cnotin $focus -and $_ -cnotin $history })
if ($old.Count -ne 485 -or $focus.Count -ne 6 -or $history.Count -ne 491 -or $names.Count -ne 1436 -or
    ($focus.Count + $history.Count + $rest.Count) -ne $names.Count) { throw 'Invalid compiled test inventory' }
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$focus | Set-Content -LiteralPath "$Run/focus-original-inventory.txt" -Encoding utf8
$history | Set-Content -LiteralPath "$Run/historical-original-inventory.txt" -Encoding utf8
$groups=@('shardA','shardB','shardC','shardD')
$ps=(Get-Command pwsh).Source
$state=for($i=0;$i -lt $groups.Count;$i++){
    $group=$groups[$i]
    $assigned=@(foreach($block in @($focus,$history,$rest)){
        for($j=$i;$j -lt $block.Count;$j+=$groups.Count){$block[$j]}
    })
    $assigned | Set-Content -LiteralPath "$Run/$group-names.txt" -Encoding utf8
    $p=Start-Process -FilePath $ps -WindowStyle Hidden -ArgumentList @('-NoLogo','-NoProfile','-File',('"' + $runner + '"'),'-Run',('"' + $Run + '"'),'-AssemblyRoot',('"' + $AssemblyRoot + '"'),'-Group',$group) -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err" -PassThru
    [pscustomobject]@{group=$group;pid=$p.Id;cases=$assigned.Count;started=$p.StartTime;assemblyRoot=$AssemblyRoot}
}
$state | ConvertTo-Json | Set-Content -LiteralPath "$Run/processes.json" -Encoding utf8
$state | Select-Object group,pid,cases | Format-Table
