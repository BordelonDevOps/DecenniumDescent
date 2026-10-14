"""Apply reviewed overlay corrections without modifying normalized source cards."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
BASE='docs/audit/2026-10-08/full-game/'
path=ROOT/'data/playtest/control_state_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
notes={
 'paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes':'Operative its-next-turn wins over summary: target next regular END. Half-Speed/noDash/no willing teleport benefit, including consent to allied transport. Legal involuntary hostile teleport remains source-governed.',
 'dragoon.hero.drake-rider.drakestorm-dive':'Cold slow and lightning Reaction denial: SOURCE next regular END, correcting earlier discussion. Fire uses existing independent periodic binding.',
 'dragoon.hero.drake-rider.elemental-lance':'Cold slow: SOURCE next regular END. Lightning opportunity-attack denial: TARGET next regular START. Preserve distinct clocks.',
 'shaman.hero.theurgist.elemental-chorus':'Slow: SOURCE next regular END, correcting earlier discussion.',
 'shaman.base.elemental-affinity':'Ice slow: SOURCE next regular END. Enhanced Attunement replaces5 with10, not another slow.',
 'oracle.supplement.life.resonant-seed':'Slow ends at end of actual triggering turn, including off-turn entry or extra turn. No turn underway:6 elapsed seconds. Printed per-creature/round pulse cap retained.',
 'druid.arch.winterfang.winter-s-embrace':'Slow ends at current triggering actual turn end. No turn underway:6 elapsed seconds; printed once/enemy/round cap retained.',
 'shaman.hero.soothsayer.balanced-elements':'Owned explicitly classified elemental control may include legal multiclass sources. No Shaman-class-only restriction. Extend from NOW to target following regular end, max with existing endpoint, capped by governing source/concentration maximum; no recursive deadline addition. Actual elemental membership in guide/metadata.',
 'warrior.supplement.hypermutation-spike':'Snapshot each possessed movement mode ordinary sheet Speed, including currently qualifying persistent passive modifiers. Exclude temporary/systemic changes. Half-baseline floor after numeric penalties, no explicit zero/absent-mode/movement-prohibition bypass. Incapacitated itself does not set Speed0 and floor grants no Actions.',
 'oracle.supplement.time.moment-s-pause':'Pending next-numbered-round canonical snapshot delay, nonstack per target. Stable application order, move after first surviving later snapshot participant, ignore new entrants. No duplicate/lost turns or changes to virtual markers. Guide procedure controls.',
 'oracle.supplement.dream.slumber-glimpse':'Initiative-2 is next eligible roll/check before encounter end; no existing-slot change. Retain separate original hard/fallback and next-attack riders.',
 'paladin.supplement.oath-of-mercy.sanctify-ground':'Selecting Staggered ends ALL present classification.staggered records on selected creature, including suppressed records. One named cleansing choice per creature per pulse; no immunity against later applications.',
 'cleric.hero.priest.divine-judgment':'Reflection triggers once each actual target turn, including extra turns, only first positive actual damage. Ordered victim resolution before damage, no summed victims. Off-turn damage none. Repeat saves/maximum expiry remain regular markers.',
 'oracle.supplement.stars.guiding-bolt':'Two independent entitlements: next ally-other-than-owner attack+2 spends on roll; next qualifying ally hit addsS and ends mark, including after a prior miss. Paid reapplication resets both without stacking.',
 'oracle.supplement.flame.wrathful-brand':'Owner damage bonus needs actual positive pre-bonus attack damage. One shared ally-positive-damage entitlement for heal attempt+WIS save; no refund from prevented healing. Timed Brand can persist after riders spent.',
 'crimson-agent.hero.thirstborn.carrion-conductor':'Separate persistent source-specific used-corpse history survives expiration/consumption/suppression; no second Carrion use by any owner. No universal ban on unrelated corpse mechanics.',
 'monk.arch.tortoise.echoing-guard':'Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Warrior version.',
 'warrior.base.brutal-strike':'Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Monk version.',
}
engine_notes={('shaman',1):'Frost slow current triggering actual turn end; no turn underway6sec. Printed entry/start and once/creature/round caps unchanged.',
              ('tinker',5):'Glue slow current triggering actual turn end, not invented next regular turn. No turn underway6sec. Other bomb components retain their own source clocks; Glue terrain lasts its independent3 rounds.'}
components={}
for binding in data['bindings']:
 binding['historicalDiscussion']=binding.pop('interpretation',binding.get('historicalDiscussion',''))
 binding['historicalDiscussionAuthority']='Historical conference context only. Exact sourceProcedure and operationalGuide with operationalOverrides control; corrected statements are not competing active rules.'
 owner=binding['bindingId'].split(':')[1]
 override=notes.get(binding['sourceId'])
 if binding['sourceKind']=='class-engine': override=engine_notes.get((owner,binding['sourceId']))
 binding['operationalOverrides']=[override] if override else []
 if override and BASE+'GPT_CONTROL_CLOCK_CORRECTIONS.md' not in binding['reviewEvidence']:
  binding['reviewEvidence'].append(BASE+'GPT_CONTROL_CLOCK_CORRECTIONS.md')
 for component in binding['componentIds']:
  components.setdefault(component,{'mechanicalId':component,'applicationBindings':[],
   'applicationRule':'Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.',
   'metadata':[]})['applicationBindings'].append(binding['bindingId'])
soft='''crimson-agent.veinjammer.slow dragoon.drakestorm-dive.cold-slow dragoon.elemental-lance.cold-slow druid.winters-embrace.slow mage.cold-focus.flat mage.cold-focus.glacier mage.elemental-fusion.slow mage.cascade-storm.cold-slow monk.pressure-point.leg oracle.guiding-bolt.enhanced-slow oracle.tremor-sense.slow oracle.shardburst.slow oracle.gale-of-unmaking.slow oracle.resonant-seed.slow paladin.black-manifestation.slow paladin.sorrows-weight.slow paladin.reign-of-ashes-aura.slow paladin.standing-stone.slow paladin.iron-leash-aura.slow shaman.frost-totem.slow shaman.elemental-affinity.ice-slow shaman.elemental-chorus.slow soldier.overwatch.snare soldier.suppression-fire.slow soldier.divine-lockdown.slow soldier.net-bolt.large-slow thief.crippling-strike.slow thief.vein-cutter.slow thief.crippling-lash.slow tinker.glue.slow wizard.mind-prison.slow'''.split()
zero='''cleric.word-of-binding.speed-zero monk.nerve-strike.speed-zero oracle.thorned-shelter.speed-zero paladin.ancients.root paladin.iron-leash.speed-zero ranger.glacial-thorn.speed-zero ranger.rootcall-quake.speed-zero shaman.flask.root shaman.ice-wisp.speed-zero soldier.hold-the-line.speed-zero soldier.divine-lockdown.speed-zero tinker.cryo.speed-zero'''.split()
soft+=['ordinary.ray-of-frost.slow','ordinary.frost-arrow.slow','monk.echoing-guard.stagger','warrior.brutal-strike.stagger','paladin.laws-weight.control','paladin.reign-of-ashes.ash-bound']
elemental='''shaman.elemental-affinity.ice-slow shaman.frost-totem.slow shaman.elemental-chorus.slow shaman.ice-wisp.speed-zero mage.cold-focus.flat mage.cold-focus.glacier mage.elemental-fusion.slow mage.cascade-storm.cold-slow dragoon.drakestorm-dive.cold-slow dragoon.elemental-lance.cold-slow'''.split()
for ident in soft+zero:
 assert ident in components,ident
 components[ident]['metadata'].append('eligibility.slowed-foe')
 components[ident]['activeHookRule']='Only when this adverse Speed component actually applies and is not suppressed/expired. Numeric overshadowing does not deactivate it.'
for ident in elemental:
 components[ident]['metadata'].append('classification.elemental-control')
for ident in ['core.staggered','monk.echoing-guard.stagger','warrior.brutal-strike.stagger']:
 components.setdefault(ident,{'mechanicalId':ident,'applicationBindings':[],'metadata':[],
  'applicationRule':'Core condition procedure remains in CONDITIONS_PLAYTEST; added here as metadata reader bridge only.'})['metadata'].append('classification.staggered')
data['componentIndex']=list(components.values())
data['precedence']='Exact operative source text > abbreviated summary; reviewed operationalGuide/operationalOverrides fill stated gaps. HistoricalDiscussion is preserved context, not active rule text.'
data['openIssues']=['Actual inflicted disease/curse source catalog and special endpoints.','Non-spell curse tier/removability metadata.','Object/tether durability beyond printed sources.','Death/replacement/resurrection interfaces.','Remaining all-source semantic review and mechanics outside this bounded control pass.','Final exact candidate review pending.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Update the old explicitly ambiguous Brand endpoint in the existing registry.
custom_path=ROOT/'data/playtest/custom_condition_bindings.json'
custom=json.loads(custom_path.read_text(encoding='utf-8'))
brand=next(x for x in custom['definitions'] if x['mechanicalId']=='paladin.vengeance-mark.judgment-brand')
brand['ending']='Third future target regular-turn end, excluding an in-progress current target end. Preserve virtual marker; outside initiative bare3 rounds is application+18 elapsed seconds.'
evidence=BASE+'GPT_CONTROL_STATE_FIRST_REVIEW.md'
if evidence not in brand['reviewEvidence']:brand['reviewEvidence'].append(evidence)
custom_path.write_text(json.dumps(custom,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Applied explicit overlay corrections; indexed {len(components)} components, all original sources unchanged.")
