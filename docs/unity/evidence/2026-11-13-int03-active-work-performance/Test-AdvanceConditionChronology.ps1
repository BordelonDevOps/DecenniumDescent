param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Force $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$actor='TEST_ONLY.actor'
$worker='TEST_ONLY.companion'
$clock=[Decennium.Foundation.RuleTime]::new(20)
$stamp=[Decennium.Foundation.ConditionStamp]::new($clock)
$application=[Decennium.Foundation.ConditionApplicationData]::new('work.poison',$worker,'work.fixture','Poisoned',$stamp,'time',$false)
$apply=[Decennium.Foundation.ConditionOperation]::Apply('event.work.poison',
    [Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(0)),$application,'')
$event=[Decennium.Foundation.Laboratory.ConditionFixtureEvent]::new($worker,$apply)
$fixture=[Decennium.Foundation.Laboratory.ConditionCombatFixture]::new([Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@($event))
$combat=[Decennium.Foundation.Laboratory.SharedCombatFixture]::new(26)
$research=[Decennium.Foundation.Laboratory.SharedResearchFixture]::new($worker)
$policy=[Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::new($combat,$research,30,$fixture,
    [Decennium.Foundation.Laboratory.TacticalTerrainCell[]]@())
$grant=[Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::Host()
$simulation=[Decennium.Foundation.Simulation]::new($policy,$policy.Initial(),'Laboratory')
function Commit($command) {
    $result=$simulation.Execute($grant,$command)
    if ($result.Outcome -ne 'Committed') { throw "Witness command $($command.Id) rejected: $($result.Code)." }
}
Commit ([Decennium.Foundation.Command]::new('work.poison',$worker,0,'DispatchConditionEvent','event.work.poison'))
Commit ([Decennium.Foundation.Command]::new('work.research',$worker,1,'StartFormulaResearch','research.guild-notes'))
$amount=[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1,3))
Commit ([Decennium.Foundation.Command]::new('work.intake',$actor,2,'StartIntake','TEST_ONLY.ready-water',0,0,$amount))
$pre=$simulation.Capture()
$advance=[Decennium.Foundation.Command]::new('work.advance',$actor,3,'AdvanceClock','',500,1)
$strict=$pre.Copy()
$scoped=$pre.Copy()
$resolve=$policy.GetType().GetMethod('ResolveCore',[Reflection.BindingFlags]'NonPublic,Instance')
$scope=$policy.GetType().Assembly.GetType('Decennium.Foundation.Laboratory.ConditionResolutionScope',$true)
$enter=$scope.GetMethod('Enter',[Reflection.BindingFlags]'NonPublic,Static')
$failure=$resolve.Invoke($policy,[object[]]@($strict,$advance,$false,$false,$null))
if ($null -ne $failure) { throw $failure }
$context=$enter.Invoke($null,[object[]]@($true))
try {
    $failure=$resolve.Invoke($policy,[object[]]@($scoped,$advance,$false,$false,$null))
    if ($null -ne $failure) { throw $failure }
} finally { $context.Dispose() }
Commit $advance
$after=$simulation.Capture()
foreach ($candidate in $strict,$scoped) {
    $candidate.Revision=$after.Revision
    $candidate.Receipts=$after.Receipts
}
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$strictBytes=$codec.Encode($strict)
$scopedBytes=$codec.Encode($scoped)
$strictDigest=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($strictBytes))
$scopedDigest=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($scopedBytes))
if ($strictDigest -cne $scopedDigest) { throw 'Cached and uncached expiry/work diverged.' }
$journal=$after.Conditions | Where-Object Target -eq $worker
if ($after.FormulaWork[0].Work.Labor.ToString() -ne '500/1' -or $after.Intakes[0].Status -ne 'Complete' -or
    [Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($after,$worker).View().Has('Poisoned')) {
    throw 'The real command history did not exercise both work procedures and expiry.'
}
$store=[Decennium.Foundation.FileSaveStore]::new()
$store.Save("$Run/expiry-parallel-pre.ddsave",$pre)
$store.Save("$Run/expiry-parallel-post.ddsave",$after)
[ordered]@{Status='PASS'; Mode='Real admitted standalone condition/work history; scoped detached resolver equivalence'
    ResearchLabor=$after.FormulaWork[0].Work.Labor.ToString(); Intake=$after.Intakes[0].Status.ToString()
    ConditionOperations=@($journal.Operations | ForEach-Object {"$($_.Id) at $($_.At.Time)"})
    ScopedSha256=$scopedDigest.ToLowerInvariant(); StrictSha256=$strictDigest.ToLowerInvariant()} |
    ConvertTo-Json -Depth 6 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
