import json,pathlib,hashlib,zlib,zipfile,copy
R=pathlib.Path(__file__).resolve().parent; S=R/'source'; P=R/'payload'
def read(p):return json.loads(p.read_bytes())
def write(name,x):
 p=P/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def bind(b,path=None):
 d={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
 return {'path':path,**d} if path else d
authority={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
target='banishment-gate';nextid='conjure-demiplane-fortress';nextgroup='rank9-planar-gates5';nextblock=['PG200-B06']
audit=read(P/'DATA_INTEGRITY_CHECK.json');assert audit['failed']==0
counts={**audit['counts'],'dataIntegrityChecks':audit['checkCount'],'failedDataChecks':0}
prior=read(S/'prior/PG200_BANISHMENT_DIRECTOR_DISPOSITION.json');procedure=read(S/'prior/procedures/banishment-gate.json')
acpath='evidence/index-bound/AC5_REVIEWED_SPELLS.json';ac=read(P/acpath);fc=ac['profiles']['AC5-PROFILE-FACTION-CHAMPION-01'];fsp=ac['spells'][14]
anchor=lambda ptr: {'path':acpath,'pointer':ptr}
gains=[
 {'id':'PG327-B03-SOURCE-PROFILE','parentBlocker':'PG200-B03','status':'CLOSED_SOURCE_AVAILABILITY_SUBPART_ONLY','finding':'Current exact accepted AC5 establishes Faction Champion as Humanoid for mechanical targeting, with a native Wizard route. The old absence-of-a-second-explicit-type source premise is superseded. This does not demonstrate a Banishment Gate nonmatching crossing.','anchors':[anchor('/profiles/AC5-PROFILE-FACTION-CHAMPION-01'),anchor('/spells/14/completeSourceAndAccess'),anchor('/spells/14/procedure')],'constraints':['alliedStatus=true','current standing > 0','invocation permission','no aid ban','actual legal acquisition, cast, body and command histories in the integrated test','conditional test facts remain conditional; no membership, native origin, soul, canonical faction or campaign event inferred']},
 {'id':'PG327-B04-FINITE-CARGO-CONTRACT','parentBlocker':'PG200-B04','status':'CLOSED_SOURCE_RULE_AVAILABILITY_SUBPART_ONLY','finding':'Accepted AC5 provides finite summoned-body ending, intrinsic-gear disappearance and genuine-object persistence/drop rules. Its accepted Elemental Banishment example AC5-X17 also provides separate-body and terminal cargo precedent in that exact interface. Neither is a new Gate case or a wholesale transfer of AC5-BANISH-EXT to Gate.','anchors':[anchor('/profiles/AC5-PROFILE-FACTION-CHAMPION-01/ending'),anchor('/profiles/AC5-PROFILE-FACTION-CHAMPION-01/intrinsicGear'),anchor('/profiles/AC5-PROFILE-FACTION-CHAMPION-01/nullHealing'),{'path':'evidence/packet327/current_sources/AC5_FACTION_CHAMPION_CASES.json','pointer':'/4','caseId':'AC5-X17'}],'constraints':['No corpse is produced by an expired Champion or Fire Pet.','No intrinsic equipment becomes loot or genuine cargo.','The accepted AC5 source expiry/cargo example is authored comparison evidence, not a full newly replayed Gate witness.']}
]
remaining=[
 {'id':'PG327-W01','blockerId':'PG200-B03','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-A','RANK9PLANARGATES5129-BANISHMENT-GATE-A/unknown-type'],'missing':'An integrated nonmatching crossing using the now-source-qualified Humanoid Champion against a gate fixed to Elemental, alongside retained matching ally/enemy admissions.','minimumWitness':'Bind the accepted AC5 envelope/receipt and native Wizard route; enumerate the summoner acquisition/repertoire, full legal actor, source-qualified faction identifier and four eligibility inputs, paid Action/V/S/F/10 RP creation within 60 ft, concentration and 60-second source clock; give the Champion complete body/gear/custody and lawful command/phase/movement history through the 10x15 opening. Record no exile, no save and no hard-denial claim for nonmatching Humanoid, while the qualifying Elementals establish their own cells. Preserve unknown-type non-diagnostic behavior separately. Conditional case facts may be used under PG200-H02; do not call them actual campaign facts.','sourceAlreadyAvailable':True},
 {'id':'PG327-W02','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-A/touch-only'],'missing':'A complete body touches the boundary without crossing; the current event 4 only records a rule observation.','minimumWitness':'Use a source-legal typed body and lawful movement with explicit aperture/body geometry and before/after coordinates; demonstrate no admission, no cell and no claim; retain movement and resources exactly. No new general rule is required.'},
 {'id':'PG327-W03','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-A/stationary-type-change'],'missing':'A real authorized type-changing source and actor, with a stationary body and no new crossing.','minimumWitness':'Bind a source that actually changes mechanical creature type, its lawful acquisition, payment, duration and body/cargo mapping. Process it at an unchanged position and show no gate trigger merely from the change. Do not turn school, appearance, ancestry, separate summon replacement or visual transformation into a same-body type transition.'},
 {'id':'PG327-W04','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-A/already-claimed'],'missing':'An already-spent creator/target/encounter guard followed by a genuine later crossing, plus duplicate-event treatment.','minimumWitness':'Fork an actually admitted target with its existing claim; settle/return it lawfully without resetting encounter/creator/body IDs, then pay the later movement/command opportunity and attempt the crossing. Show no second cell or refreshed claim. A duplicate crossing ID reuses its receipt; a distinct crossing cannot erase the spent guard.'},
 {'id':'PG327-W05','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-B/separate-carried-creature'],'missing':'Full Gate admission with a separate living body being carried and explicit lawful separation/fit.','minimumWitness':'Bind both complete bodies, carried relation, consent/permission where required, custody and geometry. Demonstrate the separate creature remains at the origin when lawful separation succeeds; if impossible, show atomic exile failure with no claim, deletion or creature-to-gear conversion. AC5-X17 is a source-backed comparison, not this Gate history.'},
 {'id':'PG327-W06','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-B/primary-independent-escape'],'missing':'An acquired escape source that actually reaches a known authorized external site from this cell, and a paid successful escape.','minimumWitness':'Bind the route, actor acquisition, actual eligible target/destination, costs/components/opportunity, destination knowledge/geometry and applicable blockers. Trace primary escape ending only its own cell, settling residual cargo once, preserving other cells/gate and all independent clocks. No default teleport or invented destination.'},
 {'id':'PG327-W07','blockerId':'PG200-B04','caseIds':[],'missing':'An eligible admitted primary with a source-established death/corpse lifecycle and actual corpse handling.','minimumWitness':'Bind a complete typed primary whose actual lifecycle leaves remains, its lawful admission, actual lethal/zero/death settlement, extant corpse and original equipment/cargo, then exact cell closure/return or terminal placement conflict. The finite Champion/Fire Pet ending cannot supply a corpse.'},
 {'id':'PG327-W08','blockerId':'PG200-B04','caseIds':['RANK9PLANARGATES5129-BANISHMENT-GATE-B/summon-expiry'],'missing':'An actual finite-summon source expiration inside a Gate cell with separately acquired genuine cargo.','minimumWitness':'Instantiate the accepted finite profile under its real route and eligibility, pay creation, record original deadline and cargo owner/custodian/physical identity before admission. At that original deadline end the body/intrinsic gear without a corpse; preserve loose genuine cargo and apply only Gate\'s expressly selected terminal settlement. Record occupied return/blocked placement, no duplicate item, no second ending/refill/refund, and complete actor/attached clocks.'}
]
blocks=[]
for bid in ['PG200-B03','PG200-B04']:
 b=copy.deepcopy(next(x for x in prior['blockers'] if x['id']==bid));b['historicalMissingText']=b.pop('missing');b['status']='OPEN';b['missing']='; '.join(x['missing'] for x in remaining if x['blockerId']==bid);b['minimalCorrection']=[x['id'] for x in remaining if x['blockerId']==bid];b['closedNarrowSubparts']=[x['id'] for x in gains if x['parentBlocker']==bid];blocks.append(b)
