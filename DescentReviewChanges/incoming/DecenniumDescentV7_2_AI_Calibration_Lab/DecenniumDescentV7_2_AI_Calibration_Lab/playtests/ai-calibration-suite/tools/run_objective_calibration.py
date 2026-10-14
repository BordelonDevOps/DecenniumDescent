#!/usr/bin/env python3
from sim_core import *
import os,json,random,statistics,csv
OUT=LAB/'results'/'08-objective-calibration';OUT.mkdir(parents=True,exist_ok=True)
RUNS=int(os.getenv('DD_OBJECTIVE_RUNS','200'));SEED=int(os.getenv('DD_CAL_SEED','720200')); rows=[]
for level in [1,5,10,15,20]:
 for size in [3,4,5,6]:
  for obj in ['defeat','protectCargo','escort','hazard','retreat']:
   for diff in ['standard','hard','severe']:
    budget=round(BASE_BUDGETS[diff]*PARTY_MULT[size]); vals=[]; rounds=[]; prog=[]
    for i in range(RUNS):
     rng=random.Random(SEED+100_000_000+level*1_000_000+size*100_000+['defeat','protectCargo','escort','hazard','retreat'].index(obj)*10_000+['standard','hard','severe'].index(diff)*1000+i)
     o=simulate_combat(level,build_encounter(level,budget,rng),rng,size,objective=obj);vals.append(o['success']);rounds.append(o['rounds']);prog.append(o['objectiveProgress'])
    rate=sum(vals)/RUNS;ci=ci95(sum(vals),RUNS)
    rows.append({'level':level,'partySize':size,'objective':obj,'listedDifficulty':diff,'budget':budget,'runs':RUNS,'successRate':round(rate,4),'ciLow':round(ci[0],4),'ciHigh':round(ci[1],4),'meanRounds':round(statistics.mean(rounds),2),'meanObjectiveProgress':round(statistics.mean(prog),2),'doubleCounted':False})
with (OUT/'objective_results.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'rows':len(rows),'runs':len(rows)*RUNS,'rule':'Each objective adjustment was represented once; kill win rate was not substituted for objective success.'};(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
