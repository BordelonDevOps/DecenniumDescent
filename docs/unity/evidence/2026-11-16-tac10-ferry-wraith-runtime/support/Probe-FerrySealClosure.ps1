param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run,[int]$TearAfterAttempts=3,[switch]$AggressiveAfterTear)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh seal-closure branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Genuine alternate combat: leave physical seal intact until a late paid tear, kill and close while suppressed; preserve original endpoint through paid ordinary expiry and reject reuse';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();restorePairs=@();probes=@();observations=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerrySealClosure.executed.ps1')
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave);$field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$after=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($after)
        Require ((Digest $path)-ceq(Digest $after)) "Strict restore changed $name."
        $report.restorePairs+=@{name=$name;sha256=(Digest $path)}
    }
    function Send($command,$hostCommand=$false){
        $response=if($hostCommand){$session.SubmitSessionCommand($command)}else{$session.Submit('Player',$command)}
        $report.commands+=@{command=$command;response=$response}
        Require ($response.Response-eq'Committed') "Seal closure command rejected: $($command.Kind) / $($response.Response) / $($response.Code)"
    }
    $hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion';$enemy='TEST_ONLY.ferry-wraith';$tear=$null;$deathSaved=$false;$attackAttempts=0
    $report.strategy=@{tearAfterActualObservedPartyAttackAttempts=$TearAfterAttempts;maximumEnemyHpBeforeTear=4;heroAggressiveAfterTear=[bool]$AggressiveAfterTear}
    $start=Capture;Require ($start.Revision-eq351-and!$start.FerryWraith.SealDestroyed) 'Expected genuine first-fire intact-seal checkpoint351.'
    Checkpoint 'first-fire'
    for($step=0;$step-lt140;$step++){
        $s=Capture;$body=$s.Lives|Where-Object ActorId -eq $enemy
        $report.observations+=@{revision=$s.Revision;clock=$s.RuleClock;enemyHp=$body.Hp;enemyDead=$body.Dead;suppressed=$s.FerryWraith.ClawSuppressed;currentActor=$s.Encounter.CurrentActor}
        if($null-ne$tear){Require ($s.FerryWraith.SealDestroyed-and$s.FerryWraith.Rupture.ExpiresAt.Equals($tear.ExpiresAt)) 'Original physical seal history changed.'}
        if($body.Dead-and!$deathSaved){
            Require ($null-ne$tear-and$s.FerryWraith.ClawSuppressed-and$s.RuleClock.CompareTo($tear.ExpiresAt)-lt0) 'Death was not within actual suppression.'
            $report.death=@{revision=$s.Revision;clock=$s.RuleClock;life=$body;rupture=$s.FerryWraith.Rupture}
            Checkpoint 'dead-still-suppressed';$deathSaved=$true
        }
        $view=$session.View('Player')
        if($view.NextSeat-eq'FerryOpponent'){
            $decision=$session.ObserveFerryDecision('FerryOpponent');$response=$session.AdvanceAutomaticDefender()
            $report.commands+=@{mode='actual-public-controller';beforeRevision=$s.Revision;decision=$decision;response=$response}
            Require ($response.Response-eq'Committed') 'Actual Ferry controller failed.';continue
        }
        Require ($view.NextSeat-eq'Player') 'Unexpected seal-closure actor authority.'
        $actor=$s.Encounter.CurrentActor
        if($body.Dead-and$actor-eq$hero){
            $end=[Decennium.Foundation.WorldTiming]::ForEncounter($s).Start($s.Encounter.TurnOrdinal+1)
            Send ([Decennium.Foundation.Command]::new("ferry.seal-close.close.$($s.Revision)",$hero,$s.Revision,'EndFixedEncounter',$s.Encounter.CurrentTurnId)) $true
            $closed=Capture
            Require (!$closed.InventoryCombat-and$closed.FerryWraith.ClawSuppressed-and$closed.RuleClock.Equals($end)-and$closed.RuleClock.CompareTo($tear.ExpiresAt)-lt0) 'Paid closure did not retain active original suppression.'
            $report.closure=@{revision=$closed.Revision;clock=$closed.RuleClock;closed=@($closed.ClosedEncounters|Where-Object {$_.Encounter.Id-eq'TEST_ONLY.ferry-encounter'})}
            Checkpoint 'closed-still-suppressed';break
        }
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded){
            $stance=if($AggressiveAfterTear-and$null-ne$tear-and$actor-eq$hero){[Decennium.Foundation.CombatStance]::Aggressive}else{[Decennium.Foundation.CombatStance]::Guarded}
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int]$stance)
            Send ([Decennium.Foundation.Command]::new("ferry.seal-close.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        $spent=($s.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent
        if(!$spent-and$actor-eq$comp){
            if($null-eq$tear-and$body.Hp-le4-and$attackAttempts-ge$TearAfterAttempts){
                $command=[Decennium.Foundation.Command]::new("ferry.seal-close.tear.$($s.Revision)",$comp,$s.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
                Require ($session.QueryCastingCommand('Player',$command).Admissible) 'Late physical seal tear unavailable.'
                Send $command;$after=Capture;$tear=$after.FerryWraith.Rupture;$report.rupture=$tear
                Require (($after.WorldIntervals|Where-Object ActorId -eq $comp).ActionSpent-and$after.RandomState-eq$s.RandomState-and$after.RuleClock.Equals($s.RuleClock)) 'Late tear did not pay its existing Action exactly.'
                Checkpoint 'late-paid-tear';continue
            }
            $health=$s.Lives|Where-Object ActorId -eq $hero
            if($health.Hp-le[math]::Floor($health.MaximumHp/2)){
                $heal=[Decennium.Foundation.Command]::new("ferry.seal-close.rite.$($s.Revision)",$comp,$s.Revision,'UseHealingRite',$hero)
                if($session.QueryCastingCommand('Player',$heal).Admissible){Send $heal;continue}
            }
        }
        if(!$spent-and$actor-eq$hero-and!$body.Dead){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'TEST_ONLY.actor-club',0,'OrdinaryOutcome',$false,'KeepExisting')
            $attack=[Decennium.Foundation.Command]::new("ferry.seal-close.attack.$($s.Revision)",$hero,$s.Revision,'AttackClub',$enemy,0,0,$null,$combat)
            Require ($session.QueryCastingCommand('Player',$attack).Admissible) 'Actual party attack unavailable.'
            Send $attack;$attackAttempts++;continue
        }
        Send ([Decennium.Foundation.Command]::new("ferry.seal-close.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    $s=Capture;Require (!$s.InventoryCombat-and$deathSaved-and$s.FerryWraith.ClawSuppressed) 'Did not reach actual suppressed closure.'
    # Actual public source cannot be readmitted by ordinary paid clock advancement.
    $beforeContacts=$s.FerryWraith.Contacts.Count;$beforeAdmission=$s.FerryWraith.Admission.Epoch.Id
    foreach($offset in -1,0,1){
        $target=[Decennium.Foundation.RuleTime]::new($tear.ExpiresAt.Numerator+$offset*$tear.ExpiresAt.Denominator,$tear.ExpiresAt.Denominator);$s=Capture
        $n=$target.Numerator*$s.RuleClock.Denominator-$s.RuleClock.Numerator*$target.Denominator;$d=$target.Denominator*$s.RuleClock.Denominator
        if($n-gt0){Send ([Decennium.Foundation.Command]::new("ferry.seal-close.clock.$offset",$hero,$s.Revision,'AdvanceClock','',[int]$n,[int]$d)) $true}
        $s=Capture;Require ($s.RuleClock.Equals($target)-and$s.FerryWraith.SealDestroyed-and$s.FerryWraith.Rupture.ExpiresAt.Equals($tear.ExpiresAt)) 'Post-close original deadline changed.'
        Require ($s.FerryWraith.ClawSuppressed-eq($offset-lt0)) 'Post-close suppression boundary wrong.'
        Require (!$s.InventoryCombat-and$s.FerryWraith.Contacts.Count-eq$beforeContacts-and$s.FerryWraith.Admission.Epoch.Id-eq$beforeAdmission) 'Single-use source readmitted after closure.'
        Checkpoint "closed-deadline-$offset"
    }
    $s=Capture;$unchanged=Bytes
    $second=[Decennium.Foundation.Command]::new('ferry.seal-close.second',$comp,$s.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
    $query=$session.QueryCastingCommand('Player',$second);$response=$session.Submit('Player',$second)
    Require (!$query.Admissible-and$response.Response-ne'Committed'-and$unchanged-ceq(Bytes)) 'Destroyed paper was reusable.'
    $report.probes+=@{name='destroyed-paper-no-second-tear';command=$second;query=$query;response=$response}
    $report.finalRevision=$s.Revision;$report.finalClock=$s.RuleClock;$report.finalFerry=$s.FerryWraith
    $report.expandedCommands=@($s.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object{@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.commands.Count-eq$report.expandedCommands.Count) 'Actual command and receipt counts differ.'
    $report.status='PASS_GENUINE_ACTIVE_SUPPRESSION_DEATH_CLOSURE_ORIGINAL_EXPIRY'
}catch{$report.error=$_.Exception.ToString();try{$report.failedRevision=(Capture).Revision;$session.Save((Join-Path $Run 'failed-last-state.ddsave'))}catch{}}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
