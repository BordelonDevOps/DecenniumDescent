#!/usr/bin/env python3
from sim_core import *
import os,json,random,statistics,csv
OUT=LAB/'results'/'11-coupled-expedition';OUT.mkdir(parents=True,exist_ok=True)
RUNS=int(os.getenv('DD_EXPEDITION_RUNS','2000'));SEED=int(os.getenv('DD_CAL_SEED','720200'));rows=[]
policies={'cautious':(3,2,.7),'balanced':(4,3,1.0),'aggressive':(5,4,1.3)}
for level in [1,5,10,15]:
 for pname,(abort,rest_at,cargo_factor) in policies.items():
  for mapping in ['Secured','Mapped','Sketched','Unknown']:
   success=extract=wipe=0;profits=[];losses=[];watches=[]
   for i in range(RUNS):
    rng=random.Random(SEED+200_000_000+level*1_000_000+list(policies).index(pname)*100_000+['Secured','Mapped','Sketched','Unknown'].index(mapping)*10_000+i)
    pressure=0;supply=24;strain=0;progress=0;cargo=0;alive=6;watch=0;rest_debt=[None]*6
    target=8
    while watch<36 and alive>0:
     watch+=1;supply-=alive/3
     if supply<0:supply=0;strain+=1
     # Forage bounded by route Sustenance 0-4.
     sust=2
     if rng.random()<.38:supply+=rng.randint(0,sust)
     base={'Secured':2,'Mapped':2,'Sketched':1,'Unknown':0}[mapping]
     if mapping=='Unknown' and watch%3==0: base=1; supply=max(0,supply-2); strain+=1 # Forced March escape valve.
     progress+=max(0,base+(1 if rng.random()<.25 else 0))
     if rng.random()<.35:
      diff='standard' if pressure<3 else 'hard';budget=round(BASE_BUDGETS[diff]*PARTY_MULT[4]);o=simulate_combat(level,build_encounter(level,budget,rng),rng,4)
      if not o['success']: alive=max(0,alive-rng.randint(0,2));strain+=1;pressure=min(6,pressure+1)
      cargo+=max(0,rng.gauss(2.5*cargo_factor,1.1))
     if strain>=rest_at:watch+=1;strain=max(0,strain-1);pressure=max(0,pressure-1)
     if pressure>=abort or progress>=target:break
    success+=progress>=target
    if alive<=0:wipe+=1;continue
    risk=pressure+{'Secured':0,'Mapped':1,'Sketched':2,'Unknown':3}[mapping]+min(6,int(cargo//8))
    retained=cargo
    tests=max(1,{'Secured':1,'Mapped':2,'Sketched':3,'Unknown':4}[mapping])
    for _ in range(tests):
     if rng.randint(1,20)+5 < 10+risk: retained*=.85
    extract+=1;losses.append(cargo-retained);profits.append(retained*100-(24-supply)*10-(6-alive)*1000);watches.append(watch)
   rows.append({'level':level,'policy':pname,'mapping':mapping,'runs':RUNS,'objectiveRate':round(success/RUNS,4),'extractionRate':round(extract/RUNS,4),'wipeRate':round(wipe/RUNS,4),'meanNet':round(statistics.mean(profits),2) if profits else None,'meanCargoLoss':round(statistics.mean(losses),2) if losses else None,'meanWatches':round(statistics.mean(watches),2) if watches else None})
with (OUT/'coupled_expedition.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'rows':len(rows),'simulatedExpeditions':len(rows)*RUNS,'rulesRepresented':['combat attrition','Supply','Strain','Pressure','bounded Forage','Unknown-route Forced March','cargo-linked extraction']};(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
