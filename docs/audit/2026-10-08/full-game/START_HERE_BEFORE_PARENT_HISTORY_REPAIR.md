# Decennium Descent — start here

**Working folder: `C:\Github\DecenniumDescent`**  
Recovery and reconciliation: 8 October 2026. No original files were deleted.

**Current position — 9 October 2026**

| Area | Completed so far | Still open |
|---|---|---|
| Classes | All 17 have provisional Base, Arch and Hero progression; 1,223 playtest cards | Full interaction review and human balance testing |
| Ordinary spells | 83 reviewed drafts; all 848 IDs and 936 placements preserved | 765 unfinished spells |
| [Feats](DescentReviewChanges/ReviewBible/docs/mechanics/FEAT_PLAYTEST_INDEX.md) | 8 complete options jointly reviewed; all 335 originals preserved | 327 unfinished feats |
| [Whole-game audit](DescentReviewChanges/ReviewBible/docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md) | 75 areas tracked; 1 fully closed | The other areas retain their specific unfinished criteria |

The latest jointly reviewed checkpoint is the [Time Loop control/healing-pulse interface](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md). Its 50 integration checks, 76 foundation checks and 22 payment/output checks pass: 148 total. The twelve earlier conservation decisions and the bounded foundation review remain recorded separately. The [current review manifest](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json) identifies the exact approved files, including the foundation extension.

Full control/pulse restoration, seven larger Time Loop integrations and the whole-game candidate remain unfinished. [Form/concentration parent policies](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md) are now settled using all 26 Druid profiles as source evidence; their runtime integration remains next. The [final joint flow review and authorized GitHub delivery](docs/audit/2026-10-08/full-game/FINAL_FLOW_AND_GITHUB_DELIVERY.md) remain later gates.

You had reached an **approved V6 release on 5 August**, followed by **V7.2 calibration work on 6 August**. V7.2 is the latest testing branch, but it was never promoted into the approved books. Several old summaries and the extracted rulebook text were misleading about that distinction.

## Read these first

