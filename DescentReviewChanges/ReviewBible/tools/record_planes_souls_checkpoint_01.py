"""Publish current navigation for verified planes and the submitted souls conference."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PART3_CHRONOLOGY_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PLANES_SOULS_SUBMISSION_01.json'
    delta=A/'PLANES_SOULS_SUBMISSION_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-planes-souls-submission-01'
    submission=A/'COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION_RECEIPT.json'
    assert all(not p.exists() for p in [checkpoint,delta,preserved,submission])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    application=A/'COSMOLOGY_PLANES_01_APPLICATION_CHECK.json';app=read(application)
    assert app['verificationFailureCount']==0 and app['verificationCheckCount']==468
    browser=A/'COSMOLOGY_SOULS_RESEARCH_01_BROWSER_RECEIPT.json';obs=read(browser)
    prep=A/'COSMOLOGY_SOULS_RESEARCH_01_PREPARATION.json';packet=read(prep)
    assert packet['archive']==info(G/packet['archive']['path'])
    dom=A/'COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION_DOM.txt';assert 'ChatGPT is responding' in dom.read_text(encoding='utf-8')
    submission.write_bytes(encoded({**obs,'preparation':info(prep),'archive':packet['archive'],'sources':79,'primaryIssues':21,'authoredSituations':34,'submittedPrompt':info(A/'COSMOLOGY_SOULS_RESEARCH_01_SUBMITTED_PROMPT.txt'),'sentDom':info(dom),'visibleProof':info(A/'COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION.png'),'sourceInformationDeleted':0}))
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
        preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('Planes review completed with corrected evidence: 11 bounded decisions, 76 retained source claims, 64 frozen source hashes and 18 actual travel-card bindings; 468 local checks passed. Two return archives preserved. '
           'The Director successor keeps original realms, mortal cosmography and saved website presentations distinct, preserves current effects and 12 pending higher travel spells, and adopts no new operating rules. '
           'COSMOLOGY-SOULS-RESEARCH-01 submitted once in owner-created Part 3 with 79 sources, 21 issues and 34 authored situations. GPT was responding at submission. '
           'It requests concrete proposed research, qualification, taint, Hunt and rare-intervention procedures; no numerical model or spell approval is adopted by submission. '
           'Current campaign epoch, chronology and epilogue adoption remain open. Ordinary spells419reviewed429pending. Latest verified GitHub18c6e3a; later work local.')
    old_start=start.read_text(encoding='utf-8');old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The [planes Director chapter](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/PLANES_REVIEWED_01.md) is verified and saved: 11 decisions, 76 preserved claims and 18 actual travel-card bindings. The [souls, Equation research, taint and Hunt conference](docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION_RECEIPT.json) is now running in the owner-created Part 3 chat, with 79 source files, 21 questions and 34 worked situations. Use the [cosmology reading guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_PLANES_SOULS_SUBMISSION_01.json). Ordinary spells remain **419 reviewed / 429 pending**; no new numerical taint or pending spell rule is adopted by this submission. Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(old_line,new_line,1),encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8');new_current=old_current
    sentence='Planes, souls/death/resurrection, history, divine/class powers and campaign revelations still need their remaining reviews.'
    assert sentence in new_current
    new_current=new_current.replace(sentence,'The [planes reference](PLANES_REVIEWED_01.md) is now verified within its bounded scope. Souls/death/resurrection, history, divine/class powers and campaign revelations still need their remaining reviews.',1)
    paragraph=next(p for p in new_current.split('\n\n') if p.startswith('The [planes review packet]'))
    replacement='The [planes review](PLANES_REVIEWED_01.md) preserves the saved website, original account and mortal teaching with their different authority. Its corrected return passed 468 local checks, including 64 frozen source hashes and 18 actual travel-card bindings. The first return and all source records remain preserved. Operational soul/death jurisdiction now follows in the [submitted souls/Research conference](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION_RECEIPT.json). This covers the 12 SH and 9 ER discussion sections and 34 situations, with library and chronology context. GPT was responding at submission; no verdict or new numerical model is implied.'
    new_current=new_current.replace(paragraph,replacement,1).replace('It is unsubmitted and unadopted.','It has been submitted in the combined souls/Research conference; its new operating proposals remain unadopted.',1)
    new_current+='\nHistorical workflow sentences inside the frozen draft artifacts describe their creation time. The owner has already created Part 3, planes verification is complete, and the combined souls/Research packet has been submitted. No continuation permission is pending. The draft source findings and open design decisions are preserved.\n'
    current.write_text(new_current,encoding='utf-8',newline='\n')
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-15','DD-46','DD-50','DD-61','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'planes-souls-submission-01','recordedAtUtc':now,'planesApplication':application.relative_to(G).as_posix(),'soulsResearchSubmission':submission.relative_to(G).as_posix(),'planesBoundedReviewComplete':True,'newOperatingRulesAdopted':False,'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [application,submission])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['status','closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "PART3_CHRONOLOGY_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "PLANES_SOULS_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    additions=[('Souls/Research — 21 issues and 34 situations submitted in Part 3',submission.name),('Planes — corrected scoped successor verified and applied',application.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in additions),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,ledger_path,nav]]
    changes[0]['operations']=[{'old':old_current,'replacement':new_current}];changes[1]['operations']=[{'old':old_line,'replacement':new_line}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageLedger=info(ledger_path),coverageDelta=info(delta),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['cosmologyPlanesReview']={'status':'corrected scoped Director reference applied','application':info(application),'chapter':app['chapter'],'data':app['reviewedData'],'verificationChecks':468,'sourceClaims':76,'directActualTravelCards':18,'newOperatingRulesAdopted':False}
    state['activeGptReview']={**obs,'submission':info(submission),'archive':packet['archive'],'continuationApproval':'Owner-created Part 3; ongoing collaboration authorized','responsePendingAtSubmission':True}
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['cosmologySoulsResearchSubmission']={'preparation':info(prep),'submission':info(submission),'sources':79,'primaryIssues':21,'authoredSituations':34,'newOperatingRulesAdopted':False}
    state['safeNextActions']=[
        'Observe the live COSMOLOGY-SOULS-RESEARCH-01 response in Part 3 Chrome tab125746244 at the recorded URL. Do not resend or ask continuation permission again. Verify its eight-file return, exact citations and proposed state model before applying.',
        'Discuss substantive research qualification, personal five-discipline competence, temporary borrowed proficiency, functional demonstration, two taint causes, Hunt initiation and exceptional intervention designs with GPT. Preserve genuine existing language/class/death-prevention benefits and distinguish new designs from source canon.',
        'After that conference, continue the chronology/research-site and 17-group epilogue work, preserving original P324 adaptation permission and the unresolved campaign epoch/calendar/Choir seams. Do not silently map cosmic libraries to Dungeon floors.',
        'Ordinary spells419reviewed429pending; no pending travel or resurrection card approval by cosmology review. Soul Mirror is already reviewed-authored. Full runtime/human playtest/game-flow certification remains open.',
        'Latest verified GitHub18c6e3a; subsequent cosmology work local. No sources deleted. Owner monitors usage.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'submission':info(submission),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'approvalStatusesUnchanged':True,'newOperatingRulesAdopted':False}))

if __name__=='__main__':main()
