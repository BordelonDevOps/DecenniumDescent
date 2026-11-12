# Unity Rules Engine Development EXP-03 source/API review

Response `84f2499c-22f3-4d15-8762-f67b068e0a17` approved proposal `6fb5529fd82ed24152ded01a37ac0cefedb030a3`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## EXP-03 existing supply-cache composition — approved for implementation

**Reviewed proposal:** `6fb5529fd82ed24152ded01a37ac0cefedb030a3`
**Accepted session implementation:** `3d866e6fa8e2996a6799b1a1f51a05b735b70b45`

**Approve this exact existing-cache composition, with the command-filtering clarification below. No additional object, stock, credential, gameplay fingerprint or save version is required. No blocking source/API question remains.**

This authorizes implementation of the bounded public session exposure—not acceptance of the unimplemented public walkthrough. No further preliminary proposal is needed within these boundaries.

The repository comparison contains documentation/evidence changes only, with **no intervening package-source changes**. EXP-03’s direct prerequisites remain **EXP-01, MGT-01 and FND-02**, without serial ordering among them.

## 1. Object, stock and credential authority are sufficient

The selected session already initializes this cache and portable kit. Its charter configuration explicitly selects carried reserve water. The proposal therefore reuses actual selected state rather than supplying a new container or placing contents into an existing save.

| Selected fact | Ruling |
|---|---|
| `TEST_ONLY.supply-cache` at `(1,2)` | Approved: stationary, unburied, already discovered, hero-owned, initially locked and closed. |
| `TEST_ONLY.ready-rations` | Approved: the existing two-pound root, retaining its actual owner, custodian, creation/freshness facts and inventory lineage. |
| `TEST_ONLY.thieves-tools` | Approved: the existing one-pound linked physical tool, initially stowed in the explorer pack. Actual retrieval is required. |
| `TEST_ONLY.actor-skin` | **Not cache contents in this profile.** Retain its actual carried location and water. The cache record’s reference does not move it into the chest. |
| Key route | Excluded. Do not add a key, invent its mass or substitute abstract possession for the physical tool. |

The initializer places the ration root at the cache but conditionally leaves the reserve skin carried. Portable initialization then stows the linked thieves’ tools in the pack. Those are distinct physical facts, and the public view must derive contents from current location—not enumerate both references in `SupplyCacheRecord` as present contents.

The existing fixture supplies fit for its admitted items. This approval adds no general item-volume calculation, movable-chest handling, discovery procedure or production loot authority.

## 2. Retain the existing paid lock, opening and pickup procedures

The pinned ordinary-lock source provides an **Action, actual thieves’ tools and DC15 Dexterity check**. Tool possession permits the attempt; proficiency bonus requires the relevant training. The six-second exploration duration and separate one-second opening are previously adopted **TEST_ONLY execution decisions**, not newly inferred universal lock timings.

Approve these public operations:

| Operation | Exact boundary |
|---|---|
| Retrieve tools | Existing `HandlePortableEquipment`/`Retrieve` for the actual linked tools, subject to the pack, access, hand, work and authority rules. |
| Start pick | `Interact` on the exact cache with `PickWithTools`, hero only, ordinary mode, stationary and in actual cache reach. |
| Interrupt pick | `Interact`/`Interrupt` for the hero’s actual working attempt on that cache, using the existing cancellation behavior. |
| Open | `Interact`/`Open` on the unlocked, closed cache; the existing separate elapsed second. |
| Retrieve rations | `HandleInventory`/`Pickup` for the exact ration root, under its actual available amount, capacity, hand and physical-access checks. |

Use the cache resolver’s existing reach predicate—**same cell or cardinally adjacent**, not a substituted tactical diagonal-distance rule. Preserve its stationary requirement. Views and input helpers must not imply that an operation is available merely because its command family is supported.

### Payment, completion and interruption

Starting an ordinary pick pays the current authoritative Action and books the full six-second worker interval, without immediately advancing time or drawing a check. Completion uses the existing shared clock, revalidates the worker and credential, and applies current check facts. Preserve source task-degree handling, Poisoned disadvantage, relevant injury penalties and the selected sight-required failure rule.

A failed attempt leaves the lock unchanged. A later attempt needs its own legal Action and six seconds; the adapter must not grant a refresh, retry automatically or reuse the failed roll.

An interruption retains elapsed time and the already-paid Action, truncates future booking, makes no roll and earns no partial unlocking. **There is no new pick-resume procedure.** A later attempt starts afresh.

Opening does not retrieve anything. Pickup is another actual handling operation and must preserve the existing shared-clock boundary guards. No wrapper may unlock, open and award the ration in a single synthetic transaction.

## 3. Public visibility and command filtering

### Correct the existing locked-stock disclosure

The current generic inventory projection selects owned/custodied lots without excluding stock physically located in the cache. That explains the reported locked-root disclosure. Correct this in the view; do not alter the authoritative stock to conceal it.

Use **actual physical location matching the cache record** to remove cache-located stock from the generic item list. Do not use `SupplyCacheRules.IsCacheLocation` alone for that exclusion: that helper deliberately recognizes only an **open** cache, so it would fail to hide the locked contents.

Approve a derived cache view showing current lock/open status and the hero’s own active attempt only within the proposed ordinary, stationary, in-reach scope. Publish an actionable stock identity and available quantity only when the actual cache is open and accessible.

An exhausted or wholly unavailable root supplies no current pickup token or positive amount. Distinguish **zero available quantity** from proven physical depletion when reservations exist. The positive depletion witness must establish the actual root amount is zero.

The chest remains an identifiable, open object on the depleted revisit. Hiding exhausted stock must not make the chest itself disappear.

