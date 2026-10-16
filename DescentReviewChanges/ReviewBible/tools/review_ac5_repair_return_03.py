"""Independently verify Repair03 preservation and references without adoption."""
from datetime import datetime, timezone
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, encoded, info
from prepare_ac5_current_interfaces_01 import at

def read(p):
    return json.loads(p.read_bytes())

def main():
    out=A/'ac5-repair-03-return'; inp=A/'ac5-repair-03-input'
    dest=A/'AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json'
    assert not dest.exists()
    checks=[]
    def ck(label, value, **detail):
        checks.append({'check':label,'pass':bool(value),**detail})
    archive=A/'DD_AC5_Repair_03_Return.zip'; raw=archive.read_bytes()
    ck('Published archive length and digest',len(raw)==183586 and hashlib.sha256(raw).hexdigest()=='42ccbc2dd1af03a66fc814aaccbb685dcb93c884c2ace308c25285759e07ab07')
    expected={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    with zipfile.ZipFile(archive) as z:
        ck('Exactly eight safe unique root files',len(z.namelist())==8 and set(z.namelist())==expected)
        for n in sorted(expected): ck('Extracted bytes equal archive', (out/n).read_bytes()==z.read(n),path=n)
    mf=read(out/'EVIDENCE_MANIFEST.json')
    for x in mf['files']:
        b=(out/x['name']).read_bytes()
        ck('Published output length and digest',len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],path=x['name'])
    bindings=read(inp/'SOURCE_MANIFEST.json')['bindings']
    ck('All 92 frozen source bindings preserved',len(bindings)==92 and read(out/'SOURCE_HASHES.json')['bindings']==bindings)
    for x in bindings:
        for root,label in [(inp/'sources','Frozen input'),(G,'Current project')]:
            p=root/x['path']; b=p.read_bytes()
            ck(label+' source remains exact',len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],path=x['path'])
    model=read(out/'SPELLS_MODEL.json'); reg=read(out/'REGISTER.json'); cb=read(out/'CASEBOOK.json'); cases=cb['cases']
    old=read(inp/'previous-return/SPELLS_MODEL.json'); oldcases=read(inp/'previous-return/CASEBOOK.json')['cases']
    source=read(inp/'ORIGINAL_REVIEW_INPUT.json'); selected={x['spellId']:x for x in source['selectedRecords']}
    ck('Sixteen exact identities and order',[x['id'] for x in model['spells']]==list(selected) and len(selected)==16)
    for s in model['spells']:
        ck('Complete source/access unchanged',s['completeSourceAndAccess']==selected[s['id']]['completeCurrentSourceAndAccess'],spellId=s['id'])
        ck('Historical question unchanged',s['historicalQuestion']==selected[s['id']]['historicalQuestionUnchanged'],spellId=s['id'])
        ck('Complete procedure string',isinstance(s['procedure'],str) and len(s['procedure'])>300,spellId=s['id'])
        for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
            ck('Exact current procedure in chapter',s['procedure'] in (out/name).read_text(encoding='utf8'),spellId=s['id'],path=name)
    ck('Seventeen original placements',sum(len(x['completeSourceAndAccess']['source']['original']['placements']) for x in model['spells'])==17)
    ck('54 prior IDs preserved, six new substantive case IDs', [x['id'] for x in cases]==[x['id'] for x in oldcases]+[f'AC5-X{i}' for i in range(25,31)] and cb['caseCount']==60)
    original={x['id']:x['originalText'] for x in source['originalExamples']}
    ck('22 historical originals retained',len(original)==22)
    for c in cases:
        if c['id'] in original: ck('Historical original case text exact',c['historicalOriginalText']==original[c['id']],caseId=c['id'])
        ck('Current case state/action/outcome present',bool(c['currentInitialState'] and c['actionsAndResolution'] and c['currentAdjudication']),caseId=c['id'])
    dispositions=[('originalQuestionDispositions','questionDispositions',[x['questionId'] for x in source['selectedRecords']]),('currentInterfaceIssueDispositions','currentInterfaceIssueDispositions',[x['id'] for x in source['currentReviewIssues']]),('classInterfaceIssueDispositions','classInterfaceIssueDispositions',[x['id'] for x in source['currentClassInterfaceAddendum']['issues']]),('repair03Dispositions','repair03Dispositions',[f'AC5-R03-{i:02}' for i in range(1,11)])]
    for mk,rk,ids in dispositions:
        ck('Required disposition IDs and register consistency',[x['id'] for x in model[mk]]==ids and reg[rk]==model[mk],kind=mk)
    cache={}; refs=[]; descriptive=[]
    def walk(value, location):
        if isinstance(value,dict):
            if isinstance(value.get('path'),str) and 'pointer' in value:
                refs.append((location,value))
            for key,child in value.items():
                # Historical evidence is intentionally preserved, including old errors.
                if key not in ['previousCurrentVersion','historicalProposalEvidence','historicalPriorCurrentVersion']:
                    walk(child,location+'/'+key)
        elif isinstance(value,list):
            for i,child in enumerate(value):walk(child,location+'/'+str(i))
    walk(model,'SPELLS_MODEL.json');walk(reg,'REGISTER.json');walk(cases,'CASEBOOK.json/cases')
    for loc,ref in refs:
        path=ref['path'];pointer=ref['pointer']; p=out/path if path in expected else inp/'sources'/path
        ck('Referenced file present',p.is_file(),location=loc,path=path)
        if isinstance(pointer,str) and pointer.startswith('/'):
            try:
                if p not in cache:cache[p]=read(p)
                at(cache[p],pointer);ok=True
            except (OSError,KeyError,IndexError,ValueError,TypeError):ok=False
            ck('Current JSON pointer resolves',ok,location=loc,path=path,pointer=pointer)
        else:descriptive.append({'location':loc,**ref})
    for k in ['runtimeTestsExecuted','humanPlaytested','balanceApproved']:ck('No unsupported approval',model[k] is False,flag=k)
    failures=[x for x in checks if not x['pass']]
    report={'id':'AC5-REPAIR-RETURN-03-STRUCTURAL-CHECK','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Independent preservation and reference verification only. Full semantic review and exact acceptance remain separate. No adoption.','archive':info(archive),'files':[info(out/n) for n in sorted(expected)],'sourceBindings':len(bindings),'spellIdentities':16,'placements':17,'caseCount':len(cases),'historicalOriginalTexts':len(original),'referenceObjectsChecked':len(refs),'descriptiveReferences':descriptive,'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'newSpellAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}
    dest.write_bytes(encoded(report))
    print(json.dumps({'report':info(dest),'checks':len(checks),'referenceObjects':len(refs),'failures':failures}))

if __name__=='__main__':main()
