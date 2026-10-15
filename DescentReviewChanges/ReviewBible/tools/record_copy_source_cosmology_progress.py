"""Reconcile navigation with source application and actual cosmology conferences."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, re, subprocess, sys
from urllib.parse import unquote
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_ACCEPTANCE_AND_RESUME.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_SOURCE_AND_COSMOLOGY_REVIEW.json'
    delta=A/'COPY_SOURCE_COSMOLOGY_NAVIGATION_DELTA.json'
    preserved_root=A/'navigation-before-copy-source-cosmology-review'
    submission_path=A/'COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json'
    assert all(not p.exists() for p in [checkpoint,delta,preserved_root,submission_path])
    now=datetime.now(timezone.utc).isoformat(); state=read(previous)
    copy_path=A/'FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json'; copy=read(copy_path)
    assert copy['checks']==1022 and not copy['failures']
    copy_ops=A/'FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json'
    for op in read(copy_ops)['changes']: assert info(G/op['after']['path'])==op['after']
    authority_path=A/'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json'; authority=read(authority_path)
    assert authority['currentAndFrozenSourceHashesVerified']==34 and not authority['cosmologyCompleted']
    prep_path=A/'COSMOLOGY_CREATION_ORIGIN_01_PREPARATION.json'; prep=read(prep_path)
    assert prep['comparisonRows']==9 and prep['payloadsVerified']==45
    sent=A/'COSMOLOGY_CREATION_ORIGIN_01_SENT_DOM.txt'
    dom=sent.read_text(encoding='utf-8')
    assert 'ChatGPT is responding' in dom and 'button "Stop"' in dom and 'DD_Cosmology_Creation_Origin_01.zip' in dom
    proof=A/'COSMOLOGY_CREATION_ORIGIN_01_SENT.png'; assert proof.is_file()
    push_path=G/'docs/audit/2026-10-15/github-snapshot/PUSH_RECEIPT.json'; push=read(push_path)
    assert push['commit']==push['verifiedRemoteCommit']=='80944e024b1dba5b1f31707b4dd951d53d9f74c8'
    index_path=R/'data/public/spell_playtests/authored_review_index.json'
    assert read(index_path)['authoredCounts']=={'reviewed':419,'pending':429}
    submission={'reviewId':prep['reviewId'],'recordedAtUtc':now,'status':'sent-once-response-running-at-submission-observation','preparation':info(prep_path),'archive':prep['archive'],'request':prep['request'],'comparison':prep['comparison'],'sentDOM':info(sent),'visibleProof':info(proof),'browserId':'3','tabId':'125745968','conversationUrl':read(A/'COSMOLOGY_SOURCE_AUTHORITY_01_SUBMISSION.json')['conversationUrl'],'payloadsVerified':45,'sourceFiles':34,'comparisonRows':9,'replyReceived':False,'sourceDoctrineChanges':0,'fullCosmologyApproved':False}
    scope=('The October15 progress backup is pushed and remotely verified at80944e024b1dba5b1f31707b4dd951d53d9f74c8; no final whole-game approval. '
           'Ordinary authored spell coverage remains419 reviewed/429 pending. Actual GPT CRS01–03 copy-release directions were received and applied to four derived source files with1022 source/preservation checks; thirteen behavioral examples remain unexecuted. '
           'The first cosmology authority conference is received and preserved: six findings dispositioned,34 source hashes verified, no doctrine rewritten or general-cosmology authority created. '
           'Creation/origin is now submitted once to actual GPT with45 payloads and nine comparison rows; no answer pre-adopted. Public/Director/revelation boundaries, unresolved identity and chronology, human balance, publication and full runtime remain open. '
           'Latest measured weekly usage16percent; mandatory owner stop50. No source information deleted.')
    start=G/'START_HERE.md'; old_start=start.read_bytes().decode(); new_start=old_start; replacements=[]
    def replace_line(prefix,replacement):
        nonlocal new_start
        old=[x for x in new_start.splitlines() if x.startswith(prefix)]; assert len(old)==1,prefix
        new_start=new_start.replace(old[0],replacement,1); replacements.append({'old':old[0],'replacement':replacement})
    replace_line('**Current joint review:**','**Current joint review:** The [authored spell index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json) remains **419 reviewed / 429 pending**. GPT’s three copy-release source rulings are [received and applied](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json): 1,022 source/preservation checks, with 13 behavioral acceptance examples still required. The [first cosmology authority verdict](docs/audit/2026-10-08/full-game/COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json) dispositions six findings without rewriting doctrine. The [creation/origins comparison](docs/audit/2026-10-08/full-game/COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json) is now with GPT. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_SOURCE_AND_COSMOLOGY_REVIEW.json). Latest measured weekly usage is 16%; stop at **50%**.')
    replace_line('**Owner-directed sequence:**','**Owner-directed sequence:** The owner-authorized progress backups were pushed and verified, most recently [15 October](docs/audit/2026-10-15/github-snapshot/PUSH_RECEIPT.json). Careful cosmology review has begun after that dependency was met. Full authored development and actual joint whole-game flow remain required before a completion or final delivery claim; neither progress backup closes those gates.')
    replace_line('| Final delivery |','| Final delivery | [Latest progress backup verified](docs/audit/2026-10-15/github-snapshot/PUSH_RECEIPT.json) at `80944e024b1dba5b1f31707b4dd951d53d9f74c8`: 18,968 selected source files verified; 86 changed delivery files committed; no tracked files deleted. Later work remains local until a further authorized delivery. The [joint flow gate](docs/audit/2026-10-08/full-game/FINAL_FLOW_AND_GITHUB_DELIVERY.md) stays open. |')
    replace_line('**Player/Director delivery is still open.**','**Player/Director delivery is still open.** The [packaging inventory](docs/audit/2026-10-08/full-game/PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json) remains its historical snapshot. Public paths do not imply approved player content. The authored spell index combines 276 preserved legacy operational records with 143 complete standalone procedures. The progress backups contain both audiences; no separate player build is certified. The [cosmology authority review](docs/audit/2026-10-08/full-game/COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json) records a source-presentation boundary risk, not proof of a deployed player leak.')
    phrase='[Copy-release questions were submitted once](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json); the source answer remains pending.'
    replacement='[Copy-release source directions are applied](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json); thirteen behavioral examples remain pending.'
    assert new_start.count(phrase)==1; new_start=new_start.replace(phrase,replacement,1); replacements.append({'old':phrase,'replacement':replacement})
    phrase='Final joint flow precedes GitHub push; remote verification precedes careful cosmology review.'
    replacement='Final joint flow remains open for completion; owner-authorized progress pushes are verified and careful cosmology review is underway.'
    assert new_start.count(phrase)==1; new_start=new_start.replace(phrase,replacement,1); replacements.append({'old':phrase,'replacement':replacement})
    inverse=new_start
    for op in reversed(replacements): inverse=inverse.replace(op['replacement'],op['old'],1)
    assert inverse==old_start
    ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    before=read(ledger_path); ledger=deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-12','DD-14','DD-50','DD-61','DD-65','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'copy-source-and-cosmology-authority-review','recordedAtUtc':now,'copySourceApplication':copy_path.relative_to(G).as_posix(),'cosmologyAuthority':authority_path.relative_to(G).as_posix(),'creationReview':submission_path.relative_to(G).as_posix(),'cosmologyCompleted':False,'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [copy_path,authority_path,submission_path,push_path])
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-12','DD-14','DD-50','DD-61','DD-65','DD-69'}: assert old==new
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_ACCEPTANCE_RESUME_NAVIGATION_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json")["changes"] + read(A / "COPY_SOURCE_COSMOLOGY_NAVIGATION_DELTA.json")["changes"]\n')
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1 and isinstance(nodes[0],ast.Constant)
    literal=ast.get_source_segment(text,nodes[0]); assert text.count(literal)==1
    text=text.replace(literal,repr(scope),1)
    text=text.replace('("Copy-release source conference — submitted", "FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json")','("Copy-release source rulings — applied; behavior pending", "FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json")')
    marker='    pending = [\n'; assert text.count(marker)==1
    text=text.replace(marker,marker+'        ("Cosmology authority verdict — six findings, bounded scope", "COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json"),\n        ("Creation/origins — nine comparisons submitted to GPT", "COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json"),\n')
    compile(text,str(nav),'exec')
    preserved=[]
    for p in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved_root/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes();preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved_root/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    submission_path.write_bytes(encoded(submission)); start.write_bytes(new_start.encode()); ledger_path.write_bytes(encoded(ledger));nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger_path,nav]]
    changes[0].update(operations=replacements,inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'allClosureAndHumanEvidenceUnchanged':True,'rulesChanged':0,'cosmologyDoctrineChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).extend([{'historicalSubmission':state['activeGptReview'],'terminalSourceDecision':info(A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json'),'derivedApplication':info(copy_path)},{'submission':info(A/'COSMOLOGY_SOURCE_AUTHORITY_01_SUBMISSION.json'),'terminalDecision':info(authority_path)}])
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageLedger=info(ledger_path),coverageDelta=info(delta),activeGptReview=submission,ordinaryAuthoredCountsCurrent=read(index_path)['authoredCounts'],currentAuthoredIndex=info(index_path),featCopyReleaseQuestions={'status':'source-rulings-received-and-derived-source-applied; behavior pending','decision':info(A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json'),'application':info(copy_path),'operations':info(copy_ops),'behavioralExamplesExecuted':0,'behavioralExamplesStillRequired':13},cosmologyAuthorityReview={'status':'six findings dispositioned; full semantic comparison incomplete','receipt':info(authority_path),'doctrineChanges':0},cosmologyCreationReview={'status':submission['status'],'submission':info(submission_path)},progressBackup={'receipt':info(push_path),'commit':push['commit'],'wholeGameAcceptance':False},pushed=True,cosmologyReviewed=False,cosmologyReviewScope='First authority conference complete for six findings; creation/origins submitted; full cosmology remains open.',usageAtLatestCheck={'usedPercent':16,'windowDurationMins':10080,'stopAtUsedPercent':50},navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['safeNextActions']=['Check weekly usage periodically; at50percent save checkpoint and pause under the owner instruction.','Observe the existing actual GPT creation/origin response in Chrome3 tab125745968; preserve its complete reply/downloaded evidence before applying any proposal. Do not restart after an observation timeout.','Implement the thirteen CRS copy-release behavioral examples against paid acquisition/capture, actual source components, class-qualification and ordinary chronological casting history; source checks alone are not behavioral completion.','Continue the remaining429 ordinary spells and all open feat, bestiary, Director, integration and packaging work.','Cosmology comparison order remains creation/origins, gods/pantheons, planes, souls/death/resurrection, history, divine/class powers and campaign revelations. Preserve unknowns, original words and all authority/audience distinctions.','Latest verified backup80944e0 precedes this checkpoint. New work is local; full game approval, runtime, human balance and publication remain open.']
    state.setdefault('preservationManifests',[]).append(info(preserved_root/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    links=set()
    for op in replacements:
        for target in re.findall(r'\]\(([^)]+)\)',op['replacement']):
            if '://' in target or target.startswith('#'):continue
            p=(G/unquote(target.split('#')[0])).resolve(); assert p.is_relative_to(G.resolve()) and p.is_file(),target
            links.add(target)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'changedLinksChecked':len(links),'ordinaryAuthoredCounts':read(index_path)['authoredCounts'],'sourceInformationDeleted':0,'cosmologyDoctrineChanged':False}))

if __name__ == '__main__':main()
