param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SaveRoot,
    [Parameter(Mandatory)][string]$Output
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$companion = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$files = @(Get-ChildItem -LiteralPath $SaveRoot -Recurse -Filter 'mgt09-connected-research-*.ddsave' -File | Sort-Object Name)
if ($files.Count -eq 0) { throw 'No connected formula research saves found.' }

$states = foreach ($file in $files) {
    $bytes = [IO.File]::ReadAllBytes($file.FullName)
    $s = $codec.Decode($bytes)
    $actor = $s.Actors | Where-Object Id -CEQ $companion
    $facts = [Decennium.Foundation.Laboratory.CharacterStateFacts]::ForActor($s,$companion)
    $intelligence = [Decennium.Foundation.CharacterAbility]::Intelligence
    $modifier = $facts.Rules.AbilityModifier($intelligence) + $facts.Rules.ProficiencyBonus + $facts.InjuryPenalty($intelligence,$true,$false,$false,$false)
    $formula = @($s.FormulaWork | ForEach-Object {
        $job = $_
        [ordered]@{id=$job.Id;worker=$job.WorkerId;recipe=$job.RecipeId;evidence=$job.EvidenceId;method=$job.MethodId
            status=$job.Status.ToString();started=$job.StartedAt.ToString();updated=$job.UpdatedAt.ToString()
            labor=$job.Work.Labor.ToString();retained=$job.Work.Retained.ToString();required=$job.Work.Required.ToString()
            first=$job.First;second=$job.Second;natural=$job.Natural
            bookings=@($s.Work.WorkerIntervals | Where-Object JobId -CEQ $job.Id | ForEach-Object {
                [ordered]@{id=$_.Id;start=$_.Start.ToString();end=$_.End.ToString();worker=$_.WorkerId}
            })}
    })
    $entry = $s.LaterEncounter.Entry
    $admission = $s.Reinforcement.Admission
    [ordered]@{save=$file.Name;sha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
        wire=$s.WireSchemaVersion;base=$s.SchemaVersion;fingerprint=$s.ContentFingerprint
        time=$s.RuleClock.ToString();revision=$s.Revision;rng=$s.RandomState;inventoryCombat=$s.InventoryCombat
        firstEncounterExit=$s.LaterEncounter.FirstExit.ClosedAt.ToString()
        mining=$s.MiningAttempts.Count;havensales=$s.HavenSales.Count;salePayment=$s.HavenSales[0].PaymentCopper
        mealPurchases=$s.HavenMealPurchases.Count;expeditionBills=$s.ExpeditionBills.Count;charter=$s.CharterAttempt.Outcome.ToString()
        companionCell=@($actor.X,$actor.Y);companionOffCalendar=@($s.WorldActivityIntervals | Where-Object ActorId -CEQ $companion).Count -eq 1
        alchemyLevel=($s.Trades | Where-Object TradeId -CEQ 'Alchemy').Level
        researchIntModifier=$modifier;formula=$formula;formulaKnown=[Decennium.Foundation.Laboratory.FormulaResearchRules]::Knows($s,$companion,'recipe-4')
        manufactureOrders=$s.ManufacturingOrders.Count;doses=$s.AlchemyDoses.Count
        stock=@($s.Work.Lots | Where-Object Id -CLike 'manufacture.*' | ForEach-Object {
            [ordered]@{id=$_.Id;unit=$_.UnitId;quantity=$_.Amount.ToString();location=$_.LocationId;custodian=$_.CustodianId}
        })
        hide=$s.ExplorationHide.Attempts.Count;search=$s.ExplorationSearch.Attempts.Count
        closedEncounters=$s.ClosedEncounters.Count
        laterEntry=if ($entry) { [ordered]@{at=$entry.Epoch.Origin.ToString();revision=$entry.ArrivalRevision
            initiative=@($entry.Draws | ForEach-Object { [ordered]@{actor=$_.ActorId;natural=$_.Natural;before=$_.RandomBefore;after=$_.RandomAfter} })} }
        reinforcement=if ($admission) { [ordered]@{at=$admission.Phase.Epoch.Origin.ToString();calendar=$admission.Phase.Epoch.Id
            order=@($admission.Phase.Epoch.Order)} }
    }
}
@{savedStates=@($states)} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $Output -Encoding utf8
