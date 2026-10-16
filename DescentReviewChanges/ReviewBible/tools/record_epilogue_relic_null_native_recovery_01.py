"""Record actual GPT completion without claiming an unretrieved archive is reviewed."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):
    return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_DRAFT_01.json'
    target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01.json'
    delta = A/'EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01_NAVIGATION_DELTA.json'
    recovery = A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_RECOVERY_RECEIPT.json'
    preserved = A/'navigation-before-epilogue-relic-null-native-recovery-01'
    assert all(not p.exists() for p in [target, delta, recovery, preserved])
    native = A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_COMPLETION_01.json'
    transfer = A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_01.json'
    raw = read(native)
    observed = json.loads(next(x['text'] for x in raw['content'] if x['type']=='text'))
    assert observed['thread']['id']=='6ad1498d-f244-83ea-8ffe-63e75ff98073'
    turn = observed['turns'][0]
    assert turn['status']=='completed'
    final = next(x['text'] for x in turn['items'] if x['type']=='agentMessage')
    assert '47 authored worked cases' in final and '70,386 bytes' in final
    expected_hash = '24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699'
    assert expected_hash in final
    transfer_state = json.loads(next(x['text'] for x in read(transfer)['content'] if x['type']=='text'))
    assert transfer_state['thread']['status']['type']=='systemError'
    assert transfer_state['turns'][0]['id']==turn['id']
    draftroot = A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    model = draftroot/'ARCS_MODEL.json'
    cases = draftroot/'CASEBOOK.json'
    validation = A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_02.json'
    refinement = A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_SEMANTIC_REFINEMENT_02.json'
    prep = A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_PREPARATION.json'
    packet = A/'DD_Cosmology_Epilogue_Campaign_Arcs_01.zip'
    v = read(validation)
    assert v['failureCount']==0 and v['checkCount']==44 and read(cases)['count']==19
    assert info(model)==v['model'] and info(cases)==v['casebook']
    assert info(packet)==read(prep)['archive'] and read(prep)['sourceCount']==41
    recovery.write_bytes(encoded({
        'recordedAtUtc':now,
        'conversationId':observed['thread']['id'],
        'observedTitle':observed['thread']['title'],
        'userName':'Calibration Review part 3',
        'completedUserTurnId':turn['id'],
        'completedAgentMessageId':next(x['id'] for x in turn['items'] if x['type']=='agentMessage'),
        'completionEvidence':info(native),
        'gptCompletionConfirmed':True,
        'gptReportedArchive':{'name':'DD_Cosmology_Epilogue_Relic_Null_01_Return.zip','bytes':70386,'sha256':expected_hash,'authoredCases':47,'rootFiles':8,'frozenSources':83},
        'archiveRetrieved':False,'archiveHashIndependentlyVerified':False,'semanticReviewComplete':False,
        'browserRecovery':{'browser':'Chrome 3','tabId':'125746286','downloadLinkRead':'CDP operation deadline before dispatch','completedConversationReload':'focus-emulation timeout','localSearch':'No matching returned archive in Downloads, Temp, workspace or audit directory.'},
        'nativeTransferAttempt':{'purpose':'Export the existing unchanged archive as text; no reauthoring.','sendToolReturnedConversationId':True,'subsequentRead':info(transfer),'observedStatus':'systemError','latestVisibleTurnStillOriginalCompletedReturn':True,'deliveryConfirmed':False,'chunksReceived':0,'doNotAssumeRunning':True},
        'nextRecovery':'Use the original download if browser becomes responsive, or owner downloads the existing return. If text export is needed, use chunks below 20000 characters because read_thread enforces that per-item limit; prefer 12000 characters. First inspect for any delivered request/response before resending.',
        'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False
    }))
    state = read(previous)
    start = G/'START_HERE.md'
    guide = R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'
    originals = {}
    pres = []
    for p in [start, guide, nav, ledger, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes()
        out = preserved/p.relative_to(G)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
        originals[p] = raw
        pres.append({**info(p), 'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    oldstart = originals[start].decode()
    oldline = next(x for x in oldstart.splitlines() if x.startswith('**Current joint review:**'))
    newline = '**Current joint review:** EPI-01–07 remains jointly confirmed and locally applied as **NEW provisional playtest authorship**, with [player rules](DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md), [Director rules](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EPILOGUE_CHARACTER_REVIEWED_01.md) and 110 preserved authored cases. [GPT has completed EPI-08–14](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_RECOVERY_RECEIPT.json): its reply reports four relics, twelve chambers, Null/life/purge rules, four plants and 47 authored cases. **The archive is not yet retrieved or independently reviewed; those rules remain unadopted.** Chrome download access fails, and the native transfer attempt reports a system error. The [three later campaign arcs](docs/audit/2026-10-08/full-game/cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json) have 19 authored situations and a [prepared 41-source conference packet](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_PREPARATION.json), still unsubmitted and unadopted. Continue from the [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame, unresolved identities, runtime, human playtesting, balance and whole-game flow remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(oldstart.replace(oldline, newline, 1), encoding='utf-8', newline='\n')
    oldguide = originals[guide].decode()
    anchor = '# Current cosmology reading order\n\n'
    current = '**Current recovery point:** [Actual Part 3 completion is confirmed through the app](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_RECOVERY_RECEIPT.json). GPT reports a finished EPI-08–14 archive with 47 authored cases, 83 frozen sources and eight root files. Its exact archive is still unavailable locally; no independent hash, source or semantic check has run, and these rules remain unadopted. Chrome 3/tab 125746286 still fails to read or reload; a native request to export the unchanged archive returned a system-error state with no new visible turn. Do not infer an ongoing generation or resend the authoring task. The earlier browser/generation status paragraphs below are preserved history, superseded by this completion evidence.\n\nThe **current EPI-15–17 local draft has 19 authored cases**, with [44 narrow file/source/structure/arithmetic checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_02.json) passing and a [41-source conference packet](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_PREPARATION.json) prepared but unsubmitted. The [preserved semantic refinement](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_SEMANTIC_REFINEMENT_02.json) restores worldwide random bard tune losses and the named Canian patent-heir role, resolves finite custody and clock examples, and retains all 13 prior case IDs. The earlier 12/13-case drafts remain history. These changes are proposals awaiting joint review; they do not choose the campaign era or adopt new canon. The packet creation-time context predates recovery of GPT’s completion reply and must be clarified when eventually submitted.\n\n'
    assert oldguide.count(anchor)==1
    guide.write_text(oldguide.replace(anchor, anchor+current, 1), encoding='utf-8', newline='\n')
    coverage = json.loads(originals[ledger])
    before = deepcopy(coverage)
    row = next(x for x in coverage['aspects'] if x['id']=='DD-50')
    before_row = deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [native, recovery, refinement, prep])
    row['validationEvidence'].append(validation.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-relic-null-native-recovery-01','recordedAtUtc':now,'gptCompletionConfirmed':True,'reportedReturnCases':47,'archiveRetrieved':False,'independentReturnReviewComplete':False,'campaignArcLocalCases':19,'campaignArcPacketSources':41,'campaignArcSelectedChecks':44,'campaignArcFailures':0,'newRulesAdopted':False,'campaignArcsSubmittedToGpt':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:
        assert row[k]==before_row[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope = 'EPI01–07 applied: 110 authored cases. Actual GPT EPI08–14 completion recovered through native reader: reports 47 cases, 83 sources, eight files; archive not retrieved or independently reviewed, no adoption. Chrome download/reload fail; native text-export attempt systemError, no new visible turn. EPI15–17 local proposal: 3 arcs, 19 cases, 44 narrow checks pass, 41-source packet prepared/unsubmitted. Campaign era, runtime, human balance, full-game flow and publication open; 419 reviewed/429 pending ordinary spells. Later work local.'
    text = originals[nav].decode()
    tail = ' + read(A / "EPILOGUE_CAMPAIGN_ARCS_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert text.count(tail)==1
    text = text.replace(tail, tail.rstrip('\n')+' + read(A / "EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n', 1)
    nodes = [v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1
    text = text.replace(ast.get_source_segment(text,nodes[0]), repr(scope), 1)
    items = [('EPI08–14 — actual GPT completion; archive transfer unresolved', recovery.name), ('EPI08–14 — native completion evidence', native.name), ('EPI15–17 — current 19-case semantic refinement', refinement.name), ('EPI15–17 — 44 narrow checks; no semantic approval', validation.name), ('EPI15–17 — prepared 41-source conference packet', prep.name)]
    text = text.replace('    pending = [\n', '    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items), 1)
    compile(text,str(nav),'exec')
    nav.write_text(text,encoding='utf-8',newline='\n')
    changes = [{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':anchor,'replacement':anchor+current}]
    changes[1]['operations']=[{'old':oldline,'replacement':newline}]
    changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:
        print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Completion evidence and local draft preparation only; no new adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(recordedAtUtc=now,tabId='125746286',status='Actual completed EPI08–14 response recovered; exact archive transfer unresolved',generationConfirmedLiveNow=False,generationConfirmedTerminal=True,completionEvidence=info(native),recoveryReceipt=info(recovery),reportedArchiveSha256=expected_hash,reportedArchiveBytes=70386,reportedCases=47,archiveRetrieved=False,independentReturnReviewComplete=False,nativeTransferStatus='systemError; original completed turn still latest; delivery unconfirmed')
    state['cosmologyEpilogueCampaignArcsLocalDraft'].update(status='local proposal; 41-source packet prepared, unsubmitted and unadopted',model=info(model),casebook=info(cases),refinement=info(refinement),validation=info(validation),initialFrozenSourceCount=11,conferenceSourceCount=41,authoredCases=19,conferencePreparation=info(prep),conferencePacket=info(packet),newRulesAdopted=False)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
        'Retrieve the existing exact EPI08–14 archive from Part3. Expected 70386 bytes and SHA256 '+expected_hash+'. Its completed reply is independently observed, but the archive content has not been read locally. Do not reauthor or presume semantic approval.',
        'Chrome3/tab286 download-link read and safe completed-page reload both time out. Native read_thread sees completion. Native text-export send returned the thread ID but following read reports systemError with no new visible turn. Inspect for delayed delivery before any retry. Do not infer live generation.',
        'If an exact existing-file text export becomes necessary, use at most12000 ASCII characters per message, below read_thread 20000-character cap. The unconfirmed first request used24000 and would require smaller chunks if actually delivered. Prefer original ZIP download by browser/owner.',
        'Once archive is available, run check_cosmology_epilogue_relic_null_return_01.py <archivePath> 01; then inspect all eight files and47 authored cases semantically against source and currentEPI01–07 before adoption.',
        'EPI15–17 current local model has19 cases,44 narrow passing checks and prepared41-source packet. Old12/13case preparation evidence remains historical. Clarify the packet creation-time EPI08 status when submitting; do not claim that source/file checks prove playable semantics.',
        'No source deletion, epoch choice, hidden identity resolution, runtime/human/balance/full-game/publication approval.419/429 ordinary spells. Last verified GitHub18c6e3a; later work local.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'recovery':info(recovery),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':
    main()
