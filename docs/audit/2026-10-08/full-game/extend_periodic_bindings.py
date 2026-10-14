"""Authored integration additions; snapshots preserve the active source objects.

Run from any directory. This updates only the provisional review registry.
It is not a source-book migration, and never marks the registry complete.
"""
from pathlib import Path
import hashlib
import json

GAME = Path(__file__).resolve().parents[4]
ROOT = GAME / 'DescentReviewChanges/ReviewBible'
PATH = ROOT / 'data/playtest/custom_condition_bindings.json'
packet = json.loads(PATH.read_text(encoding='utf-8'))
definitions = {d['mechanicalId']: d for d in packet['definitions']}
classes = {}
EVIDENCE = 'docs/audit/2026-10-08/full-game/'


def source(owner, key):
    path = f'data/public/class_playtests/{owner}.json'
    if owner not in classes:
        classes[owner] = json.loads((ROOT / path).read_text(encoding='utf-8'))
    data = classes[owner]
    if isinstance(key, int):
        text = data['engine'][key]
        return dict(kind='engine', path=path, engineIndex=key, text=text,
                    textSha256=hashlib.sha256(text.encode()).hexdigest())
    card = next(c for c in data['cards'] if c['id'] == key)
    return dict(kind='card', path=path, cardId=key, originalDisplayName=card['name'],
                effect=card['effect'], duration=card['duration'],
                sourceObjectSha256=hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False).encode()).hexdigest())


def periodic(ident, name, owner, keys, family, dice, count, marker,
             group=None, cap=1, damage_type=None, notes=()):
    # A pending proposed cure is explicit rather than silently inherited.
    record = definitions.get(ident, {})
    record.update(mechanicalId=ident, displayName=name, kind='periodic-rider',
        status='source-profile drafted; exact periodic-profile conference pending',
        familyTags=[family] if family else [],
        effect=f'{dice} {damage_type or ("fire" if family == "family.ongoing-fire" else "physical")} damage at {marker} of each of the next {count} regular target turns.',
        ending=f'After {count} due ticks, or an applicable ending method. Losing arbitration consumes a due tick.',
        stacking='Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.',
        immunityRule='Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.',
        applicationSources=[source(owner, key) for key in keys],
        periodic={'dice': dice, 'damageType': damage_type or ('fire' if family == 'family.ongoing-fire' else 'applying-physical-hit-or-slashing'),
                  'ticks': count, 'marker': f'target.regular-turn.{marker}',
                  'stackGroupTemplate': (group or ident)+':<ownerCharacterId>',
                  'maximumDamagingInstancesPerGroup': cap,
                  'replacementTiming': True, 'extraTurnTicks': False},
        cure={'status': 'explicit profile cure endpoint pending conference'},
        integrationDecisions=list(notes),
        reviewEvidence=[EVIDENCE+'GPT_CUSTOM_RIDER_FIRST_REVIEW.md', EVIDENCE+'GPT_CUSTOM_RIDER_SCOPE_REVIEW.md',
                        EVIDENCE+'GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md', EVIDENCE+'CODEX_PERIODIC_PROFILE_CONFERENCE.md'])
    definitions[ident] = record


periodic('crimson-agent.bleed','Crimson Bleed','crimson-agent',[2,'crimson-agent.base.arterial-cut','crimson-agent.base.hemorrhage-slash','crimson-agent.arch.blood-echo','crimson-agent.arch.rupture-trigger','crimson-agent.hero.thirstborn.hemorrhagic-plague','crimson-agent.hero.thirstborn.pain-to-power-conduction','crimson-agent.hero.thirstborn.bloodstorm'], 'family.bleeding','1d4',3,'start',cap=2,
    notes=['Default instance cap is one. Blood Echo permits two independent instances; third refreshes oldest.', 'Arterial Cut extends one existing instance by two ticks to maximum five remaining.', 'Blood Echo adds one to one instance next tick once on an owner turn; include that actual due bonus in group expectation.', 'No BG or proc generation from periodic damage. A spread instance cannot spread again.'])
