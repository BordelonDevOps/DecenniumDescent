# Codex of the Heartcell

## BB-01 — Monster Ecology, Gate Seals, and Creature Lexicon

*A Director's bestiary for Decennium Descent. Companion volume to the Player Rulebook and The Director's Crucible. 100% original Aethel material — no foreign tabletop product names appear in this book.*

**Book code:** BB-01
**Editable stats source:** `Bestiary.xlsx` (Monsters sheet) → re-ingested into `src/bestiary_data_full.json`. Edit the workbook, re-run the ingest, regenerate this Codex — never hand-edit stat numbers only in this file.

---

## What this book is

The *Codex of the Heartcell* is built the way an old-school bestiary is built: ecology first, statistics second. Before any Director opens a stat block, they should know what the creature *wants*, where it *lives*, and what it *costs* an Expedition to meet — win or lose. That is the order this book follows, chapter by chapter:

1. **Reading the Codex** — how a Decennium stat line works, and how to read the honesty flags this book uses constantly.
2. **The Ten Gate Seals** — full set-piece chapters for the Gate Guardians that end each tier of the Decennium, in descending order from Floor 10 to Floor 100.
3. **Ecologies and Lexicon of Aethel** — one ecology essay per creature family, immediately followed by every indexed creature of that family, sorted by Challenge Rating.
4. **Floor Cultures** — deeper looks at the living peoples of the Decennium's upper and middle floors, for Directors who want politics instead of pure combat.
5. **The Director's Toolkit** — quick monster creation, lair omens, tier-by-tier random pressure tables, and a short appendix of conditions.
6. **Numeric Challenge Index** — every indexed creature, sorted by Challenge Rating, for fast encounter-budget lookups.

## Draft-stat honesty (read this before you run anything from this book)

The Heartcell's bestiary was seeded from a portable spreadsheet generator before any Director had time to hand-tune every entry. That generator is honest about its own limits, and so is this book. Every lexicon entry below carries one of three provenance tags:

| Tag | What it means | What a Director should do |
|---|---|---|
| **Companion-authored draft** | A person wrote this creature's tactics and numbers on purpose (the ten Gate Guardians, mostly). Still draft, but intentional. | Run as written, adjust to taste. |
| **Excel-sandbox draft** | Numbers came from an automatic Challenge-Rating band generator. Attack names like *Tail Lash*, *Monstrous Claw*, *Freak Bite*, and *Aberrant Lash* are placeholders reused across hundreds of unrelated creatures. | Reflavor the attack name at the table for free. Treat the numbers as a fair starting budget, not gospel. |
| **STUB — Director must re-skin** | The Size/Type/CR combination is nonsensical (a Tiny Undead named after a sky-faring people, for instance), the name is a stock stand-in flagged for an Aethel rename, or the sheet's own `NeedsReview` column caught a size/HP inflation problem. | Do not run this showcase-ready. Reskin the name, correct the Size/Type, or swap in a nearby entry that already makes sense before spotlighting it. |

None of this is embarrassment — it is the difference between a bestiary that lies about being finished and one that tells a Director exactly how much trust to extend to each line. **A draft stat block run honestly at the table is better than a "finished" one that quietly breaks the fiction.**

This Codex does not touch `Bestiary.xlsx` directly. Every rename, stub flag, and correction proposed here is a **recommendation for the next Excel pass**, not a silent edit — see the Naming & IP Reskin Ledger in the Director's Toolkit for the full proposed rename list awaiting owner sign-off.

---

# Part I — Reading the Codex

## How to read a Decennium stat line

Every lexicon entry uses the same seven-field shape:

| Field | Meaning | Director note |
|---|---|---|
| **Size / Type / Alignment** | Fiction tags describing the creature's frame and disposition | Distrust nonsense combinations on sight — see STUB flags |
| **Challenge (XP)** | Encounter-budget aid, not a promise of balance | Draft XP awards should be treated as a starting point for the table, not a contract |
| **Zone** | Where the Excel ingest currently places this creature | A biome/region tag, independent of which tier or floor a party is actually descending through |
| **Armor / Hit Points / Speed** | The combat shell | Pulled directly from the sheet; flagged if the sheet itself flagged it |
| **Attacks** | Name, bonus, and damage | Prefer the sheet's bespoke names; generic sandbox names are called out explicitly |
| **Defenses** | Resistances, immunities, condition immunities | Only populated for companion-authored entries; sandbox entries default to none |
| **Provenance** | Which of the three honesty tags above applies | Announce draft status at the table when it matters |

## Gate Seal & legendary framing (Director rules)

The ten Gate Guardians are not random bosses — they are **seals**. Each one holds a division of the Decennium shut, and defeating one is a Cycle-defining event for the Expedition that manages it, not a Tuesday-night boss fight. Use these house rules to run them:

1. **One seal per division.** Do not reuse a Gate Guardian's stat block as a "harder version" of anything else. If the story needs two, that is a Director decision worth flagging at session zero.
2. **Telegraph before you fight.** A seal should be foreshadowed for a full in-fiction period — omens, lesser encounters, rumors from floor cultures, a research clue that only makes sense in hindsight — before the party ever rolls initiative against it.
3. **Seal Pulses, not foreign jargon.** When a Guardian needs a legendary-feeling turn between player turns, call it a **Seal Pulse**: a terrain effect, an environmental tell escalating, or a single free reaction tied to the room itself. This is Decennium Descent's own framing — do not import "legendary actions" language from other products at the table.
4. **The Canticle soft-quit line is morale, not the Horn.** Floor 50 (Choralith's seal) is where the overwhelming majority of Expeditions choose to turn back — that is a *fiction and morale* pressure point, separate from the Horn's point-of-no-return clock. Do not conflate the two when staging a session.
5. **Victory is bait, not closure.** Every seal's reward should visibly reopen new problems on the surface — see each chapter's "Reward as Bait" section. A Gate Guardian's death should never be the end of a story thread; it should be the opening of three more.
6. **Defeat costs hours and morale, not automatically the party.** Unless your table has explicitly opted into deadlier stakes, a failed seal attempt should cost Opening-calendar time and standing, not a default TPK.


---

# Part II — The Ten Gate Seals

Each Gate Guardian below is staged with its authoritative tier placement from the Chronicle of the Decennial Opening's floor gazetteer — not from the bestiary sheet's own (unreliable) description text, which was generated independently and frequently disagrees with itself about which floor each Guardian actually holds. Where the sheet and the gazetteer conflict, this Codex follows the gazetteer and calls out the discrepancy in a Draft-Stat Honesty box, so no Director is quietly running the wrong floor number.

---

## Gate Seal I — Vaskor, the Stone Maw

**Division:** Tier 1, Yieldheart Caverns (Floors 1–10) · **Seal:** the Warded Gate, end of Floor 3 · **Difficulty:** Novice

### Lore

Vaskor is the Decennium's oldest lie about safety. Floors 1–3 belong to the Automaton sentinels — patient, incorruptible, and utterly indifferent to anything that happens one floor further down. Vaskor is what convinced the Automatons to stop. Long before the current Cycle, something in the crystalline stone of Yieldheart learned to close its mouth around intruders, and the machines simply rerouted their patrols to end at its threshold rather than lose units testing it. Vaskor has never been "awake" in the way a hunting animal is awake; it is closer to a held breath the size of a cavern, and the Warded Gate is the exhale.

### Staging & Approach

The glyph puzzle sealing the Warded Gate is not decoration — it is the last thing standing between an Expedition and Vaskor's attention. A Director should telegraph the seal for the length of Floors 1–3: the Spire of Whispers murmuring warnings no one can quite parse, the Echoing Gallery amplifying a party's own noise back at them as rehearsal for what waits below, the Abandoned Stoneworks hinting that an entire dwarven expedition once tried to tame this ground and stopped trying at exactly this point. The Hearth of Yieldheart, tucked into a collapsed antechamber on Floor 3, is the last comfortable rest before the puzzle — let parties feel that comfort end.

### Lair & Terrain

Vaskor's chamber is a fusion of living rock and buried jungle stone, veined with the same luminescent minerals sold at Crystalfront Market above — which means every Expedition that outfitted itself at the surface bazaar is, in a small way, carrying a piece of this room with them already. The floor is not stable ground; it is Vaskor, extended, and burrow speed means it can withdraw beneath a party mid-fight and resurface anywhere the stone is thin.

### Tactics (Director)

Open with a burrow-and-surface strike to establish that the floor itself is a threat, then alternate the Stone Maw's twin bite-and-crush attacks against whoever clustered up first. Seismic Roar (its area shockwave) recharges fast — use it specifically to punish a Support team that planted itself in one spot to heal. Vaskor has middling Intelligence and low Charisma: it does not bargain, taunt, or feel goaded. It simply keeps closing its mouth until something stops fitting inside it.

### Reward as Bait

Vaskor's loot leans toward tremor-cores and stone-fused fangs — reagents the Anvil of Brogi's forges downstream (Tier 3) will pay well for. An Expedition that clears the Warded Gate is, whether they know it or not, now carrying an opening bid into Tier 3's crafting economy. Let a surface smith or floor-culture broker make that offer explicitly once the party surfaces.

### Draft-Stat Honesty

The sheet lists Vaskor as **Ooze**, Large, CR 8, Unaligned — but its own description calls it "a colossal earth elemental," and its abilities (burrow speed, Tremorsense, Terran, Athletics/Intimidation proficiency) all read as Elemental, not Ooze. This Codex plays Vaskor as **Elemental** in fiction and flags the Type field for correction. The sheet's field text also places it on "Floor 20 in the Heart of the Verdant Wild," which matches neither Yieldheart Caverns nor the Floor 10 seal position the Chronicle gazetteer assigns it — treat the gazetteer (Floor 10, Warded Gate) as canon and the sheet's location text as an unreconciled leftover from an earlier draft pass.

---

## Gate Seal II — The Bloom That Hungers

**Division:** Tier 2, Bloomdeep Marsh (Floors 11–20) · **Seal:** the Sporemist Gate, end of Floor 20 · **Difficulty:** Apprentice

### Lore

Bloomdeep Marsh is a closed biome — no outside bazaar, no Automaton patrol, nothing above ground has ever successfully cross-pollinated with it and lived to describe the process. The Bloom That Hungers is what that isolation eventually produces: a single carnivorous organism grown gargantuan on ten floors' worth of everything that never made it back out. It does not hunt Expeditions so much as it has simply never stopped growing toward the nearest heat source, and heat sources keep arriving on schedule, ten floors at a time, every Cycle.

### Staging & Approach

The Reedcaller's Circle on Floor 11 teaches parties that sound travels and betrays position — a lesson the Bloom has learned to exploit. Spore-Veil Falls and the Phantom Mire on Floors 12–13 exist specifically to soften a party (blinding spores, false-shallow pools) before they are anywhere near the Bloom itself; treat both as pre-seal attrition, not the seal fight. The Overgrown Reliquary's animated root-graspers on Floors 14–15 are the Bloom's outriders, not a separate species — killing them should visibly feed information (and biomass) back toward the Sporemist Gate.

### Lair & Terrain

The gate itself must be cleansed with three burning Heartroot Blossoms or it answers failure with necrotic backlash — meaning the Bloom's fight begins, mechanically, before the Bloom is even visible. Once past the gate, the lair is a closed wet chamber where burrow speed lets the Bloom's root mass approach from any angle, and where the ambient spore density means every round spent not moving is a round spent breathing the Bloom's hunting method.

### Tactics (Director)

Vine Maw is the Bloom's constant pressure — a single heavy piercing bite it can throw every round. Spore Burst is its area answer to a party that spreads out to avoid exactly that; use it the moment a Support team tries to kite at range. The Bloom has middling Wisdom and poor Intelligence: it is not clever, but its Stealth and Perception scores mean it rarely loses track of prey once blood is in the water (or sap).

### Reward as Bait

Rotroot Tendril and Lodestone Spore are both minor-but-real reagents for Bloomdeep-adjacent crafting; the real bait is narrative — the Sporemist Gate opening onto Tier 3's Anvil of Brogi means an Expedition that clears this seal has just connected two very different biomes' salvage economies, and floor cultures on both sides will have opinions about that.

### Draft-Stat Honesty

The sheet's field description places this Guardian on "Floor 10 in the Echoing Grotto" — the Chronicle gazetteer places it at the end of Floor 20 in Bloomdeep Marsh, guarding the Sporemist Gate. This Codex runs the Floor 20 / Sporemist Gate placement as canon. At CR 5, this is the *lowest*-challenge Gate Guardian in the entire ladder despite guarding the second seal — see the Seal Ladder note at the end of Part II for the full CR-curve honesty flag.

---

## Gate Seal III — Ashthirst the Hollow

**Division:** Tier 3, Anvil of Brogi (Floors 21–30) · **Seal:** the Lavaflow Gate, end of Floor 30 · **Difficulty:** Journeyman

### Lore

Brogi's forge-realm runs on the assumption that everything inside it either burns, hammers, or endures. Ashthirst endures — and resents every party that gets to leave afterward. It is not native heat or native metal; it is closer to a wound the forge never closed, a hollow shape of ash and wind that has learned to drink the life out of anything that pauses too long near its edges. Where the rest of Tier 3 is loud (hammer-strikes, molten rivers, the Chained Anvil's slow crushing arcs), Ashthirst is the one silence in the whole division, and silence here is worse than the noise.

### Staging & Approach

Hammerfall Hall and the Molten River Crossing on Floors 21–22 establish the forge's indifferent hazards — timing, heat, and terrain that punishes hesitation. The Chained Anvil Chamber on Floor 24 is a good mid-tier omen room: its suspended hammer swings on its own schedule, a preview of a boss that does not care whether the party is ready. The Rivetworks Maze on Floor 26 should feel like the corridors themselves are starting to resent the party's presence — a direct tonal rehearsal for Ashthirst.

### Lair & Terrain

The Lavaflow Gate requires a cooled slag key quenched in Brogi's Quenching Pool; failing the key invites superheated steam and molten metal before the fight even starts. Ashthirst's own chamber should feel like the one cold spot in a hot realm — flying and hovering speed let it hang above molten hazards a grounded party cannot safely stand in, forcing awkward positioning around terrain it ignores entirely.

### Tactics (Director)

Ash Claw is a fast, twin-strike necrotic pressure attack; Hollow Wail is a heavy psychic area burst on a fast recharge, best used against a party that just clustered to avoid the lava terrain. Ashthirst's genuinely high Charisma and solid Deception/Insight scores mean it should talk before and during the fight — false comfort, false warnings, anything that makes a Support team hesitate for one crucial round.

### Reward as Bait

Ashthirst's loot table is unusually deep for a Tier 3 seal — Aberrant Ichor, Mind Crystal, and Reality Shard drops all the way up through a Tier 4 rarity band. That is a deliberate mismatch a Director should lean into: word of an unusually rich Tier 3 kill should draw rival Expeditions and floor brokers who want a cut before the party ever reaches the surface market.

### Draft-Stat Honesty

Field text places Ashthirst on "Floor 30 in the Fields of Whispering Grasses" — the floor number matches the Chronicle's placement, but the location name does not match Anvil of Brogi's forge setting at all, and the sheet's Zone field ("Aethel Jungles") clashes with the forge biome a third way. Run Ashthirst as a forge-realm entity per the gazetteer; treat "Fields of Whispering Grasses" and "Aethel Jungles" as unreconciled leftover flavor text from a different draft pass, not active lore.

---

## Gate Seal IV — Gor Vekk, Architect of Ends

**Division:** Tier 4, Isles of Eternal Radiance (Floors 31–40) · **Seal:** the Radiance Gate, end of Floor 40 · **Difficulty:** Expert

### Lore

Every division so far has had an obvious hook — hunger, heat, stone. Gor Vekk has an argument instead: that everything ends, that the Isles' endless dawn is a held moment rather than a permanent one, and that its own presence is proof of the exception. Its warping of space and time around the Isles is not an attack; it is closer to an ongoing thesis statement the terrain itself keeps agreeing with. Gor Vekk is, bluntly, far too dangerous for a Tier 4 seal, and this Codex says so directly rather than pretending the escalation was intentional (see the honesty box below) — the correct table read is that Gor Vekk should be run *down* in effective difficulty by whatever margin your table needs, not run at face value.

### Staging & Approach

The Prismatic Archipelago and Mirror Reef on Floors 31 and 34 both foreshadow Gor Vekk's central trick: reflection and doubling that is not quite illusion and not quite real. The Radiant Bloom Gardens on Floor 32 give the party a tool (a dawn-glow tonic granting temporary radiant resistance) that is not incidental — Gor Vekk's attacks are almost entirely force and radiant-adjacent, and a Director should make sure the tonic-harvesting subplot actually pays off here.

### Lair & Terrain

The Radiance Gate demands three charged sun-shard vials placed precisely at dawn's zenith — a hard timing gate that should feel deliberate, not arbitrary, once Gor Vekk's whole conceit (endings arriving on a schedule) is on the table. Its lair is golden quartz and floating light; flight speed of 120 feet means it never has to fight on the ground a party can control.

### Tactics (Director)

Reality Sunder is a brutal triple-hit at-will force attack — treat it as Gor Vekk's default pressure, not a special move, because at this CR it can afford to spend it every round. End Architecture is the area finisher on a fast recharge; a Director running this fight at anything close to its listed CR should expect it to threaten a full party wipe on a single unlucky recharge, which is exactly why the honesty box below recommends scaling it down hard for a Tier 4 table.

### Reward as Bait

Fey Essence drops scale all the way to a Tier 6 rarity band — wildly disproportionate loot for a Tier 4 seal, and this Codex recommends leaning into that as *the* story hook: word that Gor Vekk's kill yields Tier 6-grade material should be the single most dangerous rumor circulating on the surface, drawing expeditions and factions who have no business attempting Tier 4 but every reason to try.

### Draft-Stat Honesty

**This is the single worst stat-line contradiction among the ten seals.** The sheet lists Gor Vekk as **Fey**, CR **29** — nearly at the Decennium's absolute ceiling — while its own field description calls it "an ancient aberration." The Chronicle gazetteer places it at Floor 40 (Tier 4, Expert difficulty); the sheet's own description text instead claims "Floor 90 in the Veiled Expanse." A CR 29 creature has no business anchoring the fourth of ten seals — it is stronger on paper than the Tier 8 and Tier 9 Guardians combined-difficulty expectation. Recommended Director fix: run Gor Vekk's *fiction* at Tier 4 (Expert) using roughly a third of its listed hit points and DCs, or reserve the sheet's numbers verbatim for a genuine end-game rematch appearance later in the Cycle. Do not run CR 29 numbers against a Tier 4 party as written.

---

## Gate Seal V — Choralith, Voice Below

**Division:** Tier 5, Sanctum of Echoing Choirs (Floors 41–50) · **Seal:** the Canticle Gate, end of Floor 50 · **Difficulty:** Master

### Lore

Choralith is the reason most Expeditions never see Floor 51. Not because it is unbeatable — because the Sanctum itself is where morale dies first. Every whisper becomes a symphony; every fear becomes a choir member. Choralith is simply the loudest voice in a division built entirely out of listening, and it has had every Cycle's worth of expedition chatter to learn exactly which frequencies make competent adventurers quietly, politely decide to go home.

### Staging & Approach

This is the single most important soft-quit point in the entire Decennium, and it should be staged as such. The Bar of Last Refuge on Floor 43 is where most parties have the actual conversation about turning back — a Director should let that conversation happen in fiction, not rush past it. The Whispering Pillars, Aeolian Mirror Pools, and A Cappella Alcove all build toward one idea: that sound and silence are both dangerous here, and that the party's own voice is a resource they are spending down.

### Lair & Terrain

The Canticle Gate demands four precise notes struck in perfect harmony, gleaned in sequence from the Whispering Pillars — a genuine puzzle gate, not a combat checkpoint, and failing it unleashes a backlash that damages both armor and spirit. Choralith's own chamber should be played as a cathedral of living sound: flight and a 60-foot fly speed let it use the whole vertical space, and its Truesight means hiding is not a viable tactic.

### Tactics (Director)

Resonant Lash is its twin-strike thunder attack; Subsonic Chord is a heavy area burst that recharges fast and should specifically target parties who bunch up to protect a caster. Choralith's very high Charisma and Arcana/History proficiencies mean it should talk in mid-fight — riddles, half-truths, and observations about the party's own fear responses, turning the encounter itself into psychological pressure rather than a pure damage race.

### Reward as Bait

Siren's Whisper and Bone Coral Phylactery are exactly the kind of unsettling, clearly-not-mundane trophies that should make surface collectors and floor cultists both want a look before the party even finishes cataloguing the loot. Choralith's death should generate rumor, not relief.

### Draft-Stat Honesty

Field text claims Floor 40 in "the Sepulcher of Silent Thrones" — which directly collides with Gor Vekk's field text, which *also* claims Floor 40. Both cannot be correct; the Chronicle gazetteer resolves the conflict by placing Choralith at Floor 50 (Canticle Gate, Tier 5) and Gor Vekk at Floor 40 (Radiance Gate, Tier 4). Run the gazetteer placement and treat both sheet descriptions as unreconciled draft leftovers.

---

## Gate Seal VI — Lumen of the Shattered Thread

**Division:** Tier 6, Crossroads of the Shattered Thread (Floors 51–60) · **Seal:** the Lumen Gate, end of Floor 60 · **Difficulty:** Adept

### Lore

**Director note: Tier 6 is an unmapped draft region.** Everything below the Canticle Gate is, in-fiction, survivor rumor rather than confirmed cartography — lean into that explicitly at the table. Lumen is a luminous knot of broken Weave-thread, formed from every path an Expedition *didn't* take through the Crossroads. It does not guard so much as accumulate: every route not chosen adds one more thread to what Lumen is made of, which means it is, quite literally, built from the sum of every Expedition's regrets.

### Staging & Approach

Because this tier is unmapped, treat the Threadbare Camp and the Shattered Crossroads as GM-improv anchors rather than fixed geography — the routes themselves are meant to feel unstable, per the region's own hazards (Path Recall, Weave-Snap, Lantern Doubt). A Director should feel free to invent additional Thread-Fork Galleries content as needed; the survivor-rumor framing means no fabricated detail here contradicts confirmed lore.

### Lair & Terrain

The Lumen Gate glows where the broken threads gather most tightly, and offers no explanation for which way it intends to lead — a genuinely disorienting final approach appropriate to a "Time" or "unmade path" theme.

### Tactics (Director)

Thread Lance is a twin heavy radiant strike; Thread Shatter is a fast-recharging force burst that should specifically punish a party that just repositioned, since Lumen's whole conceit is punishing the paths people choose. Its Truesight and telepathy in All languages mean it can taunt with specific, personal knowledge of the party's earlier route choices through the Crossroads — use this to make the fight feel omniscient rather than random.

### Reward as Bait

Fragment of Time and Fatewoven Lens both read as narratively loaded rather than mechanically explained — perfect hooks for a Director to attach unresolved plot threads that only pay off much later in the Cycle.

### Draft-Stat Honesty

No numeric HP or tactics for this Guardian were "confirmed" in the tier's own gazetteer entry — the sheet's CR 17 / 255 HP block is the only numeric draft available and should be explicitly announced as provisional, more so than any other seal in this book. This is also the first tier marked unmapped in the Chronicle; do not present its geography to players as settled.

---

## Gate Seal VII — Xarog, the Pactbound Furnace

**Division:** Tier 7, Pactbound Arena (Floors 61–70) · **Seal:** the Furnace Gate, end of Floor 70 · **Difficulty:** Veteran

### Lore

The Pactbound Arena runs on oaths the way Brogi's forge runs on heat. Xarog is the furnace that has been collecting those oaths since before the current Cycle's first Expedition arrived, and it speaks — when it speaks at all — in terms no survivor has ever managed to quote back in full. It is less a monster guarding a gate than a ledger with claws, tallying every bargain struck in the Arena above it.

### Staging & Approach

The Oath-Post Ring and the Pactbound Coliseum both establish the Arena's core mechanic: bargains that bind unpredictably, wounds treated as currency, defeated foes' oaths replaying as hostile echoes on later floors. A Director should let at least one mid-tier fight go sideways because of a "bargain" a player character made carelessly — Xarog's fight lands much harder if the table already understands that words are load-bearing here.

### Lair & Terrain

The Furnace Gate pools heat behind sealed ironwork, as if listening for the last word of a bargain no survivor can quote. Xarog's fire resistance and poison immunity mean elemental damage type matters enormously in this fight — a party that leaned on poison or fire tools all the way through Tier 7 should feel that investment fail here, on purpose.

### Tactics (Director)

Furnace Chain is a triple-hit, 20-foot-reach fire attack — Xarog does not need to close distance, which should inform how a Director positions it relative to melee-heavy parties. Its very high Deception and Intimidation scores mean it should offer a bargain mid-fight; a Director can make this genuinely tempting (a real mechanical benefit) at a genuinely painful cost, consistent with the Arena's whole ethos.

### Reward as Bait

Xarog's Infernal Heart is priced far above anything else in its own loot table (4,000 value vs. 1,200–2,000 for its lesser drops) — treat recovering it intact as its own mini-objective that rival Arena factions will contest immediately after the fight, not politely wait their turn for.

### Draft-Stat Honesty

**The sheet contains two separate Xarog entries that must not both be run.** "Xarog the Pactbound Furnace" (no comma) is a leftover Excel-sandbox row — Elemental, CR 10, using the generic placeholder attacks *Freak Bite* and *Tail Lash*, carrying no Gate Guardian tag and no bespoke abilities. "Xarog, the Pactbound Furnace" (with comma) is the companion-authored entry — Fiend, CR 26, tagged Gate Guardian, with bespoke Furnace Chain attacks and fire/poison defenses. **Use the comma version as canon and flag the no-comma duplicate for deletion in the next Excel pass.** Field text also claims "Floor 80," but the Chronicle gazetteer places Xarog at Floor 70 (Furnace Gate, Tier 7) — run Floor 70 as canon.

---

## Gate Seal VIII — Eirfax, the Dusk Crowned

**Division:** Tier 8, Duskshard Pools (Floors 71–80) · **Seal:** the Crown Gate, end of Floor 80 · **Difficulty:** Elite

### Lore

Duskshard Pools trade light and hush like currency, and Eirfax wears whichever one is winning at the moment as a literal crown. It is a twilight power that has learned reflection is more honest — and more frightening — than presence: survivor accounts consistently describe seeing its crown-shaped silhouette in still water more clearly than in the air above it, as though the Pools have a better claim to what Eirfax actually is than Eirfax does.

### Staging & Approach

The Duskshard Basins establish the tier's defining hazard — a surface that looks still from one bank and shows a different dusk from the next, meaning even scouting ahead does not guarantee consistent information. The Twilight Shelf safe haven exists specifically so parties learn to trust the basin glow before resting near it; undercut that trust once, subtly, before the Crown Gate.

### Lair & Terrain

The Crown Gate rises from the deepest reflected light at the Pools' edge — approach it as a reflection-heavy final stretch, consistent with Eirfax's whole design language.

### Tactics (Director)

Dusk Blade is a triple-hit slashing attack at-will; Crown of Dusk is a heavy necrotic area burst on fast recharge. Eirfax's very high Deception and solid Arcana/Insight mean it should offer flattery and false comfort mid-fight, consistent with a "crowned" entity that expects to be deferred to even while losing.

### Reward as Bait

Crown of Frozen Authority and Memory of the World both read as legacy-grade trophies — this Codex recommends Eirfax's death circulate as the story of *whoever* recovers and wears the crown next, seeding a surface succession plot independent of the party's own choices.

### Draft-Stat Honesty

The sheet's Type is **Fiend**, but its own field description calls Eirfax "a twilight fey lord" — a direct Type/description contradiction this Codex flags rather than silently resolves. Field text also claims "Floor 70," while the Chronicle gazetteer places Eirfax at Floor 80 (Crown Gate, Tier 8); run Floor 80 as canon. Tier 8 is another unmapped draft region — treat its geography as survivor rumor at the table.

---

## Gate Seal IX — Threxus, the Iron Spiral

**Division:** Tier 9, Veiled Iron Spiral (Floors 81–90) · **Seal:** the Spiral Gate, end of Floor 90 · **Difficulty:** Mythic

### Lore

The Veiled Iron Spiral is a descending helix that tightens the Weave around anyone who refuses to turn back, and Threxus is that pressure given a shape: iron and radiant geometry in constant, deliberate rotation. Survivor theology confuses Threxus's name with the Turning Spiral patron faith — this Codex treats that confusion as an in-world rumor problem, not a lore fact, and Directors should let player characters encounter the mix-up as a genuine source of misinformation rather than resolving it for them.

### Staging & Approach

The Veiled Helix establishes that both the path ahead and the last bend behind become invisible on the curve — distance itself becomes something the Spiral withholds. This is an excellent Director tool for pacing dread on the approach: let a party's own sense of progress become unreliable well before Threxus appears.

### Lair & Terrain

The Spiral Gate is "another turn of the same iron made absolute," with a seam visible only when shadow slips across it — a genuinely difficult-to-find final threshold appropriate to a Mythic-difficulty approach.

### Tactics (Director)

