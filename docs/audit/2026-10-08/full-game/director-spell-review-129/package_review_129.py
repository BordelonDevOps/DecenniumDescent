"""Fresh local data-only packaging for independently read spell conferences129."""
from pathlib import Path
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def package(group,label,extra,specs):
 qpath=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json';q=read(qpath);g=next(x for x in q['groups'] if x['group']==group)
 assert g['currentPhase']=='prepared-awaiting-review'
 cp=G/g['candidate']['path'];c=read(cp);assert sha(cp.read_bytes())==g['candidate']['sha256'];orig=G/g['archive']['path'];assert sha(orig.read_bytes())==g['archive']['sha256']
 checks=[]
 with zipfile.ZipFile(orig) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  for b in c['sourceBindings']:
   v=z.read('sources/'+b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256'];checks.append({'path':b['path'],'originalExact':True,'currentExact':sha((G/b['path']).read_bytes())==b['sha256']})
 cases=[{'id':label.upper()+'129-'+sid.upper()+'-'+chr(65+i),'spellId':sid,'requiredEvidence':s,'status':'REQUIRED_NEW_CASE_NOT_AUTHORED'} for sid,ss in specs.items() for i,s in enumerate(ss)]
 assert set(specs)==set(g['identities'])
 notes={'id':label.upper()+'-INDEPENDENT-CONFERENCE-129','status':'PREPARED_UNSENT_NOT_ACCEPTED','identities':g['identities'],'currentAppliedCounts':{'reviewed':616,'pending':232,'acceptedUnapplied':0},'completeOriginalQuestionsUnchanged':c['questions'],'focusedAdditionalQuestions':extra,'allQuestions':c['questions']+extra,'requiredNewCases':cases,'originalFutureCaseRequirementsUnchanged':c['futureCaseRequirements'],'sourceChecks':checks,'scope':'Preparation only. Current exact accepted contexts supersede old pending comparison labels within their scope. No new rule adopted. No supplied program execution or runtime/human/balance/cosmology/release claim.'}
 (D/(label.upper()+'_NEXT_CONFERENCE_NOTES_129.json')).write_bytes(enc(notes));files={}
 with zipfile.ZipFile(A/'DD_VitalityMatter10_Director_Conference_128.zip') as z:
  for n in z.namelist():
   if n.startswith(('accepted-context/','accepted/','current/')):files[n]=z.read(n)
 files['original/'+orig.name]=orig.read_bytes();files['INDEPENDENT_QUESTIONS_129.json']=enc(notes)
 guard=read(D/'PENDING232_NATIVE_SOURCE_GUARD_129.json');guard['records']=[r for r in guard['records'] if r['id'] in g['identities']];guard['scope']='Exact native subset for this group, from read-only pending232 audit129. Source guard only, not acceptance.'
 files['NATIVE_SOURCE_GUARD_129.json']=enc(guard)
 files['README.md']=(label+' director conference129. '+str(len(g['identities']))+' pending identities; '+str(len(notes['allQuestions']))+' questions; '+str(len(cases))+' main cases plus all genuine required branches. Baseline616applied/232pending. Read exact original sources and scoped current accepted comparisons. Preserve originals and full reversible values. No supplied/historical program execution. Independent exact acceptance required before application.\n').encode()
 m={'id':label.upper()+'-CONFERENCE-129-MANIFEST','files':[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in files.items()]};files['MANIFEST.json']=enc(m)
 out=A/('DD_'+label+'_Director_Conference_129.zip');assert not out.exists()
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,v in files.items():z.writestr(n,v)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for b in m['files']:v=z.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
 rec={'id':label.upper()+'-DIRECTOR-CONFERENCE-129','status':'PREPARED_NOT_SENT','archive':{'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes())},'members':len(files),'bindings':len(m['files']),'questions':len(notes['allQuestions']),'requiredMainCases':len(cases),'sourceChecks':len(checks),'canonicalChanges':False}
 (D/(label.upper()+'_PACKET_129.json')).write_bytes(enc(rec));g['currentPhase']='current-director-conference-prepared-129-unsent';qpath.write_bytes(enc(q));print(json.dumps(rec,indent=2))
