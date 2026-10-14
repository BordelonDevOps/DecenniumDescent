# Umbrin — lore canon stub

**Status:** `draft: true` remains in companion data where already present; it does not qualify the locked lore below. The Director locked the **Obsidian Burn** theology, Umbrin geography, and alliance posture as canon (2026-07-30). No mystery, oath, or curse draft flag changes with this lock.  
**Rulebook alignment:** Cosmology extracts already name **Umbra**, **Calan'thir**, and **First Choir**; the **Obsidian Burn** exile story is canon.  
**Product name:** **Umbrin** (one word; plural Umbrin; adjective Umbrin).  
**Glossary:** [`src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md)  
**Mechanics:** [`src/data/races.js`](../../src/data/races.js), [`src/data/reputation.js`](../../src/data/reputation.js)

---

## Who they are

The **Umbrin** are obsidian-skinned elves of **The Murk** — a people shaped by exile rather than surface sunlight. Their name echoes **Umbra**, the primordial abyssal depth, but they are mortals: a culture, not the deity.

They speak **Murkish** alongside Common and Elvish, maintain house politics beneath Aethel, and are feared on the surface the way classic dark-elven archetypes were: competent, cruel when pressed, and always negotiating from shadow.

---

## Geography

- **The Murk:** the broad subterranean region and Umbrin approach beneath Aethel.
- **Blackglass Reach:** the surface and near-Murk marches, where dark-glass outcrops, trade routes, watchposts, and wary border settlements meet.
- **Veyr-Obsid:** the primary Umbrin city, a severe dark-glass metropolis of rival houses, trade compacts, and concealed leverage.
- **the Quiet Deep:** the deeper underworld beyond settled Murk routes, where distance, silence, and old dangers outlast reliable maps.

---

## Origin — Obsidian Burn

Umbrin forebears drew too close to **Umbra's** thread through curiosity, shadow-weaving, and refusal of Calan'thir's calibration.

**Calan'thir**, architect of the Spiral, and the **First Choir** judged them unfit for the light of ordered song. They were **banished** from Choir lands and driven deep into The Murk. The exile is remembered as the **Obsidian Burn**: flesh that had known Lumina's glare cooled to an obsidian sheen — black, purple, or blue-gray skin with a glassy luster. Umbrin do not treat this as shame alone; many wear it as proof that Umbra's depth survived Choir judgment.

---

## Faith — Choir orthodoxy vs Murk Umbra cults

**Choir orthodoxy** (Celestial rites, Calan'thir's Voice, mainstream temples) holds that shadow serves the song when **bounded** — see Oracle patron **Hush Beneath the Song**, tier-10 silence, and Resonance prose.

Murk **Umbra cults** invert that: they venerate a **perverse idea of Umbra** — abyss as liberation, Obsidian Thread as license, not balance. Priesthoods in the Murk (bestiary: Spider-Priestess, Matron lines) embody this heresy. They are Aethel-original; no further high-god names are established here.

**Cleansing Orders** and **Anti-Cult Alliances** hunt cult bleed on the surface; **Dark Cults** sometimes trade whispers with Murk cells when spiral or fiend interests align.

---

## Reputation — distrusted, transactional, and never presumed redeemed

Umbrin PCs should expect **Disliked/Hated** default bias from:

- **Aethel Authorities**, **Mainstream Religious Orders**, **Good-Aligned Temples**
- **Common Folk** (fearful memory of Murk raids and cult stories)

They are **not** universally blocked from every faction, but no alliance should be read as redemption by default. Murk politics and surface expediency create temporary, transactional arrangements: each side expects leverage, a price, or a shared enemy.

| Faction | Typical Umbrin angle |
|---------|----------------------|
| **Underworld** | Smuggling, assassination contracts, syndicate pacts |
| **Planar Trading Guilds** | Murk routes and contraband Weave components |
| **Corruption Scholars** | Shared appetite for forbidden resonance research |
| **Independent Mages** | Hedge-pact tutors who don't ask about Murkish rites |
| **Anti-Cult Alliances** | Temporary truce when a mutual spiral cult is the target; neither side mistakes it for trust |
| **Merchant Guilds / Explorers Societies** | Delve guides who know Yieldheart cavern back-ways |

**Playtest rule:** No hard race-based reputation lock in `reputation.js` — apply bias through background, NPC roleplay, and manual faction edits. Document notable standings on the character sheet.

---

## Canon name examples

Umbrin personal names favor two or three clipped syllables, hard consonants, and occasional hyphenation; apostrophes are uncommon. Use these as a tonal guide rather than a caste or gender rule.

- **Personal names:** Vaerith, Sythra, Korven, Zelka, Dravik, Nyssara, Kethren, Vorskai.
- **House names:** House Veyr, Ashketh, Rhal-Voss, Obis-Keth.
- **Optional epithets:** of the Blackglass, Quiet-Step, Ash-Veiled, Deepbound.

The names belong to the Murk's dark-glass underworld: they should evoke obsidian, old ash, trade compacts, veils, and depth without borrowing foreign dark-elf or established fantasy-game proper names.

---

## Product boundaries

| Use | Avoid |
|-----|-------|
| Umbrin, The Murk, Murkish, Umbra (primordial), Calan'thir, First Choir | Drow, dark elf, Lolth, Underdark, Undercommon |
| Obsidian Burn (canon theology), Umbra cult (Murk) | FR spider goddess, Eberron, SWTOR |
| Umbrin Magic / Umbrin Weapon Training (traits) | Umbral Elf (legacy; migrates on load) |

**Legacy saves:** `character-storage.js` maps `Drow`, `Umbral Elf`, and related subrace strings → Umbrin on load.

**Author tickets:** Re-ingest the rulebook race chapter as needed; align bestiary "Umbrin *" stat blocks with locked theology. Canon names, Master Tracker, Resonance multiclass, Mystery of Shadow, and Oath of Grief are resolved; do not promote unrelated draft profiles from this lore lock.
