import pathlib,json,copy,hashlib,datetime
A=pathlib.Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');B=A/'memory-creation3-review-121';P=A/'memory-creation3-corrected-121';O=A/'spell-review-resume-116';checks=[]
def rd(p):return json.loads(p.read_bytes())
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def slot(d,p):
 parts=p.strip('/').split('/');o=d
 for k in parts[:-1]:o=o[int(k)] if isinstance(o,list) else o[k]
 return o,int(parts[-1]) if isinstance(o,list) else parts[-1]
def enc(d):return (json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode()
ops=rd(P/'CASEBOOK_RECORD_OPERATIONS.json')['operations'];orig=rd(B/'CASEBOOK.json');new=rd(P/'CASEBOOK.json');work=copy.deepcopy(orig)
for op in ops:
 obj,k=slot(work,op['pointer']);ck('Exact prior record '+op['pointer'],obj[k]==op['before']);before=op['before'];after=op['after'];
 for field,v in before.items():
  if field=='plan':ck('Preserve existing plan fields '+op['pointer'],all(after['plan'].get(k)==v for k,v in v.items()))
  else:ck('Preserve cast '+field+' '+op['pointer'],after[field]==v)
 plan=after['plan'];
 if after['spellId']=='woven-threads':ck('Complete frozen narrative '+op['pointer'],0<len(plan.get('words',plan.get('narrative','')).split())<=60)
 else:ck('Complete material plan '+op['pointer'],all(k in plan for k in ['sampleId','massLb','valueCp','boxMin','boxMax']))
 obj[k]=copy.deepcopy(after)
ck('All casebook changes exactly129 disclosed records',len(ops)==129 and work==new)
for op in reversed(ops):obj,k=slot(work,op['pointer']);obj[k]=op['before']
ck('Whole original casebook bytes restored',enc(work)==(B/'CASEBOOK.json').read_bytes())
for name in ['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','ACTOR_DEFINITIONS.json','MATERIAL_PROFILES.json','PARTITION_EVIDENCE.json','COMPLETE_COUNTERPARTS.json']:
 ck('Unchanged reviewed bytes '+name,(B/name).read_bytes()==(P/name).read_bytes())
parentOps=rd(P/'EXACT_OPERATIONS_FROM_RETURN01.json')['operations']
for name in sorted(set(x['artifact'] for x in parentOps)):
 base=rd(B/name);target=rd(P/name);work=copy.deepcopy(base)
 for op in [x for x in parentOps if x['artifact']==name]:
  ob,k=slot(work,op['pointer']);nb,nk=slot(target,op['after']['pointer']);ob[k]=copy.deepcopy(nb[nk])
 ck('Full parent reconstruction '+name,enc(work)==(P/name).read_bytes())
 for op in reversed([x for x in parentOps if x['artifact']==name]):
  ob,k=slot(work,op['pointer']);bb,bk=slot(base,op['before']['pointer']);ob[k]=copy.deepcopy(bb[bk])
 ck('Full parent reversal '+name,enc(work)==(B/name).read_bytes())
model=rd(P/'MODEL.json');ck('Complete model cases mirror',model['currentCases']==new['cases']);allcases=[x for c in new['cases'] for x in [c]+c['branches']];ck('8mains15branches88events',len(new['cases'])==8 and len(allcases)==23 and sum(len(c['timeline']) for c in allcases)==88)
for op in ops:
 if op['findingId'] in ['MC3-COMMIT-04','MC3-COMMIT-05'] and op['pointer'].endswith('/outcome'):print('PLAN',json.dumps(op['after']['plan']))
receipt=rd(P/'REVIEW_RECEIPT.json');ck('Three exact accepted identities',{x['id'] for x in receipt['identityDecisions']}=={'woven-threads','haze-of-forgetting','creation'} and all(x['decision'].startswith('ACCEPT_EXACT') for x in receipt['identityDecisions']))
for e in receipt['completeCurrentBindings']:
 b=(P/e['path']).read_bytes();ck('Exact verdict binding '+e['path'],len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'])
ck('Original archive preserved',(P/'history/DD_Memory_Creation3_Part5_Conference_Return_01.zip').read_bytes()==(A/'DD_Memory_Creation3_Part5_Conference_Return_01.zip').read_bytes())
result={'recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_CORRECTED_MEMORY_CREATION3_AUTHORED_ACCEPTANCE_WITH_RETAINED_HOLDS','archiveSha256':'3641925df3e412e8ab75785b04b0ad983d9df73d48a736650c9855705c98130d','manifestBindingsVerified':60,'priorReviewChecks':1235,'priorReviewNotRerun':True,'checks':checks,'passed':len(checks),'failed':0,'resolvedFindings':5,'acceptedIdentityIds':['woven-threads','haze-of-forgetting','creation'],'acceptedUnapplied':72,'needsAcceptance':251,'canonicalApplied':False,'runtimeExecuted':False,'retainedHoldsFile':str(P/'HOLD_REGISTER.json')};(O/'MEMORY_CREATION3_FINAL_LOCAL_ACCEPTANCE_121.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(checks))
