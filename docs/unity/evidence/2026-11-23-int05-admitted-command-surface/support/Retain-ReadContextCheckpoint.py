"""Retain actual bounded implementation checks. This does not qualify INT-05."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ARTIFACTS = ROOT/'engine/artifacts/admitted-command-surface'
OUT = PACKET/'runtime-checkpoint-01'
OUT.mkdir(exist_ok=True)

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

paths = {
    'development01-test.json':'development-01/run-20261124T025853902Z-ab54d1a0/results.json',
    'development02-test.json':'development-02/run-20261124T030034512Z-ffbf150e/results.json',
    'development02-focused.json':'development-02/focused-read-context/results.json',
    'development02-package.json':'development-02/static-20261124T030206432Z-e11b3c52/results.json',
    'candidate03-test.json':'development-03/run-20261124T030556431Z-b2790313/results.json',
    'candidate03-focused.json':'development-03/focused-read-context/results.json',
    'candidate03-package.json':'development-03/static-20261124T030657201Z-2214be34/results.json',
    'condition-disposal-independent-review.json':'condition-scope-disposal-cross-review-01.json',
    'core-read-context-independent-review.json':'core-read-context-cross-review-01.json',
}
retained=[]
for name, original in paths.items():
    source=ARTIFACTS/original
    shutil.copyfile(source, OUT/name)
    retained.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
build=ARTIFACTS/'development-03/run-20261124T030556431Z-b2790313'
report=load(build/'results.json')
assert report['status']=='PASS' and report['testsDiscovered']==1
source_rows=report['sourceHashes']
archive=OUT/'source-candidate03.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for row in sorted(source_rows,key=lambda r:r['path']):
        source=ROOT/'engine'/row['path']
        assert sha(source)==row['sha256'], ('compiled source changed',row['path'])
        entry=zipfile.ZipInfo('engine/'+Path(row['path']).as_posix(),(2026,11,24,0,0,0))
        entry.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(entry,source.read_bytes())
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==len(source_rows)
    for row in source_rows:
        assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']

summary={
    'status':'BOUNDED_READ_INFRASTRUCTURE_CHECKPOINT_NOT_MODULE_ACCEPTANCE',
    'contractCandidate':'67f3d201b202ab2f815ab69940682f04e78c511c',
    'actualContractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
    'acceptanceRecordCommit':'79afcf51f18bdfb84fa8aa1cd26ac0725f2bc7dc',
    'implemented':[
        'Core-owned unforgeable stamp/context and immutable accepted projection pair; current owner generation invalidates stale context.',
        'Construction/validated-commit projection publication; rejection/duplicate retention; guarded nonreentrant provider with current-generation unavailable detail on failure.',
        'Narrow immutable condition journal-time/current-marker materialization and strict lookup; guarded lifecycle entry points and disposal lifetime.',
        'One private canonical writer reused by public validated Encode and internal comparison, with exact gated LabModel friend access.',
    ],
    'candidateSourceArchive':{'path':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'compiledInputs':len(source_rows)},
    'candidateDlls':[{'name':f.name,'sha256':sha(f)} for f in sorted(build.glob('*.dll'))],
    'rawEvidence':retained,
    'commandsAndActualExits':[
        {'command':'pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -ResultsRoot engine/artifacts/admitted-command-surface/development-03 -CaseName int05_read_context_owner_generation_and_failure_isolation','exitCode':0},
        {'command':'pwsh -NoProfile -File docs/unity/evidence/2026-11-23-int05-admitted-command-surface/support/Run-FocusedReadContext.ps1 -AssemblyRoot engine/artifacts/admitted-command-surface/development-03/run-20261124T030556431Z-b2790313 -ResultsDirectory engine/artifacts/admitted-command-surface/development-03/focused-read-context','exitCode':0},
        {'command':'pwsh -NoProfile -File engine/tools/Validate-Package.ps1 -ResultsRoot engine/artifacts/admitted-command-surface/development-03','exitCode':0},
    ],
    'tests':{'focusedNewCases':3,'passed':3,'fullPredecessorRegression':'NOT RUN','newConnectedFivePaths':'NOT RUN'},
    'remaining':[
        'Actual Core/policy assessment dispatch, pure family extraction, all admitted command/choice/domain/fact/result surfaces and console adapters.',
        'Strict read instrumentation across all forbidden call paths, full alias/copy/consumer qualification and materializer phase/expiry/current-versus-journal cases.',
        'All required gameplay/branch/profile/pending/authority/privacy/save/replay qualification on one final frozen candidate.',
        '1601 predecessor reconciliation plus meaningful new cases; actual final GPT review and Codex acceptance; accepted push then stop.',
    ],
    'sourceApiAccepted':True,'finalRuntimeAccepted':False,'unityIntegration':False,'successorStarted':False,
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_01.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf8'))
print(json.dumps({'sourceArchive':summary['candidateSourceArchive'],'rawReports':len(retained),'focusedCases':3,'moduleAccepted':False},indent=2))
