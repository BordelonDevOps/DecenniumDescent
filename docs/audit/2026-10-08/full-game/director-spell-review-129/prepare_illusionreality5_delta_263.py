from __future__ import annotations
import copy, hashlib, json, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
FULL = ROOT / 'docs/audit/2026-10-08/full-game'
OUT = AUDIT / 'rank9_illusionreality5_delta_263_prepared'
ARCHIVE = OUT / 'DD_Rank9_SoulReflection_Delta_263.zip'
DELIVERY = OUT / 'DD_Rank9_SoulReflection_Delta_263_DELIVERY.json'
AUDIT_OUT = OUT / 'SOUL_REFLECTION_DELTA_263_INDEPENDENT_AUDIT.json'
SUBMISSION = OUT / 'SOUL_REFLECTION_DELTA_263_SUBMISSION.json'
CHAT = 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
AUTH = {'reviewedApplied': 814, 'pending': 34, 'acceptedUnapplied': 0, 'completeStandaloneProcedures': 538, 'scopedInterfaces': 173}
QUEUE = AUDIT / 'CURRENT_SPELL_QUEUE_262.json'
PENDING = AUDIT / 'CURRENT34_PENDING_IDENTITY_AUDIT_262.json'
HANDOFF = AUDIT / 'CURRENT_HANDOFF_262.json'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
LOW = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/candidate_low_rank_136.json'
LOW_RECEIPT = FULL / 'LOW_RANK_136_EXACT_FULFILLMENT.json'
RETURN = AUDIT / 'rank9_illusionreality5_return246_received'
RETURN_ZIP = RETURN / 'DD_Rank9_SoulReflection_Director_Return246_HELD.zip'
RETURN_DELIVERY = RETURN / 'DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'

def raw(p): return p.read_bytes()
def jread(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b) & 0xffffffff:08x}'
def bind(path, b): return {'path': path, 'bytes': len(b), 'sha256': sha(b), 'crc32': crc(b)}
def safe(s):
    p = PurePosixPath(s)
    return bool(s) and '\\' not in s and not p.is_absolute() and all(x not in ('', '.', '..') for x in p.parts)

def add_event(case, state, at, label, evidence, mutate):
    before = copy.deepcopy(state)
    mutate(state)
    after = copy.deepcopy(state)
    n = len(case['events']) + 1
    case['events'].append({
        'id': f"{case['id']}:{n}", 'atSeconds': at, 'label': label,
        'before': before, 'beforeSHA256': sha(canon(before)),
        'after': after, 'afterSHA256': sha(canon(after)),
        'forward': [{'op': 'test', 'path': '', 'value': before}, {'op': 'replace', 'path': '', 'value': after}],
        'inverse': [{'op': 'test', 'path': '', 'value': after}, {'op': 'replace', 'path': '', 'value': before}],
        'evidence': evidence,
    })

def make_case(case_id, title, state, qualification, source_ids):
    return {'id': case_id, 'title': title, 'spellId': 'soul-reflection', 'kind': 'bounded-static-proposal-trace',
            'caseStatus': 'PROPOSAL_TRACE_NOT_ACCEPTANCE', 'qualification': qualification,
            'sourceIds': source_ids, 'initialState': copy.deepcopy(state), 'initialSHA256': sha(canon(state)),
            'events': [], 'requirementsDemonstrated': [], 'requirementsHeld': [], 'finalState': None, 'finalSHA256': None}

def seal_case(case, state):
    case['finalState'] = copy.deepcopy(state)
    case['finalSHA256'] = sha(canon(state))
    return case

