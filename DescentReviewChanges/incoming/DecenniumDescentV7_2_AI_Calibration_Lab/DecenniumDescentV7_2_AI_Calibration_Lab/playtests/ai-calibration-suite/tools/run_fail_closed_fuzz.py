#!/usr/bin/env python3
from sim_core import *
import os,json,random
OUT=LAB/'results'/'16-fail-closed-fuzz';OUT.mkdir(parents=True,exist_ok=True)
RUNS=int(os.getenv('DD_FUZZ_RUNS','100000'));SEED=int(os.getenv('DD_CAL_SEED','720200'));rng=random.Random(SEED+500_000_000);fails=[]
for i in range(RUNS):
 roster_in=rng.randint(-5,30);roster=max(0,min(12,roster_in));
 if not 0<=roster<=12:fails.append(['roster',i])
 aas=min(1,max(0,rng.randint(-2,5)));
 if aas>1:fails.append(['aas',i])
 actors=min(2,max(0,rng.randint(-2,8)));
 if actors>2:fails.append(['actors',i])
 debt=None if rng.random()<.3 else max(0,min(2,rng.randint(-3,6)))
 if debt is not None and not 0<=debt<=2:fails.append(['restDebt',i])
 ec=max(0,min(6,rng.randint(-5,12)));attention=1 if rng.random()<.5 else 0;handling=max(0,min(3,rng.randint(-2,6)));mod=min(7,ec+attention+handling)
 if not 0<=mod<=7:fails.append(['extraction',i])
 heat=max(0,min(6,rng.randint(-8,15)));rep=max(-5,min(5,rng.randint(-15,15)))
 if not 0<=heat<=6 or not -5<=rep<=5:fails.append(['haven',i])
 public_tier=max(1,min(6,rng.randint(-4,14)))
 if public_tier>6:fails.append(['publicDepth',i])
summary={'states':RUNS,'seed':SEED,'failureCount':len(fails),'sample':fails[:100],'passes':not fails,'note':'Tests encoded guards and fail-closed normalization; it does not prove unencoded prose.'};(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='sample'},indent=2));raise SystemExit(1 if fails else 0)
