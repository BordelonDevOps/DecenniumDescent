# FEAT327-ACQ-02 — Warrior equipped-tier and activation addendum

**Disposition: REVISE the proposed global/global rule.**

The controlling interpretation is **at most two equipped Advanced mutations per actual mutation tree, but at most one equipped Apex mutation across all trees**, always within the Warrior’s actual unlocked total slots.

This is a **NEW explicit reconciliation of conflicting current wording**, not a claim that the original book unambiguously established this combination. It retains the current engine’s **“Each tree”** scope for Advanced mutations and selects the unqualified **“maximum one Apex equipped”** requirement repeated by all three specific Apex cards over the engine’s conflicting per-tree Apex clause. A global limit of two Advanced mutations would impose an additional restriction that this reconciliation does not require.

**Scope: a necessary, narrow correction to the derived Warrior class engine—not a feat-only exception.** The same legal loadout must govern ordinary Warrior play and mutation-feat prerequisite validation.

I verified that the archived `warrior.json` is **158,412 bytes** and matches your supplied SHA-256. I also inspected the corresponding Warrior manuscript, historical tier excerpts, and final shared/mutation-feat directions. The source bindings and inspected records are retained in the SOURCE_EVIDENCE.json[source evidence](sandbox:/mnt/data/feat327_acq_02/SOURCE_EVIDENCE.json).

## ACQ02-O1/O2 — Exact Warrior engine replacement

Replace:

`DescentReviewChanges/ReviewBible/data/public/class_playtests/warrior.json`  
**JSON pointer:** `/engine/17`

Also replace its identical current **MUTATION TIERS** paragraph in:

`DescentReviewChanges/ReviewBible/docs/mechanics/classes/warrior.md`  
**Submitted location:** line 54, within the Engine section.

Use this identical replacement in both operative representations:

> MUTATION TIERS. Basic mutations require Warrior 1. Advanced mutations require Warrior 6. Apex mutations require Warrior 15. You may equip only mutations whose actual Warrior class-level gate and other prerequisites you meet. NEW explicit scope reconciliation (FEAT327-ACQ-02): across your single set of unlocked mutation slots, you may equip at most two Advanced mutations from each actual mutation tree and at most one Apex mutation in total across all trees. Basic mutations have no additional tier-count ceiling beyond the remaining unlocked slots. Count every equipped mutation, including a dormant one, toward its relevant equipment ceilings; use its actual source-defined tree and tier. These are equipped-loadout ceilings, not per-tree slot grants, limits on the number of feat identities acquired, or separate active-only tier ceilings. The completed-rest equipping procedure and prohibition on duplicate named mutations remain unchanged. Mutation Efficiency changes only the ordinary global simultaneous-active limit. Transcendent and Apex Form activate only the existing legally equipped loadout and do not waive equipment ceilings, level/prerequisite gates or duplicate restrictions. Apex Form's permanent slot IV is the single Warrior-20 slot unlock, not an additional slot each time the form activates. After a temporary activation exception ends, apply its exact ending procedure and the then-applicable active-mutation limit without refreshing durations or granting an unequipped mutation.

**Keep `/engine/2`, `/engine/3`, `/engine/18` and `/engine/23` unchanged.** The three Apex cards’ existing prerequisites also remain unchanged:

- `warrior.supplement.mythic-carapace`
- `warrior.supplement.butcherform-chassis`
- `warrior.supplement.voidbirth-shell`

Their one-Apex requirement now has an explicit global engine binding. The historical book’s **“Max Equipped”** heading and **“Max 2 active / Max 1 active”** rows remain preserved source text; they do not create an additional active-tier ceiling beside this corrected engine.

## ACQ02-O3 — Exact shared feat-acquisition dependency

Append the following paragraph to the **derived current** `FEAT_SHARED_DIRECTIONS.json` rule with `"id": "FS-01"`, in its `wording` value. Insert it at the corresponding end of the FS-01 manuscript section, before **Basis**, and retain identical wording in any operative public/internal shared-contract mirrors.

