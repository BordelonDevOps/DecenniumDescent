# Condition recovery and exposure — provisional procedures

**Reviewed provisional integration, 8 October 2026.** These are fictional game procedures. The sources provide the condition identities, existing dose/tolerance rules, six Exhaustion levels and Intoxication thresholds; the exact generic recovery projects and missing endpoints below are newly authored proposals discussed with GPT. Preserve the original sources. Use with [all 28 conditions](CONDITIONS_PLAYTEST.md) and [HP, Wounds and death](CORE_RESOLUTION_PLAYTEST.md).

## Time, costs and checks

A project day is a consecutive 24-hour interval starting when that project begins, not a calendar-date change. A three-day project finishes no earlier than 72 elapsed hours; seven days means at least 168 hours. Only one project of the same kind for the same patient and named condition may be active. Concurrent clocks measure the same elapsed time once; the same active hour or consumed Supply cannot pay two activities. An active practitioner cannot simultaneously perform a long rest. A patient can receive care while resting where the care permits it.

Consume each stated Supply or kit use at the beginning of its attempt or daily work. Interruption does not refund it. Missing a required project day, taking a forbidden dose or receiving forbidden new Exposure ends that attempt; completed costs remain spent, and starting again requires a fresh full project. Merely suppressing symptoms does not interrupt abstinence or time already properly completed.

Project skill checks use the reviewed four-degree task rules. Success and Critical Success give the stated success; Failure and Critical Failure give the stated failure unless specifically differentiated. No extra reward or complication is inferred from an undefined degree. Saving throws remain binary. Use WIS (Medicine), INT (Religion), INT (Arcana), or an INT check using proficiency with alchemist's supplies for Alchemy. These ability/tool assignments are explicit integration choices; an actual feature can supply its printed alternative.

## Exhaustion

The six V6 effects are cumulative: level 1 disadvantage on ability checks; 2 Speed halved; 3 disadvantage on attack rolls and saves; 4 maximum HP halved; 5 Speed zero; 6 death. Compute level-4 maximum as `max(1, floor(otherwise-applicable maximum HP / 2))`. Recompute from the otherwise-applicable maximum whenever it changes. Clamp current HP when the maximum falls; restoring the maximum does not heal. Flat Speed changes apply before halving; a zero-Speed condition overrides the calculation. A maximum-HP reduction alone is not damage and does not trigger a Wound save.

**NEW generic recovery:** At the end of a beneficial eight-hour long rest, remove one Exhaustion level from a living creature at levels 1–5 if it met the campaign's food/water requirements, the originating cause no longer actively imposes or refreshes Exhaustion, and no source-specific rule blocks removal of the chosen level. At most one generic level can be removed per 24 elapsed hours. Specific reviewed effects can remove additional levels as printed. A prerequisite such as Moisture Dependency's one-hour immersion unlocks recovery; it does not itself remove a level unless explicitly stated. Track blocked-source levels separately so another source's removable level may still be selected; the patient chooses a legal level to remove.

Exhaustion 6 causes death. Removing levels from the corpse never revives it. A resurrection effect must also leave the creature below 6 or it immediately dies again. Global Exhaustion, expedition Strain, Warrior serum Strain and Oracle's one-turn Revelation backlash remain separate records; this procedure clears none of those other tracks. See the [Strain namespace candidate](STRAIN_PLAYTEST.md) for its separately recorded review status.

## Dependence and Withdrawal

Preserve Core's existing substance procedures: resolve benefit and crash; a repeat dose before the next long rest requires the substance's dependence CON save; three uses within seven days cause tolerance that halves duration unless doubled; more than two doses before a long rest triggers the substance's severe complication and dependence advancement. This document supplies endpoints, not a replacement substance catalog. Use each item's reviewed dependence DC and severe complication. An item lacking its actual consequence remains in the item review queue rather than gaining an invented generic overdose result.

**Maintenance:** At each completed long rest, a new maintenance dose is due for each named dependence. Withdrawal applies immediately until a qualifying dose is taken after that rest; a dose taken before its completion cannot satisfy the new interval. The dose ends that substance's current symptoms until the next maintenance interval but does not remove dependence. Ordinary consumption time, stock, crash, tolerance and repeated-dose rules still apply. No free dose or Action is granted.

**Tolerance:** Record doses in a rolling seven-day window. After the third completed dose/use within that window, tolerance becomes active; subsequent uses have half duration unless doubled. The third ordinary use is not retroactively shortened. Count a doubled dose as two doses for tolerance, repeated-dose and overdose accounting; resolve its two-dose thresholds as one consumption event, with at most one dependence save for that event. Seven full days with no dose clears tolerance. One long rest does not clear tolerance. Track each substance separately.

