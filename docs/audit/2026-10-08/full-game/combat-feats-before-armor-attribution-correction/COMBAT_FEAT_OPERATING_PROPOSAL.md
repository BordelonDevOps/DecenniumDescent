# Combat feats: complete operating proposal

**UNADOPTED — all47 original combat feats remain pending whole-feat review.** This manuscript supplies one complete proposed procedure and two authored adjudications for every CF-01–47 question. The original335-feat registries and eight reviewed feats remain unchanged.

[Complete structured proposal and preserved sources](../../data/director/combat_feat_operating_proposal_internal.json) · [Original source audit](../../../../docs/audit/2026-10-08/full-game/COMBAT_FEAT_SOURCE_AUDIT.md) · [Current combat rules](../mechanics/COMBAT_ACTION_PLAYTEST.md) · [Preservation/arithmetic receipt](../../../../docs/audit/2026-10-08/full-game/COMBAT_47_OPERATING_PROPOSAL_CHECK.json)

The94 examples are authored expectations, not runtime test results or human play. Existing rules are cited for their actual scopes; every new interpretation remains a discussion proposal. No feat is activated by this document.

## Shared rules and proposed interfaces

### Authority and acquisition

All procedures below are UNADOPTED proposals for the actual CF-01–47 questions. Original effects, prerequisites, descriptions and legacy fields remain intact. Current reviewed Core/combat/condition/healing/equipment rules control unless a precisely identified NEW feat-specific exception below is accepted. Character-level gates mean total character level; ability gates use actual permanent scores. NEW: these 47 feats are nonrepeatable. A weapon name/type prerequisite requires actual proficiency in that profile; Melee/Ranged without a named weapon requires proficiency in at least one actual melee/ranged weapon respectively. This does not make an unproficient attack proficient. Two-handed prerequisites require proficiency with an actual weapon possessing Two-Handed; a Versatile weapon held in two hands alone does not satisfy that acquisition gate. Actual items, hands, ammunition, preparation and class access remain necessary.

### Cadence and costs

Retain one ordinary Action, one available Bonus Action and one ordinary Reaction resource between regular starts, with current prohibitions. A feat grants no additional action wallet unless expressly proposed. NEW feat cadence: once per turn means one occurrence during each actual regular creature turn; an extra turn shares its associated original regular-turn identity and cannot create another allowance. Outside initiative, use one six-second interval per owner for the same benefit, with no transition refill. Once on your turn is restricted to your own regular turn and its linked extra turns, sharing one allowance. Per-encounter use belongs to a continuous actual hostile scene, including pursuit and brief initiative exits; changing combat mode never resets it. A genuinely concluded scene followed by a new threat permits a new encounter use. SR/LR refresh requires a completed legal rest on the shared campaign clock, never merely a button or encounter end. Uses pay at their stated declaration/application stage. Cannot refund a declared use through immunity, prevention, a miss, or later invalidation unless expressly allowed.

### Targets and source attribution

Use actual actors, source identities and target state. Enemy/hostile means an independent meaningful opponent in a genuine threat; staged prisoners, allies, harmless livestock, owned summons, clones and conjured resource bodies cannot generate drop/healing/kill rewards. NEW apply that anti-farm condition to all combat-generated Life Drinker recovery. Attack/hit triggers are distinct from positive resolved damage and actualDamageDealt. Reflection, transfer, Echo/copy packets and periodic damage cannot masquerade as a new weapon attack. A mount, summoned creature or controlled ally owns its own attack, not its controller's personal feat bonuses. Passive benefits persist while unconscious only where their source does not require conscious control; deliberate choices require ordinary capability. Feats do not diagnose hidden HP, type, immunity, equipment or thoughts. Director resolves actual predicates privately and communicates observable results.

### Damage arithmetic

Retain critical doubling of actual attack damage dice, never flat modifiers; an expanded critical range below 20 must still hit AC. NEW one additional weapon die means one die of the actual chosen base weapon expression, before critical doubling; a 2d6 weapon supplies one d6, a two-handed 1d10 Versatile attack supplies one d10, and a fixed-damage improvised profile supplies no die. Natural attacks qualify as weapon attacks only where their actual profile says so; unarmed attacks are separate unless explicitly included. NEW percent bonuses compute from a common eligible native event after critical dice/ordinary flat bonuses but before percent bonuses, resistance, reduction or temp HP. Percent bonuses do not compound. Each percentage source rounds its own added amount down once; allocate multi-type bonuses by proportional largest remainder, breaking ties by the original stable component order. Weapon-only percentages include that weapon's native dice and ability/modifiers attached to the weapon packet, not a separately priced spell, poison, Smite, periodic or copied rider. Broad own-damage percentages may include those independently eligible components, but never controller-owned companion damage or copied/reflected/transferred events. Do not merge separate hits for rounding. Apply actual defenses once and preserve healing/sharing provenance.

### Defense and movement

Use actual AC formula plus lawful modifiers. Same feat identity/family never stacks across duplicate owners; independent effects retain their original family restrictions. NEW feat debuffs are separate layers, not edits to armor objects. Armor Crusher and Feint each apply once and can coexist if both actually qualify; spell/class AC bonuses retain their own strongest-family rules. Every movement operation specifies ordinary or separate budget. Both pay strongest terrain plus crawl/squeeze costs and require usable Speed unless forced/teleport. No creature may voluntarily finish in occupied space or solid matter. All forced movement stops at obstacles and does not provoke ordinary opportunity attacks. Explicitly source-bound durations use preserved original regular markers, including while incapacitated or after initiative changes. Extra turns do not accelerate expiry or periodic ticks.

### Conditions and secondary attacks

Use actual Core Prone, Stunned, Dazed, Frightened and Bleeding meanings. NEW expand the existing source-character/target/encounter hard-denial ledger to feat Stunned/equivalent whole-turn denial as well as class/spell/companion entries; no new feat-specific ledger evades a spent character limit. Damage and soft riders survive a blocked hard-denial rider. No unprinted body-type immunity is invented; explicit bloodlessness, bleeding immunity, anchoring, Prone immunity, condition immunity and boss defenses apply. NEW feat-generated free/counter attacks carry a causal root and cannot generate another Riposte, Frenzied Rage bonus attack or Eldritch Combat free cast in that root. Ordinary finite damage riders may work if independently legal, but no attack loop or new action wallet arises.

### Open interfaces

These drafts discuss consequential new choices, not final game-wide adoption. Shared flanking geometry is a feat-only proposal, not universal advantage. Dragon/dragonkin predicates require supplied literal creature facts; no ancestry, plane or origin retcon. Existing bestiary candidate is source-authored and remains pending joint review. Berserker Brew and Mooncursed are not silently renamed class Rage. The two deferred magic grant outlines and the post-push cosmology boundary remain unchanged. The 58-question expedition conference remains live; all303 repository payloads stay byte-identical. Full feat runtime, class interactions, numerical balance and human playtest remain open.

## All47 source entries

### CF-01 — Armor Crusher

Source identity: `armor_crusher`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

Once per turn when you deal bludgeoning, piercing, or slashing damage, reduce the target’s AC by 1 until the start of your next turn. This does not stack with itself.

**Proposed complete procedure**

After one of your own direct damage events deals positive resolved bludgeoning, piercing or slashing damage to a creature, you may apply Armor Crusher once that turn. NEW: any actual creature defense qualifies, including natural armor and unarmored defense; the feat does not require a removable suit. The triggering event finishes against its original AC. Apply a separate −1 AC layer through your next original regular start. Further applications from any owner never sum below −1; retain independent expiry records, so the penalty persists while at least one remains. Fully prevented damage does not trigger; temp-HP absorption of a positive resolved packet still does. Copied, reflected, transferred and ongoing periodic damage do not generate applications. Do not damage or regrade armor.

**Explicit NEW choices:** Creature-wide scope, direct-event eligibility, single identity family across owners, and expiry arbitration.

**Worked adjudications**

- An AC17 creature takes 4 piercing damage: the triggering attack used17; later attacks use16 until expiry.

- Two owners apply the feat: AC falls only1. The later record can keep that same −1 after the first expires.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "armor_crusher",
  "name": "Armor Crusher",
  "description": "Repeated, well-placed blows find the seams in an enemy's armor and press the advantage.",
  "prerequisite": "Level 7",
  "effect": "Once per turn when you deal bludgeoning, piercing, or slashing damage, reduce the target’s AC by 1 until the start of your next turn. This does not stack with itself.",
  "type": "Combat",
  "legacyEffect": "Ignore 10% enemy armor",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define damage-packet eligibility, target/armor requirements, zero damage, application after the triggering damage, once-per-turn cadence and nonstacking across multiple owners. Does it alter an AC formula or a separate debuff layer, and what expires at the next regular start?

</details>

### CF-02 — Battlefield Commander

Source identity: `battlefield_commander`. Original prerequisite: **Charisma 15+, Level 12**.

**Original effect, unchanged**

As an action, choose up to three willing allies within 30 feet who can hear you. Each may use its reaction to move up to half its speed without provoking opportunity attacks. You regain this use after a short rest.

**Proposed complete procedure**

Action, once per short rest: choose one to three other willing allied creatures within30ft who can hear and understand the brief directive. Lock recipients and their order, spend the use, then resolve each sequentially. Each may spend its own available Reaction immediately for a separate floor(current relevant Speed/2)-ft movement-cost budget. Recheck hearing, willingness, position and capability at that recipient's resolution. Terrain and hazards apply; movement from this instruction provokes no opportunity attacks. Speed0 gives no movement. Declining or losing eligibility grants no replacement recipient and does not refund the commander; a recipient that does not move need not spend a Reaction. No ordinary movement/Action/BA resource is restored.

**Explicit NEW choices:** Understanding requirement, ordered locked recipients, half-Speed cost budget and skip rules.

**Worked adjudications**

- Speed30 on normal ground allows15ft. On difficult ground the same15-point budget allows only one complete5ft square on a grid.

- The second ally is incapacitated by a hazard while the first moves: skip that ally; the third may still react if legal.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "battlefield_commander",
  "name": "Battlefield Commander",
  "description": "A commanding voice directs three nearby allies into more favorable positions when the line must shift.",
  "prerequisite": "Charisma 15+, Level 12",
  "effect": "As an action, choose up to three willing allies within 30 feet who can hear you. Each may use its reaction to move up to half its speed without provoking opportunity attacks. You regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "Reposition 3 allies within 30ft",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind Action, hearing/willingness, three unique allies, Reaction expenditure, half-current-Speed separate budget, terrain costs, sequential placement, interruption and opportunity immunity. Define short-rest recovery and no movement at Speed0.

</details>

### CF-03 — Berserker Rage

Source identity: `berserker_rage`. Original prerequisite: **Strength 16+, Level 9**.

**Original effect, unchanged**

As a bonus action, enter a rage for 2 rounds. Your weapon attacks deal one additional weapon damage die, but your AC is reduced by 2. You regain this use after a short rest.

**Proposed complete procedure**

Bonus Action, once per short rest: enter this distinct feat rage through your second future original regular-start marker; outside initiative12elapsed seconds. Each qualifying weapon attack hit during it adds one base weapon damage die, doubled as part of a critical. Melee and ranged weapon attacks qualify because the current effect says weapon attacks; unarmed attacks do not, and natural attacks require an actual weapon profile. Apply its −2 AC continuously. Repeated same identity cannot stack; independently active Aggressive stance's −2 AC also applies. NEW the rage ends early if you become Incapacitated. This is a rage for Frenzied Rage's operating trigger, but acquiring this feat alone does not satisfy Frenzied Rage's separately printed Berserker-feat-or-class-rage prerequisite. It supplies no +2 rage damage to replace and no resistance or spell ban.

**Explicit NEW choices:** Exact self-buff clock, all weapon scope, die selection, incapacitation endpoint and explicit distinction between operational rage and acquisition gate.

**Worked adjudications**

- A 2d6 greatsword hit gains1d6; a critical rolls6d6 in total, plus unchanged flat modifiers.

- Activation on own turn4 expires at start6, even if turn5 is skipped; an extra turn does not extend it.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "berserker_rage",
  "name": "Berserker Rage",
  "description": "A powerful fighter accepts a brief loss of defense to drive a ten-second burst of damage.",
  "prerequisite": "Strength 16+, Level 9",
  "effect": "As a bonus action, enter a rage for 2 rounds. Your weapon attacks deal one additional weapon damage die, but your AC is reduced by 2. You regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "+25% damage for 10s, -10% AC",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define activation and exact two-round clock, weapon-die selection for multi-die/versatile/natural attacks, critical doubling and AC penalty arbitration. Establish whether this counts as the separate Berserker feat's rage for Frenzied Rage, without aliasing their sources.

</details>

### CF-04 — Bleeding Edge

Source identity: `bleeding_edge`. Original prerequisite: **Dexterity 14+, Melee**.

**Original effect, unchanged**

When you score a critical hit with a melee weapon, the target bleeds for 1d4 damage at the start of each of its turns for 3 rounds. A creature can use an action to stop the bleeding with a successful Medicine check against DC 10 + your proficiency bonus.

