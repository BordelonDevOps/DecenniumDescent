param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh Refrain branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Five actual repeated Guidance casts reach ranked blocking; funded Invocation then positively vents Dissonance';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();casts=@();rankedQueries=@()}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryRefrain.executed.ps1')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Send($command){$result=$session.Submit('Player',$command);$report.commands+=@{command=$command;response=$result};Require ($result.Response-eq'Committed') "Refrain branch rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"}
    function Checkpoint($name){$path=Join-Path $Run "$name.ddsave";$copy=Join-Path $Run "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($copy);Require ((Digest $path)-ceq(Digest $copy)) "Refrain restore changed $name."}
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$start=Capture;$vented=$false;$done=$false
    Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected genuine first-fire input.'
    $report.initialStrain=$start.CastingStrain
    Require ($start.CastingStrain[0].LastSpellId-eq'guidance'-and$start.CastingStrain[0].Refrain-eq0-and$start.CastingStrain[0].Dissonance-eq0) 'Actual historical spell identity differs from this continued Refrain witness.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Strict restore changed input.'
    for($step=0;$step-lt100;$step++){
        $s=Capture
        Require (@($s.Lives|Where-Object {$_.ActorId-in@($hero,$companion)-and($_.Dead-or$_.Hp-le0)}).Count-eq0) 'Party life could not complete this actual casting branch.'
        if($session.View('Player').NextSeat-eq'FerryOpponent'){
            $result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result};Require ($result.Response-eq'Committed') 'Actual source turn failed.';continue
        }
        $actor=$s.Encounter.CurrentActor
        if(@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-eq0){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.refrain.stance.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        if($actor-eq$companion-and!($s.WorldIntervals|Where-Object ActorId -eq $companion).ActionSpent){
            $before=Bytes;$options=@($session.DiscoverCastingCommands('Player',$companion));Require ($before-ceq(Bytes)) 'Actual casting discovery mutated state.'
            $ranked=@($options|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'purify-food-and-drink'-and$_.Command.Target-eq'TEST_ONLY.cleric-casting.contaminated-water'})
            $guidance=@($options|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'guidance'-and$_.Command.Target-eq$hero})
            Require ($ranked.Count-eq1-and$guidance.Count-eq1-and$guidance[0].Query.Admissible) 'Actual owned ranked/cantrip options are not available for comparison.'
            $dissonance=$s.CastingStrain[0].Dissonance
            $report.rankedQueries+=@{revision=$s.Revision;ownerStart=($s.WorldIntervals|Where-Object ActorId -eq $companion).LastStart;dissonance=$dissonance;command=$ranked[0].Command;query=$ranked[0].Query}
            if($report.casts.Count-lt5){
                Require ($ranked[0].Query.Admissible) 'Ranked spell blocked before its actual Dissonance threshold.'
                $expectedCost=if($dissonance-ge9){4}elseif($dissonance-ge6){3}else{2}
                $rpCost=@($ranked[0].Query.Costs|Where-Object Kind -eq 'rp')
                Require ($rpCost.Count-eq1-and$rpCost[0].Amount-eq$expectedCost) "Actual ranked query surcharge differs: $($ranked[0].Query|ConvertTo-Json -Depth 6 -Compress)"
                $command=$guidance[0].Command;Send $command;$after=Capture;$cast=$after.SpellCasts|Where-Object CommandId -eq $command.Id
                $n=$report.casts.Count+1;$repeat=[Math]::Min(3,$n)
                Require ($cast.AppliedRefrain-eq$repeat-and$cast.DissonanceBefore-eq$dissonance-and$cast.DissonanceAfter-eq($dissonance+$repeat)-and$cast.RpBefore-eq7-and$cast.RpAfter-eq7-and$cast.WordsConsumed-eq0) 'Actual repeated cantrip did not preserve Refrain, free RP cost and RNG.'
                $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Repeated cantrip retry repeated Strain or effects.'
                $report.casts+=,$cast
                if($n-eq3){Checkpoint 'surcharge-one'}
                if($n-eq5){Checkpoint 'ranked-threshold'}
                continue
            }
            Require ($dissonance-eq12-and!$ranked[0].Query.Admissible-and$ranked[0].Query.Code-eq'RankedCastingBlockedByDissonance') 'Actual Refrain did not reach the source ranked-block threshold.'
            $report.blockedResponse=$session.Submit('Player',$ranked[0].Command)
            Require ($report.blockedResponse.Response-ne'Committed'-and$before-ceq(Bytes)) 'Blocked ranked cast paid, purified or changed state.'
            $report.allowedCantripQuery=$guidance[0].Query
            # Discovery need not enumerate every legal multi-recipient selection. Submit
            # the existing typed choice already qualified by the genuine care branch.
            $values=@{id="ferry.refrain.positive-vent.$($s.Revision)";actor=$companion;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($hero,$companion))}
            $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
            $args=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
            $command=$ctor.Invoke($args);$report.invocationQuery=$session.QueryCastingCommand('Player',$command)
            Require ($report.invocationQuery.Admissible-and$before-ceq(Bytes)) "Funded typed Invocation unavailable: $($report.invocationQuery|ConvertTo-Json -Compress)"
            Send $command;$after=Capture;$use=$after.BishopEntry.Invocations|Where-Object CommandId -eq $command.Id
            Require ($null-ne$use-and$use.DissonanceBefore-eq12-and$use.DissonanceAfter-eq11-and$use.ActualVent-eq1-and$use.RpBefore-eq7-and$use.RpAfter-eq4-and$use.ConvictionBefore-eq5-and$use.ConvictionAfter-eq3-and$use.WordsConsumed-eq1) 'Actual Invocation did not pay and positively vent once.'
            $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Invocation retry repeated its vent, healing or payment.'
            $report.invocation=$use;$vented=$true;Checkpoint 'positive-invocation-vent';continue
        }
        Send ([Decennium.Foundation.Command]::new("ferry.refrain.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
        if($vented-and$actor-eq$companion){$done=$true;break}
    }
    Require ($done-and$report.casts.Count-eq5) 'Did not complete the actual repeated-casting and positive-vent branch.'
    $final=Capture
    foreach($cast in @($report.casts)+@($report.invocation)){
        $ends=@($final.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq$cast.Turn.EpochId-and$_.Turn.ActorId-eq$companion-and$_.Turn.LocalStart-eq$cast.Turn.LocalStart})
        Require ($ends.Count-eq1-and$ends[0].MagicalActivity) 'Actual magical casting End missing or duplicated.'
    }
    Require ($final.CastingStrain[0].Dissonance-eq11-and($final.ResonancePools|Where-Object ActorId -eq $companion).Current-eq4-and$final.ConvictionBalance.Current-eq3) 'Outgoing magical End applied an extra reduction or resource change.'
    Checkpoint 'continued'
    $report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalStrain=$final.CastingStrain;$report.finalLives=@($final.Lives|Where-Object {$_.ActorId-in@($hero,$companion)});$report.effects=$final.SpellEffects
    $report.castingEnds=@($final.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar});$report.incomingAttacks=@($final.MeleeAttacks|Where-Object {$_.Revision-gt351})
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt351}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Actual Refrain command history does not reconcile.'
    $report.status='PASS_GENUINE_FERRY_REFRAIN_RANKED_BOUNDARY_AND_POSITIVE_VENT_ONLY'
} catch {$report.error=$_.Exception.ToString();if($null-ne$session-and$null-ne$field){$failed=Capture;$report.failedRevision=$failed.Revision;$session.Save((Join-Path $Run 'failed-checkpoint.ddsave'))}}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
