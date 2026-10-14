"""Prepare nonactive candidate records from the actual notebook proposals.

This deliberately writes candidate_*.json, never batch_*.json. Promotion is a
separate operation after independent implementation review.
"""
from pathlib import Path
import json, re, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges'/'ReviewBible'
assert not (ROOT/'data/playtest/spell_drafts/batch_transformations.json').exists(), 'Historical candidate authoring is closed; edit/review the promoted batch explicitly instead of resetting it.'
raw=json.loads((HERE/'TRANSFORMATION_SPELL_FIRST_PROPOSALS.json').read_text(encoding='utf-8'))
cards=raw['spells']
shared=(' Use the complete TRANSFORMATION_SPELL_PLAYTEST.md procedure and finite spell_form_profiles.json register. '
        'Preflight all targets, anatomy, space and access before committing Action/RP; commit ends your old concentration '
        'before counters or saves. A failed or countered new spell does not restore old concentration. '
        'An anatomy from another source is replaced only on actual success. No displaced form remains underneath.')
for c in cards:
    c['implementationStatus']='candidate; independent implementation review pending'
    c['procedureReference']='docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md'
    if c['id']=='harmonic-bulwark':
        c['effect']=('The chosen willing recipient receives a temporary-HP offer equal to 5 times credited RP. '
                    'Credited RP is actual base RP paid after exact legal base-cost reductions plus chosen additional X from0..PB. '
                    'X cannot be discounted. Ordinary surcharges never count toward credited RP. '
                    'Use canonical ordinary-cast pricing; Refrain changes post-cast Dissonance and is not a new RP surcharge.')
        c['limitations']+=' Choose X before commitment. Commit Action plus quoted casting payment plus X before countering or arbitration; no post-commit refund. A countered spell offers nothing.'
    else:
        c['resolution']+=shared
        c['limitations']+=(' The subject owns supplied natural-attack events; the original caster supplies attack statistics. '
                           'These attacks are not spell casts or automatically caster spell-damage/kill triggers. '
                           'A Druid cannot enter Shapeshift while a spell anatomy is active. '
                           'Temporary lower-rank spells cannot replace higher-rank anatomy. '
                           'Only a successful True Polymorph or an exact named exception can replace permanent True anatomy.')
        c['duration']+='; absolute checkpoint at casting timestamp +60 seconds, never extended by extra turns'
        c['limitations']+=(' Antimagic suppresses the same record while concentration and its absolute clock continue; '
                           'True Polymorph can stabilize while suppressed. Suppression never frees an object-companion slot or resets gear. '
                           'Creature-origin type tags remain unchanged; profile names confer no creature type. '
                           'Every supplied attack has5-foot reach. Original anatomical abilities unavailable in the selected profile do not persist underneath it. '
                           'A successful new transformation closes the old record and atomically restores/recaptures still-existing original gear; '
                           'internal profile switches instead retain the same meld set and drop incompatible external gear. '
                           'Mandatory reversion returns at the same anchor; blocked placement is referred to canonical geometry without automatic teleport or crushing damage.')
        c['limitations']+=(' Original melded gear remains inaccessible under antimagic. A willing temporary creature-origin recipient can use its regular-turn rejection Action while suppressed if its root creature anatomy can act; object-origin identities gain no rejection right. No generic magical-attack bypass flag is granted.')
    if c['id']=='shapechange':
        c['resolution']+=' No internal switch on the casting turn or an extra turn; first switch is the next original regular turn, then at most one on each later original regular turn.'
    if c['id']=='mass-polymorph':
        c['resolution']+=' Before payment validate O/O, O/T, T/O and T/T footprint compatibility for every pair of targets; saves resolve independently and successful anatomy changes apply simultaneously.'
    if c['id']=='true-polymorph':
        c['concentration']=True
        c['concentrationAfterStabilization']=False
        c['scaling']+=' Snapshot PB and source class as well. All True Polymorph supplied attack/DC values use this snapshot from casting, including shaping.'
        c['limitations']+=(' Object origin and earliest physical identity persist through every transformation chain. '
                            'Object-origin creatures never gain a humanoid profile, soul, ordinary healing, resurrection or biological/class/rest resources. '
                            'Use one actual structural HP ledger; structural0 destroys the object and ends its creature manifestation. '
                            'Creature-origin object anatomy is actionless, not automatically Incapacitated. '
                            'Allowed object templates are barrier/slab, ramp/wedge, open-container, static-furniture or simple-one-piece-tool; '
                            'no actuated mechanism, magical or valuable output. Output size Tiny..Large and within one category of input; '
                            'output mass cannot exceed recorded input or earliest origin mass; value cannot exceed original documented ceiling. '
                            'Corpses/remains, magical/attuned/carried/worn/attended/structural objects and undefined structural durability are ineligible. '
                            'An object-creature reserves its original caster slot on successful shaping; suppression/control change never frees it. '
                            'At the60-second boundary finish damage, resolve due repeat save, then stabilize only surviving links.')
        c['limitations']+=(' Replacing an active True object anatomy requires legal True replacement, not fresh nonmagical/unattended outside-object admission. Creature-origin people retain their CON save against unwilling creature-profile recasts and must consent to object-profile recasts. Returning them to creature anatomy grants no companion slot.')

profiles=[]
for p in raw['profiles']:
    move={k:int(v) for k,v in re.findall(r'(walk|fly|swim|burrow) (\d+)',p['movement'])}
    if 'burrow' in move:move['burrowLooseSoil']=move.pop('burrow')
    if 'hover' in p['movement']:move['hover']=True
    ac=p['ac']
    ac={'mode':'normal','amount':0} if ac=='formNormalAC' else {'mode':'floor','amount':int(re.search(r',(\d+)',ac).group(1))} if ac.startswith('max(') else {'mode':'fixed','amount':int(ac)}
    dice,damage=p['naturalAttack'].split('+M ')
    resist=[x for x in ('lightning','fire','cold') if x+' resistance' in p['passiveAnatomy']]
    profiles.append({'id':p['id'],'tier':p['tier'],'size':p['size'],'movement':move,
                     'speech':p['speechHands']=='yes / yes','hands':p['speechHands']=='yes / yes',
                     'ac':ac,'attack':{'dice':dice,'damageType':damage,'category':'natural/form','count':1,'reachFeet':5},
                     'resistances':resist,'waterBreathing':'water breathing' in p['passiveAnatomy'],
                     'sourceProposal':p,'provenance':'NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block'})
data=ROOT/'data'/'playtest'
(data/'spell_drafts'/'candidate_transformations.json').write_text(json.dumps({'status':'CANDIDATE; independent implementation review pending','spells':cards},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(data/'spell_form_profiles.json').write_text(json.dumps({'status':'candidate; implementation review pending','profiles':profiles,
    'evidence':[{'path':n,'sha256':hashlib.sha256((HERE/n).read_bytes()).hexdigest()} for n in
    ('GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md','GPT_TRANSFORMATION_SPELL_BOUNDARIES.md','GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md')]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 5 inactive spell candidates and 12 normalized candidate profiles; active catalog unchanged.')
