from __future__ import annotations
import hashlib,json,pathlib,zipfile,shutil
from datetime import datetime,timezone
ROOT=pathlib.Path(r'C:\Github\DecenniumDescent')
AUD=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUTDIR=AUD/'vitalitymatter10_context_138'
ZIPOUT=AUD/'DD_SoulContact6_Applied_VitalityMatter10_Context_138.zip'
REQOUT=AUD/'VITALITYMATTER10_NEXT_REQUEST_138.txt'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json'
SOURCE_CAND=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/vitality_matter_10_source_conference_01.json'
SOURCE_REVIEW=AUD/'VITALITYMATTER10_CURRENT_SOURCE_PREREVIEW_129.json'
SOURCE_ZIP=ROOT/'docs/audit/2026-10-08/full-game/DD_VitalityMatter10_Director_Conference_128.zip'
OLD_REQ=AUD/'VITALITYMATTER10_NEXT_REQUEST_129.txt'
IDS=['summon-bone-colossus','black-reaping','chain-of-the-grave','finger-of-death','plague-wind','metal-to-glass','titanic-grip','flash-freeze','transmute-being','regenerate']
H=lambda b:hashlib.sha256(b).hexdigest()
def filebind(p):return {'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':H(p.read_bytes())}
def dump(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not OUTDIR.exists() and not ZIPOUT.exists() and not REQOUT.exists()
idxraw=INDEX.read_bytes(); idx=json.loads(idxraw); catraw=CAT.read_bytes(); cat=json.loads(catraw); srcqraw=QUEUE.read_bytes(); srcq=json.loads(srcqraw)
assert idx['authoredCounts']=={'reviewed':668,'pending':180}
pending=[e['id'] for e in idx['entries'] if e['authoredStatus']=='pending-authored-procedure']; assert len(pending)==180
assert all(x in pending for x in IDS)
for identity in IDS:
 e=next(e for e in idx['entries'] if e['id']==identity); cidx=int(e['wholeCardPointer'].rsplit('/',1)[1]); assert cat['spells'][cidx]['id']==identity
pre=json.loads(SOURCE_REVIEW.read_text(encoding='utf-8')); assert len(pre['selectedNativeCards'])==10 and len(pre['questionsRead'])==32 and len(pre['requiredMainCases'])==21
assert {x['id'] for x in pre['selectedNativeCards']}==set(IDS)
assert SOURCE_CAND.is_file() and SOURCE_ZIP.is_file() and OLD_REQ.is_file()
assert SOURCE_ZIP.stat().st_size==59442222 and H(SOURCE_ZIP.read_bytes())=='1a1f35cfc4308c7e8c3481cd9e94cbefd1a098eb0157b4afa7eb6e0f44545f96'
assert filebind(SOURCE_CAND)['bytes']==868854 and filebind(SOURCE_CAND)['sha256']=='46035df8a9a465e8df1d9abcc701c5ba242058c64f2250600a5c2e835b929196'
oldgroups=srcq['groups']; pendingset=set(pending); group_rows=[]; covered=[]
for g in oldgroups:
    members=[x for x in g.get('identities',[]) if x in pendingset]
    if members:
        covered.extend(members); group_rows.append({'group':g['group'],'pendingIds':members,'pendingCount':len(members),'historicalPhase':g.get('phase'),'candidate':g.get('candidate'),'archive':g.get('archive')})
assert len(covered)==180 and len(set(covered))==180, (len(covered),len(set(covered)))
nextgroup=next(g for g in oldgroups if g['group']=='vitality-matter10'); assert nextgroup['identities']==IDS
next_group={**nextgroup,'status':'NEXT_CURRENT_DIRECTOR_REVIEW','questions':32,'requiredMainCases':21,'priorCompleteOperationalProcedures':0,
            'sourceArchive':{'path':'docs/audit/2026-10-08/full-game/DD_VitalityMatter10_Director_Conference_128.zip','bytes':SOURCE_ZIP.stat().st_size,'sha256':H(SOURCE_ZIP.read_bytes())},
            'currentSourcePrereview':filebind(SOURCE_REVIEW)}
# Fresh authority overlays replace stale counts/status in the historical 137 queue files.
indexbind={'path':'authority/authored_review_index.json','bytes':len(idxraw),'sha256':H(idxraw)}
catbind={'path':'authority/catalog.json','bytes':len(catraw),'sha256':H(catraw)}
pending_audit={'id':'CURRENT180-PENDING-IDENTITY-AUDIT-138','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET',
 'indexBinding':indexbind,'catalogBinding':catbind,'authoredCounts':idx['authoredCounts'],'pendingCount':len(pending),'pendingIds':pending,
 'allPendingExistInSourceCatalog':True,'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0}
queue_overlay={'id':'SPELL-REVIEW-QUEUE-138','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'historicalSourceQueueBinding':filebind(QUEUE),'historicalQueueCountsSuperseded':True,'currentAuthority':{'reviewedApplied':668,'pending':180,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':392,'scopedInterfaces':173},
 'currentPendingGroups':group_rows,'nextSuggestedGroups':['vitality-matter10'],'nextGroup':next_group,
 'justAppliedBatch':{'group':'soul-contact6','acceptedIds':['alignment-scrying','commune','planar-binding-minor','planar-summons-lesser','planar-summons-greater','soul-cage'],
  'reviewId':'SOULCONTACT6-EXACT-AUTHORED-ACCEPTANCE-138','acceptance':filebind(AUD/'soulcontact6_return02_138/SOULCONTACT6_EXACT_ACCEPTANCE_138.json'),
  'application':filebind(AUD/'soulcontact6_return02_138/SOULCONTACT6_APPLICATION_138.json'),
  'validation':filebind(AUD/'soulcontact6_return02_138/SOULCONTACT6_APPLICATION_VALIDATION_138.json'),
  'independentAudit':filebind(AUD/'soulcontact6_return02_138/SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json')},
 'pendingIdentityAudit':'authority/CURRENT180_PENDING_IDENTITY_AUDIT_138.json','retainedBoundary':'Do not redo feats, completed16/72, the 335 closed feat identities, or applied spell cohorts. SourceStatus/content/cosmology/runtime holds remain separately tracked.',
 'next':'Complete VitalityMatter10 only, independently audit the exact return, apply its accepted identities, then proceed in current source queue order until the live pending count is zero.'}
handoff={'id':'CURRENT-HANDOFF-138','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOULCONTACT6_APPLIED_VITALITYMATTER10_NEXT_180_PENDING',
 'currentAuthority':queue_overlay['currentAuthority'],'currentIndexBinding':indexbind,'currentCatalogBinding':catbind,'pendingIdentityAudit':pending_audit,
 'appliedThisStep':queue_overlay['justAppliedBatch'],'nextGroup':next_group,'retainedBoundary':queue_overlay['retainedBoundary'],
 'director':{'title':'Calibration review part 6','conversationId':'6adc506d-8770-83ea-b64c-0345d9b9b682','role':'source/procedure authoring director; return remains proposed until independently audited'},
 'resumePriority':queue_overlay['next'],'nextPreparedRequest':'VITALITYMATTER10_NEXT_REQUEST_138.txt'}
# Reuse the detailed prior 10-spell request, with the live applied count and exact applied result placed first.
old=OLD_REQ.read_text(encoding='utf-8')
req=('Current exact applied authority is 668 reviewed/applied / 180 pending / 0 accepted-unapplied. '
     'SoulContact6 is accepted and applied with its retained CR/type roster, positive planar operation, campaign site/respondent, continuing-soul ontology, cosmology, and runtime holds. '
     'The attached DD_SoulContact6_Applied_VitalityMatter10_Context_138.zip binds the exact live index, catalog, current pending set and application receipts. '
     'The exact original DD_VitalityMatter10_Director_Conference_128.zip is attached separately at 59,442,222 bytes and SHA-256 1a1f35cfc4308c7e8c3481cd9e94cbefd1a098eb0157b4afa7eb6e0f44545f96. '
     'Proceed with VitalityMatter10 as the next 10-identity group.\n\n'+old)
REQOUT.write_text(req,encoding='utf-8',newline='\n')
context_pre={'id':'VITALITYMATTER10-CURRENT-SOURCE-CONTEXT-138','status':'SOURCE_PREREVIEW_REBOUND_TO_CURRENT_668_180_AUTHORITY',
 'currentAuthority':queue_overlay['currentAuthority'],'currentIndexBinding':indexbind,'sourcePrereviewOriginal':filebind(SOURCE_REVIEW),
 'sourceCandidateCurrent':filebind(SOURCE_CAND),'identitySet':IDS,'questions':32,'requiredMainCases':21,'priorCompleteOperationalProcedures':0,
 'sourceArchive':next_group['sourceArchive'],'historicalPrereviewCounts':pre['countsUnchanged'],'historicalCountsDoNotSupersedeCurrentIndex':True,
 'allTenRemainPendingAndCatalogBound':True,'canonicalChanged':False,'runtimeTestsExecuted':False}

OUTDIR.mkdir(parents=True)

def cp(src,rel):
 dst=OUTDIR/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
cp(INDEX,'authority/authored_review_index.json');cp(CAT,'authority/catalog.json');cp(QUEUE,'authority/remaining_work_queue_67.json')
dump(OUTDIR/'authority/CURRENT_PENDING_IDENTITY_AUDIT_138.json',pending_audit)
dump(OUTDIR/'authority/CURRENT_SPELL_QUEUE_138.json',queue_overlay)
dump(OUTDIR/'authority/CURRENT_HANDOFF_138.json',handoff)
cp(AUD/'CURRENT_SPELL_QUEUE_137.json','authority/CURRENT_SPELL_QUEUE_137_HISTORICAL.json')
cp(AUD/'CURRENT_HANDOFF_137.json','authority/CURRENT_HANDOFF_137_HISTORICAL.json')
cp(SOURCE_REVIEW,'next/vitalitymatter10/VITALITYMATTER10_CURRENT_SOURCE_PREREVIEW_129.json')
cp(SOURCE_CAND,'next/vitalitymatter10/vitality_matter_10_source_conference_01.json')
dump(OUTDIR/'next/vitalitymatter10/CURRENT_SOURCE_CONTEXT_138.json',context_pre)
(OUTDIR/'next/vitalitymatter10/VITALITYMATTER10_NEXT_REQUEST_138.txt').write_text(req,encoding='utf-8',newline='\n')
# Include exact most recent accepted SoulContact6 evidence and the complete accepted candidate envelope.
sc=AUD/'soulcontact6_return02_138'; cand=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138'
for src,rel in [(sc/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json','applied/soulcontact6/EXACT_ACCEPTANCE.json'),(sc/'SOULCONTACT6_APPLICATION_138.json','applied/soulcontact6/APPLICATION.json'),(sc/'SOULCONTACT6_APPLICATION_VALIDATION_138.json','applied/soulcontact6/APPLICATION_VALIDATION.json'),(sc/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json','applied/soulcontact6/INDEPENDENT_AUDIT.json'),(sc/'DD_SoulContact6_Director_Return02_138.zip','applied/soulcontact6/DIRECTOR_RETURN_138.zip')]: cp(src,rel)
for src in cand.iterdir():
 if src.is_file(): cp(src,'applied/soulcontact6/candidate/'+src.name)
external={'id':'VITALITYMATTER10-EXTERNAL-SOURCE-ARCHIVE-BINDING-138','artifact':filebind(SOURCE_ZIP),'filename':SOURCE_ZIP.name,'attachedSeparatelyToDirector':True,
 'archiveManifestAndSourceBindings':'The original source archive is supplied unchanged as a separate attachment. Its historical source counts are superseded only by the exact current index in the context packet.'}
dump(OUTDIR/'next/vitalitymatter10/EXTERNAL_SOURCE_ARCHIVE_BINDING.json',external)
# Exhaustive manifest over context files, excluding manifest and delivery.
files=[]
for p in sorted(OUTDIR.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();files.append({'path':p.relative_to(OUTDIR).as_posix(),'bytes':len(b),'sha256':H(b)})
manifest={'id':'DD-SOULCONTACT6-APPLIED-VITALITYMATTER10-CONTEXT-138','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'files':files,'selfExcluded':'CONTEXT_MANIFEST.json'}
dump(OUTDIR/'CONTEXT_MANIFEST.json',manifest)
with zipfile.ZipFile(ZIPOUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(OUTDIR.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(OUTDIR).as_posix())
with zipfile.ZipFile(ZIPOUT) as z:
 assert z.testzip() is None
 for rec in files:
  b=z.read(rec['path']);assert len(b)==rec['bytes'] and H(b)==rec['sha256'],rec['path']
zbytes=ZIPOUT.read_bytes()
delivery={'id':'DD-SOULCONTACT6-APPLIED-VITALITYMATTER10-CONTEXT-138-DELIVERY','file':ZIPOUT.name,'bytes':len(zbytes),'sha256':H(zbytes),'members':len(files)+1,'manifestBindings':len(files),
 'currentAuthority':queue_overlay['currentAuthority'],'nextGroup':{'group':'vitality-matter10','identities':IDS,'identityCount':10,'questions':32,'requiredMainCases':21},
 'separateOriginalSourceArchive':external['artifact'],'allContextMemberBindingsVerified':True,'zipCRCVerified':True,'runtimeOrSourceProgramsExecuted':False}
dump(AUD/'DD_SoulContact6_Applied_VitalityMatter10_Context_138_DELIVERY.json',delivery)
print(json.dumps({'status':'PASS','contextZip':delivery,'requestBytes':REQOUT.stat().st_size,'pendingGroups':len(group_rows),'pendingIdentities':len(pending),'vitalityIdentities':IDS,'archivePath':str(SOURCE_ZIP),'archiveHash':H(SOURCE_ZIP.read_bytes())},indent=2))
