# EX58-EXACT-2026-10-11 — Complete exact-candidate verdict

**Disposition: EXACT CORRECTION REQUIRED — one bounded issue, EX58-X01.**

The complete expedition, transport, social and reputation candidate is accepted **as an authored operational playtest candidate, conditionally upon the exact EX58-X01 amendment and finite fulfillment checks below**. The submitted uncorrected EX-W13 example is not accepted. No additional source conference or unchanged full resubmission is required to fulfill this verdict.

This is not the final whole-game agreement, a gameplay/application-runtime certification, a human teaching or balance finding, or a promotion of comparison class, spell or feat records.

## 1. Immutable submission and actual inspection

Submission: `DD_EX58_Complete_Exact_Candidate_01.zip`, **47,836,562 bytes**.

Archive SHA256:
`ab16fff6b7e80d755a6b4d1971c9d7e8fbe20442a1876178073b7f546edd946a`

Outer `EX58_EXACT_FILE_MANIFEST.json` SHA256:
`d79469ef1ad372fbe156cef094c59ecb9bfae827b389b3041de3f5c6b74a03e5`

The archive contains **419 payload files and the outer manifest**. I independently matched every declared payload's actual size and SHA256, and verified the **304 unchanged V3 payloads** against their preserved original manifest. The original V3 ZIP and historical deliveries are retained. The source extraction was not edited. A separate validation copy and a separate reference-amended copy were used.

I read the complete current Player and Director books and both complete candidate objects, all six current chapters and all58 directions; the190 actual chapter examples; all29 complete transport profiles and four auxiliaries; the full21-event expedition, all15 instantiated contract families, actual stock/fuel/turn/provider/service/financial/rest records; all28 instantiated boundaries; and all24 original social proposals with their actual candidate adjudications. The complete current reading object, rather than an old component's “remaining examples” notice, controls completeness.

I also compared the actual called governing procedures, the current corrected source register/contracts/conflicts, the58 original source directions, the20 background clauses, the12 source reputation probes and their preservation dispositions, and the selected class/spell/crafting interfaces. The complete17 class envelopes/1,223 cards and all44 faction records remain preserved source collections; their inclusion and source equality are not new full-catalogue approvals. The94 selected class-card comparisons and specifically called Mage/Dragoon/Tinker, completed spell, Scribing and recipe procedures were considered within their actual interface scope. Uncalled setting explanations and cosmological meanings remain outside this review.

All requested current candidate files were accessible. There is no missing candidate chapter, transport option, EC contract family, boundary or social case preventing this verdict.

## 2. Evidence: reproduced, independently checked, and semantically assessed

The supplied assembly validator reproduces **1,214 passing checks, zero failures** in the working copy. The submitted report contains1,213. The sole added passing check is the now-accessible original local `README_EXPEDITION_INTEGRATED_V3.md`; it is not a new rule test. The script itself was not changed; its root paths were rebound to the working copy.

The separate reviewer script performs **1,584 checks** of immutable/working bytes, complete projection/rendering, current bindings, coverage, source class references, exact rational quantities, declared chronology/stock/fuel/transactions/rest, raw fixtures and links. On the frozen candidate it records **1,582 passes and two failures**, both belonging to EX58-X01: the two actors' RP pools exceed their actual source maxima. On the separate reference-amended candidate it records **1,584 passes and zero failures**.

A further **435 strict amendment checks** pass on that reference tree, including complete-byte comparison of every payload against either its original hash or one of the eight exact descendant hashes, the complete corrected case, eight deliberately corrupted resource fixtures, and unchanged consequences. **411 other payloads remain byte-identical**, including all304 V3 payloads. The33 actual combined-book links/anchors resolve.

These executed checks are not a game engine. They do not execute all spell/class hooks, adjudicate arbitrary campaign histories, authenticate people/providers/geography/ownership/saves/dice, or establish human usability or balance. The semantic judgments recorded here and in the complete disposition register are Director-side assessments of the supplied authored rules and synthetic premises, separately identified from those calculations.

## 3. EX58-X01 — Correct EX-W13's two RP pools

### Finding and retained authority

EX-W13 names a **level3 Mage** and a **level8 Dragoon**, while both currently start at10RP.

