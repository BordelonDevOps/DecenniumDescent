"""Record completed AC6 authoring without promoting any pending rule."""
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

target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6.json'
assert not target.exists(), 'One-use checkpoint; preserve existing output.'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_IN6.json'
state = read(previous)
receipt_path = A / 'ABJURATION_CONJURATION_RANK6_OPERATING_PROPOSAL_CHECK.json'
receipt = read(receipt_path)
index_path = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'
index = read(index_path)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
data = read(R / 'data/director/spell_proposals/abjuration_conjuration_rank6.json')
assert receipt['failures'] == index['failures'] == 0
assert index['counts']['completeUnadoptedProcedures'] == 162
assert index['counts']['mechanicalProceduresStillToPropose'] == 226
assert not navigation['missingLinks'] and navigation['existingDistinctLinks'] == 760
for rel, binding in {**receipt['artifacts'], **index['artifacts']}.items():
    actual = info(G / rel)
    assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
assert info(G / navigation['artifact'])['sha256'] == navigation['sha256']
manifests = []
for folder in ['higher-spell-index-before-ac6', 'navigation-before-ac6-proposals']:
    p = A / folder / 'PRESERVATION_MANIFEST.json'
    for rel, binding in read(p).items():
        actual = info(G / binding['preservedCopy'])
        assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
    manifests.append(info(p))
observation = A / 'FEAT_V3_LIVE_OBSERVATION_AFTER_AC6.json'
assert read(observation)['requestId'] == 'a64ef367-c9d6-400f-8ba6-4a76dd7f8080'
state.update({
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: IN6 authored with13 procedures/26 examples and four proposed profiles; navigation and preservation checkpoint verified.',
    'previousCheckpoint': info(previous),
    'status': 'Eleven rank-six Abjuration/Conjuration procedures and22 examples completed locally. Source preservation, rendering and arithmetic checks passed. Three post-push identities are unchanged literal receipts. Actual GPT feat continuation still shows Thinking/Stop and interrupted connection; no final verdict received.',
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
    'frozenVsCurrent': 'The submitted707-payload feat ZIP remains the same packet. Higher index has162 unadopted procedures:71 previously shared as feat comparisons and91 unshared. AC6 adds11. No dedicated higher-spell verdict. Previous index/navigation bytes are preserved under higher-spell-index-before-ac6 and navigation-before-ac6-proposals.',
    'preservationManifests': manifests,
    'safeNextActions': [
        'Observe the same GPT continuation a64ef367-c9d6-400f-8ba6-4a76dd7f8080. Read-thread returned Too many requests once during this turn; actual Chrome remained accessible. Do not restart the review merely because the live page displays interrupted connection.',
        'On an actual terminal feat response, verify all327 dispositions,15 FEX interfaces, exact replacements and evidence before implementing agreed changes.',
        'Continue226 remaining mechanical spell procedures, next rank-six Divination. Read complete questions, actual Core sources and current governing counterparts before authoring.',
        'All162 higher-spell drafts await dedicated GPT review. Ordinary spells remain412 reviewed/436 pending. Preserve47 higher post-push receipts plus Blink.',
        'AC6 adds16 joint issues. Resonance Forge uses a proposed5RP/10actual-minute cycle replacing up to60recipe-work minutes; Seal adds an explicitly proposed cross-family restriction affecting earlier unadopted Spell Seal. Army retains distinct bodies but shared command/offense limits. Do not treat these as approved rules.',
        'Do not rerun one-use AC6/cohort/index/navigation helpers over emitted outputs. Preserve current navigation before later updates.',
        'Final joint whole-game agreement precedes the authorized GitHub push; verify remote commit before careful cosmology review. No deletion or cosmology decision occurred.'
    ]
})
state['activeGptReview']['currentAuthoritativeObservation'] = 'Actual Chrome DOM retains the submitted continuation, Thinking/Stop and Connection interrupted. Progress text reports draft recovery and crafting/lock/Endurance/caltrop work; no final per-feat verdict or independently verified recovered package is available.'
state['activeGptReview']['liveObservation'] = info(observation)
target.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checkpoint': info(target), 'verifiedCohortAndIndexArtifacts': len(receipt['artifacts']) + len(index['artifacts']), 'preservationManifestsVerified': len(manifests), 'navigationLinks': navigation['existingDistinctLinks'], 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}, indent=2))