write('BLOCKER_REASSESSMENT.json',{'id':'PG327-BLOCKER-REASSESSMENT','scope':[target],'wholeIdentityDecision':'HOLD','sourceLevelGains':gains,'blockers':blocks,'minimumWitnesses':remaining,'noCampaignPromotion':True,'noBlockerWaiver':True})
# Preserve exact historical qualifications with an explicit present-authority overlay.
oldpath=R.parent/'return284_payload/prior243/HOLD_REGISTER.json';old=read(oldpath);quals=old['conditionalQualifications'];assert len(quals)==10
historicalQ=[{k:q[k] for k in ('id','scope','qualification','status','blocking')} for q in quals]
write('evidence/HISTORICAL_QUALIFICATIONS_EXTRACT.json',{'sourceBinding':bind(oldpath.read_bytes(),'return284_payload/prior243/HOLD_REGISTER.json'),'sourcePointer':'/conditionalQualifications','records':historicalQ})
currentQ=copy.deepcopy(historicalQ)
for q in currentQ:
 if q['id']=='PG200-H08':q['qualification']='No domain closure, ordinary-review completion, engine readiness or release approval. Current authority remains 823 reviewed/applied / 25 pending / 0 accepted-unapplied; 547 procedures / 173 interfaces.'
 if q['id']=='PG200-H10':q['qualification']='All unrelated current holds and prior acceptances remain as bound in Packet327 queue/handoff/pending audit. Historical holds superseded by later acceptance/application are not revived. No outside identity is adjudicated.'
