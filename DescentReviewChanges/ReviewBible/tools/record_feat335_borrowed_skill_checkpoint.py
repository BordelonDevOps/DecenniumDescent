"""Record the finite borrowed class-skill declare/pay/resolve completion."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'

def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FLORA_FULFILLMENT.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_SKILL.json'
    delta=A/'FEAT335_BORROWED_SKILL_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-borrowed-skill'
    report_path=A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json';qualification=A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==362 and not report['failures'] and len(report['histories'])==38
    for b in report['sourceBindings']:assert info(G/b['path'])==b
    save(qualification,{'report':info(report_path),'earlierReport':info(A/'FEAT335_BORROWED_TRANSACTIONS_CHECK.json'),
        'resolvedEarlierLimit':'The class-skill alternative now exposes separate declaration/payment and task resolution. Declaration admits no die/result, validates the exact prepared actual class skill, ordinary source ability, actual legal Action task and available donor/channel/use. It pays before any roll. Failed/invalid outcomes do not refund the commitment; authorized interruption closes it with costs spent.',
        'scope':report['skillTransactionScope'],
        'remainingLimits':['Task Action legality and DC are explicit conditional premises. Other authorized task timings or alternate abilities are outside this finite interface, not declared illegal game actions.',
            'No donor proficiency or stats are imported. The tested borrower histories cover existing normal Athletics proficiency and untrained Intimidation. Separate own Expertise acquisition/integration is not newly certified.',
            'Nature Whisper full minor-Weave, components, Dissonance and interrupted casting still require integration. Actual event/clock/party/geometry authority, ordinary defenses/life state and full FXC04/06–10 gates remain open.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False})
    state=read(previous)
    scope=('Versatile Mastery class-skill follow-through now passes362 checks across38 conditional histories while retaining the twelve native borrowed-card cases. '
        'Actual Soldier class-selected Athletics/Intimidation use the borrower\'s own ability and normalPB with trained/untrained borrower histories. '
        'Declaration commits the existing feat use and the real task Action before accepting a die; bad declarations spend nothing, invalid results retain the commitment, failures and authorized interruptions do not refund it, and pending checks cannot be banked across turns/rest. '
        'Donor state and permanent training remain unchanged. Earlier reports/models are preserved. '
        'The separate Flora source ruling is already terminal and its four interfaces/all18 groups remain fulfilled under189 checks/54 histories; no GPT request is pending. '
        'Full Nature Whisper casting, broader use/physical/social/time examples and the full335 exact review remain open. No source rule, whole-game approval, push or cosmology change occurs; the50-percent weekly-usage stop remains in force.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-borrowed-class-skill-transactions','recordedAtUtc':now,'checks':362,'conditionalHistories':38,'borrowedCardsRetained':12,'fullUseRuntimeApproved':False})
            row['openIssues']=[('Borrowed attack/task/skill declaration, interruption and later riders have finite evidence in FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json. Full Nature Whisper casting/Weave and ordinary downstream combat/task/clock integration remain open; see FEAT335_BORROWED_SKILL_TRANSACTIONS_SCOPE.json. No full FXC gate closes from this slice.' if 'Remaining skill-alternative hidden-roll interface' in x else x) for x in row['openIssues']]
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_FLORA_FULFILLMENT_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_BORROWED_SKILL_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Borrowed class skill transactions —362 checks,38 histories',report_path),('Borrowed class skills — finite scope and remaining integration',qualification)]))
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
        borrowedSkillTransactions={'report':info(report_path),'scope':info(qualification),'checks':362,'conditionalHistories':38,'borrowedCardsRetained':12,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='Current checkpoint adds finite skill declaration/payment and outcomes only; Flora source completions remain in the prior fulfillment checkpoint.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_BORROWED_SKILL. All12 cards retained;362 checks/38 histories add explicit class-skill declaration/payment, actual Core rolls, input boundaries, interruption and recovery. Earlier reports/models remain immutable.',
        state['safeNextActions'][2],
        'Next finite work: Nature Whisper full minor-Weave/RP/components/Dissonance/casting integration and remaining FXC04/06–10 use, physical/social, original-clock and authored-example premises. Skill hidden-roll boundary is now addressed within its Action-task/normal-ability scope. No full335 submission until required acceptance evidence is complete.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))

if __name__=='__main__':main()
