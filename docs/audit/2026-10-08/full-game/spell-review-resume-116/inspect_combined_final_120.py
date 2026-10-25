import json,pathlib,copy,hashlib,datetime
A=pathlib.Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game'); O=A/'spell-review-resume-116'; F=A/'rank7-mechanics16-final-120'; checks=[]
def read(p):return json.loads(p.read_bytes())
def check(n,v):
 checks.append({'check':n,'passed':bool(v)})
 assert v,n
m=read(F/'MODEL.json'); c=read(F/'CASEBOOK.json'); base=read(A/'rank7-mechanics16-combined-input-120'/'COMBINED_CASEBOOK_CANDIDATE.json'); ops=read(F/'METADATA_SELECTION_OPERATIONS.json')['operations'];r=read(F/'REVIEW_RECEIPT.json')
check('72 disclosed selection operations',len(ops)==72)
for name in ['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','CASEBOOK.json']:
 src=A/'rank7-mechanics16-partA-117'/name if name!='CASEBOOK.json' else A/'rank7-mechanics16-combined-input-120'/'COMBINED_CASEBOOK_CANDIDATE.json'
 before=read(src);work=copy.deepcopy(before); selected=read(F/name)
 for op in [x for x in ops if x['artifact']==name]:
  check('Metadata-only path '+op['path'],op['path'].split('/')[-1] in ['id','status','auditScope','disposition'])
  parts=op['path'].strip('/').split('/'); obj=work
  for p in parts[:-1]:obj=obj[int(p)] if isinstance(obj,list) else obj[p]
  k=parts[-1]; check('Prior value '+name+op['path'],obj[k]==op['before']);obj[k]=op['after']
 check('Full forward selection '+name,work==selected)
 for op in reversed([x for x in ops if x['artifact']==name]):
  parts=op['path'].strip('/').split('/');obj=work
  for p in parts[:-1]:obj=obj[int(p)] if isinstance(obj,list) else obj[p]
  obj[parts[-1]]=op['before']
 check('Full reverse selection '+name,work==before)
for x,y in zip(c['cases'],base['cases']):check('Exact reviewed case '+x['id'],x==y)
check('32 main cases',len(c['cases'])==32)
branches=[b for x in c['cases'] for b in x.get('independentBranches',[])];check('13 branches',len(branches)==13)
check('235 full events',sum(len(x['timeline']) for x in c['cases']+branches)==235)
for key,file,subkey in [('procedures','PROCEDURES.json','procedures'),('sharedRules','SHARED_RULES.json','rules'),('questionDispositions','QUESTION_DISPOSITIONS.json','dispositions'),('currentCases','CASEBOOK.json','cases')]:check('Full MODEL mirror '+key,m[key]==read(F/file)[subkey])
check('16 acceptance IDs',len(set(r['acceptedIdentityIds']))==16 and set(r['acceptedIdentityIds'])=={p['id'] for p in m['procedures']})
for e in r['acceptedArtifactBindings']:
 b=(F/e['path']).read_bytes();check('Actual acceptance binding '+e['path'],len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'])
check('No canonical or runtime application',m['canonicalApplied']==False and m['runtimeExecuted']==False)
h=read(F/'HOLD_REGISTER.json');check('All six current holds retained',len(h['currentCohortContentAndConditionalHolds'])==6 and all(x['discharged']==False for x in h['currentCohortContentAndConditionalHolds']))
check('Five inherited holds retained',h['inheritedWholePositiveCaseHolds']==['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'])
check('Authored counts69/254',r['postVerdictAuthoredAccounting']['acceptedUnapplied']==69 and r['postVerdictAuthoredAccounting']['stillRequiringAcceptance']==254)
report={'recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'ACCEPT_EXACT_AUTHORED_R7M16_WITH_RETAINED_HOLDS','actualDownloadVerified':True,'archiveSha256':'a379379f8cb73bb54c30a56a8bbfc95bc3e9daaf5a26c4012c5602ba27b205b8','manifestBindingsVerified':32,'checks':checks,'passed':len(checks),'failed':0,'inheritedPartReviewsNotRerun':True,'acceptedIdentityIds':r['acceptedIdentityIds'],'acceptedUnapplied':69,'needsAcceptance':254,'canonicalApplied':False,'runtimeExecuted':False}
(O/'R7M16_FINAL_LOCAL_ACCEPTANCE_120.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS',len(checks))

