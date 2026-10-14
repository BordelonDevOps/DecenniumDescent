"""Preserve navigation and record the first bounded feat acceptance pass once."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil
import subprocess
import sys

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}

rp=A/'FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json';report=read(rp)
assert report['failureCount']==0 and report['caseGroups']==28 and not report['candidateReadyForSubmission']
for b in report['sourceBindings']:assert info(G/b['path'])==b,b['path']
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_ASSEMBLY.json'
target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_BOUNDARIES.json'
notes=A/'FEAT_EXACT_01_BOUNDARY_REFERENCE_NOTES.md'
folder=A/'navigation-before-feat-exact-01-boundaries'
assert not target.exists() and not notes.exists() and not folder.exists()

nav=R/'tools/build_review_map.py';s=nav.read_text('utf-8')
def once(before,after):
    global s
    assert s.count(before)==1,before
    s=s.replace(before,after)
once('    pending = [\n','    pending = [\n        ("Feat acceptance boundaries — scope and remaining work", "FEAT_EXACT_01_BOUNDARY_REFERENCE_NOTES.md"),\n        ("Feat acceptance boundaries — reproducible reference checks", "FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json"),\n')
once('The finite FXC state-boundary cases, full evidence package and actual exact review remain outstanding.',
     'A first finite reference pass now represents all28 extra FA expectations with explicit executed subsets and unexecuted premise limits:362 checks pass, including204 bounded state/predicate checks,7 arithmetic,102 unchanged input bindings,28 full procedure equalities,18 source-data,2 source-adjudication and1 coverage check. These do not execute all660 original examples or close FXC-04–10. The remaining finite acceptance evidence, full package and actual exact review remain outstanding.')
compile(s,str(nav),'exec')
manifest={}
for p in [nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
    old=info(p);q=folder/old['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    assert p.read_bytes()==q.read_bytes()
    manifest[old['path']]={**old,'preservedCopy':q.relative_to(G).as_posix()}
(folder/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

lines=['# Feat candidate: first bounded acceptance pass','',
       'The complete feat text remains an unapproved exact candidate. This pass checks named subsets of all 28 additional GPT-authored boundary expectations. It does not execute the full 660 original examples, authenticate campaign facts, or establish whole-game readiness.','',
       f"**Result:** {report['checkCount']} checks, {report['failureCount']} failures. No source rules, candidate text, original examples or live catalogs changed.",'',
       '| Evidence kind | Checks |','|---|---:|']
lines += [f'| {k} | {v} |' for k,v in report['checkKinds'].items()]
lines += ['', 'The prior unexecuted draft reference model was preserved before correcting its exact-rest endpoint order, suppressed cause credit, known-illegal command commitment, explicit Mutation Efficiency prerequisite, and meaningful-hostile predicate. These were corrections to the test model against existing reviewed source directions, not new game rules.','',
          '[Complete inputs, expected/actual values and limits](FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json).',
          '[Original GPT expectations](feat327-source-verdict/FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json).',
          '[Finite acceptance contract](feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md).','',
          '## Named case subsets','']
for c in report['cases']:
    lines += [f"### {c['caseId']} — {c['sourceExpectation']['name']}",'',
              c['executedSubset'],'',f"Premises: {c['suppliedPremises']}",'',
              f"Limits: {c['notExecutedByThisModel']}",'']
    if c.get('authoredAdjudication'):lines += [c['authoredAdjudication'],'']
lines += ['## Remaining acceptance work','']+[f'- {x}' for x in report['remainingAcceptanceWork']]
lines += ['', '## Reproduce','',
          'Run `tools/validate_feat_exact_01_boundaries.py --report <new-output-file.json>` with Python. The script rejects an existing report destination to preserve evidence. It imports only the separate bounded reference models, compares all recorded assembly inputs, and creates no runtime selections.','',
          'The GPT source conference is complete; no new message was sent for this local pass. The next GPT submission is the complete manifest-bound exact candidate after its remaining finite acceptance work. The authorized order remains final joint whole-game review, GitHub push and remote verification, then careful cosmology review.','']
notes.write_text('\n'.join(lines),encoding='utf-8')
nav.write_text(s,encoding='utf-8',newline='\n')
result=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
if result.returncode:
    print(result.stderr);raise SystemExit(result.returncode)
n=read(A/'REVIEW_MAP_BUILD.json')
assert not n['missingLinks'] and n['sha256']==info(G/'REVIEW_MAP.html')['sha256']

state=read(previous)
state.update({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'goalTurnClassification':'progress',
              'previousGoalTurnClassification':'progress: complete feat exact-candidate text assembled and independently checked; no exact approval.',
              'previousCheckpoint':info(previous),
              'status':'First bounded acceptance pass represents28 additional FA expectations with executable subsets and explicit source-adjudication/premise limits.362 checks pass, including102 unchanged source/candidate bindings. Complete feat text unchanged and unapproved; remaining FXC work, package and actual exact review remain.',
              'featBoundaryReferencePass':{'report':info(rp),'notes':info(notes),
                   'models':info(R/'tools/feat_exact_01_reference_models.py'),
                   'validator':info(R/'tools/validate_feat_exact_01_boundaries.py'),
                   'caseGroups':28,'checks':report['checkCount'],'failureCount':0,'checkKinds':report['checkKinds'],
                   'fullFeatRuntimeCases':0,'all660OriginalExamplesExecuted':False,'closesFXC04Through10':False,
                   'priorModelPreservation':info(A/'feat-exact-01-reference-model-before-boundary-corrections/PRESERVATION_MANIFEST.json'),
                   'notableSourceGrounding':'EX01-03 safe Rest completing exactly at debt deadline clears debt before assessment. Actual Mage3max8,Dragoon8max7,Warrior7zeroRP; actual Warrior slots1/5/13/20 and owned Mutation Efficiency/Apex requirements.'},
              'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':n['existingDistinctLinks'],'missingLinks':[]}})
state['activeGptReview']['currentAuthoritativeObservation']='Actual GPT source verdict complete and verified. No active unanswered request. This pass added only local bounded acceptance evidence; no new GPT message sent.'
state['safeNextActions']=[
    'Continue remaining finite acceptance from FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json and its explicit per-case limits. All28 FA records now have named executable subsets/source adjudication, not full campaign-runtime proof. Do not recount362 checks as362 fully simulated feat scenarios.',
    'Prioritize FXC-05 exhaustive acquisition/repeatability fixtures:335 exact IDs,175 printed prerequisite values in FEAT_EXACT_01_ACQUISITION_INVENTORY.json. Combine original gates with full per-feat directions, six fixed training branches,8 reviewed unchanged,12 Warrior identity pairs and actual class/ancestry/credential sources. Do not fabricate an all-heritage actor or treat stored strings as proved qualification.',
    'Complete FXC-04 operative supplement row qualification and FXC-07–09 remaining full source-based state sequences, including genuine task/natural-shift/opposed/save/reroll procedure, Ready/concentration, paid-copy costs/history/interruption, Quickened Thought, plant phases and unchanged actual no-resource exceptions.',
    'For FXC-10 audit all660 original authored examples against actual prerequisite/HP/resource/clock premises. The new28 FA pass explicitly distinguishes reference calculations from unexecuted physical/social/campaign facts; it does not validate all660 originals.',
    'The first boundary runner is reproducible with --report NEW_PATH; its default refuses overwrite. Both scripts and14 source bindings are bound in the report. Do not edit them after that receipt without preserving current bytes and issuing a new correction report. The unexecuted earlier model is preserved under feat-exact-01-reference-model-before-boundary-corrections.',
    'Exact candidate text/data/docs remain unchanged from assembly; all47 emitted artifact bindings and original source bindings still pass. Preserve current bytes before any later source-directed correction. Never rerun the one-use initial/resume builder over completed outputs.',
    'Only when finite acceptance evidence is complete, package all full exact files and submit to actual GPT Calibration Review Part2 (thread6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b; browser handlefeatVerdictTab/tab125745656, original user tab125745612). No active unanswered request exists; do not resend the old continuation or reopen generic source conference.',
    'Higher spells remain180 complete unadopted proposals/360 examples,208 pre-push procedures still to propose; all await dedicated GPT review. Preserve47 higher deferred receipts and Blink. Ordinary spells412reviewed/436pending; other catalogs and whole-game review remain open.',
    'User file-access question is answered: GPT temporary-workspace unreadable file outputs, not local source loss. Source-verdict archive was recovered,hash-verified and3884 checks reproduced. Do not keep reporting an active file-access block.',
    'After final actual joint whole-game confirmation, perform already-authorized GitHub push, verify remote commit, then careful cosmology review. No deletion/promotion/push/cosmology has occurred.'
]
state.setdefault('preservationManifests',[]).append(info(folder/'PRESERVATION_MANIFEST.json'))
target.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checkpoint':info(target),'notes':info(notes),'report':info(rp),'navigationLinks':n['existingDistinctLinks'],
                  'readyForSubmission':False,'sourceInformationDeleted':0,'newGptMessages':0},indent=2))