Spiral Strike is a triple-hit slashing at-will attack; Iron Vortex is a heavy bludgeoning area burst on fast recharge that should be used to punish a party trying to use the helix's own terrain for cover. Threxus's excellent Athletics and solid Intimidation support a straightforward, overwhelming-force combat style rather than trickery — it does not need to be clever when it can simply be enormous and constant.

### Reward as Bait

Adaptive Servo Node and Spiral Soul Engine both suggest a construct-adjacent origin worth a Director's attention (see the honesty box below) — treat these as valuable to any floor culture doing iron-and-Weave engineering, which should draw immediate attention from Tier 9's Murkish Rivet-Tunnel factions.

### Draft-Stat Honesty

The sheet lists Threxus as **Fey**, but its own field description calls it "a massive construct of spiraling iron and radiant energy" — another direct Type/description contradiction. This Codex recommends **Construct** as the corrected Director-canon type, pending an Excel fix. Field text also claims "Floor 60," while the Chronicle gazetteer places Threxus at Floor 90 (Spiral Gate, Tier 9) — a 30-floor discrepancy, the largest floor-mismatch among all ten seals apart from Gor Vekk's. Run Floor 90 as canon.

---

## Gate Seal X — The Marquis of Silence

**Division:** Tier 10, Silencebound Void (Floors 91–100) · **Seal:** the Marquis Gate, end of Floor 100 · **Difficulty:** Legendary

### Lore

The Marquis waits without ceremony at the end of the known descent, in a hush deep enough that even the First Choir's echo cannot reach it. Survivor myth calls the Marquis a demon lord, and this Codex leans into that framing directly: the Marquis rules the Silencebound Void the way a court rules a silence everyone has agreed not to break, through fear that predates argument and stillness that outlasts patience. Full-Cycle victory rumor treats defeating the Marquis as the closest thing the Decennium has to a completed story — and this Codex reminds Directors that "completed" and "safe to run at face value" are not the same claim.

### Staging & Approach

Every prior seal has been a lesson the Marquis assumes the party has already learned. The Hush Threshold marks no clean boundary — sound simply thins until the party notices the last reply never arrived — and that should be played literally: spells with verbal components, communication, even simple conversation between player characters should feel like a spent resource by the time the Marquis Gate is in sight.

### Lair & Terrain

The Marquis Gate is the Decennium's deepest, waiting without ceremony, its stillness making every survivor account of the depths feel unfinished. This is the single fight in the entire Codex that should never be treated as routine, regardless of table power level.

### Tactics (Director)

Silent Decree is a triple-hit psychic attack at-will; Zone of Silence is the single heaviest area burst of any Gate Guardian in this book (10d10 psychic on a fast recharge) and should be run as the genuine capstone threat it is. The Marquis's extraordinary Deception, Intimidation, Insight, and Perception scores mean it should never be caught by a trick twice, and it should speak — rarely, precisely, and only to say something the party will still be thinking about after the fight ends.

### Reward as Bait

This is the endgame. Mouthless Mask and Silken Shadow Coil are almost certainly the least interesting rewards available here — the real "loot" of defeating the Marquis of Silence is narrative: full-Cycle recognition, Custodian/Signatory-adjacent attention from the Heartcell's inner circles, and a season's worth of surface consequences a Director should plan out in advance, not improvise on the spot.

### Draft-Stat Honesty

The sheet lists the Marquis as **Ooze** — flatly inconsistent with its own field description as "a demon lord of unimaginable power." This Codex recommends **Fiend** as the corrected Director-canon type. More seriously: the sheet's alignment is listed as **Chaotic Good**, which cannot be reconciled with a feared demon lord "who rules through silence and fear" by any reading. Flag this alignment field for correction to an evil alignment before ever printing it on a table-facing sheet; do not narrate the Marquis as secretly benevolent based on this sandbox artifact.

---

## The Seal Ladder — an honest look at Challenge Rating across all ten seals

| Tier | Guardian | Sheet CR | Expected curve position |
|---|---|---|---|
| 1 | Vaskor, the Stone Maw | 8 | Reasonable floor for a Novice seal |
| 2 | The Bloom That Hungers | 5 | **Lower than Tier 1** — inverted |
| 3 | Ashthirst the Hollow | 11 | Reasonable |
| 4 | Gor Vekk, Architect of Ends | 29 | **Wildly inflated** — see Seal IV honesty box |
| 5 | Choralith, Voice Below | 14 | Reasonable, but far below Tier 4's neighbor |
| 6 | Lumen of the Shattered Thread | 17 | Reasonable, unconfirmed tier |
| 7 | Xarog, the Pactbound Furnace | 26 (canon) / 10 (stray duplicate) | High, but the second-highest seal is earlier appropriate escalation than Tier 4's spike |
| 8 | Eirfax, the Dusk Crowned | 23 | Reasonable |
| 9 | Threxus, the Iron Spiral | 20 | **Lower than Tier 8** — inverted |
| 10 | The Marquis of Silence | 30 | Correct as the ceiling |

Read plainly: the intended difficulty curve (Novice through Legendary) is **not monotonic** in the current sheet. Tier 4's Gor Vekk and Tier 7's Xarog are both dramatically over-tuned relative to their neighbors, while Tiers 2 and 9 dip below the seal immediately before them. This Codex does not silently smooth the curve — see `CODEX_QUALITY_AUDIT.md` for the full proposed correction and the owner decision it is waiting on.


---

# Part III — Ecologies and Lexicon of Aethel

Each family below opens with a short ecology essay, then lists every indexed creature of that family sorted from lowest to highest Challenge Rating. Entries marked **STUB** should not be run showcase-ready without a Director pass — see the honesty tags explained in Part I.


## The Aberrations

The Aberrations of Aethel are not a species so much as a symptom — proof that the Spiral's geometry has thin places, and that something pours through wherever it thins. No two Directors need to explain them the same way twice; the truth Aethel's own scholars keep discovering is that Aberrations resist a single origin story, and that resistance is the point. **Player knowledge** should stay at the level of rumor and survivor testimony: wrongness, incomprehension, things that were clearly never meant to be understood by a living mind. **Director knowledge** goes further — Aberrations are often the most reliable evidence that a given floor sits near an old Weave-fold, and their lairs are worth mapping even when the creature itself is avoided. Emphasize incomprehension and environmental wrongness over conventional monster tactics; an Aberration fight should feel like an argument with the room, not just with the creature in it.

*Indexed creatures of this family: **34**.*

### Aboleth

*Huge Aberration, True Neutral.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

Something in Bastion of Flame never finished agreeing with the rest of Aethel's geometry, and Aboleth is the proof. Directors should play its intelligence as patient and incurious about mercy. Treat it as a Research hook first and a fight second — knowledge here is worth more than the kill.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Mind Lash** (Recharge 5-6) — 5d6 psychic, 20-ft. radius — intelligence save DC 16 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Depth Toad Archpriest — STUB

*Large Aberration, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Tundra.

Where the Weave frays thin over Aethel Tundra, wrongness like Depth Toad Archpriest condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Depth Toad Archpriest* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Aberration**) was randomized independently of the Depth Toad concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gaze Tyrant

*Medium Aberration, Chaotic Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Tundra.

No cosmology fully claims Gaze Tyrant; it simply persists where Aethel Tundra stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quasit — STUB

*Huge Aberration, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Quasit reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Quasit* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Matron — STUB

*Large Aberration, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Tundra.

Where the Weave frays thin over Aethel Tundra, wrongness like Umbrin Matron condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Umbrin Matron* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Aberration**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vargouille — STUB

*Large Aberration, Chaotic Neutral.* **Challenge 7** (2900 XP). **Zone:** Spiral Nexus.

No cosmology fully claims Vargouille; it simply persists where Spiral Nexus stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — Director must re-skin.** The name *Vargouille* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### White Abishai — STUB

*Huge Aberration, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

No cosmology fully claims White Abishai; it simply persists where Bastion of Flame stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — stock alias, Director must re-skin.** Part of the Abishai (color devil) family; proposed: *Pact Devil*. Replace with Pact Devil, colored by Chaos-Realm court per Continuity C.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Chasme — STUB

*Large Aberration, True Neutral.* **Challenge 8** (3900 XP). **Zone:** Boundless Void.

Where the Weave frays thin over Boundless Void, wrongness like Chasme condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Chasme* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Glabrezu — STUB

*Large Aberration, Lawful Good.* **Challenge 8** (3900 XP). **Zone:** Aethel Oceans.

Something in Aethel Oceans never finished agreeing with the rest of Aethel's geometry, and Glabrezu is the proof. Directors should play its intelligence as patient and incurious about mercy. Treat it as a Research hook first and a fight second — knowledge here is worth more than the kill.

> **STUB — Director must re-skin.** The name *Glabrezu* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Glabrezu rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quipper — STUB

*Large Aberration, True Neutral.* **Challenge 8** (3900 XP). **Zone:** Aethel Caves.

Quipper reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Quipper* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shadow — STUB

*Large Aberration, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Boundless Void.

Shadow reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Shadow* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Azer — STUB

*Huge Aberration, Chaotic Neutral.* **Challenge 9** (5000 XP). **Zone:** Aethel Deserts.

Where the Weave frays thin over Aethel Deserts, wrongness like Azer condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Azer* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bodak — STUB

*Large Aberration, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

Something in Bastion of Flame never finished agreeing with the rest of Aethel's geometry, and Bodak is the proof. Directors should play its intelligence as patient and incurious about mercy. Treat it as a Research hook first and a fight second — knowledge here is worth more than the kill.

> **STUB — Director must re-skin.** The name *Bodak* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cow — STUB

*Large Aberration, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Cow reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Cow* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Mind Master — STUB

*Medium Aberration, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Where the Weave frays thin over Aethel Caves, wrongness like Deep Dwarf Mind Master condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Deep Dwarf Mind Master* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Aberration**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mastiff — STUB

*Medium Aberration, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Null Zones.

No cosmology fully claims Mastiff; it simply persists where Null Zones stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — Director must re-skin.** The name *Mastiff* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mimic — STUB

*Medium Aberration, Lawful Evil.* **Challenge 9** (5000 XP). **Zone:** Veiled Expanse.

No cosmology fully claims Mimic; it simply persists where Veiled Expanse stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — Director must re-skin.** The name *Mimic* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sahuagin Baron — STUB

*Large Aberration, Chaotic Neutral.* **Challenge 9** (5000 XP). **Zone:** Veiled Expanse.

Where the Weave frays thin over Veiled Expanse, wrongness like Sahuagin Baron condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Sahuagin Baron* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Red Slaad — STUB

*Large Aberration, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Aethel Caves.

Where the Weave frays thin over Aethel Caves, wrongness like Red Slaad condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Red Chaos-Husk*. Invented planar-race terminology; needs Aethel identity.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Scout — STUB

*Medium Aberration, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Choir Sanctum.

Scout reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Scout* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Ravens — STUB

*Large Aberration, Lawful Good.* **Challenge 10** (5900 XP). **Zone:** Null Zones.

No cosmology fully claims Swarm of Ravens; it simply persists where Null Zones stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ashthirst the Hollow

*Medium Aberration, Unaligned.* **Challenge 11** (7200 XP). **Zone:** Aethel Jungles.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 16 · **Hit Points** 195 · **Speed** 40 ft., fly 60 ft. (hover)

**Abilities** STR 16 · DEX 18 · CON 16 · INT 14 · WIS 16 · CHA 20

**Skills** Deception +9, Insight +7, Perception +7

**Senses** Darkvision 120 ft., passive Perception 17

**Languages** Common, Abyssal

**Attacks**
- **Ash Claw** (x2) — +8 to hit — 2d8+4 necrotic
- **Hollow Wail** (Recharge 5-6) — 5d8 psychic, 20-ft. radius — wisdom save DC 16 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Balor — STUB

*Huge Aberration, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** The Dungeon.

Balor reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Balor* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Balor rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Draegloth — STUB

*Huge Aberration, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** Aethel Tundra.

No cosmology fully claims Draegloth; it simply persists where Aethel Tundra stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Umbrin Warborn* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gaze Tyrant (in lair)

*Huge Aberration, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Aethel Caves.

Where the Weave frays thin over Aethel Caves, wrongness like Gaze Tyrant (in lair) condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gorgon — STUB

*Huge Aberration, Lawful Neutral.* **Challenge 11** (7200 XP). **Zone:** Spiral Nexus.

Where the Weave frays thin over Spiral Nexus, wrongness like Gorgon condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Gorgon* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swashbuckler — STUB

*Huge Aberration, Unaligned.* **Challenge 11** (7200 XP). **Zone:** The Dungeon.

Swashbuckler reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> **STUB — Director must re-skin.** The name *Swashbuckler* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Voidmind

*Huge Aberration, Chaotic Neutral.* **Challenge 11** (7200 XP). **Zone:** Aethel Caves.

Voidmind reads as a rumor the Spiral told itself twice, once correctly. It does not hunt so much as arrive, and things nearby stop behaving like themselves. Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Voidmind Arcanist

*Huge Aberration, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** Bastion of Flame.

No cosmology fully claims Voidmind Arcanist; it simply persists where Bastion of Flame stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Alkilith — STUB

*Huge Aberration, True Neutral.* **Challenge 12** (8400 XP). **Zone:** Radiant Isles.

Something in Radiant Isles never finished agreeing with the rest of Aethel's geometry, and Alkilith is the proof. Directors should play its intelligence as patient and incurious about mercy. Treat it as a Research hook first and a fight second — knowledge here is worth more than the kill.

> **STUB — Director must re-skin.** The name *Alkilith* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Alkilith rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Crocodile — STUB

*Huge Aberration, True Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Tundra.

Where the Weave frays thin over Aethel Tundra, wrongness like Crocodile condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Crocodile* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll Witherling — STUB

*Huge Aberration, Lawful Evil.* **Challenge 12** (8400 XP). **Zone:** Aethel Lowlands.

No cosmology fully claims Gnoll Witherling; it simply persists where Aethel Lowlands stops making sense. It communicates in impressions rather than words, and most minds regret understanding it. Recovering intact remains is its own small Expedition inside the Expedition.

> **STUB — Director must re-skin.** The name *Gnoll Witherling* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ox — STUB

*Huge Aberration, Chaotic Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Swamps.

Where the Weave frays thin over Aethel Swamps, wrongness like Ox condenses out of the gap. Expedition Recon reports rarely agree on its shape twice in the same debrief. Support teams should expect sanity and morale costs that outlast the encounter.

> **STUB — Director must re-skin.** The name *Ox* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Aberration** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Choralith, Voice Below

*Large Aberration, Chaotic Neutral.* **Challenge 14** (11500 XP). **Zone:** Choir Sanctum.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 18 · **Hit Points** 225 · **Speed** 30 ft., fly 60 ft.

**Abilities** STR 18 · DEX 14 · CON 18 · INT 20 · WIS 16 · CHA 22

**Skills** Arcana +11, History +11, Perception +8

**Senses** Truesight 120 ft., passive Perception 18

**Languages** Deep Speech, telepathy 120 ft.

**Attacks**
- **Resonant Lash** (x2) — +9 to hit — 2d10+5 thunder
- **Subsonic Chord** (Recharge 5-6) — 6d8 thunder, 20-ft. radius — constitution save DC 17 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*


## The Beasts

Beasts are Aethel's least mysterious residents and, for exactly that reason, its most persistent hazard. Most predate the Decennium's architecture entirely — they simply never left when the floors closed in around them, and they have gone on hunting, denning, and migrating in patterns a patient Recon team can learn to read. **Player knowledge** is whatever local hunters, floor cultures, and prior Expeditions have already worked out: territory, diet, and the difference between a Beast that flees a torch and one that doesn't. **Director knowledge** should treat Beasts as pressure on resources — rations, light, rope, time — rather than as headline encounters. Use them to teach new Combat teams the value of avoidance, and reserve genuine set-piece treatment for the rare Beast that has grown unnaturally large or bold on whatever a given floor feeds it.

*Indexed creatures of this family: **67**.*

### Brown Bear

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Expeditions meet Brown Bear as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dire Wolf

*Small Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Nothing about Dire Wolf is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Owl

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Giant Owl predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Green Slaad — STUB

*Small Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Expeditions meet Green Slaad as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Green Chaos-Husk*. Invented planar-race terminology; needs Aethel identity.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ice Mephit — STUB

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Expeditions meet Ice Mephit as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Ice Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Leucrotta — STUB

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Leucrotta predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Leucrotta* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Maurezhi — STUB

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Lowlands.

Maurezhi predates the Decennium's architecture and will outlast this Cycle's version of Aethel Lowlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Maurezhi* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Maurezhi rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Owlbear — STUB

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Expeditions meet Owlbear as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Owlbear* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Hookbeast* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Phase Spider

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Nothing about Phase Spider is dungeon-born; it simply never left Aethel Highlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Polar Bear

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Expeditions meet Polar Bear as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spider

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Spider predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Thug — STUB

*Small Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Nothing about Thug is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Thug* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tiger

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Tiger predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Inquisitor — STUB

*Small Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Nothing about Umbrin Inquisitor is dungeon-born; it simply never left Aethel Highlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Umbrin Inquisitor* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Beast**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Winter Wolf

*Tiny Beast, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Forests.

Winter Wolf predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Boar

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Swamps.

Boar predates the Decennium's architecture and will outlast this Cycle's version of Aethel Swamps. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Poisonous Snake

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Highlands.

Expeditions meet Giant Poisonous Snake as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Spider

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Highlands.

Expeditions meet Giant Spider as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Imp — STUB

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Swamps.

Imp predates the Decennium's architecture and will outlast this Cycle's version of Aethel Swamps. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Imp* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Poisonous Snake

*Small Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Swamps.

Nothing about Poisonous Snake is dungeon-born; it simply never left Aethel Swamps once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Reef Shark

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Oceans.

Expeditions meet Reef Shark as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Roc

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Highlands.

Expeditions meet Roc as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sea Spawn — STUB

*Small Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Lowlands.

Nothing about Sea Spawn is dungeon-born; it simply never left Aethel Lowlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Sea Spawn* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Werewolf

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Forests.

Werewolf predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wolf

*Tiny Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Forests.

Nothing about Wolf is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Remorhaz — STUB

*Small Beast, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Swamps.

Young Remorhaz predates the Decennium's architecture and will outlast this Cycle's version of Aethel Swamps. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Young Remorhaz* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Black Bear

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Forests.

Black Bear is Aethel Forests's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Constrictor Snake

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Forests.

Expeditions meet Constrictor Snake as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cult Fanatic — STUB

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Nothing about Cult Fanatic is dungeon-born; it simply never left Aethel Highlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Cult Fanatic* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Eagle

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Expeditions meet Eagle as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flying Snake

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Forests.

Flying Snake is Aethel Forests's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Constrictor Snake

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Swamps.

Nothing about Giant Constrictor Snake is dungeon-born; it simply never left Aethel Swamps once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Howler

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Howler predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Medusa — STUB

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Forests.

Medusa predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Medusa* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Merrow — STUB

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Nothing about Merrow is dungeon-born; it simply never left Aethel Highlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Merrow* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Owl

*Small Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Forests.

Nothing about Owl is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Saber-toothed Tiger

*Medium Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Swamps.

Saber-toothed Tiger is Aethel Swamps's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Poisonous Snakes

*Medium Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Swarm of Poisonous Snakes is Aethel Highlands's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Unicorn — STUB

*Medium Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Expeditions meet Unicorn as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Unicorn* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vulture

*Medium Beast, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Vulture is Aethel Highlands's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bandit — STUB

*Small Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lowlands.

Expeditions meet Bandit as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Bandit* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*
- **Desperate Lunge** (Recharge 6-6) — +4 to hit — 1d8+2 piercing

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bugbear — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Forests.

Nothing about Bugbear is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Bugbear* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bugbear Chief — STUB

*Small Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Forests.

Bugbear Chief predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Bugbear Chief* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Camel

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lowlands.

Nothing about Camel is dungeon-born; it simply never left Aethel Lowlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Chuul — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Forests.

Chuul is Aethel Forests's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *Chuul* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fire Snake — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lowlands.

Nothing about Fire Snake is dungeon-born; it simply never left Aethel Lowlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Fire Snake* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lion

*Small Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Swamps.

Lion predates the Decennium's architecture and will outlast this Cycle's version of Aethel Swamps. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Thorny Vegepygmy — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Swamps.

Nothing about Thorny Vegepygmy is dungeon-born; it simply never left Aethel Swamps once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> **STUB — Director must re-skin.** The name *Thorny Vegepygmy* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lowlands.

Umbrin is Aethel Lowlands's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *Umbrin* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Beast**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Voidmind Archivist — STUB

*Small Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Swamps.

Expeditions meet Voidmind Archivist as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Voidmind Archivist* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Beast**) was randomized independently of the Voidmind concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### War Priest — STUB

*Medium Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lowlands.

War Priest is Aethel Lowlands's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *War Priest* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Weretiger

*Small Beast, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Highlands.

Nothing about Weretiger is dungeon-born; it simply never left Aethel Highlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Chitine — STUB

*Small Beast, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Forests.

Chitine is Aethel Forests's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *Chitine* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Eagle

*Medium Beast, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Swamps.

Giant Eagle predates the Decennium's architecture and will outlast this Cycle's version of Aethel Swamps. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hawk

*Medium Beast, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Lowlands.

Nothing about Hawk is dungeon-born; it simply never left Aethel Lowlands once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d8+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rat

*Small Beast, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Swamps.

Rat is Aethel Swamps's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Werebear

*Small Beast, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Forests.

Expeditions meet Werebear as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Blood Hawk

*Medium Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Forests.

Blood Hawk is Aethel Forests's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*
- **Blood Dive** (Recharge 6-6) — +5 to hit — 2d6+2 slashing

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Blue Abishai — STUB

*Medium Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Swamps.

Expeditions meet Blue Abishai as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — stock alias, Director must re-skin.** Part of the Abishai (color devil) family; proposed: *Pact Devil*. Replace with Pact Devil, colored by Chaos-Realm court per Continuity C.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bulette — STUB

*Large Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Highlands.

Bulette predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Bulette* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cave Bear

*Medium Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Forests.

Cave Bear predates the Decennium's architecture and will outlast this Cycle's version of Aethel Forests. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cultist — STUB

*Small Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Lowlands.

Expeditions meet Cultist as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Cultist* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Wolf Spider

*Medium Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Forests.

Nothing about Giant Wolf Spider is dungeon-born; it simply never left Aethel Forests once the floors closed over it. It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal. A Director can let this be the fight that teaches new Combat teams to conserve resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll Fang of Yeenoghu — STUB

*Medium Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Highlands.

Gnoll Fang of Yeenoghu predates the Decennium's architecture and will outlast this Cycle's version of Aethel Highlands. Left alone, it is scenery; provoked, it is attrition. Its parts feed Resource Team drop tables more than its death feeds a story.

> **STUB — Director must re-skin.** The name *Gnoll Fang of Yeenoghu* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Gnoll Fang of the Howling Fracture* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Favored Consort — STUB

*Large Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Swamps.

Umbrin Favored Consort is Aethel Swamps's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *Umbrin Favored Consort* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Beast**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Winter Eladrin — STUB

*Small Beast, Unaligned.* **Challenge 2** (450 XP). **Zone:** Aethel Swamps.

Winter Eladrin is Aethel Swamps's answer to hunger — mundane in ancestry, dangerous only in number or terrain. Packs or herds of it read {zone}'s hazards better than most parties do on a first pass. Use it to tax rations, light, and rope rather than headline a set-piece.

> **STUB — Director must re-skin.** The name *Winter Eladrin* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Eladrin (season) family; proposed: *Winter Season-Bound*. Setting-specific fey-noble term tied to an external calendar cosmology.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Kruthik — STUB

*Large Beast, Unaligned.* **Challenge 13** (10000 XP). **Zone:** Aethel Forests.

Expeditions meet Adult Kruthik as a travel problem long before they meet it as a combat problem. It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful. It is the fight most parties should be able to avoid, if they think to.

> **STUB — Director must re-skin.** The name *Adult Kruthik* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Beast** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Celestials

A Celestial encountered this far into the Decennium is never simply good news. Whatever higher harmony sent it down here did not account for what the Pact's dissonance economy would eventually ask of it, and most Celestials an Expedition meets have been down here long enough to have complicated, compromised motives layered over whatever radiant mandate they started with. **Player knowledge** should read them as rare, striking, and morally unresolved — never a guaranteed ally. **Director knowledge** treats Celestials as leverage: conditional aid, expensive bargains, and judgment that is not calibrated to player convenience. A Celestial's help should always cost something specific, and its fall (if it falls) should register somewhere above the Decennium that a Director has already decided how to use later.

*Indexed creatures of this family: **34**.*

### Blue Slaad — STUB

*Medium Celestial, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Resonance Fields.

Whatever sent Blue Slaad into Resonance Fields did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Blue Chaos-Husk*. Invented planar-race terminology; needs Aethel identity.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Depth Toad Taskmaster — STUB

*Large Celestial, Chaotic Good.* **Challenge 7** (2900 XP). **Zone:** Radiant Isles.

Depth Toad Taskmaster claims descent from higher harmony, though Radiant Isles has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Depth Toad Taskmaster* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Celestial**) was randomized independently of the Depth Toad concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hobgoblin Devastator — STUB

*Large Celestial, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Choir Sanctum.

Hobgoblin Devastator claims descent from higher harmony, though Choir Sanctum has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Hobgoblin Devastator* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Knight — STUB

*Large Celestial, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Radiant Isles.

Whatever sent Knight into Radiant Isles did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Knight* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rust Monster — STUB

*Large Celestial, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Choir Sanctum.

Radiance clings to Rust Monster the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Rust Monster* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Corrosion Grazer* (not yet locked — see Naming & IP Reskin Ledger).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warhorse — STUB

*Large Celestial, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Resonance Fields.

Whatever sent Warhorse into Resonance Fields did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Warhorse* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Assassin — STUB

*Huge Celestial, Lawful Good.* **Challenge 8** (3900 XP). **Zone:** Radiant Isles.

Assassin claims descent from higher harmony, though Radiant Isles has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Assassin* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Oni — STUB

*Huge Celestial, Lawful Good.* **Challenge 8** (3900 XP). **Zone:** Radiant Isles.

Radiance clings to Oni the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Oni* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Reaver Supreme Commander — STUB

*Large Celestial, Neutral Good.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Whatever sent Astral Reaver Supreme Commander into Radiant Isles did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Astral Reaver Supreme Commander* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Celestial**) was randomized independently of the Astral Reaver concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cave Gnome — STUB

*Large Celestial, Lawful Good.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Radiance clings to Cave Gnome the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Cave Gnome* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Celestial**) was randomized independently of the Cave Gnome concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Devourer — STUB

*Huge Celestial, Lawful Good.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Devourer carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Devourer* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Red Abishai — STUB

*Huge Celestial, Chaotic Good.* **Challenge 9** (5000 XP). **Zone:** Choir Sanctum.

Radiance clings to Red Abishai the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — stock alias, Director must re-skin.** Part of the Abishai (color devil) family; proposed: *Pact Devil*. Replace with Pact Devil, colored by Chaos-Realm court per Continuity C.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sahuagin Priestess — STUB

*Large Celestial, Lawful Good.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Sahuagin Priestess carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Sahuagin Priestess* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Smoke Mephit — STUB

*Large Celestial, Chaotic Good.* **Challenge 9** (5000 XP). **Zone:** Choir Sanctum.

Whatever sent Smoke Mephit into Choir Sanctum did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Smoke Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Cranium Rats — STUB

*Large Celestial, Neutral Good.* **Challenge 9** (5000 XP). **Zone:** Choir Sanctum.

Whatever sent Swarm of Cranium Rats into Choir Sanctum did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Swarm of Cranium Rats* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cloaker — STUB

*Medium Celestial, Neutral Good.* **Challenge 10** (5900 XP). **Zone:** Radiant Isles.

Radiance clings to Cloaker the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Cloaker* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flameskull — STUB

*Large Celestial, Lawful Good.* **Challenge 10** (5900 XP). **Zone:** Radiant Isles.

Flameskull claims descent from higher harmony, though Radiant Isles has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Flameskull* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Planetar — STUB

*Large Celestial, Lawful Good.* **Challenge 10** (5900 XP). **Zone:** Resonance Fields.

Whatever sent Planetar into Resonance Fields did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Scorpion — STUB

*Large Celestial, Lawful Good.* **Challenge 10** (5900 XP). **Zone:** Choir Sanctum.

Scorpion carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Scorpion* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Catoblepas — STUB

*Large Celestial, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Resonance Fields.

Whatever sent Catoblepas into Resonance Fields did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Catoblepas* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deathlock Wight — STUB

*Huge Celestial, Lawful Good.* **Challenge 11** (7200 XP). **Zone:** Resonance Fields.

Whatever sent Deathlock Wight into Resonance Fields did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** The name *Deathlock Wight* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deva — STUB

*Huge Celestial, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Radiant Isles.

Whatever sent Deva into Radiant Isles did not account for what the Pact would ask of it here. It speaks in certainties and expects them honored; Directors should make that costly, not comforting. Its presence should complicate a floor's politics, not simplify a fight.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Incubus — STUB

