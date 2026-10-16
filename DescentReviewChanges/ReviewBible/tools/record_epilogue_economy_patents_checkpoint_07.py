"""Index the current unadopted arc proposal and exact failed-transfer evidence."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CONTRACT_ATMOSPHERE_06.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ECONOMY_PATENTS_07.json'
    delta=A/'EPILOGUE_ECONOMY_PATENTS_07_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-economy-patents-07'
    assert all(not p.exists() for p in [target,delta,preserved])
    state=read(previous)
    economy=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ECONOMY_PATENTS_07.json'
    scenes=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_SCENE_BOUNDARIES_07A.json'
    prep=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_05_PREPARATION.json'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_05.zip'
    transfer=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_03.json'
    model=A/'cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json'; cases=model.with_name('CASEBOOK.json')
    assert read(scenes)['model']==info(model) and read(scenes)['casebook']==info(cases) and read(cases)['count']==67
    assert read(economy)['failureCount']==read(scenes)['failureCount']==0 and read(prep)['archive']==info(archive)
    evidence=read(transfer)
    assert evidence['thread']['status']['type']=='systemError'
    assert evidence['turns'][0]['id']=='c702b47c-d99f-4665-8b5e-bad2f4143f60'
    assert all(x['type']=='userMessage' for t in evidence['turns'] for x in t['items'])
    start=G/'START_HERE.md'; guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py'; ledger=R/'data/playtest/game_development_coverage.json'
    originals={}; saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes(); dest=preserved/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
        originals[p]=raw; saved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    oldstart=originals[start].decode(); oldline=next(x for x in oldstart.splitlines() if x.startswith('**Current joint review:**'))
    newline=oldline.replace('have 51 authored situations','have 67 authored situations').replace('prepared 43-source conference packet','prepared 44-source conference packet').replace('COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_04_PREPARATION.json','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_05_PREPARATION.json').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CONTRACT_ATMOSPHERE_06.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ECONOMY_PATENTS_07.json')
    oldphrase='These still need joint review; payment custody and substantive patent choices still need development.'
    replacement='The [finite payment and patent scene proposal](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ECONOMY_PATENTS_07.json) now supplies real reward custody, useful engineering diagrams and a consequential choice over access to their copies. [Scene clarification](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_SCENE_BOUNDARIES_07A.json) restores the original flickering-out hook and actual hostile initiative. All these local proposals still need joint review.'
    assert oldphrase in newline and 'have 67 authored situations' in newline
    newline=newline.replace(oldphrase,replacement,1); start.write_text(oldstart.replace(oldline,newline,1),encoding='utf-8',newline='\n')
    oldguide=originals[guide].decode(); oldparagraph=next(x for x in oldguide.split('\n\n') if x.startswith('The **current EPI-15–17 local proposal'))
    paragraph='The **current EPI-15–17 local proposal has 67 authored cases**, with all earlier IDs and versions preserved. The existing voyage, annual contract and atmosphere proposals remain available in the current packet. [Economy/patents07](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ECONOMY_PATENTS_07.json) supplies five separate finite money pools, actual crew wages and scrap custody, three useful Canian engineering procedures and a working proof press. The refusal scene now allocates the first actual copy set between public reading, guild inspection or an agreed shared arrangement; its ACCEPT token does not sign the annual contract. [Scene boundaries07A](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_SCENE_BOUNDARIES_07A.json) restores the exact flickering-out source premise, requires actual initiative before lens manipulation and distinguishes a leaking seal from misrouted coolant. The 54 and 7 checks cover preservation and selected stock/time arithmetic; they are not gameplay runs. The ordinary voyage remains **8h55m**, with **117m48s fuel / 185m air** in its stated powered-idle example. Annual contract state and atmosphere procedures remain unchanged by these passes. The [44-source revision05 packet](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_05_PREPARATION.json) is **prepared, unsubmitted and unadopted**. The [latest actual GPT transfer record](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_03.json) confirms both recovery prompts have no assistant reply and the chat reports a system error. Exact EPI-08–14 recovery/integration, joint semantic review, final Player/Director prose and the owner campaign era remain open.'
    guide.write_text(oldguide.replace(oldparagraph,paragraph,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]); before=deepcopy(coverage)
    row=next(x for x in coverage['aspects'] if x['id']=='DD-50'); oldrow=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [economy,scenes,prep,transfer])
    row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [economy,scenes])
    row['currentEvidenceAddenda'].append({'id':'epilogue-economy-patents07-scenes07a-local-proposals','recordedAtUtc':now,'sourceCount':44,'authoredCases':67,'newCases':16,'economyPatentsChecks':54,'sceneBoundaryChecks':7,'checkCountsOverlap':True,'failures':0,'newRulesAdopted':False,'submittedToGpt':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==oldrow[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied/110cases. GPT EPI08–14 reported47cases; exact archive unavailable/unreviewed. Both export prompts have no assistant reply/systemError, including retry c702b47c. EPI15–17 now67 local cases: voyage04/geometry04A, annual contract05, atmosphere06, finite economy/patents07 and scene boundaries07A. Real copy-allocation scene and technical knowledge drafted;44-source packet05 prepared/unsubmitted/unadopted. Joint semantics, EPI08 integration, final prose, campaign era, runtime/human/balance/full-game/publication remain open. Ordinary spells419 reviewed/429 pending. Later work local.'
    code=originals[nav].decode(); tail=' + read(A / "EPILOGUE_CONTRACT_ATMOSPHERE_06_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1; code=code.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_ECONOMY_PATENTS_07_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']; assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('EPI15–17 — finite rewards and patent-choice scene07',economy.name),('EPI15/17 — source wording, initiative and pressure07A',scenes.name),('EPI15–17 — prepared revision05,44 sources/67 cases',prep.name),('EPI08–14 — actual failed export retry evidence',transfer.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec'); nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':oldparagraph,'replacement':paragraph}]
    changes[1]['operations']=[{'old':oldline,'replacement':newline}]
    changes[2]['operations']=[{'aspectId':'DD-50','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    result=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if result.returncode: print(result.stdout[-1500:]); print(result.stderr[-3000:]); raise SystemExit(result.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Local economy/patent/scene proposals only; actual joint adoption remains pending.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['cosmologyEpilogueCampaignArcsLocalDraft'].update(status='local voyage04/geometry04A/contract05/atmosphere06/economy-patents07/scenes07A; packet05 prepared, unsubmitted, unadopted',model=info(model),casebook=info(cases),economyPatents=info(economy),sceneBoundaries=info(scenes),authoredCases=67,conferenceSourceCount=44,conferencePreparation=info(prep),conferencePacket=info(archive),newRulesAdopted=False)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['latestActualGptTransferEvidence']=info(transfer)
    state['safeNextActions']=[
        'Actual GPT chat Calibration Review Continuation (owner part3), ID6ad1498d-f244-83ea-8ffe-63e75ff98073: latest smaller export retry c702b47c-d99f-4665-8b5e-bad2f4143f60 was delivered but has no assistant response; systemError. Do not resend completed EPI08–14 authorship or assume live generation. A recovery should retrieve exact existing bytes, not regenerate them.',
        'Expected EPI08–14 archive: DD_Cosmology_Epilogue_Relic_Null_01_Return.zip,70386bytes,SHA25624eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. If actual bytes become available, run the prepared83-source return verifier, then semantic review of47reported cases and cross-module interfaces. Native read_thread allows at most20000chars/item; the pending retry asked for12000base64characters.',
        'Current EPI15–17 packet05 is the one intended future conference input:44frozen sources/67authored cases. All15semantic-review03 topics have preserved evidence and local proposals, not joint approval. The new money/press/copy-choice content and source/initiative corrections need independent challenge, followed by full Player/Director prose.',
        'Existing annual contract states, vessel/atmosphere procedures and32100second ordinary voyage were preserved by07/07A. Pressure dynamics, knowledge benefits and actual paper/copy access are now explicit NEW local choices. CaseARC15-C01 uses1812seconds plus actual hostile-site elapsed time; the old1830fixed total is historical.',
        'Do not rerun one-shot refinement/preparation/navigation scripts. Before the next authoring pass preserve the current model/casebook/manifest; use this checkpoint and packet05, not older packet assertions. Local verification counts overlap and are not runtime or human tests.',
        'The same communication failure has recurred beyond three turns, but this turn made substantive independent progress. Mark goal blocked only when no meaningful authorized work can continue without external/user change; do not invent more review/status cycles. Never claim whole-game completion from source/metadata checks.',
        'No source deletions, epoch choice, cosmological identity merge, new-rule adoption or runtime/human/balance/publication approval. Ordinary spells remain419reviewed/429pending. Last verified GitHub backup18c6e3a; later cosmology remains local pending joint review.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'links':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
