param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string[]]$Branches,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh continuation directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Three real outgoing casting Ends from separately retained successful care branches; prefixes reused, not rerun';startedUtc=[DateTime]::UtcNow.ToString('o');branches=@();assemblies=@()}
try {
    foreach($name in 'Core','Persistence','LabModel'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Continue-FerryCareEnds.executed.ps1')
    foreach($branch in $Branches){
        $branch=(Resolve-Path -LiteralPath $branch).Path
        $prefix=Get-Content -LiteralPath (Join-Path $branch 'RESULT.json') -Raw|ConvertFrom-Json
        Require ($prefix.status-eq"PASS_GENUINE_FERRY_$($prefix.plan.ToUpperInvariant())_ONLY") 'Prefix is not a completed successful care probe.'
        $destination=(New-Item -ItemType Directory -Path (Join-Path $Run $prefix.plan)).FullName
        $inputSave=Join-Path $branch 'completed.ddsave'
        Require ((Digest $inputSave)-ceq(Digest (Join-Path $branch 'completed-restored.ddsave'))) 'Prefix lacks identical restore evidence.'
        Copy-Item -LiteralPath $inputSave -Destination (Join-Path $destination 'input.ddsave')
        Copy-Item -LiteralPath (Join-Path $branch 'RESULT.json') -Destination (Join-Path $destination 'PREFIX_RESULT.json')
        $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
            [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
            [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
            [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
        $session.Restore($inputSave)
        $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic')
        $codec=[Decennium.Foundation.SnapshotCodec]::new()
        $before=$field.GetValue($session).Capture()
        $session.Save((Join-Path $destination 'verified-input.ddsave'))
        Require ((Digest $inputSave)-ceq(Digest (Join-Path $destination 'verified-input.ddsave'))) 'Strict input restore changed the actual prefix.'
        $owner='TEST_ONLY.companion'
        Require ($before.Revision-eq$prefix.finalRevision-and$before.Encounter.CurrentActor-eq$owner-and($before.WorldIntervals|Where-Object ActorId -eq $owner).ActionSpent) 'Actual paid care turn is unavailable.'
        $turn=if($prefix.plan-eq'Invocation'){$prefix.invocations[-1].Turn}else{$prefix.cast.Turn}
        Require (@($before.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq$turn.EpochId-and$_.Turn.ActorId-eq$owner-and$_.Turn.LocalStart-eq$turn.LocalStart}).Count-eq0) 'Care turn had already ended.'
        $command=[Decennium.Foundation.Command]::new("ferry.care.$($prefix.plan).actual-end.$($before.Revision)",$owner,$before.Revision,'EndRegularTurn',$before.Encounter.CurrentTurnId)
        $result=$session.Submit('Player',$command)
        Require ($result.Response-eq'Committed') "Actual care End rejected: $($result|ConvertTo-Json -Compress)"
        $after=$field.GetValue($session).Capture()
        $ends=@($after.CastingTurnEnds|Where-Object {$_.Turn.EpochId-eq$turn.EpochId-and$_.Turn.ActorId-eq$owner-and$_.Turn.LocalStart-eq$turn.LocalStart})
        Require ($ends.Count-eq1-and$after.Encounter.CurrentActor-eq'TEST_ONLY.actor') 'Actual care End did not settle exactly once and advance to the next actor.'
        $stable=[Convert]::ToBase64String($codec.Encode($after))
        Require ($session.Submit('Player',$command).Response-eq'Duplicate'-and$stable-ceq[Convert]::ToBase64String($codec.Encode($field.GetValue($session).Capture()))) 'Repeated End changed state.'
        $final=Join-Path $destination 'continued.ddsave';$restored=Join-Path $destination 'continued-restored.ddsave'
        $session.Save($final);$session.Restore($final);$session.Save($restored)
        Require ((Digest $final)-ceq(Digest $restored)) 'Post-End strict restore changed bytes.'
        $receipt=$after.Receipts|Where-Object Id -eq $command.Id
        Require ($null-ne$receipt-and$receipt.Revision-eq$after.Revision) 'Actual End receipt is missing.'
        $report.branches+=@{plan=$prefix.plan;prefixPath=$branch;prefixReportSha256=(Digest (Join-Path $branch 'RESULT.json'));inputSha256=(Digest $inputSave);inputRevision=$before.Revision;command=$command;response=$result;receipt=$receipt;retainedCommand=[Decennium.Foundation.CommandHistory]::Read($receipt);castingEnd=$ends[0];finalRevision=$after.Revision;clock=$after.RuleClock;rp=$after.ResonancePools;strain=$after.CastingStrain;lives=@($after.Lives|Where-Object {$_.ActorId-in@($owner,'TEST_ONLY.actor')});recharges=$after.AbilityRecharges;randomBefore=$before.RandomState;randomAfter=$after.RandomState;finalSaveSha256=(Digest $final)}
    }
    Require ($report.branches.Count-eq3-and@($report.branches.plan|Sort-Object -Unique).Count-eq3) 'Expected exactly three distinct care continuations.'
    $report.status='PASS_GENUINE_FERRY_CARE_ENDS_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o')
$report|ConvertTo-Json -Depth 80|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
