# GPT redirection first review — partial capture

The completed notebook reply exceeded the connector's 20,000-character per-message capture limit. This file intentionally preserves only the returned prefix; the missing tail is not treated as reviewed evidence.

This 39-source packet supports one bounded redirection model, but **not one universal “redirect” operation**. I would use the following shared sequence plus source-specific exceptions.

## 1. Shared damage/redirection sequence

Use four quantities before the existing healing/death interface:

- `rolledPacketDamage`: finalized damage dice/flat amount after attack/save/critical resolution. A successful save has already halved here; a critical has already added its legal dice.
- `preMitigationDamage`: that finalized packet before the current recipient's DR/resistance/immunity.
- `postDefenseDamage`: after that recipient's ordinary damage defenses, **before temporary HP**.
- `actualDamageDealt`: already-closed downstream quantity after temp HP/floors/life resolution; never use this to decide a transfer amount unless a source explicitly says “actual damage dealt/absorbed.”

### A. Attack retargeting
Retarget before comparing the attack roll with AC. No damage split exists yet.

`warrior.hero.wardborn.guardian-pulse` is the supplied example.

### B. Pre-mitigation sharing
Split `preMitigationDamage`. Each branch then applies that recipient's defenses once.

Supplied examples:

- `crimson-agent.hero.bloodweaver.bloodbond`
- `crimson-agent.hero.bloodweaver.veinlock-tether`

The original attack/save/critical has already determined the raw packet. Do **not** apply the original target's resistance or flat DR before deciding the share. After splitting, each recipient applies its own eligible defenses once.

### C. Post-defense transfer
Resolve the original target's defenses first. Transfer from `postDefenseDamage`, before original temp HP.

Transferred branch:

- retains damage type;
- receives **no second DR/resistance/immunity** where source/common engine says unmitigated/no further mitigation;
- **does still interact with recipient temporary HP**, because temp HP is the later damage buffer, not a second mitigation calculation;
- still receives ordinary Wound, Instant Death, concentration and zero-HP consequences;
- may use HP floors/would-die replacements unless the source explicitly makes **death** unpreventable.

This includes the Paladin engine family, Life Linked, Shared Breath, Selfless Guardian, Guardian Tissue and Aegis Incarnate.

### D. Pure prevention
Prevention deletes part of the packet rather than creating another recipient.

Examples:

- Elemental Absorption;
- Aura of Bonds;
- Ancestral Guardian;
- Bloom Ward.

Prevented damage creates no second damage event, corpse/resource event or redirected recipient.

### E. Retaliatory/new damage
A counter/retaliation is a **new damage root**, not transferred damage.

Examples:

- Redirecting Palm's force damage;
- Guardian Pulse's counterattack.

Normal defenses apply to the new target unless its source says otherwise.

---

# 2. Bloodbond / Veinlock pre-mitigation

Confirm:

1. Original attack/save determines whether damage exists and establishes its rolled packet.
2. Critical extra dice are already included.
3. Bloodbond redirects `floor(preMitigationDamage / 4)`.
4. Veinlock may instead redirect any amount up to `min(S+M, preMitigationDamage)`.
5. They are alternatives on that event, never cumulative.
6. Original target defenses apply once to retained branch.
7. recipient defenses apply once to transferred branch.
8. Each branch then receives temp HP/life resolution independently.
9. Neither transferred branch can itself be redirected.

Original-target flat DR therefore **does not** reduce the amount from which Bloodbond/Veinlock chooses its share.

Multiple owners may not duplicate the same packet. **NEW root rule:** one original damage branch accepts at most one sharing/redirection operation unless the chosen source itself splits that operation among multiple recipients, as Burden Shared does. Mandatory/automatic redirects are resolved before optional offers; if multiple mandatory effects compete, the original target chooses one legal operation.

---

# 3. Post-defense transfers and temp HP

Use the original target's `postDefenseDamage` after its defense stage and after any pure prevention that legally applies before transfer, but before temp HP.

A transferred branch marked “cannot be reduced,” “unmitigated,” or “no further mitigation” skips a second defense stage.

