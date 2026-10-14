"""Register declared-cost, interruption and rider-use follow-through."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,shutil,subprocess,sys
from validate_feat_exact_01_composite_casting import read,info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_STUNTS.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_TRANSACTIONS.json'
    delta=A/'FEAT335_BORROWED_TRANSACTIONS_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-borrowed-transactions'
    report_path=A/'FEAT335_BORROWED_TRANSACTIONS_CHECK.json';qualification=A/'FEAT335_BORROWED_TRANSACTIONS_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==239 and not report['failures'] and len(report['histories'])==29
    for b in report['sourceBindings']:assert info(G/b['path'])==b
    save(qualification,{'report':info(report_path),'earlierReport':info(A/'FEAT335_BORROWED_STUNTS_USE_CHECK.json'),
        'resolvedEarlierLimits':['Five attack cards and two task cards now expose separate declaration and resolution methods. Declaration rejects dice/outcome keys, commits own feat/action/ammunition and shared recharge histories, and records pending state. No roll is evaluated by declaration.',
            'Invalid resolution input leaves the existing commitment unchanged. A conditional actual authorized interruption ends the pending activation with no refund. Pending activations cannot be banked across a turn/rest.',
            'Feint and Covering Fire next-attack claims consume on the applicable actual attack before its outcome; replay is rejected and applicable Covering Fire penalties do not add.',
            'Shadow Step Hide now requires the immediate same-turn, same-position, no-intervening-event window; later turns cannot retain it.'],
        'remainingLimits':['The borrowed class skill alternative still uses its original atomic helper; it does not yet expose a distinct declaration/hidden-roll interface.',
            'Nature Whisper full minor-Weave, components, Dissonance and interrupted casting are outside this witness; its positive RP/evidence checks retain explicit independent source-clearance premises.',
            'Actual interruption authority, event legality, party/alliance/physical facts and canonical clock identities come from conditional fixtures. No general scheduler/campaign authenticator, full class engines or downstream damage/defense/Wound resolution is certified.',
            'No whole FXC04/07/08/09 closure, full feat approval, human playtest or cosmology approval follows.'],
        'newRules':0,'fullFeatExactApproved':False})
    state=read(previous)
    scope=('The borrowed-ability transaction follow-through passes 239 checks across 29 conditional histories, retaining all twelve native card cases. '
        'Five attack cards and two task cards now use separate declare/pay and resolve calls without accepting roll outcomes at declaration; invalid outcome input and actual authorized interruption do not refund costs. '
        'Feint/Covering Fire consume before the next qualifying attack outcome, and Shadow Hide has an immediate same-turn window. '
        'The original158-check report/model remains preserved. The class-skill alternative still needs its separate hidden-roll interface; full minor-Weave, ordinary event authorization/scheduler and downstream defenses/life-state integration remain open. '
        'GPT is still actively generating FEAT335-FLORA-SOURCE-CHECK-01 in the existing Calibration Review Part2 conversation. Cadence remains fulfilled; no review was resent. '
        'The full feat and whole-game gates, spell work, approved GitHub-before-cosmology sequence and 50-percent weekly-usage stop remain unchanged.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-borrowed-transactions','recordedAtUtc':now,'checks':239,'conditionalHistories':29,'borrowedCards':12,'fullUseRuntimeApproved':False})
            row['openIssues']=[('Borrowed attack/task declaration, interruption and later rider cases are addressed in FEAT335_BORROWED_TRANSACTIONS_CHECK.json. Remaining skill-alternative hidden-roll interface, full minor-Weave and ordinary downstream combat integration are specified in FEAT335_BORROWED_TRANSACTIONS_SCOPE.json; full FXC gates remain open.' if 'Read FEAT335_BORROWED_STUNTS_SCOPE_QUALIFICATION.json before relying' in x else x) for x in row['openIssues']]
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_BORROWED_STUNTS_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Borrowed ability transactions —239 checks, declared costs and later riders',report_path),('Borrowed transactions — remaining integration limits',qualification)]))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy);assert copy.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        borrowedTransactions={'report':info(report_path),'scope':info(qualification),'checks':239,'conditionalHistories':29,'borrowedCards':12,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Current checkpoint adds executable declared-cost and rider-use follow-through only; no source rule change.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_BORROWED_TRANSACTIONS. All12 cards retained;239 checks/29 histories add seven explicit declare/pay/resolve card interfaces, interruption and next-attack/immediate-Hide boundaries. Preserve earlier models and reports.',
        state['safeNextActions'][2],state['safeNextActions'][3],
        'Receive the already pending actual GPT Flora ruling. Independent remaining borrowed work: class-skill explicit declare/resolve; full Nature Whisper minor-Weave/casting and downstream combat interfaces. Other full-feat finite groups remain as listed in full exact-review preflight; no full335 submission yet.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))
if __name__=='__main__':main()
