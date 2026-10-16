# Epilogue Character Module — Director Implementation

**Status:** NEW provisional authorship. This chapter operationalizes original epilogue directions EPI-01 through EPI-07 without changing source files, class progression, current resources/conditions/rests, KT/PT/Hunt/death rules, spell approval status, or campaign epoch.

## Authority and source boundary

The preserved source paragraphs are:
- EPI-01: `The Cosmology of Decennium Descent.docx`, `word/document.xml`, all-`w:p` indices 270–276.
- EPI-02: indices 279–280.
- EPI-03: indices 282–283.
- EPI-04: indices 284–288.
- EPI-05: indices 290–293.
- EPI-06: indices 295–298.
- EPI-07: index 299.

The exact paragraph hashes are in `REGISTER.json` and `EPILOGUE_CHARACTER_MODEL.json`. Source language is preserved. Every number, scene, cooldown, finite menu, endpoint, material choice, or denial rule not explicitly present in those paragraphs is **NEW provisional authorship**.

The campaign's position relative to the Proof War remains an owner choice. This module is written so its character procedures can be compared independently; it does not make the epilogue's historical placement current canon.

## EPI-01 — Home Affiliation

### Eligible choices
Use exactly four primary-realm philosophical affiliations in the current candidate:
1. Bastion of Flame — disciplined passion/temperance.
2. Veiled Expanse — secrecy yielding to honest engagement.
3. Radiant Currents — fluid law and perspective.
4. Boundless Void — questions puncturing complacency.

This deliberately does **not** treat every artwork label on the Spiral Map as an equivalent player home-plane choice. The Citadel, Nine Hells and Abyss source artwork remain source material, not eligible home affiliations in this module.

A token is symbolic. Never grant ancestry, resistance, travel, language, access, or automatic planar knowledge from token placement.

### Conduct adjudication
At the end of a beneficial Long Rest:
1. Confirm the current established plane/location.
2. If the location equals the chosen realm, stop; no EPI-01 reward/penalty.
3. If location is truly unknown, stop; do not guess.
4. Examine the previous 24 elapsed hours.
5. Identify a concrete choice that materially relates to the principle.
6. If the choice was foreseeably capable of creating Disquiet, the player should have received fair advance notice.
7. Resolve aligned / knowingly contrary / neutral.

Do not audit every sentence or personality beat. One material choice is enough. Neutral/no relevant conduct is a valid result.

The bounded resource is `resource.epilogue-inspiration`: d6, cap 2. The bounded penalty is `state.epilogue-disquiet`: one subtract-d6 pending ability-check record, expiring in 24h. Neither becomes another class engine or corruption track.

## EPI-02 — Choir Motifs

### Historical accounting boundary
The original says nine verses, “one for each virtue plus the binding Variable Omega,” but the supplied mechanical table contains seven named motif benefits. Preserve that discrepancy. Do not invent an eighth virtue, a missing verse benefit, or a Variable Omega mechanic.

### Finite availability
A Motif Score is an authored object containing melodic contour, not lyrics or Equation text. The Director decides where a finite score/teacher is actually available. Learning takes 1 uninterrupted hour. Activation takes 1 uninterrupted audible minute.

The Expedition has one shared `motifResonance` activation after a beneficial Long Rest, with a hard no-more-than-once-per-24h refresh. This prevents seven different scores, duplicate copies, multiple performers, recordings, or party swapping from multiplying daily recovery.

### Motif-specific adjudication

**Courage:** bind “hero point or equivalent” only to Epilogue Inspiration. Do not choose a character's most valuable class resource.

**Balance:** eligible current prepared systems in this candidate are Druid prepared spells, Wizard prepared ordinary matrices, and Warrior equipped mutation slots. This is a finite list. A permanent card selection, exhausted use counter, resource pool, serum reserve, spellbook ownership, rank prerequisite, form unlock, or Hero/Arch acquisition is not a prepared ability and is not reset.

**Law:** Wisdom save vs `8 + PB + CHA`. On failure, one-round hostile-targeting restriction only. It does not charm, stun, compel speech, compel truth, compel agreement, or compel surrender. A protected listener's direct damage breaks it before damage resolves. Existing source-target hard-denial applies.

**Sorrow:** legal only when the exact failed Wisdom save can still be replaced before an irreversible consequence commits. It cannot rewind death, consumed one-time offers, already-resolved damage, or a previously replaced save.

**Pattern:** pending advantage on one study/research/decipher/analysis/recall ability check, 24h.

**Contradiction:** pending advantage on one Insight check declared for hidden motive/internal inconsistency, 24h. Never truth detection.

**Transition:** NEW narrowed interpretation. Reduce remaining **active work** 25%, not source's unrestricted “halve time.” Use only the enumerated eligible projects. This is necessary to preserve current one-world clocks and avoid halving Long Rests, seasonal windows, travel, borrowed-proficiency duration, observation or Opening/Horn schedules.

## EPI-03 — Vow records

