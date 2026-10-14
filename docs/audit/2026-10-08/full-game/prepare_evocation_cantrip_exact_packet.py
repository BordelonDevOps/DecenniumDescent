from pathlib import Path
import ast,copy,json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
x=read(D/'candidate_evocation_cantrips.json');rows=copy.deepcopy(x['spells']);shared={}
for n in ast.parse((A/'author_evocation_cantrip_candidate.py').read_text(encoding='utf-8')).body:
 if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
  for t in n.targets:
   if isinstance(t,ast.Name) and t.id in ['common','ending','minute','rider']:shared[t.id]=n.value.value
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
  if isinstance(v,dict) and 'concat' in v:r[k]=''.join(shared[p['shared']] if isinstance(p,dict) else p for p in v['concat'])
 return r
assert [expand(s) for s in rows]==x['spells']
intro='''CODEX — EVOCATION CANTRIP EXACT MANUSCRIPT REVIEW: FOUR ORDERED PARTS, ONE SUBMISSION.

All twelve full cards now exist locally; none is selected or operational. Catalog remains237 reviewed/611 unfinished. Eleven local checks establish source/access/schema preservation only. All fourteen original placements/Core blocks and exact class-access rows follow. The complete source conference and your six-part authoring clarification are saved. Cosmology remains owner-deferred until AFTER successful GitHub push and remote verification. This is not final whole-game/push approval.

Part1: exact common defaults/fragments and Freezing Touch, Flame Lash, Soundburst. Part2: Minor Combustion, Force Needle, Arcane Echo. Part3: Shocking Grasp, Dancing Lights, Acid Splash. Part4: Chill Touch, Thunderclap, Poison Spray. All four are one exact submission. No separate shared-rule manuscript is needed; every mechanical procedure is on the cards.

LOSSLESS ENCODING: each card inherits defaults. A field {"concat":[...]} joins each literal string and {"shared":"name"} fragment exactly without added characters. Local reconstruction equals all original full candidate fields. Source objects are literal and complete.

Please explicitly APPROVE or REPAIR each exact card, identifying precise replacement fields/text when needed. Verify source fidelity, timing/event ownership, current class access, ordinary cast hooks, object procedures, damage/rider separation and absence of added F/scaling. In particular: Freezing Touch retains delayed onset and original +12cap on outside-to-initiative mapping; Arcane Echo actual committed Action qualifier/locked provenance/independent arm+repeat/lineage guard; Shocking Grasp independent paid interrupt and prospective denial; Dancing Lights continuous tether and legal movement without ongoing-LoE destruction; broad Chill Touch recovery prohibition with LIFE TRANSITION exception.

Explicit authoring completions beyond your clarification: (a) Arcane Echo applies Refrain in actual chronological order, not an assumption that original/repeat were consecutive despite intervening casts. It is the normal shared casting rule. (b) Freezing Touch pending onset cannot activate after original +12cap; suppressed/independent records never reset markers. (c) Dancing Lights overlap does not enlarge/upgrade light merely by stacking; one-set cap also applies with actual multiple-concentration features. (d) Chill Touch explicitly binds existing blocked natural20 to Stable0/cleared death counters/d4-hour deadline/preserved used-turn marker and retains blocked Stable recovery deadline. Maximum-HP changes remain permitted but cannot authorize a separate current-HP increase through this broad prohibition. Please approve or repair these written bindings.

Existing HEALING_DEATH_PLAYTEST.md excerpt: "A natural20 whose1HP is blocked uses the previously reviewed Decay bridge: Stable0, cleared counters, immediate d4-hour deadline and preserved used-turn marker. It does not spend Ward. This differs from blocked False LifeV, which remains dying." COMBAT_ACTION_PLAYTEST.md regular-start step3: "Resolve already-due absolute state recovery if now legal, including a previously blocked Stable recovery deadline." All underlying class/condition/core files remain unchanged; the cards reference that existing behavior rather than adding a new roll or recovery engine.

All237 prior operational records and frozen original/class files remain unchanged. Exact manuscript approval does not certify effect runtime, balance or whole-game completion. Keep the six source-conference balance flags open; no source deletion or GitHub push has occurred. Please confirm all four parts are fully available.
'''
parts=[]
for n in range(4):
 body={'cards':rows[n*3:(n+1)*3]}
 if n==0:body={'defaults':defaults,'sharedFragments':shared,**body}
 if n==3:body['repeatedSharedFragmentsForConvenience']=shared
 parts.append((intro if n==0 else 'EVOCATION CANTRIP EXACT REVIEW — inherit Part1 defaults/sharedFragments exactly.\n')+f'\nPART {n+1} OF 4\n'+compact(body)+'\n')
paths=[]
for n,t in enumerate(parts,1):
 p=A/f'CODEX_EVOCATION_CANTRIP_EXACT_REVIEW_PART{n}.txt';assert not p.exists();p.write_text(t,encoding='utf-8');paths.append(p)
p=A/'CODEX_EVOCATION_CANTRIP_EXACT_REVIEW.md';assert not p.exists();p.write_text('\n'.join(parts),encoding='utf-8')
f=A/'EVOCATION_CANTRIP_EXACT_SUBMISSION.json';d=read(f);d.update(status='four exact parts prepared; not yet submitted or promoted',packetPath=str(p),packetSha256=sha(p),parts=[{'part':n+1,'path':str(p),'sha256':sha(p),'characters':len(parts[n])} for n,p in enumerate(paths)],losslessFieldReconstruction='PASS');f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
wrapper='Please review the complete FOUR-PART Evocation cantrip EXACT MANUSCRIPT submission attached in order. It contains all twelve full cards, fourteen original placements/Core blocks and exact class access, with lossless defaults/fragments in Part1. All four parts must be read together. Give APPROVE/REPAIR for each card and precise required replacement text. Source conference plus six authoring clarifications are implemented; specifically check the marked extra bindings. Nothing is selected/promoted yet:237 reviewed/611 unfinished. This is manuscript review only, not runtime, human balance, whole-game flow or GitHub approval. Cosmology remains after the verified push.'
(A/'CODEX_EVOCATION_CANTRIP_EXACT_REVIEW_WRAPPER.txt').write_text(wrapper,encoding='utf-8')
print(json.dumps({'partCharacters':list(map(len,parts)),'totalCharacters':sum(map(len,parts)),'defaults':list(defaults),'lossless':True},indent=2))
