# AEX-167-v1 — Advanced crafting exact authored-operational verdict

**Verdict: REVISE through the seven finite corrections AEX-01–07 below. Conditional promotion of all 167 recipes and their 100 public projections is authorized once those corrections and the stated checks are completed. No additional generic source conference or resubmission of unchanged source records is required.**

This verdict covers the actual submitted candidates, not merely their previous source directions. No promotion is asserted for the uncorrected archive. The promotion conditions concern authored-operational completeness, not runtime implementation, authentic campaign facts, economic balance, class/feat approval or whole-game completion.

## 1. Exact scope and evidence

The inspected archive is `DD_Advanced_Craft_167_Exact_Review_v1.zip`, SHA256 `a29420353145c4c91ebb472f2843a3ea14041b38eb49b93420ec99294c03b1a7`.

I opened the README and manifest, verified all **195 payload hashes**, and used a separate extracted working copy. The original ZIP was not modified. All **138 protected source/dependency files** still match their supplied hashes. The final source-authoring verdict matches SHA256 `48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0`.

| Reviewed candidate set | Internal cards | Public cards | Exact recipe membership |
|---|---:|---:|---|
| Enchanting | 43 | 25 | recipe-121–159, recipe-636–639 |
| Rune Carving | 41 | 21 | recipe-396–432, recipe-664–667 |
| Scribing | 40 | 28 | recipe-471–506, recipe-672–675 |
| Tinkering | 43 | 26 | recipe-585–623, recipe-684–687 |
| **Total** | **167** | **100** | **All submitted identities** |

The inspection covered every complete card/source object and manuscript, all per-card operating bindings and body choices, shared operating procedures, all **22 internal / 15 public body variants**, all **50 existing weapon/armor host templates**, all **48 class-interface dispositions**, and all **37 qualitative sequence dispositions**. Shared wording was assessed across its complete membership rather than treating a representative card as approval of unseen variants. The 100 six-paragraph book bindings were checked against the supplied actual DOCX text: **600 paragraphs**.

The three supplied validators reproduce successfully: **5,770 internal checks; 1,725 public-envelope checks; 52 grouped numeric/coverage checks**. The detailed coverage remains **2,004 manufacturing rows, 519 structural contexts, 4,560 transitions, 185 chassis conversions, 410 restoration quotes, 59 maintenance-pack variants and 36 omitted-primary inputs**. My separate read-only audit adds **5,091 passing source/object/manuscript/arithmetic/projection assertions** and separately records the seven semantic findings. These overlapping check counts are not an overall completion percentage or evidence that the 37 sequences executed in a runtime.

Relevant paths below are relative to `DescentReviewChanges/ReviewBible/` unless prefixed otherwise:

- **I:** `data/director/advanced_craft_recipe_candidate_internal.json`
- **P:** `data/crafting/advanced_craft_recipe_candidate_public.json`
- **GI:** `docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md`
- **GP:** `docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md`
- **BI/BP:** the corresponding internal/public advanced body catalogues.
- **MI/MP:** the four internal/public trade recipe-card manuscripts.

For a card correction, update its active JSON fields, applicable paragraph, `manuscriptText`, full trade manuscript and public counterpart where that recipe is public. For a guide correction, update both the guide file and the embedded guide text. Preserve the historical source objects, source register, verdict, book paragraphs and prior submitted version; record controlling operational corrections separately.

## 2. Accepted without reopening source authoring

**KEEP the established source mappings and magnitudes.** The 43 Enchanting profiles retain their actual enhancement, damage type, carrier eligibility and dawn budgets. All 41 Rune mappings retain their exact charges, DCs and effects; the eight consumed lens-name correspondences remain distinct from the ordinary working optic. All 22 Scribing scripts retain their precise rank and one/two-use capacities. All 18 automaton attacks retain their newly authored `2+N`, `Nd6`, five-foot profiles and each original printed damage type, HP and AC.

The five distinct custom profiles remain separate: **recipe-667 null seal, recipe-674 Lexicon, recipe-675 covenant Codex, recipe-686 command relay and recipe-687 gate ram**. Their complete embedded procedures are present. None acquires another profile's spell, attack, charge, service or recharge rule. Recipe-623 correctly preserves its original one-year/null-hour fields beside the **1,920-hour / 1,440-hour eligible Forge Dwarf completion**, without rewriting its original price or labor field.

**KEEP ADV-EDIT-01 as applied.** All eleven trap cards and the active shared body/repair instructions preserve the original frame/discharge block while permitting compatible subordinate spring replacement. Historical contrary source wording is explicitly subordinate to that correction. Automaton primary actuators remain primary. The corrected **two Dissonance into one device** quantity also remains correct; AEX-04 below concerns the incomplete description of the resulting disable, not that quantity.