Preserve the existing FS-01 wording and the fulfilled ACQ-01 amendment to FS-02.

> Warrior mutation-feat acquisition uses the equipped-loadout rules in the Warrior engine as corrected by FEAT327-ACQ-02: at most two equipped Advanced mutations per actual tree and at most one equipped Apex mutation across all trees, within the actual unlocked total slots. Dormant equipped mutations count toward those ceilings. Evaluate each feat's equipped and active prerequisites only at the acquisition or use-time checkpoints that its exact procedure specifies. A temporary all-equipped activation does not supply an equipped prerequisite, slot, mutation, class level or feat opportunity. Preserve each feat's acquisition snapshot and existing ongoing operating conditions.

This dependency note does **not** make every mutation prerequisite require activation during acquisition. Each exact feat still determines whether its checkpoint requires an equipped mutation, an active mutation, or another stated condition.

## Outcomes for the four requested cases

| Case | Final disposition |
|---|---|
| **1. Warrior 13: Ossified Core, Echo Knuckles and Warpgrip Talons** | **All three may be equipped**, assuming the completed-rest procedure and other prerequisites are satisfied. This is one Advanced Vital and two Advanced Combat mutations, occupying the three unlocked slots. Dormancy does not remove any from the equipment count. With **actually acquired and operative Mutation Efficiency**, only two may ordinarily be active; a genuine applicable temporary exception can activate all three. Without Mutation Efficiency, the ordinary limit remains one. |
| **2. Warrior 16: Mythic Carapace plus Butcherform Chassis** | **Reject the combined loadout.** They are two Apex mutations, exceeding the global maximum of one even though they belong to different trees. Keeping either dormant, having a spare slot, or possessing a temporary activation feature does not cure that equipment violation. |
| **3. Warrior 20: three Advanced Combat mutations** | **Reject the loadout.** Three Advanced mutations in the same tree exceed that tree’s equipped maximum of two. Four total slots do not raise the tier ceiling. Apex Form neither equips the third Advanced Combat mutation nor authorizes it to occupy a slot in violation of that ceiling. |
| **4. Warrior 16: three Basic Vital mutations and lawfully acquired Living Fortress** | **The three distinct Basic Vital mutations may be equipped.** With only two actually active, Living Fortress provides no benefit. A genuine Transcendent pulse may activate all three and satisfy its three-active use-time predicate for the actual pulse window. When that window ends, and no other applicable exception continues, return to the ordinary active limit using the existing duration history; the three-active Living Fortress benefit stops. |

**Positive mixed-tree control:** at Warrior 20, two Advanced Combat plus two Advanced Vital mutations meet these tier-count and four-slot limits, assuming all other prerequisites are met. So do two Advanced Combat, one Advanced Vital and one Apex. There is **no compulsory Basic slot, compulsory Apex selection, or hidden global two-Advanced ceiling**.

## What the activation exceptions actually change

| Feature | Retained authority | What it does not authorize |
|---|---|---|
| **Mutation Efficiency** | When actually acquired and operative, raises the ordinary global simultaneous-active limit from one to two. | No extra mutation slot, additional equipment allowance, tier bypass or automatic activation. |
| **Transcendent** | At Warrior 12+, the first qualifying encounter event—crossing 100% Brutality Progress or reaching actual stored BT 4 with a permitted raised cap—activates the legally equipped mutations until the start of the next regular turn. Keep its one-total-pulse-per-encounter limit and exact ending procedure. | No permanent four-BT concurrency benefit, second pulse from the alternative trigger, new equipped mutation, serum-profile grant or immediate healing trigger. |
| **Apex Form** | Retains its Warrior-20 permanent slot-IV grant and its separate Bonus Action, once-per-encounter, three-round activation of the legally equipped loadout without consuming serum doses. | No fifth slot, repeated slot gain, additional Apex equipment, third same-tree Advanced equipment, or serum-profile effects. |

