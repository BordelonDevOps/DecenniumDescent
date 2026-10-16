"""Apply the exact jointly accepted three-arc reference, preserving all originals."""
from datetime import datetime, timezone
import hashlib, json
from zipfile import ZipFile
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    root=A/'arcs02-local-patch-01/candidate';archive=A/'DD_Campaign_Arcs_02_Local_Patch_01.zip'
    confirmation=A/'EPILOGUE_ARCS_LOCAL_PATCH_01_ACTUAL_ACCEPTANCE_NATIVE.json'
    native=read(confirmation);reply=next(x['text'] for x in native['turns'][0]['items'] if x['type']=='agentMessage')
    expected='9d5a0027d11a3185fad24de05dafe07e7a665242282a555e63642ea4a893babd'
    assert info(archive)['sha256']==expected and expected in reply
    assert '**Full-module verdict: ACCEPT.**' in reply
    assert 'ACCEPT the complete corrected `candidate/` directory' in reply
    assert 'No further replacement text or JSON-pointer correction is required' in reply
    assert all(f'AR2-{i:02} — AGREE.' in reply for i in range(1,7))
    sourcecheck=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_02.json'
    patchcheck=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_02_SEMANTIC_REVIEW_01.json'
    assert read(sourcecheck)['failureCount']==read(patchcheck)['failureCount']==0
    data=R/'data/director/cosmology/epilogue_campaign_arcs_reviewed_01.json'
    cases=R/'data/director/cosmology/epilogue_campaign_arcs_cases_01.json'
    player=R/'docs/mechanics/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_PLAYTEST.md'
    director=R/'docs/director-only/cosmology/EPILOGUE_CAMPAIGN_ARCS_REVIEWED_01.md'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_APPLICATION_CHECK.json'
    assert not any(p.exists() for p in [data,cases,player,director,receipt])
    original={p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}
    model=json.loads(original['CAMPAIGN_ARCS_MODEL.json']);book=json.loads(original['CASEBOOK.json']);sources=json.loads(original['SOURCE_HASHES.json'])
    checks=[]
    def ck(name,value):
        checks.append({'name':name,'passed':bool(value)});assert value,name
    with ZipFile(archive) as z:
        for name,raw in original.items():ck('Confirmed archive candidate bytes: '+name,z.read('candidate/'+name)==raw)
    ck('51 source bindings retained',len(sources['sources'])==51)
    for binding in sources['sources']:ck('Current source unchanged: '+binding['path'],info(G/binding['path'])==binding)
    ck('78 unique cases',[x['id'] for x in book['cases']]==[x['id'] for x in read(A/'cosmology-epilogue-campaign-arcs-01-return-02/CASEBOOK.json')['cases']] and len({x['id'] for x in book['cases']})==78)
    ck('Three named arcs',[x['id'] for x in model['arcs']]==['EPI-15','EPI-16','EPI-17'])
    now=datetime.now(timezone.utc).isoformat()
    wrapper={'id':'COSMOLOGY-EPILOGUE-CAMPAIGN-ARCS-REVIEWED-01','recordedAtUtc':now,
      'status':'Current NEW provisional authored EPI-15–17 playtest reference, jointly confirmed in actual Review Continuation Part 4 and locally applied.',
      'authority':model['common']['authority'],'placement':model['common']['placement'],'currentModule':model,
      'historicalCandidateStatusLabels':'The exact nested model and casebook retain prior proposal labels. This wrapper records subsequent exact full-module acceptance; no functional candidate field is changed by application.',
      'confirmedArchive':info(archive),'confirmedCandidate':info(root/'CAMPAIGN_ARCS_MODEL.json'),'confirmation':info(confirmation),'assistantMessageId':next(x['id'] for x in native['turns'][0]['items'] if x['type']=='agentMessage'),
      'sourceBindings':sources,'all51CurrentSourcesIdenticalAtApplication':True,
      'validation':{'sourceCheck':info(sourcecheck),'sourceChecks':read(sourcecheck)['checkCount'],'localPatchCheck':info(patchcheck),'localPatchChecks':read(patchcheck)['checkCount'],'failureCount':0,'authoredCases':78,'runtimeTestsExecuted':0,'humanPlaytested':False},
      'preservedArchives':[info(A/n) for n in ['DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_01.zip','DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_02.zip','DD_Campaign_Arcs_02_Local_Patch_01.zip']],
      'notAdopted':['Campaign era or automatic arc activation','Unresolved cosmological identities or canon','Unseen environment, consumable, spell, feat, bestiary or Director proposals','Runtime execution, human playtesting, numerical balance, whole-game flow or publication approval'],
      'sourceInformationDeleted':0,'wholeGameApproved':False,'fullCosmologyClosed':False,'published':False}
    prose={n:original[n].decode() for n in ['PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md']};edits=[]
    def replace(name,old,new):
        assert prose[name].count(old)==1,(name,old)
        prose[name]=prose[name].replace(old,new,1);edits.append({'file':name,'old':old,'replacement':new})
    replace('PLAYER_CHAPTER.md','## Player Chapter — NEW Provisional Authored Playtest Candidate (Local correction 01)','## Player Chapter — NEW Provisional Authored Playtest Reference\n\n> Jointly accepted in Review Continuation Part 4. These optional post-epilogue arcs require an agreed campaign placement before use. Original sources and owner decisions retain authority; runtime, human playtesting, balance and publication remain separate.')
    replace('DIRECTOR_CHAPTER.md','> NEW provisional authored playtest candidate. Exact local correction review is pending. Original manuscripts and explicit owner decisions retain authority. Campaign-era, runtime, human, balance, whole-game and publication gates remain separate.','> Current NEW provisional authored playtest reference, jointly accepted in Review Continuation Part 4. Original manuscripts and explicit owner decisions retain authority. Campaign-era, runtime, human, balance, whole-game and publication gates remain separate.')
    for name in prose:
        replace(name,'These classifications and the following source-interface completions are proposed authorship requiring GPT review; they are not recovered climate rules or real atmospheric simulation.','These classifications and the following source-interface completions are jointly reviewed provisional authorship; they are not recovered climate rules or real atmospheric simulation.')
        replace(name,'these detailed rights and procedures are NEW local proposals.','these detailed rights and procedures are jointly reviewed NEW local playtest authorship.')
    replace('DIRECTOR_CHAPTER.md','These are integration proposals within this local arc, not changes to printed abilities or global climate rules.','These are jointly reviewed integrations within this local arc, not changes to printed abilities or global climate rules.')
    replace('DIRECTOR_CHAPTER.md','NEW local operating proposal; not recovered legal lore or joint approval.','Jointly reviewed NEW local operating procedure; not recovered legal lore or canon approval.')
    for p in [data,cases,player,director]:p.parent.mkdir(parents=True,exist_ok=True)
    data.write_bytes(encoded(wrapper));cases.write_bytes(original['CASEBOOK.json'])
    for name,dest in [('PLAYER_CHAPTER.md',player),('DIRECTOR_CHAPTER.md',director)]:dest.write_text(prose[name],encoding='utf8',newline='\n')
    ck('Exact nested model',read(data)['currentModule']==model)
    ck('Exact casebook bytes',cases.read_bytes()==original['CASEBOOK.json'])
    for name,dest in [('PLAYER_CHAPTER.md',player),('DIRECTOR_CHAPTER.md',director)]:
        restored=dest.read_text(encoding='utf8')
        for op in reversed(edits):
            if op['file']==name:
                assert restored.count(op['replacement'])==1;restored=restored.replace(op['replacement'],op['old'],1)
        ck('Only recorded status edits: '+name,restored.encode()==original[name])
    ck('All source bindings preserved',read(data)['sourceBindings']==sources)
    ck('Original candidate files unchanged',all((root/n).read_bytes()==b for n,b in original.items()))
    ck('Earlier 51 sources unchanged after writing',all(info(G/x['path'])==x for x in sources['sources']))
    receipt.write_bytes(encoded({'recordedAtUtc':now,'confirmation':info(confirmation),'confirmedArchive':info(archive),'data':info(data),'casebook':info(cases),'playerChapter':info(player),'directorChapter':info(director),'sourceCheck':info(sourcecheck),'patchCheck':info(patchcheck),'sourceChecks':86,'patchChecks':996,'applicationChecks':checks,'applicationCheckCount':len(checks),'failureCount':0,'statusOnlyProseEdits':edits,'sourceBindings':51,'authoredCases':78,'newProvisionalModuleAdopted':True,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'campaignEpochChosen':False,'wholeGameApproved':False,'fullCosmologyClosed':False,'published':False}))
    print(json.dumps({'receipt':info(receipt),'data':info(data),'player':info(player),'director':info(director),'applicationChecks':len(checks),'failures':0}))

if __name__=='__main__':main()
