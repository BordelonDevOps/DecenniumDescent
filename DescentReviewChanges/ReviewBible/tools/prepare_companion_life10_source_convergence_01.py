"""Preserve ten complete companion/life proposals without adopting their new rules."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at

IDS = ['summon-corpse-golem', 'soulburn-pact', 'summon-death-knight', 'grave-gift',
       'negative-energy-flood', 'danse-macabre', 'summon-soul-wraith',
       'command-undeath', 'create-undead', 'create-homunculus']


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = R / 'data/director/spell_review/companion_life_10_source_convergence_01.json'
    report = A / 'COMPANION_LIFE_10_SOURCE_CHECK_01.json'
    root = A / 'companion-life10-source-01'
    assert not any(p.exists() for p in [out, report, root])
    sources, checks, records, history, shared = {}, [], [], [], []

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def bind(path):
        b = info(path)
        sources[b['path']] = b
        return b

    mp = R / 'data/director/spell_review/remaining_spell_authoring_map_03.json'
    cp = R / 'data/public/spell_playtests/catalog.json'
    ip = R / 'data/public/spell_playtests/authored_review_index.json'
    rp = R / 'data/director/spell_review/accepted_interface_registry_04.json'
    invp = R / 'data/director/spell_review/ordinary_spell_inventory_03.json'
    bp = R / 'data/playtest/bestiary_public_source_candidate.json'
    mapping, catalog, index, registry, inventory, bestiary = map(read, [mp, cp, ip, rp, invp, bp])
    for p in [mp, cp, ip, rp, invp, bp,
              R / 'data/public/class_playtests/wizard.json',
              R / 'data/public/class_playtests/cleric.json',
              R / 'data/public/class_playtests/mage.json',
              R / 'data/public/class_playtests/ranger.json',
              R / 'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',
              R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
              R / 'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md',
              R / 'docs/mechanics/MAXIMUM_HP_PLAYTEST.md',
              R / 'docs/mechanics/HEALING_DEATH_PLAYTEST.md',
              R / 'docs/mechanics/HEALING_SOURCE_EXTENSIONS.md',
              R / 'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',
              R / 'docs/mechanics/CONDITIONS_PLAYTEST.md',
              R / 'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
              R / 'data/playtest/equipment_acquisition_candidate.json',
              R / 'data/public/expedition_candidate/complete_candidate.json',
              A / 'CODEX_EX58_X01_FULFILLMENT_RECEIPT.txt',
              R / 'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md']:
        bind(p)
    for ident in IDS:
        row = next(r for r in mapping['rows'] if r['id'] == ident)
        oldbinding = row['completeEarlierProposalRecords'][0]
        path = G / oldbinding['source']['path']
        ck('Exact original file: ' + ident, bind(path) == oldbinding['source'])
        document = read(path)
        record = at(document, oldbinding['recordPointer'])
        current = next(s for s in catalog['spells'] if s['id'] == ident)
        ix = next(e for e in index['entries'] if e['id'] == ident)
        ck('Complete procedure: ' + ident, record['spellId'] == ident and bool(record['procedure']))
        ck('Exact current source/access: ' + ident, record['fullSourceAndCurrentAccessRecord'] == current)
        ck('Pending membership: ' + ident, ix['authoredStatus'] == 'pending-authored-procedure' and ident in {r['id'] for r in inventory['pending']})
        records.append({'spellId': ident, 'sourceReference': {'source': info(path), 'pointer': oldbinding['recordPointer']},
                        'completeEarlierRecordUnchanged': deepcopy(record),
                        'completeCurrentCatalogSourceAndAccess': deepcopy(current), 'currentIndexEntry': deepcopy(ix),
                        'riskTier': 'C', 'status': 'Source audit only; complete original procedure preserved; no newly selected rule.'})
        for n, text in enumerate(record['workedCases']):
            history.append({'spellId': ident, 'id': text.split(':', 1)[0], 'exactOriginalText': text,
                            'source': info(path), 'pointer': oldbinding['recordPointer'] + f'/workedCases/{n}'})
        if info(path)['path'] not in {s['source']['path'] for s in shared}:
            shared.append({'source': info(path), 'completeOriginalSharedProposalUnchanged': deepcopy(document['sharedProposal']),
                           'completeOriginalJointIssuesUnchanged': deepcopy(document['explicitJointIssues'])})
        for kind in ['catalog', 'core']:
            ck('Underlying source ' + kind + ': ' + ident, bind(R / current['source'][kind + 'Path'])['sha256'] == current['source'][kind + 'Sha256'])
    interfaces = []
    for n in list(range(15)) + [18, 24, 25, 26, 31, 34, 36, 39, 40, 49, 50, 51, 52, 53, 80, 81, 82, 83, 84, 85, 86, 88]:
        e = registry['entries'][n]
        b = e['currentAuthoritativeSource']
        actual = bind(G / b['path'])
        ck('Exact accepted authority: ' + str(n), actual['bytes'] == b['bytes'] and actual['sha256'] == b['sha256'])
        interfaces.append({'registryPointer': f'/entries/{n}', 'completeEntryUnchanged': deepcopy(e),
                           'scopeLimit': 'Existing source scope only; no universal summon suppression, CR, command transfer, healing exception or new RNG-disclosure permission.'})
    counterparts = []
    for ident in ['animate-dead', 'soul-tap', 'vampiric-touch', 'mending', 'dominate-beast', 'dominate-person']:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Reviewed counterpart: ' + ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent / e['procedureFile']).resolve()
        doc = read(path)
        ptr = e.get('wholeCardPointer', e['procedurePointer'])
        counterparts.append({'spellId': ident, 'source': bind(path), 'wholeCardPointer': ptr,
                             'completeCurrentCard': deepcopy(at(doc, ptr)), 'completeSharedRules': deepcopy(doc.get('sharedRules', {})),
                             'indexEntry': deepcopy(e)})
    comparisons = []
    for filename, idents in [('persistent_damage_20_current_06', ['enervation', 'leeching-plague']),
                             ('control_15_current_11', ['dominate-monster'])]:
        path = R / f'data/director/spell_proposals/{filename}.json'
        doc = read(path)
        for ident in idents:
            n, s = next((n, s) for n, s in enumerate(doc['spells']) if s.get('id', s.get('spellId')) == ident)
            comparisons.append({'spellId': ident, 'source': bind(path), 'pointer': f'/spells/{n}',
                                'completeRecord': deepcopy(s), 'status': 'Pending comparison only, not accepted authority.'})
    deltas = [
        ('summon-corpse-golem', 'Temporary Construct without a real corpse input; fixed HP60/AC15, mass600, finite incidental carrying and separately commanded Slam/Slow Aura.', 'Confer on creation-round command, declared enemy set, one CON attempt per aura activation, ordinary command channel and full-suppression ending. Same owner offense prevents a simultaneous Slam and aura.'),
        ('soulburn-pact', 'Printed 20 normal HP payment; catalog up-to3RP versus Core5RP and retained rank4 base7RP.', 'Explicitly choose the source conflict, self-target scope, pre-counter HP payment and one beneficial-LR use. Retaining7RP cost and recovering3 produces net-4RP; do not disguise this as resource generation or invent a discount.'),
        ('summon-death-knight', 'One finite HP80/AC18 Undead summon with complete new abilities, 2d10 necrotic attack and intrinsic nonloot sword/armor.', 'Confirm suppression suspends rather than ends this body; define actual original-space/adjacent pending placement using only the adopted local rule. Real cargo drops and never rematerializes or teleports.'),
        ('grave-gift', 'Half-current-normal-HP cost and full-effective-maximum recovery of another willing living dying/Stable creature.', 'Direct state assignment bypassing ordinary Critical ceiling is material new authorship. Independent stabilization through a broad HP-gain prohibition, preservation of an already-Stable deadline, and downstream actual-gain triggers need explicit disposition.'),
        ('negative-energy-flood', 'Single-target CON 5d12 full/half and animation only following actual qualifying Humanoid death from this exact packet.', 'Agree exact immediate response/body-claim order versus Auto-Raise; one-hour one-zombie cap, complete proposed zombie profile, no creation-round acts, actual consumed remains and source-specific suppression.'),
        ('danse-macabre', 'Up to five real Small/Medium Humanoid corpses, complete new zombie profile and shared owner command/offense.', 'Confirm 24-hour eligibility, one-hour cohort, separate five-body cap, successful-cohort replacement, retained missing anatomy and no creation-round acts. Do not silently create or remove physical remains.'),
        ('summon-soul-wraith', 'Finite HP100/AC18 Undead manifestation with Fly40/Hover, 2d10 necrotic, self lifetap and incorporeal passage.', 'Confer on restricted funding provenance distinct from Vampiric Touch, temporary-HP funding, real cargo blocking wall passage, finite entry-path expulsion and suppression ending. No new soul or afterlife claim.'),
        ('command-undeath', 'Permanent until dispelled control of at most two existing Undead, proposed literal exact CR2, WIS and non-Charmed hard admission.', 'Choose CR interpretation and permanent defensive-only restriction. Keep original creature type, own native attack sequence, scheduling and dual-owner budgets; owner absence/death must not produce an invented phase. Suppression restores real agency without a duplicate opportunity.'),
        ('create-undead', 'Four full new Ghoul/Ghast/Wight/Mummy profiles, one real corpse each, permanent body conversion and a separate two-slot magical creator authority.', 'Discuss consequence of repeated creation/release of permanent independently acting bodies; profile scope, unrated CR, original-owner scaling after release, suppression/dispelling of control only, and literal body requirements. No imported bestiary abilities or resurrection lore.'),
        ('create-homunculus', 'One persistent Tiny physical Construct: HP20/AC14,8lb,STR6,walk20/Fly30/Hover,45lb and3Load carrying, safe supervised chores.', 'Discuss created body ending on dispel/full suppression, allowed standing chores versus actual work roles, spoken command channel, source-qualified HP modifiers and paid Action/touch/2RP/2d6 repair. Maintenance is proposed nonspell, not an extra spell or resource reset.'),
    ]
    semantic = [{'spellId': ident, 'sourcePreserved': True, 'originalScope': old, 'newDecisionsRequired': new, 'riskTier': 'C'} for ident, old, new in deltas]
    findings = [
        ('CL10-F01', ['soulburn-pact'], 'SOURCE CONFLICT / DESIGN QUESTION',
         'Catalog up-to3RP and Core5RP disagree. The old proposal deliberately chooses3 while retaining a7RP cast and20HP cost; its once-beneficial-rest restriction is also new.',
         'Show both complete source values and actual cost arithmetic; ask GPT for an explicit choice and useful intended behavior before current authorship.'),
        ('CL10-F02', ['grave-gift'], 'NEW SOURCE-SPECIFIC EXCEPTION',
         'The proposal makes full-HP recovery a direct state operation. Existing healing distinctions support separating operation types, but do not themselves authorize Grave Gift to bypass Critical or independently stabilize.',
         'Confer on both components, actual willing recipient, 31→16 and2→1 donor costs, broad prohibition and unchanged Wounds/Stable deadline. Preserve the full former procedure.'),
        ('CL10-F03', ['summon-corpse-golem', 'summon-death-knight', 'summon-soul-wraith', 'create-homunculus', 'create-undead', 'danse-macabre', 'negative-energy-flood'], 'LOCAL LIFECYCLE CHOICES',
         'Full suppression is not uniform: Golem/Wraith/Homunculus end; Knight suspends absent; Flood/Danse keep inert real bodies; Create Undead keeps its active body while authority is suppressed.',
         'Review each exact rule. Do not generalize accepted pet suppression to these pending spells. Supply real antimagic locus, deadline, body/cargo and placement traces.'),
        ('CL10-F04', ['negative-energy-flood', 'danse-macabre', 'create-undead'], 'BODY IDENTITY / TIMING',
         'Animation consumes one actual body allocation without duplicating gear, donors or remains. Flood proposes a post-immediate-response claim before a later Auto-Raise checkpoint; Danse/Create Undead propose distinct admission and duration rules.',
         'Bind real damage/lifecycle and actually eligible corpse provenance. A newly0 surviving significant NPC, already consumed body, copied summon and reconstructed living identity must not be treated as the same eligible corpse case.'),
        ('CL10-F05', ['command-undeath', 'create-undead'], 'MISSING PROFILE AUTHORITY',
         'The four newly proposed animations are explicitly unrated. Source-only bestiary rows do not constitute operative creature approval, and no appearance or another class companion profile proves exactCR2.',
         'Keep CR2 examples conditional unless an actual individually approved complete creature profile exists. Decide exact2 versus≤2 explicitly against both printed sources.'),
        ('CL10-F06', ['create-undead'], 'UNBOUNDED PERMANENT BODY CONSEQUENCE',
         'The cap limits creator control relations, not surviving permanent bodies. Repeated paid casts with new corpses and declared releases can leave arbitrarily many independent animations over time.',
         'Ask whether that consequence is intentional; if so, define retained needs, agency, scheduling and ownership through actual rules. Do not silently add a world population cap or guaranteed hostility.'),
        ('CL10-F07', ['summon-soul-wraith'], 'EXAMPLE ERROR / UNSUPPLIED SOURCE',
         'IN6-07-A supplies17 post-defense necrotic and5temp+7normal actual loss, but lacks a complete real Cleric build, attack/dice, target lifecycle, transfer tree and healing modifiers. Its numeric12→6→3 remains a valid conditional arithmetic obligation.',
         'Preserve that arithmetic; add actual source-qualified full case. A new funding exclusion for created/animated bodies must not rewrite accepted Vampiric Touch or Soul Tap.'),
        ('CL10-F08', ['summon-soul-wraith'], 'PLACEMENT / REAL CARGO',
         '15ft wall travel costs30 fromFly40 only when the actual route is legal. Forced expulsion, no-entry-path fallback, fully obstructed placement and real cargo need explicit deterministic finite geometry.',
         'Preserve the30/10 movement obligation. Avoid gear teleportation to a distant last-open point after arbitrary later movement, and specify the actual position/departure record used.'),
        ('CL10-F09', ['command-undeath'], 'PERMANENT CONTROL AND SCHEDULING',
         'Permanent non-Charmed whole-Action restriction claims hard admission once; existing companion chassis and independent actors use different schedules. Caster death creates an absent binder phase, not a new automatic turn.',
         'Review ordinary agency while suppressed, next unresolved regular opportunity, original-owner structural reservations, competing orders, release and refusal/resource limits as separate state transitions.'),
        ('CL10-F10', ['create-homunculus'], 'MAINTENANCE / ECONOMY',
         'A new2RP Action touch repair is not ordinary organic healing or automatic Mending permission. An unskilled servant standing chore must not silently satisfy real recipe assistants, crew attendance or valuable production.',
         'Bind legal repair scope, two real dice totaling8, actual class RP, a real fitted container/lantern, capacity and actual EX58 work rules. Preserve7→15/20 and no salvage/gear reset.'),
        ('CL10-F11', IDS, 'CURRENT EXAMPLE RECONCILIATION',
         'The old rank5 shared baseline raises Dissonance to1 on a fresh ordinary cast. The current Wizard first-distinct prepared-spell rule instead has the exact accepted source cadence; old baseline text is historical evidence.',
         'Rebuild all20 current cases with actual class/school/acquisition, RP, cadence, HP, real Action/Bonus Action, geometry and source-qualified ownership. Preserve every original scenario ID/text.'),
        ('CL10-F12', ['summon-corpse-golem', 'negative-energy-flood', 'danse-macabre', 'create-undead'], 'NEW PROFILE AND ACTION CHOICES',
         'Golem Slow Aura replaces Slam; Flood/Danse use a new20HP zombie rather than Wizard standard minions; Create Undead has four complete distinct new profiles. Creation-round permission differs by source.',
         'Discuss every profile and round gate, actual native anatomy/armor, source DC snapshot/current distinctions and command channel without importing external-game monster rules.'),
    ]
    findings = [{'id': fid, 'spells': ids, 'classification': kind, 'finding': finding, 'nextStep': step}
                for fid, ids, kind, finding, step in findings]
    exact_names = ['Ghoul', 'Ghast', 'Wight', 'Mummy']
    search = {'source': info(bp), 'scope': 'Exact names in current public source candidate only; not an exhaustive historical-archive search.',
              'exactNameMatches': {name: [{'pointer': f'/records/{i}', 'completeRecordUnchanged': deepcopy(row)} for i, row in enumerate(bestiary['records']) if row.get('name', '').casefold() == name.casefold()] for name in exact_names},
              'exactCR2UndeadSourceRows': [{'pointer': f'/records/{i}', 'id': row['id'], 'name': row['name'], 'reviewStatus': row.get('reviewStatus'), 'printedFields': deepcopy(row.get('statBlock', {}).get('printedCoreFields', {}))} for i, row in enumerate(bestiary['records']) if row.get('statBlock', {}).get('printedCoreFields', {}).get('type', '').casefold() == 'undead' and str(row.get('statBlock', {}).get('printedCoreFields', {}).get('challengeRating')) == '2'],
              'qualification': 'Source rows alone do not establish an operative creature or approved CR. Proposed four spell profiles remain explicit new designs.'}
    other_ids = set()
    for filename in ['damage_control_25_current_08', 'persistent_damage_20_current_06', 'illusion_perception_14_current_11', 'control_15_current_11']:
        other_ids.update(s.get('id', s.get('spellId')) for s in read(R / f'data/director/spell_proposals/{filename}.json')['spells'])
    other_ids.update(['woven-threads', 'haze-of-forgetting', 'creation'])
    terrainp = R / 'data/director/spell_review/material_terrain_8_source_convergence_01.json'
    other_ids.update(r['spellId'] for r in read(terrainp)['records'])
    bind(terrainp)
    ck('Ten distinct spells and20 preserved original cases', len(records) == len(set(IDS)) == 10 and len(history) == len({r['id'] for r in history}) == 20)
    ck('No overlap with85 separately queued/audited identities', len(other_ids) == 85 and not set(IDS) & other_ids)
    ck('All semantic deltas cover exact cohort', {r['spellId'] for r in semantic} == set(IDS))
    root.mkdir()
    frozen = []
    for b in sources.values():
        ck('Current full source: ' + b['path'], info(G / b['path']) == b)
        p = root / 'sources' / b['path']
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((G / b['path']).read_bytes())
        ck('Exact preserved copy: ' + b['path'], info(p)['sha256'] == b['sha256'])
        frozen.append({**b, 'frozenCopy': p.relative_to(G).as_posix()})
    (root / 'MANIFEST.json').write_bytes(encoded({'sourceCount': len(frozen), 'sources': frozen, 'newRuleAdoptions': 0}))
    result = {'id': 'COMPANION-LIFE-10-SOURCE-CONVERGENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
              'status': 'SOURCE_AND_INTERFACE_AUDIT_ONLY; ten complete procedures and20 original cases preserved; UNSENT/UNADOPTED. No substantial new rule chosen.',
              'developmentDirection': 'video-game-only', 'records': records, 'all20HistoricalScenarioTexts': history,
              'completeOriginalSharedProposalsUnchanged': shared, 'currentAcceptedInterfaceComparisons': interfaces,
              'completeAcceptedCounterparts': counterparts, 'completePendingCounterparts': comparisons,
              'semanticDelta': semantic, 'findings': findings, 'bestiarySourceSearch': search, 'riskCounts': {'C': 10},
              'sourceBindings': list(sources.values()), 'sourceManifest': info(root / 'MANIFEST.json'),
              'nextRequiredWork': 'Prepare explicit design-conference alternatives and complete conditional/current cases; confer with actual GPT before choosing new lifecycle, permanent-control, resource or recovery rules. This is not a completed conference packet.',
              'countsUnchanged': {'reviewed': 480, 'pending': 368}, 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0,
              'cosmologyDecisions': 0, 'sourceInformationDeleted': 0}
    out.write_bytes(encoded(result))
    report.write_bytes(encoded({'audit': info(out), 'checkCount': len(checks), 'failureCount': 0, 'checks': checks,
                               'sources': len(sources), 'fullOriginalProcedures': 10, 'originalCases': 20,
                               'findings': len(findings), 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0}))
    print(json.dumps({'audit': info(out), 'checks': len(checks), 'sources': len(sources), 'originalProcedures': 10, 'originalCases': 20, 'findings': len(findings), 'sourceCR2UndeadCount': len(search['exactCR2UndeadSourceRows'])}))


if __name__ == '__main__':
    main()
