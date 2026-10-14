from pathlib import Path
import ast, copy, hashlib, json
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
x=read(D/'candidate_enchantment_rank3.json')
shared={}
for n in ast.parse((A/'author_enchantment_rank3_candidate.py').read_text(encoding='utf-8')).body:
    if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in ['minute','common','guard','control','extension']:
                shared[t.id]=n.value.value
rows=copy.deepcopy(x['spells'])
defaults={k:rows[0][k] for k in rows[0] if k!='id' and all(s[k]==rows[0][k] for s in rows)}
for s in rows:
    for k in defaults:del s[k]
    for k,v in list(s.items()):
        if not isinstance(v,str):continue
        pieces=[v]
        for name,fragment in shared.items():
            out=[]
            for z in pieces:
                if isinstance(z,str) and fragment in z:
                    chunks=z.split(fragment)
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
intro="""CODEX — RANK-THREE ENCHANTMENT EXACT MANUSCRIPT REVIEW. FOUR ORDERED PARTS, ONE SUBMISSION.

All eight full candidate cards and their shared integration text now exist locally but remain unselected. Catalog stays229 reviewed/619 unfinished. Nine local checks verify structure/source/access/nonpromotion only; they are not mechanical or balance approval. The actual source conference and authoring clarification are saved. All eleven original placements/Core blocks and every class-access row are included. Cosmology remains untouched until the authorized GitHub push and remote verification; this review is not about cosmology or final delivery approval.

Part1 contains exact common fields/fragments and Mass Mesmerize, Dominate Beast, Terrifying Gaze. Part2 contains Mental Chains, Hypnotic Pattern, Suggestion. Part3 contains Fear and Slow. Part4 contains the FULL new integration manuscript plus the unchanged relevant companion lifecycle source. All four must be read together.

Encoding is lossless: each card inherits the identical defaults. A field {\"concat\":[...]} concatenates literal strings and {\"shared\":\"name\"} fragment values with no added characters. Every reconstructed field equals the original candidate locally. All other values are literal; no source text omitted.

Please give explicit exact status for each of eight cards AND the shared manuscript. Required repairs should quote the precise replacement text/field. Explicitly approve or repair the marked NEW completions: (1) redirect a same-companion/same-phase pending command by reusing its structural reservation, never another execution's reservation; no new phase/virtual independent companion turn if absent; (2) independently coexisting Dominate Beast applications with actual order arbitration; (3) END-only repeat-save schedules transition to the next actual regular END without replay, while absolute maximum persists; (4) Mental Chains applies the same voluntary boundary to transport, forbids voluntary departure from the anchor plane, permits involuntary separation and resumes original anchor on return; (5) Hypnotic Pattern atomic initial component batch/queued own-concentration teardown; (6) distinct Slow modes, mandatory triggering target, no stacked-Reaction cancellation, prospective Action ceiling and explicit initiative exception; (7) Suggestion establishment-time hard reservation and inability to acquire a new hard component later.

The existing229 individual operational records and class/source files are unchanged. Planned publication adds the reviewed integration overlay and links, not a rewrite of old card records. Source fidelity, manuscript coherence, stateful runtime, numerical/human balance, whole-game flow and push approval remain separate gates. Please confirm the complete four-part submission was available.
"""
parts=[
intro+'\nPART 1 OF 4\n'+compact({'defaults':defaults,'sharedFragments':shared,'cards':rows[:3]})+'\n',
'RANK-THREE ENCHANTMENT EXACT REVIEW — PART 2 OF 4. Inherit Part1 defaults/sharedFragments exactly.\n'+compact({'cards':rows[3:6]})+'\n',
'RANK-THREE ENCHANTMENT EXACT REVIEW — PART 3 OF 4. Inherit Part1 defaults/sharedFragments exactly.\n'+compact({'cards':rows[6:]})+'\n',
'RANK-THREE ENCHANTMENT EXACT REVIEW — PART 4 OF 4. Full proposed shared manuscript and unchanged companion source.\n\n'+(D/'candidate_enchantment_rank3_shared_rules.md').read_text(encoding='utf-8')]
base=(R/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md').read_text(encoding='utf-8')
evidence=base.split('## At the table\n\n',1)[1].split('\n## Different kinds',1)[0]+'\n\n'+base.split('## Stats and ownership\n\n',1)[1].split('\n## Ranger',1)[0]
# The stats span may include additional adjacent source paragraphs; retain verbatim.
parts[3]+='\n\nUNCHANGED REVIEWED COMPANION SOURCE — CREATURE_LIFECYCLE_PLAYTEST.md\n\n'+evidence+'\n'
paths=[]
for i,t in enumerate(parts,1):
    p=A/f'CODEX_ENCHANTMENT_RANK3_EXACT_REVIEW_PART{i}.txt';assert not p.exists();p.write_text(t,encoding='utf-8');paths.append(p)
packet=A/'CODEX_ENCHANTMENT_RANK3_EXACT_REVIEW.md';assert not packet.exists();packet.write_text('\n'.join(parts),encoding='utf-8')
p=A/'ENCHANTMENT_RANK3_EXACT_SUBMISSION.json';d=read(p);d.update(status='exact packet prepared; not yet dispatched or promoted',packetPath=str(packet),packetSha256=sha(packet),parts=[{'part':i+1,'path':str(p),'sha256':sha(p),'characters':len(parts[i])} for i,p in enumerate(paths)],losslessFieldReconstruction='PASS')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'partCharacters':[len(t) for t in parts],'total':sum(map(len,parts)),'defaults':list(defaults)},indent=2))