**Proposed complete procedure**

When your actual melee weapon attack critically hits a living non-bloodless creature, after the hit resolves apply feat.bleeding-edge in family.bleeding, stack group feat.bleeding-edge:<owner>. NEW physical type is slashing. It deals1d4 at each of the next three future target regular starts, then ends; applying during a start never adds an immediate tick. Same-owner reapplication refreshes three remaining ticks without adding a second instance; different owners retain competing groups under the existing highest-expected-damage/earliest-application arbitration. Losing due groups still spend ticks. Snapshot the ending Medicine DC10+your PB at application. Victim or adjacent helper may spend an Action with one usable hand and access to the injury, selecting this record before WIS Medicine; success ends that record only. No kit charge is required by this feat. Retain generic positive-potential magical-healing automatic cure for this ordinary Bleeding record. Critical dice do not double later periodic damage; no resource/attack procs from ticks. No positive-damage prerequisite is added beyond actual hit and bleedable body.

**Explicit NEW choices:** Registered family/type/three-start clock, refresh, body gate and ordinary magical-healing endpoint.

**Worked adjudications**

- At PB3, an adjacent Medicine total13 ends one selected owner's record; another owner's independent record remains.

- A concurrent stronger Bleed wins two due starts. Bleeding Edge still uses those two ticks and has only one left.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "bleeding_edge",
  "name": "Bleeding Edge",
  "description": "A precise melee critical opens a wound that carries the feat's listed bleed effect.",
  "prerequisite": "Dexterity 14+, Melee",
  "effect": "When you score a critical hit with a melee weapon, the target bleeds for 1d4 damage at the start of each of its turns for 3 rounds. A creature can use an action to stop the bleeding with a successful Medicine check against DC 10 + your proficiency bonus.",
  "type": "Combat",
  "legacyEffect": "Adds bleed effect on crit",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Assign an explicit periodic identity/family, damage type, three-round/tick clock, repeated applications and multiple owners. Resolve bleedable-body permission, Medicine action/range/hands and whether stopping this rider also affects unrelated Bleeding families.

</details>

### CF-05 — Brace for Impact

Source identity: `brace_for_impact`. Original prerequisite: **Constitution 14+**.

**Original effect, unchanged**

If you have not moved since the start of your turn, use a reaction when you take damage to reduce it by your proficiency bonus + Constitution modifier.

**Proposed complete procedure**

If you have undergone no actual positional displacement since your most recent original regular-turn start, spend Reaction when a direct damage event would damage you. NEW all voluntary, forced, carried and teleport displacement counts, even returning to the same square; standing, turning in place and a failed move do not. Before your first encounter turn, count displacement since encounter entry. Reduce one whole resolved incoming event by max(0,PB+CON modifier), after ordinary passive defenses and before temporary HP. Allocate reduction across components in their stable order, never below0; one attack's fire and slashing are one event, separate attacks are not. Do not re-mitigate a transferred packet that explicitly forbids recipient mitigation. This affects damage only, not attached conditions, sacrificed HP or state assignment. Paying with a zero reduction is allowed but does not create healing.

**Explicit NEW choices:** Displacement receipt, whole-event post-defense timing, nonnegative reduction and stable split allocation.

**Worked adjudications**

- PB3/CON2 reduces resolved8 to3 before tempHP; it does not subtract5 independently from each component.

- You were pushed5ft and then returned5ft after your start. You cannot use the feat before the next regular start.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "brace_for_impact",
  "name": "Brace for Impact",
  "description": "A resilient combatant who holds position braces for the listed damage resistance.",
  "prerequisite": "Constitution 14+",
  "effect": "If you have not moved since the start of your turn, use a reaction when you take damage to reduce it by your proficiency bonus + Constitution modifier.",
  "type": "Combat",
  "legacyEffect": "+20% damage resistance if stationary",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define moved-since-start across forced movement, teleport and extra turns; reaction timing before/after mitigation; PB+CON minimum; one packet versus area or split damage; actual damaged recipient; and interaction with transfer/prevention rules.

</details>

### CF-06 — Break Line

Source identity: `break_line`. Original prerequisite: **Dexterity 15+, Level 10**.

**Original effect, unchanged**

Once per turn, you may move through the space of one hostile creature no more than one size larger than you. That creature may make an opportunity attack; on a miss, you complete the movement.

**Proposed complete procedure**

Once per turn during your own legal voluntary movement, declare crossing one hostile creature's occupied space whose size is no more than one category larger. You must have enough ordinary remaining movement cost and a visible or known legal unoccupied exit to traverse its entire occupied footprint; occupied terrain costs at least difficult. Before first entry, that creature may spend its Reaction for one legal melee opportunity attack against you, even though you are entering rather than leaving. All actual reaction, sight, reach and opportunity-immunity restrictions apply. If it hits, this passage fails: remain in your last legal outside space, spend the first attempted entry step's cost and the feat use. The hit's other consequences resolve normally. If it misses, declines, cannot attack or its opportunity attack is suppressed, proceed, paying actual traversal costs. Recheck the exit after interruptions; if traversal becomes impossible before entry, stay outside and spend the committed use. Do not willingly start a traversal without a complete legal route. Other creatures may make normal opportunity attacks. This does not shove or phase through a creature.

**Explicit NEW choices:** Pre-entry special opportunity trigger, declined/unavailable success, hit stops passage, full-footprint route and committed step cost.

**Worked adjudications**

- A Medium rogue has20 movement cost left and crosses one Medium hostile square for10 then exits for5. The guard has no Reaction, so passage succeeds.

- The guard's legal special attack hits. The rogue remains before the occupied square and spends10 cost for the attempted difficult entry; damage and the once-turn use remain.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "break_line",
  "name": "Break Line",
  "description": "An agile veteran slips through the enemy's frontline zone without treating it as an obstacle.",
  "prerequisite": "Dexterity 15+, Level 10",
  "effect": "Once per turn, you may move through the space of one hostile creature no more than one size larger than you. That creature may make an opportunity attack; on a miss, you complete the movement.",
  "type": "Combat",
  "legacyEffect": "Ignore enemy frontline zone",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define ordinary movement cost, occupied-space entry/exit and size limit; when the special opportunity attack occurs, who can make it, Reaction cost, declined/unavailable attack, hit consequence and legal stopping space. Do not leave passage dependent on an attack that cannot occur.

</details>

### CF-07 — Bull Rush

Source identity: `bull_rush`. Original prerequisite: **Strength 14+**.

**Original effect, unchanged**

When you hit with a melee attack after moving at least 10 feet straight toward the target, force it to make a Strength save (DC 8 + proficiency bonus + Strength modifier) or be pushed 5 feet and knocked prone. Once per turn.

**Proposed complete procedure**

Once per turn, after you hit with a melee attack immediately following at least10ft of your own continuous voluntary movement in a straight line directly toward that target, choose this rider. NEW the approach must occur on that same actual turn, without intervening attack, action, turn or teleport; forced/carried displacement does not count. Melee weapon, natural, unarmed and actual melee spell attacks qualify. Target makes STR save DC8+PB+your current STR modifier. On failure push it5ft directly away and separately apply Prone. NEW no additional size cap is added because the feat omits one; actual immovability, anatomy/support and condition immunities still apply. A wall can stop the push without preventing Prone. A hit dealing0 damage can trigger. Resolve normal damage before this rider; if no creature remains, no further effect. No additional Action cost.

**Explicit NEW choices:** Continuous approach and turn scope, all melee attacks, no imported size ceiling, independent push/Prone.

**Worked adjudications**

- A hit after10ft straight approach produces a failed save. A wall blocks displacement but the target still falls Prone if eligible.

- A teleport of10ft followed by a hit does not meet the approach; neither does being carried forward by another actor.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "bull_rush",
  "name": "Bull Rush",
  "description": "A strong combatant drives into a target, forcing the listed short displacement and knockdown.",
  "prerequisite": "Strength 14+",
  "effect": "When you hit with a melee attack after moving at least 10 feet straight toward the target, force it to make a Strength save (DC 8 + proficiency bonus + Strength modifier) or be pushed 5 feet and knocked prone. Once per turn.",
  "type": "Combat",
  "legacyEffect": "Knock target prone and move them 5ft",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind qualifying melee attack types, straight continuous ten-foot movement, actual hit versus damage, cadence and save timing. Decide push and Prone independently where displacement is blocked, and any size/anchor limits not supplied by the feat.

</details>

### CF-08 — Cleaving Momentum

Source identity: `cleaving_momentum`. Original prerequisite: **Strength 16+, 2H Weapon**.

**Original effect, unchanged**

When you reduce a hostile creature to 0 hit points with a melee weapon, make one melee weapon attack against another creature within reach as a bonus action.

**Proposed complete procedure**

Acquire with STR16 and actual proficiency in a Two-Handed weapon. NEW triggering and follow-up attacks must both use an actual melee weapon wielded with two hands; a legal Versatile two-hand attack can operate the acquired feat. During your own turn, after your attack reduces a genuine hostile creature from positiveHP to0 after floors/replacements, you may spend your still-available Bonus Action before that turn ends for one melee weapon attack against a different creature in legal reach. Death is unnecessary; a surviving downed opponent qualifies. The second target need not be hostile under the printed another-creature wording. Normal damage, ammunition if relevant, hands and perception apply. No banked off-turn use and no additional Bonus Action; multiple drops only provide alternative triggers for that same wallet. Copied/periodic damage and reducing an already0 creature do not qualify.

**Explicit NEW choices:** Two-hand operating restriction, positive-to-zero event and same-own-turn Bonus Action window.

**Worked adjudications**

- A greatsword drops a hostile to0 but the creature survives dying. One available BA can attack a second target.

- The follow-up also drops its target. There is no second Bonus Action and thus no chain of free attacks.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "cleaving_momentum",
  "name": "Cleaving Momentum",
  "description": "A heavy two-handed finishing blow carries its momentum into the listed follow-up attack.",
  "prerequisite": "Strength 16+, 2H Weapon",
  "effect": "When you reduce a hostile creature to 0 hit points with a melee weapon, make one melee weapon attack against another creature within reach as a bonus action.",
  "type": "Combat",
  "legacyEffect": "Free follow-up attack on kill",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind the 2H Weapon prerequisite and whether the triggering/bonus attack must use it. Define hostile drop event, ordinary Bonus Action cost, same-turn window, another target, reach, death versus0HP and prevention of chained extra bonus actions.

</details>

### CF-09 — Close Quarters Combat

Source identity: `close_quarters_combat`. Original prerequisite: **Dexterity 14+**.

**Original effect, unchanged**

Making a ranged attack while a hostile creature is within 5 feet does not impose disadvantage, and the attack does not provoke an opportunity attack.

**Proposed complete procedure**

Your ranged attacks ignore disadvantage caused specifically by a seeing, non-Incapacitated hostile creature within5ft of you. This covers ranged weapon and ranged spell attacks. It does not remove long-range, unseen-target, Prone, restrained or other independent disadvantage. If any other disadvantage remains, apply ordinary cancellation. Making that ranged attack does not itself provoke an opportunity attack from any source that explicitly uses making the ranged attack as its trigger; it does not suppress a separate spellcasting, movement or other legal trigger. Current generic combat creates no opportunity attack just for making a ranged attack; do not add such a penalty for other characters.

**Explicit NEW choices:** All ranged attack scope and narrow attack-trigger immunity without inventing a general penalty.

**Worked adjudications**

- A nearby guard imposes the usual proximity disadvantage on a ray; this feat removes it.

- A long-range bow shot with an adjacent hostile still has long-range disadvantage, even though proximity disadvantage is removed.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "close_quarters_combat",
  "name": "Close Quarters Combat",
  "description": "Quick control of a cramped melee keeps a ranged attack from drawing the listed opportunity attack.",
  "prerequisite": "Dexterity 14+",
  "effect": "Making a ranged attack while a hostile creature is within 5 feet does not impose disadvantage, and the attack does not provoke an opportunity attack.",
  "type": "Combat",
  "legacyEffect": "No AoO when using ranged in melee",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve ranged weapon versus spell attacks and which disadvantage sources are removed. Identify any actual attack-generated opportunity trigger in current combat rules; do not invent a universal ranged-attack opportunity penalty just to remove it.

</details>

### CF-10 — Combat Intuition

Source identity: `combat_intuition`. Original prerequisite: **Wisdom 13+**.

**Original effect, unchanged**

You cannot be surprised while conscious. During the first round of combat, gain +1 AC.

**Proposed complete procedure**

While conscious, you cannot be surprised. NEW this suppresses any still-active surprise action/reaction prohibition while consciousness lasts, without granting lost actions or retroactive turns; other conditions still restrict you. The underlying first-turn surprise schedule is retained if consciousness changes again. Gain+1 AC during the encounter's first numbered round only. A late entrant in that round gains it only for the remainder; entering in round2 does not create a personal first round. The +1 is one feat modifier and needs no action; no extra Reaction is granted when surprise is prevented, only access to the normal resource if otherwise available.