It **does not bypass recipient temp HP** unless the source expressly says it bypasses temp HP/normal HP directly.

Likewise:

- 1-HP floors remain legal if their source applies;
- Ritual Ward remains legal against an otherwise eligible death;
- Wounds/Instant Death use the transferred packet normally;
- Aegis saying the transfer still occurs even if it would kill the Warrior outright does **not** make the resulting death unpreventable.

Direct HP costs are different and continue to bypass temp HP entirely.

---

# 4. Hit/save/critical riders after transfer

**NEW common transfer rule:**

A damage transfer does **not** transfer attack identity.

The transfer recipient:

- was not hit by the original attack;
- did not fail the original save;
- was not critically hit;
- receives no attached poison/control/on-hit rider merely because damage moved to it.

The original target remains the original attack/save target.

Therefore:

- an **on-hit** rider remains attached to the original target even if all damage is transferred;
- a rider requiring the original target to **take/deal positive damage** must recheck its exact predicate after transfer;
- the transfer recipient gets only the damage type/amount plus ordinary consequences of receiving damage.

A transferred packet caused by a critical attack does **not** give a 0-HP recipient two death failures. It causes the ordinary one failure for positive damage at 0 unless that recipient itself was actually critically hit by some separate rule.

Concentration is different: the recipient is receiving a genuine damage packet. Use its received `resolvedDamage` for the ordinary concentration procedure even if its temp HP later absorbs the whole packet.

Guardian Pulse is the exception because it changes the **attack target itself**. The Guardian becomes the hit/miss/on-hit target.

---

# 5. Root damage totals after splitting

Track a `rootDamageEventId`.

After all transfer branches finish, the source's numeric total is:

> sum each final recipient branch's `actualDamageDealt` **once**.

Never count the unsplit parent plus its children.

This preserves anti-overkill and temp-HP accounting.

However, transfer branches carry source flags such as:

- `noResourceGeneration`
- `noRetaliation`
- `noHealingGeneration`
- `noRecoveryTrigger`

Those flags suppress the corresponding downstream consumer on that branch.

Thus a Paladin-transferred branch may still contribute to the root's physical accounting while remaining ineligible to manufacture a resource/retaliation/heal trigger where the transfer source expressly prohibits it.

Per-target, per-turn and per-round caps still apply normally.

Blocked/capped healing **never refunds or restores** a redirection/healing entitlement that was already legally consumed.

---

# 6. Paladin shared limits / Final Stand

Preserve `paladin.engine[10]` and `[14]` as the explicit integration ceiling:

- one Paladin redirection event per numbered round;
- exactly one Paladin redirection feature may modify a given damage event;
- Crown Undying expressly permits two **different ally-damage events** per round;
- Crown Undying total redirected damage is still capped at `Paladin level + M` for that round;
- never two transfers from the same event.

### Final Stand

I would **not invent another exception**.

`paladin.supplement.oath-of-the-chain.final-stand` remains active until source-next-start and is eligible against every damage event during that duration, but `paladin.engine[10]` means it can actually redirect **one event per numbered round**.

After it redirects one event, subsequent damage to that ally in the same numbered round resolves normally. On the next numbered round, Final Stand can redirect again if still active.

This preserves both historical texts while treating engine[10]'s explicit “unless Crown Undying” language as the operational override.

It requires no Reaction, but it still spends the shared redirection event allowance.

---

# 7. Exact transfer amounts

### Protective Stance
After original defenses:

`redirect = min(S+M, postDefenseDamage)`

Ally damage is reduced by that exact amount. Paladin receives exactly that amount as unmitigated transferred damage.

It cannot harm the Paladin for nonexistent excess damage.

### Shared Breath / Veinlock
Chosen amount is always capped to the available source packet.

### Guardian Tissue
After original defenses:

`redirect = floor(postDefenseDamage / 3)`

Original ally retains the remainder.

### Aegis Incarnate
After original defenses/resistance, before temp HP:

