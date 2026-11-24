"""Freeze the observed second runtime checkpoint; this is not INT-05 acceptance."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]
ROOT=PACKET.parents[3]
ARTIFACTS=ROOT/'engine/artifacts/admitted-command-surface'
OUT=PACKET/'runtime-checkpoint-02'
OUT.mkdir(exist_ok=True)
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

paths={
    'development04-compile-failure.json':'development-04/run-20261124T032137808Z-290e6501/results.json',
    'development05-protocol.json':'development-05/run-20261124T032347782Z-f126adc7/results.json',
    'development06-protocol.json':'development-06/run-20261124T032558000Z-8d56c424/results.json',
    'development06-focused.json':'development-06/focused/results.json',
    'development06-package.json':'development-06/static-20261124T032654240Z-4bb81735/results.json',
    'candidate07-protocol.json':'development-07/run-20261124T032805134Z-728a60b6/results.json',
    'candidate07-focused.json':'development-07/focused/results.json',
    'candidate07-legacy.json':'development-07/legacy/results.json',
    'candidate07-package.json':'development-07/static-20261124T032853565Z-9fbbc6bc/results.json',
    'genuine-concentration.json':'development-07/genuine-concentration.json',
    'core-independent-review.json':'core-native-assessment-cross-review-01.json',
    'concentration-independent-review.json':'end-concentration-assessment-cross-review-01.json',
}
pins=[]
for name,rel in paths.items():
    source=ARTIFACTS/rel
    shutil.copyfile(source,OUT/name)
    pins.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
for name in ['core-independent-review.json','concentration-independent-review.json']:
    review=load(OUT/name)
    rows=review.get('reviewedSourcePins',review.get('sourcePins',[]))
    for row in rows:
        assert sha(ROOT/row['path'])==row['sha256'],('reviewed source changed',row['path'])
build=ARTIFACTS/'development-07/run-20261124T032805134Z-728a60b6'
compiled=load(build/'results.json')
assert compiled['status']=='PASS' and compiled['testsDiscovered']==1 and compiled['passed']==1
for name,count in [('candidate07-focused.json',5),('candidate07-legacy.json',10)]:
    r=load(OUT/name)
    assert r['status']=='PASS' and len(r['cases'])==count and all(c['Passed'] for c in r['cases'])
assert load(OUT/'candidate07-package.json')['status']=='PASS'
archive=OUT/'source-candidate07.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for row in sorted(compiled['sourceHashes'],key=lambda x:x['path']):
        source=ROOT/'engine'/row['path']
        assert sha(source)==row['sha256'],('compiled source changed',row['path'])
        info=zipfile.ZipInfo('engine/'+Path(row['path']).as_posix(),(2026,11,24,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,source.read_bytes())
with zipfile.ZipFile(archive) as z:
    for row in compiled['sourceHashes']:
        assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']
save_dir=ARTIFACTS/'development-07/focused/int05_genuine_concentration_assessment_execution_restore'
for p in sorted(save_dir.glob('*.ddsave')):
    shutil.copyfile(p,OUT/p.name)
    pins.append({'path':(OUT/p.name).relative_to(ROOT).as_posix(),'original':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})

summary={
    'status':'BOUNDED_NATIVE_ASSESSMENT_CHECKPOINT_NOT_MODULE_ACCEPTANCE',
    'contractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
    'predecessorCheckpointCommit':'dba75cbf6',
    'implemented':[
        'Owning Core pure assessment dispatch with current native authority, separate observation freshness, exact receipt retry and mandatory verified capability routing without fallback.',
        'Shared unchanged native preflight/payload guards return immutable per-call exact origin data; legacy adapters preserve original strings and guard order.',
        'Per-call prohibited-operation guards/counts at common owner/RNG/validation/resolver/replay/condition/deadline/reservation entries, including swallowed violations and error cleanup.',
        'First actual native operation: EndSpellConcentration initial admission, sharing its preceding selected guards and utility predicates with legacy execution.',
    ],
    'sourceArchive':{'path':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'compiledInputs':len(compiled['sourceHashes'])},
    'dlls':[{'name':p.name,'sha256':sha(p)} for p in sorted(build.glob('*.dll'))],
    'rawEvidence':pins,
    'actualExits':{'candidate07CompileAndProtocol':0,'candidate07FiveFocused':0,'candidate07TenLegacy':0,'candidate07Package':0,
        'development04Compile':1,'development05CompileAndProtocol':0,'development06CompileAndProtocol':0,'development06Focused':0,'development06Package':0},
    'developmentCorrections':[
        'Initial compilation failed because an instance recovery selector was called from a static helper; corrected without changing its rule.',
        'Independent Core review identified uncaught derived exceptions and uncounted public owner reentry; both corrected and covered by actual regressions.',
        'Independent native review identified unsupported CommitFeasibility=true: changed to null, and genuine check asserts only initial eligibility. Shared post-resolution tail and candidate feasibility remain unqualified.',
        'One focused-run launch used a nonexistent placeholder build directory and exited1 before tests/output-directory creation; corrected to the observed build path without restarting a live process.',
    ],
    'qualification':{'newCasesPassed':6,'existingCasesPassed':10,'genuineOperation':'wire109 cast at revision123, end at124, equal clock/RNG, exact retry, fresh denial, authenticated before/after restore',
        'full1601PredecessorReconciliation':'NOT RUN','fullFiveExecutionPaths':'NOT RUN','allFactoryAndBranchQualification':'NOT RUN'},
    'remaining':[
        'Complete all78 seat/two operator native assessment paths and exact origin/fact/conditional/capacity projections; only EndSpellConcentration initial admission is wired now.',
        'Implement public V1 session descriptions, assessment, discovery, choices, actual detailed submission, retained explanation and console parity.',
        'Wire actual private planning checkpoint comparison; the current verified-routing check is explicitly a technical probe, not genuine planning proof.',
        'Complete transitive instrumentation and all-profile copy/condition/purity/privacy/authority/save/replay qualification; current guarded entry tests are not complete call-graph proof.',
        'Complete all accepted branch/profile/five-path/regression requirements; obtain actual GPT final runtime acceptance; push accepted work and stop before successor.',
    ],
    'runtimeAccepted':False,'successorStarted':False,'unityIntegration':False,
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_02.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf8'))
print(json.dumps({'sourceArchive':summary['sourceArchive'],'newCasesPassed':6,'existingCasesPassed':10,'moduleAccepted':False},indent=2))
