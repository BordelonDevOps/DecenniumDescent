"""Finite exact-origin proposal. Strings locate reviewed branches, not runtime dispatch."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'docs/unity/evidence/2026-11-23-int05-admitted-command-surface'
MODEL=ROOT/'engine/com.decennium.foundation/Laboratory/Model'
RANGES={
'SharedWorldCommandQueries.cs':[(28,189)],'SharedReinforcement.cs':[(94,145),(180,211),(251,267)],
'SharedExplorationHide.cs':[(43,115),(143,150)],'SharedExplorationSearch.cs':[(59,124),(191,199)],
'SharedObservationActions.cs':[(70,225)],'SharedFrightened.cs':[(34,95)],'SharedFerrySeal.cs':[(29,55)],
'TestOnlyInventoryPolicy.cs':[(88,198)],'SharedConnectedBloodSpecimen.cs':[(98,191)]}
OPS={
'SharedWorldCommandQueries.cs':['BeginWorldStep','SuspendWorldStep','ResumeWorldStep','BeginReinforcementApproach'],
'SharedReinforcement.cs':['BeginReinforcementApproach','SuspendWorldStep','ResumeWorldStep','EndRegularTurn','AdvanceClock'],
'SharedExplorationHide.cs':['Hide','CancelExplorationHide'],'SharedExplorationSearch.cs':['Search','CancelExplorationSearch'],
'SharedObservationActions.cs':['Hide','Search','CancelExplorationHide','CancelExplorationSearch'],
'SharedFrightened.cs':['UseIntimidatingPresence'],'SharedFerrySeal.cs':['TearExposedSeal'],
'TestOnlyInventoryPolicy.cs':['HandleInventory','PortionInventory','StartIntake','InterruptIntake'],
'SharedConnectedBloodSpecimen.cs':['StartHarvestPreservationTreatment','HandlePortableEquipment','OpenPortableContainer','ClosePortableContainer']}
GROUPS={
('InvalidRequest','REQUEST_SHAPE'):'''InvalidWorldStep InvalidTraversalControl InvalidReinforcementPayload InvalidOrdinaryHideRequest InvalidOrdinaryHideCancellation InvalidOrdinarySearchRequest InvalidOrdinarySearchCancellation InvalidObservationActionPayload InvalidSearchRequest InvalidHideRequest InvalidIntimidatingPresenceRequest InvalidSealRequest UnexpectedInventoryPayload InvalidIntakeRequest InvalidInventoryRequest CountedInventoryMustBeWhole InvalidPortionRequest InvalidHandling''',
('ChoicePending','OWN_PENDING'):'''TacticalChoicePending OrdinaryHideDecisionPending OrdinarySearchDecisionPending ReinforcementTacticalChoicePending''',
('ChoiceUnavailable','OWN_PENDING_OR_UNIFORM_UNKNOWN_TOKEN'):'''NoPendingOrdinaryHide NoPendingOrdinarySearch''',
('TurnRequired','OWN_ACTOR_AND_PUBLIC_CONTEXT'):'''WrongRegularTurn WrongOrdinaryHideStart OrdinaryHideRequiresOwnStart WrongOrdinaryActivityInterval OrdinarySearchRequiresIntervalStart''',
('ActorUnavailable','OWN_ACTOR_AND_EXACT_PUBLIC_PERMISSION'):'''ConditionPreventsMovement ReinforcementActorIncapable OrdinaryHideActionCapabilityUnavailable OrdinarySearchVisualCapabilityUnavailable ActorCannotAct ConditionPreventsAction BloodTreatmentWorkerUnavailable''',
('ActorBusy','OWN_ACTOR_AND_OWN_WORK_OR_TRAVEL'):'''WorkerBusy TraversalAlreadyPending OrdinaryHideActorBusy OrdinarySearchActorBusy OrdinaryHideInProgress OrdinarySearchInProgress ReinforcementWorkerBusy SealRequiresStationaryAccess''',
('AllowanceUnavailable','OWN_ACTOR_AND_EXACT_PUBLIC_LEDGER'):'''InsufficientMovement ActionAlreadySpent OffCalendarActionAlreadySpent InteractionBudgetUnavailable''',
('ContextRequired','OWN_ACTOR_AND_PUBLIC_CONTEXT'):'''NoActivityCalendar OffCalendarDashBudgetUnsupported OrdinaryHideRequiresStationaryAnchor OrdinarySearchRequiresStationaryAnchor ObservationActionRequiresTacticalCombat HideRequiresAuthoredGridCell ReinforcementRequiresStationaryStaging TacticalIntakeNotAdopted''',
('RangeConstraint','PUBLIC_GEOMETRY_ALL_DEPENDENCIES'):'''SearchCellOutOfRange SealOutOfReach''',
('PathUnavailable','PUBLIC_GEOMETRY_ALL_DEPENDENCIES'):'''Blocked SealEffectLineBlocked''',
('InventoryAccessUnavailable','OWN_ITEMS_ALL_REFERENCED_PLACEMENTS'):'''InventoryOutOfReach IntakeRequiresReadyCustody InvalidPickup InvalidDrop InvalidStow InvalidRetrieval InvalidHandover BloodTreatmentEquipmentOutOfReach BloodSpecimenRemainsInBoundVessel BloodSpecimenRequiresClosedVesselMovement''',
('OwnedResourceUnavailable','OWN_RESOURCE_EXACT_REGISTERED_QUANTITY'):'''InventoryQuantityUnavailable''',
('EquipmentRequired','OWN_ACTOR_AND_OWN_ITEMS'):'''BloodTreatmentToolUnavailable CleanPreservationToolUnavailable''',
('HandsUnavailable','OWN_ACTOR_AND_OWN_ITEMS'):'''UsableHandRequired RecipientHandsReserved''',
('WorkStateRequired','OWN_WORK_OR_TRAVEL'):'''NoPendingTraversal TraversalAlreadySuspended TraversalNotSuspended ReinforcementApproachNotPending ReinforcementAlreadyAttempted NoActiveIntake HarvestTreatmentInputsInUse''',
('RechargeRequired','OWN_MAGIC_EXACT_RECHARGE_FIELD'):'''IntimidatingPresenceRecharging''',
('PrerequisiteRequired','PUBLIC_PREREQUISITE_ALL_DEPENDENCIES'):'''ExposedSealAlreadyTorn BloodTreatmentAlchemyTrainingRequired BloodTreatmentContainerFitNotEstablished BloodTreatmentRequiresBoundWholeSpecimen BloodSpecimenHandlingRequiresOrdinaryOwner''',
('TargetUnavailable','UNIFORM_KNOWN_TARGET_BOUNDARY'):'''UnknownReinforcementDefinition UnknownInventoryLot ExposedSealUnavailable IntimidatingPresenceTargetUnavailable''',
('RequestUnavailable','EXACT_REVIEWED_PROTECTED_OR_MIXED_GUARD'):'''ConcurrentHostileTraversalUnsupported ConcurrentWorldTraversalUnsupported HuntingTrapTetherPreventsMovement Occupied RouteTravelPathReserved RestInterruptionAuthorityUnsupported HavenCareCombatTransitionUnsupported TacticalTransitionRequired ReinforcementParticipationMandateMissing ReinforcementAlliedSideMissing ReinforcementTieAuthorityMissing ReinforcementAwarenessUnavailable ReinforcementNotSelected ReinforcementActorUnauthorized ReinforcementEncounterUnavailable ReinforcementApproachTriggerUnsupported ReinforcementHardCarryingLimit ReinforcementRouteAttachmentUnsupported ReinforcementPassageObstructed ReinforcementEntryPositionUnavailable OrdinaryHideUnavailable ConnectedObservationStageClosed OrdinaryHideActorUnavailable ObservationHistoryCapacityReached OrdinarySearchUnavailable OrdinarySearchActorUnavailable ObservationActionNotImplemented HideWhileClearlyObserved ObservationHideHistoryCapacityReached ObservationKnowledgeCapacityReached HideAttemptUnchanged IntimidatingPresenceUnavailable IntimidatingPresenceContextUnsupported IntimidatingPresenceNotOwned IntimidatingPresenceClassUnavailable IntimidatingPresenceRequiresStationaryAccess IntimidatingPresenceHistoryFull IntimidatingPresenceHearingTargetingUnsupported IntimidatingPresenceAlternativePerceptionUnsupported IntimidatingPresenceConditionHistoryFull ConditionBoundaryPending SealActorUnsupported SealActionLedgerUnavailable HarvestTreatmentProtectionActive UnsupportedInventoryProfile IntakeExpired VesselProcedureNotImplemented ContainerFitNotEstablished CarryingCapacityNotEstablished CarryingCapacityExceeded BloodTreatmentStageClosed HarvestTreatmentCannotFinishBeforeSpoilage BloodTreatmentInputsUnavailable HarvestTreatmentInterruptionUnsupported HarvestPreservationOpenLifecycleTacticalUnsupported BloodSpecimenHandlingStageClosed''',
}
lookup={}
for binding,words in GROUPS.items():
    for word in words.split():assert word not in lookup;lookup[word]=binding
excluded={
'RouteTravelMustPauseFirst':'All24 selected factory chains lack routeTravelFixture; do not expose a new route-control capability.',
'RouteTravelerMustDetachBeforeOtherMovement':'All24 lack selected route-travel producer.',
'RoutePositionAuthorityMismatch':'Selected factories lack route-travel producer; retain native source without adding host commands.',
'RouteDepartureDirectionUnsupported':'Selected factories lack route-travel producer.',
'RouteDepartureOffsetUnsupported':'Selected factories lack route-travel producer.',
'EncounterClockNotImplemented':'Underlying isolated inventory clock branch; selected composite clock uses its authoritative outer dispatch.',
'InvalidInventoryAdvance':'Underlying isolated inventory clock branch; current selected composite clock preempts it.',
'InvalidCombatEntry':'EnterInventoryCombat is not one of78 admitted seat kinds or2 operator kinds.',
'EncounterCommandNotImplemented':'Underlying Move/Interact fallback not a selected inventory operation; selected host Interact cache/trap dispatch is separate.',
'ReinforcementExplicitSuspension':'Retained event label, not a failure.', 'ReinforcementExplicitResume':'Retained event label, not a failure.',
'Available':'Legacy successful query result label, not a denial.',
}
rows=[];exclusions=[];unmapped=[];pins=[]
for name,ranges in RANGES.items():
    path=MODEL/name;lines=path.read_text(encoding='utf-8').splitlines();rel=path.relative_to(ROOT).as_posix()
    pins.append({'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
    for line,text in enumerate(lines,1):
        if not any(a<=line<=b for a,b in ranges) or not ('return' in text or '?' in text):continue
        for token in re.findall(r'"([A-Z][A-Za-z0-9]*)"',text):
            origin={'path':rel,'line':line,'statement':text.strip(),'context':'\n'.join(lines[max(0,line-4):line+1])}
            if token in excluded:
                exclusions.append({'nativeToken':token,'origin':origin,'reason':excluded[token]});continue
            if token not in lookup:
                unmapped.append({'token':token,'origin':origin});continue
            code,gate=lookup[token]
            rows.append({'nativeToken':token,'origin':origin,'candidateKinds':OPS[name],
                'originMeaning':'Exact original guard at this source location; candidate-kind list is a call-family allocation, not permission for every kind/profile to reach every branch.',
                'publicCodeProposal':code,'disclosurePredicate':gate,
                'otherwise':'RequestUnavailable with fixed protected detail and no stage value; this fallback is proposed for this exact source guard only.',
                'stageRule':'NativeEligibility only when the actual complete guard category is independently public; otherwise fixed stage Availability.Withheld and no value. In real post-time/entry continuation use native actual stage only if disclosable. A read never reports execution reached that stage.',
                'requiredExplanation':'Preserve independent authorized current operation domain, own resources/costs, accessible source alternatives and explicit published requirements from frozen per-operation registries. Protected reason is not a waiver for those fields.',
                'nativeOutcomeBoundary':'No exception/reason string is public; missing native gameplay eligibility is not ProjectionUnavailable. Actual carrier preserves legacy result/first guard/rollback. Only genuinely absent new read/projection data uses technical unavailable.',
                'approved':False,'executed':False})
assert not unmapped,json.dumps(unmapped,indent=2)
result={'schemaVersion':1,'status':'FINITE_EXACT_ORIGIN_PUBLIC_DISPOSITION_PROPOSAL_REQUIRES_REVIEW',
    'reviewer':'Parent Codex self-review; source ranges and frozen family audits reused; not independent source closure.',
    'sourceRanges':RANGES,'rows':rows,'excludedOrigins':exclusions,'sourcePins':pins,
    'counts':{'exactOriginRows':len(rows),'distinctTokens':len(set(x['nativeToken'] for x in rows)),'sourceFiles':len(pins),'excludedLocatorRows':len(exclusions),'unmappedInDeclaredRanges':len(unmapped)},
    'precisions':[
        'Whole composite private/mixed guards deliberately use neutral RequestUnavailable; no subtype, private observer, occupied-cell count, DC, condition source, Director mandate or hidden body/capacity data.',
        'A specific public code requires the complete exact guard dependency predicate, not merely Controls(actor). Missing prerequisite disclosure means protected whole-guard output; required known fields remain mandatory.',
        'ReinforcementEntryPosition/HardCarrying/Passage checks at actual end-round admission are real continuation boundaries; assessment cannot make that future event happen.',
        'BeginWorldStep may directly enter first combat during actual submission; later traversal contacts happen during their real clock paths. Reads perform neither.',
        'Underlying inventory Handle branches remain host-limited to cache ration Pickup; other labels retained here are native source locations, not newly supported handling. Generic mass/tender restrictions and earlier outer guards remain.',
        'Blood profile validation82–95 is outside this source-origin scope; validators stay execution/restore only. WaterFilling and AssessBloodIngredient are separately assigned management supplement.',
        'Dynamic forwarded helper failures and other guarded method sources must reconcile against the retained35-origin list; this finite literal inventory does not claim total transitive closure.',
    ],'sourceApiAccepted':False,'runtimeAuthorized':False,'buildsTestsGameplay':False}
out=P/'PUBLIC_DENIAL_PHYSICAL_TACTICAL_ORIGINS.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(result['counts']))
