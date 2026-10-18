"""Record bounded implementation and the confirmed GPT conversation limit."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    P=R/'data/director/spell_review'
    oldq=P/'remaining_work_queue_16.json';newq=P/'remaining_work_queue_17.json'
    oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_SOUL_CONTACT_RECOVERY_21.json'
    cp=A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_RELEASE_CONTINUATION_22.json'
    delta=A/'COPY_RELEASE_CONTINUATION_22_NAVIGATION_DELTA.json'
    report=A/'COPY_RELEASE_CONTINUATION_22_CHECK.json'
    status=A/'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json'
    keep=A/'navigation-before-copy-release-continuation-22'
    assert not any(p.exists() for p in [newq,cp,delta,report,status,keep])
    now=datetime.now(timezone.utc).isoformat();checks=[]
    def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
    ui=A/'GPT_REVIEW_PART4_LENGTH_LIMIT_01_UI.txt';error=ui.read_text('utf8')
    ck('Exact saved actual UI length-limit observation',error.startswith('The conversation is too long, please start a new one.'))
    prep=A/'FEAT335_COPY_RELEASE_01_PREPARATION.json';pp=read(prep);result=read(A/'FEAT335_COPY_RELEASE_01_CHECK.json')
    ck('136 finite checks, no broad approval',result['checks']==136 and result['failures']==[] and result['runtimeApproved'] is False and result['wholeGameComplete'] is False)
    for k in ['archive','progress','request','manifest']:ck('Copy evidence exact '+k,info(G/pp[k]['path'])==pp[k])
    push=G/'docs/audit/2026-10-18/github-snapshot-sources-recovery/PUSH_RECEIPT.json'
    ck('Last verified push f919',read(push)['commit']==read(push)['remoteMain']=='f919c20a62b98d4c65e38320954185f00e3b1f2b')
    status.write_bytes(encoded({'id':'GPT-PART4-LENGTH-LIMIT-01','recordedAtUtc':now,
        'status':'CONVERSATION_LENGTH_LIMIT; CONTINUATION_PENDING_USER_AUTHORIZATION',
        'actualUiEvidence':info(ui),'observedText':error,
        'priorChat':{'title':'Review Continuation Part 4','threadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8'},
        'latestVerifiedSubstantiveUserTurn':'99c03218-f9ed-4545-8792-d4d87ec6e4fb',
        'illusionFinalReceived':False,'newChatCreated':False,
        'continuationHandoff':info(A/'GPT_CONTINUATION_05_HANDOFF_01_PREPARATION.json'),
        'pendingAuthorization':'Create Calibration Review Part 5 in Dungeon Crawler and carry forward the prepared handoff and full review archives; no answer received.',
        'latestProjectObservation':'Project DOM was responsive in Chrome tab125746509 this turn. Review Continuation Part4 remains listed; no Part5 appeared in the inspected project list. No message was sent this turn.',
        'qualification':'Recovery text appeared before the length-limit error; no new server-saved turn ID or successful response is asserted.',
        'nextAction':'On actual authorization, create/use the continuation, preserve Part4 and send the full Illusion14 conference plus current context. Then send the queued full Companion05/CR2 evidence. The new copy implementation progress remains UNSENT.',
        'newApprovalInferred':False}))
    q=deepcopy(read(oldq));beforeq=deepcopy(q)
    for group in q['groups']:
        if group['group']=='illusion-perception14':
            group['previousPhaseBeforeCheckpoint22']=group['phase']
            group.update(phase='gpt-chat-length-limit-continuation-pending-authorization',currentCollaborationStatus=info(status))
    for row in q['rows']:
        if row['currentGroup']=='illusion-perception14':
            row['previousPhaseBeforeCheckpoint22']=row['currentPhase']
            row.update(currentPhase='gpt-chat-length-limit-continuation-pending-authorization',nextAction='Part4 reached its actual conversation-length limit. Continue full Current12 in a user-authorized continuation chat with the two complete archives and current handoff. No final or semantic acceptance exists.')
    q.update(id='REMAINING-WORK-QUEUE-17',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])))
    q['sourceBindings'].extend([info(oldq),info(status),info(prep)])
    ck('All323 spell identity/order retained',[r['id'] for r in q['rows']]==[r['id'] for r in beforeq['rows']] and len(q['rows'])==323)
    for old,new in zip(beforeq['rows'],q['rows']):
        ck('Spell source/access/membership retained '+old['id'],all(old[k]==new[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
    ck('142 in19 groups;181 ungrouped',len(q['groups'])==19 and sum(g['identityCount'] for g in q['groups'])==142 and sum(r['currentGroup'] is None for r in q['rows'])==181)
    for b in q['sourceBindings']:ck('Exact queue source '+b['path'],info(G/b['path'])==b)
    start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py'
    ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]}
    text='**GPT continuation required:** Part4 reached the explicit conversation-length limit. The [actual UI evidence and status](docs/audit/2026-10-08/full-game/GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json) distinguish this from the earlier connection interruption. No Illusion14 final exists. The [verified continuation handoff](docs/audit/2026-10-08/full-game/GPT_CONTINUATION_05_HANDOFF_01_PREPARATION.json) and both full review archives are prepared; creating Part5 remains pending the owner’s response. Preserve Part4; do not infer delivery or approval.'
    copy='**Agreed feat-copy release integration:** [136 checks and19 conditional paid histories](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_01_CHECK.json) connect all7 profiles to acquired permissions, existing RP, chronological Refrain, current providers, consumed copy/round allowances and the shared concentration ledger. [Complete progress and coverage](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_01_PROGRESS.json) keep actual Shaman/Mirrorsage providers, recipient effects, full Ready transactions and live runtime open. Ready concentration alone is exercised from a paid-preparation premise. The [full source/code/evidence update](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_01_PREPARATION.json) is UNSENT to GPT; no new rule or feat approval is adopted.'
    edits={}
    for p in [start,guide]:
        t=raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint21]','[checkpoint22]')
        parts=t.split('\n\n');oldprefix='**GPT illusion/perception14 review interrupted:**'
        ck('Unique collaboration paragraph '+p.name,sum(x.startswith(oldprefix) for x in parts)==1)
        rel=lambda s:s if p==start else s.replace('(docs/audit/','(../../../docs/audit/')
        for n,s in enumerate(parts):
            if s.startswith(oldprefix):parts[n]=rel(text)+'\n\n'+rel(copy)
            elif s.startswith('**Remaining spell work:**'):parts[n]=s.replace('Queue16','Queue17').replace('remaining_work_queue_16.json','remaining_work_queue_17.json')
            elif s.startswith('**GitHub preservation:**'):
                parts[n]=rel('**GitHub preservation:** [Verified commit f919c20](docs/audit/2026-10-18/github-snapshot-sources-recovery/PUSH_RECEIPT.json) contains checkpoint21 and all preceding source preparations, with no prior tracked files deleted. The Part4 length-limit evidence, continuation handoff, feat-copy implementation and checkpoint22 are later local work; this checkpoint does not claim another push.')
        edits[p]='\n\n'.join(parts).replace('latest observation was 52% remaining','latest observation was 50% remaining')
    cov=read(ledger);beforecov=deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,activeGptState='Part4 conversation-length limit; continuation pending explicit owner authorization; no Illusion final.',collaborationStatus=info(status))
    cov['boundedFeatCopyReleaseProgress']=info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json')
    ck('75 full domain rows and gates unchanged',cov['aspects']==beforecov['aspects'] and len(cov['aspects'])==75)
    code=raw[builder].decode('utf8');tail=' + read(A / "SOUL_CONTACT_RECOVERY_21_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One prior navigation tail',code.count(tail)==1)
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "COPY_RELEASE_CONTINUATION_22_NAVIGATION_DELTA.json")["changes"]\n')
    featured=[('Current checkpoint22 — paid copy integration and GPT continuation',cp.relative_to(G).as_posix()),('Current323 pending identities — queue17',newq.relative_to(G).as_posix()),('Actual Part4 length limit and pending continuation',status.relative_to(G).as_posix()),('Copy release —136 finite checks, full integration open',(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json').relative_to(G).as_posix())]
    code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1)
    code=code.replace('Current checkpoint21 — soul/contact sources and review recovery','Checkpoint21 history — soul/contact sources and recovery').replace('Current323 pending identities — queue16','Queue16 history — before confirmed GPT length limit').replace('Actual GPT recovery is unconfirmed','Earlier GPT recovery delivery evidence')
    scope='Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 reached its explicit conversation-length limit. Full continuation handoff ready; new Part5 pending owner authorization. No Illusion final. CompanionExact05 plus CR2 evidence UNSENT. Queue17 keeps142 identities/19 groups and181 ungrouped. Agreed feat-copy direct Action release now has136 passing finite checks/19 conditional histories; Ready concentration only; Shaman/Mirrorsage providers, recipient payloads and runtime remain open. Full update UNSENT to GPT. No new rules, deletions or75-domain gate promotions. Last verified GitHub f919c20 covers checkpoint21; later work local. Latest allowance50percentremaining; stop at20percent or actual review completion.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    ck('One status',len(nodes)==1);code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec')
    saved=[]
    for p,b in raw.items():
        dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
        saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    newq.write_bytes(encoded(q));cov['activeOrdinarySpellReview']['currentQueue']=info(newq);ledger.write_bytes(encoded(cov))
    for p,t in edits.items():p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes=[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint=deepcopy(read(oldcp));checkpoint['previousGptReviewAtCheckpoint21']=deepcopy(checkpoint['activeGptReview'])
    checkpoint.update(id='ACTIVE-AUTHORING-COPY-RELEASE-CONTINUATION-22',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],activeGptReview=read(status),boundedFeatCopyRelease=info(prep),verifiedGitHubPush=info(push),
        laterLocalWork=['Actual Part4 conversation-length-limit evidence and continuation handoff01','Agreed feat-copy release implementation,136 finite checks and full UNSENT GPT update','Queue17 and checkpoint22 with all75 domain rows unchanged'],
        lastUsageObservation={'usedPercent':50,'remainingPercent':50,'windowMinutes':10080,'secondary':'unavailable'},
        nextAction='On owner authorization create/use GPT continuation and submit full Illusion14 Current12 plus current context. Then CompanionExact05 plus CR2 evidence. Send the complete copy integration update and resolve its exact Ready-allowance question when that cohort is reached. Continue independent agreed-rule work meanwhile.',
        coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    cp.write_bytes(encoded(checkpoint))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    ck('Review map build '+run.stderr[-1200:],run.returncode==0)
    build=read(buildfile);ck('No missing links',not build['missingLinks'])
    checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))


if __name__=='__main__':main()