A vow record should contain:
- `vowId`
- one-sentence text
- `state`
- creation/revision timestamps
- confession witness identity and language mode when a mask exists
- bound mask IDs

Never ask a player to disclose real-life emotional truths. “Confession” and “secret” are entirely character-fiction concepts.

A personal vow is separate from Paladin Sacred Oath. Do not trigger Oathbreaker solely because a player changes this vow.

When a vow is fulfilled/retired, a bound mask becomes dormant. One-hour rebind to a new vow preserves quality, key, wearer and charge ledger.

## EPI-04 — Mask implementation

### Separate ritual, not recipe
Do not modify the reviewed trade recipe count. A mask project uses its own module record.

### Material provisioning
At adoption, one initial blank per PC is available so the subsystem cannot deadlock on an undefined ingredient. Replacement abstraction is 25 gp + 1h in a suitable settled workshop/market.

Source-preserved materials:
- Ranger: still water frozen beneath moonlight.
- Wizard: liquid silver condensed from Arcane Crucible fumes.
- Thief: polished black glass.

The other 14 materials in the player table are NEW. They are fictional game materials/procurement abstractions; do not convert them into real-world chemistry.

### Project and check
- One committed blank.
- 8 active hours.
- Pause only after completed 1h blocks.
- 7-day project expiry.
- No assistant bonus/time.
- 0–3 secret count fixed at start, with the one pre-final-hour disclosure exception.
- DC `10 + secretCount`.
- Bare class-key ability check.
- Apply current fixed-DC four-degree rule and natural shift.
- Collapse CS/S => Living; F/CF => Cracked.
- No critical-quality rider.

All 17 rows are in the model. Mixed-key seams are intentionally fixed for this module:
- Crimson Agent: INT (hemomancy side).
- Ranger: WIS (primal side).
- Soldier: CON (defensive/control side).
- Thief: DEX (primary class execution).
- Warrior: permanent project choice STR or DEX.

Multiclass: select one actual class at project start and freeze the row.

### Identity and anti-reset
A mask is keyed to `wearerId + vowId + maskClass`. One operative mask per wearer. Reveal charge belongs to that identity, not to a physical copy. Lending, replacement, theft, re-donning, or switching physical masks cannot reset the charge.

No generic attunement slot.

### Wearing/reveal
Common save advantage applies only to actual fear effects and actual Null lullabies. Do not infer immunity to charm, psychic damage, Corruption, PT, KT, Dissonance, truth effects, or generic Null material.

Cracked penalty applies only when:
1. check is social;
2. deception is materially involved;
3. the deception would impede the active vow.

Reveal:
- Action.
- 20ft.
- one perceivable target with line of effect.
- CHA save vs `8 + PB + current fixed-key modifier`.
- charge spent after legal target declaration.
- failure = current **Stunned** until end target's next regular turn.
- outside initiative = 6s.
- immunity/hard denial applies normally.

Do not invent repeat-save immunity beyond the one-use rest cadence. If a target succeeds, it simply resists that reveal.

### Removal
Truthful safe removal is source-flavored convenience, not a hidden curse gate.
- own turn Free Action + spoken current emotional truth;
- off turn Reaction + spoken truth;
- sign/write alternative Action when understood;
- ordinary Action removal without truth is legal and carries no invented curse;
- forced removal simply suppresses.

## EPI-05 — Virtues and Conflict Die

### Source pairings
| Courage | Bard, Warrior, Paladin |
| Balance | Druid, Ranger, Dragoon |
| Law | Cleric, Soldier, Mage |
| Sorrow | Oracle, Shaman |
| Pattern | Wizard, Tinker, Mirrorsage |
| Contradiction | Thief, Crimson Agent |
| Transition | Monk, Mirrorsage, Paladin |

Paladin and Mirrorsage each appear in two source rows. Preserve both.

### Opposition procedure
Opposition is not “any virtue missing from your class row.” Require a session declaration naming:
- one present class;
- one actual mechanical class strength;
- one selected virtue;
- one plausible fictional tension.

Player and Director agree eligibility. This is not an alignment test.

### Conflict Die
- d12
- once per sessionId
- declare before the d20
- ability checks only
- no attack/save use
- no Epilogue Inspiration on same check
- fixed-DC total includes d12, then natural d20 degree shift
- use consumed on failure
- success then +1 **core Exhaustion**

The source says “risk of exhaustion” and then “one level of fatigue.” This candidate intentionally binds the consequence to core Exhaustion instead of inventing another fatigue track. Do not also add Expedition or Warrior Strain.

A character immune to Exhaustion cannot declare the priced benefit. At Exhaustion 5, a successful Conflict check resolves first, then the sixth Exhaustion level resolves under the current lethal rule.

## EPI-06 — Archon Petitions

### Eligibility and Witness
Eligible:
- Cleric;
- Monk;
- another character with a preexisting `spiritualMentor` record.

The mentor need not be physically present. The local Witness **must** be available and Director-designated as a sage trained to record petitions. The Witness is not an Archon and does not prove divine appearance.

Consultation: 10m.
Meditation: 60m uninterrupted.
Symbolic act: 10m from the virtue table.
Then d12.

