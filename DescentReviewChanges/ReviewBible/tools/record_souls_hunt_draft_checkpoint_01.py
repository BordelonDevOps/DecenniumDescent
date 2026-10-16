"""Expose the unsubmitted souls/Hunt draft while preserving all approval boundaries."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_Q6_PLANES_SOULS_READING_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_HUNT_DRAFT_01.json'
    delta=A/'SOULS_HUNT_DRAFT_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-souls-hunt-draft-01'
    assert all(not p.exists() for p in [checkpoint,delta,preserved])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    citation=A/'COSMOLOGY_SOULS_DEATH_HUNT_DRAFT_01_CITATION_CHECK.json';c=read(citation)
    assert c['evidenceLocationsVerified']==48 and c['sourceBindingsVerified']==25
    draft=R/'data/director/cosmology/souls_death_hunt_conference_draft_01.json'
    chapter=R/'docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md'
    assert c['draft']==info(draft) and c['chapter']==info(chapter)
    correction=A/'COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json'
    readings=[A/n for n in ['COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json','COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02.json','COSMOLOGY_SOULS_CONTRACT_READING_03.json','COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04.json']]
    for row in read(draft)['sourceBindings']:assert info(G/row['path'])==row
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json'
    nav=R/'tools/build_review_map.py';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes();preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('Souls/death/Hunt concrete discussion draft prepared:12sections,20finite situations,48exact evidence locations and25current source bindings verified. '
           'Four bounded source readings cover original souls, mortal testimony, Research, contracts, Pact enforcement, existing death/temporal rules and relevant spells. '
           'Current authored-status correction: Soul Mirror has an exact-approved standalone procedure despite its preserved pending legacy catalog; selected23ordinary identities are14reviewed/9pending, whole catalog419/429 unchanged. '
           'No new taint numbers, Hunt roster, extraordinary intervention route, spell promotion, runtime or whole-domain approval. '
           'Planes review remains halted by Part2 conversation-length limit; prepared Part3 handoff awaits the already-requested owner choice. Latest verified GitHub18c6e3a; later work local.')
    old_start=start.read_text(encoding='utf-8');old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** [Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) and the [Q6 endgame review](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md) are saved. The [souls, forbidden research and Hunt draft](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md) now has 12 discussion sections and 20 situations, with 48 source locations verified; it has not been submitted or adopted. The planes review reached [ChatGPT’s conversation-length limit](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json); the prepared Part 3 handoff awaits your already-requested choice. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_HUNT_DRAFT_01.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    changed=old_start.replace(old_line,new_line,1);assert changed.replace(new_line,old_line,1)==old_start
    start.write_text(changed,encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8')
    addition='\nFor the next souls/death conference, use the [concrete souls, forbidden research and Hunt draft](SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md): 12 discussion sections and 20 situations, with 48 exact evidence locations verified. It is unsubmitted and unadopted. Its current status correction recognizes the reviewed standalone Soul Mirror procedure; the legacy pending catalog is historical evidence. No numerical taint scale or intervention route has been chosen.\n'
    current.write_text(old_current+addition,encoding='utf-8',newline='\n')
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-24','DD-50','DD-61','DD-65','DD-69'}
    evidence=[draft,chapter,citation,correction]+readings
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'souls-hunt-draft-01','recordedAtUtc':now,'draft':draft.relative_to(G).as_posix(),'citationCheck':citation.relative_to(G).as_posix(),'jointlyReviewed':False,'newRulesAdopted':False,'fullDomainClosed':False})
            row.setdefault('draftEvidence',[]).extend(p.relative_to(G).as_posix() for p in [draft,chapter])
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [citation,correction])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['status','closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "Q6_PLANES_SOULS_READING_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "SOULS_HUNT_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]);text=text.replace(literal,repr(scope),1)
    marker='    pending = [\n';assert text.count(marker)==1
    links=[('Souls/Hunt — draft citations verified; joint review pending',citation.name),('Soul Mirror — current authored status correction',correction.name),('Taint/Research — original enforcement and actual cure sources',readings[-1].name)]
    text=text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in links),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,ledger_path,nav]]
    changes[0]['operations']=[{'old':old_current,'replacement':old_current+addition}]
    changes[1]['operations']=[{'old':old_line,'replacement':new_line}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path),coverageDelta=info(delta),ownerStartPage=info(start),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        cosmologySoulsDeathPreparation={'status':'12section/20case unsubmitted discussion draft','draft':info(draft),'chapter':info(chapter),'sourceReadings':[info(p) for p in readings],'citationCheck':info(citation),'authoredStatusCorrection':info(correction),'sourceBindingsVerified':25,'exactEvidenceLocations':48,'newRulesAdopted':False})
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions']=[
        'The existing Part3 choice remains pending; do not ask again or infer consent from elapsed time. If the owner approves or supplies the continuation chat, preserve earlier chats and submit the prepared exact planes ZIP/handoff through Chrome CUA. No planes verdict exists.',
        'After planes completion, verify its returned source/citation/evidence package before applying it. Then prepare the souls/Hunt conference using the concrete12section20case draft, all four bounded reading records and current authored-status correction. Include the actual source files and current planes outcome, not just summaries.',
        'Soul Mirror is reviewed-authored via candidate_low_rank_136.json /spells/124; the legacy catalog remains pending by design. Read authored_review_index before classifying other selected spells. Across current23ordinary selected identities14are reviewed9pending; whole419/429unchanged.',
        'Independent work remains: inventory actual library sites, Research qualifications and clue sources, then develop the Equation puzzle using original lore first. Existing six-tick examples and seven-stage notebook suggestions are not automatic owner choices.',
        'Keep Hunt threshold, taint arithmetic, pursuer roster and extraordinary intervention routes open pending explicit joint development. Do not change playable cards, claim completed Time Loop or reinstate the superseded absolute divine-intervention ban.',
        'Continue the full authored-game objective and remaining429ordinary spells/other open systems. Runtime/human balance/full-game flow are not certified.',
        'Latest verified GitHub backup18c6e3a; later work local. Owner monitors usage;50percentcutoff withdrawn.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
