param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SaveRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$policies = @{
    default = $tests.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,$null))
    masterwork = $tests.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]818668))
    mishap = $tests.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]817576))
    flawed = $tests.GetMethod('BatchPolicy',$flags).Invoke($null,@($null,[uint32]99690))
    deferred = $tests.GetMethod('BatchDeferredPolicy',$flags).Invoke($null,@())
    injury = $tests.GetMethod('BatchInjuryPolicy',$flags).Invoke($null,@())
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$worker = [Decennium.Foundation.ConnectedBloodSpecimen]::Worker
function Digest([byte[]]$bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}
$rows = @(foreach ($file in Get-ChildItem -LiteralPath $SaveRoot -Recurse -Filter 'mgt04-connected-batch-*.ddsave' | Sort-Object Name) {
    $mode = switch -Wildcard ($file.BaseName) {
        '*-masterwork-*' { 'masterwork' }
        '*-mishap' { 'mishap' }
        '*-flawed' { 'flawed' }
        '*-awaiting-check' { 'deferred' }
        '*-deferred-check-*' { 'deferred' }
        '*-injur*' { 'injury' }
        default { 'default' }
    }
    $bytes = [IO.File]::ReadAllBytes($file.FullName)
    $digest = Digest $bytes
    $sim = [Decennium.Foundation.Simulation]::new($policies[$mode],$codec.Decode($bytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $s = $sim.Capture()
    if ($s.WireSchemaVersion -ne 95 -or $s.SchemaVersion -ne 90 -or (Digest ($codec.Encode($s))) -cne $digest) {
        throw "Selected save did not restore byte-for-byte: $($file.Name)"
    }
    $batch = $s.ConnectedBatch
    $specimen = $s.BloodSpecimen
    $lot = $s.Work.Lots | Where-Object Id -ceq $specimen.LotId
    $vessel = $s.PortableEquipment | Where-Object Id -ceq $batch.ReturnVesselId
    $item = $s.PortableEquipment | Where-Object Id -ceq $specimen.LotId
    $age = $null
    if (![Decennium.Foundation.HarvestPreservationRules]::TryProject($s,$specimen.LotId,[ref]$age)) {
        throw "No bound age projection in $($file.Name)"
    }
    $job = $s.ManufacturingOrders | Select-Object -First 1
    $facts = [Decennium.Foundation.Laboratory.CharacterStateFacts]::ForActor($s,$worker)
    $int = [Decennium.Foundation.CharacterAbility]::Intelligence
    $doses = @($s.AlchemyDoses | Where-Object Spent)
    $charge = $s.Receipts | Where-Object Revision -eq $batch.ChargeRevision
    $settlement = $s.Receipts | Where-Object Revision -eq $batch.SettlementRevision
    [ordered]@{
        save=$file.Name; sha256=$digest; wire=$s.WireSchemaVersion; base=$s.SchemaVersion; profile=$mode
        clock=$s.RuleClock.ToString(); revision=$s.Revision; rng=$s.RandomState; actor=$worker; workerHp=$facts.Life.Hp
        injuryModifier=$facts.InjuryPenalty($int,$true); intelligence=$facts.Rules.AbilityModifier($int)
        proficiency=$facts.Rules.ProficiencyBonus; lifeEvents=@($s.LifeEvents | Where-Object ActorId -ceq $worker)
        incident=@($s.CraftingIncidents | Select-Object Id,Result,Revision,At,InjuryD4,Damage,WoundD20,InjuryD6,RandomBefore,RandomAfter,WordsConsumed)
        specimen=$lot.Id; amount=$lot.Amount.ToString(); available=$s.Work.AvailableAmount($lot.Id).ToString()
        origin=$specimen.Origin.ToString(); location=$lot.LocationId; custodian=$lot.CustodianId
        portableSpecimen=($null -ne $item); vesselOpen=$vessel.Open
        unprotectedAge=$age.UnprotectedAge.ToString(); preservationState=$age.State.ToString()
        apparatus=$batch.ApparatusId; disposition=$batch.Disposition.ToString()
        chargeRevision=$batch.ChargeRevision; chargeReceipt=$charge.Id; settlementRevision=$batch.SettlementRevision; settlementReceipt=$settlement.Id
        order=if ($job) {
            [ordered]@{id=$job.Id; status=$job.Status.ToString(); starts=$job.StartedAt.ToString(); updated=$job.UpdatedAt.ToString()
                labor=$job.Work.Labor.ToString(); retained=$job.Work.Retained.ToString(); completedPhases=$job.Work.CompletedPhases
                stabilizedAt=if ($null -ne $job.StabilizedAt) {$job.StabilizedAt.ToString()}; quality=$job.Quality.ToString(); natural=$job.Natural
                dice=@($job.First,$job.Second); choice=$job.Choice.ToString(); catalyst=$job.RetainedCatalyst; xp=$job.XpAward
                pendingTarget=if ($s.ManufacturingAdvance) {$s.ManufacturingAdvance.Target.ToString()}
                claims=@($s.Work.Reservations | Where-Object JobId -ceq $job.Id | ForEach-Object {
                    [ordered]@{id=$_.Id;lot=$_.LotId;reserved=$_.Amount.ToString();remaining=$_.RemainingAmount.ToString()
                        consumed=$_.ConsumedAmount.ToString();released=$_.ReleasedAmount.ToString()}
                })}
        }
        doseCount=$s.AlchemyDoses.Length; unusedDoses=$s.AlchemyDoses.Length-$doses.Count
        usedDoses=@($doses | ForEach-Object {
            [ordered]@{id=$_.Id;user=$_.UserId;recipient=$_.RecipientId;time=$_.UsedAt.ToString()
                dice=@($_.FirstD4,$_.SecondD4);potential=$_.PotentialHealing;actual=$_.ActualHealing
                emptyMass=$_.MassPounds.ToString();hp=$_.Hp;owner=$_.OwnerId;custodian=$_.CustodianId;location=$_.LocationId}
        })
        tactical=$s.InventoryCombat; laterEntry=if ($s.LaterEncounter.Entry) {$s.LaterEncounter.Entry.Epoch.Origin.ToString()}
    }
})
if ($rows.Count -ne 22 -or @($rows.save | Sort-Object -Unique).Count -ne 22) {
    throw 'Expected 22 distinct connected batch saves.'
}
@{status='PASS'; savedStates=$rows} | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $OutputPath -Encoding utf8
