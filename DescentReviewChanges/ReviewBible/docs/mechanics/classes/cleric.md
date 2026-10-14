# Cleric — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/cleric.json) · [Normalized card data](../../../data/public/class_playtests/cleric.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Wisdom
- Secondary Attributes: Intelligence, Constitution
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light and medium armor, shields
- Weapon Proficiency: Simple weapons, deity-favored weapons
- Tool Proficiency: Religious implements

PROVISIONAL PLAYTEST CONTRACT. Wisdom is the Cleric class ability. S = 1/2/3/4 at Cleric levels 1/5/11/17. M = max(1, Wisdom modifier) unless a feature explicitly substitutes another ability. Cleric technique attack = d20 + normal character proficiency bonus + Wisdom modifier. Cleric technique save DC = 8 + normal character proficiency bonus + Wisdom modifier.

Conviction is separate from Resonance Points. Base Conviction maximum is 3, automatically becoming 5 at Cleric 9; after a long rest you begin at your current maximum. A completed short rest restores 1 spent Conviction, to the maximum. A completed long rest restores all Conviction. Conviction Pool raises the maximum by 2. Conviction persists between encounters; simply declaring prayer, repeating a Rite, or performing harmless actions outside a real encounter never generates Conviction.

Only explicit features generate Conviction. Sacred Chant, Sermon of Purpose, Doctrine Shield, Dark Conviction and other printed cards are valid generators. A feature cannot generate more Conviction than its text permits, and Conviction can never exceed the current maximum. Summoned creatures, friendly creatures, trivial creatures, repeated corpse manipulation and staged out-of-combat actions cannot be used to farm Conviction.

Cleric techniques use only their printed RP and Conviction costs. All RP is paid from the Cleric's Core Systems V 2 Resonance Point pool. A Cleric technique is not automatically an ordinary spell-rank cast and does not receive Overcast, spell-slot, cost-discount or spell-proc benefits unless a feature explicitly says otherwise. Ordinary spells continue to use Core V 2 spellcasting rules.

Protected Dissonance interaction: once on each of your regular turns, when you spend at least 2 Conviction on a Rite or Invocation, reduce Dissonance by 1, minimum 0. The expenditure must actually occur; waived Conviction costs do not vent Dissonance. A single feature expenditure vents at most once even if it spends more than 2 Conviction. No Cleric card automatically adds Dissonance unless explicitly written.

One concentration effect may be maintained at a time. Starting another concentration effect immediately ends the previous one. Damage uses the current Core Systems concentration rule; for this pilot, if a division requires rounding, half damage is rounded down. Sustained Cleric effects use their printed maintenance cost and Bonus Action. A control effect that persists for multiple pulses or rounds gives the target a new save at each printed pulse or at the end of each affected turn as stated.

Round recharge counters are set after resolution and decrease once at the start of the Cleric's regular initiative turn, even if the Cleric cannot act. Extra Actions and extra turns do not create extra recharge ticks. Outside initiative, each uninterrupted 6 seconds counts as one recharge tick. Only a positive counter may be reset or shortened, and a named ability can receive at most one reset or shortening per round.

Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.

Invocation Attunement is gained automatically at Cleric level 2. Choose exactly one Invocation Path: Radiance, Judgment, Renewal, Flame, Veil or Echoes. Only the selected path bonus becomes active. Divine Invocation uses the mode belonging to that selected path unless another feature explicitly permits a different mode. Changing Invocation Path requires a future explicit retraining rule; this draft provides none.

PROPOSED ACQUISITION FOR PLAYTEST. Cleric 1: gain the Divine Favor engine and choose 4 Base cards, at least 2 Active. Cleric 2: automatically gain Invocation Attunement and the selected Invocation Path bonus, then choose 2 additional Base cards. Cleric 3: enter Bishop and choose 2 Arch cards, at least 1 Active. Levels 4-8 each grant one eligible Base/Arch choice, respecting each card's minimum class level. Level 9 grants one eligible Arch choice plus Bishop's Mandate automatically. Level 10 choose Saint, Priest or Cultist and gain 2 Hero choices from that path. Levels 12, 14, 16 and 18 each grant one additional Hero choice; levels 11, 13, 15, 17 and 19 grant one eligible unselected Base/Arch choice. The chosen Hero Finale is automatic at Cleric 20. ASI/feat milestones remain separate and do not consume these choices.

All acquisition gates use Cleric class level, not total character level. Proficiency bonus still follows normal total-character-level rules. A multiclass character cannot use non-Cleric levels to unlock Bishop, Hero, Invocation or Finale features. Divine commands, visions and social abilities can influence actions only to the extent their exact mechanical text states; no Cleric feature can force a player character to adopt, abandon or profess a belief.

Capacity clarification: the automatic level 9 Conviction increase is a new draft completion so every Hero can pay its 5-Conviction Finale without buying Conviction Pool. Conviction Pool adds 2 at any level, yielding 5 early or 7 from 9. It never fills gained capacity immediately.

**Protected source interface:** Once per turn, spending 2 or more Conviction on a Rite or Invocation vents 1 Dissonance; prayer changes cadence instead of bypassing Resonance.

## Advancement and resources

RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 3 | 1 | Choose 4 Base; at least 2 active |
| 2 | Base | 4 | 1 | Choose 2 Base; automatic: Invocation Attunement, Radiance (Radiance), Judgment (Judgment), Renewal (Renewal), Flame (Flame), Veil (Veil), Echoes (Echoes) |
| 3 | Arch | 7 | 2 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 9 | 2 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 12 | 3 | Choose 1 Base/Arch |
| 6 | Arch | 15 | 3 | Choose 1 Base/Arch |
| 7 | Arch | 18 | 4 | Choose 1 Base/Arch |
| 8 | Arch | 21 | 4 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 24 | 5 | Choose 1 Arch; automatic: Bishop's Mandate |
| 10 | Hero | 27 | 5 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 30 | 6 | Choose 1 Base/Arch |
| 12 | Hero | 33 | 6 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 36 | 7 | Choose 1 Base/Arch |
| 14 | Hero | 39 | 7 | Choose 1 Hero |
| 15 | Hero | 42 | 8 | Choose 1 Base/Arch |
| 16 | Hero | 45 | 8 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 48 | 9 | Choose 1 Base/Arch |
| 18 | Hero | 51 | 9 | Choose 1 Hero |
| 19 | Hero | 54 | 9 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 58 | 9 | No ordinary selection; automatic: Celestial Resurgence (Saint), Word of Binding (Priest), Rite of the Crimson Choir (Cultist) |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Cleric 5 example: Wisdom 16 gives M=3, PB=3, S=2. Assume the Core V 2 sheet gives this test Cleric 12 RP. The Cleric knows Conviction Pool, so maximum Conviction is 5, begins the encounter at Conviction 5, Dissonance 3, and selected Judgment at level 2.
2. Turn 1: Divine Smite costs 1 Conviction, so Conviction 5→4 and RP remains 12. On a hit it deals 2d8+3 radiant damage. Judgment automatically marks the target Judged for 2 rounds, giving it -1 AC. Spending only 1 Conviction does not vent Dissonance.
3. Turn 2: Divine Invocation costs 2 Conviction and 3 RP, so Conviction 4→2 and RP 12→9. Because an Invocation spent at least 2 Conviction, Dissonance vents once, 3→2. Using Judgment mode, a failed Wisdom save causes the printed 3d8 radiant effect and refreshes Judged.
4. Turn 3: Healing Rite costs 2 RP, so RP 9→7. It restores 2d8+3 HP to one living ally. It spends no Conviction, so Conviction remains 2 and Dissonance remains 2. If the ally stood in the Cleric's Consecrate zone and Consecrated Ground was known, the target would also regain the printed S=2 bonus HP.
5. Turn 4: Sacred Chant costs 1 RP to start, so RP 7→6. Its first pulse occurs, but generates no Conviction yet. The Cleric concentrates on the Chant. Conviction stays 2.
6. Turn 5: The Cleric maintains Sacred Chant with a Bonus Action. Because Sermon of Purpose is known, the second pulse generates 1 Conviction, 2→3. The Cleric then uses Divine Smite as the normal Action, spending 1 Conviction, 3→2. RP remains 6 and Dissonance remains 2 because no single Rite or Invocation expenditure of at least 2 Conviction occurred this turn.

## Base cards

#### Conviction Pool

**Level 1 · selection · cleric.base.conviction-pool**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Passive | Always |

Conviction Pool. Tags: conviction, passive. Increase your Conviction maximum by 2. This changes only the maximum; it does not immediately restore spent Conviction when acquired during play. A long rest restores Conviction to the new maximum.

<details><summary>Preserved source wording — book line1967</summary>

Conviction Pool: +2 max Conviction cap.

</details>

#### Consecrated Ground

**Level 1 · selection · cleric.base.consecrated-ground**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Passive | Always |

Consecrated Ground. Tags: rite, healing, passive. Whenever one of your healing Rites restores HP to a living creature standing in terrain created by your Consecrate feature, that creature regains S additional HP. Apply this once per creature per Rite pulse; it is flat healing and is not itself another healing trigger.

<details><summary>Preserved source wording — book line1968</summary>

Consecrated Ground: Healing allies on terrain you sanctify (via Rite) heals for +10%.

</details>

#### Judging Light

**Level 1 · selection · cleric.base.judging-light**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Passive | Always |

Judging Light. Tags: smite, passive. When your Divine Smite damages a creature currently affected by a Cursed or Weakened condition, add S d4 radiant damage to that Smite. Roll these dice once as part of the Smite; they do not create a second hit or trigger.

<details><summary>Preserved source wording — book line1969</summary>

Judging Light: Smite deals +20% bonus damage to enemies afflicted by Cursed or Weakened effects.

</details>

#### Fervent Ritualist

**Level 1 · selection · cleric.base.fervent-ritualist**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Passive | Always |

Fervent Ritualist. Tags: rite, ritual, passive. When a Rite with a Ritual activation normally requires at least 10 minutes, reduce its required time by 1 minute for each full 10 minutes of its printed casting time. This never reduces a Ritual below 1 minute and does not alter Action, Bonus Action or Reaction Rites.

<details><summary>Preserved source wording — book line1970</summary>

Fervent Ritualist: +10% faster channel speed on all Rites.

</details>

#### Invocation Attunement

**Level 2 · automatic · cleric.base.invocation-attunement**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic at Cleric 2 |

Invocation Attunement. Tags: invocation, core. At Cleric level 2 choose exactly one Invocation Path: Radiance, Judgment, Renewal, Flame, Veil or Echoes. You automatically gain that path's listed bonus. Divine Invocation thereafter uses that path's mode unless another feature explicitly overrides it.

<details><summary>Preserved source wording — book line1971</summary>

Invocation Attunement: Choose one Invocation Path (see below); gain a permanent passive tied to it.

</details>

### Radiance

#### Radiance

**Level 2 · automatic · cleric.base.radiance.radiance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic only if Radiance was selected |

