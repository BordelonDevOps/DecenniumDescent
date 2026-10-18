"""Audit Creation's original proposal against actual material/economy interfaces."""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib, json, zipfile
from pathlib import Path
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(path):
    return json.loads(path.read_bytes())


def main():
    out = R / 'data/director/spell_review/creation_conference_01.json'
    root = A / 'creation-conference-01'
    archive = A / 'DD_Creation_Conference_01.zip'
    prep = A / 'CREATION_CONFERENCE_01_PREPARATION.json'
    requestpath = A / 'CREATION_CONFERENCE_01_REQUEST.txt'
    assert not any(p.exists() for p in [out, root, archive, prep, requestpath])
    checks, sources = [], {}

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def bind(path):
        binding = info(path)
        sources[binding['path']] = binding
        return binding

    oldpath = R / 'data/director/spell_proposals/enchantment_illusion_rank5.json'
    old = read(oldpath)
    original = old['records'][12]
    ck('Original Creation identity', original['spellId'] == 'creation')
    catalogpath = R / 'data/public/spell_playtests/catalog.json'
    catalog = read(catalogpath)
    ci, card = next((i, s) for i, s in enumerate(catalog['spells']) if s['id'] == 'creation')
    ck('All original source/access fields unchanged', original['fullSourceAndCurrentAccessRecord'] == card)
    indexpath = R / 'data/public/spell_playtests/authored_review_index.json'
    entry = next(e for e in read(indexpath)['entries'] if e['id'] == 'creation')
    ck('Creation still pending', entry['authoredStatus'] == 'pending-authored-procedure')
    for path in [oldpath, catalogpath, indexpath,
                 R / 'data/director/spell_review/accepted_interface_registry_04.json',
                 R / 'data/director/spell_review/remaining_spell_authoring_map_03.json',
                 R / 'data/playtest/equipment_acquisition_candidate.json',
                 R / 'data/playtest/crafting_engine_candidate.json',
                 R / 'data/playtest/cooking_recipe_candidate.json',
                 R / 'data/public/expedition_candidate/complete_candidate.json',
                 R / 'data/public/class_playtests/wizard.json',
                 R / 'data/public/class_playtests/warrior.json',
                 R / 'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',
                 R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
                 R / 'docs/mechanics/SPELL_INTEGRATION_RULES.md',
                 R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
                 R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
                 R / 'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
                 R / 'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',
                 R / 'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md',
                 R / 'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
                 R / 'docs/mechanics/COOKING_RECIPE_PLAYTEST.md',
                 R / 'docs/mechanics/COOKING_REVIEW_STATUS.json',
                 R / 'docs/mechanics/CRAFTING_ENGINE_REVIEW_STATUS.json',
                 R / 'docs/mechanics/expedition/EXPEDITION_PART01_PLAYER.md',
                 R / 'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md',
                 A / 'CODEX_EX58_X01_FULFILLMENT_RECEIPT.txt',
                 A / 'GPT_EQUIPMENT_EXACT_REVIEW.md',
                 A / 'GPT_COOKING_EXACT_REVIEW.md', Path(__file__)]:
        bind(path)
    for kind in ['catalog', 'core']:
        ck('Exact underlying ' + kind, bind(R / card['source'][kind + 'Path'])['sha256'] == card['source'][kind + 'Sha256'])
    registry = read(R / 'data/director/spell_review/accepted_interface_registry_04.json')
    interfaces = []
    for i in [0, 1, 3, 4, 7, 8, 13, 14, 36, 39, 40]:
        e = registry['entries'][i]
        source = e['currentAuthoritativeSource']
        binding = bind(G / source['path'])
        ck('Current interface hash ' + e['name'], binding['bytes'] == source['bytes'] and binding['sha256'] == source['sha256'])
        interfaces.append({'registryPointer': f'/entries/{i}', 'completeEntryUnchanged': deepcopy(e), 'scope': 'Existing interface only; no permanent-matter or economic production exception inferred.'})
    equip = read(R / 'data/playtest/equipment_acquisition_candidate.json')
    si, sword = next((i, s) for i, s in enumerate(equip['items']) if s['id'] == 'martial-melee-weapons.longsword')
    cook = read(R / 'data/playtest/cooking_recipe_candidate.json')
    ri, recipe = next((i, r) for i, r in enumerate(cook['cards']) if r['recipeId'] == 'recipe-90')
    vegetable = recipe['sourceRequirements']['components'][0]
    ck('Exact ingredient occurrence', vegetable['id'] == 'ing-90-0-vegetables' and vegetable['value'] == 2 and vegetable['weight'] == 0.1)
    examples = [{'id': text.split(':', 1)[0], 'exactOriginalText': text, 'source': bind(oldpath), 'pointer': f'/records/12/workedCases/{i}'} for i, text in enumerate(original['workedCases'])]
    findings = [
        {'id': 'CR1-F01', 'classification': 'OPEN DESIGN QUESTION', 'sourcePointer': '/records/12/procedure', 'finding': 'Permanent useful material,100lb/5ftcube/10gp caps and repeated paid production are earlier proposed authorship, not existing Creation acceptance. Their economic consequences need actual joint disposition.', 'nextStep': 'Confer before final operative text; do not disguise a finite creation exception as ordinary material conservation.'},
        {'id': 'CR1-F02', 'classification': 'EXAMPLE ERROR / missing eligible material evidence', 'caseId': 'IL5-06-A', 'finding': 'The14lb edible plant-food example names no exact composition,examined example,physical dimensions or material-value reference. Ordinary ration/meal prices do not establish wholly plant-derived composition.', 'nextStep': 'Retain the14lb/sevenfooddays/no56pintswater obligation conditionally until an actual qualifying ordinary material profile is bound or a new local profile is explicitly approved.'},
        {'id': 'CR1-F03', 'classification': 'INTERFACE CONFLICT / possible alias-value substitution', 'source': bind(R / 'data/playtest/cooking_recipe_candidate.json'), 'pointer': f'/cards/{ri}/sourceRequirements/components/0', 'finding': 'The actual recipe-90 Vegetables occurrence has weight0.1 and value2 per unit;14lb would require140units with stored value280. It cannot be merged with a cheaper same-named ingredient. This audit does not silently assume the currency of the generic value field; a bound unit conversion is needed before comparing it to Creation\'s10gp cap.', 'nextStep': 'Bind exact identity/form/tier/value units,or use a separately documented ordinary food profile. No automatic ingredient identity from the word vegetables.'},
        {'id': 'CR1-F04', 'classification': 'OPEN DESIGN QUESTION / source-specific durability', 'finding': 'Existing equipment assigns cloth/paper/ropeAC11 and woodAC15,with exact item-category HP. Earlier Creation assignsAC10to unprofiled soft plant stock and mass-based5/10/20HP. The latter is a proposed special rule,not the ordinary item table.', 'nextStep': 'Keep real finished item profiles. Decide whetherAC10is a narrow unprofiled-food/pulp exception or whether ordinary materialAC11 should govern matchingfiberstock; do not silently give every rope20HP.'},
        {'id': 'CR1-F05', 'classification': 'EXAMPLE ERROR / missing actual operation', 'caseId': 'IL5-06-B', 'finding': 'The8damage example has no attack source. Splitting80lbinto20/60does not by itself grant a free cutting action,tools,time or an independently reviewed salvage procedure.', 'nextStep': 'Use actual Warrior1/Sunder/longsword for8compatible damage. Preserve the proportional partition as a conditional arithmetic input until a genuinely legal physical cutting operation is supplied.'},
        {'id': 'CR1-F06', 'classification': 'OPEN DESIGN QUESTION / divided structural state', 'finding': 'Proportional max/currentHP and remainder-to-final-piece can generate zero-max pieces and depend on piece order. Arbitrarily small repeated splitting must not duplicate HP,mass,value,nutrition or create a repeatable repair-value loophole.', 'nextStep': 'Confer on deterministic recordedpieceorder,zeroHPphysicalmaterialandloss duringactualcutting. Repair retains its actualsource/material/time rules and cannot reconstruct consumed stock.'},
        {'id': 'CR1-F07', 'classification': 'INTERFACE INHERITANCE', 'finding': 'EX58 uses actual food2lb and water8pints per ordinarySmall/Mediumday plus distinct oil/sundries. Cooking counts actual qualifiedfoodmass,and exact componentidentity/tier/role/form remains required. Created food does not supply a wholeSupply or a monster donor.', 'nextStep': 'Inherit unchanged; decide only the new source\'s eligibility and materialgrant. Actual completed meals retain their own preparation,neutralization,boons,time,containers and freshness.'},
    ]
    questions = []

    def q(ident, promise, gap, a, b, recommendation):
        questions.append({'id': ident, 'classification': 'OPEN DESIGN QUESTION', 'risk': 'C', 'sourcePromise': promise, 'newDecision': gap, 'optionA': a, 'optionB': b, 'recommendedForConference': recommendation, 'scope': 'Creation only; no global crafting exception or cosmology conclusion.', 'status': 'UNSENT; no option adopted'})

    q('CR1-Q01', 'Create one nonliving object of vegetable matter; Action,60feet,Instantaneous.', 'Confirm permanent actual plant matter and finite scale.', 'Confirm prior100lb/5ftcube/10gpordinarymaterialreference caps,all simultaneously,and permanent ordinary output.', 'Keep permanentoutput but choose different explicit finitecaps with economic consequences and exact replacement examples.', 'A as a bounded starting candidate; request numerical balance disposition rather than hiding permanence or importing temporary mineral rules.')
    q('CR1-Q02', 'Vegetable matter supplies no exact composition list.', 'Define examined ordinary raw/processed plant stock,liquids,food,fuel and poison boundaries.', 'Confirm examined mundane plant-derived composition; explicitly bind actual edible/fuel/ingredient properties and containers. Exclude liveorganisms,monstertraits,unique/magicalreagents and unexamined chemicalcomposition.', 'Restrict Creation to raw solidplantstock;processedcloth,oil,foodandfinishedproductsrequire later realwork.', 'A preserving prior source-compatible breadth,with positive exact eligibility records and no false assumption that every botanical monsterpart qualifies.')
    q('CR1-Q03', 'The source creates an object and does not print manufacturingwork ortoolrequirements.', 'Decide one finished whollyplant-derived existingitem versus crude stock,and whether castingis an explicit production exception.', 'Confirm studiedpattern+actualprimarytoolproficiency for finished mundaneprofile;creationAction substitutes for its rawmaterial/manufacturingtime only,no stationcredential/magicrecipe/qualitybonus/tradeXP.', 'Permit only crude unworkedstock;all finisheditemsrequire actual ordinarycrafting.', 'A as explicitly NEW Creation-only permission; leave genuinely missing tool/pattern/materialprofile unresolved rather than invent it from a name.')
    q('CR1-Q04', 'No source structuralAC/HP is printed for a new stock lot.', 'Reconcile existingitemprofiles,proposedcrude-stockAC/HP,and finitezeroHPfragments.', 'Retain exactfinisheditemstats; author a narrow unprofiledstockfallback with explicitAC10vscloth11scope,massbands and physicalzeroHPmeaning.', 'Require everystock type to have an individuallyapproved objectprofile; no genericmass-baseddurability.', 'A only if complete boundaries are supplied; ordinary knownrope/cloth/wood profiles retain precedence. A zeroHPfragment must not become absentmatter or a newlyusableitem.')
    q('CR1-Q05', 'Created ordinarymatter may be divided or processed afterward.', 'Confirm HP/value/mass partition,cuttingloss and stable remainderorder without extra objects/repairfarming.', 'Conserve originalmax/currentHP,mass,composition,age and remainingvalue across actualpieces;choose stablepieceorder before rounding,allocate remainderdeterministically,and require an actual legal cutting operation.', 'Use physically individuatednewobjectprofiles only after a completed realcraftingorder,and retain an aggregate stockledger beforehand.', 'PreferA for simplephysicalpartitions,but ask GPT to address tinyfragments,zeroHP,number/orderofcuts,repair,and whether any knownsourceactually permits the examplecut.')
    q('CR1-Q06', 'Eligibleediblestock would be physicallyreal.', 'Supply an exact qualifying14lb plantfoodfixture,andsettle its genuinefoodgrade/freshness withoutassuming preservedrations.', 'Approve a narrowlydefined studiedordinaryplantfoodprofile with actualcomposition,mass,dimensions and justifiedreferencevalue≤10gp;inheritEX58nutritionandactualage.', 'Keep theoriginal14lb scenario conditional until an existing sourceprofile establishes all inputs; add a smaller fullybound qualifyingstockexample if available.', 'B until a reliable profile or explicit NEW local authorship is returned. Do not use the recipe-90 Vegetables identity at an inventedcheaperprice or confer magicalmealboons.')
    q('CR1-Q07', 'The source prints no one-object limit or once-per-day cap.', 'Repeatedpaidcreation affects supply,craftingandmarkets even with finite per-castcaps.', 'Allow each otherwiselegalpaidcast to generate its separate boundedordinarylot;real RP,Dissonance,Actions,rest limits,buyers,pricesandprovenance govern,with no guaranteedcash.', 'Add an explicitlyNEW source-specific cumulativeproduction or retained-stocklimit,quantifiedwithitslifecycleandrepresentativeeconomyfixtures.', 'A preserves the source and prior proposal. Request discussion of repeatedproduction consequences,not an unprinted globalmarketguarantee or magicalreagentconversion.')
    q('CR1-Q08', 'Instantaneous creation versus later mundane matter.', 'Confirm antimagic/dispel atcreation and afterward,andexact empty supportedplacement.', 'Inherit legalcast/counter/suppressioncheckpointandwhole-outputfit. Onceoperativecreationcompletes,theordinarymatterpersists through laterdispel/antimagic and realconsumption;blockedcreationrefundsno committedcost.', 'Treatcreatedstockasongoing magicalmatter with an explicitdurationsourceconflict and dispel/suppression/dispositionprocedure.', 'A,withtheactualaffectedoutput/placementcheckpoint specified. Nofoodretractionfromcreatures,nohiddensealed-containerplacementandno unsupportedfreefallattack.')

    caster = {'class': 'Wizard', 'level': 9, 'specialization': 'Abjuration', 'INT': 18, 'CON': 14, 'DEX': 14, 'PB': 4, 'HP': 56, 'spellDC': 16, 'preparedMatrix': 'creation', 'school': 'Illusion', 'rank': 5, 'actualAccess': deepcopy(card['classAccess']['Wizard']), 'RPBefore': 32, 'baseAndFinalCost': 10, 'RPAfter': 22, 'DissonanceBefore': 0, 'DissonanceAfter': 0, 'RefrainExtra': 0, 'otherRequirements': 'AvailableAction,reallegalArcaneFocus,usablevoice/hand/V/S/F,firstdistinctpreparedmatrix,nooptionalcost/qualitymodifier.'}
    vectors = [
        {'id': 'IL5-06-A', 'originalTextUnchanged': examples[0]['exactOriginalText'], 'status': 'CONDITIONAL until actual qualifying foodprofile and jointCreationrule are established.', 'sourceActor': deepcopy(caster), 'requiredRealInput': 'One actuallyexamined,ordinary,nonliving,whollyplant-derivedediblelot;actualmaterialcompositionandreferencevalue≤10gp remainunbound. No claim thatgenericrationsorrecipe-90Vegetablesautomaticallyqualify.', 'proposedCaseGeometry': {'casterCenter': [0, 0, 1], 'outputBoxMin': [20, 0, 0], 'outputBoxMax': [22, 1, 1], 'volumeCubicFeet': 2, 'massLb': 14, 'floorSupportsWholeOutput': True, 'placementPerceivedUnoccupiedAndUnobstructed': True, 'note': 'Dimensionsare a declaredsyntheticcasepremise,notanexistingfoodprofileornewmaterialdensitygrant.'}, 'conditionalArithmetic': {'foodMassLb': 14, 'ordinarySmallMediumFoodDemandLb': 2, 'fullFoodDays': 7, 'waterStillNeededPints': 56, 'waterCreatedPints': 0, 'wholeSupplyBasketsCreated': 0, 'foodRemainingAfterSevenActual2lbConsumptions': 0, 'sameFoodAvailableToLaterRecipeLb': 0}, 'actualLedgerBoundary': 'Consumptionmustactuallyoccuratitsordinarytimeandlawfulfoodgrade;thereisnosimultaneousspell-fedsevenpersonbenefit,nofoodboon,noautomaticmealpackagingor30daypreservation. The originalprovisioningobligationremainsintact.'},
        {'id': 'IL5-06-B', 'originalTextUnchanged': examples[1]['exactOriginalText'], 'status': 'CONDITIONAL stock/partition trace; actual damage source is fully bound but stockvalueandphysicalcutpermission remainexplicit.', 'sourceActor': deepcopy(caster), 'stock': {'massLb': 80, 'boxMin': [20, 0, 0], 'boxMax': [24, 1, 0.5], 'volumeCubicFeet': 2, 'ACIfProposalAdopted': 15, 'maximumHPIfProposalAdopted': 20, 'initialCurrentHP': 20, 'referenceMaterialValue': 'Not assigned; genuineundamagedreference≤10gpisrequired.', 'physicalSupportPerceptionAndLoE': 'Clearunoccupiedfloorwithin60ft,realexaminedordinaryhardwoodcomposition.'}, 'actualDamageSource': {'class': 'Warrior', 'level': 1, 'STR': 16, 'PB': 2, 'weapon': {'source': bind(R / 'data/playtest/equipment_acquisition_candidate.json'), 'pointer': f'/items/{si}', 'completeItem': deepcopy(sword)}, 'position': [19, 0, 1], 'bodyHalfExtents': [1, 1, 1], 'ownership': 'AnactualownedandheldStandardlongswordisadeclaredstartingfixture;martialproficiencygrantsnofreeweapon.', 'operation': 'AvailableAttackAction,onelegalSunderattackagainstperceivedreachableunattendedhardwood;ordinarycompatiblephysicalslashing,nooptionalclasshook.', 'attackFace': 12, 'attackModifier': 5, 'attackTotal': 17, 'damageD8Face': 5, 'STRDamage': 3, 'damageTotal': 8, 'currentHPAfter': 12}, 'conditionalPartition': {'actualCutNotSuppliedBySpell': True, 'requestedPlaneX': 21, 'piecesMassLb': [20, 60], 'maximumHP': [5, 15], 'currentHP': [3, 9], 'unchangedTotals': {'massLb': 80, 'maximumHP': 20, 'currentHP': 12}, 'limitations': 'Thepartitionassumesagenuinelylegalcompletedphysicalcutpreservingthesestatedamounts;nodamagefreecuttingAction,zero-timecrafting,salvagerecoveryornewstockvalueisgranted. Prior8damagebyitselfdoesnotestablishthatcut.'}, 'postCreationDispel': 'IfQ01/Q08Aareapproved,laterordinarydispeldoesnotdeleteordinaryexistingstock. No actualnewdispelcastiscostlesslyinventedbythiscomparison.'},
    ]
    ck('Original two IDs and order', [v['id'] for v in vectors] == [e['id'] for e in examples] == ['IL5-06-A', 'IL5-06-B'])
    ck('Food accounting', 14 // 2 == 7 and 7 * 8 == 56 and 14 - 7 * 2 == 0)
    ck('Exact vegetable identity arithmetic', Fraction(14) / Fraction(str(vegetable['weight'])) == 140 and 140 * vegetable['value'] == 280)
    ck('Stock fits fivefootcube/mass', 4 <= 5 and 1 <= 5 and Fraction(1, 2) <= 5 and 4 * 1 * Fraction(1, 2) == 2 and 80 <= 100)
    ck('Actual source8damage', sword['sourceFields']['Damage'] == '1d8 slashing' and 12 + 2 + 3 == 17 and 17 >= 15 and 5 + 3 == 8 and 20 - 8 == 12)
    ck('Mass/max/current conservation', 20 + 60 == 80 and 5 + 15 == 20 and 3 + 9 == 12 and Fraction(20, 80) * 20 == 5 and Fraction(20, 80) * 12 == 3)
    wizard = read(R / 'data/public/class_playtests/wizard.json')
    ck('Actual Wizard9resource/access', wizard['rpByClassLevel'][8] == 32 and wizard['maxSpellRankByClassLevel'][8] == 5 and card['classAccess']['Wizard']['minimumClassLevel'] == 9 and 32 - 10 == 22)
    ck('EX58 corrected current completecandidate', info(R / 'data/public/expedition_candidate/complete_candidate.json')['sha256'] == '6de5f36fad4f06da655d9806e04b958d647aee22f58cd4b519fdc5706737c5af')
    for b in sources.values():
        ck('Full current source ' + b['path'], info(G / b['path']) == b)
    result = {'id': 'CREATION-DESIGN-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'UNSENT / UNADOPTED. Source audit and substantive economic conference; no new systemic material rule chosen.', 'developmentDirection': 'video-game-only', 'riskTier': 'C', 'sourceReference': {'source': bind(oldpath), 'pointer': '/records/12'}, 'completeEarlierRecordUnchanged': deepcopy(original), 'completeOriginalSharedProposalUnchanged': deepcopy(old['sharedProposal']), 'completeOriginalJointIssuesUnchanged': deepcopy(old['explicitJointIssues']), 'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'catalogPointer': f'/spells/{ci}', 'currentIndexEntryUnchanged': deepcopy(entry), 'originalExamplesUnchanged': examples, 'conditionalConferenceVectors': vectors, 'currentAcceptedInterfaceComparisons': interfaces, 'actualCookingIngredientComparison': {'source': bind(R / 'data/playtest/cooking_recipe_candidate.json'), 'pointer': f'/cards/{ri}/sourceRequirements/components/0', 'completeRecord': deepcopy(vegetable), 'fullRecipePreservedInSource': True, 'comparisonScope': 'Exactidentity/value/weightinput;nosubstitution,creationeligibilityorrecipeoutputgrant.'}, 'findings': findings, 'questions': questions, 'sourceBindings': list(sources.values()), 'historyPolicy': 'Alloriginalsourcesandscenariosremainunchanged. CurrenttracesareconditionalandactualpreparedWizardD0overridesstalehistoricalgenericexampleD+1. NeitherthisauditnoritsarchivemarksCreationreviewed.', 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}
    out.write_bytes(encoded(result))
    sources[info(out)['path']] = info(out)
    root.mkdir()
    frozen = []
    for b in sources.values():
        p = root / 'sources' / b['path']
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((G / b['path']).read_bytes())
        assert info(p)['sha256'] == b['sha256']
        frozen.append({**b, 'archivePath': 'sources/' + b['path']})
    (root / 'MANIFEST.json').write_bytes(encoded({'candidate': info(out), 'sources': frozen, 'sourceCount': len(frozen), 'originalProcedures': 1, 'originalCases': 2, 'conditionalTraces': 2, 'questions': len(questions), 'newRuleAdoptions': 0}))
    (root / 'LOCAL_PREFLIGHT.json').write_bytes(encoded({'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'scope': 'Source/access/preservation and arithmetic only. Conditional materialvalue/cutpermissions remain unresolved.', 'runtimeTestsExecuted': 0}))
    (root / 'README.md').write_text('Creation is a separate systemic material/economy conference. Read the complete original procedure, two original scenarios, two explicitly conditional current traces, seven findings and eight questions. The complete exact source and interface files are included. Resolve every new decision explicitly before operative authorship. Do not silently approve missingfoodcomposition/value,cuttingactions,permanentmatterlimits or createdingredientidentity. Return exactcompletecorrections,questiondispositions,currentpointerevidence and boundedreviewverdict. Existing crafting,equipment,EX58 and Cooking mechanics keep their own written scope; historical pendinglabels in componentrecords do not override the preserved exactfulfillmentreceipt. This packet grants no runtime,selection,balance,cosmology or whole-gameapproval.\n', encoding='utf-8')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(frozen) + 3
        for b in frozen:
            raw = z.read(b['archivePath'])
            assert len(raw) == b['bytes'] and hashlib.sha256(raw).hexdigest() == b['sha256']
    b = info(archive)
    requestpath.write_text(f'Please confer on Creation using DD_Creation_Conference_01.zip ({b["bytes"]} bytes; SHA-256 {b["sha256"]}). This video-game-only systemic material/economy conference preserves the complete prior proposal, exact source/access, two original cases and two conditional current traces, with {len(frozen)} full verified files. Dispose of all eight questions and seven findings, especially permanent bounded material, exact edible/ingredient/value eligibility, finished-item tool gates, crude-stock durability, real cutting/partition operations, repeated production and actual antimagic/dispel scope. Do not treat a conditional14lbfoodprofile or freecut as established. Return a downloadable verified review archive with exact complete before/after corrections and current source pointers. No adoption, runtime, balance or cosmology approval is requested.\n', encoding='utf-8')
    prep.write_bytes(encoded({'candidate': info(out), 'archive': b, 'manifest': info(root / 'MANIFEST.json'), 'checkReport': info(root / 'LOCAL_PREFLIGHT.json'), 'request': info(requestpath), 'sourceCount': len(frozen), 'checkCount': len(checks), 'findings': len(findings), 'questions': len(questions), 'submitted': False, 'adopted': False, 'allArchiveSourceHashesVerified': True}))
    print(json.dumps({'candidate': info(out), 'archive': b, 'fullSources': len(frozen), 'checks': len(checks), 'questions': len(questions), 'findings': len(findings)}))


if __name__ == '__main__':
    main()
