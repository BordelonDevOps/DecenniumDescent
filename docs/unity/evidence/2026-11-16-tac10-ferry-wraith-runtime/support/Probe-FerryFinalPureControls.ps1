param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$PrivacySave,
    [Parameter(Mandatory)][string]$LegacyRoot,[Parameter(Mandatory)][string]$Wire113Root,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
$PrivacySave=(Resolve-Path -LiteralPath $PrivacySave).Path
$LegacyRoot=(Resolve-Path -LiteralPath $LegacyRoot).Path
$Wire113Root=(Resolve-Path -LiteralPath $Wire113Root).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh control directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Json($value){ConvertTo-Json -InputObject $value -Depth 60 -Compress -EnumsAsStrings}
$report=[ordered]@{status='FAIL';scope='Actual nonmutating public denials and authentic old-profile restore rejection; detached mechanical privacy pairs are not adopted gameplay states';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();probes=@();oldProfileRejections=@();privacyPairs=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){
        $dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll
        $report.assemblies+=@{name=$part;sha256=(Digest $dll)}
    }
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryFinalPureControls.executed.ps1')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $FirstFireSave -Destination (Join-Path $Run 'original-first-fire.ddsave')
    $report.input=@{path=$FirstFireSave;sha256=(Digest $FirstFireSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($FirstFireSave)
    $simulationField=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $policyField=$session.GetType().GetField('policy',[Reflection.BindingFlags]'Instance,NonPublic')
    $policy=$policyField.GetValue($session)
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$simulationField.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Command($values){
        $values.kind=[Decennium.Foundation.CommandKind]$values.kind
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $arguments=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($arguments)
    }
    $state=Capture;$before=Bytes
    Require ($state.Revision-eq351-and$null-ne$state.FerryWraith.Admission) 'Expected genuine first-fire checkpoint.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Input restore changed bytes.'
    $hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion';$ferry='TEST_ONLY.ferry-wraith'
    $requests=@(
        @{label='creature-invocation-not-owned';seat='FerryOpponent';values=@{actor=$ferry;kind='UseDivineInvocation';target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($ferry))}},
        @{label='hero-invocation-not-owned';seat='Player';values=@{actor=$hero;kind='UseDivineInvocation';target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@($hero))}},
        @{label='unsourced-generic-PB-bleeding-condition';seat='FerryOpponent';values=@{actor=$ferry;kind='DispatchConditionEvent';target='unsupported.generic-affected-PB.bleeding'}},
        @{label='unsourced-generic-PB-bleeding-periodic';seat='FerryOpponent';values=@{actor=$ferry;kind='DispatchFixturePeriodicRider';target='unsupported.generic-affected-PB.bleeding'}},
        @{label='unsourced-creature-harvest';seat='Player';values=@{actor=$companion;kind='StartHarvest';target=$ferry}},
        @{label='general-seal-interaction-unsupported';seat='Player';values=@{actor=$hero;kind='Interact';target='TEST_ONLY.ferry-seal'}}
    )
    foreach($request in $requests){
        $request.values.id='ferry.final.'+$request.label;$request.values.revision=$state.Revision
        $command=Command $request.values
        $query=$session.QueryCastingCommand($request.seat,$command);$response=$session.Submit($request.seat,$command)
        Require (!$query.Admissible-and$response.Response-ne'Committed'-and$before-ceq(Bytes)) "Unsupported/nonowned request mutated: $($request.label)"
        $report.probes+=@{label=$request.label;command=$command;query=$query;response=$response;unchanged=$true}
    }
    # These copies test a public pure projector. They are never encoded, restored, executed or adopted.
    Copy-Item -LiteralPath $PrivacySave -Destination (Join-Path $Run 'original-privacy-input.ddsave')
    $report.privacyInput=@{path=$PrivacySave;sha256=(Digest $PrivacySave)}
    $session.Restore($PrivacySave);$privacyState=Capture
    $session.Save((Join-Path $Run 'verified-privacy-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-privacy-input.ddsave'))-ceq$report.privacyInput.sha256) 'Privacy baseline restore changed bytes.'
    $grant=[Decennium.Foundation.Laboratory.FerryWraithController]::CreatureAuthority()
    $baseView=$policy.ObserveFerryController($privacyState,$grant)
    $baseIntent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($baseView)
    Require ($baseIntent.Kind-eq'Attack'-and$baseIntent.TargetId-eq$hero) 'Private-state pairs require an actual nontrivial attack decision.'
    Json $baseView|Set-Content -LiteralPath (Join-Path $Run 'controller-base-view.json') -Encoding utf8 -NoNewline
    Json $baseIntent|Set-Content -LiteralPath (Join-Path $Run 'controller-base-intent.json') -Encoding utf8 -NoNewline
    foreach($variant in 'future-rng','enemy-HP','enemy-AC-and-class-facts'){
        $copy=$privacyState.Copy()
        if($variant-eq'future-rng'){$copy.RandomState=1234567}
        elseif($variant-eq'enemy-HP'){
            $copy.Lives=[Decennium.Foundation.ActorLifeRecord[]]@($copy.Lives|ForEach-Object{
                if($_.ActorId-eq$hero){[Decennium.Foundation.ActorLifeRecord]::new($_.ActorId,$_.MaximumHp,1,$_.TemporaryHp,$_.LinkedInjuries,$_.Stable,$_.Dead,$_.UsesDeathSaves,$_.DeathSuccesses,$_.DeathFailures,$_.StableUntil,$_.LastDeathTurn,$_.Prone,$_.HeldItems)}else{$_}
            })
        }else{
            $copy.Characters=[Decennium.Foundation.ActorCharacterRecord[]]@($copy.Characters|ForEach-Object{
                if($_.ActorId-eq$hero){$scores=[int[]]@($_.Abilities);$scores[0]=18;$scores[1]=18;[Decennium.Foundation.ActorCharacterRecord]::new($_.ActorId,$_.ProfileId,$scores,$_.Levels)}else{$_}
            })
        }
        $view=$policy.ObserveFerryController($copy,$grant);$intent=[Decennium.Foundation.Laboratory.FerryDecisionPolicy]::Select($view)
        Require ((Json $view)-ceq(Json $baseView)-and(Json $intent)-ceq(Json $baseIntent)) "Private-state pair changed public controller selection: $variant"
        Json $view|Set-Content -LiteralPath (Join-Path $Run "$variant.view.json") -Encoding utf8 -NoNewline
        Json $intent|Set-Content -LiteralPath (Join-Path $Run "$variant.intent.json") -Encoding utf8 -NoNewline
        $report.privacyPairs+=@{variant=$variant;viewSha256=(Digest (Join-Path $Run "$variant.view.json"));intentSha256=(Digest (Join-Path $Run "$variant.intent.json"));detachedOnly=$true}
    }
    $session.Save((Join-Path $Run 'after-privacy-probes.ddsave'))
    Require ((Digest (Join-Path $Run 'after-privacy-probes.ddsave'))-ceq$report.privacyInput.sha256) 'Detached privacy controls mutated the live session.'
    $session.Restore($FirstFireSave)
    Require ($before-ceq(Bytes)) 'Restoring the genuine first-fire checkpoint changed bytes.'
    $old=[Collections.Generic.List[object]]::new()
    $legacy=Get-Content -LiteralPath (Join-Path $LegacyRoot 'compatibility95-110/results.json') -Raw|ConvertFrom-Json
    foreach($case in $legacy.Cases){
        $old.Add(@{wire=$case.Wire;path=(Join-Path $repository ('docs/unity/evidence/'+$case.Source));sha256=$case.SourceSha256})
        $old.Add(@{wire=$case.Wire;path=(Join-Path $repository ('docs/unity/evidence/'+$case.Earlier));sha256=$case.EarlierSha256})
    }
    foreach($wire in 111,112,113){
        $sourceRoot=if($wire-eq113){Join-Path $Wire113Root 'sources'}else{Join-Path $LegacyRoot "wire$wire/sources"}
        $marks=Get-Content -LiteralPath (Join-Path $sourceRoot 'marks.json') -Raw|ConvertFrom-Json
        foreach($mark in $marks){$old.Add(@{wire=$wire;path=(Join-Path $sourceRoot $mark.name);sha256=$mark.sha256})}
    }
    Require ($old.Count-eq113) 'Expected both endpoints of28 old cases plus13/21/23 authentic later checkpoints.'
    foreach($source in $old){
        Require ((Digest $source.path)-ceq$source.sha256) 'Authentic old checkpoint changed.'
        $rejected=$false;$reason=''
        try{$session.Restore($source.path)}catch{$rejected=$true;$reason=$_.Exception.GetBaseException().Message}
        Require ($rejected-and$before-ceq(Bytes)) 'Old-profile restore was accepted or mutated the Ferry session.'
        $report.oldProfileRejections+=@{wire=$source.wire;path=$source.path;sha256=$source.sha256;reason=$reason;unchanged=$true}
    }
    $session.Save((Join-Path $Run 'after-all-probes.ddsave'))
    Require ((Digest (Join-Path $Run 'after-all-probes.ddsave'))-ceq$report.input.sha256) 'Final probe save changed.'
    $report.status='PASS_FINAL_PURE_CONTROLS_ONLY'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
