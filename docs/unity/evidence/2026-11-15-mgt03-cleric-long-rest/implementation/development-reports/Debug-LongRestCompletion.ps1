param([string]$AssemblyRoot,[string]$SavePath,[string]$Run,[int]$Seconds=27800)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericLongRest([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$session.Restore([IO.Path]::GetFullPath($SavePath))
$simulation=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'NonPublic,Instance').GetValue($session)
$before=$simulation.Capture()
$command=[Decennium.Foundation.Command]::new('long-rest.debug.complete',[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero,$before.Revision,[Decennium.Foundation.CommandKind]::AdvanceClock,'',$Seconds,1)
$authority=$session.GetType().GetField('ClockGrant',[Reflection.BindingFlags]'NonPublic,Static').GetValue($null)
$result=$simulation.Execute($authority,$command);$s=$simulation.Capture()
$report=[ordered]@{scope='Development diagnostic on genuine pending rest';result=$result;clock=$s.RuleClock.ToString();settlements=$s.ClericLongRestSettlements;conviction=$s.ConvictionBalance;daily=$s.DailyProvisioningSettlements;watch=$s.RestWatchOutcomes;beneficial=$s.ExpeditionBeneficialRests;randomBefore=$before.RandomState;randomAfter=$s.RandomState}
New-Item -ItemType Directory -Path $Run | Out-Null
$report | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $Run 'result.json')
$session.Save([IO.Path]::GetFullPath((Join-Path $Run 'complete.ddsave')))
$report | ConvertTo-Json -Depth 7

if($result.Code -ne 'Committed') {
 $candidate=$before.Copy();$flags=[Reflection.BindingFlags]'NonPublic,Instance';$policy=$simulation.GetType().GetField('policy',$flags).GetValue($simulation)
 try {
  'Resolve='+$policy.Resolve($candidate,$command)
  $candidate.Revision++
  $receipt=[Decennium.Foundation.CommandReceipt]::new();$receipt.Principal=$authority.Principal;$receipt.Id=$command.Id;$receipt.Fingerprint=$command.GetType().GetProperty('Fingerprint',$flags).GetValue($command);$receipt.Revision=$candidate.Revision
  $candidate.Receipts=[Decennium.Foundation.CommandReceipt[]](@($candidate.Receipts)+$receipt)
  [Decennium.Foundation.Validation]::Snapshot($candidate);'CoreShapePassed';$policy.ValidateState($candidate)
 } catch { $_.Exception.ToString() }
}
