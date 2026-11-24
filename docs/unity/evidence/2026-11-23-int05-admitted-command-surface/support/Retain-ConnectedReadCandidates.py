"""Retain raw failures and successful connected read evidence without relabeling acceptance."""
from pathlib import Path
import json,hashlib,shutil
PACKET=Path(__file__).resolve().parents[1];ROOT=PACKET.parents[3]
A=ROOT/'engine/artifacts/admitted-command-surface';OUT=PACKET/'runtime-connected-read-candidates'
OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
pins=[];runs=[]
def retain(p,rel):
 target=OUT/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha(target)==sha(p),('retained evidence differs',str(target))
 else:shutil.copyfile(p,target)
 pins.append({'path':rel.as_posix(),'original':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
for n in range(17,29):
 folder=A/f'development-{n}'
 for result in sorted(folder.rglob('results.json')):
  report=load(result);run=result.parent
  row={'candidate':n,'path':str(result.relative_to(A)).replace('\\','/'),'status':report['status'],
       'passed':report.get('passed'),'failed':report.get('failed'),
       'observedExitCode':0 if report['status']=='PASS' else 1,
       'sourceArchiveRetained':(run/'source-frozen.zip').exists(),
       'assemblies':[{'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(run.glob('*.dll'))]}
  runs.append(row);retain(result,result.relative_to(A))
  for p in run.glob('source-frozen.zip'):
   retain(p,p.relative_to(A))
  for p in run.glob('*.compile.log'):
   retain(p,Path('logs')/('c'+str(n)+'-'+p.name))
 # These are original successful producer saves and rejection diagnostic inputs, never fabricated acceptance.
 for p in sorted(folder.rglob('int05-*.ddsave')):
  retain(p,Path('saves')/('c'+str(n)+'-'+sha(p)[:12]+'.ddsave'))
for name in ['strain-diagnostic-result.json','strain-validation-diagnostic.json','strain-before-failed-advance.ddsave']:
 p=A/'development-18'/name
 if p.exists():retain(p,p.relative_to(A))
for name in ['strain-source-review-01.json','strain-consistency-fix-review-01.json',
 'management-extraction-source-review-02.json','appraisal-bill-patch-review-01.json',
 'charter-readiness-patch-review-01.json','planning-patch-review-01.json',
 'closure-work-routing-review-01.json','formula-candidate26-and-named-runner-review-01.json']:
 p=A/'reviews'/name;retain(p,Path('reviews')/name)
manifest={'status':'PARTIAL_INT05_RUNTIME_EVIDENCE_NOT_FINAL_ACCEPTANCE','runs':runs,'files':pins,
 'facts':['Candidate17 failed on diagonal pickup; candidate18 corrected route reached the real recovery boundary and failed strict validation.',
 'Candidate20 passed after preserving actual completion links and admitting the existing suspended recovery continuation.',
 'Candidate25 passed genuine planning, genuine Strain recovery with forged-save rejection checks, owner isolation and private canonical comparison.',
 'Candidates21-24 are retained compiler failures, not gameplay passes; candidate25 uses actual package assembly identities.',
 'Candidate19 passed appraisal, bill, charter agreement and charter execution, plus package validation.'],
 'limits':['Initial eligibility only; full feasibility, all public V1 surfaces, full regression and five whole paths remain incomplete. Owner accepted this current deliverable and ordered immediate push/GPT handoff; this is not actual final GPT acceptance.',
 'Independent reviews are static source reviews, not final GPT acceptance.',
 'Source archives and loaded assembly hashes bind these runs; old failed results remain FAIL.']}
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Retained',len(runs),'raw runs and',len(pins),'inputs; bytes',sum(x['bytes'] for x in pins))