periodic('dragoon.bleed','Dragoon Bleed','dragoon',[4,'dragoon.hero.dragon-tyrant.sovereign-descent','dragoon.hero.dragon-tyrant.tyrant-s-impale'],'family.bleeding','1d4',2,'start',notes=['Impale Bleeding binds this engine profile; pin and Bleed have independent endings.'])
periodic('dragoon.burn','Dragoon Burn','dragoon',[4,'dragoon.hero.drake-rider.drakestorm-dive','dragoon.hero.dragon-tyrant.sovereign-descent'],'family.ongoing-fire','1d4',2,'start')
periodic('ranger.synergy.bleed','Weapon Synergy Bleed','ranger',[1],'family.bleeding','1d4',2,'end')
periodic('ranger.imbue.burn','Fire Imbue Burn','ranger',[2,'ranger.arch.elemental-imbue'],'family.ongoing-fire','1d4',1,'end')
periodic('ranger.emberroot.burn','Emberroot Burn','ranger',[4],'family.ongoing-fire','1d4',1,'end')
periodic('shaman.blood-curse.bleed','Blood Curse Bleed','shaman',['shaman.hero.bloodcaller.blood-curse'],'family.bleeding','1d4',3,'start',damage_type='necrotic')
periodic('shaman.bloodroot.bleed','Bloodroot Trail Bleed','shaman',['shaman.hero.bloodcaller.bloodroot-trail'],'family.bleeding','1d4',1,'end',notes=['Initial zone damage remains necrotic. The separately untyped Bleed uses the explicit type bridge; not inferred from the zone.'])
periodic('shaman.flame-totem.burn','Flame Totem Burn','shaman',[1],'family.ongoing-fire','1d4',1,'end')
periodic('shaman.flask.burn','Burn Flask','shaman',[4,'shaman.base.flask-use'],'family.ongoing-fire','1d4',1,'end')
periodic('shaman.cinderflame.burn','Cinderflame Burn','shaman',['shaman.hero.theurgist.summon-cinderflame'],'family.ongoing-fire','1d4',1,'end')
periodic('soldier.overwatch.bleed','Overwatch Bleed','soldier',[1],'family.bleeding','1d4',1,'start')
periodic('thief.bloodleech.bleed','Bloodleech Bleed','thief',[2,3],'family.bleeding','1d4',2,'start',notes=['Requires failed poison save; critical healing is a separate once-per-dose consequence.', 'One recipe instance per target/owner; maximum two different active poison recipes from this owner.'])
periodic('thief.shadow-stab.bleed','Shadow Stab Bleed','thief',['thief.arch.shadow-stab'],'family.bleeding','1d4',2,'end')
periodic('thief.vein-cutter.bleed','Vein Cutter Bleed','thief',['thief.hero.shadowblade.vein-cutter'],'family.bleeding','1d4',2,'end',notes=['Explicit two-tick Bleed is preserved despite shorter generic duration field. Separate Speed/next-damage riders expire at end next turn.', 'Consumes a prepared poison without its ordinary recipe effect; recipe-slot interaction pending exact review.'])
periodic('thief.ashblood.periodic','Ashblood periodic poison','thief',[2,3],None,'1',2,'start',damage_type='fire',notes=['Proposed exclusion from ongoing-fire family: the source is an internal poison recipe without Burn/ignition wording. Exact classification and cure review pending.', 'Critical no-HP-recovery rider ends end next turn separately from two-tick fire.'])
for suffix in ['splinter-bone-fangs','gore-maw','eviscerator-protocol']:
    periodic('warrior.'+suffix+'.bleed','Mutation Bleed — '+suffix.replace('-',' ').title(),'warrior',['warrior.supplement.'+suffix],'family.bleeding','1d4',2,'start')
periodic('druid.charbear.burn','Charbear Burn','druid',['druid.hero.ashen-grove.charbear'],'family.ongoing-fire','1d4',1,'end',notes=['Nearby aura damage and smoke are separate effects; family immunity does not negate their unrelated components.'])
periodic('mage.fire-focus.burn','Fire Focus Burn','mage',['mage.base.fire.fire','mage.arch.elemental-surge','mage.arch.elemental-mastery'],'family.ongoing-fire','1d4',1,'start',group='mage.fire-focus-burn',notes=['Elemental Surge explicitly applies this profile. Arch Elemental Mastery grants one additional tick.', 'Independent Inferno schedule remains; only highest expected application in this group damages at a shared marker.'])
periodic('mage.inferno-lance.burn','Inferno Lance Burn','mage',['mage.base.fire.fire','mage.arch.elemental-mastery'],'family.ongoing-fire','1d6',2,'start',group='mage.fire-focus-burn',notes=['Requires failed initial save. Arch Elemental Mastery grants one additional tick.', 'Passive Fire Focus can legally apply on the same finisher; group arbitration prevents added shared ticks.'])
periodic('mage.elemental-bolt.burn','Elemental Bolt Fire rider','mage',['mage.base.elemental-bolt'],'family.ongoing-fire','1d4',1,'start',group='mage.fire-focus-burn',notes=['Explicit new attached-fire classification; proposed shared Focus group pending review.', 'Not a Focus card for the Arch duration upgrade merely because damage type is fire.'])
periodic('mage.elemental-fusion.burn','Elemental Fusion Fire + Cold rider','mage',['mage.hero.elementalist.elemental-fusion'],'family.ongoing-fire','1d4',1,'start',notes=['Only Fire+Cold pair applies this rider; separate Speed reduction retains its own endpoint.'])
periodic('mage.cascade-storm.burn','Cascade Storm first fire hit rider','mage',['mage.hero.elementalist.cascade-storm'],'family.ongoing-fire','1d4',1,'end',notes=['Only first fire target gets this rider. NEW missing-marker fallback is end next regular target turn.'])
periodic('cleric.flame.burn','Flame Invocation fire','cleric',['cleric.base.flame.flame'],'family.ongoing-fire','1d6',2,'start')
periodic('cleric.divine-invocation.burn','Divine Invocation Flame fire','cleric',['cleric.arch.divine-invocation'],'family.ongoing-fire','1d6',1,'start')
periodic('wizard.combo-surge.burn','Combo Surge Fire + Cold fire','wizard',['wizard.hero.elementalist.combo-surge'],'family.ongoing-fire','1d6',1,'start',notes=['Fire damage rider and failed-STR Restrained component are separate; ending one does not silently end the other.'])
periodic('tinker.burn-injector.burn','Burn Injector','tinker',[3],'family.ongoing-fire','1d4',2,'end')
periodic('tinker.fire-bomb.burn','Fire Bomb Burn','tinker',[4],'family.ongoing-fire','1d4',1,'end')

