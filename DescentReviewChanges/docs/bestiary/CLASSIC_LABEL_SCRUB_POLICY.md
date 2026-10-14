# Classic label scrub policy (commercial MM)

**Status:** Policy + sample quarantine (owner lock 2026-08-05 §8)  
**Scope:** Commercial Decennium Descent publication / player-facing app surfaces  
**Do not** mass-rename all ~299 `compatibility-classic-label` inventory hits in this pass.

**Inventory source:** `DescentReviewChanges/docs/bestiary/monster-manual/BESTIARY_INVENTORY_FOR_MM.md` § IP / compatibility risk  
**Prior scrub:** `docs/mechanics/BESTIARY_SCRUB_LOG.md` (54 FR/iconic renames, 2026-07-29)

---

## Rules

| Rule | Action |
|------|--------|
| **Generic OK** | Retain common fantasy terms that are **not** distinctive proprietary creature identities (e.g. wolf, bear, giant constrictor snake, air elemental, generic “dragon” as a type when used generically in prose). |
| **Distinctive → rename** | Rename labels strongly associated with another game’s proprietary creature identity (iconic monster proper names, distinctive demon/devil stems, product-locked lineages). |
| **Aliases internal only** | Former names live only in an internal `compatibilityAliases` field (JSON / director tools). **Never** print aliases in commercial books or player-facing UI. |
| **Quarantine unresolved** | Names not yet reviewed stay **outside** the publication build until renamed or explicitly cleared. |

The internal alias system may support migration, search, and import compatibility without making those names Decennium Descent canon.

---

## Decision guide

```
Is the name a generic fantasy noun/phrase?
  YES → may retain (still write original Aethel ecology)
  NO  → Is it a distinctive legacy identity (iconic stem, product-locked lineage)?
          YES → rename for commercial; keep old string in compatibilityAliases only
          UNSURE → quarantine (exclude from commercial build)
```

### Already scrubbed families (do not reintroduce stock headings)

See `BESTIARY_SCRUB_LOG.md` / `CONTINUITY_C_IP_SCRUB.md`: Umbrin, Gaze Tyrant, Voidmind, Depth Toad, Deep Dwarf, Serpent-Blood, Sporefolk, Astral Reaver/Ascetic, etc.

### Source Pack watchlist (authored titles still carrying iconic stems)

These appear in the **authoritative** Canon Rewrite pack and need rename before commercial ship:

| Current title / slug | Issue | Suggested direction |
|----------------------|-------|---------------------|
| Fracture-Kin **Sibriex** (`fracture-kin-sibriex`) | Iconic stem after family prefix | Rename stem; alias `Sibriex` internal only |
| Fracture-Kin **Nabassu** (`fracture-kin-nabassu`) | Iconic stem | Rename stem; alias `Nabassu` internal only |

---

## Sample quarantine list (from inventory flags)

**Not a full rename pass.** Sample drawn from inventory tags `renamed-but-iconic-stem`, `high-ip-residual`, and distinctive `compatibility-classic-label` examples. Prefer quarantine → rename → clear.

### A. Renamed-but-iconic-stem (prefix remapped; stem still distinctive)

From inventory § Examples — renamed-but-iconic-stem (excerpt):

- Fracture-Kin Armanite  
- Fracture-Kin Babau  
- Fracture-Kin Balor  
- Fracture-Kin Barlgura  
- Fracture-Kin Bulezau  
- Fracture-Kin Chasme  
- Fracture-Kin Dretch  
- Fracture-Kin Glabrezu  
- Fracture-Kin Goristro  
- Fracture-Kin Hezrou  
- Fracture-Kin Manes  
- Fracture-Kin Marilith  
- Fracture-Kin Maurezhi  
- Fracture-Kin Molydeus  
- Fracture-Kin Nabassu  
- Fracture-Kin Nalfeshnee  
- Fracture-Kin Quasit  
- *(remainder of the 24 tagged rows in inventory — same treatment)*

### B. High-IP residual

- Ulitharid  

### C. Distinctive classic labels (sample from first inventory examples — quarantine until rename or “generic OK” clearance)

| Name | Tentative call |
|------|----------------|
| Aboleth | Rename / quarantine |
| Amnizu | Rename / quarantine |
| Androsphinx | Rename / quarantine |
| Ankheg | Rename / quarantine |
| Abyssal Wretch | Review (may be clearable if genericized) |
| Adult * chromatic/metallic Dragon lines | Often **generic OK** as dragon type; still write original ecology — confirm per commercial counsel |
| Air Elemental | **Generic OK** candidate |
| Acolyte / Archer / Assassin / Archmage | Generic NPC roles — **generic OK** candidate |
| Animated Armor | Generic construct phrase — **generic OK** candidate |
| Allosaurus / Ankylosaurus / Ape | Real-world / generic beasts — **generic OK** |

Full `compatibility-classic-label` set = **299** names in inventory — process in later passes; do not block Source Pack authorship of already-cleared Aethel dossiers.

---

## Internal schema note

When implementing aliases in companion JSON / ingest:

```json
{
  "name": "Fracture-Kin <AethelStem>",
  "compatibilityAliases": ["Fracture-Kin Nabassu", "Nabassu"]
}
```

- `compatibilityAliases`: internal / migration / search only  
- Commercial DOCX, Known Descent player text, and player UI: **canonical `name` only**

---

## Related

- Source Pack authority: `Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/README.md`  
- Build filters: `…/BUILD_FILTERS.md`  
- Inventory: `DescentReviewChanges/docs/bestiary/monster-manual/BESTIARY_INVENTORY_FOR_MM.md`  
- Scrub log: `docs/mechanics/BESTIARY_SCRUB_LOG.md`

*Policy stamp: 2026-08-05 — no mass 299 rename this pass.*
