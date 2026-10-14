"""Two losslessly reconstructed messages for the independent exact-card review."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json
from prepare_tailoring_exact_review import factor
from prepare_cooking_exact_review import merge
from build_jewelcrafting_recipe_candidate import ROOT,GAME,AUDIT,read,sha,write,dump,public_projection

def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))

def main():
    target=AUDIT/'JEWELCRAFTING_EXACT_PART2_SUBMISSION.json';assert not target.exists(),'Preserve existing submission; use explicit revision'
    data=read(ROOT/'data/director/jewelcrafting_recipe_candidate_internal.json');public=read(ROOT/'data/playtest/jewelcrafting_recipe_candidate.json')
    report=read(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json');assert report['status']=='PASS' and report['checkCount']==98
    assert report['remainingRequiredEvidence']==['separate GPT exact-card review']
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    baseline=read(AUDIT/'JEWELCRAFTING_PART2_SUBMISSION.json')['protectedFiles'];assert all(sha(GAME/p)==h for p,h in baseline.items())
    cards=data['cards'];sources=factor([c['sourceRecipe'] for c in cards]);metadata=[{k:v for k,v in c.items() if k not in ('sourceRecipe','operational')} for c in cards]
    ops=[]
    for c in cards:
        op=deepcopy(c['operational']);op.pop('text');ops.append(op)
    operations=factor(ops)
    manuscript=(ROOT/'docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8');paras=manuscript.split('\n\n');counts=Counter(paras)
    shared={f'P{i+1}':p for i,p in enumerate(p for p in dict.fromkeys(paras) if counts[p]>1 and len(p)>90)};reverse={p:k for k,p in shared.items()}
    template='\n\n'.join('[[PARAGRAPH '+reverse[p]+']]' if p in reverse else p for p in paras);reconstructed=template
    for k,p in shared.items():reconstructed=reconstructed.replace('[[PARAGRAPH '+k+']]',p)
    assert reconstructed==manuscript
    for i,c in enumerate(cards):
        start=manuscript.index('## '+c['recipeId']+' — ');end=manuscript.find('\n## recipe-',start+1);section=manuscript[start:end if end>=0 else len(manuscript)]
        text=section.split('**Operational effect:** ',1)[1].split('\n\n',1)[0];op=merge(operations['COMMON'],operations['orderedOverrides'][i]);op['text']=text
        assert {**metadata[i],'sourceRecipe':merge(sources['COMMON'],sources['orderedOverrides'][i]),'operational':op}==c
    assert [public_projection(c) for c in cards if c['visibility']=='public']==public['cards']
    public_md=(ROOT/'docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8');public_paras=public_md.split('\n\n')
    allshared={p:'I'+str(i+1) for i,p in enumerate(dict.fromkeys(paras)) if p in public_paras}
    public_template='\n\n'.join('[[INTERNAL PARAGRAPH '+allshared[p]+']]' if p in allshared else p for p in public_paras);rebuilt=public_template
    for p,k in allshared.items():rebuilt=rebuilt.replace('[[INTERNAL PARAGRAPH '+k+']]',p)
    assert rebuilt==public_md
    mapping={k:paras.index(p) for p,k in allshared.items()}
    envelope={k:v for k,v in data.items() if k not in ('cards','baseModels')};public_envelope={k:v for k,v in public.items() if k not in ('cards','baseModels')}
    used={m for c in public['cards'] for m in c['operational']['baseModelIds']};public_models={k:v for k,v in data['baseModels'].items() if k in used}
    assert {**public_envelope,'baseModels':public_models,'cards':[public_projection(c) for c in cards if c['visibility']=='public']}==public
    cover='''Codex to Calibration Review Part 2: exact Jewelcrafting operational PLAYTEST candidate in TWO parts. Please acknowledge PART A only and wait for PART B before a verdict.

Your JC-D01–JC-D16 source disposition (turn96dbc19c-068f-4f2c-a81f-c2ea87d75f25, replyc510dda9-431e-478b-92ee-5ea6d42407e8) has been applied to all43 authored cards:26public,1restricted,16Director-only. Ten internal/nine public body models and14internal/12public tag predicates are supplied. Current totals remain305/687,382remaining;public197/433. No Jewelcrafting promotion.

Your requested verbatim Markdown export is locally preserved as GPT_JEWELCRAFTING_SOURCE_CONFERENCE.md (49,702 characters, SHA256 dab0f12647473f4324adc541acd539f41ae457bcae1bbdb65fc6e7ed984ecc85). Its first20,000 characters exactly match the original connector response; its remaining sections were also read in Chrome. The export request made no new rulings.

The candidate retains all200 component occurrences,11actual catalysts and26V5 public bindings. All54 protected source/reviewed-rule inputs remain unchanged. Local evidence has98checks,69positive/causal-negative predicate cases,486structural states and86ordinary/Large values. These are reported local results, not file operations attributed to you. Governing-system premises such as actual causal qualification, anatomy, fit, tools and placement remain explicitly adjudicated; the helper is not companion runtime.

Creation retains the supplied framework's otherwise legal untrained level1–4 attempts with disadvantage; actual kit/station requirements still apply. Repair remains trained-only. Same-timestamp creation records the authoritative campaign scheduler's already-processed dawn checkpoint, preventing recreation/replay of that event.

PART A contains the exact source verdict, both exact guides, all complete source records and metadata, both candidate envelopes and complete models. PART B contains exact internal/public card manuscripts, complete operations, projection proof, source-valid walkthroughs, reference code and validation assertions/results.

Lossless factoring: recursively merge COMMON with each orderedOverrides entry; dictionaries merge, arrays/scalars replace. Preserve null versus absent fields. Ordered index i matches metadata[i]. All43 objects reconstruct exactly. Public filtering removes private records and nested guidance throughout the envelope; it also selects only the nine used bodies and twelve used tag entries. The complete public envelope is separately supplied.

After BOTH parts, give exact operational approval or a finite correction list. If conditional, say explicitly whether completing those corrections and checks permits promotion without another generic conference. This requests no human balance, material availability, runtime, whole-game flow or publication approval. No source deletion or push occurred. Cosmology remains after the authorized successful GitHub push and verified remote commit.
'''
    evidence=read(AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json')
    partA='\n\n'.join([cover,'FULL COMPLETED SOURCE DISPOSITION',(AUDIT/'GPT_JEWELCRAFTING_SOURCE_CONFERENCE.md').read_text(encoding='utf-8'),'EXACT INTERNAL SHARED GUIDE',(ROOT/'docs/director-only/JEWELCRAFTING_INTERNAL_GUIDE.md').read_text(encoding='utf-8'),'EXACT PUBLIC SHARED GUIDE',(ROOT/'docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8'),'COMPLETE SOURCE RECORDS',compact(sources),'COMPLETE CARD METADATA INCLUDING PUBLIC PARAGRAPH BINDINGS',compact(metadata),'COMPLETE INTERNAL CANDIDATE ENVELOPE',compact(envelope),'COMPLETE PUBLIC CANDIDATE ENVELOPE',compact(public_envelope),'ALL TEN BODY MODELS',compact(data['baseModels']),'SOURCE HASHES AND INDICES',compact({k:evidence[k] for k in ('sourceSha256','bookSha256','sourceIndices')}),'END PART A. Acknowledge receipt only; wait for Part B.'])
    coverB='''Codex: PART B completes the exact Jewelcrafting candidate. Please now review all43 cards and both projections.

Expand [[PARAGRAPH Pn]] from the dictionary to reconstruct the entire internal manuscript. Merge operational COMMON and each ordered override; restore its text from that card's exact **Operational effect:** paragraph. Combined with Part A metadata/source records this reconstructs all43 internal card objects exactly. Public [[INTERNAL PARAGRAPH In]] references use the map to zero-based paragraphs of the reconstructed internal manuscript split on double newline. All other text is literal. The26public-card manuscript reconstructs exactly, as do the entire public guide and JSON envelope under the supplied projection report.

Audit all14causal domains and their exclusions; each item's independent premises before maximum selection; shared check/separate save families; wearer-only benefits; slots and physical conflicts; weaker-jewel charge with stronger-item modifier; before-dice commitment and debit deduplication; repeated saves and copied results; initial/dawn ledger chronology including same-timestamp creation; suppression/Broken/meld/return/custody; exact body/primary-setting repair; latest damage and structural-only quality; catalysts, real tools and work; values and public visibility.

The supplied fit/causal/placement flags are independent governing-world premises, not proof of those facts. Read the exact prose and walkthroughs as well as code. Current approvals remain305/687,public197/433; zero Jewelcrafting cards promoted. State exact approval or finite repairs and whether implementing them permits promotion. Cosmology remains post-push only.
'''
    partB='\n\n'.join([coverB,'EXACT INTERNAL SHARED PARAGRAPHS',compact(shared),'COMPLETE EXACT INTERNAL MANUSCRIPT',template,'COMPLETE OPERATIONAL OBJECTS',compact(operations),'PUBLIC PARAGRAPH INDEX MAP',compact(mapping),'COMPLETE EXACT PUBLIC MANUSCRIPT',public_template,'WHOLE PUBLIC PROJECTION PROOF',compact(read(AUDIT/'JEWELCRAFTING_PUBLIC_PARAGRAPH_PROJECTION.json')),'SOURCE-BOUND INTERFACE WALKTHROUGHS AND16-DECISION COVERAGE',(AUDIT/'JEWELCRAFTING_INTERFACE_WALKTHROUGHS.md').read_text(encoding='utf-8'),'LOCAL98-CHECK VALIDATION REPORT',compact(report),'BOUNDED JEWELCRAFTING REFERENCE',(ROOT/'tools/jewelcrafting_reference.py').read_text(encoding='utf-8'),'UNCHANGED REVIEWED TAILORING DEPENDENCY',(ROOT/'tools/tailoring_reference.py').read_text(encoding='utf-8'),'UNCHANGED REVIEWED LEATHERWORKING DEPENDENCY',(ROOT/'tools/leatherworking_reference.py').read_text(encoding='utf-8'),'VALIDATION ASSERTIONS',(ROOT/'tools/validate_jewelcrafting_recipe_candidate.py').read_text(encoding='utf-8'),'END COMPLETE EXACT REVIEW PACKET. No promotion yet.'])
    state={'status':'prepared-not-sent','threadId':data['sourceAuthority']['threadId'],'parts':{},'losslessSourceReconstructions':43,'losslessOperationalReconstructions':43,'losslessInternalCardReconstructions':43,'losslessPublicCardReconstructions':26,'losslessInternalManuscript':True,'losslessPublicManuscript':True,'wholePublicEnvelopeEqual':True,'baseModels':10,'publicBaseModels':9,'tags':14,'publicTags':12,'artifactHashes':report['artifactHashes'],'supportHashes':{p.name:sha(p) for p in [ROOT/'tools/jewelcrafting_reference.py',ROOT/'tools/validate_jewelcrafting_recipe_candidate.py',AUDIT/'JEWELCRAFTING_INTERFACE_WALKTHROUGHS.md',AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json',AUDIT/'JEWELCRAFTING_PUBLIC_PARAGRAPH_PROJECTION.json']},'recipesApproved':0,'reviewedTotal':305,'remaining':382,'publicReviewed':197,'cosmology':'post-push only'}
    for label,text in [('A_RULES_SOURCE',partA),('B_EXACT_CARDS',partB)]:
        path=AUDIT/f'CODEX_JEWELCRAFTING_EXACT_PART2_{label}.txt';assert not path.exists();write(path,text);state['parts'][label]={'file':path.name,'characters':len(text),'sha256':sha(path),'sent':False}
    dump(target,state);print(compact({'parts':state['parts'],'reconstructedCards':43,'publicCards':26}))

if __name__=='__main__':main()
