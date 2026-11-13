param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run,
    [ValidateRange(30,200)][int]$Samples=30
)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Force $Run).FullName
$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path
$assemblyWatch=[Diagnostics.Stopwatch]::StartNew()
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$assemblyMs=$assemblyWatch.Elapsed.TotalMilliseconds
$scope=(Resolve-Path (Join-Path $PSScriptRoot '../2026-11-13-int03-active-work-performance')).Path
$flags=[Reflection.BindingFlags]'NonPublic,Instance'
$static=[Reflection.BindingFlags]'NonPublic,Static'
$type=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]
$store=[Decennium.Foundation.FileSaveStore]::new()
$codec=[Decennium.Foundation.SnapshotCodec]::new()
function Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Time-Operation([scriptblock]$action) {
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $null=& $action
    $watch.Elapsed.TotalMilliseconds
}
function Summarize($rows,[string]$field) {
    $sorted=@($rows | ForEach-Object {$_[$field]} | Sort-Object)
    $mid=[int][Math]::Floor($sorted.Count/2)
    $median=if($sorted.Count % 2){$sorted[$mid]}else{($sorted[$mid-1]+$sorted[$mid])/2}
    [ordered]@{Median=$median; P95=$sorted[[int][Math]::Ceiling($sorted.Count*0.95)-1]; Max=$sorted[-1]}
}
$results=[ordered]@{}
foreach ($profile in 'Default','FishingTrap') {
    $trap=$profile -eq 'FishingTrap'
    $folder=(New-Item -ItemType Directory -Force (Join-Path $Run $profile)).FullName
    $primary=Join-Path $scope "performance/$profile/post-submit.ddsave"
    $paired=Join-Path $scope "performance/$profile/pre-submit.ddsave"
    $final=Join-Path $scope $(if($trap){'connected/FishingTrap/trap-continued.ddsave'}else{'connected/Default/travel-continued.ddsave'})
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $session=if($trap){$type::StartWithFishingTrap()}else{$type::Start()}
    $null=$session.View('Player')
    $startup=$watch.Elapsed.TotalMilliseconds
    $watch.Restart()
    $session.Restore($primary)
    $null=$session.View('Player')
    $first=$watch.Elapsed.TotalMilliseconds
    $state=$store.Load($primary)
    $policy=$type.GetField('policy',$flags).GetValue($session)
    $policyType=$policy.GetType()
    $replay=$policyType.GetMethod('ValidateCanonicalHistory',$flags)
    $profileChecks=$policyType.GetMethods($flags) | Where-Object {$_.Name -eq 'ValidateState' -and $_.GetParameters().Count -eq 2}
    $simulation=$type.GetField('simulation',$flags).GetValue($session)
    $origin=[Decennium.Foundation.Simulation].GetField('verificationOrigin',$flags).GetValue($simulation)
    $seal=$policyType.GetMethod('Decennium.Foundation.IVerifiedCommandPolicy.Seal',$flags)
    $bytes=[IO.File]::ReadAllBytes($primary)
    $digest=Digest $primary
    $rows=@()
    for ($i=1;$i -le $Samples;$i++) {
        $watch.Restart()
        $session.Restore($primary)
        $restore=$watch.Elapsed.TotalMilliseconds
        $view=$session.View('Player')
        $public=$watch.Elapsed.TotalMilliseconds
        if ($view.Revision -ne 104 -or $view.Clock.ToString() -ne '57617/2') { throw 'Public r104 restore changed revision or clock.' }
        $roundTrip=Join-Path $folder 'round-trip.ddsave'
        $session.Save($roundTrip)
        if ((Digest $roundTrip) -cne $digest) { throw 'Public restore changed canonical bytes.' }
        $rows += [ordered]@{Sample=$i; PublicMs=$public; RestoreMs=$restore; ViewMs=$public-$restore}
    }
    $probes=@()
    for ($i=1;$i -le 5;$i++) {
        $probes += [ordered]@{Sample=$i
            ReadMs=(Time-Operation {[IO.File]::ReadAllBytes($primary)})
            DecodeMs=(Time-Operation {$codec.Decode($bytes)})
            CopyMs=(Time-Operation {$state.Copy()})
            ShapeMs=(Time-Operation {[Decennium.Foundation.Validation]::Snapshot($state)})
            ProfileChecksMs=(Time-Operation {
                $failure=$profileChecks.Invoke($policy,[object[]]@($state,[Func[string]]{return ''}))
                if($failure -cne ''){throw "Profile probe failed: $failure"}
            })
            ReplayAndCompareMs=(Time-Operation {
                $failure=$replay.Invoke($policy,[object[]]@($state))
                if($null -ne $failure){throw $failure}
            })
            SealMs=(Time-Operation {
                if($null -eq $seal.Invoke($policy,[object[]]@($origin))){throw 'Seal probe failed.'}
            })}
    }
    $control=@()
    foreach ($path in $paired,$final) {
        $watch.Restart()
        $session.Restore($path)
        $view=$session.View('Player')
        $elapsed=$watch.Elapsed.TotalMilliseconds
        $session.Save((Join-Path $folder "control-r$($view.Revision).ddsave"))
        if((Digest (Join-Path $folder "control-r$($view.Revision).ddsave")) -cne (Digest $path)){throw 'Control restore changed canonical bytes.'}
        $control += [ordered]@{Revision=$view.Revision; PublicMs=$elapsed; Sha256=(Digest $path)}
    }
    $rows | ForEach-Object {[pscustomobject]$_} | Export-Csv (Join-Path $folder 'samples.csv') -NoTypeInformation
    $probes | ForEach-Object {[pscustomobject]$_} | Export-Csv (Join-Path $folder 'probes.csv') -NoTypeInformation
    $report=[ordered]@{Samples=$Samples; FirstLoadWithViewMs=$first; StartupWithViewMs=$startup; Sha256=$digest; Controls=$control}
    foreach($field in 'PublicMs','RestoreMs','ViewMs'){$report[$field]=Summarize $rows $field}
    foreach($field in 'ReadMs','DecodeMs','CopyMs','ShapeMs','ProfileChecksMs','ReplayAndCompareMs','SealMs'){$report[$field]=Summarize $probes $field}
    $results[$profile]=$report
    [ordered]@{Status='PASS'; AssemblyLoadMs=$assemblyMs; Profiles=$results} | ConvertTo-Json -Depth 8 |
        Set-Content (Join-Path $Run 'results.json') -Encoding utf8
}
Get-Content (Join-Path $Run 'results.json')
