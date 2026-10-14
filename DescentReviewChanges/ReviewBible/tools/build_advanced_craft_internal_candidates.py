"""Author the 167 internal recipe candidates from the final advanced verdict.

Additive draft output only. Original recipes, class cards and reviewer files stay
byte-identical. Public projection and the separate exact review remain required.
"""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
import math
import re
import shutil

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
V = A / 'advanced167-source-authoring-reviewer-files'
STATUS = 'authored-internal-candidate-awaiting-validation-public-projection-and-exact-review'
TRADES = {'Enchanting': ('EN', "Enchanter's tools"), 'Rune Carving': ('RC', "Runecarver's tools"),
          'Scribing': ('SC', "Calligrapher's supplies"), 'Tinkering': ('TI', "Tinker's tools")}
GUIDE = 'docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md'
BODY_GUIDE = 'docs/director-only/ADVANCED_CRAFT_INTERNAL_BODY_CATALOGUE.md'
VERDICT_HASH = '48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def objsha(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def dump(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ratio(v):
    v = F(str(v)) if not isinstance(v, F) else v
    return {'numerator': v.numerator, 'denominator': v.denominator}


def val(v):
    if isinstance(v, dict):
        v = F(v['numerator'], v['denominator'])
    else:
        v = F(str(v)) if not isinstance(v, F) else v
    return str(v.numerator) if v.denominator == 1 else f'{v.numerator}/{v.denominator}'


def sections(text):
    matches = list(re.finditer(r'^## ((?:AC|EN|RC|SC|TI|TD|B|R|W|K)-\d{2}) —\s*([^\n]+)', text, re.M))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        part = text[m.end():end].strip()
        part = re.split(r'\n# ', part, maxsplit=1)[0].strip()
        out[m[1]] = {'id': m[1], 'title': m[2], 'text': part,
                     'verdictHeading': m[0], 'sourceVerdictSha256': VERDICT_HASH}
    return out


