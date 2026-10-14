# -*- coding: utf-8 -*-
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "manuals"
OUT.mkdir(parents=True, exist_ok=True)

text = r"""# The Director's Crucible
## DM-01 — Core Director Manual for Decennium Descent

*Official GM core. Aligned to the Player Rulebook. Simulation agents: prefer this book + Player Rulebook. 2026-07-30.*

**Book code:** DM-01
**Companion volumes:** *Codex of the Heartcell* (foes) · *Instruments of the Weave* (downtime/expedition tools) · *Chronicle of the Decennial Opening* (gazetteer)

---

# Part I — Master of the Opening

## 1. The Director's Charge

You are the Director. Players steer characters; you steer consequence. Decennium Descent is not a story about defeating you—it is a story about whether mortal ambition can feed a prison without freeing what sleeps inside it.

**Tone:** grim liturgy and high stakes. Heaven and Hell hold deliberate tension. Mortals dig for glory and gold. Present the public Crucible myth as complete at campaign start. Reveal deeper machinery only through contradictions the party earns.

**Authority ladder**

1. Owner spoken lock (intent) — still ask before overwriting published books
2. Player Rulebook (player procedures)
3. This Crucible + sister Director books
4. Companion apps and playtest reports (mirrors / history)

When layers conflict on published Player Rulebook text: **stop and ask the owner**.

### Theme you are protecting

War, rivalry, and hunger keep the world noisy. Absolute peace is not a happy ending—it is an extinction risk. Treasure is bait. Expeditions are the machine's preferred fuel.

## 2. A World in Motion (Across the Cycle)

Aethel does not freeze between Descents. Between Openings, empires digest last Cycle's loot, temples rewrite sermons, and floor civilizations remember who raided them.

| Phase | Director focus |
|-------|----------------|
| Years 1–3 after seal | Surface wars over dungeon-touched weapons; funerals; debt |
| Years 4–7 | Guilds restock; rival companies form; research black markets |
| Years 8–9 | Omens near Shardspire; pilgrim traffic; Pact rhetoric spikes |
| Year 10 Opening | 100-day season — see *Chronicle* calendar |

Track one **surface consequence** per returned expedition: a market glut, a cult, a marriage alliance, a bounty. The dungeon is vertical; the Cycle is horizontal.

## 3. Session Architecture

Open with stakes (why this floor, why today). Close with consequences (loot, injuries, maps, reputation, hours burned). Rotate spotlight across **Combat, Recon, Research, Resource, Support**.

**Three clocks**

| Clock | Duration | Meaning |
|-------|----------|---------|
| Opening | 100 days / **2400 hours** | Season of entry |
| Horn PoNR | Day 50 / **1200 hours** | Retreat-or-accept-seal-risk milestone |
| Day periods | Morning / Afternoon / Evening | Team assignments |

**Do not confuse:**

- **Horn PoNR (day 50 / 1200 h)** — Opening calendar milestone.
- **Canticle Gate / Floor 50 narrative pressure** — many Expeditions psychologically quit around Sanctum of Echoing Choirs. That is **morale geography**, not the horn clock. Call it **the Bar of Last Refuge** or **soft quit line** — never "the point of no return" in the horn sense.

Legacy companion UI may show **120 h** underground horn — **code debt**. Prefer 2400/1200 in new sims unless owner restores a nested micro-budget.

Paper tracks the Session app may lack: death saves, Hit Dice, concentration, team assignment, period planner.

## 4. Expeditions (Player Rulebook RAW)

Maximum **12 characters** per Expedition — organizational roster, not initiative seats. Larger forces = **multiple Expeditions coordinating**.

| Team | Optimal | Function |
|------|---------|----------|
| Combat | 4–6 | Battles, delving, immediate threats |
| Recon | 1–3 | Scouting, maps, intelligence |
| Research | 1–3 | Lore, identify, translate |
| Resource | 2–4 | Hunt, forage, cook, craft, harvest |
| Support | 1–3 | Camp, repair, healing, transport |

Resolution modes: Quick · Scene · Parallel · Between-session — full worksheets live in *Instruments of the Weave*.

**Worked example (Yieldheart day):** Combat clears Automaton patrol (afternoon); Recon maps Echoing Gallery (morning); Research studies Spire murmurs (evening); Resource chips Luminous Veins (afternoon); Support sets Temporary Camp at Hearth (evening). One calendar day, three periods, five outputs.

## 5. Opening Calendar Play

Use *Chronicle* for the 100-day phased table. At the table:

1. Mark Opening day 1 when Shardspire activates in fiction.
2. Advance hours for travel, fights, long rests (+8 h table assumption unless haven says otherwise).
3. At day 50, stage the horn — give a real choice, not a gotcha.
4. After day 50, escalate rival companies and seal rumors.
5. Near seal, force extraction math: what do you carry, who do you leave, what research is unfinished?

---

# Part II — Master of Adventures

## 6. Creating Expedition Arcs

Every arc should answer: **what does the machine gain if they succeed?**

| Arc type | Example seed | Machine feed |
|----------|--------------|--------------|
| Dungeon push | Charge three sun-shard vials for Radiance Gate | Combat + loot circulation |
| Mystery | Why do gate records say Signatories not Creators? | Research + revelation |
| Rival race | Cult wants the same seal | Conflict dissonance |
| Rescue | Floor civ hostage | Reputation + war seeds |
| Salvage | Brogi slag key | Resource + craft |

**Villain budgets:** pick one surface face (guild, temple, empire) and one depth face (floor warlord, gate cult). They need not know each other.

**Urban / wilderness / depth mix:** Crystalfront scenes sell loot and law; wilderness approaches sell logistics; depth sells the Crucible myth.

## 7. Creating NPCs

| Tier | Detail | Use |
|------|--------|-----|
| Name + want | One sentence | Market cameo |
| Bond + fear | + quirk | Recurring ally |
| Full sheet | Stats if they fight | Patrons, rivals, bosses |

**Patrons:** Academic Concord (research), temple of a Fifteenfold mask (folk faith), infernal factor (discord contracts), imperial quartermaster (weapons for next war).

**Pact-adjacent contacts:** speak of keeping the peace by keeping the struggle honest. They are not cartoon evil; they fear silence.

## 8. Creating Monsters

1. Open `Bestiary.xlsx` for portable stats.
2. If Type/Size/CR is nonsense, mark **STUB** and reskin (see *Codex*).
3. Prefer Excel edits to ingest over silent on-table invention.
4. Draft/sandbox combat: announce it.
5. Gate Guardians are set-pieces — use *Codex* chapters, not random CR pulls.

Quick method: pick role (bruiser, controller, skirmisher, artillery, leader), pick tier terrain tag, pick one signature tell, then attach provisional numbers.

## 9. Creating Loot (Bait Philosophy)

Dungeon-touched objects should create **next session's problems**.

| Loot type | Surface consequence |
|-----------|---------------------|
| Weapon | Local warlord tribute demand |
| Relic | Temple schism |
| Map shard | Rival expedition |
| Craft part | Guild monopoly attempt |
| Truth-object | Revelation ladder step |

If loot never leaves the bag, the bait failed.

## 10. Factions and Settlements

Surface factions care about **returned power**. Floor civs care about whether you treat them as people or loot nodes.

Settlement sketch: name, export, law quirk, Opening attitude (pilgrim-friendly / predatory / closed), one NPC face.

## 11. Vertical Staging (Mapping the Descent)

Design downward as **pressure bands**, not a flat dungeon:

1. Approach and muster (Crystalfront)
2. Soft teaching floors (T1)
3. Environment as enemy (T2–T4)
4. Soft quit line (~T5 Canticle) — morale, not horn
5. Bargain and identity fracture (T6–T9 rumor bands)
6. Silence (T10) — only if earned

Cross-cuts: vents, rival camps, research stations, sealed shortcuts that cost revelation or reputation.

---

# Part III — Master of the Weave

## 12. Encounter Building

**EV sketch:** rounds approx foe HP / party DPR; incoming approx enemy DPR times rounds; compare to party HP + healing.

| Band | Feel |
|------|------|
| Under 30% expected HP loss | Patrol / teaching |
| 30–60% | Standard |
| 60–80% | Hard — demand Support |
| 80%+ | Deadly — warn or offer retreat |

Mass combat: at most about eight detailed initiative actors; abstract the rest as clocks/morale.

**Draft stats:** say provisional before initiative.

## 13. Resonance Adjudication

RP is not spell slots. Teach in session zero. Retune / full harmony are companion aliases — map to Player Rulebook Short/Long Rest language when speaking player-facing rules.

Oracle uses **Revelation Charges**, never RP.

Log alignment affinity when sheets have alignment.

## 14. Treasure and Awards

- Parts feed craft (*Instruments* salvage tables).
- Research unlocks are awards too.
- Draft XP: label provisional until owner locks CR to XP table.
- Reputation is an award with teeth.

## 15. Between Adventures

Opening-side: sell salvage, file research, recruit Support NPCs, heal, court factions. Advance calendar. Check horn proximity. See *Instruments* downtime jobs.

## 16. Edge Adjudication

| Situation | Guidance |
|-----------|----------|
| Chase in Echoing Gallery | Noise summons; Stealth contests amplify |
| Bloomdeep spore dash | Period timers; Resource masks |
| Camp siege | Watch fail adds a fight; Support triage authority |
| Escape magic to surface | Opening still ticks if they re-enter |
| Party splits three ways | Parallel resolution; merge on horn hours |

## 17. Tables (Director)

### Opening Omens (d12)

1. Shardspire hums off-key for an hour
2. Crystalfront prices spike on sun-steel
3. A returned company refuses to speak of Floor 50
4. Temple of a Fifteenfold mask declares quiet-year heresy
5. Infernal factor offers free mapping — wants first refusal on relics
6. Umbrin exile warns of sunlight politics on radiant tiers
7. Automaton scrap washes up in a surface river
8. Academic Concord posts bounty for Signatory-language tablets
9. Rival company plants false gate-glyph guide
10. Night without insect noise for three miles
11. Child sings a Canticle tune they could not know
12. Horn rehearsal echo (false) — panic tax on markets

### Trap Seeds by Tier Band (d6)

1. Glyph backlash (T1 wards)
2. Sound snare (T5)
3. Heat plate (T3)
4. Spore burst (T2)
5. Mirror double bait (T4)
6. Bargain brand (T7 rumor)

### Social Events at Crystalfront (d8)

1. Auction of sealed chest (trap or prize)
2. Memorial for sealed Cycle victims
3. Pact sermon: Struggle is mercy
4. Brawl over claim rights
5. Wedding sealed with dungeon ring
6. Census of descending companies
7. Smuggler offers haven bypass
8. Scholar hires Research seat

---

# Part IV — Master of Secrets (Director Only)

## 18. Public Myth vs Heartcell

**Public complete story at start:** Calan'thir and Asmodeus built the Crucible after the Sundering; Divine Pact; proving ground; cooperation monument.

**Director secret:** Silent Ones **are** the Old Ones. They built the **Heartcell** (100 floors, ten Gates, Opening cycle, reward architecture) with loot as bait. Calan'thir and Asmodeus discovered, claimed, or bound the machine — genuine public builders of the Crucible layer, not inventors of the engine.

**Formulation:** The Silent Ones built the prison. Calan'thir and Asmodeus taught the world to call it a dungeon.

**Revelation ladder:** pre-script architecture → Custodians/Bearers/Signatories → Pact governs but did not originate → Heartcell operating cycle. Discoverable; never common knowledge.

**Folk faith:** Fifteenfold Pantheon and planar wheel diagrams are mortal religion — useful, not objective cosmology. Hierarchy: Spiral → Old Ones/Ul'nak → Heartcell → Calan'thir and Asmodeus → First Choir (7) → Fifteenfold → cultural gods.

## 19. Gate Guardians (Live Roster Only)

Vaskor · The Bloom That Hungers · Ashthirst the Hollow · Gor Vekk · Choralith · Lumen of the Shattered Thread · Xarog · Eirfax · Threxus · The Marquis of Silence.

Retired combat aliases (do not use as gates): Hollow King, Cindervore, Vox Prime, and older cosmology names used as bosses.

Full set-pieces: *Codex of the Heartcell*.

---

# Part V — Running the Table and Simulations

## 20. Table Craft

Pace: one meaningful choice per period. Cut empty shopping. When players stall, offer a costed rumor. When they speedrun, tax logistics.

Spotlight fairness across five teams. Let injured PCs work Research/Support.

## 21. Simulation Agent Protocol

Simulations must:

- Cap 12 per Expedition (or label coalitions)
- Use 2400 / 1200 clocks
- Label draft combat/XP
- Keep Silent Ones/Heartcell out of player-facing summaries
- Use live Gate names
- Exercise five teams when claiming full ecosystem
- Prefer this Crucible + Player Rulebook over playtest dumps

Never invent foreign product cosmology. Never overwrite rulebook text silently.

## 22. Sister Books Quick Map

| Need | Open |
|------|------|
| Day planner, salvage, rivals, coalitions | *Instruments of the Weave* |
| Regions, calendar, tier seeds | *Chronicle of the Decennial Opening* |
| Monster ecology and guardians | *Codex of the Heartcell* |
| Long extracts | Legacy annex / `docs/mechanics/` locks |

---

# Appendix A — Alignment Checklist vs Player Rulebook

- Expedition max 12 and five teams match Expeditions in Aethel.
- Short/Long Rest language when teaching players; companion Retune aliases OK if mapped.
- Death/dying per rulebook; paper if Session lacks tracks.
- Umbrin naming locked.
- Player Rulebook Appendix B folk religion remains until owner approves rewrite (Q-OV-3).

# Appendix B — Quick Reference

Opening **2400 h** · Horn PoNR **1200 h / day 50** · Seal at Opening end · Expedition **12** · Teams Combat/Recon/Research/Resource/Support · Gate roster live · Soft quit line is not horn PoNR.

---

*End of The Director's Crucible (DM-01).*
"""

path = OUT / "The_Directors_Crucible.md"
path.write_text(text, encoding="utf-8")
print("wrote", path, "words", len(text.split()))
