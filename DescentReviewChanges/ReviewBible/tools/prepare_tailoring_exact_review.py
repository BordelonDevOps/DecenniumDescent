"""Losslessly factor the exact candidate into two sequential notebook messages."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from prepare_cooking_exact_review import common,delta,merge
from build_tailoring_recipe_candidate import public_projection

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
    status_path=AUDIT/'TAILORING_EXACT_PART2_SUBMISSION.json'
    assert not status_path.exists(),'Preserve existing prepared/sent exact packet; use an explicit revised packet if needed.'
    data=read(ROOT/'data/director/tailoring_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/tailoring_recipe_candidate.json')
    report=read(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json');assert report['status']=='PASS'
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    cards=data['cards'];sources=factor([c['sourceRecipe'] for c in cards]);metadata=[{k:v for k,v in c.items() if k not in ('sourceRecipe','operational')} for c in cards]
    ops=[]
    for c in cards:
        o=deepcopy(c['operational']);o.pop('text');ops.append(o)
    operation=factor(ops)
    manuscript=(ROOT/'docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
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
    internal_guide=(ROOT/'docs/director-only/TAILORING_INTERNAL_GUIDE.md').read_text(encoding='utf-8')
    public_guide=(ROOT/'docs/mechanics/TAILORING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    # Keep exact public guide and card text as factored differences, not assumed equivalents.
    public_md=(ROOT/'docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    public_paras=public_md.split('\n\n');allshared={p:'I'+str(i+1) for i,p in enumerate(dict.fromkeys(paras)) if p in public_paras}
    public_template='\n\n'.join('[[INTERNAL PARAGRAPH '+allshared[p]+']]' if p in allshared else p for p in public_paras)
    public_reconstructed=public_template
    for p,k in allshared.items():public_reconstructed=public_reconstructed.replace('[[INTERNAL PARAGRAPH '+k+']]',p)
    assert public_reconstructed==public_md
    mapping={k:paras.index(p) for p,k in allshared.items()}
    cover='Codex to Calibration Review Part 2: exact Tailoring operational PLAYTEST candidate review, in TWO parts. Please acknowledge PART A only and wait for PART B before a verdict.\n\nYour completed TA-D01..16 source conference (turn6b7474ed-1bca-40b8-81af-7bfbd843a5cc, reply95ba16b4-b85f-47d8-bc61-047f9ebfcdeb) is preserved and implemented in43 authored cards,29 public,4 restricted,10 Director-only,15 finite body models,11 public models. Current reviewed count remains262/687,425remaining; public168/433. None of these43 is approved yet. All53 protected input files remain unchanged.\n\nPART A contains the full readable source verdict, exact internal/public guides, complete factored source records, all body profiles, public paragraph bindings and candidate envelope. PART B contains every exact authored card, operational projection, exact public manuscript projection and validation/reference evidence.\n\nRecursively merge COMMON with each orderedOverrides entry. Dictionaries merge; arrays and scalars replace; legitimate nulls and absent fields stay distinct. Ordered index i matches card metadata[i]. This factoring has been reconstructed locally to assert exact equality. Public projection removes private guidance/nested private objects, selects only public recipes and their used body models.\n\nThe local check pass has120 checks and558 durability states. Those are reported local results, not file operations attributed to you. Bounded helpers take actual fit, anatomy, task circumstances and placement as governing-system premises. Please assess the actual prose as well as helpers.\n\nAfter both parts, approve the authored operational scope or list finite corrections, explicitly saying whether implementing those and passing checks permits promotion without another generic conference. This does not request human balance, availability, companion runtime, whole-game flow or publication approval. No deletion or push occurred. Cosmology remains strictly after the successful authorized GitHub push and verification of its remote commit.\n'
    envelope={k:v for k,v in data.items() if k not in ('cards','baseModels')}
    evidence=read(AUDIT/'TAILORING_SOURCE_PREPARATION.json')
    pA='\n'.join([cover,'FULL COMPLETED SOURCE VERDICT',(AUDIT/'GPT_TAILORING_SOURCE_CONFERENCE.md').read_text(encoding='utf-8'),
      'FULL EXACT INTERNAL SHARED GUIDE',internal_guide,'FULL EXACT PUBLIC SHARED GUIDE',public_guide,
      'COMPLETE SOURCE RECORDS COMMON + ORDERED OVERRIDES',compact(sources),'CARD METADATA INCLUDING FULL PUBLIC PARAGRAPH BINDINGS',compact(metadata),
      'COMPLETE CANDIDATE ENVELOPE',compact(envelope),'ALL15 COMPLETE BODY MODELS (FIVE ORIGINAL EQUIPMENT RECORDS INCLUDED)',compact(data['baseModels']),
      'IMMUTABLE SOURCE HASHES AND INDICES',compact({k:evidence[k] for k in ('sourceSha256','bookSha256','sourceIndices')}),
      'END PART A. Please acknowledge receipt; Part B follows.'])
    coverB='Codex: PART B completes the exact Tailoring review packet. Please now review all43 authored cards and both projections.\n\nExpand each [[PARAGRAPH Pn]] from the shared dictionary to reconstruct the exact saved internal manuscript. Operational objects merge COMMON and their ordered override; their text is the exact **Operational effect:** paragraph in that same card. Together with Part A sources/metadata these reconstruct all43 internal cards exactly. Public [[INTERNAL PARAGRAPH In]] references use the supplied map to zero-based paragraphs in the reconstructed internal manuscript split on double newline; all other text is literal. The saved29-card public manuscript reconstructs exactly.\n\nPlease audit source preservation,15/11 body models and91 ordinary reference combinations; wearer/operator scopes; shared garment slots and cross-trade task arbitration; absent AC candidates against Crude; seven resistance recipes; Bag geometry/relief/custody/suppression/Broken/meld/return/rescuers; original pair/outfit reconstruction; latest damage and noncompounding quality;25 reusable tool occurrences; source-null year, work phases, repair and sale reference arithmetic. Check actual prose even if a local test passes.\n\nReference calculations are isolated evidence, not companion runtime. State a precise approval or finite repair list and whether completing the repairs permits promotion. Existing reviewed counts remain262; zero Tailoring promotions.\n'
    pB='\n'.join([coverB,'EXACT MANUSCRIPT SHARED PARAGRAPHS',compact(shared_paras),
      'COMPLETE43-CARD INTERNAL MANUSCRIPT WITH EXACT REFERENCES',template,
      'COMPLETE OPERATIONAL PROJECTION COMMON + ORDERED OVERRIDES',compact(operation),
      'PUBLIC INTERNAL-PARAGRAPH INDEX MAP',compact(mapping),'COMPLETE EXACT PUBLIC MANUSCRIPT TEMPLATE',public_template,
      'LOCAL VALIDATION REPORT,120 CHECKS AND558 DURABILITY STATES',compact(report),
      'BOUNDED REFERENCE CALCULATION SOURCE',(ROOT/'tools/tailoring_reference.py').read_text(encoding='utf-8'),
      'REVIEWED LEATHERWORKING HELPER DEPENDENCY',(ROOT/'tools/leatherworking_reference.py').read_text(encoding='utf-8'),'VALIDATION ASSERTIONS (INCLUDING INDEPENDENT EXPECTED CASES)',(ROOT/'tools/validate_tailoring_recipe_candidate.py').read_text(encoding='utf-8'),
      'END COMPLETE TAILORING EXACT REVIEW PACKET. No recipes promoted yet.'])
    status={'status':'prepared-not-sent','threadId':data['sourceAuthority']['threadId'],'parts':{},'losslessSourceReconstructions':43,'losslessOperationalReconstructions':43,'losslessInternalCardReconstructions':43,'losslessPublicCardReconstructions':29,'losslessInternalManuscript':True,'losslessPublicManuscript':True,'baseModels':15,'publicBaseModels':11,'artifactHashes':report['artifactHashes'],'recipesApproved':0,'reviewedTotal':262,'remaining':425,'cosmology':'post-push only'}
    for label,t in [('A_RULES_SOURCE',pA),('B_EXACT_CARDS',pB)]:
        path=AUDIT/f'CODEX_TAILORING_EXACT_PART2_{label}.txt';assert not path.exists();write(path,t)
        status['parts'][label]={'file':path.name,'characters':len(t),'sha256':sha(path),'sent':False}
    write(status_path,json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'parts':status['parts'],'reconstructedCards':43,'publicReconstructedCards':29}))

if __name__=='__main__':main()
