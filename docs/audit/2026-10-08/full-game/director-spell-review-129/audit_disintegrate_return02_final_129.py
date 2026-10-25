"""Fresh local data/semantic acceptance evidence; supplied/historical programs never run."""
from pathlib import Path
import json,hashlib,zipfile,io,copy,datetime
D=Path(__file__).parent; E=D/'lifematter5_return02_received'; O=D/'lifematter5_return01_received'
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
def ck(label,value):
 checks.append(label);assert value,label
def apply(v,ops):
 v=copy.deepcopy(v)
 for o in ops:
  ks=[k.replace('~1','/').replace('~0','~') for k in o['path'].split('/')[1:]]
  if not ks:
   if o['op']=='test':assert v==o['value']
   elif o['op']=='replace':v=copy.deepcopy(o['value'])
   else:raise AssertionError(o)
   continue
  a=v
  for k in ks[:-1]:a=a[int(k)] if isinstance(a,list) else a[k]
  k=int(ks[-1]) if isinstance(a,list) else ks[-1]
  exists=(0<=k<len(a)) if isinstance(a,list) else k in a
  if o['op']=='test':assert exists and a[k]==o['value']
  elif o['op']=='testAbsent':assert not exists
  elif o['op']=='replace':assert exists;a[k]=copy.deepcopy(o['value'])
  elif o['op']=='add':
   assert not exists
   if isinstance(a,list):assert k==len(a);a.append(copy.deepcopy(o['value']))
   else:a[k]=copy.deepcopy(o['value'])
  elif o['op']=='remove':assert exists;del a[k]
  else:raise AssertionError(o)
 return v
raw=(E/'history/applied/DD_LifeMatter4_Applied_Context_129.zip').read_bytes()
ck('latest-applied-context-exact',raw==(D/'DD_LifeMatter4_Applied_Context_129.zip').read_bytes())
with zipfile.ZipFile(io.BytesIO(raw)) as z:oldraw=z.read('DD_LifeMatter5_Director_Return01_130.zip')
ck('complete-return01-byte-exact',oldraw==(D/'DD_LifeMatter5_Director_Return01_130.zip').read_bytes())
with zipfile.ZipFile(io.BytesIO(oldraw)) as z:
 ck('121-original-members',len(z.namelist())==121)
 for n in z.namelist():ck('original-member:'+n,z.read(n)==(O/n).read_bytes())
pa=rd(O/'PROCEDURES.json')['spells'];pb=rd(E/'PROCEDURES.json')['spells']
four=['awaken','bone-cage','contagion','telekinesis']
for a,b in zip(pa,pb):
 if a['id'] in four:
  ck('applied-procedure-exact:'+a['id'],a==b)
  ck('applied-markdown-exact:'+a['id'],(O/'procedures'/f"{a['id']}.md").read_bytes()==(E/'procedures'/f"{a['id']}.md").read_bytes())
ck('original-six-shared-rules-exact',rd(O/'SHARED_RULES.json')==rd(E/'SHARED_RULES.json')[:6])
ck('seventh-only-disintegrate',rd(E/'SHARED_RULES.json')[6]['appliesOnlyToSpellIds']==['disintegrate'])
ck('shared-model-envelope-exact',rd(E/'SHARED_RULES.json')==rd(E/'MODEL.json')['sharedRules']==rd(E/'PROPOSED_STANDALONE_ENVELOPE.json')['sharedRules'])
ck('actor-templates-unchanged',(O/'ACTOR_TEMPLATES.json').read_bytes()==(E/'ACTOR_TEMPLATES.json').read_bytes())
cc=rd(E/'evidence/CURRENT_CARDS.json')['cards']
for p in pb:ck('auxiliary-card-mirror:'+p['id'],cc[p['id']]==p)
for rec in rd(E/'REVISION_OPERATIONS.json')['records']:
 a=(O/rec['file']).read_bytes();b=(E/rec['file']).read_bytes()
 ck('revision-before:'+rec['file'],sha(a)==rec['beforeSha256'])
 ck('revision-after:'+rec['file'],sha(b)==rec['afterSha256'])
 x=json.loads(a.decode('utf-8-sig'));y=json.loads(b.decode('utf-8-sig'))
 ck('revision-forward:'+rec['file'],apply(x,rec['forward'])==y)
 ck('revision-inverse:'+rec['file'],apply(y,rec['inverse'])==x)
