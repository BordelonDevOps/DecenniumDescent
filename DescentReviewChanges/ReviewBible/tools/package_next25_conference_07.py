"""Submit-ready full next25 packet bound to actual DE4 adoption and current interfaces."""
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
 root=A/'damage-control-25-conference-07';zp=A/'DD_Damage_Control_25_Conference_07.zip';req=A/'DAMAGE_CONTROL_25_CONFERENCE_07_REQUEST.txt';prep=A/'DAMAGE_CONTROL_25_CONFERENCE_07_PREPARATION.json';assert not any(p.exists() for p in [root,zp,req,prep])
 draft=R/'data/director/spell_proposals/damage_control_25_current_07.json';d=read(draft);regp=R/'data/director/spell_review/accepted_interface_registry_04.json';reg=read(regp);paths={draft};receipt=A/'DE4_EXACT_ACCEPTANCE_07_RECEIPT.json'
 for b in d['sourceBindings']:
  p=G/b['path'];assert info(p)==b,b['path'];paths.add(p)
 def bindings(x):
  if isinstance(x,dict):
   if all(k in x for k in ['path','bytes','sha256']):yield {k:x[k] for k in ['path','bytes','sha256']}
   for v in x.values():yield from bindings(v)
  elif isinstance(x,list):
   for v in x:yield from bindings(v)
 used={x['id'] for s in d['spells'] for x in s['inheritedInterfaces']}
 for e in reg['entries']:
  if e['id'] in used:
   for b in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
    p=G/b['path'];assert info(p)==b,b['path'];paths.add(p)
 oldmanifest=read(A/'damage-control-25-conference-06/MANIFEST.json')
 for b in oldmanifest['files']:
  p=G/b['path']
  if info(p)==b:paths.add(p)
 # The original compressed packet supplies all old exact bytes for historical bindings.
 paths.update(A/n for n in ['DD_Damage_Control_25_Conference_06.zip','DD_DE4_Exact_Rebound_07_Review.zip','DE4_EXACT_ACCEPTANCE_07_ACTUAL_NATIVE.json','DE4_EXACT_ACCEPTANCE_07_RECEIPT.json','DE4_EXACT_ACCEPTANCE_07_APPLICATION_CHECK.json','DE4_REGISTRY_INVENTORY_REFRESH_04_CHECK.json','PENDING_COHORTS_AFTER_DE4_07_CHECK.json'])
 paths.update([A/'de4-exact-acceptance-07/REVIEW.json',A/'de4-exact-acceptance-07/VERDICT.md',R/'tools/refresh_pending_cohorts_after_de4_07.py'])
 root.mkdir();summary=(A/'damage-control-25-conference-06/README.md').read_text(encoding='utf8')
 summary=summary.replace('conference 06','conference 07').replace('current_06.json','current_07.json').replace('Registry03','Registry04').replace('accepted465/383 count','accepted480/368 count')
 before='This packet is independent preparation while the Director completes DE4; it does not infer or preempt DE4 acceptance.'
 assert before in summary;summary=summary.replace(before,'Actual final DE4 acceptance has been recovered and applied, with1893 local application checks and249 registry/inventory checks. Exact receipt, final review, native reply and current Registry04 are included. AC6 and DE4 remain closed within their accepted scope.')
 before='The old physical-dice/two-spell Fate wording in unchanged accepted files is historical/current pre-DE4 adoption; use the separately reviewed DE4 disposition only after it actually arrives and is integrated.'
 assert before in summary;summary=summary.replace(before,'Current07 refreshes current references to actual DE4 adoption without changing any next25 procedure or scenario outcome. The current three-spell guard and five-entry disclosure whitelist apply only within their accepted sources. Old whole-file bindings in preserved earlier drafts remain historical; the full previous Conference06 ZIP supplies all of their prior exact bytes. They do not override Current07 or Registry04.')
 summary+='\n## Current preservation and awareness\n\nThe actual DE4 receipt is separate from the unchanged accepted payloads.15 identities have now entered the authored index, giving480 reviewed/368 pending (367 pending procedures plus1 cosmology receipt-only item). Current07 is978197 bytes with SHA256 2deebb6ed2334d0453cf1dccb6757442f9fe5a50f1cc46eec71cc546b8629d19. All25 procedures, source/access records and existing expected outcomes remain as Current06; only current references/status evidence changed. The file `PROGRESS_AWARENESS.json` is status-only: persistent20 and illusion14 are not part of this semantic acceptance request. Creation remains separately preserved for an economy/crafting conference. No supplied script needs execution.\n'
 (root/'README.md').write_text(summary,encoding='utf8',newline='\n')
 awareness={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualDE4AcceptanceApplied':info(receipt),'authoredCounts':{'reviewed':480,'pending':368},'persistent20':{'candidate':info(R/'data/director/spell_proposals/persistent_damage_20_current_05.json'),'status':'UNSENT UNADOPTED;20 full procedures,40 original-case vectors,7 supplements,8 adversarial cases; current references refreshed afterDE4.'},'illusionPerception':{'audit':info(R/'data/director/spell_review/illusion_perception_15_source_convergence_01.json'),'candidate':info(R/'data/director/spell_proposals/illusion_perception_14_current_04.json'),'status':'UNSENT UNADOPTED work in progress:15 source records audited;Creation kept separately for economy/crafting.14 complete procedures,28 original texts,8 current vectors,20 remaining.','issues':['Greater Phantom Steed rider Load and full-source suppression ending need scoped agreement; original170lb-body conversion and missed Burdened threshold preserved as history.','Echofield observer-known Invisible modifiers must follow Core; Reality Fracture silhouettes must not reveal unperceived bodies.','Further actual source/case work is continuing; no illusion or Creation acceptance requested here.']},'all75DomainGatesRemainDistinct':True,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 (root/'PROGRESS_AWARENESS.json').write_bytes(encoded(awareness));paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix())
 manifest={'id':'DAMAGE-CONTROL-25-CONFERENCE-07','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(draft),'files':[info(p) for p in paths],'readme':info(root/'README.md'),'progressAwareness':info(root/'PROGRESS_AWARENESS.json'),'counts':{**oldmanifest['counts'],'boundCurrentCandidateSources':len(d['sourceBindings'])},'currentAuthoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptionsInThisPacket':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 (root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json','PROGRESS_AWARENESS.json']:z.write(root/n,n)
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for b in manifest['files']:
   raw=z.read('files/'+b['path']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
 b=info(zp);message=f'''Your actual final DE4 exact acceptance (assistant08263e22-ae30-4a00-83a9-458866080ae5; review ZIP24015 bytes SHA256261b5138a639404ea5bdb07b1525f9556eac17dfd3611c6ebf4f8ccead701f0e) has been preserved, independently verified and applied. All10 exact staged targets and4 canonical payload copies were installed byte-identically after full backups. The separately authorized15-identity index update is complete:480 reviewed/368 pending.1893 application checks,249 registry/inventory checks and566 pending-cohort reference checks pass. Registry04 has108 scoped interfaces. No sealedAC6 or acceptedDE4 payload was rewritten; no runtime/balance/canon claim.

Please now conduct the full next25 damage/control source conference using attached DD_Damage_Control_25_Conference_07.zip ({b['bytes']} bytes; SHA256 {b['sha256']}). Read README.md, MANIFEST.json, then damage_control_25_current_07.json.25 identities/26 placements;18 full restored original proposals with all36 original scenarios;7 new high-rank proposals with15 supplemental casting vectors;10 other cases and3 separate mixed-defense option vectors. Every earlier alternative/history is preserved, including the entire previous packet. Current07 changes only live reference bindings and status after real DE4 adoption; all25 procedures and expected outcomes stay unchanged.

Give substantive source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for each of25 complete procedures and all9 conference decisions:Freezing Sphere actual ice/clearance/split/melt/slip behavior; Meteor Spear exact mixed-defense allocation; Mental Bomb reaction debt; Phantom Swarm finite movement; Horrid metadata alias; source-specific geometry; Chain Lightning primary/arc locus; remaining printed/new values; and Supernova Lance recipient identity after actual damage. The README names precise unresolved edges and full-source context. Return downloadable REVIEW.json, VERDICT.md and any complete exact proposed replacements keyed to real candidate pointers; preserve original scenarios and actual class/school access. Do not substitute routine header arithmetic for substantive decisions, and do not accept unseen later integration files.

Keep settled AC6/DE4 closed and inherit only their actual scope; no sixth RNG-disclosure entry or generic cross-source allowance. PROGRESS_AWARENESS.json informs you of separate persistent20 work (40 original vectors+7 supplements+8 adversarial) and new illusion/perception audit (14 complete procedures,8 current vectors/20 remaining;Creation separated for economy/crafting). Those cohorts are not submitted for acceptance yet. Continue identifying actual issues without collapsing75 domain gates or inferring runtime/gameplay/balance/cosmology/release completion. The owner asks regular conference and continued development until20% allowance remains.'''
 req.write_text(message,encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':b,'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared; not yet submitted.'}));print(json.dumps(read(prep)))
if __name__=='__main__':main()
