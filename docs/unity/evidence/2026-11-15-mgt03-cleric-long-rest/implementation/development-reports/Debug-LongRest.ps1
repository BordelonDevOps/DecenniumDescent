param([string]$AssemblyRoot,[string]$SavePath)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericLongRest([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$session.Restore([IO.Path]::GetFullPath($SavePath))
$flags=[Reflection.BindingFlags]'NonPublic,Instance'
$simulation=$session.GetType().GetField('simulation',$flags).GetValue($session)
$policy=$simulation.GetType().GetField('policy',$flags).GetValue($simulation)
$state=$simulation.Capture()
$wait=[Decennium.Foundation.RuleTime]::new(57600*$state.RuleClock.Denominator-$state.RuleClock.Numerator,$state.RuleClock.Denominator)
$command=[Decennium.Foundation.Command]::new('long-rest.debug.advance',[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero,$state.Revision,[Decennium.Foundation.CommandKind]::AdvanceClock,'',[int]$wait.Numerator,[int]$wait.Denominator)
$authority=$session.GetType().GetField('ClockGrant',[Reflection.BindingFlags]'NonPublic,Static').GetValue($null)
try{$simulation.QueryCommand($authority,$command)|ConvertTo-Json -Depth 5}catch{ $_.Exception.ToString() }
try{$simulation.Execute($authority,$command)|ConvertTo-Json -Depth 5}catch{ $_.Exception.ToString() }
$candidate=$state.Copy()
try{$policy.Resolve($candidate,$command);$candidate.RuleClock.ToString()}catch{ $_.Exception.ToString() }
$state=$simulation.Capture()
$begin=[Decennium.Foundation.Command]::new('long-rest.debug.begin',[Decennium.Foundation.ClericRpProfile]::Actor,$state.Revision,[Decennium.Foundation.CommandKind]::BeginLongRest,[Decennium.Foundation.ClericLongRestProfile]::SiteId,0,0)
$authority=[Decennium.Foundation.Authority]::new('TEST_ONLY.host',[string[]]@([Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero,[Decennium.Foundation.ClericRpProfile]::Actor),$true,$true,$null,$null)
try{$simulation.QueryCommand($authority,$begin)|ConvertTo-Json -Depth 5}catch{ $_.Exception.ToString() }
try{$simulation.Execute($authority,$begin)|ConvertTo-Json -Depth 5}catch{ $_.Exception.ToString() }
try{$policy.Resolve($state,$begin);$policy.ValidateState($state)}catch{ $_.Exception.ToString() }
$state.Revision++
$receipt=[Decennium.Foundation.CommandReceipt]::new();$receipt.Principal='TEST_ONLY.host';$receipt.Id=$begin.Id;$receipt.Fingerprint=$begin.GetType().GetProperty('Fingerprint',$flags).GetValue($begin);$receipt.Revision=$state.Revision
$state.Receipts=[Decennium.Foundation.CommandReceipt[]](@($state.Receipts)+$receipt)
try{[Decennium.Foundation.Validation]::Snapshot($state);'CoreShapePassed'}catch{$_.Exception.ToString()}
try{$policy.ValidateState($state)}catch{$_.Exception.ToString()}
