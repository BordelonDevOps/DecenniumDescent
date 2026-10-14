#!/usr/bin/env python3
from pathlib import Path
import json, random, re, math, statistics, csv, os, hashlib

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
ROOT=LAB.parent.parent
OUT=LAB/"results"/"00-baseline-simulations"
OUT.mkdir(parents=True,exist_ok=True)

GAME=json.loads((ROOT/"data/public/Decennium_Descent_Gameplay_Loop_v1_1.json").read_text(encoding="utf-8"))
MONSTERS=json.loads((ROOT/"src/bestiary_data_full.json").read_text(encoding="utf-8"))
RUNS=int(os.getenv("DD_BASELINE_RUNS","500"))
SEED=int(os.getenv("DD_BASELINE_SEED","77100"))

DICE=re.compile(r"(?:(\d+)d(\d+))([+-]\d+)?")
ATK=re.compile(r"\+(\d+) to hit")
AVG=re.compile(r"average\s+(\d+)",re.I)

def roll_expr(expr,rng):
    m=DICE.search(expr.replace(" ",""))
    if not m:
        a=AVG.search(expr)
        return int(a.group(1)) if a else 0
    n=int(m.group(1)); sides=int(m.group(2)); mod=int(m.group(3) or 0)
    return sum(rng.randint(1,sides) for _ in range(n))+mod

def monster_profile(m):
    attacks=[]
    multi=1
    for a in m.get("actions",[]):
        name=a.get("name","")
        text=a.get("text","")
        if name.lower()=="multiattack":
            mm=re.search(r"makes\s+(\d+)\s+attacks",text,re.I)
            if mm: multi=int(mm.group(1))
        hit=ATK.search(text)
        dice=DICE.search(text.replace(" ",""))
        avg=AVG.search(text)
        if hit and (dice or avg):
            attacks.append({"name":name,"bonus":int(hit.group(1)),"text":text})
    if not attacks:
        cr=float(m.get("challengeRating") or 1)
        attacks=[{"name":"CR proxy","bonus":max(3,round(3+cr/2)),"text":f"1d8+{max(1,round(cr/2))}"}]
    return {"name":m["name"],"ac":int(m.get("armorClass") or 12),"hp":int(m.get("hitPoints") or 10),
            "cr":float(m.get("challengeRating") or 0),"multi":multi,"attacks":attacks}

