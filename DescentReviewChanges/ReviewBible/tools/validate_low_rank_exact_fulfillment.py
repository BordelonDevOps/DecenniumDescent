"""Verify current reviewed artifacts by reversing only the recorded review labels.
The resulting full bytes/JSON must equal the independently checked pre-label
artifacts; original source protection and complete authored-index pointers apply.
"""
from pathlib import Path
from hashlib import sha256
import json
from copy import deepcopy
from manifest_loader import load_protected_manifest
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return sha256(p.read_bytes()).hexdigest()
def main():
    proof=read(A/'LOW_RANK_136_EXACT_LABEL_ONLY_PROOF.json');receipt=read(A/'LOW_RANK_136_EXACT_FULFILLMENT.json')
    checks=[]
    def ck(name,good):
        checks.append({'name':name,'pass':bool(good)})
        assert good,name
    for rel,e in proof['finalArtifacts'].items():
        p=G/rel;old=A/'low-rank136-exact-prelabel'/rel
        ck('final hash '+rel,sha(p)==e['sha256'] and p.stat().st_size==e['bytes'])
        change=proof['changes'].get(rel)
        if change is None:ck('unchanged '+rel,p.read_bytes()==old.read_bytes());continue
        if change['kind']=='json':
            v=read(p)
            for op in change['operations']:
                path=op['path']
                ck('only labels '+rel+str(path),path[0] in ['version','scope','status'] or path[0]=='spells' and path[2] in ['status','reviewEvidence'])
                node=v
                for k in path[:-1]:node=node[k]
                ck('recorded label '+rel+str(path),node[path[-1]]==op['after'])
                node[path[-1]]=deepcopy(op['before'])
            ck('entire reversed envelope '+rel,v==read(old))
        else:
            v=p.read_text(encoding='utf-8')
            for op in reversed(change['operations']):
                ck('recorded text label '+rel+op['before'][:45],v.count(op['after'])==op['occurrences'])
                v=v.replace(op['after'],op['before'])
            ck('entire reversed manuscript '+rel,v==old.read_text(encoding='utf-8'))
    protected=load_protected_manifest(G)
    ck('342 full original sources unchanged',protected==receipt['protectedOriginals'] and len(protected)==342)
    pub=R/'data/public/spell_playtests';index=read(pub/'authored_review_index.json');catalog=read(pub/'catalog.json');standalone=read(pub/'candidate_low_rank_136.json')
    ck('exact ordinary identity universe',[r['id'] for r in index['entries']]==[r['id'] for r in catalog['spells']])
    ck('412 authored / 436 pending',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==412 and len(index['entries'])==848)
    ck('276 preserved legacy operational rows',sum(e['operational'] is not None for e in catalog['spells'])==276)
    ck('136 reviewed standalone procedures',sum(c['reviewEvidence']['exactCandidateApproval'] for c in standalone['spells'])==136)
    ck('no standalone runtime grant',all(c['selectionEnabled'] is False and c['reviewEvidence']['runtimeVerified'] is False for c in standalone['spells']))
    datasets={'catalog.json':catalog,'candidate_low_rank_136.json':standalone}
    for e in index['entries']:
        d=datasets[e['procedureFile']]
        def resolve(pointer):
            x=d
            for part in pointer.lstrip('/').split('/'):
                x=x[int(part)] if isinstance(x,list) else x[part]
            return x
        card=resolve(e['wholeCardPointer'])
        ck('actual whole card '+e['id'],card['id']==e['id'])
        if e['procedurePointer']:
            op=resolve(e['procedurePointer'])
            ck('complete referenced procedure '+e['id'],isinstance(op,dict) and bool(op))
            if e['procedureFile']=='candidate_low_rank_136.json':
                ck('full access/modes/shared '+e['id'],len(resolve(e['sharedRulesPointer']))==20 and card['sourceReceipt']==next(s for s in catalog['spells'] if s['id']==e['id']) and card['sourceModeBindings'])
    ck('Blink nonoperative receipt',next(c for c in standalone['spells'] if c['id']=='blink')['operationalCandidate'] is None and next(e for e in index['entries'] if e['id']=='blink')['procedurePointer'] is None)
    out={'status':'passed','scope':'Current complete authored artifact/label-reversal/source/index checks; not runtime execution or human balance.','checks':checks,'checkCount':len(checks),'failedChecks':[],'reviewedAuthored':412,'pendingAuthored':436,'protectedOriginalsUnchanged':342,'runtimeVerified':False}
    (A/'LOW_RANK_136_LOCAL_FINAL_FULFILLMENT_VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
if __name__=='__main__':main()
