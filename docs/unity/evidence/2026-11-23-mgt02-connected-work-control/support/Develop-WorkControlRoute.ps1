param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run,
    [ValidateSet('Prefix','Dose','Fight','Work')][string]$Stage='Prefix',[string]$ResumeSave)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path -LiteralPath $Run){throw 'Use a new evidence directory.'}
$null=New-Item -ItemType Directory -Path $Run
Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$repo=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$oldSupport=Join-Path $repo 'docs/unity/evidence/2026-11-23-tac01-ordinary-magic/support'
Copy-Item -LiteralPath (Join-Path $oldSupport 'TypedCommand.ps1') -Destination $Run
. (Join-Path $Run 'TypedCommand.ps1')
$report=[ordered]@{status='RUNNING';scope='Genuine new-profile principal route development; not final acceptance';stage=$Stage;startedUtc=[DateTime]::UtcNow.ToString('o');commands=0;queries=0;checkpoints=@();assemblyRoot=$AssemblyRoot;driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash.ToLowerInvariant()}
function Json($v){ConvertTo-Json -InputObject $v -Depth 12 -Compress -EnumsAsStrings}
function Require([bool]$condition,[string]$message){if(!$condition){throw $message}}
try {
    foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $store=[Decennium.Foundation.FileSaveStore]::new();$codec=[Decennium.Foundation.SnapshotCodec]::new()
    $hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero;$ally=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
    if($ResumeSave){$ResumeSave=(Resolve-Path -LiteralPath $ResumeSave).Path;$session.Restore($ResumeSave);$report.parentSave=$ResumeSave;$report.parentSha256=(Get-FileHash -LiteralPath $ResumeSave).Hash.ToLowerInvariant()}
    elseif($Stage-ne'Prefix'){throw 'A continuation stage needs a genuine same-profile save.'}
    function State {$session.Save((Join-Path $Run 'latest.ddsave'));$store.Load((Join-Path $Run 'latest.ddsave'))}
    function Witness([string]$name) {
        $path=Join-Path $Run ($name+'.ddsave');$session.Save($path);$s=$store.Load($path)
        foreach($actor in @($hero,$ally)) {
            [IO.File]::WriteAllText((Join-Path $Run ($name+'.'+$actor+'.work.json')),(Json ($session.ObserveWork('Player',$actor))))
            [IO.File]::WriteAllText((Join-Path $Run ($name+'.'+$actor+'.discover.json')),(Json @($session.DiscoverCommands('Player',$actor))))
        }
        $report.checkpoints+=,@{name=$name;revision=$s.Revision;clock=$s.RuleClock;random=$s.RandomState;sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
    }
    function Dispatch($request) {
        $command=New-TypedCommand $request
        if($request.op-eq'submit') {
            $query=$session.QueryCommand($request.seat,$command);$report.queries++
            [IO.File]::AppendAllText((Join-Path $Run 'queries.jsonl'),(Json @{request=$request;query=$query})+"`n")
            if($query.Supported){Require $query.Admissible "Denied query $($command.Kind): $($query.Code)"}
        }
        $result=switch($request.op){
            'clock'{$session.SubmitSessionCommand($command)}
            'close'{$session.SubmitSessionCommand($command)}
            'auto'{$session.AdvanceAutomaticDefender()}
            'defender-presence'{$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
            'defender-sanctuary'{$session.SubmitDefenderSanctuary([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
            default{$session.Submit($request.seat,$command)}
        }
        [IO.File]::AppendAllText((Join-Path $Run 'execution.jsonl'),(Json @{request=$request;result=$result})+"`n")
        Require ($result.Response.ToString()-eq'Committed') "Command failed $($request.id)/$($request.kind): $($result.Response)"
        $report.commands++;$session.Save((Join-Path $Run 'latest.ddsave'))
        if($report.commands%25-eq0){Write-Output ("$Stage committed $($report.commands); revision$($result.Revision)")}
    }
    function Send([string]$kind,[string]$actor=$hero,[string]$target='',[int]$x=0,[int]$y=0,$inventory=$null,$combat=$null) {
        $r=$session.View('Player').Revision
        $request=@{op=$(if($kind-eq'AdvanceClock'){'clock'}elseif($kind-eq'EndFixedEncounter'){'close'}else{'submit'});seat='Player';id="work-control.route.$r";actor=$actor;revision=$r;kind=$kind;target=$target;x=$x;y=$y}
        if($inventory){$request.inventory=$inventory};if($combat){$request.combat=$combat};Dispatch $request
    }
    function Walk([string]$actor,[int]$dx,[int]$seconds=6) {Send 'BeginWorldStep' $actor 'walk' $dx;Send 'AdvanceClock' $hero '' $seconds 1}
    function Guard([string]$actor) {Send 'SelectCombatStance' $actor -combat @{turn=$session.View('Player').TurnId;stance=1}}
    function End([string]$actor) {Send 'EndRegularTurn' $actor $session.View('Player').TurnId}
    function AdvanceTo($end) {
        $s=State;$n=$end.Numerator*$s.RuleClock.Denominator-$s.RuleClock.Numerator*$end.Denominator;$d=$end.Denominator*$s.RuleClock.Denominator
        Require ($n-gt0) 'Advancement target must be after the actual clock.'
        Send 'AdvanceClock' $hero '' ([int]$n) ([int]$d)
    }
    function Automatic {
        for($i=0;$session.View('Player').NextSeat.ToString()-eq'AutomaticDefender';$i++) {
            Require ($i-lt16) 'Automatic defender exceeded one bounded decision sequence.'
            $r=$session.View('Player').Revision
            Dispatch @{op='auto';seat='Player';id="work-control.auto.$r";actor='TEST_ONLY.later-defender';revision=$r;kind='EndRegularTurn';target='';x=0;y=0}
        }
    }
    Witness 'initial'
    if($Stage-eq'Prefix') {
        $source=Join-Path $repo 'engine/artifacts/ordinary-magic-qualification/candidate-02/five-paths-01/inputs.jsonl'
        $report.prefixInputSha256=(Get-FileHash -LiteralPath $source).Hash.ToLowerInvariant()
        $already=$session.View('Player').Revision
        $commands=@(Get-Content -LiteralPath $source|ForEach-Object{ConvertFrom-Json -AsHashtable $_}|Where-Object{$_.op-in@('submit','clock','close','auto','defender-presence','defender-sanctuary')}|Select-Object -First 108|Select-Object -Skip $already)
        Require ($commands.Count+$already-eq108) 'Missing finite prefix.'
        foreach($request in $commands) {
            Dispatch $request
            $r=$session.View('Player').Revision
            if($r-in@(15,16,17,93,94,95,96,97,104,105,106,107,108)){Witness ('r'+$r.ToString('D3'))}
        }
        $s=State
        Require ($s.ManufacturingOrders.Count-eq1-and$s.AlchemyDoses.Count-gt0) 'Prefix did not produce actual doses.'
    } elseif($Stage-eq'Dose'-and$session.View('Player').Revision-eq129) {
        # Continue the retained actual consumption at full HP; it spent dose0 but proved no
        # useful healing. Bring the already-injured Hero within the worksite user's reach.
        End $ally;Guard $hero;Send 'TacticalStep' $hero $session.View('Player').TurnId 1 2;Automatic
        End $hero;Automatic;Guard $ally
        $before=State;$life=@($before.Lives|Where-Object ActorId -eq $hero)[0];Witness 'before-use'
        $dose='manufacture.order.104.dose1'
        Send 'UseAlchemyDose' $ally $dose -inventory @{numerator=1;denominator=1;destination=$hero;handling='Pickup'}
        $after=State;$healed=@($after.Lives|Where-Object ActorId -eq $hero)[0]
        Require ($healed.Hp-gt$life.Hp-and@($after.AlchemyDoses|Where-Object Id -eq $dose)[0].Spent) 'Second actual dose did not usefully heal the injured Hero.'
        $report.usefulDose=@{id=$dose;beforeHp=$life.Hp;afterHp=$healed.Hp;beforeRng=$before.RandomState;afterRng=$after.RandomState}
    } elseif($Stage-eq'Dose') {
        Require ($session.View('Player').Revision-in@(108,110)) 'Dose stage begins at the genuine completed-batch prefix or retained failed pickup approach.'
        $dose='manufacture.order.104.dose0'
        # The selected Cleric profile leaves batch doses at the actual worksite; it does not
        # select the separate carried-vial profile. Preserve that boundary and use in reach.
        if($session.View('Player').Revision-eq110){Walk $hero -1}
        Walk $ally -1;Walk $hero -1 12
        Send 'BeginReinforcementApproach' $ally 'TEST_ONLY.companion-reinforcement.v1'
        Witness 'actual-encounter-entry'
        Guard $hero;Send 'TacticalStep' $hero $session.View('Player').TurnId 0 2;Automatic
        End $hero;Automatic;Guard $ally
        Send 'TacticalStep' $ally $session.View('Player').TurnId 2 3;Automatic
        $before=State;$life=@($before.Lives|Where-Object ActorId -eq $ally)[0]
        Witness 'before-use'
        Send 'UseAlchemyDose' $ally $dose -inventory @{numerator=1;denominator=1;destination=$ally;handling='Pickup'}
        $after=State;$healed=@($after.Lives|Where-Object ActorId -eq $ally)[0]
        Require ($healed.Hp-gt$life.Hp-and@($after.AlchemyDoses|Where-Object Id -eq $dose)[0].Spent) 'Actual batch output did not heal a damaged actor and become spent.'
        $report.usefulDose=@{id=$dose;beforeHp=$life.Hp;afterHp=$healed.Hp;beforeRng=$before.RandomState;afterRng=$after.RandomState}
    } elseif($Stage-eq'Fight') {
        $s=State;Require ($s.InventoryCombat-and@($s.AlchemyDoses|Where-Object{$_.ActualHealing-gt0}).Count-gt0) 'Combat continuation requires actual useful batch consumption.'
        End $ally
        for($turn=0;$turn-lt40;$turn++) {
            Automatic;$s=State
            Require ($s.Revision-lt440) 'Principal route command headroom exhausted.'
            $current=$s.Encounter.CurrentActor;$enemy=@($s.Lives|Where-Object ActorId -eq 'TEST_ONLY.later-defender')[0]
            Require (@($s.Lives|Where-Object{$_.ActorId-in@($hero,$ally)-and$_.Dead}).Count-eq0) 'Party death prevents the intended principal continuation.'
            if($current-eq$hero) {
                Guard $hero
                if($enemy.Dead){Send 'EndFixedEncounter' $hero $session.View('Player').TurnId;break}
                Send 'AttackClub' $hero 'TEST_ONLY.later-defender' -combat @{turn=$session.View('Player').TurnId;weapon='TEST_ONLY.actor-club'}
                $s=State;$enemy=@($s.Lives|Where-Object ActorId -eq 'TEST_ONLY.later-defender')[0]
                if($enemy.Dead){Send 'EndFixedEncounter' $hero $session.View('Player').TurnId;break}
                End $hero
            } elseif($current-eq$ally) {
                Guard $ally
                $own=@($s.Lives|Where-Object ActorId -eq $ally)[0];$lead=@($s.Lives|Where-Object ActorId -eq $hero)[0]
                $patient=if($own.Hp-le4){$ally}elseif($lead.Hp-lt18){$hero}else{''}
                if($patient) {
                    $r=$session.View('Player').Revision;$q=[Decennium.Foundation.Command]::new("work-control.route.$r",$ally,$r,'UseHealingRite',$patient)
                    if($session.QueryCommand('Player',$q).Admissible){Send 'UseHealingRite' $ally $patient}
                }
                End $ally
            } else {throw "Unexpected combat actor $current"}
        }
        $s=State;Require (!$s.InventoryCombat-and@($s.Lives|Where-Object ActorId -eq 'TEST_ONLY.later-defender')[0].Dead) 'Bounded combat did not reach actual Dead and paid closure.'
    } elseif($Stage-eq'Work') {
        $s=State;Require (!$s.InventoryCombat) 'Work continuation requires actual paid combat closure.'
        if($s.OrdinaryMagic.Current.Deadline-gt$s.RuleClock){AdvanceTo $s.OrdinaryMagic.Current.Deadline}else{Send 'AdvanceClock' $hero '' 6 1}
        $ready=State;$source=[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::SupplyId;$vessel=[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::CompanionSkinId
        $initialQuantity=@($ready.Work.Lots|Where-Object Id -eq $source)[0].Amount
        Send 'StartWaterFill' $ally $source -inventory @{numerator=1;denominator=2;destination=$vessel;handling='Pickup'}
        $s=State;$job=@($s.WaterFills|Where-Object Pending)[0].Id;Witness 'active-fill'
        Send 'BeginWorldStep' $hero 'walk' 1 0;Send 'AdvanceClock' $hero '' 3 2
        $busy=State;Require (@($busy.WaterFills|Where-Object Id -eq $job)[0].Progress-eq[Decennium.Foundation.RuleTime]::new(3,2)) 'Other actor movement did not credit exact compatible worker time.'
        $denied=[Decennium.Foundation.Command]::new('work-control.busy-magic',$ally,$busy.Revision,'CastKnownSpell',$ally,0,0,
            $null,$null,$null,$null,'None',$null,$null,$null,$null,$null,$null,$null,$null,$null,
            [Decennium.Foundation.SpellCastRequest]::new('guidance','',$true,$false))
        $beforeHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($busy)))
        $query=$session.QueryCommand('Player',$denied);$rejection=$session.Submit('Player',$denied);$after=State
        Require (!$query.Admissible-and$rejection.Response.ToString()-eq'Unavailable'-and$beforeHash-eq[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($after)))) 'Active-worker magic did not reject without mutation.'
        [IO.File]::WriteAllText((Join-Path $Run 'active-magic-denial.json'),(Json @{query=$query;response=$rejection;unchanged=$true}))
        Send 'PauseWaterFill' $ally $job;Witness 'paused-fill'
        $paused=State;AdvanceTo ($paused.OrdinaryMagic.Current.Deadline.AddSeconds(3))
        $r=$session.View('Player').Revision
        Dispatch @{op='submit';seat='Player';id="work-control.route.$r";actor=$ally;revision=$r;kind='CastKnownSpell';target=$ally;x=0;y=0;spellCast=@{spellId='guidance';focusItemId='';willingTarget=$true;electFocusedDc=$false}}
        $magic=State;Require (@($magic.WaterFills|Where-Object Id -eq $job)[0].Progress-eq[Decennium.Foundation.RuleTime]::new(3,2)) 'Paused-worker magic credited labor.'
        Witness 'paused-magic'
        AdvanceTo $magic.OrdinaryMagic.Current.Deadline
        Send 'ResumeWaterFill' $ally $job;Witness 'resumed-fill'
        Send 'AdvanceClock' $hero '' 117 2
        $complete=State;$fill=@($complete.WaterFills|Where-Object Id -eq $job)[0]
        Require ($fill.Status.ToString()-eq'Complete'-and$fill.Progress-eq[Decennium.Foundation.RuleTime]::new(60)) 'Fill did not finish after exact60 productive seconds.'
        Require (@($complete.Work.Lots|Where-Object Id -eq $fill.OutputLotId)[0].Amount-eq[Decennium.Foundation.RuleQuantity]::new(1,2)) 'Fill output quantity differs.'
        Require (@($complete.Work.Lots|Where-Object Id -eq $source)[0].Amount-eq($initialQuantity-[Decennium.Foundation.RuleQuantity]::new(1,2))) 'Finite source water was not conserved.'
        Require ($complete.RandomState-eq$ready.RandomState) 'Ordinary fill/movement/Guidance altered RNG unexpectedly.'
        Witness 'completed-fill';Walk $hero 1
        $report.workWitness=@{job=$job;productiveSeconds='60';amountPints='1/2';pausedProgress='3/2';otherActorMovement=$true;activeMagicRejected=$true;pausedGuidanceCommitted=$true;finiteSourceConserved=$true;rngUnchanged=$true;ordinaryContinuation=$true}
    } else {throw 'Continuation stage is not yet authored.'}
    Witness 'final';$s=State
    $report.finalRevision=$s.Revision;$report.finalClock=$s.RuleClock;$report.randomState=$s.RandomState
    $report.actors=@($s.Actors|Select-Object Id,X,Y);$report.lives=@($s.Lives|Select-Object ActorId,Hp,Dead)
    $report.doses=@($s.AlchemyDoses|Select-Object Id,OwnerId,LocationId,UsedAt,Spent,ActualHealing)
    $report.workCounts=@{lots=$s.Work.Lots.Count;bookings=$s.Work.WorkerIntervals.Count;reservations=$s.Work.Reservations.Count;receipts=$s.Receipts.Count}
    $report.status='PASS_BOUNDED_STAGE'
} catch {$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally {$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8;Write-Output ("$($report.status): $Run")}
if($report.status-ne'PASS_BOUNDED_STAGE'){exit 1}
