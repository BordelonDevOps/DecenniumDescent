"""Retain actual utility checks, without promoting the unfinished INT-05 module."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]; ROOT=PACKET.parents[3]
ARTIFACTS=ROOT/'engine/artifacts/admitted-command-surface'; OUT=PACKET/'runtime-checkpoint-03'
OUT.mkdir(exist_ok=True)
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
build=ARTIFACTS/'development-08/run-20261124T033922229Z-9ad7d173'
paths={
 'candidate08-grounding.json':build/'results.json',
 'candidate08-utilities.json':ARTIFACTS/'development-08/utilities/results.json',
 'candidate08-package.json':ARTIFACTS/'development-08/static-20261124T034043698Z-19369163/results.json',
 'genuine-utilities.json':ARTIFACTS/'development-08/genuine-utilities.json',
 'independent-review.json':ARTIFACTS/'ground-focus-assessment-cross-review-01.json',
 'source-candidate08.zip':build/'source-frozen.zip',
}
genuine=load(paths['genuine-utilities.json'])
for row in genuine['states']:
 p=ROOT/row['path']; assert sha(p)==row['sha256']; paths[p.name]=p
pins=[]
for name,source in paths.items():
 shutil.copyfile(source,OUT/name)
 pins.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
report=load(OUT/'candidate08-grounding.json')
assert report['status']=='PASS' and report['testsDiscovered']==1 and report['passed']==1
utilities=load(OUT/'candidate08-utilities.json')
assert utilities['status']=='PASS' and len(utilities['cases'])==4 and all(c['Passed'] for c in utilities['cases'])
assert load(OUT/'candidate08-package.json')['status']=='PASS'
with zipfile.ZipFile(OUT/'source-candidate08.zip') as z:
 assert len(z.namelist())==len(report['sourceHashes'])
 for row in report['sourceHashes']:
  assert sha(ROOT/'engine'/row['path'])==row['sha256'],row['path']
  assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']
review=load(OUT/'independent-review.json');assert len(review['sourcePins'])>0
for row in review['sourcePins']: assert sha(ROOT/row['path'])==row['sha256'],row['path']
summary={
 'status':'BOUNDED_UTILITY_ASSESSMENT_CHECKPOINT_NOT_MODULE_ACCEPTANCE',
 'previousCheckpointCommit':'d2742031ad635b3fa0a48bae00ce9a84c9db94d7',
 'contractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
 'implemented':['Shared unchanged casting Action and ordinary magical context guards with exact per-call native origins.',
  'GroundCastingStrain and FocusDetectedAura initial assessments through the owning pure-read boundary; journal-time deadline checks and current condition/permission/sight projections remain distinct.',
  'Legacy native strings, ordering, action payment, grounding settlement and opaque aura selection remain shared with execution. No predicted terminal feasibility.'],
 'currentNativeInitialAssessmentKinds':['EndSpellConcentration','GroundCastingStrain','FocusDetectedAura'],
 'sourceInputs':len(report['sourceHashes']),
 'sourceArchiveSha256':sha(OUT/'source-candidate08.zip'),
 'dlls':[{'name':p.name,'sha256':sha(p)} for p in sorted(build.glob('*.dll'))],
 'rawEvidence':pins,
 'actualExits':{'compileAndGrounding':0,'fourUtilityChecks':0,'packageValidation':0},
 'currentCandidateChecks':{'newGenuineCasesPassed':2,'priorInt05CasePassed':1,'existingSpellCasesPassed':2,'totalPassed':5},
 'genuinePaths':[
  'Wire109: genuine cast and next own turn; grounding query leaves positive strain1 unchanged; payment at131; native interval settlement at132 reduces it to0, with retry and authenticated restore.',
  'Wire116: genuine objective and earned Detect; actual Guidance/Detect casts produce public aura; pure focus at223; paid focus224, with unchanged clock/RNG/RP/strain and authenticated restore.',
 ],
 'limits':['Native initial admission only. Complete public DTO/domain/cost/choice/diagnostic/result/console projections remain unimplemented.',
  'CommitFeasibility is null: the shared post-resolution tail, conditional constraints and terminal validation are not certified by initial admission.',
  'Three native kinds are not the required78 seat/two operator coverage. All accepted branch/profile/five-path/full-regression/privacy and actual GPT final-runtime gates remain open.',
  'Independent review was static only; executed results are the separate actual harness reports. Prior raw evidence remains intact.'],
 'runtimeAccepted':False,'successorStarted':False,'unityIntegration':False,
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_03.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed':5,'compiledInputs':len(report['sourceHashes']),'sourceArchiveSha256':summary['sourceArchiveSha256'],'moduleAccepted':False},indent=2))
