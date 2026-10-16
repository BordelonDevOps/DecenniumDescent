# Core consumables — common-use discussion draft

**Local proposal, not jointly reviewed or adopted.** The 24 source brews/substances remain unchanged and individually unpromoted. This draft gives the next conference one concrete shared procedure to challenge, with explicit per-item dependencies. It is not permission to use incomplete item effects.

[Model and exact source evidence](USE_MODEL.json) · [28 authored situations](CASEBOOK.json)

The central source distinction is twelve magical substances with dependence DCs versus twelve brews without those DCs. The source supplies repeat-dose, tolerance and overdose concepts, but not a complete operational profile for every item.

## CU-01-01 — Separate the two catalogs

The twelve magical substances use their printed dependence DC and the Core repeat-dose, tolerance, overdose and crash rules. The twelve brews have no printed dependence DC and do not silently inherit that subsystem. A brew adds Intoxication only when its own proposed operational profile explicitly does so. Preserve Gatehouse Small Beer’s one-serving exemption and Thunder-Vein Ale’s printed delayed +1. Neither an alcohol-like name nor a price creates a generic poisoning, dependence or Intoxication gain. Individual brew proposals must disclose any NEW repeated-serving rule rather than hiding it in this framework.

**For actual GPT review:** Confirm the catalog boundary and whether a separate source-directed ordinary brewing rule should give other brews Intoxication; no such increase is adopted here.

Evidence: E02, E07 in USE_MODEL.json.

## CU-01-02 — Real portions and administration

NEW unit proposal: an ordinary brew serving is one actual pint of liquid, provisionally 1 lb plus its real container, drunk over one uninterrupted active minute. A named profile can expressly use a different amount/time. Each magical substance uses one measured ready dose and the existing Action/available-hand/actual-access procedure; oral administration requires actual swallowing and an eligible willing or Incapacitated recipient within 5 ft. Inability to eat as a requirement is not automatically inability to swallow, but no effect supplies missing anatomy. An unwilling active creature receives no generic forced-dose permission. All 24 profiles must specify their actual packaging/mass rather than treating a menu entry as stock. These proposed portions do not replace printed crafting recipe units or transform powders into free inhaled attacks.

**For actual GPT review:** Accept or replace the pint/minute brew convention and classify the individual substance units against their actual descriptions. Do not equate the brew serving with a universal meal duration.

Evidence: E01, E14 in USE_MODEL.json.

## CU-01-03 — Consumption and interruption

Reserve actual units when administering. A completed full serving/dose creates one consumption event at its completion timestamp. Fluid/material actually swallowed, spilled or destroyed before an interruption is physically gone; no game benefit is granted for an incomplete dose and no whole unit is refunded. Ordinary consumed water/food counts only when its own source permits that actual amount. Do not combine arbitrary fractional remains into a stronger dose: a named whole-unit preparation procedure must establish usable potency. This is an explicit NEW rule for unfinished administration, not a statement about real chemistry.

**For actual GPT review:** Confirm completion timing and distinguish physically lost quantities from completed-dose counters. Individual instant benefits still use their actual completed consumption event.

Evidence: E01, E10 in USE_MODEL.json.

## CU-01-04 — Dose history belongs to the recipient and named substance

Maintain a stable recipient ID and exact substance identity, with completed dose events (eventId, completedAt, units=1 or 2, actual stock IDs), beneficial-long-rest boundaries, dependence status, maintenance interval, tolerance latch, benefit records and crash records. Another supplier, brand, session, controller or inventory transfer does not erase a recipient’s history. Different named substances have separate histories unless an explicit later reviewed equivalence says otherwise. No broad label such as drug, wine, Null or Strain establishes identity.

**For actual GPT review:** Confirm the identity and recipient boundaries, including a real later restoration using the same character record; source-specific transformation/restoration exceptions remain controlling.

Evidence: E02, E03 in USE_MODEL.json.

## CU-01-05 — Rest boundary is an explicit unresolved integration choice

NEW proposed resolution: only a genuinely beneficial completed Long Rest resets the doses-since-rest counter and opens the next named-dependence maintenance interval. An extra safe eight-hour Rest Watch inside the reward cap can clear Rest Debt as printed but cannot be used to erase repeat-dose/overdose accounting. Resetting the counter does not clear dependence, tolerance, already scheduled crashes or running effects. This narrows the condition chapter’s unqualified completed-long-rest wording and therefore needs an explicit joint disposition before use; the currently reviewed chapter is not changed by this draft.

