# Bestiary harvest and crafting crosslinks

Prepared source comparison; not sent to GPT and not a rule approval. All original files and existing review statuses remain unchanged. Cosmology remains deferred until after verified GitHub delivery.

## What connects

The 66 harvest profiles contain 178 component occurrences. Only 34 have a literal current material-name correspondence; 144 occurrences (57 distinct labels) do not. Of the unmatched entries, 117 include a printed tier suffix; removing that suffix produces no additional material-name matches. This audit compares only whitespace and case for identities.

Three unmatched Animated Core (Tier 1) occurrences have legacy component-name evidence, but that legacy label points to eleven different current materials. The JSON preserves every contributing recipe/component. It is not a unique alias.

The one literal-match tier difference is Pact Devil (Green Court): infernal marrow is printed tier 2, while the global material is tier 3. All 31 literal matches with printed numeric rates and values differ from global rates and values. These are context differences requiring a rule decision, not automatic errors. No source is overwritten and no extra roll or price precedence is inferred.

Only two of 40 printed recipe links resolve under current or retained legacy recipe names:

| Creature | Printed recipe | Catalog ID | Current operational review | Shared printed ingredient |
|---|---|---|---|---|
| Season-Bound Autumn | Refined Storm Roast | recipe-92 | reviewed-authored-playtest | sparkling petal |
| Sporefolk Adult | Refined Verdant Tackle | recipe-173 | source-only-unreviewed | living root |

The other 38 occurrences (30 distinct labels) remain unresolved in this catalog. This does not prove that earlier notebook work or another source never contained those names. Both resolved recipes retain their actual ingredients, formula-access rules and review status; a printed link does not grant a recipe.

## Procedure interfaces

Of 64 printed harvest procedures, 36 times differ from the generic body-size table and 56 DCs differ from the generic highest-printed-tier lookup. These comparisons do not establish which procedure controls. Crystal Shardling and Pact Automaton Sentinel lack printed skill/DC/time; those fields remain null. The historical dossier has no invented harvest or stat block.

Printed skill labels are Arcana, Religion, Medicine, Nature and Engineering. The reviewed framework distinguishes identification from gathering-trade extraction. Its finite shared anatomy/yield manifest, selected-category timing, preservation and exceptional-drop rules must be reconciled with the creature-specific fields before an executable adapter can be accepted.

Of the 34 literal material matches, 31 explicitly list the donor name in the retained global sourceMonsters list. The other three lists are truncated with “and N more”; absence from that shortened list does not disqualify the donor.

## Decisions to confer on

1. For each unresolved harvest label, decide whether it is an unresolved category, a distinct new material, or an explicitly evidenced alias. Do not collapse Animated Core to one of eleven current ingredient names without provenance. Keep all originals and record any approved identity relation separately.
2. Resolve the Pact Devil (Green Court) infernal marrow tier 2 versus global tier 3. Creature-specific values/rates differ from the global reference in all 31 numeric literal matches; agree the applicable context without overwriting source or adding a second independent drop roll.
3. Determine what each printed body-level Harvest skill, Harvest DC and Base time actually governs. The generic framework separates identification and trade extraction, has finite shared yields, and allows explicit component DCs. Confirm whether these body-level fields override it, and at which step. Preserve the two absent procedures until decided.
4. Resolve 38 printed recipe references not found under any current or retained legacy recipe name in this 687-record catalog. Ask the owner/notebook history before declaring the labels nonexistent or superseded. The two resolved names still require all their ordinary components and access rules.
5. Specify a finite per-creature harvest manifest with exact units, quantities, anatomy, weight, preservation, roll dependence and exceptional-drop status. Do not assume global quantity dice multiply every row or that generic and exceptional yields add. Keep restricted materials/formulas behind their existing access routes.
6. Confirm harvest/crafting interpretation only. No source deletion, recipe promotion, runtime installation, publication reclassification or cosmology decision is authorized by this comparison. Cosmology remains deferred until the final joint flow review, successful GitHub push and remote verification.

## Preservation and evidence

All 10 bounded controls pass; 278 protected source, candidate, review and runtime files retain their hashes. No recipes were promoted, no source values were changed and no runtime data was installed.

- [BESTIARY_CRAFTING_CROSSLINK_AUDIT.json](BESTIARY_CRAFTING_CROSSLINK_AUDIT.json) contains every printed harvest row and recipe reference, matched full material/recipe records, legacy component evidence, procedure comparisons and source hashes.
- [Prepared GPT conference](CODEX_BESTIARY_CRAFTING_CROSSLINK_CONFERENCE_PREPARED.txt) contains the actual bounded evidence and questions. It has not been sent.
- [BESTIARY_CRAFTING_CROSSLINK_STATUS.json](BESTIARY_CRAFTING_CROSSLINK_STATUS.json) records output hashes and passing checks.
