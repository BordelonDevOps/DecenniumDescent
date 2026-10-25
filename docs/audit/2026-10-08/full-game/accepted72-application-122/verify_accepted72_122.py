import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
D=A/'accepted72-application-122'
I=R/'data/public/spell_playtests/authored_review_index.json'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ptr(x,p):
    for k in p.split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~')
        x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(label,condition):
    assert condition,label
    checks.append(label)
receipt=read(D/'APPLICATION_RECEIPT.json'); index=read(I);before=read(D/'authored_review_index.before.json')
accepted=set(receipt['identitiesApplied']); models={};case_counts={}
check('Index matches application receipt',digest(I)==receipt['afterIndex']['sha256'])
check('Catalog unchanged',digest(G/receipt['catalogPreserved']['path'])==receipt['catalogPreserved']['sha256'])
for b in receipt['outputs']:
    p=G/b['path'];check('Output binding '+b['path'],p.stat().st_size==b['bytes'] and digest(p)==b['sha256'])
for cb in receipt['cohortReceipts']:
    c=read(G/cb['path']);m=G/c['canonicalModel']['path'];source=G/c['acceptedModelSource']['path']
    check(c['id']+' exact complete model',m.read_bytes()==source.read_bytes())
    models[m.resolve()]=read(m)
    casebook=read(G/c['casebook']['path']);case_counts[c['id']]=len(casebook.get('cases',casebook.get('currentCases',[])))
    check(c['id']+' holds copied', (G/c['holds']['path']).is_file())
for e in index['entries']:
    if e['id'] not in accepted:continue
    model=models[(I.parent/e['procedureFile']).resolve()]
    card=ptr(model,e['wholeCardPointer'])
    check(e['id']+' whole-card identity',card[e['wholeCardIdField']]==e['id'])
    text=ptr(model,e['procedureTextPointer'])
    check(e['id']+' full operative procedure',isinstance(text,str) and len(text)>100)
    check(e['id']+' scoped shared-rule pointer',bool(ptr(model,e['sharedRulesPointer'])))
    check(e['id']+' chapter exists',(I.parent/e['manuscript']).is_file())
    check(e['id']+' reviewed with runtime disabled',e['authoredStatus']=='reviewed-authored-operational-playtest' and e['runtimeSelectionEnabled'] is False)
    check(e['id']+' retained catalog card',(ptr(read(G/receipt['catalogPreserved']['path']),e['sourceCatalogWholeCardPointer'])['id']==e['id']))
check('776 other index entries preserved',[e for e in before['entries'] if e['id'] not in accepted]==[e for e in index['entries'] if e['id'] not in accepted])
check('Exactly 72 selected',len(accepted)==72)
check('597 reviewed and251 pending',index['authoredCounts']=={'reviewed':597,'pending':251})
check('321 standalone and276 legacy',index['representationCounts']=={'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':321})
inventory=read(D/'PENDING251_REVIEW_INVENTORY.json')
pending={s['id'] for g in inventory['groups'] for s in g['spells']}
check('251 pending disjoint from72 applied',len(pending)==251 and not pending.intersection(accepted))
check('250 pending procedures plus unchanged Blink receipt-only status',all(e['authoredStatus']=='pending-authored-procedure' or (e['id']=='blink' and e['authoredStatus']=='receipt-only-post-push-cosmology' and e['procedurePointer'] is None) for e in index['entries'] if e['id'] in pending))
result={'id':'ACCEPTED72-INTEGRATION-VALIDATION-122','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'passed':len(checks),'failed':0,'checks':checks,'caseCounts':case_counts,'runtimeTestsExecuted':0,'scope':'Live source, output, identity, JSON pointer, preservation and inventory checks; no repeated semantic review or game-runtime claim.'}
write(D/'VALIDATION_REPORT.json',result)
print(json.dumps({'passed':len(checks),'failed':0,'caseCounts':case_counts,'counts':index['authoredCounts']}))
