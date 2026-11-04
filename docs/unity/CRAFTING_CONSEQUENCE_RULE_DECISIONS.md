# Crafting consequences and outside-combat life markers

Date: 2026-11-03 owner session; receipts extend into 2026-11-04 UTC.
Status: source-bound PLAYTEST procedures and explicitly delegated prototype completions, C# first. No release promotion.

## Source and scope

The exact crafting framework's mishap table (`CRAFTING_HARVEST_PLAYTEST.md`, lines82–95), Alchemy row in `CRAFTING_TRADE_REFERENCE.md`, ordinary object structure/repair rules (`EQUIPMENT_ACQUISITION_PLAYTEST.md`, lines165–211), equipment identity `tools.alchemist-s-supplies`, and Core life/condition procedures supply this increment. The pinned source revision remains main `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; exact inherited snapshots/hashes are in [bindings](evidence/2026-11-03-crafting-consequences/SOURCE_BINDINGS.json).

Schema16 explicitly selects finite host-authored mishap occurrences. Each supplies an ID, exact time, lead, already-resolved d6 result and immutable original participant IDs. This exercises the consequences of an occurred mishap. It does not resolve an entire manufacturing order, debit its ingredients, roll/select its mishap, award/deny an implemented XP transaction or produce its output. The originating crafting executor must eventually perform those earlier steps atomically. A new event ID is not permission for arbitrary client damage.

The physical fixture supplies one ordinary 50gp/8lb Alchemist's supplies kit with maximum structuralHP5. Its actual load-bearing structure is an ordinary wooden case, with intact glass/metal implements; that composition and compatibility with the mishap's bludgeoning point are TEST_ONLY facts, not catalog text. Ordinary poison/psychic immunity remains. MaterialAC15 is separate from damage resistance; no Sunder roll is added to directly sourced mishap damage. At0HP the object is Broken, retaining identity, location, ownership, custody and mass. No rest or time advance repairs it. Kit portability, all equipment structure and actual repair work remain separate.

## Implemented consequences

| Result | Consequence | Required remedy/restriction |
| --- | --- | --- |
| 1 | Spilled workspace | One active hour of cleanup; station unavailable for ordinary productive use. Cleanup itself remains possible. |
| 2 | Miscalibrated primary kit | Two active hours by a proficient worker; another crafting check with that kit is blocked. No extra ingredients and no automatic research-check prohibition. |
| 3 | Tool damage | One compatible physical structural point through the supplied object's ordinary defenses. Missing implementation is never physical immunity and never a spill fallback. |
| 4 | Alchemy accident | Lead alone takes1d4 acid through actual defense, HP, Wound and zero-HP procedures. No attack, melee knockout or additional invented condition. |
| 5 | Fouled apparatus | One labor-hour per original participating worker. Station cannot support another crafting order, including resuming another order there, until cleanup finishes. Physically capable cleaners may work in parallel. |
| 6 | Lost trade log | Original lead alone spends one active hour before beginning another order in that trade. Existing formula knowledge remains. Source also denies that failed order's researchXP; no XP executor is claimed here. |

Restrictions are separate predicates, not a universal crafting flag. Broken tools and spilled stations interrupt the selected research job because it actually needs those tools/station. Miscalibration, fouling and lost notes do not themselves prohibit research/copying. Structural repair does not clear another incident's debt; recalibration does not restore HP.

## Delegated remediation completion

GPT response `b99725cd-ea92-56a5-a32f-64527c49a5da`, accepted by Codex in turn `4beda139-b85c-4c0a-94b1-2d08ced5edb7`, supplies these NEW provisional boundaries. [Exact exchange](evidence/2026-11-03-crafting-consequences/GPT_CRAFTING_GUIDANCE.json):

- Retain actual eligible person-seconds through pause, incapacity and restore. Resume explicitly revalidates capability, access, qualifications and a legal work window. Manufacturing's unfinished eight-hour phase loss is not imported into remediation.
- Only result5 permits parallel acceleration. Result1 uses one cleaner at a time, result2 one proficient recalibrator, result6 the original lead. Each worker's interval counts once, stops at completion and supplies no excess credit to another incident.
- Keep each obligation independent. Pausing an assignment does not erase it; completing one incident does not clear others. Supplied public event identities are separate from generated internal reservation job identities.
- These remedies have no completion check. Final lawful labor completes once before endpoint incapacity can erase earned work; no additional conscious action or roll is invented.

The selected fixture supplies access to the plot station, at least one available hand for these tasks, companion Alchemist-tool proficiency and an optional explicit hero proficiency. It supplies two legal work windows `[0,8h)` and `[8h,16h)`; no unlimited work, rest benefit or global day anchor. Recalibration checks current tool-owner permission at command/resume/duplicate boundaries. Other labor uses actual exclusive worker bookings. Tactical participation pauses that participant; compatible remote work continues. Synchronous one-second handling is gated if it would cross an unhandled remedy or death-save boundary.

## Outside-combat life cadence

The earlier [shared-world policy](SHARED_WORLD_RULE_DECISIONS.md) already adopted established virtual Starts, or onset+6seconds and every6seconds when an actor lacks a schedule. Schema16 now makes these paths reachable through the sourced accident. A fixed actor uses its next genuine Start even when injury occurs less than6seconds before it; no encounter is created merely to process dying. The off-roster companion persists its onset and next ordinal. Entry, mode changes and save/load neither rebase it nor start another series.

At an admitted boundary: credit eligible work, apply condition expiry, perform permitted absolute Stable recovery, then resolve due death saves before later research checks. Stable, Dead and positive-HP actors do not roll. Natural20 recovery preserves physical Prone and independent conditions. Incapacity interrupts incompatible jobs under each job's own retention/settlement contract; later recovery does not resume them automatically.

GPT response `cbffe305-2a90-5512-b610-550e186a3e07` confirms the NEW fixed-fixture tie completion: existing-calendar due actors precede off-roster actors ordered by stable actor ID, subordinate to established expiry/recovery ordering. Eligibility is evaluated after those transitions. Each actual death save receives a global audit sequence; due scheduling never uses that sequence as a clock. A separate persisted logical marker retains actor, calendar ID, origin, ordinal and exact time, including after the dying episode ends. Calendar/fallback cursors and canonical replay prevent a second save for the same processed marker.

## Qualification and next dependency

The894-case C# suite includes30 new consequence/marker/remedy checks, real dying/broken-kit/partial-remedy disk saves, current authority, fixed versus fallback cadence, chunk equivalence, same-time order, Stable recovery, independent unconsciousness, finite work windows, parallel join/leave and pending-knockout gating. Independent review found and reproduced a cross-subsystem job-ID collision; generated internal remedy IDs and a permanent lawful regression close it. [Evidence](evidence/2026-11-03-crafting-consequences/HEADLESS_RESULTS.json) states the final tested hashes and review scope.

The separate repair helper computes this ordinary kit's12gp5sp materials, one active hour and DC10 task result. It does not implement repair jobs, material settlement, toolkit/ability eligibility or repairs while interrupted. Actual repair is the next dependency, then a current reviewed recipe through all reachable manufacturing outcomes and actual product use. General hazards, source acquisition, arbitrary object profiles, changing rosters, general spells/abilities, complete content and Unity integration remain unfinished. The engine is not complete.
