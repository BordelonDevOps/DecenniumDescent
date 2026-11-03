# Ordinary attack integration guidance

Recorded 2026-11-03 after Engine `0035d42bd85c65d64faff1183bdeac64bbb2ae2e`. [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `280da3e2-62af-58cc-943e-e38e050ef698`. This is source/engineering guidance, not a new owner approval or a review of the latest code. GPT inspected the older `ac01b64a` checkpoint; its identified whole-second recovery issue is now corrected and reviewed in the478-case exact-life checkpoint. Actor life persistence, stance/Press state, conditional reaction decisions and attack execution remain unimplemented.

**Character/life persistence and spatial preflight are the right next dependency.** Existing rules support a bounded ordinary attack on a flat, unobstructed map. General 3D geometry and arbitrary exploration-position conversion still need decisions.

I checked the pushed Engine sources at `ac01b64a`; this is source guidance, not a review of your uncommitted schema7.

“Existing rule” below includes reviewed playtest amendments. It does not mean every clause was recovered from the original books.

**Geometry already settled, and its limits**

| Question | Existing authority | Remaining boundary |
|---|---|---|
| Grid versus continuous | `COMBAT_ACTION_PLAYTEST` §Movement and geometry explicitly makes every orthogonal **or diagonal** neighboring tile 5 ft and uses that metric for ordinary ranges/areas. This is an authored playtest rule. | `VIDEO_GAME_ONLY_DIRECTIVE` permits precise digital geometry; it does **not** globally replace this intentional metric with Euclidean distance. |
| Elevation and distance | Actual height matters; transformations and lost flight preserve actual location. | No general ordinary-weapon rule located here specifies arbitrary 3D distance, body measurement points, vertical reach or a vertical extension of the diagonal metric. |
| Occupied space | Nonhostile occupied space is difficult terrain; hostile passage requires the stated size difference or an exception; voluntary movement cannot end in occupied space. Both blocked orthogonal sides prohibit diagonal **movement** through the corner. | Do not turn movement connectivity into a complete line-of-effect algorithm. |
| Body footprint | `BODY_EQUIPMENT_PLAYTEST` §Placement and involuntary endings supplies Tiny 2.5×2.5, Small/Medium 5×5 and Large 10×10 ft. | Footprint does not determine body height, exact silhouette or a universal large-body range measurement method. |
| Exploration → combat | The development brief requires preserved positions, occupancy, hazards, resources and effects; entry cannot grant movement through barriers. | An arbitrary continuous-position-to-grid conversion is not settled. Already aligned shared positions avoid needing that conversion in a fixture. |

Sources: [Combat §§Movement and geometry; Cover, sight, Hide and Search](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#movement-and-geometry), [Video-game directive §§Geometry; Preserve Source Fidelity](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md#geometry), [body placement](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#placement-and-involuntary-endings), [development brief](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/docs/unity/DEVELOPMENT_BRIEF.md).

The later accepted Euclidean/body-volume interfaces are **scoped exceptions**: registry06 entries `DC25-SHARED-digitalGeometry` and `P20-DIGITAL-GEOMETRY-01` expressly limit themselves to their named spell cohorts. They cannot supply a missing global weapon rule. See [accepted interface registry06](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json).

**The smallest ordinary attack still needs these mechanics**

1. **Validate actor, equipment and target before committing.**
   Use actual action permissions, conditions, weapon custody/readiness, hands, proficiency, weapon properties and target AC. Melee requires actual reach—normally 5 ft; the Reach property adds 5 ft. Ranged attacks beyond normal through maximum range have disadvantage; beyond maximum is illegal. A nearby non-Incapacitated hostile that sees the attacker imposes the ordinary ranged disadvantage.

   Visibility, known location and line of effect are separate. Total cover blocks direct targeting; half/three-quarters cover gives +2/+5 AC, using only the best cover. A transparent barrier does not automatically permit an attack through it.

   Sources: `COMBAT_ACTION_PLAYTEST` §§Cover, sight, Hide and Search; [Equipment §§Armor and shields; Hands and focuses; Weapons and ammunition](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md#weapons-and-ammunition). Underlying V6 paragraph 8194 supplies ordinary melee reach.

2. **Spend the existing Action and apply the selected stance.**
   V6 paragraph 8156 supplies one attack absent an actual multiple-attack grant. `COMBAT_ACTION_PLAYTEST` §Standard Actions preserves class/weapon-granted attacks. This consumes the same Action already shared with Dash and the second interaction; it adds no separate elapsed second.

   **Stance selection is required**, before the first event using its benefits/restrictions. There is no sourced neutral default. For example, Aggressive changes both attack damage and AC. Also, §Maneuvers and ordinary attacks says a regular-turn melee hit arms **Press** through the next regular start. A melee attack implementation must retain that entitlement, even if the fixture never triggers following movement.

3. **Resolve applicable choices at their actual windows.**
   An ordinary attack does not create a generic defensive Reaction. Nevertheless, actual eligible protections cannot be silently declined:
   - **Interpose:** while Guarding, after target selection and before the roll; its replacement target must be legal.
   - **Guardian Pulse:** its own retargeting procedure, before comparing the original roll with AC.
   - Applicable Ready triggers, damage prevention/transfer and survival features retain their individual timing and choices.

   An opportunity attack normally requires voluntary movement out of seen hostile reach; simply attacking does not trigger it. A fixture may explicitly contain no eligible reactive features, Guard/Ready states or movement triggers.

   Sources: `COMBAT_ACTION_PLAYTEST` §§Ready, Maneuvers and ordinary attacks; [Damage sharing §§Resolve the kind of protection first; One transfer operation and exact amounts](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/DAMAGE_SHARING_PLAYTEST.md).

4. **Roll using the actual modifier and RNG.**
   Attack is d20 + applicable ability modifier + PB when proficient, plus legal modifiers. Meeting AC hits; natural 1 misses; natural 20 hits and doubles damage dice, not flat modifiers. Advantage/disadvantage uses two d20s; any presence of both cancels.

   Ordinary weapon damage uses its specified dice and the same ability modifier used for the attack, subject to explicit exceptions. Finesse permits STR or DEX for both; thrown melee weapons retain their melee ability rule. Ammunition weapons consume a real compatible unit per attack.

   Sources: [Core §Rolls](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md#rolls), Equipment §Weapons and ammunition; [exact source packet](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/docs/audit/2026-10-08/full-game/COMBAT_ACTION_VISION_SOURCE_PACKET.json), Core paragraph 459 and V6 paragraphs 8172–8180, 8230–8243.

5. **Apply actual defenses, then the complete reachable life consequences.**
   Resistance halves matching damage; vulnerability doubles it. The shared class rule uses the strongest applicable class flat reduction before resistance. Do not generalize that ordering to every item, spell or protection: damage-sharing procedures distinguish pre-defense, post-defense and pre-temp-HP stages.

   For the ordinary unprotected life path:
   - Temporary HP absorbs first; preserve uncapped post-temp damage.
   - Check Instant Death before the Wound branch.
   - Make one Wound save for a positive-to-zero drop, post-temp damage at least half maximum HP, or actual Maiming.
   - Wound DC is `max(10, floor(postTempDamage / 2))`; apply the **pre-event** Wound penalty.
   - Resolve linked Injury, fatal existing-three-Wound failure, already-zero damage failures and the surviving zero-HP outcome.
   - Preserve the legal melee knockout choice. It cannot override Instant Death or fatal Wounds.

   Later survival amendments insert their exact prevention/replacement windows; `PlaytestLife.Damage` alone is not their dispatcher. See [Core §§Resolve a damage event; Zero HP and recovery](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md#resolve-a-damage-event) and [Healing/death §Damage quantities and resolution](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md#damage-quantities-and-resolution).

6. **Project life changes into the actor and shared world.**
   Ordinary zero-HP Unconscious includes Incapacitated, dropping held items and falling Prone. It affects action legality, attack modifiers, concentration and subsequent hits. These cannot remain decorative flags around an HP number. Healing does not automatically stand the actor up or remove independent condition causes.

   Source: [Conditions §§Incapacitated; Prone; Unconscious](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md#unconscious).

**My engineering recommendation**

Implement persisted actor life and exact recovery timing first, followed by planar attack preflight. One concrete issue is already visible: the pushed [PlaytestLife.cs](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/engine/com.decennium.foundation/Laboratory/Model/PlaytestLife.cs) stores `StableUntilSeconds` and accepts integer `nowSeconds`. A creature becoming Stable at a fractional initiative timestamp needs **that exact timestamp + rolled hours**, without rounding or restarting. This can be completed through your existing transaction/save path without choosing new gameplay rules.

For the subsequent attack fixture, explicitly supply two grid-aligned Medium actors on supported level ground, clear mutual sight/line of effect, an actual ordinary weapon, verified character statistics, a selected legal stance and an enumerated set of operative features. Those are **fixture facts**, not defaults for arbitrary actors.

Persist Action spending, actual RNG draws, damage/life results, stance/Press records and any resulting custody changes together. Conditional choice continuations and draw ordering are engineering contracts; their gameplay eligibility comes from the sources above. Reject unsupported admitted features before spending or rolling, rather than discovering after a hit that its required consequence cannot run.
