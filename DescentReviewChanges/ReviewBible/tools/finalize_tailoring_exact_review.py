"""Promote only the scoped exact-card approval after TA-ER01..04 pass."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,subprocess,sys,zipfile

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
ARCHIVE=AUDIT/'tailoring-before-part2-repairs'
TURN='b6984844-5544-4ff0-9624-50bab432dbb2';REPLY='54b2b40e-cce6-48c4-8aa6-51ea7c535f0c';THREAD='6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'
STATUS='REVIEWED — authored operational PLAYTEST Tailoring recipe set'
CARD_STATUS='reviewed-authored-operational-playtest'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def main():
    manifest=ROOT/'docs/mechanics/TAILORING_REVIEW_STATUS.json';assert not manifest.exists()
    report=read(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json')
    assert report['status']=='PASS' and report['checkCount']==157 and report['recipesApproved']==0
    verdict=AUDIT/'GPT_TAILORING_EXACT_VERDICT.md';v=verdict.read_text(encoding='utf-8')
    assert TURN in v and REPLY in v and 'promotion of all 43 cards is authorized' in v
    assert 'TA-ER01–TA-ER04 are the complete required correction list' in v
    for rel,h in read(ARCHIVE/'PRESERVATION_MANIFEST.json')['files'].items():assert sha(ARCHIVE/rel)==h
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    zpath=AUDIT/'tailoring_exact_review_evidence.zip'
    with zipfile.ZipFile(zpath) as z:
        hashes=json.loads(z.read('tailoring_exact_review_evidence/EVIDENCE_SHA256.json'))['files']
        assert all(hashlib.sha256(z.read('tailoring_exact_review_evidence/'+n)).hexdigest()==h for n,h in hashes.items())
    # The repairs alter helpers, fixtures and shared/card repair prose only.
    # All candidate JSON values must still exactly match the submitted revision.
    for rel in report['artifactHashes']:
        if rel.endswith('.json'):assert read(ROOT/rel)==read(ARCHIVE/(ROOT/rel).relative_to(GAME))
    # Check every manuscript difference is one of the two authorized prose changes.
    old_card="**Repair:** trained DEX + Weaver's-tools proficiency at the actual Loom and Cutting Table with Needles and Shears."
    new_card="**Repair:** trained DEX + Weaver's-tools proficiency and actual Weaver's tools, using the Tailor's-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears. The same actual implement may meet compatible overlapping requirements without duplicate purchases. Missing the actual toolkit prevents starting either route; a quotation alone grants no permission."
    old_guide="Repair requires trained DEX + Weaver's-tools proficiency, actual Loom and Cutting Table, Needles and Shears."
    new_guide="Repair requires trained DEX + Weaver's-tools proficiency and actual Weaver's tools, using the Tailor's-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears. The same actual implement may satisfy compatible overlapping requirements, without duplicate purchases. A trained character without the actual toolkit cannot begin either repair route; a numerical quotation is not permission to begin."
    qualification="Each physical candidate must independently satisfy its own actual task relationship, contribution, visibility, coverage and other applicable premises before the strongest-value comparison. A contributing item cannot qualify an unrelated stronger item. Apply this item-specific qualification to Bag operation and cross-trade candidates as well. Check all equipment designations before filtering task candidates; a noncontributing item still occupies its designated position. Losing task eligibility alone does not remove an independently active resistance.\n\n"
    for rel in report['artifactHashes']:
        if not rel.endswith('.md'):continue
        old=(ARCHIVE/(ROOT/rel).relative_to(GAME)).read_text(encoding='utf-8')
        expected=old.replace(old_card,new_card).replace(old_guide,new_guide)
        if 'RECIPE_CARDS' not in rel:expected=expected.replace('The card lists its exhaustive domains.',qualification+'The card lists its exhaustive domains.')
        assert (ROOT/rel).read_text(encoding='utf-8')==expected,'Out-of-scope manuscript repair: '+rel
    dump(AUDIT/'TAILORING_REPAIRED_PREPROMOTION_VALIDATION.json',report)
    changes={}
    for rel in [p for p in report['artifactHashes'] if p.endswith('.json')]:
        p=ROOT/rel;before=read(p);d=deepcopy(before)
        d.update(status=STATUS,exactRecipeApproval=True,exactReviewThreadId=THREAD,exactReviewTurnId=TURN,exactReplyId=REPLY)
        d['sharedOperationalProfile']['status']=CARD_STATUS
        for c in d['cards']:assert c['status']=='authored-draft-awaiting-exact-review';c['status']=CARD_STATUS
        restored=deepcopy(d);restored['status']=before['status'];restored['exactRecipeApproval']=False;restored['sharedOperationalProfile'].pop('status')
        for k in ['exactReviewThreadId','exactReviewTurnId','exactReplyId']:restored.pop(k)
        for c,b in zip(restored['cards'],before['cards']):c['status']=b['status']
        assert restored==before,'Non-status JSON mutation'
        dump(p,d);changes[rel]='Only operational status, approval flag and exact-review provenance; complete sources and all operational values preserved.'
    for rel in [p for p in report['artifactHashes'] if p.endswith('.md')]:
        p=ROOT/rel;s=p.read_text(encoding='utf-8');before=s
        for old in ['**DRAFT — exact review pending.**','**DRAFT; exact review pending.**','**Authored draft; exact review pending.**']:
            s=s.replace(old,'**REVIEWED — authored operational PLAYTEST.**')
        if 'RECIPE_CARDS' not in rel:
            s=s.replace('These operational additions implement the TA-D01–TA-D16 source conference in Calibration Review Part 2.',
                'These operational additions implement the historical TA-D01–TA-D16 source conference in Calibration Review Part 2. The subsequent exact review (turn `'+TURN+'`, reply `'+REPLY+'`) conditionally approved the authored cards; TA-ER01–TA-ER04 are now corrected and validated. The source conference remains authoring direction. Reviewed operational recipe totals are 305/687; 382 remain.')
        assert s!=before and s.count('\n\n')==before.count('\n\n')
        write(p,s);changes[rel]='Review labels and exact-review provenance only after the separately verified TA-ER01/04 prose repairs.'
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validate_tailoring_recipe_candidate.py')],check=True)
    final=read(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json');assert final['status']=='PASS' and final['recipesApproved']==43
    ip=(ROOT/'docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8').split('\n\n')
    pp=(ROOT/'docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8').split('\n\n')
    refs=[{'internalParagraph':ip.index(p)} if p in ip else {'literal':p} for p in pp]
    assert [ip[r['internalParagraph']] if 'internalParagraph' in r else r['literal'] for r in refs]==pp
    projection={'status':'PASS','scope':'Internal audit only; contains restricted and Director-only paragraphs.','internalParagraphs':ip,'publicParagraphProjection':refs,'internalParagraphCount':len(ip),'publicParagraphCount':len(pp),'publicReferences':sum('internalParagraph' in r for r in refs),'internalSha256':sha(ROOT/'docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md'),'publicSha256':sha(ROOT/'docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md'),'completePublicJsonEnvelopeAndDataEquality':True}
    projection_path=AUDIT/'TAILORING_FINAL_PARAGRAPH_PROJECTION.json';dump(projection_path,projection)
    repairs={'status':'PASS — exact-review conditions fulfilled','threadId':THREAD,'turnId':TURN,'replyId':REPLY,'preservedSubmittedRevision':ARCHIVE.relative_to(GAME).as_posix(),
      'repairs':{'TA-ER01':'Each physical item has its own task premises; missing premises fail closed. Slots are validated before filtering. Hidden/noncontributing/inadequately covering stronger outfits and Bags cannot borrow qualification; genuine qualifiers use the strongest once. Independent radiant resistance remains. Leatherworking qualification and task IDs are item-specific too.',
      'TA-ER02':'Cross-trade containers use actual operator, garments use wearer; no ownership/wearer fallback. Source652 tests B operating A-worn container, self-operation, nonoperator wearer and inactive/access cases.',
      'TA-ER03':'All named equipment fixtures derive from actual saved cards/models. Recipe577 acid Garment;546 Bag+1;306 Leatherworking Gloves+2;actual Hat/Helm/Gauntlets metadata. Nested546 Bag fits280 Backpack, giving7 physical lb/3.6 canonicalLoad and5 countedlb/3.4 effectiveLoad; suppression retains7/3.6. Correct548/584 reconstruction DC11/28 asserted.',
      'TA-ER04':'Both guides and all43/29 card Repair paragraphs explicitly require actual Weaver tools with Tailor binding, Loom and Cutting Table, Needles and Shears. Compatible overlapping implements allowed; rare creation rows remain outside generic repair. Missing toolkit bars starting; quotation helper grants no permission.'},
      'correctedChecks':[c for c in final['checks'] if c['name'].startswith('TA-ER')],
      'statusOnlyArtifactChanges':changes,'checks':final['checkCount'],'durabilityStates':final['durabilityStates'],'protectedFilesUnchanged':53,
      'paragraphProjectionSha256':sha(projection_path),'referenceSha256':sha(ROOT/'tools/tailoring_reference.py'),'validatorSha256':sha(ROOT/'tools/validate_tailoring_recipe_candidate.py'),'verdictSha256':sha(verdict),'reviewerArchiveSha256':sha(zpath),'reviewerArchiveInternalHashesVerified':len(hashes),'sourceInformationDeleted':0}
    receipt=AUDIT/'TAILORING_EXACT_REPAIRS_APPLIED.json';dump(receipt,repairs)
    m={'status':STATUS,'exactReviewThreadId':THREAD,'exactReviewTurnId':TURN,'exactReplyId':REPLY,'sourceConferenceTurnId':'6b7474ed-1bca-40b8-81af-7bfbd843a5cc','sourceConferenceReplyId':'95ba16b4-b85f-47d8-bc61-047f9ebfcdeb','repairsApplied':['TA-ER01','TA-ER02','TA-ER03','TA-ER04'],
      'coverage':{'recipes':43,'public':29,'restricted':4,'directorOnly':10,'baseModels':15,'publicBaseModels':11},'validationChecks':final['checkCount'],'localDurabilityStates':final['durabilityStates'],'protectedSourceAndPriorRuleArtifactsUnchanged':53,
      'artifactHashes':{(ROOT/p).relative_to(GAME).as_posix():h for p,h in final['artifactHashes'].items()},'replyHashes':{verdict.name:sha(verdict)},'validationEvidence':(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json').relative_to(GAME).as_posix(),'validationSha256':sha(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json'),'repairEvidence':receipt.relative_to(GAME).as_posix(),'repairEvidenceSha256':sha(receipt),
      'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'aggregateReviewedRecipes':305,'remainingRecipeEffects':382,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'}
    dump(manifest,m)
    sub=read(AUDIT/'TAILORING_EXACT_PART2_SUBMISSION.json');sub['status']='Completed exact verdict; four finite repairs validated;43 operational cards promoted'
    sub['parts']['B_EXACT_CARDS'].update(status='Completed conditional verdict; fulfilled conditions recorded separately',replyId=REPLY)
    sub['finalReviewManifest']=manifest.relative_to(GAME).as_posix();sub['submittedCountsAreHistorical']=True;dump(AUDIT/'TAILORING_EXACT_PART2_SUBMISSION.json',sub)
    author=read(AUDIT/'TAILORING_AUTHORING_STATUS.json');author.update(status=STATUS,recipesApproved=43,currentReviewedRecipes=305,remainingRecipes=382,exactReviewTurnId=TURN,exactReplyId=REPLY,reviewManifest=manifest.relative_to(GAME).as_posix());dump(AUDIT/'TAILORING_AUTHORING_STATUS.json',author)
    print(json.dumps({'status':m['status'],'checks':final['checkCount'],'paragraphReferences':projection['publicReferences'],'reviewedTotal':305,'remaining':382}))
if __name__=='__main__':main()
