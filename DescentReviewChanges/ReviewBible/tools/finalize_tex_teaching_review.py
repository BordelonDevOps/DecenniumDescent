"""One-use reviewed teaching labels, precise coverage errata and preserved provenance."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, copy, re
from urllib.parse import unquote
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
D=A/'teaching-nine-exact-reviewer-files';BACK=A/'teaching-before-tex-fulfillment'
F=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\teaching-tex-reproduction\frozen')
def load(p):return json.loads(p.read_text('utf-8-sig'))
def h(p):return sha256(p.read_bytes()).hexdigest()
def record(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)}
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def encode_like(b,t):
    if b'\r\n' in b:t=t.replace('\n','\r\n')
    return (b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+t.encode('utf-8')
receipt_path=A/'TEACHING_TEX_EXACT_FULFILLMENT.json'
assert not receipt_path.exists(), 'One-use finalization already exists'
pre=load(A/'TEACHING_TEX_PRELABEL_FULFILLMENT.json');c=load(D/'TEX_EXACT_CORRECTIONS.json');admin=c['administrativeFulfillment']
for rel,r in pre['preLabelArtifacts'].items():assert h(G/rel)==r['sha256'],rel
labels={
 'docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md':[
  ('**Worksheet draft for the reviewed language rules.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**'),
  ("The worksheet's presentation still awaits joint review and human use.","The worksheet's authored presentation is jointly reviewed; human use remains untested.")],
 'docs/playtest/PLAYTEST_TERMS_GLOSSARY.md': [('**Editorial draft; joint presentation review pending.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/playtest/FIRST_CRAFT_WALKTHROUGH.md':[('**Authored teaching draft; presentation review pending.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/playtest/INJURY_AND_AID_WALKTHROUGH.md':[('**Authored teaching draft; presentation review pending.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/playtest/COMPANION_COMMAND_WALKTHROUGH.md':[('**Authored teaching draft; presentation review pending.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/playtest/CLASS_RESOURCE_REFERENCE.md':[('**Presentation draft awaiting joint review.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/playtest/CHARACTER_SHEET_PLAYTEST.md':[('**Blank presentation draft awaiting joint review.**','**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.**')],
 'docs/mechanics/CHARACTER_CREATION_NAVIGATION_CANDIDATE.md':[(
  '**NAVIGATION-ONLY REVIEW COPY — five progress-note updates await joint presentation review.** The reviewed foundation mechanics below are unchanged. The original chapter and exact old wording remain preserved; use its current reviewed source for governing rules.',
  '**REVIEWED NAVIGATION COPY — TEX-EXACT-2026-10-11.** The five progress-note updates are applied to the governing character chapter. Foundation mechanics are unchanged. The original chapter and exact old wording remain preserved; use the governing chapter for current rules.')]
}
label_proofs=[]
for rel,changes in labels.items():
    p=R/rel;b=p.read_bytes();text=p.read_text('utf-8-sig');old=text
    backup=A/'teaching-tex-before-labels'/p.relative_to(G);assert not backup.exists();backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
    for before,after in changes:assert text.count(before)==1;(text:=text.replace(before,after,1))
    p.write_bytes(encode_like(b,text));reverse=text
    for before,after in reversed(changes):assert reverse.count(after)==1;(reverse:=reverse.replace(after,before,1))
    assert encode_like(b,reverse)==b
    label_proofs.append({'path':p.relative_to(G).as_posix(),'beforeSha256':sha256(b).hexdigest(),'afterSha256':h(p),'operations':[{'before':x,'after':y} for x,y in changes],'reverseRestoresExactBytes':True})

# Preserve each exact old interface issue and every other field/status.
covp=G/admin['coverageJsonPath'];oldcov=load(covp);cov=copy.deepcopy(oldcov);resolutions=[]
for pointer in admin['coverageOldPointers']:
    _,_,ai,_,oi=pointer.split('/');ai=int(ai);oi=int(oi);aspect=cov['aspects'][ai]
    prior=aspect['openIssues'][oi];assert prior==admin['coverageOriginalIssue']
    resolution={'id':'TC-RECYCLING-01','priorText':prior,'resolution':admin['coverageResolution']}
    aspect.setdefault('resolvedInterfaceIssues',[]).append(resolution);del aspect['openIssues'][oi]
    resolutions.append({'pointer':pointer,'aspectId':aspect['id'],'resolution':resolution})
save(covp,cov)
inverse=copy.deepcopy(cov)
for r in resolutions:
    _,_,ai,_,oi=r['pointer'].split('/');ai=int(ai);oi=int(oi);a=inverse['aspects'][ai]
    assert a['resolvedInterfaceIssues'].pop()==r['resolution'];a['openIssues'].insert(oi,r['resolution']['priorText'])
    if 'resolvedInterfaceIssues' not in oldcov['aspects'][ai]:del a['resolvedInterfaceIssues']
assert inverse==oldcov
covmd=R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md';b=covmd.read_bytes();t=covmd.read_text('utf-8-sig')
assert t.count(admin['coverageOriginalIssue'])==5
t=t.replace(admin['coverageOriginalIssue'],admin['coverageResolution']);covmd.write_bytes(encode_like(b,t))
assert encode_like(b,t.replace(admin['coverageResolution'],admin['coverageOriginalIssue']))==b

# Check retained dispositions, links and preserved mechanical datasets after labels.
def anchors(t):return {''.join(c for c in re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',x).lower() if c.isalnum() or c in '_- ').replace(' ','-') for x in re.findall(r'^#{1,6}\s+(.+)$',t,re.M)}
links=[]
for rel in pre['preLabelArtifacts']:
    if not rel.endswith('.md'):continue
    p=G/rel
    for raw in re.findall(r'\]\(([^)]+)\)',p.read_text('utf-8-sig')):
        if re.match(r'\w+://|mailto:',raw):continue
        file,_,anchor=unquote(raw.strip('<>')).partition('#');dest=(p.parent/file).resolve() if file else p
        ok=dest.is_file() and (not anchor or anchor in anchors(dest.read_text('utf-8-sig')))
        assert ok,(rel,raw);links.append({'from':rel,'link':raw,'passed':True})
assert len(links)==162
mf=load(F/'FILE_MANIFEST.json');all_frozen=[]
for rel,v in mf.items():assert h(F/rel)==v['sha256'];all_frozen.append(rel)
allowed=set(pre['correctedCurrentFiles'])|set(pre['preLabelArtifacts'])|{pre['navigation']['original'],admin['coverageJsonPath'],'DescentReviewChanges/ReviewBible/docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md'}
live_unchanged=[]
for rel in load(A/'TEACHING_TEX_LOCAL_PREPARATION.json')['liveDiskPayloadsUnchanged']:
    if rel not in allowed:assert h(G/rel)==mf[rel]['sha256'];live_unchanged.append(rel)
for name in admin['historyPreserved']:assert h(A/name)==h(BACK/'docs/audit/2026-10-08/full-game'/name) if (BACK/'docs/audit/2026-10-08/full-game'/name).exists() else h(A/name)==mf['docs/audit/2026-10-08/full-game/'+name]['sha256']
pub=load(R/'data/crafting/advanced_craft_recipe_candidate_public.json');assert pub['operatingGuideText']==(R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text('utf-8-sig')
assert load(R/'data/public/spell_playtests/authored_review_index.json')['authoredCounts']=={'reviewed':412,'pending':436}
pdf=G/next(x for x in pre['preLabelArtifacts'] if x.endswith('.pdf'));assert h(pdf)==pre['preLabelArtifacts'][pdf.relative_to(G).as_posix()]['sha256']
label_proof={'scope':'Eight manuscript labels only; PDF unchanged, governed chapter status unchanged. Exact byte inverses preserve pre-label proofs.','labels':label_proofs,'pdf':record(pdf),'links':links,'directLinks':len(links),'allFrozenPayloadsPreserved':len(all_frozen),'otherLiveSubmittedPayloadsUnchanged':live_unchanged,'coverageResolutions':resolutions,'coverageInverseEqualsOriginal':True,'areaStatusesChanged':False}
save(A/'TEACHING_TEX_LABEL_ONLY_AND_SCOPE_PROOF.json',label_proof)

receipt={'reviewId':'TEX-EXACT-2026-10-11','status':'FULFILLED — reviewed authored teaching/presentation, nine artifacts','createdAt':datetime.now(timezone.utc).isoformat(),'authority':pre['authority'],'preLabelProof':record(A/'TEACHING_TEX_PRELABEL_FULFILLMENT.json'),'labelAndScopeProof':record(A/'TEACHING_TEX_LABEL_ONLY_AND_SCOPE_PROOF.json'),'operationsApplied':[x['id'] for x in c['operations']],'finalArtifacts':{rel:record(G/rel) for rel in pre['preLabelArtifacts']},'correctedCurrentCraftArtifacts':{rel:record(G/rel) for rel in pre['correctedCurrentFiles'] if '/docs/playtest/' not in rel},'navigation':pre['navigation'],'erratum':pre['erratum'],'resolvedCoverageIssueOccurrences':5,'coverage':record(covp),'questionDispositions':record(D/'TEX_TE_01_29_DISPOSITIONS.json'),'all29QuestionsMatchedOriginals':True,'finiteAuthoredCases':record(D/'TEX_FINITE_ACCEPTANCE_CASES.json'),'finiteCasesReviewedAndAccepted':16,'finiteCasesAreRuntimePasses':False,'localChecks':pre['validation'],'pdfRetainedUnchanged':True,'reviewedPdfEvidence':record(D/'evidence/pdf/PDF_REVIEW_AUDIT.json'),'localFocusedEvidence':record(A/'TEACHING_TEX_LOCAL_FOCUSED_REFERENCES.json'),'localExactAmendmentEvidence':record(A/'TEACHING_TEX_LOCAL_EXACT_AMENDMENTS.json'),'localSourceEvidence':record(A/'teaching-tex-local-source/TEACHING_READ_ONLY_AUDIT.json'),'originalBackup':pre['originalBackup'],'ordinaryAuthoredCounts':{'reviewed':412,'pending':436},'recipeCounts':{'internalReviewed':687,'publicReviewed':433},'newGameplayCardPromotions':0,'gameAreaStatusesChanged':False,'sourceInformationDeleted':0,'runtimeApproved':False,'humanTrialsPerformed':False,'balanceApproved':False,'wholeGameFlowComplete':False,'githubPushed':False,'cosmologyReviewed':False,'nextWork':'Remaining content catalogs, expedition/transport/social/reputation, bestiary and Director procedures; final joint whole-game flow before authorized push, verified remote before cosmology.'}
save(receipt_path,receipt)
# Append new-current provenance; all earlier authority/hashes remain exactly as read.
statusp=G/admin['advancedStatusPath'];oldstatus=load(statusp);status=copy.deepcopy(oldstatus)
entry={'id':'TC-RECYCLING-01','reviewId':'TEX-EXACT-2026-10-11','correction':'TEX-01','fulfillmentReceipt':record(receipt_path),'currentArtifactHashes':{p:r['sha256'] for p,r in receipt['correctedCurrentCraftArtifacts'].items()},'erratum':pre['erratum'],'scope':'Existing-rule interface reconciliation only; original AEX hashes remain historical; every recipe/body/sourceCard object and prior authority/count is unchanged.'}
status.setdefault('subsequentInterfaceErrata',[]).append(entry);save(statusp,status)
reverse=copy.deepcopy(status);assert reverse['subsequentInterfaceErrata'].pop()==entry
if 'subsequentInterfaceErrata' not in oldstatus:del reverse['subsequentInterfaceErrata']
assert reverse==oldstatus
save(R/'docs/playtest/TEACHING_REVIEW_STATUS.json',{'status':receipt['status'],'reviewId':receipt['reviewId'],'fulfillmentReceipt':record(receipt_path),'artifacts':receipt['finalArtifacts'],'pdfPrintedDraftHeaderRetained':True,'humanTeachingAccessibilityOrTwoLookupTested':False,'runtimeCertified':False,'balanceApproved':False})
save(A/'TEACHING_TEX_ADMIN_APPEND_PROOF.json',{'advancedStatus':record(statusp),'onlyAppendedEntry':entry,'removingEntryRestoresOriginalObject':True,'originalStatus':pre['originals'][admin['advancedStatusPath']],'currentTeachingStatus':record(R/'docs/playtest/TEACHING_REVIEW_STATUS.json'),'allEarlierAexAuthorityAndHashesPreserved':True})
print(json.dumps({'reviewedTeachingArtifacts':9,'operativeChanges':9,'navigationNotes':5,'resolvedIssueOccurrences':5,'reversibleLabelFiles':8,'links':162,'pdfChanged':False,'newGameplayCards':0,'areaStatusChanges':0,'receipt':str(receipt_path)}))
