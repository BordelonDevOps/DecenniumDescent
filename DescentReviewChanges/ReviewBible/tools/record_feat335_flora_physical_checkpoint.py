"""Register actual bounded Flora task/terrain interfaces without broad promotion."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'

def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_VERDANT_AND_NATURE.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FLORA_PHYSICAL.json'
    delta=A/'FEAT335_FLORA_PHYSICAL_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-flora-physical'
    report_path=A/'FEAT335_FLORA_PHYSICAL_INTERFACES_CHECK.json';qualification=A/'FEAT335_FLORA_PHYSICAL_INTERFACES_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==148 and not report['failures'] and len(report['histories'])==34
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    save(qualification,{'report':info(report_path),'scope':report['scope'],'remainingLimits':report['limits'],
        'resolvedFiniteInterfaces':['Verdant actual wilderness Nature task advantage without needing Flora; ordinary advantage/disadvantage cancellation, real Action payment before roll and no training gain.',
            'Live active-Flora condition grants normal cost only for difficult terrain caused solely by nonmagical plants. Ordinary crawling/squeezing, other causes, severe/magical terrain, hazards, actual Speed, route/endpoint and movement expenditure remain.',
            'INT Investigation Action identifies actual armed Lash/Spore/Entangle mode only on successful Core task. DEX with actual usable held thieves tools disarms one actual plant without ending/healing it or creating automatic explosion on failure.',
            'Own source-materialized inspector modifiers apply; no invented Investigation/tool PB. Costs commit before rolls, failed tasks do not refund, ended targets close paid pending attempts without information.'],
        'notNewEvidence':['The conditional world cannot authenticate a real campaign, pathfinding, event schedule, hearing, legal task or physical tools. These are explicit scenario premises.',
            'No whole plant damage/defense/life-state engine, actual full Nature spell cast or complete335 feat/runtime/human balance approval.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False})
    state=read(previous)
    scope=('Flora physical interfaces add148 passing checks across34 conditional paid-source histories. '
        'Verdant wilderness Nature advantage works without a plant and follows ordinary kept-die cancellation; its separate movement exception needs active Flora and applies only to difficult terrain caused solely by nonmagical plants. '
        'Actual one-axis endpoints and movement expenditure are recorded; crawling/squeezing, other terrain, hazards, Speed and route constraints remain. '
        'All three armed Flora modes have paid INT Investigation identification and actual-tools DEX disarm cases. Failed identification reveals no mode; failed disarm grants no explosion; paid attempts on an ended target close without refund. '
        'Actor ability/training comes from source-materialized histories; actual physical/task/world facts remain conditional. '
        'GPT is still actively working on the already sent FEAT335-NATURE-SOURCE-CHECK-01 in Calibration Review Part2. No rank/component/Dissonance interpretation is invented pending that reply. '
        'Earlier Flora, Verdant message and borrowed-skill evidence remains preserved. Remaining full-use cases, whole-game agreement, GitHub-before-cosmology sequence and50-percent weekly-usage stop remain in force.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-Flora-physical-interfaces','recordedAtUtc':now,'checks':148,'conditionalHistories':34,'modes':3,'fullUseRuntimeApproved':False})
            row['openIssues']=[('Flora FLQ01–04, stored-message/simple communication and wilderness-task/plant-terrain/armed-mode identification-disarm have distinct finite evidence. Remaining work includes ordinary attacks/defenses/life-state integration, genuine world/scheduler authority and full Nature casting. These slices do not close full FXC04/06–10 or whole335 exact approval.' if 'Remaining Flora scope includes' in x else x) for x in row['openIssues']]
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_VERDANT_AND_NATURE_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_FLORA_PHYSICAL_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Flora physical interfaces —148 checks,34 histories',report_path),('Flora task/terrain/inspection — scope and remaining integrations',qualification)]))
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
        floraPhysicalInterfaces={'report':info(report_path),'scope':info(qualification),'checks':148,'conditionalHistories':34,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Bounded source-governed task/terrain/inspection follow-through; no source rule change.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_FLORA_PHYSICAL. Flora source189/54, Verdant message92/19 and physical148/34 remain distinct bounded scopes, not whole-system/runtime certification.',
        state['safeNextActions'][2],
        'Nature classification, components, strain/history and activation/check interfaces remain under actual GPT review. Independent next work: seven copy profiles, ritual/Time/transfer interfaces and full FXC06–10 source-qualified work/economic/physical/case sequences. Flora ordinary damage/defense and scheduler integration remain separate.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))

if __name__=='__main__':main()
