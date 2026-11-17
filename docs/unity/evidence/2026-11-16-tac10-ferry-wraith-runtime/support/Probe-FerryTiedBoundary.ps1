param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$SuppressedSave,[Parameter(Mandatory)][string]$ClosedSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$SuppressedSave=(Resolve-Path -LiteralPath $SuppressedSave).Path;$ClosedSave=(Resolve-Path -LiteralPath $ClosedSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh tied boundary branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Genuine paid casting End at the original seal expiry and next owner Start; actual single-use admission assessment on genuine closed state, not an invented public reentry command';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();restorePairs=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryTiedBoundary.executed.ps1')
    Copy-Item -LiteralPath $SuppressedSave -Destination (Join-Path $Run 'original-suppressed.ddsave');Copy-Item -LiteralPath $ClosedSave -Destination (Join-Path $Run 'original-closed.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$SuppressedSave;sha256=(Digest $SuppressedSave)};$report.closedInput=@{path=$ClosedSave;sha256=(Digest $ClosedSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($SuppressedSave);$flags=[Reflection.BindingFlags]'Instance,NonPublic';$field=$session.GetType().GetField('simulation',$flags);$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$after=Join-Path $Run "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($after)
        Require ((Digest $path)-ceq(Digest $after)) "Strict restore changed $name.";$report.restorePairs+=@{name=$name;sha256=(Digest $path)}
    }
    function Send($command){$response=$session.Submit('Player',$command);$report.commands+=@{command=$command;response=$response};Require ($response.Response-eq'Committed') "Boundary rejected: $($command.Kind) / $($response.Response)"}
    $start=Capture;$deadline=$start.FerryWraith.Rupture.ExpiresAt;$comp='TEST_ONLY.companion';$hero='TEST_ONLY.actor';$cast=$null;$tied=$false
    Require ($start.Revision-eq354-and$start.FerryWraith.ClawSuppressed) 'Expected genuine paid tear at354.'
    Checkpoint 'before-continuation'
    for($step=0;$step-lt30;$step++){
        $s=Capture;$view=$session.View('Player')
        if($view.NextSeat-eq'FerryOpponent'){$decision=$session.ObserveFerryDecision('FerryOpponent');$response=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-controller';decision=$decision;response=$response};Require ($response.Response-eq'Committed') 'Boundary controller failed.';continue}
        Require ($view.NextSeat-eq'Player'-and$s.FerryWraith.ClawSuppressed) 'Missed original suppression boundary.'
        $actor=$s.Encounter.CurrentActor;$interval=$s.WorldIntervals|Where-Object ActorId -eq $actor
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded){$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded);Send ([Decennium.Foundation.Command]::new("ferry.tie.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue}
        if($actor-eq$comp-and!$interval.ActionSpent){
            $before=Bytes;$options=@($session.DiscoverCastingCommands('Player',$comp)|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'guidance'-and$_.Command.Target-eq$hero-and$_.Query.Admissible})
            Require ($options.Count-eq1-and$before-ceq(Bytes)) 'Genuine Guidance not discoverable at final pre-expiry owner turn.'
            Send $options[0].Command;$cast=(Capture).SpellCasts|Where-Object CommandId -eq $options[0].Command.Id;continue
        }
        $epoch=[Decennium.Foundation.WorldTiming]::ForEncounter($s);$due=$epoch.Start($epoch.ProcessedSlot+1)
        if($due.Equals($deadline)){
            Require ($actor-eq$comp-and$null-ne$cast-and$cast.Turn.LocalStart-eq$interval.LastStart) 'Tied End lacked actual source casting on the outgoing turn.'
            Checkpoint 'before-tied-end';$beforeEnds=$s.CastingTurnEnds.Count;$beforeHero=($s.WorldIntervals|Where-Object ActorId -eq $hero).LastStart
            Send ([Decennium.Foundation.Command]::new("ferry.tie.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
            $after=Capture;$end=$after.CastingTurnEnds|Select-Object -Last 1;$heroInterval=$after.WorldIntervals|Where-Object ActorId -eq $hero
            Require ($after.RuleClock.Equals($deadline)-and$after.CastingTurnEnds.Count-eq($beforeEnds+1)-and$end.At.Equals($deadline)-and$end.Revision-eq$after.Revision) 'Actual casting End not settled at the tied marker.'
            Require (!$after.FerryWraith.ClawSuppressed-and$after.FerryWraith.SealDestroyed-and$after.FerryWraith.SuppressionExpiredRevision-eq$after.Revision-and$after.FerryWraith.Rupture.ExpiresAt.Equals($deadline)) 'Original seal expiry not settled in the same command.'
            Require ($after.Encounter.CurrentActor-eq$hero-and$heroInterval.LastStart-gt$beforeHero-and!$heroInterval.ActionSpent) 'Next actual owner Start not processed exactly after the tied boundary.'
            $report.tied=@{beforeRevision=$s.Revision;afterRevision=$after.Revision;deadline=$deadline;cast=$cast;castingEnd=$end;priorHeroStart=$beforeHero;newHeroInterval=$heroInterval;rupture=$after.FerryWraith.Rupture;expiredRevision=$after.FerryWraith.SuppressionExpiredRevision;orderingSource='TestOnlySharedWorldPolicy.AdvanceWorld: ExpireEndMarkers -> ExpireFerrySealSuppression -> RefreshActivityIntervals -> RefreshIntervals / ProcessSharedLifeMarkers; casting End settlement remains before next actor commands'}
            Checkpoint 'after-tied-end-expiry-start';$tied=$true;break
        }
        Send ([Decennium.Foundation.Command]::new("ferry.tie.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    Require $tied 'No genuine casting-End/expiry/Start tie.'
    $final=Capture;$report.finalRevision=$final.Revision;$report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object{@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.commands.Count-eq$report.expandedCommands.Count) 'Tied command/receipt counts differ.'
    $session.Restore($ClosedSave);$closed=Capture;Require (!$closed.InventoryCombat-and$null-ne$closed.FerryWraith.Admission) 'Single-use check needs genuinely closed source.'
    $before=Bytes;$policy=$session.GetType().GetField('policy',$flags).GetValue($session);$method=$policy.GetType().GetMethod('AssessFerryContact',$flags)
    $denial=$method.Invoke($policy,[object[]]@($closed,$false));$arrivalDenial=$method.Invoke($policy,[object[]]@($closed,$true))
    Require ($denial-eq'FerryEncounterAlreadyEntered'-and$arrivalDenial-eq$denial-and$before-ceq(Bytes)) 'Actual single-use admission gate changed or mutated.'
    $report.reentry=@{scope='Read-only direct existing source gate over genuine closed state; no public reentry API invented';departure=$denial;arrival=$arrivalDenial;unchanged=$true}
    Checkpoint 'closed-single-use'
    $report.status='PASS_GENUINE_CASTING_END_SEAL_EXPIRY_START_AND_SINGLE_USE_GATE'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run";if($report.status-eq'FAIL'){throw $report.error}
