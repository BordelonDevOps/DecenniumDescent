param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ForgoSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ForgoSave=(Resolve-Path -LiteralPath $ForgoSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh cached-opportunity probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Actual departure queues Claw opportunity under a cached failed Sanctuary save; lawful controller decline advances movement without Reaction/RNG, then next real source Start refreshes ward admission. Not complete OA/Press qualification.';assemblies=@();commands=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerrySanctuaryOpportunity.executed.ps1')
    $report.input=@{path=$ForgoSave;sha256=(Digest $ForgoSave)}
    Copy-Item -LiteralPath $ForgoSave -Destination (Join-Path $Run 'original-forgo-continued.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($ForgoSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function MakeCommand($values){
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object {if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($args)
    }
    function Send($seat,$command){
        $result=$session.Submit($seat,$command);$report.commands+=@{seat=$seat;command=$command;response=$result}
        Require ($result.Response-eq'Committed') "Opportunity continuation rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"
    }
    function Guard($seat){
        $s=Capture;$actor=$s.Encounter.CurrentActor
        if(@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-eq0){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send $seat ([Decennium.Foundation.Command]::new("ferry.cached.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat))
        }
    }
    function End($seat){$s=Capture;Send $seat ([Decennium.Foundation.Command]::new("ferry.cached.end.$($s.Revision)",$s.Encounter.CurrentActor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$restored=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($restored)
        Require ((Digest $path)-ceq(Digest $restored)) "Strict replay changed $name."
    }
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry=[Decennium.Foundation.FerryWraithProfile]::Actor
    $start=Capture;$oldSave=$start.SpellSaves|Where-Object {$_.Kind-eq'SanctuaryWisdom'-and!$_.Success}|Select-Object -Last 1
    Require ($null-ne$oldSave-and$oldSave.AttackerTurn.LocalStart-eq4-and$start.Encounter.CurrentActor-eq$companion-and$start.Encounter.TurnOrdinal-eq5) 'Expected the actual failed-gate forgo continuation at companion Start5.'
    Require (@($start.SanctuaryAdmissions|Where-Object Pending).Count-eq0) 'Input still has an unresolved Sanctuary choice.'
    Checkpoint 'verified-input'
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Strict input restore changed source bytes.'
    Guard 'Player';End 'Player';Guard 'Player'
    $s=Capture
    Require ($s.Encounter.CurrentActor-eq$hero-and$s.Encounter.TurnOrdinal-eq6-and($s.WorldIntervals|Where-Object ActorId -eq $ferry).LastStart-eq4) 'Actual source interval changed before departure.'
    $body=$s.Actors|Where-Object Id -eq $hero
    Require ($body.X-eq8-and$body.Y-eq2) 'Hero is not at the actual adjacent departure anchor.'
    Send 'Player' ([Decennium.Foundation.Command]::new('ferry.cached.depart',$hero,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,7,2))
    $s=Capture;$move=$s.TacticalMoves|Where-Object Pending
    Require ($null-ne$move-and$move.Reactors[$move.ResponseIndex]-eq$ferry-and$move.ActorId-eq$hero) 'Actual departure did not queue the owned Claw opportunity.'
    $view=$session.ObserveFerryDecision('FerryOpponent');$intent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($view)
    Require ($view.SourceAvailable-and$intent.Kind-eq'DeclineOpportunity') 'Controller did not distinguish available source from its cached target prohibition.'
    $accept=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$true,'KeepExisting',[Decennium.Foundation.FerryWraithProfile]::Feature)
    $request=[Decennium.Foundation.Command]::new('ferry.cached.prohibited-accept',$ferry,$s.Revision,'RespondOpportunityAttack',$move.Id,0,0,$null,$accept)
    $stable=Bytes;$query=$session.QueryCastingCommand('FerryOpponent',$request)
    Require (!$query.Admissible-and$session.Submit('FerryOpponent',$request).Response-ne'Committed'-and$stable-ceq(Bytes)) 'Cached failed admission redrew, paid or resolved an opportunity.'
    $report.cachedQuery=$query;$report.controllerView=$view;$report.controllerIntent=$intent;$report.pendingMove=$move;$report.originalWardSave=$oldSave
    Checkpoint 'cached-opportunity-pending'
    $before=Capture;$result=$session.AdvanceAutomaticDefender()
    $report.commands+=@{mode='actual-public-auto';beforeRevision=$before.Revision;response=$result}
    Require ($result.Response-eq'Committed') 'Lawful automatic cached decline failed.'
    $after=Capture;$done=$after.TacticalMoves|Where-Object Id -eq $move.Id;$body=$after.Actors|Where-Object Id -eq $hero
    Require ($done.Status-eq'Completed'-and$body.X-eq7-and$body.Y-eq2-and@($after.TacticalMoves|Where-Object Pending).Count-eq0) 'Cached decline stalled the parent movement.'
    Require ($after.RandomState-eq$before.RandomState-and$after.SpellSaves.Count-eq$before.SpellSaves.Count-and$after.MeleeAttacks.Count-eq$before.MeleeAttacks.Count-and($after.WorldIntervals|Where-Object ActorId -eq $ferry).ReactionAvailable-and($after.TacticalActors|Where-Object ActorId -eq $ferry).ReactionAvailable) 'Cached decline drew, attacked or spent a Reaction.'
    $report.completedMove=$done
    Checkpoint 'cached-opportunity-declined'
    # Re-enter reach through a second paid edge, then advance to the real next source Start.
    $s=Capture;Send 'Player' ([Decennium.Foundation.Command]::new('ferry.cached.return',$hero,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,8,2))
    End 'Player';Guard 'FerryOpponent';$s=Capture
    Require ($s.Encounter.CurrentActor-eq$ferry-and$s.Encounter.TurnOrdinal-eq7-and($s.WorldIntervals|Where-Object ActorId -eq $ferry).LastStart-eq7) 'Did not reach the actual next source Start.'
    $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$false,'KeepExisting',[Decennium.Foundation.FerryWraithProfile]::Feature)
    $attack=[Decennium.Foundation.Command]::new('ferry.cached.next-source-attack',$ferry,$s.Revision,'AttackCreatureFeature',$hero,0,0,$null,$combat)
    $stable=Bytes;Require ($session.QueryCastingCommand('FerryOpponent',$attack).Admissible-and$stable-ceq(Bytes)) 'New source interval failed to refresh admission or query drew a save.'
    $oldCount=@($s.SpellSaves|Where-Object {$_.Kind-eq'SanctuaryWisdom'}).Count
    Send 'FerryOpponent' $attack
    $after=Capture;$saves=@($after.SpellSaves|Where-Object {$_.Kind-eq'SanctuaryWisdom'});$fresh=$saves[-1]
    Require ($saves.Count-eq$oldCount+1-and$fresh.EffectId-eq$oldSave.EffectId-and$fresh.AttackerTurn.LocalStart-eq7-and$fresh.AttackerTurn.EpochId-eq$oldSave.AttackerTurn.EpochId-and$fresh.RandomBefore-eq$s.RandomState-and$fresh.Modifier-eq0) 'Next actual source Start did not make exactly one fresh source WIS save.'
    $report.refreshedWardSave=$fresh
    $pending=$after.SanctuaryAdmissions|Where-Object Pending
    if($null-ne$pending){
        $response=MakeCommand @{id='ferry.cached.new-interval-forgo';actor=$ferry;revision=$after.Revision;kind=[Decennium.Foundation.CommandKind]::RespondSanctuary;target=$pending.Id;sanctuaryResponse=[Decennium.Foundation.SanctuaryResponseRequest]::new('Forgo')}
        Send 'FerryOpponent' $response
    }
    End 'FerryOpponent';Checkpoint 'completed-next-source-interval'
    $final=Capture;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Actual cached-opportunity command history does not reconcile.'
    $report.status='PASS_GENUINE_CACHED_CLAW_OPPORTUNITY_DECLINE_AND_NEXT_START_REFRESH_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
