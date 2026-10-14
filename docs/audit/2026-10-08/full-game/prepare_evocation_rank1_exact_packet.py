from pathlib import Path
import ast,copy,json,hashlib,re
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
x=read(D/'candidate_evocation_rank1.json');rows=copy.deepcopy(x['spells']);tree=ast.parse((A/'author_evocation_rank1_candidate.py').read_text(encoding='utf-8'))
ns={'re':re};exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prose'],type_ignores=[]),'<local-prose-normalizer>','exec'),ns)
shared={}
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
  for t in n.targets:
   if isinstance(t,ast.Name) and t.id in ['common','minute','area','objects']:shared[t.id]=ns['prose'](n.value.value)
defaults={k:rows[0][k] for k in rows[0] if k!='id' and all(s[k]==rows[0][k] for s in rows)}
for s in rows:
 for k in defaults:del s[k]
 for k,v in list(s.items()):
  if not isinstance(v,str):continue
  pieces=[v]
  for name,frag in shared.items():
   out=[]
   for z in pieces:
    if isinstance(z,str) and frag in z:
     chunks=z.split(frag)
     for j,c in enumerate(chunks):
      if c:out.append(c)
      if j<len(chunks)-1:out.append({'shared':name})
    else:out.append(z)
   pieces=out
  if len(pieces)>1 or not isinstance(pieces[0],str):s[k]={'concat':pieces}
def expand(s):
 r=copy.deepcopy(defaults);r.update(s)
 for k,v in list(r.items()):
  if isinstance(v,dict) and 'concat' in v:r[k]=''.join(shared[z['shared']] if isinstance(z,dict) else z for z in v['concat'])
 return r
assert [expand(s) for s in rows]==x['spells']
intro='''CODEX — RANK-ONE EVOCATION EXACT MANUSCRIPT REVIEW. FOUR ORDERED PARTS, ONE SUBMISSION.

All twelve complete candidate cards are now authored but remain unselected. Catalog stays249 reviewed/599 unfinished. Eleven local checks establish source/access/schema preservation and nonpromotion, not mechanics/runtime/balance approval. The original source conference, eight authoring clarifications and twelve-example Shatter eligibility conference are saved. The existing249 operational records, raw sources and class cards remain unchanged.

Part1 contains exact common defaults/fragments and Chain Jolt, Force Spike, Magic Missile Storm. Part2 contains Thunder Clap, Arcane Shield Shatter, Ignition Bolt. Part3 contains Chromatic Orb, Earth Tremor, Ice Knife. Part4 contains Thunderwave, Witch Bolt, Zephyr Strike. All thirteen original placements/Core blocks and exact actual class access are included. No separate supplementary manuscript is needed: the full procedures, including the source-qualified ordinary Shield bridge and Shatter comparisons, are on these cards. After approval, a discovery paragraph may be appended to the master integration guide; old cards will not be silently rewritten.

LOSSLESS FORMAT: every card inherits defaults. Fields encoded as {"concat":[...]} join literal strings and {"shared":"name"} values with no extra characters. The local reconstruction equals all original candidate fields exactly. Repeated shared-fragment blocks, where present, are identical convenience copies, not additional rules. All other values/source objects are literal and complete.

Please give explicit APPROVE or REPAIR for each of twelve cards AND the shared/default text. Required replacements should identify the exact field and wording. Review the actual full wording, not just source summaries. In particular:
1) Magic Missile Storm fixed missile allocation/order, distinct hit/damage packets, one ordinary Shield opportunity per recipient before its first missile damage, no class-feature/global alias and no free retargeting.
2) Shatter's semantic source-qualified identity, rank0–1, both effect/recipient range/LoE, paid hidden failure, supersession versus complete suppression, accepted current Resonance Shield tempHP identity, save-only Ward inclusion versus generic Resistance/False Life exclusion, and whole Protective Sphere geometry/parent cleanup.
3) Ignition Bolt critical-only die never splashes; preserved5-foot ranges and pre-damage impact center; Ice Knife's no-save cold after legal hit/miss and no burst when target was already illegal.
4) Earth Tremor's one contiguous supported surface, damage/terrain separation and finite magical terrain with no permanent material creation.
5) Thunderwave's mandatory10-foot displacement stopping only for actual legality, independent of positive thunder damage.
6) Witch Bolt's independent initial hit/tether, maintenance as existing-spell Action activation rather than a cast, no cast-turn/extra-turn pulses, original expiry before voluntary pulse, used-pulse carry into first real turn without confiscating its unrelated ordinary Action, and no target resurrection/recreation reattachment.
7) Zephyr Strike no free cast-time attack, pending strike consumed on hit/normal critical dice even if damage0, separate continuing movement protection, and source-owned replacement cleanup.

Small explicit authoring completions for exact approval: Chain Jolt declares its two target resolution order at commitment; invalidated targets are not replaced. Force Spike applies its Prone save only if the post-damage target is still a legal creature. Witch Bolt on leaving/reordering initiative retains established regular/virtual pulse opportunities and their used histories instead of manufacturing another schedule; this extends the shared clock-preservation rule to its stated spell-specific ledger. No new current-phase timing reset is introduced.

All twelve retain Action/V,S,F/actual rank1/base2RP and no automatic scaling. These are provisional tabletop manuscripts. Human balance flags (auto-hit missile packet density, Force Spike, short-range/no-save bursts, sustained Witch Bolt, Shatter metadata and Zephyr movement protection) remain open. No runtime, whole-game flow, GitHub/publication approval or original-source deletion is implied. Cosmology remains deferred until AFTER the authorized GitHub push and remote commit verification.

Please confirm complete availability of all four parts before giving the exact dispositions.
'''
parts=[]
for n in range(4):
 body={'cards':rows[n*3:(n+1)*3]}
 if n==0:body={'defaults':defaults,'sharedFragments':shared,**body}
 head=(intro if n==0 else 'RANK-ONE EVOCATION EXACT REVIEW — inherit Part1 defaults/sharedFragments exactly.\n')+f'\nPART {n+1} OF 4\n'
 if n and len(head+compact(body))<10500:body['repeatedSharedFragmentsForConvenience']=shared
 parts.append(head+compact(body)+'\n')
