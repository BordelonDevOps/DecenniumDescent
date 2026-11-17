param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$runner=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Run-ExactBishopShard.ps1')).Path
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
if(Test-Path -LiteralPath $Run){throw 'Use a fresh complete regression directory; never restart an existing launch.'}
$build=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
if($build.status-ne'PASS'-or$build.sourceHashes.Count-ne468){throw 'Expected the passing468-input compiled source report.'}
foreach($source in $build.sourceHashes){
    if((Digest (Join-Path (Join-Path $repository 'engine') $source.path))-cne$source.sha256){throw "Compiled source changed: $($source.path)"}
}
& git -C $repository diff --quiet HEAD -- engine
if($LASTEXITCODE-ne0){throw 'Commit and freeze engine sources before qualification.'}
& git -C $repository diff --quiet c8ffee78d5047131317ff923c8e3a575b6c51f3a HEAD -- engine
if($LASTEXITCODE-ne0){throw 'This launch is bound to the exact corrected public Dash source tree.'}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")}
$names=@([Decennium.Foundation.Tests.FoundationCases]::Names())
$predecessorArchive=Join-Path $repository 'docs/unity/evidence/2026-11-16-tac03-declared-geometry-runtime/final/qualification-final.zip'
$predecessorSha='45ebff77c7fb1c39517f76c64ca5f60e1f4040c9155fa57be0bb59d24a707b72'
if((Digest $predecessorArchive)-cne$predecessorSha){throw 'Accepted1576-case predecessor archive changed.'}
$oldBytes=[ordered]@{};$oldNames=[ordered]@{}
$zip=[IO.Compression.ZipFile]::OpenRead($predecessorArchive)
try {
    foreach($file in 'all-names.txt','shardA-names.txt','shardB-names.txt','shardC-names.txt','shardD-names.txt','shardE-names.txt','shardF-names.txt'){
        $entry=$zip.GetEntry('regression/'+$file)
        if(!$entry){throw "Accepted predecessor assignment missing: $file"}
        $stream=$entry.Open();$memory=[IO.MemoryStream]::new()
        try{$stream.CopyTo($memory);$oldBytes[$file]=$memory.ToArray()}finally{$stream.Dispose();$memory.Dispose()}
        $text=[Text.Encoding]::UTF8.GetString($oldBytes[$file]).TrimStart([char]0xfeff)
        $oldNames[$file]=@($text -split '\r?\n'|Where-Object {$_-ne''})
    }
} finally {$zip.Dispose()}
$old=$oldNames['all-names.txt'];$new=@($names|Where-Object {$_-cnotin$old})
$expected=@('tac10_damage_order_preserves_source_save_flat_resistance_and_life','tac10_ferry_numeric_origin_and_source_payload_roundtrip','tac10_ferry_paid_current_epoch_admission_from_fresh_campaign','tac10_ferry_public_dash_paid_movement_and_authorized_retry','tac10_ferry_shared_untrained_checks_and_actual_initiative','tac10_ferry_typed_defenses_settle_actual_life_mechanical','tac10_petrified_poison_immunity_retains_event_condition_provenance','tac10_seal_uses_owned_action_and_original_deadline')
$predecessors=@($names|Where-Object {$_-cnotin$new})
if($names.Count-ne1584-or$old.Count-ne1576-or[string]::Join("`n",$new)-cne[string]::Join("`n",$expected)-or[string]::Join("`n",$predecessors)-cne[string]::Join("`n",$old)){throw 'The exact1584-case inventory does not retain the original1576 order plus eight new cases.'}
$groups=@('shardA','shardB','shardC','shardD','shardE','shardF')
$oldAssigned=@($groups|ForEach-Object {$oldNames["$_-names.txt"]})
if($oldAssigned.Count-ne1576-or@($oldAssigned|Sort-Object -Unique).Count-ne1576-or@($old|Where-Object {$_-cnotin$oldAssigned}).Count-ne0){throw 'Original authenticated shards lost or duplicated a predecessor.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$executionRoot=(New-Item -ItemType Directory -Path (Join-Path $Run 'execution-assemblies')).FullName
$originalRoot=(New-Item -ItemType Directory -Path (Join-Path $Run 'authenticated-predecessor')).FullName
$originalHashes=[ordered]@{}
foreach($file in $oldBytes.Keys){[IO.File]::WriteAllBytes((Join-Path $originalRoot $file),$oldBytes[$file]);$originalHashes[$file]=Digest (Join-Path $originalRoot $file)}
$names|Set-Content -LiteralPath (Join-Path $Run 'all-names.txt') -Encoding utf8
$new|Set-Content -LiteralPath (Join-Path $Run 'new-names.txt') -Encoding utf8
Copy-Item -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Destination (Join-Path $Run 'compiled-source-report.json')
Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Start-FerryDashRegression.executed.ps1')
$frozenRunner=Join-Path $Run 'Run-ExactBishopShard.executed.ps1';Copy-Item -LiteralPath $runner -Destination $frozenRunner
$assemblies=[ordered]@{}
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
    $dll="Decennium.Foundation.$name.dll";$source=Join-Path $AssemblyRoot $dll
    $assemblies[$dll]=Digest $source;Copy-Item -LiteralPath $source -Destination (Join-Path $executionRoot $dll)
}
$assignments=[ordered]@{};$assignedAll=@()
for($i=0;$i-lt$groups.Count;$i++){
    $group=$groups[$i];$assigned=@(for($j=$i;$j-lt$new.Count;$j+=$groups.Count){$new[$j]})
    $assigned+=@($oldNames["$group-names.txt"])
    $assignedAll+=$assigned;$assigned|Set-Content -LiteralPath (Join-Path $Run "$group-names.txt") -Encoding utf8
    $assignments[$group]=Digest (Join-Path $Run "$group-names.txt")
}
if($assignedAll.Count-ne1584-or@($assignedAll|Sort-Object -Unique).Count-ne1584-or@($names|Where-Object {$_-cnotin$assignedAll}).Count-ne0){throw 'New assignments lost or duplicated a case.'}
$runId=[Guid]::NewGuid().ToString('N')
[ordered]@{runId=$runId;scope='Complete1584 cases: exact authenticated1576 predecessor order and shard membership, plus eight new Ferry cases; not module acceptance';
    assemblies=$assemblies;assignments=$assignments;inventorySha256=(Digest (Join-Path $Run 'all-names.txt'));
    startedUtc=[DateTime]::UtcNow.ToString('o');compiledSourceReportSha256=(Digest (Join-Path $Run 'compiled-source-report.json'));
    runner=$frozenRunner;runnerSha256=(Digest $frozenRunner);launcherSha256=(Digest $PSCommandPath);
    sourceCommit=((& git -C $repository rev-parse HEAD).Trim());engineTreeCommit='c8ffee78d5047131317ff923c8e3a575b6c51f3a';
    sourceCommitted=$true;requiredCount=1584;retainedPredecessors=1576;newCases=8;
    predecessorArchiveSha256=$predecessorSha;predecessorAssignments=$originalHashes
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'launch.json') -Encoding utf8
$pwsh=(Get-Command pwsh).Source
$processes=foreach($group in $groups){
    $arguments=@('-NoLogo','-NoProfile','-File',('"'+$frozenRunner+'"'),'-Run',('"'+$Run+'"'),'-AssemblyRoot',('"'+$executionRoot+'"'),'-Group',$group)
    $process=Start-Process -FilePath $pwsh -WindowStyle Hidden -ArgumentList $arguments -PassThru -RedirectStandardOutput "$Run/$group.out" -RedirectStandardError "$Run/$group.err"
    [pscustomobject]@{group=$group;pid=$process.Id;cases=@(Get-Content -LiteralPath "$Run/$group-names.txt").Count;assemblyRoot=$executionRoot}
}
$processes|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'processes.json') -Encoding utf8
Write-Output "Started exact1584-case regression $runId at $Run"
$processes|Select-Object group,pid,cases|Format-Table