`redirect = floor(postDefenseDamage / 2)`

Ally retains the remainder.

### Redirecting Palm
After the Monk's ordinary defenses, before temp HP:

`prevented = floor(postDefenseDamage / 2)`  
`retained = postDefenseDamage - prevented`

The new force counter is:

`min(prevented, Monk level)`

That force damage is a **new, separately defendable damage event**, not a transfer. It inherits no attack/critical/rider identity from the original melee hit.

---

# 8. Bloom Ward

Treat `10 + Oracle level` as a **finite prevention pool across packets**, not a single-packet cap.

On placement:

`remainingBloom = 10 + Oracle level`

For each eligible packet after ordinary defenses and before temp HP:

`absorbed = min(postDefenseDamage, remainingBloom)`

Subtract absorbed amount from the packet and Bloom pool.

Bloom remains until:

- pool reaches 0; or
- its 1-minute duration ends; or
- another legal effect actually ends/removes it.

Suppression does not count as ending.

Whenever the valid Bloom record actually ends, its printed +1 Frightened-save rider begins until target-next-end.

Prevented Bloom damage creates no secondary damage/resource event.

---

# 9. Direct HP loss remains outside this system

These are not damage transfers and do not enter the damage pipeline:

- `cleric.hero.cultist.blood-sacrifice`
- `mage.hero.lich.resonance-to-flesh` Flesh→RP
- `paladin.supplement.oathbreaker-shared.profane-exchange`
- `paladin.supplement.oath-of-mercy.channel-life` donor HP cost

They:

- spend normal HP directly;
- bypass temp HP;
- cannot be reduced/redirected;
- do not create Wounds/damage triggers merely from the payment;
- obey their own floor/legality requirement.

Cosmic Equilibrium and Bones Mastery healing redirection are likewise **not damage transfer**.

---

# Classification of all 39 exact sources

