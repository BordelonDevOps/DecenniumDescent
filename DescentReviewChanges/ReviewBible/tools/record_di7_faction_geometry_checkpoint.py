"""Preserve Faction evidence and applied GPT geometry source decisions."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_VISION_TRANSACTIONS.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FACTION_AND_GEOMETRY.json'
    delta = A / 'DI7_FACTION_GEOMETRY_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-di7-faction-geometry'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    report_path = A / 'DI7_FACTION_TRANSACTIONS_CHECK.json'; report = read(report_path)
    source_delta_path = A / 'DI7_GEOMETRY_DERIVED_OPERATIONS.json'; source_delta = read(source_delta_path)
    assert report['status'] == 'pass' and report['checks'] == 63 and report['historyCount'] == 28 and not report['failures']
    for binding in report['sourceBindings']:
        if info(G / binding['path']) != binding:
            matches = [c for c in source_delta['changes'] if all(c['before'][k] == binding[k] for k in ['path','bytes','sha256'])]
            assert len(matches) == 1
            assert digest((G / matches[0]['before']['preservedCopy']).read_bytes()) == binding['sha256']
    assert len(source_delta['changes']) == 4
    for c in source_delta['changes']:
        assert info(G / c['after']['path']) == c['after']
        assert digest((G / c['before']['preservedCopy']).read_bytes()) == c['before']['sha256']
        assert c['exactInverseBytesVerified']
    scope = ('Faction Omniscience has63 checks across28 conditional histories: actual paid four-provider acquisition/casting, hidden current membership only after payment, '
        'all current institution-wide remote/unreported/unauthorized institutional work with no count cap, private and rival work excluded, personal-field protections preserved, '
        'actual material updates, reference departure/death independence, no missed-history backfill after suppression/incapacity, exact60-second expiry, caster/institution loss and actual Counterspell. '
        'Institutional facts, continuity, underlying protection grants and legal external events remain explicit Director-established conditional premises; this is not a whole runtime or real campaign claim. '
        'Actual GPT DI7-GEOMETRY-3D-01 is terminal and its exact text is applied to public/internal/manuscript counterparts with four original files preserved and exact inverse proof. '
        'KEEP horizontal grid distance and circular axial cone; NEW scoped Supreme three-axis max metric and fixed-center resolution revalidation, plus Mass fixed-origin legality at resolution. '
        'Nineteen authored geometry expectations supplement unchanged49 originals and4 Shield cases; these geometry cases are not yet executed. '
        'DI7-FACTION-REFERENCE-01 is sent to GPT for perceived-versus-visible wording; current63/28 fixtures do not settle this edge. '
        'Mass/Supreme payloads, Suggestion initiative clock, ordinary Shaman totem vent and separate exact-seven review remain. '
        'Ordinary authored coverage412/436 unchanged. Fresh weekly usage42percent; owner stop at50 remains. '
        'Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    evidence = [report_path, source_delta_path, A / 'DI7_GEOMETRY_3D_RECEIVED.json']
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'DI7-Faction-and-geometry', 'recordedAtUtc':now,
                'checks':63,'conditionalHistories':28,'geometryExpectationsAuthored':19,'geometryExpectationsExecuted':False,
                'full49Fulfilled':False,'exactCardsApproved':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old==new
    assert {k:v for k,v in before.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_VISION_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_GEOMETRY_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_FACTION_GEOMETRY_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1; text=text.replace(state['status'],scope,1)
    marker='    pending = [\n'; assert text.count(marker)==1
    items=[('Faction Omniscience —63 checks in28 conditional histories',report_path),
        ('GPT geometry ruling —terminal scoped source addendum',A/'DI7_GEOMETRY_3D_RECEIVED.json'),
        ('Geometry exact edits —originals preserved and inverse verified',source_delta_path),
        ('Faction perceived-versus-visible question —sent, response pending',A/'DI7_FACTION_REFERENCE_QUESTION.txt')]
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in items))
    compile(text,str(nav),'exec'); preserved=[]
    for path in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/path.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(path.read_bytes())
        assert dest.read_bytes()==path.read_bytes(); preserved.append({**info(path),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text,encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'spellPromotions':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        di7FactionTransactions={'report':info(report_path),'checks':63,'histories':28,'module':info(R/'tools/di7_faction_transactions.py'),
            'remaining':report['remaining'],'conditionalPremises':report['conditionalPremises'],'full49Fulfilled':False},
        di7GeometrySourceAddendum={'received':info(A/'DI7_GEOMETRY_3D_RECEIVED.json'),'changes':info(source_delta_path),
            'authoredSupplementalExpectations':19,'executed':False,'exactCardsApproved':False},
        newRuleAdoptions=3,newRuleAdoptionCountScope='GPT-scoped vertical Supreme metric and the two fixed committed geometry resolution checkpoints.')
    state['activeGptReview']['instruction']='DI7-FACTION-REFERENCE-01 sent once; inspect terminal response before retry. Geometry terminal and applied. No exact seven-card acceptance requested or received.'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_FACTION_AND_GEOMETRY. Latest fresh weekly usage42percent; stop at50 remains mandatory.',
        'Read actual GPT response to DI7-FACTION-REFERENCE-01 in Chrome3 Calibration Review Part2 tab125745960; do not resend because of timeouts. Question and sent screenshot are retained.',
        'Current Faction evidence63/28 is qualified conditional local execution; perceived-but-unseen reference edge remains pending GPT. Report binds the preserved pre-geometry candidate, not silently rewritten hashes.',
        'Geometry ruling is applied exactly. Implement Mass/Supreme paid payloads and19 geometry expectations. Preserve old report/source bytes and same-path delta chains. No generic movement rule is created.',
        'Finish Suggestion initiative/virtual clock and ordinary Shaman totem vent, assemble16groups49 originals plus4Shield and19geometry supplemental cases, then submit complete7 public/internal cards for separate exact review.',
        'No spell promotion, source deletion, exact acceptance, human evidence, whole-game flow approval, push or cosmology review occurred.',state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).extend([info(A/'source-before-di7-geometry/PRESERVATION_MANIFEST.json'),info(preservation/'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'weeklyUsagePercent':42,'pendingGptReply':True}))


if __name__=='__main__': main()