**KEEP the four artisan creation credentials, six creation bands, native casting/attack/save/task routes, structural/chassis distinction, actual reserve histories, repair/service separation, and bounded class-interface eligibility.** No feat is activated or approved by these recipe candidates. No class device becomes a crafted device, or vice versa, by naming alone.

## 3. Exhaustive finite correction list

### AEX-01 — Failure recovery uses the input entitlement, then the surviving-material cap

**Affected:** all 167 recipes, including the Failed recovery used by singleton creature-output Flawed results. **Locations:** I/P card `operational.paragraphs[label="Retention and failure"]`, their manuscripts, and the common failure explanation. **Controlling earlier rule kept:** AC-04 and the existing crafting failure rule; E-05 already states the intended cap.

Every card currently says **“25% of genuinely remaining consumed non-catalyst quantities … capped by actual remains.”** That can apply the percentage to the remainder instead of computing the quarter-input entitlement and then capping it. It is inconsistent with the clearer shared-guide formulation.

**Replace that recovery sentence with:**

> On Failed creation, for each eligible exact consumed non-catalyst input identity, recover at most one quarter of its fixed consumed-input quantity for this batch, capped by the eligible amount actually remaining from those same inputs, and rounded down once to that identity's legal source-unit precision. Do not take one quarter of the surviving remainder. Previously returned, forfeited or lost quantities and unrelated stock cannot fund this recovery.

Use the explicit common equation:

`recovered_i = u_i × floor(min(Q_i / 4, R_i) / u_i)`

Here `Q_i` is that failed batch's fixed eligible consumed-input quantity for the exact identity; `R_i` is the eligible quantity actually surviving from those same inputs; `u_i` is its existing legal precision. Preserve occurrence membership and the existing rules for grouping genuine identical inputs. Neither money nor a source bill authenticates surviving matter.

**Boundary:** recipe-480 has five source units of Preservation treatment at 0.1 lb each. With two eligible units surviving, return **1.25 source units / 0.125 lb**, not 0.50 units. With only 0.60 surviving, return **0.60 units / 0.06 lb**. Three indivisible inputs still return zero. All catalyst exclusions, retained-tool returns, body returns, source division permissions and terminal-waste rules remain unchanged.

### AEX-02 — Complete Rune control/end conditions and the public known-trap disarm action

**Affected:** the ordinary Rune procedure for **recipe-396–432 and recipe-664–666**, the eight Binding cards below, and the eleven Tinkering traps below. The custom recipe-667 activation remains RC-10, not ordinary plate arming. **Locations:** GP's Rune Carving and Tinkering sections; corresponding active JSON/manuscripts. **Earlier rules kept:** RC-01, RC-02, RC-04 and TI-02.

The public guide substitutes **“genuinely relevant INT tool check”** for the specified Rune examination credential, omits explicit known-setter disarm cost and no-automatic-rearm wording, and omits covering/Breaking from Binding termination. The Binding card paragraphs repeat the incomplete end-condition list. The public trap procedure gives the unfamiliar disarm procedure but not its setter's one-Action alternative.

**Use this controlling Rune control wording:**

> A ground plate that is moved, rotated off its declared working face, wholly covered, Broken, incomplete or suppressed cannot trigger. Restore an invalidated ground trigger only through the actual one-Action manual arming procedure on its cleared eligible square, followed by the existing next-regular-start or six-second delay; merely uncovering, repairing or unsuppressing does not rearm it. A capable authorized setter can disarm their accessible plate with an Action; physically removing it uses its actual item interaction afterward. These ground-trigger rules do not replace the specific direct-touch Healing procedure or the separate attuned-Ward duration procedure.

**Replace the Rune inspection/disarm passage with:**

> With safe access within five feet, one active minute permits an INT (Arcana) or INT check using Runecarver's tools against the original recipe creation DC, using normal Core task shifts collapsed to success/failure. Apply only the actual applicable proficiency contribution. This examination reveals supported operating type/trigger, not donor lore, and failure grants no repeat on unchanged evidence. Disarming an unknown accessible Rune requires actual Runecarver's-tools proficiency and tools, one active minute, and that source DC. Failure leaves it armed; it discharges only if an actual eligible entry/touch event occurs, not merely because the check failed. An unrelated tool proficiency is not a substitute.

**Binding IDs:** recipe-396, 400, 401, 405, 412, 413, 426, 665. Replace their abbreviated termination sentence, and GP's corresponding sentence, with:

