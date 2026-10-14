# Player 1 — Novice

**Playtest persona:** First or second TTRPG ever. Picks what *sounds* cool, not what synergizes. Confused by jargon; asks the DM to explain things mid-session. Likely to describe actions in story terms (“I sing something spooky”) instead of naming mechanics.

**Expedition:** [`EXPEDITION_SCENARIO.md`](../EXPEDITION_SCENARIO.md) — Glassbite Hollow (EXP-BGR-01). Level **3** party, **Blackglass Reach** fringe, **3 non-boss fights** before extraction.

---

## Character concept

**Name:** Vesper Ashwhisper  
**Pronouns:** she/her  
**One-liner:** A brooding Umbrin street performer who thinks the dungeon will respect artistic talent.

**Why this build (in-character reasoning):**
- Saw **Umbrin** in the race list — “obsidian-skinned children of exile” read like tragic fantasy anime. Instant yes.
- Chose **Cavern Mystic** because “mystic” felt more magical than “Shadow Blade.” Did not read that all three variants share the same mechanics or that **Sunlight Sensitivity** matters on a *surface* march near Blackglass Reach.
- Chose **Bard** because “I don’t want to stab people; I want to play music and help friends.” Ignored that the expedition brief mentioned mercenary rows and gladiatorial pressure.
- Plans to lean into **Discord** energy eventually (“twisted songweaver”) but is only level 3 — took **Virtuoso** at Bard College because the app listed it and “virtuoso” sounded prestigious.

---

## Persona & playstyle

| Aspect | How P1 plays |
|--------|----------------|
| **Decision speed** | Slow. Re-reads the character sheet every turn. |
| **Combat** | Stands near the back, tries to “perform” before attacking, forgets bonus-action economy. |
| **Social** | Over-talks to NPCs; assumes Umbrin reputation is “mysterious and cool,” not “hated by surface folk.” |
| **Rules literacy** | Knows HP and “roll a d20.” Everything else is “ask the DM.” |
| **Loot** | Wants a dramatic cloak and a better lute. Ignores armor upgrades. |
| **Failure mode** | Uses **Bardic Inspiration** on herself “for confidence,” then wonders why allies didn’t get the die. |

---

## Sheet sketch — Level 3

### Race & variant
- **Race:** Umbrin (`races.js`)
- **Variant / subrace:** Cavern Mystic (`racial-variants.json`)
- **Racial traits (key):**
  - Superior Darkvision
  - **Sunlight Sensitivity** *(did not factor into expedition planning)*
  - Umbrin Magic
  - Umbrin Weapon Training
  - **Webstep** — walk on walls/ceilings 1 turn (1/rest) *(Cavern Mystic variant ability)*
  - **Nightfang Training** — +10% damage & +2 stealth in total darkness *(racial feat)*

### Class
- **Class:** Bard (1 of 17 canon classes)
- **Hit die:** d8 (`class-hit-dice.js`)
- **Armor prof:** Light
- **Weapons prof:** Simple, hand crossbows, longswords, rapiers, shortswords

### Ability scores (point-buy, flavor-first)
Novice prioritized Charisma and “seems elvish” Dexterity; dumped Constitution.

| Ability | Score | Mod | Notes |
|---------|-------|-----|-------|
| STR | 8 | −1 | “I’m not a fighter.” |
| DEX | 14 | +2 | +2 racial → **16 (+3)** |
| CON | 10 | +0 | “How bad can it be?” |
| INT | 10 | +0 | |
| WIS | 10 | +0 | |
| CHA | 15 | +2 | +1 racial → **16 (+3)** |

### Combat numbers (estimates)
| Stat | Value | How derived |
|------|-------|-------------|
| **HP** | **18** | d8 max L1 + avg×2 at L2–3, CON +0 (`estimateMaxHpFromHitDie(3, 0, "Bard")`) |
| **AC** | **14** | Leather armor 11 + DEX 3 *(has not bought studded leather)* |
| **Speed** | 30 ft | |
| **Initiative** | +3 | DEX |

### Class features at level 3
From `class-details.js`:

**Level 1:** Spellcasting · Bardic Inspiration · Crescendo (d6)  
**Level 2:** Jack of All Trades · Song of Rest  
**Level 3:** Bard College (**Virtuoso**) · Expertise  

**Combat tags:** Crescendo die (d6) · Bardic Inspiration · Song as bonus action focus

**Expertise (novice pick):** Performance, Persuasion *(“so I can talk us out of fights”)*

### Gear (minimal)
- Rapier *(looks elegant; novice thinks finesse = safe)*
- Leather armor
- Lute (primary “weapon” in her head)
- Explorer’s pack, dagger, 15 gp

