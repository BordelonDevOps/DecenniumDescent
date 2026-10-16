"""Reconcile every ordinary spell reference after exact AC4 adoption."""
from collections import Counter
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from audit_current_spell_review_01 import pointer

def main():
    out=A/'CURRENT_SPELL_REVIEW_RECONCILIATION_02.json';assert not out.exists()
    base=R/'data/public/spell_playtests';cache={};bindings={};checks=[];rows=[]
    def read(p):
        p=p.resolve();assert p.is_relative_to(G.resolve())
        if p not in cache:cache[p]=json.loads(p.read_bytes());bindings[p]=info(p)
        return cache[p]
    def ck(name,ok,detail=None):
        row={'name':name,'passed':bool(ok)}
        if not ok:row['detail']=detail
        checks.append(row)
    index=read(base/'authored_review_index.json');catalog=read(base/'catalog.json');higher=read(R/'data/director/higher_spell_operating_proposal_index.json');old={x['spellId']:x for x in higher['entries']}
    ck('848 unique index IDs exactly match catalog',len(index['entries'])==len({e['id'] for e in index['entries']})==848 and {e['id'] for e in index['entries']}=={e['id'] for e in catalog['spells']})
    ck('Current catalog hash matches',info(base/'catalog.json')['sha256']==index['sourceCatalogSha256'])
    ck('Low-rank standalone binding',info(base/'candidate_low_rank_136.json')['sha256']==index['standaloneEnvelopeSha256'])
    for e in index['entries']:
        data=read(base/e['procedureFile']);card=pointer(data,e['wholeCardPointer']);field=e.get('wholeCardIdField','id')
        ck(e['id']+' exact whole-card identity',card.get(field)==e['id'])
        reviewed=e['authoredStatus']=='reviewed-authored-operational-playtest'
        if reviewed:
            procedure=pointer(data,e['procedurePointer']);ck(e['id']+' complete procedure reference',isinstance(procedure,dict) and bool(procedure))
            if e.get('procedureTextPointer'):ck(e['id']+' full prose reference',pointer(data,e['procedureTextPointer'])==card['procedure'] and len(card['procedure'])>300)
            if e.get('sharedRulesPointer'):ck(e['id']+' shared rules reference',bool(pointer(data,e['sharedRulesPointer'])))
            for p in e.get('supportingProfilePointers',[]):ck(e['id']+' complete profile '+p,bool(pointer(data,p)))
        else:ck(e['id']+' remains unpromoted',e.get('procedurePointer') is None)
        for k in ['completeEnvelopeBinding','authoredAcceptanceReceipt']:
            if k in e:ck(e['id']+' '+k,info(G/e[k]['path'])==e[k])
        if e.get('manuscript'):ck(e['id']+' actual manuscript exists',(base/e['manuscript']).resolve().is_file())
        state='reviewed-authored-operational-playtest' if reviewed else old[e['id']]['proposalState'] if e['id'] in old else e['authoredStatus']
        row={'id':e['id'],'name':e['name'],'authoredStatus':e['authoredStatus'],'procedureFile':e['procedureFile'],'wholeCardPointer':e['wholeCardPointer'],'currentWorkState':state}
        if not reviewed and e['id'] in old:
            h=old[e['id']];row.update(preparationFile=h['preparationFile'],proposalFile=h['proposalFile'],sharedAsFeatComparison=h['sharedAsFeatComparison'])
            if h['proposalFile']:
                records=[r for r in read(G/h['proposalFile'])['records'] if r['spellId']==e['id']]
                ck(e['id']+' preserved pending proposal identity',len(records)==1);row['authoredExampleCount']=len(records[0]['workedCases']) if len(records)==1 else None
        rows.append(row)
    accepted=[]
    for env in index['additionalStandaloneEnvelopes']:
        for k in ['binding','authority','receipt']:ck(env['reviewId']+' '+k,info(G/env[k]['path'])==env[k])
        receipt=read(G/env['receipt']['path']);ck(env['reviewId']+' accepted exact membership',set(receipt['acceptedSpellIds'])==set(env['acceptedIds']))
        for b in receipt['acceptedArtifactBindings']:ck(env['reviewId']+' accepted payload '+b['path'],info(G/b['path'])==b)
        accepted.extend(env['acceptedIds'])
    counts=Counter(e['authoredStatus'] for e in index['entries']);represented=Counter(e['procedureFile'] for e in index['entries'] if e['authoredStatus']=='reviewed-authored-operational-playtest');pending=[r for r in rows if r['authoredStatus']!='reviewed-authored-operational-playtest'];stages=Counter(r['currentWorkState'] for r in pending)
    ck('434 reviewed /414 pending actual membership',counts['reviewed-authored-operational-playtest']==434 and len(pending)==414 and index['authoredCounts']=={'reviewed':434,'pending':414})
    ck('276+136+7+15 reviewed representations',represented=={'catalog.json':276,'candidate_low_rank_136.json':136,'../spell_candidates/divination_rank7_exact_01.json':7,'../spell_candidates/abjuration_conjuration_rank4_reviewed_03.json':15})
    ck('Pending165 proposals+201 to author+48 historical source-only',stages=={'complete-unadopted-proposal':165,'source-question-prepared-procedure-not-yet-proposed':201,'post-push-literal-receipt-only':47,'receipt-only-post-push-cosmology':1})
    superseded=[e['id'] for e in index['entries'] if e['id'] in old and e['authoredStatus']=='reviewed-authored-operational-playtest']
    ck('Only accepted DI7+AC4 supersede historical higher index',set(superseded)==set(accepted) and len(accepted)==22)
    ck('Banishment remains pending',next(e for e in index['entries'] if e['id']=='banishment')['authoredStatus']=='pending-authored-procedure')
    application=read(A/'AC4_EXACT_ACCEPTANCE_03_OPERATIONS.json')
    for change in application['changes']:
        ck('Current integrated output '+change['after']['path'],info(G/change['after']['path'])==change['after'])
        original=change['before'];preserved=G/original['preservedCopy'];b=info(preserved)
        ck('Preserved prior output '+original['path'],all(b[k]==original[k] for k in ['bytes','sha256']))
    for p,b in bindings.items():ck('Audit input unchanged '+p.relative_to(G).as_posix(),info(p)==b)
    failures=[c for c in checks if not c['passed']]
    doc={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Complete848-ID authored-reference/preservation reconciliation; no runtime simulation','ordinaryCount':848,'authoredCounts':index['authoredCounts'],'reviewedRepresentations':dict(represented),'pendingWorkStates':dict(stages),'pendingAuthoredProposals':{'complete':165,'sharedOnlyAsFeatComparison':sum(r.get('sharedAsFeatComparison',False) for r in pending if r.get('proposalFile')),'dedicatedReviewStillRequired':True},'historicalIndexSupersededIds':superseded,'entries':rows,'inputs':list(bindings.values()),'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'checks':checks,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    out.write_bytes(encoded(doc));print(json.dumps({'report':info(out),'counts':index['authoredCounts'],'pending':dict(stages),'checks':len(checks),'failures':failures[:8]}))

if __name__=='__main__':main()
