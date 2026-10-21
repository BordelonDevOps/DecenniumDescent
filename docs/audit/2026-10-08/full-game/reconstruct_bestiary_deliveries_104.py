"""Independent data-only reconstruction of two preserved proposals; no canonical writes."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,zipfile
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P=A/'bestiary-deliveries-104'
OUT=A/'BESTIARY_DUAL_PROPOSAL_RECONSTRUCTION_104.json'
assert not OUT.exists()
def h(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(p.read_bytes())
def get(obj,pointer):
 for key in pointer.split('/')[1:]:
  key=key.replace('~1','/').replace('~0','~');obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 return obj
def parent(obj,pointer):
 prefix,key=pointer.rsplit('/',1);return get(obj,prefix),key.replace('~1','/').replace('~0','~')
def encode(obj,crlf=False):
 s=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
 return (s.replace('\n','\r\n') if crlf else s).encode()
checks=[]
def ck(n,ok):
 checks.append({'id':n,'pass':bool(ok)})
 assert ok,n
part=j(P/'DD_Bestiary_Recovery_Part01.json');model=j(P/'return02/MODEL.json');ops=j(P/'return02/EXACT_OPERATIONS.json')
with zipfile.ZipFile(A/part['baselineModel']['archive']) as z:basebytes=z.read(part['baselineModel']['member'])
base=json.loads(basebytes)
ck('original-source-binding',len(basebytes)==930613 and h(basebytes)==part['baselineModel']['sha256'])
ck('original-CRLF-byte-serialization',encode(base,True)==basebytes)
for row in part['sourceBindings']:
 with zipfile.ZipFile(A/row['archive']) as z:b=z.read(row['member'])
 ck('part01-source:'+row['id'],len(b)==row['bytes'] and h(b)==row['sha256'])
pwork=deepcopy(base)
for op in part['operations']:
 par,key=parent(pwork,op['path']);ck('part01-before:'+op['path'],op['op']=='add' and not op['beforePresent'] and key not in par)
 par[key]=deepcopy(op['after'])
for row in part['completeOriginalAndProposedRecords']:
 ck('part01-original:'+row['sourcePointer'],get(base,row['sourcePointer'])==row['originalCompleteRecord'])
 ck('part01-proposed:'+row['sourcePointer'],get(pwork,row['sourcePointer'])==row['proposedCompleteRecord'])
for op in reversed(part['operations']):
 par,key=parent(pwork,op['path']);ck('part01-after:'+op['path'],par[key]==op['after']);del par[key]
ck('part01-reverse-exact-source',encode(pwork,True)==basebytes)
def resolve(ref):
 if 'file' in ref:return get(j(P/'return02'/ref['file']),ref['pointer'])
 with zipfile.ZipFile(A/Path(ref['container']).name) as z:return get(json.loads(z.read(ref['member'])),ref['pointer'])
rwork=deepcopy(base)
ck('return02-operation-count',len(ops['operations'])==ops['operationCount']==70)
for op in ops['operations']:
 par,key=parent(rwork,op['path']);before=op['before'];after=op['after']
 ck('return02-before:'+op['path'],key in par and par[key]==resolve(before['valueRef']) if before['exists'] else key not in par)
 par[key]=deepcopy(resolve(after['valueRef']))
ck('return02-forward-entire-bytes',encode(rwork)==(P/'return02/MODEL.json').read_bytes())
for op in reversed(ops['operations']):
 par,key=parent(rwork,op['path']);ck('return02-after:'+op['path'],par[key]==resolve(op['after']['valueRef']))
 if op['before']['exists']:par[key]=deepcopy(resolve(op['before']['valueRef']))
 else:del par[key]
ck('return02-reverse-entire-bytes',encode(rwork,True)==basebytes)
differences=[
 {'id':'D104-PRESSURE-CONTROL','part01Pointer':'/selectedFullWording/BRP01-PW-01','return02Pointer':'/records/36/proposedOperation02/actions/2','part01':'10ft push, expressly no Prone','return02':'5ft push plus Prone','status':'CONSEQUENTIAL_NEW_AUTHORSHIP_FORK_PENDING_JOINT_SELECTION'},
 {'id':'D104-PRESSURE-RANGE','part01Pointer':'/selectedFullWording/BRP01-PW-01','return02Pointer':'/authorship02/sharedRules/1','part01':'30ft emitter-to-actual-interior-point Euclidean ray','return02':'General native range uses minimum occupied-body separation; individual Wave does not explicitly override it','status':'WITNESS_AND_ORIGIN_PRECEDENCE_NEEDS_EXPLICIT_RECONCILIATION'},
 {'id':'D104-TAIL-SAVE','part01Pointer':'/selectedFullWording/BRP01-DIM-TAIL-01','return02Pointer':'/records/15/proposedOperation02/tacticCompletions/0','part01':'DEX DC13 on-hit Prone rider','return02':'STR DC13 on-hit Prone rider','status':'CONSEQUENTIAL_NEW_AUTHORSHIP_FORK_PENDING_JOINT_SELECTION'},
 {'id':'D104-CONSTRICT-ESCAPE','part01Pointer':'/selectedFullWording/BRP01-SNAKE-CONSTRICT-01','return02Pointer':'/records/22/proposedOperation02/tacticCompletions/0','part01':'Action STR(Athletics) or DEX(Acrobatics) fixed-DC14 task with actual proficiency only','return02':'Action STR or DEX saving throw DC14','status':'TASK_VERSUS_SAVE_MECHANICS_FORK_PENDING_JOINT_SELECTION'},
 {'id':'D104-CONSTRICT-SIZE','part01Pointer':'/selectedFullWording/BRP01-SNAKE-CONSTRICT-01','return02Pointer':'/records/22/proposedOperation02/tacticCompletions/0','part01':'Up to one size larger than Huge snake, actual coiling contact required','return02':'No larger than Huge snake','status':'TARGET_ELIGIBILITY_FORK_PENDING_JOINT_SELECTION'}
]
for row in differences:
 row['completePart01Value']=get(part,row['part01Pointer']);row['completeReturn02Value']=get(model,row['return02Pointer'])
report={'id':'BESTIARY-DUAL-PROPOSAL-RECONSTRUCTION-104','status':'SOURCE_AND_REVERSIBILITY_VERIFIED_WITH_UNRESOLVED_SEMANTIC_FORKS','passed':len(checks),'failed':0,'checks':checks,'differences':differences,'distinctScopes':['Part01 only BV3-04/05/06; other24 mapped questions intentionally open.','Return02 is whole proposed bestiary with additional native actions, traits, geometry, materials, knowledge and lifecycle authorship; completeness claim is not independently accepted.','Return02 adds Containment Pulse to eligible charged Multiattack slots; Part01 deliberately excludes it from bounded scope. This is scope expansion requiring review, not automatically an accidental contradiction.'],'interimBoundary':'Earlier visible interim Part01 hashes and counts differ from the actual final downloaded files. Interim claims are history only; the preserved final Part01 has23 cases,56 transitions,5 operations and279 self-reported checks.','noCanonicalWrites':True,'noDownloadedCodeExecuted':True,'noRuntimeTests':True,'notAcceptance':True}
with OUT.open('xb') as f:f.write(encode(report))
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'passed':len(checks),'failed':0,'unresolvedForks':len(differences),'report':str(OUT)}))
