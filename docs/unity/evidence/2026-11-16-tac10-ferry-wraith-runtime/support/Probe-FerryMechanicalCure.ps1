param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$EarnedSave,[Parameter(Mandatory)][string]$ApprovedResponseId,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$EarnedSave=(Resolve-Path -LiteralPath $EarnedSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh detached mechanical control directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Raw($value){ConvertTo-Json -InputObject $value -Depth 100 -EnumsAsStrings -Compress}
function Retain($name,$value){Raw $value|Set-Content -LiteralPath (Join-Path $Run $name) -Encoding utf8}
$report=[ordered]@{status='FAIL';scope='Detached mechanical condition/owning-Ferry-epoch intersection through the actual paid Invocation producer; not a genuine condition producer, committed command, supported modified save or receipt';approvedResponseId=$ApprovedResponseId;startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=@();restorePairs=@();cases=@()}
try{
    foreach($part in 'Core','Persistence','LabModel'){$dll=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";Add-Type -Path $dll;$report.assemblies+=@{name=$part;sha256=(Digest $dll)}}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryMechanicalCure.executed.ps1')
    Copy-Item -LiteralPath $EarnedSave -Destination (Join-Path $Run 'genuine-owner-context.ddsave')
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)};$report.input=@{path=$EarnedSave;sha256=(Digest $EarnedSave)}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($EarnedSave);$session.Save((Join-Path $Run 'genuine-owner-context-restored.ddsave'))
    Require ((Digest (Join-Path $Run 'genuine-owner-context-restored.ddsave'))-ceq$report.input.sha256) 'Genuine baseline failed strict canonical restore.'
    $report.restorePairs+=@{name='genuine-owner-context';sha256=$report.input.sha256}
    $flags=[Reflection.BindingFlags]'Instance,NonPublic';$staticFlags=[Reflection.BindingFlags]'Static,NonPublic'
    $field=$session.GetType().GetField('simulation',$flags);$policy=$session.GetType().GetField('policy',$flags).GetValue($session)
    $resolve=$policy.GetType().GetMethod('ResolveDivineInvocation',$flags);$assess=$policy.GetType().GetMethod('AssessDivineInvocation',$flags)
    Require ($null-ne$resolve-and$null-ne$assess) 'Actual shared Invocation producer unavailable.'
    $codec=[Decennium.Foundation.SnapshotCodec]::new();$component=[Decennium.Foundation.ConditionJournalCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function LiveBytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    function CopyGenuine {$codec.Decode([IO.File]::ReadAllBytes($EarnedSave))}
    function Command($id,$actor,$revision,$target){
        $values=@{id=$id;actor=$actor;revision=$revision;kind=[Decennium.Foundation.CommandKind]::UseDivineInvocation;target='';divineInvocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]@('TEST_ONLY.actor','TEST_ONLY.companion'),$target,'Frightened')}
        $ctor=[Decennium.Foundation.Command].GetConstructors()[0]
        $args=[object[]]@($ctor.GetParameters()|ForEach-Object{if($values.ContainsKey($_.Name)){$values[$_.Name]}else{$_.DefaultValue}})
        $ctor.Invoke($args)
    }
    function JournalRoundtrip($label,$journal){
        $first=$component.Encode($journal);$decoded=$component.Decode($first);$second=$component.Encode($decoded)
        Require ([Convert]::ToBase64String($first)-ceq[Convert]::ToBase64String($second)) 'Selected condition component codec changed bytes.'
        [IO.File]::WriteAllBytes((Join-Path $Run "$label.condition-component.bin"),$first)
        return @{file="$label.condition-component.bin";sha256=(Digest (Join-Path $Run "$label.condition-component.bin"));scope='Condition component only; not a supported full snapshot'}
    }
    function RejectFullSnapshot($label,$copy){
        $before=Raw $copy;$stage='encode';$rejection='';$encoded=$false;$decoded=$false;$copyPath=Join-Path $Run "$label.unsupported.ddsave"
        try{$bytes=$codec.Encode($copy);$encoded=$true;[IO.File]::WriteAllBytes($copyPath,$bytes);$stage='decode';$null=$codec.Decode($bytes);$decoded=$true;$stage='strict-restore';$session.Restore($copyPath)}
        catch{$rejection=$_.Exception.GetBaseException().Message}
        Require ($rejection-ne''-and$before-ceq(Raw $copy)-and$liveOriginal-ceq(LiveBytes)) 'Unsupported mechanical snapshot was accepted or changed inputs/live state.'
        return @{stage=$stage;encoded=$encoded;decoded=$decoded;rejection=$rejection;unchanged=$true;scope='Actual rejection stage, without fabricated source-use/timing records'}
    }
    $genuine=Capture;$liveOriginal=LiveBytes;$hero='TEST_ONLY.actor';$comp='TEST_ONLY.companion'
    Require ($genuine.Revision-eq376-and$genuine.InventoryCombat-and$genuine.Encounter.CurrentActor-eq$comp-and$null-ne$genuine.FerryWraith.Admission) 'Expected genuine staged Ferry owner context376.'
    $cureType=[Decennium.Foundation.Laboratory.ConditionHistory].Assembly.GetType('Decennium.Foundation.Laboratory.ConditionCureInvocation')
    $factory=$cureType.GetMethod('ForDivineInvocation',$staticFlags)
    $bishopCodec=[Decennium.Foundation.SnapshotCodec].Assembly.GetType('Decennium.Foundation.BishopEntryCodec')
    $bishopWrite=$bishopCodec.GetMethod('Write',$staticFlags);$bishopRead=$bishopCodec.GetMethod('Read',$staticFlags)
    foreach($target in @($comp,$hero)){
        $label=if($target-eq$comp){'self'}else{'hero'};$copy=CopyGenuine;$originalJournal=$copy.Conditions|Where-Object Target -eq $target
        Require ($originalJournal.Now.Time-lt$copy.RuleClock) 'Expected retained earlier target journal marker; do not rewrite history to create one.'
        $applicationId="TEST_ONLY.mechanical.ferry-cure.$label";$deadline=[Decennium.Foundation.ConditionStamp]::new($copy.RuleClock.AddSeconds(6))
        $relation=[Decennium.Foundation.FrightenedRelationshipData]::new('TEST_ONLY.ferry-wraith',"TEST_ONLY.mechanical.supplied.$label",'TEST_ONLY.mechanical.input.v1')
        $application=[Decennium.Foundation.ConditionApplicationData]::new($applicationId,'TEST_ONLY.mechanical.supplier','TEST_ONLY.mechanical.fear','Frightened',$deadline,'TEST_ONLY.mechanical.deadline',$true,$null,$null,$null,$relation)
        $history=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($originalJournal)
        $transition=$history.Append([Decennium.Foundation.ConditionOperation]::Apply($applicationId,$originalJournal.Now,$application))
        $copy.Conditions=@($copy.Conditions|ForEach-Object{if($_.Target-eq$target){$transition.State.Journal}else{$_}})
        Require (!$transition.ApplicationPrevented-and[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($copy,$target).View().Has('Frightened')) 'Supplied mechanical application is not presently operative.'
        $input=Raw $copy;Retain "$label.mechanical-input.json" $copy
        $beforeComponent=JournalRoundtrip "$label.before" $transition.State.Journal
        $fullRejection=RejectFullSnapshot "$label.before" $copy
        $command=Command "TEST_ONLY.mechanical.invoke.$label" $comp $copy.Revision $target
        $query=$assess.Invoke($policy,[object[]]@($copy,$command))
        Require ([string]::IsNullOrEmpty($query)-and$input-ceq(Raw $copy)) 'Actual producer assessment rejected or mutated the detached input.'
        $negative=@()
        foreach($kind in @('nonowner','wrong-owning-turn')){
            # These separate copies carry no supplied condition and exercise the actual context gates.
            $deniedCopy=CopyGenuine;$deniedActor=if($kind-eq'nonowner'){$hero}else{$comp}
            if($kind-eq'wrong-owning-turn'){$deniedCopy.RuleClock=$deniedCopy.RuleClock.AddSeconds(2)}
            $deniedCommand=Command "TEST_ONLY.mechanical.deny.$label.$kind" $deniedActor $deniedCopy.Revision $target
            $deniedBefore=Raw $deniedCopy;$failure=$resolve.Invoke($policy,[object[]]@($deniedCopy,$deniedCommand))
            Require (![string]::IsNullOrEmpty($failure)-and$deniedBefore-ceq(Raw $deniedCopy)) 'Invalid owner/context executed or mutated.'
            $negative+=@{name=$kind;failure=$failure;unchanged=$true;command=$deniedCommand}
        }
        $randomBefore=$copy.RandomState;$draw=[Decennium.Foundation.DiceStream]::Draw($randomBefore,8)
        $poolBefore=($copy.ResonancePools|Where-Object ActorId -eq $comp).Current;$convictionBefore=$copy.ConvictionBalance.Current
        Require (!($copy.WorldIntervals|Where-Object ActorId -eq $comp).ActionSpent) 'Genuine Action is already spent.'
        $livesBefore=@($copy.Lives|Where-Object ActorId -in @($hero,$comp))
        $receiptBefore=Raw $copy.Receipts;$revisionBefore=$copy.Revision;$clockBefore=$copy.RuleClock
        $failure=$resolve.Invoke($policy,[object[]]@($copy,$command));Require ([string]::IsNullOrEmpty($failure)) "Actual mechanical producer rejected: $failure"
        $use=$copy.BishopEntry.Invocations|Select-Object -Last 1;$afterJournal=$copy.Conditions|Where-Object Target -eq $target
        $afterHistory=[Decennium.Foundation.Laboratory.ConditionHistory]::Restore($afterJournal)
        $ended=$afterHistory.Ledger.Applications|Where-Object Id -eq $applicationId
        Require ($use.CommandId-eq$command.Id-and$use.Turn.EpochId-eq'TEST_ONLY.ferry-calendar'-and$use.RpAfter-eq($use.RpBefore-3)-and$use.ConvictionAfter-eq($use.ConvictionBefore-2)) 'Paid producer identity, epoch or costs differ.'
        Require ($use.RpBefore-eq$poolBefore-and($copy.ResonancePools|Where-Object ActorId -eq $comp).Current-eq($poolBefore-3)-and$use.ConvictionBefore-eq$convictionBefore-and$copy.ConvictionBalance.Current-eq($convictionBefore-2)-and($copy.WorldIntervals|Where-Object ActorId -eq $comp).ActionSpent) 'Actual Action/RP/Conviction state did not pay source costs.'
        Require ($use.Die-eq($draw.Value+1)-and$use.RandomBefore-eq$randomBefore-and$use.RandomAfter-eq$draw.NextState-and$copy.RandomState-eq$draw.NextState-and$use.WordsConsumed-eq$draw.WordsConsumed) 'Shared healing draw differs.'
        foreach($recipient in $use.Recipients){
            $beforeLife=$livesBefore|Where-Object ActorId -eq $recipient.TargetId;$afterLife=$copy.Lives|Where-Object ActorId -eq $recipient.TargetId
            Require ($recipient.HpBefore-eq$beforeLife.Hp-and$recipient.Potential-eq($draw.Value+3)-and$recipient.HpAfter-eq[Math]::Min($beforeLife.MaximumHp,$beforeLife.Hp+$recipient.Potential)-and$afterLife.Hp-eq$recipient.HpAfter) 'Actual shared healing or maximum-HP cap differs.'
        }
        Require ($use.EndedApplicationIds.Count-eq1-and$use.EndedApplicationIds[0]-eq$applicationId-and$use.CureOperationId-eq($command.Id+'.invocation.cure')) 'Qualified cure ended the wrong application.'
        Require ($ended.EndedAt.Time-eq$clockBefore-and!$ended.Present($afterHistory.Ledger.Now)-and$afterJournal.Now.Time-eq$clockBefore) 'Actual cure or target-journal synchronization failed.'
        $retainedApplication=($afterJournal.Operations|Where-Object {$_.Kind-eq'Apply'-and$_.Application.Id-eq$applicationId}).Application
        Require ((Raw $retainedApplication)-ceq(Raw $application)) 'Cure rewrote supplied finite expiry/provenance.'
        $prefix=@($afterJournal.Operations|Select-Object -First $originalJournal.Operations.Count)
        Require ((Raw $prefix)-ceq(Raw @($originalJournal.Operations))) 'Mechanical test rewrote genuine condition history.'
        Require (@($afterJournal.Operations|Where-Object Id -eq ($command.Id+'.invocation.sync')).Count-eq1) 'Actual producer did not synchronize stale journal exactly once.'
        $recharge=$copy.AbilityRecharges|Where-Object {$_.ActorId-eq$comp-and$_.AbilityId-eq'cleric.arch.divine-invocation'}
        Require ($recharge.EpochId-eq'TEST_ONLY.ferry-calendar'-and$recharge.Remaining-eq3-and$recharge.LastLocalStart-eq$use.Turn.LocalStart-and$recharge.LastStartAt-eq$clockBefore) 'Actual producer recharge bound the wrong context.'
        Require ($copy.Revision-eq$revisionBefore-and$copy.RuleClock-eq$clockBefore-and$receiptBefore-ceq(Raw $copy.Receipts)) 'Detached producer fabricated a committed revision/receipt or clock advancement.'
        $post=Raw $copy;$again=$resolve.Invoke($policy,[object[]]@($copy,$command))
        Require (![string]::IsNullOrEmpty($again)-and$post-ceq(Raw $copy)) 'Unavailable repeat paid or applied effects again.'
        # The actual producer already called ForDivineInvocation. Its factory must also reject an unpaid original copy.
        $unpaid=CopyGenuine;$unpaidBefore=Raw $unpaid;$triggerRejection=''
        try{$null=$factory.Invoke($null,[object[]]@($unpaid,$command,$use))}catch{$triggerRejection=$_.Exception.GetBaseException().Message}
        Require ($triggerRejection-ne''-and$unpaidBefore-ceq(Raw $unpaid)) 'Unpaid producer trigger was accepted or mutated.'
        $afterComponent=JournalRoundtrip "$label.after" $afterJournal
        $stream=[IO.MemoryStream]::new();$writer=[IO.BinaryWriter]::new($stream)
        $null=$bishopWrite.Invoke($null,[object[]]@($writer,$copy.BishopEntry));$writer.Flush();$entryBytes=$stream.ToArray();$stream.Position=0
        $reader=[IO.BinaryReader]::new($stream);$entry=$bishopRead.Invoke($null,[object[]]@($reader));Require ($stream.Position-eq$stream.Length) 'Selected Bishop record codec left trailing bytes.'
        $secondStream=[IO.MemoryStream]::new();$secondWriter=[IO.BinaryWriter]::new($secondStream);$null=$bishopWrite.Invoke($null,[object[]]@($secondWriter,$entry));$secondWriter.Flush()
        Require ([Convert]::ToBase64String($entryBytes)-ceq[Convert]::ToBase64String($secondStream.ToArray())) 'Selected Bishop record codec changed bytes.'
        $entryFile=Join-Path $Run "$label.bishop-component.bin";[IO.File]::WriteAllBytes($entryFile,$entryBytes)
        Retain "$label.mechanical-output.json" $copy
        Require ($liveOriginal-ceq(LiveBytes)-and$report.input.sha256-ceq(Digest $EarnedSave)) 'Detached control altered genuine live/input state.'
        $report.cases+=@{name=$label;target=$target;application=$application;originalJournalAt=$originalJournal.Now;currentAt=$clockBefore;command=$command;invocation=$use;recharge=$recharge;selectedConditionBefore=$beforeComponent;selectedConditionAfter=$afterComponent;selectedBishopSha256=(Digest $entryFile);fullSnapshotRejection=$fullRejection;negativeContexts=$negative;unpaidTriggerRejection=$triggerRejection;repeatFailure=$again;unchangedLive=$true;noCommittedReceipt=$true}
    }
    $session.Save((Join-Path $Run 'genuine-live-after-controls.ddsave'))
    Require ((Digest (Join-Path $Run 'genuine-live-after-controls.ddsave'))-ceq$report.input.sha256) 'Genuine live canonical bytes changed.'
    Require ($report.cases.Count-eq2) 'Mechanical recipient controls incomplete.'
    $report.status='PASS_DETACHED_ACTUAL_PRODUCER_CURE_IN_GENUINE_FERRY_OWNER_CONTEXT_NOT_SUPPORTED_GAMEPLAY'
}catch{$report.error=$_.Exception.ToString()}
$report.finishedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 100 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
