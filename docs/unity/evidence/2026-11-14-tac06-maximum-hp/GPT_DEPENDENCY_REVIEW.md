# GPT dependency decision

Unity Rules Engine Development reply `b69cefb9-a1f8-4621-b033-8d53c2c60d8b`.

## Decision: **MGT-03 public Short Rest goes first**

**Reviewed packet:** `1381ef717c5719877c8d08e84820760d2a5d6b51`

**I accept the source/dependency finding and select the bounded MGT-03 Short Rest source/API gate before returning to TAC-06 Flesh Warden.** Flesh Warden remains the selected capacity source; another bonus search is not required.

This approves the dependency order and acceptance boundary below. **Engine edits remain gated on the exact Short Rest contract**, because this packet does not yet bind a particular rest site, its access conditions, initial rest history or complete reward disposition.

The approved map gives **MGT-03 direct prerequisites MGT-02 and TAC-05**. TAC-06 retains its mapped **TAC-04, TAC-05 and MGT-02** prerequisites; completed-rest support is an additional **operational prerequisite for this particular Flesh Warden composition**, not a rewrite of TAC-06’s general dependency list.

### 1. Flesh Warden is a valid candidate, but its endpoints need real rest authority

The normalized `warrior.supplement.flesh-warden` record requires **Warrior 1 and Basic Vital**, occupies **one mutation slot**, and operates **while equipped**. Unlike the neighboring active mutations, it does not require serum activation. At the existing Warrior level three, its contribution is **+6 maximum HP**, separate from the established base capacity. Equipping supplies no current HP; removal only clamps current HP if it exceeds the resulting maximum.

The Warrior engine places mutation equipping at a **completed Short or Long Rest**. Portable equipment handling cannot substitute for that procedure. The dependency packet correctly distinguishes the absent public Short Rest/loadout interface from the separately scoped Morale Rest and Strain-recovery procedures.

**For the eventual connected removal witness, select replacement with another explicitly authorized Basic mutation—not an assumed empty-slot command.** The engine says to equip an eligible mutation in each slot; Flesh Warden’s “unequipping” clause specifies the capacity consequence but does not independently establish an anytime removal action or an empty-loadout procedure.

A suitable exact replacement is **`warrior.supplement.spinal-buffer`**: it has the same Warrior 1/Basic Vital prerequisites and operates only while active through serum activation. In the proposed follow-up, it can remain **equipped but dormant**, without changing HP or granting its active saving-throw benefit. Bind its narrow acquisition and dormant state in that subsequent contract; do not grant the entire Basic Vital tree or serum activation. This selects a source-supported replacement route without making a universal ruling that empty mutation slots are forbidden.

### 2. MGT-03’s first slice: one actor’s genuine one-hour Short Rest

Start with the existing hero, an explicitly selected profile, and **one exact fixed rest site reached through ordinary public play**. The contract must name the site, coordinates, access/occupancy requirements and fixture authority establishing that this actor can rest there. **Do not automatically designate the treatment station or decay bed as safe.**

A Short Rest requires **one uninterrupted hour of permitted recovery**. Start/reservation does not award completion or benefits. Preserve actor identity, actual arrival, shared clock, incompatible-work exclusions, conditions and current authority. The shared class rules expressly retain expedition pressure, supplies, safe locations and rest debt; they do not grant a scene-change shortcut.

The contract must settle interruption explicitly. For this bounded slice, use **terminal interruption followed by a fresh full-hour attempt**, not banked partial progress. Preserve elapsed time and independently resolved events, release future occupancy, and award no completed-rest reward or mutation-change permission. Specify which actual events invalidate recovery—such as combat, departure, incompatible work or loss of required site access—without treating every Incapacitated condition as automatically incompatible with rest.

A safe-site fixture is not permission to stop the world. Pressure checks, supply checkpoints, expiry and other due events must continue under their existing rules. Whether a particular event interrupts the rest must follow its actual consequence, not merely the existence of a scheduled checkpoint.

### 3. Rewards must be explicit, bounded and source-qualified

The next contract needs a small **rest-effect matrix for this actual hero/profile**. Distinguish an absent entitlement from an applicable but unsupported effect; the latter cannot silently disappear behind a successful “full Short Rest” claim.

