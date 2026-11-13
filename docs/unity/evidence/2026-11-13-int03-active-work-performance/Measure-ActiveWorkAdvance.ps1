param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run,
    [ValidateRange(30,200)][int]$Samples=30,
    [string]$ReferenceRoot
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
    $startup=[Diagnostics.Stopwatch]::StartNew()
    $session=if ($profile -eq 'Default') { $sessionType::Start() } else { $sessionType::StartWithFishingTrap() }
    $null=$session.View('Player')
    $startupMs=$startup.Elapsed.TotalMilliseconds
    $policy=$sessionType.GetField('policy',$flags).GetValue($session)
    $profileChecks=$policy.GetType().GetMethods($flags) | Where-Object { $_.Name -eq 'ValidateState' -and $_.GetParameters().Count -eq 2 }
    $targetReceipt=$history.Receipts | Where-Object Id -eq 'i-94'
    $advance=[Decennium.Foundation.CommandHistory]::Read($targetReceipt)
    if ($advance.Kind -ne 'AdvanceClock' -or $advance.ExpectedRevision -ne 103 -or $advance.X -ne 15421 -or $advance.Y -ne 1) {
        throw 'Unexpected accepted research advance.'
    }
    $prefixTimings=@()
    foreach ($receipt in $history.Receipts | Where-Object Revision -le 103) {
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        $stepTimer=[Diagnostics.Stopwatch]::StartNew()
        $result=switch ($receipt.Principal) {
            'TEST_ONLY.session-first-opponent' { $session.Submit('FirstOpponent',$command) }
            'TEST_ONLY.session-operator' { $session.SubmitSessionCommand($command) }
            'TEST_ONLY.host' { $session.Submit('Player',$command) }
            default { throw "Unexpected principal before charter declaration: $($receipt.Principal)" }
        }
        $prefixTimings += [pscustomobject]@{Revision=$receipt.Revision; Kind=$command.Kind.ToString(); SubmitMs=$stepTimer.Elapsed.TotalMilliseconds}
        if ($result.Response -ne 'Committed' -or $result.Revision -ne $receipt.Revision) { throw "Prefix diverged at $($receipt.Revision)." }
    }
    $prefixTimings | Export-Csv (Join-Path $folder 'prefix.csv') -NoTypeInformation
    $prePath=Join-Path $folder 'pre-submit.ddsave'
    $session.Save($prePath)
    $pre=$store.Load($prePath)
    $preDigest=(Get-FileHash $prePath).Hash.ToLowerInvariant()
    if ($ReferenceRoot) {
        $referencePre=Join-Path $ReferenceRoot "$profile/pre-submit.ddsave"
        if ((Get-FileHash $referencePre).Hash.ToLowerInvariant() -cne $preDigest) { throw 'The normal play prefix changed.' }
    }
    $liveTimer=[Diagnostics.Stopwatch]::StartNew()
    $liveResult=$session.SubmitSessionCommand($advance)
    $liveView=$session.View('Player')
    $liveMs=$liveTimer.Elapsed.TotalMilliseconds
    if ($liveResult.Response -ne 'Committed' -or $liveView.Revision -ne 104) { throw 'Live research advance did not commit.' }
    $livePath=Join-Path $folder 'live-submit.ddsave'
    $session.Save($livePath)
    $liveDigest=(Get-FileHash $livePath).Hash.ToLowerInvariant()
    $expectedDigest=$null
    $rows=@()
    for ($i=0;$i -le $Samples;$i++) {
        $restore=Measure-Elapsed { $session.Restore($prePath) }
        $watch=[Diagnostics.Stopwatch]::StartNew()
        $result=$session.SubmitSessionCommand($advance)
        $submit=$watch.Elapsed.TotalMilliseconds
        $view=$session.View('Player')
        $total=$watch.Elapsed.TotalMilliseconds
        if ($result.Response -ne 'Committed' -or $view.Revision -ne 104) {
            throw "Public advance did not commit: $($result.Response), action r$($result.Revision), view r$($view.Revision)."
        }
        $postPath=Join-Path $folder 'post-submit.ddsave'
        $session.Save($postPath)
        $digest=(Get-FileHash $postPath).Hash.ToLowerInvariant()
        if ($null -eq $expectedDigest) {
            $expectedDigest=$digest
            if ($expectedDigest -cne $liveDigest) { throw 'Live and restored research advances differ.' }
            if ($ReferenceRoot) {
                $referencePost=Join-Path $ReferenceRoot "$profile/post-submit.ddsave"
                if ((Get-FileHash $referencePost).Hash.ToLowerInvariant() -cne $expectedDigest) { throw 'Canonical advance result changed.' }
            }
        }
        if ($digest -cne $expectedDigest) { throw 'Canonical charter output changed across samples.' }
        $copy=Measure-Elapsed { $pre.Copy() }
        $encode=Measure-Elapsed { $codec.Encode($pre) }
        $post=$store.Load($postPath)
        $coreShape=Measure-Elapsed { [Decennium.Foundation.Validation]::Snapshot($post) }
        $validation=Measure-Elapsed {
            $failure=$profileChecks.Invoke($policy,[object[]]@($post,[Func[string]]{ return '' }))
            if ($failure -cne '') { throw "Isolated profile validation failed: $failure" }
        }
        $candidate=$pre.Copy()
        $watch.Restart()
        $failure=$policy.Resolve($candidate,$advance)
        $resolver=$watch.Elapsed.TotalMilliseconds
        if ($null -ne $failure) { throw $failure }
        if ($i -ne 0) {
            $rows += [ordered]@{Sample=$i; PublicMs=$total; SubmitMs=$submit; ViewMs=$total-$submit
                ResolverMs=$resolver; CopyMs=$copy; EncodeMs=$encode; CoreShapeMs=$coreShape
                ProfileChecksMs=$validation; StrictRestoreMs=$restore}
        }
    }
    $rows | ForEach-Object {[pscustomobject]$_} | Export-Csv (Join-Path $folder 'samples.csv') -NoTypeInformation
    $post=$store.Load($livePath)
    $beforeWork=$pre.FormulaWork | Where-Object Id -eq 'formula.103'
    $afterWork=$post.FormulaWork | Where-Object Id -eq 'formula.103'
    $report=[ordered]@{Fingerprint=$pre.ContentFingerprint; PreRevision=$pre.Revision; PostRevision=$post.Revision
        ClockBefore=$pre.RuleClock.ToString(); ClockAfter=$post.RuleClock.ToString(); RandomBefore=$pre.RandomState
        RandomAfter=$post.RandomState; FormulaBefore=$beforeWork.Status.ToString(); FormulaAfter=$afterWork.Status.ToString()
        LaborBefore=$beforeWork.Work.Labor.ToString(); LaborAfter=$afterWork.Work.Labor.ToString()
        PreSha256=$preDigest; ResultSha256=$expectedDigest; Samples=$Samples
        ColdStartupWithViewMs=$startupMs; LiveSubmitWithViewMs=$liveMs; LiveResultSha256=$liveDigest}
    foreach ($field in 'PublicMs','SubmitMs','ViewMs','ResolverMs','CopyMs','EncodeMs','CoreShapeMs','ProfileChecksMs','StrictRestoreMs') {
        $report[$field]=Summary $rows $field
    }
    $reports[$profile]=$report
    $reports | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $Run 'results.json') -Encoding utf8
}
Get-Content (Join-Path $Run 'results.json')
