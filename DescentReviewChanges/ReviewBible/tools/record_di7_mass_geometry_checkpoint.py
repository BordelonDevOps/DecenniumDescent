"""Record Faction correction, geometry19 execution and Mass payload evidence."""
from copy import deepcopy
from datetime import datetime,timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G,R,A,info,encoded,digest


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FACTION_AND_GEOMETRY.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_MASS_AND_GEOMETRY_EXECUTION.json'
    delta=A/'DI7_MASS_GEOMETRY_PROGRESS_DELTA.json'; preservation=A/'navigation-before-di7-mass-geometry'
    assert all(not p.exists() for p in [checkpoint,delta,preservation])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    reports={}
    for name,filename,checks,histories in [('faction','DI7_FACTION_TRANSACTIONS_V2_CHECK.json',81,36),
        ('geometry','DI7_AREA_GEOMETRY_CHECK.json',85,41),('mass','DI7_MASS_TRANSACTIONS_CHECK.json',73,29)]:
        path=A/filename; report=read(path)
        assert report['status']=='pass' and report['checks']==checks and report['historyCount']==histories and not report['failures']
        for binding in report['sourceBindings']: assert info(G/binding['path'])==binding
        reports[name]=(path,report)
    source_delta_path=A/'DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json'; source_delta=read(source_delta_path)
    assert len(source_delta['changes'])==4
    for c in source_delta['changes']:
        assert info(G/c['after']['path'])==c['after'] and digest((G/c['before']['preservedCopy']).read_bytes())==c['before']['sha256'] and c['exactInverseBytesVerified']
    assert reports['geometry'][1]['geometry19Executed'] and len(reports['geometry'][1]['sourceExpectationCoverage'])==19
    scope=('Actual GPT DI7-FACTION-REFERENCE-01 is terminal and its exact one-word visible-to-perceived correction is applied to current public/internal/manuscript copies with originals preserved. '
        'Faction current81 checks/36 histories include actual conditionally source-qualified unseen perception for all four providers, unperceived guesses before payment and false/protected membership only after payment; unrelated protections do not become blanket bans. '
        'All19 DI7-GEOMETRY-3D-01 supplemental source expectations are executed within85 checks/41 conditional paid histories: exact3D grid Supreme and rational axial/circular Mass predicates, original fixed committed geometry, actual endpoint revalidation, no radial cap, source occupancy/clipping, actual Counterspell and paid failure. '
        'Mass Revelation has73 checks/29 histories for all four actual information categories,125 readable enemies without a count cap, real hostile intent against caster/current party rather than caller labels, actual current spell/nonspell/suppressed/dormant magic without invented rank/school, inclusive6-second understood assertions and deliberate false belief rather than objective truth, source-specific protection and actual local clipping. '
        'Source condition helper verifies observer-specific Hidden/Invisible location consequences while sight/darkness/blindness remain distinct. Only actually delivered literal records inform an ally; old location reports do not track movement or remove current Hidden. '
        'Equivalent paid repeat retains17RP cost and actual Refrain. These are conditional finite rule evaluations; world truth, occupied shapes/clipping, native protection/sense grants, semantic beliefs, communication actions and originating movement remain explicit upstream premises. '
        'Supreme historical payload, Suggestion initiative clock, ordinary Shaman totem vent, original49 compilation and separate exact-seven acceptance remain. DI7-SUPREME-TIME-SCOPE-01 is sent once for uncertain historical protection applicability and safe partial-interval projection. '
        'Ordinary authored coverage412/436 unchanged. Fresh weekly usage43percent; owner stop at50 remains. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; nothing deleted or pushed.')
    ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']; before=read(ledger_path); ledger=deepcopy(before)
    evidence=[p for p,r in reports.values()]+[source_delta_path,A/'DI7_FACTION_REFERENCE_RECEIVED.json']
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope); row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'DI7-Mass-geometry-Faction-reference','recordedAtUtc':now,
                'factionChecks':81,'factionHistories':36,'geometryChecks':85,'geometryHistories':41,'geometryExpectationsExecuted':19,
                'massChecks':73,'massHistories':29,'full49Fulfilled':False,'exactCardsApproved':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old==new
    assert {k:v for k,v in before.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_FACTION_GEOMETRY_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_MASS_GEOMETRY_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1; text=text.replace(state['status'],scope,1)
    label='Faction perceived-versus-visible question —sent, response pending'
    # json.dumps in the previous recorder escaped the non-ASCII dash.
    oldlabel=json.dumps(label); assert text.count(oldlabel)==1
    text=text.replace(oldlabel,json.dumps('Faction original wording question —terminal correction received; see ruling'),1)
    marker='    pending = [\n'; assert text.count(marker)==1
    items=[('Faction current evidence —81 checks in36 conditional histories',reports['faction'][0]),
        ('GPT Faction targeting correction —terminal received',A/'DI7_FACTION_REFERENCE_RECEIVED.json'),
        ('Faction correction preserved originals and exact inverse proof',source_delta_path),
        ('Geometry19 source expectations executed —85 checks in41 histories',reports['geometry'][0]),
        ('Mass Revelation four-category payload —73 checks in29 histories',reports['mass'][0]),
        ('Supreme uncertain historical scope question —sent, response pending',A/'DI7_SUPREME_TIME_SCOPE_QUESTION.txt')]
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
        di7FactionTransactions={'report':info(reports['faction'][0]),'checks':81,'histories':36,'module':info(R/'tools/di7_faction_transactions.py'),
            'remaining':reports['faction'][1]['remaining'],'conditionalPremises':reports['faction'][1]['conditionalPremises'],'full49Fulfilled':False},
        di7MassTransactions={'report':info(reports['mass'][0]),'checks':73,'histories':29,'module':info(R/'tools/di7_mass_transactions.py'),
            'remaining':reports['mass'][1]['remaining'],'conditionalPremises':reports['mass'][1]['conditionalPremises'],'full49Fulfilled':False},
        di7GeometryExecution={'report':info(reports['geometry'][0]),'checks':85,'histories':41,'sourceExpectationCoverage':reports['geometry'][1]['sourceExpectationCoverage'],
            'module':info(R/'tools/di7_area_geometry.py'),'geometry19Executed':True,'informationPayloadExecuted':False},
        di7FactionReferenceCorrection={'received':info(A/'DI7_FACTION_REFERENCE_RECEIVED.json'),'changes':info(source_delta_path),'newRuleAdoptions':0,'exactCardsApproved':False},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Execution of prior geometry/Mass and correction of existing perceived targeting only.')
    state['di7GeometrySourceAddendum']['executed']=True
    state['activeGptReview']['instruction']='DI7-SUPREME-TIME-SCOPE-01 sent once; inspect actual terminal reply before retry. Geometry and Faction-reference rulings both received/applied; no exact-seven acceptance requested.'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_MASS_AND_GEOMETRY_EXECUTION. Latest fresh weekly usage43percent; stop at50 remains mandatory.',
        'Read actual GPT DI7-SUPREME-TIME-SCOPE-01 response in Chrome3 Calibration Review Part2 tab125745960; do not resend on timeout. Source question and screenshot retained.',
        'Faction current81/36 settles unseen-perceived references without creating a sense. Preserve initial63/28 as historical evidence.',
        'Geometry19 source expectations executed85/41. AreaGeometryTransactions returns a geometry-only pending payload gate; MassTransactions consumes it into the actual private four-category snapshot73/29. Supreme still needs its own historical payload.',
        'Geometry shape predicates execute exactly, but actual occupied box shapes, cell/portion clipping and legal displacement remain conditional upstream world premises. The scoped max metric never generalizes to other spells.',
        'Mass native protection and semantic facts remain conditional, not new acquired abilities. Observer condition helper executes modifiers only. Literal delivered records inform allies; stale locations do not track actual movement or end current Hidden.',
        'Implement Supreme history after source clarification, then Suggestion initiative/virtual clock and ordinary Shaman totem vent. Compile49 originals plus4Shield,19geometry and4Faction-reference supplements before separate complete7 exact review.',
        'Do not rerun successful write-once reports or rewrite historical hashes. Preserve before bytes/same-path deltas on mutations. No promotion, deletion, whole-game acceptance, push or cosmology occurred.',state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).extend([info(A/'source-before-di7-faction-reference/PRESERVATION_MANIFEST.json'),info(preservation/'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'weeklyUsagePercent':43,'pendingGptReply':True}))


if __name__=='__main__': main()
