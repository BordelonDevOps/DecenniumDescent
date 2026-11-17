param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$BeforeContactSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$BeforeContactSave=(Resolve-Path -LiteralPath $BeforeContactSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh ordinary-world seal probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Two genuine alternate continuations from the actual paid pre-contact checkpoint; scheduled ordinary-world seal Action, original world deadline across entry and strict restore. Not the canonical combat witness or full module acceptance.';assemblies=@();branches=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryWorldSeal.executed.ps1')
    $report.input=@{path=$BeforeContactSave;sha256=(Digest $BeforeContactSave)}
    Copy-Item -LiteralPath $BeforeContactSave -Destination (Join-Path $Run 'original-before-contact.ddsave')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion'
    function Capture { $field.GetValue($session).Capture() }
    function Bytes { [Convert]::ToBase64String($codec.Encode((Capture))) }
    function Send($command,$sessionCommand=$false){
        $before=Capture
        $result=if($sessionCommand){$session.SubmitSessionCommand($command)}else{$session.Submit('Player',$command)}
        $record.commands+=@{command=$command;response=$result;beforeClock=$before.RuleClock}
        Require ($result.Response-eq'Committed') "World seal command failed: $($command.Kind) / $($result|ConvertTo-Json -Compress)"
    }
    function AdvanceTo($target){
        $s=Capture;$n=$target.Numerator*$s.RuleClock.Denominator-$s.RuleClock.Numerator*$target.Denominator
        $d=$target.Denominator*$s.RuleClock.Denominator
        Require ($n-ge0) 'Cannot move clock backwards.'
        if($n-gt0){Send ([Decennium.Foundation.Command]::new("ferry.world.$mode.clock.$($s.Revision)",$hero,$s.Revision,'AdvanceClock','',[int]$n,[int]$d)) $true}
    }
    function Checkpoint($name){
        $path=Join-Path $branch "$name.ddsave";$restored=Join-Path $branch "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($restored)
        Require ((Digest $path)-ceq(Digest $restored)) "Strict restore changed $mode/$name."
        $record.checkpoints+=@{name=$name;sha256=(Digest $path);revision=(Capture).Revision}
    }
    foreach($mode in 'own-slot','other-slot'){
        $branch=(New-Item -ItemType Directory -Path (Join-Path $Run $mode)).FullName
        $record=[ordered]@{mode=$mode;commands=@();checkpoints=@();checks=@()};$report.branches+=,$record
        $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
            [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
            [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
            [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
        $session.Restore($BeforeContactSave)
        $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
        $start=Capture
        Require ($start.Revision-eq344-and$null-eq$start.Encounter-and!$start.InventoryCombat-and$null-eq$start.FerryWraith.Admission-and!$start.FerryWraith.SealDestroyed) 'Expected the genuine ordinary pre-contact checkpoint.'
        Checkpoint 'verified-input'
        Require ((Digest (Join-Path $branch 'verified-input.ddsave'))-ceq$report.input.sha256) 'Current runtime changed the source checkpoint.'
        # Wait legally to the next hero virtual Start while the actual hero remains at8,1,
        # outside the contact anchor. The companion retains its own earlier Action ledger.
        $epoch=$start.PostRecoveryEncounter.Admission.Epoch
        if($mode-eq'other-slot'){
            $slot=$epoch.SlotAt($start.RuleClock)+1
            while($epoch.Order[[int]($slot%$epoch.Order.Count)]-ne$hero){$slot++}
            AdvanceTo ($epoch.Start($slot))
        }
        $s=Capture;$epoch=$s.PostRecoveryEncounter.Admission.Epoch;$slot=$epoch.SlotAt($s.RuleClock)
        $current=$epoch.Order[[int]($slot%$epoch.Order.Count)]
        Require ($null-eq$s.Encounter-and!$s.InventoryCombat) 'Ordinary wait unexpectedly entered initiative.'
        Require (($mode-eq'own-slot'-and$current-eq$companion)-or($mode-eq'other-slot'-and$current-ne$companion)) 'Incorrect actual virtual actor arrangement.'
        $interval=$s.WorldIntervals|Where-Object ActorId -eq $companion
        Require (!$interval.ActionSpent) 'Companion Action was already spent.'
        $tear=[Decennium.Foundation.Command]::new("ferry.world.$mode.tear",$companion,$s.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
        $before=Bytes;$physical=$session.ObserveExposedSeal('Player',$companion)
        Require ($null-ne$physical-and!$physical.Torn) 'Actual exposed paper was not perceived.'
        Require ((@($physical.PSObject.Properties.Name|Sort-Object)-join',')-ceq'Description,Id,Torn,X,Y') 'Physical view leaked additional source information.'
        for($query=0;$query-lt3;$query++){
            Require ($session.QueryCastingCommand('Player',$tear).Admissible) 'Ordinary scheduled Action was not admitted.'
            Require (@($session.DiscoverCastingCommands('Player',$companion)|Where-Object {$_.Command.Kind-eq'TearExposedSeal'-and$_.Query.Admissible}).Count-eq1) 'Ordinary tear was not discovered exactly once.'
        }
        Require ($before-ceq(Bytes)) 'Repeated ordinary queries changed state or RNG.'
        Send $tear
        $after=Capture;$rupture=$after.FerryWraith.Rupture
        Require ($rupture.ActionLedger-eq'Scheduled'-and!$rupture.InInitiative-and$rupture.ActionCalendarId-eq$epoch.Id-and$rupture.ActionInterval-eq$interval.LastStart) 'Tear did not bind the actual owning scheduled interval.'
        Require ($rupture.ExpiresAt.Equals($s.RuleClock.AddSeconds(6))-and$after.RuleClock.Equals($s.RuleClock)-and$after.RandomState-eq$s.RandomState) 'Ordinary tear changed time/RNG or used an initiative deadline.'
        Require (($after.WorldIntervals|Where-Object ActorId -eq $companion).ActionSpent) 'Actual scheduled Action was not paid.'
        $record.rupture=$rupture;$record.virtualActorAtRupture=$current;$record.originalInterval=$interval
        Checkpoint 'world-suppressed'
        # Pay a fresh final edge arriving at the earliest eligible original defender Start.
        $s=Capture;$epoch=$s.PostRecoveryEncounter.Admission.Epoch;$slot=$epoch.SlotAt($s.RuleClock)
        $speed=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::WalkingSpeed($s,$hero)
        $duration=[Decennium.Foundation.RuleTime]::new(30,$speed)
        $record.approachSpeed=$speed;$record.approachDuration=$duration
        do {
            $arrival=$epoch.Start($slot)
            $departure=[Decennium.Foundation.RuleTime]::new($arrival.Numerator*$duration.Denominator-$duration.Numerator*$arrival.Denominator,$arrival.Denominator*$duration.Denominator)
            if($epoch.Order[[int]($slot%$epoch.Order.Count)]-eq'TEST_ONLY.recovery-defender'-and$departure.CompareTo($s.RuleClock)-ge0){break}
            $slot++
        } while($slot-lt1000)
        Require ($slot-lt1000) 'No finite paid contact marker.'
        AdvanceTo $departure
        $s=Capture
        Send ([Decennium.Foundation.Command]::new("ferry.world.$mode.approach",$hero,$s.Revision,'BeginWorldStep','walk',0,1))
        AdvanceTo $arrival
        $s=Capture
        Require ($null-ne$s.FerryWraith.Admission-and$s.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Real paid edge did not admit the Ferry encounter.'
        Require ($s.FerryWraith.Rupture.ExpiresAt.Equals($rupture.ExpiresAt)-and$s.FerryWraith.Rupture.ActionCalendarId-eq$epoch.Id-and$s.FerryWraith.ClawSuppressed) 'Entry rewrote the world deadline or original Action ledger.'
        $record.admission=$s.FerryWraith.Admission
        Checkpoint 'entered-with-world-deadline'
        for($step=0;$step-lt20;$step++){
            $s=Capture
            Require ($s.FerryWraith.Rupture.ExpiresAt.Equals($rupture.ExpiresAt)-and$s.FerryWraith.SealDestroyed) 'Original deadline or destruction changed.'
            if($s.RuleClock.CompareTo($rupture.ExpiresAt)-ge0){Require (!$s.FerryWraith.ClawSuppressed) 'Original world deadline did not expire.';break}
            Require ($s.FerryWraith.ClawSuppressed) 'World suppression expired early after entry.'
            if($session.View('Player').NextSeat-eq'FerryOpponent'){
                $view=$session.ObserveFerryDecision('FerryOpponent')
                Require (!$view.SourceAvailable) 'Creature view restored its source before the world deadline.'
                $result=$session.AdvanceAutomaticDefender();$record.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;beforeClock=$s.RuleClock;response=$result}
                Require ($result.Response-eq'Committed') 'Suppressed automatic creature step failed.'
            } else {
                $actor=$s.Encounter.CurrentActor
                $guard=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)})
                if($guard.Count-eq0){
                    $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
                    Send ([Decennium.Foundation.Command]::new("ferry.world.$mode.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat))
                } else {Send ([Decennium.Foundation.Command]::new("ferry.world.$mode.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))}
            }
        }
        $s=Capture
        Require (!$s.FerryWraith.ClawSuppressed-and$s.FerryWraith.SuppressionExpiredRevision-gt$rupture.Revision) 'Did not observe actual original-deadline expiry.'
        Checkpoint 'expired-original-world-deadline'
        $before=Bytes;$again=[Decennium.Foundation.Command]::new("ferry.world.$mode.again",$companion,$s.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
        Require ($session.Submit('Player',$again).Response-ne'Committed'-and$before-ceq(Bytes)) 'Expired paper could be torn again or reset.'
        $record.finalRevision=$s.Revision;$record.finalClock=$s.RuleClock;$record.finalFerry=$s.FerryWraith
        $record.expandedCommands=@($s.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
        Require ($record.expandedCommands.Count-eq$record.commands.Count) 'Actual command witness does not match saved history.'
        $record.checks+='Genuine scheduled ordinary Action, nonmutating discovery/query, unchanged clock/RNG, original world endpoint across paid entry, identical strict restores and persistent destruction'
    }
    $report.status='PASS_GENUINE_ORDINARY_SEAL_OWN_AND_OTHER_VIRTUAL_SLOT_ONLY'
} catch {
    $report.error=$_.Exception.ToString()
    if($null-ne$session-and$null-ne$field){
        $failed=Capture
        $report.failedState=@{revision=$failed.Revision;clock=$failed.RuleClock;actors=$failed.Actors;traversals=$failed.WorldTraversals;ferry=$failed.FerryWraith;encounter=$failed.Encounter}
    }
}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
