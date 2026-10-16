"""Preserve navigation and record chronology source work, reader checks and live route integration."""
from datetime import datetime, timezone
from copy import deepcopy
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_CHRONOLOGY_01.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_READER_01.json'
    delta = A / 'CHRONOLOGY_READER_01_NAVIGATION_DELTA.json'
    preserved = A / 'navigation-before-chronology-reader-01'
    receipt = A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_SUBMISSION_RECEIPT.json'
    followup = A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_FOLLOWUP_SUBMISSION_RECEIPT.json'
    semantic = A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_REVISED_SEMANTIC_AUDIT.json'
    assert all(not p.exists() for p in [target, delta, preserved, receipt, followup, semantic])
    now = datetime.now(timezone.utc).isoformat(); state = read(previous)
    source_app = A / 'COSMOLOGY_CHRONOLOGY_SOURCE_01_APPLICATION_CHECK.json'
    reader_app = A / 'COSMOLOGY_COMPANION_READER_01_APPLICATION_CHECK.json'
    source = read(source_app); reader = read(reader_app)
    assert source['failures'] == 0 and reader['failureCount'] == 0
    for kind, dest, request_name in [
        ('FOLLOWUP', followup, 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_FOLLOWUP_REQUEST.txt'),
        ('INTEGRATION', receipt, 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_REQUEST.txt')]:
        dom = A / f'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_{kind}_SUBMISSION_DOM.txt'
        assert 'button "Stop"' in dom.read_text(encoding='utf-8')
        dest.write_bytes(encoded({'recordedAtUtc': now, 'reviewId': 'COSMOLOGY-CHRONOLOGY-RESEARCH-ROUTE-01',
          'statusAtSubmission': 'sent once; GPT responding in the observed Part3 conversation',
          'conversationUrl': state['activeGptReview']['conversationUrl'], 'tabId': '125746244',
          'request': info(A / request_name), 'submissionDom': info(dom),
          'screenshot': info(A / f'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_{kind}_SUBMISSION.png'),
          'sourceArchive': info(A / 'DD_Cosmology_Chronology_Research_Route_01.zip'),
          'frozenSourceCount': 83, 'newRouteRulesAdopted': False, 'sourceInformationDeleted': 0}))
    issues = [
      ('CR-I01', 'RR05 10-minute access vs20-minute task; captive key vs fractured spare', 'Mechanical catch proposal; source draft not applied.'),
      ('CR-I02', 'Stable-only test cannot prove convergence/abort', 'Two actual settings, timings, observed outcomes and real abort window requested.'),
      ('CR-I03', 'Single preliminary test must not certify KT3', 'All3 settled tests after the model; actual acquisition vs later episode save.'),
      ('CR-I04', 'No actual pre/post values and ambiguous cooling-bell phase', 'Finite values and11h20 next-opening arithmetic; missed-window correction.'),
      ('CR-I05', 'Wrong CA-W4 lineage and unsupported in-world premise/rubrics', 'Actual handouts, provenance, authentication clocks and truthful outcomes.'),
      ('CR-I06', 'Incomplete route and borrowed-proficiency schedules', 'Two-beneficial-Short-Rest limit; all10findings; legal two-day loan example.'),
      ('CR-I07', 'DC rationale and incomplete degree outcomes', 'Current15/20 rationale, success included in critical success, actual hazards or none.'),
      ('CR-I08', 'Alternate library does not replace the missing findings', 'Finite separately maintained collection and explicit authored substitute path.'),
      ('CR-I09', 'Access outcomes/recovery remain conditional', 'Complete mandatory noncombat route and finite failure/recovery branch.'),
      ('CR-I10', 'Ordinary reader exposed unreconciled original prose', 'Agreed reader boundary locally implemented and narrowly browser-checked; full runtime still open.')]
    semantic.write_bytes(encoded({'recordedAtUtc': now, 'reviewedArchive': info(A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Revised_Addendum_and_Evidence.zip'),
      'sourceCheck': info(A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_revised.json'),
      'sourceChecks': 263, 'sourceFailures': 0,
      'readScope': 'Full revised chapter; all6nodes, handouts,10findings,3tests, schedules, taint rules,12newcases and8integration dispositions.',
      'findings': [{'id': i, 'problem': p, 'disposition': d} for i,p,d in issues],
      'currentOutcome': 'Route remains a proposal pending semantic integration; source integrity does not prove playability.',
      'request': info(A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_REQUEST.txt'),
      'readerApplication': info(reader_app), 'newRouteRulesAdopted': False, 'sourceInformationDeleted': 0}))
    start = G / 'START_HERE.md'; guide = R / 'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav = R / 'tools/build_review_map.py'; ledger = R / 'data/playtest/game_development_coverage.json'
    originals = {}; pres = []
    for p in [start, guide, nav, ledger, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes(); dest = preserved/p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(raw)
        originals[p] = raw; pres.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    scope = 'Chronology source reference saved:16relative events/17EPIplanning groups; no epoch/date/identity choice. Reader selection/qualified timeline implemented locally,21recorded checks and TypeScript pass, source text preserved. Revised route263source checks pass but10semantic integration issues sent to actual GPT Part3; operating route not adopted. Souls candidate remains current. Ordinary spells419reviewed429pending. Latest GitHub18c6e3a; later work local.'
    old_start = originals[start].decode('utf-8'); old_line = next(s for s in old_start.splitlines() if s.startswith('**Current joint review:**'))
    new_line = '**Current joint review:** The [chronology source reference](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_SOURCE_REVIEWED_01.md) is saved, preserving both dates and unresolved identities. The [local companion reader changes](docs/audit/2026-10-08/full-game/COSMOLOGY_COMPANION_READER_01_APPLICATION_CHECK.json) are verified; original lore remains intact. GPT Part 3 is integrating [ten concrete research-route corrections](docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_SUBMISSION_RECEIPT.json); that operating route is **not yet adopted**. Use the [current cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_READER_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame, remaining lore and full-game validation remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(old_line, new_line, 1), encoding='utf-8', newline='\n')
    old_guide = originals[guide].decode('utf-8'); paragraphs = old_guide.split('\n\n'); replaced = 0
    for i, para in enumerate(paragraphs):
        if para.startswith('The [chronology and library-route conference]'):
            paragraphs[i] = 'The [chronology source reference](CHRONOLOGY_SOURCE_REVIEWED_01.md) now preserves16relative events and17epilogue planning groups, with250source checks. Both87AE/710AE dates remain; no prospective710AE scheduling convention, campaign frame, identity merge or epilogue mechanic was adopted. The owner question about before/during/after the Proof War remains pending.'; replaced += 1
        elif para.startswith('For that work, use the [chronology/source comparison]'):
            paragraphs[i] = 'The [research-route integration](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_SUBMISSION_RECEIPT.json) is active in the same Part3 chat. The revised return passes263source/file/location checks, but its [semantic audit](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_REVISED_SEMANTIC_AUDIT.json) identifies ten concrete corrections: key access timing, observable test outcomes, the three-test KT3 gate, local-window phase, evidence/authentication, real work/rest schedules, DC outcomes, alternate-library findings and access recovery. The proposed Floor68 placement, clues, mechanics and route remain unadopted. The [earlier comparison](CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md) is preserved history.'; replaced += 1
        elif para.startswith('The [library inventory]'):
            paragraphs[i] = para.replace('Two-library route slots in the new operating model still need actual scene/clue authorship.', 'The revised route has authored holdings and scenes, but its operational integration remains under review; proposed Floor68 Wax geography is not an original source fact.')
    assert replaced == 2
    paragraphs.insert(-1, 'The [companion reader application](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_COMPANION_READER_01_APPLICATION_CHECK.json) implements the agreed presentation boundary locally: ordinary cosmology context and qualified dates, with deliberate access to the preserved original reader/timeline and separate review notes.21recorded checks, three successful TypeScript runs and actual browser traversals support this narrow change. The existing draft-badge invalid nesting was fixed. Source JSON and original reader body remain unchanged. This is not authentication, publication, or a full companion/runtime approval; other deep-floor listings remain outside this change.')
    guide_text = '\n\n'.join(paragraphs); guide.write_text(guide_text, encoding='utf-8', newline='\n')
    coverage = json.loads(originals[ledger]); before_coverage = deepcopy(coverage); row = next(x for x in coverage['aspects'] if x['id']=='DD-50'); before_row = deepcopy(row)
    for key, paths in [('reviewEvidence', [source['chapter']['path'], source['data']['path'], semantic.relative_to(G).as_posix()]), ('validationEvidence', [source_app.relative_to(G).as_posix(), reader_app.relative_to(G).as_posix(), receipt.relative_to(G).as_posix()])]:
        for name in paths:
            if name not in row[key]: row[key].append(name)
    row['completedScopes'].append('Chronology source comparison saved without date/epoch/identity changes; narrow companion reader selection implemented and browser-checked with original text preserved. Revised research route remains pending10semantic integration corrections; source integrity alone does not close it.')
    row['currentEvidenceAddenda'].append({'id':'chronology-reader-01','recordedAtUtc':now,'chronologySource':source_app.relative_to(G).as_posix(),'readerApplication':reader_app.relative_to(G).as_posix(),'routeIntegration':receipt.relative_to(G).as_posix(),'newRouteRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']: assert row[k] == before_row[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50'] == [x for x in before_coverage['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    text = originals[nav].decode('utf-8'); tail = ' + read(A / "SOULS_CHRONOLOGY_01_NAVIGATION_DELTA.json")["changes"]\n'; assert text.count(tail)==1
    text = text.replace(tail, tail.rstrip('\n')+' + read(A / "CHRONOLOGY_READER_01_NAVIGATION_DELTA.json")["changes"]\n', 1)
    nodes = [v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']; assert len(nodes)==1
    text = text.replace(ast.get_source_segment(text,nodes[0]), repr(scope), 1)
    entries = [('Research route — ten concrete integration corrections sent to GPT', receipt.name), ('Research route — revised semantic audit, not adoption', semantic.name), ('Chronology — source comparison saved without epoch/date changes', source_app.name), ('Companion — reader selection and qualified timeline verified locally', reader_app.name)]
    text = text.replace('    pending = [\n', '    pending = [\n'+''.join('        '+repr(v)+',\n' for v in entries), 1)
    compile(text,str(nav),'exec'); nav.write_text(text,encoding='utf-8',newline='\n')
    changes = [{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_guide,'replacement':guide_text}]; changes[1]['operations']=[{'old':old_line,'replacement':new_line}]; changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    for binding in read(A/'companion-before-cosmology-reader-01/PRESERVATION_MANIFEST.json'):
        if binding['path'].endswith(('CosmologyViewer.tsx','DungeonGuide.tsx')):
            changes.append({'before':binding,'after':info(G/binding['path'])})
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRouteRulesAdopted':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout[-1000:]); print(run.stderr[-3000:]); raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state.update(newRuleAdoptions=0,newRuleAdoptionScope='This checkpoint saves a source comparison and reader presentation; the proposed operating route remains unadopted. Prior souls candidate remains current.',newRuleAdoptionCountScope='Current checkpoint delta only; earlier adopted package history is preserved.')
    state['activeGptReview'].update(recordedAtUtc=now,status='CR-I01..10 integration submitted once; GPT responding at latest observation',submission=info(receipt),verdictReceived=True,verdictStatus='First and revised returns preserved; revised route fails substantive integration and remains unadopted.',responsePendingAtSubmission=True)
    state['cosmologyChronologyResearchSites'].update(status='Source comparison applied; operating route pending substantive integration',sourceApplication=info(source_app),sourceChapter=source['chapter'],routeSemanticAudit=info(semantic),integrationSubmission=info(receipt))
    state['cosmologyChronologyRouteReview']={'firstChecks':250,'revisedChecks':263,'sourceFailures':0,'revisedArchive':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Revised_Addendum_and_Evidence.zip'),'newRouteRulesAdopted':False,'followupReceipt':info(followup),'integrationReceipt':info(receipt),'semanticAudit':info(semantic)}
    state['cosmologyCompanionReaderReview']={'application':info(reader_app),'checks':21,'typeScriptPassed':True,'boundedBrowserCheckPassed':True,'sourceTextPreserved':True,'wholeRuntimeApproved':False,'published':False}
    state['ownerCampaignFrameQuestion']={'status':'pending; no answer observed','choices':['before Proof War','during original saga','after Proof War'],'dependentChoiceAdopted':False,'independentWorkContinues':True}
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=['Observe the same actual GPT Part3 chat/tab125746244; CR-I01..10 integration was sent once. Download the integrated eight-file package when ready. Verify83sources, real source locations and every semantic correction; do not adopt based only on hashes.',
      'Chronology source comparison is saved in CHRONOLOGY_SOURCE_REVIEWED_01. No87/710date correction,710prospective anchor, epoch, identity, Floor68route or EPIrule is adopted.',
      'Reader presentation is locally implemented and narrowly checked; original data/source text preserved. Preview tab closed and development server stopped. Broader companion/deep-floor packaging remains open.',
      'Owner campaign-frame question remains pending. Continue independent route/EPIwork; no elapsed-time default is owner approval.',
      'Souls/research reviewed candidate remains current. Full3test gate, actualShortRest limits and precise KT/PT/Hunt distinctions must survive route integration.',
      'Continue17EPIgroups,419reviewed/429pending ordinary spells and remaining full-game backlog. Latest verified GitHub18c6e3a; later work local; no sources deleted.']
    state.setdefault('preservationManifests',[]).extend([info(preserved/'PRESERVATION_MANIFEST.json'),info(A/'companion-before-cosmology-reader-01/PRESERVATION_MANIFEST.json')])
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRouteRulesAdopted':False}))

if __name__ == '__main__': main()