Invocation Path — Radiance. Tags: invocation, radiance, healing. Once on each of your turns when one of your Rites restores HP to at least one living creature, choose one creature healed by that Rite. It regains S additional HP and may immediately end either Frightened or Poisoned on itself.

<details><summary>Preserved source wording — book line1974</summary>

Radiance: +10% healing power and heals cleanse minor conditions.

</details>

### Judgment

#### Judgment

**Level 2 · automatic · cleric.base.judgment.judgment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic only if Judgment was selected |

Invocation Path — Judgment. Tags: invocation, judgment, smite. When your Divine Smite deals damage to a creature, mark it Judged for 2 rounds. A Judged creature has -1 AC. Further applications refresh the duration but do not increase the AC penalty.

<details><summary>Preserved source wording — book line1975</summary>

Judgment: Smites mark enemies with Judged for 2 rounds, reducing their AC by 1.

</details>

### Renewal

#### Renewal

**Level 2 · automatic · cleric.base.renewal.renewal**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic only if Renewal was selected |

Invocation Path — Renewal. Tags: invocation, renewal, healing, rite. Once per use of a healing Rite, choose one creature that actually regained HP from it. That creature also restores 5 Stamina, not exceeding its Stamina maximum. A creature without a Stamina resource receives no secondary benefit.

<details><summary>Preserved source wording — book line1976</summary>

Renewal: Healing Rites restore 5 stamina to the target.

</details>

### Flame

#### Flame

**Level 2 · automatic · cleric.base.flame.flame**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 Conviction | One creature damaged by your Smite or Rite | 2 rounds | At most once on each of your turns |

Invocation Path — Flame. Tags: invocation, flame. Immediately after your Smite or Rite damages a creature, you may spend 1 Conviction. The target ignites and takes 1d6 fire damage at the start of each of its next 2 turns. Reapplying Flame refreshes the duration; the burning damage does not stack.

<details><summary>Preserved source wording — book line1977</summary>

Flame: Conviction can be consumed to ignite targets for 2 turns (fire DoT).

</details>

### Veil

#### Veil

**Level 2 · automatic · cleric.base.veil.veil**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic only if Veil was selected |

Invocation Path — Veil. Tags: invocation, veil, sight. You can see invisible and ethereal creatures and objects within 30 feet that are not behind total cover. This does not reveal mundane disguises, automatically defeat illusions, or let you see through opaque barriers.

<details><summary>Preserved source wording — book line1978</summary>

Veil: Gain passive True Sight vs invisible or ethereal creatures.

</details>

### Echoes

#### Echoes

**Level 2 · automatic · cleric.base.echoes.echoes**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One original target within 30 feet | Until start of your next regular turn | At most one pending Echoes-path repeat |

Invocation Path — Echoes. Tags: invocation, echoes. Once on each of your turns after a Smite or Rite produces rolled immediate damage or healing, store one original target and that raw dice total. At the start of your next regular turn, if the target is legal, repeat floor(raw dice total/10), minimum 1 for a positive total, as the same damage or healing type. This repeat carries no conditions, resources or triggers.

<details><summary>Preserved source wording — book line1979</summary>

Echoes: 10% of healing or damage is repeated 1 turn later (Echo Effect).

</details>

#### Divine Smite

**Level 1 · selection · cleric.base.divine-smite**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 Conviction | One enemy within 60 feet | Instantaneous | At will |

Divine Smite. Tags: smite, divine. Make a Cleric technique attack against one enemy. On a hit, deal S d8 + M radiant damage. This is one damage event. Invocation Path bonuses and features explicitly referring to Smite may modify it.

<details><summary>Preserved source wording — book line1982</summary>

Divine Smite: Channel divine energy into a powerful strike against a single enemy, dealing damage based on your Wisdom and consuming 1 Conviction.

</details>

#### Healing Rite

**Level 1 · selection · cleric.base.healing-rite**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One living ally within 30 feet | Instantaneous | At will while RP remains |

Healing Rite. Tags: rite, healing. One living ally regains S d8 + M HP. It cannot restore a dead creature or remove Wounds. Consecrated Ground and appropriate Invocation Path bonuses may modify this healing.

<details><summary>Preserved source wording — book line1983</summary>

Healing Rite: A channeled ability that restores health to an ally, with increased effectiveness on consecrated ground.

</details>

#### Sacred Chant

**Level 1 · selection · cleric.base.sacred-chant**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP to start; 0 RP maintenance | Self; audible 15-foot prayer aura | Concentration, maximum 3 Cleric turns | At will while RP remains |

Sacred Chant. Tags: chant, sustained, conviction. Pulse on start and once when maintained on each later regular turn with a Bonus Action. Under the base feature, the third pulse generates 1 Conviction. Only a real encounter can generate Conviction this way. Maintenance itself does not otherwise heal, damage or grant Conviction.

<details><summary>Preserved source wording — book line1984</summary>

Sacred Chant: A sustained prayer that generates 1 Conviction every 3 turns while maintained.

</details>

#### Consecrate

**Level 1 · selection · cleric.base.consecrate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | 15-foot-radius fixed zone centered at a point within 30 feet | 3 rounds | Recharge 3 rounds |

Consecrate. Tags: rite, zone. Create sanctified terrain. Your Consecrated Ground feature recognizes this zone. Undead creatures in the zone have -1 on attack rolls. A creature leaving the zone loses that penalty immediately. Only one Consecrate zone created by you may exist at a time; creating another ends the first.

<details><summary>Preserved source wording — book line1985</summary>

