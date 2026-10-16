"""Index the complete local voyage proposal while retaining the joint-review gate."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_REVIEW_03.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_VOYAGE_04.json'
    delta=A/'EPILOGUE_VOYAGE_04_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-voyage-04'
    assert all(not p.exists() for p in [target,delta,preserved])
    state=read(previous)
    refinement=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_REFINEMENT_04.json'
    geometry=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_GEOMETRY_04A.json'
    prep=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_03_PREPARATION.json'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_03.zip'
    model=A/'cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json';cases=model.with_name('CASEBOOK.json')
    assert read(geometry)['model']==info(model) and read(geometry)['casebook']==info(cases)
    assert read(refinement)['checkCount']==53 and read(geometry)['checkCount']==6 and read(refinement)['failureCount']==read(geometry)['failureCount']==0
    assert read(prep)['archive']==info(archive) and read(cases)['count']==28
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;pres.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    oldstart=originals[start].decode();oldline=next(x for x in oldstart.splitlines() if x.startswith('**Current joint review:**'))
    newline=oldline.replace('have 19 authored situations','have 28 authored situations').replace('prepared 41-source conference packet','prepared 42-source conference packet').replace('COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_02_PREPARATION.json','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_03_PREPARATION.json').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_REVIEW_03.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_VOYAGE_04.json')
    oldsummary='[The local semantic audit](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_SEMANTIC_REVIEW_03.json) records five narrow proposal corrections and ten open questions, including voyage timing, payload, breathing defenses and annual contract states.'
    newsummary='[The current local voyage proposal](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_REFINEMENT_04.json) supplies finite inventory, a real airlock, support states and a complete 8h55m worked trip. Actual trait defenses, annual contract states, payment custody and substantive patent choices still need joint review.'
    assert oldsummary in newline and 'have 28 authored situations' in newline
    newline=newline.replace(oldsummary,newsummary,1);start.write_text(oldstart.replace(oldline,newline,1),encoding='utf-8',newline='\n')
    oldguide=originals[guide].decode();oldparagraph=next(x for x in oldguide.split('\n\n') if x.startswith('The **current EPI-15–17 proposal'))
    paragraph='The **current EPI-15–17 local proposal has 28 authored cases**. [Voyage refinement 04](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_REFINEMENT_04.json) and its [geometry/boundary clarification](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_GEOMETRY_04A.json) now supply actual pounds and Load, finite equipment and fuel mass, full cabin/airlock/deck positions, support-loss and canopy procedures, real protection/door/purge cycles, and a 20-interval site schedule. The stated ordinary sample takes **8h55m**, spends **482m12s fuel** with powered idle, and leaves **117m48s fuel / 185m cabin air**. Its breathing worker uses two actual hoods. Engine-off mooring saves fuel but no elapsed air time. These are explicit NEW draft procedures; 53 source/preservation/arithmetic checks plus six narrow geometry checks support the stated examples, not runtime or human validation. All 19 earlier case IDs and previous drafts remain preserved. The [42-source revision03 conference packet](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_03_PREPARATION.json) is prepared but **unsubmitted and unadopted**. Review03 remains the issue history; the new voyage proposes resolutions for its load/support/hatch/clock gaps. Actual environmental trait/card dispositions, annual contract records and deadline composition, finite wage/scrap custody, substantive patent knowledge/free-will choices and EPI-08–14 integration still need joint review. The owner campaign era remains unanswered.'
    guide.write_text(oldguide.replace(oldparagraph,paragraph,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [refinement,geometry,prep]);row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [refinement,geometry])
    row['currentEvidenceAddenda'].append({'id':'epilogue-voyage-local-proposal-04','recordedAtUtc':now,'sourceCount':42,'authoredCases':28,'siteIntervals':20,'ordinaryVoyageSeconds':32100,'sourcePreservationArithmeticChecks':53,'geometryChecks':6,'failures':0,'newRulesAdopted':False,'submittedToGpt':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==oldrow[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before['aspects'] if x['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied/110cases. GPT EPI08–14 completion confirmed/47reported cases; exact archive unavailable/unreviewed; native export has no assistant reply/systemError. EPI15–17 local voyage04 now has finite mass/Load, airlock/support states, 20interval site and32100second ordinary trip; 28cases,53+6narrow checks, revision03packet42sources prepared/unsubmitted/unadopted. Environment/contract/economy/design/cross-module questions still open. Campaign era/runtime/human/balance/full-game/publication remain open;419/429spells. Laterwork local.'
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_CAMPAIGN_ARCS_REVIEW_03_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_VOYAGE_04_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1;text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('EPI16 — complete local voyage proposal04, not adopted',refinement.name),('EPI16 — exact airlock geometry and boundary clarification',geometry.name),('EPI15–17 — prepared revision03,42sources/28cases',prep.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':oldparagraph,'replacement':paragraph}];changes[1]['operations']=[{'old':oldline,'replacement':newline}];changes[2]['operations']=[{'aspectId':'DD-50','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1500:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Concrete local voyage proposal only; joint adoption remains pending.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['cosmologyEpilogueCampaignArcsLocalDraft'].update(status='localvoyage04/geometry04A; conference revision03prepared,unsubmitted,unadopted',model=info(model),casebook=info(cases),voyageRefinement=info(refinement),geometryClarification=info(geometry),authoredCases=28,conferenceSourceCount=42,conferencePreparation=info(prep),conferencePacket=info(archive),siteIntervals=20,ordinaryVoyageSeconds=32100,newRulesAdopted=False)
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
      'Check for the exact EPI08–14 return if external state changes. Owner already asked once. Expected70386bytes/SHA25624eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. Completion known, file unavailable. Native export user turnfb930b64-06e3-4a33-9f72-60037b465c97 has no assistant reply/systemError; Chrome3tab286 focus-emulation reads still time out. No live generation verified.',
      'Current local arc model is voyage04 plus geometry04A,28cases. Packet03has42sources including new equipment-weight source, and supersedes02for eventual submission only. Do not resend authoring of alreadycompletedEPI08–14 or submit an outdated arc packet.',
      'Voyage default is32100seconds=8h55m with20site intervals totaling3726s. Powered28932s, fuel7068sleft, air11100sleft. Engine-offsite uses12powered seconds, total25218s powered. Two actual hoods used. All prior19caseIDs retained. Currentmodel hash is bound bygeometry04A andprep03; base04receipt binds its preserved earlier version.',
      'Continue substantive independent work on actual environment/trait/card dispositions (ARC03-07), annualrecord/exit/deadline/absence states(08/09), finitecrew/scrap payments(12), and realpatentknowledge/free-willarc(15), then confer when actualGPTexchange resumes. Do not call the authored local clock a human/runtime result.',
      'All sources/prior drafts preserved, no joint adoption, epoch choice, identity merge or source deletion. Fullgame/runtime/human/balance/publication stillopen;419reviewed/429pendingordinaryspells. LatestverifiedGitHub18c6e3a; laterworklocal. Thisgoalturnmadeconcreteauthoredprogress despitejoint-transferblocker; notatimpassewhileindependentworkremains.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))
if __name__=='__main__':main()