> Moving the target completely outside the original trigger square/volume, or moving, covering, suppressing or Breaking the original plate, ends this particular Binding restraint. Restoring the plate does not resume that ended restraint, refund its charge or rearm its ground trigger. Other independent restraints remain separately governed.

**Trap IDs:** recipe-585, 588, 592, 598, 599, 601, 605, 609, 610, 613, 619. Add the missing public operative sentence:

> A capable authorized setter can safely disarm their accessible trap with one Action. This is distinct from the unfamiliar-trap procedure: trained thieves' tools or Tinker's tools, the appropriate DEX/INT method, one active minute and the printed trap save DC. Neither route grants free movement, rearming, servicing or replenishment.

**Required boundaries:** covering or Breaking ends a Binding effect; restoration does not resume it. Removing suppression from an invalidated ground plate does not immediately produce a trigger. A still-unexpired attuned Ward remains governed by RC-08's different suspension/resumption rule. A non-Runecarver's tool does not gain the Rune inspection proficiency by being called relevant.

### AEX-03 — Automaton encounter service starts with actual operation

**Affected:** all 18 ordinary automata: **recipe-586, 587, 589, 590, 593, 594, 596, 600, 607, 608, 611, 612, 615, 616, 618, 620, 622, 684**. **Locations:** GP's Service units paragraph and P's embedded guide; make the card/binding descriptions equally explicit. **Earlier rule kept:** TI-05.

The public sentence **“Spend one when a genuine encounter starts”** can debit a stored or otherwise unoperated machine simply because combat began.

**Replace it with:**

> First actual operation of this automaton in a genuine encounter spends one service unit and opens that encounter's paid operating block, lasting at most ten elapsed minutes from that operation. Mere encounter start does not debit a stored or otherwise unoperated automaton. Ordinary idleness before a block starts spends nothing and grants no active behavior. Continuing operation beyond a block's expiry needs another paid block; a distinct genuine encounter has its own service requirement. Preserve TI-05's transition from an operating noncombat block into a genuine encounter, its no-refund/no-clock-pause rules and its physical-identity history.

Do not change the explicit existing noncombat-to-combat transition or convert an already paid block into free operation. No service cost is assessed per attack inside the paid block. Zero unspent units does not invalidate the remainder of a legitimately paid block; it prevents starting the next unpaid one.

**Boundary:** a packed recipe-684 present during an encounter but never operated loses no service unit. Its first actual operation starts the paid block. Later suppression consumes elapsed block time without refund or extension. Recipe-686 remains on its separate winding clock.

### AEX-04 — Routed Dissonance disables triggers and other active functions too

**Affected:** all 43 TI recipes when they satisfy TD-08's actual active-device predicate; their 26 public instances require the same public operating rule. **Locations:** GP Tinker class interfaces / P `operatingGuideText`, and any condensed active TD-08 description. **Earlier rule kept:** TD-08, including the already corrected two-to-one quantity.

Replace **“The routed disabled state stops applicable movement, attacks and device aura functions”** with:

> The routed disabled state prevents movement, attacks, auras, triggers and every other active device use. A routed trap cannot discharge, and a routed utility cannot provide its charged task benefit while disabled. Existing durations and paid service/winding clocks continue. Clearing the disable requires its existing specifically authorized completed removal procedure; it does not refill charges, service, RP or Refrain, erase expenditures, or grant a queued activation.

Retain **once per genuine short rest, Bonus Action, up to two current Dissonance, one own active qualifying device within 30 feet**. Retain the origin-Tinker's rest rule, actual Field Repair and paid ten-minute removal procedure. Apply AC-06's normal distinction between blocked invalid declarations and already committed costs; a later disable does not refund an earlier legitimate expenditure.

**Boundary:** routing into an armed trap blocks its later trigger rather than merely preventing an attack-roll action. Routing into a utility participating in a live check removes its active benefit. Another owner's rest does not clear the originating Tinker's disable.

### AEX-05 — TI-device size and load limits are conjunctive

**Affected:** **recipe-595, recipe-602, recipe-614, recipe-617** and their shared TI-device model; public counterparts are 595 and 602. **Locations:** I's active TI-device model override, P `bodyModels["TI-device"].model`, the cards' Complete output bodies paragraphs and corresponding catalogues/manuscripts. **Earlier rule kept:** B-04's actual operating limits.

The model string says **“jaws admit 4x4x2 inches or 2 lb”**, while the complete body text correctly requires both limits.

**Canonical active model value:**

> Hand-operated bench measuring/calibration box. An admitted workpiece must both fit the actual 4 × 4 × 2-inch jaw space and weigh no more than 2 lb. These are simultaneous limits, not alternatives. No general cargo space.