**NEW dependence recovery project:** Complete seven consecutive project days without a dose of the named substance. Each day the patient spends one hour in treatment/recovery work and consumes one Supply. Choose Medicine, Religion or Alchemy at project start. At the end of the seventh full day, the designated practitioner (who may be the patient) makes that check against the substance's dependence DC, or NEW DC 14 if a direct Addicted effect supplied no substance DC. Success removes that named Addicted and its associated Withdrawal. Failure removes neither; a new attempt needs a new seven-day project. There is no extra automatic Wound on Critical Failure.

The existing Haven activity “Treat Dependence or Withdrawal” gives advantage on the next recovery check and prevents one ordinary withdrawal escalation after one full day under qualified care. For this bridge, a proficient practitioner spends an eight-hour care activity during a project day; that day's one-hour treatment requirement is included, not additional. Advantage applies once to the next recovery check and cannot be stockpiled. Different sources of advantage still do not stack. The activity does not independently cure dependence or erase a dose's printed crash.

Withdrawal imposes disadvantage on ability checks. “Disadvantage on RP recovery” affects an actual RP recovery roll only; deterministic Retune receives no invented arithmetic penalty. Oracle RC is not RP. The generic Withdrawal condition has no further severity track. An individual substance can add an explicitly reviewed duration or escalation; otherwise do not invent one. Symptom-removal magic does not remove dependence unless it explicitly does, but valid symptom suppression is compatible with completing a no-dose project.

## Intoxication

Use one dose-driven score from 0 to 5. Increase it only when an effect explicitly grants Intoxication. A direct effect saying “Intoxicated” supplies a minimum effective score of 2 for its printed duration, or NEW two hours when no duration is supplied. It does not add dose-driven points or count as a dose. Effective score is the greater of the dose-driven score and the active generic floor of 2. Generic timed floors of 3–5 do not exist. A source explicitly setting level 3–5 must individually define its dose-driven change or its own complete recovery exception before becoming operational. Each no-duration floor-2 application expires exactly two elapsed hours after application. Multiple direct floors do not stack, but the floor persists while any is active. Removing one leaves independent points and other direct applications intact.

| Score | Consequence |
|---|---|
| 0 | Sober; no Intoxication consequence. |
| 1 | Disadvantage on precise-memory checks. One available advantage use on a fear save. |
| 2 | Also disadvantage on precise DEX and INT checks. |
| 3 | Also Dazed and Speed −10 feet. |
| 4 | Also Unconscious for the level-4 timer and a poisoning save. |
| 5 | Also a medical emergency with a fixed one-hour deadline. |

The rows are cumulative. The Director identifies a “precise” check before rolling: fine manipulation or exact memory/analysis, not every possible use of DEX/INT. The player may spend the one fear-save advantage use before rolling. It refreshes only after effective score reaches 0 and a later new episode begins, never at each positive level. An explicit independent Dazed, Unconscious or Poisoned effect is not removed merely because intoxication ends.

**NEW natural reduction:** At dose-driven scores 1–3, one complete hour without new Intoxication removes one point; repeat each hour. A new positive gain resets that hourly timer even if a direct floor conceals the dose-driven change. A timed floor itself does not stop underlying points declining. At score 4 use its specific timer; score 5 cannot decay naturally. After a reduction to 3 or below, begin the next hourly interval at that transition. A timed floor can prevent the effective score from dropping until that application ends.

**NEW level 4:** On entering effective score 4 (or returning from treated 5), roll 1d4 once and set that many hours as the recovery deadline. Make a DC 14 CON save; on failure add Poisoned caused by intoxication while effective score is at least 4. Unconscious from this track lasts until that deadline unless cured earlier. Ending Unconscious alone does not clear points or reset the deadline. Reapplying score 4 without leaving it does not reroll or extend the deadline. At its deadline, if alive and no emergency is active, reduce dose-driven score to at most 3 and end track-caused Unconscious/Poisoned. A generic cure explicitly ending Intoxication removes all its track/floor records and track-caused consequences.