The submitted `docs/mechanics/classes/mage.md`, “Advancement and resources,” gives **Mage3 maximumRP8**. The submitted `docs/mechanics/classes/dragoon.md` gives **Dragoon8 maximumRP7**. The fixture supplies no actual maximum-increasing feature, effect or exceptional resource source.

The movement and spell comparison remains useful and correct after using legal pools. **Keep the class tables, class levels, spell permissions, prices and all movement/effect procedures.** Do not invent a higher pool, increase a class level, promote a feat, change a spell price, or turn the Dragoon's Dissonance reduction into an RP discount.

### Complete replacement premise

Replace EX-W13's entire `actualSyntheticPremises` string with:

> A level-8 Dragoon has genuinely acquired Featherstep and starts this fixture at 7/7 RP. A level-3 Mage ally starts at 8/8 RP and pays the actual 3 RP to cast Swiftness, leaving 5/8 RP, then continues holding its concentration. Swiftness legally raises the Dragoon’s walking Speed from 30 to 40 for its minute. On the Dragoon’s later own turn, Featherstep’s normal 2 RP is paid from 7 RP, leaving 5/7 RP. The two actors retain their own concentration and resource histories. No pending feat or unstated increase to either RP maximum is used.

### Exact field replacements

All pointers below are relative to the **EX-W13 case object**:

| Field | Submitted | Corrected |
|---|---:|---:|
| `/records/ongoingEffect/RPBefore` |10|8|
| `/records/ongoingEffect/RPAfter` |7|5|
| `/records/ownTurn/RPBefore` |10|7|
| `/records/ownTurn/RPAfter` |8|5|

Thus the Mage pays **8−3=5RP**, while the Dragoon pays **7−2=5RP**. Retain Swiftness's actual one-minute window, initial components/target and independent Mage concentration. Retain the Dragoon's Speed40, dismount cost20, actual own movement20, remaining movement0, Momentum+1, base Dissonance gain1 reduced by1, final Dissonance2, and normal Featherstep2RP. All existing `expectedOutcomes` remain unchanged.

This is an **example/resource-premise correction**, not a NEW game rule or a reversal of a source-authoring direction.

### Every current representation affected

The five current JSON case views are:

| File relative to archive root | Case pointer |
|---|---|
| `DescentReviewChanges/ReviewBible/data/public/expedition_candidate/boundary_records.json` |`/cases/12`|
| `DescentReviewChanges/ReviewBible/data/director/expedition_candidate/boundary_records.json` |`/publicEnvelope/cases/12`|
| `DescentReviewChanges/ReviewBible/data/public/expedition_candidate/complete_candidate.json` |`/components/boundary_records/cases/12`|
| `DescentReviewChanges/ReviewBible/data/public/expedition_candidate/complete_candidate.json` |`/reading/boundaryCases/12`|
| `DescentReviewChanges/ReviewBible/data/director/expedition_candidate/complete_candidate.json` |`/completeComponents/boundary_records/publicEnvelope/cases/12`|

Apply the full premise replacement and four numerical replacements identically at all five views. `EX58_X01_CORRECTIONS.json` contains the25 concrete guarded JSON operations and complete original/replacement strings.

The four Markdown mirrors in `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/` are:

- `EXPEDITION_BOUNDARY_WALKTHROUGHS.md`: replace its one EX-W13 premise paragraph.
- `EXPEDITION_BOUNDARY_RECORDS.md`: replace its one complete EX-W13 record.
- `EXPEDITION_PLAYER_BOOK.md`: regenerate the complete Player rendering from the corrected public object.
- `EXPEDITION_DIRECTOR_BOOK.md`: regenerate the complete Director rendering from the corrected internal object.

These are **eight actual candidate files**, not eight independent mechanical corrections. Refresh only the two current boundary-component size/hash bindings in the current internal complete object's `componentBindings`. Preserve the original complete object, original manifest, sourceVerdict provenance, original source outline and previous receipts as history. Do not edit the internal `completeOriginalBoundaries` copy to pretend this correction was old source text.

The frozen boundary-builder script is also historical. An actively maintained descendant of that generator must not restore the four oldRP literals or old premise; constrain its EX-W13 constructor to this same replacement and record that generator descendant separately. No unrelated generator rewrite is authorized or required.

The package includes the **complete corrected EX-W13 reference**, exact pre-label descendant hashes, and a tested standard-library script that creates a separate reference tree without writing to the submitted input tree.

