"""Build a losslessly factored exact-review packet without duplicate source catalogs."""
from pathlib import Path
from copy import deepcopy
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def common(ds):
    out={}
    for k in set.intersection(*(set(d) for d in ds)):
        vs=[d[k] for d in ds]
        if all(v==vs[0] for v in vs):out[k]=deepcopy(vs[0])
        elif all(isinstance(v,dict) for v in vs):
            c=common(vs)
            if c:out[k]=c
    return dict(sorted(out.items()))
def delta(d,c):
    out={}
    for k,v in d.items():
        if k not in c:out[k]=v
        elif v==c[k]:continue
        elif isinstance(v,dict) and isinstance(c[k],dict):out[k]=delta(v,c[k])
        else:out[k]=v
    return out
def merge(c,d):
    o=deepcopy(c)
    for k,v in d.items():o[k]=merge(o[k],v) if isinstance(v,dict) and isinstance(o.get(k),dict) else deepcopy(v)
    return o
def main():
    target=AUDIT/'CODEX_COOKING_EXACT_REVIEW.txt'
    if (AUDIT/'CODEX_COOKING_EXACT_REVIEW_SENT.txt').exists():raise SystemExit('Exact packet already sent; preserve the actual submission.')
    v=read(AUDIT/'COOKING_CANDIDATE_VALIDATION.json');assert v['status']=='PASS'
    data=read(ROOT/'data/director/cooking_recipe_candidate_internal.json');cards=data['cards'];shared=common([c['operational'] for c in cards]);variations={c['recipeId']:delta(c['operational'],shared) for c in cards}
    assert all(merge(shared,variations[c['recipeId']])==c['operational'] for c in cards)
    source=read(AUDIT/'COOKING_SOURCE_EVIDENCE.json')
    intro='''Codex to Calibration Review: exact Cooking manuscript review, following your completed source conference d4ee39f9-b5b9-41b7-87bd-4fc4d09e843f (reply 2988d5a5-60a9-4142-b0be-a9f42a809ca0).

All 44 Cooking cards are authored: 30 public, two restricted and twelve Director-only. Please review the complete shared guide and all 44 internal cards below against the full source records, source-monster passages and nine decisions from our immediately preceding source conference. This is an exact authored campaign-playtest review, not balance, runtime or whole-game certification. Cosmology remains strictly deferred until the final authorized GitHub push succeeds and its remote commit is verified. No source deletion or push has occurred.

The source-fidelity check passes: original sources and 24 protected prior-rule artifacts are byte-for-byte unchanged; all 30 public effects match exact V5 paragraphs. Source requirements, every component occurrence, current/legacy fields, visibility and economics are preserved in the JSON. Original recipe tags are separated from operative mechanics.tag. The bestiary discrepancy is recorded in the coverage ledger for later mechanical correction, not silently used as donor authority.

Please give a bounded approve/repair verdict. Specifically assess these additional implementation choices rather than treating them as previously approved:
1. Sixteen named ordinary food inputs count as nutritive bulk; every other ingredient is still required but conservatively receives zero credit. Exact occurrence-level maps and supplement arithmetic are in the cards/machine projections. Oil means actual food-grade cooking oil. This avoids assuming all roots, marrow or magical material are edible.
2. Reserve maximum possible supplemental food before the check; consume only the actual food needed by the resolved quantity/catalyst choice. Unincorporated surplus stays ordinary food. For failure, source inputs use the existing recovery rules; incorporated supplements do too, while still-unincorporated supplements remain inventory. Recipe-633 consumes its contaminated serving's actual inputs with no recovery. Please identify any needed precise incorporation boundary.
3. Borrowed walking/climbing/swimming gives a donor printed base/floor, not additive speed. Apply actual recipient modifiers/restrictions once, preserving zero-Speed and halving; missing climb/swim can be gained, missing walking cannot. Please resolve any composition ambiguity explicitly.
4. Dedicated mundane Meal Crock quality improves maximum HP 2 to 3 only once; it cannot compound through recooking or repair unrelated containers/tools. Existing current damage needs an actual applicable repair/creation procedure. Please specify if the improved dedicated crock needs an explicit current-HP adjustment.
5. Immediate consumption waives storage only with actual ready recipients and serving access at completion; all remainders still require real reserved capacity. Check this against maximum-yield reservation and ten-minute consumption.

Please also verify all-or-none feast replacement, independent temporary HP, exact rider clocks, RP without an invented rest cap, 633 failure/nutrition/exposure, and 632/634/635 donor prerequisites/actual Masterwork trigger. If finite repairs suffice, state whether the full 44-card set is approved after those exact edits without another general conference. Retain all unfinished whole-game/balance/runtime gates.

Packet format: the shared guide and internal card manuscript are reproduced in full. Complete operational JSON is losslessly factored as COMMON + per-recipe recursive overrides; applying each override reconstructs its exact original operational object (locally asserted for all 44). Source Requirements/components are identical to the full records supplied in the source conference and repeated in card ingredient/work listings; their unchanged source indices and hash bind that evidence. No public/restricted visibility is expanded by this private review packet.
'''
    blocks=[intro,'\nFULL SHARED GUIDE\n',(ROOT/'docs/mechanics/COOKING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8'),'\nFULL INTERNAL CARD MANUSCRIPT\n',(ROOT/'docs/director-only/COOKING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8'),'\nCOMPLETE FACTORED OPERATIONAL JSON\n',compact({'envelope':{k:v for k,v in data.items() if k!='cards'},'common':shared,'recipeOverrides':variations}),'\nIMMUTABLE SOURCE BINDINGS\n',compact({'sourceSha256':source['sourceSha256'],'bookSha256':source['bookSha256'],'sourceIndices':source['sourceIndices'],'publicBookBindings':source['publicBookBindings']}),'\nWORKED RULE TRACES\n',(AUDIT/'COOKING_REVIEW_CASES.md').read_text(encoding='utf-8'),'\nVALIDATION REPORT\n',compact(v)]
    packet='\n'.join(blocks);target.write_text(packet,encoding='utf-8')
    artifacts=['docs/mechanics/COOKING_RECIPE_PLAYTEST.md','docs/mechanics/COOKING_PUBLIC_RECIPE_CARDS.md','docs/director-only/COOKING_INTERNAL_RECIPE_CARDS.md','data/playtest/cooking_recipe_candidate.json','data/director/cooking_recipe_candidate_internal.json']
    submission={'status':'prepared-not-sent','sourceConferenceTurnId':data['sourceConferenceTurnId'],'packetCharacters':len(packet),'packetSha256':sha(target),'losslessOperationalReconstructions':44,'artifactHashes':{str((ROOT/p).relative_to(GAME)).replace('\\','/'):sha(ROOT/p) for p in artifacts}}
    (AUDIT/'COOKING_EXACT_SUBMISSION.json').write_text(json.dumps(submission,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'characters':len(packet),'reconstructed':44,'checks':len(v['checks'])}))
if __name__=='__main__':main()
