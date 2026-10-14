from __future__ import annotations
from pathlib import Path
import json, random, re, math, statistics, hashlib

HERE=Path(__file__).resolve(); LAB=HERE.parent.parent; ROOT=LAB.parent.parent
GAME=json.loads((ROOT/'data/public/Decennium_Descent_Gameplay_Loop_v1_2.json').read_text(encoding='utf-8'))
MONSTERS=json.loads((ROOT/'src/bestiary_data_full.json').read_text(encoding='utf-8'))
DICE=re.compile(r'(?:(\d+)d(\d+))([+-]\d+)?'); ATK=re.compile(r'([+-]\d+)\s+to hit',re.I); AVG=re.compile(r'average\s+(\d+)',re.I)

def cr_value(v):
    if isinstance(v,(int,float)): return float(v)
    s=str(v).strip()
    if '/' in s:
        a,b=s.split('/',1)
        try:return float(a)/float(b)
        except:return 0.0
    try:return float(s)
    except:return 0.0

def roll_expr(text,rng):
    clean=str(text).replace(' ','')
    m=DICE.search(clean)
    if m:
        n,sides,mod=int(m.group(1)),int(m.group(2)),int(m.group(3) or 0)
        return max(0,sum(rng.randint(1,sides) for _ in range(n))+mod)
    a=AVG.search(str(text)); return int(a.group(1)) if a else 1

def monster_profile(m):
    attacks=[]; multi=1
    for a in m.get('actions',[]):
        name=a.get('name',''); text=a.get('text','')
        if name.lower()=='multiattack':
            mm=re.search(r'makes\s+(\d+)\s+attacks',text,re.I)
            if mm: multi=max(1,int(mm.group(1)))
        h=ATK.search(text)
        if h and (DICE.search(text.replace(' ','')) or AVG.search(text)):
            attacks.append({'name':name,'bonus':int(h.group(1)),'text':text})
    cr=cr_value(m.get('challengeRating'))
    if not attacks:
        attacks=[{'name':'validated proxy','bonus':max(2,round(3+cr/2)),'text':f'1d8+{max(1,round(cr/2))}'}]
    return {'id':m.get('id'), 'name':m.get('name'), 'ac':int(m.get('armorClass') or 12),
            'hp':int(m.get('hitPoints') or max(6,8+cr*8)), 'cr':cr, 'multi':min(5,multi), 'attacks':attacks}

PROFILES=[monster_profile(m) for m in MONSTERS if m.get('name')]
REL_POINTS={int(k):v for k,v in GAME['encounterMath']['relativeThreatPoints'].items()}
BASE_BUDGETS=GAME['encounterMath']['fourCharacterBudgets']
TARGETS={k:tuple(v['partySuccessRate']) for k,v in GAME['encounterMath']['calibrationTargets'].items()}
PARTY_MULT={int(k):v for k,v in GAME['encounterMath']['partySizeMultipliers'].items()}

def party_member(level,role):
    pb=2+(level-1)//4
    ac={'front':16,'support':15,'striker':15,'caster':13}[role]+(1 if level>=9 else 0)+(1 if level>=17 else 0)
    con={'front':3,'support':2,'striker':2,'caster':1}[role]
    die={'front':10,'support':8,'striker':8,'caster':6}[role]; avg=die//2+1
    hp=die+con+(level-1)*(avg+con)
    attack=pb+3+(1 if level>=8 else 0)+(1 if level>=16 else 0)
    attacks=2 if level>=5 and role in ('front','striker') else 1
    if level>=17 and role=='striker': attacks=3
    dmg={'front':7.5,'support':5.0,'striker':8.5,'caster':7.5}[role]+level*.55
    heal=(4+level*1.0) if role=='support' else 0
    return {'role':role,'ac':ac,'hp':hp,'maxhp':hp,'attack':attack,'attacks':attacks,'dmg':dmg,'heal':heal}

def d20(rng):return rng.randint(1,20)
def hit(r,b,ac): return r==20 or (r!=1 and r+b>=ac)

