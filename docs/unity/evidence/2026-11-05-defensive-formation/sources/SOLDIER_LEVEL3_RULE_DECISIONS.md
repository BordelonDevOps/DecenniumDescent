# Soldier level 3 feature decisions

**Status: three source-legal pairs are implemented in opt-in schema34 TEST_ONLY Soldier fixtures.** Tactical Assessment + Command Step, Tactical Assessment + Suppression Fire, and Command Step + Defensive Formation execute through level-three advancement, tactical commands, persistence and replay. Suppression Fire is intentionally bounded to one authored area and one known target; it is not a general area-targeting implementation. These source cards remain provisional playtest content; this record is not release approval.

## Pinned source

The class data and common card timing rules are pinned to Engine base revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
`pwsh -NoProfile -File engine/tools/Validate-ClassAdvancementSchedule.ps1` passes against those pinned Git blobs, confirming the projected schedule and option catalog used for the three pairs below.

| Source | Blob | SHA-256 | Scope used |
| --- | --- | --- | --- |
| `DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json` | `c414a1d9ba2ce37cde89d0ef73265821bb74ac2d` | `ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0` | `/schedule/2`, `/cards/10`, `/cards/16`, `/cards/18` |
| `DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md` | `5a446dd0dabae096e51f419b5e71756e0169bb3b` | `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81` | Class-card timing, Recharge counters, and level acquisition |
| `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md` | `72bcb58af57f8bfe27596ec0b1467e4c780a6ef8` | `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6` | Shared action budget, attack legality, cover, sight, and reactions |

## Level 3 advancement row

- Soldier level 3 grants two distinct Arch selections, at least one active card, and no ASI/feat operation in the pinned schedule row.
- One source-legal pair is **Tactical Assessment + Command Step**. Tactical Assessment satisfies the active-card minimum; Command Step is a passive triggered selection.
- A second source-legal pair is **Tactical Assessment + Suppression Fire**. It is a separate choice combination; reversing IDs in the request is only canonical ordering.
- A third source-legal pair is **Command Step + Defensive Formation**. The source schedule still requires at least one active card; Defensive Formation satisfies that requirement, while Command Step is the passive selection.
- The level transition, fixed-average d10 HP increase, new unspent d10, both grants, milestone consumption, and advancement audit must commit atomically. Source-row legality alone must not grant either feature.

## Codex/GPT consensus completions

These implementation details were agreed in **Unity Rules Engine Development** under the owner's standing instruction to proceed when Codex and GPT agree. They complete gaps in the card text; they are provisional prototype policy, not quotations from the source.

### Command Step

- Offer it after a Soldier completes an Action and its outstanding choices, once per numbered round on that Soldier's own turn.
- The offer names an adjacent willing ally and remains linked to the Action that created it across save/restore. Resolve or decline it before another voluntary command or turn end.
- The ally chooses whether and where to move. Declining closes that offer without spending the once-per-round use. An invalid destination also spends nothing. A legal acceptance spends the use; if no use has yet been accepted, a later qualifying Action in the round can open another offer.
- Grant an independent 5-foot movement allowance; do not debit the ally's ordinary movement ledger. Reuse the tactical step's destination, occupancy, terrain, and travel checks. Suppress opportunity attacks while preserving existing Press and Overwatch processing. The ally spends no Reaction and gains no Action or attack.
- The schema32 regression verifies an ally can move one legal 5-foot cell without debiting ordinary movement, and covers invalid terrain, decline, repeated offers, pending-offer save/restore, accepted-move save/restore, once-per-round use, and the originating Action link. Opportunity attacks are suppressed; ordinary Press/Overwatch processing remains in the shared movement flow.

### Tactical Assessment

- Use the Soldier's existing shared Bonus Action. On a legal activation, set Recharge 3; decrement it at each of that Soldier's regular starts using the common class timing rule.
- Require a visible enemy within 60 feet using the existing sight and range checks. Only a paid activation reveals the enemy's current armor category and whether it has cover from the Soldier's position; an unpaid preview must reveal neither.
- Choose and persist one ally and the assessed enemy. Add +1 to that ally's first legal attack against that enemy, hit or miss, through the end of the Soldier's next regular turn. The attack modifier must be captured by every admitted attack route, including reactions, and consumed only when the attack is actually attempted.
- Do not expose hidden statistics, vulnerabilities, or other information. Armor and cover must be derived from authoritative simulation state or explicit, source-bound fixture facts, never accepted as caller-declared command results.

### Suppression Fire

