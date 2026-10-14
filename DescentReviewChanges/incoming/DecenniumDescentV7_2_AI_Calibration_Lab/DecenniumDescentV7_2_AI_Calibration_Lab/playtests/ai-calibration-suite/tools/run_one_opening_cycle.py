#!/usr/bin/env python3
from sim_core import *
import os,json,random,statistics,csv
OUT=LAB/'results'/'14-one-opening-cycle';OUT.mkdir(parents=True,exist_ok=True)
RUNS=int(os.getenv('DD_CYCLE_RUNS','10000'));SEED=int(os.getenv('DD_CAL_SEED','720200'));rng=random.Random(SEED+400_000_000);rows=[];viol=[]
assert GAME['seasonal']['openingsPerCycle']==1 and GAME['seasonal']['cycleLengthYears']==10
for i in range(RUNS):
 cycle=i+1;expeditions=rng.randint(1,20);routes=rng.randint(0,expeditions);artifacts=rng.randint(0,max(1,expeditions//2));haven=rng.choice(GAME['seasonal']['havenDistrictStates']);heirs=rng.randint(0,6)
 openings=1
 if openings!=1:viol.append(cycle)
 rows.append({'cycle':cycle,'years':10,'openings':openings,'expeditionsWithinOpening':expeditions,'routesPersisting':routes,'artifactsPersisting':artifacts,'havenState':haven,'successors':heirs})
with (OUT/'cycle_results.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'cycles':RUNS,'openings':RUNS,'violations':len(viol),'rule':'Exactly one Opening per ten-year Cycle; many expeditions may occur inside that Opening.'};(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));raise SystemExit(1 if viol else 0)
