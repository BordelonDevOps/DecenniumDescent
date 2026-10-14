# Player rules / class balance audit

**Scope:** Player-facing, pre-playtest audit of the 17 selectable Aethel base classes. Fighter is archive-only; Swashbuckler is an orphan reference and is not assessed as a player option. This is a comparative risk review, **not** a replacement class design. “Draft” and “unverified” mean the source material does not presently support a firm conclusion.

**Sources read:** `rulebook_output.txt` Ch. 3 and Resonance chapter; `src/data/canon-classes.js`, `class-hit-dice.js`, `class-details.js`, `class-paths.js`, `class-draft-levels.js`, `spells.js`, `feats.js`, `resonance-economy.js`, `oracle-mysteries.js`, `oracle-curses.js`, `paladin-oaths.js`, and `prestige.js`; plus `RESONANCE_CANON.md`.

## 1. Method and assumptions

This is a paper audit. It compares what is written and implemented; it does **not** claim simulated encounter results.

- **Durability:** fixed HP from the published die rule with Constitution +2: d6 = **8 / 32 / 62**, d8 = **10 / 38 / 73**, d10 = **12 / 44 / 84**, d12 = **14 / 50 / 95** at L1 / L5 / L10. AC is grouped from the rulebook proficiency table: all armor + shield = sturdy; medium armor + shield = mid; light or no armor = fragile unless a class feature states a concrete alternative AC formula.
- **Damage sketch:** a mundane d8 attack with primary ability +3 / +4 / +5 and target AC 13 / 15 / 17 gives roughly **5.3 / 11.1 / 12.4 DPR** for one attack at L1 and two attacks at L5/L10, before class riders. It is a normalization point, not a claimed output for every class. Feature text that grants extra actions, attacks, damage multipliers, summons, or spell effects changes the category, but many lack complete action, duration, hit, and recharge rules.
- **Caster comparison:** reviewed RP at L1/L5/L10, the canonical `Resonance Rank × 2` base cost, short-rest Retune, Dissonance/Refrain, and each class-specific resource. All 14 Weave-casting base classes now use authoritative progression curves; Oracle uses Revelation Charges (RC), not RP.
- **Martial versus caster:** checked attack access, armor, stated burst/control/support features, spell/RP access, and level-5 progression. No class is marked “balanced” from prose alone.

## 2. Per-class snapshot

| Class | Durability | Damage | Primary role | Audit basis / confidence |
|---|---|---|---|---|
| Bard | mid | mid | support, control, flexible caster | Crescendo and songs; hybrid RP curve is authoritative, numeric song balance still needs testing |
| Cleric | mid | mid | divine support, control, durable caster | full RP table; domain numbers incomplete |
| Crimson Agent | fragile | high | precision striker, bleed/stealth | Blood Gauge/Blood Mark + bleed/stealth; armor-source reconciliation still needs testing |
| Dragoon | sturdy | high | mobile reach striker, burst engager | Momentum/leaps; minor RP curve is authoritative; armor source conflict remains |
| Druid | mid | mid | primal control, forms, flexible caster | full RP table; Shapeshifting stat blocks incomplete |
| Mage | fragile | high | broad arcane blaster/controller | full RP table; spell and school scaling incomplete |
| Monk | fragile | mid | mobile skirmisher, control | Ki/stanzas; minor RP curve is authoritative; AC feature tuning remains incomplete |
| Mirrorsage | fragile | high* | adaptive copier, utility/controller | copy ceiling still needs human stress testing; hybrid RP + Echo cadence locked |
| Oracle | fragile | high* | revelation support/control/burst | 3–7 RC; most Mystery/Curse trees are draft |
| Paladin | sturdy | high | armored striker, aura support, emergency healing | half RP curve is authoritative; many Oath payloads remain draft |
| Ranger | mid | mid | ranged/martial hunter, exploration | half RP curve is authoritative; mark damage/action tuning remains incomplete |
| Shaman | mid | mid | totem support/control, primal caster | hybrid RP curve is authoritative; totem payloads remain partly draft |
| Soldier | sturdy | mid | formation defender, ranged control | no RP; action/weapon math incomplete |
| Thief | fragile | high | precision striker, traps, stealth | Sneak Attack stated; minor RP curve is authoritative |
| Tinker | mid | high* | deployable control, ranged burst, support | device HP/damage/action economy incomplete; minor RP curve is authoritative |
| Warrior | sturdy | high | durable melee bruiser, mutation resource | d12 plus mutation stacking needs testing |
| Wizard | fragile | high | specialist arcane controller/blaster | full RP table; strongest verified casting pool |

\* High is a **risk flag**, not a verified DPR result: Mirrorsage copying, Oracle Revelations, and Tinker devices lack enough final numeric/action constraints to calculate a dependable output.

## 3. Outliers and imbalance risks