Consecrate: Sanctify the ground in a 15-foot radius, creating consecrated terrain that enhances your healing abilities and weakens undead enemies.

</details>

#### Divine Insight

**Level 1 · selection · cleric.base.divine-insight**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 1 RP | Self; subject matter concerning a religious matter, sacred location or divine presence | 10 minutes | 1/short rest |

Divine Insight. Tags: ritual, information. Ask the Director one specific factual question about a religious practice, sacred location, divine presence or recognized supernatural sign available to your tradition. Receive one truthful fact, symbolic clue or 'unknown' if the information is genuinely unavailable. This never forces certainty about future events or another character's private beliefs.

<details><summary>Preserved source wording — book line1986</summary>

Divine Insight: Commune briefly with your deity to gain insight about a religious matter, sacred location, or divine presence.

</details>

## Arch cards

#### Aura of Faith

**Level 3 · selection · cleric.arch.aura-of-faith**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies within 15 feet who can perceive you | Passive while conscious | Always |

Aura of Faith. Tags: aura, bishop. Allies in the aura gain +1 on saving throws. Whenever your Rite restores HP to an ally in the aura, that ally also regains 1 additional HP. Multiple Aura of Faith bonuses do not stack.

<details><summary>Preserved source wording — book line1992</summary>

Aura of Faith: Allies in range gain +5% healing received and +1 to saves.

</details>

#### Sermon of Purpose

**Level 3 · selection · cleric.arch.sermon-of-purpose**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Sacred Chant | Passive | Always |

Sermon of Purpose. Tags: chant, conviction, bishop. Sacred Chant generates its 1 Conviction on its second pulse instead of its third. A normal three-pulse Sacred Chant still generates only 1 Conviction total unless another feature explicitly extends it or grants an additional generation event.

<details><summary>Preserved source wording — book line1993</summary>

Sermon of Purpose: Chants now generate 1 Conviction every 2 turns.

</details>

#### Liturgical Flow

**Level 5 · selection · cleric.arch.liturgical-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until used or sequence breaks | At most once per round |

Liturgical Flow. Tags: rite, invocation, recharge. If you start Rites on two consecutive regular turns, your next Divine Invocation started before the end of your following regular turn sets its printed round-recharge counter 1 lower, minimum 0. This counts as Divine Invocation's one allowed reset or shortening for that round.

<details><summary>Preserved source wording — book line1994</summary>

Liturgical Flow: Chaining 2 Rites reduces cooldown of your next Invocation by 1 turn.

</details>

#### Anointed Guardian

**Level 5 · selection · cleric.arch.anointed-guardian**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | First ally within 30 feet to fall to one-quarter maximum HP or less | 2 rounds | Once per encounter |

Anointed Guardian. Tags: protection, bishop. The first qualifying ally in an encounter gains a ward for 2 rounds. The first time during each round that ally takes damage, reduce that damage by PB + M, minimum 0. The ward does not prevent conditions attached to an attack unless the damage reduction itself invalidates them under another rule.

<details><summary>Preserved source wording — book line1995</summary>

Anointed Guardian: First time an ally drops below 20% HP per combat, grant them a 30% damage reduction shield for 2 rounds.

</details>

#### Sanctified Reprisal

**Level 7 · selection · cleric.arch.sanctified-reprisal**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until end of your next regular turn | At most once per turn |

Sanctified Reprisal. Tags: healing, smite, bishop. After one of your Cleric features restores HP to a living creature, empower your next Divine Smite before the end of your next regular turn. On a hit it deals S d4 additional radiant damage. If the target is Undead, it must also make a Constitution save; failure Stuns it until the end of its next turn.

<details><summary>Preserved source wording — book line1996</summary>

Sanctified Reprisal: Whenever you heal, next Smite deals 20% more damage and stuns Undead.

</details>

#### Miraculous Channel

**Level 7 · selection · cleric.arch.miraculous-channel**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 Conviction | Your next ally-targeting Rite this turn | Until end of current turn | At will while Conviction remains |

Miraculous Channel. Tags: rite, channel, bishop. Your next Rite this turn that normally affects one or more willing allies may affect up to six legal willing allies within the Rite's normal range instead. Roll shared healing or numeric effects once and apply normally. It does not multiply hostile targets, corpse targets or resource generation.

<details><summary>Preserved source wording — book line1997</summary>

Miraculous Channel: Sacrificing 3 Conviction causes your next Rite to affect the full party.

</details>

#### Bishop's Mandate

**Level 9 · automatic · cleric.arch.bishop-s-mandate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Your Sacrament and one legal Divine Invocation target set | Instantaneous | Automatic at Cleric 9; once per Sacrament start |

Bishop's Mandate. Tags: sacrament, invocation, capstone. When you legally start Sacrament, immediately resolve one free Divine Invocation using your selected Invocation Path. This free Invocation requires no Action, RP or Conviction, sets no Divine Invocation recharge and cannot itself trigger Bishop's Mandate. The Sacrament's own Conviction expenditure may still vent Dissonance normally.

<details><summary>Preserved source wording — book line1998</summary>

Capstone: Bishop's Mandate: Activating a Sacrament automatically casts a free Invocation without cost or cooldown.

</details>

#### Divine Invocation

**Level 3 · selection · cleric.arch.divine-invocation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 Conviction + 3 RP | Mode-dependent; maximum 60 feet | Instantaneous unless mode states otherwise | Recharge 3 rounds |

Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers.

<details><summary>Preserved source wording — book line2001</summary>

Divine Invocation: Channel a powerful prayer based on your chosen Invocation Path, with effects ranging from mass healing to divine fire or protective barriers.

