# Remaining131-source review — PARTIAL CAPTURE

Official read_thread capture of completed Calibration Review reply. Connector caps each message at20,000 characters; this artifact ends mid-table and MUST NOT be treated as complete. Full original remains in the notebook. Follow-up requests remaining text and source corrections.

The 131-source remainder can be classified from the supplied evidence, but it exposes **four interfaces that should be discussed next before calling the healing catalog complete**: redirection, maximum-HP composition, sustained-zone scheduling, and companion/device/temp-HP lifecycle. I would not reopen the already-closed healing/death arithmetic generally; these are bounded extensions.

## Eight source conflicts

**1. Paladin cadence conflicts — resolve in favor of the explicit engine reconciliation.**

`paladin.engine[13]` is written as an intentional pilot override: the level-17 Lay on Hands Wave is **once per long rest**. The previously reviewed Hero Lay on Hands card's `1/short rest` cadence should therefore remain preserved in source but receive an operational override to **1/long rest**. This is a narrow amendment to that binding, not deletion of the card text. :chatgpt-content-reference{index="0"}

Likewise, retain both Smite statements but enforce the narrower intersection:

> **One paid Smite total per numbered round**, including any off-turn/Reaction Smite.  
> `engine[3]`'s once-on-your-own-turn rule remains an additional eligibility restriction, not a second allowance.

Thus an off-turn Smite before the Paladin's initiative can consume that numbered round's shared Smite allowance; the later own-turn Smite is then unavailable.

---

**2. Oracle asynchronous zones need a source-owned pulse-window schedule.**

`oracle.engine[26]` says persistent healing/damaging zones have at most three pulses and require 1 RC before each pulse after the first. For target-start zones, that cannot mean “pay once for every ally.” :chatgpt-content-reference{index="1"}

Use this **NEW schedule bridge**:

- activation pays the card's printed start cost and opens **pulse window 1**;
- all legal asynchronous target-start events in that window use that one funded pulse window;
- at the Oracle's next regular start, pay **1 RC once** to open window 2;
- at the following regular start, pay **1 RC once** to open window 3;
- failure/refusal to pay ends the zone before the new window opens;
- a creature can benefit at most once in a numbered round and never more than the source's total-per-creature cap;
- payment is per **zone pulse window**, never per target.

This should apply to ordinary Oracle healing zones such as `oracle.supplement.life.resonant-seed` and the previously reviewed `garden-of-restoration`. Resonant Seed's printed 1 RC is the activation cost; engine[26] supplies the later generic upkeep. :chatgpt-content-reference{index="2"}

Once-per-long-rest Finals with printed pulses are explicitly exempt from generic upkeep. `oracle.supplement.flame.crown-restored` therefore gets its printed three target-start pulses without extra RC. :chatgpt-content-reference{index="3"}

The next schedule implementation packet should include at least:

`oracle.supplement.life.resonant-seed`  
`oracle.supplement.life.garden-of-restoration`  
`oracle.supplement.bones.unfinished-chorus`  
`oracle.supplement.flame.crown-restored`  
`oracle.supplement.life.eternal-bloom`

The last two are Final exceptions rather than ordinary paid-upkeep zones.

---

**3. Lifewell really does require the first Bonus Action + 1 RP.**

The wording is unusually explicit:

> “At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing.”

So `crimson-agent.hero.bloodweaver.lifewell` costs:

- Action;
- 4 RP;
- all BG, minimum 3;

to establish it, **then on that same turn** the first healing pulse requires its Bonus Action + 1 RP.

If that first maintenance is not paid, no first pulse occurs and the effect ends at turn end. This is intentionally different from Healing Briar and Restoration Field, whose activation itself includes their first healing pulse and only later pulses need maintenance. :chatgpt-content-reference{index="4"} :chatgpt-content-reference{index="5"} :chatgpt-content-reference{index="6"}

For Shaman:

- Extended Totem's fourth Renewal pulse requires a real fourth-turn **BA + 1 RP**.
- Echo Totem shares the parent totem's concentration and upkeep payment; it does **not** require a second upkeep payment.
- A creature overlapping primary Renewal and its Echo receives one same-name healing application, not full+half healing. Use the stronger primary amount.
- Echo cannot manufacture a fifth pulse. :chatgpt-content-reference{index="7"}

