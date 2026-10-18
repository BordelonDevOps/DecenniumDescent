"""Preserve eight complete terrain/material proposals and audit their current gaps."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at

IDS = ['control-water', 'fabricate', 'transmute-terrain', 'magnetize-field', 'passwall', 'transmute-rock', 'displace-structure', 'move-earth']


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = R / 'data/director/spell_review/material_terrain_8_source_convergence_01.json'
    report = A / 'MATERIAL_TERRAIN_8_SOURCE_CHECK_01.json'
    root = A / 'material-terrain8-source-01'
    assert not any(p.exists() for p in [out, report, root])
    sources, checks, records, history, shared = {}, [], [], [], []

    def ck(n, value):
        checks.append({'check': n, 'passed': bool(value)})
        assert value, n

    def bind(p):
        b = info(p)
        sources[b['path']] = b
        return b

    mapp = R / 'data/director/spell_review/remaining_spell_authoring_map_03.json'
    catalogp = R / 'data/public/spell_playtests/catalog.json'
    indexp = R / 'data/public/spell_playtests/authored_review_index.json'
    regp = R / 'data/director/spell_review/accepted_interface_registry_04.json'
    inventoryp = R / 'data/director/spell_review/ordinary_spell_inventory_03.json'
    mapping, catalog, index, registry, inventory = [read(p) for p in [mapp, catalogp, indexp, regp, inventoryp]]
    for p in [mapp, catalogp, indexp, regp, inventoryp,
              R / 'data/public/class_playtests/wizard.json', R / 'data/public/class_playtests/ranger.json',
              R / 'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md', R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
              R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R / 'docs/mechanics/CONDITIONS_PLAYTEST.md',
              R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md', R / 'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
              R / 'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md', R / 'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
              R / 'docs/mechanics/COOKING_RECIPE_PLAYTEST.md', R / 'docs/mechanics/FISHING_RECIPE_PLAYTEST.md',
              R / 'data/playtest/equipment_acquisition_candidate.json', R / 'data/playtest/crafting_engine_candidate.json',
              R / 'data/playtest/fishing_recipe_candidate.json', R / 'data/public/expedition_candidate/complete_candidate.json',
              R / 'data/public/expedition_candidate/transport_profiles.json', A / 'CODEX_EX58_X01_FULFILLMENT_RECEIPT.txt',
              R / 'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md']:
        bind(p)
    for ident in IDS:
        row = next(r for r in mapping['rows'] if r['id'] == ident)
        oldbinding = row['completeEarlierProposalRecords'][0]
        path = G / oldbinding['source']['path']
        ck('Exact original full file ' + ident, bind(path) == oldbinding['source'])
        document = read(path)
        record = at(document, oldbinding['recordPointer'])
        current = next(s for s in catalog['spells'] if s['id'] == ident)
        ix = next(e for e in index['entries'] if e['id'] == ident)
        ck('Complete procedure identity ' + ident, record['spellId'] == ident and bool(record['procedure']))
        ck('Exact source/access ' + ident, record['fullSourceAndCurrentAccessRecord'] == current)
        ck('Still pending ' + ident, ix['authoredStatus'] == 'pending-authored-procedure' and ident in {r['id'] for r in inventory['pending']})
        records.append({'spellId': ident, 'sourceReference': {'source': info(path), 'pointer': oldbinding['recordPointer']}, 'completeEarlierRecordUnchanged': deepcopy(record), 'completeCurrentCatalogSourceAndAccess': deepcopy(current), 'currentIndexEntry': deepcopy(ix), 'riskTier': 'B' if ident in ['control-water', 'magnetize-field'] else 'C', 'status': 'Original complete procedure read and preserved; no new operative rule authored.'})
        for i, text in enumerate(record['workedCases']):
            history.append({'spellId': ident, 'id': text.split(':', 1)[0], 'exactOriginalText': text, 'source': info(path), 'pointer': oldbinding['recordPointer'] + f'/workedCases/{i}'})
        if info(path)['path'] not in {s['source']['path'] for s in shared}:
            shared.append({'source': info(path), 'completeOriginalSharedProposalUnchanged': deepcopy(document['sharedProposal']), 'completeOriginalJointIssuesUnchanged': deepcopy(document['explicitJointIssues'])})
        for kind in ['catalog', 'core']:
            ck('Underlying ' + kind + ' ' + ident, bind(R / current['source'][kind + 'Path'])['sha256'] == current['source'][kind + 'Sha256'])
    interfaces = []
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 18, 36, 37, 39, 40]:
        entry = registry['entries'][i]
        b = entry['currentAuthoritativeSource']
        actual = bind(G / b['path'])
        ck('Current accepted authority ' + entry['name'], actual['bytes'] == b['bytes'] and actual['sha256'] == b['sha256'])
        interfaces.append({'registryPointer': f'/entries/{i}', 'completeEntryUnchanged': deepcopy(entry), 'scopeLimit': 'Only exact existing scope. Source-specific AC5/AC6/DE4 clauses do not become new global terrain/material/forced-placement permissions.'})
    counterparts = []
    for ident in ['create-water', 'shape-water', 'mending', 'earth-hand', 'mold-earth']:
        matches = [e for e in index['entries'] if e['id'] == ident and e['authoredStatus'] == 'reviewed-authored-operational-playtest']
        if not matches:
            continue
        e = matches[0]
        path = (indexp.parent / e['procedureFile']).resolve()
        doc = read(path)
        ptr = e.get('wholeCardPointer', e['procedurePointer'])
        counterparts.append({'spellId': ident, 'source': bind(path), 'wholeCardPointer': ptr, 'completeCurrentCard': deepcopy(at(doc, ptr)), 'completeSharedRules': deepcopy(doc.get('sharedRules', {})), 'indexEntry': deepcopy(e)})
    pendingcounterparts = []
    for path, label in [(R / 'data/director/spell_review/creation_conference_01.json', 'Creation source/economy design conference'), (R / 'data/director/spell_proposals/damage_control_25_current_08.json', 'Freezing Sphere corrected pending proposal')]:
        bind(path)
        doc = read(path)
        if label.startswith('Creation'):
            pendingcounterparts.append({'source': info(path), 'label': label, 'completeRecord': deepcopy(doc), 'status': 'UNSENT/UNADOPTED; no current authority inferred'})
        else:
            i, s = next((i, s) for i, s in enumerate(doc['spells']) if s['id'] == 'freezing-sphere')
            pendingcounterparts.append({'source': info(path), 'pointer': f'/spells/{i}', 'label': label, 'completeRecord': deepcopy(s), 'status': 'GPT source corrections locally applied to pending Current08; exact rebound09 unsubmitted, not adopted. No generic ice rule inferred.'})
    deltas = [
        ('control-water', 'Actual finite water identity, existing created-water lifetime/recipient limits, paid casting, ordinary movement, transport and Fishing work history.', 'Tenfootcube selectedwater/twentyfootcube region,perAction10ftdisplacement,water-supportlimit,STRswimmer/DEXhelmsman alternative and onefamilyattemptperround need currentconcurrence. Real immersion/breath/environment gaps must remain explicit.'),
        ('fabricate', 'Actual crafting access/formula/material/substitution/quality/yield/tool/assistant and physical-output rules; actual Ready and resource commitment.', 'OneAction500lb/tenfootcube mundane shaping/assembly exception; recipeeligibility, real assistantreadytiming, noXPbutfirst-successhistory, and full-order rollback/release. OriginalQ4DC12recipe is synthetic, not an approved actual product recipe.'),
        ('transmute-terrain', 'Actual body clearance, physicalstockidentity, ordinarymaterial/food/water/transport/sale handling, no donortrait or purification.', 'Fourmodes,60ftradius/topfoot,reference150/70/100/57densities and permanentvolume-preservingmasschange; occupiedbodyclearance and persistenticehazardphase map need actualdisposition. Compare pendingFreezingSphere onlywithin its ownscope.'),
        ('magnetize-field', 'Actual armor/itemmaterial, onebody identity, realforcedmovement/placement/anchors/weight and normalfalling.', '20ftsphere/pull,>halfmetalbodymass,armorholderbridge,Large/1000lbcaps,nearer-first deterministiccrowding,decliningSTRresistance and unattendedarmor handling. Examples require actualmaterial/mass/gearprofiles; no armor stripping.'),
        ('passwall', 'Actualconcentration,60secondclock,realopeningmovement,body/gearidentity,ordinarysuppression and nofreewallteleport.', '5x10x20tunnel,unseenexiteligibility,temporarywall-supportexception,nearestmouth bounded ejection,minimumclearanceconflict and fluidcapacity. Distinguish permanentlyended from suppressed-original-application states before allowing reopening.'),
        ('transmute-rock', 'Actual damage/save/Nullroots/falling,bodyclearance,materialinventory and later actualcrafting/supporthazards.', '20ftcube/interiorpermission,ordinaryworkedstoneeligibility,mass-changingstone/mudconversion,explicit4d6overheadburst/onceevent,damagefractioncarry,stockAC15versus ordinaryStone17,and finite linearHP partition. Actualceiling/supportscenario must exist.'),
        ('displace-structure', 'Actualbody/cargoweight,continuoussweptgeometry,realanchor/support and subsequent physicalstate; no inventedloot/repair.', '40x40x30/250000lb coherentbuilding,30ftpointpath/90degreerotation,foundation≤5ft/soil-exchangeexception,DEX5ftoccupantescape and simultaneous wholetransaction. Syntheticbuilding dimensions alone do not provide an actualstructure/soil/supportprofile.'),
        ('move-earth', 'Realconservedvolume/identity,ordinaryobjects/bodyclearance,fallingmarkers,environment/structurehazards require ownactualsources.', '40ftcube/8000cuft/30ftparcelmovement,materialeligibility/stableslopes,oneDEXescape/Prone/neutralreservation,wholetransitionfailure and bodyclearancevolumes. Currentcase needs completefinalsolidgeometry and actualslopes rather than a 1000cuftscalar alone.'),
    ]
    delta = [{'spellId': ident, 'sourcePreserved': True, 'inheritedInterfaces': inherit, 'genuineNewAuthorshipForConference': new, 'riskTier': next(r['riskTier'] for r in records if r['spellId'] == ident)} for ident, inherit, new in deltas]
    findings = [
        {'id': 'MT8-F01', 'classification': 'EXAMPLE ERROR / missing operative recipe', 'spells': ['fabricate'], 'finding': 'TU4-06-A deliberately uses a synthetic admittedQ4/DC12recipe andB an unnamedEnchantingorder. Those can compare conditionalframeworkarithmetic but cannot prove an existingmundaneproductmanufacture or realmagic-itemworkflow.', 'nextStep': 'Bind exact actual recipe/tool/worker/inputs/outputbody,or preserve each missing premise explicitly as conditional. Retain Q4/40lb/32lbproduct/8lbwaste obligation.'},
        {'id': 'MT8-F02', 'classification': 'OPEN DESIGN QUESTION', 'spells': ['fabricate'], 'finding': 'Assistants must use actual availableAction/ReadyReaction during one operation. Generic Ready is triggered after its trigger finishes, so an unspecified readiness arrangement cannot silently synchronize an assistant with an already-completed instantaneous manufacture.', 'nextStep': 'Confer on exact legal predeclared operation/trigger ordering or explicit local action contribution; do not invent a generic mid-cast interrupt.'},
        {'id': 'MT8-F03', 'classification': 'OPEN DESIGN QUESTION', 'spells': ['transmute-terrain', 'transmute-rock'], 'finding': 'Permanent equal-volume outputs change mass/composition,generate actualtransport/sale/water consequences,and need conservedoriginal-history plus occupiedbodyclearance. ExistingCreation/FreezingSphere are pending comparisons,not global permission.', 'nextStep': 'Give local density/conversion/provenance decisions and bodyescape/availablevolume fixtures before newoperativeauthorship.'},
        {'id': 'MT8-F04', 'classification': 'INTERFACE CONFLICT / pending special exception', 'spells': ['transmute-rock'], 'finding': 'Draft newsolidstockAC15differsfrom acceptedordinaryStoneAC17. LinearHPper100lb/splits also needs fullfinitefraction and zeroHP handling; existingdamagefraction cannot be reset by mud/rockcycling.', 'nextStep': 'Ask whether this is intentional source-specificauthorship or an example/defaultrepair; preserve the original proposal either way.'},
        {'id': 'MT8-F05', 'classification': 'OPEN DESIGN QUESTION', 'spells': ['passwall'], 'finding': 'The draft calls the spell ended at closure even though it also allows the same tunnel to reopen after temporary suppression. Suppressedapplication and finalendedapplication must not share an ambiguous resurrection path.', 'nextStep': 'Explicit state machine: operative,suppressedwithoriginaldeadline,pendingplacementandfinalended. Keep wholebody/gear/fluid identities and recordedexitclearance; no vanishedvolume.'},
        {'id': 'MT8-F06', 'classification': 'EXAMPLE ERROR / missing geometry', 'spells': ['displace-structure', 'move-earth', 'control-water'], 'finding': 'Currentoriginalvectors state aggregatevolumes/buildingbounds but not completebody/terrain/soil/swept/receivinggeometry. Rotationradius20at90degrees genuinelyexceeds30ft; that scalar does not settle alloccupants/footprints.', 'nextStep': 'Build actual coordinated finite fixtures,whole-path constraints and conservation ledgers. Realstructure/support records or unresolvedsyntheticconditional assumptions must be explicit.'},
        {'id': 'MT8-F07', 'classification': 'EXAMPLE ERROR / real damage source', 'spells': ['transmute-rock'], 'finding': 'The15bludgeoning4d6burst needs exact diefaces,saves,typeddefenses,tempHP,life/Wounds and originaldamage-root ownership. Ordinarylaterceilingcollapse is a separate genuinehazard,not arbitrarydensity-scaleddamage.', 'nextStep': 'Retain exactoriginal15→7 savehalving;use declared4d6faces summing15 and actualtargetHP/save/Nullhistory before fullcurrentvectors.'},
        {'id': 'MT8-F08', 'classification': 'EXAMPLE ERROR / source-qualified input', 'spells': ['magnetize-field', 'control-water'], 'finding': '800lbLargearmor,1400lbmetalbody,mooredboat,swimmer and actualhelmproficiency require real profiles/mass/contents where available. A genericbodylabel does not assert composition or a free anchorbreak.', 'nextStep': 'Bind namedreviewedequipment/transport/body sources; keep unavailablebestiaryorbreath/current premises conditional.'},
        {'id': 'MT8-F09', 'classification': 'OPEN DESIGN QUESTION', 'spells': ['transmute-terrain'], 'finding': 'Persistentmundaneice keeps originalspellDC and once-perregularcycle sliptrigger, but missing/ownerattachedphases and stablelot/split/reentry identity are not fully bound. FreezingSphere\'s current proposed mapping does not automatically apply.', 'nextStep': 'Ask for a local finite source-lifetime/cycle mapping and actualice/materialrules. No sixthFatepresentation or duplicateentry/STARTsave.'},
        {'id': 'MT8-F10', 'classification': 'STRUCTURAL ERROR / current review preparation', 'spells': IDS, 'finding': 'Historicalsharedexamples may have stale genericWizardDissonance and pending-interface labels. All16cases still need current realclass/source/resource/geometry expansion while exactoldtexts remain preserved.', 'nextStep': 'After sourceconference, build completecurrentvectors and exactmodel/player/directormanuscripts. Thisaudit doesnot claim currentprocedureacceptance or runtimeexecution.'},
    ]
    other_ids = set()
    for name in ['damage_control_25_current_08', 'persistent_damage_20_current_06', 'illusion_perception_14_current_11', 'control_15_current_11']:
        other_ids.update(s.get('id', s.get('spellId')) for s in read(R / f'data/director/spell_proposals/{name}.json')['spells'])
    other_ids.update(['woven-threads', 'haze-of-forgetting', 'creation'])
    ck('No overlap with77alreadyqueued', not set(IDS) & other_ids and len(other_ids) == 77)
    ck('Eightdistinctprocedures16originalcases', len(records) == len({r['spellId'] for r in records}) == 8 and len(history) == len({h['id'] for h in history}) == 16)
    ck('All8semanticdeltas', {d['spellId'] for d in delta} == set(IDS))
    root.mkdir()
    frozen = []
    for b in sources.values():
        ck('Currentfullsource ' + b['path'], info(G / b['path']) == b)
        p = root / 'sources' / b['path']
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((G / b['path']).read_bytes())
        ck('Exactfrozencopy ' + b['path'], info(p)['sha256'] == b['sha256'])
        frozen.append({**b, 'frozenCopy': p.relative_to(G).as_posix()})
    (root / 'MANIFEST.json').write_bytes(encoded({'sourceCount': len(frozen), 'sources': frozen, 'newRuleAdoptions': 0}))
    result = {'id': 'MATERIAL-TERRAIN-8-SOURCE-CONVERGENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'SOURCE_AND_INTERFACE_AUDIT_ONLY;8completeprocedures/16originalscenariosreadandpreserved;UNSENT/UNADOPTED;nosubstantialnewsystemicrulechosen.', 'developmentDirection': 'video-game-only', 'records': records, 'all16HistoricalScenarioTexts': history, 'completeOriginalSharedProposalsUnchanged': shared, 'currentAcceptedInterfaceComparisons': interfaces, 'completeAcceptedCounterparts': counterparts, 'completePendingCounterparts': pendingcounterparts, 'semanticDelta': delta, 'findings': findings, 'riskCounts': {'B': 2, 'C': 6}, 'sourceBindings': list(sources.values()), 'sourceManifest': info(root / 'MANIFEST.json'), 'nextRequiredWork': 'Create explicit sourceconference forks and current conditional/source-grounded casevectors;confer with actualGPT before choosing substantialmaterial/placement/production rules. Do not call thisaudit a completedconferencepacket.', 'countsUnchanged': {'reviewed': 480, 'pending': 368}, 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}
    out.write_bytes(encoded(result))
    report.write_bytes(encoded({'audit': info(out), 'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'sources': len(sources), 'fullOriginalProcedures': 8, 'originalCases': 16, 'placements': sum(len(r['completeCurrentCatalogSourceAndAccess']['source']['original']['placements']) for r in records), 'findings': len(findings), 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0}))
    print(json.dumps({'audit': info(out), 'checks': len(checks), 'sources': len(sources), 'originalProcedures': 8, 'originalCases': 16, 'findings': len(findings)}))


if __name__ == '__main__':
    main()