After lawful pickup, the carried descendant may appear in the normal inventory projection. Filter by **current placement**, not permanently by ancestry: otherwise the acquired ration would remain hidden merely because it came from the cache.

### Required clarification: fence in-cache portioning

**Keep fresh cache-located inventory requests restricted to the approved root pickup.**

The currently exposed `PortionInventory` path can create a descendant at the source lot’s location. Once the cache is open, that operation can legitimately create another lot **inside the cache**, while the proposed pickup API permits only the original root. That would create an avoidable public-interface gap.

For this bounded composition, reject fresh in-cache portioning and other unselected cache-stock operations before commitment. **Do not broaden the increment into arbitrary descendant retrieval.** Ordinary portioning and intake of the actually carried descendant remain governed by their existing rules.

Partial pickup from the root may retain the existing amount semantics: it creates a carried child while leaving the remainder in the same root. The principal witness should retrieve the full two pounds as proposed.

### Preserve authority and retry ordering

No new grant is needed. The player’s existing hero authority must still satisfy the actual cache/tool/input owner requirements. The director and automatic defender receive no cache operations or contents view.

Fresh guesses, remote targets, unsupported methods and unavailable stock return the session’s existing generic denial without private resolver diagnostics. Apply this restriction in execution admission, not only by hiding command options.

**Do not place current reach, stock or active-attempt filters ahead of legitimate receipt retries.** An exact previously committed pick, open, interrupt or pickup may be retried after the attempt ends, the root empties or the hero departs. Preserve the established receipt outcome under current authority, without repeating payment, rolling or moving stock. Revocation and conflicting payloads retain their existing behavior. The current session already separates receipt matching from fresh-target admission; retain that structure.

## 4. Keep wire95 and the selected fingerprint unchanged

The cache, physical credential, attempts, labor, inventory lineage and receipts already have persistent representations. The existing codec serializes cache state and attempt history, and the validator binds ordinary attempts to their six-second or interrupted worker intervals.

This increment changes the **public adapter and derived view**, not the authoritative rule configuration. Preserve:

- The existing initial state and exact ordinary recipe-4 fingerprint.
- Authentic earlier saves and strict external restoration.
- Verified-prefix execution and the executable strict reference path.
- Existing command payloads, receipts, RNG and historical stock.

No view cache or extra “looted” flag belongs in the snapshot. The root’s actual quantity and handling history already establish depletion. Do not silently upgrade, retag or replenish a restored predecessor.

The visibility correction intentionally changes the permitted public projection. It should not change canonical gameplay bytes for the same previously accepted commands.

## 5. Implementation acceptance witness

The written probe is a useful feasibility record: it reports the genuine failed and successful picks, separate opening, physical descendant, saved departure and depleted revisit. **It is not yet evidence that the proposed public C#/console surface works.** Its natural 11 and 16, timestamps and descendant ID are observed baseline results—not values to install.

Use these five acceptance groups:

| Group | Required evidence |
|---|---|
| **1. Unchanged selected authority** | Start from the actual accepted initial state. Verify the existing cache, two-pound root, stowed tool and carried reserve water. Preserve the prior connected route and its canonical revision-165 checkpoint for identical inputs. |
| **2. Paid access lifecycle** | Actual tool retrieval; failed and successful paid picks; no early roll or unlock; separate opening. Save during a real pick and compare restored completion. Exercise explicit interruption, retained payment and a full-cost later attempt without adding a resume rule. |
| **3. Scoped public information and inputs** | Closed, remote and traversing access; wrong seat/actor; unsupported key/tactical operations; hidden-root suppression; fresh guessed-target denial parity; the in-cache portion fence; current authority and exact duplicate/conflict behavior. |
| **4. Finite retrieval and persistent revisit** | Actual full pickup into one carried descendant; exact ownership, amount, mass and lineage; unchanged carried reserve. Depart, save/reload, revisit the same open depleted cache, reject fresh reopening/retrieval, and continue. Include a partial-pickup control if that existing amount range is exposed. |
| **5. Compatibility and exact execution** | Public C# and actual console walkthroughs; identical-input replay; authentic predecessor restoration; relevant malformed/provenance and unchanged-rejection controls; exact source/DLL bindings, compilation/static evidence and completed regression against the accepted inventory plus new cases. |

Use public views to obtain the permitted cache/attempt/stock identities. A verifier may inspect trusted saved state afterward to establish conservation, but the walkthrough must not require snapshot inspection to choose ordinary player inputs.

The shared clock must continue actual compatible work once and retain all due consequences. Do not restore an Action, suppress events or alter prior history to preserve the probe’s timing. Report the added public-command costs without weakening validation; the existing broader P1 disposition remains unchanged.

## Inspection limits and final ruling

I inspected the proposal, bindings and written probe; the pinned ordinary-lock source and adopted cache decisions; the existing cache initializer, admission, completion, interruption and authority paths; portable initialization; current session command filtering and view; inventory access/portion/pickup logic; cache records/codec; and relevant portions of the existing cache tests.

**I did not execute the probe, load the accepted DLLs or saves, independently recompute hashes, rerun tests or inspect a proposed implementation that does not yet exist.** The reported feasibility outcomes remain Codex’s execution evidence. No files were changed.

**Final disposition: approved for bounded implementation under the rules above.** The only scope clarification requiring explicit attention is consistent filtering of cache-located commands, particularly in-cache portioning, alongside the stock-view correction.

The accepted thin session remains closed. EXP-04/05 and MGT-06 remain later gates; broader P1 and INT-03 remain open. Production authority is unchanged, and Unity gameplay integration stays deferred.
