"""Record original alignment clock execution and received Supreme time addendum."""
from copy import deepcopy
from datetime import datetime,timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G,R,A,info,encoded,digest


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_MASS_AND_GEOMETRY_EXECUTION.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CLOCK_AND_SUPREME_SCOPE.json'
    delta=A/'DI7_CLOCK_SUPREME_PROGRESS_DELTA.json'; preservation=A/'navigation-before-di7-clock-supreme'
    assert all(not p.exists() for p in [checkpoint,delta,preservation])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    report_path=A/'DI7_ALIGNMENT_CLOCK_CHECK.json'; report=read(report_path)
    source_delta_path=A/'DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json'; source_delta=read(source_delta_path)
    assert report['status']=='pass' and report['checks']==58 and report['historyCount']==22 and not report['failures']
    for binding in report['sourceBindings']:
        if info(G/binding['path'])!=binding:
            matches=[c for c in source_delta['changes'] if all(c['before'][k]==binding[k] for k in ['path','bytes','sha256'])]
            assert len(matches)==1 and digest((G/matches[0]['before']['preservedCopy']).read_bytes())==binding['sha256']
    for c in source_delta['changes']:
        assert info(G/c['after']['path'])==c['after'] and digest((G/c['before']['preservedCopy']).read_bytes())==c['before']['sha256'] and c['exactInverseBytesVerified']
    scope=('Original Alignment Suggestion timing now has58 checks/22 conditional paid histories using its tenth future regular caster-start marker in initiative and original absolute60 seconds outside initiative. '
        'Schedule changes, leaving/reentering initiative, suppression and additional turn budgets do not recompute the original clock; source concentration endings still govern. '
        'Purge retains its separate explicit elapsed60 seconds in all four actual provider histories. Actual paid recasts, countered/saved casts and a paid observed Fate Echo child retain their own valid timers; copied Suggestion uses the new caster phase rather than inheriting the original timer. '
        'Initiative schedules, originating extra-turn/displacement/death legality and full character/rest history remain conditional upstream premises. The initial elapsed-only component and all previous reports are preserved. '
        'Actual GPT DI7-SUPREME-TIME-SCOPE-01 is terminal and its exact four-paragraph insertion is applied to current public/internal/manuscript copies with original bytes and exact inverse proof. '
        'NEW unresolved temporal applicability permits only established assertions readable under every still-consistent applicability outcome, with no invented date or subtraction of protected dates. NEW partial-history projection retains one internal effect history but publishes genuine positive facts/transitions without protection-derived boundaries or false continuity. '
        'Every historical reading uses the same non-diagnostic coverage notice. Eight authored source expectations are added, not yet executed. Existing geometry/faction rulings and all original49 plus prior27 supplements remain intact. '
        'Current finite local evidence includes Faction81/36, geometry85/41 covering19source cases, Mass73/29 and clock58/22. Supreme historical payload and actual ordinary Shaman totem vent remain before full84-case compilation and separate exact-seven review. '
        'Ordinary authored coverage412/436 unchanged. Fresh weekly usage43percent; owner stop at50 remains. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; nothing deleted or pushed.')
    ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']; before=read(ledger_path); ledger=deepcopy(before)
    evidence=[report_path,source_delta_path,A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.json']
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope); row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'DI7-original-clocks-and-Supreme-time-scope','recordedAtUtc':now,
                'checks':58,'conditionalHistories':22,'newSupremeExpectationsAuthored':8,'newSupremeExpectationsExecuted':False,
                'full49Fulfilled':False,'exactCardsApproved':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old==new
    assert {k:v for k,v in before.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_MASS_GEOMETRY_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_CLOCK_SUPREME_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1; text=text.replace(state['status'],scope,1)
    oldlabel=json.dumps('Supreme uncertain historical scope question —sent, response pending'); assert text.count(oldlabel)==1
    text=text.replace(oldlabel,json.dumps('Supreme original temporal-scope question —terminal addendum received and applied'),1)
    marker='    pending = [\n'; assert text.count(marker)==1
    items=[('Suggestion original virtual clock and paid Fate child —58 checks in22 histories',report_path),
        ('GPT Supreme historical scope ruling —terminal source addendum',A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.json'),
        ('Supreme time-scope insertion —exact source text',A/'DI7_SUPREME_TIME_SCOPE_INSERTION.txt'),
        ('Supreme time-scope originals and inverse proof',source_delta_path)]
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in items))
    compile(text,str(nav),'exec'); preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.read_bytes()); assert dest.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text,encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'spellPromotions':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        di7AlignmentClock={'report':info(report_path),'checks':58,'histories':22,'module':info(R/'tools/di7_alignment_clock.py'),
            'remaining':report['remaining'],'conditionalPremises':report['conditionalPremises'],'full49Fulfilled':False},
        di7SupremeTimeScope={'received':info(A/'DI7_SUPREME_TIME_SCOPE_RECEIVED.json'),'changes':info(source_delta_path),
            'newRuleAdoptions':2,'newExpectationsAuthored':8,'newExpectationsExecuted':False,'exactCardsApproved':False},
        newRuleAdoptions=2,newRuleAdoptionCountScope='Only GPT-directed Supreme unresolved temporal applicability and partial-history projection.')
    state['activeGptReview']['instruction']='No reply pending. DI7-GEOMETRY-3D-01, DI7-FACTION-REFERENCE-01 and DI7-SUPREME-TIME-SCOPE-01 are terminal and applied. No separate exact-seven acceptance requested or received.'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_CLOCK_AND_SUPREME_SCOPE. Latest fresh weekly usage43percent; stop at50 remains mandatory.',
        'Actual GPT Supreme time-scope ruling is received/applied exactly. No reply pending. Chrome3 Calibration Review Part2 last tab125745960; re-mark only when browser work continues.',
        'Implement Supreme historical information using current operative text plus geometry gate. Retain real temporal uncertainty, one internal effect identity, native endpoint scope and uniform notice. Do not use a fabricated actualTime to satisfy the Vision projector; its numeric-time premise does not handle unknown historical times.',
        'Unresolved applicability permits only facts readable in every consistent outcome; existence potentially protected means no attributable row absent independent readable basis. Partial histories use genuine positive observations/transitions, never protection-generated150/175 transitions, certified continuity or hidden-span diagnostics.',
        'ClockedFateTransactions and AlignmentClockComponent58/22 settle Suggestion original virtual/absolute timers while Purge stays60elapsed. Original elapsed-only component and reports stay historical. A paid Fate child has its own caster clock. Actual upstream schedule/extra-turn legality remains conditional.',
        'Ordinary Shaman totem vent remains: class source shaman.json protected interface and engine lines61–63; actual selected paid2RP Action totem, own active15ft aura, shared concentration, duration3source turns, once-round first ordinary spell strain minus1 minimum0; no RP reduction. Need confer if concentration-cast ordering against ending the own totem creates ambiguity.',
        'Current Faction81/36, geometry85/41(all19), Mass73/29 are saved and bound to preserved prior source revisions through exact deltas. Do not rerun successful write-once validators or silently rewrite source hashes.',
        'Compile16groups49 originals plus4Shield,19geometry,4Faction-reference and8Supreme-time expectations (84total) before separate complete7 public/internal exact review. Source agreement is not exact approval or promotion.',
        'No source deletion, promotion, human approval, whole-game acceptance, push or cosmology occurred. Preserve before bytes and same-path deltas for any changes.',state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).extend([info(A/'source-before-di7-supreme-time-scope/PRESERVATION_MANIFEST.json'),info(preservation/'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'weeklyUsagePercent':43,'pendingGptReply':False}))


if __name__=='__main__': main()
