param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ActiveSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
$flags=[Reflection.BindingFlags]'Static,NonPublic';$type=[Decennium.Foundation.Tests.FoundationCases]
$session=$type.GetMethod('NewFrightenedExpedition',$flags).Invoke($null,@())
$policy=$type.GetMethod('ClericPolicy',$flags).Invoke($null,@($session))
$advance=$policy.GetType().GetMethod('AdvanceTo',[Reflection.BindingFlags]'Instance,NonPublic')
$source=[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path -LiteralPath $ActiveSave).Path)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
function Q([long]$n,[long]$d=1){[Decennium.Foundation.RuleQuantity]::new($n,$d)}
function T([long]$n,[long]$d=1){[Decennium.Foundation.RuleTime]::new($n,$d)}
function Add-Time($at,[long]$n,[long]$d=1){T ($at.Numerator*$d+$n*$at.Denominator) ($at.Denominator*$d)}
function Stamp($time){[Decennium.Foundation.ConditionStamp]::new($time)}
function Outside-Candidate {
    $s=$source.Copy();$s.InventoryCombat=$false;$s.Encounter=$null;$s.InventoryTurnActor='';$s.InventoryInteractions=0
    return $s
}
function Advance($s,$target){
    $command=[Decennium.Foundation.Command]::new('TEST_ONLY.detached-clock',$hero,$s.Revision,[Decennium.Foundation.CommandKind]::AdvanceClock,'',1,1)
    try{$result=$advance.Invoke($policy,@($s,$target,$false,$command,$null))}catch{throw $_.Exception.InnerException}
    Require ($null-eq$result) "Detached shared clock refused: $result"
}
function Fear-Semantics($s){
    $conditions=@($s.Conditions|ForEach-Object{
        $ledger=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($_).Ledger
        @{target=$_.Target;now=$_.Now;applications=@($ledger.Applications|ForEach-Object{
            @{id=$_.Id;ended=$_.EndedAt;suppressed=$_.Suppressed;present=$_.Present($ledger.Now);application=$_.Application}
        })}
    })
    @{clock=$s.RuleClock;rng=$s.RandomState;saves=$s.FrightenedSaves;recharge=$s.AbilityRecharges;
        intervals=$s.WorldIntervals;edges=$s.WorldTraversals;actors=$s.Actors;conditions=$conditions}|ConvertTo-Json -Depth 16 -Compress
}
$bounds=$policy.GetType().GetMethod('BoundFrightenedTraversal',[Reflection.BindingFlags]'Instance,NonPublic')
$motion=[Collections.Generic.List[object]]::new()
foreach($scenario in 'source-approaches-retreating-target','source-retreats-from-approaching-target','source-approaches-stationary-target'){
    $candidate=Outside-Candidate;$edges=[Collections.Generic.List[Decennium.Foundation.WorldTraversalRecord]]::new()
    $away=$scenario-eq'source-retreats-from-approaching-target'
    if($scenario-ne'source-approaches-stationary-target'){
        $destination=if($away){3}else{1}
        $edges.Add([Decennium.Foundation.WorldTraversalRecord]::new($hero,$candidate.Revision,0,2,0,$destination))
    }
    $destination=if($away){4}else{2}
    $edges.Add([Decennium.Foundation.WorldTraversalRecord]::new([Decennium.Foundation.FrightenedProfile]::Actor,$candidate.Revision,0,3,0,$destination))
    $candidate.WorldTraversals=$edges.ToArray();$next=Add-Time $candidate.RuleClock 1 10
    $arguments=[object[]]@($candidate,$next,$null);$boundary=$bounds.Invoke($policy,$arguments)
    $suspended=[string[]]$arguments[2]
    Require ($(if($away){$boundary-eq$candidate.RuleClock-and$suspended.Count-eq1-and$suspended[0]-eq$hero}else{$boundary-eq$next-and$suspended.Count-eq0})) "Shared moving-edge attribution failed: $scenario"
    $motion.Add(@{case=$scenario;boundary=$boundary.ToString();suspended=$suspended})
}
$whole=Outside-Candidate;$split=Outside-Candidate
$last=Add-Time $source.RuleClock 18
Advance $whole $last
foreach($seconds in 2,4,6,10,12,18){Advance $split (Add-Time $source.RuleClock $seconds)}
$wholeSemantics=Fear-Semantics $whole;$splitSemantics=Fear-Semantics $split
$wholeSemantics|Set-Content -LiteralPath (Join-Path $Run 'whole-semantics.json') -Encoding utf8
$splitSemantics|Set-Content -LiteralPath (Join-Path $Run 'split-semantics.json') -Encoding utf8
Require ($wholeSemantics-ceq$splitSemantics) 'Whole/split retained-calendar condition, RNG, recharge or spending semantics differ.'
Require ($whole.AbilityRecharges[0].Remaining-eq0-and@($whole.FrightenedSaves|Where-Object Repeat).Count-eq2) 'Whole/split did not cover all repeat saves and three owner starts.'
$s=Outside-Candidate
$body=$s.Actors|Where-Object Id -eq $hero;$body.X=0;$body.Y=1
$s.WorldTraversals=[Decennium.Foundation.WorldTraversalRecord[]]@([Decennium.Foundation.WorldTraversalRecord]::new($hero,$s.Revision,0,1,0,2,(Q 2)))
$index=[Array]::FindIndex($s.Conditions,[Predicate[Decennium.Foundation.ConditionJournal]]{param($j)$j.Target-eq$hero})
$history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($s.Conditions[$index])
$wardEnd=Add-Time $s.RuleClock 3 10
$ward=[Decennium.Foundation.ConditionImmunityData]::new('TEST_ONLY.edge-ward','TEST_ONLY.detached','TEST_ONLY.detached-ward',[string[]]@('Frightened'),(Stamp $wardEnd),'expiry',$true)
$history=$history.Append([Decennium.Foundation.ConditionOperation]::Grant('TEST_ONLY.edge-ward',(Stamp $s.RuleClock),$ward)).State
$s.Conditions[$index]=$history.Journal
$prior=($s.WorldIntervals|Where-Object ActorId -eq $hero).MovementSpent
$beforeRng=$s.RandomState
Advance $s (Add-Time $s.RuleClock 1)
$edge=$s.WorldTraversals|Where-Object ActorId -eq $hero
$spent=($s.WorldIntervals|Where-Object ActorId -eq $hero).MovementSpent
Require ($edge.Status-eq'Suspended'-and$edge.DistanceFeet-eq(Q 3)-and$spent-eq($prior+(Q 1))-and$s.RandomState-eq$beforeRng) 'Immunity expiry did not suspend the paid partial edge at the exact lawful boundary.'
Require ([Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$hero).View().Has([Decennium.Foundation.Laboratory.ConditionKind]::Frightened)) 'The relationship did not become operative after the ward expired.'
(Fear-Semantics $s)|Set-Content -LiteralPath (Join-Path $Run 'pending-edge-semantics.json') -Encoding utf8
[ordered]@{status='PASS';scope='DETACHED_SHARED_CLOCK_COMPONENTS_NOT_CONNECTED_CLOSURE';sourceSave=(Resolve-Path -LiteralPath $ActiveSave).Path;
    sourceSha256=(Get-FileHash -LiteralPath $ActiveSave).Hash.ToLowerInvariant();assemblyRoot=$AssemblyRoot;
    detachedChanges=@('Outside-combat envelope over retained calendars without claiming lawful closure.','Pending-edge control changes hero anchor, adds a2-foot edge and an explicit temporary test immunity.');
    movingEdgeAttribution=@($motion);movingEdgeScope='Detached simultaneous-edge geometry only; concurrent public traversal and overlapping endpoint claims are not admitted by this profile.';
    wholeSplit='repeat/final endpoints, RNG and recharge agree across18seconds';partialEdge='ward expiry at3/10second:2feet becomes3feet,1foot paid, suspended without refund';
    whole=(Join-Path $Run 'whole-semantics.json');split=(Join-Path $Run 'split-semantics.json')
}|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output 'PASS: detached whole/split clock and exact immunity-expiry edge suspension.'
