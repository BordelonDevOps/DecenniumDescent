"""Expose the unsubmitted Equation research procedure and preserve existing approvals."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_LIBRARY_INVENTORY_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_RESEARCH_INTERFACE_01.json'
    delta=A/'EQUATION_RESEARCH_INTERFACE_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-equation-research-interface-01'
    assert all(not p.exists() for p in [checkpoint,delta,preserved])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    draft=R/'data/director/cosmology/equation_research_interface_draft_01.json'
    chapter=R/'docs/director-only/cosmology/EQUATION_RESEARCH_INTERFACE_DRAFT_01.md'
    citation=A/'COSMOLOGY_EQUATION_RESEARCH_INTERFACE_DRAFT_01_CHECK.json'
    c=read(citation);data=read(draft)
    assert c['draft']==info(draft) and c['chapter']==info(chapter)
    assert c['sourceBindingsVerified']==15 and c['exactEvidenceLocationsVerified']==61
    for row in data['sourceBindings']+data['contextArtifacts']:assert info(G/row['path'])==row
    for row in data['languageExactApprovalVerification']['currentFinalArtifactsMatched']:assert info(G/row['path'])==row
    planes=A/'DD_Cosmology_Planes_01.zip';assert info(planes)['sha256']=='158630558c141a69485c47bdfb727c8f29d1727bca1e78c45f01ac3944bd8fe5'
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json'
    nav=R/'tools/build_review_map.py';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert info(ledger_path)==state['coverageLedger']
    preservation=[]
    for p in [start,ledger_path,nav,current,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes();preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    scope=('Equation Research interface and Director worksheet prepared:9sections,11record fields,14worked situations;61exact source locations across15files verified. '
           'Existing LAX exact receipt and all7listed final artifact hashes match. Research is an expedition activity, not a21stbasic skill; the Core personal high-rank requirement across5disciplines still needs an explicit interpretation. '
           'Current translation, one-assistant deciphering, borrowed-skill, retained-information and work-clock rules remain unchanged. '
           'No numerical Equation qualification, functional-understanding threshold, fragment assignment, taint model or Hunt trigger adopted. '
           'Prior22record library inventory and12section20case souls/Hunt draft remain prepared. Part2 length limit is terminal; the existing Part3 choice is pending. '
           'Ordinary spells419reviewed429pending; latest verified GitHub18c6e3a, later work local.')
    old_start=start.read_text(encoding='utf-8');old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** [Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) and the [Q6 endgame review](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md) are saved. Prepared for joint discussion: the [souls/Hunt draft](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md), [22-record library inventory](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EQUATION_LIBRARY_SOURCE_INVENTORY_01.md), and [Equation Research procedure and worksheet](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EQUATION_RESEARCH_INTERFACE_DRAFT_01.md), whose 9 sections and 14 situations use 61 checked source locations. They add no adopted Equation or taint rules. The planes review reached [ChatGPT’s conversation-length limit](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json); the prepared Part 3 handoff awaits your already-requested choice. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_EQUATION_RESEARCH_INTERFACE_01.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    changed=old_start.replace(old_line,new_line,1);assert changed.replace(new_line,old_line,1)==old_start
    start.write_text(changed,encoding='utf-8',newline='\n')
    old_current=current.read_text(encoding='utf-8')
    addition='\nThe [Equation Research interface and Director worksheet](EQUATION_RESEARCH_INTERFACE_DRAFT_01.md) adds 9 discussion sections and 14 worked situations, with 61 exact evidence locations checked. The existing language review and its seven final artifact hashes remain intact. Research’s mapping to the 20-skill character system, personal high-rank qualifications and the threshold of functional Equation understanding remain explicit joint-review questions. Ordinary language, class, assistance and elapsed-work procedures are preserved.\n'
    current.write_text(old_current+addition,encoding='utf-8',newline='\n')
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-15','DD-46','DD-50','DD-61','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'equation-research-interface-01','recordedAtUtc':now,'draft':draft.relative_to(G).as_posix(),'citationCheck':citation.relative_to(G).as_posix(),'jointlyReviewed':False,'newRulesAdopted':False,'fullDomainClosed':False})
            row.setdefault('draftEvidence',[]).extend(p.relative_to(G).as_posix() for p in [draft,chapter])
            row.setdefault('validationEvidence',[]).append(citation.relative_to(G).as_posix())
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['status','closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "EQUATION_LIBRARY_INVENTORY_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "EQUATION_RESEARCH_INTERFACE_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]);text=text.replace(literal,repr(scope),1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+'        '+repr(('Equation Research — procedure/worksheet and 14 situations; joint review pending',citation.name))+',\n',1)
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
        cosmologyEquationResearchInterface={'status':'9-section proposed interface;11-field worksheet;14authored situations;unsubmitted','draft':info(draft),'chapter':info(chapter),'citationCheck':info(citation),'sourceBindingsVerified':15,'exactEvidenceLocations':61,'existingLaxFinalHashesVerified':7,'newRulesAdopted':False})
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions']=[
        'The existing Part3 choice remains pending; do not ask again or infer consent from elapsed time. If owner approves or supplies the continuation chat, preserve earlier chats and submit the prepared exact planes ZIP/handoff through Chrome CUA. No planes verdict exists.',
        'After planes completion, verify its returned source/citation/evidence package. Then prepare the souls/Hunt conference using the12section20case draft, four bounded reading records, current authored-status correction, actual source files and the current planes outcome.',
        'Use the22record library inventory and9section14case Research interface draft together for Equation development. Real library placement, clues and functional meaning still need authoring. Original-source priority remains settled; do not silently relocate cosmic sites or merge archive names.',
        'Resolve Research activity versus owner Research skill, Core personal high ranks across5disciplines, duration of qualifying competence, and functional-understanding/taint thresholds with GPT. Preserve actual language benefits and borrowed skill proficiency; temporary knowledge expiry does not erase particular learned information. Generic three-assistant rules do not override one-assistant deciphering.',
        'Independent next work: build the original-cosmology narrative chronology and current-campaign revelation comparison, particularly Academy/Citadel/Silent Library and the Q6 endgame boundary. Keep chronological reconciliation as a draft until joint discussion. Other pending full-game work remains available.',
        'Ordinary spells419reviewed429pending; use current authored_review_index, not pending legacy catalog alone. Soul Mirror is already reviewed-authored via candidate_low_rank_136.json /spells/124.',
        'Keep Hunt roster, trigger, taint arithmetic and exceptional intervention routes open. Do not reinstate the superseded absolute intervention ban or promote runtime/human balance/full-game flow. Latest verified GitHub18c6e3a; later work local. Owner monitors usage.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'delta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'ordinaryLanguageArtifactsUnchanged':7,'planesPacketUnchanged':True,'approvalStatusesUnchanged':True,'newRulesAdopted':False}))


if __name__=='__main__':main()
