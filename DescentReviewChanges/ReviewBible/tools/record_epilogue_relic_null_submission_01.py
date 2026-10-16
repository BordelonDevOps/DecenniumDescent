"""Record the active EPI08-14 conference without adopting its pending contents."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_APPLICATION_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_SUBMISSION_01.json'
    delta=A/'EPILOGUE_RELIC_NULL_SUBMISSION_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-relic-null-submission-01'
    assert all(not p.exists() for p in [target,delta,preserved])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    receipt=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_SUBMISSION_RECEIPT.json'
    preparation=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_PREPARATION.json'
    arcs=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARC_READING_01.json'
    assert read(preparation)['sourceCount']==83 and read(preparation)['failureCount']==0
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    scope='EPI01–07 exact jointly confirmed module applied;110 authored cases. EPI08–14 four relics,12chambers,Null and4flora now with actual GPT Part3 Chrome3/tab125746268:83frozen sources/14original paragraph checks. Return pending; no EPI08–14 adoption. EPI15–17 source/transport reading saved; epoch remains unanswered.419/429ordinary spells; broader runtime/human/balance/fullgame/publication open. GitHub18c6e3a; later work local.'
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line=line.replace('Next: relics, twelve chamber seeds, residual Null and flora (EPI-08–14).','[EPI-08–14 is now with GPT](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_SUBMISSION_RECEIPT.json): four relics, twelve chamber seeds, residual Null and four plants, using 83 frozen source files. Return pending.').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CHARACTER_APPLICATION_01.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_SUBMISSION_01.json')
    assert new_line!=line
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode()
    anchor='First, revised and integrated return archives remain immutable.'
    paragraph='The next **EPI-08–14 conference is active in Part 3**. Its [verified submission](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_SUBMISSION_RECEIPT.json) contains 83 frozen sources and 14 original paragraph checks, and requests four relics, twelve complete chamber scenes, residual Null/life/purge rules, four plants and the antidote. Return pending; none of these rules is adopted yet. The [three later arc source readings](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARC_READING_01.json) preserve their beyond-epilogue condition, exact source context and real sky-vessel/contract/deadline dependencies. They also flag that P262’s thousand child pendants are not automatically Xi pendants or unlimited operative relics. No campaign placement or epoch has been chosen.\n\n'
    assert old_guide.count(anchor)==1
    guide.write_text(old_guide.replace(anchor,paragraph+anchor,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [receipt,arcs])
    row['validationEvidence'].append(preparation.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-relic-null-submission-01','recordedAtUtc':now,
        'sourceCount':83,'sourceParagraphChecks':14,'sourceFailures':0,'issues':7,'submission':receipt.relative_to(G).as_posix(),
        'newRulesAdopted':False,'fullDomainClosed':False,'sourceInformationDeleted':0})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_CHARACTER_APPLICATION_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_RELIC_NULL_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1;text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('EPI08–14 — actual Part3 authoring request',receipt.name),('EPI08–14 —83sources and14original paragraphs',preparation.name),('EPI15–17 — original arc and transport reading',arcs.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(v)+',\n' for v in items),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':anchor,'replacement':paragraph+anchor}]
    changes[1]['operations']=[{'old':line,'replacement':new_line}]
    changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,
        'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1500:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview']={'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-RELIC-NULL-01',
        'status':'EPI08–14 submitted; GPT authoring response pending','browserId':'3','tabId':'125746268',
        'conversationUrl':read(receipt)['conversationUrl'],'archive':info(A/'DD_Cosmology_Epilogue_Relic_Null_01.zip'),
        'submission':info(receipt),'responsePendingAtSubmission':True,'verdictReceived':False,'newRulesAdopted':False}
    state['cosmologyEpilogueRelicNullReview']={'status':'submitted;return pending','preparation':info(preparation),'submission':info(receipt),'newRulesAdopted':False}
    state['cosmologyEpilogueCampaignArcReading']=info(arcs)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
        'Actual GPT Part3 Chrome3/tab125746268 is authoring EPI08–14. Do not resend. Read final result; download DD_Cosmology_Epilogue_Relic_Null_01_Return.zip when ready.',
        'Run prepared check_cosmology_epilogue_relic_null_return_01.py with actual downloaded path and unique suffix01; exact8rootfiles/83sources. It has only been compiled, not run on a return yet. Then independently review all four relics,12scenes,Null/flora/model/prose/cases before adoption.',
        'Check sourceP262: Concord spear remelted into1000child pendants, distinct from Xi and not infinite active relic stock. EPI15–17 source/transport reading preserves this seam. Current EPI01–07 remains applied; no repeated closed LP review.',
        'Pay particular attention to Null damage ownership and fatality overrides, mask/petition purge extensions,finite ingredients/stock,plane/time landing and deadlines,full creature profiles and original afterInfiniteYield qualification.',
        'Campaign epoch unanswered; preserve all originals,87/710AE and identity gaps. EPI15–17 can be developed conditionally later without choosing frame. Fullgame/runtime/human/balance/publication remain open; latest GitHub18c6e3a.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'returnPending':True}))

if __name__=='__main__':main()
