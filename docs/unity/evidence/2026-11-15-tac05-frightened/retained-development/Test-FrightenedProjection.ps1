param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ActiveSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
$s=[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path -LiteralPath $ActiveSave).Path)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero;$npc=[Decennium.Foundation.FrightenedProfile]::Actor
$dead='TEST_ONLY.third-combatant'
Require (($s.Lives|Where-Object ActorId -eq $dead).Dead) 'Retained feared-actor control requires an actually dead world actor.'
$index=[Array]::FindIndex($s.Conditions,[Predicate[Decennium.Foundation.ConditionJournal]]{param($j)$j.Target-eq$hero})
$history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($s.Conditions[$index])
$first=($s.FrightenedTimings|Where-Object TargetId -eq $hero).ApplicationId
$relationship=[Decennium.Foundation.FrightenedRelationshipData]::new($dead,'TEST_ONLY.independent-use','TEST_ONLY.detached-source-revision')
$application=[Decennium.Foundation.ConditionApplicationData]::new('TEST_ONLY.independent-fear','TEST_ONLY.other-owner',
    'TEST_ONLY.independent-source','Frightened',[Decennium.Foundation.ConditionStamp]::new($s.RuleClock.AddSeconds(12)),
    'source-end',$true,10,$null,$null,$relationship)
$history=$history.Append([Decennium.Foundation.ConditionOperation]::Apply('TEST_ONLY.independent-fear',$history.Journal.Now,$application)).State
$s.Conditions[$index]=$history.Journal
$view=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$hero).View()
Require ($view.Sources([Decennium.Foundation.Laboratory.ConditionKind]::Frightened).Count-eq2) 'Independent fear sources collapsed.'
$rules=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy].Assembly.GetType('Decennium.Foundation.Laboratory.FrightenedRules',$true)
$flags=[Reflection.BindingFlags]'Static,NonPublic'
$visible=$rules.GetMethod('VisibleSource',$flags)
$willing=$rules.GetMethod('WillingStepFailure',$flags)
$seen=$visible.Invoke($null,@($s,$hero))
Require $seen 'One visible source must suffice even when another is hidden.'
$target=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$npc).View().Clauses
$modifier=[Decennium.Foundation.Laboratory.PlaytestConditions]::Attack($view.Clauses,$target,5,'Melee',0,$false,$false,$false,$false,$true,$true,$false)
Require ($modifier.AdvantagePresent-and$modifier.DisadvantagePresent) 'Fear did not compose with an independent advantage.'
$roll=[Decennium.Foundation.Laboratory.PlaytestDice]::RollD20($s.RandomState,1,1)
Require ($roll.Selection-eq'Normal'-and$null-eq$roll.Second-and$roll.WordsConsumed-eq1) 'Multiple fear sources overrode ordinary advantage/disadvantage cancellation.'
$point=[ValueTuple[Decennium.Foundation.RuleQuantity,Decennium.Foundation.RuleQuantity]]::new(
    [Decennium.Foundation.RuleQuantity]::new(1),[Decennium.Foundation.RuleQuantity]::new(1))
Require ($willing.Invoke($null,@($s,$hero,$point))-eq'FrightenedPreventsWillingApproach') 'Moving farther from one source concealed approach to the independent source.'
$history=$history.Append([Decennium.Foundation.ConditionOperation]::End('TEST_ONLY.end-first',$history.Journal.Now,$first,'TEST_ONLY.detached-end')).State
$s.Conditions[$index]=$history.Journal
Require (!$visible.Invoke($null,@($s,$hero))) 'The surviving source should be unseen behind the actual blocker.'
Require ($history.Ledger.View().Sources([Decennium.Foundation.Laboratory.ConditionKind]::Frightened).Count-eq1-and
    $willing.Invoke($null,@($s,$hero,$point))-eq'FrightenedPreventsWillingApproach') 'An unseen dead feared actor was implicitly cured or lost its retained geometry.'
$modifier=[Decennium.Foundation.Laboratory.PlaytestConditions]::Attack($history.Ledger.View().Clauses,$target,5,'Melee',0,$false,$false,$false,$false,$false,$false,$false)
Require (!$modifier.DisadvantagePresent) 'An unseen feared source continued imposing attack disadvantage.'
[ordered]@{status='PASS';scope='DETACHED_RELATIONSHIP_CONSUMERS_NOT_SOURCE_ACQUISITION';sourceSave=(Resolve-Path -LiteralPath $ActiveSave).Path;
    sourceSha256=(Get-FileHash -LiteralPath $ActiveSave).Hash.ToLowerInvariant();assemblyRoot=$AssemblyRoot;
    detachedChanges=@('Adds one independent test fear of an actually dead retained world actor.','Ends only the original source application through the shared journal.');
    checks=@('Independent sources remain distinct.','Any visible source supplies the single fear penalty.','Ordinary advantage cancels fear disadvantage with one die.',
        'Farther from one source does not permit approach to another.','Ending one record preserves the other.','An unseen dead source retains movement restriction but no attack penalty.')
}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output 'PASS: independent-source, cancellation, unseen and dead-source projections.'