The **permanent slot-IV grant is the explicit equipment-capacity exception already present in Apex Form’s text**. Its temporary activation is a different effect and bypasses only ordinary active-mutation concurrency.

Mutation Surge and Mutation Overload receive no concurrency exception merely from their names. Other features retain only the exceptions their actual operative text expressly supplies.

For Transcendent, use the recorded qualifying event—not a supplied `transcendent: true` flag or the fact that a feature is listed on the character. For example, under the preserved engine, a Warrior 16 with maximum HP 80 could cross the 100% threshold after four independently lawful, qualifying 20-damage contributions across separate rounds. The fourth contribution can trigger the pulse even with stored BT capped at three. That is an **authored conditional example**, not evidence that those attacks or encounter premises actually occurred.

## Effect on the twelve mutation feats

**No operating-procedure or use-time-predicate replacement is required for any of the twelve existing mapped feats:**

`backlashEngine`, `bioStabilizer`, `bornToHorrify`, `distortedDominance`, `evisceratorProtocol`, `evolutionUnderFire`, `hypermutationSpike`, `juggernautCore`, `killChainAdaptation`, `livingFortress`, `synapticRot`, and `terrorEngine`.

Their acquisition checks now consume the corrected class-engine interpretation.

In particular, **HM-16 / `livingFortress` stays unchanged**: Warrior 8 is a minimum, acquisition requires three actual Vital mutations equipped, and its benefit requires three distinct Vital mutations actually active. Warrior 8 ordinarily has only two slots, so that printed minimum alone does not establish acquisition eligibility. Other class levels do not unlock Warrior slot III.

Its retained benefit is the precise protection against advantage granted **solely because of flanking**. This addendum does not turn it into immunity to positioning, all attack advantage, or Tactical Flanker’s separate effects.

## Finite local fulfillment path

Apply **ACQ02-O1, O2 and O3** once to each identified current operative representation. Preserve the old source files and their hashes, and append a controlling **FEAT327-ACQ-02** correction receipt with the measured descendant hashes.

Do **not** rewrite historical `completeWarriorEngine`, `originalWarriorCounterpartPairs`, original book extracts, source objects or previously delivered verdict packages to make them appear to contain this reconciliation. A current evaluator using those preserved snapshots must apply the separately recorded controlling correction.

The finite acceptance checks are:

1. The operative Warrior engine and manuscript contain the identical replacement, and the shared acquisition dependency agrees.
2. Every unaffected engine element, all class-card fields, and all twelve existing feat procedures and source examples remain unchanged.
3. The four requested cases produce the outcomes above, including the mixed-tree positive controls.
4. Dormant mutations still count; duplicate named mutations and unsupported tree relabeling do not evade a cap.
5. Total character level does not substitute for Warrior class level or unlocked slots.
6. Temporary activation uses an actual qualifying event, preserves its frequency and endpoint, and never retroactively legalizes an invalid equipment or acquisition snapshot.

The package includes **eight finite acceptance cases**, including those controls. They are authored source-based expectations, **not class/feat runtime tests claimed executed here**.

**These operations and checks close FEAT327-ACQ-02 without another generic source conference.** They authorize this narrow derived engine correction, not approval of the unfinished exact feat candidate, a class/feat promotion, or a runtime, balance or whole-game-completion claim.

### Source-linked addendum files

DD_FEAT327_ACQ_02_Warrior_Tier_Addendum.zip[Download the addendum, exact operations, source evidence and acceptance cases](sandbox:/mnt/data/DD_FEAT327_ACQ_02_Warrior_Tier_Addendum.zip)

:chatgpt-content-reference{index="2"}[Read the standalone addendum](sandbox:/mnt/data/feat327_acq_02/FEAT327_ACQ_02_ADDENDUM.md)

Package: **20,196 bytes**  
SHA-256: `7e69bc1839aa96f5119d345520b0f1f9791cd6317e9f02aa92a6b30c7303f726`

The delivery order remains **actual final joint whole-game flow agreement → already-authorized GitHub push → verified remote commit → careful cosmology review**.