**For actual GPT review:** Should substance epochs require a beneficial Long Rest, or any actual completed Long Rest? Resolve this against the current safe-Rest-Watch distinction and record an explicit supersession if needed.

Evidence: E04, E09 in USE_MODEL.json.

## CU-01-06 — Repeat-dose and overdose ordering

At a legal completed event, read the recipient’s pre-event tolerance and rest-counter state. One ordinary dose counts as one; a doubled dose counts as two. If this event contains any second-or-later dose since the rest boundary, require one CON save at that named substance’s printed dependence DC, at most one save for the whole event. NEW failure interpretation: become Addicted to that named substance; success never cures existing dependence. If the new rest count exceeds two, also execute that item’s explicit severe complication once for the event and apply the NEW dependence-advancement interpretation: acquire named dependence automatically if absent, otherwise retain it and record the overdose without inventing a second severity scale. The save cannot cancel the separate automatic overdose consequence. Every further event above two triggers its actual complication once, not once per conceptual dose inside a doubled event. A missing complication blocks an item’s operational completion; this draft supplies no generic substitute.

**For actual GPT review:** Review the save trigger for a doubled first use, once-per-event overdose, and automatic named dependence as the meaning of advances dependence. Approve each item’s actual severe complication separately.

Evidence: E02, E03, E04 in USE_MODEL.json.

## CU-01-07 — Tolerance is a latch with exact rolling history

Use seven elapsed days = 604800 seconds. The completed-dose counting window is (now−604800, now], so an event exactly seven days old is outside it. At seven full days without a dose, clear the tolerance latch immediately before processing a new dose at that timestamp. If tolerance was inactive before the event, its current ordinary benefit duration is not shortened even when that event reaches three doses in the rolling window. Set tolerance active after that completion if the new rolling count is at least three. Once active it remains active until a full seven-day no-dose interval, even if the rolling count later falls below three while some more recent use remains. A Long Rest does not clear it.

**For actual GPT review:** Confirm the exact equality boundary and its order against a simultaneous new dose; the third-use and seven-day abstinence rules come from the reviewed recovery chapter.

Evidence: E03 in USE_MODEL.json.

## CU-01-08 — What doubling and half duration actually do

A doubled event needs two real complete doses already prepared for one actual administration. It uses two units for inventory, rolling tolerance and doses-since-rest, but never doubles potency, temporary HP, damage, number of targets or entitlements. When tolerance was already active, it restores the printed normal benefit duration; without tolerance it gives only that normal duration. One actual Action is permitted only where the individual dose profile allows both ready units to be consumed in that Action; otherwise they are separate completed events, not an after-the-fact doubled declaration. Half duration uses exact elapsed seconds, with no rounding to a larger minute or round. Only duration-based benefits are halved. Crashes, recovery requirements, overdose complications and the duration of an adverse effect are not shortened by generic tolerance. Instant benefits and undefined until-next-rest/one-use endpoints require a named item interpretation; do not invent a half-rest.

**For actual GPT review:** Review per-item administration, Dreammilk/Spiral Ink endpoint semantics and Wyrmspice’s missing entitlement duration. No doubling can waive the printed Redwake benefit lock.

Evidence: E03 in USE_MODEL.json.

## CU-01-09 — Every dose keeps its own ending and crash

Create one dose-benefit record with a fixed original endpoint and one pending crash record. Same-name bonuses, advantage and resistance do not stack numerically. A later dose does not erase or postpone an earlier dose’s endpoint or crash. At each dose’s real end, apply its printed crash once even if another dose still supplies a benefit; the two can coexist. NEW proposal: an actual effect-ending cure that removes the benefit early triggers that dose’s crash at the actual ending timestamp unless it explicitly also prevents/removes the crash. Mere suppression pauses neither the original duration nor the crash clock. A spent benefit use ends that entitlement but triggers an immediate crash only where the individual item explicitly binds the crash to that expenditure. Temporary HP follows its actual source record and existing selection rules; there is no pooled duplicate award.

**For actual GPT review:** Confirm early ending versus suppression and the intended crash trigger for each consumable. A spell-only dispel does not automatically target a nonspell dose.

