"""Preserve actual incremental code for notebook review, with explicit limits."""
from pathlib import Path
import hashlib
import json

AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    out=AUDIT/'CODEX_TEMPORAL_PULSE_BRIDGE_REVIEW.md'
    assert not out.exists()
    files=['tools/temporal_control_playtest_rules.py','tools/validate_temporal_control_playtests.py',
           'docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md','docs/mechanics/TEMPORAL_CONTROL_VALIDATION.json']
    prompt='''# Actual incremental pulse payment/output code — 22 tests

Your nine-part policy conference is preserved in GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md. I accept the Sacred Chant Conviction addition, source-qualified rider distinctions, and one-evaluation-only native regular starts. No new original source text is needed. No full integration or full-game closure is claimed.

Here is the first concrete portion: the canonical pulse payment facade and the resolved independent-output guard using actual existing PulseSeries.resolve calls. All22 methods pass. Foundation helper SHA b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151 remains unchanged. This incremental helper does not yet admit active control/pulse state into TemporalKernel. All seven integrations remain counted as missing.

Please review this code for defects inside its stated payment/resolved-output scope. Source-clock restoration, authentic start receipts, missed-output treatment, parent concentration, and final Ki/Conviction resource application are explicitly still missing; do not treat these22 checks as proof of those adapters. The host must apply a returned allowance once within the same atomic event to its actual capped resource holder. This helper contains no Ki/Conviction pool. The next full adapter must join that mutation to its source transaction.

Two source wording clarifications before clock code:

1. Your maintenance paragraph said failed payment has no retry, but the existing reviewed guide explicitly preserves an early failed ordinary maintenance opportunity until that turn's end; only exact-due paid sequences/windows end immediately. Since your conference expressly does not reopen ordinary behavior, I retain that distinction. Please confirm.
2. The actual immutable snapshot is initiative-start, before its first turn/event. A source created after that boundary cannot be restored as snapshot state. Existing pre-initiative pulse series normally have outside-origin preserved virtual markers. Your in-encounter logical-opportunity rule can apply only when the actual source was already present at the immutable boundary; no later source may relabel itself to gain snapshot membership. Please confirm this constraint and identify any authentic at-boundary origin case that needs separate support. I will not fabricate a turn or entry/cast at capture.

One initial test incorrectly expected a prepaid later pulse to fail merely because the first was missed; the existing helper correctly permits the later due opportunity. I corrected the test to exercise an actually early request, without changing ordinary source behavior. The initial result is preserved as TEMPORAL_CONTROL_FIRST_TEST_RESULT.json.

The current guide records both the settled policy and outstanding implementation. Please give a bounded code disposition or concrete counterexample. Full Time Loop, remaining game authorship, final joint flow confirmation and GitHub delivery are still open.
'''
    parts=[prompt];hashes={}
    for name in files:
        raw=(ROOT/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
        parts.append('\n## '+name+'\n\n```\n'+raw.decode('utf-8')+'\n```\n')
    out.write_bytes('\n'.join(parts).encode('utf-8'))
    manifest={'status':'SUBMISSION PREPARED; independent review required','hashes':hashes,
              'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size}
    (AUDIT/'TEMPORAL_PULSE_BRIDGE_REVIEW_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest))

if __name__=='__main__':main()
