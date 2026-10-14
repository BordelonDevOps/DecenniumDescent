"""Preserve/register the finite seven-profile source adapter evidence."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FLORA_PHYSICAL.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_COPY_SOURCES.json'
    delta=A/'FEAT335_COPY_SOURCES_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-copy-sources'
    report_path=A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json';qualification=A/'FEAT335_COPY_SOURCE_COMPONENTS_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==248 and not report['failures'] and len(report['histories'])==35
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    save(qualification,{'report':info(report_path),'scope':report['scope'],'remainingLimits':report['limits'],
        'resolvedFiniteInterfaces':['Seven profiles each have an exact reviewed whole-spell source and actual source-class placement. Unsupported labels are not proof of a source component.',
            'Damage/ward native dice precede recipient limits. Lifedraw normal healing exists only for qualifying actual damage and eligible target; its native healing magnitude is floor(actual damage/2), distinct from original damage magnitude.',
            'Slow school/mode and surviving control matter; Shield grants only the AC boon choice; Step uses actual completed Mist Step distance, not the printed maximum.'],
        'pendingInterfaces':['Actual paid feat acquisitions, own learning rank route, capture costs/conditions/timing, shared one-record lifecycle, release payment/history/interrupts, recipient effects and adaptation remain distinct unfinished work.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False})
    state=read(previous)
    scope=('Seven feat-copy source profiles now have248 checks across35 conditional scenarios with exact reviewed whole-card spell bindings. '
        'Arcane Ray, Burning Hands, Lifedraw, False Life, Slow, Shield and Mist Step supply the seven actual witnessed components. '
        'Native numeric bounds, Lifedraw eligibility and damage-to-heal derivation, actual Slow mode, AC-only Shield and completed teleport distance are distinguished. '
        'Seal Minor Wound, False Comfort, Mending and Spare the Dying do not supply ordinary HP healing. '
        'This source adapter supplies no capture authorization or paid release. Actual upstream spell/perception/world facts remain conditional; own paid feats, rank access, capture lifecycle, casting and recipient application remain unfinished. '
        'The already-sent Nature source review remains active in GPT; no classification completion is assumed. '
        'Prior evidence and source information remain preserved. Full joint review precedes GitHub delivery; cosmology follows verified push. Stop at50percent weekly usage remains controlling.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-copy-source-components','recordedAtUtc':now,'checks':248,'conditionalHistories':35,'profiles':7,'fullUseRuntimeApproved':False})
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_FLORA_PHYSICAL_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_COPY_SOURCES_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Seven feat-copy source components —248 checks,35 scenarios',report_path),('Copy-source scope —capture and release still pending',qualification)]))
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
        copySourceComponents={'report':info(report_path),'scope':info(qualification),'checks':248,'conditionalHistories':35,'profiles':7,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Source-component witness adapter only; no source rule change.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_COPY_SOURCES. Source adapter248/35 covers seven profiles but neither capture authorization nor paid release. Full source-bound copy lifecycle is next independent work.',
        state['safeNextActions'][2],
        'Receive Nature classification/components/strain/commitment review in existing GPT tab when terminal. Preserve/reproduce and apply only exact authorized source amendments, then finite follow-through. Do not resend pending request.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))


if __name__=='__main__':main()