paths=[]
for n,t in enumerate(parts,1):
 p=A/f'CODEX_EVOCATION_RANK1_EXACT_REVIEW_PART{n}.txt';assert not p.exists();p.write_text(t,encoding='utf-8');paths.append(p)
p=A/'CODEX_EVOCATION_RANK1_EXACT_REVIEW.md';assert not p.exists();p.write_text('\n'.join(parts),encoding='utf-8')
f=A/'EVOCATION_RANK1_EXACT_SUBMISSION.json';d=read(f);d.update(status='four exact parts prepared; not submitted or promoted',packetPath=str(p),packetSha256=sha(p),parts=[{'part':n+1,'path':str(p),'sha256':sha(p),'characters':len(parts[n])} for n,p in enumerate(paths)],losslessFieldReconstruction='PASS');f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
wrapper='Please conduct the exact manuscript review of all FOUR attached parts, in order, for the twelve rank-one Evocation cards. Full original source/access evidence and lossless shared defaults/fragments are included. The source conference, eight authoring clarifications and twelve-example Shatter eligibility decisions are incorporated. Give APPROVE/REPAIR for each card and shared rules, with precise replacement text where needed. Confirm all four parts are available. Catalog remains249 reviewed/599 unfinished until separate promotion. This does not close runtime, balance, whole-game flow or GitHub delivery. Cosmology remains deferred until after the verified push.'
(A/'CODEX_EVOCATION_RANK1_EXACT_REVIEW_WRAPPER.txt').write_text(wrapper,encoding='utf-8')
print(json.dumps({'partCharacters':list(map(len,parts)),'total':sum(map(len,parts)),'lossless':True,'defaults':list(defaults)},indent=2))
