param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run,[switch]$FocusedOnly)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$runner=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'Run-ExactBishopShard.ps1')).Path
$prior=Join-Path $repository 'docs/unity/evidence/2026-11-16-exp07-post-recovery/implementation/regression'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$build=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
if($build.status-ne'PASS'){throw 'The compiled source report must pass before regression.'}
foreach($source in $build.sourceHashes){
    if((Digest (Join-Path (Join-Path $repository 'engine') $source.path))-cne$source.sha256){throw "Compiled source changed: $($source.path)"}
}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")}
$names=@([Decennium.Foundation.Tests.FoundationCases]::Names())
$focus=@($names|Where-Object {$_.StartsWith('chr03_bishop_')})
$old=@(Get-Content -LiteralPath (Join-Path $prior 'all-names.txt'))
$predecessors=@($names|Where-Object {$_-cnotin$focus})
if($names.Count-ne1570-or$focus.Count-ne4-or$old.Count-ne1566-or
    [string]::Join("`n",$predecessors)-cne[string]::Join("`n",$old)){throw 'Unexpected Bishop or predecessor inventory.'}
if(!$FocusedOnly){
    & git -C $repository diff --quiet HEAD -- engine
    if($LASTEXITCODE-ne0){throw 'Freeze and commit engine changes before the full regression.'}
}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$executionRoot=(New-Item -ItemType Directory -Path (Join-Path $Run 'execution-assemblies')).FullName
$names|Set-Content -LiteralPath (Join-Path $Run 'all-names.txt') -Encoding utf8
Copy-Item -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Destination (Join-Path $Run 'compiled-source-report.json')
$assemblies=[ordered]@{}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
    $dll="Decennium.Foundation.$name.dll";$source=Join-Path $AssemblyRoot $dll
    $assemblies[$dll]=Digest $source;Copy-Item -LiteralPath $source -Destination (Join-Path $executionRoot $dll)
}
$groups=if($FocusedOnly){@('shardA','shardB')}else{@('shardA','shardB','shardC','shardD','shardE','shardF')};$assignments=[ordered]@{};$assignedAll=@()
for($i=0;$i-lt$groups.Count;$i++){
    $group=$groups[$i];$assigned=@(for($j=$i;$j-lt$focus.Count;$j+=$groups.Count){$focus[$j]})
    if(!$FocusedOnly){$assigned+=@(Get-Content -LiteralPath (Join-Path $prior "$group-names.txt"))}
    $assignedAll+=$assigned;$assigned|Set-Content -LiteralPath (Join-Path $Run "$group-names.txt") -Encoding utf8
    $assignments[$group]=Digest (Join-Path $Run "$group-names.txt")
}
$required=if($FocusedOnly){$focus}else{$names}
if($assignedAll.Count-ne$required.Count-or@($assignedAll|Sort-Object -Unique).Count-ne$required.Count-or
    @($required|Where-Object {$_-cnotin$assignedAll}).Count-ne0){throw 'Shard assignment lost or duplicated a case.'}
$runId=[Guid]::NewGuid().ToString('N')
[ordered]@{runId=$runId;scope=$(if($FocusedOnly){'Focused development controls only'}else{'All predecessors and new cases'});
    assemblies=$assemblies;assignments=$assignments;inventorySha256=(Digest (Join-Path $Run 'all-names.txt'));
    startedUtc=[DateTime]::UtcNow.ToString('o');compiledSourceReportSha256=(Digest (Join-Path $Run 'compiled-source-report.json'));
    runner=$runner;runnerSha256=(Digest $runner);sourceCommit=((& git -C $repository rev-parse HEAD).Trim());
    sourceCommitted=(!$FocusedOnly);requiredCount=$required.Count;retainedPredecessors=$(if($FocusedOnly){0}else{1566})
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'launch.json') -Encoding utf8
$pwsh=(Get-Command pwsh).Source
$processes=foreach($group in $groups){
    $arguments=@('-NoLogo','-NoProfile','-File',('"'+$runner+'"'),'-Run',('"'+$Run+'"'),'-AssemblyRoot',('"'+$executionRoot+'"'),'-Group',$group)
    $process=Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=@(Get-Content -LiteralPath "$Run/$group-names.txt").Count;assemblyRoot=$executionRoot}
}
$processes|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'processes.json') -Encoding utf8
Write-Output "Started exact $($required.Count)-case regression $runId at $Run"
$processes|Select-Object group,pid,cases|Format-Table
