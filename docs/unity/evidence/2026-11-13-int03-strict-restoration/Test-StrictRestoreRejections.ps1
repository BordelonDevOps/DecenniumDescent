param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Force $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$source=(Resolve-Path (Join-Path $PSScriptRoot '../2026-11-13-int03-active-work-performance/performance')).Path
$store=[Decennium.Foundation.FileSaveStore]::new()
function Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require([bool]$ok,[string]$message) { if(-not $ok){throw $message} }
$results=[ordered]@{}
foreach($profile in 'Default','FishingTrap') {
    $trap=$profile -eq 'FishingTrap'
    $target="$source/$profile/post-submit.ddsave"
    $other=if($trap){"$source/Default/post-submit.ddsave"}else{"$source/FishingTrap/post-submit.ddsave"}
    $folder=(New-Item -ItemType Directory -Force (Join-Path $Run $profile)).FullName
    $session=if($trap){[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()}
        else{[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()}
    $session.Restore($target)
    $original=$store.Load($target)
    $invalid=$original.Copy()
    $invalid.RandomState=[uint32]($original.RandomState -bxor 1)
    $store.Save("$folder/altered.ddsave",$invalid)
    $invalid=$original.Copy()
    $receipt=$invalid.Receipts[-1]
    $command=[Decennium.Foundation.Command]::new('i-94','TEST_ONLY.actor',103,'AdvanceClock','',0,1)
    $property=$command.GetType().GetProperty('Fingerprint',[Reflection.BindingFlags]'Instance,NonPublic')
    $receipt.Fingerprint=$property.GetValue($command)
    $store.Save("$folder/later-receipt.ddsave",$invalid)
    [IO.File]::WriteAllBytes("$folder/malformed.ddsave",[byte[]]@(1,2,3))
    $session.SetSeatEnabled('Player',$false)
    $session.Save("$folder/live-before.ddsave")
    $checks=[ordered]@{}
    foreach($item in @(
        @{Name='malformed'; Path="$folder/malformed.ddsave"},
        @{Name='wrong-profile'; Path=$other},
        @{Name='later-receipt'; Path="$folder/later-receipt.ddsave"},
        @{Name='altered'; Path="$folder/altered.ddsave"})) {
        $reason=$null
        try {$session.Restore($item.Path)}
        catch [ArgumentException] {$reason=$_.Exception.InnerException.Message; if(-not $reason){$reason=$_.Exception.Message}}
        catch [IO.InvalidDataException] {$reason=$_.Exception.InnerException.Message; if(-not $reason){$reason=$_.Exception.Message}}
        Require ($reason -and -not $session.View('Player').Enabled) "Failed restore changed grant or accepted $($item.Name)."
        $path="$folder/live-after-$($item.Name).ddsave"
        $session.Save($path)
        Require ((Digest $path) -ceq (Digest "$folder/live-before.ddsave")) "Failed restore changed live state: $($item.Name)."
        $checks[$item.Name]=[ordered]@{Reason=$reason; LiveSha256=(Digest $path)}
    }
    Require ($checks['later-receipt'].Reason -match 'InvalidSharedWorldHistory' -and
        $checks['altered'].Reason -match 'InvalidSharedWorldReplay') 'Negative witnesses must fail at distinct historical stages.'
    $recovery="$folder/recovery.ddsave"
    [IO.File]::WriteAllBytes($recovery,[byte[]]@(4,5,6))
    Copy-Item "$folder/altered.ddsave" "$recovery.bak" -Force
    $primaryBefore=Digest $recovery
    $badBackup=Digest "$recovery.bak"
    $rejected=$false
    try {$null=$session.RecoverBackup($recovery)} catch [ArgumentException] {$rejected=$true}
    Require ($rejected -and (Digest $recovery) -ceq $primaryBefore -and (Digest "$recovery.bak") -ceq $badBackup -and
        -not $session.View('Player').Enabled) 'Rejected backup changed files or grants.'
    Copy-Item $target "$recovery.bak" -Force
    $displaced=$session.RecoverBackup($recovery)
    Require ((Digest $recovery) -ceq (Digest $target) -and (Digest "$recovery.bak") -ceq (Digest $target) -and
        (Digest $displaced) -ceq $primaryBefore -and -not $session.View('Player').Enabled) 'Recovery must retain both saves, displaced bytes and grants.'
    $session.SetSeatEnabled('Player',$true)
    $retry=[Decennium.Foundation.CommandHistory]::Read($original.Receipts[-1])
    Require ($session.SubmitSessionCommand($retry).Response -eq 'Duplicate') 'Recovered clock receipt must remain idempotent.'
    $checks['backup']=[ordered]@{Rejected=$rejected; RecoveredSha256=(Digest $recovery); DisplacedSha256=(Digest $displaced)}
    $results[$profile]=$checks
}
[ordered]@{Status='PASS'; Profiles=$results} | ConvertTo-Json -Depth 8 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
