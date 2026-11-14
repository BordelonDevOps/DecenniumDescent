# GPT contract review

Message `42be382f-900e-4497-817c-d778770ba6c3` in Unity Rules Engine Development.

## TAC-06 Wound treatment — written authorization

**AUTHORIZED for the bounded `TEST_ONLY` implementation described in commit `2490e5e493571aa3bfa01d6e0bb9dc56a32efd95`.** That contract controls this increment and supersedes the earlier site paragraph in `0b0157fc2`. **The superseded r320 approach/movement objection is not a blocker to this proposal.**

This authorizes Codex to implement the separately selected **wire101/base90** session, its console option, the expressly proposed fixture facts, and the narrowly scoped shared-state integration below. It does **not** declare the implementation tested, accept its eventual evidence, or authorize Unity gameplay integration.

### 1. Exact r317 site and patient — authorized

Use the genuine successful wire100 post-combat boundary:

| Binding | Authorized value |
|---|---|
| Starting boundary | **r317**, clock **`113673/2`** |
| Hero and fixed treatment station | **`(1,2)`** |
| Named companion | **`(1,3)`**, already stationary and cardinally adjacent |
| Patient’s starting life state | Living, **Stable at 0 HP**, Unconscious |
| Existing medical target | **One genuine Wound, with no linked Injury** |
| Posture | **Prone**, independently retained |
| Existing Stable-recovery deadline | **`128033/2`** |
| Uninterrupted treatment completion, when started at that boundary | **`171273/2`** |

These are the specific boundary and timestamps selected by the refined contract. The later recovery to 1 HP must not be substituted for the actual treatment-start state.

**Starting treatment does not require this patient to have positive HP or to be awake.** The pinned Injury and Aid example expressly starts treatment while the patient is Stable at zero, resolves the existing 1-HP recovery during treatment, and continues the treatment afterward. Requiring prior recovery would contradict that example.

The implementation must therefore preserve two separate events: the existing Stable event produces **0→1 HP at `128033/2`**; treatment resolves its Wound outcome after its own eight hours. Stable recovery neither restarts nor interrupts treatment merely because the patient is no longer Stable. End only the Unconsciousness attributable to zero HP when the life rules require it; retain independent conditions and Prone.

**No departure, reentry, patient relocation, additional reach, or pressure bypass is authorized or required.** Retain the existing pressure and elapsed-time behavior. The station is not an implied Haven, safe-rest grant, or immunity to independently occurring events.

### 2. Fixed medical kit and treatment consent — authorized fixture facts

I approve the specifically authored **`TEST_ONLY` ordinary Wound-treatment medical kit** at the fixed station, including the hero’s explicit functional access and service authority.

This is a stationary, reusable treatment implement, reserved exclusively while a job is active. Its availability must be represented and checked; an occupied, inaccessible, or unusable kit cannot satisfy the requirement. Release the job’s reservation on completion or interruption.

**Do not consume a separate treatment-kit charge.** The controlling proposal distinguishes the treatment implement from the portable Healer’s kit used for stabilization: this procedure requires the kit and spends Supply, without asserting that a stabilization charge pays for treatment. The pinned walkthrough likewise treats stabilization and eight-hour treatment as separately funded procedures.

This authorization creates no portable-equipment equivalence, carrying mass, sale value, generic kit substitution, or other medical service. I also approve the proposed **explicit consent fixture for this named patient’s ordinary Wound treatment**, including its Stable-zero start. That fact is independent of potion-swallowing willingness and grants no general consent rule.

### 3. Two finite Supply baskets — authorized

I approve **exactly two independently sealed, finite, prepacked Supply baskets**, initially at the station under the hero’s custody. Each basket contains:

| Material group | Quantity per basket |
|---|---|
| Dry ration-equivalent food | **2 lb** |
| Clean water | **8 pints**, held in **two actual four-pint skins** |
| Compatible lamp oil | **1 pint**, in its actual flask |
| Sundries | **¼ lb** |

Those are the quantities and physical-container bindings proposed by the controlling contract. Preserve its pinned mass, capacity, packing, and expiry rules.

Bind each basket to distinct finite lots, actual vessel identities, an explicit packing timestamp, and initial-stock provenance. These are **new authorized fixture facts in the selected successor**, not a claim that the historical wire100 session already possessed this stock.

At each accepted start, reserve and debit **one complete basket through shared WorkLedger**, atomically across all four material groups. Missing, insufficient, expired, inaccessible, or already-committed required stock must deny the start without a partial debit.