**Explicit NEW choices:** Conscious suppression of existing surprise, encounter-wide round identity and ordinary resource preservation.

**Worked adjudications**

- A conscious owner in round1 is not surprised and has+1AC. An extra turn during round1 still has the same bonus.

- Joining combat in round3 grants no first-round AC, though conscious surprise prevention still applies.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "combat_intuition",
  "name": "Combat Intuition",
  "description": "Alert instincts give a combatant the listed chance to evade an opponent's opening attack.",
  "prerequisite": "Wisdom 13+",
  "effect": "You cannot be surprised while conscious. During the first round of combat, gain +1 AC.",
  "type": "Combat",
  "legacyEffect": "+10% chance to dodge opening attack",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind consciousness, surprise handling, first-round identity for late entrants/extra turns and the+1 AC layer. Resolve changing consciousness and already-existing surprise without granting extra turns or reactions.

</details>

### CF-11 — Combat Slide

Source identity: `combat_slide`. Original prerequisite: **Dexterity 13+**.

**Original effect, unchanged**

Once on your turn, move 5 feet before or after a weapon attack without provoking an opportunity attack from the target of that attack.

**Proposed complete procedure**

Once on your own turn, immediately before or after one weapon attack, move using a separate5ft movement-cost budget. NEW choose and declare the attack target before a pre-attack slide; ordinary attack range and other legality must hold after movement. You still pay the attack's normal Action/BA/Reaction source; the slide grants no attack. For pre-slide, reserve that attack, and if an interruption prevents it the slide and use remain spent. For post-slide, a hit or miss both qualify. Only the declared target cannot make opportunity attacks provoked by this movement; other foes may. Terrain costs, usable Speed, legal endpoints and inability to occupy another creature still apply. At Speed0 you may attack if otherwise legal but cannot slide. No banking or splitting the5ft into separate later moves.

**Explicit NEW choices:** Separate5-point budget, reservation before attack, target-only immunity and interruption commitment.

**Worked adjudications**

- After missing a guard with a spear, move5ft on normal ground without that guard's opportunity attack.

- A difficult5ft grid square costs10. The slide's5-point budget cannot enter it, and the feat does not double its budget.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "combat_slide",
  "name": "Combat Slide",
  "description": "An agile fighter shifts five feet and attacks as part of the same listed action.",
  "prerequisite": "Dexterity 13+",
  "effect": "Once on your turn, move 5 feet before or after a weapon attack without provoking an opportunity attack from the target of that attack.",
  "type": "Combat",
  "legacyEffect": "Move 5ft and attack as one action",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Decide whether5ft is a separate budget or uses ordinary remaining movement; bind before/after one weapon attack, declared target, misses/cancellation, terrain, Speed0 and immunity from only that target. Define own-turn cadence across extra turns.

</details>

### CF-12 — Crippling Strike

Source identity: `crippling_strike`. Original prerequisite: **Dexterity 14+, Melee**.

**Original effect, unchanged**

Once per turn when you hit with a finesse or melee weapon, reduce the target’s speed by 10 feet until the start of your next turn.

**Proposed complete procedure**

Once per turn when your attack hits using a weapon with Finesse OR a weapon classified as melee, reduce the target's current applicable Speed modes by10ft, minimum0, through your next original regular start. NEW a thrown dagger qualifies by both its melee classification and Finesse, even though its attack is ranged; a thrown nonfinesse melee weapon also qualifies by the literal melee-weapon branch. A longbow does not. Do not require positive damage. Same-identity applications across owners do not sum; retain independent expiries for one −10 layer. Other distinct Speed modifiers follow their actual stacking rules; apply numeric changes before halving and retain spent movement cost. This is not the Thief's Slow condition and grants none of that source's other effects.

**Explicit NEW choices:** Literal weapon-class OR property scope, all Speed modes, one family and modifier ordering.

**Worked adjudications**

- A thrown dagger hit lowers walking30 and flying40 to20 and30 until the owner's next regular start.

- Two owners hit with the feat: Speed30 becomes20, not10; separate expiry records preserve the one penalty.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "crippling_strike",
  "name": "Crippling Strike",
  "description": "A Dexterity-trained melee combatant applies the listed movement reduction to an enemy.",
  "prerequisite": "Dexterity 14+, Melee",
  "effect": "Once per turn when you hit with a finesse or melee weapon, reduce the target’s speed by 10 feet until the start of your next turn.",
  "type": "Combat",
  "legacyEffect": "Reduces enemy movement by 50%",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve the printed finesse OR melee-weapon scope, including thrown finesse weapons. Define speed modes/floor, repeated/multiple-owner applications, once-per-turn cadence and expiry; do not silently replace with the Thief class's source-specific Slow.

</details>

### CF-13 — Defensive Stance

Source identity: `defensive_stance`. Original prerequisite: **Level 6**.

**Original effect, unchanged**

+15% AC, can't move this turn

**Proposed complete procedure**

NEW complete activation: when choosing your stance at the start of a regular own turn before using any stance benefit or moving voluntarily, choose Defensive Stance instead of a normal stance. No Action; one stance choice. Through your next original regular start, add floor(15% of your otherwise-current AC), minimum0, to AC. Compute the base after actual armor/shield/DEX/flat bonuses/penalties but before this or any other percentage-AC bonus; no percent-on-percent multiplication. Recompute when that underlying base changes, including conditional Guard. You cannot voluntarily change position by Speed expenditure, teleport or a feature while the current regular turn lasts; linked extra turns also retain the movement restriction. Standing/dropping Prone is allowed if ordinary budget/capability permits. Forced displacement remains possible and does not end the stance. Off-turn voluntary Reaction movement after that turn is allowed; AC lasts to expiry. It cannot coexist with Aggressive, Guarded, Mobile, Focused or Carrying because it occupies their stance choice, not a free extra buff.

**Explicit NEW choices:** Entire activation/stance slot/duration and percentage base; voluntary-only this-turn movement restriction, including teleport; retained15% numeric value.

**Worked adjudications**

- Underlying AC17 gains floor2.55=2, total19. The feat does not round to a3-point bonus.

- A forced push during the stance moves the owner normally. They cannot then voluntarily teleport during their turn, but the push does not remove AC.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "defensive_stance",
  "name": "Defensive Stance",
  "description": "You can adopt a defensive posture that greatly improves your protection.",
  "prerequisite": "Level 6",
  "effect": "+15% AC, can't move this turn",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Supply activation, duration, frequency and legal timing for the retained+15% AC and cannot-move-this-turn clause. Define percentage base, rounding and AC-family interaction, plus forced movement/teleport and stance competition. Any numeric conversion must be explicitly NEW.

</details>

### CF-14 — Disarming Blow

Source identity: `disarming_blow`. Original prerequisite: **Strength 14+, Melee**.

**Original effect, unchanged**

When you hit a creature holding an object, forgo one damage die to force a Strength or Dexterity save (target’s choice) against DC 8 + proficiency bonus + your attack ability modifier. On a failure, it drops one held object.

**Proposed complete procedure**

On a hit with a melee weapon attack, before rolling damage, select one held reachable object and forgo one actual base-weapon damage die to attempt disarming it. NEW remove one die before critical doubling; a critical1d8 weapon forgoes its entire doubled base2d8, retaining lawful flat damage and independent riders. Never pay with a rider die, a die already spent on another feat, or a fixed-damage expression. The target chooses STR or DEX save against DC8+PB+the actual attack ability modifier. Resolve remaining hit damage, then the save if the creature still holds the object. Failure drops it into an adjacent legal unoccupied space you choose, otherwise its own space. No extra damage to object, severed curse or bond; actual non-droppable bonds prevent dropping. An object wielded with two hands is still one object. No new once-turn cap: each separately paid qualifying hit can attempt, but the chosen die is spent even if immunity prevents the result.

**Explicit NEW choices:** Melee-weapon scope; pre-critical base-die payment and save order; actual held-object drop geometry.

**Worked adjudications**

- A1d8 sword critical spends its one base die, leaving zero sword dice rather than one; STR modifier and a separately paid legal rider remain.

- A target's bonded blade cannot drop. The attacker's declared damage die is still forgone; the bond is not broken.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "disarming_blow",
  "name": "Disarming Blow",
  "description": "A Strength-trained melee combatant gains the listed chance to knock away a weapon.",
  "prerequisite": "Strength 14+, Melee",
  "effect": "When you hit a creature holding an object, forgo one damage die to force a Strength or Dexterity save (target’s choice) against DC 8 + proficiency bonus + your attack ability modifier. On a failure, it drops one held object.",
  "type": "Combat",
  "legacyEffect": "Chance to knock weapon out",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Specify legal attack types, declaration/payment of one actual damage die, critical/multi-die/rider eligibility and inability to pay. Bind save/DC ability, held reachable object, selection/drop placement, non-droppable bonds and damage resolution order.

</details>

### CF-15 — Double Tap

Source identity: `double_tap`. Original prerequisite: **Dexterity 14+, Ranged**.

**Original effect, unchanged**

When you take the Attack action with a ranged weapon, make one additional attack as a bonus action. This attack does not add your ability modifier to damage unless another feature allows it.

**Proposed complete procedure**

After you take the Attack Action on your turn and make at least one attack with a weapon classified as ranged, spend your available Bonus Action that turn for one additional attack with a legal ranged weapon. NEW it may be a different ranged weapon and a different target; thrown melee weapons do not meet ranged-weapon classification. Supply actual ammunition, loaded state, reload/loading cadence and usable hands. Omit a positive ability damage modifier but retain a negative one, matching current two-weapon arithmetic; only a feature expressly restoring this attack's modifier can restore it. A two-weapon-only exception is insufficient. No attack is granted off-turn by a readied Attack; a linked extra turn may supply the trigger only if it has a legal Attack Action and Bonus Action, without refreshing any consumed shared allowances. This never grants an extra BA.

**Explicit NEW choices:** Ranged-weapon classification, positive-only omission, explicit restoring feature, same-turn use.

**Worked adjudications**

- A bow attack followed by a legal BA bow attack consumes two arrows; with DEX+3 the second damage omits+3.

- DEX−1 still reduces the second attack's damage. Loading that permits only one shot in the relevant period is not bypassed.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "double_tap",
  "name": "Double Tap",
  "description": "Practiced ranged technique fires two shots in quick succession.",
  "prerequisite": "Dexterity 14+, Ranged",
  "effect": "When you take the Attack action with a ranged weapon, make one additional attack as a bonus action. This attack does not add your ability modifier to damage unless another feature allows it.",
  "type": "Combat",
  "legacyEffect": "Fire two shots in quick succession",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind Attack-action qualification, one Bonus Action attack, weapon/ammunition/loading/hands and target choice. Resolve negative ability modifiers, an explicit modifier-restoring feature, off-turn/extra-turn timing and coexistence with other bonus-attack feats.

</details>

### CF-16 — Draw Cut

Source identity: `draw_cut`. Original prerequisite: **Dexterity 15+**.

**Original effect, unchanged**

Once per encounter, when you draw a sheathed melee weapon as part of an attack, add one weapon damage die on a hit.

**Proposed complete procedure**

Once per encounter, when you legally draw a genuinely sheathed melee weapon as part of making a weapon attack with it, declare Draw Cut before the attack roll. NEW drawing uses the normal free object interaction or another explicitly granted draw permission; this feat grants no extra hand or interaction. The weapon must actually be secured in a sheath/scabbard, not merely dropped, held or conjured. A hit adds one actual base weapon die before critical doubling. A miss spends the declaration and encounter use. Resheathing, switching weapons, initiative exits and new turns do not refresh it. The attack may be a thrown attack with that melee weapon if drawing and throwing are otherwise legal. No attack Action or BA is supplied by the feat.

**Explicit NEW choices:** Declaration spends on miss, actual sheath and ordinary interaction cost, explicit encounter boundary.

**Worked adjudications**

- Drawing a1d6 shortsword into a critical adds one base d6 and doubles both base dice for4d6.

- After a missed Draw Cut, sheathing and drawing a second weapon during the same fight cannot restore the use.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "draw_cut",
  "name": "Draw Cut",
  "description": "Quick blade work increases damage when a weapon is unsheathed.",
  "prerequisite": "Dexterity 15+",
  "effect": "Once per encounter, when you draw a sheathed melee weapon as part of an attack, add one weapon damage die on a hit.",
  "type": "Combat",
  "legacyEffect": "+25% damage when unsheathing blade",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define the once-per-encounter boundary, lawful drawing interaction within an attack, sheathed weapon eligibility and hit/miss spending. Select one base weapon die and critical interaction without multiplying riders or laundering repeated sheath/draw events.

</details>

### CF-17 — Exploit Weakness

Source identity: `exploit_weakness`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.

**Proposed complete procedure**

