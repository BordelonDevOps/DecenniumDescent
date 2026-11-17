param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$RecoveredClawSave,[Parameter(Mandatory)][string]$Run,[string]$ResumeClosedRun='')
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$RecoveredClawSave=(Resolve-Path -LiteralPath $RecoveredClawSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh continuation directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Actual recovered Claw -> party combat/owned healing -> Dead -> outgoing-slot closure -> paid retrieval/preparation/continued movement; no source rewards invented';checks=@();commands=@();assemblies=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryContinuation.executed.ps1')
    $report.source=@{path=$RecoveredClawSave;sha256=(Digest $RecoveredClawSave)}
    Copy-Item -LiteralPath $RecoveredClawSave -Destination (Join-Path $Run 'original-recovered-claw.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $resumeReport=$null
    if($ResumeClosedRun-ne''){
        $ResumeClosedRun=(Resolve-Path -LiteralPath $ResumeClosedRun).Path
        $priorResult=Join-Path $ResumeClosedRun 'RESULT.json'
        $resumeReport=Get-Content -LiteralPath $priorResult -Raw|ConvertFrom-Json
        Require ($resumeReport.status-eq'FAIL'-and$resumeReport.error.Contains('No genuine incoming party attack hit.')-and$resumeReport.compilationReport.sha256-ceq$report.compilationReport.sha256-and$resumeReport.source.sha256-ceq$report.source.sha256) 'Resume must reference the exact retained diagnostic failure and runtime/input.'
        foreach($name in 'actual-dead-before-closure','actual-ferry-closed'){
            Require ((Digest (Join-Path $ResumeClosedRun "$name.ddsave"))-ceq(Digest (Join-Path $ResumeClosedRun "$name-restored.ddsave"))) 'Prior executed checkpoint/restore bytes differ.'
        }
        $closedSource=Join-Path $ResumeClosedRun 'actual-ferry-closed.ddsave'
        $session.Restore($closedSource)
        Copy-Item -LiteralPath $closedSource -Destination (Join-Path $Run 'resumed-closed.ddsave')
        $report.commands=@($resumeReport.commands)
        $report.resumedFrom=@{scope='Reuse actual prior executed commands/checkpoints after correcting the diagnostic TargetId field; not a rerun of that prefix';resultPath=$priorResult;resultSha256=(Digest $priorResult);closedSha256=(Digest $closedSource);priorScriptSha256=$resumeReport.script.sha256;priorExecutedCommands=$resumeReport.commands.Count}
    } else {$session.Restore($RecoveredClawSave)}
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    function Capture { $field.GetValue($session).Capture() }
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Bytes { [Convert]::ToBase64String($codec.Encode((Capture))) }
    function Send($command,$sessionCommand=$false){
        $result=if($sessionCommand){$session.SubmitSessionCommand($command)}else{$session.Submit('Player',$command)}
        $report.commands+=@{mode=$(if($sessionCommand){'session-command'}else{'party-command'});command=$command;response=$result}
        Require ($result.Response-eq'Committed') "Continuation rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"
    }
    function Roundtrip($name){
        $session.Save((Join-Path $Run "$name.ddsave"));$session.Restore((Join-Path $Run "$name.ddsave"))
        $session.Save((Join-Path $Run "$name-restored.ddsave"))
        Require ((Digest (Join-Path $Run "$name.ddsave"))-ceq(Digest (Join-Path $Run "$name-restored.ddsave"))) "Verified restore changed $name."
    }
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry='TEST_ONLY.ferry-wraith'
    $start=if($null-ne$resumeReport){$codec.Decode([IO.File]::ReadAllBytes($RecoveredClawSave))}else{Capture}
    Require ($start.InventoryCombat-and$start.FerryWraith.SealDestroyed-and!$start.FerryWraith.ClawSuppressed) 'Continuation did not start after genuine seal expiry.'
    $report.initialParty=@($start.Lives|Where-Object ActorId -in $hero,$companion|Select-Object ActorId,Hp,MaximumHp,Dead)
    $report.initialResonance=$start.ResonancePools
    $initialAttackIds=@($start.MeleeAttacks|ForEach-Object Id);$initialRiteIds=@($start.HealingRites|ForEach-Object CommandId)
    $deathSaved=$false;$closure=$null
    if($null-ne$resumeReport){
        $closed=Capture;$closure=@($closed.ClosedEncounters|Where-Object {$_.Encounter.Id-eq'TEST_ONLY.ferry-encounter'-and$_.ClosedRevision-eq$closed.Revision})
        Require (!$closed.InventoryCombat-and$null-eq$closed.Encounter-and($closed.Lives|Where-Object ActorId -eq $ferry).Dead-and$closure.Count-eq1) 'Resumed state is not the actual closed Ferry checkpoint.'
        $prefix=@($closed.Receipts|Where-Object {$_.Revision-le$start.Revision})
        Require (($prefix|ConvertTo-Json -Depth 40 -Compress)-ceq($start.Receipts|ConvertTo-Json -Depth 40 -Compress)) 'Closed checkpoint does not retain the exact original command prefix.'
        $deathSaved=$true
    }
    for($step=0;$step-lt100;$step++){
        $state=Capture;$view=$session.View('Player')
        if(!$state.InventoryCombat){break}
        $body=$state.Lives|Where-Object ActorId -eq $ferry
        if($body.Dead-and!$deathSaved){Roundtrip 'actual-dead-before-closure';$deathSaved=$true}
        if($view.NextSeat-eq'FerryOpponent'){
            $decision=$session.ObserveFerryDecision('FerryOpponent');$result=$session.AdvanceAutomaticDefender()
            $report.commands+=@{mode='actual-public-auto';revision=$state.Revision;decision=$decision;response=$result}
            Require ($result.Response-eq'Committed') 'Ferry controller continuation failed.'
            continue
        }
        Require ($view.NextSeat-eq'Player') "Unexpected encounter continuation seat: $($view.NextSeat)"
        $actor=$state.Encounter.CurrentActor
        Require (@($state.Lives|Where-Object {$_.ActorId-eq$actor-and!$_.Dead}).Count-eq1) 'Party actor died before successful closure.'
        $guarded=@($state.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$state.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($state,$_.Revision)}).Count-gt0
        if(!$guarded){
            $combat=[Decennium.Foundation.CombatRequest]::new($state.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.continue.guard.$($state.Revision)",$actor,$state.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        if($body.Dead-and$actor-eq$hero){
            $epoch=[Decennium.Foundation.WorldTiming]::ForEncounter($state);$expectedEnd=$epoch.Start($epoch.ProcessedSlot+1)
            $command=[Decennium.Foundation.Command]::new("ferry.continue.close.$($state.Revision)",$hero,$state.Revision,'EndFixedEncounter',$state.Encounter.CurrentTurnId)
            Send $command $true
            $closed=Capture
            Require (!$closed.InventoryCombat-and$null-eq$closed.Encounter-and$closed.RuleClock.Equals($expectedEnd)) 'Closure omitted the actual outgoing End or retained combat.'
            $closure=@($closed.ClosedEncounters|Where-Object {$_.Reason-eq$command.Id-and$_.Encounter.Id-eq'TEST_ONLY.ferry-encounter'-and$_.ClosedRevision-eq$closed.Revision})
            Require ($closure.Count-eq1) 'Actual closure history is missing.'
            Roundtrip 'actual-ferry-closed';break
        }
        $spent=($state.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent
        if(!$spent-and$actor-eq$companion){
            $health=$state.Lives|Where-Object ActorId -eq $hero
            if($health.Hp-le[math]::Floor($health.MaximumHp/2)){
                $heal=[Decennium.Foundation.Command]::new("ferry.continue.rite.$($state.Revision)",$actor,$state.Revision,'UseHealingRite',$hero)
                $query=$session.QueryCastingCommand('Player',$heal)
                if($query.Admissible){Send $heal;continue}
            }
        }
        if(!$spent-and$actor-eq$hero-and!$body.Dead){
            Require ([Decennium.Foundation.Laboratory.ObservationRules]::CanSee($state,$actor,$ferry)) 'Party strategy cannot inspect an unseen target.'
            $combat=[Decennium.Foundation.CombatRequest]::new($state.Encounter.CurrentTurnId,'TEST_ONLY.actor-club',0,'OrdinaryOutcome',$false,'KeepExisting')
            $attack=[Decennium.Foundation.Command]::new("ferry.continue.attack.$($state.Revision)",$actor,$state.Revision,'AttackClub',$ferry,0,0,$null,$combat)
            $query=$session.QueryCastingCommand('Player',$attack)
            Require ($query.Admissible) "Observed source party attack unavailable: $($query.Code)"
            Send $attack;continue
        }
        Send ([Decennium.Foundation.Command]::new("ferry.continue.end.$($state.Revision)",$actor,$state.Revision,'EndRegularTurn',$state.Encounter.CurrentTurnId))
    }
    $closed=Capture
    Require (!$closed.InventoryCombat-and$deathSaved-and$null-ne$closure) 'Bounded genuine combat did not reach actual Dead and closure.'
    $incoming=@($closed.MeleeAttacks|Where-Object {$_.Id-notin$initialAttackIds-and$_.TargetId-eq$ferry})
    Require ($incoming.Count-gt0-and@($incoming|Where-Object {$_.Attack.Hit}).Count-gt0) 'No genuine incoming party attack hit.'
    Require (($closed.Lives|Where-Object ActorId -eq $ferry).Dead-and!($closed.Lives|Where-Object ActorId -eq $ferry).UsesDeathSaves) 'Ferry did not reach source-faithful actual death.'
    $report.incomingAttacks=$incoming;$report.healingRites=@($closed.HealingRites|Where-Object CommandId -notin $initialRiteIds);$report.closure=$closure
    $report.checks+='Actual party attacks and owned Healing Rite used retained state/RNG/resources; actual Dead alone permitted outgoing-slot closure; Dead and closed saves restored identically'
    # Return along the known southern lane to the companion's previously dropped club.
    # This retrieves an existing owned item; it creates no creature loot or source reward.
    $club=$closed.Clubs|Where-Object Id -eq 'TEST_ONLY.companion-club'
    Require ($club.HeldBy-eq''-and$club.CellX-eq3-and$club.CellY-eq3) 'Existing dropped club context changed.'
    function Walk($dx,$dy){
        $state=Capture;$actor=$state.Actors|Where-Object Id -eq $companion;$x=$actor.X+$dx;$y=$actor.Y+$dy
        $move=[Decennium.Foundation.Command]::new("ferry.continue.walk.$($state.Revision)",$companion,$state.Revision,'BeginWorldStep','walk',$dx,$dy)
        Send $move
        for($tick=0;$tick-lt14;$tick++){
            $state=Capture;$actor=$state.Actors|Where-Object Id -eq $companion
            if($actor.X-eq$x-and$actor.Y-eq$y-and@($state.WorldTraversals|Where-Object ActorId -eq $companion).Count-eq0){return}
            Send ([Decennium.Foundation.Command]::new("ferry.continue.clock.$($state.Revision)",$hero,$state.Revision,'AdvanceClock','',1,1)) $true
        }
        throw 'Paid ordinary edge did not complete through existing budget refresh.'
    }
    Walk 0 1
    for($edge=0;$edge-lt5;$edge++){Walk -1 0}
    Walk 0 -1
    $beforePickup=Capture
    $inventory=[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'','Pickup')
    $pickup=[Decennium.Foundation.Command]::new("ferry.continue.prepare.$($beforePickup.Revision)",$companion,$beforePickup.Revision,'HandlePortableEquipment','TEST_ONLY.companion-club',0,0,$inventory)
    Send $pickup
    $prepared=Capture
    Require (($prepared.Clubs|Where-Object Id -eq 'TEST_ONLY.companion-club').HeldBy-eq$companion-and$prepared.RuleClock.CompareTo($beforePickup.RuleClock)-gt0) 'Preparation did not pay time and retrieve the actual owned club.'
    $report.preparation=@{command=$pickup;before=$beforePickup.RuleClock;after=$prepared.RuleClock;club=($prepared.Clubs|Where-Object Id -eq 'TEST_ONLY.companion-club')}
    Walk 0 1
    $final=Capture
    Require (!$final.InventoryCombat-and$final.FerryWraith.SealDestroyed-and!$final.FerryWraith.ClawSuppressed-and($final.Lives|Where-Object ActorId -eq $ferry).Dead) 'Ordinary continuation reset the closed encounter or seal history.'
    Require (@($final.Lives|Where-Object {$_.ActorId-in$hero,$companion-and$_.Dead}).Count-eq0) 'A party member died during continued management.'
    Roundtrip 'continued-after-preparation'
    $report.checks+='Paid ordinary movement retrieved the previously dropped owned companion club, paid preparation time, and continued moving with unchanged source death/destruction history; final strict restore is identical'
    # Real save-store recovery, using only this probe's disposable primary and its real backup.
    $recovery=Join-Path $Run 'backup-recovery.ddsave';$session.Save($recovery);$session.Save($recovery)
    $valid=Digest $recovery;$backup=Digest ($recovery+'.bak');Require ($valid-ceq$backup) 'Real backup was not created.'
    [IO.File]::WriteAllBytes($recovery,[byte[]]@(0x42,0x41,0x44));$bad=Digest $recovery
    $displaced=$session.RecoverBackup($recovery)
    Require ((Digest $recovery)-ceq$valid-and(Digest ($recovery+'.bak'))-ceq$backup-and(Digest $displaced)-ceq$bad) 'Real recovery failed to restore/preserve primary/backup evidence.'
    Require ([Convert]::ToBase64String($codec.Encode($final))-ceq(Bytes)) 'Backup recovery changed the verified final state.'
    $report.backupRecovery=@{validSha256=$valid;backupSha256=$backup;corruptSha256=$bad;displacedPath=$displaced}
    $report.checks+='Actual corrupt-primary/valid-backup recovery validated command history, restored the exact final state and preserved displaced corrupt bytes'
    $report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalResonance=$final.ResonancePools
    $report.finalParty=@($final.Lives|Where-Object ActorId -in $hero,$companion|Select-Object ActorId,Hp,MaximumHp,Dead)
    $report.status='PASS_GENUINE_DEAD_CLOSURE_MANAGE_PREPARE_CONTINUE_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
