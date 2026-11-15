param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$runner=(Resolve-Path -LiteralPath (Join-Path $repository 'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/support/Run-ExactTrapShard.ps1')).Path
$prior=Join-Path $repository 'docs/unity/evidence/2026-11-15-tac05-frightened/retained-development/regression'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$build=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
if($build.status-ne'PASS'){throw 'The compiled source report must pass before full regression.'}
foreach($source in $build.sourceHashes){
    if((Digest (Join-Path (Join-Path $repository 'engine') $source.path))-cne$source.sha256){throw "Compiled source changed: $($source.path)"}
}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")}
$names=@([Decennium.Foundation.Tests.FoundationCases]::Names())
$focus=@($names|Where-Object {$_.StartsWith('chr03_')})
$old=@(Get-Content -LiteralPath (Join-Path $prior 'all-names.txt'))
$predecessors=@($names|Where-Object {$_-cnotin$focus})
if($names.Count-ne1524-or$focus.Count-ne7-or$old.Count-ne1517-or
    [string]::Join("`n",$predecessors)-cne[string]::Join("`n",$old)){throw 'Unexpected Cleric settlement or predecessor inventory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$executionRoot=(New-Item -ItemType Directory -Path (Join-Path $Run 'execution-assemblies')).FullName
$names|Set-Content -LiteralPath (Join-Path $Run 'all-names.txt') -Encoding utf8
Copy-Item -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Destination (Join-Path $Run 'compiled-source-report.json')
$assemblies=[ordered]@{}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
    $dll="Decennium.Foundation.$name.dll";$source=Join-Path $AssemblyRoot $dll
    $assemblies[$dll]=Digest $source;Copy-Item -LiteralPath $source -Destination (Join-Path $executionRoot $dll)
}
$groups=@('shardA','shardB','shardC','shardD','shardE','shardF');$assignments=[ordered]@{};$assignedAll=@()
for($i=0;$i-lt$groups.Count;$i++){
    $group=$groups[$i];$new=@(for($j=$i;$j-lt$focus.Count;$j+=$groups.Count){$focus[$j]})
    $assigned=$new+@(Get-Content -LiteralPath (Join-Path $prior "$group-names.txt"))
    $assignedAll+=$assigned;$assigned|Set-Content -LiteralPath (Join-Path $Run "$group-names.txt") -Encoding utf8
    $assignments[$group]=Digest (Join-Path $Run "$group-names.txt")
}
if($assignedAll.Count-ne$names.Count-or@($assignedAll|Sort-Object -Unique).Count-ne$names.Count-or
    @($names|Where-Object {$_-cnotin$assignedAll}).Count-ne0){throw 'Shard assignment lost or duplicated a case.'}
$runId=[Guid]::NewGuid().ToString('N')
[ordered]@{runId=$runId;assemblies=$assemblies;assignments=$assignments;inventorySha256=(Digest (Join-Path $Run 'all-names.txt'));
    startedUtc=[DateTime]::UtcNow.ToString('o');compiledSourceReportSha256=(Digest (Join-Path $Run 'compiled-source-report.json'));
    runner=$runner;runnerSha256=(Digest $runner);sourceCommit=((& git -C $repository rev-parse HEAD).Trim());requiredCount=1524;retainedPredecessors=1517
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'launch.json') -Encoding utf8
$pwsh=(Get-Command pwsh).Source
$processes=foreach($group in $groups){
    $arguments=@('-NoLogo','-NoProfile','-File',('"'+$runner+'"'),'-Run',('"'+$Run+'"'),'-AssemblyRoot',('"'+$executionRoot+'"'),'-Group',$group)
    $process=Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=@(Get-Content -LiteralPath "$Run/$group-names.txt").Count;assemblyRoot=$executionRoot}
}
$processes|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'processes.json') -Encoding utf8
Write-Output "Started exact1524-case regression $runId at $Run"
$processes|Select-Object group,pid,cases|Format-Table

