"""Allocate original-profile and checkpoint evidence without running the engine."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
MGT = ROOT / 'docs/unity/evidence/2026-11-23-mgt02-connected-work-control'
def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path)}

profiles = load(PACKET/'PROFILE_ADMISSION_MATRIX.json')
route = load(PACKET/'PRINCIPAL_ROUTE_ALLOCATION.json')
authentic = load(MGT/'support/compatibility-sources.json')
assert [x['wire'] for x in authentic] == list(range(95,117))
old_dir = ROOT/'engine/artifacts/connected-work-control/five-paths-02/TypedUninterrupted'
old_result = load(old_dir/'result.json')
assert digest(old_dir/'result.json') == route['predecessorResultSha256']
files = {x['name']: x['sha256'] for x in old_result['files']}

focus = {
    0: 'Genuine genesis, unopened/unseen cache, no receipts or pending choices; source descriptions distinguish selected operations from current usability.',
    15: 'First encounter actually closed; exact prior closure receipt, ordinary movement/work context and own current capabilities.',
    16: 'Real mining start and initial work/reservations; initial command is committed, not completed extraction.',
    17: 'Actual clock resolved mine work; material extraction/current local observation versus private yield/value/history fields.',
    26: 'Real appraisal completion; current report knowledge and exact monetary value, no sale proceeds yet.',
    27: 'Actual sale started; active delivery/worker/exclusive claims remain distinct from successful transfer.',
    30: 'Actual meal purchase; tender/payment/source delivery and own acquired food, no automatic intake credit.',
    94: 'Actual research start; exact knowledge/evidence/copy exclusion and native work booking.',
    95: 'Research paid progress/retry boundary; use exact retained native status, no manufactured AwaitingCheck host claim.',
    96: 'Actual research resume and selected worker/bookings; no duplicate material payment.',
    97: 'Actual research resolution and known recipe; completed knowledge remains distinct from future manufacture.',
    104: 'Real recipe4 batch start; actual ingredient/package reservations and future phase obligations.',
    105: 'Actual first batch interval; retained/partial phases, native loss policy and worker booking.',
    106: 'Genuine pending manufacturing quality; actual offer identity, FullYield/Durability semantics and priority.',
    107: 'Actual quality response; realized native yield/body effects, matching response versus initiating receipt.',
    108: 'Actual portable container closure and current item quantity under current rights.',
    117: 'Real reinforcement approach, physical arrival not yet assumed roster admission.',
    128: 'Actual opportunity response and continued combat; original response/attack lineage, current Action/Reaction/HP.',
    129: 'Actual useful bench-dose use; spent-dose authorized historical result versus current unavailable consumption.',
    136: 'Actual regular turn end; due work/life/conditions and current next actor; no replay in reads.',
    138: 'Second real useful dose use; independent actual recipient/healing/capped outcome and exactly-once effects.',
    232: 'Later real encounter closure and paid outgoing slot; current ordinary context, retained prior combat results.',
    234: 'Fractional water fill start, exact source/capacity reservation and60active-second requirement.',
    237: 'Real fill pause; progress/reservation retained and worker labor released.',
    239: 'Actual ordinary Guidance during pause; source context/strain/cast receipt and protected consumption policy.',
    241: 'Actual fill resume, remaining booked labor and current capability; no source re-reservation duplication.',
    242: 'Actual fill completion, exact output lineage and conserved quantity; no stale historical progress substitution.',
    244: 'Actual continued travel after management/preparation, preserving all earlier receipts and current state.',
}
assert set(focus) == set(route['checkpointRevisions'])
checkpoints=[]
for revision in route['checkpointRevisions']:
    name=f'r{revision:03d}.ddsave'
    path=old_dir/name
    assert digest(path)==files[name]
    previous=route['orderedCommands'][revision-1] if revision else None
    next_command=route['orderedCommands'][revision] if revision<len(route['orderedCommands']) else None
    checkpoints.append({
        'revision': revision, 'sourceExpectedFocus': focus[revision],
        'canonicalPredecessor': {'path': path.relative_to(ROOT).as_posix(), 'sha256': files[name], 'archive': route['archiveBinding']['index'], 'meaning': 'Expected unchanged authoritative state after the same exact command prefix; not new API qualification.'},
        'previousActualCommand': previous, 'nextActualCommand': next_command,
        'allApplicableReadOperations': ['DescribeCommandsV1', 'DiscoverCommandsV1', 'AssessCommandV1', 'DescribeChoicesV1', 'ExplainResultV1'],
        'actors': ['Hero', 'Companion', 'actual currently admitted source actor only for its authorized endpoint'],
        'seats': ['Player','FirstOpponent','RecoveryOpponent','FerryOpponent'],
        'expectedReadContract': [
            'ApiVersion1, exact current revision/profile/TEST_ONLY; field cardinality/order/type/width/dimension exactly VALUE_NORMALIZATION_INDEX and effective GPT decisions.',
            'Descriptions use exact original profile kind/payload constraints, public domains and source bindings. Finite examples obey EXAMPLE_RECIPE_INDEX and Core canonical order; no private target or inferred ownership.',
            'Assess next source command against exact current native prefix and shared pure facts; keep initial eligibility, definite commit capacity and conditional settlement separate. Privileged source commands use their actual operator/controller route.',
            'For the previous actual command and selected older receipts: exact authorized principal/fingerprint means AlreadyCommitted subject to current endpoint/Core rights, not fresh eligibility. Wrong principal/conflict/stale-observation controls preserve exact agreed order.',
            'Actual pending choices come only from this genuine snapshot and native current priority, with exact captured IDs, owner, domain and response continuation. Never synthesize pending choices from descriptions.',
            'Facts use independent source-bound native record joins and per-field current rights. Immediate facts only from real submission; old absent historical values NotRetained after authorization, current facts labelled current, protected fixed shapes Withheld.',
            'Compare all legacy ordered observations and canonical bytes against the pinned predecessor input plus equivalent V1 paths. No RNG, resolver, replay, settlement, reservation, validation or hidden condition fold is allowed in any read.',
        ],
        'fivePaths': route['paths'],
        'restartPlan': 'Strict save/restore at this boundary in TypedRestored/ConsoleRestored under original factory and parameters; compare before/after reads and continue next exact command. Other paths continue without reset.',
        'executed': False,
    })

factory_rows=[]
for f in profiles['factories']:
    factory_rows.append({
        'factory':f['factory'], 'exactDeclaration':f['exactDeclaration'], 'wire':f['wireEnvelope'], 'inMemorySchema':f['inMemorySchema'],
        'selectedParameterBinding':f['selectedParameterBinding'], 'kindGateCandidates':f['kindGateCandidates'],
        'checks':['Fresh factory all applicable V1 descriptions and no side effects','All four seat contexts plus enable/revoke transitions where supported','Original source actual branch route per BRANCH_QUALIFICATION_INDEX','Exact current conditions from owning published projection/journal modes','Strict own-policy restore with ordered legacy and V1 comparisons','No newest-profile-only gates for older admitted operations','Unsupported kind/payload/recipient/source context preserves native denial','Actual allowed consent/director/class selection arguments remain separate from defaults'],
        'historicalInput': None if f['factory'] in ['StartWithFishingTrap','StartWithConnectedWorkControl'] else next(({'wire':a['wire'],'sha256':a['sha256'],'inputTable':'authentic95Through116'} for a in authentic if a['wire']==f['wireEnvelope']),None),
        'ownProfileAdditionalInput': 'additionalOriginalProfileInputs factory='+f['factory'] if f['factory'] in ['StartWithFishingTrap','StartWithConnectedWorkControl'] else None,
        'sameWireException': 'Wire95 archive is original Start, not FishingTrap proof; wire116 archive is OMA, not work-control proof. Each separate factory uses its own genuine path/own save; preserve incompatible exact prefix rejection.',
        'executed':False,
    })
for entry in authentic:
    path=Path(entry['path'])
    assert path.is_file() and digest(path)==entry['sha256'], entry['wire']
    entry['path']=path.relative_to(ROOT).as_posix()
    entry['required']='Load under original policy/arguments, compare authentic bytes/old observations, replay actual receipts under original principal to equivalent boundaries and continue source-feasible command. Add pure V1 reads. Do not retag, migrate or adopt into a newer same-wire profile.'
    entry['executedForInt05']=False

result={
    'schemaVersion':1,'status':'FINITE_PROFILE_AND_CHECKPOINT_PLAN_NOT_EXECUTED',
    'reviewer':'Parent Codex self-review of frozen accepted predecessor inputs and independently audited profile declarations',
    'counts':{'factoryDeclarations':24,'authenticOldInputs':22,'principalCommands':244,'principalCheckpoints':28,'paths':5,'int05Executions':0},
    'factoryRows':factory_rows,'authentic95Through116':authentic,'principalCheckpoints':checkpoints,
    'additionalOriginalProfileInputs':[
        {'factory':'StartWithConnectedWorkControl','wire':116,'input':checkpoints[-1]['canonicalPredecessor'],'required':'Exact authentic work-control prefix; separate OMA116 compatibility and negative cross-profile restore in both directions.'},
        {'factory':'StartWithFishingTrap','wire':95,'required':'Own genuine initial/setup/retrieval path and saved boundaries; the existing plain Start95 archive does not establish this factory.'}],
    'oracleBoundary':'Expected values derive from original source clauses, frozen native record definitions and independent source dispositions. Qualification may decode genuine snapshots in the test harness to compare explicit native fields/lineage; it must not call the new field projection or copy its switch to manufacture expected output. Exact scalar values for new runtime checkpoints are retained during execution and reviewed against these bindings.',
    'sourcePins':[pin(PACKET/'PROFILE_ADMISSION_MATRIX.json'),pin(PACKET/'PRINCIPAL_ROUTE_ALLOCATION.json'),pin(MGT/'support/compatibility-sources.json'),pin(MGT/'support/WorkCompatibility.cs')],
    'runtimeAuthorized':False,'sourceApiAccepted':False,
}
(PACKET/'PROFILE_AND_CHECKPOINT_QUALIFICATION_PLAN.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(result['counts']))
