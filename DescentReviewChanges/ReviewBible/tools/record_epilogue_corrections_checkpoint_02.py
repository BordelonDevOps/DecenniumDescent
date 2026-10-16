"""Record the reviewed EPI revision and ER01-07 submission without adopting rules."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_02.json'
    delta=A/'EPILOGUE_CHARACTER_CORRECTIONS_02_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-character-corrections-02'
    receipt=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_02_SUBMISSION_RECEIPT.json'
    assert all(not p.exists() for p in [target,delta,preserved,receipt])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    audit=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_02.json'
    source_check=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_revised.json'
    assert read(source_check)['checkCount']==444 and read(source_check)['failureCount']==0
    assert len(read(audit)['issues'])==7
    dom=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_02_SUBMISSION_DOM.txt'
    s=dom.read_text('utf-8');assert 'Seven remaining correction groups ER01–ER07' in s and 'button "Stop"' in s
    archive=A/'DD_Cosmology_Epilogue_Character_01_Corrections_02.zip'
    revised=A/'DD_Cosmology_Epilogue_Character_01_Return_revised.zip'
    receipt.write_bytes(encoded({'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-CHARACTER-01-ER','status':'actual Part3 ER01–ER07 submission verified; integrated response pending at submission','browserId':'3','tabId':'125746265','conversationUrl':state['activeGptReview']['conversationUrl'],'correctionArchive':info(archive),'audit':info(audit),'sourceCheck':info(source_check),'dom':info(dom),'screenshot':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_02_SUBMISSION.png'),'correctionGroups':7,'allRevisedCasesRead':75,'newRulesAdopted':False,'sourceInformationDeleted':0}))
    scope='EPI-01–07 revised return reviewed:444source/file/location checks pass; full model/chapters/75cases/12EC dispositions read. Seven remaining semantic groups ER01–ER07 with concrete proposals sent to actual Part3, Chrome3/tab125746265. Integrated return pending; no EPI mechanics adopted. Research route current. EPI08–14 follow-up saved. Ordinary spells419/429; campaign frame/identities/fullgame/runtime/human/publication open. GitHub18c6e3a; later work local.'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The EPI-01–07 revision passes all [444 source checks](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_revised.json). Reading its full model, both chapters and 75 examples found [seven remaining correction groups](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_02.json), now [submitted with concrete proposals to actual Part 3](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_02_SUBMISSION_RECEIPT.json). **Integrated return pending; no epilogue mechanics adopted.** The jointly confirmed [Equation research route](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md) remains current. Continue from the [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_02.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame and unresolved identities remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode();old_para=next(v for v in old_guide.split('\n\n') if v.startswith('The EPI-01–07 first return is preserved'))
    new_para='The first and revised EPI-01–07 returns are preserved. The revision passes all [444 source/file/location checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_revised.json), restores source halving and the starting vow, preserves all 17 mask rows and exact blessing scopes, and contains 75 authored examples. Full semantic review found [seven remaining correction groups ER01–ER07](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_02.json): motif commitment/shared denial, preparation/time interactions, mask designation and old examples, complete challenge terminal states, finite Concord visits/return deadlines, usable prose and accurate dispositions. These are [submitted with concrete proposals to Part 3](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_02_SUBMISSION_RECEIPT.json). **Integrated response pending; no EPI mechanics adopted.** The live review now uses Chrome 3/tab 125746265, a fresh view of the same owner-created Part 3 conversation. The [EPI-08–14 reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json) and [weapon/bestiary/flora follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json) prepare the next conference without inventing recovered creature profiles or adding recipes. EPI-15–17 staging still depends on the campaign-frame question.'
    guide.write_text(old_guide.replace(old_para,new_para,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [audit,receipt]);row['validationEvidence'].append(source_check.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-character-corrections-02','recordedAtUtc':now,'sourceChecks':444,'sourceCheckFailures':0,'semanticCorrectionGroups':7,'reviewedCases':75,'priorReturnsPreserved':True,'correctionSubmission':receipt.relative_to(G).as_posix(),'newRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_CHARACTER_CORRECTIONS_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CHARACTER_CORRECTIONS_02_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('Epilogue ER01–ER07 — actual GPT integration request',receipt.name),('Epilogue revision — seven remaining semantic groups',audit.name),('Epilogue revision — 444 source checks pass',source_check.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(v)+',\n' for v in items),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_para,'replacement':new_para}];changes[1]['operations']=[{'old':line,'replacement':new_line}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification=state.get('goalTurnClassification','progress'),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},newRuleAdoptions=0,newRuleAdoptionScope='No epilogue mechanics adopted; revised return reviewed and remaining seven correction groups submitted. Earlier research route remains current.')
    state['activeGptReview'].update(recordedAtUtc=now,status='Revised return source checks pass; full semantic review found ER01–ER07; integrated response pending',reviewId='COSMOLOGY-EPILOGUE-CHARACTER-01-ER',tabId='125746265',attachmentDisplayName=archive.name,archive=info(archive),submission=info(receipt),responsePendingAtSubmission=True,verdictReceived=False,priorReturnReceived=True,revisedReturn=info(revised),revisedReturnSourceCheck=info(source_check),revisedReturnSemanticAudit=info(audit),newRulesAdopted=False)
    state['cosmologyEpilogueCharacterReview'].update(status='Revised return reviewed; seven semantic correction groups submitted; integrated response pending',revisedReturnArchive=info(revised),revisedReturnDom=info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_REVISED_RETURN_DOM.txt'),revisedSourceCheck=info(source_check),revisedSemanticAudit=info(audit),secondCorrectionSubmission=info(receipt),newRulesAdopted=False)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
      'Actual GPT Part3 Chrome3/tab125746265 is integrating ER01–ER07. Revalidate UI; do not resend/recreate. Old tab125746244 was unresponsive; the new tab is the same conversation and its revised return was downloaded successfully.',
      'When completed, download DD_Cosmology_Epilogue_Character_01_Return_Integrated.zip and run check_cosmology_epilogue_character_return_01.py with Downloads path and unique suffix integrated. Expect8files/same60source bindings, all75prior case IDs retained. Do not rerun existing revised extraction. Independently review full semantic changes before adoption.',
      'Review ER01ordinary commitment/shared denial/split ledger; ER02Transition actual work clocks and Balance state; ER03operative mask and stale cases; ER04challenge terminal states; ER05finite actual visit/exact8h return/return recheck; ER06complete prose; ER07accurate dispositions. Source checks alone do not certify these.',
      'EPI08–14 source reading and weapon/creature/flora follow-up are saved. Next conference requires actual finite relic/attunement/Null/flora/chamber profiles without promoting pending bestiary, changing687recipe count or inventing recovered geography.',
      'Keep original manuscript/owner precedence, pending campaign-frame answer, preserved87/710AE and unresolved identities. EPI15–17 staging remains open. Do not ask the same frame or continuation permission again.',
      'Goal remains active:419ordinary spells reviewed/429pending plus feats/bestiary/Director/fullgame integration. Latest verified GitHub18c6e3a; subsequent work local. No source deletion/runtime/human/balance/publication approval.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'submission':info(receipt),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
