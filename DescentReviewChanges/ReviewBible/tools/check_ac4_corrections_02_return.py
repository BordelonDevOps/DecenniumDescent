"""Preserve and source-check the actual second AC4 return; semantics remain independent."""
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    incoming=Path(r'C:\Users\cbord\Downloads\DD_AC4_Corrections_02_Return.zip')
    archive=A/incoming.name;root=A/'ac4-corrections-02-return';receipt=A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json';diffpath=A/'AC4_CORRECTIONS_02_RETURN_SEMANTIC_DIFF.json'
    assert not any(p.exists() for p in [archive,root,receipt,diffpath])
    raw=incoming.read_bytes();assert len(raw)==66379 and sha(raw)=='e3fb107f1138085681d9f8035ab559968d42becd25ab528f22178c6aa64853cc'
    names={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    with ZipFile(incoming) as z:
        assert len(z.namelist())==8 and set(z.namelist())==names
        files={name:z.read(name) for name in z.namelist()}
    archive.write_bytes(raw);root.mkdir()
    for name,content in files.items():(root/name).write_bytes(content)
    model=read(root/'SPELLS_MODEL.json');cases=read(root/'CASEBOOK.json');manifest=read(root/'EVIDENCE_MANIFEST.json');sources=read(root/'SOURCE_HASHES.json');register=read(root/'REGISTER.json')
    supplied=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json');expected={x['path']:x for x in supplied['sourceBindings']};checks=[]
    def ck(name,ok,details=None):
        item={'name':name,'passed':bool(ok)}
        if not ok:item['detail']=details
        checks.append(item)
    ck('Exact seven-output manifest',len(manifest['outputFiles'])==7 and {x['path'] for x in manifest['outputFiles']}==names-{'EVIDENCE_MANIFEST.json'})
    for b in manifest['outputFiles']:ck('Output bytes '+b['path'],len(files[b['path']])==b['bytes'] and sha(files[b['path']])==b['sha256'])
    ck('Exact70 source bindings',len(sources['bindings'])==70 and {x['path']:x for x in sources['bindings']}==expected)
    with ZipFile(A/'DD_AC4_Corrections_02.zip') as z:
        for b in sources['bindings']:
            content=z.read('sources/'+b['path']);ck('Frozen source '+b['path'],len(content)==b['bytes'] and sha(content)==b['sha256'])
    for b in expected.values():ck('Current source unchanged '+b['path'],info(G/b['path'])==b)
    expected_input={k:v for k,v in info(A/'DD_AC4_Corrections_02.zip').items() if k!='path'}
    ck('Exact correction archive identity',register['correctionInputArchive']==expected_input and manifest['sourceArchive']==expected_input)
    originals={x['spellId']:x for x in supplied['records']}
    ck('All15 spell IDs/order',[x['spellId'] for x in model['spells']]==[x['spellId'] for x in supplied['records']])
    player=files['PLAYER_CHAPTER.md'].decode('utf8')
    for row in model['spells']:
        old=originals[row['spellId']]
        ck(row['spellId']+' exact source/access record',row['sourceAndAccess']==old['fullSourceAndCurrentAccessRecord'])
        ck(row['spellId']+' source hash',row['sourceRecordSha256']==old['sourceRecordSha256'])
        ck(row['spellId']+' original question identity',row['questionId']==old['questionId'])
        ck(row['spellId']+' exact procedure in Player chapter once',player.count(row['procedure'])==1)
    ids=[c['id'] for c in cases['cases']]
    ck('48 unique case IDs',len(ids)==len(set(ids))==cases['count']==48)
    ck('All30 original IDs/order',ids[:30]==[x['id'] for x in supplied['originalExamples']])
    for old,new in zip(supplied['originalExamples'],cases['cases'][:30]):ck(old['id']+' original text preserved',old['originalText']==new['originalText'])
    ck('All15 existing integration IDs/order',ids[30:45]==[x['id'] for x in supplied['requestedIntegrationExamples']])
    ck('Three additional declared correction cases',ids[45:]==['AC4-CX01','AC4-CX04','AC4-CX05'])
    ck('All8 finding dispositions',[x['id'] for x in register['correctionDispositions']]==[f'AC4-C{i:02d}' for i in range(1,9)])
    ck('Banishment exact receipt preserved',model['banishmentSourceOnlyReceipt']==supplied['banishmentSourceOnlyReceipt'])
    ck('No runtime or human execution claim',manifest['runtimeTestsExecuted']==manifest['humanPlaytestsExecuted']==0 and all(c['runtimeTest'] is False for c in cases['cases']))
    oldmodel=read(A/'ac4-current-review-01-return-01/SPELLS_MODEL.json');oldcases=read(A/'ac4-current-review-01-return-01/CASEBOOK.json')
    changes=[]
    def walk(before,after,ptr=''):
        if type(before)==type(after)==dict:
            for key in sorted(before.keys()|after.keys()):
                q=ptr+'/'+key.replace('~','~0').replace('/','~1')
                if key not in before or key not in after:changes.append({'pointer':q,'before':before.get(key),'after':after.get(key)})
                else:walk(before[key],after[key],q)
        elif type(before)==type(after)==list and len(before)==len(after):
            for i,(b,a) in enumerate(zip(before,after)):walk(b,a,ptr+'/'+str(i))
        elif before!=after:changes.append({'pointer':ptr,'before':before,'after':after})
    walk(oldmodel,model,'/model');walk(oldcases,cases,'/casebook')
    diffpath.write_bytes(encoded({'status':'Exact structural changes for independent semantic reading; not adoption','changes':changes,'changeCount':len(changes)}))
    failed=[c for c in checks if not c['passed']]
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'submittedArchive':info(A/'DD_AC4_Corrections_02.zip'),'checks':checks,'checkCount':len(checks),'failureCount':len(failed),'failures':failed,'semanticDiff':info(diffpath),'sourceIntegrityOnly':True,'semanticReview':'Pending independent examination of every revised rule/profile/example and all8 dispositions.','newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    print(json.dumps({'receipt':info(receipt),'checks':len(checks),'failures':failed[:5],'structuralChanges':len(changes),'cases':48}))

if __name__=='__main__':main()
