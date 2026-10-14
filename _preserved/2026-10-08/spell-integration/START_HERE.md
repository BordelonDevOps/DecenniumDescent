# Decennium Descent — start here

**Working folder: `C:\Github\DecenniumDescent`**  
Recovery and reconciliation: 8 October 2026. No original files were deleted.

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
| Current completion work | [Review candidate](DescentReviewChanges/ReviewBible/RECOVERY_REVIEW_2026-10-08.md) and [all-class advancement matrix](docs/audit/2026-10-08/ADVANCEMENT_MATRIX.md) |

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
