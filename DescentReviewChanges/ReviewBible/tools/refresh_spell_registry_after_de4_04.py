"""Register exact DE4 authorities and refresh current discovery without altering payloads."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
def read(p):return json.loads(p.read_bytes())
def digest(v):return hashlib.sha256(v.encode('utf8') if isinstance(v,str) else encoded(v)).hexdigest()
def main():
 P=R/'data/director/spell_review';oldp=P/'accepted_interface_registry_03.json';newp=P/'accepted_interface_registry_04.json';invold=P/'ordinary_spell_inventory_02.json';invnew=P/'ordinary_spell_inventory_03.json';out=A/'accepted-interface-refresh-04';report=A/'DE4_REGISTRY_INVENTORY_REFRESH_04_CHECK.json'
 assert not any(p.exists() for p in [newp,invnew,out,report]);old=read(oldp);d=deepcopy(old);checks=[];now=datetime.now(timezone.utc).isoformat();frozen=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def freeze(p):
  target=out/'sources'/p.relative_to(G);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen '+p.name,target.read_bytes()==p.read_bytes());b={**info(p),'frozenCopy':target.relative_to(G).as_posix()};frozen.append(b);return b
 receiptp=A/'DE4_EXACT_ACCEPTANCE_07_RECEIPT.json';receipt=read(receiptp);modelp=R/'data/public/spell_candidates/divination_enchantment_rank4_reviewed_07.json';model=read(modelp);guidep=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';guide=guidep.read_text(encoding='utf8');oldguidep=A/'source-before-de4-exact-acceptance-07'/guidep.relative_to(G)
 ck('Actual applied DE4 model',info(modelp)==receipt['completeEnvelope'] and read(A/'DE4_EXACT_ACCEPTANCE_07_APPLICATION_CHECK.json')['failureCount']==0)
 ck('78 previous interfaces',len(old['entries'])==78)
 changed=[]
 for i,e in enumerate(old['entries']):
  b=e['currentAuthoritativeSource'];p=G/b['path'];ck('Previous authority digest '+e['id'],digest(e['exactAuthority'])==e['authoritySha256'])
  if p==guidep:
   ck('Old whole-guide preserved '+e['id'],all(info(oldguidep)[k]==b[k] for k in ['bytes','sha256']));changed.append(i)
  else:ck('Unchanged inherited source '+e['id'],all(info(p)[k]==b[k] for k in ['bytes','sha256']))
 ck('Exactly four guide bindings require refresh',changed==[0,2,11,12])
 source=freeze(modelp);authority=freeze(receiptp);guidebinding=freeze(guidep);freeze(G/receipt['acceptanceAuthority']['path']);freeze(oldp);freeze(invold);freeze(oldguidep)
 d['previousChangedInterfaceRecords04']=[deepcopy(old['entries'][i]) for i in changed]
 for i in changed:
  e=d['entries'][i];heading=e['currentAuthoritativeSource']['heading'];start=guide.index(heading+'\n');nxt=re.search(r'^## ',guide[start+len(heading):],re.M);end=start+len(heading)+nxt.start() if nxt else len(guide);exact=guide[start:end]
  if i!=12:ck('Existing section authority unchanged '+e['id'],exact==e['exactAuthority'])
  e['currentAuthoritativeSource']={**guidebinding,'heading':heading,'line':guide[:start].count('\n')+1};e['exactAuthority']=exact;e['authoritySha256']=digest(exact)
  if i==12:
   e.update(name='Mark Omen, Fate Coin and scoped DE4 extension',acceptanceBasis={'historicalBasis':deepcopy(old['entries'][i]['acceptanceBasis']),'laterExactDE4Acceptance':authority},scope='The full current guide section, including only the three named spells, source-specific RNG mapping and five disclosed presentation entries accepted in DE4; no class or global disclosure extension.',usedBy=['mark-omen','fate-coin','fate-reversal'],trigger='Only each source-specific legal roll-event commitment in exactAuthority.',inputs='Actual source eligibility, component versus whole-event identity, authorized information and original-lineage guard.',outputs='Only the chosen source replacement with its actual costs and five-entry disclosure policy.',lifecycle='One shared three-spell use per original roll lineage; preserve descendant lineage and actual source entitlement.',exceptions='Actual source predicates and the complete DE4 model control; no unseen or private information grant beyond the explicit five entries.')
 def add(ident,name,pointer,used):
  exact=at(model,pointer);d['entries'].append({'id':ident,'name':name,'acceptanceStatus':'accepted-authored-video-game-candidate','acceptanceBasis':authority,'scope':'Only source relationships expressly covered by this exact DE4 authority; no global extension, automatic acquisition or cosmological settlement.','currentAuthoritativeSource':{**source,'pointer':pointer},'exactAuthority':deepcopy(exact),'authoritySha256':digest(exact),'trigger':'Use the exact source-specific activation and checkpoints.','inputs':'Actual class/access, information, resource, geometry and lifecycle predicates in the accepted complete model.','outputs':'Only the source-specific results in exactAuthority.','lifecycle':'Unchanged accepted deadlines, identity and cleanup rules.','exceptions':'Complete accepted model and named external interfaces control; previous versions remain historical.','knownSourceSpecificExtensions':[],'usedBy':used,'usageCoverage':'Explicit known users only; shared-rule scope must be read, never assumed globally.','reusableWithinScope':True,'summaryAuthority':'Exact authority and complete source control; labels create no rules.','completeContext':{'model':source,'sharedRulesPointer':'/sharedRules','referenceAliases':receipt['caseSourceReferenceAliases']},'runtimeImplementedByRegistry':False})
 for key in model['sharedRules']:
  if key=='status':continue
  add(key if key.startswith('DE4-') else 'DE4-SHARED-'+key,key,'/sharedRules/'+key.replace('~','~0').replace('/','~1'),[])
 for i,s in enumerate(model['spells']):add('DE4-PROCEDURE-'+s['id'],s['completeSourceAndAccess'].get('name',s['id']),f'/spells/{i}/procedure',[s['id']])
 ck('108 unique scoped interfaces',len(d['entries'])==len({e['id'] for e in d['entries']})==108)
 for i,e in enumerate(old['entries']):
  if i not in changed:ck('Unrelated registry entry unchanged '+e['id'],d['entries'][i]==e)
 resolved=[e for e in d['pendingExtensions'] if e['id']=='DE4-GUARD-01'];d.setdefault('resolvedPendingExtensions',[]).extend({'previous':deepcopy(e),'resolution':'Actual exact DE4 acceptance independently applied; exact scoped interfaces indexed.','receipt':authority} for e in resolved);d['pendingExtensions']=[e for e in d['pendingExtensions'] if e['id']!='DE4-GUARD-01'];d.update(recordedAtUtc=now,previousRegistry=info(oldp),developmentDirection='video-game-only',newRulesAuthoredByRefresh=0)
 indexp=R/'data/public/spell_playtests/authored_review_index.json';index=read(indexp);inv=deepcopy(read(invold));prior=deepcopy(inv);ids=set(receipt['acceptedSpellIds']);catp=R/'data/public/spell_playtests/catalog.json'
 ck('Current counts480/368',index['authoredCounts']=={'reviewed':480,'pending':368});inv.update(recordedAtUtc=now,previousInventory=info(invold),previousCatalogBinding=deepcopy(inv['catalog']),catalog=info(catp),authoredIndex=info(indexp),reviewedRecordedCount=480,pendingRecordedCount=368,reviewedIds=[e['id'] for e in index['entries'] if e['authoredStatus']=='reviewed-authored-operational-playtest'],pending=[e for e in inv['pending'] if e['id'] not in ids],de4ExactReceiptState='Exact acceptance verified and locally applied; receipt/index control.',de4AcceptanceReceipt=info(receiptp),verifiedRemainingAfterDE4=368,statusCaveat='Current authored index controls counts; catalog status remains source history. No runtime selection, gameplay or numerical balance approval.')
 ck('15 pending removals only',len(inv['pending'])==368 and inv['pending']==[x for x in prior['pending'] if x['id'] not in ids]);ck('480 unique reviewed IDs',len(inv['reviewedIds'])==len(set(inv['reviewedIds']))==480);ck('All848 identities retained',set(inv['reviewedIds'])|{e['id'] for e in inv['pending']}=={e['id'] for e in index['entries']});ck('Current catalog binding',index['sourceCatalogSha256']==inv['catalog']['sha256'])
 newp.write_bytes(encoded(d));invnew.write_bytes(encoded(inv));(out/'SOURCE_MANIFEST.json').write_bytes(encoded({'bindings':frozen}));report.write_bytes(encoded({'recordedAtUtc':now,'registry':info(newp),'inventory':info(invnew),'checks':checks,'checkCount':len(checks),'failureCount':0,'inheritedInterfaces':78,'wholeFileBindingsRefreshed':4,'existingAuthoritiesChanged':1,'newlyIndexedAcceptedInterfaces':30,'totalInterfaces':108,'authoredCounts':index['authoredCounts'],'newRulesAuthoredByRefresh':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'registry':info(newp),'inventory':info(invnew),'checks':len(checks),'interfaces':108,'counts':index['authoredCounts']}))
if __name__=='__main__':main()