| Exact source ID | Role | Operational disposition |
|---|---|---|
| `cleric.hero.priest.cosmic-equilibrium` | HEALING_REDIRECTION | Redirects genuine excess healing into new radiant damage; reverse conversion creates healing. Existing excess ledger/no-recursion rules apply. |
| `cleric.hero.cultist.blood-sacrifice` | DIRECT_HP_LOSS_EXCLUSION | HP cost; never damage or redirectable. |
| `crimson-agent.engine[4]` | PRE_MITIGATION_TRANSFER_ENGINE | Veinweave sharing splits before mitigation; each recipient defends once; no retransfer. |
| `crimson-agent.engine[5]` | DIRECT_HP_LOSS_EXCLUSION | Sacrifice guard; no damage pipeline. |
| `crimson-agent.hero.bloodweaver.bloodbond` | PRE_MITIGATION_TRANSFER + TEMP_HP_RIDER | Quarter pre-mitigation split; each recipient defends once. Paid actual heal to owner can grant ally temp HP under reviewed healing predicate. |
| `crimson-agent.hero.bloodweaver.veinlock-tether` | PRE_MITIGATION_TRANSFER | Alternative to Bloodbond on same event; chosen amount ≤S+M and available packet. |
| `mage.hero.elementalist.elemental-absorption` | DAMAGE_PREVENTION | Adds resistance during ordinary defense stage; no transfer. |
| `mage.hero.lich.resonance-to-flesh` | DIRECT_HP_LOSS_EXCLUSION / HEAL | Flesh→RP direct HP cost; RP→Flesh ordinary healing. |
| `mirrorsage.arch.mirror-shell` | RETALIATORY_DAMAGE | No redirection. Original spell already missed/saved; new force packet against caster on failed WIS save. |
| `monk.engine[13]` | EXCLUSION | Selection/progression only. |
| `monk.arch.tortoise.redirecting-palm` | DAMAGE_PREVENTION + RETALIATORY_DAMAGE | Prevent half post-defense packet; new force event = min(prevented,L). |
| `monk.hero.enlightened-master.shared-breath` | POST_DEFENSE_TRANSFER + HEALING_ECHO | **NEW phase:** split post-defense/pre-tempHP; recipient gets no second mitigation. Existing causal-heal rules remain. |
| `oracle.engine[14]` | ENGINE_GUARD | Redirected numeric component carries no RC/Prophecy/passive/copy effects unless explicit. |
| `oracle.engine[29]` | ENGINE_GUARD | Redirected damage cannot be reduced again/reflected again/generate RC. |
| `oracle.supplement.bones.bones-revelation-mastery` | HEALING_REDIRECTION | Enhanced Chorus chooses ally as recipient of same heal; not a child/second heal. |
| `oracle.supplement.life.bloom-ward` | DAMAGE_PREVENTION | Finite `(10+L)` prevention pool across packets; no transfer. |
| `oracle.supplement.life.life-linked` | POST_DEFENSE_TRANSFER + HEALING_INTERFACE | Original mitigation once, then transfer up to half; no second mitigation/recovery/retaliation from transfer. |
| `paladin.engine[10]` | POST_DEFENSE_TRANSFER_ENGINE | Original defenses once; one paid Smite/round; one redirection event/round; no second mitigation/resource/retaliation. |
| `paladin.engine[14]` | REDIRECTION_LIMIT_ENGINE | Exactly one Paladin redirection feature/event; Crown Undying two different events exception. |
| `paladin.base.protective-stance` | POST_DEFENSE_TRANSFER | Redirect min(S+M, remaining damage); protector gets unmitigated branch. |
| `paladin.supplement.oathbreaker-shared.profane-exchange` | DIRECT_HP_LOSS_EXCLUSION | Direct HP casting cost; not damage. |
| `paladin.supplement.oath-of-mercy.channel-life` | DIRECT_HP_LOSS_EXCLUSION + HEAL | Donor loss outside damage pipeline; recipient ordinary healing packet. |
| `paladin.supplement.oath-of-the-chain.chainbound-smite` | POST_DEFENSE_TRANSFER | Later bond redirect capped by actual CHA/min3 and available post-defense damage; shared Paladin allowance. |
| `paladin.supplement.oath-of-the-chain.aura-of-bonds` | DAMAGE_PREVENTION | Flat class reduction, no transfer; participates in ordinary defense stage. |
| `paladin.supplement.oath-of-the-chain.linked-ward` | POST_DEFENSE_TRANSFER + TEMP_HP_RIDER | Redirect capped amount; if transfer reduces Paladin to0, ally gains temp HP from Paladin branch's actualDamageDealt, capped L+M. |
| `paladin.supplement.oath-of-the-chain.martyr-s-share` | POST_DEFENSE_TRANSFER | Redirect floor(postDefenseDamage/2), ally retains remainder; hit riders remain original target. |
| `paladin.supplement.oath-of-the-chain.final-stand` | POST_DEFENSE_TRANSFER | Transfers full remaining post-defense packet but constrained to one Paladin redirection event/numbered round. |
| `paladin.supplement.oath-of-the-chain.unbroken-covenant` | TEMP_HP_RIDER + REDIRECTION_MODIFIER | Does not create redirect; when one occurs, ally temp HP = floor(Paladin transfer branch actualDamageDealt/2), cap S+M. |
| `paladin.supplement.oath-of-the-martyr-king.king-s-smite` | POST_DEFENSE_TRANSFER + TEMP_HP | Smite temp HP uses root Smite actualDamageDealt; separate once/round post-defense redirect ≤5. |
| `paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown` | POST_DEFENSE_TRANSFER | Reaction after target defense; redirect ≤M; shared allowance. |
| `paladin.supplement.oath-of-the-martyr-king.crown-of-embers` | DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER | S prevention first; then at most one eligible Crown redirect from remaining packet, shared allowance. |
| `paladin.supplement.oath-of-the-martyr-king.burden-shared` | POST_DEFENSE_MULTI_TRANSFER | One redirection operation can split ≤L+M among up to two willing recipients; no second mitigation/redirect/reflection/heal/resource. |
| `paladin.supplement.oath-of-the-martyr-king.crown-undying` | DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER + HEAL | Two different ally events/round, L+M transferred total. Heal each protected ally from half Paladin branch actualDamageDealt, cap S+M; blocked/capped heal never refunds entitlement. |
| `shaman.arch.ancestral-guardian` | DAMAGE_PREVENTION | Prevent min(Sd8+M, available damage); no transfer/corpse/refund. |
| `soldier.hero.champion.selfless-guardian` | POST_DEFENSE_TRANSFER | Ally mitigates first; redirect ≤S+M from remainder; self gets no second mitigation/retaliation. |
| `tinker.arch.emergency-protocols` | POST_DEFENSE_TRANSFER + COMPANION_DEVICE | **NEW phase:** after user's defenses, before tempHP; redirect min(S+M,remaining) to drone unmitigated. |
| `warrior.hero.wardborn.guardian-tissue` | POST_DEFENSE_TRANSFER | Redirect floor(postDefenseDamage/3); no second mitigation/BT/retransfer. |
| `warrior.hero.wardborn.aegis-incarnate` | AUTOMATIC_POST_DEFENSE_TRANSFER | Automatic half after original defenses/resistance, before tempHP; no second mitigation/BT/retransfer. Survival effects still legal. |
| `warrior.hero.wardborn.guardian-pulse` | ATTACK_RETARGET + COUNTERATTACK | Retarget attack before AC resolution; Guardian becomes actual attack target. One original attack roll only. Counterattack afterward is a separate attack root whether original attack hit or missed. |