# Incorporate concluded interface decisions without rewriting any source object.
definitions['paladin.vengeance-mark.retribution']['ending'] = 'End of owner next regular turn. Spending the next-Smite die does not end this mark, its opportunity-attack advantage, or its shared Vengeance eligibility.'
definitions['warrior.brutality-vulnerable']['effect'] = 'Owner eligibility flag: perceived hostile within 60 feet, with 4 × current HP <= maximum HP. Never damage vulnerability.'
definitions['warrior.brutality-vulnerable']['ending'] = 'Only while operative. Brutality Momentum uses the pre-damage snapshot; a killing hit cannot qualify itself by reducing the target to zero.'
definitions['oracle.decay']['integrationDecisions'] += [
    'Blocks all HP increases, including natural-20 death recovery. Blocked natural 20 clears death counters and stabilizes at zero with one ordinary d4-hour deadline.',
    'An already-due Stable recovery retains its absolute deadline while prohibited; ending prohibition resolves one HP only if still living, Stable and at zero. Damage/death cancels normally.',
    'Legal positive-potential magical healing can trigger an applicable Bleed cure even with zero actual HP regained. Separately printed condition removal remains legal.']
for ident in ['paladin.vengeance-mark.retribution','warrior.brutality-vulnerable','oracle.decay']:
    for review in ['GPT_CUSTOM_RIDER_SCOPE_REVIEW.md','GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md']:
        if EVIDENCE+review not in definitions[ident]['reviewEvidence']:
            definitions[ident]['reviewEvidence'].append(EVIDENCE+review)

packet['schemaVersion'] = '0.2'
packet['definitions'] = list(definitions.values())
packet['familyRules'] = [
    {'id':'family.bleeding','rule':'Explicit hostile Bleed classification for immunity, curing and stated eligibility. Class/owner/source timing and caps remain separate. No inherited damage package.', 'sameMarkerArbitration':True},
    {'id':'family.ongoing-fire','rule':'Only explicitly registered creature-attached Burn-style periodic fire. Excludes direct fire, areas, hazards, environmental flames, object ignition, Resonance Burn and names alone.', 'sameMarkerArbitration':True},
    {'id':'periodic.arbitration','rule':'Within each family at one identical target timing marker, select one stack group by highest expected unmitigated damage then earliest application. Apply source instance caps before comparing. All due groups consume their tick, including non-damaging losers. Different markers and families resolve separately. Stable unique application sequence breaks simultaneous applications in resolution order; lexical group ID is a final implementation tie-break only.', 'reviewEvidence':[EVIDENCE+'GPT_CUSTOM_RIDER_SCOPE_REVIEW.md',EVIDENCE+'GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md']},
    {'id':'ownership','rule':'Ordinary your means ownerCharacterId. Explicit class phrases restrict sourceClass. Crimson technical Bleed engine hooks require owned Crimson instances. Suppressed, immune, inactive or expired effects do not satisfy active-effect hooks.'},
    {'id':'hp-cure-separation','rule':'HP prohibition prevents regained HP. Legal positive-potential magical healing can still invoke a registered Bleed cure, including Blood Curse CON save; a remover explicitly requiring actual HP gained retains that prerequisite.'}]
packet['openIssues'] = [
    'Complete exact periodic-profile conference, especially proposed cure defaults and split component durations.',
    'Bind source-specific hook references and remaining root/slow/curse/disease/mark metadata.',
    'Resolve remaining common round-marker endpoints.',
    'Semantically classify all active class/spell rider references; keyword scans and reference integrity are not exhaustive semantic coverage.']
PATH.write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print(f'Updated {len(definitions)} provisional definitions; registry remains {packet["status"]}.')
