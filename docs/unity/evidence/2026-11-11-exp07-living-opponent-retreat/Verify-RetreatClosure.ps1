param([Parameter(Mandatory)][string]$AssemblyRoot)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$assemblies=@(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests'){
    $path=Join-Path $root "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{name=(Split-Path -Leaf $path);sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
})
$t=[Decennium.Foundation.Tests.FoundationCases]
$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Invoke-Fixture([string]$Name,[object[]]$Arguments){
    try{$t.GetMethod($Name,$flags).Invoke($null,$Arguments)}catch{throw $_.Exception.GetBaseException()}
}
$kind=[Decennium.Foundation.CommandKind]
$guard=[Decennium.Foundation.CombatStance]::Guarded
$ordinary=[Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
$press=[Decennium.Foundation.PressHitInstruction]::KeepExisting
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$policy=Invoke-Fixture 'RetreatPolicy' @([uint32]15,$null,$null)
$sim=Invoke-Fixture 'RetreatReady' @($policy,$true,57449,2)
$admitted=$sim.Capture()
$d=$admitted.Retreat.Definition
$hostAuthority=Invoke-Fixture 'LaterHost' @()
$declare=Invoke-Fixture 'RetreatInstruction' @($sim,$kind::DeclareRetreat,$null,$d.LeadId)
$null=Invoke-Fixture 'LaterCommit' @($sim,$declare)
$null=Invoke-Fixture 'PlayRetreatToOutcome' @($sim,$true,$false)
$settled=$sim.Capture()
$checkpoint=$settled.ExpeditionPressureCheckpoints[0]
$end=$settled.Retreat.Round.Settlement
if($settled.Retreat.Escape -lt 3 -or $end.Outcome.ToString() -ne 'PhysicallyBlocked' -or $checkpoint.At.ToString() -ne '28800/1' -or $checkpoint.Natural -ne 1 -or $checkpoint.Consequence.ToString() -ne 'RouteClosure' -or $checkpoint.AppliedRevision -ne $end.Revision -or -not $end.LeadCrossingId -or -not $end.CompanionCrossingId){throw 'The actual natural-one closure did not block the threshold-qualified exit'}
for($i=0;$sim.Capture().Encounter.CurrentActor -ne $d.LeadId -and $i -lt 3;$i++){
    $null=Invoke-Fixture 'EndReinforcementTurn' @($sim,$guard)
}
$null=Invoke-Fixture 'LaterStance' @($sim,$guard)
$before=$sim.Capture()
$move=Invoke-Fixture 'Tac' @($sim,$kind::TacticalStep,$before.Encounter.CurrentTurnId,$null,0,2,'',$false,$ordinary,0,$press)
$beforeHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($before))).ToLowerInvariant()
$result=$sim.Execute($hostAuthority,$move)
$afterHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($sim.Capture()))).ToLowerInvariant()
if($result.Outcome.ToString() -ne 'Rejected' -or $result.Code -ne 'RetreatOpeningObstructedByPressure' -or $beforeHash -ne $afterHash){throw "The ordinary tactical crossing did not preserve the actual closure: $($result.Outcome)/$($result.Code)"}
[ordered]@{status='PASS';seed=15;delay='57449/2';admitted=$admitted.RuleClock.ToString();at=$end.At.ToString();
    escape=$settled.Retreat.Escape;pursuit=$settled.Retreat.Pursuit;outcome=$end.Outcome.ToString();paidCrossings=@($end.LeadCrossingId,$end.CompanionCrossingId);
    checkpoint=[ordered]@{natural=$checkpoint.Natural;consequence=$checkpoint.Consequence.ToString();revision=$checkpoint.AppliedRevision;receipt=$checkpoint.CommandId;pressure=$checkpoint.StoredPressure};
    successfulRetreatEvents=@($settled.ExpeditionPressureChanges|Where-Object {$_.Kind.ToString() -eq 'SuccessfulRetreat'}).Count;
    rejectedMove=$result.Code;unchangedSaveSha256=$beforeHash;assemblies=$assemblies} | ConvertTo-Json -Depth 6
