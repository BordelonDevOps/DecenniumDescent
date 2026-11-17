param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$PrefixTrace,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$PrefixTrace=(Resolve-Path -LiteralPath $PrefixTrace).Path
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$launcher=Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'
if(Test-Path -LiteralPath $Run){throw 'Use a fresh adapter probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($test,$message){if(!$test){throw $message}}
$report=[ordered]@{status='FAIL';scope='Actual inherited defender console adapters on a fresh Ferry prefix; no module acceptance';assemblies=@();probes=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.launcher=@{path=$launcher;sha256=(Digest $launcher)};$report.input=@{path=$PrefixTrace;sha256=(Digest $PrefixTrace)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryInheritedAdapters.executed.ps1')
    Copy-Item -LiteralPath $launcher -Destination (Join-Path $Run 'Open-ConnectedExpedition.executed.ps1')
    Copy-Item -LiteralPath $PrefixTrace -Destination (Join-Path $Run 'source-inputs.jsonl')
    foreach($part in 'Core','Persistence','LabModel'){$report.assemblies+=@{name=$part;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll"))}}
    $empty=Join-Path $Run 'empty.jsonl';[IO.File]::WriteAllText($empty,'')
    . $launcher -FerryWraith -AssemblyRoot $AssemblyRoot -InputPath $empty
    $simulationField=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $controllerField=$session.GetType().GetField('defender',[Reflection.BindingFlags]'Instance,NonPublic')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$simulationField.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Request($value) {
        $line=ConvertTo-Json -InputObject $value -Depth 16 -Compress
        Add-Content -LiteralPath (Join-Path $Run 'executed-inputs.jsonl') -Value $line -Encoding utf8
        $result=Write-SessionResponse $line
        Add-Content -LiteralPath (Join-Path $Run 'responses.jsonl') -Value $result -Encoding utf8
        return $result|ConvertFrom-Json -AsHashtable
    }
    function Commit($value) {$revision=(Capture).Revision;$result=Request $value;Require ($result.Response-eq'Committed'-and$result.Revision-eq$revision+1) "Console command failed: $($value.op)/$($value.kind)/$($result|ConvertTo-Json -Compress)"}
    function Pure($value,$expected) {$before=Bytes;$result=Request $value;Require ($result.Response-eq$expected-and$before-ceq(Bytes)) "Adapter rejection/retry differs: $($result|ConvertTo-Json -Compress)";$report.probes+=@{request=$value;response=$result}}
    function Mark($name) {
        $a=Join-Path $Run ($name+'.ddsave');$b=Join-Path $Run ($name+'-restored.ddsave')
        $saved=Request @{op='save';path=$a};Require ($saved.Response-eq'Saved') 'Console save failed.'
        $restored=Request @{op='load';path=$a};Require ($restored.Response-eq'Restored') 'Console restore failed.'
        $saved=Request @{op='save';path=$b};Require ($saved.Response-eq'Saved'-and(Digest $a)-ceq(Digest $b)) 'Console strict restore changed bytes.'
    }
    $inputs=@(Get-Content -LiteralPath $PrefixTrace|ForEach-Object {ConvertFrom-Json -AsHashtable $_})
    foreach($request in $inputs){if($request.op-eq'save'){continue};if($request.revision-ge131){break};Commit $request}
    $s=Capture;Require ($s.Revision-eq131-and$s.Encounter.CurrentActor-eq'TEST_ONLY.companion') 'Unexpected actual adapter prefix.'
    $presence=@($inputs|Where-Object {$_.op-eq'defender-presence'-and$_.revision-eq128})
    Require ($presence.Count-eq1) 'Prefix did not use the lawful inherited Presence console adapter.'
    $report.presenceReceipt=$s.Receipts|Where-Object Id -eq $presence[0].id
    Pure $presence[0] 'Duplicate'
    $wrong=$presence[0].Clone();$wrong.actor='TEST_ONLY.ferry-wraith';Pure $wrong 'NotAuthorized'
    $wrong=$presence[0].Clone();$wrong.id='adapter.presence.wrong-context';$wrong.revision=$s.Revision;Pure $wrong 'Unavailable'
    $invalid=@{op='defender-sanctuary';id='adapter.sanctuary.wrong-context';actor='TEST_ONLY.later-defender';revision=$s.Revision;kind='RespondSanctuary';target='TEST_ONLY.no-pending';x=0;y=0;sanctuaryResponse=@{kind='Forgo';targetId=''}}
    Pure $invalid 'Unavailable';$wrong=$invalid.Clone();$wrong.actor='TEST_ONLY.ferry-wraith';Pure $wrong 'NotAuthorized'
    Mark 'actual-prefix'
    $s=Capture
    $cast=@{op='query';seat='Player';id='adapter.sanctuary.cast';actor='TEST_ONLY.companion';revision=$s.Revision;kind='CastKnownSpell';target='TEST_ONLY.companion';x=0;y=0;
        spellCast=@{spellId='sanctuary';focusItemId=[Decennium.Foundation.SpellCastingProfile]::FocusId;willingTarget=$true;electFocusedDc=$false}}
    $before=Bytes;$query=Request $cast;$report.castQuery=$query
    Require ($query.Admissible-and$before-ceq(Bytes)) ('Actual Sanctuary unavailable: '+($query|ConvertTo-Json -Compress))
    $cast.op='submit';Commit $cast;Mark 'actual-sanctuary'
    $handled=$false
    for($i=0;$i-lt24;$i++) {
        $s=Capture
        # Read the existing trusted NPC controller's public plan; do not dispatch it
        # privately or infer a player command from hidden state.
        $before=Bytes;$plan=$controllerField.GetValue($session).Plan([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority())
        Require ($before-ceq(Bytes)) 'Reading the trusted defender plan changed state.'
        if($plan.View.Slot-eq'Sanctuary') {
            $report.pendingPlan=$plan;$command=$plan.Primary
            Require ($command.Kind-eq'RespondSanctuary'-and$command.Actor-eq'TEST_ONLY.later-defender') 'Wrong trusted pending owner.'
            Mark 'actual-pending-sanctuary'
            $answer=@{op='defender-sanctuary';id=$command.Id;actor=$command.Actor;revision=$command.ExpectedRevision;kind='RespondSanctuary';target=$command.Target;x=$command.X;y=$command.Y;
                sanctuaryResponse=@{kind=$command.SanctuaryResponse.Kind.ToString();targetId=$command.SanctuaryResponse.TargetId}}
            $wrong=$answer.Clone();$wrong.actor='TEST_ONLY.ferry-wraith';Pure $wrong 'NotAuthorized'
            Commit $answer;Pure $answer 'Duplicate';$wrong=$answer.Clone();$wrong.id='adapter.sanctuary.finished-context';$wrong.revision=(Capture).Revision;Pure $wrong 'Unavailable'
            Mark 'actual-sanctuary-response';$report.responseReceipt=(Capture).Receipts|Where-Object Id -eq $answer.id;$handled=$true;break
        }
        $view=$session.View('Player')
        if($view.NextSeat-eq'AutomaticDefender'){Commit @{op='auto'};continue}
        Require ($view.NextSeat-eq'Player') 'Unexpected continuation seat.'
        $actor=$view.ActingActorId
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded){Commit @{op='submit';seat='Player';id='adapter.guard.'+$s.Revision;actor=$actor;revision=$s.Revision;kind='SelectCombatStance';target='';x=0;y=0;combat=@{turn=$view.TurnId;weapon='';stance=1;knockout='OrdinaryOutcome';choice=$false;press='ArmOrReplace';feature=''}}}
        else{Commit @{op='submit';seat='Player';id='adapter.end.'+$s.Revision;actor=$actor;revision=$s.Revision;kind='EndRegularTurn';target=$view.TurnId;x=0;y=0}}
    }
    Require $handled 'No actual failed Sanctuary admission reached the inherited response adapter.'
    $s=Capture;$report.finalRevision=$s.Revision;$report.finalClock=$s.RuleClock;$report.finalRandom=$s.RandomState
    Require ((Digest $launcher)-ceq$report.launcher.sha256) 'Host changed during adapter qualification.'
    $report.status='PASS_ACTUAL_INHERITED_PRESENCE_AND_SANCTUARY_ADAPTERS'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 50|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
