"""Read-only manuscript handoff checks, not a game/runtime or human teaching test."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse, hashlib, json, re, sys
sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path('/mnt/data/onboarding_exact_reviewer/submitted'), help='Root of the unmodified extracted submitted ZIP')
parser.add_argument('--archive', type=Path, default=Path('/mnt/data/DD_Onboarding_and_Design_Charter_Exact_Review_v2.zip'))
parser.add_argument('--out', type=Path, default=Path('/mnt/data/onboarding_exact_reviewer/evidence'), help='Reviewer reports only; use a location outside submitted sources')
args = parser.parse_args()
ROOT = args.root.resolve()
RB = ROOT / 'DescentReviewChanges/ReviewBible'
A = ROOT / 'docs/audit/2026-10-08/full-game'
OUT = args.out.resolve()
if OUT == ROOT or ROOT in OUT.parents:
    parser.error('--out must be outside the immutable submitted source tree')
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(RB / 'tools'))
import character_foundation as cf
import core_playtest_rules as core
import spell_playtest_rules as spells
checks=[]
def eq(name, actual, expected, kind='reference arithmetic'):
    checks.append({'id': name, 'kind':kind, 'pass':actual==expected,
                   'actual':actual, 'expected':expected})
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
archive=args.archive.resolve()
eq('archive.bytes',archive.stat().st_size,2985983,'integrity')
eq('archive.sha256',sha(archive),'ef1e3c0c4d865de2295662fa94e13ba25f2be250ff918b3c133779445ded2302','integrity')
manifest=load(ROOT/'FILE_MANIFEST.json')
eq('manifest.count',len(manifest),72,'integrity')
for n,m in manifest.items():
    eq('payload.'+n,{'sha256':sha(ROOT/n),'bytes':(ROOT/n).stat().st_size},m,'integrity')
p=load(A/'FIRST_BARD_WALKTHROUGH_PREPARATION.json')
a=load(RB/'data/playtest/ancestry_background_candidate.json')
h=next(x for x in a['ancestries'] if x['id']=='human')
v=next(x for x in h['variants'] if x['id']=='nomadic-human')
bg=next(x for x in a['backgrounds'] if x['id']=='battlefield-medic')
eq('snapshot.human',p['humanSource'],h,'selected-source equality')
eq('snapshot.nomadic',p['selectedVariant'],v,'selected-source equality')
eq('snapshot.background',p['backgroundSource'],bg,'selected-source equality')
b=load(RB/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json')
bcards={x['id']:x for x in b['cards']}
for x in p['selectedBardCards']:
    eq('snapshot.card.'+x['id'],x,bcards[x['id']],'selected-source equality')
    eq('selected.minimum.'+x['id'],x['minimumClassLevel'],1,'selected-source membership')
    eq('selected.active.'+x['id'],x['kind'],'active','selected-source membership')
eq('selected.Bard.actives',len(p['selectedBardCards']),4,'selected-source membership')
cat=load(RB/'data/public/spell_playtests/catalog.json')
smap={x['id']:x for x in cat['spells']}
for x in p['selectedOrdinarySpells']:
    eq('snapshot.spell.'+x['id'],x,smap[x['id']],'selected-source equality')
    eq('access.'+x['id'],spells.access_for(smap[x['id']],'Bard',1),p['selectedSpellAccess'][x['id']],'selected-source equality')
f=load(RB/'data/playtest/character_foundation.json')
profiles={x['class']:x for x in f['classes']}
assigned=p['assignedScores']
eq('assigned.array',sorted(assigned.values()),sorted(f['standardArray']))
scores={k:assigned[k]+h['abilityBonuses'].get(k,0)+v['abilityBonuses'].get(k,0) for k in assigned}
eq('scores',scores,{'STR':11,'DEX':15,'CON':15,'INT':13,'WIS':10,'CHA':16})
mods={k:cf.ability_modifier(v) for k,v in scores.items()}
eq('modifiers',mods,p['modifiers'])
eq('HP.1',cf.base_maximum_hp(profiles,[{'class':'Bard','base':8}],15),p['firstLevelHP'])
eq('HP.2',cf.base_maximum_hp(profiles,[{'class':'Bard','base':8},{'class':'Bard','base':5}],15),p['levelTwoHP'])
eq('PB',cf.proficiency_bonus(1),2)
eq('RP.1',cf.merged_rp(profiles,{'Bard':1},['Bard']),p['firstLevelRP'])
eq('RP.2',cf.merged_rp(profiles,{'Bard':2},['Bard'])['maximum'],3)
eq('level.currentHP',cf.clamp_after_capacity_change(7,17),7)
eq('level.currentRP',cf.clamp_after_capacity_change(0,3),0)
selected_skills=['Acrobatics','Investigation','Performance','Perception','Survival','Medicine','Insight']
eq('skills.unique',len(set(selected_skills)),7)
eq('class.skills.eligible',all(x in profiles['Bard']['skillOptions'] for x in selected_skills[:3]),True)
eq('saves',profiles['Bard']['savingThrowProficiencies'],['DEX','CHA'],'selected-source membership')
eq('performance.attack',2+mods['CHA'],5)
eq('performance.DC',8+2+mods['CHA'],13)
eq('spell.Limit',max(4,2+2+max(0,mods['CHA'])),7)
eq('leather.AC',11+mods['DEX'],13)
eq('dagger.attack',2+mods['DEX'],4)
eq('dagger.damage.flat',mods['DEX'],2)
e=load(RB/'data/playtest/equipment_acquisition_candidate.json')
eitems={x['id']:x for x in e['items']}
weights=[]
for i,x in enumerate(p['inventory']):
    sr=x['sourceRecord']
    eq('snapshot.inventory.'+str(i),sr,eitems[sr['id']],'selected-source equality')
    w=F(str(sr['unitWeightLb']))*x['quantity']
    eq('inventory.weight.'+sr['id'],str(w),str(F(x['totalWeightLb'])))
    weights.append(w)
coins=F(10,50)
weight=sum(weights,F(0))+coins
eq('inventory.total',str(weight),str(F(294,5)))
eq('inventory.Load',str(weight/10),str(F(147,25)))
eq('inventory.half.capacity',str(F(scores['STR'],2)),str(F(11,2)))
eq('inventory.physical.capacity',15*scores['STR'],165)
eq('inventory.burden',0<weight/10 and F(scores['STR'],2)<=weight/10<=scores['STR'],True)
eq('inventory.Speed',30-10,20)
kit=next(x for x in e['classKits'] if x['class']=='Bard')
pack=next(x for x in e['packs'] if x['id']==kit['packId'])
class_qty=Counter()
for x in [*kit['contents'],*pack['contents']]:class_qty[x['itemId']]+=x['quantity']
eq('inventory.class.weight',str(sum(F(str(eitems[k]['unitWeightLb']))*q for k,q in class_qty.items())),str(F('50.5')))
eq('inventory.background.weight',str(weight-F('50.5')),str(F('8.3')))
eq('inventory.no.tinderbox',any('tinderbox' in k for k in class_qty),False)
inside=['adventuring-gear.clothes-costume','adventuring-gear.candle','adventuring-gear.rations-1-day','tools.disguise-kit']
packweight=sum(F(str(eitems[k]['unitWeightLb']))*class_qty[k] for k in inside)+F(1)
eq('inventory.backpack.contents',str(packweight),str(F('22.5')))
eq('inventory.pouch.contents',str(F('0.1')+coins),str(F('0.3')))
eq('roll.Perception11',core.task_check(11,2,12),p['rollExamples']['perceptionSuccess'])
eq('roll.Perception1',core.task_check(1,2,12),p['rollExamples']['perceptionNaturalOne'])
eq('roll.Verse7',core.attack_roll(7,5,12),p['rollExamples']['verseHit'])
eq('roll.Note7',core.saving_throw(7,0,13),p['rollExamples']['noteFailedSave'])
life,events=core.damage_event(core.LifeState(maximum_hp=10,hp=10),3)
eq('Mira.damage.HP',life.hp,7)
eq('Mira.damage.WoundSaves',events['woundSaves'],0)
eq('Mira.damage.InstantDeath',events['instantDeath'],False)
eq('Mira.Verse.targetHP',30-4,26)
eq('Mira.Echo.copy',4//2,2)
eq('Mira.Echo.targetHP',26-4//2,24)
eq('Mira.RP.after.two.paid.performances',2-1-1,0)
eq('Mira.recharge.Echo.turn2',max(0,2-1),1)
eq('Mira.recharge.Echo.turn3',max(0,2-2),0)
# Numerical healing checks use explicitly ordinary, unblocked fixtures; not source legality authentication.
eq('Chant.ordinary.healing',core.heal(core.LifeState(maximum_hp=10,hp=3),4+3).hp,10)
eq('Chant.Critical.counterexample',core.heal(core.LifeState(maximum_hp=10,hp=3,wounds=(None,None,None)),7).hp,9)
repertoire=set(p['selectedSpellAccess'])
kwargs=dict(available_spell_ids=repertoire,rp=2,max_rp=2,dissonance=0,proficiency=2,casting_modifier=3)
eq('Shield.quote',spells.quote_cast(smap['shield'],'Bard',1,**kwargs),p['shieldQuote'])
try: spells.quote_cast(smap['shield'],'Bard',1,**dict(kwargs,rp=1))
except spells.SpellRuleError as err: actual=str(err)
else: actual='incorrectly allowed'
eq('Shield.unaffordable',actual,'Insufficient RP')
eq('Shield.AC',13+5,18)
eq('Shield.attack15.misses',15<18,True)
d=0;prev=None;ref=0;seq=[]
for choice in ['mage-light','message','message',None,'message']:
    if choice is None:d=max(0,d-1)
    else:
        q=spells.quote_cast(smap[choice],'Bard',1,**dict(kwargs,dissonance=d,previous_spell_id=prev,previous_refrain=ref))
        d=q['dissonanceBeforeClassInterface'];prev=choice;ref=q['refrain']
    seq.append(d)
eq('ordinary.spell.sequence',seq,[0,0,1,0,2])
eq('retune.uncapped',spells.retune_amount(2,3),4)
eq('retune.capped',min(2,spells.retune_amount(2,3)),2)
for dmg,expected in [(12,False),(13,True)]:
    _,ev=core.damage_event(core.LifeState(maximum_hp=10,hp=3),dmg,wound_natural=20)
    eq('instant.death.'+str(dmg),ev['instantDeath'],expected)
# Fulfilled crafting gate: check included final files and receipt linkage, not repeat crafting review.
receipt=load(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json')
eq('promotion.recipes',receipt['aggregateReviewedRecipes'],687,'receipt continuity')
eq('promotion.public',receipt['publicReviewedRecipes'],433,'receipt continuity')
eq('promotion.report.hash',sha(ROOT/receipt['prepromotionValidation']),receipt['prepromotionValidationSha256'],'receipt continuity')
for n,hsh in receipt['finalArtifactHashes'].items(): eq('promotion.final.'+n,sha(ROOT/n),hsh,'receipt continuity')
# Link availability is reported, not presumed repository failure or source unavailability.
manuscripts=[RB/'docs/playtest'/f'{n}.md' for n in ['FIRST_BARD_WALKTHROUGH','SESSION_ZERO_PLAYTEST','NEWCOMER_PLAYER_GUIDE','NEWCOMER_DIRECTOR_GUIDE','RESONANCE_CHEATSHEET']]+[A/'DESIGN_CHARTER_CANDIDATE.md']
links=[]
for path in [*manuscripts,ROOT/'START_HERE.md']:
    for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
        if '://' in url or url.startswith('#'):continue
        target=(path.parent/url.split('#',1)[0]).resolve()
        links.append({'from':str(path.relative_to(ROOT)),'target':url,'presentInReviewArchive':target.exists()})
report={'scope':'Read-only payload integrity, selected source equality and finite reference arithmetic. Not gameplay/runtime, campaign authentication, human teaching, or balance verification.',
        'checks':checks,'counts':dict(Counter(c['kind'] for c in checks)),
        'totalChecks':len(checks),'failedChecks':[c for c in checks if not c['pass']],
        'links':links,'absentArchiveLinkTargets':sorted(set(x['target'] for x in links if not x['presentInReviewArchive'])),
        'semanticFindingsSeparate':True,'sourceFilesChanged':False}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'ONBOARDING_READ_ONLY_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','links']},indent=2,ensure_ascii=False))
