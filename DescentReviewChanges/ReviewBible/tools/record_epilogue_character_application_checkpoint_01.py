"""Advance navigation to the jointly confirmed EPI01-07 module, preserving history."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_CORRECTIONS_02.json'
    target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_APPLICATION_01.json'
    delta = A/'EPILOGUE_CHARACTER_APPLICATION_01_NAVIGATION_DELTA.json'
    preserved = A/'navigation-before-epilogue-character-application-01'
    receipt = A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_CONFERENCE_RECEIPT.json'
    assert all(not p.exists() for p in [target, delta, preserved, receipt])
    now = datetime.now(timezone.utc).isoformat()
    state = read(previous)
    application = A/'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json'
    assert read(application)['newProvisionalModuleAdopted'] and read(application)['failureCount'] == 0
    confirmation = A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_CONFIRMATION_DOM.txt'
    archive = A/'DD_Cosmology_Epilogue_Character_01_Local_Patch_01.zip'
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'LP01–LP10 all confirmed by actual GPT Part3; exact candidate locally applied',
        'conversationUrl':state['activeGptReview']['conversationUrl'],'browserId':'3','tabId':'125746268',
        'submittedArchive':info(archive),'submissionDom':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_SUBMISSION_DOM.txt'),
        'submissionScreenshot':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_SUBMISSION.png'),
        'confirmationDom':info(confirmation),'confirmationScreenshot':'Capture timed out; final DOM verdict saved and read. No screenshot claimed.',
        'application':info(application),'confirmedGroups':10,'authoredCases':110,'newProvisionalModuleAdopted':True,
        'sourceInformationDeleted':0,'wholeGameApproved':False}))
    scope = 'EPI01–07 exact local candidate jointly confirmed and applied:444 inherited source/location checks,11 local package/preservation checks,6 application checks pass;110 authored cases, no runtime/human runs. Next EPI08–14 relics/chambers/Null/flora. Epoch/identities/fullgame/balance/publication remain open;419/429 ordinary spells. GitHub18c6e3a; later work local.'
    start = G/'START_HERE.md'
    guide = R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'
    originals = {}; pres = []
    for p in [start, guide, nav, ledger, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes(); dest = preserved/p.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(raw)
        originals[p] = raw; pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start = originals[start].decode()
    line = next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line = '**Current joint review:** GPT and Codex confirmed the EPI-01–07 character module, now applied as **NEW provisional playtest authorship**: [player rules](DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md), [Director rules](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EPILOGUE_CHARACTER_REVIEWED_01.md), and [application evidence](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json). All 110 authored examples and earlier returns are preserved. Next: relics, twelve chamber seeds, residual Null and flora (EPI-08–14). Continue from the [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_APPLICATION_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame, identities, runtime, human playtesting, balance and whole-game flow remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide = originals[guide].decode()
    old_para = next(v for v in old_guide.split('\n\n') if v.startswith('The first and revised EPI-01–07 returns are preserved.'))
    new_para = 'The **EPI-01–07 character module is now jointly confirmed and locally applied** as NEW provisional playtest authorship. Use its [player rules](../../mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md), [Director rules](EPILOGUE_CHARACTER_REVIEWED_01.md), [complete model](../../../data/director/cosmology/epilogue_character_reviewed_01.json) and [110 authored cases](../../../data/director/cosmology/epilogue_character_cases_01.json). Actual Part 3 confirmed all ten local patch groups and both exact hashes; the [application receipt](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json) records 444 inherited source/location checks, 11 local package/preservation checks and six application checks, with zero failures. These are not runtime or human tests. The module supplies affiliations, seven motifs, personal vows, all 17 class mask keys, Conflict Die, petitions, seven virtue challenges, four finite Concord visitor rooms and finite Sentinel information. All first/revised/integrated returns and all 107 prior case IDs remain preserved. The live review is the same Part 3 conversation in Chrome 3/tab 125746268. Next are the [EPI-08–14 source reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json), [weapon/creature/flora follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json) and [Null/life-resolution follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_NULL_LIFE_SOURCE_FOLLOWUP_01.json). Those groups remain unadopted. EPI-15–17 staging still depends on the unanswered campaign-frame choice.'
    guide.write_text(old_guide.replace(old_para,new_para,1),encoding='utf-8',newline='\n')
    coverage = json.loads(originals[ledger]); before = deepcopy(coverage)
    row = next(v for v in coverage['aspects'] if v['id']=='DD-50'); before_row = deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [receipt,confirmation])
    row['validationEvidence'].append(application.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-character-application-01','recordedAtUtc':now,
        'sourceChecks':444,'localPackageChecks':11,'applicationChecks':6,'failures':0,
        'authoredCases':110,'confirmedGroups':10,'application':application.relative_to(G).as_posix(),
        'newProvisionalModuleAdopted':True,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']: assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    text = originals[nav].decode()
    tail = ' + read(A / "EPILOGUE_CHARACTER_CORRECTIONS_02_NAVIGATION_DELTA.json")["changes"]\n'
    assert text.count(tail)==1
    text = text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CHARACTER_APPLICATION_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes = [v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1
    text = text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items = [('EPI01–07 — exact candidate jointly confirmed and applied',application.name),
        ('EPI01–07 — actual Part3 confirmation',receipt.name),
        ('Null life-resolution source follow-up','COSMOLOGY_EPILOGUE_NULL_LIFE_SOURCE_FOLLOWUP_01.json')]
    text = text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(v)+',\n' for v in items),1)
    featured = [('Current epilogue character player rules', 'DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md'),
        ('Current epilogue character Director rules','DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EPILOGUE_CHARACTER_REVIEWED_01.md'),
        ('Current epilogue complete model','DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_character_reviewed_01.json'),
        ('Current epilogue110 authored cases','DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_character_cases_01.json')]
    assert text.count('    featured = [\n')==1
    text = text.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(v)+',\n' for v in featured),1)
    compile(text,str(nav),'exec'); nav.write_text(text,encoding='utf-8',newline='\n')
    changes = [{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_para,'replacement':new_para}]
    changes[1]['operations']=[{'old':line,'replacement':new_line}]
    changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,
        'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newProvisionalModuleAdopted':True}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout[-1500:]); print(run.stderr[-3000:]); raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',
        previousGoalTurnClassification=state.get('goalTurnClassification','progress'),status=scope,
        coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=1,newRuleAdoptionScope='Exact jointly confirmed EPI01–07 NEW provisional authored module; all broader approval gates unchanged.')
    state['activeGptReview'].update(recordedAtUtc=now,status='LP01–LP10 confirmed; EPI01–07 exact candidate applied',
        reviewId='COSMOLOGY-EPILOGUE-CHARACTER-01-LP',tabId='125746268',archive=info(archive),
        submission=info(receipt),responsePendingAtSubmission=False,verdictReceived=True,newRulesAdopted=True,
        confirmation=info(confirmation),application=info(application))
    state['cosmologyEpilogueCharacterReview'].update(status='Exact jointly confirmed provisional module locally adopted',
        integratedReturnArchive=info(A/'DD_Cosmology_Epilogue_Character_01_Return_integrated.zip'),
        localPatch=info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01.json'),
        confirmation=info(confirmation),application=info(application),authoredCases=110,newRulesAdopted=True)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
        'EPI01–07 exact candidate is applied. Do not repeat closed EC/ER/LP corrections or resend that patch. Actual Part3 remains Chrome3/tab125746268.',
        'Prepare and send EPI08–14 using original source inventory, current module, relic/weapon/flora and Null life follow-ups. Require finite actual relic profiles,12chambers,Null exposure/purge and flora/antidote rules. Label all missing operational details NEW.',
        'Preserve after Infinite Yield qualification for12chamber seeds; do not silently choose pending owner frame, edit87/710AE or merge hidden identities.',
        'Fullgame remains active:419ordinary spells reviewed/429pending, feats/bestiary/Director/integration and EPI15–17 staging remain. No runtime/human/balance/publication approval or source deletion.',
        'Latest verified GitHub backup18c6e3a; subsequent cosmology work remains local.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'conference':info(receipt),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0}))

if __name__=='__main__': main()