**NEW level 5:** On entering score 5, set a fixed emergency deadline one hour later and become/remain Unconscious. A jump directly from below 4 to 5 starts the emergency immediately; the level-4 recovery timer and poisoning save begin only after successful care returns it to 4. Additional gains at 5 never reset or extend it. A helper may spend ten uninterrupted minutes and one healer's-kit use, consumed at start, then make DC 15 WIS (Medicine). Success before the deadline ends the emergency, sets the dose-driven score to 4, adds one Wound if below three, and begins the level-4 timer/save. At three Wounds, successful emergency care prevents death without creating a fourth Wound; this is a specific provisional exception for this treatment. This direct Wound has no Injury roll and does not itself trigger a Wound save. Wound immunity prevents that added Wound where applicable.

Failure leaves the original emergency and deadline; another fully paid attempt is possible if it can finish before that deadline. At the exact deadline, death takes precedence over an unfinished or simultaneously finishing generic attempt. No natural score reduction can clear the emergency. A reviewed effect explicitly removing Intoxication or the emergency can end it by its own procedure. An immunity to Unconscious or Poisoned does not, by itself, prevent the separate emergency or death state.

## Corrupted

Use the condition's half healing, individually recorded Evil-source save disadvantage, aura and DC 15 WIS long-rest save. A failed long-rest save shifts the moral axis Good → Neutral → Evil without changing law/chaos. Never infer Evil from ancestry, species, faction, homeland or appearance. This label change does not compel beliefs, behavior, PvP, party separation or automatic oathbreaking. Specific conduct clauses still judge actual conduct.

**NEW generic cleansing:** One practitioner spends eight uninterrupted hours with one patient in a secure location, consumes one Supply at start, and makes INT (Religion) or INT (Arcana) against DC 15 at completion. Success removes Corrupted. Failure leaves it without any extra automatic Wound, condition or Exposure. No more than one generic attempt may complete for that patient in 24 elapsed hours; practitioners cannot stack concurrent attempts. The practitioner is working, while the patient may rest if otherwise eligible. If cleansing and the patient's long rest complete together, resolve cleansing first; make the Corrupted rest save only if it remains. A specific reviewed cleansing spell/item uses its own costs and procedure.

Guaranteed one-HP recovery from a natural-20 death save or the Stable recovery clock remains one HP: these are state-recovery rules, not healing effects. Ordinary one-point magical healing can still be halved to zero. It nevertheless ends generic Bleeding if it had positive pre-reduction healing potential.

## Unity Exposure — public provisional track

The source defines a 0–6 track with erosion of distinction and identity but no operational numeric threshold table was found in the bounded Core/V6/Director and current reference searches. GPT also reported no owner-approved numerical table in its available notebook history. The following is **NEW candidate mechanics**, not recovered setting truth. It grants no public knowledge of the exposure's hidden causes or identities.

Use the current row only; do not add lower-row modifiers.

| Score | Mechanical effect |
|---|---|
| 0 | No effect. |
| 1 | Tracked, without a generic numerical penalty. |
| 2 | −1 Perception/Investigation checks specifically distinguishing similar identities, copies, duplicates or conflicting sensory impressions. Declare this scope before rolling. |
| 3 | −1 INT and WIS ability checks. |
| 4 | −1 INT, WIS and CHA ability checks. |
| 5 | Disadvantage on INT, WIS and CHA ability checks. |
| 6 | Disadvantage on INT, WIS and CHA ability checks and saves. The character remains playable with player agency. |

Record changes only from explicit reviewed effects; cap at 0–6. These mechanics never decide a character's beliefs, loves, loyalty, factual memories, conduct or hidden revelations. A player can portray blurred memories or identity pressure without surrendering character control.

**NEW Anchor Project:** In a secure Haven or equivalent safe location, complete three full consecutive project days. Each day the patient spends two hours affirming chosen memories, relationships or personal distinctions and consumes one Supply. The player chooses the content. At the end of the third full day, make a WIS save against DC `10 + current Exposure`, including the track's actual penalties. Success reduces Exposure by one; failure does not. A new reduction requires a new full project. Ordinary rest does not reduce Exposure.

Any successful positive Exposure-gain event during the attempt interrupts it, including a gain capped at 6; prevented gains do not. Already consumed Supply remains spent. Only one Anchor Project per patient can be active. Specific reviewed removal effects may work differently. Director context and later source reconciliation remain separately packaged; private narrative information does not silently add numerical penalties or erase player agency.

## Evidence and remaining integration

The exact first and second GPT reviews, Core condition definitions, complete V6 appendix, direct dependency passages, Guard text, and bounded source searches are retained in `docs/audit/2026-10-08/full-game` at the project root. The normalized entries retain exact Core text and book hashes. These generic procedures make recovery playable but do not finish every substance/item, cure spell, encounter hazard, source of Exposure, rest resource or Director scene. Their individual audits remain in the 75-area ledger.
