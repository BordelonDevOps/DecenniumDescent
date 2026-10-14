#!/usr/bin/env python3
from sim_core import *
from pathlib import Path
import os,json,random,statistics,csv
OUT=LAB/'results'/'07-budget-autotune'; OUT.mkdir(parents=True,exist_ok=True)
TRAIN=int(os.getenv('DD_TRAIN_RUNS','40')); HOLD=int(os.getenv('DD_HOLDOUT_RUNS','100')); SEED=int(os.getenv('DD_CAL_SEED','720200'))
levels=[1,3,5,10,15,20]; sizes=[3,4,5,6]; diffs=['routine','standard','hard','severe','catastrophic']; scales=[.5,.65,.8,.9,1.0,1.1,1.25,1.4,1.6]
rows=[]; winners={}
for level in levels:
 for size in sizes:
  for diff in diffs:
   lo,hi=TARGETS[diff]; target=(lo+hi)/2; scored=[]
   for scale in scales:
    budget=round(BASE_BUDGETS[diff]*PARTY_MULT[size]*scale)
    vals=[]
    for i in range(TRAIN):
     rng=random.Random(SEED+level*1000000+size*100000+diffs.index(diff)*10000+int(scale*100)*100+i)
     foes=build_encounter(level,budget,rng); vals.append(simulate_combat(level,foes,rng,size)['success'])
    rate=sum(vals)/len(vals); score=abs(rate-target); scored.append((score,scale,budget,rate))
   scored.sort(); best=scored[0]; winners[(level,size,diff)]=best[1]
   for rank,(score,scale,budget,rate) in enumerate(scored[:3],1):
    rows.append({'phase':'training','level':level,'partySize':size,'difficulty':diff,'rank':rank,'scale':scale,'budget':budget,'runs':TRAIN,'successRate':round(rate,4),'targetLow':lo,'targetHigh':hi,'distance':round(score,4)})
# Holdout only the training winner, using disjoint seeds.
for (level,size,diff),scale in winners.items():
 lo,hi=TARGETS[diff]; budget=round(BASE_BUDGETS[diff]*PARTY_MULT[size]*scale); outcomes=[]; rounds=[]; hp=[]; downs=[]
 for i in range(HOLD):
  rng=random.Random(SEED+900_000_000+level*1000000+size*100000+diffs.index(diff)*10000+i)
  foes=build_encounter(level,budget,rng); o=simulate_combat(level,foes,rng,size); outcomes.append(o['success']); rounds.append(o['rounds']); hp.append(o['hpPct']); downs.append(o['downed'])
 rate=sum(outcomes)/HOLD; ci=ci95(sum(outcomes),HOLD)
 rows.append({'phase':'holdout','level':level,'partySize':size,'difficulty':diff,'rank':1,'scale':scale,'budget':budget,'runs':HOLD,'successRate':round(rate,4),'ciLow':round(ci[0],4),'ciHigh':round(ci[1],4),'targetLow':lo,'targetHigh':hi,'passesBand':lo<=rate<=hi,'meanRounds':round(statistics.mean(rounds),3),'meanHpPct':round(statistics.mean(hp),4),'meanDowned':round(statistics.mean(downs),3)})
with (OUT/'budget_calibration.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=sorted({k for r in rows for k in r}));w.writeheader();w.writerows(rows)
hold=[r for r in rows if r['phase']=='holdout']; summary={'trainingRunsPerCandidate':TRAIN,'holdoutRunsPerCell':HOLD,'holdoutCells':len(hold),'passingCells':sum(r['passesBand'] for r in hold),'passRate':sum(r['passesBand'] for r in hold)/len(hold),'warning':'Candidate budgets are proxy evidence until frozen class builds and dice-level fixtures corroborate them. No canon was edited.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
