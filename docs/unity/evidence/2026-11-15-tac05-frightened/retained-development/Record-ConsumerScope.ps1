param([Parameter(Mandatory)][string]$AssemblyRoot)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
$flags=[Reflection.BindingFlags]'Instance,NonPublic'
$policy=$session.GetType().GetField('policy',$flags).GetValue($session)
$nullFields=@('rangedCombat','repair','harvestFixture','huntingTrapFixture','fishingTrap','prospectingFixture',
    'recipe347Fixture','routeMappingFixture','routeMappingWorkFixture','routeReconnaissanceFixture','routeTravelFixture',
    'routeMotionFixture','expeditionCampConstructionProfile','portableStorageFixture')
$falseFields=@('readyActionEnabled','connectedWoundTreatment','connectedCompanionStabilization','harvestPreservationEnabled',
    'harvestPreservationTreatmentEnabled','harvestPreservationExposureEnabled','connectedFishingTrap')
$proof=@($nullFields+$falseFields|ForEach-Object{
    $field=$policy.GetType().GetField($_,$flags)
    if($null-eq$field){throw "Scope field no longer exists: $_"}
    $value=$field.GetValue($policy)
    $expected=if($_-in$nullFields){$null}else{$false}
    if($value-ne$expected){throw "Previously unavailable consumer family is now selected: $_"}
    @{field=$_;observed=$(if($null-eq$value){'null'}else{'false'});expectedUnavailable=$true}
})
$rows=@(
    @{family='Club and shared unarmed/OA melee';hook='TestOnlyClubAttackPolicy.cs / PlaytestConditions.Attack';scope='Shared attack roll receives actual visible feared-source projection. Club is public and genuinely demonstrated. Normal AttackUnarmed is not exposed by this connected host; do not claim a connected unarmed acquisition.'},
    @{family='Ranged/Soldier attacks and Ready';hook='SharedWorldRangedCombat.cs / RangedAttackRequest';scope='Ranged visibility hook added, but rangedCombat=null and readyActionEnabled=false. Optional predecessor consumers are not a connected frightened ranged or Ready witness.'},
    @{family='Hide and Search';hook='SharedObservationActions.cs / HideDisadvantage and ResolveSearch';scope='New profile exposes existing tactical actions. Actual paid Hide after sight loss uses one die. Search uses the same relationship projection; no affected Search witness claimed.'},
    @{family='Supply cache';hook='SharedSupplyCache.cs / ResolveCacheAttempt';scope='Genuine retrieved thieves tools and tactical paid pick select 11 from 11/16 with visible fear. New-profile host bridge admits existing tactical cache rules; earlier profiles retain ordinary-only exposure.'},
    @{family='Formula research and manufacturing';hook='SharedFormulaResearch.cs / SharedManufacturing.cs';scope='Shared selection hooks added. ConnectedExplorationObservation.StageOpen requires no later entry; connected research start/resume and recipe4 start enforce that stage. Actual research and manufacturing finish before later fear. No affected long-work completion witness claimed.'},
    @{family='Mining';hook='SharedMining.cs / CompleteMining';scope='Selected mining fixture uses shared fear projection. No affected mining completion witness claimed; completion timing/ability-choice/source qualifiers remain the existing ones.'},
    @{family='Retreat check';hook='SharedRetreat.cs / ResolveRetreatInstruction';scope='Shared fear projection added. The policy retains the selected retreat and its round/authority/context gates, but ConnectedExpeditionSession exposes neither DeclareRetreat nor AttemptRetreatEscape. No connected frightened retreat witness claimed.'},
    @{family='Blood specimen preservation';hook='SharedHarvestPreservationTreatment.cs / SharedConnectedBloodSpecimen.cs';scope='AssessBloodTreatment requires ConnectedExplorationObservation.StageOpen (later entry absent), and the existing single-attempt gate remains. The only fear producer requires later reinforcement already admitted. This selected treatment cannot begin under this source fear; no affected treatment claim or blanket optional-treatment certification.'},
    @{family='Repair, harvest, traps, prospecting, assay, route/work, temporary camp';hook='Optional families listed by actual null field proof';scope='Unavailable in this exact selected profile. Existing roll consumers are not blanket-certified for future v2 profile composition.'},
    @{family='Wound treatment and companion stabilization';hook='SharedWoundTreatment.cs / SharedCompanionStabilization.cs';scope='Both connected producer flags false. No affected Medicine treatment/stabilization claim.'},
    @{family='Tactical willing movement';hook='TacticalMovementPolicy.cs / StepFailure';scope='Shared hook covers ordinary tactical step, reposition, CommandStep, formation and Press when admitted. Actual visible and unseen closer steps reject unchanged; optional Soldier grants are not added.'},
    @{family='World willing movement and active edges';hook='SharedWorldCommandQueries.cs / SharedFrightened.cs / TestOnlySharedWorldPolicy.cs';scope='Begin/Resume and boundary/reconciliation hooks installed. Detached actual clock proves temporary immunity ending at3/10sec suspends a2foot edge at3feet with1foot paid. Actual bounder tests actor-only attribution in three simultaneous-motion cases; current host denies concurrent world traversal. Whole/split18sec matches repeat/final/recharge semantics.'},
    @{family='Reinforcement approach';hook='AssessWorldStep(... reinforcementApproach:true)';scope='Uses the shared step assessment. The only actual fear producer requires reinforcement already admitted, so this source cannot newly frighten the incoming reinforcement edge.'},
    @{family='Reengagement';hook='SharedReengagement.cs plus shared world step';scope='Existing own approach, authority and context gates retained. No frightened reengagement witness claimed.'},
    @{family='Forced movement';hook='Existing authoritative Push producers bypass willing StepFailure';scope='No forced flag in typed player movement. Detached existing Overwatch Push producer moves5feet with its real STR save while the same willing step rejects. A console root forced:true cannot bypass the genuine unseen approach denial. This is no connected Push acquisition.'},
    @{family='Saving throws, damage and passive values';hook='SharedFrightened.cs / normal shared saves';scope='Fear adds no penalty to these. Genuine first/repeat WIS draws remain single die; suppressed-repeat component control matches unsuppressed draw.'},
    @{family='Historical causal validation';hook='TestOnlySharedWorldPolicy.cs / ReconstructCanonicalHistory';scope='Strict restore reconstructs Initial plus all receipts and compares complete canonical bytes. Five paths match19 checkpoints/95 comparisons. Structurally admissible old cache/save/attack/Hide modifier forgeries reject strict restore unchanged, including attacks/checks after fear has ended. Current condition state is not used as a replacement for causal replay.'}
)
$model=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../com.decennium.foundation/Laboratory/Model')).Path
$sources=@('ConnectedExpeditionSession.cs','TestOnlySharedWorldPolicy.cs','SharedFrightened.cs','FrightenedRules.cs','TestOnlyClubAttackPolicy.cs',
    'PlaytestConditions.cs','SharedWorldRangedCombat.cs','SharedObservationActions.cs','SharedSupplyCache.cs','SharedFormulaResearch.cs',
    'SharedManufacturing.cs','SharedMining.cs','SharedRetreat.cs','SharedReengagement.cs','SharedReinforcement.cs',
    'SharedHarvestPreservationTreatment.cs','SharedWorldCommandQueries.cs','TacticalMovementPolicy.cs')
