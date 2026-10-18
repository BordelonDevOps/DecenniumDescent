"""Map every pending identity to existing drafts to prevent duplicate re-authoring."""
from collections import Counter,defaultdict
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 out=R/'data/director/spell_review/remaining_spell_authoring_map_03.json';report=A/'REMAINING_SPELL_AUTHORING_MAP_CHECK_03.json';assert not out.exists() and not report.exists()
 invp=R/'data/director/spell_review/ordinary_spell_inventory_02.json';indexp=R/'data/public/spell_playtests/authored_review_index.json';inv=read(invp);idx=read(indexp);pending={s['id']:s for s in inv['pending']};entries={e['id']:e for e in idx['entries']};sources={invp,indexp};history=defaultdict(list)
 for p in sorted((R/'data/director/spell_proposals').glob('*.json')):
  if '_current_' in p.name:continue
  data=read(p)
  for j,s in enumerate(data.get('records',[])):
   sid=s.get('spellId')
   if sid in pending:
    history[sid].append({'source':info(p),'recordPointer':f'/records/{j}','procedurePointer':f'/records/{j}/procedure','procedurePresent':bool(s.get('procedure')),'procedureCharacters':len(s.get('procedure','')),'originalWorkedCaseCount':len(s.get('workedCases',[])),'status':'Earlier unadopted complete proposal; refresh its historical dependencies and preserve every original case before new authorship.'});sources.add(p)
 de4p=R/'data/director/spell_proposals/divination_enchantment_rank4_current_05.json';nextp=R/'data/director/spell_proposals/damage_control_25_current_06.json';p20p=R/'data/director/spell_review/persistent_damage_20_source_convergence_01.json';de4=read(de4p);next25=read(nextp);p20=read(p20p);sources|={de4p,nextp,p20p}
 active={}
 for p,data,key,kind in [(de4p,de4,'spellId','active-director-review-DE4-15'),(nextp,next25,'id','prepared-unsent-next25'),(p20p,p20,'id','source-converged-persistent20')]:
  for j,s in enumerate(data['spells']):
   sid=s[key];assert sid not in active;active[sid]={'state':kind,'currentSource':info(p),'pointer':f'/spells/{j}'}
 rows=[]
 for sid,s in pending.items():
  e=entries[sid];prior=history.get(sid,[])
  state=active.get(sid,{}).get('state') or ('earlier-complete-proposal-awaiting-current-reconciliation' if any(x['procedurePresent'] for x in prior) else 'receipt-only-pending' if 'receipt' in e['authoredStatus'] else 'no-complete-procedure-found-in-current-proposal-directory')
  rows.append({'id':sid,'name':s['name'],'indexStatusUnchanged':e['authoredStatus'],'minimumActualClassRank':min(a['rank'] for a in s['classAccess'].values()),'placements':s['placements'],'classAccess':s['classAccess'],'authoringState':state,'activeQueue':active.get(sid),'completeEarlierProposalRecords':prior,'riskTier':next((x['riskTier'] for x in p20['spells'] if x['id']==sid),next((x['riskTier'] for x in next25['spells'] if x['id']==sid),'unassessed-here')),'sourcePreservationRequired':True,'semanticReviewPerformedByThisIndex':False})
 counts=Counter(x['authoringState'] for x in rows);checks=[{'check':'383 exact pending unique IDs','passed':len(rows)==383 and len({s['id'] for s in rows})==383},{'check':'465 reviewed separate','passed':len(inv['reviewedIds'])==465 and not(set(pending)&set(inv['reviewedIds']))},{'check':'All848 identities accounted','passed':set(pending)|set(inv['reviewedIds'])==set(entries)},{'check':'60 nonoverlapping active/prepared/source-audited IDs','passed':len(active)==60 and set(active)<=set(pending)},{'check':'Each classified exactly once','passed':sum(counts.values())==383}]
 for row in rows:
  for x in row['completeEarlierProposalRecords']:
   p=G/x['source']['path'];s=read(p)['records'][int(x['recordPointer'].split('/')[-1])];checks.append({'check':'Exact historical identity/pointer '+row['id'],'passed':s['spellId']==row['id'] and info(p)==x['source']})
 assert all(x['passed'] for x in checks)
 d={'id':'REMAINING-SPELL-AUTHORING-MAP-03','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Machine provenance/consolidation map; no new rule or acceptance','acceptedCounts':{'reviewed':465,'pending':383,'total':848},'pendingAuthoringStateCounts':dict(counts),'pendingRankCounts':dict(sorted(Counter(x['minimumActualClassRank'] for x in rows).items())),'rows':rows,'sourceBindings':[info(p) for p in sorted(sources)],'limits':['This map searched complete records in the current proposal directory and the three explicit active queues; a no-complete-procedure result does not claim no source, audit, historical receipt or unindexed draft exists elsewhere.','Original authored procedures and current case obligations must be read before any new rewrite.','Only exact existing accepted evidence promotes a spell. A prepared/current/source-converged label is not approval.','This index performs no new semantic risk assessment beyond the actual preassigned next25/persistent20 values. DE4 and all other risks remain separately governed.'],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 out.write_bytes(encoded(d));report.write_bytes(encoded({'artifact':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'pendingStateCounts':dict(counts),'sourceCount':len(sources),'acceptedCountsChanged':False,'sourceInformationDeleted':0,'scope':'Exact identity/pointer/source and disjoint coverage accounting; not substantive procedure review.'}));print(json.dumps(read(report)|{'checks':'see report'}))

if __name__=='__main__':main()
