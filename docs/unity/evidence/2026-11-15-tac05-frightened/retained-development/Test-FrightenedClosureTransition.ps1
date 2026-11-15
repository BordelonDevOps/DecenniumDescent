param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$AfterCheckSave,[Parameter(Mandatory)][string]$BeforeFinalSave,[Parameter(Mandatory)][string]$FourthUseAttemptSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($value,[string]$message){if(!$value){throw $message}}
$store=[Decennium.Foundation.FileSaveStore]::new();$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero;$npc=[Decennium.Foundation.FrightenedProfile]::Actor
$type=[Decennium.Foundation.Tests.FoundationCases];$flags=[Reflection.BindingFlags]'Static,NonPublic'
$session=$type.GetMethod('NewFrightenedExpedition',$flags).Invoke($null,@())
$policy=$type.GetMethod('ClericPolicy',$flags).Invoke($null,@($session))
function Fear($s){[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$hero).View().Has([Decennium.Foundation.Laboratory.ConditionKind]::Frightened)}
function Dead-Source($path){
    $s=$store.Load((Resolve-Path -LiteralPath $path).Path)
    $index=[Array]::FindIndex($s.Lives,[Predicate[Decennium.Foundation.ActorLifeRecord]]{param($x)$x.ActorId-eq$npc})
    $life=$s.Lives[$index]
    # Explicit detached setup only. No claim that these life facts were earned by commands.
    $s.Lives[$index]=[Decennium.Foundation.ActorLifeRecord]::new($life.ActorId,$life.MaximumHp,0,0,$life.LinkedInjuries,$false,$true,$life.UsesDeathSaves,0,3,$null,$life.LastDeathTurn,$true,[string[]]@())
    return $s
}
function Record($s,[string]$name){
    $journal=@($s.Conditions|Where-Object Target -eq $hero)[0]
    $ledger=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($journal).Ledger
    [ordered]@{scope='DETACHED_ACTUAL_SHARED_CLOSURE_PATH';revision=$s.Revision;clock=$s.RuleClock.ToString();randomState=$s.RandomState;
        inventoryCombat=$s.InventoryCombat;encounterPresent=$null-ne$s.Encounter;closed=@($s.ClosedEncounters|Select-Object ClosedRevision,ClosedAt,Reason);
        sourceLife=@($s.Lives|Where-Object ActorId -eq $npc);targetFearOperative=(Fear $s);
        relationships=@($ledger.Applications|Where-Object {$_.Application.Kind.ToString()-eq'Frightened'}|ForEach-Object{@{id=$_.Id;endedAt=$_.EndedAt;present=$_.Present($ledger.Now);application=$_.Application}});
        timings=$s.FrightenedTimings;saves=$s.FrightenedSaves;calendar=$s.Reinforcement.Admission.Phase.Epoch
    }|ConvertTo-Json -Depth 15|Set-Content -LiteralPath (Join-Path $Run ($name+'.json')) -Encoding utf8
}
function Close($s,[string]$id){
    $command=[Decennium.Foundation.Command]::new($id,$hero,$s.Revision,[Decennium.Foundation.CommandKind]::EndFixedEncounter,$s.Encounter.CurrentTurnId)
    $result=$policy.Resolve($s,$command)
    Require ($null-eq$result) "Detached actual closure rejected: $result"
    Require (!$s.InventoryCombat-and$null-eq$s.Encounter) 'Actual closure path did not leave combat'
}
$candidate=Dead-Source $AfterCheckSave
$timing=@($candidate.FrightenedTimings|Where-Object TargetId -eq $hero)[0]
$beforeSaves=$candidate.FrightenedSaves.Count;$beforeClosed=$candidate.ClosedEncounters.Count
Require (Fear $candidate) 'Dead source unexpectedly ended relationship before closure'
Record $candidate 'before-repeat-closure'
Close $candidate 'TEST_ONLY.detached.close-at-repeat'
$repeat=@($candidate.FrightenedSaves|Where-Object {$_.Repeat-and$_.ApplicationId-eq$timing.ApplicationId})[0]
Require ($null-ne$repeat-and!$repeat.Success-and$repeat.Natural-eq3-and$repeat.Second-eq0) 'Actual due ordinary repeat did not fail as expected'
Require ($candidate.FrightenedSaves.Count-eq$beforeSaves+1-and$candidate.RuleClock-eq$timing.RepeatAt.Time-and(Fear $candidate)) 'Failed repeat did not retain same fear after actual closure'
Require ($candidate.ClosedEncounters.Count-eq$beforeClosed+1-and$candidate.FrightenedTimings.Where({$_.ApplicationId-eq$timing.ApplicationId})[0].FinalAt.Equals($timing.FinalAt)) 'Closure changed source deadline or failed to record exit'
Record $candidate 'after-repeat-closure'
$rng=$candidate.RandomState;$count=$candidate.FrightenedSaves.Count
$command=[Decennium.Foundation.Command]::new('TEST_ONLY.detached.ordinary-final',$hero,$candidate.Revision,[Decennium.Foundation.CommandKind]::AdvanceClock,'',6,1)
$result=$policy.Resolve($candidate,$command)
Require ($null-eq$result) "Ordinary post-closure clock rejected: $result"
Require ($candidate.RuleClock-eq$timing.FinalAt.Time-and!(Fear $candidate)-and$candidate.RandomState-eq$rng-and$candidate.FrightenedSaves.Count-eq$count) 'Ordinary final expiry changed RNG, repeated save or deadline'
Record $candidate 'ordinary-final-expiry'
$candidate=Dead-Source $BeforeFinalSave
$timing=@($candidate.FrightenedTimings|Where-Object TargetId -eq $hero)[0];$rng=$candidate.RandomState;$count=$candidate.FrightenedSaves.Count
Require (Fear $candidate) 'Final closure setup lacks present relationship'
Record $candidate 'before-final-closure'
Close $candidate 'TEST_ONLY.detached.close-at-final'
Require ($candidate.RuleClock-eq$timing.FinalAt.Time-and!(Fear $candidate)-and$candidate.RandomState-eq$rng-and$candidate.FrightenedSaves.Count-eq$count) 'Final endpoint during closure failed or rolled again'
Record $candidate 'after-final-closure'
# Separately retain a genuine public-host failure without altering any life, RNG or position.
$FourthUseAttemptSave=(Resolve-Path -LiteralPath $FourthUseAttemptSave).Path
$session.Restore($FourthUseAttemptSave);$before=Join-Path $Run 'genuine-fourth-before-denial.ddsave';$session.Save($before)
$s=$store.Load($before);$life=@($s.Lives|Where-Object ActorId -eq $npc)[0]
Require ($s.Revision-eq206-and$life.Hp-eq0-and!$life.Dead) 'Wrong genuine fourth-use attempt'
$command=[Decennium.Foundation.Command]::new('fear.actual.closure-denied',$hero,$s.Revision,[Decennium.Foundation.CommandKind]::EndFixedEncounter,$s.Encounter.CurrentTurnId)
$result=$session.SubmitSessionCommand($command)
Require ($result.Response-eq'Unavailable') 'Genuine unresolved source closure should reject'
$after=Join-Path $Run 'genuine-fourth-after-denial.ddsave';$session.Save($after)
Require ((Get-FileHash -LiteralPath $before).Hash-ceq(Get-FileHash -LiteralPath $after).Hash) 'Genuine closure denial changed bytes'
[ordered]@{status='PASS';guidanceResponse='bd6e3553-7534-5fdb-9883-e2426d85c097';assemblyRoot=$AssemblyRoot;
    connectedIntersection='not demonstrated; reviewed scope exception';
    detachedChanges='Only source ActorLifeRecord replaced with explicit dead, HP0, death-failures3, prone, no held items; source conditions, target relationships, source uses, RNG and retained calendars/endpoints remain from genuine saves. This is no connected acquisition or defeat history.';
    actualPath='TestOnlySharedWorldPolicy.Resolve -> EndFixedEncounter -> normal outgoing-slot AdvanceTo -> RecordActualCombatExit';
    repeatClosure='ordinary repeat3 fails; same application remains after closure with unchanged final deadline';
    ordinaryFinal='six subsequent ordinary seconds reach final endpoint; no third save or RNG draw';
    finalClosure='outgoing slot reaches final endpoint; expiry occurs during actual closure with no third save or RNG draw';
    genuineDenial=@{revision=206;response=$result.Response.ToString();unchangedSha256=(Get-FileHash -LiteralPath $after).Hash.ToLowerInvariant()};
    inputs=@($AfterCheckSave,$BeforeFinalSave,$FourthUseAttemptSave)|ForEach-Object{@{path=(Resolve-Path -LiteralPath $_).Path;sha256=(Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant()}}
}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output 'PASS: detached actual closure repeat/final/ordinary continuation and genuine unchanged closure denial.'
