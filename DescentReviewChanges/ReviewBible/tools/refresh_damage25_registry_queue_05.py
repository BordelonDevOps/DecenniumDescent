"""Index accepted damage25 scope and current remaining work; retain all older versions."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def digest(v):return hashlib.sha256(v.encode('utf8') if isinstance(v,str) else encoded(v)).hexdigest()

def main():
 P=R/'data/director/spell_review';oldp=P/'accepted_interface_registry_04.json';newp=P/'accepted_interface_registry_05.json';invold=P/'ordinary_spell_inventory_03.json';invnew=P/'ordinary_spell_inventory_04.json';qold=P/'remaining_work_queue_08.json';qnew=P/'remaining_work_queue_09.json';out=A/'accepted-interface-refresh-05';report=A/'DAMAGE25_REGISTRY_QUEUE_05_CHECK.json'
 assert not any(p.exists() for p in [newp,invnew,qnew,out,report]);now=datetime.now(timezone.utc).isoformat();checks=[];frozen=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def freeze(p):
  dst=out/'sources'/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());ck('Frozen source '+p.name,dst.read_bytes()==p.read_bytes());b={**info(p),'frozenCopy':dst.relative_to(G).as_posix()};frozen.append(b);return b
 receiptp=A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json';receipt=read(receiptp);modelp=G/receipt['completeEnvelope']['path'];model=read(modelp);indexp=R/'data/public/spell_playtests/authored_review_index.json';index=read(indexp);old=read(oldp);d=deepcopy(old)
 ck('Verified exact acceptance applied',info(modelp)==receipt['completeEnvelope'] and read(A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json')['failureCount']==0)
 ck('108 inherited interfaces',len(old['entries'])==108)
 for e in old['entries']:
  b=e['currentAuthoritativeSource'];ck('Inherited authority '+e['id'],digest(e['exactAuthority'])==e['authoritySha256'] and all(info(G/b['path'])[k]==b[k] for k in ['bytes','sha256']))
 source=freeze(modelp);authority=freeze(receiptp)
 for p in [G/receipt['acceptanceAuthority']['path'],oldp,invold,indexp]:freeze(p)
 def add(ident,name,pointer,used,scope):
  value=at(model,pointer);d['entries'].append({'id':ident,'name':name,'acceptanceStatus':'accepted-authored-video-game-candidate','acceptanceBasis':authority,'scope':scope,'currentAuthoritativeSource':{**source,'pointer':pointer},'exactAuthority':deepcopy(value),'authoritySha256':digest(value),'trigger':'Use only the exact accepted procedure and its eligibility checkpoints.','inputs':'Actual class/access, resource, information, geometry and lifecycle conditions in the complete model.','outputs':'Only the stated source-specific results.','lifecycle':'Original identity, clocks, control limits and cleanup remain operative.','exceptions':'Full accepted context controls; no generic cross-source permission, extra Fate presentation or runtime implementation.','knownSourceSpecificExtensions':[],'usedBy':used,'usageCoverage':'Explicit users and complete source scope only.','reusableWithinScope':True,'summaryAuthority':'Exact authority and complete source control; a registry name adds no rule.','completeContext':{'model':source,'sharedRulesPointer':'/sharedRules','referenceAliases':receipt['caseSourceReferenceAliases']},'runtimeImplementedByRegistry':False})
 for key in model['sharedRules']:add('DC25-SHARED-'+key,key,'/sharedRules/'+key.replace('~','~0').replace('/','~1'),receipt['acceptedSpellIds'],'Only the25 accepted damage/control spells and source relationships actually stated in this shared rule. No global geometry, defense or lifecycle extension.')
 for n,s in enumerate(model['spells']):add('DC25-PROCEDURE-'+s['id'],s['name'],f'/spells/{n}/procedure',[s['id']],'Only this exact source-qualified spell procedure with its accepted full shared context and class/school access.')
 add('DC25-MIXED-DEFENSE-02','Meteor Spear exact mixed-defense allocation','/mixedDefenseOperatingOption/completeProposedText',['meteor-spear'],'Meteor Spear and only its actually authorized same-packet descendants. Not Ice Storm or a global defense-stacking rule. Historical staging labels in full model are superseded only by the actual exact receipt.')
 ck('143 unique scoped interfaces',len(d['entries'])==len({e['id'] for e in d['entries']})==143)
 ck('All108 inherited interfaces unchanged',d['entries'][:108]==old['entries'])
 d.update(recordedAtUtc=now,previousRegistry=info(oldp),developmentDirection='video-game-only',newRulesAuthoredByRefresh=0)
 ids=set(receipt['acceptedSpellIds']);priorinv=read(invold);inv=deepcopy(priorinv);inv.update(recordedAtUtc=now,previousInventory=info(invold),authoredIndex=info(indexp),reviewedRecordedCount=505,pendingRecordedCount=343,reviewedIds=[e['id'] for e in index['entries'] if e['authoredStatus']=='reviewed-authored-operational-playtest'],pending=[e for e in priorinv['pending'] if e['id'] not in ids],damage25AcceptanceReceipt=info(receiptp),verifiedRemainingAfterDamage25=343,statusCaveat='Current membership and exact receipts control. Historical catalog statuses remain; no runtime selection, numerical balance or whole-game approval.')
 ck('Actual505/343 counts',index['authoredCounts']=={'reviewed':505,'pending':343} and len(inv['reviewedIds'])==505 and len(inv['pending'])==343)
 ck('All848 inventory identities retained',set(inv['reviewedIds'])|{e['id'] for e in inv['pending']}=={e['id'] for e in index['entries']})
 q=deepcopy(read(qold));priorq=deepcopy(q);resolvedgroup=next(g for g in q['groups'] if g['group']=='damage-control25');q['groups']=[g for g in q['groups'] if g['group']!='damage-control25'];resolvedrows=[r for r in q['rows'] if r['id'] in ids];q['rows']=[r for r in q['rows'] if r['id'] not in ids]
 q.setdefault('resolvedGroups',[]).append({'oldGroupUnchanged':resolvedgroup,'oldRowsUnchanged':resolvedrows,'actualApplicationReceipt':info(receiptp),'resolution':'25 exact accepted procedures applied; full history retained.'})
 pg=next(g for g in q['groups'] if g['group']=='persistent-damage20');pg['previousGroupBeforeSubmission']=deepcopy(pg);pg.update(phase='actual-gpt-exact-review-in-progress',actualSubmission=info(A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_SUBMISSION.json'),actualUserTurn='82f23f2f-dc41-4814-9d0f-ec6c331ee127',actualGptThread='6ad1acef-455c-83ea-bc33-56e4adaec9c8',exactReboundSubmitted=True)
 for row in q['rows']:
  if row['id'] in pg['identities']:row.update(currentPhase=pg['phase'],nextAction='Wait for actual exact07 final; verify the returned archive and preserve all prior versions before application.')
 q['previousSourceBindingsUnchanged']=deepcopy(q['sourceBindings']);q['sourceBindings']=[info(G/b['path']) if b['path']==indexp.relative_to(G).as_posix() else b for b in q['sourceBindings']]
 q['sourceBindings'].extend(info(p) for p in [qold,receiptp,A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json',A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_SUBMISSION.json'])
 q.update(id='REMAINING-WORK-QUEUE-09',recordedAtUtc=now,previousQueue=info(qold),ordinarySpellCounts={'total':848,'reviewed':505,'pending':343},pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),preparedOrActualReviewIdentityCount=101,limitations='Current index and actual receipts control. All earlier queue rows and source snapshots remain preserved. Pending packets receive no acceptance by indexing them. Spell counts do not measure whole-game completion.')
 ck('25 exact pending removals',len(resolvedrows)==25 and len(q['rows'])==343 and [r['id'] for r in q['rows']]==[r['id'] for r in priorq['rows'] if r['id'] not in ids])
 ck('12 groups/101 disjoint pending identities',len(q['groups'])==12 and sum(g['identityCount'] for g in q['groups'])==len({i for g in q['groups'] for i in g['identities']})==101)
 ck('Other9 full proposals and233 source/receipt items retained',q['pendingDistribution']['earlier-complete-proposal-awaiting-current-reconciliation']==9 and q['pendingDistribution']['no-complete-procedure-found-in-current-proposal-directory']==232 and q['pendingDistribution']['receipt-only-pending']==1)
 for b in q['sourceBindings']:ck('Current queue binding '+b['path'],info(G/b['path'])==b)
 newp.write_bytes(encoded(d));invnew.write_bytes(encoded(inv));qnew.write_bytes(encoded(q));(out/'SOURCE_MANIFEST.json').write_bytes(encoded({'bindings':frozen}))
 report.write_bytes(encoded({'recordedAtUtc':now,'registry':info(newp),'inventory':info(invnew),'queue':info(qnew),'checks':checks,'checkCount':len(checks),'failureCount':0,'inheritedInterfaces':108,'newlyIndexedAcceptedInterfaces':35,'totalInterfaces':143,'authoredCounts':index['authoredCounts'],'pendingGroups':12,'preparedOrSubmittedIdentities':101,'otherCompleteProposals':9,'sourceOrReceiptWork':233,'newRulesAuthoredByRefresh':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'registry':info(newp),'queue':info(qnew),'checks':len(checks),'interfaces':143,'counts':index['authoredCounts']}))

if __name__=='__main__':main()
