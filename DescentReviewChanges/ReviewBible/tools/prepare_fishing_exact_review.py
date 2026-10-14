"""Preserve and losslessly package the exact Fishing candidate in three parts."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import json,re
from prepare_tailoring_exact_review import factor
from prepare_cooking_exact_review import merge
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,write,dump,public_projection


def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))


def main():
    target=AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json'
    assert not target.exists(),'Existing prepared/submitted revision must be preserved'
    data=read(ROOT/'data/director/fishing_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/fishing_recipe_candidate.json')
    pre=read(AUDIT/'FISHING_PRELIMINARY_VALIDATION.json')
    seq=read(AUDIT/'FISHING_SEQUENCE_VALIDATION.json')
    assert len(pre['checks'])==130 and len(seq['checks'])==90
    assert all(c['pass'] for c in pre['checks']+seq['checks'])
    hashes=read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs']
    assert all(sha(ROOT/p)==h for p,h in hashes.items())
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert all(sha(GAME/p)==h for p,h in baseline.items())
    cards=data['cards'];sources=factor([c['sourceRecipe'] for c in cards])
    metadata=[{k:v for k,v in c.items() if k not in ('sourceRecipe','operational')} for c in cards]
    ops=[]
    for c in cards:
        op=deepcopy(c['operational']);op.pop('text');ops.append(op)
    operations=factor(ops)
    manuscript=(ROOT/'docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    paras=manuscript.split('\n\n');counts=Counter(paras)
    shared={f'P{i+1}':p for i,p in enumerate(p for p in dict.fromkeys(paras) if counts[p]>1 and len(p)>90)}
    reverse={p:k for k,p in shared.items()}
    template='\n\n'.join('[[PARAGRAPH '+reverse[p]+']]' if p in reverse else p for p in paras)
    rebuilt=template
    for k,p in shared.items():rebuilt=rebuilt.replace('[[PARAGRAPH '+k+']]',p)
    assert rebuilt==manuscript
    sections={}
    for i,c in enumerate(cards):
        start=manuscript.index('## '+c['recipeId']+' — ');end=manuscript.find('\n## recipe-',start+1)
        section=manuscript[start:end if end>=0 else len(manuscript)];sections[c['recipeId']]=section
        text=section.split('**Operational effect:** ',1)[1].split('\n\n',1)[0]
        op=merge(operations['COMMON'],operations['orderedOverrides'][i]);op['text']=text
        assert {**metadata[i],'sourceRecipe':merge(sources['COMMON'],sources['orderedOverrides'][i]),'operational':op}==c
    public_md=(ROOT/'docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    public_header=('# Fishing public recipe cards\n\n**DRAFT; exact review pending.** Public: 28 formulas, nine models and thirteen operative affinities.\n\n'
        'Every card uses the complete [shared guide](FISHING_RECIPE_PLAYTEST.md). The JSON preserves full source objects.\n\n')
    # Independent paragraph projection: retain complete public sections and omit
    # only the explicit internal optional-guidance paragraph, preserving bytes.
    expected_sections=[]
    for c in cards:
        if c['visibility']!='public':continue
        s=sections[c['recipeId']]
        s=re.sub(r'\*\*Preserved optional Director guidance \(inactive pending separate variant review\):\*\* [^\n]*\n\n','',s)
        expected_sections.append(s.rstrip('\n'))
    expected_md=public_header+'\n\n'.join(expected_sections)+'\n'
    assert expected_md==public_md,'Independent public manuscript reconstruction differs'
    assert [public_projection(c) for c in cards if c['visibility']=='public']==public['cards']
    public_paras=public_md.split('\n\n')
    shared_public={p:'I'+str(i+1) for i,p in enumerate(dict.fromkeys(paras)) if p in public_paras}
    public_template='\n\n'.join('[[INTERNAL PARAGRAPH '+shared_public[p]+']]' if p in shared_public else p for p in public_paras)
    rebuilt_public=public_template
    for p,k in shared_public.items():rebuilt_public=rebuilt_public.replace('[[INTERNAL PARAGRAPH '+k+']]',p)
    assert rebuilt_public==public_md
    mapping={k:paras.index(p) for p,k in shared_public.items()}
    envelope={k:v for k,v in data.items() if k not in ('cards','baseModels')}
    public_envelope={k:v for k,v in public.items() if k not in ('cards','baseModels')}
    assert {**public_envelope,'baseModels':data['baseModels'],'cards':[public_projection(c) for c in cards if c['visibility']=='public']}==public
    walkthrough=(AUDIT/'FISHING_WORKED_SCENARIOS.md').read_text(encoding='utf-8')
    assert re.findall(r'^## FI-(\d\d)',walkthrough,re.M)==[f'{n:02}' for n in range(1,25)]
    # Preserve full original reports. A factored quality matrix is a lossless
    # packet representation, avoiding 528 repeated copies of common keys.
    pre_factored=deepcopy(pre);quality=pre_factored.pop('qualityCases');pre_factored['qualityCasesFactored']=factor(quality)
    assert [merge(pre_factored['qualityCasesFactored']['COMMON'],z) for z in pre_factored['qualityCasesFactored']['orderedOverrides']]==quality
    projection={'status':'PASS exact reconstruction only','internalCards':44,'publicCards':28,
        'completeSourceObjectsReconstructed':44,'completeOperationalObjectsReconstructed':44,
        'wholePublicEnvelopeEqual':True,'publicManuscriptIndependentlyReconstructed':True,
        'publicGuidePrivateColdOmitted':True,'all28SixParagraphBindingsRetained':True,
        'recipesApproved':0,'artifactHashes':hashes}
    dump(AUDIT/'FISHING_PUBLIC_PARAGRAPH_PROJECTION.json',projection)
    report={'status':'PASS local exact-review readiness; not GPT approval','checkCount':220,
        'sourceProjectionArithmeticChecks':130,'sequenceChecks':90,'qualityCases':528,
        'structuralStates':156,'repairQuotes':76,'syntheticFixtureSets':6,'protectedInputs':63,
        'artifactHashes':hashes,'sourceVerdict':data['sourceAuthority'],
        'remainingRequiredEvidence':['separate GPT exact-card review'],
        'scopeLimits':['Governing world records are cited premises, not authenticated facts.',
            'Core resolution, anatomy/fit, legal access/extraction, preservation and inventory remain separately governed.',
            'Reference helper is not companion runtime, market/ecology certification, human balance or final whole-game flow.'],
        'sourceReports':['FISHING_PRELIMINARY_VALIDATION.json','FISHING_SEQUENCE_VALIDATION.json','FISHING_PUBLIC_PARAGRAPH_PROJECTION.json'],
        'walkthroughs':'FISHING_WORKED_SCENARIOS.md','recipesApproved':0,'currentReviewedRecipes':348,
        'remainingRecipes':339,'publicReviewed':223,'runtimeImplemented':False,'sourceInformationDeleted':False,'cosmology':'post-push only'}
    dump(AUDIT/'FISHING_CANDIDATE_VALIDATION.json',report)
    cover='''Codex to Calibration Review Part 2: exact Fishing operational PLAYTEST candidate in THREE parts. This is PART A. Please acknowledge receipt only and wait for B and C before a verdict.

Your completed FI-D01–FI-D24 source/interface verdict (turn d8e96231-9912-42c7-a691-7c4ba4b68821, reply 78d78fa4-1292-4566-9f43-7149476da18e) is preserved in full: 75,298 characters, SHA256 f6b2325a6c23bd1652e0d9752bc2708754a34be2b95a5768f40b3152d5a22ad0. The downloaded export's first19,692 characters matched the actual connector reply exactly. Its authoring permission has been applied to44 draft cards,28 public/3 restricted/13 Director-only, nine bodies and14 internal/13 public affinities. No Fishing card has been promoted. Current totals348/687 reviewed,339 remaining; public223/433.

The full original44 source records,212 consumed component occurrences,zero catalysts,all28 six-paragraph V5 bindings,three historical boat concepts and literal Sporefolk Adult linkage remain preserved. All63 protected sources and older reviewed-rule inputs are unchanged. The source-developed flags remain historical fields, not card approval.

Part A supplies the full source verdict, both shared guides, every source object and card metadata, the complete internal/public envelopes and all nine body models. Part B supplies both exact card manuscripts, every operational object, reconstruction evidence, all24 written scenarios and the historical transport backlog. Part C supplies all local validation evidence and complete bounded reference/fixture-generator/validation code. Review all three together, including prose and scope limits; self-authored passing tests alone are not the verdict.

Lossless factoring: recursively merge COMMON with each orderedOverrides entry; dictionaries merge, arrays/scalars replace, and explicit null remains distinct from absent fields. Ordered index i matches metadata[i]. In Part B each operational text is the same card's exact **Operational effect:** paragraph. All44 complete cards reconstruct exactly. Public records recursively omit private cards and nested guidance and omit the private unused Cold row; the full public envelope is supplied separately.

Local checks:130 source/projection/arithmetic checks and90 sequence checks,528 source-bound quality choices,156 fixed-body structural states,76 repair quotes. These are actual locally run checks, not actions attributed to you. The helper requires cited historical governing records; it cannot authenticate their authority or establish actual stock, fit, response, legal extraction, placement or market availability. It is not companion runtime. Full vehicle/Forage/Supply/bestiary/economy integration and human balance retain their own gates.

After all THREE parts, return exact operational approval or a finite correction list. If conditional, explicitly state whether completing the listed repairs and checks authorizes promotion without another generic conference. Do not reopen unchanged earlier trade cards unless you identify a concrete new conflict. This is no publication, human-balance, runtime, whole-game flow or cosmology approval. No source deletion or GitHub push occurred. Cosmology remains after the authorized successful GitHub push and verified remote commit.
'''
    A='\n\n'.join([cover,'FULL COMPLETED SOURCE VERDICT',(AUDIT/'GPT_FISHING_SOURCE_CONFERENCE.md').read_text(encoding='utf-8'),
        'EXACT INTERNAL SHARED GUIDE',(ROOT/'docs/director-only/FISHING_INTERNAL_GUIDE.md').read_text(encoding='utf-8'),
        'EXACT PUBLIC SHARED GUIDE',(ROOT/'docs/mechanics/FISHING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8'),
        'ALL44 COMPLETE SOURCE OBJECTS',compact(sources),'COMPLETE CARD METADATA AND28 FULL V5 BINDINGS',compact(metadata),
        'INTERNAL ENVELOPE',compact(envelope),'PUBLIC ENVELOPE',compact(public_envelope),'ALL NINE BODY MODELS',compact(data['baseModels']),
        'END PART A. Acknowledge receipt; wait for B and C.'])
    B='\n\n'.join(['''Codex: PART B of THREE for exact Fishing review. Please acknowledge this part and wait for Part C before a verdict.

Expand [[PARAGRAPH Pn]] using the supplied dictionary to reconstruct the entire internal manuscript. Reconstruct every operational object by recursive COMMON/orderedOverride merge and restore its text from that card's exact **Operational effect:** paragraph. Combine with Part A source/metadata. Public [[INTERNAL PARAGRAPH In]] references use the map to zero-based paragraphs of the reconstructed internal manuscript split on double newline. Every other character is literal. The independent public reconstruction retains the28 public internal sections and removes their explicit private optional-guidance paragraphs. Both full JSON envelopes and all nine models were in A.

Audit actual catch timing/DC/credential; Bait storage/exposure/receipt; physical Rod/Net/Trap/Rig methods; finite opportunities and real stock; independently eligible maximums and one affinity; historical due events; custody and first recovery including zero; anatomy/harvesting boundaries; original bodies, work and repairs; no catalysts or artisan reduction; values, food/Supply and complete audience filtering. All24 written cases below use synthetic world facts, not new game creatures or promised availability. Source decisions alone have approved zero Fishing cards.''',
        'SHARED EXACT INTERNAL PARAGRAPHS',compact(shared),'COMPLETE EXACT INTERNAL MANUSCRIPT',template,
        'COMPLETE OPERATIONAL OBJECTS',compact(operations),'PUBLIC PARAGRAPH INDEX MAP',compact(mapping),
        'COMPLETE EXACT PUBLIC MANUSCRIPT',public_template,'INDEPENDENT PROJECTION REPORT',compact(projection),
        'ALL24 SOURCE-BOUND WORKED CASES AND SCOPE LIMITS',walkthrough,
        'THREE HISTORICAL TRANSPORT CONCEPTS',compact(read(AUDIT/'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json')),
        'END PART B. Acknowledge receipt only; Part C follows.'])
    C='\n\n'.join(['''Codex: PART C completes the THREE-part exact Fishing candidate. Please now review the full candidate and issue exact operational approval or finite corrections.

The two preliminary local report files are preserved history: they describe readiness before the final written-case and reconstruction pass. FISHING_CANDIDATE_VALIDATION.json below is the later local readiness report; none is GPT approval. The qualityCasesFactored field losslessly represents the original528 quality-case objects using the same recursive COMMON/orderedOverrides merge. All other report fields are literal.

The complete reference helper and both validation programs follow. The sequence validator is also the deterministic fixture generator: it gives every synthetic record, source recipe binding, mutation, timeline and assertion. Its saved six fixture sets are locally preserved separately; do not assume real campaign facts or a runtime implementation from them. Please examine the cited-record boundary and prose as well as numerical tests. A party's unsupported fit/availability assertion is not a governing-world record; authentication and actual Director adjudication remain outside this bounded arithmetic/journal helper.

The code derives item effects from actual source cards, binds canonical roll descriptors, reserves physical stock/gear atomically, types due events, enforces minute55 and retrieval work, snapshots Trap personal contributions, preserves one evaluation including zero, and conserves captured units through the ordinary-harvest boundary. Core dice results, real shape/behavior/legal extraction and inventory are separately governed inputs, never certified by these local fixtures. Please identify any mechanical conflict or missing finite card rule explicitly.

All44 cards remain draft. Current reviewed totals348/687,public223/433. State whether listed finite repairs, if any, permit promotion once actually completed and revalidated. Cosmology remains strictly after successful authorized push and remote verification.''',
        'FINAL LOCAL READINESS REPORT',compact(report),'FULL PRELIMINARY SOURCE/PROJECTION/ARITHMETIC REPORT WITH LOSSLESS QUALITY FACTORING',compact(pre_factored),
        'FULL SEQUENCE CHECK REPORT',compact(seq),'BOUNDED FISHING REFERENCE CODE',(ROOT/'tools/fishing_reference.py').read_text(encoding='utf-8'),
        'SOURCE/PROJECTION/ARITHMETIC VALIDATION CODE',(ROOT/'tools/validate_fishing_recipe_candidate.py').read_text(encoding='utf-8'),
        'COMPLETE SOURCE-BOUND FIXTURE GENERATOR AND SEQUENCE VALIDATION CODE',(ROOT/'tools/validate_fishing_sequences.py').read_text(encoding='utf-8'),
        'END ALL THREE PARTS. Full exact review requested; no promotion inferred.'])
    state={'status':'prepared-not-sent','threadId':data['sourceAuthority']['threadId'],'parts':{},
        'partCount':3,'losslessSourceReconstructions':44,'losslessOperationalReconstructions':44,
        'losslessInternalCardReconstructions':44,'losslessPublicCardReconstructions':28,
        'losslessInternalManuscript':True,'losslessPublicManuscript':True,'independentPublicManuscriptProjection':True,
        'wholePublicEnvelopeEqual':True,'artifactHashes':hashes,'protectedFiles':baseline,
        'supportHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in [
            ROOT/'tools/fishing_reference.py',ROOT/'tools/validate_fishing_recipe_candidate.py',ROOT/'tools/validate_fishing_sequences.py',
            AUDIT/'FISHING_WORKED_SCENARIOS.md',AUDIT/'FISHING_CANDIDATE_VALIDATION.json',AUDIT/'FISHING_PUBLIC_PARAGRAPH_PROJECTION.json',
            AUDIT/'FISHING_PRELIMINARY_VALIDATION.json',AUDIT/'FISHING_SEQUENCE_VALIDATION.json',AUDIT/'FISHING_SEQUENCE_FIXTURES.json']},
        'recipesApproved':0,'reviewedTotal':348,'remaining':339,'publicReviewed':223,
        'sourceInformationDeleted':False,'cosmology':'post-push only'}
    for label,text in [('A_RULES_SOURCE',A),('B_EXACT_CARDS',B),('C_REFERENCE_EVIDENCE',C)]:
        path=AUDIT/f'CODEX_FISHING_EXACT_PART2_{label}.txt';assert not path.exists();write(path,text)
        state['parts'][label]={'file':path.name,'characters':len(text),'sha256':sha(path),'sent':False}
    dump(target,state)
    print(compact({'parts':state['parts'],'reconstructedCards':44,'publicCards':28,'localChecks':220,'recipesApproved':0}))


if __name__=='__main__':main()