At attack-roll resolution, before that attack's damage, check whether the actual target's normalHP is strictly below half its current effective maximum:2×HP<maximum. TemporaryHP does not count as normalHP and does not change the comparison. If true, your weapon attack critically hits on a kept natural19 or20; a19 must still meet AC. Choose the broadest actually applicable critical range among this and other features; never add their range expansions. The Director can resolve this hidden predicate without disclosing numericHP or granting a diagnostic scan. A target that falls below half only from the current attack does not retroactively make that hit critical. A legal critical-if-hit feature can still apply independently; critical dice double once.

**Explicit NEW choices:** Pre-damage actual-state snapshot and private adjudication; retained reviewed nonstacking critical-range rule.

**Worked adjudications**

- HP10/max21 qualifies; HP11/max21 does not. Ten temporaryHP does not change either result.

- A natural19 totals18 against AC20: it still misses, even when the target is below half.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "exploit_weakness",
  "name": "Exploit Weakness",
  "description": "At level 7, a combatant seeks wounded enemies for the listed critical chance.",
  "prerequisite": "Level 7",
  "effect": "Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.",
  "type": "Combat",
  "legacyEffect": "+15% crit on wounded enemies",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define when actual target HP below half maximum is checked, temporary HP/temporary maxima and unknown information handling. Resolve nineteen-to-twenty critical range against other range modifiers and automatic-critical effects without unsupported stacking.

</details>

### CF-18 — Feint

Source identity: `feint`. Original prerequisite: **Dexterity 14+, Charisma 13+**.

**Original effect, unchanged**

Enemy loses AC vs next attack

**Proposed complete procedure**

NEW complete procedure: Bonus Action, one perceived hostile creature within30ft that can perceive your deliberate threatening movement; oppose your CHA Deception with its WIS Insight. Higher total wins; ties preserve state, with no task-degree/natural shift. On success, apply−2AC against your next attack on that creature before your next original regular start. Declare the affected attack before rolling; it consumes the feint hit or miss. Failure has no effect. Only one unspent Feint per owner; a new successful Feint replaces your prior mark. Multiple owners can each set their own next-attack records, but one attack never receives more than one−2 Feint layer. Feint does not compel beliefs, create a universal off-guard condition or lower AC against other attackers. No rest use cap; the real BA and opposed check fund each attempt. If a target cannot perceive the act, it is ineligible rather than automatically beaten.

**Explicit NEW choices:** Entire BA/range/contest/−2/owner-only next-attack/deadline/frequency completion.

**Worked adjudications**

- Deception17 defeats Insight14. The owner's next attack checks AC16 instead of18 and consumes the mark even on a miss.

- An ally attacks first: that attack gains no Feint bonus and does not consume the owner's mark.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "feint",
  "name": "Feint",
  "description": "You can mislead opponents with deceptive movements.",
  "prerequisite": "Dexterity 14+, Charisma 13+",
  "effect": "Enemy loses AC vs next attack",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Complete the absent Action/Bonus Action, target/range, check/save, AC amount/layer, next-attack beneficiary, deadline, use frequency and replacement behavior. Preserve the original short clause separately; do not adopt an external game's Feint by name.

</details>

### CF-19 — Grappler

Source identity: `grappler`. Original prerequisite: **Strength 14+**.

**Original effect, unchanged**

+4 to grapple rolls; enemies -4 to escape

**Proposed complete procedure**

Add+4 to your actual STR Athletics checks initiating or maintaining an ordinary grapple you control. A creature using the ordinary opposed Escape Action to escape your grapple takes−4 on its chosen Athletics/Acrobatics roll. Your opposed maintaining roll also gets+4; these are different sides of the expressly printed contest. NEW this gives no+4 to your own escape from someone else's hold, no penalty to a defender's initial resistance, and no effect on spell saves or teleports that legally escape without that opposed contest. Reach, one-size-larger cap, actual grasping hand, attack replacement and Escape Action remain unchanged. Multiple grapplers have separate holds and contests; do not multiply−4 from another grapple that is not the selected escape. PB/expertise is included normally once; opposed ties preserve the hold and have no critical task effects.

**Explicit NEW choices:** Initiating/maintaining scope versus escape, initial defense exclusion and per-hold contest.

**Worked adjudications**

- Initiation Athletics12 becomes16; defender Acrobatics15 remains15, so the hold is established.

- For escape, defender total18 becomes14 while the owner's maintenance13 becomes17. An unrelated second grappler adds no further−4.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "grappler",
  "name": "Grappler",
  "description": "You have developed the skills necessary to hold your own in close-quarters grappling.",
  "prerequisite": "Strength 14+",
  "effect": "+4 to grapple rolls; enemies -4 to escape",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Bind+4 to actual initiating/maintaining/escape contests and whose roll receives the-4. Resolve multiple grapplers, size/reach/hands limits, four-degree checks, magical escape and stacking with proficiency/expertise without granting new grapple actions.

</details>

### CF-20 — Lunge

Source identity: `lunge`. Original prerequisite: **Strength 13+, Weapon Proficiency**.

**Original effect, unchanged**

Once on your turn, increase your reach by 5 feet for one melee weapon attack.

**Proposed complete procedure**

Once on your own turn before selecting the target of one melee weapon attack, increase that attack's reach by5ft. Use its actual weapon reach and body profile, then restore ordinary reach immediately after the attack resolves or is interrupted. The declaration consumes the allowance even on a miss. It grants no attack, extra movement, general threatened space, grapple reach or persistent opportunity reach. A later off-turn opportunity attack uses ordinary reach unless its own source specifically grants an exception. A natural weapon only qualifies if actually a weapon attack. You must possess an actual weapon proficiency to acquire the feat, but use with another unproficient legal weapon does not grant PB.

**Explicit NEW choices:** Attack-scoped pre-target declaration, spent-on-miss and no persistent reach.

**Worked adjudications**

- A5ft sword can attack one target10ft away; afterward it still threatens only5ft.

- A10ft reach weapon can make one15ft attack. The target moving from15 to20ft afterward does not trigger that weapon's normal opportunity reach.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "lunge",
  "name": "Lunge",
  "description": "Strength and weapon training extend the reach of the feat's listed melee attacks.",
  "prerequisite": "Strength 13+, Weapon Proficiency",
  "effect": "Once on your turn, increase your reach by 5 feet for one melee weapon attack.",
  "type": "Combat",
  "legacyEffect": "Melee attacks gain +5ft range",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind one selected melee weapon attack, declaration before targeting, own-turn cadence, current weapon reach and reversion. Explicitly distinguish attack reach from persistent control/opportunity reach and grapple reach.

</details>

### CF-21 — Overrun

Source identity: `overrun`. Original prerequisite: **Strength 15+**.

**Original effect, unchanged**

When you Dash, you may move through spaces occupied by creatures no more than one size larger. Each may make a Strength save against DC 8 + proficiency bonus + Strength modifier or be pushed 5 feet aside.

**Proposed complete procedure**

When you legally take Dash, activate Overrun for that turn's subsequent ordinary movement; Dash supplies its normal increased cap, not a second separate movement grant. You may attempt passage through actual creatures at most one size larger, allied or hostile. NEW each distinct creature may be challenged once that turn, with no duplicate attempt from extra Dashes. Before entering its first occupied space, it makes STR save DC8+PB+your STR; a willing ally may elect failure as this feat's explicit exception. On failure push it5ft to a legal adjacent side destination you choose that clears the necessary passage. Success, anchoring, or no legal clearing destination blocks this special passage; remain outside and spend the attempted first entry step's ordinary cost. Do not start without enough budget for a complete legal path/end. The feat does not suppress opportunity attacks. A creature already passable under ordinary size rules can instead be crossed normally without invoking the feature. It grants no Prone, damage or ability to remain in occupied space.

**Explicit NEW choices:** Once-per-creature challenge, ally voluntary failure exception, side-destination requirement and blocked-passage consequence.

**Worked adjudications**

- A Medium runner Dashes and a Large guard fails; a legal5ft side space clears the route, so the runner proceeds using ordinary cost.

- A guard fills a narrow passage with no side destination. Failure alone cannot teleport it through the wall; Overrun passage stays blocked.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "overrun",
  "name": "Overrun",
  "description": "With Strength 15+, you press through movement by pushing enemies aside as the feat lists.",
  "prerequisite": "Strength 15+",
  "effect": "When you Dash, you may move through spaces occupied by creatures no more than one size larger. Each may make a Strength save against DC 8 + proficiency bonus + Strength modifier or be pushed 5 feet aside.",
  "type": "Combat",
  "legacyEffect": "Push enemies aside while moving",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Complete Dash-linked movement budget, per-creature encounter limits, ally/enemy scope, save/DC and success/failure passage. Resolve no legal five-foot side destination, blocked endpoints, opportunity attacks and size/anatomy restrictions.

</details>

### CF-22 — Power Attack

Source identity: `power_attack`. Original prerequisite: **Strength 14+**.

**Original effect, unchanged**

Trade -2 accuracy for +20% damage

**Proposed complete procedure**

NEW complete procedure: before each melee weapon attack roll using STR for that roll, you may take−2 to that roll. If it hits, add floor20% of that attack's eligible native weapon damage as defined in shared arithmetic. This is an optional per-attack trade, no Action or rest charge. Actual weapon proficiency is not granted; finesse choosingDEX, ranged attacks and melee spell/unarmed attacks do not qualify. Preserve critical dice before calculating the percent bonus; no benefit on a miss. Power Attack and Precision Strike's attack trade are mutually exclusive choices on the same attack, not cumulative penalties for stacking both percent bonuses. Giant Slayer or another genuinely independent eligible percent source adds its separately rounded bonus from the same base, without multiplication. Original−2/+20% stays preserved.

**Explicit NEW choices:** STR melee-weapon scope and per-attack timing; mutually exclusive precision/power trade; noncompounding percent contract.

**Worked adjudications**

- Eligible native weapon damage19 yields+3, total22 before defenses. The attack roll still suffers−2.

- Against a Large creature, native20 with both Power Attack20% and Giant Slayer20% totals28, not28.8 or29.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "power_attack",
  "name": "Power Attack",
  "description": "You can sacrifice accuracy for devastating damage.",
  "prerequisite": "Strength 14+",
  "effect": "Trade -2 accuracy for +20% damage",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Complete declaration, eligible attacks, frequency, exact-2 attack penalty and+20% damage base/rounding/order. Resolve multi-type packets, criticals, resistance and combination with Precision Strike/Giant Slayer without silently substituting a flat damage bonus.

</details>

### CF-23 — Precise Shot

Source identity: `precise_shot`. Original prerequisite: **Dexterity 14+**.

**Original effect, unchanged**

Your ranged attacks ignore the disadvantage normally imposed by an ally being adjacent to the target.

**Proposed complete procedure**

The current combat guide imposes no general disadvantage just because an ally is adjacent to the target; retain that printed historical removal as a compatibility clause if a specifically enabled source ever supplies it. NEW useful completion for this candidate: your ranged weapon or ranged spell attack ignores half cover when that half cover is supplied solely by one or more allied creature bodies in the shot's actual path. It ignores neither terrain cover, three-quarters/total cover, hostile-body cover, nearby-hostile disadvantage, nor long-range disadvantage. Compute remaining actual cover normally after disregarding those allied bodies; never lower a real wall's cover. This does not make firing through solid or untargetable positions legal and does not acquire a class Sharpshooter feature.

**Explicit NEW choices:** Explicit allied-body half-cover overlay because the named original disadvantage is absent; no new global penalty.

**Worked adjudications**

- An allied frontliner is the only cause of half cover: the shot ignores that+2AC.

- The target stands behind a low stone wall and beside an ally. The wall's half cover remains.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "precise_shot",
  "name": "Precise Shot",
  "description": "Dexterity 14+ supports a ranged attack into melee without the feat's listed penalty.",
  "prerequisite": "Dexterity 14+",
  "effect": "Your ranged attacks ignore the disadvantage normally imposed by an ally being adjacent to the target.",
  "type": "Combat",
  "legacyEffect": "No penalty for ranged into melee",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

The supplied current combat guide imposes nearby-hostile disadvantage, not a general ally-adjacent-to-target disadvantage. Locate source authority for the assumed penalty or choose an explicit finite new overlay; do not invent that penalty globally or silently turn this into Sharpshooter.

</details>

### CF-24 — Precision Throw

Source identity: `precision_throw`. Original prerequisite: **Dexterity 13+**.

**Original effect, unchanged**

Gain +1 to attack rolls with thrown weapons and double their normal range.

**Proposed complete procedure**

When you make a ranged attack by actually throwing a weapon whose current profile has Thrown, gain+1 attack and double its printed normal range, capped at its actual printed long range. Preserve long range unchanged. NEW no-long-range profiles retain their hard maximum; the feat cannot invent a missing legal interval. Melee use of the same weapon gains nothing. Improvised objects require an actual Thrown weapon profile supplied by another rule; merely hurling an object does not acquire the property. Distinct eligible Weapon Focus+1 may add under its separate feat family; duplicate Precision Throw never stacks. Physical quantities, recovery, hands and ammunition remain actual.

**Explicit NEW choices:** Property/use distinction, normal-range cap and separate feat attack-bonus families.