def use_text(r, reg):
    b = reg['authoredUseBinding']; p = reg['profile']; m = r['mechanics']
    if p == 'EN-standard':
        n = b['enhancement']; c = b['maximumCharges']; dt = b['damageType']
        return (f"Each finished body has enhancement +{n}, maximum {c} charge(s), and {dt} as its sole charge damage type. "
                f"An admitted actual weapon adds +{n} to its eligible item accuracy comparison and +{n} ordinary flat weapon damage once per hit; its unsuppressed ordinary B/P/S damage is magical. "
                f"Charged Strike costs one Action and one charge before its single actual weapon attack; a hit adds {n}d6 {dt} to that attack's damage event. It is not the Attack Action and grants no Extra Attack; an ordinary critical doubles dice, never flat bonuses. "
                f"An admitted armor suit supplies +{n} in equipment.defense-enhancement only while its worn armor formula is selected. Typed Guard spends a Reaction and charge on a positive resolved {dt} damage component, after defenses but before HP/positive-damage triggers, reducing it by {n}d6 to a minimum of zero. "
                f"Every other admitted carrier uses Typed Pulse: Action, one charge, one manipulating hand, one perceived creature or physically compatible object within 30 feet and line of effect; fixed +{4+n} nonspell attack, hit {2*n}d6 {dt}, no ability/PB/flat enhancement added again. "
                "Only the profile belonging to the registered body is available. These activations spend no RP, do not enter spell cadence and cannot be Counterspelled. Charges refill to maximum only at an eligible actual campaign 06:00 dawn under EN-06; suppressed/missing/zero-HP items miss that event, with no catch-up or local-sunrise/transfer reset. Titles supply no unprinted flight, command, healing or class focus. EN-01–10 and AC-07 supply the full use and comparison procedures.")
    if p == 'RC-binding':
        return (f"A prepared plate has {b['charges']} lifetime charge(s). First legal creature entry spends one: DC {b['saveDC']} STR save; failure is Restrained for at most 60 seconds. Repeat the save at the end of each regular turn. An Action permits STR (Athletics) or DEX (Acrobatics) escape, or an adjacent helper's STR (Athletics), at that same DC through Core task binary resolution. Leaving the original square or moving/suppressing the original plate ends this restraint. "
                "Use RC-02–04 entry, placement, next-regular-start/six-second arming delay, cap, discharge and manual rearming rules. No Stun, occupancy retrigger, ally exemption, recharge or repair refill.")
    if p == 'RC-explosive':
        return (f"A prepared plate has {b['charges']} lifetime charge(s). First legal creature entry spends one burst centered on that actual plate, radius {b['radiusFeet']} feet, all creatures with line of effect including allies/setter: DC {b['saveDC']} DEX, {b['damage']} {b['damageType']} on failure and zero on success. "
                "No object damage, extra condition or second burst for simultaneous entrants. Use RC-02/03/05 placement, delay, one-item-per-round discharge, stable event order, disarming and cleared-square manual rearm. Remaining in the square does not retrigger. Neither dawn nor restoration refills it.")
    if p == 'RC-healing':
        return (f"Register at most six actually known permitted allied identities. This plate has {b['charges']} lifetime charge(s); one eligible entry or Action touch spends one to restore {b['healing']} ordinary HP to one actual eligible living ally. A helper can spend an Action with direct plate contact on an assigned willing or Incapacitated ally within 5 feet under RC-06. "
                "Stationary setup/arming and helper healing are separate Actions; moving the plate does not heal creatures along its route. Ordinary healing blockers, eligibility and caps remain: no Dead target resurrection or crafted-Construct reconstruction. A legal full-HP/prevented heal still spends its charge. RC-02/03/06 enforce one discharge per physical item per round, identity and no refill.")
    if p == 'RC-warding':
        return (f"This plate has {b['charges']} lifetime charge(s) and a +{b['bonus']} ward. Ten active minutes attunes its one bearer; one ward per bearer, one bearer per ward, and death ends attunement. Wear it in one actual wrist, neck or chest jewelry position, taking an Action to don/doff. "
                f"Before an attack roll targeting the bearer or the bearer's save roll, spend one Reaction and charge for +{b['bonus']} AC in equipment.defense-enhancement and +{b['bonus']} saves in equipment.jewel-save-enhancement through the next regular-turn start, including the triggering roll. Outside initiative use the RC-07 six-second marker. "
                "No post-roll activation, second Reaction, free jewelry slot or extra-turn expiry/reset. Removal, meld, suppression or lost eligibility suspends the remaining benefit while its deadline runs. Use RC-07/08's complete timing and comparisons; charges never refill.")
    if p == 'SC-script':
        return (f"A completed blank carrier can encode one authentic, completed operational spell/ritual of rank at most {b['maximumSpellRank']}; it allows {b['lifetimeActivations']} lifetime legal cast start(s), always of that same payload, plus +{b['researchBonus']} relevant research. "
                "Record exact spell/version/rank/class placement and genuine source access. A trained Calligrapher uses INT, the real desk/kit, max(1, rank) active hours, that many sp and 0.01 lb per hour of actual encoding supplies, and DC 10 + rank Core task binary resolution. Failure consumes time/supplies; encoding earns no crafting XP or Forge Dwarf reduction. No overwrite, capacity multiplication or refill. "
                "SC-03 expressly adds one-cast temporary repertoire only for a reader with the actual class/list, level/rank, RP, component and other spell eligibility. Use the spell's own action/time, range, concentration and cadence; pay one script use and normal resources at cast commitment. Counterspell can stop that paid cast; ready/release creates no second cast. The readable open script must be handled or supported within 5 feet; spell hands/components remain mandatory. Copying words does not copy magical uses. The +research requires actual relevant consultation under SC-04, and never improves creating this bonus item. SC-01–04 and SC-10 govern the full procedure.")
    if p == 'SC-map':
        return (f"Actual authenticated map/diagram content grants +{b['navigationBonus']} appropriate navigation and +{b['researchBonus']} relevant research through equipment.leather-task-enhancement. The lead must genuinely consult it for at least one necessary minute or throughout an independently allowed shorter task; its mapped place/subject must apply. "
                f"Each physical item has {b['rerollsPerPhysicalItemPerFormalExpedition']} reroll per genuine formal expedition: after one related failed check but before consequences, reroll its original die selection with the same DC/modifiers/context and accept the replacement even if worse. One Scribing reroll per check; borrowing, repair, Watch changes and brief Haven stops do not reset it. "
                "Only formal prior expedition closure and a genuinely authorized new expedition provide another entitlement. Copies convey information, not the original item's magic or budget. SC-04–06 and SC-10 apply; an invented location or closed stowed map gives no benefit.")
    if p == 'SC-reference':
        return (f"This authentic reference supports +{b['researchBonus']} relevant Arcana, History, Religion, Nature or Engineering research through equipment.leather-task-enhancement after the actual lead's necessary consultation. Its source languages field is exactly {b['languages']}. "
                + (f"Where actual useful parallel text and an understood bridging language exist, it offers {b['languages']} Language Insight for that reader/language/evidence under SC-07/08: one active hour, same evidence once across copies, six unspent maximum; spending three plus eight active study hours interprets one preregistered supported passage of at most 250 words. " if b['languages'] else "It grants zero Language Insight and no language proficiency or fluency. ")
                + "Actual textual scope/readability controls every benefit. Copying text gives no new magical research bonus or repeat evidence reward. This is not a spell, an ink-supply generator or a hidden-lore decoder. SC-04/07/08/10 provide the full boundaries.")
    if p == 'TI-trap':
        return (f"This fixed trap has {b['charges']} charge(s). Spend one minute with both hands and actual Tinker's tools to place it on a stable eligible unoccupied 5-foot square, then an Action to arm; it becomes armed at the next regular-turn start or six-second boundary. "
                f"Its first actual creature entrant, including allies, consumes one charge and the setter's available shared offensive allowance: DC {b['saveDC']} DEX, {b['damage']} {b['damageType']} on failure, zero on success. It then disarms. "
                "No discharge, charge spend or queued attack when the setter's allowance is unavailable. Forced movement/fall/teleport arrival can be entry; remaining in place is not. Moving it disarms it. Max three armed crafted traps per setter; manual reset, cleared square, delay and one-item-per-round guard remain. Setter incapacity/death alone does not switch off an eligible automatic trap. TI-02 gives full disarm rules. TI-06's trained one-hour servicing may refill charges; HP repair/rest may not.")
    if p == 'TI-automaton':
        atk = b['attack']
        return (f"Choose Tiny or Small before work and keep that size. The finished Construct has AC {b['armorClass']} and maximum {b['hitPoints']} HP; full unmodified B5 chassis gives full HP, otherwise initial HP is max(1, floor({b['hitPoints']} × latest chassis HP / 5)). "
                f"Its fixed magical nonspell melee attack is +{atk['bonus']} to hit, reach {atk['reachFeet']} feet, {atk['dice']} {atk['damageType']} on hit, no ability damage or condition rider. Ordinary attack natural results apply. "
                "Tiny: STR 6, DEX 12, CON 10, INT 3, WIS 10, CHA 1, walk 20 feet, gripper load at most 5 lb. Small: STR 12, DEX 10, CON 12, INT 3, WIS 10, CHA 1, walk 25 feet, at most 20 lb. Ordinary senses/passive 10; no flight, PB, equipment slots or Anacite modules. Poison damage and Poisoned immunity only; other defenses are not inferred. "
                f"Maximum service units {b['serviceMaximum']}: one genuine encounter for at most ten elapsed minutes, or one ten-minute noncombat operating block, paid at block start. Continuing past expiry needs another; entering combat closes the noncombat block and spends a new unit. Zero units inside an already paid block permits that block only. Suppression/shutdown keeps the clock running. "
                "TI-04 binds a capable consenting INT-6+ controller with ten minutes of real tools/permission, max three active ordinary crafted automata separately from one 686. One owner-wide Bonus Action command and one relevant offensive allowance per numbered round across class/crafted devices; actual communication within 60 feet, execution after the whole controller turn, no independent Reaction. The commanded creature moves and makes one attack or permitted task; powered uncommanded behavior is only defensive movement/Dodge. Transfer cannot give a second attack. Finite noncombat programming is ten minutes, with Action start and paid blocks; no professional crafting, script use or ram crew. "
                "At zero HP it is a destroyed recoverable wreck if original primaries survive; no death saves, Wounds or ordinary biological healing. TI-06 servicing and AC-09/TD-07 restoration are distinct. Structural quality never changes the printed creature statistics. TI-03–07 govern the complete procedure.")
    if p == 'TI-utility':
        return (f"This actual physical tool/device/sensor has +{b['bonus']} appropriate checks and {b['charges']} utility charge(s). Before the roll, the actual lead selects this item, directly performs genuinely necessary compatible work for one active minute or throughout a separately allowed shorter task, and spends one charge. "
                "Compare it once in equipment.leather-task-enhancement; a stronger eligible source does not refund the spent charge. The original required ordinary tools still apply. Its physical probe/gauge/jaws must actually reach and perform the work; it does not detect hidden creatures through walls. "
                "No assistance to creation, repair, re-encoding, recharge or servicing of any bonus-granting advanced/gathering item, including itself or another utility. Actual ordinary engineering, exposed-mechanism investigation, compatible tool tasks and genuine formula research can qualify. Complete positive-HP unsuppressed participating state is required at work and resolution. TI-06 provides actual one-hour trained servicing to reset printed maximum; HP repair, rest and ownership do not.")
    # The five custom schemas must retain their complete distinct authored procedure.
    return {'RC-null-seal': 'This is the custom stationary null seal. Use the full RC-10 procedure below; it has one NEW lifetime activation, not an invented source charges field.',
            'SC-lexicon': 'This is the custom multilingual research Lexicon. Its three Insight are reader/evidence scoped, not charges or fluency. Use the full SC-08 procedure below.',
            'SC-pact': 'This is the custom one-bargain Codex. Consent, clauses, evidence, each signatory’s finite breach event and the independent mark deadline use the complete SC-09 procedure below.',
            'TI-drone': 'This is the custom AC 18 / 80 HP Small command relay with no attack. Its winding hour, three authorized links and current shared command limits use TI-08 below.',
            'TI-siege': 'This is the custom stationary ram: +6 melee attack within 5 feet for 12d10 force against actual doors, gates, barriers or Constructs. Its three-Action cycle and separate once-per-long-rest creator-statistic breach use TI-09 below.'}[p]


