"""Bind existing source expectations to finite V1 qualification routes; no execution."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]

def read(name):
    return json.loads((PACKET / name).read_text(encoding='utf-8'))

def pin(path):
    data = (ROOT / path).read_bytes()
    return {'path': path, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

FIVE = ['TypedUninterrupted', 'TypedRestored', 'ConsoleUninterrupted', 'ConsoleRestored', 'ReceiptReplay']
tactical = read('INDEPENDENT_TACTICAL_AXES.json')
physical = read('INDEPENDENT_PHYSICAL_AUDIT.json')
parameters = {x['kind']: x for x in read('PARAMETER_CONTRACT_INDEX.json')['operations']}

routes = dict(tactical['routeRegistry'])
routes.update({
    'CACHE': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'Start',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedExpeditionCacheCases.cs:14-148'],
        'steps': 'Replay the case from fresh Start: approach the cache, actual PickWithTools, partial clock then Interrupt, reopen work to actual completion, Open and partial ration Pickup. Keep current request revision/seat and actual generated descendant; hidden initial cache and wrong-seat attempts are unchanged negative controls.'},
    'QUALITY': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'Start',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedExpeditionQualityCases.cs:157-304'],
        'steps': 'Use exact QualityWalkthrough command iterator from genesis and its selected extra-vial branch. Source commands include genuine mine, whole iron retrieval/desk placement, appraisal/sale, treatment, meal/partial intake/portion, research and manufacture. V1 adapters replace transport only; source payloads, actual principal and original policy stay intact. Stop and branch before the relevant command; no final-save shortcut.'},
    'VIAL_STOW': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'StartWithStowedVial',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs:16-49', 'engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs:573-695'],
        'steps': 'StartVialScenario(stow:true) executes the actual manufacture prefix. Walk/pickup, stow only into selected pack, close, walk away, save and restore, open/retrieve/continue. Keep the source test detached forgery/drop probes separate from these commands. Stowed-use denial is followed by actual retrieval, not an invented use permission.'},
    'VIAL_CARRIED': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'StartWithCarriedVial',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs:696-800'],
        'steps': 'Execute the source StartVialScenario from genesis and actual pickup/carry/encounter/use route. Preserve dose ownership by Companion and Hero custody/current inventory grant; ordinary use remains denied. Restore before handling and before the actual permitted use.'},
    'VIAL_TACTICAL': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'StartWithTacticalVial',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs:397-572'],
        'steps': 'Execute each source tactical handling branch from its genuine manufacture/carry prefix; retain exact opening/retrieval interaction sequence and actual use. First interaction and second Action are separate witnessed stages. Old profile and detached invalid snapshots remain negative controls.'},
    'VIAL_COMPANION': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'StartWithCompanionDose',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs:226-396'],
        'steps': 'Execute source reinforcement, actual injury and Companion recipient use with original selected policy, genuine manufactured dose and current title/custody. Observe real pre/post HP and spent state; do not seed injuries or replace healing with a prediction.'},
    'FOCUS': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE_WITH_SEPARATE_MODEL_CONTROLS',
        'factory': 'StartWithClericCasting(ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample(), ClericMilestoneDeclaration.AuthoredExample())',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/SpellCastingCases.cs:14-15', 'engine/com.decennium.foundation/Tests/EditMode/SpellCastingCases.cs:1223-1280'],
        'steps': 'Execute source real campaign focus transitions, remove/drop/pickup/handover/wear using actual paid hands/activity and declared willing recipient. Preserve the source direct-Simulation no-consent control as mechanical; use the existing host willing-handover grant for public positive routes. Derive IDs from actual current public item identity, not an assumed universal Id==LinkedId.'},
    'WATER': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE',
        'factory': 'NewCastingExpedition exact authored selections in SpellCastingCases14-15',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/SpellCastingCases.cs:892-935'],
        'steps': 'EarnClericObjective false with actual first-Cleric-action Purify on existing contaminated flask water; continue actual combat closure, Companion east walk and clock6, whole-flask Pickup, water StartIntake1 and clock60. Exact retained assertions: Purify leaves one pint/RNG/clock unchanged at cast, pickup adds1sec, intake consumes one pint in60sec. Restore before actual cast, pickup, intake and after completion.'},
    'VESSEL_BRANCHES': {
        'classification': 'SOURCE_FEASIBLE_FUTURE_HOST_BRANCH_NOT_EXECUTED',
        'factory': 'WATER original casting factory and consent',
        'source': ['engine/com.decennium.foundation/Laboratory/Model/VesselHandling.cs:33-85', 'engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionSession.cs:387-389', 'engine/com.decennium.foundation/Tests/EditMode/SpellCastingCases.cs:912-919'],
        'steps': 'Branch at WATER actual carried-flask boundary before intake. Drop at original pool uses Amount1/Handling.Drop/emptyDestination and pays1sec; then actual Pickup restores carried flask. Separately move actual Hero via lawful paid walk to Manhattan distance<=1 from Companion, retain one usable hand and capacity on each and no pending work, then submit Companion Handover of the selected flask with Hero destination and actual current willing host grant. Do not teleport or retitle contents. If an intervening native scheduled event prevents that route, retain exact rejection and derive a different lawful prefix before calling this a positive witness. Retrieve/Stow remain negative branches.'},
    'BLOOD': {
        'classification': 'EXISTING_GENUINE_NATIVE_ROUTE_PLUS_PUBLIC_QUALITY_PREFIX',
        'factory': 'Start via QUALITY; older BloodHandoffPolicy wire94 is separate native reference only',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedBloodSpecimenCases.cs:49-178', 'engine/com.decennium.foundation/Tests/EditMode/ConnectedBloodSpecimenCases.cs:248', 'engine/com.decennium.foundation/Tests/EditMode/ConnectedExpeditionQualityCases.cs:180-228'],
        'steps': 'Use QUALITY fresh-host path to the actual named starting specimen/treatment vessel. At the exact native eligible boundary open and start treatment; advance600, restore, then1200 and continue. Preserve genuine source reference cases for before/at opening timeout and spoiled treatment; adapt only branches whose real public host prefix reaches their required clock/stock/permission. Other wire94/native or forged-snapshot controls remain labelled and cannot satisfy host positive coverage. Half-pound preservative is reserved first and spent once at resolution; no harvesting/donor producer is added.'},
    'TRAP': {
        'classification': 'EXISTING_GENUINE_HOST_ROUTE_WITH_FINITE_CONTROL_EXTENSION',
        'factory': 'StartWithFishingTrap',
        'source': ['engine/com.decennium.foundation/Tests/EditMode/ConnectedExpeditionSessionCases.cs:201-275', 'engine/com.decennium.foundation/Laboratory/Model/SharedFishingTrap.cs:584-797'],
        'steps': 'Replay accepted mgt06 connected paid setup/retrieval chronology from original factory. Branch before actual completed setup and before actual retrieved catch; use the current own pending setup/retrieval identity to Pause/Resume/Cancel. Qualify partial retrieval by advancing a positive subinterval short of actual required remaining work; pause releases worker labor but retains earned progress, resume books remaining work and eventual output occurs once. If source-admitted interruption cannot be produced at a real boundary, retain the producer gap. WIS/INT detached edits and trap Abandon are not host positives.'},
    'WORK_SPINE': {
        'classification': 'EXISTING_GENUINE_PUBLIC_HOST_ROUTE', 'factory': 'Original accepted work-control factory/selections from PRINCIPAL_ROUTE_ALLOCATION.json',
        'source': ['docs/unity/evidence/2026-11-23-int05-admitted-command-surface/PRINCIPAL_ROUTE_ALLOCATION.json'],
        'steps': 'Replay all244 original commands with28 original checkpoints and added V1 pending/attempt/result checks. This is exact accepted predecessor input, not passing V1 evidence; useful bench dose use and continued filling/preparation remain in this route.'},
})

route_groups = {
    'Interact': ['CACHE', 'TRAP'], 'HandlePortableEquipment': ['QUALITY', 'VIAL_STOW', 'VIAL_CARRIED', 'VIAL_TACTICAL', 'FOCUS', 'CASTING'],
    'OpenPortableContainer': ['VIAL_STOW', 'VIAL_TACTICAL', 'BLOOD'], 'ClosePortableContainer': ['VIAL_STOW', 'BLOOD'],
    'HandleInventory': ['CACHE'], 'PortionInventory': ['QUALITY', 'FOCUS'],
    'EquipPortableItem': ['FOCUS'], 'RemovePortableItem': ['FOCUS'], 'HandleVessel': ['WATER', 'VESSEL_BRANCHES'],
    'StartIntake': ['QUALITY', 'WATER'], 'InterruptIntake': ['QUALITY'],
    'UseAlchemyDose': ['VIAL_COMPANION', 'VIAL_TACTICAL', 'VIAL_STOW', 'VIAL_CARRIED', 'WORK_SPINE'],
    'StartHarvestPreservationTreatment': ['BLOOD', 'QUALITY'],
}
expected_physical = {
    'Interact': 'Cache and trap remain distinct native operations; preserve interrupted labor and source-check timing. Open does not duplicate stock. Retrieval yields only actual completed result once; zero request sentinel remains0/1.',
    'HandlePortableEquipment': 'Actual title/custody/link/placement/hand state changes once, preserving one physical body; ordinary payment is actual1sec, tactical first interaction/second Action preserve native order and zero tactical time.',
    'OpenPortableContainer': 'Only authorized current actual closure changes. Protected specimen exposure begins at the real opening boundary; opening does not reveal private contamination or grant arbitrary child access.',
    'ClosePortableContainer': 'Actual container becomes closed only after current guards; pending inputs/closure and protected-material exposure deadlines keep their original failures and order.',
    'HandleInventory': 'Only admitted Hero cache ration Pickup; transfer exact available rational amount, create actual traced child with original unit/age/title/custody, and preserve total resources.',
    'PortionInventory': 'Actual eligible quantity splits exactly with no new time; parent-child amounts sum to original, native age/owner/provenance retained; reservations/whole tender/unsafe stock deny under original guard order.',
    'EquipPortableItem': 'Only actual selected holy symbol and authorized placement/body route; native paid handling and hand/body occupancy, no general equipment admission.',
    'RemovePortableItem': 'Actual selected worn holy symbol removal pays original1sec and occupies real available hand; casting component rights depend on resulting actual placement.',
    'HandleVessel': 'Actual flask moves with all contained lot custody/access synchronized once, no liquid manufacture or title rewrite. Ordinary move pays1sec; pending-use/hands/range/capacity remain current; storage stays unsupported.',
    'StartIntake': 'Only safe ordinary eligible food/water; reserve exact quantity, consume in proportion to actual paid clock, preserve nutrition freshness and current title; no tactical intake expansion.',
    'InterruptIntake': 'Only own actual active intake stops, preserves actual consumed amount and earned nutrition, releases untouched reservation; no refund or invented completion.',
    'UseAlchemyDose': 'Whole-dose1/1 actual current permitted user/recipient; spend once, real capped healing under native life/blocker rules. Stowed/ordinary misuse remains unavailable; spent dose retry is exact duplicate only.',
    'StartHarvestPreservationTreatment': 'Exact existing specimen and real half-pound preservative; original1800sec work/check, freshness and access, delayed protection only on actual eligible successful completion. Spoiled endpoint and opening exposure remain distinct; no new donor/harvest authority.',
}

operations = []
for oi, op in enumerate(tactical['operations']):
    rows = []
    for ai, axis in enumerate(op['axes']):
        rows.append({
            'axis': axis['axis'], 'expected': axis['nativeExpectedBehavior'], 'domain': axis['hostDomain'],
            'sourceAudit': f'INDEPENDENT_TACTICAL_AXES.json#/operations/{oi}/axes/{ai}',
            'routeIds': axis['routeIds'], 'branchInstruction': axis['prospectiveBranch'],
            'classification': axis['disposition'], 'separateModelControls': axis['detachedOrNativeOnlyControls'],
            'remainingExecutionRisks': axis['gaps'], 'executionPaths': FIVE,
            'qualificationRule': 'All actual state-changing alternatives require five complete executions; rejection-only probes run through typed/console fresh/restored contexts and prove unchanged state. Model-only controls remain separate.',
            'executed': False,
        })
    operations.append({'kind': op['kind'], 'nativeSources': op['nativeSources'], 'axes': rows})
for oi, op in enumerate(physical['operations']):
    rows = []
    for ai, axis in enumerate(op['axes']):
        rows.append({
            'axis': axis['axis'], 'expected': expected_physical[op['kind']],
            'exactNativeGuards': op['orderedNativeGuards'], 'exactDomain': op['hostDomain'],
            'sourceAudit': f'INDEPENDENT_PHYSICAL_AUDIT.json#/operations/{oi}/axes/{ai}',
            'sourceWitness': axis['witnessOrSource'], 'routeIds': route_groups[op['kind']],
            'classification': axis['disposition'], 'remainingExecutionRisks': [axis['remaining']],
            'executionPaths': FIVE, 'executed': False,
            'qualificationRule': 'Select the matching source witness from listed operation routes; execute each distinct paid/choice alternative through five complete paths. Host-unavailable branches receive unchanged negative controls only. No route-level positive claim transfers to a detached subbranch.',
        })
    operations.append({'kind': op['kind'], 'nativeMutationBoundary': op['mutationBoundary'], 'axes': rows})

for op in operations:
    assert [x['axis'] for x in op['axes']] == parameters[op['kind']]['exactAxes'], op['kind']
    for axis in op['axes']:
        assert all(x in routes for x in axis['routeIds'])

source_paths = set()
for route in routes.values():
    for reference in route['source']:
        path = reference.split(':')[0]
        assert (ROOT / path).is_file(), path
        source_paths.add(path)
for op in tactical['operations']:
    source_paths.update(x.split(':')[0] for x in op['nativeSources'])
for name in ['INDEPENDENT_TACTICAL_AXES.json', 'INDEPENDENT_PHYSICAL_AUDIT.json', 'PARAMETER_CONTRACT_INDEX.json', 'PROFILE_ADMISSION_MATRIX.json']:
    source_paths.add(str((PACKET / name).relative_to(ROOT)).replace('\\', '/'))

result = {
    'schemaVersion': 1, 'status': 'FINITE_SOURCE_BRANCH_PLAN_PROPOSED_NOT_EXECUTED',
    'reviewer': 'Parent Codex self-review; frozen underlying axes have separately named independent reviewers.',
    'counts': {'candidateKinds': len(operations), 'candidateAxes': sum(len(x['axes']) for x in operations), 'executed': 0},
    'routeRegistry': routes, 'operations': operations,
    'operatorOperations': [
        {'kind': 'AdvanceClock', 'principal': 'Existing session operator only', 'routeIds': ['WORK_SPINE', 'LOCAL', 'FERRY', 'RECOVERY', 'ORDINARY_FUTURE'], 'expected': 'Exact rational X/Y advances only under current native grants/clock blockers. Actual work/life/contact/choice boundaries can stop early with retained progress; Stopped contact is not rollback. Pending strain response resumes only its actual remaining request. No private participant/cause/count is exposed.', 'executionPaths': FIVE, 'native': 'TestOnlySharedWorldPolicy.cs ordered AdvanceTo/contact paths; OUTER_ADMISSION_EXTRACTION_PLAN.json', 'executed': False},
        {'kind': 'EndFixedEncounter', 'principal': 'Existing session operator only', 'routeIds': ['WORK_SPINE', 'FERRY', 'FERRY_KO'], 'expected': 'Exact existing closure preconditions and paid outgoing-slot time. Dead-only source closure rejects genuine Stable knockout branch; duplicate after actual closure does not spend again. Observe actual settled work/condition/clock without a read-time simulation.', 'executionPaths': FIVE, 'native': 'SharedWorldCombatPolicy.cs closure/EndCombat guards; OUTER_ADMISSION_EXTRACTION_PLAN.json', 'executed': False},
    ],
    'commonCheckpoints': ['Fresh original factory', 'Before target command with all actual prerequisites', 'Every genuine pending choice/partial work boundary', 'After exact authoritative attempt', 'After actual response/resolution', 'After strict restore', 'After changed visibility/custody/context', 'Terminal continued gameplay'],
    'comparisonContract': 'At matching genuine checkpoints compare exact canonical bytes, original ordered views, V1 catalog/assessment/discovery/choice and separately scoped immediate/retained/current facts; runtime identities and principal-bound receipt metadata are not scrubbed. Do not infer historical values from current state or the former query.',
    'sourcePins': [pin(p) for p in sorted(source_paths)],
    'sourceApiAccepted': False, 'runtimeAuthorized': False,
    'limits': ['Routes remain source-derived qualification instructions until actual V1 execution.', 'All24 selected factory compatibility entries and authentic95–116 inputs remain separately required.', 'Genuine multi-reactor/nested Press, ordinary observation and prospective physical branches must be reached through actual commands; model fixtures do not satisfy them.', 'No accepted TAC-10/OMA/MGT-02 qualification is reopened by using original commands as new API test inputs.'],
}
(PACKET / 'PHYSICAL_TACTICAL_BRANCH_QUALIFICATION_PLAN.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(json.dumps(result['counts']))
