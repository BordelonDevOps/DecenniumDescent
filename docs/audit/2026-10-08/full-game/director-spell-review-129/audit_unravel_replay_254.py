import json,pathlib,hashlib,zlib
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
P=B/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_254.json'
d=json.loads(P.read_text(encoding='utf-8'))
def can(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sh(x): return hashlib.sha256(can(x)).hexdigest()
checks=[]
def add(n,ok,e): checks.append({'check':n,'passed':bool(ok),'evidence':e})
tr=d['forwardInverseTransitions']
add('exact-transition-count',len(tr)==23,len(tr))
for x in tr:
    add('before-hash-'+x['id'],sh(x['before'])==x['beforeSha256'],x['beforeSha256'])
    add('after-hash-'+x['id'],sh(x['after'])==x['afterSha256'],x['afterSha256'])
    add('inverse-is-exact-before-'+x['id'],x['inverseOperation']['restoreSnapshot']==x['before'] and x['inverseOperation']['restoreSha256']==x['beforeSha256'],x['inverseOperation']['id'])
states=d['commonTargetSnapshots']; a=states['afterUnravelAdmission']; n=states['afterNaturalExpiry']; m=states['afterMindBlankSuppressionBeforeEND']; q=states['afterArchDispelBeforeTargetTurn']
add('target-baseline-resources',states['afterLongRest']['HP']=={'current':138,'max':138} and states['afterLongRest']['sharedRP']=={'current':46,'max':46} and states['afterLongRest']['bufferReserve']=={'current':35,'max':35},states['afterLongRest'])
add('target-before-cast-ordered',states['afterFamiliar']['sharedRP']['current']==42 and states['afterDetectMagic']['sharedRP']['current']==41 and states['afterDetectMagic']['concentration']['active'] and states['afterEarthWarden']['shiftUses']['current']==5 and states['afterEarthWarden']['bufferReserve']['current']==5,{'familiarRP':42,'detectRP':41,'shiftUses':states['afterEarthWarden']['shiftUses'],'buffer':states['afterEarthWarden']['bufferReserve']})
add('form-instance-and-bound-tempHP',states['afterEarthWarden']['form']['id']=='FORM-EW-01' and states['afterEarthWarden']['formTempHP']==30 and states['afterEarthWarden']['form']['ordinaryDeadline']=='2026-10-30T10:10:20Z',states['afterEarthWarden']['form'])
add('unravel-terminal-callbacks',a['form'] is None and a['formTempHP']==0 and a['concentration'] is None and not a['classAvailability']['Druid'] and not a['classAvailability']['Mage'] and a['HP']=={'current':138,'max':138} and a['sharedRP']=={'current':40,'max':46} and a['familiar']['deadline']=='2026-10-30T10:10:01Z' and not a['familiarCommandAvailable'],a)
add('natural-expiry-recovery-without-recreation',n['classAvailability']=={'Druid':True,'Mage':True} and n['form'] is None and n['formTempHP']==0 and n['concentration'] is None and n['dissonance']['current']==1 and n['familiar']['HP']=={'current':14,'max':14} and n['familiar']['deadline']=='2026-10-30T10:10:01Z',n)
add('mindblank-suppression-before-original-deadline',m['classAvailability']=={'Druid':True,'Mage':True} and m['form'] is None and m['concentration'] is None and m['unravel']['endsAt']=='2026-10-30T10:00:36Z' and d['coverage']['mindBlank'].startswith('Conditional only'),d['coverage']['mindBlank'])
add('arch-dispel-early-restore-not-recreate',q['classAvailability']=={'Druid':True,'Mage':True} and q['form'] is None and q['concentration'] is None and q['unravel']['classLoss'].startswith('ended by Arch Dispel') and q['familiar']['deadline']=='2026-10-30T10:10:01Z',q)
u=d['casterSnapshots']['unravelAfter']; mb=d['casterSnapshots']['mindBlankAfter']; disp=d['casterSnapshots']['dispelAfterArchDispel']
add('unravel-caster-budget',u['RP']=={'current':38,'max':64} and u['castHistory'][0]['RP']==26,u)
add('mindblank-caster-budget',mb['RP']=={'current':43,'max':64} and mb['castHistory'][0]['RP']==21,mb)
add('arch-dispel-caster-budget-and-check',disp['RP']=={'current':59,'max':64} and disp['check']=={'roll':8,'INT':5,'PB':6,'total':19,'DC':19,'result':'success'} and disp['recharge']['ArchDispel']==2,disp)
add('one-round-turn-markers',a['unravel']['admitted']=='2026-10-30T10:00:27Z' and a['unravel']['endsAt']=='2026-10-30T10:00:36Z' and n['currentTargetTurn'].endswith('END10:00:36Z; Let the Note Fall2→1; Unravel naturally ended'),{'admitted':a['unravel']['admitted'],'start':'10:00:30Z','end':a['unravel']['endsAt']})
add('dissonance-vent-applied-once',n['dissonance']['current']==1 and 'T5 no-spell Dodge vents2→1' in d['coverage']['letTheNoteFall'] and states['afterNoSpellVentT2']['dissonance']['current']==0,d['coverage']['letTheNoteFall'])
add('branch-boundaries-disclosed',d['coverage']['mindBlank'].startswith('Conditional only') and '20ft within30ft' in d['coverage']['archDispel'],d['coverage'])
add('no-acceptance-or-application',d['accepted'] is False and d['applied'] is False and 'no runtime or campaign execution claim' in d['qualification'],{'accepted':d['accepted'],'applied':d['applied'],'qualification':d['qualification']})
ids=[x['id'] for x in tr]
add('branch-turns-fully-expanded',all(x in ids for x in ['OP254-06-NATURAL-T5-START','OP254-09-NATURAL-T5-DODGE','OP254-10-NATURAL-FAMILIAR-PHASE','OP254-11-NATURAL-T5-END','OP254-12-MINDBLANK-T5-START','OP254-13-MINDBLANK-T5-DODGE','OP254-14-MINDBLANK-FAMILIAR-PHASE','OP254-15-MINDBLANK-T5-END','OP254-16-ARCH-T5-START','OP254-17-ARCH-T5-DODGE','OP254-18-ARCH-FAMILIAR-PHASE','OP254-19-ARCH-T5-END']),ids)
ph=d['familiarAttachedPhases']
add('familiar-branch-phase-owners',all(ph[k]['time']=='2026-10-30T10:00:33Z' and ph[k]['HP']=={'current':14,'max':14} and ph[k]['AC']==18 and ph[k]['fireResistance'] for k in ['naturalExpiry','mindBlankConditional','archDispel']) and ph['naturalExpiry']['ownerCommandPermission'] is False and ph['mindBlankConditional']['ownerCommandPermission'] is True and ph['archDispel']['ownerCommandPermission'] is True and all(ph[k]['pendingOrder'] is None for k in ph),ph)
add('elemental-affinity-dependency',states['afterLongRest']['resistances']==[{'source':'mage.base.elemental-affinity','type':'fire','status':'active'}] and states['afterEarthWarden']['resistances'][0]['source']=='mage.base.elemental-affinity' and states['afterUnravelAdmission']['resistances']==[] and n['resistances'][0]['source']=='mage.base.elemental-affinity' and all(states[k]['familiar']['fireResistance'] for k in ['afterFamiliar','afterUnravelAdmission','afterNaturalExpiry']),{'before':states['afterLongRest']['resistances'],'activeForm':states['afterEarthWarden']['resistances'],'classLoss':states['afterUnravelAdmission']['resistances'],'restored':n['resistances']})
form=states['afterEarthWarden']['form']
add('earth-warden-attack-and-recharge-separation',form['naturalAttack']['circleForms']['source']=='druid.base.moon.circle-forms' and form['naturalAttack']['primalStrike']['source']=='druid.arch.moon.primal-strike' and form['earthSlamRecharge']=={'source':'druid.arch.earth-warden-dire-bear','printedRounds':2,'remainingRounds':0,'used':False,'owner':'MD196-TARGET-HUMAN-DRUID15-MAGE5','survivesFormLoss':True} and a['formSourceCounters']['earthSlam']['remainingRounds']==0,form)
disp= d['casterSnapshots']['dispelAfterArchDispel']
add('arch-dispel-range-and-observed-aura',disp['perception']['distanceFt']==20 and disp['perception']['DetectMagicRangeFt']==30 and disp['perception']['lineOfSight']=='clear' and disp['perception']['cover']=='none' and disp['perception']['activeAuraCountOnTarget']==1 and disp['perception']['observedAt']=='2026-10-30T10:00:27Z' and disp['turnBudgets']['Action']=='spent: Arch Dispel',disp['perception'])
add('paid-action-budgets-and-cadence',states['afterFamiliar']['ordinaryTurnBudgets']['Action']=='spent: Conjure Elemental Familiar' and states['afterDetectMagic']['ordinaryTurnBudgets']['Action']=='spent: Mage Detect Magic' and states['afterEarthWarden']['ordinaryTurnBudgets']['Action']=='spent: Mage Arcane Missile' and states['afterEarthWarden']['ordinaryTurnBudgets']['BonusAction']=='spent: Earth Warden shift' and states['afterNoSpellVentT2']['dissonance']['current']==0 and n['dissonance']['current']==1,{'afterFamiliar':states['afterFamiliar']['ordinaryTurnBudgets'],'afterDetectMagic':states['afterDetectMagic']['ordinaryTurnBudgets'],'afterEarthWarden':states['afterEarthWarden']['ordinaryTurnBudgets'],'T2':states['afterNoSpellVentT2']['dissonance'],'T5':n['dissonance']})
failed=[x for x in checks if not x['passed']]
raw=P.read_bytes(); bind={'path':P.relative_to(W).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
audit={'id':'UNRAVEL-IDENTITY-MD196-B02-REPLAY-AUDIT-254','recordedAtUtc':'2026-10-30T12:37:00+00:00','status':'PASS_WITH_DIRECTOR_RULINGS_PENDING' if not failed else 'FAIL','checksPassed':len(checks)-len(failed),'checkCount':len(checks),'checksFailed':len(failed),'checks':checks,'failures':failed,'replayBinding':bind,'decisionBoundary':'Hash/arithmetic/state-transition audit only. Mind Blank remains conditional without its accepted duration source; Arch Dispel is source-qualified within30ft. GPT acceptance remains pending; no application is asserted.'}
A=B/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_254_AUDIT.json'
A.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(A),'status':audit['status'],'passed':audit['checksPassed'],'count':audit['checkCount'],'failed':failed,'replayBinding':bind},ensure_ascii=False,indent=2))