def party_member(level,role):
    pb=2+(level-1)//4
    ac={"front":15,"support":14,"striker":14,"caster":13}[role]+(level//8)
    con={"front":3,"support":2,"striker":2,"caster":1}[role]
    die={"front":10,"support":8,"striker":8,"caster":6}[role]
    avg=die//2+1
    hp=die+con+(level-1)*(avg+con)
    attack=pb+3+(1 if level>=8 else 0)
    attacks=2 if level>=5 and role in ("front","striker") else 1
    dmg={"front":8.5,"support":5.5,"striker":9.5,"caster":8.0}[role]+level*0.45
    heal=(5+level*1.2) if role=="support" else 0
    return {"role":role,"ac":ac,"hp":hp,"maxhp":hp,"attack":attack,"attacks":attacks,"dmg":dmg,"heal":heal}

def d20(rng): return rng.randint(1,20)

def hit(roll,bonus,ac):
    return roll==20 or (roll!=1 and roll+bonus>=ac)

def simulate(level,monster,rng,party_size=4,max_rounds=20):
    roles=["front","support","striker","caster","front","striker"][:party_size]
    party=[party_member(level,r) for r in roles]
    foe=monster_profile(monster)
    mhp=foe["hp"]
    rounds=0; down=0; rules=[]
    while rounds<max_rounds and mhp>0 and any(p["hp"]>0 for p in party):
        rounds+=1
        # support heals the most injured living ally if below 50%
        for p in party:
            if p["hp"]<=0: continue
            if p["role"]=="support":
                candidates=[x for x in party if 0<x["hp"]<x["maxhp"]*.5]
                if candidates:
                    t=min(candidates,key=lambda x:x["hp"]/x["maxhp"])
                    t["hp"]=min(t["maxhp"],t["hp"]+max(1,round(p["heal"]+rng.randint(1,6))))
                    continue
            for _ in range(p["attacks"]):
                if hit(d20(rng),p["attack"],foe["ac"]):
                    mhp-=max(1,round(p["dmg"]+rng.uniform(-2,2)))
                    if mhp<=0: break
        if mhp<=0: break
        living=[p for p in party if p["hp"]>0]
        if not living: break
        for _ in range(foe["multi"]):
            if not living: break
            target=rng.choice(living)
            action=rng.choice(foe["attacks"])
            if hit(d20(rng),action["bonus"],target["ac"]):
                dmg=roll_expr(action["text"],rng)
                target["hp"]-=max(1,dmg)
                if target["hp"]<=0:
                    down+=1
                    living=[p for p in party if p["hp"]>0]
    won=mhp<=0
    alive=sum(1 for p in party if p["hp"]>0)
    hp_left=sum(max(0,p["hp"]) for p in party)
    hp_total=sum(p["maxhp"] for p in party)
    return {"won":won,"rounds":rounds,"downed":down,"alive":alive,"hpPct":hp_left/hp_total if hp_total else 0}

def choose_monsters(level):
    candidates=[]
    for m in MONSTERS:
        try: cr=float(m.get("challengeRating") or 0)
        except: continue
        if m.get("armorClass") and m.get("hitPoints"):
            candidates.append((abs(cr-level),m))
    candidates.sort(key=lambda x:(x[0],x[1]["name"]))
    return [m for _,m in candidates[:min(8,len(candidates))]]

rows=[]
for level in [1,3,5,10,15,20]:
    for party_size in [3,4,6]:
        for m in choose_monsters(level)[:4]:
            outcomes=[]
            for i in range(RUNS):
                rng=random.Random(SEED+level*100000+party_size*10000+i+int(float(m.get("challengeRating") or 0)*100))
                outcomes.append(simulate(level,m,rng,party_size))
            wins=sum(o["won"] for o in outcomes)/RUNS
            rows.append({
                "level":level,"partySize":party_size,"monster":m["name"],"cr":m["challengeRating"],
                "runs":RUNS,"winRate":round(wins,4),
                "meanRounds":round(statistics.mean(o["rounds"] for o in outcomes),3),
                "meanHpPct":round(statistics.mean(o["hpPct"] for o in outcomes),4),
                "meanDowned":round(statistics.mean(o["downed"] for o in outcomes),3),
            })
with (OUT/"combat_baseline.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Expedition state machine sensitivity test.
exp_rows=[]
policies={
"cautious":{"abortPressure":3,"restAtStrain":2,"cargoFactor":0.7},
"balanced":{"abortPressure":4,"restAtStrain":3,"cargoFactor":1.0},
"aggressive":{"abortPressure":5,"restAtStrain":4,"cargoFactor":1.3},
}
for policy,pp in policies.items():
  for mapping in ["Secured","Mapped","Sketched","Unknown"]:
    for sustenance in range(5):
      successes=0; extracted=0; deaths=0; profit=[]
      for i in range(RUNS*2):
        rng=random.Random(SEED+hash(policy)%10000+hash(mapping)%1000+sustenance*100+i)
        pressure=0;supply=18;strain=0;progress=0;cargo=0;alive=6;watches=0
        target=8
        while watches<30 and alive>0:
            watches+=1
            supply-=alive/3
            if supply<0: strain+=1; supply=0
            if sustenance and rng.random()<0.45:
                supply+=sustenance
            base={"Secured":2,"Mapped":2,"Sketched":1,"Unknown":0}[mapping]
            progress+=max(0,base+(1 if rng.random()<.35 else 0))
            if rng.randint(1,6)<=max(0,pressure):
                if rng.random()<.25: alive-=1
                else: strain+=1
                pressure=min(6,pressure+1)
            if rng.random()<.3:
                cargo+=max(0,rng.gauss(3*pp["cargoFactor"],1))
                pressure=min(6,pressure+(1 if cargo>15 else 0))
            if strain>=pp["restAtStrain"]:
                watches+=1; strain=max(0,strain-1); pressure=max(0,pressure-1)
            if pressure>=pp["abortPressure"] or progress>=target:
                break
        success=progress>=target
        successes+=success
        if alive<=0: deaths+=1
        # extraction
        if alive>0:
            risk=max(0,pressure+({"Secured":0,"Mapped":1,"Sketched":2,"Unknown":3}[mapping]))
            retained=cargo
            for _ in range(max(1,risk)):
                if rng.random()<risk/12:
                    retained*=.85
            extracted+=1
            profit.append(retained*100-supply*10-(6-alive)*1000)
      exp_rows.append({"policy":policy,"mapping":mapping,"sustenance":sustenance,"runs":RUNS*2,
                       "objectiveRate":round(successes/(RUNS*2),4),"extractionRate":round(extracted/(RUNS*2),4),
                       "wipeRate":round(deaths/(RUNS*2),4),"meanNetProxy":round(statistics.mean(profit),2) if profit else None})
with (OUT/"expedition_baseline.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=exp_rows[0].keys());w.writeheader();w.writerows(exp_rows)

# Economy formula stress.
econ=[]
for sponsor,share in GAME["sponsorShares"].items():
    vals=[]
    rng=random.Random(SEED+len(sponsor))
    for i in range(RUNS*10):
        base=rng.choice([100,250,500,1000,2500,5000,10000])
        prov=rng.choice(list(GAME["saleValue"]["provenance"].values()))
        demand=rng.choice(list(GAME["saleValue"]["demand"].values()))
        cond=rng.choice(list(GAME["saleValue"]["condition"].values()))
        urgency=rng.choice(list(GAME["saleValue"]["urgency"].values()))
        gross=base*prov*demand*cond*urgency
        taxes=gross*rng.choice([.02,.05,.08,.12])
        wages=rng.randint(50,500)
        replacement=rng.randint(0,1000)
        true=gross*(1-share)-taxes-wages-replacement
        vals.append(true)
    econ.append({"sponsor":sponsor,"share":share,"runs":len(vals),"meanTrueProfit":round(statistics.mean(vals),2),
                 "medianTrueProfit":round(statistics.median(vals),2),
                 "lossRate":round(sum(v<0 for v in vals)/len(vals),4)})
with (OUT/"economy_baseline.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=econ[0].keys());w.writeheader();w.writerows(econ)

summary={"runsPerCombatFixture":RUNS,"combatRows":len(rows),"expeditionRows":len(exp_rows),"economyRows":len(econ),
         "warning":"These are chassis proxies, not full class-balance evidence."}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
