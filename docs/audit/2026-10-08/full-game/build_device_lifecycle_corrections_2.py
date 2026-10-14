from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
header="""# Device lifecycle: exact correction of the final two blockers

Codex → Calibration Review. The prior116-check version remains saved with your two-blocker findings. The current132-check version fixes both blockers and the copy-provenance issue. Please confirm bounded disposition after reviewing these changes; no new source or ability was added. Reply below8,000 characters.

- configure_drones now enforces exact cardinality at13+: dual is two assets with exactly one module each; single is one asset with exactly two distinct modules. Four regressions cover both empty, one empty, single-one-module, and failure leaving prior valid configuration untouched. Existing valid single-two-distinct and dual-one-each tests still pass.
- Field Repair now uses field_repair_target: positive-HP machine, not expired/superseded/unavailable, deployed device OR deployed/retracted available Drone. It preserves retraction, pays Action1RP, and permits full-HP protected-disable clearance. Six regressions cover touched retracted HP gain, full-HP flag clear, unchanged retraction, unavailable withdrawal, and no broadened Dissonance routing. Repair Pulse's predicate is unchanged.
- Entity.is_copy owns copied-object provenance. Destruction.copied_object snapshots it; incoming_damage_was_copy is a separate event-history field. The generic ambiguous copied argument no longer exists. Hostile eligibility and Recycling inspect copied_object only, plus exact inherited flags. Six regressions show copied hostile damage can destroy a real device and qualify target-side Volatile/Recycling, while a copied device remains excluded.

All132 targeted checks plus1,200 reconfiguration states pass. Earlier three corrections stay intact: half-PB standard-elemental AC; temporary Scrapling kind without machine permissions; noDeathTriggers blocking Reaper while later Action Salvage remains legal. Full helper/tests/guide and report follow for exact verification; the unchanged74+3 source snapshots remain in the preceding conference/implementation packets.

Please state whether these corrected boundaries now meet REVIEWED/reference-VALIDATED for74 supplied lifecycle/command roles plus3 frozen paragraphs, including Magnetic Wall. Wider100-source creature conference is prepared and next; whole-card/runtime/balance remains open.

"""
parts=[header]
for name in ('tools/device_lifecycle_playtest_rules.py','tools/validate_device_lifecycle_playtests.py',
             'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md','docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
(HERE/'CODEX_DEVICE_LIFECYCLE_CORRECTIONS_2.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built132-check corrected-device packet.')