**Worked adjudications**

- A20/60 dagger becomes40/60 for throwing and gains+1attack; a melee stab does not.

- A hypothetical40/60 Thrown profile becomes60/60, with no attacks beyond60.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "precision_throw",
  "name": "Precision Throw",
  "description": "Dexterity 13+ supports thrown weapons gaining the listed +10% accuracy.",
  "prerequisite": "Dexterity 13+",
  "effect": "Gain +1 to attack rolls with thrown weapons and double their normal range.",
  "type": "Combat",
  "legacyEffect": "Thrown weapons gain +10% accuracy",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define thrown-property melee/ranged weapon use, actual attack qualifier, normal versus long range caps and legal cases where doubled normal exceeds long. Resolve+1 bonus-family stacking and improvised thrown objects.

</details>

### CF-25 — Punishing Blow

Source identity: `punishing_blow`. Original prerequisite: **Strength 13+**.

**Original effect, unchanged**

Once per turn, deal additional damage equal to your proficiency bonus to a stunned or prone enemy.

**Proposed complete procedure**

Once per turn, on one of your own direct attacks that hits a genuine enemy already Stunned or Prone immediately before damage, add your current PB as a flat damage component of that hit's native type. Choose one native type if the attack has several; if it deals no native damage, no additional damage is created. NEW all actual attack types qualify, including spell, natural and unarmed, because source says deal additional damage without weapon restriction. No application from a save-only effect, periodic tick, transfer, copy or rider that does not itself attack. The same hit cannot first inflict Prone/Stunned and retroactively qualify. The bonus is part of the hit before defenses, cannot double on a critical, and applies once across multi-type components.

**Explicit NEW choices:** Direct-attack completion, pre-damage existing condition, flat single component and broad actual attack scope.

**Worked adjudications**

- PB4 adds4 to a critical against a creature already Prone; it does not become8.

- Bull Rush knocks the standing target Prone after damage. That same attack does not receive Punishing Blow retroactively.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "punishing_blow",
  "name": "Punishing Blow",
  "description": "Strength 13+ supports the listed +10% bonus against a stunned enemy.",
  "prerequisite": "Strength 13+",
  "effect": "Once per turn, deal additional damage equal to your proficiency bonus to a stunned or prone enemy.",
  "type": "Combat",
  "legacyEffect": "+10% bonus if enemy is stunned",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define eligible damage events/attacks, hostile versus any target, actual Stunned/Prone timing, once-per-turn cadence and damage type. Avoid copying the PB rider through each damage component or transfer operation.

</details>

### CF-26 — Reckless Swing

Source identity: `reckless_swing`. Original prerequisite: **Strength 15+**.

**Original effect, unchanged**

Before making a melee weapon attack, choose to attack recklessly. Gain advantage on the attack and add one weapon damage die on a hit; attacks against you have advantage until the start of your next turn.

**Proposed complete procedure**

Before any melee weapon attack roll, you may declare Reckless Swing. That one attack gains advantage and adds one base weapon damage die if it hits; critical doubles that additional attack die. Regardless of hit, miss or advantage cancellation, all attacks against you have advantage through your next original regular start. Repeated declarations on separately legal attacks can each supply their one die but do not stack attacker advantage or create attacks; overlapping vulnerability records retain the same next-start deadline. This is not a rage and has no resistance or ability-score substitution. Spell, thrown ranged and unarmed attacks do not qualify; actual natural weapon melee attacks do. Ordinary costs, conditions and damage-source restrictions remain.

**Explicit NEW choices:** Per-attack availability, vulnerability even on miss/cancellation, exact next-start persistence.

**Worked adjudications**

- A longsword1d8 attack gains1d8; if critical, roll4d8 plus flat modifiers.

- You attack an unseen target: advantage and disadvantage cancel, but the extra die on a hit and attacks-against advantage still apply.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "reckless_swing",
  "name": "Reckless Swing",
  "description": "Strength 15+ supports the listed +50% damage with -10% defense.",
  "prerequisite": "Strength 15+",
  "effect": "Before making a melee weapon attack, choose to attack recklessly. Gain advantage on the attack and add one weapon damage die on a hit; attacks against you have advantage until the start of your next turn.",
  "type": "Combat",
  "legacyEffect": "+50% damage, but -10% to defense",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind declaration and eligible melee weapon, advantage cancellation, selection of one weapon die and critical doubling. Resolve repeated use, missed attacks, extra turns, expiry and all attacks against the user without replacing source with a class Rage rule.

</details>

### CF-27 — Riposte

Source identity: `riposte`. Original prerequisite: **Agility 15+, Melee Proficiency**.

**Original effect, unchanged**

Free attack after dodge/parry

**Proposed complete procedure**

NEW acquisition bridge: the legacy Agility15 means DEX15 for this feat only; Melee Proficiency means actual proficiency with at least one melee weapon. After a hostile melee attack against you misses while your active Dodge actually applies to it, OR after an actual sourced Parry/Deflect effect expressly turns that attack into a miss, you may spend your available Reaction to make one legal melee weapon attack against that same attacker in reach. No movement or extra Reaction is granted. A parry that merely reduces damage is insufficient; missing for ordinary AC without qualifying Dodge/Parry is insufficient. If the defensive effect already used your only Reaction, you cannot also riposte. A permitted additional Reaction must explicitly allow an attack; defensive-only grants cannot pay. Apply shared causal-root prohibition on counterattack chains. Once per original regular-start interval even if another source grants extra attack-capable Reactions.

**Explicit NEW choices:** Explicit Agility→DEX bridge, qualifying miss, Reaction instead of unspecified free action, interval and causal cap.

**Worked adjudications**

- While Dodging with Speed30, a seen adjacent enemy misses; spend the available Reaction for one weapon attack.

- A paid parry used the only Reaction to cause a miss. No Reaction remains for Riposte; reducing a hit to0damage would not qualify anyway.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "riposte",
  "name": "Riposte",
  "description": "You can quickly counterattack after successfully defending.",
  "prerequisite": "Agility 15+, Melee Proficiency",
  "effect": "Free attack after dodge/parry",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Resolve Agility15+ against the actual ability taxonomy and Melee Proficiency against existing credentials. Define dodge/parry success, trigger timing, legal target/reach, Action/Reaction cost, frequency and recursive counterattack prevention. 'Free attack' is not a completed action rule.

</details>

### CF-28 — Savage Momentum

Source identity: `savage_momentum`. Original prerequisite: **Strength 14+, Melee**.

**Original effect, unchanged**

Once per turn, after hitting the same creature with consecutive melee attacks, add +1 damage for each prior consecutive hit, to a maximum equal to your proficiency bonus. The chain ends when you miss or change targets.

**Proposed complete procedure**

Track a consecutive direct melee-attack hit chain for each owner during one encounter. Every actual melee attack you make advances the event sequence: a hit on the same current target increases the count; a miss or attack directed at a different target ends the old chain, and a hit on the new target starts a new count1. NEW any intervening nonmelee attack also breaks the chain; movement, spellcasting without attacks and nonattack actions do not. Own/off-turn melee attacks participate, but copies/periodic events do not. Once per turn, before rolling a qualifying hit's damage, add min(PB, prior consecutive hits on that target) as a flat native-type bonus. Only declare when at least one prior hit exists; spending on this hit prevents spending on a later hit that turn. The chain persists across regular turn boundaries but ends on target death/removal, encounter conclusion, or loss of that actual creature identity. Transformation of the same surviving identity retains it if target continuity is real.

**Explicit NEW choices:** Persistent encounter chain, ranged-attack break, state versus bonus budget and zero-prior-hit rule.

**Worked adjudications**

- Three consecutive hits on one foe at PB3 permit choosing+1 on hit2 or+2 on hit3 that turn, not both.

- After two hits, a missed opportunity attack breaks the chain. The next melee hit starts at1 and has no prior-hit bonus.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "savage_momentum",
  "name": "Savage Momentum",
  "description": "Strength 14+ and melee training support the listed +5% damage per consecutive hit.",
  "prerequisite": "Strength 14+, Melee",
  "effect": "Once per turn, after hitting the same creature with consecutive melee attacks, add +1 damage for each prior consecutive hit, to a maximum equal to your proficiency bonus. The chain ends when you miss or change targets.",
  "type": "Combat",
  "legacyEffect": "+5% dmg per consecutive hit",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define consecutive hit chain scope, turns/encounters/off-turn attacks, target changes, misses and nonattack interruptions. Resolve when the once-per-turn bonus is chosen and prior hits counted, PB cap and chain state through target death/transformation.

</details>

### CF-29 — Shattering Smash

Source identity: `shattering_smash`. Original prerequisite: **Strength 16+**.

**Original effect, unchanged**

When you hit a creature using a shield or maintaining a physical block, forgo one damage die to force a Strength save. On a failure, its shield bonus or block benefit is suppressed until the start of its next turn.

**Proposed complete procedure**

On a melee weapon attack hit against a creature receiving an actual wielded shield AC contribution or a sourced current physical-block benefit, before rolling damage forgo one base weapon die under the same pre-critical payment contract as Disarming Blow. NEW save is STR DC8+PB+the actual attack ability modifier. Resolve remaining damage, then on failed save suppress either the chosen shield's entire AC contribution (including its own enhancement) or one selected block benefit through the target's next original regular start. No destruction, durability loss, forced drop or suppression of unrelated item traits; independent magical barriers/unarmored formulas remain. A shield-dependent feat AC bonus is suppressed while its shield cannot supply defensive contribution. Physical block means a named sourced defense actually interposing a held body/object; ordinary armor, cover terrain and taking Dodge do not alone qualify. Same-identity suppression does not multiply, and separate expiries remain. You cannot spend the same die on another rider.

**Explicit NEW choices:** Melee scope, missing save DC, pre-critical payment and entire chosen shield AC contribution with dependency suppression.

**Worked adjudications**

- A shield contributes2 plus1enhancement. Failure suppresses those3 until the target's next regular start; the shield is not broken.

- A one-die sword cannot pay both Shattering Smash and Disarming Blow from the same die. A two-die weapon may pay distinct dice if both targets/effects qualify.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "shattering_smash",
  "name": "Shattering Smash",
  "description": "Strength 16+ supports the listed ability to break an enemy shield or block.",
  "prerequisite": "Strength 16+",
  "effect": "When you hit a creature using a shield or maintaining a physical block, forgo one damage die to force a Strength save. On a failure, its shield bonus or block benefit is suppressed until the start of its next turn.",
  "type": "Combat",
  "legacyEffect": "Break enemy shield or block",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Complete missing save DC and attack scope. Define actual physical block, one damage-die cost, declaration, save timing and suppression of ordinary shield AC versus magical enhancement/other block benefits. Do not damage/destroy equipment by implication.

</details>

### CF-30 — Shield Bash

Source identity: `shield_bash`. Original prerequisite: **Strength 13+**.

**Original effect, unchanged**

After taking the Attack action while wielding a shield, make a shield bash as a bonus action. On a hit, deal 1d4 + Strength bludgeoning damage; once per short rest, force a Constitution save or stun the target until the start of its next turn.

**Proposed complete procedure**

After you take the Attack Action on your own turn while actually wielding a usable shield, you may spend BA that turn to bash a creature within5ft. NEW this is a melee weapon attack using STR, adding PB if you are proficient with shields; the shield remains an armor/shield object, not a new purchasable weapon identity. It deals1d4+STR bludgeoning, minimum0, with ordinary critical doubling. A buckler counts only if its actual profile allows a striking shield body; this feat does not conjure a free weapon or bypass the shield hand. Once per short rest, after a bash hits and before damage, spend the stun use; target CON save DC8+PB+STR after damage. Failure applies Stunned until the target's next original regular start. Immunity and the source-character hard-denial cap apply; spent use is not refunded. This endpoint deliberately does not steal the target's whole next regular turn. No grant of another BA or off-turn bash.

**Explicit NEW choices:** Actual shield proficiency attack bridge,5ft/STR/DC, hit-stage stun payment and shared hard-denial cap.

**Worked adjudications**

- STR+3/PB3 bash attacks at+6 for1d4+3; the optional stun save isDC14.

- A stun applied just after the enemy's turn can block intervening Reactions, but expires at that enemy's next start before voluntary decisions.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "shield_bash",
  "name": "Shield Bash",
  "description": "Strength 13+ supports the listed shield stun against an enemy.",
  "prerequisite": "Strength 13+",
  "effect": "After taking the Attack action while wielding a shield, make a shield bash as a bonus action. On a hit, deal 1d4 + Strength bludgeoning damage; once per short rest, force a Constitution save or stun the target until the start of its next turn.",
  "type": "Combat",
  "legacyEffect": "Stun enemy with shield",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Supply attack ability/proficiency/weapon classification, range, shield-hand use and missing stun DC. Bind Attack-action prerequisite, Bonus Action, one-short-rest use declaration/payment and Stunned expiry; distinguish the shield from a new priced weapon.

</details>

### CF-31 — Shield Expert

Source identity: `shield_expert`. Original prerequisite: **Shield Proficiency**.

