param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$AdmissionSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$AdmissionSave=(Resolve-Path -LiteralPath $AdmissionSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh controller probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Actual first creature movement/fire attack from the genuine new-profile paid-admission checkpoint; seal/full-module qualification pending';checks=@();commands=@();assemblies=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    $report.admissionSource=@{path=$AdmissionSave;sha256=(Digest $AdmissionSave)}
    Copy-Item -LiteralPath $AdmissionSave -Destination (Join-Path $Run 'original-admission.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($AdmissionSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    function Capture { $field.GetValue($session).Capture() }
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    $start=Capture
    Require ($null-ne$start.FerryWraith.Admission-and$start.InventoryCombat-and$start.Encounter.Id-eq'TEST_ONLY.ferry-encounter') 'Genuine saved admission did not restore.'
    $before=[Convert]::ToBase64String($codec.Encode($start))
    Require ($session.ObserveFerryDecision('Player').FeatureId-eq'') 'Party controller view disclosed the private source.'
    $session.SetSeatEnabled('FerryOpponent',$false)
    Require ($session.AdvanceAutomaticDefender().Response-eq'NotAuthorized') 'Revoked creature seat dispatched a command.'
    Require ($session.ObserveFerryDecision('FerryOpponent').FeatureId-eq'') 'Revoked creature seat disclosed source.'
    $session.SetSeatEnabled('FerryOpponent',$true)
    Require ($before-ceq[Convert]::ToBase64String($codec.Encode((Capture)))) 'Authority/read probes changed live state.'
    $report.checks+='Actual new-profile admission restored; party/revoked controller views and revoked auto dispatch are nonmutating'
    for($step=0;$step-lt80;$step++){
        $state=Capture
        $attacks=@($state.MeleeAttacks|Where-Object {$_.AttackerId-eq'TEST_ONLY.ferry-wraith'})
        if(@($attacks|Where-Object {$_.Attack.Hit}).Count-gt0){break}
        $party=$session.View('Player')
        if($party.NextSeat-eq'FerryOpponent'){
            $view=$session.ObserveFerryDecision('FerryOpponent')
            $intent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($view)
            $view|ConvertTo-Json -Depth 20|Set-Content -LiteralPath (Join-Path $Run ("decision-$step.json")) -Encoding utf8
            $stable=[Convert]::ToBase64String($codec.Encode($state))
            $options=$session.DiscoverCastingCommands('FerryOpponent','TEST_ONLY.ferry-wraith')
            $options|ConvertTo-Json -Depth 20|Set-Content -LiteralPath (Join-Path $Run ("discovery-$step.json")) -Encoding utf8
            Require ($stable-ceq[Convert]::ToBase64String($codec.Encode((Capture)))) 'Creature discovery changed state/RNG.'
            if($intent.Kind-eq'Attack'){
                $source=@($options|Where-Object {$_.Command.Kind-eq'AttackCreatureFeature'-and$_.Command.Target-eq$intent.TargetId})
                Require ($source.Count-eq1-and$source[0].Command.Combat.FeatureId-eq'TEST_ONLY.ferry-wraith.hellfire-claw'-and$source[0].Query.Admissible) 'Owned source attack was not discoverable/admissible.'
                $session.Save((Join-Path $Run "before-attack-$step.ddsave"))
            }
            $result=$session.AdvanceAutomaticDefender()
            $report.commands+=@{mode='actual-public-auto';step=$step;revision=$state.Revision;intent=$intent;response=$result}
        } elseif($party.NextSeat-eq'Player'){
            $actor=$party.ActingActor
            if(!$actor){$actor=$state.Encounter.CurrentActor}
            Require (@($state.Lives|Where-Object {$_.ActorId-eq$actor-and!$_.Dead}).Count-eq1) 'Party member died before first creature hit.'
            $guarded=@($state.Stances|Where-Object { $_.ActorId -eq $actor -and $_.TurnOrdinal -eq $state.Encounter.TurnOrdinal -and [Decennium.Foundation.EncounterHistory]::InCurrent($state,$_.Revision) }).Count -gt 0
            if(!$guarded){
                $combat=[Decennium.Foundation.CombatRequest]::new($state.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
                $command=[Decennium.Foundation.Command]::new("ferry.probe.guard.$step",$actor,$state.Revision,'SelectCombatStance','',0,0,$null,$combat)
            } else {
                $command=[Decennium.Foundation.Command]::new("ferry.probe.end.$step",$actor,$state.Revision,'EndRegularTurn',$state.Encounter.CurrentTurnId)
            }
            $result=$session.Submit('Player',$command)
            $report.commands+=@{mode='actual-party-command';step=$step;command=$command;response=$result}
        } else {throw "Unexpected continuation seat: $($party.NextSeat)"}
        Require ($result.Response-eq'Committed') "Actual continuation failed at step $step`: $($result|ConvertTo-Json -Compress)"
    }
    $final=Capture
    $hit=@($final.MeleeAttacks|Where-Object {$_.AttackerId-eq'TEST_ONLY.ferry-wraith'-and$_.Attack.Hit})|Select-Object -First 1
    Require ($null-ne$hit) 'No genuine fire hit within bounded controller turns.'
    Require ($hit.WeaponId-eq'TEST_ONLY.ferry-wraith.hellfire-claw'-and$hit.Attack.Modifier-eq3-and!$hit.Opportunity) 'Creature used the wrong printed source/modifier.'
    Require ($hit.Damage.Dice.Count-eq$(if($hit.Attack.Critical){2}else{1})-and@($hit.Damage.Dice|Where-Object {$_-lt1-or$_-gt4}).Count-eq0) 'Creature did not roll the printed fire d4 dice.'
    $typed=@($final.TypedDamage|Where-Object {$_.EventId-eq$hit.Id})
    Require ($typed.Count-eq1-and$typed[0].DamageType-eq'fire'-and$typed[0].Raw-eq($hit.Damage.Dice|Measure-Object -Sum).Sum-and$typed[0].Effective-eq$hit.Damage.Total) 'Fire typed damage was missing, repeated or gained STR damage.'
    $creature=$final.Actors|Where-Object Id -eq 'TEST_ONLY.ferry-wraith'
    Require ($creature.X-ne10-or$creature.Y-ne2) 'The creature attacked without actually approaching from its contact position.'
    $session.Save((Join-Path $Run 'first-fire-hit.ddsave'))
    $session.Restore((Join-Path $Run 'first-fire-hit.ddsave'))
    $session.Save((Join-Path $Run 'first-fire-hit-restored.ddsave'))
    Require ((Digest (Join-Path $Run 'first-fire-hit.ddsave'))-ceq(Digest (Join-Path $Run 'first-fire-hit-restored.ddsave'))) 'Actual creature fire hit changed across verified restore/replay.'
    # Deliberately counterfeit condition history on the actual fire event. Both added
    # prefixes share its marker; the earlier one protects and the later one does not.
    # Structural consistency is deliberately allowed before real causal restore rejects it.
    $forged=$final.Copy()
    $actualDamage=$typed[0]
    $journal=$forged.Conditions|Where-Object Target -eq $actualDamage.TargetId
    $marker=$actualDamage.ConditionEvaluation
    Require ($journal.Now.CompareTo($marker)-le0) 'Forgery control requires the actual final damage marker.'
    $history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($journal)
    if($journal.Now.CompareTo($marker)-lt0){$history=$history.Append([Decennium.Foundation.ConditionOperation]::Advance('forged.poison.advance',$marker)).State}
    $application=[Decennium.Foundation.ConditionApplicationData]::new('forged.petrified','TEST_ONLY.caller','TEST_ONLY.unbound-event','Petrified',$null,'supplied-end',$true)
    $history=$history.Append([Decennium.Foundation.ConditionOperation]::Apply('forged.petrified.apply',$marker,$application)).State
    $earlierPrefix=$history.Journal.Operations.Count
    Require ($history.Ledger.View().Has('Petrified')) 'Earlier forged prefix did not protect.'
    $history=$history.Append([Decennium.Foundation.ConditionOperation]::End('forged.petrified.end',$marker,'forged.petrified','supplied-end')).State
    Require (!$history.Ledger.View().Has('Petrified')) 'Later forged prefix still protected.'
    $forged.Conditions=[Decennium.Foundation.ConditionJournal[]]@($forged.Conditions|ForEach-Object {if($_.Target-eq$journal.Target){$history.Journal}else{$_}})
    $falseProtection=[Decennium.Foundation.TypedDamageRecord]::new($actualDamage.EventId,$actualDamage.Revision,$actualDamage.At,$actualDamage.TargetId,$actualDamage.DamageType,$actualDamage.Raw,$actualDamage.AfterFlatReduction,$actualDamage.SuccessfulSaveHalf,$actualDamage.InnateResistanceSource,$actualDamage.ImmunitySource,$true,$earlierPrefix,[string[]]@('forged.petrified'),$journal.PolicyId,$journal.Origin,$marker)
    $forged.TypedDamage=[Decennium.Foundation.TypedDamageRecord[]]@($forged.TypedDamage|ForEach-Object {if($_.EventId-eq$actualDamage.EventId-and$_.TargetId-eq$actualDamage.TargetId){$falseProtection}else{$_}})
    [Decennium.Foundation.Laboratory.SharedTypedDamage]::ValidateConditionHistory($forged)
    $forgedPath=Join-Path $Run 'forged-earlier-prefix.ddsave'
    [IO.File]::WriteAllBytes($forgedPath,$codec.Encode($forged))
    $forgedHash=Digest $forgedPath
    $liveBefore=[Convert]::ToBase64String($codec.Encode((Capture)))
    $rejected=$false;$rejection=''
    try{$session.Restore($forgedPath)}catch{$rejected=$true;$rejection=$_.Exception.GetBaseException().Message}
    Require ($rejected-and$rejection-eq'InvalidSharedWorldReplay') "Earlier-prefix forgery was not rejected by actual causal replay: $rejection"
    Require ($liveBefore-ceq[Convert]::ToBase64String($codec.Encode((Capture)))-and$forgedHash-ceq(Digest $forgedPath)) 'Rejected restore mutated/repaired live state or the counterfeit input.'
    $report.forgery=@{scope='Counterfeit same-marker Petrified apply/end history and earlier protected prefix on the actual fire record; structural codec and historical ledger pass, causal command replay rejects';earlierPrefix=$earlierPrefix;laterPrefix=$history.Journal.Operations.Count;marker=$marker;rejection=$rejection;sha256=$forgedHash}
    $report.checks+=@('Actual source controller selected Guarded, moved toward seen hostiles and produced a genuine Claw fire hit','Printed+3/d4 or critical2d4; single typed fire settlement, no STR damage or fabricated weapon','Actual first fire hit save and verified restore/replay have identical bytes')
    $report.checks+='Structurally encodable same-marker earlier-prefix forgery passes pure history consistency but fails actual causal restore without mutation or repair'
    $report.attack=$hit;$report.typedDamage=$typed;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock
    $report.status='PASS_FIRST_GENUINE_CREATURE_FIRE_NOT_MODULE_ACCEPTANCE'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 45|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
