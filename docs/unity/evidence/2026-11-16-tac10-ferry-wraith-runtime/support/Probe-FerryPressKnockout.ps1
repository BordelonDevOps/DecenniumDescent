param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][ValidateSet('Press','Knockout')][string]$Plan,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh Press/knockout branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';plan=$Plan;scope='Genuine public source Claw Press follow or pending knockout branches; no state/resource injection and no whole-module acceptance';assemblies=@();commands=@();attacks=@();branches=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $compiled=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
    Require ($compiled.status-eq'PASS'-and$compiled.sourceHashes.Count-eq468) 'Expected the passing corrected468-input build.'
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryPressKnockout.executed.ps1')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Send($seat,$command){$result=$session.Submit($seat,$command);$report.commands+=@{seat=$seat;command=$command;response=$result};Require ($result.Response-eq'Committed') "$Plan rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"}
    function Auto {$s=Capture;$result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result};Require ($result.Response-eq'Committed') 'Actual source controller failed.'}
    function Stance($kind){$s=Capture;$request=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]$kind);Send 'Player' ([Decennium.Foundation.Command]::new("ferry.$Plan.stance.$($s.Revision)",$s.Encounter.CurrentActor,$s.Revision,'SelectCombatStance','',0,0,$null,$request))}
    function End {$s=Capture;Send 'Player' ([Decennium.Foundation.Command]::new("ferry.$Plan.end.$($s.Revision)",$s.Encounter.CurrentActor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))}
    function Checkpoint($name){$path=Join-Path $Run "$name.ddsave";$restored=Join-Path $Run "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($restored);Require ((Digest $path)-ceq(Digest $restored)) "Strict restore changed $name."}
    function Attack($knockout){
        $s=Capture;$request=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,[Decennium.Foundation.AttackKnockoutMode]$knockout,$false,'ArmOrReplace',[Decennium.Foundation.FerryWraithProfile]::Feature)
        $command=[Decennium.Foundation.Command]::new("ferry.$Plan.claw.$($s.Revision)",$ferry,$s.Revision,'AttackCreatureFeature',$hero,0,0,$null,$request)
        $before=Bytes;$query=$session.QueryCastingCommand('FerryOpponent',$command)
        Require ($query.Admissible-and$before-ceq(Bytes)) 'Actual owned source attack query rejected or mutated.'
        Send 'FerryOpponent' $command;$attack=(Capture).MeleeAttacks|Where-Object Revision -eq ($s.Revision+1)
        Require ($null-ne$attack-and$attack.WeaponId-eq[Decennium.Foundation.FerryWraithProfile]::Feature) 'Actual source attack record missing.'
        $report.attacks+=@{query=$query;attack=$attack}
    }
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry=[Decennium.Foundation.FerryWraithProfile]::Actor
    $initial=Capture;Require ($initial.Revision-eq351-and$initial.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected genuine first-fire r351.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'));Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Input strict restore changed bytes.'
    if($Plan-eq'Press'){
        Auto;Stance 'Guarded';End;Stance 'Guarded';End;Auto
        $s=Capture;Require ($s.Encounter.CurrentActor-eq$ferry-and$s.Encounter.TurnOrdinal-eq4) 'Expected actual source Start4.'
        Attack 'OrdinaryOutcome';$armedState=Capture;$attack=$report.attacks[-1].attack
        $armed=$armedState.Presses|Where-Object ActorId -eq $ferry
        Require ($attack.Attack.Hit-and$armed.TargetId-eq$hero-and$armed.ArmedRevision-eq$attack.Revision) 'Actual source hit did not arm Press.'
        $report.armed=$armed;Checkpoint 'source-press-armed'
        Auto;Stance 'Guarded';End;Stance 'Focused';$s=Capture
        Send 'Player' ([Decennium.Foundation.Command]::new("ferry.press.departure.$($s.Revision)",$hero,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,7,2))
        Require (@((Capture).TacticalMoves|Where-Object Pending).Count-eq1) 'Actual departure omitted its source opportunity.'
        Auto;$pending=Capture;$offer=$pending.PressOffers|Where-Object Status -eq 'Pending'
        Require ($null-ne$offer-and$offer.ActorId-eq$ferry-and$offer.TargetId-eq$hero-and$offer.ArmedRevision-eq$armed.ArmedRevision) 'Completed actual departure did not offer its armed Press.'
        $view=$session.View('FerryOpponent');Require ($view.PendingDecision-eq'Press'-and$view.DecisionId-eq$offer.Id) 'Public source seat did not expose the actual Press choice.'
        $report.pressView=$view;$report.pendingOffer=$offer;Checkpoint 'source-press-pending'
        $request=[Decennium.Foundation.CombatRequest]::new($pending.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$true)
        $command=[Decennium.Foundation.Command]::new("ferry.press.accept.$($pending.Revision)",$ferry,$pending.Revision,'RespondPress',$view.DecisionId,0,0,$null,$request)
        $before=Bytes;$report.choiceQuery=$session.QueryCastingCommand('FerryOpponent',$command)
        $report.choiceDiscovery=@($session.DiscoverCastingCommands('FerryOpponent',$ferry)|Where-Object {$_.Command.Kind-eq'RespondPress'})
        Require ($before-ceq(Bytes)) 'Press query/discovery changed state.'
        Send 'FerryOpponent' $command;$after=Capture
        $follow=@($after.TacticalMoves|Where-Object ParentPressOffer -eq $offer.Id);$body=$after.Actors|Where-Object Id -eq $ferry
        Require ($follow.Count-eq1-and$follow[0].Kind-eq'Press'-and$follow[0].Status-eq'Completed'-and$body.X-eq8-and$body.Y-eq2) 'Accepted source Press did not follow to the actually vacated8,2 anchor.'
        $oldInterval=$pending.WorldIntervals|Where-Object ActorId -eq $ferry;$newInterval=$after.WorldIntervals|Where-Object ActorId -eq $ferry
        Require (($oldInterval|ConvertTo-Json -Compress)-ceq($newInterval|ConvertTo-Json -Compress)-and($after.TacticalActors|Where-Object ActorId -eq $ferry).PressConsumed-and$after.RandomState-eq$pending.RandomState-and$after.RuleClock-eq$pending.RuleClock-and$after.MeleeAttacks.Count-eq$pending.MeleeAttacks.Count) 'Press repaid Action/Reaction/ordinary movement, attacked again, or changed time/RNG.'
        $report.followMove=$follow[0];$report.beforeInterval=$oldInterval;$report.afterInterval=$newInterval
        $stable=Bytes;Require ($session.Submit('FerryOpponent',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Press retry repeated its movement.'
        Checkpoint 'source-press-followed';End;$continued=Capture
        Require ($continued.Encounter.CurrentActor-eq$ferry-and$continued.Encounter.TurnOrdinal-eq7-and!($continued.TacticalActors|Where-Object ActorId -eq $ferry).PressConsumed) 'Actual next owner Start did not refresh its Press interval.'
        Checkpoint 'source-press-continued';$final=Capture
        $report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock
        $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt351}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
        Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Press command/receipt count changed.'
    } else {
        for($step=0;$step-lt100;$step++){
            $s=Capture;if(@($s.MeleeAttacks|Where-Object Pending).Count-gt0){break}
            $life=$s.Lives|Where-Object ActorId -eq $hero;Require (!$life.Dead-and$life.Hp-gt0) 'Hero resolved to zero before the selected pending source choice.'
            $actor=$s.Encounter.CurrentActor;$interval=$s.WorldIntervals|Where-Object ActorId -eq $actor
            $stance=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
            if($actor-eq$ferry){if($stance-and!$interval.ActionSpent){Attack 'AskIfEligible'}else{Auto};continue}
            Require ($actor-in@($hero,$companion)) 'Unexpected party actor.'
            if(!$stance){Stance 'Guarded'}else{End}
        }
        $pendingState=Capture;$pending=@($pendingState.MeleeAttacks|Where-Object Pending)
        Require ($pending.Count-eq1-and$pending[0].AttackerId-eq$ferry-and$pending[0].TargetId-eq$hero) 'Genuine damage sequence did not reach the source knockout decision.'
        $pending=$pending[0];$boundary=@($pendingState.TypedDamage|Where-Object EventId -eq $pending.Id);$priorLife=$pendingState.Lives|Where-Object ActorId -eq $hero
        Require ($boundary.Count-eq1-and$boundary[0].Effective-eq$pending.Damage.Total-and$priorLife.Hp-gt0) 'Pending attack lost its one retained effective damage boundary or prematurely applied life.'
        $report.pendingAttack=$pending;$report.pendingDamage=$boundary[0];$report.beforeLife=$priorLife
        $report.prefixExpandedCommands=@($pendingState.Receipts|Where-Object {$_.Revision-gt351}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
        Require ($report.prefixExpandedCommands.Count-eq$report.commands.Count) 'Knockout prefix command count changed.'
        Checkpoint 'source-knockout-pending';$prefixCommands=$report.commands
        foreach($choice in @($false,$true)){
            $session.Restore((Join-Path $Run 'source-knockout-pending.ddsave'));$report.commands=@();$label=if($choice){'knockout'}else{'ordinary'}
            $before=Capture;$view=$session.View('FerryOpponent');Require ($view.PendingDecision-eq'Knockout'-and$view.DecisionId-eq$pending.Id) 'Public source seat lost its knockout decision.'
            $request=[Decennium.Foundation.CombatRequest]::new($before.Encounter.CurrentTurnId,'',0,'OrdinaryOutcome',$choice)
            $command=[Decennium.Foundation.Command]::new("ferry.knockout.$label.$($before.Revision)",$ferry,$before.Revision,'ResolveKnockout',$view.DecisionId,0,0,$null,$request)
            $stable=Bytes;$query=$session.QueryCastingCommand('FerryOpponent',$command);Require ($stable-ceq(Bytes)) 'Knockout query mutated.'
            Require ($session.Submit('Player',$command).Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Party stole the source-owned knockout choice.'
            $session.SetSeatEnabled('FerryOpponent',$false);Require ($session.Submit('FerryOpponent',$command).Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Revoked source retained its choice.';$session.SetSeatEnabled('FerryOpponent',$true)
            Send 'FerryOpponent' $command;$after=Capture;$resolved=$after.MeleeAttacks|Where-Object Id -eq $pending.Id;$life=$after.Lives|Where-Object ActorId -eq $hero
            Require (!$resolved.Pending-and$resolved.ResolvedRevision-eq$after.Revision-and$life.Hp-eq0-and!$life.Dead-and$life.Stable-eq$choice) 'Source choice did not settle the expected ordinary/Stable life once.'
            Require (($before.TypedDamage|ConvertTo-Json -Depth 20 -Compress)-ceq($after.TypedDamage|ConvertTo-Json -Depth 20 -Compress)-and($pending.Attack|ConvertTo-Json -Compress)-ceq($resolved.Attack|ConvertTo-Json -Compress)-and$resolved.Damage.Total-eq$pending.Damage.Total-and$resolved.Damage.WoundNatural-eq$pending.Damage.WoundNatural-and$resolved.Damage.InjuryD6-eq$pending.Damage.InjuryD6-and$after.RuleClock-eq$before.RuleClock) 'Knockout completion repeated the typed boundary or rerolled attack/damage/Wound/injury.'
            if($choice){$draw=[Decennium.Foundation.DiceStream]::Draw($before.RandomState,4);Require ($after.RandomState-eq$draw.NextState-and$resolved.Damage.StableD4-eq($draw.Value+1)) 'Knockout did not draw exactly its single new Stable recovery d4.'}else{Require ($after.RandomState-eq$before.RandomState-and$resolved.Damage.StableD4-eq0) 'Ordinary resolution repeated authoritative RNG.'}
            $stable=Bytes;Require ($session.Submit('FerryOpponent',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Knockout retry repeated its life effect or RNG.'
            Checkpoint "source-$label-resolved";Auto;Stance 'Guarded';End;$continued=Capture
            Require ($continued.Encounter.CurrentActor-eq$hero) 'Actual continuation did not reach the next hero Start.'
            if($choice){Require (($continued.Lives|Where-Object ActorId -eq $hero).Stable-and$continued.RandomState-eq$after.RandomState) 'Stable hero took an early recovery/death-save RNG draw.'}
            Checkpoint "source-$label-continued";$final=Capture
            $expanded=@($final.Receipts|Where-Object {$_.Revision-gt$before.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
            Require ($expanded.Count-eq$report.commands.Count) 'Knockout branch command/receipt count changed.'
            $report.branches+=@{choice=$choice;query=$query;publicView=$view;resolved=$resolved;life=$life;afterRandom=$after.RandomState;continuedLife=($final.Lives|Where-Object ActorId -eq $hero);finalRevision=$final.Revision;finalClock=$final.RuleClock;finalRandom=$final.RandomState;commands=$report.commands;expandedCommands=$expanded}
        }
        $report.commands=$prefixCommands
    }
    $report.status="PASS_GENUINE_FERRY_$($Plan.ToUpperInvariant())_ONLY"
} catch {
    $report.error=$_.Exception.ToString()
    if($null-ne$session-and$null-ne$field){try{$failed=Capture;$report.failedRevision=$failed.Revision;$report.failedClock=$failed.RuleClock;$session.Save((Join-Path $Run 'failed-checkpoint.ddsave'))}catch{$report.failureCaptureError=$_.Exception.ToString()}}
}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