**Original effect, unchanged**

Gain +1 AC while wielding a shield. When a Dexterity save would deal half damage, use your reaction to take no damage on a success while your shield can interpose.

**Proposed complete procedure**

While proficiently wielding a usable actual shield that supplies its defensive contribution, gain+1AC as this feat's separate modifier; duplicate copies do not stack. If you succeed on a DEX save whose printed ordinary success would deal half damage, you may spend Reaction before damage to take0 from that save's damage event. NEW your shield must physically interpose against the effect's actual incoming origin/line; it cannot block an effect originating inside your body or bypass an express shield-ignoring clause. Area eligibility follows actual origin-to-target line and the same cover geometry; an all-around explosion is not automatically unblockable if a real incoming line can be interposed. Other conditions or nondamage consequences remain. Failed saves receive no reduction; a successful reroll can qualify before damage, consuming only one Reaction. If another feature already made the damage0, spending this Reaction is unnecessary.

**Explicit NEW choices:** AC dependence and successful-save timing; concrete interposition scope without universal area immunity.

**Worked adjudications**

- A successful DEX save would halve12fire to6; a legal shield interposition Reaction changes that damage to0.

- A failed save still deals normal failure damage; this feat does not turn failure into a success or remove an attached condition.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "shield_expert",
  "name": "Shield Expert",
  "description": "Shield Proficiency supports the listed +2 AC and +10% block chance.",
  "prerequisite": "Shield Proficiency",
  "effect": "Gain +1 AC while wielding a shield. When a Dexterity save would deal half damage, use your reaction to take no damage on a success while your shield can interpose.",
  "type": "Combat",
  "legacyEffect": "+2 AC and +10% block chance",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind the+1 AC as a separate actual eligible modifier and worn/wielded shield requirements. Define interposition, Reaction timing on a successful Dexterity half-damage save, area/cover geometry, rerolls and no change to failed saves.

</details>

### CF-32 — Sure Shot

Source identity: `sure_shot`. Original prerequisite: **Dexterity 14+, Ranged Proficiency**.

**Original effect, unchanged**

Your ranged weapon attacks ignore 2 points of AC granted by armor or cover. This does not ignore magical barriers.

**Proposed complete procedure**

For your ranged weapon attacks, ignore up to2 points of actual target AC attributable to worn physical armor or ordinary cover, combined rather than2 from each. NEW compute physical armor contribution as max(0, the actual suit formula including its grade and permittedDEX minus10), before magic enhancement; do not count an unarmored/natural-armor formula, shield, independent feat AC or magical enhancement as suit contribution. An actual magical armor enhancement is not removable here; physical base armor still is. Ordinary half/three-quarters cover can supply removable points; a magical barrier's cover/AC cannot. Choose eligible cover contribution first, then suit, up to2 total. This is a target-specific attack comparison, not a lasting AC reduction. Total cover remains untargetable even if physically supplied. Spell attacks and a thrown melee-class weapon are not ranged-weapon attacks for this classification unless its actual profile also says ranged.

**Explicit NEW choices:** Explicit suit-baseline attribution, combined2-point budget, exclusion of shield/natural/enchanted contribution and range classification.

**Worked adjudications**

- A chain-armored target with actualAC16 is compared at14 for a legal ranged weapon attack.

- An unarmored target behind half cover loses that ordinary+2 for this shot. Total cover still blocks the shot, and a magical barrier's+2 stays.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "sure_shot",
  "name": "Sure Shot",
  "description": "Dexterity 14+ and Ranged Proficiency support the listed armor ignore on ranged attacks.",
  "prerequisite": "Dexterity 14+, Ranged Proficiency",
  "effect": "Your ranged weapon attacks ignore 2 points of AC granted by armor or cover. This does not ignore magical barriers.",
  "type": "Combat",
  "legacyEffect": "Ranged attacks ignore 25% armor",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define attribution of up to2 AC to armor or cover across suit formulas, natural/unarmored defenses, shields, negative grades and magical enhancement. Identify what counts as a magical barrier and preserve total-cover targeting limits.

</details>

### CF-33 — Tactical Flanker

Source identity: `tactical_flanker`. Original prerequisite: **Intelligence 12+, Melee**.

**Original effect, unchanged**

Once per turn when you and an ally flank a creature, one of you adds 1d6 damage to a successful melee attack against it.

**Proposed complete procedure**

NEW feat-only geometry: you and one other willing allied, non-Incapacitated creature each threaten the same enemy with an actual legal melee attack, and the straight segment joining your occupied-space centers crosses the interior of that enemy's occupied footprint, placing you on opposite sides. Measure actual occupied bodies on the current map; a large creature needs opposite sides of its whole footprint, not merely two nearby squares. Both participants must perceive the target and be able to attack it; total cover or unusable reach prevents flanking. This geometry itself grants no universal advantage. Once per turn, when either participant hits that enemy with a melee attack, you may assign your feat allowance to add1d6 of one native damage type to that hit before damage is rolled. No Action/Reaction is required, but you must be conscious and able to coordinate. One successful attack may receive only one Tactical Flanker die across all owners; choose its funding owner before rolling. A critical doubles this attack rider die. Misses spend nothing; using your allowance on an ally prevents using it again on your own hit that actual turn. Perception/reach/geometry must hold at the hit.

**Explicit NEW choices:** Opposite-side geometry, active coordination, owner-funded allied hit and one family die per attack.

**Worked adjudications**

- Two conscious allies threaten opposite sides of a Medium foe. One owner funds1d6 on the other's hit; a critical makes that rider2d6.

- Three feat owners surround a foe. The same hit still receives only one Tactical Flanker die, with one chosen owner's allowance spent.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "tactical_flanker",
  "name": "Tactical Flanker",
  "description": "Intelligence 12+ and Melee support the listed ally damage while flanking with you.",
  "prerequisite": "Intelligence 12+, Melee",
  "effect": "Once per turn when you and an ally flank a creature, one of you adds 1d6 damage to a successful melee attack against it.",
  "type": "Combat",
  "legacyEffect": "Allies gain +1d6 dmg when flanking with you",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Supply or locate the exact current flanking geometry. Define which owner's once-per-turn budget funds which ally attack, designation timing, same-hit collisions across owners, damage type and no duplicated1d6 from one triggering application.

</details>

### CF-34 — Target Mark

Source identity: `target_mark`. Original prerequisite: **Wisdom 14+, Ranged**.

**Original effect, unchanged**

As a bonus action, mark a creature you can see within weapon range for 1 minute. The first attack by each ally against it gains +1 to hit. You may maintain only one mark and regain this use after a short rest.

**Proposed complete procedure**

Bonus Action, once per short rest: while holding an actual usable ranged weapon, choose a creature you can see within that weapon's printed maximum legal long range (normal range if no long value) and with line of effect. NEW a thrown weapon with an actual range also qualifies. Record the chosen weapon only to establish activation range; stowing it later does not end the mark. For1minute, the first attack against the marked creature by each other creature currently allied to you gains+1 to hit. This is once per ally identity for the entire mark, not per turn, and is consumed by that attack even if it misses. You are not your own ally for this feat. A creature's later alliance change does not reset its used identity; a newly arriving genuine ally can use its own first attack. Only one mark per owner; replacement, owner death or expiry ends the old record. NEW owner incapacitation does not end an existing mark. No continuous range/tether after activation and no vision/targeting permission is granted. Multiple marks never give more than+1 to the same attack; all applicable unspent first-attack entitlements for that attacker consume on that first event.

**Explicit NEW choices:** Activation range, no self, whole-mark identity budget, overlap consumption and ending.

**Worked adjudications**

- An ally misses its first attack and later hits in round2. Only the miss received the mark's+1.

- Two commanders mark the same target. An ally's first attack gains+1, not+2, and consumes that ally's first-attack entitlement in both marks.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "target_mark",
  "name": "Target Mark",
  "description": "Wisdom 14+ and Ranged support the listed mark that increases damage taken by the target.",
  "prerequisite": "Wisdom 14+, Ranged",
  "effect": "As a bonus action, mark a creature you can see within weapon range for 1 minute. The first attack by each ally against it gains +1 to hit. You may maintain only one mark and regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "Mark target to take 10% more dmg",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define weapon range as normal/long and the actual selected weapon; target legality, sight/cover and mark ending/replacement. Resolve first attack by each ally per mark versus per turn, whether self qualifies, application after misses, alliance changes and short-rest recovery.

</details>

### CF-35 — Unstoppable Force

Source identity: `unstoppable_force`. Original prerequisite: **Strength 14+, Level 8**.

**Original effect, unchanged**

When you push or knock a creature, increase the distance by 5 feet. Once per turn, a creature that fails the save by 5 or more is also knocked prone.

**Proposed complete procedure**

Whenever your own direct legal effect pushes or knocks a creature a positive specified distance away from you or along its printed outward direction, increase that displacement by5ft. It can modify a weapon, ordinary maneuver, spell or class effect if you are the actual source; not a companion's own effect, pull, teleport, fall, current, carried movement or copy/transfer. Preserve its original size/eligibility/path. Add the5 once per displacement event; same-family copies do not add further5. The final movement still stops at walls, anchors and illegal positions. Once per turn, if that same displacement-producing effect has an actual STR/DEX/other save which the target fails by5 or more, also apply Prone independently of blocked displacement. No save is invented for an ordinary opposed Shove; its numerical contest difference is not a save failure margin. Automatic failure has no numerical margin unless its source explicitly says otherwise. If an original effect already applies Prone, do not duplicate it.

**Explicit NEW choices:** Positive outward displacement predicate, once-per-event extension and literal saved failure margin.

**Worked adjudications**

- Bull Rush's failed save pushes10ft instead of5; a wall at5 stops it there, but the original Prone still applies.

- An ordinary Shove contest succeeds by7. Its push grows to10ft, but no fail-by5 save exists to add Prone.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "unstoppable_force",
  "name": "Unstoppable Force",
  "description": "Strength 14+ and Level 8 support the listed +10% knockback chance.",
  "prerequisite": "Strength 14+, Level 8",
  "effect": "When you push or knock a creature, increase the distance by 5 feet. Once per turn, a creature that fails the save by 5 or more is also knocked prone.",
  "type": "Combat",
  "legacyEffect": "+10% knockback chance",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define push/knock scope including mundane/spell/class effects, whether pulls qualify, bonus displacement limits and blocked movement. Resolve prone on fail-by5 where the original effect uses a contest or no save, cadence and interaction with Bull Rush.

</details>

### CF-36 — Volley

Source identity: `volley`. Original prerequisite: **Level 8**.

**Original effect, unchanged**

Rain arrows in small area.

**Proposed complete procedure**

NEW full completion: Action, once per short rest, wield a loaded/properly supplied bow using arrows and choose a visible point within that bow's actual normal range and line of effect. Select up to PB distinct perceived creatures in a10ft-radius area around that point, each independently in normal range and with a legal shot. You may exclude allies; no hidden-target scan or compulsory friendly fire is added. Lock targets/order, spend the use and one actual arrow per selected target, then make one separate normal ranged weapon attack against each. Apply actual AC, cover, proficiency, crits and ordinary native bow damage to each; there is no area save/DC or shared damage roll. Extra Attack does not multiply this special Action. Each target at most once; newly entering creatures cannot replace lost targets. A target becoming illegal before its shot is skipped and its committed arrow remains spent. Interrupted remaining shots lose the use and committed ammunition. Loading/reload and all other item restrictions remain, so a weapon that cannot fire the necessary arrows cannot declare that many shots. It is a special Volley Action, not Attack Action for Double Tap or Eldritch Combat.

**Explicit NEW choices:** Entire bow/Action/SR/PB-target/10ft-radius/normal-range/individual-attacks/committed-ammunition completion.

**Worked adjudications**

- PB3 with a bow selects three enemies and commits3arrows; roll three separate attacks and damage only actual hits.

- A wall gives one target total cover before its shot. Skip it without a replacement target or arrow refund; the other legal shots remain.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "volley",
  "name": "Volley",
  "description": "Level 8 supports the listed rain of arrows in a small area.",
  "prerequisite": "Level 8",
  "effect": "Rain arrows in small area.",
  "type": "Combat",
  "legacyEffect": "Rain arrows in small area",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Complete weapon/ammunition requirements, Action and frequency, area shape/size/origin/range/line, attacks versus saves/DC, target selection, damage, miss outcomes and ammunition expenditure. The retained 'small area' is not an operational template.

</details>

### CF-37 — Weapon Finesse

Source identity: `weapon_finesse`. Original prerequisite: **Dexterity 15+**.

**Original effect, unchanged**

Use Dexterity for melee attack rolls.

**Proposed complete procedure**

