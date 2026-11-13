param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)

$ErrorActionPreference = 'Stop'
$runner = (Resolve-Path (Join-Path $PSScriptRoot '../2026-11-12-mgt06-connected-trap/Run-ExactTrapShard.ps1')).Path
$prior = Join-Path $PSScriptRoot '../2026-11-12-int03-charter-performance/regression/inventory.txt'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$priorNames = @(Get-Content -LiteralPath $prior)
$focus = 'int03_active_work_condition_scope_isolation'
$predecessors = @($names | Where-Object { $_ -cne $focus })
if ($names.Count -ne 1488 -or $focus -cnotin $names -or
    [string]::Join("`n", $predecessors) -cne [string]::Join("`n", $priorNames)) {
    throw 'Unexpected active-work case or accepted predecessor inventory.'
}
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$names | Set-Content -LiteralPath "$Run/all-names.txt" -Encoding utf8
$groups = @('shardA','shardB','shardC','shardD','shardE','shardF')
$pwsh = (Get-Command pwsh).Source
function Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$assemblies = [ordered]@{}
$executionRoot = (New-Item -ItemType Directory (Join-Path $Run 'execution-assemblies')).FullName
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $dll = "Decennium.Foundation.$name.dll"
    $source = Join-Path $AssemblyRoot $dll
    $assemblies[$dll] = Digest $source
    Copy-Item -LiteralPath $source -Destination (Join-Path $executionRoot $dll)
}
$assignments = [ordered]@{}
# Preserve the prior distribution of its long-running witnesses and put the new control first.
for ($i=0; $i -lt $groups.Count; $i++) {
    $group = $groups[$i]
    $assigned = @(Get-Content -LiteralPath (Join-Path (Split-Path $prior) "$group-names.txt"))
    if ($i -eq 0) { $assigned = @($focus) + $assigned }
    $assigned | Set-Content -LiteralPath "$Run/$group-names.txt" -Encoding utf8
    $assignments[$group] = Digest "$Run/$group-names.txt"
}
[ordered]@{runId=[Guid]::NewGuid().ToString('N'); assemblies=$assemblies; assignments=$assignments
    inventorySha256=(Digest "$Run/all-names.txt"); startedUtc=[DateTime]::UtcNow.ToString('o')} |
    ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$Run/launch.json" -Encoding utf8
$processes = foreach ($group in $groups) {
    $arguments = @('-NoLogo','-NoProfile','-File',('"' + $runner + '"'),'-Run',('"' + $Run + '"'),
        '-AssemblyRoot',('"' + $executionRoot + '"'),'-Group',$group)
    $process = Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru `
        -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=@(Get-Content "$Run/$group-names.txt").Count;assemblyRoot=$executionRoot}
}
$processes | ConvertTo-Json | Set-Content -LiteralPath "$Run/processes.json" -Encoding utf8
$processes | Select-Object group,pid,cases | Format-Table
