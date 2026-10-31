# Creature companions: life, commands and identity

**REVIEWED / reference-VALIDATED: 121 targeted checks and 2,800 Ranger conversion states.** This overlay discusses 100 exact passages from Druid, Mage, Mirrorsage, Ranger and Wizard, supported by five frozen common paragraphs. It closes no full class, form, temporary-HP system or complete runtime by itself. [Source register](CREATURE_LIFECYCLE_SOURCE_BINDINGS.md), [source integrity](CREATURE_LIFECYCLE_SOURCE_VALIDATION.json), [behavior checks](CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json).

The original class cards and frozen class guide remain intact. The notebook's first classification, boundary reconciliation and event-model decisions are preserved in the audit folder. Where the historical first reply differs from the later boundary replies, the later explicit resolution controls. In particular, Auto-Raise is automatic, its new minion cannot act at all in the creation round, and Mirrorsage Charm was not in the older 219-source control closure.

## At the table

Keep one companion command and one offensive companion allowance per owner per numbered round, including multiclass companions and devices. A normal command costs your Bonus Action. A damaging companion action, or Mage/Wizard control action, spends the offensive allowance. A pure support command spends only the command. The earlier device ledger's internal field named `damage` now represents this shared offensive allowance; its public behavior remains compatible with existing device checks.

Issue ordinary commands during your regular turn. The selected companion moves and performs its command immediately after your whole turn, in an attached phase. It receives no extra independent turn. If it or its target becomes ineligible before execution, the command fails without refund. Your later incapacity or removal alone does not cancel an issued command; actual concentration/source ending can. Uncommanded companions can move defensively and Dodge, subject to their conditions; this grants no generic Reaction or autonomous attack/control.

Use the owner's original regular companion markers for recharge and previous/next-turn references. Extra turns, initiative changes and removal do not restart those markers. The attached phase's event-resolution checkpoint is distinct: it refreshes no Reaction, recharge, Action, death save or regular duration clock.

## Different kinds of creature life

| Creature | HP and 0 HP | Return and identity |
|---|---|---|
| Finite standard summons, Druid swarms, Mage Familiar, Mirror Beasts | HP-only bounded layer; at 0 disappear/end | No corpse, resource or free resummon; a new summon pays its actual source costs |
| Ranger Beast | HP-only; **NEW** immediate death at 0, no Wound checks, Stable or death saves | Actual animal and ordinary surviving corpse; death ends bond. No automatic resurrection or rebond |
| Mage Lich elite | Destroyed bound asset at 0; no usable corpse/resources | Same unique asset remains owned. Soulbound or actual completed LR can return it |
| Wizard standard undead | Destroyed at 0; consumed body never returns as new fuel | Ends on destruction, dismissal or owner's next completed LR, including Auto-Raised minions |
| Wizard elite | Supplied profile/cap only in this package | Binding/acquisition and return procedure are still missing; no create/bind/return API |
| Reflective Companion | Original creature's HP and life rules | Temporary control relation; no copied body, reset, new statistics or duplicate turn |
| Druid form | Same character's HP/life rules | Full forms and Buffer Reserve remain a separate open interface |

Companion healing restores legal normal HP only. It does not reset identity, duration, recharge, actions, source uses, effects or command budgets. Ranger's “heal normally” supplies no Hit Dice pool or automatic rest healing. The HP-only layer is specific to this reviewed companion chassis, not generic law for all animals/NPCs. Existing animal conditions, disease, poison, explicit injuries and timed effects survive bonding.

## Stats and ownership

**NEW:** finite created creatures snapshot base HP and AC at creation. Attacks, saves, class DC and S use the current values of the original source owner at resolution. Keep source owner, current controller, source class and creation source separate. A temporary controller does not donate their class levels, PB or attack bonus. The implementation rejects stats belonging to another owner/class; it provides no unrestricted transfer/rebinding operation.

Standard profile: AC 12 + floor(PB/2), HP 2L, Speed 30, owner PB for saves, one class attack for S d6 with printed melee/ranged mode. Druid swarm uses current PB+WIS, piercing and its printed tiny-gap movement. Familiar snapshots AC 12+PB and HP 5+Mage level+M; its current source-owner Mage attack fires a 30-foot Elemental Dart for S d4. Focus is fixed at creation: Lightning adds Fly30, Fire/Cold their matching resistance. Changing Focus neither morphs nor refills it. One Familiar; replacement ends the prior one.

