param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][ValidateSet('Purify','Spare','Invocation')][string]$Plan,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh ability branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';plan=$Plan;scope='Genuine alternate first-fire continuation of one owned care ability; no resource/state injection or whole-module acceptance';assemblies=@();commands=@();checks=@();rechargeObservations=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryCareAbilities.executed.ps1')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function MakeCommand($values){
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object {if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($args)
    }
    function CloneCommand($command,$id){
        $values=@{}
        foreach($parameter in [Decennium.Foundation.Command].GetConstructors()[0].GetParameters()){
            $values[$parameter.Name]=if($parameter.Name-eq'id'){$id}elseif($parameter.Name-eq'revision'){$command.ExpectedRevision}else{$command.($parameter.Name)}
        }
        MakeCommand $values
    }
    function Send($command){
        $result=$session.Submit('Player',$command);$report.commands+=@{command=$command;response=$result}
        Require ($result.Response-eq'Committed') "Care branch rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"
    }
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$restored=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($restored)
        Require ((Digest $path)-ceq(Digest $restored)) "Strict replay changed $name."
    }
    function Invocation($s,$suffix){
        MakeCommand @{id="ferry.care.invocation.$suffix.$($s.Revision)";actor=$companion;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($hero,$companion))}
    }
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry=[Decennium.Foundation.FerryWraithProfile]::Actor
    $start=Capture;$uses=0;$firstInvocation=$null;$done=$false
    Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected the genuine first-fire checkpoint.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Current strict restore changed input bytes.'
    # A creature source does not acquire character casting or class ability ownership.
    $badCast=MakeCommand @{id="ferry.care.$Plan.nonowner";actor=$ferry;revision=$start.Revision;kind=[Decennium.Foundation.CommandKind]::CastKnownSpell;target=$hero;spellCast=[Decennium.Foundation.SpellCastRequest]::new('spare-the-dying')}
    $stable=Bytes;$report.nonownerQuery=$session.QueryCastingCommand('FerryOpponent',$badCast);$report.nonownerResponse=$session.Submit('FerryOpponent',$badCast)
    Require (!$report.nonownerQuery.Admissible-and$report.nonownerResponse.Response-ne'Committed'-and$stable-ceq(Bytes)) 'Creature nonowner request threw, mutated, cast or acquired class state.'
    for($step=0;$step-lt180;$step++){
        $s=Capture;$h=$s.Lives|Where-Object ActorId -eq $hero;$c=$s.Lives|Where-Object ActorId -eq $companion
        Require (!$h.Dead-and!$c.Dead-and$c.Hp-gt0) 'Actual party life could not complete this branch.'
        if($Plan-eq'Invocation'-and$uses-eq1){
            $interval=$s.WorldIntervals|Where-Object ActorId -eq $companion
            $recharge=$s.AbilityRecharges|Where-Object {$_.ActorId-eq$companion-and$_.AbilityId-eq[Decennium.Foundation.BishopProfile]::Invocation}
            $elapsed=($interval.LastStart-$firstInvocation.Turn.LocalStart)/$s.FerryWraith.Admission.Epoch.Order.Count
            $expected=[Math]::Max(0,3-[int]$elapsed)
            Require ($null-ne$recharge-and$recharge.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar-and$recharge.LastLocalStart-eq$interval.LastStart-and$recharge.Remaining-eq$expected) 'Recharge did not follow actual owning Ferry Starts.'
            $report.rechargeObservations+=@{revision=$s.Revision;clock=$s.RuleClock;currentActor=$s.Encounter.CurrentActor;ownerStart=$interval.LastStart;recharge=$recharge}
        }
        if($session.View('Player').NextSeat-eq'FerryOpponent'){
            $result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result}
            Require ($result.Response-eq'Committed') 'Actual creature continuation failed.'
            continue
        }
        $actor=$s.Encounter.CurrentActor;$life=$s.Lives|Where-Object ActorId -eq $actor
        Require ($actor-in@($hero,$companion)) 'Unexpected care-branch actor.'
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if($life.Hp-gt0-and!$guarded){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.care.$Plan.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        if($actor-eq$companion-and!($s.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent){
            if($Plan-eq'Invocation'){
                $command=Invocation $s ($uses+1)
                $before=Bytes;$query=$session.QueryCastingCommand('Player',$command)
                Require ($before-ceq(Bytes)) 'Invocation query changed state.'
                if($uses-eq0-or$recharge.Remaining-eq0){
                    Require ($query.Admissible) "Funded invocation unavailable: $($query|ConvertTo-Json -Compress)"
                    $rp=($s.ResonancePools|Where-Object ActorId -eq $companion).Current;$conviction=$s.ConvictionBalance.Current
                    Send $command;$after=Capture;$use=$after.BishopEntry.Invocations|Where-Object CommandId -eq $command.Id
                    Require ($null-ne$use-and$use.Turn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar-and!$use.Turn.IsCarried) 'Invocation lost actual owning turn.'
                    Require (($after.ResonancePools|Where-Object ActorId -eq $companion).Current-eq($rp-3)-and$after.ConvictionBalance.Current-eq($conviction-2)-and($after.WorldIntervals|Where-Object ActorId -eq $companion).ActionSpent) 'Invocation did not pay actual RP/Conviction/Action.'
                    Require (($after.AbilityRecharges|Where-Object {$_.ActorId-eq$companion-and$_.AbilityId-eq[Decennium.Foundation.BishopProfile]::Invocation}).Remaining-eq3) 'Invocation did not establish its own recharge.'
                    $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Invocation duplicate repeated payment/healing/RNG.'
                    $uses++;if($uses-eq1){$firstInvocation=$use;Checkpoint 'first-invocation'}else{$done=$true;break}
                    continue
                }
                Require (!$query.Admissible-and$query.Code-eq'DivineInvocationRecharging') 'Existing owner cooldown was not enforced before its next eligible Start.'
                $stable=Bytes;Require ($session.Submit('Player',$command).Response-ne'Committed'-and$stable-ceq(Bytes)) 'Recharging invocation mutated state or spent resources.'
                $report.checks+="Actual owner Start$($interval.LastStart) rejects reuse with Remaining$($recharge.Remaining)"
            } elseif($Plan-eq'Purify'-or$h.Hp-eq0-and!$h.Stable){
                $spell=if($Plan-eq'Purify'){'purify-food-and-drink'}else{'spare-the-dying'}
                $target=if($Plan-eq'Purify'){'TEST_ONLY.cleric-casting.contaminated-water'}else{$hero}
                $stable=Bytes;$choices=@($session.DiscoverCastingCommands('Player',$companion)|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq$spell-and$_.Command.Target-eq$target})
                $legal=@($choices|Where-Object {$_.Query.Admissible})
                Require ($legal.Count-eq1-and$stable-ceq(Bytes)) "Expected one lawful actual $spell option: $($choices|ConvertTo-Json -Depth 8 -Compress)"
                $command=CloneCommand $legal[0].Command "ferry.care.$spell.$($s.Revision)"
                Require ($session.QueryCastingCommand('Player',$command).Admissible-and$stable-ceq(Bytes)) 'Selected source payload was not a pure admissible query.'
                $report.beforeLife=$h;$report.beforeContamination=$s.ConsumableContamination
                $beforeLots=$s.Work.Lots|ConvertTo-Json -Depth 15 -Compress;$beforeMetadata=$s.InventoryLots|ConvertTo-Json -Depth 15 -Compress
                Send $command;$after=Capture;$cast=$after.SpellCasts|Where-Object CommandId -eq $command.Id
                Require ($null-ne$cast-and$cast.Turn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar-and($after.WorldIntervals|Where-Object ActorId -eq $companion).ActionSpent) 'Care spell did not use its actual Ferry Action.'
                $report.cast=$cast
                if($Plan-eq'Purify'){
                    $prior=@($s.ConsumableContamination|Where-Object {$_.LotId-eq$target-and$_.Present-and$_.Purifiable})
                    Require ($prior.Count-gt0) 'Selected genuine batch had no actual purifiable contamination.'
                    foreach($item in $prior){$ended=$after.ConsumableContamination|Where-Object Id -eq $item.Id;Require (!$ended.Present-and$ended.DestroyedByCastId-eq$command.Id-and$ended.DestroyedRevision-eq$after.Revision) 'Actual contamination did not end under this source cast.'}
                    Require ($beforeLots-ceq($after.Work.Lots|ConvertTo-Json -Depth 15 -Compress)-and$beforeMetadata-ceq($after.InventoryLots|ConvertTo-Json -Depth 15 -Compress)) 'Purify rewrote quantities, ownership or freshness metadata.'
                    Require ($after.RandomState-eq$s.RandomState-and$cast.RpBefore-eq7-and$cast.RpAfter-eq5) 'Purify changed RNG or did not pay actual ranked cost.'
                } else {
                    $healed=$after.Lives|Where-Object ActorId -eq $hero
                    Require ($h.Hp-eq0-and!$h.Stable-and!$h.Dead-and$healed.Hp-eq0-and$healed.Stable-and!$healed.Dead-and$null-ne$healed.StableUntil-and$cast.StableRecoveryD4-ge1-and$cast.StableRecoveryD4-le4) 'Spare did not stabilize actual Dying life with its own recovery roll.'
                    Require ($cast.RpBefore-eq7-and$cast.RpAfter-eq7-and$cast.WordsConsumed-gt0) 'Spare changed the free cantrip cost or omitted actual recovery RNG.'
                }
                $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Care cast retry repeated effect/payment/RNG.'
                $done=$true;break
            }
        }
        Send ([Decennium.Foundation.Command]::new("ferry.care.$Plan.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    Require ($done) 'The genuine branch did not reach its selected ability endpoint.'
    Checkpoint 'completed'
    $final=Capture;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalRp=$final.ResonancePools;$report.finalConviction=$final.ConvictionBalance
    $report.finalLives=@($final.Lives|Where-Object {$_.ActorId-in@($hero,$companion)});$report.finalContamination=$final.ConsumableContamination
    $report.invocations=@($final.BishopEntry.Invocations|Where-Object {$_.Revision-gt$start.Revision});$report.finalRecharges=$final.AbilityRecharges
    $report.incomingAttacks=@($final.MeleeAttacks|Where-Object {$_.Revision-gt$start.Revision});$report.lifeEvents=@($final.LifeEvents|Where-Object {$_.Revision-gt$start.Revision})
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Actual care command history does not reconcile.'
    $report.status="PASS_GENUINE_FERRY_$($Plan.ToUpperInvariant())_ONLY"
} catch {
    $report.error=$_.Exception.ToString()
    if($null-ne$session-and$null-ne$field){$failed=Capture;$report.failedState=@{revision=$failed.Revision;clock=$failed.RuleClock;lives=$failed.Lives;rp=$failed.ResonancePools;recharges=$failed.AbilityRecharges}}
}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
