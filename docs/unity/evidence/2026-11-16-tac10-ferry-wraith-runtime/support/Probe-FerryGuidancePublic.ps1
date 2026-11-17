param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh Guidance branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Genuine Guidance consumption after paid movement and source Claw opportunity; existing Dash through the corrected public session query/discovery/submission surface';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@()}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $compiled=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
    Require ($compiled.coreCompilation-eq'PASS'-and$compiled.sourceHashes.Count-eq468) 'Expected a completed468-input C# compilation report; record its separate test result explicitly.'
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'));coreCompilation=$compiled.coreCompilation;testRunStatus=$compiled.status;passed=$compiled.passed;failed=$compiled.failed}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryGuidancePublic.executed.ps1')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Send($command){$result=$session.Submit('Player',$command);$report.commands+=@{command=$command;response=$result};Require ($result.Response-eq'Committed') "Guidance branch rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"}
    function Auto {$s=Capture;$result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result};Require ($result.Response-eq'Committed') 'Actual creature continuation failed.'}
    function Stance($kind){$s=Capture;$combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]$kind);Send ([Decennium.Foundation.Command]::new("ferry.guidance.stance.$($s.Revision)",$s.Encounter.CurrentActor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat))}
    function End {$s=Capture;Send ([Decennium.Foundation.Command]::new("ferry.guidance.end.$($s.Revision)",$s.Encounter.CurrentActor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))}
    function Checkpoint($name){$path=Join-Path $Run "$name.ddsave";$copy=Join-Path $Run "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($copy);Require ((Digest $path)-ceq(Digest $copy)) "Guidance restore changed $name."}
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry=[Decennium.Foundation.FerryWraithProfile]::Actor
    $start=Capture
    Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected genuine first-fire input.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Strict restore changed actual input.'
    Auto;Stance 'Guarded';$s=Capture
    # Keep the companion beyond30ft of the later Hide anchor and within the Wraith's
    # actual reach, using two paid edges rather than forcing a creature destination.
    foreach($cell in @(@(9,3),@(10,2))){
        $s=Capture
        Send ([Decennium.Foundation.Command]::new("ferry.guidance.companion-position.$($s.Revision)",$companion,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,$cell[0],$cell[1]))
    }
    $s=Capture;$before=Bytes
    $options=@($session.DiscoverCastingCommands('Player',$companion)|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'guidance'-and$_.Command.Target-eq$hero-and$_.Query.Admissible})
    Require ($options.Count-eq1-and$before-ceq(Bytes)) 'Actual owned Guidance discovery unavailable or impure.'
    $command=$options[0].Command;Send $command;$after=Capture;$cast=$after.SpellCasts|Where-Object CommandId -eq $command.Id
    Require ($cast.WordsConsumed-eq0-and$cast.RpBefore-eq7-and$cast.RpAfter-eq7-and$cast.Turn.LocalStart-eq2) 'Actual cantrip cost, RNG or owner turn changed.'
    $report.cast=$cast;$report.priorStrain=$s.CastingStrain;$report.afterCastStrain=$after.CastingStrain
    Checkpoint 'guidance-active';End;Stance 'Focused'
    $s=Capture;$before=Bytes
    $observed=@($session.DiscoverCastingCommands('Player',$hero)|Where-Object {$_.Command.Kind-eq'Hide'-and$_.Command.Guidance.EffectId-eq$cast.EffectId})
    Require ($observed.Count-eq1-and!$observed[0].Query.Admissible-and$before-ceq(Bytes)) 'Clearly observed Hide was not a pure denied choice.'
    $report.observedHideQuery=$observed[0].Query;$report.observedHideResponse=$session.Submit('Player',$observed[0].Command)
    Require ($report.observedHideResponse.Response-ne'Committed'-and$before-ceq(Bytes)) 'Rejected observed Hide spent Guidance, Action or RNG.'
    # The declaration prohibits standing inside any blocking channel. Route around the
    # declared terrain to supported2,0; the sight blocker2,1 remains an obstacle, not an anchor.
    $s=Capture;$dash=[Decennium.Foundation.Command]::new("ferry.guidance.dash.$($s.Revision)",$hero,$s.Revision,'EncounterDash',$s.Encounter.CurrentTurnId)
    $before=Bytes
    $report.sessionDashQuery=$session.QueryCastingCommand('Player',$dash)
    $report.discoveredDash=@($session.DiscoverCastingCommands('Player',$hero)|Where-Object {$_.Command.Kind-eq'EncounterDash'})
    Require ($report.sessionDashQuery.Admissible-and$report.discoveredDash.Count-eq1-and$report.discoveredDash[0].Query.Admissible-and$before-ceq(Bytes)) 'Public Dash query/discovery unavailable or impure.'
    Require ($report.sessionDashQuery.Costs.Count-eq1-and$report.sessionDashQuery.Costs[0].Kind-eq'action'-and$report.sessionDashQuery.Costs[0].Amount-eq1) 'Public Dash did not report its existing Action cost.'
    Send $dash
    $report.sessionDashSupported=$true
    $after=Capture;$interval=$after.WorldIntervals|Where-Object ActorId -eq $hero
    Require ($interval.ActionSpent-and$interval.DashPaid-and$after.RandomState-eq$s.RandomState-and$after.RuleClock-eq$s.RuleClock) 'Actual public Dash did not pay its shared Action/allowance without clock or RNG injection.'
    $report.publicDashInterval=$interval
    foreach($cell in @(@(7,2),@(6,3),@(5,2),@(4,2),@(3,1),@(2,0))){
        $s=Capture
        Send ([Decennium.Foundation.Command]::new("ferry.guidance.step.$($s.Revision)",$hero,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,$cell[0],$cell[1]))
        if($cell[0]-eq7-and$cell[1]-eq2){
            $pending=Capture;$move=$pending.TacticalMoves|Where-Object Pending
            Require ($null-ne$move-and$move.ActorId-eq$hero-and$move.Reactors[$move.ResponseIndex]-eq$ferry) 'Actual departure did not queue the owned Claw opportunity.'
            $view=$session.ObserveFerryDecision('FerryOpponent');$intent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($view)
            Require ($view.SourceAvailable-and$view.OpportunityEligible-and$intent.Kind-eq'AcceptOpportunity') 'Actual source controller did not admit the opportunity.'
            $report.pendingMove=$move;$report.opportunityView=$view;$report.opportunityIntent=$intent
            Checkpoint 'claw-opportunity-pending';$before=Capture;Auto;$after=Capture
            $attack=@($after.MeleeAttacks|Where-Object {$_.Revision-gt$before.Revision})
            Require ($attack.Count-eq1-and$attack[0].Opportunity-and$attack[0].AttackerId-eq$ferry-and$attack[0].TargetId-eq$hero-and$attack[0].WeaponId-eq[Decennium.Foundation.FerryWraithProfile]::Feature) 'Opportunity did not use exactly one actual owned Claw.'
            Require (($before.WorldIntervals|Where-Object ActorId -eq $ferry).ReactionAvailable-and!($after.WorldIntervals|Where-Object ActorId -eq $ferry).ReactionAvailable-and!($after.TacticalActors|Where-Object ActorId -eq $ferry).ReactionAvailable) 'Actual Claw opportunity did not pay its Reaction once.'
            $report.opportunityAttack=$attack[0];$report.opportunityBeforeRp=$before.ResonancePools;$report.opportunityAfterRp=$after.ResonancePools
            $done=$after.TacticalMoves|Where-Object Id -eq $move.Id;$position=$after.Actors|Where-Object Id -eq $hero
            Require ($done.Status-eq'Completed'-and$position.X-eq7-and$position.Y-eq2) 'Accepted opportunity did not finish the paid parent move.'
            $report.completedMove=$done;Checkpoint 'claw-opportunity-completed'
        }
    }
    Checkpoint 'screened-route-completed'
    # Dash used this Action. Advance actual source and companion turns before the check.
    End
    for($i=0;$i-lt8-and$session.View('Player').NextSeat-eq'FerryOpponent';$i++){Auto}
    $s=Capture;Require ($s.Encounter.CurrentActor-eq$companion-and$s.Encounter.TurnOrdinal-eq5) 'Actual source turn did not reach companion Start5.'
    Stance 'Guarded';End;Stance 'Focused';$s=Capture;$before=Bytes
    Require ($s.Encounter.CurrentActor-eq$hero-and$s.Encounter.TurnOrdinal-eq6) 'Did not reach the next actual hero Action.'
    $options=@($session.DiscoverCastingCommands('Player',$hero)|Where-Object {$_.Command.Kind-eq'Hide'-and$_.Command.Guidance.EffectId-eq$cast.EffectId})
    Require ($options.Count-eq1-and$options[0].Query.Admissible-and$before-ceq(Bytes)) "Actual screened Guidance Hide unavailable: $($options|ConvertTo-Json -Depth 8 -Compress)"
    $command=$options[0].Command;$report.hideQuery=$options[0].Query
    Send $command;$after=Capture
    $uses=@($after.GuidanceUses|Where-Object {$_.Revision-gt$s.Revision});$checks=@($after.ObservationActions|Where-Object {$_.Revision-gt$s.Revision})
    Require ($uses.Count-eq1-and$checks.Count-eq1-and$uses[0].EffectId-eq$cast.EffectId-and$uses[0].CheckKind-eq'Hide'-and$uses[0].D4-ge1-and$uses[0].D4-le4-and$uses[0].CheckId-eq$checks[0].Id) 'Guidance did not feed exactly one actual Hide check.'
    Require ($uses[0].RandomBefore-eq$s.RandomState-and$uses[0].RandomAfter-eq$checks[0].RandomBefore-and$checks[0].RandomAfter-eq$after.RandomState-and$uses[0].WordsConsumed-gt0-and$checks[0].WordsConsumed-gt0) 'Guidance and actual d20 did not consume their shared RNG in order.'
    $effect=$after.SpellEffects|Where-Object Id -eq $cast.EffectId
    Require (!$effect.Present-and$effect.EndReason-eq'GuidanceConsumed'-and$effect.EndRevision-eq$after.Revision-and($after.WorldIntervals|Where-Object ActorId -eq $hero).ActionSpent) 'Actual Guidance check did not consume its benefit and Action.'
    $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Guided Hide duplicate repeated benefit or RNG.'
    $report.guidanceUse=$uses[0];$report.hideCheck=$checks[0];$report.hideResults=@($after.ObservationHideResults|Where-Object AttemptId -eq $checks[0].Id);$report.consumedEffect=$effect
    Checkpoint 'guidance-consumed';End;Checkpoint 'continued'
    $final=Capture;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalRandom=$final.RandomState;$report.finalLives=@($final.Lives|Where-Object {$_.ActorId-in@($hero,$companion)});$report.finalStrain=$final.CastingStrain
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt351}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Actual Guidance history does not reconcile.'
    $report.status='PASS_GENUINE_PUBLIC_FERRY_DASH_GUIDANCE_AND_CLAW_OPPORTUNITY_ONLY'
} catch {
    $report.error=$_.Exception.ToString()
    if($null-ne$session-and$null-ne$field){$failed=Capture;$report.failedRevision=$failed.Revision;$report.failedClock=$failed.RuleClock;$session.Save((Join-Path $Run 'failed-checkpoint.ddsave'))}
}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
