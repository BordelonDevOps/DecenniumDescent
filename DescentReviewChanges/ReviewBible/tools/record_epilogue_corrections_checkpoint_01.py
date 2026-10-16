"""Preserve first EPI review findings and the actual correction submission."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_01.json'
    delta=A/'EPILOGUE_CHARACTER_CORRECTIONS_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-epilogue-character-corrections-01'
    receipt=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_SUBMISSION_RECEIPT.json'
    assert all(not p.exists() for p in [target,delta,preserved,receipt])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    audit=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_01.json';source_check=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_01.json';check=read(source_check)
    assert check['checkCount']==366 and check['failureCount']==1 and len(read(audit)['issues'])==12
    dom=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_SUBMISSION_DOM.txt';s=dom.read_text(encoding='utf-8')
    assert '12specific correction areas EC01–EC12' in s and 'button "Stop"' in s
    archive=A/'DD_Cosmology_Epilogue_Character_01_Corrections.zip'
    receipt.write_bytes(encoded({'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-CHARACTER-01-EC','status':'actual Part3 correction submission verified; revised response pending','correctionArchive':info(archive),'audit':info(audit),'sourceCheck':info(source_check),'dom':info(dom),'screenshot':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_SUBMISSION.png'),'correctionAreas':12,'additionalSourceFidelityPoint':'Original P283 starts every PC with one vow; may was incorrectly labeled kept. Restore source requirement within module or explicitly justify a new optional variant.','newRulesAdopted':False,'sourceInformationDeleted':0}))
    scope='EPI-01–07 first return reviewed: 365 of366source/file/location checks pass; one Bard citation fails. All17mask rows,7motifs,7blessings,7scene drafts and51cases read;12semantic correction areas sent to actual Part3. Revised return pending, no EPI mechanics adopted. EPI-08–14 source follow-up saved. Research route current. Ordinary spells419/429; epoch/identities/fullgame/runtime/human/publication open. GitHub18c6e3a; later work local.'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line='**Current joint review:** GPT returned the EPI-01–07 character epilogue draft. The [source check](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_01.json) found 365 passing checks and one broken Bard citation. Review of all 17 mask rows, seven motifs, seven blessings, seven scene drafts and 51 cases found [twelve correction areas](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_01.json), now [submitted to actual Part 3](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_SUBMISSION_RECEIPT.json). **Revised return pending; no epilogue mechanics adopted.** The jointly confirmed [Equation research route](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md) remains current. Continue from the [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame and unresolved identities remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode();old_para=next(v for v in old_guide.split('\n\n') if v.startswith('The [character epilogue conference]'))
    new_para='The EPI-01–07 first return is preserved, with all 17 class mask rows, seven motifs, seven virtue pairings/blessings, seven scene drafts and 51 authored cases. Its [source check](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_01.json) has 365 passing checks and one invalid Bard JSON Pointer. Full local review found [twelve correction areas](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_01.json): source halving, usable motif timing/payment, prepared loadouts, permanent Warrior key, wearer-wide mask charge and clocks, shared state, exact blessing scope, complete challenges, valid lamp logic, finite planar-step procedures and worked arithmetic. They are [submitted to actual Part 3](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_CORRECTIONS_SUBMISSION_RECEIPT.json); the revised return is pending. **No EPI mechanics are adopted.** The [EPI-08–14 reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json) and [weapon/bestiary/flora follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json) prepare the next conference without inventing recovered creature profiles or adding recipes. EPI-15–17 staging still depends on the campaign-frame question.'
    guide_text=old_guide.replace(old_para,new_para,1);guide.write_text(guide_text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [audit,receipt,A/'COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json']);row['validationEvidence'].append(source_check.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-character-corrections-01','recordedAtUtc':now,'sourceChecks':366,'sourceCheckFailures':1,'semanticCorrectionAreas':12,'firstReturnPreserved':True,'correctionSubmission':receipt.relative_to(G).as_posix(),'newRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_CHARACTER_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CHARACTER_CORRECTIONS_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('Epilogue EC01–EC12 — actual GPT correction submission',receipt.name),('Epilogue first return — semantic corrections required',audit.name),('Epilogue first return — source integrity check',source_check.name),('Relic weapon and creature source follow-up','COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json')]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(v)+',\n' for v in items),1);compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_para,'replacement':new_para}];changes[1]['operations']=[{'old':line,'replacement':new_line}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification=state.get('goalTurnClassification','progress'),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},newRuleAdoptions=0,newRuleAdoptionScope='No epilogue mechanics adopted; first return preserved and corrections submitted. Earlier research route remains current.')
    state['activeGptReview'].update(recordedAtUtc=now,status='First return received/reviewed; EC01–EC12 corrections submitted and revised return actively pending',reviewId='COSMOLOGY-EPILOGUE-CHARACTER-01-EC',attachmentDisplayName=archive.name,archive=info(archive),submission=info(receipt),responsePendingAtSubmission=True,verdictReceived=False,priorReturnReceived=True,firstReturnSourceCheck=info(source_check),firstReturnSemanticAudit=info(audit),newRulesAdopted=False)
    state['cosmologyEpilogueCharacterReview'].update(status='First return requires corrections; revised response pending in actual Part3',firstReturnArchive=info(A/'DD_Cosmology_Epilogue_Character_01_Return_01.zip'),firstReturnDom=info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_DOM.txt'),sourceCheck=info(source_check),semanticAudit=info(audit),correctionSubmission=info(receipt),newRulesAdopted=False)
    state['cosmologyEpilogueRelicSourceFollowup']=info(A/'COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json');state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
      'Actual GPT Part3 Chrome3/tab125746244 is revising EPI01–07 in response to EC01–EC12. Revalidate live UI. Do not resend original packet/corrections or recreate the chat. First return is preserved and NOT adopted.',
      'Download DD_Cosmology_Epilogue_Character_01_Return_Revised.zip when complete. Run check_cosmology_epilogue_character_return_01.py with Downloads path and suffix revised. Expect8files and same60source hashes; valid source pointers. Preserve all prior archives. Then separately review full revised model/chapters/cases and all12correction dispositions before adoption.',
      'Review EC02source50%halving, EC04Sorrow/Law timing/payment/attack break, EC05actual preparation, EC06Warrior permanent key/wearer charge/no clock rebasing, EC08full card envelopes, EC09all7executable scenes, EC10valid puzzle and EC11actual interlude travel especially closely. All51old case IDs must remain; new substantive examples needed. No broad acceptance from counts alone.',
      'EPI08–14 source reading/follow-up saved: actualV6Finesse/Heavy/Thrown/Versatile and mundaneSpear records; named SilenceWraith/EchoDoppelganger/Nullflora not found in inspected current bestiary/Alchemy/Herbalism or3books by exact names. New full profiles/finite flora procedures remain required, not generic approvals. Keep687recipe count and pending bestiary status.',
      'Current jointly confirmed research route remains adopted. Campaign-frame owner question remains unanswered;87/710AE and unresolved identities preserved. EPI15–17 narrative staging remains open.',
      'Full objective remains active:419ordinary spells reviewed/429pending plus feats/bestiary/Director/wholegame interfaces. No sources deleted. Latest verified GitHub18c6e3a; later work local. Runtime/human/balance/publication not approved.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'submission':info(receipt),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
