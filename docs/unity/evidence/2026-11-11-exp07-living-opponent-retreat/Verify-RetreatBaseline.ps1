param([string]$AssemblyRoot,[string]$AdmittedSave,[string]$ReportPath)
$ErrorActionPreference='Stop'
$assemblies=@('Core','Persistence','LabModel','HeadlessTests'|ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
foreach($assembly in $assemblies){Add-Type -Path $assembly}
$fixture=[Decennium.Foundation.Tests.FoundationCases]
$flags=[Reflection.BindingFlags]'Static,NonPublic'
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$laboratory=[Decennium.Foundation.ExecutionProfile]::Laboratory
function Invoke-Fixture([string]$Name,[object[]]$Arguments){
    try { $fixture.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Hash-Bytes([byte[]]$Bytes){
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}
function Assert-True([bool]$Condition,[string]$Message){
    if(-not $Condition){throw $Message}
}
$bytes=[IO.File]::ReadAllBytes((Resolve-Path $AdmittedSave).Path)
$policy=Invoke-Fixture 'ReinforcementPolicy' @($null,$null,[Decennium.Foundation.Laboratory.TerrainCost]::Normal,$null)
$sim=[Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),$laboratory)
$authority=Invoke-Fixture 'LaterHost' @()
$before=$sim.Capture()
$hero=$before.Reinforcement.Definition.AllyId
$companion=$before.Reinforcement.Definition.CompanionId
$defender=$before.LaterEncounter.Definition.DefenderId
$club=$before.LaterEncounter.Definition.DefenderClubId
$encounterId=$before.Encounter.Id
$kinds=[Decennium.Foundation.CommandKind]
$ordinary=[Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
$press=[Decennium.Foundation.PressHitInstruction]::KeepExisting
$log=[Collections.Generic.List[object]]::new()
function Tactical([Decennium.Foundation.CommandKind]$Kind,[string]$Target,[int]$X=0,[int]$Y=0,[string]$Weapon=''){
    Invoke-Fixture 'Tac' @($sim,$Kind,$Target,$null,$X,$Y,$Weapon,$false,$ordinary,0,$press)
}
function Commit($Command){
    $r=$sim.Execute($authority,$Command)
    Assert-True ($r.Outcome.ToString() -eq 'Committed') "$($Command.Kind) at $($Command.ExpectedRevision) returned $($r.Outcome)/$($r.Code)"
    $state=$sim.Capture()
    $log.Add([ordered]@{kind=$Command.Kind.ToString();id=$Command.Id;actor=$Command.Actor;target=$Command.Target;
        at=$state.RuleClock.ToString();revision=$state.Revision;rng=$state.RandomState})
}
function Step-Tactical([int]$X,[int]$Y){
    Commit (Tactical $kinds::TacticalStep ($sim.Capture().Encounter.CurrentTurnId) $X $Y)
    while([Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($sim.Capture())){
        Commit (Invoke-Fixture 'Opportunity' @($sim,$false,'',$ordinary,[Decennium.Foundation.PressHitInstruction]::ArmOrReplace))
    }
}
function End-Turn {
    Commit (Tactical $kinds::EndRegularTurn ($sim.Capture().Encounter.CurrentTurnId))
}
function Guard {
    $null=Invoke-Fixture 'LaterStance' @($sim,[Decennium.Foundation.CombatStance]::Guarded)
}
function Point($Snapshot,[string]$Actor){
    $position=[Decennium.Foundation.WorldPositionResolver]::Position($Snapshot,$Actor)
    @($position.Item1.ToString(),$position.Item2.ToString())
}
Assert-True ((Hash-Bytes ($codec.Encode($before))) -eq (Hash-Bytes $bytes) -and $before.Encounter.Round -eq 2 -and
     $before.Encounter.CurrentActor -eq $companion) 'Expected authentic round-2 reinforced start'
Assert-True ($before.ExpeditionPressureCohorts.Length -eq 0 -and $before.ExpeditionPressureExposures.Length -eq 0) 'Expected current Pressure authority gap'
$rounds=[Collections.Generic.List[object]]::new()
foreach($step in 1..3){
    $start=$sim.Capture()
    Assert-True ($start.Encounter.CurrentActor -eq $companion) 'Unexpected companion Start'
    Guard
    Step-Tactical 1 (3-$step)
    End-Turn
    Assert-True ($sim.Capture().Encounter.CurrentActor -eq $defender) 'Unexpected defender Start'
    Guard
    if($step -gt 1){ Step-Tactical 0 (5-$step) }
    $attackBefore=$sim.Capture()
    Commit (Tactical $kinds::AttackClub $hero 0 0 $club)
    $attackAfter=$sim.Capture()
    $attack=$attackAfter.MeleeAttacks[-1]
    Assert-True ($attack.AttackerId -eq $defender -and $attack.TargetId -eq $hero -and $attackAfter.RandomState -ne $attackBefore.RandomState) 'The actual Club threat did not resolve'
    End-Turn
    Assert-True ($sim.Capture().Encounter.CurrentActor -eq $hero) 'Unexpected hero Start'
    Guard
    Step-Tactical 0 (3-$step)
    End-Turn
    $end=$sim.Capture()
    Assert-True ($end.Encounter.Id -eq $encounterId -and $end.Encounter.Round -eq $start.Encounter.Round+1) 'Encounter or round continuity changed'
    $rounds.Add([ordered]@{round=$start.Encounter.Round;start=$start.RuleClock.ToString();end=$end.RuleClock.ToString();
        hero=@(Point $end $hero);companion=@(Point $end $companion);defender=@(Point $end $defender);
        heroHp=($end.Lives|Where-Object ActorId -EQ $hero).Hp;defenderHp=($end.Lives|Where-Object ActorId -EQ $defender).Hp;
        threatId=$attack.Id;threatHit=$attack.Attack.Hit})
}
$atExit=$sim.Capture()
$hash=Hash-Bytes ($codec.Encode($atExit))
$exit=Tactical $kinds::EndFixedEncounter $atExit.Encounter.CurrentTurnId
$denied=$sim.Execute($authority,$exit)
Assert-True ($denied.Outcome.ToString() -eq 'Rejected' -and $denied.Code -eq 'ConflictNotResolved' -and
     (Hash-Bytes ($codec.Encode($sim.Capture()))) -eq $hash) 'Expected unchanged living-opponent exit rejection'

$routes=Invoke-Fixture 'RouteTravelCheckpointFixture' @()
$combinedPolicy=Invoke-Fixture 'ReinforcementPolicy' @($null,$null,[Decennium.Foundation.Laboratory.TerrainCost]::Normal,$null)
$null=$combinedPolicy.EnableExpeditionRouteTravel($routes)
$pressureFixture=[Decennium.Foundation.Laboratory.TestOnlyExpeditionPressureFixture]::new(
    'TEST_ONLY.retreat-baseline.pressure',$hero,0,[string[]]@([Decennium.Foundation.Laboratory.TestOnlyCropPolicy]::PlotId))
$null=$combinedPolicy.EnableExpeditionPressure($pressureFixture)
$compositionFailure=$null
try { $null=[Decennium.Foundation.Simulation]::new($combinedPolicy,$combinedPolicy.Initial(),$laboratory) }
catch { $compositionFailure=$_.Exception.GetBaseException().Message }
Assert-True ($compositionFailure -eq 'RouteTravelSchemaMismatch') "Unexpected ordinary Pressure composition result: $compositionFailure"
$twoMemberFailure=$null
try {
    $null=[Decennium.Foundation.ExpeditionPressureCohortRecord]::new('TEST_ONLY.retreat-baseline.pressure',
        $before.ContentFingerprint,$routes.Fingerprint,0,[string[]]@($hero,$companion))
} catch { $twoMemberFailure=$_.Exception.GetBaseException().Message }
Assert-True ($twoMemberFailure -eq 'Invalid fixed expedition-pressure cohort.') "Unexpected two-member cohort result: $twoMemberFailure"
$lead=[Decennium.Foundation.Laboratory.CharacterRuleFacts]::ForActor($before,$hero)
$leadDex=$lead.AbilityModifier([Decennium.Foundation.CharacterAbility]::Dexterity)


$adverseLog=[Collections.Generic.List[object]]::new()
$ordinaryTrace=$log
$log=$adverseLog
$sim=[Decennium.Foundation.Simulation]::new((Invoke-Fixture 'ReinforcementPolicy' @($null,$null,[Decennium.Foundation.Laboratory.TerrainCost]::Normal,$null)),
    $codec.Decode($bytes),$laboratory)
foreach($step in 1..2){
    Guard
    Step-Tactical 1 (3-$step)
    End-Turn
    Guard
    if($step -eq 2){
        Step-Tactical 0 3
        Step-Tactical 1 2
    }
    Commit (Tactical $kinds::AttackClub $hero 0 0 $club)
    End-Turn
    Guard
    Step-Tactical 0 (3-$step)
    End-Turn
}
$adverse=$sim.Capture()
$fork=@(Point $adverse $defender)
Assert-True (($fork -join ',') -eq '1/1,2/1' -and $adverse.Encounter.Id -eq $encounterId) 'Expected live opponent at the reached fork'

[ordered]@{status='PASS';authority='schema 87 TEST_ONLY ordinary route and live opposition baseline';admittedSaveSha256=Hash-Bytes $bytes;
    encounter=$encounterId;start=$before.RuleClock.ToString();end=$atExit.RuleClock.ToString();rounds=$rounds;
    commandTrace=$ordinaryTrace;adverseFork=@{at=$adverse.RuleClock.ToString();hero=@(Point $adverse $hero);
        companion=@(Point $adverse $companion);defender=$fork;trace=$adverseLog};liveExitCode=$denied.Code;unchangedAfterExitRejection=$true;
    pressureCohorts=$atExit.ExpeditionPressureCohorts.Length;pressureExposures=$atExit.ExpeditionPressureExposures.Length;
    pressureCompositionRejected=$compositionFailure;twoMemberCohortRejected=$twoMemberFailure;
    candidateLead=@{id=$hero;dexterityModifier=$leadDex;proposedSkillBinding='none'};
    assemblies=@($assemblies|ForEach-Object {[ordered]@{name=Split-Path $_ -Leaf;sha256=(Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant()}})} |
    ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ReportPath -Encoding utf8
'PASS: three real rounds of paid lane movement, three actual opposing Club attacks, and living-opponent exit rejection.'