Evidence: E02, E08 in USE_MODEL.json.

## CU-01-10 — One-use rewards cannot become hidden stockpiles

NEW proposed policy for a brew or dose saying next/one check or save: overlapping applications of that same item provide at most one available entitlement. A new completed use may refresh that one available opportunity through its own stated expiry, but cannot queue several. Committing the permitted roll marks every currently overlapping same-item entitlement consumed, so an older covered dose does not reappear as another use. Independent named items remain governed by their own scope; advantage sources still do not stack. A future actually paid dose after expenditure can grant a new opportunity, subject to its actual repeat-use costs and risks. Eligibility and commitment occur before the roll, not after seeing failure.

**For actual GPT review:** Confirm for Delver’s Bitter, Dragonblood Brandy and Verdant Leaf Wine, or provide explicit alternative bounded entitlements. No use is gained if the item’s timing/eligibility remains undefined.

Evidence: E02 in USE_MODEL.json.

## CU-01-11 — Condition suppression is not cure or a free maintenance dose

Only actual completed consumption satisfies a due maintenance dose. Suppressing Withdrawal symptoms does not remove named dependence, erase the due interval or count as taking a dose. For the proposed beneficial-rest boundary, evaluate actual completed rest, open the new interval, then credit only a completed dose at/after that boundary; a dose from before completion cannot prepay it. A dose legally taken after the boundary may end that substance’s Withdrawal while still causing its own crash, dependence save, tolerance accounting and overdose. The seven-day abstinence recovery project and tolerance clearance can run on the same real calendar, but neither one automatically proves completion of the other’s work/supplies/check. A new dose breaks the abstinence project, even if its benefit was suppressed or redundant.

**For actual GPT review:** Review simultaneous completion ordering and whether a completed doubled event can satisfy only the current maintenance requirement, without stockpiling future intervals.

Evidence: E04, E05, E06 in USE_MODEL.json.

## CU-01-12 — No cross-system cure or resource conversion

Keep expedition Strain, Warrior serum Strain, global Exhaustion, dose-driven Intoxication, Unity Exposure, named dependence/Withdrawal, Wounds and HP separate. Quickglass keeps +1 expedition Strain plus its separate one-hour DEX-check disadvantage; neither rest nor suppression silently removes both. A Poisoned immunity does not imply immunity to every substance effect or dependence. Hollow Cask’s eventual −1 healing proposal belongs to the compatible flat-reduction stage and must be compared through Blight Totem’s actual alternate plans, never subtracted twice from one event. A named prohibition on spending RP does not prohibit Oracle RC by name similarity, erase material costs or grant free casts.

**For actual GPT review:** Confirm each named interface against its item’s complete profile. The shared chapter must not promote the item solely because a track or healing pipeline already exists.

Evidence: E08, E06, E07, E12, E13 in USE_MODEL.json.

## CU-01-13 — Physical provisions and economics remain real

Keep printed prices and legal labels as source fields, not guaranteed sellers, permission or stock. A bought brew/dose must come from an actual lot and container. Small/Medium normal daily demand is the current two pounds of food and eight pints of water, Large twice, with actual exceptions. Gatehouse Small Beer’s hydration-safe wording supports proposing actual liquid hydration credit, but one serving never creates a whole Supply basket or food ration. Hollow Cask’s hunger suppression does not remove food/water requirements. Deep Blue’s doubled-water crash needs a defined time-weighted or day-end procedure before it becomes operational; no food/oil/camp-sundry doubling is implied. Committing one real basket to an activity does not leave a second inventory basket.

**For actual GPT review:** Approve each actual serving’s water/food credit and the Deep Blue partial-day formula. Do not let a purchase price or recipe name decide unreviewed ingredient availability.

Evidence: E10, E11, E14 in USE_MODEL.json.

## CU-01-14 — Preserve protected-information and source-specific meanings

Current souls/research and planes companions do not mention Ghostwine, Sovereign Reserve or their exact effect phrases in their JSON string values. That bounded finding does not decide those items’ taxonomy, target predicates, observation range, protected facts or terminal recording. Keep their whole source records pending individual conference. Choir Dust’s repeated-use identity-loss phrase and Choirless Absinthe’s named auditory scope likewise cannot be converted into compulsory beliefs, automatic Equation knowledge or a new soul/realm identity. Moonsap’s movement detection must be reconciled with the current known-position Invisible exception; detecting position is not automatically true sight or permission to target through a wall.