def main():
    if OUT.exists(): raise FileExistsError(f'Refusing to overwrite {OUT}')
    queue, pending, handoff, index = map(jread, (QUEUE, PENDING, HANDOFF, INDEX))
    assert queue['currentAuthority'] == AUTH and pending['authority'] == AUTH and handoff['authority'] == AUTH
    assert queue['next']['identity'] == 'soul-reflection' and queue['next']['blocker'] == 'IR207-B02'
    assert queue['currentIndexBinding']['sha256'] == sha(raw(INDEX))
    index_entry = next(x for x in index['entries'] if x['id'] == 'gaseous-form')
    ray_entry = next(x for x in index['entries'] if x['id'] == 'ray-of-frost')
    assert index_entry['procedureFile'] == 'candidate_low_rank_136.json'
    assert index_entry['procedurePointer'] == '/spells/132/operationalCandidate'
    low = jread(LOW); gas = low['spells'][132]
    assert gas['id'] == 'gaseous-form' and gas['status'] == 'reviewed-authored-operational-playtest'
    assert gas['operationalCandidate']['duration'] == 'Concentration, up to 1 minute.'
    assert gas['operationalCandidate']['numericParameters']['seconds'] == 60
    assert ray_entry['procedureFile'] == 'catalog.json' and ray_entry['procedurePointer'] == '/spells/411/operational'
    ray = jread(CATALOG)['spells'][411]['operational']
    assert ray['id'] == 'ray-of-frost' and ray['rangeFeet'] == 10 and '1d8 cold damage' in ray['resolution']
    fulfillment = jread(LOW_RECEIPT)
    assert fulfillment['status'].startswith('fulfilled') and fulfillment['finalReplyId'] == gas['reviewEvidence']['finalReplyId']

    with zipfile.ZipFile(RETURN_ZIP) as z:
        prior_manifest = json.loads(z.read('MEMBER_MANIFEST.json'))
        prior_names = set(z.namelist())
        prior_required = ['MEMBER_MANIFEST.json', 'DIRECTOR_DECISION.json', 'HOLD_REGISTER.json', 'PROCEDURE.json', 'SOURCE_REASSESSMENT.json',
                          'CASE_AND_FUTURE_DISPOSITIONS.json', 'CASE_REPLAY.json', 'CLOCK_RESOURCE_CUSTODY_RESULTS.json',
                          'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json', 'prior/ACTOR_PROFILES.json',
                          'cases/RANK9ILLUSIONREALITY5129-SOUL-REFLECTION-A__suppression-resumption.json']
        assert all(n in prior_names for n in prior_required)
        old = {n: z.read(n) for n in prior_required}
        old_decision = json.loads(old['DIRECTOR_DECISION.json'])
        assert old_decision['perIdentity'][0]['blockerIds'] == ['IR207-B02'] and old_decision['heldIds'] == ['soul-reflection']
        source_case = json.loads(old['cases/RANK9ILLUSIONREALITY5129-SOUL-REFLECTION-A__suppression-resumption.json'])
        source_case_hash = sha(old['cases/RANK9ILLUSIONREALITY5129-SOUL-REFLECTION-A__suppression-resumption.json'])
        actor_profiles = json.loads(old['prior/ACTOR_PROFILES.json'])
        assert 'W17-IR207' in actor_profiles and actor_profiles['W17-IR207']['campaignExistenceVerified'] is False
        template = json.loads(z.read('cases/RANK9ILLUSIONREALITY5129-SOUL-REFLECTION-A.json'))
        base = copy.deepcopy(template['initialState'])
        reflection_template = copy.deepcopy(template['events'][2]['after']['actors']['R1'])

    # All cases are conditional static fixtures. Full source-built actor states are retained;
    # the new Soul-Reflection copy/termination decisions remain explicitly proposed.
    def initial(case_id):
        s = copy.deepcopy(base)
        s['caseId'] = case_id
        s['currentAuthority'] = copy.deepcopy(AUTH)
        s['actors'] = {k: copy.deepcopy(base['actors'][k]) for k in ('A', 'D', 'T')}
        s['proposalStatus'] = 'UNACCEPTED_DIRECTOR_ADJUDICATION_REQUIRED'
        s['chronology'] = []
        return s
    def sr_cast(s, t=0.1):
        a = s['actors']['A']; a['rp'] -= 26; a['action'] = 0; a['lastSpell'] = 'soul-reflection'
        a['castFamilies'] = list(a.get('castFamilies', [])) + ['soul-reflection']
        a['castHistory'] = list(a.get('castHistory', [])) + [f'A-SR-{s["caseId"]}']
        s['effects'][f'A-SR-{s["caseId"]}'] = {'kind':'soul-reflection','owner':'A','target':'T','createdAt':t,
            'deadlineAt':18.0,'active':True,'reflectionId':'R1','phaseMarkers':[5.91,11.91,17.91],
            'scheduleRule':'NEW proposed target-END markers; no target/caster refresh'}
        r = copy.deepcopy(reflection_template); r['id'] = 'R1'; r['profileId'] = 'W17-IR207'
        r['hp'] = s['actors']['T']['hp']; r['maxHP'] = s['actors']['T']['maxHP']; r['rp'] = s['actors']['T']['rp']; r['rpMax'] = s['actors']['T']['rp']
        r['finiteOriginalResourceSnapshot'] = {'sourceActor':'T','currentRP':s['actors']['T']['rp'],'sourceProfile':'W17-IR207','campaignExistenceVerified':False}
        r['position'] = [15,0,0]; r['active'] = True; r['life'] = 'Alive'
        s['actors']['R1'] = r
    def start_turn(a, t):
        a['activeRegular'] = True; a['action'] = 1; a['bonusAction'] = 1; a['interaction'] = 1
        a['lastRegularStart'] = t; a['nextRegularStart'] = t + 6
        a['regularStarts'] = list(a.get('regularStarts', [])) + [t]
    def end_turn(a, t):
        a['activeRegular'] = False; a['lastRegularEnd'] = t
        a['regularEnds'] = list(a.get('regularEnds', [])) + [t]

    # 1: target already in an exact source-backed Gaseous Form when reflected;
    # expiry/reversion is explicitly the proposed Soul-Reflection snapshot rule.
    cid = 'RANK9ILLUSIONREALITY5263-SOUL-REFLECTION-FORM'
    s = initial(cid); s['formRecords'] = {}; s['copiedForms'] = {}; s['reflectionPhases'] = []
    c = make_case(cid, 'W17 target in source-backed Gaseous Form through source expiry', s,
        'W17 is a conditional source-built fixture, not a campaign actor. Gas mechanics are source facts; reflected form/deadline and its reversion are NEW local proposals.',
        ['GASEOUS_FORM_INDEXED_ENVELOPE', 'W17-IR207', 'IR207-B02'])
    def gas_cast(st):
        t = st['actors']['T']; t['rp'] -= 5; t['action'] = 0; t['lastSpell'] = 'gaseous-form'
        t['castHistory'] = list(t.get('castHistory', [])) + ['T-GAS-263']
        t['concentration'] = {'spellId':'gaseous-form','sourceId':'T-GAS-263','startedAt':-52.0,'deadlineAt':8.0}
        st['formRecords']['T'] = {'form':'gaseous-mist','rootProfile':'W17-IR207','rootIdentity':'T','sourceId':'T-GAS-263',
            'startAt':-52.0,'deadlineAt':8.0,'currentHP':t['hp'],'maxHP':t['maxHP'],'currentRP':t['rp'],
            'size':'Medium','spaceFeet':[5,5,6],'movementFeet':10,'hover':True,'voiceUsable':False,'handsUsable':False,
            'attacksUsable':False,'gearState':'real, melded, unavailable; original owner/custodian preserved'}
        st['chronology'].append({'at':-52.0,'event':'T commits source-backed Gaseous Form; 5 RP; concentration deadline t=8'})
    add_event(c,s,-52.0,'T casts reviewed Gaseous Form; remaining duration at encounter is 8 seconds',
        {'source':'candidate_low_rank_136.json /spells/132/operationalCandidate','fixture':'self is a willing Medium target; W17 source-built acquisition and preparation'},gas_cast)
    def encounter(st):
        start_turn(st['actors']['A'],0.0)
        st['chronology'].append({'at':0.0,'event':'bounded encounter begins; A starts regular turn; T has 8 seconds of actual form duration remaining'})
    add_event(c,s,0.0,'Encounter starts with form source clock still running',{'source':'bounded elapsed-time fixture; no campaign existence claim'},encounter)
    add_event(c,s,0.1,'A commits Soul Reflection on T',{'source':'native catalog row plus proposed operational procedure'},lambda st:sr_cast(st))
    def admission(st):
        st['copiedForms']['R1'] = {'sourceFormOwner':'T','sourceId':'T-GAS-263','sourceDeadlineAt':8.0,
            'copyMode':'NEW snapshot inherits only remaining form marker; no second concentration slot or new source deadline',
            'rootProfile':'W17-IR207','sameSizeSpace':True,'gasLimitationsPreserved':True}
        st['effects'][f'A-SR-{cid}']['admittedAt'] = 0.11
        st['chronology'].append({'at':0.11,'event':'R1 admitted from current W17/form snapshot; finite RP snapshot 59'})
    add_event(c,s,0.11,'R1 admission snapshots T gas form and finite post-form RP',{'source':'NEW Soul-Reflection-local copy rule proposal'},admission)
    add_event(c,s,0.9,'A regular END 1',{'source':'actual A regular END; no extra caster turn'},lambda st:end_turn(st['actors']['A'],0.9))
    def tstart(st): start_turn(st['actors']['T'],5.0); st['chronology'].append({'at':5.0,'event':'T regular start; no independent phase added'})
    add_event(c,s,5.0,'T regular turn starts at its actual fixture marker',{'source':'bounded initiative offset; source form prevents V/S/gear use'},tstart)
    def dodge(st): st['actors']['T']['action']=0; st['chronology'].append({'at':5.1,'event':'T chooses legal Dodge; no V/S cast, attack, or new resource spend'})
    add_event(c,s,5.1,'First hard Action component does not force an illegal spell through Gaseous Form',{'source':'Gaseous Form limitations; proposed first-Action choice'},dodge)
    add_event(c,s,5.9,'T regular END 1',{'source':'actual original target END marker'},lambda st:end_turn(st['actors']['T'],5.9))
    def phase1(st): st['reflectionPhases'].append({'index':1,'startAt':5.91,'ownerMarker':'T regular END 5.9','action':'Dodge','startingActionBudget':1,'independentTargetTurn':False})
    add_event(c,s,5.91,'Reflection phase 1 follows T END without refreshing T',{'source':'NEW proposed schedule; existing companion timing rules used only as clock boundary'},phase1)
    add_event(c,s,6.0,'A regular start 2',{'source':'actual A regular start; no Reflection refresh'},lambda st:start_turn(st['actors']['A'],6.0))
    add_event(c,s,6.9,'A regular END 2',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],6.9))
    def gas_end(st):
        st['actors']['T']['concentration']=None; st['formRecords']['T']['endedAt']=8.0; st['formRecords']['T']['ending']='source concentration deadline'
        st['copiedForms']['R1']['endedAt']=8.0; st['copiedForms']['R1']['ending']='NEW inherited source deadline; revert to same copied root identity'
        st['chronology'].append({'at':8.0,'event':'T source form ends; proposed R1 form snapshot ends; neither HP nor RP resets'})
    add_event(c,s,8.0,'Exact form deadline ends source form and proposed reflected snapshot',{'source':'Gaseous Form 60-second concentration clock; local copy/reversion rule remains proposed'},gas_end)
    add_event(c,s,11.0,'T regular start 2 after reversion',{'source':'actual original target regular marker'},lambda st:start_turn(st['actors']['T'],11.0))
    add_event(c,s,11.9,'T regular END 2',{'source':'actual original target END marker'},lambda st:end_turn(st['actors']['T'],11.9))
    def phase2(st): st['reflectionPhases'].append({'index':2,'startAt':11.91,'ownerMarker':'T regular END 11.9','form':'root W17 profile','action':'Dodge','startingActionBudget':1,'independentTargetTurn':False})
    add_event(c,s,11.91,'Reflection phase 2 uses restored copied root form',{'source':'NEW proposed schedule and form-copy rule'},phase2)
    add_event(c,s,12.0,'A regular start 3',{'source':'actual A regular start; no Reflection refresh'},lambda st:start_turn(st['actors']['A'],12.0))
    add_event(c,s,12.9,'A regular END 3',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],12.9))
    add_event(c,s,17.0,'T regular start 3',{'source':'actual original target regular marker'},lambda st:start_turn(st['actors']['T'],17.0))
    add_event(c,s,17.9,'T regular END 3',{'source':'actual original target END marker'},lambda st:end_turn(st['actors']['T'],17.9))
    def phase3(st): st['reflectionPhases'].append({'index':3,'startAt':17.91,'ownerMarker':'T regular END 17.9','form':'root W17 profile','action':'Dodge','startingActionBudget':1,'independentTargetTurn':False})
    add_event(c,s,17.91,'Reflection phase 3 completes three source target-END markers',{'source':'NEW proposed schedule'},phase3)
    def fend(st):
        st['effects'][f'A-SR-{cid}']['active']=False; st['effects'][f'A-SR-{cid}']['endedAt']=18.0
        st['actors']['R1']['active']=False; st['actors']['R1']['life']='FiniteEnded'
        st['chronology'].append({'at':18.0,'event':'R1 finite body ends without corpse, loot, or restoration of original target state'})
    add_event(c,s,18.0,'Finite Reflection ends after third phase',{'source':'NEW proposed Soul-Reflection termination rule'},fend)
    c['requirementsDemonstrated']=['Exact Gaseous Form source and legal W17 route','source deadline, current HP/RP, voice/hand/attack and melded-gear limits','No additional target or caster turn in reflection phases']
    c['requirementsHeld']=['Reflected-form copy/reversion remains NEW; director acceptance required','No source-qualified attached/no-phase recipient established']
    seal_case(c,s); form_case=c

    # 2: a lawfully copied, finite concentration operation ends on a source-pipeline damage save.
    cid='RANK9ILLUSIONREALITY5263-SOUL-REFLECTION-CONCENTRATION'
    s=initial(cid); s['reflectionPhases']=[]; s['copiedConcentration']={}; s['formRecords']={}
    c=make_case(cid,'Copied Gaseous Form concentration interruption',s,
        'A proposed Soul-Reflection permission/copy rule is exercised with a complete accepted Gaseous Form procedure; trace is not itself acceptance.',
        ['GASEOUS_FORM_INDEXED_ENVELOPE','W17-IR207','CLASS_PLAYTEST_RULES','IR207-B02'])
    add_event(c,s,0.1,'A commits Soul Reflection on normal-form T',{'source':'current W17 fixture; Soul Reflection mechanics remain proposed'},lambda st:sr_cast(st))
    add_event(c,s,0.11,'R1 is admitted with current finite repertoire/resource snapshot',{'source':'NEW Q26/Q29-equivalent local proposal'},lambda st:st['chronology'].append({'at':0.11,'event':'R1 snapshot; current RP64, Gaseous Form in acquired/prepared book'}))
    add_event(c,s,0.9,'A regular END 1',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],0.9))
    add_event(c,s,5.0,'T regular start',{'source':'bounded initiative fixture'},lambda st:start_turn(st['actors']['T'],5.0))
    add_event(c,s,5.1,'T spends its single initial compelled Action on Dodge',{'source':'proposed one-Action hard component'},lambda st:st['actors']['T'].__setitem__('action',0))
    add_event(c,s,5.9,'T regular END 1',{'source':'actual target END marker'},lambda st:end_turn(st['actors']['T'],5.9))
    def cast_gas(st):
        r=st['actors']['R1']; r['rp']-=5; r['action']=0; r['lastSpell']='gaseous-form'; r['concentration']={'spellId':'gaseous-form','sourceId':'R1-GAS-263','startedAt':5.91,'deadlineAt':65.91}
        st['formRecords']['R1']={'form':'gaseous-mist','rootProfile':'W17-IR207','rootIdentity':'R1','sourceId':'R1-GAS-263',
            'startAt':5.91,'deadlineAt':65.91,'currentHP':r['hp'],'maxHP':r['maxHP'],'currentRP':59,'size':'Medium',
            'movementFeet':10,'hover':True,'voiceUsable':False,'handsUsable':False,'attacksUsable':False}
        st['copiedConcentration']['R1']={'spellId':'gaseous-form','sourceId':'R1-GAS-263','RPBefore':64,'RPAfter':59,'deadlineAt':65.91,'slotOwner':'R1','status':'active'}
        st['reflectionPhases'].append({'index':1,'startAt':5.91,'ownerMarker':'T END 5.9','action':'cast self-target Gaseous Form','costRP':5})
    add_event(c,s,5.91,'R1 uses one source-qualified copied action to cast Gaseous Form on itself',{'source':'NEW local copy/permission rule; source card supplies actual spell target/cost/duration/component constraints'},cast_gas)
    add_event(c,s,6.0,'A regular start 2',{'source':'actual A regular start; no Reflection refresh'},lambda st:start_turn(st['actors']['A'],6.0))
    add_event(c,s,6.9,'A regular END 2',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],6.9))
    add_event(c,s,11.0,'T regular start 2',{'source':'actual T regular marker; no reflection refresh'},lambda st:start_turn(st['actors']['T'],11.0))
    def bolt(st):
        t=st['actors']['T']; r=st['actors']['R1']; t['rp']-=1; t['action']=0; t['lastSpell']='wizard.base.arcane-bolt'
        hit={'attackRoll':10,'spellAttack':11,'total':21,'targetAC':r['AC'],'hit':True,'rawForce':9,'forceResistance':True,'resolvedDamage':4}
        st.setdefault('damageEvents',[]).append({'id':'R1-GAS-INTERRUPTION-263',**hit}); r['hp']-=4
        save={'save':'CON','roll':1,'modifier':2,'total':3,'DC':10,'success':False,'cause':'4 resolved damage; max(10,floor(4/2))'}
        st['copiedConcentration']['R1'].update({'damageAt':11.1,'concentrationSave':save,'status':'ended-on-failed-save','endedAt':11.1})
        r['concentration']=None; st['formRecords']['R1'].update({'endedAt':11.1,'ending':'failed CON save','currentHP':100,'currentRP':59})
        st['chronology'].append({'at':11.1,'event':'R1 reverts at same location with HP100; RP59 unchanged after paid form'})
    add_event(c,s,11.1,'T Arcane Bolt causes the actual Gaseous Form concentration save to fail',{'source':'W17 Wizard Arcane Bolt and force resistance; CLASS_PLAYTEST_RULES concentration rule; stipulated d20 roll'},bolt)
    add_event(c,s,11.9,'T regular END 2',{'source':'actual T regular END'},lambda st:end_turn(st['actors']['T'],11.9))
    add_event(c,s,11.91,'R1 reflection phase 2 uses restored root form after T END',{'source':'NEW proposed schedule; no new target or caster turn'},lambda st:st['reflectionPhases'].append({'index':2,'startAt':11.91,'ownerMarker':'T END 11.9','form':'root W17','action':'Dodge','startingActionBudget':1,'independentTargetTurn':False}))
    add_event(c,s,12.0,'A regular start 3',{'source':'actual A regular start; no Reflection refresh'},lambda st:start_turn(st['actors']['A'],12.0))
    add_event(c,s,12.9,'A regular END 3',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],12.9))
    add_event(c,s,17.0,'T regular start 3',{'source':'actual T regular start'},lambda st:start_turn(st['actors']['T'],17.0))
    add_event(c,s,17.9,'T regular END 3',{'source':'actual T regular END'},lambda st:end_turn(st['actors']['T'],17.9))
    add_event(c,s,17.91,'R1 completes its third proposed phase after T END 17.9',{'source':'NEW schedule proposal'},lambda st:st['reflectionPhases'].append({'index':3,'startAt':17.91,'ownerMarker':'T END 17.9','action':'Dodge'}))
    def cend(st): st['effects'][f'A-SR-{cid}']['active']=False; st['effects'][f'A-SR-{cid}']['endedAt']=18.0; st['actors']['R1']['active']=False; st['actors']['R1']['life']='FiniteEnded'
    add_event(c,s,18.0,'Soul Reflection finite opponent ends; original and copied resource histories remain distinct',{'source':'NEW termination proposal'},cend)
    c['requirementsDemonstrated']=['Gaseous Form source concentration, finite cost and legal target','source damage→CON save→concentration ending; reflection retains current HP and spent RP','Original target costs and body remain separate']
    c['requirementsHeld']=['Whether Soul Reflection may grant autonomous copied casting/action remains a director ruling','Source does not independently grant R1 spell repertoire or resource pool']
    seal_case(c,s); conc_case=c

    # 3: positive-to-zero damage and ordinary death-save schedule are resolved before opponent cleanup.
    cid='RANK9ILLUSIONREALITY5263-SOUL-REFLECTION-ORIGINAL-ZERO'
    s=initial(cid); s['actors']['T']['hp']=1; s['actors']['T']['deathSaves']={'successes':0,'failures':0}; s['actors']['T']['wounds']=[]
    s['damageEvents']=[]; s['reflectionPhases']=[]
    c=make_case(cid,'Original target reaches zero and survives Reflection cleanup',s,
        'Conditional W17 fixture at 1 HP. Damage, Wound-save and death-save resolution use exact source order; reflection termination is proposed.',
        ['RAY_OF_FROST_INDEXED_OPERATION','CORE_RESOLUTION_PLAYTEST','HEALING_DEATH_PLAYTEST','IR207-B02'])
    add_event(c,s,0.0,'A begins the regular turn used for the cast',{'source':'bounded initiative fixture'},lambda st:start_turn(st['actors']['A'],0.0))
    add_event(c,s,0.1,'A commits Soul Reflection on T',{'source':'current authority 814/34/0; pending identity not accepted'},lambda st:sr_cast(st))
    add_event(c,s,0.11,'R1 admission snapshots T at 1/104 HP; no health refill',{'source':'NEW finite current-HP snapshot proposal'},lambda st:st['chronology'].append({'at':0.11,'event':'R1 inherits finite profile; no healing or HP reset'}))
    add_event(c,s,0.9,'A regular END 1',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],0.9))
    add_event(c,s,5.0,'T regular start 1',{'source':'bounded regular marker'},lambda st:start_turn(st['actors']['T'],5.0))
    add_event(c,s,5.1,'T chooses legal Dodge; no copied or original resource is spent',{'source':'proposed one-Action hard component; W17 actor state'},lambda st:st['actors']['T'].__setitem__('action',0))
    add_event(c,s,5.9,'T regular END 1',{'source':'regular target END'},lambda st:end_turn(st['actors']['T'],5.9))
    def zero(st):
        r=st['actors']['R1']; t=st['actors']['T']; r['action']=0
        st['damageEvents'].append({'at':5.91,'source':'R1 copied Ray of Frost (proposed copy permission)','rangeFeet':10,'distanceFeet':5,'attackRoll':10,'spellAttack':11,'targetAC':12,'hit':True,
            'damageRoll':1,'damageType':'cold','preHP':1,'resolvedDamage':1,'postTempDamage':1,'actualHPDamage':1,'postHP':0,
            'instantDeath':False,'positiveToZero':True,'woundSave':{'CONRoll':8,'modifier':2,'total':10,'DC':10,'success':True,'woundsAfter':[]},
            'lifeAfter':'Downed','deathSaveFailures':0,'deathSaveSuccesses':0})
        st.setdefault('spellRiders',{})['R1-RAYFROST-SLOW-263']={'owner':'R1','target':'T','speedReductionFeet':10,'appliedAt':5.91,'expiresAt':11.9,'status':'active until T next actual regular END'}
        t['hp']=0; t['life']='Downed'; t['wounds']=[]; t['deathSaves']={'successes':0,'failures':0}
        st['effects'][f'A-SR-{cid}'].update({'active':False,'endedAt':5.92,'ending':'original target reached 0 after complete source damage/life-state pipeline'})
        r['active']=False; r['life']='FiniteEnded'; st['chronology'].append({'at':5.92,'event':'R1 ends after source consequences; T inventory/owner/HP/Wounds/death state preserved'})
    add_event(c,s,5.91,'R1 damage resolves original T to zero; Wound save succeeds before finite reflection ends',{'source':'reviewed Ray of Frost operation + CORE_RESOLUTION_PLAYTEST ordering; copied action remains proposed'},zero)
    add_event(c,s,6.0,'A regular start 2 after Reflection ended',{'source':'actual A regular start; no reflection exists'},lambda st:start_turn(st['actors']['A'],6.0))
    add_event(c,s,6.9,'A regular END 2',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],6.9))
    def death_save(st):
        t=st['actors']['T']; t['activeRegular']=True; t['lastRegularStart']=11.0; t['nextRegularStart']=17.0
        t['regularStarts']=list(t.get('regularStarts',[]))+[11.0]; t['deathSaves']={'successes':1,'failures':0}; t['life']='Downed'; t['action']=0
    add_event(c,s,11.0,'T next actual regular start resolves one death save with no reflection turn',{'source':'CORE_RESOLUTION_PLAYTEST: dying character rolls at each regular start'},death_save)
    def end_target_clock(st):
        end_turn(st['actors']['T'],11.9); st['spellRiders']['R1-RAYFROST-SLOW-263'].update({'status':'expired','endedAt':11.9})
    add_event(c,s,11.9,'T regular END expires the source Ray of Frost rider',{'source':'catalog.json /spells/411/operational; actual target regular END'},end_target_clock)
    add_event(c,s,12.0,'A regular start 3',{'source':'actual A regular start'},lambda st:start_turn(st['actors']['A'],12.0))
    add_event(c,s,12.9,'A regular END 3',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],12.9))
    c['requirementsDemonstrated']=['Original, not reflection, receives 1 actual cold damage to zero','Wound save and Downed state resolved before opponent cleanup','Later death save occurs only at T actual regular start; original identity/inventory persist']
    c['requirementsHeld']=['Copied Ray of Frost permission and finite reflection action require director acceptance','No actual death branch is claimed; this is the source-defined zero-HP alternative']
    seal_case(c,s); zero_case=c

    # 4: finite original target-owned map is handed to R1, drops on suppression, stays at that location on resume/end.
    cid='RANK9ILLUSIONREALITY5263-SOUL-REFLECTION-CARGO'
    s=initial(cid); s['cargoTrace']={'itemId':'T-map','events':[]}; s['cargoPhaseSource']={'caseId':source_case['id'],'archiveMember':'cases/RANK9ILLUSIONREALITY5129-SOUL-REFLECTION-A__suppression-resumption.json','sha256':source_case_hash}
    item=copy.deepcopy(s['items']['T-map']); item.update({'owner':'T','custodian':'T','held':True,'position':[10,0,0],'temporary':False})
    s['items']['T-map']=item; s['actors']['T']['hands']['right']='T-map'
    c=make_case(cid,'One actual original map transferred to Reflection and settled through suppression/resumption/end',s,
        'The item transfer is an authorized finite encounter fact. Drop/retention is a NEW Soul-Reflection-local cargo rule; copied gear remains separate.',
        ['W17-IR207-A-map','COMBAT_ACTION_PLAYTEST','RETURN246_SUPPRESSION_CASE','AC5_ANTIMAGIC_FIELD_LESSER','IR207-B02'])
    add_event(c,s,0.0,'A begins its regular turn',{'source':'bounded initiative fixture'},lambda st:start_turn(st['actors']['A'],0.0))
    add_event(c,s,0.1,'A commits Soul Reflection on T',{'source':'bounded actor/location fixture'},lambda st:sr_cast(st))
    def admit(st): st['actors']['R1']=copy.deepcopy(reflection_template); st['actors']['R1']['id']='R1'; st['actors']['R1']['position']=[15,0,0]; st['actors']['R1']['active']=True
    def admit_cargo(st):
        admit(st); st['effects'][f'A-SR-{cid}']['phaseMarkers']=[1.91,7.91,13.91]; st['effects'][f'A-SR-{cid}']['deadlineAt']=13.94; st['effects'][f'A-SR-{cid}']['endingAt']=13.94
    add_event(c,s,0.11,'R1 appears within five feet of T; temporary copied gear omits T-map',{'source':'prior Return246 bound case; exact T-map item remains original'},admit_cargo)
    add_event(c,s,0.9,'A regular END 1',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],0.9))
    add_event(c,s,1.0,'T regular start',{'source':'bounded fixture; normal one interaction remains'},lambda st:start_turn(st['actors']['T'],1.0))
    add_event(c,s,1.1,'T uses its single compelled Action to Dodge; one free object interaction remains',{'source':'COMBAT_ACTION_PLAYTEST; proposed one-Action control component'},lambda st:st['actors']['T'].__setitem__('action',0))
    def handoff(st):
        t=st['actors']['T']; r=st['actors']['R1']; it=st['items']['T-map']
        t['interaction']=0; t['hands']['right']=None; t['inventory'].remove('T-map')
        r['hands']['right']='T-map'; r['inventory'].append('T-map')
        it.update({'custodian':'R1','held':True,'position':[15,0,0]})
        st['cargoTrace']['events'].append({'at':1.12,'type':'actual handoff','from':'T','to':'R1','owner':'T','item':'T-map','copy':False})
    add_event(c,s,1.12,'Actual original T-map transfers into R1 custody',{'fixture':'owner T consents; one ordinary interaction; item identity/properties unchanged'},handoff)
    add_event(c,s,1.9,'T regular END 1',{'source':'actual T regular END'},lambda st:end_turn(st['actors']['T'],1.9))
    add_event(c,s,1.91,'R1 reflection phase 1 follows the actual T END',{'source':'bound Return246 schedule; no extra T or A turn'},lambda st:st['effects'][f'A-SR-{cid}'].setdefault('history',[]).append({'at':1.91,'phase':1,'action':'Dodge','noRefresh':True}))
    add_event(c,s,3.0,'D begins the regular turn that funds the accepted field cast',{'source':'bounded offset; D is Wizard17, prepared Antimagic Field Lesser'},lambda st:start_turn(st['actors']['D'],3.0))
    def field(st):
        st['actors']['D']['rp']-=10; st['actors']['D']['action']=0
        st['actors']['D']['concentration']={'spellId':'antimagic-field-lesser','sourceId':'D-AML263','startedAt':3.11,'deadlineAt':63.11}
        st['effects']['D-AML263']={'kind':'antimagic-field-lesser','owner':'D','center':[15,0,0],'radiusFeet':10,'createdAt':3.11,'deadlineAt':63.11,'active':True,'suppressionTarget':'R1'}
        st['actors']['R1']['active']=False
        it=st['items']['T-map']; it.update({'custodian':'ground','held':False,'position':[15,0,0]})
        st['actors']['R1']['inventory'].remove('T-map'); st['actors']['R1']['hands']['right']=None
        st['cargoTrace']['events'].append({'at':3.12,'type':'suppression drop','item':'T-map','owner':'T','custodian':'ground','position':[15,0,0]})
    add_event(c,s,3.12,'Accepted Antimagic Field Lesser suppresses R1; original map drops at exact position',{'source':'AC5 exact accepted field; timing matches bound Return246 suppression-resumption case; drop is proposed local rule'},field)
    add_event(c,s,3.9,'D regular END after committed field cast',{'source':'actual D regular END'},lambda st:end_turn(st['actors']['D'],3.9))
    add_event(c,s,6.0,'A regular start 2 while Reflection remains suppressed',{'source':'actual A regular start; no body/action refreshed for R1'},lambda st:start_turn(st['actors']['A'],6.0))
    add_event(c,s,6.9,'A regular END 2',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],6.9))
    add_event(c,s,7.0,'T regular start 2 while Reflection remains suppressed',{'source':'actual T regular start'},lambda st:start_turn(st['actors']['T'],7.0))
    add_event(c,s,7.1,'T uses a legal nonmagical Dodge while the Reflection body is suppressed',{'source':'ordinary Action; field does not remove actor turn'},lambda st:st['actors']['T'].__setitem__('action',0))
    add_event(c,s,7.9,'T regular END 2',{'source':'actual T regular END'},lambda st:end_turn(st['actors']['T'],7.9))
    add_event(c,s,7.91,'R1 scheduled phase 2 is skipped while suppressed; it is not banked',{'source':'Return246 suppression-resumption case; no replay or refresh'},lambda st:st['effects'][f'A-SR-{cid}'].setdefault('history',[]).append({'at':7.91,'phaseSkipped':True,'noBank':True}))
    def resume(st):
        st['effects']['D-AML263']['active']=False; st['effects']['D-AML263']['endedAt']=9.2; st['actors']['D']['concentration']=None; st['actors']['R1']['active']=True
        st['cargoTrace']['events'].append({'at':9.2,'type':'same-identity resume','item':'T-map','owner':'T','custodian':'ground','position':[15,0,0],'autoReacquired':False})
    add_event(c,s,9.2,'Same reflection identity resumes; map remains real at prior drop point',{'source':'bound Return246 field-end/resume marker; no cargo pickup or duplication'},resume)
    add_event(c,s,12.0,'A regular start 3',{'source':'actual A regular start'},lambda st:start_turn(st['actors']['A'],12.0))
    add_event(c,s,12.9,'A regular END 3',{'source':'actual A regular END'},lambda st:end_turn(st['actors']['A'],12.9))
    add_event(c,s,13.0,'T regular start 3 after field release',{'source':'actual T regular start'},lambda st:start_turn(st['actors']['T'],13.0))
    add_event(c,s,13.9,'T regular END 3',{'source':'actual T regular END'},lambda st:end_turn(st['actors']['T'],13.9))
    add_event(c,s,13.91,'R1 third reflection phase follows T END; original map remains on ground',{'source':'bound Return246 schedule; cargo does not return to R1'},lambda st:st['effects'][f'A-SR-{cid}'].setdefault('history',[]).append({'at':13.91,'phase':3,'noRefresh':True,'cargo':'T-map remains at [15,0,0]'}))
    def terminate(st):
        st['actors']['R1']['active']=False; st['actors']['R1']['life']='FiniteEnded'
        st['effects'][f'A-SR-{cid}']['active']=False; st['effects'][f'A-SR-{cid}']['endedAt']=13.94
        st['effects']['D-AML263']['active']=False
        st['cargoTrace']['events'].append({'at':13.94,'type':'reflection end','item':'T-map','owner':'T','custodian':'ground','position':[15,0,0],'lootCreated':False})
    add_event(c,s,13.94,'Reflection ends; only the original T-map remains at the drop location',{'source':'bound Return246 phase/end timing; cargo settlement remains a NEW rule'},terminate)
    c['requirementsDemonstrated']=['Finite real T-map ID/properties and owner-to-custodian history','Original map is not temporary copied gear or duplicate loot','Exact location and custody persist through suppression, resume, and end']
    c['requirementsHeld']=['Suppression/end drop rule is NEW local adjudication, not accepted source text','No source-qualified attached/no-phase recipient established']
    seal_case(c,s); cargo_case=c

    current_bindings = {}
    def include_file(name, path):
        b=raw(path); current_bindings[name]=bind(str(path.relative_to(ROOT)).replace('\\','/'),b); return b
    payload={}
    payload['README.md']=('''# Soul Reflection Delta 263\n\nThis compact 814/34 supplement is bound to Return246. It preserves all prior passing evidence and makes no canonical edits, acceptance, application, runtime, or campaign-actor claim. Three integrated proposal traces use the exact reviewed Gaseous Form envelope; the original-target-zero trace uses the reviewed core damage/death pipeline; the cargo trace reuses Return246’s source-bound suppression/resumption clock.\n\nEvery Soul-Reflection-local copy, reflected-form, action-permission, termination, and cargo-settlement rule is marked NEW and awaits GPT director adjudication. The source corpus does not establish an eligible low-Intelligence beast: 71 Beast rows have no explicit Intelligence value. Therefore the attached/no-phase recipient gap remains open and no acceptance is requested by implication.\n''').encode()
    payload['current/CURRENT_HANDOFF_262.json']=include_file('handoff',HANDOFF)
    payload['current/CURRENT_SPELL_QUEUE_262.json']=include_file('queue',QUEUE)
    payload['current/CURRENT34_PENDING_IDENTITY_AUDIT_262.json']=include_file('pendingAudit',PENDING)
    payload['current/MATTER_CONVERSION_APPLICATION_262.json']=include_file('matterConversionApplication',AUDIT/'MATTER_CONVERSION_APPLICATION_262.json')
    payload['current/MATTER_CONVERSION_APPLICATION_INDEPENDENT_VERIFICATION_262.json']=include_file('matterConversionVerification',AUDIT/'MATTER_CONVERSION_APPLICATION_INDEPENDENT_VERIFICATION_262.json')
    payload['current/authored_review_index.json']=include_file('authoredReviewIndex',INDEX)
    payload['current/catalog.json']=include_file('spellCatalog',CATALOG)
    payload['source/GASEOUS_FORM/candidate_low_rank_136.json']=include_file('gaseousFormEnvelope',LOW)
    payload['source/GASEOUS_FORM/LOW_RANK_136_EXACT_FULFILLMENT.json']=include_file('gaseousFormAcceptanceEvidence',LOW_RECEIPT)
    payload['source/WIZARD/wizard.json']=include_file('wizardClass',ROOT/'DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json')
    payload['source/RANGER/ranger.json']=include_file('rangerClass',ROOT/'DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json')
    payload['source/CREATURE_LIFECYCLE_PLAYTEST.md']=include_file('creatureLifecycle',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md')
    payload['source/CLASS_PLAYTEST_RULES.md']=include_file('classPlaytestRules',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md')
    payload['source/COMBAT_ACTION_PLAYTEST.md']=include_file('combatActions',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md')
    payload['source/CORE_RESOLUTION_PLAYTEST.md']=include_file('coreResolution',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md')
    payload['source/HEALING_DEATH_PLAYTEST.md']=include_file('healingDeath',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md')
    payload['source/BODY_EQUIPMENT_PLAYTEST.md']=include_file('bodyEquipment',ROOT/'DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md')
    payload['source/bestiary_data_full.json']=include_file('bestiarySource',ROOT/'DescentReviewChanges/ReviewBible/src/bestiary_data_full.json')
    payload['source/ANTIMAGIC_FIELD_LESSER/abjuration_conjuration_rank5_reviewed_05.json']=include_file('antimagicFieldEnvelope',ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json')
    payload['source/ANTIMAGIC_FIELD_LESSER/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json']=include_file('antimagicFieldAcceptance',FULL/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json')
    payload['return246/DD_Rank9_SoulReflection_Director_Return246_HELD.zip']=include_file('return246Archive',RETURN_ZIP)
    payload['return246/DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json']=include_file('return246Delivery',RETURN_DELIVERY)
    for name,b in old.items(): payload['return246/members/'+name]=b
    payload['cases/FORM_SNAPSHOT_263.json']=enc(form_case)
    payload['cases/COPIED_CONCENTRATION_263.json']=enc(conc_case)
    payload['cases/ORIGINAL_ZERO_263.json']=enc(zero_case)
    payload['cases/ORIGINAL_CARGO_263.json']=enc(cargo_case)
    payload['proposals/FIVE_GAP_DISPOSITION_263.json']=enc({
      'authority':AUTH,'identity':'soul-reflection','blocker':'IR207-B02','status':'FOUR_PROPOSED_TRACES; ATTACHED_NO_PHASE_PREMISE_UNRESOLVED',
      'gaseousFormIndexBinding':{'entry':index_entry,'candidate':current_bindings['gaseousFormEnvelope'],'fulfillment':current_bindings['gaseousFormAcceptanceEvidence'],'catalogOperationalNull':True},
      'gaps':[
       {'id':'changed-form recipient','sourceFacts':['W17-IR207 has level-5 Gaseous Form acquisition/preparation; exact reviewed envelope sets 60-second concentration, same identity/size, 10-foot flight/hover, no hands/voice/attacks/gear use, original HP/resources/gear and actual-space reversion.'],'fixtureFacts':['T is willing Medium W17, gas form began at t=-52; expiry t=8; current HP/RP and legal floor/positions are carried.'],'newProposal':['R1 snapshots the current gas body and inherited remaining source marker; it reverts to the same copied root profile at t=8 without slot/resource/HP refresh.'],'status':'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
       {'id':'attached/no-phase recipients','sourceFacts':['Ranger level-16 Beast Companion and common companion rules provide attached phase markers after owner whole turn, no independent turn/refresh/death save; 71 native Beast entries are present.'],'fixtureFacts':['No actor species/Intelligence value supplied.'],'newProposal':['None; no phase-less or attachment-eligible creature is invented.'],'unresolvedPremise':'The bound bestiary entries have no explicit INT/Intelligence field; Ranger eligibility requires INT<7. A fixture cannot repair this.','status':'OPEN_SOURCE_CONTRACT_GAP'},
       {'id':'original target zero/death settlement','sourceFacts':['Core source specifies damage→instant-death→floors→Wound save→zero-life-state ordering; Downed is living at 0 and regular-start death saves remain ordinary.'],'fixtureFacts':['W17 target starts at1 HP; R1 stipulated hit/damage/Wound-save rolls; next actual T regular start is recorded.'],'newProposal':['Resolve the original target’s complete source pipeline before ending R1; retain owner, HP, Wounds, death markers, item custody.'],'status':'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
       {'id':'copied concentration','sourceFacts':['Gaseous Form source accepts a willing self-target and concentration up to60 seconds; class source gives DC max(10,floor(damage/2)); W17 Arcane Bolt and force resistance are source-bound.'],'fixtureFacts':['A copied operation pays5 RP, takes4 force damage after resistance, then stipulated CON roll fails DC10.'],'newProposal':['R1 can invoke copied spells only under an explicit Soul-Reflection-local grant; failed concentration ends only that copied effect.'],'status':'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
       {'id':'entrusted original cargo','sourceFacts':['T-map is a finite W17 source item; ordinary turn has one free object interaction; AC5 Antimagic Field Lesser has accepted suppression/resumption behavior.'],'fixtureFacts':['T consents to hand exact T-map to R1; item keeps owner T; field suppresses at3.12 and ends9.2.'],'newProposal':['On suppression the actual item drops at R1’s exact position; it remains there on resume/end and is never converted to reflection gear or loot.'],'status':'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'}],
      'request':'Issue explicit ACCEPT or HOLD for soul-reflection / IR207-B02. If HOLD, identify every exact remaining correction and whether the eligible attached/no-phase source premise must be supplied externally or whether a narrower adjudicable interface is permitted. Acceptance of no other identity is requested.'})
    payload['sourceBindings/CURRENT_SOURCE_BINDINGS_263.json']=enc(current_bindings)

    # Candidate-independent check of the missing companion eligibility datum.
    bestiary=json.loads(raw(ROOT/'DescentReviewChanges/ReviewBible/src/bestiary_data_full.json'))
    beasts=[x for x in bestiary if str(x.get('type','')).lower()=='beast']
    int_fields=['int','INT','intelligence','intelligenceScore','intelligence_score','abilityScores','abilities']
    explicit=[x for x in beasts if any(k in x for k in int_fields)]
    payload['source/ATTACHED_RECIPIENT_SOURCE_GAP_263.json']=enc({'beastRows':len(beasts),'rowsWithExplicitINTOrAbilityObject':len(explicit),
      'status':'OPEN','finding':'The bound native Beast dataset supplies no explicit INT/Intelligence/ability object for any Beast row. Ranger Beast Companion eligibility requires INT<7; do not synthesize it from a name or fixture.',
      'source':current_bindings['bestiarySource'],'classSource':current_bindings['rangerClass']})

    now=datetime.now(timezone.utc).isoformat()
    payload['REQUEST_263.txt']=(f'''Calibration Review Part 6 — Soul Reflection / IR207-B02 (Delta263)\n\nPlease review the attached compact 814/34 supplement bound to Return246. Current authority is 814 applied / 34 pending / 0 accepted-unapplied (538 standalone procedures / 173 scoped interfaces). The catalog remains unchanged.\n\nThe indexed Gaseous Form envelope and exact fulfillment evidence are attached byte-exact. I added four static event traces for changed form, copied concentration, original-target zero/death-state settlement, and one actual original cargo item through suppression/resumption/end. Every Soul-Reflection-local rule remains labeled NEW and proposed; the traces claim no prior acceptance or runtime result. Return246’s passing evidence is preserved.\n\nThe attached/no-phase recipient remains unresolved: the native class rule requires a Beast with INT<7, but none of the 71 bound Beast entries carries an explicit Intelligence value. No fixture fills that premise. Please issue an explicit ACCEPT or HOLD for soul-reflection / IR207-B02. If HOLD, list each exact remaining correction and clarify what source can close the attached/no-phase eligibility gap. No other identity is in scope.\n''').encode('utf-8')
    payload['PREPARATION_263.json']=enc({'id':'SOUL-REFLECTION-DELTA-PREPARATION-263','recordedAtUtc':now,'authority':AUTH,'target':'soul-reflection','blocker':'IR207-B02','currentAuthorityBindings':current_bindings,'return246ArchiveSha256':sha(raw(RETURN_ZIP)),'return246ReferencedMemberCount':len(old),'gaseousFormIndexEntry':index_entry,'caseIds':[x['id'] for x in [form_case,conc_case,zero_case,cargo_case]],'newRulesAccepted':False,'canonicalFilesChanged':False,'applicationPerformed':False,'githubChanges':False})

    OUT.mkdir(parents=True)
    rows=[]
    with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(payload.items()):
            if not safe(name): raise ValueError(f'unsafe member {name}')
            z.writestr(name,b); rows.append({'path':name,'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
        manifest={'id':'SOUL-REFLECTION-DELTA-263-MEMBER-MANIFEST','authority':AUTH,'targetIds':['soul-reflection'],'memberCountExcludingSelf':len(rows),'members':rows}
        z.writestr('MEMBER_MANIFEST.json',enc(manifest))
    archive=raw(ARCHIVE)
    delivery={'id':'SOUL-REFLECTION-DELTA-263-DELIVERY','status':'PREPARED_UNSENT','archive':bind(ARCHIVE.relative_to(ROOT).as_posix(),archive),
      'archiveMembers':len(rows)+1,'boundPayloadMembers':len(rows),'memberManifestSha256':sha(enc(manifest)),'memberManifest':manifest,
      'authority':AUTH,'targetIds':['soul-reflection'],'destination':'Calibration review part 6','conversation':CHAT,'accepted':False,'applied':False}
    DELIVERY.write_bytes(enc(delivery))
    submission={'id':'SOUL-REFLECTION-DELTA-263-SUBMISSION','recordedAtUtc':now,'status':'PREPARED_UNSENT','authority':AUTH,'targetIds':['soul-reflection'],'blockerIds':['IR207-B02'],
      'archive':delivery['archive'],'deliveryManifest':bind(DELIVERY.relative_to(ROOT).as_posix(),raw(DELIVERY)),'caseCount':4,'attachedNoPhaseGapOpen':True,
      'acceptedIds':[],'appliedIds':[],'canonicalChanges':False,'githubChanges':False}
    SUBMISSION.write_bytes(enc(submission))
    print(json.dumps({'status':'PACKET_PREPARED','archive':delivery['archive'],'members':len(rows)+1,'out':str(ARCHIVE)},indent=2))

if __name__=='__main__': main()