Once rolled, 7 elapsed day cooldown. Do not permit reroll fishing because the player dislikes a response.

### Symbolic acts
Use the exact finite acts in `EPILOGUE_CHARACTER_MODEL.json`; they intentionally test a theme without requiring a preselected moral answer.

### 1–4 Guidance
24h. One Guidance at a time. Use the exact listed virtue/check pairs. Advantage does not stack with itself.

### 5–8 Blessing
Use exactly the seven verified Base passive candidates:

| Virtue | Feature |
|---|---|
| Courage | `warrior.base.combat-instinct` — Combat Instinct |
| Balance | `ranger.base.natural-explorer` — Natural Explorer |
| Law | `soldier.base.tactical-awareness` — Tactical Awareness |
| Sorrow | `shaman.base.alchemical-knowledge` — Alchemical Knowledge |
| Pattern | `wizard.base.scholarly-mind` — Scholarly Mind |
| Contradiction | `thief.base.trap-intuition` — Trap Intuition |
| Transition | `monk.base.unarmored-speed` — Unarmored Speed |

Each referenced `path + jsonPointer + id` was verified against the supplied current class-card file. Transfer only the card's effect plus the explicit adaptation. No level, class, engine, RP, proficiency, spellbook, gear, or advancement qualification transfers.

If exact feature is already possessed, no extra mechanical effect and no reroll.

### 9–11 Test
Use the seven finite scenes:

| Virtue | Scene | Limit |
|---|---|---|
| Courage | The Shaking Span | 3 rounds / 18 seconds after setup. |
| Balance | The Twin Cistern | Up to 20 minutes. |
| Law | The Broken Queue | 15 minutes. |
| Sorrow | The Missing Name | 10 minutes. |
| Pattern | The Turning Mosaic | 10 minutes. |
| Contradiction | Two Honest Lies | 10 minutes. |
| Transition | The Moving Steps | 3 rounds / 18 seconds. |

Full props, options, DCs, answers and failure states are in the model.

Success sets the existing EPI-01 pool to 2; it does not add an independent “Archon pool.”

Failure sets `VowReviewPending`. Player has agency:
- revise vow normally; or
- reaffirm it after 10m and take Disquiet.

No involuntary Oath/alignment/personality rewrite.

### 12 Revelation: Concord Step Sigil
This is a NEW module travel interface. It is not Planar Gate, Plane Shift, Teleportation Circle, time travel, or another spell.

Fixed endpoint set:
- Aethel Concord Hall threshold
- Bastion of Flame Concord Alcove
- Veiled Expanse Concord Alcove
- Radiant Currents Concord Alcove
- Boundless Void Concord Alcove

A particular destination must already be Director-declared available in the campaign. The sigil does not create an alcove after the fact.

Outbound:
- one use before next session begins;
- authorized origin threshold;
- 10m uninterrupted;
- petitioner + up to 5 willing nearby creatures;
- ordinary carried gear only.

Return:
- recorded as part of same authorization;
- within 8h;
- 10m uninterrupted from destination alcove;
- to original threshold;
- nearest legal unoccupied spaces within 30ft if needed.

If no return space exists, do not teleport into illegal occupancy; remain at destination and retry before expiry.

Arrival is only inside the alcove. Existing local exit barriers still exist. No dungeon gate, sealed room, or faction access is bypassed.

## EPI-07 — Sentinel information

### Encounter record
Each projection receives:
- `encounterId`
- location
- actual knowledge scope
- question
- whether one narrowing follow-up was used
- boon type
- exact information delivered
- spent flag

“Earnest” means character intends to use the answer for a current in-fiction question. Never judge the real player's sincerity.

If the Sentinel does not know, it says so. One narrowing follow-up is allowed; then the encounter is spent.

### Finite examples

#### Puzzle: Three Lamps
Question: which lamp opens the archive door?

Riddle:
- First: “I lie whenever Third is dark.”
- Second: “I tell truth exactly when First lies.”
- Third: “I am dark.”

**Answer: Second.** Third is dark, therefore First's condition makes First false; Second's condition is satisfied.

The boon supplies the answer, not physical access or an automatic success.

#### Map fragment
Provide exactly this local graph:
- Collapsed Gallery -> Bronze Door -> Echo Hall
- Collapsed Gallery -> Narrow Crawl -> Service Niche
- Echo Hall -> Stone Door -> Water Stair
- Service Niche -> one-way drop -> Water Stair

No teleport, key, door permission, deeper-floor truth or public map is created.

#### Contingent future
“If the western sluice remains open through the next bell under current pressure, the lower gallery floods to waist depth within 10 minutes.”

This is conditional. Closing the sluice or altering pressure can prevent it without retconning the vision.

## Remaining boundaries

This candidate does not settle:
- campaign epoch;
- nine-verses/seven-benefits historical accounting;
- EPI-08–17 mechanics;
- unresolved cosmological identities;
- runtime implementation;
- human playtest;
- balance;
- whole-game approval;
- publication.
