"""Bounded exact-CR2/Undead source search; no repaired data or invented rating."""
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 out=A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json';root=A/'command-undeath-target-source-search-01'
 assert not out.exists() and not root.exists()
 paths=['bestiary_data.json','src/bestiary_data.json','src/bestiary_data_full.json','DescentReviewChanges/ReviewBible/bestiary_data.json','DescentReviewChanges/ReviewBible/src/bestiary_data.json','DescentReviewChanges/ReviewBible/src/bestiary_data_full.json','DescentReviewChanges/incoming/DecenniumDescentv7/playtest_workspace/src/bestiary_data_full.json','DescentReviewChanges/incoming/DecenniumDescentV7_2_AI_Calibration_Lab/DecenniumDescentV7_2_AI_Calibration_Lab/src/bestiary_data_full.json','DescentReviewChanges/ReviewBible/data/director/bestiary_source_candidate_internal.json','archive/main-pre-v6-cutover-2026-08-05/src/bestiary_data_full.json','src/data/legacy/bestiary_data_full.truncated-262144.pre-v6-cutover.json']
 results=[];bindings=[]
 for rel in paths:
  p=G/rel;raw=p.read_bytes();b=info(p);dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert dst.read_bytes()==raw
  bindings.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
  try:d=json.loads(raw)
  except json.JSONDecodeError as e:
   results.append({'source':b,'parsed':False,'parseError':str(e),'interpretation':'Invalid/truncated historical JSON retained byte-identically. No incomplete record is promoted or silently repaired.'});continue
  seq=d if isinstance(d,list) else d['records'];prefix='' if isinstance(d,list) else '/records';selected=[];matches=[]
  for n,r in enumerate(seq):
   f=(r.get('statBlock') or {}).get('printedCoreFields',{}) if 'statBlock' in r else r
   typ=str(f.get('type','')).casefold();cr=str(f.get('challengeRating',''))
   if typ=='undead' or cr=='2':selected.append({'pointer':prefix+'/'+str(n),'name':r.get('name',r.get('id')),'printedType':f.get('type'),'printedCR':f.get('challengeRating'),'sourceReviewStatus':r.get('reviewStatus','No current operative acceptance established by this scan'),'exactRecordUnchanged':r})
   if typ=='undead' and cr=='2':matches.append(prefix+'/'+str(n))
  results.append({'source':b,'parsed':True,'recordsInspected':len(seq),'selectedUndeadOrCR2Records':selected,'exactCR2UndeadPointers':matches,'interpretation':'Exact printed type and challengeRating field comparison only. Historical imports/placeholders remain history, not independently authoritative operative profiles.'})
 assert sum(bool(r.get('exactCR2UndeadPointers')) for r in results)==0
 candidate=R/'data/director/spell_proposals/companion_life_10_current_04.json';d=json.loads(candidate.read_bytes());i=next(n for n,r in enumerate(d['records']) if r['spellId']=='command-undeath')
 out.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'BOUNDED_SOURCE_SEARCH_NO_ELIGIBLE_EXACT_CR2_UNDEAD_FOUND','searchPredicate':'Printed type equals Undead (case-insensitive), and printed challengeRating string equals2. Not CR<=2; do not derive rating from HP/name/level.','currentPendingProcedure':{'source':info(candidate),'pointer':f'/records/{i}','sourceSummary':d['records'][i]['completeSourceAndAccess']['source']['original']['description'],'qualification':'Actual current semantic conference under review; no acceptance implied.'},'sourceCount':len(paths),'validJsonSourceCount':sum(r['parsed'] for r in results),'invalidHistoricalJsonCount':sum(not r['parsed'] for r in results),'uniqueSourceByteHashes':len({b['sha256'] for b in bindings}),'results':results,'frozenSources':bindings,'limitations':['Bounded search of these eleven JSON sources, not proof of absence throughout every manuscript/workbook/archive.','No CR0,CR1 orCR3 body substitutes for the chosen exactCR2 admission.','No unrated Create Undead profile receives a rating, and no external monster block is imported.','The two preserved positive Command Undeath cases retain their whole-case source hold. A complete actual native NPC profile/rating review is separate work.','Invalid historical JSON is retained; this search makes no repairs or deletion.'],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0}))
 print(json.dumps({'report':info(out),'sources':len(paths),'valid':sum(r['parsed'] for r in results),'invalidHistorical':sum(not r['parsed'] for r in results),'exactCR2Undead':0}))

if __name__=='__main__':main()
