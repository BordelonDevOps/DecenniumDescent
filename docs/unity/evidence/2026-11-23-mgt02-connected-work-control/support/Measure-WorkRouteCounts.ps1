param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Save,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$s=[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path $Save).Path)
$rows=@(
 @{name='receipts';count=$s.Receipts.Length;limit=512},@{name='resource lots';count=$s.Work.Lots.Count;limit=128},
 @{name='worker bookings';count=$s.Work.WorkerIntervals.Count;limit=128},@{name='resource reservations';count=$s.Work.Reservations.Count;limit=128},
 @{name='water fills';count=$s.WaterFills.Length;limit=32},@{name='vessels';count=$s.Vessels.Length;limit=8},@{name='vessel contents';count=$s.VesselContents.Length;limit=128},
 @{name='mining attempts';count=$s.MiningAttempts.Length;limit=64},@{name='formula work';count=$s.FormulaWork.Length;limit=32},
 @{name='manufacturing orders';count=$s.ManufacturingOrders.Length;limit=16},@{name='alchemy doses';count=$s.AlchemyDoses.Length;limit=112})
foreach($j in @($s.FormulaWork)+@($s.ManufacturingOrders)){$rows+=@{name=('phases:'+ $j.Id);count=$j.Work.Phases.Count;limit=64}}
foreach($r in $rows){if($r.count-gt$r.limit){throw "Exceeded $($r.name)"};$r.headroom=$r.limit-$r.count}
@{status='PASS';revision=$s.Revision;saveSha256=(Get-FileHash $Save).Hash.ToLowerInvariant();rows=$rows;scope='Existing work-family cap inventory enumerated by WC-04/05; counts read from actual final244 save. Not new caps or all unrelated subsystem limits.'}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath $Output
Write-Output "PASS: $Output"