write('QUALIFICATIONS.json',{'currentAuthority':authority,'qualifications':currentQ,'historicalTextPreservedAt':'evidence/HISTORICAL_QUALIFICATIONS_EXTRACT.json','application':False,'canonicalChanges':False,'runtimeExecuted':False,'suppliedProgramsExecuted':False,'gatesClosed':['source-qualified actual acquisition/use','implementation','runtime','human-play','balance','cosmology','domain-closure','ordinary-review completion','release']})
native=next(x for x in read(S/'authority/catalog_selected.json')['spells'] if x['id']==target)
assert native==procedure['nativeCardUnchanged']
write('PROCEDURE_CURRENT.json',{'id':'PG327-BANISHMENT-GATE-PROCEDURE','spellId':target,'status':'HELD_STATIC_PROCEDURE_PRESERVED','accepted':False,'applied':False,'currentAuthority':authority,'exactProcedureMember':'evidence/packet327/prior/procedures/banishment-gate.json','nativeCard':native,'sourceVsAuthorship':'Native automatic specific-type portal, exact four class routes/rank9/class17/base26RP preserved. Core Action/120ft/V,S,F/Instantaneous remains native metadata; gate concentration600s, independent60s cells, geometry and terminal extensions are expressly inherited NEW local authoring, not printed source facts.','procedure':procedure['procedure'],'sharedContract':procedure['sharedContract'],'currentQualificationsOverrideHistoricalAuthorityOnly':'QUALIFICATIONS.json','AC5EvidenceIntegration':gains,'currentBlockerIds':['PG200-B03','PG200-B04'],'minimumWitnessReference':'BLOCKER_REASSESSMENT.json'})
cases=read(P/'REPLAY_RESULTS.json')['cases'];coverage=[]
for c in cases:
 cid=c['id'];req=[x['id'] for x in remaining if cid in x['caseIds']]
 if cid.endswith('-A'):result='Two concrete Elemental admissions replay; Humanoid nonmatching crossing remains absent.'
 elif cid.endswith('-B'):result='Two Elemental cells, independently recorded admissions and occupied terminal closure replay; separate-body, escape, corpse and finite-expiry/cargo main obligation remains incomplete.'
 else:result='Rule-only fixture at zero-based /events/4; no actual target/transition establishing its named branch. Replayed as recorded, not promoted to a positive witness.'
 coverage.append({'id':cid,'statusPreserved':c['statusPreserved'],'eventCount':c['eventCount'],'replay':'PASS','wholeRequiredCaseComplete':False,'result':result,'remainingWitnessIds':req})
