"""Make the completed bounded origin comparison findable without closing cosmology."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,re,subprocess,sys
from urllib.parse import unquote
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_SOURCE_AND_COSMOLOGY_REVIEW.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json'
    delta=A/'CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json'
    preserved_root=A/'navigation-before-creation-origin-completion'
    assert all(not p.exists() for p in [checkpoint,delta,preserved_root])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    received=A/'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED_DECISION.json'
    app_path=A/'COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json';app=read(app_path)
    publication=A/'COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json';pub=read(publication)
    assert app['exactSummariesVerified']==4 and app['unresolvedDependenciesRetained']==11
    assert app['originalSourceHashesUnchanged']==34 and not app['fullCosmologyApproved']
    assert len(pub['patchAnchors'])==8 and not pub['publicProjectionCertified']
    for key in ['candidate','manuscript']:assert info(G/app[key]['path'])==app[key]
    start=G/'START_HERE.md';ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    scope=('Creation/origin actual GPT conference completed for nine comparisons. Four exact editorial summaries are assembled in a Director-only reading companion: two accepted unchanged and two reviewer replacements, with seven fact/belief/revelation rows and eleven unresolved dependencies retained. '
        'All34 source hashes remain unchanged; no general-cosmology authority, public export, identity merge or full cosmology approval. Actual current player-book bytes and both living extracts contain eight AppendixB patch anchors; full publication/audience review remains open. '
        'No GPT response is pending: creation review is terminal and preserved. Next ordered cosmology phase is gods/pantheons. Ordinary spells remain419/429; thirteen copy-release behavioral examples remain unexecuted. Latest measured weekly usage17percent; owner stop50. Latest pushed backup80944e0 precedes this local work.')
    old_start=start.read_text(encoding='utf-8');lines=[x for x in old_start.splitlines() if x.startswith('**Current joint review:**')];assert len(lines)==1
    new_line='**Current joint review:** Ordinary spells remain **419 reviewed / 429 pending**. The [copy-release source rulings are applied](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json), with 13 behavioral examples still required. GPT completed the first cosmology authority pass and the nine-part origin comparison. The [reviewed creation/origins companion](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CREATION_ORIGINS_REVIEWED_01.md) preserves 11 unresolved dependencies and all original source words. [Current publication checks](docs/audit/2026-10-08/full-game/COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json) verify eight Appendix B patch anchors without certifying the full book. No GPT reply is pending; gods/pantheons is the next cosmology comparison. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json). Latest measured weekly usage is 17%; stop at **50%**.'
    new_start=old_start.replace(lines[0],new_line,1);assert new_start.replace(new_line,lines[0],1)==old_start
    before=read(ledger_path);ledger=deepcopy(before)
    touched={'DD-50','DD-61','DD-65','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'creation-origin-review-completed','recordedAtUtc':now,'receivedDecision':received.relative_to(G).as_posix(),'application':app_path.relative_to(G).as_posix(),'publicationEvidence':publication.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [received,app_path,publication,G/app['manuscript']['path']])
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in touched:assert old==new
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "COPY_SOURCE_COSMOLOGY_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json")["changes"]\n')
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1 and isinstance(nodes[0],ast.Constant)
    literal=ast.get_source_segment(text,nodes[0]);assert text.count(literal)==1;text=text.replace(literal,repr(scope),1)
    old='("Creation/origins — nine comparisons submitted to GPT", "COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json")'
    new='("Creation/origins — nine comparisons reviewed, eleven open dependencies", "COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json")'
    assert text.count(old)==1;text=text.replace(old,new,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+'        ("Current player publication — eight patch anchors verified", "COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json"),\n')
    compile(text,str(nav),'exec')
    preservation=[]
    for p in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved_root/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
        preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved_root/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    start.write_bytes(new_start.encode());ledger_path.write_bytes(encoded(ledger));nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger_path,nav]]
    changes[0].update(operations=[{'old':lines[0],'replacement':new_line}],inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newEditorialFiles':[app['candidate'],app['manuscript']],'sourceInformationDeleted':0,'cosmologyDoctrineChanged':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append({'historicalSubmission':state['activeGptReview'],'terminalDecision':info(received),'derivedEditorialApplication':info(app_path)})
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageLedger=info(ledger_path),coverageDelta=info(delta),activeGptReview=None,cosmologyCreationReview={'status':'terminal-reviewed-scoped-editorial-companion-assembled','receipt':info(received),'application':info(app_path),'manuscript':app['manuscript'],'openDependencies':11},cosmologyPublicationEvidence=info(publication),cosmologyReviewed=False,cosmologyReviewScope='Authority findings and creation/origins scoped comparison completed; full cosmology remains open.',usageAtLatestCheck={'usedPercent':17,'windowDurationMins':10080,'stopAtUsedPercent':50},navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['safeNextActions']=['Check weekly usage periodically and before substantial work; stop at50percent, preserve a checkpoint and pause under the owner instruction.','Actual GPT creation/origin conference is terminal and preserved. No request is pending. Browser observation recovered after transient timeouts; do not resend either completed conference.','Prepare the gods/pantheons comparison from the complete original later divine passages, current AppendixB counterparts, exact player-book bytes and living extracts from publication-source-check-01, applicable registered domains and identity-asserting class passages. Include original P56 infernal-roster conflict and exact authority of seven Choir names.','Preserve the eleven origin dependencies; do not invent why the Heartcell was built, how it became its builders’ prison, a Sundering/Pact chronology, cosmic cycle units, missing WorldI–VI or merged endgame identities.','Implement/validate the thirteen copy-release behavioral examples from actual paid acquisition/capture histories. The existing provider adapter covers Wizard and feat-only rank0; Shaman/Mirrorsage qualification, actual shared release allowance, Ready, concentration effects and cross-route history require genuine integration, not class-name labels or source-string checks.','Continue429 remaining ordinary spells and all other open game systems. Whole-game joint flow, full runtime, human playtesting, balance and publication gates remain open.','Latest remote backup80944e0 precedes the received cosmology reviews and this checkpoint. Subsequent work remains local pending further authorized delivery.']
    state.setdefault('preservationManifests',[]).append(info(preserved_root/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    checked=0
    for target in re.findall(r'\]\(([^)]+)\)',new_line):
        if '://' in target:continue
        p=(G/unquote(target)).resolve();assert p.is_relative_to(G.resolve()) and p.is_file();checked+=1
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'changedLinksVerified':checked,'pendingGptReviews':0,'cosmologyComplete':False}))

if __name__=='__main__':main()
