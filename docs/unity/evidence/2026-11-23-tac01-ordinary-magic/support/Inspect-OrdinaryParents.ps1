param([string]$AssemblyRoot,[string]$OutputPath)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$root='engine/artifacts/ordinary-magic-qualification/candidate-02'
$paths=@(Get-ChildItem -LiteralPath "$root/c1" -Filter '*.ddsave' -Recurse)+@(Get-Item -LiteralPath "$root/five-paths-01/ConsoleRestored/r351.ddsave","$root/five-paths-01/ConsoleRestored/r436.ddsave")
$rows=foreach($p in $paths){$s=[Decennium.Foundation.FileSaveStore]::new().Load($p.FullName);[ordered]@{path=$p.FullName;revision=$s.Revision;clock=$s.RuleClock;encounter=$s.Encounter;actors=$s.Actors;lives=$s.Lives;intervals=$s.WorldIntervals;allowance=$s.OrdinaryMagic.Current;recharge=$s.AbilityRecharges;known=$s.KnownSpells;rp=$s.ResonancePools;strain=$s.CastingStrain;stances=$s.Stances}}
$rows|ConvertTo-Json -Depth 15|Set-Content -LiteralPath $OutputPath
