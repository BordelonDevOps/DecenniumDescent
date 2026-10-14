"""One-use checkpoint for paid ownership chains and their actual GPT dispatch."""
from copy import deepcopy
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_OWNED_FEAT_CHAINS.json'
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_TRAINING_PREREQUISITES.json'
preservation=A/'navigation-and-coverage-before-feat-exact-01-owned-feat-chains'
delta_path=A/'FEAT_EXACT_01_OWNED_FEAT_COVERAGE_DELTA.json'
assert not target.exists() and not preservation.exists() and not delta_path.exists(),'One-use checkpoint already started'
report_path=A/'FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json';report=read(report_path)
notes_path=A/'FEAT_EXACT_01_OWNED_FEAT_CHAIN_NOTES.md'
dispatch_path=A/'FEAT327_FXC05_TRAINING_OWNERSHIP_SUBMISSION.json';dispatch=read(dispatch_path)
assert report['status']=='passed-finite-owned-feat-chains' and not report['failures']
assert report['counts']['ownedFeatPredicateIdentities']==10 and report['counts']['remainingCredentialDependentIdentities']==56
assert dispatch['sent'] and not dispatch['wholeExactCandidateApprovalRequested']
for source in report['sourceBindings']:assert info(G/source['path'])==source,source['path']
for key in ['archive','request','submissionScreenshot']:assert info(G/dispatch[key]['path'])==dispatch[key]
now=datetime.now(timezone.utc).isoformat()
ledger_path=R/'data/playtest/game_development_coverage.json';before=read(ledger_path);ledger=deepcopy(before)
changed={'DD-06','DD-14','DD-69'}
for row in ledger['aspects']:
    if row['id'] not in changed:continue
    row.setdefault('validationEvidence',[]).append(report_path.relative_to(G).as_posix())
    row.setdefault('reviewEvidence',[]).append(dispatch_path.relative_to(G).as_posix())
    row.setdefault('completedScopes',[]).append(
        'Ten additional owned-feat prerequisite trees have32 source-qualified partial histories and201 passing local checks. '
        'Earlier feats consume actual class ASIs and satisfy their own prerequisites; exact IDs, permanent Athlete/weapon/maneuver/ability choices, '
        'and bounded reserve/superiority initialization fields are checked. No full feat or class build/use approval is implied. '
        'The ten-identity and earlier48-training evidence packets were submitted together for actual GPT focused evidence review; reply pending at this checkpoint.')
    row.setdefault('currentEvidenceAddenda',[]).append({
        'id':'FEAT-EXACT-01-OWNED-FEAT-10','recordedAtUtc':now,'status':'finite-paid-history-evidence-focused-review-pending',
        'report':report_path.relative_to(G).as_posix(),'notes':notes_path.relative_to(G).as_posix(),
        'actualGptDispatch':dispatch_path.relative_to(G).as_posix(),'newSourceRuleOrReviewApproval':False,
    })
    if row['id']=='DD-14':
        row.setdefault('historicalOpenIssueSnapshots',[]).append({
            'recordedAtUtc':now,'reason':'Preserve the earlier66-identity remaining prerequisite checkpoint.',
            'status':row['status'],'openIssues':deepcopy(row['openIssues']),
        })
        assert '66 other credential-dependent' in row['openIssues'][1]
        row['openIssues'][1]=('FXC-05 predicate evidence covers209 numeric/level/None,12 Warrior mutation,48 training and10 owned-feat identities, '
            'with56 other credential-dependent identities remaining. The ten-identity pass supplies32 partial paid histories and201 passing local checks. '
            'The48+10 reports and full current inputs are in an actual pending GPT focused evidence review. '
            'These disjoint scopes do not establish279 complete acquisitions or approve the exact candidate. '
            'Complete class-card builds, all selection/initial resource fields and use procedures remain separate.')
for old,new in zip(before['aspects'],ledger['aspects']):
    assert old['id']==new['id'] and old.get('closure')==new.get('closure') and old.get('humanEvidence')==new.get('humanEvidence')
    if old['id'] not in changed:assert old==new
assert {x['id'] for x,y in zip(before['aspects'],ledger['aspects']) if x!=y}==changed
nav=R/'tools/build_review_map.py';text=nav.read_text(encoding='utf-8')
anchor='        "FEAT_EXACT_01_TRAINING_COVERAGE_DELTA.json",'
assert text.count(anchor)==1
text=text.replace(anchor,anchor+'\n        "FEAT_EXACT_01_OWNED_FEAT_COVERAGE_DELTA.json",')
anchor='        ("Feat training prerequisites — 184 checked cases", "FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json"),'
assert text.count(anchor)==1
text=text.replace(anchor,anchor+'\n'
 '        ("Feat ownership — ten prerequisite chains", "FEAT_EXACT_01_OWNED_FEAT_CHAIN_NOTES.md"),\n'
 '        ("Feat ownership — 32 paid histories and checks", "FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json"),\n'
 '        ("Training and ownership — actual focused GPT dispatch", "FEAT327_FXC05_TRAINING_OWNERSHIP_SUBMISSION.json"),\n'
 '        ("Training and ownership — focused review request", "FEAT327_FXC05_TRAINING_OWNERSHIP_REQUEST.txt"),')
