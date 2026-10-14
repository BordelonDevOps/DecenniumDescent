"""Execute named, bounded reference cases against the FEAT327 source directions.

Expected values are hand-authored below, separate from the reference functions.
No builder import, runtime activation, source rewrite, or whole-FXC closure.
The report distinguishes executable arithmetic/state subsets from source-based
adjudication and identifies campaign facts supplied rather than authenticated.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from fractions import Fraction
from copy import deepcopy
import json
import argparse
import feat_exact_01_reference_models as m

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
V=A/'feat327-source-verdict'
U=R/'data/public/feat_candidates/exact_01'


def read(p):return json.loads(p.read_text('utf-8-sig'))
def binding(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def normal(x):
    if isinstance(x,Fraction):return int(x) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
    if isinstance(x,(tuple,list)):return [normal(y) for y in x]
    if isinstance(x,set):return sorted(normal(y) for y in x)
    if isinstance(x,dict):return {str(k):normal(v) for k,v in x.items()}
    return x


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,default=A/'FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json')
    args=parser.parse_args()
    if args.report.exists():raise SystemExit('Preserve an existing report; pass a new --report destination.')
    checks=[];cases=[];current=None
    fa=read(V/'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json')['cases']
    sources={x['featId']:x for x in read(V/'FEAT_327_AUTHORING_REGISTER.json')['records']}
    public={x['id']:x for x in read(U/'candidate.json')['feats']}
    core=read(R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    warrior=read(R/'data/public/class_playtests/warrior.json')
    wc={x['id']:x for x in warrior['cards']}
    mage=read(R/'data/public/class_playtests/mage.json')
    dragoon=read(R/'data/public/class_playtests/dragoon.json')
    deps=read(U/'spell_dependencies.json')['spells']

    def check(name,actual,expected,kind='reference-state'):
        a,e=normal(actual),normal(expected)
        row={'caseId':current,'name':name,'kind':kind,'actual':a,'expected':e,'pass':a==e}
        checks.append(row)
        return row['pass']
    def reject(name,fn):
        try:fn()
        except ValueError as err:check(name,'rejected','rejected');checks[-1]['reason']=str(err)
        else:check(name,'accepted','rejected')
    def begin(n,premises,scope,unmodeled):
        nonlocal current
        current=f'FA-{n:02d}';s=fa[n-1]
        assert s['id']==current
        cases.append({'caseId':current,'sourceExpectation':s,'suppliedPremises':premises,
                      'executedSubset':scope,'notExecutedByThisModel':unmodeled,
                      'sourceProcedureSha256':sha256(sources[s['featId']]['completeAuthoringProcedure'].encode()).hexdigest()})
        check('Public procedure equals actual source-directed procedure',public[s['featId']]['operationalRules'],
              sources[s['featId']]['completeAuthoringProcedure'],'source-text-equality')
        # Equality is recorded without copying a full procedure into every assertion.
        checks[-1]['actual']=checks[-1]['expected']=cases[-1]['sourceProcedureSha256']

    # Bind immutable source/candidate inputs to their recorded assembly receipt.
    build=read(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    preserved=0
    for name,expected in {**build['originalSourceBindings'],**build['artifacts']}.items():
        b=binding(G/name)
        check('Unchanged source/candidate '+name,{k:b[k] for k in ('bytes','sha256')},expected,'input-integrity')
        preserved+=1

    begin(1,'One actual owner, Endurance operative, world hour0; scheduled Rest16–24 missed; later40–48 missed. Actual safe uninterrupted rest48–56. No automatic beneficial reward claim.',
          'Separate food/sleep counters; due events; later missed Watch; exact endpoint priority; no replay; suppression and acquisition variants.',
          'No authentication of actual shelter/meal consumption, whole Strain death/recovery engine, or automatic resource refill.')
    e=m.ExpeditionLedger();e.miss_rest(24,40,'rest-0');e.settle_day(24,False,False)
    check('First food event and debt opening',e.snapshot(),{'time':24,'strain':0,'food':1,'sleep':0,'debt':True,'deadline':40,'unsupported':[24]})
    e.advance(40)
    check('First sleep deadline omitted, evaluated once',e.snapshot(),{'time':40,'strain':0,'food':1,'sleep':1,'debt':True,'deadline':40,'unsupported':[24]})
    e.advance(41);e.advance(47)
    check('No hourly or Watch replay',[e.strain,e.sleep_pending,len(e.history)],[0,1,2])
    e.miss_rest(48,64,'rest-1');e.settle_day(48,False,False)
    check('Second sleep and food events both apply',e.snapshot(),{'time':48,'strain':2,'food':0,'sleep':0,'debt':True,'deadline':64,'unsupported':[24,48]})
    e.safe_rest(48,56,True,True)
    check('Safe rest clears debt only',e.snapshot(),{'time':56,'strain':2,'food':0,'sleep':0,'debt':False,'deadline':None,'unsupported':[24,48]})
    e.advance(80);check('Cleared debt has no later due event',len(e.history),4)
    e=m.ExpeditionLedger();e.miss_rest(24,40,'exact');e.safe_rest(32,40,True,True)
    check('Rest completion at exact deadline precedes assessment',[e.strain,e.sleep_pending,e.debt,len(e.history)],[0,0,False,0])
    endpoint=(R/'docs/mechanics/expedition/EXPEDITION_PART01_DIRECTOR.md').read_text('utf-8')
    check('Actual EX01-03 endpoint source','Complete the Rest and clear debt before processing the still-unpaid-debt step.' in endpoint,True,'source-adjudication')
    e=m.ExpeditionLedger();e.miss_rest(24,40,'late');e.safe_rest(33,41,True,True)
    check('Late completion does not erase earlier due history',[len(e.history),e.history[0]['at'],e.debt],[1,40,False])
    e=m.ExpeditionLedger();e.settle_day(24,False,False);e.operative=False;e.settle_day(48,False,False);e.operative=True;e.settle_day(72,False,False)
    check('Suppression clears cause credit, never replays earlier penalty',[e.strain,e.food_pending,len(e.history)],[1,1,3])
    e.settle_day(96,True,True);check('Genuinely supported day clears food credit',e.food_pending,0)
    e=m.ExpeditionLedger(strain=3,operative=False);e.miss_rest(24,40,'prior');e.advance(40);e.operative=True;e.miss_rest(48,64,'later')
    check('Acquisition does not forgive past Strain or existing debt',[e.strain,e.sleep_pending,e.debt,e.deadline],[4,1,True,64])
    e.operative=False;e.advance(64);check('Suppressed sleep applies original and clears credit',[e.strain,e.sleep_pending],[5,0])
    reject('No clock rewind',lambda:e.advance(63))
    reject('No unsafe debt payment',lambda:e.safe_rest(64,72,False,True))
    reject('No interrupted debt payment',lambda:e.safe_rest(64,72,True,False))
    reject('No seven-hour debt payment',lambda:e.safe_rest(64,71,True,True))
    r=m.RestRewards(last_long=40)
    e=m.ExpeditionLedger(now=40);e.miss_rest(48,64,'post40');e.safe_rest(48,56,True,True)
    check('Real debt-clearing rest inside reward limit',[e.debt,r.claim('rest48-56',56,'long')],[False,False])
    check('Next Long Rest at full24-hour interval',r.claim('rest56-64',64,'long'),True)
    check('Same actual rest cannot be claimed twice',r.claim('rest56-64',64,'long'),False)
    check('Two Short Rests only',[r.claim('shortA',65,'short'),r.claim('shortB',66,'short'),r.claim('shortC',67,'short')],[True,True,False])
    work=m.WorkLedger();work.claim(0,0,'work');work.claim(0,1,'work')
    reject('No third work Watch',lambda:work.claim(0,2,'work'))
    reject('No duplicate forage/craft/rest credit',lambda:work.claim(0,1,'rest'))
    work.claim(0,2,'rest');check('Third Watch can be actual Rest',work.watches[(0,2)],'rest')

    begin(2,'Actual mandatory oil/logistics shortage at daily checkpoint, possibly concurrent food/water shortage.',
          'One daily Strain total; independent shortage bypasses Endurance; absent/suppressed cause-credit cleanup.',
          'Actual logistics necessity must be declared by the controlling expedition source.')
    e=m.ExpeditionLedger();e.settle_day(24,False,False,False)
    check('Two missing supply categories still one daily penalty',[e.strain,e.food_pending,e.unsupported_days],[1,0,{24}])
    e=m.ExpeditionLedger(food_pending=1);e.settle_day(24,False,False,False)
    check('Other shortage is not an eligible prevented food-only event',[e.strain,e.food_pending],[1,1])
    e.operative=False;e.settle_day(48,False,False,False)
    check('Suppressed food shortage credit clears even with other shortage',[e.strain,e.food_pending],[2,0])
    e=m.ExpeditionLedger(food_pending=1);e.settle_day(24,True,True,False)
    check('Food support clears its credit but oil shortage remains',[e.strain,e.food_pending,e.unsupported_days],[1,0,{24}])
    reject('Daily settlement cannot be replayed',lambda:e.settle_day(24,True,True,False))

    begin(3,'One qualified holder, accessible edible14lb/potable56pints stock, ordinary biome,480 actual active minutes; separate Large ordinary-diet consumer.',
          'Finite stock debits, completion clock, cargo, own Survivalist requirement, missing oil/sundries.',
          'Lawful access, hazards, actual animal diet, load capacity and container mass remain supplied premises; no generated terrain.')
    f=m.ForageStock(28,112);yielded=f.complete('forager-A',8,480,14,56)
    check('One full yield including real mass',yielded,{'foodLb':14,'waterPints':56,'cargoLbBeforeContainers':70,'oilPints':0,'sundriesLb':0})
    check('Actual remaining site stock',[f.food,f.water],[14,56])
    check('Large ordinary needs',m.daily_need(True,False),{'foodLb':4,'waterPints':16,'fullSupplyOilPints':1,'fullSupplySundriesLb':Fraction(1,4)})
    check('Large holder-only Survivalist',m.daily_need(True,True),{'foodLb':2,'waterPints':8,'fullSupplyOilPints':1,'fullSupplySundriesLb':Fraction(1,4)})
    check('Small/Medium Survivalist',m.daily_need(False,True),{'foodLb':1,'waterPints':4,'fullSupplyOilPints':1,'fullSupplySundriesLb':Fraction(1,4)})
    reject('Completion before24 elapsed hours rejected',lambda:f.complete('forager-A',31,480,14,56))
    f.complete('forager-A',32,480,14,56);check('Real second completion exhausts stock',[f.food,f.water],[0,0])
    reject('Another holder cannot mint exhausted stock',lambda:f.complete('forager-B',40,480,14,56))
    f=m.ForageStock(14,0)
    reject('Missing potable water cannot be inferred',lambda:f.complete('A',8,480,14,56))
    check('Predeclared real partial yield',f.complete('A',8,480,14,0)['waterPints'],0)
    reject('Seven hours cannot buy guarantee',lambda:m.ForageStock(14,56).complete('A',8,420,14,56))
    reject('Desert/arctic guarantee unavailable',lambda:m.ForageStock(14,56).complete('A',8,480,14,56,ordinary_region=False))

    begin(4,'Two distinct actual concentration-save feats, each+2; actual eligible class bonuses+1/+2 from one strongest family.',
          'Feat identity deduplication and separate strongest class-family arithmetic.','No generic class/item/spell stacking override or assumed proficiency.')
    check('Distinct feats plus strongest class',m.feat_class_bonus([('featA',2),('featB',2)],[1,2]),6)
    check('Same feat from two sources once',m.feat_class_bonus([('featA',2),('featA',2)],[1,2]),4)
    check('No class bonus is invented',m.feat_class_bonus([('featA',2)],[]),2)

    begin(5,'One existing walking Speed30 and independently active hostile Slasher−10, CripplingStrike−10, optional half-Speed.',
          'Independent common-base slow comparison, suppression and hard0.','Burden/terrain/systemic stages are separate and not executed.')
    slows=[{'subtract':10},{'subtract':10}]
    check('Two−10 slows strongest once',m.controlled_speed(30,slows),20)
    check('Independent half-Speed strongest',m.controlled_speed(30,slows+[{'factor':[1,2]}]),15)
    check('Hard0 still wins',m.controlled_speed(30,slows,True),0)
    check('Suppressed half-Speed not active',m.controlled_speed(30,slows+[{'factor':[1,2],'active':False}]),20)

    begin(6,'Already critical-adjusted native packet19, separately identified external rider7; qualifying10% before one actual half save.',
          'Independent floors, typed proportional allocation with stable ties, Temp HP and overkill after resolution.',
          'No full attack/save/defense/critical pipeline, damage provenance authentication or Wound engine.')
    p=m.percent_packet([19],[(1,10)])
    check('Pre-save native percent',p,[20]);check('One subsequent half save',sum(p)//2,10,'arithmetic')
    check('External rider excluded from percent base',sum(p)+7,27,'arithmetic')
    check('Two percentages share original19 base',m.percent_packet([19],[(1,10),(1,2)]),[29])
    check('Typed floor/residual from native7+4',m.percent_packet([7,4],[(1,2)]),[10,6])
    check('Stable equal remainder tie',m.percent_packet([1,1],[(1,2)]),[2,1])
    check('Zero packet never creates minimum damage',m.percent_packet([0,0],[(1,2)]),[0,0])
    check('Temp plus normal loss excludes overkill',m.actual_damage(5,3,12),{'normalHP':0,'tempHP':0,'actualDamage':8,'overkill':4})
    check('Fully prevented event',m.actual_damage(5,3,0),{'normalHP':5,'tempHP':3,'actualDamage':0,'overkill':0})
    reject('Impossible negative HP snapshot',lambda:m.actual_damage(-1,3,2))

    begin(7,'Commander and two willing hearing allies in range; each has Speed30 and its own declared Reaction budget.',
          'Self counts toward three; each actual Reaction spent once.','Range, hearing, willingness, path and terrain are supplied, not inferred.')
    reactions={'commander':1,'A':1,'B':0}
    check('Each recipient pays own Reaction',m.self_ally_move(['commander','A','B'],'commander',reactions,{'commander':30,'A':30,'B':30}),{'commander':15,'A':15,'B':0})
    check('Actual reactions spent',reactions,{'commander':0,'A':0,'B':0})
    check('Self cannot borrow ally Reaction',m.self_ally_move(['commander'],'commander',{'commander':0,'A':1},{'commander':30}),{'commander':0})
    reject('No fourth recipient',lambda:m.self_ally_move(['commander','A','B','C'],'commander',{},{}))
    reject('Same self cannot receive two moves',lambda:m.self_ally_move(['commander','commander'],'commander',{},{}))

    begin(8,'Source explicitly typed Dragon, visible, targeting holder; available Reaction and SR charge; attack branch before roll.',
          'Ranged breath versus ordinary ranged/melee qualification and denial predicates.',
          'Save-breath uses the source separate whole-save reroll; no attack or save is fabricated by this predicate.')
    kw=dict(dragon=True,perceived=True,target_self=True,melee=False,breath=True,before_roll=True,reaction=True,sr_available=True)
    check('Ranged breath attack qualifies',m.slayer_attack_reaction(**kw),True)
    check('Non-breath ranged attack fails',m.slayer_attack_reaction(**(kw|{'breath':False})),False)
    check('Dragon melee attack qualifies',m.slayer_attack_reaction(**(kw|{'melee':True,'breath':False})),True)
    for key in ['dragon','perceived','target_self','before_roll','reaction','sr_available']:
        check('Missing '+key+' rejects attack Reaction',m.slayer_attack_reaction(**(kw|{key:False})),False)

    begin(9,'Actual armed, supported20-piece caltrop field; distinct real ground entries; accessible safe unoccupied field for later collection.',
          'Persistence after saves, per-piece custody, half-Speed avoidance, no remote replacement, no replay.',
          'Preparation/arming, square geometry, coverage after dispersal, save resolution, harm and actual safe manipulation are supplied premises.')
    c=m.CaltropField();check('First entrant saves',c.enter('entry1','A',True),'saved')
    check('Field remains after saved entry',len(c.field_pieces),20)
    check('Second entrant still affected',c.enter('entry2','B',False),'piercing1-stop-and-slow')
    check('One actual piece moved into body',[len(c.field_pieces),len(c.embedded['B']),c.total_pieces()],[19,1,20])
    check('Remote replacement cannot clear field',c.replacement_can_arm(),False)
    check('Half-Speed avoidance consumes no piece',c.enter('entry3','C',False,True),'avoided')
    reject('Same entry replay rejected',lambda:c.enter('entry2','B',False))
    reject('Occupied unsafe collection rejected',lambda:c.collect(1,True,False))
    reject('Less than one minute rejected',lambda:c.collect(Fraction(1,2),True,True))
    c.collect(1,True,True)
    check('Safe collection leaves embedded piece in body',[len(c.bag),len(c.field_pieces),len(c.embedded['B']),c.total_pieces()],[19,0,1,20])
    check('Physical clearance frees enhanced field slot',c.replacement_can_arm(),True)
    c.extract('B',0);check('Actual removed piece recovered exactly once',[len(c.bag),c.total_pieces()],[20,20])
    reject('Embedded piece cannot be recovered twice',lambda:c.extract('B',0))

    begin(10,'Ordinary reviewed lock, actual tools; DEX+3, PB2, actual proficiency or actual replacement Expertise.',
          'Proficiency contribution replaces rather than duplicates; missing tools rejected.',
          'Source specifies Action/DC15; actual lock task degrees/natural shifts/retry permission are not executed by this arithmetic model.')
    check('Proficient burglar modifier',m.lock_bonus(3,2,True,False,True),7)
    check('Expertise replaces proficiency',m.lock_bonus(3,2,True,True,True),9)
    reject('Missing actual tools',lambda:m.lock_bonus(3,2,True,False,False))
    reject('Expertise without proficiency',lambda:m.lock_bonus(3,2,False,True,True))

    begin(11,'One legally ridden real Beast with walking40 only, one controlling rider; optional Swim derived expressly from walk in a separate fixture.',
          'Actual modes+10 once; derived mode no double boost; same physical body one phase; dismount arithmetic.',
          'Actual seat/tack/load/training/placement and one-per-regular-interval mounting allowance remain source adjudication.')
    check('Only existing walk becomes50',m.mounted_speeds({'walk':40},{},True),{'walk':50})
    check('Derived mode follows parent once',m.mounted_speeds({'walk':40},{'swim':'walk'},True),{'walk':50,'swim':50})
    check('Unmounted body gets no Cavalry boost',m.mounted_speeds({'walk':40},{},False),{'walk':40})
    cl=m.CommandLedger();cl.elect_phase('beast-A',1,'owner','controlled-mount')
    reject('Bonding cannot supply second same-body phase',lambda:cl.elect_phase('beast-A',1,'owner','attached-companion'))
    reject('Custody transfer cannot reset same-round phase',lambda:cl.elect_phase('beast-A',1,'other-owner','controlled-mount'))
    check('Rider current walk30 pays half for dismount',30//2,15,'arithmetic')

    begin(12,'Owner totallevel10; two owned audible Beast companions, compatible attached phases; shared BA and one offensive allowance per numbered round.',
          'Two support recipients versus one Attack, spent-command/offense continuity, shared Trapcasting offense.',
          'Body/source eligibility and actual command channel must be established outside model; this does not grant ownership.')
    cl=m.CommandLedger();cl.elect_phase('beast-A',1,'owner','attached');cl.elect_phase('beast-B',1,'owner','attached')
    check('One support command two recipients',cl.command('owner',1,['beast-A','beast-B'],'Help',2),{'beast-A':'Help','beast-B':'Help'})
    reject('No second command from another phase',lambda:cl.command('owner',1,['beast-A'],'Attack',2,offensive_body='beast-A'))
    check('One Attack only next round',cl.command('owner',2,['beast-A','beast-B'],'Attack',2,offensive_body='beast-A'),{'beast-A':'Attack','beast-B':'defensive/Dodge'})
    check('Trapcasting cannot spend a second offense',cl.trap_attack('owner',2,True),False)
    check('False entry does not spend offense',cl.trap_attack('owner',3,False),False)
    check('One actual trap entry spends shared offense',cl.trap_attack('owner',3,True),True)
    reject('Known spent offense cannot authorize companion Attack',lambda:cl.command('owner',3,['beast-B'],'Attack',2,offensive_body='beast-B'))
    check('Rejected known-illegal attack leaves support command available',cl.command('owner',3,['beast-A','beast-B'],'Disengage',2),{'beast-A':'Disengage','beast-B':'Disengage'})
    reject('Belowlevel10 recipientcap1',lambda:m.CommandLedger().command('owner',1,['A','B'],'Help',1))
    reject('No actual audible command channel',lambda:m.CommandLedger().command('owner',1,['A'],'Help',1,channel=False))

    begin(13,'Authorized successful20-minute light partial structural repair; PB3, real currentHP3/max10, base restores2; actual beneficial SR.',
          'Entire job versus tail, headroom, genuine reward eligibility; bonus only current HP.',
          'Tools/materials/body/repair authority are premises; charge/fuel/service fields are not present in this function and receive no transition.')
    check('Entire20-minute repair addsPB3',m.whole_repair_bonus(20,20,True,True,2,3,3,10),{'restException':True,'featExtraHP':3})
    check('Total restoration2+3',2+3,5,'arithmetic')
    check('Last20 of480-minute job fails',m.whole_repair_bonus(480,20,True,True,2,3,3,10),{'restException':False,'featExtraHP':0})
    check('Already full base restoration no extra',m.whole_repair_bonus(20,20,True,True,7,3,3,10),{'restException':True,'featExtraHP':0})
    check('One HP remaining headroom',m.whole_repair_bonus(20,20,True,True,2,3,7,10),{'restException':True,'featExtraHP':1})
    check('Debt-only rest not beneficial SR',m.whole_repair_bonus(20,20,False,True,2,3,3,10),{'restException':False,'featExtraHP':0})
    check('Feat does not authorize repair',m.whole_repair_bonus(20,20,True,False,2,3,3,10),{'restException':False,'featExtraHP':0})

    begin(14,'One appraiser works inspection0–10 and remainder10–30; actual separate disposition30–60; reference40gp, mutually agreed gross20gp.',
          'Human-authored event schedule arithmetic, separate values; explicit source-based no-second-check adjudication.',
          'No simulated negotiation, property discovery, magical identification protections, title, fees or transaction authorization.')
    schedule=[{'actor':'appraiser','task':'inspection','start':0,'end':10},
              {'actor':'appraiser','task':'appraisal-remainder','start':10,'end':30},
              {'actor':'seller','task':'disposition','start':30,'end':60}]
    check('Full appraisal active minutes',sum(x['end']-x['start'] for x in schedule[:2]),30,'arithmetic')
    check('Full disposition still30',schedule[2]['end']-schedule[2]['start'],30,'arithmetic')
    check('No overlap in same appraisal subtasks',schedule[0]['end']<=schedule[1]['start'],True,'arithmetic')
    checks[-1]['timeline']=schedule
    shared=(V/'FEAT_SHARED_DIRECTIONS.md').read_text('utf-8')
    check('Source explicitly forbids second roll','No second roll is created by the label.' in shared,True,'source-adjudication')
    cases[-1]['authoredAdjudication']='40gp remains reference;20gp remains agreed gross. Full actual settlement still determines net. No assertion that a buyer must accept either value.'

    begin(15,'Actual adjudicated knowing holder of false-face100gp; combined assay/remint fees3gp or12gp.',
          'Exact greater-of allocation, fees counted once.','Intent/holder responsibility, provenance and actual fees must first be established by source procedure.')
    check('Fees3: total10, additional7',m.assay(100,3),{'total':10,'fees':3,'additional':7})
    check('Fees12: total12, no extra',m.assay(100,12),{'total':12,'fees':12,'additional':0})
    check('Rational precision before final coin rounding',m.assay(15,1),{'total':Fraction(3,2),'fees':1,'additional':Fraction(1,2)})

    begin(16,'Current genuine class envelopes: Mage3max8, Dragoon8max7, Warrior7max0. Capacity fixture startsMagecurrent7 with an acknowledged unrefunded historical payment3; authenticity of that prior history is not inferred.',
          'Actual class table bindings; headroom/expense caps; shared refunds; growth does not refill; no pool invented.',
          'This is not complete Arcane Recall trigger/recharge/history simulation. Historical-payment premise is separate from an executable fresh payment sequence.')
    check('Mage3 source capacity',mage['rpByClassLevel'][2],8,'source-data')
    check('Mage3 matches Core',core['caster_pools']['Mage'][2],8,'source-data')
    check('Dragoon8 actual capacity',dragoon['rpByClassLevel'][7],7,'source-data')
    check('Warrior7 source capacity',warrior['rpByClassLevel'][6],0,'source-data')
    rp=m.ResourceLedger(7,8,payments={'authenticated-prior-cast':3})
    check('Larger legal unrefunded payment still capped by1 headroom',rp.refund('authenticated-prior-cast',3),1)
    check('No second headroom at full pool',rp.refund('authenticated-prior-cast',3),0)
    rp=m.ResourceLedger(8,8);rp.pay('actual-rank2',3)
    check('Actual fresh payment',rp.current,5)
    check('First refund shares same expense',rp.refund('actual-rank2',2),2)
    check('Second refund only remaining paid1',rp.refund('actual-rank2',3),1)
    check('No third refund',rp.refund('actual-rank2',3),0)
    rp.capacity(10);check('Capacity growth does not refill',rp.current,8)
    rp.capacity(7);check('Capacity shrink clamps',rp.current,7)
    reject('Warrior7 cannot pay3RP',lambda:m.ResourceLedger(0,0).pay('arcane-pulse',3))
    check('Absent payment cannot refund',m.ResourceLedger(0,8).refund('missing',3),0)
    reject('Impossible above-cap resource fixture',lambda:m.ResourceLedger(9,8))

    begin(17,'Observed eligible noncopy rank4 numeric component10; actual releaser rank ceiling2, actual3d6 total12, available8RP and all actual components.',
          'Half-rank/numeric bound; actual rank-price table and paid debit; copy classification/no recapture/no class-resource output.',
          'Complete capture/action/range/components/Dissonance/Refrain/interrupt history is source adjudication, not implemented in this small model.')
    copied=m.copy_profile(4,10,12,2)
    check('Paid copy profile',copied,{'rank':2,'dice':3,'magnitude':5,'copyDerived':True,'canCapture':False,'canGenerateClassResource':False,'newPaidCast':True})
    cost=core['resonance_costs'][str(copied['rank'])]
    check('Actual rank2 base price',cost,3,'source-data')
    rp=m.ResourceLedger(8,8);rp.pay('new-paid-copy-cast',cost);check('Actual cost paid once',rp.current,5)
    reject('Same paid cast cannot be committed twice',lambda:rp.pay('new-paid-copy-cast',cost))
    reject('No rank permission from sufficient RP alone',lambda:m.copy_profile(4,10,12,1))
    reject('No release with insufficient real pool',lambda:m.ResourceLedger(2,8).pay('copy',cost))
    cases[-1]['authoredAdjudication']='Release still commits the actual route’s components, repetition/Dissonance/history and interruption. These flags do not grant a free release or bypass those procedures.'

    begin(18,'Same bounded paid-copy source family; observed native component1, actual rank2, actual2d6 total7; separate missing-source rejection fixtures.',
          'Zero numeric cap and missing/invalid source-rank/magnitude/ceiling rejection.','Monster CR-to-rank derivation and actual source observation are not inferred.')
    check('Native1 caps at0',m.copy_profile(2,1,7,1)['magnitude'],0)
    check('Cantrip staysrank0 withone die',m.copy_profile(0,10,4,0)['rank'],0)
    reject('Missing rank',lambda:m.copy_profile(None,10,7,2))
    reject('Missing observed native component',lambda:m.copy_profile(2,None,7,2))
    reject('Missing actual rank route',lambda:m.copy_profile(2,10,7,None))
    reject('Impossible rolled total',lambda:m.copy_profile(2,10,13,2))

    begin(19,'Actual reviewed current Invisibility envelope, existing spell instance, ordinary movement or a legal committed action.',
          'Movement preservation and pre-commit endpoint for A/BA/Reaction, plus current full payload binding.',
          'Visibility/location/equipment concealment, cast access and action legality must come from their source engines.')
    inv=deps['invisibility']['completeCurrentProcedureCard']['operationalCandidate']
    check('Current source duration is minute/nonconcentration',inv['duration'],'1 minute, or before the recipient next commits an Action, Bonus Action or Reaction; no concentration.','source-data')
    check('Walking survives',m.invisible_before_event(True,'movement'),{'activeAfter':True,'order':['event']})
    for kind in ['Action','Bonus Action','Reaction']:
        check('End before '+kind,m.invisible_before_event(True,kind),{'activeAfter':False,'order':['end-invisibility','commit']})
    check('Rejected never-committed action does not end',m.invisible_before_event(True,'Action',False),{'activeAfter':True,'order':['event']})

    begin(20,'Actual ritual has base cast6seconds plus600additional active seconds; known qualifying Quick Ritualist and Channeler.',
          'Named composition floors, rounding, nonworsening shorter additions.','Ritual learning/credentials, one actual cast/concentration/history and material access remain source procedures.')
    check('Quick total306',m.ritual_seconds(6,600,True,False),306)
    check('Channel floor keeps306',m.ritual_seconds(6,600,True,True),306)
    check('Channel alone rounds454.5 to455',m.ritual_seconds(6,600,False,True),455)
    check('Short existing additional time never increased',m.ritual_seconds(6,120,True,True),126)
    check('Longer ritual applies both bounded factors',m.ritual_seconds(6,1200,True,True),455)
    reject('Negative active labor',lambda:m.ritual_seconds(6,-1,True,True))

    begin(21,'Actual personally acquired nonconcentration True Strike held with original deadline10; next actual cast committed at5.',
          'One held identity consumed on next commit including counter/unfit; expiry and no second benefit.',
          'Actual attack timing and advantage cancellation, other concentration/Ready slots and cast authenticity are not simulated.')
    sw=m.Spellweave('true-strike-instance',10)
    check('Countered next spell still consumes',sw.commit_next(5,True,True),{'attached':True,'consumed':True,'benefit':False,'identity':'true-strike-instance','requiresNewConcentration':False})
    check('No second attachment',sw.commit_next(6,True),{'attached':False,'consumed':False,'benefit':False})
    check('Unsuitable next spell still consumes',m.Spellweave('held',10).commit_next(5,False),{'attached':True,'consumed':True,'benefit':False,'identity':'held','requiresNewConcentration':False})
    check('Eligible next spell can use its actual attack',m.Spellweave('held',10).commit_next(5,True),{'attached':True,'consumed':True,'benefit':True,'identity':'held','requiresNewConcentration':False})
    sw=m.Spellweave('expired',10);sw.commit_next(10,True);check('Expired record actually gone',sw.identity,None)
    check('Actual True Strike has one next-roll mark',deps['true-strike']['completeCurrentProcedureCard']['operationalCandidate']['numericParameters'],{'uses':1},'source-data')

    begin(22,'Actual occupied squares have independently established illumination; Darkvision changes perception only.',
          'Whole footprint predicate and changed light before resolution.','Actual source radius/occlusion/light conflict arbitration remains external.')
    check('All actual occupied squares dark',m.entire_darkness(['dark','dark','dark','dark']),True)
    check('One dim square fails',m.entire_darkness(['dark','dark','dark','dim']),False)
    check('Created light before damage removes qualification',m.entire_darkness(['bright']),False)
    check('No occupied footprint cannot qualify',m.entire_darkness([]),False)

    begin(23,'Actual Warrior levels8/13/20; three distinct Basic Vital source cards; at13 actual owned Mutation Efficiency; at20 actual active once-encounter Apex Form.',
          'Real slot progression, equipped vs active, actual concurrency-card premise, no slot from feat.',
          'Actual acquisition opportunity/history, dose use and complete Apex duration are not executed; those premises are bound to current cards.')
    vitals=['warrior.supplement.ironhide-graft','warrior.supplement.bloodthick-node','warrior.supplement.spinal-buffer']
    for sid in vitals:check('Actual Basic Vital source '+sid,wc[sid]['prerequisite'],'Warrior 1; Basic Vital','source-data')
    check('Actual Efficiency gate',wc['warrior.arch.mutation-efficiency']['minimumClassLevel'],3,'source-data')
    check('Actual Apex exception gate',wc['warrior.supplement.apex-form']['minimumClassLevel'],20,'source-data')
    reject('Warrior8 cannot equip third Vital',lambda:m.mutation_state(8,vitals,vitals[:2],True))
    check('Warrior13 equipped3 but active2',m.mutation_state(13,vitals,vitals[:2],True),{'slots':3,'acquisitionGate':True,'livingFortressOperative':False})
    reject('Three active without actual exception',lambda:m.mutation_state(13,vitals,vitals,True))
    check('Actual Apex20 can activate3 equipped',m.mutation_state(20,vitals,vitals,True,True),{'slots':4,'acquisitionGate':True,'livingFortressOperative':True})
    check('Expiry returns to ordinary limit/protection off',m.mutation_state(20,vitals,vitals[:2],True),{'slots':4,'acquisitionGate':True,'livingFortressOperative':False})
    reject('No implicit Mutation Efficiency',lambda:m.mutation_state(13,vitals,vitals[:2]))
    reject('Duplicate named mutations cannot fill slots',lambda:m.mutation_state(13,[vitals[0]]*3,[vitals[0]],True))

    begin(24,'Actual qualified Warrior owner with Carrion Signal Gland active; two distinct meaningful hostiles within30/LoE with own Warrior condition provenance.',
          'Pending versus active, identity counts, first positive event, per-round persistence, whole typed packet and no-mitigation exception.',
          'The actual conditions and eligibility must originate from legal source events; model does not fabricate them.')
    a={'creature':'hostile-A','meaningfulHostile':True,'ownWarriorSource':True,'inRange':True,'lineOfEffect':True,'active':True,'suppressed':False,'condition':'Shaken'}
    b=a|{'creature':'hostile-B','active':False,'condition':'Disoriented'}
    guard=m.TerrorGuard();check('Pending second hostile not ready',m.terror_ready([a,b]),False)
    check('Earlier damage receives no reduction',guard.reduce(1,[5],[a,b],True),{'components':[5],'spent':False})
    b['active']=True;check('Actual later transition creates readiness',m.terror_ready([a,b]),True)
    check('Next event reduces once across components',guard.reduce(1,[1,4],[a,b],True),{'components':[0,3],'spent':True})
    check('No second same-round reduction',guard.reduce(1,[5],[a,b],True),{'components':[5],'spent':False})
    check('Zero event leaves new round allowance',guard.reduce(2,[0],[a,b],True),{'components':[0],'spent':False})
    check('Positive1 reduced to0 still spends',guard.reduce(2,[1],[a,b],True),{'components':[0],'spent':True})
    check('NoMitigation transfer not reduced',guard.reduce(3,[5],[a,b],True,True),{'components':[5],'spent':False})
    check('Suppressed own gland not ready',guard.reduce(3,[5],[a,b],False),{'components':[5],'spent':False})
    check('Two records one body are one hostile',m.terror_ready([a,a|{'condition':'Frightened'}]),False)
    for key in ['meaningfulHostile','ownWarriorSource','inRange','lineOfEffect','active']:
        check('Second hostile missing '+key,m.terror_ready([a,b|{key:False}]),False)
    check('Suppressed condition not counted',m.terror_ready([a,b|{'suppressed':True}]),False)

    begin(25,'Actually qualified holder; completed positive-to-zero packet has already resolved Instant Death/Wounds and left living0; next original regular start is the deadline.',
          'No-Action registration despite drop incapacity; same episode; death/earlier heal/HP-gain block; preserved Wounds/Prone.',
          'Full incoming packet/Instant Death, independent unconsciousness, initiative markers and subsequent minute damage rider are not implemented here.')
    u=m.UndyingEpisode(0,wounds=2);check('Register despite drop incapacity',u.register('drop1',5,True),True)
    check('No additional use while pending',u.register('drop2',5,True),False)
    check('Deadline recovers living0',u.resolve('drop1'),True)
    check('Only HP changes, Wounds/Prone remain',[u.hp,u.wounds,u.prone,u.available],[1,2,True,False])
    u=m.UndyingEpisode(0);u.register('drop1',5,True);u.heal(4)
    check('Earlier real healing cancels without HP reduction',[u.resolve('drop1'),u.hp],[False,4])
    u=m.UndyingEpisode(0);u.register('drop1',5,True);u.die()
    check('Actual death cancels, never resurrection',[u.resolve('drop1'),u.alive,u.hp],[False,False,0])
    check('Already dead cannot register',m.UndyingEpisode(0,alive=False).register('old',5,True),False)
    check('No zero-to-zero historical trigger',m.UndyingEpisode(0).register('old',0,True),False)
    u=m.UndyingEpisode(0);u.register('drop1',5,True)
    check('Broad HP-gain block prevents point without refund',[u.resolve('drop1',True),u.hp,u.available],[False,0,False])

    begin(26,'Present own Hemocraft source record, expires10, currently suppressed by Bleed arbitration; actual consume at5, genuine beneficial-rest identity when applicable.',
          'Exact source/owner/presence/expiry, suppression exception, one consumption, empty reserve acquisition, actual restored-HP debit.',
          'Hit acquisition, BA/round/range, actual healing ceilings/Wounds and beneficial-rest authenticity remain independently governed.')
    record={'id':'bleed-A','source':'hemocraft','owner':'A','expires':10,'ended':False,'suppressed':True}
    check('Suppressed own record may be consumed',m.consume_hemocraft(record,'A',5),True)
    reject('Ended record cannot be consumed twice',lambda:m.consume_hemocraft(record,'A',5))
    reject('Another owner cannot consume',lambda:m.consume_hemocraft(record|{'ended':False},'B',5))
    reject('Another Bleed source cannot be consumed',lambda:m.consume_hemocraft(record|{'ended':False,'source':'other-bleed'},'A',5))
    reject('Expired record cannot be consumed',lambda:m.consume_hemocraft(record|{'ended':False},'A',10))
    reserve=m.HemocraftReserve();check('Acquisition begins empty',reserve.remaining,0)
    check('No benefit from empty reserve',reserve.heal(8,5,20),{'hp':5,'gained':0,'remaining':0})
    check('Debt-only rest cannot refill',reserve.refill('rest0',5,False),False)
    check('One actual beneficialLR fills2L',reserve.refill('rest1',5,True),True)
    check('Real headroom caps actual restored/debit',reserve.heal(8,18,20),{'hp':20,'gained':2,'remaining':8})
    check('Replayed rest cannot refill',reserve.refill('rest1',5,True),False)
    check('Finite reserve then exhausted',reserve.heal(8,5,20),{'hp':13,'gained':8,'remaining':0})
    check('No later healing from empty reserve',reserve.heal(8,5,20),{'hp':5,'gained':0,'remaining':0})

    begin(27,'Actual Mage route with no legacy Dragonborn or draconic-Sorcerer receipt; separate hypothetical source-qualified positive receipts marked as premises only.',
          'Exact-name/source-credential predicate; no alias creates ancestry or class.',
          'No claim any actual campaign character has a currently available legacy source; positive receipts only define the gate.')
    check('Mage alone does not equal Sorcerer',m.dragon_blood_eligible([{'actual':True,'class':'Mage','bloodline':'draconic','damageType':'fire'}]),False)
    check('Drakari spelling not Dragonborn',m.dragon_blood_eligible([{'actual':True,'lineage':'Drakari','damageType':'fire'}]),False)
    check('No source receipt means no eligibility',m.dragon_blood_eligible([]),False)
    check('Unproven legacy label fails',m.dragon_blood_eligible([{'actual':False,'lineage':'Dragonborn','damageType':'fire'}]),False)
    check('Conditional exact actual Dragonborn gate',m.dragon_blood_eligible([{'actual':True,'lineage':'Dragonborn','damageType':'fire'}]),True)
    check('Conditional exact draconic Sorcerer gate',m.dragon_blood_eligible([{'actual':True,'class':'Sorcerer','bloodline':'draconic','damageType':'fire'}]),True)
    check('Bloodline without recorded damage type incomplete',m.dragon_blood_eligible([{'actual':True,'class':'Sorcerer','bloodline':'draconic'}]),False)

    begin(28,'Two exact preserved original feat identities and finite wrappers; cosmology postponed until after authorized final push.',
          'Whole source-object preservation and explicit null/unavailable flags; no travel/binding execution.',
          'Cosmology and the actual deferred spell payloads remain unreviewed and unimplemented.')
    for sid in ['astral_projection','planar_binding']:
        check(sid+' null payload',public[sid]['payloadOperational'],None,'source-data')
        check(sid+' disabled/unapproved',[public[sid]['selectionEnabled'],public[sid]['exactApproved'],public[sid]['runtimeApproved']],[False,False,False],'source-data')
        check(sid+' complete original retained',public[sid]['sourceObject'],sources[sid]['originalSourceObject'],'source-data')

    current=None
    check('All28 authored source expectations represented',[x['caseId'] for x in cases],[x['id'] for x in fa],'coverage')
    for c in cases:
        own=[x for x in checks if x['caseId']==c['caseId']]
        c['checks']=len(own);c['failures']=[x['name'] for x in own if not x['pass']]
        c['status']='Named bounded subsets pass; full expectation includes stated source adjudication' if not c['failures'] else 'Failed bounded check'
    paths=[Path(__file__),R/'tools/feat_exact_01_reference_models.py',V/'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json',
           V/'FEAT_327_AUTHORING_REGISTER.json',V/'FEAT_SHARED_DIRECTIONS.md',V/'FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',
           U/'candidate.json',U/'spell_dependencies.json',R/'data/public/class_playtests/warrior.json',
           R/'data/public/class_playtests/mage.json',R/'data/public/class_playtests/dragoon.json',
           R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json',
           R/'docs/mechanics/expedition/EXPEDITION_PART01_DIRECTOR.md',A/'FEAT_EXACT_CANDIDATE_01_BUILD.json']
    failures=[x for x in checks if not x['pass']]
    kinds={k:sum(x['kind']==k for x in checks) for k in sorted({x['kind'] for x in checks})}
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass' if not failures else 'fail',
            'scope':'Named finite reference transitions, arithmetic and source adjudication for all28 FA expectations; not a complete feat interpreter.',
            'sourceVerdict':'FEAT327-SOURCE-2026-10-11','sourceBindings':[binding(p) for p in paths],
            'preservedInputBindingsChecked':preserved,'caseGroups':len(cases),'checkCount':len(checks),
            'checkKinds':kinds,'failureCount':len(failures),'failures':failures,'cases':cases,'checks':checks,
            'independentExpectedValues':True,'importsAssemblyBuilder':False,'fullFeatRuntimeCases':0,
            'candidateReadyForSubmission':False,'exactApproved':False,'catalogPromoted':False,
            'humanBalanceApproved':False,'wholeGameFlowApproved':False,'pushed':False,'cosmologyReviewed':False,
            'remainingAcceptanceWork':[
                'FXC-04 complete supplement operative qualification, all actual selected placement/card dependencies.',
                'FXC-05 all335 printed prerequisite/repeatability cases,175 exact text groups, six training branches, all12 paid Warrior identity pairs, persistent choice/use ledgers.',
                'FXC-06 beyond these named subsets: full active work/incorporation/discount/unsupported recovery source adjudications.',
                'FXC-07 complete task/attack/save/opposed/reroll and damage/healing/source-resource boundaries, not just arithmetic subsets.',
                'FXC-08 real physical setup/trigger/movement/custody/social sequence evidence beyond supplied fixtures.',
                'FXC-09 complete paid spell/copy/secondary/Ready/concentration/ritual/QuickenedThought and command lifecycle sequences.',
                'FXC-10 all660 original positions remain preserved authored expectations; execute applicable independent bounded calculations and audit legal premises;28 FA subsets here do not imply all original examples executed.',
                'FXC-12 manifest-bound final candidate/package/request only after finite acceptance work; actual GPT exact review remains required.'
            ]}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(normal(report),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report':str(args.report),'caseGroups':len(cases),'checks':len(checks),'kinds':kinds,'failures':len(failures),
                      'failedNames':[x['name'] for x in failures],'readyForSubmission':False}))
    if failures:raise SystemExit(1)


if __name__=='__main__':main()
