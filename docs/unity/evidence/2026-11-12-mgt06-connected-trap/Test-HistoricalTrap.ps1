param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Save,
    [switch]$Restore
)
$ErrorActionPreference = 'Stop'
$loaded = [ordered]@{}
foreach ($name in 'Core','Persistence','LabModel') {
    $dll = "Decennium.Foundation.$name.dll"
    $path = (Resolve-Path -LiteralPath (Join-Path $AssemblyRoot $dll)).Path
    $assembly = [Reflection.Assembly]::LoadFrom($path)
    if ($assembly.Location -cne $path) { throw "Unexpected loaded assembly $dll." }
    $loaded[$dll] = [ordered]@{sha256=(Get-FileHash $assembly.Location).Hash.ToLowerInvariant()
        moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
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
[ordered]@{Status='PASS'; Revision=$state.Revision; Wire=$state.SchemaVersion; Fingerprint=$state.ContentFingerprint
    Attempt=$state.FishingTrapAttempts[0].Status.ToString(); Sha256=(Get-FileHash $Save).Hash.ToLowerInvariant()
    ExecutedAssemblies=$loaded} | ConvertTo-Json -Depth 5
