# Remaining-source corrections and complete classification tail

Retrieved through the official Codex app read_thread connector from the completed Calibration Review conversation. This reply corrects three source misreadings in the prior proposal and supplies all67 remaining classification rows. The prior first64 rows remain in the explicitly partial capture; both together cover131 sources.

## Three source corrections

### 1. `oracle.supplement.flame.zealot-s-renewal`

Your reading is correct. My earlier HP-floor interpretation was wrong.

The source says the ally heals, **then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it**. That establishes a minimum **resolved backlash damage**, not a minimum surviving HP value. :chatgpt-content-reference{index="0"}

Operationally:

1. Resolve the healing attempt.
2. Unless an expressly authorized source such as First Flame Convergence/Flame Prophecy suppresses the backlash component, generate a separate `1d4 fire` damage packet.
3. Apply ordinary fire defenses.
4. After those defenses, enforce **minimum resolved backlash damage = 1**.
5. Then resolve temp HP, normal HP loss, Wounds, zero HP and death normally.

So fire immunity by itself does **not** reduce this backlash to 0. The source's explicit “cannot be reduced below 1” overrides ordinary reduction/immunity for this particular backlash. No NEW exception is required.

It may reduce the healed ally to 0 HP and can trigger the normal Wound/death procedure.

This is **not** a 1-HP survival floor.

---

### 2. `oracle.supplement.flame.crown-s-burn`

Correct. Use the frozen shared-roll baseline, not independent cap rolls.

Crown's Burn is one burst, so:

1. Resolve each enemy's fire packet separately.
2. Sum qualifying hostile `actualDamageDealt`.
3. Select 0–3 legal allied recipients.
4. If zero recipients are selected, skip the healing calculation entirely.
5. `share = floor(totalActualFireDamage / recipientCount)`.
6. Roll **one shared `S d6 + M` healing-cap roll** for the burst.
7. For each selected ally:
   `baseHeal = min(share, sharedCapRoll)`.
8. If `totalActualFireDamage > 0`, apply the printed minimum 1 to that ally's source amount.
9. Each ally then runs its own ordinary healing reductions/caps/prohibitions.

Thus:

`sourceHeal = max(1, min(share, sharedCapRoll))`

only when numeric qualifying actual fire damage is positive.

A merely positive fire packet with `actualDamageDealt = 0` does not activate the minimum-1 healing clause. :chatgpt-content-reference{index="1"}

This also preserves shared-roll provenance for per-die effects.

---

### 3. `mirrorsage.arch.dual-echo-cast`

Correct. Remove my imported “at most one healing profile” restriction.

That limit belongs to **Echo Fusion**, not Dual Echo Cast. Dual Echo Cast instead requires two records captured from different creatures and resolves each at half its own profile's rolled amount as one combined release. :chatgpt-content-reference{index="2"}

Therefore two distinct paid Mend records are legal if:

- captured from different creatures;
- both records are otherwise legal;
- both RP costs are paid;
- both records are consumed;
- combined-release/action limits are respected.

Each component is halved and rounded once independently.

If both heal the same creature, ordinary same-target/same-effect healing handling resolves them as the two actual components supplied by this feature; do not delete the second merely because both are Mend unless another rule specifically makes those healing applications mutually exclusive.

No copied resources, recursive copies or extra release are created.

---

# Classification tail only

