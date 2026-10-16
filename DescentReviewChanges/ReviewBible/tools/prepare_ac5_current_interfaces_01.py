"""Prepare current AC5 source/interface evidence while Banishment is under review."""
from datetime import datetime, timezone
from pathlib import Path
import json, re
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def at(d, pointer):
    if not pointer:
        return d
    for part in pointer.strip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        d = d[int(part)] if isinstance(d, list) else d[part]
    return d


def main():
    target = A / 'AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json'
    assert not target.exists()
    historical_path = R / 'data/director/spell_proposals/abjuration_conjuration_rank5.json'
    historical = read(historical_path)
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    index_path = R / 'data/public/spell_playtests/authored_review_index.json'
    catalog = read(catalog_path)
    index = read(index_path)
    current = {c['id']: (i, c) for i, c in enumerate(catalog['spells'])}
    entries = {c['id']: c for c in index['entries']}
    old_preparations = [read(A / n) for n in ['ABJURATION_RANK5_SOURCE_PREPARATION.json', 'CONJURATION_RANK5_SOURCE_PREPARATION.json']]
    selected = [r for p in old_preparations for r in p['selectedSpells']]
    assert len(selected) == len({r['spellId'] for r in selected}) == 16
    source_paths = {G / rel for rel in historical['sourceFiles']}
    source_paths.add(historical_path)
    source_paths.update(G / b['path'] for b in read(A / 'banishment-current-review-01-input/CURRENT_REVIEW_INPUT.json')['sourceBindings'])
    source_paths.add(A / 'BANISHMENT_CURRENT_REVIEW_01_LOCAL_AUDIT.json')
    source_paths.add(A / 'BANISHMENT_REPAIR_02_SUBMISSION_RECEIPT.json')
    drift = []
    for rel, old in historical['sourceFiles'].items():
        fresh = info(G / rel)
        if fresh['bytes'] != old['bytes'] or fresh['sha256'] != old['sha256']:
            drift.append({'path': rel, 'historicalBinding': old, 'currentBinding': fresh})
    selected_records = []
    for old in selected:
        i, card = current[old['spellId']]
        assert card == old['fullSourceAndCurrentAccessRecord'], card['id']
        selected_records.append({
            'spellId': card['id'], 'questionId': old['questionId'],
            'sourceFile': info(catalog_path), 'pointer': f'/spells/{i}',
            'completeCurrentSourceAndAccess': card, 'currentAuthoredIndexEntry': entries[card['id']],
            'historicalQuestionUnchanged': old['individualQuestion'],
            'historicalScope': old['scope'],
            'currentReviewScope': 'Full operational authoring required; prior push-dependent deferral is historical. Preserve identity and all source placements; current owner cosmology locks remain controlling.',
            'historicalProposal': next((r for r in historical['records'] if r['spellId'] == card['id']), None),
        })
    compare_ids = {c['id'] for c in historical['completeCurrentCounterparts']}
    compare_ids.update(['dimensional-anchor', 'resonance-dampening-field', 'alignment-lock', 'alignment-anchor', 'summon-water-pet', 'faction-ally', 'alignment-purge', 'alignment-suggestion', 'planar-window', 'banishment', 'counterspell'])
    comparisons = []
    for ident in sorted(compare_ids):
        i, card = current[ident]
        ent = entries[ident]
        record = {'id': ident, 'catalogBinding': info(catalog_path), 'catalogPointer': f'/spells/{i}', 'completeCatalogCard': card, 'currentAuthoredIndexEntry': ent}
        rel = ent.get('procedureFile')
        if rel:
            source = (index_path.parent / rel).resolve()
            assert source.is_relative_to(G)
            doc = read(source)
            source_paths.add(source)
            record['authoredFile'] = info(source)
            record['completeAuthoredCard'] = at(doc, ent.get('wholeCardPointer', ent['procedurePointer']))
            if ent.get('sharedRulesPointer'):
                record['completeSharedRules'] = at(doc, ent['sharedRulesPointer'])
            if ent.get('supportingProfilePointers'):
                record['supportingProfiles'] = {p: at(doc, p) for p in ent['supportingProfilePointers']}
        comparisons.append(record)
    class_paths = sorted(p for p in source_paths if p.parent == R / 'data/public/class_playtests' or p.name == 'Decennium_Descent_Bard_Playtest_v0_1.json')
    assert len(class_paths) == 17
    pattern = re.compile(r'antimagic|dispel|banish|extraplanar|planar|suppress|conversion|resonance.{0,24}(cost|shield|barrier)|spell.{0,12}resist|faction', re.I)
    navigation = []

    def walk(v, pointer, path):
        if isinstance(v, dict):
            if isinstance(v.get('id'), str) and ('effect' in v or 'activation' in v) and pattern.search(json.dumps({k: val for k, val in v.items() if k != 'source'}, ensure_ascii=False)):
                navigation.append({'path': path.relative_to(G).as_posix(), 'pointer': pointer, 'completeCard': v, 'status': 'lexical navigation only; not independent semantic approval'})
                return
            for k, val in v.items():
                walk(val, pointer + '/' + k.replace('~', '~0').replace('/', '~1'), path)
        elif isinstance(v, list):
            for i, val in enumerate(v):
                walk(val, pointer + '/' + str(i), path)

    for path in class_paths:
        walk(read(path), '', path)
    issues = [
        ('AC5-CURRENT-01', 'Historical scope and authority', 'The eleven Oct11 operating proposals and22 authored cases remain unadopted. The five post-push receipts are now active authoring work, not permanent exclusions. Preserve all16 identities and17 printed placements, including both Planar Binding placements. Refresh the input after Banishment is accepted; no unfinished Banishment rule may become authority by inclusion.'),
        ('AC5-CURRENT-02', 'Null damage and finite summons', 'The old shared summon rule ends every body at0HP. Current EPI Null procedures instead retain qualifying finite bodies as Null Disabled0 while their own source persists. Greater Fire Pet and Faction Champion need explicit current lifecycle, subsequent Null hit, real healing, independent expiry and real cargo handling. AC4-SUMMON-TARGET-01 is scoped to its two profiles; extending that healing predicate to new profiles requires explicit NEW authorship.'),
        ('AC5-CURRENT-03', 'Damage-root timing', 'Living Magma delayed ticks need an explicit original damage-root checkpoint and inherited Veil flag; a commanded companion attack uses that body\'s actual dealer identity. Define whether Greater Fire Pet aura checkpoints constitute separate root creation and reuse only rolls, without copying a different actor\'s Veil status. Suppression consumes scheduled opportunities without inventing damage roots for nonexistent packets.'),
        ('AC5-CURRENT-04', 'Nexus, Dampening and final price', 'Accepted AC4 Dampening applies mandatory+2 after ordinary reductions/waivers/minimum and before final Influence. The old Nexus proposal inserts a new reduction after mandatory extras. Decide an explicit source-coherent order with exact waiver, charge-only real spell, cantrip, protected conversion principal and concentration replacement. Do not silently change accepted Dampening or treat a nonspell class engine as a spell because it costs RP.'),
        ('AC5-CURRENT-05', 'Conversion and damage prevention', 'Resonance Barrier must define which paid price components buy the pool, especially Nexus/Ease/Burden/Dampening/surcharge and protectedX. Compare actual Harmonic Bulwark and Resonance Shield. No credit for waived/unpaidRP, no double conversion from copied source, no second mitigation of an unmitigated transfer, no prevented-damage recovery or stale source refresh.'),
        ('AC5-CURRENT-06', 'Antimagic and existing sources', 'Define exact local suppression and originating-path claims against current remote-destination spells, real teleports and AC4 ward/anchor sources. A global beam/path must not be invented for every nonprojectile spell. Item/nonspell magical components need actual source classification. Preserve pending geometry, body suppression, genuine nonliving objects and clocks. Banishment suppression will use only its eventual accepted exact interface.'),
        ('AC5-CURRENT-07', 'Dispel and Xi boundaries', 'Greater Dispel needs actual spell-effect records, real generating ranks, stable finite capture, exact source-dependent versus indivisible ending and current natural-shift checks. Xi is a different consent-based branch-ending ability; do not import its whole-zone prohibition into every dispel, or give it a new whole-zone permission. Use actual reviewed higher-rank effects for numeric examples.'),
        ('AC5-CURRENT-08', 'Force wall and environment', 'Define physical/path/light/sound/support and suppression/resumption boundaries against current Anchor/Dimensional Door/Beacon and ordinary Falling. Keep current environmental procedures separate from proposed environment packets. Air does not vanish when a wall appears, and geometry restoration cannot crush, bisect or force a chosen displacement.'),
        ('AC5-CURRENT-09', 'Faction relations and protection', 'Faction Ally currently needs membership plus invocation permission; Faction Portal needs positive standing and its own HQ gate. Neither automatically defines allied faction for Champion. Decide explicit Champion eligibility and preserve distinct credentials. Reputation Shield must use current EX58 event provenance, signed contributions, caps, corrections and actual voluntary standing costs without retroactive immunity, debt or compelled NPC friendship.'),
        ('AC5-CURRENT-10', 'Banish Elemental versus Elemental Banishment', 'AB5-02 targets Elemental OR outsider with CHA negation and Instantaneous metadata; CJ5-04 targets one summoned enemy, CHA save and concentration minute. Do not merge them or assume outsider, summoned, Elemental and extraplanar are synonyms. Define eligibility evidence, unknown-source handling, destination/ending and corpse/cargo/lifecycle under source-specific NEW rules. An accepted ordinary Banishment interface can be reused only through explicit scope, retaining these distinct source promises.'),
        ('AC5-CURRENT-11', 'Planar Protection and Planar Binding', 'Protection wards an area against creatures from a specific plane; supply actual provenance predicate, finite geometry, already-inside/entry/forced/carrying/teleport/suppression and ending without turning creature type into plane identity. Binding preserves24h service and the Universal Instantaneous metadata conflict. Define extraplanar eligibility, save/command/companion/hard-control ownership, source lifespan and service limits; no free RP, duplicated initiative or conjured creature follows from service. Do not erase24h service merely to make a simpler combat debuff.'),
        ('AC5-CURRENT-12', 'Alignment Portal', 'Preserve a gateway to an actually alignment-compatible plane, not a same-plane teleport or merely an observation window. Use current plane dossiers and owner locks; never treat four dominions, tributaries and32mortalWheel labels as interchangeable origin ontology. Define actual destination knowledge, compatible alignment evidence, AC4 Lock/Anchor and AP-AS-01 Suggestion/Purge predicates, finite gate geometry/crossing/arrival/cargo/failure/clock. No free named-plane mapping, secret identity disclosure, soul settlement or time/rest reset.'),
    ]
    cases = [
        ('Null-disabled Fire Pet', 'Greater Fire Pet reaches0 from qualifying Null; another Null hit, actual healing attempt, then independent expiry. Keep body/source and cargo ledgers distinct.'),
        ('Null-disabled Champion', 'Faction Champion takes qualifying Null versus ordinary lethal damage in separate fixtures. Decide exact healing target predicate and no fabricated soul or corpse loot.'),
        ('Living Magma provenance', 'Veiled actual caster applies the recurring spell, loses Veil before later ticks, and target is0on a later tick. Record the chosen real root timing, inherited flag and real Stable/death behavior.'),
        ('Pet aura identity', 'Owner has Veil but companion does not; commanded fire attack and aura against two recipients have explicit source/dealer and separate recipient packets.'),
        ('Nexus plus Dampening', 'An actual rank5 spell inside both fields is cast with ordinary10RP base and final Ease1. Show the accepted exact price stages, then compare a real base-only waiver.'),
        ('Charge-only and nonspell', 'A real charge-only spell versus an RP-paid nonspell class feature inside both fields. No invented RP pool or automatic rank from cost.'),
        ('Barrier conversion', 'Actual base10, protectedX2, mandatory field extra and final Influence; show actual paid costs and prevention credit without crediting unpaid or surcharge points.'),
        ('Transferred damage', 'A17-point received branch explicitly bypasses mitigation while Barrier remains. Show unchanged prevention pool and actual recipient damage.'),
        ('Antimagic versus remote travel', 'Current Dimensional Door has exact known unseen destination beyond an antimagic sphere but neither endpoint intersects. Decide actual path predicate without importing a beam.'),
        ('Antimagic body/item resume', 'A current finite summon carrying an ordinary lantern and an actual magical item are locally suppressed; restore only source-permitted bodies/bonuses without new HP, inventory or time.'),
        ('Greater Dispel snapshot', 'A wall in capture blocks another effect; terminate captured rank5and a reviewed rank7source with an actual check; do not expand the initial capture after the wall ends.'),
        ('Force-wall support', 'Horizontal wall supports a body; suppression removes a segment; a body occupies it on resumption; actual Falling and pending clearance retain real clocks.'),
        ('Reputation protection', 'One scene has+1and-2institutional contributions, followed by a genuine correction and a transaction requiring1standing. Show provenance and caps.'),
        ('Champion faction gate', 'Separate actual membership/invocation permission, positive standing, allied status and explicit aid prohibition; apply chosen source-specific gate without replacing other faction spells.'),
        ('Banish Elemental type scope', 'An actual Elemental, an actual source-classified outsider and a merely foreign ordinary mortal face separate casts. No automatic synonym or inferred origin.'),
        ('Elemental Banishment source scope', 'Actual finite summoned enemy versus transported ordinary hostile and nonsummoned Elemental. Preserve one summoned enemy criterion and its printed minute.'),
        ('Banish ending and cargo', 'Chosen eligible target has real gear, a separately carried creature, a later independent summon expiry and a real endpoint blocker. Resolve all actual identities under the exact chosen rule.'),
        ('Planar ward crossing', 'Creature with established plane provenance begins inside the area; another attempts forced/carried physical entry; another legally teleports beyond. Supply source-specific outcomes.'),
        ('Unknown provenance', 'A creature lacks an established plane-origin record. Resolve spell legality/information without secretly identifying it or equating current location with native origin.'),
        ('Binding versus finite source', 'A bound extraplanar creature\'s own summon expires before24h. Preserve printed service where a body exists without prolonging its source or recreating it.'),
        ('Binding commands and budgets', 'Two controllers issue conflicting orders with real command/offense resources and source-owner stats. Resolve source priority, unsafe/impossible service and timing explicitly.'),
        ('Alignment destination', 'Known actual aligned plane and known destination site versus a mortal Wheel label with unproved identity; preserve true gateway and prevent invented mapping.'),
        ('Alignment current overlays', 'Caster has actual accepted Lock/Anchor and an underlying Suggestion/Purge. Determine current compatible-plane predicate at the precise portal checkpoint without rewriting underlying records.'),
        ('Portal atomic crossing', 'One actual group carries real cargo through at expiry/Anchor obstruction. Preserve atomic legal placement, costs, finite doorway closure and all real clocks.'),
    ]
    result = {
        'id': 'AC5-CURRENT-SOURCE-INTERFACE-AUDIT-01',
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Prepared local source/interface audit; not sent, not jointly reviewed, no new procedures adopted. Refresh Banishment dependency before dispatch.',
        'selectedIdentityCount': 16, 'printedPlacementCount': sum(len(r['completeCurrentSourceAndAccess']['source']['original']['placements']) for r in selected_records),
        'historicalProposalFile': info(historical_path), 'historicalProposalCount': len(historical['records']),
        'historicalAuthoredCaseCount': sum(len(r['workedCases']) for r in historical['records']),
        'selectedSourcesUnchanged': True, 'selectedRecords': selected_records,
        'currentAuthoredCounts': index['authoredCounts'], 'historicalSourceDrift': drift,
        'completeCurrentComparisons': comparisons,
        'classEnvelopeCount': len(class_paths), 'classFiles': [info(p) for p in class_paths],
        'classNavigationWarning': 'Automated lexical navigation only; not exhaustive semantic review or proof that every matching class card applies.',
        'classNavigation': navigation,
        'currentReviewIssues': [{'id': i, 'title': title, 'requiredReview': body} for i, title, body in issues],
        'requiredAdditionalExamples': [{'id': f'AC5-X{i:02}', 'title': title, 'requiredResolution': body, 'adopted': False, 'runtimeTest': False} for i, (title, body) in enumerate(cases, 1)],
        'banishmentDependency': {'status': 'Repair02 generating; no accepted ordinary Banishment procedure yet', 'receipt': info(A / 'BANISHMENT_REPAIR_02_SUBMISSION_RECEIPT.json'), 'refreshRequiredBeforeSending': True},
        'sourceBindings': [info(p) for p in sorted(source_paths)],
        'manualReadScope': 'All eleven historical proposal procedures/shared rules and22 case texts, all five formerly deferred exact source records, current accepted interfaces summarized in prior exact reviews. Class lexical hits are not claimed independently read.',
        'sourceInformationDeleted': 0, 'newSpellAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
    }
    assert result['printedPlacementCount'] == 17
    target.write_bytes(encoded(result))
    print(json.dumps({'audit': info(target), 'selectedSpells': 16, 'printedPlacements': 17, 'currentComparisons': len(comparisons), 'sourceFiles': len(source_paths), 'sourceDrifts': len(drift), 'classEnvelopes': len(class_paths), 'lexicalNavigationCards': len(navigation), 'currentIssues': len(issues), 'additionalAuthoredScenariosRequired': len(cases)}))


if __name__ == '__main__':
    main()
