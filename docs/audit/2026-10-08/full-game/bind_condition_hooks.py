"""Source-qualified hooks accepted across the custom-rider conferences."""
from pathlib import Path
import hashlib
import json

GAME = Path(__file__).resolve().parents[4]
ROOT = GAME / 'DescentReviewChanges/ReviewBible'
PATH = ROOT / 'data/playtest/custom_condition_bindings.json'
p = json.loads(PATH.read_text(encoding='utf-8'))
classes = {}
prefix = 'docs/audit/2026-10-08/full-game/'

def ref(owner, key):
    path=f'data/public/class_playtests/{owner}.json'
    if owner not in classes:
        classes[owner]=json.loads((ROOT/path).read_text(encoding='utf-8'))
    d=classes[owner]
    if isinstance(key,int):
        t=d['engine'][key]
        return dict(kind='engine',path=path,engineIndex=key,text=t,textSha256=hashlib.sha256(t.encode()).hexdigest())
    c=next(c for c in d['cards'] if c['id']==key)
    return dict(kind='card',path=path,cardId=key,originalDisplayName=c['name'],
                effect=c['effect'],duration=c['duration'],activation=c['activation'],cost=c['cost'],
                rangeAndTarget=c['rangeAndTarget'],frequency=c['frequency'],
                sourceObjectSha256=hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False).encode()).hexdigest())

hooks=[]
def hook(ident,rule,owner,keys):
    hooks.append(dict(id=ident,rule=rule,sourceReferences=[ref(owner,k) for k in keys],
        reviewEvidence=[prefix+'GPT_CUSTOM_RIDER_FIRST_REVIEW.md',prefix+'GPT_CUSTOM_RIDER_SCOPE_REVIEW.md',prefix+'GPT_PERIODIC_PROFILE_REVIEW.md',prefix+'GPT_PERIODIC_REFRESH_CLOSURE.md']))

