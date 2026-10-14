# EX58-EDIT-02 — Knowing-holder assay/remint liability

**FINAL controlling addendum to EX58-SOURCE-2026-10-11. Source-authoring correction only; no exact-candidate approval.**

## Decision

**B — KEEP the original greater-of rule, with explicit total-payment/fee allocation.** FL-25's source-attributed 10% cap was my wording error, not an intended NEW capped fine. Withdraw that cap from the current operational directions; preserve the original source and the incorrect historical verdict unchanged.

The frozen `DescentReviewChanges/ReviewBible/docs/mechanics/GAMEPLAY_LOOP_CANON.md`, §17 **Haven resolution**, subsection **Coin assay and reminting**, lines613–617, says: “A knowing holder pays the greater of 10% of the false lot's face value or the assay and remint fees.” The complete relevant frozen paragraphs, their line numbers and archive/member hashes are in `EX58_EDIT_02_SOURCE_EXCERPT.md`.

The source comparator is retained. **NEW explicit accounting completion:** the greater-of amount is the total monetary liability including the actual service fees; its nonnegative remainder is the additional criminal fine. This accounting split is not claimed as verbatim source wording. It introduces no separate cap, fee schedule, offense or presumption of knowledge.

## Exact replacement paragraph

Replace only FL-25's third authoring paragraph, beginning `KEEP ordinary assay fee1%`, with this single complete paragraph in all three representations:

KEEP ordinary assay fees at 1% of the face value of the actual accepted assay bill, minimum 1 gp for that real service, and remint fees at 2% of the recovered legitimate metal value accepted for actual reminting. A combined commissioned assay bill receives its minimum once, not per coin, variant or thirty-minute stage; services not incurred create no fee, and an already-owned private testing toolkit creates no fictional desk fee to its owner. KEEP the Loop greater-of rule for a holder lawfully established to be knowing, not a 10% cap. NEW explicit total-payment and fee allocation: let F be the confirmed false lot's face value, A the actual assay fee, R the actual remint fee, and S=A+R for the same assessed lot/bill; the total monetary liability is P=max(0.10×F,S), allocated to service fees S and an additional criminal fine of P−S=max(0,0.10×F−S). Do not charge P plus those fees or levy another 10% fine on top. Compute on exact amounts under FL-21/EC-10's existing final-transaction copper rounding; allocating the total between fees and fine does not itself create extra transactions. Credit actual prior payments and fees already withheld from returned legitimate metal once against the same liability, leaving only its unpaid balance. Confirmed counterfeit coin or plated false currency is seized in full only through actual lawful authority; seizure is neither a fee nor a payment credit. Genuine coins and legitimate metal remain separately identified and are returned with actual fee deductions accounted for once. An innocent holder with documented provenance pays no criminal fine; absent a lawful knowing-holder finding, this rule imposes no criminal fine. Suspicion, ancestry, a failed die or missing documentation alone does not establish knowledge. Assessment, collection and custody require actual authorized actors; an unpaid amount remains an obligation, not automatic borrowing or remote confiscation. Cutting/reminting takes the provider's actual work and links consumed/replaced coin identities to real metal/output quantities without duplication.

## Three exact operations

| Operation | Package file | Exact location |
|---|---|---|
| EX58-EDIT-02.1 | `EX58_AUTHORING_VERDICT.md` | FL-25 — Coin, crime, labor and rescue preserve real status; third authoring paragraph; original line410 |
| EX58-EDIT-02.2 | `EX58_AUTHORING_REGISTER.json` | `/directions/24/authoringWording`; guard `/directions/24/id == "FL-25"`; original line438 |
| EX58-EDIT-02.3 | `EX58_CONFLICT_DISPOSITIONS.json` | `/conflicts/22/completeReplacementWording/FL-25`; guard `/conflicts/22/id == "EX-C23"`; original line467 |

`EX58_EDIT_02_CORRECTIONS.json` includes the exact old/new paragraph for the manuscript and exact old/new complete strings for both JSON fields. Only paragraph3 changes inside those strings; the other seven FL-25 paragraphs remain verbatim. The frozen17-payload package has exactly these three occurrences of the erroneous cap. IDs and exact strings control; line numbers locate the preserved submitted version.

EC-10 already supports the exact calculation, unique transaction IDs, prior-payment links and paid/owed distinctions. No replacement is needed in `EX58_FIELD_CONTRACTS.json` or `EX58_CONTRACTS_AND_EXACT_REVIEW.md`. The completed EX58-EDIT-01 office corrections remain unchanged. EX-C23's metadata and FL-24 direction, FL-21 rounding, EX-W28, other cases, all source fees/DCs and all unrelated procedures are retained. There are no recipe, class, spell, feat or body changes.

## Worked boundaries

These are synthetic numerical fixtures under declared lawful findings and actual-service premises, not findings about campaign actors.

