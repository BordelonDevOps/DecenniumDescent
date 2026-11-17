param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$EarnedSave,[Parameter(Mandatory)][string]$ReceiptSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$EarnedSave=(Resolve-Path -LiteralPath $EarnedSave).Path;$ReceiptSave=(Resolve-Path -LiteralPath $ReceiptSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh genuine staged-cure branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Genuine staged existing-source fear, ordinary life/death, paid closure and final edge; investigate actual retained cure window without inventing a producer or claiming global unreachability';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();restorePairs=@();observations=@();fearAttempts=@();probes=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryCureReachability.executed.ps1')
    Copy-Item -LiteralPath $EarnedSave -Destination (Join-Path $Run 'original-earned.ddsave');Copy-Item -LiteralPath $ReceiptSave -Destination (Join-Path $Run 'original-receipts.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$EarnedSave;sha256=(Digest $EarnedSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($EarnedSave);$field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){$path=Join-Path $Run "$name.ddsave";$after=Join-Path $Run "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($after);Require ((Digest $path)-ceq(Digest $after)) "Strict restore changed $name.";$report.restorePairs+=@{name=$name;sha256=(Digest $path)}}
    $hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion';$enemy='TEST_ONLY.recovery-defender'
    function Seat($actor){if($actor-eq$enemy){'RecoveryOpponent'}else{'Player'}}
    function Send($command,$hostCommand=$false){$response=if($hostCommand-or$command.Kind-eq'AdvanceClock'-or$command.Kind-eq'EndFixedEncounter'){$session.SubmitSessionCommand($command)}else{$session.Submit((Seat $command.Actor),$command)};$report.commands+=@{command=$command;response=$response};Require ($response.Response-eq'Committed') "Staged branch rejected: $($command.Kind) / $($response|ConvertTo-Json -Compress)"}
    function Command($values){$ctor=[Decennium.Foundation.Command].GetConstructors()[0];$args=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}});$ctor.Invoke($args)}
    function HasFear($s,$actor){[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$actor).View().Has('Frightened')}
    function Pending{
        $s=Capture;$move=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($s)
        if($null-ne$move){$reactor=$move.Reactors[$move.ResponseIndex];$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$false);Send ([Decennium.Foundation.Command]::new("ferry.stage.oa-decline.$($s.Revision)",$reactor,$s.Revision,'RespondOpportunityAttack',$move.Id,0,0,$null,$combat));return $true}
        $offer=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::CurrentPressOffer($s)
        if($null-ne$offer){$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$false);Send ([Decennium.Foundation.Command]::new("ferry.stage.press-decline.$($s.Revision)",$offer.ActorId,$s.Revision,'RespondPress',$offer.Id,0,0,$null,$combat));return $true}
        return $false
    }
    $start=Capture;Require ($start.Revision-eq213) 'Expected genuine earned checkpoint213.'
    $receipts=([Decennium.Foundation.FileSaveStore]::new().Load($ReceiptSave)).Receipts
    foreach($receipt in $receipts|Where-Object {$_.Revision-gt213-and$_.Revision-le290}){Send ([Decennium.Foundation.CommandHistory]::Read($receipt))}
    Checkpoint 'actual-before-staging';$report.beforeStagingLife=(Capture).Lives|Where-Object ActorId -eq $enemy
    $routes=@{};$routes[$hero]=@(@(6,3),@(7,3),@(8,2),@(8,1));$routes[$comp]=@(@(4,4),@(5,4),@(6,4),@(7,4),@(8,3));$routes[$enemy]=@(@(6,3),@(7,2))
    $indices=@{};$indices[$hero]=0;$indices[$comp]=0;$indices[$enemy]=0;$fear=$null;$stagedSaved=$false;$deadSaved=$false;$closed=$false
    for($step=0;$step-lt145;$step++){
        if(Pending){continue}
        $s=Capture;Require ($s.InventoryCombat-and$s.Encounter.Id-eq'TEST_ONLY.post-recovery-conflict') 'Unexpected staged encounter.'
        $actor=$s.Encounter.CurrentActor;$body=$s.Lives|Where-Object ActorId -eq $enemy
        $report.observations+=@{revision=$s.Revision;clock=$s.RuleClock;actor=$actor;sourceLife=$body;companionFrightened=(HasFear $s $comp)}
        if($body.Dead-and!$deadSaved){Checkpoint 'actual-source-dead';$deadSaved=$true;$report.sourceDead=@{revision=$s.Revision;clock=$s.RuleClock;life=$body}}
        $aware=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy].GetMethod('Aware',[Reflection.BindingFlags]'Static,NonPublic').Invoke($null,[object[]]@($s,$actor))
        $stance=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if($aware-and!$stance){$kind=if($actor-eq$hero){'Aggressive'}elseif($actor-eq$comp){'Focused'}else{'Guarded'};$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]$kind);Send ([Decennium.Foundation.Command]::new("ferry.stage.stance.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue}
        if($body.Dead-and$actor-eq$hero){Send ([Decennium.Foundation.Command]::new("ferry.stage.close.$($s.Revision)",$hero,$s.Revision,'EndFixedEncounter',$s.Encounter.CurrentTurnId)) $true;Checkpoint 'actual-staged-closure';$report.closure=@{revision=(Capture).Revision;clock=(Capture).RuleClock};$closed=$true;break}
        if($indices[$actor]-lt$routes[$actor].Count){
            $cell=$routes[$actor][$indices[$actor]];$move=[Decennium.Foundation.Command]::new("ferry.stage.move.$($s.Revision)",$actor,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,$cell[0],$cell[1]);$query=$session.QueryCastingCommand((Seat $actor),$move)
            if($query.Admissible){Send $move;$indices[$actor]++;continue}
            Require ($query.Code-in@('InsufficientMovement','MovementBudgetExceeded','InsufficientMovementRemaining','MovementAllowanceExceeded')) "Staging cell not admitted: $($query|ConvertTo-Json -Compress)"
        }
        $allStaged=@($indices.Keys|Where-Object {$indices[$_]-lt$routes[$_].Count}).Count-eq0
        if($allStaged-and!$stagedSaved){Checkpoint 'genuine-staged-participants';$stagedSaved=$true;$report.stagedActors=$s.Actors|Where-Object Id -in $hero,$comp,$enemy}
        $spent=($s.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent
        if($allStaged-and$null-eq$fear-and$actor-eq$enemy-and!$spent){
            $command=Command @{id="ferry.stage.fear.$($s.Revision)";actor=$enemy;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseIntimidatingPresence;target='';intimidatingPresence=[Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]@($comp))}
            if($session.QueryCastingCommand('RecoveryOpponent',$command).Admissible){Send $command;$after=Capture;$save=$after.FrightenedSaves|Where-Object Revision -eq $after.Revision;$report.fearAttempts+=@{command=$command;saves=$save};if(HasFear $after $comp){$fear=$after.FrightenedTimings|Select-Object -Last 1;$report.originalFear=$fear;Checkpoint 'actual-staged-fear'};continue}
        }
        if($null-ne$fear-and$actor-in@($hero,$comp)-and!$spent-and!$body.Dead){
            $kind=if($actor-eq$hero){'AttackClub'}else{'AttackUnarmed'};$weapon=if($actor-eq$hero){'TEST_ONLY.actor-club'}else{''}
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,$weapon,0,'OrdinaryOutcome',$false,'KeepExisting')
            $command=[Decennium.Foundation.Command]::new("ferry.stage.attack.$($s.Revision)",$actor,$s.Revision,$kind,$enemy,0,0,$null,$combat);$attackQuery=$session.QueryCastingCommand((Seat $actor),$command)
            if(!$attackQuery.Admissible){
                Require ($actor-eq$comp-and$attackQuery.Code-eq'UnsupportedOperation') "Staged real attack unavailable: $($attackQuery|ConvertTo-Json -Compress)"
                $before=Bytes;$denied=$session.Submit('Player',$command);Require ($denied.Response-ne'Committed'-and$before-ceq(Bytes)) 'Unsupported unarmed request changed state.'
                $report.probes+=@{name='existing-public-companion-unarmed-boundary';command=$command;query=$attackQuery;response=$denied}
                Send ([Decennium.Foundation.Command]::new("ferry.stage.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId));continue
            }
            Send $command
            if($actor-eq$hero){$after=Capture;$probe=[Decennium.Foundation.Command]::new("ferry.stage.probe-close.$($after.Revision)",$hero,$after.Revision,'EndFixedEncounter',$after.Encounter.CurrentTurnId);if(!($after.Lives|Where-Object ActorId -eq $enemy).Dead){$before=Bytes;$response=$session.SubmitSessionCommand($probe);Require ($response.Response-ne'Committed'-and$before-ceq(Bytes)) 'Dying source incorrectly allowed closure.';$report.probes+=@{name='actual-nonDead-closure';revision=$after.Revision;clock=$after.RuleClock;sourceLife=($after.Lives|Where-Object ActorId -eq $enemy);response=$response}}}
            continue
        }
        Send ([Decennium.Foundation.Command]::new("ferry.stage.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    Require ($closed-and$null-ne$fear) 'Staged source branch did not reach genuine fear and actual Dead closure.'
    $s=Capture;Send ([Decennium.Foundation.Command]::new("ferry.stage.final-edge.$($s.Revision)",$hero,$s.Revision,'BeginWorldStep','walk',0,1))
    for($i=0;$i-lt12;$i++){$s=Capture;if($null-ne$s.FerryWraith.Admission){break};Send ([Decennium.Foundation.Command]::new("ferry.stage.clock.$($s.Revision)",$hero,$s.Revision,'AdvanceClock','',1,2)) $true}
    $s=Capture;Require ($null-ne$s.FerryWraith.Admission) 'Staged final paid edge did not admit Ferry.'
    $report.admission=@{revision=$s.Revision;clock=$s.RuleClock;admission=$s.FerryWraith.Admission;fearTiming=$fear;fearPresent=(HasFear $s $comp)};Checkpoint 'staged-ferry-admission'
    for($i=0;$i-lt20;$i++){
        $s=Capture;$actor=$s.Encounter.CurrentActor
        if($actor-eq$comp){$stance=@($s.Stances|Where-Object {$_.ActorId-eq$comp-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0;if(!$stance){$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded);Send ([Decennium.Foundation.Command]::new("ferry.stage.new-stance.$($s.Revision)",$comp,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue};break}
        if($actor-eq'TEST_ONLY.ferry-wraith'){$response=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-ferry-controller';response=$response};Require ($response.Response-eq'Committed') 'New Ferry controller failed.';continue}
        $stance=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$stance){$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded);Send ([Decennium.Foundation.Command]::new("ferry.stage.new-stance.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue}
        Send ([Decennium.Foundation.Command]::new("ferry.stage.new-end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    $s=Capture;Require ($s.Encounter.CurrentActor-eq$comp) 'No actual new companion owner turn.'
    $cure=Command @{id="ferry.stage.new-cure.$($s.Revision)";actor=$comp;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($hero,$comp),$comp,'Frightened')}
    $report.newEpochContext=@{revision=$s.Revision;clock=$s.RuleClock;fearPresent=(HasFear $s $comp);originalTiming=$fear;query=$session.QueryCastingCommand('Player',$cure);life=($s.Lives|Where-Object ActorId -eq $enemy)}
    if(HasFear $s $comp){Send $cure;$report.newEpochCure=(Capture).BishopEntry.Invocations|Select-Object -Last 1;Require ($report.newEpochCure.EndedApplicationIds -contains $fear.ApplicationId) 'New-epoch cure did not end retained actual source application.';$report.status='PASS_GENUINE_POSITIVE_NEW_EPOCH_CURE'}else{$report.status='OBSERVED_STAGED_FEAR_WINDOW_EXPIRED_BEFORE_NEW_OWNER_START_NOT_GLOBAL_IMPOSSIBILITY'}
    Checkpoint 'staged-new-owner-context';$final=Capture;$report.finalRevision=$final.Revision;$report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object{@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.commands.Count-eq$report.expandedCommands.Count) 'Staged commands/receipts differ.'
}catch{$report.error=$_.Exception.ToString();try{$report.failedRevision=(Capture).Revision;$session.Save((Join-Path $Run 'failed-last-state.ddsave'))}catch{}}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run";if($report.status-eq'FAIL'){throw $report.error}
