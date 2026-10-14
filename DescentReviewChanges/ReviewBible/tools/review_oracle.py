"""Review Oracle integration; preserve unedited GPT answers in the audit folder."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]/'data/playtest/class_drafts/oracle.json'
d=json.loads(P.read_text(encoding='utf-8'))
def card(name):return next(c for c in d['extraCards'] if c['name']==name)
def append(name,text):
 c=card(name)
 if text not in c['effect']:c['effect']+=' '+text
def add(text):
 if text not in d['engine']:d['engine'].append(text)

old=next((c for c in d['extraCards'] if c['name']=='Ability Score Improvement — Oracle 14'),None)
if old:
 d.setdefault('excludedRegistryAlternatives',[]).append(old);d['extraCards'].remove(old)
 for lv in [12,16]:
  c=dict(old);c.update(name=f'Ability Score Improvement — Oracle {lv}',level=lv,sourceRef=None,
      effect='Use the shared ASI or feat milestone, once only; this is not a second award.',prerequisite=f'Oracle {lv}')
  d['extraCards'].append(c)
d['engine']=[s.replace('Oracle 14: separate ASI or eligible feat.','Oracle 12 and 16: separate ASI or eligible feat, replacing the conflicting registry level-14 milestone.').replace('in part 2','below').replace('in the part-2 Mystery module','in the Mystery cards below').replace('belongs to the Mystery module in part 2','is represented only by its explicit Mystery card below') for s in d['engine']]
for c in d['extraCards']:
 c['effect']=c['effect'].replace('Part 2 defines those features.','The Mystery cards below define those features.').replace('in the part-2 Mystery module','in the Mystery cards below').replace('belongs to the part-2 Mystery module','is represented by its explicit Mystery card below')
 if c.get('kind')!='curse':
  c['effect']=c['effect'].replace('Exhausted','suffering Revelation backlash').replace('Exhaustion','Revelation backlash')
  c['duration']=c['duration'].replace('Exhausted drawback','Revelation backlash')

add('INTEGRATION PRECEDENCE. The source ceiling draft conflicts with the registry on short rests and extra Revelation activations. This pilot explicitly chooses 1 RC on a completed short rest and permits a second Revelation only through an expressly granted extra Action or double-cast feature, never more than two Revelation resolutions per round. The preserved ceiling alternative is no short-rest recovery and one activation per round; do not combine both configurations.')
add('All combat-triggered RC refunds, including Prophecy, damage riders and Curse Boons, share ONE recovered RC per round. Rest recovery, encounter-start floor and explicitly limited Final refills are separate. A free, copied or refunded use cannot recursively trigger another recovery. Apply this global cap even if an individual card says its recovery is separate.')
add('The shared Prophetic Surge and your Mystery-specific level-18 Prophecy are two descriptions/options of ONE long-rest use, not two charges. Framework cards such as Tier III, Mystic Insight, Mastery and Final Revelation unlock the named Mystery card and never grant duplicate uses. A level-5 registry Mystery label grants no extra unnamed ability.')
add('Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones.')
add('Revelation backlash is the local one-turn penalty of -1 to attacks and saves and -5 feet Speed, ending at the end of your next turn. It is not a level of the general Exhaustion condition. Wound Eater\'s missed-feeding Exhaustion remains the general condition.')
add('Initiative adjustments change order beginning next round. They never produce or erase a regular turn in the current round; a creature still gets at most one regular turn each round. Ties use the original initiative order. Fixed encounter-start bonuses do not retroactively reorder an encounter.')
add('Extra attacks and echoed damage use base weapon/spell dice before critical-hit extra dice. A redirected damage event cannot be reduced a second time, reflected again or generate RC. Charmed alone does not grant command of a creature\'s actions.')

c=card('Wound Eater');c['effect']=c['effect'].replace('drain1d6 HP;','pay 1 RC to drain 1d6 HP;').replace('you may activate or suppress a 10-foot drain aura as a Bonus Action.','pay 2 RC as a Bonus Action to activate a 10-foot drain aura, requiring concentration for at most three pulses; pay 1 RC before each pulse after the first or end it. You may suppress it freely.').replace('each meaningful living enemy in the aura','up to three meaningful living enemies in the aura').replace('meaningful living enemies of your choice within20 feet','up to three meaningful living enemies within20 feet')
append('Spiral-Touched','Time Loop does not restore RP, Ki, Conviction, Blood Gauge, device stock, healing reserves or any other daily/rest resource; only the named RC and per-encounter states rewind. No loot changes ownership through rewinding. Record the snapshot at initiative; if no complete snapshot exists, this option is unavailable and unspent. It cannot undo a previous encounter or duplicate a per-rest use.')
append('Spirit Walk','Your physical body remains in its original space and can still be attacked normally; damage and conditions on either form affect your one character. The optional Revelation uses its normal activation and cost: this feature grants no free Action. Ending in an occupied or illegal space returns the spirit to its body.')
append('Bloodline Convergence','Concentration is required. At most three chosen allies gain its aura. The free Tier I activation uses its ordinary action type and shares the two-Revelation ceiling.')
append('Field Command','The ally pays every ordinary resource cost, rest use and recharge and meets every prerequisite. This is one additional Action for the shared cap; it cannot activate an action-granting feature.')
append('Fury of the Host','Concentration is required; choose at most three allies for its benefits. Each granted Action may make only one ordinary weapon attack or Dash, and cannot grant another action.')
append("Ledger's Command",'Eligible targets are nonlegendary undead of challenge rating no greater than half your Oracle level (round down), with Wisdom saves initially and at each turn end. Commanding uses your shared companion Bonus Action; only one commanded undead makes one attack per round, capped at S d8+M damage with no monster multiattack, recharge or spell resources. Commanding a hostile undead to spend its Action consumes its one hard-denial allowance; later control can only deny Reactions and reduce Speed to 0 on a failed save, never command another Action.')
append('Rotting Touch','At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack.')
append('Unfinished Chorus','Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply.')
c=card('Ledger Unbound')
if c:
 c['effect']+=' For the blast, roll 4S d8+M once; each of at most three enemies takes the lesser of that result or one-quarter its maximum HP, with a Constitution save for half. This blast cannot reduce HP below 1, including the rolled component. Servants use the shared one-damaging-companion-action budget; interception requires your Reaction and consumes that servant.'
append('Fate\'s Glimpse','The caster-side follow-up is simply advantage on your next Revelation attack before the end of your next turn. You never roll another creature\'s saving throw with advantage.')
append('Life Linked','Apply mitigation to the original damage once before splitting. The transferred portion cannot be mitigated again and cannot generate recovery or retaliation triggers.')
append('The Spiral Opens','There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve.')
d['reviewStatus']='Provisional; source gates, action/refund loops and area/companion limits reviewed by Codex; table balance testing required'
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Oracle integration reviewed; original replies and alternate milestone retained.')
