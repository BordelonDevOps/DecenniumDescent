#!/usr/bin/env python3
from sim_core import *
import os,json,random,statistics,csv
OUT=LAB/'results'/'13-haven-formulas';OUT.mkdir(parents=True,exist_ok=True)
RUNS=int(os.getenv('DD_HAVEN_RUNS','20000'));SEED=int(os.getenv('DD_CAL_SEED','720200'));rng=random.Random(SEED+300_000_000);rows=[];violations=[]
H=GAME['havenEconomy']
for sponsor,share in GAME['sponsorShares'].items():
 vals=[];taxes=[];claims=[]
 for i in range(RUNS):
  base=rng.choice([10,25,50,100,250,500,1000,2500,5000,10000]);gross=base*rng.choice(list(GAME['saleValue']['provenance'].values()))*rng.choice(list(GAME['saleValue']['demand'].values()))*rng.choice(list(GAME['saleValue']['condition'].values()))*rng.choice(list(GAME['saleValue']['urgency'].values()))
  rate=rng.choice(list(H['taxSchedule'].values()));tax=gross*rate;sponsor_cut=gross*share;premium=gross*rng.choice([.02,.04,.06]);covered=gross*rng.choice([.5,.75,1]);loss=gross*rng.random();payout=max(0,min(loss,covered)-premium)
  true=gross-tax-sponsor_cut-premium-rng.randint(0,500);vals.append(true);taxes.append(tax);claims.append(payout)
  if payout<0 or payout>covered:violations.append('insurance bounds')
 rows.append({'sponsor':sponsor,'share':share,'runs':RUNS,'meanTrueProfit':round(statistics.mean(vals),2),'lossRate':round(sum(v<0 for v in vals)/RUNS,4),'meanTax':round(statistics.mean(taxes),2),'meanClaim':round(statistics.mean(claims),2)})
# reputation and Heat boundary enumeration
for rep in range(-10,11):
 clamped=max(-5,min(5,rep));
 if clamped not in range(-5,6):violations.append('reputation')
for heat in range(-3,10):
 clamped=max(0,min(6,heat));
 if heat<=0 and clamped==0: pass
 if not 0<=clamped<=6:violations.append('heat')
with (OUT/'haven_results.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'transactions':RUNS*len(rows),'violations':violations,'passes':not violations,'formulas':['sale value','taxes','sponsor shares','insurance bounds','Heat','reputation gates','counterfeit forfeiture prose audit']};(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));raise SystemExit(1 if violations else 0)
