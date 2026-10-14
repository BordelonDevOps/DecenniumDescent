# AGENTS — V7 playtest workspace

This file satisfies pack README “read first” expectations for the **playtest staging root**.
It is **not** a promotion of product AGENTS guidance onto main.

## Authority

- Gameplay loop procedure for these runs: `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
- Design doctrine: `docs/mechanics/DESIGN_DOCTRINE.md`
- Machine-readable loop twin: `data/public/Decennium_Descent_Gameplay_Loop_v1.json` (= `src/data/gameplay-loop.json`)
- Domain registry pointer: root `CANON_MANIFEST.json` (hardlink to main `docs/canon/CANON_MANIFEST.json`)
- Pack-specific allowlist: that pack’s `SOURCE_MANIFEST.json` only

## Hard rules (from Master Instructions)

1. Identify defects and propose patches; **do not rewrite canon during a test**.
2. Distinguish illegal play, unclear rules, weak options, dominant options, and genuine numerical imbalance.
3. Player agents may use only information visible to their assigned character.
4. Director agents record rulings; do not silently treat rulings as written rules.
5. Every proposed change must cite repeated scenario evidence or be labeled a hypothesis needing another test.

## Staging notice

Gameplay Loop Bible v1 and derived playtest files live under
`DescentReviewChanges/incoming/DecenniumDescentv7/`. They are **pending-review** and are
**not** ReviewBible / main SoT until the owner promotes them.
