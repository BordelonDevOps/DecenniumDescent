param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$AttackReadySave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$AttackReadySave=(Resolve-Path -LiteralPath $AttackReadySave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh privacy-pair directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Json($value){ConvertTo-Json -InputObject $value -Depth 100 -Compress -EnumsAsStrings}
$report=[ordered]@{status='FAIL';scope='Detached mechanical private-state equivalence through the existing public read interfaces; no copied state is executed, restored, saved as a supported snapshot or adopted by the live session';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();pairs=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryPrivacyPairs.executed.ps1')
    Copy-Item -LiteralPath $AttackReadySave -Destination (Join-Path $Run 'original-attack-ready.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$AttackReadySave;sha256=(Digest $AttackReadySave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($AttackReadySave)
    $flags=[Reflection.BindingFlags]'Instance,NonPublic'
    $simField=$session.GetType().GetField('simulation',$flags);$policyField=$session.GetType().GetField('policy',$flags)
    $ferryField=$session.GetType().GetField('ferryController',$flags)
    $simulation=$simField.GetValue($session);$policy=$policyField.GetValue($session);$state=$simulation.Capture()
    $stateField=$simulation.GetType().GetField('state',$flags)
    $grant=[Decennium.Foundation.Laboratory.FerryWraithController]::CreatureAuthority()
    $session.Save((Join-Path $Run 'verified-attack-ready.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-attack-ready.ddsave'))-ceq$report.input.sha256) 'Genuine privacy baseline failed strict restore.'
    function CloneObject($value){$value.GetType().GetMethod('MemberwiseClone',$flags).Invoke($value,[object[]]@())}
    function ReadPair($copy,$label){
        # Test-only throwaway readers reuse the real source policy. Reflection changes only
        # their detached input, never the live session; no mutation/Execute API is called.
        $readerSimulation=CloneObject $simulation;$stateField.SetValue($readerSimulation,$copy)
        $reader=CloneObject $session;$simField.SetValue($reader,$readerSimulation)
        $controller=[Decennium.Foundation.Laboratory.FerryWraithController]::new($readerSimulation,$policy)
        $ferryField.SetValue($reader,$controller)
        $folder=(New-Item -ItemType Directory -Path (Join-Path $Run $label)).FullName
        $before=Json ($readerSimulation.Capture())
        $before|Set-Content -LiteralPath (Join-Path $folder 'detached-snapshot-before.json') -Encoding utf8 -NoNewline
        $decision=$controller.Plan($grant)
        $view=$reader.View('FerryOpponent')
        $publicDecision=$reader.ObserveFerryDecision('FerryOpponent')
        $discovery=@($reader.DiscoverCastingCommands('FerryOpponent','TEST_ONLY.ferry-wraith'))
        $query=$reader.QueryCastingCommand('FerryOpponent',$decision.Primary)
        Require ($decision.Intent.Kind-eq'Attack'-and$query.Admissible) 'Private pair changed actual attack eligibility.'
        $data=[ordered]@{controllerView=$decision.View;publicControllerView=$publicDecision;intent=$decision.Intent;command=$decision.Primary;seatView=$view;orderedDiscovery=$discovery;primaryQuery=$query;unauthorizedControllerView=$reader.ObserveFerryDecision('Player')}
        $data|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $folder 'public-reads.json') -Encoding utf8
        # Repeat every public read; none may consume random words or alter any copied input.
        $repeat=[ordered]@{controllerView=$controller.Plan($grant).View;publicControllerView=$reader.ObserveFerryDecision('FerryOpponent');intent=$controller.Plan($grant).Intent;command=$controller.Plan($grant).Primary;seatView=$reader.View('FerryOpponent');orderedDiscovery=@($reader.DiscoverCastingCommands('FerryOpponent','TEST_ONLY.ferry-wraith'));primaryQuery=$reader.QueryCastingCommand('FerryOpponent',$decision.Primary);unauthorizedControllerView=$reader.ObserveFerryDecision('Player')}
        Require ((Json $data)-ceq(Json $repeat)) 'Repeated public observation changed.'
        $after=Json ($readerSimulation.Capture())
        Require ($before-ceq$after) 'Read interface changed detached state/RNG.'
        $after|Set-Content -LiteralPath (Join-Path $folder 'detached-snapshot-after.json') -Encoding utf8 -NoNewline
        return @{public=(Json $data);folder=$folder;decision=$decision;discoveryCount=$discovery.Count;inputSha256=(Digest (Join-Path $folder 'detached-snapshot-before.json'))}
    }
    $baseline=ReadPair ($state.Copy()) 'baseline'
    $hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion';$ferry='TEST_ONLY.ferry-wraith';$buyer='TEST_ONLY.haven-copper-buyer'
    foreach($variant in 'future-rng','enemy-HP','enemy-AC','enemy-injury','enemy-RP','hidden-occupancy'){
        $copy=$state.Copy();$change=@{}
        switch($variant){
            'future-rng'{$change=@{before=$copy.RandomState;after=1234567};$copy.RandomState=1234567}
            'enemy-HP'{
                $prior=$copy.Lives|Where-Object ActorId -eq $hero;$change=@{actor=$hero;before=$prior.Hp;after=1}
                $copy.Lives=[Decennium.Foundation.ActorLifeRecord[]]@($copy.Lives|ForEach-Object{if($_.ActorId-eq$hero){[Decennium.Foundation.ActorLifeRecord]::new($_.ActorId,$_.MaximumHp,1,$_.TemporaryHp,$_.LinkedInjuries,$_.Stable,$_.Dead,$_.UsesDeathSaves,$_.DeathSuccesses,$_.DeathFailures,$_.StableUntil,$_.LastDeathTurn,$_.Prone,$_.HeldItems)}else{$_}})
            }
            'enemy-AC'{
                $prior=$copy.Characters|Where-Object ActorId -eq $hero;$change=@{actor=$hero;beforeDexterity=$prior.Abilities[1];afterDexterity=18}
                $copy.Characters=[Decennium.Foundation.ActorCharacterRecord[]]@($copy.Characters|ForEach-Object{if($_.ActorId-eq$hero){$scores=[int[]]@($_.Abilities);$scores[1]=18;[Decennium.Foundation.ActorCharacterRecord]::new($_.ActorId,$_.ProfileId,$scores,$_.Levels)}else{$_}})
            }
            'enemy-injury'{
                $prior=$copy.Lives|Where-Object ActorId -eq $hero;$change=@{actor=$hero;before=@($prior.LinkedInjuries);after=@(1)}
                $copy.Lives=[Decennium.Foundation.ActorLifeRecord[]]@($copy.Lives|ForEach-Object{if($_.ActorId-eq$hero){[Decennium.Foundation.ActorLifeRecord]::new($_.ActorId,$_.MaximumHp,$_.Hp,$_.TemporaryHp,[int[]]@(1),$_.Stable,$_.Dead,$_.UsesDeathSaves,$_.DeathSuccesses,$_.DeathFailures,$_.StableUntil,$_.LastDeathTurn,$_.Prone,$_.HeldItems)}else{$_}})
            }
            'enemy-RP'{
                $prior=$copy.ResonancePools|Where-Object ActorId -eq $comp;$change=@{actor=$comp;before=$prior.Current;after=$prior.Current-1}
                $copy.ResonancePools=@($copy.ResonancePools|ForEach-Object{if($_.ActorId-eq$comp){$_.Pay(1)}else{$_}})
            }
            'hidden-occupancy'{
                Require (![Decennium.Foundation.Laboratory.ObservationRules]::CanSee($state,$ferry,$buyer)) 'Occupancy pair needs an actually unseen actor.'
                $prior=$copy.Actors|Where-Object Id -eq $buyer;$change=@{actor=$buyer;before=@($prior.X,$prior.Y);after=@(1,4)}
                $copy.Actors=[Decennium.Foundation.ActorState[]]@($copy.Actors|ForEach-Object{if($_.Id-eq$buyer){$moved=$_.Copy();$moved.X=1;$moved.Y=4;$moved}else{$_}})
                Require (![Decennium.Foundation.Laboratory.ObservationRules]::CanSee($copy,$ferry,$buyer)) 'Changed occupancy became observable.'
            }
        }
        $pair=ReadPair $copy $variant
        Require ($pair.public-ceq$baseline.public) "Hidden facts changed permitted Ferry public behavior: $variant"
        $report.pairs+=@{variant=$variant;changedPrivateFacts=$change;permittedSeat='FerryOpponent';publicReadsSha256=(Digest (Join-Path $pair.folder 'public-reads.json'));detachedInputSha256=$pair.inputSha256;orderedDiscoveryCount=$pair.discoveryCount;unchanged=$true}
    }
    $session.Save((Join-Path $Run 'live-after-all-pairs.ddsave'))
    Require ((Digest (Join-Path $Run 'live-after-all-pairs.ddsave'))-ceq$report.input.sha256) 'Private-pair harness changed the actual live session.'
    $report.baselinePublicReadsSha256=Digest (Join-Path $baseline.folder 'public-reads.json')
    $report.status='PASS_SIX_DETACHED_PRIVATE_STATE_INTERFACE_PAIRS'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
