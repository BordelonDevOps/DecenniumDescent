param(
    [Parameter(Mandatory)][ValidateSet('ArchivedVector','Equivalence','Performance','Compatibility','ColdStart')][string]$Mode,
    [Parameter(Mandatory)][string]$OutputRoot,
    [string]$AssemblyRoot,
    [string]$VectorPath,
    [string]$PriorPerformancePath,
    [ValidateRange(30,60)][int]$Samples = 30
)
$ErrorActionPreference = 'Stop'
$accepted = Join-Path $PSScriptRoot '../2026-11-12-tac10-later-defender-controller'
$binding = Get-Content -LiteralPath (Join-Path $accepted 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$out = (New-Item -ItemType Directory -Path $OutputRoot -Force).FullName
function Digest([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Bound-Input([string]$Relative) {
    $path = (Get-Item -LiteralPath (Join-Path $accepted $Relative)).FullName
    $entry = $binding.artifacts[$Relative]
    if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $entry.sha256) {
        throw "Accepted input differs from its binding: $Relative"
    }
    $path
}
if ($Mode -ne 'ArchivedVector' -and !$AssemblyRoot) { throw 'Supply the candidate assembly root.' }
if ($Mode -eq 'Performance') {
    $parent = (Get-CimInstance Win32_Process -Filter "ProcessId = $PID").ParentProcessId
    $running = Get-CimInstance Win32_Process -Filter "Name = 'pwsh.exe'" | Where-Object {
        $_.ProcessId -notin @($PID,$parent) -and $_.CommandLine -match '[\\/](Run-ExactRetreatRegressionShard|Test-Foundation|Compile-Foundation|Verify-LiveCommandPath)\.ps1'
    }
    if ($running) { throw 'Run performance without a competing regression, compiler, or verification process.' }
}
$assemblies = [ordered]@{}
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $file = "Decennium.Foundation.$name.dll"
    $path = if ($Mode -eq 'ArchivedVector') { Bound-Input "focused/assemblies/$file" }
        else { (Get-Item -LiteralPath (Join-Path $AssemblyRoot $file)).FullName }
    Add-Type -Path $path
    $assemblies[$file] = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()
}

$factory = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
$inputArtifact = 'focused/saves/tac10-continued.ddsave'
$archiveBytes = [IO.File]::ReadAllBytes((Bound-Input $inputArtifact))
$recorded = $codec.Decode($archiveBytes)
$source = [ordered]@{acceptedImplementation=$binding.implementationCommit;acceptedArchive=$binding.sourceArchiveSha256
    assemblies=$assemblies;input=@{path=$inputArtifact;sha256=(Digest $archiveBytes);revision=$recorded.Revision}}
function New-WitnessPolicy {
    $defender = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
    $worker = [Decennium.Foundation.ConnectedBloodSpecimen]::Worker
    $stamp = [Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(113301,2))
    $conditions = $factory.GetMethod('CCApply',$flags)
    $arguments = [object[]]::new(2)
    $arguments[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@(
        $conditions.Invoke($null,@('tac10-defender-stun','Stunned',$defender,$null,$stamp,$null))
        $conditions.Invoke($null,@('tac10-worker-invisible','Invisible',$worker,$null,$stamp,$null))
    )
    $policy = $factory.GetMethod('BatchPolicy',$flags).Invoke($null,$arguments)
    if ($policy.ContentFingerprint -cne $recorded.ContentFingerprint) { throw 'The selected witness profile changed.' }
    $policy
}
function Write-Report($Report) {
    $Report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $out "$Mode.json") -Encoding utf8
}
if ($Mode -eq 'ArchivedVector') {
    $policy = New-WitnessPolicy
    $state = $policy.Initial()
    $rows = @([ordered]@{revision=0;sha256=(Digest ($codec.Encode($state)))})
    $rows += @(foreach ($receipt in $recorded.Receipts) {
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        if ($command.ExpectedRevision -ne $state.Revision -or $policy.Resolve($state,$command)) {
            throw "Accepted prefix replay denied $($receipt.Id)."
        }
        $state.Revision = $receipt.Revision
        $state.Receipts = [Decennium.Foundation.CommandReceipt[]](@($state.Receipts) + $receipt)
        [ordered]@{revision=$state.Revision;sha256=(Digest ($codec.Encode($state)))}
    })
    if ($rows[-1].sha256 -cne $source.input.sha256) { throw 'Archived prefix reconstruction did not reproduce the continued save.' }
    Write-Report @{status='PASS';source=$source;prefixes=$rows}
    return
}

$vector = Get-Content -LiteralPath $VectorPath -Raw | ConvertFrom-Json -AsHashtable
if ($vector.status -cne 'PASS' -or $vector.source.acceptedImplementation -cne $binding.implementationCommit -or
    $vector.source.input.sha256 -cne $source.input.sha256 -or $vector.prefixes.Count -ne 166) {
    throw 'Unexpected independent accepted vector.'
}
foreach ($file in $binding.executedAssemblies.Keys) {
    if ($vector.source.assemblies[$file] -cne $binding.executedAssemblies[$file].sha256) {
        throw "The independent prefix vector did not use the accepted assembly: $file"
    }
}
$source.vectorSha256 = (Get-FileHash -LiteralPath $VectorPath).Hash.ToLowerInvariant()
$verified = [Decennium.Foundation.CommandVerification]::VerifiedPrefix

if ($Mode -eq 'ColdStart') {
    # Fresh process, after loading the bound assemblies and decoding the reference save.
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $policy = New-WitnessPolicy
    $configuration = $timer.Elapsed.TotalMilliseconds
    $timer.Restart()
    $initial = $policy.Initial()
    $initialization = $timer.Elapsed.TotalMilliseconds
    $timer.Restart()
    $sim = [Decennium.Foundation.Simulation]::new($policy,$initial,$profile,$verified)
    $validation = $timer.Elapsed.TotalMilliseconds
    if ((Digest ($codec.Encode($sim.Capture()))) -cne $vector.prefixes[0].sha256) {
        throw 'Cold initialization diverged from the accepted initial state.'
    }
    Write-Report @{status='PASS';source=$source;mode=$verified.ToString();scope='Fresh process after assembly load'
        policyConfigurationMs=$configuration;initialStateMs=$initialization;fullValidationAndSealMs=$validation}
    return
}

if ($Mode -eq 'Compatibility') {
    $batch = Join-Path $PSScriptRoot '../2026-11-12-mgt04-connected-recipe4-batch'
    $prior = Get-Content -LiteralPath (Join-Path $batch 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
    $timeline = Get-Content -LiteralPath (Join-Path $batch 'focused/timeline.json') -Raw | ConvertFrom-Json -AsHashtable
    $profiles = @{
        default=$factory.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,$null))
        masterwork=$factory.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]818668))
        mishap=$factory.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]817576))
        flawed=$factory.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]99690))
        deferred=$factory.GetMethod('BatchDeferredPolicy',$flags).Invoke($null,@())
        injury=$factory.GetMethod('BatchInjuryPolicy',$flags).Invoke($null,@())
    }
    $rows = @(foreach ($item in $timeline.savedStates) {
        $relative = "focused/saves/$($item.save)"
        $bytes = [IO.File]::ReadAllBytes((Join-Path $batch $relative))
        $hash = Digest $bytes
        if ($hash -cne $prior.artifacts[$relative].sha256 -or $hash -cne $item.sha256) {
            throw "Predecessor save changed: $relative"
        }
        $policy = $profiles[$item.profile]
        $strict = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),$profile)
        $fast = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),$profile,$verified)
        if ((Digest ($codec.Encode($strict.Capture()))) -cne $hash -or (Digest ($codec.Encode($fast.Capture()))) -cne $hash) {
            throw "A restored mode changed the authentic predecessor: $relative"
        }
        [ordered]@{save=$item.save;profile=$item.profile;sha256=$hash;revision=$item.revision}
    })
    if ($rows.Count -ne 22) { throw 'Unexpected wire95 compatibility inventory.' }
    Write-Report @{status='PASS';source=$source;authenticWire95Saves=$rows}
    return
}