## 4. Exact disposition of the fifteen acceptance requirements

### ECX-01 — Authentic version and source preservation

KEEP — Authentic archive/outer manifest, 419 payloads and all 304 V3 payloads are preserved; historical versions and unadopted proposals remain history.

### ECX-02 — Complete player and Director reading path

KEEP complete reading path; regenerate the same full envelopes and four named rendering mirrors after EX58-X01. No missing chapter is inferred from historical component notices.

### ECX-03 — All transport

KEEP — all 29 transport rows and four auxiliaries, known source fields and NEW physical/operating additions are present and evaluated.

### ECX-04 — Clock/work/rest

KEEP — global clock, actual parallel labor, rest/debt, equal-time endpoints and source-specific interruption; FLOW-C01 and FLOW-C02 are accepted synthetic clarifications.

### ECX-05 — Supply and matter

KEEP — actual Supply, full flask/empty tare separation, continuous original oil depletion, finite forage and receiving/cargo obligations.

### ECX-06 — Route and extraction

KEEP — route, Pressure, modified severity, cadence/coalescing, bounded secondary outcomes and declared actual access.

### ECX-07 — Encounter and transport actors

EX58-X01 REQUIRED — Actor/transport procedures are retained. EX-W13's two starting RP pools violate the selected class maxima; apply the four numeric replacements and full premise.

### ECX-08 — Valuation and claims

KEEP — valuation domains, authentic finite quote premises, source-specific sponsors, greater-of assay liability and cumulative claim arithmetic.

### ECX-09 — Social source clauses

KEEP — all twelve SO directions and all twenty-four scenarios retain promised Success, voluntary costly agreement, Help/communication and authority limits.

### ECX-10 — Standing preservation

KEEP — all original 44/20/12 comparison collections and complete raw/version/earned-history boundaries; no real-save migration.

### ECX-11 — Faction work and clocks

KEEP — at most three watched factions, coalesced real checkpoints, actual work/report reception and bounded rival clocks.

### ECX-12 — Services, instruction and continuation

KEEP — paid services/learning/Scribing/repair/rest and advancement remain different procedures; no visit completes unfinished work.

### ECX-13 — Public envelope

KEEP — full public projection reconstructs correctly and does not disclose internal dossier fields; repeat whole-envelope parity after EX58-X01.

### ECX-14 — Finite examples and evidence labels

EX58-X01 REQUIRED — the 21-event flow, 190 chapter examples, 24 social scenarios and 27 other boundaries are accepted as authored expectations; EX-W13 needs only the named resource correction.

### ECX-15 — Scope and gate

KEEP — finite conditional authored acceptance below; no unrelated option, runtime, human, whole-game, delivery or cosmology gate is closed.

## 5. Integrated flow: FLOW-C01 and FLOW-C02 are accepted within this example

**KEEP FLOW-C01.** The supported thirty-minute stops at departure and hour12 are actual reserved stationary intervals. The second includes the previously counted one-minute refill. Added time is `1,800+1,800−60=3,540 seconds`, not3,600seconds plus another refill. This is a specific worked itinerary, not a universal thirty-minute meal rule.

The two travel legs retain28,800 actual moving seconds each. The revised encounter, loading, return and extraction records remain in one coherent elapsed chronology. Haven entry is **62,592 seconds after departure, 17:23:12**. The first actual safe Rest completes at **104,592 seconds, 29:03:12**. The older source outline stays historical.

Actual human and mule feeding/watering, four people's parallel container work, seven one-minute lamp refills, continuous48-hour lighting and the stock/cargo history reconcile. Eight original pints supply the declared lighting, not eight plus a free backup allotment. The final original flask splits into7/360pint for the backup and353/360pint for the final main-lantern interval; neither portion is counted twice. Original empty-flask mass remains2lb, and next-descent fuel is separately bought/handled stock.

**KEEP FLOW-C02.** Arin holds Expedition Leader and Quartermaster, Bea Routekeeper, Cora Claimant of Record, and Dane Surgeon. The assignment gives no proficiency. Bea remains a walking driver; the mule is a distinct real actor paying its own movement, not a ridden extension of Bea's turn. The withdrawal lane, cart/puller clearances, actor positions, paid actions, single threat and actual gate closure form a feasible declared synthetic sequence. No additional movement, opportunity attack or vehicle-native turn is inferred.

