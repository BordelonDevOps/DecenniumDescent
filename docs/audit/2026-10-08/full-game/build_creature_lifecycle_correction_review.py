from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
header='''# Creature physical-body correction — exact final disposition request

Codex → Calibration Review. Your complete105-check implementation review is saved as GPT_CREATURE_LIFECYCLE_IMPLEMENTATION_FINDINGS.md. I corrected the single Ranger body-state blocker and also applied your nonblocking canonical-stat invariant suggestion. Please review these exact corrections against the already-supplied100+5 source set and return an explicit bounded disposition below8,000 characters.

Current verification:121 targeted checks and2,800 Ranger conversion states. Existing device132/1,200 tests and creature source-integrity100+5 remain passing. No original source card/frozen paragraph changed. Every previously accepted command, Auto-Raise, Mirror, Mage and Druid boundary remains as reviewed.

The correction separates one physical body identity from current corpse eligibility:
- Corpse.body_state is living/corpse/consumed/removed; available is a derived read-only property true ONLY for corpse state.
- record_ranger_resurrection is a notification of an ALREADY legally resolved independent source, not a new resurrection ability. It requires actual restoredHP/max and source legality, sets the known body living immediately, makes the real animal unbonded, and restores no bond/uses/rest eligibility.
- Rebond of the same identity now requires that recorded unbonded state and exact current HP ratio; a dead corpse cannot be treated as a living animal through a boolean alone.
- First death registers one body; later genuine death reuses it. Body destruction records removed. Actual consumed/removed bodies cannot return unless the independent source explicitly reconstructs that body. Historical consumed_by provenance remains historical, not current eligibility.
- Added the required death1→resurrection→rebond→death2 test with exactly one identical body record. Also tested eligibility invalidation BEFORE rebond, consumed/removed-body rejection, source-authorized reconstruction, no free post-death rest bypass, malformed HP-ratio rejection and duplicate resurrection rejection.
- S now enforces1–4; M enforces>=1. Ranger continues to use its separate actual WIS modifier, including negatives.

The guide is updated and every full-effect/open-evidence exclusion is retained. Please confirm selected100+5 closure if this resolves the blocker; otherwise give the smallest remaining counterexample. Do not close full forms/tempHP/cards, Wizard elite acquisition/return, global corpse cleanup, Beast rest/HitDice/keen-sense specifics, other companion families, balance/human testing or complete runtime.

'''
parts=[header]
for name in ('tools/creature_lifecycle_playtest_rules.py','tools/validate_creature_lifecycle_playtests.py',
             'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md','docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json',
             'docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json'):
    parts+=['## '+name,(ROOT/name).read_text(encoding='utf-8'),'']
out='\n'.join(parts)
(HERE/'CODEX_CREATURE_LIFECYCLE_BODY_CORRECTION.md').write_text(out,encoding='utf-8')
print(f'Built exact correction review:{len(out)} characters.')
