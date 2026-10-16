"""Link the bounded library inventory without changing any rule or approval status."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_HUNT_DRAFT_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_LIBRARY_INVENTORY_01.json'
    delta=A/'EQUATION_LIBRARY_INVENTORY_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-equation-library-inventory-01'
    assert all(not p.exists() for p in [checkpoint,delta,preserved])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    inventory=R/'data/director/cosmology/equation_library_source_inventory_01.json'
    chapter=R/'docs/director-only/cosmology/EQUATION_LIBRARY_SOURCE_INVENTORY_01.md'
    citation=A/'COSMOLOGY_EQUATION_LIBRARY_SOURCE_INVENTORY_01_CHECK.json'
    c=read(citation); data=read(inventory)
    assert c['inventory']==info(inventory) and c['chapter']==info(chapter)
    assert c['exactEvidenceLocationsVerified']==125 and c['sourceBindingsVerified']==10
    for row in data['sourceBindings']: assert info(G/row['path'])==row
    planes=A/'DD_Cosmology_Planes_01.zip'
    assert info(planes)['sha256']=='158630558c141a69485c47bdfb727c8f29d1727bca1e78c45f01ac3944bd8fe5'
    souls=R/'data/director/cosmology/souls_death_hunt_conference_draft_01.json'
    assert info(souls)==state['cosmologySoulsDeathPreparation']['draft']
    for row in read(souls)['sourceBindings']: assert info(G/row['path'])==row
    start=G/'START_HERE.md'; ledger_path=R/'data/playtest/game_development_coverage.json'
    nav=R/'tools/build_review_map.py'; current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes(); preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('Equation library source inventory prepared: 22 qualified records, 125 exact evidence locations across 10 source files, '
           '6 conference questions and 8 review situations. Cantor’s Archive is explicitly Floor 47; original Wax Library is a Dungeon chamber seed without a fixed floor. '
           'Other cosmic sites, institutions, historical collectives and Director examples do not supply additional mapped Descent libraries or assigned Equation fragments. '
           'No sites relocated, aliases merged, fragments assigned, numeric Research/taint rules adopted or source information deleted. '
           'Souls/Hunt 12-section/20-case draft remains prepared and unsubmitted; ordinary spells remain 419 reviewed/429 pending. '
           'Part 2 reached its conversation-length limit; existing Part 3 choice remains pending. Latest verified GitHub 18c6e3a; subsequent work local.')
    old_start=start.read_text(encoding='utf-8'); old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** [Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) and the [Q6 endgame review](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md) are saved. The [souls, forbidden research and Hunt draft](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md) has 12 discussion sections and 20 situations. The [library source inventory](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EQUATION_LIBRARY_SOURCE_INVENTORY_01.md) adds 22 qualified records, 6 conference questions and 8 situations with 125 exact source locations checked; it assigns no Equation fragments. Both await joint review. The planes review reached [ChatGPT’s conversation-length limit](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json); the prepared Part 3 handoff awaits your already-requested choice. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_LIBRARY_INVENTORY_01.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    changed=old_start.replace(old_line,new_line,1); assert changed.replace(new_line,old_line,1)==old_start
    start.write_text(changed,encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8')
    addition='\nFor the Equation puzzle, use the [existing-library source inventory](EQUATION_LIBRARY_SOURCE_INVENTORY_01.md): 22 qualified records, 125 checked evidence locations, 6 conference questions and 8 review situations. Cantor’s Archive is mapped to Floor 47; the original Wax Library is a Dungeon chamber seed without a fixed floor. Other archive names are not automatically additional Descent libraries. No Equation fragment, new location, numeric progression or taint rule is adopted by the inventory.\n'
    current.write_text(old_current+addition,encoding='utf-8',newline='\n')
    before=read(ledger_path); ledger=deepcopy(before); touched={'DD-50','DD-61','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'equation-library-source-inventory-01','recordedAtUtc':now,'inventory':inventory.relative_to(G).as_posix(),'citationCheck':citation.relative_to(G).as_posix(),'jointlyReviewed':False,'newRulesAdopted':False,'fullDomainClosed':False})
            row.setdefault('draftEvidence',[]).extend(p.relative_to(G).as_posix() for p in [inventory,chapter])
            row.setdefault('validationEvidence',[]).append(citation.relative_to(G).as_posix())
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['status','closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched: assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "SOULS_HUNT_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "EQUATION_LIBRARY_INVENTORY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']; assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]); text=text.replace(literal,repr(scope),1)
    marker='    pending = [\n'; assert text.count(marker)==1
    text=text.replace(marker,marker+'        '+repr(('Equation libraries — 22 records and 125 source locations; joint review pending',citation.name))+',\n',1)
    compile(text,str(nav),'exec'); nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,ledger_path,nav]]
    changes[0]['operations']=[{'old':old_current,'replacement':old_current+addition}]
    changes[1]['operations']=[{'old':old_line,'replacement':new_line}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout[-2000:]); print(run.stderr[-5000:]); raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path),coverageDelta=info(delta),ownerStartPage=info(start),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        cosmologyEquationLibraryInventory={'status':'22-record qualified inventory, unsubmitted','inventory':info(inventory),'chapter':info(chapter),'citationCheck':info(citation),'sourceBindingsVerified':10,'exactEvidenceLocations':125,'questions':6,'reviewSituations':8,'equationFragmentsAssigned':0,'newRulesAdopted':False})
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions']=[
        'The existing Part3 choice remains pending. Do not ask again or infer consent from elapsed time. If the owner approves or supplies the continuation chat, preserve earlier chats and submit the prepared exact planes ZIP/handoff through Chrome CUA. No planes verdict exists.',
        'After planes completion, verify returned source/citation/evidence files before applying it. Then prepare the souls/Hunt conference using the current12section20case draft, all four bounded readings, authored-status correction, actual source files and current planes outcome.',
        'Use the Equation library inventory to author a concrete research route only as a proposal for joint review. Original Wax Library and secondary Floor47 Cantor’s Archive are candidate Descent settings; no selected passage assigns Equation fragments. Other cosmic libraries are not silently relocated. Keep Shifting Sigils/Sigil Navigators alias, campaign chronology, additional libraries, actual clue texts and exact Research prerequisites open.',
        'Independent work remains: compare the original narrative epochs and referenced sites to current campaign/Q6 revelation boundaries; prepare the language/Research prerequisites and clue provenance interfaces without deciding owner cosmology conflicts. Pending ordinary spells and other full-game domains also remain available.',
        'Soul Mirror is reviewed-authored via candidate_low_rank_136.json /spells/124; read authored_review_index before classifying selected spells. Whole ordinary-spell count419/429 is unchanged.',
        'Keep Hunt threshold, taint arithmetic, pursuer roster and exceptional intervention routes open pending explicit joint development. Do not change playable cards or reinstate the superseded absolute divine-intervention ban.',
        'Latest verified GitHub backup18c6e3a; later work local. Owner monitors usage;50percentcutoff withdrawn. Full authored game, runtime, human balance and full-game flow are not complete.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'planesPacketUnchanged':True,'soulsDraftUnchanged':True,'approvalStatusesUnchanged':True,'newRulesAdopted':False}))


if __name__=='__main__': main()
