from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_HEALING_REMAINING_CORRECTIONS.md').read_text(encoding='utf-8')
p=ROOT/'data/playtest/healing_remaining_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
rows={b['bindingId']:b for b in d['bindings']};count=0
ev='docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_CORRECTIONS.md'
for line in reply.splitlines():
 if not line.startswith('| `') or not line.endswith('|'):continue
 cells=[c.strip() for c in line.strip('|').split('|')]
 assert len(cells)==3,line
 ident,role,note=cells;ident=ident.strip('`')
 if '.engine[' in ident:
  owner,index=re.fullmatch(r'(.+)\.engine\[(\d+)\]',ident).groups();key=f'class-engine:{owner}:{index}'
 else:key=f'class-card:{ident.split(".")[0]}:{ident}'
 assert key in rows,key
 b=rows[key];b['classification']=role
 b['status']='DISCUSSED; source-specific implementation review pending'
 b['operationalOverrides']=['DISCUSSION CANDIDATE, not full-card closure: '+note]
 b['openIssues']=['Implement/verify relevant interface or record a bounded exclusion before broader closure.']
 if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
 count+=1
assert count==67,count
corrections={
 'oracle.supplement.flame.zealot-s-renewal':'CORRECTION: Backlash is a separate1d4 fire packet after the healing attempt. Apply ordinary defenses, then enforce minimum RESOLVED DAMAGE1 unless an explicit Convergence/Prophecy suppresses the component. No survivalHP floor; normal tempHP/Wounds/zero/death follow. Cure clause is independent of actualHP gained.',
 'oracle.supplement.flame.crown-s-burn':'CORRECTION: One shared S d6+M cap roll. Source amount per recipient is max(1,min(floor(total qualifying actualDamageDealt/recipient count),shared cap)) only if numeric total>0; no recipients skips healing. Each target then applies its healing restrictions. No independent cap rolls.',
 'mirrorsage.arch.dual-echo-cast':'CORRECTION: No imported Echo Fusion one-healing-profile limit. Two eligible paid/consumed Mend records from different creatures may each supply half its own profile amount, rounded independently once, including to the same target. One combined release; normal source costs/provenance/no-recursion rules remain.',
}
for ident,note in corrections.items():
 b=rows[f'class-card:{ident.split(".")[0]}:{ident}']
 b['status']='DISCUSSED; exact-source correction agreed, implementation review pending'
 b['operationalOverrides']=[note]
 b['openIssues']=['Validate selected interface against corrected source reading.']
 if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
assert all(b['classification'] for b in rows.values())
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=HERE/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('are under separate discussion. Their','now have individual discussion dispositions in the [partial first capture](GPT_HEALING_REMAINING_REVIEW_PARTIAL.md) and [complete tail/corrections](GPT_HEALING_REMAINING_CORRECTIONS.md). Implementation dependencies remain open. Their')
s=s.replace('It has not yet been submitted or approved.','It has been submitted through the official app connector to the same Calibration Review conversation; operational approval remains pending.')
p.write_text(s,encoding='utf-8')
print('Recorded all131 source dispositions and3 corrections; implementation dependency scopes remain open.')