| Exact source ID | Role | Short disposition |
|---|---|---|
| `oracle.supplement.flame.flame-prophecy` | HEALING_INTERFACE + RESOURCE_ONLY | Free chosen Flame Revelation; suppresses one eligible backlash; otherwise no healing packet of its own. |
| `oracle.supplement.flame.crown-restored` | HEALING_INTERFACE | 1/LR Final; printed target-start healing pulses included without generic RC upkeep. |
| `oracle.supplement.life.resonant-seed` | HEALING_INTERFACE + MOVEMENT_CONTROL_ONLY | Target-start healing zone; asynchronous upkeep scheduler still provisional. |
| `oracle.supplement.life.life-revelation-mastery` | HEALING_INTERFACE + CONDITION_CURE | Modifier only: Overflowing/Garden/Song upgrades; no independent heal. |
| `oracle.supplement.stars.radiant-path` | HEALING_INTERFACE + MOVEMENT_CONTROL_ONLY | Shared 1d6 ally heal only if meaningful hostile takes qualifying damage; movement separate. |
| `paladin.engine[1]` | EXCLUSION | Progression/access only. |
| `paladin.engine[2]` | EXCLUSION | Fighting style, disease-save and Extra Attack reconciliation only. |
| `paladin.engine[3]` | RESOURCE_ONLY | Smite own-turn restriction; also obey narrower engine[10] one-paid-Smite/round cap. |
| `paladin.engine[6]` | RESOURCE_ONLY | Smite/Aura/LoH Dissonance interface. |
| `paladin.engine[7]` | RESOURCE_ONLY + OTHER_NAMED_DEPENDENCY | Oath/Oathbreaker transition; LoH pool persists through switch. |
| `paladin.engine[8]` | RESOURCE_ONLY | Death Touch spends LoH points as damage; not healing. |
| `paladin.engine[10]` | OTHER_NAMED_DEPENDENCY | Shared Smite/redirection limits; dedicated redirection procedure still open. |
| `paladin.engine[13]` | HEALING_INTERFACE | **Operational correction:** level-17 Wave = 1/long rest; preserve conflicting 1/SR historical card text. |
| `paladin.engine[14]` | OTHER_NAMED_DEPENDENCY | Redirection selection/event cap; Crown Undying exception. |
| `paladin.supplement.oathbreaker-shared.blighted-benediction` | EXCLUSION | Damage/debuff only. |
| `paladin.supplement.oathbreaker-shared.dread-shelter` | TEMP_HP | One temp-HP grant plus DR; no recurring healing. |
| `paladin.supplement.oathbreaker-shared.black-manifestation` | TEMP_HP + RESOURCE_ONLY | Temp HP plus Signature-use refresh. |
| `paladin.supplement.oathbreaker-oath-of-mercy.death-touch-life-drain` | HEALING_INTERFACE + RESOURCE_ONLY | Drain heal uses secondary targets' total numeric actual necrotic damage; primary LoH-point damage does not feed heal. |
| `paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate` | HEALING_INTERFACE | Heal from half summed qualifying `actualDamageDealt`, source cap applies. |
| `paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution` | EXCLUSION | Damage rider only; no auto-execution. |
| `paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood` | EXCLUSION | Damage + temporary terrain rider only. |
| `paladin.supplement.oath-of-the-ancients.thorn-crown` | OTHER_NAMED_DEPENDENCY | Condition reflection, not healing/cure. |
| `paladin.supplement.oath-of-the-chain.chain-of-duty` | MOVEMENT_CONTROL_ONLY | Triggered teleport only; prevents/heals no damage. |
| `paladin.supplement.oath-of-grief.memorial-flame` | OTHER_NAMED_DEPENDENCY | Death-save bonus + undead detection/attack penalty. |
| `paladin.supplement.oath-of-the-martyr-king.crown-of-embers` | OTHER_NAMED_DEPENDENCY | Damage reduction/redirection; no healing itself. |
| `paladin.supplement.oath-of-the-martyr-king.burden-shared` | OTHER_NAMED_DEPENDENCY | Post-defense damage division; belongs in redirection packet. |
| `ranger.engine[5]` | TEMP_HP | Warder Arrow grants finite temp HP; remaining Arrow modes nonhealing. |
| `ranger.hero.warder.healing-briar` | HEALING_INTERFACE | Initial Action pulse included; next two require BA+1 RP. |
| `ranger.hero.warder.beast-companion` | COMPANION_DEVICE | Living companion; ordinary healing allowed, death/injury lifecycle still dependency. |
| `shaman.engine[2]` | RESOURCE_ONLY | Totem movement competes with healing upkeep/commands. |
| `shaman.engine[3]` | RESOURCE_ONLY | Finite prepared-flask inventory and carry cap. |
| `shaman.engine[4]` | HEALING_INTERFACE + CONDITION_CURE + RESOURCE_ONLY | Advanced Heal/Restore consume flask + 2 RP. |
| `shaman.arch.extended-totem-duration` | HEALING_INTERFACE | Fourth Renewal pulse requires genuine BA+1 RP; no fifth. |
| `shaman.arch.spirit-cache` | HEALING_INTERFACE + RESOURCE_ONLY | Replay pays normal activation plus new flask/full totem cost; +1d6 is real added die. |
| `shaman.arch.totem-pulse` | TEMP_HP | Non-Renewal placement only; cannot produce immediate Renewal heal. |
| `shaman.arch.spirit-saturation` | RESOURCE_ONLY | Free placement limited to non-Renewal totem. |
| `shaman.hero.theurgist.echo-totem` | HEALING_INTERFACE | Shares parent concentration/upkeep; half numeric healing; same-name overlap cannot double-heal. |
| `shaman.hero.theurgist.elemental-harmony` | COMPANION_DEVICE | Adds max/current HP on summon creation; not healing damaged summon. |
| `shaman.hero.theurgist.summon-cinderflame` | COMPANION_DEVICE | Summon/destruction interface only. |
| `shaman.hero.soothsayer.healing-splash` | HEALING_INTERFACE + RESOURCE_ONLY | Shared-roll heal; flask and 3 RP consumed. |
| `shaman.supplement.elder-spirit-accord-new-hero-capstone` | HEALING_INTERFACE + RESOURCE_ONLY | Cost reduction plus +M to one healing/damage roll; no extra use/pulse. |
| `soldier.engine[4]` | EXCLUSION | Progression and anti-infinite-healing guard only. |
| `soldier.hero.artillerist.precision-engineering` | COMPANION_DEVICE | Increases maximum/initial construct HP; never repairs existing damage. |
| `soldier.hero.tyrant.brutal-example` | EXCLUSION | Damage/fear only. |
| `thief.engine[2]` | OTHER_NAMED_DEPENDENCY | Poison/Bleed engine; Bleed does not generically block healing. |
| `thief.engine[3]` | HEALING_INTERFACE + OTHER_NAMED_DEPENDENCY | Bloodleech critical heal; Ashblood critical healing prohibition; remaining poison riders nonhealing. |
| `tinker.engine[2]` | COMPANION_DEVICE | Destroyed-drone reconstruction distinct from functional repair. |
| `tinker.engine[7]` | COMPANION_DEVICE | Device duration/repair/Dissonance-routing; healing pulse caps preserved. |
| `tinker.base.quick-fingers` | EXCLUSION | Explicitly cannot activate healing devices. |
| `tinker.arch.deployable-expertise` | COMPANION_DEVICE | Max/initial deployable HP only; no repair. |
| `tinker.hero.artificer.protective-programming` | TEMP_HP + COMPANION_DEVICE | Pre-hit temp HP; not healing. |
| `tinker.hero.artificer.efficient-power-cells` | EXCLUSION | Nonhealing device-duration extension only. |
| `tinker.hero.artificer.nano-aegis-drone` | HEALING_INTERFACE + TEMP_HP + COMPANION_DEVICE | Paid commanded organic heal or temp HP; max three pulses. |
| `tinker.hero.artificer.restoration-field` | HEALING_INTERFACE + COMPANION_DEVICE | Initial heal/repair pulse included; later paid maintenance; device repair does not trigger organic-healing hooks. |
| `tinker.hero.techsmith.technical-mastery` | EXCLUSION | Damage modifier only. |
| `tinker.hero.techsmith.reconfiguration` | EXCLUSION | Nonhealing profile changes only. |
| `tinker.hero.warmachine.scrap-reaper` | COMPANION_DEVICE | Temporary Scrapling creation from eligible destroyed device; no recursive death chain. |
| `tinker.supplement.mech-overdrive` | COMPANION_DEVICE | Extends device duration only; healing pulse count unchanged. |
| `warrior.engine[15]` | HEALING_INTERFACE | General Warrior healing/regeneration guard. |
| `warrior.arch.mutation-overload` | HEALING_INTERFACE | +1d4 to one mutation healing roll = real added die, same packet. |
| `warrior.hero.dreadspawn.pain-empowerment` | OTHER_NAMED_DEPENDENCY | Continuous missing-HP percentage state; no healing. |
| `warrior.supplement.primed` | HEALING_INTERFACE | +1 to one mutation-generated healing roll, same packet. |
| `warrior.supplement.transcendent` | EXCLUSION | Explicitly grants no immediate healing. |
| `warrior.supplement.sanguine-surge` | HEALING_INTERFACE + RESOURCE_ONLY | Finite serum-dose heal; separate from Mutation Recovery Reserve; ending Strain remains separate. |
| `wizard.engine[10]` | TEMP_HP + COMPANION_DEVICE | Abjuration/Necromancy temp HP; Conjuration summon HP granted at creation, not healing. |
| `wizard.engine[15]` | HEALING_INTERFACE | Component Enhancement adds one real primary healing die for +1 RP; same cast/event. |
| `wizard.hero.spellbinder.arcane-sanctuary` | EXCLUSION | Allows ordinary healing but grants none; belongs to environment/planar rules. |