| Component | Required disposition |
|---|---|
| **Hit Dice** | **An explicit zero-Hit-Dice choice is sufficient for this prerequisite slice.** It consumes no dice, rolls no healing and grants no automatic HP. Positive spending may remain explicitly unsupported; reject such a request before starting rather than silently replacing it with zero. |
| **RP / Revelation Charges** | Do not create either pool for this Warrior. Canonical Short Rest recovery applies only to an actual qualifying pool or Oracle entitlement. |
| **Warrior Strain** | The Warrior engine specifies reduction by **one** on a completed Short Rest. Reconcile that consequence against the actual source-owned Warrior track; do not confuse it with expedition Strain. Do not invent a positive initial balance merely to demonstrate a reduction. |
| **Serums and Mutation Recovery Reserve** | **No Short Rest refill.** Neither is replenished by a completed hour, loadout change or menu operation. |
| **Other owned Short Rest effects** | Execute the effects actually applicable to the selected profile, including valid source-specific refreshes and endings. Record explicit non-applicability or an unsupported boundary rather than granting every Warrior card. |
| **Unrelated recovery** | No automatic Wound cure, general condition cleanse, Long Rest entitlement refresh, or credit for completing an eight-hour Rest Watch. |

The canonical procedure permits Hit Dice expenditure, pool-specific recovery and Short Rest endings. The Warrior engine separately supplies its Strain reduction and excludes Short Rest refills of serum doses and Mutation Recovery Reserve. Wound treatment remains distinct.

**Two-benefit cadence:** track beneficial completions per actor between actual Long Rests. A completed beneficial rest counts even when the player chooses zero Hit Dice or receives no numerical increase because a pool is full. An interrupted attempt does not count. Reloading, encounter closure, a new day or another command ID cannot reset the counter. Initial availability must be an explicit fixture fact—not a fabricated historical Long Rest.

Also distinguish **benefit eligibility** from the mere completion of elapsed rest. A third request must not earn prohibited numerical recovery or refreshes, but that does not establish a universal rule that every effect ending on a completed rest remains active. Source-specific ending clauses need their own disposition; the reviewed maximum-HP procedure already distinguishes such removal from numerical rest rewards.

### 4. Keep mutation changes in the subsequent TAC-06 slice

**MGT-03 should produce the authoritative, receipt-bound completed-rest event and reward/cadence result—not a mutation loadout editor.** Preserve enough identity and timing to bind later permitted choices to the exact rest.

The subsequent Flesh Warden contract should attach its choice to that completion boundary, with atomic loadout validation and capacity recomputation. It must not treat an old rest receipt as a reusable permit to swap mutations during later combat.

The intended follow-up remains:

**Genuine injury → first completed rest equips Flesh Warden without healing → actual finite healing → second completed rest replaces Flesh Warden → any required downward clamp → ordinary continuation.**

The parent vial’s nine-point potential is a useful feasibility lead, **not a guaranteed successor roll**. The new route must establish its own actual HP, dice and elapsed events. Zero Hit Dice in both rests makes the capacity-versus-healing distinction easier to demonstrate without adding another healing mechanism.

**The detached temporary-HP contrast is sufficient for the capacity operation itself.** A live Consume Decay grant activated before a full one-hour rest will reach its own one-hour deadline no later than that rest completes. Preserve the grant’s genuine expiry; do not shorten the rest, extend the grant or inject an activation during rest to manufacture overlap. Bind any tied expiry/completion ordering through the shared scheduler.

### 5. Bounded MGT-03 acceptance witness

Require a public route with **lawful site arrival, rest start, a genuine pending save/restore, one-hour completion, exact applicable rewards, and paid ordinary continuation**. Add an interruption/restart branch, two beneficial completions and a third-benefit control. Compare one long advance against equivalent chunks so deadlines and rewards resolve once in the same order.

Retain current-authority retries, conflicting IDs, occupied/unsafe-site denial, no overlapping work, strict forged completion/reward/cadence rejection, authentic predecessor compatibility, and restored-console/uninterrupted-console/direct-public-C# agreement. The implementation must run the then-current **1,498 accepted predecessors plus its new registered controls**.

**No alternate maximum-HP source is selected. No additional Flesh Warden candidate search is needed before the rest contract.** I have not established another exact authored bonus whose two endpoints are already supported publicly.

I inspected the dependency packet, pinned Warrior engine and normalized mutation records, canonical Short Rest rules, shared timing, Core recovery and the MGT-03 map entry. **I did not execute the engine or reproduce the proposed feasibility route.**

**Final ruling: approve MGT-03’s bounded public Short Rest as the immediate source/API gate; then return to TAC-06 Flesh Warden and its rest-bound replacement endpoint.** Wire102 remains accepted. Broader rest/class completion, revival, production authority and Unity gameplay integration remain deferred.
