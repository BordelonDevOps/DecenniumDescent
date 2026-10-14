"""Explicit editorial corrections, preserving original GPT replies in the audit folder."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/playtest/class_drafts'
def read(n):return json.loads((D/f'{n}.json').read_text(encoding='utf-8'))
def write(n,d):
 d['reviewStatus']='Provisional; editorial review applied; human table balance testing required'
 (D/f'{n}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def add(d,s):
 if s not in d['engine']:d['engine'].append(s)
def card(d,line):return next(c for c in d['cards'] if c[0]==line)

d=read('cleric')
d['engine'][1]=d['engine'][1].replace('Base Conviction maximum is 3;','Base Conviction maximum is 3, automatically becoming5 at Cleric9;')
add(d,'Capacity clarification: the automatic level9 Conviction increase is a new draft completion so every Hero can pay its5-Conviction Finale without buying Conviction Pool. Conviction Pool adds2 at any level, yielding5 early or7 from9. It never fills gained capacity immediately.')
c=card(d,2002);c[7]=c[7].replace('until the next pulse','until the start of your next regular turn or effect end, whichever is first')
c=card(d,2014);c[2]='Triggered and passive';c[3]='1 RP per healing pulse';c[6]='Healing once/own regular turn; critical reduction once/ally/round';c[7]='Aura of Grace. At the start of your regular turn during a real encounter, you may pay1RP to heal S HP to up to3 living allies within15ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum0 extra dice. No unlimited free healing.'
c=card(d,2017)
if 'even if that event' not in c[7]:c[7]+=' This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.'
c=card(d,2055);c[3]='Lose S+M actual HP from yourself or one willing ally within5ft';c[7]=c[7].replace('loses S d6 HP','loses S+M actual HP').replace('You gain 1 Conviction.','The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain1Conviction.')
c=card(d,2052);c[7]=c[7].replace('At the end of each of your regular turns, each surviving fanatic may','Spend one Bonus Action on your regular turn to command the Choir; this explicitly priced Finale permits up to four surviving fanatics to').replace('move up to its Speed and make one melee','each move up to its Speed and make one melee')
c=card(d,2059);c[7]=c[7].replace('one attack at the end of each of your turns','one attack only when you spend your shared companion Bonus Action command')
write('cleric',d)
d=read('crimson-agent')
add(d,'Capacity clarification: Blood Gauge automatically reaches capacity6 at class9. Spill Control allows reaching6 early but never raises the cap above6. This new explicit gate ensures a later5-BG Final Cut can be used without an optional capacity selection. Gain cap2/round and encounter reset0 still apply.')
write('crimson-agent',d)
d=read('monk')
add(d,'Unarmored Flow completion: while wearing no armor or shield, AC=10+DEX modifier+WIS modifier, or ordinary armorless AC if higher, never both. Unarmed strikes use DEX for attack/damage and1d6 at1,1d8 at5,1d10 at11,1d12 at17. This is a new numeric completion; no automatic Extra Attack beyond printed techniques.')
d['engine']=[s.replace('If a tagged technique would add exactly 1 Dissonance','If a tagged technique would add at least1 Dissonance').replace('at Monk 9 it is gained automatically only if','at Monk9 or the first later level when eligible it is gained automatically only if') for s in d['engine']]
add(d,'Each technique tagged weave creates1D in this pilot, unless it explicitly says otherwise. Ki can prevent up to1D before resolution only if remaining Ki pays that additional cost. Full-Ki capstones may legally accept D. The Stun Guard shares the suite-wide once/character/target hard-denial mark; its later failed-save fallback of reaction loss is an explicit Monk exception, not a second Stun.')
c=card(d,3255)
if 'replaces only' not in c[7]:c[7]+=' Spending all5Ki replaces only that technique\'s printed Ki cost; any RP, rest-use, target and recharge requirements are still paid/met. The bonus dice apply to one target only, cannot copy critical bonus dice, and cannot generate further attacks or resources.'
c=card(d,3230);c[3]='0 for stance; healing costs1 Ki and1 RP';c[7]=c[7].replace('spend 1 Ki;','spend1Ki and1RP;')
c=card(d,3280);c[3]='1 RP for each healing trigger';c[7]=c[7].replace('that ally regains S HP','you may pay1RP for that ally to regain S HP')
write('monk',d)
d=read('mage')
d['engine']=[s.replace("Named active Mage cards whose effect begins with 'Mage spell'", "Named Mage cards tagged mage-spell, and the three Focus finishers") for s in d['engine']]
add(d,'Class-spell ranks are printed in the normalized card data: use the legal maximum Mage rank at that card\'s minimum class level, capped9; the three Focus finishers are rank1. Rank determines Dissonance, Counterspell and rank-limited interactions, not a second RP cost. A shared spell uses the ally\'s normal Action and caster-side Dissonance at the moment it is cast; it never builds the Mage\'s Nuke Chain remotely. Spellcasting through Fracture as Lich uses the shared direct-trauma rule.')
c=card(d,2939);c[7]=c[7].replace('until the next pulse','until the start of your next regular turn or effect end, whichever is first')
c=card(d,2913);c[7]=c[7].replace("critical spell's unmodified rolled damage dice total", "spell's base unmodified damage dice total before critical extra dice")
c=card(d,2935);c[7]=c[7].replace('a resistance, ', '');c[7]+=' Resistance is not a numeric bonus and is not shared by this card.' if 'is not a numeric bonus' not in c[7] else ''
c=card(d,2942);c[7]+=' The recipient is another creature; same-pool transfers and circular refund chains cannot increase total RP.' if 'another creature; same-pool' not in c[7] else ''
write('mage',d)
d=read('ranger')
for c in d.get('extraCards',[]):
 if c['level']==20:c['effect']='New playtest Hero capstone. Once per long rest when using your Hero Arrow, pay its normal Hit Chain/action requirements, then enhance only that activation: Warder grants2M temporary HP instead of M; Stalker adds S d6 piercing to one of its two hits; Outrider adds S d4 necrotic to one target on its single pulse. No extra Arrow, Hit Chain, action or copied proc.'
write('ranger',d)
d=read('wizard')
add(d,'Class matrices tagged wizard-spell receive a rank in normalized card data equal to maximum ordinary Wizard rank at their minimum class-level gate (cap9). Printed RP cost replaces generic rank cost. Counterspell is rank1 at its explicit level2 automatic grant. This explicit convention closes rank-dependent Counterspell/Dissonance interactions without inventing extra costs.')
d['engine']=[s.replace('Refrain, Overcast and any other independent Dissonance or Burn rule still apply normally.','Refrain and explicitly printed strain costs still apply; the suite disables generic Overcast and does not layer historical Burn onto Dissonance.') for s in d['engine']]
# Retain source school identity without an unlimited combat-healing loop.
d['engine']=[s.replace('NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, regain 1 HP.','NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain1temporaryHP; it is not permanent healing.') for s in d['engine']]
write('wizard',d)
print('Explicit review corrections applied to7 drafts; original GPT replies preserved.')