CUSTOM = {'RC-null-seal': 'RC-10', 'SC-lexicon': 'SC-08', 'SC-pact': 'SC-09', 'TI-drone': 'TI-08', 'TI-siege': 'TI-09'}


def body_models(reg, sec):
    models = {}
    for key, b in reg['bodyProfiles'].items():
        prefix = key.split('-')[0]; group = {'EN': 'B-01', 'RC': 'B-02', 'SC': 'B-03', 'TI': 'B-04'}[prefix]
        models[key] = {'id': key, 'status': STATUS, 'sourceAuthoringProfile': deepcopy(b),
                       'operationalBodyText': sec[group]['text'], 'worksiteText': sec['B-05']['text'],
                       'structuralTrackIsNotCreatureHP': key in ['TI-auto-tiny', 'TI-auto-small', 'TI-drone'],
                       'provenanceSections': [group, 'B-05', 'AC-01', 'AC-02', 'AC-03', 'AC-09']}
        if key == 'TI-trap':
            models[key]['openExactReviewIssue'] = 'ADV-EDIT-01: B-04 requires the original spring; the body table/register call spring/contacts replaceable. Preserve both. This candidate requires the spring pending targeted confirmation.'
    return models


def host_models():
    equipment = read(R / 'data/playtest/equipment_acquisition_candidate.json')
    out = {}
    for e in equipment['items']:
        if e['category'] not in ['Simple melee weapons', 'Simple ranged weapons', 'Martial melee weapons', 'Martial ranged weapons', 'Armor and shields']:
            continue
        sf = e.get('sourceFields', {}); armor = e.get('group') in ['Light Armor', 'Medium Armor', 'Heavy Armor']
        weapon = e['category'].endswith('weapons') and bool(re.search(r'\d', sf.get('Damage', '')))
        if not armor and not weapon:
            continue
        out[e['id']] = {'id': e['id'], 'bodyKind': 'EN-armor' if armor else 'EN-weapon',
                         'sourceEquipmentRecord': deepcopy(e),
                         'baselineStructuralHP': {'Light Armor': 10, 'Medium Armor': 15, 'Heavy Armor': 20}[e['group']] if armor else 5,
                         'ordinaryPriceGp': ratio(F(str(e['unitPriceCp'])) / 100),
                         'ordinaryWeightLb': e['unitWeightLb'], 'status': STATUS,
                         'physicalRegistration': 'Record actual complete source-compatible body, size, grade, load-bearing material/AC, dimensions, original working/structural primary members and current damage history before work. No invented stock or fit.',
                         'sizing': 'Existing eligible Large size doubles ordinary price, weight and generic HP; Small/Medium/Tiny retain their actual source sizing. Apply actual permitted grade and workmanship afterward.',
                         'sourceProcedure': 'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
                         'prohibited': ['already magically altered host', 'natural attack', 'ammunition bundle', 'shield', 'unsupported special model']}
    return out


