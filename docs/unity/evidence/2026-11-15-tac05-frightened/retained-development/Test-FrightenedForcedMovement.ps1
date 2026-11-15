param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
$type=[Decennium.Foundation.Tests.FoundationCases];$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$name,[object[]]$arguments){try{$type.GetMethod($name,$flags).Invoke($null,$arguments)}catch{throw $_.Exception.InnerException}}
$seed=Call 'SeedForNatural' @([int]10)
$fixture=[Decennium.Foundation.Laboratory.OverwatchExecutionFixture]::new($true,$true,$true,'None',-100)
$policy=Call 'OverwatchExecutionPolicy' @([uint32]$seed,$fixture,$null,$null,[long]26)
$simulation=Call 'OverwatchTrigger' @($policy)
$response=Call 'OverwatchResponse' @($simulation,$true)
Call 'WorldCommit' @($simulation,$response)
$command=Call 'OverwatchRiderCommand' @($simulation,[Decennium.Foundation.OverwatchRider]::Push)
$candidate=$simulation.Capture()
$target='TEST_ONLY.third-combatant';$feared='TEST_ONLY.companion'
$body=$candidate.Actors|Where-Object Id -eq $target;$body.X=1;$body.Y=0
$source=$candidate.Actors|Where-Object Id -eq $feared;$source.X=3;$source.Y=0
$index=[Array]::FindIndex($candidate.Conditions,[Predicate[Decennium.Foundation.ConditionJournal]]{param($j)$j.Target-eq$target})
$old=$candidate.Conditions[$index]
$journal=[Decennium.Foundation.ConditionJournal]::new([Decennium.Foundation.ConditionJournal]::RelationshipPolicyId,$old.Target,$old.Origin,$old.Operations)
$history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($journal)
$history=$history.Append([Decennium.Foundation.ConditionOperation]::Advance('TEST_ONLY.forced-sync',[Decennium.Foundation.ConditionStamp]::new($candidate.RuleClock))).State
$fear=[Decennium.Foundation.FrightenedRelationshipData]::new($feared,'TEST_ONLY.forced-test-use','TEST_ONLY.detached-source-revision')
$application=[Decennium.Foundation.ConditionApplicationData]::new('TEST_ONLY.forced-test-fear','TEST_ONLY.detached-owner',
    'TEST_ONLY.detached-source','Frightened',[Decennium.Foundation.ConditionStamp]::new($candidate.RuleClock.AddSeconds(6)),'expiry',$true,10,$null,$null,$fear)
$history=$history.Append([Decennium.Foundation.ConditionOperation]::Apply('TEST_ONLY.forced-test-fear',$history.Journal.Now,$application)).State
$candidate.Conditions[$index]=$history.Journal
$rules=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy].Assembly.GetType('Decennium.Foundation.Laboratory.FrightenedRules',$true)
$point=[ValueTuple[Decennium.Foundation.RuleQuantity,Decennium.Foundation.RuleQuantity]]::new([Decennium.Foundation.RuleQuantity]::new(2),[Decennium.Foundation.RuleQuantity]::new(0))
$denial=$rules.GetMethod('WillingStepFailure',$flags).Invoke($null,@($candidate,$target,$point))
Require ($denial-eq'FrightenedPreventsWillingApproach') 'The comparison movement must be a prohibited willing approach.'
$before=$candidate.RandomState;$moves=$candidate.TacticalMoves.Length;$attacks=$candidate.MeleeAttacks.Length
$resolve=$policy.GetType().GetMethod('ResolveOverwatchRiderChoice',[Reflection.BindingFlags]'Instance,NonPublic')
try{$failure=$resolve.Invoke($policy,@($candidate,$command))}catch{throw $_.Exception.GetBaseException()}
Require ($null-eq$failure) "Existing authoritative Push component rejected: $failure"
$result=$candidate.OverwatchRiderChoices[-1]
Require (!$result.SaveSucceeded-and$result.MovedFeet-eq5-and$result.FromX-eq1-and$result.ToX-eq2-and
    ($candidate.Actors|Where-Object Id -eq $target).X-eq2-and$candidate.TacticalMoves.Length-eq$moves-and$candidate.MeleeAttacks.Length-eq$attacks) 'Push did not bypass only the willing restriction without ordinary movement reactions.'
$expected=[Decennium.Foundation.Laboratory.PlaytestDice]::RollD20($before)
Require ($result.SaveNatural-eq$expected.Natural-and$candidate.RandomState-eq$expected.NextRandomState-and$result.RandomWordsConsumed-eq$expected.WordsConsumed) 'Fear altered the existing forced-move Strength save dice.'
Require (@($command.GetType().GetProperties()|Where-Object Name -Match 'Forced').Count-eq0) 'Ordinary typed commands unexpectedly expose a forced-movement switch.'
[ordered]@{status='PASS';scope='DETACHED_EXISTING_PUSH_PRODUCER_NOT_CONNECTED_ACQUISITION';assemblyRoot=$AssemblyRoot;seed=$seed;
    baseline='Existing OverwatchExecutionCases fixture with explicit TEST_ONLY additionalStrengthSaveModifier=-100';
    detachedChanges=@('After actual offered/paid shot, relocate target and independent feared actor for the component comparison.','Use the explicit v2 relationship journal on the detached legacy fixture candidate.');
    willingDenial=$denial;forcedMovement=$result;noPublicForcedFlag=$true
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output 'PASS: existing forced Push bypasses fear willing-approach restriction and preserves normal save dice.'