These are the requested remaining rows only. The corresponding exact source block runs from Flame Prophecy through Arcane Sanctuary. :chatgpt-content-reference{index="3"} :chatgpt-content-reference{index="4"} :chatgpt-content-reference{index="5"} :chatgpt-content-reference{index="6"}

## Recommended next dependencies

**1. Damage redirection/sharing — next.** Your prepared 39-source packet is the correct next pass. It needs to settle pre-mitigation vs post-defense splits, recipient temp HP, HP floors, Wounds, concentration, original-hit riders, retaliation/procs, and Final Stand/shared one-event-per-round exceptions. Do not reuse `actualDamageDealt` as a pre-redirection quantity.

**2. Maximum-HP/stat composition.** After redirection, reconcile Monk max-HP reductions with Flesh Warden, Exhaustion 4, Expedition 4 and other max-HP effects. Establish addition/reduction/multiplier order, min1, current-HP clamp and threshold-trigger behavior.

**3. Sustained zone/pulse scheduler.** Encode activation pulse, later source-turn pulse, asynchronous target-start pulse, entry pulse and maintenance windows. Include Resonant Seed, Garden, Eternal Bloom, Unfinished Chorus, Crown Restored, Lifewell, Healing Briar, Renewal/Echo Totem and Restoration Field. The pulse-window decisions above remain proposals until that review.

**4. Companion/device/temp-HP lifecycle.** Set shared distinctions among living-companion healing, device repair, destroyed reconstruction, max/initial HP changes, finite temp-HP reserves and nonstacking. Druid Buffer Reserve needs exact form-card evidence here.

**5. Roll/copy provenance.** Formalize `rollInstanceId`, real dice vs copied flat numeric amounts, shared rolls, per-die modifiers and no-proc flags. The Crown's Burn and Dual Echo corrections above should become regression cases.

Additional source evidence still most useful after the redirection packet: all non-Monk maximum-HP modifiers, actual Druid form temp-HP cards, Predictive Alchemy's exact flask-refund text, and the common living-companion death/injury/healing procedure.
