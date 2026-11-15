$ErrorActionPreference='Stop'
$root='engine/artifacts/tac08-cleric-casting/amended-club-build/run-20261115T203320840Z-5def1bd6'
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $root "Decennium.Foundation.$name.dll")}
$t=[Decennium.Foundation.Tests.FoundationCases];$flags=[Reflection.BindingFlags]'NonPublic,Static'
$session=$t.GetMethod('NewCastingExpedition',$flags).Invoke($null,@())
$policy=$t.GetMethod('ClericPolicy',$flags).Invoke($null,@($session))
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$s=$codec.Decode([IO.File]::ReadAllBytes((Join-Path $root 'saves/tac08-club-before-pickup.ddsave')))
$a=[Decennium.Foundation.ClericRpProfile]::Actor
$c=[Decennium.Foundation.Command]::new('inspect.pickup',$a,$s.Revision,[Decennium.Foundation.CommandKind]::HandlePortableEquipment,[Decennium.Foundation.SpellCastingProfile]::CompanionClubId,0,0,[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1)))
[pscustomobject]@{revision=$s.Revision;clock=$s.RuleClock;actor=$s.Actors|Where-Object Id -eq $a;club=$s.Clubs|Where-Object Id -eq $c.Target;burden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($s,$a);failure=$policy.Resolve($s.Copy(),$c)}|ConvertTo-Json -Depth 8
$candidate=$s.Copy();$failure=$policy.Resolve($candidate,$c)
[pscustomobject]@{failure=$failure;clock=$candidate.RuleClock;handling=$candidate.PortableHandling|Select-Object -Last 1;workers=$candidate.Work.WorkerIntervals|Select-Object -Last 1}|ConvertTo-Json -Depth 6
try{[Decennium.Foundation.PortableEquipmentValidation]::Validate($candidate)}catch{ $_.Exception.ToString() }
