"""Index the full source/proposal packet while retaining all approval boundaries."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CORE_CONSUMABLE_USE_DRAFT_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CORE_CONSUMABLE_ITEMS_DRAFT_01.json'
    delta=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-core-consumable-items-draft-01'
    prep=A/'CORE_CONSUMABLE_CONFERENCE_01_PREPARATION.json';first=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01_PREPARATION.json';refine=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01A_REFINEMENT.json'
    root=A/'core-consumable-items-local-draft-01';archive=A/'DD_Core_Consumables_24_Proposals_01.zip'
    assert all(not p.exists() for p in [target,delta,preserved])
    packet=read(prep);assert packet['archive']==info(archive) and packet['currentItemModel']==info(root/'ITEMS_MODEL.json') and packet['currentItemCases']==info(root/'CASEBOOK.json')
    assert read(root/'CASEBOOK.json')['count']==52 and read(refine)['failureCount']==0
    state=read(previous);start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    oldstart=originals[start].decode();text=oldstart
    oldcheckpoint=previous.relative_to(G).as_posix();assert oldcheckpoint in text
    text=text.replace(oldcheckpoint,target.relative_to(G).as_posix(),1)
    oldparagraph=next(x for x in text.split('\n\n') if x.startswith('**Current independent development:**'))
    paragraph='**Current independent development:** The [Core consumable item discussion](docs/audit/2026-10-08/full-game/core-consumable-items-local-draft-01/DIRECTOR_DISCUSSION.md) now contains **20 individual procedure proposals and four explicit source-decision holds**: Stoneback Stout, Sovereign Reserve, Dreammilk and Ghostwine. It adds actual overdose consequences, source-qualified Bard/vision/healing/resource interfaces, finite timing and provisions. The [27-source conference packet](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_CONFERENCE_01_PREPARATION.json) combines these with 14 shared-use proposals and **80 authored situations** (28 common plus52 individual; eight are unresolved-source boundary cases). It is prepared but unsubmitted and unadopted. No consumable, global condition or cosmological meaning is approved by local drafting; actual joint review remains necessary.'
    text=text.replace(oldparagraph,paragraph,1)
    oldrow=next(x for x in text.splitlines() if x.startswith('| Core brews and magical substances |'))
    newrow='| Core brews and magical substances | [All24 original source records](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_24_SOURCE_AUDIT.md) remain preserved. [Shared use](docs/audit/2026-10-08/full-game/core-consumable-use-local-draft-01/DISCUSSION.md) supplies14 unapproved choices. [Individual proposals](docs/audit/2026-10-08/full-game/core-consumable-items-local-draft-01/DIRECTOR_DISCUSSION.md) supply20 item envelopes and four source holds, with52 authored situations. [Refinement01A](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_ITEMS_DRAFT_01A_REFINEMENT.json) fixes rough-motion clocks, post-crash Redwake locks, zero-damage Ember Resin and mixed-element Wyrmspice accounting. The [complete27-source/80-situation packet](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_CONFERENCE_01_PREPARATION.json) is prepared, unsubmitted and unadopted. All24 still need actual exact review; no generic or individual item promotion. |'
    text=text.replace(oldrow,newrow,1);start.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-28');oldaspect=deepcopy(row)
    row['draftEvidence'].extend(p.relative_to(G).as_posix() for p in [root/'ITEMS_MODEL.json',root/'DIRECTOR_DISCUSSION.md',root/'CASEBOOK.json',prep])
    row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [root/'LOCAL_CHECKS.json',refine])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'core-consumable-items01-refinement01a-local-proposals','recordedAtUtc':now,'sourceItems':24,'individualProcedureProposals':20,'sourceDecisionHolds':['CB-03','CB-12','CS-02','CS-05'],'individualAuthoredSituations':52,'commonAuthoredSituations':28,'conferenceSources':27,'initialChecks':37,'refinementChecks':7,'checksOverlap':True,'failures':0,'submittedToGpt':False,'newRulesAdopted':False,'itemsPromoted':0,'fullDomainClosed':False,'scope':'Preserved sources and concrete unapproved authored procedures; four exact source decisions and every item’s actual review remain open.'})
    for k in ['status','closure','humanEvidence','completionClass']:assert row[k]==oldaspect[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-28']==[x for x in before['aspects'] if x['id']!='DD-28']
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied/110cases. EPI08–14 exact return still unretrieved; prior export requests terminal user-only/systemError, no live generation verified. EPI15–17 packet05 prepared/unsubmitted/unadopted:44sources/67cases. Core24 now20 local individual procedure proposals plus4 explicit source holds,14 common choices and80 authored situations;27-source packet01 prepared/unsubmitted/unadopted. Original sources and all active approvals unchanged. Ordinary spells419reviewed/429pending; joint semantics, campaign era, runtime/human/balance/full-game/publication open; later work local.'
    code=originals[nav].decode();tail=' + read(A / "CORE_CONSUMABLE_USE_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "CORE_CONSUMABLE_ITEMS_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('Core24 — individual proposals and four held sources','core-consumable-items-local-draft-01/DIRECTOR_DISCUSSION.md'),('Core24 — actual clock/lock/damage refinement01A',refine.name),('Core24 —27-source/80-situation conference prepared',prep.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]]
    changes[0]['operations']=[{'old':oldcheckpoint,'replacement':target.relative_to(G).as_posix()},{'old':oldparagraph,'replacement':paragraph},{'old':oldrow,'replacement':newrow}]
    changes[1]['operations']=[{'aspectId':'DD-28','old':oldaspect,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1500:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='20individual consumable proposals,4source holds; no item/global/cosmology promotion.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['coreConsumableItemsLocalDraft']={'status':'prepared-unsubmitted-unadopted','firstPreparation':info(first),'currentRefinement':info(refine),'model':info(root/'ITEMS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'discussion':info(root/'DIRECTOR_DISCUSSION.md'),'conferencePreparation':info(prep),'conferencePacket':info(archive),'sourceItems':24,'itemProposals':20,'sourceHolds':['CB-03','CB-12','CS-02','CS-05'],'itemSituations':52,'commonSituations':28,'frozenSources':27,'newRulesAdopted':False,'itemsPromoted':0,'runtimeSituationsExecuted':0}
    state['safeNextActions']=[
        'This turn made substantive independent progress:20 item procedures, ten actual new overdose proposals, four source holds,52 item situations, source-qualified Bard Chants, selected interaction fixes, and one full27-source conference packet. Previous turn was also progress, not a verified process wait.',
        'Current consumable packet is DD_Core_Consumables_24_Proposals_01.zip (2192850bytes,SHA25670f912923c4f91563bfe02d02dfc9863c49b102da3924e506ed95f93b6cdaa27), prepared but never submitted. It contains14common choices and80caseIDs (28common+52individual, including8held-boundarycases). Submit only through restored actual GPT exchange; no local approval substitutes for conference.',
        'Four real holds: Stoneback needs the actual cold-exposure-stage interpretation; Dreammilk needs causal first-failed-save and sleep/divination/rest semantics; Ghostwine needs actual ethereal/residue/fear eligibility and protected-information scope; Sovereign Reserve needs final-sentence/record/terminal-state interpretation. General cosmology review did not decide these items. Original24 records unchanged; all24 remain unpromoted.',
        'Refinement01A is current: Tidesilver tracks rough seconds with600steady-second reset; Redwake lock requires a qualifying rest at/after actual crash, not prepaid before it; EmberResin handles zero/negative actual damage formulas; Wyrmspice selects a real stored element and resolves each overlapping dose recoil in application order. Initial01 versions remain history. A missing digest helper interrupted first refinement after file writes; completion script verified actual state and finished manifest/receipt without reapplying. Do not rerun one-shot scripts.',
        'No EPI08–14 return ZIP was found in exact top-level Downloads/workspace search this turn. Actual GPT was last authoritatively terminal user-only/systemError; previous Chrome DOM/screenshot calls failed while tab inventory remained available. No live generation verified, and no duplicate authoring/export prompt was sent this turn. Existing user recovery question remains pending.',
        *[s for s in state['safeNextActions'] if 'Expected EPI08' in s or 'Current EPI15' in s or 'No source deletions' in s]
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'links':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