Ranger maximum is **NEW dynamic** max(1, 2×current Ranger level + actual WIS modifier), not M. Current PB updates its standard AC/saves/attack. Persistent Mage elite maxima use current source-owner Mage level; fixed AC stays fixed. Capacity growth never heals; shrink clamps HP without damage. Wizard elite profiles use the same names with their own original Wizard source statistics if a future legitimate binding source establishes them.

The [reviewed maximum-HP ledger](MAXIMUM_HP_PLAYTEST.md) supplies source-qualified modifiers. Conjuration is the original creating Wizard level snapshot and requires actual Wizard spell creation. Corpse Harvest qualifies only with actual access; Auto-Raise is not a spell and grants no new Conjuration snapshot. Flesh Ascendant is the explicit dynamic eligible-current-controller exception; engine and card are one effect, not two bonuses. Creation starts at full final legal maximum unless the actual source enters damaged; later added capacity never fills HP. Callers update dynamic modifier records from their real sources.

## Ranger's persistent bond

Use the printed one-hour ritual, touch, 4 RP and one long-rest use. The animal must already be willing/tamed, noncorrupted, INT below7 and CR no greater than Ranger level. The helper does not invent finding/taming rules. Keep one chosen movement mode, capped40 feet, and the original keen-sense identity; no monster stat block, boss powers or free special actions. Exact keen-sense selection definitions remain an evidence gap.

**NEW initial conversion:** for a living animal, new HP = max(1, floor(new maximum × old current HP / old maximum)). A wounded animal stays proportionally wounded. This is profile conversion, not healing or damage. A living bound Beast cannot be rebonded to refill HP. On death, ordinary legal resurrection may restore the same animal under its own source, but it remains unbonded. A new full ritual also requires an actual completed long rest after bond death.

Physical body identity is separate from current corpse eligibility. Keep one record whose state is living, corpse, consumed or removed. Accepting an already-resolved, independently legal resurrection immediately marks that same body living and unavailable as a corpse, before any rebond. Corpse Gateway cannot use it while living. A later genuine death with a surviving body makes that same record a corpse again; no fragment/new body identity is generated. A consumed/removed body requires explicit reconstruction by the actual resurrection source before it can return. The notification helper grants no resurrection ability, payment exemption or automatic bond. Rebond uses the actual post-resurrection HP ratio and preserves death history; it cannot claim a healthier ratio. Full global corpse decay/cleanup remains open.

## Mage Lich assets and elite commands

An actual successful Lich transformation unlocks Boneflayer, Dreadblade and Wraithbound. Readiness and informed retirement-risk consent are source guards; this lifecycle helper does not perform that irreversible ritual. **NEW shared identity:** across Mage/Wizard, one owner can have at most one of each named elite and three total. Destroyed assets still occupy those identities. Any future external Wizard binding must validate against the same asset register; the current helper offers only its profile schema.

| Elite | Profile | Source-native actions/riders |
|---|---|---|
| Boneflayer | AC14, HP12+2L, Speed30; ranged60, 2d6+S necrotic | Fear Pulse replaces attack, enemies10 feet WIS or Frightened through target-next-end, recharge3. Grave Miasma replaces attack: radius10 point30 until next owner-start, enemies entry/start1d6 once, recharge3 |
| Dreadblade | AC16, HP16+3L, Speed30; melee5, 1d8+S necrotic | Concentrating hit target immediately saves with disadvantage; natural20 applies printed −1 attack Weakened until target-next-end. Advantage against forced movement |
| Wraithbound | AC14, HP10+2L, Fly40/hover; melee5, 1d8+S necrotic | Natural20 CON or Stunned until target-next-end under shared character→target hard-denial guard |

Rolls, chosen enemy geometry, recharge payments, exact condition applications and canonical hard-guard sharing remain caller/source responsibilities. This helper returns attack profiles and bounded lifecycle/command transitions; it does not silently execute every on-hit effect.

**NEW Miasma integration:** creation spends one offensive command. Its native finite entry/start damage needs no second command and does not spend next round's offense. Retain no-resource/no-recursion flags. An old zone tick is not a new companion turn or attack.