---

**4. Healing-dependent riders must keep their exact predicates.**

`Divine Invocation — Renewal`: the 5 Stamina is a co-resolved printed effect, not an “actual HP gained” trigger. A legal target receives the 5 Stamina even if the HP portion is reduced to 0, assuming it has a Stamina resource. This differs from base Renewal, whose source explicitly requires actual HP restoration. :chatgpt-content-reference{index="8"}

`Purging Flame`: the Poisoned/disease option is independent of actual HP gained. A legal living target at full HP can still use the cure option. :chatgpt-content-reference{index="9"}

`Zealot's Renewal`: same for its Poisoned/disease clause. Its backlash is a **separate fire-damage packet** that occurs after the heal attempt even if actual healing is 0, unless a printed Convergence/Prophecy effect suppresses it. Resolve fire resistance/immunity normally; then its explicit “cannot reduce below 1” acts as a source-local HP floor. Fire immunity can therefore make resolved backlash damage 0. The floor does not turn immunity into 1 damage. :chatgpt-content-reference{index="10"}

`Flame Prophecy Trigger`: the healing branch requires actual HP restoration; the fire branch requires a positive fire-damage packet. :chatgpt-content-reference{index="11"}

`Bloodbond`: “when a paid technique heals you” means **actual positive HP restoration** by the owner. An attempted but fully blocked heal grants no M temporary HP. :chatgpt-content-reference{index="12"}

Enhanced First Flame Convergence's S temporary HP likewise requires the Zealot's Renewal target to have actually regained HP.

---

**5. Crown's Burn gets a deterministic numeric bridge.**

Use `actualDamageDealt`, not merely positive packets, for the pooled fire total. :chatgpt-content-reference{index="13"}

Operationally:

1. Choose 0–3 legal allied recipients.
2. Resolve every meaningful hostile's fire packet.
3. Sum their numeric `actualDamageDealt`.
4. If no recipients were chosen, skip healing entirely—never divide by zero.
5. Otherwise `share = floor(totalActualFireDamage / recipientCount)`.
6. Each recipient rolls its own `S d6 + M` healing-cap roll.
7. Its source base heal is the lesser of that share and its own roll.
8. If total numeric actual fire damage was positive, source minimum becomes 1.

So a positive packet that produces `actualDamageDealt = 0` because of a 1-HP floor does **not** activate Crown's Burn's minimum-1 healing clause.

I would use **independent healing rolls per recipient**, because unlike the game's explicitly shared-roll cards, Crown's Burn does not say “roll once.” This is a NEW deterministic interpretation.

For provenance generally:

- an explicit shared roll has one `rollInstanceId`; every target receives its own application using that same raw total;
- target reductions/caps still resolve separately;
- an explicit “half the rolled amount” copy becomes a flat copied numeric amount with `diceCount=0`;
- a feature saying “add 1d6” adds a real die and increments healing `diceCount`.

That distinction matters for Desecrated Ground and similar per-healing-die modifiers.

---

**6. Monk maximum-HP effects are stat changes, not damage/healing.**

Within one Monk owner's effects, use the largest reduction only as `monk.engine[9]` states. :chatgpt-content-reference{index="14"}

When effective maximum HP changes:

- recompute maximum HP;
- minimum maximum remains 1;
- if current HP exceeds the new maximum, clamp current HP down to it;
- that clamp is **not damage**;
- it creates no positive-damage event;
- it creates no Wound save;
- it triggers no damage/healing/drain effects;
- restoring maximum HP later does not restore current HP.

Continuous percentage-state calculations, such as Pain Empowerment, recompute from the new maximum because they inspect current state continuously. A trigger saying the creature **falls/crosses** a percentage threshold does not trigger merely because maximum HP changed; no HP fall occurred.

The global interaction among:

- Monk temporary max-HP reductions;
- Warrior Flesh Warden;
- Exhaustion 4;
- Expedition Strain 4;
- any other max-HP modifier

remains a **maximum-HP composition dependency** and should get its own bounded pass.

