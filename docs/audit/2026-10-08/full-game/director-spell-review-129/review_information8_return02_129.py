"""Fresh independent geometry, source-selection and exact-change review of corrected data."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,math,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');D=Path(__file__).parent;G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=D/'information8_return01_received';B=D/'information8_return02_received'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def ptr(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 return v
checks=[]
def check(k,v):assert v,k;checks.append(k)
pa=read(A/'PROCEDURES.json')['spells'];pb=read(B/'PROCEDURES.json')['spells'];closed=['arcane-eye','faction-destiny','legend-lore','prophetic-frenzy']
check('all-seven-other-procedures-exact',all(a==b for a,b in zip(pa,pb) if a['id']!='resonance-prophecy'));check('RP-only-explicit-append',pb[7]['procedure'].startswith(pa[7]['procedure']+'\n\nINFO131-RETURN02: '));check('six-shared-rules-exact',read(A/'SHARED_RULES.json')==read(B/'SHARED_RULES.json'));check('all-actor-template-source-card-and-book-data-exact',read(A/'ACTOR_TEMPLATES.json')==read(B/'ACTOR_TEMPLATES.json'))
ma=read(A/'CASEBOOK.json')['mainCases'];mb=read(B/'CASEBOOK.json')['mainCases']
for a,b in zip(ma,mb):
 if a['spellId'] in closed:check('closed-full-case-and-branches:'+a['id'],a==b)
index=read(R/'data/public/spell_playtests/authored_review_index.json');aux=read(B/'evidence/CURRENT_AUXILIARY_CARDS.json')
for sid in ['greater-dispel','antimagic-field-lesser']:
 e=next(x for x in index['entries'] if x['id']==sid);check('already-reviewed:'+sid,e['authoredStatus']=='reviewed-authored-operational-playtest');p=(R/'data/public/spell_playtests'/e['procedureFile']).resolve();v=ptr(read(p),e['wholeCardPointer']);check('exact-accepted-auxiliary:'+sid,v==aux[sid])
def corners(foot,extent):
 b=[(F(foot[i])-F(extent[i])/2,F(foot[i])+F(extent[i])/2) if i<2 else (F(foot[i]),F(foot[i])+F(extent[i])) for i in range(3)]
 return list(product(*b))
def yz_at_x(a,b,x):
 t=(F(x)-a[0])/(b[0]-a[0]);return (a[1]+t*(b[1]-a[1]),a[2]+t*(b[2]-a[2]))
def slab(a,b,lo,hi):
 t0=F(0);t1=F(1)
 for i in range(3):
  d=b[i]-a[i]
  if d==0:
   if not lo[i]<=a[i]<=hi[i]:return False
  else:
   u,v=sorted(((F(lo[i])-a[i])/d,(F(hi[i])-a[i])/d));t0=max(t0,u);t1=min(t1,v)
   if t0>t1:return False
 return True
C=corners([0,-30,0],[5,5,6]);E=corners([20,20,0],[5,5,6]);RC=corners([60,20,0],[5,5,6]);near=([5,-10,0],[12,0,8]);far=([48,-10,0],[52,16,8])
for n,(a,b) in enumerate(product(C,E)):check('near-corner-ray:'+str(n),slab(a,b,*near))
y5=[yz_at_x(a,b,5)[0] for a,b in product(C,E)];y12=[yz_at_x(a,b,12)[0] for a,b in product(C,E)];check('continuous-near-interval-bound',max(y5)<0 and min(y12)>-10)
for n,(a,b) in enumerate(product(C,RC)):check('far-corner-ray:'+str(n),slab(a,b,*far))
plane=[yz_at_x(a,b,49) for a,b in product(C,RC)];check('continuous-far-plane-bounds',min(y for y,z in plane)>-10 and max(y for y,z in plane)<16 and min(z for y,z in plane)>=0 and max(z for y,z in plane)<=8)
check('actual-caster-eye-to-field-clear',not slab(tuple(map(F,[0,-30,6])),tuple(map(F,[20,0,3])),*near));check('literal-R-fireball-source-path-clear',not slab(tuple(map(F,[60,20,3])),tuple(map(F,[40,20,3])),*far))
def pointbox(p,body):
 f=body['foot'];e=body['extent'];lo=[f[0]-e[0]/2,f[1]-e[1]/2,f[2]];hi=[f[0]+e[0]/2,f[1]+e[1]/2,f[2]+e[2]];return math.sqrt(sum(max(lo[i]-p[i],0,p[i]-hi[i])**2 for i in range(3)))
mind=next(c for c in mb if c['id']=='UN5-06-A');mind=next(c for c in mind['branches'] if 'suppressed-recipient-send' in c['id']);prop=next(c for c in mb if c['id']=='DI6-06-B');geometry=[]
for c,aid,center,am,receivers in [(mind,'X',[55,20,3],[20,20,3],list('CABDEF')),(prop,'D',[0,-65,3],[0,-30,3],['C'])]:
 cast=next(e for e in c['timeline'] if e['observations'].get('spellId')=='greater-dispel');before=cast['before'];after=cast['after'];a=before['actors'][aid]
 check('actual-GD-prepared:'+c['id'],'greater-dispel' in a['prepared'] and a['template']=='W13_GD');check('actual-GD10RP:'+c['id'],a['rp']-after['actors'][aid]['rp']==10);check('actual-GD-native-point-range:'+c['id'],math.dist([*a['body']['foot'][:2],3],center)==15);check('peripheral-AM-captured:'+c['id'],math.dist(center,am)==35<40)
 distances={k:pointbox(center,before['actors'][k]['body']) for k in receivers};check('all-receiving-bodies-excluded:'+c['id'],min(distances.values())>30);check('no-class-dispel-recharge:'+c['id'],before['actors'][aid].get('recharge')==after['actors'][aid].get('recharge'))
 geometry.append({'case':c['id'],'center':center,'AMcenterSeparation':35,'sumRadii':40,'receiverBodyDistances':distances,'onlyCapturedApplication':'AM','actualPaidRP':10})
check('prophecy-emitter-outside-purge',math.dist([0,-65,3],[20,0,3])>50)
fp=next(c for c in mb if c['id']=='DI5-06-B');e=fp['timeline'][-1];e=next(x for x in fp['timeline'] if x['id']=='DI5-06-B:30');g=e['observations']['privateGrounding'];check('seven-day-actual-window',abs(g['horizonEnd']-g['horizonStart']-604800)<1e-6);nv=e['after']['views']['C'][len(e['before']['views']['C']):];check('no-out-of-window-date-in-recipient-view',all('day8' not in str(x).replace(' ','') and '691200' not in str(x) for x in nv));check('private-day8-beyond-window',691200>g['horizonEnd'])
ready=prop['branches'][0];warning=next(e for e in ready['timeline'] if e['id'].endswith(':9'));views=warning['after']['views']['C'][len(warning['before']['views']['C']):];check('Ready-no-remote-coordinates-or-owner-marker',all('R60' not in str(v) and 'RSTART' not in str(v) and '[60, 20' not in str(v) for v in views))
counter=next(c for c in mb if c['id']=='DI6-06-A');notice=next(e for e in counter['timeline'] if e['observations'].get('applicationEventId')=='COUNTER-application');check('actual-own-nested-notice-before-resolution',notice['time']==2.115 and counter['timeline'][counter['timeline'].index(notice)+1]['time']==2.12)
result={'id':'INFORMATION8-RETURN02-INDEPENDENT-SEMANTIC-REVIEW-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checksPassed':len(checks),'dataChecksPassed':read(D/'INFORMATION8_RETURN02_INDEPENDENT_DATA_AUDIT_129.json')['checks'],'sameTemplatesRetainPrior384CardAnd663BookChecks':True,'sourceAndGeometryPassed':True,'continuousRayProof':'At fixed x, extrema over independent source/target axis boxes occur at corners of the linear-fractional coordinate ratio. All z stays in0..6. E rays at x5 below0 and x12 above-10 must intersect NEAR; every R ray at x49 lies inside FAR. Actual used eye-field and Fireball source paths are separately clear.','nearBounds':{'maxYatX5':str(max(y5)),'minYatX12':str(min(y12))},'farBoundsAtX49':{'minY':str(min(y for y,z in plane)),'maxY':str(max(y for y,z in plane))},'GreaterDispelAreaGeometry':geometry,'substantiveChangedEventsAndNewViewsRead':True,'acceptedEligibleIds':['concordant-mindlink','faction-prophecy','resonance-prophecy'],'heldId':'find-the-path','remainingFinding':'DI6-04-B/actual-crossbar-after-snapshot:12 recipient view gives missing-topology reason despite unified nondiagnostic Indeterminate contract. Private unproved-shortest qualification is retained; request exact recipient output Indeterminate.','closedFourFullProceduresAndCasesExact':True,'runtimeExecuted':False,'suppliedProgramsExecuted':False}
(D/'INFORMATION8_RETURN02_SEMANTIC_REVIEW_129.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