[ordered]@{status='CONSUMER_SCOPE_RECORDED_NOT_MODULE_ACCEPTANCE';atUtc=[DateTime]::UtcNow.ToString('o');assemblyRoot=$AssemblyRoot;
    actualUnavailableProfileFields=$proof;consumers=$rows;
    sourceHashes=@($sources|ForEach-Object{@{file=$_;sha256=(Get-FileHash -LiteralPath (Join-Path $model $_)).Hash.ToLowerInvariant()}});
    stanceCorrection='ClericGuard helper submits stance ordinal1, which is Aggressive, not Guarded. Retained snapshots/receipts are authoritative; do not describe those party turns as Guarded.';
    closureDisposition='not demonstrated; reviewed scope exception (GPT bd6e3553-7534-5fdb-9883-e2426d85c097). Detached actual closure path separately passes failed repeat retention and final expiry; no connected defeat/acquisition claim.';
    supportingReports=@('historical-check-controls/results.json','historical-consumer-controls/results.json','clock-components-3/results.json','projection-controls/results.json','forced-movement-controls-2/results.json','boundary-controls/results.json','console-boundary-controls-2/results.json','closure-transition-controls/results.json');
    outstanding=@('Exact full regression completion, final evidence retention and actual final GPT review.')
}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $PSScriptRoot 'consumer-scope-progress.json') -Encoding utf8
Write-Output "Recorded $($rows.Count) consumer families and $($proof.Count) actual unavailable-profile boundaries."
