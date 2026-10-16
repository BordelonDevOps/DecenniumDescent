"""Index the substantive common-use draft without promoting any consumable."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ECONOMY_PATENTS_07.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CORE_CONSUMABLE_USE_DRAFT_01.json'
    delta=A/'CORE_CONSUMABLE_USE_DRAFT_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-core-consumable-use-draft-01'
    prep=A/'CORE_CONSUMABLE_USE_DRAFT_01_PREPARATION.json'
    folder=A/'core-consumable-use-local-draft-01'
    assert all(not p.exists() for p in [target,delta,preserved])
    candidate=read(prep); state=read(previous)
    assert candidate['model']==info(folder/'USE_MODEL.json') and candidate['discussion']==info(folder/'DISCUSSION.md')
    assert read(folder/'LOCAL_CHECKS.json')['failures']==0 and read(folder/'CASEBOOK.json')['count']==28
    start=G/'START_HERE.md'; nav=R/'tools/build_review_map.py'; ledger=R/'data/playtest/game_development_coverage.json'
    originals={}; saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    oldstart=originals[start].decode();text=oldstart
    oldcheckpoint='docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ECONOMY_PATENTS_07.json'
    assert oldcheckpoint in text;text=text.replace(oldcheckpoint,'docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CORE_CONSUMABLE_USE_DRAFT_01.json',1)
    oldrow=next(x for x in oldstart.splitlines() if x.startswith('| Core brews and magical substances |'))
    newrow='| Core brews and magical substances | [All 24 original source records](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_24_SOURCE_AUDIT.md) remain preserved. The [new common-use discussion draft](docs/audit/2026-10-08/full-game/core-consumable-use-local-draft-01/DISCUSSION.md) proposes dose history, repeat use, tolerance, actual rest boundaries, independent crashes, maintenance and provisions: 14 explicit decisions, 28 authored situations and 16 current source bindings. [Preparation/check receipt](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_USE_DRAFT_01_PREPARATION.json). Unsubmitted and unadopted; all 24 individual profiles, severe complications and exact review remain open. Ghostwine/Sovereign Reserve still need specific information/recording decisions. |'
    text=text.replace(oldrow,newrow,1)
    newparagraph='**Current independent development:** While the actual GPT exchange is unavailable, the [Core consumable common-use draft](docs/audit/2026-10-08/full-game/core-consumable-use-local-draft-01/DISCUSSION.md) now presents concrete proposed rules for the 24-item catalog. Its 28 situations are authored examples, not executed gameplay tests; no item or global condition rule was promoted. The exact long-rest boundary, individual overdose consequences and every complete item profile still require joint review.'
    anchor='**Onboarding review complete:**';assert text.count(anchor)==1;text=text.replace(anchor,newparagraph+'\n\n'+anchor,1)
    start.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-28');oldaspect=deepcopy(row)
    row['draftEvidence'].extend(p.relative_to(G).as_posix() for p in [folder/'USE_MODEL.json',folder/'DISCUSSION.md',folder/'CASEBOOK.json'])
    row['validationEvidence'].append((folder/'LOCAL_CHECKS.json').relative_to(G).as_posix())
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'core-consumable-common-use-local-draft-01','recordedAtUtc':now,'preparation':prep.relative_to(G).as_posix(),'preservedSourceItems':24,'sharedProposedDecisions':14,'authoredSituations':28,'currentSourceBindings':16,'localPreservationAndArithmeticChecks':23,'failures':0,'scope':'Common-use proposal only; no complete individual item, exact review, runtime or human-test claim.','submittedToGpt':False,'newRulesAdopted':False,'individualItemsPromoted':0,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','completionClass']:assert row[k]==oldaspect[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-28']==[x for x in before['aspects'] if x['id']!='DD-28']
    ledger.write_bytes(encoded(coverage))
    scope=state['status']+' Core24 common-use local draft now adds14 proposed decisions and28 authored situations under16 current source bindings; all24 individual items and exact review remain open. No operational promotion or gameplay execution.'
    code=originals[nav].decode();tail=' + read(A / "EPILOGUE_ECONOMY_PATENTS_07_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1;code=code.replace(tail,tail.rstrip('\n')+' + read(A / "CORE_CONSUMABLE_USE_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('Core consumables — common use,14 proposed decisions/28 cases',prep.name),('Core consumables — readable local discussion draft','core-consumable-use-local-draft-01/DISCUSSION.md')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]]
    changes[0]['operations']=[{'old':oldcheckpoint,'replacement':target.relative_to(G).as_posix()},{'old':oldrow,'replacement':newrow},{'old':anchor,'replacement':newparagraph+'\n\n'+anchor}]
    changes[1]['operations']=[{'aspectId':'DD-28','old':oldaspect,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1500:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Common consumable use discussion draft only; no item or global-rule promotion.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['coreConsumableUseLocalDraft']={'status':'unsubmitted, unadopted; all individual items still open','preparation':info(prep),'model':info(folder/'USE_MODEL.json'),'discussion':info(folder/'DISCUSSION.md'),'casebook':info(folder/'CASEBOOK.json'),'sourceBindings':16,'sourceItems':24,'proposedDecisions':14,'authoredSituations':28,'checks':23,'runtimeTestsExecuted':0,'itemsPromoted':0}
    state['safeNextActions']=[
        'Actual part3 native reader again reports systemError and the same terminal user-only export retry c702b47c. Chrome3 tab125746286 still exists, but both DOM and screenshot calls fail at the browser focus command. No live generation verified; do not blindly resend. Existing owner recovery question remains pending.',
        'The latest substantive work is CORE_CONSUMABLE_USE_DRAFT_01_PREPARATION.json and core-consumable-use-local-draft-01:24 originals,14 explicit common-use proposals,28 authored situations,16 current sources.23 checks cover source equality and selected arithmetic only. No individual item is operational/approved by this draft.',
        'Next consumable development must finish full individual profiles, all effect/crash clauses and12 actual severe complications. Resolve the explicit beneficial-Long-Rest versus completed-rest choice and repeated-use/overdose policy with actual GPT. The generic recovery chapter is unchanged. Locate or explicitly propose the missing Wyrmspice Mutation table; do not borrow Warrior mutations by name.',
        'Ghostwine/Sovereign Reserve require specific actual source-informed perception/terminal-record decisions. Literal searches of current souls/planes JSONs found no item-specific clauses. That bounded finding is not global absence or authority to invent cosmological identities. Stoneback, Tidesilver and Embermark need actual environment semantics; preserve all source wording.',
        *state['safeNextActions'][1:]
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'links':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
