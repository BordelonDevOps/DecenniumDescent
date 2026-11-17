param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh forgery evidence directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Independently decoded counterfeit copies of genuine saves; classify codec structural rejection separately from actual strict restore rejection; preserve live state and input bytes';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();cases=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryForgeries.executed.ps1')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function SetFact($object,$name,$value){
        Require ($null-ne$object) "Missing forged object for $name."
        $flags=[Reflection.BindingFlags]'Instance,NonPublic,Public'
        $member=$object.GetType().GetField($name,$flags)
        if($null-eq$member){$member=$object.GetType().GetField("<$name>k__BackingField",$flags)}
        Require ($null-ne$member) "No actual field for $name."
        $member.SetValue($object,[Management.Automation.LanguagePrimitives]::ConvertTo($value,$member.FieldType))
    }
    $art='engine/artifacts/ferry-wraith';$paths="$art/dash-correction/five-paths-20261117T122438Z/TypedUninterrupted"
    $specs=@(
        @{name='seal-unpaid-action';path="$paths/ferry-r354.ddsave";mutation={param($s) SetFact ($s.WorldIntervals|Where-Object ActorId -eq 'TEST_ONLY.companion') 'ActionSpent' $false}},
        @{name='seal-false-action-interval';path="$paths/ferry-r354.ddsave";mutation={param($s) SetFact $s.FerryWraith.Rupture 'ActionInterval' ($s.FerryWraith.Rupture.ActionInterval+3)}},
        @{name='seal-extended-deadline';path="$paths/ferry-r354.ddsave";mutation={param($s) SetFact $s.FerryWraith.Rupture 'ExpiresAt' ($s.FerryWraith.Rupture.ExpiresAt.AddSeconds(6))}},
        @{name='initiative-invented-bonus';path="$paths/ferry-r346.ddsave";mutation={param($s) $draw=$s.FerryWraith.Admission.Draws|Where-Object ActorId -eq 'TEST_ONLY.actor';SetFact $draw 'Bonus' ($draw.Bonus+1)}},
        @{name='admission-carried-action-refund';path="$art/dash-correction/invocation-epoch-20261117T1331Z/after-admission.ddsave";mutation={param($s) $carry=$s.FerryWraith.Admission.PartyCarried|Where-Object {$_.Interval.ActorId-eq'TEST_ONLY.companion'};SetFact $carry.Interval 'ActionSpent' $false;SetFact ($s.WorldIntervals|Where-Object ActorId -eq 'TEST_ONLY.companion') 'ActionSpent' $false}},
        @{name='duplicate-old-casting-end';path="$paths/ferry-r346.ddsave";mutation={param($s) $s.CastingTurnEnds=@($s.CastingTurnEnds)+@($s.CastingTurnEnds[-1])}},
        @{name='early-recharge-tick';path="$art/dash-correction/invocation-epoch-20261117T1331Z/owner-start-1.ddsave";mutation={param($s) $row=$s.AbilityRecharges|Where-Object AbilityId -eq 'cleric.arch.divine-invocation';SetFact $row 'Remaining' ($row.Remaining-1)}},
        @{name='free-life-healing';path="$paths/ferry-r351.ddsave";mutation={param($s) $life=$s.Lives|Where-Object ActorId -eq 'TEST_ONLY.actor';SetFact $life 'Hp' ($life.Hp+1)}},
        @{name='false-zero-damage-history';path="$paths/ferry-r351.ddsave";mutation={param($s) $damage=$s.TypedDamage|Select-Object -Last 1;SetFact $damage 'AfterFlatReduction' 0}},
        @{name='pending-knockout-source-substitution';path="$art/dash-correction/knockout-20261117T112218Z/source-knockout-pending.ddsave";mutation={param($s) $attack=$s.MeleeAttacks|Where-Object Pending|Select-Object -Last 1;SetFact $attack 'WeaponId' 'TEST_ONLY.actor-club'}},
        @{name='pending-sanctuary-source-substitution';path="$art/development/sanctuary-probe-20261117T0953Z/pending-source-claw.ddsave";mutation={param($s) $pending=$s.SanctuaryAdmissions|Where-Object Pending|Select-Object -Last 1;SetFact $pending 'Source' 'RegularMelee'}},
        @{name='reaction-ledger-refund';path="$art/dash-correction/press-20261117T112218Z/source-press-followed.ddsave";mutation={param($s) $interval=$s.WorldIntervals|Where-Object ActorId -eq 'TEST_ONLY.ferry-wraith';SetFact $interval 'ReactionAvailable' (!$interval.ReactionAvailable)}}
    )
    foreach($spec in $specs){
        $folder=(New-Item -ItemType Directory -Path (Join-Path $Run $spec.name)).FullName
        $original=(Resolve-Path -LiteralPath $spec.path).Path;$originalHash=Digest $original
        $session.Restore($original);$liveBefore=Bytes
        Copy-Item -LiteralPath $original -Destination (Join-Path $folder 'genuine.ddsave')
        $session.Save((Join-Path $folder 'genuine-restored.ddsave'))
        Require ((Digest (Join-Path $folder 'genuine-restored.ddsave'))-ceq$originalHash) 'Genuine forge baseline failed canonical restore.'
        # Decode anew: reflection must not alter immutable objects shared by Snapshot.Copy/live state.
        $copy=$codec.Decode([IO.File]::ReadAllBytes($original));& $spec.mutation $copy
        $copy|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $folder 'counterfeit-input.json') -Encoding utf8
        $encoded=$false;$decoded=$false;$rejection='';$stage='encode';$forgedHash='';$forgedPath=Join-Path $folder 'counterfeit.ddsave'
        try{
            $raw=$codec.Encode($copy);$encoded=$true;[IO.File]::WriteAllBytes($forgedPath,$raw);$forgedHash=Digest $forgedPath
            $stage='decode';$null=$codec.Decode($raw);$decoded=$true
            $stage='strict-restore';$session.Restore($forgedPath)
        }catch{$rejection=$_.Exception.GetBaseException().Message}
        Require ($rejection-ne'') "Counterfeit was accepted: $($spec.name)"
        Require ($liveBefore-ceq(Bytes)-and$originalHash-ceq(Digest $original)) "Rejected forgery changed live/original state: $($spec.name)"
        if($encoded){Require ($forgedHash-ceq(Digest $forgedPath)) 'Rejected input was repaired or altered.'}
        $session.Save((Join-Path $folder 'live-after-rejection.ddsave'))
        Require ((Digest (Join-Path $folder 'live-after-rejection.ddsave'))-ceq$originalHash) 'Rejection changed canonical live bytes.'
        $report.cases+=@{name=$spec.name;sourcePath=$original;sourceSha256=$originalHash;encoded=$encoded;decoded=$decoded;rejectionStage=$stage;rejection=$rejection;counterfeitSha256=$forgedHash;unchanged=$true}
    }
    Require ($report.cases.Count-eq12) 'Forgery matrix incomplete.'
    $report.status='PASS_TWELVE_STRUCTURAL_OR_CAUSAL_FORGERY_REJECTIONS'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
