"""Update navigation for the exact owner corrections and pending actual GPT review."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_REVIEW.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_RECONCILIATION_SUBMISSION.json'
    delta=A/'OWNER_RECONCILIATION_SUBMISSION_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-owner-reconciliation-submission-01'
    assert all(not p.exists() for p in [checkpoint,delta,preserved])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    submission=A/'COSMOLOGY_OWNER_RECONCILIATION_01_SUBMISSION.json'; sent=read(submission)
    assert sent['submittedOnce']
    for row in read(A/'cosmology-owner-reconciliation-01/CURRENT_SOURCE_BINDINGS.json'): assert info(G/row['path'])==row
    start=G/'START_HERE.md'; ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    scope=('Eleven exact submitted owner corrections from Resolve Heartcell Origins are preserved; source-complete COSMOLOGY-OWNER-RECONCILIATION-01 was sent once to Calibration Review Part2 and awaits a terminal reply. '
           'A later Use the original version message quotes the contrary Director-builder account; Codex asked the human which source controls. That clarification remains pending, and GPT interpretation is not owner confirmation. '
           'No dependent authorship decision has been adopted. Unambiguous corrections include no essence tether and Mephistopheles only Cania. '
           'Source probe inspected10096paths/4983uniquecontents/63uniqueDOCX; encoding addendum resolves9decodeerrors and checks15distinctencodedtexts. No literal Harmony-author/reference hit; four World DOCX copies match the same missing-I–VI placeholder. '
           'Twelve relevant ZIP central directories checked; no missing World chapter recovered. This is a bounded search, not proof of universal absence. '
           'Transit dependency reading covers12wholecatalogcards,2unadoptedprocedures and MatrixP87–140; no spell promotion. Ordinary spells remain419reviewed/429pending. '
           'All prior originals/receipts preserved; fullcosmology/gameapprovalfalse. LatestGitbackup18c6e3a; laterworklocal; owner monitorsusage.')
    old_text=start.read_text(encoding='utf-8'); old=[x for x in old_text.splitlines() if x.startswith('**Current joint review:**')];assert len(old)==1
    line='**Current joint review:** Your eleven new cosmology corrections are [preserved exactly](docs/audit/2026-10-08/full-game/COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_MESSAGE_CAPTURE.json). GPT is reviewing the [source reconciliation packet](docs/audit/2026-10-08/full-game/COSMOLOGY_OWNER_RECONCILIATION_01_SUBMISSION.json). One later source-priority instruction is awaiting your clarification; dependent authorship changes remain open. The bounded source search did not recover World of Aethel I–VI. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_RECONCILIATION_SUBMISSION.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    new_text=old_text.replace(old[0],line,1);assert new_text.replace(line,old[0],1)==old_text
    before=read(ledger_path); ledger=deepcopy(before); touched={'DD-50','DD-61','DD-65','DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'owner-reconciliation-submitted-01','recordedAtUtc':now,'submission':submission.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend((A/n).relative_to(G).as_posix() for n in ['COSMOLOGY_OWNER_RECONCILIATION_01_SUBMISSION.json','COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json','COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json','COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json'])
    for a,b in zip(before['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if a['id'] not in touched:assert a==b
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "GODS_PANTHEONS_COMPLETION_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "OWNER_RECONCILIATION_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n')
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    literal=ast.get_source_segment(text,nodes[0]);assert text.count(literal)==1;text=text.replace(literal,repr(scope),1)
    marker='    pending = [\n';assert text.count(marker)==1
    links=[('Owner corrections — source reconciliation sent once',submission.name),('Owner source priority — exact message; human clarification pending','COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CAPTURE.json'),('Source search — encoding recovery; nine errors resolved','COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json'),('Source search — twelve archive indexes','COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json'),('Planes preparation — twelve transit cards and two unadopted procedures','COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json')]
    text=text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in links),1);compile(text,str(nav),'exec')
    preservation=[]
    for path in [start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/path.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes());assert dest.read_bytes()==path.read_bytes()
        preservation.append({**info(path),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    start.write_bytes(new_text.encode());ledger_path.write_bytes(encoded(ledger));nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==path.relative_to(G).as_posix()),'after':info(path)} for path in [start,ledger_path,nav]]
    changes[0].update(operations=[{'old':old[0],'replacement':line}],inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'cosmologyDoctrineChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',activeGptReview={'reviewId':sent['reviewId'],'status':'submitted-once-response-pending','submission':info(submission),'conversationUrl':sent['conversationUrl'],'tabId':sent['tabId']},coverageLedger=info(ledger_path),coverageDelta=info(delta),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},ownerStartPage=info(start))
    state['ownerCosmologyCorrections']={'capture':info(A/'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_MESSAGE_CAPTURE.json'),'proposedRegister':info(A/'cosmology-owner-reconciliation-01/OWNER_CORRECTION_REGISTER_PROPOSED.json'),'laterSourcePriority':info(A/'COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CAPTURE.json'),'sourcePriorityClarification':'Pending human answer: original manuscripts with corrections versus quoted Director Silent-Ones-builder account; GPT cannot decide the referent.','dependentAuthorshipAdoption':False}
    state['cosmologySourceRecovery']={k:info(A/v) for k,v in {'probe':'cosmology-owner-reconciliation-01/LOCAL_SOURCE_PROBE.json','encoding':'COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json','archives':'COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json','transitReading':'COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json'}.items()}
    state['safeNextActions']=[
      'Continue the existing pending COSMOLOGY-OWNER-RECONCILIATION-01 request; do not resend. Download and preserve its terminal evidence, verify exact owner quotes/source hashes/citations, and adopt only supported scope. A DOM or screenshot timeout alone is not completion or lost browser state.',
      'Keep the exact later source-priority question pending until a human answer. Do not accept the other GPT chat interpretation as confirmation. Other source comparison and unambiguous corrections can proceed.',
      'World I–VI remains unrecovered in the bounded search. Four named original DOCX copies are identical. No literal Harmony reference found in checked text/DOCX; external seven-principle list is context, not a Choir mapping. No invented cycle unit, essence tether, Shardspire origin, Floor97 merger, Maladomini replacement, missing formula or chapter recovery.',
      'Continue planes from the concordance and new transit dependency reading after owner correction reconciliation. Current 12 read cards remain operationally null, two detailed transport drafts unadopted. Review local accepted counterparts and expedition boundary rules before any mechanical conclusion.',
      'Remaining ordered cosmology scopes: planes; souls/death/resurrection; history; divine/class powers; campaign revelations. All other spell/feat/runtime/human-playtest scopes stay open.',
      'Owner monitors usage; prior50percentcutoff revoked. Latest verified GitHub backup18c6e3a; subsequent source work is local. Preserve all originals and prior receipts.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationDelta':info(delta),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'pendingGptRequests':1,'dependentAuthorshipAdoption':False,'sourceInformationDeleted':0}))


if __name__=='__main__':main()
