import json,pathlib,hashlib,zlib,zipfile
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
P=B/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_254.json'
Q=B/'CURRENT36_PENDING_IDENTITY_AUDIT_250.json'
Z=B/'rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip'
d=json.loads(P.read_text(encoding='utf-8')); pending=json.loads(Q.read_text(encoding='utf-8'))
def rawbind(path,raw): return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
checks=[]
def add(name,ok,evidence): checks.append({'check':name,'passed':bool(ok),'evidence':evidence})
with zipfile.ZipFile(Z) as z:
    def member(tail):
        hits=[n for n in z.namelist() if n.startswith('sources_current/') and n.endswith(tail)]
        if len(hits)!=1: raise RuntimeError((tail,hits))
        return z.read(hits[0])
    src={x:json.loads(member(f'data/public/class_playtests/{x}.json')) for x in ['druid','mage','wizard']}
    cat=json.loads(member('data/public/spell_playtests/catalog.json'))
    source_members={x:member(t) for x,t in {
      'druidClass':'data/public/class_playtests/druid.json','mageClass':'data/public/class_playtests/mage.json','wizardClass':'data/public/class_playtests/wizard.json',
      'formTempHP':'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md','creatureLifecycle':'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md',
      'maximumHP':'docs/mechanics/MAXIMUM_HP_PLAYTEST.md','bodyEquipment':'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',
      'characterCreation':'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md','resonanceCanon':'docs/mechanics/RESONANCE_CANON.md',
      'spellIntegration':'docs/mechanics/SPELL_INTEGRATION_RULES.md','catalog':'data/public/spell_playtests/catalog.json'}.items()}
    for k,b in source_members.items():
        bound=d['sourceAuthority']['packet241MemberBindings'][k]
        add('source-binding-'+k,rawbind(bound['path'],b)==bound,{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
# Authority/review-state guards.
add('authority-counts',d['authority']['reviewedApplied']==812 and d['authority']['pending']==36 and d['authority']['acceptedUnapplied']==0, d['authority'])
add('exact-current-pending-ids',pending['pendingIds']==d['authority']['pendingIdentityAudit'].get('pendingIds',pending['pendingIds']) if 'pendingIds' in d['authority']['pendingIdentityAudit'] else pending['pendingCount']==36,{'auditCount':pending['pendingCount'],'planCount':d['authority']['pending']})
add('no-accept-or-apply',d['accepted'] is False and d['applied'] is False,{'accepted':d['accepted'],'applied':d['applied'],'status':d['status']})
add('index-catalog-bindings-match-packet',d['authority']['currentIndexBinding']['bytes']==1600663 and d['authority']['currentIndexBinding']['sha256']=='565b5fce6c4797d96d2c6d8377ca152be38990216f63414cca7cff472f7993ce' and d['authority']['catalogBinding']['sha256']=='773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b',d['authority'])
# Supplemental register is a distinct extra binding.
regpath=W/d['sourceAuthority']['supplementalLocalFormRegister']['path']
regbind=rawbind(d['sourceAuthority']['supplementalLocalFormRegister']['path'],regpath.read_bytes())
add('supplemental-form-register-binding',regbind=={k:v for k,v in d['sourceAuthority']['supplementalLocalFormRegister'].items() if k in regbind},regbind)
add('supplemental-not-packet241',d['sourceAuthority']['supplementalLocalFormRegister']['status']=='SUPPLEMENTAL_SOURCE_BOUND_FOR_THIS_WITNESS_NOT_PACKET241' and 'druid_form_profiles.json' not in [x['path'] for x in d['sourceAuthority']['packet241MemberBindings'].values()],d['sourceAuthority']['supplementalLocalFormRegister']['status'])
reg=json.loads(regpath.read_text(encoding='utf-8'))
ew=reg['profiles']['druid.arch.earth-warden-dire-bear']
add('earth-warden-profile',ew['minimumLevel']==11 and ew['archAttunement'] and ew['canSpeak'] and ew['ac']['mode']=='normal' and ew['entryBuffer']==30 and ew['attack']['damage']=='1d8+WIS' and ew['handBasedEquipmentUse'] is False,{'id':ew['sourceId'],'minimumLevel':ew['minimumLevel'],'entryBuffer':ew['entryBuffer'],'ac':ew['ac'],'attack':ew['attack']})
# Target progression/resource arithmetic.
t=d['qualifiedActors']['target']
add('target-class-sequence',len(t['levelSequence'])==20 and t['levelSequence'][0]['classLevel']==1 and t['levelSequence'][-1]=={'characterLevel':20,'class':'Druid','classLevel':15} and t['entryAtCharacter2']['gates'].endswith('both pass'),{'levels':len(t['levelSequence']),'entry':t['entryAtCharacter2']})
add('asi-character-levels',[x['characterLevel'] for x in t['ASIs']]==[5,9,13,17],t['ASIs'])
add('target-computed-maxima',d['proposedTarget']['computedState']['proficiencyBonus']==6 and d['proposedTarget']['computedState']['sharedRPMax']==46 and d['proposedTarget']['computedState']['maximumHP']==138,{'PB':6,'RP':46,'HP':138})
add('equipment-custody-and-ac',t['equipment']['remainingCoin']=='74gp 5sp' and t['equipment']['rootAC']==12 and t['equipment']['EarthWardenAC']==12 and len(t['equipment']['items'])==2,t['equipment'])
# Spell repertoire and class-card acquisition.
def spellmap(): return {x['id']:x for x in cat['spells']}
sm=spellmap()
druid=src['druid']; mage=src['mage']; wizard=src['wizard']
for s in t['repertoire']['druidCantrips']+t['repertoire']['druidPrepared']:
    a=sm[s['id']]['classAccess']['Druid']
    ok=a['rank']==s['rank'] and a['minimumClassLevel']==s['minimumClassLevel'] and s['operationalEntryAvailable']
    if s in t['repertoire']['druidPrepared']: ok=ok and a['rank']<=8 and a['minimumClassLevel']<=15
    add('druid-spell-'+s['id'],ok,a)
add('druid-repertoire-count',len(t['repertoire']['druidCantrips'])==4 and len(t['repertoire']['druidPrepared'])==20 and t['repertoire']['druidPreparedCount']==20,{'cantrips':len(t['repertoire']['druidCantrips']),'prepared':len(t['repertoire']['druidPrepared'])})
druidIds={c['id'] for c in druid['cards']}
mageIds={c['id'] for c in mage['cards']}
wizardIds={c['id'] for c in wizard['cards']}
targetMageCards=t['repertoire']['mageSelected']
add('mage-selected-cards',all(s in mageIds for s in targetMageCards) and all(x in t['repertoire']['mageAutomatic'] for x in ['mage.base.spellcasting','mage.base.resonance-pool','mage.base.resonance-surge']),targetMageCards)
# Wizard profile and full spellbook, legal spell learning and matrix set.
w=d['qualifiedActors']['unravelCaster']
add('wizard-rp-rank-source',wizard['rpByClassLevel'][16]==64 and wizard['maxSpellRankByClassLevel'][16]==9 and w['RPMax']==64 and w['maxRank']==9,{'RP17':wizard['rpByClassLevel'][16],'rank17':wizard['maxSpellRankByClassLevel'][16]})
book=w['spellbook']['allLearnedEntries']; bookids={x['id'] for x in book}
add('wizard-spellbook-total',len(book)==67 and len(bookids)==67 and w['spellbook']['count']==67,{'count':len(book),'unique':len(bookids)})
for x in book:
    a=sm[x['id']]['classAccess']['Wizard']; lv=x['level']
    ok=x['rank']==a['rank'] and a['minimumClassLevel']<=lv and a['rank']<=wizard['maxSpellRankByClassLevel'][lv-1]
    add('wizard-book-'+x['id']+'-'+str(lv),ok,{'rank':x['rank'],'minimum':a['minimumClassLevel'],'legalMax':wizard['maxSpellRankByClassLevel'][lv-1]})
add('wizard-review-spell-acquisition',any(x['id']=='mind-blank' and x['level']==15 and x['rank']==8 for x in book) and any(x['id']=='unravel-identity' and x['level']==17 and x['rank']==9 for x in book),{'Mind Blank':'W15/R8','Unravel':'W17/R9'})
add('wizard-prepared-matrix-set',len(w['preparedMatrices'])==22 and {'mind-blank','unravel-identity','detect-magic'}.issubset({x['id'] for x in w['preparedMatrices']}) and all(x['id'] in bookids for x in w['preparedMatrices']),{'prepared':len(w['preparedMatrices'])})
add('wizard-dispel-card-acquired',any(x['level']==5 and 'wizard.arch.dispel-magic' in x['ids'] for x in w['selectedCards']) and 'wizard.arch.dispel-magic' in wizardIds,{'selectedAt':5,'id':'wizard.arch.dispel-magic'})
add('wizard-HP-and-DC',w['HP']=='104/104' and w['school'].startswith('Illusion') and 'spell attack12' in w['school'] and 'spell save DC20' in w['school'] and w['RPMax']==64,{'HP':w['HP'],'school':w['school'],'RP':w['RPMax']})
# Direct replay boundaries.
events=d['commonPrehistory']; names=[x['event'] for x in events]
add('lawful-cast-shift-order',names.index('TARGET-T1-CAST-FIRE-FAMILIAR')<names.index('TARGET-T3-CAST-DETECT-MAGIC')<names.index('TARGET-T4-CAST-ARCANE-MISSILE-THEN-SHIFT')<names.index('ADMIT-UNRAVEL'),names)
add('pre-cast-state-and-form',d['commonPrehistory'][4]['after']['shift']=='5/6' and d['commonPrehistory'][4]['after']['buffer']=='5/35' and d['commonPrehistory'][4]['after']['tempHP']=='30 tied to FORM-EW-01' and 'no spellcasting while shifted' in d['commonPrehistory'][4]['action'],d['commonPrehistory'][4]['after'])
adm=next(x for x in events if x['event']=='ADMIT-UNRAVEL')['after']
add('admission-resource-callback',adm['TargetHP']=='138/138' and adm['TargetRP']=='40/46' and adm['TargetDissonance']=='2/12' and 'remove30 form tempHP' in adm['form'] and adm['concentration']=='DM-01 ended terminally at admission' and 'original10:10:01Z deadline' in adm['familiar'],adm)
mb=d['coverageAndReversibleEvidencePlan']['forks'][1]
add('mindblank-branch-clock-qualification',mb['status']=='CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS' and 'rank8ward5_reviewed_149/MODEL.json /spells/3/procedure' in mb['sourceRequirement'] and 'duration' in mb['sourceRequirement'],mb)
add('arch-dispel-branch-arithmetic','d20 8 + INT5 + PB6 =19 vs DC19' in d['coverageAndReversibleEvidencePlan']['forks'][2]['separateActor'] and '20ft' in d['coverageAndReversibleEvidencePlan']['forks'][2]['separateActor'],d['coverageAndReversibleEvidencePlan']['forks'][2]['separateActor'])
add('end-turn-dissonance-cadence',any('Dissonance2→1' in x for x in d['coverageAndReversibleEvidencePlan']['forks'][0]['events']),d['coverageAndReversibleEvidencePlan']['forks'][0]['events'])
add('form-loss-is-local-proposed-rule','NEW UI251-FORM-LOSS' in json.dumps(d['dependencyCallbackPlan']) and 'No global Druid/antimagic rule' in json.dumps(d['dependencyCallbackPlan']),{'callback':'spell-local proposal only'})
add('preserve-existing-case-set',d['sourceAuthority']['return241']['sha256']=='bb972286a55bbb7ebaf9965f8d8ca1cfdc64a3f0ffe1b05067473dcdbbddb3a5' and len(d['sourceAuthority']['preservedCases'])==2,d['sourceAuthority']['preservedCases'])
add('forward-inverse-audit-only',len(d['reversibleStateOperations'])==6 and all('audit' in x['inverse'].lower() or 'static' in x['inverse'].lower() or 'inverse snapshots' in x['inverse'].lower() or 'data replay' in x['inverse'].lower() for x in d['reversibleStateOperations']),d['reversibleStateOperations'])
rules=d['sourceAuthority']['packet241MemberBindings']['classPlaytestRules']
add('fallback-repertoire-rule-source',rules['path']=='sources_current/DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md' and rules['bytes']==17321 and rules['sha256']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81' and rules['crc32']=='5ce776a0',rules)
mr=t['repertoire']
mage_cantrips=mr['mageOrdinaryCantrips']; mage_known=mr['mageOrdinaryKnownSpells']
add('mage-ordinary-repertoire-count-and-gates',len(mage_cantrips)==4 and mr['mageOrdinaryCantripCount']==4 and len(mage_known)==6 and mr['mageOrdinaryKnownSpellCount']==6 and [x['acquiredClassLevel'] for x in mage_cantrips]==[1,1,1,4] and [x['acquiredClassLevel'] for x in mage_known]==[1,1,2,3,4,5] and all(x['operationalStatus']=='operational-playtest-draft' for x in mage_cantrips+mage_known),{'cantrips':mage_cantrips,'knownSpellIds':[x['id'] for x in mage_known]})
add('mage-repertoire-progression-source-and-rank-gates',mr['mageOrdinaryCantripRule']['source']=='CLASS_PLAYTEST_RULES.md, Spell repertoires and acquisition, line 55' and mr['mageOrdinaryKnownSpellRule']['source']==mr['mageOrdinaryCantripRule']['source'] and [(x['mageLevel'],x['newRankedSpells'],x['maximumRank']) for x in mr['mageOrdinaryKnownSpellRule']['acquisitionSchedule']]==[(1,2,1),(2,1,1),(3,1,2),(4,1,2),(5,1,3)],mr['mageOrdinaryKnownSpellRule'])
wiz_cantrips=w['cantripsKnown']
add('wizard-five-cantrips-at-acquisition-gates',len(wiz_cantrips)==5 and w['cantripCount']==5 and [x['acquiredClassLevel'] for x in wiz_cantrips]==[1,1,1,4,10] and all(x['rank']==0 and x['operationalStatus']=='operational-playtest-draft' for x in wiz_cantrips),wiz_cantrips)
add('floating-preparation-capacity',w['preparationCapacity']==23 and w['unusedPreparationCapacity']==1 and len(w['preparedMatrices'])==22 and 'capacity23; prepare22' in w['preparation'],{'capacity':w['preparationCapacity'],'prepared':len(w['preparedMatrices']),'unused':w['unusedPreparationCapacity']})
activity=w['casterActivity']
add('unravel-caster-own-budgets-and-history',activity['RPBefore']=={'current':64,'max':64} and activity['RPAfter']=={'current':38,'max':64} and activity['turnBudgets']['afterCast']['Action']=='spent: Unravel Identity' and activity['concentration'] is None and len(activity['castHistory'])==1 and activity['castHistory'][0]['RP']==26 and activity['castingFamilyHistory']==['unravel-identity first prepared matrix family'],activity)
helpers=[d['qualifiedActors'][x] for x in ['unravelCaster','mindBlankSuppressor','archDispelRemover']]
add('all-helper-profile-bindings',all(x['profileBinding']['profileId'].endswith('-254') and x['HP']['max']==104 and x['RP']['max']==64 and x['turnBudgets'] and x['castHistory'] and x['concentration'] is not None for x in helpers[1:]) and bool(helpers[0]['casterActivity']),{'profiles':[x['profileBinding']['profileId'] for x in helpers]})
target_pool=next(x for x in d['dependencyCallbackPlan'] if x.get('sourceId')=='mage.base.resonance-pool')
form_loss=next(x for x in d['dependencyCallbackPlan'] if x.get('source')=='NEW UI251-FORM-LOSS (spell-local only)')
familiar_lifecycle=next(x for x in d['dependencyCallbackPlan'] if x.get('source','').startswith('Conjure Elemental Familiar +'))
add('current-resource-and-familiar-callbacks','40/46' in target_pool['duringUnravel'] and 'RP40/46' in form_loss['recovery'] and 'original10:10:01Z' in familiar_lifecycle['duringUnravel'],{'pool':target_pool,'formLoss':form_loss,'familiar':familiar_lifecycle})
failed=[x for x in checks if not x['passed']]
binding=rawbind(P.relative_to(W).as_posix(),P.read_bytes())
audit={'id':'UNRAVEL-IDENTITY-MD196-B02-INTEGRATED-WITNESS-AUDIT-254','recordedAtUtc':'2026-10-30T12:37:00+00:00','status':'PASS_WITH_DIRECTOR_RULINGS_PENDING' if not failed else 'FAIL','checksPassed':len(checks)-len(failed),'checkCount':len(checks),'checksFailed':len(failed),'checks':checks,'failures':failed,'planBinding':binding,'pendingAuthority':{'reviewedApplied':812,'pending':36,'acceptedUnapplied':0,'remainingPendingIds':pending['pendingIds']},'decisionBoundary':'Independent data audit only. Unravel acceptance remains the GPT director decision requested by packet254; no acceptance/application is inferred and UI251-FORM-LOSS remains limited to the director-approved Unravel ruling.'}
A=B/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_254_AUDIT.json'
A.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(A),'status':audit['status'],'passed':audit['checksPassed'],'count':audit['checkCount'],'failed':failed,'planBinding':binding},ensure_ascii=False,indent=2))
