"""One-use navigation/coverage update for the finite 48-feat training pass."""
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
    data=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(data),'sha256':sha256(data).hexdigest()}
def write(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_TRAINING_PREREQUISITES.json'
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_WARRIOR_ACQUISITIONS.json'
preservation=A/'navigation-and-coverage-before-feat-exact-01-training-prerequisites'
delta_path=A/'FEAT_EXACT_01_TRAINING_COVERAGE_DELTA.json'
assert not target.exists() and not preservation.exists() and not delta_path.exists(),'One-use checkpoint already started'
report_path=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json'
notes_path=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_NOTES.md'
fixture_path=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json'
report=read(report_path)
assert report['status']=='passed-finite-training-projections' and not report['failures']
assert report['counts']['trainingPredicateFeats']==48 and report['counts']['remainingCredentialDependentFeats']==66
assert not report['allTrainingCohortCompleteAcquisitionsValidated']
for source in report['sourceBindings']:assert info(G/source['path'])==source,source['path']

now=datetime.now(timezone.utc).isoformat()
ledger_path=R/'data/playtest/game_development_coverage.json'
before=read(ledger_path);ledger=deepcopy(before)
changed_ids={'DD-06','DD-14','DD-69'}
scope=('48 training prerequisite trees now have184 source-qualified synthetic cases and1917 passing checks. '
       'Actual first-class skill/tool choices, Human/Imperial bonuses once, background training, permanent skill modifiers, '
       'paid Skill Expert/Naturalist training and actual earned/unspent feat opportunities are represented. '
       'Weapon ownership, thrown/Versatile properties, missing credentials and repeat purchases are distinguished. '
       'These are partial prerequisite/payment projections, not complete class builds, feat acquisitions, full runtime or approval.')
for row in ledger['aspects']:
    if row['id'] not in changed_ids:continue
    row.setdefault('validationEvidence',[]).append(report_path.relative_to(G).as_posix())
    row.setdefault('completedScopes',[]).append(scope)
    row.setdefault('currentEvidenceAddenda',[]).append({
        'id':'FEAT-EXACT-01-TRAINING-48','recordedAtUtc':now,'status':'finite-prerequisite-payment-evidence-only',
        'report':report_path.relative_to(G).as_posix(),'notes':notes_path.relative_to(G).as_posix(),
        'newSourceRuleOrReviewApproval':False,
    })
    if row['id']=='DD-14':
        row.setdefault('historicalOpenIssueSnapshots',[]).append({
            'recordedAtUtc':now,'reason':'Preserve the earlier114-identity remaining prerequisite checkpoint.',
            'status':row['status'],'openIssues':deepcopy(row['openIssues']),
        })
        assert '114 other credential-dependent' in row['openIssues'][1]
        row['openIssues'][1]=('FXC-05 predicate evidence covers209 numeric/level/None identities,12 Warrior mutation identities '
            'and48 training identities, with66 other credential-dependent identities remaining. '
            'The48 training pass supplies184 source-qualified partial cases and1917 passing checks; '
            'spellcasting, lineage, owned-feat, trade and context receipts remain. '
            'These disjoint predicate scopes do not establish269 complete feat acquisitions or approval. '
            'Complete feat choices, initial resources, class-card builds and use procedures remain separate.')
for old,new in zip(before['aspects'],ledger['aspects']):
    assert old['id']==new['id']
    assert old.get('closure')==new.get('closure') and old.get('humanEvidence')==new.get('humanEvidence')
    if old['id'] not in changed_ids:assert old==new
assert {x['id'] for x,y in zip(before['aspects'],ledger['aspects']) if x!=y}==changed_ids

nav=R/'tools/build_review_map.py';text=nav.read_text(encoding='utf-8')
start=text.index('    coverage_delta = read(A / "FEAT_EXACT_01_WARRIOR_COVERAGE_DELTA.json")')
end=text.index('\n\n\ndef main():',start)
old_helper=text[start:end]
assert 'assert current_sha == entry["after"]["sha256"]' in old_helper
new_helper='''    coverage_deltas = [read(A / name) for name in [
        "FEAT_EXACT_01_WARRIOR_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_TRAINING_COVERAGE_DELTA.json",
    ]]
    chain = list(entries.values()) + coverage_deltas
    visited = set()
    while expected_sha != current_sha:
        assert expected_sha not in visited, ("Cyclic binding history", rel)
        visited.add(expected_sha)
        matches = [entry for entry in chain if entry["after"]["path"] == rel
                   and entry["before"]["sha256"] == expected_sha]
        assert len(matches) == 1, ("Unrecorded or ambiguous current-file change", rel)
        entry = matches[0]
        assert digest(G / entry["before"]["preservedCopy"]) == expected_sha, rel
        expected_sha = entry["after"]["sha256"]'''
text=text[:start]+new_helper+text[end:]
anchor='        ("Warrior feats — acquisition and activation checks", "FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json"),'
assert text.count(anchor)==1
text=text.replace(anchor,anchor+'\n'
    '        ("Feat training prerequisites — 48 source-qualified examples", "FEAT_EXACT_01_TRAINING_PREREQUISITE_NOTES.md"),\n'
    '        ("Feat training prerequisites — complete source fixtures", "FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json"),\n'
    '        ("Feat training prerequisites — 184 checked cases", "FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json"),')
old_sentence='The other126 identities still require actual proficiency, spell, lineage, mutation, owned-feat, trade or context credentials.'
assert text.count(old_sentence)==1
text=text.replace(old_sentence,'The following credential-dependent passes extend that numeric-only checkpoint.')
old_sentence='Only this named issue is closed.114 other credential-dependent identities and broader feat acquisition/use work remain.'
assert text.count(old_sentence)==1
text=text.replace(old_sentence,'Only this named issue is closed. A further48 training prerequisite identities now have184 source-qualified partial cases and1917 passing checks, including actual starting training, permanent skill totals, paid Expertise, weapon profiles and earned/unspent opportunities.66 other credential-dependent identities remain. These are prerequisite/payment projections, not269 complete feat acquisitions; full choice, resource and use work remains.')
compile(text,str(nav),'exec')

preserved=[]
for path in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
    original=info(path);copy=preservation/path.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(path,copy);assert copy.read_bytes()==path.read_bytes()
    preserved.append({**original,'preservedCopy':copy.relative_to(G).as_posix()})
manifest=preservation/'PRESERVATION_MANIFEST.json';write(manifest,preserved)
write(ledger_path,ledger)
delta={
 'recordedAtUtc':now,'status':'verified-scoped-coverage-update',
 'before':next(x for x in preserved if x['path']==ledger_path.relative_to(G).as_posix()),'after':info(ledger_path),
 'aspectsChanged':sorted(changed_ids),'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,
 'previousFeatOpenIssuesPreservedVerbatim':True,'validation':[info(report_path),info(notes_path)],
 'previousCoverageDelta':info(A/'FEAT_EXACT_01_WARRIOR_COVERAGE_DELTA.json'),
 'newSourceRuleOrReviewApproval':False,
}
write(delta_path,delta)
nav.write_text(text,encoding='utf-8',newline='\n')
result=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
if result.returncode:print(result.stderr);raise SystemExit(result.returncode)
navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
assert info(G/'REVIEW_MAP.html')['sha256']==navigation['sha256']
for source in report['sourceBindings']:assert info(G/source['path'])==source
state=read(previous)
state.update({
 'recordedAtUtc':now,'goalTurnClassification':'progress','previousGoalTurnClassification':'progress: twelve Warrior witnesses and fulfilled actual GPT ACQ-02.',
 'previousCheckpoint':info(previous),
 'status':'48 additional training prerequisite identities have184 source-qualified partial cases and1917 passing checks;66 other credential-dependent predicates remain. Whole acquisitions, finite acceptance and actual GPT exact-candidate review are still open. No source rule or review approval changed.',
 'featTrainingPrerequisitePass':{
    'fixtures':info(fixture_path),'report':info(report_path),'notes':info(notes_path),'counts':report['counts'],
    'checks':report['checks'],'checkKinds':report['checkKinds'],'failures':0,'scope':report['scope'],'limits':report['limits'],
    'model':info(R/'tools/feat_exact_01_training_prerequisite_model.py'),
    'validator':info(R/'tools/validate_feat_exact_01_training_prerequisites.py'),
    'allTrainingCohortCompleteAcquisitionsValidated':False,'all335ActualAcquisitionBoundaryCasesExecuted':False,
    'candidateReadyForSubmission':False,'noNewRulesAdopted':True,
 },
 'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
 'coverageLedger':info(ledger_path),'coverageDelta':info(delta_path),
 'navigationBindingPolicy':'Resolve explicitly measured correction steps from each frozen expected hash through preserved prior files to the current descendant. The new coverage-only step follows the Warrior coverage delta; it does not waive any source mismatch.',
})
state['safeNextActions']=[
 'Continue FXC-05 with the66 /remaining identities in FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json. The disjoint predicate cohorts are209 numeric/level/None,12 Warrior mutation and48 training. Their differing scope limits remain binding; do not call269 full acquisitions complete.',
 'Use actual class/repertoire sources for spellcasting and cast-access routes, paid prior feat histories for owned-feat predicates, actual lineage receipts without modern-name substitutions, and actual trade/context evidence. The current48 cohort covers first-class training and paid Skill Expert/Naturalist grants only; no complete class-card build, half-feat allocation, initial resource or full use claim.',
 'All184 training cases and three additional training traces pass1917 checks. The model corrects the Thief hand-crossbow catalog spelling. The initial fixture/author/validator that misread foundation.skillAbilities were preserved before correction; no game source or candidate changed. The corrected fixture and report refuse unpreserved overwrite.',
]+state['safeNextActions'][1:]
state.setdefault('preservationManifests',[]).extend([info(manifest),info(A/'feat-training-before-skill-map-correction/PRESERVATION_MANIFEST.json')])
with target.open('x',encoding='utf-8',newline='\n') as stream:json.dump(state,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps({'checkpoint':info(target),'coverage':info(ledger_path),'navigationLinks':navigation['existingDistinctLinks'],
 'missingLinks':0,'trainingPredicateFeats':48,'remainingCredentialDependentFeats':66,'sourceInformationDeleted':False,
 'candidateReadyForSubmission':False,'pushed':False,'cosmologyReviewed':False},indent=2))
