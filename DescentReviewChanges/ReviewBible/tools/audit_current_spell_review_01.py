"""Reconcile current authored spell coverage with preserved catalog/proposal representations."""
from collections import Counter
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def pointer(data, path):
    if path == '': return data
    assert path.startswith('/')
    for part in path[1:].split('/'):
        part = part.replace('~1','/').replace('~0','~')
        data = data[int(part)] if isinstance(data,list) else data[part]
    return data


def main():
    out = A/'CURRENT_SPELL_REVIEW_RECONCILIATION_01.json'
    assert not out.exists()
    base = R/'data/public/spell_playtests'
    inputs = {}; cache = {}; checks = []; rows = []
    def read(p):
        p = p.resolve()
        assert p.is_relative_to(G.resolve())
        if p not in cache:
            inputs[p] = info(p)
            cache[p] = json.loads(p.read_bytes())
        return cache[p]
    def ck(name, ok, detail=None):
        row={'check':name,'passed':bool(ok)}
        if not ok: row['detail']=detail
        checks.append(row)
    index=read(base/'authored_review_index.json'); catalog=read(base/'catalog.json')
    higher=read(R/'data/director/higher_spell_operating_proposal_index.json')
    old={x['spellId']:x for x in higher['entries']}
    entries=index['entries']; ids=[x['id'] for x in entries]
    ck('848 unique authored IDs match preserved ordinary catalog',len(ids)==len(set(ids))==848 and set(ids)=={x['id'] for x in catalog['spells']})
    ck('Current catalog binding',info(base/'catalog.json')['sha256']==index['sourceCatalogSha256'])
    ck('Current low-rank standalone binding',info(base/'candidate_low_rank_136.json')['sha256']==index['standaloneEnvelopeSha256'])
    for e in entries:
        target=(base/e['procedureFile']).resolve(); data=read(target); card=pointer(data,e['wholeCardPointer'])
        ck(e['id']+' whole-card identity',card['id']==e['id'])
        reviewed=e['authoredStatus']=='reviewed-authored-operational-playtest'
        if reviewed:
            procedure=pointer(data,e['procedurePointer'])
            ck(e['id']+' complete procedure reference exists',isinstance(procedure,dict) and bool(procedure))
            if e.get('sharedRulesPointer'):
                ck(e['id']+' shared rules resolve',bool(pointer(data,e['sharedRulesPointer'])))
        else:
            ck(e['id']+' no pending procedure promoted',e.get('procedurePointer') is None)
        for key in ['completeEnvelopeBinding','authoredAcceptanceReceipt']:
            if key in e:
                b=e[key];actual=info(G/b['path']);ck(e['id']+' '+key,actual==b)
        if e.get('manuscript'):
            ck(e['id']+' manuscript exists',(base/e['manuscript']).resolve().is_file())
        state='reviewed-authored-operational-playtest' if reviewed else old[e['id']]['proposalState'] if e['id'] in old else e['authoredStatus']
        row={'id':e['id'],'name':e['name'],'authoredStatus':e['authoredStatus'],'procedureFile':e['procedureFile'],'wholeCardPointer':e['wholeCardPointer'],'currentWorkState':state}
        if not reviewed and e['id'] in old:
            historical=old[e['id']]
            row.update(preparationFile=historical['preparationFile'],proposalFile=historical['proposalFile'],sharedAsFeatComparison=historical['sharedAsFeatComparison'])
            if historical['proposalFile']:
                proposal=read(G/historical['proposalFile'])
                matches=[x for x in proposal['records'] if x['spellId']==e['id']]
                ck(e['id']+' proposal still contains unique record',len(matches)==1)
                row['authoredExampleCount']=len(matches[0]['workedCases']) if len(matches)==1 else None
        rows.append(row)
    for env in index['additionalStandaloneEnvelopes']:
        for key in ['binding','authority','receipt']:
            b=env[key];ck('additional envelope '+key,info(G/b['path'])==b)
        receipt=read(G/env['receipt']['path'])
        ck('DI7 accepted membership agrees',set(receipt['acceptedSpellIds'])==set(env['acceptedIds']))
        for b in receipt['acceptedArtifactBindings']:ck('DI7 accepted artifact '+b['path'],info(G/b['path'])==b)
    counts=Counter(e['authoredStatus'] for e in entries)
    represented=Counter(e['procedureFile'] for e in entries if e['authoredStatus']=='reviewed-authored-operational-playtest')
    pending=[x for x in rows if x['authoredStatus']!='reviewed-authored-operational-playtest']
    stages=Counter(x['currentWorkState'] for x in pending)
    ck('419 reviewed /429 pending counts match actual entries',counts['reviewed-authored-operational-playtest']==419 and len(pending)==429 and index['authoredCounts']=={'reviewed':419,'pending':429})
    ck('276 legacy +136 low-rank +7 DI7 reviewed procedures',represented=={'catalog.json':276,'candidate_low_rank_136.json':136,'../spell_candidates/divination_rank7_exact_01.json':7})
    ck('Pending partition 180 proposed +201 to propose +48 historical receipts',stages=={'complete-unadopted-proposal':180,'source-question-prepared-procedure-not-yet-proposed':201,'post-push-literal-receipt-only':47,'receipt-only-post-push-cosmology':1})
    stale=[x['spellId'] for x in higher['entries'] if x['spellId'] in ids and next(e for e in entries if e['id']==x['spellId'])['authoredStatus']=='reviewed-authored-operational-playtest']
    ck('Only accepted seven DI7 records supersede higher index',set(stale)==set(index['additionalStandaloneEnvelopes'][0]['acceptedIds']))
    for p,b in inputs.items():ck('Input unchanged '+p.relative_to(G).as_posix(),info(p)==b)
    failures=[c for c in checks if not c['passed']]
    record={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Current authored coverage and pointer/source audit; no mechanics or selection changes.',
      'ordinaryCount':848,'authoredCounts':{'reviewed':419,'pending':429},'reviewedRepresentations':dict(represented),'pendingWorkStates':dict(stages),
      'pendingAuthoredProposals':{'complete':180,'sharedOnlyAsFeatComparison':sum(x.get('sharedAsFeatComparison',False) for x in pending if x.get('proposalFile')),'dedicatedReviewStillRequired':True},
      'historicalIndexSupersededIds':stale,
      'meaning':'The 276/572 preserved catalog labels classify that older representation. Current authored review combines 276 legacy procedures,136 standalone low-rank procedures and7 accepted DI7 procedures. The old higher-spell proposal index predates DI7 acceptance; its seven pending entries are historical, not lost work. Forty-eight historical post-push receipts still require dedicated source/procedure decisions despite the now-completed progress push. No automatic promotion follows.',
      'nextPreparedReview':{'cohort':'abjuration_conjuration_rank4','pendingProcedureCount':15,'status':'Existing complete proposals; refresh current interfaces and confer with GPT before adoption.','ids':[x['id'] for x in pending if x.get('proposalFile','') and x['proposalFile'].endswith('/abjuration_conjuration_rank4.json')]},
      'inputs':list(inputs.values()),'entries':rows,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'checks':checks,
      'sourceInformationDeleted':0,'newRulesAdopted':False,'catalogChanged':False,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    out.write_bytes(encoded(record))
    print(json.dumps({'report':info(out),'counts':record['authoredCounts'],'pending':dict(stages),'checks':len(checks),'failures':failures[:8]}))


if __name__=='__main__':main()
