# Exact controlling-source excerpts

These are excerpts of supplied files, not outside rules. Line numbers below refer to the submitted decoded text. Source JSON excerpts retain their complete selected object. The full archive remains controlling.

## `DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md` — lines 88–119

SHA256 `3211acc70441de0a2b59221efd57c9a6ff74155e9afcd9a4b5458bb0a2644a73`.

```text
88: ## Capacity, placement and dependent Totems
89: 
90: Deployable slots are zero before the engine's class gate, one at Tinker 6, two at 13 and three at 17. Advanced Turret Bay uses two available slots for 4 RP, or its one-slot/2-RP fallback; zero free slots is illegal. Drones use separate persistent ownership capacity, not deployable slots.
91: 
92: At Tinker 13, choose exactly two basic Drones with exactly one module each or exactly one Drone with exactly two distinct modules during the printed configuration procedure. No more than two. Earlier module acquisition remains governed by its own class gates. **NEW:** withdrawing the excess Drone into an unavailable/retracted configuration causes no destruction or salvage.
93: 
94: Totem capacity is one, then two at Shaman 13. **NEW generalization:** an ordinary new Totem placed at capacity replaces a chosen active Totem, including at capacity one. Echo needs a separate free capacity; creating Echo alone never evicts another Totem.
95: 
96: **NEW dependent Echo rule:** ending, replacing, destroying or expiring the parent ends its Echo and releases both capacities. That Echo ending is administrative, not its own destruction. Ending only Echo leaves the parent. Echo shares the parent's remaining duration, concentration and upkeep.
97: 
98: Preflight ownership, source use, space/range, action, resources and capacity before payment or ending anything. Determine all dependent releases first. A valid parent replacement can free room for the new parent plus a separately paid Echo. If Echo cannot fit, its optional creation is unavailable; the caller can submit an ordinary parent-only placement instead. Failure of a submitted combined transaction changes nothing.
99: 
100: All active Totems share their concentration burden. Losing it ends their effects and dependent Echoes without destruction rewards. Totem movement follows its printed BA, 15-foot move through an open route within the printed range; it retains expiry, concentration, recipient ledgers and pulse schedule. Movement grants no entry heal.
101: 
102: ## Destruction, debris and source-specific opportunities
103: 
104: Record the instance, original hostile cause, actual enemy hit versus transferred damage, deliberate sacrifice, whether the object itself is a copy, friendly damage, secondary explosion and inherited branch flags at destruction. Separately record whether incoming damage was copied. A real device destroyed by copied damage still has ordinary destruction consequences; only that damage's actual restriction flags suppress them. “Copied object” exclusions do not mean “any object damaged by a copy.”
105: 
106: **NEW anti-loop integration:** the first actual destruction of an instance establishes its only object-linked opportunity and material set. Nonqualifying and declined opportunities are closed for that instance. Snap does not create another set. A second physical destruction still ends the rebuilt device but cannot supply another harvest, Volatile opportunity or material record.
107: 
108: Recycling, Salvage, Reaper and Snap share the usable original material. The first successful consumer spends it. Volatile does not consume material. A source-qualified Volatile can therefore precede one legal material consumer. Declining Volatile on Device A does not spend the owner's round allowance for Device B.
109: 
110: | Source | Important predicate |
111: | --- | --- |
112: | Efficient Recycling | Your destroyed non-copy device; not deliberate sacrifice; debris within reach, after combat for one minute, 1/short rest. Refund at most min(1 RP, actual deployment RP). Enemy cause is **not required**. |
113: | Scrap Salvage | Enemy-destroyed qualifying material; Action+1 RP, 1/encounter; one slot-using Scrapling at printed location |
114: | Scrap Reaper | Qualifying destroyed enemy-hit device/material within 30 feet; Reaction+2 RP, 1/short rest; printed short-lived Scrapling uses **no deployable slot** |
115: | Volatile Components | First enemy-caused device destruction; excludes deliberate sacrifice, copy, friendly damage and secondary explosion; enemy within 5 feet; once per owner/round |
116: | Snap | Original destroyed instance/material, original footprint free and original expiry not reached |
117: 
118: Scraplings cannot spawn their own replacement. Reaper still uses the later BA command and damaging-action budget for its detonation. Its absent slot cost is not inferred from the separate Salvage card. Reaper also carries its source's broader no-own-destruction-chain property; a later type ruling must not silently remove that protection.
119: 
```

## `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md` — lines 113–128

SHA256 `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`.

