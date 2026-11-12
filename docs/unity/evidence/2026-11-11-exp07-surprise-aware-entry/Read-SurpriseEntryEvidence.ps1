param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Read-Save([string]$Name) {
    $path = Join-Path $Saves "exp07-surprise-$Name.ddsave"
    $raw = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $path).Path)
    $sha = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($raw)).ToLowerInvariant()
    [pscustomobject]@{ file=Split-Path -Leaf $path; hash=$sha; state=$codec.Decode($raw) }
}
$continued = Read-Save 'ordinary-continued'
$s = $continued.state
$sale = $s.HavenSales[0]
$meal = $s.HavenMealPurchases[0]
$bill = $s.ExpeditionBills[0]
$agreement = $s.NextCharterAgreement
$charter = $s.CharterAttempt
$heroId = $s.SurpriseEntry.Binding.ParticipantId
$hero = $s.Actors | Where-Object Id -CEQ $heroId
$stepHistory = @(foreach ($stage in 'before-approach','partial','entered','restricted-slot','after-first-end','ordinary-continued') {
    $save = Read-Save $stage
    $state = $save.state
    $first = $state.SurpriseEntry.FirstStart
    $end = $state.SurpriseEntry.FirstEnd
    $arrival = $state.SurpriseEntry.Decision
    $edge = $state.WorldTraversals | Where-Object ActorId -CEQ $heroId
    [ordered]@{stage=$stage;file=$save.file;sha256=$save.hash;revision=$state.Revision;time=$state.RuleClock.ToString()
        rng=$state.RandomState;mode=if($state.InventoryCombat){'tactical'}else{'ordinary'}
        turn=if($state.InventoryCombat){$state.Encounter.CurrentTurnId};partialFeet=if($edge){$edge.DistanceFeet.ToString()}
        decision=if($arrival){$arrival.CommandId};surprisePending=$state.SurpriseEntry.SurprisePending
        firstOrdinal=if($first){$first.Ordinal};end=if($end){$end.At.ToString()};endCommand=if($end){$end.EndCommandId} }
})
[ordered]@{
    authority='TEST_ONLY'
    earlierCombat=[ordered]@{ encounter=$s.ClosedEncounters[0].Encounter.Id; end=$s.ClosedEncounters[0].ClosedAt.ToString()
        revision=$s.ClosedEncounters[0].ClosedRevision }
    acquiredAndSold=[ordered]@{ lot=$sale.Basis.GoodsLotId; appraisal=$sale.Basis.AppraisalId; sale=$sale.Id
        paymentCopper=$sale.PaymentCopper; status=$sale.Status.ToString(); paidAt=$sale.UpdatedAt.ToString() }
    managed=[ordered]@{ meal=$meal.Id; paymentCopper=$meal.PaymentCopper; mealAt=$meal.EndedAt.ToString()
        bill=$bill.Id; status=$bill.Status.ToString(); billAt=$bill.UpdatedAt.ToString()
        priorEpisodeClosedAt=$s.ExpeditionEpisodeClose.ClosedAt.ToString() }
    prepared=[ordered]@{ plan=$agreement.PlanId; assent=$agreement.CommandId; acceptedAt=$agreement.AcceptedAt.ToString()
        charterOutcome=$charter.Outcome.ToString(); returnedAt=$charter.Returned.At.ToString() }
    surpriseStages=$stepHistory
    combatAndContinuation=[ordered]@{ encounter=$s.ClosedEncounters[1].Encounter.Id; combatClosed=$s.ClosedEncounters[1].ClosedAt.ToString()
        realHeroAttacks=@($s.MeleeAttacks | Where-Object { $_.Revision -gt $s.SurpriseEntry.Decision.Revision -and $_.AttackerId -ceq $heroId } |
            Select-Object Id,Revision,TurnOrdinal,TargetId)
        afterOrdinaryMove=$s.RuleClock.ToString(); heroPosition=@($hero.X,$hero.Y); saveSha256=$continued.hash }
} | ConvertTo-Json -Depth 16 | Set-Content -LiteralPath $OutputFile -Encoding utf8