def simulate_combat(level,monsters,rng,party_size=4,max_rounds=20,objective='defeat'):
    roles=['front','support','striker','caster','front','striker'][:party_size]
    party=[party_member(level,r) for r in roles]
    foes=[dict(m, hp_left=m['hp']) for m in monsters]
    rounds=0; downed=0; resource=0; objective_progress=0
    party_first=rng.random()<.55
    while rounds<max_rounds and any(f['hp_left']>0 for f in foes) and any(p['hp']>0 for p in party):
        rounds+=1
        turns=['party','foe'] if party_first else ['foe','party']
        for side in turns:
            if side=='party':
                for p in party:
                    if p['hp']<=0: continue
                    if p['role']=='support':
                        hurt=[x for x in party if 0<x['hp']<x['maxhp']*.45]
                        if hurt:
                            t=min(hurt,key=lambda x:x['hp']/x['maxhp']); t['hp']=min(t['maxhp'],t['hp']+round(p['heal']+rng.randint(1,6))); resource+=1; continue
                    live=[f for f in foes if f['hp_left']>0]
                    if not live: break
                    target=min(live,key=lambda f:f['hp_left'])
                    for _ in range(p['attacks']):
                        r=d20(rng)
                        if hit(r,p['attack'],target['ac']): target['hp_left']-=max(1,round(p['dmg']+rng.uniform(-2.5,2.5)))
                        if target['hp_left']<=0: break
                    if objective!='defeat' and rng.random()<.18: objective_progress+=1
            else:
                for foe in [f for f in foes if f['hp_left']>0]:
                    living=[p for p in party if p['hp']>0]
                    if not living: break
                    for _ in range(foe['multi']):
                        if not living: break
                        t=rng.choice(living); a=rng.choice(foe['attacks'])
                        if hit(d20(rng),a['bonus'],t['ac']):
                            t['hp']-=max(1,roll_expr(a['text'],rng))
                            if t['hp']<=0: downed+=1; living=[p for p in party if p['hp']>0]
            if not any(f['hp_left']>0 for f in foes) or not any(p['hp']>0 for p in party): break
        party_first=not party_first
    killed=not any(f['hp_left']>0 for f in foes); alive=sum(p['hp']>0 for p in party)
    hp_pct=sum(max(0,p['hp']) for p in party)/sum(p['maxhp'] for p in party)
    if objective=='defeat': success=killed
    elif objective=='protectCargo': success=(alive>0 and (killed or rounds>=6) and objective_progress>=1)
    elif objective=='escort': success=(alive>0 and objective_progress>=3)
    elif objective=='hazard': success=(alive>0 and objective_progress>=2)
    elif objective=='retreat': success=(alive>0 and rounds<=6 and objective_progress>=2)
    else: success=killed
    return {'success':success,'killed':killed,'rounds':rounds,'downed':downed,'alive':alive,'hpPct':hp_pct,'resource':resource,'objectiveProgress':objective_progress}

def nearest_monster(target_cr,rng,used=None):
    used=used or set(); candidates=[p for p in PROFILES if p['id'] not in used]
    if not candidates:candidates=PROFILES
    candidates.sort(key=lambda p:(abs(p['cr']-target_cr),rng.random()))
    return candidates[0]

def build_encounter(level,target_points,rng,max_actors=4):
    remaining=max(5,target_points); foes=[]; used=set()
    deltas=sorted(REL_POINTS,key=lambda d:REL_POINTS[d],reverse=True)
    while remaining>=5 and len(foes)<max_actors:
        viable=[d for d in deltas if REL_POINTS[d]<=remaining*1.20]
        if not viable: viable=[-4]
        weights=[max(1,REL_POINTS[d]) for d in viable]
        d=rng.choices(viable,weights=weights,k=1)[0]
        m=nearest_monster(max(0,level+d),rng,used); foes.append(m); used.add(m['id']); remaining-=REL_POINTS[d]
        if len(foes)>=1 and remaining<8: break
    return foes

def ci95(successes,n):
    if not n:return [0,0]
    p=successes/n; z=1.96; den=1+z*z/n
    center=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,center-half),min(1,center+half)]

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
