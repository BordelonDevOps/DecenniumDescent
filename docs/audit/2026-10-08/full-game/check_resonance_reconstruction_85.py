from pathlib import Path
from copy import deepcopy
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';P=A/'rank9-resonance-fields3-part5-return-01'
OUT=A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_RECONSTRUCTION_85.json';SAVED=A/Path(__file__).name
assert not OUT.exists() and not SAVED.exists()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sh(b):return hashlib.sha256(b).hexdigest()
def valuehash(v):return sh(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sh(b)}
checks=[]
def ck(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
ops=j(P/'EXACT_OPERATIONS_FROM_SOURCE.json');model=j(P/'MODEL.json');model_bytes=(P/'MODEL.json').read_bytes()
with zipfile.ZipFile(P/ops['baseline']['archive']) as z:original_bytes=z.read(ops['baseline']['member'])
old=json.loads(original_bytes)
ck('Exact original bytes before reconstruction',len(original_bytes)==ops['baseline']['bytes'] and sh(original_bytes)==ops['baseline']['sha256'])
ck('Exact21 full-value operations',ops['operationCount']==21 and len(ops['operations'])==21)
def parts(pointer):return [s.replace('~1','/').replace('~0','~') for s in pointer.lstrip('/').split('/')] if pointer else []
def at(root,pointer):
 v=root
 for key in parts(pointer):v=v[int(key)] if isinstance(v,list) else v[key]
 return v
def parent(root,pointer):
 ps=parts(pointer);assert ps
 v=root
 for key in ps[:-1]:v=v[int(key)] if isinstance(v,list) else v[key]
 return v,ps[-1]
def exists(root,pointer):
 try:at(root,pointer);return True
 except (KeyError,IndexError):return False
def resolve(binding):
 if not binding['present']:return None
 ref=binding['valueRef']
 if 'archive' in ref:
  ck('Reference binds complete original candidate',ref['archive']==ops['baseline']['archive'] and ref['member']==ops['baseline']['member']);v=at(old,ref['pointer'])
 else:
  ck('Reference binds complete delivered MODEL',ref['file']=='MODEL.json');v=at(model,ref['pointer'])
 ck('Complete reference hash '+ref['pointer'],valuehash(v)==binding['valueSha256'])
 return deepcopy(v)
forward=deepcopy(old);resolved=[]
for n,op in enumerate(ops['operations']):
 path=op['path'];b=resolve(op['before']);a=resolve(op['after']);present=exists(forward,path)
 ck('Forward exact presence '+path,present==op['before']['present'])
 if present:ck('Forward full before value '+path,at(forward,path)==b)
 ck('Operation kind matches actual presence '+path,op['op']==('replace' if present else 'add') and op['after']['present'])
 target,key=parent(forward,path);ck('Object-field mutation only '+path,isinstance(target,dict));target[key]=a
 resolved.append((op,b,a))
ck('Complete forward file bytes equal MODEL',enc(forward)==model_bytes)
reverse=deepcopy(model)
for op,b,a in reversed(resolved):
 path=op['path'];ck('Inverse exact complete after value '+path,at(reverse,path)==a)
 target,key=parent(reverse,path)
 if op['before']['present']:target[key]=deepcopy(b)
 else:del target[key]
ck('Complete inverse file bytes equal original including key order',enc(reverse)==original_bytes)
procedures=j(P/'PROCEDURES.json')['procedures'];questions=j(P/'QUESTION_DISPOSITIONS.json')['questions'];shared=j(P/'SHARED_RULES.json')['rules'];casebook=j(P/'CASE_DISPOSITIONS.json')
ck('Three full procedure identities',len(procedures)==3 and {p['id'] for p in procedures}=={'arc-furnace','resonance-singularity','resonance-nexus-supreme'})
for proc in procedures:
 rec=next(r for r in model['records'] if r['spellId']==proc['id'])
 ck('Complete procedure mirror '+proc['id'],rec['procedure']==proc['procedure'])
 ck('Full shared-rule binding mirror '+proc['id'],rec['sharedRuleIds']==proc['sharedRuleIds'])
ck('All24 complete question mirrors',len(questions)==24 and questions==model['selectedQuestionDispositions'])
ck('All shared-rule mirrors',shared==model['selectedSharedRules'])
ck('Seven full case mirrors',casebook['caseCount']==7 and casebook['cases']==model['currentVectors'] and len(model['currentVectors'])==7)
ck('28 branch declaration retained',casebook['branchCount']==28)
for field in ['sourceBindings','completeAppliedCounterparts','completeClassFeatureComparisons','pendingComparisonsNotAuthority','questions','countsUnchanged','earlierOperationalWorkedCases']:
 ck('Complete original field retained '+field,model[field]==old[field])
for index,(before,after) in enumerate(zip(old['records'],model['records'])):
 restored={k:v for k,v in after.items() if k not in ['procedure','sharedRuleIds','proposedSelection']}
 ck('Every original record value remains exact '+str(index),restored==before)
report={'status':'PASS_INDEPENDENT_FULL_VALUE_RECONSTRUCTION_AND_MIRRORS_NOT_SEMANTIC_ACCEPTANCE','sourceModel':info(P/'MODEL.json'),'operationFile':info(P/'EXACT_OPERATIONS_FROM_SOURCE.json'),'baselineBytes':len(original_bytes),'baselineSha256':sh(original_bytes),'forwardBytes':len(model_bytes),'forwardSha256':sh(model_bytes),'checks':checks,'checkCount':len(checks),'failures':0,'downloadedCodeExecuted':False,'canonicalMutation':False,'runtimeTestsExecuted':0,'semanticReviewStillRequired':['All24 reasoning/dispositions and complete shared clauses.','Actual seven positive encounters/28branches, source-qualified actors, source costs/history and complete arithmetic/state transitions.','All-magic interpretation and useful enhancement/conversion, protected principal and active lifecycle/expiry/suppression.'],'sourceInformationDeleted':0}
OUT.write_bytes(enc(report));SAVED.write_bytes(Path(__file__).read_bytes());print(json.dumps({'report':info(OUT),'checks':len(checks),'failures':0}))