write('CASE_DISPOSITIONS.json',{'cases':coverage,'deadPrimaryCorpseCase':'Absent; PG327-W07 remains required','AC5Examples':'Five accepted authored examples are preserved as source context; no new full-state replay or Gate encounter is claimed for them.','allPassingPreservedStateOperationsRetained':True})
qrows=[]
for q in prior['questionDispositions']:
 row=copy.deepcopy(q);row['return327Scope']=[target];row['currentDisposition']='PRESERVED_SELECTED_LOCAL_PROCEDURE_WITH_LINKED_WITNESS_HOLDS';row['currentBlockerIds']=['PG200-B03','PG200-B04']
 row['currentUpdate']='No source or selected mechanic changed. Applicable outside-spell references remain historical context, not new rulings.'
 if q['id']=='PG9-Q13':row['currentUpdate']='Accepted AC5 now supplies explicit Humanoid classification and Wizard source route; PG327-B03-SOURCE-PROFILE closes that source-availability subpart. Integrated nonmatching crossing still missing.'
 if q['id'] in ['PG9-Q17','GATE129-ADD01']:row['currentUpdate']='Accepted AC5 finite-body/cargo and separate-carriage comparison supports source rule availability only. Gate-specific full states and terminal transitions remain under B04.'
 qrows.append(row)
write('QUESTION_DISPOSITIONS.json',{'adjudicatedIdentity':target,'count':len(qrows),'questions':qrows,'scope':'Ten target-relevant records supplied in Packet327; no new ruling for the other Planar identities.'})
write('FUTURE_OBLIGATIONS.json',{'adjudicatedIdentity':target,'obligations':[
 {'id':'PG9-CAST','status':'EXISTING_COMPONENTS_PRESERVED_NEW_WITNESS_HISTORY_REQUIRED','remaining':'AC5 acquired summoner and actual paid Gate/nonmatching crossing history.'},
 {'id':'PG9-AUTOBANISH','status':'INCOMPLETE','remaining':'PG327-W01 through W04.'},
 {'id':'PG9-TRANSPORT','status':'INCOMPLETE','remaining':'PG327-W05 through W08, with exact terminal settlement.'},
 {'id':'PG9-CLOCKS','status':'PRESERVED_CASE_CALENDARS_PASS_NEW_TRACES_REQUIRED','remaining':'No missed scheduled regular starts/ends through the preserved final timestamps; extend full original-source/companion/actor deadlines in new witnesses, not spell pulses.'},
 {'id':'PG9-LIFECYCLE','status':'INCOMPLETE','remaining':'Independent escape, dead primary and finite-summon expiry/cargo inside actual Gate cells.'}]})
sem=[
 ('PG327-S01','PASS','Current scope is Banishment Gate only; native four routes and exact card preserved.'),
 ('PG327-S02','PASS','AC5 LF normalization exactly reproduces indexed accepted envelope and receipt. No stale-envelope blocker.'),
 ('PG327-S03','PASS','Humanoid Champion targeting and conditional Wizard invocation are source-backed; not campaign or native-plane evidence.'),
 ('PG327-S04','HOLD','B03 integrated legal summoner/nonmatching crossing still absent, despite source-level gain.'),
 ('PG327-S05','PASS','Seven named branch records contain QUALIFIED_RULE_INPUT, not the claimed positive transitions; records remain incomplete.'),
 ('PG327-S06','HOLD','B04 touch/type-change/claimed guard and separate-body/escape/corpse/expiry integrated branches absent.'),
 ('PG327-S07','PASS','AC5-X17 accepted Elemental Banishment comparison is not silently generalized into a Gate event; source and local extension boundaries preserved.'),
 ('PG327-S08','PASS','Champion finite ending does not generate a corpse or genuine intrinsic gear; corpse and real cargo requirements remain separate.'),
 ('PG327-S09','PASS','All nine original case bytes, 129 event chains, local inverses and full reverse traversals verified.'),
 ('PG327-S10','PASS','46 START/END markers and all regular actor scheduled starts/ends/next markers through each preserved endpoint verified; actual cost/resource histories included.'),
 ('PG327-S11','PASS','No acceptance/application/canonical changes or outside decisions; source/play/runtime/balance/cosmology/domain/completion/release gates remain.'),
 ('PG327-S12','PASS','Integrity success is explicitly distinct from whole-positive semantic completion; both required main cases remain incomplete.')]
