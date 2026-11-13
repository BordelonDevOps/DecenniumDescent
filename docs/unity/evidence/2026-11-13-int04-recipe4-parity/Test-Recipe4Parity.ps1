param([Parameter(Mandatory)][string]$Run)

$ErrorActionPreference = 'Stop'
$Run = (New-Item -ItemType Directory -Path $Run).FullName
$root = (Resolve-Path "$PSScriptRoot/../../../..").Path
$prior = (Resolve-Path "$PSScriptRoot/../2026-11-13-int03-strict-restoration").Path
$fixture = (Resolve-Path "$PSScriptRoot/../2026-11-12-int03-connected-session/correction/walkthrough.jsonl").Path
$accepted = Get-Content "$prior/regression/results.json" -Raw | ConvertFrom-Json -AsHashtable
$provenance = Get-Content "$prior/regression/shardA.execution.json" -Raw | ConvertFrom-Json -AsHashtable
$engine = '75872e1e01fea9b17fce0c5c6c34d56679848961'
$hero = 'TEST_ONLY.actor'
$worker = 'TEST_ONLY.companion'
$orderId = 'manufacture.order.104'
$blood = 'manufacture.recipe14.set0.component2'
$packaging = 'manufacture.glass-vials'
$parts = [ordered]@{'manufacture.set0.component0'=5; 'manufacture.set0.component1'=5
    'manufacture.set0.component2'=5; $blood=1; $packaging=2}
