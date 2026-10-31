from __future__ import annotations

import copy, gzip, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(r'C:\Github\DecenniumDescent-review-push-134')
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
GROUP='rank9-time-fate6'
IDS=['time-stop','fate-rewrite','collapse-timeline','eternal-prophecy']
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
QUEUE0=BASE/'CURRENT_SPELL_QUEUE_238.json'; HANDOFF0=BASE/'CURRENT_HANDOFF_238.json'; PENDING0=BASE/'CURRENT37_PENDING_IDENTITY_AUDIT_238.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
OLD_PACKET=BASE/'rank9_timefate6_current_source_221_prepared/DD_Rank9_TimeFate6_CurrentSource_221.zip'
OLD_DELIVERY=BASE/'rank9_timefate6_current_source_221_prepared/DD_Rank9_TimeFate6_CurrentSource_221_DELIVERY.json'
RETURN221_DIR=BASE/'rank9_timefate6_return221_received'
RETURN221_ZIP=RETURN221_DIR/'DD_Rank9_TimeFate4_Director_Return221_HELD.zip'
RETURN221_DELIVERY=RETURN221_DIR/'DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json'
RETURN221_AUDIT=BASE/'RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json'
RETURN221_RECEIPT=BASE/'RANK9_TIMEFATE6_RETURN221_RECEIPT.json'
RETURN238_DIR=BASE/'rank9_agencycontrol9_return238_received'
RETURN238_ZIP=RETURN238_DIR/'DD_Rank9_AgencyControl2_Director_Return238.zip'
RETURN238_DELIVERY=RETURN238_DIR/'DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json'
RETURN238_AUDIT=BASE/'RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json'
RETURN238_RECEIPT=BASE/'RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json'
PACKET238=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238.zip'
PACKET238_DELIVERY=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json'
OUT=BASE/'rank9_timefate6_current_source_239_prepared'

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def jb(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def bind(p,raw=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def safe(n):
 p=PurePosixPath(n)
 return bool(n) and '\\' not in n and not p.is_absolute() and all(x not in ('','.','..') and not x.startswith('.') for x in p.parts)

def main():
 assert not OUT.exists(),f'Output already exists: {OUT}'
 required=[QUEUE0,HANDOFF0,PENDING0,INDEX,CATALOG,OLD_PACKET,OLD_DELIVERY,RETURN221_ZIP,RETURN221_DELIVERY,RETURN221_AUDIT,RETURN221_RECEIPT,RETURN238_ZIP,RETURN238_DELIVERY,RETURN238_AUDIT,RETURN238_RECEIPT,PACKET238,PACKET238_DELIVERY]
 for p in required: assert p.is_file(),f'Missing required evidence: {p}'
 now=datetime.now(timezone.utc).isoformat()
 q0,h0,p0=readj(QUEUE0),readj(HANDOFF0),readj(PENDING0)
 index,catalog=readj(INDEX),readj(CATALOG)
 d238=readj(RETURN238_DELIVERY); a238=readj(RETURN238_AUDIT); r238=readj(RETURN238_RECEIPT)
 d221=readj(RETURN221_DELIVERY); a221=readj(RETURN221_AUDIT); r221=readj(RETURN221_RECEIPT)
 packet238_raw=PACKET238.read_bytes(); source_deliv=readj(PACKET238_DELIVERY)
 assert q0['currentAuthority']==h0['currentAuthority']==p0['authority']==AUTH
 assert p0['pendingCount']==37 and set(IDS)<=set(p0['pendingIds'])
 assert index['authoredCounts']=={'reviewed':811,'pending':37} and index['representationCounts']['completeReviewedStandaloneProcedures']==535
 assert a238['status']=='PASS' and r238['status']=='PASS' and d238['acceptedIds']==d238['appliedIds']==[]
 assert d238['heldIds']==['absolute-domination','puppetmaster-s-realm'] and d238['nextPendingGroup']=={'group':GROUP,'spellIds':IDS}
 assert d221['heldIds']==IDS and d221['acceptedIds']==[] and d221['accepted'] is False and d221['applied'] is False and a221['status']=='PASS_PACKAGE_BINDING_AND_SCOPE; ALL_FOUR_SEMANTIC_HOLDS_RETAINED'
 assert source_deliv['sourceAuthority']==AUTH and source_deliv['pendingIds']==['absolute-domination','puppetmaster-s-realm']
 group=next(x for x in q0['currentPendingGroups'] if x['group']==GROUP)
 assert group['pendingIds']==IDS and group['pendingCount']==4
 ix={x['id']:x for x in index['entries']}; cat={x['id']:x for x in catalog['spells']}
 for sid in IDS:
  assert sid in p0['pendingIds'] and ix[sid]['authoredStatus']=='pending-authored-procedure' and ix[sid]['sourceStatus']=='blocked-pending-operational-review' and cat[sid].get('operational') is None
 for sid in ['time-fracture','foresight-perfect']: assert sid not in p0['pendingIds']
 # Use the already assembled 140-source Time/Fate package as a source map, then refresh every referenced source from this checkout.
 with zipfile.ZipFile(OLD_PACKET) as old:
  assert old.testzip() is None
  candidate_old=json.loads(old.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json'))
  source_rows=candidate_old['sourceBindings']; assert len(source_rows)==140
  out={}; refreshed={}; changed=[]; current_bindings=[]
  for row in source_rows:
   path=row['path']; assert safe(path)
   raw=(ROOT/path).read_bytes(); current_bindings.append({'path':path,'bytes':len(raw),'sha256':sha(raw)})
   refreshed['sources_current/'+path]=raw
   oldraw=old.read('sources_current/'+path)
   if oldraw!=raw: changed.append({'path':path,'previousPacketSha256':sha(oldraw),'currentSha256':sha(raw),'currentBytes':len(raw)})
  for name in old.namelist():
   if name.startswith('sources_current/') or name=='MANIFEST.json': continue
   out['historical_packet_221/'+name]=old.read(name)
 # Bundle full prior Time/Fate Return221 (all four held), Return238, their audit receipts, and current-source evidence.
 for name,p in [
  ('authority_history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD.zip',RETURN221_ZIP),
  ('authority_history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json',RETURN221_DELIVERY),
  ('authority_history/return221/INDEPENDENT_AUDIT.json',RETURN221_AUDIT),
  ('authority_history/return221/RECEIPT.json',RETURN221_RECEIPT),
  ('authority_history/return238/DD_Rank9_AgencyControl2_Director_Return238.zip',RETURN238_ZIP),
  ('authority_history/return238/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json',RETURN238_DELIVERY),
  ('authority_history/return238/INDEPENDENT_AUDIT.json',RETURN238_AUDIT),
  ('authority_history/return238/RECEIPT.json',RETURN238_RECEIPT),
  ('authority_history/packet238/DD_Rank9_AgencyControl9_CurrentSource_238.zip',PACKET238),
  ('authority_history/packet238/DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json',PACKET238_DELIVERY),
 ]: out[name]=p.read_bytes()
 source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(); assert branch=='main'
 snapshot={'kind':'working-tree','headCommit':source_commit,'branch':branch,'indexBinding':bind(INDEX),'catalogBinding':bind(CATALOG)}
 context={'id':'TIMEFATE6-CURRENT-SOURCE-CONTEXT-239','recordedAtUtc':now,'sourceAuthority':AUTH,'sourceSnapshot':snapshot,'group':GROUP,'pendingIds':IDS,
  'currentIndexBinding':bind(INDEX),'currentCatalogBinding':bind(CATALOG),'currentPendingAuditInput':bind(PENDING0),'currentQueueInput':bind(QUEUE0),'currentHandoffInput':bind(HANDOFF0),
  'currentPacket238':bind(PACKET238),'currentPacket238Delivery':bind(PACKET238_DELIVERY),'return238Archive':bind(RETURN238_ZIP),'return238Delivery':bind(RETURN238_DELIVERY),'return238Audit':bind(RETURN238_AUDIT),'return238Receipt':bind(RETURN238_RECEIPT),
  'priorTimeFateReturn221Archive':bind(RETURN221_ZIP),'priorTimeFateReturn221Delivery':bind(RETURN221_DELIVERY),'priorTimeFateReturn221Audit':bind(RETURN221_AUDIT),'priorTimeFateReturn221Receipt':bind(RETURN221_RECEIPT),
  'acceptedIds':[],'appliedIds':[],'previousBlockers':{'time-stop':['TF192-B01'],'eternal-prophecy':['TF192-B02'],'fate-rewrite':['TF192-B04'],'collapse-timeline':['TF192-B05']},
  'sourceBindingsRefreshed':len(current_bindings),'sourceBindingRefreshDiff':changed}
 candidate=copy.deepcopy(candidate_old)
 candidate.update({'id':'RANK9-TIME-FATE6-CURRENT-SOURCE-CONTEXT-239','recordedAtUtc':now,'status':'CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_811_REVIEWED_37_PENDING_AUTHORITY',
  'currentAuthority':AUTH,'currentPendingGroup':{'group':GROUP,'spellIds':IDS,'count':4},'currentIndexBinding':bind(INDEX),'currentCatalogBinding':bind(CATALOG),
  'currentPendingAuditInputBinding':bind(PENDING0),'currentQueueInputBinding':bind(QUEUE0),'currentHandoffInputBinding':bind(HANDOFF0),'sourceSnapshot':snapshot,
  'currentSourceCommit':source_commit,'currentBranch':branch,'sourceBindings':current_bindings,'currentPendingIdSet':sorted(p0['pendingIds']),
  'sourceBindingRefresh':{'sourceFiles':len(current_bindings),'changedSinceTimeFateSourcePacket221':changed,'allSourceBindingsRefreshedFromWorkingTree':True},
  'countsUnchanged':{'reviewed':811,'pending':37},'priorTimeFateReturn221ReceiptBinding':bind(RETURN221_RECEIPT),'priorTimeFateReturn221AuditBinding':bind(RETURN221_AUDIT),
  'currentAgencyControlReturn238Binding':bind(RETURN238_ZIP),'currentAgencyControlReturn238AuditBinding':bind(RETURN238_AUDIT),'queueCandidateBinding':copy.deepcopy(group.get('candidate',{}))})
 request=(
  'GPT director — continue the ordinary-spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied, '
  'with 535 complete standalone procedures and 173 scoped interfaces. Review only the four pending Rank9 Time/Fate6 identities: time-stop, fate-rewrite, collapse-timeline, and eternal-prophecy. '
  'Do not re-review completed feats, time-fracture, foresight-perfect, other accepted spells, or any other pending cohort.\n\n'
  f'Current source snapshot: branch {branch}, HEAD {source_commit}; current index/catalog and queue238, handoff238, pending-audit238, plus the independently audited Return238 and its source packet are included. '
  'Return238 held only absolute-domination and puppetmaster-s-realm; it did not change spell authority. GPT selected Time/Fate6 as the next group.\n\n'
  'Reassess only the four current Time/Fate6 pending identities against refreshed source. The prior sealed Return221 independently retained TF192-B01 for time-stop, TF192-B04 for fate-rewrite, TF192-B05 for collapse-timeline, and TF192-B02 for eternal-prophecy. '
  'The complete Return221 archive, delivery manifest, independent audit and receipt are attached alongside the earlier detailed evidence in historical_packet_221. Close a blocker only with the exact source-grounded witness; preserve conditional qualifications and unrelated holds.\n\n'
  'Return explicit accepted/held rulings for only those four IDs, exact blocker and qualification IDs, source-faithful procedures, reversible before/after traces, exact costs/deadlines/resource and custody histories, and a verifiable ZIP plus delivery manifest bound to this packet. '
  'Keep all acceptances unapplied; do not edit canonical files or execute supplied programs. Preserve runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates. I will independently audit and apply only exact acceptances.')
 source_context=copy.deepcopy(context)
 candidate_raw=jb(candidate); context_raw=jb(source_context); request_raw=(request+'\n').encode()
 out.update(refreshed)
 out['authority_current/authored_review_index.json']=INDEX.read_bytes(); out['authority_current/catalog.json']=CATALOG.read_bytes()
 out['authority_current/CURRENT_SPELL_QUEUE_238_INPUT.json']=QUEUE0.read_bytes(); out['authority_current/CURRENT_HANDOFF_238_INPUT.json']=HANDOFF0.read_bytes(); out['authority_current/CURRENT37_PENDING_IDENTITY_AUDIT_238_INPUT.json']=PENDING0.read_bytes()
 out['CURRENT_SOURCE_CONFERENCE_CANDIDATE_239.json']=candidate_raw; out['CURRENT_CONTEXT_239.json']=context_raw; out['REQUEST_239.txt']=request_raw
 assert len(out)==len(set(out)) and all(safe(x) for x in out)
 rows=[{'path':n,'bytes':len(raw),'sha256':sha(raw),'crc32':crc(raw)} for n,raw in sorted(out.items())]
 manifest={'id':'RANK9-TIME-FATE6-CURRENT-SOURCE-PACKET-MANIFEST-239','sourceSnapshot':snapshot,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':IDS,'payloadMemberCount':len(rows),'members':rows}
 OUT.mkdir(parents=True)
 packet=OUT/'DD_Rank9_TimeFate6_CurrentSource_239.zip'
 with zipfile.ZipFile(packet,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,raw in sorted(out.items()): z.writestr(n,raw)
  z.writestr('MANIFEST.json',jb(manifest))
 with zipfile.ZipFile(packet) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1
  for row in rows:
   raw=z.read(row['path']); assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and crc(raw)==row['crc32']
 packet_bind=bind(packet); candidate_path=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_239.json'; candidate_path.write_bytes(candidate_raw)
 context_path=OUT/'CURRENT_CONTEXT_239.json'; context_path.write_bytes(context_raw)
 request_path=OUT/'REQUEST_239.txt'; request_path.write_bytes(request_raw)
 delivery_path=OUT/'DD_Rank9_TimeFate6_CurrentSource_239_DELIVERY.json'
 delivery={'id':'RANK9-TIME-FATE6-CURRENT-SOURCE-DELIVERY-239','status':'PREPARED_UNSENT','archive':packet_bind,'memberCount':len(rows)+1,'payloadMemberCount':len(rows),
  'sourceSnapshot':snapshot,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':IDS,'candidate':bind(candidate_path),'sourceFilesRefreshed':len(current_bindings),
  'sourceFilesChangedSinceTimeFateSourcePacket221':changed,'accepted':False,'applied':False,'conversation':CHAT}
 delivery_path.write_bytes(jb(delivery)); delivery_bind=bind(delivery_path)
 prep_path=BASE/'RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json'
 prep={'id':'RANK9-TIMEFATE6-SOURCE-PREPARATION-239','recordedAtUtc':now,'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT','sourceAuthority':AUTH,'sourceSnapshot':snapshot,'group':GROUP,'pendingIds':IDS,
  'priorTimeFateReturn221':bind(RETURN221_ZIP),'priorTimeFateReturn221Audit':bind(RETURN221_AUDIT),'latestReturn238':bind(RETURN238_ZIP),'latestReturn238Audit':bind(RETURN238_AUDIT),
  'sourceFilesRefreshed':len(current_bindings),'changedSinceTimeFateSourcePacket221':changed,'packet':packet_bind,'deliveryManifest':delivery_bind,'payloadMemberCount':len(rows),
  'checksPassed':10,'checksFailed':0,'checks':[{'check':x,'passed':True} for x in [
   'Authority 811/37/0 and 535/173 counts agree across index, queue, handoff and pending audit','Exactly four Time/Fate6 targets remain pending; already accepted identities remain excluded',
   'Return238 is independently audited and selects this exact next group without changing authority','Return221 all-held archive, delivery, audit and receipt are bound into the current packet',
   'All 140 Time/Fate6 source bindings are refreshed from current working-tree bytes','Current index/catalog status for every target matches the pending queue',
   'Current index, catalog, queue, handoff and pending audit plus 238 source archive evidence are included','Request carries forward all four prior blocker IDs and prohibits unrelated re-review/application',
   'All packet member paths are safe and unique; archive manifest and all SHA/CRC/size rows verify','No canonical changes, acceptances, applications or program execution occurred during preparation']],
  'canonicalChangesBeforePreparation':False,'accepted':False,'applied':False,'request':request}
 prep_path.write_bytes(jb(prep)); prep_bind=bind(prep_path)
 record_path=BASE/'RANK9_TIMEFATE6_PACKET_239.json'
 record={'id':'RANK9-TIMEFATE6-PACKET-239','status':'PREPARED_UNSENT','sourceAuthority':AUTH,'group':GROUP,'pendingIds':IDS,'packet':packet_bind,'deliveryManifest':delivery_bind,'preparation':prep_bind,'candidate':bind(candidate_path),'conversation':CHAT,'checksPassed':10,'checksFailed':0}
 record_path.write_bytes(jb(record)); record_bind=bind(record_path)
 pending=copy.deepcopy(p0); pending.update({'id':'CURRENT37-PENDING-IDENTITY-AUDIT-239','recordedAtUtc':now,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET_WITH_TIME_FATE6_PACKET_239',
  'currentReturnAudit':bind(RETURN238_AUDIT),'preparedNextGroup':{'group':GROUP,'pendingIds':IDS,'packet':packet_bind,'deliveryManifest':delivery_bind}})
 pending_path=BASE/'CURRENT37_PENDING_IDENTITY_AUDIT_239.json'; pending_path.write_bytes(jb(pending)); pending_bind=bind(pending_path)
 # The latest actual director return is Return238; preserve its two holds and queue Time/Fate6 next.
 decision=json.loads(zipfile.ZipFile(RETURN238_ZIP).read('DIRECTOR_DECISION.json'))
 blockers={x['spellId']:x['blockerIds'] for x in decision.get('perIdentity',[])}
 last={'return':238,'group':'rank9-agency-control9','ids':d238['heldIds'],'acceptedIds':[],'appliedIds':[],'heldIds':d238['heldIds'],'blockers':blockers,
  'authorityAfter':AUTH,'auditStatus':'PASS','archive':bind(RETURN238_ZIP),'delivery':bind(RETURN238_DELIVERY),'independentAudit':bind(RETURN238_AUDIT),'receipt':bind(RETURN238_RECEIPT)}
 q=copy.deepcopy(q0); tg=next(x for x in q['currentPendingGroups'] if x['group']==GROUP)
 tg.update({'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37','preparedPacket':packet_bind,'deliveryManifest':delivery_bind,'packetRecord':record_bind,'preparation':prep_bind,'freshPacketRequiredForCurrentAuthority':False})
 q.update({'id':'SPELL-REVIEW-QUEUE-239','recordedAtUtc':now,'supersedesQueue':bind(QUEUE0),'parentQueue':bind(QUEUE0),'currentReturnAudit':{'status':'PASS','return':238,'archive':bind(RETURN238_ZIP),'deliveryManifest':bind(RETURN238_DELIVERY),'independentAudit':bind(RETURN238_AUDIT),'receipt':bind(RETURN238_RECEIPT),'sourceArchive':bind(PACKET238),'sourceDeliveryManifest':bind(PACKET238_DELIVERY),'independentReplay':True},
  'currentReturnDelivery':bind(RETURN238_DELIVERY),'currentReturnArchive':bind(RETURN238_ZIP),'currentReturnDecision':{'path':bind(RETURN238_ZIP)['path']+'#DIRECTOR_DECISION.json'},'lastReviewedBatch':last,
  'nextGroup':GROUP,'next':{'group':GROUP,'pendingIds':IDS,'pendingCount':4,'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT','packet':packet_bind,'deliveryManifest':delivery_bind,'packetRecord':record_bind,'preparation':prep_bind,'candidate':bind(candidate_path)},
  'nextPreparedRequest':{'group':GROUP,'pendingIds':IDS,'request':bind(request_path),'status':'PREPARED_UNSENT'},'currentPreparation':prep_bind,'currentPacket':packet_bind,'currentDeliveryManifest':delivery_bind,'currentPacketDelivery':delivery_bind,
  'currentReturnSourceArchive':bind(PACKET238),'currentReturnSourceDelivery':bind(PACKET238_DELIVERY),'currentReturnReceipt':bind(RETURN238_RECEIPT),'currentPacketAudit':bind(RETURN238_AUDIT),'currentPacketAuditStatus':'PASS',
  'pendingIdentityAudit':pending_bind,'pendingCount':37,'packetStatus':'RANK9_TIMEFATE6_CURRENT_SOURCE_PACKET_239_PREPARED_UNSENT_811_37','githubChanges':False})
 queue_path=BASE/'CURRENT_SPELL_QUEUE_239.json'; queue_path.write_bytes(jb(q)); queue_bind=bind(queue_path)
 h=copy.deepcopy(h0); preserved=copy.deepcopy(h.get('preservedOtherHolds',[]))
 preserved.append({'ids':d238['heldIds'],'blockerIds':blockers,'decision':bind(RETURN238_ZIP),'independentAudit':bind(RETURN238_AUDIT),'acceptedIds':[],'appliedIds':[]})
 h.update({'id':'CURRENT-HANDOFF-239','recordedAtUtc':now,'status':'RANK9_TIMEFATE6_CURRENT_SOURCE_PACKET_239_PREPARED_UNSENT_811_37','currentAuthority':AUTH,'latestBatch':last,
  'preservedOtherHolds':preserved,'nextGroup':GROUP,'nextStep':{'group':GROUP,'pendingIds':IDS,'pendingCount':4,'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT','packet':packet_bind,'deliveryManifest':delivery_bind},
  'pendingIdentityAudit':pending_bind,'queue':queue_bind,'currentPreparation':prep_bind,'currentPacket':packet_bind,'currentPacketDelivery':delivery_bind,
  'currentReturnArchive':bind(RETURN238_ZIP),'currentReturnDelivery':bind(RETURN238_DELIVERY),'currentReturnAudit':bind(RETURN238_AUDIT),'currentReturnReceipt':bind(RETURN238_RECEIPT),
  'currentReturnSourceArchive':bind(PACKET238),'currentReturnSourceDelivery':bind(PACKET238_DELIVERY),'appliedThisStep':False,'githubChanges':False,'runtimeSelectionEnabled':False,'canonicalRuntimeApplicationPerformed':False})
 handoff_path=BASE/'CURRENT_HANDOFF_239.json'; handoff_path.write_bytes(jb(h)); handoff_bind=bind(handoff_path)
 (BASE/'CURRENT_SPELL_REVIEW_SNAPSHOT_239.md').write_text(
  '# Current ordinary spell-review checkpoint 239\n\n'
  '**811 reviewed/applied / 37 pending / 0 accepted-unapplied**, with 535 complete standalone procedures and 173 scoped interfaces. Return238 passed independent package/source verification and held absolute-domination and puppetmaster-s-realm. GPT selected the four still-pending Time/Fate6 identities for the next fresh-source review: time-stop, fate-rewrite, collapse-timeline, and eternal-prophecy. Return221 remains the prior independently audited all-held decision for this group. Packet239 is prepared and not yet sent.\n\n'
  'See [handoff](CURRENT_HANDOFF_239.json), [queue](CURRENT_SPELL_QUEUE_239.json), [pending audit](CURRENT37_PENDING_IDENTITY_AUDIT_239.json), [packet record](RANK9_TIMEFATE6_PACKET_239.json), and [source packet](rank9_timefate6_current_source_239_prepared/DD_Rank9_TimeFate6_CurrentSource_239.zip).\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':'PREPARED_UNSENT','authority':AUTH,'group':GROUP,'pendingIds':IDS,'refreshedSources':len(current_bindings),'changedSinceTimeFateSourcePacket221':changed,'packet':packet_bind,'deliveryManifest':delivery_bind,'payloadMembers':len(rows),'queue':queue_bind,'handoff':handoff_bind},indent=2))

if __name__=='__main__': main()
