from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import copy, hashlib, io, json, stat, zipfile

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
NAME='DD_Control_15_Full_Conference_Part5_Return_02.zip'
SRC=Path(r'C:\Users\cbord\Downloads')/NAME
OUT=A/'control15-full-conference-part5-return-02'
RECEIPT=A/'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'
checks=[]
def raw(p): return Path('\\\\?\\'+str(p)).read_bytes()
def enc(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def ck(label,ok):
 checks.append({'check':label,'pass':bool(ok)})
 assert ok,label
def binding(p):
 b=raw(p);return {'path':str(p.relative_to(G)).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,b):
 p=Path('\\\\?\\'+str(p));p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def member_binding(z,b):
 data=z.read(b.get('file',b.get('path',b.get('member'))))
 return len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256']
def parent(obj,ptr):
 parts=[x.replace('~1','/').replace('~0','~') for x in ptr.split('/')[1:]]
 for k in parts[:-1]:obj=obj[int(k)] if isinstance(obj,list) else obj[k]
 return obj,int(parts[-1]) if isinstance(obj,list) else parts[-1]
def at(obj,ptr):
 if isinstance(ptr,dict):ptr=ptr['pointer']
 p,k=parent(obj,ptr);return p[k]
def replay(base,ops):
 cur=copy.deepcopy(base)
 for i,o in enumerate(ops):
  p,k=parent(cur,o['jsonPointer'])
  if o['op']=='replace':ck(f'forward before {i} {o["jsonPointer"]}',p[k]==o['before'])
  else:ck(f'forward absent {i} {o["jsonPointer"]}',o['op']=='add' and o['beforeExists'] is False and k not in p)
  p[k]=copy.deepcopy(o['after'])
 return cur
def reverse(cur,ops):
 cur=copy.deepcopy(cur)
 for i,o in enumerate(reversed(ops)):
  p,k=parent(cur,o['jsonPointer']);ck(f'reverse after {i} {o["jsonPointer"]}',p[k]==o['after'])
  if o['op']=='add':del p[k]
  else:p[k]=copy.deepcopy(o['before'])
 return cur

ck('fresh immutable output',not OUT.exists() and not RECEIPT.exists() and not (A/NAME).exists())
b=raw(SRC)
ck('archive published bytes and SHA256',len(b)==20056073 and hashlib.sha256(b).hexdigest()=='2182baaad08e355da4eef8b0e476eb7b9148804710e72baa92ff3d82194c3123')
native=json.loads(raw(A/'CONTROL15_PART5_FULL_RETURN_02_NATIVE.json'))
messages={i['id']:i.get('text','') for t in native['turns'] for i in t['items']}
assistant='6aa2c282-6225-41f7-96d9-0186dc53a83e'
ck('actual final assistant binds archive and successor',all(s in messages[assistant] for s in ['2182baaad08e355da4eef8b0e476eb7b9148804710e72baa92ff3d82194c3123','80bef5de1b26e8d9beb75ddd00b30c9eff66d4e7ec3f4bd04c5d0da54ed91198']))
index=G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
index_before=raw(index)
ck('applied index remains known baseline',hashlib.sha256(index_before).hexdigest()=='6f9b86e21f6a69c7ba2469aba89d5907aa08da567226a2c4bd3ced9e09409857')
with zipfile.ZipFile(io.BytesIO(b)) as z:
 names=z.namelist();ck('34 unique archive members',len(names)==34 and len(names)==len(set(n.casefold() for n in names)))
 ck('CRC verified',z.testzip() is None)
 for zi in z.infolist():
  p=PurePosixPath(zi.filename)
  ck('safe member '+zi.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in zi.filename and ':' not in zi.filename and not stat.S_ISLNK(zi.external_attr>>16))
 manifest=json.loads(z.read('MANIFEST.json'))
 ck('manifest exact coverage',set(names)=={'MANIFEST.json'}|{e['path'] for e in manifest['files']} and len(manifest['files'])==33)
 for e in manifest['files']:ck('manifest '+e['path'],member_binding(z,e))
 for n in names:
  if n.startswith(('inputs/','history/')):ck('exact retained input '+n,z.read(n)==raw(A/PurePosixPath(n).name))
 def obj(n):return json.loads(z.read(n))
 current=obj('baseline/CONTROL15_CURRENT12.json'); prior=obj('baseline/CONTROL15_AFTER_CORRECTIONS01.json'); successor=obj('successor/CONTROL15_REVIEWED_SUCCESSOR13.json')
 ck('Current12 live baseline exact',z.read('baseline/CONTROL15_CURRENT12.json')==raw(G/'DescentReviewChanges/ReviewBible/data/director/spell_proposals/control_15_current_12.json'))
 with zipfile.ZipFile(io.BytesIO(z.read('history/DD_Part5_Control_Ready_Corrections_01.zip'))) as old:
  ck('prior corrected proposal exact',z.read('baseline/CONTROL15_AFTER_CORRECTIONS01.json')==old.read('corrected/DescentReviewChanges/ReviewBible/data/director/spell_proposals/control_15_current_12.json'))
 for opsname,base,bname,num in [('ALL_CONTROL_POINTER_OPERATIONS_FROM_CURRENT12.json',current,'baseline/CONTROL15_CURRENT12.json',14),('NEW_POINTER_OPERATIONS_FROM_CORRECTIONS01.json',prior,'baseline/CONTROL15_AFTER_CORRECTIONS01.json',5)]:
  doc=obj(opsname);ops=doc['operations'];ck('operation count '+opsname,len(ops)==num)
  ck('exact complete forward bytes '+opsname,enc(replay(base,ops))==z.read('successor/CONTROL15_REVIEWED_SUCCESSOR13.json'))
  ck('exact complete reverse bytes '+opsname,enc(reverse(successor,ops))==z.read(bname))
 ck('30 complete original scenarios preserved',len(successor['originalExamplesUnchanged'])==30 and successor['originalExamplesUnchanged']==current['originalExamplesUnchanged'])
 ck('54 source bindings preserved',len(successor['sourceBindings'])==54 and successor['sourceBindings']==current['sourceBindings'])
 ck('original 13 questions preserved',len(current['conferenceQuestions10'])==13 and successor['conferenceQuestions10']==current['conferenceQuestions10'])
 refs=obj('SOURCE_REFERENCES.json')['fullSourceMembers']
 archives={n:zipfile.ZipFile(io.BytesIO(z.read(n))) for n in names if n.startswith('inputs/') and n.endswith('.zip')}
 for e in refs:
  az=archives[e['archive']];data=az.read(e['member'])
  ck('full archived source '+e['archive']+' '+e['member'],len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'])
 for e in current['sourceBindings']:
  ck('recovered binding '+e['path'],any(r['repositoryPath']==e['path'] and r['bytes']==e['bytes'] and r['sha256']==e['sha256'] for r in refs))
 dispositions=obj('SPELL_DISPOSITIONS.json')['dispositions'];ck('15 complete dispositions',len(dispositions)==15)
 for s,d,old in zip(successor['spells'],dispositions,current['spells']):
  ck('native access and risk preserved '+s['id'],s['id']==old['id']==d['id'] and s['completeSourceAndAccess']==old['completeSourceAndAccess']==d['completeNativeSourceAndAccess'] and s['riskTier']==old['riskTier'])
  ck('complete selected procedure '+s['id'],s['procedure']==d['completeSelectedProcedure']==at(successor,d['selectedProcedurePointer']) and d['runtimeExecuted'] is False)
 cases=obj('CASE_DISPOSITIONS.json');ck('30 complete case dispositions',len(cases['cases'])==30)
 original={x['id']:x for x in current['originalExamplesUnchanged']}
 for c in cases['cases']:
  ck('case complete values '+c['id'],c['completeSelectedCurrentCase']==at(successor,c['selectedCasePointer']) and c['completeOriginalCurrent12Case']==at(current,c['selectedCasePointer']) and c['completePriorCorrections01Case']==at(prior,c['selectedCasePointer']) and c['runtimeExecuted'] is False)
  ck('original scenario exact '+c['id'],c['completeOriginalScenario']==original[c['id']]['exactOriginalText'])
 questions=obj('QUESTION_DISPOSITIONS.json');ck('all13 actual questions resolved',questions['actualQuestionCount']==13 and questions['unresolvedQuestionCount']==0 and len(questions['dispositions'])==13)
 for q,old in zip(questions['dispositions'],current['conferenceQuestions10']):ck('complete question '+q['id'],q['id']==old['id'] and q['completeSubmittedQuestion']==old['question'])
 receipt=obj('REVIEW_RECEIPT.json')
 ck('three content holds',set(receipt['wholeOriginalPositiveCaseHolds'])=={'EN5-01-A','EN5-01-B','EN6-03-B'})
 ck('successor published binding',member_binding(z,receipt['selectedSuccessor']))
 ck('only case and metadata changed since corrected predecessor',all(a['procedure']==b['procedure'] for a,b in zip(prior['spells'],successor['spells'])))
 preserved={n:z.read(n) for n in names}
ck('index unchanged after verification',raw(index)==index_before)
write(A/NAME,b)
for n,data in preserved.items():write(OUT/n,data)
record={'id':'CONTROL15-PART5-FULL-RETURN-02-LOCAL-RECEIPT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'ACTUAL_FULL_CONFERENCE_ACCEPTANCE_PRESERVED_VERIFIED_NOT_APPLIED','threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','actualAssistantResponse':assistant,'archive':binding(A/NAME),'nativeResponse':binding(A/'CONTROL15_PART5_FULL_RETURN_02_NATIVE.json'),'selectedSuccessor':binding(OUT/'successor/CONTROL15_REVIEWED_SUCCESSOR13.json'),'reviewReceipt':binding(OUT/'REVIEW_RECEIPT.json'),'holdRegister':binding(OUT/'HOLD_REGISTER.json'),'verdict':receipt['verdict'],'independentLocalChecks':{'total':len(checks),'passed':len(checks),'failed':0,'checks':checks},'gptReportedChecks':receipt['verification'],'wholePositiveCaseHolds':receipt['wholeOriginalPositiveCaseHolds'],'sourceGapResolved':{'exact':54,'formerlyUnavailableRecovered':19},'appliedIndex':binding(index),'appliedMembershipUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'boundary':'Owner reserved implementation. No rules, canonical models, index, registry, runtime flags or prior accepted artifacts changed. Downloaded Python was inspected only as source and never executed. Local checks validate exact data and reconstruction; GPT isolated specification results are attributed, not project runtime tests.','sourceInformationDeleted':0,'downloadedScriptsExecuted':False,'projectRuntimeTests':0}
write(RECEIPT,enc(record))
print(json.dumps({'receipt':binding(RECEIPT),'checks':len(checks),'failures':0,'successor':record['selectedSuccessor'],'applied':False},indent=2))