def operation(r, x, bodies, sec):
    q = r['quantity']; w = r['workRequirements']; creature = x['profile'] in ['TI-automaton', 'TI-drone']
    minutes = x['operationalActiveMinutes']; dwarf = x['forgeDwarfActiveMinutes']
    o = {'profile': x['profile'], 'useBinding': deepcopy(x['authoredUseBinding']),
         'bodyModelIds': x['bodyChoices'], 'standardQuantity': q, 'maximumOrderedBodyReserve': 3*q//2,
         'work': {'ability': 'Intelligence', 'credential': TRADES[r['skill']][1], 'artisan': True,
                  'sourceRequirements': deepcopy(w), 'sourceActiveHours': w['activeWorkHours'],
                  'activeMinutes': minutes, 'forgeDwarfActiveMinutes': dwarf,
                  'includedFirstPhaseMinutes': min(15, minutes), 'dwarfIncludedFirstPhaseMinutes': min(15, dwarf),
                  'remainingActiveMinutes': minutes-min(15, minutes), 'dwarfRemainingActiveMinutes': dwarf-min(15, dwarf),
                  'laterPhaseMaximumMinutes': 480, 'DC': r['craftingCheck']['targetDC'],
                  'sourceDiscovery': deepcopy(r['discovery']), 'sourceSkillProgression': deepcopy(r['skillProgression'])},
         'creation': {'sixBands': {'Mishap': 0, 'Failed': 0, 'Flawed': q//2 if q>=2 else (0 if creature else 1),
                                   'Standard': q, 'Exceptional': q*5//4, 'Masterwork': q*3//2},
                      'structuralAlternativeQuantity': q, 'structuralAlternativePercent': [] if creature else [25, 50],
                      'creatureQualityAlternativeHasNoMechanicalImprovement': creature,
                      'singletonFlawedMapsToFailed': creature and q==1,
                      'singletonFlawedAddsPersistentStructuralFlaw': not creature and q==1,
                      'naturalOneIsMishap': True, 'naturalTwentyShiftsBand': False,
                      'forgeDwarfStandardBecomesExceptional': True,
                      'masterworkCatalystMaximumUnits': min(1, len(x['catalystOccurrences']))},
         'references': deepcopy(x['references']), 'creatureOutput': creature,
         'componentOccurrences': [], 'sourceStandardBatchReferenceGp': ratio(r['economy']['recommendedMarketValue']),
         'sourceProcessUnitReferenceGp': ratio(F(str(r['economy']['recommendedMarketValue']))/q),
         'requiredSharedSections': [f'AC-{i:02}' for i in range(1,11)] + [f'{TRADES[r["skill"]][0]}-{i:02}' for i in range(1,11)] + ['B-01' if r['skill']=='Enchanting' else 'B-02' if r['skill']=='Rune Carving' else 'B-03' if r['skill']=='Scribing' else 'B-04', 'B-05'],
         'paragraphs': []}
    if r['skill'] == 'Tinkering': o['requiredSharedSections'] += [f'TD-{i:02}' for i in range(1,19)]
    bulk = {'Enchanting': {'Veilthread'}, 'Rune Carving': {'Runic ink', 'Binding agent'}, 'Scribing': {'Ink', 'Preservation treatment'}, 'Tinkering': set()}
    for i,c in enumerate(r['components']):
        o['componentOccurrences'].append({'index': i, 'sourceComponent': deepcopy(c), 'retainedTool': not c['consumed'] and c['role']=='tool',
                                         'consumedTool': c['consumed'] and c['role']=='tool',
                                         'masterworkCatalystEligible': c['consumed'] and c['role']=='catalyst',
                                         'failedRecoveryEligible': c['consumed'] and c['role']!='catalyst',
                                         'defaultFailurePrecision': ratio(F(1,100) if c['name'] in bulk[r['skill']] else 1),
                                         'precisionCondition': '0.01 requires the actual declared divisible form; otherwise unit 1. A genuinely independent ingredient source may specify a different legal subdivision.',
                                         'physicalIdentityMustRemainDistinct': True})
    variants = []
    for bid in x['bodyChoices']:
        b = bodies[bid]['sourceAuthoringProfile']; ref = next(z for z in x['references'] if z['body']==bid)
        B = b['HP']; hp = x['authoredUseBinding'].get('hitPoints', B) if creature else B
        v = {'bodyModelId': bid, 'mundaneBodyReferenceGp': ratio(b['priceGp']), 'bodyMassLb': b['massLb'],
             'ordinaryB': B, 'sourceCreatureMaxHP': hp if creature else None,
             'unflawedStructuralMaximumByChoice': None if creature else {'none': B, 'P25': B+max(1,B//4), 'P50': B+max(1,B//2)},
             'functionalRepair': {'DC': 10, 'materialReferenceGp': ratio(F(ref['functionalRepairGp'])), 'defaultMaxHPHours': ratio(max(F(1), F(hp,10)))},
             'brokenReconstruction': {'DC': r['craftingCheck']['targetDC'], 'materialReferenceGp': ratio(F(ref['brokenReconstructionGp'])), 'defaultMaxHPHours': ratio(max(F(8), F(hp,10)))},
             'repairUsesActualRecordedMaximum': True, 'requiresOriginalCreationAndPrimaries': True}
        if x['profile'] in ['TI-utility', 'TI-trap', 'TI-automaton']:
            mass = max(F(1,100), F(math.ceil(F(str(b['massLb']))),100))
            v['servicing'] = {'DC':10, 'activeMinutes':60, 'packGp':ratio(F(str(b['priceGp']))/10), 'packMassLb':ratio(mass),
                              'restoresPrintedMaximum':x['authoredUseBinding']['charges'], 'restoresHP':False,
                              'trainedCredential':"Tinker's tools", 'ability':'Intelligence'}
        variants.append(v)
    o['bodyVariants'] = variants
    def add(label, text): o['paragraphs'].append({'label': label, 'text': text})
    add('Effect and operation', use_text(r,x))
    if x['profile'] in CUSTOM:
        sid = CUSTOM[x['profile']]; add('Complete custom procedure — '+sid, sec[sid]['text'])
    add('Complete output bodies', 'Choose before any work: ' + '; '.join(
        f"{bid}: {bodies[bid]['sourceAuthoringProfile']['model']} {bodies[bid]['sourceAuthoringProfile']['priceGp']} gp, {bodies[bid]['sourceAuthoringProfile']['massLb']} lb, ordinary B{bodies[bid]['sourceAuthoringProfile']['HP']}, structural AC {bodies[bid]['sourceAuthoringProfile']['AC']}, dimensions {' × '.join(str(t) for t in bodies[bid]['sourceAuthoringProfile']['dimensionsIn'])} inches"
        for bid in x['bodyChoices']) + '. See the complete body catalogue for original primaries, constituent masses, hands, capacity and support. A creature output replaces stock object HP/AC with its printed creature statistics. EN alternate weapon/suit hosts use their exact registered existing equipment profile; these default figures do not overwrite that alternate body.')
    add('Before creation', f"Reserve {3*q//2} actual complete never-magically-altered bodies, one model/size per order, in an exclusive fixed order. All must be complete and positive-HP immediately before the completion roll, even if fewer outputs will result. Bodies are additional to the exact source batch components and working tools. Pre-roll lawful replacement keeps its ordered position; no post-roll acquisition, substitution or reordering. Transform the first resolved outputs; unused bodies remain actual mundane stock. " + ('Use unmodified, unflawed B5 chassis; a former creature/class device is not a blank. ' if creature else '') + 'Record material identity, condition, real storage, actual station capacity, preservation and safe handling; a quoted price supplies none of those facts.')
    add('Creation check and work', f"{r['skill']} level {r['skillLevel']}; INT with actual {TRADES[r['skill']][1]} training, one PB or replacing expertise, DC {r['craftingCheck']['targetDC']}. Untrained otherwise eligible level 1–4 uses no tool PB and disadvantage; trained recipe eligibility is max(4, trade level), with actual formula access. Source duration {r['craftingTime']}; operational {val(minutes)} active minutes, or {val(dwarf)} for an eligible Forge Dwarf. The included first stable phase is {min(15,minutes)} minutes ({min(15,dwarf)} for that Dwarf); remaining work is {val(minutes-min(15,minutes))}/{val(dwarf-min(15,dwarf))} minutes respectively, in declared phases of at most 480 minutes. Only actual incorporated inputs stabilize; raw/returned catalyst clocks continue. Interruption loses unfinished-phase progress, not costs or completed work.")
    add('Facility and assistance', f"Actual {w['station']}, with {', '.join(w['requiredTools'])}; fieldCraftable={str(w['fieldCraftable']).lower()}, source timeMode={w['timeMode']}. A field label never overrides the false creation flag. Fixed compatible facilities, actual minimum surface/bay/fixtures, safe access and expedition-site permissions remain required. Maximum {w['maximumAssistants']} eligible assistants work all required hours without shortening the task or gaining assistant XP. Ordinary facilities/tools grant +0. Two active work Watches, no overlapping labor/rest credit, actual hired capacity and lawful access still apply.")
    add('Formula and advancement', 'Preserve the exact discovery and progression records: ' + json.dumps({'discovery':r['discovery'],'skillProgression':r['skillProgression']},ensure_ascii=False) + '. The crafting framework determines actual first/repeat/qualified-failure/triviality XP. Source skillXPOnSuccess is not an extra award on use, repair, study, service or temporary class fabrication. A finished item supplies no formula/proficiency. Recipe 623 keeps its historical null activeWorkHours and zero laborValue; only its expressly reviewed active-work overlay completes the year.' if r['id']=='recipe-623' else 'Preserve the exact discovery and progression records: ' + json.dumps({'discovery':r['discovery'],'skillProgression':r['skillProgression']},ensure_ascii=False) + '. The crafting framework determines actual first/repeat/qualified-failure/triviality XP. Source skillXPOnSuccess is not an extra award on use, repair, study, service or temporary class fabrication. A finished item supplies no formula/proficiency.')
    add('Manufacturing outcomes', f"Mishap 0; Failed 0; Flawed {o['creation']['sixBands']['Flawed']}; Standard {q}; Exceptional yield {q*5//4}; Masterwork yield {q*3//2}. Natural 1 is Mishap; natural 20 adds no band shift. An eligible Forge Dwarf's Standard becomes Exceptional. " +
        (f"Creature outputs retain printed AC/HP; the alternative quality choice keeps {q} with a label only, no mechanical improvement. Q1 Flawed maps to Failed, including its recovery route; Q≥2 uses reduced yield. Initial creature HP uses max(1, floor(sourceHP × latest chassis HP / 5))." if creature else f"Alternatively retain {q} structural objects with the strongest P25/P50 workmanship once. Maximum = B + max(1, floor(B×P/100)) for positive P, else B; one existing/new singleton persistent flaw halves last, minimum 1. Preserve old maximum minus current damage deficit, clamping the new current to [0,newMax]. Q1 Flawed creates one persistent flaw; Q≥2 reduced yield adds no new singleton flaw, even when one output remains. Standard never heals. Actual EN host size/grade B takes precedence over default-body examples.") + ' No outcome improves charges, potency, source DC, spell rank, capacities or permissions; later repair does not remove a flaw or reapply manufacturing quality.')
    add('Exact component occurrences', 'All listed components are for the original whole batch, not per output. Repeated catalog IDs remain separate supplied quantities.\n\n' + '\n'.join(
        f"- [{i}] {c['name']} ({c['id']}): quantity {c['quantity']}; tier {c['tier']}; source unit {c['value']} gp / {c['weight']} lb; role {c['role']}; consumed={str(c['consumed']).lower()}."
        for i,c in enumerate(r['components'])))
    add('Retention and failure', (f"On Masterwork retain at most one actual catalyst unit total, from occurrence(s) {', '.join(map(str,x['catalystOccurrences']))}. " if x['catalystOccurrences'] else 'This recipe has no eligible catalyst-return occurrence. ') +
        'Failed creation recovers 25% of genuinely remaining consumed non-catalyst quantities by exact identity and legal unit precision, capped by actual remains. The per-occurrence record identifies only expressly divisible bulk; otherwise floor to indivisible units. No quarter tool/lens/core, money conversion, duplicate catalyst, or second salvage pass over waste. Mishap/abandonment returns no consumed inputs. Retained working tools and unused complete bodies survive only as they actually exist. Returned material retains real age, vessels and history; a retained catalyst is not also inside the finished item.')
    add('Restoration and reference prices', '; '.join(f"{v['bodyModelId']}: finished unit {val(next(z['finishedReferenceGp'] for z in x['references'] if z['body']==v['bodyModelId']))} gp, functional repair material {val(v['functionalRepair']['materialReferenceGp'])} gp and default {val(v['functionalRepair']['defaultMaxHPHours'])} hours at DC 10; recoverable Broken/wreck reconstruction material {val(v['brokenReconstruction']['materialReferenceGp'])} gp and default {val(v['brokenReconstruction']['defaultMaxHPHours'])} hours at original DC {v['brokenReconstruction']['DC']}" for v in variants) +
        '. Recompute actual time from current recorded maximum HP: max(1, maxHP/10) or max(8, maxHP/10). Alternate admitted host price/size/grade uses its actual reference. Trained primary trade + INT, original station/implements and host-compatible repair fixtures are required. Original creation record and all magic-bearing primaries must survive; missing/burnt pages, missing frame/actuator, sacrificed or already-consumed debris are not reconstructible by payment. Core task natural shifts collapse to success/failure; failure spends time/material. Restore only recorded HP and lawful function, never charges/service/spell uses, flaws or prior deadlines. No Forge reduction, quality, extra generic assistants or XP. Reference = original batch market value / original Q + actual body; keep exact fractions until final copper purchase-ceiling/sale-floor. Actual quotes, availability, service and ownership are separate.')
    if x['profile'] in ['TI-utility','TI-trap','TI-automaton']:
        add('Separate servicing', '; '.join(f"{v['bodyModelId']}: actual maintenance pack {val(v['servicing']['packGp'])} gp / {val(v['servicing']['packMassLb'])} lb" for v in variants) +
            f". End active operation first; with the complete positive-HP body, actual trained Tinker's tools, a genuinely safe surface and one active hour, make INT tool DC 10 as a Core binary task. Success sets the printed maximum to {x['authoredUseBinding']['charges']}; failure spends the pack/work. No HP repair, surplus, XP, Forge discount or reset of prior round/block history. Field servicing can qualify here while field creation remains false. TI-06 governs pack identity, procedure and failed materials.")
    add('State and interaction', 'Initialize each actual output’s budget once at completion. Track physical identity, controller/holder, complete structure, current HP, suppression/meld, permissions, exact clock/expedition/round events and expenditures. Only actual legal commitment spends resources; legal committed misses/prevention/interruption do not refund them. No transfers, snapshots, copies, repair or relabeling reset state. ' +
        ('The full 48-card Tinker interface register and TD-01–18 apply; class-only bombs, turrets, Anacite modules, deployment costs and caps are not recipe grants. All pending feat interactions remain unapproved. ' if r['skill']=='Tinkering' else '') +
        'Use the complete shared guide alongside this card. Source titles/donors/private research do not create targets, facts, custody, permissions or cosmology.')
    add('Unchanged source effect', r['effects'])
    add('Internal source history', json.dumps({k:r[k] for k in ['tags','legacyName','legacyEffect','wholeCreatureUse','matrixResearch','directorGuidance','knowledgeStatus','publicAvailability'] if k in r}, ensure_ascii=False))
    return o


def render_card(c):
    r = c['sourceRecipe']
    lines = [f"## {r['name']} — {r['id']}", '', f"**Internal candidate; {r['visibility']}; exact approval pending.**", '',
             'Use the [complete operating guide](ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md) and [body catalogue](ADVANCED_CRAFT_INTERNAL_BODY_CATALOGUE.md).', '']
    for p in c['operational']['paragraphs']:
        lines.extend(['**'+p['label']+'**', '', p['text'], ''])
    if c['publicBookBinding']:
        lines.extend(['**Six original public-book paragraphs, unchanged**',''])
        for p in c['publicBookBinding']['paragraphs']:
            lines.extend([f"Paragraph {p['index']}: {p['text']}", ''])
    lines.extend(['**Binding:** full original object/index, source register and occurrence records accompany this manuscript in the internal JSON. Required procedure sections: ' + ', '.join(c['operational']['requiredSharedSections']) + '.', ''])
    return '\n'.join(lines)


def main():
    dest = R / 'data/director/advanced_craft_recipe_candidate_internal.json'
    assert not dest.exists(), 'Do not overwrite an existing candidate; preserve and explicitly revise.'
    verdict = A / 'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md'
    assert sha(verdict) == VERDICT_HASH
    sec = sections(verdict.read_text(encoding='utf-8'))
    assert len(sec) == 100, len(sec)
    evidence = read(A / 'ADVANCED_CRAFT_SOURCE_PREPARATION.json')
    reg = read(V / 'ADVANCED_167_AUTHORING_REGISTER.json')
    originals = read(R / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes']
    protected = read(A / 'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
    assert all(sha(G/p)==h for p,h in protected.items())
    recipes = [r for r in originals if r['skill'] in TRADES]
    assert recipes == evidence['recipes'] and len(recipes)==167
    bodies = body_models(reg,sec); hosts = host_models(); rows = {x['recipeId']:x for x in reg['recipes']}
    book = {x['recipeId']:x for x in evidence['publicBookBindings']}
    cards = []
    for r in recipes:
        x = rows[r['id']]; assert objsha(r)==x['sourceObjectSha256']
        c = {'recipeId':r['id'], 'name':r['name'], 'visibility':r['visibility'], 'status':STATUS,
             'sourceRecipeIndex':evidence['sourceIndices'][r['id']], 'sourceRecipe':deepcopy(r),
             'sourceObjectSha256':objsha(r), 'sourceAuthoringRegister':deepcopy(x),
             'publicBookBinding':deepcopy(book.get(r['id'])), 'operational':operation(r,x,bodies,sec)}
        c['manuscriptText'] = render_card(c)
        cards.append(c)
    obj = {'schemaVersion':1, 'status':STATUS, 'audience':'director-internal', 'sourceSha256':evidence['sourceSha256'],
           'sourceVerdictSha256':VERDICT_HASH, 'sourceReviewReplyId':'af2a24f6-c967-4aa5-a28e-5c2e9de13cb6',
           'sharedGuide':GUIDE, 'bodyGuide':BODY_GUIDE, 'procedureSections':sec, 'bodyModels':bodies, 'enchantingHostModels':hosts,
           'tinkerInterfaceRegister':read(V/'TINKER_48_INTERFACE_REGISTER.json'),
           'versionAudit':deepcopy(evidence['versionAudit']), 'sourceNameCorrespondences':deepcopy(evidence['sourceNameCorrespondences']),
           'cards':cards, 'exactRecipeApproval':False, 'runtimeImplemented':False, 'balanceApproved':False,
           'openExactReviewIssues':[{'id':'ADV-EDIT-01','scope':'TI-trap original spring',
              'sourceA':'B-04 original primary frame/spring/working mechanism must survive',
              'sourceB':'Body profile primary frame/discharge block; spring/contacts replaceable',
              'candidateHandling':'Require original spring in the draft; preserve both statements for the targeted exact verdict.'}],
           'publicProjectionComplete':False, 'cosmology':'post-verified-push only'}
    outputs = [dest]; dump(dest,obj)
    guide = R/GUIDE
    guide.write_text('# Advanced crafting — internal operating guide\n\n**Authored candidate appendix; exact operational approval pending.** Use with all167 internal cards. These complete procedure sections preserve the final joint source directions verbatim; numeric effects are instantiated on each card. Original sources and the final verdict remain separately preserved. No pending feat/class-card promotion or cosmology interpretation.\n\n'
                     + '\n\n'.join(f"## {s['id']} — {s['title']}\n\n{s['text']}" for s in sec.values()) + '\n', encoding='utf-8'); outputs.append(guide)
    bg = R/BODY_GUIDE
    bg.write_text('# Advanced crafting — internal body catalogue\n\n**Candidate; no exact approval.** All22 defaults/size variants and the finite existing weapon/suit host profiles are in the adjacent internal JSON. B and AC-02/03/09 govern actual physical admission and repair.\n\n'
                  + '\n\n'.join(f"## {bid}\n\n{json.dumps(b['sourceAuthoringProfile'],ensure_ascii=False,indent=2)}\n\n{b.get('openExactReviewIssue','')}" for bid,b in bodies.items())
                  + '\n\n' + '\n\n'.join(f"## {sid} — {sec[sid]['title']}\n\n{sec[sid]['text']}" for sid in ['B-01','B-02','B-03','B-04','B-05'])
                  + '\n\n## Existing alternate hosts\n\nA listed source template requires actual full physical registration before work. No ammunition bundles, shields, natural attacks, net without damage, unsupported special models or already magical equipment.\n\n'
                  + '\n'.join(f"- {x['sourceEquipmentRecord']['name']} ({key}): {val(x['ordinaryPriceGp'])} gp; {x['ordinaryWeightLb']} lb; ordinary B{x['baselineStructuralHP']}; {json.dumps(x['sourceEquipmentRecord']['sourceFields'],ensure_ascii=False)}" for key,x in hosts.items()) + '\n', encoding='utf-8'); outputs.append(bg)
    for trade in TRADES:
        cs = [c for c in cards if c['sourceRecipe']['skill']==trade]
        p = R / f"docs/director-only/{trade.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md"
        assert not p.exists(), p
        p.write_text(f'# {trade} — internal recipe candidates\n\n**{len(cs)} candidates; validation, public projection and exact review pending.** Original source fields remain unchanged.\n\n' + '\n'.join(c['manuscriptText'] for c in cs),encoding='utf-8');outputs.append(p)
    assert all(sha(G/p)==h for p,h in protected.items())
    report = {'status':STATUS, 'authoredAtUtc':datetime.now(timezone.utc).isoformat(), 'cards':167,
              'tradeCounts':{t:sum(c['sourceRecipe']['skill']==t for c in cards) for t in TRADES},
              'visibilityCounts':{v:sum(c['visibility']==v for c in cards) for v in ['public','restricted','director-only']},
              'defaultBodyVariants':22, 'existingHostTemplates':len(hosts), 'completeBookBindings':100,
              'componentOccurrences':sum(len(c['sourceRecipe']['components']) for c in cards),
              'sourceDirectionSections':len(sec), 'classInterfaceCards':len(obj['tinkerInterfaceRegister']['cards']),
              'protectedSourceFilesUnchanged':len(protected), 'outputHashes':{p.relative_to(G).as_posix():sha(p) for p in outputs},
              'recipesApproved':0, 'currentReviewedRecipeCount':520, 'openExactReviewIssueIds':['ADV-EDIT-01'],
              'remainingWork':['Validate all exact internal cards and meaningful creation/state sequences', 'Author complete public guides/cards with exact withholding projection', 'Submit actual complete candidates for separate GPT exact operational review'],
              'sourceInformationDeleted':0, 'githubPushPerformed':False, 'cosmologyReviewed':False}
    dump(A/'ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json',report)
    progress = A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json'
    backup = A/'navigation-before-advanced-internal-authoring';backup.mkdir(exist_ok=True)
    shutil.copy2(progress,backup/progress.name)
    d = read(progress);d.update(status=STATUS, exactCardsAuthored=167,
        readSections=['All final verdict sections AC01–10, EN01–10, RC01–10, SC01–10, TI01–10, B01–05, TD01–18, R01–03, W01–19, K01–05', 'README and full48 interface disposition matrix'],
        readCompleteVerdict=True, sourceRegisterChecksReproduced=True,
        internalAuthoringStatusFile='ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json',
        nextAction='Validate actual internal candidates, author public projection, and return exact complete candidates to GPT with ADV-EDIT-01.')
    dump(progress,d)
    print(json.dumps({k:v for k,v in report.items() if k!='outputHashes'},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