The named Haven clerks, buyer, lodging/stable providers, lamp attendants and animal carers have actual schedules and declared permissions. Their contracts do not create extra expedition combatants or waive the12-character cap. The genuine-return and global faction checkpoints observe actual work and received evidence; the early return does not finish the archive worker's remaining hours or duplicate the later checkpoint.

Rest Debt opens at the missed prospective slot's completion, not at arbitrary Haven arrival, and clears when the first safe Rest actually completes before its debt deadline. The first Rest contains27,840seconds of sleep after its limited light activity. The later eight-hour Rest ends only68,208seconds after the first completion, so it is **not** a second beneficial long-rest resource reset.

The same history also supports the settlement:

| Quantity | Exact copper |
|---|---:|
| Actual gross sale |12,000|
| Tax |600|
| Mandatory inspection, already paid once |200|
| Net basis for the20% sponsor |11,200|
| Sponsor payment |2,240|
| Net after those deductions |8,960|
| Other unique operating costs |2,020|
| True profit |6,940|
| New reserve |2,000|
| Distribution, four×1,235 |4,940|
| Cash after distribution |5,000|
| Actual next-stock procurement |520|
| Cash before next descent |4,480|

Inspection is not deducted twice from the cash ledger. The2,000cp reserve is earmarking, not an additional payment;1,480cp of it remains in cash after the520cp purchase. The next inventory is not the old depleted stock relabeled or a second deduction from the completed episode's profit. The insurance example records the real earlier premium and zero payout because no actual covered loss is asserted.

These findings accept the stated synthetic circumstances. They do not certify that a campaign has these providers, terrain, objects, legal powers, stock or purchases.

## 6. Transport, social, reputation and service decisions retained

**All29 transport profiles and four auxiliaries: KEEP.** Their complete current physical models, action/control/turn requirements, capabilities, capacity/geometry, actual force/crew conditions, prices, custody, fuel/service and restoration distinctions were reviewed. New values remain labeled NEW authoring, not retroactively sourced facts. The nine living mounts, five drawn vehicles, tack/feed/stabling/service records and six watercraft retain their own identities.

The source Player Sled and separate Core Dungeon sled do not merge. A Hauler's moving-time fuel and40-moving-hour service counter do not imply unattended operation, a Tinker-class device, a charge refresh or free refill time. The source-defined one-minute refill still requires actual stock, access and labor in a real use. Its focused five-day service example does not waive that rule or claim to instantiate every ordinary daily action. Barding does not repeat the armor multiplier. Actual original-member repair and sinking/shoring/towing procedures do not restore erased material, reset custody or turn living healing into body repair. Quotations for specialist/teleport transport remain quotations until the actual spell/route/provider procedure is available.

**All12 SO directions and all24 proposal scenarios: KEEP their authored candidate dispositions.** The candidate distinguishes a possible uncertain request from willing cooperation and impossible demands, honors the announced successful outcome, and treats a costly agreement after failure as a separate accepted offer. It preserves native Core/opposed/spell procedures, actual language channels, Help expiry and changed-evidence retries. Standing, Performance, Insight, Charisma, Charmed and intimidation do not confer property rights, universal obedience or hidden knowledge. Player consent and safety remain distinct from fictional agency.

**FL-23 and all six RP-A directions: KEEP.** The adopted−3..+3 policy and scene-opening signed arithmetic are consistent; overflow remains history rather than a bank. Historical eleven-band/five-band/modifier data and exact source/version identifiers remain preserved, not silently remapped. Unknown keys, values, spelling/types, explicit zero, absence, null, false, duplicate keys and parsing failures retain their raw record. There is no real-save migration.

**Cult Escapee is explicit and correct in this candidate:** the source authorities clause is Disliked, yielding−1 under the adopted initialization, not runtime+1. For an existing record, only a provably wrong initial contribution can be corrected and the actual later earned events replayed; an unversioned saved number is not a licence to overwrite final standing. All20 background clauses and44 institution identities keep their source-specific scopes. The registry is not permission to delete an unknown campaign institution or publish a private dossier.

**Faction actions, finite rival clocks, Haven work and services: KEEP.** A global24-hour boundary or genuine return is a checkpoint, not free actor labor. Real projects, reports and blocked thresholds persist. Research, instruction, SC08 insight/consultation, ordinary learning, recipe creation, bodily care, repair and rest use their completed source procedures, not a generic Haven-visit exchange. No pending class/spell/feat is promoted through one of those comparisons.