</details>

#### Sacrament

**Level 3 · selection · cleric.arch.sacrament**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Conviction + 4 RP to start; 1 RP maintenance | 15-foot-radius fixed zone centered within 30 feet | Concentration, maximum 3 Cleric turns | Recharge 4 rounds |

Sacrament. Tags: sacrament, rite, sustained, zone. Pulse on start and on each paid Bonus Action maintenance. At each pulse, up to three allies in the zone gain +1 on saving throws until the start of your next regular turn or effect end, whichever is first. Up to three Undead or Fiends in the zone make Wisdom saves, taking S d6 radiant damage on failure or half on success. Maximum 3 pulses.

<details><summary>Preserved source wording — book line2002</summary>

Sacrament: Perform a sacred ceremony that consumes Conviction to create a powerful, sustained effect in an area.

</details>

#### Banish Unholy

**Level 5 · selection · cleric.arch.banish-unholy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Up to three Undead or Fiends within 30 feet | Instantaneous; banishment rider lasts until end of target's next turn | Recharge 3 rounds |

Banish Unholy. Tags: divine, control. Each target makes a Wisdom save. Failure deals (S+1)d8 radiant damage and pushes it up to 15 feet directly away from you; success takes half damage and no push. A target failing by 10 or more is also banished until the end of its next turn, then returns to the nearest legal space.

<details><summary>Preserved source wording — book line2003</summary>

Banish Unholy: Channel divine energy to damage and potentially banish undead, demons, or other unholy entities.

</details>

#### Blessing of Protection

**Level 7 · selection · cleric.arch.blessing-of-protection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One living ally within 30 feet | Concentration, maximum 3 rounds | Recharge 3 rounds |

Blessing of Protection. Tags: blessing, protection. Choose one mode on use. Resistance: choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder; the ally gains resistance to that damage type. Resolve: choose Charmed, Frightened or Poisoned; the ally gains advantage on saves against that condition and may immediately repeat one current save against it.

<details><summary>Preserved source wording — book line2004</summary>

Blessing of Protection:  Bestow a divine blessing on an ally, granting them resistance to a specific damage type or condition.

</details>

#### Commune

**Level 9 · selection · cleric.arch.commune**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 5 RP | Self | 10 minutes | 1/long rest |

Commune. Tags: ritual, information, bishop. Ask up to three questions concerning divine doctrine, sacred duties, supernatural threats or a course of action. For each, the Director answers truthfully with yes, no, unclear or a brief symbolic response based on what the contacted divine source could know. Commune cannot compel a deity, reveal another player's private belief, or guarantee a future choice.

<details><summary>Preserved source wording — book line2005</summary>

Commune:  Enter a deep meditative state to receive guidance directly from your deity, gaining insight on important matters or divine intervention.

</details>

## Hero cards

### Saint

#### Aura of Grace

**Level 10 · selection · cleric.hero.saint.aura-of-grace**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered and passive | 1 RP per healing pulse | Living allies within 15 feet | Passive during real encounters | Healing once/own regular turn; critical reduction once/ally/round |

Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.

<details><summary>Preserved source wording — book line2014</summary>

Aura of Grace: Allies in range resist critical hits and gain minor HP regen.

</details>

#### Divine Rebirth

**Level 12 · selection · cleric.hero.saint.divine-rebirth**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One ally revived by your Cleric feature | Instantaneous plus temporary HP for 1 minute | 1/long rest |

Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.

<details><summary>Preserved source wording — book line2015</summary>

Divine Rebirth: On revive, ally returns with 50% HP and a temporary resistance shield.

</details>

#### Merciful Sacrament

**Level 14 · selection · cleric.hero.saint.merciful-sacrament**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Sacrament | For that activation | 1/short rest |

Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.

<details><summary>Preserved source wording — book line2016</summary>

Merciful Sacrament: Sacraments cost no Conviction if used on an ally under 25% HP.

</details>

#### Unyielding Light

**Level 16 · selection · cleric.hero.saint.unyielding-light**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Up to six living party members within 30 feet, including you | Instantaneous | 1/long rest |

Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.

<details><summary>Preserved source wording — book line2017</summary>

Unyielding Light: Once per day, prevents party wipe and restores 30% HP.

</details>

#### Celestial Resurgence

**Level 20 · automatic · cleric.hero.saint.celestial-resurgence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Conviction + 10 RP | Up to six allied corpses within 30 feet that died during the previous 3 rounds | Instantaneous | 1/long rest |

Final Miracle — Celestial Resurgence. Tags: saint, finale, resurrection, rite. Each legal target returns to life at 1 HP. The body must be sufficiently present to sustain life. This removes no Wounds, curses or other death consequences. Divine Rebirth may modify one returned ally if available. The Conviction expenditure can vent Dissonance once under the common rule.

<details><summary>Preserved source wording — book line2018</summary>

Final Miracle: Celestial Resurgence: Revive all allies who died within the last 3 turns.

</details>

#### Mass Healing Light

**Level 10 · selection · cleric.hero.saint.mass-healing-light**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | Up to six living allies within 30 feet | Instantaneous | Recharge 3 rounds |

Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.

<details><summary>Preserved source wording — book line2021</summary>

Mass Healing Light: Channel divine energy to heal all allies within 30 feet, with increased effectiveness on those most wounded.

</details>

#### Divine Intervention

**Level 10 · selection · cleric.hero.saint.divine-intervention**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 4 RP | One ally within 60 feet | Instantaneous | 1/long rest |

