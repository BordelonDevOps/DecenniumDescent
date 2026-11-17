param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FirstFireSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$FirstFireSave=(Resolve-Path -LiteralPath $FirstFireSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh casting branch directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Genuine alternate first-fire continuation through owned Arcane Ward, Guidance, Detect Magic and Dispel Magic Lesser in the Ferry epoch. Not all-seven ability qualification or module acceptance.';assemblies=@();commands=@();casts=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryCasting.executed.ps1')
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
    function Send($command){
        $result=$session.Submit('Player',$command)
        $report.commands+=@{command=$command;response=$result}
        Require ($result.Response-eq'Committed') "Casting branch rejected $($command.Kind): $($result|ConvertTo-Json -Compress)"
    }
    # Preserve the complete discovered typed payload while giving the command its own ID.
    function CloneCommand($command,$id){
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $values=[object[]]@($ctor.GetParameters()|ForEach-Object {
            if($_.Name-eq'id'){$id}elseif($_.Name-eq'revision'){$command.ExpectedRevision}else{$command.($_.Name)}
        })
        $ctor.Invoke($values)
    }
    $start=Capture;$hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion'
    Require ($start.Revision-eq351-and$start.Encounter.Id-eq[Decennium.Foundation.FerryWraithProfile]::Encounter) 'Expected actual first-fire input.'
    $session.Save((Join-Path $Run 'verified-input.ddsave'))
    Require ((Digest (Join-Path $Run 'verified-input.ddsave'))-ceq$report.input.sha256) 'Current strict restore changed the input.'
    $plan=@('arcane-ward','guidance','detect-magic','dispel-magic-lesser');$next=0;$lastCastTurn='';$endedLast=$false
    for($step=0;$step-lt90;$step++){
        $s=Capture
        Require (@($s.Lives|Where-Object {$_.ActorId-in@($hero,$companion)-and($_.Dead-or$_.Hp-le0)}).Count-eq0) 'Party became unable to complete the real casting branch.'
        if($session.View('Player').NextSeat-eq'FerryOpponent'){
            $result=$session.AdvanceAutomaticDefender();$report.commands+=@{mode='actual-public-auto';beforeRevision=$s.Revision;response=$result}
            Require ($result.Response-eq'Committed') 'Actual automatic creature step failed.'
            continue
        }
        Require ($session.View('Player').NextSeat-eq'Player') 'Unexpected casting branch authority.'
        $actor=$s.Encounter.CurrentActor
        $guarded=@($s.Stances|Where-Object {$_.ActorId-eq$actor-and$_.TurnOrdinal-eq$s.Encounter.TurnOrdinal-and[Decennium.Foundation.EncounterHistory]::InCurrent($s,$_.Revision)}).Count-gt0
        if(!$guarded){
            $combat=[Decennium.Foundation.CombatRequest]::new($s.Encounter.CurrentTurnId,'',[int][Decennium.Foundation.CombatStance]::Guarded)
            Send ([Decennium.Foundation.Command]::new("ferry.casting.guard.$($s.Revision)",$actor,$s.Revision,'SelectCombatStance','',0,0,$null,$combat))
            continue
        }
        $interval=$s.WorldIntervals|Where-Object ActorId -eq $actor
        if($actor-eq$hero-and!$interval.ActionSpent-and!$s.FerryWraith.SealDestroyed){
            $tear=[Decennium.Foundation.Command]::new("ferry.casting.tear.$($s.Revision)",$actor,$s.Revision,'TearExposedSeal','TEST_ONLY.ferry-seal')
            Require ($session.QueryCastingCommand('Player',$tear).Admissible) 'Real defensive seal Action unavailable.'
            Send $tear;continue
        }
        if($actor-eq$companion-and!$interval.ActionSpent-and$next-lt$plan.Count){
            $spell=$plan[$next];$before=Bytes
            $options=@($session.DiscoverCastingCommands('Player',$actor)|Where-Object {$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq$spell})
            $legal=@($options|Where-Object {$_.Query.Admissible-and($spell-eq'dispel-magic-lesser'-or$_.Command.Target-eq$(if($spell-eq'detect-magic'){$companion}else{$hero}))})
            Require ($legal.Count-eq1) "Expected one lawful $spell option: $($options|ConvertTo-Json -Depth 8 -Compress)"
            $command=CloneCommand $legal[0].Command "ferry.casting.$spell.$($s.Revision)"
            Require ($session.QueryCastingCommand('Player',$command).Admissible-and$before-ceq(Bytes)) 'Discovery/query changed state or rejected the same typed payload.'
            Send $command
            $after=Capture;$cast=$after.SpellCasts|Where-Object CommandId -eq $command.Id
            Require ($null-ne$cast-and$cast.Turn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar-and!$cast.Turn.IsCarried) 'Cast did not bind the actual owning Ferry turn.'
            Require (($after.WorldIntervals|Where-Object ActorId -eq $actor).ActionSpent) 'Cast did not pay actual Action.'
            $stable=Bytes
            Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Cast retry repeated payment/effect/RNG.'
            $report.casts+=,$cast;$next++;$lastCastTurn=$s.Encounter.CurrentTurnId
            $session.Save((Join-Path $Run "$spell.ddsave"))
            continue
        }
        $turn=$s.Encounter.CurrentTurnId
        Send ([Decennium.Foundation.Command]::new("ferry.casting.end.$($s.Revision)",$actor,$s.Revision,'EndRegularTurn',$turn))
        if($next-eq$plan.Count-and$actor-eq$companion-and$turn-eq$lastCastTurn){$endedLast=$true;break}
    }
    Require ($next-eq4-and$endedLast) 'Did not execute all four owned spells and the final actual End.'
    $final=Capture
    foreach($cast in $report.casts){
        Require (@($final.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq$cast.Turn.EpochId-and$_.Turn.ActorId-eq$cast.Turn.ActorId-and$_.Turn.LocalStart-eq$cast.Turn.LocalStart}).Count-eq1) 'A real casting End is missing or duplicated.'
    }
    Require (@($final.SpellEffects|Where-Object {$_.Present-and$_.SpellId-eq'guidance'}).Count-eq0-and@($final.SpellEffects|Where-Object {$_.Present-and$_.SpellId-eq'detect-magic'}).Count-eq1) 'Dispel did not selectively end the actually observed own Guidance.'
    Require ($final.BishopEntry.Dispels.Count-eq1-and$final.BishopEntry.Dispels[0].Revision-gt$start.Revision) 'Actual source-bound Dispel record missing.'
    $session.Save((Join-Path $Run 'completed.ddsave'));$session.Restore((Join-Path $Run 'completed.ddsave'));$session.Save((Join-Path $Run 'completed-restored.ddsave'))
    Require ((Digest (Join-Path $Run 'completed.ddsave'))-ceq(Digest (Join-Path $Run 'completed-restored.ddsave'))) 'Completed four-spell branch changed across strict replay/restore.'
    $report.finalRevision=$final.Revision;$report.finalClock=$final.RuleClock;$report.finalRp=$final.ResonancePools;$report.finalStrain=$final.CastingStrain
    $report.dispels=$final.BishopEntry.Dispels;$report.effects=$final.SpellEffects;$report.castingEnds=@($final.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq[Decennium.Foundation.FerryWraithProfile]::Calendar})
    $report.expandedCommands=@($final.Receipts|Where-Object {$_.Revision-gt$start.Revision}|ForEach-Object {@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    Require ($report.expandedCommands.Count-eq$report.commands.Count) 'Saved command witness does not reconcile.'
    $report.status='PASS_GENUINE_FERRY_FOUR_OWNED_SPELLS_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
