"""Checkpoint completed IN6 authoring and the continuing actual GPT review."""
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

target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_IN6.json'
assert not target.exists(), 'One-use checkpoint; preserve existing output.'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EN6.json'
state = read(previous)
receipt_path = A / 'ILLUSION_NECROMANCY_RANK6_OPERATING_PROPOSAL_CHECK.json'
receipt = read(receipt_path)
index_path = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'
index = read(index_path)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
data = read(R / 'data/director/spell_proposals/illusion_necromancy_rank6.json')
assert receipt['failures'] == index['failures'] == 0
assert index['counts']['completeUnadoptedProcedures'] == 151
assert not navigation['missingLinks'] and navigation['existingDistinctLinks'] == 758
for rel, binding in {**receipt['artifacts'], **index['artifacts']}.items():
    actual = info(G / rel)
    assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
assert info(G / navigation['artifact'])['sha256'] == navigation['sha256']
manifests = []
for folder in ['higher-spell-index-before-in6', 'navigation-before-in6-proposals']:
    p = A / folder / 'PRESERVATION_MANIFEST.json'
    for rel, binding in read(p).items():
        actual = info(G / binding['preservedCopy'])
        assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
    manifests.append(info(p))
observation = A / 'FEAT_V3_LIVE_OBSERVATION_AFTER_IN6.json'
assert read(observation)['requestId'] == 'a64ef367-c9d6-400f-8ba6-4a76dd7f8080'
state.update({
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: EN6 navigation rebuilt with 756 valid links; five artifact bindings and two preservation manifests verified, and the source-preserving checkpoint recorded.',
    'previousCheckpoint': info(previous),
    'status': 'Thirteen rank-six Illusion/Necromancy procedures and26 examples completed locally, including four explicitly new proposed Undead profiles. Source, rendering and arithmetic checks passed. The actual GPT feat continuation remains live with additional visible crafting/locks/Endurance progress, Stop and interrupted-connection status; no final feat verdict received.',
    'newSpellCohort': {
        'reviewStatus': 'unadopted and not yet shared',
        'sourceIds': [p['spellId'] for p in data['records']],
        'completeProcedures': receipt['completeMechanicalProposals'],
        'authoredExamples': receipt['authoredExamples'],
        'untouchedPostPushReceipts': [],
        'currentWholeCounterparts': receipt['completeCurrentCounterparts'],
        'reviewedCurrentCounterparts': receipt['reviewedCurrentCounterparts'],
        'pendingCurrentCounterparts': receipt['pendingCurrentCounterparts'],
        'earlierFullUnadoptedCounterparts': receipt['earlierFullUnadoptedCounterpartProposals'],
        'completeClassEnvelopes': receipt['completeComparisonClasses'],
        'explicitNewCreatureProfiles': receipt['explicitNewCreatureProfiles'],
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
    'frozenVsCurrent': 'Original707-payload feat ZIP unchanged. Higher index contains151 unadopted procedures:71 previously shared as feat comparisons and80 unshared. IN6 adds13. No dedicated higher-spell verdict. Previous index/navigation bytes preserved under higher-spell-index-before-in6 and navigation-before-in6-proposals.',
    'preservationManifests': manifests,
    'safeNextActions': [
        'Observe the same actual GPT continuation a64ef367-c9d6-400f-8ba6-4a76dd7f8080. Additional visible review progress is not a final per-feat verdict or verified recovered package; do not restart merely from the persistent interrupted-connection display.',
        'On an actual terminal feat response, verify all327 dispositions,15 FEX interfaces, exact replacements and complete evidence before implementing agreed changes.',
        'Continue237 remaining higher-spell mechanical procedures, beginning with rank-six Abjuration/Conjuration. Read complete original questions, actual Core records and governing current counterparts before authoring.',
        'All151 higher-spell proposals await dedicated actual GPT discussion. Ordinary spells remain412 reviewed/436 pending. Preserve47 higher post-push receipts plus Blink.',
        'IN6 introduces17 consequential issues, including four new unrated Undead profiles and permanent body/control distinctions. No semantic, runtime, balance or whole-game acceptance follows from preservation/arithmetic checks.',
        'Do not rerun one-use IN6/cohort/index/navigation helpers over emitted outputs; preserve current navigation before later updates.',
        'Actual final joint whole-game agreement precedes the authorized GitHub push; verify the remote commit before careful cosmology review. No source deletion or cosmology decision was made.'
    ]
})
state['activeGptReview']['currentAuthoritativeObservation'] = 'Actual Chrome DOM still shows the submitted request, Thinking/Stop and Connection interrupted. New visible progress reports crafting-rule refinement and lock/Endurance/caltrop reconciliation. These are progress reports, not independently verified draft artifacts or a terminal final verdict.'
state['activeGptReview']['liveObservation'] = info(observation)
target.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checkpoint': info(target), 'verifiedCohortAndIndexArtifacts': len(receipt['artifacts']) + len(index['artifacts']), 'preservationManifestsVerified': len(manifests), 'navigationLinks': navigation['existingDistinctLinks'], 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}, indent=2))