`crimson-agent.hero.thirstborn.veinburst-requiem`'s later “falls to 0” clause is a separate direct HP-setting effect after its damage has resolved. It causes **no second Wound save** and adds no damage metric. Then ordinary zero-HP/dying rules begin. Damage-specific 1-HP floors do not stop this non-damage state assignment. A source whose exact wording broadly protects against any effect reducing the target to 0 may still apply; do not infer that scope for damage-only floors. :chatgpt-content-reference{index="15"}

---

**7. Keep redirection entirely separate from `actualDamageDealt`.**

Correct. The newly reviewed numeric-drain quantity must never be reused as a pre-redirection amount.

Two distinct procedures exist in these sources:

**Bloodbond**
- split `floor(1/4 × preMitigationDamage)` before mitigation;
- original target and Crimson Agent each apply their own defenses once;
- no recursive transfer. :chatgpt-content-reference{index="16"}

**Paladin engine[10]/Burden Shared**
- apply original target's defenses once;
- use resulting **post-defense, pre-temp-HP damage** as the splittable amount;
- distribute allowed amount;
- recipients receive transferred damage with no second mitigation;
- no redirection/reflection/resource generation from the transferred portion. :chatgpt-content-reference{index="17"} :chatgpt-content-reference{index="18"}

Only after each recipient's assigned packet exists do temp HP, HP loss, Wounds, floors and `actualDamageDealt` get calculated for that recipient.

This deserves the **next dedicated subsystem conference**.

---

**8. Healing/copy/device provenance must remain source-qualified.**

Druid form buffer is TEMP HP backed by its own finite Buffer Reserve; Combat Shapeshifting is real HP healing. They must not share healing triggers. :chatgpt-content-reference{index="19"}

Mirrorsage half-copy features use copied numeric amounts, not new rolls; explicit `+1d6` effects are real added dice; converted Mend is a fresh finite healing profile. Do not impose a blanket “copies never trigger anything” beyond each card's actual no-trigger language. :chatgpt-content-reference{index="20"}

Wizard Component Enhancement adds one real die to the existing healing spell packet for +1 RP. It is not a second heal or second cast. :chatgpt-content-reference{index="21"}

Shaman healing flasks consume prepared stock when thrown even if the target later receives 0 healing. Spirit Cache requires a **new** flask unit or full totem cost on replay; it does not reproduce/refund the original inventory item. :chatgpt-content-reference{index="22"}

---

# Classification of all 131 exact sources

### Cleric

| Source | Role | Operational disposition |
|---|---|---|
| `cleric.base.sacred-chant` | RESOURCE_ONLY | Sustained pulse cadence/Conviction only; no healing component. |
| `cleric.arch.miraculous-channel` | HEALING_INTERFACE | Expands legal ally targets; shared healing/numeric roll remains one roll; never multiplies resource generation. |
| `cleric.arch.divine-invocation` | HEALING_INTERFACE + RESOURCE_ONLY | Radiance/Renewal heal; Renewal's 5 Stamina is independent of actual HP gain; Echoes repeats flat copied numeric amount with no conditions/resources/triggers. |
| `cleric.hero.saint.radiant-burst` | HEALING_INTERFACE | One shared S d8 roll; healing and damage are separate target applications. |
| `cleric.hero.priest.scriptural-echo` | HEALING_INTERFACE | Half prior rolled amount; copied result is flat numeric, `diceCount=0`; no triggers/resources. |
| `cleric.hero.priest.balanced-scales` | HEALING_INTERFACE | Requires actual HP restoration to mark; retaliation uses positive damage-event predicate. |
| `cleric.hero.priest.balance-restoration` | HEALING_INTERFACE | Shared roll with separate per-target heal/damage applications. |
| `cleric.hero.priest.word-of-power` | HEALING_INTERFACE | Mercy heals; Rebuke/Command remain damage/control. |
| `cleric.hero.cultist.zealot-s-touch` | HEALING_INTERFACE | Converts printed HoT healing dice into damage; flat healing bonuses do not convert. |
| `cleric.hero.cultist.dark-sacrament` | HEALING_INTERFACE | Ally healing occurs if at least one enemy has a positive damage packet; derived heal is a flat value from the shared damage roll. |

:chatgpt-content-reference{index="23"}

### Crimson Agent / Dragoon / Druid

