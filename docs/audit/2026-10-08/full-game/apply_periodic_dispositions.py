"""Apply accepted periodic conference decisions to the preserved review overlay."""
from pathlib import Path
import json

GAME = Path(__file__).resolve().parents[4]
ROOT = GAME / 'DescentReviewChanges/ReviewBible'
PATH = ROOT / 'data/playtest/custom_condition_bindings.json'
p = json.loads(PATH.read_text(encoding='utf-8'))
review = 'docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md'
by_id = {d['mechanicalId']: d for d in p['definitions']}
for d in p['definitions']:
    if 'periodic' not in d:
        continue
    d['status'] = 'reviewed provisional periodic profile; registry-wide review pending'
    if review not in d['reviewEvidence']:
        d['reviewEvidence'].append(review)
    tags = d['familyTags']
    if 'family.bleeding' in tags:
        d['cure'] = {
            'ordinaryConditionRemoval': True, 'specialCureRequired': False, 'artifactLevel': False,
            'magicalHealingEndpoint': 'end', 'magicalHealingScope': 'every eligible active record on recipient',
            'positivePotentialRequired': True, 'actualHpGainRequired': False,
            'medicine': {'activation':'Action', 'actor':'self or adjacent helper', 'ability':'WIS', 'skill':'Medicine',
                         'dcPrecedence':['printed cure DC','recorded applying effect/class/spell DC','10'],
                         'scope':'one eligible record selected before roll'},
            'explicitRemoval':'Use remover exact one/all/owner restrictions.',
            'provenance':'NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.'}
        if d['mechanicalId'] == 'crimson-agent.bleed':
            d['cure']['kitAction'] = {'uses':1,'actor':'self or adjacent helper', 'automatic':True,
                'scope':'all Crimson-engine Bleed instances from one source owner on this victim',
                'provenance':'Printed automatic kit endpoint; NEW one-use consumption.'}
        if d['mechanicalId'] == 'dragoon.bleed':
            d['cure']['kitAction'] = {'uses':1,'actor':'self or adjacent helper', 'automatic':True,
                'scope':'selected Dragoon Bleed record','provenance':'Printed kit endpoint; NEW one-use consumption.'}
        if d['mechanicalId'] == 'shaman.blood-curse.bleed':
            d['cure']['magicalHealingEndpoint'] = 'saveToEnd'
            d['cure']['magicalHealingSave'] = {'ability':'CON','dc':'applying Shaman class DC','scope':'one save per active Blood Curse record'}
            d['cure']['medicine']['dcPrecedence'] = ['applying Shaman class DC']
            d['cure']['provenance'] = 'Printed Medicine/healing-save endpoints; reviewed ordinary explicit-removal eligibility.'
    elif 'family.ongoing-fire' in tags:
        d['cure'] = {'ordinaryConditionRemoval':True,'ordinaryExtinguishable':True,
            'mundaneMethods':['Action by self or adjacent helper','full immersion of all burning portions'],
            'mundaneScope':'all eligible ordinary-extinguishable attached-fire records on chosen creature; scope clarification pending',
            'endingSave':{'ability':'DEX','dcPrecedence':['printed ending DC','recorded source DC','10'],
                         'marker':'end of regular target turn after any end-turn tick',
                         'eligibility':'record still active with at least one future scheduled tick remaining',
                         'scope':'this record only'},
            'sourceException':'A printed prohibition on mundane extinguishing disables those mundane methods only.',
            'provenance':'NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.'}
    else:
        d['cure'] = {'ordinaryExtinguishable':False,'corePoisonedRemovalApplies':False,
            'underlyingPoisonRemoval':'Only an explicitly reviewed cure covering active poison recipe effects can remove remaining recipe riders.',
            'expiry':'Two scheduled ticks; recipe can be refreshed under Thief engine rules.'}
    d['periodic']['outsideInitiative'] = 'Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.'

by_id['crimson-agent.bleed']['periodic']['defaultInstanceCap'] = 1
by_id['crimson-agent.bleed']['periodic']['exceptionInstanceCap'] = {'feature':'crimson-agent.arch.blood-echo','cap':2}
by_id['crimson-agent.bleed']['periodic']['hardRemainingTickCap'] = 5
by_id['mage.elemental-bolt.burn']['integrationDecisions'] = [
    'Explicit new attached-fire classification in the Mage Fire Focus stack group.',
    'Its card is explicitly tagged focus: Arch Elemental Mastery adds one tick. Elemental Fusion and Cascade lack that tag and do not receive this upgrade.']
for ident in ['mage.fire-focus.burn','mage.inferno-lance.burn','mage.elemental-bolt.burn']:
    by_id[ident]['periodic']['archElementalMasteryAdditionalTicks'] = 1
by_id['thief.ashblood.periodic']['integrationDecisions'] = [
    'Internal poison-recipe delayed fire; explicitly excluded from family.ongoing-fire. Can coexist with a Burn-family tick.',
    'Poison damage immunity blocks poison damage only; Core Poisoned immunity blocks only actual Poisoned components. Explicit immunity to poison effects/toxins is checked separately against the application.',
    'Failed recipe save still required; critical no-HP-recovery ends end next regular turn separately from the two-tick fire.',
    'One recipe instance per owner/target and maximum two different ongoing poison recipes from that owner.']
by_id['thief.vein-cutter.bleed']['integrationDecisions'] = [
    'Specific effect preserves two Bleed ticks despite shorter general duration field.',
    'Speed -10 lasts through end next regular target turn; -1 next attack damage is consumed or expires at that same endpoint.',
    'Consumes a prepared poison without its normal recipe effect and does not occupy a normal recipe-instance slot.']
by_id['shaman.bloodroot.bleed']['periodic']['damageType'] = 'slashing'
by_id['shaman.bloodroot.bleed']['effect'] = '1d4 slashing damage at end of target next regular turn. Initial zone damage remains necrotic.'
for d in p['definitions']:
    # Repair only explicitly observed prose gaps; never split dice notation.
    for field in ['effect','ending']:
        for old,new in [('minimum0','minimum 0'),('Maximum2','Maximum 2'),('at most3','at most 3'),
                        ('within2 tiles','within 2 tiles'),('by1','by 1'),('adds1d8','adds 1d8'),
                        ('up to5','up to 5'),('Speed0','Speed 0'),('range30ft','range 30 feet')]:
            d[field] = d[field].replace(old,new)
p['openIssues'] = [
    'Confirm Prolonged Suffering refresh precedence and all-record mundane extinguishing scope.',
    'Complete source-qualified hook references and remaining root/slow/curse/disease/mark metadata.',
    'Resolve remaining common round-marker endpoints.',
    'Semantically classify all active class/spell rider references; reference integrity does not prove exhaustive semantic coverage.']
PATH.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Applied reviewed periodic profiles; full registry remains IN_PROGRESS.')
