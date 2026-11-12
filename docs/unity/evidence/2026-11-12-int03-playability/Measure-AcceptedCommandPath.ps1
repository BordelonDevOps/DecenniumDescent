param(
    [Parameter(Mandatory)][string]$OutputRoot,
    [ValidateRange(3,15)][int]$Samples = 5
)
$ErrorActionPreference = 'Stop'
$running = Get-CimInstance Win32_Process -Filter "Name = 'pwsh.exe'" | Where-Object {
    $_.ProcessId -ne $PID -and $_.CommandLine -match '[\\/](Run-ExactRetreatRegressionShard|Test-Foundation|Compile-Foundation)\.ps1'
}
if ($running) { throw 'Run the accepted-command baseline without competing regression or compilation jobs.' }

$accepted = Join-Path $PSScriptRoot '../2026-11-12-tac10-later-defender-controller'
$manifest = Get-Content -LiteralPath (Join-Path $accepted 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$expected = 'e7fdcbf2eab61aa5aaaf5e86e900a7346e8511c2'
if ($manifest.implementationCommit -cne $expected -or $manifest.unfilteredCases -ne 1478) {
    throw 'Unexpected accepted source or regression inventory.'
}
function Confirm-Artifact([string]$Relative) {
    $file = Get-Item -LiteralPath (Join-Path $accepted $Relative)
    $binding = $manifest.artifacts[$Relative]
    if ($file.Length -ne $binding.bytes -or (Get-FileHash -LiteralPath $file.FullName).Hash.ToLowerInvariant() -cne $binding.sha256) {
        throw "The accepted artifact changed: $Relative"
    }
    $file.FullName
}
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Confirm-Artifact "focused/assemblies/Decennium.Foundation.$name.dll")
}
$inputArtifact = 'focused/saves/tac10-continued.ddsave'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$originalBytes = [IO.File]::ReadAllBytes((Confirm-Artifact $inputArtifact))
$recorded = $codec.Decode($originalBytes)
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory

# Only the baseline uses the original test policy factory to bind the exact recorded fixture.
# No test helper drives the benchmark's command execution.
$testFactory = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$defender = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
$worker = [Decennium.Foundation.ConnectedBloodSpecimen]::Worker
$stamp = [Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(113301,2))
$conditionFactory = $testFactory.GetMethod('CCApply',$flags)
$events = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@(
    $conditionFactory.Invoke($null,@('tac10-defender-stun','Stunned',$defender,$null,$stamp,$null))
    $conditionFactory.Invoke($null,@('tac10-worker-invisible','Invisible',$worker,$null,$stamp,$null))
)
$factoryInputs = [object[]]::new(2)
$factoryInputs[0] = $events
$policy = $testFactory.GetMethod('BatchPolicy',$flags).Invoke($null,$factoryInputs)
if ($policy.ContentFingerprint -cne $recorded.ContentFingerprint) { throw 'Unexpected selected fixture identity.' }

