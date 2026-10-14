"""Prepare exact authored guide/helpers/tests and compact binding index for review."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
parts=['''# Exact control-state candidate review

Please adversarially review the attached actual candidate implementation after our219-source conference and clock corrections. All original class/spell objects remain unchanged. DD16/DD18 and all-source semantics remain open. This is a bounded interface package, not full spell/card automation. Report concrete bugs first; if bounded guide/helper checks are sound, explicitly state the exact completed scope, remaining source dependencies and no broad closure.

Current checks:107 targeted control interface cases,9,393 Speed invariant states. Source integrity219records:184cards25engines10ordinaryspells. Separate binding validator checks219source procedures and179component identities, including alternative modes; counts do not prove semantics. Raw previous conferences are preserved as historicalDiscussion in JSON, explicitly non-authoritative when corrected. The operational guide and per-source overrides control.

Please inspect these points particularly:
- The guide corrects your Incapacitated shorthand: Core Incapacitated prohibitsA/BA/R/concentration but not inherently movement/Speed. Hypermutation grants no actions and cannot overcome a separate movement prohibition.
- `effective_control_speed` has per-mode Hypermutation baseline supplied by caller after legitimate snapshot; core_speed_zero and actualzero controls win. Callers still enforce voluntary movement/action restrictions, mode validity and common spent-movement ledger.
- Speed-record refresh preserves exact-profile magnitude/deadline and independent differing candidates. A single Cold hit is caller-deduplicated into one appropriate profile; helper never adds magnitudes. Source cost/application checks are caller-owned.
- Guiding Star helper returns the attack bonus the caller had to include BEFORE rolling; it does not retroactively convert a miss. Would a separate pre-roll query + post-roll consumption interface be clearer/necessary? No actual game engine currently calls it.
- No helper for blanket event dispatch/complete source application exists. Source procedures and caller validation remain authoritative. Some source records contain non-control mechanics intentionally outside this pass.
- Metadata index has explicit elemental/stagger/slowed memberships. Composite soft-fallback components must carry slowed eligibility only while their actual Speed component is active. Please identify missing semantic members (e.g. Oracle/Paladin soft fallback packages) instead of claiming all mappings complete.
- Mage Fusion Fire+Cold's Speed rider has no separately printed endpoint in that phrase; its sibling Cold+Lightning specifies target-next-end. Guide uses target-next-end for Fusion slows as a NEW bounded missing-endpoint bridge; please explicitly accept/correct that decision. Cascade remains source-clock. Does either category require an additional per-source override?
- Ray of Frost/Frost Arrow are audited ordinary cold spells with direct-attack slow; their elemental classification remains unassigned in this index pending explicit semantic decision. We can NEW classify these two cold slow components for Balanced Elements after your confirmation; this does not classify every future cold spell by name/type.
- Carrion Conductor used-corpse history is source-family/corpse scoped, not owner-scoped, so another user cannot re-use the same corpse with Carrion Conductor. Confirm this intended scope from 'corpse cannot be reused'.
- Existing Bleed/fire generic cures on suppressed records are a separate follow-up audit; Sanctify Ground explicitly removes allpresent classifiedStaggered including suppressed. Do not silently use active-hook predicate for cures.

## Exact authored files
''']
for rel in ['docs/mechanics/CONTROL_STATES_PLAYTEST.md','tools/control_playtest_rules.py','tools/validate_control_playtests.py','tools/validate_control_bindings.py']:
 parts.extend([f'\n### {rel}\n\n',f'```{ "python" if rel.endswith(".py") else "markdown"}\n',(ROOT/rel).read_text(encoding='utf-8'),'\n```\n'])
parts.append('\n## Source identity / classification / component bindings / current explicit overrides\n\n```json\n')
parts.append(json.dumps([{k:b[k] for k in ('bindingId','classification','componentIds','operationalOverrides')} for b in data['bindings']],ensure_ascii=False,separators=(',',':')))
parts.append('\n```\n\n## Exact metadata index\n\n```json\n')
parts.append(json.dumps([{'mechanicalId':c['mechanicalId'],'metadata':c['metadata']} for c in data['componentIndex']],ensure_ascii=False,separators=(',',':')))
parts.append('\n```\n')
(HERE/'CODEX_CONTROL_EXACT_REVIEW.md').write_text(''.join(parts),encoding='utf-8')
print(f'Exact review packet: {sum(map(len,parts))} characters')