Divine Intervention. Tags: saint, emergency. Trigger when the ally either fails a saving throw or takes damage that would reduce it to 0 HP. Choose one: the ally rerolls the failed save and must use the new result; or reduce the triggering damage by 2 S d8 + M, minimum 0. This cannot negate an event that has already fully resolved.

<details><summary>Preserved source wording — book line2022</summary>

Divine Intervention: Call upon your deity to intervene directly, potentially averting disaster or creating a miraculous effect.

</details>

#### Sanctify Being

**Level 12 · selection · cleric.hero.saint.sanctify-being**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | One living ally within 30 feet | Concentration, maximum 3 rounds | Recharge 4 rounds |

Sanctify Being. Tags: saint, protection. Choose one mode. Elemental Sanctity grants resistance to one of acid, cold, fire, lightning, necrotic, poison, radiant or thunder. Purity grants immunity to exactly one of Charmed, Frightened or Poisoned. Choose when activated; the choice cannot change during that use.

<details><summary>Preserved source wording — book line2023</summary>

Sanctify Being: Bestow temporary divine protection on an ally, granting them immunity to specific conditions or damage types.

</details>

#### Radiant Burst

**Level 14 · selection · cleric.hero.saint.radiant-burst**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP | 15-foot radius centered on you; up to six allies and six Undead/Fiends | Instantaneous | Recharge 4 rounds |

Radiant Burst. Tags: saint, healing, radiant. Roll S d8 once. Each chosen living ally regains that roll + M HP. Each chosen Undead or Fiend makes a Wisdom save, taking the same S d8 roll as radiant damage on failure or half on success. Healing and damage are separate applications of the shared roll.

<details><summary>Preserved source wording — book line2024</summary>

Radiant Burst: Release a powerful wave of divine energy that heals allies and damages unholy creatures.

</details>

#### Resurrection

**Level 16 · selection · cleric.hero.saint.resurrection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Conviction + 10 RP | One allied corpse you touch that died within the previous 1 minute | Instantaneous | 1/long rest |

Resurrection. Tags: saint, resurrection, rite. Return the target to life at 1 HP and grant it 2 S + M temporary HP for 1 minute. It gains no removed Wounds and receives no restored expended resources beyond what another rule explicitly provides. A missing vital body prevents the effect. The Conviction expenditure can vent Dissonance once.

<details><summary>Preserved source wording — book line2025</summary>

Resurrection: Return a fallen ally to life with renewed vigor and temporary divine blessing.

</details>

### Priest

#### Scriptural Echo

**Level 10 · selection · cleric.hero.priest.scriptural-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One legal original target of your previously used Divine Invocation | Instantaneous | 1/short rest |

Scriptural Echo. Tags: priest, rite, invocation. When you start a Rite, you may repeat 50% of the immediate rolled damage or healing dice from the most recent Divine Invocation you personally resolved since the end of your previous regular turn. Round down once, minimum 1 for a positive source. It copies no conditions, movement, resource effects, control or Invocation Path triggers.

<details><summary>Preserved source wording — book line2031</summary>

Scriptural Echo: Casting a Rite repeats the Invocation used previously for 50% effect.

</details>

#### Words of Equilibrium

**Level 10 · selection · cleric.hero.priest.words-of-equilibrium**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Passive | Always |

Words of Equilibrium. Tags: priest, scaling. For numeric Cleric technique healing and damage that would add your Wisdom modifier, use the higher of your Intelligence or Wisdom modifier instead. M becomes max(1, that higher modifier) for those numeric effects. This does not change Cleric attack rolls or save DCs unless another rule explicitly says so.

<details><summary>Preserved source wording — book line2032</summary>

Words of Equilibrium: Heal and Damage dealt scale off the higher of INT or WIS.

</details>

#### Balanced Scales

**Level 12 · selection · cleric.hero.priest.balanced-scales**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Living creatures healed by your Cleric features | Until start of your next regular turn | At most once per marked ally per round |

Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event.

<details><summary>Preserved source wording — book line2033</summary>

Balanced Scales: Enemies take divine damage if they attack healed targets.

</details>

#### Doctrine Shield

**Level 14 · selection · cleric.hero.priest.doctrine-shield**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Instantaneous | At most once per round |

Doctrine Shield. Tags: priest, conviction, cleanse. During a real encounter, when one of your Cleric features successfully removes Charmed, Frightened, Poisoned or another explicitly removable condition from a living creature, gain 1 Conviction. Removing multiple conditions in the same event still grants only 1 Conviction.

<details><summary>Preserved source wording — book line2034</summary>

Doctrine Shield: Gain 1 Conviction anytime a condition is removed.

</details>

#### Word of Binding

**Level 20 · automatic · cleric.hero.priest.word-of-binding**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Conviction + 8 RP | Up to six enemies within 30 feet | Concentration, maximum 3 rounds | 1/long rest |

Final Miracle — Word of Binding. Tags: priest, finale, control, rite. Each target makes a Wisdom save. On failure it is Silenced and its Speed becomes 0. At the end of each of its turns it repeats the save, ending both effects on success. While a target remains bound, the first instance of divine or radiant damage it takes each round gains S d6 additional radiant damage. The Conviction expenditure can vent Dissonance once.

<details><summary>Preserved source wording — book line2035</summary>

Final Miracle: Word of Binding: Enemies in a large AoE are silenced, snared, and take +25% divine damage for 3 turns.

</details>

#### Balance Restoration

**Level 10 · selection · cleric.hero.priest.balance-restoration**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | 15-foot-radius area centered at a point within 30 feet | Instantaneous | Recharge 3 rounds |