**EX58-EDIT-01 and EX58-EDIT-02: KEEP fulfilled.** The five offices and corrected greater-of assay liability are in the operative derived directions. The knowing-holder total is the greater of10%of confirmed false face or actual applicable assay/remint fees; fees are allocated inside that total, prior payment is credited once, and the remaining fine is only the excess. No old “10%cap” or invented Lorekeeper office is reinstated. Innocent/unproven-intent and real-authority boundaries remain intact.

The public envelope contains the complete allowed operational reading material and source-printed background clauses, not the complete private faction/class/internal-source layers. General institution names and ordinary synthetic situations do not authorize publication of private memberships, backers, resonance keys, hidden plans or cosmological explanations. Full-object projection and full-book rendering equality are retained, not merely selected sentence matches.

## 7. Complete58-direction disposition

The following are exact assessments of the current operative directions. TR-03–06 keep their procedures; their shared EX-W13 resource fixture receives the single named correction.

**FL-01 — One authority map:** KEEP the explicit precedence map and preservation of older source versions. No fulfilled domain is reopened by an old preparation label.

**FL-02 — Roster, offices and real teams:** KEEP the twelve-character cap, real actors and five actual offices. EX58-EDIT-01 is correctly represented; offices neither confer proficiency nor multiply time.

**FL-03 — One elapsed campaign clock and Watch accounting:** KEEP one elapsed clock, half-open intervals, compatible parallel labor, two productive Watches, prospective Rest Debt, exact interruption and benefit lockouts.

**FL-04 — Supply is coverage of real obligations:** KEEP Supply as actual food/water/fuel/sundry coverage, with source-specific needs and no automatic fuel consumption or abstract replacement inventory.

**FL-05 — Procurement, storage and finite magical support:** KEEP finite procurement, actual containers/tare/capacity and separate nutrition, light and magical permissions. Stocks and preparation do not reset origin or age.

**FL-06 — Forage, pooled Sustenance and depletion:** KEEP predeclared finite forage/Sustenance allocations, actual work and nonoverlapping reserve output. A successful forage does not create oil or duplicate prior material.

**FL-07 — Finite camps and independent safety:** KEEP the authored camp bodies, mark totals, costs, actor labor and storage limits; building a camp does not automatically establish safety or heal gear.

**FL-08 — Pressure event ledger:** KEEP cause-bound Pressure, current cohort history, cargo high-water accounting and bounded real reductions. Do not charge the same disclosure or Watch cause twice.

**FL-09 — Total d6 severity and bounded complication processing:** KEEP the full modified-d6 severity rule, Pressure0/6 endpoints, equal-result qualification and once-per-root secondary processing with actual time/consequences.

**FL-10 — Route progress and mapping:** KEEP route quality, Mapping, access and convoy pace as separate inputs. Progress does not also award free mileage, time or travel through a blocked route.

**FL-11 — Forced march and travel interruption:** KEEP actual forced-travel intervals, declared extra supplies and source-specific interruption; no forced-march roll erases travel, debt or physical limits.

**FL-12 — Extraction episode and cargo admission:** KEEP exact cargo identities, classification, priority, actual burden and extraction-episode reservation. Class is not pounds, and pricing creates no cargo.

**FL-13 — Finite extraction checkpoints:** KEEP route-specific checkpoint cadence and coalesced coincident triggers; actual one-minute checks and partial exposed Watch settlement occur once.

**FL-14 — Failure choices, elapsed delays and cargo response:** KEEP the declared alternative failure consequences, eight-hour delays, real risk-response work and bounded threats. A risk record is not automatic loss or death.

**FL-15 — Retreat: one bounded chase round:** KEEP the source-native retreat check, own actor budgets, one paid threat per chase round and three-before-three termination; a 3/3 tie is not escape.

**FL-16 — Encounter estimate and actual participants:** KEEP participant-based N_eff and encounter estimates distinct from roster and physical carriers. Calibration numbers do not establish observed balance.

**FL-17 — Transport and inventory integration:** KEEP cargo/support/handling and custody constraints shared with transport; do not replace actual pounds, geometry or provider work with a Load label.

