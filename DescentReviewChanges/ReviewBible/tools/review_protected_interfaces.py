from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
for slug in ['druid','thief','tinker']:
 p=ROOT/'data/playtest/class_drafts'/f'{slug}.json'
 d=json.loads(p.read_text(encoding='utf-8'))
 if slug=='druid':
  d['engine']=[s.replace('Transformation itself reduces Dissonance by1 once/encounter (protected interface), never on every form change. No Refrain changes from natural attacks.','Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain.') for s in d['engine']]
 if slug=='thief':
  d['engine']=[s.replace('Following a successful Sneak Attack, your next such technique before end next turn can prevent1D, consuming the benefit; never refunds RP.','Once per round, a Weave trick cast while hidden ignores its first point of Refrain Dissonance, as the protected source contract requires. It does not reduce base Dissonance or refund RP; a technique producing only its fixed1D receives no Refrain reduction unless it actually incurred Refrain.') for s in d['engine']]
 if slug=='tinker':
  d['engine']=[s.replace('Protected magic interface: after paid deployment or paid command of a device, next ordinary spell beforeendnextturn reducesDby1 minimum0; no stacking and cannot repeatedly arm from an idle free follow command.','Protected magic interface: once per short rest, as a Bonus Action route up to2 current Dissonance into one of your active devices within30ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and1RP using Field Repair, or with10minutes and1RP using tinkers tools. No RP is created and no Refrain counter resets.') for s in d['engine']]
 d['protectedInterfaceReview']='Compared against preserved mainRegistry.core.resonanceInterface; corrected drift on2026-10-08'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Protected Druid, Thief and Tinker interfaces restored.')