| Source | Role | Operational disposition |
|---|---|---|
| `crimson-agent.engine[2]` | OTHER_NAMED_DEPENDENCY | Periodic Bleed engine; allied Bloodweaver healing records are not hostile Bleeds. |
| `crimson-agent.engine[5]` | HEALING_INTERFACE | Direct HP sacrifice is non-damage, nonredirectable, floor 1. |
| `crimson-agent.arch.bloodbound-edge` | EXCLUSION | Damage detonation; expressly no healing/BG/kill-trigger benefit. |
| `crimson-agent.hero.bloodweaver.bloodbond` | TEMP_HP + OTHER_NAMED_DEPENDENCY | Actual paid-technique HP restoration triggers M temp HP; redirection uses pre-mitigation split. |
| `crimson-agent.hero.bloodweaver.crimson-pact` | HEALING_INTERFACE + TEMP_HP | One shared damage roll and separate shared healing roll; temp HP independent of actual heal. |
| `crimson-agent.hero.bloodweaver.purify-blood` | CONDITION_CURE | Poisoned/disease cure only. |
| `crimson-agent.hero.bloodweaver.lifewell` | HEALING_INTERFACE | Same-turn first BA+1RP pulse confirmed. |
| `crimson-agent.hero.thirstborn.veinburst-requiem` | OTHER_NAMED_DEPENDENCY | Post-damage direct set-to-zero; no second Wound save. |
| `crimson-agent.hero.thirstborn.crimson-harvest` | HEALING_INTERFACE + RESOURCE_ONLY | Heal/BG only if that attack actually reduces eligible target to 0. |
| `dragoon.engine[4]` | OTHER_NAMED_DEPENDENCY | Burn/Bleed and Momentum guard; no healing. |
| `dragoon.base.wyvern-s-guard` | EXCLUSION | Damage reduction only. |
| `dragoon.hero.dragon-guardian.draconic-ward` | EXCLUSION | Damage reduction only. |
| `druid.engine[4]` | TEMP_HP + RESOURCE_ONLY | Buffer/Form Surge reserves; not real healing. Exact reserve-spend-vs-existing-temp-HP interaction remains for temp-HP pass. |
| `druid.base.moon.combat-shapeshifting` | HEALING_INTERFACE | Paid real-HP self-heal; does not restore form buffer/shift uses. |

:chatgpt-content-reference{index="24"}

### Mirrorsage / Monk

| Source | Role | Operational disposition |
|---|---|---|
| `mirrorsage.base.echo-channeling` | HEALING_INTERFACE | +M pre-resolution to one Echo target, same release. |
| `mirrorsage.arch.advanced-mirrorcall` | COMPANION_DEVICE | Appearance/movement only; no HP restoration. |
| `mirrorsage.arch.dual-echo-cast` | HEALING_INTERFACE | Half component is copied flat numeric amount; at most one healing profile. |
| `mirrorsage.arch.mimicry-focus` | RESOURCE_ONLY + HEALING_INTERFACE | Focus-spent +1d6 is a real added healing/damage die. |
| `mirrorsage.arch.echo-fusion` | HEALING_INTERFACE | Full profile retains dice; half profile becomes flat copied amount. |
| `mirrorsage.arch.mirror-shift` | COMPANION_DEVICE | No HP restoration. |
| `mirrorsage.arch.focus-channel` | HEALING_INTERFACE + RESOURCE_ONLY | +1d6 option is real added die, same packet. |
| `mirrorsage.hero.light-weaver.blessed-copy` | HEALING_INTERFACE | Second-target half amount, same root/release; no new healing proc. |
| `mirrorsage.hero.light-weaver.radiant-mirror-beast` | HEALING_INTERFACE + COMPANION_DEVICE | Paid commanded primary heal; shared companion command budget. |
| `mirrorsage.hero.light-weaver.blessing-echo` | HEALING_INTERFACE + TEMP_HP | Explicit fresh Mend/Ward conversion; no simultaneous offense. |
| `mirrorsage.hero.light-weaver.purifying-reflection` | CONDITION_CURE + HEALING_INTERFACE | Heal only if rerolled condition save succeeds. |
| `mirrorsage.hero.mirror-mage.mirror-double` | EXCLUSION | Damage copy only. |
| `mirrorsage.hero.mirror-mage.reality-fracture` | HEALING_INTERFACE | +1d6 is a real added Echo healing die. |
| `mirrorsage.hero.shattered-one.fractured-dominion` | EXCLUSION | Damage-only copy. |
| `monk.engine[1]` | RESOURCE_ONLY | Ki resource/anti-farm. |
| `monk.engine[5]` | RESOURCE_ONLY | Ki-generation guard; no free healing. |
| `monk.engine[9]` | OTHER_NAMED_DEPENDENCY | Monk maximum-HP stat layer. |
| `monk.arch.martial-apex-capstone` | EXCLUSION | Healing-only technique expressly ineligible. |
| `monk.hero.iron-fist-master.ribcrusher-strike` | OTHER_NAMED_DEPENDENCY | Max-HP reduction. |
| `monk.hero.iron-fist-master.bone-breaking-strike` | OTHER_NAMED_DEPENDENCY | Max-HP reduction. |
| `monk.hero.way-of-shadow.deathless-silence` | OTHER_NAMED_DEPENDENCY | Max-HP reduction plus other combat riders. |
| `monk.hero.way-of-shadow.death-touch` | EXCLUSION | Damage finisher only. |