write('INDEPENDENT_SEMANTIC_FAILURE_CHECK.json',{'id':'PG327-SEMANTIC','method':'Independent direct inspection of supplied sources and case transitions, distinct from package-provided assertions and numeric replay. No supplied executable run.','identityDecision':'HOLD','wholeSpellSemanticComplete':False,'checks':[{'id':i,'status':s,'finding':f} for i,s,f in sem],'checkCount':len(sem),'passCount':sum(s=='PASS' for _,s,_ in sem),'holdCount':sum(s=='HOLD' for _,s,_ in sem),'blockerIds':['PG200-B03','PG200-B04'],'integrityCheckCount':counts['dataIntegrityChecks'],'limits':'Source-linked static authored evidence only; no runtime or campaign execution. Actor acquisition assertions embedded in old cases are preserved, not replaced with a new unbound history.'})
counts.update({'semanticChecks':len(sem),'semanticPass':10,'semanticHolds':2})
queue=read(S/'authority/CURRENT_SPELL_QUEUE_327.json');pending=read(S/'authority/CURRENT25_PENDING_IDENTITY_AUDIT_327.json')
write('REMAINING_QUEUE.json',{'authorityUnchanged':authority,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'pendingIds':pending['pendingIds'],'continuingPriorityOrderUnchanged':queue['continuingPriorityOrder'],'separatelyRetainedHolds':queue['separatelyRetainedHolds'],'reviewedHereHeld':[target],'nextIdentity':nextid,'nextGroup':nextgroup,'nextBlockerIds':nextblock,'instruction':'Proceed to Fortress only after independent audit of this return; no outside disposition is made here.'})
decision={'id':'RANK9-PLANARGATES5-BANISHMENT-GATE-DIRECTOR-RETURN327','targetIds':[target],'decision':'HOLD','accepted':False,'applied':False,'held':True,'acceptedIds':[],'appliedIds':[],'heldIds':[target],'blockerIds':['PG200-B03','PG200-B04'],'qualificationIds':[q['id'] for q in currentQ],'sourceLevelGains':gains,'minimumWitnessIds':[x['id'] for x in remaining],'authorityBefore':authority,'authorityAfter':authority,'counts':counts,'applicationDisposition':'None. Identity remains pending. No index/catalog/queue/handoff/runtime/GitHub mutation.','nextIdentity':nextid,'nextGroup':nextgroup,'nextBlockerIds':nextblock,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'outOfScopeHoldsAndAcceptances':'Unchanged as bound by Packet327 authority.'}
write('DIRECTOR_DECISION.json',decision);write('COUNTS.json',counts)
write('VALIDATION.json',{'status':'DATA_PASS_SEMANTIC_HOLD','dataCheckCount':counts['dataIntegrityChecks'],'dataFailed':0,'semanticHoldIds':['PG200-B03','PG200-B04'],'exactCounts':counts,'caseBytesUnchanged':True,'canonicalEdits':False,'application':False})
readme='''# Return327 — Banishment Gate only: HOLD

acceptedIds=[]; appliedIds=[]; heldIds=[banishment-gate]. Authority 823/25/0; 547 procedures / 173 interfaces. No canonical or GitHub changes.

AC5's exact accepted Humanoid Champion profile, native Wizard route, finite-body ending and genuine-cargo rules are verified source-level gains. The raw checkout envelope and receipt normalize by CRLF-to-LF only to their exact indexed bindings. Originals and exact LF derivatives are included.

PG200-B03 remains open for the fully instantiated legal summoner/nonmatching Gate crossing. Conditional authored facts are permitted within their explicit scope; they are not campaign facts. PG200-B04 remains open for actual touch/type-change/claimed-guard, separate living carriage, lawful primary escape, dead-primary/corpse and finite-summon-expiry/cargo encounters. See BLOCKER_REASSESSMENT.json for exact per-witness fields and source anchors. Accepted AC5 examples are source comparisons, not new Gate event traces.

All nine preserved cases remain byte-exact against Return200. 129 events, 258 forward and 258 inverse operations, nine full reverse traversals; 46 regular START/END markers. Data checks pass; both main-case whole-spell obligations remain incomplete. Seven branch records retain their qualified rule-only status. No positive facts were manufactured.

PG200-H01 through H10 retained. Historical authority wording remains in historical evidence, with current authority explicitly overriding obsolete snapshots. Runtime, implementation, human-play, balance, cosmology, domain closure, completion and release remain unapproved. Native source/access qualifications remain.

Next: conjure-demiplane-fortress / PG200-B06, rank9-planar-gates5. 25 closure tasks, zero first-review tasks remain.

MANIFEST.json binds every payload except itself; external DELIVERY binds every member including MANIFEST and the complete ZIP. Hashes cover exact bytes; state hashes use the preserved Return200 JSON serialization. Supplied programs were not executed.
'''
(P/'README.md').write_text(readme)
# Include only this turn's independent verification/sealing scripts for reproducibility.
for name in ['audit327.py','seal327.py']:
 dst=P/'verification'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((R/name).read_bytes())
