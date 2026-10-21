# Bestiary workbook and build provenance

Status: read-only history reconciliation. No ingester, combat generator or source builder was executed. All source workbooks, datasets and scripts remain unchanged. This evidence supplements the [source/runtime audit](BESTIARY_SOURCE_RUNTIME_AUDIT.md); it does not approve a replacement dataset or any new creature mechanics.

## Earlier work is preserved

The inventory identifies **42 workbook/JSON files grouped into 27 byte-distinct contents**, including backups. Five JSON copies contain the same 707 records; four retained V6/V7 copies contain the same 65 source-based dossiers. Two copies of an earlier truncated JSON remain byte-preserved and are recorded as unparseable. The inventory does not claim every backup has undergone a complete semantic review.

All **707 current runtime records map uniquely to actual rows in the ReviewBible `Bestiary.xlsx` Monsters sheet** using its existing naming rules. The workbook has 708 named rows; one is excluded by the existing hidden-name predicate and remains in the original workbook. That predicate was observed, not newly approved or changed.

All 7,070 selected scalar comparisons match: size, type, alignment, CR, XP, zone, AC, HP, speed and Save DC. All 707 primary attack names and combat source/draft labels also match their workbook inputs. This proves a bounded provenance chain, not that the workbook's rules agree with the later authoritative source pack. The prior audit's 184 source/runtime differences still stand.

The main and ReviewBible primary workbooks each have 19 sheets. Both were read without recalculation or saving. Their corresponding Monsters rows differ in 99 name cells and one Loot Table cell. All 100 differences are retained verbatim in the JSON evidence; no automatic rename, loot substitution or deletion was made.

## Why “trusted” is insufficient evidence

The existing ingester sets `draft` to false whenever the Combat Provenance string contains `trusted`. The existing generation scripts choose generic attacks from type-specific pools, including deterministic selection from a hash of the creature's name, and scale values from CR/size bands.

- **686 current rows** retain “usable draft” wording in their workbook Traits column.
- **436 current rows** retain a NeedsReview note; **425 of those** currently have `combat.draft: false`.
- None of the 707 workbook Traits columns is projected into a runtime `traits` field. NeedsReview notes are likewise absent from the runtime rows.
- Every runtime defense collection is empty. The current primary workbook has no resistance/immunity columns to supply those collections; the ingester defaults missing defense input to empty lists.

The workbook still preserves these notes and inputs. Their absence from the JSON is a projection limitation, not evidence that the concerns were resolved or the information no longer matters. Existing fixed Guardian records and generic combat drafts retain their distinct provenance; this audit does not assign new balance approval to either.

## A rebuild currently has two different outcomes

Main and ReviewBible use different naming maps and different metadata-supplement paths, although their current 707-record outputs are identical. The ReviewBible map resolves 20 names that the main map leaves in their older forms.

A **name-only simulation** of the actual workbook-ingest and existing-override retention algorithm predicts:

| Build inputs | Workbook names after existing exclusion | Retained newer-name overrides | Projected distinct names |
|---|---:|---:|---:|
| Current main | 707 | 20 | 727 |
| Current ReviewBible | 707 | 0 | 707 |

This is not a performed rebuild or verification of every generated field. It demonstrates why rerunning the main ingestion command is unsafe as a routine synchronization step: the older and newer names would coexist as separate records. The exact 20 pairs, source rows and naming maps are saved in the evidence. No build was run and neither set of records was removed.

## A source-based projection already exists

The retained V6 dataset has **65 Known Descent dossiers**, all matching names in the current merged source pack, and no exact sealed-dossier name matches. Its 64 stat-bearing records match the eight selected core fields checked against the current source, excluding Save DC. The remaining dossier is a historical record rather than a stat-bearing creature.

The data and its preserved builder explicitly record these aliases:

| Retained V6 name | Existing compatibility alias |
|---|---|
| Fracture-Kin Fleshwright | Fracture-Kin Sibriex |
| Fracture-Kin Nightreaver | Fracture-Kin Nabassu |

This supplies documentary evidence that was missing from the first audit; the relationships are not newly inferred from matching statistics. The merged source pack deliberately retains all four files. The pending reconciliation should use these existing aliases while preserving the original identities and resolving how one creature is selected and saved in the companion.

The 65-record projection is useful prior work but cannot simply replace the 707-record runtime file. It has no structured `combat` objects or Save DC fields, omits structured defenses, retains historical absolute `ingestSource` paths, and stores loot under `drop1`…`drop6` with percentage/currency strings. Current crafting consumers rely on other keys and value formats. Source tactics also retain the three undefined-action references found previously. These interfaces need an explicit migration and joint review.

## Next reconciliation

Use the retained source-based projection and its aliases as evidence when authoring the candidate adapter; preserve the 707 workbook-backed catalog and all review notes as historical/source material. Settle source-pack selection, public/licensed/Director routing and the three undefined actions with GPT. Then validate source fields, loot conversion, saved identities and encounter/crafting interfaces before replacing runtime imports. Do not equate a successful parser or `draft: false` flag with creature approval.

Ten bounded provenance controls pass. All **53 inventoried source files and build scripts** are unchanged. The canonical pack, prior reviewed crafting rules and pending Blacksmithing manuscript remain untouched. No cosmology interpretation, source deletion or GitHub push occurred.

Evidence: [BESTIARY_HISTORY_PROVENANCE.json](BESTIARY_HISTORY_PROVENANCE.json). Reproduce with `DescentReviewChanges/ReviewBible/tools/audit_bestiary_history.py`.
