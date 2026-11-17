param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ReplaySave,[Parameter(Mandatory)][string]$ReceiptSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ReplaySave=(Resolve-Path -LiteralPath $ReplaySave).Path
$ReceiptSave=(Resolve-Path -LiteralPath $ReceiptSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh creature-knockout branch.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Json($value){ConvertTo-Json -InputObject $value -Depth 60 -Compress -EnumsAsStrings}
$report=[ordered]@{status='FAIL';scope='Genuine public party knockout of source creature; actual denied closure and next creature Start; explicitly detached mechanical shared-life recovery boundaries, not hours of gameplay or adopted saves';startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();commands=@();restorePairs=@();mechanicalRecovery=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryCreatureKnockout.executed.ps1')
    Copy-Item -LiteralPath $ReplaySave -Destination (Join-Path $Run 'original-replay-start.ddsave')
    Copy-Item -LiteralPath $ReceiptSave -Destination (Join-Path $Run 'original-receipt-source.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    $report.replaySource=@{path=$ReplaySave;sha256=(Digest $ReplaySave)};$report.receiptSource=@{path=$ReceiptSave;sha256=(Digest $ReceiptSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($ReplaySave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
    $codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function Checkpoint($name){
        $path=Join-Path $Run "$name.ddsave";$other=Join-Path $Run "$name-restored.ddsave"
        $session.Save($path);$session.Restore($path);$session.Save($other)
        Require ((Digest $path)-ceq(Digest $other)) "Restore changed $name."
        $report.restorePairs+=@{name=$name;sha256=(Digest $path)}
    }
    $hero='TEST_ONLY.actor';$ferry='TEST_ONLY.ferry-wraith';$start=Capture
    Require ($start.Revision-eq366) 'Expected genuine recovered-Claw revision366.'
    $receipts=([Decennium.Foundation.FileSaveStore]::new().Load($ReceiptSave)).Receipts
    foreach($receipt in $receipts|Where-Object {$_.Revision-gt366-and$_.Revision-le436}){
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        $result=if($receipt.Principal-eq'TEST_ONLY.ferry-controller'){$session.AdvanceAutomaticDefender()}else{$session.Submit('Player',$command)}
        Require ($result.Response-eq'Committed'-and$result.Revision-eq$receipt.Revision) 'Genuine receipt prefix failed.'
        $report.commands+=@{receipt=$receipt;command=$command;response=$result}
    }
    Checkpoint 'before-lawful-knockout'
    $state=Capture;$beforeLife=$state.Lives|Where-Object ActorId -eq $ferry
    Require ($state.Revision-eq436-and$state.Encounter.CurrentActor-eq$hero-and!$beforeLife.UsesDeathSaves-and$beforeLife.Hp-gt0-and!$beforeLife.Dead) 'Expected the actual source-creature fatal-hit boundary.'
    $request=[Decennium.Foundation.CombatRequest]::new($state.Encounter.CurrentTurnId,'TEST_ONLY.actor-club',0,'KnockOutIfEligible',$false,'KeepExisting')
    $command=[Decennium.Foundation.Command]::new('ferry.creature-knockout',$hero,$state.Revision,'AttackClub',$ferry,0,0,$null,$request)
    $unchanged=Bytes;$report.query=$session.QueryCastingCommand('Player',$command)
    Require ($report.query.Admissible-and$unchanged-ceq(Bytes)) 'Lawful selected knockout request unavailable.'
    $response=$session.Submit('Player',$command);$report.commands+=@{command=$command;response=$response}
    Require ($response.Response-eq'Committed') 'Actual party knockout failed.'
    $knocked=Capture;$life=$knocked.Lives|Where-Object ActorId -eq $ferry
    $attack=$knocked.MeleeAttacks|Where-Object Revision -eq $knocked.Revision
    Require ($null-ne$attack-and$attack.AttackerId-eq$hero-and$attack.TargetId-eq$ferry-and$attack.Instruction-eq'KnockOutIfEligible'-and$attack.Damage.StableD4-ge1) 'Actual source-creature knockout attack record is missing.'
    Require ($life.Hp-eq0-and$life.Stable-and!$life.Dead-and!$life.UsesDeathSaves-and$null-ne$life.StableUntil) 'Source creature did not enter lawful Stable life.'
    $report.beforeLife=$beforeLife;$report.knockedLife=$life;$report.attack=$attack
    $report.typedDamage=@($knocked.TypedDamage|Where-Object Revision -eq $knocked.Revision)
    $unchanged=Bytes;$report.exactRetry=$session.Submit('Player',$command)
    Require ($report.exactRetry.Response-eq'Duplicate'-and$unchanged-ceq(Bytes)) 'Knockout retry repeated damage or RNG.'
    $close=[Decennium.Foundation.Command]::new('ferry.knockout.invalid-close',$hero,$knocked.Revision,'EndFixedEncounter',$knocked.Encounter.CurrentTurnId)
    $report.deniedClosure=$session.SubmitSessionCommand($close)
    Require ($report.deniedClosure.Response-ne'Committed'-and$unchanged-ceq(Bytes)) 'Stable creature improperly satisfied Dead-only closure.'
    Checkpoint 'actual-stable-creature'
    $end=[Decennium.Foundation.Command]::new('ferry.knockout.next-start',$hero,$knocked.Revision,'EndRegularTurn',$knocked.Encounter.CurrentTurnId)
    $response=$session.Submit('Player',$end);$report.commands+=@{command=$end;response=$response}
    Require ($response.Response-eq'Committed') 'Actual next Start failed.'
    $next=Capture;$nextLife=$next.Lives|Where-Object ActorId -eq $ferry
    Require ($next.Encounter.CurrentActor-eq$ferry-and$nextLife.Stable-and!$nextLife.Dead-and$nextLife.Hp-eq0-and!$nextLife.UsesDeathSaves-and$next.RandomState-eq$knocked.RandomState) 'Creature Start took a death save or recovered early.'
    Checkpoint 'actual-stable-next-start'
    $liveBefore=Bytes;$deadline=$life.StableUntil
    $recover=[Decennium.Foundation.Laboratory.ActorLifeRules].GetMethod('RecoverDue',[Reflection.BindingFlags]'Static,NonPublic')
    foreach($boundary in 'before','at','after'){
        $copy=$next.Copy();$delta=if($boundary-eq'before'){-1}elseif($boundary-eq'after'){1}else{0}
        $copy.RuleClock=[Decennium.Foundation.RuleTime]::new(2*$deadline.Numerator+$delta,2*$deadline.Denominator)
        $events=$copy.LifeEvents.Count;$rng=$copy.RandomState
        $null=$recover.Invoke($null,[object[]]@($copy))
        $after=$copy.Lives|Where-Object ActorId -eq $ferry
        if($boundary-eq'before'){Require ($after.SameAs($nextLife)-and$copy.LifeEvents.Count-eq$events) 'Stable recovery happened before its exact deadline.'}
        else{Require ($after.Hp-eq1-and!$after.Stable-and!$after.Dead-and!$after.UsesDeathSaves-and$copy.LifeEvents.Count-eq($events+1)) 'Shared source-creature recovery failed at/after deadline.'}
        Require ($copy.RandomState-eq$rng) 'Recovery consumed RNG.'
        $once=Json $copy.Lives;$eventCount=$copy.LifeEvents.Count;$null=$recover.Invoke($null,[object[]]@($copy))
        Require ((Json $copy.Lives)-ceq$once-and$copy.LifeEvents.Count-eq$eventCount-and$copy.RandomState-eq$rng) 'Repeated shared recovery duplicated settlement.'
        $report.mechanicalRecovery+=@{boundary=$boundary;clock=$copy.RuleClock;life=$after;newEvents=@($copy.LifeEvents|Select-Object -Skip $events);rngBefore=$rng;rngAfter=$copy.RandomState;detachedOnly=$true}
    }
    Require ($liveBefore-ceq(Bytes)) 'Detached mechanical recovery changed live gameplay.'
    $session.Save((Join-Path $Run 'live-after-mechanical-controls.ddsave'))
    $report.finalRevision=$next.Revision;$report.finalClock=$next.RuleClock
    $report.status='PASS_GENUINE_CREATURE_KNOCKOUT_AND_MECHANICAL_RECOVERY'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
