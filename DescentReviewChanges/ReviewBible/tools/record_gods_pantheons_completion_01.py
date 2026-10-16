"""Record completed scoped gods review and the next genuine source dependencies."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, hashlib, json, subprocess, sys, zipfile, xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(path): return json.loads(path.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_FOLLOWUP_SUBMISSION.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_REVIEW.json'
    delta=A/'GODS_PANTHEONS_COMPLETION_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-gods-pantheons-completion-01'
    director_check=A/'COSMOLOGY_DIRECTOR_INTERSTICE_SOURCE_CHECK_01.json'
    assert all(not p.exists() for p in [checkpoint,delta,preserved,director_check])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    received=A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RECEIVED_DECISION.json'
    application=A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_APPLICATION_CHECK.json';app=read(application)
    assert app['exactSummariesVerified']==4 and app['uniqueParagraphCitationsVerified']==157
    assert app['originalSourceHashesUnchanged']==71 and not app['fullCosmologyApproved']
    for key in ['candidate','manuscript']: assert info(G/app[key]['path'])==app[key]
    n='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    director_paths=[G/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx',R/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx']
    paragraphs=[]
    for path in director_paths:
        with zipfile.ZipFile(path) as z:xml=ET.fromstring(z.read('word/document.xml'))
        paragraphs.append([''.join(t.text or '' for t in p.iter(n+'t')) for p in xml.iter(n+'p')])
    assert paragraphs[0][1467:1499]==paragraphs[1][1481:1513]
    assert paragraphs[0][2380:2397]==paragraphs[1][2406:2423]
    cited=[78,120,290,479,746,1093,1266,1278,1370]
    def exact(which,indices):return [{'part':'word/document.xml','paragraphIndexZeroBased':i,'text':paragraphs[which][i],'textSha256':hashlib.sha256(paragraphs[which][i].encode()).hexdigest()} for i in indices]
    director_check.write_bytes(encoded({
        'checkId':'COSMOLOGY-DIRECTOR-INTERSTICE-SOURCE-CHECK-01','recordedAtUtc':now,
        'sources':[info(p) for p in director_paths],
        'semanticRead':'Main Director chapter34 P1467-P1498 and chapter65 P2380-P2396; exact paired ReviewBible passages compared equal. Adjacent chapter66 context P2397-P2406 also read, not a full Director-book rereview.',
        'mainChapter34':exact(0,range(1467,1499)),'mainChapter65':exact(0,range(2380,2397)),
        'reviewCounterpartRanges':[[1481,1512],[2406,2422]],
        'earlierGptDirectorCoveragePositionsActualText':exact(0,cited),
        'findings':[
            'The Director explicitly distinguishes the playable Interstice between Tiers7/8 from the unanswered World Floor97 myth (mainP1494-P1495 and P3207).',
            'Main and ReviewBible editions differ elsewhere; their matching Interstice sections do not make the full files interchangeable.',
            'The earlier GPT coverage list P78/P120/P290/P479/P746/P1093/P1266/P1278/P1370 is not generally a hierarchy citation set under exact XML numbering. P746 is Interstice material; other selected positions concern party organization, encounters or hazards. Do not rely on that old claim as full Director cosmology review.',
            'WORLD_DUNGEON_LOOP WDL-4 contains a claimed resolved Floor97 chamber lock that conflicts with the explicit unanswered Q6/current Director placeholder. Establish the actual authority of that legacy annotation before any use; do not treat a status label alone as a new owner directive.',
        ],
        'furtherSources':[info(R/'docs/mechanics/WORLD_DUNGEON_LOOP.md'),info(G/'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md')],
        'sourceInformationDeleted':0,'originalSourcesModified':False,'newOwnerRulingCreated':False,
    }))
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    scope=('Gods/pantheons scoped conference and correction follow-up completed. The Director reading companion contains four exact summaries, nine GP decisions, eight GPR follow-up dispositions and17dependencies. '
           'All316 citation occurrences across157unique paragraphs match original Word text hashes and normalized excerpts; all71 original source hashes remain unchanged. '
           'The prior return and its bad citation sets remain preserved. No full cosmology/general-domain/class-mechanics/public-export approval. '
           'No GPT response is pending. Next: planes, using the32-label/ten-row preliminary concordance and actual spell dependencies, followed by souls/death/resurrection, history, divine/class powers and campaign revelations. '
           'Current Director sources retain Q6/Interstice distinctions; the legacy World/Dungeon annotation needs authority reconciliation. '
           'Ordinary spells remain419reviewed/429pending; copy-release13behavioralexamples remain pending. Latest verified backup18c6e3a precedes this work. Owner is monitoring usage; prior50percentstop revoked.')
    old_start=start.read_text(encoding='utf-8');old=[s for s in old_start.splitlines() if s.startswith('**Current joint review:**')];assert len(old)==1
    line='**Current joint review:** Ordinary spells remain **419 reviewed / 429 pending**. GPT completed the gods/pantheons conference and correction follow-up. The [reviewed gods/pantheons companion](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/GODS_PANTHEONS_REVIEWED_01.md) contains four summaries, nine decisions, eight follow-up findings and 17 retained dependencies. [Local verification](docs/audit/2026-10-08/full-game/COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_APPLICATION_CHECK.json) matched 316 citation occurrences and all 71 original source hashes. No GPT reply is pending. [Planes is next](docs/audit/2026-10-08/full-game/COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json); full cosmology and whole-game approval remain open. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_REVIEW.json). Latest verified GitHub backup is 18c6e3a; this work is local. **The owner withdrew the 50% usage stop and is monitoring usage directly.**'
    new_start=old_start.replace(old[0],line,1);assert new_start.replace(line,old[0],1)==old_start
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-50','DD-61','DD-65','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'gods-pantheons-completed-01','recordedAtUtc':now,'application':application.relative_to(G).as_posix(),'receivedDecision':received.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [received,application,director_check,G/app['manuscript']['path']])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "GODS_FOLLOWUP_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "GODS_PANTHEONS_COMPLETION_01_NAVIGATION_DELTA.json")["changes"]\n')
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]);assert text.count(literal)==1;text=text.replace(literal,repr(scope),1)
    replacements={
        repr(('Gods/pantheons — returned evidence; correction follow-up pending','COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json')):repr(('Gods/pantheons — original returned evidence, superseded by corrected successor','COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json')),
        repr(('Gods/pantheons — follow-up sent once','COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_SUBMISSION.json')):repr(('Gods/pantheons — corrected companion verified; seventeen dependencies','COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_APPLICATION_CHECK.json')),
    }
    for a,b in replacements.items():assert text.count(a)==1;text=text.replace(a,b,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+'        '+repr(('Current Director Interstice — exact counterpart/source check',director_check.name))+',\n')
    compile(text,str(nav),'exec')
    preservation=[]
    for path in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/path.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes());assert dest.read_bytes()==path.read_bytes()
        preservation.append({**info(path),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    start.write_bytes(new_start.encode());ledger_path.write_bytes(encoded(ledger));nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==path.relative_to(G).as_posix()),'after':info(path)} for path in [start,ledger_path,nav]]
    changes[0].update(operations=[{'old':old[0],'replacement':line}],inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'cosmologyDoctrineChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append({'historicalSubmission':state['activeGptReview'],'terminalDecision':info(received),'derivedEditorialApplication':info(application)})
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',
        activeGptReview=None,coverageLedger=info(ledger_path),coverageDelta=info(delta),
        cosmologyGodsPantheonsReview={'status':'terminal; corrected scoped companion assembled','receipt':info(received),'application':info(application),'manuscript':app['manuscript'],'unresolvedDependencies':17},
        cosmologyDirectorIntersticeSourceCheck=info(director_check),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['safeNextActions']=[
        'Both gods/pantheons requests are terminal and preserved. Do not resend either. The exact corrected Director companion is assembled; its17dependencies and all earlier origin gaps remain open within their recorded scopes.',
        'Continue the planes conference from COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01 and the Director Interstice source check. Read relevant Matrix plane/crossing passages and actual transit/summoning operations/receipts, including Blink, before sending the source-complete comparison.',
        'The owner is developing origins in another Chrome conversation. Inspect actual completed owner directions before making dependent cosmology changes; do not promote an assistant recommendation or an unsent draft to an owner lock. Preserve the separate live user tab and draft.',
        'Carry the ordered remaining reviews: planes; souls/death/resurrection; history; divine/class powers; campaign revelations. Do not supply missing WorldI–VI, missing formulas, a Serit bridge, Maladomini ruler, campaign epoch or endgame identity merger without adequate authority.',
        'Continue the13 copy-release behavioral examples,429 remaining ordinary spells and all other open systems. The preliminary spell-name screen is discovery only, not74 operational reviews or a complete dependency proof.',
        'Owner withdrew the50percent usage cutoff and monitors usage directly. Keep working within the active goal; do not pause under the superseded limit.',
        'Latest verified GitHub backup18c6e3a precedes the completed follow-up and this checkpoint. No subsequent push has been performed.',
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'directorSourceCheck':info(director_check),'navigationDelta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'pendingGptRequests':0,'fullCosmologyApproved':False}))


if __name__=='__main__':main()