For a melee attack normally using STR, you may use DEX instead for the attack roll only. NEW this includes actual melee weapon, natural and unarmed attacks, but does not replace a spell's designated casting ability or a special attack expressly locked to another stat. Damage still uses its original ability unless the weapon's actual Finesse property or another feature independently changes damage too. ChoosingDEX here does not grant the Finesse property, change weapon weight/hands/reach, make a Heavy weapon light, waive STR/size requirements, or qualify for a STR-attack-only Power Attack. Actual PB requires actual proficiency as before. Source attack-modifier-dependent save DCs, such as Disarming Blow, use the actual DEX attack modifier when this swap applied; STR-fixed feats retain STR.

**Explicit NEW choices:** STR melee attack-only substitution, natural/unarmed inclusion and no Finesse-property or casting-stat grant.

**Worked adjudications**

- A longsword attack may useDEX+4 to hit while damage still addsSTR+1.

- A dagger already possessing Finesse can independently useDEX for both; the feat is not the reason that dagger's damage changes.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "weapon_finesse",
  "name": "Weapon Finesse",
  "description": "Dexterity 15+ supports using Dexterity for melee attack rolls.",
  "prerequisite": "Dexterity 15+",
  "effect": "Use Dexterity for melee attack rolls.",
  "type": "Combat",
  "legacyEffect": "Use Dexterity for melee attack rolls",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind eligible melee attack types, actual weapon/natural/unarmed distinctions and attack-only versus damage ability. Preserve Strength-dependent prerequisites and weapon properties unless an explicit completion changes them.

</details>

### CF-38 — Weapon Mastery

Source identity: `weapon_mastery`. Original prerequisite: **Proficient, Level 6**.

**Original effect, unchanged**

+1 crit range with chosen weapon.

**Proposed complete procedure**

At acquisition, choose one actual weapon profile/type in which you are proficient; permanent choice, nonrepeatable. At total character level6+, attacks with that type have critical range19–20 instead of the ordinary20. NEW the printed+1 range is one downward threshold step from the ordinary20, not an additive modifier on another expanded range. Compare all applicable actual critical ranges and use the broadest, consistent with reviewed Core. Natural19 must still meetAC; natural20 retains its automatic-hit rule. Melee or thrown use of the chosen weapon type qualifies, but improvised use without that profile does not. A specific natural weapon may be chosen only if it is a genuine proficient weapon profile, not all natural/unarmed attacks by umbrella label. No external weapon-mastery maneuver system is imported.

**Explicit NEW choices:** Permanent weapon-type selection,19–20 standalone range and no additive critical stacking.

**Worked adjudications**

- Chosen longsword natural19 totaling21 againstAC20 is critical; totaling18 misses.

- Weapon Mastery plus Exploit Weakness still yields19–20. An independently granted18–20 range stays18–20, not17–20.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "weapon_mastery",
  "name": "Weapon Mastery",
  "description": "Proficient, Level 6 supports the listed +1 crit range with a chosen weapon.",
  "prerequisite": "Proficient, Level 6",
  "effect": "+1 crit range with chosen weapon.",
  "type": "Combat",
  "legacyEffect": "+1 crit range with chosen weapon",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define chosen weapon type, actual proficiency, character-level prerequisite and whether repeatable. Specify+1 critical range semantics, floor/limit and arbitration with Exploit Weakness and other critical features; no imported external Weapon Mastery system.

</details>

### CF-39 — Whip Control

Source identity: `whip_control`. Original prerequisite: **Dexterity 15+, Whip**.

**Original effect, unchanged**

Disarm or trip with whip.

**Proposed complete procedure**

With actual Whip proficiency, wielding a usable whip, replace one attack of your Attack Action with one control attempt against a creature within the whip's actual melee reach. Choose disarm or trip before the roll. NEW make one weapon check d20+the whip's actual attack ability modifier+PB against the target's chosen STR Athletics orDEX Acrobatics total; opposed ties preserve state. This deals no damage, cannot crit, and is not a hit for on-hit riders. Trip requires target no more than one size larger and on success applies Prone subject to immunity/support. Disarm requires one actual reachable held object; on success choose a legal adjacent unoccupied drop space, otherwise the target's space, respecting real non-droppable bonds. No rest cap, but each attempt spends one actual Attack Action attack. Whip reach does not create a grapple or long-term restraint. Lunge modifies one melee weapon attack, not this check, so does not extend the control reach.

**Explicit NEW choices:** Attack replacement, opposed weapon check, no damage, trip size cap and exact drop geometry.

**Worked adjudications**

- A whip at10ft reaches a Large enemy. Weapon check18 beats Acrobatics15 and trips it without damage.

- An opposed tie leaves a held sword in place. The attack replacement was spent and no hit-trigger damage occurs.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "whip_control",
  "name": "Whip Control",
  "description": "Dexterity 15+ and Whip support the listed disarm or trip with a whip.",
  "prerequisite": "Dexterity 15+, Whip",
  "effect": "Disarm or trip with whip.",
  "type": "Combat",
  "legacyEffect": "Disarm or trip with whip",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind actual Whip proficiency/use, one attack replacement or on-hit trigger, disarm versus trip choice, checks/saves/DC, reach, target size, damage/payment, frequency and legal dropped-object/push placement.

</details>

### CF-40 — Whirlwind Striker

Source identity: `whirlwind_striker`. Original prerequisite: **Level 10**.

**Original effect, unchanged**

+5% evasion and +10% cleave when surrounded.

**Proposed complete procedure**

NEW complete interpretation: surrounded means at least two different conscious hostile creatures within5ft of you, on opposite sides under Tactical Flanker's center-segment geometry, each currently able to attack you in melee. While that predicate holds, gain+1AC as an explicit conversion of the source's undefined+5% evasion; this is not literal5%damage reduction or a separate avoidance roll. Once on your own turn, after your melee weapon attack hits a creature while surrounded, you may deal a cleave packet to one different perceived hostile creature within the actual reach of that same weapon. Amount is floor10% of that hit's eligible native weapon damage before percentages/defenses; allocate native types as shared arithmetic. No second attack roll, no new critical and no on-hit riders/resources from this derived packet; ordinary recipient defenses apply. The primary attack can be fully mitigated and still supply its legal pre-defense native amount, but a missed attack cannot. Cleave needs real reach/line, deals0 if the rounded amount is0, and cannot itself cleave or trigger a drop-generated attack/heal. Losing surrounded geometry ends AC immediately.

**Explicit NEW choices:** Explicit+5% evasion→+1AC conversion, opposite-hostile geometry and finite10% derived cleave rather than imported class ability.

**Worked adjudications**

- Two opposite adjacent melee foes qualify; a native19-damage hit yields a1-damage cleave packet to one other legal foe.

- One surrounding enemy becomes Incapacitated. The+1AC ends immediately; a later hit cannot use this feat's cleave until the predicate returns.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "whirlwind_striker",
  "name": "Whirlwind Striker",
  "description": "Level 10 supports the listed +5% evasion and +10% cleave when surrounded.",
  "prerequisite": "Level 10",
  "effect": "+5% evasion and +10% cleave when surrounded.",
  "type": "Combat",
  "legacyEffect": "+5% evasion and +10% cleave when surrounded",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Complete surrounded geometry, meaning of evasion and cleave, exact percentage bases/rounding, triggers, targets, costs, frequency and ending. Preserve the+5%/+10% originals and label any conversion as NEW.

</details>

### CF-41 — Eldritch Combat

Source identity: `eldritch_combat`. Original prerequisite: **Spellcasting ability, proficiency with martial weapons**.

**Original effect, unchanged**

When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.

**Proposed complete procedure**

Acquire only with a real spellcasting route and actual martial-weapon proficiency. NEW read1st-level as rank1 for this feat only. Once on your own regular-turn interval, when you take Attack Action and complete its attack sequence, append one actually available Action-time rank0 or rank1 spell with literal Touch or Self range as part of that same Action. You must have hit a creature with at least one of those attacks if choosing an external Touch target; that exact hit creature must also be a legal sole recipient of the spell. A Self spell must actually target only you, not a cone/area originating from Self that independently targets others. Spell must be acquired/prepared on a legitimate route with real level/rank access, RP or finite charge, components/hands/focus, target consent where required, concentration, Dissonance/Refrain, casting prohibitions and interruption. No normal casting cost is waived. An attack hit does not substitute for a spell's own required attack/save. Longer spells, BA spells and Reaction spells are not compressed by this grant. Separately, once per SR after your melee weapon attack hits, you may append one legitimately available Action-time Touch spell of any legally accessible rank to that same sole target without an extra Action; this can occur off-turn. NEW both modes share at most one embedded cast per actual regular creature turn and cannot be combined on the same hit/Action. Spend SR use at casting commitment, even if countered. These appended castings do not provoke opportunity attacks solely for casting/performing the appended attack-spell operation, but movement has ordinary triggers. Neither casting may create a further Eldritch append from attacks in its own causal root. Actual source-specific secondary/resource restrictions remain; no prestige class is acquired.

**Explicit NEW choices:** Rank translation, Action-time only, one-self/one-touch recipient, timing, shared one embedded cast per actual turn and paid independent casting.

**Worked adjudications**

- After a successful sword Attack, a legitimately prepared Touch rank1 spell can target that hit creature, paying actualRP/components; the sword hit does not make its spell attack automatically hit.

- An opportunity sword hit may use the separate SR Touch cast if legal and unspent. A Touch spell with a1minute casting time remains ineligible.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "eldritch_combat",
  "name": "Eldritch Combat",
  "description": "Your strikes carry whispers from beyond the veil—steel and sigil in a single motion. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency with martial weapons",
  "effect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve legacy1st-level against this game's rank system; actual repertoire/casting-class access, RP/components/concentration/Dissonance and independent casting-time eligibility. Define ordering with Attack action, hit prerequisite, touch/self target clauses, reaction-triggered free casts, cadence and separate short-rest use without granting free costs.

</details>

### CF-42 — Favored Enemy (Dragon)

Source identity: `favored_enemy_dragon`. Original prerequisite: **Proficiency in Survival, level 5+**.

**Original effect, unchanged**

You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.

**Proposed complete procedure**

Use actual supplied creature-type/tag facts: Dragon and expressly recorded dragonkin qualify for the+2damage and knowledge clauses; do not infer these tags from a humanoid ancestry name or settle origins. Add+2flat once per own direct damage event against a qualifying creature, of one native type, before defenses; no copied, periodic, reflected or controller-owned companion event. Advantage applies to genuine Survival tracking/ecology checks and NEW INT Nature checks representing the source's undefined Lore for physical draconic ancestry traits, breath type and lair habits; Arcana/History can use their actual separate task if relevant but receive no automatic substitute proficiency. NEW in initiative spend Action to observe a visible dragon within60ft, outside initiative1minute; DC=10+ceil(actualCR), or15 when noCR exists, adjusted only for explicitly established concealment of facts. Success gives one useful actually available requested fact, not sealed origins. On such success against a visible actual Dragon, brief other willing allies within30ft who can perceive/understand you; you and those fixed recipients gain+1 to saves against that individual dragon's breath through encounter end. Same feat family does not stack and later entrants require a new successful actual read/brief. Fear caused specifically by a dragon's presence lasts at most through your next future original regular start, then that source record ends; other fear remains. Once per SR, no Action during your movement while actually pursuing that dragon, ignore difficult-terrain movement surcharge caused by its real lair hazards through the current turn's end (outside initiative6seconds). Hazard damage/saves and impassability remain. No real bestiary record is retyped by this proposal.

**Explicit NEW choices:** Literal tags, own-event+2, Nature/Lore bridge, finite observationDC/time/briefing, one-round presence fear and one-turn terrain use.

**Worked adjudications**

- A CR7 Dragon observationDC17 succeeds; three briefed allies within30 gain+1 against that dragon's breath for the encounter.

- Ignoring acidic-pool difficult terrain while pursuing the dragon removes movement surcharge only. Acid damage and other actual pool checks still resolve.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "favored_enemy_dragon",
  "name": "Favored Enemy (Dragon)",
  "description": "You have studied scaled tyrants—their breath, their pride, the tell before the roar. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
  "prerequisite": "Proficiency in Survival, level 5+",
  "effect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind current bestiary dragon/dragonkin tags without cosmology or ancestry retcons; damage event scope, Survival/Lore skill mapping and genuine information checks. Define ally+1 breath-save radius/timing/duration, Frightened one-round limit, difficult-terrain use/duration and continuing lair hazard damage.

</details>

### CF-43 — Frenzied Rage

Source identity: `frenzied_rage`. Original prerequisite: **Constitution 15+, Berserker feat or class rage ability**.

**Original effect, unchanged**

While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.

**Proposed complete procedure**

