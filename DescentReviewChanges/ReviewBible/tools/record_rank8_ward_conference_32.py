"""Register five source conferences without changing authored/domain gates."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import ast
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    base = R/'data/director/spell_review'
    oldq, newq = base/'remaining_work_queue_24.json', base/'remaining_work_queue_25.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PART5_REVIEW_31.json'
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_WARD_32.json'
    delta = A/'RANK8_WARD_32_NAVIGATION_DELTA.json'
    report = A/'RANK8_WARD_32_CHECK.json'
    keep = A/'navigation-before-rank8-ward-32'
    assert not any(p.exists() for p in [newq, cp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat()
    checks = []
    def ck(n, v):
        checks.append({'check':n,'passed':bool(v)})
        assert v, n
    pp = A/'RANK8_WARD_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    prep = read(pp)
    candidate = read(G/prep['candidate']['path'])
    for k in ['candidate','archive','manifest','check','request']:
        ck('Exact conference '+k, info(G/prep[k]['path']) == prep[k])
    ids = [r['spellId'] for r in candidate['records']]
    previous = read(oldq)
    q = deepcopy(previous)
    group = {'group':'rank8-ward5','phase':'source-conference-prepared-unsent',
        'identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(pp),
        'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0,
        'newCurrentEncounters':0,'riskCounts':candidate['riskCounts']}
    q['groups'].append(group)
    for row in q['rows']:
        if row['id'] in ids:
            ck('Previously ungrouped '+row['id'],row['currentGroup'] is None)
            row['previousPhaseBeforeConference32'] = row['currentPhase']
            row.update(currentGroup=group['group'],currentPhase=group['phase'],
                nextAction='Confer with actual GPT on23 unselected ward-source choices. Resolve eight native placements without union, alignment immunity, living-body exclusion, separate antimagic-family overlap, mind/divination protection and institutional-standing admission. Do not adopt procedures/cases before decisions.')
    q['sourceBindings'].extend([info(oldq),info(pp),prep['candidate'],prep['archive'],prep['check']])
    q.update(id='REMAINING-WORK-QUEUE-25',recordedAtUtc=now,previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        preparedOrActualReviewIdentityCount=177,originalSourceOrReceiptWorkCount=146)
    ck('323 identities/order retained',[r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('26 disjoint groups177 identities',len(q['groups']) == 26 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 177)
    ck('146 ungrouped',sum(r['currentGroup'] is None for r in q['rows']) == 146)
    ck('All prior groups unchanged',q['groups'][:-1] == previous['groups'])
    rank7rows = [row for row in q['rows'] if any(v['rank'] == 7 for v in row['completeCurrentSourceAndAccess']['classAccess'].values())]
    ck('All pending rank7 identities remain grouped',len(rank7rows) == 57 and all(row['currentGroup'] for row in rank7rows))
    for before,after in zip(previous['rows'],q['rows']):
        ck('Original full source/access/member '+before['id'],all(before[k] == after[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
    for b in q['sourceBindings']:
        ck('Exact queue source '+b['path'],info(G/b['path']) == b)
    index = R/'data/public/spell_playtests/authored_review_index.json'
    ib = info(index)
    ck('525 reviewed323 pending',read(index)['authoredCounts'] == {'reviewed':525,'pending':323})
    pushp = G/'docs/audit/2026-10-18/github-snapshot-rank7-sources/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Verified checkpoint28 push receipt',push['commit'] == push['remoteMain'] == '4e7ec8d2c9c77931ecc18e74dbcbf96eebd64cb1' and push['expectedBlobsVerified'] == 25597 and push['trackedEntriesDeleted'] == 0 and push['verificationRepair']['followUpCommitChangesOnlyIntegrityReport'])
    start,guide = G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md'
    builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'
    mapfile,buildfile = G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    raw = {p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]}
    edits = {}
    added = '**Rank-eight ward sources:** The [five-spell source conference](docs/audit/2026-10-08/full-game/RANK8_WARD_5_SOURCE_CONFERENCE_01_PREPARATION.json) preserves81 full sources, eight native school placements,21 reviewed counterpart cards and23 unselected questions.359 source/access/authority/preservation checks pass; two identities are tierB and three tierC. Alignment Immunity retains24hours; Antilife Shell retains10feet and concentration minute. Antimagic Field and Mind Blank keep their differing school descriptions and real class access. Reputation Fortress uses institutional standing rather than alignment. Exact ward geometry, protection channels and separate antimagic-family interactions require GPT decisions. This full packet remains UNSENT; no procedure/case is adopted.'
    for p in [start,guide]:
        text = raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint31]','[checkpoint32]').replace('the latest observation was 41% remaining','the latest observation was 40% remaining')
        parts = text.split('\n\n')
        for prefix in ['**Remaining spell work:**','**GitHub preservation:**','**GPT collaboration resumed:**']:
            ck('One navigation paragraph '+prefix+p.name,sum(x.startswith(prefix) for x in parts) == 1)
        for n,x in enumerate(parts):
            if x.startswith('**Remaining spell work:**'):
                parts[n] = x.replace('Queue24','Queue25').replace('remaining_work_queue_24.json','remaining_work_queue_25.json').replace('172 in twenty-five active/prepared groups and 151','177 in twenty-six active/prepared groups and 146')+'\n\n'+(added if p == start else added.replace('(docs/audit/','(../../../docs/audit/'))
            elif x.startswith('**GitHub preservation:**'):
                parts[n] = x+' The new ward5 conference and queue25/checkpoint32 are also local.'
            elif x.startswith('**GPT collaboration resumed:**'):
                parts[n] = x+' Ward5 was prepared after that message and has not yet been sent or summarized to GPT; wait for the live Illusion14 response before sending the next full review.'
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger)
    before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "GPT_PART5_LABELS_31A_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous map navigation tail',code.count(tail) == 1)
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "RANK8_WARD_32_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint32 — rank-eight ward sources',cp.relative_to(G).as_posix()),('Current323 pending identities — queue25',newq.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint31 — actual GPT Part5 review','Checkpoint31 history — actual GPT Part5 review').replace('Current323 pending identities — queue24','Queue24 history — before rank8 ward preparation')
    code = code.replace('    pending = [\n','    pending = [\n        '+repr(('Rank8 ward5 —23 questions,2B/3C, UNSENT',pp.name))+',\n',1)
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Actual Calibration Review Part5 is reading Illusion14 Current12; no final recorded. Full handoff03/copy integrations and two source conferences delivered for awareness; four later conference summaries supplied. Queue25:177 identities in26 active/prepared groups,146 ungrouped. New ward5 packet preserves81 sources/eight placements/23 unselected questions/359 checks,2B3C; UNSENT with no procedures/cases adopted. All75 domain gates unchanged. Verified GitHub4e7ec8d through28; subsequent source work and actual continuation remain local. Latest allowance40percentremaining; continue to review completion or20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value == 'notebookReview']
    ck('One map notebook status',len(nodes) == 1)
    code = code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    compile(code,str(builder),'exec')
    saved = []
    for p,b in raw.items():
        dst = keep/p.relative_to(G)
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(b)
        ck('Exact prior navigation preserved '+p.name,dst.read_bytes() == b)
        saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    newq.write_bytes(encoded(q))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq),rank8Ward5SourceConference=info(pp))
    ck('All75 full domain rows unchanged',cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p,t in edits.items(): p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint.update(id='ACTIVE-AUTHORING-RANK8-WARD-32',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),
        currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],rank8Ward5SourceConference=info(pp),
        lastUsageObservation={'usedPercent':60,'remainingPercent':40,'windowMinutes':10080,'secondary':'unavailable'},
        latestVerifiedGitHubBackup={'commit':push['commit'],'receipt':info(pushp),'coverage':'Work through checkpoint28;25597 expected blobs verified;all25371 prior entries retained. Separate follow-up integrity report commit; no history rewrite.'},
        verifiedGitHubPush=info(pushp),
        laterLocalWork=read(oldcp)['laterLocalWork']+['Rank8 ward5 source conference:23 questions/81 sources/359 checks; queue25/checkpoint32. All choices unselected and UNSENT.'],
        latestPreparedContinuation=info(A/'GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'),
        coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),
        continuationCurrencyQualification='Handoff03 through26 actually delivered in Part5 with Illusion14/current acceptance context. The exact start request supplies later checkpoint30/queue23 and four source summaries; new ward5 was prepared later and is UNSENT. Current live review must not be interrupted; no semantic approval inferred.')
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    ck('Review map build '+run.stderr[-1200:],run.returncode == 0)
    build = read(buildfile)
    ck('No missing links',not build['missingLinks'])
    ck('Authored index unchanged',info(index) == ib)
    checkpoint['navigation'] = {'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]}
    cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),
        'failures':0,'links':build['existingDistinctLinks'],'indexUnchanged':ib,'all75DomainGatesUnchanged':True,
        'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))


if __name__ == '__main__':
    main()
