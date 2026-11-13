Actual Unity Rules Engine Development reply `ffc9e6d7-4753-4166-9c51-a540557bb776`, recorded verbatim apart from trailing whitespace.

## **Approved for bounded implementation**

**Contract:** `b95c33783c4ae86eccb7b7cfb129a3774baad9a3`
**Baseline engine:** `8ff2ceea32ded339bb043b9669718535683ee577`

**Authorize the selected MGT-01 finished-vial carrying and remote-use implementation, with the held-hand clarification below. No additional preliminary source/API packet is required.** Direct prerequisites remain **FND-01, FND-02 and FND-05**, using their accepted selected scopes.

### 1. Handling correction: the root-carried vial occupies one hand

For this containerless selection, require **root `Carried` placement, no parent container, hero custody and one occupied hand**. Do not treat the vial as hands-free merely because its placement says Carried. This is the bounded fixture arrangement, not a universal rule for potions stored in actual containers.

Reuse the existing **one-second ordinary Pickup** with current actor/inventory authority, same-cell or cardinal reach, stationarity, available handling hand, work restrictions and capacity checks. Preserve its existing shared-clock ordering and unsupported-boundary guards. The companion remains owner/maker; the hero becomes custodian.

Drinking uses **that same held hand**, not a second free hand. Recognize only the selected dose’s own proven occupancy when assessing its use; do not grant a generic extra hand. After drinking, the empty vial remains held.

Existing consequences that require held equipment to drop must also reconcile this body: move the same vial, clear its hand occupancy and update physical access. Voluntary stowing, handover and general drop commands may remain outside the new public surface. A drop does not invent breakage, spilling or automatic re-equipping. The current held-hand and condition-drop implementations need this narrowly selected extension.

### 2. Approve the one-body link

Create the portable representation **only when actual settlement produces recipe-4 output ordinal zero**. It represents that existing dose/vial—not an additional item.

Keep `AlchemyDoseRecord` authoritative for provenance, maker/title, structural HP and spent/use evidence. Use the linked portable root for placement, custody and access; synchronize mirrored dose fields within the same committed transition. Validate a unique, exact link and reject contradictory custody, duplicate representation or unsupported placement.

Count mass once: **1/5 lb and 1/50 Load filled; 1/10 lb and 1/100 Load after oral use**. Derive current mass from the linked dose; do not add a second container, ordinary inventory lot or `WorkLedger` stock. These masses and the retained empty vial follow the pinned Alchemy procedure and provisional pounds-to-Load rule.

### 3. Approve explicit **wire96/base90**

Use a distinct, pre-initialization TEST_ONLY selection and fingerprint. Keep the existing base90 feature payload and required observation/specimen/batch sections, with an explicit new composition marker and the selected linkage semantics.

Preserve authentic Default and Fishing Trap wire95 bytes and behavior. **No automatic migration or post-load insertion of a vial.** Require symmetric encode/decode validation: older envelopes must reject the new link or held-vial semantics before emitting an invalid save. Wrong-profile and Release loads must reject atomically. Retain full canonical history validation; a checksum alone is insufficient.

Do not set the base feature schema to 96 merely to obtain the wire number. The current codec already distinguishes wire envelopes from their underlying feature layout.

### 4. Approve the remote tactical route

Use the existing `UseAlchemyDose` command for the hero’s self-use of the selected, actually held dose on its legal regular turn. Preserve Action payment, pending-decision precedence, bodily/ingestion eligibility, authoritative dice, healing restrictions and the retained vial.

**The linked dose must never regain workshop access through a fallback check.** Sibling doses retain their original bench restriction.

Demonstrate use at an actual position outside the old workshop reach. Use the original seed, actors and geometry, with real paid movement and required specimen-vessel closure. Actual injury is preferable when naturally produced, but lawful full-HP use is acceptable: verify the rolled potential, actual capped benefit, payment and spent vial without forcing damage or a favorable outcome.

### 5. Acceptance evidence

Require:

| Group | Evidence |
|---|---|
| **Identity and handling** | Real manufacture creates the link once; paid pickup changes custody, hand occupancy and burden once. Wrong authority, remote/malformed/stale requests and supported hand/capacity failures preserve complete state. |
| **Remote use and consequences** | Genuine carried state beyond bench reach; actual tactical use; one spent Action/dose; same retained vial; exact burden reduction; untouched siblings; applicable mandatory-drop behavior. |
| **Persistence and integrity** | New-profile save/restore and deterministic continuation; duplicate/conflict controls; forged link/custody/spent-history rejection; authentic older profiles unchanged. |
| **Exact execution** | Public C# and console evidence, source/assembly bindings, compilation/static checks, and the complete **1,491 accepted predecessors plus new registered controls**. |

**No further blocking source decision remains within these boundaries.** I inspected the contract, pinned physical/use sources and relevant portable, hand, condition and codec paths; I did not execute code or modify files.

This authorizes implementation—not acceptance of unproduced results. Prior acceptances stand; broader inventory operations, production authority and Unity integration remain deferred.
