"""Record actual repair submission and retain the full development checkpoint."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, re, subprocess, sys
from pathlib import Path
from apply_di7_ap_as_01 import G,R,A,info,encoded,digest

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DE4_CURRENT_AUDIT_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_REPAIR_04_SUBMITTED.json'
    delta=A/'AC6_REPAIR_04_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-ac6-repair-04'
    receipt=A/'AC6_REPAIR_04_SUBMISSION_RECEIPT.json'
    assert not any(p.exists() for p in [checkpoint,delta,keep,receipt])
    native=A/'AC6_REPAIR_04_SUBMITTED_NATIVE.json'; d=read(native)
    turn=d['turns'][0]; assert turn['id']=='25a53b00-c57c-432c-8717-0484b1576465'
    item=next(x for x in turn['items'] if x['type']=='userMessage')
    submitted='\n'.join(c['text'] for c in item['content'] if c['type']=='text').split('\n\n[User attached')[0]
    request=(A/'AC6_REPAIR_04_REQUEST.txt').read_text(encoding='utf8')
    assert submitted.rstrip('\n')==request.rstrip('\n')
    attachment=next(x for x in d['attachments'] if x['name']=='DD_AC6_Repair_04.zip')
    archive=A/'DD_AC6_Repair_04.zip'; assert Path(attachment['path']).read_bytes()==archive.read_bytes()
    live=A/'AC6_REPAIR_04_SUBMITTED_BROWSER.txt'; assert 'button "Stop"' in live.read_text(encoding='utf8')
    structural=A/'AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json'; assert read(structural)['failureCount']==0
    semantic=A/'AC6_LOCAL_SUBSTANTIVE_REPAIR_04.json'; assert len(read(semantic)['issues'])==6
    receipt.write_bytes(encoded({'id':'AC6-REPAIR-04-ACTUAL-SUBMISSION','recordedAtUtc':now,'threadId':d['thread']['id'],'title':d['thread']['title'],'userTurnId':turn['id'],'archive':info(archive),'request':info(A/'AC6_REPAIR_04_REQUEST.txt'),'nativeEvidence':info(native),'browserEvidence':info(live),'screenshot':info(A/'PART4_AC6_REPAIR_04_SUBMITTED.png'),'uploadedArchiveBytesMatch':True,'exactRequestMatches':submitted==request,'requestMatchesAfterTerminalNewlineNormalization':True,'status':'Submitted once; browser shows active generation. Native user-only completed/idle record is not evidence of assistant completion.','newSpellAdoptions':0}))
    start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    saved=[];raw={}
    for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);raw[p]=b
        saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=raw[start].decode();assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    replacement='**Current GPT conference:** The [rank-six return03](docs/audit/2026-10-08/full-game/DD_AC6_Full_Review_03_Return.zip) is preserved and passed [725 independent structural/preservation checks](docs/audit/2026-10-08/full-game/AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json), including all 103 frozen sources, 14 identities, 16 placements and original histories. [Six substantive findings](docs/audit/2026-10-08/full-game/AC6_LOCAL_SUBSTANTIVE_REPAIR_04.json) still prevent acceptance: missing current Nexus mode procedures, conflicting Army statistics, inconsistent portal clocks, superseded current clauses, incomplete scenario coverage and airborne suppression behavior. The [complete correction packet](docs/audit/2026-10-08/full-game/DD_AC6_Repair_04.zip) is [submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC6_REPAIR_04_SUBMISSION_RECEIPT.json). GPT is preparing its response. No AC6 spell is adopted yet.\n\n'
    text,n=re.subn(r'\*\*Current GPT conference:\*\*.*?\n\n',lambda m:replacement,text,count=1,flags=re.S);assert n==1
    replacement='**Next fifteen-spell group:** The [Divination/Enchantment rank-four current draft](DescentReviewChanges/ReviewBible/data/director/spell_proposals/divination_enchantment_rank4_current_02.json) now contains 15 procedures and 30 new worked examples, preserving 30 original texts and binding 72 sources. [220 preservation/mapping/reference checks](docs/audit/2026-10-08/full-game/DE4_CURRENT_PROCEDURES_CHECK_02.json) passed; [four local semantic corrections](docs/audit/2026-10-08/full-game/DE4_CURRENT_DRAFT_02_SEMANTIC_NOTES.json) remain before submission. The [source/interface audit](docs/audit/2026-10-08/full-game/DE4_CURRENT_SOURCE_INTERFACE_AUDIT_01.json) and [nine-file Fate Reversal guard proposal](docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json) remain preserved. This group and its guard amendment are unsent and unadopted; repair the examples and finite control expiry, then refresh any accepted AC6 dependencies before joint review.\n\n'
    text,n=re.subn(r'\*\*Next fifteen-spell group:\*\*.*?\n\n',lambda m:replacement,text,count=1,flags=re.S);assert n==1
    start.write_text(text,encoding='utf8',newline='\n')
    cov=json.loads(raw[ledger]);prior=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [structural,semantic,receipt,A/'DE4_CURRENT_PROCEDURES_CHECK_02.json',A/'DE4_CURRENT_DRAFT_02_SEMANTIC_NOTES.json'])
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac6-repair-04-submitted','recordedAtUtc':now,'status':'Return03 structurally preserved; six substantive findings sent to actual GPT for repair. DE4 draft02 has15 procedures30 examples and four remaining local semantic corrections. No adoption.','checks':725,'failures':0,'newRuleAdoptions':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in prior['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=raw[builder].decode();tail=' + read(A / "DE4_CURRENT_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC6_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n',1)
    rows=[('AC6 — return03 independent preservation check',structural.name),('AC6 — six substantive repair findings',semantic.name),('AC6 — actual repair04 submission',receipt.name),('DE4 — current15 procedures/30 examples checks','DE4_CURRENT_PROCEDURES_CHECK_02.json'),('DE4 — four remaining local semantic corrections','DE4_CURRENT_DRAFT_02_SEMANTIC_NOTES.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(row)+',\n' for row in rows),1)
    scope='451 reviewed /397 pending ordinary spells;175 complete standalone procedures. AC5 accepted/applied. AC6 return03 preserved with725 structural checks passed; six substantive issues sent to actual GPT Part4 as repair04. DE4 draft02 has15 procedures30 new examples72 sources; four semantic corrections remain unsent/unadopted. All75 development areas and final whole-game flow remain in scope.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous)
    oldreview=deepcopy(state['activeGptReview']);oldreview.update(status='Completed return03 downloaded/preserved; independent structural checks pass, six semantic findings require repair. Unadopted.',returnReceived=True,generationConfirmedLiveAtObservation=False,returnedArchive=info(A/'DD_AC6_Full_Review_03_Return.zip'),structuralCheck=info(structural),semanticFindings=info(semantic))
    state.setdefault('priorGptReviews',[]).append(oldreview)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress: DE4 current procedures/examples authored and AC6 return03 preserved',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Return03 independently reviewed; repair04 submitted. No ordinary spell membership or current accepted rule changed.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview']={**state['activeGptReview'],'reviewId':'AC6-REPAIR-04','submission':info(receipt),'userTurnId':turn['id'],'status':'Actual repair04 sent once; browser confirms live assistant generation. Await the same submission, do not resend/restart for a timeout.','generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC6_Repair_04_Return.zip','returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(live)}
    state['de4CurrentPreparation'].update(currentDraft=info(R/'data/director/spell_proposals/divination_enchantment_rank4_current_02.json'),currentDraftCheck=info(A/'DE4_CURRENT_PROCEDURES_CHECK_02.json'),remainingLocalSemanticCorrections=info(A/'DE4_CURRENT_DRAFT_02_SEMANTIC_NOTES.json'),currentProcedureCount=15,newWorkedExamples=30,currentDraftSourceCount=72,status='Current draft02 authored, unsent/unadopted. Repair four known semantic issues: Portal caster formation compatibility, DominatePerson concentration/replacement distinction, actual Dispel3RP example, finite missing-phase Compulsion expiry. Then refresh accepted AC6 dependencies and jointly review.')
    state['safeNextActions']=[
      'Continue SAME Part4 repair04 user turn25a53b00-c57c-432c-8717-0484b1576465. Current tab125746324. Do not resend or restart due timeouts; native user-only idle/completed is not terminal assistant evidence.',
      'When DD_AC6_Repair_04_Return.zip arrives, preserve exact bytes and review all six AC6-L04 findings, both complete current Nexus modes, consistent Army profile, 60/600 clocks, clean operative suppression/panel rules, all prior51 scenario obligations plus4 added cases, real Hover/Falling choice and Chain Arc geometry. Recheck sources/pointers/full chapters and remaining semantics before exact acceptance.',
      'DE4 current02 is complete draft text, not accepted:15 procedures30 examples72 sources. Correct four recorded semantic issues. Nine-file three-spell Fate guard remains an explicit unadopted proposal; preserve historical records and refresh current feat bindings only after actual joint approval.',
      'All16 AC5 procedures are applied; do not rerun application. Current451 reviewed397 pending,175 standalone procedures. Source catalog unchanged.',
      'Continue the full75-area objective, remaining spells/environment/consumables/disease/feats/bestiary/Director/packaging/companion interfaces and final actual GPT whole-game flow. Latest verified GitHub backup18c6e3a predates this local work.'
    ]
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Independently verified actual AC6 return03, identified six substantive defects, preserved evidence and submitted repair04 to actual GPT. No adoption/closure claim.','evidence':info(semantic),'activeReviewObservation':info(live)}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'newSpellAdoptions':0,'currentOrdinarySpells':state['currentOrdinarySpellCounts'],'activeReviewUserTurn':turn['id']}))

if __name__=='__main__': main()
