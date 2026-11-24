"""Retain frozen observation evidence without claiming complete INT-05 acceptance."""
from pathlib import Path
import json,hashlib,shutil,zipfile
PACKET=Path(__file__).resolve().parents[1]; ROOT=PACKET.parents[3]
OUT=PACKET/'runtime-observation-candidate16'; OUT.mkdir(exist_ok=True)
A=ROOT/'engine/artifacts/admitted-command-surface'; B=A/'development-16/run-20261124T125800563Z-20fe1eb6'
paths={'initial.json':B/'results.json','existing-observation.json':A/'development-16/observation/results.json',
 'package.json':A/'development-16/static-20261124T125843905Z-7e884c0a/results.json',
 'source-frozen.zip':B/'source-frozen.zip','independent-review.json':A/'reviews/observation-routing-review-01.json'}
for p in (B/'saves').glob('int05-*.ddsave'):paths[p.name]=p
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
assert load(paths['initial.json'])['passed']==1 and load(paths['initial.json'])['status']=='PASS'
existing=load(paths['existing-observation.json']);assert existing['status']=='PASS' and len(existing['cases'])==4
assert all(x['Passed'] for x in existing['cases']) and load(paths['package.json'])['status']=='PASS'
with zipfile.ZipFile(paths['source-frozen.zip']) as z:
 for row in load(paths['independent-review.json'])['sourcePins']:
  rel=row['path']; data=z.read(rel) if rel in z.namelist() else (ROOT/rel).read_bytes()
  assert hashlib.sha256(data).hexdigest()==row['workingTreeSha256'],rel
pins=[]
for name,src in paths.items():
 shutil.copyfile(src,OUT/name); pins.append({'path':name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'original':src.relative_to(ROOT).as_posix()})
summary={'status':'BOUNDED_OBSERVATION_ASSESSMENT_NOT_MODULE_ACCEPTANCE','sourceInputs':498,'checksPassed':5,
 'actualExitCodes':{'initial':0,'fourExistingCases':0,'package':0},
 'facts':['Repeated pure ordinary Hide/Search start/cancellation reads; genuine pending saves restored before cancellation and receipt retry.',
 'Four prior observation cases pass, including connected Hide/Search/combat/byte replay.',
 'Independent review detected and confirmed correction of native private SearchCandidateAmbiguous guard.'],
 'limits':['Candidate16 does not add pure tactical checks to the existing tactical case; candidate18 separately does.',
 'Missing-profile CancelExplorationSearch fallback remains open.',
 'No complete public V1, full module qualification, actual GPT acceptance or accepted push is claimed.'],
 'files':pins}
(OUT/'MANIFEST.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Retained',len(pins),'files and five passing cases; INT05 remains in progress.')
