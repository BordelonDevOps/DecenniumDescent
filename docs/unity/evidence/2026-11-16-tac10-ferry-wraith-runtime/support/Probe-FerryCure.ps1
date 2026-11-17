param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$EarnedSave,[Parameter(Mandatory)][string]$ReceiptSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$EarnedSave=(Resolve-Path -LiteralPath $EarnedSave).Path;$ReceiptSave=(Resolve-Path -LiteralPath $ReceiptSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh genuine cure branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Genuine paid optional Invocation cure using the existing recovery-defender fear producer in the Ferry profile, before Ferry admission; this does not claim a new-epoch positive cure intersection';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();restorePairs=@();probes=@();fearAttempts=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryCure.executed.ps1')
    Copy-Item -LiteralPath $EarnedSave -Destination (Join-Path $Run 'original-earned.ddsave');Copy-Item -LiteralPath $ReceiptSave -Destination (Join-Path $Run 'original-receipts.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$EarnedSave;sha256=(Digest $EarnedSave)};$report.receiptSource=@{path=$ReceiptSave;sha256=(Digest $ReceiptSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($EarnedSave);$field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$after=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($after)
        Require ((Digest $path)-ceq(Digest $after)) "Strict restore changed $name."
        $report.restorePairs+=@{name=$name;sha256=(Digest $path)}
    }
    function Command($values){
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($args)
    }
    $hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion';$enemy='TEST_ONLY.recovery-defender'
    function Seat($actor){if($actor-eq$enemy){'RecoveryOpponent'}else{'Player'}}
    function Send($command){
        $response=if($command.Kind-eq'AdvanceClock'){$session.SubmitSessionCommand($command)}else{$session.Submit((Seat $command.Actor),$command)}
        $report.commands+=@{command=$command;response=$response}
        Require ($response.Response-eq'Committed') "Actual cure branch rejected $($command.Kind): $($response|ConvertTo-Json -Compress)"
    }
    function Guarded($s,$actor){@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0}
    function HasFear($s,$actor){[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$actor).View().Has('Frightened')}
    $start=Capture;Require ($start.Revision-eq213) 'Expected actual earned-Bishop checkpoint213.'
    $receipts=([Decennium.Foundation.FileSaveStore]::new().Load($ReceiptSave)).Receipts
    $ready=$false
    foreach($receipt in $receipts|Where-Object {$_.Revision-gt213-and$_.Revision-lt309}){
        $s=Capture
        if($s.InventoryCombat-and$s.Encounter.CurrentActor-eq$enemy-and(Guarded $s $enemy)-and!($s.WorldIntervals|Where-Object ActorId -eq $enemy).ActionSpent){$ready=$true;break}
        Send ([Decennium.Foundation.CommandHistory]::Read($receipt))
    }
    Require $ready 'The genuine prefix did not reach the owned recovery-defender action.'
    $report.prefixEndRevision=(Capture).Revision
    Checkpoint 'before-source-fear'
    $done=$false
    for($step=0;$step-lt90;$step++){
        $s=Capture;$actor=$s.Encounter.CurrentActor;$seat=Seat $actor
        Require ($s.InventoryCombat-and$actor-in@($hero,$comp,$enemy)-and$null-eq$s.FerryWraith.Admission) 'Unexpected cure context.'
        if(!(Guarded $s $actor)){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.cure.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        $spent=($s.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent
        if($actor-eq$enemy-and!$spent){
            $fear=Command @{id="ferry.cure.fear.$($s.Revision)";actor=$enemy;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseIntimidatingPresence;target='';intimidatingPresence=[Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]@($hero,$comp))}
            $unchanged=Bytes;$query=$session.QueryCastingCommand('RecoveryOpponent',$fear)
            Require ($unchanged-ceq(Bytes)) 'Fear query mutated.'
            if($query.Admissible){Send $fear;$after=Capture;$report.fearAttempts+=@{use=($after.FrightenedUses|Select-Object -Last 1);saves=@($after.FrightenedSaves|Where-Object Revision -eq $after.Revision);timings=@($after.FrightenedTimings|Select-Object -Last 2)};continue}
        }
        if($actor-eq$comp-and!$spent){
            $target=if(HasFear $s $hero){$hero}elseif(HasFear $s $comp){$comp}else{''}
            if($target){
                Checkpoint 'genuine-fear-before-cure'
                $choice=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($hero,$comp),$target,'Frightened')
                $cure=Command @{id="ferry.cure.invocation.$($s.Revision)";actor=$comp;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=$choice}
                $unchanged=Bytes;$query=$session.QueryCastingCommand('Player',$cure)
                Require ($query.Admissible-and$unchanged-ceq(Bytes)) "Actual paid cure unavailable: $($query|ConvertTo-Json -Compress)"
                $wrongSeat=$session.Submit('RecoveryOpponent',$cure)
                Require ($wrongSeat.Response-eq'NotAuthorized'-and$unchanged-ceq(Bytes)) 'Wrong seat stole the cure.'
                $bad=Command @{id='ferry.cure.bad-recipient';actor=$comp;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@('TEST_ONLY.ferry-wraith'),'TEST_ONLY.ferry-wraith','Frightened')}
                $badQuery=$session.QueryCastingCommand('Player',$bad);$badResponse=$session.Submit('Player',$bad)
                Require (!$badQuery.Admissible-and$badResponse.Response-ne'Committed'-and$unchanged-ceq(Bytes)) 'Unsupported cure recipient changed state or received a grant.'
                $report.probes+=@{name='wrong-seat-current-cure';command=$cure;response=$wrongSeat},@{name='invalid-current-cure-recipient';command=$bad;query=$badQuery;response=$badResponse}
                Send $cure;$after=Capture;$use=$after.BishopEntry.Invocations|Select-Object -Last 1
                Require ($use.CommandId-eq$cure.Id-and$use.EndedApplicationIds.Count-gt0-and$use.CureOperationId-ne''-and!(HasFear $after $target)) 'Paid optional cure did not end actual fear.'
                Require ($use.RpAfter-eq($use.RpBefore-3)-and$use.ConvictionAfter-eq($use.ConvictionBefore-2)-and$use.Turn.EpochId-eq'TEST_ONLY.post-recovery-calendar') 'Cure changed ownership/payment/context.'
                $genuine=@($s.FrightenedSaves|Where-Object {$_.ApplicationId-in$use.EndedApplicationIds-and!$_.Success-and!$_.Prevented})
                Require ($genuine.Count-eq$use.EndedApplicationIds.Count) 'Cure did not bind actual failed source saves.'
                $report.cure=$use;$report.curedSourceSaves=$genuine;$report.cureTarget=$target
                $unchanged=Bytes;$report.retry=$session.Submit('Player',$cure)
                Require ($report.retry.Response-eq'Duplicate'-and$unchanged-ceq(Bytes)) 'Cure retry repeated payment/effects/RNG.'
                Checkpoint 'actual-paid-cure';$done=$true;break
            }
        }
        Send ([Decennium.Foundation.Command]::new("ferry.cure.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    Require $done 'No genuine positive cure in the bounded source branch.'
    $final=Capture;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object{@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.commands.Count-eq$report.expandedCommands.Count) 'Cure command/receipt counts differ.'
    $report.status='PASS_GENUINE_RECOVERY_SOURCE_INVOCATION_CURE_IN_FERRY_PROFILE'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
