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
    oldq, newq = base/'remaining_work_queue_22.json', base/'remaining_work_queue_23.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_RESOURCE_29.json'
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_CONTROL_30.json'
    delta = A/'RANK8_CONTROL_30_NAVIGATION_DELTA.json'
    report = A/'RANK8_CONTROL_30_CHECK.json'
    keep = A/'navigation-before-rank8-control-30'
    assert not any(p.exists() for p in [newq, cp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat()
    checks = []
    def ck(n, v):
        checks.append({'check':n,'passed':bool(v)})
        assert v, n
    pp = A/'RANK8_CONTROL_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    prep = read(pp)
    candidate = read(G/prep['candidate']['path'])
    for k in ['candidate','archive','manifest','check','request']:
        ck('Exact conference '+k, info(G/prep[k]['path']) == prep[k])
    ids = [r['spellId'] for r in candidate['records']]
    previous = read(oldq)
    q = deepcopy(previous)
    group = {'group':'rank8-control5','phase':'source-conference-prepared-unsent',
        'identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(pp),
        'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0,
        'newCurrentEncounters':0,'riskCounts':candidate['riskCounts']}
    q['groups'].append(group)
    for row in q['rows']:
        if row['id'] in ids:
            ck('Previously ungrouped '+row['id'],row['currentGroup'] is None)
            row['previousPhaseBeforeConference30'] = row['currentPhase']
            row.update(currentGroup=group['group'],currentPhase=group['phase'],
                nextAction='Confer with actual GPT on18 unselected control-source choices. Resolve Prism state/time/save timing, Presence sight admission, Power Word150HP threshold/lifetime, Mental Collapse communication/casting boundaries and Reality Rewrite subjective effect before adopting procedures/cases.')
    q['sourceBindings'].extend([info(oldq),info(pp),prep['candidate'],prep['archive'],prep['check']])
    q.update(id='REMAINING-WORK-QUEUE-23',recordedAtUtc=now,previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        preparedOrActualReviewIdentityCount=172,originalSourceOrReceiptWorkCount=151)
    ck('323 identities/order retained',[r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('25 disjoint groups172 identities',len(q['groups']) == 25 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 172)
    ck('151 ungrouped',sum(r['currentGroup'] is None for r in q['rows']) == 151)
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
    added = '**Rank-eight control sources:** The [five-spell source conference](docs/audit/2026-10-08/full-game/RANK8_CONTROL_5_SOURCE_CONFERENCE_01_PREPARATION.json) preserves61 full sources, five placements,11 reviewed spell counterparts and18 unselected questions.251 source/access/authority/preservation checks pass; three identities are tierB and two tierC. Frozen Time Prism needs an explicit movement/action/time state; Paralyzing Presence retains actual sight and one-round Paralyzed; Power Word Stun keeps150HP-or-less; Mental Collapse keeps its one-minute communication/casting denial; Reality Rewrite remains one-creature subjective experience plus WIS-or-Stunned. Existing condition, hard-control, language and clock contracts retain their scopes. No procedure/case is adopted.'
    github = '**GitHub preservation:** Commit `4e7ec8d2c9c77931ecc18e74dbcbf96eebd64cb1` contains work through checkpoint28, including all three rank-seven source conferences and handoff03.25,597 expected blobs were verified; all25,371 prior tracked entries were retained. The integrity report was added in a separate follow-up commit without rewriting history. See the [verified receipt](docs/audit/2026-10-18/github-snapshot-rank7-sources/PUSH_RECEIPT.json). Later rank-eight resource6/control5 conferences and queues22–23/checkpoints29–30 remain local pending a later snapshot.'
    for p in [start,guide]:
        text = raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint29]','[checkpoint30]')
        parts = text.split('\n\n')
        for prefix in ['**Remaining spell work:**','**GitHub preservation:**','**GPT continuation required:**']:
            ck('One navigation paragraph '+prefix+p.name,sum(s.startswith(prefix) for s in parts) == 1)
        for n,s in enumerate(parts):
            if s.startswith('**Remaining spell work:**'):
                parts[n] = s.replace('Queue22','Queue23').replace('remaining_work_queue_22.json','remaining_work_queue_23.json').replace('167 in twenty-four active/prepared groups and 156','172 in twenty-five active/prepared groups and 151')+'\n\n'+(added if p == start else added.replace('(docs/audit/','(../../../docs/audit/'))
            elif s.startswith('**GitHub preservation:**'):
                parts[n] = github if p == start else github.replace('(docs/audit/','(../../../docs/audit/')
            elif s.startswith('**GPT continuation required:**'):
                link = 'docs/audit/2026-10-08/full-game/GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'
                if p == guide: link = '../../../'+link
                parts[n] = '**GPT continuation required:** Part4 reached its explicit conversation-length limit; no Illusion14 final exists. The [prepared handoff03]('+link+') contains56 context source files and five full nested progress/source archives through checkpoint26. Initial Illusion14 and current-acceptance archives remain separate full attachments. Creating Part5 still awaits the owner response; no new delivery or approval is inferred. Later perception5, gate/glyph3, resource6 and control5 packets plus queue23/checkpoint30 supplement that frozen handoff; handoff03 does not claim to include them.'
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger)
    before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "RANK8_RESOURCE_29_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous map navigation tail',code.count(tail) == 1)
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "RANK8_CONTROL_30_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint30 — rank-eight control sources',cp.relative_to(G).as_posix()),('Current323 pending identities — queue23',newq.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint29 — rank-eight resource sources','Checkpoint29 history — rank-eight resource sources').replace('Current323 pending identities — queue22','Queue22 history — before control-source preparation')
    code = code.replace('    pending = [\n','    pending = [\n        '+repr(('Rank8 control5 —18 questions,3B/2C, UNSENT',pp.name))+',\n',1)
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 full; Part5 creation pending owner authorization; no Illusion final. Queue23:172 identities in25 active/prepared groups,151 ungrouped. Rank8 control5 preserves61 sources/5 placements/18 unselected questions/251 checks,3B2C; no procedures/cases adopted. Native control, language, clock and life contracts remain unchanged. All pending rank7 access identities have review packets, not semantic approval. Handoff03 remains through26, with later complete supplements. All75 domain gates unchanged. Verified push4e7ec8d through28 preserves25597 blobs/allpriorentries; resource6/control5/checkpoints29–30 local. Allowance42percentremaining; continue to review completion or20percent.'
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
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq),rank8Control5SourceConference=info(pp))
    ck('All75 full domain rows unchanged',cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p,t in edits.items(): p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint.update(id='ACTIVE-AUTHORING-RANK8-CONTROL-30',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),
        currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],rank8Control5SourceConference=info(pp),
        lastUsageObservation={'usedPercent':58,'remainingPercent':42,'windowMinutes':10080,'secondary':'unavailable'},
        latestVerifiedGitHubBackup={'commit':push['commit'],'receipt':info(pushp),'coverage':'Work through checkpoint28;25597 expected blobs verified;all25371 prior entries retained. Separate follow-up integrity report commit; no history rewrite.'},
        verifiedGitHubPush=info(pushp),
        laterLocalWork=['Rank8 resource6 source conference:24 questions/52 sources/229 checks; queue22/checkpoint29. All choices unselected and UNSENT.', 'Rank8 control5 source conference:18 questions/61 sources/251 checks; queue23/checkpoint30. All choices unselected and UNSENT.'],
        latestPreparedContinuation=info(A/'GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'),
        coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),
        continuationCurrencyQualification='Handoff03 is current through checkpoint26. Perception5/gate-glyph3/resource6/control5 and queue23/checkpoint30 are later supplemental context; send complete cohort packets at actual review, preserving the frozen handoff.')
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
