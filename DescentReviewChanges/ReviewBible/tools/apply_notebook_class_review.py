"""Apply fifteen notebook findings plus one independently found condition mismatch."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data/playtest/class_drafts'
def read(n):return json.loads((D/(n+'.json')).read_text(encoding='utf-8'))
def write(n,d):
 d['reviewStatus']='Provisional; notebook adversarial findings reconciled and source-preserving editorial review complete. Human balance testing remains.'
 (D/(n+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def card(d,line):return next(c for c in d['cards'] if c[0]==line)
def add(d,s):
 if s not in d['engine']:d['engine'].append(s)

d=read('crimson-agent')
d['engine']=[s.replace('One Blood Mark at a time on a living target with your Bleed.','One Blood Mark at a time on a living target with your Bleed, except Phantom Strike, which explicitly may apply the mark without Bleed. It does not add a free Bleed.') for s in d['engine']]
c=card(d,2155);c[7]=c[7].replace('at each turn end and whenever it takes damage','at the end of each of its turns and the first time each round it takes damage')
c=card(d,2208);c[7]=c[7].replace('Each creature can be Stunned by this card only once/encounter.','The Stun uses the shared hard-denial guard across all this character’s features. If this character already hard-denied that target this encounter, only damage and the non-hard-denial rider resolve.')
write('crimson-agent',d)
d=read('shaman');c=card(d,4055);c[7]=c[7].replace('Failure by10 also Stunned once/target/encounter.','Failure by 10 also Stunned, subject to the shared hard-denial guard across all the Shaman’s features. Companion Stun counts as the Shaman’s denial; if the target already suffered that denial this encounter, only damage and Reaction loss resolve.');write('shaman',d)
d=read('druid')
for line in [2736,2802]:card(d,line)[6]='1/long rest'
write('druid',d)
d=read('mirrorsage');c=card(d,3069);c[7]+=' An inert backup counts toward the absolute six-record archive ceiling. A backup cannot be created if usable records plus inert backups would exceed six.' if 'inert backups would exceed six' not in c[7] else ''
c=card(d,3121);c[4]='One damage Echo you released this turn';c[7]=c[7].replace("Counts within the originating round's release package; no separate future release action spent.",'Declare Mirror Double before the current turn ends; its pending copy remains part of this turn’s one release package and does not consume a later release allowance.');write('mirrorsage',d)
d=read('ranger');card(d,3898)[1]=11
add(d,'If a primed Arrow expires unused, the prime ends and Hit Chain resets to 0. This applies equally to Efficient Killer’s threshold of two. Efficient Killer itself requires Ranger 11, when Hit Chain exists.')
write('ranger',d)
d=read('soldier');c=card(d,4217);c[7]=c[7].replace('Counts against shared extra-action/attack grant cap for that ally this round.','For cap purposes this granted move plus one weapon attack counts as the ally’s one additional full Action for the round; it still permits only one weapon attack and never Extra Attack.');write('soldier',d)
d=read('tinker');c=card(d,4585);c[7]+=' If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses.' if 'also clears that disabled state' not in c[7] else '';write('tinker',d)
d=read('thief');old=next((c for c in d['extraCards'] if c['name']=='Master of the Unseen' and not c.get('path')),None)
if old:
 d.setdefault('supersededCompletionAlternatives',[]).append(old);d['extraCards'].remove(old)
 for path in ['Arcane Trickster','Shadowblade']:
  c=dict(old);c.update(path=path,band='Hero',acquisition='automatic',prerequisite=f'Thief 20; {path}',rangeAndTarget=f'Self; {path} only');d['extraCards'].append(c)
d['engine']=[s.replace('Poisoned means-1attack rolls/ability checks (not every save)','Poisoned uses the Core V2 condition: disadvantage on attacks and ability checks (not saving throws)') for s in d['engine']]
write('thief',d)
d=read('paladin')
for c in d['extraCards']:
 if c['name']=='Aura of the Crown':c['effect']='Selected allies gain +1 on saving throws. Once per round when one selected ally takes damage, you may use your Reaction after that target applies its defenses once to redirect up to M of its remaining damage to yourself. The transferred amount cannot be reduced, reflected, redirected again or generate resources. This consumes the shared Paladin redirection allowance.'
 if c['name']=="King's Smite":
  c['effect']=c['effect'].replace('Redirected damage keeps its type and cannot be redirected again.','Apply the original target’s defenses once, then transfer up to 5 of the remaining damage. Transferred damage keeps its type and cannot be reduced again, reflected, redirected again or generate resources.')
  c['duration']='Smite instantaneous; temporary HP until lost; redirection passive while this Oath is active'
  c['frequency']='One paid Smite total per round, shared with all normal and reactive Smite uses; redirection uses the shared Paladin allowance'
 if c.get('kind')=='oathSmite':c['frequency']='One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance'
 # Keep every Oath's transfer wording consistent, not only the reviewed Martyr King example.
 c['effect']=c['effect'].replace('your defenses mitigate it once after transfer','the original target’s defenses apply once before transfer, with no further mitigation').replace('Your own resistance and DR may mitigate your portion once.','Your portion cannot be mitigated again after the original target’s defenses have applied.').replace('and may be mitigated once by your defenses','and cannot be mitigated again after the original target’s defenses apply once')
add(d,'For any one damage event choose exactly one Paladin redirection feature. Using it consumes the shared redirection allowance for that round. Crown Undying permits two DIFFERENT ally-damage events per round, but still only one redirection feature may modify each event.')
write('paladin',d)
d=read('oracle')
remove=[c for c in d['extraCards'] if c['name'] in ['Ability Score Improvement — Oracle 12','Ability Score Improvement — Oracle 16']]
for c in remove:d.setdefault('supersededPlaytestOverrides',[]).append(c);d['extraCards'].remove(c)
if not any(c['name']=='Ability Score Improvement — Oracle 14' for c in d['extraCards']):
 c=next(x for x in d['excludedRegistryAlternatives'] if x['name']=='Ability Score Improvement — Oracle 14');d['extraCards'].append(dict(c))
d['engine']=[s.replace('Oracle 12 and 16: separate ASI or eligible feat, replacing the conflicting registry level-14 milestone.','Oracle 14: separate ASI or eligible feat.').replace('HERO-STAGE PROGRESSION.','HERO-STAGE PROGRESSION.') for s in d['engine']]
add(d,'Oracle’s exceptional ASI/feat schedule is 4, 8, 14 and 19. It does not gain extra ASIs at 12 or 16 from the generic class schedule. The rejected five-milestone draft remains in supersededPlaytestOverrides for traceability.')
write('oracle',d)
print('Applied all fifteen notebook findings and aligned Thief Poisoned with Core V2.')
