# Aura save-consumer reconciliation

The [source audit](implementation/SOURCE_AUDIT.json) pins the former candidate inventory and identifies current call sites. Semantic treatment is as follows; runtime qualification remains required in addition to this review.

| Producer | Event-time treatment |
| --- | --- |
| Fear initial and repeat WIS | Qualify before the actual source save; retain the final modifier and outcome in both fear and Aura histories. |
| Sanctuary attacker WIS | Qualify the actual attacker; preserve sanctuary targeting and held-choice semantics. |
| Concentration CON | Complete life/condition settlement first. Existing death/incapacity ending precedes any concentration save. |
| Wound CON | One shared damage wrapper qualifies incoming life and geometry before applying zeroHP/Unconscious/fatal consequences. Ordinary melee, pending melee reconstruction, ranged, Overwatch, periodic rider, crafting, harvesting, mining and both trap damage paths use it. Pending reconstruction reuses the original qualification and draw without another ledger entry. |
| Overwatch Push STR | Preserve the existing base/source modifiers and apply strongest temporary flat arbitration. |
| Suppression Fire DEX | Preserve advantage/disadvantage and automatic-failure behavior; record the actual accepted save. |
| Hunting-trap DEX | Preserve automatic failure and no-draw branches; record qualified contribution separately. |
| Death saves | Original implementation unchanged. Unconscious recipients cannot perceive the owner; no Aura modifier is added. |
| Checks, attacks, initiative, Guidance | No Aura save contribution. |

All connected callers of `PlaytestDamageDice.Resolve` now go through the one Aura wrapper; the underlying source damage helper remains unchanged. Strongest-flat arbitration uses the maximum existing temporary bonus and the qualified Aura bonus, never their sum. Standalone Incapacitated does not imply unconsciousness; blindness/unawareness, actual life, ally identity and exact fractional positions govern qualification. The player-owned Aura view excludes opponents' forensic geometry, life and sensory qualification; full records remain in diagnostic snapshots and strict replay.

Rite healing requires positive original base healing. Radiance resolves before the separately capped Aura point; neither repeats the base Rite or recursively triggers another rider. Invocation uses neither Rite rider. Actual primary gameplay supplies changed-outcome fear, concentration and distinct positive healing witnesses. Supplemental boundaries do not replace those witnesses.
