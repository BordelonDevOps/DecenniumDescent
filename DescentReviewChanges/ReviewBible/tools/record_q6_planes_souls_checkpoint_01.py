"""Checkpoint verified Q6, the planes conversation limit, and bounded souls reading."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_HEARTCELL_OWNER_UPDATE_02.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_Q6_PLANES_SOULS_READING_01.json'
    delta=A/'Q6_PLANES_SOULS_READING_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-q6-planes-souls-reading-01'
    limit=A/'COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json'
    handoff=A/'CALIBRATION_REVIEW_PART_3_HANDOFF_01.txt'
    assert all(not p.exists() for p in [checkpoint,delta,preserved,limit,handoff])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    q6=A/'COSMOLOGY_Q6_LATER_LOCK_01_APPLICATION_CHECK.json';q=read(q6)
    assert q['boundSourcesVerified']==28 and q['citationOccurrences']==29
    submission=A/'COSMOLOGY_PLANES_01_SUBMISSION.json'
    prep=A/'COSMOLOGY_PLANES_01_PREPARATION.json'
    souls=A/'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json'
    soulcheck=A/'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01_CHECK.json'
    dom=A/'COSMOLOGY_PLANES_01_LENGTH_LIMIT_DOM.txt'
    assert "You've reached the maximum length for this conversation" in dom.read_text(encoding='utf-8')
    assert info(A/'DD_Cosmology_Planes_01.zip')['sha256']=='158630558c141a69485c47bdfb727c8f29d1727bca1e78c45f01ac3944bd8fe5'
    for row in read(souls)['sourceBindings']:assert info(G/row['path'])==row
    limit.write_bytes(encoded({'reviewId':'COSMOLOGY-PLANES-01','recordedAtUtc':now,
        'conversationTitle':'Calibration Review Part 2','tabId':'125746244',
        'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'submission':info(submission),'inputArchive':info(A/'DD_Cosmology_Planes_01.zip'),
        'observation':info(dom),'screenshot':info(A/'COSMOLOGY_PLANES_01_LENGTH_LIMIT.png'),
        'exactVisibleNotice':"You've reached the maximum length for this conversation, but you can keep talking by starting a new chat.",
        'observedProgress':'GPT verified the exact input archive SHA256 and 64 bound files; final visible UI says Worked for6m3s / Analysis paused plus conversation-length limit. No terminal decision or output archive received.',
        'reviewCompleted':False,'verdictReceived':False,'newRulesAdopted':False,
        'nativeReaderCaveat':'Codex read_thread still returns the older failed base64-transfer branch. It is not the status of this UI-submitted review.',
        'continuation':'Owner asked whether to create Calibration Review Part3 in Dungeon Crawler. Await actual answer; elapsed time is not approval.',
        'sourceInformationDeleted':0}))
    handoff.write_text('''Decennium Descent — continuation from Calibration Review Part2.

Part2 reached ChatGPT’s conversation-length limit during COSMOLOGY-PLANES-01. It verified the attached packet’s hash and64 source bindings but returned no verdict. Continue that bounded review here. Preserve Part2 and Resolve Heartcell Origins. This is the owner’s game at C:\\Github\\DecenniumDescent; Codex maintains files and GPT is the design notebook/reviewer.

Attached: DD_Cosmology_Planes_01.zip,4196132bytes, SHA256158630558c141a69485c47bdfb727c8f29d1727bca1e78c45f01ac3944bd8fe5. Read REQUEST.txt, REVIEW_SCOPE.json, SOURCE_BINDINGS.json and PACKAGE_MANIFEST.json inside. All64 original source files are supplied under sources/. Do not depend on old chat memory or recreate facts from summaries.

Current authority: the owner says always use original cosmology and answer from existing lore first, with explicit owner corrections. HEARTCELL-OWNER-UPDATE-02 is jointly checked and supplied. Primordial cycles are ages, with no fixed year conversion. Choir attack-response/derivative-virtue intent is preserved; exact P35/P39 chronology and named Harmony mapping are unresolved. The new Equation inscriptions are commissioned drafts, not recovered original math. Research across multiple libraries, functional-knowledge taint, level5 voice/proximity taint, Hunt-triggered hardcore death and extremely rare Divine/Abyssal exceptions are qualitative owner decisions, not seven-stage or numerical mechanics. Underlying Heartcell builder remains unresolved; source preference is settled.

Q6 is complete within its bounded scope: the existing15130byte archive was recovered, all28 frozen sources and29 citation locations verified, and its Director successor applied. Regular Floor97 has a distinct hidden chamber. Floor100 confrontation produces OR exposes the crystal; avoid narrowing to guaranteed defeat/drop. OldGod/survivor/Ul’nak/Binding/Interstice identity is unresolved. Public reliable knowledge ends at the failed SixthGate. No new base64 transfer is needed.

Planes review: cover all11 PL issues and the 76-claim source inventory. Compare original four primary realms/four tributaries, the32 mortal Wheel labels/courts, saved webpage.html and actual companion viewer/data without forcing equivalence. The owner explicitly reminded us to use the saved cosmology website. Read the specified whole paragraphs/cards and distinguish semantic reading from hash validation. FactionPortal has a real cross-plane receiving-headquarters procedure; other reviewed local/observation/summoning effects retain their own scope. Twelve named higher travel effects remain pending; two supplied transport proposals are unadopted. No spell approvals by this review.

Return the exact eight-file COSMOLOGY_PLANES_01_Addendum_and_Evidence.zip requested in REQUEST.txt, including all11 decisions, readable Director chapter, plane/court index, travel matrix, source hashes, semantic coverage, verdict and evidence manifest. Use precise verifiable citations and label any new policy proposal. Leave operational soul/death jurisdiction to the next conference.

Codex has separately begun bounded original-soul and death-interface reading while this review waited. That newer preparation has not changed the attached source corpus or adopted new rules; it will follow this planes review.

Ordinary spells remain419reviewed/429pending of848; whole-game/runtime/human-playtest approval remains open. The owner-authorized progress backup is verified GitHub commit18c6e3ae8b3c1d391dd91121693931657ae9c98f; subsequent cosmology work remains local. No sources have been deleted. The owner withdrew the50%usage stop and monitors usage directly.
''',encoding='utf-8',newline='\n')
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json'
    nav=R/'tools/build_review_map.py';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
        preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('Q6 later-lock return verified and Director successor applied:28frozen sources,29citation occurrences and3exact Director paragraphs; later owner source-priority qualification retained. '
           'COSMOLOGY-PLANES-01 submitted once with64sources and11issues, then halted at ChatGPT conversation-length limit after input-hash verification; no verdict received. '
           'Part3 continuation handoff prepared; owner answer pending. Bounded souls/death reading preserves81original paragraphs,6ordinary and8class whole cards,5mechanics sections and9issues under13verified sources. '
           'No numeric taint, Hunt exception or other new mechanics adopted. Ordinary spells419reviewed/429pending. Latest verified GitHub backup18c6e3a; later work local.')
    old=start.read_text(encoding='utf-8');old_line=next(x for x in old.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The [Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) and [Q6 endgame review](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md) are saved and verified. The 64-source planes review reached [ChatGPT’s conversation-length limit](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json); a [continuation handoff](docs/audit/2026-10-08/full-game/CALIBRATION_REVIEW_PART_3_HANDOFF_01.txt) is prepared. [Souls, death and Hunt source reading](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_DEATH_REVIEW_PREPARATION_01.md) is prepared for its later conference. The saved cosmology website is included. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_Q6_PLANES_SOULS_READING_01.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    changed=old.replace(old_line,new_line,1);assert changed.replace(new_line,old_line,1)==old
    start.write_text(changed,encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8')
    extra='\nThe [planes review packet](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_01_PREPARATION.json) includes the saved website and 64 sources. GPT reached its conversation-length limit before returning a verdict; the packet and continuation handoff are preserved. The [souls/death preparation](SOULS_DEATH_REVIEW_PREPARATION_01.md) compares original soul lore, existing resurrection procedures and the Hunt owner direction; its proposed interfaces are not adopted mechanics.\n'
    current.write_text(old_current+extra,encoding='utf-8',newline='\n')
    before_ledger=read(ledger_path);ledger=deepcopy(before_ledger)
    touched={'DD-50','DD-61','DD-65','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'q6-planes-souls-reading-01','recordedAtUtc':now,'q6Verified':q6.relative_to(G).as_posix(),'planesLengthLimit':limit.relative_to(G).as_posix(),'soulsPreparation':souls.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [q6,submission,limit,souls,soulcheck])
    for a,b in zip(before_ledger['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "HEARTCELL_OWNER_UPDATE_02_NAVIGATION_DELTA.json")["changes"]\n'
    assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "Q6_PLANES_SOULS_READING_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1;literal=ast.get_source_segment(text,nodes[0]);text=text.replace(literal,repr(scope),1)
    text=text.replace('Q6 — captured terminal verdict; archive verification pending','Q6 — historical terminal capture; archive now verified')
    marker='    pending = [\n';assert text.count(marker)==1
    links=[('Q6 — verified return and current Director application',q6.name),('Planes — conversation-length limit; no verdict',limit.name),('Continuation — exact Part3 handoff',handoff.name),('Souls and death — bounded source reading, no new mechanics',soulcheck.name)]
    text=text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in links),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[q['readingOrderChange']]+[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,ledger_path,nav]]
    changes[1]['operations']=[{'old':old_current,'replacement':old_current+extra}]
    changes[2]['operations']=[{'old':old_line,'replacement':new_line}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newMechanicsAdopted':False}))
    result=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if result.returncode:print(result.stdout[-2000:]);print(result.stderr[-5000:]);raise SystemExit(result.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append({'historicalSubmission':state['activeGptReview'],'q6Application':info(q6),'status':'verified and applied with current owner qualification'})
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path),coverageDelta=info(delta),ownerStartPage=info(start),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        activeGptReview={'reviewId':'COSMOLOGY-PLANES-01','status':'submitted once; conversation-length limit prevented completion; no verdict','conversationTitle':'Calibration Review Part 2','tabId':'125746244','submission':info(submission),'lengthLimitReceipt':info(limit),'continuationHandoff':info(handoff),'continuationApproval':'asked; actual owner reply required'},
        cosmologyQ6LaterLock={'status':'verified and applied','check':info(q6),'receipt':info(A/'COSMOLOGY_Q6_LATER_LOCK_01_RECEIVED_DECISION.json'),'companion':info(R/'docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md')},
        cosmologyPlanesPreparation=info(prep),cosmologySoulsDeathPreparation={'status':'bounded local reading; unsubmitted','record':info(souls),'check':info(soulcheck)})
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions']=[
        'Use the actual owner reply about Calibration Review Part3; do not infer approval from elapsed time. Preserve existing chats. If approved, create the continuation in Dungeon Crawler and send the prepared handoff with the same exact4196132byte planes ZIP. No planes verdict has been received.',
        'Do not use native send_message_to_thread for this GPT collaboration; its stale branch caused an earlier systemError. Native read_thread still shows that older branch. Use the existing Chrome browser3 through CUA.',
        'Q6 is verified and applied; do not retrieve it again or rerun its one-use application. Its specific endgame path does not settle full entity identity or encounter mechanics.',
        'Original source priority is settled. Builder, exact Choir timing/mapping and missing original formula remain open; new inscription drafts are preserved separately.',
        'After planes, finish souls/death original and current interface reading: mortal afterlife testimony, Research/library rules, contracts/body claims, relevant soul spells and temporal policies. Then confer with GPT. Preserve rare Divine/Abyssal intervention without inventing numerical taint or a routine bypass.',
        'Continue all remaining spells and systems toward the full authored candidate. Do not claim runtime, human playtesting, balance or whole-game certification.',
        'Latest verified GitHub backup18c6e3a; later work local. Owner monitors usage and withdrew50percent cutoff.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'lengthLimit':info(limit),'handoff':info(handoff),'links':navigation['existingDistinctLinks'],'missingLinks':0,'newMechanicsAdopted':False}))

if __name__=='__main__':main()
