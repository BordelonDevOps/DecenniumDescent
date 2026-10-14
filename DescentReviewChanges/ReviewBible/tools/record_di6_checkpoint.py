"""Record DI6 authoring, preserved navigation and the continuing GPT request."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
R = G / 'DescentReviewChanges/ReviewBible'
def read(p): return json.loads(p.read_text('utf-8'))
def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}

target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI6.json'
assert not target.exists(), 'One-use checkpoint; preserve existing output.'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6.json'
state = read(previous)
receipt_path = A / 'DIVINATION_RANK6_OPERATING_PROPOSAL_CHECK.json'
receipt = read(receipt_path)
index_path = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'
index = read(index_path)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
data = read(R / 'data/director/spell_proposals/divination_rank6.json')
assert receipt['failures'] == index['failures'] == 0
assert index['counts']['completeUnadoptedProcedures'] == 167
assert index['counts']['mechanicalProceduresStillToPropose'] == 221
assert not navigation['missingLinks'] and navigation['existingDistinctLinks'] == 762
for rel, binding in {**receipt['artifacts'], **index['artifacts']}.items():
    actual = info(G / rel)
    assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
assert info(G / navigation['artifact'])['sha256'] == navigation['sha256']
manifests = []
for folder in ['higher-spell-index-before-di6', 'navigation-before-di6-proposals']:
    p = A / folder / 'PRESERVATION_MANIFEST.json'
    for rel, binding in read(p).items():
        actual = info(G / binding['preservedCopy'])
        assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
    manifests.append(info(p))
observation = A / 'FEAT_V3_LIVE_OBSERVATION_AFTER_DI6.json'
assert read(observation)['requestId'] == 'a64ef367-c9d6-400f-8ba6-4a76dd7f8080'
state.update({
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: AC6 authored11 procedures/22 examples; eight old navigation artifacts preserved, map rebuilt with760 valid links and checkpoint verified.',
    'previousCheckpoint': info(previous),
    'status': 'Five rank-six Divination procedures and10 examples completed locally. Source preservation, rendering and arithmetic checks passed. Planar Binding Minor remains a literal post-push receipt. Actual GPT feat continuation still shows Thinking/Stop and interrupted connection; no terminal final verdict received.',
    'newSpellCohort': {
        'reviewStatus': 'unadopted and not yet shared',
        'sourceIds': [p['spellId'] for p in data['records']],
        'completeProcedures': receipt['completeMechanicalProposals'],
        'authoredExamples': receipt['authoredExamples'],
        'untouchedPostPushReceipts': [p['spellId'] for p in data['completeUntouchedDeferredReceipts']],
        'currentWholeCounterparts': receipt['completeCurrentCounterparts'],
        'reviewedCurrentCounterparts': receipt['reviewedCurrentCounterparts'],
        'pendingCurrentCounterparts': receipt['pendingCurrentCounterparts'],
        'earlierFullUnadoptedCounterparts': receipt['earlierFullUnadoptedCounterpartProposals'],
        'completeClassEnvelopes': receipt['completeComparisonClasses'],
        'newJointIssues': receipt['newJointIssues'],
        'checks': receipt['checks'],
        'plainArithmeticChecks': receipt['plainArithmeticChecks'],
        'boundedReferenceModelChecks': receipt['boundedReferenceModelChecks'],
        'fullSpellRuntimeCases': receipt['fullSpellRuntimeCases'],
        'receipt': info(receipt_path), 'artifacts': receipt['artifacts']
    },
    'higherSpellCounts': index['counts'],
    'higherSpellIndex': info(R / 'data/director/higher_spell_operating_proposal_index.json'),
    'higherSpellIndexCheck': info(index_path), 'indexChecks': index['checks'],
    'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': navigation['missingLinks']},
    'frozenVsCurrent': 'The original707-payload feat ZIP remains the submitted packet. Higher index has167 unadopted procedures:71 previously shared as feat comparisons and96 unshared. DI6 adds5. No dedicated higher-spell verdict. Previous index/navigation bytes are preserved under higher-spell-index-before-di6 and navigation-before-di6-proposals.',
    'preservationManifests': manifests,
    'safeNextActions': [
        'Observe the same actual GPT continuation a64ef367-c9d6-400f-8ba6-4a76dd7f8080. Read-thread returned Too many requests while actual Chrome remained accessible. Do not restart solely from interrupted connection or an observation error.',
        'On an actual terminal feat response, verify all327 dispositions,15 FEX interfaces, exact replacements and evidence before implementing agreed changes.',
        'Continue221 remaining mechanical spell procedures, next TRANSMUTATION_UNIVERSAL_RANK6_SOURCE_PREPARATION.json: elemental-rebind, earthstep, metaburst, displace-structure, flesh-to-stone, move-earth, wind-walk, rift-spiral, arcane-clone, spell-sculptor, contingency, create-homunculus and instant-summons. Read complete source questions, original Core entries and current counterparts first.',
        'All167 higher-spell drafts await dedicated GPT discussion; ordinary spells remain412 reviewed/436 pending. Preserve47 higher post-push receipts plus Blink.',
        'DI6 introduces13 joint issues: full no-save school-harmonized stasis; class-information/suppression boundaries including Oracle protection, dependent forms/assets and capacity excess; actual shortest routes;30-day institutional futures; and a committed-spell warning stream replacing Instantaneous operationally. None is approved by local checks.',
        'Do not rerun one-use DI6/cohort/index/navigation helpers over emitted outputs. Preserve current navigation before later updates.',
        'Final joint whole-game agreement precedes the authorized GitHub push; verify the remote commit before careful cosmology review. No source deletion, catalog promotion or cosmology decision occurred.'
    ]
})
state['activeGptReview']['currentAuthoritativeObservation'] = 'Actual Chrome retains the submitted continuation, Thinking/Stop and Connection interrupted. Visible progress still reports drafting and crafting/lock/Endurance/caltrop findings; no final per-feat verdict or independently verified recovered package is present.'
state['activeGptReview']['liveObservation'] = info(observation)
target.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checkpoint': info(target), 'verifiedCohortAndIndexArtifacts': len(receipt['artifacts']) + len(index['artifacts']), 'preservationManifestsVerified': len(manifests), 'navigationLinks': navigation['existingDistinctLinks'], 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}, indent=2))