**FL-18 — Integrity retained as history, structural HP operative:** KEEP operative structural HP and retained legacy Integrity. An existing HP record is not healed by reinterpreting an older Integrity value.

**FL-19 — Haven intake, evidence and disposition:** KEEP actual Haven actors, intake, inspections, provenance, custody and scheduled service intervals. Authority and completed work are not inferred from a title.

**FL-20 — Valuation has one correct domain:** KEEP separate equipment, crafted-item, material and artifact valuation domains; real finite buyers and missing artifact inputs stay explicit.

**FL-21 — One gross-to-net ledger and one rounding per transaction:** KEEP one gross-to-net ledger and final-transaction rounding. Already paid mandatory costs appear once; negative estimates do not invent credit or debt.

**FL-22 — Claims, sponsors, taxes and finite insurance:** KEEP distinct sponsor/policy sources, actual taxable brackets, cumulative partial claims and one deductible per loss episode. No duplicate payout.

**FL-23 — One standing policy, preserved originals:** KEEP one operational standing policy, signed scene accounting and lossless raw/source-version records. Do not turn the refinements into independent scales.

**FL-24 — Haven work, services, instruction and recovery:** KEEP each service, learning, research, Scribing and condition-care procedure's actual hours, prerequisites and costs. Haven entry is not completion.

**FL-25 — Coin, crime, labor and rescue preserve real status:** KEEP the EX58-EDIT-02 greater-of liability and fee allocation, innocent/unproven-intent boundaries and actual lawful assessment. Preserve person/status distinctions.

**FL-26 — Advancement, closure and a real next descent:** KEEP declared advancement, prior resource state, real closure and distinct next-descent purchases. No pending choice or resource refill is awarded by bookkeeping.

**SO-01 — Want, leverage, authority and one declared uncertainty:** KEEP actual Want/Leverage/Limit, authority and declared possible uncertainty. Automatic cooperation and impossible requests do not receive fabricated checks.

**SO-02 — Four degrees, three narrative possibilities:** KEEP announced Success and native Core/opposed distinctions. A costly agreement after Failure is a separate freely accepted offer, not a hidden Success surcharge.

**SO-03 — All five Charisma skills and actual Insight:** KEEP the five actual Charisma skill scopes and evidence-limited Insight. No social skill grants telepathy, ownership, lawmaking or guaranteed obedience.

**SO-04 — Standing access is not an added die modifier:** KEEP standing-based access without importing a second universal numerical modifier from the competing historical scale.

**SO-05 — Alignment remains receipt-only:** KEEP alignment text as preserved, nonoperative receipts in this scope. No moral, cosmological or alignment auto-bonus is inferred.

**SO-06 — One communication clock for all participants:** KEEP the LAX communication clock, aggregate short speech, real interpretation and named components. More speakers do not create simultaneous translated time.

**SO-07 — Actual Help and meaningful retries:** KEEP actual Help intervals/expiration and meaningful changed-evidence retries. Ally rotation, repeated unchanged requests and token assistance grant nothing.

**SO-08 — Magic and acquired class interfaces do only their own work:** KEEP each selected class/oath/spell effect's actual trigger, cost, perception, command and expiry. Shared names and comparisons do not promote pending options.

**SO-09 — Agreements do not manufacture authority or player consent:** KEEP actual authority, agreements and table consent; checks and fictional compulsion do not override player safety or convey another person's property.

**SO-10 — Witnessed attributed consequences and standing:** KEEP witnessed, attributed institution-specific consequences and one signed scene-opening delta. No unseen report or repeated proof becomes a fresh award.

**SO-11 — Faction turns are paid actions, not return rewards:** KEEP global 24-hour and genuine-return coalescing, at most three watched factions, actual independent workers, action times and received information.

**SO-12 — Finite rival clocks and complete faction records:** KEEP finite predeclared rival clocks, real causes and blocked thresholds. Reaching a threshold is not permission for an impossible raid, route or instant report.

**TR-01 — Nine real mount profiles:** KEEP all nine source-bound mount rows and explicitly NEW complete physical profiles. Source price/speed/carry remains distinct from added body values.

**TR-02 — Riding control, training and actor caps:** KEEP real willingness/training/control, actor caps and completed handling work. A mount's presence grants no extra independent class/device command budget.