```text
113: ## Stances
114: 
115: Choose one stance during a **regular** own turn before the first event that would use any stance benefit/restriction: attack, spell, relevant check/save or movement. If none occurs, choose before turn end. No retroactive selection. It lasts until next regular start. NEW: extra turns preserve the stance and spent allowances; they cannot choose/replenish it.
116: 
117: | Stance | Effect |
118: |---|---|
119: | Aggressive | +2 damage once per qualifying weapon attack's damage packet; −2 AC. Not periodic or copied damage. |
120: | Guarded | +1 AC, advantage on explicit roll/contest resisting Shove, Speed −5 (minimum 0). Its +1 can coexist with Guard's first-attack +2, giving +3 then +1. This combination is explicitly allowed here. |
121: | Mobile | First 5 ft of actual voluntary movement does not provoke; no free movement is granted. Your opportunity attacks reduce each base weapon die one step: d12→d10→d8→d6→d4 (minimum d4). Rider dice unchanged. Die sequence is NEW. |
122: | Focused | Choose +1 save DC for one spell OR +1 to one attack roll from one spell. After use, no-Reaction-except-Counterspell restriction remains through expiry. This grants no Counterspell knowledge, free cost or extra Reaction. |
123: | Carrying | Choose one actual currently applicable cargo penalty to ignore; choice fixed through expiry. It does not increase capacity or erase all load limits. DEX saves have disadvantage. |
124: 
125: ## Maneuvers and ordinary attacks
126: 
127: All opposed checks use Core total comparison: higher wins, exact tie preserves state. No natural-20 automatic victory or hidden task-degree effect on an opposed tie. A printed save-based class maneuver keeps its own method.
128: 
```

## `DescentReviewChanges/ReviewBible/docs/mechanics/classes/crimson-agent.md` — lines 20–36

SHA256 `e0c14a88bd05c0a57e729959bc6318085382307b411544599aa6a5481145233b`.

```text
20: Blood Gauge (BG) starts and ends each encounter at 0, capacity 3; Spill Control raises capacity 6 while known. Once on your own regular turn, a weapon attack that damages a hostile living creature grants 1 BG. Hemorrhage Slash uses this same trigger, not an additional one. Explicit critical/kill/refund features can add more, but total BG gained is capped 2 per round. Self-inflicted damage, allies, summons, helpless captives and repeated damage to a corpse never generate BG. Blood is an encounter resource, not a currency carried into rest.
21: 
22: Dexterity governs weapon attacks; Intelligence governs hemomancy save DC and M. S scales from Crimson Agent class level. A weapon technique includes only its printed attacks, with normal weapon die plus Dexterity (or Strength when that weapon requires it). No free attack is implied by attack-speed wording. Class BG and RP are separate. Once per turn when casting an ordinary spell, optionally spend 1 BG to prevent 1 of that cast's Dissonance gain, minimum 0; never reduce RP this way.
23: 
24: Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation.
25: 
26: One Blood Mark at a time on a living target with your Bleed, except Phantom Strike, which explicitly may apply the mark without Bleed. It does not add a free Bleed. Marks last 5 of your regular turns, expire on encounter end or if the target dies, and never create damage by themselves. Rupture requires the target still within 60 ft and line of effect; it spends the mark. A mark does not defeat cover, planar boundaries or bloodlessness. Bloodtrail has its own tracking limits.
27: 
28: Veinweaves are self buffs unless their card expressly allows an ally. They require concentration and one may be active. Crimson Harmony is an explicit exception permitting two Veinweaves as one linked concentration burden; a failed concentration check ends both. A non-Veinweave concentration effect replaces the whole group. BG is spent on activation; no upkeep unless printed. Damage-sharing is redirection before mitigation, not extra damage: apply each recipient's own defenses once and never redirect the redirected portion again.
29: 
30: The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds.
31: 
32: At level 1 learn the core Blood Gauge/Bleed rules automatically. Blood Mark and Veinweaver's Core remain selections; Quickblood can be selected and used without a second unlock tax. Veinweaver's Core improves that foundation as printed. Standard scheduled acquisition applies. Bloodbound Edge is automatic 9. At 10 choose Bloodweaver, Shadow Operative or Thirstborn; its Final Cut is automatic 20. Duplicate Hemostasis names are separate Arch and Bloodweaver IDs.
33: 
34: Capacity clarification: Blood Gauge automatically reaches capacity 6 at class 9. Spill Control allows reaching 6 early but never raises the cap above 6. This new explicit gate ensures a later 5-BG Final Cut can be used without an optional capacity selection. Gain cap 2/round and encounter reset 0 still apply.
35: 
36: **Protected source interface:** Once per turn, spend 1 Blood Gauge while casting to prevent 1 Dissonance; the Agent routes Weave strain through blood rather than gaining free casts.
```

## `DescentReviewChanges/ReviewBible/docs/mechanics/classes/shaman.md` — lines 20–28

SHA256 `7129b8d5ec27e4fb036b1954861e8e642ed66d68f942f6d2fce021803f6952dc`.

