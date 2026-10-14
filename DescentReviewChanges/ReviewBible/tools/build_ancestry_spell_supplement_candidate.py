"""Author repaired spell dependency candidates; do not promote them to public catalog."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'

def main():
    # name, school, rank, action, range, targets, duration, concentration, components, resolution, effect
    specs=[
    ('Shape Water','Transmutation',0,'Action',5,
     'One contiguous quantity of nonmagical liquid water fitting a 5-foot cube within range; unattended, caster-held or willingly presented/contained. No hostile worn/carried container.',
     'Instantaneous; ordinary gravity resumes after resolution.',False,['V','S'],'No attack or save.',
     'Move the actual water up to 5 feet along an unobstructed path into available space, or reshape its surface harmlessly. Cannot create, freeze, purify, split an occupied body, lift a creature, deal damage, grant a swimming speed or maintain an unsupported shape. Actual potable water remains potable; no abstract Supply is created.'),
    ('Mold Earth','Transmutation',0,'Action',5,
     'Unattended natural nonmagical earth, soil, sand or similarly excavatable ground fitting a 5-foot cube within range.',
     'Instantaneous; the earthworks remain under ordinary gravity and support.',False,['V','S'],'No attack or save.',
     'Excavate, mound or smooth the selected earth into vacant contiguous space up to 5 feet away. Worked stone, solid rock, foundations and a creature-occupied space are excluded. Cannot bury/crush a creature, move valuables separately, or transform earth into a different material. No direct damage. Ordinary terrain consequences can remain, but the cast cannot ignore its foundation exclusion to manufacture structural collapse.'),
    ('Gust','Transmutation',0,'Action',30,
     'One visible Medium-or-smaller creature, one unattended object weighing at most 5 lb, or one harmless air effect in a 5-foot cube within range.',
     'Instantaneous.',False,['V','S'],'Creature: STR save against spell DC; failure permits the push, success no movement. Object/harmless modes need no roll.',
     'Push the selected creature 5 feet directly away from the caster into legal space. No damage or Prone rider; normal destination hazards apply. Forced movement does not provoke Opportunity Attacks unless an exact rule says otherwise. Alternatively move the selected object 5 feet away along a clear path without attack damage; or briefly disperse ordinary smoke in the cube or extinguish one candle. Cannot end magical clouds, defeat weather, create ongoing breathable air or change a sound spell.'),
    ('Minor Illusion','Illusion',0,'Action',30,
     'One stationary object image fitting a 5-foot cube, or one sound originating at a chosen point within range.',
     'Concentration, up to 1 minute.',True,['V','S'],'No initial save. An observer can use an Action for INT (Investigation) against spell DC to discern either mode.',
     'Choose image or sound. The image has no light, weight, smell, touch, movement or actual cover. The sound is a simple noise or short repeated phrase no louder than ordinary speech; cannot impersonate a voice never heard. Physical interaction reveals an image to that observer; an informed observer perceives through it. A believable distraction uses ordinary checks. No Charmed, Frightened, automatic disadvantage, actual control or damaging apparent object.'),
    ('Disguise Self','Illusion',1,'Action',0,
     'Yourself and your worn/carried gear; Self.',
     '1 hour; no concentration. Ends on expiry, legal dispelling or your Action dismissal.',False,['V','S','F'],
     'No initial save. Touch or other physical interaction can reveal a mismatch; an observer can use an Action for INT (Investigation) against spell DC to recognize the disguise.',
     'Change visible appearance. Your actual body, size category, occupied space, anatomy, equipment, voice, reach, statistics, proficiencies, identity records and physical capabilities do not change. The illusion cannot create a mechanically functional body part or make the apparent form occupy a different mechanical size category. An item leaving your possession loses the illusion. A studied identity supplies no unknown mannerisms/passwords. Recasting replaces the prior disguise without stacking. No external one-foot height/anatomical arrangement rule is imported.'),
    ('Water Breathing','Transmutation',3,'Action',60,
     'Up to ten willing creatures you can see within range.',
     'Instantaneous casting; NEW persistent respiration benefit lasts 24 elapsed hours.',False,['V','S','F'],'No attack or save.',
     'Each selected creature retains normal respiration and can breathe water. A creature that does not breathe gains no useful respiration benefit. No swimming speed, depth/temperature immunity, freedom of movement or immunity to suffocation outside breathable air/water. Does not create water or remove poison. The benefit can be legally dispelled on an affected creature individually using original cast rank/school. Recasting refreshes only selected targets, never doubles benefits.'),
    ('Vampiric Touch','Necromancy',3,'Action',0,
     'One creature in actual touch reach; no creature-type exclusion is added.',
     'Instantaneous.',False,['V','S','F'],'One melee spell attack against AC: hit 3d6 necrotic; miss no damage or healing.',
     'After damage resolves, heal yourself floor(actualDamageDealt / 2), once from that attack packet. Use eligible final recipient branches under damage sharing without counting the unsplit parent or overkill. Ordinary healing modifiers, prohibitions and caps apply; actual target defenses determine damage, including for Undead/Constructs. The healing is one secondary result and cannot reproduce this attack or create a second Vampiric Touch heal for the same cast. It grants no continuing repeat-attack permission or concentration. Unrelated eligible triggers retain their own restrictions.'),
    ('Create or Destroy Water','Transmutation',1,'Action',30,
     'One visible 5-foot cube containing open unattended/willingly held containers for creation, or exposed unattended nonmagical water for destruction.',
     'Instantaneous; created water persists ordinarily.',False,['V','S'],'No attack or save.',
     'Choose creation or destruction. Create up to 10 US gallons of clean drinking water in the actual open containers, limited by their real capacity; or destroy up to 10 gallons of qualifying exposed water. No water inside creatures, blood, potions, acid, selective seawater desalination, hostile held containers or magical fluid. No damaging flood/drowning attack. Actual water meets actual drinking needs by volume but never creates food, fuel or abstract Supply.'),
    ('Faerie Fire','Evocation',1,'Action',60,
     'Every creature and unattended object in a 20-foot cube whose center you can see within range; snapshot at resolution.',
     'Concentration, up to 1 minute.',True,['V','S'],'Each creature makes a DEX save; failure is outlined, success unaffected. Unattended objects are outlined without a roll.',
     'Affected subjects shed dim light within 10 feet. Attacks against an outlined creature have advantage if the attacker actually sees it. Invisibility cannot conceal it visually while outlined, but the condition itself is not removed. No vision through walls, removal of total cover, later tracking, damage, repeated save or ally exemption. Later entrants are not affected. Outline ends with concentration, expiry or legal dispelling.'),
    ('Darkness','Evocation',2,'Action',60,
     'A stationary 15-foot-radius sphere centered on a point you can see within range, blocked by total cover.',
     'Concentration, up to 10 minutes.',True,['V','S','F'],'No attack or save.',
     'Opaque magical darkness prevents ordinary vision and darkvision through or within the area; an explicit ability to see through magical darkness still works. Ordinary/nonmagical light cannot illuminate it. A magical light effect illuminates or penetrates it only if that light\'s reviewed source expressly permits magical-darkness interaction, or a later reviewed shared light rule grants it. Darkness neither dispels nor ranks against another magical-light effect merely because of rank. Physical fires and permanent lights are not extinguished. No silence, Blind condition, damage, nonvisual cover or plane effect. Creatures leave normally; the sphere ends with concentration, expiry or legal dispelling.'),
    ('Speak with Plants','Divination',3,'Action',0,
     'Self: communication with actual plants within 30 feet; Cavern Mystic grant is fungi only.',
     '10 minutes; no concentration.',False,['V','S'],'No save for communication; an autonomous intelligent participant is not compelled to cooperate or tell the truth.',
     'Exchange simple spoken questions/responses. Plants relay limited impressions of events they could locally sense in the preceding 24 hours, relative movement and growing conditions. No remote memory network, automatic knowledge of names/species/magic, movement control or guaranteed answer to unknowable questions. Plant creatures retain autonomy. Noncreature plants supply the spell\'s local information procedure without adjudicating souls or ontology.'),
    ('Produce Flame','Evocation',0,'Action',30,
     'Light mode: yourself, one flame in your hand. Attack mode: one visible creature within 30 feet.',
     'Light lasts up to 10 minutes without concentration; attack resolves instantaneously.',False,['V','S'],'Attack mode makes one ranged spell attack: hit 1d8 fire, miss zero. Light mode requires no roll.',
     'Each cast chooses light or attack. Light is harmless to held gear and illuminates bright 10 feet plus dim 10 more. Another light cast replaces your prior flame. An attack is always a new cast and extinguishes your prior spell flame; no prepared flame is required. As an Action, an existing flame can ignite one unattended mundane combustible object in touch reach and then ends; this is not another cast and cannot target hostile worn/carried equipment. Light never ignites automatically. Every actual new cast updates ordinary casting history.'),
    ('Misty Step','Conjuration',2,'Bonus Action',0,
     'Yourself and normally carried gear; one visible unoccupied destination up to 30 feet away that fits your body.',
     'Instantaneous.',False,['V'],'No attack or save.',
     'Teleport to that destination, respecting actual teleport-blocking effects. No passenger or route traversal; ordinary destination hazards apply. Conditions whose attachments remain do not automatically end. A positional restraint may end only if leaving the actual grip/fixture removes its source. No ethereal travel or plane access.'),
    ('Thorn Whip','Transmutation',0,'Action',30,
     'One visible creature within 30 feet; the extended melee reach applies only to this spell.',
     'Instantaneous.',False,['V','S'],'One melee spell attack: hit 1d6 piercing; miss zero and no pull.',
     'On hit, optionally pull a Large-or-smaller target up to 10 feet straight toward you into a fitting unoccupied space, stopping at an obstruction. No passage through creatures/walls, no Prone. Ordinary forced movement and hazard rules apply; no Opportunity Attacks from forced movement absent an exact exception. The whip exists only for resolution, not as a rope, grapple or crafting material. No gear targeting or multiple targets.'),
    ('Goodberry','Transmutation',1,'Action',0,
     'Create ten individually tracked berries in your empty hand or an open willingly held container within touch reach.',
     'Instantaneous creation; each berry\'s magical potency expires 24 elapsed hours from its cast.',False,['V','S'],'No attack or save.',
     'A living creature consumes one berry as an Action, or another creature safely administers one as an Action to a willing/helpless living creature within reach. Consume it exactly once: ordinary healing 1 HP, plus one day\'s ordinary food for that recipient. No water, fuel, shelter or extra nutrition from repeated berries. The healing is flat, not a die; caps/prohibitions do not return the berry. No dead revival or feeding through a sealed/inaccessible mouth or unsafe administration. Potency cannot be stockpiled past its deadline or duplicated by copies. Record the specific food recipients/amount; numerical bundled Supply reduction remains a separate integration dependency, never a second Supply award.'),
    ('Speak with Animals','Divination',1,'Action',0,
     'Self: basic communication with Beasts within ordinary auditory range that can hear you.',
     '10 minutes; no concentration.',False,['V','S'],'No save for communication. Ordinary social checks may govern requests.',
     'Understand and communicate basic spoken ideas within each Beast\'s actual experience/intelligence. No Charmed, domination, forced truth, guaranteed favor or summon. Does not add language proficiency or extend to other creature types.'),
    ('Blood Manipulation','Transmutation',0,'Action',5,
     'Up to one pint of exposed blood outside a living creature within range; unattended, caster-held or willingly presented.',
     'Instantaneous; ordinary gravity and decay follow.',False,['V','S'],'No attack or save.',
     'Move the actual blood up to 5 feet into an open container or shape a harmless pattern. Cannot target internal blood, a hostile worn bandage, hostile held blood or a magic item; create blood; diagnose identity/disease; damage; heal; stabilize; stop Bleed; replenish RP/RC; create viable transfusion/reagents; or animate a creature. Actual material remains without creating a new medical or combat hemomancy procedure.'),
    ]
    catalog={s['name']:s for s in json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']}
    common=('No automatic level scaling, generic upcast or new action budget. Use the actual casting source\'s access, components, costs, shared concentration and Dissonance/Refrain, then the legal interruption window. Countering or later failure refunds no committed use/payment or displaced concentration. Spell attacks use d20 + PB + actual source casting modifier; saves use DC 8 + PB + that modifier. Actual defenses, critical rules, core conditions, ordinary life-state rules and source-specific callbacks retain their scopes. Total cover prevents targeting unless this card expressly allows otherwise. For ancestry casts use ANCESTRY_BACKGROUND_PLAYTEST.md; existing ordinary identities retain their actual class/school/rank access and RP price.')
    spells=[]
    for name,school,rank,activation,range_feet,targets,duration,concentration,components,resolution,effect in specs:
        old=catalog.get(name);identity=old['id'] if old else name.lower().replace(' ','-')
        spells.append({'id':identity,'name':name,'school':school,'rank':rank,'identityType':'existing-catalog' if old else 'new-ancestry-grant-only',
          'activation':activation,'rangeFeet':range_feet,'targets':targets,'duration':duration,'concentration':concentration,
          'components':components,'resolution':resolution,'effect':effect,'scaling':'None.','limitations':common,
          'designNotes':(('PRESERVED existing catalog/Core identity, source placement, action, range and components. NEW: the 24-elapsed-hour persistent respiration benefit and its lifecycle are conference decisions.' if name=='Water Breathing' else 'PRESERVED existing catalog/Core identity, source placement, action, range and components. Explicit operational additions are conference decisions.') if old else 'NEW procedure for a printed ancestry spell name missing from the ordinary catalog. School/rank/effect are expressly authored proposals; no ordinary class access is granted.'),
          'sourceCoreEntries':old['source']['coreEntries'] if old else [],'ordinaryClassAccess':old['classAccess'] if old else {},
          'reviewStatus':'reviewed-authored-playtest-manuscript-four-repairs-applied'})
    assert len(spells)==17 and sum(s['identityType']=='existing-catalog' for s in spells)==7
    out={'status':'reviewed-authored-playtest-manuscript-four-repairs-applied','spells':spells}
    (ROOT/'data/playtest/ancestry_spell_supplement_candidate.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    doc=['# Ancestry spell dependency supplement','','**REVIEWED authored PLAYTEST manuscript.** Seven existing spell identities plus ten new ancestry-grant-only procedures. All four exact-review repairs are applied. The seven existing identities are approved for ordinary catalog promotion; the ten additions grant no ordinary class access. Runtime and balance remain open.', '', '[Ancestry casting route](ANCESTRY_BACKGROUND_PLAYTEST.md) · [Original grant evidence](ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md)', '', 'Existing identities keep their own class access and source school placement. The ten additions grant no ordinary class access. All school/rank choices for those additions are explicit new mechanics. No source record was overwritten.', '', '## Shared resolution', '', common]
    for s in spells:
        doc.extend(['','## '+s['name'], '',s['school']+' · rank '+str(s['rank'])+' · '+s['identityType'], ''])
        for field in ['activation','rangeFeet','targets','duration','concentration','components','resolution','effect','scaling','designNotes']:
            value=s[field];value=', '.join(value) if isinstance(value,list) else str(value)
            doc.extend(['**'+field+':** '+value,''])
    (ROOT/'docs/mechanics/ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
    print('Authored 17 repaired spell candidates: 7 existing IDs, 10 ancestry-grant-only additions; no public promotion.')

if __name__=='__main__':main()
