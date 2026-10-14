"""Freeze the complete authored advanced candidates for the separate exact review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, zipfile

R=Path(__file__).resolve().parents[1]; G=R.parents[1]; A=G/'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(G).as_posix()
def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

README='''# Advanced crafting: all 167 exact authored candidates

This is the requested separate exact authored-operational review, following the final source-authoring verdict and ADV-EDIT-01. All167 actual internal cards, all100 actual player cards, complete guides/manuscripts,22 internal/15 public body defaults or variants,50 actual weapon/suit host templates,37 qualitative sequences and current numerical evidence are included under their real repository-relative paths. FILE_MANIFEST.json binds every payload's exact bytes. No installation or network access is needed.

## Start with these actual documents

Under DescentReviewChanges/ReviewBible/:
- data/director/advanced_craft_recipe_candidate_internal.json: complete originals, operational fields and rendered manuscriptText for all167, complete procedure sections, original body profiles plus controlling corrections, all48 class-interface dispositions, version/name history and source hashes.
- data/crafting/advanced_craft_recipe_candidate_public.json: all100 player projections, full operatingGuideText/bodyGuideText,15 body profiles and50 host templates.
- docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md and ADVANCED_CRAFT_INTERNAL_BODY_CATALOGUE.md: complete governing operational text and body definitions. Historical conflicting text is preserved and expressly superseded by ADV-EDIT-01.
- docs/director-only/{ENCHANTING,RUNE_CARVING,SCRIBING,TINKERING}_INTERNAL_RECIPE_CARDS.md: the complete actual167 rendered cards.
- docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md and ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md, plus {ENCHANTING,RUNE_CARVING,SCRIBING,TINKERING}_CANDIDATE_RECIPE_CARDS.md: the whole actual player envelope. Review the prose and operating dependencies, not only equal effect fields.
- docs/director-only/ADVANCED_CRAFT_PHYSICAL_SEQUENCE_CASEBOOK.md: all19 W fixtures,18 further E sequences with explicit rejected alternatives, and22 body boundaries. These are authored expected adjudications requiring your semantic review, not automated runtime passes.

## Authority and corrections

Under docs/audit/2026-10-08/full-game/:
- GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md is the FINAL 171095-byte source verdict, SHA256 48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0, reply af2a24f6-c967-4aa5-a28e-5c2e9de13cb6. The exact final13-file package is preserved in advanced167-source-authoring-reviewer-files/. Earlier live draft values are not authority.
- GPT_ADVANCED_TRAP_SPRING_CLARIFICATION.md and ADVANCED_TRAP_SPRING_INTEGRATION.json bind ADV-EDIT-01, reply a01ad150-d04b-4fb8-ae18-9ea476535a93: original trap frame/discharge block are primary; compatible spring and separate subordinate contacts are replaceable through actual restoration. All11 trap cards and shared body/repair rules carry this correction. Automaton primary actuators are unchanged.
- ADVANCED_CRAFT_PLAYER_DISSONANCE_CORRECTION.json records a local adaptation error corrected before this submission: TD-08 routes up to TWO current Dissonance into ONE own actual active qualifying device within30 feet. The player guide and embedded JSON now agree with the complete source section. This is not a new class ruling. Prior local files remain archived outside this active envelope.
- All138 source/dependency files of the earlier submission are included unchanged. ADVANCED_CRAFT_JOINT_SUBMISSION.json binds their original hashes. Source/register checks5248/1623 reproduced identically; ADVANCED_CRAFT_LOCAL_SOURCE_VERIFICATION.json records this finite scope.

## Validation, scope and reproduction

ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json:5770 complete-source, source-index/book/manuscript, preserved-field and finite-arithmetic assertions. ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json:1725 assertions independently reconstructing every projected component occurrence, preserving all600 book paragraphs and checking the entire public envelope for withheld fields/memberships. All343 public component mentions remain;100 supplemental profiles have independent public authority. ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json preserves every exclusion internally.

ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json:52 grouped numeric/coverage assertions;2004 recipe×six-band×two-option cases,519 structural contexts,4560 transitions over eight distinct ordinary B values,185 damaged-chassis conversions,410 restoration quotations,59 maintenance-pack variants,36 missing-primary rejection inputs. Inapplicable manufacturing choices are explicitly labeled. Shared Core/structural/quotation calculations are reused only for identical mathematics; this does not import Fishing item effects or implement an advanced crafting runtime.

From the extracted repository root, Python3 standard library is sufficient for:
python DescentReviewChanges/ReviewBible/tools/validate_advanced_craft_internal_candidates.py
python DescentReviewChanges/ReviewBible/tools/validate_advanced_craft_public_candidates.py
python DescentReviewChanges/ReviewBible/tools/validate_advanced_craft_worked_cases.py
These validators write their named reports. Run them in a working copy after preserving the supplied manifest snapshot if retaining exact submitted evidence. Do not rerun the one-use authoring/correction/checkpoint builders. Their code is provenance, not a reviewer setup command.

Numeric passes are not proof of authentic stock, anatomy, access, consent, world events, protocol compatibility, functional spell payloads, table balance or companion runtime. The37 qualitative cases are expected rulings for review. In particular check event ordering, live eligibility/fallback, spent-resource persistence, class device interfaces and legitimate failure paths against the full source directions.

## Requested verdict and boundaries

Inspect all167 actual cards, all100 player projections, their complete shared guides and body dependencies; assess all37 sequences and every current source-authoring section. Give one exact authored-operational verdict and an exhaustive finite list of actual corrections with affected IDs/fields and replacement wording. State whether completing those named corrections and appropriate checks permits promotion without a further generic conference. If something was inaccessible or uninspected, identify it rather than approving unseen material.

Retain all source fields, nulls, original manuscripts, history and the genuine particular-operation prerequisites. Unsupported operations remain unavailable; a price, name, declared boolean or check pass supplies no missing campaign fact. Missing spell payloads and later feat/bestiary/language interfaces remain bounded dependencies rather than grounds for repeating the settled preliminary source conference. No class card or pending feat is promoted by this recipe review.

Current totals remain520/687 recipes and333/433 public reviewed, with167/100 candidates awaiting this exact verdict. The separate complete authored game and final joint whole-game flow confirmation still precede the authorized GitHub push; remote-commit verification precedes careful cosmology review. No deletion, push, cosmology interpretation, runtime implementation, human balance approval or publication claim occurs in this submission.
'''

def main():
    archive=A/'DD_Advanced_Craft_167_Exact_Review_v1.zip'
    receipt=A/'ADVANCED_CRAFT_EXACT_REVIEW_PREPARATION.json'
    assert not archive.exists() and not receipt.exists(), 'Use a new revision; preserve the frozen handoff'
    internal=R/'data/director/advanced_craft_recipe_candidate_internal.json'
    public=R/'data/crafting/advanced_craft_recipe_candidate_public.json'
    iv=read(A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json')
    pv=read(A/'ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json')
    wv=read(A/'ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json')
    assert iv['status']=='PASS' and iv['candidateSha256']==sha(internal) and iv['checks']==5770
    assert pv['status']=='PASS' and pv['publicCandidateSha256']==sha(public) and pv['checks']==1725
    assert wv['status'].startswith('PASS') and not wv['failedChecks'] and wv['internalCandidateSha256']==sha(internal)
    protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
    assert len(protected)==138 and all(sha(G/p)==h for p,h in protected.items())
    d=read(internal);p=read(public)
    assert len(d['cards'])==167 and len(p['cards'])==100 and not d['exactRecipeApproval'] and not p['exactRecipeApproval']
    backup=A/'advanced167-before-exact-review-preparation'
    assert not backup.exists()
    backup.mkdir()
    for name in ['ADVANCED_CRAFT_CANDIDATE_READINESS.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json']:
        file=A/name;shutil.copy2(file,backup/name);obj=read(file)
        obj['status']='authored-candidate-local-numeric-checks-pass-awaiting-exact-semantic-review'
        obj['localNumericValidationComplete']=True
        obj['qualitativeSequencesAuthored']=37
        obj['qualitativeExactReviewPending']=True
        obj['stateSequenceValidationComplete']=False
        obj['exactReviewSubmitted']=False
        obj['nextAction']='Submit the complete frozen167 exact-candidate package for separate GPT authored-operational review.'
        obj['publicCandidateSha256']=sha(public)
        obj['workedCaseReport']='ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json'
        obj['workedCaseCounts']=wv['counts']
        if 'remainingWork' in obj:obj['remainingWork']=['Exact semantic review of all167 candidates,100 complete public projections and37 qualitative sequences','Integrate actual named corrections and appropriate checks before any promotion']
        dump(file,obj)
    files={G/path for path in protected}
    files.update((A/'advanced167-source-authoring-reviewer-files').glob('*'))
    files.update([internal,public,Path(__file__).resolve()])
    for folder,suffix,guide,body in [('director-only','INTERNAL','ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md','ADVANCED_CRAFT_INTERNAL_BODY_CATALOGUE.md'),('mechanics','CANDIDATE','ADVANCED_CRAFT_CANDIDATE_GUIDE.md','ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md')]:
        files.update([R/'docs'/folder/guide,R/'docs'/folder/body])
        files.update(R/'docs'/folder/f'{trade}_{suffix}_RECIPE_CARDS.md' for trade in ['ENCHANTING','RUNE_CARVING','SCRIBING','TINKERING'])
    files.add(R/'docs/director-only/ADVANCED_CRAFT_PHYSICAL_SEQUENCE_CASEBOOK.md')
    for name in ['GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md','ADVANCED_CRAFT_SOURCE_VERDICT_CAPTURE.json','GPT_ADVANCED_TRAP_SPRING_CLARIFICATION.md','ADVANCED_TRAP_SPRING_INTEGRATION.json','ADVANCED_CRAFT_PLAYER_DISSONANCE_CORRECTION.json','ADVANCED_CRAFT_LOCAL_SOURCE_VERIFICATION.json','ADVANCED_CRAFT_JOINT_SUBMISSION.json','ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json','ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json','ADVANCED_CRAFT_INTERNAL_MANUFACTURING_OUTCOMES.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json','ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json','ADVANCED_CRAFT_CANDIDATE_READINESS.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json','ADVANCED_CRAFT_AUTHORED_SEQUENCE_CASES.json','ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json']:
        files.add(A/name)
    for name in ['build_advanced_craft_internal_candidates.py','build_advanced_craft_public_candidates.py','build_advanced_craft_sequence_casebook.py','apply_advanced_trap_spring_clarification.py','correct_advanced_player_dissonance_wording.py','validate_advanced_craft_internal_candidates.py','validate_advanced_craft_public_candidates.py','validate_advanced_craft_worked_cases.py','core_playtest_rules.py','spell_playtest_rules.py','fishing_reference.py']:
        files.add(R/'tools'/name)
    assert all(f.is_file() for f in files), [str(f) for f in files if not f.is_file()]
    manifest={rel(f):{'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(files,key=rel)}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README_EXACT_REVIEW.md',README.encode())
        z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
        for file in sorted(files,key=rel):z.write(file,rel(file))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(manifest)+2==len(set(z.namelist()))
        assert all(hashlib.sha256(z.read(path)).hexdigest()==m['sha256'] for path,m in manifest.items())
    result={'status':'PASS frozen complete exact-review preparation; UNSENT','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'bundleFile':archive.name,'bundleBytes':archive.stat().st_size,'bundleSha256':sha(archive),'payloadFiles':len(manifest),'currentFileHashes':{k:v['sha256'] for k,v in manifest.items()},'internalCandidateSha256':sha(internal),'publicCandidateSha256':sha(public),'internalCards':167,'publicCards':100,'qualitativeSequences':37,'localNumericCounts':wv['counts'],'sent':False,'newApprovals':0,'githubPushPerformed':False,'cosmologyReviewed':False}
    dump(receipt,result)
    prompt=f'''Codex exact advanced-crafting review. The attached {archive.name} contains ALL167 actual complete Enchanting/Rune Carving/Scribing/Tinkering candidates, their originals, full internal/public JSON and manuscripts,100 complete player projections,22/15 body variants,50 actual host templates,48 class-interface dispositions and37 authored qualitative sequences. This is the separate exact-candidate review you requested, not another source conference. Archive SHA256 {sha(archive)}; {len(manifest)} payload files.

Please open README_EXACT_REVIEW.md and FILE_MANIFEST.json, then inspect all actual cards, shared guides and the whole public envelope. The FINAL source verdict is SHA48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0 and its original13-file package is included. ADV-EDIT-01 is applied beside preserved originals to all11 trap cards and body/repair rules. A local player-guide transcription error was also corrected before handoff: TD-08 moves up to TWO current Dissonance into ONE own active qualifying device within30ft. The complete correction record is included; original class cards are unchanged.

Local evidence:5770 source/book/manuscript/field checks,1725 full public-envelope checks,52 grouped numeric/coverage checks. Detailed2004 manufacturing rows,519 structural contexts,4560 transitions,185 chassis conversions,410 repair quotes,59 maintenance packs and36 omitted-primary inputs are included. These are finite source-bound arithmetic checks, not an advanced runtime or actual campaign authentication. The37 sequence dispositions are explicitly authored expectations for your semantic assessment. All138 original submitted source files remain byte-identical.

Please return ONE exact authored-operational verdict covering all167 candidates, all100 public envelopes and37 sequences, with an exhaustive finite list of actual corrections if necessary. Identify affected recipe IDs/fields and exact replacement wording. State explicitly whether the named corrections plus appropriate checks permit promotion without another generic conference. Source directions are settled; retain genuine particular-operation prerequisites without expanding hypothetical edge cases into a new preliminary-source queue. If any files cannot be opened or were not inspected, identify the limitation rather than approving unseen material. Reproduction uses Python standard library only; run validators in a working copy because they write reports.

No new approvals inferred: totals remain520/687 recipes and333/433public. No class/feat promotion, deletion, push or cosmology review. The owner's final whole-game flow confirmation precedes the authorized push; verified remote commit precedes careful cosmology review.'''
    (A/'CODEX_ADVANCED_CRAFT_EXACT_REVIEW_PROMPT.txt').write_text(prompt+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='currentFileHashes'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
