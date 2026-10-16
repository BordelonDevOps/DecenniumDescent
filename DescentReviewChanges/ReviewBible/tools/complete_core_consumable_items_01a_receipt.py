"""Finish the interrupted 01A manifest/receipt without applying edits twice."""
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import A,info,encoded
from refine_core_consumable_items_01a import read,digest,render

def main():
    root=A/'core-consumable-items-local-draft-01';history=root/'history/before-refinement-01a'
    receipt=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01A_REFINEMENT.json';assert not receipt.exists()
    old=read(history/'ITEMS_MODEL.json');new=read(root/'ITEMS_MODEL.json')
    oldcb=read(history/'CASEBOOK.json');cb=read(root/'CASEBOOK.json');check=read(root/'LOCAL_CHECKS.json')
    assert oldcb['count']==48 and cb['count']==52 and check['refinementCheckCount']==7 and check['failures']==0
    assert (root/'DIRECTOR_DISCUSSION.md').read_text(encoding='utf-8')==render(new)
    assert all(x['pass'] for x in check['refinementChecks'])
    prior={x['id']:x for x in old['items']};changes=[]
    reasons={
        ('CB-04','benefit'):'Resolve continuous/paused clock contradiction with cumulative rough-motion seconds within one episode.',
        ('CB-04','endingOrCrash'):'Define quiet recovery and exact episode-reset boundary independently of brew expiry.',
        ('CS-03','endingOrCrash'):'Prevent a rest before the crash from prepaying its proposed post-crash benefit lock.',
        ('CS-10','benefit'):'Remove unsupported positive-base gate and state ordinary zero/negative damage flooring.',
        ('CS-12','repetitionAndTolerance'):'Select an actual stored-element dose before cone orientation; preserve per-dose recoil types and order.'}
    for p in new['items']:
        for k,v in p.items():
            if prior[p['id']].get(k)!=v:
                assert (p['id'],k) in reasons
                changes.append({'itemId':p['id'],'field':k,'reason':reasons[(p['id'],k)],'before':prior[p['id']].get(k),'after':v})
    assert len(changes)==5
    oldids={x['id'] for x in oldcb['cases']};newcases=[x for x in cb['cases'] if x['id'] not in oldids];assert len(newcases)==4
    entries=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json']
    (root/'MANIFEST.json').write_bytes(encoded({'files':entries}))
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Local unadopted refinement; four source holds remain.','previousModel':info(history/'ITEMS_MODEL.json'),'previousCases':info(history/'CASEBOOK.json'),'model':info(root/'ITEMS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'discussion':info(root/'DIRECTOR_DISCUSSION.md'),'changes':changes,'newCases':newcases,'authoredSituations':52,'checks':check['refinementChecks'],'checkCount':7,'failureCount':0,'repairNote':'The first script stopped after preserving history and writing the revised model/cases/discussion/checks because a digest helper was undefined. This completion verified the actual revised state and finished only manifest/receipt; it did not apply edits twice. The helper is repaired for source completeness; the one-shot script must not be rerun.','newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeSituationsExecuted':0}))
    print(json.dumps({'refinement':info(receipt),'model':info(root/'ITEMS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'situations':52,'checks':7,'failures':0}))

if __name__=='__main__':main()
