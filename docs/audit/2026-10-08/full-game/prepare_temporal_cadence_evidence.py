"""Preserve the actual missing cadence authority, without editing frozen rules."""
from pathlib import Path
import hashlib
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
out=audit/'CODEX_TEMPORAL_CADENCE_EVIDENCE.md'
assert not out.exists()
rules=root/'docs/mechanics/CLASS_PLAYTEST_RULES.md'
assert hashlib.sha256(rules.read_bytes()).hexdigest()=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81'
parts=['''# Additional exact evidence: Time Loop and conserved casting cadence

This supplies the frozen common rules and the actual quote helper for parent-conference case9. They are unchanged, not newly authored replacements. Dissonance survives encounters and costs/resources remain conserved; Refrain survives idle/weapon turns but a real Druid form entry clears its remembered spell/count. Time Loop itself is not such an entry. The exact original Time Loop procedure is included below.

Please distinguish: restoring anatomy without firing entry; preserving the current already-paid casting economy; and any genuine iteration-qualified idle/grounding event later. Proposed rule for this evidence is to conserve current Dissonance, Refrain count and remembered spell through temporal assignment, then use actual new legal events normally. No past idle turn, vent, shift or rest replays. This would be an explicit temporal cadence bridge, not a claim that all17 class-specific cadence hooks are implemented. If the evidence does not authorize that choice, identify the exact remaining ambiguity.

''']
for name in ('docs/mechanics/CLASS_PLAYTEST_RULES.md','tools/spell_playtest_rules.py'):
    p=root/name
    parts.append(f'\n## Exact {name}\nSHA-256: `{hashlib.sha256(p.read_bytes()).hexdigest()}`\n\n'+p.read_text(encoding='utf-8')+'\n')
bindings=json.loads((root/'data/playtest/form_temphp_bindings.json').read_text(encoding='utf-8'))
def walk(x):
    if isinstance(x,dict):
        if x.get('id')=='oracle.supplement.spiral-touched.spiral-touched-boon-v':return x
        for v in x.values():
            z=walk(v)
            if z:return z
    elif isinstance(x,list):
        for v in x:
            z=walk(v)
            if z:return z
source=walk(bindings);assert source
parts.append('\n## Exact normalized Time Loop procedure\n\n```json\n'+json.dumps(source,ensure_ascii=False,indent=2)+'\n```\n')
out.write_text(''.join(parts),encoding='utf-8')
print(f'{out}: {out.stat().st_size} bytes')