**TR-03 — One whole regular turn for a controlled mount:** KEEP the whole controlled-mount turn after its rider, permitted actions and prospective scheduling. EX-W13's separate RP fixture requires EX58-X01.

**TR-04 — Mount, dismount and stay seated:** KEEP current-Speed dismount cost, actual hands/support and one source-defined seat check per physical root. EX58-X01 corrects only EX-W13's RP premises.

**TR-05 — Mounted geometry and opportunity attacks:** KEEP actual mounted seat/reach geometry and one lawful opportunity-attack budget. EX58-X01 does not change EX-W13's seat or movement result.

**TR-06 — Pending mounted feats and motion hooks:** KEEP actual self-powered Dragoon movement, no carried/teleport credit, narrow Dissonance—not RP—reduction and pending feat boundaries. Correct EX-W13 pools by EX58-X01.

**TR-07 — All tack, feed and boarding rows:** KEEP all tack, feed and boarding source rows, exact fit/capacity, separate feed/water and real stable care. Barding costs/mass and armor candidate are not compounded twice.

**TR-08 — Five drawn vehicles and distinct Dungeon sled:** KEEP the five drawn vehicles, actual driver/puller contributions and physical capacities; Player Sled and Core Dungeon sled remain different records.

**TR-09 — All six watercraft, real crews and movement:** KEEP all six watercraft, real crew/propulsion/wind/draft/body limits and paid work. No native vehicle turn, automatic crew or capacity-based expedition-cap waiver.

**TR-10 — Porter, bearer and pack-animal services:** KEEP porter, bearer and animal service rates, real load/handling and work/rest limits. Hiring does not create bodies, ownership or extra combat participants.

**TR-11 — Hauler, caravans and specialist extraction:** KEEP the manually controlled finite Hauler, moving-time fuel and service counters. Caravan/teleport quotations remain distinct from actual travel or spell permission.

**TR-12 — Passengers, casualties and exact transfer work:** KEEP real passenger/casualty mass, stretcher capacity, actual transfers and compatible helpers. Petrification does not multiply gear or invent a carry allowance.

**TR-13 — One route travel rate and real transfers:** KEEP one convoy pace, real route modifiers, transfers and actual travel time. Do not double-apply route penalties or gain mileage from reassigned Progress.

**TR-14 — Living recovery, structural repair and rescue:** KEEP living healing separate from structural repair, original-member requirements, actual material/time and finite sinking/shoring/towing. Repair does not reset service, custody or terminal claims.

**RP-A01 — Explicit source-version interpretation, not clamping:** KEEP explicit known-version interpretations with preserved raw values. Unknown versions are not automatically clamped into the adopted scale.

**RP-A02 — Lossless raw envelopes and unknown keys:** KEEP byte-preserving envelopes, ordered duplicate keys, null/absence/zero/false/strings and parse failures. No real saves were read or migrated.

**RP-A03 — All20 background starts and actual later histories:** KEEP all twenty background starts and the Cult Escapee authorities Disliked=-1 correction. Replace only a provably wrong initialization contribution, then replay earned history.

**RP-A04 — Display labels never rewrite numeric authority:** KEEP display labels as derived views; ambiguous historical labels cannot rewrite exact scores or recreate absent keys.

**RP-A05 — 44 stable institution keys and privacy:** KEEP all forty-four stable source institution identities without treating the registry as a closed-world whitelist. Public names do not publish private dossiers.

**RP-A06 — Signed events, caps and reversible interpretation:** KEEP signed scene proposals from the opening score, one ±2 scene cap, ±3 scale cap, retained overflow and reversible source interpretation; no sequential-clamp exploit.

## 8. Finite fulfillment and conditional acceptance

The correction list is exhaustive for this exact submission: **EX58-X01 only**. There is no new source-authoring blocker, missing output family or request for another preliminary conference.

Fulfillment requires the following finite evidence:

