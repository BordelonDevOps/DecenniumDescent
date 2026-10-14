"""Preserve and register the bounded all12 borrowed-card pass without closing full-use gates."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,shutil,subprocess,sys
from validate_feat_exact_01_composite_casting import read,info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    now=datetime.now(timezone.utc).isoformat();previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_CADENCE_AND_FLORA.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_STUNTS.json';delta=A/'FEAT335_BORROWED_STUNTS_PROGRESS_DELTA.json'
    preservation=A/'navigation-before-feat335-borrowed-stunts';qualification=A/'FEAT335_BORROWED_STUNTS_SCOPE_QUALIFICATION.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification])
    report_path=A/'FEAT335_BORROWED_STUNTS_USE_CHECK.json';report=read(report_path)
    assert report['checks']==158 and not report['failures'] and report['counts']['permittedCards']==12 and len(report['histories'])==19
    for b in report['sourceBindings']:assert info(G/b['path'])==b
    save(qualification,{'report':info(report_path),'status':'bounded-conditional-transaction-evidence',
        'clarifications':[
            'Every recorded activation supplies already chosen test die faces and performs one atomic fixture transaction. The event field committedBeforeOutcome describes the intended cost commitment, not proof of a separate hidden-roll declaration/resolution protocol; some native outcome calculations are evaluated before the commit call. No interactive reveal-order or interrupted-activation claim follows.',
            'Shadow Step Hide is exercised only as an immediate paired operation. The helper is not a scheduler and does not reject every possible later/interleaved call; arbitrary scheduling remains outside its stated slice.',
            'Covering Fire and Feint later-attack consumption/nonstacking, full minor-Weave casting interfaces and independent owned class-feature triggers still need distinct implementation/evidence. Native damage is before downstream defenses/life-state resolution.',
            'The 158 checks establish the enumerated paid-source/native effect and rejection cases only. They do not establish all FXC04/07/08/09 requirements, actual campaign facts or full feat approval.'],
        'newRules':0,'fullFeatExactApproved':False})
    state=read(previous)
    scope=('The twelve Versatile Mastery borrowed cards and its skill alternative now have a source-bound finite transaction pass: 158 checks across 19 conditional histories. '
        'Actual Human lineage, earned level4 feat payment, source class-card selection schedules, own training/equipment/stat calculations, preparation, donor consent/range, all12 native effects, separate movement budgets, RP/ammunition costs and shared same-card cooldown/rest histories are bound. '
        'The scope qualification explicitly excludes hidden-roll declaration/interruption sequencing, arbitrary Shadow Hide scheduling, later Feint/Covering Fire consumption, full minor-Weave integration and downstream life-state effects. Full feat/runtime approval remains open. '
        'The earlier cadence correction is fulfilled. Actual GPT is still answering the already sent FEAT335-FLORA-SOURCE-CHECK-01; no duplicate submission occurred. '
        'All original files and prior evidence remain preserved. Remaining full exact-review and whole-game development gates, spell totals, GitHub-before-cosmology order and the owner50-percent weekly-usage stop remain unchanged.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-borrowed-stunts','recordedAtUtc':now,'checks':158,'conditionalHistories':19,'borrowedCards':12,'fullUseRuntimeApproved':False})
            row['openIssues'].append('Read FEAT335_BORROWED_STUNTS_SCOPE_QUALIFICATION.json before relying on158 bounded checks. Complete hidden-roll declaration/interruption, Feint/Covering Fire later-attack consumption, immediate Shadow Hide sequencing and minor-Weave integration; full exact-review FXC gates remain open.')
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_CADENCE_AND_FLORA_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Borrowed class abilities —158 checks across12 cards and skill alternative',report_path),
        ('Borrowed-ability scope limits — retain remaining integration gates',qualification)]))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        assert p.read_bytes()==copy.read_bytes();preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        borrowedStunts={'report':info(report_path),'qualification':info(qualification),'checks':158,'conditionalHistories':19,'borrowedCards':12,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint adds bounded borrowed-card evidence only; current cadence completion remains in its prior checkpoint.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_BORROWED_STUNTS. All12 cards/skill alternative have158 bounded checks in19 histories; read scope qualification. Preserve successful report/models rather than rerun unchanged suites.',
        state['safeNextActions'][2],state['safeNextActions'][3],
        'Next complete genuine declare/resolve and interruption handling for borrowed uses without exposing outcome before payment, then later Feint/Covering Fire rider use and immediate Shadow Hide. Minor-Weave, arbitrary class triggers and life-state damage remain explicit integration obligations. No full335 submission yet.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))
if __name__=='__main__':main()
