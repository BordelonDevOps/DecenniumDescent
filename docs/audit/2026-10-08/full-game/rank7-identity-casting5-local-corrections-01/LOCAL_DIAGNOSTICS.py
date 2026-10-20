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
P = A / 'rank7-identity-casting5-part5-conference-return-01'
OUT = A / 'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json'

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
        R / 'data/director/spell_review/accepted_interface_registry_06.json', R / 'data/public/spell_playtests/catalog.json']
    protected = [p for p in P.rglob('*') if p.is_file()] + sourcepaths + [
        R / 'data/public/spell_playtests/authored_review_index.json',
        R / 'data/director/spell_review/remaining_work_queue_54.json',
        A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RETURN_RANK8_DISPATCH_67.json',
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
       'All class4/8/12 choices are explicitly score increases; no independent feat source is supplied. Conditional feat availability does not free an already-spent advancement choice.')
    findings=[
        {'id':'RIC5-LOCAL68-01','priority':2,'status':'FIXTURE_CORRECTION_REQUIRED',
         'caseIds':['RIC5-02-B-a','RIC5-02-B-b'],'title':'Claimed Adept acquisition conflicts with the full advancement history',
         'evidence':{'positiveCasePointer':'/currentVectors/3/independentBranches/0','asiHistory':adept['asiHistory'],
           'legalMilestones':classes['Wizard']['asiClassLevels'],'source':'CHARACTER_CREATION_PLAYTEST.md:45; wizard.json and mage.json asiClassLevels',
           'observed':'Positive Wizard branch claims acquired Adept Sculpt at an eligible feat milestone, but all three reached milestones are spent on scores and the supplied actor says no extra feat. The negative two-provider branch inherits the same issue when claiming both providers genuinely acquired.'},
         'requestedCorrection':'Supply one internally consistent full acquisition fixture with actual chosen Adept modes, milestone and source. If one reached milestone becomes a feat, reconcile starting/final scores and dependent saves/stats. Do not grant a free bonus feat. Retain genuine external feat-operational availability qualification. For the negative branch, either bind legal both-provider ownership or label its provider predicate explicitly conditional without claiming a complete acquired actor.'},
        {'id':'RIC5-LOCAL68-02','priority':2,'status':'STATE_CORRECTION_REQUIRED',
         'caseIds':list(dict.fromkeys(row[0] for row in action_rows)),
         'title':'Eight successful Action events leave the remaining Action ledger true',
         'evidence':{'events':[{'caseId':cid,'timelineIndex':ix,'actor':who,'event':event(cid,ix)['event'],
             'beforeAction':actor(cid,ix,who,'before')['action'],'afterAction':actor(cid,ix,who)['action']} for cid,ix,who in action_rows],
             'budgetSemantics':cases[0]['budgetSemantics'],'source':'CLASS_PLAYTEST_RULES.md:11,15; each exact procedure/native source still spends an Action.'},
         'requestedCorrection':'Apply the real regular-START refresh before the event, then consume the successful Action once and carry false through intermediate/terminal states until a later real refresh. Repair all full case/model/chapter/specification mirrors. Audit other cadence-normalized events for the same defect. Do not change legal rejection cases or add an Action charge to a composite Cast Echo child or a Reaction-only release.'},
        {'id':'RIC5-LOCAL68-03','priority':2,'status':'STATE_CORRECTION_REQUIRED','caseIds':['RIC5-03-B-a'],
         'title':'Successful Erase observer-exclusion branch omits casting history',
         'evidence':{'pointer':'/currentVectors/5/independentBranches/0/expectedFinalState/actors/caster',
             'rp':erase['rp'],'action':erase['action'],'lastSpell':erase['lastSpell'],'preparedFamiliesUsed':erase['preparedFamiliesUsed'],
             'observed':'The caster pays17 and establishes protection on the willing subject; only the observer is excluded by a wall. lastSpell stays null and the used matrix-family list stays empty.'},
         'requestedCorrection':'Record actual erase-from-reality casting history and the spent prepared-family exemption at commitment in every mirror. Preserve zero base Dissonance for this real first prepared cast, the valid subject protection, and the excluded observer. This is not an illegal-cast refund case.'}
    ]
    for p,h in before.items(): assert digest(p)==h,str(p)
    result={'id':'RANK7-IDENTITY-CASTING5-PART5-SEMANTIC-REVIEW-68',
      'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'verdict':'REQUIRES_BOUNDED_CORRECTIONS_NOT_ACCEPTED',
      'package':info(A/'DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip'), 'model':info(P/'MODEL.json'),
      'cases':info(P/'CASE_DISPOSITIONS.json'), 'priorIntegrityReceipt':info(A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_LOCAL_PREFLIGHT.json'),
      'reviewCoverage':{'fullProceduresRead':5,'sharedRulesRead':5,'questionDispositionsRead':24,'mainCasesRead':10,
          'independentBranchesRead':39,'conditionalBranchesRetained':11,'uniqueFullActorDefinitionsChecked':len(unique),
          'scope':'Manual procedure/state review plus source-derived fixture diagnostics. Exact archive/reversible reconstruction remains the separate577-check receipt; those checks are not counted again here.'},
      'diagnosticChecks':checks,'diagnosticCheckCount':len(checks),'diagnosticFailures':sum(not c['passed'] for c in checks),
      'findings':findings,'findingsCount':len(findings),'sourceBindings':[info(p) for p in sourcepaths],
      'distinctActorLocations':[{'sha256':key,'locations':v['locations']} for key,v in unique.items()],
      'protectedFilesChecked':len(before),'sourceInformationDeleted':0,'downloadedCodeExecuted':False,'canonicalChanges':0,
      'newAcceptedIdentities':0,'acceptedButUnappliedUnchanged':39,
      'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},
      'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproval':False,'cosmologyChanges':0,'releaseApproval':False,
      'nextConference':'Prepare exact complete correction request; submit only after the currently active Rank8 correction response finishes.'}
    OUT.write_bytes(enc(result))
    print(json.dumps({'review':info(OUT),'checks':len(checks),'failures':result['diagnosticFailures'],'findings':len(findings),
       'failedNames':[c['check'] for c in checks if not c['passed']]}))

if __name__ == '__main__': main()
