# GPT rank-two Evocation exact review and delivery priorities

Source: Calibration Review, response to turn 174b2eda-9e1c-4f1a-b342-b082f21e4586. Complete connector Markdown. This contains the eight-card manuscript disposition and a separate prioritization discussion, not final game-flow or push approval.

Both Evocation parts are available and reconstruct cleanly under the shared defaults/fragments.

## Rank-2 Evocation exact review

**APPROVE — all eight cards and the shared wording. No exact manuscript repairs required.**

**Scorching Raystorm — APPROVE.** Fixed three-ray allocation, numbered resolution order, separate attacks/damage/crit events, lost allocation when its recipient becomes illegal, and legal-object handling all match the conference. Nothing accidentally converts the three rays into one packet.

**Lightning Pulse — APPROVE.** The 20×5-ft creature-only line, CON full/half, shared 3d6 roll and per-recipient defenses correctly implement the source. No invented conductive chaining, objects, Stunned or Reaction denial.

**Frost Nova — APPROVE.** The candidate correctly incorporates the later clarification: same owner/target/group/exact-profile Speed 0 refreshes one record; different owners stay independent. The first-future-target-END/+6s endpoint is the base deadline rather than an extension ceiling. `slowed-foe` eligibility and Balanced Elements' `max(existingDeadline, targetFollowingRegularEndMeasuredNow)` extension are properly bounded. It remains magical elemental Speed 0, **not** Frozen, Root, Restrained or hard denial.

**Arcane Implosion — APPROVE.** Automatic 4d6 force followed by the conditional CON save for Stunned matches the conference. Damage remains independent of the control gate. Skipping the Stun procedure when the combined hard-denial allowance is already unavailable is the previously reviewed behavior; successful save/prevention does not spend a new allowance, and damage never gains a soft fallback.

**Scorching Line — APPROVE.** Historical Aganazzar's Scorcher evidence is being used only to fill matching source metadata. It does not merge identities, grant access or import external mechanics. The 30×5-ft DEX full/half procedure is clean.

**Shatter — APPROVE.** The object scope matches the prior conference: ordinary nonmagical eligible objects, no hostile worn/carried inventory, shared 3d8+1d8 grouped object packet, and creatures receive only the 3d8 base. The fixed pre-damage creature/object/structure snapshot is important and correctly prevents destroyed cover from exposing a second wave of recipients. The one bounded contiguous structural section per actual structural whole, nearest-center selection and neutral tie rule prevent both caster optimization and “I target every brick” multiplication.

**Snowball Swarm — APPROVE.** Historical Snilloc evidence remains source evidence only. The separate 5-ft casting range and 5-ft sphere, DEX full/half and absence of Frozen/slow/terrain riders are correct.

**Acid Arrow — APPROVE.** Historical Melf evidence remains separately preserved. Hit → initial 4d4 → attach one delayed 2d4 rider only to the same continuing recipient is correct. Initial critical doubles only the initial attack dice. Independent riders coexist. The delayed event is an existing-effect consequence, not another cast; no RP/Refrain/Dissonance/Counterspell cycle occurs. Suppression at its due marker consumes the one-shot without replay, and identity-ending/destruction prevents inheritance by a corpse, reconstruction or replacement.

The common `area`, `objects`, `hostile_end` and `common` fragments are also approved for these cards.

**Disposition:** the eight rank-2 Evocation identities may proceed to promotion as reviewed authored PLAYTEST manuscript, subject to the explicitly separate runtime, numerical-balance, human-playtest and whole-game gates. The three historical names remain preserved evidence, not merged identities.

---

# Delivery prioritization

The proposed faster workflow is sound. I would change **one thing**: step 4 is still broad enough to become another endless “review everything” pass unless the whole-game work is dependency-ordered. The next work should follow the playable game loop rather than ledger row number.

