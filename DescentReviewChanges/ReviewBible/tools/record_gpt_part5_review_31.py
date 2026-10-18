"""Record actual Part5 delivery and repair current navigation; preserve every prior state."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import ast
import json
import subprocess
import sys
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    base = R/'data/director/spell_review'
    oldq, newq = base/'remaining_work_queue_23.json', base/'remaining_work_queue_24.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_CONTROL_30.json'
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PART5_REVIEW_31.json'
    receiptp = A/'GPT_CONTINUATION_05_ACTUAL_START_01.json'
    delta = A/'GPT_PART5_REVIEW_31_NAVIGATION_DELTA.json'
    report = A/'GPT_PART5_REVIEW_31_CHECK.json'
    keep = A/'navigation-before-gpt-part5-review-31'
    assert not any(p.exists() for p in [newq, cp, receiptp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat()
    checks = []
    def ck(n, v):
        checks.append({'check':n,'passed':bool(v)})
        assert v, n
    appp = A/'GPT_CONTINUATION_05_ACTUAL_START_01_APP.json'
    requestp = A/'GPT_CONTINUATION_05_ACTUAL_START_01_REQUEST.txt'
    uip = A/'GPT_CONTINUATION_05_ACTUAL_START_01_UI.txt'
    app = read(appp)
    tid = '6ad4a867-f330-83e9-829e-bf2bb41a6c09'
    uid = '49c773ce-baf8-44ed-9658-595d5a7e5b10'
    url = 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/'+tid
    ck('Actual native chat identity',app['thread']['id'] == tid and app['thread']['title'] == 'Calibration Review Part 5')
    ck('Actual native user turn',app['turns'][0]['id'] == uid and app['turns'][0]['status'] == 'completed')
    ck('Exact full request delivered',app['turns'][0]['items'][0]['content'][0]['text'] == requestp.read_text('utf8').rstrip()+'\n\n[User attached 3 files; file contents were not included]')
    ck('Actual UI generation at capture','button "Stop"' in uip.read_text('utf8'))
    files = [
        ('DD_Continuation_05_Handoff_03.zip','DD_Continuation_05_Handoff_03.zip',14554879,'dc406a0665740d7148503947faa7561929da32d8a231ee045c892fb4995ef568'),
        ('DD_Illusion_Perception_14_Conference_12.zip','DD_Illusion_Perception_14_Conference_12(1).zip',6026932,'625b1be66eafe2dce1ce43d5d53900de98bfe66d0aa96a679276edc2554276ab'),
        ('DD_Control_Illusion_Current_Acceptance_Context_01.zip','DD_Control_Illusion_Current_Acceptance_Context_01(1).zip',1818434,'b6c44900551f63abbee02d29256aade0477f9990e547a50c53447ef272de14ca')]
    attached = {a['name'] for a in app['attachments']}
    ck('Exactly three actual attachment names',attached == {x[1] for x in files})
    bindings = []
    for name,shown,size,sha in files:
        b = info(A/name)
        ck('Exact submitted archive '+name,b['bytes'] == size and b['sha256'] == sha)
        with zipfile.ZipFile(A/name) as z:
            ck('Archive CRC '+name,z.testzip() is None)
        bindings.append({'file':b,'actualAttachmentName':shown})
    receipt = {'id':'GPT-CONTINUATION-05-ACTUAL-START-01','recordedAtUtc':now,
        'status':'ACTUALLY_DELIVERED; ILLUSION14_REVIEW_IN_PROGRESS_AT_CAPTURE; NO_FINAL_RECEIVED',
        'chat':{'title':app['thread']['title'],'threadId':tid,'url':url},'actualUserTurn':uid,
        'actualUserTurnTimestamp':app['turns'][0]['startedAt'],
        'request':info(requestp),'nativeReadEvidence':info(appp),'uiEvidence':info(uip),'attachments':bindings,
        'observationQualification':'The native read showed only the completed user turn and an idle aggregate status while the browser showed GPT reading the supplied archives and the Stop button. Native aggregate status was not used to restart the live response. No assistant final or semantic acceptance is asserted.',
        'authorizationBasis':'The owner explicitly directed continuing development with GPT, pushing latest changes to GPT, conferring on consequential issues and keeping GPT regularly involved. The prior extra continuation confirmation was an unnecessary Codex interpretation, not an actual browser-policy requirement or automatic approval rejection. No new human answer is claimed. Historical pending labels remain preserved as historical states.',
        'priorLengthLimitEvidence':info(A/'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json'),
        'reviewPriority':'Full Illusion/Perception14 Current12, with current accepted-interface supplement. CompanionExact05 and expanded CR2 evidence are next as separate full attachments.',
        'deliveredForAwareness':'Handoff03 contains full copy commitment/recipient/class integrations and full Rank8Damage6 and Rank7IdentityCasting5 conferences. Formal semantic review of those later source conferences and COPY-READY-ALLOWANCE-01 remains pending; delivery alone is not acceptance.',
        'laterSummaryOnly':'Rank7Perception5, Rank7GateGlyph3, Rank8Resource6 and Rank8Control5 summaries and checkpoint30/queue23 currency were included in the exact request. Their full packets have not yet been sent.',
        'localProofScreenshot':'C:/Users/cbord/Documents/ChatGPT/Decennium Descent/audit_work/continuation05-delivered01.png',
        'sourceInformationDeleted':0,'semanticAcceptanceClaimed':False,'runtimeApprovalClaimed':False,'wholeGameComplete':False}
    previous = read(oldq)
    q = deepcopy(previous)
    matches = [g for g in q['groups'] if g['group'] == 'illusion-perception14']
    ck('Unique Illusion14 group',len(matches) == 1)
    group = matches[0]
    oldgroup = deepcopy(group)
    group.update(phase='actual-gpt-part5-current12-semantic-conference-in-progress',
        previousGroupAtCheckpoint30=oldgroup,actualUserTurn=uid,actualGptThread=tid,
        latestObservedStatus='Part5 received all three full archives and is visibly reviewing Current12. No final or acceptance received at this observation.')
    for row in q['rows']:
        if row['id'] in group['identities']:
            row['previousPhaseBeforeCheckpoint31'] = row['currentPhase']
            row.update(currentPhase=group['phase'],nextAction='Receive and preserve actual Part5 final and exact return archive; verify full source-linked decisions and reversible operations before applying any successor. Do not interrupt the live review.')
    q.update(id='REMAINING-WORK-QUEUE-24',recordedAtUtc=now,previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        deliveredContextNotYetConferenced=receipt['deliveredForAwareness'])
    ck('323 identities/order retained',[r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('25 disjoint groups172 identities',len(q['groups']) == 25 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 172)
    ck('151 ungrouped',sum(r['currentGroup'] is None for r in q['rows']) == 151)
    ck('Other prepared groups unchanged',[g for g in q['groups'] if g['group'] != group['group']] == [g for g in previous['groups'] if g['group'] != group['group']])
    for before,after in zip(previous['rows'],q['rows']):
        ck('Original source/access/member '+before['id'],all(before[k] == after[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
    for b in q['sourceBindings']:
        ck('Exact queue source '+b['path'],info(G/b['path']) == b)
    index = R/'data/public/spell_playtests/authored_review_index.json'
    ib = info(index)
    ck('525 reviewed323 pending',read(index)['authoredCounts'] == {'reviewed':525,'pending':323})
    start,guide = G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md'
    builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'
    mapfile,buildfile = G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    raw = {p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]}
    current = '**GPT collaboration resumed:** [Calibration Review Part 5]('+url+') received the full handoff03, Illusion14 Current12 and current-acceptance archives. The [actual delivery receipt](docs/audit/2026-10-08/full-game/GPT_CONTINUATION_05_ACTUAL_START_01.json) records the saved user turn, exact request, attachments and live review evidence. GPT is reviewing all14 procedures,28 original/current cases,3 supplements and16 questions; no final or acceptance has yet been recorded. Part4 and its length-limit history remain preserved. The extra continuation confirmation was an unnecessary Codex interpretation; standing owner authorization already covers this work. CompanionExact05 plus expanded CR2 evidence are next. Handoff03 includes complete copy integrations and two later source conferences for awareness; perception5/gate-glyph3/resource6/control5 were summarized and their full packets remain to be delivered.'
    edits = {}
    for p in [start,guide]:
        text = raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint30]','[checkpoint31]')
        text = text.replace('the latest observation was 44% remaining','the latest observation was 41% remaining')
        parts = text.split('\n\n')
        ck('Unique continuation navigation '+p.name,sum(s.startswith('**GPT continuation required:**') for s in parts) == 1)
        for n,s in enumerate(parts):
            if s.startswith('**GPT continuation required:**'):
                parts[n] = current if p == start else current.replace('(docs/audit/','(../../../docs/audit/')
            elif s.startswith('**Remaining spell work:**'):
                parts[n] = s.replace('Queue23','Queue24').replace('remaining_work_queue_23.json','remaining_work_queue_24.json')
            elif s.startswith('**Agreed feat-copy release integration:**'):
                parts[n] = s.replace('is UNSENT to GPT','was delivered to GPT inside handoff03 for awareness')
            elif s.startswith('**Copied recipient effects integrated:**'):
                parts[n] = s.replace('are UNSENT to GPT','were delivered to GPT inside handoff03 for awareness')
            elif s.startswith('**Shaman and Mirrorsage copy integration:**'):
                parts[n] = s.replace('is prepared UNSENT to GPT','was delivered to GPT inside handoff03 for awareness')
            elif s.startswith('**GitHub preservation:**'):
                parts[n] = s+' The actual Part5 continuation and queue24/checkpoint31 also remain local.'
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger)
    before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "RANK8_CONTROL_30_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous map navigation tail',code.count(tail) == 1)
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "GPT_PART5_REVIEW_31_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint31 — actual GPT Part5 review',cp.relative_to(G).as_posix()),('Current323 pending identities — queue24',newq.relative_to(G).as_posix()),('Actual GPT continuation delivery',receiptp.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint30 — rank-eight control sources','Checkpoint30 history — rank-eight control sources').replace('Current323 pending identities — queue23','Queue23 history — before GPT Part5 continuation')
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Calibration Review Part5 actually received handoff03, Illusion14 Current12 and the current acceptance supplement. Live GPT review in progress at capture; no final or new acceptance. Part4 preserved. Prior additional authorization gate corrected under standing owner instructions. Queue24 preserves172 identities in25 groups and151 ungrouped. Copy integration progress and two complete source conferences delivered inside handoff for awareness; later four conference summaries supplied, full packets pending. All75 domain gates unchanged. Verified GitHub4e7ec8d through28; subsequent work including this actual continuation remains local. Latest allowance41percentremaining; continue to review completion or20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value == 'notebookReview']
    ck('One map notebook status',len(nodes) == 1)
    code = code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    compile(code,str(builder),'exec')
    saved = []
    for p,b in raw.items():
        dst = keep/p.relative_to(G)
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(b)
        ck('Exact prior navigation '+p.name,dst.read_bytes() == b)
        saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    receiptp.write_bytes(encoded(receipt))
    group['actualSubmission'] = group['currentCollaborationStatus'] = info(receiptp)
    q['sourceBindings'].extend([info(oldq),info(receiptp),info(requestp),info(appp),info(uip)])
    newq.write_bytes(encoded(q))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq),activeGptSubmission=info(receiptp),activeGptState=receipt['status'],collaborationStatus=info(receiptp))
    ck('All75 full domain rows unchanged',cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p,t in edits.items(): p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint['previousGptReviewAtCheckpoint30'] = deepcopy(checkpoint['activeGptReview'])
    checkpoint.update(id='ACTIVE-AUTHORING-GPT-PART5-REVIEW-31',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),
        currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],activeGptReview=receipt,
        lastUsageObservation={'usedPercent':59,'remainingPercent':41,'windowMinutes':10080,'secondary':'unavailable'},
        nextAction='Receive actual GPT Current12 final/return without interrupting the live review; preserve and verify all decisions and operations before adopting a successor. Then submit CompanionExact05 and full CR2 supplement. Continue regular source-linked updates.',
        coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),
        continuationCurrencyQualification='Frozen handoff03 through26 actually delivered in Part5. Exact start request supplies later checkpoint30/queue23, verified GitHub and four conference summaries. Later full conference archives still require separate delivery; no semantic approval inferred.')
    checkpoint['laterLocalWork'].append('Actual GPT Part5 continuation delivery and queue24/checkpoint31; current Illusion14 review resumed without new authorship.')
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    ck('Review map build '+run.stderr[-1200:],run.returncode == 0)
    build = read(buildfile)
    ck('No missing links',not build['missingLinks'])
    ck('Authored index unchanged',info(index) == ib)
    checkpoint['navigation'] = {'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]}
    cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'actualSubmission':info(receiptp),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'indexUnchanged':ib,'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'actualSubmission':info(receiptp),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))


if __name__ == '__main__':
    main()
