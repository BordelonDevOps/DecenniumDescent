param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run,
    [ValidateRange(30,200)][int]$Samples=30
)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Force $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$flags=[Reflection.BindingFlags]'NonPublic,Instance'
$sessionType=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]
$store=[Decennium.Foundation.FileSaveStore]::new()
$codec=[Decennium.Foundation.SnapshotCodec]::new()
function Measure-Elapsed([scriptblock]$action) {
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $null=& $action
    $watch.Elapsed.TotalMilliseconds
}
function Summary($rows,[string]$field) {
    $sorted=@($rows | ForEach-Object {$_[$field]} | Sort-Object)
    [ordered]@{Median=$sorted[[int][Math]::Ceiling($sorted.Count/2.0)-1]
        P95=$sorted[[int][Math]::Ceiling($sorted.Count*0.95)-1]; Max=$sorted[-1]}
}
$reports=[ordered]@{}
foreach ($profile in 'Default','FishingTrap') {
    $folder=(New-Item -ItemType Directory -Force (Join-Path $Run $profile)).FullName
    $source=if ($profile -eq 'Default') {
        Join-Path $PSScriptRoot '../2026-11-12-exp05-local-mining/connected/travel-continued.ddsave'
    } else {
        Join-Path $PSScriptRoot '../2026-11-12-mgt06-connected-trap/connected/trap-continued.ddsave'
    }
    $history=$store.Load((Resolve-Path $source).Path)
    $session=if ($profile -eq 'Default') { $sessionType::Start() } else { $sessionType::StartWithFishingTrap() }
    $policy=$sessionType.GetField('policy',$flags).GetValue($session)
    $proof=$policy.GetType().GetMethod('FindPlanningPassage',$flags)
    $profileChecks=$policy.GetType().GetMethods($flags) | Where-Object { $_.Name -eq 'ValidateState' -and $_.GetParameters().Count -eq 2 }
    $plan=$history.NextCharterPlans[0]
    $planReceipt=$history.Receipts | Where-Object Revision -eq $plan.StartRevision
    $planCommand=[Decennium.Foundation.CommandHistory]::Read($planReceipt)
    if ($planCommand.Kind -ne 'StartNextCharterPlan' -or $planCommand.ExpectedRevision -ne 74) { throw 'Unexpected accepted charter checkpoint.' }
    foreach ($receipt in $history.Receipts | Where-Object Revision -le 74) {
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        $result=switch ($receipt.Principal) {
            'TEST_ONLY.session-first-opponent' { $session.Submit('FirstOpponent',$command) }
            'TEST_ONLY.session-operator' { $session.SubmitSessionCommand($command) }
            'TEST_ONLY.host' { $session.Submit('Player',$command) }
            default { throw "Unexpected principal before charter declaration: $($receipt.Principal)" }
        }
        if ($result.Response -ne 'Committed' -or $result.Revision -ne $receipt.Revision) { throw "Prefix diverged at $($receipt.Revision)." }
    }
    $prePath=Join-Path $folder 'pre-submit.ddsave'
    $session.Save($prePath)
    $pre=$store.Load($prePath)
    $through=$pre.ExpeditionEpisodeClose.SourceRevision
    $expectedDigest=$null
    $rows=@()
    for ($i=0;$i -le $Samples;$i++) {
        $restore=Measure-Elapsed { $session.Restore($prePath) }
        $watch=[Diagnostics.Stopwatch]::StartNew()
        $result=$session.Submit('Player',$planCommand)
        $submit=$watch.Elapsed.TotalMilliseconds
        $view=$session.View('Player')
        $total=$watch.Elapsed.TotalMilliseconds
        if ($result.Response -ne 'Committed' -or $view.Revision -ne 75) {
            throw "Public charter command did not commit: $($result.Response), action r$($result.Revision), view r$($view.Revision)."
        }
        $postPath=Join-Path $folder 'post-submit.ddsave'
        $session.Save($postPath)
        $digest=(Get-FileHash $postPath).Hash.ToLowerInvariant()
        if ($null -eq $expectedDigest) { $expectedDigest=$digest }
        if ($digest -cne $expectedDigest) { throw 'Canonical charter output changed across samples.' }
        $copy=Measure-Elapsed { $pre.Copy() }
        $encode=Measure-Elapsed { $codec.Encode($pre) }
        $post=$store.Load($postPath)
        $coreShape=Measure-Elapsed { [Decennium.Foundation.Validation]::Snapshot($post) }
        $validation=Measure-Elapsed {
            $failure=$profileChecks.Invoke($policy,[object[]]@($post,[Func[string]]{ return '' }))
            if ($failure -cne '') { throw "Isolated profile validation failed: $failure" }
        }
        $watch.Restart()
        $revision=$proof.Invoke($policy,[object[]]@($pre,$plan.Terms,$through))
        $passage=$watch.Elapsed.TotalMilliseconds
        if ($revision -ne $plan.PassageRevision) { throw 'The isolated reference found a different passage.' }
        $candidate=$pre.Copy()
        $watch.Restart()
        $failure=$policy.Resolve($candidate,$planCommand)
        $resolver=$watch.Elapsed.TotalMilliseconds
        if ($null -ne $failure) { throw $failure }
        if ($i -ne 0) {
            $rows += [ordered]@{Sample=$i; PublicMs=$total; SubmitMs=$submit; ViewMs=$total-$submit
                PassageMs=$passage; ResolverMs=$resolver; CopyMs=$copy; EncodeMs=$encode; CoreShapeMs=$coreShape
                ProfileChecksMs=$validation; StrictRestoreMs=$restore}
        }
    }
    $rows | ForEach-Object {[pscustomobject]$_} | Export-Csv (Join-Path $folder 'samples.csv') -NoTypeInformation
    $report=[ordered]@{Fingerprint=$pre.ContentFingerprint; PreRevision=$pre.Revision; CloseSourceRevision=$through
        PassageRevision=$plan.PassageRevision; ResultSha256=$expectedDigest; Samples=$Samples}
    foreach ($field in 'PublicMs','SubmitMs','ViewMs','PassageMs','ResolverMs','CopyMs','EncodeMs','CoreShapeMs','ProfileChecksMs','StrictRestoreMs') {
        $report[$field]=Summary $rows $field
    }
    $reports[$profile]=$report
    $reports | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $Run 'results.json') -Encoding utf8
}
Get-Content (Join-Path $Run 'results.json')
