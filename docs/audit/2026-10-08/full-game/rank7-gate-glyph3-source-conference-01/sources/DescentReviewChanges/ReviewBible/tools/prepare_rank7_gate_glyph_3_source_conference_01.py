"""Freeze complete rank-seven sources and unselected portal/glyph questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank7_gate_glyph_3_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK7_GATE_GLYPH_3_SOURCE_CONFERENCE_01'
    root = A/'rank7-gate-glyph3-source-conference-01'
    out = R/'data/director/spell_review/rank7_gate_glyph_3_source_conference_01.json'
    check, prep, request = [A/(stem+s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A/'DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    cp = R/'data/public/spell_playtests/catalog.json'; ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_20.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('Current membership525/323', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 exact scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank7_gate_glyph_3_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_PERCEPTION_27.json',
              G/'docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json']: bind(p)
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference_lines = (G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        oldp = A/ORIGINALS[ident]; old = read(oldp); bind(oldp)
        n = next(n for n, s in enumerate(old['selectedSpells']) if s['spellId'] == ident)
        historical = old['selectedSpells'][n]; card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident); entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Original/current/queue source equality '+ident, historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No earlier complete procedure '+ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Exact pending identity '+ident, entry['authoredStatus'] == 'pending-authored-procedure')
        ck('All real native routes '+ident, set(card['classAccess']) == ({'Cleric', 'Druid', 'Shaman', 'Wizard'} if ident == 'symbol-of-death' else {'Bard', 'Cleric', 'Mage', 'Mirrorsage', 'Wizard'}))
        ck('Real native rank7 prices and levels '+ident, all(v['rank'] == 7 and v['baseRpCost'] == 17 and v['minimumClassLevel'] == (19 if k in ['Bard', 'Mirrorsage', 'Shaman'] else 13) for k, v in card['classAccess'].items()))
        bb = [deepcopy(b) for b in old['currentBookBindings'] if b['spellId'] == ident]
        ck('Every original placement '+ident, len(bb) == len(card['source']['original']['placements']))
        for b in bb:
            k = b['currentBookRow']['line']-1
            ck('Exact current book line '+ident+str(k), lines[k] == b['currentBookRow']['exactText'])
            ck('Exact preserved reference line '+ident+str(k), reference_lines[k] == lines[k])
        for key in ['catalog', 'core']:
            ck('Underlying source hash '+ident+key, bind(R/card['source'][key+'Path'])['sha256'] == card['source'][key+'Sha256'])
        for cls in card['classAccess']:
            bind(R/('data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if cls == 'Bard' else 'data/public/class_playtests/'+cls.lower()+'.json'))
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Prepared UNSENT; no operational procedure/case adoption.'})
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    selected = list(range(0, 15))+[22, 28, 30, 32, 33, 36, 38, 39, 40, 42]+list(range(43, 49))+[56, 57, 59, 60, 65, 66, 67, 68, 77]+list(range(143, 152))
    for n in selected:
        e = registry['entries'][n]; b = e['currentAuthoritativeSource']; actual = bind(G/b['path'])
        ck('Exact current interface '+str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Retain exact named scope. Extending a source-limited price, clock, body, companion, RNG or copying rule needs explicit new concurrence; no global extension is inferred.'})
    counterparts = []
    names = ['glyph-trace', 'glyph-of-warding', 'death-ward', 'circle-of-death', 'arcane-portal', 'faction-portal',
             'alignment-portal', 'dimensional-door', 'dimensional-anchor', 'planar-protection', 'forbiddance',
             'antimagic-field-lesser', 'greater-dispel', 'guards-and-wards']
    for ident in names:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Reviewed counterpart '+ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent/e['procedureFile']).resolve(); doc = read(path); ptr = e.get('wholeCardPointer', e['procedurePointer'])
        binding = bind(path)
        if e.get('completeEnvelopeBinding'): ck('Whole accepted envelope '+ident, binding == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):
            b = e['authoredAcceptanceReceipt']; ck('Exact authored receipt '+ident, bind(G/b['path']) == b)
        for source in e.get('caseSourceReferenceAliases', {}).values(): bind(G/source)
        shared = at(doc, e['sharedRulesPointer']) if e.get('sharedRulesPointer') else doc.get('sharedRules', {})
        card = at(doc, ptr)
        for key in ['sourceReview', 'reviewEvidence']:
            if isinstance(card.get('operational', {}).get(key), list):
                for name in card['operational'][key]: bind(G/name)
        counterparts.append({'spellId': ident, 'source': binding, 'pointer': ptr,
            'completeCurrentCard': deepcopy(card), 'completeSharedRules': deepcopy(shared), 'indexEntry': deepcopy(e),
            'qualification': 'Actual current index/acceptance governs preserved older candidate labels. Comparison does not extend eligibility to any new spell.'})
    # Full post-push planes authority and original sources qualify the historical receipt.
    bind(A/'LOW_RANK_136_EXACT_FULFILLMENT.json')
    pp = R/'data/director/cosmology/planes_reviewed_01.json'; planes = read(pp); bind(pp)
    pushp = G/'docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json'; push = read(pushp)
    ck('Verified prior push permits careful source conference', push['commit'] == push['remoteMain'] == '7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9' and push['trackedEntriesDeleted'] == 0)
    originals = ['The Cosmology of Decennium Descent.docx', 'The Decennium Descent and the Matrix of Oblivion.docx',
        'The_World_of_Aethel_Lore.docx', 'books/player/Decennium_Descent_Player_Rulebook_v6.docx',
        'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx',
        'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md', 'docs/mechanics/APPENDIX_B_FOLK_RELIGION.md',
        'webpage.html', 'src/data/cosmology-lore.json']
    original_proofs = []
    for name in originals:
        prior = next(b for b in planes['sourceBindings'] if b['path'] == name); actual = bind(G/name)
        ck('Original planes source unchanged '+name, actual == prior)
        original_proofs.append({'priorReviewedBinding': prior, 'currentBinding': actual})
    for p in [G/planes['localVerification']['path'], G/planes['reviewArchive']['path'],
              A/'COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json', A/'COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json',
              A/'COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json', A/'COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json',
              A/'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json', R/'docs/canon/PLAYER_DIRECTOR_BOUNDARY.md',
              R/'data/public/expedition_candidate/complete_candidate.json',
              R/'data/director/cosmology/heartcell_owner_update_02.json', R/'data/director/cosmology/q6_later_lock_reviewed_01.json',
              R/'data/director/cosmology/epilogue_relic_null_reviewed_01.json', R/'data/director/cosmology/epilogue_relic_null_cases_01.json',
              A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_APPLICATION_CHECK.json']:
        bind(p)
    for name in ['CURRENT_COSMOLOGY_READ_FIRST.md', 'PLANES_REVIEWED_01.md', 'HEARTCELL_OWNER_UPDATE_02.md',
                 'OWNER_RECONCILIATION_REVIEWED_01.md', 'Q6_LATER_LOCK_REVIEWED_01.md', 'SOULS_RESEARCH_REVIEWED_01.md']:
        bind(R/'docs/director-only/cosmology'/name)
    # Actual class survival counterparts: do not substitute names for predicates.
    survival = []
    for cls, ident in [('cleric', 'cleric.hero.cultist.ritual-of-undeath'), ('mage', 'mage.hero.lich.undying-spellform')]:
        path = R/('data/public/class_playtests/'+cls+'.json'); d = read(path); b = bind(path)
        n = next(n for n, c in enumerate(d['cards']) if c['id'] == ident)
        survival.append({'source': b, 'pointer': '/cards/'+str(n), 'completeCard': deepcopy(d['cards'][n]),
            'scope': 'Existing actual source predicate, plus current healing/death and Null rules. This comparison supplies no new acquisition or death-prevention exception.'})
    pending = []
    for groupname in ['planar-travel6', 'ward7', 'rank7-mechanics16']:
        g = next(g for g in queue['groups'] if g['group'] == groupname); b = g['candidate']
        ck('Exact pending comparison '+groupname, bind(G/b['path']) == b)
        pending.append({'group': groupname, 'candidate': deepcopy(b), 'identities': deepcopy(g['identities']),
            'scope': 'Full source/proposal/question file included for reconciliation only; unadopted proposals are not accepted authority.'})
    questions = [{'id': i, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': rec, 'decisionSelected': False} for i, ids, src, options, rec in Q]
    ck('15 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 15 and not any(q['decisionSelected'] for q in questions))
    ck('All three identities questioned', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('OneB twoC individually justified', risk == {'C': 2, 'B': 1})
    placements = sum(len(r['completeCurrentBookBindings']) for r in records)
    ck('Three identities three native placements', len(records) == 3 and placements == 3)
    candidate = {'id': 'RANK7-GATE-GLYPH-3-SOURCE-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAcceptedCounterparts': counterparts,
        'pendingComparisonSources': pending, 'completeSurvivalComparisons': survival,
        'cosmologyAuthority': {'currentPlanesReference': info(pp), 'completeQualifiedRegisterUnchanged': deepcopy(planes['register']),
            'completeCurrentQualificationUnchanged': deepcopy(planes['currentQualification']), 'originalSourceProofs': original_proofs,
            'verifiedPriorPush': info(pushp), 'scope': 'Qualified source reference only. Current accepted spell/Null/souls procedures supersede older pending labels only within exact scope. Original manuscripts and saved website retain different provenance; no topology, identity, epoch, revelation or planar-time policy is adopted.'},
        'questions': questions, 'riskCounts': risk,
        'semanticDelta': [{'spellId': r['spellId'], 'riskTier': r['riskTier'], 'riskReason': r['riskReason'],
            'startingPoint': 'Full original source and old questions; no earlier complete procedure or operational case.',
            'genuineQuestionIds': [q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'importantScopeBoundaries': [
            'Chain Gate retains its complete historical post-push receipt and Planar tag. Verified push and qualified planes review permit this careful source conference, not automatic spell/topology approval.',
            'Glyph of Warding is now authored-reviewed despite the older Symbol question calling it pending. Its alarm/repulsion/ward menu,60foot range and minute concentration do not automatically become Symbol mechanics.',
            'Death Ward is positive-to-zero prevention and expressly excludes outright death; Ritual of Undeath is an actual would-die replacement. Null Veil has damage-only provenance rules, and Undying Spellform requires damage reaching0 without killing. These existing distinctions are inherited, not reopened.',
            'Alignment Portal physical-gateway and Faction Portal teleport classifications differ intentionally. Chain Gate needs its own explicit transport scope; Arcane Portal one-transit/capacity restrictions cannot be copied silently.',
            'PlanarTravel6, Ward7 and Rank7Mechanics16 remain unadopted comparisons, including Symbol of Stunning. No family naming supplies shared approval.',
            'Original cosmology/Matrix/world manuscripts and saved website are included with owner corrections and qualified current references; no new plane, soul, Heartcell identity or public knowledge is invented.',
            'Part4 is full; Part5 creation authorization remains pending. This packet is UNSENT, with no actual GPT response or inferred approval.'],
        'earlierOperationalWorkedCases': [], 'currentVectors': [],
        'futureCaseRequirements': [
            'After exact source decisions author at least two complete real-source cases per spell and every materially distinct new branch. No fabricated source profile, endpoint or feat/class acquisition may stand in for missing content.',
            'All cases need exact native access/repertoire, actual class level/PB/ability/RP, actual component/focus, strain/history and paid counter timing. Preserve parent/cast/application/recipient/trigger provenance and complete intermediate/final state.',
            'Chain Gate: all three real aperture poses and selected link graph; qualified actual plane/site prerequisites; complete body/cargo fit/support and movement; each distinct blocker; known illegal versus late invalid crossing; forced versus voluntary motion; partial suppression/closure and deadline equality with no body split or invented rerouting.',
            'Symbol: each full chosen harmful payload and actual save/outcome; true surface/custody/movement, actual sensor paths, initial occupancy versus genuine trigger, allies/owner where relevant, disarm success/failure, consume/counter/expiry and finite multi-glyph dispatch without new hidden facts.',
            'Symbol of Death: actual60versus61normal/formHP and real temporaryHP layer; live and source-qualified nonliving targets; direct nondamage death with no Death Ward/zero-only/Null-damage substitution; real eligible paid Ritual would-die replacement or explicit absent-grant case; preserve real death/remains/cargo history.',
            'Exercise concurrent/successive death-rune events under genuine replacements with exact once-per-event threshold and lifecycle evaluation. No speculative NPC HP/CR or unsourced death immunity can certify a branch.',
            'Use actual known geography and unmodified public/Director knowledge boundaries. Missing cosmological mapping, content profile or accepted counterpart remains an explicit hold, not a new canonical invention.',
            'Source checks and authored deterministic cases do not prove runtime, human gameplay, balance, cosmological canon or whole-game completion.'],
        'countsUnchanged': deepcopy(index['authoredCounts']), 'sourceBindings': list(sources.values()),
        'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytests': 0, 'sourceInformationDeleted': 0,
        'cosmologyDecisions': 0, 'wholeGameComplete': False}
    # All adaptive semantic/source inspection above occurs before creating any output artifact.
    root.mkdir(); frozen = []
    for b in sources.values():
        p = G/b['path']; ck('Current source unchanged '+b['path'], info(p) == b)
        dst = root/'sources'/b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        ck('Frozen exact source '+b['path'], dst.read_bytes() == p.read_bytes())
        frozen.append({**b, 'frozenCopy': dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate': info(out), 'checks': checks, 'checkCount': len(checks), 'sourceCount': len(sources),
        'sourceIdentities': 3, 'placements': placements, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'questions': 15, 'riskCounts': risk, 'failures': 0,
        'validationScope': 'Exact source, native metadata/access, accepted/pending comparison separation and byte preservation only; no new semantic or runtime approval.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    (root/'README.md').write_text('# Three rank-seven gate and glyph sources\n\nRead all complete sources, three original placements,15 unselected questions and14 reviewed spell counterparts. Chain Gate and Symbol of Death are individually tierC; Symbol is tierB. Original cosmology manuscripts, saved website, owner corrections and carefully qualified planes reference are included after verified GitHub push. No new planar topology, soul/Heartcell identity or time policy is adopted.\n\nKeep three linked portals, harmful glyph, and the lethal60HP threshold. Reviewed Glyph of Warding is current authority within its own scope despite older pending wording. Death Ward, Ritual of Undeath, Undying Spellform and Null damage rules remain distinct. Return complete proposed procedures and every question disposition; current operational cases must follow actual design choices.525reviewed/323pending remain unchanged. No source deletion, new rule adoption or GPT delivery is claimed.\n', encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in ['README.md', 'MANIFEST.json']: z.write(root/name, name)
        z.write(out, 'CANDIDATE.json'); z.write(check, 'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'], 'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please conduct the three-spell rank7 gate/glyph source conference using {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read full originals/current access, three placements,15 unselected questions,14 reviewed spell counterparts, actual survival cards and qualified post-push cosmology originals/website/owner corrections. Chain Gate and Symbol of Death are tierC; Symbol tierB. Preserve exactly three linked portals, a native harmful glyph and actual lethal60HP threshold. Reuse existing Death Ward outright-death exclusion, actual would-die replacements and Null damage-only scope. Different portal transport predicates remain source-specific. No topology, identity, spell, case or rule is adopted; return all dispositions and complete proposed procedures with real content holds.525/323membership unchanged.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive': b, 'candidate': info(out), 'manifest': info(root/'MANIFEST.json'),
        'check': info(check), 'request': info(request), 'sourceCount': len(sources), 'allArchiveSourcesVerified': True,
        'riskCounts': risk, 'status': 'Prepared UNSENT; no actual GPT decision on this packet.', 'newRuleAdoptions': 0}))
    print(json.dumps({'archive': b, 'candidate': info(out), 'sources': len(sources), 'checks': len(checks), 'questions': 15, 'riskCounts': risk, 'operationalCases': 0}))


if __name__ == '__main__': main()
