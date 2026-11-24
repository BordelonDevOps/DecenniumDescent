"""Document/source integrity checks only; no C# build, test or gameplay claim."""
import hashlib
import json
import subprocess
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '78dcd8632b3f7ddf2f1353bb69ec1096f9effd7f'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

manifest = load(PACKET/'CHECKPOINT_06_INPUT_MANIFEST.json')
reports = sorted(ROOT/row['path'] for row in manifest['reports'])
for row in manifest['reports']:
    assert digest((ROOT/row['path']).read_bytes())==row['sha256'], ('report changed',row['path'])
# Previously retained review inputs may intentionally have an older design hash.
aliases = {}
for name in ['RETAINED_INPUT_ALIASES_05.json','INPUT_VERSION_RECONCILIATION_04.json','INPUT_VERSION_RECONCILIATION_05.json','INPUT_VERSION_RECONCILIATION_06.json']:
    doc=load(PACKET/name)
    for row in doc.get('aliases',[])+doc.get('historicalInputs',[]):
        aliases[(row['originalPath'],row['sha256'])]=ROOT/row['retainedPath']

packet_bytes={}
for p in PACKET.rglob('*'):
    if p.is_file():
        packet_bytes.setdefault(digest(p.read_bytes()),p)
verified=set(); uses=[]; native={}; examined=0
arrays=['pins','sourcePins','inputPins','reviewedDocuments','referencePins','contractPins','nativeSourcePins','independentlyInspectedNativePins','principalNativeSourcePins','inputs','nativePins','evidencePins','sourceAndInputPins']
for report_path in reports:
    report=load(report_path);examined+=1
    for key in arrays:
        items=report.get(key,[])
        if not isinstance(items,list): continue
        for row in items:
            if not isinstance(row,dict) or not {'path','sha256'}<=row.keys(): continue
            path,sha=row['path'],row['sha256']
            candidates=[ROOT/path,PACKET/path]
            match=next((p for p in candidates if p.is_file() and digest(p.read_bytes())==sha),None)
            if match is None:
                old=aliases.get((path,sha),packet_bytes.get(sha))
                assert old is not None and old.is_file() and digest(old.read_bytes())==sha,(report_path.name,path,sha)
                match=old
                uses.append({'report':report_path.name,'originalPath':path,'retainedPath':old.relative_to(ROOT).as_posix(),'sha256':sha})
            if path.startswith('engine/com.decennium.foundation/'):
                if path not in native: native[path]=git('show',BASELINE+':'+path)
                assert digest(native[path])==sha,(report_path.name,path,'native drift')
            verified.add((path,sha))

values=load(PACKET/'VALUE_NORMALIZATION_INDEX.json')
examples=load(PACKET/'EXAMPLE_RECIPE_INDEX.json')
assert values['counts']=={'operationKinds':80,'uniqueDefinitions':1097,'operationFieldReferences':2850,'fixedListDefinitions':23}
assert examples['counts']=={'candidateKinds':78,'operatorKinds':2,'candidateAxes':204,'registeredVariants':145,'executedExampleRecipes':0}
plans=load(PACKET/'PHYSICAL_TACTICAL_BRANCH_QUALIFICATION_PLAN.json')
assert plans['counts']=={'candidateKinds':33,'candidateAxes':96,'executed':0}
assert len(plans['operatorOperations'])==2
branches=load(PACKET/'BRANCH_QUALIFICATION_INDEX.json')
assert branches['counts']=={'candidateKinds':78,'candidateAxes':204,'operatorKinds':2,'newApiQualifiedBranches':0}
profiles=load(PACKET/'PROFILE_AND_CHECKPOINT_QUALIFICATION_PLAN.json')
assert profiles['counts']=={'factoryDeclarations':24,'authenticOldInputs':22,'principalCommands':244,'principalCheckpoints':28,'paths':5,'int05Executions':0}
for name in ['StartWithFishingTrap','StartWithConnectedWorkControl']:
    row=next(f for f in profiles['factoryRows'] if f['factory']==name)
    assert row['historicalInput'] is None and row['ownProfileAdditionalInput'].endswith(name)
for row in profiles['authentic95Through116']:
    assert digest((ROOT/row['path']).read_bytes())==row['sha256']
for row in profiles['principalCheckpoints']:
    p=row['canonicalPredecessor'];assert digest((ROOT/p['path']).read_bytes())==p['sha256']
units=load(PACKET/'OWNED_LOT_UNIT_BINDINGS.json')
assert [r['unit'] for r in units['units']]==['TEST_ONLY.ration-pound','prototype.potable-water.pint','mass-pound','TEST_ONLY.genuine-copper-piece','drop-black_blood_sample']
assert len(load(PACKET/'OWNED_LOT_UNIT_CROSS_REVIEW_01.json')['factoryMatrix'])==24
diagnostics=load(PACKET/'DIAGNOSTIC_ORIGIN_INDEX.json')
assert diagnostics['counts']=={'registeredPublicCodes':30,'registeredStages':8,'originalCandidateDispositions':74,'namedMissingRootsDispositioned':35,'uniqueExactOrigins':1421,'originBindings':1495,'overlappingOrigins':74,'newApiExecutions':0}
assert {r['originalIndex'] for r in diagnostics['missingRootDispositions']}==set(range(35))
for row in diagnostics['origins']:
    assert row['effectiveSourceBinding']==row['bindings'][-1]
    for binding in row['bindings']:
        doc=load(PACKET/binding['document'])
        for part in binding['pointer'].strip('/').split('/'):
            doc=doc[int(part)] if isinstance(doc,list) else doc[part]
        assert isinstance(doc,dict)
assert not git('diff',BASELINE,'--','engine/com.decennium.foundation','engine/tools','engine/hosts').strip()
for name in ['OPERATION_INVENTORY.json','PROFILE_ADMISSION_MATRIX.json','MODULE_DEFINITION.md','PRINCIPAL_ROUTE_ALLOCATION.json']:
    path=PACKET/name
    assert path.read_bytes()==git('show',BASELINE+':'+path.relative_to(ROOT).as_posix())
for name in ['VALUE_NORMALIZATION_INDEX.json','EXAMPLE_RECIPE_INDEX.json','OWNED_LOT_UNIT_BINDINGS.json','PHYSICAL_TACTICAL_BRANCH_QUALIFICATION_PLAN.json','PROFILE_AND_CHECKPOINT_QUALIFICATION_PLAN.json']:
    d=load(PACKET/name);assert not d.get('sourceApiAccepted',False) and not d.get('runtimeAuthorized',False)

print(json.dumps({
    'status':'PASS_DOCUMENT_AND_SOURCE_INTEGRITY_ONLY','baseline':BASELINE,
    'newJsonReportsExamined':examined,'uniqueTopLevelDeclaredPathHashPairs':len(verified),'nativeGitBlobsVerified':len(native),
    'retainedHistoricalOrAliasUses':uses,
    'normalizationCounts':values['counts'],'exampleCounts':examples['counts'],
    'parentBranchPlanCounts':plans['counts'],'profileCheckpointCounts':profiles['counts'],
    'allBranchPlanCounts':branches['counts'],
    'diagnosticCounts':diagnostics['counts'],
    'exactUnitBindings':5,'runtimeToolsHostsUnchanged':True,
    'runtimeBuildsTestsOrGameplayExecuted':False,'sourceApiAccepted':False,
    'limits':'Integrity and structural reconciliation do not establish source semantics, disclosure, full transitive purity or gameplay. Each review retains its precise actual scope.',
},indent=2))
