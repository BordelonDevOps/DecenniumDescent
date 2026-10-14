"""Losslessly factor the exact candidate into two sequential notebook messages."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from prepare_cooking_exact_review import common,delta,merge
from build_leatherworking_recipe_candidate import public_projection

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def factor(ds):
    shared=common(ds);diffs=[delta(d,shared) for d in ds]
    assert all(merge(shared,d)==original for d,original in zip(diffs,ds))
    return {'COMMON':shared,'orderedOverrides':diffs}

def main():
    status_path=AUDIT/'LEATHERWORKING_EXACT_PART2_SUBMISSION.json'
    assert not status_path.exists(),'Preserve existing prepared/sent exact packet; use an explicit revised packet if needed.'
    data=read(ROOT/'data/director/leatherworking_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/leatherworking_recipe_candidate.json')
    report=read(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json');assert report['status']=='PASS'
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    cards=data['cards'];sources=factor([c['sourceRecipe'] for c in cards]);metadata=[{k:v for k,v in c.items() if k not in ('sourceRecipe','operational')} for c in cards]
    ops=[]
    for c in cards:
        o=deepcopy(c['operational']);o.pop('text');ops.append(o)
    operation=factor(ops)
    manuscript=(ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    paras=manuscript.split('\n\n');counts=Counter(paras)
    shared_paras={f'P{i+1}':p for i,p in enumerate(p for p in dict.fromkeys(paras) if counts[p]>1 and len(p)>90)}
    reverse={p:k for k,p in shared_paras.items()}
    template='\n\n'.join('[[PARAGRAPH '+reverse[p]+']]' if p in reverse else p for p in paras)
    reconstructed=template
    for k,p in shared_paras.items():reconstructed=reconstructed.replace('[[PARAGRAPH '+k+']]',p)
    assert reconstructed==manuscript
    for i,c in enumerate(cards):
        begin=manuscript.index('## '+c['recipeId']+' — ');end=manuscript.find('\n## recipe-',begin+1);section=manuscript[begin:end if end>=0 else len(manuscript)]
        text=section.split('**Operational effect:** ',1)[1].split('\n\n',1)[0]
        op=merge(operation['COMMON'],operation['orderedOverrides'][i]);op['text']=text
        restored={**metadata[i],'sourceRecipe':merge(sources['COMMON'],sources['orderedOverrides'][i]),'operational':op}
        assert restored==c,c['recipeId']
    expected_public=[public_projection(c) for c in cards if c['visibility']=='public']
    assert expected_public==public['cards']
    public_ids={id for c in expected_public for id in c['operational']['baseModelIds']}
    assert public['baseModels']=={k:v for k,v in data['baseModels'].items() if k in public_ids}
    internal_guide=(ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_GUIDE.md').read_text(encoding='utf-8')
    public_guide=(ROOT/'docs/mechanics/LEATHERWORKING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    # Keep exact public guide and card text as factored differences, not assumed equivalents.
    public_md=(ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    public_paras=public_md.split('\n\n');allshared={p:'I'+str(i+1) for i,p in enumerate(dict.fromkeys(paras)) if p in public_paras}
    public_template='\n\n'.join('[[INTERNAL PARAGRAPH '+allshared[p]+']]' if p in allshared else p for p in public_paras)
    public_reconstructed=public_template
    for p,k in allshared.items():public_reconstructed=public_reconstructed.replace('[[INTERNAL PARAGRAPH '+k+']]',p)
    assert public_reconstructed==public_md
    mapping={k:paras.index(p) for p,k in allshared.items()}
    cover='''Codex to Calibration Review Part 2: exact Leatherworking candidate review, in TWO parts.

Your completed source/interface conference turn86413ad7-8096-4e6f-baca-3cab34aa66a3/reply4f808c26-f93b-4b50-ac05-a917b7ca2b7e is captured in full and implemented in 44 authored cards (30 public,1 restricted,13 Director-only), 19 finite body profiles and separate public/internal guides. There is no Leatherworking card approval yet: current pass218/687 reviewed,469remaining; public138/433. All42 protected original/reviewed files remain unchanged. No source deletion, GitHub push or cosmology review occurred.

Please wait for PART B before delivering the exact-card verdict. Acknowledge this PART A receipt only. PART A supplies the full source verdict, exact guide/body rules, all44 losslessly factored original source records, full19 body models, source/public bindings and candidate envelope. PART B supplies all44 exact authored cards, complete operational projections, public text projection and independent validation/reference evidence.

When both parts are present, review the actual authored operational PLAYTEST scope and identify finite repairs or approve that scope. If precise finite edits suffice, state whether implementing them and passing validation allows promotion without another generic source conference. This does not request human balance, source-material availability, companion runtime, whole-game flow or publication approval. Cosmology remains after the successful authorized GitHub push and verification of its remote commit.

The first local check pass has89 checks,50 worked cases,2,832 durability states and1,065 burden states; these are reported local results, not checks attributed to you. Geometry helpers prove only explicit orthogonal box layouts; they do not claim a universal shape/diagonal-fitting algorithm. Actual permissions, body fit and placement remain governing-system premises.

Lossless dictionary rule: recursively merge COMMON with each orderedOverrides entry. Dictionaries merge recursively; arrays/scalars replace. Lists keep their exact order. Null fields are real preserved values. Index i corresponds to card metadata[i]. No recipe source field is removed from the internal record. Public projection removes private guidance/nested private records only, preserves legitimate nulls, and selects exactly public cards plus their used bodies. The public text is also supplied exactly through references in Part B.
'''
    envelope={k:v for k,v in data.items() if k not in ('cards','baseModels')}
    evidence=read(AUDIT/'LEATHERWORKING_SOURCE_PREPARATION.json')
    pA='\n'.join([cover,'FULL COMPLETED SOURCE VERDICT',(AUDIT/'GPT_LEATHERWORKING_SOURCE_CONFERENCE.txt').read_text(encoding='utf-8'),
      'FULL EXACT INTERNAL SHARED GUIDE',internal_guide,'FULL EXACT PUBLIC SHARED GUIDE',public_guide,
      'COMPLETE SOURCE RECORDS COMMON + ORDERED OVERRIDES',compact(sources),'CARD METADATA INCLUDING FULL PUBLIC PARAGRAPH BINDINGS',compact(metadata),
      'COMPLETE CANDIDATE ENVELOPE',compact(envelope),'ALL19 COMPLETE BODY MODELS (FOUR ORIGINAL EQUIPMENT RECORDS INCLUDED)',compact(data['baseModels']),
      'IMMUTABLE SOURCE HASHES AND INDICES',compact({k:evidence[k] for k in ('sourceSha256','bookSha256','sourceIndices')}),
      'END PART A. Please acknowledge receipt; Part B follows.'])
    coverB='''Codex: PART B of the exact Leatherworking candidate review. PART A already supplied full decisions, guides, all44 source records,19 body models and card metadata. This completes the packet; please now deliver the exact-card approve/finite-repair verdict for all44.

Expand each [[PARAGRAPH Pn]] token with its literal shared paragraph from the dictionary below. The result is the complete exact saved internal manuscript. Each operational JSON object is COMMON recursively merged with its ordered override, then its text field is the exact **Operational effect:** paragraph in that same card. Combined with Part A source/metadata this reconstructs all44 complete internal card objects exactly, locally asserted.

The exact public manuscript uses [[INTERNAL PARAGRAPH In]] tokens. Map each In to its zero-based paragraph index in the fully reconstructed internal manuscript split on double newline; all other public text is literal. The public header and any changed paragraphs are retained literally. Local reconstruction equals the saved30-card public manuscript exactly. Its JSON is the public projection described in Part A, retaining exactly14 used models; the guide and full recipe visibility boundary are independently checked.

Please especially audit the explicit numerical AC overlay against unchanged V5 prose, strong negative/zero arbitration, real geometry versus relief, five positions, printed Load and inclusive weights, all immediate custody subtrees, transfer/suppression/Broken/placement/meld/return/rescuer cases, actual operator/task scope and Action/hands costs, latest completion damage, persistent flaw/durability, source-null year and source trivial thresholds, pair reconstruction, finished unit repair price, and all source/public information preservation.

The reference model is isolated evidence, not a live implementation or replacement for the complete prose. No new authority is inferred from a passing test. Tell us if the actual cards/guide require finite corrections despite those tests.
'''
    pB='\n'.join([coverB,'EXACT MANUSCRIPT SHARED PARAGRAPHS',compact(shared_paras),
      'COMPLETE44-CARD INTERNAL MANUSCRIPT WITH EXACT REFERENCES',template,
      'COMPLETE OPERATIONAL PROJECTION COMMON + ORDERED OVERRIDES',compact(operation),
      'PUBLIC INTERNAL-PARAGRAPH INDEX MAP',compact(mapping),'COMPLETE EXACT PUBLIC MANUSCRIPT TEMPLATE',public_template,
      'LOCAL VALIDATION REPORT AND ALL50 WORKED CASES',compact(report),
      'BOUNDED REFERENCE CALCULATION SOURCE',(ROOT/'tools/leatherworking_reference.py').read_text(encoding='utf-8'),
      'VALIDATION ASSERTIONS (INCLUDING INDEPENDENT EXPECTED CASES)',(ROOT/'tools/validate_leatherworking_recipe_candidate.py').read_text(encoding='utf-8'),
      'END COMPLETE LEATHERWORKING EXACT REVIEW PACKET. No recipes promoted yet.'])
    status={'status':'prepared-not-sent','threadId':data['sourceConferenceThreadId'],'parts':{},'losslessSourceReconstructions':44,'losslessOperationalReconstructions':44,'losslessInternalCardReconstructions':44,'losslessPublicCardReconstructions':30,'losslessInternalManuscript':True,'losslessPublicManuscript':True,'baseModels':19,'publicBaseModels':14,'artifactHashes':report['artifactHashes'],'recipesApproved':0,'reviewedTotal':218,'remaining':469,'cosmology':'post-push only'}
    for label,t in [('A_RULES_SOURCE',pA),('B_EXACT_CARDS',pB)]:
        path=AUDIT/f'CODEX_LEATHERWORKING_EXACT_PART2_{label}.txt';assert not path.exists();write(path,t)
        status['parts'][label]={'file':path.name,'characters':len(t),'sha256':sha(path),'sent':False}
    write(status_path,json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'parts':status['parts'],'reconstructedCards':44,'publicReconstructedCards':30}))

if __name__=='__main__':main()