Balance Restoration. Tags: priest, healing, radiant. Choose up to three living allies and three enemies in the area. Roll S d8 once. Each ally regains the roll + M HP. Each enemy makes a Wisdom save, taking the same S d8 roll as radiant damage on failure or half on success.

<details><summary>Preserved source wording — book line2038</summary>

Balance Restoration: Channel divine energy that both heals allies and damages enemies in an area, maintaining cosmic balance.

</details>

#### Divine Judgment

**Level 10 · selection · cleric.hero.priest.divine-judgment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy within 60 feet | Concentration, maximum 3 rounds | Recharge 3 rounds |

Divine Judgment. Tags: priest, judgment. The target makes a Wisdom save; success ends the attempt. On failure it is marked. The first time on each of its turns that it deals damage to another creature, it takes radiant damage equal to half that actual damage rounded down, minimum 1, maximum your Cleric level. It repeats the Wisdom save at the end of each turn, ending the mark on success.

<details><summary>Preserved source wording — book line2039</summary>

Divine Judgment: Mark an enemy for judgment, causing them to take damage proportional to the harm they inflict.

</details>

#### Ritual of Cleansing

**Level 12 · selection · cleric.hero.priest.ritual-of-cleansing**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | Up to three living allies within 30 feet; secondary enemies within 15 feet of you | Instantaneous | Recharge 3 rounds |

Ritual of Cleansing. Tags: priest, rite, cleanse. Each ally may end one of Charmed, Frightened or Poisoned. For each distinct condition actually removed, choose one enemy within 15 feet; each chosen enemy makes a Wisdom save. On failure it becomes Frightened of you until the end of its next turn. One enemy can be chosen only once per use.

<details><summary>Preserved source wording — book line2040</summary>

Ritual of Cleansing: Perform a ritual that removes multiple negative conditions from allies while potentially imposing them on enemies.

</details>

#### Word of Power

**Level 14 · selection · cleric.hero.priest.word-of-power**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | One creature within 30 feet | Instantaneous | Recharge 2 rounds |

Word of Power. Tags: priest, divine. Choose one mode. Mercy: one willing living creature regains S d8+M HP. Rebuke: one Undead or Fiend makes a Constitution save, taking (S+1)d8 radiant on failure or half on success; failure also removes its Reaction until the start of its next turn. Command: one other hostile creature makes a Wisdom save; failure knocks it Prone and removes its Reaction until the start of its next turn. No mode changes beliefs, loyalty or ideology.

<details><summary>Preserved source wording — book line2041</summary>

Word of Power: Speak a divine word that has different effects based on the target's nature and actions.

</details>

#### Cosmic Equilibrium

**Level 16 · selection · cleric.hero.priest.cosmic-equilibrium**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 7 RP | 15-foot-radius fixed zone centered within 30 feet | Concentration, maximum 3 rounds | 1/short rest |

Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.

<details><summary>Preserved source wording — book line2042</summary>

Cosmic Equilibrium: Create a zone where healing and harm are balanced, converting excess damage to healing and vice versa.

</details>

### Cultist

#### Sanguine Rite

**Level 10 · selection · cleric.hero.cultist.sanguine-rite**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self and one ally within 30 feet | Instantaneous | At most once on each of your turns |

Sanguine Rite. Tags: cultist, rite, healing. When one of your Rites deals damage to at least one enemy, choose one living ally within 30 feet. That ally regains HP equal to half the actual damage dealt to one chosen damaged enemy, rounded down, maximum S+M HP. This healing cannot trigger Sanguine Rite again.

<details><summary>Preserved source wording — book line2048</summary>

Sanguine Rite:  Rites damage enemies and heal allies for a portion of the same amount.

</details>

#### Blasphemous Tongue

**Level 10 · selection · cleric.hero.cultist.blasphemous-tongue**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Enemies affected by your Sacrament | Until the next Sacrament pulse or effect end | Once per target per pulse |

Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack.

<details><summary>Preserved source wording — book line2049</summary>

Blasphemous Tongue: Sacraments inflict Doomed, reducing healing received and buff duration.

</details>

#### Dark Conviction

**Level 12 · selection · cleric.hero.cultist.dark-conviction**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Instantaneous | At most once on each of your turns |

Dark Conviction. Tags: cultist, conviction. During a real encounter, when a hostile non-summoned creature that meaningfully threatened the party dies after taking damage from one of your Cleric features since the start of your current turn, gain 1 Conviction. Friendly creatures, summoned creatures, trivial staged creatures and repeated corpse destruction never qualify.

<details><summary>Preserved source wording — book line2050</summary>

Dark Conviction: Killing an enemy grants 1 Conviction instantly.

</details>

#### Zealot's Touch

**Level 14 · selection · cleric.hero.cultist.zealot-s-touch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Healing-over-time Rites you control | Passive | Always |

Zealot's Touch. Tags: cultist, rite, necrotic. When starting a Rite whose printed pulse would restore HP over multiple turns, you may designate a hostile creature instead of a healing recipient. At each applicable pulse that enemy makes a Wisdom save. On failure it takes necrotic damage equal to the Rite's rolled healing dice; on success it takes half. Flat healing bonuses are not converted. The enemy receives no healing.

<details><summary>Preserved source wording — book line2051</summary>

Zealot's Touch: Healing over time effects become life drain if cast on enemies.

</details>

#### Rite of the Crimson Choir

**Level 20 · automatic · cleric.hero.cultist.rite-of-the-crimson-choir**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Conviction + 8 RP | Four unoccupied spaces within 30 feet | Concentration, maximum 3 rounds | 1/long rest |