| Priority | Authored-delivery blocker | Read next |
|---|---|---|
| **0** | **Correct audit state/entrypoint.** DD-13's `83/765` spell count is stale; current verified state is `261/587`. This is bookkeeping, not a mechanics reopening. Confirm the active candidate entrypoint and manifest before more consolidation. | `docs/canon/CANON_MANIFEST.json`; `START_HERE.md`; `SPELL_PLAYTEST_STARTER.md`; `SPELL_VARIANT_REVIEW_STATUS.json` |
| **1** | **Character creation → advancement must become one executable player flow.** Blank sheet→legal level 1 and level 1→20 are prerequisites for meaningful whole-game testing. Multiclassing must either be explicitly unsupported or actually operational. | `CHARGEN_PROGRESSION.md`; `CLASS_PLAYTEST_RULES.md`; `CLASS_PLAYTEST_INDEX.md`; `data/playtest/class_sources` |
| **2** | **Equipment/inventory/feat acquisition.** A legal character needs weapons, armor, carrying, item use and feat selection before encounter/exploration flow can genuinely close. The 327 unfinished feats remain real authored work. | `BODY_EQUIPMENT_PLAYTEST.md`; `TEMPORAL_CARRYING_SOURCE_EVIDENCE.json`; `BUFFER_FEAT_COMPLETION_SOURCES.json`; `BUFFER_FEAT_DEPENDENCY_SOURCES.json`; existing feat-source/draft records |
| **3** | **Expedition → encounter → reward → extraction → Haven loop.** This is the biggest whole-game authored-flow blocker visible in the ledger. Read the existing procedure before creating anything new. | `GAMEPLAY_LOOP_CANON.md` first, then the exact source files it cites for encounter construction/procedure, loot, travel, rest, extraction, Haven and downtime. The ledger's `OPEN` state is not evidence those procedures are absent. |
| **4** | **Director execution interfaces.** Creature/boss/stat interfaces and encounter construction have to support the loop without Director invention. Summon/companion lifecycle work already exists and should be linked rather than rewritten. | `CREATURE_LIFECYCLE_PLAYTEST.md`; `CREATURE_LIFECYCLE_SOURCE_BINDINGS.md`; `REMAINING_LIFECYCLE_PLAYTEST.md`; then actual creature/boss source datasets located by the gameplay-loop docs |
| **5** | **Spells and feats continue in large parallel batches.** Do not pause the rest of the game until 848/848 spells are finished, but do not waive the remaining 587 either. Shared patterns should be reviewed once and reused. Variants must remain separately adjudicated. | `data/playtest/spell_sources`; current placement/access audit; `SPELL_VARIANT_REVIEW_STATUS.json`; unassigned-variant evidence; feat source objects |
| **6** | **Hazards/environment/crafting/economy source inventory.** Several ledger rows have no actual source-evidence path attached. Before drafting gaps, locate the authoritative source material and decide whether content exists, conflicts, or is genuinely missing. | Search the source corpus for the actual weapon/armor/item/recipe/economy/hazard records; do **not** infer absence from the ledger's empty refs. Crafting's 687/433 recipe counts especially warrant source inventory before rewriting. |
| **7** | **Onboarding/reference/public-Director packaging.** Once the playable loop is coherent, build the first-character/first-turn/first-expedition examples, indexes and public/Director separation around the actual rules rather than polishing moving targets. | `START_HERE.md`, active player/Director source books, build/export manifests/scripts, then DD-60 through DD-67 acceptance material |
| **8** | **Final authored-flow agreement → Git delivery.** Only after the other authored requirements are actually settled should we perform the owner-requested joint flow review and delivery decision. | `FINAL_FLOW_AND_GITHUB_DELIVERY.md`, current manifest/build outputs and repository state |

### Requirements already justified by owner/source evidence

The full objective remains unchanged: all 17 class families/stages/oaths, 848 spell identities/936 placements, 335 feats, game systems and source conflicts remain in scope. Unfinished content cannot be declared done merely to reduce elapsed time. Source preservation is mandatory; consolidation does not require deletion. Actual joint flow agreement is still required before pushing to `BordelonDevOps/DecenniumDescent`. **Cosmology remains completely deferred until after a successful push and verified remote commit.**

Runtime, human balance and publication are separate gates. In particular, the disabled full Time Loop runtime should **stay disabled** until its genuine integrations exist; that does not prevent us from completing and reviewing its tabletop procedure separately.

### Additional workflow recommendation

Freeze/version the shared procedure fragments used by bulk spell/feat batches and rerun regressions only when those shared rules change. That lets routine records move in large exact batches without repeatedly reopening already-settled action economy, timing, targeting, damage, concentration or control semantics.

The main correction to the last 20 hours is therefore **not a smaller game**. It is: finish routine catalog work in larger batches while moving the whole playable player/Director flow forward in parallel, reserving conferences for actual source conflicts rather than every ordinary card.