Retain the historical `sourceAuthoringProfile.model` and original register unchanged. Add/use a separately identified active `operationalModelDescription`, as already done for the trap clarification, and project that active value consistently.

The 15-gp reference, five-pound empty body, HP/AC, overall envelope, original frame/gauge/calibration primaries, operating hands and repair rules do not change.

**Boundary:** an oversized half-pound workpiece fails; a fitting three-pound workpiece fails; a genuinely fitting workpiece of at most two pounds can qualify. Passing only one limit is insufficient.

### AEX-06 — The Warding trigger field must include actual saving-throw events

**Affected:** all 19 wards: **recipe-398, 402, 403, 404, 406, 407, 408, 409, 411, 414, 417, 419, 420, 421, 423, 424, 428, 431, 664**. **Locations:** I/P `cards[*].operational.useBinding.trigger`, plus any trigger summary derived from it. **Earlier rule kept:** RC-07.

The active compact field currently says **“attuned bearer is targeted.”** The complete procedure correctly also admits an actual saving throw, including an area event which need not target that bearer individually.

**Replace the active trigger value with:**

> An attack legally targets the attuned bearer, or an actual event requires that bearer's saving throw, including an area effect. The capable bearer must declare and spend one Reaction and one charge before the initiating attack or saving throw is rolled.

Preserve the original source register's historical abbreviated field. The active operational binding is the original binding plus this named correction, not an unauthorized rewrite of the source. No change to B, C, positions, attunement, defenses, duration or suspension rules.

**Boundary:** an incoming area effect requiring a DEX save permits the pre-roll Reaction. Mere inclusion in an effect that requires neither an attack roll against the bearer nor their saving throw does not. Seeing the roll and then invoking the ward remains illegal.

### AEX-07 — Correct operational section locators and expose the actual consultation boundary

**Affected:** the explicit groups below. **Locations:** their Effect and operation paragraphs in I/P and MI/MP, plus the public guide's source-section cross-reference legend. These are corrections to operative locators, not changes to protected source citations or source-book paragraphs.

| Affected recipes | Current defect | Replacement wording/reference |
|---|---|---|
| All 22 scripts: 471, 473–475, 480–484, 487–492, 495, 496, 499, 501, 502, 504, 505 | Consultation points to SC-04, which governs copying | **“The research bonus requires the actual relevant lead consultation under SC-05. SC-01–05 and SC-10 govern the full procedure.”** |
| Five references: 476, 486, 498, 500, 672 | “Full boundaries” omits SC-05 | **“SC-04, SC-05, SC-07, SC-08 and SC-10 provide the applicable full boundaries.”** |
| All 19 wards listed in AEX-06 | Six-second marker incorrectly attributed to RC-07 | **“Outside initiative use the RC-08 six-second marker.”** |
| Eight Binding cards listed in AEX-02 | Placement reference omits RC-01 | **RC-01–04** |
| Six Explosive cards: 397, 410, 418, 429, 430, 666 | Placement reference omits RC-01 | **RC-01–03 and RC-05** |
| Seven Healing cards: 399, 415, 416, 422, 425, 427, 432 | Ground/direct-touch boundary reference omits RC-01 | **RC-01–03 and RC-06** |

Retain SC-05's full scope explicitly in the public Research and navigation paragraph:

> These research/navigation bonuses apply only to their genuinely relevant recorded subject and actual eligible information task. They do not improve attacks, saves, spell DCs, spellcasting, unrelated checks, manufacture or repair. The item's own authoring, copying or encoding, and creation of a new bonus-granting reference from that same item, receive no self-production bonus. Genuine relevant formula research remains separately eligible without guaranteeing discovery.

Provide a compact public locator legend mapping referenced AC/EN/RC/SC/TI/TD and body-section IDs to the corresponding **already supplied public procedure headings**. For SC-08, expose only the ordinary Language Insight procedure relevant to public items, not the private Lexicon membership or custom dossier. Do not resolve public references by linking the unfiltered internal verdict, private body list or hidden annotations. The complete ordinary rules must remain in the public guide itself.

## 4. Public component envelope: KEEP

The submitted advanced envelope has **343 component occurrences**, not the previous gathering envelope's counts. I independently reconstructed **100 authorized supplemental profile occurrences** and **243 withheld supplemental profile occurrences** from the source material visibility/matching rule. This preserves all 343 printed names, quantities, roles and consumption flags, along with their operational precision and separate physical-occurrence requirements.

