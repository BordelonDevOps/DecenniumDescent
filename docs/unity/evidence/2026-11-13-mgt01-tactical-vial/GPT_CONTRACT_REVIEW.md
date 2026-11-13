# GPT contract review

Unity Rules Engine Development reply `637db451-53eb-448f-af1f-d90ec7c61357`.

## MGT-01 tactical packed-vial access — **approved for implementation**

**Contract:** `fbf57bd85732e30d35986430135ecf4623e2a83c`
**Accepted baseline:** `35feab09594441183f5070b1f3cfdc6afc8ff3fb`

**Authorize this bounded implementation. No blocking source/API correction remains, and no additional preliminary packet is required.** Direct mapped prerequisites remain **FND-01, FND-02 and FND-05**; accepted wire97 handling and tactical action procedures are operational dependencies. The inspected comparison contains documentation changes only.

### 1. Tactical costs — approved as proposed

The pinned Combat Action rules and adopted handling decision support separate opening and retrieval interactions. Drinking remains its own Action; ordinary exploration’s one-second cost does not apply during tactical handling.

| Actual starting state | Approved sequence |
|---|---|
| **Closed pack; free interaction and Action unused** | Open spends the free interaction. Retrieve spends the second interaction **and Action**. Same-turn drinking rejects. Drink only after a subsequent lawful Action becomes available. |
| **Pre-opened pack; free interaction and Action unused** | Retrieve spends the free interaction. Drink spends that turn’s Action. |
| **Action already spent; free interaction unused** | One otherwise lawful simple Open or Retrieve remains possible. Drinking and a second interaction remain unavailable. |
| **Vial still contained, open or closed** | Direct drinking rejects without payment or mutation. |

An Action restriction must not automatically deny an otherwise lawful first simple interaction. **Surprise alone preserves that distinction**, while incapacity, unavailable hands, physical inaccessibility and other applicable restrictions still control. Do not grant new condition exceptions or additional interactions.

Opening and retrieval add **no RuleClock time and no worker interval**. They update the existing tactical interaction/Action ledger and receipt-linked handling history. Resource refresh occurs through the actual regular-turn procedure—not a save/load, query, round-number change or additional command. The existing handler already supplies this separate tactical accounting.

### 2. Authority, physical state and scope

Approve only the selected hero’s **Open of the exact worn pack** and **Retrieve of the exact directly contained vial**, during the genuine active later encounter and the hero’s owning regular turn.

Keep current grant and revision checks, receipt matching, current-slot validation, pending tactical/manufacturing-choice precedence, stationarity, work restrictions, physical access and available-hand checks. The existing payloads need no separate new turn token, provided authoritative current-turn validation and receipt-bound reconstruction remain mandatory. A revoked grant cannot recover authority by retrying an earlier successful command.

Retrieval requires one genuinely free hand and occupies it. Drinking uses that same held hand—not a second free hand—and retains the existing Action, ingestion, RNG, healing and empty-vial procedure. The current held-dose assessment already distinguishes actual held access from bench access.

Opening the **pack** changes access only; it does not open the sealed dose, start an opened-dose expiry, consume anything or change mass. Preserve companion title/maker, hero custody, one physical identity, exact burden and sibling locations.

Tactical Stow, Close, Pickup, voluntary Drop, removal and handover of this selected arrangement remain unsupported. Mandatory held-item consequences remain operative; if an intervening event drops the retrieved vial or incapacitates the hero, later use must recheck the resulting state.

### 3. Approve explicit **wire98/base90** isolation

Use the proposed pre-initialization selection, distinct fingerprint and discriminator, retaining the existing physical and tactical records rather than adding another hand, Action or inventory ledger.

Wire98 alone admits these tactical operations. Authentic wire95, wire96 and wire97 selections must retain their bytes and behavior; **no automatic migration or silent relaxation of wire97**.

Encoding, decoding and full historical validation must reject inconsistent selection, parent/custody/hand state, duplicate representation and forged tactical spending. Establish handling’s owning encounter/turn through its actual receipt and reconstructed ledger; equal start/end timestamps alone are insufficient proof of payment. Restoration remains atomic.

### 4. Acceptance evidence

**Both genuine routes are required.** Enter the later encounter still packed. For the closed route, retain packed-entry, post-Open, post-Retrieve and post-use saves; demonstrate same-turn drinking rejection and play through the actual intervening turns and defender decisions. For the pre-opened route, demonstrate free Retrieve followed by the same turn’s paid drink.

Require wrong-seat/turn, pending-choice, unavailable-hand, spent-Action and exhausted-interaction contrasts; current-authority retries; and unchanged complete state around rejected inputs. Distinguish live histories from any labelled detached controls. Full-HP use remains acceptable—do not force damage or reseed to obtain healing.

Compare restored console, uninterrupted console and direct public C# **within each branch**. Closed and pre-opened branches need not share final bytes because their legitimate actions and timing differ. Preserve authentic predecessor continuation, compilation/static evidence, exact source/assembly bindings and the completed suite of **1,493 accepted predecessors plus new registered controls**.

**Final ruling: implementation authorized under these boundaries.** I inspected the exact proposal, pinned action/Alchemy rules, adopted handling decisions, current handling/use paths and documentation comparison. I did not execute code or modify files.

Prior acceptances stand. General tactical inventory, production authority and Unity gameplay integration remain outside this approval.
