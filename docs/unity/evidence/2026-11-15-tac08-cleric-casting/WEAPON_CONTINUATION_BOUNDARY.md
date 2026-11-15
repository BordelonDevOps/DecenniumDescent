# TAC08 genuine caster weapon continuation boundary

Actual checkpoint review `ab86f808-3d58-5629-8796-57523b2b5f73` requires genuine nonzero Refrain across the caster's idle and weapon-action intervals and explicitly requests the precise boundary if the selected host cannot admit that weapon continuation. The new actual branch starts through the normal declared profile, exploration/work/first conflict and paid reinforcement. It casts Guidance twice on separate caster turns, retains Refrain1/Dissonance1, then crosses a real caster idle interval. At revision145, Refrain remains1, Dissonance is0 and the last cast revision remains131. Save/restore of this actual state succeeds. No HP, RNG, held item, known spell or receipt is injected.

The actual Cleric club attack then rejects with `ClubNotHeld`. The selected companion owns and has custody of `TEST_ONLY.companion-club`, but it remains unheld at the initial plot `(3,3)`. The caster is now `(1,3)` beside the living defender `(0,3)`, has8HP and no held items. This is not an attack-range or Action failure. The hero still holds its own club; its attacks cannot stand in for the caster's required weapon interval.

Three direct query/execution controls reproduce the boundary against the unchanged previously frozen Core/Persistence/LabModel DLLs, independently of the in-progress controller correction. All retain identical before/after bytes:

| Actual request | State | Query and execution |
| --- | --- | --- |
| Cleric AttackClub with its supplied club | Genuine restored revision145 | `ClubNotHeld` |
| Pickup of that owned grounded club through HandlePortableEquipment | Declared revision0, actor and club both at `(3,3)` | `UnknownPortableItem` |
| EquipPortableItem for that same club | Declared revision0 | `UnknownPortableItem` |

[Retained boundary report](review-correction/weapon-boundary/results.json), generated C# harness and six unchanged snapshots retain the exact state and binary/source hashes. The actual pre-idle/after-idle saves and the attempted enhanced Foundation case's failed report are retained alongside them. The failed attempt also exposed a test compilation typo (`CombatAttackRoll.WordsConsumed` instead of its existing `Words` property); that first compilation failure remains in local development reports and is not a pass.

The existing source explains the limitation:

- `TestOnlySharedWorldPolicy.Initial`, lines165–167, deliberately leaves the remote worker's supplied club grounded and clears its held list so both hands are free. This is a settled initial fact, not a lost item to repair silently.
- `SharedPortableEquipment.ResolvePortableEquipment`, line133, requires a matching `PortableEquipmentRecord` and returns `UnknownPortableItem` for this legacy `ClubInstance`. The item has no corresponding portable record.
- Existing club mutations update initialized/moving/grounded equipment; no admitted command retrieves this grounded legacy club into the caster's hands.
- `ClubInstance` stores identity, profile, ownership, custody, held actor and cell. It does not itself provide a portable mass or storage-volume fact. No additional physical quantities are inferred here.
- The already adopted `INVENTORY_RULE_DECISIONS.md` sectionA supplies ordinary accessible handheld pickup/drop timing: one active second in exploration, or the existing tactical interaction/Action allowance. It preserves ownership, actual access, hands and capacity. It does not itself wire this legacy weapon into the host.

Codex recommends resolving this as a bounded source/API integration: a genuine, paid pickup of the existing owned grounded Club before tactical entry, using the already adopted ordinary handling procedure and actual shared custody/location/hand state. Do not grant another item, alter revision0 held equipment, add free grip changes, infer storage volume or invent mass/Load facts. The exact admission, physical-source/capacity treatment, history and compatibility requirements need GPT agreement before that dependent implementation. A general weapon catalogue, storage or handover feature is not proposed by this boundary report.

No unarmed substitution or detached held-club edit has been used to claim the required weapon witness. Please settle the exact bounded integration needed for this genuine continuation, or explicitly revise the acceptance requirement if the existing physical-source scope cannot support it. The caster weapon witness is presently **not demonstrated**.

Independent blocker1 is corrected in the working tree: the opportunity selector now honors `DirectAttackAllowed`. The enhanced genuine Sanctuary regression passes, including the second occurrence, completed parent, unchanged RNG/save count, preserved Reaction and restore/replay. The same retained-save external reproduction changes from `AcceptOpportunity`/Unavailable/pending at revision130 to `DeclineOpportunity`/Committed/completed at revision131, with unchanged RNG1652186263 and one save. These are targeted correction results, not a new complete source freeze or full regression qualification.