| Fixture | Exact fees | Correct total liability | Additional fine | Remaining after specified credits |
|---|---:|---:|---:|---:|
| Knowing holder; false face1000gp; mixed assay bill1200gp; legitimate metal actually reminted worth200gp | Assay12 + remint4 =16gp | max(100,16)=100gp | 84gp | 84gp when16gp of fees were already paid/withheld; not100gp or116gp |
| Knowing holder; false face20gp; mixed assay bill120gp; legitimate metal reminted worth100gp | 1.20 +2 =3.20gp | max(2,3.20)=3.20gp | 0gp | 3.20gp if nothing paid;0 after fees fully paid |
| Knowing holder; false face50gp; assay bill500gp; no remint service | 5gp | max(5,5)=5gp | 0gp | 5gp if unpaid |
| Innocent documented holder with the first fixture's actual services | 16gp | 16gp | 0gp | 0 if16gp already paid |
| No lawful knowing-holder finding, including missing provenance alone, with the first fixture's actual services | 16gp | 16gp under this rule | 0gp | Actual fees only; unresolved intent is not a guilty finding |
| Knowing holder; false face100.03gp; same-face assay; no remint; one genuinely combined final bill | 1.0003gp exact | 10.003gp exact | 9.0027gp exact | Combined final bill10.01gp under existing copper ceiling, not repeated intermediate rounding |

The confirmed false portion supplies F; the actual accepted assay bill supplies A. These need not be the same face value in a mixed lot. No hypothetical remint fee is assessed when no remint service is incurred. Seizing false currency does not pay the monetary liability or create a second fee. Authority, knowledge, actual services, payments, original coin identities and legitimate-metal custody still need their own real records. Unknown facts do not become zero, guilt, paid status or permission by arithmetic.

## Finite acceptance and history

Apply the three exact amendments only to current derived authoring copies; preserve the original EX58 ZIP, its manifest, original source/verdict hashes, receipt and2,316-check report unchanged. Preserve EX58-EDIT-01 and the source's original greater-of wording. Append this addendum ID, source link and measured descendant hashes as a separate current correction/receipt. Do not overwrite historical artifact hashes or use a new hash as evidence that an old verdict already contained this rule.

The machine-readable correction lists seven finite acceptance expectations. They require three-way paragraph parity; no unrelated wording changes; the fee-plus-fine identity; greater/equal/lesser comparator cases; innocent/unresolved-intent boundaries; single credit for actual paid/withheld fees; existing final rounding; real authority/custody; and immutable historical provenance. This is sufficient for authoring the corrected FL-25 candidate without another source conference. Full exact-candidate review remains ahead.

### Measured minimal-replacement descendants

These hashes are for in-memory minimal byte replacements against the frozen source-direction package. They are not claims about the user's current repository. They apply when all other bytes in each of these three files remain unchanged.

- `EX58_AUTHORING_VERDICT.md`: 225,196 bytes; SHA-256 `028c2b870e07b79a78f1ae8caccd78421e8f9083f6d3e518288f9a2b8960d3fb`.
- `EX58_AUTHORING_REGISTER.json`: 265,762 bytes; SHA-256 `5e02480b98b8085c9be8decc381b85565b9b0611c753903c7b31dc3fb3b0aa4f`.
- `EX58_CONFLICT_DISPOSITIONS.json`: 214,911 bytes; SHA-256 `e9e85a6f2d7d6dc85884d65acfdf76694de0d0cbf72de753aad16a3e3421238b`.

## Executed evidence and reproduction

**68 focused checks passed; zero failures.** These verify the two archive hashes, the controlling Loop member, all17 original verdict payload hashes/lengths, the exhaustive three-location cap scan, the three in-memory replacements, unchanged other values/paragraphs, JSON/manuscript parity, repeat-application rejection and nine exact-rational reference fixtures. The original2,316-check suite was not rerun here. The seven semantic expectations are source-based acceptance requirements, not executed world-authority, custody or gameplay-runtime tests.

Run the included standard-library script with the preserved archives:

```bash
python validate_ex58_edit_02.py --source-archive DD_Expedition_Transport_Social_58_Source_v3.zip --verdict-archive DD_Expedition_58_Source_Verdict_and_Evidence_2026_10_11.zip --report EX58_EDIT_02_CHECKS_REPRODUCED.json
```

The script reads archives and checks amendments in memory; it writes only the requested new report. It does not modify a repository, submit work, patch originals or implement the game procedures.

No other EX58 decision or fulfilled gate changes. No new owner-confirmation gate, exact-candidate approval, promotion, push, deletion, human/balance/runtime certification or cosmology interpretation is granted. The agreed sequence remains actual final joint whole-game flow agreement, the already-authorized push, verified remote commit, then careful cosmology review.
