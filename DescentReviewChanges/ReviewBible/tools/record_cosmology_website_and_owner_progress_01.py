"""Checkpoint owner adoption, the actual saved website, and pending Q6 conference."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_RECONCILIATION_SUBMISSION.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_ADOPTION_AND_WEBSITE_SOURCE.json'
    delta=A/'OWNER_ADOPTION_WEBSITE_SOURCE_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-owner-adoption-website-source-01'
    assert all(not p.exists() for p in [checkpoint,delta,preserved])
    assert not (A/'COSMOLOGY_Q6_LATER_LOCK_01_RECEIVED_DECISION.json').exists(),'Use a terminal-review checkpoint if Q6 finishes first.'
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    adopted=A/'COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json';ad=read(adopted)
    assert ad['exactOwnerQuotesVerified']==11 and ad['docxCitationOccurrencesVerified']==34
    website=A/'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json';web=read(website)
    assert len(web['companionWebsite']['firstSongChapterSourceComparisons'])==12
    for row in web['sourceBindings']:assert info(G/row['path'])==row
    submitted=A/'COSMOLOGY_Q6_LATER_LOCK_01_SUBMISSION.json';sent=read(submitted);assert sent['submittedOnce']
    recovery=A/'COSMOLOGY_Q6_LATER_LOCK_01_RECOVERY_CONTINUATION.json';assert read(recovery)['recoveryContinuationCount']==1
    scope=('The actual GPT owner reconciliation is received, checked and applied to Director companions and a preserved revision of derived CANON_CORE: 11 exact owner statements, 34 DOCX citations, 24 non-DOCX evidence records classified. '
           'Thirteen dependencies remain, including the pending human clarification of Use the original version versus the quoted Director-builder account. '
           'A focused Q6 later-lock conference was submitted once with 28 sources and eight issues. After a persistent connection interruption, one continuation was sent using the same attachment; GPT acknowledged and resumed. Its response is not yet terminal or adopted. The registered August 5 crystal path and failed-Sixth-Gate public boundary must be distinguished from the still-open identity and full encounter rules. '
           'The owner reminded us of the saved website. webpage.html is Interactive Cosmology; the full viewer code, seven plane summaries, and World I–VI placeholder were inspected. All 12 website FirstSong bodies match contiguous original DOCX text after whitespace normalization. This does not recover missing World I–VI. The three website files exactly match the last pushed Git blobs. '
           'Planes preparation now includes 31 Director paragraphs, two frozen Blink receipt-only dispositions, 12 pending cards and six reviewed counterpart cards. A preparation script adds the saved website as PL-11; no planes packet has yet been built or submitted. '
           'Ordinary spells remain 419 reviewed / 429 pending; no spell flags, runtime or whole-game approvals changed. Original sources and prior receipts preserved. Latest GitHub backup18c6e3a; later work local; owner monitors usage.')
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    original=start.read_text(encoding='utf-8');old=[x for x in original.splitlines() if x.startswith('**Current joint review:**')];assert len(old)==1
    line='**Current joint review:** The [eleven owner cosmology corrections are reviewed and applied](docs/audit/2026-10-08/full-game/COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json), with Heartcell authorship still conditional on your pending clarification. The saved [interactive cosmology website](webpage.html) and companion are now explicitly [included in the source audit](docs/audit/2026-10-08/full-game/COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json). GPT’s [focused Q6 later-lock review](docs/audit/2026-10-08/full-game/COSMOLOGY_Q6_LATER_LOCK_01_SUBMISSION.json) is pending. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_ADOPTION_AND_WEBSITE_SOURCE.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    new=original.replace(old[0],line,1);assert new.replace(line,old[0],1)==original
    before=read(ledger_path);ledger=deepcopy(before);touched={'DD-50','DD-61','DD-65','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'owner-adoption-website-source-01','recordedAtUtc':now,'adoption':adopted.relative_to(G).as_posix(),'websiteAudit':website.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [adopted,website,submitted,A/'COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json',A/'COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json'])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "OWNER_RECONCILIATION_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "OWNER_ADOPTION_WEBSITE_SOURCE_01_NAVIGATION_DELTA.json")["changes"]\n')
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]);assert text.count(literal)==1;text=text.replace(literal,repr(scope),1)
    marker='    pending = [\n';assert text.count(marker)==1
    links=[('Owner cosmology corrections — reviewed and applied',adopted.name),('Saved cosmology website — source audit and backup verification',website.name),('Q6 later lock — focused review submitted once',submitted.name),('Planes preparation — Director context and frozen Blink receipts','COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json'),('Planes preparation — six reviewed counterpart cards','COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json')]
    text=text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in links),1);compile(text,str(nav),'exec')
    preservation=[]
    for p in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes();preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    start.write_bytes(new.encode());ledger_path.write_bytes(encoded(ledger));nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger_path,nav]]
    changes[0].update(operations=[{'old':old[0],'replacement':line}],inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'cosmologyDoctrineChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',activeGptReview={'reviewId':sent['reviewId'],'status':'same review resumed after one recovery continuation; terminal result pending','submission':info(submitted),'recovery':info(recovery),'conversationUrl':sent['conversationUrl'],'tabId':sent['tabId']},coverageLedger=info(ledger_path),coverageDelta=info(delta),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['ownerCosmologyCorrections'].update(status='reviewed and applied within stated scope',adoption=info(adopted),received=info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_RECEIVED_DECISION.json'),candidate=info(R/'data/director/cosmology/owner_reconciliation_reviewed_01.json'),companion=info(R/'docs/director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md'),readingOrder=info(R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'),remainingDependencies=13)
    state['savedCosmologyWebsite']=info(website)
    state['planesPreparationSuccessors']={k:info(A/v) for k,v in {'reviewedCounterparts':'COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json','directorAndReceipts':'COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json','website':'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json'}.items()}
    state['safeNextActions']=[
        'Continue the existing Q6 later-lock request in Calibration Review Part2 without duplicate submission. One source upload and one recovery continuation are recorded. After a failed reconnect and stopping the stalled response, GPT visibly acknowledged the continuation and resumed the same eight issues. Preserve and verify its terminal answer before adoption; partial earlier code is not final evidence.',
        'Keep the pending human Heartcell-builder/source-priority question open. The reviewed eleven corrections are already applied; no need to rerun their one-use scripts.',
        'After Q6 is verified, write a precise successor Director companion and current reading pointer; preserve prior sources and receipts. Distinguish locked path/public ceiling from identity, full stats and encounter-mapping gaps. Do not claim prior source-authority review entirely missed later locks.',
        'Run prepared tools/prepare_cosmology_planes_01.py only after the expected Q6 receipt, application check and companion files exist; it has not run. It includes all saved website files as PL-11. Review website labels/diagram statements with GPT as source evidence before additional cosmology adoption.',
        'Website source is webpage.html, src/components/CosmologyViewer.tsx and src/data/cosmology-lore.json. Three exact files already backed up at18c6e3a. All12FirstSong bodies match originalDOCX after whitespace normalization; WorldI–VI placeholder is not recovery evidence. Browser rendering has not been tested.',
        'Remaining ordered scopes: planes; souls/death/resurrection; history; divine/class powers; campaign revelations. All ordinary spell/feat/runtime/human-playtest scopes stay open.',
        'Owner monitors usage; prior50percentcutoff revoked. Latest verified GitHub backup18c6e3a; subsequent work local. Preserve all originals and prior receipts.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationDelta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'pendingGptRequests':1,'ownerCorrectionsApplied':11,'websiteChaptersMatchedToOriginal':12,'sourceInformationDeleted':0}))


if __name__=='__main__':main()
