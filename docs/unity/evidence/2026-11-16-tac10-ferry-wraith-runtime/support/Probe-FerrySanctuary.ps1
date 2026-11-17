param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh Sanctuary probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Genuine owned Sanctuary and failed source Claw admission, saved full payload, actual regular retarget/forgo branches and cached prohibition. Opportunity/Press/knockout qualification remains separate.';assemblies=@();prefixCommands=@();branches=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerrySanctuary.executed.ps1')
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
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object {
            if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}
        })
        $ctor.Invoke($args)
    }
    function Send($seat,$command){
        $result=$session.Submit($seat,$command)
        $row=@{seat=$seat;command=$command;response=$result}
        if($null-eq$branch){$report.prefixCommands+=,$row}else{$branch.commands+=,$row}
        Require ($result.Response-eq'Committed') "Sanctuary command failed: $($command.Kind) / $($result|ConvertTo-Json -Compress)"
    }
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$restored=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($restored)
        Require ((Digest $path)-ceq(Digest $restored)) "Strict restore changed $name."
    }
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry=[Decennium.Foundation.FerryWraithProfile]::Actor
    $branch=$null;$start=Capture;$warded=$false;$positioned=$false;$pending=$null
    Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected genuine first-fire input.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Current restore changed the original first-fire save.'
    for($step=0;$step-lt90;$step++){
        $s=Capture;$pending=$s.SanctuaryAdmissions|Where-Object Pending
        if($null-ne$pending){break}
        Require (@($s.Lives|Where-Object {$_.ActorId-in@($hero,$companion)-and($_.Dead-or$_.Hp-le0)}).Count-eq0) 'Party could not continue the genuine Sanctuary branch.'
        $actor=$s.Encounter.CurrentActor;$seat=if($actor-eq$ferry){'FerryOpponent'}else{'Player'}
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send $seat ([Decennium.Foundation.Command]::new("ferry.sanctuary.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat));continue
        }
        $interval=$s.WorldIntervals|Where-Object ActorId -eq $actor
        if($actor-eq$companion-and!$warded-and!$interval.ActionSpent){
            $spell=[Decennium.Foundation.SpellCastRequest]::new('sanctuary',[Decennium.Foundation.SpellCastingProfile]::FocusId,$true)
            $cast=MakeCommand @{id="ferry.sanctuary.cast.$($s.Revision)";actor=$actor;revision=$s.Revision;kind=[Decennium.Foundation.CommandKind]::CastKnownSpell;target=$hero;spellCast=$spell}
            $before=Bytes;Require ($session.QueryCastingCommand('Player',$cast).Admissible-and$before-ceq(Bytes)) 'Actual owned Sanctuary was unavailable or query mutated.'
            Send 'Player' $cast;$warded=$true;$report.cast=(Capture).SpellCasts|Where-Object CommandId -eq $cast.Id
            continue
        }
        if($actor-eq$ferry-and$warded-and!$interval.ActionSpent){
            # Select explicit non-controller-default knockout and Press options so their
            # exact preservation is observable through the real pending source path.
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',0,'AskIfEligible',$false,'ArmOrReplace',[Decennium.Foundation.FerryWraithProfile]::Feature)
            $attack=[Decennium.Foundation.Command]::new("ferry.sanctuary.claw.$($s.Revision)",$actor,$s.Revision,'AttackCreatureFeature',$hero,0,0,$null,$combat)
            $before=Bytes;Require ($session.QueryCastingCommand('FerryOpponent',$attack).Admissible-and$before-ceq(Bytes)) 'Actual source Claw was unavailable or query drew a save.'
            Send 'FerryOpponent' $attack;continue
        }
        if($actor-eq$companion-and$warded-and!$positioned){
            # The real controller stood at9,1 for its first Claw. Pay two legal
            # nondeparting steps to put the companion at9,2 for an actual5ft retarget.
            Send 'Player' ([Decennium.Foundation.Command]::new("ferry.sanctuary.position.1.$($s.Revision)",$actor,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,9,3))
            $s=Capture
            Send 'Player' ([Decennium.Foundation.Command]::new("ferry.sanctuary.position.2.$($s.Revision)",$actor,$s.Revision,'TacticalStep',$s.Encounter.CurrentTurnId,9,2))
            $positioned=$true;continue
        }
        Send $seat ([Decennium.Foundation.Command]::new("ferry.sanctuary.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
    }
    Require ($null-ne$pending-and$warded) 'No actual failed Sanctuary admission occurred.'
    $s=Capture;$save=$s.SpellSaves|Where-Object Id -eq $pending.SaveId
    $sourceReceipt=$s.Receipts|Where-Object Id -eq $pending.SourceCommandId
    $source=[Decennium.Foundation.CommandHistory]::Read($sourceReceipt)
    Require ($pending.Source-eq'RegularCreatureFeature'-and$source.Kind-eq'AttackCreatureFeature'-and$source.Combat.FeatureId-eq[Decennium.Foundation.FerryWraithProfile]::Feature-and$source.Combat.WeaponId-eq'') 'Pending admission lost the actual Claw source.'
    Require ($source.Combat.Knockout-eq'AskIfEligible'-and$source.Combat.PressInstruction-eq'ArmOrReplace') 'Pending source lost explicit knockout/Press options.'
    Require (!$save.Success-and$save.SubjectId-eq$ferry-and$save.Modifier-eq0-and$save.AttackerTurn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar) 'Creature ward save did not use actual non-class WIS0 and owning epoch.'
    Require (@($s.MeleeAttacks|Where-Object Revision -eq $pending.SourceRevision).Count-eq0-and!($s.WorldIntervals|Where-Object ActorId -eq $ferry).ActionSpent) 'Failed save resolved the attack or paid its Action early.'
    $report.pending=$pending;$report.save=$save;$report.sourceCommand=$source
    Checkpoint 'pending-source-claw'
    $verified=Capture;$read=[Decennium.Foundation.CommandHistory]::Read(($verified.Receipts|Where-Object Id -eq $source.Id))
    Require (($read|ConvertTo-Json -Depth 10 -Compress)-ceq($source|ConvertTo-Json -Depth 10 -Compress)) 'Pending restore changed the full typed attack payload.'
    $report.prefixExpandedCommands=@($verified.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.prefixExpandedCommands.Count-eq$report.prefixCommands.Count) 'Common actual prefix does not reconcile.'
    foreach($choice in 'Forgo','Retarget'){
        $session.Restore((Join-Path $Run 'pending-source-claw.ddsave'))
        $branch=[ordered]@{choice=$choice;commands=@();checks=@()};$report.branches+=,$branch
        $before=Capture;$stable=Bytes
        $request=[Decennium.Foundation.SanctuaryResponseRequest]::new($choice,$(if($choice-eq'Retarget'){$companion}else{''}))
        $response=MakeCommand @{id="ferry.sanctuary.$($choice.ToLowerInvariant())";actor=$ferry;revision=$before.Revision;kind=[Decennium.Foundation.CommandKind]::RespondSanctuary;target=$pending.Id;sanctuaryResponse=$request}
        $session.SetSeatEnabled('FerryOpponent',$false)
        Require ($session.Submit('FerryOpponent',$response).Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Revoked creature retained pending-choice authority.'
        $session.SetSeatEnabled('FerryOpponent',$true)
        Require ($session.Submit('Player',$response).Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Party stole creature pending-choice authority.'
        $query=$session.QueryCastingCommand('FerryOpponent',$response);$branch.query=$query
        Require ($query.Admissible-and$stable-ceq(Bytes)) "Lawful source-preserving response was not a pure admissible query: $($query|ConvertTo-Json -Compress)"
        Send 'FerryOpponent' $response
        $after=Capture;$resolved=$after.SanctuaryAdmissions|Where-Object Id -eq $pending.Id
        $beforeWardSaves=@($before.SpellSaves|Where-Object {$_.Kind-eq'SanctuaryWisdom'})
        $afterWardSaves=@($after.SpellSaves|Where-Object {$_.Kind-eq'SanctuaryWisdom'})
        Require (!$resolved.Pending-and$resolved.SourceFingerprint-ceq$sourceReceipt.Fingerprint-and$after.RuleClock.Equals($before.RuleClock)-and$afterWardSaves.Count-eq$beforeWardSaves.Count) 'Response changed source fingerprint, time or redrew the ward save.'
        $branch.newSpellSaves=@($after.SpellSaves|Where-Object {$_.Revision-gt$before.Revision})
        if($choice-eq'Forgo'){
            Require ($resolved.Status-eq'Forgone'-and$after.RandomState-eq$before.RandomState-and$after.MeleeAttacks.Count-eq$before.MeleeAttacks.Count-and!($after.WorldIntervals|Where-Object ActorId -eq $ferry).ActionSpent) 'Regular forgo paid or rolled an attack.'
            $retry=[Decennium.Foundation.Command]::new('ferry.sanctuary.cached-prohibited',$ferry,$after.Revision,'AttackCreatureFeature',$hero,0,0,$null,$source.Combat)
            $stable=Bytes
            Require (!$session.QueryCastingCommand('FerryOpponent',$retry).Admissible-and$session.Submit('FerryOpponent',$retry).Response-ne'Committed'-and$stable-ceq(Bytes)) 'Cached failure redrew, paid, or bypassed the ward.'
            $branch.checks+='Cached original target remains prohibited without RNG/payment/revision; regular forgo preserves unspent Action'
        } else {
            $attack=$after.MeleeAttacks|Where-Object Revision -eq $after.Revision
            Require ($resolved.Status-eq'Retargeted'-and$null-ne$attack-and$attack.TargetId-eq$companion-and$attack.WeaponId-eq$source.Combat.FeatureId-and$attack.Instruction-eq$source.Combat.Knockout-and$attack.PressInstruction-eq$source.Combat.PressInstruction-and$attack.Attack.Modifier-eq3-and$attack.Attack.RandomBefore-eq$save.RandomAfter) 'Retarget changed the source, options, bonus or random continuation.'
            Require (($after.WorldIntervals|Where-Object ActorId -eq $ferry).ActionSpent) 'Real retarget did not pay the original Action entitlement.'
            $branch.attack=$attack;$branch.typedDamage=@($after.TypedDamage|Where-Object {$_.Revision-eq$after.Revision})
            $branch.checks+='Retarget resolves original source Claw with exact AskIfEligible/ArmOrReplace payload and one actual Action'
        }
        $stable=Bytes
        Require ($session.Submit('FerryOpponent',$response).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Response retry repeated resolution.'
        $session.SetSeatEnabled('FerryOpponent',$false)
        Require ($session.Submit('FerryOpponent',$response).Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Revoked duplicate exposed saved authority.'
        $session.SetSeatEnabled('FerryOpponent',$true)
        Checkpoint ($choice.ToLowerInvariant()+'-resolved')
        $after=Capture
        Send 'FerryOpponent' ([Decennium.Foundation.Command]::new("ferry.sanctuary.$choice.end",$ferry,$after.Revision,'EndRegularTurn',$after.Encounter.CurrentTurnId))
        $ended=Capture;Require ($ended.Encounter.CurrentActor-ne$ferry) 'Resolved regular choice stalled its actual turn.'
        Checkpoint ($choice.ToLowerInvariant()+'-continued')
        $branch.finalRevision=$ended.Revision;$branch.finalClock=$ended.RuleClock;$branch.resolved=$resolved
        $branch.expandedCommands=@($ended.Receipts|Where-Object {$_.Revision-gt$verified.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
        Require ($branch.expandedCommands.Count-eq$branch.commands.Count) 'Branch command history does not reconcile.'
    }
    $report.status='PASS_GENUINE_SANCTUARY_REGULAR_SOURCE_RETARGET_FORGO_ONLY'
} catch {
    $report.error=$_.Exception.ToString()
    if($null-ne$session-and$null-ne$field){$s=Capture;$report.failedState=@{revision=$s.Revision;clock=$s.RuleClock;lives=$s.Lives;pending=$s.SanctuaryAdmissions;spellSaves=$s.SpellSaves;intervals=$s.WorldIntervals}}
}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
