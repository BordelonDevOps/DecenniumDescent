"""Make the substantive local arc audit discoverable without promoting it."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_REVIEW_03.json'
    delta=A/'EPILOGUE_CAMPAIGN_ARCS_REVIEW_03_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-campaign-arcs-review-03'
    assert all(not p.exists() for p in [target,delta,preserved])
    state=read(previous)
    review=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_SEMANTIC_REVIEW_03.json'
    validation=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_03.json'
    prep=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_02_PREPARATION.json'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_02.zip'
    model=A/'cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json'
    cases=A/'cosmology-epilogue-campaign-arcs-local-draft-01/CASEBOOK.json'
    assert read(review)['issueCount']==15 and read(review)['openJointReviewIssues']==10
    assert read(validation)['failureCount']==0 and read(validation)['checkCount']==49
    assert read(validation)['model']==info(model) and read(validation)['casebook']==info(cases)
    assert read(prep)['archive']==info(archive)
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;pres.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    oldstart=originals[start].decode();oldline=next(x for x in oldstart.splitlines() if x.startswith('**Current joint review:**'))
    newline=oldline.replace('COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_PREPARATION.json','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_02_PREPARATION.json').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_REVIEW_03.json')
    newline=newline.replace('still unsubmitted and unadopted.','still unsubmitted and unadopted. [The local semantic audit](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_SEMANTIC_REVIEW_03.json) records five narrow proposal corrections and ten open questions, including voyage timing, payload, breathing defenses and annual contract states.')
    start.write_text(oldstart.replace(oldline,newline,1),encoding='utf-8',newline='\n')
    oldguide=originals[guide].decode();paragraphs=oldguide.split('\n\n');ops=[]
    oldrecovery=next(x for x in paragraphs if x.startswith('**Current recovery point:**'))
    newrecovery='**Current recovery point:** [Actual Part 3 completion is confirmed through the app](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_RECOVERY_RECEIPT.json). GPT reports a finished EPI-08–14 archive with 47 authored cases, 83 frozen sources and eight root files. Its exact archive is still unavailable locally; no independent hash, source or semantic check has run, and these rules remain unadopted. The [native export request is now visible as a user message](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_02.json), with no assistant reply and a system-error state. This is not a live generation to wait on. Chrome access still needs recovery or the original archive needs to be downloaded by the owner; do not resend the authoring request.'
    ops.append({'old':oldrecovery,'replacement':newrecovery})
    olddraft=next(x for x in paragraphs if x.startswith('The **current EPI-15–17 local draft'))
    newdraft='The **current EPI-15–17 proposal has 19 authored cases**. [Semantic review 03](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_SEMANTIC_REVIEW_03.json) identifies 15 issues: five have narrow local proposal corrections, and ten remain open for joint review. The current draft restores the original errant-equation cause and Mephistopheles envoy, proposes a mooring strong enough for the ship, ties release to the actual authorized work clock, and corrects a 24-hour case duration. The complete voyage still needs a physical load/Load ledger, support and hatch procedures, actual ancestry/class defenses and a full actor schedule. The annual contract still needs exact record and deadline states plus a substantive knowledge/choice review. [49 source/preservation/selected-arithmetic checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_03.json) pass, but **do not prove those unresolved procedures complete**. The earlier flight calculation omitted a canopy Action and must not be cited as a complete voyage clock. [Conference packet revision 02](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_02_PREPARATION.json) preserves all 41 frozen sources and is prepared, unsubmitted and unadopted. Earlier proposals and packet revision 01 remain intact.'
    ops.append({'old':olddraft,'replacement':newdraft})
    # Preserve the exact earlier guide while removing obsolete live-status narration from this current reader.
    obsolete=[x for x in paragraphs if x.startswith('The next **EPI-08–14 conference') or x.startswith('A [browser recovery record]') or x.startswith('The **three later arcs now have concrete local proposals**')]
    assert len(obsolete)==3
    for old in obsolete:ops.append({'old':old+'\n\n','replacement':''})
    history_note='Earlier submission, browser-recovery and 13-case drafting status is preserved in the [previous reader snapshot](../../../../../docs/audit/2026-10-08/full-game/navigation-before-epilogue-campaign-arcs-review-03/DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md) and linked checkpoints. Current status is stated above. The [original arc reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARC_READING_01.json), [relic/divination interface reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_DIVINATION_INTERFACE_READING_01.json) and [400-day calendar follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_CALENDAR_FOLLOWUP_01.json) remain available.\n\n'
    anchor='First, revised and integrated return archives remain immutable.'
    ops.append({'old':anchor,'replacement':history_note+anchor})
    text=oldguide
    for op in ops:
        assert text.count(op['old'])==1
        text=text.replace(op['old'],op['replacement'],1)
    guide.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [review,prep]);row['validationEvidence'].append(validation.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-campaign-arcs-semantic-review-03','recordedAtUtc':now,'sourceCount':41,'authoredCases':19,'semanticIssues':15,'locallyCorrectedProposalIssues':5,'openJointReviewIssues':10,'selectedPreservationChecks':49,'failures':0,'newRulesAdopted':False,'submittedToGpt':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==oldrow[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied/110 cases. GPT EPI08–14 completion confirmed/47 reported cases; exact archive unavailable and unreviewed. Native export user turn visible but no assistant reply/systemError. EPI15–17 semantic review03: 15 findings, five local proposal corrections, ten unresolved interfaces/design questions; 19 preserved cases, 49 narrow checks pass. Revision02 packet/41 sources prepared, unsubmitted and unadopted. Whole-game/runtime/human/balance/publication and campaign era remain open; spells419/429. Later work local.'
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_RELIC_NULL_NATIVE_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CAMPAIGN_ARCS_REVIEW_03_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('EPI15–17 — semantic review03; ten issues remain open',review.name),('EPI15–17 —49 narrow checks, not full procedural approval',validation.name),('EPI15–17 — prepared conference revision02',prep.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=ops;changes[1]['operations']=[{'old':oldline,'replacement':newline}];changes[2]['operations']=[{'aspectId':'DD-50','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1500:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Local semantic audit and five narrow proposal corrections only; no joint adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(recordedAtUtc=now,status='EPI08–14 completion known; exact archive transfer unavailable. Export request visible but no assistant reply.',nativeTransferStatus='systemError; user turn fb930b64-06e3-4a33-9f72-60037b465c97 visible with no assistant message',nativeExportRequestDelivered=True,nativeExportResponseReceived=False,nativeTransferLatestEvidence=info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_02.json'),generationConfirmedLiveNow=False,archiveRetrieved=False)
    state['cosmologyEpilogueCampaignArcsLocalDraft'].update(status='local semantic review03; successor proposal and conference revision02 prepared/unsubmitted/unadopted',model=info(model),casebook=info(cases),semanticReview=info(review),validation=info(validation),authoredCases=19,conferenceSourceCount=41,semanticIssues=15,locallyCorrectedProposalIssues=5,openJointReviewIssues=10,conferencePreparation=info(prep),conferencePacket=info(archive),newRulesAdopted=False)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
      'Check Downloads for the exact EPI08–14 return; owner has already been asked once. Expected70386bytes/SHA25624eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. Original completion is confirmed, not the file. Run the prepared83-source checker only once the file is available, then semantic review.',
      'The native export request is now actually visible as user turn fb930b64-06e3-4a33-9f72-60037b465c97, but no assistant reply and status systemError. Do not call it still generating or resend the EPI08 authoring task. If exact archive text export becomes possible, use at most12000characters per reply, below reader20000 cap.',
      'Current arc proposal revision03 preserves19case IDs and41sources; semantic audit records15findings, five narrow proposed corrections, ten open joint questions. Prepared archive is DD_Cosmology_Epilogue_Campaign_Arcs_02.zip, superseding01for submission only. Nothing submitted or adopted.',
      'Do not treat old flight31968seconds or old44checks as a complete voyage schedule. Resolve load/Load inventory, support, hatch/exposure, crew/boarding/unmooring and actual defenses together; then author the exact full clock. Contract annual-record/exit and deadline composition also need real joint decisions.',
      'Independent local work remains possible despite repeated joint-transfer failures; this turn made substantive semantic/source corrections. Do not mark the whole goal complete or blocked solely for the browser error. If later truly at an impasse with the same repeated blocker, follow the blocked audit threshold.',
      'All original and prior proposal bytes preserved. No epoch choice, identity merge, source deletion, runtime/human/balance/publication or whole-game approval. Ordinary spells419reviewed/429pending; latest verified GitHub18c6e3a, subsequent work local.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))
if __name__=='__main__':main()
