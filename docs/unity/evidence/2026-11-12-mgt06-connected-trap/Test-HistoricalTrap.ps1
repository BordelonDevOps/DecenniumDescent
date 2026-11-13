param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Save,
    [switch]$Restore
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$profile = [Decennium.Foundation.Laboratory.SharedFishingTrapFixture]::new()
$policy = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::WithFishingTrap($profile,23)
$store = [Decennium.Foundation.FileSaveStore]::new()
if ($Restore) {
    $initial = $store.Load($Save)
    $simulation = [Decennium.Foundation.Simulation]::new($policy,$initial,'Laboratory')
    $store.Save("$Save.restored.ddsave",$simulation.Capture())
    if ((Get-FileHash $Save).Hash -cne (Get-FileHash "$Save.restored.ddsave").Hash) { throw 'Authentic standalone save changed.' }
} else {
    $simulation = [Decennium.Foundation.Simulation]::new($policy,$policy.Initial(),'Laboratory')
    $hostGrant = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::Host()
    $set = [Decennium.Foundation.Command]::new('historical.set',$profile.SetterId,0,'Interact',$profile.TrapIdentity,1)
    $clock = [Decennium.Foundation.Command]::new('historical.clock','TEST_ONLY.actor',1,'AdvanceClock','',300,1)
    if ($simulation.Execute($hostGrant,$set).Outcome -ne 'Committed' -or $simulation.Execute($hostGrant,$clock).Outcome -ne 'Committed') {
        throw 'The historical witness did not deploy.'
    }
    $store.Save($Save,$simulation.Capture())
}
$state = $simulation.Capture()
[ordered]@{Status='PASS'; Revision=$state.Revision; Wire=$state.WireSchemaVersion; Fingerprint=$state.ContentFingerprint
    Attempt=$state.FishingTrapAttempts[0].Status.ToString(); Sha256=(Get-FileHash $Save).Hash.ToLowerInvariant()} | ConvertTo-Json
