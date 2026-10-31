import json,pathlib,hashlib,zlib
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
P=B/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_255.json'
PLAN=B/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_255.json'
d=json.loads(P.read_text(encoding='utf-8'))
plan=json.loads(PLAN.read_text(encoding='utf-8'))
def can(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sh(x): return hashlib.sha256(can(x)).hexdigest()
checks=[]
def add(n,ok,e): checks.append({'check':n,'passed':bool(ok),'evidence':e})
tr=d['forwardInverseTransitions']; ids=[x['id'] for x in tr]
add('transition-count-and-unique-ids',len(tr)==30 and len(ids)==len(set(ids)),{'count':len(tr),'unique':len(set(ids))})
for x in tr:
    add('before-hash-'+x['id'],sh(x['before'])==x['beforeSha256'],x['beforeSha256'])
    add('after-hash-'+x['id'],sh(x['after'])==x['afterSha256'],x['afterSha256'])
    add('inverse-exact-before-'+x['id'],x['inverseOperation']['restoreSnapshot']==x['before'] and x['inverseOperation']['restoreSha256']==x['beforeSha256'],x['inverseOperation']['id'])
byid={x['id']:x for x in tr}
branches=['NATURAL-EXPIRY','MINDBLANK-CONDITIONAL','ARCH-DISPEL-REMOVAL']
add('each-branch-has-separate-start-admission-dodge-end-phase',all(f'OP255-08-{b}-T5-START' in byid and f'OP255-11-{b}-UNRAVEL-ADMISSION' in byid and ({'NATURAL-EXPIRY':'OP255-16-NATURAL-T5-DODGE','MINDBLANK-CONDITIONAL':'OP255-17-MINDBLANK-T5-DODGE','ARCH-DISPEL-REMOVAL':'OP255-18-ARCH-DISPEL-T5-DODGE'}[b] in byid) and ({'NATURAL-EXPIRY':'OP255-19-NATURAL-T5-END','MINDBLANK-CONDITIONAL':'OP255-20-MINDBLANK-T5-END','ARCH-DISPEL-REMOVAL':'OP255-21-ARCH-DISPEL-T5-END'}[b] in byid) and any(b in k and 'FAMILIAR-ATTACHED-PHASE' in k for k in ids) for b in branches),ids)
for b in branches:
    st=byid[f'OP255-08-{b}-T5-START']; ad=byid[f'OP255-11-{b}-UNRAVEL-ADMISSION']
    add('branch-clock-'+b,st['timestamp']=='2026-10-30T10:00:24Z' and ad['timestamp']=='2026-10-30T10:00:27Z' and ad['after']['unravel']['endsAt']=='2026-10-30T10:00:30Z',{'start':st['timestamp'],'admission':ad['timestamp'],'end':ad['after']['unravel']['endsAt']})
states=d['commonTargetSnapshots']; target_start=states['afterTargetT5Start']; adm=states['afterUnravelAdmission']; nat=states['afterNaturalExpiry']
add('target-t5-start-before-admission',target_start['currentTargetTurn'].startswith('T5 START10:00:24Z') and target_start['ordinaryTurnBudgets']=={'Action':'ready','BonusAction':'ready','Reaction':'ready'} and adm['unravel']['admitted']=='2026-10-30T10:00:27Z' and adm['unravel']['endsAt']=='2026-10-30T10:00:30Z',{'start':target_start['currentTargetTurn'],'admission':adm['unravel']})
add('refrain-cleared-by-shift',states['afterDetectMagic']['refrain']=={'repeatCount':0,'lastSpell':'mage.base.detect-magic'} and states['afterEarthWardenShift']['refrain']=={'repeatCount':0,'lastSpell':None} and states['afterEarthWardenShift']['sharedRP']=={'current':41,'max':46} and states['afterEarthWardenShift']['dissonance']['current']==1,{'before':states['afterDetectMagic']['refrain'],'after':states['afterEarthWardenShift']['refrain']})
add('no-arcane-missile-event',not any('arcane-missile' in json.dumps(x,ensure_ascii=False).lower() and ('cast' in json.dumps(x,ensure_ascii=False).lower() or 'paid' in json.dumps(x,ensure_ascii=False).lower()) for x in tr),[x['id'] for x in tr])
add('target-vent-at-first-future-end',nat['dissonance']['current']==0 and nat['currentTargetTurn'].endswith('Let the Note Fall1→0; Unravel naturally ended') and nat['unravel']['endsAt']=='2026-10-30T10:00:30Z',{'dissonance':nat['dissonance'],'turn':nat['currentTargetTurn']})
# The attached phase is after the owner's full T5 end; its before and after both carry complete actor/familiar state.
ph=d['familiarAttachedPhases']
required={'actor','id','source','identity','HP','AC','speed','fireResistance','created','deadline','positionFt','ownerId','ownerClassAvailability','ownerClassDerivedProficiencyAvailable','ownerCommandPermission','ownerUnravel','ownerSubjectiveBelief','ownerResistances','pendingOrder','mode','conjureFamiliarUse','commandHistory','attachedPhase','phase'}
for name,key in [('naturalExpiry','NATURAL-EXPIRY'),('mindBlankConditional','MINDBLANK-CONDITIONAL'),('archDispel','ARCH-DISPEL-REMOVAL')]:
    pair=ph[name]
    add('complete-familiar-before-after-'+name,all(required.issubset(pair[x].keys()) for x in ['before','after']) and all(pair[x]['HP']=={'current':14,'max':14} and pair[x]['AC']==18 and pair[x]['fireResistance'] and pair[x]['deadline']=='2026-10-30T10:10:01Z' and pair[x]['pendingOrder'] is None and pair[x]['ownerCommandPermission'] is True for x in ['before','after']),{'beforeKeys':sorted(pair['before'].keys()),'afterKeys':sorted(pair['after'].keys())})
    add('familiar-phase-after-owner-end-'+name,pair['before']['attachedPhase']['ownerTurnEnd']=='2026-10-30T10:00:30Z' and pair['after']['attachedPhase']['phaseTime']=='2026-10-30T10:00:30.1Z' and 'Action' not in pair['after'] and 'BonusAction' not in pair['after'] and 'Reaction' not in pair['after'] and not any(k.lower().startswith('generic') or k=='turnBudgets' for k in pair['after']),pair['after']['attachedPhase'])
# Each target branch ledger explicitly shows the complete :24, :27, :29, :30, :30.1 sequence.
for b,ledger in d['branchTurnLedgers'].items():
    times=[x['time'] for x in ledger]
    add('full-target-turn-ledger-'+b,times[0]=='2026-10-30T10:00:24Z' and '2026-10-30T10:00:27Z' in times and '2026-10-30T10:00:29Z' in times and '2026-10-30T10:00:30Z' in times and times[-1]=='2026-10-30T10:00:30.1Z',times)
add('mindblank-remains-conditional',states['afterMindBlankConditionalProjection']['suppressionBranchStatus'].startswith('CONDITIONAL_NOT_COUNTED') and d['coverage']['mindBlank'].startswith('Conditional only'),d['coverage']['mindBlank'])
# Verify helper profile and regular-turn lifecycle, including class matrix source and recharge tick.
helper=d['helperRegularTurnSnapshots']; ledger=d['helperRegularTurnLedger']; disp=helper['T3AfterArchDispel']; final=helper['T4StartAfterRechargeTick']
profile=plan['qualifiedActors']['archDispelRemover']
add('dispel-always-prepared-class-matrix-outside-slots',profile['acquiredClassCards']==['wizard.arch.dispel-magic acquired at Wizard5'] and profile['castHistory'][-1]['family']=='always-prepared Wizard class matrix; outside daily prepared-slot count',{'acquired':profile['acquiredClassCards'],'family':profile['castHistory'][-1]['family']})
add('helper-turn-schedule-t1-to-t4',[x['turn'] for x in ledger]==['AD-T1','AD-T2','AD-T3','AD-T4'] and ledger[0]['start'].endswith('10:00:12Z') and ledger[0]['end'].endswith('10:00:18Z') and ledger[1]['start'].endswith('10:00:18Z') and ledger[1]['end'].endswith('10:00:24Z') and ledger[2]['start'].endswith('10:00:24Z') and ledger[2]['end'].endswith('10:00:30Z') and ledger[3]['start'].endswith('10:00:30Z'),ledger)
add('helper-t2-no-spell-preserves-history',helper['T2End']['refrain']==helper['T1AfterDetectMagic']['refrain'] and helper['T2End']['castHistory']==helper['T1AfterDetectMagic']['castHistory'] and helper['T2End']['castingFamilyHistory']==helper['T1AfterDetectMagic']['castingFamilyHistory'] and helper['T2End']['dissonance']['current']==0,helper['T2End'])
add('helper-dispel-family-and-refrain',disp['refrain']=={'repeatCount':0,'lastSpell':'wizard.arch.dispel-magic'} and disp['castingFamilyHistory']==['detect-magic prepared matrix family','wizard.arch.dispel-magic always-prepared Wizard class matrix family'] and disp['recharge']['ArchDispel']==2,{'refrain':disp['refrain'],'families':disp['castingFamilyHistory'],'recharge':disp['recharge']})
add('helper-recharge-ticks-at-next-regular-start',helper['T3End']['recharge']['ArchDispel']==2 and final['recharge']['ArchDispel']==1 and final['rechargeTickHistory']==[{'time':'2026-10-30T10:00:30Z','before':2,'after':1,'source':'wizard.json /engine/12'}],{'T3End':helper['T3End']['recharge'],'T4Start':final['recharge'],'history':final['rechargeTickHistory']})
add('arch-dispel-observation-and-check',disp['perception']=={'distanceFt':20,'DetectMagicRangeFt':30,'lineOfSight':'clear','cover':'none','activeAuraCountOnTarget':1,'observedAt':'2026-10-30T10:00:27Z','observation':'the unique ongoing spell aura on the target is UI-01; no other active spell aura is present'} and disp['check']=={'roll':8,'INT':5,'PB':6,'total':19,'DC':19,'result':'success'},disp['perception'])
add('no-acceptance-or-application',d['accepted'] is False and d['applied'] is False and plan['accepted'] is False and plan['applied'] is False,{'replay':[d['accepted'],d['applied']],'plan':[plan['accepted'],plan['applied']]})
failed=[x for x in checks if not x['passed']]
raw=P.read_bytes(); bind={'path':P.relative_to(W).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
planraw=PLAN.read_bytes(); planbind={'path':PLAN.relative_to(W).as_posix(),'bytes':len(planraw),'sha256':hashlib.sha256(planraw).hexdigest(),'crc32':f'{zlib.crc32(planraw)&0xffffffff:08x}'}
audit={'id':'UNRAVEL-IDENTITY-MD196-B02-REPLAY-AUDIT-255','recordedAtUtc':'2026-10-30T12:49:00+00:00','status':'PASS_WITH_DIRECTOR_RULINGS_PENDING' if not failed else 'FAIL','checksPassed':len(checks)-len(failed),'checkCount':len(checks),'checksFailed':len(failed),'checks':checks,'failures':failed,'replayBinding':bind,'planBinding':planbind,'decisionBoundary':'Independent hash, chronology, resource, lifecycle and callback audit only. Mind Blank remains conditional. GPT acceptance remains pending; no application is asserted.'}
A=B/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_255_AUDIT.json'
A.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(A),'status':audit['status'],'passed':audit['checksPassed'],'count':audit['checkCount'],'failed':failed,'replayBinding':bind},ensure_ascii=False,indent=2))
