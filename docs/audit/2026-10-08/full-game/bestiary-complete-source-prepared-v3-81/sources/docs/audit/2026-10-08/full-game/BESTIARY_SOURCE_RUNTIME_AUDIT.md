# Bestiary source and companion audit

Status: source audit and proposed reconciliation only. No source, creature, publication filter or runtime file has been changed. GPT review remains pending. Cosmology is deferred until after verified GitHub delivery.

Subsequent [workbook/build provenance evidence](BESTIARY_HISTORY_PROVENANCE.md) binds all 707 runtime records to preserved workbook rows and locates a retained 65-dossier source projection. That dataset and its builder explicitly record the Fleshwright/Sibriex and Nightreaver/Nabassu aliases, supplying evidence for the identity question below. Its missing combat/defense fields and different loot schema still require integration. The first prepared conference packet remains preserved unchanged; the supplement adds this later evidence.

## What the folders actually contain

The canonical merged source pack contains **85 files, not 85 creatures**. Main and ReviewBible copies are byte-identical. Its Known Descent directory has **67 dossiers: 66 stat blocks and one historical disaster record**. The sealed Director directory contains five additional dossiers; only their names and publication routes were inventoried here.

The actual V2 player book binds to 65 Known Descent dossiers, including 64 stat blocks and the historical record. All **64 sets of core statistics and 157 listed action paragraphs** agree with their corresponding source Markdown. This comparison does not claim every lore, harvest, trait or other paragraph has been semantically reviewed.

The two additional Markdown dossiers, Fracture-Kin Fleshwright and Fracture-Kin Nightreaver, are preserved alongside the classic-label records. They are absent from the V2 book and build-filter index. Both source headers say “Licensed expedition reference.” Their relationship to the older records requires an explicit identity decision; matching statistics alone does not authorize merging or deletion.

The build-filter index contains 70 routes: 26 public, 39 restricted and five Director-only. Its counts correctly describe its own rows but omit those two retained dossiers. “Known Descent” is a volume name and includes restricted records; it is not equivalent to the public build bucket.

## Companion differences

Main and ReviewBible both retain the same 707-record `bestiary_data_full.json`. It has 62 exact-name matches to Known Descent dossiers, five exact-name matches to sealed dossiers, and 640 names without an exact match to this pack. The unmatched names are preserved; this check neither establishes aliases nor declares them obsolete.

Of the 62 Known Descent matches, **59 records have at least one difference among the selected fields**, totaling 184 differences:

| Field | Differences |
|---|---:|
| Size | 34 |
| Creature type label | 6 |
| Alignment label | 40 |
| Save DC, including missing fields | 17 |
| Damage resistances | 44 |
| Damage immunities | 7 |
| Condition immunities | 36 |

CR, XP, AC, HP and speed match in all 62 exact-name comparisons. Seventeen records have different ordered attack/action names, excluding the source Multiattack entry. This action-name comparison does not verify damage, cadence, targeting, triggers or other action semantics.

For example, the source Cave Bear is Large and uses Mauling Claws; the companion says Medium and Goring Horn. Source Sporefolk Adult is Medium with poison resistance and Poisoned immunity; the companion is Large and omits both defenses. Matching AC and HP would miss those differences. Existing Cooking decisions that explicitly use the approved source remain unchanged.

Four Known Descent stat blocks have no exact-name runtime match: Crystal Shardling, Pact Automaton Sentinel and the two additional Fracture-Kin dossiers. The historical disaster record also lacks an exact-name match and should not be manufactured into a playable creature merely to equalize counts.

The stored combat labels include 696 records with `draft: false` and 11 with `draft: true`. Labels such as `band-trusted` do not prove agreement with the domain's authoritative source.

## Where the companion uses this data

Four ReviewBible components directly import the 707-record dataset:

| Consumer | Observed source-code use |
|---|---|
| `MonstersLibrary.tsx` | Maps all records into the library, filters by search/type/CR/size/zone, and hands selected names/HP/CR/zone to the session. Its selection path does not apply the pack's publication filter. |
| `SessionTracker.tsx` | Searches names in the imported array and accepts creature handoffs. |
| `CraftingBuilder.tsx` | Derives a component list from monster loot, iterating the legacy tier1/tier2/tier3 keys. |
| `ItemsLibrary.tsx` | Builds dropped-item entries and source-monster lists from the same data. |

All five sealed Director names are present in that client-imported array. This is a static import and selection-path finding, not a browser test or a claim about deployment. The audit saves exact import/usage lines and file hashes. It does not infer a public source's missing mechanics from sealed material.

## Problems inside the source itself

Three tactics paragraphs name actions absent from their corresponding action lists. The actual book tactics paragraphs and source action lists are retained in the JSON evidence:

| Creature | Unlisted action referenced by tactics |
|---|---|
| Cave Bear | Bite |
| Dimetrodon | Tail Sweep |
| Giant Constrictor Snake | Constrict |

These references need a joint decision: either author a justified action or correct the tactics text in a clearly marked candidate overlay. No attack should be invented from its name, and no source paragraph should silently disappear.

## Required reconciliation decisions

1. Preserve the 707-record dataset and all source dossiers before producing any replacement projection. Resolve the provenance of the 640 unmatched names without assuming they are duplicates or disposable.
2. Confirm how the two additional Fracture-Kin dossiers relate to the retained classic-label records. Repair the filter index only with an explicit recorded classification and identity policy; retain all originals.
3. Derive candidate stat records from the authoritative source and maintain distinct public, restricted and Director routes. Confirm how licensed access works in the companion before changing its selection paths.
4. Resolve the three undefined action references and audit the remaining action/trait procedures before claiming complete playable stat blocks. Matching selected fields is not whole-creature approval.
5. Integrate approved profiles with encounters, saved session references and crafting donor/harvest rules. Keep source statistics separate from newly proposed rules and preserve existing character/session data.

Ten bounded source controls pass. They establish inventory, copy equality, book bindings, selected source parity, unique runtime names, consumers and preservation—not game balance or runtime readiness. DD-33, DD-36 and DD-63 remain open; no GitHub push or cosmology review has occurred.

Full evidence: [BESTIARY_SOURCE_RUNTIME_AUDIT.json](BESTIARY_SOURCE_RUNTIME_AUDIT.json). Reproduce with `DescentReviewChanges/ReviewBible/tools/audit_bestiary_source_runtime.py`.
