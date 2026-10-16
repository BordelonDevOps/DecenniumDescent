"""Save actual notebook handoff and refresh navigation without adopting EPI rules."""
from copy import deepcopy
from datetime import datetime, timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_ROUTE_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_01.json'
    delta=A/'EPILOGUE_CHARACTER_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-epilogue-character-01'
    submission=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SUBMISSION_RECEIPT.json'
    assert all(not p.exists() for p in [target,delta,preserved,submission])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    prep=read(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json')
    dom=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SUBMISSION_DOM.txt';screen=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SUBMISSION.png';s=dom.read_text(encoding='utf-8')
    assert 'The chronology/research route is adopted locally' in s and prep['archive']['sha256'] in s and 'button "Stop"' in s
    submission.write_bytes(encoded({'recordedAtUtc':now,'reviewId':prep['reviewId'],'status':'actual Part3 submission verified; notebook independently matched archive size and hash','archive':prep['archive'],'sources':60,'allClassFiles':17,'sourceParagraphChecks':25,'dom':info(dom),'screenshot':info(screen),'sendClickReportedTimeout':True,'actualSubmissionVerifiedWithoutResending':True,'responsePendingAtSubmission':True,'newRulesAdopted':False,'sourceInformationDeleted':0}))
    source_check=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_01.json'
    returned=source_check.is_file()
    semantic=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_01.json'
    stage='returned; source checks saved; semantic review remains open' if returned else 'submitted; actual GPT is authoring the return'
    if semantic.is_file():stage='returned; source checks and first semantic findings saved; corrections remain open'
    scope=f'EPI-01–07 {stage}. Frozen60sources include all17class files and25exact original paragraphs; no EPI mechanics adopted. EPI-08–14 source/interface preparation saved. Research route remains jointly confirmed. Ordinary spells419reviewed429pending; epoch, identities, full-game/runtime/human/publication open. Latest verified GitHub18c6e3a; later work local.'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line=f'**Current joint review:** The character epilogue review, EPI-01–07, is **{stage}** in actual Calibration Review Part 3. The [source packet receipt](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json) records 60 frozen files, all 17 current class files and 25 exact original paragraphs. Vows, masks, seven Choir motifs, home-plane rewards, virtues, petitions and Sentinel encounters remain candidates until joint semantic review is complete. [Relics, chamber seeds and Null mechanics](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json) are prepared for the next conference. The [Equation research route](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md) remains jointly confirmed and locally adopted. Continue from the [current cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame and unresolved identities remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start_text=old_start.replace(line,new_line,1)
    spell_row=next(v for v in start_text.splitlines() if v.startswith('| Spells |'))
    spell_new='| Spells | All 848 ordinary identities remain indexed: **419 reviewed / 429 pending**, as recorded in the [current authored index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json). [The 44 original source cohorts](docs/audit/2026-10-08/full-game/PREPARED_SPELL_SOURCE_INDEX.md) and earlier cohort counts remain historical evidence. Refresh current interfaces before the next submission; ten ancestry-only spells remain separate. |'
    start_text=start_text.replace(spell_row,spell_new,1)
    push=read(G/'docs/audit/2026-10-15/github-snapshot-pantheons/PUSH_RECEIPT.json');assert push['commit']==push['verifiedRemoteCommit']=='18c6e3ae8b3c1d391dd91121693931657ae9c98f'
    delivery_row=next(v for v in start_text.splitlines() if v.startswith('| Final delivery |'))
    delivery_new='| Final delivery | [Latest progress backup verified](docs/audit/2026-10-15/github-snapshot-pantheons/PUSH_RECEIPT.json) at `18c6e3ae8b3c1d391dd91121693931657ae9c98f`: 19,172 selected source files verified; 113 changed delivery files committed; no tracked files deleted. Later work remains local. The [joint flow gate](docs/audit/2026-10-08/full-game/FINAL_FLOW_AND_GITHUB_DELIVERY.md) stays open. |'
    start_text=start_text.replace(delivery_row,delivery_new,1);start.write_text(start_text,encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode()
    paragraph=f'The [character epilogue conference](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_SUBMISSION_RECEIPT.json), EPI-01–07, is **{stage}** in Part 3. It supplies 60 frozen current sources, all 17 class files, 25 verified manuscript paragraphs and concrete interfaces for home-plane rewards, seven motifs, vows, masks, virtue/Conflict Die choices, petitions and Sentinel encounters. No EPI rule is adopted by submission or source-hash checking. The [next source reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json) preserves EPI-08–14 relics, twelve chamber seeds and Null/antidote mechanics. Their attunement, nonlethal damage, field exposure and mask/blessing interfaces remain to author. EPI-15–17 story staging still depends on the open campaign-frame question.'
    guide_text=old_guide.replace('First, revised and integrated return archives remain immutable.',paragraph+'\n\nFirst, revised and integrated return archives remain immutable.',1);assert guide_text!=old_guide
    guide.write_text(guide_text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    evidence=[submission,A/'COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json',A/'COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json']
    if returned:evidence.append(source_check)
    if semantic.is_file():evidence.append(semantic)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
    row['currentEvidenceAddenda'].append({'id':'epilogue-character-01','recordedAtUtc':now,'status':stage,'submission':submission.relative_to(G).as_posix(),'sourceFiles':60,'currentClassFiles':17,'originalParagraphs':25,'newRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    text=originals[nav].decode();tail=' + read(A / "CHRONOLOGY_ROUTE_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CHARACTER_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('Character epilogue EPI-01–07 — actual Part3 submission',submission.name),('Epilogue 60-source preparation', 'COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json'),('Relics chambers and Null — EPI-08–14 source reading','COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json')]
    if returned:items.append(('Character epilogue return — source integrity only',source_check.name))
    if semantic.is_file():items.append(('Character epilogue — semantic corrections pending',semantic.name))
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(item)+',\n' for item in items),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_guide,'replacement':guide_text}];changes[1]['operations']=[{'old':line,'replacement':new_line},{'old':spell_row,'replacement':spell_new},{'old':delivery_row,'replacement':delivery_new}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    prior_active=deepcopy(state['activeGptReview'])
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification=state.get('goalTurnClassification','progress'),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},newRuleAdoptions=0,newRuleAdoptionScope='This checkpoint submits and preserves epilogue proposals; no EPI mechanics adopted. Previously adopted route remains current.',newRuleAdoptionCountScope='New package adoptions in this checkpoint only; prior history preserved.')
    state['activeGptReview']={'recordedAtUtc':now,'reviewId':prep['reviewId'],'status':stage,'browserId':'3','tabId':'125746244','conversationUrl':prior_active['conversationUrl'],'conversationTitle':prior_active['conversationTitle'],'attachmentDisplayName':'DD_Cosmology_Epilogue_Character_01.zip','archive':prep['archive'],'submission':info(submission),'responsePendingAtSubmission':True,'verdictReceived':returned,'newRulesAdopted':False,'continuationApproval':'Owner-created Part3; ongoing collaboration authorized; no new-chat permission needed.'}
    state['cosmologyEpilogueCharacterReview']={'previousCompletedActiveReview':prior_active,'preparation':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json'),'submission':info(submission),'sourceCheck':info(source_check) if returned else None,'semanticAudit':info(semantic) if semantic.is_file() else None,'status':stage,'newRulesAdopted':False}
    state['cosmologyEpilogueRelicNullReading']=info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json')
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
      'Continue actual Part3 Chrome3/tab125746244. EPI01–07 is '+stage+'. Do not resend the original packet or recreate the chat. If response is still generating, wait while doing independent work.',
      'Download the exact EPI return once; verifier tools/check_cosmology_epilogue_character_return_01.py takes the Downloads archive path and optional suffix. It safely preserves the archive and checks all60frozen sources, output hashes and citations only. Then read full model/player/Director/cases and review semantic completeness before adoption.',
      'EPI01–07 must preserve all17mask classes,7motifs,7virtues including dualpairings, original9verse gap, real class/rest/resource/condition/KT/PT boundaries, finite blessings and Sentinel scenes. New mechanics remain proposals until joint semantic confirmation; source checks are not balance or runtime approval.',
      'EPI08–14 source reading and interface questions saved. Author relic attunement, finite12chambers, explicit Null nonlethal/death interactions and actual antidote ingredients/time/availability after character module interfaces settle. Current687recipes are not silently increased.',
      'Research route already jointly confirmed and adopted; do not resume superseded route corrections. Owner campaign-frame question remains unanswered; preserve87/710AE and unresolved identity gaps. EPI15–17 need careful staging.',
      'Continue remaining419reviewed/429pending ordinary spells and full-game work after current cosmology conferences. No deletion, no fullgame/human/runtime/publication approval. Latest verified GitHub18c6e3a; current additions local.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state));print(json.dumps({'checkpoint':info(target),'submission':info(submission),'stage':stage,'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
