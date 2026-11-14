param([string]$AssemblyRoot,[string]$PendingSave,[string]$Output,[switch]$ExpectReversed)
$ErrorActionPreference='Stop'
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
$session.Restore($PendingSave)
$flags=[Reflection.BindingFlags]'Instance,NonPublic'
$policy=$session.GetType().GetField('policy',$flags).GetValue($session)
$state=$session.GetType().GetField('simulation',$flags).GetValue($session).Capture()
$rest=$state.ShortRests[0]
$grant=$state.ConsumeDecay
# Detached coincidence control; no public state editing or forged restore is admitted.
$state.ConsumeDecay=[Decennium.Foundation.ConsumeDecayRecord]::new($grant.CommandId,$grant.Revision,$rest.StartedAt,$grant.Offer,$true)
$command=[Decennium.Foundation.Command]::new('rest.order-observation','TEST_ONLY.actor',$state.Revision,'AdvanceClock','',3600,1)
$failure=$policy.Resolve($state,$command)
if ($null -ne $failure) { throw "Scheduler did not reach the observation: $failure" }
$probe=[Decennium.Foundation.Laboratory.ShortRestOrderProbe]::Last
if ([Decennium.Foundation.Laboratory.ShortRestOrderProbe]::Count -ne 1 -or $null -eq $probe) { throw 'Expected exactly one actual completion observation.' }
if ($state.ShortRests[0].Outcome -ne 'Completed' -or $state.ConsumeDecay.End -ne 'Expired') { throw 'Both operations must eventually complete in each variant.' }
$passed=$probe.Clock -ceq $rest.DueAt.ToString() -and $probe.RestBeforeWrite -ceq 'Active' -and $probe.TemporaryHp -eq 0 -and
    $probe.GrantId -ceq $grant.CommandId -and $probe.GrantRevision -eq $grant.Revision -and
    $probe.GrantEnd -ceq 'Expired' -and $probe.GrantEndedAt -ceq $rest.DueAt.ToString()
$assertionFailure=$null
try { if (!$passed) { throw 'ORDER_BEFORE_COMPLETION: the same grant must already be expired and its buffer zero at the tied completion write.' } }
catch { $assertionFailure=$_.Exception.Message }
if ($ExpectReversed -and ($passed -or $assertionFailure -notlike 'ORDER_BEFORE_COMPLETION:*')) { throw 'Reversed order did not fail the ordering assertion itself.' }
if (!$ExpectReversed -and !$passed) { throw $assertionFailure }
$assemblies=[ordered]@{}
foreach ($name in 'Core','Persistence','LabModel') {
    $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    $assembly=[AppDomain]::CurrentDomain.GetAssemblies() | Where-Object Location -eq $path
    $assemblies[$name]=@{sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant();moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
[ordered]@{Status='PASS'; Variant=if ($ExpectReversed) {'ReversedOrder'} else {'ObservedOriginal'}
    OrderingAssertion=if ($passed) {'PASS'} else {'EXPECTED_FAIL'}; AssertionFailure=$assertionFailure
    Observations=[Decennium.Foundation.Laboratory.ShortRestOrderProbe]::Count; AtCompletionWrite=$probe
    ExpectedGrantId=$grant.CommandId; ExpectedGrantRevision=$grant.Revision; ExpectedDeadline=$rest.DueAt.ToString()
    FinalRest=$state.ShortRests[0].Outcome.ToString(); FinalGrant=$state.ConsumeDecay.End.ToString()
    PendingSaveSha256=(Get-FileHash -LiteralPath $PendingSave).Hash.ToLowerInvariant(); Assemblies=$assemblies} |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Output -Encoding utf8
Write-Output "PASS: $($probe.Clock) ordering assertion $passed; reversed=$ExpectReversed"
