"""Record only complete captured rows; disputed interpretations remain inactive."""
from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_HEALING_REMAINING_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
p=ROOT/'data/playtest/healing_remaining_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
rows={b['bindingId']:b for b in d['bindings']};count=0
disputed={'oracle.supplement.flame.zealot-s-renewal','oracle.supplement.flame.crown-s-burn','mirrorsage.arch.dual-echo-cast'}
ev='docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_REVIEW_PARTIAL.md'
for line in reply.splitlines():
 if not line.startswith('| `') or not line.endswith('|'):continue
 cells=[c.strip() for c in line.strip('|').split('|')]
 if len(cells)!=3:raise AssertionError(line)
 ident,role,note=cells;ident=ident.strip('`')
 if '.engine[' in ident:
  owner,index=re.fullmatch(r'(.+)\.engine\[(\d+)\]',ident).groups();key=f'class-engine:{owner}:{index}'
 else:key=f'class-card:{ident.split(".")[0]}:{ident}'
 assert key in rows,key
 b=rows[key];b['classification']=role
 b['status']='DISCUSSED; source-specific implementation review pending'
 b['operationalOverrides']=['DISCUSSION CANDIDATE, not full-card closure: '+note]
 b['openIssues']=['Implement/verify relevant interface or record a bounded exclusion before broader closure.']
 if ident in disputed:
  b['status']='DISCUSSED; proposed interpretation challenged against exact source'
  b['operationalOverrides']=[]
  b['openIssues']=['Source interpretation challenged in CODEX_HEALING_REMAINING_CORRECTIONS.md; await correction before operationalizing.']
 if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
 count+=1
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded',count,'complete rows from partial capture; incomplete rows remain UNREVIEWED.')

# Narrow, explicitly discussed correction to the prior candidate wording.
p=ROOT/'docs/mechanics/HEALING_DEATH_PLAYTEST.md';s=p.read_text(encoding='utf-8')
s=s.replace('Hero1/SR spends the entire remaining pool','Hero1/LR spends the entire remaining pool')
needle='No RP conversion. Verdict Absolute\'s explicit qualifying brand-kill refill is a source exception.'
if 'engine[13] cadence reconciliation' not in s:
 s=s.replace(needle,needle+' **Remainder-conference amendment — engine[13] cadence reconciliation:** level17 Wave is1/long rest, superseding the preserved Hero card and earlier guide\'s1/short-rest wording. This follows the explicit engine reconciliation; the old source remains intact. Wider pool/recharge execution still belongs to the resource pass.')
p.write_text(s,encoding='utf-8')
p=ROOT/'data/playtest/healing_death_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
for b in d['bindings']:
 if b['sourceId']=='paladin.hero.lay-on-hands':
  rule='NARROW CADENCE AMENDMENT from remaining-source conference: engine[13] explicitly reconciles level17 Full Cleansing Wave as1/LONG rest, superseding preserved card1/short rest and earlier guide. Full remaining pool cost/target cap/cleanse and Oathbreaker modes retained. Wider resource implementation remains open.'
  if rule not in b['operationalOverrides']:b['operationalOverrides'].append(rule)
  if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
