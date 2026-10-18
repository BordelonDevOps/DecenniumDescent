"""Record full rank-nine source preparation without rule/index application."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    qp = R/'data/director/spell_review/remaining_work_queue_36.json'
    outq = qp.with_name('remaining_work_queue_37.json')
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_COPIED_FEAT_DIAGNOSTICS_44.json'
    outcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45.json'
    check = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45_CHECK.json'
    keep = A/'navigation-before-rank9-catastrophe-45'
    pp = A/'RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_01_PREPARATION.json'
    assert not any(p.exists() for p in [outq, outcp, check, keep])
    q0 = read(qp); q = deepcopy(q0); cp = read(previous); prep = read(pp)
    candidate = read(G/prep['candidate']['path']); checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    protected = {p: p.read_bytes() for p in [qp, previous,
        R/'data/public/spell_playtests/authored_review_index.json',
        R/'data/public/spell_playtests/catalog.json', R/'data/playtest/game_development_coverage.json',
        R/'data/director/spell_review/accepted_interface_registry_06.json']}
    ck('Complete packet bindings', all(info(G/prep[k]['path']) == prep[k] for k in ['candidate','archive','check','manifest','request']))
    ck('Unselected source preparation', prep['status'] == 'PREPARED_UNSENT' and candidate['newRuleAdoptions'] == candidate['cosmologyDecisions'] == 0 and not candidate['currentVectors'])
    ids = [r['spellId'] for r in candidate['records']]
    ck('Ten previously ungrouped identities', len(set(ids)) == 10 and all(next(r for r in q['rows'] if r['id'] == sid)['currentGroup'] is None for sid in ids))
    group = {'group': 'rank9-catastrophe10', 'phase': 'source-conference-prepared-unsent',
        'identities': ids, 'identityCount': 10, 'candidate': prep['candidate'], 'preparation': info(pp),
        'archive': prep['archive'], 'adopted': False, 'sourceCount': 77, 'placementCount': 12,
        'questionCount': 25, 'riskCounts': {'B': 3, 'C': 7}, 'currentCaseCount': 0,
        'latestObservedStatus': 'Full native sources,12 placements,11 applied counterparts and25 unselected decisions. Preserve entire large areas, four meteors, structure/terrain effects, random plural typing and actual self-sacrifice.'}
    q['groups'].append(group)
    for before, row in zip(q0['rows'], q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'], currentPhase=group['phase'], semanticAcceptanceClaimed=False,
                nextAction='Conduct the complete catastrophe10 source conference before procedure/case authorship. Resolve actual range/duration/typing/overlap/material/sacrifice choices; preserve native magnitude and access.',
                sourceConferencePreparation=info(pp))
        ck('Full source/index/history unchanged '+row['id'], all(before[k] == row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-37', recordedAtUtc=now, previousQueue=info(qp),
        preparedOrActualReviewIdentityCount=221, originalSourceOrReceiptWorkCount=102,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])), latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp), prep['candidate'], prep['archive'], prep['check']])
    q['limitations'] += ' Rank9 catastrophe10 adds77 complete sources,12 placements and25 unselected questions.321 source-preservation checks are not semantic acceptance.102 ungrouped identities remain, all actual rank9.39 accepted identities remain unapplied.'
    ck('323 pending across35 groups and102 ungrouped', len(q['rows']) == 323 and len(q['groups']) == 35 and sum(r['currentGroup'] is not None for r in q['rows']) == 221 and sum(r['currentGroup'] is None for r in q['rows']) == 102)
    ck('39 accepted still unapplied', sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows']) == 39)
    ck('Remaining ungrouped allrank9', all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values()) == 9 for r in q['rows'] if r['currentGroup'] is None))
    start = G/'START_HERE.md'; direction = R/'docs/DEVELOPMENT_DIRECTION.md'; mapfile = G/'REVIEW_MAP.html'
    nav = {p:p.read_bytes() for p in [start,direction,mapfile]}; after = {}; base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(start,''),(direction,'../../../')]:
        text=nav[p].decode('utf-8-sig'); marker='**Current position — 18 October 2026:**'
        ck('One current position marker '+p.name,text.count(marker)==1)
        notice='**Latest work — rank-nine source review:** [Checkpoint45]('+prefix+base+outcp.name+') and [Queue37]('+prefix+outq.relative_to(G).as_posix()+') add ten catastrophe spells with77 full sources,12 placements and25 unselected decisions.321 preservation checks pass.221 pending identities now have review groups;102 rank9 identities remain ungrouped. Four copied-feat defects were independently reproduced in the [local diagnostic receipt]('+prefix+base+'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json). GPT’s final copied-feat corrections are still pending. Applied525/323/249 and39 accepted-but-unapplied identities remain unchanged.\n\n'
        after[p]=text.replace(marker,notice+marker,1).encode('utf8')
    html=nav[mapfile].decode('utf-8-sig');pos=html.index('</h1>')+len('</h1>')
    banner='<section class="sequence" aria-label="Latest source preparation"><p><strong>Checkpoint45:ten rank9 catastrophe sources prepared.</strong>77 sources,12 placements,25 unselected decisions;321 preservation checks. Queue37:221 grouped pending identities,102 ungrouped rank9. Four copied-feat defects reproduced; final GPT corrections pending. No rule application. <a href="'+base+outcp.name+'">Latest checkpoint</a> · <a href="'+outq.relative_to(G).as_posix()+'">Queue37</a></p></section>'
    after[mapfile]=(html[:pos]+banner+html[pos:]).encode('utf8')
    ck('All domain content retained',after[mapfile].decode().replace(banner,'')==html)
    keep.mkdir()
    for p,b in nav.items():(keep/p.name).write_bytes(b)
    outq.write_bytes(encoded(q))
    for p,b in after.items():p.write_bytes(b)
    cp.update(id='ACTIVE-AUTHORING-RANK9-CATASTROPHE-45',recordedAtUtc=now,
        status='Ten rank9 sources prepared, copied-feat defects preserved, GPT final pending;39 accepted spell identities remain unapplied.',
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=35,
        groupedPendingIdentities=221,ungroupedPendingIdentities=102,rank9Catastrophe10SourceConference=info(pp),
        navigation=[info(p) for p in after],preservedNavigation=[info(keep/p.name) for p in nav],
        nextAction='Receive and independently verify the actual copied-feat final, compare four reproduced defects, then update GPT with exact local progress. Continue102 ungrouped rank9 source identities; apply no reserved rule/index/runtime changes.')
    cp['laterLocalWork'] += ' Rank9 catastrophe10 source packet, Queue37 and checkpoint45 are later local work.'
    outcp.write_bytes(encoded(cp))
    for p,b in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    check.write_bytes(encoded({'recordedAtUtc':now,'scope':'Source preparation, full history preservation and navigation only.',
        'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failureCount':0,
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'check':info(check),'checks':len(checks),'grouped':221,'ungrouped':102}))

if __name__=='__main__':main()
