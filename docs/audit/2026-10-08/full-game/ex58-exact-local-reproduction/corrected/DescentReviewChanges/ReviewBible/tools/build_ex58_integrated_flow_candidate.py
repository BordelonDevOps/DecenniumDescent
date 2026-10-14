"""Author the EX58 synthetic expedition record. This is not a gameplay adapter."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import copy
import hashlib
import json

G = Path(__file__).resolve().parents[3]
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OUT = [R/'data/public/expedition_candidate/integrated_flow.json',
       R/'data/director/expedition_candidate/integrated_flow.json',
       R/'docs/mechanics/expedition/EXPEDITION_INTEGRATED_WALKTHROUGH.md',
       R/'docs/mechanics/expedition/EXPEDITION_INTEGRATED_RECORDS.md',
       A/'EX58_INTEGRATED_FLOW_CANDIDATE_CHECK.json']
OFFSET = 86400  # Departure preparation begins on the second canonical campaign day.
CHECKS = []


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def digest(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest()}


def serial(v):
    if isinstance(v, F):
        return {'numerator': v.numerator, 'denominator': v.denominator}
    if isinstance(v, dict):
        return {k: serial(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [serial(x) for x in v]
    return v


def check(name, condition, actual=None):
    CHECKS.append({'name': name, 'passed': bool(condition), 'actual': serial(actual)})
    if not condition:
        raise AssertionError(name + ': ' + repr(actual))


def clock(t):
    return {'epochId': 'EX-FLOW-SYNTHETIC-EPOCH', 'elapsedSeconds': OFFSET+t,
            'departurePreparationOffsetSeconds': t}


def span(a, b):
    return {'startSeconds': OFFSET+a, 'endSeconds': OFFSET+b,
            'activeSeconds': b-a, 'halfOpen': True}


def hms(t):
    return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d}'


def main():
    for p in OUT:
        if p.exists():
            history=read(A/'ex58-flow-before-policy-binding/manifest.json')
            old=history[p.relative_to(G).as_posix()]
            assert digest(p)['sha256']==old['sha256'], f'Unexpected candidate version; preserve before replacement: {p}'
    seq_path = A/'ex58-final-gpt-verdict/EX58_WORKED_SEQUENCES.json'
    source = read(seq_path)['integratedSequence']
    contracts_path = R/'data/director/expedition_candidate/source_contracts_corrected.json'
    contracts = read(contracts_path)
    inputs = [seq_path, contracts_path, A/'EX58_EDIT_01_FULFILLMENT.json',
              A/'EX58_EDIT_02_FULFILLMENT.json',
              R/'data/public/expedition_candidate/transport_profiles.json']
    for n in range(1, 7):
        inputs += [R/f'data/public/expedition_candidate/part{n:02d}.json',
                   R/f'data/director/expedition_candidate/part{n:02d}.json']
    input_receipts = [digest(p) for p in inputs]
    profiles = read(inputs[4])['profiles']
    mule = next(x for x in profiles if x['name'] == 'Donkey or mule')
    cart = next(x for x in profiles if x['name'] == 'Cart')
    roster = ['Arin', 'Bea', 'Cora', 'Dane']
    offices = {'Expedition Leader': 'Arin', 'Quartermaster': 'Arin',
               'Routekeeper': 'Bea', 'Surgeon': 'Dane', 'Claimant of Record': 'Cora'}
    bodies = [{'id': x, 'kind': 'Expedition character', 'level': 3, 'size': 'Medium',
               'bodyMassLb': 150, 'STR': 14, 'walkingSpeedFt': 30,
               'personalGearMassLb': 24, 'personalGearLoad': F(12, 5),
               'currentHP': 20, 'maximumHP': 20, 'Wounds': 0, 'Strain': 0,
               'conditions': [], 'lastBeneficialLongRest': clock(0),
               'sourceStatus': 'Synthetic fixture values; not a complete or approved character build',
               'acquiredOptionsAdded': [], 'gear': [
                   {'id': x+'-closed-gear', 'massLb': 22 if x in ('Arin','Cora') else 24,
                    'description': 'Owned clothing, bedding and closed personal kit; physical contents stipulated, no combat or magical effect invoked'},
                   *([{'id': 'Lantern-A' if x=='Arin' else 'Lantern-B', 'emptyMassLb': 2,
                       'description': 'Owned hooded lantern, compatible with the purchased oil; fuel counted separately'}]
                     if x in ('Arin','Cora') else [])]} for x in roster]
    bodies += [{'id': 'Mule-1', 'kind': 'significant registered animal',
                'profile': copy.deepcopy(mule), 'currentHP': 20, 'maximumHP': 20,
                'remainingHitDice': 3, 'Wounds': 0, 'Strain': 0,
                'training': ['harness', 'Bea audible stop/walk cues', 'calm feeding'],
                'willing': True, 'carriedHarnessLb': 8, 'carriedHarnessLoad': F(4,5),
                'diet': {'feedLbPerDay': 10, 'waterPintsPerDay': 24},
                'classBond': {'presence': 'absent'}, 'rider': {'presence': 'absent'}},
               {'id': 'Cart-1', 'kind': 'owned drawn frame', 'profile': copy.deepcopy(cart),
                'currentHP': 30, 'occupants': [], 'driver': 'Bea', 'driverWalking': True,
                'originalPrimaryMembers': ['frame-1','axle-1','bed-1'],
                'repairEvents': [], 'nativeCreatureTurn': False}]
    corrections = [{
        'id': 'FLOW-C01', 'status': 'NEW candidate clarification, pending exact GPT review',
        'originalSourcePreserved': True,
        'issue': 'The original chronology debits animal meals at hours 0 and 12 without reserving stationary feeding/watering intervals.',
        'candidateChoice': 'Use actual 30-minute supported stops at [0,1800) and [43200,45000). Human meals and animal care have disjoint assigned workers. The second stop includes the existing 60-second lamp refill, so it is not charged twice.',
        'result': {'addedStopsSeconds': 3600, 'overlappedPreviouslySeparatePauseSeconds': 60,
                   'netAdditionalSecondsToHaven': 3540, 'sourceHavenEntry': 59052,
                   'candidateHavenEntry': 62592, 'sourceRestCompletion': 101052,
                   'candidateRestCompletion': 104592},
        'scope': 'One synthetic itinerary, not a new universal meal duration or a silent amendment to GPT source directions.'}, {
        'id': 'FLOW-C02', 'status': 'NEW explicit synthetic premises',
        'candidateChoice': 'Assign all five offices to named people, name real provider shifts, give the cart a physically traversable withdrawal lane and gate, and preserve walking-driver versus ridden-mount distinctions.',
        'scope': 'Offices grant no proficiency. No pending class, spell or feat is activated.'}]

    # Real physical origin records. Amounts are never duplicated as an abstract Supply asset.
    lots = [
        {'id':'food-0', 'item':'sealed ration-equivalent food', 'amount':F(16), 'unit':'lb', 'massLb':F(16), 'packedAt':clock(-36000), 'expiresAt':clock(-36000+30*86400), 'costCp':400},
        {'id':'water-human-0', 'item':'potable water', 'amount':F(64), 'unit':'pint', 'massLb':F(64), 'costCp':8},
        {'id':'feed-0', 'item':'species-compatible mule feed', 'amount':F(20), 'unit':'lb', 'massLb':F(20), 'costCp':10},
        {'id':'water-mule-0', 'item':'potable water', 'amount':F(48), 'unit':'pint', 'massLb':F(48), 'costCp':6},
        {'id':'sundries-0', 'item':'ordinary expendable cleaning cloth and twine', 'amount':F(2), 'unit':'lb', 'massLb':F(2), 'costCp':16},
    ]
    lots += [{'id':f'oil-{n}', 'item':'compatible lamp oil', 'amount':F(1), 'unit':'pint',
              'massLb':F(3,4), 'containerId':f'flask-{n}', 'costCp':10,
              'fullInclusiveMassLb':F(1)} for n in range(1,9)]
    for lot in lots:
        lot.update({'owner':'Expedition-1', 'origin':'actual finite stock sold before this descent, synthetic seller receipt',
                    'creationByRule':False, 'transfersResetAge':False,
                    'restrictions':['ordinary nonmagical stock; no recipe/harvest output implied']})
    containers = [
        *[{'id':f'skin-{n:02d}', 'emptyMassLb':1, 'capacityPints':4,
           'openingContents': {'lot':'water-human-0' if n<=16 else 'water-mule-0', 'pints':4},
           'location':'Cart-1', 'ownedBeforeEpisode':True, 'cleanAndCompatible':True}
          for n in range(1,29)],
        *[{'id':f'flask-{n}', 'emptyMassLb':F(1,4), 'capacityPints':1,
           'openingContents':{'lot':f'oil-{n}', 'pints':1}, 'location':'Cart-1',
           'retainedWhenEmpty':True, 'cleanAndCompatible':True} for n in range(1,9)],
        *[{'id':f'feedbag-{n}', 'emptyMassLb':1, 'capacityLb':10,
           'openingContents':{'lot':'feed-0','lb':10}, 'location':'Cart-1',
           'ownedBeforeEpisode':True} for n in (1,2)]
    ]
    supply = {'basketCountForPurchase':8, 'abstractSupplyBalanceExists':False,
              'basketPurchaseCp':504, 'animalFeedWaterPurchaseCp':16,
              'lots':lots, 'containers':containers,
              'packing':{'initialPreallocationPayloadLb':188, 'initialGrossDrawLb':388,
                         'contentsFit':{'bedFt':[6,4,3], 'allocatedStorageFt3':24,
                                       'longestPackedBundleFt':3, 'crateFt':[2,1,1],
                                       'closure':'sealed skins and flasks; lashed food/feed bags and closed crate'},
                         'noDoubleTare':'8 full 1-lb flasks already include 2 lb of flask bodies; water is separate from the 28 one-pound skins.'}}

    consumption = []
    def consume(cid, lot, actor, start, end, amount, unit, day):
        consumption.append({'id':cid, 'lotId':lot, 'recipient':actor, 'interval':span(start,end),
                            'relativeStart':start,'relativeEnd':end,'amount':F(amount), 'unit':unit,
                            'canonicalRelativeDay':day, 'evidence':'authored actual supported interval',
                            'creditsNutritionOnce':unit in ('lb','pint') and lot!='sundries-0'})
    human_meals = {}
    for person in roster:
        human_meals[person] = [(0,900), ((43320 if person in ('Arin','Cora') else 43200),
                                       (44220 if person in ('Arin','Cora') else 44100)),
                              (86400,87300),(129600,130500)]
        for i,(start,end) in enumerate(human_meals[person]):
            consume(f'meal-{person}-{i}-food','food-0',person,start,end,1,'lb',i//2)
            consume(f'meal-{person}-{i}-water','water-human-0',person,start,end,4,'pint',i//2)
    for i,(start,end) in enumerate([(900,1800),(44100,45000),(86400,87300),(129600,130500)]):
        consume(f'mule-meal-{i}-feed','feed-0','Mule-1',start,end,5,'lb',i//2)
        consume(f'mule-meal-{i}-water','water-mule-0','Mule-1',start,end,12,'pint',i//2)
    for i,(start,end) in enumerate([(900,960),(44220,44280),(87300,87360),(130500,130560)]):
        consume(f'cleaning-{i}','sundries-0','Expedition shared cleanup',start,end,F(1,2),'lb',i//2)

    burns = []
    refills = []
    transfers = [
        {'id':'initial-A','time':clock(-30000),'from':'flask-1','to':'Lantern-A','lotId':'oil-1','pints':F(1)},
        {'id':'initial-B','time':clock(-29940),'from':'flask-8','to':'Lantern-B','lotId':'oil-8','pints':F(7,360)}]
    main_start = 0
    for n in range(1,9):
        end = min(main_start+21600,172800)
        burns.append({'id':f'burn-A-{n}', 'lantern':'Lantern-A', 'lotId':f'oil-{n}',
                      'relativeStart':main_start,'relativeEnd':end,'interval':span(main_start,end),
                      'pints':F(end-main_start,21600),'lightCoverage':'declared safe occupied area and route, not unlimited radius'})
        if n<8:
            workers = ['Arin','Cora'] if n<=2 else (['Iris','June'] if end<115200 else ['Leto','Mara'])
            refills.append({'id':f'refill-{n}', 'interval':span(end,end+60),
                            'relativeStart':end,'relativeEnd':end+60,
                            'mainWorker':workers[0], 'backupWorker':workers[1],
                            'hands':{'mainWorker':2,'backupWorker':1},
                            'method':'Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.',
                            'travelPauseAddedSeconds':60 if n==1 else 0,
                            'reason': 'Independent route pause' if n==1 else ('Inside the existing meal stop' if n==2 else 'Actual Haven provider work; no travel underway')})
            burns.append({'id':f'burn-B-{n}', 'lantern':'Lantern-B','lotId':'oil-8',
                          'relativeStart':end,'relativeEnd':end+60,'interval':span(end,end+60),
                          'pints':F(1,360),'lightCoverage':'same supported area for this minute'})
            transfers.append({'id':f'pour-A-{n}', 'time':clock(end+60), 'from':f'flask-{n+1}',
                              'to':'Lantern-A','lotId':f'oil-{n+1}',
                              'pints':F(1) if n<7 else F(353,360)})
            main_start=end+60
    light={'burns':burns,'refills':refills,'transfers':transfers,
           'rate':'1 pint per 21600 actual lit seconds', 'noFreeBackupFuel':True,
           'totalOriginalOilPints':F(8), 'totalEmptyFlaskMassLb':F(2),
           'nextOilPreparation':{'interval':span(151620,151680), 'actor':'Mara',
                                 'from':'next-flask-1','to':'Lantern-B','pints':F(1),
                                 'lotId':'oil-next-1', 'ignitionAt':clock(172800),
                                 'oldBurnsUnchanged':True,'costIncludedInNextProcurement':True}}

    moving = [span(1800,21600),span(21660,30660),span(31932,43200),span(45000,62532)]
    route={'id':'route-known-1','outboundEndpoints':['Haven door','licensed store entrance'],
           'returnEndpoints':['withdrawal gate','Haven inspection point'],
           'routeQuality':'Known','qualityFactor':F(1),'Mapping':'Mapped','Risk':1,
           'lengthProgressEachDirection':F(2),'capacityLoad':F(60),
           'capacityConvention':'This fixture counts freight, personal gear, empty frame and harness once. Self-moving bodies use separate floor/bridge support facts, not passenger burden.',
           'conservativeFreightUpperBoundLoad':F(256,5),
           'support':{'combinedSelfMovingBodiesLb':1000,'freightUpperBoundLb':512,
                      'continuousSupportedFloorRatingLb':2000,
                      'minimumWidthFt':12,'minimumHeightFt':12,
                      'terrain':'firm level rolling surface; no gap, stairs, slope or closed obstacle',
                      'turns':'straight lane or actual swept turning areas at least 30 by 30 feet'},
           'pace':{'charactersFt':30,'muleBaseFt':40,'drawBurdenPenaltyFt':10,
                   'currentMuleFt':30,'cartCapFt':40,'convoyMph':3,
                   'nominalSecondsEachDirection':28800,'movingSecondsEachDirection':28800},
           'movingIntervals':moving,'ordinaryProgressTotal':4,'additionalMileageAward':0,
           'extractionCheckpoint':{'id':'route-known-return-exit','position':F(2),
                                   'reasons':['Mapped Length under 6 exit'],
                                   'inspection':span(62532,62592)}}
    timeline = [
        ('E01',0,0,'Charter, roster and opening funds are carried from actual signed prior records.'),
        ('E02',0,1800,'Feed and water before departure. Human meals finish first; Bea and Dane then care for the mule. Arin and Cora finish cleanup. Depart at 00:30.'),
        ('E03',21600,21660,'Arin refills A while Cora holds the prepared B. The convoy stops for exactly this minute.'),
        ('E04',28800,28800,'Watch 0 checkpoint: Pressure 1, natural 5, no complication. The route has not yet finished.'),
        ('E05',30660,30660,'Arrive at 08:31 after exactly 480 moving minutes. Gain the single mapped 2 Progress.'),
        ('E06',30660,31860,'Verify release markings and free the 20-lb closed crate. Dane takes it in two hands; Cora records title. Class 2 adds one Pressure on genuine extraction.'),
        ('E07',31860,31866,'Retreat round 1 uses the existing actors and budgets. Arin earns one Escape; one legal opposing attack misses.'),
        ('E08',31866,31872,'Retreat round 2: Arin earns two Escape from the shifted critical. One attack misses; Cora uses her readied gate closure after the threat. Everyone is beyond the actual gate.'),
        ('E09',31872,31932,'Dane and Cora load and lash the closed crate into the stopped cart for one actual minute. Begin the return at 08:52:12.'),
        ('E10',43200,45000,'Stop for the second feeding/watering period. Arin and Cora refill A with B backup at 12:01–12:02, then eat. Bea and Dane eat first and tend the mule second. This is one 30-minute pause.'),
        ('E11',57600,57600,'Watch 1: open combat adds one Pressure, 3 to 4. Natural 5 gives no complication. Return travel still needs 82 minutes 12 seconds.'),
        ('E12',62532,62592,'Reach the exit at 17:22:12. Arin performs the separately timed minute of extraction verification: natural 11 plus 5 meets DC 16.'),
        ('E13',62592,62592,'Settle the exposed partial Watch once, natural 6 at Pressure 4. Actually enter the secured Haven and apply one reduction to Pressure 3.'),
        ('E14',62592,75792,'Complete the nine timed Haven steps in 220 minutes, including actual sale, charges, standing notice and the next charter. Named provider workers handle the lamps.'),
        ('E15',86400,86400,'Settle day 0 nutrition, the missed scheduled Rest and one canonical faction checkpoint. Actual Rest remains in progress. Day 1 breakfast follows as light activity during Rest.'),
        ('E16',104592,104592,'At 29:03:12 the eight-hour safe Rest ends. Its 16 minutes of supported breakfast/cleanup leave over six hours of sleep. Clear the debt before hour 40 and grant only the eligible first beneficial Long Rest.'),
        ('E17',129600,130560,'Complete day 1 second-half meals and cleanup with actual stock. Named staff separately tend the mule and lamps.'),
        ('E18',140400,140400,'At hour 39 close the first expedition accounts and divide only profit after the agreed next reserve.'),
        ('E19',142200,143520,'Buy new stock at 39:30, refill all 28 now-empty skins with four separate workers, receive sealed food/feed/oil, and pack before hour 40. Old flask bodies are retained.'),
        ('E20',144000,144000,'Begin the scheduled 40–48-hour safe Rest. The prior beneficial completion is 29:03:12, so this Rest cannot grant another benefit at 48.'),
        ('E21',172800,172800,'Settle day 1 support and Rest completion before next departure. Old oil totals exactly eight pints used; B already holds separately paid new oil. Cash, Pressure 3, standing, assets and source statuses carry forward.')]

    haven_steps=[]
    start=62592
    for name,minutes,actors in [
        ('intake',10,['Arin','Ione']),('quarantine inspection',10,['Dane','Oren']),
        ('provenance',30,['Cora','Ione']),('known finite appraisal and quote',30,['Cora','Pera']),
        ('buyer agreement',30,['Arin','Pera']),('ledger and claims',30,['Arin','Ione']),
        ('standing notice',10,roster+['Ione']),('advancement record',10,['Arin','Dane']),
        ('prospective next charter',60,roster)]:
        end=start+minutes*60
        haven_steps.append({'id':'haven-'+name.replace(' ','-'),'activity':name,
                            'actors':actors,'interval':span(start,end),
                            'relativeStart':start,'relativeEnd':end,
                            'completion':'Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture'})
        start=end
    check('Haven steps occupy exactly 220 minutes',start==75792,start)
    providers={'rooms':{'id':'ROOM-1','owner':'Sera','recipients':roster,
                         'term':span(62592,177792),'priceCp':800,
                         'realFacilities':['four safe beds','secure dry gear storage','potable-service access'],
                         'includedWork':'Staff keep the party-owned lamps fueled using party-owned finite oil; no new party provisions or training credit.'},
               'stable':{'id':'STABLE-1','owner':'Toma','animal':'Mule-1','term':span(62592,235392),
                          'priceCp':100,'facilities':'fitting Large stall, safe water/feed access, actual staff',
                          'partyStockUsed':True,'automaticHealing':False},
               'lampShifts':[{'actors':['Iris','June'],'interval':span(62592,115200)},
                             {'actors':['Leto','Mara'],'interval':span(115200,172800)},
                             {'actors':['Iris','June'],'interval':span(172800,177792)}],
               'providerRest':[{'actors':['Iris','June'],'interval':span(115200,144000)},
                               {'actors':['Leto','Mara'],'interval':span(86400,115200)}],
               'muleCare':[{'actor':'Nell','interval':span(86400,87300)},
                           {'actor':'Orin','interval':span(129600,130500)}],
               'authority':'All provider bodies, own support, wages, permissions and facility capacities are explicit synthetic premises. A payment alone is not used as proof of a worker.',
               'externalNotRoster':True}

    # Costs are each one real transaction. Capital and allocations never masquerade as expenses.
    tx=[]
    def pay(tid,t,amount,payer,payee,kind,episode='first'):
        tx.append({'transactionId':tid,'time':clock(t),'relativeTime':t,
                   'payer':payer,'payee':payee,'exactCp':F(amount),'settledCp':amount,
                   'rounding':'sale floor once' if kind=='sale' else 'purchase/fee ceil once',
                   'status':'paid','kind':kind,'episode':episode})
    pay('buy-human-0',-34000,504,'Expedition cash','Provisioner','operating cost')
    pay('buy-animal-0',-33900,16,'Expedition cash','Provisioner','operating cost')
    pay('premium-0',-33000,600,'Expedition cash','Underwriter','operating cost')
    pay('room-fee',62592,800,'Expedition cash','Sera','operating cost')
    pay('stable-fee',62592,100,'Expedition cash','Toma','operating cost')
    pay('mandatory-inspection',63792,200,'Expedition cash','Haven inspector','mandatory')
    pay('sale-crate',69192,12000,'Pera','Expedition cash','sale')
    pay('levy',70992,600,'Expedition cash','Haven treasury','tax')
    pay('guild-share',70992,2240,'Expedition cash','Local guild','sponsor')
    for person in roster:
        pay('distribution-'+person,140400,1235,'Expedition cash',person,'profit distribution')
    pay('next-stock',142200,520,'Expedition cash','Provisioner','next inventory purchase','next')
    money={'startingCapitalCp':3000,'transactions':tx,
           'sponsor':{'id':'SPONSOR-1','rate':F(1,5),'base':'gross less one applicable tax and mandatory rescue/quarantine',
                      'signedBeforeDeparture':True,'grossGrantOrLoan':False},
           'policy':{'id':'INSURANCE-1','insuredLot':'crate-1','insuredValueCp':12000,
                     'premiumRate':F(1,20),'premiumPayment':'premium-0','term':span(0,62592),
                     'provenance':'documented licensed title and inspected original lot',
                     'provenancePayoutRate':F(9,10),'episodeDeductibleCp':2400,
                     'premiumAndPayoutAreIndependent':'Ordinary cargo selects the 5% premium; documented provenance separately selects the 90% loss-rate formula. No loss occurred.',
                     'lossEvents':[],'claims':[],'payoutCp':0,'status':'closed without claim'},
           'settlement':{'grossCp':12000,'taxCp':600,'mandatoryCp':200,'sponsorBaseCp':11200,
                         'sponsorCp':2240,'netCp':8960,'uniqueOtherOperatingCostsCp':2020,
                         'trueProfitCp':6940,'nextReserveCp':2000,'distributionCp':4940,
                         'eachCharacterCp':1235,'cashBeforeDistributionCp':9940,
                         'cashAfterDistributionCp':5000,'nextProcurementCp':520,
                         'finalCashCp':4480,'capitalStillCashCp':3000,'unspentEarmarkCp':1480,
                         'nextInventoryPaidCostCp':520,'unpaidLiabilitiesCp':0}}

    pressure_events=[{'id':'initial-risk','relativeTime':0,'before':0,'delta':1,'after':1,'cause':'actual Risk 1 floor'},
                     {'id':'class-highwater','relativeTime':31860,'before':1,'delta':1,'after':2,'cause':'Class 2 extraction first surcharge','highwater':1},
                     {'id':'successful-retreat','relativeTime':31872,'before':2,'delta':1,'after':3,'cause':'successful retreat once'},
                     {'id':'watch1-open-combat','relativeTime':57600,'before':3,'delta':1,'after':4,'cause':'one open combat category, both rounds same Watch'},
                     {'id':'actual-secured-entry','relativeTime':62592,'before':4,'delta':-1,'after':3,'cause':'move onto genuinely secured route','WatchReductionCreditsUsed':1}]
    pressure_tests=[{'id':'watch0','time':clock(28800),'Pressure':1,'naturalD6':5,'result':'none'},
                    {'id':'watch1','time':clock(57600),'Pressure':4,'naturalD6':5,'result':'none'},
                    {'id':'partial-watch2','time':clock(62592),'Pressure':4,'naturalD6':6,'result':'none',
                     'phase':'before secured-entry reduction','laterWatch2Repeat':False}]
    retreat={'id':'retreat-1','participants':roster+['Mule-1','Opponent-1'],
             'vehicleIsNotCreature':'Cart-1',
             'estimate':{'status':'authored bounded attack context only; not a calibrated full enemy build',
                         'actualCharacters':4,'characterLevels':[3,3,3,3],
                         'absentRosterMembers':0,'opponentCR':{'presence':'absent'},
                         'separateCalibrationBoundariesStillRequired':True},
             'route':{'lengthFt':60,'minimumWidthFt':12,'startingPositions':'all withdrawing bodies and whole cart can clear the real gate after two 30-foot coherent movements',
                      'gate':'actual manual lever next to Cora at final position; closes after the second opposing attack; no new magical barrier'},
             'leadCheck':{'actor':'Arin','ability':'WIS','skill':'Survival','modifier':5,
                          'sourceOfModifier':'synthetic acquired proficiency plus ability total, counted once',
                          'DC':16,'baseTierIIDC':13,'declaredSuperiorPursuit':3},
             'rounds':[],'terminal':{'Escape':3,'Pursuit':0,'winner':'retreat before Pursuit 3',
                                    'sameEncounterResourcesRetained':True,'enemyDeath':False,'lootCreated':False}}
    for n, natural, total, escape in [(1,11,16,1),(2,20,25,2)]:
        budgets={p:{'stance':'Mobile','movementSpentFt':30,'ActionSpent':True,
                    'BonusActionSpent':False,'ReactionSpent':False} for p in roster}
        budgets['Arin']['Action']='one escape check while carrying A in the other available hand'
        budgets['Bea']['Action']='driver command/brake contribution; walks with reins, no cart seat'
        budgets['Cora']['Action']='Dodge' if n==1 else 'Ready manual gate closure after the one enemy attack'
        budgets['Cora']['ReactionSpent']=n==2
        budgets['Dane']['Action']='Dodge while carrying crate in both hands; no weapon attack'
        retreat['rounds'].append({'round':n,'interval':span(31860+(n-1)*6,31860+n*6),
                                 'initiative':['Arin','Bea','Mule-1','Cora','Dane','Opponent-1'],
                                 'driverContributionReservedBeforeMule':True,
                                 'drive':{'id':f'drive-{n}','mover':'Mule-1','carrier':'Cart-1',
                                          'initiator':'Bea','distanceFt':30,'selfPowered':True,
                                          'pullerMoveSpentFt':30,'pullerAction':'Dodge',
                                          'resolvesAfterRequiredContributions':True,'vehicleDriveCount':1},
                                 'actorBudgets':budgets,'leadDie':natural,'leadTotal':total,
                                 'numericalDegree':'Success','naturalShift':'up one to Critical Success' if n==2 else 'none',
                                 'EscapeAdded':escape,'PursuitAdded':0,
                                 'threat':{'actor':'Opponent-1','attackBonus':3,'naturalDie':n+1,
                                           'total':n+4,'target':'Arin','AC':13,'nativeResult':'miss',
                                           'actualReachFt':5,'actualTargetDistanceFt':5,
                                           'movementAvailableFt':30,'damage':0,'otherThreats':0},
                                 'otherGenericEscapeAwards':0})
    # Positions use a 20-foot-wide straight withdrawal chamber, within the route's
    # declared minimum requirements. All rectangles translate coherently; the gate
    # is closed only after the last real threat, with every friendly body clear.
    retreat['route']['actualChamberWidthFt']=20
    retreat['route']['gatePlaneXFt']=35
    retreat['route']['gateLeverPointFt']=[39,F(35,2)]
    retreat['route']['startingRectanglesFt']={
        'Cart-1':{'x':[-23,-15],'y':[F(15,2),F(25,2)]},
        'Mule-1':{'x':[-10,0],'y':[5,15]},
        'harness-gap':{'x':[-15,-10],'y':[9,11]},
        'Arin':{'x':[-25,-20],'y':[0,5]},
        'Bea':{'x':[-20,-15],'y':[F(25,2),F(35,2)]},
        'Cora':{'x':[-25,-20],'y':[15,20]},
        'Dane':{'x':[-20,-15],'y':[0,5]},
        'Opponent-1':{'x':[-30,-25],'y':[0,5]}}
    retreat['route']['geometryMeaning']='Actual authored rectangles in feet. Each actor advances 30 feet per round; the harness and cart translate with the mule. Side lanes keep walkers clear of the vehicle and puller. Gate closure at x=35 separates the opponent from the whole friendly convoy after round 2.'
    retreat['route']['opponentContext']={'walkingSpeedFt':30,'attackBonus':3,'reachFt':5,
        'ActionsPerRound':1,'opportunityAttacksTaken':0,
        'singleThreatChoice':'Opponent uses its predeclared one attack on its regular turn, declining extra opportunity attacks. No second abstract threat is imposed.'}
    for turn in retreat['rounds']:
        distance=turn['round']*30
        turn['endingRectanglesFt']={k:{'x':[v+distance for v in rect['x']],'y':rect['y']}
                                    for k,rect in retreat['route']['startingRectanglesFt'].items()}
    extraction={'id':'extract-1','start':clock(31860),'destination':'Haven inspection point',
                'crate':{'id':'crate-1','massLb':20,'Load':F(2),'outerFeet':[2,1,1],
                         'Class':2,'priority':1,'tags':[],'closed':True,'condition':'unchanged sound ordinary material',
                         'title':'licensed assignment verified from actual stipulated release record',
                         'custody':[{'from':clock(31860),'to':clock(31932),'custodian':'Dane'},
                                    {'from':clock(31932),'to':clock(69192),'custodian':'Expedition in Cart-1'},
                                    {'from':clock(69192),'custodian':'Pera, actual paid buyer'}]},
                'surchargeHighwater':1,'checkpoints':[{'id':'route-known-return-exit','position':F(2),
                'interval':span(62532,62592),'actor':'Arin','nativeRoute':'Core fixed DC task',
                'DCInputs':{'tier':13,'Class':2,'Attention':0,'Burden':1,'unsecuredDangerous':0,'pursuit':0,'Secured':0},
                'DC':16,'natural':11,'modifier':5,'total':16,'degree':'Success',
                'processedCount':1,'cargoLoss':[],'addedPressure':0}],
                'pendingQueue':[],'terminal':'arrived with crate, closed once'}

    standing={'subject':'Expedition-1 members as recorded counterparties', 'institution':'FX-LOCAL-GUILD',
              'sourceVersion':'standing-v1 synthetic campaign state','policy':'standing-v1',
              'rawSource':'{"FX-LOCAL-GUILD":0}', 'presence':'value','rawValue':0,
              'initialContribution':{'origin':'declared existing neutral relationship','backgroundContributionApplied':False},
              'sceneId':'licensed-return-1','openingScore':0,
              'events':[{'id':'licensed-recovery-delivered','causeId':'crate-1-return',
                         'time':clock(70992),'knownBy':['Ione','Pera'],
                         'evidence':['actual original license','same crate inspected','buyer transfer witnessed'],
                         'proposedDelta':1,'signedSceneSum':1,'sceneCappedDelta':1,
                         'appliedDelta':1,'overflow':0,'endingScore':1}],
              'derivedView':{'score':1,'band':'Liked'},'replayedReportsDelta':0,
              'otherRegistryEntriesChanged':0,'buyerQuoteRetroactivelyRepriced':False}
    faction={'institution':'FX-LOCAL-GUILD','watchedCount':1,
             'action':{'id':'proof-review-1','type':'Research','actor':'Rhea',
                       'interval':span(50400,79200),'activeSeconds':28800,
                       'tools':['actual local title archive','written charter','received intake copies'],
                       'stock':'ordinary owned writing stock; no party ingredients or magical output',
                       'permissions':'actual synthetic local archive authority',
                       'result':'confirm existing release and receipt, no new ownership or secret lore',
                       'additionalGenericRoll':'none; genuine known paperwork is not an uncertain new claim'},
             'receivedInformation':[{'actor':'Milo','interval':span(65592,66192),
                                     'payload':'copy of the actual completed provenance record',
                                     'source':'Ione','recipient':'Rhea'}],
             'checkpoints':[{'id':'actual-return','time':clock(62592),'actionId':'proof-review-1',
                             'activeSecondsSoFar':12192,'status':'still in progress; no extra action'},
                            {'id':'canonical-day0','time':clock(86400),'actionId':'proof-review-1',
                             'completedAt':clock(79200),'status':'report already completed real work once'}],
             'clock':{'id':'claim-proof','kind':'Claim','length':4,'opening':2,
                      'segments':[{'id':'actual-proof-accepted','causeId':'proof-review-1','time':clock(79200),'delta':1}],
                      'ending':3,'thresholdTriggered':False,'duplicateNoticeDelta':0},
             'standingEffectOfDuplicateProof':0,'rivalFrame':{'applicable':False,'reason':'No rival is introduced by this fixture'},
             'audience':'Only the synthetic public desk relationship is shown. No original private faction dossier or resonance data is projected.'}

    rest={'prospectiveDay0Slot':span(57600,86400),'actualFirst':span(75792,104592),
          'debtEvents':[{'id':'missed-rest-0','time':clock(86400),'actors':roster,
                         'deadline':clock(144000),'StrainAtOpening':0},
                        {'id':'clear-debt','time':clock(104592),'actors':roster,'debtRemaining':False,'deadlineStrain':0}],
          'firstRestLightActivity':[span(86400,87300),span(87300,87360)],
          'firstRestSleepSeconds':27840,'firstBeneficial':True,
          'previousBeneficialCompletion':clock(0),'secondActual':span(144000,172800),
          'secondBeneficial':False,'secondsBetweenCompletions':68208,
          'noNewHPNeeded':True,'HPAfter':{p:20 for p in roster},
          'classResourceChanges':[],'simultaneousCraftTrainingResearchSeconds':0,
          'extraWork':'Return travel and required Haven operations replace part of scheduled Rest; no third productive crafting/research/training Watch is awarded.'}
    procurement={'id':'next-procurement','payment':'next-stock','start':clock(142200),
                 'completion':clock(143520),'newOriginLots':[
                     {'id':'food-next','lb':16},{'id':'water-human-next','pints':64},
                     {'id':'feed-next','lb':20},{'id':'water-mule-next','pints':48},
                     {'id':'sundries-next','lb':2},
                     *[{'id':f'oil-next-{n}','pints':1,'container':f'next-flask-{n}'} for n in range(1,9)]],
                 'waterFilling':{'interval':span(142200,142620),'workers':roster,
                                 'assignment':{p:[f'skin-{n:02d}' for n in range(i*7+1,i*7+8)] for i,p in enumerate(roster)},
                                 'minutesPerSkin':1,'totalWorkerMinutes':28,'elapsedMinutes':7},
                 'remainingPacking':{'interval':span(142620,143520),'workers':roster,
                                     'method':'Receive sealed fitting bundles, place/secure disjoint bundles with actual access; no new harness or vehicle is purchased'},
                 'oldContainerHistoryRetained':True,'nextPreallocationPayloadUpperBoundLb':190,
                 'newFuelAlreadyInLanternBAtDeparturePints':1,
                 'oldOilAtDeparturePints':0,'costChargedToCompletedEpisodeAgain':0}

    def consumed(lot,t):
        return sum((x['amount']*F(max(0,min(t,x['relativeEnd'])-x['relativeStart']),
                                  x['relativeEnd']-x['relativeStart'])
                    for x in consumption if x['lotId']==lot), F(0))

    def oil_used(t,lantern=None):
        return sum((F(max(0,min(t,x['relativeEnd'])-x['relativeStart']),21600)
                    for x in burns if lantern is None or x['lantern']==lantern),F(0))

    def snapshot(t, before_safe_entry=False):
        pressure=0
        for x in pressure_events:
            if x['relativeTime']<=t and not (before_safe_entry and x['id']=='actual-secured-entry'):
                pressure=x['after']
        cash=3000
        for x in tx:
            if x['relativeTime']<=t and not (before_safe_entry and x['transactionId'] in ('room-fee','stable-fee')):
                cash += x['settledCp'] if x['payee']=='Expedition cash' else -x['settledCp']
        outstanding_debt=86400<=t<104592
        return {'time':clock(t),'cashCp':cash,'Pressure':pressure,
                'oldPhysicalStockRemaining':{
                    'humanFoodLb':F(16)-consumed('food-0',t),
                    'humanWaterPints':F(64)-consumed('water-human-0',t),
                    'muleFeedLb':F(20)-consumed('feed-0',t),
                    'muleWaterPints':F(48)-consumed('water-mule-0',t),
                    'sundriesLb':F(2)-consumed('sundries-0',t),
                    'oilPints':F(8)-oil_used(t)},
                'oldOilUsedPints':oil_used(t),'retainedFlaskBodyMassLb':F(2),
                'newStockPurchased':t>=142200,'newStockIsOldStockRefill':False,
                'crateCustodian':'licensed store' if t<31860 else ('Dane' if t<31932 else ('Expedition in Cart-1' if t<69192 else 'Pera')),
                'humanHP':{p:20 for p in roster},'muleHP':20,'cartHP':30,
                'humanStrain':{p:0 for p in roster},'RestDebtOwed':{p:outstanding_debt for p in roster},
                'guildStanding':1 if t>=70992 else 0,'newLevelsAwarded':0,
                'beneficialLongRestsSinceDeparture':int(t>=104592),
                'newSpellClassFeatPromotions':0}

    events=[]
    for index,(eid,start,end,note) in enumerate(timeline,1):
        original=next(x for x in source['events'] if x['id']==eid)
        events.append({'id':eid,'schemaVersion':'EX58-flow-event-v1','version':index,
                       'expectedPredecessorVersion':index-1,'time':{**clock(end),'phase':'after recorded interval','sequence':index},
                       'interval':span(start,end),'relativeStart':start,'relativeEnd':end,
                       'sourceEventId':eid,'sourceElapsedSeconds':original['elapsedSeconds'],
                       'status':'resolved','audience':'public synthetic worked example',
                       'evidence':'authored expectation with separately executed exact reference arithmetic',
                       'sourceBindings':[{'path':seq_path.relative_to(G).as_posix(),'pointer':'/integratedSequence/events/'+str(index-1),'sha256':input_receipts[0]['sha256']}],
                       'currentCandidateNarrative':note,'stateAfter':snapshot(end,before_safe_entry=eid=='E12')})

    records={
        'EC-01':{'expeditionId':'Expedition-1','charterVersion':{'id':'charter-1','next':'charter-2','acceptedBy':roster},
                 'roster':roster,'teams':{'Combat':roster,'Reconnaissance':['Bea'],'Research':[], 'Resource':['Cora'],'Support':['Dane'], 'assignmentOverlap':'Job labels are not concurrent task credit'},
                 'offices':offices,'objective':{'id':'licensed-crate-retrieval','evidence':'same licensed crate delivered'},
                 'thresholds':{'returnBySeconds':172800,'grossAtLeastCp':10000,'netAtLeastCp':8000,'profitAtLeastCp':6000,'nextReserveCp':2000,'casualtyAbort':'any member missing or incapacitated; never triggered'},
                 'finance':money,'participants':bodies,'closure':{'realHavenEntry':clock(62592),'nextDeparture':clock(172800),'unresolvedObligations':[]}},
        'EC-02':{'epochId':'EX-FLOW-SYNTHETIC-EPOCH','interval':span(0,172800),'actorId':roster,
                 'activityId':'full-expedition-timeline','reservedResources':{'retreat':retreat['rounds'],'refills':refills,'Haven':haven_steps,'mealIntervals':consumption},
                 'activeProgressSeconds':{'travel':57600,'Haven':13200,'extraStops':3600,'overlapAlreadyCounted':60},
                 'rest':rest,'restDebt':rest['debtEvents'],'completion':'one continuing clock; detailed event states supplied'},
        'EC-03':{'lotId':'physical-manifest-1','identity':lots,'amount':'See exact per-lot rational quantities',
                 'massAndGeometry':supply['packing'],'clockAndCondition':{'sameOriginalLots':True,'newProcurement':procurement},
                 'custody':containers,'originRestrictions':'Ordinary purchased stock only; no new magical, harvest or crafting output',
                 'allocation':consumption,'dailyDemand':{'humanEach':{'foodLb':2,'waterPints':8},'Mule-1':{'feedLb':10,'waterPints':24}},'support':light},
        'EC-04':{'opportunityId':{'applicable':False,'reason':'No forage or camp construction is performed'},
                 'ordinaryAllocation':[],'site':providers,'campTierAndMarks':{'applicable':False},'materialBill':[],
                 'functionalFacts':'Actual contracted Haven beds/stall, not a camp-tier benefit','storage':'Rooms and stall physically fit listed occupants and gear','supplyLine':{'applicable':False}},
        'EC-05':{'routeId':route['id'],'lengthProgress':2,'riskMappingQuality':{k:route[k] for k in ('Risk','Mapping','routeQuality','qualityFactor')},
                 'capacityAndAccess':{k:route[k] for k in ('capacityLoad','capacityConvention','support')},
                 'pace':route['pace'],'tranche':route['movingIntervals'],'mappingAndRecon':'Existing genuine mapped route, no new Recon bonus',
                 'forcedMarch':{'performed':False},'result':{'outboundProgress':2,'returnProgress':2,'HavenEntry':clock(62592)}},
        'EC-06':{'cohortId':'Expedition-1 together','pressure':pressure_events,'causeEvents':[x['id'] for x in pressure_events],
                 'extractionEpisode':extraction,'checkpoints':extraction['checkpoints'],'test':extraction['checkpoints'][0],
                 'complication':pressure_tests,'response':'No complication triggered; no invented delay/loss','queue':[]},
        'EC-07':{'encounterId':retreat['id'],'participants':retreat['participants'],'estimate':retreat['estimate'],
                 'retreat':retreat['route'],'roundBudgets':retreat['rounds'],'counters':retreat['terminal'],
                 'consequences':{'HPChanges':[],'StrainChanges':[],'PressureEvent':'successful-retreat','enemyLoot':[]}},
        'EC-08':{'sourceRow':[mule['id'],cart['id']],'body':bodies[-2:],
                 'payload':{'supply':supply,'crate':extraction['crate'],'riders':[],'walkingDriver':'Bea'},
                 'controller':{'actor':'Bea','channel':'trained audible cues plus fitting reins','hands':1,'riding':False},
                 'turnSchedule':[x['initiative'] for x in retreat['rounds']], 'movement':[x['drive'] for x in retreat['rounds']],
                 'crewReservations':[x['actorBudgets']['Bea'] for x in retreat['rounds']],
                 'operation':{'nutrition':consumption,'harness':'owned fitted 8-lb harness; same throughout'},
                 'repair':[],'hireContract':providers['stable']},
        'EC-09':{'arrival':clock(62592),'lot':extraction['crate'],'claimants':['Expedition under licensed release; no dispute'],
                 'inspection':haven_steps[:4],'valuationDomain':'unpriced ordinary finite lot, actual buyer offer',
                 'offer':{'id':'QUOTE-1','buyer':'Pera','quantity':'one complete crate-1','priceCp':12000,
                          'issuedAt':clock(67392),'acceptedAt':clock(69192),'expiresAt':clock(72000),
                          'authority':'actual licensed buyer and seller; verified original release','chargesIncluded':[]},
                 'artifactInputs':{'applicable':False,'reason':'No artifact valuation formula invoked'},
                 'quarantine':{'reason':'required incoming licensed-material inspection, no inferred contamination','interval':span(63192,63792),'worker':'Oren','paidTransaction':'mandatory-inspection','release':'sound matching sealed crate'}},
        'EC-10':{'transactionId':[x['transactionId'] for x in tx],'payerPayee':tx,'currencyAndExactAmount':'cp, exact rational per entry',
                 'rounding':'one final direction-specific cp rounding per real payment','paymentStatus':'all listed paid',
                 'sponsor':money['sponsor'],'insurance':money['policy'],'settlement':money['settlement']},
        'EC-11':{'sceneId':'licensed-return-1','frame':{'Want':'sell the licensed lot','Leverage':'actual title, sound crate and buyer need','Limit':'only this buyer and this lot','Clock':'offer expires at hour 20','Witness':['Ione','Pera'],'authority':'Pera can spend the stated funds; Arin may accept for this charter'},
                 'channel':'shared spoken language; all actual participants hear and understand; no spell used',
                 'stakes':{'promisedResult':'accepted finite 120-gp sale','costlyAgreement':'none'},
                 'resolutionRoute':'noCheck','timing':haven_steps[3:5],'help':[],'outcome':'agreed paid sale at stated price','retries':[]},
        'EC-12':{'rawSource':standing['rawSource'],'sourceVersion':standing['sourceVersion'],'presence':standing['presence'],
                 'subjectAndBinding':{'subject':standing['subject'],'institution':standing['institution'],'synthetic':True},
                 'interpretation':standing['policy'],'initialContribution':standing['initialContribution'],
                 'events':standing['events'],'derivedView':standing['derivedView'],'history':{'originalRawUnchanged':True,'overflow':0,'duplicateReportsDelta':0}},
        'EC-13':{'institution':faction['institution'],'sourceRecord':{'publicBinding':'synthetic local guild example only; exact private original binding preserved internally'},
                 'rivalFrame':faction['rivalFrame'],'action':faction['action'],'checkpoint':faction['checkpoints'],
                 'clocks':faction['clock'],'publication':faction['audience']},
        'EC-14':{'serviceOrder':providers,'labor':haven_steps,'inputs':{'partyStock':supply,'newStock':procurement},
                 'result':'actual accepted sale, paid services and completed rest; no training or craft completion',
                 'advancement':{'mode':'milestone','achievement':'licensed-crate-retrieval','contributingCharacters':roster,
                                'largerMilestoneCompleted':False,'XP':0,'newLevels':0,'recordedProgress':True},
                 'stateCarry':snapshot(172800),'continuation':{'nextCharter':'charter-2','newInsuranceAssumed':False,'Pressure':3,'stock':procurement}},
        'EC-15':{'sourceManifest':input_receipts,'directionBindings':source['questionIds'],
                 'candidateTexts':[p.relative_to(G).as_posix() for p in OUT[:4]],
                 'audienceProjection':'Entire public synthetic envelope explicitly authored from public blocks; no original faction dossiers. Saved equality is checked here; independent whole-candidate reconstruction remains an assembly requirement.',
                 'evidenceClass':'executed reference arithmetic and source equality; qualitative facts remain authored synthetic expectations',
                 'status':'unadopted integrated example; 28 boundaries and 24 social instances still to assemble',
                 'deliveryGate':'actual final joint whole-game agreement, already-authorized push, remote verification, then careful cosmology review'}
    }
    for c in contracts['contracts']:
        fields=records[c['id']]
        check(c['id']+' instance supplies its named fields',set(c['requiredFields'])<=set(fields))
        records[c['id']]={'id':'FLOW-'+c['id'],'schemaVersion':'EX58-contract-instance-v1','version':1,
                          'expectedPredecessorVersion':0,'time':{**clock(172800),'phase':'compiled from history','sequence':0},
                          'status':'resolved synthetic record','audience':'public synthetic fixture',
                          'evidence':'authored expectation; specific arithmetic checks separately labeled',
                          'sourceBindings':[{'path':contracts_path.relative_to(G).as_posix(),'contractId':c['id'],'sha256':input_receipts[1]['sha256']}],
                          'fields':fields}

    # Exact reference arithmetic over real input intervals and finite lots, not a production runtime.
    check('21 source events preserved and instantiated',len(events)==len(source['events'])==21)
    check('event state predecessor chain is ordered',all(e['expectedPredecessorVersion']==i for i,e in enumerate(events)))
    check('event endpoints monotone',all(a['relativeEnd']<=b['relativeEnd'] for a,b in zip(events,events[1:])))
    check('five offices all bind real members',len(offices)==5 and set(offices.values())<=set(roster))
    check('outbound moving duration',sum(x['activeSeconds'] for x in moving[:2])==28800)
    check('return moving duration',sum(x['activeSeconds'] for x in moving[2:])==28800)
    check('all nontravel intervals account for Haven entry',57600+3600+60+1200+12+60+60==62592)
    check('explicit meal timing difference retained',62592-source['numericSummary']['HavenEntrySeconds']==3540)
    check('one shared second-meal/refuel pause',43200<=refills[1]['relativeStart']<refills[1]['relativeEnd']<=45000)
    check('Watch 1 remaining return time',62532-57600==4932)
    check('first Rest exact 8 hours',104592-75792==28800)
    check('first Rest sleep meets actual six-hour need',rest['firstRestSleepSeconds']==28800-960 and rest['firstRestSleepSeconds']>=21600)
    check('debt cleared before deadline',104592<144000)
    check('next Rest inside reward lockout',172800-104592==68208 and 68208<86400)
    ordered_burns=sorted(burns,key=lambda x:x['relativeStart'])
    check('light begins and ends on actual 48h limits',ordered_burns[0]['relativeStart']==0 and ordered_burns[-1]['relativeEnd']==172800)
    check('light intervals cover exactly with no overlap or gap',all(a['relativeEnd']==b['relativeStart'] for a,b in zip(ordered_burns,ordered_burns[1:])))
    check('oil consumption 8 real pints',oil_used(172800)==8,oil_used(172800))
    check('main oil exact fraction',oil_used(172800,'Lantern-A')==F(2873,360))
    check('backup uses actual reserved fraction',oil_used(172800,'Lantern-B')==F(7,360))
    for n in range(1,9):
        check(f'oil origin {n} consumed exactly once',sum((x['pints'] for x in burns if x['lotId']==f'oil-{n}'),F(0))==1)
    check('container bodies retained',sum(F(x['emptyMassLb']) for x in containers if x['id'].startswith('flask'))==2)
    check('opening manifest sums without double tare',16+64+8+2+20+48+28+2==188)
    check('opening draw and capacities',200+188==388 and 388<=600 and 188<=300 and F(188,10)<=30)
    check('route cargo upper bound remains under route capacity',F(96+188+200+8+20,10)==F(256,5)<60)
    check('floor supports all actual bodies and cargo',1000+512<=2000)
    # Return-end gross draw is still above half capacity even using an intentionally low bound:
    # subtract all consumed material and all oil from the cart, while keeping the crate and original tares.
    lower_bound=200+188+20-(40+34+1+6)
    check('draw remains Burdened throughout actual field travel',lower_bound>300,lower_bound)
    for recipient in roster+['Mule-1']:
        for day in (0,1):
            relevant=[x for x in consumption if x['recipient']==recipient and x['canonicalRelativeDay']==day]
            food=sum((x['amount'] for x in relevant if x['lotId'] in ('food-0','feed-0')),F(0))
            water=sum((x['amount'] for x in relevant if x['unit']=='pint'),F(0))
            check(f'{recipient} day {day} food actual amount',food==(10 if recipient=='Mule-1' else 2),food)
            check(f'{recipient} day {day} water actual amount',water==(24 if recipient=='Mule-1' else 8),water)
            check(f'{recipient} day {day} consumed within day',all(day*86400<=x['relativeStart']<x['relativeEnd']<=(day+1)*86400 for x in relevant))
    for lot,amount in [('food-0',16),('water-human-0',64),('feed-0',20),('water-mule-0',48),('sundries-0',2)]:
        check(lot+' finite depletion exactly once',consumed(lot,172800)==amount)
    check('retreat final counters',sum(x['EscapeAdded'] for x in retreat['rounds'])==3 and sum(x['PursuitAdded'] for x in retreat['rounds'])==0)
    for turn in retreat['rounds']:
        rects=turn['endingRectanglesFt']
        check(f"round {turn['round']} actual hostile remains in reach",rects['Arin']['x'][0]-rects['Opponent-1']['x'][1]<=5)
        check(f"round {turn['round']} exact cart/puller gap",rects['Mule-1']['x'][0]-rects['Cart-1']['x'][1]==5)
        check(f"round {turn['round']} no chamber width overflow",all(0<=v['y'][0]<v['y'][1]<=20 for v in rects.values()))
        names=[k for k in rects if k!='harness-gap']
        overlaps=[]
        for i,left in enumerate(names):
            for right in names[i+1:]:
                a,b=rects[left],rects[right]
                if max(a['x'][0],b['x'][0])<min(a['x'][1],b['x'][1]) and max(a['y'][0],b['y'][0])<min(a['y'][1],b['y'][1]):
                    overlaps.append([left,right])
        check(f"round {turn['round']} distinct bodies do not overlap",not overlaps,overlaps)
    end=retreat['rounds'][1]['endingRectanglesFt']
    check('every friendly body and frame clears actual gate',all(end[k]['x'][0]>=35 for k in roster+['Mule-1','Cart-1']))
    check('hostile remains on other side at closure',end['Opponent-1']['x'][1]<=35)
    check('Cora reaches actual gate lever',end['Cora']['x'][0]<=39<=end['Cora']['x'][1] and end['Cora']['y'][0]<=F(35,2)<=end['Cora']['y'][1])
    check('retreat attacks both miss natively',all(x['threat']['total']<13 and x['threat']['naturalDie'] not in (1,20) for x in retreat['rounds']))
    check('withdrawal lead natural20 shifts only task',25<26 and 25>=16 and retreat['rounds'][1]['EscapeAdded']==2)
    check('extraction DC actual inputs and total',sum(extraction['checkpoints'][0]['DCInputs'].values())==16 and 11+5==16)
    check('Pressure final, no reset',snapshot(172800)['Pressure']==3)
    check('same-time verification retains pre-entry Pressure',events[11]['stateAfter']['Pressure']==4 and events[12]['stateAfter']['Pressure']==3)
    check('same-time room payment follows actual entry',events[11]['stateAfter']['cashCp']==1880 and events[12]['stateAfter']['cashCp']==980)
    check('unique source causes and processed checkpoints',len({x['id'] for x in pressure_events})==len(pressure_events) and extraction['checkpoints'][0]['processedCount']==1)
    check('guild scene signed result',standing['openingScore']+standing['events'][0]['sceneCappedDelta']==1)
    check('guild research completed with actual 8h work',79200-50400==28800 and 66192<79200<86400)
    check('return checkpoint does not grant unfinished research',62592-50400==12192<28800)
    check('unique payment IDs',len(tx)==len({x['transactionId'] for x in tx}))
    running_cash=3000
    for x in sorted(tx,key=lambda x:x['relativeTime']):
        running_cash += x['settledCp'] if x['payee']=='Expedition cash' else -x['settledCp']
        check('payment affordable: '+x['transactionId'],running_cash>=0,running_cash)
    check('net uses real tax mandatory and sponsor',12000-600-200-2240==8960)
    check('sponsor actual net base',F(12000-600-200,5)==2240)
    check('unique other costs total',504+16+600+800+100==2020)
    check('true profit and reserve distribution',8960-2020==6940 and 6940-2000==4*1235)
    check('closing cash identity',running_cash==4480==3000+1480)
    check('new reserve value conserved',1480+520==2000)
    check('next stock not charged twice as old cost',money['settlement']['uniqueOtherOperatingCostsCp']==2020 and procurement['costChargedToCompletedEpisodeAgain']==0)
    check('all 28 actual skins filled once',sorted(n for xs in procurement['waterFilling']['assignment'].values() for n in xs)==[f'skin-{n:02d}' for n in range(1,29)])
    check('next packing before scheduled Rest',procurement['completion']['elapsedSeconds']<OFFSET+144000)
    check('new lamp fuel after old backup emptied',151620>=max(x['relativeEnd'] for x in burns if x['lantern']=='Lantern-B'))
    check('next lamp prep outside party Rest workers',light['nextOilPreparation']['actor']=='Mara' and 115200<=151620<151680<=172800)

    # Work conflicts are checked from explicit actor reservations, independently of the event prose.
    reservations=[]
    def reserve(actor,a,b,activity):
        reservations.append({'actor':actor,'start':a,'end':b,'activity':activity})
    for person in roster:
        for a,b in human_meals[person]:reserve(person,a,b,'light meal')
    for a,b in [(900,1800),(44100,45000)]:
        for person in ('Bea','Dane'):reserve(person,a,b,'stationary mule care')
    for x in refills:
        reserve(x['mainWorker'],x['relativeStart'],x['relativeEnd'],'two-handed refill')
        reserve(x['backupWorker'],x['relativeStart'],x['relativeEnd'],'backup light')
    for x in haven_steps:
        for person in x['actors']:reserve(person,x['relativeStart'],x['relativeEnd'],x['activity'])
    for person in roster:
        reserve(person,142200,142620,'seven actual waterskins')
        reserve(person,142620,143520,'actual packing')
    for person in sorted({x['actor'] for x in reservations}):
        rows=sorted([x for x in reservations if x['actor']==person],key=lambda x:x['start'])
        conflicts=[(a,b) for i,a in enumerate(rows) for b in rows[i+1:] if max(a['start'],b['start'])<min(a['end'],b['end'])]
        check(person+' assigned hands/work intervals do not overlap',not conflicts,conflicts)
    for x in reservations:
        if x['actor'] in roster:
            for ra,rb in [(75792,104592),(144000,172800)]:
                if max(x['start'],ra)<min(x['end'],rb):
                    check(x['actor']+' Rest compatible reservation '+x['activity'],x['activity']=='light meal')

    public={'schemaVersion':'EX58-integrated-flow-v1','id':'EX-FLOW-01-CANDIDATE',
            'status':'Draft actual record instances; exact GPT review pending',
            'completeExpeditionCandidate':False,'selectionEnabled':False,
            'evidenceBoundary':'Synthetic facts and authored outcomes, with executed finite reference arithmetic. No real campaign, save adapter, balance or whole-game approval.',
            'readingNote':'Times in prose use departure preparation as 00:00. The canonical campaign clock begins one day earlier, so preparatory payments and the previous Rest retain nonnegative timestamps.',
            'correctionsToOriginalWorkedOutline':corrections,'rosterAndBodies':bodies,
            'offices':offices,'provisions':supply,'consumption':consumption,'lighting':light,
            'route':route,'retreat':retreat,'extraction':extraction,'HavenSteps':haven_steps,
            'providers':providers,'money':money,'standing':standing,'factionWork':faction,
            'rest':rest,'nextProcurement':procurement,'events':events,'contractInstances':records,
            'actorReservations':reservations,'finalState':snapshot(172800),
            'remainingExamples':{'crossDomainBoundaryInstances':28,'originalSocialScenarioInstances':24},
            'sourceBindings':input_receipts}
    internal={'schemaVersion':'EX58-integrated-flow-director-v1','id':public['id'],
              'status':public['status'],'publicEnvelope':copy.deepcopy(public),
              'originalGPTIntegratedSequence':source,
              'originalCorrectedContracts':contracts,
              'sourceIntegrity':input_receipts,
              'privateInstitutionBinding':{'syntheticInstitution':'FX-LOCAL-GUILD',
                'exactSourceId':'merchant-guilds','meaning':'Synthetic local instance solely for this fixture, not a universal alias or new canonical institution',
                'fullOriginalRecord':next(x for x in read(R/'data/director/expedition_candidate/part06.json')['completeReputationSourceBinding']['fullOriginalFactionRecords'] if x['id']=='merchant-guilds'),
                'other43SourceRecordsUnchanged':True,'publicProjectionIncludesPrivateRecord':False},
              'newPromotions':0,'runtimeImplemented':False,'realSavesReadOrWritten':0,
              'humanBalanceConfirmed':False,'sourceInformationDeleted':0}
    check('public whole envelope matches internal projection',internal['publicEnvelope']==public)
    check('original GPT chronology preserved verbatim as structured content',internal['originalGPTIntegratedSequence']==read(seq_path)['integratedSequence'])
    check('all original input bytes unchanged',all(digest(G/x['path'])==x for x in input_receipts))
    for p,obj in zip(OUT[:2],[public,internal]):
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    player=['# One complete expedition — worked candidate', '',
            'This synthetic example follows four people, their mule and cart from a charter to the next descent. It uses the six expedition chapter drafts. It is pending GPT exact review; it does not approve a character build or supply evidence of human playtesting.', '',
            '## A timing correction made explicit', '',corrections[0]['issue'], '',corrections[0]['candidateChoice'], '',
            'The original GPT outline remains intact in the Director data. The candidate reaches Haven at **17:23:12**, finishes the Haven work at **21:03:12**, and completes its first safe Rest at **29:03:12**. The added elapsed time is 59 minutes. These are example-specific feeding stops, not a universal meal-duration rule.', '',
            '## People and responsibilities', '',
            'Arin is Leader and Quartermaster; Bea is Routekeeper and walking driver; Cora is Claimant of Record; Dane is Surgeon. Each has the stated existing abilities only. The mule pulls the cart; Bea is not riding it. External Haven staff provide their contracted work and never become extra party Actions.', '',
            '## The continuous record', '',
            '| Event | Candidate interval | Cash after event | Pressure |', '|---|---|---:|---:|']
    for e in events:
        cp=e['stateAfter']['cashCp']
        player.append(f"| {e['id']} | {hms(e['relativeStart'])}–{hms(e['relativeEnd'])} | {cp//100}.{cp%100:02d} gp | {e['stateAfter']['Pressure']} |")
    for e in events:
        player += ['',f"### {e['id']} — {hms(e['relativeStart'])}–{hms(e['relativeEnd'])}",'',e['currentCandidateNarrative']]
    player += ['', '## What was actually spent', '',
               'The eight human baskets cost 5.04 gp; the mule’s two feed/water days cost 0.16 gp. The party consumes 16 lb of food and 64 pints of water. The mule consumes 20 lb of feed and 48 pints of water. Two pounds of ordinary sundries are actually used. No second virtual Supply balance exists.', '',
               'Continuous light uses exactly eight purchased pints over 48 hours. A uses 2873/360 pints and B uses 7/360 pint during seven real one-minute refill gaps. All eight old flask bodies, weighing two pounds in total, survive. The next descent uses newly paid stock with distinct origin records.', '',
               'The cart’s initial 188 lb of provisions and containers plus its 200-lb body produce 388 lb of gross draw. The mule’s 600-lb draw limit is not exceeded; being above half that limit applies one Speed penalty. The convoy travels at 3 mph. There are no passengers hidden inside a cargo allowance.', '',
               '## Settlement', '',
               '| Item | gp |','|---|---:|','| Actual buyer payment | 120.00 |','| One applicable levy | −6.00 |',
               '| Mandatory inspection | −2.00 |','| Sponsor: 20% of the remaining 112 gp | −22.40 |',
               '| Net expedition proceeds | 89.60 |','| Unique other operating costs | −20.20 |',
               '| True profit | 69.40 |','| Agreed next reserve | −20.00 |','| Distributable profit | 49.40 |',
               '| Each of four members | 12.35 |','',
               'After distribution, the company still has 50 gp: the original 30 gp capital and the 20 gp reserve. New provisions cost 5.20 gp, leaving 44.80 gp cash and 5.20 gp in real next-expedition inventory. The reserve was an allocation, not a second expense. No insurance loss occurred and no payout is claimed.', '',
               '## What carries forward', '',
               'The guild’s witnessed licensed recovery changes its standing from Neutral 0 to Liked 1 once. It does not change every faction or reprice the accepted sale. The milestone record gains progress, with no level or XP award. Pressure remains 3. The second eight-hour Rest clears ordinary rest obligations but finishes less than 24 hours after the first beneficial completion, so it provides no second refill.', '',
               'The complete [Director records](EXPEDITION_INTEGRATED_RECORDS.md) retain the original outline and distinguish the new timing choice. The 28 cross-domain boundaries and 24 original social scenarios still need their separately assembled record instances.']
    OUT[2].write_text('\n'.join(player)+'\n',encoding='utf-8')
    director=['# Expedition walkthrough — complete synthetic records','',
              'These are authored record instances, not a production save schema or executed campaign. The public walkthrough is independently readable. Original GPT facts and times are retained in the internal JSON; FLOW-C01 explicitly proposes the feeding-stop correction for exact review.','',
              '## Source comparison','',
              '| Quantity | Original outline | Current instantiated candidate |','|---|---:|---:|',
              '| Haven entry, elapsed seconds | 59052 | 62592 |','| First Rest completion | 101052 | 104592 |',
              '| Return deadline | 172800 | 172800 |','| Cash at next departure, cp | 4480 | 4480 |',
              '| Oil consumed, pints | 8 | 8 |','',
              'The 3,540-second difference is two explicit 1,800-second supported meal stops, less the 60-second refill already inside the second stop. The canonical Watch boundaries remain fixed; they do not move to preserve the old example totals.','',
              '## Record instances','']
    for cid,record in records.items():
        name=next(c['name'] for c in contracts['contracts'] if c['id']==cid)
        director += [f'### {cid} — {name}', '', '```json',json.dumps(serial(record),ensure_ascii=False,indent=2),'```','']
    director += ['## Evidence limits','',
                 'Executed checks cover exact arithmetic, finite origin quantities, explicit actor-interval conflicts, input-byte preservation, source-event retention and public/internal projection equality. They do not authenticate a real route, worker, body, buyer or institution; those are synthetic premises. EC-04 is explicitly unused, and encounter calibration, all cross-domain boundaries and all original social scenario instances remain separate work. No card is promoted, live save migrated, source deleted or GitHub push performed.']
    OUT[3].write_text('\n'.join(director)+'\n',encoding='utf-8')
    check('saved public reparse equals complete intended envelope',read(OUT[0])==serial(public))
    check('saved internal public envelope equals separately saved public',read(OUT[1])['publicEnvelope']==read(OUT[0]))
    check('all 21 authored event paragraphs appear in player chapter',all(e['currentCandidateNarrative'] in OUT[2].read_text(encoding='utf-8') for e in events))
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'id':public['id'],
             'status':'21-event integrated candidate instantiated; 28 boundaries, 24 original social instances and full assembly/exact review remain',
             'sourceEventsPreserved':21,'candidateEvents':21,'contractInstances':15,
             'timingCorrectionPendingGPT':corrections[0],
             'checks':len(CHECKS),'failures':[x for x in CHECKS if not x['passed']],
             'scope':'Exact source equality, finite reference arithmetic, physical quantity conservation and explicit interval checks; not runtime or actual campaign verification',
             'outputs':{x.relative_to(G).as_posix():{k:v for k,v in digest(x).items() if k!='path'} for x in OUT[:4]},
             'builder':digest(Path(__file__)),'inputs':input_receipts,
             'runtimeTestsExecuted':0,'realSavesReadOrWritten':0,'newPromotions':0,
             'sourceInformationDeleted':0,'details':CHECKS}
    OUT[4].write_text(json.dumps(serial(receipt),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('details','inputs','timingCorrectionPendingGPT')},indent=2))


if __name__=='__main__':
    main()