1. Preserve the frozen ZIP, all419 original payloads, original outer/V3 manifests,304 V3 payloads, earlier source packages/errata and historical receipts. Apply only the five logical EX-W13 replacements to the five named current JSON views and four Markdown mirrors, with the two current boundary-component bindings refreshed.
2. Match the complete corrected case and eight pre-label descendant files to the packaged reference, or prove the same complete object/text differences under an equivalent renderer. Keep the other411 payloads unchanged. Do not edit any class table, spell source, body, source directive, expected consequence, original boundary outline or fulfilled receipt to make the example pass.
3. Verify all current public/internal component and whole-reading equality, complete Player/Director rendering, current bindings and33 reading links. Preserve the original1,213-check report and the reproduced1,214-check report as their own evidence; any fresh assembly receipt must be a descendant record, not a rewrite of the frozen submission.
4. Reproduce the two corrected debits and unchanged movement/Dissonance consequences. Reject the original over-maximum pools, insufficient funds, a fabricated movement RP discount, no-payment outcomes and an unannounced class-level change. The packaged435-check strict reference report contains these eight deliberate-corruption rejection fixtures; they are bounded reference checks, not a spell runtime.
5. Record a version-bound fulfillment receipt naming this verdict, the actual pre-label/current hashes, applied locations, result totals and preserved boundaries. The1,584-check reviewer script can be rerun on the corrected tree; the supplied expected reference result is1,584/0.

**When these conditions pass, Codex is explicitly authorized to mark the corrected EX58 authored expedition/transport/social/reputation candidate as reviewed and accepted within this verdict's scope, without another generic conference or unchanged full resubmission.** A concise fulfillment receipt is sufficient. A genuinely different amendment or an unexpected failed condition must be named precisely rather than silently accepted.

Any status normalization must be separately recorded and reversible against the checked pre-label tree. It may identify this current top-level candidate/reading wrapper as **“Reviewed authored expedition, transport, social and reputation candidate under EX58-EXACT-2026-10-11; runtime, human testing and final whole-game flow remain open.”** An authored-only `exactCandidateApproved` marker may change only after fulfillment, with that scope recorded. Keep runtime/selection disabled, do not change historical source/component status labels into new approvals, and do not alter any gameplay value through a status update. Append current receipt/hashes; do not overwrite prior authority or original artifact hashes.

No additional owner confirmation is introduced.

## 9. What remains outside acceptance

Carry forward the fulfilled LAX/NWX/LRX/TEX and687 internal/433 public recipe scopes, with ordinary authored spells412 reviewed/436 pending. This review does not reopen them or complete the remaining catalogues.

Actual operation prerequisites remain actual inputs: a real compatible route/body, accessible components/cargo, finite stock and crew, legal ownership/authority, authentic source-version/earned standing, safe handling, actual quoted services, and a separately applicable operative spell where specialist transport needs one. They do not become a new blanket authoring queue, and synthetic acceptance is not proof those inputs exist.

Unrelated pending class/spell/feat choices, full class combinations, bestiary/Director and remaining catalogue work, application implementation, arbitrary-save migration, human teaching/two-lookup/playtesting/balance and DD01 remain open. The current candidate's record contracts and examples are not a universal runtime adapter. Incidental Opening/Horn, sealed-language and other setting references remain literal receipts; no cosmology or deep-setting interpretation is granted.

The order remains **actual final joint Codex/GPT whole-game flow agreement → already-authorized GitHub push → verified remote commit → careful cosmology review**. This expedition verdict is not that final agreement. No source deletion, push, remote verification or cosmology review was performed.

## 10. Package and reproduction

`EX58_EXACT_DISPOSITION_REGISTER.json` contains individual dispositions and exact pointers for all58 directions, ECX-01–15,190 chapter examples,29 transport profiles,four auxiliaries,21 integrated events,15 contract families,28 boundaries,24 social scenarios and12 reputation probes. All are authored review decisions, not relabeled runtime passes.

`EX58_X01_CORRECTIONS.json` contains complete old/new values and all affected representations. `EX_W13_CORRECTED_REFERENCE.json` is the complete corrected record, not an abbreviated patch. `EX58_X01_SOURCE_EXCERPTS.md` supplies the submitted source locations/lines/hashes.

The scripts use Python's standard library and need no network or installation. `apply_ex58_x01_reference.py` creates a separate unlabelled reference tree, preserving the original. `review_ex58_exact.py` is read-only except for its chosen new report. `validate_ex58_x01_fulfillment.py` checks the exact pre-label descendant. All refuse to overwrite existing output reports/destinations.

No hash in this package is claimed to describe Codex's later repository changes. The measured descendant hashes refer only to the separate reviewer-created reference copy. Original files and past failed expectations remain preserved rather than rewritten to appear to have passed.
