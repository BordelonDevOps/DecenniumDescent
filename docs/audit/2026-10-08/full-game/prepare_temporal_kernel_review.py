"""Build an immutable, game-only bounded implementation review packet."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[3] / 'DescentReviewChanges/ReviewBible'
TARGET = AUDIT / 'CODEX_TEMPORAL_KERNEL_REVIEW.md'
FILES = [
    'tools/temporal_playtest_rules.py', 'tools/validate_temporal_playtests.py',
    'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md', 'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json',
]

def main():
    assert not TARGET.exists(), 'Preserve the exact submitted packet; use a revision filename'
    rows = []
    intro = '''# Time Loop foundational kernel: actual implementation review

I implemented the first bounded transaction kernel from your twelve boundary decisions. Please review the ACTUAL attached code, guide and 46 passing adversarial test methods. This is intentionally an intermediate review: seven major integrations are not yet implemented. No source/card is promoted, playable_plan always rejects, and this is NOT a request to close Time Loop or the whole game.

Please identify concrete correctness defects in the admitted fixture scope, with reproducible counterexamples and required repairs. Also check that the scope claims accurately reflect what exists. In particular:

1. Atomicity: costs, canonical aliases, stale plans, unknown/dynamically added fields and partial failures.
2. Reaction debt and logical iteration identity, with all actual elapsed clocks and finite expenditures conserved.
3. Same-ID one-shot healing consumption: historical events versus active iteration, including future integration with actual FeatWorld. Its creation/refresh/removal synchronization is expressly unimplemented.
4. HP/max-HP/Stable/Soul Bind identity and absolute deadlines; no generated healing/death/reward events.
5. Physical derivation and original/transferable inventory: surviving harvested parts, mixed roots and source slots. Are there ways the currently admitted fixtures duplicate or wrongly erase matter?
6. Atomic finite ground geometry and outsiders: enclosure/support without direct overlap. This adapter intentionally does not cover elevation, flight, portals or growth.
7. External dependencies and memory: current external sources remain; unhandled effects block. External concentration is only a checked projection until the actual callback adapter is added.
8. Any unjustified claim of implemented completeness, unchecked opt-in, or a missing validation allowing an admitted fixture to silently violate the twelve decisions.

After repairs I will add the real transformation/Druid, creature/device/remaining-life, feat and control/pulse integrations. Please distinguish a defect in this bounded kernel from one of those explicitly outstanding integrations. The owner still requires a final whole-game flow conference before the authorized GitHub push; this packet does not satisfy that gate.
'''
    parts = [intro]
    for relative in FILES:
        path = ROOT / relative
        raw = path.read_bytes()
        rows.append({'path': relative, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        parts.append('\n## ' + relative + '\n\n```\n' + raw.decode('utf-8') + '\n```\n')
    TARGET.write_text('\n'.join(parts), encoding='utf-8')
    (AUDIT/'TEMPORAL_KERNEL_REVIEW_MANIFEST.json').write_text(json.dumps({
        'status': 'PREPARED; actual browser send and completed reply tracked separately',
        'scope': 'Unpromoted foundational kernel, not all seventeen temporal integrations',
        'files': rows, 'packetBytes': TARGET.stat().st_size,
    }, indent=2)+'\n', encoding='utf-8')
    print(str(TARGET), TARGET.stat().st_size)

if __name__ == '__main__':
    main()
