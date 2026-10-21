from pathlib import Path
import datetime,hashlib,json,zipfile
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');OUT=A/'joint-followthrough-verdict-110';OUT.mkdir(exist_ok=False)
P=Path(r'C:\Users\cbord\Downloads\DD_Joint_Followthrough_109_Review_01.zip');checks=[]
def h(b):return hashlib.sha256(b).hexdigest()
def ser(x):return (json.dumps(x,ensure_ascii=False,indent=2)+chr(10)).encode()
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
def write(p,b):
 with p.open('xb') as f:f.write(b)
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':h(b)}
b=P.read_bytes();ck('Actual final archive matches visible/native final',len(b)==25079 and h(b)=='23659921391528e0845879a6d68f4bdc8fd7703928da3ae6bad3ee0961df8d92');write(OUT/P.name,b)
with zipfile.ZipFile(P) as z:
 ck('Five exact safe text/data members',set(z.namelist())=={'DECISION.json','EVIDENCE_COVERAGE.json','MANIFEST.json','REVIEW.md','VALIDATION_REPORT.json'} and len(z.namelist())==5)
 ck('CRC',z.testzip() is None)
 m=json.loads(z.read('MANIFEST.json'))
 for row in m['files']:
  data=z.read(row['path']);ck('Manifest '+row['path'],len(data)==row['bytes'] and h(data)==row['sha256'])
 for name in z.namelist():write(OUT/name,z.read(name))
 d=json.loads(z.read('DECISION.json'));e=json.loads(z.read('EVIDENCE_COVERAGE.json'))
for key in ['outer','planarNested','fxc06Mapping']:
 row=d['input'][key];actual=bind(A/row['path']);ck('Exact submitted source '+key,actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'])
for row in d['item2']['beforeAfterBindings']:
 for side in ['before','after']:
  expected=row[side];actual=bind(A/'feat335-planar-reference-108'/expected['path']);ck('Current bound '+side+' '+row['file'],actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'])
ck('Eight complete mirror successors',len(d['item2']['beforeAfterBindings'])==8 and not d['item2']['necessaryCorrections'])
mapping=json.loads((A/'FEAT335_FXC06_EXACT_MAPPING_108.json').read_bytes())
ck('Exact complete FXC06 requirement',e['completeOriginalRequirement']==mapping['completeOriginalRequirement']==d['item3']['completeOriginalRequirement'])
for area in e['areas']:
 row=mapping['namedRequirementMap'][area['areaIndex']]
 ck('Exact original case partition '+area['area'],area['originalCaseIds']==[x['id'] for x in row['originalCases']])
 ck('Exact later case partition '+area['area'],area['laterCaseIds']==[x['id'] for x in row['acceptedScopedNewCases']])
ck('Named source evidence confirmed only',d['item3']['authoredNamedRequirementSatisfied'] and not d['item3']['parent335Accepted'] and not d['item3']['parentGlobalGateFlagsModified'] and not d['item3']['necessaryCorrections'])
ck('No change operations or new gameplay rules',not d['noChanges']['sourcePointerOperations'] and d['noChanges']['newGameplayRules']==0 and not d['noChanges']['canonicalApplied'])
report={'id':'JOINT-FOLLOWTHROUGH-109-VERDICT-INTAKE-110','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ACTUAL_FINAL_RECEIVED_AND_EXACT_BOUND_SCOPED_VERDICTS_RECORDED','archive':bind(OUT/P.name),'decision':bind(OUT/'DECISION.json'),'coverage':bind(OUT/'EVIDENCE_COVERAGE.json'),'verdicts':d['verdicts'],'currentPlanarMirrorsConfirmed':8,'currentFXC06NamedAuthoredEvidenceCovered':True,'historicalFT84HoldsRetained':d['holds'],'scope':'Local checks validate actual delivered data and its exact input/eight-file/case partition bindings. The618GPT checks remain separately reported evidence; neither previous local programs nor supplied scripts were executed. No broader gameplay/parent/runtime approval or flag mutation.','passed':len(checks),'failed':0,'checks':checks,'runtimeExecuted':False,'canonicalApplied':False,'parent335Accepted':False}
write(OUT/'LOCAL_INTAKE.json',ser(report));receipt={k:report[k] for k in ['id','status','archive','decision','coverage','verdicts','currentPlanarMirrorsConfirmed','currentFXC06NamedAuthoredEvidenceCovered','passed','failed','canonicalApplied','parent335Accepted']};receipt['report']=bind(OUT/'LOCAL_INTAKE.json')
write(A/'JOINT_FOLLOWTHROUGH_VERDICT_RECEIPT_110.json',ser(receipt));write(A/Path(__file__).name,Path(__file__).read_bytes());print(json.dumps(receipt))
