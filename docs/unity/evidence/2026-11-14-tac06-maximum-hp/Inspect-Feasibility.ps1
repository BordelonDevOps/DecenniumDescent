param([string]$AssemblyRoot,[string]$OrdinaryRun,[string]$CalendarRun,[string]$Output)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function ReadProbe($path,$kind,$target,$inventory) {
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
    $session.Restore((Resolve-Path -LiteralPath $path).Path)
    $flags=[Reflection.BindingFlags]'Instance,NonPublic'
    $policy=$session.GetType().GetField('policy',$flags).GetValue($session)
    $state=$session.GetType().GetField('simulation',$flags).GetValue($session).Capture()
    $view=$session.View('Player')
    $before=@{Revision=$state.Revision;Clock=$state.RuleClock.ToString();InventoryCombat=$state.InventoryCombat
        PublicInEncounter=$view.InEncounter;Hero=($state.Actors | Where-Object Id -eq 'TEST_ONLY.actor')
        HeroLife=($state.Lives | Where-Object ActorId -eq 'TEST_ONLY.actor')
        EncounterId=$state.Encounter.Id;EncounterSparse=$state.Encounter.Sparse;ShortRests=$state.ShortRests.Count}
    $command=[Decennium.Foundation.Command]::new('capacity.feasibility.reason','TEST_ONLY.actor',$state.Revision,$kind,$target,0,0,$inventory)
    $failure=$policy.Resolve($state,$command)
    @{SnapshotSha256=(Digest $path);Before=$before;ResolverFailure=$failure}
}
$inventory=[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'TEST_ONLY.actor','Pickup')
$ordinary=ReadProbe "$OrdinaryRun/after-rest.ddsave" 'UseAlchemyDose' 'manufacture.order.104.dose0' $inventory
$calendar=ReadProbe "$CalendarRun/before-first-rest.ddsave" 'BeginShortRest' 'TEST_ONLY.short-rest-berth' $null
if ($ordinary.ResolverFailure -cne 'AlchemyOwnTacticalTurnRequired') { throw 'Ordinary healing diagnosis changed.' }
if ((Digest "$OrdinaryRun/after-rest.ddsave") -cne (Digest "$OrdinaryRun/after-heal.ddsave")) { throw 'Rejected ordinary healing changed state.' }
if ($calendar.ResolverFailure -cne 'ShortRestRequiresOrdinaryExploration' -or $calendar.Before.InventoryCombat -or
    $calendar.Before.PublicInEncounter -or !$calendar.Before.EncounterSparse -or
    $calendar.Before.Hero.X -ne 0 -or $calendar.Before.Hero.Y -ne 1) { throw 'Sparse-calendar admission diagnosis changed.' }
$assemblies=[ordered]@{}
foreach ($name in 'Core','Persistence','LabModel') {
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    $assembly=[AppDomain]::CurrentDomain.GetAssemblies() | Where-Object Location -eq $file
    $assemblies[$name]=@{sha256=(Digest $file);moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
[ordered]@{Status='DIAGNOSED_CAPABILITY_BOUNDARIES';Implementation='44837a2ed2be8a558ca6d37544621dac6400ab9d'
    Scope='Read-only diagnostics of canonical predecessor saves; no Flesh Warden runtime or capacity change implemented'
    OrdinaryHealing=$ordinary;SparseCalendarRest=$calendar;Assemblies=$assemblies} |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Output -Encoding utf8