- Use the Soldier's Action, three loaded bolts, a 15-foot square within weapon range, up to three perceived enemies, and the existing DEX save path. It makes no attack roll and creates no on-hit technique effects.
- The pinned card gives `S d6` piercing damage, where `S` is the Soldier level, half damage rounded down on success, and a 10-foot Speed reduction on failure. In the level 3 fixture, the save DC must come from the existing ability/proficiency calculation.
- Apply the one-shot save/damage/slow effect once for the volley; do not create repeated entry pulses. The general card duration says “Until start next turn” while the slow text says “through end next turn.” The specific slow endpoint is the Soldier's next regular-turn End; record this timing interpretation in the implementation audit before enabling the feature.
- Reuse existing range, perception, cover, save, damage, condition, and action machinery. Reject full-cover targets and preserve ammunition costs and save results in replayable records.
- **Area placement boundary:** the pinned card says “15-foot square within weapon range”; it does not establish a creature-centered, corner-anchored, or rotatable grid template. The pinned combat geometry rule supplies a five-foot orthogonal/diagonal measurement metric and leaves exact area templates for further review. The prior fixed axis-aligned Overwatch footprint is explicitly a fixture restriction and does not settle Suppression Fire placement. GPT review confirmed there is no adopted general anchor/orientation rule.
- The opt-in TEST_ONLY fixture therefore uses one authored axis-aligned 3×3-cell square (nine 5-foot cells), centered on cell `(4,0)` with footprint `x=3..5, y=-1..1`, and only the fixture's known target. The volley record saves this placement at activation; it does not track a target that later moves. That placement is a fixture convention, not sourced player targeting. General player-selected placement, orientation, boundary inclusion, multiple-target perception/cover and multi-target resolution remain unimplemented.
- The bounded handler resolves Soldier level 3 as one shared 3d6 roll, applies each target's DEX save and damage separately, charges three actual loaded bolts and one Action, sets Recharge 3, and records the slow until the Soldier's next regular-turn End. The regression verifies the recharge counter ticks at the next regular Start and reaches zero after three subsequent Soldier starts. The current fixture admits one target despite the card's “up to three” ceiling; do not describe that as full multi-target support.

### Defensive Formation

- Activate once per encounter as a Bonus Action. Select one to three willing allies within 15 feet; the bounded roster currently supplies only the Soldier and one companion. Apply the formation benefit immediately, then resolve each selected recipient's optional shift in selection order.
- Each recipient may decline or shift up to five feet using one legal adjacent step. The shift is an independent movement allowance and grants no opportunity attack. Revalidate actor capability, destination, occupancy, terrain and special-movement cost when the response is submitted. If a recipient cannot move, skip that recipient and continue the sequence.
- Keep the benefit active for all selected recipients through the Soldier's next regular Start, including recipients who decline or cannot shift. At damage resolution, reduce damage by one while a recipient is adjacent to another recipient from that activation. Recompute adjacency from current positions; this reduction does not stack with Shield Trained's same-strength reduction.
- Existing Press and Overwatch continue through their shared movement procedures after the shift; they do not convert the shift into ordinary movement. Mode switches do not refresh the once-per-encounter use.
- The schema34 regressions cover the third legal advancement pair, pure Bonus Action query, hostile-recipient rejection, selection order, accepted and declined responses, five-foot shift without opportunity attacks or ordinary movement debit, dynamic adjacency, nonstacking reduction, unable-to-move skips, pending-choice save/restore, exact next-Start expiry and one-use enforcement. The full suite and current source-binding record are in [schema34 verification evidence](evidence/2026-11-05-defensive-formation/README.md).

## Implementation gate and current gap

Schema32 enables **Tactical Assessment + Command Step**, schema33 enables **Tactical Assessment + Suppression Fire**, and schema34 enables **Command Step + Defensive Formation**. Advancement records are validated against the actor's chronological history; grants and feature state survive save/restore and replay. Tactical Assessment is encounter-only and obtains bounded armor/cover facts from admitted tactical state. Command Step opens after a completed Action and its outstanding choices, allows an adjacent willing ally to decide, preserves the offer and response, and consumes the once-per-round use only on legal acceptance. Suppression Fire is limited to the authored center/footprint and single known target described above. Defensive Formation is limited to the shared Bonus Action ledger, one use per encounter, the fixed two-allies test roster and the ordered shift semantics above.

Other level-three Arch candidates remain catalogued but are not executable by virtue of being in the source row. This increment does not implement general advancement for every class, complete the Soldier class, or finish the full game engine. Unity Editor compilation and gameplay validation have not run.

