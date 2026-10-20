# Strain — source-qualified playtest reference

**Status: REVIEWED / reference-VALIDATED within the supplied namespace, penalty and recovery scope.** [GPT's exact disposition](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FINAL_REVIEW.md) confirms this bounded candidate. The two names below refer to independent systems. This candidate preserves the Warrior engine and retains the Gameplay Loop's expedition track as a provisional campaign overlay. It does not promote that older table into the approved Core book.

Use [source bindings](../../data/playtest/strain_bindings.json), [source validation](STRAIN_SOURCE_VALIDATION.json), [combat timing](COMBAT_ACTION_PLAYTEST.md), [conditions](CONDITIONS_PLAYTEST.md) and [HP/Wounds](CORE_RESOLUTION_PLAYTEST.md). The [first GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md) and [counterexample corrections](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_COUNTEREXAMPLE_REVIEW.md) preserve the decisions. The latter corrects an earlier summary that misplaced the expedition attack/save penalties at level3; their source places them at level2.

## Identify the track first

| Mechanical ID | What it represents | Range | Generic recovery |
|---|---|---:|---|
| `warrior.serum-strain` | The Warrior serum/mutation engine, including an explicit Serum Sharing recipient | 0–3 | Beneficial completed1h Short Rest−1; beneficial completed8h Long Rest→0 |
| `expedition.strain` | Campaign attrition, Rest Debt, unsupported Supply, Quickglass crash and ordinary Wound-treatment critical failure | 0–6 | Secure beneficial Long Rest−1 eligible point; Morale Rest−1; qualifying Haven care removes all eligible ordinary points |

Neither is global `core.exhaustion`, Oracle Revelation backlash, Dissonance or historical Resonance Burn. A single cause applies multiple tracks only if its operative source explicitly says so. Serum3 never becomes expedition3, and serum overflow never becomes expedition6. A namespace binding identifies a reference; it does not itself apply any effect.

Inside the supplied Warrior engine/cards, Strain means serum Strain. In the supplied campaign references, Strain means expedition Strain. **Future ambiguous sources remain unbound until reviewed.** The source register records8 Warrior engine references,17 cards,3 campaign sections and12 exact Core paragraphs. Do not classify a new immunity or source by its name alone.

Quickglass's crash adds1 expedition point and retains its independent one-hour DEX-check disadvantage. Ordinary Wound-treatment Critical Failure adds1 expedition point to the **patient**, without inventing another Wound or Exhaustion level. Morale Rest removes expedition Strain only. Serum Tolerance suppresses the profile side effects it names; it does not prevent serum Strain or its penalties.

## Warrior serum Strain

Preserve the source engine: normal Serum Injection/Mutagen Injection and Mutation Surge add1; Serum Cocktail/Mutation Overload add2 unless a printed modifier applies. Cap3. At2, Speed−5. At3, also AC−1 and saves−1; the source's voluntary serum/Cocktail/Overclock/Surge activation lock applies. All card costs, prepared doses, mutation limits and frequencies remain required.

For an activation explicitly illegal if it exceeds the cap, calculate its **final modified gain first**, including applicable Mutation Adaptation and the minimum1 for Cocktail/Overload where applicable. Reject a resulting value above3. Never clip a voluntary overcap cost into legality. A separate activation lock can still prohibit activation even if a gain modifier makes its cost small or zero.

Automatic later gains, such as the actual **Sanguine Surge** profile's ending side effect, clamp at3. They do not retroactively invalidate the original activation, cause overflow death or add expedition points.

**Serum Sharing — NEW integration.** Its willing recipient receives serum Strain even when not a Warrior. At recipient3, the attempted+1 clamps at3; this is not the recipient activating an otherwise locked class ability. The recipient retains all existing penalties and receives only the card's actual diluted effects and side effects. Source-owner Serum Tolerance does not protect the ally. Recipient Strain uses the same beneficial1h/8h recovery; no serum preparation, mutation slots or other Warrior powers are granted.

## Expedition Strain

NEW interpretation: rows are cumulative. Preserve the original placement of effects:

| Level | Additional consequence |
|---:|---|
| 0 | None |
| 1 | −1 initiative and expedition checks |
| 2 | Speed−10; −1 attacks and saving throws |
| 3 | Disadvantage on expedition checks; Dash lock below |
| 4 | Effective maximum HP×3/4 |
| 5 | Core Incapacitated plus the explicit movement restriction below |
| 6 | Deterministic death/collapse endpoint below |

Initiative−1 applies when a roll is made. Changing Strain does not reorder an established encounter. Ordinary advantage/disadvantage does not numerically stack from multiple sources.

Represent each point with `pointId`, `sourceId`, `ordinaryRemovable` and `removalGateMet`. Level is the active count, maximum6. Keep source history and attempted overflow even when no additional point can be stored. A generic recovery can select only points that are ordinary-removable **and** whose gate is met. A specific treatment can override only the source it expressly covers. Clearing a gate updates metadata; it does not silently delete a point.

**Level6 — NEW deterministic interpretation.** On every positive, unprevented expedition gain that would reach **or exceed6**, evaluate that gain's endpoint before clamping stored points at6. Default: ordinary Dead state. Only that gain's explicit reviewed nonlethal source can instead produce `expedition.collapse`. A living collapsed creature already at6 can die from a later ordinary gain; it is not protected by the cap. A prevented/zero gain causes no endpoint. Nonlethal gains or Strain removal never revive a corpse.

Collapse leaves the creature alive, Unconscious, Speed0 and unable to act/travel. It does not set HP0, grant Stable or create death saves by itself. Independently dying0HP creatures still follow their normal saves. Short/Long/Morale Rest cannot reduce expedition points while this level6 collapse persists; qualifying24h Haven care or explicit treatment may. Collapse ends only when the track falls below6. Other Unconscious sources remain independent. If all six points stay blocked, Haven care cannot clear the collapse by assertion.

This recoverable collapse is a **NEW operational replacement** for the source's undefined “permanent collapse” alternative. The original wording remains preserved; it did not itself specify this recovery. Actual resurrection while six expedition points remain is a separate unresolved resurrection interface.

## Independent penalties and maximum HP

Apply flat Speed changes first, floor at0, then applicable multipliers and floor normally. A rule setting Speed0 takes precedence. Serum2's−5 and expedition2's−10 coexist: base30 becomes15, then Exhaustion2's half Speed gives7. Mutation Adaptation's explicit serum Speed exception does not cancel expedition Speed loss.

Expedition2 and serum3 each impose saves−1, totaling−2. The class rule against stacking duplicate bonuses does not merge these independent tracks.

NEW maximum-HP composition: multiply applicable rational factors against the same otherwise-applicable maximum, floor **once**, minimum1. Expedition4×3/4 and Exhaustion4×1/2 produce37 from base100. Clamp currentHP down if necessary; that clamp is not damage and triggers no Wound, death-save failure or damage resource. Removing a modifier raises capacity without healing/resetting death counters. Critical Wounds' healing ceiling then uses `max(1, effectiveMaximumHP−1)`; it is not another maxHP multiplier.

The helper accepts other multipliers only after their compatibility has been established elsewhere. It does not decide whether unrelated gear/ancestry/spell modifiers stack.

## Dash lock — NEW

At expedition3–4, a legal Dash consumes the current opportunity and creates a lock. No other Dash is legal while locked, whether Action, Bonus Action, extra Action or extra turn. A non-Dash Action, round boundary or extra turn does not clear it.

In initiative, lock through the **end of the next future regular turn** of the creature. A Dash during its current turn excludes that current end, using the exact marker-exclusion rule from combat. Thus turn1 Dash blocks another that turn and turn2; turn2's end unlocks turn3. An off-turn Dash locks through the next regular turn's end. Extra turns cannot substitute for that marker.

Outside initiative, unlock at Dash time+6 seconds. Preserve whichever endpoint was recorded across initiative entry/exit/reorder; do not restart or convert it. Falling below expedition3 clears the restriction and stored lock immediately. Returning to3 begins unlocked until a new legal Dash. Expedition5 cannot Dash at all.

The exact review confirms exclusion of the current in-progress turn end. Its earlier “strictly after Dash” shorthand is superseded by these specific marker rules and tests.

## Expedition5 and assistance

Core Incapacitated denies Action/Bonus Action/Reaction and ends concentration. NEW expedition-specific restriction: no voluntary tactical movement in initiative. This does **not** redefine generic Incapacitated or automatically set the creature's actual Speed statistic to0. Forced movement, an external legal teleport and lawful carrying still work.

Outside combat, apply the slow-travel exception by halving the otherwise legal walking/travel pace once after applicable load/Speed/environment rules. Do not repeatedly halve per Watch or invent miles-per-hour values here. Detailed stacking with other travel-pace modifiers remains the travel review's responsibility.

Brief communication is possible if no other condition prevents it. The victim cannot use an Action-time consumable by itself. A legal willing recipient can be fed, given a potion or treated by someone paying the actual required Action/activity, supplies and costs. This creates no free administration or universal restraint/capture rule. Rest and Haven care remain possible when their eligibility requirements are met.

## Recovery and actual elapsed time

Preserve campaign limits: Short Rest1h, at most **two beneficial Short Rests between beneficial Long Rests**; Long Rest8h, at most **one beneficial Long Rest per24 elapsed hours**. Those limits apply to serum recovery too, including non-Warrior recipients. Exact completion timestamps and IDs prevent replay. Work, travel, short rest, sleep and recreation cannot spend the same active hours twice. Unfinished/interrupted activity provides no completion benefit.

**Rest Debt order.** First complete a qualifying safe8hRestWatch and clear debt it satisfies. Then evaluate beneficial Long Rest eligibility. If eligible, apply its sourced benefits, including serum reset and one eligible expedition point when secure. Persistent food/water/source blocks still prevent expedition reduction. An additional safe RestWatch inside the24h reward cap can discharge debt but cannot restore resources, remove expedition Strain, reset the beneficial-rest clock or reset short-rest counts.

**Secure Long Rest.** Remove one eligible expedition point chosen by the patient, once the rest qualifies and no reduction block remains. This is a separate benefit from serum reset, so one actual qualifying rest may do both. Class-only serum reduction never silently removes expedition points.

**Morale Rest — NEW endpoint.** Four consecutive safe hours of voluntarily chosen recreation, without forced substance use, work, expedition travel or simultaneous sleep/ShortRest. At most one beneficial Morale Rest per24 elapsed hours. Remove one eligible expedition point. It never removes a Wound. A distinct4hMoraleRest plus an eligible8hsecureLongRest can legitimately remove two points; there is no new shared one-point cap.

**Haven care.** One full day means24 consecutive hours under qualifying Haven care/location conditions, with real care, food and water supplied under campaign rules. One active care interval per patient; interrupted care gives no completion benefit and restarting requires a fresh24h window. At completion remove all eligible ordinary expedition points; blocked/special points remain. The care window may contain separate sleep, meals and4h recreation because it is not24h of active practitioner work. Incompatible practitioner activities cannot be double-counted.

The Strain reference does not replace HP/RP/RC rest rewards or settle all supply prices, travel limits or camp security. Those systems retain their source review gates.

## Immunity, suppression and removal

Only explicit source-qualified wording changes a track. Poison immunity, global Exhaustion immunity, serum-profile tolerance and expedition immunity do not automatically cover serum Strain. Exhaustion removal does not clear either track. An unqualified future “immune to Strain” remains unbound.

- “Cannot gain expedition Strain” blocks gains only.
- “Ignore expedition Strain penalties” retains the points; no implied prevention of gain or level6 endpoint.
- “Remove X expedition Strain” actually removes eligible points under that source.

These tracks do not inherit the generic condition-immunity suppression rule merely because their UI label resembles a condition.

## Reference scope

The implementation in `tools/strain_playtest_rules.py` covers selected namespace lookups, gain/cap/death transitions, point recovery, numeric composition, Dash deadlines and completed-rest accounting. It does not run the campaign, grant class abilities, create inventory, verify all care activities, dispatch conditions or perform resurrection. The caller supplies legality and source eligibility. Its penalty projection does not replace independent life-state, collapse, condition or travel rules.

The namespace lookup rejects unknown/ambiguous sources. Low-level transition helpers such as `expedition_gain` accept already-validated source IDs from their caller; they do not independently repeat the registry lookup.

The [validation report](STRAIN_PLAYTEST_VALIDATION.json) records71 transition checks,30 exact source checks and4,949 maximum-HP invariant states. Broader rest rewards, travel, all-source class semantics, future Strain references, resurrection and human balance remain open.
