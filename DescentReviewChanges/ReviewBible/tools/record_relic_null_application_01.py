"""Update owner navigation after actual complete-module acceptance and application."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat();application=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json';app=read(application)
    assert app['newProvisionalModuleAdopted'] and app['failureCount']==0
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_PATCH_REVIEW_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_APPLICATION_01.json'
    delta=A/'RELIC_NULL_APPLICATION_01_NAVIGATION_DELTA.json';keep=A/'navigation-before-relic-null-application-01'
    assert all(not p.exists() for p in [target,delta,keep])
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b);originals[p]=b
        saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=next(s for s in text.split('\n\n') if s.startswith('**Current joint review:**'))
    new='**Current joint review:** **EPI-01–14 is now jointly reviewed and locally applied as NEW provisional playtest authorship.** The latest EPI-08–14 module supplies four relics, twelve optional chambers, eight actors, Null exposure/damage/purges, four finite plants and the Bittersap Antidote. Read the [player chapter](DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md) and [Director chapter](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EPILOGUE_RELIC_NULL_REVIEWED_01.md). [Actual GPT accepted the complete corrected module](docs/audit/2026-10-08/full-game/RELIC_NULL_03_FINAL_MODULE_CONFIRMATION_01_DOM.txt), following the nine exact correction approvals. The [application receipt](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json) records 247 source checks, 87 patch checks and 8 application checks with no failures; all 75 authored examples and 85 source bindings are retained. These are not runtime or human tests. Next is the prepared EPI-15–17 conference, followed by the remaining game systems and content. Continue from the [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_APPLICATION_01.json), [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md) or [review map](REVIEW_MAP.html). Ordinary spells remain **419 reviewed / 429 pending**. Campaign era, unresolved identities, runtime, human playtesting, balance and whole-game flow remain open. Latest verified GitHub backup is **18c6e3a**; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    text=text.replace(old,new,1)
    text=text.replace('Part 4 is now reviewing the complete corrected EPI-08–14 module.','Part 4 has completed the corrected EPI-08–14 module review.',1)
    text=text.replace('Actual joint work has resumed in Part 4 on the EPI-08–14 correction packet; the consumable and environment packets await their own later review.','Actual joint work continues in Part 4; EPI-08–14 is applied, while the consumable and environment packets await their own later review.',1)
    row='| Careful cosmology playtest modules | [EPI-01–07 character rules](DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md), [EPI-08–14 relics, optional chambers and Null rules](DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md); current provisional authorship, with separate Director material |\n'
    anchor='| Detailed interfaces and remaining work |';assert text.count(anchor)==1;text=text.replace(anchor,row+anchor,1);start.write_text(text,encoding='utf-8',newline='\n')
    text=originals[guide].decode();old=next(s for s in text.split('\n\n') if s.startswith('**Current review:**'))
    new='**Current review:** The complete corrected **EPI-08–14 module is jointly accepted and locally applied as NEW provisional playtest authorship**. Use the [player chapter](../../mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md), [Director chapter](EPILOGUE_RELIC_NULL_REVIEWED_01.md), [exact model and confirmation wrapper](../../../data/director/cosmology/epilogue_relic_null_reviewed_01.json) and [75 authored cases](../../../data/director/cosmology/epilogue_relic_null_cases_01.json). Actual Review Continuation Part4 agreed with all nine local corrections and then [accepted the complete combined module by exact archive hash](../../../../../docs/audit/2026-10-08/full-game/RELIC_NULL_03_FINAL_MODULE_CONFIRMATION_01_DOM.txt). The [application receipt](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json) records 247 source/citation/identity checks, 87 patch-preservation checks and eight application checks, all passing. Original84 source entries plus the separately supplied existing Expedition-cap source are preserved. Original returns and pending labels in the historical audit copy are unchanged. This is not canon, runtime, balance, human-playtest, full-cosmology or whole-game approval. EPI-15–17 remains prepared for its own conference.'
    text=text.replace(old,new,1)
    old='The [latest actual GPT transfer record](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_NATIVE_TRANSFER_STATUS_03.json) confirms both recovery prompts have no assistant reply and the chat reports a system error. Exact EPI-08–14 recovery is complete. Its correction review/integration, final Player/Director prose and the owner campaign era remain open.'
    new='Earlier recovery failures are retained as history. The EPI-08–14 dependency is now satisfied by the exact joint acceptance/application above. The owner campaign era remains unresolved; EPI-15–17 must be reviewed as conditional staging, without silently choosing that era.'
    assert old in text;text=text.replace(old,new,1)
    text=text.replace('Next are the [EPI-08–14 source reading]','Preserved evidence includes the [EPI-08–14 source reading]',1)
    text=text.replace('Those groups remain unadopted. EPI-15–17 staging still depends on the unanswered campaign-frame choice.','Those EPI-08–14 groups are now applied within the provisional scope above. EPI-15–17 staging still depends on the unanswered campaign-frame choice.',1)
    guide.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['draftEvidence'].extend([application.relative_to(G).as_posix(),app['confirmation']['path'],app['data']['path'],app['playerChapter']['path'],app['directorChapter']['path']])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'epilogue-relic-null-application01','recordedAtUtc':now,'completeModuleJointlyAccepted':True,'newProvisionalModuleApplied':True,'authoredCases':75,'sourceBindings':85,'sourceChecks':247,'patchChecks':87,'applicationChecks':8,'failureCount':0,'wholeAreaClosed':False,'runtimeTestsExecuted':0,'humanPlaytested':False})
    assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id']!='DD-50']==[x for x in coverage['aspects'] if x['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='Complete EPI08–14 accepted by actual Part4 and applied as NEW provisional authored reference:4 relics,12 chambers,8 actors,Null/purges,4 flora,finite antidote,75 examples,85 sources.247 source+87 patch+8 application checks pass. EPI01–14 now locally applied; EPI15–17 remains prepared/unsent. Runtime,human,balance,whole-game and owner epoch/identities remain open.'
    code=originals[nav].decode();tail=' + read(A / "RELIC_NULL_PATCH_REVIEW_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "RELIC_NULL_APPLICATION_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(values)==1
    code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    items=[('EPI08–14 — applied module and validation',application.name),('EPI08–14 — actual complete-module acceptance','RELIC_NULL_03_FINAL_MODULE_CONFIRMATION_01_DOM.txt')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newProvisionalModuleApplied':'EPI08–14','fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=1,newRuleAdoptionScope='Exact EPI08–14 complete module adopted locally as NEW provisional authored playtest reference only.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['relicNullRevision03'].update(moduleApplied=True,application=info(application),fullModuleConfirmation=app['confirmation'])
    state['activeGptReview'].update(status='Complete module explicitly ACCEPTED by actual Part4; exact candidate locally applied.',generationConfirmedLiveAtObservation=False,returnReceived=True,expectedReturn=None,newRulesAdopted=True,application=info(application))
    state['safeNextActions']=['Continue in actual Review Continuation Part4. EPI08–14 is complete within authored provisional scope; do not restart its accepted conference.','Prepare the existing44-source/67-case EPI15–17 conference for actual submission, carrying the newly accepted EPI08–14 module as explicit current context. Preserve original packet/source hashes and conditional campaign-era/identity holds. Do not adopt the later arcs before actual review.','Then proceed through remaining environment/consumable/disease, ordinary spells, feats, bestiary, Director, packaging and companion work according to the75-area ledger. Human playtests/balance remain separate from authored completion.','Latest GitHub backup remains18c6e3a; do final joint whole-game flow and authorized delivery at the appropriate milestone. No later push claimed.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(application),'meaningfulProgress':scope};state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'application':info(application),'links':build['existingDistinctLinks'],'missingLinks':0}))

if __name__=='__main__':main()
