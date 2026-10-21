"""Build a derived fixture successor from the exact jointly confirmed data only."""
from pathlib import Path
import copy, hashlib, json, zipfile

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
OUT=A/'bestiary-schedule-confirmed-109'
OUT.mkdir(exist_ok=False)
DOWNLOAD=Path(r'C:\Users\cbord\Downloads\DD_Bestiary_Schedule_108_Confirmation_01.zip')
BASE=A/'bestiary-reconciliation-108/delivery/DISTINGUISHING_CASES.json'
PROPOSAL=A/'bestiary-schedule-correction-108/PROPOSAL.json'
CHECKS=[]
def h(b): return hashlib.sha256(b).hexdigest()
def serial(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def ck(name,value):
    CHECKS.append({'name':name,'passed':bool(value)})
    assert value,name
def write(path,b):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f: f.write(b)
def binding(path):
    b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':h(b)}
def get(obj,path):
    for part in path.split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~')
        obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj
def parent(obj,path):
    parts=path.rsplit('/',1);return get(obj,parts[0]),parts[1]

rawzip=DOWNLOAD.read_bytes()
ck('Actual downloaded final ZIP matches visible final',len(rawzip)==9045 and h(rawzip)=='67de7d38fd7ab1a60e94b356699485d06337418a817c2416a08902e5c8f8ac1f')
write(OUT/DOWNLOAD.name,rawzip)
with zipfile.ZipFile(DOWNLOAD) as z:
    ck('Exactly four nonexecutable flat members',set(z.namelist())=={'CHECKS.json','DECISION.json','MANIFEST.json','REVIEW.md'} and len(z.namelist())==4)
    ck('CRC succeeds',z.testzip() is None)
    manifest=json.loads(z.read('MANIFEST.json'))
    for row in manifest['files']:
        b=z.read(row['file']);ck('Manifest '+row['file'],len(b)==row['bytes'] and h(b)==row['sha256'])
    for n in z.namelist():write(OUT/'decision'/n,z.read(n))
    decision=json.loads(z.read('DECISION.json'))
ck('Exact proposal confirmed unchanged',decision['disposition']=='CONFIRM_EXACT_SUBMITTED_SCHEDULE_ONLY_FIXTURE_SUCCESSOR' and decision['proposalAlterationCount']==0)
packet=A/decision['input']['file'];b=packet.read_bytes()
ck('Incoming proposal packet exact',len(b)==decision['input']['bytes'] and h(b)==decision['input']['sha256'])
raw=BASE.read_bytes();old=json.loads(raw);pr=PROPOSAL.read_bytes();proposal=json.loads(pr)
ck('Complete original member exact',len(raw)==921721 and h(raw)=='0458966939d12bf9388f19c753cc3b46efa71ba28b00378254060790b5f5696c')
ck('Complete proposal exact',len(pr)==670006 and h(pr)=='6ed09fea766f287456f5d6d11d654c031322717bde38ccf8e1a1ec85b2e62f93')
write(OUT/'before/DISTINGUISHING_CASES.json',raw)
write(OUT/'PROPOSAL.json',pr)
successor=copy.deepcopy(old)
for row in decision['wholeCaseReplacementAlternative']:
    before=get(proposal,row['beforeRef']['pointer']);after=get(proposal,row['afterRef']['pointer'])
    ck('Bound full original '+row['path'],get(successor,row['path'])==before and before['id']==row['caseId'])
    obj,key=parent(successor,row['path']);obj[int(key)]=copy.deepcopy(after)
    ck('Full final state remains exact '+row['path'],before['finalState']==after['finalState'])
ops=decision['fieldOperations']
ck('43 exact operations',len(ops)==43 and sum(o['op']=='replace' for o in ops)==40 and sum(o['op']=='add' for o in ops)==3)
comparison=copy.deepcopy(old)
for op in ops:
    obj,key=parent(comparison,op['path']);key=int(key) if isinstance(obj,list) else key
    if op['op']=='replace':
        ck('Field baseline '+op['path'],obj[key]==op['before'])
        obj[key]=op['after']
    else:
        ck('Appended premise position '+op['path'],isinstance(obj,list) and key==len(obj))
        obj.append(op['after'])
ck('Alternative reconstructions agree; only one is emitted',comparison==successor)
rebuilt=serial(successor);rec=decision['reconstruction']
ck('Entire successor matches GPT bytes and hash',len(rebuilt)==rec['selectedVirtualSuccessorBytes']==922913 and h(rebuilt)==rec['selectedVirtualSuccessorSha256']=='61422722e9a599804e0d9f870135dcba8a4b9d2170b375d6011c09e79dbcf8fb')
changed=[i for i,(o,n) in enumerate(zip(old['completeCases'],successor['completeCases'])) if o!=n]
ck('Exactly three of sixteen cases changed',len(old['completeCases'])==len(successor['completeCases'])==16 and changed==[8,9,10])
reverse=copy.deepcopy(successor)
for row in proposal['completeCases']:
    obj,key=parent(reverse,row['originalPointer']);obj[int(key)]=row['completeBefore']
ck('Whole reconstruction reverses to all original bytes',serial(reverse)==raw)
starts=[]
for ci in [8,9,10]:
    case=successor['completeCases'][ci];state=case['initialState']
    for event in case['timeline']:
        ck(case['id']+'/'+event['id']+' exact input chain',event['before']==state)
        for aid,after in event['after']['actors'].items():
            before=event['before']['actors'][aid]
            ck(case['id']+'/'+event['id']+'/'+aid+' next START later than previous',after['nextRegularStart']>after['regularStart'])
            if before['regularStart']!=after['regularStart']:
                ck(case['id']+'/'+event['id']+'/'+aid+' actual next START honored',before['nextRegularStart']==event['time']==after['regularStart'] and after['nextRegularStart']==after['regularStart']+6)
                starts.append({'caseId':case['id'],'eventId':event['id'],'actorId':aid,'time':event['time'],'before':[before['regularStart'],before['nextRegularStart']],'after':[after['regularStart'],after['nextRegularStart']]})
        state=event['after']
    ck(case['id']+' final chain',state==case['finalState'])
ck('Exactly four formerly contradictory START transitions',len(starts)==4)
write(OUT/'after/DISTINGUISHING_CASES.json',rebuilt)
ck('Original and submitted proposal remain unchanged',BASE.read_bytes()==raw and PROPOSAL.read_bytes()==pr and DOWNLOAD.read_bytes()==rawzip)
report={'id':'BESTIARY-SCHEDULE-CONFIRMED-SUCCESSOR-109','status':'JOINTLY_CONFIRMED_DERIVED_FIXTURE_SUCCESSOR_ONLY','decision':binding(OUT/'decision/DECISION.json'),'original':binding(BASE),'proposal':binding(PROPOSAL),'successor':binding(OUT/'after/DISTINGUISHING_CASES.json'),'changedCases':changed,'correctedStarts':starts,'operationCounts':decision['operationCounts'],'passed':len(CHECKS),'failed':0,'checks':CHECKS,'historicalFindingPreserved':binding(A/'BESTIARY_RECONCILIATION_CASE_REVIEW_108.json'),'qualification':'Fresh exact-data reconstruction and four schedule transitions only. Prior successful scripts and downloaded code were not executed. Original 220-pass/four-mismatch report remains historical evidence. Five agreed mechanics unchanged. No new scheduler rule, runtime execution, whole-bestiary approval or canonical integration.','canonicalApplied':False,'runtimeExecuted':False,'wholeBestiaryAccepted':False}
write(OUT/'REPORT.json',serial(report))
files=[binding(p) | {'file':p.relative_to(OUT).as_posix()} for p in sorted(OUT.rglob('*')) if p.is_file()]
write(OUT/'MANIFEST.json',serial({'id':'BESTIARY-SCHEDULE-CONFIRMED-109-MANIFEST','files':files}))
archive=A/'DD_Bestiary_Schedule_Confirmed_Successor_109.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in files:assert h(z.read(row['file']))==row['sha256']
receipt={'id':report['id'],'archive':binding(archive),'report':binding(OUT/'REPORT.json'),'successor':report['successor'],'passed':len(CHECKS),'failed':0,'canonicalApplied':False,'runtimeExecuted':False}
write(A/'BESTIARY_SCHEDULE_CONFIRMED_RECEIPT_109.json',serial(receipt))
write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps(receipt))
