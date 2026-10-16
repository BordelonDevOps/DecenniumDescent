"""Independent current-surface verification of the actual GPT Repair04 return."""
import json,hashlib,zipfile
from datetime import datetime,timezone
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';I=A/'ac6-full-current-review-03-input';O=A/'ac6-repair-04-return';P=A/'ac6-full-review-03-return'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def ck(k,a,b=True):checks.append({'check':k,'passed':a==b,**({} if a==b else {'actual':a,'expected':b})})
def at(d,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
history={'completeSourceAndAccess','historicalQuestionAndRecord','completePriorDraftRecord','previousCurrentVersion','repair04PreviousCurrentVersion'}
def current(d):
 if isinstance(d,dict):return {k:current(v) for k,v in d.items() if k not in history and not k.endswith('_repair04PreviousCurrentVersion')}
 if isinstance(d,list):return [current(v) for v in d]
 return d
def refs(d,path=''):
 if isinstance(d,dict):
  if 'path' in d and ('pointer' in d or 'section' in d):yield path,d
  for k,v in d.items():yield from refs(v,path+'/'+k)
 elif isinstance(d,list):
  for i,v in enumerate(d):yield from refs(v,path+'/'+str(i))
def leaves(d):
 if isinstance(d,str):yield d
 elif isinstance(d,dict):
  for v in d.values():yield from leaves(v)
 elif isinstance(d,list):
  for v in d:yield from leaves(v)
model=read(O/'SPELLS_MODEL.json');old=read(P/'SPELLS_MODEL.json');cases=read(O/'CASEBOOK.json');oldcases=read(P/'CASEBOOK.json');reg=read(O/'REGISTER.json');manifest=read(O/'EVIDENCE_MANIFEST.json');input=read(I/'CURRENT_REVIEW_INPUT.json')
names={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
archive=A/'DD_AC6_Repair_04_Return.zip';b=archive.read_bytes();ck('archive bytes',len(b),253952);ck('archive SHA',sha(b),'a9a32823acc03843f3aa4f947182d0c4ebeb25312cc26258a964adcb674656fa')
with zipfile.ZipFile(archive) as z:
 ck('exact eight root members',len(z.namelist())==8 and set(z.namelist())==names)
 for n in names:ck('extracted bytes '+n,(O/n).read_bytes(),z.read(n))
for e in manifest['files']:
 b=(O/e['name']).read_bytes();ck('output bytes '+e['name'],len(b),e['bytes']);ck('output SHA '+e['name'],sha(b),e['sha256'])
bindings=read(I/'SOURCE_MANIFEST.json')['bindings'];ck('exact source hashes list',read(O/'SOURCE_HASHES.json')['bindings'],bindings)
for e in bindings:
 b=(I/'sources'/e['path']).read_bytes();ck('source bytes '+e['path'],len(b),e['bytes']);ck('source SHA '+e['path'],sha(b),e['sha256'])
ck('14 ordered identities',[v['id'] for v in model['spells']],[v['id'] for v in old['spells']])
for n,o in zip(model['spells'],old['spells']):
 for k in ['questionId','completeSourceAndAccess','historicalQuestionAndRecord','completePriorDraftRecord','priorDraftBinding','priorWholeRecordPointer']:ck(n['id']+' preserves '+k,n[k],o[k])
 if n['procedure']!=o['procedure']:ck(n['id']+' retains superseded procedure',n.get('repair04PreviousCurrentVersion'),o['procedure'])
ck('22 original texts',cases['historicalOriginalTexts'],oldcases['historicalOriginalTexts']);ck('32 original requirements',cases['originalRequiredExamples'],oldcases['originalRequiredExamples'])
ck('55 ordered current cases',[v['id'] for v in cases['cases']],[v['id'] for v in oldcases['cases']])
for n,o in zip(cases['cases'],oldcases['cases']):
 ck(n['id']+' original previous history',n.get('previousCurrentVersion'),o.get('previousCurrentVersion'))
 core={k:v for k,v in n.items() if k!='repair04PreviousCurrentVersion'}
 if core!=o:ck(n['id']+' retains return03 current case',n.get('repair04PreviousCurrentVersion'),o)
for k in ['originalQuestionDispositions','historicalIssueDispositions','currentInterfaceIssueDispositions','currentReviewQuestionDispositions']:
 ck(k+' retained',model[k],old[k]);ck(k+' register agrees',reg[k],model[k])
ck('all six repair IDs',[v['id'] for v in model['repair04Dispositions']],[f'AC6-L04-{n:02}' for n in range(1,7)])
ck('repair dispositions agree',model['repair04Dispositions'],reg['repair04Dispositions'])
ck('51 coverage IDs',[v['caseId'] for v in reg['caseScenarioCoverage']],[v['id'] for v in input['currentExamples']])
for flag in ['runtimeTestsExecuted','humanPlaytested','balanceApproved','cosmologyCanonModified']:ck('no unsupported '+flag,model[flag],False)
cache={};pointer_results=[];sections=[]
surfaces={'model':{'sharedRules':current(model['sharedRules']),'profiles':current(model['profiles']),'spells':current(model['spells'])},'cases':current(cases['cases'])}
for where,r in refs(surfaces):
 path=O/r['path'] if r['path'] in names else I/'sources'/r['path']
 if 'pointer' not in r:
  sections.append({'where':where,**r,'sourceExists':path.exists()});ck('descriptive reference source '+where,path.exists());continue
 try:
  if path not in cache:cache[path]=read(path)
  found=at(cache[path],r['pointer']);ok=found is not None;error=None
 except Exception as exc:ok=False;error=str(exc)
 ck('current pointer '+where,ok);pointer_results.append({'where':where,**r,'resolves':ok,**({'error':error} if error else {})})
ck('pointer traversal matches reported scope',len(pointer_results),manifest['currentReferenceVerification']['jsonPointersResolved'])
ck('section traversal matches reported scope',len(sections),manifest['currentReferenceVerification']['descriptiveSectionReferences'])
for chapter in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
 text=(O/chapter).read_text()
 for s in model['spells']:
  for i,leaf in enumerate(leaves(s['procedure'])):
   ck(chapter+' procedure leaf '+s['id']+':'+str(i),leaf in text)
 for key in model['profiles']:ck(chapter+' names profile '+key,key in text)
nx=model['spells'][13]['procedure'];ck('both current Nexus modes',set(nx['modes'])=={'Divination6','Conjuration8'});ck('Nexus lower duration','60elapsed seconds' in nx['modes']['Divination6']['formation']);ck('Nexus portal duration','600elapsed seconds' in nx['modes']['Conjuration8']['openings'])
ck('Army actual AC14',model['profiles']['AC6-FACTION-SOLDIER-PROFILE-01']['armorClass'],14)
ck('Army owner-scaled attack','source-owner' in model['profiles']['AC6-FACTION-SOLDIER-PROFILE-01']['attack']['attackModifier'])
report={'id':'AC6-REPAIR-04-INDEPENDENT-STRUCTURAL-CHECK','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkCount':len(checks),'failureCount':sum(not c['passed'] for c in checks),'checks':checks,'sourceCount':103,'identityCount':14,'currentCases':55,'currentPointers':len(pointer_results),'descriptiveSections':len(sections),'pointerResults':pointer_results,'sectionReferences':sections,'scope':'Preservation/reference and complete-current-procedure inclusion checks. Section prose headings are descriptive references, not exact-anchor assertions. Scenario semantic coverage still requires independent content review.','semanticReviewComplete':False,'knownRemainingIssues':['AC6-N17 still omits B and C from the U successor set despite measuring from the Large occupied body; direct geometry disproves the claimed complete set.','AC6-N15 needs exact initiating slot-end and suppressor geometry that remains effective during descent; same-body Falling choice itself agrees with accepted Falling rules.'],'newSpellAdoptions':0,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False}
target=A/'AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json';assert not target.exists();target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:report[k] for k in ['checkCount','failureCount','currentPointers','descriptiveSections']}));print(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False))