:chatgpt-content-reference{index="25"}

### Oracle

| Source | Role | Operational disposition |
|---|---|---|
| `oracle.engine[6]` | RESOURCE_ONLY | RC recovery ceilings and anti-farm. |
| `oracle.engine[14]` | HEALING_INTERFACE + RESOURCE_ONLY | Copy provenance: numeric component only; no RC/Prophecy/proc copying without explicit exception. |
| `oracle.engine[26]` | HEALING_INTERFACE | Generic zone schedule/upkeep; async pulse-window bridge required. |
| `oracle.supplement.shared.mystery-surge` | HEALING_INTERFACE | +S to one healing result is pre-resolution flat modifier; no extra targets/actions. |
| `oracle.supplement.burning-blood.burning-blood-boon-v` | HEALING_INTERFACE | Once/turn self-heal if at least one enemy takes a positive fire-damage packet. |
| `oracle.supplement.consumed.consumed-boon-v` | HEALING_INTERFACE | +S to one Revelation healing roll/turn. |
| `oracle.supplement.battle.host-s-cry` | HEALING_INTERFACE + RESOURCE_ONLY | Ally heal and RC refund share trigger but are independent outcomes. |
| `oracle.supplement.battle.fury-of-the-host` | HEALING_INTERFACE | First qualifying defeat each round heals 1d6. |
| `oracle.supplement.bones.death-s-threshold` | OTHER_NAMED_DEPENDENCY | Threshold defensive state; ends when current HP actually exceeds half max. |
| `oracle.supplement.bones.ledger-s-memory` | EXCLUSION | Corpse information only. |
| `oracle.supplement.bones.bones-revelation-mastery` | HEALING_INTERFACE + MOVEMENT_CONTROL_ONLY | Unfinished Chorus redirect changes recipient before resolution, not secondary healing. |
| `oracle.supplement.flame.flame-prophecy-trigger` | RESOURCE_ONLY | Heal branch requires actual HP restoration; fire branch requires positive fire packet. |
| `oracle.supplement.flame.wrathful-brand` | HEALING_INTERFACE | Triggered ally heal from positive damage event; reviewed Brand entitlement retained. |
| `oracle.supplement.flame.purging-flame` | HEALING_INTERFACE + CONDITION_CURE | Cure independent of actual HP gain. |
| `oracle.supplement.flame.crown-s-burn` | HEALING_INTERFACE | Numeric actual-fire-damage pool; division/independent-roll bridge above. |
| `oracle.supplement.flame.zealot-s-renewal` | HEALING_INTERFACE + CONDITION_CURE | Cure independent; backlash separate fire packet even if heal restores 0 unless suppressed. |
| `oracle.supplement.flame.first-flame-convergence` | HEALING_INTERFACE | Positive fire packet can create child heal; its later damage-reduction rider requires actual HP restoration. |
| `oracle.supplement.flame.flame-revelation-mastery` | HEALING_INTERFACE + TEMP_HP | Enhanced Convergence temp HP requires actual Zealot HP gain. |
| `oracle.supplement.flame.flame-prophecy` | HEALING_INTERFACE + RESOU
