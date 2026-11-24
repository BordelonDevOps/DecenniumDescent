"""Apply exact independent source corrections, preserving the original proposal."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
source = ROOT / 'engine/artifacts/admitted-command-surface/owned-lot-unit-cross-review-01.json'
data = source.read_bytes()
expected = 'c0c6cd416bffa8267fe3a9ec7d00785e256949c2511e2c5ab932695bd9152fe8'
assert hashlib.sha256(data).hexdigest() == expected
(PACKET / 'OWNED_LOT_UNIT_CROSS_REVIEW_01.json').write_bytes(data)
review = json.loads(data)
assert len(review['exactFieldBindings']) == 5
assert len(review['factoryMatrix']) == 24
result = {
    'schemaVersion': 1,
    'status': 'CORRECTED_SOURCE_BOUND_UNIT_TABLE_REQUIRES_ACTUAL_GPT_CONCURRENCE',
    'scope': review['scope'],
    'actualPredicateDecision': review['actualDecision'],
    'supersedes': 'Exact available-unit applicability of OWNED_LOT_UNIT_DISCLOSURE_PROPOSAL.json only. Original ten-row proposal retained for review provenance.',
    'review': {'path': 'OWNED_LOT_UNIT_CROSS_REVIEW_01.json', 'sha256': expected},
    'scopeResolution': review['scopeResolution'],
    'units': review['exactFieldBindings'],
    'profileBindings': 'OWNED_LOT_UNIT_CROSS_REVIEW_01.json#/factoryMatrix (all24 original declarations); apply actual source flags and every current field/target predicate.',
    'excludedOrOutOfFieldUnits': review['excludedOrOutOfFieldUnits'],
    'rightsAndTemporalRequirements': review['rightsAndTemporalRequirements'],
    'descendantAndTransferProof': review['descendantAndTransferProof'],
    'sourcePins': review['sourcePins'],
    'codexConcurrence': 'The three concrete corrections are adopted as source design. Five exact field branches replace an overbroad ten-unit list; unchanged evidence keeps its historical meaning. Concrete table awaits actual GPT review.',
    'sourceApiAccepted': False, 'runtimeAuthorized': False,
}
(PACKET / 'OWNED_LOT_UNIT_BINDINGS.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(json.dumps({'availableUnitBindings': len(result['units']), 'selectedFactories': 24, 'runtimeAuthorized': False}))