function Digest([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Replay-Receipts($End, [bool]$KeepPrefixes = $false) {
    $state = $policy.Initial()
    $state.SchemaVersion = $End.SchemaVersion
    if ($KeepPrefixes -and 0 -in $revisions) { $prefixes[0] = $state.Copy() }
    foreach ($receipt in $End.Receipts) {
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $failure = $policy.Resolve($state, $command)
        if ($failure -or $command.ExpectedRevision -ne $state.Revision) { throw "Recorded history rejected: $($receipt.Id) $failure" }
        $state.Revision = $receipt.Revision
        $state.Receipts = [Decennium.Foundation.CommandReceipt[]](@($state.Receipts) + $receipt)
        if ($KeepPrefixes -and $state.Revision -in $revisions) { $prefixes[[int]$state.Revision] = $state.Copy() }
    }
    $state
}

$checkpoints = @(
    @{label='opening-step'; revision=0; kind='BeginWorldStep'},
    @{label='first-encounter-attack'; revision=9; kind='AttackClub'},
    @{label='mid-expedition-clock'; revision=49; kind='AdvanceClock'},
    @{label='stabilization-work-milestone'; revision=104; kind='AdvanceClock'},
    @{label='off-turn-opportunity'; revision=113; kind='RespondOpportunityAttack'},
    @{label='defender-stance'; revision=116; kind='SelectCombatStance'},
    @{label='defender-tactical-step'; revision=117; kind='TacticalStep'},
    @{label='ordinary-continuation'; revision=164; kind='AdvanceClock'}
)
$revisions = @($checkpoints | ForEach-Object { $_.revision; $_.revision + 1 })
$prefixes = @{}
$replayed = Replay-Receipts $recorded $true
if ((Digest ($codec.Encode($replayed))) -cne (Digest $originalBytes)) { throw 'Canonical full replay differed from the accepted save.' }
$defenderGrant = [Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority()
$actors = [string[]]@($recorded.Actors | ForEach-Object Id)
$benchmarkHost = [Decennium.Foundation.Authority]::new('TEST_ONLY.host',$actors,$true,$true,$actors,$actors)
$clock = [Diagnostics.Stopwatch]::new()
$store = [Decennium.Foundation.FileSaveStore]::new()
$work = (New-Item -ItemType Directory -Path $OutputRoot -Force).FullName
$rows = @(foreach ($check in $checkpoints) {
    $snapshot = $prefixes[$check.revision]
    $receipt = $recorded.Receipts[$check.revision]
    $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
    if ($command.Kind.ToString() -cne $check.kind) { throw "Unexpected recorded command at revision $($check.revision)." }
    $useDefender = $receipt.Principal -ceq $defenderGrant.Principal
    $grant = if ($useDefender) { $defenderGrant } else { $benchmarkHost }
    $expectedInput = Digest ($codec.Encode($snapshot))
    $expectedResult = Digest ($codec.Encode($prefixes[$check.revision + 1]))
    for ($i = 0; $i -le $Samples; $i++) {
        $row = [ordered]@{workload=$check.label;revision=$snapshot.Revision;clock=$snapshot.RuleClock.ToString();sample=$i;command=$check.kind}
        $clock.Restart()
        $detached = $snapshot.Copy()
        $row.copy_ms = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        [Decennium.Foundation.Validation]::Snapshot($detached)
        $row.structure_ms = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $policyError = $policy.ValidateState($detached)
        $row.policy_full_ms = $clock.Elapsed.TotalMilliseconds
        if ($policyError) { throw "Accepted prefix did not validate: $policyError" }
        $clock.Restart()
        $history = Replay-Receipts $snapshot
        $row.history_reconstruction_ms = $clock.Elapsed.TotalMilliseconds
        if ((Digest ($codec.Encode($history))) -cne $expectedInput) { throw 'Isolated reconstruction changed the accepted prefix.' }
        $clock.Restart()
        $encoded = $codec.Encode($detached)
        $row.encode_ms = $clock.Elapsed.TotalMilliseconds
        $path = Join-Path $work "$($check.label)-$i.ddsave"
        $clock.Restart()
        $store.Save($path,$detached)
        $row.disk_save_ms = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $decoded = $store.Load($path)
        $row.disk_load_decode_ms = $clock.Elapsed.TotalMilliseconds
        $clock.Restart()
        $sim = [Decennium.Foundation.Simulation]::new($policy,$decoded,$profile)
        $row.restore_validation_ms = $clock.Elapsed.TotalMilliseconds
        if ((Digest ($codec.Encode($sim.Capture()))) -cne $expectedInput) { throw 'The benchmark restore changed accepted state.' }
        if ($useDefender) {
            $controller = [Decennium.Foundation.Laboratory.LaterDefenderController]::new($sim,$policy)
            $clock.Restart()
            $plan = $controller.Plan($grant)
            $row.projection_ms = $clock.Elapsed.TotalMilliseconds
            if ($plan.Primary.Id -cne $receipt.Id) { throw 'Restored controller intent differs from the accepted command.' }
            $clock.Restart()
            $admission = $sim.AssessCommandAdmission($grant,$command)
            $row.admission_ms = $clock.Elapsed.TotalMilliseconds
            if ($admission.Status.ToString() -cne 'Admitted') { throw "Recorded command inadmissible: $($admission.Code)" }
        }
        $candidate = $decoded.Copy()
        $clock.Restart()
        $failure = $policy.Resolve($candidate,$command)
        $row.resolver_only_ms = $clock.Elapsed.TotalMilliseconds
        if ($failure) { throw "Detached resolver rejected accepted command: $failure" }
        $clock.Restart()
        $result = $sim.Execute($grant,$command)
        $row.execute_ms = $clock.Elapsed.TotalMilliseconds
        if ($result.Outcome.ToString() -cne 'Committed' -or (Digest ($codec.Encode($sim.Capture()))) -cne $expectedResult) {
            throw 'The accepted command did not commit its exact next recorded state.'
        }
        if ($i -ne 0) { $row }
    }
    Write-Host "Measured $($check.label) at revision $($check.revision)"
})
$processor = Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors
[ordered]@{
    status = 'PASS'
    implementationCommit = $expected
    sourceArchiveSha256 = $manifest.sourceArchiveSha256
    input = @{path=$inputArtifact;sha256=(Digest $originalBytes);revision=$recorded.Revision;fingerprint=$recorded.ContentFingerprint}
    assemblies = $manifest.executedAssemblies
    hardware = $processor
    os = [Runtime.InteropServices.RuntimeInformation]::OSDescription
    runtime = [Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    powerShell = $PSVersionTable.PSVersion.ToString()
    availableLogicalProcessors = [Environment]::ProcessorCount
    sampling = "$Samples consecutive measured samples per checkpoint after one discarded warm-up. Sequential and without competing regression or compilation jobs at launch."
    notes = 'Policy full validation includes history and canonical encoding. Reconstructed history is an independent timing of replay without canonical byte comparison, with PowerShell loop overhead. Detached resolver timing is diagnostic. Every timed Execute uses the original full validation and matches the next recorded bytes.'
    samples = $rows
} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $work 'results.json') -Encoding utf8