```text
20: Wisdom is the class ability. Choose Elemental Affinity automatically at 1: Fire, Ice, Air or Earth. Spellcasting/RP remain separate from Totem objects and flasks. Totem capacity 1, rises 2 at 13; any third replaces one of your existing totems. A totem is a visible Tiny magical object: AC 12+PB, HP 2 L, immobile, immune to poison/psychic/conditions, vulnerable to ordinary weapon and other damage. At 0 HP its aura ends. A new totem appears within 30 ft; cannot occupy a creature's space, serve as a bridge, trap a creature without a save or move through walls.
21: 
22: Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack.
23: 
24: On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction.
25: 
26: The book places Flask Use at Base but describes advanced flask casting as Theurgist/Soothsayer-only. For this draft, Base Flask Use grants mundane prepared tactical flasks thrown with an Action; at Hero 10 only Theurgist/Soothsayer gain magical Bonus Action flasks. Bloodcaller retains mundane alchemical knowledge, not the advanced flask subsystem. At long rest prepare 2 flasks, rising to 3 at 5 and 4 at 11; no encounter refill or stockpiling, total carry cap 4, unused contents become inert when preparing a new batch. This finite-rest supply replaces encounter-based free heal farming.
27: 
28: Flask tier uses S. Mundane Base modes: Burn=one enemy 30 ft DEX save S d6 fire half, failure 1d4 fire next turn; Root=one ground enemy 30 ft STR save Speed 0 until end its next turn; Weaken=one enemy 30 ft CON save or-1 attack damage until end its next turn. Advanced Hero modes additionally: Stun=one enemy 30 ft CON save or no Reactions, failure by 10 Stunned until end its next turn; Heal=one living ally 30 ft S d6+M HP; Restore=end Frightened or Poisoned on one ally 30 ft. Every thrown flask consumes one prepared unit and 2 RP for advanced magic (Base mundane flasks cost 0 RP). Changing payload requires no separate crafting action when throwing. No flask leaves harvestable poison or another flask.
```

## `docs/audit/2026-10-08/full-game/GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md` — lines 604–606

SHA256 `48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0`.

```text
604: ## TD-13 — Recycling refunds actual deployment RP only
605: 
606: KEEP actual enemy destruction, your own device, one minute after combat, once per short rest, consume its usable debris and return at most1RP actually paid to **deploy that same device**. Crafting GP, ingredients, dawn charges, service packs, encoding, field repairs, Dissonance routing and later Overcharge RP are not deployment RP. These43 crafted devices have no innate RP deployment cost, so they create **zero refundable deployment RP** through this card. Do not consume a valuable wreck merely by falsely asserting that its price is RP; admission must identify an actual eligible prior paid deployment. Deliberate sacrifice, copied objects and repeated debris claims do not qualify. No unspecified material salvage percentage is added by the class's legacy name.
```

## `DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md` — lines 177–183

SHA256 `6986ed6bee0e88a1f5308bba534ebb0c2538d21c9ee3fc61e7c462246ac2fd60`.

```text
177: Class drone accuracy/control upgrades, modules, Recalibrate, interception, bolts/healing modes, class turret improvements, bomb specialization, Safe Detonation and bomb-stock recovery stay class-specific. Gadget Sync remains the actual paid class-bomb-to-class-turret shot and still uses the shared offensive allowance. Crafted devices receive no turret shot or bomb-specific ally exclusion. A genuinely eligible ally may receive Calibrated Precision or the actual class drone's Protective Programming benefit under their printed comparisons/costs; the recipient does not become a source of those features.
178: 
179: Malfunction Field can use actual eligible active own devices as origins for its one once-per-numbered-round hostile spell-attack disadvantage under the printed range/perception rules. Multiple devices do not create several auras, a save penalty or antimagic. Volatile Components requires actual enemy destruction and its source first-event-per-round/one-enemy-within5-feet/S-fire conditions. Friendly destruction and deliberate sacrifice do not create that trigger or secondary chains.
180: 
181: Efficient Recycling refunds at most one RP actually paid to deploy the particular owned device, after its genuine enemy destruction and the feature's real one-minute/once-per-short-rest salvage procedure. GP construction, later repair RP and activation RP are not deployment costs: an ordinary crafted deployment paid0RP, so no refund is available from it. A quoted recipe value does not create paid RP.
182: 
183: Scrap Salvage and Scrap Reaper can consume a genuinely eligible physical wreck through their actual costs, temporary slots, timing and command limits. That exclusive debris cannot also fund another Scrapling, reconstruction, new ingredients or generic magical salvage. Remote Detonation and Catastrophic Overload are terminal primary-consuming sacrifices under their exact class costs/targets; no second repair/recycling chain survives the sacrifice. Harmless actual residue may remain without magical reconstruction rights.
```

## Actual Efficient Recycling card

`DescentReviewChanges/ReviewBible/data/public/class_playtests/tinker.json#/cards/31`, SHA256 `f087cc9250f1864e60209fb13bff86800d45b7238dc09e8eac2dbf2272b09c1d`. The source card is not edited or promoted.

```json
{
  "id": "tinker.hero.techsmith.efficient-recycling",
  "name": "Efficient Recycling",
  "className": "Tinker",
  "band": "Hero",
  "path": "Techsmith",
  "sourceKind": "passive",
  "minimumClassLevel": 10,
  "acquisition": "selection",
  "activation": "Triggered",
  "cost": "One destroyed device remains",
  "rangeAndTarget": "Your destroyed device within reach",
  "duration": "After combat 1 minute",
  "frequency": "1/short rest",
  "effect": "Recover 1 RP spent on deploying it, never more than its actual paid cost. Deliberate sacrifice or copy does not qualify. Consume usable debris; no repeated salvage from same object.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 4631,
    "originalText": "Efficient Recycling: Recover components from destroyed devices to create new ones."
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```