| What you need | Open this |
|---|---|
| Player rules and the 17 classes | [Player Rulebook V6](books/player/Decennium_Descent_Player_Rulebook_v6.docx) |
| Combat, Resonance, economy and Gate scaling | [Core Systems — Known Descent V2](books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx) |
| Player crafting | [Crafting — Known Descent V5](books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx) |
| Feats | [Feat Compendium](books/player/Decennium_Descent_Feat_Compendium_v1.docx); the [registry](src/data/feats.js) owns the current entries |
| Public creatures | [Monster Manual of the Known Descent V2](books/player/Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx) |
| Running the world — Director only | [The Director's Crucible](docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx), with the source-linked [recovered lore addendum](docs/director-only/RECOVERED_THEME_ADDENDUM.md). Both original editions are preserved. |
| Which source wins a disagreement | [Canon manifest](docs/canon/CANON_MANIFEST.json) — authority is assigned by domain, not filename date |
| What was recovered and what remains | [Recovery audit](docs/audit/2026-10-08/AUDIT_REPORT.md) and [completion checklist](docs/audit/2026-10-08/READINESS.md) |
| Start a Base-class character | [Base class starting guide](DescentReviewChanges/ReviewBible/docs/mechanics/BASE_CLASSES_START_HERE.md) — all 17 identities, with Arch and Hero kept as later progression. |
| Complete class playtest drafts | [All-class library](DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md): 1,223 cards, costs, timing, source wording, level 1–20 progression and legal builds. Provisional mechanics; human balance testing remains. |
| Next development priorities and ordinary spells | [Development roadmap](DescentReviewChanges/ReviewBible/docs/mechanics/DEVELOPMENT_ROADMAP.md), [first spell packet](DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_PLAYTEST_STARTER.md), and [spell integration rules](DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md). Full source register; staged provisional drafts, not approved-book changes. |
| Current completion work | [Review candidate](DescentReviewChanges/ReviewBible/RECOVERY_REVIEW_2026-10-08.md) and [all-class advancement matrix](docs/audit/2026-10-08/ADVANCEMENT_MATRIX.md) |
| Whole-game development with GPT | [75-area coverage ledger](DescentReviewChanges/ReviewBible/docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md) and [current review status](docs/audit/2026-10-08/full-game/REVIEW_STATUS.md). These distinguish discussion, drafted rules, checked interfaces and unfinished work. |
| Combat procedure candidate | [Actions, timing, movement and vision](DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md), with the source-conflict table and bounded reference checks. Detailed cargo, travel and class interactions remain tracked in the ledger. |
| Strain and recovery tracks | [Source-qualified Strain reference](DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md): Warrior serum Strain, expedition Strain, rest eligibility and their separation from Exhaustion. |
| Slows, roots, marks and control | [Control-state candidate](DescentReviewChanges/ReviewBible/docs/mechanics/CONTROL_STATES_PLAYTEST.md) and [219 source bindings](DescentReviewChanges/ReviewBible/docs/mechanics/CONTROL_SOURCE_BINDINGS.md). Supplied control scope reviewed and reference-validated (150 checks including the healing clarification); wider condition and class semantics remain open. |
| Healing, survival and resurrection | [Working guide](DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md) and [source reference](DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md). 153-source interface reviewed;164 selected checks. Six spells promoted. All131 further class passages discussed; [three selected extensions](DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_SOURCE_EXTENSIONS.md) now reviewed with21 checks. Broader integration remains open. |
| Damage sharing and interception | [Reviewed guide](DescentReviewChanges/ReviewBible/docs/mechanics/DAMAGE_SHARING_PLAYTEST.md) and [39 exact source bindings](DescentReviewChanges/ReviewBible/docs/mechanics/REDIRECTION_SOURCE_BINDINGS.md), plus two supporting Tinker engines. Bounded interface jointly closed with94 checks and186 conservation states; broader combat and companion work remains open. |
| Current shared rules candidate | [Core resolution and Wounds](DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md), [all 28 Core conditions](DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md), [recovery](DescentReviewChanges/ReviewBible/docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md), and [source-qualified custom riders](DescentReviewChanges/ReviewBible/docs/mechanics/CUSTOM_CONDITION_BINDINGS.md). Provisional overlays preserve the approved source books. |
| Companions, summons and structures | [Devices and Totems](DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md), [Beasts and creature companions](DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md), and [Cleric/Oracle summons, Paladin spirits and Soldier structures](DescentReviewChanges/ReviewBible/docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md). Selected lifecycle and command rules are jointly reviewed; full-card effects remain separately tracked. |
| Forms and temporary HP | [Reviewed interface](DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_PLAYTEST.md), [Druid quick reference](DescentReviewChanges/ReviewBible/docs/mechanics/DRUID_FORM_QUICK_REFERENCE.md), [source register](DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_SOURCE_BINDINGS.md) and [validation](DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json). Selected form/shield rules are jointly closed; full cards, equipment/weapon taxonomy and named unfinished feat/spell components retain their separate review requirements. |
| Time Loop development | [Current bounded candidate and remaining integrations](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md), with the [actual review/repair trail](docs/audit/2026-10-08/full-game/TEMPORAL_KERNEL_REPAIR_LOG.md). The full feature remains unpromoted while the larger integrations are unfinished. |

The public bestiary source is under [Monster Manual of the Known Descent](docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/). The adjacent Director's Sealed Bestiary is private campaign material. Do not distribute the entire repository as a player packet.

## Where your work now lives

| Folder | Meaning |
|---|---|
| `books/player`, `books/director`, `docs`, `data`, `src` | The recovered main working tree. The manifest identifies approved sources within it. |
| `DescentReviewChanges/ReviewBible` | Existing assembled review build. Contains some curated lore absent from main. It is not a second app to launch. |
| [V7.2 calibration lab](DescentReviewChanges/incoming/DecenniumDescentV7_2_AI_Calibration_Lab/DecenniumDescentV7_2_AI_Calibration_Lab/) | Latest completed automated calibration, including gameplay loop V1.2. Preserved as evidence; not automatically approved. |
| `DescentReviewChanges/incoming` | Earlier delivery packs and pending review material. V7.1 and V7 remain history behind V7.2. |
| `DecenniumDescentv6` | Retained V6 delivery snapshot. Do not edit it as a new working copy. |
| `_preserved/2026-10-08/outer-root` | The older July working folder that formerly occupied this root. Preserved intact. |
| `_preserved/2026-10-08/pre-edit` | Originals of files repaired during this recovery. |
| `archive`, `backups` | Earlier preserved states; not the current release. |
| `Descent assets` | Separate imported game-asset experiment and tools. Most of the disk usage is here, not in the TTRPG books. |

The former active path `Descent assets\DecenniumDescent-main` has moved to this root. The Codex conversation folder under Documents is a separate workspace, not the game source.

## Where you left off

The game has extensive written material, 17 protected class identities, 848 spell records, 335 feat records and 433 public crafting recipes. V7.2 reports all 20 calibration packs complete. Those runs are useful evidence, not proof that all classes are ready for a human campaign.

The class playtest drafts and reviewed gameplay procedures now provide a concrete candidate for review. Remaining game-wide work includes ordinary-spell and live companion integration, character-sheet consistency, closing the public/Director data mismatch, and an actual table playtest. New design decisions must be labelled as such; recovered historical decisions are recorded separately.

The current working finish line is a consistent campaign-playtest candidate. Publication readiness and balance approval remain separate milestones.

The selected [maximum-HP and threshold interface](DescentReviewChanges/ReviewBible/docs/mechanics/MAXIMUM_HP_PLAYTEST.md) is now jointly reviewed:58 source records,60 checks and909 systemic states. This is one bounded part of the continuing full-game review.

The selected [recurring healing and zone schedules](DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_PULSE_PLAYTEST.md) are jointly reviewed:100 source roles plus6 supporting passages,89 checks and301 reserve partitions. All33 internal profiles link to supplied abilities; none adds a new spell or class card. Companion/device lifecycle and wider game development continue.

The selected [device, Totem and shared-command rules](DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md) are jointly reviewed:74 source roles plus3 shared passages,132 checks and1,200 state cases. Repair, reconstruction, disablement, slots and destruction provenance now have explicit contracts. Broader creature companions and the remaining game audit continue.

The selected [creature companion rules](DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md) are jointly reviewed:100 source roles+5 shared paragraphs,121 checks and2,800 Ranger conversion cases. Temporary summons, persistent beasts, raised undead, commands and body identity have explicit boundaries. Full forms/tempHP, remaining companions and the rest of the game audit continue.

The [remaining companion and structure rules](DescentReviewChanges/ReviewBible/docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md) are jointly reviewed with129 checks: Cleric/Oracle summons, controlled undead, Paladin spirits, Soldier cover and turrets now have explicit creation, command and ending procedures. The175-source form/temporary-HP interface is also reviewed within its bounded scope; the whole-game audit is still in progress.

### Eight-feat reviewed playtest overlay

Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and the Soul Cage feat are reviewed in full with131 targeted checks and2,520 funding cases. All335 original records are preserved:8 reviewed/327 unfinished. [Current feat index](DescentReviewChanges/ReviewBible/docs/mechanics/FEAT_PLAYTEST_INDEX.md). The subsequent Time Loop conference settled twelve conservation boundaries; its bounded foundation has completed joint review, while seven larger integrations remain unfinished. This is not whole-game completion.
