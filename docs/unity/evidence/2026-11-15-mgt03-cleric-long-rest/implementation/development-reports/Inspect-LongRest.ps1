param([string]$AssemblyRoot,[string]$SavePath)
foreach($part in 'Core','Persistence'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$s=[Decennium.Foundation.SnapshotCodec]::new().Decode([IO.File]::ReadAllBytes([IO.Path]::GetFullPath($SavePath)))
[pscustomobject]@{Clock=$s.RuleClock.ToString();Revision=$s.Revision;Strain=$s.ExpeditionStrainGains;Daily=$s.DailyProvisioningSettlements;Rests=$s.ClericLongRests;Casting=$s.CastingStrain}|ConvertTo-Json -Depth 5