Acquire with CON15 and the actual Berserker feat or an actual class feature expressly granting a rage state. No name-only qualification from Berserker Brew, Mooncursed, a prestige lineage or a damage buff. While in an actual acquired Berserker rage, replace its+2 melee bonus with+3 on melee weapon attacks; for any other qualifying rage lacking that+2, NEW grant+3flat melee-weapon damage as this feat's own family, without replacing separately rolled dice. Do not add+3 on top of the same Berserker+2. Berserker Rage CF-03 is an operating rage once this feat was legally acquired by its printed prerequisite, but not an acquisition substitute. Once per turn after your melee attack reduces an independent meaningful hostile from positiveHP to0, choose EITHER one immediate additional melee attack (NEW only on your own turn) OR extend that same currently active rage's time endpoint by one original6second round. Extra attack requires real reach/target/weapon/capability and creates no Action/BA; shared causal limits prevent drop-trigger attack chains. NEW at most three time extensions per single rage use; non-time endings such as incapacitation or missing upkeep remain. Once per rage, on your turn spend BA to charge along a declared straight legal route with a separate current walking-Speed movement-cost budget, through at most three hostile creatures no more than one size larger. Recheck a complete legal unoccupied endpoint before starting, pay occupied-space difficult cost and normal hazards/opportunity attacks. Each crossed creature once makesCON save DC8+PB+STR; failure applies Dazed until its next future original regular end. No damage/Prone/push is implied. If the route is interrupted, stop in the last legal space; already crossed targets remain affected and use stays spent. It cannot force passage when there is no legal complete crossing route.

**Explicit NEW choices:** Explicit rage-source distinction, replacement damage, hostile reward gate, once-turn extra attack/extension choice, three-extension cap and full BA charge procedure.

**Worked adjudications**

- Berserker's+2 becomes+3, not+5. A drop can fund one extra own-turn attack; a drop from that extra attack cannot spawn another.

- After three accepted extensions (+18seconds), a fourth drop cannot extend that same rage further. Incapacitation still ends a rage that has that endpoint.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "frenzied_rage",
  "name": "Frenzied Rage",
  "description": "Rage becomes avalanche—each kill feeds the next swing until the world is only red and thunder. Prestige lineage: Berserker. completed from the existing development record.)",
  "prerequisite": "Constitution 15+, Berserker feat or class rage ability",
  "effect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve all three clauses: replacement+3 instead of+2, drop-trigger extra attack OR one-round extension, and once-per-rage charge with Dazed. Bind valid rage sources and acquisition prerequisites, action/cadence/caps, movement/save/DC/targets/duration, avoiding unlimited kill/extension loops or name-only class eligibility.

</details>

### CF-44 — Giant Slayer

Source identity: `giant_slayer`. Original prerequisite: **Precision Strike or level 8+**.

**Original effect, unchanged**

You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.

**Proposed complete procedure**

Acquire with actual Precision Strike OR total level8. Against actual Large-or-larger creatures, add floor20% of each own direct damage event's eligible native amount before defenses, using shared noncompounding percent arithmetic. This broad damage clause includes own actual spell and weapon components but not periodic/copy/reflection/transfer or companion-owned attacks. Once per SR after a melee attack hits a Huge-or-larger creature, before damage declare the cripple use; after damage halve all its current Speed modes through its next future regular end, retaining spent movement cost. NEW no additional save is invented; same feat family halves once and actual immunities/specific movement protections apply. When a Huge-or-larger enemy misses you with a melee attack, you may spend Reaction for a separate5ft movement-cost step, then, only if that creature is within your own actual melee weapon/natural/unarmed reach and line, deal1d6 direct damage of that legal attack profile's native physical type (bludgeoning for unarmed) without an attack roll. You may step0 if already in reach; normal terrain/opportunity attacks/Speed restrictions apply. If the step cannot bring it into your reach, do not start this Reaction. The original source wording about stepping into its reach does not let you strike from beyond your own reach. It then has disadvantage on its next attack against you before its next future regular end, consumed hit or miss. Direct reaction damage is not a hit/critical, cannot start attack/heal/resource chains, and receives no added Giant Slayer percent because it is this feat's derived reaction packet.

**Explicit NEW choices:** Broad percent event scope, no-save cripple, complete5ft reaction step/own-reach/direct-damage contract and no recursion.

**Worked adjudications**

- A native27-damage hit against Large adds5 for32 before defenses, independently of other eligible percent sources.

- A Huge enemy misses from15ft away while your reach is5. A5ft step cannot reach it, so this Reaction is unavailable; its own15ft reach is not yours.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "giant_slayer",
  "name": "Giant Slayer",
  "description": "Colossi fall when the small learn where the giant bleeds. Prestige lineage: Giant Killer. completed from the existing development record.)",
  "prerequisite": "Precision Strike or level 8+",
  "effect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind Size thresholds and the+20% damage base/order, successful melee-hit speed-halving timing/recovery and short-rest use. Complete miss-trigger Reaction movement budget/reach, direct1d6 versus an attack, type, geometry and disadvantage deadline. Preserve all three effects.

</details>

### CF-45 — Life Drinker

Source identity: `life_drinker`. Original prerequisite: **Dark Affinity or Hemocraft**.

**Original effect, unchanged**

When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.

**Proposed complete procedure**

Acquisition requires the exact source feat dark_affinity OR hemocraft, legitimately acquired under its eventual reviewed procedure; neither is silently granted or approved here. NEW finite Life Drinker Recovery Reserve=2×total character level, initially full on feat acquisition and refilled only by a completed LR. Level increases raise capacity without refilling current reserve; capacity reductions clamp without damage. This is a distinct personal feat reserve, not Mutation Recovery Reserve. After your direct melee critical against an independent meaningful hostile resolves, one healing event has base floor(actualDamageDealt/2), using the reviewed metric tempAbsorbed+actualHpDamage with no overkill, floor-protected or state-assignment loss. After your direct melee attack reduces such a hostile from positiveHP to0, a separate healing event has base current total level. NEW resolve critical healing then drop healing if both trigger, spending actualHP restored from the same finite reserve; available reserve caps each after ordinary healing modifiers/prohibitions/max/Critical ceiling. No healing on dead self, no Wound cure, resurrection, copied-damage reward or artificial resource farm. Suppress secondary healing/resource/excess-conversion triggers from these recovery events as an explicit anti-loop choice. Blocked/fullHP healing spends0 reserve but grants no stored heal. While your actual normalHP is strictly below half your current effective maximum before an attack's damage (tempHP excluded), melee weapon attacks against creatures with actual blood add1d4 necrotic before defenses and critical doubling. Actual blood fact, not type-name inference; no rider against known bloodless bodies. The extra die may contribute to that same legitimate critical's numeric damage, never copied again. Healing after the hit cannot retroactively remove its already-qualified die.

**Explicit NEW choices:** Finite2×level LR reserve, current reviewed temp-inclusive numeric drain metric, meaningful-hostile reward gate, ordered same-hit heals and no secondary conversion; blood/threshold snapshot.

**Worked adjudications**

- A critical deals12resolved to HP3/temp4: actualDamageDealt7, so critical healing base3. The drop also offers level healing; both share remaining reserve.

- At level8 with2reserve and missing10HP, a legal base8 drop heal restores at most2 and exhausts reserve. A later critical that day cannot heal until a completed LR.

**Dependencies:** Reviewed healing/damage quantities and causal ledger; maximumHP thresholds; pending exact dark_affinity and hemocraft sources; actual blood traits.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "life_drinker",
  "name": "Life Drinker",
  "description": "Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Dark Affinity or Hemocraft",
  "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind actual Dark Affinity/Hemocraft prerequisite IDs without approving them. Resolve critical-hit healing from final paid HP damage versus tempHP/overkill/copied damage, hostile0HP healing identity/cadence and simultaneous triggers; define below-half/creatures-with-blood rider using reviewed healing ledgers.

</details>

### CF-46 — Precision Strike

Source identity: `precision_strike`. Original prerequisite: **Dexterity 13+ or Weapon Focus**.

**Original effect, unchanged**

Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.

**Proposed complete procedure**

Acquire with permanentDEX13 OR the exact Weapon Focus feat. Once per turn before one weapon attack roll choose one mode. Ordinary mode takes−2 on that roll and, on hit, adds floor50% of its eligible native weapon damage before percentages/defenses; actual critical dice are included before this computation. NEW alternative critical mode is available when the actual target is currently Restrained, Grappled, or carries your actual active Anatomy Lore identified-weak-point record. Spend the once-per-SR critical use on declaration; take no−2 and no+50% from this feat for this attack. If it hits, treat it as critical; a miss remains a miss and spends the use and turn allowance. Condition/mark eligibility is rechecked at resolution; losing it leaves an ordinary hit with the use spent. Actual critical immunity remains; no additional critical multiplier. Either mode is mutually exclusive with Power Attack's trade on this same attack. Anatomy Lore's own separately legal bonus can coexist under its precise native-damage scope, with percentages from the same base; the weak-point prerequisite does not grant that feat or let another owner's undisclosed read qualify. A grapple by another creature suffices because that alternative predicate has no ownership restriction.

**Explicit NEW choices:** Pre-roll mode and SR declaration, replacement of both penalty and percent, own Anatomy Lore record, miss spending and noncompounding interactions.

**Worked adjudications**

- A native21 weapon packet in ordinary mode adds10 for31 before defenses, after taking−2 to hit.

- Against a Grappled foe, critical mode rolls normally. On a hit dice double without+50%; on a miss the SR use is still spent.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "precision_strike",
  "name": "Precision Strike",
  "description": "One opening. One breath. One strike where the giant's armor forgot to cover bone. Prestige lineage: Giant Killer. completed from the existing development record.)",
  "prerequisite": "Dexterity 13+ or Weapon Focus",
  "effect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind the explicit Dexterity OR Weapon Focus prerequisite, once-per-turn choice and-2/+50% arithmetic. Resolve whether automatic-critical mode replaces both penalty and percent bonus, restrained/grappled/Anatomy Lore qualification, timing, short-rest charge and immunity/critical-range interfaces.

</details>

### CF-47 — Slayer’s Resolve

Source identity: `slayer_s_resolve`. Original prerequisite: **Favored Enemy (Dragon) or level 8+**.

**Original effect, unchanged**

You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.

**Proposed complete procedure**

Acquire with actual Favored Enemy (Dragon) OR total level8. You are immune specifically to actual Dragons' Frightful Presence effects; unrelated dragon fear/spell effects are not automatically that identity. Existing source-qualified Frightful Presence records are suppressed while immunity applies, with clocks retained. While you are conscious, other allied creatures within30ft and with line of effect to you have advantage on saves against effects that actually impose fear/Frightened; no hearing or common-language gate is added. This is current-position aura, checked at each save, not a permanent recipient list and not self-benefit. Gain+2AC against actual attacks made by a creature explicitly typed Dragon; dragonkin alone does not satisfy this feat. Once per SR, when a Dragon you can see makes a melee attack targeting you, spend Reaction before the attack roll to impose disadvantage on that one attack. Alternatively, when such a Dragon's actual breath weapon requires your save, after the initial result but before consequences, spend Reaction and the same shared SR use to reroll your whole save with advantage; independent disadvantage cancels normally and the new result is mandatory. It does not reroll anyone else or waive a no-save breath effect. A breath that instead makes an attack roll is eligible only for the attack mode if it is actually melee; the source's breath-save language creates no new save. Immunities, sight, Reaction prohibitions and actual source tags remain.

**Explicit NEW choices:** Source-qualified immunity, conscious other-ally aura/line, Dragon-onlyAC, two exact declaration windows and mandatory save reroll.

**Worked adjudications**

- A visible Dragon melee attack prompts the pre-roll Reaction, consuming the shared SR use even if it misses.

- A breath DEX save initially fails. The owner rerolls with advantage before damage and must keep the new result; nearby allies keep their own original saves.

**Dependencies:** Core combat and action timing; current conditions; actual equipment and feat acquisition.

<details><summary>Complete original source object and conference question</summary>

```json
{
  "id": "slayer_s_resolve",
  "name": "Slayer’s Resolve",
  "description": "You have buried friends under dragonfire. Their memory is armor the wyrms cannot melt. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
  "prerequisite": "Favored Enemy (Dragon) or level 8+",
  "effect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind Favored Enemy OR level prerequisite, actual dragon source tags, Frightful Presence versus broader fear immunity, conscious ally aura/line and+2 AC eligibility. Resolve Reaction declaration for attack disadvantage or personal breath-save reroll, information window, mandatory reroll choice and short-rest payment.

</details>

## Specific decisions for the joint conference

Decide each original question, including these consequential NEW boundaries: turn/extra-turn cadence; ability and weapon-category gates; percent and critical arithmetic; physical movement interruption; Defensive Stance's full15% procedure; the missing Precise Shot penalty and allied-body cover proposal; Riposte's Agility bridge and Reaction cost; shield suppression/deflection; feat-only flank geometry; finite Volley; literal Weapon Finesse attack-only substitution; Whirlwind's explicit5%-evasion conversion; Eldritch Combat paid embedded casts; literal dragon tags; Frenzied Rage reward and extension ceilings; and Life Drinker's finite reserve and reviewed numeric damage metric.

These are proposed completions, not prior reviewer agreement. Do not infer whole-class, whole-bestiary, heritage, cosmology or software completion. Reconcile the actual expedition verdict before the complete feat package is sent. Preserve conflicting source wording and the earlier unadopted proposals alongside any selected result. Final joint whole-game flow agreement precedes the authorized GitHub push, and verified remote commit precedes the careful cosmology review.
