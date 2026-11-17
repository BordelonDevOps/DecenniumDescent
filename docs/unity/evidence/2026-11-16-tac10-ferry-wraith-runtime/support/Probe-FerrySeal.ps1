param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh seal probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Genuine first fire -> paid seal tear -> saved suppression -> original expiry -> recovered Claw; full module qualification pending';checks=@();commands=@();assemblies=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerrySeal.executed.ps1')
    $report.firstFireSource=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    function Capture { $field.GetValue($session).Capture() }
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Bytes { [Convert]::ToBase64String($codec.Encode((Capture))) }
    $start=Capture
    Require (@($start.MeleeAttacks|Where-Object {$_.AttackerId-eq'TEST_ONLY.ferry-wraith'-and$_.Attack.Hit}).Count-gt0) 'No genuine preceding first fire.'
    $session.Save((Join-Path $Run 'verified-current-first-fire.ddsave'))
    Require ((Digest $FirstFireSave)-ceq(Digest (Join-Path $Run 'verified-current-first-fire.ddsave'))) 'Current strict replay changed the genuine first-fire checkpoint.'
    $tear=$null;$recovered=$null;$suppressedTurns=0;$expiredObserved=$false
    for($step=0;$step-lt65;$step++){
        $state=Capture;$party=$session.View('Player')
        if($null-ne$tear){
            Require ($state.FerryWraith.SealDestroyed-and$state.FerryWraith.Rupture.ExpiresAt.Equals($tear.ExpiresAt)) 'Seal destruction or original endpoint changed.'
            if($state.RuleClock.CompareTo($tear.ExpiresAt)-lt0){Require ($state.FerryWraith.ClawSuppressed) 'Suppression expired early.'}
            else {Require (!$state.FerryWraith.ClawSuppressed) 'Suppression survived its original deadline.';$expiredObserved=$true}
            $recovered=@($state.MeleeAttacks|Where-Object {$_.AttackerId-eq'TEST_ONLY.ferry-wraith'-and$_.Revision-gt$tear.Revision})|Select-Object -First 1
            if($null-ne$recovered){Require ($expiredObserved) 'Claw occurred while suppressed.';break}
        }
        if($party.NextSeat-eq'FerryOpponent'){
            $decision=$session.ObserveFerryDecision('FerryOpponent')
            if($state.FerryWraith.ClawSuppressed){
                # CanAttack describes bodily/Action capacity; SourceAvailable independently gates the Claw.
                $intent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($decision)
                $offers=@($session.DiscoverCastingCommands('FerryOpponent','TEST_ONLY.ferry-wraith')|Where-Object {$_.Command.Kind-eq'AttackCreatureFeature'})
                Require (!$decision.SourceAvailable-and$intent.Kind-ne'Attack'-and$offers.Count-eq0) 'Controller selected or discovered a suppressed source.'
                $suppressedTurns++
            }
            $result=$session.AdvanceAutomaticDefender()
            $report.commands+=@{mode='actual-public-auto';step=$step;revision=$state.Revision;clock=$state.RuleClock;decision=$decision;response=$result}
        } elseif($party.NextSeat-eq'Player'){
            $actor=$state.Encounter.CurrentActor
            Require (@($state.Lives|Where-Object {$_.ActorId-eq$actor-and!$_.Dead}).Count-eq1) 'Party died before recovered Claw.'
            $guarded=@($state.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$state.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($state,$_.Revision)}).Count-gt0
            $candidate=[Decennium.Foundation.Command]::new("ferry.seal.tear.$step",$actor,$state.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
            $query=$session.QueryCastingCommand('Player',$candidate)
            if($null-eq$tear-and$guarded-and$query.Admissible){
                $seen=$session.ObserveExposedSeal('Player',$actor);Require ($null-ne$seen-and!$seen.Torn) 'Physical seal was not observed.'
                $seen|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'seen-physical-seal.json') -Encoding utf8
                $unchanged=Bytes
                $session.SetSeatEnabled('Player',$false)
                Require ($null-eq$session.ObserveExposedSeal('Player',$actor)-and$session.Submit('Player',$candidate).Response-eq'NotAuthorized') 'Revoked party retained seal authority.'
                $session.SetSeatEnabled('Player',$true)
                Require ($unchanged-ceq(Bytes)) 'Authority probes mutated state.'
                $result=$session.Submit('Player',$candidate)
                Require ($result.Response-eq'Committed') 'Actual paid tear failed.'
                $after=Capture;$tear=$after.FerryWraith.Rupture
                Require ($null-ne$tear-and$after.RuleClock.Equals($state.RuleClock)-and$after.RandomState-eq$state.RandomState) 'Tear changed clock/RNG or omitted provenance.'
                Require (($after.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent) 'Tear did not spend the existing scheduled Action.'
                $unchanged=Bytes
                Require ($session.Submit('Player',$candidate).Response-eq'Duplicate') 'Repeated source command was not idempotent.'
                $second=[Decennium.Foundation.Command]::new("ferry.seal.second.$step",$actor,$after.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
                Require ($session.Submit('Player',$second).Response-ne'Committed'-and$unchanged-ceq(Bytes)) 'Second tear changed destruction, timer or state.'
                $session.Save((Join-Path $Run 'suppressed.ddsave'));$session.Restore((Join-Path $Run 'suppressed.ddsave'))
                $session.Save((Join-Path $Run 'suppressed-restored.ddsave'))
                Require ((Digest (Join-Path $Run 'suppressed.ddsave'))-ceq(Digest (Join-Path $Run 'suppressed-restored.ddsave'))) 'Suppressed save failed verified identical restore.'
                $report.rupture=$tear;$report.checks+='Paid tear preserved clock/RNG, spent actual Action, retained destruction/deadline through strict restore, and rejected revoked/second requests without mutation'
                $command=$candidate
            } else {
                if(!$guarded){
                    $combat=[Decennium.Foundation.CombatRequest]::new($state.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
                    $command=[Decennium.Foundation.Command]::new("ferry.seal.guard.$step",$actor,$state.Revision,'SelectCombatStance','',0,0,$null,$combat)
                } else {$command=[Decennium.Foundation.Command]::new("ferry.seal.end.$step",$actor,$state.Revision,'EndRegularTurn',$state.Encounter.CurrentTurnId)}
                $result=$session.Submit('Player',$command)
            }
            $report.commands+=@{mode='actual-party-command';step=$step;command=$command;tearQuery=$query;response=$result}
        } else {throw "Unexpected seal continuation seat: $($party.NextSeat)"}
        Require ($result.Response-eq'Committed') "Seal continuation failed at step $step`: $($result|ConvertTo-Json -Compress)"
    }
    Require ($null-ne$tear-and$suppressedTurns-gt0-and$null-ne$recovered) 'Did not reach paid tear, an actual suppressed creature turn and recovered Claw.'
    $final=Capture
    Require ($recovered.WeaponId-eq'TEST_ONLY.ferry-wraith.hellfire-claw'-and$recovered.Attack.Modifier-eq3) 'Recovered attack changed its source.'
    $session.Save((Join-Path $Run 'recovered-claw.ddsave'));$session.Restore((Join-Path $Run 'recovered-claw.ddsave'))
    $session.Save((Join-Path $Run 'recovered-claw-restored.ddsave'))
    Require ((Digest (Join-Path $Run 'recovered-claw.ddsave'))-ceq(Digest (Join-Path $Run 'recovered-claw-restored.ddsave'))) 'Recovered Claw failed verified identical restore.'
    $report.checks+='Actual suppressed creature turn could not use Claw; ordinary End advancement reached original expiry and a genuine source Claw returned with identical verified save/restore'
    $report.recoveredAttack=$recovered;$report.suppressedControllerSteps=$suppressedTurns;$report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock
    $report.status='PASS_GENUINE_SEAL_SUPPRESSION_RECOVERED_CLAW_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