def flat(book):
 out={}
 def walk(c):
  out[c['id']]=c
  for b in c['branches']:walk(b)
 for c in book['mainCases']:walk(c)
 return out
a=flat(rd(O/'CASEBOOK.json'));b=flat(rd(E/'CASEBOOK.json'))
ck('original-35-cases-retained',set(a)<=set(b))
new='EV6-06-A/original-target-InstantDeath-stops-dust';fork=new+'/actual-RitualWard-intercepts-InstantDeath'
ck('exact-two-new-case-identities',set(b)-set(a)=={new,fork})
for cid,c in a.items():
 if c['spellId'] in four:ck('applied-case-exact:'+cid,c==b[cid])
ck('fatal-floor-one-original-exact',a['EV6-06-A/fatal-preexisting-third-Wound']==b['EV6-06-A/fatal-preexisting-third-Wound'])
for cid,c in a.items():
 if cid not in ['EV6-06-A','EV6-06-A/actual-Null-positive-zero','EV6-06-A/actual-Null-positive-zero/already-Dying']:
  ck('other-original-case-exact:'+cid,c==b[cid])
q=rd(E/'history/ORIGINAL_CANDIDATE.json')['questions']+rd(E/'history/ORIGINAL_FOLLOWUPS.json')['reviewRequirements'];answers=rd(E/'QUESTION_DISPOSITIONS.json')['dispositions']
ck('all20-questions',len(q)==len(answers)==20)
for x in q:ck('question-exact:'+x['id'],next(v for v in answers if v['id']==x['id'])['originalQuestionCompleteUnchanged']==x)
main=b[new];f=b[fork]
ck('new-case-11-events',len(main['timeline'])==11)
ck('new-fork-18-events',len(f['timeline'])==18)
ck('real-initial-20HP',main['initialState']['actors']['T']['hp']==main['initialState']['actors']['T']['maxHp']==20)
ck('real-7-damage-creates-13HP',main['timeline'][3]['after']['actors']['T']['hp']==13 and main['timeline'][3]['observations']['raw']==7)
dead=main['finalState']['actors']['T'];alive=f['finalState']['actors']['T']
ck('instant-death-intact-zero',dead['life']=='Dead' and dead['hp']==0 and dead['wounds']==0 and dead['body']['extent']==[5,5,6])
ck('actual-ward-living-one',alive['life']=='living' and alive['hp']==1 and alive['wounds']==0 and alive['type']=='Humanoid')
for cid in [new,fork]:
 c=b[cid];geom=c['geometry']
 for s in ['ArcaneBolt','Disintegrate','RitualWard']:
  x=geom[s];dist=sum((u-v)**2 for u,v in zip(x['sourcePoint'],x['targetPoint']))
  ck(cid+':geometry:'+s,dist==x['squaredDistance'] and dist<=x['rangeFeet']**2)
 for e in c['timeline']:
  for aid in e['after']['actors']:
   before=e['before']['actors'][aid];after=e['after']['actors'][aid]
   if any(before['wallet'][k] and not after['wallet'][k] for k in ['action','bonusAction']):
    p=before['phase'];ck(e['id']+':own-paid-action:'+aid,p['lastStart'] is not None and p['lastStart']<=e['time']<=p['lastStart']+p['turnSeconds'] and (p['lastEnd'] is None or p['lastStart']>p['lastEnd']))
  obs=e['observations']
  if 'damage' in obs:
   dm=obs['damage'];ck(e['id']+':real-75-over-13',dm['raw']==75 and dm['preHP']==13 and dm['maximum']==20 and dm['excessOverPreHP']==62)
   ck(e['id']+':terminal-no-replay',dm['woundSave'] is None and dm['WoundBranchSkipped'] and not dm['zeroHPFailureReplay'] and not dm['dustCheckpointEntered'] and not dm['originalTargetDust'])
   ck(e['id']+':no-dust-stock',not any('dust' in k.lower() for k in e['after']['objects']))
