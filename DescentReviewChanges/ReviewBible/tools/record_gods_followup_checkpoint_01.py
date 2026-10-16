"""Make verified gods evidence and the pending correction review findable."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(path): return json.loads(path.read_bytes())


def main():
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_SUBMISSION.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_FOLLOWUP_SUBMISSION.json'
    delta = A/'GODS_FOLLOWUP_01_NAVIGATION_DELTA.json'
    preserved = A/'navigation-before-gods-followup-01'
    assert all(not p.exists() for p in [checkpoint, delta, preserved])
    state = read(previous)
    now = datetime.now(timezone.utc).isoformat()
    received = A/'COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json'
    citations = A/'COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json'
    submission = A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_SUBMISSION.json'
    planes = A/'COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json'
    formula = A/'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json'
    assert read(received)['currentAndFrozenSourceHashesVerified'] == 71
    assert read(received)['candidateAssembled'] is False
    assert read(submission)['tabId'] == '125746244'
    backup_path = G/'docs/audit/2026-10-15/github-snapshot-pantheons/PUSH_RECEIPT.json'
    backup = read(backup_path)
    assert backup['commit'] == '18c6e3ae8b3c1d391dd91121693931657ae9c98f'
    start = G/'START_HERE.md'
    ledger_path = R/'data/playtest/game_development_coverage.json'
    nav = R/'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    scope = ('Gods/pantheons actual GPT verdict GP-01–09 returned and preserved: four returned evidence payloads and all71 current/frozen source hashes verified. '
             'Current-book citation errors and eight local later-source findings require follow-up before the reviewed gods companion is assembled. '
             'COSMOLOGY-GODS-PANTHEONS-FOLLOWUP-01 was sent once on Chrome tab125746244 in Calibration Review Part2 and observed responding; subsequent observation timeouts do not establish completion or failure. '
             'A preliminary planes concordance records32 public plane labels, ten comparison rows and74 spell-name matches with unchanged status (17reviewed,56pending,oneBlinkreceipt-only). '
             'The Matrix formula source check confirms23 incomplete-looking paragraphs already have those fragments in original XML. '
             'No original doctrine, class mechanics, draft flags or full-domain closure changed. Ordinary spells remain419/429. '
             'Latest verified Git backup18c6e3a precedes this follow-up work. Owner withdrew the50percentusage stop and is watching usage directly.')
    old_start = start.read_text(encoding='utf-8')
    old_lines = [s for s in old_start.splitlines() if s.startswith('**Current joint review:**')]
    assert len(old_lines) == 1
    line = '**Current joint review:** Ordinary spells remain **419 reviewed / 429 pending**. The [returned gods/pantheons verdict](docs/audit/2026-10-08/full-game/COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json) is preserved, with all 71 source hashes verified. [Citation errors](docs/audit/2026-10-08/full-game/COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json) and eight later-source findings are in a [follow-up submitted to GPT](docs/audit/2026-10-08/full-game/COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_SUBMISSION.json); the gods companion has not yet been assembled. A [preliminary plane comparison](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json) records the maps and outstanding spell dependencies. The [latest GitHub backup](docs/audit/2026-10-15/github-snapshot-pantheons/PUSH_RECEIPT.json) is commit 18c6e3a; this follow-up work is local. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_FOLLOWUP_SUBMISSION.json). Full cosmology and whole-game approval remain open. **The owner withdrew the 50% usage stop and is monitoring usage directly.**'
    new_start = old_start.replace(old_lines[0],line,1)
    assert new_start.replace(line,old_lines[0],1) == old_start
    before = read(ledger_path)
    ledger = deepcopy(before)
    touched = {'DD-50','DD-61','DD-65','DD-69'}
    evidence = [received,citations,submission,planes,formula]
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'gods-followup-01','recordedAtUtc':now,'receivedDecision':received.relative_to(G).as_posix(),'followupSubmission':submission.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in evidence)
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in touched: assert old==new
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json")["changes"]\n'
    assert text.count(chain)==1
    text = text.replace(chain,chain.rstrip('\n')+' + read(A / "GODS_FOLLOWUP_01_NAVIGATION_DELTA.json")["changes"]\n')
    nodes = [v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1 and isinstance(nodes[0],ast.Constant)
    literal = ast.get_source_segment(text,nodes[0]); assert text.count(literal)==1
    text = text.replace(literal,repr(scope),1)
    marker = '    pending = [\n'; assert text.count(marker)==1
    entries = [('Gods/pantheons — returned evidence; correction follow-up pending',received.name),('Gods/pantheons — exact citation check',citations.name),('Gods/pantheons — follow-up sent once',submission.name),('Planes — preliminary source and spell concordance',planes.name),('Matrix — original formula source gaps checked',formula.name)]
    text = text.replace(marker,marker+''.join('        '+repr(pair)+',\n' for pair in entries),1)
    compile(text,str(nav),'exec')
    preservation = []
    for path in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest = preserved/path.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(path.read_bytes()); assert dest.read_bytes()==path.read_bytes()
        preservation.append({**info(path),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    start.write_bytes(new_start.encode())
    ledger_path.write_bytes(encoded(ledger))
    nav.write_text(text,encoding='utf-8',newline='\n')
    changes = [{'before':next(x for x in preservation if x['path']==path.relative_to(G).as_posix()),'after':info(path)} for path in [start,ledger_path,nav]]
    changes[0].update(operations=[{'old':old_lines[0],'replacement':line}],inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'cosmologyDoctrineChanged':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:
        print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append({'historicalSubmission':state['activeGptReview'],'terminalDecision':info(received),'candidateAssembled':False,'followupRequired':info(citations)})
    state.setdefault('ownerInstructionHistory',[]).append({'priorUsageStopCondition':state.get('ownerUsageStopCondition'),'supersededBy':'dont worry about the limit. I am watching it.','recordedAtUtc':now})
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress: backup18c6e3a pushed and verified',coverageLedger=info(ledger_path),coverageDelta=info(delta),
        activeGptReview={'reviewId':'COSMOLOGY-GODS-PANTHEONS-FOLLOWUP-01','status':'submitted once; response last successfully observed running; later read timeouts are not terminal','tabId':'125746244','conversationTitle':'Calibration Review Part 2','submission':info(submission)},
        cosmologyGodsPantheonsReview={'receivedDecision':info(received),'citationCheck':info(citations),'candidateAssembled':False,'followupSubmission':info(submission)},
        cosmologyPlanesPreparation=info(planes),cosmologyMatrixFormulaSourceCheck=info(formula),
        ownerUsageStopCondition={'enabled':False,'ownerInstruction':'dont worry about the limit. I am watching it.','supersedes':'prior weekly 50% stop'},
        usageAtLatestCheck={'monitoring':'owner is watching; no agent-imposed 50% stop remains'},latestProgressBackup=info(backup_path),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['safeNextActions'] = [
        'Read the existing follow-up in Calibration Review Part2 on Chrome tab125746244. It was sent once and observed processing the evidence. Re-poll the same handle after transient observation timeouts; do not resend or reload solely because a read timed out.',
        'Preserve and hash-verify the corrected return, audit every corrected source citation against actual bytes, and compare all eight GPR dispositions before assembling the gods/pantheons reading companion. Keep the original returned register and citation errors as historical evidence.',
        'The original user tab125745968 is being used for a separate owner lore conversation. Do not replace its draft or navigate it away. GPT-generated proposed owner locks are not owner approval; verify actual completed owner directions before changing dependent origin doctrine.',
        'Complete the plane source comparison from the new concordance, actual Director and Matrix passages, reviewed transit procedures and pending receipts. Follow with souls/death/resurrection, full history, divine/class powers and campaign revelations.',
        'Keep all existing ordinary spell and feat status boundaries. Finish the13 copy-release behavioral examples using actual acquisition/capture/release histories, remaining429 ordinary spells and all other open game systems. Human playtesting, balance, full runtime and publication approval remain separate gates.',
        'Owner withdrew the50percent usage cutoff and monitors usage directly. Do not pause under the superseded instruction.',
        'Commit18c6e3a is the verified GitHub backup. Later review work is local and is not automatically pushed.',
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationDelta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':len(navigation['missingLinks']),'fullCosmologyApproved':False}))


if __name__=='__main__': main()