---

# Adversarial reference cases

1. **Bloodbond:** raw fire packet40; redirect10 before mitigation. Ally fire resistance halves retained30→15; Agent resistance halves10→5. Total branches20, not “ally resistance first then transfer5.”
2. **Post-defense transfer:** raw30, original flat DR5 then resistance½ →12. Redirect5: ally gets7 before tempHP; protector receives5 with no second mitigation.
3. Protector has5 temp HP and receives5 “unmitigated” transfer → temp HP absorbs5; `actualDamageDealt=5`, normal HP unchanged.
4. Original critical hit is fully transferred. Original target remains the hit/on-hit rider target; recipient at0 receives one ordinary damage failure, not two critical-hit failures.
5. Protective Stance sees only3 post-defense damage with S+M=8 → redirects3, never inflicts8 on Paladin.
6. Redirecting Palm receives post-defense9 → prevents4, retains5; force counter=min(4,L), new target applies own defenses.
7. Bloom capacity15: packet6 → pool9; later packet12 → absorbs9, 3 continues to tempHP, Bloom ends and save rider starts.
8. Crown Undying Paladin branch has4 temp absorption +2 real HP lost due floor → actualDamageDealt6; ally heal base=floor(6/2)=3, not based on original pre-transfer amount. If healing is blocked, event entitlement remains spent.
9. Final Stand receives two ally damage events in same numbered round → first/chosen event redirects; second cannot. A later numbered round can redirect again if duration remains.
10. Aegis transfer would meet Instant Death on Warrior → transfer still occurs; eligible Ritual Ward may replace the death because Aegis does not state death is unpreventable.
11. Burden Shared divides8 of12 post-defense damage among two willing allies 3+5; original retains4. This is one transfer operation, not two redirection events.
12. Guardian Pulse retargets before AC: attack that would hit ally AC14 but misses Guardian AC19 is a miss; Guardian still gets its printed counterattack if attacker is in reach.

---

# Remaining implementation dependencies

This packet is sufficient to build the **bounded redirection helper**, but I would keep four items explicitly open until its exact implementation review:

1. **Global defense-stage ordering.** The overlay should encode flat class DR → resistance/immunity → finite/reactive pure prevention → redirection → temp HP. Verify this against any unsupplied item/spell prevention sources before making it game-wide.
2. **Root attribution flags.** Implement branch provenance (`rootDamageEventId`, transfer operation, noResource/noHealing/noRetaliation/noReflection flags) and

[CAPTURE TRUNCATED — continuation requested separately.]

