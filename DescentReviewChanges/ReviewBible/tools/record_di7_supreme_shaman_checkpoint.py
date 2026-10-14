"""Record Supreme execution and the exact Shaman casting-interface clarification."""
from copy import deepcopy
from datetime import datetime,timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G,R,A,info,encoded,digest


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CLOCK_AND_SUPREME_SCOPE.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SUPREME_AND_SHAMAN_RULING.json'
    delta=A/'DI7_SUPREME_SHAMAN_PROGRESS_DELTA.json'; preservation=A/'navigation-before-di7-supreme-shaman'
    assert all(not p.exists() for p in [checkpoint,delta,preservation])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    report_path=A/'DI7_SUPREME_TRANSACTIONS_CHECK.json'; report=read(report_path)
    source_delta_path=A/'DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json'; source_delta=read(source_delta_path)
    assert report['status']=='pass' and report['checks']==74 and report['historyCount']==31 and not report['failures']
    assert report['supremeTime8Executed'] and len(report['sourceExpectationCoverage'])==8
    for binding in report['sourceBindings']:
        if info(G/binding['path'])!=binding:
            matches=[c for c in source_delta['changes'] if all(c['before'][k]==binding[k] for k in ['path','bytes','sha256'])]
            assert len(matches)==1 and digest((G/matches[0]['before']['preservedCopy']).read_bytes())==binding['sha256']
    for c in source_delta['changes']:
        assert info(G/c['after']['path'])==c['after'] and digest((G/c['before']['preservedCopy']).read_bytes())==c['before']['sha256'] and c['exactInverseBytesVerified']
    exp=read(R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json')
    assert sum(len(g['variants']) for g in exp['groups'])==49 and sum(len(g['variants']) for g in exp['supplementalSourceExpectations'])==44
    scope=('Supreme Sight now has74 checks/31 conditional paid histories covering all8 temporal-scope expectations. Four actual provider routes, current scoped3D geometry, empty-now historical locations, ancient and rank9 traces,129 actual occurrences without cap, one real continuous interval/actual transitions, local visits without remote destination, missing nonspell school/rank and private source boundaries are exercised. '
        'Unresolved historical applicability never invents a date or subtracts a protected span. Additional actual-world relations can establish inside/outside without changing public precision. Field-only protection retains other facts; partial histories retain one underlying identity and positive genuine transitions while omitting false continuity and protection-created cutoffs. '
        'Protected-interior changes have identical permitted public output, current-only defenses do not erase old history, native endpoints/subject/school/rank/query-time scopes remain literal, and an explicitly authorized field mask keeps its altered result. '
        'Unchanged paid repetition/different casters agree; empty absent/protected/unresolved histories share the same notice/result. Actual Counterspell blocks information; history grants no Fate original observation, blueprint, restoration or acquisition. Only actual delivered literal assertions are communicated. '
        'History facts, native grants, temporal relations and geometry/channel legality remain explicit Director-established conditional premises, not real campaign authentication or full runtime. '
        'Actual GPT DI7-SHAMAN-VENT-01 is terminal KEEP clarification and is applied as an exact shared interface note in current public/internal/manuscript representations; all7 payloads and class/guide source paragraphs remain unchanged. '
        'Vent checks actual step5 state after step4 concentration displacement; first qualifying zero-strain cast still occupies the opportunity; Fate child is excluded; Ready hold concentration ends incompatible totems before vent. Nine source-derived expectations are authored, not yet executed. '
        'Ordinary Shaman totem activation/vent is the remaining named casting interface before compiling49 originals plus44 source supplements (93total) and separate exact-seven review. Ordinary authored coverage412/436 unchanged. Fresh weekly usage44percent; owner stop at50 remains. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; nothing deleted or pushed.')
    ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']; before=read(ledger_path); ledger=deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,source_delta_path,A/'DI7_SHAMAN_VENT_RECEIVED.json'])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'DI7-Supreme-payload-and-Shaman-interface','recordedAtUtc':now,'checks':74,'conditionalHistories':31,
                'supremeTimeExpectationsExecuted':8,'shamanExpectationsAuthored':9,'shamanExpectationsExecuted':False,'full49Fulfilled':False,'exactCardsApproved':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old==new
    assert {k:v for k,v in before.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_CLOCK_SUPREME_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_SUPREME_SHAMAN_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1; text=text.replace(state['status'],scope,1)
    marker='    pending = [\n'; assert text.count(marker)==1
    items=[('Supreme historical payload —74 checks in31 conditional histories, all8 temporal cases',report_path),
        ('GPT Shaman vent checkpoint —terminal existing-source clarification',A/'DI7_SHAMAN_VENT_RECEIVED.json'),
        ('Shaman shared interface —preserved original files and inverse proof',source_delta_path),
        ('Exact Shaman interface text received from GPT',A/'DI7_SHAMAN_VENT_CLARIFICATION.txt')]
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in items))
    featured='    featured = [\n'; assert text.count(featured)==1
    text=text.replace(featured,featured+'        ('+json.dumps('DI7 Shaman casting-interface clarification')+', '+json.dumps('DescentReviewChanges/ReviewBible/docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md')+'),\n')
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
        di7SupremeTransactions={'report':info(report_path),'checks':74,'histories':31,'module':info(R/'tools/di7_supreme_transactions.py'),
            'sourceExpectationCoverage':report['sourceExpectationCoverage'],'remaining':report['remaining'],'conditionalPremises':report['conditionalPremises'],'full49Fulfilled':False},
        di7ShamanVentRuling={'received':info(A/'DI7_SHAMAN_VENT_RECEIVED.json'),'changes':info(source_delta_path),
            'interfaceNote':info(R/'docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md'),'newRuleAdoptions':0,'expectationsAuthored':9,'expectationsExecuted':False},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Supreme executes previously applied rules; Shaman is KEEP existing-source clarification only.')
    state['di7SupremeTimeScope']['newExpectationsExecuted']=True
    state['activeGptReview']['instruction']='No reply pending. Supreme temporal and Shaman vent rulings are terminal/applied. Execute remaining Shaman interface then compile93 finite cases and submit separate exact-seven review.'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_SUPREME_AND_SHAMAN_RULING. Fresh weekly usage44percent; stop at50 mandatory.',
        'SupremeTransactions74/31 executes all8 temporal cases and current historical payload. HistoricalInformation handles actual uncertain-window/point/continuous/relative precision separately, native query scopes and source-proven additional temporal relations. Do not replace unknown historical time with the older numeric Vision projector.',
        'No GPT reply pending. Chrome3 Calibration Review Part2 tab125745960. Shaman vent exact5-paragraph KEEP note is now sharedOperatingRules.shamanCastingInterface and standalone DI7_SHAMAN_CASTING_INTERFACE.md; all7 payloads unchanged.',
        'Implement actual selected Shaman Totem Casting and its vent at step5 AFTER required concentration displacement. A first qualifying0-strain cantrip consumes opportunity; outside/excluded-route cast does not. Two own auras share one opportunity; other owner aura does not qualify. Ready hold concentration displaces own totems BEFORE outer strain, not after; release has no second checkpoint. Fate child receives/occupies no ordinary vent, and concentration child ends actual totems without undoing outer vent.',
        'Fate forecast must include the outer actual vent and known mandatory Ready concentration loss, then child revalidation uses actual updated strain. Existing FateTransactions.begin_fate applies held concentration after its ordinary declare; a Shaman extension must correct this order for that interface, preserving old histories and avoiding premature effects before validated commitment.',
        'Shaman source shaman.json schedule at1 is4 Base selections minimum2active. Totem Casting is selected not automatic; use exact card/source binding and actual selection receipt. Engine places Tiny visible magical AC12+PB HP2L immobile totem within30,15ft aura,3source turns, capacity2at13,2RP Action, shared concentration. A Stone-only finite vent adapter must not claim other aura profiles/healing/damage executed.',
        'Rank0 first-spell case can use actual reviewed Shaman Divination Detect Poison: Action30ftVS, perceived creature/object, current explicit poison yes/no, no type/cure. Actual cantrip acquisition uses shared CLASS_PLAYTEST_RULES known-cantrip counts (hybrid2atfirst,3at10). Existing DI7Sources rejects ordinary modes other than its named adapters and DI7CastTransactions.learn handles ranked only; add an explicit narrow source/acquisition/payload adapter rather than fake rank0 learning or bypassing predicates.',
        'Current local reports: Shield95/36, acquisition385/77, Vision97/44, Faction81/36, geometry85/41(all19), Mass73/29, clock58/22, Supreme74/31(all8). Keep all report/module before bytes and source hash chains; do not rerun successful write-once validators.',
        'Compile16groups49 originals plus4Shield+19geometry+4Faction-reference+8Supreme-time+9Shaman expectations (93total). Verify full coverage and submit all7 exact public/internal envelopes separately; source directions/local checks never count as exact acceptance or promotion.',
        'No source deletion, promotion, human approval, whole-game acceptance, push or cosmology occurred. Preserve same-path deltas for edits.',state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).extend([info(A/'source-before-di7-shaman-vent/PRESERVATION_MANIFEST.json'),info(preservation/'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'weeklyUsagePercent':44,'pendingGptReply':False}))


if __name__=='__main__': main()
