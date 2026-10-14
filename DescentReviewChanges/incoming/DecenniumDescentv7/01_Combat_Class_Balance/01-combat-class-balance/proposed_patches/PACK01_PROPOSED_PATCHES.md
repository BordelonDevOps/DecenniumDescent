# Pack 01 — Proposed Patches (NOT applied)

**Status:** proposals only — do not silently rewrite canon  
**Evidence base:** `01-combat-class-balance/results/` + `COMPILED_REPORT.md` (140 seeds across 10 scenarios)  
**Date:** 2026-08-05

## P1 — Clarify summon / deployable / reflection layering (HIGH)

**Observed:** CMB-L10-DARK / CMB-L15-CONTROL / CMB-L20-CEILING showed `summons_illegal_rate` 0.67–1.0 when Wizard Necromancer / Mirrorsage / Tinker desired >2 independent combat actors.

**Rule conflict:**
- Gameplay Loop: max 2 independent combat-capable summons; excess → swarm/unit block.
- Core Systems / class-details: permanent undead counts, Tinker draft 3 deployables, Mirrorsage Charm Bind companions.

**Proposed patch (wording, not numbers first):**
1. In Loop Encounter Mode, define three buckets: **Summons** (independent combat turns, cap 2), **Deployables** (structures/devices; no full independent turns unless stated), **Reflections/Companions** (count as summons unless Charm Bind says otherwise).
2. Necromancer excess undead must use one swarm/unit stat block while the controller already has 2 independent units.
3. Promote relevant `class-ceiling-caps.js` draft lines into Loop glossary on V7 promote.

## P2 — Additional Action stacking (Bard + Action Surge) (HIGH)

**Observed:** CMB-L5-SUPPORT `extra_action_stack_rate=1.0` whenever Bard tempo grants overlapped Soldier Action Surge.

**Proposed patch:**
- Explicit: the single additional full Action slot is shared across all sources (Action Surge, Crescendo tempo, Dual Cast-as-Action, items).
- Bard Crescendo ally grant: either (a) fills that slot, or (b) is redefined as Extra Attack / Bonus Action rider that is *not* a full Action — pick one and mirror in Bard class text.

## P3 — Wizard Dual Cast vs Action economy (MEDIUM)

**Observed:** Rules Observer flagged Dual Cast (class-details L9) every L10+ caster scenario.

**Proposed patch:** State Dual Cast is **one Action** that resolves two Tier 1–2 spells, not a second Action. If it is a second Action, it consumes the additional-Action cap.

## P4 — Encounter budget calibration (MEDIUM)

**Observed:**
- CMB-L1-BASE Standard: win_rate 1.0 (too soft for “meaningful cost”).
- CMB-L3-CARGO Hard+cargo step: win_rate 0.35 (appropriately harsh).
- CMB-L20-CEILING Catastrophic: win_rate 1.0 in ~2.8 rounds (party output outpaces +4 threat / 240×1.4 budget).

**Proposed patch (numerical — requires re-test):**
- Raise Standard equal-level foe HP/damage ~15–25% **or** reduce L1 party nova assumptions.
- Catastrophic / L20: increase boss suite TP or add phase gates; do not nerf all classes blindly.
- Keep cargo Hard budget step (+1 difficulty) — evidence supports it.

## P5 — Control + Tenacity readability (MEDIUM)

**Observed:** CMB-L15-CONTROL avg lookups 3.85; Tenacity triggered (~4/seed) correctly converting denies. Same-source denial without escalation flagged.

**Proposed patch:**
- One-page Director strip: Tenacity, same-source denial limit, Oracle 1 hard-deny/target draft ceiling.
- Cross-link Oracle ceiling caps with Loop general control rule (Oracle is stricter, not looser).

## P6 — Retreat procedure works; pursuer damage presentation (LOW)

**Observed:** CMB-RETREAT success_rate 0.8 with Escape/Pursuit scoring playable. High KO count in model is a sim artifact of continuous pursuer DPR during retreat rounds — table fiction should emphasize Escape checks and cargo sacrifice over full attack routines unless Pursuit success lands.

**Proposed patch:** Director example: on Retreat rounds, default to Pursuit check + one meaningful threat, not full multiattack nova unless fiction demands.

## P7 — Traumatic / Dark Resonance (LOW–MEDIUM)

**Observed:** CMB-L10-DARK Mage trauma path self-damage + Dissonance bypass notes.

**Proposed patch:** Explicit anti-loop clause: traumatic surge cannot refund its own Action or reset the same cooldown in the round it is used; self-damage cannot be prevented by the same feature that caused it.

## Left unchanged (and why)

- Seventeen class identity loops (`class-core-mechanics.js`) — each showed a recurring decision; no class was “always wrong” at L1–L5 baseline.
- Retreat 3-Escape / 3-Pursuit structure — functioned without improvised total-party-kill.
- Tenacity converting stun/deny → Staggered — prevented automatic boss locks when applied.
- Draft ceiling caps for Mirrorsage/Oracle/Tinker/Warrior/Dragoon/Paladin — directionally correct; need promotion, not deletion.
