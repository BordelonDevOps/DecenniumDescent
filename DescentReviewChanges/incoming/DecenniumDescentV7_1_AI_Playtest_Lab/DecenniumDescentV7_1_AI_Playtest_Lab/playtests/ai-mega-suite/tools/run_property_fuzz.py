#!/usr/bin/env python3
from pathlib import Path
import json, random, os

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
ROOT=LAB.parent.parent
GAME=json.loads((ROOT/"data/public/Decennium_Descent_Gameplay_Loop_v1_1.json").read_text(encoding="utf-8"))
RUNS=int(os.getenv("DD_FUZZ_RUNS","100000"))
SEED=int(os.getenv("DD_FUZZ_SEED","71600"))
rng=random.Random(SEED)
failures=[]

for i in range(RUNS):
    extra_sources=rng.randint(0,5)
    extra_actions=min(1,extra_sources)
    reactions=min(1,rng.randint(0,4))
    actors=min(2,rng.randint(0,6))
    if extra_actions>1: failures.append(("extra_action",i))
    if reactions>1: failures.append(("reaction",i))
    if actors>2: failures.append(("actor_cap",i))

    pressure=max(0,min(6,rng.randint(-3,9)))
    supply=max(0,rng.gauss(12,8))
    strain=max(0,min(6,rng.randint(-2,8)))
    progress=max(0,rng.randint(-3,15))
    if not 0<=pressure<=6: failures.append(("pressure",i))
    if supply<0: failures.append(("supply",i))
    if not 0<=strain<=6: failures.append(("strain",i))
    if progress<0: failures.append(("progress",i))

    base=rng.uniform(0,1e7)
    factors=[rng.choice([.5,.75,1,1.1,1.25,1.5]) for _ in range(4)]
    sale=base
    for x in factors: sale*=x
    if sale<0 or sale!=sale or sale==float("inf"): failures.append(("sale",i))

    rep=max(-5,min(5,rng.randint(-20,20)))
    if not -5<=rep<=5: failures.append(("reputation",i))

out=LAB/"results"/"16-rules-fuzz-property-tests"
out.mkdir(parents=True,exist_ok=True)
summary={"runs":RUNS,"seed":SEED,"failureCount":len(failures),"failures":failures[:1000],
         "note":"This verifies encoded invariants and does not prove all prose rules are represented."}
(out/"property_fuzz_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k!="failures"},indent=2))
raise SystemExit(1 if failures else 0)
