"""Apply the exact jointly accepted EPI08-14 candidate without changing source history."""
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'relic-null-03-local-patch-01/candidate';archive=A/'DD_Relic_Null_03_Local_Patch_01.zip'
    confirmation=A/'RELIC_NULL_03_FINAL_MODULE_CONFIRMATION_01_DOM.txt';seen=confirmation.read_text(encoding='utf-8')
    assert info(archive)['sha256']=='748593ca501cd43c6557a4101525ed1362d89d3283c7c41bad4070df540aefcb'
    assert info(root/'RELIC_NULL_MODEL.json')['sha256']=='b4c3a10725f057ba156f819ba668ef70df8a7f5bb1d28e76778008816752d0ed'
    assert info(archive)['sha256'] in seen and 'FINAL EPI-08–14 MODULE-LEVEL VERDICT: ACCEPT' in seen
    assert 'no concrete remaining authored-procedure blocker and no remaining source-conflict blocker' in seen
    assert 'ACCEPT the complete corrected EPI-08–14 candidate' in seen
    sourcecheck=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_RETURN_SOURCE_CHECK_01.json'
    patchcheck=A/'RELIC_NULL_03_LOCAL_PATCH_01_VALIDATION.json'
    assert read(sourcecheck)['failureCount']==read(patchcheck)['failureCount']==0
    target=R/'data/director/cosmology/epilogue_relic_null_reviewed_01.json'
    cases=R/'data/director/cosmology/epilogue_relic_null_cases_01.json'
    player=R/'docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md'
    director=R/'docs/director-only/cosmology/EPILOGUE_RELIC_NULL_REVIEWED_01.md'
    receipt=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json'
    assert all(not x.exists() for x in [target,cases,player,director,receipt])
    originals={n:(root/n).read_bytes() for n in ['RELIC_NULL_MODEL.json','CASEBOOK.json','PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','SOURCE_HASHES.json']}
    m=json.loads(originals['RELIC_NULL_MODEL.json']);book=json.loads(originals['CASEBOOK.json']);sources=json.loads(originals['SOURCE_HASHES.json'])
    assert len(book['cases'])==75 and len(sources['sources'])==85
    current_sources=[]
    guide='DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    for binding in sources['sources']:
        current=info(G/binding['path']);same=all(current[k]==binding[k] for k in ['path','bytes','sha256'])
        assert same or binding['path']==guide,('Unexpected current gameplay source drift',binding['path'])
        current_sources.append({'frozen':binding,'currentAtApplication':current,'same':same,'explanation':None if same else 'Current reading-order navigation records subsequent submissions, proposed later arcs and recovery. Full diff inspected: navigation/status only; no source gameplay procedure changed. Frozen reviewed version remains preserved and authoritative for its historical evidence.'})
    now=datetime.now(timezone.utc).isoformat()
    data={'id':'COSMOLOGY-EPILOGUE-RELIC-NULL-REVIEWED-01','recordedAtUtc':now,
      'status':'Current NEW provisional authored EPI08–14 playtest reference, jointly confirmed in actual Review Continuation Part4 and locally applied. Not canon or human/runtime/balance approval.',
      'authority':m['authority'],'scope':m['scope'],'currentModule':m,
      'historicalCandidateStatusLabels':'The nested exact candidate retains its historical pending/proposal labels. This wrapper records subsequent exact complete-module acceptance; no functional candidate field was changed during application.',
      'confirmedArchive':info(archive),'confirmedCandidate':info(root/'RELIC_NULL_MODEL.json'),'confirmation':info(confirmation),
      'sourceBindings':sources,'currentSourceComparison':current_sources,
      'validation':{'sourceCheck':info(sourcecheck),'sourceChecks':247,'patchCheck':info(patchcheck),'patchChecks':87,'failureCount':0,'authoredCases':75,'runtimeTestsExecuted':0,'humanPlaytested':False},
      'preservedArchives':[info(A/n) for n in ['DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip','DD_Cosmology_Epilogue_Relic_Null_02_Return_01.zip','DD_Cosmology_Epilogue_Relic_Null_02_Return_02.zip','DD_Cosmology_Epilogue_Relic_Null_03_Return_01.zip','DD_Relic_Null_03_Local_Patch_01.zip']],
      'notAdopted':['Cosmological canon or unresolved identities','Campaign epoch','EPI15–17','Pending spells, feats, bestiary, Director, environment or consumable proposals','Runtime, human playtest, numerical balance, whole-game flow or publication approval'],
      'sourceInformationDeleted':0,'wholeGameApproved':False,'fullCosmologyClosed':False,'published':False}
    heading='> **Current NEW provisional playtest reference.** The complete corrected EPI-08–14 module was jointly accepted in Review Continuation Part 4. Original sources and owner decisions retain authority; this is not canon, runtime, numerical-balance or human-playtest approval.'
    oldnote='> Local correction proposal01 to the preserved revision03. GPT review is pending; this is not adopted.'
    prose={n:b.decode() for n,b in originals.items() if n.endswith('.md')};status_edits=[]
    for name in prose:
        assert prose[name].count(oldnote)==1
        prose[name]=prose[name].replace(oldnote,heading,1);status_edits.append({'file':name,'old':oldnote,'replacement':heading})
    pold='## Candidate status and authority';pnew='## Playtest status and authority'
    prose['PLAYER_CHAPTER.md']=prose['PLAYER_CHAPTER.md'].replace(pold,pnew,1);status_edits.append({'file':'PLAYER_CHAPTER.md','old':pold,'replacement':pnew})
    pold='This is the complete player-facing EPI-08–14 candidate for review.';pnew='This is the complete player-facing EPI-08–14 provisional playtest reference.'
    assert pold in prose['PLAYER_CHAPTER.md'];prose['PLAYER_CHAPTER.md']=prose['PLAYER_CHAPTER.md'].replace(pold,pnew,1);status_edits.append({'file':'PLAYER_CHAPTER.md','old':pold,'replacement':pnew})
    pold='This is candidate authorship only. No EPI-08–14 adoption is claimed.';pnew='This is jointly reviewed NEW provisional playtest authorship for EPI-08–14. No canon adoption is claimed.'
    assert pold in prose['DIRECTOR_CHAPTER.md'];prose['DIRECTOR_CHAPTER.md']=prose['DIRECTOR_CHAPTER.md'].replace(pold,pnew,1);status_edits.append({'file':'DIRECTOR_CHAPTER.md','old':pold,'replacement':pnew})
    for p in [target,cases,player,director]:p.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(encoded(data));cases.write_bytes(originals['CASEBOOK.json'])
    for name,dest in [('PLAYER_CHAPTER.md',player),('DIRECTOR_CHAPTER.md',director)]:dest.write_text(prose[name],encoding='utf-8',newline='\n')
    checks=[]
    def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
    ck('nested-model-exact-confirmed-candidate',read(target)['currentModule']==m)
    ck('casebook-exact-confirmed-candidate',cases.read_bytes()==originals['CASEBOOK.json'])
    ck('all75-existing-ids-order-retained',[x['id'] for x in book['cases']]==[x['id'] for x in read(A/'cosmology-epilogue-relic-null-03-return/CASEBOOK.json')['cases']])
    for name,dest in [('PLAYER_CHAPTER.md',player),('DIRECTOR_CHAPTER.md',director)]:
        restored=dest.read_text(encoding='utf-8')
        for op in reversed(status_edits):
            if op['file']==name:assert restored.count(op['replacement'])==1;restored=restored.replace(op['replacement'],op['old'],1)
        ck(name+'-only-listed-status-edits',restored.encode()==originals[name])
    ck('all85-source-bindings-preserved',read(target)['sourceBindings']==sources)
    ck('all84-current-gameplay-sources-match',sum(x['same'] for x in current_sources)==84)
    ck('original-candidate-files-unchanged',all((root/n).read_bytes()==b for n,b in originals.items()))
    failures=[x for x in checks if not x['passed']];assert not failures,failures
    receipt.write_bytes(encoded({'recordedAtUtc':now,'confirmation':info(confirmation),'confirmedArchive':info(archive),'confirmedCandidate':info(root/'RELIC_NULL_MODEL.json'),'data':info(target),'playerChapter':info(player),'directorChapter':info(director),'casebook':info(cases),'sourceCheck':info(sourcecheck),'patchCheck':info(patchcheck),'sourceChecks':247,'patchChecks':87,'applicationChecks':checks,'applicationCheckCount':len(checks),'failureCount':0,'statusOnlyProseEdits':status_edits,'sourceBindings':85,'currentSourceComparison':current_sources,'authoredCases':75,'newProvisionalModuleAdopted':True,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'campaignEpochChosen':False,'wholeGameApproved':False,'fullCosmologyClosed':False,'published':False}))
    print(json.dumps({'receipt':info(receipt),'player':info(player),'director':info(director),'data':info(target),'applicationChecks':len(checks),'failureCount':0}))

if __name__=='__main__':main()
