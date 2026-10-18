"""Prepare genuine design forks for eight material/terrain spells before new rules."""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import hashlib, json, math, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    ap = R / 'data/director/spell_review/material_terrain_8_source_convergence_01.json'
    out = R / 'data/director/spell_review/material_terrain_8_conference_01.json'
    root = A / 'material-terrain8-conference-01'
    archive = A / 'DD_Material_Terrain_8_Conference_01.zip'
    prep = A / 'MATERIAL_TERRAIN_8_CONFERENCE_01_PREPARATION.json'
    requestp = A / 'MATERIAL_TERRAIN_8_CONFERENCE_01_REQUEST.txt'
    assert not any(p.exists() for p in [out, root, archive, prep, requestp])
    audit = read(ap)
    sources = {b['path']: b for b in audit['sourceBindings']}
    checks, questions = [], []

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def bind(p):
        b = info(p)
        sources[b['path']] = b
        return b

    for p in [ap, A / 'MATERIAL_TERRAIN_8_SOURCE_CHECK_01.json', Path(__file__)]:
        bind(p)
    records = audit['records']
    by_id = {r['spellId']: r for r in records}
    wizard = read(R / 'data/public/class_playtests/wizard.json')

    def q(n, ids, promise, gap, option_a, option_b, recommendation, inherited):
        questions.append({'id': f'MT8-Q{n:02}', 'spells': ids, 'classification': 'OPEN DESIGN QUESTION',
                          'sourcePromise': promise, 'gap': gap, 'optionA': option_a, 'optionB': option_b,
                          'recommendedForConference': recommendation, 'acceptedInterfaceInherited': inherited,
                          'scope': 'Named spells only; no global physics, production or relocation rule.',
                          'sourcePointers': [by_id[ident]['sourceReference'] for ident in ids],
                          'status': 'UNSENT; no option adopted'})

    q(1, ['control-water'], 'Raise, lower, or redirect water; exact Core casting source is preserved in the full record.',
      'Confirm finite water volume, operating region, subsequent Action and real support/flow.',
      'Keep the original selected contiguous ten-foot-cube quantity, fixed twenty-foot-cube region and ten-foot displacement/raise/lower limit per actual control Action, preserving real water identity and any original magical expiry.',
      'Use a different explicitly quantified source-local volume/region/displacement model with full counterexamples; no unlimited water supply or subjective strength.',
      'A preserves the complete prior proposal, conditional on exact body/receiving-space constraints. Clarify whether any initial manipulation is included in casting or needs its separate Action.',
      'Ordinary paid casting, real material ownership, concentration and no free Supply remain inherited.')
    q(2, ['control-water'], 'Redirecting real water can move bodies, but the source does not print a complete swimmer/boat model.',
      'Choose the existing proposed STR swimmer / trained actual DEX helmsman alternative and once-per-target-per-numbered-round cap.',
      'Retain that bounded displacement rule, require actual flotation/boat/helm eligibility and legal full-body path, stop at fixed anchors and obstacles, and do not grant drowning or anchor-breaking damage.',
      'Move water only; creature/boat displacement requires a separately established physical current/buoyancy interface, leaving this source unable to infer a new forced-movement rule.',
      'A as explicit local authorship, with missing actual transport/breath premises still conditional. A second paid Action does not bypass the proposed cap.',
      'Existing actual movement, anchors, Falling and transport ownership remain unchanged.')
    q(3, ['fabricate'], 'Transform raw materials into finished items; two placements remain Transmutation and Universal.',
      'Define precisely which real work an Action replaces and how actual quality, output and history are recorded.',
      'Retain one preregistered eligible mundane shaping/assembly order within500lb/ten-foot-cube: actual formula, proficiency, tool/station, materials, substitutions and yield remain; replace only active manufacturing work with the spell Action, not growth/chemical/magical waits; no tradeXP, but retain actual first-success history.',
      'Limit to one actual mundane item profile rather than a recipe batch; ordinary recipe work/quality checks remain outside the cast, with the narrower exception fully specified.',
      'A preserves the stated source breadth and original Q4 batch obligation. Decide first-success history explicitly so later ordinary work cannot farm it.',
      'Current crafting credentials, stock identity, real recipe quality and payments are inherited, not reopened.')
    q(4, ['fabricate'], 'The spell does not print an assistant timing exception.',
      'Generic Ready resolves after its observed trigger; it cannot retroactively contribute to a completed instantaneous manufacture.',
      'Allow an explicit Fabricate-only assistant commitment during declared setup, with real available contribution Action/Reaction, observable trigger and exact ordering before output resolution.',
      'No assistant contribution to this one-Action manufacture; inherited ordinary recipe assistance remains available only when its actual timing can occur lawfully.',
      'B unless GPT identifies an already lawful source ordering. Do not create a generic mid-cast Ready interrupt or a free assistant Action.',
      'Accepted Ready commitments, release, expiry and real action wallets remain unchanged.')
    q(5, ['transmute-terrain', 'transmute-rock'], 'Swamp/stone and sand/ice terrain changes; rock-to-mud or mud-to-rock transformation.',
      'Confirm permanent composition changes conserving selected volume while changing mass, with exact local density defaults.',
      'Retain ordinary densities stone150, swamp/mud70, sand100, ice57lb/cu.ft, equal selected volume, finite original stock identity, retained contamination/claims/damage, no new precious or donor properties, and real later transport/market consequences.',
      'Require actual source/material densities per content profile; preserve volume but leave unprofiled conversion unresolved instead of granting those universal numeric defaults.',
      'A only as explicit defaults for these two spells, with material/source eligibility and actual consequences disclosed. This does not establish universal scientific density or clean drinking water.',
      'Real inventory/ownership, consumption, transport, actual recipe eligibility and no double stock are inherited.')
    q(6, ['transmute-terrain'], 'The source promises a full60-foot-radius terrain change, including swamp-to-stone and sand-to-ice.',
      'Finish four finite modes, top-foot selection, excluded living/structural matter, body clearance and surface-height reference.',
      'Retain the four original named reciprocal modes and eligible exposed top foot inside a sixty-foot-radius disk, excluding living roots, bodies and actual structures; explicitly define occupied-body/clearance subtraction and connected trapped-space handling before conversion.',
      'Retain the same area and top-foot limit but reject each connected selected component whose conversion would obstruct required whole-body escape/clearance, leaving that component unchanged.',
      'Ask for an explicit local completion against both examples; do not adopt pending Freezing Sphere clearance by analogy or silently petrify a recipient.',
      'Actual body occupancy, perception/line of effect and paid hidden failure remain inherited.')
    q(7, ['transmute-terrain'], 'Sand-to-ice creates persistent real terrain; the prior draft gives a spell-DC slip hazard.',
      'Define finite slip event history, schedules and stable material identity after splits/merges and caster removal.',
      'Keep local first-entry/regular-START slip with one opportunity per original regular six-second cycle, exact source DC and stable original lot; specify owner-attached/no-phase schedule, contact geometry and actual expiry by ice loss.',
      'Use only a separately approved ordinary ice terrain profile; no ongoing spell-DC hazard survives the instantaneous conversion.',
      'A preserves the pending source proposal, but requires full deterministic local text. Current pending Freezing Sphere is a comparison only, not the deciding authority.',
      'Actual saves, native Prone, no extra turn and current Fate disclosure gates are inherited.')
    q(8, ['magnetize-field'], 'All metal creatures/armor are pulled to a center; STR save to resist.',
      'Choose the proposed 20-foot sphere/pull, Large/1000lb cap, metal-body definition and armor-to-wearer bridge.',
      'Retain those exact local limits; more than half actual body mass must be metal for the body route, or actual worn metal armor carries the whole wearer once; unattended armor moves without save, coin-purse possession alone does not qualify.',
      'Remove the invented size/mass and body-percentage caps and author a different finite source-faithful definition with explicit path/anchor/crowding limits.',
      'A as an explicit bounded proposal, including consequences for the preserved800lb and1400lb scenarios; never infer material composition from a creature name.',
      'Real body identity, actual gear, forced movement, ordinary collision and source-qualified saves remain inherited.')
    q(9, ['magnetize-field'], 'Multiple actual subjects can be pulled toward one center.',
      'Resolve simultaneous path conflicts and point/body reference without extra armor saves or collision damage.',
      'Retain nearer-subject-first then stable-ID ordering and stop each full body at the first blocker; define exact body reference and center-contact stop, preserving declared initial membership and one movement per subject.',
      'Use a simultaneous swept-volume solve with deterministic conflict truncation, fully specified before hidden outcomes.',
      'A is the existing proposal and simpler to audit in software. Specify exact distance/stop metric rather than assume center distance is the accepted range rule.',
      'One physical body and full-body collision are inherited; the group ordering is new local authorship.')
    q(10, ['passwall'], 'Create an actual passage through a wall.',
      'Confirm maximum5×10×20foot tunnel, ordinary material scope, required second side and temporary support.',
      'Retain original finite tunnel, hidden actual wall thickness check and real opening; give only the explicit temporary structural-support exception while operative, with no portal, excavated stock or thickness readout.',
      'Permit a blind recess without a second opening, with separately defined endpoint/closure behavior and no guessed safe far side.',
      'A retains the original through-wall obligation and paid failure for an unknown25ft wall. Do not alter the source into teleportation.',
      'Actual movement, collision, perception, no refund and source concentration remain inherited.')
    q(11, ['passwall'], 'A temporary passage closes, potentially containing real bodies, cargo and fluid.',
      'Separate operative, suppressed, pending-placement and permanently ended states; settle bounded ejection.',
      'Retain nearest reachable mouth/exterior ejection within the original bounded20ft route plus legal adjacent space; record finite local clearance conflict when neither exit can receive a body. Suppression keeps the original live application/deadline distinct from final ending; no new entrants use a closing conflict corridor.',
      'Use strictly adjacent-only mandatory placement, and reject any proposed tunnel that cannot guarantee that limited ending placement.',
      'A preserves the prior bounded-ejection intent, but ask GPT for complete body/cargo/fluid and suppressed-to-operative transition text. No arbitrary distant safe room or volume deletion.',
      'Accepted placement rules remain source-scoped; this proposed exception is local and needs concurrence.')
    q(12, ['transmute-rock'], 'Transform rock to mud or vice versa.',
      'Reconcile20ftcube/8000cu.ft selection including connected unseen interior, solid AC and damage-fraction carry.',
      'Retain the finite selection and explicit interior exception; use ordinary known stone AC17 rather than the draft unqualified AC15, and complete finite mass-based HP/partition/damage-fraction tracking as local authorship.',
      'Keep draftAC15 as an explicitly named source-specific created-stone exception, with complete linearHP/partition and damage-fraction behavior.',
      'A resolves the known ordinary-material mismatch unless GPT justifies a genuine distinct stone profile. Exact HP scaling, zeroHP material and conversion cycling still require disposition.',
      'Current actual object/gear damage, stock identity and later repair-source requirements are inherited.')
    q(13, ['transmute-rock'], 'Rock-to-mud can remove support; no complete burst model is printed.',
      'Confer on the proposed local4d6 overhead burst versus actual later structural collapse.',
      'Retain one4d6 bludgeoning burst with DEX half for the exact selected unsupported overhead section within20ft, actual area/LoE, one original source root and no density scaling; separate any genuinely sourced later collapse.',
      'Use only ordinary existing support/Falling/hazard procedures and supply no new spell burst.',
      'A retains the original15→7 scenario as explicit new authorship; specify geometry and which subjects qualify. No invented building-collapse damage follows from mass alone.',
      'Actual typed defenses, Null dealer provenance, Wounds, death and Falling remain unchanged.')
    q(14, ['displace-structure'], 'Move or rotate a building or structure up to30feet.',
      'Confirm finite coherent building bounds, continuous path and foundation/soil exchange exception.',
      'Retain40×40×30feet/250000lb, at most90degrees, each point actual path≤30ft, real occupants/contents, whole swept clearance and actual support; explicit≤5ft foundation/soil-exchange exception conserves soil and ownership.',
      'Require entirely detached structures and pre-cleared supported receiving space, without foundation displacement or soil exchange.',
      'A retains the proposed breadth, with exact atomically validated solid/soil geometry; no repair, loot generation or automatic crushing. A20ft-radius corner cannot rotate90degrees under30ft arc limit.',
      'Body/gear identity, source custody, real support, cost commitment and ordinary later hazards are inherited.')
    q(15, ['displace-structure', 'move-earth'], 'Physical terrain/structure movement can carry occupants.',
      'Decide proposed DEX5ft escape, failed-save carry/Prone, and indivisible transitions when bodies cannot fit.',
      'Retain one actual DEX escape opportunity with a real reachable safe5ft route, no invented free action elsewhere; failed Move Earth carry adds only stated Prone; any whole transition with illegal final/swept bodies or impossible volume fails under exact commitment/hidden-eligibility rules.',
      'Remove the new escape/save rider and permit transformations only when every occupied body already has a legal unchanged or voluntarily accepted displacement route.',
      'A preserves all original scenario obligations, requiring clear ordering and no duplicate relocation or body-volume reservation. Displace Structure does not inherit Move Earth Prone unless expressly chosen.',
      'Actual saves, real body collision, no refund on hidden failure, and native Falling remain unchanged.')
    q(16, ['move-earth'], 'Reshape terrain dramatically.',
      'Confirm finite40ftcube/8000cu.ft/30ft-per-parcel movement and actual stable final slopes.',
      'Retain these limits, conserved actual loose substrate and whole continuously valid transformation; explicit final geometry and real material slope/support predicates are required before resolving.',
      'Use a different quantified local shaping volume/displacement model with its actual permitted shape and support defaults supplied.',
      'A preserves the original1000cu.ft and200cu.ft cavity failure. Do not assume a scalar volume proves a stable berm or that excess800cu.ft disappears.',
      'Real material identity, actual containers/receiving capacity and no compressed commodity conversion are inherited.')

    # These traces discuss the alternatives. They do not certify a not-yet-authored rule.
    vectors = []
    def v(case_id, ids, initial, operation, expected, gaps):
        original = next(h for h in audit['all16HistoricalScenarioTexts'] if h['id'] == case_id)
        ident = original['spellId']
        access = by_id[ident]['completeCurrentCatalogSourceAndAccess']['classAccess']['Wizard']
        level, rank, cost = access['minimumClassLevel'], access['rank'], access['baseRpCost']
        pb = 2 + (level - 1) // 4
        actor = {'class': 'Wizard', 'level': level, 'specialization': 'Abjuration', 'INT': 18, 'CON': 14, 'DEX': 14,
                 'PB': pb, 'normalHP': 8 + 6 * (level - 1), 'spellDC': 8 + pb + 4,
                 'preparedMatrix': ident, 'generatingRank': rank, 'actualAccess': deepcopy(access),
                 'RPBefore': wizard['rpByClassLevel'][level - 1], 'baseAndFinalCost': cost,
                 'RPAfter': wizard['rpByClassLevel'][level - 1] - cost,
                 'DissonanceBefore': 0, 'DissonanceAfter': 0, 'RefrainExtra': 0,
                 'ordinaryRequirements': 'Actually learned at a legal level-up choice, prepared, first distinct matrix this encounter; actual owned legal focus, usable voice/hands, available Action, no optional cost/geometry modification, no armor surcharge, no existing concentration unless expressly stated.'}
        vectors.append({'id': case_id, 'spellId': ident, 'originalTextUnchanged': original['exactOriginalText'],
                        'originalSource': {'source': original['source'], 'pointer': original['pointer']},
                        'sourceActor': actor, 'questionIds': ids, 'initialState': initial, 'operation': operation,
                        'expectedIfNamedProposalAgreed': expected, 'unresolvedPremises': gaps,
                        'status': 'Conditional design-conference vector; not current operative acceptance or runtime execution.'})
        ck('Actual Wizard access/rank: ' + case_id, wizard['maxSpellRankByClassLevel'][level - 1] >= rank)
        ck('Actual RP/DC/HP: ' + case_id, actor['RPAfter'] >= 0 and actor['spellDC'] == 8 + pb + 4 and actor['normalHP'] == 6 + 2 + (level - 1) * (4 + 2))

    v('TU4-05-A', ['MT8-Q01'], {'casterCenter': [0, 0, 1], 'regionMin': [10, -10, -2], 'regionMax': [30, 10, 18], 'waterBoxMin': [10, -5, 0], 'waterBoxMax': [12, 5, 10], 'quantityCuFt': 200, 'receivingBoxMin': [20, -5, 0], 'receivingBoxMax': [22, 5, 10], 'actualWater': 'One already present ordinary unowned-or-lawfully-controlled water lot; no magical expiry or consumption is invented.'}, 'Cast the selected water/region at t0. On a later real regular turn with live concentration, spend the separately available Action to redirect all parcels by[10,0,0]; actual route and channel capacity must permit it.', {'sourceLotRemainingCuFt': 0, 'destinationSameLotCuFt': 200, 'parcelDistanceFt': 10, 'abstractSupplyAdded': 0, 'afterConcentration': 'The same actual200cu.ft remains subject to real gravity, receiving structure and flow.'}, 'The coordinates are declared test geometry. Container walls, actual open route, water support during movement and capacity after release need actual authored physical fixtures; these boxes alone do not prove them.')
    v('TU4-05-B', ['MT8-Q02'], {'recipient': 'Actual unarmored Wizard1, STR10, untrained STR save+0; normalHP8, no Wounds, tempHP0, capable and actually swimming in the selected water.', 'save': {'face': 10, 'modifier': 0, 'total': 10, 'DC': 15}, 'declaredPath': {'centerFrom': [15, 0, 1], 'centerTo': [25, 0, 1], 'bodyHalfExtents': [1, 1, 1]}, 'boat': 'A distinct real moored boat remains a conditional transport fixture; no guessed boat mass, helm proficiency or anchor strength.'}, 'Use a genuinely available control Action during the continuing source. A second Action in the same numbered round is only compared if independently supplied by an actual source; none is granted here.', {'failedSave': True, 'oneLegalPathDistanceFt': 10, 'secondAttemptSameFamilyRoundAllowed': False, 'anchorBroken': False}, 'Actual swimmer immersion/current/breath and boat profiles are not established by this vector. It grants no second Action or damage.')
    v('TU4-06-A', ['MT8-Q03', 'MT8-Q04'], {'recipe': 'Original explicitly synthetic admitted mundane Q4/DC12 recipe, not an approved actual product.', 'inputLb': 40, 'outputCount': 4, 'eachOutputLb': 8, 'wasteLb': 8, 'checkTotal': 12, 'stockAndOutputs': 'All actual stock and finished bodies must fit the ten-foot cube and500lb cap; no dimensions are inferred from mass.'}, 'One paid Fabricate Action under the proposed exception; no assistant is supplied.', {'checkMeetsDC': True, 'outputTotalLb': 32, 'wasteLb': 8, 'totalConservedLb': 40, 'tradeXP': 0, 'ordinaryWorkHoursInvented': 0}, 'Full recipe ID/formula/tool/station/skill modifier/face, ingredients, output geometry and actual first-success record remain required. Total12 alone is not a sourced four-degree task roll.')
    v('TU4-06-B', ['MT8-Q03'], {'mundaneOrder': 'Separate actual mundane sword recipe and raw stocks required.', 'enchantingOrder': 'Actual source Enchanting order and magical process inputs required; no named order is invented.'}, 'Evaluate Fabricate only against its proposed mundane shaping/assembly scope.', {'enchantmentCompletedByFabricate': False, 'magicalProcessInputsWaived': False, 'laterActualEnchantingWorkStillRequired': True}, 'The original two unnamed orders remain conditional. An actual ordinary sword equipment profile is not by itself a complete manufacture recipe or Enchanting credential.')
    v('TR5-01-A', ['MT8-Q05', 'MT8-Q06', 'MT8-Q07'], {'casterCenter': [0, 0, 1], 'diskCenter': [20, 0, 0], 'radiusFt': 60, 'selectedSandBoxMin': [20, 0, -1], 'selectedSandBoxMax': [25, 4, 0], 'selectedCuFt': 20, 'sandDensityIfApproved': 100, 'iceDensityIfApproved': 57}, 'Convert the one exposed ordinary eligible patch to ice if all actual clearance and selection requirements are met.', {'volumeBeforeAndAfterCuFt': 20, 'massBeforeLb': 2000, 'massAfterLb': 1140, 'oldSeparateSandRemainingCuFt': 0, 'cleanWaterCertificationGranted': False}, 'Material density defaults, exact occupied-volume handling, local ice durability/support/slip and later melting remain the explicit questions. No unseen parallel stock or later melt Action is invented.')
    v('TR5-01-B', ['MT8-Q05', 'MT8-Q06'], {'casterCenter': [0, 0, 1], 'diskCenter': [20, 0, 0], 'terrainBoxMin': [10, -5, -1], 'terrainBoxMax': [30, 5, 0], 'excludedObjects': 'Actual living roots, a built bridge and occupied creature volumes are supplied as exclusion classes, not newly generated objects.'}, 'Attempt swamp-to-stone within the exposed top foot, subject to the chosen clearance rule.', {'livingRootsConverted': False, 'bridgeConverted': False, 'creatureVolumeFilled': False, 'finishedMasonryCreated': False, 'oldAndNewStockSeparatelySaleable': False}, 'Exact root/bridge/body collision meshes and the component/clearance fork must be supplied before asserting a numeric converted volume. Rectangular terrain bounds do not erase these objects.')
    v('TR5-04-A', ['MT8-Q08', 'MT8-Q09'], {'casterCenter': [0, 0, 1], 'sphereCenter': [20, 0, 1], 'radiusFt': 20, 'subjects': [{'id': 'large-armored', 'center': [8, 0, 5], 'halfExtents': [2, 2, 5], 'totalMassLb': 800, 'size': 'Large'}, {'id': 'medium-ally', 'center': [32, 0, 1], 'halfExtents': [1, 1, 1], 'totalMassLb': 150, 'size': 'Medium'}], 'membership': 'Both declared body centers strictly inside20ft; actual body geometry also intersects the sphere. Metal armor material/fit and whole subject mass must be actual facts.'}, 'Each unwilling eligible subject makes its own actual STR save. A failed subject moves under the chosen ordered collision rule, at most20ft, with its entire real armor/body once.', {'duplicateArmorSave': False, 'twoArmorPiecesGrant40ft': False, 'largeAbove1000lbCap': False}, 'The800lb Large creature has no actual operative profile here. Neither actual STR save nor final collision stop is fabricated; a150lb total alone cannot certify body/armor masses or metal composition.')
    v('TR5-04-B', ['MT8-Q08', 'MT8-Q09'], {'items': 'Actual unattended breastplate profile exists at equipment_acquisition_candidate.json/items/7 (20lb), but actual metal construction remains an explicit physical input.', 'overweightBodyLb': 1400, 'proposedCapLb': 1000, 'otherSubjects': 'One unarmored carrier with a coin purse and one genuinely rigid anchored armored subject.'}, 'Resolve each actual eligibility and permitted movement independently.', {'unattendedEligibleArmorRequiresSave': False, 'coinPurseQualifiesWholeCarrier': False, 'overweightBodyMoved': False, 'fixedAnchorTorn': False, 'inventedCrushingDamage': 0}, 'Full item/body/anchor geometry and genuine material identities are still required. No armor is stripped from a wearer by treating it as unattended.')
    v('TR5-06-A', ['MT8-Q10'], {'casterCenter': [0, 0, 1], 'wallNearX': 20, 'wallFarX': 32, 'tunnelY': [-2.5, 2.5], 'tunnelZ': [0, 10], 'actualThicknessFt': 12, 'hiddenAlternativeFarX': 45, 'hiddenAlternativeThicknessFt': 25}, 'Declare a through-passage using real near-face perception and actual second-side eligibility. These are alternative initial worlds, not a free test followed by re-aiming.', {'12ftFormationIfEligible': True, '25ftFormationUnder20ftCap': False, '25ftPaidCastRefund': False, 'revealsExactHiddenThickness': False}, 'Both wall material and real far-side receiving corridor must exist. Actual moving bodies spend their own real movement; the spell supplies no travel Action or portal.')
    v('TR5-06-B', ['MT8-Q11'], {'tunnelBoxMin': [20, -2.5, 0], 'tunnelBoxMax': [32, 2.5, 10], 'bodyCenter': [21.5, 0, 1], 'bodyHalfExtents': [1, 1, 1], 'nearExteriorCandidateCenter': [19, 0, 1], 'cargo': 'Real held gear within the same whole-body fit, unchanged identity/charges.'}, 'At the actual source ending or suppression checkpoint, test legal local mouth routes and full-body exterior occupancy under the chosen bounded rule.', {'nearCandidateCenterDistanceFt': 2.5, 'normalCase': 'If the stated path/exterior is genuinely clear, move that same whole body/cargo to the local exterior.', 'bothMouthsBlocked': 'Record finite local pending-placement conflict; no new body, arbitrary damage, remote safe-room search or new entrant passage.'}, 'Exact ejection rule, closing clearance, fluid capacity and distinction between suppressed-live and final-ended application remain Q11. No actual antimagic cast or resource-free closure trigger is invented.')
    v('TR5-08-A', ['MT8-Q05', 'MT8-Q12'], {'casterCenter': [0, 0, 1], 'selectedMudBoxMin': [20, 0, -1], 'selectedMudBoxMax': [25, 2, 0], 'volumeCuFt': 10, 'mudDensityIfApproved': 70, 'stoneDensityIfApproved': 150}, 'Convert the one actual eligible lot, preserving its complete provenance and damage fraction.', {'massBeforeLb': 700, 'massAfterLb': 1500, 'oldMudRetainedLb': 0, 'automaticallyMinedOrTransported': False, 'gemOrFinishedBrickCreated': False}, 'Actual mud/stone admission, whole-body clearance, density/solid durability and excavation permissions remain explicit; the spell grants no real excavation Action.')
    v('TR5-08-B', ['MT8-Q12', 'MT8-Q13'], {'casterCenter': [0, 0, 1], 'ceilingBoxMin': [19, -1, 10], 'ceilingBoxMax': [21, 1, 11], 'recipient': {'class': 'Wizard', 'level': 1, 'DEX': 14, 'CON': 14, 'normalHPBefore': 8, 'maximumHP': 8, 'tempHP': 0, 'WoundsBefore': 0, 'center': [20, 0, 1], 'bodyHalfExtents': [1, 1, 1]}, 'damageFacesD6': [4, 4, 4, 3], 'DEXSave': {'face': 14, 'modifier': 2, 'total': 16, 'DC': 16}, 'woundSave': {'face': 15, 'modifier': 2, 'total': 17, 'DC': 10}}, 'If the exact proposed overhead burst applies to the actual unsupported converted section, resolve its one original caster damage root; ordinary caster outside Null, no defense/transfer/floor/concentration.', {'sum4d6': 15, 'saveHalfFloor': 7, 'postTempDamage': 7, 'normalHPAfter': 1, 'woundTrigger': '2×7≥8, once', 'woundSaveSuccess': True, 'WoundsAfter': 0, 'newDeathState': False, 'laterCollapseDamageAutomaticallyGranted': False, 'separateHardenedOccupiedRegion': 'Chosen body-clearance rule must retain the actual occupied volume; damaged material cycling retains its damage fraction.'}, 'The4d6 burst itself is proposed new authorship, and actual ceiling support/source geometry must qualify. The separate occupied mud and damaged-stock obligations remain explicit pending complete geometry/HP rules; they are not claimed demonstrated by this target trace.')
    v('TU6-04-A', ['MT8-Q14', 'MT8-Q15'], {'casterCenter': [0, 0, 1], 'buildingBoxMin': [10, -10, 0], 'buildingBoxMax': [40, 10, 20], 'translation': [20, 0, 0], 'wholeMassLb': 80000, 'wholeContents': 'Same actual occupants, fittings, furniture and damaged roof; attached external services disconnected under actual permissions.'}, 'Validate entire structure, contents, soil/foundation and swept geometry before one atomic20ft horizontal translation.', {'dimensionsFt': [30, 20, 20], 'sweptBoundsMin': [10, -10, 0], 'sweptBoundsMax': [60, 10, 20], 'eachPointPathFt': 20, 'massBelowCap': True, 'automaticRepair': False, 'duplicateContents': False, 'edgeOccupant': 'Only the separately proposed actual successful DEX/clear5ft route can permit leaving.'}, 'Bounding box/mass alone do not prove a real building/support/soil profile. Occupant escape, actual supports, clear swept space and final capacity must be supplied; no success die or physical structure is invented.')
    v('TU6-04-B', ['MT8-Q14'], {'farthestPointRadiusFt': 20, 'declaredRotationDegrees': 90, 'pointPathCapFt': 30}, 'Apply the proposed actual point-arc distance limit before payment for known illegal declarations.', {'pointArcFt': 10 * math.pi, 'known90DegreeRotationLegal': False, 'maximumPermittedAngleRadiansFromThisOnePoint': 1.5, 'unsupportedPitDestinationLegal': False}, 'A smaller angle alone does not prove every other point/collision/support constraint. The original example remains an eligibility rejection, not a paid successful move or crushing attack.')
    v('TU6-06-A', ['MT8-Q16'], {'sourceDimensionsFt': [10, 10, 10], 'sourceVolumeCuFt': 1000, 'candidateCavityVolumeCuFt': 200, 'selectionCubeSideFt': 40, 'maximumVolumeCuFt': 8000, 'eachParcelPathLimitFt': 30}, 'Compare a genuinely supported/conserved final berm with the insufficient200cu.ft cavity as separate declared plans.', {'cavityShortfallCuFt': 800, 'deletedOrCompressedExcessCuFt': 0, 'validBermMaterialSameLot': True}, 'Full final berm mesh, parcel mapping, continuous path, actual stable slope and material profile are still required. Source volume fits the cap but is not proof of any particular final legal berm.')
    v('TU6-06-B', ['MT8-Q15', 'MT8-Q16'], {'recipient': {'class': 'Wizard', 'level': 1, 'DEX': 14, 'CON': 14, 'normalHP': 8, 'Wounds': 0}, 'failedDEX': {'face': 8, 'modifier': 2, 'total': 10, 'DC': 16}, 'supportRemovalAlternative': 'Actual recipient feet40ft above the legal landing surface, no flight/hover/support substitute, actual subsequent same-slot-next-round-END Fall Marker.'}, 'For a legal displacement, the failed save conditionally carries the body and adds only proposed Prone. In the distinct support-removal branch, use actual Falling rather than a new spell attack.', {'failedSave': True, 'legalCarryBranchProne': True, 'separateSpell6d6Added': False, 'fallingDiceIf40ftActuallyDescended': '2d6', 'fallingTiming': 'First descent at END of this initiative slot next round; no immediate descent invented.', 'hiddenImmovableBlocker': 'Whole declared conserved transition may fail after actual commitment, without deleting the object or exposing a map.'}, 'No actual final terrain mesh or landing/swept path is supplied, so the fall is a conditional timing/dice obligation, not a completed damage event. Actual die faces/life consequences belong to the eventual full vector.')

    ck('Sixteen original IDs and order retained', [v['id'] for v in vectors] == [h['id'] for h in audit['all16HistoricalScenarioTexts']])
    ck('Sixteen genuine questions', len(questions) == len({q['id'] for q in questions}) == 16)
    ck('No orphan question reference', all(set(v['questionIds']) <= {q['id'] for q in questions} for v in vectors))
    ck('Water volume and translation', (12-10)*(5-(-5))*(10-0) == 200 and 20-10 == 10)
    ck('Fabricate conserved conditional mass', 4*8+8 == 40 and 12 >= 12)
    ck('Terrain volume and mass', 5*4*1 == 20 and 20*100 == 2000 and 20*57 == 1140)
    ck('Magnetize subject center membership', 12**2 + 4**2 < 20**2 and 12 < 20 and 800 <= 1000 < 1400)
    ck('Passwall limits and nearest candidate', 12 <= 20 < 25 and Fraction(43,2)-19 == Fraction(5,2))
    ck('Mud volume and conversion', 5*2*1 == 10 and 10*70 == 700 and 10*150 == 1500)
    ck('Burst dice/save/Wound arithmetic', sum([4,4,4,3]) == 15 and 15//2 == 7 and 8-7 == 1 and 2*7 >= 8 and 15+2 >= max(10,7//2))
    ck('Building bounds and sweep', 30<=40 and 20<=40 and 20<=30 and 80000<=250000 and 20<=30 and 40+20==60)
    ck('Rotation arc is strictly above limit', 10*math.pi > 30 and 20*1.5 == 30)
    ck('Earth volume and missing capacity', 10**3 == 1000 and 1000-200==800 and 1000<=8000)
    ck('Actual Falling dice', 40//20 == 2)
    for r in records:
        ref = r['sourceReference']
        ck('Original full record unchanged: ' + r['spellId'], at(read(G/ref['source']['path']), ref['pointer']) == r['completeEarlierRecordUnchanged'])
    result = {'id': 'MATERIAL-TERRAIN-8-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
              'status': 'UNSENT / UNADOPTED design conference before substantial new systemic rules.',
              'developmentDirection': 'video-game-only', 'sourceAudit': info(ap), 'records': deepcopy(records),
              'all16HistoricalScenarioTexts': deepcopy(audit['all16HistoricalScenarioTexts']),
              'completeOriginalSharedProposalsUnchanged': deepcopy(audit['completeOriginalSharedProposalsUnchanged']),
              'inheritedAcceptedInterfaces': deepcopy(audit['currentAcceptedInterfaceComparisons']),
              'completeAcceptedCounterparts': deepcopy(audit['completeAcceptedCounterparts']),
              'completePendingCounterparts': deepcopy(audit['completePendingCounterparts']),
              'semanticDelta': deepcopy(audit['semanticDelta']), 'findings': deepcopy(audit['findings']),
              'conferenceQuestions': questions, 'conditionalConferenceVectors': vectors, 'riskCounts': audit['riskCounts'],
              'sourceBindings': list(sources.values()), 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0,
              'sourceInformationDeleted': 0, 'cosmologyDecisions': 0,
              'countsUnchanged': {'reviewed':480,'pending':368},
              'scopeLimit': 'All original procedures and scenario obligations preserved. Conditional comparisons do not prove missing real recipes, materials, actors, structures or physical-engine rules. Ask GPT for genuine local choices before authoring a new operative candidate.'}
    out.write_bytes(encoded(result))
    bind(out)
    root.mkdir()
    frozen=[]
    for b in sources.values():
        ck('Current exact source: '+b['path'], info(G/b['path'])==b)
        p=root/'sources'/b['path']
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((G/b['path']).read_bytes())
        ck('Preserved exact source: '+b['path'], info(p)['sha256']==b['sha256'])
        frozen.append({**b,'archivePath':'sources/'+b['path']})
    (root/'MANIFEST.json').write_bytes(encoded({'id':'MATERIAL-TERRAIN-8-CONFERENCE-01-MANIFEST','candidate':info(out),'sources':frozen,'sourceCount':len(frozen),'procedures':8,'originalCases':16,'conditionalVectors':16,'questions':16,'status':'Unsent design conference; no new operative rule adopted.'}))
    (root/'LOCAL_PREFLIGHT.json').write_bytes(encoded({'checks':checks,'checkCount':len(checks),'failureCount':0,'runtimeTestsExecuted':0,'scope':'Exact source/preservation/access and stated conditional arithmetic; not semantic approval or simulation.'}))
    (root/'README.md').write_text('''# Material and terrain: eight-source design conference

Read the manifest, complete candidate, eight original procedures, original shared proposals and all sixteen original scenario obligations. Current conditional traces retain those obligations and distinguish real accepted interfaces from missing actual physical/recipe/content prerequisites. They are not complete executed game cases.

Resolve only the sixteen genuine new decisions. Do not reopen casting, existing crafting, ordinary movement, Ready, Falling, damage/Null, corpse or accepted antimagic rules. Creation and Freezing Sphere are full pending comparisons, not accepted global physics. Source-specific geometry, conversion, permanent stock, manufacture and placement choices require explicit concurrence before a new operative candidate is authored.

Return per-spell and per-question dispositions, exact source/pointer findings, complete proposed before/after rule replacements where necessary, original-case coverage and the exact input/output hashes. Explicitly state remaining conditional content prerequisites. Preserve nine school/rank placements (including both Fabricate placements), original access, histories, all75 project domain gates and video-game-only direction. This conference cannot confer adoption, runtime, balance, cosmology, release or whole-game closure.
''',encoding='utf-8')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(set(z.namelist()))==len(frozen)+3
        for b in frozen:
            raw=z.read(b['archivePath'])
            assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    b=info(archive)
    requestp.write_text(f"Please conduct the eight-spell material/terrain design conference using DD_Material_Terrain_8_Conference_01.zip ({b['bytes']} bytes; SHA-256 {b['sha256']}). All {len(frozen)} full files are frozen and verified. Read all8 complete preserved proposals,9 placements,16 original cases and16 explicit conditional traces. Resolve the16 real forks in volume/control, mundane manufacturing, assistant timing, permanent material conversions, body clearance, local ice, magnetized bodies/crowding, Passwall state/ending, stone durability/overhead burst, structure displacement and finite earth geometry. Inherit accepted interfaces and keep missing actual recipe/material/actor/geometry inputs explicit. Creation and Freezing Sphere remain pending comparisons, not global authority. Return complete source-linked corrections and dispositions in a downloadable archive, preserving every original ID/text. This is video-game-only design conference before new systemic authorship, not exact acceptance or adoption. Current480 reviewed/368 pending and75 domain gates remain unchanged; no cosmology or release claim.\n",encoding='utf-8')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'localPreflight':info(root/'LOCAL_PREFLIGHT.json'),'request':info(requestp),'sourceCount':len(frozen),'checkCount':len(checks),'allArchiveSourceHashesVerified':True,'submitted':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sourceCount':len(frozen),'checks':len(checks),'procedures':8,'originalCases':16,'conditionalCases':16,'questions':16}))


if __name__ == '__main__':
    main()