*Huge Celestial, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Resonance Fields.

Incubus carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Incubus* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kenku — STUB

*Gargantuan Celestial, Neutral Good.* **Challenge 11** (7200 XP). **Zone:** Resonance Fields.

Radiance clings to Kenku the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Kenku* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Mimic-Crow (Aethel unaffiliated)* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kraken — STUB

*Huge Celestial, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Choir Sanctum.

Kraken claims descent from higher harmony, though Choir Sanctum has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Riding Horse — STUB

*Huge Celestial, Neutral Good.* **Challenge 11** (7200 XP). **Zone:** Radiant Isles.

Radiance clings to Riding Horse the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Riding Horse* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tlincalli — STUB

*Huge Celestial, Lawful Good.* **Challenge 11** (7200 XP). **Zone:** Resonance Fields.

Radiance clings to Tlincalli the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Mage — STUB

*Huge Celestial, Lawful Good.* **Challenge 11** (7200 XP). **Zone:** Radiant Isles.

Umbrin Mage carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Umbrin Mage* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Celestial**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Awakened Shrub — STUB

*Huge Celestial, Neutral Good.* **Challenge 12** (8400 XP). **Zone:** Resonance Fields.

Awakened Shrub claims descent from higher harmony, though Resonance Fields has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Awakened Shrub* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Berbalang — STUB

*Huge Celestial, Lawful Good.* **Challenge 12** (8400 XP). **Zone:** Radiant Isles.

Berbalang claims descent from higher harmony, though Radiant Isles has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Berbalang* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deathlock — STUB

*Large Celestial, Lawful Good.* **Challenge 12** (8400 XP). **Zone:** Radiant Isles.

Radiance clings to Deathlock the way guilt clings to a debt not yet called in. It judges before it helps, and its judgment is not aligned with player convenience. Use it sparingly — Celestial pressure works best as leverage, not loot.

> **STUB — Director must re-skin.** The name *Deathlock* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gibbering Mouther — STUB

*Huge Celestial, Chaotic Good.* **Challenge 12** (8400 XP). **Zone:** Choir Sanctum.

Gibbering Mouther carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Gibbering Mouther* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nightwalker — STUB

*Huge Celestial, Chaotic Good.* **Challenge 12** (8400 XP). **Zone:** Resonance Fields.

Nightwalker claims descent from higher harmony, though Resonance Fields has bent that claim into something stranger. Its aid is never free — Pact politics stain even the most radiant motive down here. Play it as a conditional ally at best — a Director's tool for making mercy expensive.

> **STUB — Director must re-skin.** The name *Nightwalker* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Elder Brain — STUB

*Gargantuan Celestial, Chaotic Good.* **Challenge 21** (33000 XP). **Zone:** Resonance Fields.

Elder Brain carries the manner of a messenger who has forgotten, or refuses to say, who sent it. It remembers oaths precisely and holds Expeditions to the letter, not the spirit. If it falls, something above the Decennium notices; decide in advance what that costs later.

> **STUB — Director must re-skin.** The name *Elder Brain* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Celestial** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Constructs

Constructs are Aethel's oldest engineering wearing whatever purpose has outlived its original maker. In the Anvil tiers especially, a Construct is as often evidence as it is a threat — a labor unit, a weapon left running past its intended service life, a guardian obeying an order its makers would now regret giving. **Player knowledge** is limited to function: what it guards, how it moves, whether it responds to command tokens or seals. **Director knowledge** should treat every Construct encounter as a small mystery — who built it, why, and what happened to them — worth more to a Research team than the Construct's salvage value. Disabling and questioning a Construct (however it "answers") is consistently more interesting than simply destroying it.

*Indexed creatures of this family: **44**.*

### Remorhaz — STUB

*Tiny Construct, True Neutral.* **Challenge 0** (10 XP). **Zone:** Aethel Deserts.

Somewhere upstream of Aethel Deserts, someone had a use for Remorhaz; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Remorhaz* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rothe — STUB

*Small Construct, Lawful Evil.* **Challenge 0** (10 XP). **Zone:** Veiled Expanse.

Somewhere upstream of Veiled Expanse, someone had a use for Rothe; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Rothe* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shadow Mastiff

*Tiny Construct, Chaotic Good.* **Challenge 1/8** (25 XP). **Zone:** Aethel Lakes.

Nothing about Shadow Mastiff improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tarrasque — STUB

*Tiny Construct, Neutral Evil.* **Challenge 1/8** (25 XP). **Zone:** Aethel Deserts.

Nothing about Tarrasque improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Tarrasque* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Worldbreaker* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Animated Armor

*Tiny Construct, Lawful Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Rivers.

Animated Armor is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lizard King/Queen — STUB

*Small Construct, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Veiled Expanse.

Somewhere upstream of Veiled Expanse, someone had a use for Lizard King/Queen; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Lizard King/Queen* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quadrone — STUB

*Small Construct, Chaotic Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Tundra.

Quadrone is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Quadrone rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Solar — STUB

*Small Construct, Chaotic Evil.* **Challenge 1/4** (50 XP). **Zone:** Radiant Isles.

Solar is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Solar* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Black Abishai — STUB

*Small Construct, Lawful Evil.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lakes.

Nothing about Black Abishai improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — stock alias, Director must re-skin.** Part of the Abishai (color devil) family; proposed: *Pact Devil*. Replace with Pact Devil, colored by Chaos-Realm court per Continuity C.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dimetrodon — STUB

*Small Construct, Neutral Good.* **Challenge 1/2** (100 XP). **Zone:** Yieldheart.

Dimetrodon is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Dimetrodon* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Draft Horse — STUB

*Small Construct, Lawful Good.* **Challenge 1/2** (100 XP). **Zone:** Shardpools.

Somewhere upstream of Shardpools, someone had a use for Draft Horse; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Draft Horse* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Clay Golem

*Small Construct, Lawful Good.* **Challenge 1** (200 XP). **Zone:** Aethel Lowlands.

Somewhere upstream of Aethel Lowlands, someone had a use for Clay Golem; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d8+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spectator

*Large Construct, Lawful Good.* **Challenge 1** (200 XP). **Zone:** Aethel Swamps.

Spectator is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin House Captain — STUB

*Medium Construct, Lawful Neutral.* **Challenge 2** (450 XP). **Zone:** Veiled Expanse.

Umbrin House Captain was built, not born, and Veiled Expanse still remembers who built it even if the party does not. Damage does not deter it the way pain deters living things; only disabling function stops it. Use it as evidence: what it guards, obeys, or was built for tells an Expedition more than its stat line.

> **STUB — Director must re-skin.** The name *Umbrin House Captain* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Construct**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Scion — STUB

*Medium Construct, True Neutral.* **Challenge 4** (1100 XP). **Zone:** Yieldheart.

Somewhere upstream of Yieldheart, someone had a use for Deep Scion; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Deep Scion* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*
- **Pressure Wave** (Recharge 5-6) — 4d6 bludgeoning, 20-ft. radius — constitution save DC 14 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nalfeshnee — STUB

*Medium Construct, Neutral Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Nalfeshnee was built, not born, and Aethel Lowlands still remembers who built it even if the party does not. Damage does not deter it the way pain deters living things; only disabling function stops it. Use it as evidence: what it guards, obeys, or was built for tells an Expedition more than its stat line.

> **STUB — Director must re-skin.** The name *Nalfeshnee* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Nalfeshnee rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Twig Blight — STUB

*Large Construct, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Mountains.

Somewhere upstream of Aethel Mountains, someone had a use for Twig Blight; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Twig Blight* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wood Woad — STUB

*Large Construct, Neutral Evil.* **Challenge 6** (2300 XP). **Zone:** Bastion of Flame.

Wood Woad is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Plesiosaurus — STUB

*Large Construct, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Planar Crossroads.

Nothing about Plesiosaurus improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Plesiosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Helmed Horror — STUB

*Huge Construct, Lawful Good.* **Challenge 11** (7200 XP). **Zone:** Aethel Swamps.

Somewhere upstream of Aethel Swamps, someone had a use for Helmed Horror; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vrock — STUB

*Gargantuan Construct, Unaligned.* **Challenge 13** (10000 XP). **Zone:** Yieldheart.

Vrock is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Vrock* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Vrock rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Commoner — STUB

*Huge Construct, Lawful Neutral.* **Challenge 16** (15000 XP). **Zone:** Shardpools.

Commoner is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Commoner* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +9 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quetzalcoatlus — STUB

*Huge Construct, Lawful Evil.* **Challenge 17** (18000 XP). **Zone:** Aethel Forests.

Quetzalcoatlus is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Quetzalcoatlus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deathlock Mastermind — STUB

*Gargantuan Construct, True Neutral.* **Challenge 18** (20000 XP). **Zone:** Aethel Tundra.

Somewhere upstream of Aethel Tundra, someone had a use for Deathlock Mastermind; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Deathlock Mastermind* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hydroloth — STUB

*Gargantuan Construct, Lawful Evil.* **Challenge 18** (20000 XP). **Zone:** Aethel Forests.

Somewhere upstream of Aethel Forests, someone had a use for Hydroloth; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Hydroloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Hydroloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gargoyle — STUB

*Huge Construct, Lawful Neutral.* **Challenge 19** (22000 XP). **Zone:** Aethel Forests.

Nothing about Gargoyle improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Gargoyle* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Trapper — STUB

*Gargantuan Construct, Neutral Good.* **Challenge 19** (22000 XP). **Zone:** Aethel Mountains.

Somewhere upstream of Aethel Mountains, someone had a use for Trapper; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Trapper* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d12+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll Hunter — STUB

*Gargantuan Construct, Lawful Neutral.* **Challenge 20** (25000 XP). **Zone:** Aethel Tundra.

Somewhere upstream of Aethel Tundra, someone had a use for Gnoll Hunter; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Gnoll Hunter* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quaggoth — STUB

*Huge Construct, Chaotic Good.* **Challenge 20** (25000 XP). **Zone:** Aethel Lakes.

Somewhere upstream of Aethel Lakes, someone had a use for Quaggoth; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Quaggoth* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +11 to hit — 3d12+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vegepygmy — STUB

*Gargantuan Construct, Unaligned.* **Challenge 21** (33000 XP). **Zone:** Veiled Expanse.

Nothing about Vegepygmy improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Vegepygmy* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Jackal — STUB

*Huge Construct, Lawful Evil.* **Challenge 22** (41000 XP). **Zone:** Aethel Mountains.

Somewhere upstream of Aethel Mountains, someone had a use for Jackal; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Jackal* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stone Golem — STUB

*Gargantuan Construct, Neutral Evil.* **Challenge 23** (50000 XP). **Zone:** Aethel Swamps.

Stone Golem is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Baboon — STUB

*Gargantuan Construct, Neutral Good.* **Challenge 24** (62000 XP). **Zone:** Aethel Swamps.

Nothing about Baboon improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Baboon* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nagpa — STUB

*Gargantuan Construct, Neutral Evil.* **Challenge 25** (75000 XP). **Zone:** Aethel Lowlands.

Nothing about Nagpa improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Nagpa* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 397 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +12 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flesh Golem — STUB

*Gargantuan Construct, Chaotic Evil.* **Challenge 26** (90000 XP). **Zone:** Null Zones.

Flesh Golem was built, not born, and Null Zones still remembers who built it even if the party does not. Damage does not deter it the way pain deters living things; only disabling function stops it. Use it as evidence: what it guards, obeys, or was built for tells an Expedition more than its stat line.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Succubus — STUB

*Gargantuan Construct, Neutral Evil.* **Challenge 26** (90000 XP). **Zone:** Aethel Lakes.

Succubus is older engineering wearing a newer purpose, patched together by whoever last needed it to move. Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around. It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.

> **STUB — Director must re-skin.** The name *Succubus* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tridrone — STUB

*Gargantuan Construct, Chaotic Neutral.* **Challenge 26** (90000 XP). **Zone:** Bastion of Flame.

Somewhere upstream of Bastion of Flame, someone had a use for Tridrone; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Tridrone rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Elite Warrior — STUB

*Gargantuan Construct, Unaligned.* **Challenge 26** (90000 XP). **Zone:** Boundless Void.

Somewhere upstream of Boundless Void, someone had a use for Umbrin Elite Warrior; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Umbrin Elite Warrior* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Construct**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Corpse Flower — STUB

*Gargantuan Construct, Lawful Evil.* **Challenge 27** (105000 XP). **Zone:** Resonance Fields.

Nothing about Corpse Flower improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Corpse Flower* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bheur Hag — STUB

*Gargantuan Construct, Neutral Good.* **Challenge 28** (120000 XP). **Zone:** Veiled Expanse.

Nothing about Bheur Hag improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Bheur Hag* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 442 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Barghest — STUB

*Gargantuan Construct, Lawful Good.* **Challenge 29** (135000 XP). **Zone:** Aethel Swamps.

Nothing about Barghest improvises — it executes, which is its own kind of danger. It recognizes authority by token, seal, or command phrase — not by argument. Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.

> **STUB — Director must re-skin.** The name *Barghest* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 457 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +14 to hit — 5d10+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Soul Monger — STUB

*Gargantuan Construct, True Neutral.* **Challenge 29** (135000 XP). **Zone:** Aethel Lakes.

Somewhere upstream of Aethel Lakes, someone had a use for Soul Monger; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** The name *Soul Monger* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 457 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +14 to hit — 5d10+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Iron Golem — STUB

*Gargantuan Construct, True Neutral.* **Challenge 30** (155000 XP). **Zone:** Choir Sanctum.

Somewhere upstream of Choir Sanctum, someone had a use for Iron Golem; the use outlived the reason. It follows its last standing order literally, including orders its makers would now regret. A captured command phrase or control core is often better loot than its salvage value.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 23 · **Hit Points** 472 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +14 to hit — 5d10+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lizard — STUB

*Gargantuan Construct, Neutral Evil.* **Challenge 30** (155000 XP). **Zone:** Aethel Tundra.

Lizard was built, not born, and Aethel Tundra still remembers who built it even if the party does not. Damage does not deter it the way pain deters living things; only disabling function stops it. Use it as evidence: what it guards, obeys, or was built for tells an Expedition more than its stat line.

> **STUB — Director must re-skin.** The name *Lizard* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Construct** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 23 · **Hit Points** 472 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +14 to hit — 5d10+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Dragons

Dragons are Aethel's apex predators of ambition, and the Decennium has never managed to fully domesticate that ambition into something predictable. A Dragon's hoard is a symptom of its nature, not the nature itself — pride, territory, and a long memory for anyone who tries to lie to it matter more than the gold ever does. **Player knowledge** treats a Dragon sighting as a campaign event: rumor, omen, and reputation travel ahead of the creature itself. **Director knowledge** should plan the hoard's aftermath before the fight — surface factions will contest a Dragon's leftover wealth for sessions afterward, and a Dragon fight run as a single floor's random encounter wastes the type's entire narrative weight. Reserve genuine Dragon encounters for moments that deserve a full session of build-up.

*Indexed creatures of this family: **84**.*

### Young Faerie Dragon

*Tiny Dragon, Lawful Good.* **Challenge 0** (10 XP). **Zone:** Aethel Mountains.

Young Faerie Dragon treats Aethel Mountains as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Blue Dragon

*Tiny Dragon, Neutral Good.* **Challenge 1/8** (25 XP). **Zone:** Spiral Nexus.

Ambition made scales on Young Blue Dragon; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Bronze Dragon

