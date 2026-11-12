param([Parameter(Mandatory)][string]$AssemblyRoot)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $file = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $file
    [ordered]@{name=Split-Path -Leaf $file;sha256=(Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant()}
})
$fixture = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$Name,[object[]]$Arguments) {
    try { $fixture.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
$policy = Call 'ReengagementPolicy' @([uint32]1,$null,$true,$true)
$null = $policy.EnableSurpriseAwareEntry([Decennium.Foundation.SurpriseAwareness]::Surprised)
$sim = Call 'LaterEarly' @($policy)
$null = Call 'EnterLater' @($sim)
$entry = $sim.Capture()
$start = $entry.SurpriseEntry.FirstStart
if ($start.Ordinal -ne 0 -or $entry.Encounter.CurrentActor -ne $entry.SurpriseEntry.Binding.ParticipantId -or -not $entry.SurpriseEntry.SurprisePending) {
    throw 'Hero-first actual entry did not record first Start 0.'
}
$null = Call 'EndReinforcementTurn' @($sim,[Decennium.Foundation.CombatStance]::Guarded)
$ended = $sim.Capture()
if ($ended.SurpriseEntry.FirstEnd.At -ne $entry.Encounter.StartAt(1) -or $ended.SurpriseEntry.SurprisePending) {
    throw 'Hero-first actual End did not clear surprise.'
}
[ordered]@{status='PASS';initiative=@($entry.LaterEncounter.Entry.Draws.Total);entry=$entry.RuleClock.ToString()
    firstOrdinal=$start.Ordinal;firstEnd=$ended.RuleClock.ToString();assemblies=$assemblies} | ConvertTo-Json -Depth 7
