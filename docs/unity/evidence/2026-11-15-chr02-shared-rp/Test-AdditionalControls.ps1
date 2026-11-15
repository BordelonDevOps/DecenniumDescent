param([string]$AssemblyRoot,[string]$PublicRoot,[string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path; $PublicRoot=(Resolve-Path $PublicRoot).Path
$Run=(New-Item -ItemType Directory $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require($condition,$message) { if (!$condition) { throw $message } }
function DigestBytes([byte[]]$bytes) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant() }
function DetachedBytes($state) { [Text.Encoding]::UTF8.GetBytes((ConvertTo-Json -InputObject $state -Depth 100 -Compress -EnumsAsStrings)) }
function Start-Cleric { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample()) }
$store=[Decennium.Foundation.FileSaveStore]::new(); $codec=[Decennium.Foundation.SnapshotCodec]::new()
$session=Start-Cleric
$policy=$session.GetType().GetField('policy',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($session)
$before=$store.Load("$PublicRoot/Restored/before-payment.ddsave")
$hero='TEST_ONLY.actor'; $ally='TEST_ONLY.companion'; $controls=[Collections.Generic.List[object]]::new()
foreach ($channel in 'sight','effect') {
    # These map variants are detached mechanical controls, never campaign saves or claimed source history.
    $s=$before.Copy()
    $cell=[Decennium.Foundation.ObservationMapCellRecord]::new(0,2,($channel -eq 'sight'),($channel -eq 'effect'),$false,$false)
    $s.ObservationCells=[Decennium.Foundation.ObservationMapCellRecord[]](@($s.ObservationCells | Where-Object { $_.X -ne 0 -or $_.Y -ne 2 })+@($cell))
    $visible=[Decennium.Foundation.Laboratory.ObservationRules]::CanSee($s,$ally,$hero)
    $effect=[Decennium.Foundation.Laboratory.ObservationGeometry]::LineOfEffectClear($s,$ally,$hero)
    Require ($visible -eq ($channel -eq 'effect') -and $effect -eq ($channel -eq 'sight')) "Independent $channel blocker did not affect its own channel."
    $sourceRejected=$false
    try { $null=$codec.Encode($s) } catch { $sourceRejected=$true }
    Require $sourceRejected 'Changed authored geometry must remain forbidden as a campaign save.'
    $bytes=DetachedBytes $s
    $command=[Decennium.Foundation.Command]::new("detached.$channel",$ally,$s.Revision,'UseHealingRite',$hero)
    $result=$policy.Resolve($s,$command)
    Require ($result -eq 'HealingRiteTargetUnavailable' -and (DigestBytes $bytes) -ceq (DigestBytes (DetachedBytes $s))) "$channel preflight changed detached state."
    $controls.Add(@{Kind="Detached $channel blocker";Result=$result;Visible=$visible;LineOfEffect=$effect;CampaignSaveRejected=$sourceRejected
        ComparisonEncoding='Complete public snapshot JSON; deliberately not an accepted campaign save';UnchangedSha256=(DigestBytes $bytes)})
}
$continued=$store.Load("$PublicRoot/Restored/continued.ddsave")
$partitionResults=[ordered]@{}
foreach ($partition in 'whole','split') {
    $session=Start-Cleric; $session.Restore("$PublicRoot/Restored/continued.ddsave")
    $parts=if ($partition -eq 'whole') { @(6) } else { @(2,4) }
    $i=0
    foreach ($seconds in $parts) {
        $view=$session.View('Player')
        $command=[Decennium.Foundation.Command]::new("partition.$partition.$i",$hero,$view.Revision,'AdvanceClock','',$seconds,1)
        Require ($session.SubmitSessionCommand($command).Response -eq 'Committed') "$partition ordinary clock did not advance."
        $i++
    }
    $path="$Run/$partition.ddsave"; $session.Save($path); $s=$store.Load($path)
    Require ($s.ResonancePools[0].Current -eq 1 -and $s.HealingRites.Count -eq 1 -and
        $s.RandomState -eq $continued.RandomState -and $s.ResonancePools[0].InitialFunding.Id -eq $continued.ResonancePools[0].InitialFunding.Id) 'Elapsed time changed funding or paid RNG.'
    $partitionResults[$partition]=@{Clock=$s.RuleClock.ToString();CurrentRp=$s.ResonancePools[0].Current;RNG=$s.RandomState
        FundingId=$s.ResonancePools[0].InitialFunding.Id;PaymentCommand=$s.HealingRites[0].CommandId;Revision=$s.Revision
        Sha256=(Get-FileHash $path).Hash.ToLowerInvariant()}
}
foreach ($field in 'Clock','CurrentRp','RNG','FundingId','PaymentCommand') {
    Require ($partitionResults.whole[$field] -eq $partitionResults.split[$field]) "Clock partition changed $field."
}
[ordered]@{Status='PASS';DetachedControls=$controls;Partitions=$partitionResults;Scope='Detached geometry plus lawful paid-history continuation; distinct partition receipts retained'} |
    ConvertTo-Json -Depth 6 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output 'PASS: independent sight/effect rejection and actual whole/split clock preservation.'