Wraithbound loses source invisibility on attack **or control**. It can regain it at the end of its next original regular companion marker if the predicate remains satisfied. A current-marker end cannot immediately restore it. The actual offense event must notify its marker state. Core Invisible still does not grant unknown location, sight through walls or automatic target legality.

Soulbound requires the destroyed own bound elite within30 or its inert token, legal empty space30, Action, 5 RP and one LR use. Return the same asset/instance at **NEW source-specific** max(1, floor(current maximum/2)), plus S+M temp HP for60 seconds under normal temp-HP rules. Do not copy machine reconstruction permissions. Preserve spent uses, recharge clocks, command history and still-applicable effects. Completed LR returns those same Mage assets at full current HP unless an actual campaign consequence prevents it. Rest-use/recharge resets come only from the canonical rest system; a return itself grants none. Natural effect expiries must still be processed.

## Wizard corpses, standard minions and Auto-Raise

Corpse Harvest costs Action+4 RP, recharge2, legal corpse/space30. Humanoids qualify; actual Infernal Pact also permits Fiends. Skeleton: AC14, HP6+2WizardL, Speed30, ranged30 1d6+S necrotic. Zombie: AC12, HP10+3L, Speed20, melee5 1d8+S. Goblin Thrall: AC13, HP8+2L, Speed30, melee5 1d6+S; requires a goblinoid body even with Pact.

All standard minions and reserved Auto-Raise slots share a cap of3. Manually dismiss an existing standard minion before attempting a fourth; failed creation spends nothing and does not consume the body. Harvest consumes the original body. Summoned, raised, copied, illusory or fragmented remains provide no new corpse fuel. Corpse Gateway uses a legal body without consuming it; it does not grant raising permission. Global corpse decay/removal rules remain open.

Ghoul Lash uses the shared BA command and2 RP with another controlled undead within5 at issuance. Its chosen standard minion makes **two independently rolled normal attacks**, not numerical damage copies. Each can miss/hit/crit. This remains one command and one offensive allowance, with at most one Auto-Raise opportunity.

**NEW queue integration, preserving the printed automatic trigger:** the first qualifying personal killing blow by a standard minion automatically reserves the body, one capacity slot and the killer's mechanical minion type. It spends the owner's round opportunity immediately. Ineligible kills do not spend it; a qualifying trigger cannot voluntarily be declined. Body reservation does not prevent another legal consumer from taking the body first. A destroyed/expired killer does not cancel an already-created reservation.

Resolve after immediate death responses and already-due end damage/saves, before ordinary expiry cleanup, in stable application order. An ordinary attached attack has its own `attachedCompanionEnd` queue checkpoint after its consequences, in the same numbered round. That checkpoint is not a second regular turn marker. Kills before the checkpoint closes may reserve. A later administrative kill cannot reopen it, roll forward or leave an orphan queue; its unused opportunity remains unused unless another independently valid trigger occurs before another legally open checkpoint.

At resolution, still-eligible body, legal space and cap permit creation; otherwise release the reservation but retain the spent round use. Auto-Raise costs no Action or RP. The newborn cannot voluntarily move, Dodge, support, attack, control or react in its creation numbered round. Passive defenses/conditions/expiry continue. It ends at destruction, dismissal or next completed owner LR. Owner unconsciousness/death alone does not invent a new ending.

## Mirror Beast, Reflective Companion and Echo origin

One Mirror Beast **or** Reflective Companion slot. Summoning a Beast replaces the old body/control relation administratively; it never kills the real previously controlled target. Mirrorcall adds M max/current HP at creation and5 Speed. Advanced Mirrorcall spends BA once/encounter for appearance plus its printed swim/climb adjustment; Mirror Shift spends BA+1 RP/recharge2 for swim30 or climb30. Neither heals, restores uses, releases Echoes, grants flight/anatomy, or refreshes duration. Corrupted and Shattered on-hit dice/splash retain their exact once-round source qualifiers; full damage-event execution remains in the later copy/trigger work. Luminant Bond supplies only its printed local WIS-save/Invisible advantage interface, with ordinary cover/targeting intact.

Ordinary Beast: Action2 RP, empty space15, one minute, recharge3. Radiant/Shattered: Action4 RP, empty space15, concentration3 of the owner's regular turns, recharge4. Actual scheduler supplies the precise three-turn endpoint. Radiant chooses attack, BA+1 RP heal S d4 to living ally5, or paid Echo origin, once per numbered round. The healing pipeline resolves rolls/modifiers before the lifecycle HP gain; no invented resurrection.