1. **Mirrorsage is the largest ceiling risk.** “Spell Mimicry,” stored Echoes, reduced RP costs, copied abilities, and later reflections do not define a universal eligibility list, target ceiling, action cost, or interaction with unique/boss effects. A copied stronger class feature can exceed its original owner while the Mirrorsage still retains its own kit.
2. **Oracle ranges from tightly bounded to effectively unbounded depending on selected draft content.** RC is only 3–7 and has no rest recovery, which is a real limiter; however several draft Prophecy Triggers can return RC once per round, and draft Revelations include extra actions, turn denial, rerolls, stabilization, or high-value prevention. The single rulebook-complete example cannot validate the other nine Mystery and nine Curse trees.
3. **Paladin compresses offense, AC, healing, aura support, and control.** The chassis is robust even before an Oath. Many Oath spell entries add hard control, rescue effects, immunity, or execution language without final resource, save, duration, targeting, or stacking rules. This can easily surpass Soldier/Warrior in party value if not bounded.
4. **Warrior and Dragoon have strong burst/durability packages but insufficient resource constraints.** Warrior begins with the highest HP curve and gains mutation slots, resistance, self-healing, and damage scaling; Dragoon combines mobility, armor, Momentum overflow, armor-ignore, and extra-action wording. Validate their action economy and encounter caps before comparing them to the lower-AC thief chassis.
5. **Tinker’s deployable multiplication is a control and damage risk.** Drone, turret, traps, bombs, three concurrent gadgets, remote detonation, and ally-safe detonation cannot be priced against normal attacks until each has finalized damage, HP, range, duration, action, recharge, and targeting rules.
6. **Caster/martial parity still needs human testing.** All 14 Weave classes now have authoritative RP curves and a Dissonance anti-spam layer, but spell damage, save DCs, preparation limits, and class-specific cadence reductions still need encounter-level tuning.

## 4. Resonance and RC fairness notes

- **Verified full RP pools:** at L10 Wizard 36, Mage 29, Cleric/Druid 27. At base tier-1 cost (2 RP), that is roughly 18/14/13 tier-1 casts before discounts, retunes, or higher-tier costs. This is only an endurance comparison.
- **Authoritative curves are not balance proof.** Half, hybrid, and minor progression curves are now canon for Paladin/Ranger; Bard/Shaman/Mirrorsage/Crimson Agent; and Dragoon/Monk/Thief/Tinker respectively. Their values are executable rules, but encounter-level tuning can still change them through an explicit balance revision.
- **Retune favors larger pools in absolute RP** (about one quarter of max plus casting modifier), while a flat ±1 faction cost modifier is proportionally much stronger for minor pools and low-tier spells. Test both short-rest-heavy and short-rest-scarce adventuring days.
- **Specialization discount remains unwired and unspecified.** A −1 to −3 RP discount can make tier-1 effects free under the stated cost formula. It needs an explicit floor, eligible spell list, and limit before evaluation.
- **Overcast remains a balance hotspot.** Empowered, Quickened, and Twinned can multiply output/action economy. Every Overcast now adds Dissonance and ordinary casters lose Overcast while Discordant, but numeric costs still need adversarial playtesting.
- **Oracle is not disadvantaged merely because it lacks RP:** RC recovery is trigger-based and can be functionally encounter-renewable. Test RC income, rather than comparing its 3–7 number directly to RP.
- **Approved multiclass rule:** use the highest caster-tier pool plus 25% of one secondary pool (rounded up); tertiary casters add none. This mitigates full-pool stacking, but it still needs combination tests for feature/action stacking and for a full caster paired with a high-value martial or RC Oracle.

## 5. Recommended playtest priorities

1. Run L1/L5/L10 four-character combats: Wizard, Paladin, Warrior, and a control/support slot, against a fixed encounter budget; record DPR, damage prevented, actions denied, and resource spent.
2. Stress test Mirrorsage against enemy spellcasters and bosses. Predeclare what may be copied, the stored-spell limit, action cost, duration, and exclusions before the test.
3. Test each Oracle Mystery/Curse separately with a strict “one RC recovered per round” ledger. Compare canon Ancestor/Shadow and Spiral-Touched against every draft profile; do not promote draft trees from anecdotal play.
4. Run Paladin, Soldier, and Warrior side by side in a protect-the-ally scenario. Measure aura value, interception, healing, AC, and control—not only damage.
5. Test Tinker, Shaman, and Ranger in grid encounters with terrain. Track every deployable/totem/mark action and total board occupancy.
6. Test RP in two day structures: two fights + frequent short rests and six fights + scarce short rests. Include a low-cost specialty spell, Refrain repetition, and one Overcast attempt. Reputation should alter access/support only, never intrinsic RP physics.
7. Test multiclass Resonance pairs: Wizard/Cleric, Paladin/Warrior, Mage/Mirrorsage, and an Oracle multiclass. Record pool, recovery, and turn economy separately.

## 6. What cannot be verified from data alone

- Final weapon lists, armor proficiencies, and AC formulas conflict between `rulebook_output.txt` and companion entries for Crimson Agent, Dragoon, Mirrorsage, Oracle, and Tinker.
- Most class abilities are descriptive rather than executable: action type, recharge, range, targeting, scaling, saving throw, damage die, duration, stacking, and conditions are often absent.
- No final enemy AC/HP/save benchmarks, encounter XP/budget, resistance frequency, adventuring-day cadence, or equipment/magic-item assumptions are provided.
- `spells.js` now carries class-specific rank/acquisition metadata for the reconciled 848-spell catalog. Remaining work is preparation/known limits, numeric scaling, and specialization eligibility—not class-tag cleanup.
- Feat and prestige prerequisites/effects, item access, and crafting output cannot be converted to a reliable class-power delta without finalized rules and acquisition rates.
- Only four RP tables and limited Oracle/Paladin source trees are rulebook-complete. The rest must remain draft and be playtested before mechanical parity can be claimed.

## Audit conclusion

The roster has identifiable roles and reasonable HP bands, but it is not yet numerically balance-verifiable. The urgent work is to turn high-impact prose into bounded rules, reconcile the source contradictions, and test the high-ceiling copy, revelation, aura, mutation, and deployable systems before adjusting class numbers.
