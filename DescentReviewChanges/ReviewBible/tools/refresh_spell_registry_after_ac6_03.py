"""Index exact accepted AC6 authorities without changing or broadening rules."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def main():
 P=R/'data/director/spell_review';oldp=P/'accepted_interface_registry_02.json';newp=P/'accepted_interface_registry_03.json';invold=P/'ordinary_spell_inventory_01.json';invnew=P/'ordinary_spell_inventory_02.json';out=A/'accepted-interface-refresh-03';report=A/'AC6_REGISTRY_INVENTORY_REFRESH_03_CHECK.json'
 assert not any(p.exists() for p in [newp,invnew,out,report])
 old=read(oldp);d=deepcopy(old);checks=[];now=datetime.now(timezone.utc).isoformat()
 def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
 ck('49 inherited exact interfaces',len(old['entries'])==49)
 for e in old['entries']:
  b=e['currentAuthoritativeSource'];ck('Inherited source unchanged '+e['id'],all(info(G/b['path'])[k]==b[k] for k in ['bytes','sha256']))
  raw=e['exactAuthority'].encode('utf8') if isinstance(e['exactAuthority'],str) else encoded(e['exactAuthority'])
  ck('Inherited authority digest '+e['id'],hashlib.sha256(raw).hexdigest()==e['authoritySha256'])
 modelp=R/'data/public/spell_candidates/abjuration_conjuration_rank6_reviewed_06.json';receiptp=A/'AC6_EXACT_ACCEPTANCE_06_RECEIPT.json';receipt=read(receiptp);model=read(modelp)
 ck('Accepted complete model',info(modelp)==receipt['completeEnvelope'])
 frozen=[]
 def freeze(p):
  target=out/'sources'/p.relative_to(G);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen '+p.name,target.read_bytes()==p.read_bytes());b={**info(p),'frozenCopy':target.relative_to(G).as_posix()};frozen.append(b);return b
 source=freeze(modelp);authority=freeze(receiptp);freeze(G/receipt['acceptanceAuthority']['path']);freeze(oldp);freeze(invold)
 def add(ident,name,pointer,used):
  exact=at(model,pointer);raw=exact.encode('utf8') if isinstance(exact,str) else encoded(exact)
  d['entries'].append({'id':ident,'name':name,'acceptanceStatus':'accepted-authored-video-game-candidate','acceptanceBasis':authority,'scope':'Only the AC6 source relationships expressly covered by exactAuthority; no automatic extension to unrelated spells, profiles, global rules or cosmology.','currentAuthoritativeSource':{**source,'pointer':pointer},'exactAuthority':deepcopy(exact),'authoritySha256':hashlib.sha256(raw).hexdigest(),'trigger':'Use the exact source-specific activation and checkpoints in exactAuthority.','inputs':'Use the actual class/access, state, geometry, resource and lifecycle predicates in the complete accepted model.','outputs':'Only the source-specific results in exactAuthority.','lifecycle':'Use the unchanged accepted source deadlines, identity and cleanup rules.','exceptions':'The complete accepted model and its named external interfaces control; archived previous versions do not become operative.','knownSourceSpecificExtensions':[],'usedBy':used,'usageCoverage':'Explicit named procedure user where applicable; shared-rule users must be established from exact scope, not assumed for the entire cohort.','reusableWithinScope':True,'summaryAuthority':'Exact authority and complete source control; registry labels create no rules.','completeContext':{'model':source,'sharedRulesPointer':'/sharedRules','profilesPointer':'/profiles','referenceAliases':receipt['caseSourceReferenceAliases']},'runtimeImplementedByRegistry':False})
 for key,value in model['sharedRules'].items():
  pointer='/sharedRules/'+key.replace('~','~0').replace('/','~1')
  if 'PreviousCurrentVersion' in key:
   d['inactiveHistoricalInterfaces'].append({'id':key,'source':source,'pointer':pointer,'status':'Preserved historical version only; corresponding current unsuffixed AC6 rule controls.'});continue
  add(key,key,pointer,[])
 for i,spell in enumerate(model['spells']):add('AC6-PROCEDURE-'+spell['id'],spell['completeSourceAndAccess'].get('name',spell['id']),f'/spells/{i}/procedure',[spell['id']])
 ck('78 unique accepted interfaces',len(d['entries'])==len({e['id'] for e in d['entries']})==78)
 ck('All49 previous entries unchanged',d['entries'][:49]==old['entries'])
 d['resolvedPendingExtensions']=[{'previous':deepcopy(e),'resolution':'Exact Current06 acceptance independently applied; scoped interfaces indexed here.','receipt':authority} for e in d['pendingExtensions'] if e['id']=='AC6']
 d['pendingExtensions']=[e for e in d['pendingExtensions'] if e['id']!='AC6']
 d.update(recordedAtUtc=now,previousRegistry=info(oldp),developmentDirection='video-game-only',newRulesAuthoredByRefresh=0)
 indexp=R/'data/public/spell_playtests/authored_review_index.json';index=read(indexp);inv=deepcopy(read(invold));prior=deepcopy(inv);ids=set(receipt['acceptedSpellIds'])
 ck('Current authoritative counts',index['authoredCounts']=={'reviewed':465,'pending':383})
 inv.update(recordedAtUtc=now,previousInventory=info(invold),authoredIndex=info(indexp),reviewedRecordedCount=465,pendingRecordedCount=383,reviewedIds=[e['id'] for e in index['entries'] if e['authoredStatus']=='reviewed-authored-operational-playtest'],pending=[e for e in inv['pending'] if e['id'] not in ids],ac6ExactReceiptState='Exact acceptance recovered, verified and locally applied; current receipt/index control.',ac6AcceptanceReceipt=info(receiptp),verifiedRemainingAfterAC6=383,statusCaveat='Counts come from the current authored index. Historical source catalog statuses are not silently rewritten. Authored acceptance does not enable runtime or prove gameplay/balance.')
 inv.pop('conditionalRemainingAfterVerifiedAC6',None)
 ck('14 pending records removed only after application',len(inv['pending'])==383 and inv['pending']==[x for x in prior['pending'] if x['id'] not in ids])
 ck('465 unique reviewed records',len(inv['reviewedIds'])==len(set(inv['reviewedIds']))==465)
 ck('848 original identities retained',set(inv['reviewedIds'])|{x['id'] for x in inv['pending']}=={x['id'] for x in index['entries']} and len(index['entries'])==848)
 ck('Original catalog binding retained',inv['catalog']==prior['catalog'] and all(info(G/inv['catalog']['path'])[k]==inv['catalog'][k] for k in ['bytes','sha256']))
 newp.write_bytes(encoded(d));invnew.write_bytes(encoded(inv));(out/'SOURCE_MANIFEST.json').write_bytes(encoded({'bindings':frozen}))
 report.write_bytes(encoded({'id':'AC6-REGISTRY-INVENTORY-REFRESH-03','recordedAtUtc':now,'registry':info(newp),'inventory':info(invnew),'previousRegistry':info(oldp),'previousInventory':info(invold),'checks':checks,'checkCount':len(checks),'failureCount':0,'inheritedInterfaces':49,'newlyIndexedAcceptedInterfaces':29,'totalInterfaces':78,'authoredCounts':index['authoredCounts'],'newRuleAdoptionsByRefresh':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
 print(json.dumps({'registry':info(newp),'inventory':info(invnew),'checks':len(checks),'failures':0,'interfaces':78,'counts':index['authoredCounts']}))
if __name__=='__main__':main()