**For actual GPT review:** Resolve these specific item interfaces with actual GPT using the reviewed cosmology sources; do not assume the general cosmology review was also a consumable verdict.

Evidence: E15, E16, E17 in USE_MODEL.json.

## Individual completion register

Every item below still requires its complete individual effect and exact review; none is promoted by this shared proposal.

| ID | Source name | Remaining individual/interface work |
|---|---|---|
| CB-01 | Gatehouse Small Beer | CU-01-01; CU-01-02; CU-01-03; CU-01-13 |
| CB-02 | Delver's Bitter | CU-01-09; CU-01-10 |
| CB-03 | Stoneback Stout | Actual cold-exposure scale/HZ-03; no universal Exhaustion or cold-resistance substitution |
| CB-04 | Tidesilver Grog | Actual seasickness checks/hazard cadence |
| CB-05 | Embermark Porter | Meaning and ordering of fire resistance 1 against environmental heat |
| CB-06 | Verdant Leaf Wine | CU-01-10; Actual meal interval and check eligibility |
| CB-07 | Mooncap Mead | Actual sleep/vision/nightmare/save endpoint and player agency |
| CB-08 | Thunder-Vein Ale | CU-01-09; CU-01-12; Actual repeated brew serving policy |
| CB-09 | Dragonblood Brandy | CU-01-02; CU-01-10; Actual fast-drinking threshold and fear entitlement expiry |
| CB-10 | Hollow Cask | CU-01-09; CU-01-12; CU-01-13 |
| CB-11 | Choirless Absinthe | CU-01-14; Actual receiving versus sending telepathy and named Bard Chant scopes |
| CB-12 | Sovereign Reserve | CU-01-14; Final sentence/record custody/protected information; specific actual GPT decision required |
| CS-01 | Quickglass | CU-01-04; CU-01-05; CU-01-06; CU-01-07; CU-01-08; CU-01-09; CU-01-12; Individual severe complication |
| CS-02 | Dreammilk | CU-01-08; Actual qualifying sleep/rest anchors and nonretroactive first-failed-save rule; Individual severe complication |
| CS-03 | Redwake | Selected real Wound penalty; temporary HP source and expiry; crash damage type; Actual benefit lock; Individual severe complication |
| CS-04 | Moonsap | CU-01-09; CU-01-14; Actual movement-detection predicate and known-position interface; Individual severe complication |
| CS-05 | Ghostwine | CU-01-14; Ethereal/residue eligibility, range, barriers, actual spirit/corpse fear source and save DC; Individual severe complication |
| CS-06 | Null Salt | CU-01-09; CU-01-12; Spell-source damage root and reduction order; Individual severe complication |
| CS-07 | Choir Dust | CU-01-09; CU-01-12; CU-01-14; Specific Unity-gain authorization and repeated-use meaning; Individual severe complication |
| CS-08 | Spiral Ink | Actual selected research work/check eligibility; finite concentration-penalty ending; Individual severe complication |
| CS-09 | Deep Blue | CU-01-09; CU-01-13; Actual partial-day doubled-water accounting; Individual severe complication |
| CS-10 | Ember Resin | Actual eligible melee damage packets, de-escalation checks and noncoercive scope; Individual severe complication |
| CS-11 | Saint's Ash | Actual available Hit Die/maximization/healing; Poisoned source suppression; accelerated dependence interpretation; Individual severe complication |
| CS-12 | Wyrmspice | CU-01-08; Actual ingestion/Action/entitlement and cone/DC/type/recoil; Locate or explicitly author the referenced Mutation complication table |

The current Core search found the item references to Mutation complications, cold-weather exposure and seasickness, but did not establish their full procedures in that bounded matching set. The reviewed souls/planes JSONs contain no literal item-specific Ghostwine or Sovereign Reserve clause; that is not a general claim that spirit or death sources are absent. Actual item-specific conference remains necessary.

Nothing here changes the completed 687 crafting recipes, 419 reviewed ordinary spells, original books, approved condition recovery, cosmological identities or owner campaign era. Runtime, human playtesting, balance and whole-game approval remain open.