**NEW Mirror-origin exception:** your Echo resolves immediately as your Action during your own turn, including a real extra own turn if real Action, BA and unused shared caps exist. An extra Action alone supplies no BA. Preflight active Beast, actual record, release cap, owner target perception, current Beast range/LOE, Action, BA and RP before any spend. The Beast grants no remote sensory feed or free preceding movement. You own record consumption, Dissonance, Refrain, concentration and spell damage. BA command is spent; offensive companion allowance is not. A later independently legal Gadget Sync may spend it. No second BA command or second local Beast option appears.

Charm Creature remains Action3 RP, one LR use, WIS save, target INT<=6 within30, concentration at most3 rounds, no PC/boss without actual encounter permission. Repeat save at target's actual turn end and when harmed by your side. No suicide, compelled beliefs or permanent allegiance. Original identity/HP/conditions/effects/stat provenance/initiative remain unchanged. A successful save spends cast costs but does not replace an existing Beast. Source-specific save/Charm immunity and permitted target/route checks remain caller responsibilities.

**NEW hard-denial reconciliation:** initial Charm applies the actual Charmed relation and slot without spending hard denial. While active, one BA may queue at most one pending forced ordinary Action, never unique powers; ordinary attack damage capped S d6. Queue to the next future regular target Action: this round if upcoming, next round if already passed. Pay BA in issue round; reserve offensive allowance in the resolution round. The target receives no duplicate attached turn.

At the designated Action slot, revalidate Charm, capability, legal order and the shared character→target→encounter hard guard. Valid execution replaces that Action and spends both hard guard and offense. If Charm ends, target becomes incapable, legality fails or another same-character feature spends hard denial, cancel and release unused offense; retain BA/costs and do not spend an additional hard denial. Call the pending-order revalidation when those facts change, not only at the future turn. Once a forced Action has occurred, this effect permits no further forced attack, Dodge, movement or replacement Action. Actual Charmed restrictions/repeat saves remain; no new fallback is invented.

## Druid summon dependencies

Base Swarm Summoning: Action, one SR use, space30, concentration10 minutes; independent of form. Carrion Rat King: Action, actual Form Surge, once per shift, one standard swarm for at most60 seconds and only while its parent form remains; replacement affects its old form swarm, not independent Base Swarm. Broodmother: on entry actual Form Surge creates two adjacent bodies with one combined commanded attack; end at the earlier of60 seconds or parent form end. Form change ends those children, not unrelated paid summons.

Master of Vermin substitutes the paid summoning spell's profile while preserving its actual count, duration and concentration. No extra casts, creatures or command budget. Its independently paid spell creatures do not inherit a form-ending dependency solely from that substitution. Full forms, reserve arithmetic, per-form special actions and temporary-HP effects remain open.

## Reference boundaries and next work

The helper requires certified source access, legal target/space/range/LOE/perception, ordinary condition capability, real paid Form Surge, canonical action wallets/use scopes, actual concentration/clock endpoints and actual completed rest events. These are explicit inputs, not guessed by creature names. A fresh wallet/ledger per ability is invalid integration. Recharge/frequency keys represent already validated canonical scopes; caller must not mint a new key to bypass them.

Open: Wizard elite binding/return, real Beast natural rest and keen-sense details, global corpse cleanup, broader companion families, full forms/tempHP, complete damage/copy/proc execution, ordinary spell and content catalogs, human balance and complete runtime. Classification of incidental source passages is not closure of their complete effects.

[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md) approves only the selected100+5 source roles and interfaces described here. Incidental full-form/tempHP effects remain deferred.


## Dominate Beast integration

The [reviewed rank-three Enchantment supplement](ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md) adds the source-qualified Dominate Beast bridge for actual Beast companions. It redirects only an existing owner-attached execution opportunity, preserves original profile/source-owner stats, reuses a same-companion/same-phase pending reservation where applicable, and occupies the original owner's structural command/offense caps without charging that owner's Bonus Action. It grants no independent companion turn, duplicate phase or new resource pool. The prior lifecycle text above remains intact; the new bridge is an authored manuscript addition whose stateful runtime integration remains open.
