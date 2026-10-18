"""Refresh current navigation after actual GPT review; preserve every prior state."""
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
    oldq,newq = base/'remaining_work_queue_25.json',base/'remaining_work_queue_26.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_WARD_32.json'
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_PROGRESS_33.json'
    delta = A/'PART5_PROGRESS_33_NAVIGATION_DELTA.json'
    report = A/'PART5_PROGRESS_33_CHECK.json'
    keep = A/'navigation-before-part5-progress-33'
    assert not any(p.exists() for p in [newq,cp,delta,report,keep])
    now = datetime.now(timezone.utc).isoformat()
    checks = []
    def ck(name,value):
        checks.append({'check':name,'passed':bool(value)})
        assert value,name
    illusionp = A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'
    exactp = A/'ILLUSION_PERCEPTION_14_EXACT_13_PREPARATION.json'
    replayp = A/'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_RECEIPT.json'
    companionp = A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01.json'
    illusion,exact,companion = read(illusionp),read(exactp),read(companionp)
    ck('Actual Illusion assistant',illusion['actualAssistantMessageId'] == '1329ce3a-137c-4789-928c-b0eda39df21e')
    ck('Actual Companion user turn',companion['actualUserTurn'] == 'e7643d79-8ef1-4c64-b216-89a20101d269')
    for k in ['archive','candidate','artifactCheck','request']:
        ck('Exact Illusion rendering '+k,info(G/exact[k]['path']) == exact[k])
    previous = read(oldq)
    q = deepcopy(previous)
    updated = {}
    for group in q['groups']:
        name = group['group']
        if name not in ['illusion-perception14','companion-life10']:
            continue
        oldgroup = deepcopy(group)
        group['previousGroupAtCheckpoint32'] = oldgroup
        if name == 'illusion-perception14':
            group.update(phase='actual-part5-semantics-accepted-exact13-prepared-unsent',candidate=exact['candidate'],preparation=info(exactp),archive=exact['archive'],actualReturn=info(illusionp),replayReceipt=info(replayp),semanticPayloadAcceptedForIntegration=True,canonicalApplicationComplete=False,adopted=False)
            action = 'After active Companion review finishes, submit eight exact Current13 rendering artifacts. Reuse actual semantic acceptance; address only concrete rendering/flow defects, then verify canonical/index application. All conditional holds remain.'
        else:
            group.update(phase='actual-gpt-part5-exact05-companion-review-in-progress',actualSubmission=info(companionp),actualUserTurn=companion['actualUserTurn'],actualGptThread=companion['chat']['threadId'],adopted=False)
            action = 'Receive actual Part5 CompanionExact05 final without interrupting the live review; preserve and verify exact return and eight artifact bindings. Both Command Undeath exactCR2 whole-case holds remain unless actual evidence resolves them.'
        updated[name] = group
        for row in q['rows']:
            if row['id'] in group['identities']:
                row['previousPhaseBeforeCheckpoint33'] = row['currentPhase']
                row.update(currentPhase=group['phase'],nextAction=action)
    ck('Exactly two updated groups',set(updated) == {'illusion-perception14','companion-life10'})
    q['sourceBindings'].extend([info(oldq),info(illusionp),info(exactp),info(replayp),info(companionp)])
    q.update(id='REMAINING-WORK-QUEUE-26',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),limitations='Current exact receipts and index govern authored membership. Illusion14 repaired semantics are accepted for integration; canonical Exact13 rendering is prepared unsent. CompanionExact05 is actively submitted in Part5. Historical frozen labels remain history. No new authored membership, runtime, numerical balance or domain closure is claimed.')
    ck('323 identities and order unchanged',[r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('26 disjoint groups177 identities',len(q['groups']) == 26 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 177)
    ck('146 ungrouped retained',sum(r['currentGroup'] is None for r in q['rows']) == 146)
    for a,b in zip(previous['groups'],q['groups']):
        if a['group'] not in updated:
            ck('Other prepared group unchanged '+a['group'],a == b)
    for a,b in zip(previous['rows'],q['rows']):
        ck('Full source/access/member unchanged '+a['id'],all(a[k] == b[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
    for b in q['sourceBindings']:
        ck('Exact queue binding '+b['path'],info(G/b['path']) == b)
    index = R/'data/public/spell_playtests/authored_review_index.json'
    ib = info(index)
    ck('525/323 remains authoritative',read(index)['authoredCounts'] == {'reviewed':525,'pending':323})
    pushp = G/'docs/audit/2026-10-18/github-snapshot-part5-wards/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Actual verified GitHub checkpoint32 backup',push['commit'] == push['remoteMain'] == 'c9c9ffb759f3c48ce47a814f03c4e53b2cfeb2a0' and push['expectedBlobsVerified'] == 25880 and push['priorTrackedEntriesPreserved'] == 25711 and push['trackedEntriesDeleted'] == 0)
    start,guide = G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md'
    builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'
    mapfile,buildfile = G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    raw = {p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]}
    update = '**GPT collaboration current:** [Calibration Review Part 5]('+companion['chat']['url']+') returned the [actual Illusion14 semantic decision](docs/audit/2026-10-08/full-game/ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json). Two exact repairs were replayed and reversed with339 checks; all28 originals,28 current cases and3 supplements remain unchanged. The [Exact13 rendering](docs/audit/2026-10-08/full-game/ILLUSION_PERCEPTION_14_EXACT_13_PREPARATION.json) has eight full artifacts,19 routed shared clauses and309 checks; it is prepared UNSENT for faithful integration review. **525 reviewed/323 pending remains the applied count.** GPT is now actively reviewing [CompanionExact05 and expanded Command Undeath evidence](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01.json). Both exactCR2 whole-case holds remain. Do not interrupt the live review. All conditional Illusion holds, Creation, Mental Prison, Control15, runtime, human gameplay, balance, cosmology and domain gates remain separate. Ward5 was summarized in the Companion request; its full packet remains unsent.'
    github = '**GitHub preservation:** [Commit c9c9ffb](https://github.com/BordelonDevOps/DecenniumDescent/commit/c9c9ffb759f3c48ce47a814f03c4e53b2cfeb2a0) preserves work through checkpoint32, including the actual Part5 start and three rank8 source conferences.25880 expected blobs verified; all25711 prior tracked entries retained; no deletion. The Illusion return/replay/Exact13 preparation, actual Companion submission and checkpoint33 are later local work. See the [verified push receipt](docs/audit/2026-10-18/github-snapshot-part5-wards/PUSH_RECEIPT.json).'
    edits = {}
    for p in [start,guide]:
        text = raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint32]','[checkpoint33]').replace('the latest observation was 40% remaining','the latest observation was 38% remaining')
        parts = text.split('\n\n')
        for prefix in ['**Remaining spell work:**','**GitHub preservation:**','**GPT collaboration resumed:**']:
            ck('Unique navigation paragraph '+p.name+prefix,sum(x.startswith(prefix) for x in parts) == 1)
        for n,x in enumerate(parts):
            if x.startswith('**Remaining spell work:**'):
                parts[n] = x.replace('Queue25','Queue26').replace('remaining_work_queue_25.json','remaining_work_queue_26.json')
            elif x.startswith('**GitHub preservation:**'):
                parts[n] = github if p == start else github.replace('(docs/audit/','(../../../docs/audit/')
            elif x.startswith('**GPT collaboration resumed:**'):
                parts[n] = update if p == start else update.replace('(docs/audit/','(../../../docs/audit/')
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger)
    before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Actual Part5 Illusion14 repaired semantics accepted for integration. Current13 replays/reverses two changes with339 checks and zero case rewrites; Exact13 eight-file rendering prepared UNSENT with309 checks and19 scoped shared clauses. Actual CompanionExact05 plus expanded CR2 evidence actively submitted; two whole-case holds remain. Queue26 retains177 identities in26 groups and146 ungrouped. All75 domain gates unchanged. GitHub c9c9ffb verified through checkpoint32; these subsequent reviews/receipt/renderings and checkpoint33 remain local. Latest allowance38percentremaining; continue to completion or20percent.'
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "RANK8_WARD_32_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous map delta tail',code.count(tail) == 1)
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "PART5_PROGRESS_33_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint33 — actual Illusion return and Companion review',cp.relative_to(G).as_posix()),('Current323 pending identities — queue26',newq.relative_to(G).as_posix()),('Illusion14 actual semantic return and two repairs',illusionp.relative_to(G).as_posix()),('CompanionExact05 actual Part5 submission',companionp.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint32 — rank-eight ward sources','Checkpoint32 history — rank-eight ward sources').replace('Current323 pending identities — queue25','Queue25 history — before actual Illusion return')
    code = code.replace('    pending = [\n','    pending = [\n        '+repr(('Illusion14 — repaired semantics accepted; Exact13 rendering UNSENT',exactp.name))+',\n',1)
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value == 'notebookReview']
    ck('One current notebook map status',len(nodes) == 1)
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
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq),activeGptSubmission=info(companionp),activeGptState=companion['status'],collaborationStatus=info(companionp),illusion14SemanticReturn=info(illusionp),illusion14ReplayedSuccessor=info(replayp),illusion14ExactRendering=info(exactp),latestVerifiedGitHubPush=info(pushp))
    ck('All75 full domain rows unchanged',cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p,t in edits.items():
        p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint['previousAuthoringContextAt32'] = {k:deepcopy(checkpoint[k]) for k in ['activeGptReview','companionLife10','latestVerifiedGitHubBackup','laterLocalWork','nextAction']}
    checkpoint.update(id='ACTIVE-AUTHORING-PART5-PROGRESS-33',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],activeGptReview=companion,companionLife10=deepcopy(updated['companion-life10']),illusion14=deepcopy(updated['illusion-perception14']),lastUsageObservation={'usedPercent':62,'remainingPercent':38,'windowMinutes':10080,'secondary':'unavailable'},latestVerifiedGitHubBackup={'commit':push['commit'],'receipt':info(pushp),'coverage':'Work through checkpoint32;25880 expected blobs verified,25711 prior entries preserved,zero deletion.'},verifiedGitHubPush=info(pushp),laterLocalWork=['Actual Illusion14 return preserved; two operations replayed/reversed; complete Exact13 rendering prepared unsent.','Actual CompanionExact05 submission with expanded CR2 evidence preserved; review active at capture.','Queue26/checkpoint33 navigation, no membership or domain gate change.'],nextAction='Receive and verify active CompanionExact05 review, then send prepared IllusionExact13 for faithful rendering review. Apply only actual accepted exact artifacts with source/access/index validation. Continue full pending conference queue and all75 domains.',coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),continuationCurrencyQualification='Actual Part5 handoff and follow-up requests preserved. Illusion semantic return is real; Companion review active. Exact13 and full ward5 packet remain unsent. Summary delivery and source preparation do not constitute acceptance.')
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    ck('Review map build '+run.stderr[-1200:],run.returncode == 0)
    build = read(buildfile)
    ck('No missing navigation links',not build['missingLinks'])
    ck('Authored index untouched',info(index) == ib)
    checkpoint['navigation'] = {'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]}
    cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'indexUnchanged':ib,'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))


if __name__ == '__main__':
    main()