$marks = 103,104,105,106,107,113,114,115,163,164,165
$checks = [Collections.Generic.List[object]]::new()
$branch = 'Provenance'
$report = [ordered]@{Status='RUNNING'; Source=$engine; RunId=[guid]::NewGuid().ToString('N'); PID=$PID
    StartedUtc=[DateTime]::UtcNow.ToString('o'); OS=[Runtime.InteropServices.RuntimeInformation]::OSDescription
    PowerShell=$PSVersionTable.PSVersion.ToString(); Runtime=[Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
    Loaded=[ordered]@{}; Branches=[ordered]@{}; SelfChecks=@()}

function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Json($data) { ConvertTo-Json -InputObject $data -Depth 12 -Compress -EnumsAsStrings }
function Assert($name,$expected,$actual) {
    $ok = (Json $expected) -ceq (Json $actual)
    $checks.Add([ordered]@{Branch=$branch; Name=$name; Expected=$expected; Actual=$actual; Passed=$ok})
    if (!$ok) { throw "$branch / $name expected $(Json $expected), got $(Json $actual)" }
}
function Fields($prefix,$expected,$actual) {
    foreach ($key in $expected.Keys) { Assert "$prefix $key" $expected[$key] $actual[$key] }
}
function Single($rows,$label) {
    Assert "$label count" 1 @($rows).Count
    @($rows)[0]
}
function Quantity($q) {
    if ($q.Denominator -ne 1) { throw "Expected a whole quantity, got $q" }
    $q.Numerator
}
function Lot($state,$id) { Single @($state.Work.Lots | Where-Object Id -CEQ $id) "lot $id" }
function Life($state) { Single @($state.Lives | Where-Object ActorId -CEQ $hero) 'hero life' }
function Action-Spent($state) { (Single @($state.WorldIntervals | Where-Object ActorId -CEQ $hero) 'hero interval').ActionSpent }
function Own-Actor($view,$id) { Single @($view.Actors | Where-Object { $_.Position.Id -ceq $id }) "view for $id" }

function Draw-Vector([uint64]$word,[int]$sides) {
    # Independent transcription of xorshift32-v1 and the nonzero bounded mapping.
    $mask = [uint64]4294967295
    $limit = $mask - ($mask % $sides)
    $words = 0
    do {
        $word = ($word -bxor ($word -shl 13)) -band $mask
        $word = ($word -bxor ($word -shr 17)) -band $mask
        $word = ($word -bxor ($word -shl 5)) -band $mask
        $words++
    } while ($word - 1 -ge $limit)
    [ordered]@{Face=[int](($word - 1) % $sides + 1); Word=$word; Words=$words}
}

function Capture-Checkpoint($game,$name) {
    $file = Join-Path $folder "$name.ddsave"
    $game.Save($file)
    $state = $codec.Decode([IO.File]::ReadAllBytes($file))
    $view = $game.View('Player')
    Assert "$name permitted revision and clock" @($state.Revision,$state.RuleClock.ToString()) @($view.Revision,$view.Clock.ToString())
    [ordered]@{File=$file; Hash=(Digest $file); State=$state; View=$view}
}
function View-Record($view) {
    $record = $view | Select-Object * -ExcludeProperty KnownTargets
    $targets = [ordered]@{}
    foreach ($pair in $view.KnownTargets.GetEnumerator() | Sort-Object Key) { $targets[$pair.Key.ToString()] = $pair.Value }
    $record | Add-Member NoteProperty KnownTargets $targets
    $record
}
function Log($request,$result) {
    if ($result -is [Decennium.Foundation.Laboratory.ExpeditionSeatView]) { $result = View-Record $result }
    Add-Content -LiteralPath $journal -Value (Json @{Input=$request; Observed=$result}) -Encoding utf8
}
function Submit-Input($game,$request) {
    switch ($request.op) {
        'view' { $game.View(($request.seat ?? 'Player')); break }
        'auto' { $game.AdvanceAutomaticDefender(); break }
        'submit' {
            $seat = $request.seat ?? 'Player'
            $game.Submit($seat,(New-SessionCommand $request ($game.View($seat)) $request.kind))
            break
        }
        { $_ -in 'clock','close' } {
            $commandInput = [ordered]@{} + $request
            $commandInput.actor = $hero
            $kind = if ($_ -eq 'clock') { 'AdvanceClock' } else { 'EndFixedEncounter' }
            $game.SubmitSessionCommand((New-SessionCommand $commandInput ($game.View('Player')) $kind))
            break
        }
        default { throw "Unexpected operation $($request.op)" }
    }
}
function Restore-Checkpoint($checkpoint,$revision) {
    $next = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
    $next.Restore($checkpoint.File)
    $loaded = Capture-Checkpoint $next "r$revision-restored"
    Assert "r$revision restored bytes" $checkpoint.Hash $loaded.Hash
    Assert "r$revision restored pending identity" @($checkpoint.View.PendingDecision.ToString(),$checkpoint.View.DecisionId) @(
        $loaded.View.PendingDecision.ToString(),$loaded.View.DecisionId)
    Log @{op='restore'; checkpoint=$revision} @{Response='Restored'; Sha256=$loaded.Hash}
    Log @{op='view'; checkpoint="$revision restored"; seat='Player'} $loaded.View
    $next
}
function Assert-Unchanged($game,$name,$priorState,$request,$expectedResponse) {
    $result = Submit-Input $game $request
    Log $request $result
    $after = Capture-Checkpoint $game $name
    Assert "$name response/revision/clock" @($expectedResponse,$priorState.State.Revision,$priorState.State.RuleClock.ToString()) @(
        $result.Response.ToString(),$result.Revision,$result.Clock.ToString())
    Assert "$name complete canonical bytes" $priorState.Hash $after.Hash
    Assert "$name receipt count and RNG" @($priorState.State.Receipts.Length,$priorState.State.RandomState) @(
        $after.State.Receipts.Length,$after.State.RandomState)
    Assert "$name permitted view" (Json (View-Record $priorState.View)) (Json (View-Record $after.View))
}

function Verify-Manufacturing($states,$choice) {
    $initial = $states[103].State
    $charged = $states[104].State
    $phase = $states[105].State
    $pending = $states[106].State
    $settled = $states[107].State
    $facts = [ordered]@{Orders=[ordered]@{}; Claims=[ordered]@{}}
    $character = Single @($initial.Characters | Where-Object ActorId -CEQ $worker) 'crafter'
    $research = Single @($initial.FormulaWork | Where-Object { $_.WorkerId -ceq $worker -and $_.RecipeId -ceq 'recipe-4' }) 'recipe research'
    $trade = Single @($initial.Trades | Where-Object WorkerId -CEQ $worker) 'starting trade'
    $int = [int][Math]::Floor(($character.Abilities[3] - 10) / 2)
    $pb = 2 + [int][Math]::Floor(($character.Levels.Count - 1) / 4)
    $workerView = Own-Actor $states[103].View $worker
    $workerLife = Single @($phase.Lives | Where-Object ActorId -CEQ $worker) 'crafter at pre-check'
    $preCheckWorker = Own-Actor $states[105].View $worker
    $tool = Single @($initial.Structures | Where-Object Id -CEQ 'craft.alchemist-kit') 'physical Alchemist supplies'
    $station = Single @($initial.CropPlots | Where-Object Id -CEQ 'TEST_ONLY.prepared-plot') 'selected workshop'
    Assert 'qualified worker has intact tool at owned workshop' @(
        'tools.alchemist-s-supplies',$worker,$worker,$station.Id,$worker,$false
    ) @($tool.ProfileId,$tool.OwnerId,$tool.CustodianId,$tool.LocationId,$station.OwnerId,$tool.Broken)
    Assert 'working pre-check has no injury penalty or disadvantage' @(0,$false,0) @(
        $workerLife.LinkedInjuries.Count,($preCheckWorker.Conditions -contains 'Poisoned'),$phase.CraftingIncidents.Length)
    Assert 'qualified first nontrivial craft fixture' @(0,2,'Success',$true,$false,$false) @(
        $int,$pb,$research.Status.ToString(),($trade.Level -ge 5 -and $trade.Level -lt 10),
        ($trade.SuccessfulRecipes -contains 'recipe-4'),($workerView.Conditions -contains 'Poisoned'))
    Assert 'no prior order or dose' @(0,0) @($initial.ManufacturingOrders.Length,$initial.AlchemyDoses.Length)
    $specimen = Lot $initial $blood
    $vessel = Single @($initial.PortableEquipment | Where-Object Id -CEQ $initial.BloodSpecimen.VesselId) 'specimen vessel'
    Assert 'actual whole open specimen' @($blood,$vessel.Id,1,$true) @(
        $initial.BloodSpecimen.LotId,$specimen.LocationId,(Quantity $specimen.Amount),$vessel.Open)
    Assert 'worker is physically at the open specimen and workshop' $true (
        $vessel.Placement -eq 'Ground' -and $vessel.GroundX -eq 3 -and $vessel.GroundY -eq 3 -and
        [Math]::Max([Math]::Abs($workerView.Position.X - 3),[Math]::Abs($workerView.Position.Y - 3)) -le 1 -and
        @($initial.WorldTraversals | Where-Object ActorId -CEQ $worker).Count -eq 0)
    $booked = Single @($charged.Work.WorkerIntervals | Where-Object JobId -CEQ $orderId) 'work booking'
    Assert 'exclusive work booking' @($worker,'42248/1','56648/1') @($booked.WorkerId,$booked.Start.ToString(),$booked.End.ToString())
    $apparatus = Single @($charged.PortableEquipment | Where-Object Id -CEQ 'TEST_ONLY.recipe4.bench-apparatus.v1') 'apparatus'
    Assert 'same specimen charged into selected closed apparatus' @(
        $apparatus.Id,'Charged',$false,'Ground',3,3,'TEST_ONLY.recipe4.closed-processing.v1',$blood
    ) @((Lot $charged $blood).LocationId,$charged.ConnectedBatch.Disposition.ToString(),$apparatus.Open,
        $apparatus.Placement.ToString(),$apparatus.GroundX,$apparatus.GroundY,$apparatus.ProfileId,$apparatus.FitMemberIds[0])
    $facts.Fixture = @{Research=$research; Trade=$trade; Intelligence=$character.Abilities[3]; Level=$character.Levels.Count
        Modifier=$int; Proficiency=$pb; Worker=$workerView; PreCheckWorker=$preCheckWorker; WorkerLife=$workerLife
        Tool=$tool; Station=$station; Specimen=$specimen; Vessel=$vessel; Apparatus=$apparatus; Booking=$booked}
    $expectedLabor = @{
        104=@('42248/1','0/1',0,'Working',$null)
        105=@('43148/1','900/1',1,'Working','43148/1')
        106=@('56648/1','14400/1',2,'AwaitingChoice','43148/1')
        107=@('56648/1','14400/1',2,'Complete','43148/1')
    }
    foreach ($revision in 104..107) {
        $state = $states[$revision].State
        $order = Single $state.ManufacturingOrders "r$revision order"
        Assert "r$revision exact order" @($orderId,'recipe-4',$worker,0,2,$false) @(
            $order.Id,$order.RecipeId,$order.WorkerId,$order.MaterialSet,$order.ExtraVials,$order.TakeTen)
        $stabilized = if ($null -ne $order.StabilizedAt) { $order.StabilizedAt.ToString() }
        Assert "r$revision active work and stabilization" $expectedLabor[$revision] @(
            $state.RuleClock.ToString(),$order.Work.Labor.ToString(),$order.Work.CompletedPhases,$order.Status.ToString(),$stabilized)
        Assert "r$revision phases and partial" @('900/1','13500/1','0/1') @(
            $order.Work.Phases[0].ToString(),$order.Work.Phases[1].ToString(),$order.Work.Partial.ToString())
        if ($revision -le 105) {
            Assert "r$revision no premature quality draw" @(0,0,0,'None',$initial.RandomState) @(
                $order.First,$order.Second,$order.Natural,$order.Quality.ToString(),$state.RandomState)
        }
        if ($revision -le 106) { Assert "r$revision no premature output" 0 $state.AlchemyDoses.Length }
        $facts.Orders["r$revision"] = $order
        $actualClaims = @($state.Work.Reservations | Where-Object JobId -CEQ $orderId)
        Assert "r$revision exactly five claims" 5 $actualClaims.Length
        $facts.Claims["r$revision"] = foreach ($id in $parts.Keys) {
            $claim = Single @($actualClaims | Where-Object LotId -CEQ $id) "r$revision claim $id"
            $baseLot = Lot $initial $id
            $actualLot = Lot $state $id
            $consumed = 0
            $released = 0
            if ($revision -eq 107) {
                $consumed = if ($id -ceq $packaging) { [int]($choice -ceq 'FullYield') } else { $parts[$id] }
                $released = $parts[$id] - $consumed
            }
            $remaining = $parts[$id] - $consumed - $released
            $baselineAvailable = Quantity ($initial.Work.AvailableAmount($id))
            $available = Quantity ($state.Work.AvailableAmount($id))
            Fields "r$revision $id" ([ordered]@{Reserved=$parts[$id]; Consumed=$consumed; Released=$released
                Remaining=$remaining; Physical=((Quantity $baseLot.Amount) - $consumed)
                Available=($baselineAvailable - $consumed - $remaining)}) ([ordered]@{
                Reserved=(Quantity $claim.Amount); Consumed=(Quantity $claim.ConsumedAmount); Released=(Quantity $claim.ReleasedAmount)
                Remaining=(Quantity $claim.RemainingAmount); Physical=(Quantity $actualLot.Amount); Available=$available})
            @{Claim=$claim; Before=$baseLot; After=$actualLot; BeforeAvailable=$baselineAvailable; AfterAvailable=$available}
        }
    }
    $draw = Draw-Vector $phase.RandomState 20
    $margin = $draw.Face + $int + $pb - 8
    Assert 'independent Exceptional margin' $true ($margin -ge 5 -and $margin -le 9)
    $quality = $pending.ManufacturingOrders[0]
    Assert 'single d20 quality check and RNG' @($draw.Face,0,$draw.Face,'Exceptional',$draw.Word) @(
        $quality.First,$quality.Second,$quality.Natural,$quality.Quality.ToString(),$pending.RandomState)
    Assert 'actual quality pending and then resolved' @('ManufacturingQuality',$orderId,'None') @(
        $states[106].View.PendingDecision.ToString(),$states[106].View.DecisionId,$states[107].View.PendingDecision.ToString())
    Assert 'native choice, specimen disposition and no draw' @($choice,'Consumed',107,$pending.RandomState) @(
        $settled.ManufacturingOrders[0].Choice.ToString(),$settled.ConnectedBatch.Disposition.ToString(),
        $settled.ConnectedBatch.SettlementRevision,$settled.RandomState)
    $count = if ($choice -ceq 'FullYield') { [int][Math]::Floor(5 * 125 / 100) } else { 5 }
    $hp = if ($choice -ceq 'FullYield') { 1 } else { 2 }
    $tradeAfter = Single @($settled.Trades | Where-Object WorkerId -CEQ $worker) 'settled trade'
    $extra = Single @($settled.Work.Reservations | Where-Object { $_.JobId -ceq $orderId -and $_.LotId -ceq $packaging }) 'settled packaging'
    $expected = [ordered]@{Yield=$count; PackagingConsumed=[int]($choice -ceq 'FullYield'); Xp=4}
    $observed = [ordered]@{Yield=$settled.AlchemyDoses.Length; PackagingConsumed=(Quantity $extra.ConsumedAmount); Xp=($tradeAfter.Xp - $trade.Xp)}
    Fields 'settlement' $expected $observed
    Assert 'one successful recipe identity and one XP award' @(1,4) @(
        @($tradeAfter.SuccessfulRecipes | Where-Object { $_ -ceq 'recipe-4' }).Count,$settled.ManufacturingOrders[0].XpAward)
    foreach ($i in 0..($count - 1)) {
        $id = "$orderId.dose$i"
        $dose = Single @($settled.AlchemyDoses | Where-Object Id -CEQ $id) $id
        Assert "$id finite output identity" @($orderId,'recipe-4',$worker,$worker,$worker,'TEST_ONLY.prepared-plot','56648/1',$hp,$hp,'1/5',$false) @(
            $dose.OrderId,$dose.RecipeId,$dose.MakerId,$dose.OwnerId,$dose.CustodianId,$dose.LocationId,$dose.CreatedAt.ToString(),
            $dose.MaximumHp,$dose.Hp,$dose.MassPounds.ToString(),$dose.Spent)
    }
    $facts.Quality = @{BeforeRng=$phase.RandomState; Vector=$draw; Margin=$margin; ActualRng=$pending.RandomState}
    $facts.Output = $settled.AlchemyDoses
    $facts.Trade = $tradeAfter
    $facts.Expected = $expected
    $facts.Observed = $observed
    $facts
}


function Verify-DoseAndTravel($states) {
    $settled = $states[107].State
    $before = $states[114].State
    $used = $states[115].State
    $life = Life $before
    $visible = Own-Actor $states[114].View $hero
    $position = $visible.Position
    $hands = 2 - @($before.Clubs | Where-Object HeldBy -CEQ $hero).Count
    foreach ($weapon in $before.RepeatingCrossbows | Where-Object HeldBy -CEQ $hero) { $hands -= $weapon.GripHands }
    foreach ($item in $before.PortableEquipment | Where-Object { $_.CustodianId -ceq $hero -and $_.ParentId -ceq '' }) {
        if ($item.Placement -eq 'Carried') { $hands -= $item.HeldHands }
        if ($item.Placement -eq 'Worn' -and $item.ProfileId -ceq 'armor-and-shields.shield') { $hands-- }
    }
    Assert 'actual automatic opportunity and pre-use health' @('Opportunity','None',26,23,26) @(
        $states[113].View.PendingDecision.ToString(),$states[114].View.PendingDecision.ToString(),
        (Life $states[113].State).Hp,$life.Hp,$life.MaximumHp)
    Assert 'legal living own-turn user near bench with free hand' $true (
        $before.InventoryCombat -and $before.Encounter.CurrentActor -ceq $hero -and $hands -ge 1 -and !$life.Dead -and
        [Math]::Max([Math]::Abs($position.X - 3),[Math]::Abs($position.Y - 3)) -le 1 -and
        @($before.WorldTraversals | Where-Object ActorId -CEQ $hero).Count -eq 0)
    $heroApplications = @($before.Conditions | Where-Object Target -CEQ $hero | ForEach-Object Operations |
        Where-Object Kind -EQ 'Apply')
    Assert 'no injury cap or disabling public condition' @(0,0,0) @($life.LinkedInjuries.Count,$heroApplications.Count,@($visible.Conditions | Where-Object {
        $_ -in 'Incapacitated','Paralyzed','Petrified','Poisoned','Staggered','Stunned','Unconscious'
    }).Count)
    Assert 'action unspent before use' $false (Action-Spent $before)
    Assert 'pre-use custody and doses match settlement' (Json $settled.AlchemyDoses) (Json $before.AlchemyDoses)
    $id = "$orderId.dose0"
    $dose = Single @($before.AlchemyDoses | Where-Object Id -CEQ $id) 'available dose'
    $vial = Single @($used.AlchemyDoses | Where-Object Id -CEQ $id) 'spent vial'
    $first = Draw-Vector $before.RandomState 4
    $second = Draw-Vector $first.Word 4
    $potential = $first.Face + $second.Face + 2
    $actual = [Math]::Min($potential,$life.MaximumHp - $life.Hp)
    $expected = [ordered]@{First=$first.Face; Second=$second.Face; Potential=$potential; Actual=$actual
        EndRng=$second.Word; Action=$true; VialMass='1/10'; Hp=($life.Hp + $actual)}
    $observed = [ordered]@{First=$vial.FirstD4; Second=$vial.SecondD4; Potential=$vial.PotentialHealing; Actual=$vial.ActualHealing
        EndRng=$used.RandomState; Action=(Action-Spent $used); VialMass=$vial.MassPounds.ToString(); Hp=(Life $used).Hp}
    Fields 'dose' $expected $observed
    Assert 'spent vial identity, custody, provenance and structural HP' @(
        $dose.Id,$dose.OrderId,$dose.RecipeId,$dose.MakerId,$dose.OwnerId,$dose.CustodianId,
        $dose.LocationId,$dose.CreatedAt.ToString(),$dose.MaximumHp,$dose.Hp,$hero,$hero,$used.RuleClock.ToString()
    ) @($vial.Id,$vial.OrderId,$vial.RecipeId,$vial.MakerId,$vial.OwnerId,$vial.CustodianId,
        $vial.LocationId,$vial.CreatedAt.ToString(),$vial.MaximumHp,$vial.Hp,$vial.UserId,$vial.RecipientId,$vial.UsedAt.ToString())
    Assert 'exactly one spent dose' 1 @($used.AlchemyDoses | Where-Object Spent).Count
    $siblings = @($before.AlchemyDoses | Where-Object Id -CNE $id)
    Assert 'other doses unchanged' (Json $siblings) (Json @($used.AlchemyDoses | Where-Object Id -CNE $id))
    $sibling = Single @($siblings | Where-Object Id -CEQ "$orderId.dose1") 'sibling for same-turn rejection'
    $usedView = Own-Actor $states[115].View $hero
    Assert 'same-turn sibling otherwise available and reachable' $true (
        !$sibling.Spent -and $sibling.Hp -gt 0 -and $sibling.LocationId -ceq $vial.LocationId -and
        $sibling.CustodianId -ceq $vial.CustodianId -and $used.Encounter.CurrentActor -ceq $hero -and
        $used.Encounter.CurrentTurnId -ceq $before.Encounter.CurrentTurnId -and
        $usedView.Position.X -eq $position.X -and $usedView.Position.Y -eq $position.Y -and
        (Json $usedView.HeldItems) -ceq (Json $visible.HeldItems))
    Assert 'no condition or injury cure' (Json @($visible.Conditions,$life.LinkedInjuries)) (
        Json @($usedView.Conditions,(Life $used).LinkedInjuries))
    $closed = $states[163].State
    $walking = $states[164].State
    $final = $states[165].State
    $from = (Own-Actor $states[163].View $hero).Position
    $to = (Own-Actor $states[165].View $hero).Position
    Assert 'ordinary continuation outside encounter' @($false,$false,$false) @($closed.InventoryCombat,$walking.InventoryCombat,$final.InventoryCombat)
    Assert 'actual pending ordinary walk' 1 @($walking.WorldTraversals | Where-Object ActorId -CEQ $hero).Count
    Assert 'six seconds and one paid square' @('113403/2','113403/2','113415/2',$from.X,($from.Y - 1)) @(
        $closed.RuleClock.ToString(),$walking.RuleClock.ToString(),$final.RuleClock.ToString(),$to.X,$to.Y)
    Assert 'finite dose history survives travel' (Json $used.AlchemyDoses) (Json $final.AlchemyDoses)
    Assert 'trade history survives travel' (Json $settled.Trades) (Json $final.Trades)
    Assert 'order history survives travel' (Json $settled.ManufacturingOrders) (Json $final.ManufacturingOrders)
    [ordered]@{BeforeRng=$before.RandomState; FirstVector=$first; SecondVector=$second
        Expected=$expected; Observed=$observed; Before=$dose; After=$vial; Siblings=$siblings
        FreeHands=$hands; Actor=$visible; ConditionApplications=$heroApplications; Travel=@{From=$from; To=$to; ElapsedSeconds=6}}
}

function Invoke-Scenario($name,$choice,[bool]$restoreQuality,[bool]$restoreOpportunity) {
    $branch = $name
    $folder = (New-Item -ItemType Directory -Path (Join-Path $Run $name)).FullName
    $journal = Join-Path $folder 'operations.jsonl'
    $game = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
    $states = @{}
    $hashes = [ordered]@{}
    $revision = 0
    foreach ($line in [IO.File]::ReadLines($fixture)) {
        $request = ConvertFrom-Json -AsHashtable $line
        if ($request.op -in 'save','load') { continue }
        if ($choice -ceq 'Durability' -and $request.kind -ceq 'ResolveManufacturingQuality') { $request.x = 2 }
        $result = Submit-Input $game $request
        Log $request $result
        if ($request.op -eq 'view') {
            Assert 'fixture view response type' $true ($result -is [Decennium.Foundation.Laboratory.ExpeditionSeatView])
            continue
        }
        $revision++
        Assert "r$revision public input commits" @('Committed',$revision) @($result.Response.ToString(),$result.Revision)
        if ($revision -notin $marks) { continue }
        $mark = Capture-Checkpoint $game "r$revision"
        $states[$revision] = $mark
        $hashes["r$revision"] = @{Sha256=$mark.Hash; Clock=$mark.State.RuleClock.ToString()}
        Assert "r$revision exact profile and schema" @(
            'TEST_ONLY.recipe4-batch-v1-8e3fd0fe4005207e90bffc01cd900efddcfd6e976e7aab4b46000d64d50c4d01',95,90
        ) @($mark.State.ContentFingerprint,$mark.State.WireSchemaVersion,$mark.State.SchemaVersion)
        Log @{op='view'; checkpoint=$revision; seat='Player'} $mark.View
        if (($revision -eq 106 -and $restoreQuality) -or ($revision -eq 113 -and $restoreOpportunity)) {
            $game = Restore-Checkpoint $mark $revision
        }
        if ($choice -ceq 'FullYield' -and $revision -in 107,115) {
            Assert-Unchanged $game "r$revision-duplicate" $mark $request 'Duplicate'
        }
        if ($choice -ceq 'FullYield' -and $revision -eq 115) {
            $sibling = [ordered]@{} + $request
            $sibling.id = 'int04.sibling-dose-after-action'
            $sibling.revision = 115
            $sibling.target = "$orderId.dose1"
            Assert-Unchanged $game 'r115-sibling-rejected' $mark $sibling 'Unavailable'
        }
    }
    Assert 'all committed commands' 165 $revision
    Assert 'all named checkpoints' $marks @($states.Keys | Sort-Object)
    $manufacturing = Verify-Manufacturing $states $choice
    $dose = Verify-DoseAndTravel $states
    [ordered]@{Status='PASS'; Choice=$choice; RestoredQuality=$restoreQuality; RestoredOpportunity=$restoreOpportunity
        Checkpoints=$hashes; OperationsSha256=(Digest $journal); Manufacturing=$manufacturing; Dose=$dose}
}

try {
    $report.FixtureSha256 = Digest $fixture
    Assert 'pinned input bytes' 'd258bb4b36ae18b26f1f5c2db85fc879e1519aaecf8b703bdfb8b00b131b1a43' $report.FixtureSha256
    Assert 'exact engine tree' (git -C $root rev-parse "${engine}:engine") (git -C $root rev-parse 'HEAD:engine')
    git -C $root diff --quiet HEAD -- engine
    Assert 'engine worktree clean' 0 $LASTEXITCODE
    Assert 'predecessor suite binding' @($engine,1489,1489,0) @(
        $accepted.implementationCommit,$accepted.testsDiscovered,$accepted.passed,$accepted.failed)
    Assert 'predecessor inventory binding' $provenance.inventorySha256 (Digest "$prior/regression/inventory.txt")
    $report.VerifierSha256 = Digest $PSCommandPath
    $report.SourceArchiveSha256 = $accepted.sourceArchiveSha256
    $report.Predecessor = @{Commit='5d79ebf258197ca671677a0bee532ad18246ca47'; Tests=1489
        ReportSha256=(Digest "$prior/regression/results.json"); InventorySha256=$provenance.inventorySha256; Assemblies=$accepted.executedAssemblies}
    $assemblyRoot = (Resolve-Path "$prior/assemblies").Path
    foreach ($name in 'Core','Persistence','LabModel') {
        $dll = "Decennium.Foundation.$name.dll"
        $file = Join-Path $assemblyRoot $dll
        Assert "$dll accepted digest" $accepted.executedAssemblies[$dll].sha256 (Digest $file)
        $assembly = [Reflection.Assembly]::LoadFrom($file)
        Assert "$dll actual loaded path" $file $assembly.Location
        Assert "$dll actual loaded module" $provenance.assemblies[$dll].moduleId $assembly.ManifestModule.ModuleVersionId.ToString()
        $report.Loaded[$dll] = @{Path=$assembly.Location; Sha256=(Digest $assembly.Location)
            ModuleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
    }
    $codec = [Decennium.Foundation.SnapshotCodec]::new()
    # Reuse the public input adapter's command constructor. Direct calls below
    # preserve exceptions rather than treating them as an Unavailable response.
    $empty = New-Item -ItemType File -Path (Join-Path $Run 'empty.jsonl')
    . (Join-Path $root 'engine/tools/Open-ConnectedExpedition.ps1') -AssemblyRoot $assemblyRoot -InputPath $empty.FullName
    $report.Branches.Uninterrupted = Invoke-Scenario 'Uninterrupted' 'FullYield' $false $false
    $report.Branches.Restored = Invoke-Scenario 'Restored' 'FullYield' $true $true
    $report.Branches.Durability = Invoke-Scenario 'Durability' 'Durability' $true $false
    $branch = 'Comparison'
    foreach ($mark in 'r107','r115','r165') {
        Assert "$mark Full Yield restored and uninterrupted" $report.Branches.Uninterrupted.Checkpoints[$mark].Sha256 $report.Branches.Restored.Checkpoints[$mark].Sha256
    }
    Assert 'Durability produces a distinct final save' $true (
        $report.Branches.Durability.Checkpoints.r165.Sha256 -cne $report.Branches.Restored.Checkpoints.r165.Sha256)
    $branch = 'Verifier self-check'
    $witness = $report.Branches.Restored
    foreach ($change in @(
        @{Group='Manufacturing'; Prefix='settlement'; Field='Yield'; Value=7}
        @{Group='Manufacturing'; Prefix='settlement'; Field='PackagingConsumed'; Value=2}
        @{Group='Manufacturing'; Prefix='settlement'; Field='Xp'; Value=8}
        @{Group='Dose'; Prefix='dose'; Field='Potential'; Value=($witness.Dose.Observed.Potential + 1)}
        @{Group='Dose'; Prefix='dose'; Field='Action'; Value=$false}
        @{Group='Dose'; Prefix='dose'; Field='VialMass'; Value='0/1'}
    )) {
        $group = $witness[$change.Group]
        $wrong = [ordered]@{} + $group.Observed
        $wrong[$change.Field] = $change.Value
        $start = $checks.Count
        $caught = $null
        try { Fields $change.Prefix $group.Expected $wrong } catch { $caught = $_.Exception.Message }
        $invariant = "$($change.Prefix) $($change.Field)"
        $last = $checks[$checks.Count - 1]
        if (!$caught -or $last.Passed -or $last.Name -cne $invariant) { throw "Self-check failed for $invariant" }
        $report.SelfChecks += @{Invariant=$invariant; AlteredObservation=$change.Value; Result='EXPECTED_REJECTION'; Message=$caught}
        $checks.RemoveRange($start,$checks.Count - $start)
    }
    $report.Status = 'PASS'
} catch {
    $report.Status = 'FAIL'
    $report.Failure = @{Message=$_.Exception.Message; Location=$_.ScriptStackTrace}
    throw
} finally {
    $report.CompletedUtc = [DateTime]::UtcNow.ToString('o')
    $report.Assertions = $checks.Count
    $report.AssertionsPassed = @($checks | Where-Object Passed).Count
    $report.AssertionsFailed = @($checks | Where-Object { !$_.Passed }).Count
    $checks | ForEach-Object { Json $_ } | Set-Content "$Run/assertions.jsonl" -Encoding utf8
    ConvertTo-Json -InputObject $report -Depth 18 | Set-Content "$Run/results.json" -Encoding utf8
}
