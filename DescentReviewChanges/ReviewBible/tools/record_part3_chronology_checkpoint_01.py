"""Record the owner-created Part 3 continuation and source-bound chronology draft."""
from copy import deepcopy
from datetime import datetime, timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_RESEARCH_INTERFACE_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PART3_CHRONOLOGY_01.json'
    delta=A/'PART3_CHRONOLOGY_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-part3-chronology-01'
    receipt=A/'CALIBRATION_REVIEW_PART_3_SUBMISSION_RECEIPT_01.json'
    assert all(not p.exists() for p in [checkpoint,delta,preserved,receipt])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    draft=R/'data/director/cosmology/chronology_research_sites_draft_01.json'
    chapter=R/'docs/director-only/cosmology/CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md'
    citation=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_SITES_DRAFT_01_CHECK.json'
    c=read(citation);data=read(draft)
    assert c['draft']==info(draft) and c['chapter']==info(chapter)
    assert c['sourceBindingsVerified']==11 and c['exactEvidenceLocationsVerified']==173
    for row in data['sourceBindings']:assert info(G/row['path'])==row
    planes=A/'DD_Cosmology_Planes_01.zip'
    assert info(planes)['sha256']=='158630558c141a69485c47bdfb727c8f29d1727bca1e78c45f01ac3944bd8fe5'
    browser=A/'CALIBRATION_REVIEW_PART_3_BROWSER_RECEIPT_01.json';observed=read(browser)
    assert observed['ownerCreatedContinuation'] and observed['conversationUrl'].endswith('6ad1498d-f244-83ea-8ffe-63e75ff98073')
    dom=A/'CALIBRATION_REVIEW_PART_3_SUBMISSION_DOM_01.txt'
    assert 'ChatGPT is responding' in dom.read_text(encoding='utf-8')
    receipt.write_bytes(encoded({**observed,'archive':info(planes),'browserReceipt':info(browser),'submittedText':info(A/'CALIBRATION_REVIEW_PART_3_SUBMITTED_HANDOFF_01.txt'),'sentDom':info(dom),'visibleProof':info(A/'CALIBRATION_REVIEW_PART_3_SUBMISSION_01.png'),'priorPart2Submission':info(A/'COSMOLOGY_PLANES_01_SUBMISSION.json'),'priorPart2TerminalReceipt':info(A/'COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json'),'sourceInformationDeleted':0}))
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json'
    nav=R/'tools/build_review_map.py';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes();preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('The owner created Calibration Review Part 3, displayed as Calibration Review Continuation. The unchanged planes packet and handoff were submitted there once; GPT was responding at the recorded observation. Part 2 and Resolve Heartcell Origins remain preserved. '
           'Chronology/research-site draft now has 16 relative events, 9 site qualifications, 8 open issues and 8 discussion situations, checked against 173 exact locations in 11 sources. '
           'It preserves all dates and reuses the existing 17 epilogue rule IDs. Wax Library has a post-Infinite-Yield source frame with explicit original permission for independent adaptation; neither automatic starting availability nor an absolute earlier-era ban is adopted. '
           'The 87/710 AE date comparison is a conditional cadence tension, not a corrected date. Current campaign epoch, research-site placement, epilogue mechanics, public revelations, Equation and Hunt procedures still need joint discussion. '
           'Ordinary spells remain 419 reviewed/429 pending; latest verified GitHub backup is 18c6e3a, subsequent work local.')
    old_start=start.read_text(encoding='utf-8');old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** [Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) and the [Q6 endgame review](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md) are saved. The owner-created Part 3 chat has [received the unchanged planes packet and handoff](docs/audit/2026-10-08/full-game/CALIBRATION_REVIEW_PART_3_SUBMISSION_RECEIPT_01.json); GPT was responding at submission. Prepared for the next conference: [souls/Hunt](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md), [22-record library inventory](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EQUATION_LIBRARY_SOURCE_INVENTORY_01.md), [Equation Research procedure](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EQUATION_RESEARCH_INTERFACE_DRAFT_01.md), and [chronology/site comparison](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md). These drafts adopt no new rules or dates. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_PART3_CHRONOLOGY_01.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(old_line,new_line,1),encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8')
    old_sentence='GPT reached its conversation-length limit before returning a verdict; the packet and continuation handoff are preserved.'
    new_sentence='Part 2 reached its conversation-length limit before returning a verdict. The owner-created Part 3 continuation has now received the unchanged packet and preserved handoff; its [submission receipt](../../../../../docs/audit/2026-10-08/full-game/CALIBRATION_REVIEW_PART_3_SUBMISSION_RECEIPT_01.json) records GPT responding.'
    assert old_current.count(old_sentence)==1
    addition='\nThe [chronology and research-site comparison](CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md) preserves 16 relative events and all printed dates, qualifies 9 research sites, and carries 8 open questions with 8 discussion situations. Its 173 evidence locations are checked. Original epilogue portability does not automatically place the Wax Library in the starting era or adopt its rules. The current campaign epoch, Library placements and calendar reconciliation remain open. The existing 17 epilogue rule IDs are reused. Website findings are static-source observations, not a rendered publication test.\n'
    new_current=old_current.replace(old_sentence,new_sentence,1)+addition
    current.write_text(new_current,encoding='utf-8',newline='\n')
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-15','DD-46','DD-50','DD-61','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'part3-chronology-01','recordedAtUtc':now,'draft':draft.relative_to(G).as_posix(),'citationCheck':citation.relative_to(G).as_posix(),'planesSubmission':receipt.relative_to(G).as_posix(),'jointlyReviewed':False,'newRulesAdopted':False,'fullDomainClosed':False})
            row.setdefault('draftEvidence',[]).extend(p.relative_to(G).as_posix() for p in [draft,chapter])
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [citation,receipt])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['status','closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "EQUATION_RESEARCH_INTERFACE_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "PART3_CHRONOLOGY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    marker='    pending = [\n';assert text.count(marker)==1
    additions=[('Planes — resumed in owner-created Part 3; submission receipt',receipt.name),('Chronology and research sites — 173 source locations; joint review pending',citation.name)]
    text=text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in additions),1)
    text=text.replace('Planes — conversation-length limit; no verdict','Planes — historical Part 2 length-limit receipt').replace('Continuation — exact Part3 handoff','Continuation — preserved original Part 3 handoff')
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,ledger_path,nav]]
    changes[0]['operations']=[{'old':old_current,'replacement':new_current}]
    changes[1]['operations']=[{'old':old_line,'replacement':new_line}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    old_active=deepcopy(state['activeGptReview'])
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageLedger=info(ledger_path),coverageDelta=info(delta),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},cosmologyChronologyResearchSites={'status':'source-bound draft; joint discussion pending','draft':info(draft),'chapter':info(chapter),'citationCheck':info(citation),'relativeEvents':16,'siteQualifications':9,'exactEvidenceLocations':173,'newRulesOrDatesAdopted':False})
    state['activeGptReview']={'reviewId':'COSMOLOGY-PLANES-01','status':'resumed in owner-created Part 3; response running at submission observation','conversationTitle':observed['observedTitle'],'conversationUrl':observed['conversationUrl'],'tabId':observed['tabId'],'submission':info(receipt),'continuationApproval':'Owner explicitly created Part 3; continuation submitted','previousPart2Review':old_active,'verdictReceived':False}
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions']=[
        'Observe the existing Part 3 response in Chrome tab125746244 at the recorded URL; do not ask permission again or resend the packet. Verify the returned eight-file planes archive and substantive citations before applying.',
        'Then prepare the souls/Hunt conference using the 12-section20-case draft, original readings, authored-status correction, library inventory, Equation Research procedure, chronology/site comparison and verified planes outcome. Supply actual sources and separate reviewable proposals from source canon.',
        'Current campaign epoch, Equation research qualification/functional understanding, real library placement and clue design, chronology/calendar reconciliation and 17 preserved epilogue rule groups remain open for discussion.',
        'Ordinary spells419reviewed429pending. Preserve language benefits and borrowed proficiency. Soul Mirror already has reviewed-authored status. Do not adopt numerical taint, Hunt triggers/roster or exceptional intervention routes without joint development.',
        'Preserve Q6 crystal produces OR exposes wording, hidden Floor97 chamber and public failed-Sixth-Gate boundary. No full runtime/human balance/game-flow closure. Latest verified GitHub18c6e3a; later work local. Owner monitors usage.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'planesSubmission':info(receipt),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'planesPacketUnchanged':True,'approvalStatusesUnchanged':True,'newRulesAdopted':False}))

if __name__=='__main__':main()