*Tiny Dragon, Chaotic Good.* **Challenge 1/8** (25 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Young Bronze Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Gold Dragon

*Tiny Dragon, Lawful Good.* **Challenge 1/8** (25 XP). **Zone:** Bastion of Flame.

Young Gold Dragon does not compete for Bastion of Flame — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Green Dragon

*Tiny Dragon, True Neutral.* **Challenge 1/8** (25 XP). **Zone:** Spiral Nexus.

Young Green Dragon treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Kruthik — STUB

*Tiny Dragon, True Neutral.* **Challenge 1/8** (25 XP). **Zone:** Spiral Nexus.

Young Kruthik treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Young Kruthik* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Red Dragon

*Tiny Dragon, Chaotic Evil.* **Challenge 1/8** (25 XP). **Zone:** Bastion of Flame.

Young Red Dragon treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Black Dragon

*Small Dragon, Chaotic Good.* **Challenge 1/4** (50 XP). **Zone:** Veiled Expanse.

Young Black Dragon does not compete for Veiled Expanse — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Brass Dragon

*Small Dragon, Chaotic Evil.* **Challenge 1/4** (50 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Young Brass Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Silver Dragon

*Small Dragon, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Aethel Caves.

Young Silver Dragon does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Red Shadow Dragon — STUB

*Medium Dragon, Neutral Evil.* **Challenge 1** (200 XP). **Zone:** Bastion of Flame.

Young Red Shadow Dragon does not compete for Bastion of Flame — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Young Red Shadow Dragon* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young White Dragon

*Large Dragon, Lawful Evil.* **Challenge 1** (200 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Young White Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Young Copper Dragon

*Large Dragon, Neutral Evil.* **Challenge 2** (450 XP). **Zone:** Aethel Caves.

Ambition made scales on Young Copper Dragon; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Blue Dragon Wyrmling

*Huge Dragon, Neutral Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Aethel Mountains is quieter than it should be wherever Blue Dragon Wyrmling has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Green Dragon Wyrmling

*Large Dragon, Unaligned.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Ambition made scales on Green Dragon Wyrmling; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hungry Sorrowsworn — STUB

*Huge Dragon, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Hungry Sorrowsworn treats Aethel Mountains as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — stock alias, Director must re-skin.** Part of the Sorrowsworn family; proposed: *Hungry Grief-Bound*. Invented emotion-fey terminology; safe to rename without losing concept.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Leviathan

*Large Dragon, Lawful Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Aethel Mountains is quieter than it should be wherever Leviathan has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nabassu — STUB

*Huge Dragon, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Nabassu has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Nabassu* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Nabassu rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Oinoloth — STUB

*Huge Dragon, Chaotic Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Oinoloth treats Aethel Mountains as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Oinoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Oinoloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wyvern

*Large Dragon, Lawful Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Caves.

Wyvern does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Boggle — STUB

*Huge Dragon, Lawful Neutral.* **Challenge 8** (3900 XP). **Zone:** Aethel Caves.

Boggle does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Boggle* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gold Dragon Wyrmling

*Large Dragon, True Neutral.* **Challenge 8** (3900 XP). **Zone:** Bastion of Flame.

Gold Dragon Wyrmling treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kruthik Hive Lord — STUB

*Large Dragon, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Spiral Nexus.

Kruthik Hive Lord does not compete for Spiral Nexus — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Kruthik Hive Lord* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Red Dragon Wyrmling

*Huge Dragon, True Neutral.* **Challenge 8** (3900 XP). **Zone:** Bastion of Flame.

Ambition made scales on Red Dragon Wyrmling; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Arcanaloth — STUB

*Huge Dragon, Lawful Evil.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Arcanaloth does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Arcanaloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Arcanaloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bronze Scout — STUB

*Large Dragon, Chaotic Evil.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Bronze Scout treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Bronze Scout* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cadaver Collector — STUB

*Huge Dragon, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Ambition made scales on Cadaver Collector; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> **STUB — Director must re-skin.** The name *Cadaver Collector* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Copper Dragon Wyrmling

*Large Dragon, Chaotic Neutral.* **Challenge 9** (5000 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Copper Dragon Wyrmling has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deer — STUB

*Large Dragon, Chaotic Neutral.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Deer has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Deer* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Depth Toad — STUB

*Large Dragon, Lawful Good.* **Challenge 9** (5000 XP). **Zone:** Spiral Nexus.

Depth Toad treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Depth Toad* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Dragon**) was randomized independently of the Depth Toad concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flind — STUB

*Large Dragon, Chaotic Good.* **Challenge 9** (5000 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Flind has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Flind* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gray Render — STUB

*Large Dragon, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Spiral Nexus.

Gray Render treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Gray Render* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Half-Red Dragon Veteran — STUB

*Large Dragon, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

Half-Red Dragon Veteran treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Half-Red Dragon Veteran* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kobold Dragonshield — STUB

*Huge Dragon, Chaotic Evil.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Kobold Dragonshield does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Kobold Dragonshield* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Silver Dragon Wyrmling

*Large Dragon, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Silver Dragon Wyrmling has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wererat

*Large Dragon, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Aethel Caves.

Wererat treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Blue Dragon

*Large Dragon, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Adult Blue Dragon treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Copper Dragon

*Large Dragon, Neutral Good.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Adult Copper Dragon does not compete for Spiral Nexus — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Gold Dragon

*Huge Dragon, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Bastion of Flame.

Bastion of Flame is quieter than it should be wherever Adult Gold Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Silver Dragon

*Large Dragon, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Adult Silver Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ape — STUB

*Large Dragon, Unaligned.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Ape does not compete for Spiral Nexus — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Ape* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Doppelganger — STUB

*Large Dragon, Neutral Good.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Ambition made scales on Doppelganger; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> **STUB — Director must re-skin.** The name *Doppelganger* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dragon Turtle

*Large Dragon, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Dragon Turtle treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Guard Drake

*Huge Dragon, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Guard Drake has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Meazel — STUB

*Large Dragon, Lawful Good.* **Challenge 10** (5900 XP). **Zone:** Aethel Mountains.

Aethel Mountains is quieter than it should be wherever Meazel has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Meazel* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pentadrone — STUB

*Huge Dragon, True Neutral.* **Challenge 10** (5900 XP). **Zone:** Aethel Mountains.

Pentadrone treats Aethel Mountains as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Pentadrone* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Pentadrone rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pseudodragon

*Large Dragon, Unaligned.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Pseudodragon treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Redcap — STUB

*Huge Dragon, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Bastion of Flame.

Redcap treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Redcap* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stirge — STUB

*Large Dragon, Lawful Evil.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Ambition made scales on Stirge; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> **STUB — Director must re-skin.** The name *Stirge* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Insects

*Large Dragon, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Aethel Caves.

Swarm of Insects treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Thri-kreen — STUB

*Large Dragon, Neutral Good.* **Challenge 10** (5900 XP). **Zone:** Aethel Caves.

Thri-kreen does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Thri-kreen* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Chitin-Strider* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Yagnoloth — STUB

*Large Dragon, Neutral Good.* **Challenge 10** (5900 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Yagnoloth has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Yagnoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Yagnoloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Oblex — STUB

*Huge Dragon, Lawful Neutral.* **Challenge 11** (7200 XP). **Zone:** Aethel Caves.

Adult Oblex does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Adult Oblex* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Red Dragon

*Large Dragon, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Bastion of Flame.

Adult Red Dragon treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bandit Captain — STUB

*Large Dragon, Chaotic Neutral.* **Challenge 11** (7200 XP). **Zone:** Aethel Mountains.

Bandit Captain does not compete for Aethel Mountains — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Bandit Captain* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Black Dragon Wyrmling

*Large Dragon, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Veiled Expanse.

Veiled Expanse is quieter than it should be wherever Black Dragon Wyrmling has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Night Hag — STUB

*Huge Dragon, Chaotic Good.* **Challenge 11** (7200 XP). **Zone:** Aethel Caves.

Night Hag does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Night Hag* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Oblex Spawn — STUB

*Huge Dragon, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Spiral Nexus.

Ambition made scales on Oblex Spawn; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> **STUB — Director must re-skin.** The name *Oblex Spawn* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orthon — STUB

*Huge Dragon, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Orthon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> **STUB — Director must re-skin.** The name *Orthon* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Roper — STUB

*Huge Dragon, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Aethel Mountains.

Ambition made scales on Roper; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> **STUB — Director must re-skin.** The name *Roper* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Summer Eladrin — STUB

*Huge Dragon, True Neutral.* **Challenge 11** (7200 XP). **Zone:** Aethel Caves.

Summer Eladrin does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Summer Eladrin* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Eladrin (season) family; proposed: *Summer Season-Bound*. Setting-specific fey-noble term tied to an external calendar cosmology.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### White Dragon Wyrmling

*Huge Dragon, Lawful Neutral.* **Challenge 11** (7200 XP). **Zone:** Spiral Nexus.

Ambition made scales on White Dragon Wyrmling; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Brass Dragon Wyrmling

*Huge Dragon, Lawful Good.* **Challenge 12** (8400 XP). **Zone:** Spiral Nexus.

Brass Dragon Wyrmling treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bronze Dragon Wyrmling

*Large Dragon, Lawful Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Bronze Dragon Wyrmling has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Efreeti — STUB

*Large Dragon, True Neutral.* **Challenge 12** (8400 XP). **Zone:** Spiral Nexus.

Efreeti does not compete for Spiral Nexus — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> **STUB — Director must re-skin.** The name *Efreeti* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Goristro — STUB

*Large Dragon, Neutral Good.* **Challenge 12** (8400 XP). **Zone:** Spiral Nexus.

Goristro treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Goristro* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Goristro rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Green Abishai — STUB

*Huge Dragon, True Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Caves.

Green Abishai treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — stock alias, Director must re-skin.** Part of the Abishai (color devil) family; proposed: *Pact Devil*. Replace with Pact Devil, colored by Chaos-Realm court per Continuity C.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vampiric Mist — STUB

*Huge Dragon, Chaotic Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Caves.

Vampiric Mist treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> **STUB — Director must re-skin.** The name *Vampiric Mist* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Dragon** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Brass Dragon

*Huge Dragon, Unaligned.* **Challenge 13** (10000 XP). **Zone:** Spiral Nexus.

Adult Brass Dragon treats Spiral Nexus as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Faerie Dragon

*Large Dragon, Lawful Neutral.* **Challenge 13** (10000 XP). **Zone:** Aethel Mountains.

Aethel Mountains is quieter than it should be wherever Adult Faerie Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Green Dragon

*Huge Dragon, Neutral Evil.* **Challenge 13** (10000 XP). **Zone:** Aethel Caves.

Adult Green Dragon does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Black Dragon

*Large Dragon, Neutral Good.* **Challenge 14** (11500 XP). **Zone:** Veiled Expanse.

Veiled Expanse is quieter than it should be wherever Adult Black Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult White Dragon

*Huge Dragon, Chaotic Neutral.* **Challenge 15** (13000 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Adult White Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Bronze Dragon

*Huge Dragon, Lawful Neutral.* **Challenge 16** (15000 XP). **Zone:** Spiral Nexus.

Spiral Nexus is quieter than it should be wherever Adult Bronze Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Brass Dragon

*Gargantuan Dragon, Lawful Good.* **Challenge 16** (15000 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Ancient Brass Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient White Dragon

*Gargantuan Dragon, Chaotic Evil.* **Challenge 17** (18000 XP). **Zone:** Aethel Mountains.

Ancient White Dragon does not compete for Aethel Mountains — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Copper Dragon

*Gargantuan Dragon, Unaligned.* **Challenge 19** (22000 XP). **Zone:** Aethel Caves.

Ambition made scales on Ancient Copper Dragon; the hoard is a symptom, not the point. It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it. Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Bronze Dragon

*Gargantuan Dragon, Lawful Good.* **Challenge 20** (25000 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Ancient Bronze Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Repulsion Breath** (Recharge 5-6) — 9d10 lightning, 20-ft. radius — dexterity save DC 21 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Red Dragon

*Gargantuan Dragon, Lawful Neutral.* **Challenge 20** (25000 XP). **Zone:** Bastion of Flame.

Ancient Red Dragon treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Green Dragon

*Huge Dragon, Lawful Neutral.* **Challenge 21** (33000 XP). **Zone:** Aethel Caves.

Aethel Caves is quieter than it should be wherever Ancient Green Dragon has decided to be understood as law. Pride is a lever here — flattery, challenge, and bargains land where steel does not. A Director should decide in advance what the hoard buys and who else wants it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +11 to hit — 3d12+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Blue Dragon

*Gargantuan Dragon, Neutral Good.* **Challenge 22** (41000 XP). **Zone:** Aethel Caves.

Ancient Blue Dragon treats Aethel Caves as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Silver Dragon

*Gargantuan Dragon, Chaotic Good.* **Challenge 22** (41000 XP). **Zone:** Aethel Caves.

Ancient Silver Dragon does not compete for Aethel Caves — it simply outlasts anyone who tries to. It delegates lesser threats to guard the approach and saves itself for parties worth its time. Treat it as a campaign event, not a floor's random encounter.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Black Dragon

*Gargantuan Dragon, Neutral Good.* **Challenge 23** (50000 XP). **Zone:** Veiled Expanse.

Ancient Black Dragon treats Veiled Expanse as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ancient Gold Dragon

*Gargantuan Dragon, Lawful Good.* **Challenge 23** (50000 XP). **Zone:** Bastion of Flame.

Ancient Gold Dragon treats Bastion of Flame as a claim, not a home, and enforces the distinction personally. Its territory is marked in ways only apparent after an Expedition has already crossed the line. Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Elementals

Elementals are what happens when the Spiral's folds concentrate raw matter and energy hard enough that it starts behaving like a creature. They do not evolve so much as precipitate, and most have no memory of anything before the moment they formed. **Player knowledge** is almost entirely about the terrain that produced them — heat, current, stone, wind — and about who, if anyone, bound the specific Elemental in front of them into service. **Director knowledge** should treat terrain as half of every Elemental encounter: the room is the creature's extended body, and a smothered, quenched, or grounded Elemental is a puzzle worth rewarding, not a stalemate to grind through. Ask whether a given Elemental is a natural seam or a bound servant before deciding what its "defeat" actually means.

*Indexed creatures of this family: **57**.*

### Astral Reaver War-Captain — STUB

*Tiny Elemental, Chaotic Neutral.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Astral Reaver War-Captain did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Astral Reaver War-Captain* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Elemental**) was randomized independently of the Astral Reaver concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Choker — STUB

*Small Elemental, Chaotic Evil.* **Challenge 0** (10 XP). **Zone:** Shardpools.

Where the Spiral folds hardest over Shardpools, raw element condenses into something like Choker. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Choker* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Derro Savant — STUB

*Small Elemental, Lawful Evil.* **Challenge 1/4** (50 XP). **Zone:** Resonance Fields.

Derro Savant is Resonance Fields's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Derro Savant* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nightmare — STUB

*Tiny Elemental, Chaotic Evil.* **Challenge 1/4** (50 XP). **Zone:** Boundless Void.

Nightmare is Boundless Void's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Nightmare* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Harpy — STUB

*Small Elemental, True Neutral.* **Challenge 1/2** (100 XP). **Zone:** Radiant Isles.

Where the Spiral folds hardest over Radiant Isles, raw element condenses into something like Harpy. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Harpy* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mule — STUB

*Medium Elemental, Chaotic Evil.* **Challenge 1/2** (100 XP). **Zone:** Boundless Void.

Mule is Boundless Void's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Mule* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Purple Worm — STUB

*Small Elemental, Chaotic Good.* **Challenge 1/2** (100 XP). **Zone:** Aethel Tundra.

Purple Worm did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Purple Worm* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Water Elemental Myrmidon

*Small Elemental, Lawful Evil.* **Challenge 1** (200 XP). **Zone:** Aethel Lakes.

The terrain of Aethel Lakes is not a backdrop to Water Elemental Myrmidon — it is Water Elemental Myrmidon's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Neothelid — STUB

*Large Elemental, Chaotic Neutral.* **Challenge 2** (450 XP). **Zone:** Yieldheart.

Where the Spiral folds hardest over Yieldheart, raw element condenses into something like Neothelid. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Neothelid* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Spiral Worm* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pegasus — STUB

*Medium Elemental, Lawful Evil.* **Challenge 2** (450 XP). **Zone:** Aethel Lakes.

The terrain of Aethel Lakes is not a backdrop to Pegasus — it is Pegasus's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Pegasus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bullywug — STUB

*Medium Elemental, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Aethel Rivers.

Bullywug is Aethel Rivers's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Bullywug* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Bogkin* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stench Kow — STUB

*Medium Elemental, Lawful Good.* **Challenge 3** (700 XP). **Zone:** Null Zones.

The terrain of Null Zones is not a backdrop to Stench Kow — it is Stench Kow's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Stench Kow* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Djinni

*Large Elemental, Neutral Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Deserts.

Djinni did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Earth Elemental Myrmidon

*Huge Elemental, Unaligned.* **Challenge 6** (2300 XP). **Zone:** Resonance Fields.

The terrain of Resonance Fields is not a backdrop to Earth Elemental Myrmidon — it is Earth Elemental Myrmidon's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grick — STUB

*Large Elemental, Chaotic Neutral.* **Challenge 6** (2300 XP). **Zone:** The Dungeon.

Where the Spiral folds hardest over The Dungeon, raw element condenses into something like Grick. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quaggoth Thonot — STUB

*Medium Elemental, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Jungles.

Quaggoth Thonot is Aethel Jungles's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Quaggoth Thonot* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fire Elemental Myrmidon — STUB

*Large Elemental, Neutral Good.* **Challenge 8** (3900 XP). **Zone:** Choir Sanctum.

Fire Elemental Myrmidon is Choir Sanctum's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Transmuter — STUB

*Large Elemental, Lawful Evil.* **Challenge 8** (3900 XP). **Zone:** Choir Sanctum.

Where the Spiral folds hardest over Choir Sanctum, raw element condenses into something like Transmuter. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Transmuter* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Air Elemental Myrmidon — STUB

*Large Elemental, Chaotic Evil.* **Challenge 9** (5000 XP). **Zone:** Aethel Jungles.

Air Elemental Myrmidon did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Gale Burst** (Recharge 5-6) — 5d10 lightning, 20-ft. radius — dexterity save DC 17 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Eidolon

*Medium Elemental, Lawful Evil.* **Challenge 9** (5000 XP). **Zone:** Resonance Fields.

Eidolon is Resonance Fields's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Water Elemental

*Large Elemental, Lawful Neutral.* **Challenge 9** (5000 XP). **Zone:** Aethel Mountains.

Water Elemental is Aethel Mountains's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lizardfolk — STUB

*Large Elemental, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Radiant Isles.

Lizardfolk did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Lizardfolk* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Xarog the Pactbound Furnace — STUB

*Large Elemental, Chaotic Evil.* **Challenge 10** (155000 XP). **Zone:** Boundless Void.

Xarog the Pactbound Furnace is Boundless Void's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — duplicate row.** A second entry, "Xarog, the Pactbound Furnace" (with comma), carries the Gate Guardian tag and bespoke companion-authored stats. This no-comma row is a stray Excel-sandbox leftover — see Gate Seal VII in Part II. Recommend deleting this row in the next Excel pass.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Inferno Pact** (Recharge 5-6) — 8d10 fire, 20-ft. radius — dexterity save DC 21 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Abominable Yeti — STUB

*Huge Elemental, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Null Zones.

Where the Spiral folds hardest over Null Zones, raw element condenses into something like Abominable Yeti. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Firenewt Warrior — STUB

*Gargantuan Elemental, Unaligned.* **Challenge 11** (7200 XP). **Zone:** Radiant Isles.

The terrain of Radiant Isles is not a backdrop to Firenewt Warrior — it is Firenewt Warrior's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Firenewt Warrior* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mouth of Grolantor — STUB

*Large Elemental, Lawful Evil.* **Challenge 13** (10000 XP). **Zone:** Spiral Nexus.

Mouth of Grolantor did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Mouth of Grolantor* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Star Spawn Larva Mage — STUB

*Huge Elemental, True Neutral.* **Challenge 13** (10000 XP). **Zone:** Null Zones.

The terrain of Null Zones is not a backdrop to Star Spawn Larva Mage — it is Star Spawn Larva Mage's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Star Spawn Larva Mage* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Star Spawn family; proposed: *Spiral Breach Larva Mage*. Owner-flagged: full Aethel rewrite or 'Spiral breach echo' ecology stub.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Velociraptor — STUB

*Huge Elemental, Chaotic Neutral.* **Challenge 13** (10000 XP). **Zone:** Aethel Lakes.

The terrain of Aethel Lakes is not a backdrop to Velociraptor — it is Velociraptor's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Velociraptor* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Water Weird — STUB

*Huge Elemental, True Neutral.* **Challenge 13** (10000 XP). **Zone:** Shardpools.

The terrain of Shardpools is not a backdrop to Water Weird — it is Water Weird's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Displacer Beast — STUB

*Gargantuan Elemental, Neutral Evil.* **Challenge 15** (13000 XP). **Zone:** Aethel Caves.

Where the Spiral folds hardest over Aethel Caves, raw element condenses into something like Displacer Beast. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Displacer Beast* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Refractor Panther* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lonely Sorrowsworn — STUB

*Huge Elemental, Lawful Neutral.* **Challenge 15** (13000 XP). **Zone:** The Dungeon.

Where the Spiral folds hardest over The Dungeon, raw element condenses into something like Lonely Sorrowsworn. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — stock alias, Director must re-skin.** Part of the Sorrowsworn family; proposed: *Lonely Grief-Bound*. Invented emotion-fey terminology; safe to rename without losing concept.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Abomination — STUB

*Gargantuan Elemental, Neutral Evil.* **Challenge 15** (13000 XP). **Zone:** Spiral Nexus.

The terrain of Spiral Nexus is not a backdrop to Serpent-Blood Abomination — it is Serpent-Blood Abomination's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Serpent-Blood Abomination* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Elemental**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fire Elemental — STUB

*Huge Elemental, Lawful Evil.* **Challenge 16** (15000 XP). **Zone:** Aethel Lakes.

Where the Spiral folds hardest over Aethel Lakes, raw element condenses into something like Fire Elemental. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +9 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nothic — STUB

*Gargantuan Elemental, Chaotic Evil.* **Challenge 16** (15000 XP). **Zone:** Planar Crossroads.

The terrain of Planar Crossroads is not a backdrop to Nothic — it is Nothic's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Nothic* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fire Giant Dreadnought — STUB

*Gargantuan Elemental, Lawful Neutral.* **Challenge 17** (18000 XP). **Zone:** Radiant Isles.

The terrain of Radiant Isles is not a backdrop to Fire Giant Dreadnought — it is Fire Giant Dreadnought's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Fire Giant Dreadnought* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Firenewt Warlock of Imix — STUB

*Gargantuan Elemental, Lawful Evil.* **Challenge 17** (18000 XP). **Zone:** Aethel Jungles.

Firenewt Warlock of Imix did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Firenewt Warlock of Imix* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Firenewt Warlock of the Ember Court* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Meenlock — STUB

*Huge Elemental, Lawful Evil.* **Challenge 18** (20000 XP). **Zone:** Spiral Nexus.

The terrain of Spiral Nexus is not a backdrop to Meenlock — it is Meenlock's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Meenlock* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warlock of the Great Old One — STUB

*Huge Elemental, Chaotic Neutral.* **Challenge 19** (22000 XP). **Zone:** Aethel Swamps.

Where the Spiral folds hardest over Aethel Swamps, raw element condenses into something like Warlock of the Great Old One. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Warlock of the Great Old One* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bulezau — STUB

*Gargantuan Elemental, Lawful Neutral.* **Challenge 20** (25000 XP). **Zone:** Planar Crossroads.

The terrain of Planar Crossroads is not a backdrop to Bulezau — it is Bulezau's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Bulezau* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Bulezau rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Archer — STUB

*Gargantuan Elemental, Lawful Neutral.* **Challenge 21** (33000 XP). **Zone:** The Dungeon.

The terrain of The Dungeon is not a backdrop to Archer — it is Archer's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Archer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gaze Tyrant Sovereign (in lair) — STUB

*Gargantuan Elemental, Neutral Evil.* **Challenge 21** (33000 XP). **Zone:** Aethel Mountains.

The terrain of Aethel Mountains is not a backdrop to Gaze Tyrant Sovereign (in lair) — it is Gaze Tyrant Sovereign (in lair)'s body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Gaze Tyrant Sovereign (in lair)* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Elemental**) was randomized independently of the Gaze Tyrant concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dolphin Delighter — STUB

*Gargantuan Elemental, Lawful Good.* **Challenge 22** (41000 XP). **Zone:** Veiled Expanse.

Where the Spiral folds hardest over Veiled Expanse, raw element condenses into something like Dolphin Delighter. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Fire Beetle — STUB

*Gargantuan Elemental, Lawful Evil.* **Challenge 22** (41000 XP). **Zone:** Radiant Isles.

Where the Spiral folds hardest over Radiant Isles, raw element condenses into something like Giant Fire Beetle. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Giant Fire Beetle* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Choldrith — STUB

*Gargantuan Elemental, Lawful Good.* **Challenge 23** (50000 XP). **Zone:** Null Zones.

Choldrith is Null Zones's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Choldrith* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Elder Oblex — STUB

*Gargantuan Elemental, Chaotic Neutral.* **Challenge 23** (50000 XP). **Zone:** Aethel Deserts.

Elder Oblex did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Elder Oblex* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Neogi Master — STUB

*Gargantuan Elemental, Lawful Neutral.* **Challenge 23** (50000 XP). **Zone:** Veiled Expanse.

Neogi Master did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Neogi Master* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Neogi family; proposed: *Void Broker Master*. Owner-flagged: 'Spiral breach echo' family or full rewrite.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Galeb Duhr

*Huge Elemental, Unaligned.* **Challenge 24** (62000 XP). **Zone:** Aethel Highlands.

The terrain of Aethel Highlands is not a backdrop to Galeb Duhr — it is Galeb Duhr's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lost Sorrowsworn — STUB

*Gargantuan Elemental, Chaotic Neutral.* **Challenge 24** (62000 XP). **Zone:** Aethel Tundra.

Lost Sorrowsworn did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — stock alias, Director must re-skin.** Part of the Sorrowsworn family; proposed: *Lost Grief-Bound*. Invented emotion-fey terminology; safe to rename without losing concept.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Morkoth (in lair) — STUB

*Gargantuan Elemental, Chaotic Evil.* **Challenge 24** (62000 XP). **Zone:** Aethel Rivers.

Morkoth (in lair) did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Morkoth (in lair)* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Mind Whisperer — STUB

*Gargantuan Elemental, Chaotic Good.* **Challenge 24** (62000 XP). **Zone:** Resonance Fields.

Serpent-Blood Mind Whisperer is Resonance Fields's weather made vindictive, a concentrated state of matter that decided to have opinions. Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it. Terrain is half the encounter — let the room do damage the creature's stat block cannot.

> **STUB — Director must re-skin.** The name *Serpent-Blood Mind Whisperer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Elemental**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Earth Elemental — STUB

*Gargantuan Elemental, Unaligned.* **Challenge 25** (75000 XP). **Zone:** Yieldheart.

Where the Spiral folds hardest over Yieldheart, raw element condenses into something like Earth Elemental. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 397 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hezrou — STUB

*Gargantuan Elemental, Unaligned.* **Challenge 26** (90000 XP). **Zone:** Aethel Swamps.

Where the Spiral folds hardest over Aethel Swamps, raw element condenses into something like Hezrou. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Hezrou* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Hezrou rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Air Elemental — STUB

*Gargantuan Elemental, Chaotic Good.* **Challenge 27** (105000 XP). **Zone:** Aethel Tundra.

Where the Spiral folds hardest over Aethel Tundra, raw element condenses into something like Air Elemental. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mammoth — STUB

*Huge Elemental, Lawful Evil.* **Challenge 27** (105000 XP). **Zone:** Aethel Caves.

Where the Spiral folds hardest over Aethel Caves, raw element condenses into something like Mammoth. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Mammoth* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flail Snail — STUB

*Gargantuan Elemental, Chaotic Good.* **Challenge 28** (120000 XP). **Zone:** Yieldheart.

Flail Snail did not evolve; it precipitated, and it remembers nothing before that moment. Silence and stillness are the two things it cannot fake; both give away its position. Its origin (natural seam vs. bound servant) should change what victory means here.

> **STUB — Director must re-skin.** The name *Flail Snail* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 442 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fire Giant — STUB

*Huge Elemental, Chaotic Neutral.* **Challenge 30** (155000 XP). **Zone:** Planar Crossroads.

Where the Spiral folds hardest over Planar Crossroads, raw element condenses into something like Fire Giant. It reads intent the way fire reads fuel: indifferently, and only as a resource. A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.

> **STUB — Director must re-skin.** The name *Fire Giant* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 23 · **Hit Points** 472 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +14 to hit — 5d10+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sea Hag — STUB

*Gargantuan Elemental, Unaligned.* **Challenge 30** (155000 XP). **Zone:** Aethel Deserts.

The terrain of Aethel Deserts is not a backdrop to Sea Hag — it is Sea Hag's body, extended. It fights by reshaping the room, not by outmaneuvering the people in it. Use it to force positioning choices before initiative is even rolled.

> **STUB — Director must re-skin.** The name *Sea Hag* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Elemental** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 23 · **Hit Points** 472 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +14 to hit — 5d10+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Fey

The Fey of Aethel answer to rules that only partially overlap with the rest of the Decennium's logic — hospitality, names, and debts are load-bearing structure here, not manners. **Player knowledge** should never take a Fey bargain at face value: every promise is kept with exact, punishing precision, which is a worse trap than an outright lie. **Director knowledge** treats combat as the failure state of a Fey encounter rather than its default outcome — a "defeated" Fey rarely ends the arrangement it represents, and the bargain it embodies often survives the fight that supposedly settled it. Use Fey encounters specifically to teach a table that not every problem this deep in the Decennium has a violent solution, and that the clever solution usually costs something just as real as blood.

*Indexed creatures of this family: **44**.*

### Nycaloth — STUB

*Tiny Fey, Lawful Good.* **Challenge 1/4** (50 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Nycaloth is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Nycaloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Nycaloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Quippers

*Small Fey, Unaligned.* **Challenge 1/4** (50 XP). **Zone:** Shardpools.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Swarm of Quippers is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ultroloth — STUB

*Small Fey, True Neutral.* **Challenge 1** (200 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Ultroloth is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Ultroloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Court Broker of the Hush* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rakshasa — STUB

*Medium Fey, Chaotic Neutral.* **Challenge 3** (700 XP). **Zone:** Aethel Forests.

Rakshasa answers to rules Aethel Forests only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Rakshasa* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Yeti — STUB

*Medium Fey, Unaligned.* **Challenge 4** (1100 XP). **Zone:** Aethel Forests.

Yeti treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Yeti* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Otyugh — STUB

*Huge Fey, True Neutral.* **Challenge 5** (1800 XP). **Zone:** Radiant Isles.

Otyugh answers to rules Radiant Isles only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Otyugh* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cat — STUB

*Large Fey, Neutral Good.* **Challenge 6** (2300 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Cat is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Cat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Raven — STUB

*Large Fey, Lawful Evil.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Raven is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Raven* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spring Eladrin — STUB

*Huge Fey, Neutral Evil.* **Challenge 6** (2300 XP). **Zone:** Shardpools.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Spring Eladrin is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — stock alias, Director must re-skin.** Part of the Eladrin (season) family; proposed: *Spring Season-Bound*. Setting-specific fey-noble term tied to an external calendar cosmology.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Molydeus — STUB

*Large Fey, Chaotic Good.* **Challenge 8** (3900 XP). **Zone:** Aethel Forests.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Molydeus is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Molydeus* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Molydeus rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bone Naga — STUB

*Huge Fey, Lawful Neutral.* **Challenge 9** (5000 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Bone Naga is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Bone Naga* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Nightmare Speaker — STUB

*Medium Fey, Neutral Good.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Serpent-Blood Nightmare Speaker treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Serpent-Blood Nightmare Speaker* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fey**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Slithering Tracker — STUB

*Large Fey, Chaotic Neutral.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Slithering Tracker is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Slithering Tracker* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Bats

*Medium Fey, Unaligned.* **Challenge 9** (5000 XP). **Zone:** Radiant Isles.

The closer Radiant Isles sits to an old fold, the more likely Swarm of Bats is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mezzoloth — STUB

*Huge Fey, Lawful Good.* **Challenge 11** (7200 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Mezzoloth is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Mezzoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Mezzoloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mud Mephit — STUB

*Huge Fey, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** Radiant Isles.

Mud Mephit answers to rules Radiant Isles only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Mud Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Duodrone — STUB

*Huge Fey, Neutral Good.* **Challenge 12** (8400 XP). **Zone:** Radiant Isles.

Duodrone answers to rules Radiant Isles only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Duodrone* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Duodrone rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Dreadnought — STUB

*Gargantuan Fey, Chaotic Neutral.* **Challenge 14** (11500 XP). **Zone:** Shardpools.

Astral Dreadnought treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Astral Dreadnought* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Berserker — STUB

*Large Fey, Lawful Evil.* **Challenge 14** (11500 XP). **Zone:** Shardpools.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Berserker is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Berserker* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Evoker — STUB

*Huge Fey, Unaligned.* **Challenge 14** (11500 XP). **Zone:** Shardpools.

Evoker answers to rules Shardpools only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Evoker* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d8+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gladiator — STUB

*Huge Fey, Unaligned.* **Challenge 14** (11500 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Gladiator is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Gladiator* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sprite — STUB

*Huge Fey, Lawful Evil.* **Challenge 14** (11500 XP). **Zone:** Radiant Isles.

The closer Radiant Isles sits to an old fold, the more likely Sprite is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Darkling Elder — STUB

*Huge Fey, Lawful Neutral.* **Challenge 15** (13000 XP). **Zone:** Radiant Isles.

The closer Radiant Isles sits to an old fold, the more likely Darkling Elder is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orog — STUB

*Huge Fey, Neutral Evil.* **Challenge 15** (13000 XP). **Zone:** Radiant Isles.

Orog treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Orog* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +9 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sea Horse — STUB

*Gargantuan Fey, Lawful Evil.* **Challenge 15** (13000 XP). **Zone:** Radiant Isles.

The closer Radiant Isles sits to an old fold, the more likely Sea Horse is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Sea Horse* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quickling

*Large Fey, Lawful Good.* **Challenge 19** (22000 XP). **Zone:** Shardpools.

Quickling answers to rules Shardpools only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Blink Dog — STUB

*Gargantuan Fey, Lawful Neutral.* **Challenge 20** (25000 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Blink Dog is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Champion — STUB

*Gargantuan Fey, Lawful Evil.* **Challenge 20** (25000 XP). **Zone:** Shardpools.

Champion treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Champion* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stone Defender — STUB

*Gargantuan Fey, Neutral Evil.* **Challenge 20** (25000 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Stone Defender is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Stone Defender* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Threxus, the Iron Spiral

*Large Fey, Chaotic Evil.* **Challenge 20** (25000 XP). **Zone:** Radiant Isles.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 20 · **Hit Points** 285 · **Speed** 30 ft., fly 60 ft.

**Abilities** STR 24 · DEX 16 · CON 20 · INT 16 · WIS 18 · CHA 14

**Skills** Athletics +13, Intimidation +8, Perception +10

**Senses** Darkvision 120 ft., passive Perception 20

**Languages** Common, Celestial

**Attacks**
- **Spiral Strike** (x3) — +11 to hit — 2d10+6 slashing
- **Iron Vortex** (Recharge 5-6) — 7d10 bludgeoning, 20-ft. radius — strength save DC 19 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Dryad — STUB

*Gargantuan Fey, Lawful Evil.* **Challenge 21** (33000 XP). **Zone:** Aethel Forests.

Dryad treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Minotaur — STUB

*Gargantuan Fey, Neutral Evil.* **Challenge 22** (41000 XP). **Zone:** Shardpools.

Minotaur treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Minotaur* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Star Spawn Seer — STUB

*Gargantuan Fey, Chaotic Neutral.* **Challenge 22** (41000 XP). **Zone:** Radiant Isles.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Star Spawn Seer is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Star Spawn Seer* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Star Spawn family; proposed: *Spiral Breach Seer*. Owner-flagged: full Aethel rewrite or 'Spiral breach echo' ecology stub.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +11 to hit — 4d10+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ghast — STUB

*Gargantuan Fey, Chaotic Evil.* **Challenge 23** (50000 XP). **Zone:** Aethel Forests.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Ghast is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Ghast* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +12 to hit — 4d10+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shoosuva — STUB

*Huge Fey, Chaotic Good.* **Challenge 24** (62000 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Shoosuva is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Shoosuva* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Shoosuva rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tanarukk — STUB

*Gargantuan Fey, Lawful Neutral.* **Challenge 24** (62000 XP). **Zone:** Shardpools.

Tanarukk answers to rules Shardpools only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Tanarukk* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +12 to hit — 4d10+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warlock of the Archfey — STUB

*Gargantuan Fey, Lawful Neutral.* **Challenge 25** (75000 XP). **Zone:** Aethel Forests.

Somewhere adjacent to this fold of the Weave, a bargain is already being kept — Warlock of the Archfey is enforcing it. It never lies outright and never tells the whole truth either; Directors should play every promise literally. Combat should be the failure state of a fey encounter, not the default one.

> **STUB — Director must re-skin.** The name *Warlock of the Archfey* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 397 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gaze Tyrant Sovereign — STUB

*Gargantuan Fey, Lawful Neutral.* **Challenge 26** (90000 XP). **Zone:** Shardpools.

Gaze Tyrant Sovereign treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Gaze Tyrant Sovereign* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fey**) was randomized independently of the Gaze Tyrant concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Intellect Devourer — STUB

*Gargantuan Fey, Lawful Good.* **Challenge 26** (90000 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Intellect Devourer is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Intellect Devourer* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Mind Leech* (not yet locked — see Naming & IP Reskin Ledger).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dhergoloth — STUB

*Gargantuan Fey, Chaotic Neutral.* **Challenge 27** (105000 XP). **Zone:** Shardpools.

Dhergoloth answers to rules Shardpools only partially shares with the rest of the Decennium. Bargains offered by it always cost more than they first appear to — that is the entire point of it. Let a bargain with it cost something narratively real — a debt, a name, a future favor.

> **STUB — Director must re-skin.** The name *Dhergoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Dhergoloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gor Vekk, Architect of Ends

*Large Fey, Neutral Evil.* **Challenge 29** (135000 XP). **Zone:** Radiant Isles.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 23 · **Hit Points** 400 · **Speed** 50 ft., fly 120 ft.

**Abilities** STR 28 · DEX 20 · CON 24 · INT 26 · WIS 22 · CHA 28

**Skills** Arcana +15, History +15, Insight +13, Perception +13

**Senses** Truesight 120 ft., passive Perception 23

**Languages** Deep Speech, telepathy 120 ft.

**Attacks**
- **Reality Sunder** (x3) — +14 to hit — 3d12+7 force
- **End Architecture** (Recharge 5-6) — 9d8 force, 20-ft. radius — intelligence save DC 22 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Pixie — STUB

*Gargantuan Fey, Chaotic Evil.* **Challenge 29** (135000 XP). **Zone:** Shardpools.

The closer Shardpools sits to an old fold, the more likely Pixie is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 457 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +14 to hit — 5d10+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Xvart Warlock of Raxivort — STUB

*Gargantuan Fey, Neutral Evil.* **Challenge 29** (135000 XP). **Zone:** Shardpools.

Xvart Warlock of Raxivort treats hospitality, names, and debts as load-bearing structure, not manners. Music, riddles, and names are weapons here as often as claws are. Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.

> **STUB — Director must re-skin.** The name *Xvart Warlock of Raxivort* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Xvart Warlock of the Nine-Legged Choir* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 457 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +14 to hit — 5d10+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Needle Blight — STUB

*Gargantuan Fey, Lawful Good.* **Challenge 30** (155000 XP). **Zone:** Aethel Forests.

The closer Aethel Forests sits to an old fold, the more likely Needle Blight is to have opinions about trespass. It keeps its word with exact, punishing precision, which is worse than breaking it. Use it to teach a table that not every problem in the Decennium has a violent solution.

> **STUB — Director must re-skin.** The name *Needle Blight* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Fey** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 23 · **Hit Points** 472 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +14 to hit — 5d10+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +14 to hit — 5d10+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Fiends

Fiends carry the Chaos-Realm's dissonance directly into Aethel, and the Pact's uneasy peace depends on that dissonance having somewhere to go. Most Fiends an Expedition meets did not arrive by accident — something summoned, bound, or invited them, and that original debt is very often still open when the party arrives. **Player knowledge** treats a Fiend as cruelty with a procedure behind it: not passion, just the most efficient route to whatever it wants. **Director knowledge** should always ask who summoned or bound the Fiend before treating the fight as the whole story — that answer is worth more than any loot table, and a Fiend's eternal war with its own kind can be turned into a one-time, expensive advantage for a clever Expedition. Victory here is always temporary; the dissonance a Fiend fed does not end when its body does.

*Indexed creatures of this family: **45**.*

### Astral Ascetic Enlightened — STUB

*Large Fiend, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Null Zones.

Wherever Null Zones keeps its oldest scars, Astral Ascetic Enlightened tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Astral Ascetic Enlightened* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fiend**) was randomized independently of the Astral Ascetic concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Awakened Tree — STUB

*Large Fiend, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

Wherever Bastion of Flame keeps its oldest scars, Awakened Tree tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Awakened Tree* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bone Devil

*Huge Fiend, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Boundless Void.

Bone Devil is Chaos-Realm lineage wearing Boundless Void like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hell Hound

*Large Fiend, Neutral Evil.* **Challenge 7** (2900 XP). **Zone:** Boundless Void.

Wherever Boundless Void keeps its oldest scars, Hell Hound tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hellfire Engine — STUB

*Medium Fiend, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Null Zones.

Hellfire Engine is Chaos-Realm lineage wearing Null Zones like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> **STUB — Director must re-skin.** The name *Hellfire Engine* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lesser Gaze Tyrant — STUB

*Large Fiend, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Boundless Void.

Wherever Boundless Void keeps its oldest scars, Lesser Gaze Tyrant tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Lesser Gaze Tyrant* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fiend**) was randomized independently of the Lesser Gaze Tyrant concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Neogi Hatchling — STUB

*Large Fiend, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Neogi Hatchling. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Neogi Hatchling* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Neogi family; proposed: *Void Broker Hatchling*. Owner-flagged: 'Spiral breach echo' family or full rewrite.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pit Fiend

*Medium Fiend, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Null Zones.

Pit Fiend is Chaos-Realm lineage wearing Null Zones like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Skull Lord — STUB

*Large Fiend, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Boundless Void.

Skull Lord is Chaos-Realm lineage wearing Boundless Void like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> **STUB — Director must re-skin.** The name *Skull Lord* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Will-o-wisp — STUB

*Large Fiend, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Will-o-wisp. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Will-o-wisp* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Amnizu

*Large Fiend, Lawful Evil.* **Challenge 8** (3900 XP). **Zone:** Null Zones.

Amnizu is Chaos-Realm lineage wearing Null Zones like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Hellfire Cone** (Recharge 5-6) — 5d8 fire, 20-ft. radius — dexterity save DC 16 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Barlgura

*Medium Fiend, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Bastion of Flame.

Barlgura is Chaos-Realm lineage wearing Bastion of Flame like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Couatl — STUB

*Medium Fiend, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Null Zones.

Couatl did not come to Null Zones by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Couatl* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ice Devil

*Huge Fiend, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Null Zones.

Wherever Null Zones keeps its oldest scars, Ice Devil tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lemure

*Large Fiend, Lawful Evil.* **Challenge 8** (3900 XP). **Zone:** Bastion of Flame.

Lemure did not come to Bastion of Flame by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Maw Demon

*Large Fiend, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Boundless Void.

Wherever Boundless Void keeps its oldest scars, Maw Demon tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Pureblood — STUB

*Huge Fiend, Lawful Evil.* **Challenge 8** (3900 XP). **Zone:** Boundless Void.

Wherever Boundless Void keeps its oldest scars, Serpent-Blood Pureblood tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Serpent-Blood Pureblood* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fiend**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spined Devil

*Medium Fiend, Chaotic Evil.* **Challenge 8** (3900 XP). **Zone:** Bastion of Flame.

Wherever Bastion of Flame keeps its oldest scars, Spined Devil tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 142 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Balhannoth — STUB

*Large Fiend, Lawful Evil.* **Challenge 9** (5000 XP). **Zone:** Null Zones.

Balhannoth did not come to Null Zones by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Balhannoth* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Horned Devil

*Large Fiend, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Boundless Void.

Horned Devil is Chaos-Realm lineage wearing Boundless Void like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lamia — STUB

*Medium Fiend, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Null Zones.

Wherever Null Zones keeps its oldest scars, Lamia tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Lamia* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Anathema — STUB

*Large Fiend, Chaotic Evil.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

Serpent-Blood Anathema did not come to Bastion of Flame by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Serpent-Blood Anathema* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fiend**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Steel Predator — STUB

*Large Fiend, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

Wherever Bastion of Flame keeps its oldest scars, Steel Predator tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Steel Predator* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d10+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stegosaurus — STUB

*Large Fiend, Lawful Evil.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

Stegosaurus did not come to Bastion of Flame by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Stegosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d10+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tortle — STUB

*Huge Fiend, Neutral Evil.* **Challenge 9** (5000 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Tortle. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Tortle* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Shellkin* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 16 · **Hit Points** 157 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d10+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d10+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Abyssal Wretch

*Large Fiend, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Abyssal Wretch. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Soul Scream** (Recharge 5-6) — 6d8 necrotic, 20-ft. radius — wisdom save DC 17 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Reaver Spellblade — STUB

*Large Fiend, Lawful Evil.* **Challenge 10** (5900 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Astral Reaver Spellblade. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Astral Reaver Spellblade* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Fiend**) was randomized independently of the Astral Reaver concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Barbed Devil

*Medium Fiend, Lawful Evil.* **Challenge 10** (5900 XP). **Zone:** Boundless Void.

Barbed Devil did not come to Boundless Void by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Chain Devil

*Large Fiend, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Null Zones.

Chain Devil is Chaos-Realm lineage wearing Null Zones like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dolphin — STUB

*Large Fiend, Lawful Evil.* **Challenge 10** (5900 XP). **Zone:** Boundless Void.

Dolphin did not come to Boundless Void by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Dolphin* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Female Steeder — STUB

*Large Fiend, Neutral Evil.* **Challenge 10** (5900 XP). **Zone:** Null Zones.

The dissonance the Pact requires has a face in Null Zones, and today it is Female Steeder. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Female Steeder* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Manes — STUB

*Large Fiend, Chaotic Evil.* **Challenge 10** (5900 XP). **Zone:** Boundless Void.

Manes did not come to Boundless Void by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Manes rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bearded Devil — STUB

*Huge Fiend, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Null Zones.

The dissonance the Pact requires has a face in Null Zones, and today it is Bearded Devil. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Girallon — STUB

*Huge Fiend, Neutral Evil.* **Challenge 11** (7200 XP). **Zone:** Null Zones.

Girallon did not come to Null Zones by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Girallon* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Invisible Stalker — STUB

*Huge Fiend, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Bastion of Flame.

Wherever Bastion of Flame keeps its oldest scars, Invisible Stalker tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> **STUB — Director must re-skin.** The name *Invisible Stalker* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nupperibo

*Huge Fiend, Lawful Evil.* **Challenge 11** (7200 XP). **Zone:** Boundless Void.

Wherever Boundless Void keeps its oldest scars, Nupperibo tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shadow Demon — STUB

*Huge Fiend, Chaotic Evil.* **Challenge 11** (7200 XP). **Zone:** Bastion of Flame.

The dissonance the Pact requires has a face in Bastion of Flame, and today it is Shadow Demon. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Archdruid — STUB

*Large Fiend, Chaotic Evil.* **Challenge 12** (8400 XP). **Zone:** Null Zones.

The dissonance the Pact requires has a face in Null Zones, and today it is Archdruid. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Archdruid* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 3d8+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Goat — STUB

*Gargantuan Fiend, Chaotic Evil.* **Challenge 12** (8400 XP). **Zone:** Boundless Void.

The dissonance the Pact requires has a face in Boundless Void, and today it is Goat. It bargains before it fights, fights before it flees, and never forgets which party did which to it. Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.

> **STUB — Director must re-skin.** The name *Goat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gynosphinx — STUB

*Huge Fiend, Neutral Evil.* **Challenge 12** (8400 XP). **Zone:** Null Zones.

Gynosphinx did not come to Null Zones by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Gynosphinx* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Narzugon

*Gargantuan Fiend, Neutral Evil.* **Challenge 12** (8400 XP). **Zone:** Null Zones.

Wherever Null Zones keeps its oldest scars, Narzugon tends to be found standing in them. It reads weakness in a party's cohesion faster than in their hit points. Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spy — STUB

*Huge Fiend, Neutral Evil.* **Challenge 12** (8400 XP). **Zone:** Boundless Void.

Spy did not come to Boundless Void by accident — something summoned, bound, or invited it, and that debt is still open. If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it. Play victory as temporary; the dissonance it fed does not vanish when the body does.

> **STUB — Director must re-skin.** The name *Spy* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warlock of the Fiend — STUB

*Huge Fiend, Lawful Evil.* **Challenge 12** (8400 XP). **Zone:** Null Zones.

Warlock of the Fiend is Chaos-Realm lineage wearing Null Zones like a costume it intends to keep. Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants. Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.

> **STUB — Director must re-skin.** The name *Warlock of the Fiend* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Fiend** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 3d8+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Eirfax, the Dusk Crowned

*Medium Fiend, Lawful Evil.* **Challenge 23** (50000 XP). **Zone:** Spiral Nexus.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 21 · **Hit Points** 315 · **Speed** 50 ft., fly 100 ft.

**Abilities** STR 18 · DEX 22 · CON 20 · INT 22 · WIS 20 · CHA 26

**Skills** Arcana +12, Deception +14, Insight +11, Perception +11

**Senses** Truesight 120 ft., passive Perception 21

**Languages** Sylvan, Common, telepathy 120 ft.

**Attacks**
- **Dusk Blade** (x3) — +12 to hit — 2d12+6 slashing
- **Crown of Dusk** (Recharge 5-6) — 8d8 necrotic, 20-ft. radius — wisdom save DC 20 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Xarog, the Pactbound Furnace

*Huge Fiend, Lawful Evil.* **Challenge 26** (90000 XP). **Zone:** Chorus of the First Choir.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 22 · **Hit Points** 350 · **Speed** 40 ft., fly 80 ft.

**Abilities** STR 26 · DEX 18 · CON 22 · INT 20 · WIS 18 · CHA 24

**Skills** Deception +13, Intimidation +13, Insight +10, Perception +10

**Senses** Truesight 120 ft., passive Perception 20

**Languages** Abyssal, Infernal, telepathy 120 ft.

**Attacks**
- **Furnace Chain** (x3) — +13 to hit — 3d10+6 fire, reach 20 ft.

**Defenses** Resistances: fire; Immunities: poison; Condition immunities: poisoned

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*


## The Giants

Giants measure Aethel in strides an Expedition measures in days, and their danger is almost always a logistics problem before it is a combat one. **Player knowledge** treats a Giant sighting as a warning about camps, caravans, and safe havens — Giants break structures and supply lines far more often than they hunt individual adventurers. **Director knowledge** should run Giant encounters as siege framing rather than duels: let terrain and structures become casualties alongside hit points, and force an Expedition to choose what to save rather than simply what to fight. A Giant's size should matter as much mechanically as it does narratively — collateral damage is the entire point of the type.

*Indexed creatures of this family: **72**.*

### Cyclops

*Medium Giant, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Veiled Expanse.

Scale is the argument Cyclops makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Darkling — STUB

*Medium Giant, Chaotic Good.* **Challenge 3** (700 XP). **Zone:** Aethel Rivers.

Scale is the argument Darkling makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Darkling* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dire Troll

*Large Giant, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Yieldheart.

Scale is the argument Dire Troll makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Erinyes — STUB

*Medium Giant, Neutral Good.* **Challenge 3** (700 XP). **Zone:** Null Zones.

Erinyes measures Null Zones in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Erinyes* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Frost Giant

*Medium Giant, Lawful Neutral.* **Challenge 3** (700 XP). **Zone:** Veiled Expanse.

Frost Giant does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Ape — STUB

*Medium Giant, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Aethel Deserts.

Scale is the argument Giant Ape makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Ape* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Bat — STUB

*Medium Giant, Chaotic Evil.* **Challenge 3** (700 XP). **Zone:** Aethel Lakes.

Aethel Lakes bears the marks of Giant Bat's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Bat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Centipede — STUB

*Medium Giant, True Neutral.* **Challenge 3** (700 XP). **Zone:** Radiant Isles.

Radiant Isles bears the marks of Giant Centipede's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Centipede* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Hyena — STUB

*Medium Giant, Neutral Good.* **Challenge 3** (700 XP). **Zone:** Radiant Isles.

Giant Hyena measures Radiant Isles in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Hyena* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Strider — STUB

*Medium Giant, Unaligned.* **Challenge 3** (700 XP). **Zone:** Aethel Tundra.

Giant Strider measures Aethel Tundra in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Strider* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Wasp — STUB

*Medium Giant, Chaotic Good.* **Challenge 3** (700 XP). **Zone:** Aethel Rivers.

Scale is the argument Giant Wasp makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Wasp* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Martial Arts Adept — STUB

*Large Giant, Unaligned.* **Challenge 3** (700 XP). **Zone:** The Dungeon.

The Dungeon bears the marks of Martial Arts Adept's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Martial Arts Adept* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shrieker — STUB

*Large Giant, Chaotic Evil.* **Challenge 3** (700 XP). **Zone:** Null Zones.

Shrieker measures Null Zones in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Shrieker* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Troll

*Large Giant, Chaotic Good.* **Challenge 3** (700 XP). **Zone:** Aethel Jungles.

Troll does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cloud Giant Smiling One

*Medium Giant, True Neutral.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Aethel Lowlands bears the marks of Cloud Giant Smiling One's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Conjurer — STUB

*Large Giant, Chaotic Good.* **Challenge 4** (1100 XP). **Zone:** Choir Sanctum.

Conjurer measures Choir Sanctum in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Conjurer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Badger — STUB

*Medium Giant, Chaotic Neutral.* **Challenge 4** (1100 XP). **Zone:** Aethel Jungles.

Scale is the argument Giant Badger makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Badger* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Octopus — STUB

*Medium Giant, Unaligned.* **Challenge 4** (1100 XP). **Zone:** Spiral Nexus.

Giant Octopus measures Spiral Nexus in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Octopus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Rat — STUB

*Medium Giant, Lawful Evil.* **Challenge 4** (1100 XP). **Zone:** Bastion of Flame.

Bastion of Flame bears the marks of Giant Rat's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Rat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Shark — STUB

*Medium Giant, Lawful Neutral.* **Challenge 4** (1100 XP). **Zone:** Null Zones.

Giant Shark measures Null Zones in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Shark* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Weasel — STUB

*Medium Giant, Lawful Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Scale is the argument Giant Weasel makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Weasel* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Killer Whale — STUB

*Large Giant, True Neutral.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Scale is the argument Killer Whale makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Killer Whale* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Merregon

*Large Giant, Lawful Neutral.* **Challenge 4** (1100 XP). **Zone:** Aethel Swamps.

Scale is the argument Merregon makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Noble — STUB

*Large Giant, Neutral Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Tundra.

Scale is the argument Noble makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Noble* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre

*Large Giant, Lawful Neutral.* **Challenge 4** (1100 XP). **Zone:** Veiled Expanse.

Ogre measures Veiled Expanse in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre Battering Ram

*Large Giant, Lawful Good.* **Challenge 4** (1100 XP). **Zone:** Radiant Isles.

Ogre Battering Ram measures Radiant Isles in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre Bolt Launcher

*Large Giant, Unaligned.* **Challenge 4** (1100 XP). **Zone:** Boundless Void.

Ogre Bolt Launcher does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre Chain Brute

*Large Giant, True Neutral.* **Challenge 4** (1100 XP). **Zone:** Aethel Swamps.

Ogre Chain Brute measures Aethel Swamps in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Star Spawn Grue — STUB

*Medium Giant, Lawful Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Rivers.

Star Spawn Grue measures Aethel Rivers in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Star Spawn Grue* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Star Spawn family; proposed: *Spiral Breach Grue*. Owner-flagged: full Aethel rewrite or 'Spiral breach echo' ecology stub.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Aurochs — STUB

*Huge Giant, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Aethel Deserts.

Scale is the argument Aurochs makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Aurochs* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cambion — STUB

*Large Giant, Lawful Evil.* **Challenge 5** (1800 XP). **Zone:** Choir Sanctum.

Cambion measures Choir Sanctum in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Cambion* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Frost Giant Everlasting One

*Large Giant, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Resonance Fields.

Scale is the argument Frost Giant Everlasting One makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Crab — STUB

*Large Giant, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Scale is the argument Giant Crab makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Crab* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Elk — STUB

*Large Giant, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Null Zones.

Null Zones bears the marks of Giant Elk's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Elk* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Goat — STUB

*Large Giant, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Jungles.

Aethel Jungles bears the marks of Giant Goat's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Goat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Lizard — STUB

*Huge Giant, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Planar Crossroads.

Scale is the argument Giant Lizard makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Lizard* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Scorpion — STUB

*Huge Giant, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Veiled Expanse.

Giant Scorpion measures Veiled Expanse in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Scorpion* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Vulture — STUB

*Large Giant, True Neutral.* **Challenge 5** (1800 XP). **Zone:** Veiled Expanse.

Giant Vulture measures Veiled Expanse in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Vulture* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hill Giant

*Large Giant, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Lakes.

Aethel Lakes bears the marks of Hill Giant's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre Howdah

*Large Giant, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Aethel Rivers.

Ogre Howdah does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rug of Smothering — STUB

*Large Giant, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Shardpools.

Rug of Smothering does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> **STUB — Director must re-skin.** The name *Rug of Smothering* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Storm Giant Quintessent

*Huge Giant, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Storm Giant Quintessent does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Triceratops — STUB

*Huge Giant, Lawful Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Lakes.

Aethel Lakes bears the marks of Triceratops's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Triceratops* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Troglodyte — STUB

*Large Giant, Chaotic Neutral.* **Challenge 5** (1800 XP). **Zone:** Aethel Deserts.

Scale is the argument Troglodyte makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Troglodyte* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Venom Troll

*Large Giant, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Swamps.

Scale is the argument Venom Troll makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Behir — STUB

*Large Giant, Lawful Evil.* **Challenge 6** (2300 XP). **Zone:** Bastion of Flame.

Bastion of Flame bears the marks of Behir's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Behir* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Carrion Crawler — STUB

*Large Giant, Lawful Neutral.* **Challenge 6** (2300 XP). **Zone:** Aethel Tundra.

Scale is the argument Carrion Crawler makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Carrion Crawler* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Charnel Crawler* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cloud Giant

*Large Giant, Neutral Evil.* **Challenge 6** (2300 XP). **Zone:** Spiral Nexus.

Spiral Nexus bears the marks of Cloud Giant's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flumph — STUB

*Huge Giant, Neutral Good.* **Challenge 6** (2300 XP). **Zone:** Spiral Nexus.

Flumph measures Spiral Nexus in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Lumen Drifter* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Boar — STUB

*Huge Giant, Neutral Evil.* **Challenge 6** (2300 XP). **Zone:** Bastion of Flame.

Scale is the argument Giant Boar makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Boar* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Toad — STUB

*Huge Giant, Chaotic Evil.* **Challenge 6** (2300 XP). **Zone:** Bastion of Flame.

Scale is the argument Giant Toad makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Toad* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shield Guardian — STUB

*Huge Giant, Unaligned.* **Challenge 6** (2300 XP). **Zone:** The Dungeon.

Shield Guardian does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> **STUB — Director must re-skin.** The name *Shield Guardian* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stone Giant

*Huge Giant, Unaligned.* **Challenge 6** (2300 XP). **Zone:** Bastion of Flame.

Bastion of Flame bears the marks of Stone Giant's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Storm Giant

*Huge Giant, Neutral Good.* **Challenge 6** (2300 XP). **Zone:** Aethel Oceans.

Storm Giant measures Aethel Oceans in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Arachnomancer — STUB

*Huge Giant, Chaotic Evil.* **Challenge 6** (2300 XP). **Zone:** Aethel Caves.

Umbrin Arachnomancer measures Aethel Caves in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Umbrin Arachnomancer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Giant**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Ascetic Monk — STUB

*Large Giant, Chaotic Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Astral Ascetic Monk measures Aethel Highlands in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Astral Ascetic Monk* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Giant**) was randomized independently of the Astral Ascetic concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Boneclaw — STUB

*Large Giant, Lawful Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Boneclaw does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> **STUB — Director must re-skin.** The name *Boneclaw* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Stone Guard — STUB

*Large Giant, Lawful Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Aethel Highlands bears the marks of Deep Dwarf Stone Guard's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Deep Dwarf Stone Guard* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Giant**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Flying Sword — STUB

*Huge Giant, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Flying Sword measures Aethel Mountains in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Flying Sword* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Crocodile — STUB

*Large Giant, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Rivers.

Aethel Rivers bears the marks of Giant Crocodile's passing the way a coastline bears the marks of tide. Its rages are slow to build and slower to end — the fight rarely ends when the giant does. Its size should matter mechanically as much as narratively — collateral damage is the point.

> **STUB — Director must re-skin.** The name *Giant Crocodile* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Frog — STUB

*Large Giant, Neutral Evil.* **Challenge 7** (2900 XP). **Zone:** Shardpools.

Scale is the argument Giant Frog makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Giant Frog* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giant Sea Horse — STUB

*Huge Giant, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Spiral Nexus.

Giant Sea Horse measures Spiral Nexus in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Giant Sea Horse* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Half-ogre — STUB

*Huge Giant, Unaligned.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Scale is the argument Half-ogre makes before anyone gets close enough to hear another one. It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is. Siege framing works better than a duel; let the terrain itself become a casualty.

> **STUB — Director must re-skin.** The name *Half-ogre* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Jackalwere

*Large Giant, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Swamps.

Jackalwere measures Aethel Swamps in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Master Thief — STUB

*Huge Giant, Neutral Evil.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Master Thief measures Yieldheart in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Master Thief* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rot Troll

*Large Giant, Chaotic Neutral.* **Challenge 7** (2900 XP). **Zone:** Veiled Expanse.

Rot Troll measures Veiled Expanse in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spirit Troll

*Huge Giant, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Spirit Troll measures Aethel Mountains in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stone Giant Dreamwalker

*Huge Giant, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Stone Giant Dreamwalker does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Shadowblade — STUB

*Large Giant, True Neutral.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Umbrin Shadowblade does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> **STUB — Director must re-skin.** The name *Umbrin Shadowblade* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Giant**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Archmage — STUB

*Large Giant, Lawful Neutral.* **Challenge 17** (18000 XP). **Zone:** Aethel Deserts.

Archmage does not fit the Decennium's corridors so much as override them. It negotiates only from a position of visible strength, and reads retreat as an invitation. A giant fight is a logistics problem wearing a combat encounter's face.

> **STUB — Director must re-skin.** The name *Archmage* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Elder Tempest — STUB

*Large Giant, Lawful Evil.* **Challenge 18** (20000 XP). **Zone:** Aethel Caves.

Elder Tempest measures Aethel Caves in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Elder Tempest* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll Pack Lord — STUB

*Huge Giant, Lawful Evil.* **Challenge 20** (25000 XP). **Zone:** Aethel Rivers.

Gnoll Pack Lord measures Aethel Rivers in strides most Expeditions measure in days. Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that. Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.

> **STUB — Director must re-skin.** The name *Gnoll Pack Lord* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Giant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +11 to hit — 3d12+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Humanoids

Humanoids are Aethel's living politics, not merely another bestiary category, and treating them as pure combat encounters wastes most of what the type is for. **Player knowledge** is whatever an Expedition has actually learned about a given floor culture's factions, grudges, and territory — Humanoids negotiate, inform, and betray as often as they fight. **Director knowledge** should track consequences: killing a Humanoid has a reputational cost that outlives the encounter, rippling through kin, rank, and floor politics an Expedition may need to navigate again later. A parley option should exist even when the table does not expect to use it, and a Humanoid's death should visibly change something — a market price, a patrol route, a grudge carried forward — rather than simply ending an encounter.

*Indexed creatures of this family: **40**.*

### Orc War Chief

*Small Humanoid, Neutral Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Orc War Chief belongs to Aethel Highlands's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Babau — STUB

*Medium Humanoid, Neutral Good.* **Challenge 3** (700 XP). **Zone:** Aethel Lowlands.

Aethel Lowlands has a culture, and Babau is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> **STUB — Director must re-skin.** The name *Babau* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Babau rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*
- **Abyssal Leak** (Recharge 5-6) — 3d8 acid, 20-ft. radius — constitution save DC 13 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gloom Weaver

*Large Humanoid, Neutral Evil.* **Challenge 3** (700 XP). **Zone:** Aethel Lowlands.

Gloom Weaver is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*
- **Shadow Weave** (Recharge 5-6) — 3d6 necrotic, 20-ft. radius — wisdom save DC 13 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hobgoblin Warlord

*Small Humanoid, True Neutral.* **Challenge 3** (700 XP). **Zone:** Aethel Highlands.

Aethel Highlands has a culture, and Hobgoblin Warlord is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kobold

*Medium Humanoid, Unaligned.* **Challenge 3** (700 XP). **Zone:** Aethel Forests.

Aethel Forests has a culture, and Kobold is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Eye of Gruumsh — STUB

*Small Humanoid, Chaotic Good.* **Challenge 3** (700 XP). **Zone:** Yieldheart.

Somewhere in Yieldheart, Orc Eye of Gruumsh answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Eye of the One-Eyed Pact* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Nurtured One of Yurtrus — STUB

*Medium Humanoid, Chaotic Good.* **Challenge 3** (700 XP). **Zone:** Aethel Highlands.

Orc Nurtured One of Yurtrus belongs to Aethel Highlands's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Nurtured One of the Rot Sigil* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spirit Naga — STUB

*Medium Humanoid, True Neutral.* **Challenge 3** (700 XP). **Zone:** Aethel Lowlands.

Spirit Naga is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — Director must re-skin.** The name *Spirit Naga* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wastrilith — STUB

*Small Humanoid, Unaligned.* **Challenge 3** (700 XP). **Zone:** Yieldheart.

Somewhere in Yieldheart, Wastrilith answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — Director must re-skin.** The name *Wastrilith* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Wastrilith rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Reaver Warrior

*Medium Humanoid, Neutral Evil.* **Challenge 4** (1100 XP). **Zone:** Aethel Forests.

Somewhere in Aethel Forests, Astral Reaver Warrior answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hobgoblin Captain

*Medium Humanoid, Lawful Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Highlands.

Somewhere in Aethel Highlands, Hobgoblin Captain answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kobold Scale Sorcerer

*Small Humanoid, Chaotic Good.* **Challenge 4** (1100 XP). **Zone:** Yieldheart.

Somewhere in Yieldheart, Kobold Scale Sorcerer answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Monodrone — STUB

*Small Humanoid, Chaotic Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Monodrone is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — Director must re-skin.** The name *Monodrone* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Monodrone rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc

*Large Humanoid, Neutral Good.* **Challenge 4** (1100 XP). **Zone:** Yieldheart.

Yieldheart has a culture, and Orc is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Red Fang of Shargaas — STUB

*Medium Humanoid, Neutral Good.* **Challenge 4** (1100 XP). **Zone:** Yieldheart.

Somewhere in Yieldheart, Orc Red Fang of Shargaas answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Red Fang of the Veiled Hunt* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dretch — STUB

*Large Humanoid, Unaligned.* **Challenge 5** (1800 XP). **Zone:** Aethel Highlands.

Dretch is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — Director must re-skin.** The name *Dretch* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Dretch rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Goblin Boss

*Medium Humanoid, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Highlands.

Goblin Boss belongs to Aethel Highlands's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kobold Inventor — STUB

*Large Humanoid, Chaotic Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Kobold Inventor is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Marilith — STUB

*Medium Humanoid, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Lowlands.

Marilith belongs to Aethel Lowlands's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — Director must re-skin.** The name *Marilith* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Marilith rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Claw of Luthic — STUB

*Medium Humanoid, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Highlands.

Somewhere in Aethel Highlands, Orc Claw of Luthic answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Claw of the Den-Mother* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sibriex — STUB

*Medium Humanoid, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Yieldheart.

Sibriex belongs to Yieldheart's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — Director must re-skin.** The name *Sibriex* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Sibriex rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Veteran

*Medium Humanoid, Chaotic Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Somewhere in Aethel Forests, Veteran answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wereboar

*Large Humanoid, Neutral Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Somewhere in Aethel Forests, Wereboar answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Winged Kobold — STUB

*Large Humanoid, Unaligned.* **Challenge 5** (1800 XP). **Zone:** Aethel Highlands.

Somewhere in Aethel Highlands, Winged Kobold answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bard

*Large Humanoid, Chaotic Evil.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

Bard is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Dissonant Verse** (Recharge 5-6) — 4d8 thunder, 20-ft. radius — constitution save DC 15 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dybbuk — STUB

*Large Humanoid, Lawful Evil.* **Challenge 6** (2300 XP). **Zone:** Yieldheart.

Dybbuk belongs to Yieldheart's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — Director must re-skin.** The name *Dybbuk* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Frost Salamander — STUB

*Large Humanoid, Chaotic Neutral.* **Challenge 6** (2300 XP). **Zone:** Aethel Lowlands.

Aethel Lowlands has a culture, and Frost Salamander is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> **STUB — Director must re-skin.** The name *Frost Salamander* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Guard

*Medium Humanoid, Chaotic Good.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

Guard is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hobgoblin — STUB

*Large Humanoid, Neutral Good.* **Challenge 6** (2300 XP). **Zone:** Aethel Lowlands.

Somewhere in Aethel Lowlands, Hobgoblin answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hobgoblin Iron Shadow — STUB

*Large Humanoid, Unaligned.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

Somewhere in Aethel Forests, Hobgoblin Iron Shadow answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Blade of Ilneval — STUB

*Large Humanoid, Chaotic Neutral.* **Challenge 6** (2300 XP). **Zone:** Aethel Highlands.

Somewhere in Aethel Highlands, Orc Blade of Ilneval answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Blade of the Iron March* (not yet locked — see Naming & IP Reskin Ledger).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Spawn of Kyuss — STUB

*Large Humanoid, Chaotic Good.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

Spawn of Kyuss belongs to Aethel Forests's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — Director must re-skin.** The name *Spawn of Kyuss* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Spawn of the Worm Spiral* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Violet Fungus — STUB

*Large Humanoid, Lawful Neutral.* **Challenge 6** (2300 XP). **Zone:** Aethel Lowlands.

Violet Fungus belongs to Aethel Lowlands's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> **STUB — Director must re-skin.** The name *Violet Fungus* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Centaur — STUB

*Medium Humanoid, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Centaur is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — Director must re-skin.** The name *Centaur* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Druid

*Medium Humanoid, Chaotic Good.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Druid belongs to Yieldheart's living politics, not merely its bestiary. Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score. Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Goblin

*Medium Humanoid, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Somewhere in Aethel Highlands, Goblin answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Green Hag — STUB

*Large Humanoid, Unaligned.* **Challenge 7** (2900 XP). **Zone:** Aethel Highlands.

Aethel Highlands has a culture, and Green Hag is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> **STUB — Director must re-skin.** The name *Green Hag* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Iron Cobra — STUB

*Medium Humanoid, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Lowlands.

Somewhere in Aethel Lowlands, Iron Cobra answers to a chain of command an Expedition has not yet mapped. It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point. A parley option should exist even when the table does not expect to take it.

> **STUB — Director must re-skin.** The name *Iron Cobra* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Humanoid** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Orc Hand of Yurtrus — STUB

*Large Humanoid, Lawful Good.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Orc Hand of Yurtrus is a person first and a stat block second, whatever the Excel sheet implies. Its loyalty is to people and place first, ideology a distant second. Its death should change something on the floor: a market price, a patrol route, a grudge.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Orc Hand of the Rot Sigil* (not yet locked — see Naming & IP Reskin Ledger).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warlord

*Medium Humanoid, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Yieldheart.

Yieldheart has a culture, and Warlord is one of the people who has to live in it after the party leaves. It fights smarter than its stat block suggests when defending home ground or kin. Use it to make the Decennium feel inhabited, not just infested.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## Monstrosities

Monstrosities are life that should not breed true in Aethel, and yet, floor after floor, evidently does. No single natural process explains the type; something about the Decennium's depths keeps deciding that biology is a suggestion rather than a rule. **Player knowledge** treats a Monstrosity sighting as territory marked in ways a careful approach can read before contact — most hunt with an efficiency that outpaces their apparent intelligence. **Director knowledge** should treat repeat sightings as an infestation problem rather than a monster-of-the-week problem, escalating a given Monstrosity type across a Cycle as "the thing that's spreading" when it recurs. Their parts are valuable specifically because they should not exist — Research teams will pay well for proof, and an Expedition often has to choose between finishing the kill and finishing the investigation.

*Indexed creatures of this family: **50**.*

### Banderhobb

*Large Monstrosity, Lawful Good.* **Challenge 3** (700 XP). **Zone:** Choir Sanctum.

Choir Sanctum keeps producing things like Banderhobb, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Basilisk

*Medium Monstrosity, Unaligned.* **Challenge 3** (700 XP). **Zone:** Aethel Highlands.

Basilisk is life that should not breed true in Aethel Highlands — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Bat — STUB

*Large Monstrosity, True Neutral.* **Challenge 3** (700 XP). **Zone:** Aethel Mountains.

No natural process explains Bat; something in Aethel Mountains decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Bat* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Chimera

*Small Monstrosity, Lawful Good.* **Challenge 3** (700 XP). **Zone:** Aethel Jungles.

No natural process explains Chimera; something in Aethel Jungles decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Kavalrachni — STUB

*Medium Monstrosity, True Neutral.* **Challenge 3** (700 XP). **Zone:** Yieldheart.

Deep Dwarf Kavalrachni is life that should not breed true in Yieldheart — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Deep Dwarf Kavalrachni* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Monstrosity**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gelatinous Cube — STUB

*Medium Monstrosity, Chaotic Neutral.* **Challenge 3** (700 XP). **Zone:** Shardpools.

Gelatinous Cube is life that should not breed true in Shardpools — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Gelatinous Cube* reads as **Ooze** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grung — STUB

*Large Monstrosity, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Aethel Swamps.

Aethel Swamps keeps producing things like Grung, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Grung* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Poison-Skin* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Manticore

*Medium Monstrosity, True Neutral.* **Challenge 3** (700 XP). **Zone:** Radiant Isles.

Radiant Isles keeps producing things like Manticore, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Nilbog — STUB

*Medium Monstrosity, Unaligned.* **Challenge 3** (700 XP). **Zone:** Radiant Isles.

No natural process explains Nilbog; something in Radiant Isles decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Nilbog* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Phoenix — STUB

*Medium Monstrosity, Lawful Good.* **Challenge 3** (700 XP). **Zone:** Boundless Void.

Phoenix looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Phoenix* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pteranodon — STUB

*Medium Monstrosity, True Neutral.* **Challenge 3** (700 XP). **Zone:** Aethel Mountains.

Pteranodon is life that should not breed true in Aethel Mountains — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Pteranodon* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 2d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rutterkin — STUB

*Large Monstrosity, Neutral Evil.* **Challenge 3** (700 XP). **Zone:** Shardpools.

Rutterkin is life that should not breed true in Shardpools — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Rutterkin* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Giff — STUB

*Medium Monstrosity, Chaotic Evil.* **Challenge 4** (1100 XP). **Zone:** Boundless Void.

No natural process explains Giff; something in Boundless Void decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Giff* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hadrosaurus — STUB

*Medium Monstrosity, Unaligned.* **Challenge 4** (1100 XP). **Zone:** Veiled Expanse.

Hadrosaurus is life that should not breed true in Veiled Expanse — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Hadrosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Homunculus — STUB

*Medium Monstrosity, Neutral Evil.* **Challenge 4** (1100 XP). **Zone:** Aethel Oceans.

No natural process explains Homunculus; something in Aethel Oceans decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Homunculus* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hydra

*Medium Monstrosity, Neutral Evil.* **Challenge 4** (1100 XP). **Zone:** Aethel Swamps.

Hydra is life that should not breed true in Aethel Swamps — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Gargantuan**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mindwitness — STUB

*Medium Monstrosity, Lawful Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Rivers.

No natural process explains Mindwitness; something in Aethel Rivers decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Mindwitness* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shadow Mastiff Alpha

*Large Monstrosity, Chaotic Good.* **Challenge 4** (1100 XP). **Zone:** Aethel Lowlands.

Shadow Mastiff Alpha looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d6+3 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Rot Grubs

*Medium Monstrosity, Chaotic Evil.* **Challenge 4** (1100 XP). **Zone:** Shardpools.

Shardpools keeps producing things like Swarm of Rot Grubs, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Huge**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Acolyte — STUB

*Large Monstrosity, Lawful Good.* **Challenge 5** (1800 XP). **Zone:** Aethel Rivers.

Acolyte is life that should not breed true in Aethel Rivers — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Acolyte* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Warp Pulse** (Recharge 5-6) — 4d8 psychic, 20-ft. radius — wisdom save DC 15 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Allip — STUB

*Large Monstrosity, True Neutral.* **Challenge 5** (1800 XP). **Zone:** Radiant Isles.

Radiant Isles keeps producing things like Allip, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Allip* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ankheg

*Large Monstrosity, Lawful Neutral.* **Challenge 5** (1800 XP). **Zone:** Aethel Forests.

Aethel Forests keeps producing things like Ankheg, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Darkmantle — STUB

*Large Monstrosity, Neutral Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Deserts.

Darkmantle looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Xarrorn — STUB

*Large Monstrosity, Neutral Good.* **Challenge 5** (1800 XP). **Zone:** Yieldheart.

Yieldheart keeps producing things like Deep Dwarf Xarrorn, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Deep Dwarf Xarrorn* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Monstrosity**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dust Mephit — STUB

*Large Monstrosity, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Choir Sanctum.

Dust Mephit is life that should not breed true in Choir Sanctum — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Dust Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ettin — STUB

*Large Monstrosity, Unaligned.* **Challenge 5** (1800 XP). **Zone:** Aethel Lakes.

Aethel Lakes keeps producing things like Ettin, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Ettin* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Froghemoth

*Medium Monstrosity, Chaotic Neutral.* **Challenge 5** (1800 XP). **Zone:** Aethel Jungles.

No natural process explains Froghemoth; something in Aethel Jungles decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grick Alpha

*Large Monstrosity, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Veiled Expanse.

Veiled Expanse keeps producing things like Grick Alpha, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Griffon — STUB

*Huge Monstrosity, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Radiant Isles.

No natural process explains Griffon; something in Radiant Isles decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Griffon* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mage — STUB

*Huge Monstrosity, Unaligned.* **Challenge 5** (1800 XP). **Zone:** Boundless Void.

Mage is life that should not breed true in Boundless Void — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Mage* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Rhinoceros — STUB

*Large Monstrosity, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Aethel Caves.

Rhinoceros is life that should not breed true in Aethel Caves — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Rhinoceros* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Slaad Tadpole — STUB

*Large Monstrosity, Chaotic Good.* **Challenge 5** (1800 XP). **Zone:** Spiral Nexus.

Slaad Tadpole looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Chaos-Husk Tadpole*. Invented planar-race terminology; needs Aethel identity.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Blackguard — STUB

*Large Monstrosity, Unaligned.* **Challenge 6** (2300 XP). **Zone:** Aethel Forests.

Blackguard looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Blackguard* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Death Kiss — STUB

*Large Monstrosity, Lawful Evil.* **Challenge 6** (2300 XP). **Zone:** Aethel Lakes.

No natural process explains Death Kiss; something in Aethel Lakes decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Death Kiss* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gazer — STUB

*Large Monstrosity, Unaligned.* **Challenge 6** (2300 XP). **Zone:** Spiral Nexus.

No natural process explains Gazer; something in Spiral Nexus decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Gazer* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Monstrosity**) was randomized independently of the Gazer concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Neogi — STUB

*Large Monstrosity, Chaotic Evil.* **Challenge 6** (2300 XP). **Zone:** Aethel Swamps.

Neogi is life that should not breed true in Aethel Swamps — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Neogi* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Neogi family; proposed: *Void Broker*. Owner-flagged: 'Spiral breach echo' family or full rewrite.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Skulk — STUB

*Huge Monstrosity, Neutral Good.* **Challenge 6** (2300 XP). **Zone:** Aethel Rivers.

Skulk is life that should not breed true in Aethel Rivers — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Skulk* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Star Spawn Mangler — STUB

*Huge Monstrosity, True Neutral.* **Challenge 6** (2300 XP). **Zone:** Choir Sanctum.

Star Spawn Mangler looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Star Spawn Mangler* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Star Spawn family; proposed: *Spiral Breach Mangler*. Owner-flagged: full Aethel rewrite or 'Spiral breach echo' ecology stub.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +6 to hit — 2d8+4 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Stone Cursed — STUB

*Medium Monstrosity, Chaotic Neutral.* **Challenge 6** (2300 XP). **Zone:** Null Zones.

Stone Cursed looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Stone Cursed* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +6 to hit — 2d8+4 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Ascetic Sentinel — STUB

*Large Monstrosity, True Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Swamps.

Astral Ascetic Sentinel is life that should not breed true in Aethel Swamps — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Astral Ascetic Sentinel* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Monstrosity**) was randomized independently of the Astral Ascetic concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Badger — STUB

*Huge Monstrosity, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Badger looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Badger* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Soulblade — STUB

*Large Monstrosity, Chaotic Evil.* **Challenge 7** (2900 XP). **Zone:** Bastion of Flame.

Deep Dwarf Soulblade is life that should not breed true in Bastion of Flame — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Deep Dwarf Soulblade* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Monstrosity**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Enchanter — STUB

*Large Monstrosity, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Aethel Tundra.

Aethel Tundra keeps producing things like Enchanter, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Enchanter* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll Flesh Gnawer — STUB

*Large Monstrosity, Chaotic Neutral.* **Challenge 7** (2900 XP). **Zone:** Spiral Nexus.

No natural process explains Gnoll Flesh Gnawer; something in Spiral Nexus decided biology was a suggestion. It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them. Its parts are valuable specifically because it should not exist — Research teams will pay for proof.

> **STUB — Director must re-skin.** The name *Gnoll Flesh Gnawer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Guardian Naga — STUB

*Large Monstrosity, Unaligned.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Guardian Naga is life that should not breed true in Aethel Mountains — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Guardian Naga* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hippogriff — STUB

*Medium Monstrosity, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Aethel Swamps.

Hippogriff looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Hippogriff* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hyena — STUB

*Large Monstrosity, Lawful Evil.* **Challenge 7** (2900 XP). **Zone:** Veiled Expanse.

Hyena looks assembled from parts that used to belong to smaller arguments. It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor. Use it to make an Expedition choose between finishing the kill and finishing the investigation.

> **STUB — Director must re-skin.** The name *Hyena* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ki-rin — STUB

*Large Monstrosity, Lawful Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Mountains.

Aethel Mountains keeps producing things like Ki-rin, which is either an infestation or an ecosystem, depending who you ask. Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem. A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.

> **STUB — Director must re-skin.** The name *Ki-rin* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Octopus — STUB

*Large Monstrosity, Neutral Evil.* **Challenge 7** (2900 XP). **Zone:** Choir Sanctum.

Octopus is life that should not breed true in Choir Sanctum — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Octopus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +7 to hit — 2d8+5 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vegepygmy Chief — STUB

*Large Monstrosity, True Neutral.* **Challenge 7** (2900 XP). **Zone:** Aethel Tundra.

Vegepygmy Chief is life that should not breed true in Aethel Tundra — and yet, evidently, it does. Its territory in {zone} is marked in ways a careful Recon pass can read before contact. Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.

> **STUB — Director must re-skin.** The name *Vegepygmy Chief* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Monstrosity** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Gargantuan**.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +7 to hit — 2d8+5 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Oozes

Oozes are Aethel's patience made corrosive — environmental hazards wearing a stat block, born from a failed watch rotation, a badly sealed corridor, or a drain that should have been checked years ago. **Player knowledge** is almost entirely procedural: what dissolves it, what it dissolves in turn, and which gaps a locked door was supposed to make irrelevant. **Director knowledge** should punish poor watch rotations and sealed, unventilated spaces specifically — an Ooze encounter is at its best when it is clearly the consequence of an earlier logistics failure rather than a random ambush. Let equipment loss matter as much as hit point loss, and remember that most Oozes do not negotiate, flee meaningfully, or feel provoked; they simply continue until something stops them.

*Indexed creatures of this family: **43**.*

### Grung Wildling — STUB

*Small Ooze, Lawful Evil.* **Challenge 0** (10 XP). **Zone:** Null Zones.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Grung Wildling is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Grung Wildling* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Poison-Skin Wildling* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Marid — STUB

*Tiny Ooze, Chaotic Good.* **Challenge 0** (10 XP). **Zone:** Aethel Rivers.

Marid has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Marid* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Merrenoloth — STUB

*Small Ooze, Lawful Evil.* **Challenge 0** (10 XP). **Zone:** Yieldheart.

Merrenoloth is Yieldheart's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Merrenoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Ferry-Wraith of the Hush* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Piercer — STUB

*Tiny Ooze, Lawful Evil.* **Challenge 0** (10 XP). **Zone:** Aethel Swamps.

Aethel Swamps keeps Piercer the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Piercer* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Retriever — STUB

*Tiny Ooze, Lawful Neutral.* **Challenge 0** (10 XP). **Zone:** Radiant Isles.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Retriever is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Retriever* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Revenant — STUB

*Tiny Ooze, Lawful Good.* **Challenge 0** (10 XP). **Zone:** Aethel Oceans.

Revenant has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Revenant* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umber Hulk — STUB

*Small Ooze, Chaotic Good.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Umber Hulk is Aethel Highlands's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Umber Hulk* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Deep Borer* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Weasel — STUB

*Tiny Ooze, True Neutral.* **Challenge 0** (10 XP). **Zone:** Radiant Isles.

Weasel is Radiant Isles's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Weasel* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Xorn — STUB

*Small Ooze, Lawful Good.* **Challenge 0** (10 XP). **Zone:** Shardpools.

Xorn is Shardpools's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Xorn* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Screamer — STUB

*Tiny Ooze, Neutral Evil.* **Challenge 1/8** (25 XP). **Zone:** Aethel Lowlands.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Deep Dwarf Screamer is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Deep Dwarf Screamer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Ooze**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Fomorian — STUB

*Tiny Ooze, Lawful Good.* **Challenge 1/8** (25 XP). **Zone:** Aethel Rivers.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Fomorian is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Fomorian* reads as **Giant** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Illusionist — STUB

*Small Ooze, Neutral Evil.* **Challenge 1/8** (25 XP). **Zone:** Bastion of Flame.

Illusionist has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Illusionist* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Androsphinx — STUB

*Small Ooze, Lawful Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Highlands.

Androsphinx has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Androsphinx* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*
- **Caustic Surge** (Recharge 6-6) — 2d6 acid, 20-ft. radius — constitution save DC 11 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Annis Hag — STUB

*Small Ooze, Chaotic Neutral.* **Challenge 1/4** (50 XP). **Zone:** Aethel Rivers.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Annis Hag is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Annis Hag* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Despot — STUB

*Small Ooze, Chaotic Good.* **Challenge 1/4** (50 XP). **Zone:** Veiled Expanse.

Deep Dwarf Despot is Veiled Expanse's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Deep Dwarf Despot* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Ooze**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gray Ooze

*Tiny Ooze, Neutral Evil.* **Challenge 1/4** (50 XP). **Zone:** Radiant Isles.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Gray Ooze is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ochre Jelly

*Small Ooze, Neutral Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Caves.

Aethel Caves keeps Ochre Jelly the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Worg — STUB

*Small Ooze, Chaotic Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Rivers.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Worg is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Worg* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Canoloth — STUB

*Small Ooze, Lawful Neutral.* **Challenge 1/2** (100 XP). **Zone:** Choir Sanctum.

Choir Sanctum keeps Canoloth the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Canoloth* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Yugoloth rank family; proposed: *Hush-Broker (Canoloth rank)*. Invented neutral-fiend hierarchy; fold into Aethel 'Hush-Broker' mercenary fiends.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Dao — STUB

*Small Ooze, Chaotic Neutral.* **Challenge 1/2** (100 XP). **Zone:** Spiral Nexus.

Spiral Nexus keeps Dao the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Dao* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ettercap — STUB

*Small Ooze, Chaotic Good.* **Challenge 1/2** (100 XP). **Zone:** Spiral Nexus.

Ettercap is Spiral Nexus's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Ettercap* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hook Horror — STUB

*Small Ooze, Chaotic Evil.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lakes.

Hook Horror is Aethel Lakes's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Rip-Auger* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Hunter Shark — STUB

*Tiny Ooze, Lawful Good.* **Challenge 1/2** (100 XP). **Zone:** Spiral Nexus.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Hunter Shark is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Hunter Shark* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Merfolk — STUB

*Small Ooze, Chaotic Evil.* **Challenge 1/2** (100 XP). **Zone:** Aethel Oceans.

Aethel Oceans keeps Merfolk the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Merfolk* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Morkoth — STUB

*Medium Ooze, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Rivers.

Morkoth is Aethel Rivers's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — Director must re-skin.** The name *Morkoth* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shadow Dancer — STUB

*Small Ooze, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Bastion of Flame.

Shadow Dancer has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Shadow Dancer* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tribal Warrior

*Medium Ooze, Neutral Good.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lakes.

Tribal Warrior has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Allosaurus — STUB

*Medium Ooze, Lawful Good.* **Challenge 1** (200 XP). **Zone:** Resonance Fields.

Allosaurus has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Allosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*
- **Caustic Spit** (Recharge 5-6) — 2d8 acid, 20-ft. radius — dexterity save DC 12 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Black Pudding

*Small Ooze, Chaotic Good.* **Challenge 1** (200 XP). **Zone:** Aethel Tundra.

Black Pudding is Aethel Tundra's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Hammerer — STUB

*Medium Ooze, Chaotic Good.* **Challenge 1** (200 XP). **Zone:** Shardpools.

Deep Dwarf Hammerer has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Deep Dwarf Hammerer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Ooze**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Drider — STUB

*Small Ooze, True Neutral.* **Challenge 1** (200 XP). **Zone:** Yieldheart.

Drider is Yieldheart's patience made corrosive — it does not chase, because it has never needed to. It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse. Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Umbrin Arachnid* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gnoll — STUB

*Small Ooze, Lawful Neutral.* **Challenge 1** (200 XP). **Zone:** Boundless Void.

Boundless Void keeps Gnoll the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Gnoll* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Kraken Priest

*Medium Ooze, Chaotic Evil.* **Challenge 1** (200 XP). **Zone:** Aethel Lakes.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Kraken Priest is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Malison — STUB

*Medium Ooze, Unaligned.* **Challenge 1** (200 XP). **Zone:** Aethel Mountains.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Serpent-Blood Malison is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Serpent-Blood Malison* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Ooze**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Swarm of Rats

*Large Ooze, Chaotic Evil.* **Challenge 1** (200 XP). **Zone:** Aethel Lakes.

Swarm of Rats has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Yochlol — STUB

*Medium Ooze, Chaotic Evil.* **Challenge 1** (200 XP). **Zone:** Aethel Highlands.

Aethel Highlands keeps Yochlol the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Yochlol* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Yochlol rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d8+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deinonychus — STUB

*Small Ooze, Unaligned.* **Challenge 2** (450 XP). **Zone:** Spiral Nexus.

Deinonychus has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Deinonychus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Korred — STUB

*Medium Ooze, Neutral Evil.* **Challenge 2** (450 XP). **Zone:** Choir Sanctum.

Korred has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous. Splitting it without the right approach multiplies the problem instead of solving it. Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.

> **STUB — Director must re-skin.** The name *Korred* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Magma Mephit — STUB

*Medium Ooze, Chaotic Neutral.* **Challenge 2** (450 XP). **Zone:** The Dungeon.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Magma Mephit is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Magma Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Steam Mephit — STUB

*Medium Ooze, Neutral Good.* **Challenge 2** (450 XP). **Zone:** Aethel Caves.

Aethel Caves keeps Steam Mephit the way old buildings keep damp: quietly, structurally, and worse than it looks. It does not negotiate, flee meaningfully, or feel provoked — it simply continues. Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.

> **STUB — Director must re-skin.** The name *Steam Mephit* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Xvart — STUB

*Medium Ooze, Lawful Evil.* **Challenge 2** (450 XP). **Zone:** Aethel Swamps.

Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and Xvart is the result. It squeezes through gaps a locked door was supposed to make irrelevant. Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.

> **STUB — Director must re-skin.** The name *Xvart* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Ooze** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vaskor, the Stone Maw

*Large Ooze, Unaligned.* **Challenge 8** (3900 XP). **Zone:** Boundless Void.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 17 · **Hit Points** 168 · **Speed** 30 ft., burrow 20 ft.

**Abilities** STR 20 · DEX 8 · CON 18 · INT 10 · WIS 12 · CHA 8

**Skills** Athletics +8, Intimidation +2

**Senses** Darkvision 60 ft., Tremorsense 120 ft., passive Perception 11

**Languages** Terran

**Attacks**
- **Stone Maw** (x2) — +7 to hit — 2d10+5 bludgeoning
- **Seismic Roar** (Recharge 5-6) — 4d8 bludgeoning, 20-ft. radius — strength save DC 15 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### The Marquis of Silence

*Large Ooze, Chaotic Good.* **Challenge 30** (155000 XP). **Zone:** Aethel Caves.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 24 · **Hit Points** 450 · **Speed** 60 ft., fly 120 ft.

**Abilities** STR 30 · DEX 22 · CON 26 · INT 28 · WIS 24 · CHA 30

**Skills** Deception +17, Intimidation +17, Insight +15, Perception +15

**Senses** Truesight 120 ft., passive Perception 25

**Languages** All, telepathy 120 ft.

**Attacks**
- **Silent Decree** (x3) — +15 to hit — 4d10+7 psychic
- **Zone of Silence** (Recharge 5-6) — 10d10 psychic, 20-ft. radius — constitution save DC 23 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*


## The Plants

Plants across Bloomdeep and Aethel's verdant zones grew where the Decennium should have stayed empty, and kept growing past the point anyone could stop them politely. **Player knowledge** treats a Plant encounter as area control and attrition rather than a single dramatic strike — the terrain itself punishes anyone who lingers. **Director knowledge** should reward antidotes, cleared sightlines, and fire over raw damage output, and should remember that cutting the visible threat rarely solves the root problem, sometimes literally. A Plant's harvestable parts are valuable specifically because most Expeditions are too busy retreating to collect them — use that tension to make retreat a real, costed choice rather than a free action.

*Indexed creatures of this family: **36**.*

### Banshee — STUB

*Tiny Plant, Lawful Evil.* **Challenge 0** (10 XP). **Zone:** Aethel Swamps.

Banshee grew where Aethel Swamps should have stayed empty, and kept growing past the point anyone could stop it politely. Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest. Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.

> **STUB — Director must re-skin.** The name *Banshee* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cranium Rat — STUB

*Tiny Plant, Lawful Good.* **Challenge 0** (10 XP). **Zone:** The Dungeon.

The Dungeon's bloom cycles produced Cranium Rat the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Cranium Rat* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Priest — STUB

*Tiny Plant, True Neutral.* **Challenge 0** (10 XP). **Zone:** Aethel Oceans.

Priest does not hate the Expeditions that pass through Aethel Oceans; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Priest* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tyrannosaurus Rex — STUB

*Tiny Plant, Neutral Evil.* **Challenge 0** (10 XP). **Zone:** Aethel Highlands.

Root, spore, and vine answer to Tyrannosaurus Rex across more of Aethel Highlands than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Tyrannosaurus Rex* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Umbrin Spider-Priestess — STUB

*Tiny Plant, True Neutral.* **Challenge 0** (10 XP). **Zone:** Aethel Jungles.

Root, spore, and vine answer to Umbrin Spider-Priestess across more of Aethel Jungles than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Umbrin Spider-Priestess* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Umbrin concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Derro — STUB

*Tiny Plant, Neutral Good.* **Challenge 1/8** (25 XP). **Zone:** Aethel Lowlands.

Aethel Lowlands's bloom cycles produced Derro the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Derro* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Diviner — STUB

*Tiny Plant, Neutral Evil.* **Challenge 1/8** (25 XP). **Zone:** Aethel Oceans.

Aethel Oceans's bloom cycles produced Diviner the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Diviner* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Empyrean — STUB

*Tiny Plant, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Lowlands.

Empyrean grew where Aethel Lowlands should have stayed empty, and kept growing past the point anyone could stop it politely. Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest. Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.

> **STUB — Director must re-skin.** The name *Empyrean* reads as **Celestial** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grung Elite Warrior — STUB

*Tiny Plant, Lawful Neutral.* **Challenge 1/8** (25 XP). **Zone:** Boundless Void.

Boundless Void's bloom cycles produced Grung Elite Warrior the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Grung Elite Warrior* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Poison-Skin Elite* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sahuagin — STUB

*Tiny Plant, Lawful Evil.* **Challenge 1/8** (25 XP). **Zone:** Spiral Nexus.

Root, spore, and vine answer to Sahuagin across more of Spiral Nexus than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Sahuagin* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Shambling Mound

*Tiny Plant, Chaotic Good.* **Challenge 1/8** (25 XP). **Zone:** Null Zones.

Shambling Mound grew where Null Zones should have stayed empty, and kept growing past the point anyone could stop it politely. Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest. Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d4+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sporefolk Sovereign

*Tiny Plant, Chaotic Evil.* **Challenge 1/8** (25 XP). **Zone:** The Dungeon.

Root, spore, and vine answer to Sporefolk Sovereign across more of The Dungeon than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Ascetic Anarch — STUB

*Small Plant, True Neutral.* **Challenge 1/4** (50 XP). **Zone:** Aethel Lakes.

Astral Ascetic Anarch does not hate the Expeditions that pass through Aethel Lakes; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Astral Ascetic Anarch* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Astral Ascetic concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d6+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lizardfolk Shaman — STUB

*Medium Plant, Lawful Evil.* **Challenge 1/4** (50 XP). **Zone:** Aethel Oceans.

Root, spore, and vine answer to Lizardfolk Shaman across more of Aethel Oceans than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Lizardfolk Shaman* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Oaken Bolter — STUB

*Small Plant, Lawful Evil.* **Challenge 1/4** (50 XP). **Zone:** Aethel Jungles.

Oaken Bolter does not hate the Expeditions that pass through Aethel Jungles; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Oaken Bolter* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Broodguard — STUB

*Medium Plant, Chaotic Evil.* **Challenge 1/4** (50 XP). **Zone:** Aethel Swamps.

Serpent-Blood Broodguard does not hate the Expeditions that pass through Aethel Swamps; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Serpent-Blood Broodguard* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ulitharid — STUB

*Small Plant, Neutral Good.* **Challenge 1/4** (50 XP). **Zone:** Aethel Jungles.

Aethel Jungles's bloom cycles produced Ulitharid the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Ulitharid* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d6+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wretched Sorrowsworn — STUB

*Medium Plant, True Neutral.* **Challenge 1/4** (50 XP). **Zone:** Aethel Caves.

Root, spore, and vine answer to Wretched Sorrowsworn across more of Aethel Caves than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — stock alias, Director must re-skin.** Part of the Sorrowsworn family; proposed: *Wretched Grief-Bound*. Invented emotion-fey terminology; safe to rename without losing concept.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **18** instead of **14**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 18 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +3 to hit — 1d6+1 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cockatrice — STUB

*Small Plant, Chaotic Evil.* **Challenge 1/2** (100 XP). **Zone:** Choir Sanctum.

Cockatrice grew where Choir Sanctum should have stayed empty, and kept growing past the point anyone could stop it politely. Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest. Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.

> **STUB — Director must re-skin.** The name *Cockatrice* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf Warlord — STUB

*Small Plant, Unaligned.* **Challenge 1/2** (100 XP). **Zone:** Aethel Forests.

Root, spore, and vine answer to Deep Dwarf Warlord across more of Aethel Forests than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Deep Dwarf Warlord* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Elk — STUB

*Small Plant, Lawful Evil.* **Challenge 1/2** (100 XP). **Zone:** Boundless Void.

Elk does not hate the Expeditions that pass through Boundless Void; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Elk* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Panther — STUB

*Tiny Plant, True Neutral.* **Challenge 1/2** (100 XP). **Zone:** Bastion of Flame.

Root, spore, and vine answer to Panther across more of Bastion of Flame than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Panther* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Peryton — STUB

*Small Plant, Neutral Good.* **Challenge 1/2** (100 XP). **Zone:** Bastion of Flame.

Peryton does not hate the Expeditions that pass through Bastion of Flame; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Peryton* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sporefolk Sprout

*Small Plant, Lawful Good.* **Challenge 1/2** (100 XP). **Zone:** Planar Crossroads.

Sporefolk Sprout does not hate the Expeditions that pass through Planar Crossroads; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Tortle Druid — STUB

*Small Plant, Neutral Good.* **Challenge 1/2** (100 XP). **Zone:** Aethel Lakes.

Aethel Lakes's bloom cycles produced Tortle Druid the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Tortle Druid* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Shellkin Warden* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d6+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Treant

*Small Plant, Neutral Good.* **Challenge 1/2** (100 XP). **Zone:** Boundless Void.

Boundless Void's bloom cycles produced Treant the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **31** instead of **26**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 12 · **Hit Points** 31 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +4 to hit — 1d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Astral Reaver Knight — STUB

*Medium Plant, Neutral Good.* **Challenge 1** (200 XP). **Zone:** Bastion of Flame.

Root, spore, and vine answer to Astral Reaver Knight across more of Bastion of Flame than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — Director must re-skin.** The name *Astral Reaver Knight* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Astral Reaver concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Crab — STUB

*Medium Plant, True Neutral.* **Challenge 1** (200 XP). **Zone:** Aethel Deserts.

Crab grew where Aethel Deserts should have stayed empty, and kept growing past the point anyone could stop it politely. Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest. Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.

> **STUB — Director must re-skin.** The name *Crab* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ghoul — STUB

*Large Plant, Chaotic Neutral.* **Challenge 1** (200 XP). **Zone:** Shardpools.

Shardpools's bloom cycles produced Ghoul the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Ghoul* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +4 to hit — 1d8+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Star Spawn Hulk — STUB

*Medium Plant, Lawful Good.* **Challenge 1** (200 XP). **Zone:** Radiant Isles.

Star Spawn Hulk does not hate the Expeditions that pass through Radiant Isles; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Star Spawn Hulk* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Star Spawn family; proposed: *Spiral Breach Hulk*. Owner-flagged: full Aethel rewrite or 'Spiral breach echo' ecology stub.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **52** instead of **40**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 52 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +4 to hit — 1d8+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Crawling Claw — STUB

*Large Plant, Neutral Evil.* **Challenge 2** (450 XP). **Zone:** Aethel Tundra.

Crawling Claw does not hate the Expeditions that pass through Aethel Tundra; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Crawling Claw* reads as **Undead** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Death Slaad — STUB

*Small Plant, Neutral Good.* **Challenge 2** (450 XP). **Zone:** Aethel Highlands.

Root, spore, and vine answer to Death Slaad across more of Aethel Highlands than any single map admits. Cutting the visible threat rarely solves the root problem — literally, in {zone}. Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Death Chaos-Husk*. Invented planar-race terminology; needs Aethel identity.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 1d10+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Dwarf — STUB

*Medium Plant, Neutral Good.* **Challenge 2** (450 XP). **Zone:** Yieldheart.

Deep Dwarf does not hate the Expeditions that pass through Yieldheart; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> **STUB — Director must re-skin.** The name *Deep Dwarf* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Plant**) was randomized independently of the Deep Dwarf concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Salamander — STUB

*Medium Plant, Neutral Evil.* **Challenge 2** (450 XP). **Zone:** Shardpools.

Shardpools's bloom cycles produced Salamander the way a wound produces scar tissue — necessary, ugly, permanent. It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs. A Support team's antidotes and cleared sightlines matter more here than raw damage output.

> **STUB — Director must re-skin.** The name *Salamander* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Plant** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 1d10+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### The Bloom That Hungers

*Gargantuan Plant, Chaotic Evil.* **Challenge 5** (1800 XP). **Zone:** Planar Crossroads.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 15 · **Hit Points** 112 · **Speed** 20 ft., burrow 30 ft.

**Abilities** STR 18 · DEX 12 · CON 16 · INT 8 · WIS 14 · CHA 10

**Skills** Perception +5, Stealth +4

**Senses** Tremorsense 60 ft., passive Perception 15

**Languages** —

**Attacks**
- **Vine Maw** — +6 to hit — 2d8+4 piercing
- **Spore Burst** (Recharge 6-6) — 1d8 poison, 20-ft. radius — constitution save DC 14 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Sporefolk Adult

*Large Plant, Lawful Neutral.* **Challenge 14** (11500 XP). **Zone:** Shardpools.

Sporefolk Adult does not hate the Expeditions that pass through Shardpools; it simply metabolizes them. It reacts to fire and light with something close to fear, if fear is the right word for a plant. Use it to make retreat a real, costed choice instead of a free action.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d8+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


## The Undead

The Undead of Aethel are history that refused to stay buried, in the most literal sense the Decennium offers. Whatever ended a given Undead's first life rarely ended its business here, and most repeat a pattern from that life — a duty, a grudge, a routine — with none of the judgment that once tempered it. **Player knowledge** should feel the necrotic and fear pressure these encounters are built to apply: exhaustion, dread, and morale cost should be as real as hit point loss. **Director knowledge** treats an Undead's unfinished business, once learned, as frequently the actual quest, with the fight itself only a symptom. Let its remains carry at least one true clue toward why it rose, even in an otherwise minor encounter, and remember that turning or destroying it does not always end whatever compelled it to rise in the first place.

*Indexed creatures of this family: **58**.*

### Aarakocra — STUB

*Tiny Undead, Chaotic Good.* **Challenge 0** (10 XP). **Zone:** Null Zones.

Whatever ended Aarakocra's first life did not end its business in Null Zones. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Aarakocra* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Proposed Aethel name: *Skyfolk of the High Vents* (not yet locked — see Naming & IP Reskin Ledger).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*
- **Grave Shriek** (Recharge 6-6) — 1d6 necrotic, 20-ft. radius — wisdom save DC 10 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Abjurer — STUB

*Tiny Undead, Unaligned.* **Challenge 0** (10 XP). **Zone:** Aethel Caves.

Aethel Caves keeps its dead close, and Abjurer is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Abjurer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Necromancer — STUB

*Tiny Undead, Neutral Good.* **Challenge 0** (10 XP). **Zone:** Null Zones.

Whatever ended Necromancer's first life did not end its business in Null Zones. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Necromancer* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vampire (warrior)

*Tiny Undead, Neutral Evil.* **Challenge 0** (10 XP). **Zone:** Aethel Caves.

Aethel Caves keeps its dead close, and Vampire (warrior) is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **9** instead of **7**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 10 · **Hit Points** 9 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Armanite — STUB

*Tiny Undead, Lawful Neutral.* **Challenge 1/8** (25 XP). **Zone:** Veiled Expanse.

Armanite is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** The name *Armanite* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Demon rank family; proposed: *Fracture-Kin (Armanite rank)*. Invented chaotic-fiend hierarchy; fold into Aethel 'Fracture-Kin' Chaos-Realm ranks.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Elephant — STUB

*Tiny Undead, Neutral Good.* **Challenge 1/8** (25 XP). **Zone:** Null Zones.

Whatever ended Elephant's first life did not end its business in Null Zones. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Elephant* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mummy Lord

*Tiny Undead, Chaotic Evil.* **Challenge 1/8** (25 XP). **Zone:** Null Zones.

Mummy Lord is history in Null Zones that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +3 to hit — 1d4+1 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Pony — STUB

*Tiny Undead, Unaligned.* **Challenge 1/8** (25 XP). **Zone:** Aethel Caves.

Whatever ended Pony's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Pony* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Specter

*Tiny Undead, Neutral Evil.* **Challenge 1/8** (25 XP). **Zone:** Aethel Caves.

Whatever ended Specter's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **12** instead of **9**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 11 · **Hit Points** 12 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +3 to hit — 1d4+1 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Marut — STUB

*Medium Undead, Unaligned.* **Challenge 2** (450 XP). **Zone:** Veiled Expanse.

Veiled Expanse keeps its dead close, and Marut is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Marut* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Modron rank family; proposed: *Order-Drone (Marut rank)*. Invented lawful-construct hierarchy; fold into Aethel 'Order-Drone' clockwork sect.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **68** instead of **50**.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +5 to hit — 1d10+2 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ghost

*Medium Undead, Unaligned.* **Challenge 3** (700 XP). **Zone:** Aethel Caves.

Ghost remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Monstrous Claw* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** — +5 to hit — 2d6+2 slashing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gray Slaad — STUB

*Medium Undead, Lawful Good.* **Challenge 3** (700 XP). **Zone:** Aethel Caves.

Gray Slaad is history in Aethel Caves that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — stock alias, Director must re-skin.** Part of the Slaad family; proposed: *Gray Chaos-Husk*. Invented planar-race terminology; needs Aethel identity.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vampire

*Medium Undead, Lawful Evil.* **Challenge 3** (700 XP). **Zone:** Null Zones.

Vampire remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: Excel's own `NeedsReview` column flags Hit Points as likely low — sandbox suggests **88** instead of **63**.

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 88 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +5 to hit — 2d6+2 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vine Blight — STUB

*Small Undead, Neutral Evil.* **Challenge 4** (1100 XP). **Zone:** Veiled Expanse.

Whatever ended Vine Blight's first life did not end its business in Veiled Expanse. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Vine Blight* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attack *Aberrant Lash* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d6+3 acid *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Warhorse Skeleton — STUB

*Medium Undead, Unaligned.* **Challenge 4** (1100 XP). **Zone:** Aethel Caves.

Whatever ended Warhorse Skeleton's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Medium** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attack *Freak Bite* is reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 14 · **Hit Points** 75 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** — +6 to hit — 2d6+3 piercing *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Autumn Eladrin — STUB

*Medium Undead, Neutral Good.* **Challenge 5** (1800 XP). **Zone:** Veiled Expanse.

Autumn Eladrin remembers a version of Veiled Expanse that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Autumn Eladrin* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — stock alias, Director must re-skin.** Part of the Eladrin (season) family; proposed: *Autumn Season-Bound*. Setting-specific fey-noble term tied to an external calendar cosmology.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 95 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** — +6 to hit — 2d8+4 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +6 to hit — 2d8+3 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grell — STUB

*Medium Undead, Neutral Good.* **Challenge 7** (2900 XP). **Zone:** Null Zones.

Whatever ended Grell's first life did not end its business in Null Zones. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Grell* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 15 · **Hit Points** 123 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +7 to hit — 2d8+5 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +7 to hit — 2d8+4 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Death Knight

*Medium Undead, Lawful Evil.* **Challenge 10** (5900 XP). **Zone:** Veiled Expanse.

Death Knight remembers a version of Veiled Expanse that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 2d10+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Yeth Hound — STUB

*Large Undead, Lawful Neutral.* **Challenge 10** (5900 XP). **Zone:** Veiled Expanse.

Yeth Hound is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** The name *Yeth Hound* reads as **Fiend** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Large** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 172 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +8 to hit — 2d10+6 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Deep Rothe — STUB

*Huge Undead, Chaotic Evil.* **Challenge 11** (7200 XP). **Zone:** Veiled Expanse.

Deep Rothe remembers a version of Veiled Expanse that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Deep Rothe* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 187 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +8 to hit — 2d10+6 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 2d10+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Cave Fisher

*Huge Undead, True Neutral.* **Challenge 12** (8400 XP). **Zone:** Aethel Caves.

Aethel Caves keeps its dead close, and Cave Fisher is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 17 · **Hit Points** 202 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Brontosaurus — STUB

*Huge Undead, Neutral Evil.* **Challenge 13** (10000 XP). **Zone:** Null Zones.

Brontosaurus remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Brontosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 217 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +8 to hit — 3d8+6 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +8 to hit — 3d8+5 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Death Dog — STUB

*Huge Undead, Neutral Good.* **Challenge 14** (11500 XP). **Zone:** Null Zones.

Death Dog remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Death Dog* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d8+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gas Spore — STUB

*Large Undead, Unaligned.* **Challenge 14** (11500 XP). **Zone:** Veiled Expanse.

Veiled Expanse keeps its dead close, and Gas Spore is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Gas Spore* reads as **Plant** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d8+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ogre Zombie — STUB

*Huge Undead, Neutral Good.* **Challenge 14** (11500 XP). **Zone:** Aethel Caves.

Whatever ended Ogre Zombie's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d8+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Scarecrow — STUB

*Large Undead, True Neutral.* **Challenge 14** (11500 XP). **Zone:** Null Zones.

Scarecrow is history in Null Zones that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** The name *Scarecrow* reads as **Construct** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 232 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x2) — +9 to hit — 3d8+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d8+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Adult Blue Dracolich

*Huge Undead, Unaligned.* **Challenge 15** (13000 XP). **Zone:** Veiled Expanse.

Adult Blue Dracolich is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*
- **Lightning Breath** (Recharge 5-6) — 8d10 lightning, 20-ft. radius — dexterity save DC 19 (half on success)

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Angry Sorrowsworn — STUB

*Huge Undead, Neutral Good.* **Challenge 15** (13000 XP). **Zone:** Veiled Expanse.

Angry Sorrowsworn remembers a version of Veiled Expanse that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — stock alias, Director must re-skin.** Part of the Sorrowsworn family; proposed: *Angry Grief-Bound*. Invented emotion-fey terminology; safe to rename without losing concept.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x2) — +9 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Skeleton

*Huge Undead, Chaotic Good.* **Challenge 15** (13000 XP). **Zone:** Veiled Expanse.

Skeleton is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 247 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x2) — +9 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vampire Spawn — STUB

*Huge Undead, Lawful Evil.* **Challenge 16** (15000 XP). **Zone:** Aethel Caves.

Whatever ended Vampire Spawn's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 18 · **Hit Points** 262 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +9 to hit — 3d10+7 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +9 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lumen of the Shattered Thread

*Large Undead, True Neutral.* **Challenge 17** (18000 XP). **Zone:** Aethel Caves.

**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.

**Armor Class** 19 · **Hit Points** 255 · **Speed** 40 ft., fly 80 ft.

**Abilities** STR 20 · DEX 18 · CON 18 · INT 18 · WIS 20 · CHA 24

**Skills** Insight +11, Perception +11, Religion +10

**Senses** Truesight 120 ft., passive Perception 21

**Languages** All, telepathy 120 ft.

**Attacks**
- **Thread Lance** (x2) — +10 to hit — 3d8+5 radiant
- **Thread Shatter** (Recharge 5-6) — 6d10 force, 20-ft. radius — dexterity save DC 18 (half on success)

*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*

### Wight

*Large Undead, Chaotic Neutral.* **Challenge 17** (18000 XP). **Zone:** Null Zones.

Wight remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 277 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Magmin — STUB

*Huge Undead, Chaotic Evil.* **Challenge 18** (20000 XP). **Zone:** Veiled Expanse.

Whatever ended Magmin's first life did not end its business in Veiled Expanse. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Magmin* reads as **Elemental** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d10+7 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Voidmind Lich — STUB

*Huge Undead, Unaligned.* **Challenge 18** (20000 XP). **Zone:** Veiled Expanse.

Voidmind Lich is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** The name *Voidmind Lich* reads as **Aberration** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Undead**) was randomized independently of the Voidmind concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 292 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d10+7 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d10+6 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Ankylosaurus — STUB

*Huge Undead, Chaotic Neutral.* **Challenge 19** (22000 XP). **Zone:** Null Zones.

Ankylosaurus remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Ankylosaurus* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +10 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Apprentice Wizard — STUB

*Huge Undead, Chaotic Neutral.* **Challenge 19** (22000 XP). **Zone:** Null Zones.

Null Zones keeps its dead close, and Apprentice Wizard is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Apprentice Wizard* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Gaze Tyrant Husk — STUB

*Huge Undead, True Neutral.* **Challenge 19** (22000 XP). **Zone:** Null Zones.

Null Zones keeps its dead close, and Gaze Tyrant Husk is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Undead**) was randomized independently of the Gaze Tyrant concept. Treat as **Aberration** regardless of the sheet field.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +10 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mummy Lord (in lair) — STUB

*Huge Undead, Unaligned.* **Challenge 19** (22000 XP). **Zone:** Veiled Expanse.

Whatever ended Mummy Lord (in lair)'s first life did not end its business in Veiled Expanse. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Huge** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 307 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +10 to hit — 3d12+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +10 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Frog — STUB

*Huge Undead, Chaotic Evil.* **Challenge 20** (25000 XP). **Zone:** Aethel Caves.

Whatever ended Frog's first life did not end its business in Aethel Caves. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Frog* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Mummy — STUB

*Gargantuan Undead, Chaotic Good.* **Challenge 20** (25000 XP). **Zone:** Veiled Expanse.

Veiled Expanse keeps its dead close, and Mummy is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 19 · **Hit Points** 322 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Demilich (in lair) — STUB

*Gargantuan Undead, Unaligned.* **Challenge 21** (33000 XP). **Zone:** Null Zones.

Demilich (in lair) is history in Null Zones that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 3d12+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lich (in lair) — STUB

*Gargantuan Undead, Chaotic Evil.* **Challenge 21** (33000 XP). **Zone:** Aethel Caves.

Lich (in lair) is history in Aethel Caves that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 337 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +11 to hit — 3d12+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 3d12+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Male Steeder — STUB

*Gargantuan Undead, Chaotic Neutral.* **Challenge 22** (41000 XP). **Zone:** Aethel Caves.

Male Steeder is history in Aethel Caves that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** The name *Male Steeder* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 352 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +11 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +11 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Demilich — STUB

*Gargantuan Undead, Neutral Evil.* **Challenge 23** (50000 XP). **Zone:** Aethel Caves.

Demilich remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Serpent-Blood Pit Master — STUB

*Gargantuan Undead, Unaligned.* **Challenge 23** (50000 XP). **Zone:** Veiled Expanse.

Whatever ended Serpent-Blood Pit Master's first life did not end its business in Veiled Expanse. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** The name *Serpent-Blood Pit Master* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Culture-family entry; sheet Type (**Undead**) was randomized independently of the Serpent-Blood concept. Treat as **Humanoid** regardless of the sheet field.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d10+8 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sword Wraith Commander — STUB

*Gargantuan Undead, Neutral Good.* **Challenge 23** (50000 XP). **Zone:** Veiled Expanse.

Sword Wraith Commander is history in Veiled Expanse that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 20 · **Hit Points** 367 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +12 to hit — 4d10+8 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Lich — STUB

*Gargantuan Undead, Chaotic Good.* **Challenge 24** (62000 XP). **Zone:** Aethel Caves.

Lich remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 382 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +12 to hit — 4d10+8 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d10+7 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Sword Wraith Warrior — STUB

*Gargantuan Undead, Unaligned.* **Challenge 25** (75000 XP). **Zone:** Null Zones.

Sword Wraith Warrior remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 397 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Wraith

*Gargantuan Undead, True Neutral.* **Challenge 25** (75000 XP). **Zone:** Aethel Caves.

Wraith remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 397 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +12 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +12 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Specter (poltergeist) — STUB

*Gargantuan Undead, Neutral Evil.* **Challenge 26** (90000 XP). **Zone:** Null Zones.

Whatever ended Specter (poltergeist)'s first life did not end its business in Null Zones. It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it. Its unfinished business, once learned, is often the actual quest — the fight is a symptom.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Medium**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Zombie — STUB

*Gargantuan Undead, Lawful Neutral.* **Challenge 26** (90000 XP). **Zone:** Aethel Caves.

Zombie remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 21 · **Hit Points** 412 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Axe Beak — STUB

*Gargantuan Undead, Neutral Good.* **Challenge 27** (105000 XP). **Zone:** Null Zones.

Null Zones keeps its dead close, and Axe Beak is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Axe Beak* reads as **Beast** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Grimlock — STUB

*Huge Undead, Chaotic Neutral.* **Challenge 27** (105000 XP). **Zone:** Null Zones.

Grimlock remembers a version of Null Zones that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Grimlock* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Satyr — STUB

*Gargantuan Undead, Chaotic Evil.* **Challenge 27** (105000 XP). **Zone:** Aethel Caves.

Satyr remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Satyr* reads as **Fey** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Small**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Vampire (spellcaster)

*Gargantuan Undead, True Neutral.* **Challenge 27** (105000 XP). **Zone:** Veiled Expanse.

Vampire (spellcaster) remembers a version of Veiled Expanse that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 427 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Minotaur Skeleton — STUB

*Gargantuan Undead, Neutral Evil.* **Challenge 28** (120000 XP). **Zone:** Null Zones.

Minotaur Skeleton is history in Null Zones that refused to stay buried, in the most literal sense available. Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical. Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Freak Bite*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 442 · **Speed** 40 ft.

**Attacks**
- **Freak Bite** (x3) — +13 to hit — 4d12+9 piercing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Quaggoth Spore Servant — STUB

*Gargantuan Undead, Chaotic Evil.* **Challenge 28** (120000 XP). **Zone:** Aethel Caves.

Quaggoth Spore Servant remembers a version of Aethel Caves that no living Expedition member has ever seen. It does not negotiate with the living, only occasionally with itself, out loud, in fragments. Use it to remind a table that some floors of the Decennium are, quite literally, graves.

> **STUB — Director must re-skin.** The name *Quaggoth Spore Servant* reads as **Humanoid** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Tiny**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Monstrous Claw*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 442 · **Speed** 40 ft.

**Attacks**
- **Monstrous Claw** (x3) — +13 to hit — 4d12+9 slashing *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*

### Zaratan — STUB

*Gargantuan Undead, Chaotic Good.* **Challenge 28** (120000 XP). **Zone:** Veiled Expanse.

Veiled Expanse keeps its dead close, and Zaratan is proof that 'close' is not the same as 'quiet.' Turning or destroying it does not always end whatever compelled it to rise in the first place. Let its remains carry one true clue to why it rose, even in a throwaway encounter.

> **STUB — Director must re-skin.** The name *Zaratan* reads as **Monstrosity** in ordinary Aethel usage, but the sheet lists Type **Undead** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).

> **STUB — Director must re-skin.** Excel's own `NeedsReview` column flags Size: sandbox suggests **Gargantuan** instead of the sheet's **Large**, and Challenge Rating looks suspiciously high for the sheet's current Size.

> Draft note: attacks *Aberrant Lash*, *Tail Lash* are reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.

**Armor Class** 22 · **Hit Points** 442 · **Speed** 40 ft.

**Attacks**
- **Aberrant Lash** (x3) — +13 to hit — 4d12+9 acid *[provisional attack name — generic sandbox filler]*
- **Tail Lash** — +13 to hit — 4d12+8 bludgeoning *[provisional attack name — generic sandbox filler]*

*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*


---

# Part IV — Floor Cultures & Humanoid Deep Dives

Not every Humanoid entry in the Lexicon is a fight waiting to happen. The families below have enough internal structure — ranks, courts, rivalries — to function as recurring political actors across a Cycle rather than one-off encounters. Directors are encouraged to treat first contact with any of these cultures as a conversation option, not just an initiative roll.

## The Umbrin

Deep-folk of the Bloomdeep tiers, the Umbrin organize around Houses bound by spider-cult hierarchy: Matrons at the top, Favored Consorts and House Captains beneath them, Inquisitors policing doctrine, and Elite Warriors and Shadowblades doing the actual killing. **Director naming note:** *Umbrin* replaces the retired stock alias formerly used for this culture in Director materials — use Umbrin exclusively at the table going forward. Their politics run on obligation and betrayal in roughly equal measure; an Expedition that survives contact with one House often finds itself, whether it wants to or not, an asset in that House's feud with another.

*Data honesty note:* the sheet currently assigns wildly inconsistent Types and Sizes across the ten Umbrin entries (ranging from Beast to Construct to Celestial, Tiny to Gargantuan) because each row was generated independently rather than as a coherent culture. Every Umbrin entry should be read as **Humanoid**, roughly Medium, regardless of what its individual sheet row claims — see the Lexicon entries for the specific per-row flag.

## The Deep Dwarf

Where Umbrin politics run on doctrine, Deep Dwarf politics run on rank and debt. Despots and Warlords command; Hammerers, Stone Guards, and Xarrorn enforce; Mind Masters and Soulblades handle the parts of deep-dwarf warfare that aren't purely physical. **Director naming note:** *Deep Dwarf* replaces the retired stock alias for this culture. Treat every Deep Dwarf entry as **Humanoid** regardless of its individual sheet Type — the same randomization problem affecting the Umbrin affects this family as well.

## The Astral Reaver and Astral Ascetic courts

Two mirror-image philosophies descended from the same shattered origin: Astral Reavers (Knights, Spellblades, War-Captains, and a Supreme Commander) pursue conquest and certainty through force; Astral Ascetics (Monks, Sentinels, the Enlightened, and rare Anarchs) pursue the same certainty through discipline and withdrawal. **Director naming note:** these names replace two retired stock aliases; use Astral Reaver / Astral Ascetic exclusively. The two courts' rivalry is old enough that most individual members have stopped remembering why it started — which makes them useful as a Director tool for introducing conflict an Expedition did not create and cannot easily resolve by force alone.

## The Serpent-Blood bloodlines

A cline of increasingly inhuman ranks — Pureblood, Malison, Broodguard, Nightmare Speaker, Pit Master, Anathema, Abomination, Mind Whisperer — that reads as much like a spectrum of transformation as a fixed hierarchy. **Director naming note:** *Serpent-Blood* replaces the retired stock alias for this culture. Treat encounters with lower-rank Serpent-Blood as potential Humanoid social contact; higher ranks (Anathema, Abomination) should be played as having largely lost whatever diplomacy the bloodline once had.

## The Depth Toad clergy

A small but coherent religious hierarchy (Archpriest, Taskmaster, and common Depth Toad) built around whatever the Aethel Oceans and Lakes zones' deep currents actually worship. **Director naming note:** *Depth Toad* replaces the retired stock alias for this culture. Their theology is deliberately left undefined in this Codex — Directors are encouraged to invent a specific patron current, tide, or drowned court as needed, rather than importing any external deity concept.

## Orc, gnoll, and firenewt warband ranks (deity-lock scrub)

Several warband rank-names in the sheet are still built around a named foreign deity lock (a specific god a warrior is dedicated to). Per Continuity C's IP scrub, **Decennium Descent does not lock any monster identity to a foreign product's deity name.** The table below gives the sheet's current name, why it is flagged, and the proposed Aethel-native rank this Codex uses in its own prose (final naming pending owner sign-off — see the Naming & IP Reskin Ledger):

| Sheet name | Flag | Codex-proposed Aethel rank |
|---|---|---|
| Gnoll Fang of Yeenoghu | Foreign deity lock | Gnoll Fang of the Howling Fracture |
| Orc Blade of Ilneval | Foreign deity lock | Orc Blade of the Iron March |
| Orc Eye of Gruumsh | Foreign deity lock | Orc Eye of the One-Eyed Pact |
| Orc Hand of Yurtrus | Foreign deity lock | Orc Hand of the Rot Sigil |
| Orc Nurtured One of Yurtrus | Foreign deity lock | Orc Nurtured One of the Rot Sigil |
| Orc Red Fang of Shargaas | Foreign deity lock | Orc Red Fang of the Veiled Hunt |
| Orc Claw of Luthic | Foreign deity lock | Orc Claw of the Den-Mother |
| Spawn of Kyuss | Foreign deity lock | Spawn of the Worm Spiral |
| Firenewt Warlock of Imix | Foreign deity lock | Firenewt Warlock of the Ember Court |
| Xvart Warlock of Raxivort | Foreign deity lock | Xvart Warlock of the Nine-Legged Choir |

None of these are official Fifteenfold names — they are working Codex labels only, meant to demonstrate that a deity-free rank name is easy to write. Treat "the Iron March," "the One-Eyed Pact," "the Rot Sigil," "the Veiled Hunt," "the Den-Mother," "the Worm Spiral," "the Ember Court," and "the Nine-Legged Choir" as placeholder cult names, not locked cosmology — the Cosmology continuity thread owns final naming authority here.

## Generic floor classes

A large share of the Humanoid lexicon (Bandit, Guard, Veteran, Cultist, Cult Fanatic, Scout, Thug, Knight, Mage, Priest, Noble, Assassin, Gladiator, Spy, Archer, and the named spellcasting specialists like Diviner, Evoker, Necromancer, and Conjurer) are not a single culture at all — they are **floor-class templates**: reusable NPC statistics meant to be reskinned as whichever faction, cult, or mercenary company a Director needs on a given floor. Give them a faction name and a one-line motive before combat starts, and they stop feeling like reused sandbox rows.


---

# Part V — The Director's Toolkit

## DIY Monster: the quick method

Most floors do not need a full Excel row before a Director can run a creature. Use this five-step method for anything improvised at the table, and only open the spreadsheet afterward if the creature is going to recur:

1. **Pick a role, not a species.** Bruiser (soaks hits, hits back), skirmisher (mobile, punishes stragglers), controller (area denial, terrain manipulation), artillery (range, low durability), or leader (buffs/commands lesser threats). Everything else is decoration on top of the role.
2. **Borrow the nearest Challenge Rating band.** Find an existing Lexicon entry within one CR of the encounter budget you want and reuse its Armor/HP/attack-bonus numbers wholesale. Do not invent numbers from scratch at the table — draft numbers borrowed honestly beat improvised numbers guessed under pressure.
3. **Give it exactly one tell.** A sound, a smell, a heat shimmer, a way it moves that a Recon-minded player can notice and exploit. One tell is memorable; three tells are a checklist nobody uses.
4. **Mark the numbers provisional out loud.** Tell the table "this is a draft stat block, treat the numbers as fair but not fixed" — this is not a confession of failure, it is how every entry in this Codex is labeled internally.
5. **Decide what its death changes.** A drop that seeds surface trouble, a faction that notices, a floor culture whose patrol routes shift — every creature killed for good should leave one loose thread behind, even an improvised one.

**When to open Excel instead:** if the creature is going to appear more than once, if it is a Gate Guardian-tier set piece, or if its loot needs to interact with the crafting sheets (Drops, Crafting Materials, Drop Locations), write it into `Bestiary.xlsx` properly and re-ingest before the next session rather than carrying it as table-only improv indefinitely.

## Lair omens: telegraphing before the fight

Every Gate Seal chapter in Part II uses omens deliberately — this is the general method behind that pattern, usable for any recurring threat:

- **Environmental drift.** Something about the room is subtly wrong before the creature is present: temperature, sound, light quality, the behavior of mundane animals nearby. Let players notice this on a passive check, not an active roll — omens that require asking for them defeat the purpose.
- **Secondhand account.** A floor culture, a rival Expedition's survivor, or a research fragment describes an earlier, failed encounter. This is cheaper than a live omen and doubles as worldbuilding.
- **Escalating minor encounters.** Two or three weaker fights that are thematically or literally connected to the coming set piece (outriders, spawn, patrol units) — see how The Bloom That Hungers's root-graspers or Vaskor's Automaton-avoidance zone work in Part II.
- **A real cost for ignoring the omen.** If nothing changes whether the party heeds the warning or not, it was never really an omen — it was flavor text. Attach at least a small, concrete consequence (resource cost, positioning disadvantage, a Support team's supplies running short) to skipping past the warning signs.
- **A retreat that is genuinely available.** An omen without an exit is a trap disguised as foreshadowing. Every seal in Part II assumes the party could, in principle, turn back after the omens — the story is that most don't.

## Random pressure by tier

These are seeds, not fixed encounter tables — roll or pick, then reskin with the specific floor culture, hazard, or Gate Guardian material already established for that tier in the Chronicle of the Decennial Opening.

| Tier | d6 | Pressure seed |
|---|---|---|
| **1 — Yieldheart Caverns** | 1–2 | An Automaton patrol treats the party as unauthorized past its usual boundary |
| | 3–4 | A ward-surge from the Warded Gate's glyph puzzle triggers early |
| | 5–6 | A rival salvage crew claims a Luminous Vein first and disputes the party's cut |
| **2 — Bloomdeep Marsh** | 1–2 | A spore timer forces a decision: press on or lose visibility |
| | 3–4 | The Phantom Mire's false-shallow floor swallows equipment, not just footing |
| | 5–6 | A false signal through the Reedcaller's Circle draws the party off-route |
| **3 — Anvil of Brogi** | 1–2 | Slag rain forces a scramble for cover mid-corridor |
| | 3–4 | The Chained Anvil's swing window is tighter than the last pass through |
| | 5–6 | Heat exhaustion becomes a genuine resource drain, not flavor text |
| **4 — Isles of Eternal Radiance** | 1–2 | A Mirror Reef double convinces the party it is fighting itself |
| | 3–4 | A light-sprite attempts to steal a charged sun-shard vial mid-transport |
| | 5–6 | A sun-shield or dawn-glow tonic fails at the worst possible moment |
| **5 — Sanctum of Echoing Choirs** | 1–2 | An Echoing Pillar replays a fragment of an earlier failed Expedition |
| | 3–4 | A pocket of total silence disables verbal spellcasting without warning |
| | 5–6 | Morale event: someone in the party seriously proposes turning back — resolve it in fiction |
| **6 — Crossroads of the Shattered Thread** | 1–2 | Path Recall erases the party's own footprints mid-retreat |
| | 3–4 | A Weave-Snap causes brief, disorienting planar shear |
| | 5–6 | Lantern Doubt leads the party to refight a corridor they already cleared |
| **7 — Pactbound Arena** | 1–2 | A mid-fight "bargain" offer binds unpredictably if accepted |
| | 3–4 | A defeated foe's oath replays as a hostile echo one floor later |
| | 5–6 | Blood-Tally rumor makes a wound feel like currency being spent |
| **8 — Duskshard Pools** | 1–2 | Dusk Inversion swaps light and shadow mid-encounter |
| | 3–4 | A basin's reflection shows a different, worse version of the coming fight |
| | 5–6 | Prayer Rust corrodes a piece of gear faster than expected |
| **9 — Veiled Iron Spiral** | 1–2 | Coil Tighten makes distance itself feel withheld |
| | 3–4 | Rail-Vanish erases the last bend from memory, forcing a navigation check |
| | 5–6 | Shadow Trade disorients a scout mid-Recon |
| **10 — Silencebound Void** | 1–2 | Sound Theft fails a spell or shout with no warning |
| | 3–4 | Void Lean pulls gravity toward an unseen center |
| | 5–6 | An Unasked Question makes the party's own unspoken doubts feel audible |

Tiers 6–10 are explicitly marked **draft / unmapped** in the Chronicle gazetteer — present all pressure seeds above as survivor rumor, not confirmed geography, until that continuity thread ships confirmed maps.

## Appendix: Conditions

A short, Decennium-native glossary of the status conditions this Codex's combat lines assume. These are generic tabletop-fantasy terms, defined here in Decennium Descent's own words — cross-reference the Player Rulebook for any player-facing mechanical resolution; this list is a Director quick-reference only.

| Condition | Effect (Director quick-reference) |
|---|---|
| **Blinded** | Cannot see; automatically fails sight-based checks and treats all attackers as unseen. |
| **Charmed** | Cannot attack the charmer and treats their words with unwarranted trust. |
| **Deafened** | Cannot hear; automatically fails hearing-based checks. |
| **Exhaustion** | Escalating tiers of cumulative penalty, worst at the top; rest and care remove it in tiers, not all at once. |
| **Frightened** | Cannot willingly approach the source of fear and suffers a penalty while it is in sight. |
| **Grappled** | Speed becomes zero; ends if the grappler is incapacitated or the target is forcibly moved away. |
| **Incapacitated** | Cannot take actions or reactions. |
| **Invisible** | Unseen; attackers are at a disadvantage, the invisible creature at an advantage. |
| **Paralyzed** | Incapacitated and unable to move or speak; attacks against it land unusually hard. |
| **Petrified** | Transformed to inert stone-like substance; incapacitated and effectively immune to most further harm while in this state. |
| **Poisoned** | A general penalty to effectiveness, distinct from ongoing poison damage. |
| **Prone** | Only able to crawl unless it stands; attackers nearby have an easier time, ranged attackers a harder one. |
| **Restrained** | Speed becomes zero; both the restrained creature and its attackers trade accuracy for the situation. |
| **Stunned** | Incapacitated, cannot move, and can barely speak. |
| **Unconscious** | Incapacitated, unaware, and drops anything held; treated as prone for attack purposes. |

## Naming & IP Reskin Ledger

This Codex does not silently mass-edit `Bestiary.xlsx`. The rename table below is a **proposal for the next Excel pass**, matching Continuity C's IP scrub findings — until the owner signs off, the sheet's current names remain canon and every affected Lexicon entry below carries an individual STUB flag rather than a silent substitution.

### Already resolved in the current data (no action needed)

These culture families were already reskinned to their Aethel names in the current `bestiary_data_full.json` ingest — the retired stock aliases no longer appear anywhere in the live dataset. Use the Aethel name exclusively at the table.

| Aethel canon (live, in use) | Retired stock alias (no longer in the dataset) |
|---|---|
| Umbrin | *(retired drow-adjacent alias)* |
| Gaze Tyrant | *(retired beholder-adjacent alias)* |
| Voidmind | *(retired mind-flayer-adjacent alias)* |
| Depth Toad | *(retired kuo-toa-adjacent alias)* |
| Deep Dwarf | *(retired duergar-adjacent alias)* |
| Serpent-Blood | *(retired yuan-ti-adjacent alias)* |
| Sporefolk | *(retired myconid-adjacent alias)* |
| Astral Reaver | *(retired githyanki-adjacent alias)* |
| Astral Ascetic | *(retired githzerai-adjacent alias)* |

**Umbrin** — deep-folk of the Bloomdeep; replaces the retired stock alias formerly used in Director materials. This note is placed here, on first mention, per Continuity C's requested lexicon convention.

### Still stock — proposed renames awaiting owner sign-off

| Sheet name (current, unchanged) | Codex-proposed Aethel name | Family |
|---|---|---|
| Flumph | Lumen Drifter | Single |
| Owlbear | Hookbeast | Single |
| Tarrasque | Worldbreaker | Single |
| Intellect Devourer | Mind Leech | Single |
| Neothelid | Spiral Worm | Single |
| Draegloth | Umbrin Warborn | Single |
| Drider | Umbrin Arachnid | Single |
| Displacer Beast | Refractor Panther | Single |
| Hook Horror | Rip-Auger | Single |
| Umber Hulk | Deep Borer | Single |
| Rust Monster | Corrosion Grazer | Single |
| Carrion Crawler | Charnel Crawler | Single |
| Aarakocra | Skyfolk of the High Vents | Single |
| Kenku | Mimic-Crow | Single |
| Tortle / Tortle Druid | Shellkin / Shellkin Warden | Single |
| Grung (+ ranks) | Poison-Skin (+ matching ranks) | Single |
| Thri-kreen | Chitin-Strider | Single |
| Bullywug | Bogkin | Single |
| Merrenoloth | Ferry-Wraith of the Hush | Yugoloth |
| Ultroloth | Court Broker of the Hush | Yugoloth |
| Arcanaloth, Canoloth, Dhergoloth, Hydroloth, Mezzoloth, Nycaloth, Oinoloth, Yagnoloth | Hush-Broker (rank-named) | Yugoloth |
| Duodrone, Monodrone, Pentadrone, Quadrone, Tridrone, Marut | Order-Drone (rank-named) | Modron |
| Balor, Marilith, Glabrezu, Nalfeshnee, Vrock, Hezrou, Babau, Dretch, Manes, Molydeus, Nabassu, Goristro, Yochlol, Armanite, Bulezau, Shoosuva, Maurezhi, Alkilith, Wastrilith, Sibriex | Fracture-Kin (rank-named) | Demon hierarchy |
| Black/Blue/Green/Red/White Abishai | Pact Devil (colored by Chaos-Realm court) | Abishai |
| Blue/Death/Gray/Green/Red Slaad, Slaad Tadpole | Chaos-Husk (rank-named) | Slaad |
| Autumn/Spring/Summer/Winter Eladrin | Season-Bound (rank-named) | Eladrin |
| Angry/Hungry/Lonely/Lost/Wretched Sorrowsworn | Grief-Bound (rank-named) | Sorrowsworn |
| Star Spawn Grue/Hulk/Larva Mage/Mangler/Seer | Spiral Breach (rank-named) | Star Spawn |
| Neogi, Neogi Hatchling, Neogi Master | Void Broker (rank-named) | Neogi |
| Gnoll Fang of Yeenoghu, Orc Blade of Ilneval, Orc Eye of Gruumsh, Orc Hand/Nurtured One of Yurtrus, Orc Red Fang of Shargaas, Orc Claw of Luthic, Spawn of Kyuss, Firenewt Warlock of Imix, Xvart Warlock of Raxivort | See Part IV deity-lock table | Deity locks |

### Recommended procedure (per Continuity C)

1. Edit `Bestiary.xlsx` directly — rename or delete the stock-named rows above once the owner approves specific replacements.
2. Re-run the ingest script that produces `src/bestiary_data_full.json`.
3. Regenerate this Codex so the Lexicon reflects the approved names automatically.
4. Do **not** hand-edit only this markdown file with new names — it will drift from the sheet on the next regeneration.


---

# Part VI — Numeric Challenge Index

Every indexed creature, grouped by Challenge Rating and sorted numerically from lowest to highest, for fast encounter-budget lookups. **STUB**-flagged names are marked with a dagger (†).


**Challenge 0** (38) — Aarakocra†, Abjurer†, Astral Reaver War-Captain†, Banshee†, Brown Bear, Choker†, Cranium Rat†, Dire Wolf, Giant Owl, Green Slaad†, Grung Wildling†, Ice Mephit†, Leucrotta†, Marid†, Maurezhi†, Merrenoloth†, Necromancer†, Owlbear†, Phase Spider, Piercer†, Polar Bear, Priest†, Remorhaz†, Retriever†, Revenant†, Rothe†, Spider, Thug†, Tiger, Tyrannosaurus Rex†, Umber Hulk†, Umbrin Inquisitor†, Umbrin Spider-Priestess†, Vampire (warrior), Weasel†, Winter Wolf, Xorn†, Young Faerie Dragon


**Challenge 1/8** (34) — Armanite†, Boar, Deep Dwarf Screamer†, Derro†, Diviner†, Elephant†, Empyrean†, Fomorian†, Giant Poisonous Snake, Giant Spider, Grung Elite Warrior†, Illusionist†, Imp†, Mummy Lord, Poisonous Snake, Pony†, Reef Shark, Roc, Sahuagin†, Sea Spawn†, Shadow Mastiff, Shambling Mound, Specter, Sporefolk Sovereign, Tarrasque†, Werewolf, Wolf, Young Blue Dragon, Young Bronze Dragon, Young Gold Dragon, Young Green Dragon, Young Kruthik†, Young Red Dragon, Young Remorhaz†


**Challenge 1/4** (38) — Androsphinx†, Animated Armor, Annis Hag†, Astral Ascetic Anarch†, Black Bear, Constrictor Snake, Cult Fanatic†, Deep Dwarf Despot†, Derro Savant†, Eagle, Flying Snake, Giant Constrictor Snake, Gray Ooze, Howler, Lizard King/Queen†, Lizardfolk Shaman†, Medusa†, Merrow†, Nightmare†, Nycaloth†, Oaken Bolter†, Ochre Jelly, Orc War Chief, Owl, Quadrone†, Saber-toothed Tiger, Serpent-Blood Broodguard†, Solar†, Swarm of Poisonous Snakes, Swarm of Quippers, Ulitharid†, Unicorn†, Vulture, Worg†, Wretched Sorrowsworn†, Young Black Dragon, Young Brass Dragon, Young Silver Dragon


**Challenge 1/2** (35) — Bandit†, Black Abishai†, Bugbear†, Bugbear Chief†, Camel, Canoloth†, Chuul†, Cockatrice†, Dao†, Deep Dwarf Warlord†, Dimetrodon†, Draft Horse†, Elk†, Ettercap†, Fire Snake†, Harpy†, Hook Horror†, Hunter Shark†, Lion, Merfolk†, Morkoth†, Mule†, Panther†, Peryton†, Purple Worm†, Shadow Dancer†, Sporefolk Sprout, Thorny Vegepygmy†, Tortle Druid†, Treant, Tribal Warrior, Umbrin†, Voidmind Archivist†, War Priest†, Weretiger


**Challenge 1** (24) — Allosaurus†, Astral Reaver Knight†, Black Pudding, Chitine†, Clay Golem, Crab†, Deep Dwarf Hammerer†, Drider†, Ghoul†, Giant Eagle, Gnoll†, Hawk, Kraken Priest, Rat, Serpent-Blood Malison†, Spectator, Star Spawn Hulk†, Swarm of Rats, Ultroloth†, Water Elemental Myrmidon, Werebear, Yochlol†, Young Red Shadow Dragon†, Young White Dragon


**Challenge 2** (23) — Blood Hawk, Blue Abishai†, Bulette†, Cave Bear, Crawling Claw†, Cultist†, Death Slaad†, Deep Dwarf†, Deinonychus†, Giant Wolf Spider, Gnoll Fang of Yeenoghu†, Korred†, Magma Mephit†, Marut†, Neothelid†, Pegasus†, Salamander†, Steam Mephit†, Umbrin Favored Consort†, Umbrin House Captain†, Winter Eladrin†, Xvart†, Young Copper Dragon


**Challenge 3** (40) — Babau†, Banderhobb, Basilisk, Bat†, Bullywug†, Chimera, Cyclops, Darkling†, Deep Dwarf Kavalrachni†, Dire Troll, Erinyes†, Frost Giant, Gelatinous Cube†, Ghost, Giant Ape†, Giant Bat†, Giant Centipede†, Giant Hyena†, Giant Strider†, Giant Wasp†, Gloom Weaver, Gray Slaad†, Grung†, Hobgoblin Warlord, Kobold, Manticore, Martial Arts Adept†, Nilbog†, Orc Eye of Gruumsh†, Orc Nurtured One of Yurtrus†, Phoenix†, Pteranodon†, Rakshasa†, Rutterkin†, Shrieker†, Spirit Naga†, Stench Kow†, Troll, Vampire, Wastrilith†


**Challenge 4** (33) — Astral Reaver Warrior, Cloud Giant Smiling One, Conjurer†, Deep Scion†, Giant Badger†, Giant Octopus†, Giant Rat†, Giant Shark†, Giant Weasel†, Giff†, Hadrosaurus†, Hobgoblin Captain, Homunculus†, Hydra, Killer Whale†, Kobold Scale Sorcerer, Merregon, Mindwitness†, Monodrone†, Nalfeshnee†, Noble†, Ogre, Ogre Battering Ram, Ogre Bolt Launcher, Ogre Chain Brute, Orc, Orc Red Fang of Shargaas†, Shadow Mastiff Alpha, Star Spawn Grue†, Swarm of Rot Grubs, Vine Blight†, Warhorse Skeleton†, Yeti†


**Challenge 5** (43) — Acolyte†, Allip†, Ankheg, Aurochs†, Autumn Eladrin†, Cambion†, Darkmantle†, Deep Dwarf Xarrorn†, Djinni, Dretch†, Dust Mephit†, Ettin†, Froghemoth, Frost Giant Everlasting One, Giant Crab†, Giant Elk†, Giant Goat†, Giant Lizard†, Giant Scorpion†, Giant Vulture†, Goblin Boss, Grick Alpha, Griffon†, Hill Giant, Kobold Inventor†, Mage†, Marilith†, Ogre Howdah, Orc Claw of Luthic†, Otyugh†, Rhinoceros†, Rug of Smothering†, Sibriex†, Slaad Tadpole†, Storm Giant Quintessent, The Bloom That Hungers, Triceratops†, Troglodyte†, Twig Blight†, Venom Troll, Veteran, Wereboar, Winged Kobold†


**Challenge 6** (32) — Bard, Behir†, Blackguard†, Carrion Crawler†, Cat†, Cloud Giant, Death Kiss†, Dybbuk†, Earth Elemental Myrmidon, Flumph†, Frost Salamander†, Gazer†, Giant Boar†, Giant Toad†, Grick†, Guard, Hobgoblin†, Hobgoblin Iron Shadow†, Neogi†, Orc Blade of Ilneval†, Raven†, Shield Guardian†, Skulk†, Spawn of Kyuss†, Spring Eladrin†, Star Spawn Mangler†, Stone Cursed†, Stone Giant, Storm Giant, Umbrin Arachnomancer†, Violet Fungus†, Wood Woad†


**Challenge 7** (65) — Aboleth, Astral Ascetic Enlightened†, Astral Ascetic Monk†, Astral Ascetic Sentinel†, Awakened Tree†, Badger†, Blue Dragon Wyrmling, Blue Slaad†, Bone Devil, Boneclaw†, Centaur†, Deep Dwarf Soulblade†, Deep Dwarf Stone Guard†, Depth Toad Archpriest†, Depth Toad Taskmaster†, Druid, Enchanter†, Flying Sword†, Gaze Tyrant, Giant Crocodile†, Giant Frog†, Giant Sea Horse†, Gnoll Flesh Gnawer†, Goblin, Green Dragon Wyrmling, Green Hag†, Grell†, Guardian Naga†, Half-ogre†, Hell Hound, Hellfire Engine†, Hippogriff†, Hobgoblin Devastator†, Hungry Sorrowsworn†, Hyena†, Iron Cobra†, Jackalwere, Ki-rin†, Knight†, Lesser Gaze Tyrant†, Leviathan, Master Thief†, Nabassu†, Neogi Hatchling†, Octopus†, Oinoloth†, Orc Hand of Yurtrus†, Pit Fiend, Plesiosaurus†, Quaggoth Thonot†, Quasit†, Rot Troll, Rust Monster†, Skull Lord†, Spirit Troll, Stone Giant Dreamwalker, Umbrin Matron†, Umbrin Shadowblade†, Vargouille†, Vegepygmy Chief†, Warhorse†, Warlord, White Abishai†, Will-o-wisp†, Wyvern


**Challenge 8** (22) — Amnizu, Assassin†, Barlgura, Boggle†, Chasme†, Couatl†, Fire Elemental Myrmidon†, Glabrezu†, Gold Dragon Wyrmling, Ice Devil, Kruthik Hive Lord†, Lemure, Maw Demon, Molydeus†, Oni†, Quipper†, Red Dragon Wyrmling, Serpent-Blood Pureblood†, Shadow†, Spined Devil, Transmuter†, Vaskor, the Stone Maw


**Challenge 9** (40) — Air Elemental Myrmidon†, Arcanaloth†, Astral Reaver Supreme Commander†, Azer†, Balhannoth†, Bodak†, Bone Naga†, Bronze Scout†, Cadaver Collector†, Cave Gnome†, Copper Dragon Wyrmling, Cow†, Deep Dwarf Mind Master†, Deer†, Depth Toad†, Devourer†, Eidolon, Flind†, Gray Render†, Half-Red Dragon Veteran†, Horned Devil, Kobold Dragonshield†, Lamia†, Mastiff†, Mimic†, Red Abishai†, Sahuagin Baron†, Sahuagin Priestess†, Serpent-Blood Anathema†, Serpent-Blood Nightmare Speaker†, Silver Dragon Wyrmling, Slithering Tracker†, Smoke Mephit†, Steel Predator†, Stegosaurus†, Swarm of Bats, Swarm of Cranium Rats†, Tortle†, Water Elemental, Wererat


**Challenge 10** (34) — Abyssal Wretch, Adult Blue Dragon, Adult Copper Dragon, Adult Gold Dragon, Adult Silver Dragon, Ape†, Astral Reaver Spellblade†, Barbed Devil, Chain Devil, Cloaker†, Death Knight, Dolphin†, Doppelganger†, Dragon Turtle, Female Steeder†, Flameskull†, Guard Drake, Lizardfolk†, Manes†, Meazel†, Pentadrone†, Planetar†, Pseudodragon, Red Slaad†, Redcap†, Scorpion†, Scout†, Stirge†, Swarm of Insects, Swarm of Ravens†, Thri-kreen†, Xarog the Pactbound Furnace†, Yagnoloth†, Yeth Hound†


**Challenge 11** (38) — Abominable Yeti†, Adult Oblex†, Adult Red Dragon, Ashthirst the Hollow, Balor†, Bandit Captain†, Bearded Devil†, Black Dragon Wyrmling, Catoblepas†, Deathlock Wight†, Deep Rothe†, Deva†, Draegloth†, Firenewt Warrior†, Gaze Tyrant (in lair), Girallon†, Gorgon†, Helmed Horror†, Incubus†, Invisible Stalker†, Kenku†, Kraken†, Mezzoloth†, Mud Mephit†, Night Hag†, Nupperibo, Oblex Spawn†, Orthon†, Riding Horse†, Roper†, Shadow Demon†, Summer Eladrin†, Swashbuckler†, Tlincalli†, Umbrin Mage†, Voidmind, Voidmind Arcanist, White Dragon Wyrmling


**Challenge 12** (23) — Alkilith†, Archdruid†, Awakened Shrub†, Berbalang†, Brass Dragon Wyrmling, Bronze Dragon Wyrmling, Cave Fisher, Crocodile†, Deathlock†, Duodrone†, Efreeti†, Gibbering Mouther†, Gnoll Witherling†, Goat†, Goristro†, Green Abishai†, Gynosphinx†, Narzugon, Nightwalker†, Ox†, Spy†, Vampiric Mist†, Warlock of the Fiend†


**Challenge 13** (10) — Adult Brass Dragon, Adult Faerie Dragon, Adult Green Dragon, Adult Kruthik†, Brontosaurus†, Mouth of Grolantor†, Star Spawn Larva Mage†, Velociraptor†, Vrock†, Water Weird†


**Challenge 14** (12) — Adult Black Dragon, Astral Dreadnought†, Berserker†, Choralith, Voice Below, Death Dog†, Evoker†, Gas Spore†, Gladiator†, Ogre Zombie†, Scarecrow†, Sporefolk Adult, Sprite†


**Challenge 15** (10) — Adult Blue Dracolich, Adult White Dragon, Angry Sorrowsworn†, Darkling Elder†, Displacer Beast†, Lonely Sorrowsworn†, Orog†, Sea Horse†, Serpent-Blood Abomination†, Skeleton


**Challenge 16** (6) — Adult Bronze Dragon, Ancient Brass Dragon, Commoner†, Fire Elemental†, Nothic†, Vampire Spawn†


**Challenge 17** (7) — Ancient White Dragon, Archmage†, Fire Giant Dreadnought†, Firenewt Warlock of Imix†, Lumen of the Shattered Thread, Quetzalcoatlus†, Wight


**Challenge 18** (6) — Deathlock Mastermind†, Elder Tempest†, Hydroloth†, Magmin†, Meenlock†, Voidmind Lich†


**Challenge 19** (9) — Ancient Copper Dragon, Ankylosaurus†, Apprentice Wizard†, Gargoyle†, Gaze Tyrant Husk†, Mummy Lord (in lair)†, Quickling, Trapper†, Warlock of the Great Old One†


**Challenge 20** (12) — Ancient Bronze Dragon, Ancient Red Dragon, Blink Dog†, Bulezau†, Champion†, Frog†, Gnoll Hunter†, Gnoll Pack Lord†, Mummy†, Quaggoth†, Stone Defender†, Threxus, the Iron Spiral


**Challenge 21** (8) — Ancient Green Dragon, Archer†, Demilich (in lair)†, Dryad†, Elder Brain†, Gaze Tyrant Sovereign (in lair)†, Lich (in lair)†, Vegepygmy†


**Challenge 22** (8) — Ancient Blue Dragon, Ancient Silver Dragon, Dolphin Delighter†, Giant Fire Beetle†, Jackal†, Male Steeder†, Minotaur†, Star Spawn Seer†


**Challenge 23** (11) — Ancient Black Dragon, Ancient Gold Dragon, Choldrith†, Demilich†, Eirfax, the Dusk Crowned, Elder Oblex†, Ghast†, Neogi Master†, Serpent-Blood Pit Master†, Stone Golem†, Sword Wraith Commander†


**Challenge 24** (8) — Baboon†, Galeb Duhr, Lich†, Lost Sorrowsworn†, Morkoth (in lair)†, Serpent-Blood Mind Whisperer†, Shoosuva†, Tanarukk†


**Challenge 25** (5) — Earth Elemental†, Nagpa†, Sword Wraith Warrior†, Warlock of the Archfey†, Wraith


**Challenge 26** (10) — Flesh Golem†, Gaze Tyrant Sovereign†, Hezrou†, Intellect Devourer†, Specter (poltergeist)†, Succubus†, Tridrone†, Umbrin Elite Warrior†, Xarog, the Pactbound Furnace, Zombie†


**Challenge 27** (8) — Air Elemental†, Axe Beak†, Corpse Flower†, Dhergoloth†, Grimlock†, Mammoth†, Satyr†, Vampire (spellcaster)


**Challenge 28** (5) — Bheur Hag†, Flail Snail†, Minotaur Skeleton†, Quaggoth Spore Servant†, Zaratan†


**Challenge 29** (5) — Barghest†, Gor Vekk, Architect of Ends, Pixie†, Soul Monger†, Xvart Warlock of Raxivort†


**Challenge 30** (6) — Fire Giant†, Iron Golem†, Lizard†, Needle Blight†, Sea Hag†, The Marquis of Silence
