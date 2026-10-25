"""Fresh local case-only corrections implementing already selected director procedures."""
from pathlib import Path
import json,copy,hashlib,shutil,math
D=Path(__file__).parent;S=D/'time5-return01';T=D/'time5-corrected-127'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def data(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def ptr(x,p):
 for k in p.strip('/').split('/'):x=x[int(k)] if isinstance(x,list) else x[k]
 return x
assert not T.exists();shutil.copytree(S,T)
old=read(S/'CASEBOOK.json');cb=copy.deepcopy(old)
ts=cb['cases'][4];assert ts['id']=='TU4-08-A'
timeline=ts['timeline'];draw=timeline.pop(12);old_draw_id=draw['id']
assert draw['time']==24.005 and draw['label'].startswith('Actual normal-turn')
book=copy.deepcopy(draw['after']['actors']['C']['gear']['book'])
draw['id']='TU4-08-A:127-book-before-departure';draw['time']=12.3
draw['label']='Actual original-turn free interaction opens the real book before departure'
draw['before']=copy.deepcopy(timeline[1]['after']);draw['after']=copy.deepcopy(draw['before']);draw['after']['time']=12.3
draw['after']['actors']['C']['gear']['book']=copy.deepcopy(book);draw['after']['actors']['C']['ordinaryInteractionUsed']=True
draw['observations']={'oneOriginalTurnInteractionSpent':True,'actualFreeRightHandNowHoldsBook':True,'returnBonusNotYetExists':True,'noSpellOrExtraAction':True,'sameBookCarriedThroughDepartureAndReturn':True}
timeline.insert(2,draw)
for e in timeline[3:]:
 for sn in ['before','after']:
  st=e[sn];st['actors']['C']['gear']['book']=copy.deepcopy(book)
  # Original turn's interaction is spent; the real return START refreshes its own ordinary allowance.
  returned=st['actors']['C']['regularStart']>=24
  st['actors']['C']['ordinaryInteractionUsed']=not returned
timeline[3]['before']['time']=12.3
sigil=next(e for e in timeline if e['time']==24.01);sigil['before']['time']=24.0
for e in timeline:
 for sn in ['before','after']:
  st=e[sn];events=st['consumedEvents'];events[:]=[x for x in events if x!=old_draw_id]
  if st['time']>=12.3 and draw['id'] not in events:events.insert(2,draw['id'])
ts['finalState']=copy.deepcopy(timeline[-1]['after'])
ts['syntheticPremises'].append('LOCAL CASE CORRECTION127: after paid Time Skip12.1 and arming12.2, the actual free right hand draws/opens the same book using the original turn interaction12.3. It stays held through departure18/return24. No voluntary interaction intervenes between mandatory return START and immediate Sigil Rewrite24.01. Return turn ordinary interaction is unused. No spell procedure, paid cost or final HP/RP/cadence changed.')
changed_vectors={}
def replace_fields(x,oldpoint,newpoint,keys):
 count=0
 if isinstance(x,dict):
  for k,v in x.items():
   if k in keys and v==oldpoint:x[k]=copy.deepcopy(newpoint);count+=1
   else:count+=replace_fields(v,oldpoint,newpoint,keys)
 elif isinstance(x,list):
  for v in x:count+=replace_fields(v,oldpoint,newpoint,keys)
 return count
az=cb['cases'][0]['branches'][1];assert az['id']=='TC124-AZ-ACTUAL-ANTIMAGIC'
changed_vectors['AZ-ANTIMAGIC']=replace_fields(az,[20,0,3],[20,-3,3],{'target','center'})
assert changed_vectors['AZ-ANTIMAGIC']==104
az['syntheticPremises'].append('LOCAL CASE CORRECTION127: actual Lesser Antimagic point[20,-3,3] is open air before T body y=-2.5, seven feet from H source[20,-10,3]. Radius10 still intersects T at y0 and after its actual five-foot move to y5; both selected suppression and resumption outcomes are unchanged. D at y10 is outside the corrected sphere, and performs no affected magic during this interval. No rule grants targeting an opaque interior.')
ct=cb['cases'][8];assert ct['id']=='TU6-11-A'
ctb=ct['branches'][0];assert ctb['id']=='TC124-CT-SUPPRESSED-DEADLINE'
for ca in [ct,ctb]:
 # Restrict to this case's own states; its independent branches are processed separately.
 core={k:v for k,v in ca.items() if k!='branches'}
 changed_vectors[ca['id']+'-FIREBALL']=replace_fields(core,[15,0,3],[12.5,0,3],{'bodyCenteredArea'})
 def policy(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k=='relativeCenter' and v=='bound body center at release':x[k]='same declared visible front-surface point at bound-body offset[-2.5,0,3]; current body pose at release'
    else:policy(v)
  elif isinstance(x,list):
   for v in x:policy(v)
 policy(core)
 ca['syntheticPremises'].append('LOCAL CASE CORRECTION127: the Fireball LOAD fixes visible R front-surface point[12.5,0,3], at offset[-2.5,0,3] from its foot anchor[15,0,0], rather than an unperceived opaque body interior. The same fixed body-relative origin is used at release. The native20ft LOAD range is satisfied; C/R/E remain inside radius20. R is the expressly selected emitting body under the existing director local source-body rule, and its fixed Evocation exclusion remains R. No body becomes generally transparent and no new retargeting is introduced.')
changed_vectors['CT-ANTIMAGIC']=replace_fields(ctb,[15,0,3],[15,3,3],{'target','center'})
ctb['syntheticPremises'].append('LOCAL CASE CORRECTION127: E at[15,10,0] selects open point[15,3,3], seven feet from its source point, before R body y=2.5. The radius10 field still intersects R and suppresses the frame at its fixed deadline8.2. C remains outside. No opaque interior is selected.')
# Reconcile all complete case mirrors and canonical-object references.
original_dis=read(S/'ORIGINAL_SCENARIO_DISPOSITIONS.json');case_dis=read(S/'CASE_DISPOSITIONS.json')
for row in original_dis['scenarios']:
 row['currentCase']['canonicalObjectSha256']=canon(ptr(cb,row['currentCase']['pointer']))
for row in case_dis['cases']:
 case=ptr(cb,row['completeCase']['pointer']);row['completeCase']['canonicalObjectSha256']=canon(case)
 row['completeSyntheticPremises']=copy.deepcopy(case['syntheticPremises'])
 row['sourceReferences']=list(dict.fromkeys(s for e in case['timeline'] for s in e.get('sourceRefs',[])))
model=read(S/'MODEL.json');model['selectedCurrentCases124']=copy.deepcopy(cb['cases']);model['selectedOriginalScenarioDispositions124']=copy.deepcopy(original_dis['scenarios'])
modified={'CASEBOOK.json':cb,'MODEL.json':model,'CASE_DISPOSITIONS.json':case_dis,'ORIGINAL_SCENARIO_DISPOSITIONS.json':original_dis}
ops=[]
def diff(a,b,p=''):
 if type(a)==type(b) and isinstance(a,dict):
  out=[]
  for k in a.keys()|b.keys():
   q=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in a:out.append({'pointer':q,'beforePresent':False,'afterPresent':True,'after':b[k]})
   elif k not in b:out.append({'pointer':q,'beforePresent':True,'afterPresent':False,'before':a[k]})
   else:out.extend(diff(a[k],b[k],q))
  return out
 if type(a)==type(b) and isinstance(a,list) and len(a)==len(b):
  return [z for i,(av,bv) in enumerate(zip(a,b)) for z in diff(av,bv,p+'/'+str(i))]
 return [] if a==b else [{'pointer':p,'beforePresent':True,'afterPresent':True,'before':a,'after':b}]
def apply(x,ds,rev=False):
 x=copy.deepcopy(x)
 for op in reversed(ds) if rev else ds:
  pp,k=op['pointer'].rsplit('/',1);p=ptr(x,pp) if pp else x;k=k.replace('~1','/').replace('~0','~');k=int(k) if isinstance(p,list) else k
  side='after' if rev else 'before';other='before' if rev else 'after'
  if op[side+'Present']:assert p[k]==op[side]
  else:assert k not in p
  if op[other+'Present']:p[k]=copy.deepcopy(op[other])
  else:del p[k]
 return x
for file,obj in modified.items():
 before=read(S/file);ds=diff(before,obj);assert apply(before,ds)==obj and apply(obj,ds,True)==before
 (T/file).write_bytes(data(obj));ops.append({'file':file,'before':{'path':str(S/file),'bytes':(S/file).stat().st_size,'sha256':sha((S/file).read_bytes())},'after':{'bytes':(T/file).stat().st_size,'sha256':sha((T/file).read_bytes())},'operations':ds,'forwardReverseExact':True,'originalBytesRetained':True})
# No selected rules, sources, questions, actor selections or holds changed.
for file in ['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','ACTOR_TEMPLATES.json','HOLD_REGISTER.json','IDENTITY_DISPOSITIONS.json','DIRECTOR_SELECTIONS.json','OPERATIVE_TEXT.md']:
 assert (T/file).read_bytes()==(S/file).read_bytes()
def verify_chain(c):
 prev=c['initialState']
 for e in c['timeline']:assert prev==e['before'];assert e['before']['time']<=e['time']==e['after']['time'];prev=e['after']
 assert prev==c['finalState']
 for b in c['branches']:verify_chain(b)
for c in cb['cases']:verify_chain(c)
scalar=['hp','rp','dissonance','lastSpell','refrain','alive','dying','stable','wounds','critical']
def unchanged_results(a,b):
 for aid,x in a['finalState']['actors'].items():
  for k in scalar:assert x[k]==b['finalState']['actors'][aid][k]
 for x,y in zip(a['branches'],b['branches']):unchanged_results(x,y)
for a,b in zip(old['cases'],cb['cases']):unchanged_results(a,b)
receipt={'id':'TIME5-LOCAL-CASE-CORRECTIONS-127','scope':'Case inputs/order only, within unchanged director-selected procedures. Native sources, five procedures, six shared clauses,22 answers and all retained holds unchanged.','findings':['Return01 TU4-08-A24.005 free interaction preceded an immediate extra BA that expires before the next ordinary voluntary event. Move that actual ordinary interaction to original turn12.3; carry the same open book through absence.','Return01 Lesser Antimagic points were inside opaque T/R bodies; select real open nearby points at7ft within native10ft range.','Return01 Contingency Fireball LOAD selected unperceived R body interior although native LOAD legality is required. Select actual visible front surface and preserve that same declared body-relative point at release.'],'changedVectorCopies':changed_vectors,'files':ops,'fullStateContinuity':True,'allFinalHPResourcesLifeUnchanged':True,'noRuleChanges':True,'runtimeExecuted':False,'historicalBindings':'MANIFEST.json, ARTIFACT_BINDINGS.json, source additive operations, timestamp operations and original review remain the original director-return records; use CURRENT_MANIFEST_127 and this exact original-to-current chain for amended files. Original complete return remains in ../time5-return01 and original ZIP.'}
(T/'LOCAL_CASE_CORRECTIONS_127.json').write_bytes(data(receipt))
(T/'CURRENT_LOCAL_REVIEW_127.md').write_text('# Current Time/Cast5 case corrections127\n\nThe original director return and its historical review/manifests remain preserved. Current cases are CASEBOOK.json, with exact MODEL and disposition mirrors. LOCAL_CASE_CORRECTIONS_127.json supplies all full-value forward/inverse changes; CURRENT_MANIFEST_127.json binds current files. The original source-to-return operations are followed by these local operations.\n\nTime Skip opens its book at12.3 before departure18, carries it through the same-body return24, then immediately uses Sigil Rewrite24.01 after mandatory START processing. No ordinary voluntary interaction intervenes. Antimagic points are open air; Contingency fixes a visible front-surface Fireball point at LOAD and follows that same body-relative point at release. Costs, rolls, final HP/RP/Dissonance and life outcomes are unchanged. All procedures, shared clauses, question dispositions and retained holds remain exact.\n',encoding='utf-8')
files=[{'path':p.relative_to(T).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(T.rglob('*')) if p.is_file()]
(T/'CURRENT_MANIFEST_127.json').write_bytes(data({'id':'TIME5-CURRENT-CORRECTED-MANIFEST-127','files':files,'originalDirectorArchiveSha256':'cc1666c049c8045ece39c68041cb623140e618e61f653463896e1bcffe5c7f8d'}))
print(json.dumps({'modifiedFiles':[(x['file'],len(x['operations'])) for x in ops],'changedVectors':changed_vectors,'fullStateContinuity':True,'finalResultsUnchanged':True,'currentModelSha256':sha((T/'MODEL.json').read_bytes())},indent=2))
