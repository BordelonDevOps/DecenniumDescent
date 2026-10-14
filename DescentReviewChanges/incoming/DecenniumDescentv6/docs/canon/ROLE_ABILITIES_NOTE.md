# Role abilities — continuity note (§9)

**Status:** Owner lock **2026-08-05**  
**Audience:** Continuity agents, class/feat workers, Session / expedition UI

---

## Ruling

There is **no separate role-ability corpus**.

**Roles** (Combat / Reconnaissance / Research / Resource / Support, and any named seat within those teams) are **expedition functions** — assignment labels for how a character spends a time period on an expedition. They are **not** a third character-build track and do **not** grant a dedicated pool of “role abilities.”

Canon expedition structure remains Player Rulebook **Expeditions in Aethel** / [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md).

---

## Ability surface (what actually grants capabilities)

| Layer | Examples |
|-------|----------|
| **Racial** | Racial traits / variants |
| **Class progression** | Base class, archetype, hero path, prestige path features |
| **Feats** | `src/data/feats.js` / feat registry |
| **Spells** | Weave / Resonance catalog (Core Systems owns packaging; class lists identity stays class books) |
| **Items** | Gear, consumables, crafted items |
| **Universal actions** | Shared combat actions and expedition activity checks (skill/tool driven), not role-gated powers |

Monster dossier text that says “change one role ability” (e.g. Umbrin entries) means **swap an expedition-function emphasis or kit tool**, not a PC feat-like role power list.

---

## Do not

- Invent a `role-abilities.js` (or equivalent) as product SoT
- Treat expedition team assignment as granting class-feature-tier powers
- Confuse **party role fantasy** (tank/healer slang) with **expedition team functions**
