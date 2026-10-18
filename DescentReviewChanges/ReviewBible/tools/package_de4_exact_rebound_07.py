"""Freeze a reviewable final integration packet without modifying any live rule."""
import json,hashlib,zipfile
from copy import deepcopy
from datetime import datetime,timezone
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())
def main():
 out=A/'de4-exact-rebound-07';archive=A/'DD_DE4_Exact_Rebound_07.zip';request=A/'DE4_EXACT_REBOUND_07_REQUEST.txt';prep=A/'DE4_EXACT_REBOUND_07_PACKET.json';independent=A/'DE4_EXACT_REBOUND_07_INDEPENDENT_CHECK.json'
 assert not any(p.exists() for p in [archive,request,prep,independent])
 ck=[]
 def check(n,v):ck.append({'check':n,'passed':bool(v)});assert v,n
 manifest=read(out/'EVIDENCE_MANIFEST.json');plan=read(out/'INTEGRATION_PLAN.json');model=read(out/'SPELLS_MODEL.json');cases=read(out/'CASEBOOK.json');source=read(R/'data/director/spell_proposals/divination_enchantment_rank4_current_07.json')
 for b in manifest['files']:
  raw=(out/b['name']).read_bytes();check('Exact candidate payload '+b['name'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
 for row in plan['changes']:
  old=out/row['preservedBefore'];new=out/row['proposedFile'];live=G/row['target'];check('Live before remains exact '+live.name,live.read_bytes()==old.read_bytes())
  if live.suffix=='.json':
   obj=read(old)
   for o in row['operations']:
    node,key=parent(obj,o['pointer'])
    if o['operation']=='replace':check('Before operation '+live.name+o['pointer'],node[key]==o['before'])
    else:check('Add only absent field '+live.name+o['pointer'],key not in node)
    node[key]=deepcopy(o['after'])
   check('Replay entire proposed JSON '+live.name,obj==read(new))
 check('Shared rules identical to corrected input',model['sharedRules']==source['sharedRules']);check('Casebook all37 exact',cases['cases']==source['currentExamples']);check('All30 original texts exact',cases['historicalOriginalTexts']==source['originalExamplesUnchanged'])
 for s,t in zip(model['spells'],source['spells']):check('Only ID discovery alias on full spell '+s['id'],{k:v for k,v in s.items() if k!='id'}==t)
 for c in cases['cases']:
  for ref in c.get('sourceRefs',[]):
   if 'pointer' in ref:
    p=G/ref['path'];proposed=out/'proposed'/ref['path'];doc=read(proposed if proposed.exists() else p);check('Current resolved case pointer '+c['id']+ref['pointer'],at(doc,ref['pointer']) is not None)
 independent.write_bytes(encoded({'id':'DE4-EXACT-REBOUND-07-INDEPENDENT-CHECK','checks':ck,'checkCount':len(ck),'failureCount':0,'status':'Independent manifest/delta replay, complete procedure/case equality and current pointer verification; no runtime execution.'}))
 awareness={'id':'PARALLEL-AUTHORING-AWARENESS-07','approvalRequested':False,'counts':{'reviewed':465,'pending':383},'next25':{'candidate':info(R/'data/director/spell_proposals/damage_control_25_current_06.json'),'preparedPacket':info(A/'DD_Damage_Control_25_Conference_06.zip'),'status':'Full semantic review UNSENT; nine explicit pending choices; refresh changed source bindings after actual DE4 adoption.'},'persistent20':{'candidate':info(R/'data/director/spell_proposals/persistent_damage_20_current_04.json'),'status':'UNSENT, UNADOPTED full20 procedures,40 current original-case vectors,7 supplements and8 adversarial compositions. All old20 procedures and40 original texts retained.','newWork':['All40 original scenarios now have explicit current source-grounded vectors.','Actual ongoing-fire arbitration, ordinary extinguishing, real Mage Undying Spellform, Burden Shared/Life Linked and no-recovery funding.','Actual Globe versus Lesser Antimagic boundaries and finite source clocks; no generic rank ceiling for Lesser Antimagic.','Real Oracle9 Spiral BoonI/Bane/Synaptic and Ranger16 Warder Beast ordinary death versus Null Disabled fixtures.','NEW pending Ice Storm mixed-defense option scoped separately from next25 Meteor Spear; new finite Inferno provenance proposal remains unadopted.'],'unresolved':'Per-source new authorship still needs its own actual joint semantic review.'},'all75DomainGatesUnchanged':True,'runtimeImplemented':False,'sourceInformationDeleted':0}
 awarenessp=A/'DE4_EXACT_07_PROGRESS_AWARENESS.json';assert not awarenessp.exists();awarenessp.write_bytes(encoded(awareness))
 message='''I preserved and independently verified your final Followup06 archive (34,683 bytes,40dee719099012a8491a96c123f487bd55ce193a31a3c76807c1eb0236cdb4a9) and actual assistant message72260b80-d940-4e87-b0a9-a4c88ffd2501. Thank you for identifying your inherited N04 adjective. Current07 applies the one complete exact replacement, preserves full Current06 and its old N04 object, and leaves all15 procedures, all shared rules and all37 scenarios otherwise unchanged except self-path rebinding.

Please review DD_DE4_Exact_Rebound_07.zip for FINAL EXACT AUTHORED INTEGRATION ACCEPTANCE. Read README.md, current/REGISTER.json, current/INTEGRATION_PLAN.json and current/EVIDENCE_MANIFEST.json. Retain settled substantive DE4 decisions and AC6 closure; this is the one-word N04 correction plus final mirror/dependency/provenance binding, not a fresh full-cohort semantic review.

All ten live targets remain unchanged. Nine reviewed semantic mirrors plus the catalog-discovery index are staged in current/proposed/, with complete original before bytes in current/before/. The model,casebook,both complete manuscripts and full frozen95 sources are supplied. Rebinding includes202 whole-catalog public feat rows,196 General Combat catalog cards, and11 governing excerpt bindings. Exact full Fate excerpt ordering now matches the governing guide (the prior proposed excerpt contained identical nonblank lines in another order); both historical and prior proposed excerpt objects are retained. Raw whole-file hashes retain original bytes, while excerpt text explicitly normalizes CRLF to LF. Mark Omen/Fate Coin retain historical designNotes and add explicit later-extension provenance. Original dependency/source records and sealedAC6 bytes are untouched.

3,070 preparation checks and an independent full operation-replay/pointer check pass. They establish authored-file consistency, not game-runtime behavior. Proposed pending labels are intentionally immutable review-stage history; a later real acceptance receipt establishes authored status, and no unseen future receipt is fabricated. The index here changes only its catalog binding; 15 membership updates, registry refresh and actual receipt registration occur only after your affirmative acceptance. Counts remain465/383 now, then480/368 only if actually accepted and applied.

Return a downloadable REVIEW.json and VERDICT.md, binding the actual input archive and all18 operative candidate files (8 root files including EVIDENCE_MANIFEST.json plus10 proposed targets) by bytes andSHA256. Explicitly disposition N04, mirror/provenance coherence, whole-card/excerpt binding and preservation. If coherent, ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_DE4_VIDEO_GAME_CANDIDATE and the10 exact staged integration copies; otherwise provide only minimal exact pointers/full replacements. Do not reserialize unchanged artifacts. No runtime, human gameplay, numerical balance, cosmology/canon, full75-domain closure or release approval.

PROGRESS_AWARENESS.json keeps you informed: next25 is ready but UNSENT; persistent20 now has all40 source-grounded original-case vectors plus7 supplements and8 adversarial cases, including actual class and suppression/transfer interfaces. Both remain pending and receive no approval in this review. I will refresh their current bindings after any real DE4 adoption and bring the next full cohort to you. The owner asks for regular actual conference and drift checks.'''
 request.write_text(message+'\n',encoding='utf-8',newline='\n')
 members={}
 for p in sorted(out.rglob('*')):
  if p.is_file():members['current/'+p.relative_to(out).as_posix()]=p.read_bytes()
 for b in read(out/'SOURCE_HASHES.json')['bindings']:
  p=G/b['path'];assert info(p)==b;members['sources/'+b['path']]=p.read_bytes()
 evidence=[request,independent,A/'DE4_EXACT_REBOUND_07_CHECK.json',A/'DE4_REVIEW_FOLLOWUP_06_FINAL_NATIVE.json',A/'DD_DE4_Review_Followup_06_Review.zip',A/'DE4_REVIEW_FOLLOWUP_06_FINAL_RECEIPT.json']+list((A/'de4-review-followup-06-review-final').iterdir())
 for p in evidence:members['evidence/'+p.name]=p.read_bytes()
 members['PROGRESS_AWARENESS.json']=awarenessp.read_bytes()
 roots=['INTEGRATION_PLAN.json','SPELLS_MODEL.json','CASEBOOK.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','SOURCE_HASHES.json','REGISTER.json','EVIDENCE_MANIFEST.json']
 targets=['current/'+n for n in roots]+['current/'+r['proposedFile'] for r in plan['changes']]
 members['README.md']=('''# DE4 exact rebound07 — narrow final review

This packet contains complete proposed files, immutable before copies, complete frozen sources and actual prior review evidence. Nothing is adopted. Read evidence/DE4_EXACT_REBOUND_07_REQUEST.txt for the narrow review request. current/REGISTER.json declares scope; INTEGRATION_PLAN.json gives exact target bindings and all JSON operations. SOURCE_HASHES.json binds the frozen before-source evidence; proposed current bindings are separate. EVIDENCE_MANIFEST.json covers all27 other current payloads.

The eight root candidate files and ten current/proposed/ targets are the18 requested exact operative acceptance files. Before copies and source files remain evidence; no claim that a frozen old catalog hash is current after later application. All original scenario text, source/access and older alternatives remain preserved. Current07 is a full immutable source; its case self-references remain resolvable. Earlier pending language is preserved as review-stage history, with live acceptance recorded separately after actual approval.

PROGRESS_AWARENESS.json is status-only, not a next-cohort review request. The complete game has75 distinct gates; do not infer runtime, human-playtest, balance, cosmology, canon or release approval.
''').encode()
 top={'id':'DD-DE4-EXACT-REBOUND-07-PACKET-MANIFEST','files':[{'name':n,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for n,v in members.items()],'requestedExactAcceptanceFiles':targets,'scope':'Every packet member except this manifest; archive hash covers manifest.'};members['MANIFEST.json']=encoded(top)
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for n,v in members.items():z.writestr(n,v)
 with zipfile.ZipFile(archive) as z:assert len(z.namelist())==len(members) and z.testzip() is None
 prep.write_bytes(encoded({'id':'DD-DE4-EXACT-REBOUND-07-PACKET','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'request':info(request),'candidatePreparation':info(A/'DE4_EXACT_REBOUND_07_PREPARATION.json'),'independentCheck':info(independent),'progressAwareness':info(awarenessp),'memberCount':len(members),'operativeAcceptanceFileCount':18,'status':'READY_UNSENT_UNADOPTED'}));print(json.dumps({'packet':info(archive),'members':len(members),'independentChecks':len(ck),'operativeFiles':len(targets)}))

if __name__=='__main__':main()
