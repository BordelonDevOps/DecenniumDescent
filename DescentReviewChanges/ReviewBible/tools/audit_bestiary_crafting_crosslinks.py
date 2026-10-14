"""Read-only source comparison for harvest identities and printed recipe links.

Writes audit artifacts only. It never resolves aliases, rewrites prices, applies
harvest procedures, promotes recipes, or installs a runtime bestiary.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
PREFIX = 'BESTIARY_CRAFTING_CROSSLINK'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def norm(value):
    return ' '.join(value.split()).casefold()


def relative(path):
    return path.relative_to(GAME).as_posix()


def main():
    status_path = AUDIT / (PREFIX + '_STATUS.json')
    if status_path.exists():
        previous = read(status_path)
        assert previous['reviewStatus'] == 'PREPARED_NOT_SENT'
        assert all(sha(GAME / p) == h for p, h in previous['artifactHashes'].items()), 'Preserve altered or reviewed artifacts before rebuilding.'

    candidate_path = ROOT / 'data/director/bestiary_source_candidate_internal.json'
    crafting_path = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    index_path = ROOT / 'data/director/crafting_recipe_review_catalog.json'
    framework_path = ROOT / 'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md'
    candidate_manifest_path = AUDIT / 'BESTIARY_SOURCE_CANDIDATE_VALIDATION.json'
    crafting_baseline_path = AUDIT / 'LEATHERWORKING_REVIEW_BASELINE.json'
    candidate_manifest, crafting_baseline = read(candidate_manifest_path), read(crafting_baseline_path)
    baseline = {}
    for group in (candidate_manifest['sourceHashes'], candidate_manifest['artifactHashes'],
                  crafting_baseline['files'], crafting_baseline['pendingBlacksmithDependencyFiles']):
        for path, digest in group.items():
            assert path not in baseline or baseline[path] == digest, path
            baseline[path] = digest
    for path in (candidate_path, crafting_path, index_path, framework_path,
                 candidate_manifest_path, crafting_baseline_path):
        rel = relative(path)
        assert rel not in baseline or baseline[rel] == sha(path), rel
        baseline[rel] = sha(path)
    assert all(sha(GAME / p) == h for p, h in baseline.items()), 'Source changed: reconcile before auditing.'

    candidate, crafting, review_index = read(candidate_path), read(crafting_path), read(index_path)
    records, recipes = candidate['records'], crafting['recipes']
    materials = {norm(x['name']): x for x in crafting['materials']}
    assert len(materials) == len(crafting['materials']) == 696
    review_by_id = {x['recipeId']: x for x in review_index['recipes']}
    recipe_names, component_aliases = defaultdict(list), defaultdict(list)
    for recipe in recipes:
        for field in ('name', 'legacyName'):
            if recipe.get(field):
                recipe_names[norm(recipe[field])].append({'recipeId': recipe['id'], 'field': field, 'literalName': recipe[field]})
        for pos, component in enumerate(recipe['components']):
            if component.get('legacyName'):
                component_aliases[norm(component['legacyName'])].append({
                    'recipeId': recipe['id'], 'componentIndex': pos, 'sourceComponent': component})

    harvest_rows, links, procedures = [], [], []
    linked_recipe_ids = set()
    generic_minutes = {'Tiny': 10, 'Small': 20, 'Medium': 30, 'Large': 60, 'Huge': 120, 'Gargantuan': 240}
    generic_dc = {1: 12, 2: 13, 3: 15, 4: 16, 5: 18, 6: 19}
    for creature in records:
        harvest, stat = creature['harvest'], creature['statBlock']
        if harvest is None:
            assert stat is None, creature['name']
            continue
        common = {'creatureId': creature['id'], 'creatureName': creature['name'],
                  'sourcePath': creature['source']['path'], 'sourceSha256': creature['source']['sha256']}
        for component in harvest['components']:
            key = norm(component['name'])
            material = materials.get(key)
            diagnostic_base = re.sub(r' \(Tier \d+\)$', '', component['name'])
            alias_evidence = []
            for alias in dict.fromkeys((key, norm(diagnostic_base))):
                if alias in component_aliases:
                    alias_evidence.append({'lookupLabel': alias,
                                          'method': 'literal-label' if alias == key else 'tier-suffix-removed-diagnostic-only',
                                          'currentNames': sorted({x['sourceComponent']['name'] for x in component_aliases[alias]}),
                                          'occurrences': component_aliases[alias]})
            row = {**common, 'sourceComponent': component,
                   'identityComparison': 'literal-name-correspondence-only' if material else 'no-literal-material-name-match',
                   'globalMaterialRecord': material,
                   'suffixRemovedDiagnostic': {'label': diagnostic_base,
                       'matchingMaterialName': (materials.get(norm(diagnostic_base)) or {}).get('name'),
                       'identityResolved': False},
                   'recipeComponentLegacyNameEvidence': alias_evidence}
            if material:
                numeric = component['printedRatePercent'] is not None
                row['contextComparison'] = {
                    'printedTierDiffers': component['printedTier'] != material['tier'],
                    'printedRateDiffersFromGlobal': abs(component['printedRatePercent'] / 100 - material['dropRate']) > 1e-10 if numeric else None,
                    'printedBaseValueDiffersFromGlobal': component['printedValueGp'] != material['value'] if numeric else None,
                    'donorExplicitInRetainedList': norm(creature['name']) in {norm(x) for x in material.get('sourceMonsters', [])},
                    'retainedDonorListContainsTruncation': any(re.search(r'\(and \d+ more\)', x) for x in material.get('sourceMonsters', [])),
                    'interpretation': 'Different source contexts; no rate, value, tier, donor or quantity precedence inferred.'}
            harvest_rows.append(row)

        printed_links = re.findall(r'^\*\*Known recipe links:\*\* (.+)$', harvest['sourceText'], re.M)
        assert len(printed_links) <= 1
        if printed_links:
            labels = [label.strip() for label in printed_links[0].rstrip().removesuffix('.').split(',')]
            assert ', '.join(labels) + '.' == printed_links[0].rstrip(), creature['name']
            for label in labels:
                matches = recipe_names.get(norm(label), [])
                ids = sorted({x['recipeId'] for x in matches})
                linked_recipe_ids.update(ids)
                links.append({**common, 'printedLine': printed_links[0], 'printedLabel': label,
                              'nameMatches': matches, 'recipeIds': ids,
                              'reviewIndexRecords': [review_by_id[i] for i in ids],
                              'status': 'unique-literal-catalog-match' if len(ids) == 1 else 'ambiguous' if ids else 'unresolved-in-current-and-retained-legacy-recipe-names'})

        highest_tier = max((x['printedTier'] for x in harvest['components']), default=None)
        time = harvest['printedBaseTime']
        parsed_time = None
        if time:
            match = re.fullmatch(r'(\d+) (minutes?|hours?)', time)
            assert match, time
            parsed_time = int(match[1]) * (60 if match[2].startswith('hour') else 1)
        size = stat['printedCoreFields']['size']
        procedures.append({**common, 'size': size, 'sourceHarvestText': harvest['sourceText'],
                           'sourceSkillLabel': harvest['skillLabel'], 'sourceDC': harvest['printedDC'],
                           'sourceBaseTime': time, 'sourceBaseMinutes': parsed_time,
                           'genericBodySizeMinutes': generic_minutes[size],
                           'printedTimeDiffersFromGenericBodySize': parsed_time != generic_minutes[size] if parsed_time is not None else None,
                           'highestPrintedMaterialTier': highest_tier,
                           'genericHighestTierDC': generic_dc.get(highest_tier),
                           'printedDCDiffersFromGenericHighestTier': harvest['printedDC'] != generic_dc[highest_tier] if harvest['printedDC'] is not None and highest_tier in generic_dc else None,
                           'interpretation': 'Comparison only. The source body-level skill/DC/time has not been assigned to identification, extraction or a specific override. Missing fields stay null.'})

    matches = [x for x in harvest_rows if x['globalMaterialRecord']]
    unmatched = [x for x in harvest_rows if not x['globalMaterialRecord']]
    resolved_links = [x for x in links if len(x['recipeIds']) == 1]
    unresolved_links = [x for x in links if not x['recipeIds']]
    linked_recipes = []
    for recipe in recipes:
        if recipe['id'] not in linked_recipe_ids:
            continue
        donors = []
        for link in resolved_links:
            if recipe['id'] not in link['recipeIds']:
                continue
            names = {norm(x['sourceComponent']['name']) for x in harvest_rows if x['creatureId'] == link['creatureId']}
            donors.append({'creatureId': link['creatureId'], 'creatureName': link['creatureName'],
                           'literalSharedComponentNames': [c['name'] for c in recipe['components'] if norm(c['name']) in names]})
        linked_recipes.append({'sourceRecipe': recipe, 'reviewIndexRecord': review_by_id[recipe['id']], 'donorIngredientCorrespondences': donors,
                               'interpretation': 'A printed reference and shared ingredient do not grant a formula, harvest quantity, access, or a recipe review.'})

    framework_lines = framework_path.read_text(encoding='utf-8-sig').splitlines()
    framework_evidence = [{'line': i + 1, 'text': line} for i, line in enumerate(framework_lines)
                          if 109 <= i + 1 <= 148]
    counts = {'sourceDossiers': len(records), 'harvestProfiles': len(procedures), 'materialCatalogNames': len(materials),
              'recipeCatalogIds': len(recipes), 'harvestOccurrences': len(harvest_rows),
              'literalMaterialNameMatches': len(matches), 'unresolvedMaterialOccurrences': len(unmatched),
              'uniqueUnresolvedMaterialLabels': len({x['sourceComponent']['name'] for x in unmatched}),
              'unresolvedTierSuffixLabels': sum(x['suffixRemovedDiagnostic']['label'] != x['sourceComponent']['name'] for x in unmatched),
              'additionalMaterialMatchesFromSuffixRemoval': sum(bool(x['suffixRemovedDiagnostic']['matchingMaterialName']) for x in unmatched),
              'unresolvedOccurrencesWithComponentLegacyEvidence': sum(bool(x['recipeComponentLegacyNameEvidence']) for x in unmatched),
              'literalMatchedTierDifferences': sum(x['contextComparison']['printedTierDiffers'] for x in matches),
              'literalMatchesWithNumericSourceRateAndValue': sum(x['sourceComponent']['printedRatePercent'] is not None for x in matches),
              'numericRateContextDifferences': sum(x['contextComparison']['printedRateDiffersFromGlobal'] is True for x in matches),
              'numericValueContextDifferences': sum(x['contextComparison']['printedBaseValueDiffersFromGlobal'] is True for x in matches),
              'printedRecipeLinkOccurrences': len(links), 'uniquePrintedRecipeLabels': len({x['printedLabel'] for x in links}),
              'uniqueResolvedRecipeLinkOccurrences': len(resolved_links), 'unresolvedRecipeLinkOccurrences': len(unresolved_links),
              'uniqueUnresolvedRecipeLabels': len({x['printedLabel'] for x in unresolved_links}),
              'printedProcedures': sum(x['sourceDC'] is not None for x in procedures),
              'absentProcedures': sum(x['sourceDC'] is None for x in procedures),
              'printedTimeContextDifferences': sum(x['printedTimeDiffersFromGenericBodySize'] is True for x in procedures),
              'printedDCContextDifferences': sum(x['printedDCDiffersFromGenericHighestTier'] is True for x in procedures),
              'protectedFiles': len(baseline)}
    questions = [
        'For each unresolved harvest label, decide whether it is an unresolved category, a distinct new material, or an explicitly evidenced alias. Do not collapse Animated Core to one of eleven current ingredient names without provenance. Keep all originals and record any approved identity relation separately.',
        'Resolve the Pact Devil (Green Court) infernal marrow tier 2 versus global tier 3. Creature-specific values/rates differ from the global reference in all 31 numeric literal matches; agree the applicable context without overwriting source or adding a second independent drop roll.',
        'Determine what each printed body-level Harvest skill, Harvest DC and Base time actually governs. The generic framework separates identification and trade extraction, has finite shared yields, and allows explicit component DCs. Confirm whether these body-level fields override it, and at which step. Preserve the two absent procedures until decided.',
        'Resolve 38 printed recipe references not found under any current or retained legacy recipe name in this 687-record catalog. Ask the owner/notebook history before declaring the labels nonexistent or superseded. The two resolved names still require all their ordinary components and access rules.',
        'Specify a finite per-creature harvest manifest with exact units, quantities, anatomy, weight, preservation, roll dependence and exceptional-drop status. Do not assume global quantity dice multiply every row or that generic and exceptional yields add. Keep restricted materials/formulas behind their existing access routes.',
        'Confirm harvest/crafting interpretation only. No source deletion, recipe promotion, runtime installation, publication reclassification or cosmology decision is authorized by this comparison. Cosmology remains deferred until the final joint flow review, successful GitHub push and remote verification.'
    ]
    controls = {
        'all67SourceDossiersIncludedWithoutReadingSealedContents': len(records) == 67 and len(procedures) == 66,
        'all178PrintedHarvestRowsAccountedFor': len(harvest_rows) == 178 and len(matches) + len(unmatched) == 178,
        'all696MaterialNamesUniqueUnderOnlyWhitespaceAndCaseNormalization': len(materials) == 696,
        'all687RecipesIndexedByCurrentAndRetainedLegacyNames': len(recipes) == len(review_by_id) == 687,
        'everyPrintedRecipeLineReconstructsFromItsPreservedLabels': all(', '.join(x['printedLabel'] for x in links if x['creatureId'] == record['id']) + '.' == re.search(r'^\*\*Known recipe links:\*\* (.+)$', record['harvest']['sourceText'], re.M)[1].rstrip() for record in records if record['harvest'] and '**Known recipe links:**' in record['harvest']['sourceText']),
        'all40RecipeReferencesAccountedForIncludingTwoUniqueMatches': len(links) == 40 and len(resolved_links) == 2 and len(unresolved_links) == 38,
        'bothMatchedRecipesPreserveFullSourceAndExistingReviewStatus': {x['sourceRecipe']['id'] for x in linked_recipes} == {'recipe-92', 'recipe-173'} and all(x['sourceRecipe'] == next(r for r in recipes if r['id'] == x['sourceRecipe']['id']) for x in linked_recipes),
        'all30DirectorSetRowsRemainNumericallyUnset': sum(x['sourceComponent']['requiresDirectorValues'] for x in harvest_rows) == 30 and all(x['sourceComponent']['printedRatePercent'] is None and x['sourceComponent']['printedValueGp'] is None for x in harvest_rows if x['sourceComponent']['requiresDirectorValues']),
        'twoMissingProceduresStayUnset': sum(x['sourceDC'] is None and x['sourceBaseMinutes'] is None and x['sourceSkillLabel'] is None for x in procedures) == 2,
        'allProtectedSourcesCandidatesReviewCountsAndRuntimeFilesUnchanged': all(sha(GAME / p) == h for p, h in baseline.items())}
    assert all(controls.values()), controls
    report = {'schemaVersion': 1, 'status': 'SOURCE_COMPARISON_ONLY', 'reviewStatus': 'PREPARED_NOT_SENT',
              'scope': 'All Known Descent source-candidate harvest entries, current 696-material/687-recipe crafting catalog and retained recipe/component legacy names. No unobserved notebook history or all-project naming history claimed.',
              'normalization': 'Only whitespace collapse and casefold define literal-name comparisons. Tier suffix removal is a separately labeled diagnostic, never an identity decision.',
              'counts': counts, 'controls': controls, 'sourceHashes': baseline, 'harvestRows': harvest_rows,
              'printedRecipeReferences': links, 'linkedRecipes': linked_recipes, 'harvestProcedures': procedures,
              'frameworkEvidence': {'path': relative(framework_path), 'sha256': sha(framework_path), 'lines': framework_evidence},
              'reviewQuestions': questions, 'sourceEdits': False, 'runtimeInstalled': False, 'cosmologyReviewed': False}
    json_path = AUDIT / (PREFIX + '_AUDIT.json')
    write(json_path, report)

    md = ['# Bestiary harvest and crafting crosslinks', '',
          'Prepared source comparison; not sent to GPT and not a rule approval. All original files and existing review statuses remain unchanged. Cosmology remains deferred until after verified GitHub delivery.', '',
          '## What connects', '',
          f'The 66 harvest profiles contain 178 component occurrences. Only 34 have a literal current material-name correspondence; 144 occurrences (57 distinct labels) do not. Of the unmatched entries, 117 include a printed tier suffix; removing that suffix produces no additional material-name matches. This audit compares only whitespace and case for identities.', '',
          'Three unmatched Animated Core (Tier 1) occurrences have legacy component-name evidence, but that legacy label points to eleven different current materials. The JSON preserves every contributing recipe/component. It is not a unique alias.', '',
          'The one literal-match tier difference is Pact Devil (Green Court): infernal marrow is printed tier 2, while the global material is tier 3. All 31 literal matches with printed numeric rates and values differ from global rates and values. These are context differences requiring a rule decision, not automatic errors. No source is overwritten and no extra roll or price precedence is inferred.', '',
          'Only two of 40 printed recipe links resolve under current or retained legacy recipe names:', '',
          '| Creature | Printed recipe | Catalog ID | Current operational review | Shared printed ingredient |',
          '|---|---|---|---|---|']
    for linked in linked_recipes:
        for donor in linked['donorIngredientCorrespondences']:
            recipe = linked['sourceRecipe']
            md.append(f"| {donor['creatureName']} | {recipe['name']} | {recipe['id']} | {linked['reviewIndexRecord']['status']} | {', '.join(donor['literalSharedComponentNames'])} |")
    md += ['', 'The other 38 occurrences (30 distinct labels) remain unresolved in this catalog. This does not prove that earlier notebook work or another source never contained those names. Both resolved recipes retain their actual ingredients, formula-access rules and review status; a printed link does not grant a recipe.', '',
           '## Procedure interfaces', '',
           f"Of 64 printed harvest procedures, {counts['printedTimeContextDifferences']} times differ from the generic body-size table and {counts['printedDCContextDifferences']} DCs differ from the generic highest-printed-tier lookup. These comparisons do not establish which procedure controls. Crystal Shardling and Pact Automaton Sentinel lack printed skill/DC/time; those fields remain null. The historical dossier has no invented harvest or stat block.", '',
           'Printed skill labels are Arcana, Religion, Medicine, Nature and Engineering. The reviewed framework distinguishes identification from gathering-trade extraction. Its finite shared anatomy/yield manifest, selected-category timing, preservation and exceptional-drop rules must be reconciled with the creature-specific fields before an executable adapter can be accepted.', '',
           'Of the 34 literal material matches, 31 explicitly list the donor name in the retained global sourceMonsters list. The other three lists are truncated with “and N more”; absence from that shortened list does not disqualify the donor.', '',
           '## Decisions to confer on', '']
    md.extend(f'{i}. {question}' for i, question in enumerate(questions, 1))
    md += ['', '## Preservation and evidence', '',
           f"All {len(controls)} bounded controls pass; {len(baseline)} protected source, candidate, review and runtime files retain their hashes. No recipes were promoted, no source values were changed and no runtime data was installed.", '',
           f'- [{PREFIX}_AUDIT.json]({PREFIX}_AUDIT.json) contains every printed harvest row and recipe reference, matched full material/recipe records, legacy component evidence, procedure comparisons and source hashes.',
           f'- [Prepared GPT conference](CODEX_{PREFIX}_CONFERENCE_PREPARED.txt) contains the actual bounded evidence and questions. It has not been sent.',
           f'- [{PREFIX}_STATUS.json]({PREFIX}_STATUS.json) records output hashes and passing checks.', '']
    md_path = AUDIT / (PREFIX + '_AUDIT.md')
    md_path.write_text('\n'.join(md), encoding='utf-8')
    packet_path = AUDIT / ('CODEX_' + PREFIX + '_CONFERENCE_PREPARED.txt')
    packet = ('Prepared, not sent. Continue the existing Decennium Descent source review. This is an internal mechanical-interface evidence packet; no cosmology interpretation is requested. Preserve all originals. The owner requires the final joint flow review before GitHub delivery and cosmology only after the successful, verified push.\n\n'
              + '\n'.join(md) + '\n\nActual bounded evidence follows. Full linked recipes are historical source plus current review-index status; previously reviewed operational cards remain controlling for those reviewed interfaces. Do not treat a source field as reversing a reviewed decision.\n\n'
              + json.dumps({key: report[key] for key in ('normalization', 'counts', 'harvestRows', 'printedRecipeReferences', 'linkedRecipes', 'harvestProcedures', 'frameworkEvidence', 'reviewQuestions')}, ensure_ascii=False, indent=2) + '\n')
    packet_path.write_text(packet, encoding='utf-8')
    write(status_path, {'status': 'PASS_SOURCE_COMPARISON; JOINT_DECISIONS_PENDING', 'reviewStatus': 'PREPARED_NOT_SENT',
                        'sent': False, 'reviewVerdict': None, 'controls': controls, 'counts': counts,
                        'packetCharacters': len(packet), 'artifactHashes': {relative(p): sha(p) for p in (json_path, md_path, packet_path)},
                        'sourceEdits': False, 'runtimeInstalled': False, 'cosmologyReviewed': False})
    print(json.dumps({'counts': counts, 'controls': controls, 'packetCharacters': len(packet)}, indent=2))


if __name__ == '__main__':
    main()