payloads=sorted(f for f in P.rglob('*') if f.is_file() and f.name!='MANIFEST.json');manifest={'id':'RETURN327-MEMBER-MANIFEST','scope':[target],'authority':authority,'acceptedIds':[],'appliedIds':[],'heldIds':[target],'inputArchive':read(P/'SOURCE_BINDINGS.json')['packet'],'payloadEntryCount':len(payloads),'memberCount':len(payloads)+1,'selfExcluded':True,'counts':counts,'members':[bind(f.read_bytes(),str(f.relative_to(P))) for f in payloads]};write('MANIFEST.json',manifest)
files=sorted(f for f in P.rglob('*') if f.is_file());name='DD_Rank9_BanishmentGate_Director_Return327_HELD.zip';zp=R/name
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:
  info=zipfile.ZipInfo(str(f.relative_to(P)),(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
sealed=[]
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None; sealed.append('archive CRC/readback')
 assert z.namelist()==[str(f.relative_to(P)) for f in files];sealed.append('exact sorted allowlist')
 assert len(z.namelist())==len(set(z.namelist()));sealed.append('unique members')
 for f in files:
  n=str(f.relative_to(P));assert z.read(n)==f.read_bytes();sealed.append('bytes:'+n);assert z.getinfo(n).CRC==(zlib.crc32(f.read_bytes())&0xffffffff);sealed.append('crc:'+n)
 for m in manifest['members']:assert bind(z.read(m['path']),m['path'])==m
 sealed.append('all internal payload hashes')
 dd=json.loads(z.read('DIRECTOR_DECISION.json')); assert dd['counts']==counts==json.loads(z.read('COUNTS.json'))==json.loads(z.read('VALIDATION.json'))['exactCounts'];sealed.append('count mirrors')
 assert dd['acceptedIds']==dd['appliedIds']==[] and dd['heldIds']==[target] and dd['authorityAfter']==authority;sealed.append('decision scope and authority')
delivery={'id':'RANK9-PLANARGATES5-BANISHMENT-GATE-DIRECTOR-RETURN327-DELIVERY','archive':bind(zp.read_bytes(),name),'memberCount':len(files),'payloadEntryCount':len(files)-1,'exactAllowlist':[str(f.relative_to(P)) for f in files],'members':[bind(f.read_bytes(),str(f.relative_to(P))) for f in files],'sourcePacket':read(P/'SOURCE_BINDINGS.json')['packet'],'acceptedIds':[],'appliedIds':[],'heldIds':[target],'blockerIds':['PG200-B03','PG200-B04'],'qualificationIds':decision['qualificationIds'],'authorityUnchanged':authority,'counts':counts,'sealVerification':{'status':'PASS','checkCount':len(sealed),'checks':sealed},'semanticStatus':'HOLD','nextIdentity':nextid,'nextGroup':nextgroup,'nextBlockerIds':nextblock,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'application':False,'canonicalFilesChanged':False}
dp=R/'DD_Rank9_BanishmentGate_Director_Return327_HELD_DELIVERY.json';dp.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'archive':delivery['archive'],'delivery':bind(dp.read_bytes(),dp.name),'memberCount':len(files),'sealChecks':len(sealed),'counts':counts},indent=2))
