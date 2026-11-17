param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh Ward branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Two genuine alternate branches isolate Ward AC under actual incoming Claw with Focused stance';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();branches=@()}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryWardConsumer.executed.ps1')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    foreach($plan in 'WithoutWard','WithWard'){
        $directory=(New-Item -ItemType Directory -Path (Join-Path $Run $plan)).FullName
        $branch=[ordered]@{plan=$plan;commands=@();cast=$null;attack=$null}
        $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
            [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
            [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
        $session.Restore($FirstFireSave)
        $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
        $codec=[Decennium.Foundation.SnapshotCodec]::new()
        function Capture {$field.GetValue($session).Capture()}
        function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
        function Send($command){$result=$session.Submit('Player',$command);$branch.commands+=@{command=$command;response=$result};Require ($result.Response-eq'Committed') "Ward branch rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"}
        function Checkpoint($name){$path=Join-Path $directory "$name.ddsave";$copy=Join-Path $directory "$name-restored.ddsave";$session.Save($path);$session.Restore($path);$session.Save($copy);Require ((Digest $path)-ceq(Digest $copy)) "Ward restore changed $name."}
        $start=Capture;$hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion'
        Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected actual first-fire input.'
        $session.Save((Join-Path $directory 'verified-input.ddsave'))
        Require ((Digest (Join-Path $directory 'verified-input.ddsave'))-ceq$report.input.sha256) 'Strict input restore changed bytes.'
        $done=$false
        for($step=0;$step-lt25;$step++){
            $s=Capture
            if($s.Encounter.CurrentActor-eq$companion-and($s.WorldIntervals|Where-Object ActorId -eq $companion).LastStart-eq5){$done=$true;break}
            if($session.View('Player').NextSeat-eq'FerryOpponent'){
                $beforeAttacks=$s.MeleeAttacks.Count
                $result=$session.AdvanceAutomaticDefender();$branch.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result}
                Require ($result.Response-eq'Committed') 'Actual Claw controller continuation failed.'
                $after=Capture
                if($after.MeleeAttacks.Count-gt$beforeAttacks){
                    $branch.attack=$after.MeleeAttacks[-1]
                    $branch.attackTargetStance=@($s.Stances|Where-Object {$_.ActorId-eq$hero-and$_.TurnOrdinal-eq3-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)})
                    $branch.effectsBeforeAttack=$s.SpellEffects
                    Require ($branch.attack.AttackerId-eq[Decennium.Foundation.FerryWraithProfile]::Actor-and$branch.attack.TargetId-eq$hero-and$branch.attack.WeaponId-eq[Decennium.Foundation.FerryWraithProfile]::Feature) 'Expected actual source Claw against the selected recipient.'
                    Checkpoint 'after-claw'
                }
                continue
            }
            $actor=$s.Encounter.CurrentActor
            $stance=if($actor-eq$hero){[Decennium.Foundation.CombatStance]::Focused}else{[Decennium.Foundation.CombatStance]::Guarded}
            if(@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-eq0){
                $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int]$stance)
                $command=[Decennium.Foundation.Command]::new("ferry.ward.$plan.stance.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat)
                Send $command;continue
            }
            if($plan-eq'WithWard'-and$actor-eq$companion-and$null-eq$branch.cast){
                $before=Bytes
                $options=@($session.DiscoverCastingCommands('Player',$companion)|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'arcane-ward'-and$_.Command.Target-eq$hero-and$_.Query.Admissible})
                Require ($options.Count-eq1-and$before-ceq(Bytes)) 'Actual owned Ward discovery unavailable or impure.'
                $command=$options[0].Command
                Require ($session.QueryCastingCommand('Player',$command).Admissible-and$before-ceq(Bytes)) 'Ward query changed state.'
                Send $command;$after=Capture;$branch.cast=$after.SpellCasts|Where-Object CommandId -eq $command.Id
                Require ($branch.cast.WordsConsumed-eq0-and$branch.cast.RpBefore-eq7-and$branch.cast.RpAfter-eq7) 'Ward changed its actual cantrip cost or RNG.'
                $stable=Bytes;Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Ward retry mutated state.'
                Checkpoint 'active-ward';continue
            }
            Send ([Decennium.Foundation.Command]::new("ferry.ward.$plan.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$s.Encounter.CurrentTurnId))
        }
        Require ($done-and$null-ne$branch.attack) 'Did not reach actual post-Claw caster Start5.'
        $final=Capture
        Require ($branch.attackTargetStance.Count-eq1-and$branch.attackTargetStance[0].Kind-eq'Focused') 'Ward AC was confounded by a different recipient stance.'
        if($plan-eq'WithWard'){
            $active=$branch.effectsBeforeAttack|Where-Object Id -eq $branch.cast.EffectId
            $expired=$final.SpellEffects|Where-Object Id -eq $branch.cast.EffectId
            Require ($active.Present-and!$expired.Present-and$expired.ExpiresAt-eq$final.RuleClock) 'Ward did not protect the incoming attack and expire at original next caster Start.'
        }
        Checkpoint 'next-caster-start'
        $branch.finalRevision=$final.Revision;$branch.finalClock=$final.RuleClock;$branch.finalEffects=$final.SpellEffects;$branch.finalRandom=$final.RandomState
        $branch.finalLives=@($final.Lives|Where-Object {$_.ActorId-in@($hero,$companion)});$branch.observationCells=$final.ObservationCells
        $branch.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt351}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
        Require ($branch.expandedCommands.Count-eq$branch.commands.Count) 'Actual Ward command history does not reconcile.'
        $report.branches+=,$branch
    }
    $control=$report.branches[0].attack;$ward=$report.branches[1].attack
    Require ($ward.Attack.ArmorClass-eq($control.Attack.ArmorClass+1)) 'Actual Ward did not add exactly one AC to the otherwise matching Focused recipient.'
    Require ($ward.Attack.RandomBefore-eq$control.Attack.RandomBefore-and$ward.Attack.RandomAfter-eq$control.Attack.RandomAfter-and$ward.Attack.Selected-eq$control.Attack.Selected-and$ward.Attack.Modifier-eq$control.Attack.Modifier-and$ward.Damage.Total-eq$control.Damage.Total-and$report.branches[0].finalRandom-eq$report.branches[1].finalRandom) 'Comparison did not retain matching actual source rolls/outcomes.'
    $report.status='PASS_GENUINE_FERRY_WARD_AC_CONSUMER_ONLY'
} catch {$report.error=$_.Exception.ToString();if($null-ne$branch){$report.failedBranch=$branch}}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
