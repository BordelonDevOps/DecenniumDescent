import json,pathlib,hashlib,zipfile,copy,subprocess
D=pathlib.Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game\director-spell-review-126');P=D/'body8-final';G=pathlib.Path(r'C:\Github\DecenniumDescent');checks=[]
def load(n):return json.loads((P/n).read_text(encoding='utf-8-sig'))
def ck(ok,label):checks.append({'check':label,'passed':bool(ok)});assert ok,label
def raw(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def parts(p):return [x.replace('~1','/').replace('~0','~') for x in p.strip('/').split('/')]
def get(d,p):
 for x in parts(p):d=d[int(x)] if isinstance(d,list) else d[x]
 return d
def parent(d,p):
 a=parts(p)
 for x in a[:-1]:d=d[int(x)] if isinstance(d,list) else d[x]
 return d,int(a[-1]) if isinstance(d,list) else a[-1]
def replace_roundtrip(before,after,ops,label):
 d=copy.deepcopy(before)
 for o in ops:
  n,k=parent(d,o['pointer']);ck(n[k]==o['before'],label+' before '+o['pointer']);n[k]=copy.deepcopy(o['after'])
 ck(d==after,label+' forward full value')
 for o in reversed(ops):
  n,k=parent(d,o['pointer']);ck(n[k]==o['after'],label+' reverse '+o['pointer']);n[k]=copy.deepcopy(o['before'])
 ck(d==before,label+' reverse full value');return d
man=load('MANIFEST.json')
for b in man['files']:
 r=(P/b['path']).read_bytes();ck(len(r)==b['bytes'] and hashlib.sha256(r).hexdigest()==b['sha256'],'Manifest '+b['path'])
cp=P/'history/DD_Body_Defense8_INCOMPLETE_CHECKPOINT_123_01.zip'
ck(cp.read_bytes()==(D.parent/'director-spell-review-125/DD_Body_Defense8_INCOMPLETE_CHECKPOINT_123_01.zip').read_bytes(),'Original checkpoint archive exact')
with zipfile.ZipFile(cp) as z:
 original=json.loads(z.read('CASE_CHECKPOINT_08.json'));actor0=json.loads(z.read('ACTOR_TEMPLATES.json'))
 for n in ['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','OPERATIVE_TEXT.md','NATIVE_SOURCE_HISTORY.json']:ck(z.read(n)==(P/n).read_bytes(),'Previously reviewed source/procedure unchanged '+n)
 restored=replace_roundtrip(original,load('CASEBOOK.json'),load('CASEBOOK_REPAIR_OPERATIONS.json')['operations'],'241 case repairs');ck(raw(restored)==z.read('CASE_CHECKPOINT_08.json'),'Case reverse exact bytes')
 replace_roundtrip(actor0,load('ACTOR_TEMPLATES.json'),load('ACTOR_REPAIR_OPERATIONS.json')['operations'],'Actor repair')
replace_roundtrip(load('history/pre_custody_selected/CASEBOOK.json'),load('CASEBOOK.json'),load('FINAL_CUSTODY_AND_WITNESS_OPERATIONS.json')['operations'],'Alternative32 delta')
base=load('evidence/ORIGINAL_CANDIDATE.json');model=load('MODEL.json');ops=load('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'];d=copy.deepcopy(base)
for o in ops:
 n,k=parent(d,o['pointer']);ck(k not in n,'Model absent '+o['pointer']);n[k]=copy.deepcopy(get(load(o['after']['file']),o['after']['pointer']))
ck(d==model,'Model additive forward exact');ck(raw(d)==(P/'MODEL.json').read_bytes(),'Model bytes exact')
for o in reversed(ops):n,k=parent(d,o['pointer']);del n[k]
ck(d==base,'Model reversible source exact');ck(raw(d)==(P/'evidence/ORIGINAL_CANDIDATE.json').read_bytes(),'Model reversed source bytes')
for k,n in [('selectedSharedRules123','SHARED_RULES.json'),('selectedQuestionDispositions123','QUESTION_DISPOSITIONS.json'),('selectedCurrentCasebook123','CASEBOOK.json'),('selectedActorTemplates123','ACTOR_TEMPLATES.json'),('selectedHoldRegister123','HOLD_REGISTER.json')]:ck(model[k]==load(n),'Full model mirror '+k)
for i,r in enumerate(load('PROCEDURES.json')['spells']):ck(model['records'][i]['selectedOperationalProcedure123']==r,'Complete procedure mirror '+r['id'])
for r in load('NATIVE_SOURCE_HISTORY.json')['records']:
 b=r['source'];v=(G/b['path']).read_bytes();ck(len(v)==b['bytes'] and hashlib.sha256(v).hexdigest()==b['sha256'],'Native source '+r['spellId']);ck(get(json.loads(v),r['recordPointer'])==r['completeOriginalRecordUnchanged'],'Native full record '+r['spellId'])
ck(len(load('QUESTION_DISPOSITIONS.json')['questions'])==22,'22 questions');ck(len(load('CASEBOOK.json')['cases'])==16,'16 mains')
r=subprocess.run([r'C:\Python\python.exe',str(D.parent/'director-spell-review-125/inspect_return_data.py'),str(P)],capture_output=True,text=True,check=True);v=json.loads(r.stdout);ck(not v['findings'],'Independent numerical/state/observation/acquisition/range checks');(D/'BODY8_DATA_CHECKS.json').write_text(json.dumps(v,indent=2))
(D/'BODY8_FINAL_VERIFICATION.json').write_text(json.dumps({'checks':checks,'count':len(checks),'passed':all(c['passed'] for c in checks),'scope':'Data/source/roundtrip checks, not gameplay'},indent=2));print('Passed',len(checks))
