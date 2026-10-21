"""Propose complete corrected synthetic schedules without modifying GPT finals."""
from pathlib import Path
import copy,hashlib,json,zipfile

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P=A/'bestiary-reconciliation-108/delivery/DISTINGUISHING_CASES.json'
OUT=A/'bestiary-schedule-correction-108';OUT.mkdir(exist_ok=False)
raw=P.read_bytes();d=json.loads(raw);cases=[];checks=[];ops=[]
def h(b):return hashlib.sha256(b).hexdigest()
def serial(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def ck(n,v):
    checks.append({'name':n,'passed':bool(v)});assert v,n
def write(n,b):
    with (OUT/n).open('xb') as f:f.write(b)
def walk(x,p=''):
    if isinstance(x,dict):
        yield p,x
        for k,v in x.items():yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
for ci,actors in [(8,{'S':(-3,3),'D':(-2,4)}),(9,{'D':(-2,4)}),(10,{'D':(-2,4)})]:
    old=d['completeCases'][ci];new=copy.deepcopy(old)
    for path,x in walk(new):
        if 'actorId' in x and x['actorId'] in actors and x.get('regularStart')==0 and x.get('nextRegularStart')==6:
            start,nxt=actors[x['actorId']]
            for k,value in [('regularStart',start),('nextRegularStart',nxt)]:
                ops.append({'op':'replace','caseIndex':ci,'relativePath':path+'/'+k,'before':x[k],'after':value});x[k]=value
    premise='Synthetic schedule clarification only: this is an ongoing fixture encounter observed at t=0. '+('; '.join(f'{a} has actual previous regular START {v[0]} and next regular START {v[1]}' for a,v in actors.items()))+'. N retains actual START0/next6. These disclosed actor opportunities are fixture inputs, not campaign facts or a global time-to-round formula. No action, Reaction, result or elapsed event is added.'
    new['premises'].append(premise)
    ops.append({'op':'add','caseIndex':ci,'relativePath':'/premises/'+str(len(old['premises'])),'beforeAbsent':True,'after':premise})
    states=[new['initialState']]+[e['after'] for e in new['timeline']]
    ck(new['id']+' complete corrected state chain',all(e['before']==states[i] for i,e in enumerate(new['timeline'])) and new['finalState']==states[-1])
    for ei,e in enumerate(new['timeline']):
        for aid,v in e['after']['actors'].items():
            b=e['before']['actors'][aid]
            if b['regularStart']!=v['regularStart']:ck(new['id']+'/'+e['id']+' corrected declared next START',b['nextRegularStart']==v['regularStart']==e['time'])
    stripped=copy.deepcopy(new);stripped['premises']=old['premises']
    for op in reversed([o for o in ops if o['caseIndex']==ci and o['op']=='replace']):
        x=stripped;parts=op['relativePath'].split('/')[1:]
        for k in parts[:-1]:x=x[int(k)] if isinstance(x,list) else x[k]
        x[parts[-1]]=op['before']
    ck(new['id']+' exact original recovered and mechanics untouched',stripped==old)
    cases.append({'originalPointer':'/completeCases/'+str(ci),'completeBefore':old,'proposedCompleteAfter':new})
proposal={'id':'BESTIARY-SCHEDULE-CORRECTION-108','status':'PROPOSED_DATA_ONLY_FIXTURE_CORRECTION_PENDING_GPT_CONFIRMATION','exactOriginalFile':{'path':str(P),'bytes':len(raw),'sha256':h(raw)},'actualFinalArchive':{'file':'DD_Bestiary_Final_Reconciliation_105_01.zip','bytes':634707,'sha256':'951bdc3d80f1b803e92584139ba50c900294af62ec7e38860ae697b96873465c'},'finding':'Four new fixture regular START events in three cases contradict the preceding nextRegularStart=6. Correct only their synthetic prior/next schedule metadata; retain all event times, actual paid Actions, Help deadline9, task RNG, damage, bodies and outcome state.','completeCases':cases,'exactOperationsRelativeToCase':ops,'passed':len(checks),'failed':0,'checks':checks,'canonicalApplied':False,'fiveMechanicalChoicesReopened':False,'originalDeliveryModified':False,'scope':'Proposed complete data correction; no new engine timing rule or campaign entitlement.'}
write('PROPOSAL.json',serial(proposal));write('CASE_REVIEW_108.json',(A/'BESTIARY_RECONCILIATION_CASE_REVIEW_108.json').read_bytes())
readme='Bestiary schedule-only follow-up108\n\nThe actual final105_01 ZIP is preserved. Independent reconstruction:44JSON/24text operations reproduce and reverse exact bytes. Independent new-case/ripple audit:220checks passed,4schedule metadata discrepancies found.\n\nPROPOSAL.json carries complete before/after cases8,9,10 and exact field operations. It proposes explicitly ongoing synthetic schedules S[-3,3] and D[-2,4] before their next actual turns; all outcomes, RNG, damage, Help expiry9, budgets and real event times remain. Please confirm this narrow fixture correction or supply a consistent alternative. No five-choice redesign, broad bestiary approval or canonical integration is requested.\n'
write('README.txt',readme.encode())
files=[{'file':p.name,'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in sorted(OUT.iterdir())]
write('MANIFEST.json',serial({'id':'BESTIARY-SCHEDULE-CORRECTION-108-MANIFEST','files':files}))
archive=A/'DD_Bestiary_Schedule_Correction_108.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):z.write(p,p.name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for r in files:assert h(z.read(r['file']))==r['sha256']
receipt={'id':proposal['id'],'proposal':{'path':str(OUT/'PROPOSAL.json'),'bytes':(OUT/'PROPOSAL.json').stat().st_size,'sha256':h((OUT/'PROPOSAL.json').read_bytes())},'archive':{'path':str(archive),'bytes':archive.stat().st_size,'sha256':h(archive.read_bytes())},'passed':len(checks),'failed':0,'actuallySentToGpt':False}
with (A/'BESTIARY_SCHEDULE_CORRECTION_RECEIPT_108.json').open('xb') as f:f.write(serial(receipt))
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps(receipt))
