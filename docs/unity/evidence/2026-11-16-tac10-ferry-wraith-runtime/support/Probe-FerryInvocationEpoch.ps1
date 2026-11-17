param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$BeforeAdmissionSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$BeforeAdmissionSave=(Resolve-Path -LiteralPath $BeforeAdmissionSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh epoch branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Genuine funded Invocation immediately before the already-paid Ferry approach completes; actual epoch transfer and owner Starts, no state injection';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();observations=@();probes=@();restorePairs=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){
        $dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll
        $report.assemblies+=@{name=$part;sha256=(Digest $dll)}
    }
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryInvocationEpoch.executed.ps1')
    Copy-Item -LiteralPath $BeforeAdmissionSave -Destination (Join-Path $Run 'original-before-admission.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    $report.input=@{path=$BeforeAdmissionSave;sha256=(Digest $BeforeAdmissionSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($BeforeAdmissionSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$restored=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($restored)
        Require ((Digest $path)-ceq(Digest $restored)) "Restore changed $name."
        $report.restorePairs+=@{name=$name;sha256=(Digest $path)}
    }
    function MakeCommand($values){
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($args)
    }
    function Send($command,[switch]$HostCommand){
        $result=if($HostCommand){$session.SubmitSessionCommand($command)}else{$session.Submit('Player',$command)}
        $report.commands+=@{command=$command;response=$result;sessionAuthority=[bool]$HostCommand}
        Require ($result.Response-eq'Committed') "Actual command rejected: $($command.Kind) $($result|ConvertTo-Json -Compress)"
    }
    $hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion';$ability=[Decennium.Foundation.BishopProfile]::Invocation
    $start=Capture
    Require ($start.Revision-eq345-and!$start.InventoryCombat-and$null-eq$start.FerryWraith.Admission) 'Expected genuine pre-admission checkpoint345.'
    Require (@($start.WorldTraversals|Where-Object ActorId -eq $hero).Count-eq1) 'The actual final paid approach is absent.'
    Checkpoint 'before-invocation'
    $command=MakeCommand @{id='ferry.epoch.invocation';actor=$comp;revision=$start.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($comp))}
    $before=Bytes;$query=$session.QueryCastingCommand('Player',$command)
    Require ($query.Admissible-and$before-ceq(Bytes)) "Funded old-epoch Invocation unavailable: $($query|ConvertTo-Json -Compress)"
    $session.SetSeatEnabled('Player',$false)
    $revoked=$session.Submit('Player',$command)
    $session.SetSeatEnabled('Player',$true)
    Require ($revoked.Response-eq'NotAuthorized'-and$before-ceq(Bytes)) 'Revoked owner changed state.'
    $report.probes+=@{name='revoked-actual-invocation-owner';response=$revoked}
    Send $command
    $paid=Capture;$recharge=$paid.AbilityRecharges|Where-Object {$_.ActorId-eq$comp-and$_.AbilityId-eq$ability}
    Require ($recharge.Remaining-eq3-and$recharge.EpochId-eq'TEST_ONLY.post-recovery-calendar') 'Paid Invocation did not create actual old-epoch recharge3.'
    Require (($paid.ResonancePools|Where-Object ActorId -eq $comp).Current-eq4-and$paid.ConvictionBalance.Current-eq3) 'Invocation payment was not exactly3RP/2Conviction.'
    $report.paidInvocation=$paid.BishopEntry.Invocations|Select-Object -Last 1
    $report.paidRecharge=$recharge
    Checkpoint 'paid-old-epoch'
    # Same finite world duration as the genuine main trace:30/20 seconds, no teleport or clock assignment.
    Send ([Decennium.Foundation.Command]::new('ferry.epoch.complete-paid-approach',$hero,$paid.Revision,'AdvanceClock','',30,20)) -HostCommand
    $entered=Capture
    Require ($entered.InventoryCombat-and$entered.Encounter.Id-eq'TEST_ONLY.ferry-encounter'-and$null-ne$entered.FerryWraith.Admission) 'Actual paid approach did not admit the source encounter.'
    $report.admission=$entered.FerryWraith.Admission
    $epoch=$entered.FerryWraith.Admission.Epoch
    $ownerIndex=[Array]::IndexOf([string[]]@($epoch.Order),$comp)
    $observedStarts=0;$last=-1L;$done=$false
    for($step=0;$step-lt70;$step++){
        $s=Capture;$interval=$s.WorldIntervals|Where-Object ActorId -eq $comp
        $current=$s.AbilityRecharges|Where-Object {$_.ActorId-eq$comp-and$_.AbilityId-eq$ability}
        Require ($null-ne$current-and$current.EpochId-eq'TEST_ONLY.ferry-calendar') 'Invocation recharge did not transfer to the exact new epoch.'
        if($interval.LastStart-ge0-and$interval.LastStart-ne$last){$observedStarts++;$last=$interval.LastStart}
        $expected=[Math]::Max(0,3-$observedStarts)
        Require ($current.Remaining-eq$expected) 'Admission/End/nonowner Start reset or double-ticked recharge.'
        Require (($s.ResonancePools|Where-Object ActorId -eq $comp).Current-eq4-and$s.ConvictionBalance.Current-eq3) 'Admission or turn progress changed paid pools.'
        $report.observations+=@{revision=$s.Revision;clock=$s.RuleClock;currentActor=$s.Encounter.CurrentActor;ownerStart=$interval.LastStart;actualOwnerStarts=$observedStarts;expectedRemaining=$expected;recharge=$current}
        if($step-eq0){Checkpoint 'after-admission'}
        if($s.Encounter.CurrentActor-eq$comp-and$interval.LastStart-ge0-and@($report.restorePairs|Where-Object name -eq "owner-start-$($interval.LastStart)").Count-eq0){Checkpoint "owner-start-$($interval.LastStart)"}
        if($expected-eq0){$done=$true;break}
        if($session.View('Player').NextSeat-eq'FerryOpponent'){
            $result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result}
            Require ($result.Response-eq'Committed') 'Creature public continuation failed.'
            continue
        }
        $actor=$s.Encounter.CurrentActor
        Require ($actor-in@($hero,$comp)-and!($s.Lives|Where-Object ActorId -eq $actor).Dead) 'No lawful party continuation.'
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded-and($s.Lives|Where-Object ActorId -eq $actor).Hp-gt0){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.epoch.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat))
        }else{Send ([Decennium.Foundation.Command]::new("ferry.epoch.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))}
    }
    Require ($done-and$observedStarts-eq3) 'Did not reach exactly three actual new owner Starts.'
    Checkpoint 'recharge-complete'
    $final=Capture
    $report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalLives=$final.Lives
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object{@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Actual command/receipt count differs.'
    $report.status='PASS_GENUINE_INVOCATION_EPOCH_TRANSFER'
}catch{$report.error=$_.Exception.ToString();if($null-ne$field-and$null-ne$session){$s=Capture;$report.failedRevision=$s.Revision;$report.failedClock=$s.RuleClock;$report.failedRecharge=$s.AbilityRecharges}}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