ck('ward-actual-costs',f['finalState']['actors']['K']['rp']==39 and f['finalState']['actors']['K']['conviction']==2)
for c in [main,f]:
 ck(c['id']+':disintegrate-real-cost',c['finalState']['actors']['C']['rp']==35)
 ck(c['id']+':arcane-bolt-real-cost',c['finalState']['actors']['B']['rp']==47)
timing=rd(D/'LIFEMATTER5_RETURN02_INDEPENDENT_DATA_AUDIT_129.json')['timingCandidates']
ck('zero-offturn-paid-actions',all(not x['spent'] for x in timing))
idx=R/'data/public/spell_playtests/authored_review_index.json'
ck('current627-index-exact',idx.read_bytes()==(E/'evidence/CURRENT_INDEX_129.json').read_bytes())
ck('still-pending-only-dis',next(e for e in rd(idx)['entries'] if e['id']=='disintegrate')['authoredStatus']=='pending-authored-procedure')
notes={
 'LM129-F01':'Resolved: actual ranged Prone disadvantage and Unconscious advantage cancel; one genuine d20=8+9=17 hitsAC13, source-created7force/failure1 preserved. Full casts inspector independently passes1222 checks.',
 'LM129-F02':'Resolved: exact spell and mirrored answer preserve independent temporal restoration/reconstruction contracts; no generic free regrowth, positive TimeLoop fixture or closure of its topology/equipment/clock hold.',
 'LM129-F03':'Resolved: explicit local terminal ordering follows current Healing/Death. Native paid new75force on actual13/20HP exceeds62>=20, finishes InstantDeath and stops dust. Exact paid Cult16Ritual6RP+3Conviction+1LR intercepts once, leaves1, no Wound/death/dust replay; type overlay ends at actual next targetEND8. Original floor-at1 fatal-Wound branch is exact.',
 'remainingOriginalDisintegrateCases':'Prior full semantic read remains supported by unchanged original case data except corrected Prone roll and explicit local ordering. Preserve realNullroot creation/exposure and already-zero histories, original-target-only rider, genuine transfer/protection,75-10temp=65 with excess15<100 and WoundDC32, separate gear, realPetrification/dust/Dispel and paid26RPTrueResurrection gates.',
 'timing':'All13 flagged body changes are forced/anatomy/death/return/fall cleanup, not off-turn normal paid actions. The added target at2.2 dies from another actor\'s spell; it does not take an Action.',
 'retainedBoundary':'Authored procedure acceptance only; finite newly declared scene premises remain qualified. No runtime/human/balance/cosmology/release certification or reopening of four applied identities.'}
selected=[c for c in b.values() if c['spellId']=='disintegrate']
report={'id':'DISINTEGRATE-RETURN02-FINAL-INDEPENDENT-REVIEW-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'checks':len(checks),'errors':[],'semanticFindings':[],'resolvedFindings':notes,'selectedIdentity':'disintegrate','selectedCases':[c['id'] for c in selected],'counts':{'mains':2,'branches':len(selected)-2,'events':sum(len(c['timeline']) for c in selected),'allQuestionsPreserved':20,'newBranches':2,'newEvents':29},'allNewSubstantiveEventsRead':True,'originalReviewRetained':'LIFEMATTER5_RETURN01_SEMANTIC_REVIEW_129.json','originalArchiveMembersByteExact':121,'appliedFourUnchanged':True,'canonicalChanges':False,'runtimeExecuted':False,'suppliedCodeExecuted':False}
out=D/'DISINTEGRATE_RETURN02_FINAL_INDEPENDENT_REVIEW_129.json';assert not out.exists();out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