$actors = [string[]]@($recorded.Actors | ForEach-Object Id)
$hostGrant = [Decennium.Foundation.Authority]::new('TEST_ONLY.host',$actors,$true,$true,$actors,$actors)
$defenderGrant = [Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority()
$commands = @($recorded.Receipts | ForEach-Object { [Decennium.Foundation.CommandHistory]::Read($_) })
$grants = @($recorded.Receipts | ForEach-Object {
    if ($_.Principal -ceq $defenderGrant.Principal) { $defenderGrant }
    elseif ($_.Principal -ceq $hostGrant.Principal) { $hostGrant }
    else { throw "Unknown recorded principal $($_.Principal)." }
})
function Check-State($Simulation,[int]$Revision) {
    if ((Digest ($codec.Encode($Simulation.Capture()))) -cne $vector.prefixes[$Revision].sha256) {
        throw "Canonical state diverged from the accepted archive at revision $Revision."
    }
}
function Same-Result($Left,$Right) {
    foreach ($key in 'Outcome','Code','Revision','IsSuspended','TacticalDecisionAt','ReachedClock') {
        if ($Left.$key -ne $Right.$key) { throw "Different public command result property: $key" }
    }
}
function Check-Denial($Reference,$Fast,$Grant,$Command,[string]$ExpectedCode,[int]$Revision) {
    $left = $Reference.Execute($Grant,$Command)
    $right = $Fast.Execute($Grant,$Command)
    Same-Result $left $right
    if ($left.Code -cne $ExpectedCode) { throw "Unexpected denial $($left.Code), expected $ExpectedCode." }
    Check-State $Reference $Revision
    Check-State $Fast $Revision
    [ordered]@{revision=$Revision;command=$Command.Kind.ToString();code=$left.Code}
}
if ($Mode -eq 'Equivalence') {
    $strictPolicy = New-WitnessPolicy
    $fastPolicy = New-WitnessPolicy
    $strict = [Decennium.Foundation.Simulation]::new($strictPolicy,$strictPolicy.Initial(),$profile)
    $fast = [Decennium.Foundation.Simulation]::new($fastPolicy,$fastPolicy.Initial(),$profile,$verified)
    Check-State $strict 0
    Check-State $fast 0
    $denials = @()
    $fileStore = [Decennium.Foundation.FileSaveStore]::new()
    $rows = @(for ($i=0; $i -lt $commands.Count; $i++) {
        $command = $commands[$i]
        $grant = $grants[$i]
        if ($i -eq 113) {
            $save = Join-Path $out 'verified-pending-opportunity.ddsave'
            $fileStore.Save($save,$fast.Capture())
            $restoredPolicy = New-WitnessPolicy
            $fast = [Decennium.Foundation.Simulation]::new($restoredPolicy,$fileStore.Load($save),$profile,$verified)
            Check-State $fast $i
            $noClub = [Decennium.Foundation.Authority]::new($defenderGrant.Principal,[string[]]@($command.Actor))
            $denials += Check-Denial $strict $fast $noClub $command 'InventoryNotAuthorized' $i
            $playerOnly = [Decennium.Foundation.Authority]::new($hostGrant.Principal,
                [string[]]@([Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId,
                    [Decennium.Foundation.ConnectedBloodSpecimen]::Worker))
            $denials += Check-Denial $strict $fast $playerOnly $command 'NotAuthorized' $i
        }
        $expected = $strict.Execute($grant,$command)
        $actual = $fast.Execute($grant,$command)
        Same-Result $expected $actual
        if ($actual.Outcome.ToString() -cne 'Committed') { throw "Accepted receipt did not commit: $i $($actual.Code)" }
        Check-State $strict ($i+1)
        Check-State $fast ($i+1)
        if ($i -eq 113) {
            $denials += Check-Denial $strict $fast $grant $command 'AlreadyCommitted' ($i+1)
            $denials += Check-Denial $strict $fast $noClub $command 'InventoryNotAuthorized' ($i+1)
        }
        [ordered]@{revision=$i+1;receipt=$command.Id;kind=$command.Kind.ToString();outcome=$actual.Outcome.ToString()
            code=$actual.Code;clock=$fast.Capture().RuleClock.ToString();sha256=$vector.prefixes[$i+1].sha256}
    })
    $validated = New-WitnessPolicy
    $replayed = [Decennium.Foundation.Simulation]::new($validated,$fast.Capture(),$profile)
    Check-State $replayed 165
    $fileStore.Save((Join-Path $out 'verified-continued.ddsave'),$fast.Capture())
    Write-Report @{status='PASS';source=$source;committed=$rows;denials=$denials;restoreRevision=113;strictFinalReplay=$true}
    return
}

$baseline = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'BASELINE_RESULTS.json') -Raw | ConvertFrom-Json -AsHashtable
$workloads = @{}
foreach ($sample in $baseline.samples) { $workloads[[int]$sample.revision] = $sample.workload }
$clock = [Diagnostics.Stopwatch]::new()
$runPolicy = New-WitnessPolicy
$warmSaves = @{}
$process = [Diagnostics.Process]::GetCurrentProcess()
$initialTimes = @()
$measurements = @(for ($sample=0; $sample -le $Samples; $sample++) {
    $clock.Restart()
    $sim = [Decennium.Foundation.Simulation]::new($runPolicy,$runPolicy.Initial(),$profile,$verified)
    if ($sample -ne 0) { $initialTimes += $clock.Elapsed.TotalMilliseconds }
    for ($i=0; $i -lt $commands.Count; $i++) {
        if ($sample -eq 0 -and $workloads.ContainsKey($i)) {
            $warmSaves[$i] = $sim.Capture()
            Check-State $sim $i
        }
        $measure = $sample -ne 0 -and $workloads.ContainsKey($i)
        if ($measure) {
            $process.Refresh()
            $cpuBefore = $process.TotalProcessorTime.TotalMilliseconds
            $gcBefore = @(0..2 | ForEach-Object { [GC]::CollectionCount($_) })
        }
        $clock.Restart()
        $result = $sim.Execute($grants[$i],$commands[$i])
        $elapsed = $clock.Elapsed.TotalMilliseconds
        if ($measure) {
            $process.Refresh()
            $cpu = $process.TotalProcessorTime.TotalMilliseconds - $cpuBefore
            $collections = @(0..2 | ForEach-Object { [GC]::CollectionCount($_) - $gcBefore[$_] })
        }
        if ($result.Outcome.ToString() -cne 'Committed') { throw "Timed execution rejected at revision $i." }
        if ($measure) {
            Check-State $sim ($i+1)
            [ordered]@{workload=$workloads[$i];revision=$i;sample=$sample;execute_ms=$elapsed
                process_cpu_ms=$cpu;gcCollections=$collections}
        }
    }
    Check-State $sim 165
    Write-Host "Measured verified connected run $sample of $Samples"
})
$measurements | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $out 'warm-samples.json') -Encoding utf8
function Measure-Percentiles($Rows, [int]$CountPerWorkload) {
    foreach ($group in $Rows | Group-Object { $_['revision'] }) {
    $ordered = @($group.Group | ForEach-Object { [double]$_['execute_ms'] } | Sort-Object)
    if ($ordered.Count -ne $CountPerWorkload) { throw 'Missing warm measured command.' }
    $p95 = $ordered[[int][Math]::Ceiling(0.95 * $ordered.Count) - 1]
    $middle = [int][Math]::Floor($ordered.Count / 2)
    $median = if ($ordered.Count % 2) { $ordered[$middle] } else { ($ordered[$middle - 1] + $ordered[$middle]) / 2 }
    $revision = [int]$group.Name
    $budget = if ($revision -eq 104) { 350 } else { 150 }
    [ordered]@{revision=$revision;workload=$workloads[$revision];count=$ordered.Count;median_ms=$median
        p95_ms=$p95;maximum_ms=$ordered[-1];budget_ms=$budget;met=($p95 -le $budget)}
    }
}
$stats = @(Measure-Percentiles $measurements $Samples)
$combined = $null
$priorHash = $null
if ($PriorPerformancePath) {
    $prior = Get-Content -LiteralPath $PriorPerformancePath -Raw | ConvertFrom-Json -AsHashtable
    if ($prior.source.vectorSha256 -cne $source.vectorSha256 -or $prior.mode -cne $verified.ToString() -or
        $prior.results.Count -ne 8 -or $prior.warmSamplesPerWorkload -ne $Samples) {
        throw 'The original timing run does not match this candidate and workload.'
    }
    foreach ($file in $assemblies.Keys) {
        if ($prior.source.assemblies[$file] -cne $assemblies[$file]) { throw "Timing assembly changed: $file" }
    }
    $combined = @(Measure-Percentiles (@($prior.samples) + $measurements) (2 * $Samples))
    $priorHash = (Get-FileHash -LiteralPath $PriorPerformancePath).Hash.ToLowerInvariant()
}
$fileStore = [Decennium.Foundation.FileSaveStore]::new()
$storage = @(foreach ($key in $warmSaves.Keys | Sort-Object) {
    for ($sample=1; $sample -le 5; $sample++) {
        $path = Join-Path $out "restore-$key-$sample.ddsave"
        $state = $warmSaves[$key]
        $clock.Restart()
        $encoded = $codec.Encode($state)
        $encode = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $fileStore.Save($path,$state)
        $save = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $decoded = $fileStore.Load($path)
        $load = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $sim = [Decennium.Foundation.Simulation]::new($runPolicy,$decoded,$profile,$verified)
        $restore = $clock.Elapsed.TotalMilliseconds
        Check-State $sim $key
        [ordered]@{revision=$key;sample=$sample;encode_ms=$encode;disk_save_ms=$save;disk_load_decode_ms=$load
            complete_restore_and_seal_ms=$restore;bytes=$encoded.Length}
    }
})
$resultsToAccept = @($stats)
if ($combined) { $resultsToAccept += $combined }
$missed = @($resultsToAccept | Where-Object { !$_['met'] })
Write-Report ([ordered]@{status=if($missed){'FAIL'}else{'PASS'};source=$source;mode=$verified.ToString()
    hardware=(Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors)
    os=[Runtime.InteropServices.RuntimeInformation]::OSDescription;runtime=[Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    warmSamplesPerWorkload=$Samples;percentile='Nearest rank, ceil(0.95*n). One whole connected warm-up run discarded.'
    measuredInitialConstructionMs=$initialTimes;results=$stats;samples=$measurements;storage=$storage
    priorPerformanceSha256=$priorHash;combinedResults=$combined})
if ($missed) { throw 'At least one measured public command missed its approved performance budget.' }