anchor='66 other credential-dependent identities remain. These are prerequisite/payment projections, not269 complete feat acquisitions; full choice, resource and use work remains.'
assert text.count(anchor)==1
text=text.replace(anchor,'A further ten owned-feat prerequisite trees now have32 partial paid histories and201 passing checks, with exact parent IDs, own prerequisites and required acquisition choices.56 other credential-dependent identities remain. The48-training and ten-ownership evidence, with34 full payloads, was submitted to actual GPT for focused evidence review; that reply is pending. These are prerequisite/payment projections, not279 complete feat acquisitions; full choice, resource and use work remains.')
compile(text,str(nav),'exec')
saved=[]
for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
    original=info(p);q=preservation/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==p.read_bytes()
    saved.append({**original,'preservedCopy':q.relative_to(G).as_posix()})
manifest=preservation/'PRESERVATION_MANIFEST.json';write(manifest,saved)
write(ledger_path,ledger)
delta={'recordedAtUtc':now,'status':'verified-scoped-coverage-update',
 'before':next(x for x in saved if x['path']==ledger_path.relative_to(G).as_posix()),'after':info(ledger_path),
 'aspectsChanged':sorted(changed),'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,
 'previousFeatOpenIssuesPreservedVerbatim':True,'validation':[info(report_path),info(notes_path)],
 'previousCoverageDelta':info(A/'FEAT_EXACT_01_TRAINING_COVERAGE_DELTA.json'),
 'actualGptDispatch':info(dispatch_path),'newSourceRuleOrReviewApproval':False}
write(delta_path,delta);nav.write_text(text,encoding='utf-8',newline='\n')
result=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
if result.returncode:print(result.stderr);raise SystemExit(result.returncode)
navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
assert info(G/'REVIEW_MAP.html')['sha256']==navigation['sha256']
for source in report['sourceBindings']:assert info(G/source['path'])==source
state=read(previous)
state.update({
 'recordedAtUtc':now,'goalTurnClassification':'progress','previousGoalTurnClassification':'progress:48 source-qualified training identities and preserved navigation/coverage.',
 'previousCheckpoint':info(previous),
 'status':'Ten additional owned-feat prerequisite identities have32 partial paid histories and201 passing checks;56 other credential-dependent predicates remain. Both new48+10 evidence packets are submitted to actual GPT for a focused evidence check. Exact-candidate approval, full acquisitions/use and whole-game work remain open.',
 'featOwnedFeatPrerequisitePass':{'report':info(report_path),'notes':info(notes_path),'counts':report['counts'],'checks':report['checks'],
    'checkKinds':report['checkKinds'],'failures':0,'scope':report['scope'],'limits':report['limits'],
    'model':info(R/'tools/feat_exact_01_owned_feat_model.py'),'validator':info(R/'tools/validate_feat_exact_01_owned_feat_chains.py'),
    'allCohortCompleteAcquisitionsValidated':False,'candidateReadyForSubmission':False,'noNewRulesAdopted':True},
 'activeGptReview':{'id':dispatch['reviewId'],'status':'submitted-visible-responding','dispatch':info(dispatch_path),
    'chatUrl':dispatch['chatUrl'],'browserId':dispatch['browserId'],'tabId':dispatch['tabId'],'requestMessageId':None,
    'wholeExactCandidateApprovalRequested':False,'replyReceived':False,
    'observationLimit':'The message/attachment and responding UI were observed; a DOM identity lookup timeout is not a failed send. Do not resend.'},
 'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
 'coverageLedger':info(ledger_path),'coverageDelta':info(delta_path),
 'navigationBindingPolicy':'Explicit preserved coverage steps now chain Warrior -> Training -> Owned-feat evidence. Current source corrections remain separately bound by ACQ-01/02; no blanket hash mismatch exemption.',
})
state['safeNextActions']=[
 'Poll the same actual Calibration Review Part2 chat for FEAT327-FXC05-TRAINING-OWNERSHIP. Chrome3 tab125745639 showed the submitted34-payload ZIP and ChatGPT responding. Preserve the final response and apply only any concrete source-backed finite corrections. No new whole-candidate approval was requested; do not resend because an identity-read observation timed out.',
 'Continue independent FXC-05 work on the56 /remaining identities in FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json: actual spellcasting/repertoire, supplementary Spell Focus, remaining paid ownership chains, lineage/trade/context receipts. Cohorts209+12+48+10 are disjoint partial predicate scopes, not279 complete acquisitions.',
 'The ten owned-feat report has32 histories/201 passing checks and complete involved source procedures plus six maneuver profiles. Required parent choices are recorded; Giant Slayer/Slayer\'s Resolve parent histories also meet level8 and do not isolate a hypothetical earlier grant. The old-spent-die case is a stated legitimate-spend premise, not a tested attack.',
]+state['safeNextActions'][1:]
state.setdefault('preservationManifests',[]).extend([info(manifest),info(A/'fxc05-evidence-before-readme-wording-correction/PRESERVATION_MANIFEST.json')])
with target.open('x',encoding='utf-8',newline='\n') as stream:json.dump(state,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps({'checkpoint':info(target),'coverage':info(ledger_path),'navigationLinks':navigation['existingDistinctLinks'],
 'missingLinks':0,'ownedFeatPredicateIdentities':10,'remainingCredentialDependentIdentities':56,
 'actualGptReviewPending':dispatch['reviewId'],'sourceInformationDeleted':False,'pushed':False,'cosmologyReviewed':False},indent=2))