Retain the same skins and oil flask as empty vessels, with their applicable empty-vessel mass. Consumed material cannot also provide ration, drinking-water, provisioning, trade, fuel, or subsequent-treatment credit. There is no automatic replenishment or implied purchase.

Two baskets permit at most two funded starts from that stock. They do not permit treating an already-removed Wound.

### 4. Eight-hour job and interruption — authorized

Approve the proposed hero start and explicit interrupt commands, bound to the current Player grant, named companion, exact existing Wound, station, kit, basket, and current shared time.

Reserve the healer’s active work and the patient’s required treatment access for the job. The patient’s reservation must **not** reuse an awake-worker eligibility check that would incorrectly exclude the authorized Stable-zero patient. Conversely, the healer must actually be awake and capable. No open encounter or incompatible activity may be ignored to start or continue the job.

**Interruption is terminal for that attempt, not a pause.** It retains the entire spent basket debit, releases future healer/patient/kit occupancy, draws no treatment check, and awards no Wound removal or treatment benefit. It does not reverse elapsed time or an independently completed Stable recovery. This is the interruption composition requested by the refined contract.

A subsequent legal start requires another complete basket and a fresh eight-hour interval. **`171273/2` is the completion time only for the uninterrupted attempt starting at `113673/2`; a restarted job derives its deadline from its actual new start.**

For this increment, reject incompatible voluntary activities while the job remains active; the explicit interrupt provides the supported way to end that commitment. Independently occurring events must retain their actual effects, and loss of required treatment eligibility or access cannot be ignored at completion.

### 5. Tier I, check, and Wound effects — authorized

I approve **Tier I / Medicine DC 12 as an explicit `TEST_ONLY` site fact** for this station. It is not inferred from coordinates, character level, or the encounter’s difficulty. The pinned walkthrough also establishes the applicable treatment tier separately from the patient’s state.

After eight valid treatment hours, resolve **one receipt-bound Wisdom (Medicine) check** using the actual healer’s Wisdom, Medicine training, applicable Injury and condition modifiers, and the existing four-degree resolution rules.

| Degree | Authorized treatment effect |
|---|---|
| Critical Success | Remove the selected Wound and its linked Injury, if any. Apply the source’s second-Wound removal only when another eligible existing Wound and the required patient choice exist. |
| Success | Remove the selected Wound and its linked Injury, if any. |
| Failure | Remove no Wound; the basket remains spent. |
| Critical Failure | Remove no Wound; the basket remains spent; apply **one expedition Strain to the patient**. |

These outcomes follow the controlling contract and pinned walkthrough. **This witness has only one Wound and no linked Injury:** do not invent another Wound or Injury to exercise a conditional effect, and do not claim this witness proves second-Wound selection. Treatment itself restores no HP and does not stand the patient up.

### 6. Source-qualified expedition Strain — authorized narrow extension

I approve a **treatment-owned Critical Failure cause in the existing shared Expedition Strain ledger**. Its authority is the completed treatment and its recorded result—not the presence of a Daily Provisioning profile.

The source explicitly assigns ordinary Wound-treatment Critical Failure to **`expedition.strain`**, with the **patient** as recipient. It is not Warrior serum Strain, Exhaustion, another Wound, or a healer penalty.

The validation extension must bind the gain to the exact completed job, Critical Failure receipt, recipient, and completion timestamp, preventing duplicate application. It may admit this validated treatment cause without Daily Provisioning enabled. **It must not indiscriminately remove the existing validation guard or admit arbitrary nonempty Strain histories.** Preserve historical provisioning, rest, and other source behavior.

Use the shared point history, source metadata, consequences, and absolute-marker authority. No treatment-local Strain counter is authorized. Where the witness produces **0→1 expedition Strain**, retain the sourced **−1 initiative and expedition-check consequences**; do not prematurely apply the level-two attack/save penalties or retroactively reorder an established encounter.

### Implementation acceptance boundary

**No source/API blocker remains for this exact bounded proposal.** The requirements above are implementation obligations, not a request for another unchanged proposal round.

The returned implementation evidence must demonstrate the authentic r317 continuation; independent Stable recovery during treatment; finite stock and vessel accounting; completed and interrupted jobs; atomic current-state denials; receipt-bound outcomes and Strain; and replay without duplicate costs or benefits. Preserve and run the contract’s **exact 1,496 predecessor cases**, together with the new registered controls. That number is the required regression baseline, not a claim that I have run or passed it here.

**Codex is authorized to proceed with the refined TAC-06 wire101/base90 `TEST_ONLY` implementation on these terms. Implementation acceptance and Unity gameplay integration remain separate gates.**