hook('cleric.judging-light','Active, unsuppressed eligibility.weakened or classification.curse qualifies; no owner restriction. A Curse class engine name or unclassified flavor text does not qualify. One added dice packet per qualifying Smite, not per condition.','cleric',['cleric.base.judging-light'])
hook('thief.sneak-condition','Owned active family.bleeding, core.poisoned or thief.crippled can satisfy the condition route. Own legal multiclass effects qualify; the remaining weapon, turn, disadvantage and trigger requirements still apply.','thief',[0])
hook('thief.vile-tactics','Active Bleeding, Poisoned or Crippled target as stated in the card trigger. No invented owner restriction; several conditions do not multiply bonus.','thief',['thief.hero.blackguard.vile-tactics'])
hook('warrior.terror-engine','Only this owner\'s Warrior-feature Shaken, Frightened or ACTIVE Disoriented. Count creatures, not effect records. At least two hostile creatures within 30 feet; pending Disoriented does not qualify.','warrior',['warrior.supplement.terror-engine'])
hook('druid.snow-leopard','Explicit hostile Speed reduction or root tagged eligibility.slowed-foe qualifies. Prone, difficult terrain, cargo, Exhaustion, Grappled or Restrained alone do not.','druid',['druid.hero.winterfang.snow-leopard'])
hook('warrior.mythic-carapace','Blocks family.bleeding, core.poisoned and family.ongoing-fire. This does not grant fire-damage immunity or blanket poison-effect immunity. Damage reduction and mutation refresh keep exact card limits.','warrior',['warrior.supplement.mythic-carapace'])
hook('dragoon.wyrmhide','Advantage only on CON saves against registered Bleed, ongoing fire or Core Poisoned. It does not convert DEX extinguishing saves into CON saves or grant condition immunity.','dragoon',['dragoon.hero.dragon-guardian.wyrmhide'])
hook('crimson.bleed-engine','Technical Crimson Bleed counters, spreading, detonations, Blood Mark prerequisites and named engine benefits require this owner\'s Crimson-engine instances. Broad end-all wording is separately bound. No allied healing replacement is hostile Bleed.','crimson-agent',[2,3,'crimson-agent.base.blood-tithe','crimson-agent.arch.bloodbound-edge','crimson-agent.hero.thirstborn.blood-frenzy','crimson-agent.hero.thirstborn.hemorrhagic-plague','crimson-agent.hero.thirstborn.exsanguinate'])
hook('crimson.hemostasis','Arch Hemostasis ends all Bleed on the target irrespective of owner, subject to an expressly stated protected cure exception. Healing remains its printed fixed roll even with no Bleed. Bloodweaver Hemostasis instead replaces a new allied application with one bounded healing effect, never a hostile Bleed.','crimson-agent',['crimson-agent.arch.hemostasis','crimson-agent.hero.bloodweaver.hemostasis'])
hook('thief.persistent-bleed','Actual qualifying trigger refreshes one existing owned record, max(current remaining,2); if owner has Prolonged and underlying base duration is exactly2, replace2 with4. Do not revive expired records, change dice, create instances or exceed an express hard cap.','thief',['thief.hero.shadowblade.persistent-bleed'])
hook('thief.prolonged-suffering','Owner-created Bleeds with printed base duration exactly2 use4 on application and qualifying refresh. Includes another legal class owned by same character; excludes base3 Crimson and Blood Curse. Base duration is not a hard cap; duration modifiers do not add unless explicit.','thief',['thief.hero.blackguard.prolonged-suffering'])
hook('mage.arch-elemental-mastery','Adds one tick to a reviewed Fire Burn from a Mage card explicitly tagged focus, or an explicit Focus-Burn reference. Includes Focus passive, Inferno Lance, Elemental Bolt and Elemental Surge reference. Excludes Fusion and Cascade. Group arbitration still applies.','mage',['mage.arch.elemental-mastery','mage.base.fire.fire','mage.base.elemental-bolt','mage.arch.elemental-surge'])
hook('oracle.burning-blood-boon-ii','An eligible ongoing fire rider from that paid Revelation use cannot be ended by mundane extinguishing. This does not create a new ongoing fire rider, convert other damage to a Burn, or protect unrelated effects.','oracle',['oracle.supplement.burning-blood.burning-blood-boon-ii'])

spell_path='data/public/spell_playtests/catalog.json'
s=next(s for s in json.loads((ROOT/spell_path).read_text(encoding='utf-8'))['spells'] if s['id']=='seal-minor-wound')
hooks.append(dict(id='spell.seal-minor-wound',rule='Select one eligible ordinary Bleed record and end that record. Shaman Blood Curse currently qualifies as Bleed; this does not remove an independently present curse, poison package, Wound or other affliction. The alternate stabilization choice restores no HP.',
    sourceReferences=[dict(kind='operational-spell',path=spell_path,spellId=s['id'],operational=s['operational'],operationalSha256=hashlib.sha256(json.dumps(s['operational'],sort_keys=True,ensure_ascii=False).encode()).hexdigest())],
    reviewEvidence=[prefix+'GPT_CUSTOM_RIDER_SECOND_REVIEW.md',prefix+'GPT_PERIODIC_PROFILE_REVIEW.md']))
p['hooks']=hooks
for d in p['definitions']:
    if 'periodic' in d:
        d['periodic']['baseDurationTicks']=d['periodic']['ticks']
        d['periodic']['refreshNeverShortens']=True
        d['reviewEvidence']=list(dict.fromkeys(d['reviewEvidence']+[prefix+'GPT_PERIODIC_REFRESH_CLOSURE.md']))
        if 'family.ongoing-fire' in d['familyTags']:
            d['cure']['mundaneScope']='all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive'
p['openIssues']=[x for x in p['openIssues'] if not x.startswith('Confirm Prolonged')]
PATH.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Bound {len(hooks)} source-qualified hooks; registry remains {p["status"]}.')