**No recipe-critical audience correction requires publishing any of those 243 withheld dossiers.** Each withheld occurrence is indexed on its actual recipe and the player text explicitly requires the Director to verify the exact required stock before commitment; it does not authorize a wildcard, cheaper name match or free material. Internal matching retains the complete source identity, quantities, age and actual physical history.

The 100 admitted supplements are separately nested public material records. Their material-catalogue `category` must not be flattened into or overwrite the preserved recipe occurrence's different category namespace. They disclose neither a new drop roll nor a donor-access right. Missing public provenance for further metadata remains fail-closed. An input amount needed in actual play must be verified through the complete internal formula, not invented from the public preview.

Keep all **100 public recipes / seven restricted / 60 Director-only**, the **15 public body variants**, all 50 eligible host templates, and the seven withheld custom/private body variants. All600 original book paragraphs remain immutable. The audience defects in this submission concern the operating rules identified above, not permission to export private source dossiers.

## 5. Verdict on all 37 qualitative sequences

**KEEP the expected adjudications for W-01–W-19, E-01–E-16 and E-18 under their stated premises.** They correctly separate genuine histories, source values, paid commitments, interpretation and runtime evidence. E-05's quarter-input/surviving-cap expectation is made explicit by AEX-01; its intended result is not changed.

**E-17's completeness assertion is not satisfied by the uncorrected public guide.** Retain it as a required expectation, then satisfy it by applying AEX-01–07 and rebuilding the whole public envelope. Do not mark that assertion passed merely because the current public JSON exactly repeats the same defective guide wording.

The semantic review also keeps the boundaries exercised by the 22 body rows: genuine geometry/load/handling, original primary constituents, simultaneous reserve exclusivity, fixed chassis type, and no free stock. AEX-05 removes the one conflicting TI-device model string; it does not relax those boundaries.

These are adjudications of the supplied test premises, **not claims of 37 executed state-machine tests**. The correction package includes a finite focused-regression specification for checking the identified seams. No additional preliminary-source queue is created.

## 6. Conditional promotion authority and required receipt

**All 167 candidates and all 100 public projections may be promoted as reviewed authored-operational recipes after the following finite work is complete, without another generic conference:**

1. Apply **AEX-01–07** as named, versioned operational corrections. Preserve original sources, book paragraphs, the final13-file source package, ADV-EDIT-01 and the class/source records. Do not change recipe membership, printed mechanics, source values, nulls, consumed flags or private visibility to force a pass.
2. Regenerate/compare the full internal and public JSON, all eight recipe manuscripts, shared guides and body catalogues. Every corrected operational paragraph must equal its own rendered manuscript, and every player-visible behavior must match the applicable internal behavior. Historical source summaries can remain historical; they must not compete as active contradictory rules.
3. Rerun all three submitted validators and retain their coverage. Where an old assertion equates a historical abbreviated field with its newly corrected active field, replace it narrowly with **preserved original plus the exact named correction**. Do not disable the assertion or weaken source preservation. Maintain the detailed manufacturing, structural, chassis, quote, pack, primary-member and 37-case coverage; raw check totals alone are not the acceptance criterion.
4. Pass the finite focused checks for the seven corrections: input-entitlement versus surviving cap; Rune invalidation/termination and known/unknown disarm distinction; first actual service operation; all-function routed disable; simultaneous TI-device limits; area-saving-throw Ward eligibility; and correct/publicly resolvable section references. Record corrected file hashes, the correction application map, unchanged protected-source hashes and explicit semantic dispositions, distinguishing numeric/static checks from authored sequence expectations.

The receipt can close this exact-review gate under the authority above. No resubmission of the same original sources or another full source-authoring verdict is necessary. A change beyond these named corrections, a new contradictory source or an unresolved failure should return only the affected exact material and failed condition—not restart a generic conference.

Until the corrections are applied and that receipt exists, counts remain **520/687 recipes and 333/433 public**. After completion under this conditional authority, they become **687/687 recipes and 433/433 public**. That means the recipe authored-operational review count is complete; it does not mean all game systems, spells, classes, feats, expedition flows or runtime are complete.

There is **no remaining general source question blocking correction and promotion of these recipes**. Particular operations still require their real spell payload, exact stock, lawful custody, actual language/evidence, compatible device protocol, body geometry, supported breach target and safe containment. Unsupported particular operations remain unavailable under the already authored predicates rather than forcing another preliminary recipe conference.

**No class/feat promotion, runtime certification, human-balance approval, source deletion, publication/push authorization or cosmology interpretation is granted.** The owner's final whole-game flow confirmation still precedes an authorized GitHub push; verified remote commit still precedes careful cosmology review.
