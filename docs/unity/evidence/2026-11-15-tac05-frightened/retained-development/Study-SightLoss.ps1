param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$BeforeCheckSave)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$run=New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot ('sight-study-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')))
$flags=[Reflection.BindingFlags]'Static,NonPublic'
$caseType=[Decennium.Foundation.Tests.FoundationCases]
function Call([string]$Name,[object[]]$Arguments){try{$caseType.GetMethod($Name,$flags).Invoke($null,$Arguments)}catch{throw $_.Exception.InnerException}}
$session=Call 'NewFrightenedExpedition' @()
$session.Restore((Resolve-Path -LiteralPath $BeforeCheckSave).Path)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$npc=[Decennium.Foundation.FrightenedProfile]::Actor
foreach($point in @(@(1,1),@(2,0))){
    $turn=$session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player).TurnId
    Call 'ClericCommit' @($session,$hero,[Decennium.Foundation.CommandKind]::TacticalStep,$turn,$point[0],$point[1],$null)
    Call 'ClericDefender' @($session)
}
$s=Call 'ShortRestCapture' @($session)
$session.Save((Join-Path $run.FullName 'sight-lost.ddsave'))
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$bytes=$codec.Encode($s)
$turn=$session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player).TurnId
$step=[Decennium.Foundation.Command]::new('fear.unseen.approach',$hero,$s.Revision,[Decennium.Foundation.CommandKind]::TacticalStep,$turn,1,1)
$policy=Call 'ClericPolicy' @($session)
$reason=$policy.Resolve($s.Copy(),$step)
$response=$session.Submit([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player,$step).Response
$after=Call 'ShortRestCapture' @($session)
$session.Save((Join-Path $run.FullName 'unseen-approach-denied.ddsave'))
$report=[ordered]@{revision=$s.Revision;visible=[Decennium.Foundation.Laboratory.ObservationRules]::CanSee($s,$hero,$npc);
    frightened=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$hero).View().Has([Decennium.Foundation.Laboratory.ConditionKind]::Frightened);
    reason=$reason;response=$response.ToString();unchanged=[Convert]::ToBase64String($bytes)-eq[Convert]::ToBase64String($codec.Encode($after))}
Call 'ClericCommit' @($session,$hero,[Decennium.Foundation.CommandKind]::Hide,$turn,0,0,$null)
$hidden=Call 'ShortRestCapture' @($session)
$session.Save((Join-Path $run.FullName 'unseen-source-hide-check.ddsave'))
$report.hide=$hidden.ObservationActions[-1]
$report|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $run.FullName 'results.json') -Encoding utf8
$report|ConvertTo-Json -Depth 5 -Compress
