"""Independent source/fixture diagnostics. Returned Python is never imported or run.

This is an authored-example review, not a combat engine or gameplay test.
Diagnostic failures intentionally record corrections still required from GPT.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'rank7-identity-casting5-part5-correction-return-02'
OUT = A / 'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_74.json'

def read(p): return json.loads(p.read_bytes())
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def delta(a, b, path=''):
    if a == b: return []
    if isinstance(a, dict) and isinstance(b, dict):
        rows = []
        for k in a.keys() | b.keys():
            q = path + '/' + str(k)
            if k not in a or k not in b: rows.append(q)
            else: rows += delta(a[k], b[k], q)
        return sorted(rows)
    return [path]

def main():
    assert not OUT.exists(), 'Preserve an existing successful review; do not overwrite it.'
    m = read(P / 'MODEL.json'); cf = read(P / 'CASE_DISPOSITIONS.json')
    cases = cf['cases']; allcases = [x for c in cases for x in [c] + c['independentBranches']]
    by = {c['id']: c for c in allcases}
    checks = []
    def ck(name, actual, expected, basis=None):
        row = {'check': name, 'actual': actual, 'expected': expected, 'passed': actual == expected}
        if basis: row['basis'] = basis
        checks.append(row)
    def eq(name, actual, expected): ck(name, actual == expected, True, 'Complete objects compared, not hashes of abbreviated summaries.')
    def event(cid, index): return by[cid]['timeline'][index]
    def actor(cid, index, who, side='after'): return event(cid, index)[side]['actors'][who]
    def final(cid, who): return by[cid]['expectedFinalState']['actors'][who]
    sourcepaths = [R / 'data/public/class_playtests/wizard.json', R / 'data/public/class_playtests/mage.json',
        R / 'docs/mechanics/CLASS_PLAYTEST_RULES.md', R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
        R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',
        R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'data/director/feat_candidates/exact_01/cohorts/magic_core.json', R / 'data/director/spell_review/accepted_interface_registry_06.json', R / 'data/public/spell_playtests/catalog.json']
    protected = [p for p in P.rglob('*') if p.is_file()] + sourcepaths + [
        R / 'data/public/spell_playtests/authored_review_index.json',
        R / 'data/director/spell_review/remaining_work_queue_60.json',
        A / 'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK7_CORRECTIONS_73.json',
        A / 'PERTINENT_GPT_DECISIONS_2026_10_20_02.json']
    before = {p: digest(p) for p in protected}
    eq('Full case mirror', m['currentVectors'], cases)
    eq('Clock matrix mirror', m['clockMatrix'], read(P / 'CLOCK_AND_BODY_MATRIX.json')['clocks'])
    eq('Simulacrum field mirror', m['simulacrumFieldDisposition'], read(P / 'CLOCK_AND_BODY_MATRIX.json')['simulacrumFields'])
    eq('Conditional register mirror', m['conditionalBranchRegister'], read(P / 'HOLD_REGISTER.json')['conditionalBranches'])
    ck('Case inventory', [len(cases), len(allcases)-len(cases), len(m['conditionalBranchRegister'])], [10,39,11])
    sd = read(P / 'SPELL_DISPOSITIONS.json')['dispositions']
    for i, record in enumerate(m['records']):
        eq(record['spellId'] + ' full procedure mirror', record['proposedProcedure'], sd[i]['fullSelectedProcedure'])
        ck(record['spellId'] + ' risk remains C', record['riskTier'], 'C')

    # Each distinct full actor definition is checked once, retaining every location.
    unique = {}
    for c in allcases:
        for who, a in c['actorDefinitions'].items():
            key = hashlib.sha256(enc(a)).hexdigest()
            unique.setdefault(key, {'actor': a, 'locations': []})['locations'].append(c['id'] + '/' + who)
    classes = {n: read(R / ('data/public/class_playtests/' + n.lower() + '.json')) for n in ['Wizard','Mage']}
    for i, entry in enumerate(unique.values()):
        a = entry['actor']; cls = classes[a['class']]; tag = 'Distinct actor ' + str(i) + ' ' + entry['locations'][0]
        level = a['classLevel']; pb = 2 + (a['totalLevel'] - 1)//4; mod = (a['INT'] - 10)//2
        ck(tag + ' progression', [a['PB'], a['S'], a['maxRp'], a['maxRank'], a['Limit']],
            [pb, 1+(level>=5)+(level>=11)+(level>=17), cls['rpByClassLevel'][level-1], cls['maxSpellRankByClassLevel'][level-1], max(4,2+pb+mod)])
        ck(tag + ' HP and base spell stats', [a['maxHp'],a['spellAttack'],a['spellDc']], [8+12*6,pb+mod,8+pb+mod])
        saves = {k:(a[k]-10)//2 + (pb if k in ['INT','WIS'] else 0) for k in ['STR','DEX','CON','INT','WIS','CHA']}
        ck(tag + ' natural saves', a['saves'], saves)
        sourcecards = {v['id']:v for v in cls['cards']}
        selections = [x for row in a['selectedAcquisition'] for x in row['cards']]
        eq(tag + ' complete selected/automatic card provenance', selections+a['automaticCards'], [sourcecards[v['id']] for v in selections+a['automaticCards']])
        ck(tag + ' selected minimum levels', all(v['minimumClassLevel'] <= row['classLevel'] for row in a['selectedAcquisition'] for v in row['cards']), True)
        ck(tag + ' no duplicate selections', len({v['id'] for v in selections}), len(selections))
        schedule = {row['classLevel']:row for row in cls['schedule']}
        ck(tag + ' scheduled selection counts', [len(row['cards']) for row in a['selectedAcquisition']], [schedule[row['classLevel']]['choose'] for row in a['selectedAcquisition']])
        eq(tag + ' complete class engine', a['completeEngine'], cls['engine'])

    # Check complete serial states and every explicitly supplied roll independently.
    cadence = {'action','bonusAction','reaction','regularStart','nextRegularStart','counterRecharge','movementSpent','companionCommandUsed','companionOffenseUsed'}
    for c in allcases:
        previous = c['initialState']; gaps = []; bounds = []
        for i,e in enumerate(c['timeline']):
            for path in delta(previous,e['before']):
                if not (path.startswith('/actors/') and path.rsplit('/',1)[-1] in cadence): gaps.append([i,path])
            for side in ['before','after']:
                for who,a in e[side]['actors'].items():
                    if not (0 <= a['hp'] <= a['maxHp'] and 0 <= a['rp'] <= a['maxRp'] and a['tempHp'] >= 0): bounds.append([i,side,who])
            for name,v in e['rng'].items():
                tag = c['id'] + '/timeline/' + str(i) + '/rng/' + name
                if isinstance(v,dict) and all(k in v for k in ['natural','modifier','total']):
                    ck(tag + ' total', v['total'], v['natural']+v['modifier'])
                    ck(tag + ' natural d20', 1 <= v['natural'] <= 20, True)
                elif isinstance(v,list):
                    match = re.search(r'(\d+)d(\d+)', name)
                    if match:
                        n,sides = map(int,match.groups()); ck(tag + ' legal dice', len(v)==n and all(1<=face<=sides for face in v), True)
                    elif len(v)==3:
                        ck(tag + ' total',v[2],v[0]+v[1])
            previous = e['after']
        ck(c['id'] + ' unexplained non-cadence gaps',gaps,[])
        ck(c['id'] + ' actor resource bounds',bounds,[])
        eq(c['id'] + ' terminal state',previous,c['expectedFinalState'])

    # Independent arithmetic from source-qualified dice and save outcomes.
    damage_rows = [
        ('RIC5-01-A',1,'donor',24//2),('RIC5-01-A',1,'oldTarget',24),
        ('RIC5-01-A',4,'echoer',28//2),('RIC5-01-A',4,'newTarget',28),
        ('RIC5-01-A-c',2,'echoer',28//2),('RIC5-01-A-c',2,'newTarget',28),
        ('RIC5-01-A-g',3,'donor',6+7),('RIC5-02-A',1,'target',6),('RIC5-02-A',2,'target',5),
        ('RIC5-02-A-a',2,'target',6),('RIC5-02-B',2,'foe',28),('RIC5-02-B-a',1,'foe',28),
        ('RIC5-02-B-c',1,'foe',28+12),('RIC5-03-A',3,'protected',28),
        ('RIC5-03-A',3,'attacker',28//2),('RIC5-03-A',3,'observer',28//2),
        ('RIC5-04-A',0,'patient',4),('RIC5-04-A',4,'patient',6),('RIC5-04-A-b',0,'patient',4),
        ('RIC5-05-A',2,'foe',6)]
    for cid,ix,who,damage in damage_rows:
        b=actor(cid,ix,who,'before'); a=actor(cid,ix,who)
        ck(f'{cid}/{ix}/{who} damage and temporary HP', [a['hp'],a['tempHp']],
           [max(0,b['hp']-max(0,damage-b['tempHp'])),max(0,b['tempHp']-damage)])
    payments = [
        ('RIC5-01-A',2,'echoer',17),('RIC5-01-A',3,'echoer',5),('RIC5-01-A-c',1,'echoer',6),
        ('RIC5-01-A-d',1,'counterer',3),('RIC5-01-A-e',2,'counterer',3),
        ('RIC5-01-A-f',2,'echoer',17+3),('RIC5-01-A-g',1,'echoer',17+7),
        ('RIC5-01-B',2,'echoer',17),('RIC5-01-B',4,'echoer',5),('RIC5-01-B-f',2,'echoer',3),
        ('RIC5-02-B',1,'mage',5),('RIC5-02-B-c',0,'mage',5+2),
        ('RIC5-04-A',1,'caster',17),('RIC5-04-B-b',0,'caster',10),('RIC5-05-B',7,'creator',17)]
    for cid,ix,who,cost in payments:
        ck(f'{cid}/{ix}/{who} actual RP debit',actor(cid,ix,who,'before')['rp']-actor(cid,ix,who)['rp'],cost)
    ck('Cast Echo age inclusive boundary',round(18.1-0.1,8),18)
    ck('Cast Echo expired original is older than eighteen seconds',18.101-0.1>18,True)
    ck('Cast Echo rank9 bare conditional forecast',17+26,43)
    ck('Echo long cast full work',event('RIC5-01-A-f',3)['timeSeconds']-event('RIC5-01-A-f',2)['timeSeconds'],600)
    ck('Meta Reach target in modified range',math.dist([10,0,0],[40,0,0])<=10+30,True)
    ck('Meta target outside unmodified Ray range',math.dist([10,0,0],[40,0,0])>10,True)
    ck('Sculpt source outside Fireball sphere even with body extent',math.sqrt(17.5**2+17.5**2)>20,True)
    ck('Sequester pause elapsed',round(7.1-2.1,8),5)
    ck('Carrying pounds legal',170+10<=14*15,True)
    ck('Carrying Load reaches burden threshold',6+1>=14/2,True)
    ck('Sequester carrying spent only ten feet',10<=20,True)
    ck('Erase outsider outside observer radius',math.dist([10,0,0],[150,0,0])>120,True)
    ck('Erase does not restore independently deleted recent memory',
        [v['id'] for v in by['RIC5-03-B']['expectedFinalState']['privateMemories']['observer']['episodes']],['old'])
    ck('Self Simulacrum snapshots post-payment RP',by['RIC5-05-A']['expectedFinalState']['objects']['duplicate']['rp'],48-17)
    sim=by['RIC5-05-B']['expectedFinalState']
    ck('Replacement body retains derivative RP',sim['objects']['duplicate']['rp'],min(5,6))
    ck('Replacement body retains derivative Dissonance',sim['objects']['duplicate']['dissonance'],max(4,2))
    ck('Original donor RP independent',sim['actors']['donor']['rp'],6)
    ck('Replacement preserves derivative casting history',sim['objects']['duplicate']['lastSpell'],'resonance-shield')
    ck('Real lantern remains local and unheld', [sim['objects']['realLantern']['position'],sim['objects']['realLantern']['custodian']],[[10,0,0],None])
    ck('Independent Resonance Shield remains until its own ending',sim['actors']['creator']['tempHp'],4)
    ck('Ordinary zero ends finite duplicate',by['RIC5-05-B-c']['expectedFinalState']['objects']['duplicate']['state'],'ended')
    ck('Null zero retains disabled duplicate',by['RIC5-05-B-d']['expectedFinalState']['objects']['duplicate']['state'],'NullDisabled')

    # Concrete defects: use exact paths rather than treating prose as changed state.
    action_rows=[('RIC5-01-B',3,'enemy'),('RIC5-02-A',2,'mage'),('RIC5-04-A',3,'enemy'),
        ('RIC5-04-B',3,'carrier'),('RIC5-05-B',5,'creator'),('RIC5-05-B',7,'creator'),
        ('RIC5-02-B-a',1,'wizard'),('RIC5-04-B-b',0,'caster')]
    for cid,ix,who in action_rows:
        ck(f'{cid}/timeline/{ix}/after/actors/{who}/action actual Action consumed',actor(cid,ix,who)['action'],False,
           'CLASS_PLAYTEST_RULES.md lines11,15; event explicitly performs a successful Action after its regular START.')
    erase=final('RIC5-03-B-a','caster')
    ck('RIC5-03-B-a paid successful cast records last spell',erase['lastSpell'],'erase-from-reality')
    ck('RIC5-03-B-a prepared family spent', 'erase-from-reality' in erase['preparedFamiliesUsed'],True)
    adept=by['RIC5-02-B-a']['actorDefinitions']['wizard']
    ck('RIC5-02-B-a acquisition history grants claimed Metamagic Adept',
       any('metamagic' in str(v).lower() for v in adept['asiHistory'].values()),True,
       'The corrected class12 history must actually choose the feat instead of CHA+2; operational availability stays conditional.')

    old=read(A/'rank7-identity-casting5-part5-conference-return-01/MODEL.json')
    for key in ['records','selectedSharedRules','selectedQuestionDispositions','conditionalBranchRegister']:
        eq('Prior full authority retained: '+key,m[key],old[key])
    eq('Full worked-case evidence mirror',read(P/'evidence/worked_cases.json'),cases)
    eq('Full actor evidence mirror',read(P/'evidence/actor_profiles.json'),read(P/'ACTOR_FEATURE_ACCOUNTING.json')['profiles'])
    # Independent manual classification of all121 events; no returned audit used as authority.
    ordinary=[('01-A',0,'donor'),('01-A',2,'echoer'),('01-A-c',0,'echoer'),('01-A-d',0,'echoer'),
      ('01-A-e',0,'echoer'),('01-A-f',2,'echoer'),('01-A-g',0,'donor'),('01-A-g',1,'echoer'),
      ('01-B',0,'enemy'),('01-B',2,'echoer'),('01-B',3,'enemy'),('01-B-f',0,'echoer'),('01-B-f',1,'enemy'),
      ('02-A',0,'surger'),('02-A',1,'mage'),('02-A',2,'mage'),('02-A-a',0,'mage'),
      ('02-B',0,'surger'),('02-B',1,'mage'),('02-B-a',0,'wizard'),('02-B-a',1,'wizard'),('02-B-c',0,'mage'),
      ('03-A',0,'protected'),('03-A',2,'attacker'),('03-A-a',0,'protected'),('03-B',0,'caster'),('03-B',1,'subject'),('03-B-a',0,'caster'),
      ('04-A',0,'enemy'),('04-A',1,'caster'),('04-A',3,'enemy'),('04-A-a',0,'caster'),
      ('04-B',0,'caster'),('04-B',1,'carrier'),('04-B',3,'carrier'),('04-B-a',0,'carrier'),('04-B-b',0,'caster'),
      ('05-A',0,'creator'),('05-A-a',0,'creator'),('05-B',0,'creator'),('05-B',5,'creator'),('05-B',7,'creator'),('05-B-a',0,'creator'),('05-B-g',0,'creator')]
    ordinary=[('RIC5-'+cid,ix,who) for cid,ix,who in ordinary]
    ck('Independent ordinary Action inventory',len(ordinary),44)
    returned=read(P/'ACTION_AUDIT.json')
    eq('Returned classification independently agrees',sorted((v['caseId'],v['eventIndex'],who) for v in returned['events'] for who in v['ordinaryActionsCommitted']),sorted(ordinary))
    ck('Independent event inventory',sum(len(c['timeline']) for c in allcases),121)
    for cid,ix,who in ordinary:
        e=event(cid,ix);b=actor(cid,ix,who,'before');a=actor(cid,ix,who)
        ck(f'{cid}/{ix}/{who} legal available then spent Action',[b['action'],a['action']],[True,False])
        ck(f'{cid}/{ix}/{who} actual acting cadence bounds',b['regularStart']<=e['timeSeconds']<b['nextRegularStart'],True)
    for c in allcases:
        prev=c['initialState'];unearned=[];record_errors=[]
        for ix,e in enumerate(c['timeline']):
            starts={row['actor']:row for row in e.get('regularStartsBeforeEvent',[])}
            for who,row in starts.items():
                a=e['before']['actors'][who];before_actor=prev['actors'][who]
                if not (row['lastStart']==row['firstStart']+6*(row['count']-1) and row['firstStart']==before_actor['nextRegularStart'] and row['lastStart']<=e['timeSeconds'] and a['regularStart']==row['lastStart'] and a['nextRegularStart']==row['lastStart']+6 and a['action'] is True):
                    record_errors.append({'event':ix,'actor':who,'record':row})
            for who,b in e['before']['actors'].items():
                a=e['after']['actors'][who];prior=prev['actors'][who]
                if prior['action'] is False and b['action'] is True and who not in starts:unearned.append([ix,who,'before'])
                if b['action'] is False and a['action'] is True:unearned.append([ix,who,'after'])
            prev=e['after']
        ck(c['id']+' actual START sequence',record_errors,[])
        ck(c['id']+' no unearned Action restoration',unearned,[])
    feat=read(R/'data/director/feat_candidates/exact_01/cohorts/magic_core.json')['records'][21]
    for cid,who,points in [('RIC5-02-B-a','wizard',0),('RIC5-02-B-b','mage',2)]:
        a=by[cid]['actorDefinitions'][who];f=a['featAcquisition'];h=a['asiHistory']
        ck(cid+' legitimate feat milestone',[f['milestoneClassLevel'],f['totalCharacterLevelAtAcquisition'],a['classLevel']],[12,12,13])
        ck(cid+' milestone belongs to actual class',12 in classes[a['class']]['asiClassLevels'],True)
        ck(cid+' full final scores',[a[k] for k in ['STR','DEX','CON','INT','WIS','CHA']],[10,14,14,18,12,8])
        ck(cid+' declared advancement replaces CHA increase',h['rolledCHA']==8 and 'instead' in h['class12'] and 'Metamagic Adept' in h['class12'],True)
        ck(cid+' permanent modes and independent pool',[f['chosenModes'],f['permanentChoices'],f['poolMaximum'],f['poolAtAcquisition'],f['currentFixturePoints']],[['Reach','Sculpt'],True,2,2,points])
        eq(cid+' complete actual feat source',f['completeSourceRecordUnchanged'],feat)
        ck(cid+' operational approval remains false',[feat[k] for k in ['selectionEnabled','exactApproved','runtimeApproved']],[False]*3)
    neg=by['RIC5-02-B-b']
    eq('Rejected two-mode declaration preserves complete state',neg['initialState'],neg['expectedFinalState'])
    ma=neg['actorDefinitions']['mage']
    ck('Actual selected Mage5 Metaspell Access',any(v['id']=='mage.arch.metaspell-access' for row in ma['selectedAcquisition'] if row['classLevel']==5 for v in row['cards']),True)
    ck('Actual class mode is Sculpt','Sculpt' in ma['metaspellMode'],True)
    # Real first Erase and independent repeated-cast diagnostic, sourceWizard prepared family/Refrain engine.
    er=read(P/'NUMERICAL_STATE_EVIDENCE.json')['erase']
    eq('Erase corrected full first actor mirrors real case',er['correctedFirstAfter'],final('RIC5-03-B-a','caster'))
    first=er['correctedFirstAfter'];nb=er['nextCastBefore'];na=er['nextCastAfter']
    ck('Erase first history and actual cost',[first['rp'],first['dissonance'],first['refrain'],first['lastSpell'],first['preparedFamiliesUsed']],[48-17,0,0,'erase-from-reality',['erase-from-reality']])
    ck('Erase next lawful Action and same spent family',[nb['regularStart'],nb['nextRegularStart'],nb['action'],nb['rp'],nb['lastSpell'],nb['preparedFamiliesUsed']],[6,12,True,31,'erase-from-reality',['erase-from-reality']])
    ck('Erase repeated cast pays and incurs base plus Refrain',[na['rp'],na['dissonance'],na['refrain'],na['action'],na['lastSpell'],na['preparedFamiliesUsed']],[31-17,2+1,1,False,'erase-from-reality',['erase-from-reality']])
    # Three reported additional timing repairs, explicitly distinct from stale Ready deadline below.
    b=actor('RIC5-01-B-f',1,'enemy','before');a=actor('RIC5-01-B-f',1,'enemy')
    ck('Class Echo donor actual START3 then Action',[b['regularStart'],b['nextRegularStart'],b['action'],a['action']],[3,9,True,False])
    b=actor('RIC5-01-A-g',0,'donor','before');a=actor('RIC5-01-A-g',0,'donor')
    ck('Corpse Golem donor preceding real turn',[b['regularStart'],b['nextRegularStart'],b['action'],a['action'],b['rp']-a['rp']],[-6,0,True,False,7])
    ck('Donor START0 materialized once',sum(r['count'] for e in by['RIC5-01-A-g']['timeline'] for r in e.get('regularStartsBeforeEvent',[]) if r['actor']=='donor'),1)
    c=by['RIC5-02-A-a'];e=c['timeline'][2];b=e['before']['actors']['mage'];a=e['after']['actors']['mage']
    ck('Ready repaired actual cadence and release budget',[e['timeSeconds'],b['regularStart'],b['nextRegularStart'],b['action'],a['action'],b['reaction'],a['reaction'],e.get('regularStartsBeforeEvent')],[60.9,55,61,False,False,True,False,[]])
    ck('Ready release after Meta expiry but before own START',c['timeline'][1]['timeSeconds']<e['timeSeconds']<b['nextRegularStart'],True)
    deadline_locations=[]
    for ix,event_value in enumerate(c['timeline']):
        for side in ['before','after']:
            hold=event_value[side]['sourceLedger'].get('hold')
            if isinstance(hold,dict) and 'deadline' in hold:
                deadline_locations.append({'pointer':f'/currentVectors/2/independentBranches/0/timeline/{ix}/{side}/sourceLedger/hold/deadline','actual':hold['deadline'],'expected':61})
    hold=c['expectedFinalState']['sourceLedger']['hold']
    deadline_locations.append({'pointer':'/currentVectors/2/independentBranches/0/expectedFinalState/sourceLedger/hold/deadline','actual':hold['deadline'],'expected':61})
    ck('Ready all materialized deadlines equal actual next own START',[r['actual'] for r in deadline_locations],[61]*len(deadline_locations),'COMBAT_ACTION_PLAYTEST.md:99; existing ordinary Ready expires at next regular own-turn START. No global rule change.')
    boundary=[{'time':t,'lawfulBeforeActualStart':t<61,'storedDeadlinePredicate':t<hold['deadline']} for t in [60.9,61,61.1,62]]
    ck('Independent Ready legal boundary demonstration',[r['lawfulBeforeActualStart'] for r in boundary],[True,False,False,False])
    findings=[{'id':'RIC5-LOCAL74-01','priority':2,'status':'STATE_CORRECTION_REQUIRED','caseIds':['RIC5-02-A-a'],
      'title':'Ready state still stores deadline62 despite actual next regular START61',
      'evidence':{'locations':deadline_locations,'boundaryDiagnostic':boundary,'completeCase':c,
        'source':'COMBAT_ACTION_PLAYTEST.md:99','scope':'Stored authoring fixture mismatch; no production runtime executed. The amended release60.9 itself remains legal.'},
      'requestedCorrection':'Set the actual Ready deadline to61 in every current materialized hold and reconcile complete model/case/evidence/chapter mirrors. Keep original historical bytes, actual55/61 cadence, preparation56.1, Meta expiry60.5, release60.9, Action spent and existing Reaction debit, six damage, all other corrections and all procedures/settled choices. Supply exact reversible full-object changes and positive60.9/negative61 and61.1 boundary evidence. Do not extend Ready or rewrite historical inputs.'}]
    for p,h in before.items(): assert digest(p)==h,str(p)
    result={'id':'RANK7-IDENTITY-CASTING5-PART5-CORRECTION-SEMANTIC-REVIEW-74','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
      'verdict':'THREE_ORIGINAL_FINDINGS_RECONCILED_ONE_REMAINING_READY_STATE_CORRECTION_NOT_ACCEPTED',
      'package':info(A/'DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip'),'model':info(P/'MODEL.json'),'cases':info(P/'CASE_DISPOSITIONS.json'),
      'priorIntegrityReceipt':info(A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json'),
      'priorSemanticReceipt':info(A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json'),
      'reviewCoverage':{'semanticDeltaReview':True,'unchangedFullProcedures':5,'unchangedSharedRules':5,'unchangedQuestionDispositions':24,'mainCases':10,'independentBranches':39,'conditionalBranchesRetained':11,'events':121,'independentlyClassifiedOrdinaryActions':44,'uniqueFullActorDefinitionsChecked':len(unique),'scope':'Own source-derived data diagnostics and manual event/actor semantic review. Separate1057-check integrity report is not counted here.'},
      'priorFindingDispositions':[{'id':'RIC5-LOCAL68-01','status':'RECONCILED_WITH_EXISTING_FEAT_AVAILABILITY_QUALIFICATION'},{'id':'RIC5-LOCAL68-02','status':'RECONCILED_EIGHT_ACTION_DEBITS_AND_PROPAGATION'},{'id':'RIC5-LOCAL68-03','status':'RECONCILED_CAST_HISTORY_AND_REPEATED_CAST_EVIDENCE'}],
      'diagnosticChecks':checks,'diagnosticCheckCount':len(checks),'diagnosticFailures':sum(not c['passed'] for c in checks),'findings':findings,'findingsCount':len(findings),
      'independentActionClassification':[{'caseId':cid,'eventIndex':ix,'actor':who} for cid,ix,who in ordinary],
      'sourceBindings':[info(p) for p in sourcepaths],'protectedFilesChecked':len(before),'sourceInformationDeleted':0,'downloadedCodeExecuted':False,'canonicalChanges':0,
      'newAcceptedIdentities':0,'acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},
      'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproval':False,'cosmologyChanges':0,'releaseApproval':False,
      'nextConference':'One bounded deadline-field correction; submit only after currently active Rank8 history response finishes.'}
    OUT.write_bytes(enc(result))
    print(json.dumps({'review':info(OUT),'checks':len(checks),'failures':result['diagnosticFailures'],'findings':len(findings),'failedNames':[c['check'] for c in checks if not c['passed']]}))

if __name__ == '__main__': main()
