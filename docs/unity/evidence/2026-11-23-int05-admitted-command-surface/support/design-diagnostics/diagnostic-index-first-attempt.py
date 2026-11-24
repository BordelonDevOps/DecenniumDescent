"""Join frozen design audits by exact native origin; no runtime qualification."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]

def load(name):
    return json.loads((PACKET / name).read_text(encoding='utf-8-sig'))

def save(name, value):
    (PACKET / name).write_bytes((json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode('utf8'))

def pin(name):
    p = PACKET / name
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}

inputs = [
    'PUBLIC_DENIAL_VOCABULARY_PROPOSAL.json',
    'PUBLIC_DENIAL_CANDIDATE_CLOSURE_01.json',
    'PUBLIC_DENIAL_PHYSICAL_TACTICAL_ORIGINS.json',
    'PUBLIC_DENIAL_PHYSICAL_TACTICAL_CORRECTIONS.json',
    'MAGIC_CARE_DENIAL_ORIGIN_MAPPING_PROPOSAL.json',
    'INDEPENDENT_MAGIC_CARE_PLAN_AND_MANAGEMENT_ORIGIN_REVIEW.json',
    'PUBLIC_DENIAL_REMAINING_NATIVE_ORIGINS_01.json',
    'SAFE_DIAGNOSTIC_CONTRACT_PROPOSAL.md',
    'SOURCE_AND_BRANCH_CORRECTIONS_06.json',
]
registry = {}

def add(file, pointer, origin, token, role, code=None, overrides=None):
    line = origin.get('line', origin.get('nativeReturnLine'))
    key = (origin['path'], line, token)
    assert line and token, (file, pointer, origin)
    row = registry.setdefault(key, {'path': key[0], 'line': line, 'nativeToken': token, 'bindings': []})
    binding = {'document': file, 'pointer': pointer, 'sourceRole': role, 'proposedPublicCode': code}
    if overrides:
        binding['effectiveOverrides'] = overrides
    row['bindings'].append(binding)

v = load(inputs[0])
for i, row in enumerate(v['nativeMappings']):
    for j, origin in enumerate(row['sourceOrigins']):
        add(inputs[0], f'/nativeMappings/{i}/sourceOrigins/{j}', origin, row['nativeCode'], 'INITIAL_EXACT_SOURCE_MAPPING_WITH_OPERATION_PROFILE_RESTRICTIONS', row['publicCode'])

c = load(inputs[1])
for i, row in enumerate(c['rows']):
    for j, origin in enumerate(row['originalOrigins']):
        add(inputs[1], f'/rows/{i}/originalOrigins/{j}', origin, row['nativeToken'], row['disposition'], row.get('publicCode'))

corrections = load(inputs[3])['overrides']
parent = load(inputs[2])
for i, row in enumerate(parent['rows']):
    overrides = [f"{inputs[3]}#/overrides/{j}" for j, fix in enumerate(corrections)
                 if row['origin']['path'].endswith('/'+fix['file']) and row['origin']['line'] in fix['lines']]
    add(inputs[2], f'/rows/{i}', row['origin'], row['nativeToken'], 'EXACT_PARENT_MAPPING_SUBJECT_TO_LINKED_OVERRIDES', row['publicCodeProposal'], overrides)
for i, row in enumerate(parent['excludedOrigins']):
    add(inputs[2], f'/excludedOrigins/{i}', row['origin'], row['nativeToken'], 'EXPLICIT_SELECTED_PROFILE_EXCLUSION')

magic = load(inputs[4])
for i, row in enumerate(magic['rows']):
    mapping = row.get('primaryMapping') or {}
    add(inputs[4], f'/rows/{i}', row['origin'], row['origin']['nativeCode'], row['status'], mapping.get('publicCode', mapping.get('proposedPublicCode')))

management = load(inputs[5])['denialOriginSupplement']
for i, row in enumerate(management['mappings']):
    add(inputs[5], f'/denialOriginSupplement/mappings/{i}', row, row['nativeCode'], 'EXACT_SELECTED_MANAGEMENT_ORIGIN_MAPPING', row['proposedPublicCode'])

last = load(inputs[6])
for field in ['rows','existingSharedWorldOriginReconciliation']:
    for i, row in enumerate(last[field]):
        add(inputs[6], f'/{field}/{i}', row['origin'], row['nativeToken'], row['sourceRole'], row['publicCodeProposal'])

root_bindings=[]
magic_indices={0,1,2,3,4,5,6,7,19,20}
management_indices={8,9,10,11,12,13}
parent_indices={14,15,21,22,23,24,25,26,27}
last_indices={16,17,18,28,29,30,31,32,33,34}
assert magic_indices|management_indices|parent_indices|last_indices==set(range(35))
for i, entry in enumerate(c['omittedSelectedOrigins']):
    if i in magic_indices:
        supplements=[inputs[4]]
    elif i in management_indices:
        supplements=[inputs[5]+'#/denialOriginSupplement']
    elif i in parent_indices:
        supplements=[inputs[2], inputs[3]]
        if i==14:
            supplements.append(inputs[5]+'#/denialOriginSupplement')
    else:
        supplements=[inputs[6]]
    rows=[r for r in registry.values() if r['path']==entry['path'] and any(b['document'] in [s.split('#')[0] for s in supplements] for b in r['bindings'])]
    root_bindings.append({'originalIndex':i, 'nativeRoot':entry['path'], 'frozenScope':entry['methodsOrRanges'], 'supplements':supplements, 'indexedExactOriginsInFile':len(rows), 'disposition':'FINITE_SELECTED_ROOT_SOURCE_DISPOSITION; explicit nonadmitted, mutation-only, forwarding and committed-stop roles remain distinct; not a runtime coverage claim'})
    assert rows or any(r['originListIndex']==i for r in last['roots']), (i,entry)

rows=sorted(registry.values(),key=lambda r:(r['path'],r['line'],r['nativeToken']))
overlaps=[]
for row in rows:
    if len(row['bindings'])<2:
        continue
    codes=sorted({b['proposedPublicCode'] for b in row['bindings'] if b['proposedPublicCode']})
    overlaps.append({'path':row['path'],'line':row['line'],'nativeToken':row['nativeToken'],'codesBeforeEffectiveOverrides':codes,'bindingCount':len(row['bindings'])})

save('DIAGNOSTIC_ORIGIN_INDEX.json', {
    'schemaVersion':1,
    'status':'CONSOLIDATED_FINITE_SOURCE_DESIGN_FOR_ACTUAL_GPT_REVIEW_NOT_RUNTIME_ACCEPTANCE',
    'scope':'Join the original bounded vocabulary, exact74 candidate dispositions and all35 named missing-root supplements. This index preserves source roles and does not assert a compiler-derived whole-call-graph proof.',
    'rules':[
        'Each key includes native path, line and token; selected operation/variant/profile and exact predicates remain in linked bindings. No token-global dispatch.',
        'Exact physical/tactical corrections override only their named rows. Source/branch corrections override only their named frozen plan locations.',
        'A later exact-source supplement refines the initial grouped-token proposal at that origin; exclusions apply only to their proven selected profile/caller path.',
        'Exceptions caught as PolicyFailure, committed contact stops, mutation-only delegates and forwarded guards are distinct from initial rejected commands.',
        'All thirty codes/eight stages and per-origin disclosure proposals require actual GPT agreement; origin capture must be immutable per call and preserve native guard order.',
        'Unknown required origin is a qualification defect. Native absence is never automatically ProjectionUnavailable. Current authorized explanations remain required.',
    ],
    'inputPins':[pin(n) for n in inputs],
    'counts':{'registeredPublicCodes':len(v['codes']),'registeredStages':len(v['proposedPublicStages']),'originalCandidateDispositions':len(c['rows']),'namedMissingRootsDispositioned':len(root_bindings),'uniqueExactOrigins':len(rows),'originBindings':sum(len(r['bindings']) for r in rows),'overlappingOrigins':len(overlaps),'newApiExecutions':0},
    'missingRootDispositions':root_bindings,
    'origins':rows,
    'overlapReconciliation':overlaps,
    'forwardedAndDelegatedSource':inputs[6]+'#/forwardingBoundaries',
    'sourceApiAccepted':False,'runtimeAuthorized':False,'runtimeChanged':False,
})
print(json.dumps({'counts':load('DIAGNOSTIC_ORIGIN_INDEX.json')['counts'],'distinctCodeOverlaps':[r for r in overlaps if len(r['codesBeforeEffectiveOverrides'])>1]},indent=2))