Final Miracle — Rite of the Crimson Choir. Tags: cultist, finale, summon, rite. Summon four spectral fanatics. Each has AC 14, 10 HP, Speed 30 feet and cannot take Reactions. Spend one Bonus Action on your regular turn to command the Choir; this explicitly priced Finale permits up to four surviving fanatics to each move up to its Speed and make one melee spell-like attack using your Cleric technique attack bonus against an enemy within 5 feet; on hit it deals 1d6+S necrotic damage and you regain 1 HP, maximum 4 HP per round from the Choir. When a fanatic reaches 0 HP, when concentration ends or after the third round, it explodes; enemies within 5 feet make Dexterity saves, taking 1d6 necrotic on failure or half on success. Fanatics grant no XP, loot, corpse, resurrection target or Conviction. The Conviction expenditure can vent Dissonance once.

<details><summary>Preserved source wording — book line2052</summary>

Final Miracle: Rite of the Crimson Choir: Summon 4 fanatics for 3 turns. Each heals you for 10% of their damage dealt and explodes in death.

</details>

#### Blood Sacrifice

**Level 10 · selection · cleric.hero.cultist.blood-sacrifice**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Lose S+M actual HP from yourself or one willing ally within 5 ft | Self or one willing ally within 5 feet | Empowerment lasts until end of your next regular turn | 1/short rest |

Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.

<details><summary>Preserved source wording — book line2055</summary>

Blood Sacrifice: Sacrifice a portion of your health or an ally's to generate Conviction and empower your next divine ability.

</details>

#### Dark Sacrament

**Level 10 · selection · cleric.hero.cultist.dark-sacrament**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Conviction + 5 RP to start; 1 RP maintenance | 15-foot-radius fixed zone centered within 30 feet | Concentration, maximum 3 Cleric turns | Recharge 4 rounds |

Dark Sacrament. Tags: cultist, sacrament, rite, sustained, zone. On start and each paid maintenance pulse, roll S d6 once. Up to three enemies in the zone make Constitution saves, taking that roll as necrotic damage on failure or half on success. If at least one enemy takes damage, up to three living allies in the zone each regain floor(roll/2)+M HP. Maximum 3 pulses. The Conviction expenditure can vent Dissonance once.

<details><summary>Preserved source wording — book line2056</summary>

Dark Sacrament: Perform a twisted ritual that drains life from enemies to heal allies or create other beneficial effects.

</details>

#### Corrupt Divinity

**Level 12 · selection · cleric.hero.cultist.corrupt-divinity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | One enemy within 60 feet | Maximum 2 rounds | Recharge 3 rounds |

Corrupt Divinity. Tags: cultist, debuff, control. The target makes a Wisdom save. On failure it takes -1 on attack rolls and saving throws. It repeats the save at the end of each turn, ending the effect on success. If a non-player NPC at or below one-quarter maximum HP fails the initial save by 10 or more, it is also Charmed by you until the end of its next turn. This never permanently converts allegiance, changes beliefs or overrides a player character's agency.

<details><summary>Preserved source wording — book line2057</summary>

Corrupt Divinity: Channel corrupted divine energy to weaken enemies and potentially convert them to your cause.

</details>

#### Zealot's Fervor

**Level 14 · selection · cleric.hero.cultist.zealot-s-fervor**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 Conviction | Self | 3 rounds | 1/short rest |

Zealot's Fervor. Tags: cultist, stance. For 3 rounds, once on each of your turns add S to one damage roll from a Cleric feature and S to one HP-healing roll from a Cleric feature. While the Fervor lasts, your AC is reduced by 1. The Conviction expenditure is not a Rite or Invocation and therefore does not vent Dissonance by itself.

<details><summary>Preserved source wording — book line2058</summary>

Zealot's Fervor: Enter a state of religious frenzy, increasing your damage output and healing power at the cost of defense.

</details>

#### Ritual of Undeath

**Level 16 · selection · cleric.hero.cultist.ritual-of-undeath**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Conviction + 6 RP | One eligible corpse within 30 feet or one living ally within 30 feet | Mode-dependent | 1/long rest |

Ritual of Undeath. Tags: cultist, undead, rite. Choose one mode. Corpse Servant: one humanoid corpse dead no more than 1 minute rises for 3 rounds as a temporary thrall with AC 13, 10 HP, Speed 30 feet and one attack only when you spend your shared companion Bonus Action command using your Cleric technique attack bonus; on hit it deals S d6 necrotic. The thrall disappears at 0 HP or when duration ends and grants no XP, loot, new corpse, Conviction or resurrection target. Death Ward: one living ally is marked for 1 minute; the first time it would die during that duration, it instead remains at 1 HP and counts as both humanoid and undead until the end of its next turn. Neither mode removes Wounds. The Conviction expenditure can vent Dissonance once.

<details><summary>Preserved source wording — book line2059</summary>

Ritual of Undeath: Perform a forbidden ritual that can temporarily raise fallen enemies as servants or prevent allies from dying by transforming them into undead-like entities.

</details>

## Source appendix and open balance questions

The complete original Cleric book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/cleric.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does a 3-point base Conviction cap, or 5 with Conviction Pool, create meaningful expenditure choices without making Sacred Chant mandatory in every encounter?
- Do Bishop's Mandate, Miraculous Channel and the six Invocation modes create excessive burst or action compression when combined, especially at levels 7-10?
- Across Saint, Priest and Cultist, are healing, control, resurrection and Conviction regeneration sufficiently bounded across multiple encounters without making ordinary Core V2 spellcasting irrelevant?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