### Spells known (conceptual — novice didn’t optimize)
Likely picked **flashy** over **useful for fringe combats**:
- **Cantrips:** *Vicious Mockery*, *Prestidigitation* (make ash swirl for drama)
- **L1:** *Dissonant Whispers*, *Healing Word*, *Silvery Barbs* or *Sleep* if available in list
- **L2:** *Suggestion* (“talk our way out”), *Invisibility* (hide from scary things)

*Player note:* Not sure which spells are on the Bard list in this ruleset — would pick whatever has the spookiest description.

---

## What I’d do in a fight (naive)

1. **Turn 1:** “Can I roll Performance to intimidate them with a song?” *(Doesn’t understand action vs. bonus action yet.)*
2. If allowed, spends action on **Performance**; bonus action tries to “start a song” without naming **Crescendo** or a specific feature.
3. Gives **Bardic Inspiration** to **herself** before remembering allies exist.
4. If hurt: casts **Healing Word** on herself at 0 HP instead of stabilizing a downed ally *(panics)*.
5. If cornered: stabs with rapier once, then tries **Webstep** to cling to the ceiling “like in the movies,” forgetting she still has Sunlight Sensitivity in torchlight.
6. After combat: **Song of Rest** during short rest — asks if that heals HP or “just vibes.”

---

## Roleplay choices (suboptimal on purpose)

### Session zero / briefing
- Misreads **Blackglass Reach** as “fancy elf city” instead of oath-law mercenary fringe.
- Introduces herself as an “Umbrin mystic bard” loudly in a tavern; surprised if NPCs flinch.
- Asks if the party can detour to **Veyr-Obsid** because she saw it on a lore tab.

### During exploration
- Insists on scouting ahead alone “because darkvision” — ignores that the fringe may be **lit**.
- Tries to befriend a hostile creature with **Suggestion** before initiative is rolled.
- Collects “black glass” shards for costume jewelry instead of checking for hazards.

### During the three fights
- **Fight 1:** Burns **Bardic Inspiration** pre-combat for “good luck,” then has none when the Soldier ally fails a save.
- **Fight 2:** Uses **Webstep** for style points, not positioning; ends up separated from the party.
- **Fight 3:** Attempts to **Persuade** gladiatorial oath-bound foes to “settle this with a poetry slam.”

### Aftermath
- Blames Sunlight Sensitivity for a miss even if the fight was underground.
- Writes in her journal that she needs the **Discord** hero path at level 10 — doesn’t understand she’s on **Virtuoso** until the DM corrects her.

---

## Questions I’d ask the DM

### Before we start
1. “What’s **AC** again — is that how hard I am to hit?”
2. “What’s a **short rest**? Is that like… a bathroom break?”
3. “The sheet says **Crescendo** — is that the same as Bardic Inspiration?”
4. “We’re going to **Blackglass Reach** — is that outside? My Umbrin has **Sunlight Sensitivity** and I just noticed.”
5. “Can I use **Murkish** so the bad guys think I’m local Umbrin nobility?” *(She is not.)*

### During combat
6. “Is **Performance** an action? Can it replace attacking?”
7. “Can I give **Bardic Inspiration** to more than one person if I sing louder?”
8. “What’s **advantage** mean — do I roll twice and pick the high one?”
9. “If I’m on the ceiling with **Webstep**, do melee enemies still hit me?”
10. “When someone drops to zero HP, do they die immediately or is there a **death save** thing?”

### Rules / class jargon
11. “What’s **Expertise** — double my bonus?”
12. “**Jack of All Trades** — does that mean I’m good at everything now?”
13. “What’s the difference between **Virtuoso** and **Discord**? I want Discord but I’m only level 3.”
14. “**Revelation Charges** came up on someone else’s Oracle sheet — why don’t I have those? Is Bard magic different?”
15. “What’s a **tier** in Decennium Descent? The dungeon menu said tier 7 — are we underleveled?”

### Setting / lore
16. “Are Umbrin actually evil? The race blurb said ‘perverse Umbra’ and I’m worried the Paladin will smite me.”
17. “Who is **Calan'thir** and should I hate him in character?”
18. “Is **The Murk** where I’m from? I picked Cavern Mystic so I assume yes.”
19. “Can we sell loot at **Mercenary Row** or do we need licenses?”
20. “If this is a playtest, does my character die for real?”

---

## Playtest value (OOC note for facilitators)

This sheet is intentionally **weak for combat clarity** and **weak for Blackglass Reach lighting**, but **strong for testing**:
- Whether new players can parse Bard **Crescendo / Inspiration / Song** economy from the companion UI
- Whether **Sunlight Sensitivity** is surfaced clearly during surface-fringe scenarios
- Whether **Umbrin** social friction appears without hard-setting enforcement
- How much jargon (tier, revelation, short rest, expertise) needs DM scaffolding at L3

**No commit** — local playtest artifact only.
