# TAC-06 selected resurrection: source/API and prerequisite gate

Status: PROPOSED FOR GPT REVIEW. This is a contract and capability audit, not resurrection implementation or engine completion. Baseline Engine is `2082003073be9124e7a3e6c15113828cceee56e6`. Flesh Warden source `0742794a7c1f8e15dd4e38ff72ae21dd61762b4a` and final evidence `16984cdf3d79450d42880140dacaa69634c8ae42` were accepted in actual GPT response `7b1e6b05-b5aa-5853-9cae-0bb428e20edb`. Codex agrees with that acceptance and the next TAC-06/DD-24 source/API gate. No successor C# source has changed. Unity gameplay integration stays deferred.

## Selected source and authority

Select the authored **Cleric / Saint / Resurrection** card, canonical identity `cleric.hero.saint.resurrection`, solely for the proposed TEST_ONLY integration. It is distinct from the ordinary rank-7 spell named Resurrection, Celestial Resurgence, Divine Rebirth, and would-die replacement. `SOURCE_API_BINDINGS.json` binds the exact files, selectors, Git blobs and SHA-256 values. The ReviewBible revision is `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; the binding verifier compares those bytes with baseline HEAD.

The manifest and promotion policy remain the authority registry. The selected class card is marked `provisional-playtest`, its enclosing document `provisional-card-draft-not-balance-approved`. The healing binding calls only its classified components REVIEWED/reference-VALIDATED. This is neither approved release authority nor proof of a working C# card. Historical source-wide spell counts and pending labels do not decide this exact class procedure, and the Director rank-9 overlay does not apply to it. Source originals are preserved.

| Requirement | Exact selected rule |
|---|---|
| Acquisition | Cleric class level at least 16; Saint Hero path; selected eligible Hero card under the actual class schedule. Total level, a display name, or pooled RP does not grant it. |
| Activation and payment | One Action, 3 Conviction and 10 RP; at most once per qualifying Long Rest. Conviction and the character's shared RP pool are separate. |
| Target | One actually dead, willing allied identity; touch its sufficiently present vital body, with legal perception/line of effect. No living/downed target or bodyless reconstruction. |
| Window | Death at or before the current shared clock; elapsed time at most 60 seconds, inclusive. Rounds and encounter start cannot replace the timestamp. |
| Return | Same identity returns at 1 normal HP; clear death counters, Stable flag and deadline. Preserve used turn markers, Wounds/Injuries, source histories and other retained consequences. This is a life transition, not ordinary healing. |
| Temporary HP | Grant `2*S + M` for one minute, with S from actual Cleric level (3 at 16) and M=max(1, actual Wisdom modifier). Apply nonstacking temporary-HP rules and retain its independent source/expiry. No HP roll is printed. |
| Dissonance | Actual payment of at least 2 Conviction on this Rite may vent 1, minimum zero, at most once on each regular turn under the Cleric rule. No automatic ordinary-spell Dissonance, Overcast or rank benefits. |
| Persistent state | Do not restore resources, other uses, Wounds, Corruption, intrinsic curse, debts/legal-death/body claims, equipment or looted stock. No duplicate body/identity/loot/XP/Conviction. |

Cleric engine `/engine/1` sets base Conviction maximum 3, increasing automatically to 5 at Cleric 9. Conviction Pool adds 2 only if actually owned; gained capacity does not fill itself. A completed Short Rest restores 1 spent Conviction; a qualifying Long Rest restores all. Prayer, scene transitions, staged deaths or harmless actions generate none. `/engine/3` pays the class technique from the character's Core RP pool. CHARACTER_CREATION_PLAYTEST specifies one merged RP pool and separates capacity changes from recovery. We must not create a second Cleric RP balance alongside it.

The eventual bounded source excludes unowned Divine Rebirth rather than silently applying its half-maximum replacement. Any later profile that owns it needs its own real optional trigger/use integration. Unknown modifiers, blockers or resource tracks cannot be defaulted to zero by a purported general resurrection API.

## Current connected capabilities and concrete gaps

The dependency map lists TAC-04, TAC-05 and MGT-02 directly under TAC-06. Their selected implementations provide damage/death, conditions, shared actor identity, scheduling, command receipts and persistence. Those IDs are not claims that every source-specific dependency is complete. The audit is pinned to the files listed in `SOURCE_API_BINDINGS.json`.

| Concern | Current evidence | Required connected work |
|---|---|---|
| Numerical class/RP facts | `PlaytestCharacterBuild.MergedRp` calculates capacity; `CharacterProfiles` has Cleric pools. The helper expressly grants neither current RP nor access. | Shared persisted current RP, source-bound initialization/recovery/payment and retained history; source acquisition separately. |
| Card acquisition | The catalog contains Cleric Resurrection. `SharedCharacterAdvancement.Assess` accepts only the bounded Soldier paths; shared grants validate Soldier choices. Flesh Warden fixture entitlements are exact Warrior exceptions. | Lawful Cleric levels, Saint selection and card grant in the shared character history, with actual eligibility. No mutation entitlement reuse, fabricated milestone, or catalog-name ownership. |
| Class resources | Runtime/model search finds no shared spendable RP or Conviction ledger or Cleric Dissonance cadence. | Atomic finite RP/Conviction payment, capacity and use history, actual regular-turn vent, qualified rest recovery. No fresh pool on entry/return. |
| Death identity | `ActorLifeRecord` has Dead/counters/Stable/used turn but no death occurrence ID/time or body/soul eligibility. `ActorLifeEvent` covers StableRecovery/DeathSave. Harvest donor `DeathAt` belongs to a harvesting lifecycle. | Record genuine actor death occurrence and its shared-clock marker; bind that identity to the lawful body without treating an arbitrary harvest donor as an actor corpse. |
| Body, willingness and blocks | Existing handover consent is inventory authority, not post-death identity consent. No connected resurrection eligibility interface was found. | Source-qualified host authority for willingness, body vitality/location, identity availability and applicable corpse-local/soul blocks. Unknown authority is unsupported, not false. |
| Consequences after return | Existing HP, injury, condition, expedition Strain and temporary-HP state are shared. Consume Decay has its own source-specific grant history. | A separate revival transition; source-specific temp grant; reconcile retained lethal tracks and scheduling without refresh. Do not route through ordinary `Heal`. |
| Rest cadence | Completed Short Rest is accepted for its bounded profile; wider rest rewards/class recoveries are not thereby implemented. | Once-per-Long-Rest entitlement must refer to a real qualifying reset or explicit supported initial provenance; no refund from death, save loading, scene changes or short rest. |

The existing numerical Warrior hero and Soldier companion are not a Cleric 16. Replacing their class facts or supplying a fixture Resurrection grant would bypass the identified gameplay dependency. This contract proposes neither. It does not yet reserve wire105 or add a start-profile option.

## Proposed dependency order and next concrete gate

Do **not** implement Resurrection immediately. Keep it selected and blocked on the above capabilities. The earliest missing prerequisite is the mapped **CHR-02 connected class-entry/access and shared RP lifecycle**. Propose its separate source/API contract next, starting from the existing ordered class facts and capacity calculator and determining one lawful, paid connected route. A bare balance schema or finite-looking initial fixture is not acceptance of that lifecycle.

Preserve the map's other edges: CHR-05 depends on CHR-03, TAC-02, TAC-05 and TAC-08; TAC-08 depends on TAC-02, TAC-05 and TAC-07; TAC-07 depends on CHR-02 and FND-05. The selected Cleric technique is not an ordinary spell, but that distinction does not silently waive mapped class-engine prerequisites. After the CHR-02 contract, identify the smallest source-specific slices needed along those edges, submit each concrete contract, implement and obtain acceptance separately, and then return to the TAC-06 resurrection command. Broader work-item completion is never inferred from a bounded slice.

Ask GPT to agree or correct this first prerequisite gate and the remaining dependency sequence. No entire chain is preauthorized by this proposal. In particular, the next deliverable is the CHR-02 contract, not an unreviewed Cleric engine or general spell system.

## Eventual transaction contract (not implementation authorization)

The proposed public operation is a typed source-specific request `UseClericResurrection(targetActorId, deathOccurrenceId)` through the existing session/command/receipt machinery. Names are provisional. Actor identity, source ownership, costs, returned HP, time, willing/body/soul facts and resource balances are derived from validated shared state and host authority; the request cannot assert them. The selected death occurrence prevents a stale request from addressing a later death of the same actor.

Admission must use current seat/actor authority before duplicate handling. Query is read-only. Validate supported profile/source, actual Cleric/Saint/grant, consciousness/conditions, physical touch/perception/line of effect, target identity and exact death occurrence, inclusive window, body/soul eligibility, Action, finite pools and per-rest use. A generic boolean `sourceEligibilityMet` supplied by the client is insufficient. Unsupported authoritative facts return a named unsupported capability result; do not spend or invent them.

For the fully admissible case, atomically debit Action, 3 Conviction, 10 shared RP and one source use, apply any legal once-per-regular-turn vent, perform the same-identity return at 1 HP and the one-minute temporary-HP grant, and persist one causal result. These printed effects draw no RNG. Damage causing death still uses the real shared RNG and damage/condition resolution. Duplicate receipt retry cannot pay, vent, revive or grant again; a conflicting payload is rejected.

Death must originate in the real simulation. Resurrection preserves linked Wounds/Injuries, actual inventory ownership/location, dropped items, spent Action/Bonus Action/Reaction histories and past turn markers. It does not clone a roster slot or roll initiative again. Scheduling resumes only through an explicitly reviewed rule using the shared calendar, with no free current turn. Retained expedition Strain 6 keeps all provenance and collapse; later positive gain reevaluates the lethal endpoint. The documented Core Exhaustion 6 protected return must either be supported explicitly or reported unsupported for that profile. Do not claim absence of an unrepresented track proves a general zero value.

Persist the death occurrence, body/identity association, authority provenance, source grant, payment/use/vent record, transition and temporary grant with strict validation and deterministic replay. Exact public schema/fingerprint and scheduling policy await prerequisite contracts. Authentic wire95-104 saves keep their byte layouts and behavior; no migration invents new Cleric or resurrection facts. A forged or incomplete history is rejected rather than repaired.

## Payment ambiguity requiring actual consensus

CLASS_PLAYTEST_RULES first says to satisfy ownership, prerequisites, targets, action, recharge and costs before spending and that illegal activation spends nothing. Its later resurrection paragraph says resurrection never refunds on failure to meet known prerequisites. The Python `resurrection_transition` requires external source validation but raises an eligibility failure with the phrase `no automatic cost refund`; it does not model payment. These passages do not define a complete hidden-blocker attempt protocol.

Propose the initial API only admits the fully host-validated legal transaction described above. Known invalid and unsupported preflight requests reject unchanged. A completed legal payment is never refunded by the pure life transition. A paid attempt that discovers hidden/contested eligibility later remains explicitly unsupported until its source/knowledge/payment boundary is reviewed. This is a proposed bounded policy, not a silent rewriting of the conflicting sentence. GPT must accept it or provide the precise alternative before runtime work.

## Eventual acceptance, evidence and exclusions

The required witness must reach a lawful caster through accepted connected prerequisites, explore and encounter real opposition, sustain genuine death of the same allied actor, physically reach the valid body in the inclusive time window, pay the real resources and Action, return at printed HP, preserve consequences, and continue by a paid command. Retain acquire/manage/prepare connections and the same inventories/work/clock; do not replace death, access or funding with test setters. Observe and report the resulting route rather than prescribing lucky dice.

Save before death, dead/in-window, immediately before payment, after return, after temporary-HP expiry and after paid continuation. Compare uninterrupted, save/restored, receipt replay and direct typed C# paths byte-for-byte. Show paid depletion and actual cadence denial, exactly-once payment on retries, real death RNG continuity, no resource refresh and no second actor/body/loot. If a required boundary cannot be reached on the connected path, label detached controls honestly and leave that connected requirement open.

Controls must cover living/downed/Stable targets, wrong occurrence/identity/source/grant/actor, unwilling or unavailable soul, missing vital body, out-of-touch/cover, exactly 60 seconds and just beyond, insufficient RP/Conviction, spent Action/use, nonzero applicable Dissonance vent with duplicate/turn limits, retained wounds/conditions/lethal-track collapse, stronger existing temp HP and independent expiry, and identity/body duplicate prevention. Unknown states must not masquerade as legal negatives. Include malformed histories, current-authority-before-retry, stale/conflicting commands and unchanged full state on preflight rejection.

After implementation, compile standalone C# 9 with warnings as errors, pass all package checks, preserve all 1,503 accepted cases and add the meaningful new connected/regression controls. Retain exact source/assembly/run hashes, authentic wire95-104 continuation, public/typed transcript/checkpoint evidence and exact-file commits. Present actual reports to GPT and wait for acceptance. No new compilation or runtime test is claimed for this documentation-only gate; the accepted predecessor evidence remains linked from the baseline handoff.

Ordinary Resurrection/True Resurrection, other Cleric cards, body reconstruction, cosmology answers, general class/spell completion and production authority remain outside this contract. Records, helpers, source-binding checks and reviews are supporting evidence, not playable resurrection or engine completion.
