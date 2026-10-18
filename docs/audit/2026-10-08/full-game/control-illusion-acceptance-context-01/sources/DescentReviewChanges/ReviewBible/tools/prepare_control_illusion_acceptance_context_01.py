"""Bind unchanged pending packets to the current45 accepted spell additions."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 root=A/'control-illusion-acceptance-context-01';out=A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01.json';check=A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01_CHECK.json';archive=A/'DD_Control_Illusion_Current_Acceptance_Context_01.zip';prep=A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01_PREPARATION.json'
 assert not any(p.exists() for p in [root,out,check,archive,prep]);checks=[];sources={}
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 ip=R/'data/public/spell_playtests/authored_review_index.json';index=read(ip);rp=R/'data/director/spell_review/accepted_interface_registry_06.json';reg=read(rp);oldrp=rp.with_name('accepted_interface_registry_04.json');oldreg=read(oldrp)
 ck('Current525/323',index['authoredCounts']=={'reviewed':525,'pending':323});ck('108 previous interfaces unchanged',len(oldreg['entries'])==108 and reg['entries'][:108]==oldreg['entries']);ck('173 current interfaces',len(reg['entries'])==173)
 for p in [ip,rp,oldrp,Path(__file__),R/'data/director/spell_review/ordinary_spell_inventory_05.json',R/'data/director/spell_review/remaining_work_queue_11.json',R/'docs/DEVELOPMENT_DIRECTION.md',R/'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md',A/'ACTIVE_AUTHORING_CHECKPOINT_PERSISTENT20_APPLIED_COMPANION_ACTIVE_16.json',G/'docs/audit/2026-10-18/github-snapshot-damage25/PUSH_RECEIPT.json']:bind(p)
 receipt_paths=[A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json',A/'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json'];accepted=set();receipts=[]
 for p in receipt_paths:
  d=read(p);bind(p);accepted.update(d['acceptedSpellIds']);receipts.append({'source':info(p),'completeReceipt':deepcopy(d)})
  for key in ['actualNativeFinal','actualReturnReceipt','acceptanceArchive']:
   if key in d and isinstance(d[key],dict) and 'path' in d[key]:bind(G/d[key]['path'])
 for stem,version in [('damage_control_25','10'),('persistent_damage_20','07')]:
  for p in [R/f'data/public/spell_candidates/{stem}_reviewed_{version}.json',R/f'data/playtest/spell_candidates/{stem}_cases_{version}.json',R/f'docs/spells/candidates/{stem.upper()}_REVIEWED_{version}.md',R/f'docs/director-only/spells/{stem.upper()}_REVIEWED_{version}.md']:bind(p)
 for f in ['DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json','PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json','DAMAGE25_REGISTRY_QUEUE_05_CHECK.json','PERSISTENT20_REGISTRY_QUEUE_06_CHECK.json']:bind(A/f)
 ck('45 disjoint accepted additions',len(accepted)==45)
 packets=[]
 for group,dirname,zipname,candidate,prefix in [('Control15','control-15-conference-12','DD_Control_15_Conference_12.zip','control_15_current_12.json','sources/'),('Illusion14','illusion-perception-14-conference-12','DD_Illusion_Perception_14_Conference_12.zip','illusion_perception_14_current_12.json','files/')]:
  mp=A/dirname/'MANIFEST.json';m=read(mp);zp=A/zipname;cp=R/'data/director/spell_proposals'/candidate;c=read(cp);bind(mp);bind(cp)
  ck('Candidate exact '+group,info(cp)==m['candidate']);drifts=[]
  with zipfile.ZipFile(zp) as z:
   ck('Archive CRC '+group,z.testzip() is None)
   for b in m['files']:
    data=z.read(prefix+b['path']);ck('Frozen member '+group+' '+b['path'],len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256'])
    actual=info(G/b['path'])
    if actual!=b:drifts.append({'originalFrozenBinding':b,'currentBinding':actual,'classification':'Current membership advances only' if b['path']==ip.relative_to(G).as_posix() else 'Current navigation/progress only'})
   oldidx=json.loads(z.read(prefix+ip.relative_to(G).as_posix()))
  expected={ip.relative_to(G).as_posix()}
  if group=='Illusion14':expected.add((R/'docs/DEVELOPMENT_DIRECTION.md').relative_to(G).as_posix())
  ck('Only membership/navigation drift '+group,{d['originalFrozenBinding']['path'] for d in drifts}==expected)
  ck('Historical480/368 preserved '+group,oldidx['authoredCounts']=={'reviewed':480,'pending':368})
  before={e['id']:e for e in oldidx['entries']};after={e['id']:e for e in index['entries']};changed={i for i in before if before[i]!=after[i]}
  ck('All848 identities/order preserved '+group,[e['id'] for e in oldidx['entries']]==[e['id'] for e in index['entries']] and len(before)==848)
  ck('Exactly45 accepted entries changed '+group,changed==accepted)
  for s in c['spells']:ck('Pending complete source card unchanged '+s['id'],before[s['id']]==after[s['id']] and after[s['id']]['authoredStatus']=='pending-authored-procedure')
  packets.append({'group':group,'archive':info(zp),'manifest':info(mp),'candidate':info(cp),'currentSourceDrifts':drifts,'unmodifiedSourceFileCount':len(m['files'])-len(drifts),'fullSpellIdentities':[s['id'] for s in c['spells']],'currentCounts':deepcopy(index['authoredCounts']),'originalCountsPreserved':deepcopy(oldidx['authoredCounts']),'originalCases':len(c['originalExamplesUnchanged']),'currentMainCases':len(c['currentExamples']),'changedIndexEntries':[{'id':i,'old':before[i],'new':after[i]} for i in sorted(changed)],'ruleSemanticsChangedByThisContext':False})
 context={'id':'CONTROL-ILLUSION-CURRENT-ACCEPTANCE-CONTEXT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT_CONTEXT_ONLY','developmentDirection':'video-game-only','packets':packets,'currentIndex':info(ip),'currentRegistry':info(rp),'registryPrefixCheck':'All108 registry04 entries remain byte-equivalent structured records within registry06;65 additions do not rewrite them.','acceptedApplications':receipts,'currentCounts':{'reviewed':525,'pending':323,'standalone':249,'scopedInterfaces':173},'reviewRouting':'Review the separately attached original full Current12 packet. Its sources and procedures remain exact; this context supersedes only obsolete current-count/navigation claims. Control CTRL15-LIMITS480/368 and old archive status are historical counts. Do not infer adoption of any pending procedure, including cross-cohort True Seeing/Mental Prison. New45 accepted procedures remain within exact separate scopes; all prior comparisons are unchanged.','preservation':'No old packet/case/question/hash was edited. Complete old/new changed membership records are present. Both original archives must be provided separately when their actual conference occurs; this context alone is not their full submission.','sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Live source stable '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 out.write_bytes(encoded(context));check.write_bytes(encoded({'context':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceCount':len(sources),'validationScope':'Exact archive and current-source reconciliation; not new semantic acceptance or runtime tests.'}));(root/'MANIFEST.json').write_bytes(encoded({'context':info(out),'check':info(check),'sources':frozen}))
 (root/'README.md').write_text('# Current acceptance context for Control15 and Illusion14\n\nThis supplement accompanies the separately attached full Current12 packet. It preserves both original packets unchanged and accounts for the only source drift:525/323 membership and current progress navigation. All108 old registry interfaces remain unchanged within173 current interfaces. The45 added accepted entries are exactly damage/control25 and persistent20, with full canonical chapters/models/cases and receipts included. All29 pending identities remain pending. Do not treat this supplement as a full submission of either underlying packet.\n',encoding='utf8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(out,'CURRENT_CONTEXT.json');z.write(check,'PREFLIGHT.json');z.write(root/'README.md','README.md');z.write(root/'MANIFEST.json','MANIFEST.json')
  for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and z.read('CURRENT_CONTEXT.json')==out.read_bytes()
  for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
 prep.write_bytes(encoded({'archive':info(archive),'context':info(out),'check':info(check),'manifest':info(root/'MANIFEST.json'),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'status':'Prepared UNSENT; context accompanies separately supplied original full packet.'}));print(json.dumps({'archive':info(archive),'context':info(out),'checks':len(checks),'sources':len(sources),'failures':0}))

if __name__=='__main__':main()
