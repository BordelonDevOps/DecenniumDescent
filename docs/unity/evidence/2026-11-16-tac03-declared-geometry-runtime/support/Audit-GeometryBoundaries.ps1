param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$OutputPath,[string]$Checkpoint)
$ErrorActionPreference='Stop'
$auditRoot=Split-Path -Parent ([IO.Path]::GetFullPath($OutputPath))
if(!(Test-Path -LiteralPath $auditRoot)){New-Item -ItemType Directory -Path $auditRoot|Out-Null}
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $auditRoot @($PSCommandPath)
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){
    $path=(Resolve-Path -LiteralPath (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")).Path
    $assembly=[Reflection.Assembly]::LoadFrom($path)
    if($assembly.Location-cne$path){throw 'Unexpected loaded exclusion-audit assembly'}
    $loaded[$part]=@{sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant();moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
$geometrySession=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
    [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
    [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
if($Checkpoint){$geometrySession.Restore((Resolve-Path -LiteralPath $Checkpoint).Path)}
$flags=[Reflection.BindingFlags]'Instance,NonPublic'
$policy=$geometrySession.GetType().GetField('policy',$flags).GetValue($geometrySession)
$simulation=$geometrySession.GetType().GetField('simulation',$flags).GetValue($geometrySession)
$state=$simulation.Capture();$codec=[Decennium.Foundation.SnapshotCodec]::new();$before=$codec.Encode($state)
$selected=[ordered]@{}
foreach($name in 'overwatchFoundation','overwatchRuntime','overwatchExecution','rangedCombat','soldierInitialLoadout','soldierCharacterBuild','routeTravelFixture','routeMotionFixture','expeditionCampSiteProfile','huntingTrapFixture','worldConfiguration'){
    $field=$policy.GetType().GetField($name,$flags)
    if(!$field){throw "Missing audited field: $name"}
    $selected[$name]=$null-ne$field.GetValue($policy)
    if($selected[$name]){throw "Unexpected selected capability: $name"}
}
$counts=[ordered]@{}
foreach($name in 'RepeatingCrossbows','OverwatchIntervals','OverwatchDesignations','OverwatchOffers','OverwatchRiderChoices','RouteTravels','ExpeditionCampSites','ExpeditionCampActivities','HuntingTrapDeployments','HuntingTrapActions','HuntingTrapTriggers','HuntingTrapTethers'){
    $counts[$name]=$state.$name.Count
    if($counts[$name]-ne0){throw "Unexpected excluded runtime records: $name"}
}
$overwatchGrants=@($state.CharacterFeatureGrants|Where-Object {$_.FeatureId-match'overwatch'})
if($overwatchGrants.Count-ne0){throw 'Unexpected Overwatch grant'}
$probes=[Collections.Generic.List[object]]::new()
foreach($kind in 'StartRouteTravel','BeginCampUse','ResolveOverwatchRider'){
    $command=[Decennium.Foundation.Command]::new('geometry.boundary.'+$kind,'TEST_ONLY.actor',$state.Revision,$kind,'TEST_ONLY.geometry-unsupported')
    $query=$policy.QueryCommand($state,[Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::Host(),$command)
    if($query.Admissible){throw "Excluded internal command admitted: $kind"}
    $probes.Add([ordered]@{kind=$kind;internalQuery=$query;publicQuery=$geometrySession.QueryCastingCommand('Player',$command)})
}
$trapCommand=[Decennium.Foundation.Command]::new('geometry.boundary.trap','TEST_ONLY.actor',$state.Revision,'Interact','TEST_ONLY.geometry-unsupported')
$trapGate=$policy.GetType().GetMethod('IsHuntingTrapCommand',$flags).Invoke($policy,@($state,$trapCommand))
if($trapGate){throw 'Unselected hunting trap entered internal dispatch'}
$after=$codec.Encode($state)
if(![Linq.Enumerable]::SequenceEqual[byte]($before,$after)){throw 'Boundary queries modified state'}
$report=[ordered]@{status='PASS';scope='Selected configuration, actual grants/genesis or restored records and internal dispatch probes; combine with source control-flow review';checkpoint=$Checkpoint;revision=$state.Revision;wire=$state.WireSchemaVersion;fingerprint=$state.ContentFingerprint;selected=$selected;recordCounts=$counts;overwatchGrants=$overwatchGrants;internalQueries=$probes.ToArray();huntingTrapDispatch=$trapGate;queriesUnchanged=$true}
$report.assemblies=$loaded
Complete-GeometryExecutionBinding $auditRoot $executionSourceBinding
$report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $OutputPath -Encoding utf8
$report|ConvertTo-Json -Depth 10
